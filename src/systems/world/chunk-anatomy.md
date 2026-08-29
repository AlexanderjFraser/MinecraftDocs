# Chunk anatomy

> Verified against **Minecraft 26.2** · Part IV · No trace — the data page: what a chunk is made of, from the 16×16×16 section down to the bit-packed palette, and the three shapes a chunk takes on its way to being ticked.

## Responsibility

A chunk is the unit the world is stored, generated, loaded, lit, sent and
ticked in: a 16×16 column of the full build height, cut into 16-block
sections. Every other page in this part moves chunks around — through
tickets, the generation pyramid, the light engine, the region files — and
none of them look inside. This page does. It has no trace because a chunk
does not *do* anything; it is the thing the traces happen to.

The one sentence a player recognises: *the 16×16 column that F3 reports you
are standing in, and that loads and unloads as one piece.*

## The data it owns

### The hierarchy

`ChunkAccess` is the abstract chunk and has exactly two concrete lines.
`ProtoChunk` is a chunk under construction on the worker pool
(`ChunkType.PROTOCHUNK`); `LevelChunk` is a live chunk owned by a `Level`
(`ChunkType.LEVELCHUNK`). `ImposterProtoChunk` is a `ProtoChunk`-shaped
view over a finished `LevelChunk`, and `EmptyLevelChunk` is the client's
stand-in for "not loaded". Nothing else extends `ChunkAccess`.

What every chunk owns, whatever its shape:

- `ChunkAccess.chunkPos` and `ChunkAccess.levelHeightAccessor` — where it is
  and how tall it is. `LevelHeightAccessor.getMinY` / `LevelHeightAccessor.getHeight`
  are the two facts; `LevelHeightAccessor.getSectionsCount` and
  `LevelHeightAccessor.getSectionIndex` derive from them. The overworld is
  −64 with height 384: section Y −4 to 19, **24 sections**.
- `ChunkAccess.sections` — the `LevelChunkSection[]`. Never has a hole:
  the constructor runs `ChunkAccess.replaceMissingSections` so an absent
  section becomes a fresh air section from the level's
  `PalettedContainerFactory`.
- `ChunkAccess.heightmaps` — an `EnumMap` by `Heightmap.Types`, created
  lazily (`ChunkAccess.getOrCreateHeightmapUnprimed`); `ChunkAccess.setHeightmap`
  installs raw `long[]` from disk or packet.
- `ChunkAccess.skyLightSources` — a `ChunkSkyLightSources`, a *second*,
  private heightmap used only by the sky-light engine ([lighting](lighting.md)).
- `ChunkAccess.blockEntities` (live `BlockEntity` objects) and
  `ChunkAccess.pendingBlockEntities` (still NBT, not yet deserialised —
  `ChunkAccess.getBlockEntitiesPos` unions the two).
- `ChunkAccess.structureStarts` and `ChunkAccess.structuresRefences`
  (Mojang's spelling) — Part XI's structure bookkeeping; every setter
  marks the chunk unsaved.
- `ChunkAccess.postProcessing` — per-section `ShortList`s of packed block
  offsets to revisit after load (`ProtoChunk.packOffsetCoordinates`: four
  bits each of x, y, z in a short).
- `ChunkAccess.upgradeData` (an `UpgradeData`, normally `UpgradeData.EMPTY`;
  edge fix-ups for chunks bordering older terrain) and
  `ChunkAccess.blendingData` (a `BlendingData`, nullable; its presence is
  what `ChunkAccess.isOldNoiseGeneration` means).
- `ChunkAccess.inhabitedTime` — the counter behind local difficulty,
  bumped per tick while a player is near ([the level tick](../server/server-level-tick.md)).
- Two *volatile* flags: `ChunkAccess.unsaved` (`ChunkAccess.markUnsaved`;
  `ChunkAccess.tryMarkSaved` is the test-and-clear the saver uses) and
  `ChunkAccess.isLightCorrect` (saved as *isLightOn*).
- `ChunkAccess.getPersistedStatus` — the `ChunkStatus` that goes to disk;
  `ChunkAccess.getHighestGeneratedStatus` folds in the below-zero-retrogen
  target (`BelowZeroRetrogen.targetStatus`) for chunks still being
  deepened.

`ChunkAccess` also implements `LightChunk` (what the light engine reads:
`LightChunk.findBlockLightSources`, `LightChunk.getSkyLightSources`),
`StructureAccess`, and `BiomeManager.NoiseBiomeSource`.

### `LevelChunkSection` — 16×16×16

A section is two palette containers and four counters.

- `LevelChunkSection.states` — a `PalettedContainer` of `BlockState`, 4096
  entries.
- `LevelChunkSection.biomes` — a `PalettedContainerRO` of `Holder` of
  `Biome`, **64** entries: biomes are stored per 4×4×4 *quart*
  (`LevelChunkSection.BIOME_CONTAINER_BITS` = 2 bits per axis). It is
  read-only and *not final*: `LevelChunkSection.fillBiomesFromNoise`,
  `LevelChunkSection.read` and `LevelChunkSection.readBiomes` replace the
  whole container through `PalettedContainerRO.recreate` rather than
  mutate it.
- `LevelChunkSection.nonEmptyBlockCount` (`LevelChunkSection.hasOnlyAir` is
  "== 0"), `LevelChunkSection.fluidCount`,
  `LevelChunkSection.tickingBlockCount` and
  `LevelChunkSection.tickingFluidCount`. Every `LevelChunkSection.setBlockState`
  adjusts all four from the old and new state;
  `LevelChunkSection.recalcBlockCounts` recounts after a disk load.
  `LevelChunkSection.isRandomlyTicking` (blocks *or* fluids) is what lets
  the level tick skip a section of stone outright.
- `LevelChunkSection.acquire` / `LevelChunkSection.release` forward to the
  block-state container's threading detector (below). The five-argument
  `LevelChunkSection.setBlockState` with *checkThreading* false is the
  worker-pool path — `NoiseBasedChunkGenerator` and `OreFeature` hold the
  section and write through `PalettedContainer.getAndSetUnchecked`.
- `LevelChunkSection.write` / `LevelChunkSection.read` are the wire form:
  two shorts (`LevelChunkSection.nonEmptyBlockCount`, `LevelChunkSection.fluidCount`),
  then the two containers. `LevelChunkSection.copy` is the deep copy the
  saver and the client mesher take.

### `PalettedContainer` — palettes and bit packing

`PalettedContainer` maps 4096 (or 64) small integers to values through a
palette, and stores the integers in a `BitStorage`. Its state is one
*volatile* record, `PalettedContainer.Data` — `PalettedContainer.Data.configuration`,
`PalettedContainer.Data.storage`, `PalettedContainer.Data.palette` — swapped
atomically on resize and on network read. Reads
(`PalettedContainer.get`) take no lock; they read the record once.

The tiers come from a top-level `Strategy` (it is no longer nested in
`PalettedContainer`): `Strategy.createForBlockStates` and
`Strategy.createForBiomes`, each returning a `Configuration` for a
requested bit count (`Strategy.getConfigurationForBitCount`,
`Strategy.getConfigurationForPaletteSize`). `Configuration.Simple` has one
width in memory and on the wire; `Configuration.Global` stores registry ids
at `Configuration.bitsInMemory` = ceillog2(registry size) and
`Configuration.alwaysRepack` on load.

| palette needs | block states | biomes |
|---|---|---|
| 0 bits (one value) | `Strategy.ZERO_BITS` → `SingleValuePalette` + `ZeroBitStorage` | same |
| 1–4 bits | `Strategy.FOUR_BITS_LINEAR` → `LinearPalette`, *always* 4 bits | `Strategy.ONE_BIT_LINEAR` / `Strategy.TWO_BITS_LINEAR` / `Strategy.THREE_BITS_LINEAR` |
| 5–8 bits | `Strategy.FIVE_BITS_HASHMAP` … `Strategy.EIGHT_BITS_HASHMAP` → `HashMapPalette` | — (no hashmap tier) |
| more | `Configuration.Global` → `GlobalPalette` (the registry `IdMap` itself) | `Configuration.Global` |

The palettes: `SingleValuePalette` holds one value and resizes on the
second; `LinearPalette` is an array scanned by identity; `HashMapPalette`
is a `CrudeIncrementalIntIdentityHashBiMap`; `GlobalPalette` writes nothing
on the wire and maps unknown values to id 0. Each one calls
`PaletteResize.onResize` when it is full, and the container *is* its own
`PaletteResize`: `PalettedContainer.onResize` builds a new `PalettedContainer.Data`
for the next width, `PalettedContainer.Data.copyFrom` re-encodes every
entry, the record is published, and the value that triggered the growth
is added under `PaletteResize.noResizeExpected` (which throws if growth
were needed again).

Storage: `SimpleBitStorage` never lets an entry straddle a long —
`SimpleBitStorage.valuesPerLong` is 64 ÷ bits, so a 4-bit section is 256
longs (2 KiB), a 5-bit one 342, an 8-bit one 512; the cell index uses the
`SimpleBitStorage.MAGIC` multiply-shift table instead of dividing.
`ZeroBitStorage` returns 0 for everything and shares one empty
`ZeroBitStorage.RAW` array. A wrong-length array from disk is a
`SimpleBitStorage.InitializationException`, which `PalettedContainer.unpack`
turns into a `DataResult` error rather than a crash.

Two serialised forms. `PalettedContainer.write` / `PalettedContainer.read`
are the wire: a bits byte, the palette, a fixed-size long array — exactly
the in-memory width. `PalettedContainer.pack` / `PalettedContainer.unpack`
(`PalettedContainerRO.PackedData`, the *palette* and optional *data* NBT
fields behind `PalettedContainer.codecRW` / `PalettedContainer.codecRO`) are
the disk: `PalettedContainer.pack` re-encodes into a `HashMapPalette` and
picks the width by *palette size*, so the disk form is the smallest that
fits and `PalettedContainer.unpack` re-encodes on load whenever the widths
differ.

Thread safety is a **detector, not a lock**. `PalettedContainer.threadingDetector`
is a `ThreadingDetector` around a one-permit semaphore:
`ThreadingDetector.checkAndLock` tries to acquire, and on failure records
the loser, waits, and throws `ThreadingDetector.makeThreadingException`
("Accessing PalettedContainer from multiple threads") with both stacks.
Contention is a crash by design; the rule it enforces is that only one
thread writes a section at a time — the server thread for a live chunk,
the worker that holds `LevelChunkSection.acquire` for a proto chunk.

### Heightmaps

`Heightmap` is 256 entries (`x + z·16`) in a `SimpleBitStorage` whose width
is `Mth.ceillog2` of height + 1 — **9 bits for a 384-tall world**, stored
relative to the minimum Y. `Heightmap.primeHeightmaps` fills several types
in one top-down column scan; `Heightmap.update` is the incremental path
from `LevelChunk.setBlockState` (raise on an opaque placement, rescan
downward when the top block turns transparent). `Heightmap.getFirstAvailable`
is the first *free* Y; `Heightmap.getHighestTaken` the last solid one.

`Heightmap.Types` has six constants and three audiences (`Heightmap.Usage`):

| type | opaque means | usage | saved | sent |
|---|---|---|---|---|
| `Heightmap.Types.WORLD_SURFACE_WG` | not air | `Heightmap.Usage.WORLDGEN` | no | no |
| `Heightmap.Types.WORLD_SURFACE` | not air | `Heightmap.Usage.CLIENT` | yes | yes |
| `Heightmap.Types.OCEAN_FLOOR_WG` | blocks motion | `Heightmap.Usage.WORLDGEN` | no | no |
| `Heightmap.Types.OCEAN_FLOOR` | blocks motion | `Heightmap.Usage.LIVE_WORLD` | yes | **no** |
| `Heightmap.Types.MOTION_BLOCKING` | blocks motion or has fluid | `Heightmap.Usage.CLIENT` | yes | yes |
| `Heightmap.Types.MOTION_BLOCKING_NO_LEAVES` | same, not `LeavesBlock` | `Heightmap.Usage.CLIENT` | yes | yes |

Which ones a chunk carries depends on its status: `ChunkStatus.heightmapsAfter`
is the two *_WG* maps up to `ChunkStatus.SURFACE` and the four others from
`ChunkStatus.CARVERS` on. A `LevelChunk` is built with exactly
`ChunkStatus.FULL`'s four.

### `ProtoChunk` — generation-only state

On top of the shared state a `ProtoChunk` has the things only generation
needs: `ProtoChunk.status` (volatile; `ProtoChunk.setPersistedStatus` also
retires a finished `BelowZeroRetrogen`), `ProtoChunk.lightEngine` (set by
`ProtoChunk.setLightEngine`; `ProtoChunk.setBlockState` only tells it about
changes once the status `ChunkStatus.isOrAfter` `ChunkStatus.INITIALIZE_LIGHT`),
`ProtoChunk.entities` (a list of `CompoundTag` — `ProtoChunk.addEntity`
serialises immediately; they become real entities at `ChunkStatus.FULL`),
`ProtoChunk.carvingMask` (a `CarvingMask`, a `BitSet` of 256 × height),
and `ProtoChunk.blockTicks` / `ProtoChunk.fluidTicks` as `ProtoChunkTicks`,
unpacked into `LevelChunkTicks` on promotion. `ProtoChunk.getNoiseBiome`
throws "Asking for biomes before we have biomes" before `ChunkStatus.BIOMES`.
`ProtoChunk.setBlockState` writes the section and updates heightmaps and
light; it has no block-entity or neighbour side effects.

### `LevelChunk` — the live chunk

- `LevelChunk.level`, `LevelChunk.loaded` (`LevelChunk.setLoaded`), and
  `LevelChunk.fullStatus`, a `Supplier` of `FullChunkStatus` that the
  holder owns (`FullChunkStatus.INACCESSIBLE` / `FullChunkStatus.FULL` /
  `FullChunkStatus.BLOCK_TICKING` / `FullChunkStatus.ENTITY_TICKING` — the
  [next page](tickets-and-loading.md)).
- `LevelChunk.blockTicks` / `LevelChunk.fluidTicks` — `LevelChunkTicks`,
  attached to the level's queues by `LevelChunk.registerTickContainerInLevel`
  and detached by `LevelChunk.unregisterTickContainerFromLevel`.
- `LevelChunk.postLoad` — a `LevelChunk.PostLoadProcessor` run once by
  `LevelChunk.runPostLoad` (the entity load).
- `LevelChunk.unsavedListener` — `LevelChunk.markUnsaved` fires it only on
  the false→true edge; it is how the server's dirty set learns of a change
  without scanning.
- `LevelChunk.gameEventListenerRegistrySections` — one
  `EuclideanGameEventListenerRegistry` per section Y, created on demand,
  server only ([game events](game-events-and-poi.md)).
- `LevelChunk.getPersistedStatus` is always `ChunkStatus.FULL`.

The constructor from a `ProtoChunk` **shares the section array** — no copy
— and copies block entities, pending NBT, post-processing lists,
structure data, the four final heightmaps and the sky-light sources.

`LevelChunk.setBlockState` is the one write path and does, in order:
early-out if an air-only section is being given air; the section write;
return null if nothing changed; update the four heightmaps; if the
section's emptiness flipped, `LevelLightEngine.updateSectionStatus` and
`ChunkSource.onSectionEmptinessChanged`; if
`LightEngine.hasDifferentLightProperties`, `ChunkSkyLightSources.update`
and `LevelLightEngine.checkBlock`; remove the old block entity (with
`BlockEntity.preRemoveSideEffects` on the server); `BlockBehaviour.BlockStateBase.onPlace`;
create or re-validate the new block entity; `LevelChunk.markUnsaved`. The
flags are `Block.UpdateFlags` (`Block.UPDATE_ALL`, `Block.UPDATE_NONE`);
neighbour *updates* are not here — they are `Level.setBlock`'s job, after
the chunk returns (Part V).

Block entities and tickers: `LevelChunk.getBlockEntity` takes a
`LevelChunk.EntityCreationType` (`LevelChunk.EntityCreationType.IMMEDIATE`,
`LevelChunk.EntityCreationType.QUEUED`, `LevelChunk.EntityCreationType.CHECK`)
and promotes pending NBT through `LevelChunk.promotePendingBlockEntity` on
first touch. `LevelChunk.addAndRegisterBlockEntity` sets it, registers its
game-event listener and its ticker. Tickers are indirected twice: a
`LevelChunk.BoundTickingBlockEntity` binds the entity to its
`BlockEntityTicker` and gates on `LevelChunk.isTicking` (border, block-ticking
status, entities loaded); it sits inside a
`LevelChunk.RebindableTickingBlockEntityWrapper` held in
`LevelChunk.tickersInLevel`, so `Level.blockEntityTickers` keeps one stable
handle per position and removal is a `LevelChunk.RebindableTickingBlockEntityWrapper.rebind`
to `LevelChunk.NULL_TICKER`, whose `TickingBlockEntity.isRemoved` is true
and lets the level's list prune itself.

`LevelChunk.postProcessGeneration` runs the post-processing offsets,
promotes every pending block entity and applies `UpgradeData.upgrade`.
`LevelChunk.replaceWithPacketData` is the client's refill from a packet;
`LevelChunk.replaceBiomes` the refill for `ClientboundChunksBiomesPacket`.

### `ImposterProtoChunk` and `EmptyLevelChunk`

Once a chunk is `ChunkStatus.FULL`, neighbours still generating ask the holder for "the
chunk at status X" and must get something `ProtoChunk`-typed.
`GenerationChunkHolder.replaceProtoChunk` (from `ChunkStatusTasks.full`)
and `SerializableChunkData` (when a `ChunkStatus.FULL` chunk is read from disk) install
an `ImposterProtoChunk` over the `LevelChunk`. Reads delegate; writes are
ignored unless *allowWrites*; `ImposterProtoChunk.fixType` maps the *_WG*
heightmap requests onto the live ones; `ImposterProtoChunk.canBeSerialized`
is false (the `LevelChunk` is what gets saved); and its carving mask
throws "Meaningless in this context". `ImposterProtoChunk.getWrapped` is
the way back.

`EmptyLevelChunk` is `Blocks.VOID_AIR` everywhere, `LevelChunk.isEmpty`
true, one fixed biome; `ClientChunkCache.emptyChunk` is the one instance
the client hands out for any position outside its ring.

## When it runs

A chunk has no tick of its own. Who touches it and on which thread:

- **Worker-Main-n** builds and writes a `ProtoChunk` through
  `LevelChunkSection.acquire` and the unchecked setter ([the generation
  pipeline](chunk-generation-pipeline.md)); the light engine reads it there too.
- **Server thread** owns every `LevelChunk`: `LevelChunk.setBlockState`,
  block entities, tickers, ticks. Promotion from proto to level happens
  here (`ChunkStatusTasks.full`).
- **IO-Worker-n** never sees a live section: the saver takes
  `LevelChunkSection.copy` snapshots on the server thread
  (`SerializableChunkData.copyOf`) and serialises the copies off-thread
  ([chunk storage](chunk-storage.md)).
- **Render thread** owns the client's `LevelChunk`s inside
  `ClientChunkCache.Storage`, an `AtomicReferenceArray` ring of
  (2·radius+1)² slots addressed by `ClientChunkCache.Storage.getIndex`;
  `ClientChunkCache.Storage.onSectionEmptinessChanged` and its
  double-buffered added/removed lists are the renderer's "which sections
  exist" feed. The mesher takes a `SectionCopy` (the block-state container
  copied, block entities snapshotted) so it can run on the pool.

## Interfaces

- **Called by:** everything in this part; `Level.getBlockState` ends in
  `LevelChunk.getBlockState`, `Level.setBlock` in `LevelChunk.setBlockState`.
- **Calls into:** `LevelLightEngine` and `ChunkSkyLightSources` (lighting),
  `Heightmap`, `LevelChunkTicks` (block ticks), `BlockBehaviour.BlockStateBase.onPlace` and
  `EntityBlock.newBlockEntity` (Part V), `GameEventListenerRegistry`.
- **Crosses the network as:** `ClientboundLevelChunkWithLightPacket`,
  whose `ClientboundLevelChunkPacketData` holds the heightmaps whose type
  `Heightmap.Types.sendToClient`, a buffer of *every* section's
  `LevelChunkSection.write` (empty ones included; the reader caps it at
  `ClientboundLevelChunkPacketData.TWO_MEGABYTES`), and the block-entity
  update tags (`ClientboundLevelChunkPacketData.BlockEntityInfo`). Light
  rides beside it in `ClientboundLightUpdatePacketData`. The client
  applies it with `ClientPacketListener.updateLevelChunk` →
  `ClientChunkCache.replaceWithPacketData` → `LevelChunk.replaceWithPacketData`.
  Biome-only refreshes are `ClientboundChunksBiomesPacket`.
- **Data-driven by:** `Block.BLOCK_STATE_REGISTRY` and the biome registry —
  the two `IdMap`s a `PalettedContainerFactory` is built from
  (`PalettedContainerFactory.create`), which is why the global palette's
  width is computed at runtime, not a constant.

## Invariants and surprises

- **Biomes are 4×4×4 and replaced, never mutated.** The
  `LevelChunkSection.biomes` container is read-only; every biome change
  swaps in a new one. Only block states resize in place.
- **Small palettes are padded to 4 bits.** A section with two block
  states ships 256 longs, the same as one with sixteen; the disk form
  (`PalettedContainer.pack`) is the one that shrinks to fit.
- **The proto and the level chunk share sections.** Promotion is a
  handover of the same `LevelChunkSection[]`, which is why the imposter
  keeps its own empty array and only exposes the wrapped one when writes
  are allowed.
- **Concurrent section writes crash on purpose.** `ThreadingDetector` is
  not a mutex; the second thread is the one that dies, with both stacks in
  the report. Reads are lock-free against a volatile record.
- **Heightmaps are not nine bits by definition** — the width is
  ceillog2(height + 1) per dimension — and only three of the six types
  reach the client. `Heightmap.Types.OCEAN_FLOOR` is saved and never sent.
- **The client trusts the counters.** `LevelChunkSection.read` takes the
  two shorts from the wire and never recounts;
  `LevelChunkSection.recalcBlockCounts` runs on disk load only.
- **`ChunkAccess.getHighestSectionPosition` is deprecated for removal** and
  is still where `Heightmap.primeHeightmaps` starts its scan.
- **A block entity is created lazily.** Until something asks with
  `LevelChunk.EntityCreationType.IMMEDIATE` or the chunk registers after
  load (`LevelChunk.registerAllBlockEntitiesAfterLevelLoad`), a loaded
  chest is a `CompoundTag` in `ChunkAccess.pendingBlockEntities`.

## Where to look

`ChunkAccess` · `LevelChunk.setBlockState` · `LevelChunk.getBlockEntity` ·
`LevelChunkSection.setBlockState` · `LevelChunkSection.write` ·
`PalettedContainer.onResize` · `PalettedContainer.pack` · `Strategy.createForBlockStates` ·
`Configuration.Global` · `SimpleBitStorage` · `ThreadingDetector.checkAndLock` ·
`Heightmap.Types` · `ChunkStatus.heightmapsAfter` · `ProtoChunk.setBlockState` ·
`ImposterProtoChunk` · `ChunkStatusTasks.full` · `ClientChunkCache.Storage` ·
`ClientboundLevelChunkPacketData.extractChunkData`

---

*Rules: names, never code · how the system works, not how the code reads ·
newest version only · every backticked name passes `tools/verify_names.py`.*
