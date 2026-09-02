# Hand-built structures

> Verified against **Minecraft 26.2** · Part XII · A stronghold is generated: a piece grammar written in Java, a budget that decides when to stop, a graph assembled at an imaginary height and moved down afterwards, and a whole structure thrown away and rebuilt because it had no portal room.

## Responsibility

[Structures](structures.md) traces a village, and a village is a jigsaw:
pieces come from a data-pack registry and find each other through jigsaw
blocks. That is one of the sixteen structure types. **The other fifteen use
an older assembler that is still the majority of the code** — 30 classes
and about 10,000 lines under `levelgen/structure/structures`, against
roughly 1,300 for the whole jigsaw package.

In this model there is no pool and no registry of pieces. A piece is a Java
class that knows how to write its own blocks, and it grows the structure by
constructing its own neighbours. Strongholds, mineshafts, nether
fortresses, ocean monuments, woodland mansions, end cities, ruined portals,
igloos, shipwrecks, ocean ruins, desert pyramids, jungle temples, swamp
huts, buried treasure and nether fossils are all built this way.

Everything *outside* the assembler is shared with jigsaw and belongs to
[structures](structures.md): the placement lottery, `Structure`,
`StructureStart`, `StructureCheck`, the reference scan, `Beardifier`, and
the whole `.nbt` template system. This page is only the part where the
pieces come from.

The one sentence a player recognises: *the stronghold corridor that dead-ends
into a library, and the fact that there is always exactly one portal room.*

## The data it owns

- **`StructurePiece`** — the base class, and the reason this system holds
  together. It owns a **mutable** `BoundingBox`, a `Direction` orientation,
  a `Mirror`, a `Rotation`, a `StructurePiece.genDepth`, and its
  `StructurePieceType`.
  The orientation is not independent of the other two:
  `StructurePiece.setOrientation` derives mirror and rotation from it, and
  a south-facing piece is expressed as a **left-right mirror** rather than
  a 180° rotation. That trick is why every piece in this package is written
  once, in a north-facing local frame, and comes out correct four ways.
- **The coordinate transform** — `StructurePiece.getWorldX`,
  `StructurePiece.getWorldY` and `StructurePiece.getWorldZ` map
  piece-local coordinates into the world. Local Y is measured **from the
  box floor**, which is what makes moving a finished graph vertically free.
  When the orientation is null the transform is the identity, which is how
  `BuriedTreasurePieces` gets away with a bounding box one block wide.
- **The write helpers** — `StructurePiece.placeBlock` is the single choke
  point: it converts to world coordinates, drops the write if it is outside
  the chunk box it was handed, applies the piece's mirror and rotation *to
  the block state*, and schedules a fluid tick if it displaced one.
  `StructurePiece.generateBox` fills a local box while distinguishing edge
  cells from interior ones; `StructurePiece.generateAirBox`,
  `StructurePiece.generateMaybeBox`,
  `StructurePiece.generateUpperHalfSphere`,
  `StructurePiece.fillColumnDown` and `StructurePiece.createChest` are the
  rest of the vocabulary.
- **`StructurePiece.BlockSelector`** — a stateful per-block state chooser,
  and the thing that gives a structure its texture.
  `StrongholdPieces.SmoothStoneSelector` is the canonical one: on a box
  edge it rolls cracked, mossy or infested stone brick and otherwise plain,
  and interior cells become cave air. One small object is the entire visual
  character of a stronghold. `JungleTemplePiece.MossStoneSelector` is the
  other.
- **`StructurePieceAccessor`** — an eleven-line interface with two methods,
  `StructurePieceAccessor.addPiece` and
  `StructurePieceAccessor.findCollisionPiece`. `StructurePiecesBuilder`
  implements it, and `StructurePiece.findCollisionPiece` is a **linear scan
  returning the first overlapping box**. There is no spatial index.
- **`StructurePiecesBuilder`'s vertical moves** —
  `StructurePiecesBuilder.moveBelowSeaLevel`,
  `StructurePiecesBuilder.moveInsideHeights` and
  `StructurePiecesBuilder.offsetPiecesVertically`, each of which shifts
  every piece in the list.
- **`TemplateStructurePiece`** — the bridge to the `.nbt` machinery, for
  the structures that are procedural in *layout* but templated in
  *content*. It owns a `StructureTemplate`, a `StructurePlaceSettings` and
  a mutable `TemplateStructurePiece.templatePosition`, and its bounding box
  is derived rather than
  stored.
- **`ScatteredFeaturePiece`** — the base for one-shot surface buildings,
  adding a `ScatteredFeaturePiece.heightPosition` and the two ground-finders
  `ScatteredFeaturePiece.updateAverageGroundHeight` and
  `ScatteredFeaturePiece.updateHeightPositionToLowestGroundHeight`.
  `SinglePieceStructure` is the forty-line `Structure` that places exactly
  one of them.

## When it runs

All of it at `ChunkStatus.STRUCTURE_STARTS`, inside the same
`Structure.GenerationStub` consumer the jigsaw assembler runs in
([structures](structures.md)) — so the whole graph is built in memory, on a
worldgen worker, with no world access and no blocks written. Writing
happens later, at `ChunkStatus.FEATURES`, once per chunk the structure
overlaps.

**`StructurePiece.addChildren` is not a framework hook.** Its default body
is empty and nothing in the framework ever calls it; every call site is a
structure's own generation code. The recursion is arranged by each family
for itself, in one of two shapes:

- **A shuffled work queue** — strongholds and nether fortresses. A new
  piece is added to the builder *and* to the start piece's pending list;
  the structure then drains that list by repeatedly removing a **random**
  index and expanding it. Growth is therefore breadth-ish and unbiased.
- **Inline recursion** — mineshafts. `MineshaftPieces` expands each new
  piece immediately, depth-first, so the first branch of a crossing is
  fully grown before the second is attempted.

## The trace: a stronghold

```mermaid
sequenceDiagram
    participant CG as ChunkGenerator
    participant SS as StrongholdStructure
    participant SP as StrongholdPieces
    participant PB as StructurePiecesBuilder
    participant ST as StructureStart

    CG->>SS: Structure.generate → findGenerationPoint → GenerationStub
    loop until a portal room exists
        SS->>PB: clear
        SS->>SS: setLargeFeatureSeed(seed + tries++, chunk)
        SS->>SP: resetPieces — static weight table and imposedPiece
        SS->>SP: new StartPiece → addChildren the start room
        loop drain pendingChildren at a random index
            SP->>SP: pick by weight; reject the previous type; 5 attempts
            SP->>PB: findCollisionPiece(candidate box) — linear scan
            PB-->>SP: null → construct; hit → try the next candidate
            SP->>PB: addPiece · append to pendingChildren
        end
        SS->>PB: moveBelowSeaLevel(seaLevel, minY, random, 10)
    end
    PB-->>ST: build → PiecesContainer → StructureStart
    Note over ST: at FEATURES: placeInChunk → postProcess per overlapping piece
```

1. **Build at an imaginary height.** The start piece is constructed at a
   fixed Y — 64 for strongholds and fortresses, 50 for mineshafts — with no
   idea where the ground is. Every collision test, every staircase descent
   and the floor guard that refuses a box below Y 10 is done in that frame.
2. **Pick a piece by weight, with a budget.**
   `StrongholdPieces.STRONGHOLD_PIECE_WEIGHTS` pairs each piece class with
   a weight *and* a maximum placement count: straight corridors and turns
   are unlimited, a room crossing may appear six times, a library twice, a
   portal room **once**. Library and portal room additionally refuse to
   appear before a certain depth. The picker makes up to five weighted
   attempts, rejecting whichever type was placed immediately before, and
   falls back to a filler corridor.
3. **Collision is the other brake.** Each candidate constructor computes
   its box and asks `StructurePieceAccessor.findCollisionPiece`; a hit
   means the candidate simply is not built. Some pieces negotiate instead
   of failing — a mineshaft corridor tries decreasing lengths until one
   fits, and a stronghold library falls back from its tall variant to its
   short one.
4. **Growth stops when the budget is spent, not when the depth runs out.**
   The depth cap is 50 for strongholds — far more than any real stronghold
   reaches. What actually ends generation is that the piece picker returns
   nothing once **every piece type with a limit has hit it**, even though
   corridors and turns are unlimited.
5. **Move the whole graph.** `StructurePiecesBuilder.moveBelowSeaLevel`
   shifts every piece so the graph's top sits below sea level; nether
   fortresses use `StructurePiecesBuilder.moveInsideHeights` to land in a
   band; a mesa mineshaft uses
   `StructurePiecesBuilder.offsetPiecesVertically` to sit between sea level
   and the surface. This is the payoff for local-Y-from-the-box-floor.
6. **Throw it away if it is wrong.** `StrongholdStructure` wraps the whole
   of the above in a loop that repeats **while the builder is empty or no
   portal room was placed**, reseeding with the world seed plus a try
   counter each time. A stronghold without an end portal is not patched up;
   it is discarded and generated again from a different seed.
7. **Write, per chunk.** At `ChunkStatus.FEATURES`,
   `StructureStart.placeInChunk` calls `StructurePiece.postProcess` on
   every piece whose box intersects this chunk, and `StructurePiece.placeBlock` drops
   anything outside it. A piece's `StructurePiece.postProcess` therefore runs **once per
   chunk it overlaps**, which is why pieces persist booleans like
   *has placed chest* and *spawned witch* — the method must be idempotent.

## Interfaces

- **Called by:** `Structure.generate`, through each structure's
  `Structure.findGenerationPoint`; then `StructureStart.placeInChunk` from
  `ChunkGenerator.applyBiomeDecoration`.
- **Calls into:** `WorldGenLevel` for writes, `StructureTemplate` for the
  templated families, `ChunkGenerator` height queries, and — for
  `TemplateStructurePiece` — the entire processor stack in
  the *templatesystem* package, shared with jigsaw.
- **Crosses the network as:** nothing. Ordinary blocks.
- **Data-driven by:** almost nothing, and that is the point. Piece choice,
  weights, budgets, layout rules and adjacency are all Java.
  `Registries.STRUCTURE` still supplies the settings wrapper, and the
  templated families read `.nbt` files, but a data pack cannot add a room
  to a stronghold.

## The families

**Procedural piece graphs** — the pieces write their own blocks.
`StrongholdPieces`, `MineshaftPieces` and `NetherFortressPieces` are the
three that genuinely grow a graph. The fortress runs *two* weight tables
and a mode switch: a castle entrance is a one-way door out of bridge mode
into castle mode, and only a T-balcony can fall back, on a one-in-eight
roll per branch.

**Grid and graph solvers** — `WoodlandMansionPieces` and
`OceanMonumentPieces` do not grow a piece graph at all; they solve a layout
first and emit pieces afterwards, and neither ever calls
`StructurePieceAccessor.findCollisionPiece`. Their layout *is* the
collision guarantee.

**Template-backed pieces** — `EndCityPieces`, `RuinedPortalPiece`,
`OceanRuinPieces`, `ShipwreckPieces`, `IglooPieces`, `NetherFossilPieces`
and `BuriedTreasurePieces`. Procedural placement, `.nbt` content, and
therefore the same processors and the same `StructureTemplate.placeInWorld`
the jigsaw path uses.

**One-shot surface buildings** — `DesertPyramidPiece`, `JungleTemplePiece`
and `SwampHutPiece` over `ScatteredFeaturePiece`. No graph, no children:
one box, dropped on the ground.

## Invariants and surprises

- **A stronghold is a rejection sampler.** The portal room is weighted
  heavily, capped at one, and forbidden near the start — and if the graph
  finishes without one, `StrongholdStructure` clears the builder, adds one
  to the seed and does the whole thing again. It is the only structure in
  the game that regenerates itself until it likes the result.
- **The portal room has no children.** Its entire `StructurePiece.addChildren` body
  records itself on the start piece. That record is both the loop's exit
  condition and what `/locate` reports, so the command points at the
  portal rather than the entrance.
- **Generation is not thread-safe, and visibly so.** `StrongholdPieces`
  keeps its remaining-piece list, its running weight total and a
  one-shot "force this piece next" override in **private static fields**,
  reset by `StrongholdPieces.resetPieces` from inside a generation lambda
  that runs on chunk workers. The nether fortress's placement counters live
  on static array elements that are merely reset at start-piece
  construction, so the per-structure budget is an illusion. Two strongholds
  generating at once would interleave. It is rare enough not to bite, and
  it is the sharpest contrast with the stateless jigsaw path.
- **The mansion's floor plan is grown and then tidied to a fixed point.**
  Corridors are recursed out from the entrance on an 11×11 grid, rooms are
  stamped alongside them, and then an edge-cleaning pass runs **repeatedly
  until nothing changes**, filling any cell with enough occupied
  neighbours. That pass is why a mansion is a solid block of building
  rather than the thin maze the corridor walk actually produced. Rooms are
  then greedily merged into 2×2, 1×2 and 1×1 units, with type, id and flags
  packed into a single int per cell; a room that ends up with no corridor
  edge becomes a **secret room**, reachable only from above.
- **A mansion may have two floors instead of three.** The third floor needs
  a second-floor room with a door to hang its staircase on. If there is
  none, or no free direction to grow into, the third-floor grid is blanked
  entirely.
- **The ocean monument carves its maze backwards.** It wires a lattice of
  rooms fully connected, then repeatedly closes a random opening and
  **keeps the closure only if both sides can still reach the entrance
  room**, using a depth-first reachability walk with an increasing scan
  counter in place of a visited set. Rooms are then fitted by a list of
  room-shape fitters in fixed order, first match wins, so the large double
  rooms get first refusal and the plain room is the fallback.
- **The ocean monument is the one structure that re-derives itself on
  load.** Its room pieces are held privately on the main building and never
  reach the builder, so they are never saved — and their save method is
  empty anyway. `StructureStart.loadStaticStart` therefore carries a
  hardcoded type check that calls
  `OceanMonumentStructure.regeneratePiecesAfterLoad`, which reads position
  and orientation from the save and rebuilds every room from the world
  seed. Every other structure deserialises what it wrote.
- **End city sections collide as groups, not as pieces.** Each candidate
  section is generated into a scratch list and tagged with one shared
  random `StructurePiece.genDepth` — used as a **group identity, not a depth**. The
  section is accepted only if every collision it finds is with a piece
  carrying the *parent's* tag; one foreign overlap discards the entire
  candidate list atomically. Bridges opt out with a tag of −1, and the ship
  becomes likelier the longer the bridge gets, with at most one per city.
- **Ruined portal decay is a processor stack, not code.** The rot, the
  gold-block gaps, the lava-to-magma substitutions and the mossiness are
  `StructureProcessor`s assembled per portal and stored in the saved piece,
  so decay reproduces exactly on reload — and every one of those
  processors is shared with the jigsaw path.
- **Two pieces deliberately widen the chunk they were given.** A ruined
  portal and a nether fossil both call `BoundingBox.encapsulate` on the
  writable area so they are placed whole from a single chunk rather than
  sliced across several. `BoundingBox` is mutable and the box is shared
  between the pieces of one start, so the widening leaks — harmlessly
  today, because both structures have exactly one piece.
- **A saved bounding box is not always where the structure is.** Buried
  treasure rewrites its own box while placing; igloos are built at a
  hardcoded Y 90 and re-seated at write time from the live heightmap, then
  put *back*; shipwrecks latch a flag so the second chunk does not move
  them again. For these types the persisted box is a placement hint, not a
  location.
- **The whole-graph move is deprecated; the jigsaw path has nothing
  deprecated in it.** `StructurePiecesBuilder.moveBelowSeaLevel`,
  `StructurePiecesBuilder.offsetPiecesVertically`,
  `TemplateStructurePiece.move` and the mansion's siting helper are all
  marked for removal. Mojang has flagged the idiom, not just the methods.
- **The reference position comes from piece zero.**
  `StructureStart.placeInChunk` derives the position it passes to every
  template from the *first* piece in the list, and that position seeds the
  processors' randomness. Piece order is semantic, not cosmetic.
- **Hand-built templates still honour one jigsaw rule.**
  `TemplateStructurePiece.postProcess` scans what it placed for jigsaw
  blocks and replaces each with its final state — so a stray jigsaw block
  in a mansion `.nbt` resolves quietly instead of connecting to anything.
  `Beardifier`'s type test is the only place at runtime where the
  two assemblers are told apart.
- **Dead code, and dead constants.** `PostPlacementProcessor` is referenced
  nowhere; `PieceGenerator` and `PieceGeneratorSupplier` only by each
  other. Three separate *magic start Y* constants are read by nothing — the
  literals are retyped at their use sites — which is a trap for anyone
  changing one.
- **One discarded random draw is load-bearing.**
  `MineshaftStructure.findGenerationPoint` opens by drawing a double and
  throwing it away: a random-stream alignment relic that has to stay, or
  every mineshaft in every existing world moves.

## Where to look

`StructurePiece` · `StructurePiece.addChildren` ·
`StructurePiece.placeBlock` · `StructurePiece.generateBox` ·
`StructurePiece.BlockSelector` · `StructurePiece.setOrientation` ·
`StructurePieceAccessor.findCollisionPiece` · `StructurePiecesBuilder` ·
`StructurePiecesBuilder.moveBelowSeaLevel` ·
`StructurePiecesBuilder.moveInsideHeights` · `StrongholdStructure` ·
`StrongholdPieces.STRONGHOLD_PIECE_WEIGHTS` ·
`StrongholdPieces.resetPieces` · `MineshaftPieces` ·
`NetherFortressPieces` · `WoodlandMansionPieces` ·
`OceanMonumentPieces` · `EndCityPieces` · `RuinedPortalPiece` ·
`TemplateStructurePiece` · `ScatteredFeaturePiece` ·
`SinglePieceStructure` · `OceanMonumentStructure.regeneratePiecesAfterLoad` ·
`StructureStart.loadStaticStart`

---

*Rules: names, never code · how the system works, not how the code reads ·
newest version only · every backticked name passes `tools/verify_names.py`.*
