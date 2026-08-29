# Lighting

> Verified against **Minecraft 26.2** · Part IV · A torch is placed: the change is queued on the server thread, propagated on a worker, published as a copy-on-write map, and sent to the client as one packet of changed sections.

## Responsibility

Light is two independent 4-bit fields over every block — block light from
emitters, sky light from above — kept consistent as the world changes.
Every block change that could matter (`LightEngine.hasDifferentLightProperties`)
is queued; a serialised worker drains the queue, floods increases and
decreases through the neighbours, and publishes the result; the sections it
touched are what the clients are told about. Nothing about light is
computed on the server thread.

The one sentence a player recognises: *the torch lights up a tick later
than it is placed, and the mob-spawning darkness the F3 light values report.*

## The data it owns

- `LightLayer` — `LightLayer.SKY`, `LightLayer.BLOCK`. Every engine and
  storage is per layer.
- `LevelLightEngine` is the facade both sides hold: `LevelLightEngine.blockEngine`
  and `LevelLightEngine.skyEngine` (null where the `DimensionType` has no
  sky light), fanning out `LevelLightEngine.checkBlock`,
  `LevelLightEngine.updateSectionStatus`, `LevelLightEngine.setLightEnabled`,
  `LevelLightEngine.propagateLightSources`, `LevelLightEngine.runLightUpdates`
  and `LevelLightEngine.hasLightWork`. `LevelLightEngine.getLayerListener`
  is the read side (a `LayerLightEventListener`, or its
  `LayerLightEventListener.DummyLightLayerEventListener` for a missing
  layer); `LevelLightEngine.queueSectionData` and `LevelLightEngine.retainData`
  are how whole nibble arrays arrive from disk or the wire.
  `LevelLightEngine.getRawBrightness` is max(block, sky − darkening).
  Light has one section of padding above and below the world
  (`LevelLightEngine.LIGHT_SECTION_PADDING`; `LevelLightEngine.getLightSectionCount`
  is sections + 2).
- `LightEngine` is the algorithm, one per layer, reading through a
  `LightChunkGetter` (`ServerChunkCache` or `ClientChunkCache`;
  `LightChunkGetter.getChunkForLighting`, and the one outbound hook,
  `LightChunkGetter.onLightUpdate`). It owns `LightEngine.blockNodesToCheck`
  (positions whose properties changed — `LightEngine.checkBlock` only adds
  here), and two FIFO queues of packed long pairs,
  `LightEngine.increaseQueue` and `LightEngine.decreaseQueue`, whose second
  long is a `LightEngine.QueueEntry`: four level bits, six direction bits,
  `LightEngine.QueueEntry.FLAG_FROM_EMPTY_SHAPE` and
  `LightEngine.QueueEntry.FLAG_INCREASE_FROM_EMISSION`. `LightEngine.MAX_LEVEL`
  15, `LightEngine.MIN_OPACITY` 1, `LightEngine.PULL_LIGHT_IN_ENTRY` (a
  level-1 decrease in all directions meaning "re-pull from the neighbours").
  The block-side inputs are `BlockBehaviour.BlockStateBase.getLightEmission`,
  `BlockBehaviour.BlockStateBase.getLightDampening` (15 for a solid render,
  0 if `BlockBehaviour.BlockStateBase.propagatesSkylightDown`, else 1 —
  *getLightBlock* is gone), `BlockBehaviour.BlockStateBase.useShapeForLightOcclusion`
  and `BlockBehaviour.BlockStateBase.getFaceOcclusionShape`, through
  `LightEngine.getOpacity` and `LightEngine.shapeOccludes`.
- `BlockLightEngine` — `BlockLightEngine.checkNode` compares emission with
  the stored level and enqueues a decrease, a pull-in, and/or an emission
  increase; `BlockLightEngine.propagateIncrease` spreads level − opacity;
  `BlockLightEngine.propagateDecrease` zeroes dimmer neighbours and
  enqueues brighter ones as refills; `BlockLightEngine.propagateLightSources`
  scans a chunk with `LightChunk.findBlockLightSources` at generation.
- `SkyLightEngine` — the sky column model. Each chunk has a
  `ChunkSkyLightSources` (`ChunkAccess.skyLightSources`): 256 entries of
  "lowest Y that is a sky source", filled by `ChunkSkyLightSources.fillFrom`
  and updated per block by `ChunkSkyLightSources.update`; an edge is
  `ChunkSkyLightSources.isEdgeOccluded` if the lower block dampens or the
  face shapes occlude. `SkyLightEngine.checkNode` repairs the column
  (`SkyLightEngine.updateSourcesInColumn`, `SkyLightEngine.removeSourcesBelow`,
  `SkyLightEngine.addSourcesAbove`); `SkyLightEngine.propagateFromEmptySections`
  fills or clears whole all-air sections below at once when light crosses a
  section edge, because such sections have no data of their own;
  `SkyLightEngine.setLightEnabled` fills everything above the highest
  non-source with 15; `SkyLightEngine.propagateLightSources` seeds a fresh
  chunk from its own and its four neighbours' source tables.
- `LayerLightSectionStorage` is the store, and it is **double-buffered**:
  `LayerLightSectionStorage.updatingSectionData` (the engine's write copy)
  and `LayerLightSectionStorage.visibleSectionData` (volatile; what
  everyone else reads), both `DataLayerStorageMap`s. `LayerLightSectionStorage.setStoredLevel`
  clones a section's `DataLayer` on the first write of a batch
  (`DataLayerStorageMap.copyDataLayer`) and marks the section and its 26
  neighbours in `LayerLightSectionStorage.sectionsAffectedByLightUpdates`.
  `LayerLightSectionStorage.sectionStates` is a byte per section — a
  has-data bit and a 5-bit count of neighbours with data
  (`LayerLightSectionStorage.SectionState`); a section holds a `DataLayer`
  if it is non-empty *or* any of its 26 neighbours is.
  `LayerLightSectionStorage.queuedSections` is where outside data waits;
  `LayerLightSectionStorage.markNewInconsistencies` splices it in and
  `LayerLightSectionStorage.swapSectionMap` publishes a copy and fires
  `LightChunkGetter.onLightUpdate` once per affected section — **the only
  path out of the engine**. `SkyLightSectionStorage.getLightValue` walks
  *up* to the first section with data and answers 15 above the top;
  `SkyLightSectionStorage.createDataLayer` seeds a new section below
  existing data from the slice above (`SkyLightSectionStorage.repeatFirstLayer`).
- `DataLayer` — 16×16×16 nibbles in `DataLayer.SIZE` (2048) bytes, indexed
  `y ≪ 8 | z ≪ 4 | x`. **Lazily allocated**: `DataLayer.data` is null and
  `DataLayer.defaultValue` answers every read until the first `DataLayer.set`;
  `DataLayer.fill` de-allocates again. `DataLayer.isEmpty` means
  "homogeneous zero", which is what the packet's empty mask and the chunk
  saver test. There is no shared empty constant.
- `ThreadedLevelLightEngine` (server only) wraps the facade: every mutator
  becomes a `ThreadedLevelLightEngine.addTask` of
  `ThreadedLevelLightEngine.TaskType.PRE_UPDATE` or
  `ThreadedLevelLightEngine.TaskType.POST_UPDATE`, submitted through
  `ChunkMap.lightTaskDispatcher` at the chunk's queue level into
  `ThreadedLevelLightEngine.lightTasks`; `ThreadedLevelLightEngine.runUpdate`
  drains up to `ThreadedLevelLightEngine.taskPerBatch` (1000) of them
  around one `LevelLightEngine.runLightUpdates`. Calling
  `ThreadedLevelLightEngine.runLightUpdates` directly **throws**. It is
  `ChunkMap.lightEngine`, reached through `ServerChunkCache.getLightEngine`.
- On the client `ClientChunkCache.lightEngine` is a plain `LevelLightEngine`,
  and `ClientChunkCache.onLightUpdate` is `LevelExtractor.setSectionDirty`.

## When it runs

- **Server thread**, synchronously, inside `LevelChunk.setBlockState`
  ([chunk anatomy](chunk-anatomy.md)): if the section flipped between empty
  and non-empty, `LevelLightEngine.updateSectionStatus`; if
  `LightEngine.hasDifferentLightProperties`, `ChunkSkyLightSources.update`
  and then `LevelLightEngine.checkBlock` — which on the server merely queues
  a task. `ProtoChunk.setBlockState` does the same once the chunk is past
  `ChunkStatus.INITIALIZE_LIGHT`.
- **The light executor** — a `ConsecutiveExecutor` named *light* on the
  shared pool, one task at a time, no dedicated thread. The kick is
  `ThreadedLevelLightEngine.tryScheduleUpdate`, called from
  `ServerChunkCache.MainThreadExecutor.pollTask` whenever the server thread
  idles ([tickets](tickets-and-loading.md)), or inline when 1000 tasks
  have piled up.
- **In the generation pipeline**: `ChunkStatusTasks.initializeLight` →
  `ThreadedLevelLightEngine.initializeLight` (mark non-air sections, enable
  the column) and `ChunkStatusTasks.light` → `ThreadedLevelLightEngine.lightChunk`
  (propagate sources, then `ChunkAccess.setLightCorrect`); a chunk from
  disk with *isLightOn* skips the recompute. `ServerChunkCache.getChunkForLighting`
  hands the engine chunks at *FEATURES*, before the game may see them.
  `ChunkMap.waitForLightBeforeSending` makes `ThreadedLevelLightEngine.waitForPendingTasks`
  a send dependency so no chunk ships half-lit.
- **On unload**: `ThreadedLevelLightEngine.updateChunkStatus` disables the
  column and nulls its sections ([chunk storage](chunk-storage.md)); on
  load `SerializableChunkData.read` hands the saved `DataLayer`s in with
  `LevelLightEngine.retainData` and `LevelLightEngine.queueSectionData`.
- **Client**: `ClientLevel.update`, from `Minecraft.renderFrame` — **per
  frame, not per tick** — runs `ClientLevel.pollLightUpdates` (max(10,
  backlog ÷ 10) queued packet closures, all of them past a backlog of 1000)
  and then `LevelLightEngine.runLightUpdates` on the client's own engine.

## The trace: a torch is placed

```mermaid
sequenceDiagram
    participant LC as LevelChunk
    participant TLE as ThreadedLevelLightEngine
    participant TD as ChunkTaskDispatcher (light)
    participant MT as ServerChunkCache.MainThreadExecutor
    participant LE as BlockLightEngine (light executor)
    participant ST as LayerLightSectionStorage
    participant SCC as ServerChunkCache
    participant CH as ChunkHolder
    participant CPL as ClientPacketListener
    participant CL as ClientLevel

    LC->>LC: setBlockState — hasDifferentLightProperties(air, torch)? yes
    LC->>LC: ChunkSkyLightSources.update — column unchanged
    LC->>TLE: checkBlock(pos) — wrapped as a PRE_UPDATE task
    TLE->>TD: addTask → submit at the chunk's queue level
    TD->>TLE: lightTasks += (PRE_UPDATE, checkBlock)
    MT->>TLE: pollTask → tryScheduleUpdate → runUpdate on the light executor
    TLE->>LE: PRE tasks: LightEngine.checkBlock → blockNodesToCheck
    TLE->>LE: LevelLightEngine.runLightUpdates
    LE->>LE: checkNode: emission 14 > stored → enqueue PULL_LIGHT_IN_ENTRY, increaseLightFromEmission(14)
    LE->>LE: propagateDecreases (refill entries only)
    LE->>ST: propagateIncreases: setStoredLevel 14, 13, 12 … copy-on-write per section; section + 26 neighbours affected
    LE->>ST: markNewInconsistencies · swapSectionMap → visibleSectionData = copy
    ST->>SCC: onLightUpdate(BLOCK, section) per affected section
    SCC->>MT: execute → ChunkHolder.sectionLightChanged
    MT->>CH: blockChangedLightSectionFilter bit set · holder joins chunkHoldersToBroadcast
    SCC->>CH: (end of tick) broadcastChangedChunks → broadcastChanges
    CH->>CPL: ClientboundLightUpdatePacket — changed sections' 2048 bytes, empty mask for the rest
    CPL->>CL: handleLightUpdatePacket → queueLightUpdate
    CL->>CL: (next frame) update → pollLightUpdates → applyLightData → queueSectionData · setSectionDirtyWithNeighbors
    CL->>CL: runLightUpdates → swapSectionMap → LevelExtractor.setSectionDirty → remesh
```

1. **The block write.** `Level.setBlock` → `LevelChunk.setBlockState`. The
   section was not empty, so no status change. `LightEngine.hasDifferentLightProperties`
   (emission 0 → 14) is true → `ChunkSkyLightSources.update` runs
   synchronously on the chunk (a torch dampens nothing and occludes
   nothing, so the column's lowest source is unchanged) →
   `ThreadedLevelLightEngine.checkBlock`, which wraps the facade call in a
   *PRE_UPDATE* runnable and `ThreadedLevelLightEngine.addTask`s it. The
   server thread is done with light. `Level.setBlock` goes on to
   `ServerLevel.sendBlockUpdated` → `ChunkHolder.blockChanged` — the block
   packet is a separate matter.
2. **Dispatch.** `ChunkTaskDispatcher.submit` queues the task under the
   chunk's ticket level; when popped, it appends to
   `ThreadedLevelLightEngine.lightTasks`.
3. **Trigger.** The next time the server thread idles,
   `ServerChunkCache.MainThreadExecutor.pollTask` calls
   `ThreadedLevelLightEngine.tryScheduleUpdate`; `ThreadedLevelLightEngine.scheduled`
   flips and `ThreadedLevelLightEngine.runUpdate` goes to the light executor.
4. **The engine runs**, on a pool thread, serialised. PRE tasks first:
   `LightEngine.checkBlock` adds the position to `LightEngine.blockNodesToCheck`
   of both engines. Then `LevelLightEngine.runLightUpdates`, block layer
   first. `BlockLightEngine.checkNode`: emission 14 exceeds the stored
   level, so `LightEngine.enqueueDecrease` with `LightEngine.PULL_LIGHT_IN_ENTRY`
   and `LightEngine.enqueueIncrease` with
   `LightEngine.QueueEntry.increaseLightFromEmission`. `LightEngine.propagateDecreases`
   drains first: the pull-in entry finds brighter neighbours and enqueues
   "increase only back toward me" refills. `LightEngine.propagateIncreases`
   then sets the torch node to 14 through `LayerLightSectionStorage.setStoredLevel`
   — the first write to that section this batch clones its `DataLayer`, and
   the section and its 26 neighbours join the affected set — and
   `BlockLightEngine.propagateIncrease` floods 13, 12, … through air
   (opacity 1), stopping at level 1 or at occluders. The sky engine's
   `SkyLightEngine.checkNode` finds the column unchanged and gives the node
   a pull-in that changes nothing. `LayerLightSectionStorage.markNewInconsistencies`
   (nothing queued), then `LayerLightSectionStorage.swapSectionMap`: the
   updating map is copied into `LayerLightSectionStorage.visibleSectionData`
   and `ServerChunkCache.onLightUpdate` fires for each affected section —
   up to 27, across up to 9 holders.
5. **Back to the server thread.** Each `ServerChunkCache.onLightUpdate` is
   posted to `ServerChunkCache.mainThreadProcessor`; there it runs
   `ChunkHolder.sectionLightChanged`, setting a bit in
   `ChunkHolder.blockChangedLightSectionFilter` (or
   `ChunkHolder.skyChangedLightSectionFilter`) and adding the holder to
   `ServerChunkCache.chunkHoldersToBroadcast`. `ChunkHolder.sectionLightChanged`
   also `ChunkAccess.markUnsaved` — light is saved data.
6. **The packet.** At the end of `ServerChunkCache.tick`,
   `ServerChunkCache.broadcastChangedChunks` → `ChunkHolder.broadcastChanges`
   ([the level tick](../server/server-level-tick.md)): with either filter
   non-empty it builds one `ClientboundLightUpdatePacket` whose
   `ClientboundLightUpdatePacketData` has a sky and a block mask, an empty
   mask for each (a `DataLayer.isEmpty` section costs one bit, not 2048
   bytes), and the changed sections' bytes from
   `LayerLightEventListener.getDataLayerData` — queued-or-visible, never the
   updating copy. It goes to `ChunkHolder.PlayerProvider.getPlayers` with
   border players included. Filters cleared. The block packet follows.
7. **The client.** `ClientPacketListener.handleLightUpdatePacket` pushes a
   closure onto `ClientLevel.lightUpdateQueue`. Next frame, `ClientLevel.update`
   → `ClientLevel.pollLightUpdates` runs it: `ClientPacketListener.applyLightData`
   → `ClientPacketListener.readSectionList` per layer →
   `LevelLightEngine.queueSectionData` with a cloned `DataLayer` (or an
   empty one for masked sections), and `ClientLevel.setSectionDirtyWithNeighbors`
   → `LevelExtractor.setSectionRangeDirty` → `SectionUpdateTracker.setDirty`.
   Then `LevelLightEngine.runLightUpdates` on the client's own engine:
   `LayerLightSectionStorage.markNewInconsistencies` splices the layers in,
   `LayerLightSectionStorage.swapSectionMap` publishes and
   `ClientChunkCache.onLightUpdate` marks the section dirty again. The
   mesher reads the new values on rebuild (Part X). The client had already
   run its own `LevelLightEngine.checkBlock` when it placed the torch
   locally — the packet mostly confirms.

## Interfaces

- **Called by:** `LevelChunk.setBlockState` and `ProtoChunk.setBlockState`
  (the only runtime sources of *checkBlock*), `ChunkStatusTasks.initializeLight`
  / `ChunkStatusTasks.light` ([the generation pipeline](chunk-generation-pipeline.md)),
  `ChunkMap.scheduleUnload`, `SerializableChunkData.read`,
  `ServerChunkCache.MainThreadExecutor.pollTask`; on the client
  `ClientPacketListener.handleLightUpdatePacket`,
  `ClientPacketListener.handleLevelChunkWithLight` (which applies the
  initial light with rebuild off, then `ClientPacketListener.enableChunkLight`),
  `ClientPacketListener.queueLightRemoval` on `ClientboundForgetLevelChunkPacket`.
- **Calls into:** `LightChunk` (`ChunkAccess`) for block states and sources;
  `LightChunkGetter.onLightUpdate` → `ServerChunkCache.onLightUpdate` /
  `ClientChunkCache.onLightUpdate`. Readers: `BlockAndLightGetter.getBrightness`,
  `BlockAndLightGetter.getRawBrightness`, `LevelReader.getMaxLocalRawBrightness`
  (minus `LevelReader.getSkyDarken`), `BlockAndLightGetter.canSeeSky`
  (sky ≥ 15); `SerializableChunkData.copyOf` for saving.
- **Crosses the network as:** `ClientboundLightUpdatePacket` for changes,
  and the same `ClientboundLightUpdatePacketData` inside
  `ClientboundLevelChunkWithLightPacket` with both filters null — every
  section — when a chunk is first sent (`PlayerChunkSender.sendChunk`).
- **Data-driven by:** `DimensionType.hasSkyLight` (whether a sky engine
  exists), and `BlockBehaviour.Properties.lightLevel` per block
  (`Blocks.TORCH` is 14).

## Invariants and surprises

- **There is no light thread.** The work runs on the shared pool through a
  one-at-a-time `ConsecutiveExecutor`; the kick comes from the server
  thread's idle loop, not from the level tick; and
  `ThreadedLevelLightEngine.runLightUpdates` throws if called.
- **Sky light does not use the heightmaps.** `ChunkSkyLightSources` is its
  own 256-entry "lowest source Y" table, and sections above the top data
  section have no `DataLayer` at all — reads walk up and answer 15.
- **`DataLayer` is lazy**, and "empty" means homogeneous zero. A section of
  air above ground costs no bytes on disk or the wire.
- **The engine never touches a `ChunkHolder`.** Its only exit is
  `LightChunkGetter.onLightUpdate` from the map swap, and every write
  dirties the section plus all 26 neighbours — one torch marks up to 27
  sections in up to 9 holders for re-send.
- **Decreases always finish before increases** in a batch, and the
  published map is a copy: readers on other threads never see a
  half-propagated state.
- **The client lights per frame**, and rate-limits packet application; a
  flood of light packets is applied over several frames.
- **Vocabulary**: *getLightBlock* is `BlockBehaviour.BlockStateBase.getLightDampening`;
  *LightTexture* is `Lightmap` (Part X). `DynamicGraphMinFixedPoint`,
  `LeveledPriorityQueue` and `SpatialLongSet` still live in
  `world/level/lighting` but the light engine no longer uses them — they
  serve `ChunkTracker` and `SectionTracker` ([tickets](tickets-and-loading.md)).

## Where to look

`LightEngine.runLightUpdates` · `LightEngine.QueueEntry` · `BlockLightEngine.checkNode` ·
`BlockLightEngine.propagateIncrease` · `SkyLightEngine.checkNode` ·
`SkyLightEngine.propagateFromEmptySections` · `ChunkSkyLightSources.update` ·
`LayerLightSectionStorage.setStoredLevel` · `LayerLightSectionStorage.swapSectionMap` ·
`SkyLightSectionStorage.getLightValue` · `DataLayer` · `ThreadedLevelLightEngine.addTask` ·
`ThreadedLevelLightEngine.runUpdate` · `ThreadedLevelLightEngine.tryScheduleUpdate` ·
`ThreadedLevelLightEngine.lightChunk` · `ServerChunkCache.onLightUpdate` ·
`ChunkHolder.sectionLightChanged` · `ChunkHolder.broadcastChanges` ·
`ClientboundLightUpdatePacketData` · `ClientPacketListener.applyLightData` ·
`ClientLevel.update` · `LevelChunk.setBlockState`

---

*Rules: names, never code · how the system works, not how the code reads ·
newest version only · every backticked name passes `tools/verify_names.py`.*
