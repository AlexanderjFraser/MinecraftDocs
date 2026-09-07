# Terrain

> Verified against **Minecraft 26.2** · Part XII · One chunk's rock: seven hundred and sixty-eight cells filled from their corners, a water table decided before the caves are cut, and the cave that fills with water because of it.

You dig into a cave and it is flooded. The water is not a fluid that flowed
in and settled; nothing flowed anywhere. Before the cave existed, while the
chunk was still solid stone, something decided that a point at that depth in
that column belongs to water rather than to air — and when the carver came
through and asked what to put in the hole it was digging, that answer was
still on file. **A carver does not choose the block it carves.** It chooses
the *shape*; the `Aquifer` chooses the material, and it chose it for the
stone as well.

This page is the three chunk statuses that turn a scalar field into blocks —
`ChunkStatus.NOISE`, `ChunkStatus.SURFACE` and `ChunkStatus.CARVERS`, plus
the workspace that `ChunkStatus.BIOMES` quietly builds before any of them.
The conveyor that runs the statuses, the dependency pyramid and the
threading are [the chunk generation
pipeline](../world/chunk-generation-pipeline.md#the-pyramid-drawn) in Part IV;
this is the
cargo. The scalar field itself is [density
functions](density-functions.md#three-forms-of-one-graph), and the labels that
steer the surface pass are [biomes](biomes.md#the-trace-a-chunks-biomes).

## The cast

| class | what it decides | when |
|---|---|---|
| `ChunkGenerator` | the API the statuses call — `ChunkGenerator.fillFromNoise`, `ChunkGenerator.buildSurface`, `ChunkGenerator.applyCarvers`. `ChunkGenerators.bootstrap` registers exactly three implementations | worldgen executor |
| `NoiseGeneratorSettings` | the whole per-dimension recipe: the `NoiseSettings` cell dimensions, the default block and fluid, the `NoiseRouter`, the surface rules, the sea level, the aquifer and ore-vein switches | data, loaded with the world |
| `NoiseChunk` | the per-chunk workspace — the wrapped router, the cell interpolators, the `Aquifer`, the filler chain | built at `ChunkStatus.BIOMES`, dies with the chunk |
| `MaterialRuleList` | which filler answers first: the aquifer, then the ore veins | inside the cell loop |
| `Aquifer` | what liquid, if any, belongs at a point — and therefore what a carver may leave behind | noise *and* carvers |
| `OreVeinifier` | copper or iron, from the sign of one router function | inside the cell loop |
| `SurfaceSystem` | the column re-skin: grass over dirt over stone, sand, the badlands bands | `ChunkStatus.SURFACE`, one instance per level |
| `WorldCarver` | the shape of caves and canyons, and nothing about their contents | `ChunkStatus.CARVERS` |

Everything here runs on the worldgen executor, and two of these steps fan out
from it — the biome fill for every generator, the noise fill for this one
([which steps fork, and why the parallelism is smaller than the thread
names](../world/chunk-generation-pipeline.md#dispatch-and-why-the-parallelism-is-smaller-than-the-thread-names)).
What is worth carrying from that into this page is one object.
`RandomState` — the per-level seed root — is built once in `ChunkMap` and
shared by every generating chunk, and it owns the `SurfaceSystem`, which is
therefore per **level**, not per chunk.

## Four statuses, and what each hands on

```mermaid
flowchart LR
    BIO["BIOMES"] -- "the NoiseChunk, with its caches and its Aquifer" --> NOI["NOISE"]
    NOI -- "solid rock, two worldgen heightmaps" --> SUR["SURFACE"]
    SUR -- "a skin, and a preliminary surface level" --> CAR["CARVERS"]
    CAR -- "holes, and a CarvingMask" --> FEA["FEATURES"]
```

The odd arrow is the first one. **The workspace is born one status before
the terrain needs it**, because the biome sampler wants the chunk's caches
too ([biomes](biomes.md#the-trace-a-chunks-biomes) reads the climate functions
through `NoiseChunk.cachedClimateSampler`). So `NoiseChunk.forChunk` runs at
`ChunkStatus.BIOMES`, wrapping the seeded router into chunk-local caches and
constructing the `Aquifer` and the `NoiseChunk.BlockStateFiller` chain,
before a single block exists. Two things depend on that one status of slack:
the beardifier is built with the workspace, so a structure has bent the
density field before the field is ever sampled
([structure placement](structure-placement.md#the-ground-bends-and-then-the-blocks-arrive)),
and the blender that reaches the density graph is the one built here rather
than at any later step
([blending](blending.md#following-one-chunk-through)).

That one instance then serves all three terrain steps, which is exactly what
makes the aquifer's answers agree between filling and carving. It is heavily
mutated on the way — and `NoiseChunk.stopInterpolation`, at the end of the
noise fill, *disarms* it: from the surface step onward, an interpolator
sampled with the `NoiseChunk` itself as the context throws, while every other
context is served by the wrapped function
([the caches, and which of them a single point may use](density-functions.md#the-six-caches-and-the-three-a-single-point-may-use)).
What survives for reuse is the aquifer's grid cache and
the preliminary surface level. It is never cleared and it is not pinned to a
thread; the three steps run as separate tasks on whichever worker takes
them, and what serialises them is the chunk-status future chain rather than
thread affinity.

## Filling the noise: six loops, one number at the bottom

The overworld's `NoiseSettings` asks for a horizontal noise size of one and
a vertical size of two, and `NoiseSettings.getCellWidth` and
`NoiseSettings.getCellHeight` turn those into blocks by multiplying by four.
So the unit of overworld terrain is a cell **four blocks wide, four deep and
eight tall**, and a chunk is four by four by forty-eight of them.

**768** — cells in one overworld chunk, each holding 128 blocks
(`NoiseBasedChunkGenerator.fillFromNoise`).

`NoiseChunk` evaluates the *interpolated* density terms at cell **corners**
only. Everything inside a cell is three linear interpolations away from the
eight corners around it, and the walk that does this is six loops deep:

```mermaid
flowchart TB
    subgraph CX["for each of the 4 cell columns in X: advanceCellX fills the next corner slice, swapSlices drops the old one"]
    subgraph CZ["for each of the 4 cell rows in Z"]
    subgraph CY["for each of the 48 cells in Y, downward: selectCellYZ loads its eight corner values"]
    subgraph BY["for each of the 8 block layers in the cell, downward: updateForY"]
    subgraph BX["for each of the 4 blocks across in X: updateForX"]
    BZ["for each of the 4 blocks across in Z: updateForZ, then getInterpolatedState — one block decided"]
    end
    end
    end
    end
    end
```

Read the nesting as the cost model. The two outer levels are where the
sampling happens — a slice of corner values is filled per cell column and
dropped one column later — and everything below `NoiseChunk.selectCellYZ`
is arithmetic on eight numbers. Counting the slices, one *interpolated* term
is sampled five times five times forty-nine per chunk:

**1,225** — corner samples per interpolated density term, per chunk
(`NoiseChunk.fillSlice`, five slices of five by forty-nine).

The Y direction runs **downward** at both nesting levels, which matters
because the two worldgen heightmaps are updated as blocks are written and
the first non-air block seen from the top is the answer.

**Eight** — *interpolated* terms in the overworld router, resolved through
every reference: one round the whole final-density subtree, four inside the
noodle-cave graph, and three across the two vein terms. *vein_gap* is not one
of them, and neither is the aquifer's barrier, which the `Aquifer` samples per
block. Those eight are the only terms this loop reads at cell corners; the
final density is then wrapped in a *cache_all_in_cell* and filled for every
block in the cell. Everything else in the router is sampled at a resolution of
its own, and the resolutions are coarser than the names suggest
([the caches, and which of them a single point may
use](density-functions.md#the-six-caches-and-the-three-a-single-point-may-use)).

The write at the bottom of the loop skips air entirely — a chunk starts empty,
so only non-air is ever written — and updates
`Heightmap.Types.OCEAN_FLOOR_WG` and `Heightmap.Types.WORLD_SURFACE_WG` by
hand rather than through the chunk's ordinary write path. It can, because it
holds every section across its noise range for the whole fill
([what placing a block actually does](../world/chunk-anatomy.md#what-placing-a-block-actually-does)).

## The two fillers: what the number becomes

`NoiseChunk.getInterpolatedState` does not read the density and compare it
to zero. It runs the `MaterialRuleList` — a chain of
`NoiseChunk.BlockStateFiller`s — and takes the first non-null answer. There
are two of them, in this order.

**The aquifer.** `Aquifer.computeSubstance` receives the final density and
decides, from its own barrier and fluid-level noises sampled on a coarse
grid, whether this point is stone, air, or a fluid. It takes five of the
router's fifteen functions: those four noises, and *preliminary_surface_level*,
which it samples at a single point per column through
`NoiseChunk.preliminarySurfaceLevel` to know roughly where the ground is
before any ground exists. `Aquifer.FluidPicker`
and `Aquifer.FluidStatus` are the global fallback underneath its local water
tables — the sea, and the lava. `Aquifer.NoiseBasedAquifer` is the real
implementation; a dimension with aquifers switched off gets a trivial one.

**The ore veins.** `OreVeinifier` is the second filler, active only when the
settings enable it, and it is why copper and iron veins are *terrain rather
than decoration*: they exist before the surface pass and before the carvers,
and no feature places them. Every other ore in the game is an `OreFeature`
placed at `ChunkStatus.FEATURES`
([features and placement](features-and-placement.md#what-a-feature-may-write-and-where-it-may-read)).
Which of the two `OreVeinifier.VeinType`s you
get is the **sign** of one router function, `NoiseRouter.veinToggle` — there
is no separate "which ore" noise.

If both fillers return nothing, the block becomes the settings' default
block. And `Aquifer` marks the positions where it placed fluid for
post-processing, so the settled water table you can see in a cross-section
becomes real fluid ticks the moment the chunk is promoted — which is why
"nothing flowed in" is a true statement about worldgen and not about the
chunk's first live tick
([scheduled ticks](../world/scheduled-ticks.md#appointments-that-survive-a-restart)).

## The surface pass, and the two places it breaks its own rule

`SurfaceSystem.buildSurface` compiles the **dimension's**
`NoiseGeneratorSettings.surfaceRule` tree once for the whole chunk — one rule
tree per dimension, which then branches on biome inside itself, then walks each of the 256 columns downward
from the worldgen surface heightmap, tracking depth below stone and water
height in a `SurfaceRules.Context` that carries its own caches. Every write
is gated on the existing block still being the settings' **default block**,
which is what makes ore veins and aquifer water immune to being turned into
grass.

That rule tree is itself two registries of data-driven types inlined into the
noise settings — `SurfaceRules.RuleSource` for what to write and
`SurfaceRules.ConditionSource` for when, each dispatched on a type id like any
other ([the data-driven type
pattern](../foundations/data-driven-types.md#the-idea-stated-once)) — so a
pack composes a surface out of the shipped conditions and cannot write a new
kind of condition. The biome the tree branches on is the *jittered* read,
`BiomeManager.getBiome`, not the palette's exact one
([the two borders](biomes.md#the-two-borders)), which is why a surface rule
can change block for block along the same ragged line the grass colour does.

Two things sit outside the rule system entirely, and neither obeys that
gate. `SurfaceSystem.erodedBadlandsExtension` runs *before* the column walk
and fills air with the default block to raise the terracotta pillars.
`SurfaceSystem.frozenOceanExtension` runs *after* it and writes snow and
packed ice over air **and over water**, ungated. Both are selected by biome
rather than by rule, and `SurfaceSystem` owns the noises they need along
with the ones for the badlands bands and the icebergs.

## Carving, and who chooses the block

`ChunkGenerator.applyCarvers` does not carve the chunk it was given from the
chunk it was given. It loops over a **17×17 neighbourhood of source
chunks**, asks each configured carver of that source chunk's biome whether a
cave or a canyon *starts* there, and carves whatever does into the centre
chunk. That reach costs the dependency pyramid nothing: the neighbours are
read only as memo holders for `ChunkAccess.carverBiome`, and the biome
itself is recomputed from the biome source. The reach is already paid for,
because every generation step from `ChunkStatus.STRUCTURE_REFERENCES` to
`ChunkStatus.FEATURES` asks for structure starts eight chunks out anyway
([the pyramid, drawn](../world/chunk-generation-pipeline.md#the-pyramid-drawn)).

Three carvers are registered — `WorldCarver.CAVE` and `WorldCarver.CANYON`,
which are `CaveWorldCarver` and `CanyonWorldCarver`, and
`WorldCarver.NETHER_CAVE`, which is the odd one below — each paired with a
`CarverConfiguration` as a
`ConfiguredWorldCarver`, reading the world through a `CarvingContext` and
recording what they touched in a `CarvingMask`, the per-chunk bit set. The
two configuration classes, `CaveCarverConfiguration` and
`CanyonCarverConfiguration`, are the data-pack half, and each carries a
`CarverDebugSettings` that a development build can turn on to write marker
blocks instead of real ones.

And then the hook. `WorldCarver.getCarveState` returns lava below the
configuration's own `CarverConfiguration.lavaLevel`, and otherwise asks
`Aquifer.computeSubstance` with a
density of **zero** what belongs at this point. `Aquifer.FluidStatus.at`
answers plain air above the local water table and the fluid below it — never
null; the null is `Aquifer.computeSubstance`'s own, and it means *do not carve
here at all*. So the water in a flooded cave
was decided by the same object that decided the water in the stone around
it, and a dry cave is the carver writing air one block at a time because the
aquifer told it to. What a cave may eat through is itself a data-pack
decision: `WorldCarver.canReplaceBlock` tests the configuration's
*replaceable* `HolderSet`, which is also what stops a carver from hollowing
out an ore vein it was not told about. If a grass or mycelium block was
passed on the way down, the dirt below is re-skinned through
`SurfaceSystem.topMaterial`.

`NetherWorldCarver` is the exception that proves the rule. It overrides
`WorldCarver.carveBlock`, never consults the aquifer at all, and writes lava
below thirty-one blocks above the dimension's minimum and cave air above.

## Questions players ask

**Why is there always lava at the same depth, in every world?** Because the
two levels are anchored to different things. The sea level is a field of the
noise settings and moves with them; the lava a carver leaves behind is
`CarverConfiguration.lavaLevel`, a `VerticalAnchor` on the *configured carver*
rather than on the dimension — and all four shipped configured carvers anchor
it eight blocks above the world's **bottom**, not below its sea. A data pack
could move it; nothing in vanilla does, and changing the sea level would not.

**Do the caves change if I switch the dimension to the modern random
source?** Not their seeding.
`NoiseBasedChunkGenerator.applyCarvers` hardcodes a `LegacyRandomSource`
whatever the settings say. The settings'
`NoiseGeneratorSettings.useLegacyRandomSource` reaches further than the
level's root random in one other way, though: it re-seeds `BlendedNoise`, and
it changes the *Y* at which the surface pass samples a column's biome. The
legacy nether biome noises are not part of that — `RandomState`'s wiring
visitor builds those two from a `LegacyRandomSource` whatever the setting
says.

**Where does the flat shelf under a village come from?** From this page's
density field, not from any block edit. The beardifier is a node spliced into
the router in code and swapped for the chunk's real `Beardifier` during the
per-chunk rewrite
([wrap: once per chunk](density-functions.md#wrap-once-per-chunk)), so what a
village does to the ground is a term added to a scalar field, decided before
the cell loop reads it. What that term's shape is —
`Beardifier.Rigid` boxes, junctions at half weight, and the five
`TerrainAdjustment` modes — is
[structure placement](structure-placement.md#the-ground-bends-and-then-the-blocks-arrive).

**What height does a structure think the ground is at, then?** The one
*before* it changes it. `NoiseBasedChunkGenerator.iterateNoiseColumn`,
behind `ChunkGenerator.getBaseHeight` and `ChunkGenerator.getBaseColumn`,
builds a throwaway one-cell `NoiseChunk` with an empty
`Blender` and the
bare beardifier marker, samples a column, and discards it.

**What happens at the boundary with chunks generated by an older version?**
`Blender` reads `BlendingData` harvested from the neighbours and enters the
density graph as three nodes — [blending at the old-chunk
border](blending.md#one-measurement-five-consumers) is the page for it, and
for [`BelowZeroRetrogen`](blending.md#the-other-passenger), the
world-deepening path that rides the same hooks: it wraps the biome
resolver, patches bedrock after the noise step, and gates the spawn step.

**Is any of this really running in a superflat world?** Almost none of it.
`FlatLevelSource` and `DebugLevelSource` implement surface, carvers and
spawning as no-ops, and `DebugLevelSource` writes its state grid at the
decoration step rather than the noise step. Development builds can switch
off much more: `SharedConstants` carries flags that disable the surface
pass, the carvers, the aquifers, the ore veins and fluid generation
outright, plus visualisation modes that make the aquifer and the ore veins
write marker blocks instead of real ones.

**Why does a half-generated chunk have the wrong heightmaps in it?**
Because which two are live is a property of the *status*, not of the step —
the two *_WG* maps up to `ChunkStatus.SURFACE`, the four final ones from
`ChunkStatus.CARVERS` on
([the six heightmaps](../world/chunk-anatomy.md#the-six-heightmaps)). The
consequence for this page is that the two maps the noise fill maintains by
hand stop being written one status after the fill ends, and a chunk saved
mid-generation really does persist them.

## Where to look

`ChunkGenerator` · `ChunkGenerators.bootstrap` ·
`NoiseBasedChunkGenerator.fillFromNoise` · `NoiseGeneratorSettings` ·
`NoiseSettings.getCellWidth` · `NoiseChunk.forChunk` ·
`NoiseChunk.fillSlice` · `NoiseChunk.getInterpolatedState` ·
`NoiseChunk.stopInterpolation` · `MaterialRuleList` ·
`Aquifer.computeSubstance` · `Aquifer.NoiseBasedAquifer` ·
`OreVeinifier.create` · `SurfaceSystem.buildSurface` ·
`SurfaceRules.RuleSource` · `SurfaceRules.ConditionSource` ·
`SurfaceRules.Context` · `CarverConfiguration.lavaLevel` ·
`NoiseBasedChunkGenerator.applyCarvers` · `CaveWorldCarver` ·
`WorldCarver.getCarveState` ·
`WorldCarver.canReplaceBlock` · `CarvingContext` · `CarvingMask` ·
`Beardifier` · `Blender` · `BelowZeroRetrogen` · `Heightmap.Types` ·
`RandomState.create`

---

*Rules: names, never code · how the system works, not how the code reads ·
newest version only · every backticked name passes `tools/verify_names.py`.*
