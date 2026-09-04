# What this book skips

> Verified against **Minecraft 26.2** · Part I · A reader opens the atlas, sees a dozen boxes hatched, and asks what is in them and why they are not taught.

Open the atlas and part of the jar is drawn hatched. That hatching is this
page. Java Minecraft is 7,055 classes and 719,302 lines, and the parts do
not reach all of it. Some of what is left out is excluded on purpose by
[rule three](../../introduction.md) — save migration is version-difference
code, and a book that documents only the current version has nothing to say
about it. Some is out of scope because it is a client for a service this
book cannot read. And one hatched box is not skipped code so much as skipped
*ground*: `net/minecraft/data` is the program that writes vanilla's own
content as a data pack, it ships in the dedicated server jar — all 163
classes of it — and the running game compiles against it and calls into it.
`Blocks` names `TreeFeatures` keys while it constructs mushroom blocks;
`MinecraftServer` reaches for a `MiscOverworldFeatures` key for the bonus
chest; the F3 screen's biome line runs through
`NoiseRouterData.peaksAndValleys` into `TerrainProvider`. The boundary this
page draws is honest, and part of drawing it honestly is showing where it
leaks.

<figure class="map">
{{#include ../../generated/packages-treemap.svg}}
<figcaption>The jar by package, area by lines of decompiled source. Hatched boxes are the packages this page tours and the parts do not. Click to enlarge.</figcaption>
</figure>

## The sizes, and which jar ships them

Each entry below says what the thing is, roughly how big it is, whether the
dedicated server ships it, one fact worth knowing, and where to start
reading. The treemap deliberately does not hatch `net/minecraft/gametest`:
Part XIII covers it, so it is a gap that closed rather than a skip. The
counts in the table are files, so a *package-info.java* counts as a class
there and not in the prose below.

| package | classes | lines | side |
|---|---:|---:|---|
| `net/minecraft/util/datafix` | 396 | 26,372 | both |
| `net/minecraft/util/filefix` | 57 | 3,544 | both |
| `net/minecraft/client/telemetry` | 18 | 1,221 | client |
| `net/minecraft/util/profiling` | 70 | 4,260 | both |
| `net/minecraft/server/jsonrpc` | 65 | 4,094 | dedicated server |
| `net/minecraft/server/rcon` | 9 | 839 | dedicated server |
| `com/mojang/realmsclient` | 127 | 13,217 | client |
| `net/minecraft/realms` | 4 | 203 | client |
| `net/minecraft/stats` | 10 | 873 | both |
| `net/minecraft/gizmos` | 15 | 569 | both |
| `net/minecraft/references` | 5 | 1,434 | both |
| `net/minecraft/data` | 163 | 15,587 | both — see below |
| └ `net/minecraft/data/worldgen` | 56 | 5,369 | both — see below |
| `net/minecraft/client/data` | 28 | 6,176 | client |
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
body is the migration history of the game written out longhand: three
hundred schema registrations and four hundred-odd fixes, from schema 99 up
to the current world version. The rewriting machinery itself is Mojang's
external DataFixerUpper library; what lives here is the vanilla catalogue —
`util/datafix/schemas` describing the *shape* of the data at each version,
and `util/datafix/fixes` doing the individual rewrites.

A version number becomes a chain of fixes through `DataFixTypes`, an enum
of about thirty type references (level, chunk, player, entity chunk, POI
chunk, options, stats, advancements, and a long tail of saved-data kinds).
`DataFixTypes.updateToCurrentVersion` takes the data version as an
argument — every one of its thirteen callers reads the version itself — and
asks the fixer to compose every rule from there to now.
`DataFixTypes.wrapCodec` is the one that reads the version *out of the tag*:
it wraps an ordinary codec so decoding pulls the data version, runs the
chain, and encoding stamps the current version back in. It is the rarer
door — two callers, `PlayerAdvancements` and `DebugScreenEntryList` — while
[chunk storage](../world/chunk-storage.md) and player data take the first
one and read the version themselves. The rules are
pre-compiled on a dedicated bootstrap thread, and that thread is built with
some care to cost nothing: one thread, daemon, at minimum priority, with a
single caller in the client's entry point, optimising exactly one type (the
level-summary schema, so the world list opens fast). The dedicated server
never asks for it at all.

**`net/minecraft/util/filefix`** does what the other cannot. A data fixer
rewrites the *contents* of a tag after it has been read, so it can never
move, rename, split or delete a file. `FileFixerUpper` operates on the
world **directory**: its operations are moves, regex moves, group moves,
deletions, content modifications and one composite that scopes a nested list
of operations to matching folders, and the concrete fixes do things like
relocate dimension storage, split player storage and pull data out of
*level.dat* into saved data
([level data and rules](../../reference/level-data-and-rules.md)).

It stays safe by working somewhere else: the whole upgrade runs against a
**custom copy-on-write file system** rooted at a scratch directory, and the
result is swapped in at the end. Exactly how safe depends on the filesystem
underneath. Where hard links are available it uses them. Where they are not,
it writes one file, *upgrade_in_progress.json*, recording the moves, and an
interrupted upgrade resumes from it while an aborted one reverts. And where atomic move is
unavailable it refuses to run at all rather than risk a half-moved world.

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
internal name and a different export key.

Opting out is two-tier and neither tier is a plain checkbox.
`Minecraft.allowsTelemetry` reads an *account-level* flag the game only
reports; the in-game control only chooses whether the four opt-in events
are sent, and is only offered when the account carries the flag that allows
it. Everything sent is **also written locally** as a JSON event log with a
seven-day expiry — and the send is nested *inside* the log write, so a
failed log suppresses the send. A player can read their own outgoing
telemetry, though not in the game: the telemetry screen renders the
*catalogue* of event types and their properties, and a button next to it
opens the log directory in the platform's file manager.

Start at `ClientTelemetryManager`, `TelemetryEventType`.

## Four profilers, two of them in this package

**`net/minecraft/util/profiling`** holds four profiling systems, though
only two of them are self-contained here.

The **tick profiler** is the familiar one: `Profiler` is a thread-local
holder of a `ProfilerFiller`, `ActiveProfiler` records the push/pop tree of
named sections that every page in this book quotes, and `/debug start`
drives it.

**Tracy** is the surprise, and it is one class bridging out to Mojang's
Tracy binding. `TracyZoneFiller` implements the same interface, and
`Profiler.get` falls back to the Tracy filler rather than the inactive one
when Tracy is available — and `Profiler.decorateFiller` *combines* the two,
so an attached Tracy build and a running `/debug start` both see every
section. With a Tracy build attached, every profiler section in the game
streams out with no command run. Tracy reaches outside this package too,
into Blaze3D's frame capture and GPU profiler and into the executor
wrappers.

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
including the idle-pause window, whose actual behaviour is documented in
[anatomy](anatomy.md), because a dedicated server pauses too.
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
socket code on its own threads. `RconThread` speaks Valve's Source RCON
framing; commands execute as a `RconConsoleSource`, a command source that
accumulates output into a string rather than a chat feed
([Brigadier and commands](../commands/brigadier-and-commands.md)).
`QueryThreadGs4` speaks the GameSpy4 UDP query protocol with a
challenge-token handshake and a five-second response cache.

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

**`com/mojang/realmsclient`**, client-only, 127 classes and 13,217 lines —
about the size of the whole packet catalogue in `network/protocol`. Roughly
sixty per cent is screens and the records behind them — subscriptions, world
slots, templates, invites, backups, minigames, upload and download — and the
rest is a task framework, the world-upload pipeline and the HTTP layer, a
list of REST paths with a small request wrapper. Three classes and a
*package-info.java* in `net/minecraft/realms` are the only part of vanilla
the Realms UI extends.

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
`net/minecraft/world/scores/criteria`
([scores, teams and stored data](../commands/scoreboard-and-data.md)).
It parses a criterion name containing a colon by looking the left half up in
the stat-type registry and the right half in *that stat type's* registry,
then wrapping the resulting stat as a criterion. So
*minecraft.mined:minecraft.stone* is not a special case — it is the
statistics registry addressed through a string.

**The recipe book** is the second concern, here for historical reasons
rather than architectural ones: `RecipeBook`, `RecipeBookSettings` and
`ServerRecipeBook`, which [recipes](../items/recipes.md) and
[advancements](../commands/advancements.md) both reach into.

## Two packages nobody will recognise

**`net/minecraft/gizmos`** is a **debug-drawing API**, in the game-engine
sense of the word: the immediate-mode "draw me a box in the world for one
frame" facility most engines have and Minecraft did not. `Gizmos` is a
static façade over a thread-local `GizmoCollector`; calling a shape method
outside a collector scope throws. The shapes are small records; a style is
a stroke and fill; the returned handle can pin a shape on top, persist it
for a duration or fade it out.

Every one of the debug renderers — chunk borders, hitboxes, pathfinding,
brains, points of interest, raids, light sections — is now written against
it. The part that surprises is that it is **server-side too**: there are
four collectors — three on the client (per-tick, the extract pass, the
render thread) and one on the integrated server, which wraps its whole
packet-and-tick step in a collector scope and publishes the result for the
client to drain. Server tick code can draw into the singleplayer world; a
dedicated server installs no collector at all, so the same calls there would
throw. A headless test server installs a no-op collector so the same calls
cost nothing.

**`net/minecraft/references`** is not "references" in the data-fixer sense.
It is a set of **id-constant tables**, and the split is not the one the
package names suggest: `BlockIds` holds the keys for blocks with **no item
form** (water, lava, wall torches, piston heads, wall signs), `ItemIds` the
items with no block, and `BlockItemIds` — seven times `BlockIds` and not
quite twice `ItemIds` — the pairs. Look for stone in `BlockIds` and it is not there. They exist to break
a class-initialisation cycle: exactly **ten** files outside the package name
it, and they are precisely the ones that need to name a block or item
*before* the block and item classes are loaded — `Blocks` and `Items`
themselves, `GrassBlock` and `MyceliumBlock`, which name another block
during that initialisation, `DecoratedPotPatterns` beside them, and the five
tag providers. A resource key is a registry plus
an [identifier](../foundations/identifiers-and-registries.md), so it can be
built with nothing loaded. Practically, it is the canonical machine-readable
list of *block and item* ids, and a better starting point than the block and
item holder classes if that is what you want — but not the id list: five
sibling tables for entity types, block-entity types, potions, fluids and
atlases live outside the package, in the trees they belong to.

## The data generators, and why "data-driven" is both true and misleading

Most of **`net/minecraft/data`** is a build-time program: a second entry
point with its own options, a generator that groups providers into packs,
and a hash cache that skips unchanged files. `net/minecraft/client/data` is
its client half, generating block and item models and the atlas definitions.

The significance is a genuine paradox worth stating plainly. **Vanilla's own
content is a data pack.** `net/minecraft/data/worldgen` is the entire
vanilla worldgen data pack written as Java — the biome feature lists, the
surface rules, the noise settings, the carvers, the jigsaw pools, the
structures and structure sets, the processor lists — and the loot, recipe,
tag and advancement packages do the same for their domains, all serialised
through the *same* codecs the game uses to read a pack.

So "Minecraft is data-driven" is true: the running game only ever sees JSON
parsed by codecs, with no vanilla-specific path
([the resource system](../foundations/resource-system.md)). And "you cannot
change it without a data pack" is *nearly* true — which is the more useful
statement, because the exceptions are load-bearing and a reader who believes
the absolute version will misread three other pages.

**The package is not build-time only, and the dedicated server ships all 163
classes of it.** Three kinds of exception:

- **Plain id tables.** `AtlasIds` is read at runtime by the model manager,
  the atlas manager, the map, sky, painting and particle renderers, and by a
  chat component. Nothing build-time about it.
- **The bootstrap interface itself.** `BootstrapContext` — in
  `net/minecraft/data/worldgen` — is what every vanilla registry bootstrap in
  the game is written against, from damage types and enchantments to chat
  types, dialogs and world clocks. It is the most-imported type in the
  package by a wide margin.
- **Constants and math the running game calls.** `Blocks` itself names
  `TreeFeatures` and `CaveFeatures` keys while constructing mushroom and
  fungus blocks; `MinecraftServer` reaches for a `MiscOverworldFeatures` key
  for the bonus chest; a jigsaw block entity defaults to a `Pools` key;
  `NoiseRouterData` and `NoiseGeneratorSettings`, both shipped worldgen
  classes, are compiled against `TerrainProvider` and `SurfaceRuleData`; and
  the F3 screen's biome line calls `NoiseRouterData.peaksAndValleys`, one
  line that delegates straight into `TerrainProvider`
  ([density functions](../worldgen/density-functions.md)).

Vanilla's density functions and noise settings still reach the running game
as JSON. `NoiseRouterData.bootstrap` and `NoiseGeneratorSettings.bootstrap`
are collected by `VanillaRegistries`, which the data-generator entry point
runs and which `Commands.validate` borrows for its ambiguity check; the game
itself reads the generated files out of the built-in pack. Editing
`TerrainProvider` changes terrain by changing what that generator writes.

So `net/minecraft/data` holds a build-time program *and* a handful of tables
and functions the shipped game compiles against and executes. The generator
half really is inert at runtime, and it is the half worth reading — it is
the fastest way to understand what a vanilla biome or structure declares,
because it is typed and cross-referenced where the JSON is not, a point
[biomes](../worldgen/biomes.md) and
[structure placement](../worldgen/structure-placement.md) both depend on. And the report
providers are how you get machine-readable dumps of exactly the tables this
book's own [reference layer](../../reference/README.md) covers.

## The audio backend lives in Blaze3D

**`com/mojang/blaze3d/audio`** wraps OpenAL — and what is worth flagging is
the *location*. The binding sits inside Blaze3D, beside the GPU
abstraction, not in the client's sound package where the engine, the
manager, the channel pool and the Ogg decoding live
([the sound engine](../client/sound-engine.md)). Blaze3D is the platform layer for both
devices, not only the graphics one.

`Library` owns the device and context and splits a default thirty channels
into static and streaming pools; a `Channel` is one source, with either a
whole buffer or a small streaming queue. Binaural rendering needs the
platform's HRTF extension **and** the Directional Audio option — it is never
switched on behind the player's back. And there is a whole device-hotplug
apparatus with both callback and polling implementations, so plugging in
headphones mid-game moves the audio without a restart. Detecting a device
*disconnect* needs a second extension again.

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

These were never excluded on principle — they were simply not written when
the book reached them. Each carries one of four rulings: **covered** (a page
now owns it), **absorbed** (a paragraph or a section on a page that already
exists), **reframed** (the gap was described wrongly, and the description is
what changed), or **declined** with a reason. A decline is a promise that a
reader will not miss it, not a shrug.

| what | size | ruling | where |
|---|---|---|---|
| `net/minecraft/gametest` | 47 classes, 5,514 lines | covered, which is why the treemap does not hatch it | [game tests](../commands/game-tests.md) |
| the debug cluster | four packages' worth | covered: the F3 entry registry, and the server-push subscriptions, sample loggers and debug renderers | [the HUD](../client/hud.md), [debugging the running game](../client/debugging-the-running-game.md) |
| `com/mojang/blaze3d/platform` | 29 classes, 3,896 lines | covered | [the window](../rendering/the-window.md) |
| `PostChain`, `PostChainConfig`, `PostPass`, `UniformValue` | 4 classes, 996 lines, and six shipped chains | covered — it was the only place in the game where user-authored shaders are first class | [post-processing](../rendering/post-processing.md) |
| `net/minecraft/client/renderer/item`, its item-properties subtree included | 63 classes | covered as a section rather than a page: the trace starts at an `ItemStack` but everything it touches is Part XI's | [models and atlases](../rendering/models-and-atlases.md#how-an-item-picks-its-model) |
| the scoreboard, teams and command storage | 32 classes, ~3,830 lines | covered — it was the largest coherent system in the book with no page at all | [scores, teams and stored data](../commands/scoreboard-and-data.md) |
| `net/minecraft/util/parsing` | 29 classes, 1,879 lines | absorbed — Mojang's own packrat parser-combinator framework, and the question it answers, why the client can complete mid-token, is that page's question | [Brigadier and commands](../commands/brigadier-and-commands.md), and [codecs, NBT and JSON](../foundations/codecs-nbt-json.md) for its largest consumer, the SNBT reader |
| `net/minecraft/client/animation` | 23 classes, 509 lines | absorbed for its five framework classes, declined for the sixteen pure-keyframe definitions | [entity rendering](../rendering/entity-rendering.md) |
| `net/minecraft/server/packs` | 55 classes, 4,975 lines | absorbed — mostly covered already, two corners owed a sentence each | [the resource system](../foundations/resource-system.md) |
| `net/minecraft/client/resources` | 101 classes, 7,612 lines | reframed — it is not one system, and five pages own its parts | [models and atlases](../rendering/models-and-atlases.md), [what makes a sound happen](../client/what-makes-a-sound.md), [entity rendering](../rendering/entity-rendering.md), [the HUD](../client/hud.md), [the resource system](../foundations/resource-system.md) |
| `com/mojang/blaze3d/vulkan` | 40 classes, 7,477 lines | declined — a faithful second implementation of an interface already documented, and the abstraction is the lecture | [Blaze3D](../rendering/blaze3d.md) |
| `net/minecraft/client/data` | 28 classes, 6,176 lines | declined — build-time model and atlas generators, the same category as the generator half of `net/minecraft/data`, but big enough that a reader trips over it | named here and nowhere else |
| the catalogues | ~230 mob models, ~73 particles, 101 render states, 50 render layers, 16 animation definitions, 61 of 63 worldgen features, 50 tree kits, the entity sub-predicates | declined — each is one shape repeated, and the shape is on the page that owns the framework | [the reference layer](../../reference/README.md) |
| `client/quickplay`, `client/profiling`, `client/renderer/gizmos` | a few classes each | declined — no mechanism a lecture needs | — |
| `net/minecraft/data/worldgen` as content | 52 classes, 5,353 lines | declined *as content*: it is the datagen bootstrap that emits vanilla's JSON | the runtime exceptions named above, which are not a decline |

Three of those rows need a sentence more. `client/animation` comes with a
warning owed to anyone who measures it, because *lines* is the wrong unit
for that package: 509 lines and 674 KB, with one file whose single longest
line is thirty thousand characters, because the decompiler renders each
animation as one builder chain. Four things inside `blaze3d/vulkan` are not
backend detail and are named before the decline — `GlslCompiler` and the
`vulkan/glsl` shaderc and spirv-cross pair, because Minecraft still authors
GLSL and cross-compiles it to SPIR-V, which is the whole reason one shader
source can feed two backends; `DestructionQueue`, the deferred-free
discipline OpenGL needs no equivalent of, which is the clearest illustration
of what the device seam hides; and `vulkan/checkpoints`, vendor breadcrumb
extensions for GPU crash reports. The interiors of `blaze3d/opengl` are
declined on the same grounds.

The `client/resources` reframing is the third. The old entry called it "the
client reload" with "no page owning the client half end to end", and that
overstates it: models and atlases, sound instances, skins, waypoint styles,
and the pack source, splashes, language and metadata all have owners. What
no page walks is the client *reload* as one sequence, which is a question
about the shape of the documentation rather than a hole in it. The one
substantively uncovered corner is `client/resources/server`, the
server-resource-pack prompt and download flow — and it pairs with the two
corners of `net/minecraft/server/packs` that the resource-system page owes a
sentence each: *linkfs*, a synthetic read-only file system that lets a
development checkout's scattered directories present as one pack root, and
`DownloadQueue` with `DownloadCacheCleaner`, the server-resource-pack
download queue and its cache eviction.

**Named for a later pass to place.** These are real systems with real
lectures in them, found by the coverage sweeps and not written:
the carver tunnel walk; the dragon fight
(`EnderDragonFight`); the advancements screen; and `client/multiplayer`'s
joining-a-server tail. Each is recorded with a size and a recommendation in
the coverage queue in the project's restructuring notebook.

## Where to look

If you need one of these the entry points are named in each section; if you
want a *list* rather than a system, start at `net/minecraft/references` for
ids and the report providers in `net/minecraft/data` for everything else,
and the [atlas](../../maps/packages.md) for the shape of the whole jar.

---

*Rules: names, never code · how the system works, not how the code reads ·
newest version only · every backticked name passes `tools/verify_names.py`.*
