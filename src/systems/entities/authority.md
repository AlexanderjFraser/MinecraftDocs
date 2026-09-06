# Authority: who is allowed to simulate

> Verified against **Minecraft 26.2** · Part VI · A zombie, a player and a boat each take one step, on the server and on the client, and only one side of each pair does any arithmetic.

A zombie walks towards you across a field. Both programs have a `Zombie`
object; both tick it every twentieth of a second; both call the same
`Entity.tick`. Only one of them works out where it goes. Standing next to
the zombie is another player, and their copy is the other way up — and the
boat you are sitting in is a third case again, authoritative on your machine
and nowhere else. Five predicates on `Entity` — one of them final — decide
all of it, and they invert the naive picture in **both** directions: **the client runs no physics
at all for the mob chasing you, while the server runs your player's physics
every tick and then overwrites the answer with a number your client sent.**

This is the single most error-prone idea in the entity part, and four later
parts rest on it — [movement and collision](movement-and-collision.md#who-is-allowed-to-run-this-at-all)
here, every page in Part VIII about a player, [what the client is
told](../networking/what-the-client-is-told.md#gate-1-who-is-allowed-to-see-it)
in Part IX, and in Part X both [the client
level](../client/the-client-level.md#where-the-two-levels-differ), for what
the client is allowed to simulate, and [prediction and
acknowledgement](../client/prediction-and-acks.md#two-state-machines-running-against-each-other),
for what it is allowed to *guess* while it waits to be told.
Sixteen pages link back to this one. It is stated in full once, here.

## The cast

| class | what it decides | thread |
|---|---|---|
| `Entity` | the five predicates, and every gate inside `Entity.move` that reads them | both main threads |
| `Player` | overrides four of the five, and is the reason the picture inverts | both |
| `Mob` | narrows `Entity.isEffectiveAi` with `Mob.isNoAi` | both, but only the server's copy acts on the answer |
| `LivingEntity` | `LivingEntity.aiStep`, which either simulates or coasts | both |
| `ClientPacketListener` | whether an inbound position packet moves the entity or only updates a codec | client main |
| `ServerGamePacketListenerImpl` | re-runs the client's numbers for the entities the client owns | server main |

## Five predicates, and the final one the other four hang off

`Entity.isLocalInstanceAuthoritative` is the root and it is **final** — no
class overrides it. It asks a different question on each side: on the client,
*am I locally client-authoritative?*; on the server, *am I **not**
client-authoritative?* Everything else hangs off those two.

```mermaid
flowchart TD
    Q["Entity.isLocalInstanceAuthoritative — final"]
    Q -- "on the client" --> LCA["Entity.isLocalClientAuthoritative"]
    Q -- "on the server" --> NCA["not Entity.isClientAuthoritative"]
    LCA --> LCAD["base: my controlling passenger's answer, or false"]
    LCA --> LCAP["Player: am I the local player?"]
    NCA --> CAD["base: my controlling passenger's answer, or false"]
    NCA --> CAP["Player: always true"]
    Q --> SIM["Entity.canSimulateMovement — defaults to it"]
    Q --> AI["Entity.isEffectiveAi — defaults to it"]
    SIM --> SIMP["Player overrides: not a client, or I am the local player"]
    AI --> AIP["Player overrides: the same"]
    AI --> AIM["Mob narrows: and not Mob.isNoAi"]
```

Two things in that picture are easy to miss. The base implementations of
both `Entity.isLocalClientAuthoritative` and `Entity.isClientAuthoritative`
**delegate to the controlling passenger** — an entity with nobody steering it
answers false to both, and an entity with a rider inherits the rider's answer.
That single line is the whole vehicle model. And `Player` overrides
`Entity.canSimulateMovement` and `Entity.isEffectiveAi` to something
*different* from the root — *not a client, or I am the local player* — which
is what lets the server simulate a player it is not authoritative for. The
member three later pages quote for that is `Player.isClientAuthoritative`, an
unconditional true.

Three classes narrow the AI predicate further and are worth naming because
they are the exceptions people trip over: `Mob.isEffectiveAi` adds
`Mob.isNoAi`, which is where the *NoAI* tag actually bites (what the guard
around it does and does not wrap is [goals and
brains](ai-goals-and-brains.md#where-both-of-them-sit-in-one-mob-tick)), and both
`ArmorStand.isEffectiveAi` and `Mannequin.isEffectiveAi` add a physics or
immovability flag of their own.

## Three cases, read on both sides

The columns are three shapes an entity can have; the rows are what each
predicate answers and what follows from it.

| | a tracked mob | a player | a boat you are riding |
|---|---|---|---|
| `Entity.isClientAuthoritative` | false | **true**, unconditionally | true, inherited from you |
| `Entity.isLocalInstanceAuthoritative`, **server** | **true** | false | false |
| `Entity.isLocalInstanceAuthoritative`, **client** | false | true only on *your own* player | **true**, on your machine only |
| `Entity.canSimulateMovement`, server | true | **true** — the override | false |
| `LivingEntity.travel` runs on the server | yes | yes, and the result is overwritten | n/a |
| `LivingEntity.travel` runs on the client | **never** | only for your own player | n/a — `AbstractBoat.floatBoat` and `AbstractBoat.controlBoat` do it instead |
| `Entity.checkFallDamage` inside `Entity.move` | server only | **your own client only** — the server reaches it by the packet path | client only |
| what the other side does instead | is interpolated, and stands still when the interpolation runs out | applies your movement packet | applies its own copy's packet |

The row that surprises people is the last-but-one. `Entity.move` gates
`Entity.checkFallDamage` on `Entity.isLocalInstanceAuthoritative`, which for
a player is true on your own client and **false on the server** — so the copy
that runs it every tick is the one that cannot hurt you.
`LivingEntity.checkFallDamage` needs a `ServerLevel` before it computes any
damage, so your client only accumulates the fall distance and lets
`Block.fallOn` fire. The server reaches fall damage from
`Entity.doCheckFallDamage` instead, driven by the movement packet, which is
[Part VIII's subject](../player/input-to-movement.md#the-trace-w-is-pressed).

### The mob: the client is not correcting, it is replaying

A client-side zombie fails `Entity.isLocalInstanceAuthoritative` because
nothing is riding it, so `Entity.canSimulateMovement` is false and
`LivingEntity.aiStep` never reaches `LivingEntity.travel`. What it does
instead is the branch `LivingEntity.aiStep` opens with: if an
`InterpolationHandler` is running, step it; **otherwise scale the stored
delta by 0.98** — and nothing then applies that delta, because the only thing
that would is `Entity.move`, which nothing in the mob's own tick reaches on
this side — and this is precisely the seam where the client's other answer
begins: what it may guess rather than simulate is [prediction and
acknowledgement](../client/prediction-and-acks.md#two-state-machines-running-against-each-other)'s.
(A piston or a shulker box can still drive a client-side mob into
`Entity.move`, with a vector of their own rather than its stored delta —
[movement and collision](movement-and-collision.md#building-the-delta) has the
five `MoverType` constants that say who is pushing.) There is no collision, no
gravity, no friction and no attempt at
prediction. It is not simulating and being corrected — it is replaying what
`ClientboundMoveEntityPacket` and `ClientboundEntityPositionSyncPacket` tell
it, and standing perfectly still when the interpolation runs out.

### The player: simulated twice, believed once

A `ServerPlayer` passes `Entity.canSimulateMovement` and
`Entity.isEffectiveAi` — both true on the server by `Player`'s override — so
the server's copy runs the whole of `LivingEntity.travel`. It also fails
`Entity.isLocalInstanceAuthoritative`, so none of the consequences that gate
on it fire. The predicates are why a copy that is not authoritative simulates
at all; what the server then does with the answer is [the two-phase
tick](../player/the-two-phase-tick.md#the-bracket-and-what-survives-it) —
the physics run in the connection phase, after every level has ticked, inside
a bracket that puts the player straight back where it found them, and the
authoritative position moves in the movement packet instead. The server's own
simulation is a sanity check whose position nobody uses.

One consequence reaches a block. `SweetBerryBushBlock.entityInside` needs to
know how far the entity moved this tick, and it asks
`Entity.isClientAuthoritative` to decide **how to find out**:
`Entity.getKnownMovement` for a player, whose movement the server did not
compute, and old-position-minus-current for everything else. Authority is not
only about physics — it is about which of two numbers is real.

### The boat: authoritative on exactly one machine

Sit in a boat and the base delegation makes it yours. On your client
`Entity.isLocalClientAuthoritative` walks to the controlling passenger, finds
you, and returns true, so your machine simulates the boat for real. On the
server the same delegation makes `Entity.isClientAuthoritative` true, so the
server's copy is *not* authoritative and does not simulate — it zeroes its
own delta outright. Every other client's copy does the same, and is moved
only by `AbstractBoat.interpolation`.

```mermaid
sequenceDiagram
    participant CL as ClientLevel
    participant LP as LocalPlayer
    participant AB as AbstractBoat
    participant Wire as the network
    participant SGPL as ServerGamePacketListenerImpl
    participant SL as ServerLevel
    participant CPL as ClientPacketListener

    CL->>AB: tickNonPassenger, and isLocalInstanceAuthoritative is true
    AB->>AB: floatBoat, then controlBoat, then move for real
    LP->>Wire: ServerboundMoveVehiclePacket.fromEntity, once per client tick
    Wire->>SGPL: handleMoveVehicle
    SGPL->>AB: move with MoverType.PLAYER and my distance, then absSnapTo
    SGPL->>AB: setOnGroundWithMovement then doCheckFallDamage
    Note over SGPL,SL: the server never simulated it, so this is where the boat gets its physics consequences
    SGPL-->>Wire: nothing, when the move is accepted
    SGPL->>Wire: ClientboundMoveVehiclePacket, only when it is rejected
    Wire->>CPL: handleMoveVehicle
    CPL->>AB: absSnapTo the server's position, then echo a ServerboundMoveVehiclePacket back
```

The inbound half of that is the sharpest demonstration of what the predicate
is for. `ClientboundMoveVehiclePacket` is not a routine update — the server
sends it only when it has *rejected* your movement, and the client applies it
only for a vehicle it is authoritative for, and then immediately echoes a
`ServerboundMoveVehiclePacket` back to confirm. Meanwhile the ordinary
per-entity position packets take the opposite branch:
`ClientPacketListener.handleEntityPositionSync` and
`ClientPacketListener.handleMoveEntity` both check
`Entity.isLocalInstanceAuthoritative` and, when it holds, **do not move the
entity** — `ClientPacketListener.handleMoveEntity` decodes the delta into the
entity's position codec and stops there, and
`ClientPacketListener.handleEntityPositionSync` records the absolute position
in the codec on either branch. The server's opinion about where your boat is
gets recorded and ignored.

## Where the gates actually sit

Authority is not one flag consulted once. It is read at eight places in
`Entity.move` and `LivingEntity.aiStep` alone — four of them reading
`Entity.isLocalInstanceAuthoritative` itself, three `Entity.canSimulateMovement`
and two `Entity.isEffectiveAi`, one place consulting a pair:

- the vertical collision flags and `Entity.setOnGroundWithMovement` run if
  the entity moved vertically **or** is locally authoritative — the
  horizontal flags are always updated;
- `Entity.checkFallDamage` runs only if it is locally authoritative;
- `Entity.restituteMovementAfterCollisions` — the bounce — runs on
  `Entity.canSimulateMovement`;
- the step sound and `GameEvent.STEP` run if this is not a client **or** the
  instance is locally authoritative;
- in `LivingEntity.aiStep`, the 0.98 decay of the stored delta runs
  precisely when `Entity.canSimulateMovement` is **false** — it is the
  not-authoritative branch, not a fallback inside the authoritative one;
- `Mob.serverAiStep` runs on `Entity.isEffectiveAi` **and** not client-side,
  and `LivingEntity.travel` on `Entity.canSimulateMovement` **and**
  `Entity.isEffectiveAi`;
- `Entity.applyEffectsFromBlocks` follows the travel fork, on the same
  not-a-client-or-authoritative test as the step sound.

The last one has a fork in front of it — the ridden branch, which [movement
and collision](movement-and-collision.md#building-the-delta) walks. What
belongs here is that `LivingEntity.travelRidden` carries a ninth reading of
its own: an `Entity.canSimulateMovement` test that zeroes the delta outright
when it fails.

## What the predicates explain

**Why does a mob rubber-band and my own player does not?** Neither one is
being corrected, and for opposite reasons. Your client does simulate your own
player — and a boat or a horse you are riding, and a dropped item, which
consult no predicate at all — but it never simulates a tracked mob, so there
is nothing about the mob for the server to disagree with. What you see on a
mob is the gap between position packets, walked by `InterpolationHandler`.

**Why does a boat feel responsive and a horse feel heavy?** Both are ridden,
and both are authoritative on your machine — but a horse is a `LivingEntity`
going through `LivingEntity.travelRidden`, which asks the mob for its own
speed and drag, while a boat runs its own physics directly. The authority
answer is the same; the layer above it is not.

**Does *NoAI* stop a mob moving?** Completely, and by more than the obvious
route. It stops `Mob.serverAiStep`, because `Mob.isEffectiveAi` is what
`LivingEntity.aiStep` gates that call on — and the same predicate is the
second half of the gate on `LivingEntity.travel`, so nothing reaches
`Entity.move` for that mob either. A *NoAI* mob does not even fall.

## Where to look

`Entity.isLocalInstanceAuthoritative` · `Entity.isLocalClientAuthoritative` ·
`Entity.isClientAuthoritative` · `Entity.canSimulateMovement` ·
`Entity.isEffectiveAi` · `Player.isLocalPlayer` · `Mob.isNoAi` ·
`LivingEntity.aiStep` · `LivingEntity.travel` · `LivingEntity.travelRidden` ·
`Entity.move` · `Entity.checkFallDamage` · `Entity.doCheckFallDamage` ·
`ServerGamePacketListenerImpl.handleMovePlayer` ·
`ServerGamePacketListenerImpl.handleMoveVehicle` ·
`ClientPacketListener.handleEntityPositionSync` ·
`ClientPacketListener.handleMoveEntity` ·
`ClientPacketListener.handleMoveVehicle` · `InterpolationHandler` ·
`SweetBerryBushBlock.entityInside` · `AbstractBoat.floatBoat` ·
`AbstractBoat.controlBoat`

---

*Rules: names, never code · how the system works, not how the code reads ·
newest version only · every backticked name passes `tools/verify_names.py`.*
