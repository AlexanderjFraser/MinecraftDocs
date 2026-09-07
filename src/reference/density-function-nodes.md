# Density-function nodes

> Verified against **Minecraft 26.2** · Reference · the thirty-four node types a
> *worldgen/density_function* file may name: what each one takes, what the
> per-chunk rewrite turns it into, what range it reports, and which ids the
> shipped data actually writes.

[Density functions](../systems/worldgen/density-functions.md) is the lecture:
three forms of one graph, two rewrites, and the six caches. This is the
catalogue behind it — the four tables you would pause the video to read.

`DensityFunctions.bootstrap` registers every entry below into
`BuiltInRegistries.DENSITY_FUNCTION_TYPE`, in this order, under the
*minecraft* namespace. That registry is built-in and
[frozen at start-up](../systems/foundations/identifiers-and-registries.md#the-freeze-rule-stated),
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
each case the *enum constant* carries its own codec, and the node's *codec()*
returns its type's — which is how a re-serialised graph comes back with the
right id. The two classes in the *add* and *mul* rows are the same story: the
constructor folds a constant argument away
([the parse step](../systems/worldgen/density-functions.md#parse-one-file-one-graph)),
so *add* in the JSON may come back as either.

Two members of `DensityFunctions` are **not** in this table because they are
not registered: `DensityFunctions.HolderHolder`, the in-memory stand-in for an
id reference, which has no codec at all; and
`DensityFunctions.TransformerWithContext`, a shape with no implementation.

## What the caches become

`NoiseChunk.wrapNew` is the
[per-chunk rewrite](../systems/worldgen/density-functions.md#wrap-once-per-chunk).
A marker is a *request*; this is what is installed instead. All six installed
classes implement `DensityFunctions.MarkerOrMarked`, so the marker type
survives the swap and the graph would re-serialise unchanged.

| marker type | installed | keyed on |
|---|---|---|
| `DensityFunctions.Marker.Type.Interpolated` | `NoiseChunk.NoiseInterpolator` | nothing — two slices of cell-corner values, and eight corners loaded per cell |
| `DensityFunctions.Marker.Type.FlatCache` | `NoiseChunk.FlatCache` | **position**, at quart resolution: one array entry per 4×4 block column group, filled at construction |
| `DensityFunctions.Marker.Type.Cache2D` | `NoiseChunk.Cache2D` | **position**, one entry — the packed XZ of the last sample |
| `DensityFunctions.Marker.Type.CacheOnce` | `NoiseChunk.CacheOnce` | **a counter** — `NoiseChunk.interpolationCounter` for the scalar, a second counter for the array form |
| `DensityFunctions.Marker.Type.CacheAllInCell` | `NoiseChunk.CacheAllInCell` | **the cell** — one array entry per block in the cell, Y stored inverted |
| `DensityFunctions.Marker.Type.BlendDensity` | `NoiseChunk.BlendDensity`, **or nothing at all** if the level's [`Blender`](../systems/worldgen/blending.md#what-the-blender-actually-answers) is empty, in which case the marker is replaced by its own child | not cached |

The same rewrite resolves three unregistered singletons by object identity,
and every `DensityFunctions.HolderHolder` to its value:

| singleton | installed | with no blending to do |
|---|---|---|
| `DensityFunctions.BlendAlpha` | a `NoiseChunk.FlatCache` the constructor has already filled | survives as the constant 1.0 |
| `DensityFunctions.BlendOffset` | a `NoiseChunk.FlatCache`, likewise | survives as the constant 0.0 |
| `DensityFunctions.BeardifierMarker` | this chunk's [`Beardifier`](../systems/worldgen/structure-placement.md#the-ground-bends-and-then-the-blocks-arrive) | — the swap is unconditional |

## Bounds

Every node answers `DensityFunction.minValue` and `DensityFunction.maxValue`
without a position. Most take theirs from a child; the arithmetic family — the
two-argument nodes, the mapped ones and *clamp* — stores them as record
components filled once at construction, and so does `BlendedNoise`. The bounds
of a *parsed* graph are not the bounds of the running one, which is
[the lecture's argument](../systems/worldgen/density-functions.md#questions-players-ask);
this table is which node departs from its child, and how.

| id | its range | |
|---|---|---|
| *add*, *mul*, *min*, *max* | sign-aware and eager | *mul* takes the four cross products and picks by the signs of the operands' ends; *min* and *max* take the element-wise minimum and maximum. Two ranges that cannot overlap log a warning and proceed |
| *abs*, *square* | the child's endpoints, minimum clamped up to zero | `DensityFunctions.Mapped.create` transforms both ends |
| *invert* | **±infinity** whenever the child's range straddles zero | the reciprocal has no finite bound across zero |
| *clamp* | its own record components | they are literally named *minValue* and *maxValue*, so the codec's *min* and *max* fields **are** the interface's bound methods |
| *shifted_noise* | the noise's | all three children are ignored |
| *blend_density* | **±infinity**, whatever its child says | the one marker type that is not transparent |
| *find_top_surface* | its *lower_bound* and its upper bound's maximum | **Y coordinates** — this node's range is on a different scale from every other row |
| *noise* | from the `DensityFunction.NoiseHolder`; 2.0 until the graph is seeded | the sixty-three shipped noise definitions come out between 2.57 and 7.32 once seeded |

`DensityFunctions.HolderHolder`, off the table, reports ±infinity while its
holder is unbound, which is what lets forward references parse at all.

## What vanilla actually uses

Thirty-five JSON files ship under *worldgen/density_function* — four at the
top level plus the per-dimension directories — and between them they use
twenty-five of the thirty-four ids. Five more appear only inline, in the
seven `Registries.NOISE_SETTINGS` files, the per-dimension recipes
[terrain](../systems/worldgen/terrain.md#the-cast) reads: *blend_density* and
*squeeze* in all seven, and *square*, *invert* and *find_top_surface* in the
three overworld variants.

That leaves four ids vanilla data never writes. *constant* is never written
as a typed object, because a bare number is one. *cache_all_in_cell* and
*beardifier* are added **in code**, by `NoiseChunk`'s constructor, around the
router's final density. And *shift* — the three-dimensional domain warp — is
[used by nothing](../systems/worldgen/density-functions.md#questions-players-ask):
`DensityFunctions.ShiftA` and
`DensityFunctions.ShiftB` cover the two two-dimensional warps vanilla wants.

---

*Rules: names, never code · how the system works, not how the code reads ·
newest version only · every backticked name passes `tools/verify_names.py`.*
