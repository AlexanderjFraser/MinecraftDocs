# Models and atlases

> Verified against **Minecraft 26.3** · Part XI · a resource pack changes one texture, and every stone block in the world redraws.

You drop a pack into the folder, move it above the default, and the screen
goes to the loading overlay for a second. The pack replaced exactly one
file, a single stone texture, and when the overlay clears every block you
can see has been thrown away and rebuilt — not just the stone. The models
for stone were byte-identical before and after, and were still re-listed,
re-parsed, re-resolved and re-baked: nothing in the reload asks what changed,
and the sprite they point at is now a different object in a different image.
**Nothing here is incremental. The unit of change is the model layer.**

Every block face, every item sprite and every particle texture starts as a
PNG in a pack, and most of them as JSON too, and ends as four vertices pointing at a rectangle
of a stitched atlas. The stages below are that journey, and they happen
inside a resource reload — [the resource
system](../foundations/resource-system.md) owns `ReloadableResourceManager`
and the barrier this rides on — and at no other time.

## The cast

| class | what it decides | thread |
|---|---|---|
| `ModelManager` | the reload's spine, and what the finished lookup sets contain | the Render thread to start and to apply, workers between |
| `AtlasManager` | which atlases exist, and it publishes their stitches for others to await | Render thread for the handshake, workers for the work |
| `SpriteLoader` | how one atlas is decoded, packed and mipmapped | workers |
| `ModelDiscovery` | which file an `Identifier` means, and what its parent chain resolved to | one worker task |
| `ModelBakery` | which unbaked model each `BlockState` and each item file bakes to | workers, in batches |
| `FaceBakery` | a quad's positions and UVs, both rotated, and its chunk layer | workers |
| `TextureManager` | who owns each `AbstractTexture`, and when an animation advances | Render thread |
| `ItemModelResolver` | which `ItemModel` a given `ItemStack` draws with | Render thread, every frame |

## The shape of the work: seventeen fans, one barrier

This is the clearest fan-out-and-barrier in the client. Seventeen independent
pieces of work start on worker threads at once, and the figure below draws
all of them, each set in two boxes: the twelve atlas stitches
`AtlasManager.reload` schedules, and the five roots `ModelManager.reload`
opens. Three of those five
are directory listings that are each themselves a fan of one task per file.
The bake waits on only two of the twelve stitches, and everything meets at the
barrier.

```mermaid
flowchart TD
    RL["a reload starts: F3+T, a pack change, or the game booting"]
    HS["Render thread: AtlasManager.prepareSharedState, then every listener's reload called"]
    subgraph W["on worker threads"]
        subgraph AT["the atlas stitches"]
            S1["the blocks and items atlases"]
            S2["the other ten atlases"]
        end
        subgraph MR["the five model roots"]
            LST["three listings, models/, blockstates/ and items/, one task per file"]
            ONE["EntityModelSet.vanilla and BuiltInBlockModels.createBlockModels"]
        end
        RES["ModelDiscovery resolves what the three listings name"]
        BAKE["the bakes: ModelBakery.bakeModels, then the BlockModel layer and fluids"]
    end
    BAR["the barrier"]
    UP["Render thread: TextureAtlas.upload, then ModelManager.apply"]
    INV["LevelExtractor.allChanged raises a flag the next frame reads"]
    RL --> HS
    HS --> AT
    HS --> MR
    LST --> RES
    S1 & RES & ONE --> BAKE
    BAKE & S2 --> BAR
    BAR --> UP --> INV
```

*The reload as a fan and its joins: the Render thread publishes the pending
stitches and calls each listener's reload, and what those schedule runs on
workers, the bake waiting on two atlases and all five roots. Everything meets
at the barrier, and what follows it runs on the Render thread in one order.*

Read it as **spread, converge, upload, invalidate**: inside the outer box,
worker threads in whatever order the joins allow; below the barrier, the
Render thread in exactly one.

## Twelve atlases and three listings, all at once

**In:** every enabled pack. **Out:** twelve stitched images, three parsed maps.

`AtlasManager` owns `AtlasManager.KNOWN_ATLASES` — twelve of them, named
in `AtlasIds` — and each is a definition file in *atlases/*, read from every
pack that ships one, not a folder scan. `SpriteSourceList` runs that file's five kinds of source in order —
`SingleFile`, `DirectoryLister`, `SourceFilter`, `Unstitcher` and
`PalettedPermutations`, registered in `SpriteSources` — and a later source
overwrites an earlier one by id, which is how a pack's own definition file
redirects a sprite; replacing a vanilla texture needs none of that, since the
pack's PNG shadows vanilla's under the same name. `SpriteLoader.loadAndStitch` decodes and reads metadata one
task per sprite, hands the results to `Stitcher` — which sorts by height
and grows by powers of two — and returns a `SpriteLoader.Preparations`,
after which `MipmapGenerator` builds the mip chain under whatever
`MipmapStrategy` the texture's own metadata asks for.

Two properties of that packing surprise people, and a third setting rides on
both of them. The mip level is clamped by
the lowest set bit of each sprite's width and height, with a warning, so **one
undersized or oddly sized texture degrades mipmapping for every sprite in the
atlas** — and only the
block atlas asks for mipmaps, the other eleven stitch flat. And sprite
padding derives from the mip level *and* the anisotropic filtering setting,
with the UVs computed inside the padded box, so anisotropy changes the
layout and every UV in the game. The mipmap slider is blunter still: it
writes the new level onto `AtlasManager` and asks for a full resource reload
when the video settings close, so every sprite in the game is decoded and
stitched again.

Meanwhile `BlockStateModelLoader` parses *blockstates/* into a
`BlockStateModel.UnbakedRoot` per `BlockState`, through
`BlockStateModelDispatcher` and `VariantSelector`, and `ClientItemInfoLoader`
parses *items/* into `ClientItem`.

### The handshake that lets listeners share a future

Reload listeners are not supposed to reach into each other, and these have
to: baking cannot resolve a texture slot without knowing where the
sprite landed. The channel that lets them is [the resource system's
shared-state
pass](../foundations/resource-system.md#the-shared-state-channel), and
`AtlasManager.PENDING_STITCH` is the only key the game declares. What
matters here is which end of it this page is: `AtlasManager` publishes a
pending stitch for all twelve atlases, and `ModelManager` awaits exactly
the two it bakes against — the blocks atlas and the items atlas — from
inside its own prepare, which lets loading and resolving the models overlap
the stitching even though the bake waits for it. `ParticleResources` awaits
the particles atlas the same way.

## Interning the models, and dropping the ones that loop

**In:** the raw *models/* map. **Out:** a `ResolvedModel` per `Identifier`.

`ModelDiscovery` is a single worker task and the narrow waist of the
pipeline. Every `Identifier` becomes one `ModelDiscovery.ModelWrapper`,
caching its resolved texture slots and its baked geometry per `ModelState`,
and `ModelDiscovery.resolve` returns the map of `ResolvedModel`, whose
helpers walk the parent chain for geometry, slots, ambient occlusion and
transforms. A model whose parent chain loops is logged and excluded, one whose parent
is missing inherits from the missing model,
and a model nothing references is parsed and never baked. In parallel,
`ModelGroupCollector` gives each block state a visual-equality group, which
is what lets `ModelManager.requiresRender` later say *that change is
invisible*: two states sharing a group id cost nothing to draw when one
becomes the other, unless their fluid state differs.

The JSON model itself is `CuboidModel`, made of `CuboidModelElement`,
`CuboidFace` and `CuboidRotation`, with `UnbakedGeometry` and
`UnbakedCuboidGeometry` between a resolved model and its quads, and
`Material`, `SpriteId`, `TextureSlots` and `MaterialBaker` are the
indirection from a model's *slot* reference to a real sprite.

## One bake per block state, and why that is affordable

**In:** resolved models and the stitched sprites. **Out:** a `ModelBakery.BakingResult`.

`ModelBakery.bakeModels` bakes once per *block state* and once per item
model file, sharing one baker whose caches are concurrent maps, and the
bakes are batched rather than scheduled individually, so this is at most
sixteen tasks per worker thread for each of the two maps, and not tens of
thousands. `ModelBakery.MissingModels` — a block
part, a block, an item and a fluid — is baked first of all, so there is
always something to substitute. Two further bakes follow: the `BlockModel`
display layer, including the hard-coded `BuiltInBlockModels`, and the
`FluidStateModelSet`.

That name is the trap this page owes you, and it is worth taking now rather
than later. **`BlockStateModel` and `BlockModel` are different interfaces in
different packages.** `BlockStateModel` is the quad source, the thing a
mesher reads. `BlockModel` is the *display* model, the thing an entity
renderer reads, and the tints and the transform a reader expects on the
interface belong to its usual implementation, `BlockStateModelWrapper`,
rather than to the interface itself. Two block tables come out of a bake
because there are two interfaces, and [block-entity
rendering](block-entity-rendering.md#the-chests-block-model-is-empty-and-there-are-two-tables-of-them)
explains which is which.

Dedup is what makes per-state baking cheap. Every state sharing an unbaked
variant gets the *same* baked object, geometry is cached per `ModelState`,
and vertex positions and material infos are interned. Multipart is the
exception that proves it: each state gets its own thin `MultiPartModel`
over a shared `MultiPartModel.SharedBakedState`, so every fence, wall, pane
and redstone-wire state really is a distinct object.

The output is a `QuadCollection` of `BakedQuad` — a ten-component record
of four positions, four packed UVs, a `Direction` recomputed from the baked
vertices, and a `BakedQuad.MaterialInfo` holding the sprite, the
`ChunkSectionLayer`, the item `RenderType` and its two glint variants, the tint index, shade and
light emission. Three things are decided here, and one of them is to put a thing off. Cull faces are rotated
at bake time — a rotated variant's north-culled quad is filed under the
rotated direction, in `UnbakedCuboidGeometry`, while `FaceBakery` rotates the
quad's vertices and UVs and applies the uvlock — so the mesher never thinks about
it. Tint is *not* resolved: the quad carries an index, and the colour
arrives later from `BlockColors` or an `ItemTintSource`. And
`QuadCollection` carries translucent and animated flags, OR-ed up through
every model wrapper, so the code that handles a block's model outside the terrain mesh — the block
outline, moving blocks, the breaking overlay, the display and item models —
can decide whether they need sorting or re-uploading without reading a quad.

### A quad's chunk layer is read out of the sprite's pixels

The most surprising decision in the pipeline is the one nobody has to make.
`FaceBakery.bakeQuad` does not take the render layer from the block or from
any per-face declaration: it asks `SpriteContents` what transparency
exists inside *that quad's UV rectangle*. The answer is a `Transparency`, two
booleans wide — are there fully transparent pixels in there, and are there
partly transparent ones — and `ChunkSectionLayer.byTransparency` reads them the
other way round: any partial alpha makes it translucent, otherwise any full
transparency makes it cutout, otherwise solid. The item render type is picked here
too, out of `Sheets`, by the partial alpha alone and by whether the sprite is on
the blocks atlas.

**One pixel** — enough alpha inside a quad's UV rectangle to move that face
out of the solid layer (`FaceBakery`, asking `SpriteContents`).

A pack author who softens one edge of a texture has changed which chunk
layer that face draws in, and so when it is sorted and how it blends with
everything behind it. There is no warning, and only one way out: a
`Material` may set `Material.forceTranslucent`, from a *force_translucent*
key beside the sprite name, which skips the scan and takes the translucent
layer whatever the pixels say. A hundred and ten of the shipped models use
it — the stained glass, mostly — and it is the exception that shows the
rule, because it exists for textures whose alpha the scan would read
correctly and whose author wants them sorted anyway.

## Every layer fails soft, and the two that do not

Missing and malformed input is a warning and a substitution at every layer
of the pipeline above, which is why a broken pack usually produces
checkerboards rather than a crash report.

| what goes wrong | what you get instead |
|---|---|
| a model file will not parse | that model alone is dropped |
| a blockstate file will not parse | that pack's copy is skipped and a lower pack's used; with none left, the block's states are dropped |
| one variant selector is malformed | that selector alone is dropped |
| a model's parent is missing | the missing model stands in as its parent |
| the parent chain is a cycle | the model is logged and excluded |
| a bake throws | `ModelBakery.MissingModels`, baked first for exactly this |
| a sprite id belongs to no atlas | the `MissingTextureAtlasSprite` checkerboard |
| a texture slot is unbound, or its chain does not resolve | the same |
| a block model draws from outside the block atlas | the model is refused and the missing model substituted |
| a block state has no entry at all | the missing model — the broadest of them, and the last |

The atlas-membership case is caught only at the moment a model is baked, and
quietly. `Minecraft.selfTest`, the startup sweep that throws rather than
warns, **only runs in a development environment**, and it looks for states
that got the missing model, not at atlases.

Two places have no soft path. If `Stitcher` cannot grow an atlas within the
device's maximum texture size it raises `StitcherException`, which becomes
a crash report listing every sprite, and mip generation is the second hard
crash site. A pack with too many textures does not degrade — it crashes.

## The barrier, and how a sprite reaches the GPU

**In:** everything above. **Out:** live lookup sets and live GPU textures.

The Render thread started the reload — every listener's shared state,
`AtlasManager.prepareSharedState` among them, then every listener's reload,
which scheduled the work — and now it does the rest. `TextureAtlas.upload` builds
the new texture and closes the old sprites, and `ModelManager.apply`
assigns the new lookup sets in one go. Underneath sits `TextureManager`, a
`PreparableReloadListener` owning every `AbstractTexture` by `Identifier` —
each atlas included — plus the `TickableTexture`s it advances, and it
registers a checkerboard texture at `MissingTextureAtlasSprite`'s location at
construction.
The GPU side belongs to [blaze3d](blaze3d.md).

How a sprite's pixels reach the atlas depends on whether it moves. A static
sprite goes into a throwaway scratch texture, is blitted into every mip
level by a render pass, and the scratch texture is closed. An animated
sprite instead keeps one *persistent* texture per unique frame for the life
of the atlas and is redrawn only when it has something new to show, through
a second pipeline entirely if the animation interpolates —
`SpriteContents.AnimationState` drives it and
`TextureAtlas.cycleAnimationFrames` steps it.

## The flag that rebuilds the world

**In:** a successful reload. **Out:** every visible section re-meshed, a frame later.

Nothing rebuilds during the reload. `LevelExtractor.allChanged` raises a
flag, and on the *next frame's* extract
`LevelRenderer.invalidateCompiledGeometry` builds a new `SectionCompiler`
from the new model sets and replaces every section with a fresh, uncompiled
one, each re-meshed as it is found visible — see
[section meshing](section-meshing.md). `SectionCompiler` is the biggest
consumer of `BlockStateModelSet.get` but far from the only one: the
block-breaking overlay, moving blocks, the in-wall screen effect, the
nether-portal sprite on the loading screen, `TerrainParticle` and
`BlockMarker` all read it too, with the HUD, `LevelExtractor`,
`FeatureRenderDispatcher` and the display table's own fallback covering the
rest, bar the development-only `Minecraft.selfTest`. The path from a set to triangles is
`BlockStateModel.collectParts` then `BlockStateModelPart.getQuads`, over
`SingleVariant`, `WeightedVariants` or `MultiPartModel` with
`SimpleModelWrapper` as the usual concrete part. None of it crosses the
network: the server has no idea what a model is.

## How an item picks its model

An item never asks for a model by name. An `ItemStack` names its model in
`DataComponents.ITEM_MODEL` — an `Identifier`, nothing else, and a stack
without one draws nothing — and that id is the whole decision: a stack whose component says *diamond sword* renders
as a diamond sword whatever item it actually is.

`ItemModelResolver` — held by `Minecraft`, called by the entity, block
entity and GUI renderers as they extract a frame — reads the component,
asks `ModelManager.getItemModel` for the baked model and
`ModelManager.getItemProperties` for the flags that travel with it, then
calls `ItemModel.update`, which appends the layers it draws to an
`ItemStackRenderState`. Both lookups fall back rather than fail: an unknown
id quietly yields the missing item model and the default
`ClientItem.Properties`, whose two flags are whether the item plays
the hand-swap animation and whether it may overflow its slot in the GUI, beside a scale for the swap
animation.

What each id maps to came from *items/*, parsed into `ClientItem` by
`ClientItemInfoLoader` and baked alongside the block models. `ItemModels`
registers **eight** kinds of unbaked item model and only one of them,
`CuboidItemModelWrapper`, draws quads of its own. `EmptyModel` draws
nothing, `CompositeModel` stacks the others, `SpecialModelWrapper` hands the
layer to a renderer instead of quads, `BundleSelectedItemSpecialRenderer` is
a bundle's peek — and the remaining three, `RangeSelectItemModel`,
`SelectItemModel` and `ConditionalItemModel`, do not draw at all. They
*branch*. `SpecialModelRenderers` covers the thirteen shapes no cuboid model
can express, from chests and banners to shields, heads, tridents and
decorated pots ([block-entity
rendering](block-entity-rendering.md#where-rendererspecial-borrows-its-geometry)
is what eleven of those thirteen borrow from). `ItemModelGenerator` is the odd
one out and by far the most-used model in the game: it extrudes a flat sprite
into geometry by tracing its alpha channel, which is what *item/generated*
means.

### What the three branching models branch on

The three are the whole of how an item's appearance changes without the item
changing, and each reads from its own registry of *properties* under
`client/renderer/item/properties`. There are thirty-three of them in three
shapes, and the shape decides which model can use it.

| the model | what the property returns | how many | examples |
|---|---|---:|---|
| `RangeSelectItemModel` | a float, thresholded against declared cut-offs | 10, in `RangeSelectItemModelProperties` | `CompassAngle`, `Damage`, `Cooldown`, `CrossbowPull`, `BundleFullness`, `UseDuration` |
| `SelectItemModel` | a value matched against declared cases | 10, in `SelectItemModelProperties` | `MainHand`, `DisplayContext`, `TrimMaterialProperty`, `ItemBlockState`, `LocalTime`, `ContextDimension` |
| `ConditionalItemModel` | a boolean, choosing one of two models | 13, in `ConditionalItemModelProperties` | `Damaged`, `Broken`, `IsUsingItem`, `IsSelected`, `IsCarried`, `FishingRodCast`, `IsKeybindDown` |

Three of them keep state, which nothing else in the baking pipeline does. A
compass and a clock each run a `NeedleDirectionHelper`, a damped follower
updated once per tick for the baked model rather than per stack, and a
compass that has a target damps only when its owner is the local player — which is the wobble, and a
model may declare *wobble: false* and get the raw angle instead. `LocalTime` is
the third, and it re-reads the wall
clock at most once a second, which is why a chest *item* notices Christmas
and [a placed
chest](block-entity-rendering.md#one-partial-tick-for-the-whole-world) does
not.

`DisplayContext` is the row worth knowing for a different reason: it is what
lets one item file draw one thing in your hand, another in a frame and a
third in the GUI, and the context comes from whoever is drawing rather than
from the stack.

One rule is enforced here. A block model may only use the
block atlas, and a cuboid *item* model must draw every quad from a single
atlas — items or blocks, not both. A model that mixes them throws, the
exception is caught upstream, and the item falls back to the missing model.
Where the stack itself comes from is [items and
stacks](../items/items-and-stacks.md).

## Questions players ask

**Why does lag slow the water down but the pause menu not stop it?** Because
animations do not advance once per tick. `TextureManager.tick` sits outside
the client's catch-up tick loop, so a laggy client advances every animation
by one tick however many ticks it just owed. Pausing does not touch it —
`DeltaTracker` keeps handing out ticks with the menu open — and the one thing
that does stop the water is `/tick freeze`, because the guard on that call, beside a tick being owed, is
`Minecraft.isLevelRunningNormally`.

**Can I look at the atlas?** Yes, and it is the fastest way to understand
this page. `Options.keyDebugDumpDynamicTextures` runs
`TextureManager.dumpAllSheets`, which writes every atlas in the game to disk
under the game directory with a text listing of each sprite's position and
size beside it. A shared-constant flag,
`SharedConstants.DEBUG_DUMP_TEXTURE_ATLAS`, makes every atlas dump itself at
each upload too, without the keypress.

> **For a 1.21-era reader.** *BlockModelShaper* is now `BlockStateModelSet`;
> *BlockElement* and *BlockElementFace* are `CuboidModelElement` and
> `CuboidFace`; *BlockModelDefinition* is `BlockStateModelDispatcher`; and
> *BlockRenderDispatcher* and *ItemRenderer* are gone with no successor of that
> name. One trap: `BlockModel` still exists and now means something entirely
> different — the display model above, where the JSON one is `CuboidModel`.

## Where to look

`ModelManager.reload` for the shape of the pipeline, then
`AtlasManager.prepareSharedState` for the handshake that makes it parallel.
`ModelDiscovery` for resolution, `ModelBakery.bakeModels` for baking,
`SpriteLoader.loadAndStitch` and `Stitcher` for the atlas,
`FaceBakery.bakeQuad` for where a face's layer is decided, and
`ItemModelResolver` and `BlockStateModelSet.get` for the two ways out.

---

*Rules: names, never code · how the system works, not how the code reads ·
newest version only · every backticked name passes `tools/verify_names.py`.*
