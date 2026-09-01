# The plan — the passes

*Rewritten 2026-09-01, at the end of pass 1. This is the document every
session reads first and ticks last. Pass 1's catalogue, protocol and
session log are archived in [pass1.md](pass1.md); the running work queue
for the current pass is [pass2.md](pass2.md).*

## Where we are

Pass 1 is done: fifty-six pages, thirteen parts, twelve sessions, all
deployed, every name verified. What pass 1 could not guarantee is that
the *claims* attached to those names are true (the verifier checks
existence, not truth), that nothing in scope was missed, or that the
uniform page-per-system format is the most interesting shape for each
part. That is what the remaining AI passes are for — the corpus gets
correct, then complete, then well-shaped, then well-written, and only
then does the owner spend reading time on it.

The planned pass-1 closing session (16) never ran; its to-dos are folded
into pass 2's queue in [pass2.md](pass2.md).

## The passes

| pass | what | status |
|---|---|---|
| **1 — rough draft** | every page drafted from the decompile, names verified | done — [pass1.md](pass1.md) |
| **2 — completeness and accuracy** | every claim fact-checked against the decompile; gaps filled; pages split/added freely — length is not a concern here | **current** |
| **3 — restructuring** | each part gets the shape of the system it explains; diagram/image plan; lecture order drafted | next |
| **4 — polish** | wording, per page; corpus-wide consistency sweep; cut what pass 2 over-added | after 3 |
| **5+ — human feedback** | the owner reads part by part with the decompile open; `<!-- Q: … -->` comments answered in the prose; lecture order confirmed; then voice and cuts | after 4 |

The rules stand for every pass: names never code · how the system works,
not how the code reads · newest version only (26.2) · trace-driven ·
`python tools/verify_names.py` clean before every commit that touches a
page. And the pass-1 addition still stands: claims come from the
decompile, never from model memory of 1.21.

---

## Pass 2 — completeness and accuracy (current)

**Goal:** everything the corpus should say is on the site, and everything
the site says is true. Do not worry about page length — add and split
freely in the name of completeness; pass 4 cuts.

### Accuracy: the fact-check protocol

`verify_names.py` proves a name exists; it cannot prove a claim true. So
each page gets an **adversarial fact-check**: one agent per page, given
the page and access to `reference/26.2`, whose brief is to *falsify*,
not confirm — re-derive from the decompile every checkable claim (which
thread runs it, who calls whom in what order, what crosses the wire and
when, which class owns which state, every "invariant and surprise") and
return a discrepancy list: **wrong** (the decompile disagrees),
**unverifiable** (the page asserts something the agent could not find),
or **misleading** (true but the emphasis implies something false). The
session fixes the page from the list. An empty discrepancy list from an
agent that quotes no decompile evidence is a failed check, not a pass.

The *Load-bearing facts* section of [pass2.md](pass2.md) — each stated
once, in one page — is the seed list: those get checked hardest, because
every other page leans on them.

### Completeness: the inverse question

The same agent answers: *what is in this page's scope in the decompile
that the page never mentions?* — plus the standing queue in
[pass2.md](pass2.md): the split candidates, the catalogue gaps needing
a ruling (the debug cluster, `client/resources`, `client/animation`,
`util/parsing`, Blaze3D's Vulkan/platform halves), and the pass-1
closing-session leftovers. Known new-page work already agreed:

- **`environment-attributes-and-timelines`** — the most load-bearing gap:
  four written pages explain `world/attribute` / `world/timeline`
  piecemeal without owning it. Write it (Part IV, or a short part of its
  own), then cut the borrowed paragraphs out of `biomes` and
  `lightmap-fog-and-sky`.
- **The rendering split.** Part X currently holds two subjects. It
  becomes **Part X · The client** (the loop and tick/frame interleave,
  `ClientLevel`, input and options, GUI and screens, the HUD, sound) and
  a new **Part XI · Rendering** (`the-frame` as the opening trace,
  `blaze3d`, `level-rendering`, `models-and-atlases`, `entity-rendering`,
  `lightmap-fog-and-sky`, `particles`), with new pages where pass 1
  found lectures hiding inside pages — the text/font engine out of
  `gui-and-screens`, and possibly the frame graph out of
  `level-rendering`. Later parts renumber (worldgen → XII, commands →
  XIII, appendix → XIV); the exact page allocation is the client
  sessions' call, this is the default.
- Splits from the [pass2.md](pass2.md) table are executed in this pass
  **when the fact-check adds material and the page is carrying two
  subjects anyway**; splits that are purely about presentation wait for
  pass 3.

### Session protocol

One session = one part (small parts bundle, as in pass 1). Each session:

1. **Read** this file, `CLAUDE.md`, and the part's entries in
   [pass2.md](pass2.md) (split candidates, load-bearing facts, gaps).
2. **Check** — spawn one fact-check agent per page, in parallel, with
   the brief above. Fact-check output is not committed.
3. **Fix** — correct every *wrong*, resolve every *unverifiable* (fix
   the page or confirm against the decompile and keep it), add what the
   completeness question surfaced, execute this part's agreed splits and
   new pages.
4. **Verify** — `verify_names.py` clean; `mdbook build` clean;
   `SUMMARY.md` and cross-links updated; regenerate `class-index` if
   pages moved.
5. **Ship** — commit (`pass 2, Part N: <summary>`), deploy, tick the
   part in the schedule below, log below. Anything left for later is
   written down as it is found, not at the end: **structural
   observations** (part shape, page/lecture boundaries, diagram shape,
   lecture order, dependencies) go to [pass3.md](pass3.md); **wording
   debt and material added on spec that pass 4 may cut** go to
   [pass2.md](pass2.md)'s hand-off section.

Three protocol notes, all cheap and all load-bearing:

- **Always ask the fact-check agent for a NAMES section.**
  `verify_names.py` matches a token anywhere in the named class's file,
  so a member *called* in class A but *declared* on class B passes the
  verifier and is still a wrong citation. Only the agent catches those.
- **Distrust a page that has never been checked, not just an overloaded
  one.** All eight of session A's pages had at least one *wrong* claim,
  including the three shortest. Session B's four had **twenty-nine** between
  them; the shortest page had six.
- **Verify the agent, not just the page** *(session B)*. Fact-check reports
  are long and confident, and a session that applies them wholesale is
  trusting an unaudited agent. Session B re-read the decisive decompile
  methods — `MinecraftServer.runServer`, `tickChildren`, `stopServer`,
  `ServerLevel.tick`, `ServerChunkCache.tick`, `Connection.tick`,
  `PacketProcessor` — before editing, which cost about ten reads and caught
  the ordering questions the reports disagreed on. Do this for every *wrong*
  finding that changes a trace; take the *completeness* findings on trust.

Three protocol notes have now been added by three consecutive sessions;
session C adds a fourth: **suspect the tool once before rewording the
page.** A name you are certain about that fails `verify_names.py` is
occasionally the verifier's bug, not yours — session A found one in
`gen_reference.py`, session C found one in `verify_names.py` itself. Run
the verifier after each page rather than at the end, so a systematic
failure is localised to the page that provoked it.

### After-session housekeeping

Every session ends with the same five: naming drift written to **both**
`docs/pass2.md` and `src/systems/appendix/naming-drift.md`; structural
observations to `docs/pass3.md`; on-spec additions and wording debt to
`docs/pass2.md`'s hand-off; the load-bearing-facts list extended with
anything a later part will lean on; and a check that the session's findings
do not now contradict a page in another part. Session B's flush correction
had to be applied to `anatomy` and `the-connection` as well as its own pages
— **grep the corpus for every corrected claim, not just the page you were
given.**

### Schedule

Part order as in pass 1, with the pass-1 leftovers first. Tick as done.

- [x] **Session A** — Part I `anatomy` (re-read against the finished
  corpus: the render-thread claim, the threads table vs
  `reference/threads.md`) + `sound` (predates the extract/render split)
  + Part II Foundations. *(2026-09-01)*
- [x] **Session B** — Part III The server. *(2026-09-01)*
- [x] **Session C** — Part IV The world, plus the new
  `environment-attributes-and-timelines` page. *(2026-09-01)*
- [ ] **Session D** — Part V Blocks.
- [ ] **Session E** — Part VI Entities.
- [ ] **Session F** — Part VII Items · Part VIII The player.
- [ ] **Session G** — Part IX Networking.
- [ ] **Session H** — Part X: the client half, and the X/XI split lands
  here (SUMMARY, renumbering, redirects if any).
- [ ] **Session I** — Part XI Rendering: the render half plus its new
  pages.
- [ ] **Session J** — Part XII World generation.
- [ ] **Session K** — Part XIII Commands · Part XIV Appendix (the gaps
  list gets its rulings here; naming-drift and glossary re-swept after
  every earlier session's changes).

---

## Pass 3 — restructuring (sketch; charter written when it starts)

Is each part presented in the most interesting shape? The uniform
template served pass 1; pass 3 lets the structure of the documentation
mirror the structure of the code. Small self-contained systems (blocks,
foundations) stay short self-contained pages. Long sequential systems
(rendering, worldgen, the chunk pipeline) should *read like a pipeline*
— a part-level through-line where each page hands off to the next.
Networking is two connected pipelines meeting at the wire and should
read like one. Also in this pass:

- **Diagrams and images.** Plan visuals part by part: where a diagram
  replaces a wall of text, which existing diagrams are wrong-shaped
  (sequence where the truth is a graph). The standing convention is
  mermaid-in-page, never images; if static images are wanted, that is a
  deliberate decision here — pipeline, format, theming, where they live
  — not a drift.
- The **lane-abbreviation standard** for sequence diagrams (`SGPL`/`CPL`
  is the pass-1 majority; settle it corpus-wide).
- **Draft the lecture order** into `src/lectures.md` — restructuring and
  lecture order are the same judgement. The owner confirms it in pass 5.

## Pass 4 — polish (sketch)

Per page: does it read well, is everything needed explained and nothing
more? This is where pass 2's "don't worry about length" bill comes due —
cut what over-grew, using pass 2's on-spec log. Corpus-wide: one
terminology sweep (the glossary is the checklist), one voice sweep
against the best page, links and cross-references complete.

## Pass 5+ — the owner reads

Unchanged from the original conception: part by part, decompile open,
questions left **in the page** as `<!-- Q: … -->` comments; a session
answers each in the prose — if the owner had to ask, the page was wrong
or missing it — and removes the comment. The owner confirms or reorders
`lectures.md`. Then voice and cuts, and recording.

## Risks

- **The rubber-stamp fact-check.** An agent that confirms instead of
  falsifies makes pass 2 worthless. The brief demands discrepancies or
  quoted evidence; sessions should distrust clean reports on pages the
  split table already calls overloaded.
- **Growth without limit.** Pass 2 adds freely by design; passes 3–4
  must actually cut. Every session logs what it added speculatively.
- **26.3 lands mid-pass.** Finish the current pass on 26.2; re-verify
  the whole corpus once, in one session, between passes.
- **Renumbering churn.** The X/XI split renumbers three parts; do it in
  one session (H), everywhere at once, or links rot.

## Session log — pass 2 onward

- **2026-09-01, session C** — Part IV The world: eight adversarial
  fact-checks, eight rewrites, and the **57th page written** —
  `environment-attributes-and-timelines`, the pass-1 catalogue gap that four
  parts had been leaning on. The pattern from A and B holds: every one of the
  eight had at least one *wrong* claim, and this time the errors clustered in
  **thread attribution** and **file paths** rather than in orderings. What
  mattered most:
  - **The new page.** `world/attribute` and `world/timeline` are one system
    with a fixed four-layer stack — dimension, biome, timelines, weather —
    baked once per level and never rebuilt. 48 attributes in three
    namespaces; exactly two are non-positional; a biome may set only
    positional ones and a data pack that tries fails to load. The
    modify-don't-set model (`EnvironmentAttributeMap.Entry` is an argument
    plus an `AttributeModifier`) is the design decision everything rests on:
    the night curve *multiplies* sky light rather than setting it, so it
    composes with whatever the dimension and biome produced. The wire carries
    the rules, not the values — `Registries.TIMELINE` and
    `Registries.WORLD_CLOCK` are synced and the client rebuilds the same
    stack, adding spatial (216 Gaussian biome samples per tick) and
    partial-tick smoothing the server never does. And `WorldGenRegion`
    answers every attribute with its default, so generation cannot depend on
    the time of day. Session A's and B's dependants (`sound`, `biomes`,
    `lightmap-fog-and-sky`, `block-ticks-and-fluids`, `ai-goals-and-brains`,
    `server-level-tick`) now link here; the borrowed explanations were cut
    out of `biomes` and `lightmap-fog-and-sky`.
  - **`tickets-and-loading` mis-attributed its own asynchrony.** The
    player-ticket throttler runs its task on the **main thread** — the
    worker only does the queue bookkeeping — so the page's "each runs on a
    worker" and its diagram's worker→main hop were both wrong.
    `TicketType.ENDER_PEARL` is loading *and* simulation (flags 14), not
    simulation alone. `ChunkHolder.sendSync` starts complete and
    `ChunkMap.waitForLightBeforeSending` has exactly one caller,
    `EnderDragonFight` — the page presented an End special case as the normal
    send gate. `MainThreadExecutor.pollTask` short-circuits: if the distance
    updates did anything, no light schedule and no queued task that poll, so
    propagation *starves* the chunk queue rather than sharing with it.
  - **`chunk-storage` had `forceSynchronousWrites` backwards.** The base
    class returns true; both subclasses override it, and the integrated
    server takes the client option whose default is **Windows only** — so
    singleplayer on Linux or macOS runs without DSYNC by default, the
    opposite of what the page said. Datafixing turned out to live on the
    worker pool between the IO lane and `parse`, which the page located on
    the lane. And the crash-safety invariant does not hold for oversized
    chunks: a `.mcc` sidecar is moved into place *after* the header is
    committed.
  - **`level-data-and-rules` had eleven wrong file paths.** Every `SavedData`
    id is an `Identifier`, so every file is under *data/&lt;namespace&gt;/*; the
    page had them all one folder up. Also: five game rules reach the client,
    not three (`GameRules.ADVANCE_TIME` broadcasts a clock sync);
    `ClientboundLoginPacket` carries hardcore but not difficulty;
    `MinecraftServer.updateMobSpawningFlags` sends no packet at all; and
    every level reports the server's *effective* respawn data, which is
    relocated if the stored spawn has fallen outside the border.
  - **`lighting` over-counted its own dirtying.** A write marks the sections
    touching the block — one, or up to eight on a corner — not 27; the 3×3×3
    marking fires only when a section is first allocated a `DataLayer`. "No
    light is computed on the server thread" was too strong:
    `ChunkSkyLightSources.update` runs inline. And what stops a chunk
    shipping half-lit is the pyramid's radius-1 `INITIALIZE_LIGHT`
    requirement, not a send dependency.
  - **`chunk-anatomy`'s three headline invariants were each slightly
    false.** Promotion copies the section *array* (the sections are shared);
    `ThreadingDetector` kills **both** threads and the winner throws first;
    and `PalettedContainer.pack` uses the same tier ladder as memory, so
    packing shrinks the palette rather than the width.
  - **`chunk-generation-pipeline` mis-stated the ticket→status map** (34 is
    *INITIALIZE_LIGHT*, not *SPAWN*), counted eleven pass-through layers
    where there are seven, and had three radius-0 dependencies missing from
    its table — including *SURFACE* needing *NOISE*, which is the one that
    stops a surface build reading un-noised terrain. The pyramid is also
    chosen per chunk per layer, not per task, which is what stops
    already-generated neighbours being regenerated.
  - **`block-ticks-and-fluids`** had `getNewLiquid`'s three branches in the
    wrong precedence, missed that an empty result reschedules **nothing**,
    and attributed `LiquidBlock.tick` to the wrong callee. Its best new
    surprise: **lava random-ticks twice** per selected position, once as a
    block and once as a fluid.
  - **`game-events-and-poi`** miscounted the registry (61, not 62), had the
    wake-up chain going through `SleepInBed` when `WakeUp` calls
    `stopSleeping` itself, put the sensor's cooldown after `deactivate`
    rather than started by it, and — the best find — standing *on* a sculk
    sensor bypasses `isValidVibration` entirely, so **sneaking does not
    protect you when you are on the sensor**.

  Tool fix: `verify_names.py`'s `RECORD` regex required `record Name(` and
  so could not see the components of a **generic** record — five correct
  citations on `AttributeType` failed. Fixed; the new protocol note is
  *suspect the tool once before rewording the page*.

  Split rulings: neither Part IV split was executed. `game-events-and-poi`'s
  seam is confirmed real (the two fact-check halves shared no classes) but
  purely presentational; `block-ticks-and-fluids` was **added** to the split
  table as a new candidate — the scheduler and the fluid model are two
  lectures and the page's own trace changes subject halfway. Both are in
  [pass3.md](pass3.md) §2, along with the part-shape finding: Part IV is a
  genuine forward-only pipeline of four pages with a data page in front and
  three unrelated pages behind it, and it is the first part in the corpus
  whose internal order is a real dependency chain.

- **2026-09-01, session B** — Part III The server: `server-tick`,
  `server-level-tick`, `players-and-sessions`, `server-lifecycle`. Four
  adversarial fact-checks, four rewrites, twenty-nine *wrong* findings
  between them — the shortest page had six. Session A's conclusion holds and
  hardens: **a page that has never been checked is wrong somewhere, and the
  wrongness clusters in orderings and in "only/never" claims.** The four
  that mattered most:
  - `server-tick` said outbound packets leave **once** per client per tick.
    They leave twice: `Connection.tick` flushes the channel unconditionally
    inside the `suspendFlushing`/`resumeFlushing` bracket, so the levels' and
    the player's own traffic goes in the connection phase and only the chunk
    batch rides the resume. The same wrong claim was in `anatomy` and — in a
    bullet that contradicted its own first sentence — in `the-connection`;
    both were fixed. Also: a throwing packet handler is logged and
    *suppressed*, not disconnected (`ClientboundDisconnectPacket` comes from
    a throw out of `Connection.tick` instead); the "Can't keep up!" log and
    the deadline skip are one condition, so a server that warned recently
    stays behind; `MinecraftServer.haveTime` is true whenever a task is
    running and is bypassed entirely inside `managedBlock`, which is the
    mechanism that keeps a mid-tick chunk wait from deadlocking and was
    absent from the page; and the tick-time ledger and the debug TPS chart
    are two separate pipes written from three separate places.
  - `server-level-tick` had the **broadcast and tracking steps inverted** —
    `ServerChunkCache.broadcastChangedChunks` runs before `ChunkMap.tick`,
    so block changes are queued ahead of the same tick's entity movement. The
    broadcast unit is the 16³ section, not the chunk. `purgeStaleTickets` *is*
    freeze-gated, against a page that said the whole chunk system was not. An
    empty dimension does not stop after 300 ticks; it skips exactly three
    steps and the entity manager keeps draining. The tick's **first**
    statement — `EnvironmentAttributeSystem.invalidateTickCache` — and its
    **last** — `LevelDebugSynchronizers.tick` — were both missing. All three
    load-bearing facts (`ServerClockManager`, the server-global `WeatherData`,
    and `forEachBlockTickingChunk` walking the entity-ticking set) were
    **confirmed with evidence**, which is the first time the seed list has
    been independently re-derived.
  - `players-and-sessions` attached `canBypassPlayerLimit` to the whitelist
    (it is the capacity check; the whitelist is bypassed by being an op),
    gave a joining player ten unacknowledged chunk batches (it is one until
    the first ack), called `restoreFrom`'s restore-everything branch the
    *keepInventory* path (it is the end-credits return), and implied the
    registry sync and the spawn-chunk load overlap (configuration tasks are
    strictly sequential). Four members were cited on the wrong class —
    caught only by the NAMES section, exactly as session A predicted. Gained
    `NameAndId`, the `LevelBasedPermissionSet` model, `IntegratedPlayerList`,
    `ServerPlayerGameMode` and the `switchToConfig` exit path.
  - `server-lifecycle` said shutdown calls `saveEverything` (it calls
    `PlayerList.saveAll` and `saveAllChunks` by hand), that
    `ServerConnectionListener.stop` closes client connections (it closes only
    the bound channels — live sessions die with `PlayerList.removeAll`, and a
    connection still in login is closed by neither), that
    `MinecraftServer.isReady` is what the "Done" message waits for (that is
    logged before the loop starts), and that there is a persisted spawn
    ticket (there is not: only `TicketType.FORCED` and `TicketType.PORTAL`
    persist, so `prepareLevels` loads nothing on an ordinary world). Its
    closing invariant was backwards — a tick-loop crash saves the world, a
    **watchdog kill does not**, because `System.exit` runs a hook that joins
    the very thread that is wedged.

  Split ruling: `server-lifecycle` was **not** split, and the pass-2 table's
  proposed seam (lifecycle vs the side threads) was rejected — the side
  threads are four bullets with no trace of their own, and the page's real
  seam is its two traces. Recorded in `docs/pass3.md` along with the
  strongest new-page candidate the session found: *how a Minecraft server
  dies*, three endings and one diagram, currently three bullets.

  Protocol addition: **verify the agent, not just the page.** Ten decompile
  re-reads before editing settled every ordering question the reports raised
  and is now in the session protocol.

- **2026-09-01, session A** — Part I `anatomy`, `sound`, and all six Part
  II Foundations pages: eight adversarial fact-checks, eight rewrites.
  **The protocol works and the corpus needed it.** Every one of the eight
  pages had at least one *wrong* claim, and three had claims that were
  exactly inverted. The worst of them:
  - `sound` said "nothing outside `client/sounds` touches OpenAL" when
    *only* `com/mojang/blaze3d/audio` does, and its headline trace
    followed a block **break** — which is a level event and never reaches
    `Level.playSound` at all. Retraced on block placement, with the
    level-event path documented as the larger second path. Music and
    ambience turned out to have moved to `EnvironmentAttributes` (a fifth
    dependant for session C's new page).
  - `anatomy` called the HUD `Gui` (it is `Hud`, held as `Gui.hud`), had
    `runTick`'s steps in the wrong order, claimed two concrete
    `MinecraftServer` subclasses (three), claimed Netty never runs game
    logic (handshake and login run entirely there), and said
    `MinecraftServer.haveTime` gates chunk loading (it gates unloading,
    eager saves and section-storage flushing — and sprinting polls chunk
    sources *more*). Gained the three missing dedicated-server threads,
    and `src/reference/threads.md` was re-synced because it had the same
    gaps.
  - `tags` was wrong about which thread `/reload` runs on, about apply
    being atomic (three unsynchronised steps), and about tag reads
    throwing before the first bind (they return empty).
  - `data-components` misattributed the container-sync call, miscounted
    the slash-namespaced types, and described `validateStrict` as
    recursive (it reaches one level).
  - `identifiers-and-registries` had an off-by-one registry count, the
    wrong purpose for `MappedRegistry.componentLookup`, and a `Lifecycle`
    rule that reads `KnownPack.isVanilla` and then discards it.
  - `codecs-nbt-json` said a mixed `ListTag`'s wrapper is never written
    (it is, on every write), and built an invariant on
    `ByteBufCodecs.TRUSTED_TAG`, which has no call sites.
  - `resource-system` described a snapshot of file *contents* (it is a
    snapshot of the pack list), had the pack-precedence direction
    unanchored, attributed the atlas→model dependency to apply order (it
    is a `PreparableReloadListener.SharedState` channel resolved in
    prepare), and said a failed reload deselects the offending pack (it
    deselects all of them, or crashes).
  - `math-and-primitives` credited `Cursor3D` to `BlockPos`, credited
    `BlockBox` with structure bounds (it has zero call sites; that is
    `BoundingBox`), and missed that `LegacyRandomSource`'s atomic is a
    *threading detector* that crashes on cross-thread use.

  Also: found and fixed a **generator bug** — `gen_reference.py`'s
  component regex used `\w+` for the id, silently dropping all 29
  slash-namespaced components, so `reference/components.md` had claimed
  82 of 111 since pass 1. Class index regenerated (2,163 classes). Both
  pages that lacked the standard rules footer (`anatomy`, `sound` — the
  only two in the corpus) now have it. `docs/pass3.md` opened as the
  restructuring notebook and filled in for Parts I and II.

  Decisions and observations recorded rather than acted on: Part II is
  six pages of three different kinds and `math-and-primitives` is not a
  lecture at all (pass 3); `sound` is the best-argued split candidate
  outside the pass-2 table but was left whole; `verify_names.py` proves a
  name *exists*, not that it is declared where it is cited, which let two
  wrong citations through — so every fact-check agent must be asked for a
  NAMES section.

- **2026-09-01, planning session** — pass 1 closed out and archived to
  [pass1.md](pass1.md); this plan written (passes 2–5); pass2.md
  repurposed from "the owner's read" to the pass-2 work queue (the
  owner's read is now pass 5); CLAUDE.md updated to match. Decisions:
  closing session 16 folded into pass 2; adversarial per-page
  fact-check protocol; rendering split out of Part X into its own part;
  `environment-attributes-and-timelines` page approved; lecture order
  drafted in pass 3 rather than deferred to the owner.
