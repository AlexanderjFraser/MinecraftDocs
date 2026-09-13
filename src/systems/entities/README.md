# VI · Entities

> Verified against **Minecraft 26.2** · Part VI · Everything in the world that is not a block: what one is, who is allowed to move it, how it is described to the other side, and how it stops.

A zombie glides where your own movement is crisp. A sheared sheep changes on
every screen at once. A mob you named never despawns, a hit that lands during
the red flash usually does nothing, and Strength II raises your damage without
a single packet leaving the server. Those are five different systems and one
question: **which of the two programs is allowed to decide this, and how does
the other one find out?** Part VI is that question asked about everything in
the world that is not in the grid — the zombie, the arrow, the boat, the
dropped pickaxe, the invisible marker a data pack left as a bookmark. All of
them are an `Entity`, a base class deliberately thin *on behaviour*: it gives
them a box, a numbered array for describing themselves to clients, one
collision resolver and one abstract method for being hurt, and almost nothing
else. So the answer to the question is never in one place. It is five
mechanisms that each decide it separately, and the part's claim is that
**every surprise on this list is one of those five answering a question you
thought a different one had already settled.**

## The shape of the part

Part VI is a ladder, drawn here from the bottom rung up. Each page needs the
ones below it and nothing above them, and the second rung — *authority* — is
the one everything else leans on, including Parts VIII, IX and X, which link
back to it rather than re-deriving it.

```mermaid
flowchart BT
    A["Entity anatomy — what an entity is"]
    B["Authority — who is allowed to simulate it"]
    C["Entity lifecycle — how it enters a world and leaves one"]
    D["Synched entity data — the channel that describes it"]
    E["Attributes — the named numbers it carries"]
    F["Movement and collision — what it does"]
    G["Goals and brains — why it does it"]
    H["Pathfinding — how a decision becomes a direction"]
    I["Damage and death — how it stops"]
    A -- "one type, one factory, one live object" --> B
    B -- "and one side of each pair does the arithmetic" --> C
    C -- "now it is in a world, findable and ticking" --> D
    D -- "one of the six channels that describe it; here is another" --> E
    E -- "gravity, step height, speed: the physics knobs are attributes" --> F
    F -- "something has to decide where to walk" --> G
    G -- "a decision is only a position until something walks there" --> H
    H -- "and everything above can be ended by one abstract method" --> I
```

Two of the eight steps up the ladder are pairings rather than sequels.
*Synched entity data* and *attributes* are two channels doing the same job
differently, and the contrast is the lesson, so the second wants the first
fresh in mind. *Pathfinding* is the other half of *goals and brains* and
watchable on its own once that page has said where a wanted position comes
from.

There is also one arrow that runs the other way, out of the part rather than
up the ladder, and it is Part X's dependency rather than this part's: [the
client level](../client/the-client-level.md) opens by saying it is *not* an
authority either, which only lands once
[authority](authority.md#five-predicates-and-the-final-one-the-other-four-hang-off)
has said what one is. So this part is watched first, and nothing here waits on
Part X.

## Before you start

[The level tick](../server/server-level-tick.md#the-broadcast-which-is-why-entities-are-a-tick-behind),
because half this part's surprises are claims about *which phase* something
ran in — the entity phase runs *after* the phase that broadcasts entity
changes, which is why an attribute change waits for the next tick the entity's
update interval allows, while a sheep sheared out of [the packet
queue](../server/server-tick.md#every-packet-since-last-time-in-one-drain),
before the tick proper, does not. [Tickets and
loading](../world/tickets-and-loading.md#the-four-statuses), because whether an
entity ticks at all is a property of the chunk it is standing in — for
everything except a player, which is exempt — and [chunk
anatomy](../world/chunk-anatomy.md#the-six-heightmaps) for the heightmaps that
decide where a mob may spawn. [Points of
interest](../world/points-of-interest.md#a-ticket-is-a-claim-nothing-enforces),
because a villager's whole day is claims on them and [goals and
brains](ai-goals-and-brains.md) draws `PoiManager` as a lane rather than
explaining it. [Blocks and
states](../blocks/blocks-and-states.md#four-decisions-four-lookups) for the
shapes that entities collide with. Part IV's *scheduled ticks* is the one page
of the world part you can skip before this one: entities keep no appointment
book.

One more Part IV page, for one lecture: [environment attributes and
timelines](../world/environment-attributes-and-timelines.md#the-four-timelines)
before [goals and brains](ai-goals-and-brains.md). A villager's timetable is a
data-pack `Timeline` looked up at a position, and this part asks that system a
question rather than teaching it.

## Watch in this order

1. [Entity anatomy](entity-anatomy.md) — one `EntityType` from the registry,
   through a factory, to a live object the level ticks. The registry's
   default is a pig, and that default reaches the network and never reaches
   your save file.
2. [Authority](authority.md) — a zombie, a player and a boat each take one
   step on both sides. The client runs no physics at all for the mob chasing
   you, and the server runs your own player's physics every tick and then
   throws the answer away.
3. [Entity lifecycle](entity-lifecycle.md) — a zombie appears in the dark,
   is ticked for a while, and is either forgotten or written to disk. The
   spawner rolls one height per category per chunk per tick, so caves and the
   open field compete for the same slice.
4. [Synched entity data](synched-entity-data.md) — a sheep is sheared and
   every screen in range agrees within the tick. The slot the wool lives in
   is written nowhere in `Sheep`: it is 18 because eighteen slots were handed
   out above it, and the ids stop at 254 because 255 means stop.
5. [Attributes](attributes.md) — Strength II lands, and no packet is sent at
   all. Eight of the forty attributes never reach the client, and attack
   damage is one of them.
6. [Movement and collision](movement-and-collision.md) — one tick of a
   falling zombie. The mover answers *what did I walk through* afterwards, by
   replaying the tick's movement, which is why fire and water touched in one
   step always end in the extinguish.
7. [AI: goals and brains](ai-goals-and-brains.md) — a villager's day, and the
   same machinery under a zombie that has none of it. The timetable is not on
   the villager: it goes to bed because it asked the world what time it is
   where it is standing.
8. [Pathfinding](pathfinding.md) — the other half of the same lecture. Giving
   up is machinery: the node being walked towards carries a timeout, and the
   mob you watch walk into a fence and then wander off is running a scheduled
   surrender.
9. [Damage and death](damage-and-death.md) — the part's closer, and it
   assumes nothing above it. An arrow, a dozen owners of one number, and one
   abstract method. A hit that lands inside the red flash usually does nothing
   at all, and when it is stronger than the last, only its excess lands —
   silently.

## Where the part stops

This is the largest part of the book —
{{#include ../../generated/part-entities.md}} in `world/entity` (less
`world/entity/player`), `network/syncher`, `world/level/pathfinder`,
`world/damagesource` and `world/effect` — and
{{#include ../../generated/coverage-entities.md}}. Most of that is one class
per species, and a species is the same nine pages instantiated: `Panda` is
1,121 lines of `Mob` with a sitting animation, and the 103 behaviour classes
and 61 goal classes are one shape each, drawn once on [goals and
brains](ai-goals-and-brains.md#what-holds-the-state).

Four mechanisms there are more than a species and are explained nowhere — the
minecart's two movement models, the ender dragon's sixteen flight phases, a
raid, and villager gossip — and a second edition should take them. The part
also stops one rung short of `Avatar`: everything player-shaped is Part VIII,
drawing an entity is Part XI, and the prediction ledger is [Part
X](../client/prediction-and-acks.md#the-four-writes). `world/effect` is the one
package above whose lecture is elsewhere, because the split an effect
demonstrates is the player's: [status effects](../player/status-effects.md).

## Reference this part uses

Five were written for this part.
[Attributes](../../reference/attributes.md) — all forty, with defaults,
ranges and the syncable flag, generated from the registrations.
[Entity data serializers](../../reference/entity-data-serializers.md) — all
43, in wire-id order, which is registration order.
[Entity spawn reasons](../../reference/spawn-reasons.md) — all nineteen, with
the classes that behave differently for each; eight are labels nothing tests.
[Structure spawn overrides](../../reference/structure-spawn-overrides.md) —
which six structures replace a biome's spawn list, and what they put there
instead. [Damage outside `LivingEntity`](../../reference/non-living-damage.md) — what
each of the twenty-one non-living classes does with a `DamageSource`, on
either side.

Then the shelf the whole book shares:
[packets](../../reference/packets.md),
[registries](../../reference/registries.md),
[game rules](../../reference/gamerules.md) — eleven of which this part's pages
read — [math and primitives](../../reference/math-and-primitives.md) for
`AABB` and `VoxelShape`, [the glossary](../../reference/glossary.md),
[threads](../../reference/threads.md) and [diagram
lanes](../../reference/lanes.md).

---

*Rules: names, never code · how the system works, not how the code reads ·
newest version only · every backticked name passes `tools/verify_names.py`.*
