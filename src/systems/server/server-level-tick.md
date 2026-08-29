# The level tick

> Verified against **Minecraft 26.2** · Part III · One tick of one `ServerLevel`, from the world border to the last entity, and the queued-up packets it leaves behind.

## Responsibility

`ServerLevel.tick` is where the world actually changes. The server tick
([previous page](server-tick.md)) is scheduling; the level tick is content:
weather advances, scheduled block and fluid ticks fire, raids progress,
chunks near players get random ticks and mob spawns, every entity in range
runs its `Entity.tick`, block entities run their tickers, and the block
changes that all of that produced are batched up for the clients. Each
dimension is its own `ServerLevel` and gets its own call, overworld first.

The one sentence a player recognises: *crops grow, mobs spawn, water flows
and the rain starts — all inside this one method, twenty times a second.*

## The data it owns

- `ServerLevel` holds the per-dimension tick state: `ServerLevel.blockTicks`
  and `ServerLevel.fluidTicks` (two `LevelTicks`, the scheduled-tick queues
  — one `LevelChunkTicks` per loaded chunk, gathered on demand);
  `ServerLevel.blockEvents` (an ordered, de-duplicating set of
  `BlockEventData` — note-block plays, piston pushes, chest lid counts — for
  this tick); `ServerLevel.entityTickList` (an `EntityTickList`: every entity
  whose chunk is in ticking state, keyed by entity id);
  `ServerLevel.entityManager` (the `PersistentEntitySectionManager` that
  decides which entities are in that list); `ServerLevel.raids`;
  `ServerLevel.dragonFight` (an `EnderDragonFight`, End only);
  `ServerLevel.sleepStatus`; `ServerLevel.customSpawners` (the overworld's
  `PhantomSpawner`, `PatrolSpawner`, `CatSpawner`, `VillageSiege`,
  `WanderingTraderSpawner`); `ServerLevel.emptyTime`; and the flag
  `ServerLevel.handlingTick`.
- Two things a 1.21 reader expects here have **left the level**. Day time is
  a set of `WorldClock`s owned by `ServerClockManager` (server-wide saved
  data, ticked from `MinecraftServer.tickChildren`); `ServerLevel.tickTime`
  only advances *gameTime* (and only in the overworld) and runs the timer
  queue. Weather is one `WeatherData` saved-data object owned by the
  *server* — `ServerLevel.getWeatherData` delegates to the `MinecraftServer`
  — and every level that `Level.canHaveWeather` advances the same countdowns; the
  only per-level part is the `Level.rainLevel`/`Level.thunderLevel` fade.
- `ServerChunkCache` (the level's chunk source; the rest of it is Part IV)
  owns the chunk-ticking half: `ServerChunkCache.spawningChunks`,
  `ServerChunkCache.lastSpawnState` (a `NaturalSpawner.SpawnState`, the mob
  counts the debug screen shows) and `ServerChunkCache.chunkHoldersToBroadcast`
  (every `ChunkHolder` with a pending block or light change).
- Random ticks do not draw from `Level.random`. `Level.getBlockRandomPos`
  advances `Level.randValue`, a plain LCG, and packs x, y, z out of one int;
  `Level.random` (a `RandomSource`) is for the ice/snow and lightning rolls
  and the shuffle of the spawning chunks.
- Inherited from `Level`: `Level.blockEntityTickers` with its
  `Level.pendingBlockEntityTickers` side list and the
  `Level.tickingBlockEntities` guard, so a block entity created mid-tick
  (a chest a piston just pushed) waits a tick.

## When it runs

On the *Server thread*, once per level per server tick, from
`MinecraftServer.tickChildren` under the *levels* profiler section, wrapped
in a `CrashReport` titled "Exception ticking world". The `BooleanSupplier`
it receives is the server's `MinecraftServer.haveTime`; the level itself
does not check it — it hands it to `ServerChunkCache.tick`, which passes it
to `ChunkMap.tick` for chunk unloading, the one time-sliced piece.

Everything below is synchronous. The single concurrent structure is
`PersistentEntitySectionManager.loadingInbox`, the queue that the chunk
storage fills with loaded entities from IO threads and that the level
drains, on this thread, at the end of the tick.

`TickRateManager.runsNormally` — false while `/tick freeze` is on and no
step is pending — gates most of the steps below individually. The
`ServerChunkCache.tick` call is *not* gated, which is why a frozen world
still loads and unloads chunks and still sends block updates.

## The trace: one tick of one level

```mermaid
sequenceDiagram
    participant SL as ServerLevel
    participant WB as WorldBorder
    participant LT as LevelTicks (blocks, then fluids)
    participant SCC as ServerChunkCache
    participant NS as NaturalSpawner
    participant CM as ChunkMap
    participant ETL as EntityTickList
    participant E as Entity
    participant PESM as PersistentEntitySectionManager
    participant PL as PlayerList

    SL->>WB: tick — the border interpolates toward its target size
    SL->>SL: advanceWeatherCycle — countdowns on the server's WeatherData; rain/thunder level fade ±0.01
    SL->>PL: broadcastAll ClientboundGameEventPacket — RAIN_LEVEL_CHANGE / START_RAINING as needed
    SL->>SL: SleepStatus.areEnoughSleeping? moveToTimeMarker(WAKE_UP_FROM_SLEEP), wakeUpAllPlayers, resetWeatherCycle
    SL->>SL: updateSkyBrightness · tickTime (gameTime++, timer queue)
    SL->>LT: tick(gameTime, 65536, tickBlock) — collect due containers, run, cleanup
    LT->>SL: tickBlock — still the same Block here? then BlockState.tick
    SL->>LT: tick(gameTime, 65536, tickFluid)
    SL->>SL: Raids.tick
    SL->>SCC: tick(haveTime, true)
    SCC->>SCC: purge stale tickets · runDistanceManagerUpdates
    SCC->>NS: createState — count mobs per MobCategory over the spawnable chunks
    SCC->>CM: collectSpawningChunks — within 8 chunks and 128 blocks of a player, then shuffled
    loop each spawning chunk
        SCC->>SL: tickThunder — 1 in 100000 while raining and thundering
        SCC->>NS: spawnForChunk — only categories under their cap
    end
    loop each block-ticking chunk
        SCC->>SL: tickChunk — iceandsnow (1/48 per roll), then RANDOM_TICK_SPEED random ticks per non-empty section
    end
    SCC->>SL: tickCustomSpawners — phantoms, patrols, cats, sieges, wandering trader
    SCC->>CM: tick — player chunk tracking, TrackedEntity updates (entity add/move/remove packets)
    SCC->>CM: broadcastChangedChunks — ChunkHolder.broadcastChanges: block and light update packets, once per chunk
    SCC->>CM: tick(haveTime) — poi, chunk_unload, until haveTime is false
    SL->>SL: runBlockEvents — BlockState.triggerEvent, then ClientboundBlockEventPacket within 64 blocks
    SL->>SL: emptyTime < 300? (a level nobody is in stops here)
    SL->>SL: EnderDragonFight.tick (End only)
    SL->>ETL: forEach
    loop each entity in ticking chunks
        ETL->>SL: skip if removed or isEntityFrozen · checkDespawn
        SL->>E: tickNonPassenger — setOldPosAndRot, Entity.tick, then tickPassenger → rideTick for each rider
    end
    SL->>SL: tickBlockEntities — each TickingBlockEntity whose chunk is block-ticking
    SL->>PESM: tick — drain loadingInbox (new entities start ticking), then chunksToUnload
```

Narrated:

1. **Border and weather, if running.** `WorldBorder.tick` moves the
   interpolated extent. `ServerLevel.advanceWeatherCycle` counts down the
   clear/rain/thunder timers on the shared `WeatherData` — the ranges are the
   constants `ServerLevel.RAIN_DELAY`, `ServerLevel.RAIN_DURATION`,
   `ServerLevel.THUNDER_DURATION` — and fades the two float levels by 0.01
   per tick, so a rain start is a five-second ramp. Every change is a
   `ClientboundGameEventPacket`: the level packets go to this dimension's
   players, the start/stop packets go to *every* player in every dimension.
2. **Sleep.** `SleepStatus.areEnoughSleeping` (against
   `GameRules.PLAYERS_SLEEPING_PERCENTAGE`) and
   `SleepStatus.areEnoughDeepSleeping` decide the skip; if
   `GameRules.ADVANCE_TIME` is on and the dimension has a default clock,
   `ServerClockManager.moveToTimeMarker` jumps it to
   `ClockTimeMarkers.WAKE_UP_FROM_SLEEP`; `ServerLevel.wakeUpAllPlayers`
   and, if `GameRules.ADVANCE_WEATHER`, `ServerLevel.resetWeatherCycle`.
   The clock move is what sends the `ClientboundSetTimePacket` — the level
   does not send time itself.
3. **Scheduled ticks.** `LevelTicks.tick` is called twice — blocks, then
   fluids — with *gameTime* and a budget of
   `ServerLevel.MAX_SCHEDULED_TICKS_PER_TICK` (65536) each. It collects
   every `LevelChunkTicks` container whose next `ScheduledTick` is due and
   whose chunk passes `ServerLevel.isPositionTickingWithEntitiesLoaded`,
   drains them in `ScheduledTick.DRAIN_ORDER` (time, then `TickPriority`,
   then submission order), and calls back `ServerLevel.tickBlock` /
   `ServerLevel.tickFluid` — which check the block is *still* the scheduled
   `Block` before `BlockBehaviour.BlockStateBase.tick` runs. A replaced block's pending tick
   silently evaporates. Part IV's *block-ticks-and-fluids*
   page has the queue itself.
4. **Raids**, then **the chunk source.** `ServerChunkCache.tick` first
   purges stale tickets and runs `DistanceManager` updates (chunks change
   ticking state here — the reason an entity starts or stops ticking is
   decided *before* entities tick), then, if running, `ServerChunkCache.tickChunks`.
5. **Two chunk sets, two jobs.** `NaturalSpawner.createState` counts every
   mob by `MobCategory` across `DistanceManager.getNaturalSpawnChunkCount`
   chunks; a category may spawn only while its count is under
   `MobCategory.getMaxInstancesPerChunk` × spawnable chunks ÷ 289
   (`NaturalSpawner.MAGIC_NUMBER`, 17²) — the mob cap — and
   `LocalMobCapCalculator` applies the same test per player. Persistent
   categories (animals) are only considered every 400 ticks.
   `ChunkMap.collectSpawningChunks` gathers the **spawning chunks** — within
   8 chunks *and* 128 blocks (`ChunkMap.playerIsCloseEnoughForSpawning`) of
   some player — shuffles them, and each gets its inhabited time bumped,
   `ServerLevel.tickThunder` (a 1-in-100000 roll per chunk per tick while
   raining and thundering; the bolt prefers a lightning rod, then a mob
   that can see the sky, then the heightmap; a trap skeleton horse rides in
   with `effective difficulty` × 1 % odds), and `NaturalSpawner.spawnForChunk`.
   Separately `ChunkMap.forEachBlockTickingChunk` — which, despite the
   name, walks the *entity*-ticking set — gives each chunk
   `ServerLevel.tickChunk`: *tickSpeed* rolls of 1/48 for ice and snow
   (`Biome.shouldFreeze`, `Biome.shouldSnow`, snow capped by
   `GameRules.MAX_SNOW_ACCUMULATION_HEIGHT`), then
   `GameRules.RANDOM_TICK_SPEED` (default 3) random positions in every
   `LevelChunkSection` that `LevelChunkSection.isRandomlyTicking` — a
   section with nothing that random-ticks costs nothing.
6. **Custom spawners, then tracking.** `ServerLevel.tickCustomSpawners`
   runs the list above (each a `CustomSpawner`, gated by its own rule:
   `GameRules.SPAWN_PHANTOMS`, `GameRules.SPAWN_PATROLS`,
   `GameRules.SPAWN_WANDERING_TRADERS`). `ChunkMap.tick` (the no-argument
   one) updates every player's chunk tracking and every
   `ChunkMap.TrackedEntity` — the entity add/move/remove packets for
   everything that moved last tick go out here, to whoever is in range.
7. **Block and light changes leave once.** `ServerLevel.sendBlockUpdated`
   never sends a packet; it calls `ServerChunkCache.blockChanged`, which
   marks the `ChunkHolder`. `ServerChunkCache.broadcastChangedChunks` now
   walks `ServerChunkCache.chunkHoldersToBroadcast` and `ChunkHolder.broadcastChanges` emits
   one `ClientboundBlockUpdatePacket` for a section with one change, a
   `ClientboundSectionBlocksUpdatePacket` for several, and
   `ClientboundLightUpdatePacket` for light — to the players tracking that
   chunk. A hundred blocks changed by a command in one tick are one packet.
   This happens **before** entities tick, so an entity's own block changes
   are seen by clients one tick later.
8. **Unloads, time-sliced.** `ChunkMap.tick` with the supplier: POI saving
   and *chunk_unload* until `MinecraftServer.haveTime` says stop. The only step in the level
   tick that yields to the clock.
9. **Block events.** `ServerLevel.runBlockEvents` drains `ServerLevel.blockEvents`
   completely, calling `BlockBehaviour.BlockStateBase.triggerEvent` and, when it returns true,
   broadcasting a `ClientboundBlockEventPacket` to players within 64
   blocks. Events for chunks outside block-ticking range are re-queued
   (`ServerLevel.blockEventsToReschedule`) rather than dropped. Because the
   set is a linked hash set, two identical events in one tick collapse to
   one.
10. **The empty check.** `ServerChunkCache.hasActiveTickets` resets
    `ServerLevel.emptyTime`; otherwise it counts, and past
    `ServerLevel.EMPTY_TIME_NO_TICK` (300) the level skips everything that
    follows. A dimension with nobody in it and no forced chunks costs the
    steps above and nothing more.
11. **Entities.** After `EnderDragonFight.tick` in the End,
    `EntityTickList.forEach` runs the loop. Per entity: skip if removed;
    skip if `TickRateManager.isEntityFrozen` (frozen, and not a player or
    a player's mount); `Entity.checkDespawn`; then tick only if it is a
    `ServerPlayer` **or** its chunk is in `DistanceManager.inEntityTickingRange`.
    A passenger whose vehicle is alive and still lists it is skipped here
    and ticked by the vehicle: `ServerLevel.tickNonPassenger` records the
    old position, calls `Entity.tick`, then `ServerLevel.tickPassenger` →
    `Entity.rideTick` for each rider, recursively. `Level.guardEntityTick`
    wraps each in a "Ticking entity" crash report section.
12. **Block entities, then bookkeeping.** `Level.tickBlockEntities` runs
    every `TickingBlockEntity` whose position passes
    `Level.shouldTickBlocksAt` (block-ticking range, not entity range).
    Finally `PersistentEntitySectionManager.tick` drains the
    `PersistentEntitySectionManager.loadingInbox` — entities from freshly loaded chunks appear in the world
    now — and processes `PersistentEntitySectionManager.chunksToUnload`; the `ServerLevel.EntityCallbacks`
    it fires (`ServerLevel.EntityCallbacks.onTickingStart`, `ServerLevel.EntityCallbacks.onTickingEnd`) are what add and remove
    entries in `ServerLevel.entityTickList`, so the loop in step 11 never sees an
    entity from a chunk that is not ticking.

## Interfaces

- **Called by:** `MinecraftServer.tickChildren`, only.
- **Calls into:** `LevelTicks` and `BlockBehaviour.BlockStateBase.tick` (Parts IV and V),
  `ServerChunkCache` / `ChunkMap` / `DistanceManager` (Part IV),
  `NaturalSpawner` and `Entity.tick` (Part VI), `TickingBlockEntity`
  (Part V), `Raids`, `EnderDragonFight`, `ServerClockManager`.
- **Crosses the network as:** `ClientboundGameEventPacket` (weather, from
  `ServerLevel.advanceWeatherCycle`); `ClientboundBlockUpdatePacket` /
  `ClientboundSectionBlocksUpdatePacket` / `ClientboundLightUpdatePacket`
  (from `ChunkHolder.broadcastChanges`); `ClientboundBlockEventPacket`
  (from `ServerLevel.runBlockEvents`); `ClientboundSetTimePacket` (from the clock
  manager, not the level); entity packets from `ChunkMap.TrackedEntity`
  (Part IX). All of them are queued behind the connection's suspended flush
  and leave at the end of the server tick.
- **Data-driven by:** the game rules named above (`GameRules` now lives in
  `world/level/gamerules`; there is no *DO_DAYLIGHT_CYCLE* or
  *DO_MOB_SPAWNING* — they are `GameRules.ADVANCE_TIME` and `GameRules.SPAWN_MOBS`); `Biome`
  for precipitation; `MobCategory` for the caps; the dimension type's
  default clock for whether sleeping does anything.

## Invariants and surprises

- **Order is decided, then acted on.** Chunk ticking state
  (`ServerChunkCache.runDistanceManagerUpdates`) and entity ticking membership
  (`PersistentEntitySectionManager.tick`) are updated in fixed slots; between them the
  entity loop sees a stable list. `EntityTickList` enforces this: it allows
  exactly one `EntityTickList.forEach` at a time and swaps its `EntityTickList.active`/`EntityTickList.passive` maps on
  a mid-iteration add or remove so the running loop keeps the old view.
- **Players always tick; nothing else ticks outside entity-ticking range.**
  The `ServerPlayer` check in the loop is the only exemption. A mob in a
  chunk that is loaded but only `FullChunkStatus.BLOCK_TICKING` stands still
  and does not despawn.
- **Block entities follow block-ticking range; entities follow entity-ticking
  range.** Two different `ChunkLevel` thresholds
  (`ChunkLevel.BLOCK_TICKING_LEVEL` 32, `ChunkLevel.ENTITY_TICKING_LEVEL` 31);
  a furnace keeps smelting one chunk further out than a zombie keeps walking.
- **Random ticks are per section, and cheap sections are free.**
  `LevelChunkSection.isRandomlyTicking` is a counter maintained on every
  block change; a section of stone is skipped outright.
- **Freezing the game does not freeze the chunk system.** Tickets, distance
  updates, chunk broadcast and unloads run every tick regardless of
  `TickRateManager.runsNormally`; only `ServerChunkCache.tickChunks` (spawning, random ticks) is gated.
- **A block's scheduled tick is a promise to *that block*.** `ServerLevel.tickBlock`
  compares the `Block` at the position with the one scheduled; mismatch
  means nothing runs. This is why replacing a block cancels its pending
  ticks without any explicit cancellation.
- **Weather timers are shared by every dimension.** One `WeatherData`;
  `/weather` in the Nether changes the overworld's rain. Only levels whose
  dimension `Level.canHaveWeather` act on it.
- **Two `ServerLevel` tick counters that are not time.** *gameTime*
  advances only in the overworld (`ServerLevel.tickTime`), and the other
  levels read the overworld's; day time is not here at all.

## Where to look

`ServerLevel.tick` · `ServerLevel.tickChunk` · `ServerLevel.tickThunder` ·
`ServerLevel.runBlockEvents` · `ServerLevel.tickNonPassenger` ·
`ServerChunkCache.tick` · `ServerChunkCache.tickChunks` ·
`ServerChunkCache.broadcastChangedChunks` · `ChunkMap.collectSpawningChunks` ·
`ChunkMap.forEachBlockTickingChunk` · `ChunkMap.tick` · `DistanceManager` · `LevelTicks` ·
`NaturalSpawner` · `EntityTickList` · `PersistentEntitySectionManager` ·
`Level` (`Level.tickBlockEntities`, `Level.getBlockRandomPos`) · `WeatherData` ·
`ServerClockManager` · `SleepStatus` · `ChunkHolder.broadcastChanges`

---

*Rules: names, never code · how the system works, not how the code reads ·
newest version only · every backticked name passes `tools/verify_names.py`.*
