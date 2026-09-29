# Biomes

> Verified against **Minecraft 26.3** · Part XII · A point in the world gets a biome: six numbers quantised to integers, a nearest-neighbour search in seven dimensions, and the two different answers the game keeps for the same block.

Walk out of a desert into a jungle and watch the ground. The grass changes colour along one line, softened over a few blocks. The fog and the sky change along a *different* line, a couple of blocks away, and fade across it over a band several times as wide. Neither is a bug and neither is a rendering artefact:
the game genuinely stores one biome per four-by-four-by-four volume and then
answers "which biome is this block in?" **two different ways**, one jittered
and one not, and different systems ask different questions. The surprise is
which side each thing is on — grass colour, mob spawning and whether water
freezes are all on the *jittered* side, and the sky is not.

A biome is a label in the chunk at quarter resolution — one per
four-by-four-by-four block volume, which this book calls a **quart cell** (the code's *quart*) — plus a bundle of consequences hanging off that label. The
bundle is a thin one: `Biome` itself holds four things, and most of what a
player would call "the biome" lives in the environment-attribute stack, where the biome is
one layer among several rather than the owner
([environment attributes and timelines](../world/environment-attributes-and-timelines.md)).

## The cast

| class | what it decides | when |
|---|---|---|
| `BiomeSource` | which biome a quart cell gets, through the `BiomeResolver` it makes for the chunk fill. `BiomeSources.bootstrap` registers four — `MultiNoiseBiomeSource`, `TheEndBiomeSource`, `FixedBiomeSource` (one biome everywhere, which is what a Single Biome world is, and what a superflat and a *Debug Mode* world use too) and `CheckerboardColumnBiomeSource` (a listed few in squares) — and `BiomeSource.possibleBiomes` is the memoised pre-filter everything else leans on | `ChunkStatus.BIOMES`, on the [worker pool](../../reference/threads.md#the-threads-a-lecture-leans-on) |
| `Climate.Sampler` | the six climate numbers at a point — temperature, humidity, continentalness, erosion, depth and weirdness. `RandomState.createClimateSampler` binds the six to a sampling context, with or without caches: filling a chunk takes a caching one, whose functions `MultiNoiseBiomeSource.createResolverForChunk` samples over the whole chunk at once, and `BiomeSource.createCachingResolver` and `BiomeSource.createUncachedResolver` wrap one for a lookup outside the fill ([density functions](density-functions.md#seed-once-per-dimension)) | once per chunk filled, or per point asked |
| `Climate.ParameterList` | the search space: `Climate.ParameterPoint`s paired with biomes, indexed by a `Climate.RTree` | built at each world load |
| `OverworldBiomeBuilder` | the overworld's parameter table, in Java — temperature, humidity, erosion and continentalness bands over six tables of biome keys | each world load |
| `LevelChunkSection` | where the answer lives: a second `PalettedContainer` keyed by biome holder, two bits per axis | written at generation, saved, shipped |
| `BiomeManager` | the jitter — which biome this *block* gets, as opposed to which cell it is in | every gameplay read |
| `Biome` | four things: climate settings, an `EnvironmentAttributeMap`, `BiomeSpecialEffects` and generation settings | — |
| `EnvironmentAttributeMap` | the biome's contribution to sky, fog, music, the spawn lists and the gameplay switches — as *modifiers*, not values. Twenty-three gameplay attributes exist; the sixty-seven vanilla biome files touch five of them between them — every file sets the spawn lists, and for fifty that is the only one | per attribute, per read |

## Deciding a chunk's biomes, cell by cell

```mermaid
sequenceDiagram
    participant NBC as NoiseBased<br/>ChunkGenerator
    participant MNBS as MultiNoise<br/>BiomeSource
    participant ClimS as Climate.Sampler
    participant CA as ChunkAccess
    participant LCS as LevelChunkSection
    participant CPList as Climate.<br/>ParameterList

    Note over NBC,CPList: ChunkStatus.BIOMES, forked to the worker pool as createBiomes
    NBC->>MNBS: createResolverForChunk, with a caching Climate.Sampler
    MNBS->>ClimS: each of its six functions, sampled over the whole chunk
    ClimS-->>MNBS: a buffer per function, one value per quart cell
    MNBS-->>NBC: a resolver that reads the six buffers
    NBC->>NBC: decorateBiomeResolver, wrap the resolver twice
    NBC->>CA: fillBiomesFromNoise, with the wrapped resolver
    loop per section
        CA->>LCS: fillBiomesFromNoise, into a new container
        loop per quart cell, 64 of them
            LCS->>MNBS: getNoiseBiome, through the resolver
            MNBS->>CPList: findValue, the six buffered values as a Climate.TargetPoint
            CPList->>CPList: findValueIndex, the search down its Climate.RTree
            CPList-->>MNBS: the nearest biome holder
            MNBS-->>LCS: into the new container
        end
    end
```

*A chunk's biomes are the six climate functions sampled once over the whole chunk, then 64 searches per section, each a lookup into those samples and a nearest-neighbour walk; no block is read and none is written.*

The two wrappers `NoiseBasedChunkGenerator.decorateBiomeResolver` adds only do anything beside or inside chunks an older version generated: the blender's beside them ([blending at the old-chunk border](blending.md#what-the-blender-actually-answers)) and `BelowZeroRetrogen`'s inside one being deepened ([the other passenger](blending.md#the-other-passenger)).

**Biomes are decided before terrain, and not for its shape.** `ChunkPyramid` makes
`ChunkStatus.BIOMES`, one chunk out, a requirement of `ChunkStatus.TERRAIN`,
so the order is enforced — but what the terrain step collects from it serves its surface pass alone: the biomes in the three-by-three chunks' palettes (the carvers work theirs out again from the biome source).
**The noise fill never reads a biome.** What makes a jungle and its
terrain agree is that both were computed from the *same* noise router:
four of the six functions in the climate sampler `RandomState.createClimateSampler` binds are the very depth, continents, erosion and ridges functions that shape the land — under the
`Climate.Sampler` names *depth*, *continentalness*, *erosion* and *weirdness*.
Neither was consulted about the other. The biome does not touch a block until
the surface pass, which follows the fill inside the same `ChunkStatus.TERRAIN`
task ([terrain](terrain.md#the-surface-pass-and-the-two-places-it-breaks-its-own-rule)).

The *fork* at the top of that trace is not the noise generator's:
`ChunkGenerator.createBiomes` is the base class's alone and forks to the worker pool, as *createBiomes*, for every generator, so a superflat world leaves the worldgen
executor for its biomes exactly as the overworld does. What
`NoiseBasedChunkGenerator` overrides is one step,
`ChunkGenerator.decorateBiomeResolver`, for its two wrappers; `FlatLevelSource`
and `DebugLevelSource` keep the base one, which wraps nothing. Sampling the
whole chunk up front is the biome source's choice, not the generator's: only
`MultiNoiseBiomeSource` overrides `BiomeSource.createResolverForChunk`, and the
other three sources answer cell by cell through `BiomeSource.createResolver`.
The End is a `NoiseBasedChunkGenerator` like the
overworld and the nether — just with `TheEndBiomeSource` in front of it,
which does not do a climate search at all: it thresholds a single erosion
sample outside a fixed central radius.

## The search, and the axis that is not sampled

`Climate.quantizeCoord` multiplies each of the six climate values by ten
thousand and truncates, so the entire search is integer arithmetic. The
target is a `Climate.TargetPoint` of six longs; each entry in the list pairs a biome with a `Climate.ParameterPoint` of six `Climate.Parameter` intervals, and most biomes have several; and
`Climate.ParameterList.findValue` walks a `Climate.RTree` — up to nineteen
children per node — minimising the sum of squared distances from the target
to each interval.

Except the count is seven, not six. `Climate.PARAMETER_COUNT` is **7** and
`Climate.RTree.create` refuses a point that does not supply seven, because
each `Climate.ParameterPoint` carries a scalar *offset* alongside its six
intervals, and `Climate.TargetPoint.toParameterArray` appends a literal zero
as the seventh coordinate of every query. So the seventh term of the metric
is always that biome's offset squared: a fixed penalty added to its score. It
is a "make this biome harder to win" dial, not anything sampled from the
world.

The tree also remembers. `Climate.RTree` keeps the winning leaf in a
`ThreadLocal` and seeds the next search with it as the initial candidate.
Adjacent quart cells almost always resolve to the same biome, so the walk
usually prunes immediately — which is what makes filling sixty-four cells a
section cheap. The tree is therefore stateful per thread, though never
incorrect: the remembered leaf is only a starting bound.

Which is also the answer to whether a pack can move the overworld's biomes
around: not the vanilla preset. `OverworldBiomeBuilder` is hardcoded Java, and
the data-pack element that would carry it,
`MultiNoiseBiomeSourceParameterList`, serialises to nothing but a preset name —
`MultiNoiseBiomeSourceParameterLists` registers two. A pack may supply its own
parameter list inline for a multi-noise source; it cannot edit the one that
ships.

One thing the parameter table does *not* have is a separate underground
system. `OverworldBiomeBuilder.addUndergroundBiomes` and
`OverworldBiomeBuilder.addBottomBiome` place dripstone caves, lush caves,
sulfur caves and the deep dark into the same seven-dimensional table by their
*depth* band. A
cave biome is an ordinary entry that happens to win only below the surface.

## The two borders

The label goes into the section's second paletted container — two bits per
axis, so **sixty-four biome cells per section**
([sections and their four counters](../world/chunk-anatomy.md#sections-and-their-four-counters)) —
and is shipped to the client
inside the chunk payload. From then on it is *stored*, not computed, which is
why `FillBiomeCommand` can exist at all and why `ClientboundChunksBiomesPacket`
exists to tell the client about the result.

And then two different readers ask for it two different ways.

| | the jittered read | the exact read |
|---|---|---|
| entry point | `LevelReader.getBiome` → `BiomeManager.getBiome` | `BiomeManager.getNoiseBiomeAtPosition`, and on the client `BiomeManager.getNoiseBiomeAtQuart` |
| what it does | offsets by two, takes the eight surrounding quart corners, and picks the one minimising `BiomeManager.getFiddledDistance` — a seeded hash worth up to ±0.45 of a cell per axis | floors to the quart cell and reads the palette |
| who uses it | freezing and precipitation, mob spawning, commands, the surface rules during generation — **and block tint**: grass, foliage and water colour, through `ClientLevel.calculateBlockTint` | the environment-attribute stack, for every attribute but the spawn lists — `EnvironmentAttribute.isFullResolutionBiomes` sends those to the jittered read — and nothing else that goes through `BiomeManager` |
| what it looks like | the ragged border | the straight one |

**Block tint is on the jittered side**, which is the half of this that
surprises people: grass colour comes from the same jittered read as whether snow falls. What softens the colour boundary in game is not the biome
lookup but a box blur on top of it, which the client owns
([the client level](../client/the-client-level.md#the-four-tint-caches-and-the-soft-biome-edge)).
Fog and sky are the ones on the other border.

The client's exact read is the more expensive of the two, and it is spent
**unconditionally**: the probe that feeds the attribute stack runs its
Gaussian pass over the neighbourhood every tick whether or not any attribute
at that position is interpolated at all, because the test is applied later,
when the layer is applied
([the same value on the client](../world/environment-attributes-and-timelines.md#the-same-value-on-the-client)).
The server never interpolates and never pays it — it passes no interpolator.

## What a biome still owns

Four things, and none of them stops being read once the chunk is generated —
`NaturalSpawner` reads the spawn attribute every tick and a bone-mealed grass block
asks the generation settings.

`Biome.climateSettings` is precipitation, a base temperature, a
`Biome.TemperatureModifier` and downfall. Temperature is the interesting one:
`Biome.getHeightAdjustedTemperature` samples noise per block high above sea
level — which is why snow lines are uneven rather than flat — and `Biome`
keeps a fixed-size per-thread cache in front of it that evicts rather than
grows. Most of the public surface is the questions rather than the number:
`Biome.warmEnoughToRain`, `Biome.coldEnoughToSnow`, `Biome.shouldFreeze`,
`Biome.shouldSnow`. `Biome.getBaseTemperature` is the raw, uncached,
unadjusted escape hatch.

`BiomeSpecialEffects` is **only block tint** — five fields, all of
them colours or a grass-colour modifier, and only the water colour is
mandatory. Fog, sky, clouds, ambient sound, music and particles are attributes instead. What is left is read by nothing in the attribute
system at all: `BiomeColors` reaches these five fields through four
`ColorResolver`s, with no probe and no layer stack anywhere in the path
([lightmap, fog and sky](../rendering/lightmap-fog-and-sky.md)). And when the
four optional ones are silent, the grass and foliage tints do not come from the effects at all: they are a lookup into the colormap images by the biome's base temperature and downfall, through `GrassColor`, `FoliageColor` and `DryFoliageColor`. "The
biome's grass colour" is usually just the two climate numbers that index a
texture.

`Biome.getAttributes` returns the `EnvironmentAttributeMap`, and what a biome
puts in it are *modifiers*, not values — which is how a swamp thickens water
fog without naming a distance
([arguments, not values](../world/environment-attributes-and-timelines.md#arguments-not-values)).
One restriction lands here specifically:
`EnvironmentAttributeMap.CODEC_ONLY_POSITIONAL` means a biome may not set a
non-positional attribute at all. And one cost lands on the whole dimension:
a positional layer is built per attribute that **any** biome in the registry
mentions, at level construction
([the stack a value falls through](../world/environment-attributes-and-timelines.md#the-stack-a-value-falls-through)),
and a layer is not free where the biome that wanted it is absent — a biome that names an attribute no other biome does adds a layer every position in every dimension then falls through.

`BiomeGenerationSettings` holds two lists, and they are read by different
pages: the placed features, one set *per decoration step*, by
[features and placement](features-and-placement.md#one-chunks-decoration-from-the-corner-outward),
and the carvers by [terrain](terrain.md#carving-and-who-chooses-the-block), at
a different status. `BiomeGenerationSettings.getBoneMealFeatures` is its only
reader outside worldgen, and its one caller is `GrassBlock`. The spawn lists
are in the attribute map, as `EnvironmentAttributes.NATURAL_MOB_SPAWNS`, which
every biome file sets with a `MobSpawnSettings` argument and `NaturalSpawner`
reads through the attribute stack — though a structure at the position can
replace them outright before the spawner ever looks
([a spawn attempt is a filter](../entities/entity-lifecycle.md#a-spawn-attempt-is-a-filter-not-a-conversation)) —
and the `MobSpawnSettings.SpawnerData` constructor silently rewrites any
miscellaneous-category entity type to pig.

Of the four, the client is given two and a half. `Biome.NETWORK_CODEC` sends
the climate settings, the *syncable* attributes and the effects, and
substitutes empty generation settings; the spawn-list attribute is not
syncable, so features, carvers and spawn lists never cross the wire. And when
a client asks for a biome in a chunk it does not have, it gets plains.

## Questions players ask

**Why do I always spawn near the origin?** Because the *chunk* is chosen by a climate search. The search runs every time the world is loaded, since the structure state of a dimension whose settings name a spawn target asks for its result, but only a brand-new world takes a spawn from it, running the search a second time to do so ([building the levels](../server/starting-a-server.md#building-the-levels) owns *when*). `NoiseSpawnFinder.findSpawnPosition` looks for the point whose
climate best matches the noise settings' spawn target — a list of
`SpawnTargetPoint`s, each a set of intervals on named density functions, for
the overworld five of the six climate functions with depth left out — in two spiral passes, the first out to 2,048 blocks and the second a finer one around its best, with the fitness
deliberately biased toward the origin so that a tie lands near 0,0.
`NoiseBasedChunkGenerator.getOrigin` keeps only that answer's chunk, and
`MinecraftServer` does a terrain search from it: an eleven-by-eleven chunk
spiral of `PlayerSpawnFinder.getSpawnPosInChunk`, over a first guess taken from
`ChunkGenerator.getSpawnHeight` or, failing that, the *WORLD_SURFACE*
heightmap. A dimension whose settings name no spawn target skips the climate
half and starts that spiral at the origin chunk.

**Why does `/locate biome` find biomes in chunks I have never visited?**
Because it asks the generator, not the world. `BiomeSource.findClosestBiome3d`
spirals through a resolver from `BiomeSource.createCachingResolver` and never
reads a palette — so it finds biomes in ungenerated chunks and will **never**
find one placed by `/fillbiome`. It pre-filters against
`BiomeSource.possibleBiomes`, so asking for an impossible biome fails
instantly rather than after a spiral out to six thousand four hundred blocks.

> **For a 1.21-era reader.** *Biome.getMobSettings* is gone: the spawn lists are the
> attribute `EnvironmentAttributes.NATURAL_MOB_SPAWNS`. `BiomeSource` is not itself a
> `BiomeResolver`; it makes one. *RandomState.sampler* and
> *NoiseChunk.cachedClimateSampler* are gone; `RandomState.createClimateSampler` does their
> work. *Climate.findSpawnPosition* is `NoiseSpawnFinder.findSpawnPosition`.

## Where to look

`BiomeResolver.getNoiseBiome` is the one method the whole search hangs off, and
`BiomeSource.createResolver` and `BiomeSource.createResolverForChunk` are where a
source makes one; read them with `MultiNoiseBiomeSource` beside them, and
`TheEndBiomeSource` after, for the source that does no search at all. Then
`Climate` whole — it is one file holding `Climate.Sampler`, `Climate.quantizeCoord`,
`Climate.ParameterList.findValue` and the `Climate.RTree` — and
`Climate.PARAMETER_COUNT` is the line that explains the seventh dimension.
`OverworldBiomeBuilder.addBiomes` is vanilla's table, in Java, and
`OverworldBiomeBuilder.addUndergroundBiomes` is where the cave biomes turn out
not to be a separate system. For the two reads, `BiomeManager.getBiome` against
`BiomeManager.getNoiseBiomeAtPosition`, with `BiomeManager.getFiddledDistance`
as the jitter itself. Finish at `Biome`, which is short, and at
`LevelChunkSection.fillBiomesFromNoise` for where the answer is stored. Two
doors the page does not open: `BiomeColors`, for how the five effects fields
reach a rendered block, and `Climate.RTree.search`, for the walk the page only
describes.

---

*Rules: names, never code · how the system works, not how the code reads ·
newest version only · every backticked name passes `tools/verify_names.py`.*
