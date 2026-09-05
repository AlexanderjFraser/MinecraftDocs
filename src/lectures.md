# The lecture map

The video series is an *ordering* over the system pages, which are the
stable content. Each part's landing page lists its lectures in watching
order and says in a line what each one is; this page assembles the thirteen
orders and states the dependencies between them — where a later part is
assumed by an earlier one, and what to watch first because of it. It was
drafted in pass 3, one part per session, and is confirmed by the owner, who
reads every part with the decompile open, before anything is recorded.
Nothing in [Reference](reference/README.md) is watched, and nothing in the
[maps](maps/README.md) is: the maps are looked at once, the reference pages
are looked up, and a lecture links into them wherever a viewer would pause
the video to read a table.

Because the subject here is the order, nothing below describes a lecture.
What each one is about is said once, on its part's landing page; what is
here is what the order needs — the shape of each part, the lectures that
must be watched together or in a fixed sequence, and the three that are
worth taking out of turn: *environment attributes and timelines* before Part
III, *contexts and predicates* before Part XIII's advancements, and *the
client loop* before Part XI.

The one rule that holds everywhere: **each part assumes only the parts
before it**, and where that is not true the section says so and names the
page to watch early. [The dependencies between parts](#the-dependencies-between-parts),
at the end, draws the whole graph.

## I · Anatomy

1. [Anatomy](systems/anatomy/anatomy.md) — watched first, because every
   later diagram's lanes assume it.
2. [What this book skips](systems/anatomy/what-this-book-skips.md) — second
   and not last, for the reason the closing paragraph of this page gives.

## II · Foundations

Part II is a stack, watched bottom-up; each page is the machinery the one
above it assumes.

1. [Codecs, NBT and JSON](systems/foundations/codecs-nbt-json.md)
2. [Identifiers and registries](systems/foundations/identifiers-and-registries.md)
3. [The resource system](systems/foundations/resource-system.md)
4. [Tags](systems/foundations/tags.md)
5. [Data components](systems/foundations/data-components.md)
6. [Text components](systems/foundations/text-components.md)
7. [The data-driven type pattern](systems/foundations/data-driven-types.md)

[Math and primitives](reference/math-and-primitives.md) is not a lecture;
it is Reference, and the parts link into it.

## III · The server

Part III is a line into a loop and out again: the loop first, because it is
what the rest of the book lives inside, and the beginning and the end last,
because they are only interesting once you know what they start and stop.

1. [The server tick](systems/server/server-tick.md)
2. [The level tick](systems/server/server-level-tick.md) — watched
   immediately after the first, and never apart from it.
3. [Players and sessions](systems/server/players-and-sessions.md)
4. [Starting a server](systems/server/starting-a-server.md)
5. [How a server dies](systems/server/how-a-server-dies.md)

Watch [environment attributes and
timelines](systems/world/environment-attributes-and-timelines.md) (Part IV)
before *the level tick* if you want its opening to mean anything.
It costs nothing to take out of order — it depends on nothing but registries
and codecs — and Part III is the earliest of the six other parts that lean
on it.

## IV · The world

Part IV is a conveyor: five pages that hand a chunk along a line, and five
more about the world the line delivers. The conveyor is lectures 2 to 6 and
must be watched in that order — nothing later in the chain can be watched
first. Lecture 1 is off the line on purpose, and the last four can be
watched in any order once the vocabulary page is done.

1. [Environment attributes and
   timelines](systems/world/environment-attributes-and-timelines.md) —
   first, for the reason Part III already gave: it depends on nothing but
   registries and codecs, and nine pages in six other parts depend on it.
2. [Chunk anatomy](systems/world/chunk-anatomy.md) — the vocabulary page.
   Everything below assumes it, and so does Part V.
3. [Tickets and loading](systems/world/tickets-and-loading.md)
4. [The chunk generation
   pipeline](systems/world/chunk-generation-pipeline.md) — Part XII is the
   cargo on this conveyor and cannot be watched before it.
5. [Lighting](systems/world/lighting.md) — self-contained.
6. [Chunk storage](systems/world/chunk-storage.md)
7. [Scheduled ticks](systems/world/scheduled-ticks.md) — Part V's redstone
   lecture assumes this one, and so does the next.
8. [Fluids](systems/world/fluids.md)
9. [Game events and vibrations](systems/world/game-events-and-vibrations.md)
10. [Points of interest](systems/world/points-of-interest.md) — Part VI owns
    the brain; this owns the index it reads.

[Level data and rules](reference/level-data-and-rules.md) is not a lecture;
it is Reference, and this part and Part III both link into it.

## V · Blocks

Part V is a hub and six spokes, and the hub is watched first because the
other six all reach back into the same figure in it: what `Level.setBlock`
and `LevelChunk.setBlockState` do once the section has been written. Two of
the six are one lecture in two halves.

1. [Blocks and states](systems/blocks/blocks-and-states.md)
2. [Block interaction](systems/blocks/block-interaction.md)
3. [Block breaking](systems/blocks/block-breaking.md) — the same lecture's
   other half. Watch it immediately after, and never apart from it.
4. [Block entities](systems/blocks/block-entities.md) — self-contained.
5. [Signal and dust](systems/blocks/signal-and-dust.md) — assumes [scheduled
   ticks](systems/world/scheduled-ticks.md) only lightly.
6. [Pistons and block events](systems/blocks/pistons-and-block-events.md)
7. [Diodes and the observer](systems/blocks/diodes-and-observers.md) —
   assumes [scheduled ticks](systems/world/scheduled-ticks.md) properly: a
   repeater's delay is an entry in that queue.

Part V's two click lectures are the applications of [prediction and
acknowledgement](systems/client/prediction-and-acks.md) in Part X, and that
page's own scenario needs this part's vocabulary. The dependency is
circular and this book cuts it here: both click pages open with the same
statement of the contract, and the machinery waits for Part X.

## VI · Entities

Part VI is a ladder, and the second rung carries the rest of it. Nothing in
the part can be reordered without breaking something, and the one page most
often skipped — *authority* — is the one three later parts link back to.

1. [Entity anatomy](systems/entities/entity-anatomy.md) — the vocabulary the
   other eight lectures use.
2. [Authority](systems/entities/authority.md) — short, and Parts VIII, IX
   and X all assume it rather than re-deriving it.
3. [Entity lifecycle](systems/entities/entity-lifecycle.md) — assumes
   [tickets and loading](systems/world/tickets-and-loading.md) for what
   *entity-ticking* means.
4. [Synched entity data](systems/entities/synched-entity-data.md) — the
   first of the two channels that describe an entity.
5. [Attributes](systems/entities/attributes.md) — the second. Watch it after
   *synched entity data*, because the contrast between the two is the
   lesson.
6. [Movement and collision](systems/entities/movement-and-collision.md) —
   needs *authority* in front of it, and [blocks and
   states](systems/blocks/blocks-and-states.md) for what a collision shape
   is.
7. [AI: goals and brains](systems/entities/ai-goals-and-brains.md) — assumes
   [environment attributes and
   timelines](systems/world/environment-attributes-and-timelines.md) for the
   schedule and [points of
   interest](systems/world/points-of-interest.md) for the bed.
8. [Pathfinding](systems/entities/pathfinding.md) — the other half of the
   same lecture, and watchable on its own once *goals and brains* has said
   where the wanted position comes from.
9. [Damage and death](systems/entities/damage-and-death.md)

Part VI must precede Part VIII, which is the player half of nearly every
page here, and it should precede Parts IX and X, both of which lean on
*authority*. It assumes Part IV for what makes an entity tick at all and
Part V for what it collides with.

## VII · Items and inventories

Part VII is two tiers. The first three lectures are the vocabulary and are
watched in order; the last five are three engines that hand each other nothing,
so they can be watched in any order — though the two pairs below want to stay
together, and *contexts and predicates* leans on no stack at all and could come
first.

1. [Items and stacks](systems/items/items-and-stacks.md) — assumes [data
   components](systems/foundations/data-components.md) completely.
2. [Using an item](systems/items/using-an-item.md)
3. [Containers and menus](systems/items/containers-and-menus.md) — needs
   [the level tick](systems/server/server-level-tick.md) for when a
   broadcast happens.
4. [Recipes](systems/items/recipes.md)
5. [Enchantments](systems/items/enchantments.md)
6. [Enchanting](systems/items/enchanting.md) — watch it directly after
   *enchantments*.
7. [Contexts and predicates](systems/items/contexts-and-predicates.md) — the
   one page in this part that Part XIII needs.
8. [Loot tables](systems/items/loot-tables.md)

Part VII assumes Part II for components, codecs and the reload, Part III for
where in a tick a packet is drained and a broadcast lands, and Part V for how a
chest gets opened. It must precede Part VIII, which is the player's own inventory and
the swing that spends an item's durability. *Contexts and predicates* is a
prerequisite of Part XIII's `/execute if predicate` and of the advancement
system, and is the one lecture here a viewer coming for commands should
watch out of order.

## VIII · The player

Part VIII is a trunk and four branches: two lectures on what a player is and
when it runs, then five more on what a player does, in four independent
groups. Only one group has an internal order — the spear is the sword
swing's sequel.

1. [Player anatomy](systems/player/player-anatomy.md) — the vocabulary
   lecture.
2. [The two-phase tick](systems/player/the-two-phase-tick.md) — watch it
   immediately after *player anatomy*.
3. [Input to movement](systems/player/input-to-movement.md)
4. [The sword swing](systems/player/the-sword-swing.md)
5. [The spear](systems/player/the-spear.md)
6. [Hunger and experience](systems/player/hunger-and-experience.md)
7. [Status effects](systems/player/status-effects.md)

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

1. [The connection](systems/networking/the-connection.md)
2. [Packets and stream codecs](systems/networking/packets-and-stream-codecs.md)
   — the second half of the same lecture.
3. [Protocol phases](systems/networking/protocol-phases.md)
4. [What the client is told](systems/networking/what-the-client-is-told.md)
5. [Chat and signing](systems/networking/chat-and-signing.md)

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
   page every other page in the part leans on.
2. [The client level](systems/client/the-client-level.md)
3. [Prediction and acknowledgement](systems/client/prediction-and-acks.md)
4. [Input and keybinds](systems/client/input-and-keybinds.md)
5. [Options](systems/client/options.md)
6. [GUI and screens](systems/client/gui-and-screens.md)
7. [The GUI render tree](systems/client/the-gui-render-tree.md)
8. [Text and fonts](systems/client/text-and-fonts.md)
9. [The HUD](systems/client/hud.md)
10. [Sound: the engine](systems/client/sound-engine.md)
11. [What makes a sound happen](systems/client/what-makes-a-sound.md)
12. [Debugging the running game](systems/client/debugging-the-running-game.md)

Six to nine are the part's one internal pipeline — a screen records, the
tree sorts and batches, the text becomes glyphs — and are watched
consecutively. Two and three are the other pair: the ledger lives on
`ClientLevel` and is reached through four of its methods.

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

*A substrate under a pipeline.* Two lectures are what the renderer stands
on and have no trace through the world; the rest are one frame in the order
it happens. The part opens on the frame itself because it is the shortest
way to see the whole shape at once — and because a viewer who has watched
one frame end to end has a reason to care what a `GpuDevice` is.

1. [The frame](systems/rendering/the-frame.md)
2. [The window](systems/rendering/the-window.md)
3. [Blaze3D](systems/rendering/blaze3d.md)
4. [Visibility and the frame graph](systems/rendering/visibility-and-the-frame-graph.md)
5. [Section meshing](systems/rendering/section-meshing.md)
6. [Models and atlases](systems/rendering/models-and-atlases.md)
7. [Entity rendering](systems/rendering/entity-rendering.md)
8. [Block-entity rendering](systems/rendering/block-entity-rendering.md)
9. [Lightmap, fog and sky](systems/rendering/lightmap-fog-and-sky.md)
10. [Particles](systems/rendering/particles.md)
11. [Post-processing](systems/rendering/post-processing.md)

Four and five are a pair — two pages that were one, and still one journey
seen from its two ends — and so are seven and eight, the second written as
the differences from the first. One to three can also be watched one, three,
two.

Part XI assumes two pages of Part X: the [client
loop](systems/client/the-client-loop.md), which is what says when a frame
happens, and [the client level](systems/client/the-client-level.md), for
what the thing being drawn actually is. Lecture six assumes Part II's [resource
system](systems/foundations/resource-system.md); lecture nine assumes Part
IV's [environment attributes and
timelines](systems/world/environment-attributes-and-timelines.md), which
owns the system this part only consumes.

## XII · World generation

A substrate, a pipeline, and a wing — and the wing runs first while being
watched last. The ten lectures below run against the chunk status ladder
rather than along it: a structure is *decided* two statuses before the
biomes and terrain it will stand in exist, and writes its blocks four
statuses later, so keeping the three structure lectures together at the end
costs one forward reference and buys a whole arc in one place.

1. [Density functions](systems/worldgen/density-functions.md)
2. [Biomes](systems/worldgen/biomes.md)
3. [Terrain](systems/worldgen/terrain.md)
4. [Blending at the old-chunk border](systems/worldgen/blending.md)
5. [Features and placement](systems/worldgen/features-and-placement.md)
6. [Trees](systems/worldgen/trees.md)
7. [Structure placement](systems/worldgen/structure-placement.md)
8. [Jigsaw and templates](systems/worldgen/jigsaw-and-templates.md)
9. [Hand-built structures](systems/worldgen/hand-built-structures.md)
10. [Creating a world](systems/worldgen/creating-a-world.md)

Two comes before three: `ChunkPyramid` makes `ChunkStatus.BIOMES` a
requirement of both `ChunkStatus.NOISE` and `ChunkStatus.SURFACE`, and the
surface pass reads the biome. Four needs both, and reaches one status forward
into five and six's. Seven
comes before eight and nine, which are alternatives to each other rather
than a sequence. Ten is the object the other nine read, told last because
it is a tree of everything they explain.

Part XII assumes Part IV's [chunk generation
pipeline](systems/world/chunk-generation-pipeline.md), and hard: it is the
only page that says when any of this runs and what the twelve statuses are,
and eight of the ten lectures here name one. It also assumes Part IV's
[chunk anatomy](systems/world/chunk-anatomy.md) for what is being written
into and Part IV's [environment attributes and
timelines](systems/world/environment-attributes-and-timelines.md) for lecture
two, where `Biome` has been hollowed out into one layer of a modifier stack;
and three Part II lectures — codecs, registries and [the data-driven type
pattern](systems/foundations/data-driven-types.md), whose fifty-six instances
this part owns twenty-six of — because worldgen is the most thoroughly
data-driven system in the game.

## XIII · Commands and data packs

A stack of three floors, and the dependency runs strictly one way: *parse*,
then *execute*, then the four systems built on both. The last four are peers
rather than a sequence — watch them in any order, or only the ones you care
about — but neither of the first two floors is optional for any of them.

1. [Brigadier and commands](systems/commands/brigadier-and-commands.md)
2. [Permissions](systems/commands/permissions.md)
3. [Entity selectors](systems/commands/entity-selectors.md)
4. [The execution engine](systems/commands/the-execution-engine.md)
5. [Functions and macros](systems/commands/functions-and-macros.md)
6. [Advancements](systems/commands/advancements.md)
7. [Scores, teams and stored data](systems/commands/scoreboard-and-data.md)
8. [Dialogs](systems/commands/dialogs.md)
9. [Game tests](systems/commands/game-tests.md)

Two and four are the pair that most changes how a viewer reads everything
else, and two is the one an existing mod author most needs; three sits
between them because it needs the atom two defines and hands its fan-out to
four. Six, seven, eight and nine each assume one through five and nothing
else in this part.

Part XIII assumes Part III's [server tick](systems/server/server-tick.md)
twice over — command functions run near the top of `MinecraftServer.tickChildren`, before any
level ticks, and the connection phase that calls `ServerPlayer.doTick` runs
after the levels, which is what puts a periodic advancement trigger one tick
behind the packet that should have carried it. It assumes Part II's [codecs](systems/foundations/codecs-nbt-json.md)
and [the data-driven type pattern](systems/foundations/data-driven-types.md),
of which dialogs and game tests are the two clearest instances; Part IX's
[connection](systems/networking/the-connection.md) for the Netty/server
thread boundary the command packets cross two different ways; and, for
advancements alone, Part VII's
[contexts and predicates](systems/items/contexts-and-predicates.md), because
a trigger's conditions are loot conditions.

## The dependencies between parts

Every arrow below is a *before you start* entry on a landing page: the part
at the tail is one the part at the head assumes, and not optionally. The
two dependencies every part shares are drawn as boxes but not as edges,
because their arrows would reach almost every node — Part I's [anatomy](systems/anatomy/anatomy.md), for
the threads every diagram's lanes are on, and Part II's
[codecs](systems/foundations/codecs-nbt-json.md) and
[registries](systems/foundations/identifiers-and-registries.md), assumed
wherever something is written to disk, sent on the wire or looked up by
name. Read a solid arrow as *watch before*.

{{#include figures/parts-dependency.md}}

The graph is a line with two knots in it, and the sidebar order is a valid
walk through it: no solid arrow points at an earlier part. The two dashed
arrows are the places where it does not hold, and each is cut on purpose
rather than solved by reordering.

**Part III assumes two pages of Part IV.** [The level
tick](systems/server/server-level-tick.md) uses *entity-ticking* and
*block-ticking* range, which [tickets and
loading](systems/world/tickets-and-loading.md) owns, and its first step
throws away a cache belonging to [environment attributes and
timelines](systems/world/environment-attributes-and-timelines.md). The first
is cut by definition — the level tick defines both ranges before it uses
them — and the second by order: the environment page depends
on nothing but registries and codecs, so it is the first page of Part IV in
the sidebar, in that part's watch order and in the list above, and it is the
one lecture worth watching before its part.

**Part V and Part X assume each other.** The two click lectures in Part V
are the applications of [prediction and
acknowledgement](systems/client/prediction-and-acks.md), and that page's own
scenario is a block placed against a wall, which needs Part V's vocabulary.
The cut is at Part V: both click pages open with the same four-sentence
statement of the ledger's contract, which is all either needs, and the
machinery waits for Part X, so the whole of Parts V and VI is watched before
that one Part X lecture. Part VI hands something forward to a *different*
Part X page: [the client level](systems/client/the-client-level.md) opens by
saying it is not an authority either, which needs
[authority](systems/entities/authority.md) behind it.

Ten pages carry most of the graph — nine rows below, because the two server
ticks are one dependency in two lectures. The membership rule is
mechanical: **a page that two or more landing pages name under *before you
start***, less the three every part assumes, which are the boxes the figure
draws without edges. A viewer who has watched these ten can take the parts
they belong to in almost any order; a viewer who skips one of them will
find a later part's first surprise unexplained.

| the page | its part | the parts whose landing pages assume it |
|---|---|---|
| [The server tick](systems/server/server-tick.md) and [the level tick](systems/server/server-level-tick.md) | III | IV, V, VI, VII, VIII, IX, XIII — seven of the eight later parts that run on the Server thread, for *which phase* something ran in |
| [Environment attributes and timelines](systems/world/environment-attributes-and-timelines.md) | IV | III, VI, XI, XII — the clock, the schedule, and the colour of the sky |
| [Chunk anatomy](systems/world/chunk-anatomy.md) | IV | V, VI, XII — a block state's home, a ticking entity's chunk, and what terrain is written into |
| [Authority](systems/entities/authority.md) | VI | VIII, IX, X — the premise under every page about a player, and under *what the client is told* |
| [The resource system](systems/foundations/resource-system.md) | II | III, VII, XI — the staged load and its barrier: a server's own data at startup, where recipes and loot tables come from, and the reload the atlases are built by |
| [The connection](systems/networking/the-connection.md) | IX | X, XIII — the thread boundary every packet crosses |
| [Tickets and loading](systems/world/tickets-and-loading.md) | IV | III, VI — what *entity-ticking* means |
| [The data-driven type pattern](systems/foundations/data-driven-types.md) | II | XII, XIII — the *type* field in a data-pack file and the registry it dispatches on; these two parts own most of its instances |
| [Text components](systems/foundations/text-components.md) | II | IX, X — what a chat message and a screen's label are before anything draws them |

Three more pages are a single part's dependency, and each is named in that
part's *before you start* rather than here: [blocks and
states](systems/blocks/blocks-and-states.md) before Part VI, [contexts and
predicates](systems/items/contexts-and-predicates.md) before Part XIII's
advancements, and [the client loop](systems/client/the-client-loop.md)
before Part XI. The last two are the ones a viewer coming for that part
alone most often has to fetch from elsewhere in the book.

Watched straight through, the sidebar order still needs one departure from
itself, and it is now as small as it can be: *environment attributes and
timelines* is the first lecture of Part IV and wants watching before Part
III's second. A viewer coming for one part rather than the whole book takes
that part's *before you start* list as the order.

[What this book skips](systems/anatomy/what-this-book-skips.md) is the
second lecture and not the last: it is the only page that states the
series' boundary, and a boundary is drawn before the investment, not after.
Part XIII's game tests are the closing lecture because they are the game's
own answer to the question the whole book has been asking — how do you know
what it does — and because nothing later depends on them.
