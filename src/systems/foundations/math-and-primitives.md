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
| **integer box** | blocks | `BlockBox` — record of min/max `BlockPos`, iterable | structure bounds, fill commands | `BlockBox.aabb`, `BlockBox.contains`, `BlockBox.extend` |
| **double box** | blocks | `AABB` | entity bounding boxes, block shapes' bounds | `AABB.move`, `AABB.inflate`, `AABB.intersects`, `AABB.clip` |
| **pitch / yaw** | degrees, float | `Vec2` | look direction | `Direction.fromYRot`, `Direction.toYRot`; `Vec3.xRot`, `Vec3.yRot` |
| **model / render space** | float | JOML `Vector3f`, `Matrix4f`, `Quaternionf` (external) | everything under `client/renderer` | `Vec3.toVector3f`; `Direction.step`, `Direction.getRotation`; `com/mojang/math` `Axis` builds quaternions |

`Position` is the three-double interface `Vec3` implements. `Vec3i` is the
mutable-under-the-hood int triple with the arithmetic (`Vec3i.offset`,
`Vec3i.relative`, `Vec3i.distSqr`, `Vec3i.distManhattan`); `BlockPos` adds
the iteration helpers (`BlockPos.betweenClosed`, `BlockPos.withinManhattan`,
`BlockPos.spiralAround`, `BlockPos.breadthFirstTraversal`) backed by
`Cursor3D`, an allocation-free box iterator that also classifies each
position as inside, face, edge or corner.

## Packing

Three long-packings appear everywhere as map keys.

- **`BlockPos.asLong`** — 26 bits X, 26 bits Z, 12 bits Y, high to low.
  Twenty-six bits because the world border's 30,000,000 needs them
  (`BlockPos.MAX_HORIZONTAL_COORDINATE` is 33,554,431); twelve bits of Y
  leaves ±2048. `BlockPos.getFlatIndex` masks off the low four Y bits to
  make a per-column key. `BlockPos.STREAM_CODEC` sends the packed long;
  `Vec3i.STREAM_CODEC` sends three varints.
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
order (`Direction.get2DDataValue`). `Direction.Axis` (X, Y, Z),
`Direction.AxisDirection` and `Direction.Plane` (horizontal, vertical) are
the nested helpers; `Direction8` the compass points; `FrontAndTop` the twelve
jigsaw/crafter orientations; `AxisCycle` the axis permutation
`VoxelShape` lookups use.

Block rotation is `Rotation` and `Mirror` (`world/level/block`), each of
which maps onto `OctahedralGroup` (`com/mojang/math`) — the 48-element
symmetry group of a cube, each element a permutation plus three inversion
flags. `Transformation` wraps a JOML matrix and lazily decomposes it into
translation, left rotation, scale and right rotation for model JSON.

There are two things called `Axis`: `Direction.Axis` and the quaternion
factory in `com/mojang/math`. They are unrelated.

## Shapes and collision

A `VoxelShape` is a set of boxes on a per-axis coordinate grid, backed by a
`DiscreteVoxelShape` bit grid (`BitSetDiscreteVoxelShape`). `Shapes` is the
factory and algebra: `Shapes.block`, `Shapes.empty`, `Shapes.box`,
`Shapes.or`, `Shapes.join` with a `BooleanOp`, `Shapes.collide`,
`Shapes.blockOccludes`. Implementations differ by how the grid is stored —
`CubeVoxelShape` (even divisions), `ArrayVoxelShape` (explicit coordinate
lists), `SliceShape` (one-cell-thick view for face culling) — and
`Shapes.join` picks an `IndexMerger` strategy for the coordinate lists.

`CollisionContext` is what a shape query knows about who is asking:
`CollisionContext.of` an entity (`EntityCollisionContext` — descending,
bottom Y, held item, whether fluids collide), `CollisionContext.empty`, or
`CollisionContext.placementContext`. Ray casts return a `HitResult`:
`BlockHitResult` (position, face, inside, world-border) or
`EntityHitResult`.

## Randomness

`RandomSource` (`net/minecraft/util`) is the interface; the implementations live in
`world/level/levelgen`. Two families coexist in one process:

- **Legacy LCG** — `LegacyRandomSource` (the java.util.Random algorithm),
  `SingleThreadedRandomSource` (same, no atomics), `ThreadSafeLegacyRandomSource`.
  `RandomSource.create` returns a `LegacyRandomSource` with a unique seed;
  this is `Level.random` (inherited unchanged by `ServerLevel` and
  `ClientLevel`), `Entity.random`, `GameRenderer.random`,
  `ParticleEngine.random`. `RandomSource.createThreadLocalInstance` is what
  `LevelRenderer` and `ClientLevel` use for block animation.
- **Xoroshiro** — `XoroshiroRandomSource` (128-bit state via
  `RandomSupport.Seed128bit`), the default for world generation:
  `NoiseGeneratorSettings.getRandomSource` returns
  `WorldgenRandom.Algorithm.XOROSHIRO` unless the settings opt into legacy.
  `RandomState` forks it positionally (`PositionalRandomFactory.at`,
  `PositionalRandomFactory.fromHashOf`) so every feature, ore and aquifer
  gets a deterministic stream from the seed and position.

`WorldgenRandom` wraps any delegate and adds the seeding conventions —
`WorldgenRandom.setDecorationSeed`, `WorldgenRandom.setFeatureSeed`,
`WorldgenRandom.setLargeFeatureWithSalt`, `WorldgenRandom.seedSlimeChunk` —
that make a structure land in the same place for the same seed.

## `Mth` and `Util`

`Mth` is the maths grab-bag (677 importers): `Mth.floor`, `Mth.clamp`,
`Mth.lerp`, `Mth.wrapDegrees`, `Mth.rotLerp`, `Mth.smallestEncompassingPowerOfTwo`,
`Mth.log2`, `Mth.positiveModulo`, `Mth.hsvToRgb`. `Mth.sin` and `Mth.cos`
are lookups in a 65,536-entry table, which matters when reasoning about
animation determinism across platforms. `Util` (in `net/minecraft/util`, 454 importers)
is where the executors live — `Util.backgroundExecutor`, `Util.ioPool`,
`Util.nonCriticalIoPool` — along with time sources and collection helpers;
`Unit` is the single-valued "void" type codecs and futures use.

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
- **Tick randomness and worldgen randomness are different generators.**
  The LCG drives every `Level` and `Entity`; Xoroshiro drives terrain. Seed
  parity guarantees apply only to the second.
- **`Direction.getRotation` treats UP as identity**, and `Direction.step`
  returns a fresh JOML vector while `Direction.getUnitVec3f` returns the
  read-only shared one.
- **`SectionPos` has `x()` and `x(long)`,** instance and static, same name.
- **`BlockUtil` is in `net/minecraft/util`, not `net/minecraft/core`;** `BlockBox`, `BlockMath` and
  `Cursor3D` are in `net/minecraft/core`. `BlockMath` is model-rotation plumbing, not
  coordinates.

## Where to look

`Vec3i` · `BlockPos` · `ChunkPos` · `SectionPos` · `QuartPos` · `GlobalPos` ·
`Vec3` · `AABB` · `Direction` · `Rotation` · `OctahedralGroup` ·
`VoxelShape` · `Shapes` · `CollisionContext` · `HitResult` · `Mth` ·
`RandomSource` · `WorldgenRandom` · `PositionalRandomFactory` · `Util`

---

*Rules: names, never code · how the system works, not how the code reads ·
newest version only · every backticked name passes `tools/verify_names.py`.*
