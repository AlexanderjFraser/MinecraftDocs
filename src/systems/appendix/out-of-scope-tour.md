# The out-of-scope tour

> Verified against **Minecraft 26.2** · Part XIII · No trace — a map of what this corpus does not cover: what each subsystem is, why it is skipped, and the two or three class names to start at if you need it anyway.

## Responsibility

Fifty-six pages cover the game. The jar contains 7,055 classes and 719,302
lines, and the pages do not reach all of it. Some of what is left out is
excluded on purpose by [rule three](../../introduction.md) — save migration
is version-difference code, and a corpus that documents only the current
version has nothing to say about it. Some is out of scope because it is a
client for a service this corpus cannot read. And some is simply a gap: a
real subsystem that no page owns, which the closing pass should either
absorb or explicitly decline.

This page draws the boundary honestly. Each entry says what the thing is,
roughly how big, whether the dedicated server ships it, one fact worth
knowing, and where to start reading.

The oracle for "server or client" throughout is the list of classes the
dedicated server jar ships, which lives beside the decompile.

## The sizes

| package | classes | lines | side |
|---|---:|---:|---|
| `net/minecraft/util/datafix` | 396 | 26,372 | both |
| `net/minecraft/util/filefix` | 57 | 3,544 | both |
| `net/minecraft/client/telemetry` | 18 | 1,221 | client |
| `net/minecraft/util/profiling` | 70 | 4,260 | both |
| `net/minecraft/server/jsonrpc` | 65 | 4,094 | dedicated server |
| `net/minecraft/server/rcon` | 9 | 839 | dedicated server |
| `com/mojang/realmsclient` | 127 | 13,217 | client |
| `net/minecraft/stats` | 10 | 873 | both |
| `net/minecraft/gizmos` | 15 | 569 | both |
| `net/minecraft/references` | 5 | 1,434 | both |
| `net/minecraft/data` | 163 | 15,587 | build-time |
| └ `net/minecraft/data/worldgen` | 56 | 5,369 | build-time |
| `net/minecraft/client/data` | 28 | 6,176 | build-time |
| `com/mojang/blaze3d/audio` | 12 | 1,013 | client |
| `net/minecraft/client/multiplayer/chat/report` | 12 | 952 | client |

## Save migration

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
`DataFixTypes.updateToCurrentVersion` reads the data version out of the tag
and asks the fixer to compose every rule in that range;
`DataFixTypes.wrapCodec` wraps an ordinary codec so decoding runs the chain
and encoding stamps the current version back in. That wrapper is how the
version number reaches the fixer at all — you will see it in
[chunk storage](../world/chunk-storage.md), in player data, and in
[advancements](../commands/advancements.md). Pre-compiling those rules on a
dedicated bootstrap thread is a substantial part of the game's start-up
cost.

**`net/minecraft/util/filefix`** does what the other cannot. A data fixer
rewrites the *contents* of a tag after it has been read, so it can never
move, rename, split or delete a file. `FileFixerUpper` operates on the
world **directory**: its operations are moves, regex moves, group moves,
deletions and content modifications, and the concrete fixes do things like
relocate dimension storage, split player storage and pull data out of
`level.dat` into saved data ([level data and rules](../world/level-data-and-rules.md)).

The interesting part is how it does it safely: the whole upgrade runs
against a **custom copy-on-write file system** rooted at a
scratch directory, and the result is swapped in at the end. An interrupted
upgrade leaves a marker and resumes; an aborted one reverts. The client
greys out a world that needs it.

## Telemetry

**`net/minecraft/client/telemetry`**, client-only. Exactly seven event
types: world loaded, world unloaded, graphics capabilities (which now
carries the backend name and the reason a backend failed — see
[Blaze3D](../client/blaze3d.md)), and four opt-in ones covering performance
metrics, world load times, advancements and game load times.
`TelemetryProperty` is the vocabulary; each property carries both an
internal name and a different export key.

Opting out is two-tier and neither tier is a plain checkbox.
`Minecraft.allowsTelemetry` reads an *account-level* flag the game only
reports; the in-game control only chooses whether the four opt-in events
are sent, and is only offered when the account carries the flag that allows
it. The fact worth knowing: everything sent is **also written locally** as
a JSON event log with a seven-day expiry, and there is a screen that
renders it — a player can read their own outgoing telemetry.

Start at `ClientTelemetryManager`, `TelemetryEventType`.

## Profiling

**`net/minecraft/util/profiling`** holds four distinct profilers.

The **tick profiler** is the familiar one: `Profiler` is a thread-local
holder of a `ProfilerFiller`, `ActiveProfiler` records the push/pop tree of
named sections that every page in this corpus quotes, and `/debug start`
drives it.

**Tracy** is the surprise. `TracyZoneFiller` bridges the same interface into
Mojang's Tracy binding — and `Profiler.getDefaultFiller` returns the Tracy
filler rather than the inactive one when Tracy is available. With a Tracy
build attached, every profiler section in the game streams out with no
command run. Tracy reaches outside this package too, into Blaze3D's frame
capture and GPU profiler and into the executor wrappers.

**JFR** (`util/profiling/jfr`) registers ten custom flight-recorder events
under a Minecraft category — chunk generation, region reads and writes,
packets sent and received, network summaries, server tick time, client FPS,
structure generation, world load. Packet events are emitted straight from
the packet codecs, so a recording gives a per-packet-type byte breakdown
that this corpus's [packet reference](../../reference/packets.md) cannot.
Start with `--jfrProfile` or `/jfr start`.

**Metrics** (`util/profiling/metrics`) is `/perf`: sampling by category —
pathfinding, event loops, ticking, JVM, chunk rendering, CPU, GPU — into a
zip of CSVs.

## The management server

**`net/minecraft/server/jsonrpc`**, dedicated server only, and genuinely
new. It is **not** RCON: it is JSON-RPC 2.0 over a WebSocket, served by its
own Netty bootstrap with an HTTP codec, an authentication handler, the
WebSocket handshake and optional TLS. It is disabled by default and the
server refuses to start without a forty-character secret, generating one if
absent.

What it exposes is the administrator's surface, not the game's: allow-list,
bans, players and kicks, operators, server status, save and stop, system
messages, and a family of live server settings. Implementations sit behind
service interfaces so the wire layer never touches the server object
directly, and an executor service marshals calls onto the server thread.

The fact worth knowing: every method is registered with a description and
typed parameter and response schemas, and a discovery method returns a
machine-readable description of the whole API, generated from the same
builders that register the handlers. There is also an outgoing direction
for server-initiated notifications. The audience is panel and hosting
operators.

Start at `JsonRpc`, `ManagementServer`.

## RCON, query, and the pre-1.7 ping

**`net/minecraft/server/rcon`** is nine classes of pre-Netty blocking
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

## Realms

**`com/mojang/realmsclient`**, client-only, and about as large as this
corpus's whole networking part. Almost all of it is screens and the records
behind them — subscriptions, world slots, templates, invites, backups,
minigames, upload and download. One subpackage is the HTTP layer, a list of
REST paths and a small request wrapper. A four-class shim in
`net/minecraft/realms` is the only part of vanilla the Realms UI extends.

Out of scope because it is a service client: its behaviour is defined by a
server this corpus cannot read. One fact anyway — the environment (staging
or production) is chosen from an environment variable falling back to a
system property, and that switch ships in the release client.

## Statistics, the scoreboard, and the recipe book

**`net/minecraft/stats`** is ten classes covering three concerns.

**Statistics**: `Stats` declares eight registry-backed stat types — mined,
crafted, used, broken, picked up, dropped, killed, killed by — plus a
custom type holding the seventy-odd hand-declared counters (play time,
distances by every mode of travel, damage dealt and blocked), each bound to
a formatter that affects display only. A stat type is a lazily-populated
map over a registry, so stat objects are interned; `ServerStatsCounter`
adds the per-player file and a dirty set, and only dirty stats are sent.
Statistics are the one part of the save that goes through the data fixer as
*JSON* rather than NBT.

**The scoreboard link** is why the package is worth a paragraph.
`ObjectiveCriteria` parses a criterion name containing a colon by looking
the left half up in the stat-type registry and the right half in *that stat
type's* registry, then wrapping the resulting stat as a criterion. So
`minecraft.mined:minecraft.stone` is not a special case — it is the
statistics registry addressed through a string.

**The recipe book** also lives here, for historical reasons rather than
architectural ones: `RecipeBook`, `RecipeBookSettings` and
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
it. The fact worth knowing is that it is **server-side too**: there are
three separate collectors, and the integrated server runs its whole tick
inside a collector scope and publishes the result for the client to drain.
Server tick code can draw into the singleplayer world. A headless test
server installs a no-op collector so the same calls cost nothing.

**`net/minecraft/references`** is not "references" in the data-fixer sense.
It is a set of **id-constant tables**: resource keys for every block, every
item, and the pairing between them. They exist to break a
class-initialisation cycle — only about fifteen files import the package,
and they are exactly the ones that need to name a block or item *before*
the block and item classes are loaded, including those classes themselves
and the tag providers. A resource key is a registry plus an
[identifier](../foundations/identifiers-and-registries.md), so it can be
built with nothing loaded. Practically, it is the canonical machine-readable
list of vanilla ids, and a better starting point than the block and item
holder classes if that is what you want.

## The data generators — and why "data-driven" is both true and misleading

**`net/minecraft/data`** is a build-time program, not part of the game: a
second entry point with its own options, a generator that groups providers
into packs, and a hash cache that skips unchanged files. The client half
generates block and item models.

The significance is a genuine paradox worth stating plainly. **Vanilla's own
content is a data pack.** `net/minecraft/data/worldgen` is the entire
vanilla worldgen data pack written as Java — the biome feature lists, the
surface rules, the noise settings, the carvers, the jigsaw pools, the
structures and structure sets, the processor lists — and the loot,
recipe, tag and advancement packages do the same for their domains, all
serialised through the *same* codecs the game uses to read a pack.

So "Minecraft is data-driven" is true: the running game only ever sees JSON
parsed by codecs, with no vanilla-specific path
([the resource system](../foundations/resource-system.md)). And "you cannot
change it without a data pack" is equally true: these Java classes never
execute at runtime. They are the *source* the shipped JSON was generated
from, and editing them changes nothing.

Reading them is nonetheless the fastest way to understand what a vanilla
biome or structure declares, because it is typed and cross-referenced where
the JSON is not — a point [biomes](../worldgen/biomes.md) and
[structures](../worldgen/structures.md) both depend on. And the report
providers are how you get machine-readable dumps of exactly the tables this
corpus's own [reference layer](../../reference/README.md) covers.

## The audio backend

**`com/mojang/blaze3d/audio`** wraps OpenAL — and the point worth flagging
is the *location*. The binding sits inside Blaze3D, beside the GPU
abstraction, not in the client's sound package where the engine, the
manager, the channel pool and the Ogg decoding live ([sound](../client/sound.md)).
Blaze3D is the platform layer for both devices, not only the graphics one.

`Library` owns the device and context and splits a default thirty channels
into static and streaming pools; a `Channel` is one source, with either a
whole buffer or a small streaming queue. Two facts: binaural rendering is
enabled when the platform extension is present, and there is a whole
device-hotplug apparatus with both callback and polling implementations, so
plugging in headphones mid-game moves the audio without a restart.

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

## Gaps this corpus has not covered

Not excluded on principle — simply not written. The closing pass should
decide for each.

- **`net/minecraft/gametest`** (47 classes) is covered, in
  [dialogs and tests](../commands/dialogs-and-tests.md).
- **`net/minecraft/server/packs`** (55) and **`net/minecraft/client/resources`**
  (101) — the pack repository and the client reload. Split across
  [the resource system](../foundations/resource-system.md) and Part X, with
  no page owning the client half end to end.
- **The debug cluster** (about 91 classes across the debug screen
  components, the debug renderers, and the server-side debug subscription
  system). The F3 screen is now a registry of entries assembled into
  profiles, fed by sample loggers and by a *server push* subscription
  system — brains, paths and points of interest reach the client through
  it. That last part is server-side and nothing here documents it.
- **`net/minecraft/util/parsing`** (29) — the string-parsing toolkit under
  the command arguments.
- **`net/minecraft/client/animation`** (23) — declarative keyframe
  animation data for entity models, adjacent to
  [entity rendering](../client/entity-rendering.md).
- **The Vulkan and platform halves of Blaze3D** (about 69 classes) — named
  by [Blaze3D](../client/blaze3d.md) but not walked.

## Where to look

If you need one of these, the entry points are named in each section. If
you are looking for a *list* rather than a system, start at
`net/minecraft/references` for ids and the report providers in
`net/minecraft/data` for everything else.

---

*Rules: names, never code · how the system works, not how the code reads ·
newest version only · every backticked name passes `tools/verify_names.py`.*
