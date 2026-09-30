# Density-function nodes

> Verified against **Minecraft 26.3** · Reference · the forty-four node types a
> *worldgen/density_function* file may name: what each one takes, what the
> compiler turns it into, what range it reports, and which ids the shipped
> data actually writes.

[Density functions](../systems/worldgen/density-functions.md) is the lecture:
one graph, rewritten twice and compiled once per dimension, and one kind of
cache. This is the catalogue behind it — the four tables you would pause the
video to read.

`DensityFunctions.bootstrap` registers every entry below into
`BuiltInRegistries.DENSITY_FUNCTION_TYPE`, in this order, under the
*minecraft* namespace. That registry is built-in and
[frozen at start-up](../systems/foundations/identifiers-and-registries.md#the-freeze-rule-stated),
which is why adding a new *kind* of node takes code while adding a new graph
takes a JSON file.

**Forty-four node types** are registered (`DensityFunctions.bootstrap`): one by name,
then three context values, seven more by name, eleven unary transforms, four
roundings, six arithmetic, and twelve last.

## The table

*children* counts the density-function slots; each one accepts an id string,
an inline object or a bare number, because every child slot is typed
`DensityFunction.CODEC`.

| id | class | children | other fields | what it computes |
|---|---|---:|---|---|
| *constant* | `ConstantFunction` | 0 | *value* | a fixed value |
| *blend_alpha* | `SimpleDensityFunction` | 0 | — | the chunk's blend alpha from the sampling context, else 1.0 |
| *blend_offset* | `SimpleDensityFunction` | 0 | — | the chunk's blend offset from the context, else 0.0 |
| *beardifier* | `SimpleDensityFunction` | 0 | — | the chunk's structure-terrain adjustment from the context, else 0.0 |
| *noise* | `NoiseFunction` | 3, optional | *noise*, *xz_scale*, *y_scale* | samples the noise a `NormalNoise` defines at position × scale, plus three offsets |
| *end_outer_islands* | `EndIslandFunction` | 0 | — | the End's simplex field of outer islands, as a density |
| *distance_to_point* | `DistanceToPointFunction` | 0 | *point*, *metric* | the distance from a fixed point, by one of four metrics |
| *gradient* | `GradientFunction` | 0 | *axis*, *tiling*, *from_coordinate*, *to_coordinate*, *from_value*, *to_value* | one coordinate mapped onto a value range, clamped, repeated or mirrored past the ends |
| *shift_a* | `ShiftNoiseFunction.ShiftA` | 0 | *noise* | domain warp read at x, 0, z |
| *shift_b* | `ShiftNoiseFunction.ShiftB` | 0 | *noise* | domain warp read at z, x, 0 |
| *shift* | `ShiftNoiseFunction.Shift` | 0 | *noise* | domain warp read at x, y, z |
| *abs* | `UnaryFunction` | 1 | — | absolute value |
| *square* | `UnaryFunction` | 1 | — | the child squared |
| *cube* | `UnaryFunction` | 1 | — | the child cubed |
| *sqrt* | `UnaryFunction` | 1 | — | the square root |
| *half_negative* | `UnaryFunction` | 1 | — | identity above zero, halved below |
| *quarter_negative* | `UnaryFunction` | 1 | — | identity above zero, quartered below |
| *reciprocal* | `UnaryFunction` | 1 | — | the reciprocal |
| *negate* | `UnaryFunction` | 1 | — | the child negated |
| *squeeze* | `UnaryFunction` | 1 | — | clamp to ±1, then a soft odd cubic |
| *log* | `UnaryFunction` | 1 | — | the natural logarithm |
| *sign* | `UnaryFunction` | 1 | — | the child's sign: −1, 0 or 1 |
| *floor* | `RoundFunction` | 2 | — | rounded down to a multiple of *multiple*, 1 unless given |
| *round* | `RoundFunction` | 2 | — | rounded to the nearest multiple |
| *ceil* | `RoundFunction` | 2 | — | rounded up to a multiple |
| *truncate* | `RoundFunction` | 2 | — | rounded toward zero to a multiple |
| *add* | `BinaryFunction` | 2 | — | the sum |
| *sub* | `BinaryFunction` | 2 | — | the difference |
| *mul* | `BinaryFunction` | 2 | — | the product — with neither child a constant, a single sample short-circuits when the first is exactly zero |
| *div* | `BinaryFunction` | 2 | — | the quotient, with the same short-circuit |
| *min* | `BinaryFunction` | 2 | — | the minimum — with neither child a constant, a single sample skips the second when the first is already at or below the second's lower bound |
| *max* | `BinaryFunction` | 2 | — | the maximum, with the symmetric skip |
| *pow* | `PowFunction` | 2 | — | *base* raised to *exponent* |
| *spline* | `SplineFunction` | inside the spline | *spline* | a `CubicSpline` whose coordinates are themselves density functions |
| *lerp* | `LerpFunction` | 3 | — | from *first* to *second*, by *alpha* |
| *clamp* | `ClampFunction` | 1 | *min*, *max* | the child, clamped |
| *range_choice* | `RangeChoiceFunction` | 3 | *min_inclusive*, *max_exclusive* | one of two branches, by whether the input is in range |
| *interval_select* | `IntervalSelectFunction` | 1 + a list | *thresholds* | the branch whose ascending threshold the input first falls below |
| *cache* | `CacheFunction` | 1 | — | nothing of its own — a request the compiler replaces with a cache of its child; left in place it refuses to compile |
| *blend_density* | `BlendDensityFunction` | 1 | — | the child, blended toward old-terrain density where the context holds a non-empty `Blender` |
| *interpolated* | `InterpolatedFunction` | 1 | *cell_size_xz*, *cell_size_y* | the child read at cell corners and interpolated between them |
| *slice* | `SliceFunction` | 1 | *axis*, *coordinate* | the child read with one coordinate pinned |
| *find_top_surface* | `FindTopSurfaceFunction` | 2 | *lower_bound*, *cell_height* | steps down in strides until the density goes positive, and returns that **Y** |
| *old_blended_noise* | `BlendedNoise` | 0 | *xz_scale*, *y_scale*, *xz_factor*, *y_factor*, *smear_scale_multiplier* | the pre-1.18 terrain noise, decoded unseeded |

**Where one class serves several ids.** The three context values are the
constants of one enum, `SimpleDensityFunction`; the eleven unary transforms
are all `UnaryFunction`, a record of a `UnaryFunction.Type` and its input;
the four roundings share `RoundFunction`, and the six arithmetic ids share
`BinaryFunction`. In each case an *enum constant* carries its own codec, and
the node's *codec()* returns it — which is how a re-serialised graph comes
back with the right id. Nothing is folded while parsing:
[the parse step](../systems/worldgen/density-functions.md#parse-one-file-one-graph)
builds each record as written, a constant operand is specialised only when
the graph is compiled (into a sampler such as `BinaryFunction.ConstAddSampler`),
and *add* in the JSON comes back as *add*.

One member of `DensityFunctions` is **not** in this table because it is not
registered: `DensityFunctions.HolderHolder`, the in-memory stand-in for an id
reference, which has no codec at all.

## What the caches become

`DensityFunctionCompiler.getSampler` is the
[compile step](../systems/worldgen/density-functions.md#seed-once-per-dimension):
each dimension's `RandomState` compiles a graph the first time it is asked
for, and no chunk rewrites anything. A *cache* node is a *request*. Before
compiling, the compiler's rewrite inlines every `DensityFunctions.HolderHolder`
and installs a `DensityFunctionCompiler.PreparedCache` in place of each
*cache* node — one per distinct input, so two *cache* nodes around equal
graphs share one cache. A second rewrite wraps each subgraph that ignores an
axis its parent reads, constants and gradients aside, in a *slice* pinned at
zero on that axis. A prepared cache refuses to encode, so only the parsed
graph, which the rewrites copy rather than change, re-serialises.

| node | compiled to | keyed on |
|---|---|---|
| *cache* | a `CachingDensitySampler` carrying the prepared cache's number; its storage is a cell of the `SamplerContext` it runs in | **the volume** for a volume read — one buffer, refilled when a different `DensityVolume` asks — and **the position** for a single sample: the last block sampled, or its entry in the cached volume |
| *interpolated* | a sampler that reads the child at the cell corners, a volume stepped by *cell_size_xz* and *cell_size_y*, and interpolates every block between | nothing — no value outlives the read |
| *blend_density* | a sampler that asks the context for this chunk's [`Blender`](../systems/worldgen/blending.md#what-the-blender-actually-answers) and blends only when there is a non-empty one | not cached |

A context has cache cells only when it was built with
`SamplerContext.Builder.enableCaches`: `NoiseChunk` builds one for each chunk and for each height query, and the biome step, the structure starts and checks, a caching biome resolver, the spawn search and the F3 readout build their own,
and `SamplerContext.EMPTY_UNCACHED` passes every cached read straight through.

Three of the registered nodes above are the constants of one enum,
`SimpleDensityFunction`, and the compiler replaces none of them: each compiles
to a `ContextBoundSampler` that looks its key up in the sampling context on
every read, which is how one compiled graph serves every chunk.

| singleton | reads | with nothing in the context |
|---|---|---|
| `SimpleDensityFunction.BLEND_ALPHA` | `Blender.ALPHA_KEY`, a sampler over the alphas `NoiseChunk`'s constructor computes at quart resolution when the blender is not empty | the constant 1.0 |
| `SimpleDensityFunction.BLEND_OFFSET` | `Blender.OFFSET_KEY`, likewise | the constant 0.0 |
| `SimpleDensityFunction.BEARDIFIER` | `Beardifier.CONTEXT_KEY`, this chunk's [`Beardifier`](../systems/worldgen/structure-placement.md#the-ground-bends-before-the-ground-exists) | the constant 0.0 |

## Bounds

Every node answers `DensityFunction.range`, an `Interval`, without a
position. Most take theirs from a child — *cache*, *interpolated*, *slice*
and *blend_density* all do — and no registered node stores one: `BinaryFunction`, `UnaryFunction` and `ClampFunction` combine their children's ranges through `Interval` on every call, and
`BlendedNoise` derives its own from its parameters. The bounds of a *parsed*
graph are the ones the compiler reads: a noise's range comes from its
definition, not its seed, and no rewrite changes a bound. What a bound is
worth is
[the lecture's argument](../systems/worldgen/density-functions.md#what-a-bound-is-worth-and-which-form-told-you);
this table is which node departs from its child, and how.

| id | its range | |
|---|---|---|
| *add*, *sub*, *mul*, *div*, *min*, *max* | interval arithmetic on the two children's ranges | *mul* takes the least and greatest of the four products of the operands' ends, a zero end giving zero even against infinity; *div* multiplies by the reciprocal's range; *min* and *max* take the element-wise minimum and maximum. A *min* or *max* whose two ranges cannot overlap logs a warning when it is compiled, and only the side that wins whenever the inputs stay inside their declared ranges is sampled |
| *abs*, *square* | the child's ends mapped, with zero as the minimum when the child's range contains zero | `Interval.abs` and `Interval.square` map both ends |
| *reciprocal* | **±infinity** whenever the child's range straddles zero | the reciprocal has no finite bound across zero |
| *clamp* | the child's range, clamped into *min* and *max* | a child already inside them keeps its own, narrower range |
| *find_top_surface* | its *lower_bound* and its upper bound's maximum | **Y coordinates** — this node's range is on a different scale from every other row |
| *noise* | its `NormalNoise`'s, fixed when the noise definition is decoded | the three shifts are ignored; the sixty-four shipped noise definitions come out between ±0.87 and ±5.73 |

`DensityFunctions.HolderHolder`, off the table, asks its target, and throws
while its holder is unbound; forward references parse anyway, because nothing
asks a node for its bound until the graph is compiled.

## What vanilla actually uses

Fifty-five JSON files ship under *worldgen/density_function* — four at the top level, the rest in a directory each for the End, the Nether, the overworld and the overworld's two preset variants — and between them they use
thirty-three of the forty-four ids. The seven `Registries.NOISE_SETTINGS`
files, the recipes [terrain](../systems/worldgen/terrain.md#the-cast) reads — two of them, *caves* and *floating_islands*, named by no shipped world preset — write no id the
density-function files lack. All seven final densities end by adding
*beardifier*, three of them in a file and four inline.

That leaves eleven ids vanilla data never writes. *constant* is never written
as a typed object, because a bare number is one. Nine are maths on a value: *sqrt*,
*reciprocal*, *log*, *sign*, *pow* and the four roundings. And *shift* — the
three-dimensional domain warp — is
[used by nothing](../systems/worldgen/density-functions.md#what-nothing-reaches):
`ShiftNoiseFunction.ShiftA` and
`ShiftNoiseFunction.ShiftB` cover the two two-dimensional warps vanilla wants.

> **For a 1.21-era reader.** *NoiseChunk.wrapNew* is gone: `DensityFunctionCompiler`
> compiles each graph once per dimension, and each chunk supplies a
> `SamplerContext`. *flat_cache*, *cache_2d*, *cache_once* and
> *cache_all_in_cell* are gone, and *cache* does their work. *shifted_noise* is
> *noise* with shift fields, *y_clamped_gradient* is *gradient* on the Y axis,
> *end_islands* is *end_outer_islands* with the central island left to
> *distance_to_point*, and *minValue* and *maxValue* are `DensityFunction.range`.

---

*Rules: names, never code · how the system works, not how the code reads ·
newest version only · every backticked name passes `tools/verify_names.py`.*
