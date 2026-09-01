# Math and primitives

> Verified against **Minecraft 26.2** · Part II · The coordinate spaces, geometry and randomness every other page assumes. No trace — a table of who owns which space.

## Responsibility

Every system in the game speaks in a handful of value types: an integer
block position, a chunk column, a 16³ section, a double-precision world
position, a direction, a box, a collision shape, a random source. They are
the most-imported classes in the codebase — `BlockPos` alone has 1,221
importers — and most of what is confusing about "which coordinate is this"
is answered by knowing which type a method takes.

## The coordinate spaces

| space | unit | type | owner / notes | conversions |
|---|---|---|---|---|
| **block** | 1 block, int | `BlockPos` (extends `Vec3i`) | immutable; `BlockPos.MutableBlockPos` for loops | `BlockPos.containing` floors a double position; `BlockPos.asLong` / `BlockPos.of` pack to a long |
| **world position** | 1 block, double | `Vec3` (implements `Position`) | entity positions, ray casts, velocities | `Vec3.atCenterOf`, `Vec3.atLowerCornerOf`, `Vec3.atBottomCenterOf` from a `Vec3i`; `Vec3.directionFromRotation` from pitch/yaw |
| **chunk column** | 16 blocks | `ChunkPos` — a **record** of x and z | the key of every chunk map | `ChunkPos.containing` from a `BlockPos`; `ChunkPos.pack` / `ChunkPos.unpack`; `ChunkPos.getMinBlockX`, `ChunkPos.getWorldPosition` |
| **section** | 16³ cube | `SectionPos` (extends `Vec3i`) | lighting, entity sections, render sections | `SectionPos.of` from block/chunk/entity; `SectionPos.blockToSectionCoord` (shift 4), `SectionPos.sectionToBlockCoord`, `SectionPos.sectionRelative` (mask 15); `SectionPos.asLong` |
| **quart / biome** | 4 blocks | `QuartPos` (static only) | biome sampling | `QuartPos.fromBlock` (shift 2), `QuartPos.toBlock`, `QuartPos.fromSection`, `QuartPos.toSection` |
| **region** | 32 chunks | none — methods on `ChunkPos` | the `.mca` file grid | `ChunkPos.getRegionX`, `ChunkPos.getRegionLocalX`, `ChunkPos.minFromRegion`; `ChunkPos.REGION_SIZE` |
| **dimension-qualified block** | — | `GlobalPos` — record of a `Level` key and a `BlockPos` | compass targets, beds, portals | `GlobalPos.of` |
| **integer box** | blocks | `BoundingBox` for structures; `BlockBox` is a newer record that nothing yet uses | structure bounds, piece placement | `BoundingBox.intersects`, `BoundingBox.encapsulate`; `BlockBox.aabb`, `BlockBox.contains` |
| **double box** | blocks | `AABB` (a class of eight public final doubles) | entity bounding boxes, block shapes' bounds | `AABB.move`, `AABB.inflate`, `AABB.intersects`, `AABB.clip` |
| **pitch / yaw** | degrees, float | `Vec2` | look direction, as (yRot, xRot) | `Direction.fromYRot`, `Direction.toYRot`; `Vec3.xRot`, `Vec3.yRot` |
| **pose rotation** | degrees, float ×3 | `Rotations` | armour stand and similar poses | — |
| **model / render space** | float | JOML `Vector3f`, `Matrix4f`, `Quaternionf` (external) | everything under `client/renderer` | `Vec3.toVector3f`; `Direction.step`, `Direction.getRotation`; `com/mojang/math` `Axis` builds quaternions |

`Position` is the three-double interface `Vec3` implements. `Vec3i` is the
mutable-under-the-hood int triple with the arithmetic (`Vec3i.offset`,
`Vec3i.relative`, `Vec3i.distSqr`, `Vec3i.distManhattan`); `BlockPos` adds
the iteration helpers (`BlockPos.betweenClosed`, `BlockPos.withinManhattan`,
`BlockPos.spiralAround`, `BlockPos.breadthFirstTraversal`), each of which
walks a single reused `BlockPos.MutableBlockPos` rather than allocating.
`Cursor3D` is a *different* allocation-free box cursor — the one that also
classifies each position as inside, face, edge or corner
(`Cursor3D.TYPE_INSIDE`, `Cursor3D.TYPE_FACE`, `Cursor3D.TYPE_EDGE`,
`Cursor3D.TYPE_CORNER`) — and it is used by `SectionPos`, `BlockCollisions`
and `ClientLevel`, not by `BlockPos`.

Colours are a primitive too, and they live in `net/minecraft/util`: `ARGB` is
where every pack, unpack, lerp, multiply and alpha helper is, with
`CommonColors` for the named constants, `ColorRGBA` for the codec-friendly
value and `Brightness` for the packed block/sky light pair.

## Packing

Three long-packings appear everywhere as map keys.

- **`BlockPos.asLong`** — 26 bits X, 26 bits Z, 12 bits Y, high to low.
  `BlockPos.PACKED_HORIZONTAL_LENGTH` is literally derived from the world
  border's 30,000,000, which is why it is 26
  (`BlockPos.MAX_HORIZONTAL_COORDINATE` is 33,554,431); the remaining
  `BlockPos.PACKED_Y_LENGTH` is 12, giving −2048 to 2047. The *usable*
  range is narrower: `DimensionType` reserves a 32-block margin, so
  `DimensionType.MIN_Y` is −2032, `DimensionType.MAX_Y` is 2031 and
  `DimensionType.Y_SIZE` is 4064. `BlockPos.getFlatIndex` masks off the low
  four Y bits — it snaps a packed position to the bottom of its own
  16-block section, which is the skylight walk-up idiom, not a per-column
  key (the top eight Y bits survive). `BlockPos.STREAM_CODEC` sends the
  packed long; `Vec3i.STREAM_CODEC` sends three varints.
- **`SectionPos.asLong`** — 22 bits X, 22 bits Z, 20 bits Y. A section-relative
  position packs into a short (`SectionPos.sectionRelativePos`).
- **`ChunkPos.pack`** — X in the low 32 bits, Z in the high 32.
  `ChunkPos.INVALID_CHUNK_POS` is a sentinel; `ChunkPos.isValid` is bounded
  by `ChunkPyramid.MAX_CHUNK_COORDINATE_VALUE`, which lives with the chunk
  status pyramid because the safety margin is derived from how many
  neighbours generation reads.

## Directions and symmetry

`Direction` is the six-valued enum in 3D-data order `DOWN, UP, NORTH, SOUTH,
WEST, EAST` (`Direction.get3DDataValue`); its horizontal subset has its own
order starting at south (`Direction.get2DDataValue`). `Direction.Axis` (X, Y, Z),
`Direction.AxisDirection` and `Direction.Plane` (horizontal, vertical) are
the nested helpers; `Direction8` the compass points; `FrontAndTop` the twelve
jigsaw and crafter orientations; `AxisCycle` the axis permutation
`VoxelShape` lookups use.

Block rotation is `Rotation` and `Mirror` (`world/level/block`), each of
which maps onto `OctahedralGroup` (`com/mojang/math`) — the 48-element
symmetry group of a cube, each element a permutation plus three inversion
flags. That group is not decoration: `Shapes.rotate`, `Shapes.rotateAll`,
`Shapes.rotateHorizontal` and `Shapes.rotateAttachFace` are how a block
declares one shape and gets the other seven. `Transformation` wraps a JOML
matrix and lazily decomposes it into translation, left rotation, scale and
right rotation for model JSON.

There are two things called `Axis`: `Direction.Axis` and the quaternion
factory in `com/mojang/math`. They are unrelated.

## Shapes and collision

A `VoxelShape` is a set of boxes on a per-axis coordinate grid, backed by a
`DiscreteVoxelShape` bit grid (`BitSetDiscreteVoxelShape`). `Shapes` is the
factory and algebra: `Shapes.block`, `Shapes.empty`, `Shapes.box`,
`Shapes.or`, `Shapes.join` with a `BooleanOp`, `Shapes.joinIsNotEmpty`,
`Shapes.collide`, `Shapes.blockOccludes`, with `Shapes.EPSILON` and
`Shapes.BIG_EPSILON` the tolerances every comparison uses. Implementations
differ by how the grid is stored — `CubeVoxelShape` (even divisions),
`ArrayVoxelShape` (explicit coordinate lists), `SliceShape` (a
one-cell-thick view, used for face culling and occlusion) — and `Shapes.join`
picks an `IndexMerger` strategy per axis, returning a `CubeVoxelShape` only
when all three merge evenly.

Shape queries are cheap because they are mostly not computed:
`BlockBehaviour.BlockStateBase.initCache` builds a
`BlockBehaviour.BlockStateBase.Cache` per block state holding the collision
shape, the occlusion shape, whether the collision shape is a full block, and
a per-face sturdiness array.

`CollisionContext` is what a shape query knows about who is asking:
`CollisionContext.of` an entity (`EntityCollisionContext` — descending,
bottom Y, held item, whether fluids collide), `CollisionContext.empty`,
`CollisionContext.placementContext`, plus `PositionCollisionContext` and
`MinecartCollisionContext` for the two cases that are neither. Ray casts
return a `HitResult`: `BlockHitResult` (position, face, inside,
world-border) or `EntityHitResult`.

## Randomness

`RandomSource` (`net/minecraft/util`) is the interface; the implementations live in
`world/level/levelgen` and share `BitRandomSource`, which defines
`RandomSource.nextInt` and friends on top of a raw bit generator. Two
families coexist in one process:

- **Legacy LCG** — `LegacyRandomSource` (the java.util.Random algorithm),
  `SingleThreadedRandomSource` (same, no atomics), `ThreadSafeLegacyRandomSource`.
  `RandomSource.create` returns a `LegacyRandomSource` with a uniquified
  seed; this is `Level.random` (inherited unchanged by `ServerLevel` and
  `ClientLevel`), `Entity.random`, `GameRenderer.random`,
  `ParticleEngine.random`. `RandomSource.createThreadLocalInstance` returns a
  `SingleThreadedRandomSource` and is what `ClientLevel.animateTick` uses for
  block animation, and `LevelRenderer` for the block-destroy overlay.
- **Xoroshiro** — `XoroshiroRandomSource` (128-bit state via
  `RandomSupport.Seed128bit`), the default for world generation:
  `NoiseGeneratorSettings.getRandomSource` returns
  `WorldgenRandom.Algorithm.XOROSHIRO` unless the settings opt into legacy.
  `RandomState` forks it positionally (`PositionalRandomFactory.at`,
  `PositionalRandomFactory.fromHashOf`) for the named noise consumers — the
  aquifer and the ore placer each get their own deterministic stream from
  the seed and position.

`WorldgenRandom` wraps any delegate and adds the seeding conventions —
`WorldgenRandom.setDecorationSeed`, `WorldgenRandom.setFeatureSeed`,
`WorldgenRandom.setLargeFeatureWithSalt`, `WorldgenRandom.seedSlimeChunk` —
that make a structure land in the same place for the same seed. Features go
through *those*, not through `RandomState`.

There is a third randomness path that is neither: `RandomSequence` and
`RandomSequences`, a saved, `Identifier`-keyed table of `XoroshiroRandomSource`
streams derived from the world seed, which is what makes a loot table and
`/random` reproducible across sessions. And a fourth that is not a
`RandomSource` at all: `LinearCongruentialGenerator`, the bare mixer
`BiomeManager` uses for biome fuzzing.

`Mth.nextGaussian` is produced by `MarsagliaPolarGaussian`, which caches a
spare value — which is why reseeding a source must reset it.

## `Mth` and `Util`

`Mth` is the maths grab-bag (677 importers): `Mth.floor`, `Mth.clamp`,
`Mth.lerp`, `Mth.wrapDegrees`, `Mth.rotLerp`, `Mth.smallestEncompassingPowerOfTwo`,
`Mth.log2`, `Mth.positiveModulo`, `Mth.hsvToRgb`. `Mth.sin` and `Mth.cos`
are lookups in a 65,536-entry table (`Mth.cos` is the same table with a
quarter-turn phase shift), and the table is filled from the JDK's ordinary
sine rather than its strict one — so the platform-dependent step, if
you are chasing animation determinism, is the table's construction and not
the lookup. `Util` (in `net/minecraft/util`, 454 importers) is where the
executors live — `Util.backgroundExecutor`, `Util.ioPool`,
`Util.nonCriticalIoPool` — along with time sources and collection helpers;
`Unit` is the single-valued "void" type codecs and futures use. The other
numeric odds and ends worth knowing by name are `CubicSpline` (terrain
shaping), `InclusiveRange`, and `BitStorage`, the packed-integer array
underneath every palette.

## Invariants and surprises

- **`ChunkPos` is a record with no *asLong*.** The names are `ChunkPos.pack`
  and `ChunkPos.unpack`; construction from a block is `ChunkPos.containing`;
  the components are accessed as x() and z().
- **`Vec3i.toMutable` returns a JOML `Vector3i`,** not a
  `BlockPos.MutableBlockPos`; the mutable block position is constructed
  directly and its `BlockPos.MutableBlockPos.set` / `BlockPos.MutableBlockPos.move`
  are the loop idiom.
- **`BlockPos` is immutable, `Vec3i` only pretends to be.** `Vec3i` keeps
  protected setters that `BlockPos.MutableBlockPos` uses; every other
  subclass treats them as final. `BlockPos.immutable` is the copy to call
  before storing a mutable one.
- **`Level.random` deliberately crashes on cross-thread use.**
  `LegacyRandomSource` holds an atomic seed not for safety but as a
  *detector*: a concurrent reseed fails the compare-and-set and raises a
  `ThreadingDetector` exception. The genuinely safe variant,
  `ThreadSafeLegacyRandomSource`, and `RandomSource.createThreadSafe` are
  both deprecated. Touching a level's random from a worker is meant to be
  loud.
- **Tick randomness and worldgen randomness are different generators.**
  The LCG drives every `Level` and `Entity`; Xoroshiro drives terrain **and**
  the saved `RandomSequences` behind loot and `/random`. Seed-parity
  guarantees apply to the second family only.
- **`BlockBox` is declared and unused.** It is a tidy `BlockPos`-pair record
  in `net/minecraft/core`, and in 26.2 nothing calls it; structure bounds
  are still `BoundingBox` in `world/level/levelgen/structure`. Worth knowing
  before assuming a rename happened.
- **`Direction.getRotation` treats UP as identity**, and `Direction.step`
  returns a fresh JOML vector while `Direction.getUnitVec3f` returns the
  read-only shared one.
- **`SectionPos` has `x()` and `x(long)`,** instance and static, same name.
- **`BlockUtil` is in `net/minecraft/util`, not `net/minecraft/core`;** `BlockBox`, `BlockMath` and
  `Cursor3D` are in `net/minecraft/core`. `BlockMath` is model-rotation plumbing, not
  coordinates.

## Where to look

`Vec3i` · `BlockPos` · `ChunkPos` · `SectionPos` · `QuartPos` · `GlobalPos` ·
`Cursor3D` · `Vec3` · `AABB` · `BoundingBox` · `Direction` · `Rotation` ·
`OctahedralGroup` · `VoxelShape` · `Shapes` · `CollisionContext` ·
`HitResult` · `ARGB` · `Mth` · `RandomSource` · `BitRandomSource` ·
`WorldgenRandom` · `PositionalRandomFactory` · `RandomSequences` · `Util`

---

*Rules: names, never code · how the system works, not how the code reads ·
newest version only · every backticked name passes `tools/verify_names.py`.*
