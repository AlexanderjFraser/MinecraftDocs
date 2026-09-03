# Signal and dust

> Verified against **Minecraft 26.2** · Part V · A lever on the floor is flipped, and two redstone dust to the east of it go to 15 and 14.

You flip a lever, and the dust beside it turns bright. Flip it back and a long
line does not go dark all at once — it counts down, 14, 13, 12, visibly, one
value per wire. That staircase is not an animation and not a tick delay. It is
the shape of the algorithm: each wire recomputes its own strength from
scratch, writes it, and then **hand-issues seven `Level.updateNeighborsAt`
calls — its own position and all six neighbours — which is forty-two neighbour
updates for one wire that changed**, and the wire at the far end of the line
is reached once per intermediate value on the way down. The game ships a
second implementation of exactly this computation, behind a feature flag,
which walks the whole connected network in two ordered phases and does not
produce the staircase at all.

**Forty-two** — neighbour updates issued by one wire whose power changed
(`DefaultRedstoneWireEvaluator.updatePowerStrength`).

## The cast

| class | what it decides | thread |
|---|---|---|
| `SignalGetter` | every question about power: what a position emits, what reaches it, and the direction order the answers are gathered in | a `Level` interface, either side |
| `BlockBehaviour.BlockStateBase` | the three answers a state gives — is it a source, what is its weak signal per face, what is its strong signal | either side |
| `LeverBlock` | the trace's source: 15 in every direction, and 15 *strongly* into one block only | server — the client's copy writes nothing |
| `RedStoneWireBlock` | which sides a wire connects to, what it emits through them, and the mutable flag that stops it counting itself | server |
| `RedstoneWireEvaluator` | *minus one per block*: what the neighbouring wires are worth to this one | server |
| `DefaultRedstoneWireEvaluator` | one wire at a time, recursively, with the fan-out issued by hand | server |
| `ExperimentalRedstoneWireEvaluator` | the whole network at once, off in two phases and on in one, allocated fresh per call | server |
| `Orientation` | in the experimental mode only, where an update *came from*, so the fan-out can be ordered relative to it | server |

## What one neighbour update to a wire costs

Redstone has no scheduler and no graph. It is what happens when blocks answer
two questions about their neighbours — *how much signal do you give me* and
*did something near you change* — through the same `BlockBehaviour.neighborChanged`
fan-out every block update uses. This is the whole of the default
implementation, from one update arriving to the next batch leaving.

```mermaid
flowchart TB
    IN["RedStoneWireBlock.neighborChanged arrives on the server"]
    CLIENT{"is this a ClientLevel"}
    SURV{"RedStoneWireBlock.canSurvive"}
    DROP["dropResources and Level.removeBlock"]
    NOTHING["nothing at all. Level.updateNeighborsAt and Level.neighborChanged are empty on Level"]
    BLK["RedStoneWireBlock.getBlockSignal: set shouldSignal false, ask SignalGetter.getBestNeighborSignal, set it back"]
    WIRE["RedstoneWireEvaluator.getIncomingWireSignal: the best of the four side wires, the wire above a conducting neighbour, the wire below a non-conducting one, minus one"]
    TARGET["DefaultRedstoneWireEvaluator.calculateTargetStrength: block signal if it is 15, else the larger of the two"]
    SAME{"is the target the POWER already stored"}
    STOP["return. No write, no fan-out, and the cascade ends here"]
    WRITE["Level.setBlock with flag 2 alone. Clients are told, no neighbour updates come from the write itself, shape updates still run"]
    FAN["seven Level.updateNeighborsAt calls: this position and its six neighbours, collected in a hash set"]
    OUT["forty-two neighbour updates, queued in CollectingNeighborUpdater.addedThisLayer and run before the caller's remaining directions"]
    IN --> CLIENT
    CLIENT -- "yes" --> NOTHING
    CLIENT -- "no" --> SURV
    SURV -- "no" --> DROP
    SURV -- "yes" --> BLK
    BLK --> WIRE --> TARGET --> SAME
    SAME -- "yes" --> STOP
    SAME -- "no" --> WRITE --> FAN --> OUT
```

The two facts that make the staircase are both in that figure. The write uses
`Block.UPDATE_CLIENTS` **alone**, so the fan-out is not the one
`Level.setBlock` would have done — it is issued afterwards, by hand, over
seven positions rather than one. And the recursion terminates on *value*, not
on distance: a wire whose recomputed strength equals what it already holds
writes nothing and tells nobody. A line going dark therefore re-enters every
wire once per step of the descent, and each visit is the last one only when
the value has stopped moving.

## What a block answers when it is asked for power

Three questions, all on `BlockBehaviour.BlockStateBase`, all answered by the
block. `BlockBehaviour.BlockStateBase.isSignalSource` is whether the block
emits at all. `BlockBehaviour.BlockStateBase.getSignal` is the **weak** signal
it offers to a given face. `BlockBehaviour.BlockStateBase.getDirectSignal` is
the **strong** one, and the difference between them is entirely a matter of
who is allowed to pass it on. Conduction is
`BlockBehaviour.BlockStateBase.isRedstoneConductor`, from
`BlockBehaviour.Properties.isRedstoneConductor`, which defaults to *is this
state's collision shape a full block*.

`SignalGetter` is where the two meet, and the join is easy to get backwards.
`SignalGetter.getSignal` reads the block's own weak signal and then, **only
if that block is a redstone conductor**, takes the larger of it and
`SignalGetter.getDirectSignalTo` — the strongest signal being pushed into that
position from any of its six neighbours. It is a maximum, not a choice between
two modes: a powered conductor offers the greater of what it emits itself and
what is being forced into it. That single line is what "strongly powered"
means, and it is why a block with a lever on it powers the dust beside it
while a block merely *touched* by dust does not.

The lever shows both halves at once. `LeverBlock.ownSignal` is 15 in every
direction when powered — that is the weak signal, and it is what the dust next
to the lever reads. `LeverBlock.getDirectSignal` is 15 only into the one block
the lever is attached to. So the block behind a lever becomes a source in its
own right, and everything touching *that* block sees 15 too.

### Three direction orders, and only one of them is about reading

The corpus has three fixed direction arrays and they are not interchangeable.
Two decide who gets **told** something; the third decides what a block
**reads**, and it is the one this page uses.

| array | order | what it governs |
|---|---|---|
| `SignalGetter.DIRECTIONS` | down, up, north, south, west, east | what a block reads — `SignalGetter.getBestNeighborSignal`, `SignalGetter.getDirectSignalTo` and `SignalGetter.hasNeighborSignal` all walk it, and all stop early on a 15 |
| `NeighborUpdater.UPDATE_ORDER` | west, east, down, up, north, south | which neighbour is told first about a change, on the neighbour channel |
| `BlockBehaviour.UPDATE_SHAPE_ORDER` | west, east, north, south, down, up | which neighbour is asked first to re-fit, on the shape channel |

The early exit on 15 is not a micro-optimisation with no consequences: it
means a position saturated from one side never reads the others at all.
`SignalGetter.DIRECTIONS` is plain `Direction` order, which is the only reason
its first entry is *down*.

## Dust, and how far it reaches

`RedStoneWireBlock.POWER` is the number, 0 to 15. Four `RedstoneSide`
properties — one per horizontal — record how the wire is drawn and, more
importantly, which sides it will actually talk through. What a wire is worth
to its neighbours is `RedstoneWireEvaluator.getIncomingWireSignal`, and the
*minus one per block* everyone knows lives in its last line: it takes the best
of the wires it can see and subtracts one, floored at zero. The wires it can
see are the four beside it, plus the wire on top of a conducting neighbour
when nothing conducts above this position, plus the wire below a
non-conducting neighbour — which is the whole of "dust climbs a block and
falls down one".

Two asymmetries follow from `RedStoneWireBlock.getSignal` and are worth
stating plainly, because they are the two questions every redstone build
eventually asks. A wire returns **zero** when the direction asked about is
`Direction.DOWN` — so dust never powers the block above it. It returns its
full power without any connection test when the direction is `Direction.UP` —
so dust always powers the block below it. In every other direction it answers
only if its connection on the opposite side is made.

Connection itself is two rules and a completion pass.
`RedStoneWireBlock.shouldConnectTo` is the real one: another wire always, a
`Blocks.REPEATER` along its own axis, a `Blocks.OBSERVER` only from its facing
side, and otherwise any block that says it is a signal source.
`RedStoneWireBlock.getConnectingSide` adds the vertical cases — up over a
face-sturdy neighbour, down past a non-conducting one. And then
`RedStoneWireBlock.getConnectionState` runs a completion pass that produces
most of the confusion: **if a wire has no north or south connection, west and
east are set anyway**, and the same the other way round. That is why a lone
dust is drawn as a cross, and why a wire fed from the west appears to point
firmly into whatever is on its east — a piston, say — which satisfies neither
real rule. The piston is not a source and, by `Blocks.pistonProperties`, not a
conductor. It gets powered anyway, because the wire's east side is *SIDE* by
completion and `RedStoneWireBlock.getSignal` asks about the side, not about
the neighbour.

> **For a 1.21-era reader.** `BlockBehaviour.neighborChanged` now takes a
> nullable `Orientation` rather than a source `BlockPos`, and
> `BlockBehaviour.affectNeighborsAfterRemoval` — which replaced the old
> removal hook — does not take one at all.

`RedStoneWireBlock.shouldSignal` is the oddest thing on the page: a mutable
boolean on the block singleton, flipped false for the duration of
`RedStoneWireBlock.getBlockSignal` so that a wire does not count itself or its
neighbouring wires as sources while it works out its *block* power. It works
because the server thread is the only writer and never re-enters the method.

## The lever, two dust, and a powered piston

```mermaid
sequenceDiagram
    participant LevB as LeverBlock
    participant SL as ServerLevel
    participant CNU as CollectingNeighborUpdater
    participant RSWB as RedStoneWireBlock
    participant DRWE as DefaultRedstoneWireEvaluator
    participant PBB as PistonBaseBlock
    Note over LevB,PBB: all of this is one call stack, inside one packet handler, before the level ticks
    LevB->>SL: setBlock POWERED with flags 3, then updateNeighbours by hand
    SL->>CNU: two MultiNeighborUpdates, this position and the block behind the lever
    CNU->>RSWB: neighborChanged at the first dust
    RSWB->>DRWE: getBlockSignal sees the lever at 15, so the target is 15
    DRWE->>SL: setBlock POWER 15 with flag 2, then seven updateNeighborsAt
    CNU->>RSWB: neighborChanged at the second dust, depth-first, ahead of the lever's other directions
    RSWB->>DRWE: block signal 0, incoming wire signal 15 minus 1
    DRWE->>SL: setBlock POWER 14 with flag 2, then seven more
    CNU->>PBB: neighborChanged, and the piston reads the wire's east side at 14
    Note over CNU,PBB: the remaining dozens of updates run against blocks that do not care, and the count resets
```

The lever is the one place in this trace where the client does nothing at all.
`LeverBlock.useWithoutItem` writes no state on a `ClientLevel` — it spawns a
particle and returns — so unlike a door, a lever is not predicted, and the
client's dust changes colour only when the block updates arrive. The sound
follows the same split for a different reason: `LeverBlock.pull` is handed a
null player, so nobody is excluded and the clicker hears the server's
`ClientboundSoundPacket` like everyone else. Compare
[block interaction](block-interaction.md), where the door passes the clicker
as *except* and they hear their own prediction instead.

Two details in the diagram are worth naming. The lever's `Level.setBlock`
uses flags 3, so `Block.UPDATE_NEIGHBORS` has already fanned out once before
`LeverBlock.updateNeighbours` fans out again, at its own position and at the
block it hangs on. And the ordering of the seven positions a wire updates is
not fixed by anything: they come out of a hash set. The depth-first drain of
`CollectingNeighborUpdater` is [block interaction](block-interaction.md)'s
subject, and it is what puts the second dust's whole cascade ahead of the
lever's remaining directions.

Placing and breaking a wire take a wider path again:
`RedStoneWireBlock.onPlace` and
`RedStoneWireBlock.affectNeighborsAfterRemoval` both call
`RedStoneWireBlock.updateNeighborsOfNeighboringWires`, which walks the four
horizontals and then the diagonals — reaching over a conducting neighbour and
under a non-conducting one — and calls
`RedStoneWireBlock.checkCornerChangeAt` on each. That is another seven
`Level.updateNeighborsAt` per wire found. Which write does what is
[blocks and states](blocks-and-states.md#the-two-update-channels).

## The second implementation

`FeatureFlags.REDSTONE_EXPERIMENTS` is a built-in data pack, and
`RedStoneWireBlock.useExperimentalEvaluator` asks the level for it on **every
call** — `RedStoneWireBlock.evaluator` is always the default one, and an
`ExperimentalRedstoneWireEvaluator` is a fresh object per update, because it
carries working state. What changes is not speed but semantics.

`ExperimentalRedstoneWireEvaluator.calculateCurrentChanges` computes the whole
connected network before writing anything. Phase one drains
`ExperimentalRedstoneWireEvaluator.wiresToTurnOff`: a wire whose recomputed
power is lower than its stored value goes to **zero** in the working map
rather than to its new value, and is re-queued into the turn-on deque if it
has block power of its own. Phase two drains
`ExperimentalRedstoneWireEvaluator.wiresToTurnOn`, raising each to its true
value. Both phases spread through
`ExperimentalRedstoneWireEvaluator.propagateChangeToNeighbors` and
`ExperimentalRedstoneWireEvaluator.enqueueNeighborWire`, and every wire is
recorded in `ExperimentalRedstoneWireEvaluator.updatedWires`, an
insertion-ordered map of position to a packed orientation and power. Only then
are the states written — with `Block.UPDATE_CLIENTS` plus
`Block.UPDATE_SKIP_SHAPE_UPDATE_ON_WIRE`, which
`NeighborUpdater.executeShapeUpdate` honours by skipping any shape update
whose **target** is dust, whatever the source.

The fan-out is the other half of the difference.
`ExperimentalRedstoneWireEvaluator.causeNeighborUpdates` issues one
`Level.neighborChanged` per *connected* side per changed wire, in
`Orientation.getDirections` order — an order derived from where the update
came from rather than from a fixed array — and, where that side is a redstone
conductor, five more at that conductor's own sides. That is how the
experimental evaluator carries strong power without the seven-position
scattergun. And `RedStoneWireBlock.neighborChanged` ignores wire-sourced
updates entirely in this mode, which is what closes the recursion; the default
evaluator does not, which is what opens it.

## Questions players ask

**Why does a long line of dust flicker through every value when it turns
off?** Because each wire recomputes independently and tells its neighbours
only when its own number moved, so the far end is reached once for each value
the near end passes through on the way down. The experimental evaluator exists
to make that one ordered pass instead.

**Why does dust point into a block that cannot be powered?** Because the
drawing rule and the powering rule are different rules.
`RedStoneWireBlock.getConnectionState` fills in the missing half of a line
whenever the perpendicular axis is empty, and
`RedStoneWireBlock.getSignal` then answers on the strength of that filled-in
side. Whether the neighbour does anything with the signal is the neighbour's
business.

**Why does dust power the block underneath it but not the one above?**
`RedStoneWireBlock.getSignal` returns zero for `Direction.DOWN` and returns
full power for `Direction.UP` without checking any connection. Those are two
lines in one method, and every "torch under the dust" contraption rests on
them.

**Does a redstone torch really burn out after a fixed number of flickers?**
Yes, and the count is a literal rather than the constant beside it.
`RedstoneTorchBlock.RECENT_TOGGLES` is a weak map from level to a list of
toggles, pruned at the top of `RedstoneTorchBlock.tick` of anything older than
60 ticks, and `RedstoneTorchBlock.isToggledTooFrequently` burns the torch out
on the **eighth** surviving entry for that position.
`RedstoneTorchBlock.MAX_RECENT_TOGGLES` and
`RedstoneTorchBlock.RECENT_TOGGLE_TIMER` hold 8 and 60, and the method uses
neither.

## Where to look

`SignalGetter.getSignal` · `SignalGetter.getDirectSignalTo` ·
`SignalGetter.getBestNeighborSignal` · `SignalGetter.getControlInputSignal` ·
`SignalGetter.DIRECTIONS` · `BlockBehaviour.BlockStateBase.isRedstoneConductor` ·
`LeverBlock.pull` · `LeverBlock.updateNeighbours` ·
`RedStoneWireBlock.neighborChanged` · `RedStoneWireBlock.getBlockSignal` ·
`RedStoneWireBlock.getSignal` · `RedStoneWireBlock.getConnectionState` ·
`RedStoneWireBlock.getConnectingSide` · `RedStoneWireBlock.shouldConnectTo` ·
`RedStoneWireBlock.updateNeighborsOfNeighboringWires` ·
`RedstoneWireEvaluator.getIncomingWireSignal` ·
`DefaultRedstoneWireEvaluator.updatePowerStrength` ·
`ExperimentalRedstoneWireEvaluator.calculateCurrentChanges` ·
`ExperimentalRedstoneWireEvaluator.causeNeighborUpdates` ·
`NeighborUpdater.executeShapeUpdate` · `RedstoneTorchBlock.isToggledTooFrequently`

---

*Rules: names, never code · how the system works, not how the code reads ·
newest version only · every backticked name passes `tools/verify_names.py`.*
