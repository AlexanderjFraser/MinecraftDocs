# The worldgen pipeline

> Verified against **Minecraft 26.2** · Part XII · One chunk's terrain: noise cells filled from an interpolated lattice, an aquifer that decides what liquid belongs where, ore veins placed before the surface exists, and carvers that let the aquifer choose the block.

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
  `Heightmap.Usage` classes. Which two are live is a property of the
  *status*, not of the step: `ChunkStatus` registers every status up to and
  including `ChunkStatus.SURFACE` with the worldgen pair and
  `ChunkStatus.CARVERS` onward with the four final ones. A proto chunk
  saved at noise or surface therefore really does persist its worldgen
  heightmaps; they stop being written from the carvers status on.
- **Randomness** — `RandomState` is the per-level seed root
  (`RandomState.aquiferRandom`, `RandomState.oreRandom`, the noise memo);
  `WorldgenRandom`, `PositionalRandomFactory`, `XoroshiroRandomSource` and
  `LegacyRandomSource` are the sources.

## When it runs

Every step below is on the worldgen executor, which runs **one task at a
time per dimension**, and only `ChunkStatusTasks.full` touches the main
thread. Two steps fan out to the background pool, and only for the noise
generator: `NoiseBasedChunkGenerator.createBiomes` (as *init_biomes*) and
`NoiseBasedChunkGenerator.fillFromNoise` (as *wgen_fill_noise*).
`FlatLevelSource` and `DebugLevelSource` complete both inline.
`RandomState` is built once per level in `ChunkMap` and shared by every
generating chunk — and it owns the `SurfaceSystem`, which is therefore
per-level, not per-chunk.

Three of the four terrain steps declare a block write radius of zero —
`ChunkStatus.NOISE`, `ChunkStatus.SURFACE` and `ChunkStatus.CARVERS` — and
every status except `ChunkStatus.FEATURES` (radius one) otherwise declares
**minus one**, which no position satisfies. The subtlety is that none of
the three terrain steps writes *through* `WorldGenRegion.setBlock` at all:
they hold the `ChunkAccess` and write to it directly, so
`WorldGenRegion.ensureCanWrite` never gates them. For those steps the
declared radius only governs **reads**, through
`WorldGenRegion.warnIfReadOutsideWriteZone`. The radius is a real guard at
`ChunkStatus.FEATURES`, where features do go through the region.

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
    NBC->>PC: LevelChunkSection.setBlockState directly, non-air only · heightmaps by hand
    CST->>NBC: buildSurface — SURFACE
    NBC->>SS: buildSurface — one rule for the chunk, then 256 columns walked downward
    SS->>PC: replace only where the block is still the default block
    CST->>NBC: applyCarvers — CARVERS
    NBC->>WC: 17×17 source chunks; isStartChunk per carver, then carve into the centre
    WC->>AQ: getCarveState — aquifer answers air, water, lava or null (don't carve)
    WC->>PC: setBlockState · re-skin the dirt below via CarvingContext.topMaterial
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
   whatever does into the centre chunk. That reach costs the pyramid
   nothing: the neighbours are read only as memo holders for
   `ChunkAccess.carverBiome`, and the biome itself is recomputed from the
   biome source. The pyramid is eight chunks wide because every step
   through `ChunkStatus.FEATURES` declares
   `ChunkStatus.MAX_STRUCTURE_DISTANCE`, not because of the carvers.
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

- **A carver does not choose the block it carves — the aquifer does.**
  `WorldCarver.getCarveState` asks `Aquifer.computeSubstance` with a density
  of zero, and `Aquifer.FluidStatus.at` answers plain air above the local
  water table, the fluid below it, or null for "do not carve here". So the
  water in a flooded cave was decided by the same object that decided the
  water in the stone around it — but a dry cave is still the carver writing
  air, one block at a time. The nether carver is the exception that proves
  it: `NetherWorldCarver` overrides `WorldCarver.carveBlock`, never consults the
  aquifer, and writes lava below `minGenY + 31` and cave air above.
- **Carving is gated on a data-driven block set.**
  `WorldCarver.canReplaceBlock` tests the configuration's *replaceable*
  `HolderSet`, so what a cave may eat through is a data-pack decision —
  which is also what stops a carver from hollowing out an ore vein it was
  not told about.
- **Ore veins are terrain, not features.** They are the second block-state
  filler in the noise step, so copper and iron veins exist before the
  surface pass and before the carvers. Which vein you get is the **sign** of
  one router function — there is no separate "which ore" noise.
- **The surface pass only replaces the default block — except at both ends
  of itself.** The column walk really does gate every write on the existing
  block still being the settings' default, which is why ore veins and
  aquifer water survive it untouched. The two hardcoded extensions do not
  play by that rule: `SurfaceSystem.erodedBadlandsExtension` runs *before*
  the walk and fills air with the default block to raise the pillars, and
  `SurfaceSystem.frozenOceanExtension` runs *after* it and writes snow and
  packed ice over air **and over water**, ungated.
- **Almost nothing here is evaluated per block, and the lattice is coarser
  than the famous one.** Only the terms explicitly marked *interpolated* —
  the 3-D base noise and the ore-vein trio — come from the eight-corner
  lerp; the final density is wrapped in a *cache_all_in_cell* that is
  filled for every block in the cell. Meanwhile the 2-D shaping terms
  (continentalness, erosion, ridges, the splines) sit behind *flat_cache*,
  which samples once per **4×4 block column group** at y = 0 and reuses
  that value for all sixteen columns. Only *cache_2d* is exact per column.
  "Minecraft terrain is a lattice" is true twice over, at two different
  resolutions ([density functions](density-functions.md)).
- **The `NoiseChunk` outlives the noise step, but not intact.** The same
  instance is created at the biomes step and reused through noise, surface
  and carvers — which is what makes the aquifer's answers consistent
  between filling and carving. It is heavily mutated along the way, and
  `NoiseChunk.stopInterpolation` at the end of the fill *disarms* it: from
  the surface step on, sampling an interpolator throws. What survives for
  reuse is the aquifer's grid cache and the preliminary surface level. It
  is never cleared; it dies with the proto chunk. Nor is it pinned to one
  thread — the stages run on different workers, and what serialises them is
  the chunk-status future chain, not thread affinity.
- **The lava sea is not data-driven.** The sea level moves with the noise
  settings; the lava level below it is a constant in the generator.
- **Carvers use the legacy random source even in a dimension configured for
  the modern one** — `NoiseBasedChunkGenerator.applyCarvers` hardcodes a
  `LegacyRandomSource`. The settings' `NoiseGeneratorSettings.useLegacyRandomSource`
  reaches further than the level's root random, though: it also re-seeds
  `BlendedNoise` and the legacy nether biome noises, and it changes the *Y*
  at which the surface pass samples a column's biome.
- **Most statuses cannot write blocks at all.** The default write radius is
  minus one, which no position satisfies; a write from a step that has not
  declared a radius is logged and dropped. This bites features, not the
  terrain steps — see *when it runs* above.
- **Reading a chunk outside the declared dependencies throws**, with a full
  crash report naming what was generating and what it asked for. There is no
  lazy load and no null return — the reason cascading worldgen is gone.
- **The world-deepening upgrade is still live code**, four years on: it
  wraps the biome resolver, patches bedrock after the noise step, and gates
  the spawn step.
- **`Beardifier` enters by identity, not by call — and not from the data.**
  `NoiseChunk`'s constructor adds `DensityFunctions.BeardifierMarker` to the
  router's final density itself, then swaps that exact instance for the
  chunk's real `Beardifier` while wrapping. So every noise dimension is
  beardified whether or not its router JSON ever mentions a beardifier, and
  "structures flatten terrain" is implemented as an object comparison
  inside a visitor.
- **The flat and debug generators are mostly empty.** Both implement
  surface, carvers and spawning as no-ops, and `DebugLevelSource` writes
  its grid at the decoration step rather than the noise step.
- **The height queries build a throwaway world.**
  `NoiseBasedChunkGenerator.iterateNoiseColumn`, behind
  `ChunkGenerator.getBaseHeight` and `ChunkGenerator.getBaseColumn`,
  constructs a one-cell `NoiseChunk` with an empty `Blender` and the bare
  beardifier marker. So the height a structure consults when deciding where
  to sit is the terrain *before* beardifying and blending — the ground it
  is about to change.
- **Every arrow in this trace has a debug switch behind it.**
  `SharedConstants` carries flags that disable the surface pass, the
  carvers, the aquifers, the ore veins and fluid generation outright, plus
  visualisation modes that make the aquifer and the ore veins write marker
  blocks instead of real ones.
- **Aquifer water is scheduled, not static.** `Aquifer` marks positions for
  post-processing as it places fluid, so what looks like a settled water
  table becomes real fluid ticks when the chunk is promoted — which is why
  "there is no later flood fill" is true of worldgen and not of the chunk's
  first moments as a live chunk.

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
