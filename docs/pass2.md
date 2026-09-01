# Pass 2 — the work queue (completeness and accuracy)

*Repurposed 2026-09-01. Pass 2 is now the AI completeness-and-accuracy
pass defined in [plan.md](plan.md); the owner's read — which this file
originally served — is pass 5. Everything below was consolidated from
pass 1's session log ([pass1.md](pass1.md)) and is the standing input:
pass-2 sessions work it off part by part and tick items here; anything
left for passes 3–5 goes in the hand-off section at the bottom.*

## Split candidates (pages over the ~250-line guideline that carry two ideas)

Pass 2 executes a split when the fact-check adds material and the page
is carrying two subjects anyway; splits that are purely presentational
wait for pass 3 (and feed the lecture-order draft there).

| page | lines | what would split off |
|---|---:|---|
| ~~`server/server-lifecycle`~~ | ~390 | **Session B: not split, and the proposed seam was wrong.** The side threads are four bullets with no trace; a page of them would break rule 4. The page's real seam is its *two traces* (startup and `/stop`) and its best new material is the failure paths. See [pass3.md](pass3.md) §2. |
| `world/game-events-and-poi` | 375 | two traces: sculk/vibrations vs villager POI — the obvious split. **Session C: confirmed but not executed.** The two fact-check halves shared no classes at all, so the seam is real; the fact-check did not add enough to force the split in pass 2, and it is now recorded as presentational in [pass3.md](pass3.md) §2. |
| `world/block-ticks-and-fluids` | ~330 | **Added by session C.** The scheduled-tick scheduler and the fluid model are two lectures with two traces; the page's own numbered trace changes subject at step 6. Not split in pass 2 for the same reason; see [pass3.md](pass3.md) §2. |
| `blocks/redstone` | ~520 | ~~the experimental-evaluator coda vs the default trace~~ — **session D: the proposed seam is wrong, and the page is now three lectures, not two.** The evaluator coda belongs *to* the dust half. The real split is dust/neighbour-updates · pistons/block-events · diodes-and-observers, the last of which session D had to **write** (comparators, repeaters and observers were absent). Not executed; see [pass3.md](pass3.md) §2. |
| `blocks/blocks-and-states` | ~510 | the state table (data page) vs the placement trace + prediction. **Session D: confirmed and not executed.** The fact-check grew both halves evenly and neither became unwieldy; purely presentational, so pass 3's call. |
| `blocks/block-interaction` + `blocks/block-breaking` | ~456 + ~445 | **Added by session D.** Not a split — a possible *merge*, or a shared preamble. The two pages re-derive the same prediction ledger, reach check, sequence number and ack ordering, and session D had to correct the same ack-timing sentence in both. See [pass3.md](pass3.md) §1. |
| `entities/entity-anatomy` | 367 | the base class + `EntityType` vs the hierarchy tour. **Session E: confirmed, not executed.** The fact-check grew both halves; the seam is real but presentational, and the page is Part VI's map page, which argues for keeping it whole. Pass 3's call — see [pass3.md](pass3.md) §2. |
| `entities/ai-goals-and-brains` | 357 | goals vs brains vs pathfinding — three lectures in one page. **Session E: confirmed, and the third lecture is the strongest of them.** Pathfinding grew most in the fact-check (node budget, `Path.canReach`, stuck detection) and shares almost nothing with the goals/brains split except `MoveControl`. Not executed; see [pass3.md](pass3.md) §2. |
| `entities/movement-and-collision` | ~400 | **Added by session E.** Not a split — the page acquired a new *first* section (the authority matrix: `Entity.isLocalInstanceAuthoritative` / `canSimulateMovement` / `isEffectiveAi` / `isClientAuthoritative`) that is arguably a lecture of its own and is the shared prerequisite of this page, Part VIII's *input to movement* and Part IX's *what the client is told*. Decide one owner in pass 3. |
| `items/items-and-stacks` | 340 | the stack data model vs the use pipeline + the eating trace |
| `items/containers-and-menus` | 320 | the menu/slot model vs the click protocol (state id, `HashedStack`) |
| `player/player-anatomy` | 404 | the class ladder + `Inventory`/`Abilities` (a data page) vs the two-phase tick trace |
| `player/input-to-movement` | 305 | the client input chain vs the server's validation and rubber-band |
| ~~`client/client-world-and-options`~~ | ~300 | **Session H: executed, four ways.** The page is gone; its four subjects became `the-client-level`, `prediction-and-acks`, `input-and-keybinds` and `options`. The prediction ledger got the single owner the entry asked for, and the three other pages that described it now link to it. The proposed `input-and-keybinds` seam (`ClientInput.tick`) was wrong in detail — the real seam is the *callback*, because GLFW handlers run inline on the game thread, not queued. |
| ~~`client/gui-and-screens`~~ | ~300 | **Session H: executed, three ways.** The text engine left as `text-and-fonts` (the entry's own proposal) and the record/draw model left as `the-gui-render-tree`, which the entry did not anticipate and which is the more interesting of the two. What is left is the screen lifecycle and container screens. |
| `client/level-rendering` | ~310 | the meshing pipeline (dirty → compile → upload) vs visibility and the frame graph (session 10). **Session H did not touch it — it is Part XI now (`systems/rendering/`) and belongs to session I.** |
| `worldgen/structures` | 307 | the placement decision (sets, `StructurePlacement`, `StructureCheck`, `/locate`) vs jigsaw assembly and template placement — two lectures, and the only page in Part XI with two distinct mechanisms (session 11) |
| `worldgen/density-functions` | 307 | the node library and the codec/registry model vs the two rewrites (`RandomState`, `NoiseChunk.wrapNew`) and the cell loop. The rewrite story is the lecture; the catalogue is reference (session 11) |
| `commands/brigadier-and-commands` | 313 | the parse/suggest/permission story vs the permission model itself. The permission rewrite (`PermissionSet`, `Permission`, `PermissionCheck`, `LevelBasedPermissionSet`) is a lecture on its own and is currently a section inside a page whose trace is `/give`; it is also the single biggest API break in the corpus and deserves the billing (session 12) |
| `commands/execution-and-functions` | 310 | the non-recursive engine (queue, `Frame`, forks, `/return`) vs the function model (compile, macros, tags). Two lectures; the seam is clean and the second half is the one data-pack authors want (session 12) |
| `appendix/naming-drift` | 422 | not a split candidate — a reference table. Flagged only so nobody counts it as an over-long page (session 12) |

Parts III–V all came out at 260–380 lines. Where a split is deferred,
the "one page, two lectures" call gets settled by pass 3's lecture-order
draft.

## Carried over from pass 1's closing session (never ran; folded into pass 2)

The diagram-consistency and lane-abbreviation items below are **pass-3**
work (the lane standard is settled corpus-wide there); the content
re-reads and appendix rulings are pass-2 session A / session K work.

- [x] `anatomy` threads table: add *Management server IO*, *RCON Listener /
  Client*, *Query Listener* (found in session 3); confirm against
  `reference/threads.md`. **Done, session A** — all three added to both the
  page and `src/reference/threads.md`, which had the same gap, plus a
  "situational threads" paragraph for the ones no lecture hangs on.
- Appendix tour still needs its paragraph on JSON-RPC (`server/jsonrpc`,
  `ManagementServer`) — session K. *pause-when-empty-seconds* is now
  covered in `anatomy` (the dedicated server pauses too), so the appendix
  only needs to point at it.
- [x] Re-read `anatomy` and `sound` against the finished corpus. **Done,
  session A** — both were substantially wrong; see the session log in
  [plan.md](plan.md).
- Diagram consistency: lane names are class names everywhere; check that
  the same class is abbreviated the same way across parts
  (`ServerGamePacketListenerImpl` is *SG* in Part V, *SGPL* in Parts VII
  and IX, *CL* in Part VIII, *G* in Part III; `ClientPacketListener` is
  *CPL*, *CP* and *CL*. Session 9 used *SGPL* / *CPL*; pick one.)
- Glossary + the naming-drift appendix (list below).
- Part X diagram lanes use `LX` (`LevelExtractor`), `LR`, `GR`
  (`GameRenderer`), `SRD`, `ERD`, `FRD`, `PE`, `H`/`G` — fold into the
  lane-abbreviation decision above (session 10).
- [x] `sound` was written before the extract/render split was documented;
  re-read it against `the-frame` and check whether the sound engine's
  threading paragraph still matches (session 10). **Done, session A** —
  it did not: the page claimed every OpenAL call was on the sound thread
  (device setup, teardown and enumeration are not) and that nothing
  outside `client/sounds` touches OpenAL (exactly inverted).
- [x] `anatomy` predates Part X. Check its claim about the render thread:
  in 26.2 the thread named *Render thread* **is** the main thread, and
  the client has no second render thread (session 10). **Confirmed,
  session A** — there is no *initGameThread* and no *isOnGameThread*
  anywhere in the tree; `anatomy` now says so explicitly.
- The naming-drift appendix will be dominated by Part X. It is by far
  the biggest source of gone names in the corpus (session 10).

- **Session 12 additions.** The appendix now exists, so the closing pass
  has three concrete jobs on it rather than a wish:
  - `appendix/naming-drift` is generated from the table below plus a
    hand-written Part XII block. If pass 2 finds a *wrong* row, fix it in
    both places or the next regeneration reintroduces it.
  - `appendix/out-of-scope-tour` ends with a **gaps** list — the debug
    cluster, `client/resources`, `util/parsing`, `client/animation`,
    Blaze3D's Vulkan and platform halves. Each needs a ruling: absorb into
    an existing page, add a page, or decline explicitly. **Session H ruled
    on the debug cluster: it got a page** (`debugging-the-running-game`,
    Part X), because the "server-side subscription system" turned out to be
    the interesting part and the largest undocumented system in the corpus —
    a registry of `DebugSubscription`s, a per-level poll-and-diff engine that
    sleeps until somebody subscribes, six packets, and about two dozen
    renderers. The tour's bullet now points at it. The remaining four are
    still session K's.
  - `appendix/glossary` has ~110 entries and deliberately stops there. It
    should be re-swept once the lecture order exists, because the lecture
    order decides which page "owns" a term when two could.
- The **lane-abbreviation** decision now also covers Part XII, which used
  full-ish abbreviations (`SGPL`, `CPL`, `EC`, `PA`) — consistent with
  session 9's choice, so `SGPL`/`CPL` is now the majority spelling.
- [x] `anatomy`'s thread table should gain the **management server** (JSON-RPC,
  its own Netty bootstrap) alongside RCON and query — the appendix tour
  describes it and `anatomy` predates it. **Done, session A.**
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
| `Ingredient.EMPTY` | gone — `Ingredient.CODEC` rejects an empty literal list, but a tag that resolves to nothing still yields an empty one, hence `Ingredient.isEmpty` | session 7, **corrected session F** |
| `ClientboundUpdateRecipesPacket` carrying recipes | property sets + the stonecutter input set; the book gets `RecipeDisplayEntry`s | session F |
| `net.minecraft.advancements.CriteriaTriggers` | `CriteriaTriggers`, moved to the *advancements.triggers* package | session F |
| `Player.permissionLevel` / `hasPermissions(int)` | `Player.permissions` → a `PermissionSet`, queried by named `Permissions` keys | session F |
| `ServerboundPlayerCommandPacket.Action.PRESS_SHIFT_KEY` / `RELEASE_SHIFT_KEY` | gone — sneak rides `ServerboundPlayerInputPacket` → `Entity.setShiftKeyDown` | session F |
| `Mannequin` on the client | `ClientMannequin`, installed by swapping the mutable `Mannequin.constructor` factory at client startup | session F |
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
| `Font.drawInBatch` and every `drawString` variant | `Font.prepareText` → `Font.PreparedText`, drawn by somebody else | session H |
| `Font.StringRenderOutput` | `Font.PreparedTextBuilder` (private), exposed as `Font.PreparedText` + `Font.GlyphVisitor` | session H |
| `BakedGlyph` (a class) | an interface; the sheet implementation is `BakedSheetGlyph`, effects are `EffectGlyph` | session H |
| `RawGlyph` / `SheetGlyphInfo` | `UnbakedGlyph` (info + bake) and `GlyphBitmap` (pixels + upload) | session H |
| `GlyphProviderBuilder` / `GlyphProviderBuilderType` | `GlyphProviderDefinition` / `GlyphProviderType` | session H |
| `Style.getFont` returning an id | still `Style.getFont`, but it returns a `FontDescription` — which may be a *sprite*, not a font | session H |
| `FontSet.getGlyph` as public API | private; the entry point is `FontSet.source` → `GlyphSource.getGlyph` | session H |
| `Minecraft.destroy` | gone — `Minecraft.stop`, then `Minecraft.exitWorldAndClose` and `Minecraft.close` | session H |
| raw `(key, scancode, modifiers, action)` on every `Screen` method | the `client/input` records: `KeyEvent`, `MouseButtonEvent`, `CharacterEvent`, `PreeditEvent`, over `InputWithModifiers` | session H |
| `Options.keyBindings` | `Options.keyMappings`; `KeyMapping.Category` is a registrable record, not a translation-key string | session H |
| `RenderStateShard` composition | `RenderType` over a `RenderPipeline`, catalogued in `RenderTypes`, built by `RenderSetup`, resolved to a `PreparedRenderType` | session I |
| `BakedQuad` as a 4-vertex array | a 10-component record: 4 positions, 4 packed UVs, a recomputed `Direction`, and a 6-component `BakedQuad.MaterialInfo` | session I |
| `LiquidBlockRenderer` | `FluidRenderer`, fed by a `FluidStateModelSet` of `FluidModel` | session I |
| `DimensionSpecialEffects.forType` | `DimensionType.skybox` (`DimensionType.Skybox`), plus `EnvironmentAttributes` | session I |
| `ParticleGroup` as a limit record | `ParticleLimit`; `ParticleGroup` is the per-render-type bucket | session I |
| `ScreenManager` (in Blaze3D) | never existed — monitor handling is `MonitorManager`; menu-type→screen mapping is `MenuScreens` | session I |
| `Window.updateDisplay` / `setVsync` | `GpuSurface.present`; vsync is a `GpuSurface.PresentMode` in the surface configuration | session I |
| `ItemOverrides` / `getPropertyOverride` | `SelectItemModel` / `RangeSelectItemModel` / `ConditionalItemModel` over `renderer/item/properties` | session I |
| `Options.mouseSensitivity` and the other public option fields | private fields with same-named accessor *methods* (`Options.sensitivity()`) | session H |
| `MouseHandler.lastMouseEventTime` | gone | session H |
| `ClientChunkCache.ChunkArray` | `ClientChunkCache.Storage` | session H |
| `ClientLevel.getStarBrightness` / `ClientLevel.effects` | `EnvironmentAttribute` lookups through the probe | session H |

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

| *SwordItem* | gone — a kit of components on a plain `Item`. `AxeItem` / `ShovelItem` / `HoeItem` **survive**, for stripping, path-making and tilling only | session A |
| integer `pack_format` | `PackFormat` major/minor, with *min_format* / *max_format* replacing it above `PackFormat.lastPreMinorVersion` | session A |
| *ClientboundCustomSoundPacket* | gone — `ClientboundSoundPacket` carries an inline `SoundEvent` when it needs to | session A |
| `RandomSource.createThreadSafe` / `ThreadSafeLegacyRandomSource` | deprecated; `LegacyRandomSource`'s atomic is a `ThreadingDetector`, not a safety feature | session A |
| `Registry.getRandom` on a tag | `HolderSet.getRandomElement` (`Registry.getRandom` still exists, for a whole registry) | session A |
| `BlockPos.betweenClosed` backed by *Cursor3D* | `Cursor3D` is a separate cursor (`SectionPos`, `BlockCollisions`, `ClientLevel`); `BlockPos` iterators reuse a `BlockPos.MutableBlockPos` | session A |
| `ParserUtils` / lenient JSON everywhere | `StrictJsonParser` for data, `LenientJsonParser` for the two surviving JSON packets | session A |

| `GameProfile` on the player lists | `NameAndId` (record of UUID + name) — `canPlayerLogin`, `isWhiteListed`, `op`, all four stored-user files | session B |
| `MinecraftServer.getProfilePermissions` → int | → `LevelBasedPermissionSet` | session B |
| `ServerPlayer.sendAllPlayerInfo` / `sendActivePlayerEffects` | declared on `PlayerList`, not `ServerPlayer` | session B |
| `ServerPlayer.resetPosition` | `ServerGamePacketListenerImpl.resetPosition` | session B |
| `PoiManager.flushAll` | `SectionStorage.flushAll` (inherited) | session B |
| `QueryThreadGs4.stop` | `GenericThread.stop` (inherited; `RconThread.stop` *is* overridden) | session B |
| `ScheduledTick.DRAIN_ORDER` as the level's drain order | `ScheduledTick.INTRA_TICK_DRAIN_ORDER`; `DRAIN_ORDER` orders each chunk's own queue | session B |
| day time → sky light on the level | `EnvironmentAttributes.SKY_LIGHT_LEVEL` via `EnvironmentAttributeSystem` | session B |
| `MinecraftServer.scheduledEvents` as level state | server-wide `TimerQueue`, advanced by the overworld's `ServerLevel.tickTime` | session B |

## Cross-part obligations — discharged

Every "link, don't repeat" obligation recorded during pass 1 was
discharged as its part was written; the full ticked list is in this
file's git history and in [pass1.md](pass1.md)'s session log. The rule
itself still applies: a fact-check agent that finds a page *re-explaining*
a mechanism another page owns should flag it as a *misleading* finding.

## Load-bearing facts (the fact-check seed list)

Each fact below is established once, in the page named, and other pages
lean on it — so these are what the pass-2 fact-check agents verify
hardest: a wrong entry here corrupts every page that cites it. All are
easy to get wrong from 1.21 memory.

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
  `LivingEntity` with no `GoalSelector` and no `PathNavigation` — but it
  *does* have a `Brain`, which is declared on `LivingEntity`, not `Mob`
  (**corrected session E**) — `entity-anatomy`.
- `LevelWriter.addFreshEntity` is a default returning false; **two** classes
  implement it, `ServerLevel` and `WorldGenRegion`, and the second writes
  into the proto-chunk instead of the section manager (**corrected session
  E**) — `entity-lifecycle`.
- There are two mob caps (global, scaled by covered chunk area; and
  per-player) and persistent mobs count for neither; persistent *categories*
  are additionally offered a spawn only every 400 ticks — `entity-lifecycle`.
- Synched-data ids are class-tree ordinals; defaults never travel; the
  client's writes are discarded — `synched-entity-data`.
- Eight attributes are not client-syncable, `Attributes.ATTACK_DAMAGE`
  among them, so the client's damage prediction is always stale —
  `attributes`. (Re-counted in session E against all 40 registrations:
  exact, and the eight names are exact.)
- Damage is server-only (`Entity.hurtServer`); the amount never crosses
  the wire; i-frames compare against the last damage — and a hit that lands
  *inside* the window sends no packet, no knockback and no flash either
  (**session E**) — `damage-and-death`.
- AI is strictly single-threaded and pathfinding never loads a chunk —
  `ai-goals-and-brains`.
- **A tracked mob's physics run on the server only.** The client never calls
  `Entity.move` for it — `LivingEntity.aiStep` gates travel on
  `Entity.canSimulateMovement`, and a client-side mob coasts and
  interpolates instead. A *player* is the mirror image: client-authoritative
  on both sides. (**Session E; this reverses what the page said.**) —
  `movement-and-collision`.
- An unknown entity id in **save data** drops the entity with a *Skipping
  Entity* warning; the registry's pig default applies only to the value and
  numeric lookups the network uses (**session E**) — `entity-anatomy`.
- Attribute mutations made during the entity phase are broadcast on the
  **next** tick: `ChunkMap.tick` runs in the chunkSource phase, before
  entities. Merely *reading* an attribute for the first time dirties it
  (**session E**) — `attributes`.
- An item's default components are built at *reload*, not at
  construction; `Item.components` throws before then — `items-and-stacks`.
- A shift-click that agrees costs **zero** clientbound packets; the
  server adopts the client's hash as its new baseline — `containers-and-menus`.
- The client is never sent a recipe. A `RecipeDisplayId` is a list index,
  and — **refined session F** — it is *deterministic* for a given recipe
  set and unstable across any change to it; the server does not try to
  work out which, and re-sends the whole book with a replace flag. It does
  hold the whole *contents* of every recipe it has unlocked, as a
  `RecipeDisplay`; what it is denied is the identity — `recipes`.
- No enchantment **entity or location-based** effect can run on the
  client — but **corrected session F**, two *value* effects do:
  `Enchantment.modifyCrossbowChargeTime` and
  `Enchantment.modifyTridentSpinAttackStrength` take a `RandomSource` and
  no level, and are reached from the item renderer, three entity renderers
  and `MultiPlayerGameMode.useItem`. Also corrected: the client usually
  receives only the enchantment's *id*, not the definition — the
  known-packs handshake elides contents the client's own pack already has
  — `enchantments`.
- Loot tables are never synced; a chest's table key is cleared *before*
  the roll, and a container **read** (a hopper's pull, a comparator)
  commits it with no player luck. **Corrected session F:** `/data` does
  *not* — the save path writes the key back out and never touches the
  items, and `clearContent` and `getContainerSize` do not unpack either.
  The unpacking reads are emptiness, item read, both removals and item
  write — `loot-tables`.

- The server **simulates a human player fully every tick and then throws
  the position away** (`ServerGamePacketListenerImpl.tickPlayer` →
  `ServerPlayer.doTick` → snap back to `firstGood…`); the authoritative
  position only moves in `handleMovePlayer` or a teleport, and the
  simulation exists to produce `Entity.getDeltaMovement` for the
  anti-cheat — `input-to-movement`.
- `ServerboundPlayerInputPacket` never moves **the player** — but
  **corrected session F**, it is not inert: `NewMinecartBehavior` and
  `OldMinecartBehavior` both read `ServerPlayer.getLastClientMoveIntent`
  to nudge a stalled cart, and the handler itself calls
  `Entity.setShiftKeyDown`. The advancement `InputPredicate` is the third
  consumer — `input-to-movement`.
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

- Outbound packets leave a server tick in **two** flushes per client, not
  one: `Connection.tick` flushes inside the suspend/resume bracket, and the
  second flush carries everything `MinecraftServer.tickChildren` does after
  it — player list, debug subscribers, game-test ticker, tickables, and
  last the chunk batch (**narrowed session G**, which read `tickChildren`;
  the earlier "only the chunk batch" was too tight) — `server-tick` (and
  corrected in `anatomy` and `the-connection`).
- `MinecraftServer.haveTime` is **true whenever a task is running**, and the
  budget stops applying altogether inside `BlockableEventLoop.managedBlock`
  (`shouldRunAllTasks` skips `shouldRun`). That is why a level can block on a
  chunk mid-tick — `server-tick`.
- "Can't keep up!" **logs and skips in the same condition**: a server that
  warned recently stays behind instead of skipping — `server-tick`.
- A serverbound packet handler that throws is **logged and suppressed**, not
  fatal and not a disconnect; `ClientboundDisconnectPacket` comes from a
  throw out of `Connection.tick` instead — `server-tick`.
- `ServerChunkCache.broadcastChangedChunks` runs **before** `ChunkMap.tick`,
  so block changes are queued ahead of the same tick's entity movement; and
  the broadcast unit is the **16³ section**, not the chunk —
  `server-level-tick`.
- `TicketStorage.purgeStaleTickets` **is** gated by `runsNormally`, so a
  frozen world never expires a ticket — `server-level-tick`. (The rest of the
  chunk system is genuinely un-gated.)
- An empty dimension past `ServerLevel.EMPTY_TIME_NO_TICK` skips exactly
  three things — dragon fight, entity loop, block entities. The entity
  manager's load/unload drain and the debug feed keep running —
  `server-level-tick`.
- The level tick's **first** statement is
  `EnvironmentAttributeSystem.invalidateTickCache`, and sky brightness is read
  from `EnvironmentAttributes.SKY_LIGHT_LEVEL` — `server-level-tick`. Part IV's
  new environment-attributes page must agree.
- `LocalMobCapCalculator` uses the **raw** `MobCategory.getMaxInstancesPerChunk`
  per player, not the chunk-scaled global cap — two different formulas —
  `server-level-tick`.
- Identity on the server is a `NameAndId` record, not a `GameProfile`;
  the whitelist is bypassed by being an **op**, and `bypassesPlayerLimit`
  applies only to the capacity check — `players-and-sessions`.
- A joining player gets **one** unacknowledged chunk batch, not ten; the
  limit rises to ten only after the client's first acknowledgement —
  `players-and-sessions` / `tickets-and-loading`.
- `ServerPlayer.restoreFrom`'s "restore everything" branch is the
  **end-credits** return, not *keepInventory* — `players-and-sessions`.
- **A player's fall damage never comes from the server's own simulation.**
  `Entity.move` gates `Entity.checkFallDamage` on local-instance
  authority, which is false for a `ServerPlayer`; it comes from
  `Entity.doCheckFallDamage` on the movement-packet path, computed from
  the client's reported delta (**session F**) —
  `input-to-movement` / `player-anatomy`.
- **Against a mob the client predicts nothing at all.** `Entity.hurtClient`
  returns false and neither `LivingEntity` nor `Mob` overrides it, so on
  the client `Player.attack`'s whole post-hit block — knockback, sweep,
  visual effects, durability, exhaustion — is skipped. `RemotePlayer` is
  the exception (**session F**) — `the-sword-swing`, agreeing with
  session E's `damage-and-death`.
- **A menu change made by a block entity reaches the client on the *next*
  tick; one made by a packet handler reaches it in the same tick.**
  Packets drain before the levels tick, and `ServerPlayer.tick`'s
  broadcast runs in the entity phase, before block entities. Nothing calls
  back into the menu — `Container.setChanged` is a no-op, a chunk mark or
  a counter (**session F**) — `containers-and-menus`.
- **`Item.getAttackDamageBonus` is added between the sprint-knockback
  branch and the crit**, so the mace's fall bonus is multiplied by the
  ×1.5 (**session F**) — `the-sword-swing`.
- **`ServerboundSetCreativeModeSlotPacket` is the one packet whose *data*
  the server adopts verbatim**, straight into `Inventory` behind four
  cheap gates. Every other client claim is a hash to compare against
  (**session F**) — `containers-and-menus`.
- **`CraftingMenu.slotChangedCraftingGrid` is a third state-id bump and an
  unsuppressed clientbound channel**, sending a slot packet mid-click,
  outside `ContainerSynchronizer` and outside
  `AbstractContainerMenu.suppressRemoteUpdates` (**session F**) —
  `containers-and-menus` / `recipes`.
- **`ClientboundSetExperiencePacket` is change-detected on
  `Player.totalExperience` alone**, which is why five level-only mutations
  poison `ServerPlayer.lastSentExp` to force it (**session F**) —
  `hunger-xp-and-effects`.
- **Starvation's floor is five hearts on Easy, not ten**, the health term
  is difficulty-independent, and the branch is not gated by
  `GameRules.NATURAL_HEALTH_REGENERATION` although both regen branches are
  (**session F**) — `hunger-xp-and-effects`.
- Shutdown does **not** call `MinecraftServer.saveEverything`; it calls
  `PlayerList.saveAll` then `MinecraftServer.saveAllChunks` —
  `server-lifecycle`.
- `ServerConnectionListener.stop` closes only the **bound** channels; live
  sessions are severed by `PlayerList.removeAll`, and a connection still in
  handshake/login/configuration is closed by neither — `server-lifecycle`.
- **A tick-loop crash saves the world; a watchdog kill does not.**
  `ServerWatchdog` calls `System.exit`, whose hook joins the wedged Server
  thread, so `Runtime.halt` fires ten seconds later with nothing written —
  `server-lifecycle`.
- `MinecraftServer.prepareLevels` re-arms only **persistent** tickets, of
  which there are two types (`TicketType.FORCED`, `TicketType.PORTAL`).
  There is no spawn ticket; on an ordinary world the step loads nothing —
  `server-lifecycle`.

- `Level.setBlock` runs **three** shape passes, not one — the old state's
  indirect, the new state's direct, the new state's indirect — and ends with
  `Level.updatePOIOnBlockStateChange`. `Block.UPDATE_NEIGHBORS` and
  `Block.UPDATE_SUPPRESS_DROPS` are masked out of the flags it propagates —
  `blocks-and-states`.
- `BlockBehaviour.BlockStateBase.onPlace` is gated on **side and flag 512
  only**, not on the block changing: a same-block state write on the server
  runs it — `block-interaction`.
- `Block.updateOrDestroy`'s **destroy** branch is server-only and goes through
  `Level.destroyBlock` at flags 3, so a shape cascade that kills a block does
  fire neighbour updates and a `GameEvent.BLOCK_DESTROY`. That is why breaking
  one door half is *not* predicted for the other — `block-interaction`.
- Block entities tick in the **last** world phase, after the chunk-source
  broadcast drain and after the entity phase. So a block entity's own block
  write and its menu data both reach clients on the **following** tick —
  `block-entities` (agrees with `server-level-tick`).
- `Level.tickBlockEntities` is gated by `TickRateManager.runsNormally` and by
  `Level.shouldTickBlocksAt`, which on the server is **simulation distance**:
  a loaded chunk's furnaces need not tick. Both gates pass trivially on the
  client — `block-entities`.
- Twenty of the 49 block-entity types send a `ClientboundBlockEntityDataPacket`
  (nineteen classes declare `BlockEntity.getUpdatePacket`;
  `HangingSignBlockEntity` inherits `SignBlockEntity`'s) — `block-entities`.
- `Tool.getMiningSpeed` and `Tool.isCorrectForDrops` are **two independent
  scans** of the rule list, each skipping rules that lack the field it wants.
  Hence full pickaxe speed on obsidian with no drop — `block-breaking`.
- A failed reach check on a dig or a use sends the client **nothing at all**;
  spawn protection sends only a chat overlay. Only build height,
  `ServerLevel.mayInteract` and `Player.blockActionRestricted` answer with a
  `ClientboundBlockUpdatePacket` — `block-breaking`, `block-interaction`.
- **ABORT does not cancel a deferred destroy.** `ServerPlayerGameMode.tick`
  tests `hasDelayedDestroy` first and the ABORT branch never clears it, so a
  client that STOPs early and releases still gets the block broken — and the
  delayed path re-checks nothing but `isAir` — `block-breaking`.
- Piston placeholders are written with flags 324, **without**
  `Block.UPDATE_CLIENTS`: the client's moving blocks come *only* from
  re-running `PistonBaseBlock.moveBlocks` off `ClientboundBlockEventPacket`,
  and no correcting packet ever follows — `redstone`.
- There are **three** direction orders, not two: `SignalGetter.DIRECTIONS`
  (D U N S W E) decides what a block *reads*, against
  `BlockBehaviour.UPDATE_SHAPE_ORDER` (W E N S D U) and
  `NeighborUpdater.UPDATE_ORDER` (W E D U N S) for what gets *notified* —
  `redstone`.
- The **observer fires on shape updates**, not neighbour updates
  (`ObserverBlock.updateShape` → a two-tick scheduled tick) — `redstone`.

- The environment-attribute layer stack is **fixed and four deep**:
  dimension (constant) → biome (positional) → timelines (time-based) →
  weather, built once in the level constructor and never rebuilt —
  `environment-attributes-and-timelines`.
- A biome may only set **positional** attributes
  (`EnvironmentAttributeMap.CODEC_ONLY_POSITIONAL`); exactly two attributes
  are non-positional, `EnvironmentAttributes.SKY_LIGHT_LEVEL` and
  `EnvironmentAttributes.FAST_LAVA` —
  `environment-attributes-and-timelines`.
- The wire carries the **rules**, not the values: `Registries.TIMELINE` and
  `Registries.WORLD_CLOCK` are synced registries, and the client rebuilds
  the same layer stack. The only per-tick traffic is `ClientboundSetTimePacket`
  — `environment-attributes-and-timelines`.
- `WorldGenRegion.environmentAttributes` returns `EnvironmentAttributeReader.EMPTY`:
  **worldgen sees attribute defaults only** —
  `environment-attributes-and-timelines`.
- `TicketType.ENDER_PEARL` is loading **and** simulation (and
  keep-dimension-active) — `tickets-and-loading`.
- The player-ticket throttler runs its submitted task on the **main
  thread**; only the dispatcher's queue bookkeeping is on a worker. Nothing
  in the ticket system adds a ticket from a worker — `tickets-and-loading`.
- `ChunkHolder.sendSync` starts already complete. `ChunkMap.waitForLightBeforeSending`
  has exactly one caller, `EnderDragonFight` — `tickets-and-loading` /
  `lighting`.
- A light write marks only the sections the written block touches (one, or
  up to eight on a corner), **not** 27. The 3×3×3 marking happens once, when
  a section is first given a `DataLayer` — `lighting`.
- `MinecraftServer.forceSynchronousWrites` is true in the **base class**;
  both subclasses override it, and singleplayer's default is *Windows only*
  — `chunk-storage`.
- Datafixing on the chunk read path happens on the **worker pool**, between
  the IO lane and `SerializableChunkData.parse` — `chunk-storage`.
- Every `SavedData` file lives under a **namespace folder**:
  *data/&lt;namespace&gt;/&lt;id&gt;.dat* — `level-data-and-rules`.
- Five game rules reach the client, not three; the fifth is
  `GameRules.ADVANCE_TIME`, which broadcasts a clock sync —
  `level-data-and-rules`.
- `ServerLevel.getRespawnData` returns the **server's effective** spawn,
  relocated if it has fallen outside the border — `level-data-and-rules`.
- Lava random-ticks **twice** per selected position, once as a block and
  once as a fluid — `block-ticks-and-fluids`.
- A `ChunkAccess` built from a `ProtoChunk` copies the section **array**;
  the section objects are shared — `chunk-anatomy`.
- `ThreadingDetector` kills **both** threads, and the winner throws first,
  from `checkAndUnlock` — `chunk-anatomy`.
- `PalettedContainer.pack` uses the **same tier ladder** as memory; packing
  shrinks the palette, not the width — `chunk-anatomy`.
- `ChunkLevel.generationStatus` maps 34 to *INITIALIZE_LIGHT*, not *SPAWN* —
  `chunk-generation-pipeline`.
- The pyramid is chosen **per chunk, per layer**, so one task's ring mixes
  both pyramids — `chunk-generation-pipeline`.
- `ChunkStep`'s default block-state write radius is **−1**: most steps may
  not write at all — `chunk-generation-pipeline`.

- There is **no render thread**: the thread named *Render thread* is
  the main thread (`Main` renames it, `Minecraft.gameThread` is it) —
  `the-frame`. `anatomy` predates this and must be re-checked.
- Ticks the client cannot keep up with are **dropped, not deferred**;
  at most ten run per frame — `the-frame`.
- The client lights **per frame**, not per tick, and drains the whole
  queue past a threshold — `client-world-and-options`.
- ~~Animated textures advance **once per frame**~~ — **falsified twice.**
  Session H corrected the `Minecraft.pick` half (once per tick *and* once per
  frame). Session I corrected the rest: `TextureManager.tick` is outside the
  catch-up tick loop **and** gated on the level running normally, so a laggy
  client advances animations once per *tick batch* and a frozen or paused
  world does not advance them at all — `the-client-loop`, `models-and-atlases`.
- The lightmap is drawn on the GPU, once per tick, ignoring partial
  ticks — `lightmap-fog-and-sky`.
- **Nearly** every per-dimension and per-biome visual constant is an
  `EnvironmentAttribute`; `BiomeSpecialEffects` keeps only
  water/foliage/grass colours — `lightmap-fog-and-sky`. **Part XI must
  not describe biome fog or sky colours as living on
  `BiomeSpecialEffects`.** *(session I: "every" needs the qualifier.*
  `DimensionType.ambientLight` *and* `DimensionType.cardinalLightType` *are
  plain record fields, not attributes, and block tint is still* `BiomeColors`
  *reading* `BiomeSpecialEffects`*.)*
- Only **visible** sections are re-meshed, and a dirty flag waits
  indefinitely *while its ring slot stays put*; there are **three** chunk
  layers, and the mesher can still overrule a quad's baked layer (leaves,
  fluids) — `level-rendering`.
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

- `Gui` is the whole 2D UI layer; the HUD is `Hud`, reached as `Gui.hud` —
  `anatomy`. Any page that says "the HUD (`Gui`)" is wrong.

- The client's loop **drops** the ticks it cannot run — at most ten per frame,
  and the rest are already gone from the residual — while the server never
  drops a tick, only runs late. `Minecraft.MAX_TICKS_PER_UPDATE` exists and has
  **no callers**; the clamp is a literal — `the-client-loop`.
- **The server owns the client's tick rate.** `DeltaTracker.Timer`'s
  target-milliseconds provider is `Minecraft.getTickTargetMillis`, which reads
  the level's `TickRateManager` — so `/tick rate` changes the arithmetic inside
  the client's frame loop — `the-client-loop`.
- **GLFW callbacks are not queued.** `BlockableEventLoop.execute` runs the task
  inline when already on the thread, and `RenderSystem.pollEvents` dispatches on
  the game thread — so input handlers run *before* the tick that observes them.
  Any page that says input is "queued onto the client thread" is wrong —
  `input-and-keybinds`.
- `Minecraft.pick` runs **once per tick and once per frame**, not "twice per
  ticking frame" — `the-client-loop`.
- **The acknowledgement is a receipt for a sequence number, not a verdict.**
  `ServerGamePacketListenerImpl.ackBlockChangesUpTo` fires for rejected actions
  too, and even for an unsequenced abort (an ack of 0). Correctness rests on the
  ordering rule: corrections travel earlier in the same tick —
  `prediction-and-acks`.
- An inbound block update is only swallowed **for a position in the ledger**;
  for any other position `ClientLevel.setServerVerifiedBlockState` writes the
  world at once — `prediction-and-acks`.
- **`Options.save` is the only caller of `Options.broadcastOptions`, and that is
  weaker than it sounds**: every cycle-option button calls `Options.save` on
  click. Sliders wait for the screen to close; cycles do not — `options`.
- **The server never replies to a view-distance request.**
  `ClientboundSetChunkCacheRadiusPacket` is only ever broadcast by
  `PlayerList.setViewDistance` when the *server's* distance changes. The client
  clamps itself — `options`.
- In singleplayer, `IntegratedServer.tickServer` reads the render **and
  simulation** sliders off the client's options every tick. "Simulation distance
  is never sent to the server" is true only of multiplayer — `options`.
- **`Level.tickBlockEntities` still checks the tick rate manager**, so "every
  block entity ticks everywhere" is true of distance and false of `/tick
  freeze` — `the-client-level`.
- Only the client's light **queue** is budgeted (a tenth of the backlog, floored
  at ten, or all of it past a thousand); `LevelLightEngine.runLightUpdates`
  drains completely every frame — `the-client-level`.
- **F1 does not hide the sleep fade**, which sits between the HUD's two
  hidden-gated blocks; and the saving indicator, toasts, the debug overlay and
  deferred subtitles are recorded by `Gui`, not `Hud` — `hud`.
- **`Gui.isPausing` is what pauses the integrated server**, and
  `Screen.isPauseScreen` defaults to true — `AbstractContainerScreen` overrides
  it to false. That is why a chest does not pause singleplayer —
  `gui-and-screens` / `the-client-loop`.
- **Measuring text bakes glyphs.** `Font.width` resolves to a *baked* glyph, so
  measuring a never-seen codepoint stitches it into a texture and uploads it —
  `text-and-fonts`.

- **A failed surface acquisition does not skip the frame, only the picture.**
  The whole frame renders into `GameRenderer.mainRenderTarget`; only the blit
  and the present re-test the surface. A minimized window renders complete
  frames nobody sees — `the-frame`.
- One frame uses **five** partial ticks, and one of them is **per entity**:
  `LevelExtractor` asks `DeltaTracker.getGameTimeDeltaPartialTick` with the
  frozen flag per entity, and `TickRateManager.isEntityFrozen` excludes
  players — so under `/tick freeze` mobs pin and players interpolate, in the
  same frame — `the-frame`.
- The post-effect chain is chosen by the **camera entity's type** (creeper,
  spider, enderman), not by an option — `the-frame`.
- **The dirty halo is 27 block positions, not 27 sections** — one section for
  any block off a boundary, at most eight on one. Only the mesher's *read*
  region is 27 — `level-rendering`.
- The section-mesh result **does** come back through the client thread as a
  callback, fired from `SectionRenderDispatcher.uploadTerrainBuffersToGpu`;
  and `SectionOcclusionGraph`'s full BFS is the *second* thing on
  `Util.backgroundExecutor` — `level-rendering`.
- A layer's terrain geometry lives in a growing **list** of 128 MiB heaps
  sub-allocated by a `TlsfAllocator`, not one buffer — `level-rendering`.
- `CardinalLighting` is **two hard-coded records**; the dimension only picks
  between them — `level-rendering`.
- **A quad's chunk layer is read out of the sprite's pixels** at bake time —
  `FaceBakery` asks what transparency exists inside that quad's UV rectangle
  — `models-and-atlases`.
- `Minecraft.selfTest` **only runs in a development environment**, and throws
  rather than warns — `models-and-atlases`.
- **`RenderSystem.assertOnRenderThread` is called from `RenderSystem` itself**,
  on current API (`setProjectionMatrix`, `getModelViewStack`,
  `getSequentialBuffer`). It is `GpuDevice`/`CommandEncoder`/`RenderPass` that
  assert nothing — `blaze3d`.
- There is **one fog UBO per frame**, handed to four passes; the clouds pass
  gets none. The sky and cloud fog ends are fields inside that one block —
  `lightmap-fog-and-sky`.
- `ClientLevel`'s two extra attribute layers are the **lightning** flash, not
  the End's; `EndFlashState` is a free-running 600-tick End-sky flash and has
  nothing to do with the dragon fight — `lightmap-fog-and-sky`,
  `environment-attributes-and-timelines`.
- `EnvironmentAttributes.SKY_LIGHT_FACTOR` (visual) and
  `EnvironmentAttributes.SKY_LIGHT_LEVEL` (gameplay) are **two tracks**, at
  different times and different night values — `lightmap-fog-and-sky`.
- **Explosion particles are not particle packets.** `ClientboundExplodePacket`
  carries a weighted `ExplosionParticleInfo` list and `ClientExplosionTracker`
  generates them client-side, budgeted per tick and cleared entirely unless
  the particle setting is *All* — `particles`.
- The break puff walks the **outline** shape, not the collision shape — a
  torch has no collision shape and still puffs — `particles`.
- The override-limiter flag skips the *client* distance check and **widens**
  the server's from 32 to 512 — it does not skip it — `particles`.
- The handshake and login state machines run **entirely on the Netty
  thread**; the first `PacketUtils.ensureRunningOnSameThread` is in the
  configuration phase. "Netty never runs game logic" is a *play*-phase
  rule — `anatomy`.
- `MinecraftServer.haveTime` gates only chunk **unloading**, eager chunk
  saving and section-storage flushing. Chunk loading and generation are
  never gated by it, and sprinting polls chunk sources *more*, not less —
  `anatomy`.
- Most world sounds are **level events**, not sound packets: the client
  picks the `SoundEvent` from an int. A block break takes that path, so it
  never touches `Level.playSound` — `sound`.
- Music, ambient loops, additions and mood are `EnvironmentAttributes`
  now; `BiomeSpecialEffects` is block tint only — `sound` (confirms
  `biomes` and `lightmap-fog-and-sky`).
- The **last** pack in the selected list wins, and vanilla sits at index 0
  (`Pack.Position.BOTTOM`). "Higher in the UI" means "later in the list" —
  `resource-system`.
- A reload snapshots the **pack list**, not the bytes; files are still
  opened lazily at read time — `resource-system`.
- The atlas → model dependency is a **prepare**-phase dependency through
  `PreparableReloadListener.SharedState` (`AtlasManager.PENDING_STITCH`),
  not an apply-order one — `resource-system`.
- Numeric ids come from two places: source order for `BuiltInRegistries`,
  **sorted element ids** for a dynamic registry. That is why the client can
  rebuild the same ids — `identifiers-and-registries`.
- `Registries.DIMENSION` and `Registries.LEVEL_STEM` are literally the same
  interned `ResourceKey` object — `identifiers-and-registries`.
- Between bootstrap and world load a tag read returns **empty/false**, not
  a throw; the throwing window is during `BuiltInRegistries.bootStrap`
  itself — `tags`.
- A tag whose entries fail is dropped **whole**, and on a static registry
  the *required* flag is ignored entirely — `tags`.
- Item prototypes bind at **reload**; the throw is on
  `Holder.Reference.components`, and `Holder.areComponentsBound` is the
  guard. On a multiplayer client only networkable registries get bound —
  `data-components`.
- `ItemStack.validateStrict` reaches **one** level into containers and does
  not re-run itself there; the damageable-and-stackable rule is a
  *prototype-build-time* validator, a different check at a different time —
  `data-components`.
- `BlockPos.asLong`'s 12 Y bits give −2048…2047, but `DimensionType`
  reserves a 32-block margin: the real limits are −2032 and 2031 —
  `math-and-primitives`.
- `Level.random` deliberately **crashes** on cross-thread use
  (`ThreadingDetector`); it is a detector, not a safe generator —
  `math-and-primitives`.
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

- **The `ServerPlayer` is constructed *after* the client acknowledges the
  end of configuration**, not during the task that bears its name.
  `PrepareSpawnTask` resolves a spawn and tickets its chunks; the object is
  built by `PrepareSpawnTask.spawnPlayer`, called from
  `ServerConfigurationPacketListenerImpl.handleConfigurationFinished`, by
  which point the server's *outbound* protocol is already PLAY (the inbound
  one is swapped later still, in `PlayerList.placeNewPlayer`).
  `players-and-sessions` had this right; `protocol-phases` had it backwards
  and is fixed (**session G**).
- **`TickablePacketListener` is the only route to a game thread that is not
  a packet.** `Connection.tick` calls it; five classes implement it; it is
  what runs the whole server login state machine and every keep-alive.
  Nothing outside `the-connection` explained how a listener with no
  hopping handlers still gets server-thread time (**session G**) —
  `the-connection` / `protocol-phases`.
- **The client drains packets once per *frame*, before that frame's ticks**
  — `Minecraft.runTick`, which may then run zero ticks or ten.
  `the-frame` had this right and `what-the-client-is-told` had it exactly
  backwards (**session G**).
- **`ServerEntity.sendChanges` is reached on three conditions and gates on
  three more**, and the call counter advances outside the gate — so
  `ServerEntity.FORCED_POS_UPDATE_PERIOD` counts calls while
  `ServerEntity.teleportDelay` counts gated ones (**session G**) —
  `what-the-client-is-told`, agreeing with `synched-entity-data`.
- **Seven packets override `Packet.isTerminal`, not eight.**
  `ServerboundResourcePackPacket.Action.isTerminal` is a namesake about
  resource-pack responses and has nothing to do with the phase machine
  (**session G**) — `packets-and-stream-codecs`.
- **Two of five `SignedMessageChain.DecodeException` reasons break the
  chain**, not most of them: out-of-order and invalid-signature. A missing
  or expired profile key rejects one message and poisons nothing
  (**session G**) — `chat-and-signing`.

## Catalogue gaps found during pass 1

Both items below now have a decision in [plan.md](plan.md): the
environment-attributes page is approved (pass-2 session C), and the
under-coverage of rendering is answered by splitting Part X into a
client part and a rendering part (sessions H–I), with new pages for the
lectures pass 1 found hiding inside pages (the text/font engine, the
frame graph). The appendix's remaining gaps (the debug cluster,
`client/resources`, `util/parsing`, `client/animation`, Blaze3D's
Vulkan/platform halves) get their rulings in session K.

- ~~**Environment attributes and timelines have no page**~~ — **written
  in session C** as `src/systems/world/environment-attributes-and-timelines.md`,
  last in Part IV. The borrowed explanations were cut out of `biomes` and
  `lightmap-fog-and-sky` and replaced with pointers; `block-ticks-and-fluids`,
  `level-data-and-rules` and `game-events-and-poi` now link to it for the
  mechanism rather than restating it. The original entry, for the record:

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

## The client's remaining gaps *(session H's inventory)*

Session H measured `net/minecraft/client/` at **1,864 classes / 172,711
lines** and `com/mojang/blaze3d/` at **211 / 26,111**, and mapped every
package to a page. One rule worth keeping: **`server-classes.txt` contains
zero entries under `net/minecraft/client/` or `com/mojang/blaze3d/`** — the
client packages are client-only without exception, so the corpus can state
that as a rule rather than checking case by case. A spot-check of the
forty-five most-cited class names on the client pages found no
mis-attribution in either direction.

What is left with no owner, in priority order:

- **`client/gui/screens` — 224 classes / 33,521 lines, the largest unmapped
  block in the corpus.** `gui-and-screens` explains the *machinery*
  (lifecycle, widgets, layout, focus) and nothing explains the *catalogue*:
  world selection (20/4,474), the container screens beyond
  `AbstractContainerScreen` (49/7,552), the recipe book (13/1,968), options
  (22/2,009), social/report/friends/multiplayer/packs (40/6,845).
  Recommendation: **absorb** as a one-paragraph taxonomy naming the families
  and their entry points. Do not write per-screen pages.
- ~~**`blaze3d/platform`**~~ — **session I: written as a page,
  `systems/rendering/the-window.md`.** Session H's count (29 / 3,896) was
  close; the real figure is 25 classes plus 2 under `platform/cursor`, 3,843
  lines. It was not absorbed because three pages in two parts all began after
  it and none could explain it without a digression. **`ScreenManager` does
  not exist in 26.2 and never did** — that name was carried in from older
  notes; the monitor side is `MonitorManager` / `Monitor` / `VideoMode`.
- **`client/multiplayer` tail (~15 classes)** — `ServerData`, `ServerList`
  and the address resolver, `LevelLoadTracker` and the receiving-level
  screen, `TransferState`, `SessionSearchTrees`, `CacheSlot`,
  `PingDebugMonitor`. "How the client joins a server" is a real lecture and
  the corpus covers the protocol but not the client's session.
  Recommendation: **absorb** into `the-client-level`, or a short
  *joining a server* page if session K disagrees.
- **`client/server` (6 / 838)** — `IntegratedServer` is named on six pages;
  `IntegratedServerLoader`, `IntegratedPlayerList` and the three LAN classes
  are named nowhere. "Singleplayer is a server" is a claim the corpus makes
  repeatedly and never walks. Recommendation: **absorb** into
  `server-lifecycle` (Part III), which already owns the server's two ends.
- **`client/resources` strays (~6)** — `SkinManager` and
  `DefaultPlayerSkin` (genuinely interesting: they feed entity rendering),
  `MapTextureManager`, `WaypointStyleManager`, `IndexedAssetSource`.
  Recommendation: skins into `entity-rendering`, the rest a sentence each in
  `resource-system`.
- **Small and self-contained:** `client/searchtree` (8/505 — the suffix
  array behind creative and recipe-book search), `client/gui/narration`
  (7/235), `client/gui/components/toasts` (9/1,180),
  `client/gui/contextualbar` (5/237) and `client/waypoints` (2/44) — the
  last two are a real hole in `hud`, which session H closed by naming them.
  Recommendation: absorb, one paragraph each.
- **Decline explicitly** (session K): `client/data*` (28 / 6,176 — build-time
  model generators, the same category as `net/minecraft/data`, and big enough
  that a reader will trip over it), `client/quickplay` (3/284),
  `client/profiling` (2/81), `client/renderer/gizmos` (2/91), the ~230
  per-mob classes under `client/model/*`, and the interiors of
  `blaze3d/opengl` and `blaze3d/vulkan`.

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
- **JDK class names in backticks fail** the same way keywords do: `Math`
  was session A's only miss. Say "the JDK's sine", not `Math.sin`.
- Session H's four misses were the same three shapes as every previous
  session and one new one: an unqualified member (`doAddParticle`,
  `handlePlayerAction`), a JDK type (`AutoCloseable`), a **bare English word
  in backticks used as a value** (`false`, in "reports `false` for"), and a
  member cited on the wrong class — `Level.getUncachedNoiseBiome`, which is
  declared on `LevelReader`. The last one is the interesting one: it is the
  declaring-class trap that the protocol says only a fact-check agent can
  catch, and here the *verifier* caught it, because `Level` genuinely does
  not contain the token. **The verifier catches the wrong-class citation
  whenever the cited class's file does not happen to mention the member —
  which is most of the time for an interface method.** It is the citations
  to *superclasses whose files do mention the name* that stay invisible.
- Session A's four failures were all *unqualified members* written mid
  sentence — `managedBlock`, `tickChildren`, `prepareSharedState` — plus
  two names being introduced as **gone** (*initGameThread*,
  *isOnGameThread*) that wanted italics. Same two traps as every previous
  session; the fix is mechanical, so run the verifier before reading back
  rather than after.
- The verifier proves a name **exists**, not that it is declared where you
  cite it — see the hand-off section below.
- **A method *parameter* name in backticks is a new trap shape** (session D):
  `ExperimentalRedstoneWireEvaluator.shapeUpdateWiresAroundInitialPosition`
  looked like a field and is an argument of
  `ExperimentalRedstoneWireEvaluator.updatePowerStrength`. Same rule as
  config keys and JSON keys — if it is not a declared `Class` or
  `Class.member`, say it in prose. Session D's other three failures were the
  familiar ones: two **bare members** (`initCache`, `saveWithoutMetadata`)
  written mid-sentence, and one member cited on the subclass
  (`Player.swing`, declared on `LivingEntity`) — the verifier caught that
  last one only because `Player.java` happens not to contain the token, so
  do not rely on it.
- **The verifier could not see record components on a generic record.**
  Session C found and fixed a real bug in `tools/verify_names.py`: the
  `RECORD` regex required `record Name(` and so missed `record Name<T>(`,
  which is why `AttributeType.valueCodec` and its four `LerpFunction`
  siblings failed. Same class of bug as session A's `gen_reference.py`
  component regex. **When a name you are certain about fails, suspect the
  tool once before rewording the page.**
- Session C's other failures were the usual two shapes and were caught by
  running the verifier after every page rather than at the end. Doing it per
  page also localises a regex bug like the one above.
- Session B's failures were the same two shapes yet again: **bare members**
  (`shouldRun`, `player`) and **file/JSON key names in backticks**
  (*bypassesPlayerLimit*, *singleplayer_uuid*). A key in a config or save file
  is not an identifier — italicise it. Also `BlockableEventLoop.runningTask`
  is declared on `ReentrantBlockableEventLoop`; the verifier accepted it
  because the base class file mentions the token.

- **A helper type you assume is nested may be top-level** (session E):
  `PostSpawnProcessor` is used inside `EntityType` and reads like
  `EntityType.PostSpawnProcessor`, but it is its own file in `world/entity`.
  When a name fails and you are sure it exists, check whether you invented
  the enclosing class.
- Session E's other four failures were the usual bare members written mid
  sentence — *noPhysics*, *equals*, *hashCode*, *define* — plus `super` used
  as a noun. Say "the superclass hook", not `super`.

- **The generated reference can be wrong, and prose that quotes it
  launders the error** (session G). `packets-and-stream-codecs` said "225
  packet types" because `tools/gen_reference.py` matched `PacketType<(\w+)>`
  and `\w` does not match a dot, so the seven nested types
  (`ClientboundMoveEntityPacket.Pos` and its siblings,
  `ServerboundMovePlayerPacket.Pos` and its three) were silently dropped.
  The true count is **232**. This is the third generator/verifier regex bug
  found by a pass-2 session — session A in `gen_reference.py`, session C in
  `verify_names.py`, session G in `gen_reference.py` again — and the first
  where the bad number had been copied into a page. **Any number a page
  takes from a tool gets re-derived by hand once.**
- Session G's only two verifier failures were JDK names in backticks
  (`AutoCloseable`, `Exception`) and two bare members written mid sentence.
  Same two shapes as every session since A.

## Hand-off to passes 3–5

Pass-2 sessions append here whatever they leave for later: wording debt
for pass 4, and material added speculatively that pass 4 may cut.
**Structural observations now go to [pass3.md](pass3.md)** — the
restructuring notebook opened in session A — so that pass 3 starts with
evidence rather than a blank page.

### Session D (Part V Blocks)

**Added on spec — pass 4 should weigh these:**

- `redstone` gained a whole new section, *The diodes, and the one block
  that is not on this channel* (~55 lines): `DiodeBlock`'s input/side/output
  model, the repeater's `RepeaterBlock.LOCKED`-as-a-shape-update, the
  comparator's block entity and its reach-through-a-conductor input
  (including the single `ItemFrame`), the container fullness formula, and
  the observer. This was a real catalogue gap — the page previously named
  `DiodeBlock.checkTickOnNeighbor` and nothing else while claiming to cover
  redstone — so it should survive, but it is the largest single addition of
  the session and it pushes the page to ~520 lines. If pass 3 splits the
  page three ways ([pass3.md](pass3.md) §2) this section becomes its own
  lecture and the length problem goes away by itself.
- `block-breaking` gained the deferred-destroy consequences (ABORT does not
  cancel it; the delayed path re-checks nothing), the two anti-desync paths,
  and the two-independent-scans rule for `Tool`. The anti-desync bullet is
  the most cuttable — it is a debug-string-level detail — but it is also the
  only place the corpus explains what happens when the two clocks disagree.
- `block-entities` gained the simulation-distance and freeze gates on
  ticking. Load-bearing and player-visible; keep.
- `blocks-and-states` gained the property-identity-versus-equality trap and
  the `Block.getId` → air degradation. Both are "surprise" material rather
  than trace material; if pass 4 needs to cut, they are the candidates.

**Wording debt:**

- Three pages now say some version of "shape updates run on both sides,
  neighbour updates are server-only, and here is the exception". Pass 4
  should pick one page to own the sentence and have the others point at it —
  most likely `block-interaction`, which already has the cleanest statement.
- `blocks-and-states` step 7 has grown into a single paragraph walking the
  whole tail of `Level.setBlock` and is now hard to read as prose. It wants
  to be a list, or the flowchart [pass3.md](pass3.md) §3 asks for.
- "The one sentence a player recognises" in `block-breaking` had a factual
  error in it (1.5 *seconds*, which is the hardness, not the time). Worth a
  pass-4 sweep of those sentences specifically — they are the least-checked
  line on every page because they read as flavour.

**Naming drift:** none new. Session D checked every *gone* name its five
pages assert — *ItemInteractionResult*, *DirectionProperty*,
*markAndNotifyBlock*, *onRemove*, *rebuildCache*, *saveToItem*,
*doTileDrops*, *dropsLike*, *BlockModelShaper* — and all are already in the
table below and in `appendix/naming-drift`. Part V's renames were caught in
pass 1 (sessions 4–5) and have held up.

**Not done, deliberately:**

- The `redstone` and `blocks-and-states` splits, and the
  interaction/breaking merge question — all presentational, all in
  [pass3.md](pass3.md).
- `redstone`'s remaining completeness gaps, which are real but are
  circuit-building detail rather than mechanism: `RedStoneWireBlock`'s
  corner-update fan-out (`updateNeighborsOfNeighboringWires`,
  `checkCornerChangeAt`), the dot/cross connection rules, the redstone
  torch's own toggle path beyond burnout, and the long tail of piston
  special cases (slime reordering, the sticky-retract interrupt,
  `MovingPistonBlock.destroy`, the moving hitbox). Listed here so a later
  session can decide rather than rediscover.

### Session C (Part IV The world + the new environment page)

**Added on spec.** The new page is 300 lines and entirely on spec — it was
approved, but pass 4 should check two things: the 48-attribute census
(counts by namespace, syncable, spatially interpolated) is reference
material inside a lecture page and may want to move to
`src/reference/`; and the *Interfaces* bullet listing ~25 consumer classes
is a wall of names that earns its place only if the reader is meant to
grasp how wide the system reaches. One or the other should probably go.

The eight fact-checked pages grew by roughly 15% — much less than session
A's 40%, because most of session C's work was correction rather than
addition. Specific additions pass 4 should weigh:

- `block-ticks-and-fluids` gained the `TickAccess` interface-layer bullet.
  It is true and it explains why the client and worldgen can substitute
  no-ops, but it is five interface names in a row with no trace.
- `tickets-and-loading` gained five invariants at once. The
  natural-spawn-radius one and the keep-dimension-active one are load-bearing;
  the singleplayer batch-quota one is a footnote.
- `chunk-anatomy` gained `LevelChunkSection.maybeHas` and the
  client-counters-are-zero invariant. Both are good; the palette one is the
  better of the two and could carry the other.
- `chunk-generation-pipeline`'s dependency table grew from six rows to nine
  because the six were wrong. It is now correct and less readable. Pass 3's
  "draw the pyramid" note (§3) would fix this properly.

**Wording debt for pass 4.**

- The same register problem session A flagged, worse here: session C's
  fixes are full of "not X but Y" and "except that", because a great many of
  them were corrections to over-confident claims. `chunk-storage`'s
  invariant list in particular now reads as a series of retractions.
- Three pages now say some variant of "*and it is not what you think*"
  about a thread. Pick one.
- `game-events-and-poi` and `block-ticks-and-fluids` both now carry a
  parenthetical aside longer than the sentence containing it.
- The em-dash density in the new page is high even by this corpus's
  standards.

**Left for later, deliberately.**

- The two Part IV splits (`block-ticks-and-fluids`,
  `game-events-and-poi`) — recorded in [pass3.md](pass3.md) §2.
- The completeness findings session C did **not** act on, in rough order of
  how much they would add: `chunk-storage`'s `IOWorker.isOldChunkAround`
  blending cache (a genuinely separate second job of the chunk lane, and a
  page-sized omission); `game-events-and-poi`'s sculk-shrieker → warden
  chain and the calibrated sensor's frequency filter; `lighting`'s
  `BlockLightSectionStorage` and the `SkyLightSectionStorage.topSections`
  map; `tickets-and-loading`'s `ChunkMap.getChunkRangeFuture` bail-out;
  `chunk-anatomy`'s `LevelChunk.setBlockState` re-entrancy guard and the
  three flag gates it does not name. Any of these is a fair pass-4 or
  pass-5 addition; none of them makes a current claim false.

### Session A (Part I · `sound` · Part II Foundations)

**Added on spec, and pass 4 should look hard at it.** Pass 2's charter
says add freely, and session A grew eight pages by roughly 40%. The
candidates for cutting:

- `anatomy`'s *situational threads* paragraph. It is a list of a dozen
  thread names no lecture depends on. It exists so the threads table can
  honestly claim to be "the set worth memorising, not the set that
  exists" — but it may be a footnote, not prose.
- `sound`'s music-and-ambience section duplicates framing that
  `environment-attributes-and-timelines` (session C) will own. Once that
  page exists, this should shrink to a pointer plus the sound-specific
  attributes.
- `codecs-nbt-json` now traces **four** serialisations of one `ItemStack`
  rather than three. The fourth (`HashOps`) is genuinely the best
  illustration of "one codec, many formats", but the click protocol
  belongs to `containers-and-menus`; check for overlap when Part VII is
  fact-checked (session F).
- `math-and-primitives` gained colour types, `RandomSequences`,
  `MarsagliaPolarGaussian` and the shape cache. It is now a reference
  page pretending to be a lecture — see [pass3.md](pass3.md).
- `resource-system`'s pack-format numbers (resource 88.0, data 107.1, the
  64/81 cutoffs) are the most version-fragile paragraph in the corpus.
  Flag it for the 26.3 re-verification sweep.

**Wording debt for pass 4.**

- Three pages now open a section with "There are two X and they are not
  the same shape" or a close variant. Pick one and vary the others.
- `anatomy` and `threads.md` state the thread table twice, deliberately.
  Pass 4 should check they have not drifted again — they had, before
  session A.
- The corrected claims tend to read as corrections ("not X but Y", "the
  page is wrong to say"). That register is right for a fact-check and
  wrong for a lecture. Pass 4 should restate them positively.

**A verifier gap worth knowing.** `verify_names.py` matches a token
anywhere in the named class's file, so a member *called* in class A but
*declared* on class B still passes. Two session-A citations were wrong
that way and only the fact-check caught them
(*NetworkRegistryLoadTask.findAndLoadFromResource*, actually on
`RegistryLoadTask.PendingRegistration`; *ChannelAccess.execute*, actually
on `ChannelAccess.ChannelHandle`). The verifier cannot be tightened
cheaply — but a fact-check agent should always be asked for a NAMES
section, as session A's were.

### Session B (Part III · The server)

**Added on spec, and pass 4 should look hard at it.** The four pages grew
from 1,203 lines to about 1,580 — roughly 30 %, in line with session A. The
candidates for cutting:

- `server-tick`'s new step 10 (the crash path and `BlockableEventLoop.delayCrash`)
  duplicates framing `server-lifecycle` owns. It is here because the tick
  loop's *finally* is genuinely part of the loop, but if the "how a server
  dies" lecture in [pass3.md](pass3.md) happens, this shrinks to a pointer.
- `server-tick`'s `SampleLogger` / `TpsDebugDimensions` paragraph is now
  three sentences about a debug feed nothing else in the corpus uses. It is
  correct and it earned its place by replacing a *wrong* claim ("the F3
  charts read these"), but it is a candidate.
- `server-level-tick`'s guard bookkeeping — which steps are behind
  `runsNormally`, `emptyTime`, `isDebug` — is now spread across six of the
  thirteen narrated steps. Pass 3's proposed guard flowchart would let pass 4
  cut most of that prose.
- `players-and-sessions` gained the permission model, `NameAndId`,
  `IntegratedPlayerList`, `ServerPlayerGameMode` and `switchToConfig`. The
  permission paragraph is the one to watch: Part XIII's
  `brigadier-and-commands` owns that model and session K should check the two
  have not drifted.
- `server-lifecycle` gained the two-failure-paths material, the
  `server.properties`-is-writable invariant and the `SystemReport` bullet.
  All three are genuinely new coverage rather than expansion.

**Wording debt for pass 4.**

- Session A flagged that corrected claims "read as corrections". Session B
  made it worse: the four pages now contain roughly a dozen constructions of
  the form "not X but Y", "two, not one", "and there is no Z". It is the
  right register for a fact-check and the wrong one for a lecture, and Part
  III is now the worst offender in the corpus. Pass 4 should restate all of
  them positively.
- Three Part III pages open a bullet with "Two …" (*Two player lists*, *Two
  `ServerLevel` tick counters*, *Two chunk sets*). Vary them.
- `server-lifecycle`'s startup section is a numbered list inside a page whose
  other trace is a diagram. It reads as an appendix to its own page.

**Cross-page corrections made outside Part III.** The "one flush per client
per tick" claim was wrong in three places; session B fixed
`anatomy` and `the-connection` alongside `server-tick`. `the-connection` was
self-contradictory — it already said `Connection.tick` flushes
unconditionally and then concluded "one flush". Worth a pass-4 sweep for
other bullets that state a mechanism and then draw the opposite conclusion.

---

### Session E — Part VI Entities

**Material added on spec (pass 4 may cut).**

- `movement-and-collision` gained a whole new subsection, *Who is allowed to
  simulate*, before the trace. It is not padding — three of the page's errors
  followed from its absence — but it is a second opening and it makes an
  already-long page longer. If pass 3 gives the authority matrix its own home
  (see the split table), most of this becomes a pointer.
- `attributes` gained the tick-phase paragraph explaining why the send is a
  tick behind. This is the third page in the corpus to explain the same
  chunkSource-before-entities ordering from scratch (`block-entities` and
  `server-level-tick` are the others). Pass 4 should pick one owner and have
  the other two point at it.
- `entity-lifecycle` step 5 grew a nether-fortress aside and a
  reduced-water-ambient aside that are both one-line curiosities.
- `synched-entity-data`'s serializer catalogue is now a 43-entry ordered list
  with ids. It is reference data in the middle of a lecture page and it is
  the obvious candidate for `src/reference/`.
- `ai-goals-and-brains` gained four new invariants (control flags, the
  sentinel goal, brain rebuild on profession change, activity-switch memory
  erasure). All are real mechanisms; the page now has fifteen bullets under
  *invariants and surprises*, which is too many to say out loud.
- `damage-and-death` gained the non-living-`hurtServer` bullet, which is
  really a pointer to coverage that does not exist. See the gap below.

**Wording debt for pass 4.**

- The "not X but Y" register session B complained about is now worse in Part
  VI than in Part III, because session E's corrections were mostly *inversions*
  rather than adjustments: "it does not become a pig", "only one side runs the
  physics", "the client never calls `Entity.move`", "`hurtArmor` is empty",
  "the fence is 1.5 to stand on". Every one of those is currently phrased
  against the wrong belief it replaces. Restate positively.
- Three Part VI pages now say some version of "the gate is X, not Y". Vary.
- `movement-and-collision` and `entity-anatomy` both now carry a
  cross-reference to the other about what the client's tick does and does not
  do. One of them should own it.

**A catalogue gap, found and *not* filled.** `damage-and-death` covers
`LivingEntity` and stops. About thirty classes override `Entity.hurtServer`
directly — `ArmorStand`, `VehicleEntity`, `ItemFrame`, `EndCrystal`,
`FallingBlockEntity`, `PrimedTnt`, `Display`, `Interaction` — with their own
rules, and the armour-stand damage-type tags the page lists exist *only* for
that code. Session E added a bullet naming the gap rather than writing the
section, because the page is already the part's longest trace and the material
is a data table more than a lecture. Pass 3 should decide whether it is a
section, a sibling page, or an appendix table.

**Cross-page corrections made outside Part VI.** Part IX's
`what-the-client-is-told` said "the client interpolates and then simulates",
which reads as the claim session E disproved; its heading and first sentence
were corrected and it now points at `movement-and-collision`. Session G should
check the rest of that page against the authority matrix — in particular
anything it says about client-side entity movement.

---

### Session F — Part VII Items · Part VIII The player

**Added on spec, and pass 4 should look hard at it.** Nine pages, roughly
+35 % in total.

- `items-and-stacks` gained a whole **durability** subsection. It is a
  genuine catalogue gap — the page's scope is the `ItemStack` data model
  and half of that model was missing — but it is not part of the eating
  trace and pass 4 should check it earns its place rather than becoming a
  reference block.
- `enchantments` gained ten `EnchantmentHelper` entry points (including
  Fortune and Looting, which were absent from a page about enchantments),
  a fourth acquisition path, and the exclusivity mechanism. The hook table
  is now the largest single artefact in Part VII. It is the right shape;
  it may be the wrong length.
- `containers-and-menus` gained the creative-mode parallel protocol, the
  crafting-result side channel, the drag protocol's real packet count and
  the data-slot truncation. The creative material is new coverage; the
  rest is correction.
- `input-to-movement` and `player-anatomy` both gained an **authority**
  section. This is deliberate duplication pending pass 3's ruling — see
  [pass3.md](pass3.md) — and one of the two should be cut to a pointer
  once the owner is chosen.
- `the-sword-swing`'s ordered list grew from eleven steps to fourteen. Two
  of the three additions are real gates that change the arithmetic; the
  third (`Player.cannotAttack`) is completeness.
- `recipes` gained `ClientRecipeContainer`, `RecipeBookMenu`, the
  non-shaped crafting serializers and the five `RecipeDisplay`s. The
  serializer paragraph is the one to watch — it is a catalogue inside a
  trace page.

**Wording debt for pass 4.**

- Session F inherited the A–E problem and added to it: these nine pages
  now contain a large number of "not X but Y", "three, not two", "and it
  is not what the name suggests" constructions. Part VIII is now as bad as
  Part III. Restate positively.
- Three pages open a bullet with "There are two/three …" and two more use
  "the interesting one is". Vary.
- `loot-tables`'s invariant list has grown to fourteen bullets and reads
  as a checklist rather than prose.
- The em-dash density in `containers-and-menus`'s new *When it runs*
  section is high enough to hurt.

**Cross-page corrections made outside Parts VII–VIII.**

- `appendix/naming-drift` had a **wrong row**: *Ingredient.EMPTY* → "an
  `Ingredient` cannot be empty". A tag that resolves to nothing yields a
  legally empty ingredient, which is why `Ingredient.isEmpty` exists.
  Fixed in both this file's table and the page.
- `entity-anatomy` gained one clause naming `ClientMannequin` and the
  swapped `Mannequin.constructor` factory, because its `AvatarRenderer`
  sentence was true but incomplete and session F needed the mechanism for
  `player-anatomy`.
- Checked and found **already correct**: `damage-and-death`'s
  `Entity.hurtClient` account (session E got this right), the
  `HashOps` description in `codecs-nbt-json`, and every
  `Entity.invulnerableTime` attribution outside `the-sword-swing`.
- **Not fixed, flagged:** `HashedStack`'s shape is now described on five
  pages — `containers-and-menus`, `codecs-nbt-json`, `data-components`,
  `packets-and-stream-codecs` and, in passing, `block-entities`. Session F
  gave `containers-and-menus` the *use* and left the *production* to
  `codecs-nbt-json`, but `data-components` still restates both almost
  verbatim. Pass 4 should cut three of the five.

**Verifier lessons.** Two bare words slipped through as identifiers
(`true` used as a value, `doTick` unqualified) and one member was
attributed to the wrong class in a way the verifier cannot see
(`Entity.jumpFromGround` is `LivingEntity.jumpFromGround`). The session-E
habit of running the verifier after each page rather than at the end held
up. The fact-check agents found four more mis-attributions the verifier
passed — `LivingEntity.moveRelative`, `ServerPlayer.move`,
`ServerPlayer.absSnapTo` and `Minecraft.execute` were all declared on
`Entity` or `BlockableEventLoop` — which is now five sessions running that
the **NAMES section has caught something `verify_names.py` structurally
cannot**. It is the single highest-value part of the fact-check brief.

### Session G — Part IX Networking

**Added on spec, and pass 4 should look hard at it.** Five pages,
1,780 → 2,367 lines (+33 %).

- `the-connection` gained a whole **"How a connection dies"** section
  (`Connection.exceptionCaught`'s four outcomes) and a **"Sending"**
  section (the outbound event-loop hop, `PacketSendListener`). Both are
  genuine gaps — the page opened by promising the reader the "Timed out"
  message and never explained where it comes from — but the sending
  section is short and might fold into *When it runs*.
- `protocol-phases` gained the handshake phase's real gates (version
  check, transfer and status refusals) and a short **status** section. The
  status phase had been a table row on a page about logging in; it is two
  packets and a hang-up, and it now says so.
- `what-the-client-is-told` gained **"The rest of the push"** (time,
  weather, level events, view distances, the debug feed) and **"What the
  client does on receipt"**. The first is a list and reads like one; pass 4
  should decide whether it is a section or a table.
- `packets-and-stream-codecs` gained `ByteBufCodecs.readCount` (the count
  check that matters more than the famous allocation clamp),
  `ProtocolInfoBuilder`'s four entry points, and `PacketReport`. The
  security bullet is now three defences in one paragraph and may want
  splitting.
- `chat-and-signing` gained four invariants (message and key expiry, the
  client's own `ChatAbilities` / `ChatRestriction` gating layer, the
  receiving client's error path, and the session-update failure modes).
  The invariant list is now sixteen bullets — the same complaint session F
  logged against `loot-tables`.

**Wording debt for pass 4.**

- Part IX now has the "not X but Y" problem badly. `the-connection` alone
  has *conditional, not the default*, *containment, not recovery*, *not
  untouched*, *in the middle, not at the end*, *two flushes, not one*.
  Five pages of corrections read as five pages of arguing with a reader
  who is not there. Restate positively.
- Three of the five pages now open a paragraph with **"Two of the five"**
  or **"three conjuncts, not two"**. The counting habit that made the
  session accurate has made the prose repetitive.
- `what-the-client-is-told` is 553 lines and the longest page in the
  corpus.

**Cross-page corrections made outside Part IX.**

- `server-tick`'s second-flush bullet said `resumeFlushing` "carries only
  the chunk batch". Corrected to name everything `tickChildren` does after
  `MinecraftServer.tickConnection`. The load-bearing entry above is
  narrowed to match.
- `tools/gen_reference.py`'s packet regex fixed, and `src/reference/packets.md`
  regenerated (225 → 232; the game group goes 124/57 → 127/61).
- Checked and found **already correct**, which is the session's most
  reassuring result: `the-frame`'s per-frame packet drain,
  `synched-entity-data`'s three-way `ServerEntity.sendChanges` gate,
  `block-entities`' empty-`BlockEntity.getUpdateTag` default,
  `players-and-sessions`' entire join trace (including the
  spawn-after-acknowledgement ordering that `protocol-phases` had wrong),
  and `anatomy`'s "the first thread hop is in the configuration phase".
  Where Part IX disagreed with another part, **Part IX was the wrong
  one every time** — which is an argument for watching the parts that
  were written earliest.
- No new rows for `appendix/naming-drift`: session 9's networking rows
  were re-read against the decompile and are all still right.

### Session H — Part X The client (and the X/XI split)

**What the session did.** Eight fact-check agents: `the-frame`,
`ClientLevel`, the prediction ledger (cross-checked against `block-breaking`,
`block-interaction` and `what-the-client-is-told`), input/options, screens,
the text engine, `hud`, and one full `net/minecraft/client/**` coverage
inventory, plus a ninth agent to research the debug subscription pipeline
once the inventory found it. Part X's eleven pages became **eleven client
pages plus a seven-page Part XI**; three parts renumbered;
`client-world-and-options` and the old `the-frame` were split four ways and
two ways respectively.

**On-spec additions pass 4 may cut.** Everything here was added because a
fact-check found the page silent about it, not because a lecture demanded it:

- `the-client-loop`'s **starting and stopping** section (the teardown order
  in `Minecraft.close`, the three exits, the out-of-memory ladder) and its
  **tick, in order** section. Both are catalogues; the second earns its place
  because three other parts cite the order, the first may not.
- `the-client-level`'s **chunk-cache torus** and the unload counter-trace.
  The torus is load-bearing for the render-distance story; the unload half is
  symmetry, and symmetry is the first thing to cut.
- `prediction-and-acks`'s **what the ledger does not cover** section. It
  exists because three pages had implied the ledger covers item use and
  movement. If pass 3 moves the page to Part IX, this section is what keeps
  it honest; if not, it could shrink to two sentences.
- `options`'s **listener side-effect** paragraph and the graphics-preset /
  restart-required material. Genuinely new machinery, genuinely dull.
- `hud`'s **contextual-bar priority** paragraph. Four states with an
  asymmetric rule; correct, and possibly more detail than a lecture wants.
- `debugging-the-running-game` in its entirety — a page nobody asked for,
  written because the coverage inventory found ~4,900 lines of undocumented
  pipeline and the page's own trace turned out to be one of the better ones
  in the corpus. If pass 4 disagrees, the sample-logger section is the half
  to cut first: it shares one subscription with the rest and nothing else.
- `text-and-fonts` as a whole is 260 lines about a subject no other page
  needed. It is the clearest single-lecture page in Part X and also the one
  a viewer is least likely to have asked for.

**Wording debt.**

- Three pages now open with "The headline for a 1.21-era reader", four with
  "The one sentence a player would recognise". The formula is doing real work
  and is starting to show. Pass 4 should vary it or commit to it.
- `the-client-loop` and `the-frame` both use "owe, spend, draw, settle" /
  "acquire, snapshot, draw, present" as a four-beat gloss under their
  diagram. Two is a pattern; a third would be a tic.
- `the-gui-render-tree`'s title is the weakest in the part. It is really
  *how the UI is recorded and drawn*, and the tree is the mechanism, not the
  subject.

**Cross-part edits made** (grep the corpus, as session B's rule says):
`block-breaking` (two corrections — the redstone-ore retain, and the
pop-back on a too-early stop), `block-interaction` (the unconditional
"always ends by sending" gated, the ledger bullet cut to a pointer),
`what-the-client-is-told` (the ack claim corrected, the `ClientLevel`
section handed over to Part X as session G recommended), `anatomy` (linked
to the new loop page), `items-and-stacks` (a genuinely broken link to
`../anatomy.md`, pre-existing and unrelated), and the appendix's
naming-drift tables split between Parts X and XI.

**Left for session I.** The old `the-frame`'s render half is now Part XI's
opening page and was rewritten from session H's fact-check, but only its
*wrong* claims were fixed — the missing rendering material the report found
(the non-world tail of `GameRenderer.render`, the cross-frame resource pool,
window and resize handling, the frame graph's relationship to
`FeatureRenderDispatcher`) is session I's. Two of its findings matter
immediately: `LevelRenderer.render` takes eight parameters and none is a
`GameRenderState`, and `GameRenderer.render` is **not** on the pure side of
the extract/render wall — it reads the player's portal and nausea
intensities and the boss overlay's fog question. The wall is real one level
down, at `LevelRenderer`.

### Session I — Part XI Rendering

**What the session did.** Eight agents: one adversarial fact-check per page
(`the-frame`, `blaze3d`, `level-rendering`, `models-and-atlases`,
`entity-rendering`, `lightmap-fog-and-sky`, `particles`) and one mechanical
coverage inventory of the whole rendering tree. All seven pages were
rewritten; one page was added (`the-window`), discharging the ruling session
H deferred. 1,797 lines became 2,430 across eight pages.

**The remaining rendering gaps** *(session I's inventory, for session K's
rulings and pass 3's page plan)*. The tree is **1,187 classes / 97,864
lines**; the corpus names 294 of them, and **58% by line count is named
nowhere**. Coherent systems with no owner, in priority order:

- **Post-processing** — `PostChain` / `PostPass` / `PostChainConfig` /
  `UniformValue`, ~1,000 lines, named on no page. JSON-declared shader chains
  that add passes to the same frame graph. **Recommend a page.**
- **Block-entity rendering** — `renderer/blockentity` + its 26 render states,
  ~3,300 lines; only the dispatcher is named, and the extract/submit
  conversion is undocumented. `renderer/special` (16 classes) belongs with
  it. **Recommend a page.**
- **How an item picks its model** — `renderer/item` + 42 classes under
  `item/properties/**`, the successor to *ItemOverrides*. **Recommend a
  page; decide whether it is Part VII's or Part XI's.**
- **`RenderTypes` / `RenderSetup`** (890 lines) — absorbed into `blaze3d`
  this session as a section, because `blaze3d` already declared
  *RenderStateShard* dead without saying what replaced it. Could grow.
- **`BlockModelLighter`** (462 lines) — smooth lighting and ambient
  occlusion. Named in `level-rendering` this session, not explained.
  **Recommend a section.**
- **`LayerDefinitions`** (582 lines, the largest unnamed non-backend class)
  plus `client/model/geom/builders` — named in `entity-rendering` this
  session, not explained. **Recommend a section.**
- **The uniform ring buffers** — `DynamicUniforms`, `DynamicUniformStorage`,
  `GlobalSettingsUniform`, `ProjectionMatrixBuffer`, ~640 lines. Named in
  `blaze3d` this session. **Section at most.**
- **Smaller and unowned:** `Sheets` (the twelve non-block atlases),
  `MipmapGenerator`, `ItemModelGenerator` + `ItemTransforms`,
  `SkinTextureDownloader` / `PlayerSkinRenderCache`, `WorldBorderRenderer`,
  `CubeMap` / `Panorama`, `MapRenderer`, `TlsfAllocator`, `GlslPreprocessor`,
  `renderer/gizmos`. A paragraph each at most.
- **The 27 debug renderers** (`renderer/debug`, 2,411 lines) — only two are
  named, on `debugging-the-running-game`. **Recommend an enumerated table on
  that page**, not a new page: they are the client end of packets Part IX
  already covers.
- **Decline explicitly** (session K): the ~232 concrete entity models, the
  ~73 concrete particles, the 101 entity render states, the 50 render layers,
  the 16 animation definitions, and the interiors of `blaze3d/opengl` and
  `blaze3d/vulkan` — but name `GlslPreprocessor`, `vulkan/glsl`'s
  shaderc/spirv-cross pair, `TransientMemory` and `GlHeuristics` before
  declining the rest, because all four are shared concerns rather than
  backend detail.

**On-spec additions pass 4 may cut.**

- `the-window` in its entirety. It is a real gap and a real lecture, but it
  is the second page in two sessions written because a *counting* agent found
  a hole, and a viewer has not asked for either.
- `blaze3d`'s **What replaced *RenderStateShard*** and **Resources and
  uniforms** sections. Both are answers to "where did the old thing go",
  which is a naming-drift job, not a lecture's.
- `particles`' **The other way a particle is born** section (explosions). It
  is a genuinely separate mechanism with a budget and a weighted list, and it
  is also a second trace on a page that already has one.
- `models-and-atlases`' twelve-layer soft-failure enumeration. The old page
  said "four separate layers" and was wrong; the honest number is a list, and
  a list is not a lecture. Pass 4 should probably say "a dozen" and name
  three.
- `entity-rendering`'s thirteen-feature-renderer list and fifteen-phase list.
  Both are catalogues; the first earns its place ("what can be drawn in a
  level" has no other answer in the corpus), the second may not.
- `lightmap-fog-and-sky`'s **Not every visual constant is an attribute**
  invariant. It exists to qualify a load-bearing fact three other pages
  state absolutely. If pass 4 restates the fact with the qualifier built in,
  this bullet goes.

**Wording debt.**

- Session H flagged the "acquire, snapshot, draw, present" four-beat gloss as
  a pattern that must not become a tic. Session I did not add a third, but
  `the-window` opens with the same "The headline for a 1.21-era reader"
  formula as the other seven, so Part XI is now **eight for eight**. Pass 4
  should decide whether the formula is the part's voice or its crutch.
- Three pages now say some version of "and that is why *X* looks the way it
  does" as their invariant payoff (the sneaking shadow, the untiled break
  puff, the fade on streaming terrain). It works; three is the limit.
- `level-rendering` is 300 lines and carries the split table's oldest
  deferred seam (meshing vs visibility vs the frame graph). It grew this
  session rather than splitting, because the fact-check's material landed on
  both halves evenly — the same reason sessions D and E gave. Pass 3 now has
  four sessions' worth of "confirmed, not executed" on this shape of page.

**Cross-part edits made** (session B's rule):
`environment-attributes-and-timelines` (Part IV) attributed `ClientLevel`'s
two extra attribute layers to the End flash; they are the **lightning**
flash. Corrected, with a pointer to the End's actual mechanism.
`the-client-loop`'s animated-texture bullet was checked and is right — it is
the *load-bearing-facts list* that was stale, and that is now fixed above.

**Left for session J and later.** Nothing in Part XI is half-done, but three
of this session's findings are other parts' business: the item-model property
system may be Part VII's page; the debug-renderer table is Part X's
`debugging-the-running-game`; and `renderer/special` is the reason a chest in
your hand looks right, which `items-and-stacks` currently does not say.
