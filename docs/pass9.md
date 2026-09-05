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

## Pass 5, session D — Part IV · The world *(2026-09-05)*

Eleven Part IV pages plus `reference/level-data-and-rules`, read by one agent
each; the part read end to end in watching order first. Four pages outside the
part were edited, each because a Part IV page disagreed with it:
`server/server-level-tick`, `server/server-tick`,
`networking/what-the-client-is-told`, `rendering/lightmap-fog-and-sky`. One
tool bug, and it had been hiding broken links.

### Corrections — every one re-derived against the decompile

- `world/chunk-anatomy`:247 said "Packing therefore buys a smaller palette,
  **not narrower entries**: unreferenced entries are dropped, which can demote
  a container a whole rung, and a `Configuration.Global` container shrinks from
  `Configuration.bitsInMemory` to `Configuration.bitsInStorage`." The head
  clause is false and the two tails contradict it.
  `PalettedContainer.pack` (`PalettedContainer.java:255-281`) re-encodes into a
  fresh `HashMapPalette`, asks `Strategy.getConfigurationForPaletteSize` for
  the *shrunken* palette's configuration, and writes at
  `Configuration.bitsInStorage`. `Configuration.Simple` reports one width for
  both (`Configuration.java:40-47`) and `Configuration.Global` two, so packing
  narrows entries in exactly two cases: a smaller palette landing a rung lower,
  and a global container's storage width. **Now:** what packing recomputes is
  the palette, and narrower entries are the consequence in those two cases,
  each named.
- `world/chunk-storage`:334 said `ImposterProtoChunk` "does not defer to the
  `LevelChunk` it wraps, which **only** `ImposterProtoChunk.markUnsaved` does".
  `ImposterProtoChunk.java:157-158, 248-254`: `markUnsaved`, `isLightCorrect`
  **and** `setLightCorrect` all delegate unconditionally, which
  `chunk-anatomy`:112 already said — the two pages disagreed. The two flat
  falses are `canBeSerialized` and `tryMarkSaved`
  (`ImposterProtoChunk.java:162-169`). **Now:** all three delegating members are
  named, both pages say the same thing, and `chunk-storage` cites
  `chunk-anatomy`'s anchor.
- `world/chunk-storage`:281 said loading "changes hands **four** times" and
  then named four stages. `ChunkMap.java:582-610` and `997-1001`: the stages are
  the IO lane, *upgradeChunk* and *parseChunk* on `Util.backgroundExecutor`, and
  `SerializableChunkData.read` on the main-thread executor — four stages across
  **three** lanes, two of them sharing one. **Now:** "four stages across three
  lanes", with the shared lane said out loud. The same sentence's
  `SimpleRegionStorage.upgradeChunkTag` is now `ChunkMap.upgradeChunkTag`, which
  is the call `ChunkMap.readChunk` actually makes (`ChunkMap.java:999`), so the
  two Part IV pages name one member for one hop.
- `world/scheduled-ticks`:81 said "**Two type parameters**, two parallel
  worlds". `LevelTicks.java:34`, `LevelChunkTicks.java:17`,
  `LevelTickAccess.java:5` and `ScheduledTick.java:8` each declare exactly one
  parameter. **Now:** "Two type *arguments*", with the one-parameter fact stated
  and `Block` and `Fluid` named as what fills it.
- `world/lighting`:184 said `LightEngine.checkNode` "only decides what to
  enqueue", two paragraphs before describing the sky engine writing stored
  levels. Both engines' `checkNode` writes: `BlockLightEngine.java:36`
  (`setStoredLevel(blockNode, 0)` when emission dropped below the stored level)
  and `SkyLightEngine.java:73`, plus `updateSourcesInColumn` →
  `removeSourcesBelow`/`addSourcesAbove` at `SkyLightEngine.java:108, 135`.
  **Now:** "zeroes the stored level where the light that is there must go and
  enqueues the rest as work".
- `world/fluids`:275 attributed lava's slope numbers through
  `WaterFluid.getSlopeFindDistance` while its own table at :338 used
  `FlowingFluid.getSlopeFindDistance`. `FlowingFluid.java:353` declares it
  abstract; `WaterFluid.java:86` and `LavaFluid.java:154` override.
  **Now:** `FlowingFluid.getSlopeFindDistance` in both places.
- `rendering/lightmap-fog-and-sky`:61 said the lightning layer lerps
  `EnvironmentAttributes.SKY_COLOR` "**a fifth** of the way";
  `environment-attributes-and-timelines`:92 says 22%. `ClientLevel.java:274` is
  `ARGB.srgbLerp(0.22F, …)`, so the owner page is right. **Now:** the rendering
  page's whole duplicate paragraph is one clause and a link, so the number is
  stated once.
- `networking/what-the-client-is-told`:368 said the once-a-second time sync
  "carries a game time plus **a map of clock updates**".
  `MinecraftServer.java:1299-1305` broadcasts
  `new ClientboundSetTimePacket(this.overworld().getGameTime(), Map.of())` — an
  **empty** map, which is what `environment-attributes-and-timelines`:221 says.
  **Now:** the networking page says the map is empty and that clock state travels
  only on a change or a join, with the owner's anchor.
- `reference/level-data-and-rules`:47 sent the reader to `server/server-tick`
  for day time; that page does not own it, `environment-attributes-and-timelines`
  does, and the environment page was claiming this Reference page pointed at it.
  **Now:** repointed to `#who-owns-the-clock`, so the hand-forward is paid.

### Suspicions re-derived and found sound — a strike is a claim

- `chunk-generation-pipeline`:190's "the dispatcher's own **four-slot** queue"
  is real: `ChunkTaskDispatcher.DISPATCHER_PRIORITY_COUNT` is 4 and the four
  users are resort 0, release 1, submit 2, poll 3
  (`ChunkTaskDispatcher.java:18, 38, 51, 63, 80`), so a re-sort really does
  outrank a new submission. Unchanged, and it is a *different* four from the
  ticket throttle's.
- `chunk-generation-pipeline`:211's two requirements on the centre chunk are
  both real and not in conflict: `ChunkGenerationTask.java:92-118` wants the
  persisted status at or past the target **and** every chunk of the loading
  pyramid's square at or past what its distance requires. Unchanged.
- `tickets-and-loading`:346's purge gate — "unless the level is frozen and
  chunk ticking is on" — is exactly `ServerChunkCache.java:328`
  (`runsNormally() || !tickChunks`). Unchanged; `server-level-tick`'s shorter
  "running" is a table compressing it.
- `scheduled-ticks`:364's "only `/clone` and the gametest framework do, in bulk"
  distributes correctly: `CloneCommands.java:248` calls `copyAreaFrom`, which
  only reads (`LevelTicks.java:301-326`), and `GameTestInfo.java:81` /
  `StructureUtils.java:107` call `clearArea`, which removes. Unchanged.
- `chunk-anatomy`:126's double-buffered added and removed sets really are
  `ClientChunkCache.Storage`'s fields (`ClientChunkCache.java:220-221`), with
  the accessors and `flipUpdateTrackingSets` on the cache. Unchanged.
- `points-of-interest`:316's "`PoiManager.loadedChunks` never forgets" holds:
  `PoiManager.java:49, 263` is a `LongSet` only ever added to. Unchanged.

### Claims introduced

- `world/README` — the header now says "the five pages off that line — what the
  place and the hour decide, and the four systems that make the world the line
  delivers feel alive", which is a claim that the environment page is neither
  conveyor nor side-system. A new ***Where the part stops*** section claims that
  about 2,900 lines of the part's packages are taught in six other parts, and
  names each family and its owner part; and it **declares the world border
  Reference-only**, with the reason (no scenario, and what a reader needs of it
  is enumerable). *Watch in this order* entry 1 no longer claims the environment
  page is "the one page here that depends on nothing else in the part" — it says
  *off the conveyor, ahead of it*, which is what the figure draws. Five blurbs
  re-synced word for word to their pages (fluids' two halves, chunk storage's
  "almost every write", the sensor's "at least one tick", the tickets page's
  "nothing asks for a chunk *because* it is loaded", chunk anatomy's *distinct*).
  The Reference list gains `reference/registries.md` with the claim that three
  of the part's mechanisms are registry-backed.
- `src/lectures.md` — Part IV's shape paragraph now counts the conveyor the way
  the landing page does (four pages plus a vocabulary page, not five), and
  lighting's blurb no longer says *self-contained*: it says nothing later in the
  part assumes it and Part XI does.
- `world/tickets-and-loading` — a new paragraph claims `ChunkResult` is the
  two-case type all three holder futures carry and that
  `ChunkHolder.UNLOADED_LEVEL_CHUNK` is simply its shared failure, whose message
  is *Unloaded level chunk*. The spectator answer gains a claim that the skip is
  **remembered** in a `PlayerMap` at join rather than re-asked. The renamed
  section *Which chunks a player is owed, and what makes one eligible* claims
  that the BLOCK_TICKING row is the join between the two systems — nothing is
  sent that the server is not also simulating.
- `world/chunk-generation-pipeline` — a new paragraph on the *EMPTY* step
  claims that a null parse and a thrown load both end at
  `ChunkMap.createEmptyChunk`, that the position is marked replaceable in
  `ChunkMap.chunkTypeCache`, and therefore that **an unreadable chunk is
  regenerated, not skipped**. Three passages cut to citations now claim their
  owners: the level→status line to `tickets-and-loading#the-number-line`, the
  synchronous ask to `#when-the-graphs-run`, the pool sizing to
  `anatomy#four-threads-worth-memorising` with the new claim that "the only knob
  is the pool's, and widening the pool widens everything else that shares it".
- `world/chunk-storage` — a new section *The other store under* data/ claims
  `SavedDataStorage` encodes on the caller's thread and writes on the IO pool,
  at most `Util.maxAllowedExecutorThreads` at a time, chained through
  `SavedDataStorage.pendingWriteFuture`, with `SavedDataStorage.saveAndJoin` the
  only wait — moved from `reference/level-data-and-rules`, which now cites it.
  A new section *Doing all of it at once, with no server running* claims
  `WorldUpgrader` runs one daemon thread named *World Upgrader*, hands each of
  the three stores to a `RegionStorageUpgrader`, optionally recreates region
  files (which compacts a fragmented save), and reports through
  `UpgradeProgress` — and that nothing there loads, generates or consults a
  status.
- `world/environment-attributes-and-timelines` — a new paragraph claims
  `ClockState` is the saved form and `PackedClockStates` the saved map,
  `ClockNetworkState` the wire form, that **the difference between the two is
  the paused flag**, and that `ClockManager` is a one-method interface which is
  why `AttributeTrackSampler` is the same class on both sides.
- `world/points-of-interest` — a new callout, ***A village is made of loaded
  sections only***, claims `PoiManager.isVillageCenter` alone in the query
  family reads through the non-loading `SectionStorage.get`, treats its null as
  *not a centre*, and that this is deliberate because the flood settles every
  tick and must not touch the disk.
- `world/scheduled-ticks` — the random-tick section is cut to the contrast and
  now claims two things as its own: that at the edge of simulation distance
  there is **a ring of chunks where appointments come due and nothing is chosen
  at random**, and that a random tick's eligibility is baked in at
  `BlockBehaviour.BlockStateBase.initCache` **before the world exists**, unlike
  an appointment, which is checked against the world when it comes due.
- `world/chunk-anatomy` — the ticker section, renamed *What step 11 leaves
  behind, and what the chunk goes on holding*, claims the handle belongs to the
  chunk and outlives the block entity in it. The step-8/9 paragraph now claims
  step 9 is "the only step whose whole job is to notice that the world moved
  underneath it".
- `world/fluids` — claims `LiquidBlockContainer` is the interface
  `SimpleWaterloggedBlock` narrows to water, and that the client holds the
  predicted bucket write until the acknowledgement arrives (a citation of
  `prediction-and-acks#the-six-windows`, added where the page previously said
  only "with no round trip").
- `world/lighting` — claims a section is not meshed at all until
  `LevelLightEngine.lightOnInColumn` is true for each of its eight surrounding
  columns, so a light flag decides whether a section may have a mesh (the same
  claim as before, now stated once and cited rather than told twice).
- `server/server-level-tick` — now claims `ServerChunkCache.tickChunks` reads
  `GameRules.RANDOM_TICK_SPEED` once per level tick and hands it down (the page
  previously attributed the read to `ServerLevel.tickChunk`); and its
  scheduled-tick section claims only what belongs to the tick — the two calls,
  their order and their budget — citing `scheduled-ticks` for the drain order
  and the cancellation rule.
- `reference/level-data-and-rules` — claims four parts point at it (III, IV,
  VIII, XII) where it previously named only Part IV and the level tick; claims
  *the border has no lecture* and says why. Its game-rule ids no longer carry
  hand-copied defaults, because `gamerules.md` generates them.
- **Eighteen cross-part and nineteen within-part citations gained the owner's
  anchor.** Part IV carried **none** before this session. Each anchor is a claim
  that the named section is the answer; pass 9 should spot-check that the
  section under each anchor says what the citing sentence says it says.

### The tool bug — the seventeenth of the project, and the first that was hiding failures

`tools/check_links.py` scanned each page **line by line**, and its link regex
cannot match across a newline. The corpus hard-wraps its prose, so a link
written as `[tickets and\nloading](…)` was invisible to the gate: **243 of the
corpus's 7,811 links had never been checked**, and one of them was broken by
this session's own heading rename — `server/server-tick`:225 pointed at
`tickets-and-loading#what-the-player-is-sent-and-when` after the heading
changed, and the gate said clean. Fixed by matching against the whole page
outside its fences with a character-to-line map, so a link is still reported on
the line its `[` sits on. On the first run the fixed gate caught **two** real
broken anchors — that one and `world/README`'s `#packing-a-position`, an anchor
this session had invented and which the old gate would have published. The
number of anchors the gate actually checks went from 12 at pass 5's planning
session to 174, which is mostly this pass's own anchor work finally coming under
the gate. `--probe` now writes a wrapped link with a bad anchor and a wrapped
link with a good one, and fails if either is misjudged.

**For pass 9:** every anchor added by pass-5 sessions A, B and C was written
while the gate was blind to wrapped links. They are checked now, but they were
not checked when they were written.

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
