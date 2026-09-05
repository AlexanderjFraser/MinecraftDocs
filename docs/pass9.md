# Pass 9 — the third fact-check (queue; opened 2026-09-05)

*Pass 9 re-runs pass 4's adversarial protocol — archived in
[pass4.md](pass4.md) with its charter, its agent brief
([pass4-brief.md](pass4-brief.md)) and its lessons — over the corpus passes
5–8 rewrite. This file is where every pass-5, -6, -7 and -8 session writes
down what pass 9 must check first: every page it rewrote, every claim a
rewrite introduced (a hook, a moved paragraph, a redrawn arrow, a re-scoped
count, a new section, a landing page's new argument), and every correction
it made with the decompile open. Pass 9 checks everything anyway; this list
decides what it checks first. It is also what made pass 4 checkable: from
Part VI on, the errors were in what the writing session did not know it had
changed, so a session lists what it changed on purpose and pass 9 reads the
rest harder.*

## How to write an entry

Per session, newest first, under `## Session X — Part N (pass M)`: the pages
rewritten; per page, one line per claim introduced, quoting the sentence;
the figures redrawn, and which orderings they assert; the material moved,
from where to where; and, under *Corrections*, every fact changed with the
decompile open — what the page said, what the decompile says, file and line.
Name the page in backticks on every line so a queue tool can route it.
Strike nothing here; pass 9 strikes.

## Standing items

- **A correction is a claim.** Pass 9 confirms the fix, not the original,
  and its close audits the pass's own strikes — session O of pass 4 found a
  strike that had settled nothing and a correction that was the error.
- **The summarisers are read last.** The thirteen landing pages,
  `lectures.md`, the glossary and the introduction are re-read after the
  pages they summarise are fixed, never before.
- **The figure against the section under it first**, before either is read
  against the source: nine pages in pass 4 had a diagram contradicting its
  own paragraph, and the prose was right every time.
- **Counts are call sites, not `grep -c` lines**; a generated page is
  checked by re-deriving the population, never a row.
- **Names inside mermaid blocks** are under a gate from pass 7's close; the
  23 ambiguous simple names the verifier prints are settled by pass 8 or in
  the tool.
- **Pass 9 adds nothing.** A gap it finds goes to [pass3.md](pass3.md) §7,
  the coverage queue, which seeds the second edition.

## Entries

*(pass-5 sessions append below, newest first)*

## Session A — the standard (pass 5) *(2026-09-05)*

Three published pages rewritten — `src/lectures.md`, `src/SUMMARY.md` and
`src/systems/commands/README.md` — plus `TEMPLATE.md` and two tools. No
system page touched, no fact changed, and **no correction made**: nothing
this session read was found wrong against the decompile, and nothing was
re-derived, because every finding was about where a claim lives rather than
whether it is true. The claims introduced:

**`src/lectures.md`**

- The dependency table gained a **membership rule** and three rows and lost
  three. The rule is a claim about the corpus, checkable without the
  decompile: *a page two or more landing pages name under **before you
  start***, less `anatomy/anatomy`, `foundations/codecs-nbt-json` and
  `foundations/identifiers-and-registries`. `tools/check_deps.py` re-derives
  it on every run and fails on a mismatch, so pass 9's job here is to check
  the rule is the right rule, not the rows.
- Three new rows carry a new third-column phrase each, and each is a claim
  about why a part depends on the page, re-derived from the depending
  landing pages' own sentences: **`resource-system`** — "the staged load and
  its barrier: a server's own data at startup, where recipes and loot tables
  come from, and the reload the atlases are built by" (from `server/README`,
  `items/README`, `rendering/README`); **`data-driven-types`** — "the *type*
  field in a data-pack file and the registry it dispatches on; these two
  parts own most of its instances" (from `worldgen/README`,
  `commands/README`; the "most" rests on `worldgen/README`'s existing
  twenty-six-of-fifty-six claim); **`text-components`** — "what a chat
  message and a screen's label are before anything draws them" (from
  `networking/README`, `client/README`).
- "Watched straight through, the sidebar order still needs one departure
  from itself, and it is now as small as it can be" — the claim is that
  moving *environment attributes and timelines* to first in Part IV leaves
  exactly one out-of-order watch (Part IV lecture 1 before Part III lecture
  2) and that no other part's order departs. `check_deps.py` checks the
  three orders agree; the "one departure" is the session's own reading of
  the graph.
- **102 blurbs cut.** Each was a second copy of a line on a landing page.
  The ordering claims inside them were kept and are quoted unchanged; the
  descriptions were dropped, not moved, because the landing page has them.
  Pass 9 should read the kept clauses against the landing pages rather than
  against the source: the risk is a clause that lost its subject in the cut,
  not a fact that changed.
- The new second paragraph ("Because the subject here is the order, nothing
  below describes a lecture…") is a claim about the page itself.
- "one page until this pass" became "two pages that were one" — a
  pass-number rot fix, no claim.

**`src/SUMMARY.md`** — *environment attributes and timelines* is now first
in Part IV. Nothing else moved; no URL changed (mdBook derives the path from
the file, not the summary).

**`src/systems/commands/README.md`** (the exemplar landing page)

- The size sentence is now `{{#include ../../generated/part-commands.md}}`
  and reads **470 classes and 43,126 lines**, against the hand-count it
  replaced (473 / 43,900). The prose's population is now "the nine packages
  the atlas lists for this part", which is `map_source.PARTS` — check the
  nine, and the `#where-each-part-lives` anchor.
- New: "the command catalogue alone (`net/minecraft/server/commands`) is 102
  classes and 12,800 lines" — the old sentence said "a hundred command
  classes and 12,800 lines" without naming the package.
  `src/generated/packages-depth4.md` gives 102 / 12,781.
- New in the argument: "**None of those four needs any of the others.**" —
  moved up from the shape section, which says "none of them needs another".
  The sentence after it ("a reader who has those two can explain any of the
  four from them") is new and is a claim about the part, not about the game.
- **Cut, not moved**: "one of only two parts of a save that go through the
  data fixer as JSON, the other being advancement progress".
  `anatomy/what-this-book-skips`:252 owns it and this page links there.
- Three *before you start* links now carry an anchor
  (`server-tick#what-minecraftservertickchildren-runs-and-in-what-order`,
  `data-driven-types#the-idea-stated-once`,
  `the-connection#the-threads-underneath-it`). The claim in an anchored link
  is that the named section is where the thing is explained; all three were
  checked against the built heading ids.

**`TEMPLATE.md`** — two new sections, *One home per mechanism* and *The
landing page*. The only measured claim in them is the landing-page budget
("about a hundred lines plus the watch order"), derived from the thirteen
pages on 2026-09-05.

**`tools/check_deps.py`, `tools/verify_names.py`** — two new failing checks
and the index label; see `docs/pass5-brief.md` A5. A tool is suspected
first, twice over: `check_deps.py`'s membership check reproduced pass-4
session A's hand-found list exactly (three absent, three present that should
not be) before anything was edited, which is the evidence that it reads the
pages right; and `check_deps.py --probe` now proves both new checks fail on
the constructs they are for — a reordered sidebar, a short sidebar, a
qualifying page with no row, a row for a page one part assumes, a row for a
page nobody assumes, and a universal that takes a row — and pass on the
shapes they must accept.

## Planning session — between passes 4 and 5 (2026-09-05)

No system page rewritten. Three claims introduced, all in the frame and the
atlas:

- `src/introduction.md` — the *Verified means tested* paragraph now says
  "every link and anchor between pages is checked to land" and "a page that
  fails any of those does not go up": the claim is that `tools/check_links.py`
  runs in `tools/deploy.sh` before the build and exits non-zero on a broken
  link, anchor, include, `SUMMARY.md` entry or redirect (`tools/deploy.sh`,
  the line after `check_deps.py`).
- `src/maps/packages.md` — the *Where each part lives* table is now
  `src/generated/parts.md`, written from `map_source.py`'s `PARTS`. The
  mapping is a set of claims about which packages each part covers, and it
  differs from the hand table it replaced: Part IV adds `world/level/material`,
  `world/attribute`, `world/timeline`, `world/clock`, `world/level/border`;
  Part VI adds `world/damagesource`, `world/effect` and subtracts
  `world/entity/player`; Part II adds `world/flag`; Part IX subtracts
  `network/syncher` (Part VI's); Part X adds `client/input`, `client/server`
  and counts `net/minecraft/client` itself only; Part XI adds
  `client/particle`; Part XIII adds `server/permissions`, `server/bossevents`
  and `client/gui/screens/dialog`. The paragraph above the table says how
  it is counted (no prefix, *itself only*, shared packages counted twice,
  skipped packages left out) — check each against `map_source.in_part`.
  Every landing page's size sentence will quote its row once the part
  sessions switch them to the include; until then a landing page's hand
  count and its row may differ (Part XIII: 473 / 43,900 by hand, 470 /
  43,126 by the atlas).
- `docs/pass5-brief.md` Part 4 — the measured tables (coverage per part, the
  queue by kind, the duplication pairs) are the tools' output on 2026-09-05
  and are claims about the corpus on that day, not about the game; pass 9
  need not check them.

## Pass 5, session B — Parts I and II *(2026-09-05)*

Eleven pages read by one agent each, both parts read end to end, nine pages
rewritten (`anatomy/README.md`, `anatomy/anatomy.md`,
`anatomy/what-this-book-skips.md`, `foundations/README.md`,
`foundations/identifiers-and-registries.md`, `foundations/resource-system.md`,
`foundations/tags.md`, `foundations/codecs-nbt-json.md`,
`foundations/data-driven-types.md`) plus one-clause link edits on
`data-components.md` and `text-components.md`.

### Corrections — re-derived against the decompile before the fix

- `foundations/identifiers-and-registries.md` — said `MappedRegistry` "is
  keyed three ways (`byKey`, `byLocation` and the insertion-ordered
  `byId`)". **There are four.** `MappedRegistry.java:40` declares
  `private final Map<T, Holder.Reference<T>> byValue`, an `IdentityHashMap`
  built at :65 and written at :129; `getKey` (:141) and `getResourceKey`
  (:148) both read it, so the object-to-name direction goes through `byValue`
  and not through the three the page named. `toId` (:37) is the parallel
  identity map to the number. Now: four indexes, one per lookup direction.
- `foundations/codecs-nbt-json.md` — said `StreamTagVisitor` and its
  neighbours "let `NbtIo.parse` pull **two** fields out of a region chunk",
  then named three consumers. Two is right for one of them only:
  `IOWorker.java:105` builds a `CollectFields` of two `FieldSelector`s
  (*DataVersion*, *blending_data*); `StructureCheck.java:113` builds one of
  three (*DataVersion*, *Level/Structures/Starts*, *structures/starts*). Now
  stated as the mechanism — a `CollectFields` over whatever selectors the
  caller wants — with both counts attributed.
- **Checked and found correct, so no change:** `data-components.md`:183-191
  and `identifiers-and-registries.md`:306-311 were reported as contradicting
  each other on the singleplayer component binding. They do not.
  `ClientConfigurationPacketListenerImpl.java:177` passes
  `connection.isMemoryConnection()` as
  `tagsAndComponentsForSynchronizedRegistriesOnly`, and
  `RegistryDataCollector.java:166` negates it into `updateComponents`'
  `includeSharedRegistries` (:142-148), so a memory connection binds only the
  `RegistrySynchronization.isNetworkable` registries. Both pages say that.

### Claims introduced

- **A new section, `identifiers-and-registries.md` §*Feature flags: the same
  registry, narrowed*** — the largest new claim of the session, discharging
  a coverage entry. Each sentence, with where it came from:
  `FeatureFlagSet` is a *long* mask plus a `FeatureFlagUniverse`, cap
  `MAX_CONTAINER_SIZE` = 64 (`FeatureFlagSet.java:9-18`); one universe,
  *main*, and four flags — `VANILLA`, `TRADE_REBALANCE`,
  `REDSTONE_EXPERIMENTS`, `MINECART_IMPROVEMENTS` (`FeatureFlags.java:37-48`);
  `isExperimental` is "not a subset of `VANILLA_SET`" (:34-36);
  `FeatureElement` has one method and seven implementors — `Item`,
  `BlockBehaviour`, `EntityType`, `GameRule`, `MenuType`, `Potion`,
  `MobEffect`; `FILTERED_REGISTRIES` names those seven registries
  (`FeatureElement.java:10`);
  `HolderLookup.RegistryLookup.filterFeatures` returns *this* for a registry
  not in the set and a filtering delegate for one that is
  (`HolderLookup.java:82-87`); **"the registry underneath is not touched, and
  neither is its numbering — a disabled item keeps its wire id"** is the
  inference from that delegation and is the sentence most worth re-deriving;
  the consumers are `CommandBuildContext.java:22`, `GameRules.java:109`,
  `MinecraftServer.java:373` and `LevelReader.java:232-235`; the set is
  `WorldDataConfiguration.enabledFeatures`.
- **`resource-system.md`, the two `server/packs` corners** the skips page had
  been promising it: *linkfs* as `LinkFileSystem` / `LinkFSProvider` /
  `LinkFSPath`, and `DownloadQueue` — one directory per pack UUID, one at a
  time on a `ConsecutiveExecutor` over `Util.nonCriticalIoPool`, a
  `JsonEventLog` per attempt, and `DownloadCacheCleaner.vacuumCacheDir` at
  construction trimming to `MAX_KEPT_PACKS` = 20 (`DownloadQueue.java:37-47`,
  `DownloadCacheCleaner.java:30-60`). **"newest kept, one per directory
  before any directory's second"** is a reading of `prioritizeFilesInDirs` and
  the two comparators, and is the claim here to check.
- **`anatomy.md`, the packet-drain contrast.** The hop paragraph now ends
  "so a client at 200 frames a second takes the server's updates ten times
  more often than it ticks" — arithmetic over the page's own 20 Hz tick, and
  a restatement of `what-the-client-is-told.md`:442. Check the framing, not
  the numbers.
- **`anatomy.md`, the 1.21-era callout** was replaced: out went the
  `Gui`/`Hud` box (owned by `client/hud` and `reference/naming-drift`), in
  came `DeltaTracker` was *Timer*, which restates
  `reference/naming-drift.md`:52 and :68.
- **`anatomy.md`, `GameConfig`** — new clause: the client's `Main` parses its
  command line into a `GameConfig` the `Minecraft` constructor is built from.
  Closes the part's one coverage gap; check against `client/main/Main`.
- **`anatomy/README.md` is rewritten to the landing-page role** and its
  figure redrawn from the twelve other parts to the part's own two pages.
  New claims: that the part's argument is the two loops rather than "a server
  that ticks and a client that draws"; that the boundary page is second
  because a boundary is drawn before the investment (moved from
  `lectures.md`:466-468, which keeps it as an ordering claim); and *where the
  part stops*, which asserts that Parts III, IX and X take the three threads
  onward. The lane sentence is now "nearly every lane ... is a class, and the
  handful that are not stand for a thread", which is
  `reference/lanes.md`:5-10 and `check_lanes.py`'s own count (333 and 9).
- **`foundations/README.md`** — "Part II is not a stack but a fan ... the
  figure has two roots and no single column" replaces "Part II is a stack".
  A claim about the figure directly above it, and checkable against it.
- **`what-this-book-skips.md`, three reframings.** `com/mojang/blaze3d/audio`
  is no longer presented as skipped — `client/sound-engine` teaches all of it
  (its cast carries `Library` and `AbstractDeviceTracker`; :129 the thirty
  channels, :240 HRTF), so the section keeps only the address argument. The
  statistics page's criterion-parse paragraph became a citation of
  `scoreboard-and-data`:158-162, which owns it. The recipe book is stated as
  `items/recipes`' rather than as skipped. **The hatching in the generated
  treemap was not changed to match**, so the figure and the prose should be
  read together at pass 9.
- **Ownership moves that changed what a page asserts** (each now one sentence
  and a link where it was an explanation): the two tag tables, from
  `identifiers-and-registries` to `tags`; the GPU-backend retry order, to
  `rendering/the-window`; the crash relay, to `how-a-server-dies`; the
  empty-server pause, to `server-tick`; `MinecraftServer.spin`'s order, to
  `starting-a-server`; the Netty hop's mechanism, to `the-connection`. In
  each case check that the surviving sentence is still true on its own — a
  trimmed sentence is a new claim.
- **Outbound links gained anchors** across the nine pages. An anchor is a
  claim that the named section is the answer; all resolve under
  `check_links.py`, which proves the heading exists and not that it answers.

### Tool bug

- `tools/map_source.py` and `tools/pass5_coverage.py` reported different
  populations for the same packages — Part I as 7 classes / 6,770 lines and
  6 / 6,766 — while `map_source.py`'s own comment claimed they "can never
  disagree". The difference is `package-info.java`, which the atlas counts as
  a file and the coverage tool drops. No published page states either number
  today (Part I's landing page carries no size), so nothing false was
  published. Both tools now say which population they mean, and the false
  comment is gone. Every part with a `package-info.java` reads one class
  larger in the atlas than in its coverage report.

## Pass 5, session C — Part III · The server *(2026-09-05)*

All six pages of Part III touched: `src/systems/server/README.md` (rewritten
to the landing-page role), `server-tick.md`, `server-level-tick.md`,
`players-and-sessions.md`, `starting-a-server.md`, `how-a-server-dies.md`.
Also one line each in `src/lectures.md` and `src/reference/README.md`.

### Corrections — re-derived against the decompile before the fix

- **`how-a-server-dies`: the autosave interval.** The page said the autosave
  runs "every 6000 ticks — five minutes of game clock, floored at 100 ticks".
  The decompile: `MinecraftServer.ticksUntilAutosave` starts at 6000 ticks
  (`MinecraftServer.java`:337) and is thereafter
  `computeNextAutosaveInterval` = `Math.max(100, (int)(ticksPerSecond *
  300.0F))` (`MinecraftServer.java`:1149-1162), i.e. **300 seconds of wall
  clock at the current rate**, not 6000 ticks and not game clock. Now "on the
  countdown the tick keeps … five wall-clock minutes, whatever the tick
  rate", citing `server-tick#the-bookkeeping-at-the-bottom`, which owns the
  arithmetic. This agrees with `server-tick`:403-412 and
  `chunk-storage`:311-316, which were already right.
- **`starting-a-server`: a missing management secret.** The page said
  `JsonRpc.create` "throws, ending the boot, if it is set and the secret is
  not forty alphanumeric characters rather than quietly going without one",
  which reads as *absent secret kills the boot*. The decompile:
  `DedicatedServerProperties`:132 resolves *management-server-secret* with
  `SecurityConfig.generateSecretKey()` as its **default**, and `Settings.get`
  puts the resolved value back into the properties map, which
  `DedicatedServerSettings.forceSave` writes — so an absent secret is
  generated and saved. `JsonRpc.create` throws only when the secret present
  fails `SecurityConfig.isValid` (non-empty, exactly forty alphanumerics —
  `SecurityConfig.java`:9-11). This also settles the disagreement with
  `what-this-book-skips`:180-181 ("generating one if absent"), which was the
  right half.
- **`starting-a-server`: what `DerivedLevelData` causes.** The page said the
  derived data is "why the time of day, the weather, the difficulty and the
  world spawn are one set of numbers every dimension shares". The decompile:
  `DerivedLevelData.java`:18-80 forwards game time, level name, game type,
  hardcore, allow-commands, initialised, difficulty and the difficulty lock,
  and swallows every setter but `setSpawn`. It carries **no** day time and
  **no** weather — day time is `ServerClockManager`'s and weather is one
  server-wide `WeatherData` — and the spawn a level reports comes from
  `MinecraftServer.effectiveRespawnData` through `ServerLevel.getRespawnData`
  (`ServerLevel.java`:1523-1524, `MinecraftServer.java`:1289-1292,
  1884-1885). Three of the four attributions were wrong; the paragraph now
  claims difficulty (and the rest of the forwarded set) and names the real
  owners of the other three, citing
  `level-data-and-rules#the-spawn-every-level-reports-is-the-servers-not-each-levels`.
- **`server-tick`: what ticks the `/schedule` queue.** The page said it
  "ticks from inside `ServerLevel.tickTime`, with the dimension's own game
  time". The decompile: `ServerLevel.tickTime` is wholly inside
  `if (this.tickTime)` (`ServerLevel.java`:458-466), the flag only the
  overworld is constructed with, and it passes the overworld's incremented
  game time to `getScheduledEvents().tick`. Now "which runs in the overworld
  alone and off the overworld's *gameTime*", citing the level tick. This was
  a disagreement with its own declared pair (`server-level-tick`:135-141),
  which was right.
- **`server-level-tick`: what the mob count walks.** The page said
  `NaturalSpawner.createState` walks every entity "skipping mobs that require
  persistence". The decompile (`NaturalSpawner.createState`) also skips every
  entity whose category is `MobCategory.MISC` — items, projectiles, armour
  stands — which is most entities in a busy world. Now states both skips.
  `entity-lifecycle`:41 had both and was right.
- **`server-level-tick`: the second chunk set.** The page said
  `ChunkMap.forEachBlockTickingChunk` walks the entity-ticking set and "each
  of those chunks gets `ServerLevel.tickChunk`". The decompile: it also drops
  any position whose `ChunkHolder` is absent or whose
  `ChunkHolder.getTickingChunk` is null. Now "keeps only those whose
  `ChunkHolder` has a live `ChunkHolder.getTickingChunk`".
  `scheduled-ticks`:295-297 had the filter.

**Re-derived and found sound** (a strike is a claim, so these are recorded
too): `starting-a-server`'s "the tickets the last shutdown parked" —
`TicketStorage.fromPacked` loads every persisted ticket into the
*deactivated* map, so "parked" is exactly the loaded state;
`players-and-sessions`' "`MinecraftServer.saveAllChunks` stamps the current
owner's id into the level data" — `MinecraftServer.java`:642-644 passes
`getSingleplayerProfile().id()` to `saveDataTag`; `server-level-tick`'s
`Player.isAlwaysTicking` — declared on `EntityAccess`, false on `Entity`,
overridden true on `Player` alone, so both this page's and
`entity-lifecycle`'s spellings are right; `server-level-tick`'s ticket-purge
gate — `ServerChunkCache.java`:328 is `runsNormally() || !tickChunks`, and
the page's scope is the level tick, where `tickChunks` is true;
`server-tick`'s *clocks* and *command functions* table rows — both guards are
inside the called method (`ServerClockManager.tick`,
`ServerFunctionManager.tick`), which is what the *skipped when* column
describes; the landing page's "five side threads" — `reference/threads.md`
has exactly five dedicated-only rows.

### Claims introduced

- **`src/systems/server/README.md` rewritten to the landing-page role.** New
  claims: the part's argument, that "almost everything surprising about a
  server's timing is the order of one method", and that a reader who finishes
  can answer *when* for four named things; the size paragraph, which is the
  atlas include plus "over half of those lines are
  `net/minecraft/server/level`'s forty-two classes, at nearly three hundred
  lines apiece" (42 / 11,977 from `map_source.py packages`); the pair claim
  moved in from `lectures.md` ("seven later parts assume one of them or the
  other"), which is `lectures.md`'s own count and is now stated once; a new
  *where the part stops* section, asserting that `ChunkGenerationTask`,
  `ChunkTaskDispatcher`, `ChunkTaskPriorityQueue` and `WorldGenRegion` belong
  to Part IV, `ServerPlayerGameMode` to Parts V and VIII, `ServerScoreboard`,
  `ServerFunctionLibrary` and `ServerAdvancementManager` to Part XIII, and
  `ReloadableServerRegistries` to Part II (each from the coverage report's
  *named on pages of other parts* table); and the *Game rules* line, now "the
  fourteen these five pages name, out of fifty-nine" — counted by grep over
  the five pages and against `gamerules.md`'s own 59.
  **Cut:** "a hopper moves one item per eight of them", which was true
  (`HopperBlockEntity.MOVE_ITEM_SPEED` is 8) and had no home but this
  summariser; logged to [pass5.md](pass5.md) for session E.
  **Moved out:** "a console command … is as late as the piston", now a
  sentence on `server-level-tick`'s broadcast section, where the rule it
  qualifies lives.
- **`server-level-tick`: two new passages.** A paragraph after the cast on
  what the abstract `Level` holds and leaves abstract, and what `ServerLevel`
  adds — the §7 gap, discharged; every member named was read
  (`Level.java`:110-134 for the fields, its nineteen abstract declarations,
  `ServerLevel.java`:202-216 for the four additions), and `getChunkSource` is
  deliberately *not* claimed for `Level`, because it is declared on
  `LevelAccessor`. And a sentence naming the tick's profiler zones in order —
  *world border*, *weather*, *tickPending* (*blockTicks*, *fluidTicks*),
  *raid*, *chunkSource*, *blockEvents*, *entities* (*dragonFight*,
  *checkDespawn*, *tick*), *blockEntities*, *entityManagement*,
  *debugSynchronizers* — read off `ServerLevel.tick`'s own `push`/`popPush`
  calls. Ten pages in five parts already cite these names; this is the first
  page that defines them.
- **`players-and-sessions`: three coverage additions.** The stored-user-list
  family (`StoredUserList` as a JSON file of `StoredUserEntry` records,
  subclassed as `UserBanList`, `IpBanList`, `ServerOpList`, `UserWhiteList`;
  `BanListEntry`'s source, reason and expiry; and **the expiry swept on
  read** — `StoredUserList.get` calls `removeExpired` before answering, so a
  temporary ban lapses when somebody asks rather than on a timer). The
  identity cache named as `CachedUserNameToIdResolver` over *usercache.json*
  with `ProfileResolver` behind it (`Services.java`:17-22). And
  `PlayerDataStorage`'s rescue, which the cast cell had promised and the page
  never gave: a failed *.dat* read copies the file aside under a
  *_corrupted_* name and then tries the *.dat_old* twin
  (`PlayerDataStorage.java`:69-114). The clause that a player with neither is
  "built from nothing, which is a new spawn rather than an error" is the
  session's inference from `load` returning empty, and is the line on this
  page to check hardest.
- **`starting-a-server`: one coverage addition.** `Bootstrap.bootStrap`'s
  last act installs `LoggedPrintStream` (or `DebugLoggedPrintStream` when
  debug logging is on) over `System.out` and `System.err`, keeping the
  original as `Bootstrap.STDOUT` — `Bootstrap.java`:39, 63-64, 146-155. That
  is why `Bootstrap.realStdoutPrintln` exists for the watchdog report.
- **Ownership cuts, each now one sentence and an anchored link.** The crash
  relay, from `server-tick` to `how-a-server-dies#the-crash-that-saves`
  (session B's ruling, applied); what a stopped server does with a submitted
  task, from `server-tick` to
  `how-a-server-dies#the-front-door-closes-the-guests-do-not-leave`, with
  *RejectedExecutionException* **moved** into that page rather than dropped;
  `session.lock`'s nature, from `how-a-server-dies` to
  `starting-a-server#taking-the-lock-and-fixing-leveldat-twice`; the
  `level.dat` write path, from both Part III pages to
  `level-data-and-rules#what-is-left-in-leveldat` (three tellings to one, and
  `how-a-server-dies` keeps `NbtIo.writeCompressed`, which the Reference page
  lacks); the ticket-persistence half, from `how-a-server-dies` to
  `tickets-and-loading#what-a-ticket-asks-for`, keeping only *why the drain
  loop ends*; *Done* against `MinecraftServer.isReady`, from
  `how-a-server-dies` to `starting-a-server#done-comes-before-the-loop`; the
  flush bracket and the 601st-call latency sweep, from `players-and-sessions`
  to `server-tick`; the per-chunk save spacing, from `how-a-server-dies` to
  `chunk-storage#the-four-moments-a-chunk-is-written`; the thread table's
  *what it may touch* framing, from `starting-a-server` to
  `reference/threads#the-threads-a-lecture-leans-on`. **Every trimmed
  sentence is a new claim** — pass 4's finding — and these are where to look
  first.
- **Seams repointed, which are claims about who owns what.**
  `starting-a-server`'s login-encryption hand-forward now goes to
  `protocol-phases#login` instead of `players-and-sessions`, which never
  explained it; `players-and-sessions`' two-place tick hand-forward now goes
  to `the-two-phase-tick#the-trace-one-player-one-tick-twice` instead of
  `player-anatomy`, which does not contain `ServerPlayer.doTick`; its
  permission-model link now goes to `permissions#where-a-set-comes-from`
  instead of `brigadier-and-commands`, which owns the packet and not the set;
  and `how-a-server-dies`' claim about connections with no `ServerPlayer` now
  cites `protocol-phases#configuration` rather than `players-and-sessions`.
- **`players-and-sessions`: `GameRules.KEEP_INVENTORY` re-scoped.** "decides
  only whether `ServerPlayer.transferInventoryXpAndScore` runs" is now
  "decides only whether `ServerPlayer.restoreFrom` runs" it, with a link to
  `damage-and-death` for what the same rule decides on the way out. The rule
  is read in three places (`ServerPlayer.java`:1749, `Player.java`:551 and
  `Player.java`:1609); the *only* was true of `restoreFrom` and read as
  global.
- **Anchors on twenty-eight outbound links across the six pages.** An anchor
  asserts that the named section is the answer; `check_links.py` proves the
  heading exists and not that it answers.
- **`src/lectures.md`** loses the pair claim (moved to the landing page), and
  its III-to-IV paragraph now says the level tick's first step "throws away a
  cache" rather than that its "first statement about the day-night cycle"
  rests on the environment page — the page's dependency is the cache, per
  `server-level-tick`:94-105. **`src/reference/README.md`** adds III to
  *Level data and rules*' parts column, which the landing page now points at.

### For pass 9's attention, found and not fixed

- `server-tick`:403-412 says the autosave countdown "starts at
  `MinecraftServer.AUTOSAVE_INTERVAL` (6000)". The value is right and the
  constant exists, but the constructor writes the literal 6000
  (`MinecraftServer.java`:337) and nothing reads `AUTOSAVE_INTERVAL` — a dead
  constant the page presents as the source of the number.
- `server-tick`:211-212 has `Connection.tick` flushing "at the end of the
  connection phase"; the flush is inside each connection's own tick, so it is
  true of the phase as a whole and not of any one call.
- `server-tick`'s *clocks* row gives *skipped when* as "frozen, or
  `GameRules.ADVANCE_TIME` is off", where only the first is a skip of the
  call and the second is a no-op inside it. Same shape as the *command
  functions* row, so the two are at least consistent.
- `commands/scoreboard-and-data`:277-278 says "a score set and a crash a tick
  later is a score lost", which contradicts `how-a-server-dies`' hook (a
  tick-loop crash writes what `/stop` writes) unless it means a watchdog kill
  or a *kill -9*. Session M's page, flagged in [pass5.md](pass5.md).
