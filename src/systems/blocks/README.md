# V · Blocks

> Verified against **Minecraft 26.2** · Part V · Everything that happens at the moment one block state replaces another: the click that asks for it, the write that performs it, and the four kinds of block that answer back.

Part IV built the container. This part is about what is *in* it, and it has
one moment at its centre: a position in a chunk section stops holding one
block state and starts holding another. Every page here is about choosing
that state, about the write itself, about a block that answers a write near
it, or — once — about the state a position cannot hold at all. A player
recognises the part by how it *feels* — the block that appears under the
crosshair before the server has heard about it, the door whose top half
swings with the bottom, the redstone lamp that does not light until the
server says so. The first of those is a prediction and Part X
owns it. The other two come from one distinction, and it is this part's:
**there are two entirely different ways a block hears that its neighbour
changed, and the client runs only one of them.**

## The shape of the part

Part V is a hub and six spokes. The hub is `blocks-and-states`, and what the
spokes reach back into it for is not the state table — it is the tail of a
write, drawn there once as a flowchart and linked to from everywhere else.

```mermaid
flowchart TD
    BS["Blocks and states — the table, and what a write actually does"]
    BI["Block interaction — the right click"]
    BB["Block breaking — the left click"]
    BE["Block entities — when a state is not enough"]
    SD["Signal and dust — reading power, and the cascade"]
    PE["Pistons and block events — a change that waits for a phase"]
    DO["Diodes and the observer — a change that books a turn"]
    BS -- "the shape channel, which the client runs too" --> BI
    BS -- "what a flags-3 write does after the section is written" --> BB
    BS -- "where a block entity is created, kept, replaced, removed" --> BE
    BS -- "the neighbour channel, which is the server's alone" --> SD
    BS -- "the flag word, and which bits the placeholders leave out" --> PE
    BS -- "a flag-2 write, and the onPlace that runs inside it anyway" --> DO
    BI -- "one lecture in two halves, one prediction ledger" --> BB
    SD -- "what powers a piston, and how the wire connects to it" --> PE
    SD -- "what a diode reads, and what reads a diode" --> DO
    BE -- "the one int redstone keeps outside a block state" --> DO
    BE -- "the placeholder's entity carries a whole state" --> PE
```

## Before you start

[Chunk anatomy](../world/chunk-anatomy.md), because the first half of every
write in this part is a section write with four heightmaps and a light check
behind it, and [the level tick](../server/server-level-tick.md), because half
of this part's surprises are really claims about which phase of a tick
something ran in — with [the server tick](../server/server-tick.md) behind
it, for the two claims this part makes about what happens *outside* the level
tick: that a packet handler runs before the levels do, and that a connection
is flushed after they have. Two more Part IV pages are load-bearing here
rather than merely adjacent: [scheduled
ticks](../world/scheduled-ticks.md) is how a block gets a turn *later*, which
is the whole of the diode lecture, and [fluids](../world/fluids.md) owns the
`FluidState` that shares a `StateHolder` with every block state, and the
waterlogging this part keeps writing around.

One dependency runs the other way. [Prediction and
acknowledgement](../client/prediction-and-acks.md) is Part X, and the two
click lectures here are its two applications — but its own scenario is a
block placed against a wall, which needs this part's vocabulary. So watch
Part V first: both click pages open with the same four-sentence statement of
the contract, which is all either lecture needs, and the machinery keeps
until Part X.

## Watch in this order

1. [Blocks and states](blocks-and-states.md) — a right-click on stone puts one
   of oak stairs' eighty states into the world. Every state the game will ever
   have was built before the world was, and the world stores an index into
   that table. The second half — what a write does after the section has been
   written — is the figure the other six lectures point back at.
2. [Block interaction](block-interaction.md) — the right click, in full: a
   door opened by hand. It fires no neighbour update at all, and the top half
   follows anyway.
3. [Block breaking](block-breaking.md) — the same lecture's other half: two
   clocks that agree without exchanging a packet. Let go too early and the
   block comes back, then vanishes again, and nothing short of the block
   itself going away stops it.
4. [Block entities](block-entities.md) — a furnace smelts while nobody is
   looking. It tells nobody anything: the fire is a block state, the arrow is
   four ints from a menu, and both are a tick late by construction.
5. [Signal and dust](signal-and-dust.md) — a lever, two dust, and the
   cascade. A line turning off is visited once for every intermediate value it
   passes through, none of which is ever sent to anybody, and the game ships a
   second implementation behind a flag that does not do it at all.
6. [Pistons and block events](pistons-and-block-events.md) — the part's
   deferral with no delay in it: the work waits for one named phase of the
   level tick rather than for a number of ticks, and usually gets it in the
   same tick. Also the one place the client is handed a re-simulation instead
   of a result: no block update is ever sent for the moving blocks.
7. [Diodes and the observer](diodes-and-observers.md) — the part's closer.
   Three blocks that read their neighbours three different ways, and the one
   whose entire job is noticing change turns out not to be listening on the
   channel that carries it.

## Reference this part uses

[Block update flags](../../reference/block-update-flags.md) — the ten bits of
`Level.setBlock`'s flag word and what reads each. [Registries](../../reference/registries.md) — `Registries.BLOCK` and
`Registries.BLOCK_ENTITY_TYPE` are two of its rows.
[Packets](../../reference/packets.md) — every block update, block event and
acknowledgement in one table. [Data
components](../../reference/components.md) — `DataComponents.TOOL`, which
decides how fast a stack mines and whether the block drops. [Game
rules](../../reference/gamerules.md). [Math and
primitives](../../reference/math-and-primitives.md) — `BlockPos`,
`Direction` and the packings every page here assumes. [Diagram
lanes](../../reference/lanes.md).

---

*Rules: names, never code · how the system works, not how the code reads ·
newest version only · every backticked name passes `tools/verify_names.py`.*
