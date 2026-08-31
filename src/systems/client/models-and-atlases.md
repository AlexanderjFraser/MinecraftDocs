# Models and atlases

> Verified against **Minecraft 26.2** · Part X · a resource pack changes one texture, and every stone block in the world redraws.

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
  `ModelManager.getItemModel` and `ModelManager.requiresRender`.
- **`ModelBakery`** — `ModelBakery.bakeModels` produces a
  `ModelBakery.BakingResult`
  (`ModelBakery.BakingResult.blockStateModels`,
  `.itemStackModels`, `.itemProperties`, `.missingModels`). It also owns
  the block-breaking overlay constants `ModelBakery.DESTROY_STAGES`,
  `ModelBakery.DESTROY_TYPES` and `ModelBakery.DESTROY_STAGE_COUNT`.
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
`CuboidFace` and `CuboidRotation` — and its baked output is a
`QuadCollection` of `BakedQuad`, now a record carrying four positions,
four packed UVs and a `BakedQuad.MaterialInfo` (sprite,
`ChunkSectionLayer`, tint index, shade, light emission).
`FaceBakery.bakeQuad` is where a face becomes a quad.

### The atlas

- **`AtlasManager`** — a reload listener *and* a `SpriteGetter`. It owns
  `AtlasManager.KNOWN_ATLASES` (thirteen of them, named in `AtlasIds`)
  and publishes `AtlasManager.PENDING_STITCH` — the shared-state key that
  lets `ModelManager` consume the stitch results without depending on
  listener order.
- **`SpriteLoader`** — `SpriteLoader.loadAndStitch` and
  `SpriteLoader.stitch`, producing a `SpriteLoader.Preparations`.
- **`Stitcher`** — the packer. `Stitcher.registerSprite`,
  `Stitcher.stitch`, `Stitcher.HOLDER_COMPARATOR`, and
  `StitcherException` when it cannot fit.
- **`TextureAtlas`** and **`TextureAtlasSprite`** — the GPU side, with
  `SpriteContents` holding the mip chain and
  `SpriteContents.AnimationState` driving animated frames.
  `TextureAtlas.upload`, `TextureAtlas.uploadInitialContents`,
  `TextureAtlas.cycleAnimationFrames`.
- **The atlas definition files** — `SpriteSourceList`, `SpriteSources`,
  and the source types `SingleFile`, `DirectoryLister`, `SourceFilter`,
  `Unstitcher`, `PalettedPermutations`.
- **`Material`, `SpriteId`, `MaterialBaker`, `TextureSlots`** — the
  indirection from a model's `#slot` reference to a real sprite.

### The consumers

`BlockStateModelSet.get` is what the mesher calls;
`BlockStateModel.collectParts` yields `BlockStateModelPart`s and
`BlockStateModelPart.getQuads` yields the quads.
`SingleVariant`, `WeightedVariants` and `MultiPartModel` are the three
shapes a blockstate file can take, with `Variant` and `VariantMutator`
carrying the rotation and UV-lock. Items go through `ItemModelResolver`
and `ItemModel` into an `ItemStackRenderState`; the model is chosen by
the stack's `DataComponents.ITEM_MODEL`. Special-cased renderers (chests,
shields, heads, banners) come from `SpecialModelRenderers`.

## When it runs

Only at a resource reload — see
[the resource system](../foundations/resource-system.md) for
`ReloadableResourceManager`, `PreparableReloadListener` and the barrier
semantics this rides on. What is new here is the shared-state handshake:
`PreparableReloadListener.prepareSharedState` runs for *every* listener
on the client thread before *any* reload task starts, and `AtlasManager`
uses it to publish thirteen pending stitch futures.

The work, by stage:

1. **Workers, in parallel** — thirteen atlas stitches (one task per
   sprite for decode and metadata, then a single-threaded stitch per
   atlas, then mip generation), plus the *models/*, *blockstates/* and
   *items/* listings, one task per file.
2. **One worker task** — `ModelDiscovery` walks parent chains and
   interns everything; in parallel, `ModelGroupCollector` builds the
   visual-equality groups.
3. **Workers, massively parallel** — `ModelBakery.bakeModels`: one bake
   per *block state* and one per item model file, sharing one baker whose
   caches are concurrent maps.
4. **The barrier**, then the client thread: the atlas uploads
   (`TextureAtlas.upload`), then `ModelManager.apply` assigns the new
   lookup sets.
5. **After the whole reload succeeds** — `LevelExtractor.allChanged`
   builds a new `SectionCompiler` from the new model sets and every
   section is re-meshed. See [level rendering](level-rendering.md).

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
    MM->>MB: bakeModels — one bake per BlockState, in parallel
    MB->>SL: MaterialBaker resolves each #slot to the NEW sprite
    MB->>MB: FaceBakery writes the new UVs into each BakedQuad
    Note over AM,MM: the barrier
    AM->>TA: upload — new GpuTexture, old sprites closed
    MM->>MM: apply — the new BlockStateModelSet goes live
    M->>LX: allChanged — new SectionCompiler, every section re-meshed
```

The point the trace makes: **changing one texture rebuilds the entire
model layer.** Nothing is incremental. The models for stone were
byte-identical before and after, but they are re-parsed, re-resolved and
re-baked anyway, because the sprite they point at is a different object
with different UVs.

## Interfaces

- **Called by:** `SectionCompiler` for terrain,
  `BlockEntityRenderDispatcher` and `ItemModelResolver` for everything
  else, `ParticleEngine` for the break-particle sprite.
- **Calls into:** the resource manager for files, and
  [blaze3d](blaze3d.md) for the atlas texture and the sprite blit.
- **Crosses the network as:** nothing. This is entirely client-side; the
  server has no idea what a model is.
- **Data-driven by:** *models/*, *blockstates/*, *items/*, *atlases/* and
  *textures/* in every enabled resource pack, plus
  `DataComponents.ITEM_MODEL` on the stack.

## Invariants and surprises

- **Baking is per block state, and dedup is what makes it affordable.**
  Tens of thousands of bakes are scheduled, but every state sharing an
  unbaked variant gets the *same* baked model object, geometry is cached
  per `ModelState`, and vertex positions and material infos are interned.
  A quad on a shared face is often literally one object across thousands
  of states.
- **A cyclic model is dropped, not fatal.** A model whose parent chain
  never reaches a root is logged and excluded. Unreferenced models are
  parsed and never baked.
- **Missing things fail soft at four separate layers** — a failed
  texture becomes the missing sprite, an unbound `#slot` is reported, a
  missing model file becomes the missing model, and a block state with no
  entry at all is filled in with a warning. `Minecraft.selfTest` sweeps
  for the last case at startup.
- **A pack with too many textures crashes the game.** If the stitcher
  cannot grow the atlas within the device's maximum texture size it
  throws, and that becomes a crash report listing every sprite. There is
  no graceful degradation.
- **One small texture degrades mipmapping for the whole atlas.** The mip
  level is clamped to the smallest sprite's power of two, with a warning.
  And only the block atlas requests mipmaps at all; the other twelve
  stitch flat.
- **Anisotropic filtering changes the atlas layout.** Sprite padding is
  derived from the mip level *and* the anisotropy setting, and the UVs
  are computed inside that padded box.
- **Sprites are uploaded by drawing, not by a texture write.** Each
  sprite goes into a scratch texture and is blitted into the atlas with a
  render pass per mip level, driven by a per-sprite uniform. Animated
  frames use the same path every tick.
- **Blocks have two model layers with different jobs.**
  `BlockStateModel` is the quad source for the mesher and for particles;
  `BlockModel` — a different interface in a different package — is the
  *display* model for item frames, block entities and moving blocks, and
  carries tint sources and a transform.
- **Cull faces are rotated at bake time.** A rotated variant's
  `cullface: north` quad is filed under the rotated direction, so the
  mesher never has to think about it.
- **Tint is not resolved during baking.** The quad carries only a tint
  *index*; the colour comes from `BlockColors` at mesh time or from an
  `ItemTintSource` at item-render time.
- **Block models may only use the block atlas.** A baked block model
  found referencing a sprite from another atlas is rejected and replaced
  with the missing part. Item models are allowed either.
- **Model groups let invisible state changes skip a rebuild.** Two states
  that look identical share a group id, and `ModelManager.requiresRender`
  returns false for a change between them — unless the fluid state
  differs.
- **Names a 1.21-era reader will hunt for and not find:** *BakedModel*
  (split into `BlockStateModel` and `ItemModel`),
  *ModelResourceLocation* (block models are keyed by `BlockState`
  directly), *BlockModelShaper* (now `BlockStateModelSet`),
  *ItemModelShaper*, *WeightedBakedModel* (now `WeightedVariants`),
  *BlockElement* and *BlockElementFace* (now `CuboidModelElement` and
  `CuboidFace`), *BlockModelDefinition* (now
  `BlockStateModelDispatcher`), *AtlasSet* (now `AtlasManager`),
  *BlockRenderDispatcher*, *ItemRenderer*, *ItemColors*, and
  *SpriteTicker*. The old `TextureAtlas.LOCATION_BLOCKS` constants still
  exist but are deprecated in favour of `AtlasIds`.

## Where to look

`ModelManager.reload` for the shape of the pipeline, then
`AtlasManager.prepareSharedState` for the handshake that makes it
parallel. `ModelDiscovery` for resolution, `ModelBakery.bakeModels` for
baking, `SpriteLoader.stitch` and `Stitcher` for the atlas.
`BlockStateModelSet.get` for how a block finally finds its quads.

---

*Rules: names, never code · how the system works, not how the code reads ·
newest version only · every backticked name passes `tools/verify_names.py`.*
