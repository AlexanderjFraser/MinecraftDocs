# The chunk generation pipeline

> Verified against **Minecraft 26.2** · Part IV · One chunk from *EMPTY* to *FULL*: the twelve statuses, the two pyramids that say which neighbours each step needs, the task that walks them a layer at a time, and the one step that runs on the server thread.

## Responsibility

A chunk is not generated in one go. It is raised through twelve
`ChunkStatus`es, and each step may read — and sometimes write — its
neighbours at an *earlier* status, which is why asking for one finished
chunk quietly asks for a 23×23 square of partly-finished ones. The pipeline
is the machinery that keeps that square consistent: which step needs what,
who has already started it, and which thread it may run on. The terrain
itself — noise, surface, carvers, features, structures — is Part XI; this
page is about the conveyor, not what rides on it.

The one sentence a player recognises: *the ring of half-made chunks beyond
render distance, and why "generating" is never one chunk at a time.*

## The data it owns

- **`ChunkStatus`** is inert: a registry entry (`BuiltInRegistries.CHUNK_STATUS`)
  with `ChunkStatus.getIndex`, `ChunkStatus.getParent`, a `ChunkType`
  (`ChunkType.PROTOCHUNK` for all but the last, `ChunkType.LEVELCHUNK` for
  `ChunkStatus.FULL`) and `ChunkStatus.heightmapsAfter`. No task, no radius.
  Twelve, in order: `ChunkStatus.EMPTY`, `ChunkStatus.STRUCTURE_STARTS`,
  `ChunkStatus.STRUCTURE_REFERENCES`, `ChunkStatus.BIOMES`,
  `ChunkStatus.NOISE`, `ChunkStatus.SURFACE`, `ChunkStatus.CARVERS`,
  `ChunkStatus.FEATURES`, `ChunkStatus.INITIALIZE_LIGHT`, `ChunkStatus.LIGHT`,
  `ChunkStatus.SPAWN`, `ChunkStatus.FULL`. `ChunkStatus.MAX_STRUCTURE_DISTANCE`
  (8) is declared but dead — the pyramid writes the literal.
- **`ChunkPyramid`** is where the work lives: a list of `ChunkStep`s, one per
  status, each with `ChunkStep.targetStatus`, `ChunkStep.directDependencies`
  and `ChunkStep.accumulatedDependencies` (both `ChunkDependencies`: the
  status required at each Chebyshev distance, and the inverse
  `ChunkDependencies.getRadiusOf`), `ChunkStep.blockStateWriteRadius`, and
  `ChunkStep.task`. There are **two** pyramids. `ChunkPyramid.GENERATION_PYRAMID`
  does the work; `ChunkPyramid.LOADING_PYRAMID` is used when the chunk and
  its ring are already on disk at or past the target — every step is
  `ChunkStatusTasks.passThrough` except `ChunkStatusTasks.loadStructureStarts`,
  `ChunkStatusTasks.initializeLight`, `ChunkStatusTasks.light` and
  `ChunkStatusTasks.full`. A loaded chunk still walks all twelve steps and
  still needs its 3×3 ring for *LIGHT*.

  The generation pyramid's direct requirements, as declared:

  | step | needs | writes |
  |---|---|---|
  | *STRUCTURE_STARTS* | — | — |
  | *STRUCTURE_REFERENCES*, *BIOMES*, *CARVERS* | *STRUCTURE_STARTS* within 8 | (carvers: 0) |
  | *NOISE*, *SURFACE* | *BIOMES* within 1, *STRUCTURE_STARTS* to 8 | 0 |
  | *FEATURES* | *CARVERS* within 1, *STRUCTURE_STARTS* to 8 | **1** |
  | *LIGHT* | *INITIALIZE_LIGHT* within 1 | — |
  | *SPAWN* | *LIGHT* at 0, *BIOMES* within 1 | — |

  Accumulated, the FULL step needs *SPAWN* at distance 0, *INITIALIZE_LIGHT*
  at 1, *CARVERS* at 2, *BIOMES* at 3 and *STRUCTURE_STARTS* from 4 to 11 —
  radius **11**, and that number is `ChunkLevel.RADIUS_AROUND_FULL_CHUNK`,
  the reason `ChunkLevel.MAX_LEVEL` is 44 ([tickets](tickets-and-loading.md)).
- **`ChunkStatusTasks`** are the step bodies, each a `ChunkStatusTask`
  taking a `WorldGenContext` (`WorldGenContext.level`, `WorldGenContext.generator`,
  `WorldGenContext.structureManager`, `WorldGenContext.lightEngine`,
  `WorldGenContext.mainThreadExecutor`, `WorldGenContext.unsavedListener` —
  built once as `ChunkMap.worldGenContext`), the step, a `StaticCache2D` of
  holders and the chunk. `ChunkStep.apply` runs the task and, if the chunk's
  persisted status was below the target, `ChunkStep.completeChunkGeneration`
  bumps `ProtoChunk.setPersistedStatus`.
- **`GenerationChunkHolder`** is the per-chunk generation state, all
  atomics because workers and the server thread both touch it:
  `GenerationChunkHolder.futures` (one `ChunkResult` future per status),
  `GenerationChunkHolder.startedWork` (the highest status whose step has
  been *started*; `GenerationChunkHolder.acquireStatusBump` is a CAS, so
  exactly one caller runs a step and everyone else gets the future),
  `GenerationChunkHolder.highestAllowedStatus` (the ticket-derived ceiling,
  `ChunkLevel.generationStatus`; `GenerationChunkHolder.isStatusDisallowed`
  gates every request), `GenerationChunkHolder.task` (the one
  `ChunkGenerationTask` in flight) and `GenerationChunkHolder.generationRefCount`
  (while any task's cache holds this holder, `GenerationChunkHolder.generationSaveSyncFuture`
  keeps it from being saved or unloaded). Three statuses to keep apart:
  *persisted* (`GenerationChunkHolder.getPersistedStatus`, what the chunk
  object reports), *highest allowed* (the ceiling), *target* (what a caller
  asked for).
- **`ChunkGenerationTask`** — one per (holder, target): `ChunkGenerationTask.targetStatus`,
  `ChunkGenerationTask.scheduledStatus`, `ChunkGenerationTask.scheduledLayer`
  (the futures of the layer in flight), `ChunkGenerationTask.needsGeneration`,
  `ChunkGenerationTask.markedForCancellation`, and `ChunkGenerationTask.cache`,
  a `StaticCache2D` of the worst-case radius (11 for FULL: **529 holders**),
  each `ChunkMap.acquireGeneration`d on creation.
- **The executors.** `ChunkMap` builds two `ConsecutiveExecutor`s on the
  shared pool, named *worldgen* and *light*, each behind a
  `ChunkTaskDispatcher` (`ChunkMap.worldgenTaskDispatcher`,
  `ChunkMap.lightTaskDispatcher`). A `ConsecutiveExecutor` runs **one task
  at a time**, on whichever `Worker-Main-n` picks it up
  (`AbstractConsecutiveExecutor.run` pops one and re-registers itself). The
  dispatcher owns a `ChunkTaskPriorityQueue` of
  `ChunkTaskPriorityQueue.PRIORITY_LEVEL_COUNT` (46) buckets keyed by the
  holder's queue level — closer to a player runs first — and hands one
  chunk's batch to the executor at a time (`ChunkTaskDispatcher.scheduleForExecution`).
  The pool itself is `Util.backgroundExecutor`, sized
  `Util.maxAllowedExecutorThreads` (cores − 1, capped by the
  *max.bg.threads* property, `Util.DEFAULT_MAX_THREADS` 255). There is no
  generation thread count setting.
- **`WorldGenRegion`** is the worker's view of the world: built per task
  with the cache, the step and the centre; `WorldGenRegion.getChunk` serves
  a neighbour only if its distance is inside `ChunkStep.directDependencies`
  *and* the requested status is at most what that distance guarantees —
  otherwise "Requested chunk unavailable during world generation".
  `WorldGenRegion.ensureCanWrite` limits writes to `WorldGenRegion.writeRadius`
  and `WorldGenRegion.warnIfReadOutsideWriteZone` logs unsafe terrain reads.
  `WorldGenRegion.currentlyGenerating` names the feature for crash reports.

## When it runs

Three threads, and it matters which:

- **Server thread**: everything that starts and finishes a chunk.
  `GenerationChunkHolder.scheduleChunkGenerationTask` (from `ChunkHolder.updateFutures`
  via `ChunkMap.getChunkRangeFuture`, or from `ServerChunkCache.getChunkFutureMainThread`),
  `ChunkMap.runGenerationTasks` at the end of every
  `ServerChunkCache.runDistanceManagerUpdates`, `SerializableChunkData.read`
  (NBT → chunk object — on the main thread, not the pool), and
  `ChunkStatusTasks.full`.
- **The *worldgen* executor** (one worker at a time per dimension):
  `ChunkGenerationTask.runUntilWait` and, inline within it, every step
  except the three that fork: structure starts and references, surface,
  carvers, features, spawn. Only `NoiseBasedChunkGenerator.createBiomes`
  and `NoiseBasedChunkGenerator.fillFromNoise` fan out to the pool
  (`Util.backgroundExecutor` under the names *init_biomes* and
  `NoiseBasedChunkGenerator.doFill`).
- **The *light* executor**: `ChunkStatusTasks.initializeLight` and
  `ChunkStatusTasks.light` hand the chunk to `ThreadedLevelLightEngine.initializeLight`
  / `ThreadedLevelLightEngine.lightChunk` ([lighting](lighting.md)).
- **The pool** also runs the disk path's `SerializableChunkData.parse`
  (*parseChunk*) and the DataFixer upgrade (*upgradeChunk*); the region
  read is on the IO lane ([chunk storage](chunk-storage.md)).

Parallelism comes from the *wait*: `ChunkGenerationTask.runUntilWait`
returns as soon as a layer has an unfinished future, `ChunkMap.runGenerationTask`
chains a resubmit onto that future, and the executor moves on to another
chunk's task. No thread ever blocks on a neighbour.

## The trace: one chunk from EMPTY to FULL

```mermaid
sequenceDiagram
    participant DM as DistanceManager
    participant CH as ChunkHolder / GenerationChunkHolder
    participant CM as ChunkMap
    participant TD as ChunkTaskDispatcher (worldgen)
    participant GT as ChunkGenerationTask
    participant ST as ChunkStatusTasks
    participant CG as ChunkGenerator (pool)
    participant LE as ThreadedLevelLightEngine
    participant SCD as SerializableChunkData
    participant MT as main thread

    DM->>CH: updateHighestAllowedStatus · updateFutures → prepareAccessibleChunk
    CH->>CH: scheduleChunkGenerationTask(FULL) — no task yet
    CH->>CM: scheduleGenerationTask → ChunkGenerationTask.create: StaticCache2D radius 11, acquireGeneration ×529
    CM->>TD: runGenerationTasks → submit(runUntilWait, queue level)
    TD->>GT: runUntilWait (worldgen executor)
    GT->>CH: layer EMPTY, loading radius 1: applyStep → acquireStatusBump
    CH->>CM: applyStep(EMPTY) → scheduleChunkLoad
    CM->>SCD: read region → upgrade (pool) → parse (pool)
    SCD->>MT: SerializableChunkData.read → ProtoChunk / ImposterProtoChunk / empty
    GT-->>TD: wait — futures pending; resubmit on completion
    TD->>GT: runUntilWait — canLoadWithoutGeneration? no → EMPTY again at radius 11
    GT->>ST: STRUCTURE_STARTS at radius 11 — createStructures, inline
    GT->>ST: STRUCTURE_REFERENCES, BIOMES at radius 3
    ST->>CG: createBiomes — forks to the pool
    GT->>ST: NOISE at radius 2
    ST->>CG: fillFromNoise — forks to the pool
    GT->>ST: SURFACE, CARVERS at radius 2 — inline, write radius 0
    GT->>ST: FEATURES at radius 1 — inline, write radius 1
    GT->>ST: INITIALIZE_LIGHT at 1, LIGHT at 0
    ST->>LE: initializeLight · lightChunk (light executor)
    GT->>ST: SPAWN at 0 — spawnOriginalMobs
    GT->>ST: FULL at 0
    ST->>MT: supplyAsync on the main-thread executor
    MT->>CH: new LevelChunk from the proto · replaceProtoChunk(ImposterProtoChunk) · setLoaded · registerAllBlockEntitiesAfterLevelLoad · registerTickContainerInLevel
    CH->>CH: completeFuture(FULL)
    GT->>CM: releaseClaim → releaseGeneration ×529
    CH-->>DM: (later) promotion confirmed → onFullChunkStatusChange
```

1. **A ticket, a ceiling, a request.** A level ≤ 33 reaches the chunk
   ([tickets](tickets-and-loading.md)). `DistanceManager.runAllUpdates`
   gives every touched holder `GenerationChunkHolder.updateHighestAllowedStatus`
   (33 → *FULL*, 34 → *SPAWN*, … 36 → *BIOMES*, 37–44 → *STRUCTURE_STARTS*)
   and `ChunkHolder.updateFutures`, which crosses `FullChunkStatus.FULL` and
   calls `ChunkMap.prepareAccessibleChunk` → `ChunkMap.getChunkRangeFuture`
   → `GenerationChunkHolder.scheduleChunkGenerationTask` with *FULL* on the
   centre and `ChunkLevel.getStatusAroundFullChunk` on the ring.
2. **The task is made.** No task exists, so `GenerationChunkHolder.rescheduleChunkTask`
   → `ChunkMap.scheduleGenerationTask` → `ChunkGenerationTask.create`: the
   `StaticCache2D` of radius 11 is filled from `ChunkMap.acquireGeneration`
   (every holder's ref-count goes up — none of the 529 can be unloaded
   now). It waits in `ChunkMap.pendingGenerationTasks` until
   `ChunkMap.runGenerationTasks`, at the end of the same update, submits
   `ChunkGenerationTask.runUntilWait` to the worldgen dispatcher at the
   holder's queue level.
3. **Dispatch.** `ChunkTaskDispatcher.submit` buckets it; `ChunkTaskDispatcher.pollTask`
   pops the lowest level and `ChunkTaskDispatcher.scheduleForExecution` hands
   the chunk's runnables to the worldgen `ConsecutiveExecutor`, which runs
   them one at a time on a pool thread.
4. **Layer *EMPTY*, loading radius.** `ChunkGenerationTask.scheduleNextLayer`
   always starts with *EMPTY* at the *loading* pyramid's radius, 1. For the
   3×3, `GenerationChunkHolder.applyStep` CASes *startedWork* and
   `ChunkMap.applyStep` turns *EMPTY* into `ChunkMap.scheduleChunkLoad`: a
   region read, `ChunkMap.upgradeChunkTag` on the pool, `SerializableChunkData.parse`
   on the pool, and `SerializableChunkData.read` **on the main thread** —
   a `ProtoChunk` with the saved status, an `ImposterProtoChunk` over a
   `LevelChunk` if the file was *FULL*, or `ChunkMap.createEmptyChunk` if
   there was no file. The futures are not done, so *runUntilWait* returns
   the last one and the task is re-entered when it completes.
5. **Load or generate?** `ChunkGenerationTask.canLoadWithoutGeneration`
   checks the centre's persisted status against the target and the 3×3
   against `ChunkPyramid.LOADING_PYRAMID`. If yes, the cheap path: eleven
   pass-through layers at radius ≤ 1, `ChunkStatusTasks.loadStructureStarts`
   to feed `StructureCheck`, light with *lighted* true (`ChunkStatusTasks.isLighted`:
   persisted ≥ *LIGHT* and `ChunkAccess.isLightCorrect` — the engine only
   re-enables, it does not recompute), and *full*. If no,
   `ChunkGenerationTask.needsGeneration` is set and *EMPTY* is rescheduled
   at the *generation* radius, 11: up to 529 disk reads, most returning
   "no file" and an empty proto chunk quickly.
6. ***STRUCTURE_STARTS* at radius 11**, inline on the worldgen executor for
   every chunk not already past it: `ChunkGenerator.createStructures`
   decides which structures *start* in each chunk — it needs only the seed
   and the placement state (`ChunkGeneratorStructureState`). Then
   `ServerLevel.onStructureStartsAvailable`.
7. ***STRUCTURE_REFERENCES* and *BIOMES* at radius 3.** References
   (`ChunkGenerator.createReferences`) record which starts within 8 chunks
   touch each chunk — the reason starts needed radius 8 around *it*. Biomes
   fork: `ChunkGenerator.createBiomes` → `NoiseBasedChunkGenerator.createBiomes`
   on the pool; the task waits.
8. ***NOISE* at radius 2.** `ChunkGenerator.fillFromNoise` forks to the pool
   (`NoiseBasedChunkGenerator.doFill`); on completion the below-zero
   retrogen bedrock fix-ups (`BelowZeroRetrogen.replaceOldBedrock`,
   `BelowZeroRetrogen.applyBedrockMask`) if the chunk is being deepened.
9. ***SURFACE* and *CARVERS* at radius 2**, inline, write radius 0.
   `ChunkGenerator.buildSurface`; then `Blender.addAroundOldChunksCarvingMaskFilter`
   and `ChunkGenerator.applyCarvers`. Neighbour reads are policed by the
   direct dependencies.
10. ***FEATURES* at radius 1**, inline, **write radius 1** — a tree may
    cross into a neighbour, and the neighbour is only at *CARVERS*, so
    nobody else is writing it. `Heightmap.primeHeightmaps` for the four
    final heightmaps first, then `ChunkGenerator.applyBiomeDecoration`,
    then `Blender.generateBorderTicks`. Note the write into a neighbour
    goes through `LevelChunkSection.acquire` and the unchecked setter
    ([chunk anatomy](chunk-anatomy.md)).
11. **Light.** `ChunkStatusTasks.initializeLight` at radius 1 —
    `ChunkAccess.initializeLightSources`, `ProtoChunk.setLightEngine` (from
    now on the proto forwards block changes to the engine),
    `ThreadedLevelLightEngine.initializeLight` — then `ChunkStatusTasks.light`
    at radius 0 → `ThreadedLevelLightEngine.lightChunk`. Both run on the
    light executor; the task waits on the returned future.
12. ***SPAWN* at radius 0**: `ChunkGenerator.spawnOriginalMobs` through the
    `WorldGenRegion`, skipped for a chunk that `ChunkAccess.isUpgrading`.
13. ***FULL* — on the main thread.** `ChunkStatusTasks.full` is scheduled
    like every other step but does its work through
    *supplyAsync* on `WorldGenContext.mainThreadExecutor`:
    a `LevelChunk` is built from the proto (sharing its sections);
    `GenerationChunkHolder.replaceProtoChunk` rewrites slots 0–10 to an
    `ImposterProtoChunk` with writes disallowed; `LevelChunk.setFullStatus`
    is wired to the holder; `LevelChunk.runPostLoad` turns
    `ProtoChunk.getEntities` into entities via `ChunkStatusTasks.postLoadProtoChunk`
    and `ServerLevel.addWorldGenChunkEntities`; `LevelChunk.setLoaded`;
    `LevelChunk.registerAllBlockEntitiesAfterLevelLoad`;
    `LevelChunk.registerTickContainerInLevel`; `LevelChunk.setUnsavedListener`.
    `GenerationChunkHolder.completeFuture` for *FULL*.
14. **Release.** *runUntilWait* sees the scheduled status equal the target
    and calls `ChunkGenerationTask.releaseClaim`: `GenerationChunkHolder.removeTask`,
    then `ChunkMap.releaseGeneration` on all 529 holders. The ring's
    partial chunks are now free to be saved or dropped as their tickets
    dictate. Later, `ChunkHolder.scheduleFullChunkPromotion` confirms on
    the main thread and `ChunkMap.onFullChunkStatusChange` tells the entity
    manager; if the level is ≤ 32, `ChunkMap.prepareTickingChunk` follows.

## Interfaces

- **Called by:** `ChunkHolder.updateFutures` (through `ChunkMap.prepareAccessibleChunk`,
  `ChunkMap.prepareTickingChunk`, `ChunkMap.prepareEntityTickingChunk`),
  `ServerChunkCache.getChunkFutureMainThread` (a synchronous
  `ServerChunkCache.getChunk` at any status — the server thread runs
  `ServerChunkCache.MainThreadExecutor.managedBlock`, draining chunk tasks
  while it waits), `ChunkLoadCounter` for the spawn-loading progress bar.
- **Calls into:** `ChunkGenerator` (`ChunkGenerator.createStructures`,
  `ChunkGenerator.createReferences`, `ChunkGenerator.createBiomes`,
  `ChunkGenerator.fillFromNoise`, `ChunkGenerator.buildSurface`,
  `ChunkGenerator.applyCarvers`, `ChunkGenerator.applyBiomeDecoration`,
  `ChunkGenerator.spawnOriginalMobs` — Part XI; the implementations are
  `NoiseBasedChunkGenerator`, `FlatLevelSource`, `DebugLevelSource`),
  `ThreadedLevelLightEngine`, `ChunkMap.scheduleChunkLoad`, `StructureCheck`.
- **Crosses the network as:** nothing. A chunk reaches a client only after
  *BLOCK_TICKING* promotion and `ChunkHolder.sendSync`
  ([tickets](tickets-and-loading.md)).
- **Data-driven by:** the `LevelStem`'s generator and its
  `NoiseGeneratorSettings` (`ChunkMap.randomState` from `RandomState.create`),
  `WorldOptions.generateStructures`, and *max.bg.threads*.

## Invariants and surprises

- **Worldgen is much less parallel than the thread names suggest.** One
  worldgen `ConsecutiveExecutor` per dimension runs one task at a time, and
  the dispatcher hands over one chunk's batch at a time; only biomes and
  noise fan out to the pool. Overlap comes from *runUntilWait* yielding at
  every layer.
- **Two pyramids, and loading still walks all twelve steps.** A *FULL*
  chunk on disk is not "just loaded": it passes through eleven no-op
  layers and needs its 3×3 ring at *INITIALIZE_LIGHT* before its own
  *LIGHT* step.
- **Two steps touch the server thread**: NBT → chunk object
  (`SerializableChunkData.read`) and *FULL* itself. Everything between is
  off-thread.
- **One request is 529 holders and a level-44 ring.** Radius 11 falls out
  of *STRUCTURE_STARTS* within 8 stacked on the radius-1 dependencies;
  `ChunkLevel.MAX_LEVEL` is computed from the pyramid, not chosen.
- **Each step runs once per holder.** `GenerationChunkHolder.startedWork`
  is a CAS; concurrent requesters share the future. A ticket level that
  drops fails pending futures with `GenerationChunkHolder.UNLOADED_CHUNK`
  (`GenerationChunkHolder.failAndClearPendingFuturesBetween`) rather than
  interrupting a thread.
- **Reads are policed at runtime.** A feature that reaches past its step's
  direct dependencies crashes with a named `WorldGenRegion.currentlyGenerating`;
  reading outside the write zone is logged, not allowed silently.
- **`ThrottlingChunkTaskDispatcher` is not worldgen.** It throttles the
  player-ticket work on the main thread, four chunks at a time.
- **A chunk mid-generation cannot be saved or unloaded**:
  `GenerationChunkHolder.generationRefCount` chains into the holder's save
  sync ([chunk storage](chunk-storage.md)).

## Where to look

`ChunkPyramid.GENERATION_PYRAMID` · `ChunkPyramid.LOADING_PYRAMID` ·
`ChunkStep.apply` · `ChunkDependencies.getRadiusOf` · `ChunkStatusTasks.full` ·
`ChunkStatusTasks.generateFeatures` · `ChunkGenerationTask.runUntilWait` ·
`ChunkGenerationTask.scheduleNextLayer` · `ChunkGenerationTask.canLoadWithoutGeneration` ·
`GenerationChunkHolder.scheduleChunkGenerationTask` · `GenerationChunkHolder.applyStep` ·
`GenerationChunkHolder.replaceProtoChunk` · `ChunkMap.applyStep` ·
`ChunkMap.scheduleChunkLoad` · `ChunkMap.runGenerationTask` ·
`ChunkTaskDispatcher.scheduleForExecution` · `ChunkTaskPriorityQueue` ·
`ChunkLevel.generationStatus` · `WorldGenRegion.getChunk` · `StaticCache2D` ·
`AbstractConsecutiveExecutor.run` · `Util.maxAllowedExecutorThreads` ·
`ServerChunkCache.getChunkFutureMainThread`

---

*Rules: names, never code · how the system works, not how the code reads ·
newest version only · every backticked name passes `tools/verify_names.py`.*
