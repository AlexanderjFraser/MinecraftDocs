# Blaze3D

> Verified against **Minecraft 26.2** · Part XI · one draw call, from a declared pipeline to a triangle — and the two backends that can serve it.

Open Video Settings, change **Graphics API**, restart, and the game comes back
looking exactly as it did. Nothing in the *net.minecraft* packages noticed,
because nothing in them talks to a driver: they talk to `GpuDevice`,
`CommandEncoder` and `RenderPass`, and a backend under
`com/mojang/blaze3d/opengl` or `com/mojang/blaze3d/vulkan` turns that into
real calls. What made the swap possible is that the state machine left the
game. Blend mode, depth test, cull and polygon mode are *fields of a
`RenderPipeline`*, declared once and applied when the pipeline is bound, and
`RenderSystem` — the class that used to be the state machine — contains no GL
call at all. It did not vanish, though. It moved behind the backend boundary,
where `GlStateManager` still shadows every toggle and still elides the
redundant ones.

This page is the vocabulary of that boundary; the window the device is created
against is [the window](the-window.md), the frame [the frame](the-frame.md).

## The cast

| class | what it decides | thread |
|---|---|---|
| `RenderSystem` | the static holder: the device, the render thread, the frame's shared uniforms and buffers | Render thread |
| `GpuBackend` | which API is alive — window hints, creation errors, and the device itself | Render thread |
| `GpuDevice` | what exists, and what the hardware will allow | Render thread |
| `CommandEncoder` | whether a pass may open, and with which attachments | Render thread |
| `RenderPass` | that the pipeline matches the attachments before a draw is allowed | Render thread |
| `GpuSurface` | how a finished frame reaches the screen, and what vsync means | Render thread |
| `RenderPipeline` | how to rasterise: shaders, blend, depth, cull, topology — declared, never called | declaration only, read on the Render thread |
| `BufferBuilder` | vertex data, and the one part of Blaze3D not on the render thread | worker threads |

## Four objects with a façade, and one without

Four concrete, validating classes sit in `blaze3d/systems`, each over one thin
per-backend interface: the game holds the left column below, never the right.

```mermaid
flowchart TB
    GB["GpuBackend — GLFW window hints, window-creation errors, and it creates the device. The one interface with no facade"]
    subgraph F["what the game holds: the facade in blaze3d/systems, concrete and validating"]
      GD["GpuDevice"]
      CE["CommandEncoder"]
      RP["RenderPass"]
      GS["GpuSurface"]
    end
    subgraph I["one thin interface behind each"]
      GDB["GpuDeviceBackend"]
      CEB["CommandEncoderBackend"]
      RPB["RenderPassBackend"]
      GSB["GpuSurfaceBackend"]
    end
    GB -- "creates the device, and the device creates the rest" --> GD
    GD --> GDB
    CE --> CEB
    RP --> RPB
    GS --> GSB
    I --> OGL["com/mojang/blaze3d/opengl — GlStateManager shadows every toggle"]
    I --> VK["com/mojang/blaze3d/vulkan — swapchain, SPIR-V, reflection"]
```

| the game holds | the backend implements |
|---|---|
| `GpuDevice` | `GpuDeviceBackend` |
| `CommandEncoder` | `CommandEncoderBackend` |
| `RenderPass` | `RenderPassBackend` |
| `GpuSurface` | `GpuSurfaceBackend` |

`GpuBackend` is the entry point and the exception: no façade, because it is
what exists before a device does. Everything else the device creates, and it
answers for the hardware too — as one record graph, not a pile of getters.
`GpuDevice.getDeviceInfo` returns a `DeviceInfo` of `DeviceInfo.name`,
`DeviceInfo.backendName`, `DeviceInfo.isZZeroToOne`, a `DeviceFeatures` of
seven booleans, a `HintsAndWorkarounds`, a `DeviceType` and a `DeviceLimits`
whose `DeviceLimits.maxMemoryAllocationSize` caps the window size.

### Who checks what

The façade owns the **API-contract** checks and the backend owns the
resource-state ones. `CommandEncoder.createRenderPass` validates the attachment
count against `DeviceLimits.maxColorAttachments`, each attachment's
`GpuTexture.USAGE_RENDER_ATTACHMENT` bit, that the attachments are all one size,
that a render area was supplied and fits, and that no pass is already open.
`RenderPass.setPipeline` checks the pipeline's `ColorTargetState` list against
the pass's attachments in both count and `GpuFormat`. The `GpuBufferSlice`
overload of `RenderPass.setUniform` checks the offset against
`DeviceLimits.minUniformOffsetAlignment` — the plain `GpuBuffer` overload checks
nothing.

Underneath, the backend throws on its own account: `GlBuffer` for a buffer
mapped without persistent-mapping support, unreadably, unwritably or over two
gigabytes, and `GlDevice` `GpuOutOfMemoryException` on a failed allocation.
Those are not development-only, as several of the façade's own checks are.

The thread assertions are not where a reader expects them either.
`RenderSystem.assertOnRenderThread` is called from eleven classes, eight of
those sites inside `RenderSystem` itself: it guards `RenderSystem`'s own
mutable statics and the GL- and GLFW-facing classes, while `GpuDevice`,
`CommandEncoder` and `RenderPass` assert nothing at all. And
`GpuDevice.createCommandEncoder` does not create an encoder — it allocates a
fresh façade over the one long-lived encoder the backend owns, so the *is a
pass open* guard is per-façade and the game calls it fresh at every use site.

### How tight the boundary is

**OpenGL is imported by exactly fourteen files** — thirteen in
`com/mojang/blaze3d/opengl`, the fourteenth the native-library bootstrap — and
nothing else in the game references LWJGL's OpenGL bindings. Vulkan
leaks upward in two places, not one: `RenderPass` imports two Vulkan
indirect-command structs to use their size when validating an indirect buffer,
and the loader probe imports Vulkan too, while `BackendCreationException` in
`blaze3d/systems` carries seven Vulkan-named failure reasons. The two exemptions
are one, granted twice. Graphics is not all of it either: `com/mojang/blaze3d/audio`
is the OpenAL wrapper — see [the sound engine](../client/sound-engine.md).

## Vulkan is not a stub

**7,477 lines against 5,627** — the Vulkan backend against the OpenGL one,
forty classes against twenty-eight.

It is the larger of the two trees: a real swapchain, the same GLSL compiled to
SPIR-V and reflected to build bind-group layouts, five required device
extensions, nine required features, and vendor-specific GPU crash breadcrumbs in
*vulkan/checkpoints* that OpenGL has no answer to.
`VulkanBackend.checkBackendAvailable` says why it is unavailable, though only
the default preference consults it.

The backends differ in six of the seven `DeviceFeatures` flags, and only one
difference is symmetric: Vulkan hardcodes five flags true that OpenGL derives
from extensions, and the mirrored pair is the two direct multi-draw flavours,
where OpenGL has the separate one and never the interleaved one and Vulkan the
interleaved one only if the driver offers *VK_EXT_multi_draw* — so a Vulkan
device can support neither. Not every draw consults those flags: the six
multi-draw and indirect entry points gate unconditionally, `RenderPass.draw`
and `RenderPass.drawIndexed` only when a non-zero first instance is asked for,
and `RenderPass.drawMultipleIndexed` — the batched chunk path — not at all.

## A pipeline is a record, not a sequence of calls

`RenderPipeline` is declarative and effectively immutable: a
`RenderPipeline.getLocation` identity, two shader `Identifier`s, a
`ShaderDefines`, a list of `BindGroupLayout`, up to eight `ColorTargetState`,
an optional `DepthStencilState`, vertex bindings, a `PolygonMode`, a cull flag
and a `PrimitiveTopology`. `RenderPipeline.Builder` assembles one, and
composition is the static `RenderPipeline.builder` taking
`RenderPipeline.Snippet`s, which `RenderPipeline.Builder.buildSnippet`
produces rather than consumes.

Blending is a named `BlendFunction` (`BlendFunction.TRANSLUCENT`,
`BlendFunction.ADDITIVE`…) rather than a pair of loose factors, and
`RenderPipeline.Builder.build` refuses a pipeline whose colour targets do not
all share one blend function, or that binds more than sixteen vertex
attributes. Depth is reversed-Z throughout: `DepthStencilState.DEFAULT`
compares greater-or-equal and `RenderSystem.DEFAULT_DEPTH_CLEAR_VALUE` is zero.

The catalogue lives on the game side: `RenderPipelines` registers the static
pipelines — `RenderPipelines.GUI`, `RenderPipelines.LIGHTMAP`,
`RenderPipelines.SKY` and dozens more, eighty-seven in all — from a shallow
tree of snippets and the shared uniform-name sets in `BindGroupLayouts`, and
`RenderPipelines.getStaticPipelines` is the list `ShaderManager` walks to
precompile them.

## What a pipeline does not say

A `RenderPipeline` says how to rasterise. It does not say which textures to
bind or which target to draw into — and that is where a 1.21 reader's composed
stack of *RenderStateShard*s went. The answer is *client/renderer/rendertype*:
`RenderType` wraps a `RenderPipeline` with an `OutputTarget`, a
`TextureTransform`, a `LayeringTransform`, an outline variant and the batching
predicates `RenderType.canConsolidateConsecutiveGeometry` and
`RenderType.sortOnUpload`. `RenderTypes` is the static catalogue, `RenderSetup`
builds the entries, and `RenderType.prepare` resolves one into a
`PreparedRenderType` — pipeline, texture bindings, uniform slice — at draw time.

## Buffers, uniforms, and the ring that resets every frame

The resource vocabulary is small: `GpuBuffer` and `GpuBufferSlice` with usage
bits (`GpuBuffer.USAGE_VERTEX`, `GpuBuffer.USAGE_UNIFORM`,
`GpuBuffer.USAGE_MAP_WRITE`…), `GpuTexture` and `GpuTextureView` with theirs,
`GpuSampler`, `GpuFence`, `GpuFormat`, `IndexType`, `PrimitiveTopology`. Two of
those are where old habits break. Sampler state left the texture — `GpuTexture`
has no filter or wrap setters, filtering is an immutable `GpuSampler` bound per
draw, and `SamplerCache` eagerly creates all thirty-two combinations at startup
and throws if either enum ever gains a constant. And there are three shared
index buffers, not one: `RenderSystem.getSequentialBuffer` switches between a
quad buffer, a line buffer with different winding, and a one-to-one buffer.

Per-draw uniform data does not come from per-draw uniform calls; it is carved
out of ring buffers. `DynamicUniforms` and `DynamicUniformStorage` hand out
`GpuBufferSlice`s of a `MappableRingBuffer` reset once a frame,
`GlobalSettingsUniform` and `ProjectionMatrixBuffer` do the same for the
frame-wide values, and per-frame scratch comes from `TransientMemory` — one
interface, two large implementations over the shared `TransientBlockAllocator`.
Blocks are packed by hand with `Std140Builder`, sized by `Std140SizeCalculator`.

Vertex data is described by `VertexFormat` and `VertexFormatElement` (a plain
record of name, offset and `GpuFormat`) with the standard layouts in
`DefaultVertexFormat`, and built with `ByteBufferBuilder` and `BufferBuilder`
into a `MeshData`. This is the one part of Blaze3D not on the render thread:
chunk meshing runs `BufferBuilder` on worker threads and stages the result
through `StagedVertexBuffer` and `UberGpuBuffer` into a `StagingBuffer`, which
is why `SectionRenderDispatcher` has a spin-wait guarded by
`RenderSystem.isOnRenderThread`. Render targets are `RenderTarget`,
`TextureTarget` and `MainTarget`, the transient ones allocated through
`GraphicsResourceAllocator` — `CrossFrameResourcePool` implements it — and
declared in the `FrameGraphBuilder` of [visibility and the
frame graph](visibility-and-the-frame-graph.md).

## Shaders, and the reflection that checks them

`ShaderManager` loads shader sources and hands them to a backend through
`ShaderSource`, and before either backend sees one the shared
`GlslPreprocessor` resolves its *moj_import* directives and injects the
`ShaderDefines`. The Vulkan side goes further than compiling: `GlslCompiler`
runs the GLSL through shaderc to SPIR-V and `IntermediaryShaderModule`
*reflects* the result with spirv-cross, enumerating `SpvUniformBuffer`s and
`SpvSampler`s — which is what lets a declared `BindGroupLayout` be checked
against what the shader declares. It is all data on disk, alongside the chains
in [post-processing](post-processing.md).

## One draw

Every drawing class comes through this one shape: `LevelRenderer`,
`GuiRenderer`, `FeatureRenderDispatcher`, `Lightmap`, `TextureAtlas`.

```mermaid
sequenceDiagram
    participant Game as the game's own code
    participant GD as GpuDevice
    participant CE as CommandEncoder
    participant RP as RenderPass
    participant GlCE as GlCommandEncoder
    participant GpuS as GpuSurface

    Game->>GD: createCommandEncoder — a fresh facade over the one real encoder
    Game->>CE: createRenderPass with a RenderPassDescriptor
    CE->>CE: validate attachments, sizes, usage bits, render area, no pass open
    CE->>GlCE: bind an FBO from the cache, viewport, scissor, clear
    CE-->>Game: RenderPass, an AutoCloseable
    Game->>RP: setPipeline — formats must match the attachments
    Game->>RP: bindDefaultUniforms — Projection, Fog, Globals, Lighting
    Game->>RP: setVertexBuffer, setIndexBuffer, bindTexture
    Game->>RP: drawIndexed
    RP->>GlCE: look up or compile the program, apply pipeline state, bind VAO
    GlCE->>GlCE: glDrawElementsInstancedBaseVertex
    Game->>RP: close — debug groups must balance
    RP->>CE: submitRenderPass
    Note over GpuS: end of frame
    Game->>GpuS: acquireNextTexture, blitFromTexture of the main target, present
```

Everything above the `GlCommandEncoder` lane is validation or declaration.
Below it, one call is not one call: pass setup alone binds a framebuffer, sets
viewport and scissor and clears, and a single `RenderPass.drawIndexed` applies
depth, cull, blend, polygon mode and colour mask, binds a program, walks the
uniform and sampler bindings, binds a vertex array and finally draws. The
point is not that a draw is cheap. It is that *the game* never sees any of it.

The pipeline compiles lazily on its first `RenderPass.setPipeline` and is
cached by identity on the device, but no frame in a running game pays for it:
`ShaderManager` precompiles the static catalogue into that cache on every
resource reload, leaving the lazy path for pipelines outside it. Run the trace
on Vulkan and the game code is unchanged — dynamic rendering replaces the
framebuffer bind, push descriptors the uniform binding, and the swapchain
lives in `VulkanGpuSurface`.

## How a frame reaches the screen

Presentation is a four-step protocol, not a swap: `GpuSurface.configure`, then
`GpuSurface.acquireNextTexture`, then `GpuSurface.blitFromTexture`, then
`GpuSurface.present`. Vsync is not a toggle in that sequence but a
`GpuSurface.PresentMode` in the configuration: OpenGL offers a fixed pair of
modes, Vulkan whatever the driver enumerates, mailbox and relaxed FIFO included.

## Questions players ask

**Why did that draw produce nothing, and say nothing?** Because the deep
validation is a development-environment feature: the *missing uniform*,
*invalid shader program* and buffer-usage checks are gated on the in-IDE flag,
and in a shipped game the same conditions make the draw return without a word.

**Why is the game on OpenGL when I asked for Vulkan?** Because the backend is
chosen in `Minecraft`, not in Blaze3D. `PreferredGraphicsApi.getBackendsToTry`
returns an ordered *pair*, each candidate tried in turn, so every setting has
the other API as its fallback and the default is OpenGL-first. A previous
unclean shutdown downgrades twice: a Vulkan preference to the default, the
default to OpenGL.

**Why does the game care which GPU I have, when it can ask the driver?**
Because the capability record is sniffed as well as queried. `GlHeuristics`
reads the renderer and vendor strings to guess the device type, flags
GL-over-D3D12 — assumed on Windows-on-ARM whatever the string says — and flags
AMD for anisotropy problems, both of which change how the game uploads and
filters. The backend also probes the reported maximum texture size rather than
trusting it, halving a proxy allocation until the driver accepts one.

**What stops the CPU running a hundred frames ahead of the GPU?** A two-deep
submit fence, not the present: `GlCommandEncoder` rotates its transient memory
and a small fence ring on submit, and that is the pacing. Results that must come
*back* use `GpuFence` — a callback registered with
`RenderSystem.queueFencedTask`, run by `RenderSystem.executePendingTasks` once a
frame in the *gpuAsync* zone, stopping at the first fence that has not
signalled. Its one registration site is `GlCommandEncoder`'s texture readback,
and Vulkan routes the same callbacks through its own destruction queue.

> **For a 1.21-era reader.** Nearly every name you would reach for in this
> corner of the codebase has gone. `PoseStack` did *not* move, and is still here.

| you are looking for | it is now |
|---|---|
| *RenderSystem.setShader* and every state toggle on it | fields of a `RenderPipeline` |
| *ShaderInstance* | the pipeline's two shader `Identifier`s, compiled by `ShaderManager` |
| *RenderStateShard* | `RenderType` over a `RenderPipeline` |
| *VertexBuffer*, *Tesselator*, *BufferUploader* | `BufferBuilder` into a `MeshData`, then a `GpuBuffer` |
| *VertexFormat.Mode*, *VertexFormat.IndexType*, *TextureFormat* | `PrimitiveTopology`, a top-level `IndexType`, `GpuFormat` |
| *GpuDevice.getDeviceName* and its siblings | the `DeviceInfo` record |
| *Window.updateDisplay*, *setVsync* | `GpuSurface.present` and a `GpuSurface.PresentMode` |

## Where to look

`RenderSystem` for what the game holds, then `GpuDevice`, `CommandEncoder` and
`RenderPass` for the façade and its checks. `RenderPipeline.Builder` and
`RenderPipelines` for how a draw is declared, `RenderTypes` for how one is
dressed. `GlCommandEncoder` for an OpenGL draw, `VulkanCommandEncoder` for the
other answer, `GpuSurface` for where a frame ends.

---

*Rules: names, never code · how the system works, not how the code reads ·
newest version only · every backticked name passes `tools/verify_names.py`.*
