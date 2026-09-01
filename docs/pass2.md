# Pass 2 — running notes for the owner's read

Consolidated from the session log in [plan.md](plan.md), one place per
concern, so the pass-2 sessions and the closing session (16) do not have
to re-read every log entry. Pass 1 sessions **append here** whenever they
leave something for later; pass 2 ticks items off.

## How pass 2 works (recap)

The owner reads part by part with the decompile open and leaves questions
**in the page** as `<!-- Q: … -->` comments. A pass-2 session answers each
in the prose — if the owner had to ask, the page was wrong or missing it —
removes the comment, and re-runs `tools/verify_names.py`. Pass 2 also
writes `src/lectures.md` (the lecture order) once every part has been
read.

## Split candidates (pages over the ~250-line guideline that carry two ideas)

| page | lines | what would split off |
|---|---:|---|
| `server/server-lifecycle` | ~310 | startup and `/stop` vs the side threads (RCON, query, management server) |
| `world/game-events-and-poi` | 375 | two traces: sculk/vibrations vs villager POI — the obvious split |
| `blocks/redstone` | ~380 | the experimental-evaluator coda (`ExperimentalRedstoneWireEvaluator`, `Orientation`) vs the default trace |
| `blocks/blocks-and-states` | ~340 | the state table (data page) vs the placement trace + prediction |
| `entities/entity-anatomy` | 367 | the base class + `EntityType` vs the hierarchy tour |
| `entities/ai-goals-and-brains` | 357 | goals vs brains vs pathfinding — three lectures in one page |
| `items/items-and-stacks` | 340 | the stack data model vs the use pipeline + the eating trace |
| `items/containers-and-menus` | 320 | the menu/slot model vs the click protocol (state id, `HashedStack`) |
| `player/player-anatomy` | 404 | the class ladder + `Inventory`/`Abilities` (a data page) vs the two-phase tick trace |
| `player/input-to-movement` | 305 | the client input chain vs the server's validation and rubber-band |
| `client/client-world-and-options` | ~300 | **strongest new candidate.** Four subjects: the tick/frame split and the client's own lighting; the prediction ledger (`MultiPlayerGameMode` + `BlockStatePredictionHandler`); options and `ClientInformation`; and input (`KeyMapping`, `MouseHandler`, `KeyboardHandler`). A sibling *input-and-keybinds* page would pair with Part VIII's *input to movement* — the seam is `ClientInput.tick`. The prediction ledger could also be its own page with its own trace; it is currently split across three pages (Part IX names `BlockStatePredictionHandler`, Part V's *block-breaking* has the prediction, this page has the ledger). Decide one owner. (session 10) |
| `client/gui-and-screens` | ~300 | the two-phase render model + widgets/layouts vs the font and text engine (`Font`, `FontSet`, `GlyphStitcher`, `StringSplitter`, bidi) — the text half is a lecture on its own (session 10) |
| `client/level-rendering` | ~310 | the meshing pipeline (dirty → compile → upload) vs visibility and the frame graph (session 10) |
| `worldgen/structures` | 307 | the placement decision (sets, `StructurePlacement`, `StructureCheck`, `/locate`) vs jigsaw assembly and template placement — two lectures, and the only page in Part XI with two distinct mechanisms (session 11) |
| `worldgen/density-functions` | 307 | the node library and the codec/registry model vs the two rewrites (`RandomState`, `NoiseChunk.wrapNew`) and the cell loop. The rewrite story is the lecture; the catalogue is reference (session 11) |
| `commands/brigadier-and-commands` | 313 | the parse/suggest/permission story vs the permission model itself. The permission rewrite (`PermissionSet`, `Permission`, `PermissionCheck`, `LevelBasedPermissionSet`) is a lecture on its own and is currently a section inside a page whose trace is `/give`; it is also the single biggest API break in the corpus and deserves the billing (session 12) |
| `commands/execution-and-functions` | 310 | the non-recursive engine (queue, `Frame`, forks, `/return`) vs the function model (compile, macros, tags). Two lectures; the seam is clean and the second half is the one data-pack authors want (session 12) |
| `appendix/naming-drift` | 422 | not a split candidate — a reference table. Flagged only so nobody counts it as an over-long page (session 12) |

Parts III–V all came out at 260–380 lines. The lecture-order decision in
pass 2 is where "one page, two lectures" gets settled; splitting the
markdown is optional.

## Closing session (16) to-dos

- `anatomy` threads table: add *Management server IO*, *RCON Listener /
  Client*, *Query Listener* (found in session 3); confirm against
  `reference/threads.md`.
- Appendix tour needs a paragraph on JSON-RPC (`server/jsonrpc`,
  `ManagementServer`) and on *pause-when-empty-seconds* (session 3).
- Re-read `anatomy` and `sound` against the finished corpus.
- Diagram consistency: lane names are class names everywhere; check that
  the same class is abbreviated the same way across parts
  (`ServerGamePacketListenerImpl` is *SG* in Part V, *SGPL* in Parts VII
  and IX, *CL* in Part VIII, *G* in Part III; `ClientPacketListener` is
  *CPL*, *CP* and *CL*. Session 9 used *SGPL* / *CPL*; pick one.)
- Glossary + the naming-drift appendix (list below).
- Part X diagram lanes use `LX` (`LevelExtractor`), `LR`, `GR`
  (`GameRenderer`), `SRD`, `ERD`, `FRD`, `PE`, `H`/`G` — fold into the
  lane-abbreviation decision above (session 10).
- `sound` was written before the extract/render split was documented;
  re-read it against `the-frame` and check whether the sound engine's
  threading paragraph still matches (session 10).
- `anatomy` predates Part X. Check its claim about the render thread:
  in 26.2 the thread named *Render thread* **is** the main thread, and
  the client has no second render thread (session 10).
- The naming-drift appendix will be dominated by Part X. It is by far
  the biggest source of gone names in the corpus (session 10).

- **Session 12 additions.** The appendix now exists, so the closing pass
  has three concrete jobs on it rather than a wish:
  - `appendix/naming-drift` is generated from the table below plus a
    hand-written Part XII block. If pass 2 finds a *wrong* row, fix it in
    both places or the next regeneration reintroduces it.
  - `appendix/out-of-scope-tour` ends with a **gaps** list — the debug
    cluster (~91 classes, and the *server-side* debug subscription system
    that pushes brains, paths and POIs to the client is genuinely
    undocumented), `client/resources`, `util/parsing`, `client/animation`,
    Blaze3D's Vulkan and platform halves. Each needs a ruling: absorb into
    an existing page, add a page, or decline explicitly.
  - `appendix/glossary` has ~110 entries and deliberately stops there. It
    should be re-swept once the lecture order exists, because the lecture
    order decides which page "owns" a term when two could.
- The **lane-abbreviation** decision now also covers Part XII, which used
  full-ish abbreviations (`SGPL`, `CPL`, `EC`, `PA`) — consistent with
  session 9's choice, so `SGPL`/`CPL` is now the majority spelling.
- `anatomy`'s thread table should gain the **management server** (JSON-RPC,
  its own Netty bootstrap) alongside RCON and query — the appendix tour
  describes it and `anatomy` predates it.
- The corpus now claims specific counts in two places (`CLAUDE.md`'s
  7,055 classes / 719k lines, and the appendix's per-package table).
  Re-measure both on the next version bump; the appendix table is the one
  that will rot first.

## Naming drift for the appendix (1.21-era name → 26.2)

Collected so far; each entry was found by a fact-sheet agent looking for
the old name and not finding it.

| old | 26.2 | found in |
|---|---|---|
| `ResourceLocation` | `Identifier` | CLAUDE.md |
| `LightTexture` | `Lightmap` | CLAUDE.md |
| `Timer` | `DeltaTracker` | CLAUDE.md |
| `TagManager` | gone | session 2 |
| `Minecraft.reloadResources` | `Minecraft.reloadResourcePacks` | session 2 |
| `ItemStack.save` / `parse` | `ValueOutput` / `ItemStack.CODEC` | session 2 |
| `ChunkPos.asLong` | `ChunkPos.pack` / `unpack` (record) | session 2 |
| `DO_DAYLIGHT_CYCLE` | `GameRules.ADVANCE_TIME` | session 3 |
| `DO_MOB_SPAWNING` | `GameRules.SPAWN_MOBS` | session 3 |
| `DO_WEATHER_CYCLE` | `GameRules.ADVANCE_WEATHER` | session 3 |
| `GameRules` package | `world/level/gamerules` | session 3 |
| day time on `ServerLevel` | `ServerClockManager` (`world/clock`) | session 3 |
| per-level weather | server-global `WeatherData` | session 3 |
| `ChunkStorage` | gone — `ChunkMap extends SimpleRegionStorage` | session 4 |
| `DimensionDataStorage` | `SavedDataStorage` (two of them) | session 4 |
| `getLightBlock` | `BlockBehaviour.BlockStateBase.getLightDampening` | session 4 |
| `PalettedContainer.Strategy` | top-level `Strategy` + `Configuration` | session 4 |
| `ForcedChunksSavedData` | `TicketStorage` | session 4 |
| `TicketType<T>` | a registry record with flag bits | session 4 |
| `DimensionType` booleans | `EnvironmentAttributeMap` | session 4 |
| `ItemInteractionResult` | gone — `InteractionResult.TryEmptyHandInteraction` | session 5 |
| `DirectionProperty` | gone — `EnumProperty<Direction>` | session 5 |
| `Level.markAndNotifyBlock` | gone — inline in `Level.setBlock` | session 5 |
| `BlockBehaviour.onRemove` | `affectNeighborsAfterRemoval` + `BlockEntity.preRemoveSideEffects` | session 5 |
| `doTileDrops` | `GameRules.BLOCK_DROPS` | session 5 |
| `BlockModelShaper` | `BlockStateModelSet` / `BlockModelSet` | session 5 |
| `RenderShape.ENTITYBLOCK_ANIMATED` | gone — `INVISIBLE` / `MODEL` only | session 5 |
| `Player.canInteractWithBlock` | `Player.isWithinBlockInteractionRange` | session 5 |
| `Block.rebuildCache` | gone — `BlockStateBase.initCache` from the `Blocks` static init | session 5 |
| `Material` | gone — individual `Properties` flags | session 5 |
| `BlockEntity.saveToItem` | `BlockItem.setBlockEntityData` + `BlockEntity.collectComponents` | session 5 |
| `MobEffects.DIG_SPEED` / `DIG_SLOWDOWN` | `HASTE` / `MINING_FATIGUE` | session 5 |
| `Player extends LivingEntity` | `Player extends Avatar extends LivingEntity` | session 6 |
| `EntityType.PIG` (constants) | `EntityTypes.PIG` + `EntityTypeIds.PIG` | session 6 |
| `MobSpawnType` | `EntitySpawnReason` (+ `EntitySpawnRequest`) | session 6 |
| `SpawnPlacements.Type` | `SpawnPlacementType` / `SpawnPlacementTypes` | session 6 |
| `Entity.hurt(DamageSource, float)` | `Entity.hurtServer` / `Entity.hurtClient` | session 6 |
| `doMobLoot` | `GameRules.MOB_DROPS` | session 6 |
| `LivingEntity.isDamageSourceBlocked` | gone — `DataComponents.BLOCKS_ATTACKS` | session 6 |
| `Schedule` / `ScheduleBuilder` | gone — `Timeline` + `EnvironmentAttribute` | session 6 |
| `BlockPathTypes` | `PathType` | session 6 |
| `Mob.brainProvider` | `LivingEntity.makeBrain(Brain.Packed)` | session 6 |
| `Entity.moveTo` / `absMoveTo` | `Entity.snapTo` / `Entity.absSnapTo` | session 6 |
| `Entity.maxUpStep` (field) | `Attributes.STEP_HEIGHT` | session 6 |
| `Entity.updateFluidHeightAndDoFluidPushing` | `EntityFluidInteraction` | session 6 |
| `Entity.lerpTo` | `Entity.moveOrInterpolateTo` + `InterpolationHandler` | session 6 |
| `EntityDataSerializers.OPTIONAL_UUID` / `COMPOUND_TAG` | gone | session 6 |
| UUID-keyed `AttributeModifier` | `Identifier`-keyed record | session 6 |
| `AttributeMap.getDirtyAttributes` | `getAttributesToSync` + `getAttributesToUpdate` | session 6 |
| `PlayerRenderer` | `AvatarRenderer` | session 6 |
| `InteractionResultHolder` | gone — `InteractionResult.Success.heldItemTransformedTo` | session 7 |
| `UseAnim` | `ItemUseAnimation` | session 7 |
| `Item.getFoodProperties` | `DataComponents.FOOD` on the stack | session 7 |
| `ItemStack.getTag` / `getOrCreateTag` | gone — components | session 7 |
| `LivingEntity.triggerItemUseEffects` | `Consumable.emitParticlesAndSounds` | session 7 |
| `FoodProperties` effects list | `Consumable.onConsumeEffects` | session 7 |
| `ClickType` | `ContainerInput` | session 7 |
| `MultiPlayerGameMode.handleInventoryMouseClick` | `handleContainerInput` | session 7 |
| `ClientboundSetCarriedItemPacket` | split: `ClientboundSetCursorItemPacket` + `ClientboundSetHeldSlotPacket` | session 7 |
| `ClientboundSetSlotPacket` | `ClientboundContainerSetSlotPacket` | session 7 |
| `ClientboundHorseScreenOpenPacket` | `ClientboundMountScreenOpenPacket` | session 7 |
| `Container.startOpen(Player)` | `Container.startOpen(ContainerUser)` | session 7 |
| `Recipe.getResultItem` / `getIngredients` | gone — `Recipe.assemble` / `PlacementInfo` | session 7 |
| `Ingredient.EMPTY` | gone — an `Ingredient` cannot be empty | session 7 |
| `data/<ns>/recipes/` | `data/<ns>/recipe/` (singular) | session 7 |
| `EnchantmentCategory` | `Enchantment.EnchantmentDefinition` item sets | session 7 |
| `Enchantment.getDamageBonus`, `EnchantmentHelper.getFireAspect`… | gone — `EnchantmentEffectComponents` | session 7 |
| `EnchantedBookItem` | gone — `DataComponents.STORED_ENCHANTMENTS` | session 7 |
| `Item.getEnchantmentValue` | `DataComponents.ENCHANTABLE` | session 7 |
| `LootContextParam` / `LootContextParamSet` | `ContextKey` / `ContextKeySet` (`util/context`) | session 7 |
| `LootDataManager` / `LootTables` | `ReloadableServerRegistries` + `BuiltInLootTables` | session 7 |
| `LootTableReference` | `NestedLootTable` | session 7 |
| `LootingEnchantFunction` | `EnchantedCountIncreaseFunction` | session 7 |
| `SetCountFunction` | `SetItemCountFunction` | session 7 |
| `LootContextParams.KILLER_ENTITY` | `LootContextParams.ATTACKING_ENTITY` | session 7 |
| `PlayerRenderer` | `AvatarRenderer` (generic over `Avatar` + `ClientAvatarEntity`) | session 8 |
| `Inventory.armor` / `offhand` / `compartments` | one 36-slot `Inventory.items` + `Inventory.EQUIPMENT_SLOT_MAPPING` | session 8 |
| `Inventory.setPickedItem` | `Inventory.addAndPickItem` / `Inventory.pickSlot` | session 8 |
| `Entity.moveTo` | `Entity.absSnapTo` / `Entity.snapTo` | session 8 |
| `GameRenderer.pick` | `Minecraft.pick` → `LocalPlayer.raycastHitResult` | session 8 |
| `ServerboundInteractPacket.Action.ATTACK` | `ServerboundAttackPacket` (a record of one int) | session 8 |
| `GameRules.NATURAL_REGENERATION` | `GameRules.NATURAL_HEALTH_REGENERATION` | session 8 |
| `Player.isCritArrow` / `Player.sweepAttack` | `Player.canCriticalAttack` / `Player.isSweepAttack` + `Player.doSweepAttack` | session 8 |
| `LivingEntity.eat` / `Player.eat` | gone — `Consumable.onConsume` → `FoodProperties` → `FoodData.eat` | session 8 |
| `MobEffect.createModifier` | `MobEffect.createModifiers` (plural) | session 8 |
| `DataComponents.MENDING` | `EnchantmentEffectComponents.REPAIR_WITH_XP` | session 8 |
| `Connection.setListener` / `setProtocol` / `getCurrentProtocol` | gone — `Connection.setupInboundProtocol` / `setupOutboundProtocol` | session 9 |
| `ConnectionProtocol.getById` / packet tables | gone — a bare enum; ids are `addPacket` order in `IdDispatchCodec` | session 9 |
| `Connection.NETWORK_WORKER_GROUP` etc. | `EventLoopGroupHolder` (in `server/network`) | session 9 |
| `MemoryConnection` | gone — `Connection.isMemoryConnection` | session 9 |
| `ensureRunningOnSameThread(…, BlockableEventLoop)` | `PacketUtils.ensureRunningOnSameThread` with a `PacketProcessor` | session 9 |
| `Packet.write(FriendlyByteBuf)` | gone — a `STREAM_CODEC` field the protocol reads | session 9 |
| `ClientboundAddPlayerPacket` / `ClientboundAddMobPacket` | gone — `ClientboundAddEntityPacket` | session 9 |
| `ClientboundUpdateViewPositionPacket` | `ClientboundSetChunkCacheCenterPacket` | session 9 |
| `ClientboundUpdateViewDistancePacket` | `ClientboundSetChunkCacheRadiusPacket` | session 9 |
| `ClientboundLevelChunkPacket` | `ClientboundLevelChunkWithLightPacket` | session 9 |
| routine `ClientboundTeleportEntityPacket` | `ClientboundEntityPositionSyncPacket` | session 9 |
| `ClientboundGameProfilePacket` | `ClientboundLoginFinishedPacket` (+ a session id) | session 9 |
| `ServerboundLoginStartPacket` | `ServerboundHelloPacket` | session 9 |
| `ClientboundEncryptionRequestPacket` / response | `ClientboundHelloPacket` / `ServerboundKeyPacket` | session 9 |
| `ClientboundSetCompressionPacket` | `ClientboundLoginCompressionPacket` | session 9 |
| `ClientboundResourcePackPacket` | `ClientboundResourcePackPushPacket` / `…PopPacket` | session 9 |
| `MinecraftServer.getSessionService` | `MinecraftServer.services` | session 9 |
| `PlayerChunkSender` in `server/level` | `server/network` | session 9 |
| `Component.Serializer` (Gson) | `ComponentSerialization` (codecs; NBT on the wire) | session 9 |
| `TextComponent` / `TranslatableComponent` / … | `network/chat/contents` — `PlainTextContents` etc. | session 9 |
| `ComponentUtils.updateForEntity` | `ComponentUtils.resolve` with a `ResolutionContext` | session 9 |
| `SignedMessageHeader` / `MessageSigner` | `SignedMessageLink` / `SignedMessageChain.Encoder` | session 9 |
| `ChatPreview` and its packets | gone | session 9 |
| `ClientboundSetTimePacket(gameTime, dayTime, …)` | a game time plus a `WorldClock` update map | session 9 |
| `Gui` (the HUD) | `Hud`, held as `Gui.hud`; the name `Gui` now means the screen/overlay manager | session 10 |
| `Minecraft.screen` / `Minecraft.setScreen` | `Gui.screen` / `Gui.setScreen` | session 10 |
| `GuiGraphics` | `GuiGraphicsExtractor` (records states; does not draw) | session 10 |
| `Screen.render` / every `render*` on `Gui` | `Screen.extractRenderState` / `Hud.extract*` | session 10 |
| `LayeredDraw` | call order plus `GuiRenderState.nextStratum` | session 10 |
| `Options.hideGui` | `Hud.isHidden`, published as `GuiRenderState.isHudHidden` | session 10 |
| `MultiBufferSource` / `BufferSource` | `SubmitNodeCollector` / `SubmitNodeStorage` / `FeatureRenderDispatcher` | session 10 |
| `ShaderInstance`, `RenderStateShard` | `RenderPipeline` + `RenderPipelines` + `BindGroupLayouts` | session 10 |
| `VertexBuffer`, `Tesselator`, `BufferUploader` | `GpuBuffer` / `GpuBufferSlice`, `ByteBufferBuilder` → `MeshData`, `UberGpuBuffer` | session 10 |
| `RenderSystem.setShader` / `enableBlend` / `depthMask` … | fields of a `RenderPipeline` | session 10 |
| `VertexFormat.Mode`, `VertexFormat.IndexType`, `TextureFormat` | `PrimitiveTopology`, `IndexType`, `GpuFormat` | session 10 |
| `Window.updateDisplay`, vsync as a swap interval | `GpuSurface.present`, vsync as a `GpuSurface.PresentMode` | session 10 |
| `LightTexture.pack` and friends | `LightCoordsUtil` | session 10 |
| `DimensionSpecialEffects` | `DimensionType.skybox` + `EnvironmentAttributes` + `Timeline` | session 10 |
| `FogParameters`, `RenderSystem.setShaderFogColor` | `FogData`, `RenderSystem.setShaderFog` (a uniform slice) | session 10 |
| `Level.getSkyColor`, `ClientLevel.getStarBrightness`, `ClientLevel.effects` | `EnvironmentAttributeProbe.getValue` on an `EnvironmentAttribute` | session 10 |
| `LevelRenderer.renderLevel` / `renderSky` / `renderChunkLayer` | `LevelRenderer.render` and the `addSkyPass` family of frame-graph passes | session 10 |
| `LevelRenderer.blockChanged` / `setSectionDirty` / `allChanged` | the same names on `LevelExtractor` | session 10 |
| `ChunkRenderDispatcher`, `RenderChunk`, `CompiledChunk` | `SectionRenderDispatcher`, its `RenderSection`, `CompiledSectionMesh` | session 10 |
| `RenderType.chunkBufferLayers` (five layers) | `ChunkSectionLayer` — three layers | session 10 |
| `BakedModel`, `ModelResourceLocation` | `BlockStateModel` / `ItemModel`; block models keyed by `BlockState` | session 10 |
| `BlockModelShaper`, `ItemModelShaper`, `BlockRenderDispatcher`, `ItemRenderer` | `BlockStateModelSet`, `ItemModelResolver`, `ModelBlockRenderer` | session 10 |
| `BlockElement` / `BlockElementFace`, `AtlasSet`, `ItemColors` | `CuboidModelElement` / `CuboidFace`, `AtlasManager`, `ItemTintSource` | session 10 |
| `PlayerRenderer` | `AvatarRenderer` (serves players and mannequins, keyed by skin model) | session 10 |
| `EntityRenderer.render`, `RenderLayer.render` | `extractRenderState` + `submit` | session 10 |
| `TextureSheetParticle`, sheet `ParticleRenderType`s | `SingleQuadParticle` + `SingleQuadParticle.Layer` | session 10 |
| `ParticleGroup` (a limit record) | `ParticleLimit`; `ParticleGroup` is now the per-render-type bucket | session 10 |
| `Minecraft.getPartialTick`, `Timer`, `Camera.setup` | `DeltaTracker.Timer`, `Camera.update` + `Camera.extractRenderState` | session 10 |
| `ClickType` | `ContainerInput` | session 10 |

| `GenerationStep.Carving` | gone — `BiomeGenerationSettings.carvers` is one flat `HolderSet` | session 11 |
| `DensityFunctions.WeirdScaledSampler` | `DensityFunctions.IntervalSelect` | session 11 |
| `StructureFeature` / `ConfiguredStructureFeature` | `Structure` / `Registries.STRUCTURE` | session 11 |
| `Feature.RANDOM_PATCH`, `Feature.FLOWER` | gone — composed from `Feature.SIMPLE_BLOCK` + placement | session 11 |
| `Feature.POINTED_DRIPSTONE` / `DRIPSTONE_CLUSTER` | `Feature.SPELEOTHEM` / `SPELEOTHEM_CLUSTER` | session 11 |
| `AbstractTreeGrower` and its subclasses | one final `TreeGrower` with constants | session 11 |
| `TreeConfiguration.dirtProvider` | `TreeConfiguration.belowTrunkProvider` | session 11 |
| `Biome.BiomeCategory` / `Biome.getDownfall` | gone | session 11 |
| `MultiNoiseBiomeSource.Preset` | `MultiNoiseBiomeSourceParameterList.Preset` | session 11 |
| `BiomeSpecialEffects.fogColor` / `skyColor` / music / ambient sound | `EnvironmentAttributes.*` via `Biome.getAttributes` | session 11 |
| the +8 chunk population offset | gone — decoration starts at the chunk corner, `InSquarePlacement` scatters | session 11 |
| `StructureTemplateManager` folder *structures/* | *structure/* | session 11 |

| `ResourceLocationArgument` | `IdentifierArgument` (registry id unchanged) | session 12 |
| `CommandSourceStack.hasPermission(int)` | `CommandSourceStack.permissions` + `PermissionSet.hasPermission` | session 12 |
| `CommandSourceStack.getPermissionLevel` | gone — `PermissionLevel` lives inside `LevelBasedPermissionSet` | session 12 |
| `SharedSuggestionProvider.hasPermission(int)` | gone — it extends `PermissionSetSupplier` | session 12 |
| `Commands.hasPermission(int)` | `Commands.hasPermission` taking a `PermissionCheck` | session 12 |
| `ServerPlayer.hasPermissions(int)` | `ServerPlayer.permissions` | session 12 |
| `MinecraftServer.getFunctionCompilationLevel` | `MinecraftServer.getFunctionCompilationPermissions` | session 12 |
| `ServerOpListEntry.getLevel` | `ServerOpListEntry.permissions` | session 12 |
| `ParserUtils.parseJson` | gone — `SnbtGrammar` + `ParserBasedArgument` | session 12 |
| `ServerFunctionManager.ExecutionContext` (nested) | top-level `ExecutionContext` (`commands/execution`) | session 12 |
| `CommandFunction.Entry` / `CommandEntry` / `FunctionEntry` | gone — `BuildContexts.Unbound` / `MacroFunction.MacroEntry` | session 12 |
| `Commands.performCommand` returning a count | returns nothing; a `CommandResultCallback` pair | session 12 |
| `data/<ns>/functions/` (plural) | `data/<ns>/function/` (singular), likewise `tags/function/` | session 12 |
| maxCommandChainLength | `GameRules.MAX_COMMAND_SEQUENCE_LENGTH` | session 12 |
| maxCommandForkCount | `GameRules.MAX_COMMAND_FORKS` | session 12 |
| announceAdvancements | `GameRules.SHOW_ADVANCEMENT_MESSAGES` | session 12 |
| `net.minecraft.advancements.critereon` | `advancements/triggers` + `advancements/predicates` | session 12 |
| `AdvancementList` | `AdvancementTree` (+ `AdvancementNode`, `AdvancementHolder`) | session 12 |
| `FrameType` | `AdvancementType` | session 12 |
| `CriterionTrigger.addPlayerListener` | gone — triggers are stateless; state is in `PlayerAdvancements` | session 12 |
| `@GameTest` and the annotation framework | gone — `GameTestInstance` in `Registries.TEST_INSTANCE` | session 12 |
| `GameTestRegistry` / `TestFunction` | `Registries.TEST_FUNCTION` + `TestFunctionLoader`, and `TestData` | session 12 |

## Cross-part obligations (link, don't repeat)

What each unwritten part should point at instead of re-explaining. Tick
when the part is written.

- [x] **Part VI Entities** (session 6) — villager/POI half of `game-events-and-poi`;
  `PersistentEntitySectionManager.updateChunkStatus` / `Visibility`
  (session 4); `Block.popResource` → `ItemEntity` and `Entity.absSnapTo`
  from `block-breaking` / `blocks-and-states` (session 5).
- [x] **Part VII Items** (session 7) — menus (`ServerPlayer.openMenu`,
  `AbstractContainerMenu.broadcastChanges`, `ContainerSynchronizer`,
  `RemoteSlot.Synchronized` hashing) are half-explained in
  `block-entities`; `Tool` / `ToolMaterial` in `block-breaking`; item
  component prototypes bind at reload (`DataComponentInitializers`,
  session 2); serverbound container clicks carry `HashedStack` (session 2);
  `ItemAttributeModifiers` / `EquipmentSlotGroup` / the item-tooltip
  `ItemAttributeModifiers.Display` are named but not explained in
  `attributes`, and `DataComponents.BLOCKS_ATTACKS`,
  `DataComponents.DAMAGE_RESISTANT` and `DataComponents.DEATH_PROTECTION`
  in `damage-and-death` (session 6).
- [x] **Part VIII The player** (session 8) — `ServerPlayer` is created in the
  configuration phase (`PrepareSpawnTask`), owned by `players-and-sessions`;
  player ticking is split (`doTick` from the connection, `tick` from the
  level's entity loop) — do not contradict (session 3); the prediction
  ledger (`BlockStatePredictionHandler`) is in `block-interaction`;
  `Avatar`, i-frames, the armour/protection formulas and
  `ServerPlayer.die` (which never calls `super.die`) are in Part VI — link,
  do not repeat (session 6). `Player.attack`, `Player.itemAttackInteraction`
  and `ServerPlayer.getEnchantedDamage` (the base `Player.getEnchantedDamage`
  returns its argument unchanged) are named but not owned by
  `enchantments`; attacks arrive as `ServerboundAttackPacket`; `FoodData`
  and `FoodConstants` are half-explained in `items-and-stacks`; the
  enchanting seed `Player.enchantmentSeed` is re-rolled by *spending XP*
  (session 7).
- [x] **Part IX Networking** (session 9) — `protocol-phases` points back at
  `players-and-sessions` for the configuration phase (session 3);
  *what-the-client-is-told* points at `tickets-and-loading` for
  `PlayerChunkSender` batching, `lighting` for `ClientboundLightUpdatePacket`
  (session 4), and gains `ClientboundBlockChangedAckPacket`,
  `ClientboundBlockEventPacket`, `ClientboundBlockDestructionPacket` and
  the "clicked block always comes back" rule from `block-interaction`
  (session 5); and the entity channels from Part VI —
  `ClientboundSetEntityDataPacket`, `ClientboundUpdateAttributesPacket`,
  `ClientboundSetEquipmentPacket` (which bypasses `ServerEntity`),
  `ClientboundDamageEventPacket` (**no damage amount on the wire**),
  `ClientboundHurtAnimationPacket`, `ClientboundEntityPositionSyncPacket`
  and the `ServerEntity.sendPairingData` bundle (session 6). Adds the whole container
  packet set, `HashedStack` / `HashedPatchMap` (CRC32C over component
  values, cached per player) and the 15-bit state id from
  `containers-and-menus`; `ItemStack.OPTIONAL_UNTRUSTED_STREAM_CODEC` for
  inbound stacks; and the registry-sync asymmetry — `Registries.ENCHANTMENT`
  is synced with its **full** direct codec while the three loot registries
  are never synced at all (session 7). From session 8: `ServerboundAttackPacket` (a record of **one int** — no hand, no hit
  position; `ServerboundInteractPacket` is right-click only and has no
  `Action` enum), the four `ServerboundMovePlayerPacket` variants and
  their two-flag byte, `ServerboundPlayerInputPacket` with
  `Input.STREAM_CODEC` (seven booleans in one byte),
  `ServerboundClientTickEndPacket`, `ClientboundPlayerPositionPacket`
  (`PositionMoveRotation` + a `Relative` set) and the twenty-tick
  teleport re-send, `ClientboundPlayerAbilitiesPacket` (four bits, and
  `Abilities.mayBuild` never travels), `CommonPlayerSpawnInfo`,
  `ClientboundSetHealthPacket` (saturation is sent but only its
  zero-ness is change-detected) and `ClientboundSetExperiencePacket`.
- [x] **Part X The client** — *written in session 10.* Names picked up: `LevelExtractor`,
  `SectionUpdateTracker`, `SectionCopy` (session 4);
  `LevelExtractor.blockChanged`, `BlockBreakingRenderState`,
  `ModelBakery.DESTROY_TYPES`, `BlockStateModelSet`, `PistonHeadRenderer`,
  `BlockEntityRenderDispatcher` (session 5); the client lights per frame
  (`ClientLevel.update`, session 4); `EntityRenderDispatcher.extractEntity`,
  `SheepRenderState`, `AvatarRenderer` (there is no `PlayerRenderer`),
  `InterpolationHandler`, and `LivingEntityRenderer`'s red overlay from
  `LivingEntity.hurtTime` (session 6). From session 7:
  `AbstractContainerScreen`, `MenuScreens`,
  `ItemInHandRenderer.applyEatTransform`, `Hud.extractFood`,
  `RecipeBookComponent`, `GhostSlots`, `ClientRecipeBook`,
  `EnchantmentNames`. From session 8: `AvatarRenderer` (generic over an `Avatar`
  that is also a `ClientAvatarEntity` — there is no `PlayerRenderer`),
  `ClientAvatarState`, `KeyMapping.Category` (a record, publicly
  registerable), `ToggleKeyMapping`, `MouseHandler` (which turns the
  player per **frame**, not per tick), and the attack indicator in
  `Hud` with `AttackIndicatorStatus`. From session 9: `ClientChunkCache`
  and its nested `Storage` (a torus of slots indexed modulo the view
  range, read off-thread by the render path), `ChunkBatchSizeCalculator`
  (the chunk-rate control loop, measured on the Netty thread),
  `InterpolationHandler` again (three client ticks per update), the chat
  HUD — `ChatComponent`, `ChatListener`, `GuiMessage`, `GuiMessageTag`,
  `ChatTrustLevel`, `GuiMessageSource`, `ChatAbilities` /
  `ChatRestriction` — and the render side of `Component`
  (`FontDescription`, `ObjectContents` with `AtlasSprite` /
  `PlayerSprite`, `SubStringSource` for bidi). Note `ClientLevel.hasChunk`
  returns true unconditionally and `ClientLevel.explode` is empty; *what
  the client is told* owns those, Part X should link rather than repeat.
- [x] **Part XII Commands** — from session 9: `SignableCommand`,
  `SignedArgument` (the only implementation is `MessageArgument`),
  `ArgumentSignatures` (one signature per argument, each burning a chain
  index), `CommandSigningContext`, `CommandSourceStack.withSigningContext`
  and `DebugConfigCommand` (the only vanilla caller of
  `ServerGamePacketListenerImpl.switchToConfig` and
  `ServerConfigurationPacketListenerImpl.returnToWorld`). Chat *signing*
  is owned by *chat-and-signing*; Part XII owns the argument plumbing.
- [x] **Part XIII Appendix** — the out-of-scope tour gains
  `client/multiplayer/chat/report` (`ReportingContext`,
  `AbuseReportSender`, the report screens) and `LegacyQueryHandler` /
  `LegacyProtocolUtils` (the pre-1.7 ping still in the pipeline)
  (session 9).
- [x] **Part XI World generation** (session 11) — *worldgen-pipeline* points at
  `chunk-generation-pipeline` for the conveyor;
  `ChunkStatus.MAX_STRUCTURE_DISTANCE` is dead code (session 4). Also took
  from session 10: `Biome.getAttributes` carries the visual attributes and
  `BiomeSpecialEffects` keeps only water/foliage/grass colours — confirmed
  and stated in `biomes`.
- [x] **Part XII Commands** — `loot-tables` now owns the loot data model,
  so Part XII need only cover the commands: `/loot`, `/item … with`
  (`ItemCommands.applyModifier`) and `EnchantCommand`, plus
  `ResourceOrIdArgument` accepting an inline table (session 7).
- [x] **Part XIII Appendix** — the naming-drift table above; the JSON-RPC
  and pause-when-empty paragraphs.
- [x] **Part XII Commands** — from session 11: `/locate structure` and
  `/locate biome` are *very* different (the first can drive world
  generation on the server thread through `StructureCheck.checkStart`, the
  second asks the `BiomeSource` and never reads a stored palette);
  `/fillbiome` writes the biome palette and resends it with
  `ClientboundChunksBiomesPacket`; `/place` reaches
  `JigsawPlacement.generateJigsaw`. `structures` and `biomes` own the
  mechanisms — Part XII owns the command plumbing and should link.
- [x] **Part XIII Appendix** — from session 11: the out-of-scope tour
  should note `net/minecraft/data/worldgen` (`Structures`, `StructureSets`,
  `PlainVillagePools`, `ProcessorLists`, `TreeFeatures`,
  `VegetationPlacements`, `BiomeData`) — vanilla's entire worldgen data
  pack is Java that is data-generated to JSON, which is why "it is
  data-driven" and "you cannot change it" are both true of the overworld
  biome table.

## Facts that later sessions must not contradict

Short list of things established by a page and easy to get wrong from
1.21 memory. Each is stated once, in the page named.

- Day time is `ServerClockManager`, server-wide; `ServerLevel.tickTime`
  only bumps `gameTime` in the overworld — `server-level-tick`.
- Weather is server-global `WeatherData` — `server-tick`.
- `ChunkMap.forEachBlockTickingChunk` walks the entity-ticking set —
  `server-level-tick` / `tickets-and-loading`.
- Two level graphs (`LoadingChunkTracker`, `SimulationChunkTracker`): a
  holder can be `ENTITY_TICKING` by status and tick nothing —
  `tickets-and-loading`.
- No light thread; a `ConsecutiveExecutor` on the pool — `lighting`.
- `level.dat` is a stub; rules, border, weather, dragon fight are
  `SavedData` — `level-data-and-rules`.
- `IOWorker` is a lane on `Util.ioPool`, not a thread — `chunk-storage`.
- Shape updates run on both sides; neighbour updates only on the server;
  the client never runs `neighborChanged` — `block-interaction`.
- The client places and breaks blocks for real under prediction; the
  server's update for a predicted position is swallowed until the ack —
  `blocks-and-states`, `block-breaking`.
- `BlockEntity.setChanged` sends nothing; `getUpdatePacket` is called only
  from `ChunkHolder.broadcastBlockEntity` — `block-entities`.
- Block events are a set on `ServerLevel`, drained a tick later; the
  client simulates pistons from `ClientboundBlockEventPacket` — `redstone`.
- `Player extends Avatar extends LivingEntity`; `ArmorStand` is a
  `LivingEntity` with no AI — `entity-anatomy`.
- `LevelWriter.addFreshEntity` is a default returning false; only
  `ServerLevel` implements it — `entity-lifecycle`.
- There are two mob caps (global, scaled by covered chunk area; and
  per-player) and persistent mobs count for neither — `entity-lifecycle`.
- Synched-data ids are class-tree ordinals; defaults never travel; the
  client's writes are discarded — `synched-entity-data`.
- Eight attributes are not client-syncable, `Attributes.ATTACK_DAMAGE`
  among them, so the client's damage prediction is always stale —
  `attributes`.
- Damage is server-only (`Entity.hurtServer`); the amount never crosses
  the wire; i-frames compare against the last damage — `damage-and-death`.
- AI is strictly single-threaded and pathfinding never loads a chunk —
  `ai-goals-and-brains`.
- An item's default components are built at *reload*, not at
  construction; `Item.components` throws before then — `items-and-stacks`.
- A shift-click that agrees costs **zero** clientbound packets; the
  server adopts the client's hash as its new baseline — `containers-and-menus`.
- The client is never sent a recipe; a `RecipeDisplayId` is a list index
  that changes on every reload — `recipes`.
- No enchantment effect runs on the client, but the client still gets the
  full definitions for tooltips — `enchantments`.
- Loot tables are never synced; a chest's table key is cleared *before*
  the roll, and any container read (a hopper, `/data`) commits it with no
  player luck — `loot-tables`.

- The server **simulates a human player fully every tick and then throws
  the position away** (`ServerGamePacketListenerImpl.tickPlayer` →
  `ServerPlayer.doTick` → snap back to `firstGood…`); the authoritative
  position only moves in `handleMovePlayer` or a teleport, and the
  simulation exists to produce `Entity.getDeltaMovement` for the
  anti-cheat — `input-to-movement`.
- `ServerboundPlayerInputPacket` **never moves anyone**; its only
  consumers are `ServerPlayer.getLastClientMoveIntent` and an
  `InputPredicate` — `input-to-movement`.
- `Inventory` is 43 slots (36 + equipment view), and `EquipmentSlot.MAINHAND`
  is an alias for the selected hotbar slot via `PlayerEquipment` —
  `player-anatomy`.
- `Player.isCreative` / `isSpectator` read `Player.gameMode`, not
  `Abilities`; on the client the mode comes from the tab-list `PlayerInfo`
  and can be null — `player-anatomy`.
- Attack and interact are **different packets**;
  `ServerboundAttackPacket` carries only an entity id, and a
  `PiercingWeapon` takes a third path that never reaches `Player.attack` —
  `the-sword-swing`.
- The enchanting seed is re-rolled by `Player.onEnchantmentPerformed`
  (enchanting), **not** by spending levels elsewhere — `enchantments`
  (corrected in session 8) / `hunger-xp-and-effects`.

- There is **no render thread**: the thread named *Render thread* is
  the main thread (`Main` renames it, `Minecraft.gameThread` is it) —
  `the-frame`. `anatomy` predates this and must be re-checked.
- Ticks the client cannot keep up with are **dropped, not deferred**;
  at most ten run per frame — `the-frame`.
- The client lights **per frame**, not per tick, and drains the whole
  queue past a threshold — `client-world-and-options`.
- Animated textures advance **once per frame**, not once per tick, and
  `Minecraft.pick` runs **twice** per ticking frame — `the-frame`.
- The lightmap is drawn on the GPU, once per tick, ignoring partial
  ticks — `lightmap-fog-and-sky`.
- Every per-dimension and per-biome visual constant is an
  `EnvironmentAttribute`; `BiomeSpecialEffects` keeps only
  water/foliage/grass colours — `lightmap-fog-and-sky`. **Part XI must
  not describe biome fog or sky colours as living on
  `BiomeSpecialEffects`.**
- Only **visible** sections are re-meshed, and a dirty flag waits
  indefinitely; there are **three** chunk layers — `level-rendering`.
- Every block entity ticks on the client regardless of simulation
  distance, and client-side scheduled ticks are black-holed —
  `client-world-and-options`.
- The survival inventory is opened entirely client-side and
  `Player.inventoryMenu` has **no `MenuType`** — `gui-and-screens`.
- Block-break particles bypass both the distance cull and the particle
  setting; simulation distance is never sent to the server —
  `particles` / `client-world-and-options`.
- The client **replays the server's opinion** rather than rolling back:
  the ledger stores what the server last said and the ack is permission
  to apply it — `client-world-and-options`.

- A `DensityFunction` graph in the registry is **unseeded and cacheless**;
  it is rewritten by `RandomState` and again by `NoiseChunk`, and a
  `DensityFunctions.Marker` computes nothing on its own — `density-functions`.
- Density-function caches key on **object identity**, so any
  `DensityFunction.SinglePointContext` sampler bypasses them —
  `density-functions`.
- `BiomeSpecialEffects` is **only block tint**; everything else is an
  `EnvironmentAttribute` and the biome is one layer of a stack — `biomes`
  (and `lightmap-fog-and-sky`).
- There are **two biomes per block**: fuzzed for gameplay
  (`BiomeManager.getBiome`), unfuzzed for environment attributes —
  `biomes`.
- Biomes are chosen at `ChunkStatus.BIOMES`, **before** `ChunkStatus.NOISE`
  — the biome shapes the terrain, never the reverse — `biomes`.
- **Carvers never place air**: `WorldCarver.getCarveState` asks the
  `Aquifer` — `worldgen-pipeline`.
- Ore veins are placed in the **noise** step, and the surface pass only
  replaces the settings' default block, so they survive it —
  `worldgen-pipeline`.
- Feature order is **global and topologically sorted**; a cycle between two
  biomes makes the world refuse to load — `features-and-placement`.
- A `RepeatingPlacement` emits N copies of the **same** position; the
  scatter is a separate modifier, so list order is load-bearing —
  `features-and-placement`.
- Writes outside the 3×3 decoration zone are **logged and dropped**, so an
  over-reaching feature is truncated, not moved; and
  `WorldGenRegion.getChunk` **throws** rather than loading, which is why
  cascading worldgen cannot happen — `features-and-placement`.
- A structure's placement lottery is **pure seed arithmetic**; the biome
  test only vetoes afterwards — `structures`.
- Terrain adaptation around a structure writes **no blocks** — it is a
  `Beardifier` density term at `ChunkStatus.NOISE` — `structures`.
- Sapling growth **bypasses the whole placement layer**, on the main
  thread, with no write guard — `features-and-placement`.
- A permission is **not an integer** any more: `PermissionSet` /
  `Permission` / `PermissionCheck` in `net/minecraft/server/permissions`.
  `Commands.LEVEL_GAMEMASTERS` kept its name and changed type. Ints survive
  only in *ops.json*, *server.properties* and the op-level entity event —
  `brigadier-and-commands`.
- `LevelBasedPermissionSet` grants **one** atom (entity selectors, at
  gamemaster and above) and denies all others, including the chat atoms;
  an op does *not* have everything — `brigadier-and-commands`.
- A permission failure is reported as an **unknown command**, because the
  requirement is consulted inside Brigadier's parse —
  `brigadier-and-commands`.
- `/reload` does **not** resend the command tree; clients complete against
  a dead dispatcher until they rejoin, change dimension or are op'd —
  `brigadier-and-commands`.
- Item, block-state and component completion is **local**; the server
  round trip is a fallback, capped at a thousand entries —
  `brigadier-and-commands`.
- `ServerboundChatCommandPacket` does **not** hop to the main thread before
  its legality check; it can disconnect from the Netty thread —
  `brigadier-and-commands`.
- Command execution is a queue, not the Java stack; a fork creates **no
  frames**, the fan-out is lazy for three or more sources, and depth is
  unbounded — only the cost quota and the queue cap stop recursion —
  `execution-and-functions`.
- A forked source **suppresses failure messages**, and every conditional is
  a fork node — `execution-and-functions`.
- Function folders are **singular** (*function/*, *tags/function/*), and a
  macro function reached with no arguments fails **silently, every tick** —
  `execution-and-functions`.
- Advancement subscriptions are per player and only shrink; the client is
  told the requirements but never the criteria or the rewards; the tree is
  laid out **on the server**; and `/reload` rolls back unsaved progress —
  `advancements`.
- Dialogs work in the **configuration phase**, and vanilla does nothing
  with a custom click action but log it — `dialogs-and-tests`.
- The game-test annotations are gone; a batch **is** an environment —
  `dialogs-and-tests`.

## Catalogue gaps found during pass 1

- **Environment attributes and timelines have no page** (session 6).
  `world/attribute` (`EnvironmentAttribute`, `EnvironmentAttributes`,
  `EnvironmentAttributeMap`, `EnvironmentAttributeSystem`,
  `AttributeType`/`AttributeTypes`, `WeatherAttributes`) and
  `world/timeline` (`Timeline`, `Timelines`, `AttributeTrack`) are a 26.2
  system that three written pages already depend on: `DimensionType` lost
  its booleans to it (`level-data-and-rules`), `LavaFluid.isFastLava` reads
  it (`block-ticks-and-fluids`), and the **entire villager schedule** is
  now one of its attributes (`ai-goals-and-brains`). Also note it declares
  a second, unrelated `AttributeModifier` — a real name collision with
  `world/entity/ai/attributes`. Suggested fix: a 57th page in Part IV or a
  short one of its own, for the owner to decide.
  **Session 11 escalates this.** `biomes` had to explain
  `EnvironmentAttributeSystem`'s layer stack (dimension → biome → timeline
  → weather), `EnvironmentAttributeMap.Entry`'s modify-don't-set model,
  and the client's `EnvironmentAttributeProbe` / `GaussianSampler`
  blending, none of which it owns — and Part X's `lightmap-fog-and-sky`
  explains the same system from the other end. Four pages now depend on a
  page that does not exist. Recommendation: write it, in Part IV or as its
  own short part, and cut the paragraph out of `biomes`.

## Verifier lessons (so drafting stays clean)

- Qualify every member: `Class.member`; bare members fail.
- Cite the **declaring** class — the verifier does not walk inheritance
  (`LevelHeightAccessor.getMaxY`, not `Level.getMaxY`; `Entity.absSnapTo`,
  not `LocalPlayer.absSnapTo`; `TypedInstance.is`, not `FluidState.is`).
- Enum/status constants in prose: `ChunkStatus.FULL` or *FULL*.
- Names that do **not** exist in 26.2 go in italics, never backticks.
- Library names (JDK, Guava, fastutil, DFU, jtracy) go in `ALLOW` in
  `tools/verify_names.py`, with a comment.
- Package names need the `pkg/path` form (`world/attribute`,
  `entity/ai`), never the dotted Java form — the verifier matches
  directories by suffix (session 6).
- **The headline paragraph is the biggest trap in a rename-heavy part.**
  Session 10's 66 fixes were mostly gone names written in backticks
  while *introducing* the rename (*ShaderInstance*, *BakedModel*,
  *GuiGraphics*, *MultiBufferSource*, *DimensionSpecialEffects*).
  Italicise a name the moment you say it no longer exists.
- Java keywords and JDK exception names in backticks fail (`long`,
  `OutOfMemoryError`); phrase them as prose. So do bare method names
  used as concepts (`render`, `submit`, `extract`, `get`) — italics.
- **Bare lowercase words in backticks** were session 11's whole fix pass
  (nine names): category or field names used as prose (*visual*, *audio*,
  *gameplay*, *offset*), and Java primitives (*double*). If it is not
  `Class` or `Class.member`, it is italics.
- A member cited on the subclass still fails in Part X:
  `Level.tickBlockEntities` not `ClientLevel.tickBlockEntities`,
  `Model.setupAnim` not `EntityModel.setupAnim` (session 10).

## Questions already known to be waiting for the owner

None yet — the owner has not started reading. When `<!-- Q: -->` comments
appear, a pass-2 session lists the pages here before answering them.
