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
  (`ServerGamePacketListenerImpl` is *SG* in Part V, check Part IX).
- Glossary + the naming-drift appendix (list below).

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

## Cross-part obligations (link, don't repeat)

What each unwritten part should point at instead of re-explaining. Tick
when the part is written.

- [x] **Part VI Entities** (session 6) — villager/POI half of `game-events-and-poi`;
  `PersistentEntitySectionManager.updateChunkStatus` / `Visibility`
  (session 4); `Block.popResource` → `ItemEntity` and `Entity.absSnapTo`
  from `block-breaking` / `blocks-and-states` (session 5).
- [ ] **Part VII Items** — menus (`ServerPlayer.openMenu`,
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
- [ ] **Part VIII The player** — `ServerPlayer` is created in the
  configuration phase (`PrepareSpawnTask`), owned by `players-and-sessions`;
  player ticking is split (`doTick` from the connection, `tick` from the
  level's entity loop) — do not contradict (session 3); the prediction
  ledger (`BlockStatePredictionHandler`) is in `block-interaction`;
  `Avatar`, i-frames, the armour/protection formulas and
  `ServerPlayer.die` (which never calls `super.die`) are in Part VI — link,
  do not repeat (session 6).
- [ ] **Part IX Networking** — `protocol-phases` points back at
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
  and the `ServerEntity.sendPairingData` bundle (session 6).
- [ ] **Part X The client** — names to pick up: `LevelExtractor`,
  `SectionUpdateTracker`, `SectionCopy` (session 4);
  `LevelExtractor.blockChanged`, `BlockBreakingRenderState`,
  `ModelBakery.DESTROY_TYPES`, `BlockStateModelSet`, `PistonHeadRenderer`,
  `BlockEntityRenderDispatcher` (session 5); the client lights per frame
  (`ClientLevel.update`, session 4); `EntityRenderDispatcher.extractEntity`,
  `SheepRenderState`, `AvatarRenderer` (there is no `PlayerRenderer`),
  `InterpolationHandler`, and `LivingEntityRenderer`'s red overlay from
  `LivingEntity.hurtTime` (session 6).
- [ ] **Part XI World generation** — *worldgen-pipeline* points at
  `chunk-generation-pipeline` for the conveyor;
  `ChunkStatus.MAX_STRUCTURE_DISTANCE` is dead code (session 4).
- [ ] **Part XII Commands** — the loot system's data-pack side
  (`LootTable`, `LootParams`, `LootContextParamSets.BLOCK`) is used but
  not explained in `block-breaking`.
- [ ] **Part XIII Appendix** — the naming-drift table above; the JSON-RPC
  and pause-when-empty paragraphs.

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

## Questions already known to be waiting for the owner

None yet — the owner has not started reading. When `<!-- Q: -->` comments
appear, a pass-2 session lists the pages here before answering them.
