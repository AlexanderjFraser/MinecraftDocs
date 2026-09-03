# Lightmap, fog and sky

> Verified against **Minecraft 26.2** · Part XI · the sun goes down: every colour on screen, traced back to one keyframe curve.

Stand on a hill and watch the light go. The sky over the taiga slides from
blue towards black, the murk closes in until the far trees dissolve, stars
come up, the moon takes whatever shape it is owed tonight, and if a storm
arrives the scene goes grey and streaked. Five renderers make those colours —
`Lightmap` decides how bright, `FogRenderer` how far, `SkyRenderer` and
`CloudRenderer` what is up there, `WeatherEffectRenderer` what is coming down
— and between them they ask one question and nothing else: *what is this
attribute worth, here, now?* The surprise is who they ask. **Most of them no
longer know what time it is.** They ask a probe for a named value at a
position and a partial tick, and the day/night curve behind it is keyframes in
a data pack. Only two still read the raw world clock: the clouds, because they
drift, and the weather, whose streaks are seeded from it.

## The cast

| class | what it decides | thread |
|---|---|---|
| `EnvironmentAttributeProbe` | what any attribute is worth at the camera, this frame | Render thread |
| `LightmapRenderStateExtractor` | the lightmap's ten uniforms, and whether to redraw at all | Render thread |
| `Lightmap` | how bright, as the 16×16 texture every terrain vertex samples | Render thread |
| `FogRenderer` | how far you can see, in what colour, and in which medium | Render thread |
| `SkyRenderer` | what hangs above the horizon — and which of two skies it is | Render thread |
| `CloudRenderer` | the cloud cells, and the face list built from them | `CloudRenderer.prepare` bakes on a worker, the rest on Render |
| `WeatherEffectRenderer` | which columns get rain, which get snow, and how hard | Render thread |
| `LevelRenderer` | which of those become frame-graph passes at all | Render thread |

## What a renderer has to know about an attribute, and no more

An **environment attribute** is a named, typed quantity — a colour, a
distance, an angle, a moon phase — that the world answers for a position and
an instant. `EnvironmentAttributeSystem` assembles that answer by running a
short stack of layers over the attribute's own default: the dimension, the
biome, one layer per timeline the dimension runs, and weather where a
dimension can have it. That machinery belongs to [environment attributes and
timelines](../world/environment-attributes-and-timelines.md); this page
assumes it and names only what it consumes. Three consequences shape
everything below.

**The client resolves the same stack from the same data** — it is never sent
a resolved colour — and what it adds is `EnvironmentAttributeProbe`, on the
camera. `EnvironmentAttributeProbe.tick` re-samples the biome neighbourhood
once per client tick and rolls each probed value's new answer down into last
tick's; `EnvironmentAttributeProbe.getValue` fetches the fresh one lazily,
during the frame, and interpolates between the two by partial tick; and any
attribute nobody asked for during a tick is evicted. Every renderer here goes
through the probe, never through the system.

**Whether a value smooths or steps is declared on the attribute**, not chosen
by the renderer — which is why the sky colour slides and
`EnvironmentAttributes.MOON_PHASE` snaps, and why a renderer that wants a
different curve must ask for a different attribute.

**`ClientLevel` adds two layers of its own** on top of the four, and both are
the **lightning** flash: one whitens `EnvironmentAttributes.SKY_COLOR`, the
other pins `EnvironmentAttributes.SKY_LIGHT_FACTOR` to one while the flash
lasts. Neither has anything to do with the End's sky flash, which never
enters the stack at all.

### What the dimension type and the biome still carry

Two record fields survived the migration. `DimensionType.skybox` is a
three-valued `DimensionType.Skybox` — `DimensionType.Skybox.NONE`,
`DimensionType.Skybox.OVERWORLD`, `DimensionType.Skybox.END` — and it is a
*branch*, not a colour. `BiomeSpecialEffects` still exists, hollowed out to
`BiomeSpecialEffects.waterColor`, `BiomeSpecialEffects.grassColorOverride`,
`BiomeSpecialEffects.grassColorModifier` and the foliage colours: every fog
and sky colour left it for `Biome.getAttributes`. None of it crosses the
network as pixels — the inputs arrive as registry sync during configuration,
attribute maps filtered through `EnvironmentAttributeMap.NETWORK_CODEC`, then
world time and weather during play ([protocol
phases](../networking/protocol-phases.md)) — so a data pack retints a
dimension without touching the client.

## The five askers

| renderer | what it asks for | when it asks | what it produces |
|---|---|---|---|
| `Lightmap`, through `LightmapRenderStateExtractor` | how bright block light and sky light should read, and in what tint | once per tick, at a partial tick of exactly one | ten std140 uniforms and one 16×16 texture |
| `FogRenderer` | the colour of the murk and the six distances it lives between | once per frame, inside the camera extract | one `FogData`, uploaded as one UBO slice |
| `SkyRenderer` | where the sun, moon and stars are, and how bright | once per frame | a `SkyRenderState` for the sky pass |
| `CloudRenderer` | what colour the clouds are and how high they sit | once per frame, read for it by `LevelExtractor` | a compressed face list, rebaked only when it must be |
| `WeatherEffectRenderer` | nothing, until it is raining | once per frame, and only then | a list of `WeatherEffectRenderer.ColumnInstance` |

## The trace: the sun goes down

```mermaid
sequenceDiagram
    participant Time as Timelines
    participant EAS as EnvironmentAttributeSystem
    participant EAP as EnvironmentAttributeProbe
    participant LRSE as LightmapRenderStateExtractor
    participant FR as FogRenderer
    participant SR as SkyRenderer
    participant LR as LevelRenderer
    participant LM as Lightmap

    Note over Time,EAS: per client tick
    Time->>EAS: the keyframe tracks for this world time — SUN_ANGLE, SKY_COLOR, SKY_LIGHT_FACTOR
    EAS->>EAS: invalidateTickCache — every non-positional value recomputes once
    EAS->>EAP: tick — Gaussian biome blend, last becomes new, unread attributes evicted
    LRSE->>LRSE: tick — flicker walk, then needsUpdate is raised

    Note over EAP,SR: per frame, extract
    LRSE->>EAP: getValue(SKY_LIGHT_FACTOR, BLOCK_LIGHT_TINT, AMBIENT_LIGHT_COLOR)
    LRSE-->>LM: LightmapRenderState — ten std140 values, plus the flag
    FR->>EAP: getValue(FOG_COLOR, SUNRISE_SUNSET_COLOR, SKY_FOG_END_DISTANCE)
    FR-->>LR: FogData — one colour and six distances, in one UBO
    SR->>EAP: getValue(SUN_ANGLE, MOON_ANGLE, STAR_BRIGHTNESS, MOON_PHASE)
    SR-->>LR: SkyRenderState

    Note over LM,LR: per frame, render
    LM->>LM: render — one three-vertex draw into a 16×16 texture
    LR->>LR: addSkyPass — disc, sunrise fan, sun, moon, stars, dark disc
    LR->>LR: addMainPass — terrain samples the lightmap
    LR->>LR: addCloudsPass, then addWeatherPass
```

The middle band's order is a dependency order. `GameRenderer.extract` runs
`LightmapRenderStateExtractor.extract`, then `GameRenderer.extractCamera` —
where `FogRenderer.setupFog` stashes its `FogData` on
`CameraRenderState.fogData` — then `LevelExtractor.extract`, which drives
`WeatherEffectRenderer.extractRenderState` and
`SkyRenderer.extractRenderState`. Then `GameRenderer.renderLevel` uploads the
fog with `FogRenderer.updateBuffer`, takes one slice with
`FogRenderer.getBuffer`, and `LevelRenderer.render` declares the passes.

`SkyRenderer.renderSunriseAndSunset` is the clearest instance of the pattern.
The sunrise fan's colour *is* `EnvironmentAttributes.SUNRISE_SUNSET_COLOR`, an
ARGB keyframe track, and its visibility is that colour's own alpha channel —
which the renderer also scales the fan's depth by. The fade is a property of
the data, not of the geometry, so a data pack restyles the sunset without a
line of client code changing.

## How bright: one draw per tick, and no partial ticks at all

`Lightmap` is a 16×16 `GpuTexture` plus a `MappableRingBuffer` of uniforms.
`Lightmap.render` writes those uniforms and issues **one three-vertex draw**
with `RenderPipelines.LIGHTMAP`: the brightness curve lives in the shader and
the whole texture is a by-product of it. In 1.21 this was a `NativeImage`
filled pixel by pixel in Java and re-uploaded every frame.

What it draws from is `LightmapRenderState`: ten values in std140 order — six
floats from `LightmapRenderState.skyFactor` and
`LightmapRenderState.blockFactor` to `LightmapRenderState.brightness`, then
four colours, `LightmapRenderState.blockLightTint` and
`LightmapRenderState.skyLightColor` from
`EnvironmentAttributes.BLOCK_LIGHT_TINT` and
`EnvironmentAttributes.SKY_LIGHT_COLOR`, the other two from
`EnvironmentAttributes.AMBIENT_LIGHT_COLOR` and
`EnvironmentAttributes.NIGHT_VISION_COLOR` — and an eleventh field,
`LightmapRenderState.needsUpdate`, which is not a uniform at all but the flag
that decides whether the draw happens. `LightmapRenderStateExtractor.tick`
runs the torch-flicker random walk in
`LightmapRenderStateExtractor.blockLightFlicker` and raises its own copy of
the flag; `LightmapRenderStateExtractor.extract` copies it across, clears it,
and reads the probe alongside `Options.gamma`, `Options.darknessEffectScale`,
the conduit-power water vision and
`LightmapRenderStateExtractor.calculateDarknessScale`. **So the lightmap is
recomputed once per tick and not once per frame** — and, deliberately,
`GameRenderer.extract` hands the extractor a partial tick of exactly one
while `FogRenderer.setupFog` and `SkyRenderer.extractRenderState` get the
real one. Sky and fog interpolate mid-tick. World lighting steps.

Three leftovers. `Lightmap.getBrightness` survives but no longer feeds the
lightmap: it is a CPU-side duplicate of the shader's curve, kept for `Hud`,
`EntityRenderer`'s shadow sampling and `ScreenEffectRenderer` alone. The
packing statics moved out of the texture into `LightCoordsUtil`, from where a
packed value reaches a vertex through `VertexConsumer.setLight`. And
`UiLightmap` is the 1×1 white `DynamicTexture` handed out while
`GameRenderer.useUiLightmap` is set.

### Two curves that look like one

`EnvironmentAttributes.SKY_LIGHT_FACTOR` is a *visual* attribute, spatially
interpolated, and the lightmap reads it;
`EnvironmentAttributes.SKY_LIGHT_LEVEL` is a *gameplay* attribute, not
positional, and `Level.updateSkyBrightness` turns it into `Level.skyDarken`
for mob spawning. `Timelines.OVERWORLD_DAY` keyframes both, at slightly
different times and to different night values — so they look like one number,
and a data pack can pull them apart.

## How far: one block for the whole frame, filled by a priority walk

`FogRenderer`'s output is a mutable `FogData`: `FogData.color` plus six
distances — a start and an end each for the medium and the horizon, then
`FogData.skyEnd` and `FogData.cloudEnd`. In open air those are
`EnvironmentAttributes.FOG_COLOR`, `EnvironmentAttributes.FOG_START_DISTANCE`,
`EnvironmentAttributes.FOG_END_DISTANCE`,
`EnvironmentAttributes.SKY_FOG_END_DISTANCE` and
`EnvironmentAttributes.CLOUD_FOG_END_DISTANCE`, and underwater they are
`EnvironmentAttributes.WATER_FOG_COLOR`,
`EnvironmentAttributes.WATER_FOG_START_DISTANCE` and
`EnvironmentAttributes.WATER_FOG_END_DISTANCE` instead. It owns one ring
buffer, `FogRenderer.regularBuffer`, and a static `FogRenderer.emptyBuffer`
filled with *infinitely far* for when fog is off.

**There is one fog UBO for the whole frame, not one per pass.**
`LevelRenderer.render` takes a single slice and hands the same one to the
sky, main, weather and always-on-top passes — and hands the clouds pass no
fog at all. The sky and cloud fog ends are separate fields *inside that one
block*, which the shaders choose between, so what a player sees as
per-element fog is a shader decision and not a binding.

### The list that decides the colour

The colour and the darkening come from different places.
`FogRenderer.FOG_ENVIRONMENTS` is an ordered list and the order *is* the
priority: `LavaFogEnvironment`, `PowderedSnowFogEnvironment`,
`BlindnessFogEnvironment`, `DarknessFogEnvironment`, `WaterFogEnvironment`,
and `AtmosphericFogEnvironment` **last**, which is what makes it the
guaranteed fallback. `FogRenderer.computeFogColor` walks that list twice —
once for the first environment whose `FogEnvironment.providesColor` is true,
separately for the first whose `FogEnvironment.modifiesDarkness` is — whereas
`FogEnvironment.setupFog` stops at the first applicable one, and it and
`FogEnvironment.isApplicable` are the class's only abstract methods.
`MobEffectFogEnvironment` declares `FogEnvironment.providesColor` false on
purpose: blindness and darkness may darken somebody else's colour, never
supply one, and the atmospheric environment sits last precisely so somebody
always does. Which medium the camera is in is a `FogType` (`FogType.WATER`,
`FogType.LAVA`, `FogType.POWDER_SNOW`, `FogType.ATMOSPHERIC`,
`FogType.NONE`), and *NONE* maps to the atmospheric environment. Rain fog is
the only stateful one: `AtmosphericFogEnvironment.rainFogMultiplier` is an
exponential follower, so the murk lags a storm starting rather than
snapping to it, and `AtmosphericFogEnvironment.updateRainFogState` thickens it
even in a biome with no precipitation, at half strength.

## What is up there: two skies, and a texture that is never bound

`SkyRenderer` builds every buffer it will ever need in its constructor, from
`SkyRenderer.buildStars` to `SkyRenderer.buildMoonPhases` against the
`AtlasIds.CELESTIALS` atlas, and per frame fills a `SkyRenderState` running
from `SkyRenderState.skybox` through `EnvironmentAttributes.SUN_ANGLE`,
`EnvironmentAttributes.MOON_ANGLE`, `EnvironmentAttributes.STAR_ANGLE` and
`EnvironmentAttributes.STAR_BRIGHTNESS` to `SkyRenderState.endFlashIntensity`.

**The stars are the same in every world.** `SkyRenderer.buildStars` seeds a
fixed constant and rejects samples outside a shell, so `SkyRenderer.STAR_COUNT`
is an attempt count rather than a star count, and they are rebuilt only when a
resource reload takes the whole renderer down:
`LevelExtractor.onResourceManagerReload` sets
`LevelExtractor.shouldResetSkyRenderer` and `LevelRenderer.addSkyPass` closes
and reconstructs the entire `SkyRenderer`, stars, moon phases and all. The moon
phase, likewise, is no longer arithmetic on the day count — it is
`EnvironmentAttributes.MOON_PHASE` driven by `Timelines.MOON`, whose period is
`MoonPhase.COUNT` days, and the renderer picks a sub-quad of an eight-quad
buffer by `MoonPhase.index`.

**The End takes a different branch entirely.** With
`DimensionType.Skybox.END`, `SkyRenderer.extractRenderState` fills only the
End-flash fields: the sun angle, the moon phase, the sky colour and the dark
disc are never sampled. And `EndFlashState` is not the dragon fight — it is a
free-running flash on a six-hundred-tick cycle, seeded per interval for its
offset, duration and angles, advanced by `EndFlashState.tick` in any dimension
whose skybox is the End's. The sky is also skipped five ways:
`LevelRenderer.addSkyPass` bails in lava, in powder snow, under blindness,
under darkness, and when `DimensionType.Skybox` is *NONE* — the Nether — and
`GameRenderer.renderLevel` suppresses it when a boss bar wants world fog,
with `AtmosphericFogEnvironment.setupFog` clamping the fog hard in that case.

### The clouds, which get no fog and no texture

The clouds are the first of the two exceptions: their colour and height are
`EnvironmentAttributes.CLOUD_COLOR` and `EnvironmentAttributes.CLOUD_HEIGHT`,
but their *drift* is raw world time. **And the cloud texture is never bound as
a texture.** `CloudRenderer.prepare` reads the image on a worker and
`CloudRenderer.apply` bakes it into `CloudRenderer.TextureData` through
`CloudRenderer.packCellData`, one 64-bit word per pixel with the colour in the
high bits and four neighbour-emptiness flags in the low four.
`CloudRenderer.buildMesh` walks cells of `CloudRenderer.CELL_SIZE_IN_BLOCKS`,
writing three bytes per face through `CloudRenderer.encodeFace` — a compressed
*face list*, expanded to quads in the shader, with
`CloudRenderer.RelativeCameraPos` and `CloudStatus` deciding which faces
exist. It is rebuilt on a reload, when the camera crosses a cell boundary or
changes side, or when the `CloudStatus` changes — and a data pack setting the
cloud colour to zero alpha removes the pass entirely.

## What is coming down: rebuilt every frame, and seeded from the clock

`WeatherEffectRenderer` is the second exception: its columns are placed by
world position, but the streaks are seeded from raw world time. It holds one
`WeatherEffectRenderer.vertexBuffer` and the precomputed tangent tables
`WeatherEffectRenderer.columnSizeX` and `WeatherEffectRenderer.columnSizeZ`,
and its per-frame product is a list of `WeatherEffectRenderer.ColumnInstance`
records inside a `WeatherRenderState`.
`WeatherEffectRenderer.extractRenderState` returns immediately when the rain
level is zero, so a clear sky costs nothing. Otherwise it loops every column
in a square of radius `Options.weatherRadius`, querying the heightmap and the
precipitation at each — every frame, on the CPU. The vertex buffer is rebuilt in
`WeatherEffectRenderer.render` rather than in extract, rain and snow are two
indexed draws sharing it, and the world border rides in the same pass. Particles and sound are somebody else's job:
`ClientLevel.tickWeatherEffects` spawns those per tick within the same radius,
next to `ClientLevel.animateTick`, which scatters
`EnvironmentAttributes.AMBIENT_PARTICLES`.

## What is not an attribute

The migration was not total, which is why *everything is an attribute now*
needs a qualifier. `DimensionType.ambientLight` — the floor under the
lightmap's curve — and `DimensionType.cardinalLightType` are plain record
fields, read directly. Block tint never moved at all: grass, foliage and water
are still `BiomeColors` reading `BiomeSpecialEffects` through the four
`ColorResolver`s, with no probe and no layer stack in it. And the clouds and
the weather still read the world clock, because a value sampled at the camera
and lerped by partial tick is the wrong shape for a drift or a seed.

> **For a 1.21-era reader.** Nearly every per-dimension, per-biome,
> per-time-of-day visual constant is an environment attribute now, so the
> names to stop hunting for are: *LightTexture* (now `Lightmap` plus
> `LightCoordsUtil`), *DimensionSpecialEffects* and all three subclasses (now
> `DimensionType.skybox` plus attributes), *FogParameters* (now `FogData`),
> *RenderSystem.setShaderFogColor* and its siblings (now one
> `RenderSystem.setShaderFog` taking a uniform slice),
> *LevelRenderer.renderSky* / *renderClouds* / *renderSnowAndRain* (now the
> `LevelRenderer.addSkyPass` family of frame-graph passes, declared as
> [visibility and the frame graph](visibility-and-the-frame-graph.md)
> describes), and *Level.getSkyColor*, *ClientLevel.getStarBrightness* and
> *ClientLevel.effects*, all attributes now. The draws went the way of
> everything in [blaze3d](blaze3d.md), from `RenderPipelines.LIGHTMAP` and
> `RenderPipelines.SKY` to `RenderPipelines.WEATHER_DEPTH_WRITE`.

## Where to look

`LightmapRenderStateExtractor.extract` first, then `Lightmap.render` for what
it feeds. `EnvironmentAttributeProbe.getValue` for the question every renderer
here asks, and [environment attributes and
timelines](../world/environment-attributes-and-timelines.md) for how it is
answered. `FogRenderer.computeFogColor` for the priority walk.
`SkyRenderer.extractRenderState` and `LevelRenderer.addSkyPass` for the sky
and its two branches, `CloudRenderer.buildMesh` and
`WeatherEffectRenderer.extractRenderState` for the meshes rebuilt inside the
frame, and `BiomeColors` for the colour system that did not move.

---

*Rules: names, never code · how the system works, not how the code reads ·
newest version only · every backticked name passes `tools/verify_names.py`.*
