# Biomes

> Verified against **Minecraft 26.2** · Part XI · A point in the world gets a biome: a climate sample, a nearest-neighbour search in seven dimensions, and the two different answers the game keeps for the same block.

## Responsibility

A biome is a label stored in the chunk at quarter resolution, and a bundle
of consequences attached to that label: which features decorate, which mobs
spawn, whether water freezes, what colour the grass is, and — through the
environment-attribute stack — what the sky looks like. In 26.2 the bundle
has been hollowed out. `Biome` holds five things and most of what a player
would call "the biome" now lives in `EnvironmentAttributeMap`, where the
biome is one layer among several rather than the owner.

The one sentence a player recognises: *the line where the desert becomes
the jungle* — and this page's best surprise is that there are two such
lines, a couple of blocks apart, and different systems use different ones.

## The data it owns

- **`Biome`** — a final class (not a record), built only through
  `Biome.BiomeBuilder`, holding exactly five things:
  `Biome.climateSettings` (the private record `Biome.ClimateSettings`:
  precipitation, temperature, `Biome.TemperatureModifier`, downfall),
  `Biome.attributes` (an `EnvironmentAttributeMap`), `Biome.specialEffects`,
  `Biome.generationSettings` and `Biome.mobSettings`. Plus one
  `ThreadLocal` temperature cache.
- **`BiomeSpecialEffects`** — in 26.2 this is **only block tint**: five
  fields, `BiomeSpecialEffects.waterColor`,
  `BiomeSpecialEffects.foliageColorOverride`,
  `BiomeSpecialEffects.dryFoliageColorOverride`,
  `BiomeSpecialEffects.grassColorOverride` and
  `BiomeSpecialEffects.grassColorModifier`. Fog, sky, clouds, ambient
  sound, music and particles have all left it
  ([lightmap, fog and sky](../client/lightmap-fog-and-sky.md)).
- **`EnvironmentAttributeMap`** — what `Biome.getAttributes` returns. Each
  `EnvironmentAttributeMap.Entry` is an `AttributeModifier` plus its
  argument, so a biome may **override** a value or merely **modify** the
  one coming from the layer below. The attributes themselves are
  `EnvironmentAttribute`s from `EnvironmentAttributes` — *visual*
  (`EnvironmentAttributes.FOG_COLOR`, `EnvironmentAttributes.SKY_COLOR`,
  `EnvironmentAttributes.CLOUD_HEIGHT`, `EnvironmentAttributes.STAR_BRIGHTNESS`…),
  *audio* (`EnvironmentAttributes.AMBIENT_SOUNDS`,
  `EnvironmentAttributes.BACKGROUND_MUSIC`) and *gameplay*
  (`EnvironmentAttributes.PIGLINS_ZOMBIFY`,
  `EnvironmentAttributes.CREAKING_ACTIVE`,
  `EnvironmentAttributes.VILLAGER_ACTIVITY`…). The stack that combines
  them is `EnvironmentAttributeSystem`, whose layers are
  `EnvironmentAttributeLayer.Constant` (the `DimensionType`),
  `EnvironmentAttributeLayer.Positional` (the biome),
  `EnvironmentAttributeLayer.TimeBased` (the timelines) and the weather
  layers from `WeatherAttributes`. That system has no page of its own yet
  and is bigger than biomes; treat this as the biome's doorway into it.
- **`BiomeGenerationSettings`** — a `HolderSet` of
  `ConfiguredWorldCarver`s and one `HolderSet` of `PlacedFeature`s **per
  `GenerationStep.Decoration` ordinal**. Read by
  [features and placement](features-and-placement.md);
  `BiomeGenerationSettings.getBoneMealFeatures` is the one runtime use.
- **`MobSpawnSettings`** — `MobSpawnSettings.creatureGenerationProbability`,
  a weighted list of `MobSpawnSettings.SpawnerData` per `MobCategory`, and
  `MobSpawnSettings.MobSpawnCost` per entity type. Read by `NaturalSpawner`
  ([entity lifecycle](../entities/entity-lifecycle.md)).
- **`BiomeSource`** — the abstract chooser, and a `BiomeResolver`. Four
  implementations, their codecs registered by `BiomeSources.bootstrap`:
  `FixedBiomeSource`, `CheckerboardColumnBiomeSource`,
  `MultiNoiseBiomeSource`, `TheEndBiomeSource`.
  `BiomeSource.possibleBiomes` is memoised and used as a pre-filter
  everywhere.
- **`Climate`** — the search space. `Climate.Sampler` is a record of six
  `DensityFunction`s plus a spawn target; `Climate.TargetPoint` is six
  quantised longs; `Climate.Parameter` is an interval;
  `Climate.ParameterPoint` is six intervals **plus a scalar offset**;
  `Climate.ParameterList` holds the pairs and builds a `Climate.RTree`.
  `Climate.quantizeCoord` multiplies by 10,000 and truncates, so the whole
  search is integer arithmetic.
- **`OverworldBiomeBuilder`** — the overworld's parameter table, in Java:
  temperature, humidity, erosion and continentalness bands and six 5×5
  tables of biome keys, assembled by `OverworldBiomeBuilder.addBiomes`.
  `MultiNoiseBiomeSourceParameterList` is a data-pack registry element, but
  all it stores is a `MultiNoiseBiomeSourceParameterList.Preset` id and
  there are only two.
- **Where the label lives** — a second `PalettedContainer` in every
  `LevelChunkSection`, keyed by `Holder<Biome>`, built with
  `Strategy.createForBiomes`: **two bits per axis**, so 4×4×4 = 64 biome
  cells per section ([chunk anatomy](../world/chunk-anatomy.md)).
  `PalettedContainerFactory.defaultBiome` is plains.
- **`BiomeManager`** — the fuzz layer between "which quart cell" and "which
  biome does this *block* have". `BiomeManager.obfuscateSeed` derives its
  seed; `BiomeManager.getFiddledDistance` jitters the eight surrounding
  quart corners.

## When it runs

- **Once per chunk, on a worldgen worker.** `ChunkStatus.BIOMES` sits after
  structure references and **before `ChunkStatus.NOISE`** — the biome is
  decided before the terrain shape exists, not derived from it.
  `NoiseBasedChunkGenerator.createBiomes` forks to
  `Util.backgroundExecutor` under the name *init_biomes*.
- **Constantly, on the server thread**, for gameplay: precipitation and
  freezing in `ServerLevel.tickPrecipitation`, spawning in
  `NaturalSpawner`, commands.
- **Every client tick, on the main thread**, for looks:
  `EnvironmentAttributeProbe.tick` on the `Camera` re-samples the
  neighbourhood; `EnvironmentAttributeProbe.getValue` interpolates it per
  frame. Block tint is resolved on the render path through `BiomeColors`.

## The trace: a point gets a biome

```mermaid
sequenceDiagram
    participant CST as ChunkStatusTasks
    participant CG as NoiseBasedChunkGenerator
    participant CA as ChunkAccess
    participant LCS as LevelChunkSection
    participant MN as MultiNoiseBiomeSource
    participant CS as Climate.Sampler
    participant RT as Climate.RTree
    participant BM as BiomeManager
    participant EAS as EnvironmentAttributeSystem

    CST->>CG: createBiomes — ChunkStatus.BIOMES, before NOISE
    CG->>CG: fork to init_biomes · wrap resolver in Blender and BelowZeroRetrogen
    CG->>CA: fillBiomesFromNoise(BiomeResolver, cachedClimateSampler)
    CA->>LCS: fillBiomesFromNoise — 4×4×4 cells per section
    LCS->>MN: getNoiseBiome(quartX, quartY, quartZ, sampler)
    MN->>CS: Climate.Sampler.sample — six density functions, ×10000 to longs
    CS-->>MN: Climate.TargetPoint
    MN->>RT: Climate.ParameterList.findValue → RTree.search, 7 dimensions
    RT-->>LCS: Holder<Biome> → into the palette
    Note over LCS: saved under "biomes", shipped inside the chunk payload
    BM->>CA: gameplay read: getBiome → fiddled corner → getNoiseBiome
    EAS->>BM: visual read: getNoiseBiomeAtPosition — unfuzzed
    EAS->>EAS: dimension → biome → timeline → weather layers
```

1. **Generation.** `ChunkGenerator.createBiomes` is the status task's entry.
   `NoiseBasedChunkGenerator` wraps its `BiomeSource` in the blending and
   below-zero-retrogen resolvers and uses
   `NoiseChunk.cachedClimateSampler` so the sample hits the chunk's caches
   ([density functions](density-functions.md)); the flat, debug and end
   generators use `RandomState.sampler` directly.
2. **Per quart cell.** `ChunkAccess.fillBiomesFromNoise` walks the sections;
   `LevelChunkSection.fillBiomesFromNoise` rebuilds the container and
   writes 64 entries per section.
3. **The sample.** `Climate.Sampler.sample` converts quart to block
   coordinates, builds a single-point context, computes the six functions —
   temperature, humidity, continentalness, erosion, depth, weirdness — and
   quantises each into a `Climate.TargetPoint`.
4. **The search.** `MultiNoiseBiomeSource.getNoiseBiome` hands the target to
   `Climate.ParameterList.findValue`, which walks the `Climate.RTree`:
   six children per node, the metric a sum of squared distances from the
   target to each `Climate.Parameter` interval, over seven dimensions. The
   winning `Climate.RTree.Leaf` carries the `Holder<Biome>`. The end does
   not do this at all — `TheEndBiomeSource` thresholds one erosion sample
   outside a fixed central radius.
5. **Storage.** The holder goes into the section's palette, is written to
   NBT under *biomes* ([chunk storage](../world/chunk-storage.md)) and is
   sent to the client inside the chunk payload
   ([what the client is told](../networking/what-the-client-is-told.md)).
6. **The gameplay read.** `LevelReader.getBiome` goes through
   `BiomeManager.getBiome`, which does not floor to the quart cell: it
   offsets by two, takes the eight surrounding corners, and picks the one
   minimising `BiomeManager.getFiddledDistance` — a seeded hash giving each
   corner up to ±0.45 of jitter per axis. That is the ragged border. The
   chosen corner then resolves through `ChunkAccess.getNoiseBiome` to the
   palette.
7. **The visual read.** `EnvironmentAttributeSystem` and the client's
   `EnvironmentAttributeProbe` call
   `BiomeManager.getNoiseBiomeAtPosition` — the **unfuzzed** value — and
   for attributes declared spatially interpolated, `GaussianSampler.sample`
   blends a 6×6×6 quart neighbourhood into a
   `SpatialAttributeInterpolator` before
   `EnvironmentAttributeMap.applyModifier` runs.

## Interfaces

- **Called by:** `ChunkGenerator.createBiomes` and
  `ChunkGenerator.getMobsAt`; `NaturalSpawner`;
  `ServerLevel.tickPrecipitation`; `SurfaceRules` and `SurfaceSystem`;
  `LocateCommand` and `FillBiomeCommand`; on the client, `BiomeColors`,
  `BiomeAmbientSoundsHandler` and `SkyRenderer` through the probe.
- **Calls into:** `Climate.Sampler` and, behind it, the density-function
  graph; nothing else. Choosing a biome reads no blocks.
- **Crosses the network as:** the registry itself, synced with
  `Biome.NETWORK_CODEC`; the palette, inside the chunk payload; and
  `ClientboundChunksBiomesPacket` after `/fillbiome`
  (`ChunkMap.resendBiomesForChunks`).
- **Data-driven by:** `Registries.BIOME` (a data-pack registry loaded with
  `Biome.DIRECT_CODEC`), `Registries.MULTI_NOISE_BIOME_SOURCE_PARAMETER_LIST`,
  and `BiomeTags`. `BuiltInRegistries.BIOME_SOURCE` and
  `BuiltInRegistries.ENVIRONMENT_ATTRIBUTE` are code registries — a pack
  adds biomes, not kinds of biome source.

## Invariants and surprises

- **The game keeps two biomes for the same block, deliberately.**
  Gameplay uses the fuzzed `BiomeManager.getBiome`; environment attributes
  and the client probe use the unfuzzed
  `BiomeManager.getNoiseBiomeAtQuart`. Fog and grass colour follow a
  slightly different boundary from the one that decides whether the water
  freezes.
- **`BiomeSpecialEffects` is only block tint now.** Anything else you
  remember on it is an `EnvironmentAttribute`, and the biome is one layer
  in a stack — it can multiply the dimension's value rather than replace
  it, which is how swamps thicken water fog without naming a distance.
- **The search is seven-dimensional and the seventh axis is a constant.**
  `Climate.ParameterPoint` carries a `Climate.ParameterPoint.offset` that pads the target's
  seventh slot with zero — a fixed fitness penalty, a "make this biome
  harder to win" dial, not a sampled value.
- **Biomes are decided before terrain.** `ChunkStatus.BIOMES` precedes
  `ChunkStatus.NOISE`, so the biome shapes the terrain and never the
  reverse ([the pipeline](../world/chunk-generation-pipeline.md)).
- **Biomes are stored, not computed** — at 1/64 the resolution of blocks,
  in a second palette per section. `/fillbiome` exists because the stored
  value can be made to disagree with what the generator would say, and
  `ClientboundChunksBiomesPacket` exists to tell the client about it.
- **`/locate biome` asks the generator, not the world.**
  `BiomeSource.findClosestBiome3d` spirals through `BiomeSource.getNoiseBiome` with the
  live sampler and never reads a palette — so it finds biomes in
  ungenerated chunks and will never find one placed by `/fillbiome`. It
  pre-filters against `BiomeSource.possibleBiomes`, so an impossible biome
  fails instantly rather than after 6,400 blocks.
- **The overworld's biome table is code.** `OverworldBiomeBuilder` is a
  hardcoded parameter table; a pack can supply its own parameter list for a
  multi-noise source, but it cannot edit the vanilla preset — the data-pack
  element serialises to nothing but a preset name.
- **The client's `Biome` is hollow.** `Biome.NETWORK_CODEC` sends climate,
  the *syncable* attributes and the effects, and substitutes
  `BiomeGenerationSettings.EMPTY` and `MobSpawnSettings.EMPTY`. Features,
  carvers and spawn lists never cross the wire. And when a client asks for
  a biome in a chunk it does not have, it gets plains.
- **Structures outrank biomes for spawning.** `ChunkGenerator.getMobsAt`
  consults `Structure.spawnOverrides` before `Biome.getMobSettings`
  ([structures](structures.md)). And `MobSpawnSettings.SpawnerData`'s
  constructor silently rewrites any `MobCategory.MISC` entity type to pig.
- **Temperature is noisy above sea level and cached per thread.**
  `Biome.getHeightAdjustedTemperature` samples noise per block high up —
  that is why snow lines are ragged rather than flat — and `Biome` keeps a
  fixed-size, per-thread cache in front of it that evicts rather than
  grows. The public API is only the questions: `Biome.warmEnoughToRain`,
  `Biome.coldEnoughToSnow`, `Biome.shouldFreeze`, `Biome.shouldSnow`.
- **Adding one biome can change the whole dimension's layer stack.**
  `EnvironmentAttributeSystem` builds one positional layer per attribute
  *any* biome in the registry mentions, at level construction.

## Where to look

`Biome` · `Biome.BiomeBuilder` · `BiomeSpecialEffects` ·
`Biome.getAttributes` · `EnvironmentAttributeMap` ·
`EnvironmentAttributeSystem` · `BiomeSource.getNoiseBiome` ·
`MultiNoiseBiomeSource` · `Climate.Sampler.sample` ·
`Climate.ParameterList.findValue` · `Climate.RTree.search` ·
`OverworldBiomeBuilder.addBiomes` · `BiomeManager.getBiome` ·
`BiomeManager.getFiddledDistance` · `LevelChunkSection.fillBiomesFromNoise` ·
`Strategy.createForBiomes` · `BiomeColors` · `EnvironmentAttributeProbe`

---

*Rules: names, never code · how the system works, not how the code reads ·
newest version only · every backticked name passes `tools/verify_names.py`.*
