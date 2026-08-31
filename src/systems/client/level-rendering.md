# Level rendering

> Verified against **Minecraft 26.2** · Part X · a block is placed, and the section it lives in is re-meshed, uploaded and drawn.

## Responsibility

Turning a world into triangles. This page covers the client's terrain
pipeline — which sections are visible, which need re-meshing, what a
mesher is allowed to read, how the result gets onto the GPU, and the
order in which the passes of a frame are declared and executed.

The one sentence a player would recognise: *terrain pops in as you fly,
and a block you place appears instantly.*

The headline for a 1.21-era reader: **the level renderer was cut in half.**
Everything about *the world* — dirty flags, frustum application,
gathering entities and block entities — moved into
the new `LevelExtractor`, in *client/renderer/extract*. `LevelRenderer`
keeps only GPU-facing work and reads nothing but render state.
*LevelRenderer.renderLevel* does not exist; the method is
`LevelRenderer.render`.

## The data it owns

### The extract side

- **`LevelExtractor`** — the world-facing half. It owns the dirty API
  (`LevelExtractor.blockChanged`, `LevelExtractor.setBlocksDirty`,
  `LevelExtractor.setSectionDirty`,
  `LevelExtractor.setSectionDirtyWithNeighbors`,
  `LevelExtractor.setSectionRangeDirty`, `LevelExtractor.allChanged`),
  the frustum step (`LevelExtractor.applyFrustum`, which asserts it is on
  the client thread), and the gathering passes
  `LevelExtractor.extractVisibleEntities` and
  `LevelExtractor.extractVisibleBlockEntities`. Its output is a
  `LevelRenderState`.
- **`SectionUpdateTracker`** — where dirtiness now lives, *not* on the
  render section. Each entry is a
  `SectionUpdateTracker.SectionDirtyState` with
  `SectionUpdateTracker.SectionDirtyState.isDirty` and
  `SectionUpdateTracker.SectionDirtyState.isDirtyFromPlayer`;
  `SectionUpdateTracker.hasAllNeighbors` is the gate a never-compiled
  section must pass.
- **`RotatingSectionStorage`** — a fixed ring of section slots,
  re-homed by `RotatingSectionStorage.repositionCenter` as the camera
  moves. Both `ViewArea` and `SectionUpdateTracker` are built on it.
- **`RenderRegionCache`** and **`RenderSectionRegion`** — the snapshot a
  mesher reads: a 3×3×3 grid of `SectionCopy`, each holding a *copy* of
  one section's `PalettedContainer` plus an immutable map of the chunk's
  block entities.
- **`LevelRenderState`** — the frame's product:
  `LevelRenderState.sectionUpdateRenderStates`,
  `LevelRenderState.entityRenderStates`,
  `LevelRenderState.blockEntityRenderStates`,
  `LevelRenderState.blockOutlineRenderState`,
  `LevelRenderState.blockBreakingRenderStates`,
  `LevelRenderState.skyRenderState`,
  `LevelRenderState.weatherRenderState`,
  `LevelRenderState.particlesRenderState`, plus `CameraRenderState` and
  `OptionsRenderState`.

### The render side

- **`LevelRenderer`** — `LevelRenderer.visibleSections` and
  `LevelRenderer.nearbyVisibleSections`, the `LevelRenderer.viewArea`,
  the `LevelRenderer.sectionOcclusionGraph`, the
  `LevelRenderer.sectionRenderDispatcher`, the
  `LevelRenderer.submitNodeStorage`, the render targets in
  `LevelRenderer.targets` (a `LevelTargetBundle`), and the translucency
  bookkeeping `LevelRenderer.lastTranslucentSortBlockPos` and
  `LevelRenderer.translucencyResortIterationIndex`.
- **`SectionOcclusionGraph`** — the reachability BFS.
  `SectionOcclusionGraph.GraphState` (published atomically),
  `SectionOcclusionGraph.Node`, an `Octree` of sections,
  `SectionOcclusionGraph.update`,
  `SectionOcclusionGraph.scheduleFullUpdate`,
  `SectionOcclusionGraph.runPartialUpdate`,
  `SectionOcclusionGraph.addSectionsInFrustum`,
  `SectionOcclusionGraph.schedulePropagationFrom`, and the smart-cull
  threshold `SectionOcclusionGraph.MINIMUM_ADVANCED_CULLING_DISTANCE`.
  The per-section visibility data it walks is a `VisibilitySet`, produced
  at compile time by `VisGraph`.
- **`SectionRenderDispatcher`** — the mesher.
  `SectionRenderDispatcher.RenderSection` (with
  `SectionRenderDispatcher.RenderSection.sectionMesh`,
  `.compileAsync`, `.compileSync`, `.resortTransparency`,
  `.getVisibility`, `.reset`), the work queue
  `SectionTaskDynamicQueue`, the scratch buffers
  `SectionBufferBuilderPack` / `SectionBufferBuilderPool`, and the GPU
  side: one `UberGpuBuffer` pair per layer fed through a `StagingBuffer`,
  drained by `SectionRenderDispatcher.uploadTerrainBuffersToGpu`.
- **`SectionCompiler`** — what runs on a worker.
  `SectionCompiler.compile` produces `SectionCompiler.Results`
  (`SectionCompiler.Results.renderedLayers`,
  `.blockEntities`, `.visibilitySet`, `.transparencyState`), which
  becomes a `CompiledSectionMesh`. The sentinels
  `CompiledSectionMesh.UNCOMPILED` and `CompiledSectionMesh.EMPTY` are
  the two states a section can be in without geometry.
- **`ChunkSectionLayer`** — `ChunkSectionLayer.SOLID`,
  `ChunkSectionLayer.CUTOUT`, `ChunkSectionLayer.TRANSLUCENT`. Three,
  and only three. `ChunkSectionLayerGroup.OPAQUE` and
  `ChunkSectionLayerGroup.TRANSLUCENT` are the two draw groups, batched
  into a `ChunkSectionsToRender`.
- **The frame graph** — `FrameGraphBuilder.addPass`,
  `FrameGraphBuilder.importExternal`,
  `FrameGraphBuilder.createInternal`, `FrameGraphBuilder.execute`, and
  the per-pass declarations `FramePass.reads`,
  `FramePass.readsAndWrites`, `FramePass.executes`. Targets are named in
  `LevelTargetBundle` (`LevelTargetBundle.main`, `.translucent`,
  `.itemEntity`, `.particles`, `.weather`, `.clouds`,
  `.entityOutline`).

## When it runs

Everything is on the client thread except meshing, which goes to
`Util.backgroundExecutor` — the shared background pool, not a dedicated
chunk-builder pool. Concurrency is throttled not by thread count but by
buffers: `SectionRenderDispatcher` submits one task-runner per schedule,
and each runner must acquire a `SectionBufferBuilderPack` from
`SectionBufferBuilderPool` before it can work.

A mesher may read only its `RenderSectionRegion`. Block states and block
entities are snapshotted (that is what `SectionCopy` is for — the compile
runs for an unbounded time while the client thread keeps applying block
updates); tints and light are read live through the region's references
to `ClientLevel` and the light engine.

The result does not come back through the render thread as a callback.
The worker writes into a `StagingBuffer` under a lock, spinning if it is
full; the client thread drains it into the per-layer `UberGpuBuffer`s in
the *uploadTerrainBuffers* step at the end of `LevelRenderer.render`.

## The trace: a block is placed

```mermaid
sequenceDiagram
    participant MPGM as MultiPlayerGameMode
    participant CL as ClientLevel
    participant LX as LevelExtractor
    participant SUT as SectionUpdateTracker
    participant LR as LevelRenderer
    participant SRD as SectionRenderDispatcher
    participant W as (worker)
    participant SC as SectionCompiler

    MPGM->>CL: setBlock — the client predicts the placement
    CL->>LX: setBlocksDirty — but only if ModelManager.requiresRender
    CL->>LX: blockChanged — playerChanged, from the update flags
    LX->>SUT: setDirty for each of the 27 sections in the halo

    Note over LX: next frame, extract
    LX->>LR: walk visibleSections only
    LX->>LX: RenderRegionCache.createRegion — 27 SectionCopy snapshots
    LX->>LX: SectionUpdateRenderState added; the dirty flag is cleared

    Note over LR: same frame, after the frame graph has executed
    LR->>SRD: compileAsync (or compileSync, per PrioritizeChunkUpdates)
    SRD->>W: queued nearest-first; a buffer pack must be free
    W->>SC: compile — every block in the section, into up to three layers
    SC-->>W: Results — meshes, block entities, VisibilitySet, sort state
    W->>SRD: append to the staging buffer, spin-wait if it is full
    Note over LR: at the end of a later frame
    LR->>SRD: uploadTerrainBuffersToGpu — the mesh becomes live
    SRD->>LR: schedulePropagationFrom — the occlusion graph re-walks
```

Two things in that diagram are the whole point. First, **only visible
sections are re-meshed**: `LevelExtractor` iterates
`LevelRenderer.visibleSections`, so a block change behind you costs
nothing until the occlusion graph makes that section visible again — the
dirty flag simply waits. Second, **the swap is atomic and late**: a
section keeps drawing its old mesh until every layer's vertex *and* index
buffer has reported uploaded, so there is no frame in which a rebuilt
section is missing.

## The passes of a frame

`LevelRenderer.render` builds a graph, then executes it. The passes, in
declaration order: *clear*, *sky* (`LevelRenderer.addSkyPass`), *main*
(`LevelRenderer.addMainPass`), the entity-outline post chain, *clouds*
(`LevelRenderer.addCloudsPass`), *weather*
(`LevelRenderer.addWeatherPass`), the transparency post chain, and
*always on top* (`LevelRenderer.addAlwaysOnTopPass`). Inside the main
pass: opaque terrain, then `FeatureRenderDispatcher.PreparedFrame.executeSolid`,
then depth copies, then
`FeatureRenderDispatcher.PreparedFrame.executeTranslucent` and
`FeatureRenderDispatcher.PreparedFrame.executeOutline`, then translucent
terrain, then
`FeatureRenderDispatcher.PreparedFrame.executeTranslucentAfterTerrain`. After the graph executes,
`LevelRenderer.compileSections` queues this frame's rebuilds,
`SectionRenderDispatcher.uploadTerrainBuffersToGpu` drains the staging
buffer, and `SectionOcclusionGraph.update` re-walks reachability.

Note the ordering: **terrain is drawn before the sections queued this
frame are compiled.** Even the "prioritise chunk updates" option only
guarantees the mesh exists by the end of frame *N*; it appears in frame
*N+1*.

## Interfaces

- **Called by:** `GameRenderer.renderLevel` — see
  [the frame](the-frame.md).
- **Calls into:** [blaze3d](blaze3d.md) for every draw;
  `BlockStateModelSet` and `ModelBlockRenderer` for the meshing itself —
  see [models and atlases](models-and-atlases.md); the entity and block
  entity submit path in [entity rendering](entity-rendering.md).
- **Crosses the network as:** nothing directly. Block changes arrive as
  the packets described in
  [what the client is told](../networking/what-the-client-is-told.md),
  and `ClientLevel.sendBlockUpdated` is what turns them into dirty
  sections.
- **Data-driven by:** the models and the atlas, via `SectionCompiler`'s
  `BlockStateModelSet`; and `Options` — render distance, ambient
  occlusion, `PrioritizeChunkUpdates`, section fade-in time.

## Invariants and surprises

- **`LevelRenderer` no longer touches the level.** Its only
  `ClientLevel` reference is a parameter to
  `LevelRenderer.invalidateCompiledGeometry`. Every block-state read in
  the render path is somebody else's.
- **A dirty section that is not visible is never rebuilt** — and its
  flag is kept indefinitely, so it rebuilds the instant it becomes
  visible.
- **A never-compiled section additionally waits for its neighbours.**
  `SectionUpdateTracker.hasAllNeighbors` requires the surrounding chunks
  to be full and lit. A *re*compile skips that check entirely.
- **There are only three chunk layers.** Cutout-mipped and tripwire are
  gone: mipping is a sampler concern
  (`LevelRenderer.chunkLayerSampler`, rebuilt when the filtering options
  change) and tripwire is an ordinary cutout. A quad's layer is decided
  at model-bake time and carried on `BakedQuad.MaterialInfo.layer`.
- **All sections of a layer live in one GPU buffer.**
  `ChunkSectionsToRender` batches draws by buffer identity and issues one
  multi-draw per group, with the per-section transform arriving as a
  uniform slice — not one draw call per section.
- **Translucent batching deliberately defeats itself.** The grouping hash
  skips the buffer contribution for the translucent layer, so those
  sections stay in visit order and are drawn reversed. Back-to-front
  correctness beats batching.
- **Translucency is re-sorted on a rolling budget.** Everything within a
  short radius, plus a round-robin slice of the visible set, is
  considered each frame; a resort only fires if the point of view
  actually changed.
- **Buffer-pool exhaustion is signalled by a null.** A worker that cannot
  acquire a scratch pack puts its task back on the queue. That is the
  throttle: the number of concurrently meshing sections equals the number
  of packs, however many threads exist.
- **The task queue is nearest-first with a starvation guard.** A
  recompile only beats a first-time compile while a small quota lasts,
  so terrain still fills in while you are placing blocks.
- **An uncompiled section is opaque to the BFS; an empty one is
  transparent.** That asymmetry is why terrain reveals itself outward as
  it compiles rather than all at once.
- **Beyond a threshold distance, smart cull adds a ray march** back
  toward the camera, rejecting a neighbour if any section along the way
  is missing.
- **The frame graph culls passes and aliases targets.** A pass that
  does not transitively feed an imported external resource is not
  executed at all — the clouds pass simply does not exist in a frame with
  clouds off. The five internal targets are created only when the
  transparency post chain is active; otherwise clouds and weather write
  straight to the main target.
- **Sections fade in, but only far ones.**
  `SectionRenderDispatcher.RenderSection.setFadeDuration` is non-zero
  only for distant sections that were not previously empty — so a block
  you place snaps in and streaming terrain fades.
- **Directional shading is per-dimension data now.** Shading reads a
  `CardinalLighting` record supplied by the dimension, not a fixed table.
- **Names a 1.21-era reader will hunt for and not find:**
  *ChunkRenderDispatcher* and *RenderChunk* (now `SectionRenderDispatcher`
  and its nested `SectionRenderDispatcher.RenderSection`), *CompiledChunk* (now `CompiledSectionMesh`),
  *RenderType.chunkBufferLayers* and the five chunk render types (now
  three `ChunkSectionLayer`s), *LevelRenderer.renderChunkLayer*,
  *LevelRenderer.renderLevel*, *LevelRenderer.setupRender*, every dirty
  method on `LevelRenderer`, *RenderChunkRegion* (now
  `RenderSectionRegion`), *BlockRenderDispatcher*, *LiquidBlockRenderer*
  (now `FluidRenderer`) and *BlockAndTintGetter.getShade*. `ViewArea`,
  `VisGraph`, `Octree` and `Frustum` all survive.

## Where to look

`LevelExtractor.extract` for the world half, then `LevelRenderer.render`
for the graph. `SectionUpdateTracker` for where dirtiness lives.
`SectionRenderDispatcher.RenderSection.compileAsync` and
`SectionCompiler.compile` for the mesher. `SectionOcclusionGraph.update`
for what is visible. `ChunkSectionsToRender` for how it is finally drawn.

---

*Rules: names, never code · how the system works, not how the code reads ·
newest version only · every backticked name passes `tools/verify_names.py`.*
