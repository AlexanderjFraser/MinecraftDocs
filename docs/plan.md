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
- [x] **Session D — Part III The server.** *(done 2026-09-02)* Lifecycle last and reframed as
  *how a server dies* (three endings, one diagram; startup gets its own
  diagram with the JVM main thread as a lane); the event-loop section in
  `server-tick`; `server-level-tick`'s guard flowchart beside its trace;
  `players-and-sessions` as a join trace plus a three-path comparison, its
  nine-lane diagram split in two.
- [x] **Session E — Part IV The world.** *(done 2026-09-02)* The conveyor made explicit:
  `chunk-anatomy` first, then the four pipeline pages handing off;
  `block-ticks-and-fluids` and `game-events-and-poi` each split in two;
  `level-data-and-rules` to Reference; the pyramid drawn; the light batch
  drawn; `tickets-and-loading` from the pilot re-checked. Probably two
  sessions.
- [x] **Session F — Part V Blocks.** *(done 2026-09-02)* The update-channels flowchart in
  `blocks-and-states`; `block-interaction` + `block-breaking` as one lecture
  in two halves with the shared preamble; `redstone` split three ways
  (signal and dust · pistons and block events · diodes, comparators and the
  observer); `block-entities` kept as the part's model page.
- [x] **Session G — Part VI Entities.** *(done 2026-09-03)* The authority page; the serializer
  and attribute catalogues to Reference (generated); `entity-lifecycle`'s
  spawner as a filter-cascade flowchart; `ai-goals-and-brains` ruled (three
  lectures — pathfinding is the strongest); the non-living `hurtServer` gap
  ruled (section, sibling page, or Reference table).
- [x] **Session H — Part VII Items and inventories.** *(done 2026-09-03)* The two-tier landing
  (vocabulary, then three engines); `loot-tables` split into *contexts and
  predicates* plus loot as its worked example; enchantment acquisition out
  of `enchantments`; the *drawing a bow* trace as the use pipeline's second
  half; item-model ownership settled with session L.
- [x] **Session I — Part VIII The player.** *(done 2026-09-03)* `player-anatomy` split into the
  reference half and the two-phase-tick trace; status effects out of
  `hunger-xp-and-effects`; the spear ruled (own lecture or
  `the-sword-swing`'s coda); `the-sword-swing`'s damage pipeline drawn as a
  flow over one number.
- [x] **Session J — Part IX Networking.** *(done 2026-09-03)* `the-connection` +
  `packets-and-stream-codecs` taught as one lecture with one round-trip
  diagram (merge or shared trace — ruled with the pages open);
  `protocol-phases` from the pilot; `what-the-client-is-told` as a policy
  page with its `ClientLevel` sections handed to Part X; `chat-and-signing`
  with the adversary table. Part IX's three borrowed facts replaced by links
  to Parts I and III.
- [x] **Session K — Part X The client.** *(done 2026-09-03)* The hub-and-spokes landing, each
  spoke named by its cadence; `sound` split (the engine · what makes a
  sound happen); the GUI stack as the part's one internal pipeline,
  `the-gui-render-tree` drawn as a tree; `hud`'s gate table to Reference;
  `prediction-and-acks` as a two-column state diagram;
  `debugging-the-running-game` placed.
- [x] **Session L — Part XI Rendering.** *(done 2026-09-03)* Frame → substrate → pipeline;
  `the-window`'s retry loop as a flowchart; `models-and-atlases`'
  fan-out/barrier drawn; the lane collisions fixed; one of post-processing
  / block-entity rendering / item models written (R7), the others queued.
  Probably two sessions.
- [x] **Session M — Part XII World generation.** *(done 2026-09-03)* `density-functions` first,
  its three-graphs figure as generated SVG or a before/after pair;
  `structures` split into placement and jigsaw beside
  `hand-built-structures`; `worldgen-pipeline`'s nested cell loop drawn as
  nesting; the two halves (terrain · structures) on the landing page.
- [x] **Session N — Part XIII Commands and data packs.** *(done 2026-09-03)* The stack landing
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
- **2026-09-02, session D — Part III The server.** *Rulings, written before
  editing.* **Part III is a line into a loop and out again**, and the
  landing page draws exactly that: `starting-a-server` runs into
  `server-tick`, which turns with `server-level-tick`, with
  `players-and-sessions` hanging off the loop as who is in it, and
  `how-a-server-dies` at the exit. **The part gains one page** — R7's
  allowance, spent on the coverage queue's *how a server dies* — and
  `server-lifecycle` splits, which **overrules the schedule line** ("lifecycle
  last and reframed … startup gets its own diagram"): the schedule asked for
  one page with two traces, and one page with two traces is precisely the
  lecture/page mismatch this pass exists to fix (charter §*What is wrong
  today* item 6). Session B's own note called *how a server dies* "the
  strongest new page candidate found in Part III". The side threads, which
  span both halves, are described where they are **created** (startup) and
  their non-daemon consequence is stated where it **bites** (the death page's
  `onServerExit`). `server-lifecycle.md` becomes
  `starting-a-server.md` with a redirect (R8); nothing outside Part III
  linked to it. **The five pages, their shapes and their hooks.**
  **`server-tick`** keeps the **trace** shape but takes a seven-lane
  sequence that ends on the wire, so the two flushes are visible rather
  than asserted, plus a small flowchart of the budget for the **event-loop
  section R6 gives it to own** (`BlockableEventLoop`, `TickTask`,
  `shouldRun`, `managedBlock`) — the section four parts link to instead of
  re-explaining. Hook: "Can't keep up!" is not a warning that the server is
  skipping ticks, it *is* the skip, and the same condition holds the log, so
  a server that complained recently stays behind instead. It also absorbs
  the two Part I invariants `anatomy` still carries (the `haveTime` "gates
  exactly three things" claim, the sprint-polls-chunk-sources conclusion),
  cut there to a link. **`server-level-tick`** trades its twelve-lane
  conversation for the **guard flowchart** the notebook asked for — the
  fourteen phases with their gates (`runsNormally`, `emptyTime`, `isDebug`,
  none) on the arrows, which carries the ordering and the gating at once —
  plus a four-lane sequence of the block-change broadcast alone. It opens by
  defining the three chunk ranges in two sentences (pass3 §5's
  recommendation) so the page does not borrow Part IV's vocabulary
  unexplained. Hook: the tick broadcasts its block changes *before* it ticks
  its entities, so a change an entity makes always reaches the client a tick
  later than a change a command makes. **`players-and-sessions`** becomes a
  **trace** and a **comparison** with the seam the notebook found: the join
  as two diagrams (admission and configuration, then `placeNewPlayer`'s
  packet burst) in place of the nine-lane one whose implied concurrency was
  wrong anyway, then the exits as a four-column table (respawn · dimension
  change · disconnect · `switchToConfig`) with the question people actually
  ask as its headings. Hook: dying destroys and rebuilds your `ServerPlayer`
  while a trip to the Nether does not, and both keep the entity id and the
  same connection object. **`starting-a-server`** is the **trace** shape
  with the diagram the notebook asked for: the only figure in the corpus
  where the **JVM main thread is a lane**, handing off to the Server thread
  and never appearing again. Hook: the step the loading screen calls
  preparing the world loads no chunks at all on an ordinary world —
  `prepareLevels` re-arms persisted tickets, and only `/forceload` and
  portal tickets persist. **`how-a-server-dies`** is the **comparison**
  shape: three endings (`/stop`, a tick-loop crash, a watchdog kill) as the
  columns, `/stop` traced in full because the other two are differences from
  it, and a four-lane sequence of the watchdog's self-deadlock. Hook: a
  crash saves your world and the watchdog does not — `System.exit` runs a
  hook that joins the very thread that is wedged. **Lanes**: the Part III
  rows go into the key before drafting; `G` becomes `SGPL` (the notebook's
  odd one out), `LevelTicks` lengthens to `LTs` because session C's
  `LT` is `LootTable`, and `SL`/`MS` lose their parenthetical labels so the
  linter can read them. `check_lanes.py --strict --pages src/systems/server`
  before shipping.
  *Done.* Part III is five pages in a line-into-a-loop, drawn on a new
  landing page the sidebar's Part III opens on. `server-tick` is a
  six-lane trace that ends on the wire, so the two writes per client are
  visible rather than asserted, and it now owns **the event loop** (R6) as
  a named section with a flowchart of `pollTask` → `shouldRun` →
  `haveTime` and the `managedBlock` suspension — the section four parts
  will link to instead of re-explaining; `anatomy`'s two Part III
  invariants moved here and are a pointer there. `server-level-tick`
  traded its twelve-lane conversation for the **guard flowchart** the
  notebook asked for, twenty-odd phases each labelled with the gate it
  sits behind, plus a four-lane sequence of the block-change broadcast
  that is the page's hook drawn; it opens by defining the three chunk
  ranges, so Part III no longer needs Part IV in front of it.
  `players-and-sessions` is a trace and a comparison at the seam session B
  found: two join diagrams in place of the corpus's widest one, then the
  four exits as a table with sections per point of difference (*what comes
  across when you die*, *why the Nether keeps your potion effects*,
  *where your llama goes when you log out*). `server-lifecycle` split:
  `starting-a-server` is the boot trace with the only diagram in the book
  that has the JVM main thread as a lane, and **`how-a-server-dies` is the
  part's closer** — three endings as columns, `/stop` traced in full, and
  the watchdog's self-deadlock drawn in four lanes.
  **Eighteen pass-2 errors found**, the largest crop since pass 2 itself,
  twelve of them re-derived by the session from the decompile: among them
  `ServerLevel.runBlockEvents` is freeze-gated (the old figure said
  otherwise by omission), a debug world drops the block-change broadcast,
  `ChunkHolder.broadcastChanges` sends light *before* blocks,
  `NaturalSpawner.createState` walks every entity rather than a chunk
  window, `MinecraftServer.scheduleExecutables` runs a late task inline
  instead of throwing, `PlayerList.respawn` is handed its removal reason
  rather than choosing it, `IntegratedServer` does set a simulation
  distance, the *Done* line is logged before RCON and the watchdog exist,
  and an ordinary autosave rewrites `level.dat` — which is what the new
  durability section rests on. All are in pass4.md with the fixes flagged
  for re-checking.
  Thirteen lane rows added plus two word lanes;
  `check_lanes --strict --pages src/systems/server` is clean, 103 diagrams
  render, 19,659 names resolve, and the old `server-lifecycle` URL
  redirects. Hand-offs in pass3.md §8 (the event loop's owner, the
  three-ranges opener session E must keep in step, two wrong link labels
  for sessions I and N), pass4.md and pass5.md.
  Process note: five pages drafted by parallel Opus agents against a shared
  brief and diffed by the session. **One agent reported a corrected
  ordering in its prose and then drew the old ordering in its own new
  diagram**; the session caught it against the decompile. A drafting
  report is not evidence about the figure — later sessions should read
  every redrawn diagram separately, and pass 4 has been told the same.
- **2026-09-02, session E — Part IV The world.** *Rulings, written before
  editing.* **Part IV is a conveyor with a vocabulary page in front of it and
  three lectures hanging off the side**, and the landing page draws exactly
  that: `chunk-anatomy` defines the thing, then four pages hand a chunk along
  a line — a ticket asks for it (`tickets-and-loading`), the pyramid builds
  it (`chunk-generation-pipeline`), the light engine finishes it
  (`lighting`), the region file forgets it (`chunk-storage`) — and
  `environment-attributes-and-timelines`, the two tick pages and the two
  index pages are about the world the conveyor delivers, not about the
  conveyor. **The part goes from nine pages to ten**, and both changes are
  the notebook's confirmed splits rather than R7's new-page allowance, which
  this session does not spend (Part IV has no coverage-queue entry).
  `block-ticks-and-fluids` splits at its own trace step 5 → 6 into
  **`scheduled-ticks`** and **`fluids`**; `game-events-and-poi` splits into
  **`game-events-and-vibrations`** and **`points-of-interest`**, the seam the
  pass-2 fact-check found by producing two reports with no shared class in
  them. `level-data-and-rules` moves to `src/reference/` (R5), which leaves
  Part IV with no page that says of itself "short, no trace". Four redirects
  (R8).
  **The ten pages, their shapes and their hooks.**
  **`chunk-anatomy`** takes the **vocabulary** shape: two figures of the data
  (the four shapes a chunk takes, and the containment from chunk down to bit
  storage) and a tour by object grounded in one small trace, one block
  written. Hook: a section holding two block states costs exactly what one
  holding sixteen costs, on disk as well as in memory — and the block that
  makes it seventeen re-encodes all 4,096 entries.
  **`tickets-and-loading`** is session A's policy pilot and is not rewritten;
  it is re-read against `server-level-tick`'s new three-ranges opener so the
  two agree.
  **`chunk-generation-pipeline`** takes the **pipeline** shape the notebook
  asked for, and **the pyramid is drawn** — twelve statuses, the radius each
  needs, the four that fork off the worldgen executor — instead of living in
  a markdown table; a section per stage; the ten-lane trace comes down to
  seven. Hook: asking for one chunk asks for 529, and eleven chunks of that
  ring will never become chunks you can stand on.
  **`lighting`** keeps the **trace** shape and gains the figure the notebook
  says it lacks: the four-stage batch (check nodes, decreases, increases,
  swap) as a pipeline flowchart beside the torch trace, which also comes down
  to seven lanes. Hook: there is no light thread and no light phase of the
  tick — the light engine runs because the server thread had nothing else to
  do.
  **`chunk-storage`** keeps the **trace** shape with a three-lane hand-off
  figure in front of it (the server thread copies, the worker encodes, the IO
  lane writes), and its eleven-lane diagram splits: the unload and the write
  are two pictures. Hook: almost every write of your world is one nobody
  asked for — a chunk you touched is written about every ten seconds by a
  background sweep, and the autosave is five minutes of wall clock whatever
  `/tick rate` says.
  **`scheduled-ticks`** is the **pipeline** shape: schedule, index, collect,
  drain, run, with a section per phase and a repeater as the grounding trace
  (the notebook's suggestion; it is also what Part V will link to). Hook:
  dedup is by type and position only, so a second, *sooner* tick for the same
  block is dropped — "rescheduling moves the tick" is folklore.
  **`fluids`** is the **trace** shape on the bucket, with
  `FlowingFluid.getNewLiquid`'s three branches drawn as a decision flowchart
  — the ordering pass 2 found wrong is exactly the thing a flowchart cannot
  fudge. Hook: water finds a hole four blocks away because every side runs
  its own depth-first search, and a side the water cannot even enter still
  votes on where the rest of it goes.
  **`game-events-and-vibrations`** is the **trace** shape (the footstep) with
  the filter cascade drawn — every test that drops a vibration, in order,
  which is the page's real subject and today is prose. Hook: a sensor always
  hears you one tick late by design, and the wool box only works if all six
  rays hit wool — but standing *on* the sensor skips the whole cascade,
  sneaking included.
  **`points-of-interest`** is the **trace** shape (the villager and the bed).
  Hook: the bed is claimed the moment a path to it exists, up to 48 blocks
  away, and the claim and the *occupied* flag are two facts that never speak
  to each other.
  **`environment-attributes-and-timelines`** is the best-shaped page in the
  part and keeps its mirrored server/client pair; it gains the third figure
  the notebook asked for — **the layer stack drawn as a stack** above the two
  sequence diagrams — and the frame every page now keeps (hook first, cast
  table, headings that say what they say). Hook: the night does not set the
  sky's colour, it multiplies whatever the biome produced — every timeline
  track carries a modifier argument, not a value, which is the one decision
  the whole system rests on.
  **`level-data-and-rules`** becomes Reference: the who-owns-what table is
  the page, the header stops promising a lecture, and Part IV's landing page
  points at it as the part's look-up.
  **Lanes**: the Part IV rows go into the key before drafting. Three
  collisions with existing rows are resolved by lengthening the later
  claimant, as the rule says — `LevelChunkTicks` cannot be `LCT`
  (`LoadingChunkTracker`, session A) and becomes `LCTs`; `PoiRecord` cannot
  be `PR` (`PackRepository`, session C) and becomes `PRec`; and
  `PalettedContainer` yields `PC` to `ProtoChunk` and becomes `PCon`. `VS` is
  claimed for `VibrationSystem`, and `EnvironmentAttributeSystem.ValueSampler`
  is recorded as `EVS` under the nested-class exception. `check_lanes.py
  --strict --pages src/systems/world` before shipping.
  *Done.* Part IV is ten pages in a conveyor, drawn on a new landing page
  the sidebar's Part IV opens on: `chunk-anatomy` defines the thing, four
  pages hand it along the line, and five are about the world the line
  delivers. `chunk-anatomy` is a vocabulary page with two figures — the four
  shapes a chunk takes and where each is made, and the containment from
  chunk down to the bit storage, which is the hook drawn — in place of a
  415-line field inventory. `chunk-generation-pipeline` **draws the
  pyramid** the notebook has asked for since session C: twelve statuses,
  the radius each sweeps, and which of them leave the worldgen executor,
  with its ten-lane conversation cut to seven. `lighting` gained the
  four-stage batch as a pipeline figure beside the torch trace, and now
  says plainly that the light engine runs because the server thread went
  idle. `chunk-storage`'s eleven-lane monster became three figures — the
  three-thread hand-off, the unload, and `RegionFile.write`'s sector dance,
  whose in-file and sidecar branches commit in opposite orders. Both
  confirmed splits were executed: `block-ticks-and-fluids` at its own trace
  step 5 → 6 into **`scheduled-ticks`** (a pipeline, traced on a repeater,
  which is what Part V will link to) and **`fluids`** (the bucket, with
  `FlowingFluid.getNewLiquid`'s three branches drawn as a decision
  flowchart, because the ordering is what pass 2 got wrong);
  `game-events-and-poi` into **`game-events-and-vibrations`** (the filter
  cascade drawn, which the old page carried as a numbered list with no
  figure at all) and **`points-of-interest`** (the villager and the bed,
  with the life of one ticket as a state diagram).
  `environment-attributes-and-timelines` kept its matched server/client
  pair and gained the layer stack drawn as a stack.
  `level-data-and-rules` is Reference.
  **Twelve pass-2 errors found**, seven of them re-derived by the session
  from the decompile. The largest is `lighting`'s: the light packet goes to
  **border players only** — `ChunkHolder.broadcastChanges` passes
  *borderOnly* true for light and false for blocks — where the old page
  said "with border players included", exactly inverting it. Two more
  overturned claims this session's own rulings had repeated: POI records
  appear **synchronously** on the server thread (`MinecraftServer.scheduleExecutables`
  is false outside a queued task, so `BlockableEventLoop.execute` runs the
  body inline), and the vetoing side in `FlowingFluid.getSpread` is one the
  water may enter but not *replace*, and it clears the collected winners as
  well as lowering the minimum. Also: the scheduled-tick drain **does** run
  during `/tick step`; biomes have no four-bit linear palette rung; the
  nether has no day timeline at all; a positional attribute no layer makes
  positional is memoised like any other; and a vibration arrives
  ⌊distance⌋ − 1 ticks after selection, not ⌊distance⌋.
  Two release paths for a villager's bed that no page had.
  **One tool bug**: `check_lanes.py --pages src/systems/world` also matched
  `src/systems/worldgen`, so it was reporting nine Part XII pages as Part IV
  failures — a plain `startswith` on paths, fixed with a separator-aware
  check that session M would otherwise have hit.
  Thirty-three lane rows added and twenty-nine speculative ones pruned
  before shipping, on the principle that a key row is a claim on a lane and
  claiming one a page does not use pre-empts a session that has not run;
  `check_lanes --strict --pages src/systems/world` is clean, 117 diagrams
  render, 19,215 names resolve, and four old URLs redirect. Twenty pages
  across nine other parts were re-pointed at the right half of each split.
  Hand-offs in pass3.md §8 (the tool bug, the lane ledger, the four
  collisions later sessions must lengthen, and what Parts V, VI and O
  inherit), pass4.md and pass5.md.
  Process note: nine pages drafted by parallel Opus agents against a shared
  brief, each report diffed by the session. **Three agents overruled the
  session's own rulings with evidence** — the fluid hook's wording, the POI
  deferral, and the brief's "four steps leave the worldgen executor" (it is
  five) — which is the protocol working as intended; a ruling written
  before the pages are open is a hypothesis. The session read every redrawn
  diagram against the source separately from its page's prose, per session
  D's lesson, and that caught four figure-level problems the reports did not
  mention: a `getNewLiquid` flowchart that implied `FlowingFluid.spread` is
  not called on an empty result, a pyramid caption asserting radius 11 for
  *EMPTY* without saying the first sweep is the loading pyramid's 1, a
  containment figure showing the block-state palette ladder on a node shared
  with biomes, and a lane carrying a parenthetical the linter cannot read.
- **2026-09-02, session F — Part V Blocks.** *Rulings, written before
  editing.* **Part V is a hub and six spokes, and the hub's second half is
  the part's real subject.** `blocks-and-states` is the vocabulary page every
  other page reaches back into, and the thing they reach for is not the state
  table but **the tail of a write**: what `LevelChunk.setBlockState` and
  `Level.setBlock` do after the section has been written. R6 puts the *two
  update channels* flowchart there and this session draws it as one figure
  spanning both methods, because the split runs through the middle of them —
  `BlockEntity.preRemoveSideEffects`,
  `BlockBehaviour.BlockStateBase.affectNeighborsAfterRemoval` and
  `BlockBehaviour.BlockStateBase.onPlace` are inside the **chunk** write
  (session E's correction), while the broadcast, the neighbour fan-out and the
  three shape passes are in `Level.setBlock`'s tail. Every other page in the
  part links to that one figure instead of restating it, which is the fix for
  the notebook's finding that three of five pages had the distinction subtly
  wrong.
  **The part goes from five pages to seven**, all of it the schedule's own
  work: `redstone` splits three ways, and R7's new-page allowance is **not
  spent** — Part V has no entry in the coverage queue, which therefore still
  stands at fifteen items. `blocks-and-states` is **not** split, overruling
  nothing (pass 2 left it as pass 3's call): its two halves are the state
  table and the write, and the write is what the other six pages need, so
  cutting between them would put the part's load-bearing figure on a page
  nobody is sent to. One redirect (R8): the old `redstone` URL goes to
  `signal-and-dust`.
  **The seven pages, their shapes and their hooks.**
  **`blocks-and-states`** takes the **vocabulary** shape with two figures — a
  containment figure of the objects (`Block`, `BlockBehaviour`,
  `StateDefinition`, `Property`, `StateHolder`,
  `BlockBehaviour.BlockStateBase`, `BlockState`) and the two-channel flowchart
  of a write — and the stair placement kept as the grounding trace, cut to
  the state *choice* and the write, since the click that led to it is the
  next page's. Hook: every state the game will ever have is built before any
  world exists, and the world stores an index into that table, so setting a
  property allocates nothing and a client that disagrees with the server
  about a block's properties does not throw — it sees air.
  **`block-interaction`** and **`block-breaking`** are **one lecture in two
  halves** (R6): both keep the **trace** shape and both open with the *same*
  preamble stating the prediction ledger's contract — the ack is a receipt
  for a number and not a verdict, and correctness comes from the ordering —
  with the mechanism left to `prediction-and-acks`. Neither page re-derives
  the ledger again. `block-interaction`'s hook: opening a door fires no
  neighbour update at all, and the other half follows anyway, through the
  one channel the client also runs. `block-breaking`'s hook is the hook bank's
  block that comes back and vanishes again: releasing the button does not
  cancel a break, and nothing the client does between the two can stop it.
  **`block-entities`** keeps the **trace** shape and the furnace, reshaped to
  the frame; the notebook calls it the best-shaped page in the part and this
  session does not go looking for a reason to change it. Hook: a furnace
  tells nobody anything — the fire is a block state, the arrow is four ints
  from a menu, and both are a tick late because block entities tick last.
  **`signal-and-dust`** takes the **trace** shape (lever, two dust) but the
  notebook's wrong-shape finding is honoured in the figure: the cascade is
  drawn as a **flowchart of one wire's recomputation and its hand-issued
  fan-out**, not as a conversation, and the experimental evaluator is the
  coda it belongs to rather than a page of its own. Hook: a line of dust
  turning off counts down through every intermediate value because each wire
  recomputes from scratch and then hand-notifies forty-two positions — and
  the game ships a second implementation, behind a feature flag, that does
  not. It owns the third direction order, `SignalGetter.DIRECTIONS`, and the
  weak/strong distinction.
  **`pistons-and-block-events`** keeps its **lanes** — the notebook says this
  half is genuinely sequential — and owns the block-event queue, which is the
  part's only *deferral* mechanism and is what makes the piston a tick late.
  Hook: the moving blocks are never sent. The client re-runs the push itself
  from one event packet, the placeholders are written with the tell-clients
  bit deliberately clear, and no correction ever follows.
  **`diodes-and-observers`** takes the **comparison** shape — repeater,
  comparator and observer as three columns of *what it reads*, *how it books
  its turn*, *how it outputs* — because that is exactly how they differ and
  the old section read as three unrelated paragraphs. Hook: the observer, the
  block whose whole job is noticing that something changed, is not on the
  channel that carries change notifications, and neither is the repeater's
  lock — both listen on the shape channel.
  **What Part V no longer teaches.** `scheduled-ticks` (Part IV) owns the
  appointment book, the priorities and the repeater's pulse extension;
  `fluids` owns `LiquidBlock` and waterlogging; `prediction-and-acks` owns the
  ledger; `game-events-and-vibrations` owns `GameEvent` posting;
  `chunk-anatomy` owns the section and palette. The diodes page links to the
  first for delay and priority rather than restating either.
  **Lanes**: the Part V rows go into the key after drafting, from the
  diagrams that actually exist, not before (session E's rule that a key row
  is a claim). Four collisions with existing rows are resolved by lengthening
  the later claimant: `LeverBlock` cannot be `LB` (`LiquidBlock`, session E)
  and becomes `LevB`; `BlockItem` cannot be `BI` (`BucketItem`, session E) and
  becomes `BItem`; `BlockPlaceContext` cannot be `PC` (`ProtoChunk`, session
  E) and becomes `BPC`; `PistonStructureResolver` cannot be `PR`
  (`PackRepository`, session C) and becomes `PSR`.
  `check_lanes.py --strict --pages src/systems/blocks` before shipping.
  *Done.* Part V is seven pages in a hub and six spokes, drawn on a new
  landing page the sidebar's Part V opens on. **The hub's second half is the
  part's real payload**: `blocks-and-states` now draws the tail of a write as
  one flowchart spanning `LevelChunk.setBlockState` and `Level.setBlock`,
  with every server-only step and its flag gate marked, and the other six
  pages link to that anchor instead of restating the shape-versus-neighbour
  distinction — the fix for the notebook's finding that three of five Part V
  pages had it subtly wrong. `block-interaction` and `block-breaking` are one
  lecture in two halves, opening with an identical four-sentence statement of
  the prediction contract and leaving the machinery to
  `prediction-and-acks`; the landing page rules that Part V is watched
  *before* it, resolving the circular dependency section 5 flagged.
  `block-entities` kept the furnace and gained the tick bars it needed.
  **`redstone` split three ways** — `signal-and-dust` (the cascade drawn as a
  flowchart rather than a conversation, with the experimental evaluator as
  its coda), `pistons-and-block-events` (block events as a general mechanism,
  then the piston) and `diodes-and-observers` (the repeater, comparator and
  observer as a comparison table of what each reads, how each books its turn
  and how each outputs) — and the old URL redirects to the first. R7's
  new-page allowance was not spent, so the coverage queue still stands at
  fifteen.

  **The session was interrupted and lost five drafting agents**, four pages
  in. The four drafted pages were complete on disk, but **two of the four
  agent reports did not survive**, which is the part that matters: a page
  whose claim-diff never arrived cannot be said to have been diffed.
  `pass4.md` records the four classes of evidence explicitly and tells pass 4
  to treat `blocks-and-states` and `block-entities` as unaudited and to diff
  them against their pass-2 versions in git. The three redstone pages were
  then written by the session itself from the decompile, method by method,
  with every diagram read separately from its prose.

  **Nine corrections re-derived by the session.** The largest is that
  **block events are not "a tick late"** — the old `redstone` diagram said so,
  but packets are drained before `MinecraftServer.tickServer` and the
  *blockEvents* phase precedes *entities*, so an event queued by a packet
  handler or a scheduled tick drains in the same tick, and only the entity
  and block-entity phases push one over the boundary. `reference/glossary.md`
  already had it right, so the corpus had been contradicting itself.
  Next: **`RepeaterBlock.LOCKED` does not survive on a client** and the old
  page's stated reason for saying it did was backwards —
  `RepeaterBlock.updateShape` and `ObserverBlock.startSignal` both refuse to
  run client-side, and a client keeps no appointment book to fire into.
  Also: `blocks-and-states`' new hook overclaimed *you get air* and was
  narrowed, because `ClientboundBlockUpdatePacket.STREAM_CODEC` throws on an
  unknown id where `Block.stateById` does not; dust powers the block **below**
  it and never the one above; `LeverBlock.pull` is handed a null player so
  the clicker hears the server's sound, unlike the door; a diode's `FACING`
  points at its **input**; `PistonBaseBlock.checkIfExtend` resolves as a dry
  run before it queues anything; `ComparatorBlock.checkTickOnNeighbor` books
  on a condition the repeater has no analogue of; and `SignalGetter.getSignal`
  is a maximum of weak and strong power rather than a choice between them.
  The one agent report the session did fully re-derive,
  `block-interaction`'s, found six more, including that a player mid-use has
  their queued right-clicks **discarded** rather than delivered.

  Thirteen lane rows added and four collisions lengthened;
  `check_lanes --strict --pages src/systems/blocks` is clean, **122 diagrams
  render**, 18,194 names resolve, the class index is regenerated, the old
  `redstone` URL redirects, and four cross-part links plus three glossary
  entries were re-pointed at the right half of the split. Seven pages at
  243–388 lines — the first part to land inside the length brief rather than
  over it. Hand-offs in pass3.md (the shared anchor six pages depend on, the
  split seams other parts link across, two Reference candidates for session O,
  the lane ledger), pass4.md and pass5.md.
- **2026-09-03, session G — Part VI Entities.** *Rulings, written before
  editing.* **Part VI is a ladder with a missing rung, and the rung goes in
  second.** The notebook's order survives — object, world, the channels that
  describe it, what it does, why, how it stops — and R6's authority page is
  inserted directly after `entity-anatomy`, where it is a prerequisite for
  everything above it and for Parts VIII, IX and X. The landing page draws
  the ladder and says so.
  **The part goes from seven pages to nine.** One page is R6's
  (`authority`); one is the notebook's confirmed split of
  `ai-goals-and-brains`. R7's new-page allowance is **not** spent as a page:
  Part VI's single coverage-queue entry, the non-living `Entity.hurtServer`
  overrides, is discharged as **a named closing section in
  `damage-and-death` plus a Reference table** — the queue itself offered
  that as one of its three options, and a twenty-one-row table of "what
  this class does when you hit it" is the definition of something a viewer
  pauses on (R5). Two catalogues move to Reference **generated**, as the
  schedule asks: the 43 entity-data serializers with their wire ids and the
  40 attributes with their defaults, ranges and syncable flags —
  `gen_reference.py` gains two views, so both are re-derived on the next
  version rather than re-checked by hand.
  **`ai-goals-and-brains` splits in two, not three**, which is this
  session's answer to the schedule's *ruled*. The page's argument is that
  two decision systems coexist and are identical below the waterline;
  cutting between goals and brains would destroy the one comparison the
  page exists to make. The seam the notebook actually found is the
  waterline itself — `MoveControl.setWantedPosition` — so the cut is there:
  **`ai-goals-and-brains`** keeps goals, brains, activities, the villager
  day and the zombie (and its URL, so no redirect), and **`pathfinding`** is
  new and takes navigation, the A\* and its budget, the node evaluator and
  path types, the region snapshot, stuck detection and the four controls.
  **`entity-anatomy` is not split** (pass 2 confirmed the seam and left the
  call here): it is the part's map page and its two halves are what an
  entity *is* and what the tree *looks like*, which is one lecture. But its
  hand-drawn mermaid class tree goes, replaced by the atlas's **generated**
  `tree-Entity.svg` (R4: a figure has to be regenerable, and session B
  already draws this one with real counts).
  **The nine pages, their shapes and their hooks.**
  **`entity-anatomy`** takes the **vocabulary** shape: a containment figure
  of what an entity is made of, the generated tree, and the registry-to-live-object
  trace kept as the grounding. Hook: the entity registry's default is a
  pig, and that default reaches the network and not your save file — a bad
  id on the wire is a pig, a bad id in a region file is a *Skipping Entity*
  line and a hole where the entity was.
  **`authority`** is new (R6) and takes the **comparison** shape: a mob and
  a player, each taking one step, on each side, as the columns; the four
  predicates as the rows; a section per point of difference. Hook: the
  client runs no physics at all for the zombie chasing you, and it runs
  full physics for the player standing beside you — while the server runs
  that player's physics too and throws the answer away. Parts VIII, IX and
  X link here instead of re-teaching the matrix, and
  `movement-and-collision` loses its opening section to it.
  **`entity-lifecycle`** keeps the **trace** shape (a zombie's life) and
  gains the two figures the notebook asked for: the spawn attempt as a
  **filter cascade** — every test that rejects, in order, with the
  rejections drawn — and `Visibility` as a small state diagram. Hook: the
  spawner rolls **one** height per category per chunk per tick, uniform
  from the world bottom to the surface, so every category gets its own
  horizontal slice and a taller world thins the surface out.
  **`synched-entity-data`** keeps the **trace** shape (the sheep) with the
  43-serializer catalogue gone to Reference and the sheep's nineteen slots
  kept, because that table *is* the lecture. Hook: the id of the sheep's
  wool byte is decided by the order the JVM runs static initialisers in,
  and the packet stops at 254 because 255 means stop.
  **`attributes`** takes the **vocabulary** shape — the five objects, the
  three-pass arithmetic, the sync gate — with the Strength II trace as its
  grounding and the forty-attribute catalogue gone to Reference. Hook:
  Strength II sends no packet at all, because eight of the forty attributes
  are not syncable and attack damage is one of them.
  **`movement-and-collision`** keeps the **trace** shape (the falling
  zombie) and hands its authority section to the new page. Hook: the mover
  answers *what did I walk through* after the fact, by replaying the tick's
  movement in the same axis order the collision used — which is why fire
  and water touched in the same step always end in the extinguish.
  **`ai-goals-and-brains`** takes the **comparison** shape: the goal
  selector and the brain as two columns of *what holds the state*, *what
  decides*, *what arbitrates* and *what persists*, with the villager day
  as the brain's trace and the zombie as the goal selector's. Hook:
  schedules are gone — a villager goes to bed because it asks the world
  what time it is *where it is standing*.
  **`pathfinding`** is new and takes the **pipeline** shape: walk target →
  navigation → region snapshot → node evaluator → A\* → path → move
  control, a section per stage. Hook: giving up is machinery — every node
  carries a timeout derived from its distance and the mob's speed, and
  three overruns abandon the path, so the mob you watch walk into a wall
  and then wander off is running a scheduled surrender.
  **`damage-and-death`** keeps the **trace** shape (the arrow) and gains
  the closing section it has been missing: **the five families of
  non-living damage**, with the per-class table in Reference. Hook stays
  the i-frame one — a hit inside the red flash that *does* land is
  invisible: health drops and nothing else happens.
  **Reference.** `reference/entity-data-serializers.md` and
  `reference/attributes.md` are generated by two new `gen_reference.py`
  views; `reference/non-living-damage.md` is hand-kept and re-swept in pass
  4. All three are in `SUMMARY.md` and the reference README.
  **Lanes** go into the key *after* drafting, from the diagrams that exist
  (session E's rule); collisions are resolved by lengthening the later
  claimant. `check_lanes.py --strict --pages src/systems/entities` before
  shipping.
  *Done.* Part VI is nine pages in a ladder, drawn on a new landing page the
  sidebar's Part VI opens on. **The missing rung went in second**:
  `authority` is a comparison of three cases — a tracked mob, a player and a
  ridden boat, each read on both sides — with the four predicates as its
  rows, the six gates inside `Entity.move` and `LivingEntity.aiStep` that
  read them, and the vehicle case nothing in the corpus had: both base
  client-authority predicates delegate to the *controlling passenger*, which
  is the whole vehicle model, and `ClientboundMoveVehiclePacket` turns out to
  be a rejection notice rather than a routine update. Sessions I, J and K now
  link there instead of re-teaching the matrix, and
  `movement-and-collision` is already cut to three sentences and a link.
  **`ai-goals-and-brains` split in two, not three** — the ruling the schedule
  asked for. The page's argument is that two decision systems coexist and are
  identical below the waterline, so cutting between goals and brains would
  have destroyed the one comparison it exists to make; the cut is at the
  waterline itself, `MoveControl.setWantedPosition`. Goals and brains keep the
  URL (no redirect) and became a **comparison** with seven rows of
  difference; **`pathfinding`** is new and took navigation, the A\* and its
  budget, the node evaluator, the region snapshot, stuck detection and the
  four controls. `entity-lifecycle` got the **filter cascade** the notebook
  has asked for since session E — every rejection in source order, with the
  only-now-is-the-mob-constructed boundary drawn — plus `Visibility` as a
  state diagram; `entity-anatomy` traded its hand-drawn class tree for the
  atlas's generated `tree-Entity.svg`, the first system page to use session
  B's figure pipeline. Both reference catalogues moved out **generated**:
  `gen_reference.py` grew `entity-data-serializers` (43 rows, registration
  order, which is the wire id) and `attributes` (40 rows with range, syncable
  and sentiment). R7's allowance was **not** spent as a page: Part VI's one
  coverage-queue entry, the non-living `Entity.hurtServer` overrides, became
  a five-family closing section in `damage-and-death` plus the hand-kept
  `reference/non-living-damage.md` — and the count was wrong twice over, at
  21 classes rather than "about thirty", with `Entity.hurtServer` **abstract**
  so there is no default behaviour anywhere in the tree. The queue drops to
  fourteen.
  **Twenty-two pass-2 errors found**, eight of them re-derived by the session
  itself. The largest is that **only `Villager` has a schedule**:
  `Brain.setSchedule` has two call sites, both in `Villager`, and the other
  nineteen brain mobs use `Brain.setActiveActivityToFirstValid` — the old
  page called that the exception used by three mobs. Then: the spawner's
  biome energy budget runs *before* construction, not after;
  `INSCRIBED_SQUARE_SPAWN_DISTANCE_CHUNK` is 5, not 8, and feeds only
  `DistanceManager.hasPlayersNearby`'s fast-yes arm;
  `EntityTypes.ITEM_FRAME`'s update interval is `Integer.MAX_VALUE`, which is
  *why* `ServerEntity` has an item-frame bypass — and that bypass is the only
  one, where the old page named two; the *chunkSource* phase is mid-tick, not
  near its start; `LivingEntity.shouldTravelInFluid` reads the cached flags,
  not the live fluid state; `Attributes.DEFAULT_ATTACK_SPEED` has no callers
  at all; `EntitySpawnRequest.ignoreChecks` is never true;
  `entity-anatomy`'s subpackage table summed to 639 of a stated 716; and
  — the one that would have embarrassed the new page most — the old
  `damage-and-death` opened its list of classes that "never touch armour,
  i-frames or the combat tracker" with `ArmorStand`, which is a
  `LivingEntity`.
  **One tool bug**: `gen_reference.py`'s *gamerules* blurb still linked to
  the pre-session-E path for `level-data-and-rules`, so **regenerating the
  reference tier reintroduced a broken link somebody had fixed by hand** —
  found by a link sweep, fixed in the tool.
  Twenty-two lane rows added and five later claimants lengthened (`MoveC`,
  `SumC`, `AttrM`, `AttrI`, `EffC`); `check_lanes --strict --pages
  src/systems/entities` is clean, **135 diagrams render**, 18,015 names
  resolve, and every relative link in `src/` resolves. Nine pages at 118–420
  lines, two of them over the length brief and logged in pass5.md. Three of the six identical *Questions players ask* headings were
  varied in-session, which is the "second uniformity" risk showing up for the
  first time. Hand-offs in pass3.md §8 (the authority owner and its four
  dependants, the AI seam, the `SE` lane session K must lengthen, the
  Nether-fortress material that now lives nowhere), pass4.md and pass5.md.
  Process note: seven pages drafted by parallel Opus agents against a shared
  brief, every report diffed by the session. `damage-and-death`'s report ran
  long, and rather than wait the session audited that page against the
  decompile itself — so when the report did arrive there were **two
  independent audits of one page, and they agreed**, which is a cheap check
  worth repeating on the page a part cares most about. Three agents overruled
  the session's own rulings with evidence — the spawner's budget ordering, the
  claim in the brief that `ServerEntity.handleMinecartPosRot` bypasses the
  send gate, and the brief's own roster of non-living damage classes, whose
  first entry — `ArmorStand` — is a `LivingEntity` — which is the protocol
  working: a ruling written before the pages are open is a hypothesis.
- **2026-09-03, session H — Part VII Items and inventories.** *Rulings,
  written before editing.* **Part VII is two tiers, and the part currently
  pretends it is a chain.** Tier one is the vocabulary — what a stack *is*,
  what happens when you use one, and how two machines agree about a set of
  them — and every page of it is a hard prerequisite for everything above.
  Tier two is three data-driven engines that produce or decorate stacks —
  recipes, enchantments, loot — which depend on tier one completely and on
  each other not at all. The landing page draws the two tiers rather than a
  list, and says that the three engines may be watched in any order.
  **The part goes from five pages to eight**, all three additions being
  splits the notebook confirmed. `items-and-stacks` sheds the use pipeline
  to **`using-an-item`**, which is also where R7's allowance is spent: the
  coverage queue's *drawing a bow* is not a new subject but the **second
  half** of that page, because the release branch and the completion branch
  are one guard read two ways. `loot-tables` sheds its front to
  **`contexts-and-predicates`**, so that Part XIII and the advancement
  material depend on a page whose title describes what they need — the
  notebook's own preferred option, because the dependants are in another
  part. `enchantments` sheds its fourth section to **`enchanting`**, the
  acquisition lecture, which is a menus story and belongs beside the anvil
  and the grindstone rather than behind a hook table. No page changes URL,
  so no redirects.
  **The eight pages, their shapes and their hooks.**
  **`items-and-stacks`** takes the **vocabulary** shape: a containment
  figure of what a stack is made of, a tour by object, and one small trace
  — a pickaxe losing its last point of durability — as the grounding. Hook:
  an `Item` holds almost no data and an `ItemStack` holds a *diff*, against
  a prototype map that does not exist until the first data-pack load.
  **`using-an-item`** is new and takes the **comparison** shape: the meal
  and the bow as two columns over one guard. Hook: the client's countdown
  does not stop at zero, the meal ends because one byte arrives, and the
  bow never ends that way at all — `ItemStack.useOnRelease` is the third
  term of the completion guard, so a bow is finished by the packet the
  eating path treats as an abandonment.
  **`containers-and-menus`** keeps the **trace** shape (the shift-click)
  and gains the resync ladder as a **flowchart**, because the page's
  argument is a decision the server makes about the client's claim. Hook
  stays: agreement is silence — one packet up and zero down, because the
  server adopted the client's *belief object*, never its data, as the new
  baseline. Not split: the model and the protocol are one lecture, and the
  seam the notebook found is presentational.
  **`recipes`** keeps the **trace** shape (eight planks) and gains a
  figure of the load and its four derived indexes. Hook stays: no recipe
  ever crosses the wire, and what the client is denied is the *identity*,
  not the contents.
  **`enchantments`** takes the **pattern** shape — one idea (a named
  modifier is a map of effect components other systems ask about) with the
  hooks as its instance table and Fire Aspect as the traced instance. The
  thirty-odd-row `EnchantmentHelper` table goes to Reference **generated**
  (R5), because "which class calls which hook" is a question the decompile
  can answer on every version.
  **`enchanting`** is new and takes the **comparison** shape: the table,
  the anvil, the grindstone, the providers and `/enchant` as columns over
  the same questions — what it costs, what it may add, what it checks.
  Hook: the enchanting seed is per player, saved, sent to the client, and
  re-rolled by nothing but the table itself. It absorbs the three
  enchanting facts pass-5 recorded as homeless.
  **`contexts-and-predicates`** is new and takes the **vocabulary** shape:
  the five objects (`ContextKey`, `ContextKeySet`, `ContextMap`,
  `LootParams`, `LootContext`), the twenty-six sets as a Reference table
  **generated** from the decompile, and one small trace —
  `/execute if predicate` — as the grounding. Hook: five of the
  twenty-six sets have no loot caller at all, and the enforcement point is
  the *caller's* declared set, never the table's.
  **`loot-tables`** keeps the **trace** shape (the dungeon chest) and
  becomes the worked example of the page above it, with the draw drawn as
  a flowchart. Hook stays: the chest is empty on disk, the key is cleared
  *before* the roll, and the first toucher — which need not be a player —
  commits it with no luck, permanently.
  **Two coverage-queue entries are answered.** *Drawing a bow* is
  discharged inside `using-an-item`. *How an item picks its model* is
  **ruled to Part XI** (session L's call to make it a page or a section of
  `models-and-atlases`): the trace starts at an `ItemStack` but everything
  it touches — `ItemModelResolver`, the baked models, the atlas, the
  render state — is Part XI's, and Part VII owns the stack, not its
  appearance. Part VII links forward instead.
  **Lanes** go into the key after drafting, from the diagrams that exist;
  Part VII is the later claimant everywhere, so `ItemStack` is `IStack`
  (`IS` is `IntegratedServer`), the menus take word-plus-initial forms
  (`ChestM`, `CraftM`, `InvM`, `AnvilM`) because `CM` is `ChunkMap`, and
  `RemoteSlot`, `ResultSlot`, `LootPool` and `RandomizableContainer`
  lengthen off `RS` (`RenderSystem`), `LP` (`LocalPlayer`) and `RC`
  (`ReloadCommand`). `check_lanes.py --strict --pages src/systems/items`
  before shipping.
  *Done.* Part VII is eight pages in two tiers, drawn on a new landing page
  the sidebar's Part VII opens on. **The three splits went in as ruled, and
  each of the three new pages found its own reason to exist.**
  **`using-an-item`** took the use pipeline out of `items-and-stacks` and
  put the bow opposite the meal — and writing the bow settled the question
  the coverage queue had been carrying: the release branch is not chosen by
  `ItemStack.useOnRelease` at all. **`CrossbowItem` is its only override in
  the tree**, and the bow and trident are release-ended only because their
  duration is 72000 and their `Item.releaseUsing` does the work. What
  `useOnRelease` actually buys is one *extra* tick — `LivingEntity.releaseUsingItem`
  re-enters `LivingEntity.updatingUsingItem` when it is true, so a crossbow
  gets a final `CrossbowItem.onUseTick` to latch its charge. The old page
  named three items for a predicate that has one. **`contexts-and-predicates`**
  took the front off `loot-tables` and, counting the call sites from
  scratch, overruled this session's own hook: not five sets without a loot
  caller but **twelve of the twenty-six that never roll a `LootTable`** —
  the old sentence had listed six under a count of five and included a set
  that does have one. **`enchanting`** took acquisition out of
  `enchantments` and turned four paragraphs into the part's densest page:
  the table charges the *slot index plus one* rather than the displayed
  cost, the clue is a genuine member of the list you will receive, and every
  one of the five paths ends on the same
  `ItemStack.enchant` → `EnchantmentHelper.updateEnchantments` tail.
  **`containers-and-menus` was not split**, against the notebook's offered
  seam: the model and the protocol are one lecture. It gained the resync
  ladder as a flowchart, which is where four of its six outcomes turn out
  to be *nothing sent*.
  **Two Reference catalogues, both generated.** `gen_reference.py` gained
  `enchantment-hooks` — every `EnchantmentHelper` entry point with the
  classes that call it, scanned across the whole tree, **50 entry points, 47
  called from outside the class** — and `loot-context-params`, the
  twenty-six sets with their required and optional keys. The hook table was
  the largest artefact in the old Part VII and is now re-derivable on every
  version; the page keeps a seven-row *families* table and the five
  annotated highlights.
  **Nine pass-2 errors found**, one of them audited twice. Besides the three
  above: `Item.Properties.repairable` is **eager**, not delayed, so the old
  page's example of a tag-dependent delayed component was wrong;
  `Inventory.tick` is reached from `Player.aiStep`, not `Player.tick`;
  `DecoratedPotRecipe` is a `CustomRecipe`, making **nine** of fourteen
  crafting serializers special rather than eight, and eleven `SlotDisplay`
  variants exist rather than eight; **twenty-four** of the thirty-one
  enchantment effect components carry the decode-time validator, not ten;
  `/enchant` does *not* skip the supported-items and level rules — it is
  **stricter** about levels than the anvil, which clamps where the command
  refuses; and Fortune and Looting do not read
  `LootContextParams.ENCHANTMENT_LEVEL` at all — they read
  `LootContextParams.TOOL` and `LootContextParams.ATTACKING_ENTITY`, and
  `ENCHANTMENT_LEVEL` is written only by the five enchantment effect
  contexts. `loot-tables`' trace also had two orderings wrong: a single
  chest's menu provider **is** the block entity, and
  `ClientboundOpenScreenPacket` precedes `ServerPlayer.initMenu`.
  **The `useOnRelease` correction has two independent audits**: the session
  read the release path in the decompile while the agents were drafting, and
  the agent's report, arriving last, agreed line for line. That is session
  G's cheap check repeated, and it worked the same way.
  R7's allowance was spent on `using-an-item`, so the queue drops to
  thirteen; *how an item picks its model* was **ruled to Part XI** rather
  than written, with both Part VII references pointing forward at
  `models-and-atlases` for session L to land.
  Twenty-one lane rows added and fourteen later claimants lengthened, so
  Part VII takes no single-letter lane at all —
  `check_lanes --strict --pages src/systems/items` is clean, **148 diagrams
  render**, 18,201 names resolve, every relative link in `src/` resolves,
  and the class index is regenerated. Eight pages at 318–391 lines, all over
  the length brief and logged in pass5.md with the names that left them.
  Hand-offs in pass3.md §8 (the two-tier claim, `contexts-and-predicates` as
  Part XIII's dependency, the item-model ruling for session L, what session
  I should read first), pass4.md and pass5.md.
  Process note: eight pages drafted by parallel Opus agents against one
  shared brief, every report diffed by the session before acceptance. Three
  agents overruled the session's rulings with evidence — the twelve-sets
  count, the `useOnRelease` roster and `/enchant`'s real gates — which is
  the protocol working for the second session running. The one thing to do
  differently: eight concurrent agents each ran `mdbook build`, and they
  raced each other's output directory; one agent hit a spurious `ENOENT` and
  had to re-run with `--no-build`. A future session should tell agents to
  verify names only and leave the build to the session.
- **2026-09-03, session I — Part VIII The player.** *Rulings, written before
  editing.* **Part VIII is a trunk and four branches**, not a chain: two
  pages say what a player is and when it runs, and everything else is one
  thing a player *does*. So the part grows from four pages to seven.
  **`player-anatomy` splits** as the pass-2 table and the notebook both
  asked: the vocabulary half keeps the URL, and the two-phase tick —
  record, simulate, snap back — becomes **`the-two-phase-tick`**, a trace
  page, because it is the one thing on the old page nobody would guess.
  **`hunger-xp-and-effects` splits** at the seam the notebook named: status
  effects take **`status-effects`** (own registry, the hidden-effect stack,
  two synched values, the client blend), and the hunger and experience
  halves stay together in **`hunger-and-experience`** — a rename, so the old
  URL is redirected. **The spear gets its own lecture** (`the-spear`),
  discharging the coverage-queue entry: two data components, two entry
  points, two implementations of `LivingEntity.stabAttack`, a mob AI that
  uses it and a first-person animation that reads a combat field — it is
  far more than the two invariants it was, and it is the 26.2 combat change
  a viewer will most want explained. `the-sword-swing` keeps the ordinary
  path and hands both spear paths forward. **`the-sword-swing`'s figure
  becomes a flow over one number** (base damage in, total damage out) as the
  notebook asked, with the sequence kept only for the round trip.
  **The authority matrix leaves Part VIII entirely**: session G gave it a
  page, so `input-to-movement`'s four-method table and `player-anatomy`'s
  authority section are cut to a link, the way `movement-and-collision` was.
  *Done.* **Part VIII is seven pages, up from four**, with a landing page the
  sidebar's Part VIII now opens on. Both splits were free in the sense that
  matters: the material was already written, inside a page doing something
  else, and taking it out put both hosts inside the length brief.
  **`the-two-phase-tick`** took the *when it runs* half and the
  record–simulate–snap-back bracket out of `player-anatomy`, which is the one
  thing on that page nobody would guess and was buried under a class ladder;
  **`status-effects`** took the third of `hunger-xp-and-effects` that shared
  nothing with the other two but a sentence, leaving
  **`hunger-and-experience`** — a rename, so pass 3's first content-page
  redirect. **`the-spear` was written from the decompile**, the session's one
  piece of new research and the only page here pass 2 has never seen: two data
  components (`PiercingWeapon`, `KineticWeapon`) on one item, two entry points
  (a `ServerboundPlayerActionPacket.Action.STAB` carrying **no target id**,
  and item *use* with a 72000-tick duration), one shared filter, and two
  implementations of `stabAttack`. Writing it found the hook the coverage
  queue could not: **`Player.stabAttack` applies the two cooldown curves only
  when the player is not currently using an item in that slot**, so a stab is
  charged like a sword swing and a charging spear ignores the attack cooldown
  entirely. Also worth the trip: `KineticWeapon.forwardMovement` is a combat
  component field read only by the first-person animation, and the non-player
  action factor of 0.2 *lowers* the speed thresholds, so a zombie needs a
  fifth of the closing speed a player does.
  **One pass-2 error found while redrawing.** `the-sword-swing`'s numbered
  damage list gave the crit gate as `Player.canCriticalAttack`; it is
  `fullStrengthAttack && canCriticalAttack`, so the 0.9 scale is part of the
  crit condition. The page's new figure — the damage as a **flow over one
  number**, as the notebook asked — is what exposed it: drawing an ordering
  forces you to say where each factor enters, and the old prose had not.
  **The authority matrix is gone from Part VIII.** Session G gave it a page;
  session I deleted the last two copies (`input-to-movement`'s four-method
  table and `player-anatomy`'s section) in favour of a link plus the two
  consequences each page's own story needs. That closes the notebook's
  three-pages-in-two-parts finding and answers its open question with a
  fourth answer: none of the three candidates — its own page.
  **Lanes.** Six rows added (`Inv`, `FD`, `FP`, `KM`, `KI`, `MEI`) and five
  mis-keyed lanes corrected in the old diagrams — `CL` meaning
  `ServerGamePacketListenerImpl`, `PL` meaning `Player`, `CM` meaning
  `AbstractContainerMenu`, `IS` meaning `ItemStack`, `MG` meaning
  `MultiPlayerGameMode`, each of which already meant something else corpus-wide.
  `check_lanes --strict --pages src/systems/player` is clean, **154 diagrams
  render**, 18,240 names resolve, every relative link in `src/` resolves, and
  the reference indexes are regenerated. Seven pages at 174–410 lines, six of
  them inside the brief for the first time in pass 3; `input-to-movement` is
  the outlier and its seam (client half / server judgement) is logged for
  pass 5. Hand-offs in pass3.md §8, pass4.md and pass5.md.
  Process note: written by the session directly rather than by parallel
  drafting agents, because everything but `the-spear` was pass-2 prose being
  re-cut and the diffing step is the expensive half of that protocol. The one
  page that needed research was researched first, before any page was written,
  which is what made the seven-page rewrite affordable.

- **2026-09-03, out of band — the repo went public-safe.** Not a pass session;
  triggered by the first fork (and star) of the GitHub repo, which made the
  question *what does a stranger get when they clone this* worth answering
  properly. **Nothing was leaking.** `git log --all --diff-filter=A` over the
  whole history finds no file under `reference/`, no jar, zip or class, no
  secret; `tools/deploy.sh` reads the Cloudflare token from `~/.cloudflare/`
  at run time and has never contained one; there are no ```` ```java ```` blocks
  in any of the 132 tracked files, so rule 1 is holding by practice and not
  only by intent. The file most likely to be a problem, `class-index.md` at
  372 KB, is a book index — 2,560 class names against the pages that discuss
  them, no obfuscated pairs, no member signatures — and is not a mappings
  extract.
  **What was missing was a licence.** The repo was all-rights-reserved by
  default, which is the worst of both: a good-faith reader has no safe way to
  quote a page, and a bad-faith one gets to say it looked open. Now
  **CC BY-SA 4.0** for `src/` (the prose and the figures) and **MIT** for
  `tools/`. The owner chose BY-SA over BY-NC-SA on the argument that the real
  threat is an unattributed mirror outranking minecraftdocs.dev, which
  attribution and share-alike prevent and a non-commercial clause does not —
  NC does not even forbid an ad-free mirror, and it costs citations and wiki
  reuse. The cost accepted: someone may build their own videos from these
  notes, but only with visible credit. `LICENSE` is the canonical CC text with
  no preamble so GitHub's detector recognises it; the scope note lives in the
  README instead.
  **The Mojang carve-out is now stated, not assumed.** README and
  introduction both say the licence covers the writing and the figures and
  not the game, its source, its assets or the mappings, and tie that to why
  the pages name identifiers and never reproduce code. `site-footer.js` puts
  that line plus the unofficial/trademark disclaimer on **every** page
  (mdBook has no footer setting, so it appends to each page's `<main>`) —
  every page rather than the introduction alone, because pages are linked to
  and quoted individually and a mirror has to actively strip a footer.
  **Two smaller things.** The introduction's *verified means tested* rule now
  says what the check does **not** prove — that the sentence around the name
  is true — and points at the passes; publishing the pass notebooks means
  that admission is public anyway, and stating it first turns it from a
  gotcha into the method. And the README now has a corrections policy:
  issues with a decompile citation are the wanted contribution, prose PRs are
  not merged, because nothing publishes here that the owner has not read
  against the source, and a merged patch routes around exactly that.
  Process note: session I was running concurrently and its add-all commit
  (`a520d6c`) absorbed the half of this change that existed at the time, so
  the licensing lands in two commits — `a520d6c` and `185f16b`, whose message
  names the first. Worth knowing for pass 4, when sessions may again overlap:
  commit named files as soon as the checks pass rather than batching.

- **2026-09-03, pass 3 session J — Part IX Networking. The ruling, written
  before any edit.** *(the record of what was done follows below)*
  **The part's shape: one wire, three passengers.** The notebook's finding
  (§1, session G) stands with the pages open — Part IX is not two pipelines
  meeting at the wire, it is one pipeline that three unrelated systems ride.
  The landing page draws it that way: a spine of two pages that carry bytes,
  and three pages hanging off it that each have a different shape and a
  different reason to exist.
  **The page list: no splits, no merges, no new pages, no renames** — and so
  no redirects. Five pages, reordered, four of them rewritten.
  1. `the-connection` — **the trace**, and it takes the merge's dividend
     without the merge: the notebook wanted one round-trip diagram, and this
     page gets it (client value → codec → wire → server handler → back),
     because a single picture of the thread hop *and* the codec layer is the
     artefact the pair exists for. Splitting a 550-line page and a 448-line
     one into one 1,000-line page would have failed the length brief on its
     own; the pair becomes **one lecture in two halves** by sharing one
     diagram and one continuous story instead. Half one is the transport.
  2. `packets-and-stream-codecs` — half two, and a **vocabulary page**: what
     a packet *is*, once you know how it travels. It does not redraw the
     journey; its figure is the codec layer itself. Moved to second in the
     sidebar so the two halves are adjacent.
  3. `protocol-phases` — untouched in shape (session A's pilot, a **state
     machine**); re-checked for borrowed facts and links only.
  4. `what-the-client-is-told` — the **policy** page it always was. The
     creeper trace's gate cascade becomes a flowchart of one entity's tick;
     the sequence diagram keeps only the pairing bundle. Its client-coping
     sections go to Part X as links (session G's guess, taken).
  5. `chat-and-signing` — a **protocol with an adversary**, and its figure is
     the three-column table of what each check catches and what dies:
     message, chain, or connection. Its `Component` paragraph becomes a link
     to Part II's `text-components`, which session C wrote.
  **The three borrowed facts are replaced by links, not restated.** The
  broadcast in the chunk-source phase → Part III's `server-level-tick`; the
  second flush after `MinecraftServer.tickChildren` → Part III's
  `server-tick`; the per-frame packet drain → Part I's `anatomy` two-loops
  figure, with Part X's `the-client-loop` as the deeper reference. Session I
  named the first two as Part III's to own; this session is the caller that
  stops restating them.
  **No coverage page.** R7 allows one; the queue holds none for Part IX (the
  debug-subscription question is session K's, since `debugging-the-running-game`
  already lives in Part X), and the budget is better spent on the round-trip
  diagram.

  **What was done.** Five pages, four rewritten, one landing page written,
  no splits and no renames — so no redirects, and the sidebar changed only
  in order: the wire pair is now adjacent and `protocol-phases` follows it
  rather than sitting between its halves. `the-connection` (550→442) is the
  trace and carries the round-trip diagram the merge was wanted for: six
  lanes, four thread boundaries marked, a value leaving the client's main
  thread and the reply arriving back at a drain that runs once per frame.
  Its hook is the one the pair had been sitting on all along — **singleplayer
  serialises every packet to bytes and parses them back**, through a real
  encoder and a real decoder, with the in-memory pipeline differing only in
  the framing and in never installing a cipher.
  `packets-and-stream-codecs` (448→449) is the second half and a vocabulary
  page: it does not redraw the journey, its figure is the codec composition,
  and its hook is that **a packet's id is the position of one line in a chain
  of registration calls** — so the same packet type is a different number in
  each phase it appears in. `what-the-client-is-told` (546→461) became the
  policy page it always was, the buried gate cascade drawn as a flowchart of
  one entity's tick and the old trace reduced to the pairing bundle, which is
  the only part of it that was really a conversation; its client half went to
  Part X. `chat-and-signing` (365→316) is the adversary page: three ways to
  say no, drawn, then eighteen checks in a table whose third column has
  exactly three values — the message dies, the chain dies, or the connection
  dies.
  **The lane ruling was overruled once, correctly.** The session proposed
  `PktE`/`PktD` for the packet encoder and decoder to avoid `PE`
  (`ParticleEngine`); the drafting agent found the key already had
  `PEnc`/`PDec` from `codecs-nbt-json`, satisfying the actual constraint, and
  used those instead of putting two abbreviations on one class. Three
  standing Part IX lane disagreements are now gone; the details are in
  [pass3.md](pass3.md).
  **What went wrong, and what it cost.** Two of the four drafting agents hit
  the account's spend limit *after* writing their pages and *before*
  reporting, so `packets-and-stream-codecs` and `chat-and-signing` were
  accepted on the session's own checks — names, lanes, mermaid, budgets,
  shape, and four load-bearing claims spot-checked by hand — without the
  claim-by-claim diff against pass 2's text that step 4 of the protocol
  requires. That is a real gap, it is written down as one at the head of
  [pass4.md](pass4.md)'s session-J entry, and pass 4 re-checks those two
  pages whole rather than targeting a list. The lesson for the remaining part
  sessions: **an agent's page is worth nothing until its claim list is in
  hand**, so ask for the list first and the prose second, or budget for
  losing the last agent in a fan-out.
  Checks at commit: 18,034 names resolve, 158 diagrams pass, Part IX clean
  under `check_lanes.py --strict`, class index and lane index regenerated.

- **2026-09-03, pass 3 session K — Part X The client. The ruling, written
  before any page was opened.**
  **The part's shape is a hub and its spokes, and every spoke is named by
  its cadence.** Session H's finding, taken as-is: Part X is not a pipeline
  and must not pretend to be. `the-client-loop` is the hub — the one page
  that says when anything on the client runs — and every other page in the
  part answers "when in that loop does *this* happen": per tick, per frame,
  per event, per packet, per sound, per subscription. The landing page's
  figure is that hub with its spokes labelled by cadence, not by hand-off
  order. The one internal pipeline is the GUI stack
  (`gui-and-screens` → `the-gui-render-tree` → `text-and-fonts`), taught
  consecutively, with `hud` as its fourth page — the other recorder.
  **Thirteen pages after one split.** `sound` becomes `sound-engine` (the
  machine: five threads, one OpenAL device, one hop the sound cannot skip)
  and `what-makes-a-sound` (the content model: the three doors a sound comes
  through, and the fact that most world sounds are an int). `sound.md` is
  deleted and redirects to `sound-engine.md`. Session A found the material
  was two pages' worth and did not split; after session H every other page
  in the part is one cadence and one subject, and sound was the only page
  still carrying an engine and a content model. No other splits, no merges,
  no renames.
  **The order, hub first, then the spokes grouped by cadence:**
  `the-client-loop` · `the-client-level` · `prediction-and-acks` ·
  `input-and-keybinds` · `options` · `gui-and-screens` ·
  `the-gui-render-tree` · `text-and-fonts` · `hud` · `sound-engine` ·
  `what-makes-a-sound` · `debugging-the-running-game`. Unchanged from the
  sidebar's order except that the sound pair replaces one page.
  **The shapes, one per page, chosen so no two neighbours read alike:**

  | page | shape | its hook |
  |---|---|---|
  | `README` | landing | — |
  | `the-client-loop` | trace, figure overruled to a **flowchart** | the frame that earns fifteen ticks runs ten and loses five |
  | `the-client-level` | **comparison** — the same `Level` class, two authorities — grounded by the chunk-arrival trace | the client's tick lists accept a schedule, drop it, and then answer *no* when asked whether one is pending |
  | `prediction-and-acks` | **state machine** — a two-column state diagram, ledger entry against server counter | the receipt is for a number, and it is sent for the actions the server refused |
  | `input-and-keybinds` | trace — **holding sneak**, not pressing E | a key press is fully processed before the tick that observes it |
  | `options` | **policy** — saving *is* the event system | a cycle button broadcasts your client information on every click |
  | `gui-and-screens` | **vocabulary page**, grounded by pressing E | the survival inventory is opened entirely client-side, and its menu has no `MenuType` |
  | `the-gui-render-tree` | **vocabulary page** — a figure of the tree, not of time | layering is inferred from bounding boxes and never declared |
  | `text-and-fonts` | **pipeline** — six stages from a `Component` to a quad | measuring text bakes a glyph and uploads a texture |
  | `hud` | **policy** — what is drawn, when, and what F1 does not hide | F1 does not hide the sleep fade |
  | `sound-engine` | trace — a block placed near you, through five threads | a sound always starts at least one hop after the packet, even on a cache hit |
  | `what-makes-a-sound` | **comparison** — three doors | most world sounds are an int, and your own sounds never round-trip |
  | `debugging-the-running-game` | **the pattern** — one subscription, sixteen instances, one traced | none of it is stripped from the shipped jar; the client simply never asks |

  **Two diagram-shape overrules, both session H's.** `the-client-loop`'s
  trace is a *loop* and a sequence diagram cannot say so — its most
  important fact, that ticks are dropped, was living in a label on a bounded
  block. It becomes a flowchart with the clamp as a decision node and the
  drop as its own box. `the-gui-render-tree`'s subject is a tree with a
  placement rule, and its sequence diagram was a flowchart in a sequence
  diagram's clothes; it becomes two flowcharts, one of the data and one of
  the draw pass. `prediction-and-acks` gains the two-column state diagram
  session H asked for and keeps the refusal sequence as its second figure —
  the one page in the part with two figures of different kinds, because the
  ledger's *state* and the packet *ordering* are two different claims.
  **`hud`'s gate table goes to Reference**, as `src/reference/hud-elements.md`
  — the twenty-two elements of the HUD in record order with the condition
  each is gated on, which is exactly the thing R5 says a viewer would pause
  the video to read. `hud` keeps the two-block structure as a flowchart and
  links.
  **`prediction-and-acks` and `text-and-fonts` stay in Part X**, overruling
  session H's own observation that they would sit equally well in Parts IX
  and XI. The packaging argument is weak, but the *watching* argument is
  not: Part V's landing page already rules that Part V is watched before
  `prediction-and-acks`, so moving the page into Part IX would put it before
  its own two applications, and `text-and-fonts` is the only page a viewer
  can watch after Part II's `text-components` without having seen a single
  render pass. Both are recorded as answered open questions in
  [pass3.md](pass3.md) §6.
  **`debugging-the-running-game` is placed, and stays where it is.** Session
  H asked whether the debug subscription system belongs to Part IX (a server
  push), Part X (the client draws it) or a part of its own. It is Part X's,
  as the part's closer, for the reason the page already gives: the
  machinery ships on the dedicated server, but the client is the only thing
  that ever asks and the only thing that draws, and the page's trace ends in
  a renderer. It is the part's one **pattern** page, which is also why it
  closes rather than opens.
  **No coverage page.** R7 allows one; the queue's only Part X entry is
  *world creation and the world-select screens*, ~5,100 lines that session J
  found spanning Parts X and XII. It is ruled **not this session's**: half of
  it is worldgen's world-creation settings and half is a screen family, and
  splitting the subject across two part sessions is how the corpus grew its
  duplications. It stays in the queue with that reason, for session M and
  session P to co-rule. The sound split is a confirmed split, not new
  coverage, and spends no allowance.
  **What session J handed over is checked, not assumed.** Session J's
  hand-off lists six `ClientLevel` facts that left `what-the-client-is-told`
  for Part X; each is confirmed present in `the-client-level` or added, and
  the one with no owner anywhere in the corpus —
  `Entity.moveOrInterpolateTo` and which entity families supply an
  `InterpolationHandler` — is written into `the-client-level` this session.

  **What was done.** Thirteen pages where there were eleven: twelve system
  pages plus a landing page, one split, one new Reference page, and no
  renames beyond the split — so one redirect (`sound.html` to
  `sound-engine.html`) and a sidebar that now folds onto a real page. Every
  page lost the seven-heading skeleton, the field inventories and the
  invariants bullet wall; the material went into a cast table, into the
  sentence that touches it, or into a *questions players ask* section, and
  the *headline for a 1.21-era reader* formula that opened seven of the
  eleven pages became a blockquote at the foot of each. Six shapes are in
  use across the twelve pages — trace, comparison, state machine, policy,
  vocabulary, pipeline and pattern — and no two neighbours share one.
  **Three diagrams were the wrong shape and are now right.**
  `the-client-loop`'s loop is a flowchart with the ten-tick clamp as a
  decision node and the dropped ticks as their own box, which is where its
  hook now lives instead of in a label on a bounded block. `prediction-and-acks`
  gained the two-column `stateDiagram-v2` session H asked for — a ledger
  entry's five transitions against a connection counter's three — and kept
  the refusal sequence beside it, because the ledger's *state* and the
  packet *ordering* are two different claims and only the second is a
  conversation. `the-gui-render-tree` became two flowcharts, one of the data
  and one of the draw pass, in place of a sequence diagram that was a
  flowchart in disguise.
  **Redrawing the loop found a real error.** The old sequence diagram put
  `FramerateLimiter.limitDisplayFPS` at the end of `Minecraft.runTick`,
  after *Post render*. It is inside `Minecraft.renderFrame`, after the
  present and before *Post render*. Session B's lesson holds — suspect the
  page, not only the tool — and the correction is at the head of
  [pass4.md](pass4.md)'s session-K entry so pass 4 checks it first, along
  with `the-frame`, which may have inherited the same mistake.
  **Session J's hand-off was checked rather than assumed, and one item was
  missing.** Five of the six `ClientLevel` facts handed over from
  `what-the-client-is-told` were present. The sixth —
  `Entity.moveOrInterpolateTo` and which entity families supply an
  `InterpolationHandler` — had no owner anywhere in the corpus and is now a
  table in `the-client-level`: seven overrides against a default that
  returns null and therefore snaps, which is why a dropped item moves
  differently from a mob over the same connection. Two smaller gaps were
  filled at the same time: `ClientPacketListener.serverChunkRadius` and
  `ClientPacketListener.serverSimulationDistance`, and the torus's
  `AtomicReferenceArray` and volatile centre.
  **`hud`'s gate table is the R5 precedent.** Twenty-two HUD elements plus
  the four `Gui` records after them, in record order, with the condition
  each is gated on: `src/reference/hud-elements.md`. It answers section 6's
  open question about reference-tier tables inside lecture pages with *no,
  a Reference page and a link* — which is the answer session L needs for the
  render-state hierarchy and session N for the selector grammar.
  **No coverage page, deliberately.** The queue's only Part X entry spans
  Parts X and XII, so it is deferred to session M with the worldgen half in
  front of it rather than declined; the reason is written into
  [pass3.md](pass3.md) §7's discipline note rather than only here.
  Checks at commit: 17,869 names resolve, 165 diagrams pass, Part X clean
  under `check_lanes.py --strict`, the corpus-wide lane count down from 25
  disagreements and 16 collisions to 19 and 10, class index and lane index
  regenerated, `mdbook build` clean and no broken internal links.
- **2026-09-03, session L — Part XI Rendering.** *Rulings, written before
  editing.* **The part is a substrate under a pipeline, and the order is
  R6's.** `the-frame` opens — it is the part's trace and its shortest page,
  and a reader who has seen one frame end to end has a reason to care what a
  `GpuDevice` is — then the substrate (`the-window`, `blaze3d`), then the
  pipeline. Session I's two open questions are closed with it: **the
  substrate is two lectures, not one** (a GLFW window, its six callbacks and
  `NativeImage` are a different subject from a graphics API with two
  backends, and neither hook survives being merged with the other), and
  **`the-window` stays in Part XI**, second, rather than moving to Part I —
  it is a rendering prerequisite, not a program-anatomy one, and Part I is
  deliberately two pages.
  **`level-rendering` splits, and it is the corpus's oldest deferred seam.**
  Four sessions (10, H, I and the split table) confirmed *meshing* against
  *visibility and the frame graph* and none executed it; pass 3 is the pass
  that executes splits, and the page fails the cast budget twice over — its
  two halves share `LevelRenderer` and nothing else. The halves are
  **`visibility-and-the-frame-graph`** (what the frame draws: the occlusion
  BFS over an `Octree`, the frustum, the pass declaration order, the
  multi-draw batching and the translucency resort) and **`section-meshing`**
  (where the triangles came from: the dirty halo, the 27-section snapshot,
  the worker compile, the staging buffer and the late atomic swap).
  Visibility comes first, because it continues `the-frame` — which ends at
  `LevelRenderer.render` — and because meshing is gated on it. The old URL
  redirects to the visibility half (R8).
  **The R7 page is post-processing**, session I's strongest candidate: 996
  lines in four classes named on no page, six `post_effect` chains now in
  `reference/26.2/assets/` to write it against, and the only place in the
  game where user-authored shaders are first class. It is the part's closer,
  because its instances are spread across every page before it — two chains
  declared inside `LevelRenderer.render`, three chosen by
  `GameRenderer.checkEntityPostEffect`, one behind a pause screen.
  Block-entity rendering stays queued; **"how an item picks its model"
  becomes a named section of `models-and-atlases`**, not a page, which is
  what session H's hand-off requires — Part VII's two forward links now land
  on a heading rather than a page that only mentions `ItemModelResolver` in
  passing.
  **Shapes, one per page, no two neighbours alike.** `the-frame` the trace;
  `the-window` the trace with the retry loop drawn as the flowchart the
  notebook asked for; `blaze3d` the **vocabulary page** (the façade and its
  four objects, grounded by one draw); `visibility-and-the-frame-graph` the
  pipeline; `section-meshing` the trace; `models-and-atlases` the pipeline,
  with the fan-out/barrier figure the notebook asked for; `entity-rendering`
  the pipeline (extract, submit, prepare, execute); `lightmap-fog-and-sky`
  the **pattern** — one question (*what is this attribute worth, here,
  now?*) asked by five renderers, which is what lets the page stop
  re-teaching Part IV's system; `particles` the **policy**, because its
  subject is five gates that disagree with each other; `post-processing` the
  pipeline.
  **Two Reference extractions, on session K's precedent** (a reference-tier
  table is a Reference page and a link, never a table inside a lecture):
  `entity-rendering`'s fifteen submit phases and thirteen feature renderers
  become `src/reference/submit-phases.md`, and its render-state hierarchy
  becomes a **generated** tree figure — `EntityRenderState` joins
  `TREE_ROOTS` in `map_source.py`, the pattern session G set with
  `tree-Entity.svg`. `lightmap-fog-and-sky`'s twenty-four-attribute
  enumeration is not extracted but dissolved: the page names the attributes
  in the sentences that use them and links to Part IV for the system.
  **Lanes: eleven collisions fixed, all by lengthening the later claimant.**
  `SectionCompiler` → `SectC` (`SC` is `StopCommand`), `Timelines` → `Time`
  (`TL` is `TagLoader`), `LightmapRenderStateExtractor` → `LRSE` (`LX` is
  `LevelExtractor`, keyed by session K), `SpriteLoader` → `SprL` (`SL` is
  `ServerLevel`), `GlCommandEncoder` → `GlCE` and `GpuBackend` → `GB` (`B`
  is `Block`, which particles should have been using), `MonitorManager` →
  `MonM` (`MM` is `ModelManager`), `GpuSurface` → `GpuS` (`GS` is
  `GaussianSampler`), `EnvironmentAttributeProbe` → `EAP` (keyed already;
  `P` was wrong), `Minecraft` → `MC` and `Window` → `Window` (both keyed
  already; `M` and `W` were wrong), and `(worker)` takes the existing word
  lane `Worker`.

  **What was done.** Thirteen pages where there were eight: eleven system
  pages, a landing page and a new Reference page. One split executed
  (`level-rendering` → `visibility-and-the-frame-graph` + `section-meshing`,
  one redirect), one page written from nothing (`post-processing`), one
  section written to discharge a ruling (*How an item picks its model*, which
  Part VII's two forward links now reach by anchor), one catalogue extracted
  (`src/reference/submit-phases.md`) and one figure generated
  (`tree-EntityRenderState.svg`, from `EntityRenderState` added to
  `map_source.py`'s `TREE_ROOTS`). Every page lost the seven-heading
  skeleton, and the part now has **zero bulleted lists in it** — eight pages
  each opened with a field inventory and closed with a twenty-bullet
  invariant wall, and all of that is now cast tables, decision tables,
  *Questions players ask* sections and the sentences that use each name.
  **Every page landed inside the 260–340 brief**, 256 to 339, which is a
  first; the brief went to the drafters in the prompt rather than as a
  correction. Six shapes across eleven pages — trace, vocabulary, pipeline,
  pattern, policy and the landing page — and no two neighbours share one.

  **Redrawing found two errors, which is three sessions in a row.** The first
  is the more instructive. `the-window` said that three of the six
  operating-system callbacks reach the game through `WindowEventHandler`;
  **only two do**, and the interface's third method, `resizeGui`, is never
  called by `Window` at all — its callers are `Minecraft` and `Options`,
  calling the game on itself. The old claim was an inference from three
  method names lining up with three callbacks, and it survived pass 2 because
  nobody had to *draw* it. The second: `level-rendering` gave
  `SectionOcclusionGraph.invalidateIfNeeded`'s triggers (an eight-block
  camera move, a field-of-view change, the smart-cull toggle) as the reason
  `LevelExtractor.applyFrustum` re-runs. Those schedule the **full walk**;
  the frustum step has its own gate, and the common half of it is the
  camera's pitch or yaw crossing a **two-degree** step — so turning your head
  re-applies the frustum without touching the walk. Both are fixed in the
  pages and are at the head of [pass4.md](pass4.md)'s session-L entry. The
  lesson for the remaining part sessions: **a figure asserts more than the
  prose it was drawn from**, which is the argument for drawing them.

  **The R7 page is `post-processing`, and it earned the slot.** 996 lines in
  four classes that no page named, six shipped chains, written against the
  JSON the planning session staged in `reference/26.2/assets/`. Its findings
  are the kind a coverage queue entry cannot predict: a chain's uniforms are
  packed and uploaded **once, at load**, so anything that has to vary per
  frame — the blur radius, for one — cannot be a chain uniform at all and has
  to come through the global block; the per-entry *name* in the JSON is read
  by no codec, only the type and the value, and members match the GLSL
  positionally; a resource pack can rewrite all six chains and add none,
  because the six ids are constants in Java; and the two chains that go
  through the deprecated `PostChain.process` door build a throwaway frame
  graph with no inspector, so **the pause blur and the spectator shaders
  appear in no slice of the F3 pie chart**.

  **Two more numbers were corrected in passing**, both cases of a page
  disagreeing with the corpus rather than with the decompile. `blaze3d`
  compared the backends at 7,461 lines against 5,623; they are 7,477 and
  5,627, and `what-this-book-skips` was already saying 7,477. And the landing
  page could not reproduce session I's "1,187 classes / 97,864 lines" for the
  rendering tree — the inventory never said which packages it counted — so
  the page states its own package set and counting rule and gives 1,179 and
  87,000, which is CLAUDE.md's own table added up.

  Checks at commit: 17,694 names resolve, 174 diagrams pass, Part XI clean
  under `check_lanes.py --strict` with thirty-three lane rows added (the
  pass's largest single addition, eleven of them lengthened later claimants),
  the corpus-wide lane count down from 19 disagreements and 10 collisions to
  15 and 6, class index and lane index regenerated, `mdbook build` clean and
  no broken internal links.
- **2026-09-03, session M — Part XII World generation.** *Rulings, written
  before editing.*

  **The part is a substrate, a pipeline and a wing.** Session J's §1 read is
  confirmed with the pages open: `density-functions` is not a step, it is the
  material every other page is made of, and the genuine sequence underneath
  it is biomes → noise/surface/carvers → features. What §1 did not name is
  that the three structure pages are not a fourth stage of that pipeline —
  they are a parallel wing that starts *earlier* than any of it
  (`ChunkStatus.STRUCTURE_STARTS` is the second status, two before
  `ChunkStatus.BIOMES`) and finishes inside `ChunkStatus.FEATURES`. So the
  part has two halves, terrain and structures, exactly as the schedule says,
  and the landing page draws them against the status ladder so that the
  lecture order and the execution order are visibly not the same thing.

  **`density-functions` still opens the part, against session L's
  evidence.** R6 ruled it and session L offered Part XI's counter-argument
  (open with the trace, then the substrate, then the pipeline, because a
  reader who has seen one frame end to end has a reason to care about
  `GpuDevice`). It is a real argument and it loses here for the reason
  session L itself gave: Part XII's substrate is genuinely prerequisite
  rather than merely underneath. `biomes` cannot explain the climate sampler
  without it, and `terrain`'s aquifer, ore veins and beardifier are all
  density terms. What Part XI's *frame* page bought — the whole shape before
  the abstract part — is bought here by the **landing page**, which carries
  the one-chunk overview figure. That is the ruling: the overview is the
  landing page's job in a part whose substrate is load-bearing, and no
  content page is spent on it.

  **Part XII stays one part.** §1 raised Part XII-A / XII-B, or promoting
  structures. R1 forbids a new numbered part this pass, and with the split
  executed the part is eight pages — the same size as Parts IV and XI — so
  the halves are a landing-page fact, not a numbering one.

  **The page list after the session** (eight content pages, one landing
  page, one new Reference page):

  | page | shape | hook |
  |---|---|---|
  | `README.md` *(new)* | the landing page | the status ladder, and why the lecture order runs against it |
  | `density-functions.md` | the pipeline (three rewrites) | the graph in the registry never runs as written, and a caching marker does not cache |
  | `biomes.md` | the trace, with one comparison section | there are two biome borders a couple of blocks apart, and block tint is on the side nobody guesses |
  | `terrain.md` *(renamed from `worldgen-pipeline.md`)* | the pipeline (noise · surface · carvers) | the carver does not choose the block it carves — the aquifer does |
  | `features-and-placement.md` | the trace (a stream of positions) | two biomes that disagree about feature order make the world refuse to open *(landed here rather than on count-then-scatter — see below)* |
  | `trees.md` *(new — the R7 spend)* | the pattern | the dark-oak sapling that never grows alone, which is an `Optional` left empty |
  | `structure-placement.md` *(from `structures.md`)* | the policy | the grid never looks at the world, and absence is stored as a hole rather than a marker |
  | `jigsaw-and-templates.md` *(from `structures.md`)* | the trace (a village) | a village stops growing because at the depth limit the assembler is offered only the fallback pool |
  | `hand-built-structures.md` | the pattern (four families, one traced) | a stronghold is a rejection sampler — no portal room, and the whole thing is thrown away and regenerated |
  | `src/reference/density-function-nodes.md` *(new)* | Reference | — |

  **`structures` splits three ways, not two.** The schedule says placement
  and jigsaw beside `hand-built-structures`, and the seam that survives
  contact with the page is: everything that is true of all sixteen structure
  types goes to `structure-placement` (the lottery, `StructureSet`,
  `StructurePlacement`, `ChunkGeneratorStructureState`, `Structure`,
  `StructureStart`, the reference scan, `StructureCheck`,
  `StructureManager`, `Beardifier`, `/locate`, and the per-chunk write), and
  the `.nbt` template system goes with **jigsaw** rather than staying in the
  framework page, because a template is how a pool element becomes blocks
  and the hand-built families reach it by link. `hand-built-structures`
  already declared that boundary from the other side and now points at the
  right page.

  **`worldgen-pipeline` is renamed `terrain`.** Two pages called *pipeline*,
  one the conveyor (Part IV) and one the cargo (Part XII), is a name
  collision that costs a reader the whole distinction the split was made
  for. Redirect kept under R8.

  **The catalogue extraction is the node families**, to
  `src/reference/density-function-nodes.md` — §1's "the rewrite story is the
  lecture, the node families are reference", executed. Hand-kept, for
  session O's sweep.

  **The R7 spend is the tree kit** (`trees.md`), the coverage queue's
  "probably the most watchable page in Part XII": fifty classes and ~3,000
  lines of `TrunkPlacer` / `FoliagePlacer` / `RootPlacer` / `TreeDecorator`
  implementations that `features-and-placement` documents as five contracts
  and zero instances. It also relieves that page, which is over-budget with
  tree material.

  **The world-creation ruling session L asked for.** *World creation and the
  world-select screens* (~5,100 lines, zero citations) is **one lecture and
  it belongs to Part XII**, not Part X: the subject is `WorldGenSettings`,
  `WorldDimensions`, `WorldOptions`, `levelgen/flat` and `levelgen/presets`,
  and `client/gui/screens/worldselection` is that subject's user interface —
  a Part X page would have to teach worldgen settings before it could
  explain a single screen. It is **not** written this session (the R7
  allowance went to the trees, which is a lecture rather than a settings
  tour) and stays in the queue with Part XII named as its owner, for session
  P or pass 6.

  **What was done.** Ten pages where there were six: eight system pages, a
  landing page and a new Reference page. One split executed (`structures`
  → `structure-placement` + `jigsaw-and-templates`), one page renamed
  (`worldgen-pipeline` → `terrain`), two redirects, one page written from
  nothing (`trees`, the R7 spend) and one catalogue extracted
  (`src/reference/density-function-nodes.md`). Every page lost the
  seven-heading skeleton and the part now has **zero bulleted lists in it**.
  Lengths 204 to 288 against the 260–340 brief — the first part to
  *undershoot* it, three pages under 240, which is worth noticing rather
  than fixing: the structure pages are short because the split gave each of
  them one subject.

  **Two hooks moved off the plan above while writing.**
  `features-and-placement` was slated for count-then-scatter and opens on
  the global sort instead — a data pack that makes the world refuse to open
  is the more surprising true thing, and count-then-scatter survives as a
  named paragraph. `trees`, whose hook the table could not name before the
  source inventory came back, opens on `TreeGrower.DARK_OAK`: the
  best-known growth rule in the game, that a lone dark-oak sapling never
  grows, is implemented as an `Optional` left empty.

  **Redrawing found two errors, which is four sessions in a row, and both
  are counts.** `features-and-placement` said sixty-three features are
  registered; it is **61**. And it called `CountOnEveryLayerPlacement` "the
  fifteenth" of the fifteen placement modifier types — there are fifteen,
  but it is **ninth** in declaration order, so the ordinal is wrong where
  the count is right. Both are fixed and both head
  [pass4.md](pass4.md)'s session-M entry. The generalisation for the
  remaining sessions: pass 2 checked counts and did not check **ordinals**,
  and an ordinal is a count with an extra claim in it.

  **The R7 page is `trees`, and the coverage queue's own framing was
  wrong.** The entry promised "how one species of tree differs from
  another" and the page that came out is mostly about what they *share*: one
  `final` algorithm with five codec-dispatched slots, and an asymmetry
  inside it that no configuration can reach — `TreeFeature` samples a
  proposed height, sizes the foliage height and leaf radius from it, and
  only then runs the clearance scan, so a clipped tree grows a short trunk
  under a full-size crown and every one of the eleven foliage placers
  ignores the clipped height it is handed. Three more findings the queue
  could not have predicted: `FancyTrunkPlacer`'s crown-candidates-per-level
  count is pinned at one by a minimum against one, so its named density
  constant does nothing at any height; `CherryFoliagePlacer`'s codec gives
  its *corner hole chance* field a getter that returns the *wide bottom
  layer* field, so decoding is right and any encode writes one value into
  both; and `TreeGrower.PALE_OAK` points at the decorator-free bone-meal
  variant, so a player-grown pale oak gets neither moss nor a creaking
  heart.

  **Three of the part's lane collisions were settled by not drawing a
  sequence.** `terrain`, `density-functions` and `structure-placement` all
  chose flowcharts, and `SS` — which meant `SurfaceSystem`, `StructureStart`
  and `StrongholdStructure` on three adjacent pages — is now used by none of
  them and left free for Part XIII's `ServerScoreboard`. Twenty-eight rows
  added, seven lengthened later claimants, two claimed against unconverted
  Part XIII (`CA`, `CF`). Part XII is clean under `check_lanes.py --strict`
  and the corpus-wide count fell from 15 disagreements and 6 collisions to
  **7 and 1, every one of them in Part XIII**.

  **The world-creation ruling** session L asked for is above and is recorded
  against the queue entry in [pass3.md](pass3.md) §7: one lecture, Part
  XII's, not written this session.

  Checks at commit: 17,335 names resolve, 179 diagrams pass, Part XII clean
  under `check_lanes.py --strict`, class index and lane index regenerated,
  `mdbook build` clean and no broken internal links across `src/`.

- **2026-09-03, session N — Part XIII Commands and data packs.** *(rulings
  written before any editing, per protocol step 2.)*

  **The part is a stack with three floors**, and the landing page says so:
  *parse* (`brigadier-and-commands`, `permissions`) → *execute*
  (`the-execution-engine`, `functions-and-macros`) → *what commands are for*
  (`advancements`, `scoreboard-and-data`, `dialogs`, `game-tests`). The
  dependency is strictly one-directional, which is why the third floor's four
  pages are peers rather than a sequence.

  **Nine pages where there were five**, with the shape and the hook decided
  first:

  | page | shape | hook |
  |---|---|---|
  | `README.md` | landing | — (the three floors, drawn) |
  | `brigadier-and-commands` | trace — `/give` | the client parses every keystroke against a real dispatcher and throws the answer away; the round trip is the default, not the fallback (62 of 67 providers) |
  | `permissions` **(new, the R7 spend)** | vocabulary | an op does not have everything: `LevelBasedPermissionSet` grants exactly one atom, and a permission failure is reported as an unknown command |
  | `the-execution-engine` | trace + queue snapshots | `/return` deletes work out of a queue instead of unwinding a stack, and a fork creates no frames at all |
  | `functions-and-macros` | pipeline — file → compiled → instantiated → queued | a macro function reached with no arguments fails silently, every tick, forever |
  | `advancements` | trace — "Stone Age" | the subscription table only ever shrinks, and the client is told the requirements but never the criteria |
  | `dialogs` | trace | a server can put a form in front of you *before you are in a world*, and the pause validation then runs on the client |
  | `game-tests` | vocabulary | the annotations are gone, a batch **is** an environment, and the shipped jar contains exactly one test |
  | `scoreboard-and-data` | trace — `execute store` | a player's score is keyed by their name and a mob's by its UUID, in one flat map |

  **Three splits, all confirmed by the notebook and named in the schedule:**
  `brigadier-and-commands` → + `permissions`; `execution-and-functions` →
  `the-execution-engine` + `functions-and-macros`; `dialogs-and-tests` →
  `dialogs` + `game-tests`, which is now safe because
  [the data-driven type pattern](../src/systems/foundations/data-driven-types.md)
  exists in Part II and owns the argument that held the page together.

  **The R7 allowance is spent on `permissions`** — it is in the coverage
  queue, it is the biggest API break in the corpus and four sessions running
  named it as the cleanest seam. The function model and the dialogs/tests
  split are executed as *splits* (§2's split table), not as coverage
  additions. The **selector grammar** and **`GameTestHelper`** stay queued.

  **Advancements' client screen stays a section**, and becomes the page's
  closing one. It is six classes of user interface whose only mechanism —
  a tree the server laid out and shipped — is already the page's subject; a
  page of its own would be a screen tour, and Part X owns screens. What it
  gets instead is the last word, where a viewer sees the data structure they
  already know from playing.

  **The predicate-shape library stays on `advancements`**, trimmed.
  `contexts-and-predicates` (Part VII) owns the context machinery and does
  not own `MinMaxBounds`, `CollectionPredicate`, `EntitySubPredicate` or
  `DataComponentMatchers`; advancements is their biggest consumer, so they
  stay where they are read and go to [pass3.md](pass3.md) §7 as a Reference
  candidate for a later pass.

  **`scoreboard-and-data` stays one page**, and the scoreboard stays in Part
  XIII (R6). The scores/teams and paths/storage halves are joined by
  `execute store`, which is the page's only trace; split them and neither
  half has one.

  **What was done.** Nine pages where there were five: eight system pages
  and a landing page. Two splits executed (`execution-and-functions` →
  `the-execution-engine` + `functions-and-macros`; `dialogs-and-tests` →
  `dialogs` + `game-tests`), both redirected under R8; one page written from
  nothing (`permissions`, the R7 spend); and the remaining four pages
  rewritten end to end. Every page lost the seven-heading skeleton and every
  diagram in the part is new or redrawn. The part now has **one bulleted
  list in it** — a two-item list on the engine page — where it had eleven
  bullet walls.

  Lengths 131 to 371 against the 260–340 brief, and the distribution is the
  honest result of the splits: `dialogs` (174), `game-tests` (178) and
  `functions-and-macros` (189) undershoot because each now has exactly one
  subject, and `scoreboard-and-data` (371) is the one page that overshoots —
  which is the split this session declined, arguing back. The part's total is
  2,129 lines against the old 2,150, so nothing grew; it redistributed.

  **The R7 page is `permissions`, and writing it changed the claim.** The
  queue promised "the biggest API break in the corpus" and that is true, but
  the page's actual subject turned out to be an asymmetry nobody had named:
  the server's permission model is **additive** — a rung, plus exactly one
  hard-coded atom, unioned upward, and `LevelBasedPermissionSet.union` of two
  level sets is just the higher of the two — while the client's chat model is
  **subtractive**, starting from all four chat atoms granted and letting each
  of four purely local `ChatRestriction`s remove some. No packet carries a
  `PermissionSet` in either direction. The consequence is the page's second
  half: the client can only ever learn *"this needed some permission"*, and
  it learns even that by parsing the same string twice, once with its own set
  and once with `PermissionSet.NO_PERMISSIONS`, and reading the difference.
  One exception proves the rule — `GameModeCommand.PERMISSION_CHECK` is
  exported so that `KeyboardHandler` and `GameModeSwitcherScreen` can run a
  *server* check locally, which is why the F3+F4 switcher greys out.

  **Rewriting found three count errors, which is five sessions in a row.**
  Pass 2's "all ninety-four *requires* calls in the game use
  `Commands.hasPermission`" was a true statement about the server made as a
  statement about the game: `.requires(` appears 245 times, and 150 of those
  are `ShapelessRecipeBuilder.requires`. There are **95**
  `Commands.hasPermission` call sites — 94 server-side registrations plus
  one on the *client*. `advancements` said the client half was "six classes
  … (`net/minecraft/client/gui/screens/advancements`)", which counted
  `package-info.java` and put `ClientAdvancements` in the wrong package; it
  is five classes there plus `ClientAdvancements` in `client/multiplayer`,
  about 1,240 lines. And the worst of the three, because a sentence's
  argument rested on it: `scoreboard-and-data` said `execute store` has
  **two** sinks "which are exactly the two models here". It has **three** —
  `ExecuteCommand.wrapStores` builds score, boss bar, and the three data
  providers. The generalisation to carry: pass 2 checked counts inside a
  page's own scope and did not check counts used as *arguments for the page's
  shape*, which are the ones a restructure leans on hardest.

  **Two rulings the schedule asked for.** *Advancements' client screen* stays
  a section and becomes the page's closing one — six classes of user
  interface whose only mechanism is a tree the server laid out, which is
  already the page's subject; a page of its own would be a screen tour, and
  Part X owns screens. *`scoreboard-and-data` stays one page*, which also
  answers §1's older question about whether the scoreboard belongs to Part
  XIII at all: R6 said it stays, and the page's only trace is a command. The
  boss bar and the statistics are still the two subjects with no owner
  anywhere in the corpus.

  **The lane gate is now green corpus-wide.** Twenty-six rows added, and
  Part XIII took the three short forms Part XII deliberately left free (`SS`
  for `ServerScoreboard`; `SP` stays `ServerPlayer`). Seven later claimants
  lengthened (`CSug`, `CAdv`, `CallF`, `ContT`, `GTR`, `DlgS`, `CComPL`) and
  four bare-initial lanes the old diagrams used were retired under the
  two-letter rule (`C`, `M`, `T`, `R`). `python tools/check_lanes.py` reports
  **537 participants, 0 disagreeing and 0 colliding, across the whole
  corpus** — session P can turn `--strict` on unconditionally. One collision
  is recorded and deliberately not drawn: `ExecuteCommand` names two
  unrelated classes, and the key resolves simple names, so the engine page
  names the task in prose and never as a lane.

  Checks at commit: 17,056 names resolve, 184 diagrams pass, Part XIII **and
  the whole corpus** clean under `check_lanes.py --strict`, class index and
  lane index regenerated, `mdbook build` clean, and no broken internal links
  across `src/`. Hand-offs written to [pass4.md](pass4.md) (the three count
  corrections first, then thirteen new source-derived claims and every
  redrawn figure), [pass5.md](pass5.md) (the cuts, and second person now five
  parts wide) and [pass3.md](pass3.md) (two queue entries discharged, one
  opened, and the notes for sessions O and P).
