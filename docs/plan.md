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

Every session since has added one. Session C's is **suspect the tool once
before rewording the page.** A name you are certain about that fails `verify_names.py` is
occasionally the verifier's bug, not yours — session A found one in
`gen_reference.py`, session C found one in `verify_names.py` itself. Run
the verifier after each page rather than at the end, so a systematic
failure is localised to the page that provoked it.

Session E adds a sixth, and it is the one with the worst failure mode:
**ask which side is *authoritative*, not which side runs the code.** Both
sides run `Entity.tick` for a tracked mob; only one of them runs its physics,
because `LivingEntity.aiStep` gates travel on `Entity.canSimulateMovement`.
`movement-and-collision` had a whole "when it runs" section, and an invariant
headed *Both sides run the physics*, built on the first observation without
ever checking the second — and a page can be right about the call graph and
backwards about the system. The tell is a page that establishes "the same
code runs on both sides" and then never says what each side is allowed to
*do* with it. Ask the fact-check agent, for every shared code path, which
side is authoritative and what the other one does instead.

Session F adds a seventh, and it is the cheapest of the lot: **make the
agent count the call sites.** Sessions D and E found conditions wrong on a
path; session F's errors were almost all *cardinality* — a rule stated
correctly with the wrong number of exceptions. "Only the server's
synchronizer bumps the state id" (three call sites, one of them elsewhere);
"no enchantment effect runs on the client" (two value effects do); "the only
override of `Item.finishUsingItem` in the item package" (it is the only one
anywhere); "an `Ingredient` cannot be empty" (a tag can make one); "twenty-five
named sets" (twenty-six); "forty loot functions" (forty-three); "thirty
component keys" (thirty-one); "there is a second melee path" (there are
three). **Every sentence containing "the only", "exactly one" or a count is a
question for the agent**, and the answer is a grep it can run in seconds.
Ask for the *complete* caller or implementor list for any claim of the form
"only X does Y", and take the count from the report rather than the page.

Session G adds an eighth, and it is about the tooling rather than the
page: **re-derive by hand any number a page took from a tool.**
`packets-and-stream-codecs` said "225 packet types" and was quoting
`src/reference/packets.md`, which was quoting `tools/gen_reference.py`,
whose regex required the packet's type parameter to be `\w+` — so the
seven nested types (`ClientboundMoveEntityPacket.Pos` and siblings) were
dropped without a warning. The real number is 232. A generated catalogue
reads like evidence and is really just another claim; this is the third
pass-2 session to find a bug in one of these two scripts, and the first
where the bug had already been copied into prose. Fix the tool,
regenerate, and check whether any page repeated the number.

Session H adds a ninth, and it is about *scope* rather than accuracy:
**ask the coverage question with a tool, once per part, before writing.**
Every session so far has answered "what is missing?" per page, from the
page's own point of view — which cannot see a package no page mentions.
Session H spent one agent on a mechanical inventory instead: every package
under `net/minecraft/client/`, real class and line counts from `find` and
`wc`, each one grepped against the corpus and marked covered, mentioned or
absent. It found ~4,900 lines of a coherent, undocumented **server-push
debug subscription pipeline** that eight per-page fact-checks had all
walked past, because no existing page was in its neighbourhood. It also
produced a rule worth keeping: **`server-classes.txt` contains no entry
under `net/minecraft/client/` or `com/mojang/blaze3d/`** — the client tree
is client-only without exception, so that whole class of side-attribution
error cannot occur there. One cheap agent, and it changed the shape of the
part.

Session I adds a tenth, and it is the counterweight to the ninth:
**a fact-check agent's *names* are as suspect as the page's.** Session I's
reports were the strongest of the pass — six of seven found a reversed
invariant — and two of them cited a method that does not exist. One had the
rain/snow scatter as *ClientLevel.tickPrecipitation* (it is
`ClientLevel.tickWeatherEffects`; the name it used belongs to `ServerLevel`);
another attributed a throw to `LevelRenderer.submitFeatures` when the throw
is in `LevelRenderer.checkPoseStack`. Both would have passed
`verify_names.py` had they reached a page, because the token appears
somewhere in the right file. The agent re-deriving your page's citations is
producing citations of its own, under no verifier at all — so **run the
verifier after applying each report, not after applying all of them**, and
treat any name you have not personally grepped as the agent's claim rather
than the decompile's.

Session J adds an eleventh, and it is aimed at this file's own artefacts:
**re-derive the load-bearing facts hardest, because they rot invisibly.**
The *Load-bearing facts* list in [pass2.md](pass2.md) exists so that a fact
stated once can be leaned on everywhere — which means a wrong entry is a
wrong entry in every page that trusted it, and none of those pages will
show the error. Three of Part XII's seed entries were wrong: the
density-function caches key on identity (only three of six do), carvers
never place air (the aquifer answers air above the water table), and the
biome shapes the terrain (neither shapes the other; both come off the same
noise router). All three had the same signature — **a true observation with
an invented causal story attached**, written as an absolute because the
*invariants and surprises* section rewards absolutes. The status order
really is biomes-before-noise; "so the biome shapes the terrain" was the
page explaining a fact it had not checked. When a load-bearing entry states
both a mechanism and a reason, **the reason is the part to re-derive** —
and when a page's own best surprise rests on one, check which side of the
surprise each consumer is actually on. `biomes` sold "two biomes per block"
and put grass colour on the wrong one.

Session D adds a fifth: **hunt the unstated conditional.** Nearly every
session-D error was a claim that held in the traced case and was written as
though it held always — a hook skipped "because the block didn't change"
when the real gate is the side; "every refusal is answered with a block
update" when three of five refusals answer differently; "later in the tick"
for a broadcast that is next tick. The template invites this: *invariants
and surprises* rewards absolute sentences. When fixing a page, ask of every
"always", "never", "only" and "the" whether the decompile's condition is the
one the page names — and ask the fact-check agent for the **gates** on each
call, not just the call order.

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
- [x] **Session D** — Part V Blocks. *(2026-09-01)*
- [x] **Session E** — Part VI Entities. *(2026-09-01)*
- [x] **Session F** — Part VII Items · Part VIII The player. *(2026-09-01)*
- [x] **Session G** — Part IX Networking. *(2026-09-01)*
- [x] **Session H** — Part X: the client half, and the X/XI split.
  *(2026-09-01)*
- [x] **Session I** — Part XI Rendering: the render half plus its new
  pages. *(2026-09-01)*
- [x] **Session J** — Part XII World generation, plus the new
  `hand-built-structures` page. *(2026-09-01)*
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

- **2026-09-01, session J** — Part XII World generation (`worldgen-pipeline`,
  `density-functions`, `biomes`, `features-and-placement`, `structures`), a
  mechanical coverage inventory of the whole worldgen tree, and a research
  agent on what it found. Five adversarial fact-checks, five rewrites, one
  new page; 1,364 lines became 1,661 across the five, plus 300 new. The
  A–I pattern holds — every page had *wrong* claims.
  **Session J's centre of gravity is the load-bearing fact that was half
  true.** Where F miscounted exceptions and I inverted invariants, Part
  XII's worst errors were facts on the *seed list itself* — three of them —
  each correct in the case that had been traced and written as an absolute.
  A fact promoted to "load-bearing" is a fact several pages lean on without
  re-deriving, so it is exactly the kind that rots unnoticed. What mattered
  most:
  - **"Density-function caches key on object identity" was half wrong, and
    the wrong half was the load-bearing one.** Only three of the six do the
    identity test. `NoiseChunk.FlatCache` and `NoiseChunk.Cache2D` key on
    **position**, which is precisely what makes
    `NoiseChunk.cachedClimateSampler` and `NoiseChunk.preliminarySurfaceLevel`
    cheap — the page had drawn "a single-point sample bypasses the caches"
    from the half that holds. The tell was structural and in plain sight:
    `Cache2D` is the one nested class that is `static`, so it *cannot* hold
    a reference to compare against.
  - **"Carvers never place air" is exactly backwards.** `Aquifer.FluidStatus.at`
    answers plain air above the local water table; every dry cave is the
    carver writing air. And `NetherWorldCarver` overrides
    `WorldCarver.carveBlock` and never consults the aquifer at all. The
    page's *mechanism* was right and its headline was the negation of it.
  - **"The biome shapes the terrain, never the reverse" is wrong in both
    directions.** `NoiseBasedChunkGenerator.fillFromNoise` never reads a
    biome, and the biome is itself read off the terrain-shaping functions —
    `RandomState` builds the `Climate.Sampler` from `NoiseRouter.depth`,
    `continents`, `erosion` and `ridges`. Neither causes the other; both
    come off one router. The status *order* was right and the causal story
    invented to explain it was not, which is the shape to watch for.
  - **The page's own best surprise was half inverted.** `biomes` sold "two
    biomes per block, and different systems use different ones" and then
    put grass colour on the wrong side: `ClientLevel.calculateBlockTint`
    calls `LevelReader.getBiome`, the **fuzzed** path. What softens a colour
    boundary is the blur on top, not the lookup. Only the
    environment-attribute stack reads unfuzzed.
  - **Two more inversions with the same signature** — a true observation and
    a false consequence. `WorldgenRandom`'s draw counter is **dead** and
    every feature is reseeded absolutely, so "one extra draw shifts every
    feature after it" is the opposite of the truth. And the guard that makes
    cascading worldgen impossible is not the write-zone check on reads (that
    only *logs*) but `WorldGenRegion.getChunk` throwing at the dependency
    radius — nine chunks for FEATURES, not three.
  - **A side-attribution error of a new kind.** `ChunkGenerator.validate` is
    **client-only**: `WorldOpenFlows` calls it, catches the exception and
    offers safe mode. A dedicated server never calls it, so a feature-order
    cycle there is not a refusal to load but a crash on the first decorating
    chunk. Session E's rule was "ask which side is authoritative"; this is
    its cousin — *ask whether the failure path exists on both sides at all*.
  - **Cardinality, as usual:** 63 registered features not ~65, 63 noise keys
    not ~65, fifteen placement modifier types not fourteen, five 5×5 biome
    tables plus a 2×5 not six 5×5, two of four terrain adaptations
    kernel-weighted not all four, three `StructureProcessor`s named of
    eleven. Both "~65"s were the page hedging with a tilde instead of
    counting — session G's rule (re-derive any number a page took from a
    tool) extends to numbers a page took from its own estimate.
  - **`hand-built-structures` is new**, and it is the largest gap the pass
    has found: `levelgen/structure/structures` is 10,012 lines, 98% of it
    named nowhere, and it is the assembler **fifteen of the sixteen
    structure types actually use** — `structures` documents the jigsaw path
    and silently implies that is how structures work. Its best facts are
    that `StructurePiece.addChildren` is *not* a framework hook (empty
    default body, never called by the framework — every family arranges its
    own recursion), that a stronghold is a **rejection sampler** which
    discards and reseeds the entire graph until one contains a portal room,
    that growth stops when the piece *budget* is spent rather than when the
    depth cap is hit, and that `StrongholdPieces` keeps its generation state
    in **private static fields** mutated from chunk workers.
  - **The inventory found that ~53% of the worldgen tree by line count is in
    classes no page names** (272 of 429 classes, 24,512 of 46,628 lines).
    The ranked remainder is in [pass2.md](pass2.md): concrete features
    (5,928 lines, of which the *composition* features are the interesting
    part), the tree kit's implementations (3,219 — probably the most
    watchable page in the part), `Blender`/`BlendingData` (858, named in
    five pages and explained in none), and world creation + the world-select
    screens (~5,100, spanning Parts X and XII).
  - **First session to add no naming drift.** All thirteen Part XII rows
    were re-derived and hold — worth recording as a positive result about
    session 11's fact sheets rather than a gap.
  - **Structural notes to [pass3.md](pass3.md):** Part XII is a pipeline
    with a substrate underneath it and `density-functions` is sitting in the
    wrong place for either reading; `structures` is now three subjects, not
    the two the split table proposed, which may argue for promoting it to
    its own part; two of the five diagrams are the wrong shape, and
    `density-functions`' is the corpus's strongest case for a static figure;
    three internal lane collisions, of which `SS` and `TP` will actually
    mislead.

- **2026-09-01, session I** — Part XI Rendering (`the-frame`, `blaze3d`,
  `level-rendering`, `models-and-atlases`, `entity-rendering`,
  `lightmap-fog-and-sky`, `particles`), plus a mechanical coverage inventory
  of the whole rendering tree. Seven adversarial fact-checks, seven rewrites,
  one new page; 1,797 lines became 2,430 across eight pages. The A–H pattern
  holds: every page had *wrong* claims.
  **Session I's centre of gravity is the inverted invariant.** Where F found
  miscounted exceptions, G borrowed claims and H unowned ones, Part XI's
  worst errors were sentences that were *backwards* — six of the seven pages
  had at least one, and in every case the page had the call graph right and
  the meaning wrong. What mattered most:
  - **"The frame just stops" was exactly wrong, and it is the page's own
    next sentence that disproves it.** A failed surface acquisition does not
    abort `Minecraft.renderFrame`; the whole frame renders into the main
    target and only the blit and the present skip. A minimized window renders
    complete frames nobody will ever see, and what actually saves the work is
    `FramerateLimitTracker` dropping the limit to ten. The old page had
    written the heading and the refutation two lines apart.
  - **The meshing result does come back as a callback — the page said it
    did not.** `SectionRenderDispatcher.uploadTerrainBuffersToGpu` fires the
    per-allocation callback that publishes the mesh and re-arms the occlusion
    graph. And the occlusion graph's *full* BFS is a second thing on
    `Util.backgroundExecutor`, which is the whole reason its `GraphState`
    lives in an `AtomicReference` — a fact the page stated ("published
    atomically") without ever saying what it was published *from*.
  - **A cost model off by up to 27×.** "The 27 sections in the halo" is 27
    **block positions** mapped through `SectionPos.blockToSectionCoord` — one
    section for any block not on a boundary, at most eight when it is. Only
    the mesher's *read* region is genuinely 27 sections. The diagram had
    taught the wrong number to anyone reasoning about what a placed block
    costs.
  - **Two flashes, conflated in two parts.** `ClientLevel`'s two extra
    attribute layers are the **lightning** flash (`LightningBolt` sets it);
    `EndFlashState` is a free-running 600-tick End-sky flash with nothing to
    do with the dragon fight. Both `lightmap-fog-and-sky` and Part IV's
    `environment-attributes-and-timelines` had it wrong, in the same way —
    session B's grep-the-corpus rule earning its keep again.
  - **A load-bearing fact needed a qualifier, not a correction.** "Every
    per-dimension visual constant is an `EnvironmentAttribute`" is *nearly*
    true: `DimensionType.ambientLight` and `DimensionType.cardinalLightType`
    are plain record fields, `CardinalLighting` is two hard-coded records the
    dimension merely chooses between, and block tint is still `BiomeColors`
    over `BiomeSpecialEffects`. Three pages state the fact absolutely.
  - **Cardinality, in the now-familiar shapes:** four call sites of
    `FeatureRenderDispatcher.renderAllFeatures`, not two — and two of them
    are the GUI, which is why it needs its own submit storage;
    `RenderSystem.assertOnRenderThread` is called from eleven classes
    including eight sites in `RenderSystem` itself, on current API, so "only
    the legacy corners" was wrong about the class that owns it; three of four
    particle groups ignore the frustum, not two; a layer's terrain geometry
    is a growing *list* of 128 MiB heaps, not one buffer; the two backends
    differ in six of seven feature flags, not one; and `ParticleLimit` really
    does have exactly one instance, which the page had right.
  - **The inventory found three more whole systems and one phantom.**
    Counting the tree (1,187 classes / 97,864 lines, 58% named nowhere)
    turned up post-processing (`PostChain`), block-entity rendering with its
    26 render states, and the item-model property system — all unowned, all
    recommended as pages in [pass2.md](pass2.md). It also killed
    *ScreenManager*, a class the pass-2 queue had been listing as
    `blaze3d/platform` content since session H and which does not exist in
    26.2 in any package.
  - **`the-window` is new**, discharging the ruling session H deferred to
    this session. `blaze3d/platform` is 25 classes and ~3,800 lines that no
    page explained, and three pages in two parts all began *after* it. Its
    best fact is structural: the backend-selection loop encloses **both**
    window creation and device creation, because an OpenGL window and a
    Vulkan window need different GLFW hints — so a rejected backend leaves a
    window behind that has to be destroyed before the next one is tried.
  - **Structural notes to [pass3.md](pass3.md):** Part XI is **two substrate
    pages and one six-page pipeline**, which reframes session H's open
    "`blaze3d` second or last?" question; `the-window`'s trace is a retry
    loop that a sequence diagram renders badly; and the part now has **three
    internal lane collisions**, the worst being `LX` for two different
    extractors on adjacent pages.

- **2026-09-01, session H** — Part X The client, and the X/XI split. Eight
  adversarial fact-checks (`the-frame`, `ClientLevel`, the prediction ledger,
  input/options, screens, the text engine, `hud`, and a full
  `net/minecraft/client/**` coverage inventory), plus a ninth agent to
  research what the inventory found. **Part X's eleven pages became eleven
  client pages and a seven-page Part XI**; worldgen, commands and the
  appendix renumbered to XII–XIV; the rendering pages moved to
  `src/systems/rendering/` with `[output.html.redirect]` entries in
  `book.toml` keeping the published URLs alive. 2,931 lines of Part X became
  2,631 lines of Part X plus the rendering part, and every page in it is now
  one subject.
  **Session H's centre of gravity is ownership.** Where G found errors in
  claims a page had borrowed, H found errors in claims *nobody* owned: four
  pages described the prediction ledger and disagreed; the loop and the frame
  shared a page and the loop lost; the text engine was a paragraph inside a
  page about screens. What mattered most:
  - **The split is not where the plan said, and the difference matters.**
    The plan put `the-frame` in Part XI as the render part's opening trace.
    Correct for the frame, wrong for the *loop*: `Minecraft.runTick` and
    `Minecraft.renderFrame` are two subjects in one method chain. Splitting
    them into `the-client-loop` (X) and `the-frame` (XI) resolved the
    corpus's worst ordering dependency — Part IX now depends on one short
    page rather than on all of Part X.
  - **A whole undocumented system, found by counting rather than by
    reading.** The debug subscription pipeline — a `DebugSubscription`
    registry, a per-level poll-and-diff engine that sleeps until somebody
    subscribes, six packets, two dozen renderers — is ~4,900 lines that no
    page mentioned. It is now `debugging-the-running-game`, and the appendix
    gap it closes had been open since session 12. Hence the new protocol
    note above.
  - **The prediction ledger had four owners and four stories.**
    `client-world-and-options` said an inbound block update "does not touch
    the world" — true only for a position already in the ledger, and the two
    Part V pages had it right. It also listed five methods on
    `BlockStatePredictionHandler` and omitted the three that matter
    (`isPredicting`, `currentSequence`, `close`). The system now has one
    page, `prediction-and-acks`, and its headline is the fact all four pages
    had missed: **the acknowledgement is a receipt for a sequence number,
    not a verdict** — it fires for rejected actions too, and even an
    unsequenced abort produces an ack of zero. Correctness rests entirely on
    the ordering rule that corrections precede the receipt. The most visible
    consequence, which no page had: releasing a dig too early makes the
    block *come back* and then vanish again.
  - **A trace with two fabricated arrows.** The render-distance slider trace
    ended with the server replying `ClientboundSetChunkCacheRadiusPacket` and
    the client's effective distance moving a second time. Neither happens:
    `ServerGamePacketListenerImpl.handleClientInformation` does two things,
    and neither is a reply; that packet is only ever broadcast when the
    *server's* view distance changes. The client clamps itself and is never
    told. The absence of a return arrow is now the point of the diagram.
  - **"Queued onto the client thread" was wrong about input, and it is a
    threading claim.** GLFW callbacks are dispatched inside
    `RenderSystem.pollEvents`, on the game thread, and
    `BlockableEventLoop.execute` runs a task inline when already on its
    thread. Input handlers run *before* the tick that observes them, not
    inside it.
  - **Cardinality again, and in the same shapes as F and G:**
    `Minecraft.pick` runs once per tick and once per frame, not "twice per
    ticking frame"; `Minecraft.MAX_TICKS_PER_UPDATE` has **no callers**;
    `ClientLevel.serverSimulationDistance` has two consumers, not one;
    `ClientChunkCache.tick` has an **empty body**, so "the chunk cache" was
    listed as per-tick work that does not exist; F1 does *not* hide the
    sleep fade; `Options.save` is the only caller of `broadcastOptions` but
    every cycle-option button calls `Options.save`; three entities implement
    `HasCustomInventoryScreen` by two different packets, not one.
  - **Structural notes to [pass3.md](pass3.md):** Part X is a **hub and five
    spokes**, not a pipeline — the loop is the hub and every other page is
    defined by its cadence; the GUI stack is the one genuine internal
    pipeline; two of the new pages (`prediction-and-acks`,
    `text-and-fonts`) are arguably in the wrong part; and two lane
    abbreviations now collide across neighbouring parts (`CL`, `GR`).

- **2026-09-01, session G** — Part IX Networking (`the-connection`,
  `protocol-phases`, `packets-and-stream-codecs`,
  `what-the-client-is-told`, `chat-and-signing`). Five adversarial
  fact-checks, five rewrites; 1,780 → 2,367 lines. **Session G's centre of
  gravity is the boundary between a page and the things it borrows.**
  Where F found miscounted exceptions and E the client/server split, Part
  IX's errors clustered in claims it had inherited from *other* parts and
  restated slightly wrong — and in one case from a generated file that was
  wrong itself. What mattered most:
  - **A tool bug had been laundered into prose.**
    `packets-and-stream-codecs` opened with "225 packet types", quoting
    `src/reference/packets.md`, which was generated by a regex that could
    not match a nested type parameter and silently dropped seven packets.
    The number is **232**. `tools/gen_reference.py` is fixed and the
    catalogue regenerated. This is now the third pass-2 session to find a
    bug in one of the two scripts, and it is the first that had already
    reached a reader — hence the new protocol note above.
  - **`protocol-phases` had the login's most interesting moment two arrows
    too early.** It said the `ServerPlayer` is built by `PrepareSpawnTask`
    during configuration, before the finish packets. In fact the task only
    resolves a spawn and tickets its chunks; the object is constructed by
    `PrepareSpawnTask.spawnPlayer` from
    `ServerConfigurationPacketListenerImpl.handleConfigurationFinished`,
    i.e. **after** the client acknowledges the end of the phase, by which
    point the server's outbound protocol is already PLAY. `players-and-sessions`
    (session B) had this exactly right, which is how the disagreement was
    caught — and it is the pattern of the whole session: **where Part IX
    contradicted another part, Part IX was wrong every time.**
  - **`what-the-client-is-told` said the client applies packets once per
    client tick, "not per frame". It is precisely the other way round** —
    `Minecraft.runTick` drains the queue once per frame, before that
    frame's zero-to-ten ticks. `the-frame` had it right. Two more of its
    claims inverted on reading: `Entity.setRequiresPrecisePosition` has a
    caller after all (a happy ghast on its still timeout), and
    `MinecraftServer.getScaledTrackingDistance` is overridden in both
    server classes — in singleplayer a *graphics slider* sets how far
    mobs are tracked.
  - **Three "the only path" claims in `the-connection` were the same
    mistake in different clothes.** The inbound pipeline had two handlers
    in the wrong order; `HandlerNames` is a complete index of names that
    **no code reads**; and `MonitoredLocalFrameDecoder` is never installed
    at all, because the only pipeline that could take one always passes a
    null monitor — so bandwidth accounting is client-only, inbound-only
    and socket-only. The page also gained `TickablePacketListener`, which
    it had listed and not explained, and which turns out to be the only
    way a listener with no hopping handlers gets time on a game thread —
    the missing rung under the login state machine and every keep-alive.
  - **Cardinality again, but smaller:** seven terminal packets, not eight
    (the eighth was `ServerboundResourcePackPacket.Action.isTerminal`, an
    unrelated namesake); two of five chain-decode failures break the
    signing chain, not most of them; the signature cache holds 128
    entries, not the last-seen window's 20; eight client handlers skip the
    thread hop, not two.
  - Structural notes to [pass3.md](pass3.md): Part IX is **one pipeline
    and three passengers**, not two pipelines; `the-connection` and
    `packets-and-stream-codecs` are one lecture read from two ends;
    `protocol-phases` wants a state diagram, `what-the-client-is-told` a
    decision flow, and `chat-and-signing` a table of what each check
    catches. And the part cannot be taught before Part III's tick order
    and Part X's frame/tick interleave, which it currently restates three
    times.

- **2026-09-01, session F** — Part VII Items (`items-and-stacks`,
  `containers-and-menus`, `recipes`, `enchantments`, `loot-tables`) and
  Part VIII The player (`player-anatomy`, `input-to-movement`,
  `the-sword-swing`, `hunger-xp-and-effects`). Nine adversarial
  fact-checks, nine rewrites. The A–E pattern holds without exception —
  every page had *wrong* claims. **Session F's centre of gravity is
  counting**: where B found orderings wrong, C thread attribution, D
  unstated conditionals and E the client/server split, almost every
  session-F error was a correct rule with the wrong number of exceptions.
  Three entries in this file's own load-bearing list were falsified. What
  mattered most:
  - **Two load-bearing facts were reversed and one narrowed.**
    `/data get block` on an unopened chest does **not** commit the loot
    roll — `trySaveLootTable` writes the key back out and never reads an
    item, so the save path is not one of the unpacking reads (the hopper
    and comparator halves are right).
    `ServerboundPlayerInputPacket` never moves the *player* but is not
    inert: both minecart behaviours read the move intent to nudge a
    stalled cart, and the handler sets the sneak flag directly. And "no
    enchantment effect runs on the client" is true only of entity and
    location-based effects — `Enchantment.modifyCrossbowChargeTime` and
    `Enchantment.modifyTridentSpinAttackStrength` take no level, and run
    on the render thread and in `MultiPlayerGameMode.useItem`
    respectively. All three confirmed by direct reads.
  - **`player-anatomy` had the player's second tick phase backwards.**
    `ServerGamePacketListenerImpl.tickPlayer` *records* the current
    position into `firstGood…` and then restores it after
    `ServerPlayer.doTick` with `Entity.absSnapTo`; the page had it
    resetting to the last accepted position first and the player "actually
    moving, falling" inside `doTick`. `input-to-movement` had the same
    mechanism right and the page it depends on had it wrong — the two are
    now consistent, and both carry the four-method authority matrix
    (`Player.isClientAuthoritative` is an unconditional true, so the server
    is *not* locally authoritative, yet `Entity.canSimulateMovement` and
    `Entity.isEffectiveAi` are overridden true, which is why it simulates
    at all, and why fall damage arrives via `Entity.doCheckFallDamage` on
    the packet path).
  - **`the-sword-swing` was missing the fact that the client predicts
    nothing.** `Entity.hurtClient` returns false and neither
    `LivingEntity` nor `Mob` overrides it, so client-side `Player.attack`
    skips its entire post-hit block; only `RemotePlayer` returns true.
    Also: a whole damage term was missing — `Item.getAttackDamageBonus`
    sits between the sprint check and the crit, so the mace's bonus is
    multiplied by 1.5 — the sweep damage is scaled by the attack-strength
    ratio and run through the enchantments, `ItemStack.hurtEnemy` does not
    apply durability (`ItemStack.postHurtEnemy` does),
    `LivingEntity.getKnockback` does not damp the attacker
    (`Player.causeExtraKnockback` does), and there is a *third* melee path,
    `KineticWeapon`, reached from item use.
  - **`containers-and-menus` had the suppression invariant inverted.** The
    advancement channel does *not* see intermediate states — nothing calls
    back into the menu during a click — but `CraftingMenu.slotChangedCraftingGrid`
    *does* send a packet mid-click, bypassing both the synchronizer and the
    suppression flag, and is a third `incrementStateId` call site. Also:
    one synchronizer per `ServerPlayer`, not per menu;
    `AbstractContainerMenu.broadcastChanges` is a single loop, not two
    passes; `AbstractContainerMenu.isValidSlotIndex` is only an upper
    bound; and the page's "the server can never adopt the client's data"
    is falsified by `ServerboundSetCreativeModeSlotPacket`, which takes an
    `ItemStack` verbatim.
  - **`items-and-stacks` had the prediction after the packet.**
    `MultiPlayerGameMode.startPrediction` runs the local action and *then*
    sends what it returns. Also: `ItemStack.onUseTick` runs before the
    decrement (so a 32-tick meal is offered 32…1 and never 0), the item-swap
    cancel is in the private `LivingEntity.updatingUsingItem` rather than
    `LivingEntity.updateUsingItem`, the "pre-use copy" is taken at
    *completion*, the untrusted stream codec is used by exactly one packet
    and validates by re-encoding rather than by `ItemStack.validateStrict`,
    the two durability-vs-stackability validators test *different*
    components, and the client's counter does not stop at zero. Durability
    was missing from the page entirely.
  - **`hunger-xp-and-effects` had the starvation floor at ten hearts.** It
    is five on Easy, the health term is difficulty-independent, and unlike
    both regen branches the starvation branch is not gated on the game
    rule. Bigger: the page's premise that "the client computes none of
    them" is wrong for eating — entity event 9 makes the client re-run
    `FoodProperties.onConsume` and its `FoodData.eat` locally. Also:
    infinite effects are never re-sent (−1 modulo 600 is −1), the XP packet
    is change-detected on the total alone, `ExperienceOrb.award` does not
    split (its delegate does), and the merge bucket is a fresh random
    number rather than an entity id.
  - **`recipes` and `loot-tables` were mostly right and badly counted.**
    Recipe ties resolve **path before namespace** (`Identifier`'s own
    order); an unplaceable recipe is logged and *kept*, not dropped, and
    then lights up as always-craftable in the book; `AbstractFurnaceMenu`
    uses a property set rather than a cached check and `CrafterMenu` has no
    `RecipeCache` at all; `ServerPlaceRecipe` counts before it clears. On
    loot: the recursion guard is a **stack**, not a visited-forever ledger,
    so a table referenced twice in one draw yields items twice; the
    all-parameters set is not all of them; running out of slots discards
    silently; and `DynamicLoot` breaks the "a leaf always makes a fresh
    stack" invariant.

  **Split rulings: none executed.** All four Part VII/VIII candidates
  confirmed and left presentational; `loot-tables` **added** to the table,
  because the page's own headline is that predicates are the bigger client
  and five of its twenty-six parameter sets have no loot caller. One
  cross-part correction outside these parts (`entity-anatomy` gained
  `ClientMannequin`) and one **wrong naming-drift row** fixed in both
  places. All of it in [pass2.md](pass2.md) and [pass3.md](pass3.md).

  Verifier lesson: two bare words slipped through as identifiers, and the
  agents caught four member mis-attributions the verifier structurally
  cannot see — five sessions running that the NAMES section has earned its
  place.

- **2026-09-01, session E** — Part VI Entities: all seven pages
  (`entity-anatomy`, `entity-lifecycle`, `synched-entity-data`, `attributes`,
  `movement-and-collision`, `ai-goals-and-brains`, `damage-and-death`). Seven
  adversarial fact-checks — one died on an API error and was relaunched — and
  seven rewrites. The A–D pattern holds: every page had *wrong* claims. Where
  session B found orderings wrong, C thread attribution and D unstated
  conditionals, **session E's centre of gravity is the client/server split**:
  the biggest errors were pages that correctly observed the same code runs on
  both sides and then assumed both sides do the same thing with it. What
  mattered most:
  - **`movement-and-collision` had the client/server model backwards, in an
    invariant headed *Both sides run the physics*.** A tracked mob on the
    client never calls `Entity.move` at all: `LivingEntity.aiStep` gates
    travel on `Entity.canSimulateMovement` (which is
    `Entity.isLocalInstanceAuthoritative`), and a non-authoritative living
    entity instead **coasts** — interpolate if interpolating, else scale the
    delta by 0.98. The mirror-image surprise is the player: `Player`
    overrides `Entity.isClientAuthoritative` to true, so on the *server* a
    player fails the authority test and `Entity.move` applies it no fall
    damage — that comes from `Entity.doCheckFallDamage` on the packet path
    instead. Confirmed directly against `LivingEntity.aiStep`, `Entity` and
    `Player`. The page now opens with an authority subsection; Part IX's
    `what-the-client-is-told` was corrected to match.
  - **`entity-anatomy` said an unknown entity id becomes a pig.** It does
    not, on the path that matters. `DefaultedMappedRegistry` overrides the
    value and numeric lookups but *not* the `Optional` one the name codec
    uses, so a bad id in save data makes `EntityType.create` log *Skipping
    Entity with id …* and drop the entity. The pig default is real, and it is
    the network's. Also on that page: `Brain` is declared on `LivingEntity`,
    not `Mob` (so an armour stand has one), `PathfinderMob` adds walk-target
    valuation rather than navigation, entity ids come from a **process-global**
    counter on `ServerLevel`, and a freshly constructed entity has a
    full-size box, not the zero-size one the field initialiser suggests. The
    sharpest new fact: on the client `Level.getNextEntityId` returns 0, 0 is
    the reserved invalid id, and `Entity.getId` *throws* on it — a
    client-side entity is unusable until `Entity.recreateFromPacket`.
  - **`attributes` had the send a tick early.** `ServerEntity.sendDirtyEntityData`
    is reached from `ChunkMap.tick` in `ServerLevel.tick`'s **chunkSource**
    phase, which runs *before* the entities phase — so an attribute dirtied
    during an entity's own tick goes out on the following tick. Same ordering
    session D found for block entities. Also: `LivingEntity.refreshDirtyAttributes`
    runs on **both** sides (which is why its waypoint branch has to test for a
    `ServerLevel`); `Mob.onAttributeUpdated` reacts to `Attributes.TEMPT_RANGE`
    as well as follow range; `Attributes.bootstrap` does nothing but return
    `Attributes.MAX_HEALTH`; and the best find — **`AttributeMap.getInstance`
    dirties on creation**, so merely *reading* a syncable attribute for the
    first time queues it for broadcast. The eight-non-syncable fact was
    re-counted from all 40 registrations and is exact.
  - **`damage-and-death` missed the flag that makes i-frames silent.** A hit
    inside the window that *is* bigger than the last still clears the
    took-full-damage flag, and the damage-event broadcast, `Entity.markHurt`,
    the knockback, the hurt sound and the red flash are all inside a test of
    it — health drops and nothing else happens. Also: `LivingEntity.hurtArmor`
    is **empty**, overridden only by `Player`, `Horse` and `Wolf`, so a
    skeleton in iron never wears its armour out; a successful block replaces
    the damage event rather than accompanying it; freezing and cramming are
    ticked from `LivingEntity.aiStep`, not `LivingEntity.baseTick`; `Monster`
    drops the baby gate on loot; `GameRules.SHOW_DEATH_MESSAGES` off still
    sends the kill packet, with an empty component; and
    `RemotePlayer.hurtClient` returns true, so there *is* one living entity
    that simulates a hit client-side.
  - **`entity-lifecycle`'s spawner diagram had the checks after
    construction.** Every type-level check — placement, spawn rules, light —
    runs before `EntityType.create`; only `Mob.checkSpawnRules` and
    `Mob.checkSpawnObstruction` run after. Also: `WorldGenRegion` is a
    **second** implementor of `LevelWriter.addFreshEntity`; the y roll is one
    per chunk per *category*, not per chunk; nether fortresses are a hardcoded
    short-circuit in `NaturalSpawner.mobsAt`, not a `ChunkGenerator.getMobsAt`
    structure override; both despawn distance branches also require
    `Mob.removeWhenFarAway`; the Peaceful branch consults no player at all;
    the remove packet goes out at the tracking stop, ticks *before* the unload
    write; `EntityTickList` swaps rather than copies (the walk keeps the
    original); and three of the four `NaturalSpawner` constants the page cited
    are declared and never read. Best new material: persistent categories are
    offered a spawn only every **400 ticks**, which is most of why animals
    feel rare beside monsters, and the 17 in 17² comes from the spawn-chunk
    tracker propagating diagonally, giving each player a Chebyshev square.
  - **`synched-entity-data` had the serializer wire ids wrong from 9 up** and
    placed the variant tail in the wrong half of the list;
    `EntityDataSerializers.HUMANOID_ARM` is the *last* registered, not an
    early one. Also: `ServerEntity.sendPairingData` reads a cached
    `ServerEntity.trackedDataValues`, not a fresh
    `SynchedEntityData.getNonDefaultValues` — so an all-default entity sends
    no data packet on pairing at all; `ServerEntity.sendChanges` is gated by
    `ChunkMap.tick` on section change / needs-sync / ticking range; A→B→A
    dirties twice, and there is a force-dirty overload vanilla uses; the
    duplicate-id check is in `SynchedEntityData.Builder.define`, not
    `SynchedEntityData.Builder.build`; and `Mob.interact` calls the
    superclass hook *between* its two mob hooks.
  - **`ai-goals-and-brains` had the villager's job-site memory wrong.**
    `AcquirePoi` writes `MemoryModuleType.POTENTIAL_JOB_SITE`;
    `AssignProfessionFromJobSite` promotes it to
    `MemoryModuleType.JOB_SITE` only once the villager is within two blocks —
    so walking to the workstation is a required step, and `Activity.WORK`'s
    requirement is never satisfied by the acquirer alone. Also: it pathfinds
    **once** with five targets, not five times; `Sensing` is shared with brain
    mobs, not the goal system's alone; the zombie has seven goals including
    the new `SpearUseGoal` at a better priority than its attack goal; the node
    budget comes from `PathNavigation.requiredPathLength` (48 for a villager),
    not follow range alone; `MoveControl.setWantedPosition` is the single
    *method* but not the single call site; and `Mob.tickHeadTurn` has no side
    check, so `BodyRotationControl.clientTick` really does run on both sides.
    New material: `Mob.updateControlFlags` as the second writer of the flag
    table, `GoalSelector`'s sentinel goal, brain rebuild on profession change,
    and `Path.canReach` as the number that actually matters.

  **Split rulings: none executed.** Both Part VI candidates confirmed but
  presentational; `movement-and-collision` **added** to the table, not as a
  split but because its new authority section is a shared prerequisite for
  four pages across three parts and needs one owner. A **catalogue gap was
  found and deliberately left**: `damage-and-death` covers `LivingEntity` and
  never mentions the ~30 non-living `Entity.hurtServer` overrides; session E
  added a bullet naming the gap and left the ruling to pass 3. Both in
  [pass3.md](pass3.md).

  Verifier lesson: a helper type that *reads* nested can be top-level —
  `PostSpawnProcessor` is its own file, not `EntityType.PostSpawnProcessor`.
  Otherwise the usual bare members, plus `super` used as a noun.

- **2026-09-01, session D** — Part V Blocks: `blocks-and-states`,
  `block-interaction`, `block-breaking`, `block-entities`, `redstone`. Five
  adversarial fact-checks, five rewrites. The pattern from A–C holds without
  exception — every page had *wrong* claims — but session D's errors have a
  different centre of gravity: **conditionals**. Where session B found
  orderings wrong and session C found thread attribution wrong, almost every
  session-D error was a claim that was true in the traced case and stated as
  though it were universal: a hook "not called" for the wrong reason, a
  refusal "always answered" when three of five refusals answer differently,
  a broadcast "later in the tick" that is actually next tick. What mattered
  most:
  - **Two pages had the tick phase wrong in the same direction.**
    `block-entities` had the furnace's block update *and* its menu data
    leaving in the tick they were produced. `ServerLevel.tick` runs
    chunkSource (the broadcast drain) → blockEvents → entities (where
    `ServerPlayer.tick` reconciles menus) → **blockEntities**, so a block
    entity's own writes always reach clients on the *following* tick, by
    both routes. Confirmed directly against `ServerLevel.tick`; it agrees
    with session B's `server-level-tick`, which was right.
  - **`Level.setBlock` runs three shape passes, not one**, and ends with
    `Level.updatePOIOnBlockStateChange` — `blocks-and-states` named the
    middle pass only and stopped a statement early. The new state's
    *indirect* pass is how dust reaches diagonal wires.
  - **`block-interaction` had the door's `onPlace` skipped for the wrong
    reason.** `BlockBehaviour.BlockStateBase.onPlace` is gated on the side
    and on flag 512, *not* on the block changing — so it does run for the
    server's same-block write. And the page's clean "shape updates run on
    both sides" story has a hole it did not mention:
    `Block.updateOrDestroy`'s destroy branch is server-only and re-enters at
    flags 3, which is why breaking one door half is not predicted for the
    other.
  - **`block-breaking`'s headline sentence was wrong in the flavour line** —
    "stone takes 1.5 seconds" is the *hardness*, and the page's own
    arithmetic three sections later says eight ticks. Also: a failed reach
    check sends the client **nothing at all** and spawn protection sends
    only a chat overlay, against a page that said every refusal answers with
    a block update; mining fatigue is not read through `MobEffectUtil`;
    `Minecraft.continueAttack`, not the game mode, spawns the particle and
    swings; and the best find — **ABORT does not cancel a deferred
    destroy**, because `ServerPlayerGameMode.tick` tests `hasDelayedDestroy`
    first and the ABORT branch never clears it, so stopping early and
    letting go still breaks the block, down a path that re-checks neither
    reach nor spawn protection nor whether you are still there.
  - **`redstone` had a piece of dead code presented as a mechanism.** The
    piston's `SignalGetter.hasSignal` downward on itself can never return
    true — `SignalGetter.getSignal` only consults strong power for a
    conductor, and `Blocks.pistonProperties` declares a piston a
    non-conductor. Also: the moving placeholders are written at flags 324,
    **without** `Block.UPDATE_CLIENTS`, so the client's copy comes *only*
    from re-simulating the block event and no correcting packet ever
    follows (the page claimed one arrived and changed nothing); the client
    does not play the piston sound itself; comparators override
    `ComparatorBlock.checkTickOnNeighbor` and never use the two urgent tick
    priorities the page attributed to them; and `PistonMovingBlockEntity.finalTick`
    places **air** for the head entity rather than being an early-exit form
    of the normal landing.
  - **`blocks-and-states`' "no allocation, no search" was half right.**
    `StateHolder.setValue` allocates nothing but does a linear scan of the
    key array by reference — and the sting is that `Property.equals` is
    *value*-based while that scan is identity-based, so two equal properties
    can still throw. Also `StateHolder.hashCode` is not final (only
    `equals` is); the place sound is the *mean* of the sound type's volume
    and 1.0, not half of it; six stairs use `Blocks.registerStair`, not
    three; and `Block.UpdateFlags` is an empty marker annotation that names
    nothing.

  **Catalogue gap found and filled.** `redstone` claimed to cover redstone
  while naming `DiodeBlock.checkTickOnNeighbor` and nothing else:
  comparators, repeaters and observers were **entirely absent**. Session D
  wrote a new section covering `DiodeBlock`'s input/side/output model, the
  repeater's `RepeaterBlock.LOCKED` (recomputed by a *shape* update, which
  is why it survives on a client), the comparator's block entity and its
  reach-through-a-conductor input including the single `ItemFrame`, the
  container fullness formula, and the observer — which fires on
  `ObserverBlock.updateShape`, i.e. the one block whose job is noticing
  changes listens on the *other* channel.

  Split rulings: none of the three Part V candidates executed. `redstone`'s
  proposed seam in the pass-2 table was **rejected** — the
  experimental-evaluator coda belongs to the dust half, and the page is
  three lectures (dust · pistons · diodes), not two.
  `blocks-and-states`' seam is confirmed but presentational.
  `block-interaction` + `block-breaking` were **added** to the table as a
  possible *merge* rather than a split: they re-derive the same prediction
  ledger and ack ordering, and the same wrong sentence had to be fixed in
  both. All three in [pass3.md](pass3.md).

  Verifier lesson: a method **parameter** name in backticks is a new trap
  shape (it looks exactly like a field). Otherwise the usual two — bare
  members, and one member cited on a subclass that the verifier caught only
  by luck.

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
