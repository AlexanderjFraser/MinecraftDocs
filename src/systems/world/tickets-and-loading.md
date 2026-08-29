# Tickets and loading

> Verified against **Minecraft 26.2** · Part IV · A player walks one block east across a chunk boundary, and a chunk eleven chunks away becomes a ticking part of the world.

## Responsibility

Nothing in the server asks "is this chunk loaded?" — it asks for a chunk at
a *level*, and the ticket system decides what that level means. A ticket is
a request for a chunk at some level of readiness; levels propagate outward
from each ticket, one per chunk of distance; and every chunk's level is the
minimum of everything reaching it. Below one threshold a chunk exists, below
another it is fully generated, below another it ticks blocks, and below the
last it ticks entities. Players, portals, ender pearls, the dragon and
`/forceload` are all just ticket sources.

The one sentence a player recognises: *render distance is how far you can
see; simulation distance is how far the world is alive — and they are two
different graphs.*

## The data it owns

- `TicketType` is a record — `TicketType.timeout` and `TicketType.flags` —
  registered in `BuiltInRegistries.TICKET_TYPE`. The flags say what a ticket
  *does*: `TicketType.FLAG_LOADING` (feeds the loading graph),
  `TicketType.FLAG_SIMULATION` (feeds the simulation graph),
  `TicketType.FLAG_PERSIST` (survives a restart),
  `TicketType.FLAG_KEEP_DIMENSION_ACTIVE` (stops the level's empty-tick
  countdown) and `TicketType.FLAG_CAN_EXPIRE_IF_UNLOADED`. There are exactly
  nine:

  | type | timeout | loading | simulation | persists | who adds it |
  |---|---:|---|---|---|---|
  | `TicketType.PLAYER_LOADING` | — | ✓ | | | `DistanceManager.PlayerTicketTracker`, one per chunk in view |
  | `TicketType.PLAYER_SIMULATION` | — | | ✓ | | `DistanceManager.addPlayer`, the player's chunk |
  | `TicketType.FORCED` | — | ✓ | ✓ | ✓ | `/forceload` via `TicketStorage.updateChunkForced` |
  | `TicketType.PORTAL` | 300 | ✓ | ✓ | ✓ | `Entity` on portal travel, radius 3 |
  | `TicketType.PLAYER_SPAWN` | 20 | ✓ | | | `PrepareSpawnTask` (configuration phase), radius 3 |
  | `TicketType.SPAWN_SEARCH` | 1 | ✓ | | | `PlayerSpawnFinder` |
  | `TicketType.ENDER_PEARL` | 40 | | ✓ | | `ServerPlayer`, the pearl's chunk, radius 2 |
  | `TicketType.DRAGON` | — | ✓ | ✓ | | `EnderDragonFight`, radius 9 |
  | `TicketType.UNKNOWN` | 1 | ✓ | | | every synchronous `ServerChunkCache.getChunk` |

- `Ticket` is a type, a `Ticket.ticketLevel` and `Ticket.ticksLeft`; identity
  is (type, level) — there is no key object and no owner. Re-adding an
  identical ticket `Ticket.resetTicksLeft`.
- `TicketStorage` (in `world/level`, not `server/level`) holds every ticket
  per chunk in `TicketStorage.tickets`. It **is `SavedData`** —
  `TicketStorage.TYPE` is the *chunk_tickets* file in the dimension's
  *data/* folder — and `TicketStorage.packTickets` writes only the types
  that `TicketType.persist`: forced and portal tickets come back after a
  restart, the rest evaporate. On shutdown
  `TicketStorage.deactivateTicketsOnClosing` parks everything except
  `TicketType.UNKNOWN` in `TicketStorage.deactivatedTickets`;
  `TicketStorage.activateAllDeactivatedTickets` replays them during
  `MinecraftServer.prepareLevels`.
- `ChunkLevel` is the number line. `ChunkLevel.byStatus` gives 31 for
  `FullChunkStatus.ENTITY_TICKING`, 32 for `FullChunkStatus.BLOCK_TICKING`,
  33 for `FullChunkStatus.FULL`. Above 33 a chunk is
  `FullChunkStatus.INACCESSIBLE` but still *generating*:
  `ChunkLevel.RADIUS_AROUND_FULL_CHUNK` is 11 (the neighbourhood the FULL
  step of `ChunkPyramid.GENERATION_PYRAMID` needs, computed, not written
  down), so `ChunkLevel.MAX_LEVEL` is 44 and `ChunkLevel.generationStatus`
  maps 34…44 onto ever-earlier `ChunkStatus`es. 45 means no holder.
- Two graphs, both `ChunkTracker`s — the chunk flavour of
  `DynamicGraphMinFixedPoint`, the same flood-fill the light engine uses,
  where a neighbour is level + 1 across the eight Chebyshev neighbours.
  `LoadingChunkTracker` (levels 0–45) decides which `ChunkHolder`s exist and
  how far they generate; `SimulationChunkTracker` (0–33) decides which of
  them tick. They are separate top-level classes, not inner classes.
- `DistanceManager` owns both graphs plus two player-radius trackers:
  `DistanceManager.naturalSpawnChunkCounter` (a
  `DistanceManager.FixedPlayerDistanceChunkTracker` of radius 8 — the mob
  spawning set) and `DistanceManager.playerTicketManager` (a
  `DistanceManager.PlayerTicketTracker` of radius `ChunkMap.MAX_VIEW_DISTANCE`,
  32). It also owns `DistanceManager.simulationDistance` (default 10),
  `DistanceManager.playersPerChunk`, `DistanceManager.chunksToUpdateFutures`,
  and `DistanceManager.ticketDispatcher`, a `ThrottlingChunkTaskDispatcher`
  that allows at most **four** player-view chunks to be loading at once.
- `ChunkHolder` (extends `GenerationChunkHolder`, the
  [next page](chunk-generation-pipeline.md)) carries three levels —
  `ChunkHolder.ticketLevel` (what the graph last said),
  `ChunkHolder.oldTicketLevel` (what the futures reflect) and
  `ChunkHolder.queueLevel` (the dispatcher's priority) — and three futures:
  `ChunkHolder.fullChunkFuture`, `ChunkHolder.tickingChunkFuture`,
  `ChunkHolder.entityTickingChunkFuture`, each a `ChunkResult` of
  `LevelChunk` defaulting to `ChunkHolder.UNLOADED_LEVEL_CHUNK_FUTURE`. It
  also collects the block and light changes that
  `ChunkHolder.broadcastChanges` sends ([the level tick](../server/server-level-tick.md)).
- `ChunkMap` keeps the holders in a pair of maps:
  `ChunkMap.updatingChunkMap`, mutated only on the server thread, and
  `ChunkMap.visibleChunkMap`, a volatile clone that
  `ChunkMap.promoteChunkMap` refreshes when `ChunkMap.modified` — workers
  and everyone else read the visible one. `ChunkMap.getUpdatingChunkIfPresent`
  still exists. Also `ChunkMap.toDrop`, `ChunkMap.pendingUnloads`,
  `ChunkMap.unloadQueue`, `ChunkMap.serverViewDistance` (clamped
  `ChunkMap.MIN_VIEW_DISTANCE` 2 … 32) and `ChunkMap.playerMap`.
- Per player: `ServerPlayer.requestedViewDistance` (from
  `ClientInformation.viewDistance`), `ServerPlayer.chunkTrackingView` (a
  `ChunkTrackingView.Positioned`, centre plus radius) and
  `ServerPlayer.lastSectionPos`. Server-wide: `PlayerList.viewDistance` and
  `PlayerList.simulationDistance`.
- `ServerChunkCache` is the level's `ChunkSource`: `ServerChunkCache.chunkMap`,
  `ServerChunkCache.distanceManager`, `ServerChunkCache.ticketStorage`, a
  four-entry cache (`ServerChunkCache.CACHE_SIZE`, `ServerChunkCache.lastChunk`),
  and `ServerChunkCache.mainThreadProcessor`, a
  `ServerChunkCache.MainThreadExecutor` — a `BlockableEventLoop` pinned to
  the server thread.

## When it runs

All of it on the **Server thread**, in three slots:

1. `ServerChunkCache.tick`, from the level tick: `TicketStorage.purgeStaleTickets`
   (countdowns; a timed ticket only counts down if it
   `TicketType.canExpireIfUnloaded` *or* its holder
   `ChunkHolder.isReadyForSaving`, so a portal ticket never expires under a
   chunk still loading), then `ServerChunkCache.runDistanceManagerUpdates`.
2. `ServerChunkCache.MainThreadExecutor.pollTask` — whenever the server
   thread idles (`MinecraftServer.pollTaskInternal` polls every level's
   chunk executor), it runs distance-manager updates *first*, then one
   light-engine schedule, then one queued task. Ticket propagation is not
   once per tick; it is whenever there is slack.
3. `ServerChunkCache.getChunk` from anywhere on the server thread: cache,
   then `ServerChunkCache.getChunkFutureMainThread` (adds a
   `TicketType.UNKNOWN` ticket, and if `ServerChunkCache.chunkAbsent` runs
   the distance updates synchronously so the holder exists *in this call*),
   then `BlockableEventLoop.managedBlock` until the future is done. The
   server thread never sleeps on a chunk: it runs chunk tasks while it
   waits. Off-thread callers are bounced to the main thread and joined.

The two `ChunkTracker` drains happen inside `DistanceManager.runAllUpdates`:
spawn counter, simulation tracker, player ticket tracker, loading tracker,
then `ChunkHolder.updateFutures` for every holder in
`DistanceManager.chunksToUpdateFutures`. The only worker-thread piece is
the throttled dispatcher that adds `TicketType.PLAYER_LOADING` tickets,
and it posts back to `DistanceManager.mainThreadExecutor`.

## The trace: a player walks east across a chunk boundary

View distance 10, simulation distance 10.

```mermaid
sequenceDiagram
    participant PL as ServerGamePacketListenerImpl
    participant CM as ChunkMap
    participant DM as DistanceManager
    participant TS as TicketStorage
    participant ST as SimulationChunkTracker
    participant PT as PlayerTicketTracker
    participant TD as ThrottlingChunkTaskDispatcher
    participant LT as LoadingChunkTracker
    participant CH as ChunkHolder
    participant PESM as PersistentEntitySectionManager
    participant PCS as PlayerChunkSender

    PL->>CM: move(player) — section changed?
    CM->>DM: removePlayer(old) · addPlayer(new)
    DM->>TS: removeTicket / addTicket PLAYER_SIMULATION, level 31 − 10
    TS->>ST: update(chunk, level) — queued, not propagated yet
    CM->>CM: updateChunkTracking → ClientboundSetChunkCacheCenterPacket; markChunkPendingToSend / dropChunk for the two crescents
    Note over DM: runAllUpdates (this tick, or the next idle pollTask)
    DM->>ST: runAllUpdates — the simulation graph is final now: entity range 10, block range 11
    DM->>PT: runAllUpdates — 21 chunks entered view, 21 left
    PT->>TD: submit(chunk, distance) — at most 4 in flight
    PT->>TS: removeTicket PLAYER_LOADING for the western column
    TD-->>TS: (worker → main) addTicket PLAYER_LOADING level 31
    TS->>LT: update(chunk, 31)
    DM->>LT: runDistanceUpdates → ChunkMap.updateChunkScheduling: new holders out to level 44
    DM->>CH: updateFutures — 45 → 31 crosses FULL, BLOCK_TICKING, ENTITY_TICKING
    CH->>CM: prepareAccessibleChunk · prepareTickingChunk · prepareEntityTickingChunk (the generation pipeline)
    CM->>CM: promoteChunkMap · clearCache
    CH-->>CM: (later) onFullChunkStatusChange FULL
    CM->>PESM: updateChunkStatus → entities TRACKED, entity data queued to load
    CH-->>CM: prepareTickingChunk continuation: postProcessGeneration, startTickingChunk, onChunkReadyToSend
    CM->>PCS: markChunkPendingToSend for every player whose view contains it
    CH-->>PESM: ENTITY_TICKING → startTicking → EntityTickList.add
    DM->>TD: release — the next view chunk may start
    PCS->>PL: sendNextChunks — batch start, ≤ quota chunks nearest first, batch finished
```

1. **The move.** `ServerGamePacketListenerImpl.handleMovePlayer` applies the
   position and calls `ServerChunkCache.move` → `ChunkMap.move`, which first
   updates every `ChunkMap.TrackedEntity` for this player and then compares
   `ServerPlayer.getLastSectionPos` with the new `SectionPos`. It changed:
   `ChunkMap.updatePlayerPos`, `DistanceManager.removePlayer` on the old
   section, `DistanceManager.addPlayer` on the new, `ChunkMap.updateChunkTracking`.
2. **The simulation ticket moves.** `DistanceManager.removePlayer` finds
   the old chunk's `DistanceManager.playersPerChunk` set empty, pokes both
   player trackers with "no player here" and removes the
   `TicketType.PLAYER_SIMULATION` ticket; `DistanceManager.addPlayer`
   mirrors it at `DistanceManager.getPlayerTicketLevel`, 31 − simulation
   distance = 21. `TicketStorage.addTicket` computes the new lowest level for
   each graph the ticket's flags name and calls the registered
   `TicketStorage.ChunkUpdated` listener; the tracker only *queues* the
   change.
3. **The view moves.** `ChunkMap.updateChunkTracking` builds a
   `ChunkTrackingView.of` the new centre; `ChunkMap.applyChunkTrackingView`
   sends `ClientboundSetChunkCacheCenterPacket` and walks
   `ChunkTrackingView.difference`: the eastern crescent gets
   `ChunkMap.markChunkPendingToSend` (which only marks if
   `ChunkMap.getChunkToSend` already has a ticking chunk — for fresh chunks
   it does not, yet), the western crescent gets `ChunkMap.dropChunk` →
   `PlayerChunkSender.dropChunk` → `ClientboundForgetLevelChunkPacket`. The
   view is a **disc**: `ChunkTrackingView.isWithinDistance` squares the
   distance, with a one-chunk buffer.
4. **The simulation graph settles first.** In `DistanceManager.runAllUpdates`,
   `SimulationChunkTracker.runAllUpdates` floods: level 31 out to distance
   10, 32 at 11, 33 (absent from `SimulationChunkTracker.chunks`) at 12; the
   west relaxes symmetrically. No futures, no IO. From this moment
   `DistanceManager.inEntityTickingRange` and
   `DistanceManager.inBlockTickingRange` answer differently — block ticking
   at the far western edge has already stopped.
5. **The view tickets are throttled.** `DistanceManager.PlayerTicketTracker.runAllUpdates`
   floods its own radius-32 graph. For each chunk newly inside
   `DistanceManager.PlayerTicketTracker.haveTicketFor` (distance ≤ view
   distance) `DistanceManager.PlayerTicketTracker.onLevelChange` submits a
   task to the `ThrottlingChunkTaskDispatcher`, priority = distance; for
   each chunk that left it releases the slot with a main-thread continuation
   that removes the `TicketType.PLAYER_LOADING` ticket. The dispatcher lets
   four through at a time; each runs on a worker and posts
   `TicketStorage.addTicket` at `DistanceManager.PLAYER_TICKET_LEVEL` (31)
   back to the main thread, recording the key in
   `DistanceManager.ticketsToRelease`.
6. **The loading graph creates holders.** `LoadingChunkTracker.runDistanceUpdates`
   floods from the new level-31 ticket: 31 at the chunk, 32 and 33 in the
   rings, then 34…44 eleven chunks further east. `LoadingChunkTracker.setLevel`
   → `ChunkMap.updateChunkScheduling` creates a `ChunkHolder` for every
   chunk whose level drops to ≤ 44 (or resurrects one from
   `ChunkMap.pendingUnloads`), and adds the holders whose level rose past 44
   to `ChunkMap.toDrop`. Every changed holder lands in
   `DistanceManager.chunksToUpdateFutures`.
7. **Futures are made.** For each of those, `GenerationChunkHolder.updateHighestAllowedStatus`
   then `ChunkHolder.updateFutures`, which compares `ChunkLevel.fullStatus`
   of the old and new level. Our chunk went 45 → 31, crossing all three
   thresholds upward: `ChunkHolder.fullChunkFuture` =
   `ChunkMap.prepareAccessibleChunk` (range 1, neighbours at
   `ChunkLevel.getStatusAroundFullChunk`), `ChunkHolder.tickingChunkFuture`
   = `ChunkMap.prepareTickingChunk` (range 1, all FULL),
   `ChunkHolder.entityTickingChunkFuture` = `ChunkMap.prepareEntityTickingChunk`
   (range 2, all FULL). Each is wrapped by `ChunkHolder.scheduleFullChunkPromotion`
   so that success fires `ChunkMap.onFullChunkStatusChange` on the main
   thread, and each is chained into `ChunkHolder.addSaveDependency` so the
   chunk cannot be saved or unloaded mid-promotion. Under the hood they all
   call `GenerationChunkHolder.scheduleChunkGenerationTask` — the
   [generation pipeline](chunk-generation-pipeline.md). Finally
   `ChunkMap.promoteChunkMap` publishes the new holders and
   `ServerChunkCache.clearCache`.
8. **FULL.** When the range future completes (a worker finished, or the
   region file was read), the promotion confirmation runs
   `ChunkMap.onFullChunkStatusChange` with `FullChunkStatus.FULL` →
   `PersistentEntitySectionManager.updateChunkStatus` →
   `Visibility.TRACKED`: the chunk's entities become visible and their
   entity data is queued to load (Part VI).
9. **BLOCK_TICKING.** `ChunkMap.prepareTickingChunk`'s main-thread
   continuation runs `LevelChunk.postProcessGeneration`,
   `ServerLevel.startTickingChunk` (which is `LevelChunk.unpackTicks` — the
   saved scheduled ticks become real), and, once `ChunkHolder.sendSync` is
   satisfied (the light engine has finished what
   `ChunkMap.waitForLightBeforeSending` registered),
   `ChunkMap.onChunkReadyToSend` → `PlayerChunkSender.markChunkPendingToSend`
   for every player whose view contains it.
10. **ENTITY_TICKING.** The third future completes →
    `PersistentEntitySectionManager.startTicking` →
    `ServerLevel.EntityCallbacks.onTickingStart` → `EntityTickList.add`.
    `DistanceManager.runAllUpdates` sees the entity-ticking future done for
    a key in `DistanceManager.ticketsToRelease` and releases the throttle
    slot: the next view chunk may start loading.
11. **Sending.** Once per tick, from `MinecraftServer.tickChildren`,
    `PlayerChunkSender.sendNextChunks`: if under the acknowledgement limit,
    accrue quota, `PlayerChunkSender.collectChunksToSend` nearest-first,
    then `ClientboundChunkBatchStartPacket`, up to the quota of
    `ClientboundLevelChunkWithLightPacket`, `ClientboundChunkBatchFinishedPacket`.
    The client answers `ServerboundChunkBatchReceivedPacket` with how many
    chunks per tick it wants (`PlayerChunkSender.onChunkBatchReceivedByClient`,
    clamped `PlayerChunkSender.MIN_CHUNKS_PER_TICK` 0.01 …
    `PlayerChunkSender.MAX_CHUNKS_PER_TICK` 64, starting at
    `PlayerChunkSender.START_CHUNKS_PER_TICK` 9). Only one batch may be
    unacknowledged until the first reply, then
    `PlayerChunkSender.MAX_UNACKNOWLEDGED_BATCHES`, 10.
12. **The west unloads.** The removed `TicketType.PLAYER_LOADING` tickets
    raise the western column past 44 → `ChunkMap.toDrop` →
    `ChunkHolder.updateFutures` completes the futures with
    `ChunkHolder.UNLOADED_LEVEL_CHUNK` and `ChunkHolder.demoteFullChunk`
    fires `FullChunkStatus.INACCESSIBLE` immediately → entities stop. The
    next `ChunkMap.tick` with the time supplier runs `ChunkMap.processUnloads`
    → `ChunkMap.scheduleUnload` → save and `ServerLevel.unload`
    ([chunk storage](chunk-storage.md)). There is no unload timeout.

## Interfaces

- **Called by:** `ServerLevel.tick` (via `ServerChunkCache.tick`);
  `MinecraftServer.pollTaskInternal`; every `ServerChunkCache.getChunk`;
  `ChunkMap.move` from the movement handler, teleports and
  `ServerPlayer.doTick`; `PlayerList.setViewDistance` /
  `PlayerList.setSimulationDistance` (broadcast
  `ClientboundSetChunkCacheRadiusPacket` / `ClientboundSetSimulationDistancePacket`
  and reach `ChunkMap.setServerViewDistance` / `DistanceManager.updateSimulationDistance`,
  which swaps every simulation ticket's level through
  `TicketStorage.replaceTicketLevelOfType`); `ForceLoadCommand` →
  `ServerLevel.setChunkForced` (a `TicketType.FORCED` ticket at
  `ChunkMap.FORCED_TICKET_LEVEL`, 31, loaded synchronously on add).
- **Calls into:** the generation pipeline (`GenerationChunkHolder`,
  `ChunkTaskDispatcher`), `PersistentEntitySectionManager.updateChunkStatus`
  (Part VI), `ThreadedLevelLightEngine` (lighting), `ChunkMap.processUnloads`
  (storage).
- **Crosses the network as:** `ClientboundSetChunkCacheCenterPacket` on
  every chunk-boundary crossing; `ClientboundSetChunkCacheRadiusPacket` and
  `ClientboundSetSimulationDistancePacket` on settings changes;
  `ClientboundChunkBatchStartPacket` / `ClientboundLevelChunkWithLightPacket`
  / `ClientboundChunkBatchFinishedPacket` outbound and
  `ServerboundChunkBatchReceivedPacket` inbound; `ClientboundForgetLevelChunkPacket`
  when a chunk leaves the view.
- **Data-driven by:** *view-distance* and *simulation-distance* in
  server.properties (`PlayerList`), the client's requested view distance,
  `GameRules.SPECTATORS_GENERATE_CHUNKS` (`ChunkMap.skipPlayer`), and the
  *chunk_tickets* saved data.

## Invariants and surprises

- **Two graphs, one store.** A chunk can be `FullChunkStatus.ENTITY_TICKING`
  by *holder* status — a `TicketType.PLAYER_LOADING` ticket puts it at
  level 31 — and yet tick nothing, because `ServerLevel.shouldTickBlocksAt`,
  the entity loop's `DistanceManager.inEntityTickingRange` check and
  `ChunkMap.forEachBlockTickingChunk` all consult the *simulation* graph.
  Render distance loads and generates; simulation distance is what is alive.
- **Player tickets are per chunk, throttled, and asynchronous.** There is
  no single "player ticket with a radius"; each chunk in view gets its own
  level-31 ticket, at most four are in flight, ordered by distance. Sprinting
  outruns the loader by design.
- **Tickets are saved data, and only two kinds persist.** `TicketStorage`
  replaced the forced-chunks file; `TicketType.FORCED` and `TicketType.PORTAL`
  come back after a restart (the portal one with its remaining
  `Ticket.ticksLeft`). There is no *LIGHT*, *PLAYER*, *START* or
  *POST_TELEPORT* ticket.
- **`TicketType.UNKNOWN` can expire before the chunk loads** (timeout 1,
  `TicketType.canExpireIfUnloaded`), which is why
  `ServerChunkCache.addTicketAndLoadWithRadius` refuses such types.
- **The server thread is never idle inside a chunk load.**
  `BlockableEventLoop.managedBlock` keeps draining chunk tasks and distance
  updates until the future resolves.
- **The view is a disc, and an unsent chunk is untracked.**
  `ChunkMap.isChunkTracked` is false while the chunk sits in
  `PlayerChunkSender.pendingChunks`, so block updates to a chunk the client
  has not received are simply not sent — the full chunk will carry them.
- **Unloading is immediate, and safe against re-loads.** A holder whose
  level passes 44 is scheduled the next `ChunkMap.tick`; if a ticket
  re-adopts it first, `ChunkMap.updateChunkScheduling` pulls it back out of
  `ChunkMap.pendingUnloads` and the unload task finds nothing to do.
- **`ChunkLevel.MAX_LEVEL` is derived, not declared.** It is 33 plus the
  radius the FULL step of the generation pyramid needs; change the pyramid
  and the loading radius changes with it.

## Where to look

`TicketType` · `TicketStorage.addTicket` · `TicketStorage.purgeStaleTickets` ·
`ChunkLevel.byStatus` · `ChunkLevel.fullStatus` · `DistanceManager.addPlayer` ·
`DistanceManager.runAllUpdates` · `DistanceManager.PlayerTicketTracker.onLevelChange` ·
`LoadingChunkTracker` · `SimulationChunkTracker` · `ChunkTracker.computeLevelFromNeighbor` ·
`ChunkMap.updateChunkScheduling` · `ChunkMap.move` · `ChunkMap.applyChunkTrackingView` ·
`ChunkMap.prepareTickingChunk` · `ChunkHolder.updateFutures` ·
`ChunkHolder.scheduleFullChunkPromotion` · `ServerChunkCache.getChunk` ·
`ServerChunkCache.getChunkFutureMainThread` · `ServerChunkCache.runDistanceManagerUpdates` ·
`ChunkTrackingView.difference` · `PlayerChunkSender.sendNextChunks`

---

*Rules: names, never code · how the system works, not how the code reads ·
newest version only · every backticked name passes `tools/verify_names.py`.*
