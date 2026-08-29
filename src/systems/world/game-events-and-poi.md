# Game events and points of interest

> Verified against **Minecraft 26.2** · Part IV · A villager claims a bed — and, for the other half of the page, a footstep reaches a sculk sensor. Two side-indexes the world keeps about itself: what just happened, and what is worth going to.

## Responsibility

Two systems that let blocks and mobs know about the world without scanning
it. **Game events** are a fire-and-forget spatial broadcast: something
happens at a position, and every registered listener within range is told,
synchronously, on the server thread; vibrations (sculk, wardens, allays) are
a layer on top that adds travel time, selection and occlusion.
**Points of interest** are a persisted index of block states that matter to
AI — beds, bells, job blocks, portals, hives, lodestones — each carrying a
small ticket count that mobs claim and release, kept per chunk section in
its own region files and repaired on load.

The one sentence a player recognises: *the villager who walks straight to
"his" bed, and the sculk sensor that hears you unless you sneak.*

## The data it owns

### Game events

- `GameEvent` is a record of one field, `GameEvent.notificationRadius`
  (default `GameEvent.DEFAULT_NOTIFICATION_RADIUS`, 16; `GameEvent.JUKEBOX_PLAY`
  is 10, `GameEvent.SHRIEK` is 32), registered in `BuiltInRegistries.GAME_EVENT`
  — a defaulted registry whose fallback is `GameEvent.STEP`. Sixty-two
  constants, fifteen of them `GameEvent.RESONATE_1` … `GameEvent.RESONATE_15`,
  one per vibration frequency. `GameEvent.Context` carries the source entity
  and the affected block state.
- `GameEventDispatcher`, one per `ServerLevel` (`ServerLevel.gameEventDispatcher`),
  owns nothing across ticks: `GameEventDispatcher.post` walks the sections
  within the radius and calls listeners inline; only
  `GameEventListener.DeliveryMode.BY_DISTANCE` listeners (the sculk
  catalyst alone) are collected into `GameEvent.ListenerInfo`s, sorted, and
  delivered after the walk by `GameEventDispatcher.handleGameEventMessagesInQueue`.
- Listeners live in the chunk: `LevelChunk.gameEventListenerRegistrySections`,
  one `EuclideanGameEventListenerRegistry` per section Y, created on demand
  by `LevelChunk.getListenerRegistry` and dropped by
  `LevelChunk.removeGameEventListenerRegistry` when the last listener
  leaves. `ChunkAccess.getListenerRegistry` is `GameEventListenerRegistry.NOOP`
  — proto chunks and the client have no listeners. Block entities register
  through `LevelChunk.addGameEventListener` (via `EntityBlock.getListener`
  and `GameEventListener.Provider`); entities carry a
  `DynamicGameEventListener` that `ServerLevel.EntityCallbacks` adds,
  removes and `DynamicGameEventListener.move`s across sections
  (`Entity.updateDynamicGameEventListener`, overridden by `Warden` and
  `Allay`).
- A `GameEventListener` has a `PositionSource` (`BlockPositionSource` or
  `EntityPositionSource`, the latter resolving a UUID lazily), a
  `GameEventListener.getListenerRadius` and `GameEventListener.handleGameEvent`.
  The registry test is Euclidean, block-position distance squared against
  radius squared — a sphere inside the dispatcher's cube.
- `VibrationSystem` is the vibration layer, implemented by
  `SculkSensorBlockEntity`, `CalibratedSculkSensorBlockEntity`,
  `SculkShriekerBlockEntity`, `Warden` and `Allay`. Its parts:
  `VibrationSystem.User` (the policy — radius, `VibrationSystem.User.canReceiveVibration`,
  `VibrationSystem.User.onReceiveVibration`, `VibrationSystem.User.getListenableEvents`
  defaulting to `GameEventTags.VIBRATIONS`), `VibrationSystem.Listener`
  (the `GameEventListener` adapter that validates, tests occlusion and
  schedules), `VibrationSystem.Data` (the persisted state:
  `VibrationSystem.Data.currentVibration`, `VibrationSystem.Data.travelTimeInTicks`,
  a `VibrationSelector`; saved under *listener* through
  `VibrationSystem.Data.CODEC`, so an in-flight vibration survives a
  reload), and `VibrationSystem.Ticker`. `VibrationSystem.VIBRATION_FREQUENCY_FOR_EVENT`
  maps events to frequencies 1–15 (`GameEvent.STEP` is 1,
  `GameEvent.ENTITY_DIE` and `GameEvent.EXPLODE` are 15);
  `VibrationSystem.getRedstoneStrengthForDistance` is max(1, 15 − ⌊15 ×
  distance ÷ radius⌋). `VibrationSelector` holds at most one candidate per
  tick and `VibrationSelector.addCandidate` replaces it only for a closer
  one, or an equal-distance one with a higher frequency.
- Radii: sculk sensor `SculkSensorBlockEntity.VibrationUser.LISTENER_RANGE`
  8; calibrated sensor, warden and allay 16; shrieker
  `SculkShriekerBlockEntity.VibrationUser.LISTENER_RADIUS` 8. Sensor
  timings `SculkSensorBlock.ACTIVE_TICKS` 30, `SculkSensorBlock.COOLDOWN_TICKS`
  10. Warden `Warden.VIBRATION_COOLDOWN_TICKS` 40.

### Points of interest

- `PoiType` is a record: `PoiType.matchingStates`, `PoiType.maxTickets`
  and `PoiType.validRange`, registered in `BuiltInRegistries.POINT_OF_INTEREST_TYPE`
  by `PoiTypes.bootstrap`. `PoiTypes.HOME` (the bed — `PoiTypes.BEDS` is
  the **head** half only, `BedBlock.PART` = `BedPart.HEAD`), `PoiTypes.MEETING`
  (the bell, 32 tickets, range 6), the thirteen profession sites (1 ticket
  each), and the locatable-but-unclaimable `PoiTypes.NETHER_PORTAL`,
  `PoiTypes.BEEHIVE`, `PoiTypes.BEE_NEST`, `PoiTypes.LODESTONE`,
  `PoiTypes.LIGHTNING_ROD` with 0 tickets. `PoiTypes.TYPE_BY_STATE` is the
  block-state → type map built at bootstrap (a duplicate state throws);
  `PoiTypes.forState` and `PoiTypes.hasPoi` read it.
- `PoiRecord` is one entry: `PoiRecord.pos`, `PoiRecord.poiType`,
  `PoiRecord.freeTickets` (starts at `PoiType.maxTickets`);
  `PoiRecord.acquireTicket` / `PoiRecord.releaseTicket` are protected —
  only the section calls them. `PoiRecord.hasSpace`, `PoiRecord.isOccupied`.
- `PoiSection` holds a section's records (`PoiSection.records`, by
  section-relative position; `PoiSection.byType`) and a validity flag
  `PoiSection.isValid`; `PoiSection.Packed` is the disk form under
  *Valid* and *Records*.
- `PoiManager` extends `SectionStorage` ([chunk storage](chunk-storage.md))
  and is owned by `ChunkMap.poiManager` — the *poi/* folder,
  `DataFixTypes.POI_CHUNK`. Reached through `ServerLevel.getPoiManager`.
  Its query API is a stream family — `PoiManager.getInRange`,
  `PoiManager.getInSquare`, `PoiManager.getInChunk`, `PoiManager.findAll`,
  `PoiManager.findAllClosestFirstWithType`, `PoiManager.findClosest`,
  `PoiManager.find`, `PoiManager.getRandom`, `PoiManager.getCountInRange`,
  `PoiManager.exists`, `PoiManager.getType` — filtered by
  `PoiManager.Occupancy` (`PoiManager.Occupancy.HAS_SPACE`,
  `PoiManager.Occupancy.IS_OCCUPIED`, `PoiManager.Occupancy.ANY`).
  `PoiManager.take` acquires a ticket on the first free match;
  `PoiManager.release` gives one back and **throws** "POI never
  registered" if there is no record there. `PoiManager.add` /
  `PoiManager.remove` maintain the index.
- `PoiManager.distanceTracker`, a `PoiManager.DistanceTracker`, is the
  village graph: a `SectionTracker` (the same `DynamicGraphMinFixedPoint`
  the light engine once used and the ticket system still does) with
  `PoiManager.MAX_VILLAGE_DISTANCE` 6 sections, whose sources are sections
  where `PoiManager.isVillageCenter` — any *occupied* record whose type is
  in `PoiTypeTags.VILLAGE`. `PoiManager.sectionsToVillage` reads it;
  `ServerLevel.isVillage` is "within one section".
- The villager's side (Part VI owns the brain; named here because the
  trace passes through it): `MemoryModuleType.HOME`, `MemoryModuleType.JOB_SITE`,
  `MemoryModuleType.POTENTIAL_JOB_SITE`, `MemoryModuleType.MEETING_POINT`,
  each a persisted `GlobalPos`; `Villager.POI_MEMORIES` maps them to the
  types they may hold; the behaviours `AcquirePoi` (`AcquirePoi.SCAN_RANGE`
  48), `ValidateNearbyPoi` (`ValidateNearbyPoi.MAX_DISTANCE` 16),
  `SetWalkTargetFromBlockMemory`, `SleepInBed`, `PoiCompetitorScan`,
  `AssignProfessionFromJobSite`, wired up in `VillagerGoalPackages.getCorePackage`
  and `VillagerGoalPackages.getRestPackage`.

## When it runs

**Server thread, all of it.** Game events are posted from wherever the
thing happened — `Entity.move`, `Level.destroyBlock`, block use — and
delivered before the caller returns. Vibration travel is ticked by the
host: `SculkSensorBlock.getTicker` runs `VibrationSystem.Ticker.tick`
from the block-entity tick loop, `Warden.tick` and `Allay.tick` run it
themselves. The client's `ClientLevel.gameEvent` is an empty method; the
only thing a client sees of a vibration is a `VibrationParticleOption`
particle and the block-state changes.

POIs update from `Level.setBlock`: `ServerLevel.updatePOIOnBlockStateChange`
diffs `PoiTypes.forState` of the old and new state, and — because
`WorldGenRegion.setBlock` calls the same hook from worker threads — wraps
the `PoiManager.add` / `PoiManager.remove` in `MinecraftServer.execute`,
so even on the server thread the record appears on a later task, not
synchronously with the block. `PoiManager.tick` runs from `ChunkMap.tick`
under *poi* (dirty sections written while there is time, then the village
graph's `PoiManager.DistanceTracker.runAllUpdates`). On chunk load
`SerializableChunkData.read` calls `PoiManager.checkConsistencyWithBlocks`
per section — a section whose `PoiSection.isValid` is false is rebuilt by
scanning its block states (`PoiManager.updateFromSection`), short-circuited
by `PoiManager.mayHavePoi` when the palette has nothing interesting.

## The trace: a villager claims a bed

```mermaid
sequenceDiagram
    participant L as Level / ServerLevel
    participant PM as PoiManager
    participant PS as PoiSection
    participant B as Brain (Villager)
    participant AP as AcquirePoi
    participant NAV as PathNavigation
    participant WT as SetWalkTargetFromBlockMemory
    participant VP as ValidateNearbyPoi
    participant SB as SleepInBed

    L->>L: setBlock(bed) → updatePOIOnBlockStateChange: forState(head) = HOME
    L->>PM: (MinecraftServer.execute) add(pos, HOME)
    PM->>PS: add → PoiRecord(freeTickets = 1) · setDirty
    Note over B: CORE activity, every tick; HOME absent
    B->>AP: tick — nextScheduledStart passed?
    AP->>PM: findAllClosestFirstWithType(HOME, HAS_SPACE, 48) — five nearest, validateBedPoi
    AP->>NAV: createPath(candidates, range 1) — canReach?
    AP->>PM: take(HOME, target) → PoiRecord.acquireTicket (1 → 0)
    AP->>B: HOME = GlobalPos · broadcastEntityEvent 14 (happy particles)
    Note over B: night — REST activity
    B->>WT: WALK_TARGET toward HOME
    B->>VP: within 16: exists(pos, HOME)? bed OCCUPIED by another?
    B->>SB: within 2 and free → startSleeping → setBlock OCCUPIED (same PoiType, record untouched)
    Note over PM: the section is now a village centre — DistanceTracker floods 6 sections
```

1. **The bed becomes a POI.** Placing it runs `Level.setBlock` →
   `ServerLevel.updatePOIOnBlockStateChange`: the old state has no type,
   the new head-half state maps to `PoiTypes.HOME`, so a task is queued
   that calls `PoiManager.add` → `SectionStorage.getOrCreate` →
   `PoiSection.add` → a `PoiRecord` with one free ticket. `PoiSection.setDirty`
   marks the section for the *poi/* write; `PoiManager.setDirty` re-seeds
   the village graph. `LevelDebugSynchronizers.registerPoi` tells any debug
   subscriber.
2. **Acquisition is not a night thing.** The villager's `Activity.CORE`
   package always runs, and its priority-10 `AcquirePoi` for `PoiTypes.HOME`
   fires whenever `MemoryModuleType.HOME` is *absent* and the 20–40-tick
   `AcquirePoi.nextScheduledStart` has passed. It asks
   `PoiManager.findAllClosestFirstWithType` with `PoiManager.Occupancy.HAS_SPACE`
   and radius 48 — `PoiManager.getInSquare` over a chunk radius of 4,
   `PoiManager.getInChunk` per section (`SectionStorage.getOrLoad`, which
   blocks on a synchronous read if the section was never prefetched),
   `PoiSection.getRecords` filtered by `PoiRecord.hasSpace` — sorted by
   distance, limited to five, then `VillagerGoalPackages.validateBedPoi`
   (a bed, not `BedBlock.OCCUPIED`). Beds that recently failed are skipped
   by the `AcquirePoi.JitteredLinearRetry` cache (40–80 ticks, capped at
   `AcquirePoi.MAX_RETRY_PATHFINDING_INTERVAL`, 400).
3. **A path decides it.** `AcquirePoi.findPathToPois` →
   `PathNavigation.createPath` to the candidate set with range
   `PoiType.validRange` (1). If `Path.canReach`, `Path.getTarget` is the
   bed.
4. **The claim happens now, before walking.** `PoiManager.getType` still
   says *HOME* → `PoiManager.take` → `PoiSection` → `PoiRecord.acquireTicket`:
   `PoiRecord.freeTickets` goes 1 → 0 and the section is dirty. The memory
   is set to `GlobalPos.of` the level and position;
   `ServerLevel.broadcastEntityEvent` 14 is the green particle burst;
   `LevelDebugSynchronizers.updatePoi`. If no candidate was reachable,
   all of them go into the retry cache.
5. **Night.** `UpdateActivityFromSchedule` switches the brain to
   `Activity.REST`. `SetWalkTargetFromBlockMemory` for *HOME* (close enough
   1, too far 150, stale after 1200 ticks) writes `MemoryModuleType.WALK_TARGET`;
   `MoveToTargetSink` drives the navigation. `ValidateNearbyPoi` for *HOME*
   runs each tick within 16 blocks: if `PoiManager.exists` with the right
   type is false the memory is erased; if the bed is occupied by someone
   else (`ValidateNearbyPoi.bedIsOccupied`) the memory is erased and — if
   no sleeping villager is in it — the ticket `PoiManager.release`d.
6. **Arrival.** Within 2 blocks and the bed free, `SleepInBed.start` →
   `LivingEntity.startSleeping` → `Level.setBlock` with `BedBlock.OCCUPIED`
   true; `MemoryModuleType.LAST_SLEPT` is set and the walk target erased.
   That *setBlock* runs `ServerLevel.updatePOIOnBlockStateChange` too, but
   both occupied variants of the head map to *HOME*, so the record is
   untouched. **The ticket and the OCCUPIED flag are two independent
   facts.** Morning: `WakeUp` → `SleepInBed.stop` → `LivingEntity.stopSleeping`
   clears the flag; the ticket stays taken.
7. **The village.** The moment the ticket was taken the record became
   `PoiRecord.isOccupied`, `PoiTypes.HOME` is in `PoiTypeTags.VILLAGE`, so
   its section is a `PoiManager.isVillageCenter`; `PoiManager.DistanceTracker`
   floods level 0 six sections out. An *unclaimed* bed does not make a
   village.

Release paths: `Villager.die` → `Villager.releaseAllPois` →
`Villager.releasePoi` (`PoiManager.getType`, a `Villager.POI_MEMORIES`
check, then `PoiManager.release`); the same on witch conversion. A broken
bed goes `Level.setBlock` → `ServerLevel.updatePOIOnBlockStateChange` →
`PoiManager.remove` → `PoiSection.remove` — the record and its tickets
vanish, nothing is released — and the villager keeps the stale `GlobalPos`
until `ValidateNearbyPoi` finds `PoiManager.exists` false within 16 blocks;
nothing pushes the news to it. Job sites add `PoiCompetitorScan` (two
villagers, one site — the loser forgets), `YieldJobSite`,
`AssignProfessionFromJobSite` and `ResetProfession`.

## The second trace: a footstep reaches a sculk sensor

Registration first: `LevelChunk.registerAllBlockEntitiesAfterLevelLoad`
(or `LevelChunk.addAndRegisterBlockEntity` on placement) →
`LevelChunk.addGameEventListener` → `SculkSensorBlockEntity.getListener`
→ `EuclideanGameEventListenerRegistry.register` in the section's registry.

1. `Entity.move` → `Entity.applyMovementEmissionAndPlaySound` →
   `Entity.vibrationAndSoundEffectsFromBlock`: on the ground and not
   swimming, `GameEvent.STEP` with `GameEvent.Context.of` the entity and the
   block, if the entity's `Entity.MovementEmission` emits events.
2. `ServerLevel.gameEvent` → `GameEventDispatcher.post`: the radius 16 cube
   becomes a 3×3×3 range of sections; each chunk is fetched with
   `ServerChunkCache.getChunkNow` — loaded only, never loaded for the
   occasion — and each section's registry runs
   `EuclideanGameEventListenerRegistry.visitInRangeListeners`: sphere test
   at the listener's own radius (8 for a sensor), then
   `GameEventListener.handleGameEvent` inline. A registry being visited
   defers any register or unregister (`EuclideanGameEventListenerRegistry.processing`).
3. `VibrationSystem.Listener.handleGameEvent`: busy already? drop.
   `VibrationSystem.User.isValidVibration`: the event is in
   `GameEventTags.VIBRATIONS`; the source is not a spectator; if the entity
   `Entity.isSteppingCarefully` and the event is in
   `GameEventTags.IGNORE_VIBRATIONS_SNEAKING`, drop (and, since the sensor
   `VibrationSystem.User.canTriggerAvoidVibration`, fire
   `CriteriaTriggers.AVOID_VIBRATION` for a player); `Entity.dampensVibrations`
   (a warden) or an affected block in `BlockTags.DAMPENS_VIBRATIONS`, drop.
   Then `SculkSensorBlockEntity.VibrationUser.canReceiveVibration` — the
   sensor must be inactive (`SculkSensorBlock.canActivate`). Then
   `VibrationSystem.Listener.isOccluded`: six rays from positions nudged off
   the source block's centre, each a `BlockGetter.isBlockInLine` looking for
   `BlockTags.OCCLUDES_VIBRATION_SIGNALS` — occluded only if **all six**
   hit wool. Then `VibrationSystem.Listener.scheduleVibration` →
   `VibrationSelector.addCandidate` with a `VibrationInfo`.
4. Next tick, `SculkSensorBlock.getTicker` → `VibrationSystem.Ticker.tick`:
   nothing in flight, so `VibrationSelector.chosenCandidate` (only
   candidates from an *earlier* tick — one tick of latency by design) →
   `VibrationSystem.Data.setCurrentVibration`, travel time
   `VibrationSystem.User.calculateTravelTimeInTicks` = ⌊distance⌋ — one
   block per tick — and `ServerLevel.sendParticles` a `VibrationParticleOption`
   carrying the destination `PositionSource` and the tick count: the whole
   of what the client is told.
5. Each tick `VibrationSystem.Data.decrementTravelTime`; at zero,
   `VibrationSystem.User.requiresAdjacentChunksToBeTicking` (true for a
   sensor: the 3×3 must `Level.shouldTickBlocksAt`, else wait) →
   `SculkSensorBlockEntity.VibrationUser.onReceiveVibration` → frequency 1,
   power from `VibrationSystem.getRedstoneStrengthForDistance` →
   `SculkSensorBlock.activate` (`SculkSensorBlock.PHASE` active, 30 ticks,
   emitting `GameEvent.SCULK_SENSOR_TENDRILS_CLICKING` — what shriekers
   listen for — and `SculkSensorBlock.tryResonateVibration` from adjacent
   `BlockTags.VIBRATION_RESONATORS`). `SculkSensorBlock.deactivate` after
   the cooldown. Standing *on* the sensor is a shortcut:
   `SculkSensorBlock.stepOn` → `VibrationSystem.Listener.forceScheduleVibration`,
   no dispatcher, no occlusion.

## Interfaces

- **Called by:** every emitter — `Entity.gameEvent`, `Level.destroyBlock`,
  block and item code — through `LevelAccessor.gameEvent`; `Level.setBlock`
  via `ServerLevel.updatePOIOnBlockStateChange`; the brain behaviours above;
  `PortalForcer` (`PoiTypes.NETHER_PORTAL`, radius 16, after
  `PoiManager.ensureLoadedAndValid`), `Bee` (`PoiTypeTags.BEE_HOME`), the
  lightning-rod search in `ServerLevel` (radius 128), `LocateCommand`,
  `Raids`, `CatSpawner`, `WanderingTraderSpawner`, `VillageSiege` and the
  village-bound goals through `ServerLevel.isVillage` /
  `ServerLevel.isCloseToVillage` / `ServerLevel.sectionsToVillage`.
- **Calls into:** `PathNavigation` (Part VI), `SectionStorage` (storage),
  `BlockGetter.isBlockInLine`, `SculkSensorBlock` / `Warden` / `Allay` users.
- **Crosses the network as:** nothing of its own. `VibrationParticleOption`
  through the particle packet; `ServerLevel.broadcastEntityEvent` 14; the
  debug channel — `DebugSubscriptions.GAME_EVENTS`,
  `DebugSubscriptions.GAME_EVENT_LISTENERS`, `DebugSubscriptions.POIS`,
  `DebugSubscriptions.VILLAGE_SECTIONS` via `LevelDebugSynchronizers` (there
  is no *DebugPackets* class; `ClientboundGameEventPacket` is weather and
  game state, unrelated).
- **Data-driven by:** `Registries.GAME_EVENT` and
  `Registries.POINT_OF_INTEREST_TYPE` (both built-in, not data-pack);
  `GameEventTags.VIBRATIONS`, `GameEventTags.WARDEN_CAN_LISTEN`,
  `GameEventTags.SHRIEKER_CAN_LISTEN`, `GameEventTags.ALLAY_CAN_LISTEN`,
  `GameEventTags.IGNORE_VIBRATIONS_SNEAKING`; `BlockTags.OCCLUDES_VIBRATION_SIGNALS`,
  `BlockTags.DAMPENS_VIBRATIONS`, `BlockTags.VIBRATION_RESONATORS`;
  `PoiTypeTags.VILLAGE`, `PoiTypeTags.ACQUIRABLE_JOB_SITE`, `PoiTypeTags.BEE_HOME`.

## Invariants and surprises

- **The bed is claimed when a path exists, not on arrival.** `AcquirePoi`
  takes the ticket up to 48 blocks away; `SleepInBed` sets `BedBlock.OCCUPIED`
  later, and the two facts are independent. An empty bed can be "owned".
- **The dispatcher never queues.** Every ordinary listener is called inside
  the section walk, before the emitter's method returns; only the sculk
  catalyst is sorted by distance. The per-tick "nearest wins" is
  `VibrationSelector`, per listener, and always costs one tick.
- **Wool is a six-ray test.** One block on the straight line is usually
  not enough; all six nudged rays must hit `BlockTags.OCCLUDES_VIBRATION_SIGNALS`.
- **POI updates are deferred through `MinecraftServer.execute`**, even
  from the server thread, because worldgen calls the same hook from
  workers. A record appears a task later than its block.
- **`PoiManager.release` throws** on a position with no record — which is
  why every releaser checks `PoiManager.getType` or `PoiManager.exists`
  first, and why a broken bed's record simply disappears rather than being
  released.
- **Only the bed's head is a POI**; the foot half is not in `PoiTypes.BEDS`.
- **Events near unloaded chunks are silently dropped** for those sections
  — `GameEventDispatcher.post` uses `ServerChunkCache.getChunkNow`.
- **The village graph is the light engine's graph.** `PoiManager.DistanceTracker`
  → `SectionTracker` → `DynamicGraphMinFixedPoint`.
- **Sneaking is a tag, not a hard rule** (`GameEventTags.IGNORE_VIBRATIONS_SNEAKING`),
  and an unknown game-event id decodes to `GameEvent.STEP`.

## Where to look

`GameEventDispatcher.post` · `EuclideanGameEventListenerRegistry.visitInRangeListeners` ·
`LevelChunk.getListenerRegistry` · `LevelChunk.addGameEventListener` ·
`DynamicGameEventListener.move` · `ServerLevel.EntityCallbacks` ·
`Entity.vibrationAndSoundEffectsFromBlock` · `VibrationSystem.Listener.handleGameEvent` ·
`VibrationSystem.Listener.isOccluded` · `VibrationSystem.Ticker.tick` ·
`VibrationSelector.addCandidate` · `SculkSensorBlockEntity.VibrationUser` ·
`SculkSensorBlock.activate` · `Warden.VibrationUser` · `PoiManager.take` ·
`PoiManager.release` · `PoiManager.getInRange` · `PoiManager.checkConsistencyWithBlocks` ·
`PoiManager.DistanceTracker` · `PoiSection` · `PoiRecord.acquireTicket` ·
`PoiTypes.forState` · `ServerLevel.updatePOIOnBlockStateChange` ·
`AcquirePoi.create` · `ValidateNearbyPoi` · `SleepInBed.start` ·
`Villager.releasePoi` · `VillagerGoalPackages.getCorePackage`

---

*Rules: names, never code · how the system works, not how the code reads ·
newest version only · every backticked name passes `tools/verify_names.py`.*
