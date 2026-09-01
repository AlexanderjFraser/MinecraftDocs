# The worldgen pipeline

> Verified against **Minecraft 26.2** · Part XII · One chunk's terrain: noise cells filled from an interpolated lattice, an aquifer that decides what liquid belongs where, ore veins placed before the surface exists, and carvers that never place air.

## Responsibility

Four of the twelve chunk statuses produce terrain — biomes, noise, surface,
carvers — and this page is what happens inside them. The conveyor that runs
them, the dependency pyramid and the threading are
[the chunk generation pipeline](../world/chunk-generation-pipeline.md);
this is the cargo. The scalar field the whole thing rests on is
[density functions](density-functions.md), and the labels that steer it are
[biomes](biomes.md).

The one sentence a player recognises: *the shape of the land, and the
water table in the cave you just dug into.*

## The data it owns

- **`ChunkGenerator`** — the abstract API the statuses call:
  `ChunkGenerator.createBiomes`, `ChunkGenerator.fillFromNoise`,
  `ChunkGenerator.buildSurface`, `ChunkGenerator.applyCarvers`,
  `ChunkGenerator.applyBiomeDecoration`, `ChunkGenerator.spawnOriginalMobs`,
  plus the height queries `ChunkGenerator.getBaseHeight` and
  `ChunkGenerator.getBaseColumn`. `ChunkGenerators.bootstrap` registers
  exactly three: `NoiseBasedChunkGenerator` (final — it cannot be
  subclassed), `FlatLevelSource` and `DebugLevelSource`.
- **`NoiseGeneratorSettings`** — the per-dimension record: a `NoiseSettings`
  (min Y, height, and the horizontal/vertical noise sizes that give the cell
  dimensions through `NoiseSettings.getCellWidth` and
  `NoiseSettings.getCellHeight`), the default block and fluid, the
  `NoiseRouter`, the surface `SurfaceRules.RuleSource`, the sea level, and
  the aquifer and ore-vein switches. `NoiseSettings.guardY` enforces that
  the height and minimum are multiples of sixteen.
- **`NoiseChunk`** — the per-chunk workspace, created at
  `ChunkStatus.BIOMES` and cached on `ChunkAccess.getOrCreateNoiseChunk`.
  It holds the wrapped router, the cell interpolators, the `Aquifer`, and
  the `NoiseChunk.BlockStateFiller` chain assembled into a
  `MaterialRuleList`. Its cell walk is
  `NoiseChunk.initializeForFirstCellX`, `NoiseChunk.advanceCellX`,
  `NoiseChunk.selectCellYZ`, `NoiseChunk.updateForY`,
  `NoiseChunk.updateForX`, `NoiseChunk.updateForZ`,
  `NoiseChunk.swapSlices`, `NoiseChunk.stopInterpolation`.
- **`Aquifer`** — what liquid, if any, belongs at a point.
  `Aquifer.NoiseBasedAquifer` samples on a coarse grid, and
  `Aquifer.computeSubstance` turns a density plus its own barrier and
  fluid-level samples into a `BlockState`. `Aquifer.FluidPicker` and
  `Aquifer.FluidStatus` are the global fallback — the sea, and the lava.
- **`OreVeinifier`** — a second block-state filler, active when the settings
  enable it, choosing between its two `OreVeinifier.VeinType`s.
- **`SurfaceSystem`** and **`SurfaceRules`** — the column re-skinning pass.
  `SurfaceRules.RuleSource` is the data-driven rule tree,
  `SurfaceRules.ConditionSource` its predicates, and
  `SurfaceRules.Context` the mutable cursor walking each column with its
  own caches. `SurfaceSystem` owns the noises for badlands bands and
  icebergs, and the two hardcoded extensions
  `SurfaceSystem.erodedBadlandsExtension` and
  `SurfaceSystem.frozenOceanExtension`.
- **Carvers** — `WorldCarver` with its three registered instances
  (`WorldCarver.CAVE`, `WorldCarver.NETHER_CAVE`, `WorldCarver.CANYON`),
  `ConfiguredWorldCarver` pairing one with a `CarverConfiguration`,
  `CarvingContext` (a `WorldGenerationContext` that also carries the noise
  chunk and the surface rule), and `CarvingMask`, the per-chunk bit set.
- **`Beardifier`** and **`Blender`** — the two things that reach into the
  density field from outside: structures ([structures](structures.md)) and
  the boundary with pre-existing chunks. `BelowZeroRetrogen` is the
  world-deepening upgrade path, still live.
- **`Heightmap`** and `Heightmap.Types` — six maps in three
  `Heightmap.Usage` classes. The two worldgen ones are maintained up to
  the carvers step and dropped at save; the four final ones are primed
  before decoration.
- **Randomness** — `RandomState` is the per-level seed root
  (`RandomState.aquiferRandom`, `RandomState.oreRandom`, the noise memo);
  `WorldgenRandom`, `PositionalRandomFactory`, `XoroshiroRandomSource` and
  `LegacyRandomSource` are the sources.

## When it runs

Every step below is on the worldgen executor, which runs **one task at a
time per dimension**. Only two fan out to the background pool —
`ChunkGenerator.createBiomes` (as *init_biomes*) and
`ChunkGenerator.fillFromNoise` (as *wgen_fill_noise*) — and only
`ChunkStatusTasks.full` touches the main thread. `RandomState` is built
once per level in `ChunkMap` and shared by every generating chunk.

Three of the four terrain steps can write blocks, and only within their own
chunk: `ChunkStatus.NOISE`, `ChunkStatus.SURFACE` and `ChunkStatus.CARVERS`
all have a block write radius of zero. Every other status except
`ChunkStatus.FEATURES` has a radius of **minus one** — no write succeeds at
all.

## The trace: one chunk's terrain

```mermaid
sequenceDiagram
    participant CST as ChunkStatusTasks
    participant NBC as NoiseBasedChunkGenerator
    participant NC as NoiseChunk
    participant MRL as MaterialRuleList
    participant AQ as Aquifer
    participant OV as OreVeinifier
    participant SS as SurfaceSystem
    participant WC as WorldCarver
    participant PC as ProtoChunk

    CST->>NBC: createBiomes (init_biomes) — builds the NoiseChunk
    NBC->>NC: forChunk — wrap the router, install caches, create the Aquifer
    CST->>NBC: fillFromNoise (wgen_fill_noise)
    NBC->>NC: initializeForFirstCellX · advanceCellX · selectCellYZ
    loop cells: X outward, Z, Y descending
        NC->>NC: interpolate the eight corners down to one block
        NC->>MRL: getInterpolatedState
        MRL->>AQ: computeSubstance(context, final density)
        MRL->>OV: vein filler — sign of veinToggle picks copper or iron
        MRL-->>NBC: BlockState, or null → the settings' default block
    end
    NBC->>PC: LevelChunkSection.setBlockState directly · heightmaps updated by hand
    CST->>NBC: buildSurface — SURFACE
    NBC->>SS: buildSurface — one rule for the chunk, then 256 columns walked downward
    SS->>PC: replace only where the block is still the default block
    CST->>NBC: applyCarvers — CARVERS
    NBC->>WC: 17×17 source chunks; isStartChunk per carver, then carve into the centre
    WC->>AQ: getCarveState — the aquifer says water, lava or nothing
    WC->>PC: setBlockState · re-skin the dirt below with SurfaceSystem.topMaterial
```

1. **Biomes, and the workspace.** `NoiseBasedChunkGenerator.createBiomes`
   forks to the pool, builds the `NoiseChunk` — wrapping the seeded router
   into chunk-local caches and creating the `Aquifer` and the block-state
   filler chain — and fills the biome palette. **The noise chunk is born one
   status before the terrain needs it**, because the biome sampler wants its
   caches too.
2. **Noise.** `ChunkGenerator.fillFromNoise` forks to the pool and walks
   cells: X outward, Z, and **Y descending**. The eight corner densities of
   each cell come from the interpolators; every block inside is three
   lerps away. For each block, `NoiseChunk.getInterpolatedState` runs the
   `MaterialRuleList` — the aquifer first, then ore veins — and a null from
   both means the settings' default block.
3. **The write does not go through `ChunkAccess.setBlockState`.** The noise fill calls the section
   setter directly with the threading check disabled, and updates the two
   worldgen heightmaps by hand. The surrounding acquire/release pair is a
   concurrent-access assertion, not a lock.
4. **Surface.** `SurfaceSystem.buildSurface` compiles the rule tree once for
   the chunk, then walks each of the 256 columns downward from the worldgen
   surface heightmap, tracking depth below stone and water height in a
   `SurfaceRules.Context`. It writes **only where the existing block is
   still the settings' default block** — so anything the aquifer or the ore
   veins placed is immune. The two biome-keyed extensions for eroded
   badlands and frozen oceans sit outside the rule system entirely.
5. **Carvers.** `ChunkGenerator.applyCarvers` loops over a **17×17
   neighbourhood of source chunks**, asking each configured carver of that
   source chunk's biome whether a cave or canyon *starts* there, and carving
   whatever does into the centre chunk. That reach, not the write radius, is
   why the pyramid is as wide as it is.
6. **Carving asks the aquifer.** `WorldCarver.getCarveState` returns lava
   below the configured lava level and otherwise asks
   `Aquifer.computeSubstance` what belongs at that point. A cave through a
   water table fills with water because the aquifer said so — there is no
   later flood fill. A null answer means "do not carve here at all". If a
   grass or mycelium block was passed on the way down, the dirt below is
   re-skinned through `SurfaceSystem.topMaterial`.
7. **Then decoration**, at `ChunkStatus.FEATURES`
   ([features and placement](features-and-placement.md)), and the rest of
   the ladder to `ChunkStatus.FULL`.

## Interfaces

- **Called by:** `ChunkStatusTasks.generateBiomes`,
  `ChunkStatusTasks.generateNoise`, `ChunkStatusTasks.generateSurface`,
  `ChunkStatusTasks.generateCarvers` and
  `ChunkStatusTasks.generateSpawn`, all through `ChunkStep.apply`.
- **Calls into:** the density-function graph via `NoiseChunk`;
  `BiomeSource`; `StructureManager` for the beardifier;
  `NaturalSpawner.spawnMobsForChunkGeneration` at the spawn step.
- **Crosses the network as:** nothing. Terrain reaches the client as chunk
  payloads only after promotion
  ([what the client is told](../networking/what-the-client-is-told.md)).
- **Data-driven by:** `Registries.NOISE_SETTINGS` (which carries the whole
  router and the surface rules), `Registries.DENSITY_FUNCTION`,
  `Registries.NOISE`, `Registries.CONFIGURED_CARVER`, and the biome's
  carver list. The generator kinds, the carver kinds, and the four surface
  rule sources and eleven conditions are code registries.

## Invariants and surprises

- **Carvers never place air.** They ask the aquifer what belongs at the
  carved position; the water in a flooded cave was decided by the same
  object that decided the water in the stone around it.
- **Ore veins are terrain, not features.** They are the second block-state
  filler in the noise step, so copper and iron veins exist before the
  surface pass and before the carvers. Which vein you get is the **sign** of
  one router function — there is no separate "which ore" noise.
- **The surface pass only replaces the default block.** That identity check
  is why ore veins and aquifer water survive it untouched.
- **The noise lattice is coarse but the shaping is not.** Density is
  evaluated only at cell corners and interpolated between them; the 2-D
  shaping terms behind the caches are exact per column
  ([density functions](density-functions.md)).
- **The `NoiseChunk` outlives the noise step.** Created at the biomes step
  and reused unmodified through noise, surface and carvers — which is what
  makes the aquifer's answers consistent between filling and carving. It is
  never cleared; it dies with the proto chunk.
- **The lava sea is not data-driven.** The sea level moves with the noise
  settings; the lava level below it is a constant in the generator.
- **Carvers use the legacy random source even in a dimension configured for
  the modern one** — the settings' choice only selects the level's root
  random, never the carver's.
- **Most statuses cannot write blocks at all.** The default write radius is
  minus one, which no position satisfies; a write from a step that has not
  declared a radius is logged and dropped.
- **Reading a chunk outside the declared dependencies throws**, with a full
  crash report naming what was generating and what it asked for. There is no
  lazy load and no null return — the reason cascading worldgen is gone.
- **The world-deepening upgrade is still live code**, four years on: it
  wraps the biome resolver, patches bedrock after the noise step, and gates
  the spawn step.
- **`Beardifier` enters by identity, not by call.** The router graph
  contains a marker that computes zero; the noise chunk swaps that exact
  instance for the chunk's real beardifier while wrapping. "Structures
  flatten terrain" is implemented as an object comparison inside a visitor.
- **The flat and debug generators are mostly empty.** `FlatLevelSource`
  implements surface, carvers and spawning as no-ops, and `DebugLevelSource`
  writes its grid at the decoration step rather than the noise step.

## Where to look

`ChunkGenerator` · `ChunkGenerators.bootstrap` ·
`NoiseBasedChunkGenerator.fillFromNoise` · `NoiseGeneratorSettings` ·
`NoiseSettings.getCellWidth` · `NoiseChunk.forChunk` ·
`NoiseChunk.getInterpolatedState` · `MaterialRuleList` ·
`Aquifer.computeSubstance` · `Aquifer.NoiseBasedAquifer` ·
`OreVeinifier.create` · `SurfaceSystem.buildSurface` ·
`SurfaceRules.RuleSource` · `SurfaceRules.Context` ·
`NoiseBasedChunkGenerator.applyCarvers` · `WorldCarver.getCarveState` ·
`CarvingContext` · `CarvingMask` · `Beardifier` · `Blender` ·
`BelowZeroRetrogen` · `Heightmap.Types` · `RandomState.create`

---

*Rules: names, never code · how the system works, not how the code reads ·
newest version only · every backticked name passes `tools/verify_names.py`.*
