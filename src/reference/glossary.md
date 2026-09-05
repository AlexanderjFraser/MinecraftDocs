# Glossary

> Verified against **Minecraft 26.2** · Reference · One sentence
> per term the rest of the corpus uses, and a link to the page that owns it.

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

**Activity** — the filter that decides which of a brain's behaviours are
asked at all, rather than a mode it runs in: the active set is always the core
activities plus exactly one other, and an `ActivityData` declares each one's
prioritised behaviour list. → [AI](../systems/entities/ai-goals-and-brains.md)

**Advancement** — a data-pack-defined goal: criteria, a requirements
expression over them, an optional display entry and a reward. → [advancements](../systems/commands/advancements.md)

**Aquifer** — the worldgen component that decides what a point is made of
once the density is known — stone, air, water or lava — from its own barrier
and fluid-level noises; a carver writes the block itself but asks the aquifer
which block to write. → [terrain](../systems/worldgen/terrain.md)

**Argument type** — a Brigadier `ArgumentType` that parses one *argument* off
the command line, however many words that takes — three for a `Vec3Argument`,
all of the rest for a `MessageArgument`; vanilla's live in
`net/minecraft/commands/arguments` and are described to the client through an
`ArgumentTypeInfo`. → [Brigadier and commands](../systems/commands/brigadier-and-commands.md)

**Atlas** — one large texture stitched at load time out of many sprite
files, so a chunk section can be drawn with a single bound texture. → [models and atlases](../systems/rendering/models-and-atlases.md)

**Attribute** — a named, ranged, modifiable number on a `LivingEntity`;
modifiers are keyed by `Identifier`, and eight attributes are not
client-syncable at all. → [attributes](../systems/entities/attributes.md)

**Authority** — whose copy of an entity produces the position that counts:
the server for a mob, the owning client for its own player and for the boat
that player is steering — the server still runs your player's physics, then
overwrites its answer with the number your client sent. Five predicates on
`Entity` decide it, starting with the final
`Entity.isLocalInstanceAuthoritative`. → [authority](../systems/entities/authority.md)

**Avatar** — the class between `LivingEntity` and `Player`; a `Mannequin`
is an `Avatar` that is not a player, and `AvatarRenderer` draws both. → [player anatomy](../systems/player/player-anatomy.md)

## B

**Batch** — a group of game tests keyed by the environment they share;
a batch *is* an environment, not a name and not a class. → [game tests](../systems/commands/game-tests.md)

**Beardifier** — the density-function term that bends terrain around a
structure; terrain adaptation writes no blocks, it changes the noise. → [structure placement](../systems/worldgen/structure-placement.md)

**Behaviour** — one unit of brain AI, gated on memories and asked once a
tick; unless it overrides `Behavior.canStillUse` it stops inside the same
`Brain.tick` that started it, so everything it does it does in
`Behavior.start`. → [AI](../systems/entities/ai-goals-and-brains.md)

**Biome** — a named bundle of generation settings, mob spawns, block tints
and environment attributes, attached to a 4×4×4 volume of the world. → [biomes](../systems/worldgen/biomes.md)

**BiomeSource** — the object that answers "which biome is at this quart
position": by a climate search, from one fixed biome, from a checkerboard of a
listed few, or — in the End — off a single erosion sample. → [biomes](../systems/worldgen/biomes.md)

**Blaze3D** — Mojang's GPU abstraction, with OpenGL and Vulkan backends
behind one `GpuDevice`. → [Blaze3D](../systems/rendering/blaze3d.md)

**Blend alpha** — the mixing weight `Blender` computes from the distance to
the nearest measured old column: zero against the seam (use the old
measurement), one out of range (use the noise). → [blending at the old-chunk border](../systems/worldgen/blending.md)

**Blending data** — the sixteen-column ring of heights, densities and biomes
a `BlendingData` measures out of its **own** chunk's blocks, on the sides
facing ground the game has yet to generate; its presence on a chunk is what
makes the chunk old. → [blending at the old-chunk border](../systems/worldgen/blending.md)

**Block** — the singleton describing a kind of block: its behaviour, its
property set and its state table. One `Block`, many `BlockState`s. → [blocks and states](../systems/blocks/blocks-and-states.md)

**Block entity** — the per-position mutable state a block cannot fit into
its state (a chest's contents, a furnace's progress), stored on the chunk. → [block entities](../systems/blocks/block-entities.md)

**Block event** — a message from a block to itself (a piston push, a note
block, a chest lid), queued on `ServerLevel` and drained at one fixed point
in the level tick — so it lands late, usually within the same tick — and
mirrored to nearby clients as a packet. → [pistons and block events](../systems/blocks/pistons-and-block-events.md)

**BlockState** — one combination of a block's property values, built once by
the block's `StateDefinition` and compared by identity;
`Block.BLOCK_STATE_REGISTRY` is the flat table that numbers it for the wire and
the global palette. → [blocks and states](../systems/blocks/blocks-and-states.md)

**Border tick** — a position along an old chunk's seam queued for
post-processing, so a leaf or a fluid there is re-evaluated when the chunk
goes live. → [blending at the old-chunk border](../systems/worldgen/blending.md)

**Brain** — the memory-and-behaviour AI used by villagers, piglins and
axolotls, as opposed to the older goal system. → [AI](../systems/entities/ai-goals-and-brains.md)

**Brigadier** — Mojang's command-parsing library: a tree of literal and
argument nodes with per-node requirements, shared by client and server. → [Brigadier and commands](../systems/commands/brigadier-and-commands.md)

**Built-in block model** — a block model attached in code by
`BuiltInBlockModels` rather than by a resource pack, living in a second
model table that terrain never reads; how a minecart or a block display
draws a chest. → [block-entity rendering](../systems/rendering/block-entity-rendering.md)

## C

**Camera** — the client's eye: position, rotation and the cull frustum,
copied into a `CameraRenderState` once per frame — plus an
`EnvironmentAttributeProbe` that `Camera.tick` advances and no render state
carries. → [the frame](../systems/rendering/the-frame.md)

**Carver** — a worldgen pass that hollows out caves and ravines by writing
air, water or lava, asking the `Aquifer` which — except the nether carver,
which does not ask. → [terrain](../systems/worldgen/terrain.md)

**Cell** — the lattice unit of terrain noise, four blocks wide and deep and
eight tall in the overworld, 768 to a chunk: the expensive three-dimensional
density terms are evaluated at its corners and interpolated within it, and the
caches keyed on it mean nothing outside the cell loop. → [terrain](../systems/worldgen/terrain.md), [density functions](../systems/worldgen/density-functions.md)

**Chunk** — a 16-by-16 column of the world's full height: sections,
heightmaps, block entities, tick queues and a status. → [chunk anatomy](../systems/world/chunk-anatomy.md)

**Chunk layer** — which of the three `ChunkSectionLayer` buffers a block's
quads are meshed into — solid, cutout or translucent — decided at bake time
from the alpha inside that quad's own patch of its sprite rather than from the
block. → [models and atlases](../systems/rendering/models-and-atlases.md), [section meshing](../systems/rendering/section-meshing.md)

**ChunkHolder** — the server's per-chunk record of the *level* the two graphs
computed for it, a future per threshold and status, and what changed in it this
tick; which tickets asked for that level is `TicketStorage`'s business, not the
holder's. → [tickets and loading](../systems/world/tickets-and-loading.md)

**ChunkMap** — the server's chunk table: holders, the ticket-driven level
graphs, entity tracking, and the region-file storage underneath. → [tickets and loading](../systems/world/tickets-and-loading.md)

**ChunkStatus** — one rung of the generation ladder; a chunk advances one
status at a time, and the `ChunkStep` for each status declares the neighbour
radius that step needs. → [the chunk generation pipeline](../systems/world/chunk-generation-pipeline.md)

**Climate** — the noise sample (temperature, humidity, continentalness,
erosion, depth, weirdness) a biome is chosen by. → [biomes](../systems/worldgen/biomes.md)

**Codec** — a DataFixerUpper object that both encodes and decodes one type
against any `DynamicOps`; the corpus's universal serialisation vocabulary. → [codecs, NBT and JSON](../systems/foundations/codecs-nbt-json.md)

**CommandSourceStack** — *who is running this command, and from where*:
position, rotation, level, entity, a `PermissionSet` and an output sink,
immutable, so every `with…` returns a copy. → [Brigadier and commands](../systems/commands/brigadier-and-commands.md)

**Compiled query** — the immutable `EntitySelector` a parse produces:
thirteen fields, no reader and no grammar, resolvable any number of times
against different sources. → [entity selectors](../systems/commands/entity-selectors.md)

**Component** — two different things the corpus keeps apart: a *data
component* on an item stack, and a `Component` of chat text. → [data components](../systems/foundations/data-components.md), [text components](../systems/foundations/text-components.md)

**Connection** — the tail handler of one Netty pipeline plus the channel it
holds, with exactly one packet listener at a time, swapped when the protocol
phase changes. → [the connection](../systems/networking/the-connection.md)

**Container** — the interface a thing with item slots implements (a chest,
a hopper, an inventory), as distinct from the *menu* a player interacts
with it through. → [containers and menus](../systems/items/containers-and-menus.md)

**Criterion** — one condition inside an advancement, backed by a
`CriterionTrigger` the server fires when the relevant thing happens. → [advancements](../systems/commands/advancements.md)

## D

**DamageSource** — the *what hit you, and who is responsible* record every
damage calculation and death message reads. → [damage and death](../systems/entities/damage-and-death.md)

**Data component** — a typed, codec-backed value keyed by a
`DataComponentType`: a patch over the item's prototype on a stack, a whole map
on a block entity, read-only on an entity; what NBT item tags became. → [data components](../systems/foundations/data-components.md)

**Data pack** — a pack of JSON, structure NBT and function files supplying
the server's data-driven content; the server half of the resource system. → [the resource system](../systems/foundations/resource-system.md)

**DataLayer** — the nibble array one section's block light or sky light lives
in, owned by the light engine and never by the section. → [lighting](../systems/world/lighting.md)

**Debug subscription** — a registered kind of debug value a client can ask
the server for; most kinds the server polls, diffs and sends only when they
change, and the rest it pushes as they happen. → [debugging the running game](../systems/client/debugging-the-running-game.md)

**DeltaTracker** — the client's clock: how much of a tick has elapsed, and
the source of every partial tick in the frame but the lightmap's, which is a
literal one. → [the client loop](../systems/client/the-client-loop.md)

**Density function** — a node in the JSON-defined graph that turns a
position into a number; the graph in the registry is never the graph that
actually runs. → [density functions](../systems/worldgen/density-functions.md)

**Dialog** — a data-pack-defined form the server can put on a player's
screen, whose submitted values come back as a packet. → [dialogs](../systems/commands/dialogs.md)

**Dimension** — one `ServerLevel` and its `DimensionType`: a height range,
a set of environment attributes and its own chunk storage. → [level data and rules](level-data-and-rules.md)

## E

**Enchantment** — a data-pack record of effect components conditioned on loot
predicates; its registry is synchronised, but a client that already has the
pack is sent only the id. → [enchantments](../systems/items/enchantments.md)

**Entity** — a thing the level ticks in its own right: a position, a bounding
box, synched data and a tick method. A *block entity* is not one. → [entity anatomy](../systems/entities/entity-anatomy.md)

**EntityType** — the registry entry for a kind of entity: its factory,
category, size, feature flags and the two numbers that decide how it reaches
clients. Spawn rules are keyed *by* the type in `SpawnPlacements`, not held on
it. → [entity anatomy](../systems/entities/entity-anatomy.md)

**EnvironmentAttribute** — a per-dimension, per-biome, per-time-of-day,
per-weather value resolved through a stack of layers: directly on the server,
through the camera's smoothing probe on the client. Not only the visual ones:
alongside fog and sky colour sit twenty gameplay attributes — whether lava
flows fast, whether piglins zombify, whether a bed works, and the villager's
schedule. → [environment attributes and timelines](../systems/world/environment-attributes-and-timelines.md)

**Event loop** — the queue-and-thread pairing `BlockableEventLoop` is: an
owning thread that drains posted tasks and, through
`BlockableEventLoop.managedBlock`, keeps draining while it waits.
`Minecraft` and `MinecraftServer` are both one — but only the server rations
the drain against a time budget; the client empties the queue every frame. → [the server tick](../systems/server/server-tick.md#the-event-loop-and-what-a-ticks-spare-time-buys)

**Experiment** — a built-in data pack whose `PackSource` is
`PackSource.FEATURE`, enabling one non-vanilla `FeatureFlag`; switching one
on in the create-world screen is a data-pack reload. → [creating a world](../systems/worldgen/creating-a-world.md)

**Extract** — the first half of the client's frame: walk the game state, cull
it, and write the render states, so that the drawing half reads no live game
object from `LevelRenderer.render` down — the top of the render half still
does. The top-level states are single objects re-filled each frame, not fresh
immutable values. → [the frame](../systems/rendering/the-frame.md)

## F

**Feature** — the algorithm half of decoration: what to build, with no say in
which positions it is offered. → [features and placement](../systems/worldgen/features-and-placement.md)

**Flat level generator preset** — a `FlatLevelGeneratorPreset`: a display
item plus a `FlatLevelGeneratorSettings`, one row of the Superflat *Presets*
screen. → [creating a world](../systems/worldgen/creating-a-world.md)

**Fluid** — the registry object behind a `FluidState`, a source and a flowing
instance per liquid, with `FlowingFluid` holding the spread algorithm and
`LiquidBlock` the block form. → [fluids](../systems/world/fluids.md)

**Font** — a resource-pack-defined glyph source plus the measuring and
wrapping API on top of it; a glyph is baked into a texture the first time it
is asked for. → [text and fonts](../systems/client/text-and-fonts.md)

**Frame** — the execution engine's unit of a running function: a depth, a
result callback that `/return` feeds sideways, and a control that can delete
the frame's pending work — one object shared by reference across a whole
function body, and deliberately *not* a stack frame. → [the execution engine](../systems/commands/the-execution-engine.md)

**Frame graph** — the client's per-frame declaration of render passes and
the targets each reads and writes, resolved before anything is drawn. → [visibility and the frame graph](../systems/rendering/visibility-and-the-frame-graph.md)

**Function** — a `.mcfunction` file: a list of commands loaded as a
`CommandFunction`, optionally with macro lines. → [functions and macros](../systems/commands/functions-and-macros.md)

## G

**Game event** — a broadcast fact about something that just happened at a
position (a block placed, a door opened) that sculk sensors and mobs
listen for. → [game events and vibrations](../systems/world/game-events-and-vibrations.md)

**Game rule** — one typed, server-wide switch or number in `GameRules`, saved
with the world and sometimes sent to the client. → [level data and rules](level-data-and-rules.md)

**Game test** — a data-driven test instance: a structure, an environment
and a check the server runs and reports on. → [game tests](../systems/commands/game-tests.md)

**Globally-rendered block entity** — one whose renderer says
`BlockEntityRenderer.shouldRenderOffScreen`, so the client keeps it in a
level-wide set and draws it whether or not its section is visible; three
renderers qualify. → [block-entity rendering](../systems/rendering/block-entity-rendering.md)

**Goal** — one unit of the older mob AI: a start condition, an answer to
whether it may be interrupted, and the set of `Goal.Flag` controls it claims
while running. The priority belongs to the `WrappedGoal` that holds it, and
the flag table rather than the priority is what arbitrates. → [AI](../systems/entities/ai-goals-and-brains.md)

**GpuDevice** — the façade every GPU resource is created through; both
graphics backends sit behind it as `GpuDeviceBackend` implementations. A draw
reaches the driver through the `CommandEncoder` it hands out and the
`RenderPass` that opens. → [Blaze3D](../systems/rendering/blaze3d.md)

**GuiRenderState** — the 2D render tree: strata of nodes that infer their own
layering from bounding boxes and are batched into draw calls at the end of the
frame. → [the GUI render tree](../systems/client/the-gui-render-tree.md)

## H

**Heightmap** — a per-chunk 2D array holding the first *free* Y above the
topmost block matching a predicate; six types exist, and a live chunk keeps the
four that survive worldgen. → [chunk anatomy](../systems/world/chunk-anatomy.md)

**Holder** — a reference to a registry entry that can exist before the
entry is bound: `Holder.Reference` for a registered value, `Holder.Direct`
for an inline one. → [identifiers and registries](../systems/foundations/identifiers-and-registries.md)

**HolderSet** — a set of holders: either a tag (`HolderSet.Named`) or a
literal list. → [tags](../systems/foundations/tags.md)

**HUD** — the in-world overlay (hotbar, hearts, chat, boss bars), which in
26.2 is the class `Hud` — `Gui` now means the screen manager. → [the HUD](../systems/client/hud.md)

## I

**Identifier** — a namespace and a path; the id of everything. A 1.21-era
reader knows it as *ResourceLocation*. → [identifiers and registries](../systems/foundations/identifiers-and-registries.md)

**Ingredient** — a recipe's "any of these items" test. It cannot be an
empty inline list, but a tag that resolves to nothing makes one empty — and a
recipe holding it is never placeable. → [recipes](../systems/items/recipes.md)

**Integrated server** — the `MinecraftServer` a singleplayer client runs on
its own Server thread. Every change to the *world* still crosses as a packet;
a handful of settings cross by direct call. → [anatomy](../systems/anatomy/anatomy.md)

**InteractionResult** — the answer a block or item gives to a click: was
the input consumed, should the arm swing, did the held item change. → [block interaction](../systems/blocks/block-interaction.md)

**Item** — the singleton for a kind of item, holding none of the components
a stack shows; a stack is a holder to one of these, a count, a pop time and a
patched component map — the item's defaults plus the ways this stack differs
from them. → [items and stacks](../systems/items/items-and-stacks.md)

**ItemStackTemplate** — the immutable item-shaped record (an item holder, a
count, a component patch) that data uses where a live, mutable `ItemStack`
would be wrong. → [items and stacks](../systems/items/items-and-stacks.md)

## J

**Jigsaw** — the structure-assembly system that grows a village out of
template pieces by matching connector blocks. → [jigsaw and templates](../systems/worldgen/jigsaw-and-templates.md)

## K

**KeyMapping** — one bindable action: whether its key is down, plus a counter
of owed clicks that `KeyMapping.consumeClick` **drains** rather than
edge-detects. → [input and keybinds](../systems/client/input-and-keybinds.md)

## L

**Level** — a world: `ServerLevel` on the server, `ClientLevel` on the
client, sharing an abstract `Level` and remarkably little else. → [the level tick](../systems/server/server-level-tick.md), [the client level](../systems/client/the-client-level.md)

**Lightmap** — the small texture the client samples to turn a block-light /
sky-light pair into a colour; drawn on the GPU once per tick. → [lightmap, fog and sky](../systems/rendering/lightmap-fog-and-sky.md)

**LocalPlayer** — the `Player` a human steers: its own `ClientInput`, its own
prediction, and the last input and position it sent. → [player anatomy](../systems/player/player-anatomy.md)

**Loot table** — the data-driven roll that turns an event (a block broken, a
mob killed, anything at all reading a container that has not been rolled yet)
into item stacks. → [loot tables](../systems/items/loot-tables.md)

## M

**Macro** — a function line beginning with a `$` substitution. The plain
lines of the file are parsed once at load; a macro line is substituted and
**re-parsed** per distinct argument tuple, cached only eight deep. → [functions and macros](../systems/commands/functions-and-macros.md)

**Memory** — one typed, optionally expiring value in a `Brain`; behaviours
are gated on which memories are present. → [AI](../systems/entities/ai-goals-and-brains.md)

**Menu** — the server-authoritative object behind an open container screen:
slots, a synchroniser and a state id. → [containers and menus](../systems/items/containers-and-menus.md)

**MultiPlayerGameMode** — the client's only channel for acting on the world:
every break, place, use and attack goes through it, and the ones that predict
open a prediction window before they send. → [prediction and acknowledgement](../systems/client/prediction-and-acks.md)

## N

**NBT** — Minecraft's binary tag format; in 26.2 a sealed `Tag` hierarchy
whose scalars are records and whose containers (`CompoundTag`, `ListTag`) are
final classes, read and written through `NbtIo` and reached by codecs through
`NbtOps`. → [codecs, NBT and JSON](../systems/foundations/codecs-nbt-json.md)

**NBT path** — a compiled query over a tag, six node kinds deep — a named
child, an index, all elements, and three kinds of match — that `/data` uses to
read and write, and which materialises the structure it walks through on a
write. → [scores, teams and stored data](../systems/commands/scoreboard-and-data.md)

**Neighbour update** — the server-only notification a block sends its six
neighbours after a change; distinct from a *shape update*, which runs on
both sides. → [blocks and states](../systems/blocks/blocks-and-states.md)

**NoiseChunk** — the per-chunk machine that fills the noise lattice and
installs the caches the density-function graph asked for. → [density functions](../systems/worldgen/density-functions.md)

**NoiseRouter** — the density functions a generator asks for, as one record;
`NoiseRouter.mapAll` rebuilds them all at once, which is how a whole graph gets
its caches installed in one pass. → [density functions](../systems/worldgen/density-functions.md)

## O

**Objective** — a named scoreboard column: a criterion, a display name, a
render type and a number format. Only the *dummy* and *trigger* criteria wait
for commands; every other one — including every statistic in the game, since
`Stat` extends `ObjectiveCriteria` — is driven from `ServerPlayer`. → [scores, teams and stored data](../systems/commands/scoreboard-and-data.md)

**Old chunk** — a chunk whose `ChunkAccess.blendingData` is non-null, which
is to say one whose save data carried a *blending_data* compound;
`ChunkAccess.isOldNoiseGeneration` is the test. → [blending at the old-chunk border](../systems/worldgen/blending.md)

## P

**Packet** — an interface: a `PacketType`, which is a name and a direction,
and one handler method. Roughly half the implementations are records, the
wire form is a `StreamCodec` the phase's protocol description holds rather
than something the class owns, and a few types are registered into more than
one phase. → [packets and stream codecs](../systems/networking/packets-and-stream-codecs.md)

**PalettedContainer** — the bit-packed storage a chunk section keeps its
block states and biomes in, with a palette that grows as the section gets
more varied. → [chunk anatomy](../systems/world/chunk-anatomy.md)

**Partial tick** — the fraction of a tick elapsed at the moment a frame is
drawn, used to interpolate the world. There is no single one: a frame carries
six values, they disagree on purpose, and the one screens are handed is not a
fraction of a tick at all. → [the frame](../systems/rendering/the-frame.md)

**Path** — the list of nodes a navigator is following, produced by
`PathFinder`'s A\* over a snapshot of already-loaded chunks, with a
`NodeEvaluator` deciding what each candidate block *is* to this mob. → [pathfinding](../systems/entities/pathfinding.md)

**Permission atom** — a named capability with an `Identifier`
(`Permission.Atom`), the other kind of permission besides a command level;
an operator's level-based set grants exactly one, the entity-selector atom,
from gamemaster up. → [permissions](../systems/commands/permissions.md)

**Permission level** — one rung of `PermissionLevel` (all, moderators,
gamemasters, admins, owners), and only the *ordered* half of a permission: a
command source carries a `PermissionSet` and a node requires a
`PermissionCheck`, neither of which is an integer. → [permissions](../systems/commands/permissions.md)

**Permission set** — what a command source carries and a node's check is
asked against: on the server a level-based set (a rung plus one atom). The
client rebuilds four of those from the op level it is told — rung zero maps to
`PermissionSet.NO_PERMISSIONS` instead — and keeps a chat set built by
subtraction beside them. No packet carries a `PermissionSet` itself. → [permissions](../systems/commands/permissions.md)

**PlacedFeature** — a configured feature plus an ordered list of placement
modifiers; the unit a biome actually names. → [features and placement](../systems/worldgen/features-and-placement.md)

**Point of interest** — a block state the game has decided is worth walking
to: a bed, a job site, a portal. `PoiManager` indexes them by position, in its
own files beside the chunks. → [points of interest](../systems/world/points-of-interest.md)

**Prediction ledger** — the corpus's name for `BlockStatePredictionHandler`:
the client's record of what the server is known to have at a block it changed
optimistically. The ack is a receipt for a number, not a verdict — it settles
every entry at or below it, writing back a correction if one arrived and
rolling the block back if none did. → [prediction and acknowledgement](../systems/client/prediction-and-acks.md)

**Protocol phase** — one of handshake, status, login, configuration and
play; each has its own packet table and its own listener. → [protocol phases](../systems/networking/protocol-phases.md)

## Q

**Quart** — a four-block cell, the resolution biomes are stored and
sampled at; `QuartPos` is the arithmetic. → [biomes](../systems/worldgen/biomes.md), [math and primitives](math-and-primitives.md)

## R

**Recipe** — a server-side matcher and assembler; no `Recipe` ever crosses
the wire. The client gets a `RecipeDisplay` and a `RecipeDisplayId`, which is a
position in a list rather than the recipe's name. → [recipes](../systems/items/recipes.md)

**Region file** — the 32-by-32-chunk container file chunks are stored in,
addressed by a sector table at its head. → [chunk storage](../systems/world/chunk-storage.md)

**Registry** — a frozen, id-assigning table of one kind of thing; some are
built into the jar, some are loaded from data packs, some are sent to the
client. → [identifiers and registries](../systems/foundations/identifiers-and-registries.md)

**Reload listener** — the unit of a reload: one object that reads what it
needs off the worker pool and swaps its live state on the owning thread, every
apply running in order behind a `PreparableReloadListener.PreparationBarrier`. → [the resource system](../systems/foundations/resource-system.md)

**Render state** — the write-once snapshot of what to draw, produced by the
extract half of the frame and consumed by the drawing half. The property that
matters is that the drawing half reads no game object, not that the state is
an immutable value. → [the frame](../systems/rendering/the-frame.md), [entity rendering](../systems/rendering/entity-rendering.md)

**RenderPipeline** — the client's declaration of how to rasterise: shaders,
blend, depth, cull, vertex format, topology. It says nothing about which
textures to bind or which target to draw into; that is `RenderType`. → [Blaze3D](../systems/rendering/blaze3d.md)

**RenderType** — a `RenderPipeline` plus everything a pipeline does not say:
which target to draw into, which textures to bind, and the layering and
batching rules. → [Blaze3D](../systems/rendering/blaze3d.md)

**Resource pack** — a pack of assets; the client half of the same pack
machinery data packs use. → [the resource system](../systems/foundations/resource-system.md)

## S

**SavedData** — a named, codec-backed blob stored beside the world (the
border, the weather, the rules, raids, the dragon fight); `level.dat`
itself is nearly a stub. → [level data and rules](level-data-and-rules.md)

**Scheduled tick** — a block or fluid position queued to run at a named
future tick, with a priority breaking ties inside that tick. → [scheduled ticks](../systems/world/scheduled-ticks.md)

**Score** — one number for one holder under one objective, reached through a
`ScoreAccess` handle rather than a setter. → [scores, teams and stored data](../systems/commands/scoreboard-and-data.md)

**Screen** — one full-window client UI with its own widget tree and
lifecycle; the server is told nothing about most of them. → [GUI and screens](../systems/client/gui-and-screens.md)

**Section** — a 16-cubed piece of a chunk: one paletted container of block
states, one of biomes, and four counters. Its light lives in the light
engine's own storage, not on the section. → [chunk anatomy](../systems/world/chunk-anatomy.md)

**Section mesh** — the compiled vertex buffers for one section
(`CompiledSectionMesh`), rebuilt when the section is both dirty and visible —
usually on a worker, but inline on the client thread when the chunk-builder
option asks for it. → [section meshing](../systems/rendering/section-meshing.md)

**Selector head** — the single character after the *@* (*a*, *e*, *n*,
*p*, *r*, *s*) that sets a selector's default limit, order and entity scope
before any option is read; three of the six also pin the type to player, and
two instead add an aliveness test. → [entity selectors](../systems/commands/entity-selectors.md)

**Sensor** — the half of brain AI that writes memories from the world, on a
fixed interval. → [AI](../systems/entities/ai-goals-and-brains.md)

**ServerEntity** — the server's per-tracked-entity bookkeeping: what the
watching clients were last told, and what to send them next. → [what the client is told](../systems/networking/what-the-client-is-told.md)

**Shape update** — the "your neighbour changed, recompute yourself" call
that runs on both client and server, unlike a neighbour update. → [blocks and states](../systems/blocks/blocks-and-states.md)

**Signed message** — a chat message carrying a signature over its content
and its place in a per-player chain, so the server can prove who said it. → [chat and signing](../systems/networking/chat-and-signing.md)

**Simulation distance** — how far the world *ticks*, as against how far you
can see: the radius behind `TicketType.PLAYER_SIMULATION`, deciding which
chunks tick blocks, fluids and entities. → [tickets and loading](../systems/world/tickets-and-loading.md)

**Special model renderer** — a hand-written submitter for a shape no cuboid
model can express, reached from an item model or a block state rather than
from a block entity; thirteen of them. → [block-entity rendering](../systems/rendering/block-entity-rendering.md)

**Staging buffer** — the list an executing action appends its spawned
commands to, spliced onto the *head* of the queue after it runs — which is
what makes an `ArrayDeque` behave as a call stack. → [the execution engine](../systems/commands/the-execution-engine.md)

**StreamCodec** — the wire counterpart of a `Codec`: encodes to and decodes
from a `ByteBuf`, with no schema and no field names. → [packets and stream codecs](../systems/networking/packets-and-stream-codecs.md)

**Structure** — a generated building or landmark: a placement lottery, a
start assembled in memory, and pieces written a chunk at a time. → [structure placement](../systems/worldgen/structure-placement.md)

**StructurePiece** — one room, corridor or slab of a structure. In the
hand-built half it is a Java class that writes its own blocks and constructs its
own neighbours, chosen by no pool; the jigsaw half's `PoolElementStructurePiece`
is one too. Every piece carries a registered `StructurePieceType`, which is how
it comes back off disk. → [hand-built structures](../systems/worldgen/hand-built-structures.md)

**StructureStart** — one decided structure: the `Structure`, the chunk it
started in, a `PiecesContainer`, a reference count and a cached bounding box,
stored on the chunk it began in. → [structure placement](../systems/worldgen/structure-placement.md)

**Submit node** — one thing to draw that is not terrain, written into
`SubmitNodeStorage` by the *submit* pass out of the render states extract left
behind, and sorted into a phase before the feature renderers turn it into
vertices. → [entity rendering](../systems/rendering/entity-rendering.md), [submit phases](submit-phases.md)

**SynchedEntityData** — the per-entity table of small values the server
pushes to watching clients, keyed by class-tree ordinal. → [synched entity data](../systems/entities/synched-entity-data.md)

## T

**Tag** — a named set of registry entries defined by data packs and merged
across them, unless a higher pack sets *replace*. (The unrelated NBT sense of
the word belongs to [NBT](../systems/foundations/codecs-nbt-json.md).) → [tags](../systems/foundations/tags.md)

**Team** — a named set of score holders carrying a colour, a friendly-fire
flag, a collision rule and a nametag rule — so a class in the scores package
is read by collision and by rendering. → [scores, teams and stored data](../systems/commands/scoreboard-and-data.md)

**Tick** — one step of the server's simulation, 50 ms at the default rate
that `/tick rate` can change, or one step of the client's; a client behind
the clock catches up to ten accumulated ticks in a frame and discards the
rest. → [the server tick](../systems/server/server-tick.md), [the client loop](../systems/client/the-client-loop.md)

**Ticket** — the reason a chunk is loaded: a type and a level, fed into two
separate graphs, with `ChunkLevel` deciding what the level buys — a holder
only, then full, then block-ticking, then entity-ticking. → [tickets and loading](../systems/world/tickets-and-loading.md)

**Timeline** — one clock's data-driven curve set: an optional period, the
named instants on that clock, and one `AttributeTrack` per environment
attribute — keyframed over *modifier arguments*, not over values. → [environment attributes and timelines](../systems/world/environment-attributes-and-timelines.md)

**Trigger** — the server-side hook that tells **one** player's advancement
state that something happened, by sweeping that player's listener map for
this trigger. Nothing broadcasts. → [advancements](../systems/commands/advancements.md)

## U

**Unattended command** — a command the player did not type: a dialog button
or a chat click event, sent through `ClientPacketListener.sendUnattendedCommand`.
The client re-parses it and asks first if it fails to parse, needs a signature,
or needs a permission the client believes it lacks; a clean one goes without a
prompt. A sign's command is not one of these — it runs on the server at
gamemaster level and the client is never asked. → [permissions](../systems/commands/permissions.md)

## V

**View distance** — how far the *server* sends chunks. A client's
render-distance request only clamps what it is sent; the ticket radius comes
from the server's own number. Not *simulation distance*, which is how far
the world ticks. → [tickets and loading](../systems/world/tickets-and-loading.md)

**VoxelShape** — the collision or outline volume of a block state, held as
a set of boxes with fast merge and sweep operations. → [math and primitives](math-and-primitives.md)

## W

**Watchdog** — `ServerWatchdog`, the daemon that treats a tick longer than
*max-tick-time* as a dead server: it writes a crash report, calls `System.exit`,
and halts the JVM ten seconds later whether the shutdown finished or not. → [how a server dies](../systems/server/how-a-server-dies.md)

**Window** — the GLFW handle the whole client hangs off: the framebuffer
size, the GUI scale, fullscreen, and the six window callbacks — not the input
ones, which `KeyboardHandler` and `MouseHandler` register. → [the window](../systems/rendering/the-window.md)

**World clock** — the identity a timeline is sampled against: a unit record
in `Registries.WORLD_CLOCK`, two of them in vanilla, holding nothing at all.
The tick count, the rate and the paused flag are
`ServerClockManager.ClockInstance`'s, one per clock, and `/time` can move or
pause each independently. → [environment attributes and timelines](../systems/world/environment-attributes-and-timelines.md)

**World gen settings** — `WorldGenSettings`: a `WorldOptions` (the seed,
*generate structures*, *bonus chest*) and the `LevelStem` map, a `SavedData`
written to *data/minecraft/world_gen_settings.dat*. It is the only part of world
generation that is saved; everything else Part XII reads is re-read from the
enabled packs on every world open. → [creating a world](../systems/worldgen/creating-a-world.md)

**World preset** — a `WorldPreset` registry entry holding one `LevelStem`
per dimension; what the world-type button selects, and what *level-type*
names on a dedicated server. → [creating a world](../systems/worldgen/creating-a-world.md)

**World stem** — `WorldStem`, the four things `WorldLoader.load` hands the
server constructor in one bundle: the resource manager, the reloadable server
resources, the layered registries, and the level data with its gen settings. → [starting a server](../systems/server/starting-a-server.md)

**World-limited** — a parse-time flag, set by any of seven positional
selector options, that confines a selector's resolve to the source's own
level instead of every level on the server. → [entity selectors](../systems/commands/entity-selectors.md)

**WorldGenRegion** — the bounded, write-guarded view of the world a
generation step is given; it throws rather than loading a chunk, which is
why cascading worldgen cannot happen. → [the chunk generation pipeline](../systems/world/chunk-generation-pipeline.md)


---

*Rules: names, never code · how the system works, not how the code reads ·
newest version only · every backticked name passes `tools/verify_names.py`.*
