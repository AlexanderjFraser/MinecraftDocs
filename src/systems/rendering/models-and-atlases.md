# Models and atlases

> Verified against **Minecraft 26.2** · Part XI · a resource pack changes one texture, and every stone block in the world redraws.

## Responsibility

Turning JSON into quads. Every block face, every item sprite, every
particle texture starts as a file in a resource pack and ends as four
vertices pointing at a rectangle of a stitched atlas. This page is that
journey: how the atlases are built, how models are resolved and baked,
what happens when one is missing, and what a reload actually costs.

The one sentence a player would recognise: *installing a resource pack.*

The headline for a 1.21-era reader: **this subsystem was renamed and
re-packaged wholesale.** *BakedModel*, *ModelResourceLocation*,
*BlockModelShaper*, *ItemModelShaper*, *BlockRenderDispatcher*,
*ItemRenderer*, *BlockElement*, *AtlasSet* — all gone. And `BlockModel`
still exists but now means something entirely different.

## The data it owns

### The loader

- **`ModelManager`** — the reload listener. It ends up holding
  `ModelManager.blockStateModelSet`, `ModelManager.blockModelSet`,
  `ModelManager.fluidStateModelSet`,
  `ModelManager.bakedItemStackModels`, `ModelManager.itemProperties`,
  `ModelManager.modelGroups` and `ModelManager.missingModels`. Its
  lookups are `ModelManager.getBlockStateModelSet`,
  `ModelManager.getBlockModelSet`, `ModelManager.getFluidStateModelSet`,
  `ModelManager.getItemModel`, `ModelManager.getItemProperties`,
  `ModelManager.entityModels` and `ModelManager.requiresRender`.
- **`ModelBakery`** — `ModelBakery.bakeModels` produces a
  `ModelBakery.BakingResult`
  (`ModelBakery.BakingResult.blockStateModels`,
  `.itemStackModels`, `.itemProperties`, `.missingModels`). It also owns
  the block-breaking overlay constants `ModelBakery.DESTROY_STAGES`,
  `ModelBakery.DESTROY_TYPES` and `ModelBakery.DESTROY_STAGE_COUNT`, and
  the two fire sprites. `ModelBakery.MissingModels` is a record of
  **four** separate fallbacks — a block part, a block, an item and a
  fluid — baked before anything else.
- **`ModelDiscovery`** — parent-chain resolution. Every `Identifier` is
  interned to one `ModelDiscovery.ModelWrapper`, which caches resolved
  texture slots and per-`ModelState` baked geometry.
  `ModelDiscovery.resolve` returns the map of `ResolvedModel`, whose
  parent-walking helpers are `ResolvedModel.getTopTextureSlots`,
  `ResolvedModel.getTopAmbientOcclusion`,
  `ResolvedModel.getTopGeometry` and `ResolvedModel.getTopTransforms`.
- **`BlockStateModelLoader`** — parses *blockstates/* into
  `BlockStateModel.UnbakedRoot` per `BlockState`, through
  `BlockStateModelDispatcher` (`BlockStateModelDispatcher.SimpleModelSelectors`
  and `BlockStateModelDispatcher.MultiPartDefinition`) and
  `VariantSelector`.
- **`ClientItemInfoLoader`** — parses *items/* into `ClientItem`.
- **`ModelGroupCollector`** — assigns a visual-equality group per block
  state, which is what makes `ModelManager.requiresRender` able to say
  "that state change is invisible, skip the rebuild".

The JSON model itself is now `CuboidModel`, with `CuboidModelElement`,
`CuboidFace` and `CuboidRotation`; `UnbakedGeometry` and
`UnbakedCuboidGeometry` are the interface between a `ResolvedModel` and
its quads, and `FaceBakery.bakeQuad` is where a face becomes one. The
baked output is a `QuadCollection` of `BakedQuad` — a ten-component
record carrying four positions, four packed UVs, a `Direction`
recomputed from the baked vertices, and a `BakedQuad.MaterialInfo`
(sprite, `ChunkSectionLayer`, item `RenderType`, tint index, shade,
light emission).

`ItemModelGenerator` is the odd one out and the most-used model in the
game: it takes a flat sprite and extrudes it into geometry by tracing the
alpha channel, which is what *item/generated* means.

### The atlas

- **`AtlasManager`** — a reload listener *and* a `SpriteGetter`. It owns
  `AtlasManager.KNOWN_ATLASES` (thirteen of them, named in `AtlasIds`)
  and publishes `AtlasManager.PENDING_STITCH` — the shared-state key that
  lets `ModelManager` consume the stitch results without reaching into
  another listener.
- **`SpriteLoader`** — `SpriteLoader.loadAndStitch`, producing a
  `SpriteLoader.Preparations`.
- **`Stitcher`** — the packer. `Stitcher.registerSprite`,
  `Stitcher.stitch`, and `StitcherException` when it cannot fit.
- **`TextureAtlas`** and **`TextureAtlasSprite`** — the GPU side, with
  `SpriteContents` holding the mip chain and
  `SpriteContents.AnimationState` driving animated frames.
  `TextureAtlas.upload`, `TextureAtlas.uploadInitialContents`,
  `TextureAtlas.cycleAnimationFrames`. `MipmapGenerator` builds the mip
  chain, under a `MipmapStrategy` a texture's metadata can override.
- **`TextureManager`** — the layer under all of it: a
  `PreparableReloadListener` owning every `AbstractTexture` by
  `Identifier`, including each atlas, and the set of `TickableTexture`s
  it advances. `MissingTextureAtlasSprite` is the checkerboard it
  registers at construction.
- **The atlas definition files** — `SpriteSourceList`, `SpriteSources`,
  and the five source types `SingleFile`, `DirectoryLister`,
  `SourceFilter`, `Unstitcher`, `PalettedPermutations`.
- **`Material`, `SpriteId`, `MaterialBaker`, `TextureSlots`** — the
  indirection from a model's `#slot` reference to a real sprite. There
  are two `MaterialBaker`s, and which one is used is what enforces the
  block-atlas rule below. `Sheets` names the non-block atlases and their
  mappers.

### The consumers

`BlockStateModelSet.get` is what the mesher calls;
`BlockStateModel.collectParts` yields `BlockStateModelPart`s and
`BlockStateModelPart.getQuads` yields the quads, with `SimpleModelWrapper`
as the usual concrete part. `SingleVariant` and `WeightedVariants` are
the two shapes of an unbaked model entry and `MultiPartModel` is the
multipart form. `Variant` and `VariantMutator` carry the rotation and
UV-lock. Items go through `ItemModelResolver` and `ItemModel` into an
`ItemStackRenderState`; the model is chosen by the stack's
`DataComponents.ITEM_MODEL`. Special-cased renderers come from
`SpecialModelRenderers` — thirteen of them, including chests, banners,
shields, heads, tridents, conduits, bells and decorated pots.

## When it runs

Only at a resource reload — see
[the resource system](../foundations/resource-system.md) for
`ReloadableResourceManager`, `PreparableReloadListener` and the barrier
semantics this rides on. What is new here is the shared-state handshake:
`PreparableReloadListener.prepareSharedState` runs for *every* listener
on the client thread before *any* reload task starts, and `AtlasManager`
uses it to publish thirteen pending stitch futures. The *ordering* is
still guaranteed the old way — the reload chains each listener's barrier
onto the previous one, and `AtlasManager` is registered before
`ModelManager` — but the handshake means `ModelManager` never has to
reach for another listener's object.

The work, by stage:

1. **Workers, in parallel** — thirteen atlas stitches (one task per
   sprite for decode and metadata, then a single-threaded stitch per
   atlas, then mip generation), plus the *models/*, *blockstates/* and
   *items/* listings, one task per file.
2. **One worker task** — `ModelDiscovery` walks parent chains and
   interns everything; in parallel, `ModelGroupCollector` builds the
   visual-equality groups.
3. **Workers, in parallel batches** — `ModelBakery.bakeModels`: one bake
   per *block state* and one per item model file, sharing one baker whose
   caches are concurrent maps. The bakes are batched rather than
   scheduled individually, so this is tens of tasks, not tens of
   thousands. Two further bakes follow: the `BlockModel` display layer —
   including the hard-coded `BuiltInBlockModels` — and the
   `FluidStateModelSet`.
4. **The barrier**, then the client thread: the atlas uploads
   (`TextureAtlas.upload`), then `ModelManager.apply` assigns the new
   lookup sets.
5. **After the whole reload succeeds** — `LevelExtractor.allChanged`
   raises a flag; on the *next frame's* extract,
   `LevelRenderer.invalidateCompiledGeometry` builds a new
   `SectionCompiler` from the new model sets and every section is
   re-meshed. See [level rendering](level-rendering.md).

## The trace: a resource pack changes a texture

```mermaid
sequenceDiagram
    participant KH as KeyboardHandler
    participant M as Minecraft
    participant AM as AtlasManager
    participant SL as SpriteLoader
    participant MM as ModelManager
    participant MB as ModelBakery
    participant TA as TextureAtlas
    participant LX as LevelExtractor

    KH->>M: F3+T — reloadResourcePacks
    M->>AM: prepareSharedState — publish thirteen pending stitches
    par on worker threads
        AM->>SL: loadAndStitch(blocks atlas)
        SL->>SL: SpriteSourceList runs each source; the pack's PNG wins
        SL->>SL: Stitcher — sort by height, grow by powers of two
    and
        MM->>MM: parse models/, blockstates/, items/
    end
    MM->>MM: ModelDiscovery — intern, resolve parents, drop cycles
    MM->>MB: bakeModels — one bake per BlockState, in batches
    MB->>SL: MaterialBaker resolves each #slot to the NEW sprite
    MB->>MB: FaceBakery writes the new UVs into each BakedQuad
    Note over AM,MM: the barrier
    AM->>TA: upload — new GpuTexture, old sprites closed
    MM->>MM: apply — the new BlockStateModelSet goes live
    M->>LX: allChanged — a flag; next frame rebuilds the SectionCompiler
```

The point the trace makes: **changing one texture rebuilds the entire
model layer.** Nothing is incremental. The models for stone were
byte-identical before and after, but they are re-parsed, re-resolved and
re-baked anyway, because the sprite they point at is a different object
with different UVs.

## Interfaces

- **Called by:** `SectionCompiler` for terrain, and eight other readers
  of `BlockStateModelSet` — the block-breaking overlay, moving blocks,
  the in-wall screen effect, the nether-portal sprite on the loading
  screen, and `TerrainParticle` / `BlockMarker` for the break-particle
  sprite. `BlockEntityRenderDispatcher` and `ItemModelResolver` cover
  everything else.
- **Calls into:** the resource manager for files, and
  [blaze3d](blaze3d.md) for the atlas texture and the sprite blit.
- **Crosses the network as:** nothing. The server has no idea what a
  model is.
- **Data-driven by:** *models/*, *blockstates/*, *items/*, *atlases/* and
  *textures/* in every enabled resource pack, plus
  `DataComponents.ITEM_MODEL` on the stack.

## Invariants and surprises

- **A quad's render layer is read out of the sprite's pixels.**
  `FaceBakery` asks `SpriteContents` what transparency actually exists
  inside that quad's UV rectangle and picks solid, cutout or translucent
  from the answer. A texture with one translucent pixel changes which
  chunk layer the face is drawn in.
- **Baking is per block state, and dedup is what makes it affordable.**
  Every state sharing an unbaked variant gets the *same* baked model
  object, geometry is cached per `ModelState`, and vertex positions and
  material infos are interned. Multipart is the exception: each state
  gets its own thin `MultiPartModel` over a shared
  `MultiPartModel.SharedBakedState`, so every fence, wall, pane and
  redstone-wire state really is a distinct object.
- **A cyclic model is dropped, not fatal.** A model whose parent chain
  never reaches a root is logged and excluded. Unreferenced models are
  parsed and never baked.
- **Missing things fail soft at a dozen separate layers** — an
  unparseable model, an unparseable blockstate file, one bad variant
  selector, an unparseable item file, a missing parent, a cycle, a bake
  that throws, a sprite id in no atlas, an unbound `#slot`, an
  unresolvable slot chain, a block model reaching outside the block
  atlas, and finally a block state with no entry at all. Every one is a
  warning and a substitution. The startup sweep that would catch the last
  case, `Minecraft.selfTest`, **only runs in a development environment** —
  and there it throws rather than warns.
- **A pack with too many textures crashes the game.** If the stitcher
  cannot grow the atlas within the device's maximum texture size it
  throws, and that becomes a crash report listing every sprite. Mip
  generation is a second hard-crash site. There is no graceful
  degradation on either.
- **One small texture degrades mipmapping for the whole atlas.** The mip
  level is clamped to the smallest sprite's power of two, with a warning.
  And only the block atlas requests mipmaps at all; the other twelve
  stitch flat.
- **Anisotropic filtering changes the atlas layout.** Sprite padding is
  derived from the mip level *and* the anisotropy setting, and the UVs
  are computed inside that padded box. The mipmap slider changes it too,
  by rebuilding the `AtlasManager` outright.
- **Static sprites are uploaded by drawing; animated ones are not.** A
  static sprite goes into a throwaway scratch texture and is blitted into
  every mip level of the atlas by a render pass, then the scratch texture
  is closed. An animated sprite instead keeps one *persistent* texture
  per unique frame for the life of the atlas, and is redrawn only when it
  has something new to show — through a second pipeline entirely if the
  animation interpolates.
- **Animations do not advance once per tick.** `TextureManager.tick` sits
  outside the client's catch-up tick loop and is gated on the level
  running normally, so a laggy client advances every animation by exactly
  one frame no matter how many ticks it ran, and a paused single-player
  game freezes them.
- **Blocks have two model layers with different jobs.**
  `BlockStateModel` is the quad source for the mesher and for particles;
  `BlockModel` — a different interface in a different package, reached
  through `ModelManager.getBlockModelSet` — is the *display* model for
  item frames, block entities and a dozen entity renderers. Tints and a
  transform belong to its usual implementation,
  `BlockStateModelWrapper`, not to the interface.
- **Cull faces are rotated at bake time.** A rotated variant's
  `cullface: north` quad is filed under the rotated direction — in
  `UnbakedCuboidGeometry`, while `FaceBakery` handles the UV half of
  rotation and the uvlock — so the mesher never has to think about it.
- **Tint is not resolved during baking.** The quad carries only a tint
  *index*; the colour comes from `BlockColors` at mesh time or from an
  `ItemTintSource` at item-render time.
- **Block models may only use the block atlas; item models may use one
  atlas, and mixing throws.** A baked block model found referencing a
  sprite from another atlas is rejected and replaced with the missing
  part — softly. A cuboid item model must draw every quad from a single
  atlas, items or blocks, and a model that mixes them throws; the
  exception is caught upstream and the item falls back to the missing
  model.
- **A model knows whether it needs sorting or re-uploading without being
  read.** `QuadCollection` carries translucent and animated flags,
  OR-ed up through every model wrapper, which is how the mesher and
  `ItemStackRenderState` decide cheaply.
- **Model groups let invisible state changes skip a rebuild.** Two states
  that look identical share a group id, and `ModelManager.requiresRender`
  returns false for a change between them — unless the fluid state
  differs.
- **You can dump the atlas.** A debug keybind writes every atlas to disk,
  and with a shared-constant flag set, a text listing of every sprite's
  position and size alongside it.
- **Names a 1.21-era reader will hunt for and not find:** *BakedModel*
  (split into `BlockStateModel` and `ItemModel`),
  *ModelResourceLocation* (block models are keyed by `BlockState`
  directly), *BlockModelShaper* (now `BlockStateModelSet`),
  *ItemModelShaper*, *WeightedBakedModel* (now `WeightedVariants`),
  *BlockElement* and *BlockElementFace* (now `CuboidModelElement` and
  `CuboidFace`), *BlockModelDefinition* (now
  `BlockStateModelDispatcher`), *AtlasSet* (now `AtlasManager`),
  *BlockRenderDispatcher*, *ItemRenderer*, *ItemColors*, and
  *SpriteTicker*. `TextureAtlas.LOCATION_BLOCKS` and its siblings are
  deprecated but far from dead — they are still the *texture* ids the
  atlas-membership checks compare against, while `AtlasIds` names the
  *definition* files.

## Where to look

`ModelManager.reload` for the shape of the pipeline, then
`AtlasManager.prepareSharedState` for the handshake that makes it
parallel. `ModelDiscovery` for resolution, `ModelBakery.bakeModels` for
baking, `SpriteLoader.loadAndStitch` and `Stitcher` for the atlas.
`FaceBakery.bakeQuad` for where a face's layer is decided, and
`BlockStateModelSet.get` for how a block finally finds its quads.

---

*Rules: names, never code · how the system works, not how the code reads ·
newest version only · every backticked name passes `tools/verify_names.py`.*
