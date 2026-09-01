# Structures

> Verified against **Minecraft 26.2** · Part XI · A village is generated: a lottery that never looks at the world, a jigsaw assembled in memory, terrain bent by a density function, and blocks written one chunk-slice at a time.

## Responsibility

A structure is a thing the generator decides to build *at* a place rather
than *from* it. The decision, the layout and the blocks are three separate
stages, run at three different chunk statuses, and each is cached
differently — which is why "is there a village here?" is a question the
game can usually answer without generating anything, and occasionally
answers by generating everything.

The one sentence a player recognises: *the village on the hill, and the
flat shelf of ground it is standing on that was not there before.*

## The data it owns

- **`Structure`** — the abstract definition. Its
  `Structure.StructureSettings` record carries the biomes it may appear in,
  a `StructureSpawnOverride` per `MobCategory`, the
  `GenerationStep.Decoration` it is placed at, and a `TerrainAdjustment`.
  Two methods matter: `Structure.findGenerationPoint` decides *where*, and
  `Structure.generate` produces the pieces. `StructureType` is the registry
  of kinds; `BuiltinStructures` holds the keys
  (`BuiltinStructures.VILLAGE_PLAINS` and its four siblings).
- **`StructureSet`** — the placement grid, shared by a group of structures.
  A list of `StructureSet.StructureSelectionEntry` (a structure and a
  weight) plus one `StructurePlacement`. `BuiltinStructureSets.VILLAGES`
  holds all five villages.
- **`StructurePlacement`** — where a set's grid falls.
  `RandomSpreadStructurePlacement` is the spacing/separation lottery
  (`RandomSpreadStructurePlacement.getPotentialStructureChunk`,
  `RandomSpreadType` linear or triangular);
  `ConcentricRingsStructurePlacement` is strongholds.
  `StructurePlacement.isStructureChunk` is the composite test, with
  `StructurePlacement.frequency`, a
  `StructurePlacement.FrequencyReductionMethod` and a deprecated
  `StructurePlacement.ExclusionZone` that lets one set repel another.
- **`ChunkGeneratorStructureState`** — the per-world placement state, built
  by `ChunkGenerator.createState` and held as `ChunkMap.chunkGeneratorState`.
  It keeps `ChunkGeneratorStructureState.possibleStructureSets` (filtered at
  construction to sets with a biome that can actually occur),
  `ChunkGeneratorStructureState.getPlacementsForStructure`, and the
  stronghold ring futures behind
  `ChunkGeneratorStructureState.ensureStructuresGenerated`.
- **`StructureStart`** — a final class, not a per-structure subclass: the
  structure, the `ChunkPos` it started in, a `PiecesContainer`, a reference
  count and a cached `BoundingBox`. `StructureStart.INVALID_START` is the
  written-down "nothing here".
- **`StructurePiece`** — one placeable box, with
  `StructurePiece.postProcess` as the write-into-the-world call.
  `StructurePiecesBuilder` accumulates them (and is the
  `StructurePieceAccessor` the assembler talks to); `StructurePieceType` is
  the registry that deserialises them. Concrete bases:
  `TemplateStructurePiece` (one `.nbt` template),
  `PoolElementStructurePiece` (jigsaw), `ScatteredFeaturePiece`.
- **Jigsaw** — `JigsawStructure` holds the start pool, the start jigsaw
  name, a depth (`JigsawStructure.MAX_DEPTH` is 20; villages use six), a
  start height, `JigsawStructure.MaxDistance` and the pool aliases.
  `StructureTemplatePool` is a weighted list of `StructurePoolElement`s
  (`SinglePoolElement`, `LegacySinglePoolElement`, `ListPoolElement`,
  `FeaturePoolElement`, `EmptyPoolElement`) with a fallback pool and a
  `StructureTemplatePool.Projection` — rigid, or terrain-matching, which
  carries a gravity processor. `JigsawBlock` and `JigsawBlockEntity` are the
  connectors; `JigsawBlockEntity.JointType` decides whether rotation must
  match. `JigsawJunction` records a made connection.
  `PoolAliasBinding` and `PoolAliasLookup` let one structure swap pools per
  placement.
- **Templates** — `StructureTemplate` is a parsed `.nbt` file:
  `StructureTemplate.Palette`s of `StructureTemplate.StructureBlockInfo`,
  entities, and `StructureTemplate.JigsawBlockInfo` for the connectors.
  `StructureTemplateManager` loads them, in order, from the world's
  generated directory, the gametest source, then data packs.
  `StructurePlaceSettings` carries rotation, mirror, bounding box,
  `LiquidSettings` and an ordered list of `StructureProcessor`s —
  `RuleProcessor` with its `ProcessorRule`s, `BlockRotProcessor`,
  `GravityProcessor`, `BlockIgnoreProcessor`,
  `JigsawReplacementProcessor` — grouped into a `StructureProcessorList`.
- **The seam into the world** — `StructureManager` is the per-level view of
  starts and references (`StructureManager.startsForStructure`,
  `StructureManager.setStartForStructure`,
  `StructureManager.addReferenceForStructure`,
  `StructureManager.getStructureAt`), with
  `StructureManager.forWorldGenRegion` for a generating chunk. `StructureCheck`
  is the presence cache that answers `StructureCheckResult`.

## When it runs

Four moments, three of them on the worldgen executor
([the pipeline](../world/chunk-generation-pipeline.md)):

- **World start, main thread.** `ChunkGenerator.createState` filters the
  structure sets; `ChunkGeneratorStructureState.ensureStructuresGenerated`
  fills the placements and fires the stronghold ring searches onto the
  background pool.
- **`ChunkStatus.STRUCTURE_STARTS`** — the lottery and the whole jigsaw
  assembly. No blocks are written and no neighbour is read.
- **`ChunkStatus.STRUCTURE_REFERENCES`** — each chunk scans the 17×17
  square around itself for starts that overlap it. This is why almost every
  later step in the pyramid requires structure starts within 8.
- **`ChunkStatus.NOISE`** — `Beardifier` reads those references and bends
  the terrain, as a density function
  ([density functions](density-functions.md)).
- **`ChunkStatus.FEATURES`** — `StructureStart.placeInChunk` writes blocks,
  before that step's features
  ([features and placement](features-and-placement.md)).

`StructureCheck` is main-thread-only and unsynchronised, which is why
`ServerLevel.onStructureStartsAvailable` hops back to the server thread from
the worldgen executor to feed it.

## The trace: a village

```mermaid
sequenceDiagram
    participant ST as ChunkStatusTasks
    participant CG as ChunkGenerator
    participant SP as RandomSpreadStructurePlacement
    participant JS as JigsawStructure
    participant JP as JigsawPlacement.Placer
    participant SM as StructureManager
    participant BD as Beardifier
    participant SS as StructureStart
    participant TP as StructureTemplate

    ST->>CG: createStructures — ChunkStatus.STRUCTURE_STARTS
    CG->>SP: isStructureChunk — spacing 34, separation 8, salt; seed arithmetic only
    SP-->>CG: yes: this is the grid cell's chosen chunk
    CG->>CG: weighted pick among the five villages; re-roll on failure
    CG->>JS: Structure.generate → findValidGenerationPoint
    JS->>JS: sample start height · pick a town centre · drop to getFirstFreeHeight
    JS-->>CG: Structure.GenerationStub — pieces still a deferred consumer
    CG->>JP: GenerationStub.getPiecesBuilder → tryPlacingChildren
    loop until the priority queue drains, depth ≤ 6
        JP->>JP: JigsawBlock.canAttach · rotation · projection · collision against the free shape
        JP->>JP: add PoolElementStructurePiece · JigsawJunction on both sides
    end
    JP-->>CG: StructurePiecesBuilder.build → PiecesContainer → StructureStart
    CG->>SM: setStartForStructure · onStructureStartsAvailable (hop to main thread)
    ST->>CG: createReferences — 17×17 scan, each overlapped chunk records the start
    ST->>BD: NOISE: Beardifier.forStructuresInChunk — density term, no blocks
    ST->>SS: FEATURES: placeInChunk, clipped to this chunk's writable area
    SS->>TP: StructurePiece.postProcess → StructureTemplate.placeInWorld
    Note over TP: processors run in order · jigsaw blocks replaced by final_state · loot seed stamped
```

1. **The lottery.** `ChunkGenerator.createStructures` walks the possible
   structure sets. For villages that is
   `RandomSpreadStructurePlacement.getPotentialStructureChunk`: divide the
   chunk coordinates by the spacing, seed a `WorldgenRandom` from the level
   seed, the grid cell and the set's salt, and draw two offsets inside the
   cell. This chunk is the village chunk only if the draw lands exactly
   here. **Nothing about the world is consulted** — no biome, no terrain,
   no chunk data.
2. **Which village.** The set has five entries, so a second `WorldgenRandom`
   picks one by weight. If it fails — almost always the biome filter — that
   entry is removed, its weight subtracted, and the roll repeated. A chunk
   on a biome border therefore still gets *a* village rather than none.
3. **The start point.** `Structure.generate` calls
   `Structure.findValidGenerationPoint`, which is
   `Structure.findGenerationPoint` filtered through `Structure.isValidBiome`
   — the biome is sampled *at the proposed point*, after the lottery.
   `JigsawStructure.findGenerationPoint` samples its start height, picks a
   town centre from the start pool, and moves it so its ground level sits on
   `ChunkGenerator.getFirstFreeHeight`. It returns a
   `Structure.GenerationStub` whose piece list is still an unexecuted
   consumer.
4. **Assembly.** `Structure.GenerationStub.getPiecesBuilder` runs it:
   `JigsawPlacement.addPieces` builds a free-space shape around the centre
   and hands it to `JigsawPlacement.Placer`. For each jigsaw block of a
   placed piece — shuffled, then sorted by selection priority — the target
   pool's shuffled templates are tried, then the *fallback* pool's;
   `JigsawBlock.canAttach` requires opposed faces and matching names, and an
   aligned joint additionally requires matching rotation. Y comes from the
   `StructureTemplatePool.Projection`: rigid onto rigid keeps the parent's
   offset, terrain-matching drops the piece onto the surface. A candidate
   that survives the collision test against the free shape becomes a
   `PoolElementStructurePiece`, subtracts its box from the free shape,
   records a `JigsawJunction` on **both** sides, and is pushed onto
   `JigsawPlacement.Placer.placing` — a priority queue, not a stack — for
   its own children, until the depth limit.
5. **The start is stored.** `StructurePiecesBuilder.build` gives a
   `PiecesContainer`; a `StructureStart` wraps it and goes onto the
   `ChunkAccess` through `StructureManager.setStartForStructure`. Then
   `ServerLevel.onStructureStartsAvailable` hops to the server thread to
   tell `StructureCheck`.
6. **References.** At `ChunkStatus.STRUCTURE_REFERENCES`,
   `ChunkGenerator.createReferences` scans the 17×17 chunk square around
   *each* chunk and records the packed position of every start whose
   bounding box overlaps it. Discovery is outside-in: a village never walks
   its own pieces to announce itself.
7. **The ground bends.** At `ChunkStatus.NOISE`,
   `Beardifier.forStructuresInChunk` reads those references, keeps the rigid
   pieces as `Beardifier.Rigid` boxes plus the nearby junctions, and adds a
   density contribution from a precomputed kernel. `TerrainAdjustment` picks
   the shape. **No blocks are edited** — the shelf under a village is the
   noise field being told to be solid there
   ([the worldgen pipeline](worldgen-pipeline.md)).
8. **The blocks.** At `ChunkStatus.FEATURES`,
   `ChunkGenerator.applyBiomeDecoration` places structures at their declared
   decoration step, *before* that step's features.
   `StructureStart.placeInChunk` derives a reference position from piece
   zero and calls `StructurePiece.postProcess` on every piece overlapping
   this chunk's writable area.
9. **One piece, one template.** `PoolElementStructurePiece` places its
   element; `SinglePoolElement` assembles the `StructurePlaceSettings` —
   the chunk box, the rotation, the ignore processor, then
   `JigsawReplacementProcessor`, then the element's own processor list, then
   the projection's. `StructureTemplate.placeInWorld` runs every block
   through `StructureTemplate.processBlockInfos`, writes what falls inside
   the box, loads block-entity data
   ([block entities](../blocks/block-entities.md)) and stamps a fresh loot
   seed into containers ([loot tables](../items/loot-tables.md)).
   A `FeaturePoolElement` places a `PlacedFeature` instead — that is how
   village trees arrive.
10. **Repeat per chunk.** Every chunk the village touches runs steps 8–9
    with its own box, so a house that straddles four chunks is written in
    four slices, at four different times.

## Interfaces

- **Called by:** `ChunkStatusTasks.generateStructureStarts`,
  `ChunkStatusTasks.generateStructureReferences` and
  `ChunkStatusTasks.generateFeatures`;
  `NoiseBasedChunkGenerator` (for the beardifier); `NaturalSpawner` through
  `ChunkGenerator.getMobsAt`; `LocateCommand.locateStructure`;
  `ExplorationMapFunction` for treasure maps; `EnderEyeItem`.
- **Calls into:** `StructureTemplateManager`, the placed-feature path for
  feature pool elements, `ChunkGenerator.getFirstFreeHeight`, and
  `BiomeSource.getNoiseBiome` for the biome filter.
- **Crosses the network as:** nothing directly. Structures reach the client
  as ordinary blocks. Only the *effects* travel — a filled map, a spawner's
  mobs.
- **Data-driven by:** `Registries.STRUCTURE`, `Registries.STRUCTURE_SET`,
  `Registries.TEMPLATE_POOL` and `Registries.PROCESSOR_LIST` (all data-pack
  registries, bootstrapped from the Java in the data package —
  `Structures`, `StructureSets`, `PlainVillagePools`, `ProcessorLists`),
  plus the `.nbt` templates themselves and the biome tags
  (`BiomeTags.HAS_VILLAGE_PLAINS`) and `StructureTags` that gate placement
  and locating.

## Invariants and surprises

- **The grid is decided by seed arithmetic alone.** A village's candidate
  chunk falls out of the level seed, the spacing and the salt, with no
  reference to the world. The biome test happens afterwards and can veto
  it, leaving the cell empty — the slot still exists, the village does not.
- **Assembly is lazy, and may run twice.** `Structure.GenerationStub` holds
  the pieces as an unexecuted consumer, so `StructureCheck` can answer "a
  village exists here" without ever laying one out — and `Structure.generate`
  then lays it out again. Both runs are deterministic and agree.
- **`/locate` can drive world generation from the server thread.** On a
  cache miss `StructureCheck` re-runs the placement test; on
  `StructureCheckResult.CHUNK_LOAD_NEEDED` it loads the chunk to structure
  starts, synchronously, for up to a hundred expanding rings of grid cells.
  That is the pause after the command.
- **Absence is written to disk.** An invalid start is persisted with an id
  of *INVALID*, so a partial chunk scan can prove there is nothing there
  without regenerating it.
- **Terrain adaptation writes no blocks.** It is a density term added by
  `Beardifier` at `ChunkStatus.NOISE`, kernel-weighted, with the junctions
  between pieces contributing at a lower weight than the pieces — which is
  where the smooth shoulders under village streets come from.
- **The 128-block cage is enforced when the data pack loads**, not when the
  structure generates: a jigsaw whose maximum distance plus the terrain
  margin exceeds `JigsawStructure.MAX_TOTAL_STRUCTURE_RANGE` fails
  validation. That limit is what keeps the 17×17 reference scan sufficient.
- **Jigsaw blocks delete themselves.** `JigsawReplacementProcessor` swaps
  each one for the state named in its final-state string, or removes it
  entirely. The assembly graph is invisible in the finished village unless
  the debug flag in `SharedConstants` is set.
- **Placement is a priority queue.** Children are expanded by the jigsaw's
  placement priority, insertion order breaking ties — not depth-first —
  so a pool can insist its connections are made before its siblings'.
- **Structures outrank biomes for spawning.** `ChunkGenerator.getMobsAt`
  checks `Structure.spawnOverrides` first, scoped either to the piece or
  the whole start ([biomes](biomes.md)). Nether fortresses are special-cased
  earlier still, in `NaturalSpawner`.
- **Two unrelated classes are called `StructureManager`-ish.**
  `ServerLevel.structureManager` is the starts-and-references view;
  `ServerLevel.getStructureManager` is the `.nbt` template loader owned by
  the server. And there is a second, unrelated `StructureCheck` in the
  entity-variant package.
- **Dead code ships in this package.** `PostPlacementProcessor`,
  `PieceGenerator` and `PieceGeneratorSupplier` are referenced by nothing;
  the live hook is `Structure.afterPlace`.

## Where to look

`Structure.generate` · `Structure.findGenerationPoint` ·
`Structure.StructureSettings` · `StructureSet` ·
`RandomSpreadStructurePlacement.getPotentialStructureChunk` ·
`ChunkGeneratorStructureState.generatePositions` ·
`ChunkGenerator.createStructures` · `ChunkGenerator.createReferences` ·
`JigsawStructure` · `JigsawPlacement.addPieces` ·
`JigsawPlacement.Placer` · `StructureTemplatePool` ·
`PoolElementStructurePiece.place` · `StructureStart.placeInChunk` ·
`StructureTemplate.placeInWorld` · `StructurePlaceSettings` ·
`JigsawReplacementProcessor` · `Beardifier.forStructuresInChunk` ·
`StructureManager.startsForStructure` · `StructureCheck.checkStart` ·
`ChunkGenerator.findNearestMapStructure`

---

*Rules: names, never code · how the system works, not how the code reads ·
newest version only · every backticked name passes `tools/verify_names.py`.*
