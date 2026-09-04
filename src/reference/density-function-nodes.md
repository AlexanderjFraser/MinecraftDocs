# Density-function nodes

> Verified against **Minecraft 26.2** · Reference · the thirty-four node types a
> *worldgen/density_function* file may name, what each one takes, and what the
> per-chunk rewrite turns it into.

[Density functions](../systems/worldgen/density-functions.md) is the lecture:
three forms of one graph, two rewrites, and the six caches. This is the
catalogue behind it — the table you would pause the video to read.

`DensityFunctions.bootstrap` registers every entry below into
`BuiltInRegistries.DENSITY_FUNCTION_TYPE`, in this order, under the
*minecraft* namespace. That registry is **built-in and frozen at startup**,
which is why adding a new *kind* of node takes code while adding a new graph
takes a JSON file.

**34** — registered node types (`DensityFunctions.bootstrap`): four by name,
then six markers, nine more by name, seven mapped transforms, four
arithmetic, and four last.

## The table

*children* counts the density-function slots; each one accepts an id string,
an inline object or a bare number, because every child slot is typed
`DensityFunction.CODEC`.

| id | class | children | other fields | what it computes |
|---|---|---:|---|---|
| *blend_alpha* | `DensityFunctions.BlendAlpha` | 0 | — | constant 1.0 as data — a placeholder the chunk swaps out |
| *blend_offset* | `DensityFunctions.BlendOffset` | 0 | — | constant 0.0 as data — likewise a placeholder |
| *beardifier* | `DensityFunctions.BeardifierMarker` | 0 | — | constant 0.0 as data — the structure-terrain placeholder |
| *old_blended_noise* | `BlendedNoise` | 0 | *xz_scale*, *y_scale*, *xz_factor*, *y_factor*, *smear_scale_multiplier* | the pre-1.18 terrain noise, decoded unseeded |
| *interpolated* | `DensityFunctions.Marker` | 1 | — | delegates — requests cell-corner interpolation |
| *flat_cache* | `DensityFunctions.Marker` | 1 | — | delegates — requests a quart-resolution 2-D cache |
| *cache_2d* | `DensityFunctions.Marker` | 1 | — | delegates — requests a one-entry XZ memo |
| *cache_once* | `DensityFunctions.Marker` | 1 | — | delegates — requests reuse within one interpolation step |
| *cache_all_in_cell* | `DensityFunctions.Marker` | 1 | — | delegates — requests a whole-cell block cache |
| *blend_density* | `DensityFunctions.Marker` | 1 | — | delegates — requests old-terrain density blending |
| *noise* | `DensityFunctions.Noise` | 0 | *noise*, *xz_scale*, *y_scale* | samples a `NormalNoise` at the scaled position |
| *end_islands* | `DensityFunctions.EndIslandDensityFunction` | 0 | — | the End's simplex island field, as a density |
| *shifted_noise* | `DensityFunctions.ShiftedNoise` | 3 | *noise*, *xz_scale*, *y_scale* | samples noise at position × scale plus three offsets |
| *range_choice* | `DensityFunctions.RangeChoice` | 3 | *min_inclusive*, *max_exclusive* | one of two branches, by whether the input is in range |
| *interval_select* | `DensityFunctions.IntervalSelect` | 1 + a list | *thresholds* | the branch whose ascending threshold the input first falls below |
| *shift_a* | `DensityFunctions.ShiftA` | 0 | *argument* (a noise) | domain warp read at x, 0, z |
| *shift_b* | `DensityFunctions.ShiftB` | 0 | *argument* (a noise) | domain warp read at z, x, 0 |
| *shift* | `DensityFunctions.Shift` | 0 | *argument* (a noise) | domain warp read at x, y, z |
| *clamp* | `DensityFunctions.Clamp` | 1 | *min*, *max* | the child, clamped |
| *abs* | `DensityFunctions.Mapped` | 1 | — | absolute value |
| *square* | `DensityFunctions.Mapped` | 1 | — | the child squared |
| *cube* | `DensityFunctions.Mapped` | 1 | — | the child cubed |
| *half_negative* | `DensityFunctions.Mapped` | 1 | — | identity above zero, halved below |
| *quarter_negative* | `DensityFunctions.Mapped` | 1 | — | identity above zero, quartered below |
| *invert* | `DensityFunctions.Mapped` | 1 | — | the reciprocal |
| *squeeze* | `DensityFunctions.Mapped` | 1 | — | clamp to ±1, then a soft odd cubic |
| *add* | `DensityFunctions.Ap2` or `DensityFunctions.MulOrAdd` | 2 | — | the sum |
| *mul* | `DensityFunctions.Ap2` or `DensityFunctions.MulOrAdd` | 2 | — | the product, short-circuiting on an exact zero |
| *min* | `DensityFunctions.Ap2` | 2 | — | the minimum, skipping the second child when the first is already below its bound |
| *max* | `DensityFunctions.Ap2` | 2 | — | the maximum, with the symmetric skip |
| *spline* | `DensityFunctions.Spline` | inside the spline | *spline* | a `CubicSpline` whose coordinates are themselves density functions |
| *constant* | `DensityFunctions.Constant` | 0 | *argument* | a fixed value |
| *y_clamped_gradient* | `DensityFunctions.YClampedGradient` | 0 | *from_y*, *to_y*, *from_value*, *to_value* | block Y mapped onto a value range |
| *find_top_surface* | `DensityFunctions.FindTopSurface` | 2 | *lower_bound*, *cell_height* | steps down in strides until the density goes positive, and returns that **Y** |

**Where one class serves several ids.** The six markers are all
`DensityFunctions.Marker`, a record of a `DensityFunctions.Marker.Type` and a
wrapped function; the seven transforms are all `DensityFunctions.Mapped`; the
four arithmetic ids share `DensityFunctions.TwoArgumentSimpleFunction`. In
each case the *enum constant* carries its own codec, and the node's `codec()`
returns its type's — which is how a re-serialised graph comes back with the
right id. `DensityFunctions.MulOrAdd` is the specialisation
`DensityFunctions.TwoArgumentSimpleFunction.create` picks when the id is
*add* or *mul* and one argument folded to a `DensityFunctions.Constant`, so
*add* in the JSON may come back as either class.

## What the caches become

`NoiseChunk.wrapNew` is the per-chunk rewrite. A marker is a *request*; this
is what is installed instead. All six replacements implement
`DensityFunctions.MarkerOrMarked`, so they still report their marker type and
would re-serialise unchanged.

| marker type | installed | keyed on |
|---|---|---|
| `DensityFunctions.Marker.Type.Interpolated` | `NoiseChunk.NoiseInterpolator` | nothing — two slices of cell-corner values, and eight corners loaded per cell. Requires the context to *be* the `NoiseChunk`, and throws if sampled outside the loop |
| `DensityFunctions.Marker.Type.FlatCache` | `NoiseChunk.FlatCache` | **position**, at quart resolution: one array entry per 4×4 block column group, filled at construction |
| `DensityFunctions.Marker.Type.Cache2D` | `NoiseChunk.Cache2D` | **position**, one entry — the packed XZ of the last sample |
| `DensityFunctions.Marker.Type.CacheOnce` | `NoiseChunk.CacheOnce` | **a counter** — `NoiseChunk.interpolationCounter` for the scalar, a second counter for the array form |
| `DensityFunctions.Marker.Type.CacheAllInCell` | `NoiseChunk.CacheAllInCell` | **the cell** — one array entry per block in the cell, Y stored inverted |
| `DensityFunctions.Marker.Type.BlendDensity` | `NoiseChunk.BlendDensity`, **or nothing at all** if the level's `Blender` is empty, in which case the marker is replaced by its own child | not cached |

The same rewrite resolves three singletons by object identity:
`DensityFunctions.BlendAlpha` and `DensityFunctions.BlendOffset` become flat
caches the `NoiseChunk` constructor has *already filled* (or survive as the
constants 1.0 and 0.0 when there is no blending to do), and
`DensityFunctions.BeardifierMarker` becomes this chunk's `Beardifier`. And
`DensityFunctions.HolderHolder` — the in-memory stand-in for an id reference,
which is not registered and has no codec — is resolved to its value once
instead of on every sample.

## Bounds

Every node answers `DensityFunction.minValue` and `DensityFunction.maxValue`
without a position. The arithmetic family — the two-argument nodes, the
mapped ones and *clamp* — stores its bounds as record components filled once
at construction; every other node answers by delegating to its input or by
walking its list again on each call. The rules worth knowing:

The arithmetic bounds are **sign-aware** and eager: *mul* takes the four
cross products and picks by the signs of the operands' ends, and *min* and
*max* take the element-wise minimum and maximum of the ends. Building a *min*
or a *max* over two ranges that cannot overlap logs a warning and proceeds.
`DensityFunctions.Mapped.create` transforms the child's two endpoints, with
*abs* and *square* clamping the minimum up to zero and *invert* reporting
**±infinity** whenever the child's range straddles zero. *clamp* is the one
node whose bounds are not derived from its child at all: its record
components are literally named *minValue* and *maxValue*, so the codec's
*min* and *max* fields *are* the interface's bound methods.

Three nodes report bounds that are not densities or not final.
`DensityFunctions.Marker` passes its child's bounds through except when its
type is `DensityFunctions.Marker.Type.BlendDensity`, where it reports ±infinity — the one place a marker
is not transparent. `DensityFunctions.HolderHolder` reports ±infinity while
its holder is unbound, which is what lets forward references parse. And
`DensityFunctions.FindTopSurface` reports its *lower bound* and its upper
bound's maximum, which are **Y coordinates** — this node's range is on a
different scale from every other node in the table.

One more, on the unseeded graph: `DensityFunction.NoiseHolder` answers a
maximum of 2.0 while its `NormalNoise` is still null, so a freshly parsed
router reports wider noise bounds than the seeded one it becomes.

## What vanilla actually uses

Thirty-five JSON files ship under *worldgen/density_function* — four at the
top level plus the per-dimension directories — and between them they use
twenty-five of the thirty-four ids. Four more appear only inline, in the
seven `Registries.NOISE_SETTINGS` files: *blend_density* and *squeeze* in all
seven, and *square*, *invert* and *find_top_surface* in the three overworld
variants.

That leaves four ids vanilla data never writes. *constant* is never written
as a typed object, because a bare number is one. *cache_all_in_cell* and
*beardifier* are added **in code**, by `NoiseChunk`'s constructor, around the
router's final density. And *shift* — the three-dimensional domain warp — is
used by nothing: `DensityFunctions.shift` has no callers anywhere in the
decompile, and no shipped file names the id. `DensityFunctions.ShiftA` and
`DensityFunctions.ShiftB` cover the two two-dimensional warps vanilla wants.

---

*Rules: names, never code · how the system works, not how the code reads ·
newest version only · every backticked name passes `tools/verify_names.py`.*
