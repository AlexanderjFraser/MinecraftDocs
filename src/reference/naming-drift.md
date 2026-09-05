# Naming drift

> Verified against **Minecraft 26.2** · Reference · The translation
> layer: every name a 1.21-era reader will reach for that 26.2 does not have,
> and what it is called now.

Rule three of this corpus is *newest version only*: no page says "in 1.21
this was…", because version-difference prose is the first thing to rot and
the last thing anyone rereads. That rule costs something, and this page is
where the cost is paid back once. Every page assumes you are reading the
26.2 tree; this page assumes you are not, yet, and are still typing the
names you learned somewhere else.

Two audiences. A reader coming from **1.21** — the version most public
writing, most tutorials and most model weights are anchored to — needs the
first table: the old name on the left, what to grep for on the right. A
reader coming from **Yarn** (Fabric's community mappings) needs the last
one: not a version difference at all, just a different name for the same
class in the same version.

The one sentence: *if a name in your head does not appear in the tree, it
is probably on this page.*

## How to read the tables

The left column is **italic, not backticked**. Most of these names do not
exist in 26.2, and `tools/verify_names.py` — which checks every backticked
identifier on every page against the decompile — would reject the page if
they were. Italics is the corpus's mark for *a name, but not a 26.2 name*.
The right column is backticked and therefore verified: those names are in
the tree.

"gone" in the right column means exactly that: there is no replacement
class, the responsibility moved into something structurally different, and
the entry names where it went. Those are the interesting rows — a rename is
a nuisance, a disappearance is a design change, and the page named beside
each part explains it.

Every row here was found the same way: a fact-sheet agent reading the 26.2
decompile went looking for a name it expected and did not find it. The
table is therefore *not* exhaustive — it is exhaustive over the names the
corpus needed. Two hundred and forty-three rows, and the distribution is
itself a finding: the three biggest tables are **commands** (36), **the
server** (31) and **items** (30), and the fourth is **rendering** (27). The
client was rewritten around extract-then-render, which is why almost nothing
at the top of the render stack kept its name — but the permission rewrite and
the game-rule registry moved more names than the renderer did.

## The four you will hit in the first ten minutes

`Identifier` is *ResourceLocation*. `Lightmap` is *LightTexture*.
`DeltaTracker` is *Timer*, and `partialTick` is now a `DeltaTracker.Timer`
you ask rather than a float you are handed. And `Gui` no longer means the
HUD: the HUD is `Hud`, held as `Gui.hud`, while `Gui` is the screen and
overlay manager that also owns `Gui.screen` and `Gui.setScreen` — so a
1.21-era `Minecraft.setScreen` call site is now on `Gui`. Both `Gui` and
`Hud` exist, which is the single most confusing pair of names in the tree.

## The tables


### Everywhere

| the name you remember | 26.2 |
|---|---|
| *ResourceLocation* | `Identifier` |
| *LightTexture* | `Lightmap` |
| *Timer* | `DeltaTracker` |

### Part II — Foundations

| the name you remember | 26.2 |
|---|---|
| *TagManager* | gone |
| *Minecraft.reloadResources* | `Minecraft.reloadResourcePacks` |
| *ItemStack.save* / *parse* | `ValueOutput` / `ItemStack.CODEC` |
| *ChunkPos.asLong* | `ChunkPos.pack` / `ChunkPos.unpack` (a record) |

### Part III — The server

| the name you remember | 26.2 |
|---|---|
| *DO_DAYLIGHT_CYCLE* | `GameRules.ADVANCE_TIME` |
| *DO_MOB_SPAWNING* | `GameRules.SPAWN_MOBS` |
| *DO_WEATHER_CYCLE* | `GameRules.ADVANCE_WEATHER` |
| *GameRules* package | `world/level/gamerules` |
| *GameRules.Key&lt;T&gt;* / *GameRules.Value* / *BooleanValue* / *IntegerValue* / *GameRules.Type* (all nested) | top-level `GameRule`, with `GameRuleType`, `GameRuleTypeVisitor`, `GameRuleMap` for the values and `GameRuleCategory` for the grouping |
| game rules as a hard-coded map | a **registry** — `Registries.GAME_RULE` / `BuiltInRegistries.GAME_RULE`, bootstrapped by `GameRules` |
| *level.dat* field *GameRules*, ids camelCase and unnamespaced | field *game_rules*, ids namespaced (*minecraft:advance_time*) — the whole rename table is `GameRuleRegistryFix` |
| *doEntityDrops* | `GameRules.ENTITY_DROPS` |
| *doImmediateRespawn* | `GameRules.IMMEDIATE_RESPAWN` |
| *doInsomnia* | `GameRules.SPAWN_PHANTOMS` |
| *doLimitedCrafting* | `GameRules.LIMITED_CRAFTING` — the name survives elsewhere, as a component of `ClientboundLoginPacket` and a field on `LocalPlayer` |
| *doPatrolSpawning* / *doTraderSpawning* / *doWardenSpawning* | `GameRules.SPAWN_PATROLS` / `GameRules.SPAWN_WANDERING_TRADERS` / `GameRules.SPAWN_WARDENS` |
| *doVinesSpread* | `GameRules.SPREAD_VINES` |
| *enableCommandBlocks* **and** *commandBlocksEnabled* | one rule, `GameRules.COMMAND_BLOCKS_WORK` |
| *spawnerBlocksEnabled* | `GameRules.SPAWNER_BLOCKS_WORK` |
| *commandModificationBlockLimit* | `GameRules.MAX_BLOCK_MODIFICATIONS` |
| *minecartMaxSpeed* | `GameRules.MAX_MINECART_SPEED` |
| *snowAccumulationHeight* | `GameRules.MAX_SNOW_ACCUMULATION_HEIGHT` |
| *spawnRadius* | `GameRules.RESPAWN_RADIUS` |
| *disableElytraMovementCheck* | `GameRules.ELYTRA_MOVEMENT_CHECK` — **inverted** |
| *disablePlayerMovementCheck* | `GameRules.PLAYER_MOVEMENT_CHECK` — **inverted** |
| *disableRaids* | `GameRules.RAIDS` — **inverted** |
| *doFireTick* + *allowFireTicksAwayFromPlayer* (two booleans) | one integer, `GameRules.FIRE_SPREAD_RADIUS_AROUND_PLAYER` (0 none, 128 near players only, −1 everywhere) |
| *spawnChunkRadius*, *entitiesWithPassengersCanUsePortals*, *gameLoopFunction* | gone with no replacement — the fix simply deletes them |
| day time on *ServerLevel* | `ServerClockManager` (`world/clock`) |
| per-level weather | server-global `WeatherData` |
| *GameProfile* on the player lists | `NameAndId` (a record of UUID and name) — `PlayerList.canPlayerLogin`, `PlayerList.isWhiteListed`, `PlayerList.op`, the ban/op/whitelist files |
| *ServerPlayer.sendAllPlayerInfo* / *sendActivePlayerEffects* | `PlayerList.sendAllPlayerInfo` / `PlayerList.sendActivePlayerEffects` |
| *MinecraftServer.getScheduledEvents* returning a per-level queue | the same name, returning a server-wide `TimerQueue` saved data, advanced only by the overworld's `ServerLevel.tickTime` |
| *ServerLevel.updateSkyBrightness* reading day time | the method survives, declared on `Level`, and now reads `EnvironmentAttributes.SKY_LIGHT_LEVEL` through `EnvironmentAttributeSystem` |
| *ChunkMap.forEachBlockTickingChunk* meaning block-ticking | it walks the **entity**-ticking set; the name did not follow the split |

### Part IV — The world

| the name you remember | 26.2 |
|---|---|
| *ChunkStorage* | gone — `ChunkMap extends SimpleRegionStorage` |
| *DimensionDataStorage* | `SavedDataStorage` (two of them) |
| *getLightBlock* | `BlockBehaviour.BlockStateBase.getLightDampening` |
| *PalettedContainer.Strategy* | top-level `Strategy` + `Configuration` |
| *ForcedChunksSavedData* | `TicketStorage` |
| *TicketType&lt;T&gt;* | a registry record with flag bits |
| *DimensionType* booleans | `EnvironmentAttributeMap` |
| *DimensionType.ultraWarm* | split four ways: `EnvironmentAttributes.FAST_LAVA`, `EnvironmentAttributes.WATER_EVAPORATES`, `EnvironmentAttributes.INCREASED_FIRE_BURNOUT`, `EnvironmentAttributes.SNOW_GOLEM_MELTS` |
| *DimensionType.piglinSafe* | `EnvironmentAttributes.PIGLINS_ZOMBIFY` — **inverted** |
| *DimensionType.bedWorks* | `EnvironmentAttributes.BED_RULE`, a `BedRule` record, not a boolean |
| *DimensionType.hasRaids* | `EnvironmentAttributes.CAN_START_RAID` |
| *DimensionType.natural* | `EnvironmentAttributes.NETHER_PORTAL_SPAWNS_PIGLINS` and neighbours |
| *DimensionType.fixedTime* | `DimensionType.hasFixedTime`, a bare boolean — the time itself moved to `WorldClock` and `Timelines.OVERWORLD_DAY` |
| *DimensionType.ambientLight* | unchanged; one of the three visual fields that did not become an attribute, with `DimensionType.skybox` and `DimensionType.cardinalLightType` |
| *Schedule* (the villager's) | `EnvironmentAttributes.VILLAGER_ACTIVITY` on `Timelines.VILLAGER_SCHEDULE` |
| *Level.dayTime* | `ServerClockManager`, keyed by `WorldClock` |
| *data/&lt;id&gt;.dat* | *data/&lt;namespace&gt;/&lt;id&gt;.dat* — every saved-data file gained a namespace folder |

### Part V — Blocks

| the name you remember | 26.2 |
|---|---|
| *ItemInteractionResult* | gone — `InteractionResult.TryEmptyHandInteraction` |
| *DirectionProperty* | gone — `EnumProperty<Direction>` |
| *Level.markAndNotifyBlock* | gone — inline in `Level.setBlock` |
| *BlockBehaviour.onRemove* | `BlockBehaviour.affectNeighborsAfterRemoval` + `BlockEntity.preRemoveSideEffects` |
| *doTileDrops* | `GameRules.BLOCK_DROPS` |
| *BlockModelShaper* | `BlockStateModelSet` / `BlockModelSet` |
| *RenderShape.ENTITYBLOCK_ANIMATED* | gone — `RenderShape.INVISIBLE` / `RenderShape.MODEL` only |
| *Player.canInteractWithBlock* | `Player.isWithinBlockInteractionRange` |
| *Block.rebuildCache* | gone — `BlockBehaviour.BlockStateBase.initCache` from the `Blocks` static init |
| *Material* | gone — individual `BlockBehaviour.Properties` flags |
| *BlockEntity.saveToItem* | `BlockItem.setBlockEntityData` + `BlockEntity.collectComponents` |
| *MobEffects.DIG_SPEED* / *DIG_SLOWDOWN* | `MobEffects.HASTE` / `MobEffects.MINING_FATIGUE` |

### Part VI — Entities

| the name you remember | 26.2 |
|---|---|
| *Player extends LivingEntity* | `Player extends Avatar extends LivingEntity` |
| *EntityType.PIG* (constants) | `EntityTypes.PIG` + `EntityTypeIds.PIG` |
| *MobSpawnType* | `EntitySpawnReason` (+ `EntitySpawnRequest`) |
| *SpawnPlacements.Type* | `SpawnPlacementType` / `SpawnPlacementTypes` |
| *Entity.hurt(DamageSource, float)* returning a boolean | split into `Entity.hurtServer` and `Entity.hurtClient`. Both old shapes survive as deprecated finals — `Entity.hurt` delegating to the server half, `Entity.hurtOrSimulate` as the boolean-returning successor — so grep still finds the name |
| *doMobLoot* | `GameRules.MOB_DROPS` |
| *LivingEntity.isDamageSourceBlocked* | gone — `DataComponents.BLOCKS_ATTACKS` |
| *Schedule* / *ScheduleBuilder* | gone — `Timeline` + `EnvironmentAttribute` |
| *BlockPathTypes* | `PathType` |
| *Mob.brainProvider* | `LivingEntity.makeBrain(Brain.Packed)` |
| *Entity.moveTo* / *absMoveTo* | `Entity.snapTo` / `Entity.absSnapTo` |
| *Entity.maxUpStep* (field) | `Attributes.STEP_HEIGHT` |
| *Entity.updateFluidHeightAndDoFluidPushing* | `EntityFluidInteraction` |
| *Entity.lerpTo* | `Entity.moveOrInterpolateTo` + `InterpolationHandler` |
| *EntityDataSerializers.OPTIONAL_UUID* / *COMPOUND_TAG* | gone |
| UUID-keyed *AttributeModifier* | `Identifier`-keyed record |
| *AttributeMap.getDirtyAttributes* | `AttributeMap.getAttributesToSync` + `AttributeMap.getAttributesToUpdate` |
| *PlayerRenderer* | `AvatarRenderer` (serves players and mannequins, keyed by skin model) |

### Part VII — Items and inventories

| the name you remember | 26.2 |
|---|---|
| *InteractionResultHolder* | gone — `InteractionResult.Success.heldItemTransformedTo` |
| *UseAnim* | `ItemUseAnimation` |
| *Item.getFoodProperties* | `DataComponents.FOOD` on the stack |
| *ItemStack.getTag* / *getOrCreateTag* | gone — components |
| *LivingEntity.triggerItemUseEffects* | `Consumable.emitParticlesAndSounds` |
| *FoodProperties* effects list | `Consumable.onConsumeEffects` |
| *ClickType* | `ContainerInput` |
| *MultiPlayerGameMode.handleInventoryMouseClick* | `MultiPlayerGameMode.handleContainerInput` |
| *ClientboundSetCarriedItemPacket* | split: `ClientboundSetCursorItemPacket` + `ClientboundSetHeldSlotPacket` |
| *ClientboundSetSlotPacket* | `ClientboundContainerSetSlotPacket` |
| *ClientboundHorseScreenOpenPacket* | `ClientboundMountScreenOpenPacket` |
| *Container.startOpen(Player)* | `Container.startOpen(ContainerUser)` |
| *Recipe.getResultItem* / *getIngredients* | `Recipe.assemble` / `PlacementInfo`. The first is gone outright; the second is off the `Recipe` interface and survives only as a test-visible method on `ShapedRecipe` |
| *Ingredient.EMPTY* | gone — `Ingredient.CODEC` rejects an empty literal list, but a tag that resolves to nothing still yields an empty one, hence `Ingredient.isEmpty` |
| *ClientboundUpdateRecipesPacket* carrying recipes | property sets + the stonecutter input set; the book gets `RecipeDisplayEntry`s |
| *net.minecraft.advancements.CriteriaTriggers* | `CriteriaTriggers`, moved to `net/minecraft/advancements/triggers` |
| *Player.permissionLevel* / *hasPermissions(int)* | `Player.permissions` → a `PermissionSet`, queried by named `Permissions` keys |
| *ServerboundPlayerCommandPacket.Action.PRESS_SHIFT_KEY* / *RELEASE_SHIFT_KEY* | gone — sneak rides `ServerboundPlayerInputPacket` → `Entity.setShiftKeyDown` |
| *Mannequin* on the client | `ClientMannequin`, installed by swapping the mutable `Mannequin.constructor` factory at client startup |
| *data/&lt;ns&gt;/recipes/* | `data/<ns>/recipe/` (singular) |
| *EnchantmentCategory* | `Enchantment.EnchantmentDefinition` item sets |
| *Enchantment.getDamageBonus*, *EnchantmentHelper.getFireAspect*… | gone — `EnchantmentEffectComponents` |
| *EnchantedBookItem* | gone — `DataComponents.STORED_ENCHANTMENTS` |
| *Item.getEnchantmentValue* | `DataComponents.ENCHANTABLE` |
| *LootContextParam* / *LootContextParamSet* | `ContextKey` / `ContextKeySet` (`util/context`) |
| *LootDataManager* / *LootTables* | `ReloadableServerRegistries` + `BuiltInLootTables` |
| *LootTableReference* | `NestedLootTable` |
| *LootingEnchantFunction* | `EnchantedCountIncreaseFunction` |
| *SetCountFunction* | `SetItemCountFunction` |
| *LootContextParams.KILLER_ENTITY* | `LootContextParams.ATTACKING_ENTITY` |

### Part VIII — The player

| the name you remember | 26.2 |
|---|---|
| *Inventory.armor* / *offhand* / *compartments* | one 36-slot `Inventory.items` + `Inventory.EQUIPMENT_SLOT_MAPPING` |
| *Inventory.setPickedItem* | `Inventory.addAndPickItem` / `Inventory.pickSlot` |
| *Entity.moveTo* | `Entity.absSnapTo` / `Entity.snapTo` |
| *GameRenderer.pick* | `Minecraft.pick` → `LocalPlayer.raycastHitResult` |
| *ServerboundInteractPacket.Action.ATTACK* | `ServerboundAttackPacket` (a record of one int) |
| *GameRules.NATURAL_REGENERATION* | `GameRules.NATURAL_HEALTH_REGENERATION` |
| *isCritArrow* / *Player.sweepAttack* | `Player.canCriticalAttack` / `Player.isSweepAttack` + `Player.doSweepAttack`, all three private. *isCritArrow* was never a `Player` method and is still live on `AbstractArrow` |
| *LivingEntity.eat* / *Player.eat* | gone — `Consumable.onConsume` → `FoodProperties` → `FoodData.eat` |
| *MobEffect.createModifier* | `MobEffect.createModifiers` (plural) |

### Part IX — Networking

| the name you remember | 26.2 |
|---|---|
| *Connection.setListener* / *setProtocol* / *getCurrentProtocol* | gone — `Connection.setupInboundProtocol` / `Connection.setupOutboundProtocol` |
| *ConnectionProtocol.getById* / packet tables | gone — a bare enum; ids are `ProtocolInfoBuilder.addPacket` order in `IdDispatchCodec` |
| *Connection.NETWORK_WORKER_GROUP* etc. | `EventLoopGroupHolder` (in `server/network`) |
| *MemoryConnection* | gone — `Connection.isMemoryConnection` |
| *ensureRunningOnSameThread(…, BlockableEventLoop)* | `PacketUtils.ensureRunningOnSameThread` with a `PacketProcessor` |
| *Packet.write(FriendlyByteBuf)* | gone — a per-packet `StreamCodec` constant the protocol reads |
| *ClientboundAddPlayerPacket* / *ClientboundAddMobPacket* | gone — `ClientboundAddEntityPacket` |
| *ClientboundUpdateViewPositionPacket* | `ClientboundSetChunkCacheCenterPacket` |
| *ClientboundUpdateViewDistancePacket* | `ClientboundSetChunkCacheRadiusPacket` |
| *ClientboundLevelChunkPacket* | `ClientboundLevelChunkWithLightPacket` |
| routine *ClientboundTeleportEntityPacket* | `ClientboundEntityPositionSyncPacket` |
| *ClientboundGameProfilePacket* | `ClientboundLoginFinishedPacket` (+ a session id) |
| *ServerboundLoginStartPacket* | `ServerboundHelloPacket` |
| *ClientboundEncryptionRequestPacket* / response | `ClientboundHelloPacket` / `ServerboundKeyPacket` |
| *ClientboundSetCompressionPacket* | `ClientboundLoginCompressionPacket` |
| *ClientboundResourcePackPacket* | `ClientboundResourcePackPushPacket` / `…PopPacket` |
| *MinecraftServer.getSessionService* | `MinecraftServer.services` |
| *PlayerChunkSender* in *server/level* | `server/network` |
| *Component.Serializer* (Gson) | `ComponentSerialization` (codecs; NBT on the wire) |
| *TextComponent* / *TranslatableComponent* / … | `network/chat/contents` — `PlainTextContents` etc. |
| *ComponentUtils.updateForEntity* | `ComponentUtils.resolve` with a `ResolutionContext` |
| *SignedMessageHeader* / *MessageSigner* | `SignedMessageLink` / `SignedMessageChain.Encoder` |
| *ChatPreview* and its packets | gone |
| *ClientboundSetTimePacket(gameTime, dayTime, …)* | a game time plus a `WorldClock` update map |

### Part X — The client

| the name you remember | 26.2 |
|---|---|
| *Gui* (the HUD) | `Hud`, held as `Gui.hud`; the name `Gui` now means the screen/overlay manager |
| *Minecraft.screen* / *Minecraft.setScreen* | `Gui.screen` / `Gui.setScreen` |
| *GuiGraphics* | `GuiGraphicsExtractor` (records states; does not draw) |
| *Screen.render* / every *render** on *Gui* | `Screen.extractRenderState` / every *extract\** on `Hud` |
| *LayeredDraw* | call order plus `GuiRenderState.nextStratum` |
| *Options.hideGui* | `Hud.isHidden`, published as `GuiRenderState.isHudHidden` |
| *Minecraft.getPartialTick*, *Timer* | `DeltaTracker.Timer` and its three questions |
| *Minecraft.destroy* | gone — `Minecraft.stop`, then `Minecraft.exitWorldAndClose` and `Minecraft.close` |
| *Options.keyBindings* | `Options.keyMappings`; `KeyMapping.Category` is a registrable record, not a string |
| *Options.mouseSensitivity* | the field is `Options.sensitivity` with an accessor of that name; *mouseSensitivity* survives only as the key in *options.txt* |
| *MouseHandler.lastMouseEventTime* | gone |
| raw *(key, scancode, modifiers, action)* on every `Screen` method | the `client/input` records: `KeyEvent`, `MouseButtonEvent`, `CharacterEvent`, `PreeditEvent` |
| *ClientChunkCache.ChunkArray* | `ClientChunkCache.Storage` |
| *Font.drawInBatch* and every *drawString* variant | `Font.prepareText` → `Font.PreparedText`; the drawing verbs are on `GuiGraphicsExtractor` |
| *Font.StringRenderOutput* | `Font.PreparedText` plus `Font.GlyphVisitor` |
| *BakedGlyph* (a class) | an interface; the sheet implementation is `BakedSheetGlyph`, effects are `EffectGlyph` |
| *RawGlyph* / *SheetGlyphInfo* | `UnbakedGlyph` (info and bake) and `GlyphBitmap` (pixels and upload) |
| *GlyphProviderBuilder* / *GlyphProviderBuilderType* | `GlyphProviderDefinition` / `GlyphProviderType` |
| *Style.withFont* taking an id | still `Style.withFont`, but the type is `FontDescription`, which may be a sprite rather than a font |
| *FontSet.getGlyph* as public API | private — `FontSet.source` then `GlyphSource.getGlyph` |

### Part XI — Rendering

Twenty-seven rows, and almost all of them are one refactor: extract then
render.

| the name you remember | 26.2 |
|---|---|
| *MultiBufferSource* / *BufferSource* | `SubmitNodeCollector` / `SubmitNodeStorage` / `FeatureRenderDispatcher` |
| *ShaderInstance*, *RenderStateShard* | `RenderPipeline` + `RenderPipelines` + `BindGroupLayouts` |
| *VertexBuffer*, *Tesselator*, *BufferUploader* | `GpuBuffer` / `GpuBufferSlice`, `ByteBufferBuilder` → `MeshData`, `UberGpuBuffer` |
| *RenderSystem.setShader* / *enableBlend* / *depthMask* … | fields of a `RenderPipeline` |
| *VertexFormat.Mode*, *VertexFormat.IndexType*, *TextureFormat* | `PrimitiveTopology`, `IndexType`, `GpuFormat` |
| *Window.updateDisplay*, vsync as a swap interval | `GpuSurface.present`, vsync as a `GpuSurface.PresentMode` |
| *LightTexture.pack* and friends | `LightCoordsUtil` |
| *DimensionSpecialEffects* | `DimensionType.skybox` + `EnvironmentAttributes` + `Timeline` |
| *FogParameters*, *RenderSystem.setShaderFogColor* | `FogData`, `RenderSystem.setShaderFog` (a uniform slice) |
| *Level.getSkyColor*, *ClientLevel.getStarBrightness*, *ClientLevel.effects* | `EnvironmentAttributeProbe.getValue` on an `EnvironmentAttribute` |
| *LevelRenderer.renderLevel* / *renderSky* / *renderChunkLayer* | `LevelRenderer.render` and the `LevelRenderer.addSkyPass` family of frame-graph passes |
| *LevelRenderer.blockChanged* / *setSectionDirty* / *allChanged* | the same names on `LevelExtractor` |
| *ChunkRenderDispatcher*, *RenderChunk*, *CompiledChunk* | `SectionRenderDispatcher`, its `SectionRenderDispatcher.RenderSection`, `CompiledSectionMesh` |
| *RenderType.chunkBufferLayers* (five layers) | `ChunkSectionLayer` — three layers |
| *BakedModel*, *ModelResourceLocation* | `BlockStateModel` / `ItemModel`; block models keyed by `BlockState` |
| *BlockModelShaper*, *ItemModelShaper*, *BlockRenderDispatcher*, *ItemRenderer* | `BlockStateModelSet`, `ItemModelResolver`, `ModelBlockRenderer` |
| *BlockElement* / *BlockElementFace*, *AtlasSet*, *ItemColors* | `CuboidModelElement` / `CuboidFace`, `AtlasManager`, `ItemTintSource` |
| *EntityRenderer.render*, *RenderLayer.render* | `EntityRenderer.extractRenderState` + `EntityRenderer.submit` |
| *TextureSheetParticle*, sheet *ParticleRenderType*s | `SingleQuadParticle` + `SingleQuadParticle.Layer` |
| *ParticleGroup* (a limit record) | `ParticleLimit`; `ParticleGroup` is now the per-render-type bucket |
| *Camera.setup* | `Camera.update` + `Camera.extractRenderState` |
| *RenderStateShard* composition (the texture/target/layering half) | `RenderType` over a `RenderPipeline`, catalogued in `RenderTypes`, built by `RenderSetup` |
| *BakedQuad* as four vertices | a ten-component record, with a `BakedQuad.MaterialInfo` of six |
| *LiquidBlockRenderer* | `FluidRenderer`, over a `FluidModel` |
| *ItemOverrides* / *getPropertyOverride* | `SelectItemModel` / `RangeSelectItemModel` / `ConditionalItemModel` |
| *ScreenManager* (the Blaze3D monitor manager) | `MonitorManager`, with `Monitor` and `VideoMode` — same package, same GLFW monitor callback |
| *Window.setVsync* | a `GpuSurface.PresentMode` in the surface configuration |

### Part XII — World generation

| the name you remember | 26.2 |
|---|---|
| *GenerationStep.Carving* | gone — `BiomeGenerationSettings.carvers` is one flat `HolderSet` |
| *DensityFunctions.WeirdScaledSampler* | `DensityFunctions.IntervalSelect` |
| *StructureFeature* / *ConfiguredStructureFeature* | `Structure` / `Registries.STRUCTURE` |
| *Feature.RANDOM_PATCH*, *Feature.FLOWER* | gone — composed from `Feature.SIMPLE_BLOCK` + placement |
| *Feature.POINTED_DRIPSTONE* / *DRIPSTONE_CLUSTER* | `Feature.SPELEOTHEM` / `Feature.SPELEOTHEM_CLUSTER` |
| *AbstractTreeGrower* and its subclasses | one final `TreeGrower` with constants |
| *TreeConfiguration.dirtProvider* | `TreeConfiguration.belowTrunkProvider` |
| *Biome.BiomeCategory* / *Biome.getDownfall* | gone |
| *MultiNoiseBiomeSource.Preset* | `MultiNoiseBiomeSourceParameterList.Preset` |
| *BiomeSpecialEffects.fogColor* / *skyColor* / music / ambient sound | `EnvironmentAttributes.*` via `Biome.getAttributes` |
| the +8 chunk population offset | gone — decoration starts at the chunk corner, `InSquarePlacement` scatters |
| *StructureTemplateManager* folder *structures/* | *structure/* |

### Part XIII — Commands and data packs

The permission rewrite is the largest single break in this table: the
integer permission level is gone from the whole command API, replaced by
`PermissionSet` and `PermissionCheck` in `net/minecraft/server/permissions`.
The ints survive only in *ops.json*, in *server.properties* and on the wire.

| the name you remember | 26.2 |
|---|---|
| *ResourceLocationArgument* | `IdentifierArgument` (the registry id is unchanged) |
| *CommandSourceStack.hasPermission(int)* | `CommandSourceStack.permissions` + `PermissionSet.hasPermission` |
| *CommandSourceStack.getPermissionLevel* | gone — a source carries a `PermissionSet`. `PermissionLevel` itself is very much alive: `LevelBasedPermissionSet`, *server.properties*, `ServerOpListEntry` and the JSON-RPC schema all still speak it |
| *CommandSourceStack.withPermission(int)* | `CommandSourceStack.withPermission` taking a `PermissionSet` |
| *SharedSuggestionProvider.hasPermission(int)* | gone — the interface extends `PermissionSetSupplier` |
| *Commands.LEVEL_GAMEMASTERS* as an int | same name, now a `PermissionCheck` |
| *Commands.hasPermission(int)* | `Commands.hasPermission` taking a `PermissionCheck`, returning a `PermissionProviderCheck` |
| *ServerPlayer.hasPermissions(int)* | `ServerPlayer.permissions` |
| *MinecraftServer.getProfilePermissions* returning an int | the same name returning a `LevelBasedPermissionSet` |
| *MinecraftServer.getFunctionCompilationLevel* | `MinecraftServer.getFunctionCompilationPermissions` |
| *Commands.LEVEL_ALL* / *LEVEL_MODERATORS* / *LEVEL_ADMINS* / *LEVEL_OWNERS* as ints | all four are `PermissionCheck`s too — `PermissionCheck.AlwaysPass` for the first, `PermissionCheck.Require` for the rest |
| *ServerPlayer.setPermissionLevel(int)* | `PlayerList.sendPlayerPermissionLevel` on the server; `LocalPlayer.setPermissions` on the client |
| *ColorArgument* | `TeamColorArgument`, yielding a `TeamColor` rather than a `ChatFormatting` |
| *PlayerTeam.getColor* returning a *ChatFormatting* | returns an optional `TeamColor`, its own enum carrying a `TextColor` |
| *TestFunctionArgument* / *TestClassNameArgument* | gone — `/test` addresses tests as registry ids through `ResourceSelectorArgument` and `TestFinder` |
| *net.minecraft.advancements.Criterion* / *CriterionTrigger* / *SimpleCriterionTrigger* | all moved to `net/minecraft/advancements/triggers`; `CriterionTriggerInstance` is the one that stayed behind in `net/minecraft/advancements` |
| *ServerOpListEntry.getLevel* | `ServerOpListEntry.permissions` |
| *ParserUtils.parseJson* | gone — `SnbtGrammar` plus `ParserBasedArgument` |
| *ItemInput.createItemStack(int, boolean)* | `ItemInput.createItemStack` with one argument; the guard is `GiveCommand.MAX_ALLOWED_ITEMSTACKS` |
| *ServerFunctionManager.ExecutionContext* (nested) | top-level `ExecutionContext` in `net/minecraft/commands/execution` |
| *CommandFunction.Entry* / *CommandEntry* / *FunctionEntry* | gone — a line is a `BuildContexts.Unbound`, a macro line a `MacroFunction.MacroEntry` |
| *CommandFunction.CacheableFunction* (nested) | top-level `CacheableFunction`, codec-backed |
| *Commands.performCommand* returning a success count | returns nothing; results are a `CommandResultCallback` pair |
| `data/<ns>/functions/`, `data/<ns>/tags/functions/` | singular — *function/* and *tags/function/* |
| *maxCommandChainLength* | `GameRules.MAX_COMMAND_SEQUENCE_LENGTH` |
| *maxCommandForkCount* | `GameRules.MAX_COMMAND_FORKS` |
| *announceAdvancements* | `GameRules.SHOW_ADVANCEMENT_MESSAGES` |
| *net.minecraft.advancements.critereon* | split **three** ways: `net/minecraft/advancements/triggers`, `net/minecraft/advancements/predicates`, and `advancements/predicates/entity` for the entity half |
| *AdvancementList* | `AdvancementTree` (+ `AdvancementNode`, `AdvancementHolder`) |
| *FrameType* | `AdvancementType` |
| *CriterionTrigger.addPlayerListener* / *removePlayerListener* | gone — triggers are stateless; subscriptions live in `PlayerAdvancements` |
| *LootContextParamSet* | `ContextKeySet` |
| *@GameTest*, *@GameTestGenerator*, *@BeforeBatch*, *@AfterBatch* | gone — `GameTestInstance` in `Registries.TEST_INSTANCE` |
| *GameTestRegistry* / *TestFunction* | gone — `Registries.TEST_FUNCTION` + `TestFunctionLoader`, and `TestData` |
| a test's batch as a string | `GameTestInstance.batch` — the batch *is* a `TestEnvironmentDefinition` |
| the structure block as the test host | `TestInstanceBlock` / `TestInstanceBlockEntity` |

## The shape changes, not just the names

A rename table flatters the reader: it suggests that if you learn the two
hundred and forty-three rows above you can read the tree. You cannot, because a dozen of these rows are one
design change each, and the change is what the corresponding page is about.
The recurring ones:

- **Tags on an item became components.** *ItemStack.getTag* /
  *getOrCreateTag* have no replacement; a stack is an `Item` plus a
  `PatchedDataComponentMap` and every former tag key is a
  `DataComponentType` in `DataComponents` — [data components](../systems/foundations/data-components.md),
  [items and stacks](../systems/items/items-and-stacks.md).
- **Hand-written serialisation became codecs.** *Packet.write* is gone: a
  packet is a record with a `StreamCodec` the protocol table reads.
  *ItemStack.save* is gone: there is `ItemStack.CODEC` and, for saved data,
  the `ValueOutput` façade — [packets and stream codecs](../systems/networking/packets-and-stream-codecs.md),
  [codecs, NBT and JSON](../systems/foundations/codecs-nbt-json.md).
- **Rendering split into extract and render.** *GuiGraphics*,
  *EntityRenderer.render*, *LevelRenderer.renderLevel*, *MultiBufferSource*
  and every `RenderSystem` state setter are gone or repurposed, because the
  frame now builds an immutable render state on the game thread and draws
  from it — [the frame](../systems/rendering/the-frame.md), [Blaze3D](../systems/rendering/blaze3d.md),
  [entity rendering](../systems/rendering/entity-rendering.md).
- **Per-dimension and per-biome constants became one attribute system.**
  *DimensionSpecialEffects* and most of *BiomeSpecialEffects* are gone;
  fog, sky, water colour, ambient sound and music are
  `EnvironmentAttribute`s resolved through an `EnvironmentAttributeProbe`
  over a stack of layers — [lightmap, fog and sky](../systems/rendering/lightmap-fog-and-sky.md),
  [biomes](../systems/worldgen/biomes.md).
- **Enums of behaviour became registries of data.** *EnchantmentCategory*,
  *MobSpawnType*, *BlockPathTypes*, *GenerationStep.Carving* and
  *Biome.BiomeCategory* are all gone, replaced by item sets, registry
  records, `HolderSet`s or nothing at all.
- **UUIDs became identifiers.** An `AttributeModifier` is keyed by
  `Identifier`, not a UUID, which is why a data pack can now name one —
  [attributes](../systems/entities/attributes.md).
- **Sides split.** *Entity.hurt* became `Entity.hurtServer` and
  `Entity.hurtClient`; *Player.attack* is still there but the packet that
  reaches it is `ServerboundAttackPacket`, a record of one integer, and
  `ServerboundInteractPacket` is right-click only. The general rule: where
  1.21 had one method that checked `Level.isClientSide`, 26.2 tends to have
  two methods — [damage and death](../systems/entities/damage-and-death.md),
  [the sword swing](../systems/player/the-sword-swing.md).

## Yarn

Yarn is Fabric's community mapping set. It is not a different version of
the game and nothing on this list is a *change*: it is the same 26.2 class
under the name a Fabric modder has in their head. Only the ones that
actually trip people are listed — where the Yarn and Mojang names differ
enough that grep fails.

Both columns are italic here, because Yarn names are not in the decompile
and `verify_names.py` cannot check them; the Mojang column is the one this
corpus uses everywhere else, and every one of those names is backticked and
verified on its own page.

| Yarn | Mojang (this corpus) |
|---|---|
| *World* / *ServerWorld* / *ClientWorld* | *Level* / *ServerLevel* / *ClientLevel* |
| *WorldChunk* | *LevelChunk* |
| *MinecraftClient* | *Minecraft* |
| *PlayerEntity* / *ServerPlayerEntity* / *ClientPlayerEntity* | *Player* / *ServerPlayer* / *LocalPlayer* |
| *ClientPlayNetworkHandler* | *ClientPacketListener* |
| *ServerPlayNetworkHandler* | *ServerGamePacketListenerImpl* |
| *ClientConnection* | *Connection* |
| *Text* / *MutableText* | *Component* / *MutableComponent* |
| *TextRenderer* | *Font* |
| *TextHandler* | *StringSplitter* |
| *TextVisitFactory* | *StringDecomposer* |
| *OrderedText* | *FormattedCharSequence* |
| *StringVisitable* | *FormattedText* |
| *FontStorage* | *FontSet* |
| *GlyphAtlasTexture* | *FontTexture* |
| *DrawContext* | *GuiGraphicsExtractor* — and in 26.2 it does not draw; see the drift table |
| *NbtCompound* / *NbtList* / *NbtElement* | *CompoundTag* / *ListTag* / *Tag* |
| *RegistryEntry* / *RegistryEntryList* | *Holder* / *HolderSet* |
| *Registries* / *RegistryKeys* | *BuiltInRegistries* / *Registries* |
| *Vec3d* | *Vec3* |
| *Box* | *AABB* |
| *Hand* | *InteractionHand* |
| *ActionResult* | *InteractionResult* |
| *Inventory* (the interface) | *Container* |
| *PlayerInventory* | *Inventory* |
| *ScreenHandler* / *ScreenHandlerType* | *AbstractContainerMenu* / *MenuType* |
| *StatusEffect* / *StatusEffectInstance* | *MobEffect* / *MobEffectInstance* |
| *EntityAttribute* / *EntityAttributeInstance* | *Attribute* / *AttributeInstance* |
| *ParticleEffect* | *ParticleOptions* |
| *BlockPos.Mutable* | *BlockPos.MutableBlockPos* |
| *Identifier* | *Identifier* — Yarn was right first; Mojang renamed to match in 26.2 |

The last row is the joke that keeps giving: the single most-cited example
of "Yarn names are better" stopped being an example, and a decade of
Fabric code now compiles against a Mojang-named class with the Yarn name.

## What a rename table cannot tell you

- **A verified name is not a correct claim.** `verify_names.py` proves the
  right-hand column exists; it cannot prove the left-hand column ever did.
  The 1.21 side of this table is the only unverifiable content in the
  corpus, which is why it is confined to one page.
- **The names did not move where you would guess.** Rendering is the
  fourth-largest table, behind commands, the server and items. Two rewrites
  nobody advertised — permissions ceasing to be integers, and game rules
  becoming a registry — renamed more identifiers than the render-stack
  refactor did, and the render one is the famous half only because its
  classes are the ones tutorials name.
- **Renames cluster with rewrites.** No part of the tree renamed a class
  and kept its design; where the name changed, the responsibility usually
  moved too. Reading the row is not enough, which is what the linked page
  is for.
- **Two subsystems have no rows at all, and that is the answer.** Dialogs
  (`net/minecraft/server/dialog` and its client screens) and the JSON-RPC
  management server postdate 1.21 entirely: there is no old name to look up,
  and a reader who cannot find one is not missing a row. Game tests are the
  opposite case — the *whole* 1.21 API is gone, which is why they have five.
- **`Minecraft.setScreen` is a trap rather than a rename.**
  `Minecraft.setScreenAndShow` exists in 26.2 and a 1.21-era reader grepping
  for the old name will land on it, then wonder why the screen stack behaves
  differently. The method that replaced the old one is `Gui.setScreen`.
- **Some names survived and changed meaning**, which is worse than a
  rename because grep still finds them: `Gui` (now the screen manager, not
  the HUD), `Material` (now a texture reference in
  `client/resources/model/sprite`, not a block property), `ParticleGroup` (now a per-render-type bucket, not
  a count limit), `Strategy` (now top-level, not nested in
  `PalettedContainer`), and `MultiVariant`, whose name survives only in the
  data-generator package while the runtime type is gone.

## Where to look

`Identifier`, then `Holder` and `HolderSet` (`net/minecraft/core`), then `DataComponents`
— those three carry more of the drift than any others. After that, pick the
part you are lost in and read its page rather than its rows.

---

*Rules: names, never code · how the system works, not how the code reads ·
newest version only · every backticked name passes `tools/verify_names.py`.*
