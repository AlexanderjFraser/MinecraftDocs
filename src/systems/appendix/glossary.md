# Glossary

> Verified against **Minecraft 26.2** · Part XIII · No trace — one sentence
> per term the rest of the corpus uses, and a link to the page that owns it.

## Responsibility

Every page in this corpus assumes the vocabulary of the pages before it.
That is deliberate — a lecture that redefines "chunk holder" every time it
appears is unwatchable — but it means a reader who arrives in the middle
has no way back. This page is the way back: the terms, alphabetically, one
sentence each, each pointing at the page where the term is actually
explained.

A sentence here is a *reminder*, not a definition to rely on. If the
sentence is all you needed, good; if it is not, the link is the point of
the entry. Where a term is a class name, the class name is the entry —
this corpus uses Mojang's names for concepts as well as for types, and
inventing a second vocabulary to sit beside them would only double the
work.

## A

**Activity** — a named mode a `Brain` can be in (core, idle, work, rest);
the brain runs only the behaviours listed for the current one, with
`ActivityData` holding each one's priority table. → [AI](../entities/ai-goals-and-brains.md)

**Advancement** — a data-pack-defined goal: criteria, a requirements
expression over them, an optional display entry and a reward. → [advancements](../commands/advancements.md)

**Aquifer** — the worldgen component that decides whether the non-stone
part of a column is air, water or lava; carvers ask it rather than placing
air themselves. → [the worldgen pipeline](../worldgen/worldgen-pipeline.md)

**Argument type** — a Brigadier `ArgumentType` that parses one token of a
command; vanilla's live in `net/minecraft/commands/arguments` and are
described to the client through an `ArgumentTypeInfo`. → [Brigadier and commands](../commands/brigadier-and-commands.md)

**Atlas** — one large texture stitched at load time out of many sprite
files, so a chunk section can be drawn with a single bound texture. → [models and atlases](../client/models-and-atlases.md)

**Attribute** — a named, ranged, modifiable number on a `LivingEntity`;
modifiers are keyed by `Identifier`, and eight attributes are not
client-syncable at all. → [attributes](../entities/attributes.md)

**Avatar** — the class between `LivingEntity` and `Player`; a `Mannequin`
is an `Avatar` that is not a player, and `AvatarRenderer` draws both. → [player anatomy](../player/player-anatomy.md)

## B

**Beardifier** — the density-function term that bends terrain around a
structure; terrain adaptation writes no blocks, it changes the noise. → [structures](../worldgen/structures.md)

**Behaviour** — one unit of brain AI, gated on memories and running over
several ticks. → [AI](../entities/ai-goals-and-brains.md)

**Biome** — a named bundle of generation settings, mob spawns, block tints
and environment attributes, attached to a 4×4×4 volume of the world. → [biomes](../worldgen/biomes.md)

**BiomeSource** — the object that answers "which biome is at this quart
position", either by a climate search or from a fixed table. → [biomes](../worldgen/biomes.md)

**Blaze3D** — Mojang's GPU abstraction, with OpenGL and Vulkan backends
behind one `GpuDevice`. → [Blaze3D](../client/blaze3d.md)

**Block** — the singleton describing a kind of block: its behaviour, its
property set and its state table. One `Block`, many `BlockState`s. → [blocks and states](../blocks/blocks-and-states.md)

**Block entity** — the per-position mutable state a block cannot fit into
its state (a chest's contents, a furnace's progress), stored on the chunk. → [block entities](../blocks/block-entities.md)

**Block event** — a deferred, one-tick-late message from a block to itself
(a piston push, a note block, a chest lid), queued on `ServerLevel` and
mirrored to the client as a packet. → [redstone](../blocks/redstone.md)

**BlockState** — one immutable combination of a block's properties,
interned in `Block.BLOCK_STATE_REGISTRY` and compared by identity. → [blocks and states](../blocks/blocks-and-states.md)

**Brain** — the memory-and-behaviour AI used by villagers, piglins and
axolotls, as opposed to the older goal system. → [AI](../entities/ai-goals-and-brains.md)

**Brigadier** — Mojang's command-parsing library: a tree of literal and
argument nodes with per-node requirements, shared by client and server. → [Brigadier and commands](../commands/brigadier-and-commands.md)

## C

**Camera** — the client's eye: position, rotation and the partial tick it
was computed at, extracted into a render state once per frame. → [the frame](../client/the-frame.md)

**Carver** — a worldgen pass that removes terrain to make caves and
ravines, asking the `Aquifer` what to leave behind. → [the worldgen pipeline](../worldgen/worldgen-pipeline.md)

**Chunk** — a 16-by-16 column of the world's full height: sections,
heightmaps, block entities, tick queues and a status. → [chunk anatomy](../world/chunk-anatomy.md)

**ChunkHolder** — the server's per-chunk record of who wants it, what
status it has reached, and what changed in it this tick. → [tickets and loading](../world/tickets-and-loading.md)

**ChunkMap** — the server's chunk table: holders, the ticket-driven level
graphs, entity tracking, and the region-file storage underneath. → [tickets and loading](../world/tickets-and-loading.md)

**ChunkStatus** — one rung of the generation ladder; a chunk advances one
status at a time and each status declares the neighbour radius it needs. → [the chunk generation pipeline](../world/chunk-generation-pipeline.md)

**Climate** — the noise sample (temperature, humidity, continentalness,
erosion, depth, weirdness) a biome is chosen by. → [biomes](../worldgen/biomes.md)

**Codec** — a DataFixerUpper object that both encodes and decodes one type
against any `DynamicOps`; the corpus's universal serialisation vocabulary. → [codecs, NBT and JSON](../foundations/codecs-nbt-json.md)

**Component** — two different things the corpus keeps apart: a *data
component* on an item stack, and a `Component` of chat text. → [data components](../foundations/data-components.md), [chat and signing](../networking/chat-and-signing.md)

**Container** — the interface a thing with item slots implements (a chest,
a hopper, an inventory), as distinct from the *menu* a player interacts
with it through. → [containers and menus](../items/containers-and-menus.md)

**Criterion** — one condition inside an advancement, backed by a
`CriterionTrigger` the server fires when the relevant thing happens. → [advancements](../commands/advancements.md)

## D

**Data component** — a typed, codec-backed value on an item stack, keyed by
a `DataComponentType`; what NBT item tags became. → [data components](../foundations/data-components.md)

**Data pack** — a pack of JSON and function files supplying the server's
data-driven content; the server half of the resource system. → [the resource system](../foundations/resource-system.md)

**DeltaTracker** — the client's clock: how much of a tick has elapsed, and
the source of every partial tick in the frame. → [the frame](../client/the-frame.md)

**Density function** — a node in the JSON-defined graph that turns a
position into a number; the graph in the registry is never the graph that
actually runs. → [density functions](../worldgen/density-functions.md)

**Dialog** — a data-pack-defined form the server can put on a player's
screen, whose submitted values come back as a packet. → [dialogs and tests](../commands/dialogs-and-tests.md)

**Dimension** — one `ServerLevel` and its `DimensionType`: a height range,
a set of environment attributes and its own chunk storage. → [level data and rules](../world/level-data-and-rules.md)

## E

**Entity** — anything in the world that is not a block: a position, a
bounding box, synched data and a tick method. → [entity anatomy](../entities/entity-anatomy.md)

**EntityType** — the registry entry for a kind of entity: its factory,
size, tracking range and spawn rules. → [entity anatomy](../entities/entity-anatomy.md)

**EnvironmentAttribute** — a per-dimension, per-biome, keyframed value (fog
colour, sky colour, music, ambient sound) resolved through a probe over a
stack of layers; nearly every visual constant is one. → [lightmap, fog and sky](../client/lightmap-fog-and-sky.md)

**Extract** — the first half of the client's frame: walk the game state on
the game thread and record an immutable render state, so that the drawing
half touches no game object. → [the frame](../client/the-frame.md)

## F

**Feature** — the algorithm half of decoration: what to build, with no
opinion about where. → [features and placement](../worldgen/features-and-placement.md)

**Frame graph** — the client's per-frame declaration of render passes and
the targets each reads and writes, resolved before anything is drawn. → [level rendering](../client/level-rendering.md)

**Function** — a `.mcfunction` file: a list of commands loaded as a
`CommandFunction`, optionally with macro lines. → [execution and functions](../commands/execution-and-functions.md)

## G

**Game event** — a broadcast fact about something that just happened at a
position (a block placed, a door opened) that sculk sensors and mobs
listen for. → [game events and points of interest](../world/game-events-and-poi.md)

**Game rule** — one typed, per-world switch or number in `GameRules`, saved
with the world and sometimes sent to the client. → [level data and rules](../world/level-data-and-rules.md)

**Game test** — a data-driven test instance: a structure, an environment
and a check the server runs and reports on. → [dialogs and tests](../commands/dialogs-and-tests.md)

**Goal** — one unit of the older mob AI: a priority, a start condition, and
the set of controls it claims while running. → [AI](../entities/ai-goals-and-brains.md)

## H

**Heightmap** — a per-chunk 2D array of the topmost block matching a
predicate; four are kept on a live chunk and worldgen placement reads them. → [chunk anatomy](../world/chunk-anatomy.md)

**Holder** — a reference to a registry entry that can exist before the
entry is bound: `Holder.Reference` for a registered value, `Holder.Direct`
for an inline one. → [identifiers and registries](../foundations/identifiers-and-registries.md)

**HolderSet** — a set of holders: either a tag (`HolderSet.Named`) or a
literal list. → [tags](../foundations/tags.md)

**HUD** — the in-world overlay (hotbar, hearts, chat, boss bars), which in
26.2 is the class `Hud` — `Gui` now means the screen manager. → [the HUD](../client/hud.md)

## I

**Identifier** — a namespace and a path; the id of everything. Known as
*ResourceLocation* before 26.2. → [identifiers and registries](../foundations/identifiers-and-registries.md)

**Ingredient** — a recipe's "any of these items" test, which can never be
empty. → [recipes](../items/recipes.md)

**Integrated server** — the `MinecraftServer` a singleplayer client runs in
its own thread; it still talks to the client only in packets. → [anatomy](../anatomy/anatomy.md)

**InteractionResult** — the answer a block or item gives to a click: was
the input consumed, should the arm swing, did the held item change. → [block interaction](../blocks/block-interaction.md)

**Item** — the singleton for a kind of item; a stack is an item, a count
and a component patch. → [items and stacks](../items/items-and-stacks.md)

## J

**Jigsaw** — the structure-assembly system that grows a village out of
template pieces by matching connector blocks. → [structures](../worldgen/structures.md)

## L

**Level** — a world: `ServerLevel` on the server, `ClientLevel` on the
client, sharing an abstract `Level` and remarkably little else. → [the level tick](../server/server-level-tick.md)

**Lightmap** — the small texture the client samples to turn a block-light /
sky-light pair into a colour; drawn on the GPU once per tick. → [lightmap, fog and sky](../client/lightmap-fog-and-sky.md)

**Loot table** — the data-driven roll that turns an event (a block broken,
a chest opened, a mob killed) into item stacks. → [loot tables](../items/loot-tables.md)

## M

**Macro** — a function line beginning with a substitution; the function is
compiled once and instantiated per call with the caller's arguments. → [execution and functions](../commands/execution-and-functions.md)

**Memory** — one typed, optionally expiring value in a `Brain`; behaviours
are gated on which memories are present. → [AI](../entities/ai-goals-and-brains.md)

**Menu** — the server-authoritative object behind an open container screen:
slots, a synchroniser and a state id. → [containers and menus](../items/containers-and-menus.md)

## N

**NBT** — Minecraft's binary tag format; in 26.2 a sealed `Tag` hierarchy
of records, read and written through `NbtIo` and reached by codecs through
`NbtOps`. → [codecs, NBT and JSON](../foundations/codecs-nbt-json.md)

**Neighbour update** — the server-only notification a block sends its six
neighbours after a change; distinct from a *shape update*, which runs on
both sides. → [block interaction](../blocks/block-interaction.md)

**NoiseChunk** — the per-chunk machine that fills the noise lattice and
installs the caches the density-function graph asked for. → [density functions](../worldgen/density-functions.md)

## P

**Packet** — a record with a `PacketType` and a `StreamCodec`, valid in one
protocol phase and one direction. → [packets and stream codecs](../networking/packets-and-stream-codecs.md)

**PalettedContainer** — the bit-packed storage a chunk section keeps its
block states and biomes in, with a palette that grows as the section gets
more varied. → [chunk anatomy](../world/chunk-anatomy.md)

**Partial tick** — the fraction of a tick elapsed at the moment a frame is
drawn, used to interpolate everything the client shows. → [the frame](../client/the-frame.md)

**Permission level** — the integer a command source carries and a command
node requires; four levels, granted by the ops file or by being the server. → [Brigadier and commands](../commands/brigadier-and-commands.md)

**PlacedFeature** — a configured feature plus an ordered list of placement
modifiers; the unit a biome actually names. → [features and placement](../worldgen/features-and-placement.md)

**Point of interest** — a per-position index of blocks worth walking to
(beds, job sites, portals), stored beside the chunks in its own files. → [game events and points of interest](../world/game-events-and-poi.md)

**Prediction ledger** — the client's record of what the server last said
about a block it changed optimistically; the ack is permission to apply
that opinion, not a rollback. → [block interaction](../blocks/block-interaction.md)

**Protocol phase** — one of handshake, status, login, configuration and
play; each has its own packet table and its own listener. → [protocol phases](../networking/protocol-phases.md)

## R

**Recipe** — a server-side matcher and assembler; the client is never sent
one, only a display and an id. → [recipes](../items/recipes.md)

**Region file** — the 32-by-32-chunk container file chunks are stored in,
addressed by a sector table at its head. → [chunk storage](../world/chunk-storage.md)

**Registry** — a frozen, id-assigning table of one kind of thing; some are
built into the jar, some are loaded from data packs, some are sent to the
client. → [identifiers and registries](../foundations/identifiers-and-registries.md)

**RenderPipeline** — the client's declaration of everything fixed about a
draw (shader, blend, depth, vertex format). → [Blaze3D](../client/blaze3d.md)

**Render state** — the immutable snapshot of what to draw, produced by the
extract half of the frame and consumed by the drawing half. → [entity rendering](../client/entity-rendering.md)

**Resource pack** — a pack of assets; the client half of the same pack
machinery data packs use. → [the resource system](../foundations/resource-system.md)

## S

**SavedData** — a named, codec-backed blob stored beside the world (the
border, the weather, the rules, raids, the dragon fight); `level.dat`
itself is nearly a stub. → [level data and rules](../world/level-data-and-rules.md)

**Section** — a 16-cubed piece of a chunk: one paletted container of block
states, one of biomes, and light arrays owned by the light engine. → [chunk anatomy](../world/chunk-anatomy.md)

**Section mesh** — the compiled vertex buffers for one section, rebuilt off
the main thread when the section is both dirty and visible. → [level rendering](../client/level-rendering.md)

**Sensor** — the half of brain AI that writes memories from the world, on a
fixed interval. → [AI](../entities/ai-goals-and-brains.md)

**ServerEntity** — the server's per-tracked-entity bookkeeping: what the
watching clients were last told, and what to send them next. → [what the client is told](../networking/what-the-client-is-told.md)

**Shape update** — the "your neighbour changed, recompute yourself" call
that runs on both client and server, unlike a neighbour update. → [block interaction](../blocks/block-interaction.md)

**Signed message** — a chat message carrying a signature over its content
and its place in a per-player chain, so the server can prove who said it. → [chat and signing](../networking/chat-and-signing.md)

**StreamCodec** — the wire counterpart of a `Codec`: encodes to and decodes
from a `ByteBuf`, with no schema and no field names. → [packets and stream codecs](../networking/packets-and-stream-codecs.md)

**Structure** — a generated building or landmark: a placement lottery, a
start assembled in memory, and pieces written a chunk at a time. → [structures](../worldgen/structures.md)

**SynchedEntityData** — the per-entity table of small values the server
pushes to watching clients, keyed by class-tree ordinal. → [synched entity data](../entities/synched-entity-data.md)

## T

**Tag** — a named set of registry entries defined by data packs and merged
across them. (The NBT sense of the word is written *NBT tag* throughout.) → [tags](../foundations/tags.md)

**Tick** — one 50 ms step of the server's simulation, or one step of the
client's; the client drops the ticks it cannot keep up with rather than
deferring them. → [the server tick](../server/server-tick.md), [the frame](../client/the-frame.md)

**Ticket** — the reason a chunk is loaded, with a level deciding how far it
gets: loaded, block-ticking or entity-ticking. → [tickets and loading](../world/tickets-and-loading.md)

**Timeline** — the keyframe curve an environment attribute is sampled from
as the day advances. → [lightmap, fog and sky](../client/lightmap-fog-and-sky.md)

**Trigger** — the server-side hook that tells every listening player's
advancement state that something happened. → [advancements](../commands/advancements.md)

## V

**VoxelShape** — the collision or outline volume of a block state, held as
a set of boxes with fast merge and sweep operations. → [math and primitives](../foundations/math-and-primitives.md)

## W

**WorldGenRegion** — the bounded, write-guarded view of the world a
generation step is given; it throws rather than loading a chunk, which is
why cascading worldgen cannot happen. → [the chunk generation pipeline](../world/chunk-generation-pipeline.md)

---

*Rules: names, never code · how the system works, not how the code reads ·
newest version only · every backticked name passes `tools/verify_names.py`.*
