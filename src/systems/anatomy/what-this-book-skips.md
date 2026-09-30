# What this book skips

> Verified against **Minecraft 26.3** · Part I · A reader opens the atlas, sees fourteen packages hatched, and asks what is in them and why no part counts them.

Open the atlas and part of the jar is drawn hatched. That hatching is this
page. Java Minecraft is 7,301 source files and 741,069 lines, and the parts do
not reach all of it. Some of what is left out is excluded on purpose by the
[newest-version-only rule](../../introduction.md#the-rules-the-book-keeps) —
save migration is version-difference code, and a book that documents only
the current version has nothing to say about it. Some is out of scope because it is a client for a service this
book cannot read. And one hatched box is not skipped code so much as skipped
*ground*: `net/minecraft/data` is the program that writes vanilla's own
content as a data pack, it ships in the dedicated server jar — all 174 files of it — and the running game compiles against it and calls into it.
`Blocks` names `TreeFeatures` keys while it constructs mushroom blocks;
`MinecraftServer` reaches for a `MiscOverworldFeatures` key for the bonus
chest; the F3 screen's biome-builder line runs through
`NoiseRouterData.peaksAndValleys` into `TerrainProvider`. A boundary drawn
honestly has to show where it leaks, and that is the largest leak in it.

<figure class="map">
{{#include ../../generated/packages-treemap.svg}}
<figcaption>The jar by package, area by lines of decompiled source. Hatched boxes are the packages this page tours, which no part counts. Click to enlarge.</figcaption>
</figure>

## The sizes, and which jar ships them

Each entry below says what the thing is, roughly how big it is, whether the
dedicated server ships it, one fact worth knowing, and where to start
reading. The treemap deliberately does not hatch `net/minecraft/gametest`:
Part XIII covers it, so it is a gap that closed rather than a skip. It cannot
hatch player reporting either, which is why the table has fifteen top-level
rows against the map's fourteen hatched packages: the map's smallest box is a
package four levels deep, and `net/minecraft/client/multiplayer/chat/report`
is six, sitting inside a package Parts IX and X between them own. The counts in the tables are files unless a cell says *classes*, so a *package-info.java* counts as one there and wherever the prose quotes the tables; a cell or a sentence that counts a
package's working classes leaves it out.

| package | files | lines | side |
|---|---:|---:|---|
| `net/minecraft/util/datafix` | 411 | 27,048 | both |
| `net/minecraft/util/filefix` | 57 | 3,553 | both |
| `net/minecraft/client/telemetry` | 18 | 1,221 | client |
| `net/minecraft/util/profiling` | 70 | 4,265 | both |
| `net/minecraft/server/jsonrpc` | 65 | 4,118 | dedicated server |
| `net/minecraft/server/rcon` | 9 | 837 | dedicated server |
| `com/mojang/realmsclient` | 137 | 14,701 | client |
| `net/minecraft/realms` | 4 | 203 | client |
| `net/minecraft/stats` | 10 | 874 | both |
| `net/minecraft/gizmos` | 15 | 569 | both |
| `net/minecraft/references` | 5 | 1,483 | both |
| `net/minecraft/data` | 174 | 16,849 | both — see below |
| └ `net/minecraft/data/worldgen` | 64 | 6,016 | both — see below |
| `net/minecraft/client/data` | 28 | 6,189 | client |
| `com/mojang/blaze3d/audio` | 12 | 1,013 | client |
| `net/minecraft/client/multiplayer/chat/report` | 12 | 952 | client |

The oracle for "server or client" throughout is the list of classes the
dedicated server jar ships, which lives beside the decompile. It answers
exactly one question — *does the dedicated server have this class* — so it
can prove "client-only" and it can prove "both jars", and it cannot prove
"dedicated server only". Two rows are labelled that way on the strength of a
different check: nothing under `net/minecraft/client` or `com/mojang/blaze3d`
references them. *rcon* is reached from `DedicatedServer` alone; *jsonrpc*
from six files, and two of them — `BuiltInRegistries` and `Registries` — are
classes the client loads at bootstrap, so the package's *types* are on the
client and the server it configures is not.

## Save migration, and the fixer that moves files

**`net/minecraft/util/datafix`** — the largest thing on this page and the
most explicitly out of scope. `DataFixers` is one static class whose whole
body is the migration history of the game written out longhand: just over
three hundred schema registrations and four hundred-odd fixes, from schema 99 up
to the current world version. The rewriting machinery itself is Mojang's
external DataFixerUpper library; what lives here is the vanilla catalogue —
`util/datafix/schemas` describing the *shape* of the data at each version,
and `util/datafix/fixes` doing the individual rewrites.

A version number becomes a chain of fixes through `DataFixTypes`, an enum
of about thirty type references (level, chunk, player, entity chunk, POI
chunk, options, stats, advancements, and a long tail of saved-data kinds).
`DataFixTypes.updateToCurrentVersion` takes the data version as an
argument — every one of its fourteen callers reads the version itself — and
asks the fixer to compose every rule from there to now.
`DataFixTypes.wrapCodec` is the one that reads the version *out of the tag*:
it wraps an ordinary codec so decoding pulls the data version, runs the
chain, and encoding stamps the current version back in. It is the rarer
door — two callers, `PlayerAdvancements` and `DebugScreenEntryList` — while
player data takes the first one and reads the version itself, and
[chunk storage](../world/chunk-storage.md) reads it too and takes a third,
`DataFixTypes.update`. The rules are
pre-compiled on a dedicated bootstrap thread, and that thread is built with
some care to stay out of the way: one thread, daemon, at minimum priority, with a
single caller in the client's entry point, optimising exactly one type (the
level-summary schema, so the world list opens fast). The dedicated server
never asks for it at all.

**`net/minecraft/util/filefix`** does what the other cannot. A data fixer
rewrites the *contents* of a tag after it has been read, so it can never
move, rename, split or delete a file. `FileFixerUpper` operates on the
world **directory**: its operations are moves, regex moves, group moves,
deletions, content modifications and one composite that scopes a nested list
of operations to matching folders, and the concrete fixes do things like
relocate dimension storage, gather player storage into one folder and pull data out of
*level.dat* into saved data
([level data and rules](../../reference/level-data-and-rules.md)).

It stays safe by working somewhere else: the whole upgrade runs against a
**custom copy-on-write file system** over the world folder, whose writes land
in a scratch directory, and the result is swapped in at the end. Exactly how safe depends on the filesystem
underneath. Where hard links are available it uses them. Where they are not,
it writes one file, *upgrade_in_progress.json*, recording the moves, and an
upgrade cut short by a crash resumes from it the next time the world is
opened, while one that fails on an error tries to move its files back. And where atomic move is
unavailable it stops before the swap rather than risk a half-moved world.

The client does not grey out a world that needs the upgrade — it relabels
the button. `LevelSummary.primaryActionMessage` turns Play into *Upgrade and
Play* while leaving it active; what is disabled is Edit and Recreate, which
would otherwise touch a directory the fixer is about to rearrange.

## Telemetry writes to disk before it writes to the network

**`net/minecraft/client/telemetry`**, client-only. Exactly seven event
types: world loaded, world unloaded, graphics capabilities (which now
carries the backend name and the reason a backend failed — see
[Blaze3D](../rendering/blaze3d.md)), and four opt-in ones covering
performance metrics, world load times, advancements and game load times.
`TelemetryProperty` is the vocabulary; each property carries both an
internal name and an export key.

Opting out is two-tier, and the game controls only one of the tiers.
`Minecraft.allowsTelemetry` reads an *account-level* flag the game only
reports; the in-game control only chooses whether the four opt-in events
are sent, and is only offered when the account carries the flag that allows
it. Everything sent is **also written locally** as a JSON event log with a
seven-day expiry — and the send waits on the log opening, so a log that
cannot be opened suppresses the send. A player can read their own outgoing
telemetry, though not in the game: the telemetry screen renders the
*catalogue* of event types and their properties, and a button next to it
opens the log directory in the platform's file manager.

Start at `ClientTelemetryManager`, `TelemetryEventType`.

## Four profiling systems, and Tracy is the surprise

**`net/minecraft/util/profiling`** holds four profiling systems. Two sit in
the package itself — the tick profiler and the Tracy bridge — and two in
subpackages of it, *jfr* and *metrics*.

The **tick profiler** is the familiar one: `Profiler` is a thread-local
holder of a `ProfilerFiller`, `ActiveProfiler` records the push/pop tree of
named sections that pages in this book quote, and `/perf` and the client's
F3 profiler chart drive it.

**Tracy** is the surprise, and it is one class bridging out to Mojang's
Tracy binding. `TracyZoneFiller` implements the same interface, and
`Profiler.get` falls back to the Tracy filler rather than the inactive one
when Tracy is available — and `Profiler.decorateFiller` *combines* the two,
so an attached Tracy build and a running `/perf` both see every section. With a Tracy build attached, every profiler section in the game
streams out with no command run. Tracy reaches outside this package too,
into Blaze3D's frame capture, into the GPU abstraction's `TracyGpuProfiler`
and into the executor wrappers.

**JFR** (`util/profiling/jfr`) registers ten custom flight-recorder events
under a Minecraft category — chunk generation, region reads and writes,
packets sent and received, network summaries, server tick time, client FPS,
structure generation, world load. Packet events are emitted straight from
the packet codecs, so a recording gives a per-packet-type byte breakdown
that this book's [packet reference](../../reference/packets.md) cannot.
Start with *--jfrProfile* or `/jfr start`.

**Metrics** (`util/profiling/metrics`) is `/perf`: sampling by nine
`MetricCategory` values — pathfinding, event loops, consecutive executors,
the tick loop, JVM, chunk rendering, chunk-rendering dispatch, CPU and GPU —
written out as CSVs that `PerfCommand` zips.

## The management server is not RCON

**`net/minecraft/server/jsonrpc`**, dedicated server only, and genuinely
new. It is JSON-RPC 2.0 over a WebSocket, served by its own Netty bootstrap
with an HTTP codec, an authentication handler, the WebSocket handshake and
optional TLS. It is disabled by default; when enabled, TLS is on unless
explicitly turned off, and the server refuses to start without a
forty-character alphanumeric secret, generating one if absent.

What it exposes is the administrator's surface, not the game's: allow-list,
bans and IP bans, players and kicks, operators, game rules, server status,
save and stop, system messages, and a family of live server settings —
including the idle-pause window, whose behaviour belongs to
[the server tick](../server/server-tick.md#an-empty-server-stops-ticking),
because a dedicated server pauses too.
Implementations sit behind service interfaces so the wire layer never
touches the server object directly, and an executor service marshals calls
onto the server thread.

The description of the API cannot drift from the handlers, because it is
derived from them: every method is registered with a description and typed
parameter and response schemas, and a discovery method returns an
**OpenRPC 1.3.2** document built by walking the two method registries and
filtering on a per-method discoverable flag. There is also an outgoing
direction for server-initiated notifications. The audience is panel and
hosting operators.

Start at `JsonRpc`, `ManagementServer`.

## RCON, query, and the pre-1.7 ping that removes itself

**`net/minecraft/server/rcon`** is seven classes of pre-Netty blocking
socket code on its own threads. `RconThread` accepts the connections and
`RconClient` speaks Valve's Source RCON framing; commands execute as a `RconConsoleSource`, a command source that
accumulates output into a string rather than a chat feed
([Brigadier and commands](../commands/brigadier-and-commands.md)).
`QueryThreadGs4` speaks the GameSpy4 UDP query protocol with a
challenge-token handshake and a five-second cache on its full-status reply.

The **pre-1.7 ping is not in that package**. `LegacyQueryHandler` sits in
the server's network package and is installed into the Netty pipeline
*before* the length-prefix splitter and the packet codec, right after the
read timeout ([the connection](../networking/the-connection.md)). It peeks
at the first byte; if it is the legacy ping marker it answers in the old
format and closes, and otherwise it resets the reader index, **removes
itself from the pipeline**, and re-fires the bytes downstream. It costs one
byte comparison per connection and then vanishes. The same encoding is used
client-side so the server list can still ping ancient servers.

## Realms is a client for a server nobody here can read

**`com/mojang/realmsclient`**, client-only, 137 files and 14,701 lines —
more lines than the whole packet catalogue in `network/protocol`. Roughly
sixty per cent is screens and the records behind them — subscriptions, world
slots, templates, invites, backups, minigames, upload and download — and the
rest is a task framework, the world-upload pipeline and the HTTP layer, a
list of REST paths with a small request wrapper. `net/minecraft/realms` is
three classes and a *package-info.java* vanilla keeps for Realms, `RealmsScreen`
among them, the base the Realms screens extend; beyond it the Realms UI extends
ordinary vanilla screens and widgets.

Out of scope because it is a service client: its behaviour is defined by a
server this book cannot read. One fact anyway. The environment is chosen
from an environment variable falling back to a system property, defaulting
to production, in a static final field of the release client — and there are
three environments, not two, because the third points at *localhost*.

## Statistics, the scoreboard, and the recipe book

**`net/minecraft/stats`** is nine classes covering two concerns, plus a link
into a third package that is the reason it is worth a paragraph.

**Statistics**: `Stats` declares eight registry-backed stat types — mined,
crafted, used, broken, picked up, dropped, killed, killed by — plus a
custom type holding the seventy-odd hand-declared counters (play time,
distances by every mode of travel, damage dealt and blocked), each bound to
a formatter that affects display only. A stat type is a lazily-populated
map over a registry, so stat objects are interned; `ServerStatsCounter`
adds the per-player file and a dirty set, and only dirty stats are sent.
Statistics are one of **two** parts of the save that go through the data
fixer as *JSON* rather than NBT — the other is advancement progress
([advancements](../commands/advancements.md)), and they are the only two.

**The scoreboard link** is why the package is worth a paragraph — and note
that the class doing the linking is not in it: `ObjectiveCriteria` lives in
`net/minecraft/world/scores/criteria`, which is why a scoreboard objective
can name a statistic and why this package is reachable from a command at all
([scores, teams and stored data](../commands/scoreboard-and-data.md#what-a-criterion-can-be-which-is-nearly-anything)
is how the name is parsed).

**The recipe book** is the second concern, and it is in this package for
historical reasons rather than architectural ones — `RecipeBook`,
`RecipeBookSettings` and `ServerRecipeBook` are not skipped, they belong to
[recipes](../items/recipes.md), with [advancements](../commands/advancements.md)
reaching in from the other side. The address is the only thing surprising
about them.

## Two packages nobody will recognise

**`net/minecraft/gizmos`** is a **debug-drawing API**, in the game-engine
sense of the word: the immediate-mode "draw me a box in the world for one
frame" facility most engines have and Minecraft did not. Every one of the
debug renderers — chunk borders, hitboxes, pathfinding, brains, points of
interest, raids, light sections — is now written against it, and it is not
client-only, which is the surprise. It is taught where its output is, in Part
X, by [debugging the running
game](../client/debugging-the-running-game.md#a-renderer-does-not-draw-a-gizmo-it-appends-one);
the address is what belongs here, because a reader hunting for the debug
renderers' drawing code will look under `client/renderer/debug` and find
nothing that draws.

**`net/minecraft/references`** is not "references" in the data-fixer sense.
It is a set of **id-constant tables**, and the split is not the one the
package names suggest: `BlockIds` holds the keys for blocks with **no item
form** (water, lava, wall torches, piston heads, wall signs), `ItemIds` the
items with no block, and `BlockItemIds` — seven times `BlockIds` and not
quite twice `ItemIds` — the pairs. Look for stone in `BlockIds` and it is not there. They exist to break
a class-initialisation cycle: exactly **twelve** files outside the package
name it, and four of them are the ones that need to name a block or item
*before* the block and item classes are loaded — `Blocks` and `Items`
themselves, and `GrassBlock` and `MyceliumBlock`, which name another block
during that initialisation — while `PotDecorations` looks its brick up by key.
The other seven are data generators that work in keys: four tag providers, a
tag appender and two feature bootstraps, `AquaticFeatures` and
`NetherFeatures`. A resource key is
a registry plus an [identifier](../foundations/identifiers-and-registries.md), so it can be
built with nothing loaded. Practically, it is the canonical machine-readable
list of *block and item* ids, and a better starting point than the block and
item holder classes if that is what you want — but not the id list: five
sibling tables for entity types, block-entity types, potions, fluids and
atlases live outside the package, in the trees they belong to.

## The data generators, and why "data-driven" is both true and misleading

Most of **`net/minecraft/data`** is a build-time program: a second entry
point with its own options, a generator that groups providers into packs,
and a hash cache that skips unchanged files. `net/minecraft/client/data` is
its client half, generating block and item models, the atlas definitions,
equipment assets and waypoint styles.

The significance is a genuine paradox worth stating plainly. **Vanilla's own
content is a data pack.** `net/minecraft/data/worldgen` is most of the
vanilla worldgen data pack written as Java — the biome feature lists, the
material rules, the carvers, the jigsaw pools, the structures and structure
sets, the processor lists — and the loot, recipe,
tag and advancement packages do the same for their domains, all serialised
through the *same* codecs the game uses to read a pack.

So "Minecraft is data-driven" is true: the running game only ever sees JSON
parsed by codecs, with no vanilla-specific path
([the resource system](../foundations/resource-system.md)). And "you cannot
change it without a data pack" is *nearly* true — which is the more useful
statement, because the exceptions are load-bearing and a reader who believes
the absolute version will misread three other pages.

**The package is not build-time only, and the dedicated server ships all 174 files of it.** Three kinds of exception:

- **Plain id tables.** `AtlasIds` is read at runtime by the model manager,
  the atlas manager, the map, sky, painting and particle renderers, and by a
  chat component. Nothing build-time about it.
- **The bootstrap interface itself.** `BootstrapContext` — in
  `net/minecraft/data/worldgen` — is what every vanilla data-pack registry's
  bootstrap is written against, from damage types and enchantments to chat
  types, dialogs and world clocks. It is the most-imported type in the
  package by a wide margin.
- **Constants and math the running game calls.** `Blocks` itself names
  `TreeFeatures` keys while constructing mushroom and fungus blocks, and a
  `CaveFeatures` key and a `VegetationFeatures` key for the moss and pale moss
  blocks; `MinecraftServer` reaches for a
  `MiscOverworldFeatures` key for the bonus chest; a jigsaw block entity
  defaults to a `Pools` key; `NoiseRouterData` and `NoiseGeneratorSettings`,
  both shipped worldgen classes, are compiled against `TerrainProvider` and the
  material rules in `net/minecraft/data/worldgen/material`; and the F3 screen's
  biome-builder line calls `NoiseRouterData.peaksAndValleys`, one line that delegates
  straight into `TerrainProvider` ([density functions](../worldgen/density-functions.md)).

Vanilla's density functions and noise settings still reach the running game
as JSON. `NoiseRouterData.bootstrap` and `NoiseGeneratorSettings.bootstrap`
are collected by `VanillaRegistries`, which the data-generator entry point
runs and which `Commands.validate` borrows for its ambiguity check; the game
itself reads the generated files out of the built-in pack. Editing
`TerrainProvider` changes terrain by changing what that generator writes.

So `net/minecraft/data` holds a build-time program *and* a handful of tables
and functions the shipped game compiles against and executes. The generator
half is inert at runtime but for one static helper `StructureTemplateManager`
borrows from `NbtToSnbt`, and it is the half worth reading — it is
the fastest way to understand what a vanilla biome or structure declares,
because it is typed and cross-referenced where the JSON is not, a point
[biomes](../worldgen/biomes.md) and
[structure placement](../worldgen/structure-placement.md) both depend on. And the report
providers are how you get machine-readable dumps of the registries and the
packets, two of the tables this book's own
[reference layer](../../reference/README.md) covers.

## The audio backend lives in Blaze3D, and is not skipped

**`com/mojang/blaze3d/audio`** is hatched for its *address*, like
`net/minecraft/gizmos` above: the book teaches what it does and the atlas
still counts it outside every part, because it is filed where nobody looks
for it. It wraps OpenAL, and
it sits inside Blaze3D, beside the window and `RenderSystem`, rather than in the
client's sound package where the engine, the manager, the channel bookkeeping
and the Ogg decoding live. That is the boundary fact: Blaze3D is the platform
layer for both devices, not only the graphics one, and a reader looking for
the sound code under `client/sounds` will not find the half that talks to the
driver. Everything the package does — the device and context, the channel
limits (which are counters and not pools, as that page's own heading insists),
binaural rendering through `Options.directionalAudio`, hot-plugging a headset
mid-game — is taught, in Part X, by [the sound
engine](../client/sound-engine.md#the-channel-limits-are-counters-not-pools).

## Player reporting

**`net/minecraft/client/multiplayer/chat/report`**, client-only.
`ReportingContext` holds the sender, the environment (which server or
realm), a log of the last thousand-odd received messages, and at most one
draft report. There are three report kinds — chat, skin, name — and an
eleven-value reason enum.

The piece worth naming is the context builder: a chat report does not send
just the offending line, it walks the log backwards to assemble surrounding
**signed** context, which is what makes the report verifiable at the other
end. The report machinery is the consumer of the chat-signing system that
[chat and signing](../networking/chat-and-signing.md) documents. Neither the
transport nor the policy is in the game — both come from the account
service library.

## Gaps, and the ruling on each

The hatched boxes above are the boundary as drawn. Beside them sits a
shorter list of things that were never excluded on principle — they were
simply not written when the book reached them, and each has since been
ruled on. **Ten are now taught**, either as a page of their own
(`net/minecraft/gametest`, `com/mojang/blaze3d/platform`, the post-effect
chains, the scoreboard and command storage) or as a section of one (the
debug cluster across the HUD and debugging pages, item models on models and
atlases, the packrat parser on Brigadier and on codecs, the animation
framework on entity rendering, the pack classes on the resource system, and
`net/minecraft/client/resources`, which turned out to be five systems with
five owners rather than one gap). Naming where each landed is the landing
pages' job, not this one's; what belongs here is the other ruling.

**Declined, with the reason.** A decline is a promise that a reader will not
miss it, not a shrug.

| what | size | why | what carries it instead |
|---|---|---|---|
| `com/mojang/renderpearl/backend/vulkan` | 33 files, 7,387 lines | a faithful second implementation of an interface already documented, and the abstraction is the lecture | [Blaze3D](../rendering/blaze3d.md) |
| `net/minecraft/client/data` | 28 files, 6,189 lines | build-time model, atlas, equipment and waypoint generators, the same category as the generator half of `net/minecraft/data`, but big enough that a reader trips over it | named here and in the list of *main* methods on [anatomy](anatomy.md#from-main-to-a-world) |
| the catalogues | ~140 entity models, ~80 particles, 102 render states, 50 render layers, 16 animation definitions, 56 of 58 worldgen features, 57 tree kits, the entity sub-predicates | each is one shape repeated, and the shape is on the page that owns the framework | [the reference layer](../../reference/README.md) |
| `client/quickplay`, `client/profiling`, `client/renderer/gizmos` | one or two classes each | no mechanism a lecture needs | — |
| `net/minecraft/data/worldgen` as content | 64 files, 6,016 lines | declined *as content*: it is the datagen bootstrap that emits vanilla's JSON | the runtime exceptions named above, which are not a decline |
| `net/minecraft/client/animation`'s keyframe definitions | 16 of its 21 classes | pure data in Java clothing — and *lines* is the wrong unit for it: 266 lines and 665 KB, one file's longest line thirty thousand characters, because the decompiler renders each animation as one builder chain | [entity rendering](../rendering/entity-rendering.md) has the framework |

Two things inside `com/mojang/renderpearl/backend/vulkan` are named before
the decline rather than after it: `DestructionQueue`, the deferred-free
discipline OpenGL needs no equivalent of, which is the clearest illustration
of what the device seam hides, and `vulkan/checkpoints`, vendor breadcrumb
extensions for GPU crash reports. The shader compiler is not in the declined
tree. `GlslCompiler` and `SPIRVModule`, the shaderc and spirv-cross pair, sit
in front of both backends in `renderpearl/frontend/shaders`, because
Minecraft still authors GLSL and compiles it to SPIR-V once — Vulkan takes
the SPIR-V as it is and OpenGL cross-compiles it back to GLSL — which is the
whole reason one shader source can feed two backends. The interiors of
`com/mojang/renderpearl/backend/opengl` are declined on the same grounds.

**Named, and not yet written.** These are real systems with real lectures
in them, and no ruling above covers them: the carver tunnel walk; the dragon
fight (`EnderDragonFight`); `client/multiplayer`'s joining-a-server tail; and
two corners of the pack system that
[the resource system](../foundations/resource-system.md) names without teaching — the
server-resource-pack prompt and download flow in `client/resources/server`,
and the *linkfs* synthetic file system that presents the launcher's hash-named asset files as the one tree their index describes. Beside them sit the maps' saved data and the wandering trader's timer, which the [level data](../../reference/level-data-and-rules.md) table names and no page teaches, four Part V mechanisms its landing page does not list: rails, the shelf, the beehive and fire spread; local difficulty (`DifficultyInstance`), which only that table's page explains; and four things a player carries that Part VIII lists and does not teach — the attack's visual effects, the damage statistics, the warden-spawn tracker and the spectator camera behind */spectate*. They are
named here so that a reader who wants one knows the book knows it is
missing, and knows where to start.

## Where to look

If you need one of these the entry points are named in each section; if you
want a *list* rather than a system, start at `net/minecraft/references` for
ids and the report providers in `net/minecraft/data` for everything else,
and the [atlas](../../maps/packages.md) for the shape of the whole jar.

---

*Rules: names, never code · how the system works, not how the code reads ·
newest version only · every backticked name passes `tools/verify_names.py`.*
