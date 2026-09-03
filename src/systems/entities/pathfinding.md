# Pathfinding

> Verified against **Minecraft 26.2** · Part VI · A villager decides to walk to its bed, and eight ticks later it is standing still against a fence, having formally given up.

A behaviour has produced a position and stopped caring. Everything between
that position and a mob actually leaning into a direction is this page: one
A\* search over a snapshot of already-loaded chunks, a `Path` of nodes, and a
control that has to be told again every single tick. The part of it people
recognise is the failure. **Giving up is machinery, not an absence of it** —
every node the mob is walking towards carries a timeout computed from its
distance and the mob's current speed, three times over that budget abandons
the path outright, and a separate check every hundred ticks asks whether the
mob has covered a quarter of the ground its speed says it should have. The
mob you watch walk into a wall and then wander off is running a scheduled
surrender.

Above the waterline is [goals and brains](ai-goals-and-brains.md), which
decides *where*; this page is *how*, and it is the same machinery whichever
decision system asked.

## The cast

| class | what it decides | thread |
|---|---|---|
| `PathNavigation` | when to search, what budget to search with, when to give up | server main |
| `PathNavigationRegion` | which blocks the search is allowed to see — a snapshot, never a load | server main |
| `NodeEvaluator` | what a block *is* to this mob, as a `PathType` | server main |
| `PathTypeCache` | the 4,096-entry memo that makes that affordable | server main, owned by `ServerLevel` |
| `PathFinder` | the A\* itself, bounded by a node budget | server main |
| `Path` | the node list, and whether it actually reaches the target | server main, with a stream codec for the debug channel only |
| `MoveControl` | the one place a position becomes a yaw and a speed | server main |

Nothing here is asynchronous. There is not a future, an executor or a thread
anywhere in the pathfinder, and every entry point takes a `ServerLevel` or a
`Mob` on one. Nothing crosses the network either, except when a debug client
has subscribed.

## The pipeline

```mermaid
flowchart TB
    WANT["a goal or a behaviour calls PathNavigation.createPath or moveTo"]
    GATE["four early exits: no targets, mob below the world floor, canUpdatePath false, or a live path to the same target"]
    REGION["PathNavigationRegion: a cube of chunks fetched with ChunkSource.getChunkNow"]
    EVAL["NodeEvaluator turns each candidate block into a PathType, through PathTypeCache"]
    SEARCH["PathFinder: A* over a BinaryHeap, bounded by maxVisitedNodes"]
    PATH["a Path — reached, or the best node it found"]
    FOLLOW["PathNavigation.tick advances the node index"]
    CTRL["MoveControl.setWantedPosition, re-issued every tick"]
    GIVEUP["stuck check every 100 ticks, node timeout at three times the budget"]

    WANT --> GATE
    GATE -- "returns null, or the existing path unchanged" --> WANT
    GATE --> REGION
    REGION --> EVAL
    EVAL --> SEARCH
    SEARCH --> PATH
    PATH --> FOLLOW
    FOLLOW --> CTRL
    FOLLOW --> GIVEUP
    GIVEUP -- "stop, and the behaviour is told the path is done" --> WANT
```

## Asking: the four ways a search does not happen

`PathNavigation.createPath` refuses before it does anything expensive. It
returns null on an empty target set, on a mob below `Level.getMinY`, and on
`PathNavigation.canUpdatePath` — which for `GroundPathNavigation` means *on
the ground, in liquid, or riding something*, so an airborne mob simply cannot
ask. The fourth exit is the interesting one: if there is already a path that
is not done and the requested target is among its targets, **the existing
path is returned unchanged**. Re-asking for a destination you are already
walking to costs nothing and changes nothing.

`PathNavigation.recomputePath` is the other entrance, and it is rate-limited
rather than refused. More often than every twenty game ticks, or with
`PathNavigation.canUpdatePath` false, it sets a flag instead and the next
`PathNavigation.tick` tries again. That deferral is what keeps a mob standing
in a doorway from re-searching twenty times a second.

## The budget, which is also the map

One number governs both how hard the search may work and how much world it
may look at. `PathNavigation` builds its `PathFinder` with
`Attributes.FOLLOW_RANGE`'s **base** value times sixteen, and
`PathNavigation.updatePathfinderMaxVisitedNodes` later recomputes it as
sixteen times the larger of the *modified* follow range and
`PathNavigation.setRequiredPathLength` — 16 by default, and raised by seven
classes: 48 for `Villager`, `Allay`, `Bee`, `CopperGolem` and `HappyGhast`,
40 for `Llama`, 32 for `Fox`. `PathNavigation.setMaxVisitedNodesMultiplier`
scales the result for one search.

The same maximum path length becomes the **radius of the
`PathNavigationRegion`**, plus an offset of 8 or 16 depending on which
`PathNavigation.createPath` overload was used — and inside the search it appears twice more,
as a test on the current node's distance from the start and on each
neighbour's walked distance. A villager can find a bed 48 blocks away because
one attribute is 48; it cannot find one 60 blocks away no matter how open the
ground is.

That region is built by asking `ChunkSource.getChunkNow` for every chunk in
the cube. **A path search never loads a chunk and never blocks** — an absent
chunk is a null entry that reads as air. This is the same discipline
`Entity.move` uses for collisions, and it is why AI cannot stall a tick.

## What a block is

`NodeEvaluator` answers *what is this position, to this mob* with a
`PathType`: 27 constants, each carrying a default cost, and **a negative cost
means impassable, not expensive**. `PathType.BLOCKED`, `PathType.LAVA`,
`PathType.FENCE`, `PathType.LEAVES`, the two closed doors and
`PathType.POWDER_SNOW` are all −1; `PathType.WATER` is 8, `PathType.FIRE` 16,
`PathType.OPEN` and `PathType.WALKABLE` 0. A mob overrides any of them for
itself with `Mob.setPathfindingMalus`, read back through
`Mob.getPathfindingMalus` — which is how a zombified piglin walks through
fire and a spider does not.

Four evaluators cover the movement modes: `WalkNodeEvaluator`, and the three
that specialise it or replace it — `FlyNodeEvaluator` and
`AmphibiousNodeEvaluator` extend the walker, `SwimNodeEvaluator` extends
`NodeEvaluator` directly. Each `PathNavigation` subclass chooses one:
`GroundPathNavigation`, `FlyingPathNavigation`, `WaterBoundPathNavigation`,
`AmphibiousPathNavigation`, and `WallClimberNavigation` on top of the ground
one.

Classifying a block is expensive enough to memo. `PathTypeCache` is a fixed
4,096-entry table owned by `ServerLevel`, consulted through
`PathfindingContext` — which attaches it **only** on a `ServerLevel` and
falls back to computing the type from scratch otherwise. It is invalidated
one position at a time from `ServerLevel.sendBlockUpdated`, which is the
subject of the last section.

## The search

`PathFinder.findPath` is plain A\* over a `BinaryHeap`, and three of its
details decide what mobs feel like.

**It is bounded by a node count, not by a distance.** The loop breaks as soon
as it has popped its budget of nodes — `PathFinder.setMaxVisitedNodes`,
scaled by the multiplier. A
search through open ground reaches much further than the same budget spends
in a maze.

**The heuristic is inflated.** Each neighbour's *h* is the best straight-line
estimate multiplied by 1.5, which makes the search greedy: it finds a route
sooner and the route it finds is not guaranteed to be the shortest. Ties, at
the end, go to the path with the fewest nodes.

**A failed search still returns a path.** If no target came within
the *reach range* — measured as a Manhattan distance from the popped node — the
finder reconstructs a path to the closest node it managed to reach and marks
it *not reached*. That is what `Path.canReach` reports, and it is the number
that matters rather than "was a path found": `AcquirePoi` tests it before
claiming a point of interest, and `MoveToTargetSink` turns a false into a
*cannot reach* memory. A null return means only that the node list came out
empty.

One more thing the search does not do unless asked: it accumulates its closed
set, and attaches it to the `Path`, only while something is subscribed to
`DebugSubscriptions.ENTITY_PATHS`. `PathNavigation` installs that predicate
in its constructor, off the server's `ServerDebugSubscribers`. `Path` has a
stream codec for exactly this and no gameplay reason.

```mermaid
sequenceDiagram
    participant MTS as MoveToTargetSink
    participant PN as PathNavigation
    participant PNR as PathNavigationRegion
    participant NE as NodeEvaluator
    participant PF as PathFinder
    participant MoveC as MoveControl

    MTS->>PN: createPath to the walk target, then moveTo with a speed modifier
    PN->>PN: four early exits, then push the pathfind profiler section
    PN->>PNR: build a cube of maxPathLength plus the offset, with getChunkNow
    PN->>PF: findPath — region, mob, targets, maxPathLength, reachRange, multiplier
    PF->>NE: getStart, then getNeighbors per popped node
    NE->>PNR: getPathTypeFromState, through PathTypeCache on a server level
    PF-->>PN: a Path, reached or best-effort, with canReach set accordingly
    PN->>PN: trimPath, record the stuck-check position, keep the node index
    Note over PN,MoveC: every tick from here
    PN->>MoveC: setWantedPosition for the next node, at speedModifier
    MoveC->>MoveC: tick — set yaw, set speed, reset the operation to WAIT
```

## Following it, one tick at a time

`PathNavigation.tick` advances the node index and calls
`MoveControl.setWantedPosition` with the next node and the speed modifier.
It has to do that **every** tick, because `MoveControl.tick` sets its own
`MoveControl.Operation` back to `MoveControl.Operation.WAIT` as it handles
the move — the control is a one-shot instruction, not a destination it
remembers.

`MoveControl.setWantedPosition` is the single method where any decision, goal
or brain, becomes movement. It is not the single *call site*: eight places
skip the pathfinder and drive the control directly — `TemptGoal`,
`TryFindWaterGoal`, and the per-mob goals of `Bee`, `Fox`, `Rabbit`,
`Blaze`, `Ghast` and `Vex` — which is why a tempted animal drifts towards you
in a straight line through terrain a path search would have routed around.

Three more controls sit beside it and are the rest of what turns a decision
into a pose. `LookControl` aims the head, `JumpControl` fires a jump the mover
then executes, and `BodyRotationControl` swings the body to follow the head
after a run of stable ticks. `BodyRotationControl.clientTick` is a leftover
name: `LivingEntity.tick` calls `Mob.tickHeadTurn` with no side check at all,
so it runs on both sides every tick.

The mover itself is Part VI's [movement and
collision](movement-and-collision.md) — the control sets `LivingEntity.xxa`,
`LivingEntity.zza` and the speed, and `LivingEntity.travel` does the rest.

## Giving up

Two independent timers, and they answer different questions.

`PathNavigation.doStuckDetection` runs its first half **every hundred ticks**:
it compares where the mob is with where it was at the last check, against a
threshold of the mob's effective speed times 100 times 0.25 — a quarter of
the ground the speed claims. Below that, `PathNavigation.isStuck` is set and
the path is stopped. The effective speed is the speed itself at 1.0 or above
and the *square* of it below, which quietly makes the threshold far more
forgiving for slow mobs.

The second half is per node. When the next node changes, the navigation
computes a time budget for it — the distance to that node divided by the
mob's speed, times twenty — and accumulates real ticks against it. Past
**three times** that budget, `PathNavigation.timeoutPath` resets the counters
and stops. This is the one that catches a mob whose path is fine and whose
route is blocked by something the search could not see.

Both endings are the same ending from outside: `PathNavigation.isDone`
becomes true, and whichever behaviour or goal was waiting on the path finds
out on its next evaluation.

## The one place the world pushes back

Everything above is AI asking the world questions. `ServerLevel.sendBlockUpdated`
is the single call in the other direction. It invalidates the changed
position in the path-type cache **unconditionally**, and then — only if
`Shapes.joinIsNotEmpty` says the collision shape actually changed — walks
`ServerLevel.navigatingMobs`, asks each navigation
`PathNavigation.shouldRecomputePath` about the position, and calls
`PathNavigation.recomputePath` on the ones that say yes. The whole block is
wrapped in a re-entrancy guard, because a recompute can itself change blocks;
a recursive call logs and, in a development environment, pauses.

That is why closing a door in front of a mob re-routes it and repainting a
block does not.

## Why mobs look stupid

**Why do mobs take silly routes?** The heuristic is multiplied by 1.5, so the
search is deliberately greedy — it stops at the first route that reaches,
not the best one. Cost is a per-block malus, not a distance, so a mob will
happily walk three blocks further to avoid a `PathType.WATER` node worth 8.

**Why does a mob stop dead at the edge of my render distance?** It did not.
The search only sees chunks already loaded on the server, and a target
outside them is simply not reachable; the path comes back with
`Path.canReach` false and the behaviour that asked gives up.

**Why does a villager find a bed across the village but not one behind a
wall?** Because 48 is `Villager`'s required path length, so distance is
rarely the limit — and because `AcquirePoi` runs a real path search before it
claims anything, so unreachable is invisible rather than merely far.

## Where to look

`PathNavigation` · `PathNavigation.createPath` · `PathNavigation.moveTo` ·
`PathNavigation.tick` · `PathNavigation.recomputePath` ·
`PathNavigation.canUpdatePath` · `PathNavigation.doStuckDetection` ·
`PathNavigation.updatePathfinderMaxVisitedNodes` ·
`PathNavigation.setRequiredPathLength` · `GroundPathNavigation` ·
`FlyingPathNavigation` · `WaterBoundPathNavigation` ·
`AmphibiousPathNavigation` · `WallClimberNavigation` ·
`PathNavigationRegion` · `PathFinder.findPath` · `BinaryHeap` · `Node` ·
`Target` · `Path.canReach` · `NodeEvaluator` · `WalkNodeEvaluator` ·
`SwimNodeEvaluator` · `FlyNodeEvaluator` · `AmphibiousNodeEvaluator` ·
`PathType` · `PathTypeCache` · `PathfindingContext` ·
`Mob.getPathfindingMalus` · `MoveControl.setWantedPosition` · `LookControl` ·
`JumpControl` · `BodyRotationControl` · `ServerLevel.sendBlockUpdated`

---

*Rules: names, never code · how the system works, not how the code reads ·
newest version only · every backticked name passes `tools/verify_names.py`.*
