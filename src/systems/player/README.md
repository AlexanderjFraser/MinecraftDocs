# VIII · The player

> Verified against **Minecraft 26.2** · Part VIII · The one entity a human is steering: what it is made of, when it runs, and the four things it does that the rest of the world does differently.

Everything in Parts IV to VII happens to the world. This part is about the
one object in it that argues back. A player is an entity like any other —
same base class, same tick, same synched data — and then almost every rule
is bent for it: it is ticked twice instead of once, it is the only thing the
server simulates and then contradicts, its inventory reports seven slots it
does not store and aliases an eighth, and its melee combat has three
separate entry points of which the famous one is the least interesting. A player recognises the part
by the friction: the snap back after a laggy jump, the swing that does more
damage if you wait, the food bar that empties from sprinting and not from
walking, the effect timer that keeps counting while the connection is down.

## The shape of the part

Part VIII is a trunk and four branches. Two pages say what a player *is* and
when it runs; everything after them is one thing a player *does*, and they
are independent of each other — except the spear, which is the sword swing's
sequel and should not be watched before it. The inventory is on the trunk:
Part VII stops at the slot, and the container the slots sit in is this
part's.

```mermaid
flowchart TD
    PA["Player anatomy — what a player is made of"]
    TT["The two-phase tick — when it runs, and what is thrown away"]
    IM["Input to movement — walking, and being believed"]
    SS["The sword swing — one integer, and a number rebuilt"]
    SP["The spear — two attacks on one item, neither through Player.attack"]
    HE["Hunger and experience — two bars the server owns"]
    SE["Status effects — a list of things happening to you"]
    PA -- "eight classes, forty-three slots" --> TT
    TT -- "phase two is where the player acts" --> IM
    TT --> SS
    TT --> HE
    TT --> SE
    SS -- "and two other melee paths" --> SP
```

## Before you start

[Part VI](../entities/README.md) is the hard prerequisite, and two of its
pages in particular. [Entity
anatomy](../entities/entity-anatomy.md#the-tree-and-the-class-that-was-inserted-into-it),
because a player is a `LivingEntity` with three rungs added on the server
and four on the client, and this part never re-teaches the base; and
**[authority](../entities/authority.md#five-predicates-and-the-final-one-the-other-four-hang-off)**,
because every page here rests on it — a `Player` is client-authoritative on
*both* sides, which is why the server's own answer for your movement is
thrown away in favour of the number you sent it. If you watch one page from
another part first, watch that one. Three more of Part VI's are assumed
rather than re-taught: [attributes](../entities/attributes.md#forty-numbers-every-one-of-them-clamped),
because reach and every number a hit is worth is one; [synched entity
data](../entities/synched-entity-data.md#nineteen-slots-and-where-the-numbers-come-from);
and [movement and collision](../entities/movement-and-collision.md#the-tick),
the pipeline *input to movement* feeds and never repeats.

Then [the server tick](../server/server-tick.md#where-a-players-own-tick-actually-happens)
and [the level tick](../server/server-level-tick.md#every-entity-and-then-its-riders),
because half this part's timing claims are about which phase something ran in
— including the fact that a player's own physics run *after* every level has
finished. [Players and
sessions](../server/players-and-sessions.md#preparing-a-place-to-stand) owns
how a `ServerPlayer` comes to exist at all, and how the session it belongs to
ends. From [Part VII](../items/README.md), [using an
item](../items/using-an-item.md#the-two-paths-side-by-side), because the
spear's charge is an item you *use* and the meal in *hunger and experience*
is that same machinery from the eater's end.

## Watch in this order

1. [Player anatomy](player-anatomy.md) — the vocabulary page: eight
   classes, two game-mode objects, forty-three slots. There is an abstract
   class between `LivingEntity` and `Player` — `Avatar` — with no instance
   fields at all, and the main-hand *item* is not stored anywhere: it is the
   selected hotbar slot, aliased.
2. [The two-phase tick](the-two-phase-tick.md) — one player, one tick,
   twice. The connection records where you are, runs the whole physics
   pipeline, and then puts you back: the server keeps the velocity and
   throws the position away.
3. [Input to movement](input-to-movement.md) — W is pressed. A movement key
   held for less than a tick never happened, sending move packets faster makes the
   anti-cheat *stricter*, and the packet that reports your key presses
   cannot move you but can move a minecart.
4. [The sword swing](the-sword-swing.md) — left-click on a pig. The attack
   packet carries one integer and the server rebuilds the rest, applying the
   cooldown twice in two different shapes and multiplying the mace's fall
   bonus by the critical hit.
5. [The spear](the-spear.md) — the 26.2 combat change, and the part's most
   surprising lecture. Two components on one item: a stab whose packet has
   no target in it, and a charge whose damage comes from closing speed and
   which ignores the attack cooldown entirely.
6. [Hunger and experience](hunger-and-experience.md) — two bars the server
   owns outright. Walking costs exactly zero exhaustion, and not one of the
   named thresholds in the file the system is built on is read by anything —
   `FoodData` writes every number as a literal instead.
7. [Status effects](status-effects.md) — the part's closer, and the cleanest
   statement of the server/client split in the book: the client never runs a
   single one of an effect's hooks, only counts it down — and an infinite
   effect is never re-sent, because −1 never satisfies the re-send test.

Watched as lectures, one and two are the pair to keep together, and four and
five are the other pair. Six and seven can be watched in either order, or
skipped and returned to.

## Reference this part uses

[Attributes](../../reference/attributes.md), because reach, attack damage,
attack speed, sweeping ratio and knockback are all attributes — and attack
damage and knockback, the two that decide what a hit is worth, are not
synced to the client at all. [Packets](../../reference/packets.md) for the
movement, attack and health packets by name. [Data
components](../../reference/components.md) for the components that make an
item a weapon. [Damage outside
`LivingEntity`](../../reference/non-living-damage.md) for what a swing meets
when the target is not a mob. Then [game
rules](../../reference/gamerules.md), [level data and
rules](../../reference/level-data-and-rules.md) and [diagram
lanes](../../reference/lanes.md).

## Where the part stops

Part VIII is the smallest part of the book —
{{#include ../../generated/part-player.md}} in `world/entity/player`,
`world/food`, `ServerPlayer` and `client/player` — and almost the only part
where a size is not a warning: 97% of those lines are named somewhere in the
book, because a player is a small object surrounded by large ones. Nearly
everything a page here reaches for lives in another part, so the borders are
worth stating.

Upward, the part starts at `Avatar` rather than at `Entity`: what a player
*inherits* is [Part VI](../entities/README.md)'s, including the `Mannequin`
that shares the rung. Outward, it stops where the player stops being a
player. How a hit is resolved once it lands is [damage and
death](../entities/damage-and-death.md#the-number-the-arrow-decides) in Part
VI; what your client is *told* about everyone else is [what the client is
told](../networking/what-the-client-is-told.md#one-entitys-tick-and-the-gates-it-does-not-pass)
in Part IX; the ledger behind the block you already saw break is [prediction
and acknowledgement](../client/prediction-and-acks.md#the-four-writes) in
Part X; drawing a player, its skin and its model parts is Part XI's; and the
chat session a `ServerPlayer` carries — the public half of message signing, the
key itself never leaving the client — is [chat and
signing](../networking/chat-and-signing.md#what-the-signature-covers)'s. The two game-mode objects are
the sharpest of those borders: this part says what they hold, and what they
*do* with a block is Part V's two click pages.

Two things inside these packages are nobody's, and both are declined rather
than missed. `Hotbar` and `HotbarManager` are the nine *saved* creative
hotbars, which belong to the creative inventory screen this book does not
cover. And sleep is half-explained on purpose: [player
anatomy](player-anatomy.md#what-player-owns) names the fields and the
refusals a bed answers with, and the *everyone is asleep* half — the night
skip and the weather reset — is [the level
tick](../server/server-level-tick.md#sleeping-is-the-one-thing-a-freeze-cannot-stop)'s.
Nobody explains the walk between them: what one player lying down does over
the hundred ticks that follow.

---

*Rules: names, never code · how the system works, not how the code reads ·
newest version only · every backticked name passes `tools/verify_names.py`.*
