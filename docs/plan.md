# The plan — the passes

*Rewritten 2026-09-02 at the start of pass 3 and again 2026-09-03 at its
close. This is the document every session reads first and ticks last. Each
finished pass is archived whole in its own file — [pass1.md](pass1.md),
[pass2.md](pass2.md), [pass3.md](pass3.md) (the notebook, then the charter,
rulings, protocol, schedule and log) — and each future pass has a file
that earlier passes fill in as they go: [pass4.md](pass4.md) is the queue
the second fact-check works from, [pass5.md](pass5.md) collects polish
debt.*

## Where we are

**Pass 3 is done** (2026-09-03, sessions A–P): the site is a book.
Thirteen parts, each opening on a landing page that draws the part's shape
and rules its watching order; **102 system pages** where pass 2 left 79,
each in one of eight shapes from `TEMPLATE.md`'s menu instead of the one
seven-heading template; a Reference tier of twenty-one pages, eight of them
generated; the introduction as a front door, the maps as an atlas, and the
lecture map assembled with the dependency graph between parts drawn. Three
gates now stand between a page and the site: every backticked name resolves
in the decompile, every diagram parses under the site's own mermaid, and
every diagram lane means what the one corpus-wide key says. The full record
— the evidence, the rulings, the per-session log — is in
[pass3.md](pass3.md).

Two findings from the restructure shape what comes next:

- **Pass 3 put errors back, as predicted, and wrote down where.** Nearly
  every page was rewritten and most figures redrawn; every session listed
  the claims its rewrite introduced in [pass4.md](pass4.md) — hooks,
  orderings, counts, new sections, and the landing pages' dependency lists
  — and that file is over two thousand lines. Four sessions in a row found
  a wrong *count* while redrawing a page, three of them load-bearing for
  the sentence around them.
- **The menu held; the closing device did not.** Session P's audit found
  the trace is the plurality shape and not the majority — thirty-one of
  the hundred and two pages, with twenty-five vocabulary pages, nineteen
  pipelines, eleven comparisons, seven policies, seven patterns and two
  state machines making up the rest — but sixty-six pages end on a
  *Questions players ask* section and four more carry one, which is one
  device become a slot. That is pass 5's problem, and it is written down there with the
  counts and the seven pairs of pages that share a skeleton.

## The passes

| pass | what | status |
|---|---|---|
| **1 — rough draft** | every page drafted from the decompile, names verified | done — [pass1.md](pass1.md) |
| **2 — completeness and accuracy** | every claim adversarially fact-checked; gaps filled; pages split and added freely | done, 2026-09-01 — [pass2.md](pass2.md) |
| **3 — restructuring** | the site became a book: each part the shape of its system, each page the shape of its story; the frame, the introduction, the maps and the reference tier redone; the lecture order drafted | done, 2026-09-03 — [pass3.md](pass3.md) |
| **4 — the second fact-check** | pass 2's protocol again, over everything pass 3 rewrote, redrew or added; the claims pass 3 introduced checked first | **current** — charter below; queue in [pass4.md](pass4.md) |
| **5 — polish** | wording, voice, consistency, cuts | after 4 — queue in [pass5.md](pass5.md) |
| **6+ — the owner reads** | part by part with the decompile open; `<!-- Q: … -->` answered in the prose; lecture order confirmed; then voice and recording | after 5 |

The rules stand for every pass: names never code · how the system works,
not how the code reads · newest version only (26.2) · trace-driven ·
`python tools/verify_names.py` clean before every commit that touches a page
· claims come from the decompile, never from model memory of 1.21 · every
diagram passes `node tools/check_mermaid.js` · every lane passes
`python tools/check_lanes.py --strict` · the landing pages, the lecture map
and the dependency figure agree under `python tools/check_deps.py` (the
fourth gate, added by pass-4 session A). `tools/deploy.sh` runs all four
and refuses to publish on any failure.

---

## Pass 4 — the second fact-check (current)

**Goal:** everything the restructured corpus says is true. Pass 2 proved
that every page had at least one wrong claim and that the errors live in
the confident sentences — orderings, "only" and "never", counts, and "X,
not Y". Pass 3 then rewrote the prose of nearly every page, redrew most of
the figures, wrote thirteen landing pages, a lecture map and twenty-three
new pages, and on pass 2's evidence that put errors back. Pass 4 runs pass
2's protocol again over the whole corpus, checks the claims pass 3
introduced first, and does nothing else. Nothing gets polished that has not
been checked twice.

### The protocol

Pass 2's, archived in [pass2.md](pass2.md) under *The pass-2 charter and
protocol*, with its lessons under *Verifier lessons* and in the session
log: **one adversarial agent per page**, given the page and
`reference/26.2`, briefed to *falsify* — re-derive from the decompile every
checkable claim and return a discrepancy list: **wrong** (the decompile
disagrees), **unverifiable** (the agent could not find it), **misleading**
(true, but the emphasis implies something false). An empty list from an
agent that quotes no decompile evidence is a failed check, not a pass. Pass
3 makes eight additions:

1. **The pass4.md entry is the opening checklist.** Every pass-3 session
   listed, per page, the claims its rewrite introduced. The agent gets that
   list first and reports on every line of it, with the file and line that
   settles each, before it reads the rest of the page.
2. **Order and dependency are claims.** The thirteen landing pages,
   `lectures.md` and the parts-dependency figure assert that part B needs
   page A. For every *before you start* entry and every arrow, find the
   sentence in the part that actually uses it; a dependency no page uses is
   struck, and a page that uses something its part's landing page does not
   list is a missing arrow.
3. **Diagrams, arrow by arrow.** `check_mermaid.js` proves a diagram
   parses, not that it is true. Every sequence diagram's arrows are checked
   in order against the code that makes the calls, every tick-boundary bar
   against the tick phase it names, every flowchart branch against the
   condition that decides it, every state transition against its trigger.
4. **Every count is re-counted.** "Twenty-one option names", "fifteen
   phases", "sixty-two of the sixty-seven": the agent lists the population
   from the decompile and quotes the listing. Pass 3's sessions K, L, M and
   N each found a count wrong while redrawing, and in three of the four it
   carried the sentence's argument.
5. **The population behind every only, never, all and none is named**, as
   in pass 2 — the claim is checked against the whole population, and the
   report says which population.
6. **Libraries and data are checkable now and were not.** `reference/libs/`
   holds Brigadier, DataFixerUpper and authlib; `reference/26.2/data/` and
   `assets/` hold the jar's data packs, models, atlases, fonts, shaders and
   post-effect chains. Pass 2 took every claim about them on trust. Hardest
   on: `codecs-nbt-json` (DFU semantics), `protocol-phases` and
   `players-and-sessions` (authlib), `chat-and-signing` (signatures),
   `brigadier-and-commands`, `the-execution-engine` and
   `functions-and-macros` (Brigadier), `post-processing`,
   `models-and-atlases` and `text-and-fonts` (assets), and every Part XII
   page (worldgen JSON).
7. **Reference is checked like the parts.** The ten hand-kept pages one
   row at a time (the four catalogues the part sessions wrote, the block
   update flags, threads, math and primitives, level data and rules, naming
   drift, and the glossary against each entry's owner page); the eight
   generated views by re-deriving one sample per view by hand, because pass
   2 found bugs in both of the generators it had.
8. **The four session-P pages have been checked zero times, not once.**
   `block-entity-rendering`, `entity-selectors`, `blending` and
   `creating-a-world` get pass 2's completeness question as well — *what is
   in this page's scope in the decompile that the page never mentions* —
   and their pass4.md claims lists are the longest in the file.

### What pass 4 does not do

It does not restructure, it does not add pages, and it does not polish. A
wrong fact is fixed in place, and that includes a hook: a hook the decompile
contradicts is replaced by a true one even when the opening paragraph has
to be rewritten around it, and that rewrite is logged in
[pass5.md](pass5.md) as wording to re-read. A structural finding — a page
carrying two subjects, a figure in the wrong shape — is logged in
[pass5.md](pass5.md) and not acted on; a system with no owner page goes to
[pass3.md](pass3.md) §7, which stays the coverage queue. A fix that changes
what a landing page, `lectures.md` or the glossary says about the page
changes those in the same commit, because a landing page is a claim about
order and pass 4 has just checked it.

### The tooling

Built 2026-09-03 by the planning session between the passes, so that
fifteen Opus sessions run the same check the same way. All in `tools/`,
all read-only over the corpus, none a deploy gate yet:

- `pass4_queue.py` — every pass4.md note that names a page (either entry
  format, either page name, renamed pages aliased), as one checklist per
  page; reads `~~strikes~~`, so checklists shrink as sessions settle lines.
  `--summary` is the corpus-wide count.
- `claims.py` — a page's confident sentences by category: count, absolute,
  order, contrast, side. About 5,000 count sentences and 4,700 absolutes
  corpus-wide; `--all --counts --out DIR` is session N's queue.
- `diagram_arrows.py` — every diagram as a numbered list of arrows, notes
  and bars (195 diagrams, 2,442 items, none unparsed), so an arrow-by-arrow
  report has one verdict per number and a gap is visible.
- `check_deps.py` — the mechanical half of addition 2: landing pages, the
  figure, the lecture table and every cross-part link against each other.
  Exit 1 on a contradiction; a report for the rest.
- `pass4_prompts.py` — the four above assembled into one prompt file per
  page behind the brief in [pass4-brief.md](pass4-brief.md), which is also
  the session runbook.

### Session protocol

One session = one part (Parts IV, XI, XII and XIII may take two), plus a
first session on the frame and a closing session. The step-by-step
version, with the commands, is [pass4-brief.md](pass4-brief.md) Part 2.
Each part session:

1. **Read** this charter, `CLAUDE.md`, [pass2.md](pass2.md)'s protocol and
   lessons, every [pass4.md](pass4.md) entry that names the part (grep it —
   sessions other than the part's own left notes, and session O's standing
   items apply to every part), and the part's landing page.
2. **Check.** One agent per page, in parallel, on Opus, each given the
   prompt file `python tools/pass4_prompts.py --part <part> --out DIR`
   writes for its page: the brief ([pass4-brief.md](pass4-brief.md) Part
   1), the page's pass4.md checklist, its confident sentences by category
   and its diagrams arrow by arrow. The part's page-less notes land in
   `_part-notes.md` for the session to route. Fact-check output is not
   committed.
3. **Re-derive before rewording.** Suspect the tool once, then the agent
   once, before the page: pass 2's verifier and both generators had bugs,
   and pass 3's drafting agents were wrong in about a third of their own
   corrections. The session opens the decompile for every *wrong* before
   it changes a sentence.
4. **Fix**, in place, with the landing page, `lectures.md` and the glossary
   kept in step. Strike the pass4.md lines as they are settled and log each
   correction under the part's entry — what the page said, what the
   decompile says, the file and line — so pass 6 can see what changed and
   why.
5. **Verify and ship.** `python tools/verify_names.py` ·
   `node tools/check_mermaid.js` · `python tools/check_lanes.py --strict` ·
   `mdbook build` clean · commit `pass 4, session X — Part N: <summary>` ·
   deploy.
6. **Log and hand off.** The session log below; [pass5.md](pass5.md) for
   wording debt and structural findings; [pass3.md](pass3.md) §7 for a
   gap with no owner.

### Schedule

Tick as done. Session A is the frame; B–N are the parts in sidebar order;
O is the close.

- [x] **Session A — The frame** *(2026-09-04)*. Addition 2 done in full:
  `check_deps.py`'s two failures and three forward links were all real and
  are fixed, the checker is green, and it is now `tools/deploy.sh`'s
  **fourth gate**. The generated views' one-sample check: all eight
  confirmed. Twenty agents over the introduction, `lectures.md`, the atlas
  and the Reference tier; four tool bugs found by suspecting the tool first
  (`map_source.py`'s hierarchy resolver, `gen_reference.py`'s serializer
  regex, `check_deps.py`'s README asymmetry, `check_lanes.py`'s
  single-page unkeyed lane). What it did not reach is written out under
  *Open* in [pass4.md](pass4.md).
- [x] **Session B — Part I Anatomy · Part II Foundations** *(2026-09-04)*.
  Ten pages, ten agents; **every one had at least one wrong claim**. The
  freeze rule was wrong on three pages at once — a frozen registry swaps
  the tag table *and* the component prototypes, on consecutive lines of
  `ReloadableServerResources`. The two-loops figure and the threads table
  survived arrow by arrow except for one thing, and it is corpus-wide: the
  **login state machine is advanced from the Server thread**, because
  `ServerLoginPacketListenerImpl` is a `TickablePacketListener`; only the
  handlers stay on Netty. `data-driven-types`' fifty-six is right and its
  stated criterion was not. Fifth tool bug: `gen_reference.py` missed one
  register helper and published 94 built-in registries for 95. Everything
  in [pass4.md](pass4.md).
- [x] **Session C — Part III The server** *(2026-09-04)*. Six pages, six
  agents; **all six had at least one wrong claim**, which is pass 2's finding
  for a fourth time — and this time on `server-tick` and `server-level-tick`,
  the pair seven later parts assume. Twenty-eight corrections. Three carry a
  lecture: `server-tick`'s **event-loop figure had two impossible edges**
  (`pollTaskInternal` offers the chunk sources a turn only in the *else*, and
  `waitForTasks` is reachable only from `managedBlock`, where no task is ever
  left queued for want of budget); its **packet-drain punchline was false** —
  chat and both command packets never call `ensureRunningOnSameThread` and
  arrive as *tasks* through `MinecraftServer.execute`; and
  `server-level-tick`'s "nothing sends a block update at the moment a block
  changes" has a counter-example the page had been using as an *example*, a
  landing `FallingBlockEntity` sending its own packet on the line after
  `setBlock`. `how-a-server-dies` — the page pass 2 never saw — lost nine
  claims around an argument that held, the sharpest being that the watchdog
  **is** still armed through a crash teardown, because only
  `MinecraftServer.halt` clears `running` and the crash path never calls it.
  `starting-a-server`'s `forceDifficulty` note was exactly backwards. Addition
  2 done in full: all five *before you start* entries are used by a sentence,
  and one was missing (`foundations/resource-system`). **Sixth tool bug**,
  again by suspecting the tool first: `pass4_queue.py` split a continuation
  line opening on a page marker into its own unit without inheriting the
  parent's strike, so a struck bullet's children came back on every later
  checklist for ever. Two agent findings rejected on re-derivation.
  Everything in [pass4.md](pass4.md).
- [x] **Session D — Part IV The world** *(2026-09-04)*. Done in one, not two:
  eleven pages, eleven agents; **every one had at least one wrong claim**.
  Forty-nine corrections, and the numbers five other parts cite were where the
  worst of them lived — `tickets-and-loading`'s **eleven is thirteen**,
  `chunk-generation-pipeline`'s own derivation of the 11 came to 10, and
  `lighting`'s **27 sections is 14**, a figure geometry forbids. Two hooks fell:
  `points-of-interest`'s, contradicted by its own state diagram, and
  `environment-attributes-and-timelines`' orange badlands sky, which is
  `#6eb1ff`. No tool bug — the first session without one; instead **two of
  session E's own *session-verified* corrections were wrong**. Everything in
  [pass4.md](pass4.md).
- [x] **Session E — Part V Blocks** *(2026-09-04)*. Eight pages, eight agents;
  **every one had at least one wrong claim**, and this part had the worst
  provenance in the corpus. Sixty-one corrections. `signal-and-dust`'s
  **staircase is invisible** — the packet is built once a tick by re-reading the
  level, so the 14, 13, 12 the hook promised is never sent; the forty-two
  survived both factors. `pistons-and-block-events`' motion is **off by one
  tick** the whole way through, its block-event census is three blocks not four,
  and quasi-connectivity turns out to be three blocks' quirk rather than the
  piston's. `diodes-and-observers` calls a five-row table "exactly three places".
  `blocks-and-states`, the hub, had the door on the wrong update channel. The
  **shared click-page preamble** described a comparison that does not exist, on
  both pages and in `lectures.md`. Addition 2 done in full, with
  `server/server-tick` added as a missing entry. **Seventh tool bug**:
  `pass4_queue.py` could not settle a numbered list item. Everything in
  [pass4.md](pass4.md).
- [x] **Session F — Part VI Entities** *(2026-09-04)*. Nine pages and the
  landing page, ten agents; **every one had at least one wrong claim**.
  Sixty-two corrections. The part's own pass-3 checklist came back almost
  clean — so the errors were in the *illustrations*, not in what pass 3 knew
  it had changed. `authority` is wrong about your own player on the client
  (`LocalPlayer.isLocalPlayer` is true, so `Entity.checkFallDamage` **does**
  run there) and its *NoAI* closer is exactly backwards; the **0.98 coast
  does not exist** on any page, because nothing applies that delta;
  `pathfinding`'s hook invented an eight-tick give-up the page's own next
  paragraph contradicts, and its fire/spider example is wrong on both halves.
  `synched-entity-data`'s hook was falsified by its own next section — ids
  are fixed by the superclass chain, not by initialiser order.
  `points-of-interest` was a missing *before you start* entry. No tool bug —
  the second such session. Instead the **queue was wrong once**
  (`EntitySpawnRequest.ignoreChecks` **is** true, twice, exactly where
  session G said it was not) and an **agent once** (the packet queue does
  drain before `tickServer`). Everything in [pass4.md](pass4.md).
- [x] **Session G — Part VII Items and inventories** *(2026-09-04)*. Eight pages
  and the landing page, nine agents; **every one had at least one wrong claim**,
  which is pass 2's finding for an eighth time. Sixty corrections, and session
  H's own checklist held almost entirely — so, as in Part VI, the errors were in
  what pass 3 did not know it had changed. Four carry a lecture:
  `enchanting`'s **shared tail does not exist** (only three of the five paths
  reach `ItemStack.enchant`, and the anvil is outside `updateEnchantments` too —
  what all five share is `EnchantmentHelper.getComponentType`, which is the
  routing-by-item-identity the section was actually about);
  `loot-tables`' trace **opens the wrong menu**, since a single chest is
  `ChestMenu.threeRows` and `sixRows` has one caller in the game, the double
  chest's; `contexts-and-predicates` says "the fifteen [`ContextKey`s] that
  exist" when there are **seventeen**, and the missing two are a *client* user
  of `ContextMap` that makes the page's own two-packages argument; and
  `recipes`' reload window holds **empty** indexes, not the previous recipe set,
  and is five statements of one synchronous lambda wide. Two more punchlines
  fell: `items-and-stacks`' contained-size check is not at the creative-slot
  door at all, and `enchantments`' "no other item can be made to behave like
  one" is false of the *component*, which the anvil keys on. Addition 2 in full:
  all six *before you start* entries used by a sentence, **`server/server-tick`
  added** as a missing one, and three order claims on the landing page and
  `lectures.md` corrected — including that **`/reload` does not change an
  enchantment**, because `Registries.ENCHANTMENT` is a world-load dynamic
  registry and not a reload citizen at all. **Eighth tool bug**, found by
  suspecting the tool when striking session H's entry made the checklists grow:
  `pass4_queue.py` lost a struck bullet's strike across a **blank line**, so
  only the first paragraph of a long entry could ever be settled. Everything in
  [pass4.md](pass4.md).
- [ ] **Session H — Part VIII The player.** The two-phase tick's callers;
  the damage pipeline's one number; the spear's two cooldown curves.
- [ ] **Session I — Part IX Networking.** The round-trip diagram; the phase
  state machine against authlib; the seven handlers that never hop.
- [ ] **Session J — Part X The client.** The tick arithmetic; the
  prediction ledger's two columns; the sound engine's five threads.
- [ ] **Session K — Part XI Rendering.** Probably two sessions: the frame's
  nine zones and five partial ticks; the six post chains against the JSON;
  `block-entity-rendering` (addition 8).
- [ ] **Session L — Part XII World generation.** Probably two sessions:
  the density graph and its caches against the data; the tree kit's
  placer counts; `blending` and `creating-a-world` (addition 8).
- [ ] **Session M — Part XIII Commands and data packs.** Probably two
  sessions: the three parsers against Brigadier; the engine's queue
  snapshots; `entity-selectors` (addition 8).
- [ ] **Session N — The corpus-wide count sweep.** Every number on every
  page, in one pass with one brief, because a count checked inside a page's
  argument is checked by a reader who already believes the argument.
- [ ] **Session O — The close.** The glossary against the corpus; the
  tools (the verifier, the generators, the lane key, the mermaid checker)
  re-read for the bug pass 2 found in each; the queue in pass4.md struck
  through or carried; pass 5's charter written; if 26.3 has landed, the
  re-verification session scheduled before it.

### Hand-off rules

Two files. [pass4.md](pass4.md) — the corrections, per part, struck through
as settled, and anything the next pass-4 session must know.
[pass5.md](pass5.md) — wording debt, cuts, structural findings. A gap with
no owner page goes to [pass3.md](pass3.md) §7. Anything left for later is
written when it is found, not at the end.

---

## Pass 5 — polish (sketch)

Per page: does it read well, is everything needed explained and nothing
more? This is where pass 2's "don't worry about length" bill comes due —
cut what over-grew, using the on-spec logs in [pass2.md](pass2.md)'s
hand-off and [pass5.md](pass5.md). Corpus-wide: one terminology sweep (the
glossary is the checklist), one voice sweep against the best page, links
and cross-references complete, the "not X but Y" tic and the
named-qualifier tic hunted, and the *Questions players ask* slot broken up
— session P's rule of thumb, at most half the pages in a part, is in
[pass5.md](pass5.md) with the counts.

## Pass 6+ — the owner reads

Unchanged from the original conception: part by part, decompile open,
questions left **in the page** as `<!-- Q: … -->` comments; a session
answers each in the prose — if the owner had to ask, the page was wrong or
missing it — and removes the comment. The owner confirms or reorders
`lectures.md`. Then voice and cuts, and recording.

## Risks

- **Confirming instead of falsifying.** An agent that likes the page
  returns an empty list. The rule stands: no quoted evidence, no pass. Brief
  per page, not per part, so the spend limit does not end a check halfway
  (session O's glossary audit hit it).
- **A fix that is a rewrite.** A wrong hook tempts a new opening, and a new
  opening is where the next error goes. Fix the sentence; log the rest.
- **A count checked from inside the argument.** Session N's sweep exists
  because a reader who has followed the page's reasoning counts what the
  page told them to expect.
- **The tools.** The verifier, the generators, the lane key and the mermaid
  checker each had a bug in pass 2; suspect them first.
- **26.3 lands mid-pass.** Finish on 26.2; re-verify once, in one session,
  between passes.

## Session log — pass 4 onward

*(newest last; pass 3's log is in [pass3.md](pass3.md) §10)*

- **2026-09-03, planning session (Fable, between passes 3 and 4).** No
  page touched. Read the charter, the queue and pass 2's protocol; built
  the five tools under *The tooling* above and wrote
  [pass4-brief.md](pass4-brief.md) — the agent brief (one report shape,
  nine steps in order, evidence for every verdict) and the session
  runbook (nine steps, each a command or a rule) — so sessions A–O on
  Opus do no planning of their own. Measured while building: the queue
  is 562 page-attributed notes and 82 part-wide ones; the corpus has
  about 5,000 count sentences and 4,700 absolutes for session N; all
  195 diagrams parse into 2,442 checkable items. `check_deps.py` found
  session A's first findings (listed in its schedule line). Rulings:
  `check_deps.py` treats Parts I and II as universally assumed (session
  P's figure omits them on purpose) and reports a forward link rather
  than failing it, because a landing page may link a later part to say
  what it hands forward; the session decides which it is. A note in
  pass4.md written under a renamed page's old name is routed to the new
  page(s) by an alias table in `pass4_queue.py`.
- **2026-09-04, session A — the frame (Opus).** Addition 2 in full, the
  Reference tier, the atlas, the introduction and the lecture map. All five
  of `check_deps.py`'s opening findings were real: two lecture-table rows
  (the environment row was right and two landing pages were missing the
  entry; the blocks-and-states row claimed a part that assumes *block
  interaction* instead) and three *before you start* links to later parts,
  every one a hand-forward or a pointer rather than a dependency, so each
  moved out of the section instead of gaining an arrow. The checker is green
  and is the fourth deploy gate. **Four tool bugs**, each found by suspecting
  the tool before the page: `map_source.py` resolved every *Outer.Inner*
  parent by its last segment and keyed types by simple name (222
  mis-resolutions; `Entity` 193 to 191, `Screen` 157 to 158, `Packet` 232 to
  236, 21 of 60 hierarchy rows), `gen_reference.py` published a `?` for the
  one serializer declared as an anonymous subclass, `check_deps.py` called
  every "read Part N first" entry unused, and `check_lanes.py --strict`
  passed any unkeyed lane used on a single page — which is how a retired
  lane and an unkeyed one survived. The session's own first replacement for
  a corrected sentence was itself wrong (a lines-per-class superlative),
  which is the re-derive rule earning its place against the session rather
  than against an agent. Rulings: a hand-forward belongs outside *before you
  start* rather than on a dashed arrow; a word lane in the key is marked by
  an italic cell rather than by the literal phrase "not a class", because
  that phrase was false of `Main`; a landing-page link is a whole-part
  dependency and cannot satisfy a page-level mention check. Fifteen of the
  twenty pages are settled; the five with findings still open are listed
  under *Open* in [pass4.md](pass4.md), with what belongs to Parts VI, IX,
  XI, XII and XIII.
- **2026-09-04, session B — Parts I and II (Opus).** Ten pages, one
  adversarial agent each; the order work, the tool audit and every *wrong*
  re-derived by the session before a sentence moved. **All ten pages had at
  least one wrong claim**, which is pass 2's finding holding for a third
  time — and the two pages pass 2 never saw (`text-components`,
  `data-driven-types`) were not the worst of them. Three findings crossed
  pages: the **freeze rule** (a frozen registry swaps two things, not one —
  the tag table and the component prototypes, applied on consecutive lines
  of `ReloadableServerResources.updateComponentsAndStaticRegistryTags`),
  the **login state machine** (advanced from the Server thread through
  `MinecraftServer.tickConnection`, not run start to finish on Netty; wrong
  on `anatomy`, on `reference/threads.md` in three places, and still wrong
  on Part IX's `protocol-phases`), and the **`ComponentSerialization`
  superlative**, which no population supports and which is now gone from
  both pages that carried it. Two inversions worth remembering: the
  homogeneous-numeric-list section of `codecs-nbt-json` had the collectors
  backwards, and `data-components` had the component-binding asymmetry the
  wrong way round — it is the *singleplayer* client that binds only the
  synchronized registries, and as written no multiplayer client could
  decode a stack. **Fifth tool bug**, again by suspecting the tool first:
  `gen_reference.py`'s built-in regex spelled the register helpers out and
  missed `registerSimpleWithIntrusiveHolders`, so `registries.md` published
  94 built-in registries for 95 and left `block_entity_type` unclassified.
  Rulings: a superlative no population supports is deleted rather than
  re-scoped (session A's lines-per-class precedent, now twice); a stale
  pass4.md note is corrected in the settling session's entry rather than
  edited in place; and a wrong fact found on another part's page is logged
  under *For other parts' sessions* rather than fixed across the boundary
  (session A's precedent), because the fix needs that part's argument open
  beside it. Four table cells on `data-driven-types` and one premise are
  the only findings left unactioned, and they are written out there.
- **2026-09-04, session C — Part III The server (Opus).** Six pages, one
  adversarial agent each; the order work, the part-wide notes and every
  *wrong* re-derived by the session before a sentence moved. **All six pages
  had at least one wrong claim** — pass 2's result for a fourth time, and the
  first time it has landed on the pair the rest of the book leans on hardest:
  seven later parts assume `server-tick` or `server-level-tick`. Twenty-eight
  corrections. The three that carry a lecture: `server-tick`'s **event-loop
  flowchart had two edges the code cannot take** — `pollTaskInternal` offers
  the levels' chunk sources a turn only in the `else`, when the server's own
  queue ran nothing, and `waitForTasks` is reachable only from `managedBlock`,
  where `shouldRunAllTasks` is true and no task is ever left queued for want
  of budget; the same page's **packet-drain punchline** ("the only point in a
  tick where player input enters the world") is false, because
  `handleChat` and both command packets never call
  `ensureRunningOnSameThread` and post through `MinecraftServer.execute`
  instead, arriving as tasks; and `server-level-tick`'s "nothing sends a block
  update at the moment a block changes" is broken by a landing
  `FallingBlockEntity`, which sends its own `ClientboundBlockUpdatePacket` on
  the line after `setBlock` — the page had been offering falling sand as an
  *example* of the rule it breaks, and the landing page repeated it.
  `how-a-server-dies`, the page pass 2 never saw, kept its three-way argument
  and lost nine claims around it, the sharpest being that the watchdog **is**
  still armed all the way through a crash teardown (only
  `MinecraftServer.halt` clears `running`, and the crash path never calls it)
  and that weather and game rules have not been in `level.dat` since they
  became `SavedData` — a 1.21-era fact that `reference/level-data-and-rules`
  already had right, which is the second time this pass that one page's
  correctness has convicted another's. `starting-a-server`'s `forceDifficulty`
  aside was exactly backwards: the integrated server has no override and
  `DedicatedServer` is the only one. Addition 2 done in full — all five
  *before you start* entries are used by a sentence rather than merely
  linked, `check_deps.py` green, and one entry missing
  (`foundations/resource-system`, which `starting-a-server` leans on for the
  staged load). **Sixth tool bug**, again from suspecting the tool before the
  page: `pass4_queue.py` splits a continuation line that opens on a page
  marker into its own unit — a feature — but did not give that unit its
  parent's strike, so **striking a bullet could never settle it** and four of
  session D's notes came back mid-sentence on every checklist. Fixed. Two
  agent findings rejected on re-derivation, both worth recording: a
  "missing dependency" on `protocol-phases` that is a pointer the page
  explicitly disclaims needing, and — the session's own error, caught by
  counting rather than by an agent — a pass-5 note asserting Part III is 5 of
  5 on *Questions players ask* when it is 2 of 5. Rulings: a superlative the
  page itself contradicts one sentence later is deleted, not re-scoped
  (sessions A and B's precedent, now three times); a saved-data *file name* is
  italics, not backticks, like any other non-identifier; and a diagram fixed
  by adding an edge is fixed, not restructured — the arrow count going up is
  pass 5's problem and is logged there.
- **2026-09-04, session D — Part IV The world (Opus).** Ten pages and the
  landing page, one adversarial agent each; the order work, the part-wide notes
  and every *wrong* re-derived by the session before a sentence moved. **All
  eleven had at least one wrong claim** — pass 2's result for a fifth time, and
  it did not spare the numbers five other parts cite. Forty-nine corrections.
  The four that carry a lecture: `tickets-and-loading`'s **eleven is thirteen**
  (eleven is the reach past a level-**33** chunk, and a `PLAYER_LOADING` ticket
  sits at 31), and the same page's level-44 holder is at
  `ChunkStatus.STRUCTURE_STARTS`, not "the first noise pass" — replaying
  `ChunkStep.Builder` over the pyramid gives the FULL step's twelve entries as
  *SPAWN, INITIALIZE_LIGHT, CARVERS, BIOMES, STRUCTURE_STARTS × 8*, with
  *NOISE* on the list nowhere; `chunk-generation-pipeline`'s **own derivation of
  the 11 came to 10**, because three radius-1 rows widen the accumulated list and
  the page named two — the missing one is *LIGHT* wanting *INITIALIZE_LIGHT*, and
  `getRadiusOfParent` is why *SURFACE* and *SPAWN* contribute nothing;
  `lighting`'s **"up to 27 sections across nine chunks" is 14 across seven**, and
  27 is not merely wrong but impossible — an exhaustive enumeration over all
  4,096 placements settles it, and the two opposite corner sections need the
  torch's section coordinates to sum to at most 13 and at least 32 at once; and
  `points-of-interest`'s **hook was falsified by its own state diagram**, since
  `ValidateNearbyPoi` reads `BedBlock.OCCUPIED` and releases the ticket, so the
  true statement is that the flag can only take a claim away, never make one.
  Two more punchlines fell: the **badlands sky is blue** (`#6eb1ff`, bluer than
  taiga's `#7da3ff`; no overworld biome declares an orange sky), and the day
  timeline's Bézier makes the sun **slowest at its zenith**, not at the horizon —
  which is why a day is about 13,564 ticks of sun against 10,436 of night, a
  better fact than the one it replaced. `chunk-storage` lost thirteen claims
  around an argument that held, the sharpest being that a flush is submitted at
  *foreground* priority like any store and that a no-save world does let go of
  its chunks, on `/save-all flush` and on shutdown. Addition 2 done in full:
  all four *before you start* entries are used by a sentence,
  `foundations/identifiers-and-registries` gained the page-level link it had been
  missing (settling the Part IV half of session A's note), `foundations/tags` was
  a missing entry, and `check_deps.py` has no Part IV line left. **No tool bug
  this session** — the first pass-4 session without one. Instead the queue itself
  was wrong twice: two of session E's *session-verified* pass-3 corrections are
  false (`/tick sprint` **does** clear the freeze flag through
  `ServerTickRateManager.requestGameToSprint`, and
  `DynamicGameEventListener.move` does not "do nothing" on a half-loaded pair —
  it guards its two halves separately and can drop a listener out of the world),
  which is the re-derive rule earning its place against the checklist rather than
  against an agent. Rulings: a hook a page's own figure contradicts is replaced,
  and the replacement states what the figure draws; a dead constant that names
  the right number is kept and *said to be dead* rather than deleted — four of
  them turned up in this one part, and the resulting tic is logged in pass 5.
  Everything in [pass4.md](pass4.md).
- **2026-09-04, session E — Part V Blocks (Opus).** Seven pages and the landing
  page, one adversarial agent each; the order work, the part-wide notes and every
  *wrong* re-derived by the session before a sentence moved. **All eight had at
  least one wrong claim** — pass 2's result for a sixth time, over the part with
  the worst provenance in the corpus: two pages drafted by agents whose reports
  were lost, one by an agent whose twelve corrections were never re-derived, and
  three written by the pass-3 session itself. Sixty-one corrections. The four
  that carry a lecture: `signal-and-dust`'s **staircase is invisible** — the
  cascade finishes inside one packet handler and `ChunkHolder.broadcastChanges`
  builds the packet once per tick by *re-reading the level*, so a position
  written five times is sent once with its final value, and "it counts down, 14,
  13, 12, visibly" was the page's hook (the **forty-two** survived, both factors
  re-derived); `pistons-and-block-events`' **motion is off by one tick**, because
  `Level.addBlockEntityTicker` puts a ticker straight into the live list whenever
  `tickingBlockEntities` is false, so the placeholders move in the *blockEvents*
  tick's own *blockEntities* phase and land at N+2, not N+3; the **block-event
  census is three blocks, not four**, and `ComparatorBlock` — the fourth — raises
  no event at all and owns a `triggerEvent` override that is dead in both
  directions; and **quasi-connectivity is not the piston's alone**, since
  `DispenserBlock` (hence `DropperBlock`) and `DoorBlock.getStateForPlacement`
  read `hasNeighborSignal(pos.above())` the same way. Two more punchlines fell:
  `diodes-and-observers` says its comparison table is "exactly three places" over
  a table with **five rows** and calls the comparator "the only redstone block
  with a block entity" (the sculk sensor answers from one, and the daylight
  detector's stores nothing at all); and `block-breaking`'s "nothing crosses the
  wire" is false client-to-server, where a `ServerboundSwingPacket` goes up every
  dig tick. `blocks-and-states`, the hub, had the door on the wrong one of its own
  two channels — `DoorBlock` does not override `affectNeighborsAfterRemoval` —
  and its "what differs is entirely inside the write", the sentence that lets
  Part X be watched later, is broken by two side-branches in `BlockItem.place`.
  The **shared preamble's fourth sentence was a mechanism error** on both click
  pages and in `lectures.md`: a correction *overwrites* the ledger entry rather
  than being compared with it, and the settle compares that one value against the
  world. Addition 2 done in full: all four entries used by a sentence, two of the
  stated reasons rewritten to what the part actually leans on, and
  `server/server-tick` added as a missing entry that two pages depend on and
  neither linked. **Seventh tool bug**, again from suspecting the tool first:
  `pass4_queue.py`'s strike regex did not recognise a **numbered** list item, so
  session F's four provenance classes could never be settled. Ten of the ten
  never-re-derived pass-3 leads on `block-breaking` came back CONFIRMED, and
  every count on `block-entities` was right. Everything in [pass4.md](pass4.md).
- **2026-09-04, session F — Part VI Entities (Opus).** Nine pages and the
  landing page, one adversarial agent each; the order work, the part-wide
  notes and every *wrong* re-derived by the session before a sentence moved.
  **All ten had at least one wrong claim** — pass 2's result for a seventh
  time. Sixty-two corrections, and the shape of them is new: this part's
  pass-3 checklist came back almost entirely clean (twenty of session G's
  twenty-one corrections re-confirmed, every count on `attributes` and
  `synched-entity-data` right, all fifteen figures checked arrow by arrow
  with four arrows wrong), so the errors were not in what pass 3 knew it had
  changed but in the **illustrations hung off mechanisms it had got right**.
  The four that carry a lecture: `authority`'s "false for a player on **both**
  sides — so no player anywhere takes fall damage from the mover" is false on
  the client, where `LocalPlayer.isLocalPlayer` returns true and
  `Entity.java:823` runs every tick (harmless only because
  `LivingEntity.checkFallDamage` needs a `ServerLevel`) — and Part VIII's two
  survivors of the deleted matrix were the correct ones all along, settling
  session I's note the other way round; the same page's ***NoAI* answer is
  exactly backwards**, because `LivingEntity.travel` is gated on
  `Entity.isEffectiveAi` as well as `Entity.canSimulateMovement`, so a *NoAI*
  mob does not even fall; the **0.98 coast does not exist**, on three pages'
  worth of sentences, because nothing on the client applies that delta — a
  tracked mob is moved only by `InterpolationHandler` and stands still when
  it runs out; and `pathfinding`'s hook **invented its number** ("eight ticks
  later"), which the page's own second paragraph contradicts with 100 and
  ~260. Two more punchlines fell: `synched-entity-data`'s hook blamed JVM
  static-initialiser order for a slot `ClassTreeIdRegistry` fixes from the
  **superclass chain** alone, which the page says itself forty lines later;
  and `pathfinding`'s "a zombified piglin walks through fire and a spider does
  not" is wrong on both halves (the piglin overrides *lava*; the spider sets
  no malus at all, so fire is passable-but-expensive). Addition 2 done in
  full: all five entries used by a sentence, **`world/points-of-interest`
  added** as a missing entry that `ai-goals-and-brains` spends throughout,
  `world/chunk-anatomy` given the page-level link it lacked, and
  `authority`'s Part X link moved from `the-client-loop` (which never
  mentions authority) to `the-client-level` — which settles both halves of
  session A's pass4.md:1517 and required the same correction in
  `lectures.md`, where the whole *ledger's foundation* premise was wrong:
  the prediction ledger is `BlockStatePredictionHandler`, keyed by `BlockPos`,
  and has nothing to do with movement. **No tool bug** — the second pass-4
  session without one. Instead the checklist itself was wrong once
  (`EntitySpawnRequest.ignoreChecks` **is** true, at
  `BaseSpawner.java:348` and `TrialSpawnerStateData.java:266`, both building
  a display entity — exactly what session G struck as false), and an agent
  once, rejected on re-derivation: `MinecraftServer.processPacketsAndTick`
  does drain the packet queue at `:1122` before `tickServer` at `:1124`, so
  `attributes`' sentence stands. Rulings: a hook that invents a number the
  page then contradicts is replaced with the page's own number; an
  illustration wrong on both halves is replaced rather than repaired; and a
  "never" the page's own later text contradicts is narrowed to what the later
  text says, the later text being the authority — three times this session.
  Everything in [pass4.md](pass4.md).
- **2026-09-04, session G — Part VII Items and inventories (Opus).** Eight pages
  and the landing page, one adversarial agent each; the order work, the
  part-wide notes and every *wrong* re-derived by the session before a sentence
  moved. **All nine had at least one wrong claim** — pass 2's result for an
  eighth time. Sixty corrections, and the shape is Part VI's again: session H's
  own checklist held almost entirely (all nine of its pass-2 corrections
  re-confirmed, every count on `items-and-stacks`, `containers-and-menus`,
  `enchantments` and `loot-tables` right, both `containers-and-menus` figures
  clean arrow by arrow), so the errors were in what pass 3 did not know it had
  changed. The four that carry a lecture: `enchanting`'s **shared tail does not
  exist** — the section rested on "All of them end at `ItemStack.enchant`" and
  only three of the five do, the grindstone and the providers calling
  `EnchantmentHelper.updateEnchantments` themselves and the anvil writing with
  `EnchantmentHelper.setEnchantments` outside even that; what all five share is
  the private `EnchantmentHelper.getComponentType`, which *is* the
  routing-by-item-identity the section was about, so the argument survives under
  a new name. `loot-tables`' trace **opens the wrong menu**: a single chest —
  which arrow 1 of the same figure establishes as the scenario — opens
  `ChestMenu.threeRows`, and `ChestMenu.sixRows` has exactly one caller in the
  game, inside the double chest's anonymous provider.
  `contexts-and-predicates` says "the fifteen [`ContextKey`s] that exist are the
  static fields of `LootContextParams`" when there are **seventeen** —
  `SlotDisplayContext.FUEL_VALUES` and `.REGISTRIES` are the other two, and
  `SlotDisplayContext.fromLevel` builds a `ContextMap` from six *client* files,
  which is a second user for the page's own *util/context knows nothing about
  loot* thesis and makes the cast table's "server main" wrong. And `recipes`'
  reload window is not what the page says: a reload builds a **fresh**
  `RecipeManager` whose four derived indexes start *empty*, and the swap and
  `finalizeRecipeLoading` are five statements apart in one synchronous
  main-thread lambda, so the "short and, on a reload, real" window is neither.
  Two more punchlines fell: `items-and-stacks`' contained-size check is reached
  only from `ItemStack.validateStrict` and so is **not** at the creative-slot
  door the paragraph puts it at (and is one level deep, not recursive), and
  `enchantments`' "no other item can be made to behave like one" is false of the
  *component* — `AnvilMenu` keys `usingBook` on `STORED_ENCHANTMENTS`, not on
  `Items.ENCHANTED_BOOK`. Addition 2 done in full: all six *before you start*
  entries are used by a sentence, **`server/server-tick` added** as a missing
  one that `containers-and-menus`' whole tick section rests on (session E's Part
  V finding, again), and three order claims corrected across the landing page
  and `lectures.md` — "every later page assumes all three" (no engine page links
  all three, and two link none), "four and five are the pair" (it is five and
  six), and **"all three engines are reload-time citizens of the same
  machinery"**, which is false for enchantments: `Registries.ENCHANTMENT` is a
  world-load dynamic registry, so `/reload` does not change an enchantment.
  **Eighth tool bug**, again from suspecting the tool before the page — striking
  session H's entry made the part's checklists *grow*, because
  `pass4_queue.py` resets its current unit on a blank line and session H wrote
  one long bullet of blank-line-separated paragraphs, so only the first
  paragraph of a struck entry could ever be settled. Session C fixed the same
  inheritance within an unbroken run; this is the same bug across the blank
  line, and the fix moves exactly this part's nine pages and one `lectures.md`
  line (620 open units to 596) and nothing else. The checklist itself was wrong
  once (`MonsterRoomFeature`'s "two chest attempts" is two chests of up to three
  attempts each) and an agent once, rejected on re-derivation: the arrow's spawn
  packet *does* leave on the release tick, because `ChunkMap.addEntity`
  broadcasts inside the handler and the packet drain precedes `tickServer`.
  Rulings: a section title whose named mechanism is wrong but whose argument is
  right is renamed for the argument rather than deleted; a figure edge whose
  label justifies a *different* edge is re-sourced to the edge the label is true
  of; and a superlative the page's own later text contradicts is narrowed to
  what the later text says — four times this session, which is sessions D, E and
  F's precedent again. Everything in [pass4.md](pass4.md).
