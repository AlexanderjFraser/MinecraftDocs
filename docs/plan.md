# The plan — the passes

*Rewritten 2026-09-02, at the end of pass 2 and the start of pass 3. This is
the document every session reads first and ticks last. Each finished pass is
archived whole in its own file — [pass1.md](pass1.md), [pass2.md](pass2.md)
(queue, hand-off, charter, protocol and log) — and each future pass has a
file that earlier passes fill in as they go: [pass3.md](pass3.md) is the
restructuring notebook pass 2 kept, [pass4.md](pass4.md) collects what the
second fact-check must re-check, [pass5.md](pass5.md) collects polish debt.*

## Where we are

**Pass 2 is done** (2026-09-01, sessions A–K): seventy-nine pages in
fourteen parts, every page read back against the decompile by an agent
briefed to falsify it, five pages added, the X/XI split executed. The
one-line result is the one that reshapes the rest of the plan: **every page
had at least one wrong claim**, and the errors clustered in the corpus's most
confident sentences — orderings, "only/never" claims, counts, and the
sentence that frames a true fact. The full record is in
[pass2.md](pass2.md).

Two consequences, both decided in the 2026-09-02 planning session:

- **A second fact-check pass is inserted after the restructure.** Pass 3
  rewrites the prose of nearly every page and redraws many diagrams; on pass
  2's evidence, that will put errors back. So the old pass 4 (polish) becomes
  pass 5, the old pass 5 (the owner's read) becomes pass 6, and the new
  **pass 4 runs pass 2's protocol again** over the restructured corpus.
  Nothing gets polished that has not been checked twice.
- **Pass 3 covers the whole site, not just the system pages** — the
  introduction, the maps, the reference tier and the site's own frame
  (sidebar, tables, diagrams). The owner's read of the live site found four
  things pass 2 could not see from inside a page: every page has the same
  seven headings and leans on bullet walls; many diagrams render as *Syntax
  error in text*; tables scroll sideways on a wide screen; and the sidebar
  is a flat list of eighty pages. All four are in this pass's charter.

## The passes

| pass | what | status |
|---|---|---|
| **1 — rough draft** | every page drafted from the decompile, names verified | done — [pass1.md](pass1.md) |
| **2 — completeness and accuracy** | every claim adversarially fact-checked; gaps filled; pages split and added freely | done, 2026-09-01 — [pass2.md](pass2.md) |
| **3 — restructuring** | the site becomes a book: each part takes the shape of its system, each page the shape of its story; the frame (sidebar, tables, figures), the introduction, the maps and the reference tier all redone; the lecture order drafted | **current** — charter below; evidence in [pass3.md](pass3.md) |
| **4 — the second fact-check** | pass 2's protocol again, over everything pass 3 rewrote, redrew or added | after 3 — queue in [pass4.md](pass4.md) |
| **5 — polish** | wording, voice, consistency, cuts | after 4 — queue in [pass5.md](pass5.md) |
| **6+ — the owner reads** | part by part with the decompile open; `<!-- Q: … -->` answered in the prose; lecture order confirmed; then voice and recording | after 5 |

The rules stand for every pass: names never code · how the system works,
not how the code reads · newest version only (26.2) · trace-driven ·
`python tools/verify_names.py` clean before every commit that touches a page
· claims come from the decompile, never from model memory of 1.21. Pass 3
adds one: **every diagram passes `node tools/check_mermaid.js`** before it
is committed. A diagram that does not render is worse than no diagram.

---

## Pass 3 — restructuring (current)

**Goal:** a reader opens any page and wants to keep reading, and a viewer of
the series can see, from the site alone, what order to watch in and why.
Pass 2 made the corpus true; pass 3 makes it a book. Length is still not the
concern — pass 5 cuts — but *shape* is, everywhere: the shape of the site,
of each part, of each page, and of each figure.

### What is wrong today

Written down so the sessions aim at it. The first four are the owner's,
from reading the live site; the rest are the notebook's, from eleven
sessions of pass 2.

1. **Every page is the same page.** Seventy-nine pages, seven identical H2s
   in identical order (*Responsibility · The data it owns · When it runs ·
   The trace · Interfaces · Invariants and surprises · Where to look*). The
   template served pass 1, which needed a checklist; it now guarantees
   monotony. Its two worst sections are the bullet walls — the data section
   (a class name followed by fifteen field names) and the invariants section
   (twelve bold-led bullets) — and every page has both.
2. **Diagrams fail to render.** A mermaid sequence diagram ends a statement
   at `;` and treats `#` as the start of an entity code, and the pass-1
   style of writing arrow labels as *"call — what it decides; what happens
   next"* put semicolons into dozens of diagrams. Each shows as *Syntax
   error in text mermaid version 11.6.0*. The planning session built
   `tools/check_mermaid.js` — it parses the *built* HTML with the site's own
   mermaid, so its verdict is the browser's — fixed the failures, and made it
   a gate in `tools/deploy.sh`. A diagram that does render is still scaled
   down to the column, and a nine-lane trace is unreadable there;
   `diagram-zoom.js` (planning session) opens any diagram at viewport size on
   click.
3. **Tables scroll sideways with room to spare.** mdBook's reading column is
   750px and cells pad 20px a side, so a four-column table of identifiers
   overflowed on any screen. `custom.css` (planning session) widens the
   column to 1100px for tables, diagrams and figures while capping prose at
   800px, and lets identifiers wrap inside cells.
4. **The sidebar is a flat list of eighty pages.** Sections now fold
   (`[output.html.fold]`, planning session) so only the current part is
   open; the parts themselves are not yet clickable because they have no
   page. Every part gets a landing page in this pass.
5. **The shape of each part is invisible.** The notebook found Part IV is a
   conveyor, Part V a hub, Part VI a ladder, Part IX one pipeline and three
   passengers, Part X a hub and spokes, Parts XI and XII a substrate under a
   pipeline, Part XIII a stack — and nothing on the site says so. Pages that
   are reference material (`math-and-primitives`, `level-data-and-rules`,
   the appendix's tables, the catalogues inside `synched-entity-data`,
   `attributes` and `hud`) sit in the lecture sequence, and the appendix is
   numbered as if it could be watched.
6. **Pages carry two or three lectures**, and the lecture boundary and the
   page boundary disagree: the split table in [pass2.md](pass2.md) has
   nineteen confirmed-not-executed entries. Several ideas have no owner or
   four (the prediction ledger had four until session H; authority has
   three; the event loop is explained in four parts).
7. **The front and back of the book were never revisited.** The introduction
   is three bullets from pass 1; the maps are four generated tables; the
   reference README is a list.
8. **Figures are all one kind.** Seventy-six sequence diagrams and one
   flowchart. The notebook names a dozen that are the wrong shape — state
   machines, filter cascades, trees, graphs and pipelines drawn as
   conversations — and a handful of pages whose real figure is a picture no
   mermaid type draws.

### The rulings

Decided now, so that sixteen sessions build on one frame rather than each
re-deciding it. A session may overrule a ruling with the page in front of
it, but writes down that it did, and why, in the log.

**R1 · Three tiers, and the appendix dissolves.** The site is *Parts*
(numbered I–XIII, watched in order), *Maps* (the atlas: looked at once), and
*Reference* (catalogues: looked up). The appendix stops being Part XIV:
`naming-drift` and `glossary` move to Reference; `out-of-scope-tour` becomes
the closing page of Part I as *what this book skips* — a viewer should know
the boundary before investing in thirteen parts, and its treemap wants to
live beside the maps. No part is renumbered and no new numbered part is
created in this pass; where a part has two halves (Part XII's terrain and
structures, Part VII's two tiers) the landing page says so.

**R2 · The template becomes a menu of shapes.** `TEMPLATE.md` is rewritten
(session A, from two pilots) from a skeleton into a menu. What every page
keeps: the title; the verified line with the part and the scenario; an
**opening paragraph that starts inside the scenario and ends on the hook** —
the one observable, surprising, true thing the page explains (the pass-2
findings are the hook bank: the block that comes back and vanishes again,
lava random-ticking twice, the watchdog kill that saves nothing, the
minimized window rendering frames nobody sees); a **cast** of at most eight
classes with role and thread, as a small table or in the narration, in place
of the field inventories (the exhaustive lists go to the class index, which
already exists); at least one figure; *Where to look* and the rules footer.
Everything between is the page's own, with headings that say what the
section says (*The two flushes*, *Who is told, and when*), never what
template slot it fills. The shapes:

| shape | for | its figure |
|---|---|---|
| **the trace** | one scenario through the system | a sequence diagram, narrated as prose in the order things happen, with each surprise placed where it happens |
| **the pipeline** | stages that hand off | a flowchart of stages at the top; a section per stage: what comes in, what is decided, what goes out |
| **the state machine** | phases and transitions | `stateDiagram-v2`, transitions labelled with the packets or events; a section per state; what can go wrong in each |
| **the policy** | who is told what, when | a decision table or flowchart per decision; the surprises are its rows |
| **the comparison** | two or three paths that differ | a table with the paths as columns; one diagram per path, or one with `alt` |
| **the vocabulary page** | the objects and their relations | a figure of the data (a containment or class diagram, or a flowchart), then a tour by object, grounded by one small trace |
| **the pattern** | one idea, many instances | the instances as a table; one instance traced |
| **the landing page** | a part | the part's shape as a figure of its pages |

Devices any page may use and none must: the myth table (*what the forum
says* / *what the decompile does*); *the number* (a count with its owner,
set off on its own line); the *for a 1.21-era reader* box (a styled
blockquote, replacing the names-you-will-hunt-for bullets); a
question-and-answer section where the surprises are answers to questions
players ask; the same trace seen from the other side (a mirrored
client/server pair, as `environment-attributes-and-timelines` already does);
the tick-boundary bar (`Note over` marking every tick crossed — session D's
rule) and the explicit *no reply* annotation (session H's).

The budgets, which are the enforceable part: a bulleted list holds parallel
items of at most two sentences, at most seven of them, and a page has at
most three lists; anything explanatory is prose; anything enumerative beyond
seven is a table, or Reference; every section has a figure or a subsection
before it passes forty lines; *Interfaces* survives only as a row of the
cast table or one sentence (what crosses the network, and as which
packets). A page is not done until it reads differently from its
neighbours.

**R3 · Every part has a landing page**, `src/systems/<part>/README.md`,
linked from the sidebar as the part itself: one paragraph on what the
system is and the one thing a player would recognise it by; the part's
shape as a figure of its pages (the conveyor, the hub, the ladder — pages
as nodes, what each hands to the next as edges); *before you start* — the
earlier pages this part assumes, by link; *watch in this order* — the
part's lectures with a one-line teaser each, which is the draft lecture
order `lectures.md` assembles; and the Reference pages the part uses. Under
a hundred lines, no trace. The sidebar folds to the current part; the
landing page is what the fold opens on.

**R4 · Figures.** The standing convention becomes: mermaid in the page for
anything mermaid 11.6.0 draws (`sequenceDiagram`, `flowchart`,
`stateDiagram-v2`, `classDiagram`, `timeline`, `block-beta` — the checker is
the arbiter of what the site's version accepts); **generated SVG** from
`tools/` for the maps and for figures no mermaid type draws (a treemap, a
bar chart, a tree with numbers on it), inlined with mdBook's `{{#include}}`
so it inherits the theme; **never a hand-drawn or raster image** — a figure
has to be regenerable on the next version, like a table. Every diagram is
checked by `tools/check_mermaid.js`, which is part of `tools/deploy.sh`.
Lanes: a lane is a class name abbreviated by the initials of its CamelCase
words, at least two letters, one meaning corpus-wide — `SGPL`, `CPL`, `MC`,
`MS`, `SL` — recorded in a lane key in `TEMPLATE.md` that session A writes
and every later session extends; collisions (`GR`, `CL`, `LX`, `SS`, `TP`,
`C`, `CM`, `PE`) are resolved by lengthening the later claimant. A short
whole word is allowed for a lane that is not a class (`Wire`, `Disk`,
`Main`).

**R5 · The Reference tier grows, and the rule for it is "would a viewer
pause the video to read this".** A table a viewer would pause on belongs in
Reference with the page linking to it. Members now: `math-and-primitives`
and `level-data-and-rules` (moved out of Parts II and IV), `naming-drift`
and `glossary` (out of the appendix), `threads` (kept; `anatomy` trims to
the four threads a viewer must hold), and the catalogues extracted from
lecture pages — the serializer list in `synched-entity-data`, the attribute
list in `attributes`, the HUD gate table `hud` compressed to prose, the
`EnchantmentHelper` hook table, the structure-piece families. Generated
where the decompile can generate them (`gen_reference.py` gains views);
hand-kept otherwise, and re-swept in pass 4. The glossary becomes generated
if session O finds a cheap per-page term declaration; otherwise it is
re-swept. The maps become the atlas: figures with prose, not tables alone.

**R6 · Where the shared ideas live.** *Authority*
(`Entity.isLocalInstanceAuthoritative` and its three siblings) gets its own
short page at the head of Part VI after `entity-anatomy`, in the comparison
shape — a mob and a player each taking one step, on each side — and Parts
VIII, IX and X link to it instead of re-teaching it. *The two loops* (the
tick cadence, the frame/tick interleave, the per-frame packet drain) become
a figure in `anatomy`, so Part IX's dependency on the client is a dependency
on Part I; `the-client-loop` stays in Part X as its hub. *The event loop*
(`BlockableEventLoop`, `TickTask`, `managedBlock`) is owned by `server-tick`
as a named section and linked from everywhere else. *The two update
channels* (shape versus neighbour updates) become one flowchart of
`Level.setBlock`'s tail, drawn once in `blocks-and-states` and reused by
reference. *`Component`* gets a Part II page — the object is a foundation,
not a networking detail — so `text-and-fonts` and `chat-and-signing` stop
sharing a subject. *The data-driven type pattern* (a registry of
codec-loaded element types: loot functions, features, density functions,
placement modifiers, dialogs, tests) gets a Part II page as the part's
closer, and `dialogs-and-tests` may then split without losing its argument.
*The scoreboard* stays in Part XIII (its trace is a command) and Part IV's
landing page points at it as level state. *`prediction-and-acks`* stays in
Part X; the Part V pair (`block-interaction`, `block-breaking`) gets one
shared preamble that states the ledger's contract in three sentences and
links forward. *`density-functions`* opens Part XII; *`the-frame`* opens
Part XI, then the substrate (`the-window`, `blaze3d`), then the pipeline.
*`environment-attributes-and-timelines`* stays in Part IV and is placed
early in the lecture order. The cross-part lecture order stays I → XIII as
numbered; `lectures.md` is assembled from the landing pages by session P.

**R7 · What pass 3 writes, and what it does not.** It executes the splits
and merges the notebook confirmed (they are in the schedule, per part); it
writes the owner pages in R6; and each part session may add **at most one**
of the coverage pages the pass-2 inventories found (post-processing,
block-entity rendering, item models, how a server dies, the spear, drawing
a bow, status effects, the permission model, the function model,
`GameTestHelper`, the selector grammar) — the rest go to the coverage queue
in [pass3.md](pass3.md) §7, discharged by session P if there is budget and
otherwise carried forward, written down. Pass 3 may drop material from a
page only by moving it (to Reference, to another page) or by logging the
cut in [pass5.md](pass5.md) with the reason. And **every page pass 3
rewrites is listed in [pass4.md](pass4.md)** with the claims the rewrite
introduced (hooks, redrawn orderings, new sections), because pass 4 checks
those hardest.

**R8 · URLs live forever.** Every moved or renamed page gets an
`[output.html.redirect]` entry in `book.toml`, as the X/XI split did.
`llms-full.txt` follows `SUMMARY.md` and needs nothing.

### Session protocol

One session = one part (large parts may take two; the schedule says
which), except the four site sessions (A, B, O, P). Each part session:

1. **Read** this charter, `CLAUDE.md`, `TEMPLATE.md` (the menu and the lane
   key), the part's notes in [pass3.md](pass3.md) — grep the part in every
   section, not just §1 — the part's rows in [pass2.md](pass2.md)'s split
   table and its hand-off section (the hook bank and the on-spec material),
   and the pages.
2. **Rule before editing.** Write the part's shape, the page list after
   splits/merges/moves/extractions, each page's shape from the menu and its
   hook, into the session's log entry *first*. Decisions first, so the work
   can be checked against them.
3. **Restructure.** Create, split, merge and move files; `SUMMARY.md`;
   redirects; cross-links (grep the corpus for every old link).
4. **Reshape.** Rewrite each page in its shape, hook first, figures redrawn
   where the notebook says the shape is wrong, lanes from the key, the
   bullet budget kept. Agents may draft pages in parallel given the old
   page, the shape, the notebook's notes, the menu and the rules — but the
   session **diffs every draft's claims against the old page** before
   accepting it: a fact reworded is a fact changed until proven otherwise,
   and pass 4 is a net, not a licence. Anything an agent adds that the old
   page did not say goes on the pass4.md list.
5. **The landing page**, and the part's lecture list in `lectures.md`.
6. **Verify and ship.** `python tools/verify_names.py` ·
   `node tools/check_mermaid.js` · `mdbook build` clean · class index
   regenerated if pages moved · commit `pass 3, Part N: <summary>` · deploy.
7. **Log and hand off.** The session log below; [pass4.md](pass4.md) (pages
   rewritten, claims introduced, diagrams redrawn); [pass5.md](pass5.md)
   (wording debt, cuts); [pass3.md](pass3.md) (anything structural found for
   a *later* session — a cross-part consequence, a coverage-queue entry, a
   lane).

Three lessons carried from pass 2 that bite here too: **suspect the tool
once before rewording the page** (the checker, the verifier and the
generators all had bugs in pass 2); **grep the corpus for every moved
claim** — a fact that moves to a new owner page must be removed from its
old hosts, not duplicated; and **a landing page is a claim about order**,
which pass 4 must check like any other.

### Schedule

Tick as done. Sessions A, B, O and P are the site; C–N are the parts, in
sidebar order.

- [x] **Session A — The frame.** *(done 2026-09-02)* Two pilot pages reshaped end to end —
  `tickets-and-loading` (a policy page: eleven lanes today; wants a
  flowchart and a small state diagram) and `protocol-phases` (a state
  machine) — and then `TEMPLATE.md` rewritten from what worked: the menu,
  the devices, the budgets, the lane key. The introduction rewritten as a
  front door (what the game is as a program, in a page; how the site is
  read; the three tiers; the rules; `llms-full.txt`). The landing-page spec
  proven on Part I's. `lectures.md` reduced to a skeleton the parts fill. A
  lane linter if it is cheap (a lane not in the key fails).
- [x] **Session B — Maps: the atlas.** *(done 2026-09-02)* `map_source.py` grows an SVG output
  and the maps become figures with prose: the jar as a treemap by package,
  coloured client-only versus shared (which is also the *two jars* figure
  the introduction wants); the biggest classes and the fan-in hubs as bars;
  the widest hierarchies as trees; the threads as a figure beside
  `reference/threads.md`. This session builds the figure pipeline
  (`{{#include}}`, theming through `custom.css`) every later session
  reuses, which is why it comes second.
- [x] **Session C — Part I Anatomy · Part II Foundations.** *(done 2026-09-02)* `anatomy` split
  into a startup diagram and a steady-state one, the two-loops figure, the
  threads table trimmed to four rows; `out-of-scope-tour` joins Part I as
  *what this book skips*, with the treemap. Part II: `math-and-primitives`
  to Reference; `codecs-nbt-json` leads; the registries/tags/resources knot
  cut where §1 says (state the freeze rule, pay it off in tags); the
  `Component` page and the data-driven-types page written or ruled out with
  the pages open; `resource-system`'s two traces settled as one lecture
  with a coda, or two.
- [ ] **Session D — Part III The server.** Lifecycle last and reframed as
  *how a server dies* (three endings, one diagram; startup gets its own
  diagram with the JVM main thread as a lane); the event-loop section in
  `server-tick`; `server-level-tick`'s guard flowchart beside its trace;
  `players-and-sessions` as a join trace plus a three-path comparison, its
  nine-lane diagram split in two.
- [ ] **Session E — Part IV The world.** The conveyor made explicit:
  `chunk-anatomy` first, then the four pipeline pages handing off;
  `block-ticks-and-fluids` and `game-events-and-poi` each split in two;
  `level-data-and-rules` to Reference; the pyramid drawn; the light batch
  drawn; `tickets-and-loading` from the pilot re-checked. Probably two
  sessions.
- [ ] **Session F — Part V Blocks.** The update-channels flowchart in
  `blocks-and-states`; `block-interaction` + `block-breaking` as one lecture
  in two halves with the shared preamble; `redstone` split three ways
  (signal and dust · pistons and block events · diodes, comparators and the
  observer); `block-entities` kept as the part's model page.
- [ ] **Session G — Part VI Entities.** The authority page; the serializer
  and attribute catalogues to Reference (generated); `entity-lifecycle`'s
  spawner as a filter-cascade flowchart; `ai-goals-and-brains` ruled (three
  lectures — pathfinding is the strongest); the non-living `hurtServer` gap
  ruled (section, sibling page, or Reference table).
- [ ] **Session H — Part VII Items and inventories.** The two-tier landing
  (vocabulary, then three engines); `loot-tables` split into *contexts and
  predicates* plus loot as its worked example; enchantment acquisition out
  of `enchantments`; the *drawing a bow* trace as the use pipeline's second
  half; item-model ownership settled with session L.
- [ ] **Session I — Part VIII The player.** `player-anatomy` split into the
  reference half and the two-phase-tick trace; status effects out of
  `hunger-xp-and-effects`; the spear ruled (own lecture or
  `the-sword-swing`'s coda); `the-sword-swing`'s damage pipeline drawn as a
  flow over one number.
- [ ] **Session J — Part IX Networking.** `the-connection` +
  `packets-and-stream-codecs` taught as one lecture with one round-trip
  diagram (merge or shared trace — ruled with the pages open);
  `protocol-phases` from the pilot; `what-the-client-is-told` as a policy
  page with its `ClientLevel` sections handed to Part X; `chat-and-signing`
  with the adversary table. Part IX's three borrowed facts replaced by links
  to Parts I and III.
- [ ] **Session K — Part X The client.** The hub-and-spokes landing, each
  spoke named by its cadence; `sound` split (the engine · what makes a
  sound happen); the GUI stack as the part's one internal pipeline,
  `the-gui-render-tree` drawn as a tree; `hud`'s gate table to Reference;
  `prediction-and-acks` as a two-column state diagram;
  `debugging-the-running-game` placed.
- [ ] **Session L — Part XI Rendering.** Frame → substrate → pipeline;
  `the-window`'s retry loop as a flowchart; `models-and-atlases`'
  fan-out/barrier drawn; the lane collisions fixed; one of post-processing
  / block-entity rendering / item models written (R7), the others queued.
  Probably two sessions.
- [ ] **Session M — Part XII World generation.** `density-functions` first,
  its three-graphs figure as generated SVG or a before/after pair;
  `structures` split into placement and jigsaw beside
  `hand-built-structures`; `worldgen-pipeline`'s nested cell loop drawn as
  nesting; the two halves (terrain · structures) on the landing page.
- [ ] **Session N — Part XIII Commands and data packs.** The stack landing
  (parse → execute → what commands are for); the permission model out of
  `brigadier-and-commands`; `execution-and-functions` split into the engine
  and the function model, the queue drawn as snapshots; advancements'
  client screen ruled; `dialogs-and-tests` split if the Part II pattern
  page exists; the scoreboard stays.
- [ ] **Session O — Reference.** The moved pages redirected and reframed;
  the extracted catalogues generated (`gen_reference.py` views for
  serializers and attributes at least); the glossary generated or re-swept;
  the reference README as a real page; the class index regenerated;
  `threads` beside its figure.
- [ ] **Session P — The lecture order and the close.** `lectures.md`
  assembled from the landing pages with the cross-part dependencies stated;
  the parts-dependency figure in the introduction; the cross-corpus sweep
  (lane key complete, links, every landing page's *before you start* true,
  redirects); the coverage queue discharged as budget allows; the
  distribution of page shapes checked (if half the corpus chose the trace,
  the menu failed); pass 4's charter written; pass 3 closed.

### Hand-off rules

Three files, three kinds of note. [pass3.md](pass3.md) — structural, for a
later pass-3 session (its §7 is the coverage queue). [pass4.md](pass4.md) —
factual: what pass 4 must re-check, per page. [pass5.md](pass5.md) —
wording debt and cuts. Anything left for later is written when it is
found, not at the end.

---

## Pass 4 — the second fact-check (sketch; charter written by session P)

Pass 2's protocol, archived in [pass2.md](pass2.md) with its twelve lessons,
run again over the whole corpus: one adversarial agent per page briefed to
falsify, the NAMES section, the call-site counts, the complete populations
behind every "only" and "not", the re-derived numbers. Three additions pass
3 makes necessary: the **landing pages and `lectures.md` are claims about
order and dependency** and get checked as such; **redrawn diagrams assert
orderings** and each is checked arrow by arrow; and the
[pass4.md](pass4.md) list of claims pass 3 introduced is checked first and
hardest. Pass 4 does not restructure and does not polish; it fixes facts and
logs the rest.

## Pass 5 — polish (sketch)

Per page: does it read well, is everything needed explained and nothing
more? This is where pass 2's "don't worry about length" bill comes due —
cut what over-grew, using the on-spec logs in [pass2.md](pass2.md)'s
hand-off and [pass5.md](pass5.md). Corpus-wide: one terminology sweep (the
glossary is the checklist), one voice sweep against the best page, links
and cross-references complete, the "not X but Y" tic and the
named-qualifier tic hunted.

## Pass 6+ — the owner reads

Unchanged from the original conception: part by part, decompile open,
questions left **in the page** as `<!-- Q: … -->` comments; a session
answers each in the prose — if the owner had to ask, the page was wrong or
missing it — and removes the comment. The owner confirms or reorders
`lectures.md`. Then voice and cuts, and recording.

## Risks

- **Interesting and wrong.** A rewrite for shape reorders and rewords
  facts, and pass 2 proved that is where errors live. Pass 4 exists for
  this; the claim-diff in protocol step 4 is the cheaper guard.
- **A second uniformity.** A menu of eight shapes can become eight
  templates. The budgets are the floor, not the ceiling; session P checks
  the distribution, and a page that reads like its neighbour is not done.
- **Scope creep through new pages.** R7's one-per-part cap. The coverage
  queue is the pressure valve, and it is allowed to be long.
- **A session that does not fit.** Parts IV, XI, XII and XIII may take two
  sessions; take two rather than ship half a part. A part is shipped whole
  or not at all, because its landing page and `SUMMARY.md` change together.
- **URL churn.** Redirects for every move; check the redirect table before
  deploy.
- **mermaid features.** The site pins 11.6.0; a diagram type the checker
  rejects is not available, whatever the docs say. Upgrading mermaid is a
  deliberate act (`mdbook-mermaid install` plus a re-check of every
  diagram), not a drift.
- **26.3 lands mid-pass.** Finish on 26.2; re-verify once, in one session,
  between passes.

## Session log — pass 3 onward

- **2026-09-02, planning session** — pass 2 closed: its charter, protocol
  and session log archived into [pass2.md](pass2.md); this plan rewritten
  for passes 3–6 (the second fact-check inserted as pass 4; polish and the
  owner's read renumbered). Pass 3 chartered above with eight rulings and
  sixteen sessions. Site mechanics that no ruling depends on were fixed at
  once: `[output.html.fold]` collapses the sidebar to the current part;
  `custom.css` widens the column for tables and diagrams and caps prose at
  800px; `tools/check_mermaid.js` parses every built diagram with the
  site's own mermaid and is a gate in `tools/deploy.sh` — **41 of the 77
  diagrams were failing**, every one from a `;` in a label, and three more
  were silently truncated at a `#`; all fixed with syntax-only edits (75
  lines in 40 pages, `;` → `#59;` and `#` → `#35;`).
  [pass4.md](pass4.md) and [pass5.md](pass5.md) opened; `CLAUDE.md`,
  `README.md`, `TEMPLATE.md` and `lectures.md` brought current.
  **Second half, on two owner notes.** Diagrams that render are still too
  small to read: `diagram-zoom.js` opens any diagram at viewport size on
  click, on the page's own background. And the fact base was widened
  *before* pass 3 rather than after it: session K had recorded one question
  the decompile could not settle because Brigadier is not in the tree, and
  that was the visible tip of a larger gap — pass 2 took every claim about
  Brigadier, DataFixerUpper and authlib on trust, and every data-driven claim
  (atlases, fonts, post-effect chains, shaders) against a tree that held the
  jar's `data/` but not its `assets/`. Now staged, all gitignored: the jar's
  `assets/` minus textures beside `data/`; Brigadier 1.3.10 and
  DataFixerUpper 10.0.21 from their published source jars; authlib 9.0.75
  decompiled from the launcher's jar with the PvP mod's Vineflower — by the
  new `tools/fetch_libs.sh`. `verify_names.py` indexes `reference/libs/` and
  twenty-seven allow-list entries were retired, so library names are now
  checked at member level; all 19,745 names still resolve. The `execute
  store` question is answerable and is on pass 4's list. Also noted: this
  machine has 26.3 snapshots 8 and 9 installed, on authlib 10.0.77 and
  Brigadier 1.3.11 — the 26.3 risk is near, and `fetch_libs.sh` carries the
  versions to bump.
- **2026-09-02, session A — the frame.** *Rulings, written before editing.*
  **`tickets-and-loading` takes the policy shape.** Its questions are
  decisions — what level a chunk gets, which graph answers which question,
  when a holder is promoted or demoted, what a player is sent and when a
  ticket dies — so the page becomes one figure per decision: a flowchart of
  ticket → level → status → future, a `stateDiagram-v2` of the four
  `FullChunkStatus` values, three decision tables, and one six-lane trace of
  the walk east kept as the grounding. Hook: two graphs share one ticket
  store, so a chunk can be entity-ticking by holder status and tick nothing.
  The field inventories go (logged in pass5.md); the nine-row ticket table
  stays, because nine is past the list budget and the table is the
  reference. **`protocol-phases` takes the state-machine shape.** Two
  `stateDiagram-v2`s — the five `ConnectionProtocol`s with the terminal
  packets as transitions, and `ServerLoginPacketListenerImpl.State` with
  its orphan — one small sequence diagram for the encryption handshake
  alone, one flowchart for the configuration task queue; a section per
  phase ending in what disconnects it. Hook: the `ServerPlayer` is built
  after the client has acknowledged the end of the phase named for
  preparing it. **`TEMPLATE.md`** becomes the menu (R2) with the two
  pilots named as its worked examples, the devices, the budgets, the
  mermaid rules the checker enforces, and the lane key — seeded with the
  hubs whose spelling is already the majority, the two pilots' lanes and
  Part I's; one-word classes take a fixed prefix of two or more letters
  (`Conn`), not one initial. **`tools/check_lanes.py`** is the lane linter:
  every key expansion must be a class in the decompile (hard), a lane in
  the key must mean the same class on every page (report-only until session
  P; `--strict` fails; `--pages` scopes it to a part). **The introduction**
  becomes the front door with one figure of the two programs and the wire;
  the two-jars treemap (B) and the parts-dependency figure (P) are named
  as placeholders, not drawn. **Part I's landing page** is written as the
  R3 proof: its figure is a root, `anatomy` handing a thread to every part.
  **`lectures.md`** becomes a skeleton, one section per part, Part I filled.
  No page moves this session, so no redirects.
  *Done.* Both pilots rewritten and shipped: `tickets-and-loading` at 330
  lines with a flowchart, a state diagram, three decision tables, a six-lane
  trace (was eleven) and a *questions players ask* close;
  `protocol-phases` with two state diagrams, a three-lane handshake, the
  task-queue flowchart and a section per phase. The reshaping surfaced one
  pass-2 error: the keep-dimension-active flag is on the player
  *simulation* ticket, not the loading tickets (pass4.md has it).
  `TEMPLATE.md` is the menu, with the two pilots as its worked examples;
  `tools/check_lanes.py` is written and in `deploy.sh` (key verified
  against the decompile, page drift report-only until session P) and
  generates `src/reference/lanes.md` so readers see the key; the
  introduction is the front door with the two-programs figure; Part I's
  landing page is the R3 proof and the sidebar's Part I now opens on it;
  `lectures.md` is the skeleton. 84 diagrams checked, 0 failed; all names
  resolve; hand-offs in pass3.md §8, pass4.md and pass5.md.
- **2026-09-02, session B — maps: the atlas.** *Rulings, written before
  editing.* **One generated directory.** Everything a page includes that a
  tool wrote lives in `src/generated/` — the SVG figures and the markdown
  tables — and nothing there is hand-edited; `python tools/map_source.py`
  with no argument rewrites all of it, so regenerating on the next version
  can never clobber prose. `llms_full.py` expands the markdown includes and
  replaces an SVG include with a one-line note, so agents get the tables.
  **The figure pipeline** is `<figure class="map">` + `{{#include
  ../generated/<name>.svg}}` + `<figcaption>`, with the SVG carrying only
  classes (`svg.mapfig`, `.shared`, `.client`, `.skip`, `.lib`) and all
  colour, font and theme in `custom.css`; text is `currentColor`, so the
  five mdBook themes and the zoom overlay all read. **The atlas is four
  maps and a front page**, each a figure with prose then the table it
  summarises: *where the code is* (`packages`: the jar as a treemap of
  packages, area by lines, colour by jar, the out-of-scope packages
  hatched — which is also the two-jars figure the introduction wanted and
  the treemap `out-of-scope-tour` wants in session C); *where the mass is*
  (`biggest`: bars); *what everything imports* (`fanin`: bars, with the
  library classes the old table could not see — `Codec` was not counted —
  now counted and marked); *what extends what* (`hierarchy`: trees with
  numbers on them for the roots the parts teach, and the table split into
  class roots and interface roots, because the old table's top was mixin
  interfaces). File names and URLs do not change (R8); sidebar titles do.
  **The threads figure is mermaid** (R4: mermaid for what mermaid draws): a
  flowchart beside `reference/threads.md` of every thread a lecture leans
  on and the three ways work crosses between them — a posted task, a
  completed future, a hopped packet handler — drawn from the pass-2
  verified table, no new fact. **The verifier stops skipping `maps/`** now
  that the atlas has prose; it skips `generated/` instead. The atlas pages
  say how each number was counted (a class is one `.java` file, a line is a
  line of decompiled source, client-only is absence from
  `server-classes.txt`, fan-in is import statements), because pass 4 will
  re-derive them.
  *Done.* `tools/map_source.py` rewritten: it writes `src/generated/` —
  six markdown tables and seven SVGs (the treemap, two bar charts, four
  trees) — and `deploy.sh` runs it first, so the atlas cannot drift from
  the decompile. Rewriting it found two bugs in the old view: nested
  classes and records were invisible to the hierarchy parser (every count
  moved; `Goal` went from 70 to 200 because two thirds of its subclasses
  are nested in the mobs that use them; `Packet` appeared at 232), and the
  import count ignored `com.mojang.*`, which hid the best fact on the map:
  `Codec` is the second most-imported class in the game. The five atlas
  pages are prose over figures over tables — *where the code is*, *where
  the mass is*, *what everything imports*, *what extends what*, and a front
  page that says how every number is counted. The treemap is in the
  introduction as the two-jars figure; `reference/threads.md` has its
  mermaid figure of the eight threads and the three ways work crosses
  between them; `verify_names.py` now checks the atlas prose (all 19,895
  names resolve); `llms_full.py` expands includes; the figure recipe is in
  `TEMPLATE.md` and `CLAUDE.md`. Rendered and looked at in the light and
  navy themes with headless Chrome before shipping. 85 diagrams, 0 failed.
  Hand-offs in pass3.md §8 (session C's treemap include, the `SKIPPED`
  list), pass4.md (every number, the tool itself, `entity-anatomy`'s
  corrected 193) and pass5.md.
- **2026-09-02, session C — Part I Anatomy · Part II Foundations.**
  *Rulings, written before editing.* **Part I is a root of two pages.**
  `anatomy` keeps the trace shape but takes **two figures**: a startup
  sequence (the JVM main thread becoming the Render thread, the Server
  thread born in `MinecraftServer.spin`, the in-process channel) and the
  two-loops figure R6 asks for — a flowchart of the frame loop and the tick
  loop side by side with the packet drain in each, which Parts III, IX and
  X then link to instead of restating. Hook: the client walks the same
  handshake against the server in its own process as against one across
  the world, and the one thing that leaks between them is a setting —
  pause is decided on the client and enforced by the server, so a
  published LAN world never pauses. The threads table trims to the four a
  viewer must hold (Render, Server, Netty, workers) and defers the rest to
  `reference/threads.md`, which already carries every row; the situational
  paragraph goes with it. The invariants that belong to Part III (the
  `haveTime` budget, sprinting, the stale `TickTask`, the overload
  warning, the flush bracket) are already owned by `server-tick` and are
  cut here to a link, logged in pass5.md as moved. **`out-of-scope-tour`
  becomes `systems/anatomy/what-this-book-skips.md`** (R1; redirect from
  the appendix URL), opening on the treemap with the skipped packages
  hatched, a section per skipped thing as today, and the four-way rulings
  list compressed to one table. Hook: vanilla's own content is a data pack,
  and the generator that writes it ships in the server jar and is called
  by the running game. **The appendix dissolves now, not in session O**:
  `naming-drift` and `glossary` move to `src/reference/` with redirects
  and their headers corrected, because a Part XIV of two look-up pages is
  not a part (R1); session O reframes them. **Part II is a stack**, drawn
  on its landing page bottom-up: codecs (how anything becomes data) →
  registries (how anything gets a name and a number) → the resource system
  (where data comes from and when) → tags (data reaching into code) → data
  components and text components (data on an object) → the data-driven
  type pattern (the closer, which every data-pack file is an instance of).
  `math-and-primitives` moves to `src/reference/` (redirect; header
  reframed; the notebook's coordinate-spaces figure left for session O).
  Page shapes and hooks: **`codecs-nbt-json`** leads and takes the
  **comparison** shape — one `ItemStack` four ways is four paths that
  differ, so a table with the paths as columns and one short diagram per
  path replace the ten-lane conversation; hook: the click on a chest slot
  sends the server no item data at all, only a checksum per component.
  **`identifiers-and-registries`** keeps the **trace** shape with its two
  diagrams (the notebook calls them the model for the corpus); hook: the
  wire id of a diamond sword is the line number of its registration in
  `Items`; it states the freeze rule (contents never change; tags and
  components do) without justifying it. **`resource-system`** is one
  lecture in the **pipeline** shape — discover, snapshot, prepare in
  parallel, apply in order, finish or roll back — with the prepare/apply
  lattice drawn as a flowchart with three listeners explicit (the
  notebook's clearest wrong-shape case), F3+T as the grounding trace and
  `/reload` as a comparison coda (what differs, as a table); hook: a reload
  that fails does not find the bad pack, it deselects every pack and
  reloads again. **`tags`** keeps the **trace** shape and pays the freeze
  rule off; hook: a frozen registry's contents cannot change, and yet
  `/reload` changes what `#minecraft:logs` contains — the tag table is the
  one part of a frozen registry that is swapped, in three ordered steps
  with no lock. **`data-components`** takes the **vocabulary** shape — a
  figure of prototype, patch and map, a tour by object, the enchanting
  trace cut to the grounding so Part VII keeps the enchanting table; hook:
  an item's prototype is built on every reload with the world's registries
  in hand, not in its constructor, which is why a stack cannot be decoded
  before the first reload. **`text-components`** is written (R6): the
  **vocabulary** shape — contents, style, siblings as a figure; the seven
  contents kinds as the table; one small trace of a death message crossing
  the wire as a translation key and being worded on the client; hook: the
  client receives the death message before anyone knows what it says. The
  `Component` section of `chat-and-signing` moves here and that page links
  (grep-the-corpus rule); `text-and-fonts` points here. **`data-driven-types`**
  is written (R6) as the part's closer in the **pattern** shape: the idea
  (a `type` field is a lookup in a registry data packs cannot extend), the
  instances as a table drawn from every `Registry<MapCodec<? extends …>>`
  and every `…Type<?>` registry in `BuiltInRegistries`, one instance traced
  from JSON to object; hook: `type` is the most important key in a data
  pack. `dialogs-and-tests` keeps its own statement of the pattern until
  session N links here. Lanes: 45 rows added to the key before drafting;
  `CH`, `MC`, `IS`, `PE`, `TP` collisions in Part II resolved by lengthening
  the later claimant (`CHelp`, `IStack`, `PEnc`, `TagP`); expansions are the
  bare class name, thread in the cast. Agents draft in parallel; every
  draft's claims are diffed against the old page before acceptance.
  *Done.* Part I: `anatomy` rewritten as a trace with two figures — the
  startup sequence (seven lanes, the JVM main thread becoming the Render
  thread, the Server thread born in `spin`) and the two-loops flowchart
  Parts III, IX and X now link to — the threads table cut to four rows
  with `reference/threads.md` carrying the rest, the Part III invariants
  cut to a link; `out-of-scope-tour` became `what-this-book-skips` in Part
  I with the treemap and the rulings as one table; `naming-drift` and
  `glossary` moved to Reference and the appendix is gone from the sidebar
  (four redirects). Part II: seven pages in a stack, drawn on a new
  landing page — `codecs-nbt-json` leads in the comparison shape (a
  four-column table and four short diagrams for the ten-lane one),
  `identifiers-and-registries` keeps its two traces and states the freeze
  rule, `resource-system` is a pipeline with the prepare/apply lattice
  drawn and `/reload` as a comparison table, `tags` pays the freeze rule
  off, `data-components` is a vocabulary page with the enchanting trace
  cut to its Part II core, and two R6 pages were written from the decompile:
  `text-components` (the death message worded on the client) and
  `data-driven-types` (fifty-six registries of kinds, `set_count` traced
  from JSON to a chest). `math-and-primitives` is Reference.
  `chat-and-signing`'s `Component` section is a pointer; `text-and-fonts`
  points here. Fifty-two lane rows added; `check_lanes --strict` is clean
  for both parts. **Two pass-2 errors caught by drafting agents**: the axe
  does not strip by tag (`AxeItem.STRIPPABLES` is a map), and
  `NoiseRouterData` does not call `TerrainProvider` per chunk (its
  bootstraps are datagen and `Commands.validate`); both verified by the
  session and logged in pass4.md. 97 diagrams, 0 failed; 19,720 names
  resolve. Hand-offs in pass3.md §8 (the two Part III invariants still on
  `anatomy`, the three enchanting facts for session H, the treemap's
  hatch limitation, the pattern page's *taught in* obligations), pass4.md
  (every introduced claim, per page) and pass5.md (every cut name).
  Process note: nine pages drafted by parallel agents against a shared
  brief, each report diffed by the session; three agents lost to an
  interrupt were relaunched on Opus with no visible loss — the part
  sessions from D on should run on Opus, with Fable kept for O, P and the
  inter-pass planning.
