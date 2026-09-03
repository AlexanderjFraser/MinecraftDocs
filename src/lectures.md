# The lecture map

The video series is an *ordering* over the system pages, which are the
stable content. Each part's landing page lists its lectures in watching
order; this page assembles them and states the dependencies between parts
— where a later part is assumed by an earlier one, and what to watch first
because of it. It is drafted in pass 3, one part per session, and confirmed
by the owner in pass 6 after reading every part with the decompile open.
Until a part's section below is filled, its sidebar order is its watching
order.

The one rule that holds everywhere: **each part assumes only the parts
before it**, and where that is not true the section says so and names the
page to watch early.

## I · Anatomy

1. [Anatomy](systems/anatomy/anatomy.md) — four threads, two loops, one
   wire. Watched first, because every later diagram's lanes assume it.
2. [What this book skips](systems/anatomy/what-this-book-skips.md) — the edge
   of the map, drawn on the treemap of the jar, before investing in thirteen
   parts.

## II · Foundations

Part II is a stack, watched bottom-up; each page is the machinery the one
above it assumes.

1. [Codecs, NBT and JSON](systems/foundations/codecs-nbt-json.md) — one
   `ItemStack` four ways: a chunk file, a packet, a checksum, the text of a
   `/give`. How anything becomes data.
2. [Identifiers and registries](systems/foundations/identifiers-and-registries.md)
   — how anything gets a name and a number, before the game exists and
   again when a world opens; the freeze rule, stated.
3. [The resource system](systems/foundations/resource-system.md) — where
   data comes from and when: F3+T as a pipeline, `/reload` as its coda.
4. [Tags](systems/foundations/tags.md) — data reaching into code; the
   freeze rule paid off.
5. [Data components](systems/foundations/data-components.md) — data on an
   item: prototype, patch, and when the prototype is built.
6. [Text components](systems/foundations/text-components.md) — text as
   data: a death message that is worded on the client.
7. [The data-driven type pattern](systems/foundations/data-driven-types.md)
   — the closer: every *type* field in a data pack is a lookup in a
   registry data packs cannot extend.

[Math and primitives](reference/math-and-primitives.md) is not a lecture;
it is Reference, and the parts link into it.

## III · The server

Part III is a line into a loop and out again: the loop first, because it is
what the rest of the book lives inside, and the beginning and the end last,
because they are only interesting once you know what they start and stop.

1. [The server tick](systems/server/server-tick.md) — one 50 ms lap of the
   Server thread. The most load-bearing lecture in the book after
   *Anatomy*: Parts IV to VIII all assume it, and it is the first place a
   viewer sees a named thread do a full lap.
2. [The level tick](systems/server/server-level-tick.md) — one step of that
   lap, which is the entire world changing. Watched immediately after, and
   never apart from it.
3. [Players and sessions](systems/server/players-and-sessions.md) — a join,
   then death, a dimension and a disconnect compared. The second half
   answers the question people actually ask about a server.
4. [Starting a server](systems/server/starting-a-server.md) — the cold
   open, told fourth: *java -jar server.jar* to the word *Done*.
5. [How a server dies](systems/server/how-a-server-dies.md) — the part's
   closer, and the strongest single lecture in it: three endings, and only
   two of them save your world.

Watch [environment attributes and
timelines](systems/world/environment-attributes-and-timelines.md) (Part IV)
before *the level tick* if you want its first statement to mean anything;
it is the page with the most dependants in the book and Part III is the
earliest of them.

## IV · The world

Part IV is a conveyor: five pages that hand a chunk along a line, and five
more about the world the line delivers. The first five must be watched in
order — nothing later in the chain can be watched first — and the rest can
be watched in any order once the vocabulary page is done.

1. [Environment attributes and
   timelines](systems/world/environment-attributes-and-timelines.md) —
   what the place and the hour decide, resolved through four layers on the
   server and the same four plus two kinds of smoothing on the client. It
   is listed first here for the reason Part III already gave: it depends on
   nothing but registries and codecs, and six pages across four parts
   depend on it.
2. [Chunk anatomy](systems/world/chunk-anatomy.md) — the vocabulary page:
   sections, palettes, bit storage, heightmaps, and the four shapes a
   chunk takes. Everything below assumes it, and so does Part V.
3. [Tickets and loading](systems/world/tickets-and-loading.md) — a player
   takes one step east. Two graphs over one ticket store, and what each of
   the four `FullChunkStatus` values buys.
4. [The chunk generation
   pipeline](systems/world/chunk-generation-pipeline.md) — *EMPTY* to
   *FULL* in twelve steps, and the pyramid of neighbour requirements that
   turns one request into 529. Part XII is the cargo on this conveyor and
   cannot be watched before it.
5. [Lighting](systems/world/lighting.md) — a torch, a flood on a worker,
   and a copy-on-write publish. Self-contained, and the only part of the
   pipeline with an executor of its own.
6. [Chunk storage](systems/world/chunk-storage.md) — the walk back west:
   snapshot, encode, write, on three threads, and the sector dance in the
   region file.
7. [Scheduled ticks](systems/world/scheduled-ticks.md) — how anything
   happens later. Part V's redstone lecture assumes this one, and so does
   the next.
8. [Fluids](systems/world/fluids.md) — the bucket. The scheduler's biggest
   customer, and the best worked example of a block that keeps booking its
   own future.
9. [Game events and vibrations](systems/world/game-events-and-vibrations.md)
   — a footstep, a filter cascade and a sculk sensor.
10. [Points of interest](systems/world/points-of-interest.md) — a villager
    and a bed. Part VI owns the brain; this owns the index it reads.

[Level data and rules](reference/level-data-and-rules.md) is not a lecture;
it is Reference, and this part and Part III both link into it.


## V · Blocks

Part V is a hub and six spokes, and the hub is watched first because the
other six all reach back into the same figure in it: what `Level.setBlock`
and `LevelChunk.setBlockState` do once the section has been written. Two of
the six are one lecture in two halves.

1. [Blocks and states](systems/blocks/blocks-and-states.md) — the state
   table, built before any world exists, and the write. The most linked-to
   figure in the part is in its second half.
2. [Block interaction](systems/blocks/block-interaction.md) — the right
   click: a door opened by hand, and no neighbour update anywhere.
3. [Block breaking](systems/blocks/block-breaking.md) — the same lecture's
   other half: two clocks, no packets between them, and the block that comes
   back and vanishes again. Watch it immediately after, and never apart
   from it.
4. [Block entities](systems/blocks/block-entities.md) — a furnace that tells
   nobody anything. Self-contained, and the part's most watchable lecture on
   its own.
5. [Signal and dust](systems/blocks/signal-and-dust.md) — a lever, two dust,
   forty-two neighbour updates per wire, and a second implementation behind
   a feature flag. Assumes [scheduled
   ticks](systems/world/scheduled-ticks.md) only lightly.
6. [Pistons and block events](systems/blocks/pistons-and-block-events.md) —
   the part's one deferral mechanism, and the one place the client is handed
   a re-simulation instead of a result.
7. [Diodes and the observer](systems/blocks/diodes-and-observers.md) — the
   closer. Assumes [scheduled ticks](systems/world/scheduled-ticks.md)
   properly: a repeater's delay is an entry in that queue.

Part V's two click lectures are the applications of [prediction and
acknowledgement](systems/client/prediction-and-acks.md) in Part X, and that
page's own scenario needs this part's vocabulary. The dependency is
circular and this book cuts it here: both click pages open with the same
statement of the contract, and the machinery waits for Part X.

## VI · Entities

Part VI is a ladder, and the second rung carries the rest of it. Nothing in
the part can be reordered without breaking something, and the one page most
often skipped — *authority* — is the one four later parts link back to.

1. [Entity anatomy](systems/entities/entity-anatomy.md) — one `EntityType`
   from the registry, through a factory, to a live object the level ticks.
   The vocabulary the other eight lectures use.
2. [Authority](systems/entities/authority.md) — a zombie, a player and a
   boat each take one step, on both sides. Short, and the highest
   consequence-per-minute lecture in the part: Parts VIII, IX and X all
   assume it rather than re-deriving it.
3. [Entity lifecycle](systems/entities/entity-lifecycle.md) — a mob
   appears, is ticked, and is either forgotten or written to disk. Assumes
   [tickets and loading](systems/world/tickets-and-loading.md) for what
   *entity-ticking* means.
4. [Synched entity data](systems/entities/synched-entity-data.md) — a sheep
   is sheared and every screen agrees within the tick. The first of the two
   channels that describe an entity, and the one every later part reaches
   for.
5. [Attributes](systems/entities/attributes.md) — the second channel, and
   the one that sends nothing. Watch it after *synched entity data*, because
   the contrast between the two is the lesson.
6. [Movement and collision](systems/entities/movement-and-collision.md) —
   one tick of a falling zombie. Needs *authority* in front of it and
   [blocks and states](systems/blocks/blocks-and-states.md) for what a
   collision shape is.
7. [AI: goals and brains](systems/entities/ai-goals-and-brains.md) — a
   villager's day, and a zombie with none of it. Assumes [environment
   attributes and timelines](systems/world/environment-attributes-and-timelines.md)
   for the schedule and [points of
   interest](systems/world/points-of-interest.md) for the bed.
8. [Pathfinding](systems/entities/pathfinding.md) — the other half of the
   same lecture, and watchable on its own once *goals and brains* has said
   where the wanted position comes from.
9. [Damage and death](systems/entities/damage-and-death.md) — the closer.
   An arrow, a dozen multiplications, and the twenty-one classes that
   implement being hurt some other way entirely.

Part VI must precede Part VIII, which is the player half of nearly every
page here, and it should precede Parts IX and X, both of which lean on
*authority*. It assumes Part IV for what makes an entity tick at all and
Part V for what it collides with.

## VII · Items and inventories

Part VII is two tiers. The first three lectures are the vocabulary and are
watched in order; the last five are three engines that assume all three and
nothing of each other, so they can be watched in any order — though the two
pairs below want to stay together.

1. [Items and stacks](systems/items/items-and-stacks.md) — an `Item` holds
   almost no data and an `ItemStack` holds a diff, against a prototype that
   does not exist until the first data-pack load. Assumes [data
   components](systems/foundations/data-components.md) completely.
2. [Using an item](systems/items/using-an-item.md) — a meal and a bow as one
   machine read two ways. The client's countdown never stops at zero.
3. [Containers and menus](systems/items/containers-and-menus.md) — one
   shift-click, one packet up, nothing down. Needs [the level
   tick](systems/server/server-level-tick.md) for when a broadcast happens.
4. [Recipes](systems/items/recipes.md) — no recipe ever crosses the wire,
   and the client still holds the contents of every one it has unlocked.
5. [Enchantments](systems/items/enchantments.md) — a named modifier that
   holds no code, and the hook table that is its real interface.
6. [Enchanting](systems/items/enchanting.md) — the five ways one lands on
   an item. Watch it directly after *enchantments*.
7. [Contexts and predicates](systems/items/contexts-and-predicates.md) —
   the engine that answers *is this true here*, and the one page in this
   part that Part XIII needs.
8. [Loot tables](systems/items/loot-tables.md) — the worked example, and
   the part's closer.

Part VII assumes Part II for components, codecs and the reload, Part III for
which tick phase a broadcast lands in, and Part V for how a chest gets
opened. It must precede Part VIII, which is the player's own inventory and
the swing that spends an item's durability. *Contexts and predicates* is a
prerequisite of Part XIII's `/execute if predicate` and of the advancement
system, and is the one lecture here a viewer coming for commands should
watch out of order.

## VIII · The player

Part VIII is a trunk and four branches: two lectures on what a player is and
when it runs, then four independent ones on what a player does. Only the
last pair has an internal order — the spear is the sword swing's sequel.

1. [Player anatomy](systems/player/player-anatomy.md) — the vocabulary
   lecture: five classes, two game-mode objects, forty-three slots. `Avatar`
   holds no state at all, and the main hand is not stored anywhere.
2. [The two-phase tick](systems/player/the-two-phase-tick.md) — one player,
   ticked twice by two callers. The connection records the position, runs
   the whole physics pipeline and puts the player back; the velocity is what
   it wanted. Watch it immediately after *player anatomy*.
3. [Input to movement](systems/player/input-to-movement.md) — W is pressed,
   and the server decides whether to believe it. A key shorter than a tick
   never happened, and sending move packets faster makes the check stricter.
4. [The sword swing](systems/player/the-sword-swing.md) — one integer on the
   wire and a damage figure rebuilt from nothing. Two curves over one
   cooldown, and the mace's fall bonus multiplied by the crit.
5. [The spear](systems/player/the-spear.md) — the 26.2 combat change, and
   the strongest single lecture in the part. Two components on one item, a
   packet with no target in it, and a charge that ignores the cooldown.
6. [Hunger and experience](systems/player/hunger-and-experience.md) — two
   bars the server owns outright, meeting at the enchanting table. Walking
   costs exactly zero exhaustion.
7. [Status effects](systems/player/status-effects.md) — the closer. The
   client never runs an effect; it counts down and spawns particles, and an
   infinite effect is never re-sent at all.

Part VIII assumes Part VI above everything — [authority](systems/entities/authority.md)
in particular, which is where the whole part's premise is stated — and Part
III for the tick phases the two-phase tick lives between. It assumes Part VII
for the inventory and for [using an item](systems/items/using-an-item.md),
which is the machinery the spear's charge runs on. Nothing later in the book
is needed to watch it, but Part IX and Part X both come back to it.

## IX · Networking

Part IX is one wire and three passengers. The first two lectures are one
lecture in two halves and should be watched together; the last three are
unrelated systems that ride the wire, and each has a different shape.

1. [The connection](systems/networking/the-connection.md) — bytes land on a
   socket and, some milliseconds later, a method runs on the game thread.
   The lecture with the round-trip diagram: two threads, two codec layers,
   one hop, and the packets that never make the hop at all.
2. [Packets and stream codecs](systems/networking/packets-and-stream-codecs.md)
   — the second half of the same lecture. What the thing crossing the wire
   actually is, once you have watched it travel: a record, a codec built
   from its fields, and an id that only means something inside one phase.
3. [Protocol phases](systems/networking/protocol-phases.md) — a login, from
   clicking a server in the list to standing in the world. Four languages
   over one socket, and a `ServerPlayer` constructed *after* the client has
   acknowledged that the phase named for preparing it is over.
4. [What the client is told](systems/networking/what-the-client-is-told.md)
   — a creeper walks into view. A policy, not a trace: every gate a change
   passes before it becomes a packet, and the things the server chooses
   never to say at all.
5. [Chat and signing](systems/networking/chat-and-signing.md) — the closer,
   and the only lecture in the book with an adversary in the diagram. What
   each check catches, and whether it kills the message, the chain, or the
   connection.

Part IX assumes Part III for the tick phases its traffic is timed against,
and Part I's [anatomy](systems/anatomy/anatomy.md) for the two loops — the
client drains packets once per *frame*, and that single fact explains most
of what looks like network jitter. It assumes Part II for codecs and for
`Component`, and Part VI's [authority](systems/entities/authority.md) for
the premise under lecture four. It is a prerequisite of Part X, which is the
same wire watched from the receiving end.

## X · The client

Part X is a hub and its spokes, and the spokes are cadences rather than
stages. Nothing here hands off to anything; every page after the first
answers "when in the client's one loop does *this* happen". Watch the hub
first and then take the rest in any order that suits — except the two pairs
noted below.

1. [The client loop](systems/client/the-client-loop.md) — the hub, and the
   shortest page in the part. One turn of `Minecraft.run`: how much
   simulated time a frame owes, and what happens to the time it cannot
   afford. A frame that earns fifteen ticks runs ten and loses five.
2. [The client level](systems/client/the-client-level.md) — the same `Level`
   class the server runs, with its authority removed. A comparison of what
   the client really simulates against what it only pretends to, and the
   client's tick lists confidently answering *no*.
3. [Prediction and acknowledgement](systems/client/prediction-and-acks.md) —
   the block that appears and then disappears. The receipt is for a number,
   not a verdict, and it is sent for the actions the server refused.
4. [Input and keybinds](systems/client/input-and-keybinds.md) — holding
   sneak. Five chances for a press to be swallowed, and a key that stays
   down while you are not touching it.
5. [Options](systems/client/options.md) — the render-distance slider.
   Saving *is* the event system, and a cycle button broadcasts your client
   information on every click.
6. [GUI and screens](systems/client/gui-and-screens.md) — what a screen is,
   grounded in pressing E: a screen the server is never told about, over a
   menu with no `MenuType`.
7. [The GUI render tree](systems/client/the-gui-render-tree.md) — nothing in
   the 2D UI draws anything. Layering is inferred from bounding boxes, which
   is what makes the batching possible.
8. [Text and fonts](systems/client/text-and-fonts.md) — six stages from a
   `Component` to a quad, one of which uploads a texture while pretending to
   measure.
9. [The HUD](systems/client/hud.md) — the other thing that records into that
   tree. Two hidden-gated blocks, and the one element between them that F1
   does not hide.
10. [Sound: the engine](systems/client/sound-engine.md) — five threads and
    one OpenAL device. A sound always starts at least one hop after the
    packet, even on a cache hit.
11. [What makes a sound happen](systems/client/what-makes-a-sound.md) — three
    doors, and only one of them names the sound. Your own sounds never round
    trip.
12. [Debugging the running game](systems/client/debugging-the-running-game.md)
    — the closer, and the part's one *pattern* lecture: sixteen instances of
    one subscription mechanism, all shipped and none of them on.

Six to nine are the part's one internal pipeline — a screen records, the
tree sorts and batches, the text becomes glyphs — and are watched
consecutively. Two and three are the other pair: the ledger lives on
`ClientLevel` and is reached through three of its methods.

Part X assumes [Part IX](systems/networking/README.md), which is the same
wire watched from the sending end, and Part I's
[anatomy](systems/anatomy/anatomy.md) for the two loops. It assumes Part
VI's [authority](systems/entities/authority.md) as the premise under
lectures two and three, and **Part V before lecture three** — Part V's
landing page rules that its two click lectures come first, because they are
the ledger's two applications. Lecture eight assumes Part II's [text
components](systems/foundations/text-components.md). Lecture one is a
prerequisite of Part XI, which begins where it ends, at the acquired
surface.

## XI · Rendering

*Filled by session L.*

## XII · World generation

*Filled by session M.*

## XIII · Commands and data packs

*Filled by session N.*

## The dependencies between parts

*Assembled by session P from the landing pages' "before you start" lists,
with the figure of which part assumes which.* Two are already known from
the pass-2 notebook: Part IX assumes the server tick's phase order (Part
III) and the client's frame/tick interleave (Part X); and
[environment attributes and timelines](systems/world/environment-attributes-and-timelines.md)
in Part IV is assumed by a Part III page and by four later parts, so it is
watched early.
