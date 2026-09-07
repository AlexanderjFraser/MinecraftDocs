# Features and placement

> Verified against **Minecraft 26.2** · Part XII · A chunk decorates: a stream of positions folded through filters, an order every chunk in the dimension already agreed on, and a data pack that can stop the world from opening.

The oak in the middle of a plains chunk was not placed by the plains biome.
It was placed by a list that every biome in the dimension contributed to,
sorted once at world load into one order per decoration step, with an index
per entry that the random seed for each feature is derived from. That is how the same
seed grows the same forest — and it is also why **two biomes that list the
same two features in opposite orders make the world refuse to open.** The
order is a topological sort of a graph, and a graph can have a cycle.

Decoration is everything the terrain steps did not put there: trees, flowers,
ores, lakes, patches, springs. The system separates three things a modder
usually wants separately — *what* to build, *where* to try, and *who* wants
it — and this page is how those three meet at `ChunkStatus.FEATURES`. All
three are registries of dispatched types, which makes this the largest single
instance of [the data-driven type
pattern](../foundations/data-driven-types.md#the-idea-stated-once) in the
game. The
biggest single feature, the tree, has its own page
([trees](trees.md#one-algorithm-five-slots)); the terrain that decoration
lands on is [terrain](terrain.md#the-two-fillers-what-the-number-becomes).

## The cast

| class | its job | notes |
|---|---|---|
| `Feature` | the algorithm, with one method: `Feature.place`, taking a `FeaturePlaceContext` and returning whether it wrote anything | **63** registered into `BuiltInRegistries.FEATURE` |
| `FeatureConfiguration` | its parameters, per feature type | `NoneFeatureConfiguration` for the ones that need none |
| `ConfiguredFeature` | a feature plus its configuration, and **no position logic at all** | the unit a sapling grows |
| `PlacedFeature` | a configured feature plus an ordered list of modifiers | the unit a biome names — the only one of the three that owns placement modifiers |
| `PlacementModifier` | one function from a position to a *stream* of positions, over a `PlacementContext` | 15 registered types |
| `GenerationStep.Decoration` | the eleven steps, in order, from raw generation to top-layer modification | a biome's list is a list of lists, by ordinal |
| `FeatureSorter` | flattens every possible biome's per-step lists into one sorted list per step, with an index lookup | once per generator, memoised |
| `WorldgenRandom` | the seed, reseeded absolutely twice: once per chunk, then once per feature | on the worldgen executor |

## The trace: a chunk decorates

```mermaid
sequenceDiagram
    participant CST as ChunkStatusTasks
    participant ChunkG as ChunkGenerator
    participant FS as FeatureSorter
    participant WR as WorldgenRandom
    participant PlacedF as PlacedFeature
    participant PMod as PlacementModifier
    participant CF as ConfiguredFeature

    CST->>ChunkG: applyBiomeDecoration — write radius 1, four final heightmaps primed
    ChunkG->>FS: featuresPerStep — one sorted list per step, and an index per PlacedFeature
    ChunkG->>WR: setDecorationSeed(level seed, chunk corner)
    ChunkG->>ChunkG: union the biome palettes of the 3x3 chunks, intersect with possibleBiomes
    Note over ChunkG: per step: structures first, then features in sorted index order
    ChunkG->>WR: setFeatureSeed(decoration seed, feature index, step)
    ChunkG->>PlacedF: placeWithBiomeCheck, from the chunk's minimum corner
    PlacedF->>PMod: fold — each modifier flat-maps one position into zero or more
    PMod-->>PlacedF: the surviving positions
    PlacedF->>CF: place, once per surviving position
    CF->>CF: Feature.place — ensureCanWrite checked once, for the origin
```

**The driver.** `ChunkGenerator.applyBiomeDecoration` starts at the chunk's
minimum corner, at the world's minimum Y. There is no eight-block population
offset; the scatter comes later, from a modifier.

**The seed.** A `WorldgenRandom` is built over a genuinely random seed and
then reseeded absolutely, twice, before anything uses it.
`WorldgenRandom.setDecorationSeed` derives a per-chunk seed from the world
seed and the chunk corner, and each feature then gets
`WorldgenRandom.setFeatureSeed` from that seed, its index within the step and
the step number, which the seed multiplies by ten thousand to keep the steps
apart. Features in a step therefore do *not* share a random stream: every one
is reseeded absolutely before it runs, so an extra draw inside a feature
perturbs the rest of *that* feature and nothing after it.

**Who wants what.** The biome palettes of the surrounding 3×3 chunks are
unioned and intersected with the biome source's possible biomes
([biomes](biomes.md#the-cast)). Every placed
feature any of those biomes lists for this step — the per-step lists on its
`BiomeGenerationSettings` — is collected by its index in
that step's list, and the indices are **sorted** — that sort is the execution order, and
it is the same for every chunk *in that dimension*, because
`ChunkGenerator.featuresPerStep` is memoised per generator and built from
that generator's possible biomes. The Nether's order has nothing to do with
the Overworld's. Within each step, structures at that step are placed before
its features ([structure
placement](structure-placement.md#then-the-blocks-arrive-one-chunk-at-a-time)).

## The fold

`PlacedFeature.placeWithBiomeCheck` starts a stream containing exactly one
position — the chunk corner — and flat-maps it through each modifier in list
order. Nothing about that is a filter chain in the usual sense: a modifier
may return nothing, one position, or many.

```mermaid
flowchart TB
    A["1 position: the chunk corner, at minimum Y"] --> B["RarityFilter — 1 or 0"]
    B --> C["CountPlacement — N copies of the SAME position"]
    C --> D["InSquarePlacement — each scattered inside the 16x16"]
    D --> E["SurfaceWaterDepthFilter — some drop out"]
    E --> F["HeightmapPlacement — Y is finally set, on top of the surface"]
    F --> G["BlockPredicateFilter — would a sapling survive here"]
    G --> H["BiomeFilter — does the biome HERE want this exact feature"]
    H --> I["ConfiguredFeature.place, once per surviving position"]
```

Three things about that chain are load-bearing and none of them is obvious
from a data pack. Four of the modifiers in it are pure filters —
`RarityFilter` at the head, which turns one position into one or none on a
roll; `SurfaceWaterDepthFilter`; `BlockPredicateFilter`, the survival check;
and `BiomeFilter` — and they are what a `PlacementFilter` is: a modifier that
returns the position it was given, or nothing.

**A repeating placement does not scatter.** `CountPlacement`,
`NoiseBasedCountPlacement` and `NoiseThresholdCountPlacement` are
`RepeatingPlacement`s: they emit the *same* position N times, and the scatter
is a separate modifier downstream. List order decides the outcome —
count-then-scatter gives ten trees in ten places, scatter-then-count gives
ten trees in one.

**Y is set late.** Positions travel through most of the chain at the world's
minimum Y; a `HeightmapPlacement` or a `HeightRangePlacement` is what puts
them on the ground, and a chain that forgets one places at the bottom of the
world. `WorldGenRegion.getHeight` returns the stored height **plus one**, so
a heightmap placement lands on top of the surface rather than in it. Two of
vanilla's heightmap presets read the *worldgen* heightmaps, which are not
among the four `ChunkStatusTasks.generateFeatures` primed on the way in
([the six heightmaps](../world/chunk-anatomy.md#the-six-heightmaps)).

**The biome is checked twice.** A feature was selected because *some* biome
in the 3×3 wanted it; `BiomeFilter` re-reads the biome at the scattered
position and asks whether *that* biome's generation settings contain this
exact placed feature. Without it every biome would bleed its trees a chunk in
each direction. Vanilla is not consistent about where it goes: the base tree
placement ends with the biome filter and the survival-checked variant appends
its block predicate *after* it, so both orders ship.

What every one of them is handed is a `PlacementContext`, and it is more
world than anything else in this system gets: the block state at a position,
a heightmap reading, the chunk's carving mask, and — the field the biome
filter needs — which placed feature the chain started from.

The rest of the fifteen modifiers move a position rather than counting or
filtering it: `InSquarePlacement` scatters within the chunk,
`RandomOffsetPlacement` jitters, `EnvironmentScanPlacement` searches up or
down for a surface over a `CaveSurface`, `FixedPlacement` names absolute
positions, and `SurfaceRelativeThresholdFilter` keeps a position only if a
heightmap reading above or below it falls in a range. One of the
fifteen fits neither shape: `CountOnEveryLayerPlacement` is deprecated,
extends `PlacementModifier` directly, and does its own scatter and cave-layer
scan inside `PlacementModifier.getPositions`.

## A feature that is a tree of features

Five of the sixty-three registered features write no blocks of their own.
They take other *placed* features and choose between them, which is how a data
pack builds decoration out of decoration rather than out of algorithms:
`RandomSelectorFeature` walks a weighted list rolling each entry's chance and
falls back to a default; `SimpleRandomSelectorFeature` picks a uniform index;
`WeightedRandomSelectorFeature` draws from a weighted list;
`RandomBooleanSelectorFeature` flips a coin between two;
and `SequenceFeature` places every entry in order and **stops at the first
failure**, reporting failure itself. The plains oak is one of these — a
random selector between a fancy oak, a fallen oak and a plain oak with bees.
(A sixth writes nothing and chooses nothing: `Feature.NO_OP` is a deliberate
blank, and it is what an empty slot in a data pack is spelled as.)

All five call `PlacedFeature.place`, not
`PlacedFeature.placeWithBiomeCheck` — which is exactly why a `BiomeFilter`
inside a nested placed feature is an *error* rather than a no-op. The filter
needs the context's top feature, and only the biome-check entry sets it. That
is why the "checked" tree placements carry no biome filter and the
biome-level ones do.

## What a feature may write, and where it may read

`ChunkStatus.FEATURES` is the only step in the generation pyramid with a
*positive* block write radius, and the radius is one — so a tree may cross
into a neighbour, and nothing else in generation may cross into anything
([four steps may write, and only
four](../world/chunk-generation-pipeline.md#four-steps-may-write-and-only-four)).

What that permission is worth is decided twice, and the second time is this
page's. `Feature.place` checks `WorldGenLevel.ensureCanWrite` for the origin
once, and then each individual write is re-checked by
`WorldGenRegion.ensureCanWrite`, which logs — and pauses, in a development
environment — and does not write. A canopy that would reach two chunks out is
therefore **truncated**, not moved and not abandoned: half a tree, written
without complaint. Reading is looser and then suddenly much stricter. A read
outside the write zone is a warning and still happens; a read past the step's
declared dependency radius — eight chunks at this step, and only of chunks at
`ChunkStatus.STRUCTURE_STARTS` — throws instead of loading, which is what makes
cascading worldgen structurally impossible rather than merely discouraged
([a read too far crashes, a read too wide only
warns](../world/chunk-generation-pipeline.md#a-read-too-far-crashes-a-read-too-wide-only-warns)).

The supporting value types are worth naming because they are handed four
different amounts of world, and the ladder is the whole design. An
`IntProvider` and a `FloatProvider` get a random source and nothing else.
`HeightProvider.sample` and `VerticalAnchor.resolveY` get a
`WorldGenerationContext`, which despite the name is two integers — the world's
minimum Y and its height. A `BlockStateProvider` gets a random source and a
position, and picks the block to write from it. Only `BlockPredicate` sees the
world: it
extends `BiPredicate<WorldGenLevel, BlockPos>`, and that is why a placement
can ask what block is under the sapling. Each of the four is its own registry
of dispatched types, and each is mostly instances: fourteen block predicates,
of which four are boolean combinators over the other ten; six height
providers, which are distribution shapes over one range; eight state
providers, which pick a block from a weight, a noise or a rule. The head of
each family is explained once, here; the members are a catalogue this book
declines ([what this book skips](../anatomy/what-this-book-skips.md)).

## Questions players ask

**How does a datapack make a world refuse to load?** Feature order is global:
every biome's list contributes "this before that" edges to one graph, and
`FeatureSorter.buildFeaturesPerStep` topologically sorts it. Two biomes
listing the same two features in opposite orders form a cycle, and the sort
throws rather than returning an order — it will even re-run itself, dropping
one source at a time, to name the smallest offending set. Where you find out
depends on which side you are: the **client** calls
`ChunkGenerator.validate` from `WorldOpenFlows` while opening the world,
catches the exception and offers safe mode. A dedicated server never calls
`ChunkGenerator.validate` at all, so there the cycle surfaces later, as a
crash report wrapped around the first chunk that tries to decorate.

**Why does a chunk keep changing after it has decorated?** Because all eight
neighbours write into it when *they* decorate, and nothing about the
dependency graph says that is safe — the graph fixes the *order*, not the
exclusion. What makes it safe is that every worldgen task in a dimension is
serialised behind one executor, so no two neighbours are ever inside the
centre chunk at once
([dispatch, and why the parallelism is smaller than the thread
names](../world/chunk-generation-pipeline.md#dispatch-and-why-the-parallelism-is-smaller-than-the-thread-names)).

**Is decoration the only way a feature runs?** No, there are three doors, and
two of them skip this page entirely. A configured feature can be placed
straight from `/place feature`, with no placement layer at all; a sapling
grows through the third.

**Does a sapling grow the same way a worldgen tree does?** No — it skips this
whole page. `SaplingBlock.advanceTree` and bone meal run on the **server main
thread** and call `ConfiguredFeature.place` on the `ServerLevel` directly, so
there is no placement chain, no biome filter and no write guard at all
(`WorldGenLevel.ensureCanWrite` is an interface default that is always true).
It also hand-manages the sapling block, which is a story of its own
([trees](trees.md)).

**Is every `Feature` subclass in the registry?** No, and the exception is a
good one: `EndPodiumFeature` is constructed directly by the dragon fight and
appears in no registry at all. Being a `Feature` and being data-driven are
different things.

**Where are the actual features?** Sixty-three algorithms is the longest tail
in the part — icebergs, geodes, dripstone clusters, lakes, springs, coral,
huge fungi, the End spikes — and none of them is a mechanism this page has not
already explained: each is one `Feature.place` writing blocks from a
configuration, reached the same way as every other. The book names the
framework and declines the catalogue
([what this book skips](../anatomy/what-this-book-skips.md)); the two that do
something structurally different are named where they bite, `OreFeature` on
[chunk anatomy](../world/chunk-anatomy.md#sections-and-their-four-counters)
for holding a section open across many writes, and `TreeFeature` on
[trees](trees.md#one-algorithm-five-slots). A development build can count the
rest: with
`SharedConstants.DEBUG_FEATURE_COUNT` set, `FeatureCountTracker` tallies every
feature placed per level and dumps the table on a key press.

**Are structures and features really the same step?** They share the step
loop and not the index space, so a structure and a feature at the same index
in the same step draw the *same* feature seed. They also differ in reach: a
structure piece gets an explicit writable box covering exactly the centre
chunk, while a feature gets only the softer 3×3 write-zone check.

## Where to look

`Feature.place` · `ConfiguredFeature` ·
`PlacedFeature.placeWithBiomeCheck` · `PlacementModifier.getPositions` ·
`PlacementFilter` · `RepeatingPlacement` · `CountPlacement` ·
`InSquarePlacement` · `HeightmapPlacement` · `BiomeFilter` ·
`RandomSelectorFeature` · `SequenceFeature` ·
`GenerationStep.Decoration` · `FeatureSorter.buildFeaturesPerStep` ·
`ChunkGenerator.applyBiomeDecoration` · `ChunkGenerator.validate` ·
`PlacementContext` · `FeaturePlaceContext` ·
`SurfaceRelativeThresholdFilter` · `BlockStateProvider` ·
`WorldgenRandom.setDecorationSeed` · `WorldgenRandom.setFeatureSeed` ·
`WorldGenRegion.ensureCanWrite` · `WorldGenRegion.getChunk` ·
`BlockPredicate` · `HeightProvider` · `VerticalAnchor` ·
`SaplingBlock.advanceTree`

---

*Rules: names, never code · how the system works, not how the code reads ·
newest version only · every backticked name passes `tools/verify_names.py`.*
