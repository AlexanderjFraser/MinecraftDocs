# Pass 5 — the book: the agent's brief, the session's runbook, the standard and the schedule

*Written 2026-09-05 by the planning session between pass 4 and pass 5, so that
every pass-5 session (A–O, run on Opus) launches the same read the same way.
Part 1 is handed to the agent verbatim — `tools/pass5_prompts.py` prepends it
to each page's prompt file. Part 2 is the session's own procedure. Part 3 is
session A's work: the rulings the part sessions apply, made once. Part 4 is
the schedule, one session per part, with what the tools measured before the
first session spent anything. The charter this implements is in
[plan.md](plan.md) under *Pass 5 — the book*; the queue it draws on is
[pass5.md](pass5.md), kind `book`; the coverage queue is [pass3.md](pass3.md) §7.*

**The owner's ruling, 2026-09-05, which shapes this pass.** The site is the
deliverable and it stands alone: readers today have only the textbook, so
nothing on a page may lean on a lecture to make sense, and the lecture order
and any tiering of episodes are the owner's own work, not this pass's. The
page count is whatever the book needs — a merge or a split is judged by the
reader who has only the page, never by the number of episodes. Everything
inside the current scope is explained, concisely: the coverage question is
real, and its answer is usually a section, a Reference row or a sentence,
with a page only where a part's argument has a hole. Concision governs *how*
a thing is explained, not *whether*.

**The tools** (all new this session; every one ships with `--probe`, which
proves it fails on the construct it should):

| tool | what it answers | run as |
|---|---|---|
| `tools/pass5_dups.py` | where the book explains one thing twice: page pairs ranked by the rare backticked names they share, and near-duplicate sentences across pages; `--terms` asks which pages carry a through-line | `--summary`, `--page world/lighting`, `--terms "a,b"` |
| `tools/pass5_coverage.py` | the coverage question per part, with the atlas as the population: every class in the part's packages that no page names, ranked by lines, by sub-package | `--part world`, `--all --summary` |
| `tools/check_links.py` | every internal link, anchor, include, SUMMARY entry and redirect resolves — **a deploy gate from this session** (clean on day one); `--inbound PAGE` lists every page that links to a page, with the sentence | `--quiet`, `--inbound src/systems/world/lighting.md` |
| `tools/pass5_queue.py` | [pass5.md](pass5.md) routed by kind (book · lecture · figure · voice) and by page; a `?` marks a guessed kind, and a `[kind=…]` tag in the entry settles it | `--kind book --part world`, `--summary`, `--unsure` |
| `tools/map_source.py` | the atlas now carries the thirteen parts as package sets (`PARTS`) and writes `src/generated/parts.md` and one `part-<dir>.md` phrase per part, so a landing page includes its size instead of counting it | `python tools/map_source.py` (deploy runs it) |
| `tools/pass5_prompts.py` | one prompt file per page: Part 1 below, then the page's queue entries, its duplication report, its inbound and outbound links with sentences, and the through-lines it carries; per part, the coverage report and the part-wide notes | `--part world --out DIR` |

---

## Part 1 — The brief (given to one agent per page)

You are reading one page of MinecraftDocs — a book about how the Java
Minecraft 26.2 codebase works — **as a page of a book**, not as a page on its
own. The book has 102 system pages, thirteen landing pages and twenty-one
Reference pages, written by thirty sessions each of which saw one page or one
part; every fact on every page has been checked against the decompiled source
twice. What no session could see is the book: the mechanism explained on two
pages, the term used before the page that defines it, the dependency with no
link, the class in a part's packages that no page mentions. Your job is to
find those for this page. You have no decompiled source, on purpose, and you
change no fact.

### What you have

- **The page**: the path is at the top of your prompt file. Read all of it.
- **The other pages**: the whole book is under `src/` (system pages under
  `src/systems/<part>/`, the part's landing page at `README.md` there,
  Reference under `src/reference/`). Read whole any page the prompt file names
  under *Pages this one shares the most rare names with*, any page that links
  here, and the part's landing page. Do not skim them; the finding is in the
  paragraph, not the title.
- **The prompt file**, after this brief: (1) every open queue entry about this
  page from the earlier passes, (2) the duplication report — which pages share
  this page's rare identifiers, and which sentences here have a near-twin
  elsewhere, (3) every inbound link with the sentence it sits in and every
  outbound link, (4) which of the book's seven through-lines this page
  carries. The part's coverage report is beside it as
  `_part-coverage-<part>.md`: every class in the part's packages that no page
  names, ranked by lines.
- **The rules of the book**, which decide what a finding is: a page names
  classes, never reproduces code; a page is one scenario followed through the
  system; every mechanism has one home; later parts assume earlier ones and a
  link points from the page that assumes to the page that explains;
  Reference pages hold enumerations, never explanations.

### The five questions

1. **Ownership.** For every mechanism this page *explains* — says how it
   works, not merely names — is the same mechanism explained on another page?
   A shared backticked name is a hint, not a finding; two paragraphs that
   would teach a reader the same thing are the finding. For each: both
   locations as `page:line` with the sentences quoted; which page should own
   it under the ownership rule, applied in this order — the page whose
   scenario the mechanism is the answer to; within a part, the page whose
   figure draws it; a vocabulary page owns what a thing *is* and a trace owns
   what *happens*; and only then, between parts, the earlier one. Reference
   owns lists, and a lecture never reproduces one. Then: what the other page
   keeps, which is at most one sentence and a link to the owner's **anchor**.
   If the second explanation says something the owner lacks, say so: that is
   a move, not a cut.
2. **The seams.** Every dependency without a link: a term, a mechanism or a
   class this page assumes the reader knows, explained on another page and not
   linked at first use here. Every link that lands on the wrong page — the
   page it points at no longer explains the thing, or another page explains it
   better. Every hand-forward that is not paid off: a sentence saying another
   page owns or will explain something, where that page does not. Every link
   into a *later* part, which is a promise the later page must keep.
3. **The through-lines.** The seven ideas that cross parts — the tick and its
   phases, the four threads, the wire and the hop, authority and prediction,
   the registry freeze and the reload, the data-driven type pattern, the
   ledger — are each told once at full length on an owner page and cited
   everywhere else. Where this page *retells* one at length rather than citing
   it, quote the retelling with line numbers and say whether it adds anything
   the owner page lacks.
4. **Coverage and scope.** From the part's coverage report: which unnamed
   classes are in *this page's* scope — the mechanism its scenario runs
   through — and should be mentioned, and which are a family this page's
   pattern already covers (one sentence saying so is enough). Which classes
   the page names without explaining, where no other page explains them
   either. And the reverse: material on this page that belongs to another
   part's scope.
5. **The moves.** A section that would read better on another page, and
   which. A page carrying two subjects. A title that promises something the
   page does not deliver. A watch-order or a heading that disagrees with the
   landing page. Recommend; do not rewrite.

### Rules

- **No facts.** You are not fact-checking, and you have no source to check
  against. If you believe a sentence is false, put it under *Suspected
  errors* with your reason; the session re-derives it against the decompile.
  Never propose a rewording that changes what a sentence claims.
- **Quote line numbers** for every finding, on every page you cite. A finding
  without a line on both pages is not a finding.
- **Explained is not named.** A backticked name in passing is a mention. A
  duplicate is two explanations. The duplication report cannot tell them
  apart; you can.
- **A summariser is not a duplicate.** The part's landing page, the lecture
  map, the glossary and the introduction restate pages by design. Report them
  only where they *disagree* with the page, under *Summariser drift*.
- **The deliberate pairs stay.** Where a landing page or `src/lectures.md`
  calls two pages one lecture in two halves, a sequel, or a pair to keep
  together, a shared preamble between them is deliberate; report a drift
  between the two copies, never the copy. The fifteen declared pairs are
  listed in `docs/pass5-brief.md` Part 3 (A4), and the rule is in
  `TEMPLATE.md` under *One home per mechanism*.
- **Do not rewrite the page.** Report; the session decides; the owner judges.
- **Cover the whole page.** A report that stops early says where.

### What to report

A single markdown report in this shape. Nothing else.

```
## Ownership
- <mechanism, in five words> — here L<n> "<sentence>"; also `<page>`:L<n> "<sentence>"
  owner: <page> — because <the rule that decides it>; the other keeps: <one sentence, or nothing>
  adds: <what the losing explanation says that the owner lacks, or "nothing">

## Seams
- L<n> — assumes <term/mechanism> without a link; explained at `<page>`#<anchor>
- L<n> — links `<page>` for <thing>; the thing is at `<other page>`#<anchor>
- L<n> — hands forward to `<page>`, which does not <explain it / say so>
- L<n> — link into a later part (<page>); paid off there at L<n> | not paid off

## Through-lines
- <name> — retold at L<n>–L<n>: "<first sentence>" — adds <thing> | adds nothing

## Coverage
- in scope, unnamed: `<Class>` (<lines>) — <where on this page it belongs, one line>
- named, unexplained anywhere: `<Class>` L<n>
- a family the page's pattern covers: <sub-package> — <one sentence>
- on this page, another part's: L<n>–L<n> <what> — belongs to `<page>`

## Moves
- <recommendation> — <why, one sentence>

## Summariser drift
- `<landing page | lectures | glossary | introduction>`:L<n> says "<…>"; the page says "<…>" at L<n>

## Suspected errors
- L<n> — "<sentence>" — <why you doubt it>

## Could not judge
- <what, and why>
```

---

## Part 2 — The session runbook

One session = one part (Part II may take two; Parts I and II share session
B), on Opus. Every step is a command or a rule; the judgement is in steps 6
and 7.

### 1. Read

[plan.md](plan.md) (the charter and this session's line in Part 4 below),
`CLAUDE.md`, this file whole, and the part's landing page. Then the part's
queue, which is what earlier passes already know about it:

```
python tools/pass5_queue.py --kind book --part world
```

Grep the part for `<!-- Q:` — the owner's questions — and answer each in the
prose before the session ends.

### 2. Generate the prompts

```
python tools/pass5_prompts.py --part world --out <scratchpad>/pass5-world
```

One file per page, `<part>--<slug>.prompt.md`, plus `_part-coverage-<part>.md`
and `_part-notes.md`. Read those two yourself: the coverage report is the
part's population, and routing its rows to pages is the session's job; the
part-wide notes name no page and are the session's to place. The frame session
uses `--part frame` and `--part reference`.

### 3. Launch

One background agent per page, all at once, on Opus. The prompt is one line:
*Read `<prompt file>` and do what it says; the page is at `<path>`. Write your
report to `<scratchpad>/pass5-<part>/<slug>.report.md`.* Reports are not
committed. Brief per page, never per part.

### 4. Read the part whole while they run

**Read the part end to end in watching order**, in one sitting, before
changing anything — this is the first pass that can, because the facts are
settled, and it is the reading none of the thirty sessions did. Keep a list
as you go: what the part argues (one sentence — it becomes the landing page's
argument), where you met a term before its definition, where two pages told
you the same thing, what you expected the part to explain and it did not.
Then run the two mechanical checks for the part:

```
python tools/check_deps.py                 # the landing page against the lecture map and the figure
python tools/check_links.py --inbound src/systems/<part>/README.md
```

### 5. Audit the reports

Every finding you act on is re-derived by reading both pages yourself. The
agents have no source, so their *Suspected errors* are opinions: for each,
open the decompile, decide, and if the page is wrong fix it and log the
correction in [pass9.md](pass9.md) the way a pass-4 session did (what the page
said, what the decompile says, file and line). Take nothing else on trust
either — the duplication report ranks by shared names, and shared names are
often a link doing its job.

### 6. Decide, under the rulings

For each duplicate: the owner, by the ownership rule in Part 3; the other page
keeps one sentence and a link to the owner's anchor. For each seam: the link,
at first use, pointing the right way. For each through-line retold: cut it to
a citation, unless it adds something, in which case move the addition to the
owner. For each coverage row: a sentence, a section, a Reference row or a
`gen_reference.py` view; a page only where the part's argument has a hole,
and then a page that reads as one lecture's notes. For each move: done or
ruled out, in writing, this session — after pass 5 no page moves again.

### 7. Act

- **Moves** change `SUMMARY.md`, the landing page, `lectures.md`, the
  glossary's owner links and `book.toml`'s redirects in **one commit**, and
  keep every old URL.
- **The landing page** is rewritten last, to the role in Part 3, from the pages
  as they now stand; its size sentence becomes
  `{{#include ../../generated/part-<dir>.md}}` and no landing page hand-counts
  again.
- **The summarisers** are re-synced: the part's section of `lectures.md`, the
  glossary entries that point into the part, the Reference front page's
  *parts* column if the part's Reference use changed.
- **The part's Reference pages** are the session's too — each hand-kept
  Reference page is kept by the part whose landing page points at it — and
  the completeness findings pass 4's close logged against them
  ([pass5.md](pass5.md), session O) are this session's coverage work.
- Nothing is dropped except by moving it or logging the cut with its reason.
  Nothing on a page is reshaped for its own sake (pass 6), no figure is redrawn
  for legibility (pass 7), no sentence is polished (pass 8); a finding of those
  kinds found on the way goes to [pass5.md](pass5.md) tagged `[kind=lecture]`,
  `[kind=figure]` or `[kind=voice]`.

### 8. Verify and ship

```
python tools/verify_names.py
node tools/check_mermaid.js
python tools/check_lanes.py --strict
python tools/check_deps.py
python tools/check_links.py --quiet
mdbook build
git add <your files, by name> && git commit -F <message file>     # "pass 5, session X — Part N: <summary>"
tools/deploy.sh
```

Run `verify_names.py` after each page you touch, not after all of them.
Commit your own files by name, never `add -A`.

### 9. Record

- [pass5.md](pass5.md): strike (`~~…~~`) each book-kind entry settled, with a
  word saying how (done · overtaken · ruled out and why); tag the entries the
  tool guessed wrong; append what the reading raised for passes 6 to 8,
  tagged by kind.
- [pass9.md](pass9.md): the session's entry — every page rewritten, every
  claim introduced (a moved paragraph, a new link's implied claim, a landing
  page's argument, a section added for coverage), every correction with file
  and line.
- [pass3.md](pass3.md) §7: strike each coverage entry discharged, carry each
  ruled out with the reason.
- [plan.md](plan.md): the session log line, and the schedule line ticked.

---

## Part 3 — Session A: the standard

*Done 2026-09-05. Session A makes the rulings once so that thirteen part
sessions apply them rather than re-deciding them. What follows is what it
ruled, not what it was asked; where it amended the planning session's draft
the amendment is marked. Its edits landed in `TEMPLATE.md` (A1, A2),
`src/systems/commands/README.md` (the exemplar), `src/lectures.md` and
`src/SUMMARY.md` (A5), and `tools/check_deps.py` and
`tools/verify_names.py` (the two checks A5 turned into gates).*

### A1. The ownership rule — in `TEMPLATE.md`, under *One home per mechanism*

The planning session's draft stands, with three amendments.

**Amendment 1 — the tie-break is a tie-break.** The draft read as though the
earlier part owned a shared mechanism. It does not: the first rule is *the
page whose scenario the mechanism is the answer to*, and the earlier part
decides only when that leaves a tie. The counter-example is in the book
already — the prediction ledger belongs to `client/prediction-and-acks`
though Part V meets it first, because the block that appears and then
disappears is that page's whole scenario, and the two circular cuts (A5)
exist precisely so it can. The four rules are now numbered in priority
order: the scenario · the figure, within a part · vocabulary owns *is* and a
trace owns *happens* · the earlier part, last.

**Amendment 2 — the Reference rule binds both ways.** The draft bound the
Reference page (an enumeration, never an explanation); it now also binds the
lecture, which names the three or four rows its scenario touches and links
the rest and never reproduces the catalogue. That is the rule the
`entity-rendering` ↔ `submit-phases` and `density-functions` ↔
`density-function-nodes` pairs are decided under (sessions K and L).

**Amendment 3 — three rules under *a summariser never explains*.** A
summariser is never a fact's only home; where a summariser disagrees with
its page the page wins and the summariser is corrected in the same session,
after the page; and where both say the same thing, **the summariser is the
copy that gets shorter**. The third is new, and it is what A5's blurb ruling
applies.

Added beside them: **a pair the book declares stays a pair** (A4's list),
and **the citation form** as its own subsection, because the rule "one
sentence and a link" was silent on what the link points at.

### A2. The landing page's role — in `TEMPLATE.md`, under *The landing page*

Six things in order — the argument · the size · the shape · *before you
start* · *watch in this order* · the Reference it uses — then the rules
footer. Three rulings inside it:

**The size is conditional, and never hand-counted.** The charter's
requirement is that no landing page hand-counts; it does not follow that
every landing page carries a number. Three do today (XI, XII, XIII) and each
uses size *as* part of its argument. A part whose size is not part of its
argument says nothing and leaves the number to the atlas, whose
`maps/packages.md` carries the per-part table and is generated. Where a
landing page does state a size it is
`{{#include ../../generated/part-<dir>.md}}` and the prose names the
packages the way `src/generated/parts.md` does.

**The blurb has one home: *watch in this order*.** `SUMMARY.md` copies the
order, `lectures.md` copies the order and adds only what is about the order,
and neither repeats the line. This is A5's blurb ruling stated from the
landing page's side.

**The budget is measured, not wished.** "Under a hundred lines" was true of
three of the thirteen pages and of neither the best-argued one nor the
exemplar, so it was not a budget. Measured without the watch order — which
is one blurb per page and grows with the part — the thirteen run 45 · 61 ·
71 · 84 · 89 · 89 · 90 · 94 · 95 · 104 · 106 · 124 · 144. **The rule is
therefore about a hundred lines plus the watch order**, and it names two
outliers rather than eleven: `rendering/README` (124) and `worldgen/README`
(144), for sessions K and L to judge.

**The exemplar is `src/systems/commands/README.md`**, rewritten this session
to the role: the argument now ends on the claim rather than on the list of
four systems; the size sentence is the include (its hand-count said 473
classes and 43,900 lines against the mapping's 470 and 43,126, because it
counted a different set of packages); the scope statement — what the part
declines — moved up beside the size, where it belongs; and one sentence was
cut under A1 rather than moved, the statistics-and-the-data-fixer claim,
because `anatomy/what-this-book-skips`:252 owns it and the landing page
already links there. The three *before you start* links that had an owner
section to land on now carry its anchor, which is the citation form (A3).

### A3. The through-lines: owners, anchors and the citation form

The owners the planning session proposed are confirmed; every anchor below
was checked against the built page's heading id.

| through-line | owner and anchor | the other pages' form |
|---|---|---|
| the tick and its phases | `server/server-tick`<br>`#what-minecraftservertickchildren-runs-and-in-what-order` | one clause naming the phase, then *(the server tick)* with the anchor. The event loop is the same page at `#the-event-loop-and-what-a-ticks-spare-time-buys`. |
| the four threads | `anatomy/anatomy`<br>`#four-threads-worth-memorising` | name the thread and link; the roster is `reference/threads#the-threads-a-lecture-leans-on` and no page reproduces it |
| the wire and the hop | `networking/the-connection`<br>`#the-pipeline-in-both-directions` for the wire, `#one-packet-there-and-one-back` for the hop (session I: the anchor A3 first gave — `#the-threads-underneath-it` — exists but is about `EventLoopGroupHolder`'s groups, not the hop; three pages had cited it) | *…deferred to the game thread (the connection)* — one clause, never the mechanism |
| authority and prediction | authority: `entities/authority`<br>`#five-predicates-and-the-final-one-the-other-four-hang-off`<br>prediction: `client/prediction-and-acks`<br>`#two-state-machines-running-against-each-other` | the premise in one sentence in the page's own terms, then the link. Part V's two click pages are the declared exception (A4). |
| the registry freeze and the reload | freeze: `foundations/identifiers-and-registries`<br>`#the-freeze-rule-stated`<br>reload: `foundations/resource-system`<br>`#reload-the-same-pipeline-on-the-server` | *…because the registry is frozen by then (the freeze rule)* — the consequence here, the rule there |
| the data-driven type pattern | `foundations/data-driven-types`<br>`#the-idea-stated-once` | name the instance, link the pattern; the page that owns the instance never restates the pattern |
| the ledger | `client/prediction-and-acks`<br>`#the-four-writes` | the sequence number and what it buys, in one sentence; the four writes are the owner's |

**Lecture zero is `anatomy/anatomy`, and no new page is written.** It already
carries the four threads (24 term hits, the most of any page that is not
about a thread dying), the two loops and the wire, and the introduction stays
short. The tick, authority, prediction, the freeze, the reload, the pattern
and the ledger each belong to a page inside a part, and a reader meets each
where it does work.

**The citation form, stated once** (and copied into `TEMPLATE.md`): the
parenthetical link at the end of the sentence that needs it, carrying **the
anchor of the section that is the answer**. The book already writes the
parenthetical — 34 inbound links to `server-tick` from 26 pages, almost all
in that shape — and what pass 5 adds is the anchor, so that a reader lands on
the paragraph rather than the top of a four-hundred-line page. **The eight
owner pages above take 169 inbound links, and three carried an anchor before
this session** (`check_links.py --inbound` prints them); the exemplar added
three more. That is the work, and it is a part session's, one link at a
time.

**Measured spread, for the part sessions** (`pass5_dups.py --terms`; a hit is
a mention, not a retelling): tick 26 pages · threads 72 · wire and hop 28 ·
authority and prediction 35 · freeze and reload 39 · the pattern 11 · the
ledger 18. Two notes fall out of the measurement and are pass 8's, logged in
[pass5.md](pass5.md): *ledger* is used for three unrelated things (the
prediction ledger; `server-tick`'s three closing ledgers; a metaphor on two
`items/` pages), and *the data-driven type pattern*'s terms are ordinary
words, so its 11 is a floor and not a count.

### A4. The duplication report, routed

**The routing rule stands**, with one addition: a cross-part pair is
resolved by the later part's session; a within-part pair by the part's
session; a pair with a Reference page by the part whose landing page points
at that Reference page; and **a pair between the frame (`lectures.md`, a
landing page, the glossary) and a system page is the part's session too** —
the landing page belongs to the part, and session O re-syncs the frame at
the close. The routed list in Part 4 stands as the planning session wrote
it.

**The declared pairs — checked, not merged.** These are the pairs a landing
page or `lectures.md` calls one lecture in two halves, a sequel, or a pair to
keep together. A shared preamble between them is deliberate; the finding is a
*drift between the two copies*, never the copy. No session merges one of
these without saying so in [pass9.md](pass9.md).

| pair | declared by |
|---|---|
| `server-tick` ↔ `server-level-tick` | `lectures.md` III: *never apart from it* — ~~the landing page does not say it~~; **session C moved it**, and `server/README`:47 now declares the pair (session O checked the thirteen) |
| `block-interaction` ↔ `block-breaking` | V: *one lecture in two halves*, and the figure's own edge label |
| `synched-entity-data` ↔ `attributes` | `lectures.md` VI: *the contrast between the two is the lesson* — ~~the landing page does not say it~~; **session F moved it**, and `entities/README`:73 now declares the pair (session O checked the thirteen) |
| `ai-goals-and-brains` ↔ `pathfinding` | VI: *the other half of the same lecture* |
| `enchantments` ↔ `enchanting` | VII: *the pair to keep together* |
| `contexts-and-predicates` ↔ `loot-tables` | VII: *the other pair* |
| `player-anatomy` ↔ `the-two-phase-tick` | VIII: *the pair to keep together* |
| `the-sword-swing` ↔ `the-spear` | VIII: *the spear is the sword swing's sequel* |
| `the-connection` ↔ `packets-and-stream-codecs` | IX: *one lecture in two halves* |
| `the-client-level` ↔ `prediction-and-acks` | X: *a pair — the ledger lives on `ClientLevel`* |
| `gui-and-screens` → `the-gui-render-tree` → `text-and-fonts` → `hud` | X: *the GUI stack, watched together* |
| `sound-engine` ↔ `what-makes-a-sound` | X: *the two halves of sound* |
| `visibility-and-the-frame-graph` ↔ `section-meshing` | XI: *one journey seen from its two ends* |
| `entity-rendering` ↔ `block-entity-rendering` | XI: *the second written as the differences from the first* |
| Part V's two click pages ↔ `prediction-and-acks` | V: both open with *the same four-sentence statement of the contract*, which is the V ↔ X cut (A5) |

**A finding that falls out of building the list**: a part's ordering
paragraph is on its landing page *and* in its section of `lectures.md`, and
the two have already drifted, in both directions. The landing page has pairs
the map does not (Part X's ten and eleven, the two halves of sound; Part
VII's seven and eight; Part VIII's six and seven); the map has pairs the
landing page does not (Part III's *never apart from it*, Part VI's
*attributes* against *synched entity data* — **both moved to the landing page
by sessions C and F**, checked at the close); and `lectures.md`:296 and
`rendering/README`:140 were near-verbatim until this session shortened the
first. Under A1 the ordering claim belongs to the landing page and the
summariser is the copy that gets shorter, so a claim the map has and the
page lacks **moves to the page**. Each part session re-syncs its own at the
end; session O checks the thirteen.

### A5. The frame's own seams

**The dependency table has a rule now, and a gate.** The rule the table was
groping for is mechanical: *a page two or more landing pages name under
**before you start***, less the three every part assumes — `anatomy`,
`codecs-nbt-json` and `identifiers-and-registries` — which are exactly the
boxes the figure draws without edges, for the reason the paragraph above it
already gives. Membership by that rule loses `blocks-and-states`,
`contexts-and-predicates` and `the-client-loop` (one dependent part each,
and the last two are named in the paragraph below the table instead) and
gains `resource-system` (III, VII, XI), `data-driven-types` (XII, XIII) and
`text-components` (IX, X). Nine rows and ten pages, as before.
`check_deps.py` now fails on a page that qualifies and has no row, on a row
that does not qualify, and on a universal that takes a row, and
`check_deps.py --probe` proves both new checks on synthetic input — the
first probe on a tool built before pass 5, added because these two checks
are the session's own work and a tool is suspected first.

**Part IV's three orders: the landing page's *watch in this order* is the
book's order, and `SUMMARY.md` and `lectures.md` follow it.** That is the
general rule; applied, it moves *environment attributes and timelines* to
first in Part IV's sidebar block, which is where the part's own landing page
and the lecture map have always had it. `check_deps.py` already forced
`lectures.md` to agree with the landing page; it now forces `SUMMARY.md` too,
and Part IV was the only part of the thirteen where they differed. Session D
may re-judge the order itself when it reads the part whole; it may not leave
the three disagreeing.

**The lecture map keeps the order and drops the blurbs.** The planning
session's recommendation is taken. `lectures.md` carried a one-line
description of each of the 102 pages, in different words from the same
description on the part's landing page: two copies of one claim, which is
the drift machine pass 4 found errors in, and 102 of them. The page's own
first paragraph says its subject is the *ordering*, so what stays is
everything about the order — each part's shape paragraph, the ordering
claims that were inside the blurbs (*watched immediately after and never
apart from it*, *assumes scheduled ticks only lightly*, *Part XII is the
cargo on this conveyor*), the cross-part dependency paragraphs, the graph
and the table — and what goes is the description of content, which the
landing page owns. 662 lines to 469, and a new second paragraph tells the
reader where the descriptions are. Two open queue entries were settled by the
cut and are struck as overtaken; one published sentence that named a pass
number went with it.

**The two circular cuts stand, re-judged with the pages open.**
III ↔ IV is *better* cut than it was: the environment page is now the first
lecture of Part IV in all three orders, so the one departure a straight-
through viewer makes is as small as it can be, and the ranges half is cut by
definition — which under A1 means `server-level-tick`'s two sentences must
read as a citation of `tickets-and-loading`, not as a second explanation
(session D). V ↔ X stands unchanged, and A4 records the shared preamble as a
declared pair rather than a duplicate.

**The glossary: one owner per sense.** An entry has one owner link. Where a
word names two different things the entry says so and gives one link per
*sense* — which is what `Component`, `Level` and `Tick` already do, and they
keep both links. Where one thing is explained on a page and enumerated on a
Reference page, the owner is the page that explains and the Reference page is
named in the sentence as where the list is: that reduces `Render state`,
`Quart` and `Submit node` to one owner each. **Yes, the glossary
disambiguates**, but only for a word the corpus itself uses in more than one
sense, and the entry *is* the disambiguation: one line per sense, each with
the page that uses it that way. *Occlusion* (four senses over nine pages, no
owner) is therefore written, by session N, after the parts have settled — as
are the five headwords the corpus does not use and `Blending data` →
`BlendingData`, under the page's own class-name rule.

**The class index labels a landing page by its title.** Eleven distinct
pages rendered as *README*, three of them in one row. `verify_names.py`'s
index now labels any `README.md` with its own `#` heading — *VI · Entities*,
*Reference*, *The atlas* — which is general, self-maintaining and needs no
table in the tool.

**The introduction's gate sentence is right.** *Verified means tested* now
names all five gates — names, diagrams, lanes, links and anchors, and the
landing-page/lecture-map/figure check — and says narrowly what the guarantee
covers. No change.

**The licence footer stays doubled on the introduction.** The queue entry
proposed having `site-footer.js` skip the introduction. Ruled out: the JS
footer never reaches `llms-full.txt`, the prose does, and duplication in
favour of the licence being visible is the right way to err. Struck with the
reason.

### A6. What session A did not do

It did not read a part, did not rewrite a system page, and made no ruling a
part session could make better with the pages open. Three questions it was
handed were left where they belong: `reference/README.md`'s hand-written
*parts* column (session N — it is a Reference page, not a frame ruling), the
lane key's 45 unclaimed rows (pass 7 prunes lanes, and the key is only
authority until then), and the two-lanes-for-one-class case, `RCPL` and
`CPL`, which the chat figure needs and pass 7 owns.

## Part 4 — The schedule

Sessions B–N run in sidebar order, one part each, after A; O closes. The
numbers are what the tools found on 2026-09-05, before any session ran — they
say where the work is, and no count is a target.

**Coverage by part** (`pass5_coverage.py --all --summary`; the population is
the atlas's `PARTS` mapping, which is the *where each part lives* table on
`maps/packages.md`, now generated):

| part | classes | lines | named on a page of the part | named elsewhere | named nowhere | nowhere, lines | named, by lines |
|---|---:|---:|---:|---:|---:|---:|---:|
| I · anatomy | 6 | 6,766 | 2 | 4 | 0 | 0 | 100% |
| II · foundations | 422 | 47,098 | 148 | 99 | 173 | 12,942 | 72% |
| III · server | 90 | 21,759 | 47 | 18 | 25 | 1,951 | 91% |
| IV · world | 202 | 30,886 | 145 | 29 | 27 | 1,152 | 96% |
| V · blocks | 466 | 60,355 | 63 | 60 | 343 | 36,232 | 40% |
| VI · entities | 674 | 110,083 | 208 | 49 | 417 | 43,436 | 61% |
| VII · items | 483 | 45,193 | 186 | 57 | 240 | 16,426 | 64% |
| VIII · player | 25 | 8,119 | 15 | 4 | 6 | 277 | 97% |
| IX · networking | 471 | 39,334 | 196 | 151 | 120 | 6,002 | 84% |
| X · client | 627 | 93,392 | 152 | 122 | 346 | 33,137 | 64% |
| XI · rendering | 1,121 | 92,480 | 314 | 54 | 743 | 43,158 | 53% |
| XII · worldgen | 423 | 45,637 | 199 | 31 | 189 | 10,855 | 76% |
| XIII · commands | 439 | 43,002 | 211 | 31 | 193 | 12,502 | 69% |

How to read it: a class being named is a floor, not coverage, and a low
percentage is not by itself a gap. Parts V, VI, X and XI are low because
their packages are families — 343 unnamed Part V classes are mostly one
`Block` subclass each, which `blocks-and-states` covers as a pattern. The gap
the tool is for is a **mechanism** no page names: a whole sub-package
(`world/level/block/entity` has sixty block entities and one page about the
pattern), a large class with behaviour of its own (`SculkSpreader`,
`RailState`, `MultifaceSpreader`, `BlockPattern` in Part V), or a class the
book leans on that only Reference names (`WorldBorder`, 573 lines, named on
`level-data-and-rules` and `server-level-tick` only). Each part's report
lists the sub-packages by unnamed lines for exactly this.

**The queue by kind** (`pass5_queue.py --summary`): 348 open units, of which
114 are pass 5's, 75 pass 6's, 28 pass 7's, 131 pass 8's; 185 of the 348 are
guesses the tool marks `?`, and each part session tags its own as it reads
them.

**The duplication report, routed** (`pass5_dups.py --summary`; score is the
sum of 1/(pages carrying it) over shared names on at most six pages; the
session named resolves the pair, by A4's rule):

| pair | score | resolved by |
|---|---:|---|
| `foundations/data-components` ↔ `items/items-and-stacks` | 17.00 | G (VII): the prototype and the patch — who owns *what a component is* against *what a stack holds* |
| `foundations/identifiers-and-registries` ↔ `foundations/tags` | 12.45 | B (II): the freeze and the tag rebind |
| `worldgen/density-functions` ↔ `reference/density-function-nodes` | 11.92 | L (XII): the catalogue's preamble against the lecture |
| `entities/damage-and-death` ↔ `reference/non-living-damage` | 11.62 | F (VI) |
| `foundations/codecs-nbt-json` ↔ `networking/packets-and-stream-codecs` | 11.57 | I (IX): where `ByteBufCodecs` and the NBT bridge live |
| `server/how-a-server-dies` ↔ `server/starting-a-server` | 11.43 | C (III): one skeleton forwards and backwards (the lock, the halt, the save) |
| `foundations/data-driven-types` ↔ `items/loot-tables` | 11.08 | G (VII) |
| `entities/ai-goals-and-brains` ↔ `world/points-of-interest` | 10.95 | F (VI): the bed claim from both ends |
| `networking/protocol-phases` ↔ `server/players-and-sessions` | 10.27 | I (IX): the configuration tasks and the join |
| `blocks/diodes-and-observers` ↔ `world/scheduled-ticks` | 10.00 | E (V): the repeater's booking is told twice, nearly verbatim (`diodes-and-observers`:119 ↔ `scheduled-ticks`:263) |
| `networking/what-the-client-is-told` ↔ `world/tickets-and-loading` | 9.48 | I (IX): the send table |
| `entities/entity-anatomy` ↔ `entities/synched-entity-data` | 9.32 | F (VI) |
| `entities/entity-lifecycle` ↔ `server/server-level-tick` | 9.23 | F (VI): the spawn cascade against the tick's spawning phase |
| `networking/packets-and-stream-codecs` ↔ `networking/protocol-phases` | 9.17 | I (IX) |
| `foundations/data-driven-types` ↔ `items/contexts-and-predicates` | 9.15 | G (VII) |
| `server/server-level-tick` ↔ `world/scheduled-ticks` | 8.67 | D (IV) |
| `items/using-an-item` ↔ `player/hunger-and-experience` | 8.48 | H (VIII): the meal from both ends |
| `world/chunk-generation-pipeline` ↔ `world/tickets-and-loading` | 8.30 | D (IV) |
| `rendering/lightmap-fog-and-sky` ↔ `world/environment-attributes-and-timelines` | 8.27 | K (XI) |
| `entities/entity-anatomy` ↔ `entities/entity-lifecycle` | 8.12 | F (VI): `EntityType.create`'s gates, the charter's named duplicate |
| `items/contexts-and-predicates` ↔ `items/loot-tables` | 8.00 | G (VII) |
| `client/input-and-keybinds` ↔ `player/input-to-movement` | 7.73 | J (X): `KeyMapping` from both sides |
| `world/chunk-anatomy` ↔ `world/chunk-generation-pipeline` | 7.40 | D (IV) |
| `player/the-spear` ↔ `player/the-sword-swing` | 7.40 | H (VIII): deliberate sequel — check, do not merge |
| `server/starting-a-server` ↔ `reference/level-data-and-rules` | 7.33 | C (III) |
| `reference/level-data-and-rules` ↔ `reference/naming-drift` | 7.32 | N (Reference): a naming-drift row is not an explanation |
| `foundations/data-driven-types` ↔ `foundations/identifiers-and-registries` | 7.07 | B (II) |
| `entities/synched-entity-data` ↔ `networking/what-the-client-is-told` | 6.97 | I (IX) |
| `rendering/blaze3d` ↔ `reference/naming-drift` | 6.95 | K (XI) |
| `networking/packets-and-stream-codecs` ↔ `networking/the-connection` · `protocol-phases` ↔ `the-connection` | 6.87 · 6.85 | I (IX): one lecture in two halves, by the lecture map's own account |
| `world/chunk-anatomy` ↔ `world/lighting` | 6.85 | D (IV) |
| `entities/authority` ↔ `entities/movement-and-collision` | 6.70 | F (VI) |
| `server/server-level-tick` ↔ `world/tickets-and-loading` | 6.53 | D (IV): the three ranges, defined on the tick page by the circular cut |
| `blocks/block-breaking` ↔ `player/player-anatomy` | 6.42 | H (VIII): `ServerPlayerGameMode` — Part III's homeless paragraph lands here |
| `server/how-a-server-dies` ↔ `world/chunk-storage` | 6.35 | D (IV): the save path from both ends |
| `items/containers-and-menus` ↔ `items/recipes` | 6.12 | G (VII) |
| `blocks/block-entities` ↔ `world/chunk-anatomy` | 6.10 | E (V): the ticker wrappers — `chunk-anatomy`'s drafter already named its *double indirection* subsection as `block-entities` material |
| `anatomy/anatomy` ↔ `reference/threads` | 6.07 | B (I): the thread table is Reference's; the page keeps the four |
| `server/how-a-server-dies` ↔ `server/server-tick` | 6.03 | C (III) |

Twin sentences across pages (near-verbatim, not summariser echoes): 58 pairs;
the top ones are the two click lectures' shared preamble (deliberate), the
repeater's booking (above), `entity-rendering`:241 ↔ `submit-phases`:31 on
the merge rule, `hud`:58 ↔ `hud-elements`:69 on the deferred subtitles,
`density-functions`:225 ↔ `density-function-nodes`:122 on the noise bounds,
`input-to-movement`:28 ↔ `the-two-phase-tick`:119 on the fall-damage gate,
and `codecs-nbt-json`:185 ↔ `packets-and-stream-codecs`:128 on the NBT
bridge. Each page's prompt file lists its own.

### The sessions

| session | part | pages | queue (book) | named nowhere | the charter's named items, and what the tools add |
|---|---|---:|---:|---:|---|
| **A** — *done 2026-09-05* | the standard | — | 24 (frame + Reference) | — | Part 3 above, whole. Five queue entries struck, six findings logged back to [pass5.md](pass5.md), two checks added to `check_deps.py`. |
| **B** — *done 2026-09-05* | I · Anatomy, II · Foundations | 2 + 7 | 3 + 4 | 0 + 173 | The owners of four through-lines live here (A3). `anatomy` ↔ `reference/threads` (6.07): the page keeps the four threads, the table is Reference's. **Feature flags and `FeatureFlagSet`** (§7): backticked on twelve pages, explained on none — a section on `identifiers-and-registries` (it gates registry contents) or `resource-system`; `world/flag` is in Part II's packages now. Part II's coverage is 173 classes / 12.9k lines: read the sub-package table (`util` is the toolbox every part uses; `core/component` and `server/packs` are the part's own). `identifiers-and-registries` ↔ `tags` (12.45) and ↔ `data-driven-types` (7.07). `text-components` ↔ `chat-and-signing` twins at 270/235. The *not X but Y* and the second person are pass 8's and 6's; leave them. |
| **C** — *done 2026-09-05* | III · The server | 5 | 6 | 25 | **`how-a-server-dies`' two subjects** (the three endings; the durability page inside it): section or page, decided. `how-a-server-dies` ↔ `starting-a-server` (11.43) and ↔ `server-tick` (6.03). **The three homeless items** from `players-and-sessions`: the `ServerPlayerGameMode` paragraph (→ `player-anatomy`, session H receives it), the view-distance packets (→ `what-the-client-is-told`, session I), `PlayerDataStorage`'s rescue (→ `level-data-and-rules`, session D). `server-tick`'s packet-drain paragraph: point forward to the event-loop section instead of explaining in place. The event-loop machinery (`BlockableEventLoop`, `TickTask`, `managedBlock`) — four parts cite it; confirm `server-tick` owns it and the others cite. **The abstract `Level`** (§7): decide with session D whether it is a section of `server-level-tick`, of `chunk-anatomy`, or a Reference page; the glossary asserts it with nowhere to send the reader. Coverage: `ServerBossEvent` is Part XIII's (session M); `DemoMode`, `ChunkResult`, `ServerEntityGetter` are this part's to place or decline. | **Done:** all six pages rewritten; `how-a-server-dies`' durability section ruled a section (it is the comparison table's payoff) after the autosave, the per-chunk spacing and `session.lock` went to their owners; the three homeless items all found settled (two before pass 5, `PlayerDataStorage`'s rescue written here); the event loop confirmed `server-tick`'s, with the crash relay and the stopped-server doors cut to citations of `how-a-server-dies`; the abstract `Level` written as a paragraph on `server-level-tick` (§7 discharged) and `ServerBossEvent` left to M, `ChunkResult` and `PlayerMap` routed to D, `DemoMode` to H, `ServerEntityGetter` to F. Plus **six corrections**, four of them one page disagreeing with another; the `server/players` stored-user-list family and `CachedUserNameToIdResolver` named; the tick's profiler zone names defined for the ten pages that cite them; twenty-eight anchors.
| **D** — *done 2026-09-05* | IV · The world | 10 | 14 | 27 | **Part IV's three orders**, applied as session A ruled. **`chunk-storage`'s proposed hand-off** of the null-parse branch and `ChunkMap.handleChunkLoadFailure` to `chunk-generation-pipeline`: do it or drop it. The five within-part pairs (`chunk-generation-pipeline` ↔ `tickets-and-loading` 8.30, `chunk-anatomy` ↔ `chunk-generation-pipeline` 7.40, `chunk-anatomy` ↔ `lighting` 6.85) and the three with Part III (`server-level-tick` ↔ `scheduled-ticks` 8.67, ↔ `tickets-and-loading` 6.53, `how-a-server-dies` ↔ `chunk-storage` 6.35): the tick page defines the three ranges by the circular cut and cites the rest. `points-of-interest`'s missing sentence on `PoiManager.isVillageCenter` reading through the non-loading `SectionStorage.get` — a fact, so decompile open. `WorldBorder` (573 lines) is named only on `level-data-and-rules` and `server-level-tick`: a home, or a declared Reference-only. `level-data-and-rules` (this part's Reference page): `DirectoryLock`, `LevelVersion`, `LevelSummary`'s states, the four `LevelResource` paths, the per-player files, `MinecraftServer.saveAllChunks`, and the seven table rows with no prose (pass-4 session O's list). Receives `PlayerDataStorage`'s rescue from C. The landing page's *four side-systems* against five pages off the conveyor. | **Done:** all eleven pages and `reference/level-data-and-rules` rewritten; Part IV's three orders left as session A set them, re-judged with the part read whole and found right; `chunk-storage`'s null-parse branch and `ChunkMap.handleChunkLoadFailure` **moved** to `chunk-generation-pipeline` (the proposal settled), and the `SavedDataStorage` write path moved the other way, off the Reference shelf onto `chunk-storage`; all eight named duplication pairs resolved, of which the largest cut was the chunk-batch pacing going back to Part IX; `points-of-interest` gained the `SectionStorage.get` fact as its own callout — a village is made of loaded sections only; **`WorldBorder` declared Reference-only** in both places with the reason, and the ruling written into §7; `level-data-and-rules` given its four reader-parts, its hand-copied game-rule defaults dropped (`gamerules.md` generates them) and its `DimensionType` drift note cut to a citation, the third copy of three. Plus **nine corrections**, five of them page-against-page; six suspicions re-derived and found sound; thirty-seven anchors; and the seventeenth tool bug of the project — `check_links.py` could not see a wrapped link, so 243 links had never been checked and the gate called this session's own broken anchor clean. |
| **E** — *done 2026-09-05* | V · Blocks | 7 | 9 | 343 | **The two update channels**: owned once by `blocks-and-states`; check the six linking pages have not started re-explaining it (the duplication that produced three pass-2 errors). **`signal-and-dust`'s two subjects** (the lever; the second evaluator) and the staircase's *why* said twice on it. **`block-entities` as the part's odd page**: the landing page's fourth clause, or the cleaner reading (a hub, two click lectures, a redstone trio, one page about state that outgrew a block state). `diodes-and-observers` ↔ `scheduled-ticks` (10.00; the repeater's booking near-verbatim at 119/263). `block-entities` ↔ `chunk-anatomy` (6.10): the ticker wrappers move here. Coverage 343 classes / 36k lines: the sub-package table — sixty block entities under one pattern page (a `gen_reference.py` view of block entities and their tickers is the cheap answer), and the large single-mechanism classes (`SculkSpreader`, `RailState`, `MultifaceSpreader`, `BlockPattern`, `BaseFireBlock`) named or declined in a sentence each. The block-event users (§7) stay a paragraph on `pistons-and-block-events`. `block-update-flags` is this part's Reference page. | **Done:** all seven pages and `reference/block-update-flags` rewritten; the two update channels checked on all six spokes and **one had re-explained them** (`block-interaction`, cut to the door's consequence and the anchor); `signal-and-dust`'s second evaluator **ruled to stay** as the page's counterfactual and its lever ruled the page's, with the staircase's third telling cut; `block-entities` left where it is and the landing page's fourth clause removed by rewriting the argument instead; the `diodes-and-observers` ↔ `scheduled-ticks` pair cut on the Part IV side, because rule 1 gives all three bold paragraphs to the diode page; the ticker wrappers found already cut by session D and the anchor checked. Coverage answered as five family sentences (the three `block/state/` sub-packages, the redstone sources, the seven block-event raisers, the `block/entity` family, the use-hook family with its count restored — 25 and 52) plus a *where the part stops* section; the hopper, the sculk spreader, the structure and command blocks and four state machines declared too big for a sentence and sent to §7. The block-event users' §7 entry **discharged, with its count corrected to three blocks**. Plus **six corrections**, four page-against-page; seven suspicions re-derived and found sound; thirty-seven anchors and one link repointed at the right page. |
| **F** — *done 2026-09-05* | VI · Entities | 9 | 7 | 417 | **`EntityType.create`'s gates** on `entity-anatomy` and `entity-lifecycle` (8.12): one owner, one link. `ai-goals-and-brains` ↔ `points-of-interest` (10.95): the bed claim from both ends — Part IV owns the index, this part the behaviour. `entity-lifecycle` ↔ `server-level-tick` (9.23), `entity-anatomy` ↔ `synched-entity-data` (9.32), `authority` ↔ `movement-and-collision` (6.70), `damage-and-death` ↔ `non-living-damage` (11.62; the Reference page wants its `hurtClient` column and its `Entity.isPickable` sentence — pass-4 session O's list). **Part VI ← `chunk-anatomy`**: `entity-lifecycle` spends the chunk model throughout and links it nowhere. Homeless material (§7 and the pass-3 cuts): the fall-attribution threshold (death-message machinery — a `CombatTracker` sentence or a Reference row), the position-and-teleport family on neither `entity-anatomy` nor `authority`, `damage-and-death`'s cut *Interfaces* (`DamageTypes`, `DamageTypeTags` — a Reference view), the fortress spawn list and `Structure.spawnOverrides` and the `EntitySpawnReason` constants (§7's three `gen_reference.py` views — session N builds the views, this session says what each page cites). Coverage 417 classes: mobs are a family; the sub-packages (`ai/behavior`, `boss`, `raid`, `schedule`, `variant`) are the mechanisms to name or decline. | **Done:** all nine pages and `reference/non-living-damage` rewritten; `EntityType.create`'s gates settled to `entity-anatomy` with the spawner's consequence kept on `entity-lifecycle`; the `ai-goals-and-brains` ↔ `points-of-interest` pair cut on the Part VI side, because claiming a POI is Part IV's scenario; `entity-lifecycle` ↔ `server-level-tick` cut on the Part III side for the two caps and the spawner roster; `damage-and-death` ↔ `non-living-damage` cut on the lecture's side, and the two partitions of the same twenty-one classes reconciled to the catalogue's six; `entity-anatomy` ↔ `synched-entity-data` and `authority` ↔ `movement-and-collision` both resolved. Part VI ← `chunk-anatomy` found already paid. The homeless material placed: the fall-attribution threshold as a new section of `damage-and-death`, the position-and-teleport family declined (`Entity.absSnapTo` and `Entity.snapTo` are the last two names and belong to `entity-anatomy`, logged), the `EntitySpawnReason` and `Structure.spawnOverrides` views given their citers and the fortress list written. Plus **thirteen corrections**, eight of them page-against-page; five suspicions re-derived and found sound; sixty-nine anchors where the part had none; and the eighteenth tool bug of the project — the atlas printed four packages Parts VI and IX *include* as exclusions. |
| **G** — *done 2026-09-05* | VII · Items and inventories | 8 | 4 | 240 | **`data-components` ↔ `items-and-stacks`** (17.00, the top pair in the book): the prototype and the patch — Part II owns what a component *is*, this part what a stack *holds*; decide the line and cut to it. `data-driven-types` ↔ `loot-tables` (11.08) and ↔ `contexts-and-predicates` (9.15): the pattern page owns the pattern, these own the instances. `contexts-and-predicates` ↔ `loot-tables` (8.00), `containers-and-menus` ↔ `recipes` (6.12). **The predicate shape library** (§7: `MinMaxBounds`, `CollectionPredicate`, `EntitySubPredicate`, `DataComponentMatchers`) — a table on `advancements` today; owner here or a Reference page, decided with session M. The `Item.getUseDuration` roster (§7, lost prose): a sentence or a Reference row. `Registries.LOOT_TABLE` named once. The three enchanting facts moved from `data-components` in pass 3: confirm they landed on `enchantments`. The `Item.Properties` weapon helpers view (§7, session N builds). `enchantment-hooks` and `loot-context-params` are this part's Reference pages. | | **Done:** all eight pages and the landing page rewritten; **the top duplication pair in the book settled** — Part II owns the component system's machinery, Part VII owns the stack as an object, six mechanisms cut to a citation on the Part VII side and three moved to Part II, with the validators, `ItemStackTemplate` and `ignoreSwapAnimation` moving the other way, and `items-and-stacks` given a hook only it can say. `data-driven-types` ↔ `loot-tables` cut on the Part II side (*The run half* now stops at the object existing); `contexts-and-predicates` ↔ `loot-tables` resolved three ways (the recursion guard, the random-source order and the villager aside all to the context page, which owns `LootContext`), and `contexts-and-predicates` ↔ `enchantments`, `containers-and-menus` ↔ `recipes` and `enchanting` ↔ `enchantments` all resolved. The predicate shape library **ruled, not moved** — it stays a table on `advancements`, and the citation Part VII owed now exists. The `Item.getUseDuration` roster **written** as a sentence on `using-an-item` with the base method's three-way answer in front of it. `Registries.LOOT_TABLE` found already named, and the whole `loot-tables` half of that queue entry overtaken. The three pass-3 enchanting facts all landed — on `enchanting`, not `enchantments`, which is the brief's own claim corrected. Both Reference pages are generated and were not edited. Plus **twelve corrections**, four page-against-page and three a page against itself; seven suspicions re-derived and found sound; forty-four anchors where the part had two; seven `taught in` cells re-pointed; and a coverage answer of four families plus four declines written into §7. |
| **H** — *done 2026-09-06* | VIII · The player | 7 | 6 | 6 | Receives the `ServerPlayerGameMode` paragraph from C (`block-breaking` ↔ `player-anatomy` 6.42 is the same seam). `using-an-item` ↔ `hunger-and-experience` (8.48): the meal from both ends. `input-to-movement` ↔ `the-two-phase-tick` twins at 28/119 (the fall-damage gate) and `input-to-movement` ↔ `input-and-keybinds` (7.73, resolved by J). `the-spear` ↔ `the-sword-swing` (7.40) is a deliberate sequel: check the second cites the first. `status-effects`' `LivingEntity.effectsDirty` with no reader named, `MobEffectCategory` in *Where to look* unexplained — coverage findings. `the-spear`'s component table: complete, or the heading says which subset. | **Done:** all seven pages and the landing page rewritten, the landing page gaining a *where the part stops* the part had never had; the `ServerPlayerGameMode` paragraph found already settled (session C); `using-an-item` ↔ `hunger-and-experience` split along rule 1 rather than routed whole — `Consumable`'s field roster and the five `ConsumeEffect`s to Part VII, the `ConsumableListener` walk kept because it is the Part VIII page's own hook, and the decline of the routing rule's default written out; `UseEffects` to Part VII with its vibration half; the record-and-discard bracket and the shared hook settled between the two trunk pages, which are *not* a declared pair; the fall-damage gate and the authority preamble cut to citations on both; the spear sequel checked and left, and its component table declared a subset with the material's three named; `effectsDirty`, `MobEffectCategory`, the per-effect subclass family and the six-hundred-tick re-send all written. Plus the pass's largest move — `Player.cannotAttack` and `Player.deflectProjectile` off `reference/non-living-damage` onto `the-sword-swing`, with the sharper *was anything damaged* reading coming back the other way — and **eight corrections**, three page-against-page and two page-against-Reference, four suspicions re-derived and found sound, seventy-one anchors where the part had none, and no tool bug. |
| **I** — *done 2026-09-06* | IX · Networking | 5 | 5 | 120 | **The shape sentence** (*one wire and three passengers* against *protocol phases is the wire*), and the landing figure's arrows 3 and 4 that assert a dependency neither page uses. `codecs-nbt-json` ↔ `packets-and-stream-codecs` (11.57): where the NBT bridge lives. `protocol-phases` ↔ `players-and-sessions` (10.27): the configuration tasks and the join. `what-the-client-is-told` ↔ `tickets-and-loading` (9.48) and ↔ `synched-entity-data` (6.97): the send gates against their owners. The three within-part pairs (9.17, 6.87, 6.85): the lecture map already calls the first two one lecture in two halves. Receives the view-distance packets from C. `reference/threads`' never-hop population framed as a class rather than a runtime object. `packets` (generated) is this part's Reference page. | **Done:** all five pages and the landing page rewritten; the shape sentence decided as *the wire three times, and two things it carries*, with the figure's two unlabelled arrows redrawn to match after checking that neither target page names the phase machinery; `codecs-nbt-json` ↔ `packets-and-stream-codecs` split so that the wire's vocabulary, the trusted constants and the creative slot's three fences are Part IX's and the four-path comparison keeps only the fact that the serverbound path runs a codec for its errors; `protocol-phases` ↔ `players-and-sessions` split so that the phase edges (including the reconfigure) are Part IX's and the spawn task's internals and the admission gate are Part III's; the send table, the tracking view and the two block-entity defaults cut to citations; the three within-part pairs checked and only the play-binding and creative-filter duplicates found real. The view-distance packets from C arrived already settled; both of C's and D's remaining wrong-page citations repointed. **Seventeen corrections** (eight page-against-page, five page-against-itself), the text filter, the per-phase listener interfaces and `client/multiplayer/resolver` written, sixty new anchors, and the A3 row for *the wire and the hop* corrected because the anchor session A declared is about something else. |
| **J** — *done 2026-09-06* | X · The client | 12 | 5 | 346 | **Part X ← `anatomy/anatomy`** (`the-client-loop`'s hook contrasts the two loops and links nowhere) and **← `entities/authority`** (`the-client-level` opens on *not an authority either*). **The GUI stack watched in a different order from the one it runs in** — a move, decided. **`the-gui-render-tree`'s title** — a rename, decided (the redirect is cheap). `input-and-keybinds` ↔ `input-to-movement` (7.73). `hud` ↔ `hud-elements` twins at 58/69; `hud-elements`' missing `SpectatorGui.extractAction` row and `Gui.overlay`/`Gui.screen`. `prediction-and-acks` owns the ledger through-line; the two click lectures cite it — check the citation form. Coverage 346 classes / 33k lines: `client/gui/screens` is a family; `client/gui/components`, `client/sounds`, `client/resources` have mechanisms to name or decline. | **Done:** all twelve pages, the landing page and `reference/hud-elements` rewritten. Both queued moves settled in writing and both **declined**: the GUI watch order stands (the premise was wrong — text is baked *during* the record pass, so the stages interleave rather than run in a different order, and the tree comes first because the text pipeline cannot be followed until you know what it records into), and `the-gui-render-tree` keeps its title (all eight inbound links call it the render tree in their own sentences). `input-and-keybinds` ↔ `input-to-movement` (7.73) resolved: two long Part VIII bullets and the mouse-look paragraph cut to two citations, and the Part VIII citation that had been landing on `#the-cast` now lands on a new section, *A key press is not queued*. The `hud` ↔ `hud-elements` twins split by the Reference rule — the Reference page lost the three-gates prose and the two-consequences paragraph to `hud`, and gained the `SpectatorGui.extractAction` row and a row for the screen itself. `GuiMessageTag` and the chat family named on `hud`, with two of the queue entry's own guesses corrected. The ledger through-line's citation form checked: the two click lectures were already right. Coverage answered on the landing page rather than by writing pages — 92% of the part's unnamed lines are `client/gui` and four fifths of those are one screen or one widget — with `GameNarrator`, `DebugQueryHandler`, the toast shelf and the pip renderers written for the four genuine gaps, and `Gizmos` moved in from `what-this-book-skips`. **Fifteen corrections** (six page-against-page, three page-against-itself, two in the Reference table), nine suspicions re-derived and found sound, and a new VII → X arrow in the dependency figure that `check_deps.py` demanded. **No tool bug.** |
| **K** — *done 2026-09-06* | XI · Rendering | 11 | 7 | 743 | **`entity-rendering` against `reference/submit-phases`** (twins at 241/31; the catalogue wants `SubmitNodeStorage`, `TranslucentSubmit` and `RenderType.canConsolidateConsecutiveGeometry` named): whether the lecture wants more of the catalogue or the catalogue less preamble. `post-processing`'s *what a player sees* column: keep with a caption saying it is a reading, or cut. `the-window`'s *rest of the package* list omits seven of twenty-six classes (coverage); its seventh callback's section order is pass 6's. `lightmap-fog-and-sky` ↔ `environment-attributes-and-timelines` (8.27). `blaze3d` ↔ `naming-drift` (6.95). Homeless pass-3 cuts: `RenderSystem.outputColorTextureOverride` / `outputDepthTextureOverride` (the only mention of where the world can be redirected), the two `endFrame` ring buffers, the second `MaterialBaker` behind the block-atlas rule `models-and-atlases` still states. `block-entity-rendering`'s nineteen unmentioned in-scope classes, five worth a sentence each. Coverage 743 classes / 43k lines: renderers and models are families; `blaze3d`'s two backends and `client/renderer/*` sub-packages are the mechanisms.  | **Done:** all eleven pages, the landing page and `reference/submit-phases` rewritten. `entity-rendering` ↔ `submit-phases` decided **the catalogue's way round**: the lecture was already inside budget at four phases and one renderer, and it was the *Reference page* out-explaining it, so the merging rule moved up with the two phase classes and `RenderType.canConsolidateConsecutiveGeometry` and the catalogue kept the 12:3 split, now enumerated. `post-processing`'s *what a player sees* column **kept**, with a sentence saying it is a reading rather than a citation and the one row that was doing a different job reworded. `the-window`'s *rest of the package* completed — `TextureUtil` explained, five pipeline-state enums handed to `blaze3d`, and the cast's package claim corrected. `lightmap-fog-and-sky` ↔ `environment-attributes-and-timelines` (8.27) cut on the rendering side to one clause and an anchor; `blaze3d` ↔ `naming-drift` (6.95) left, with the 1.21 *table* flagged for pass 8 rather than the two sections the queue named. All three homeless pass-3 cuts placed — the two `RenderSystem` output overrides on `blaze3d`, the two rotated ring buffers written there too, the second `MaterialBaker` found already covered. `block-entity-rendering`'s completeness sweep done: all five prioritised items plus the built-in table's four other model kinds and its **five bare wrappers**, the enchanting table among them. Coverage answered on the landing page as Part X's was, by stating the boundary from both ends and **ruling out the `PARTS` change in writing**; the genuine gaps written on eight pages, the largest being the item-model property vocabulary — thirty-three properties in three registries — which discharges *what this book skips*' promise. Plus **fourteen corrections** (five page-against-page, three page-against-itself, two on Reference pages), four suspicions re-derived and found sound, the four proposed cuts all declined with reasons, and **no tool bug**. |
| **L** — *done 2026-09-07* | XII · World generation | 10 | 6 | 189 | **The lattice fact three times** across `terrain` and `density-functions`: one owner, two links. **`terrain`'s title** — a rename, decided. **Part XII ← `identifiers-and-registries` and `codecs-nbt-json`**, the two cross-links still open. `density-functions` ↔ `density-function-nodes` (11.92; twins at 225/122 on the noise bounds): the catalogue's preamble against the lecture. **`JigsawStructure`'s three unnamed fields** (§7: the expansion hack, dimension padding, liquid settings) — a section on `jigsaw-and-templates`. `features-and-placement`'s *tree of features* section with an unrelated sixth member. `blending`'s dashed annotation node saying what the prose says thirty lines below: pass 7 redraws, this pass decides which of the two owns the fact. `Structure.spawnOverrides` (§7; session N's view). | | **Done:** all ten pages, the landing page and `reference/density-function-nodes` rewritten. The lattice fact was **four** tellings, not three — twice on `terrain` — and `density-functions` keeps the resolutions while `terrain` keeps the eight-term census neither other page has. `density-functions` ↔ `density-function-nodes` settled the catalogue's way round *and* the lecture's: the Reference page's *Bounds* section became a table plus one paragraph and gave back the parse-time story, while the lecture gave up the per-node infinities. **`terrain` is not renamed**, ruled in writing. The two Part II cross-links paid at first use on four pages (`check_deps` had been printing both as unnamed by anything in the part). §7's `JigsawStructure` entry **discharged** as the close of *The assembly loop*, with the shipped-data census correcting the entry's own count; `features-and-placement`'s *tree of features* separated from `Feature.NO_OP`; `blending`'s dashed node **ruled the prose's**, with the page's three counts of one list reconciled; `Structure.spawnOverrides` found to be a **three-way** duplicate whose owner is Part VI's, with the two worldgen pages citing each other in a circle and neither citing it. Two moves in (`getLocatePos` to `structure-placement`, the processor census to `jigsaw-and-templates`) and the structure block taken off `blocks/README`'s unpaid hand-forward. Plus **fifteen corrections**, two of them on a Part IV page, six suspicions re-derived and found sound, **158 anchored links where the part had none on 82**, and no tool bug. |
| **M** — *done 2026-09-07* | XIII · Commands and data packs | 9 | 14 | 193 | **`ContinuationTask.schedule`** on `the-execution-engine` and `functions-and-macros`: the engine owns the arithmetic, the functions page cites. **The command-tree packet** on `permissions` and `brigadier-and-commands`: shape versus gating, read together once. The permission union paragraph on both `permissions` and `functions-and-macros`: the fact belongs on `permissions`. **`GameProfileArgument` and `ScoreHolderArgument`** (§7): a section on `entity-selectors`. **The boss bar** (§7): a section on `scoreboard-and-data` (`ServerBossEvent`, `CustomBossEvents`, `BossEvent` — 400 lines, no owner). The predicate catalogue and shape library (§7, with G). *Commands that are algorithms* (§7): a Reference page, not a lecture — write it or carry it with the reason. `advancements`' lost reload-listener sentence (when the layout runs) and `brigadier-and-commands`' `CommandSource` row — coverage, decompile open. The landing page's size sentence is the charter's example: it becomes the include. | **Done:** all ten pages rewritten and eight pages elsewhere edited. **The boss bar settled at both ends and not declined** — `scoreboard-and-data` gains *The third sink is a boss bar*, naming `BossEvent`, `ServerBossEvent`, `CustomBossEvent`, `CustomBossEvents` and `BossBarCommands`, none of which any page had named, so §7's entry, session J's routing from the HUD's end and session I's from the wire's are all discharged and `networking/README` cites an owner. **`GameProfileArgument` and `ScoreHolderArgument`** written as a section on `entity-selectors` (§7 discharged); **session G's shape-library ruling applied** and the concrete predicates declined as a family on `advancements`; ***commands that are algorithms* ruled out as a lecture in writing** and declared on the landing page's new *where the part stops*. `ContinuationTask.schedule` read and found a one-sentence pair, but the two pages *disagreed* about whether a nested execution gets its own budget and the reconciling fact was on neither — now on the engine page. The command-tree pair read together and found a sound split missing only its link. The permission union cut to a citation on the functions page. `brigadier-and-commands`' `CommandSource` row restored and widened into the answer to why a command block does not spam chat, which pays off `blocks/README`'s promise. `SharedSuggestionProvider` — the largest class named nowhere in the book — and the resource-argument family written. The landing page's size sentence now names its nine packages, as the template asks. Plus **thirteen corrections**, six page-against-page and two a page against itself; six suspicions re-derived and found sound; twenty queue entries settled in place. **No tool bug.** |
| **N** — *done 2026-09-07* | Reference, maps, the frame's Reference-facing pages | 21 + 5 | 24 (with A) | — | The cross-cutting Reference pages: `threads`, `math-and-primitives`, `naming-drift`, `glossary` (owner links after every part has settled; the two-owner entries as A ruled; *Blending data* → `BlendingData`), `lanes` (pruning is pass 7's), the class index labelled by part. **The three `gen_reference.py` views §7 names** (`EntitySpawnReason` with what each gates; the `Item.Properties` weapon helpers; `Structure.spawnOverrides`), plus whichever the part sessions asked for (block entities and tickers, `DamageTypes`). `reference/README.md`'s hand-written *parts* column: generate it from the landing pages' *Reference this part uses* sections (a `check_deps.py` or `gen_reference.py` change) or re-derive it by hand once. The maps: `packages.md`'s part table is generated now; `hierarchy.md`'s two-sentence section grows a figure or folds. | **Done:** the eleven hand-kept Reference pages and the five maps read one agent each; `threads`, `level-data-and-rules`, `naming-drift`, `math-and-primitives`, `glossary`, `submit-phases`, `hud-elements`, `reference/README`, `maps/README`, `maps/biggest` and `maps/fanin` rewritten or corrected; eleven pages outside the tier edited. **`reference/README`'s parts column is generated in effect** — `check_deps.py` derives it from the thirteen landing pages and fails on a disagreement, which is the fourth `F` check and the answer to A6's question; it found six of twenty rows stale. **All three §7 views built** (`spawn-reasons`, `weapon-helpers`, `structure-spawn-overrides`), each with a citer and a landing-page row. The glossary's owner links checked (all agree), *Occlusion* written with four senses, `BlendingData` renamed, the two-owner entries reduced, eight entries added; the *five headwords* finding **re-measured as four and ruled to stand**. `hierarchy.md`'s two-sentence section **stands as prose** — a `Goal` figure would draw 200 descendants of which 130 are nested in the mob they serve, which is the section's own point and the one thing a tree drawing hides. Plus **twenty-one corrections**, five suspicions re-derived and found sound, and no tool bug. |
| **O** — *done 2026-09-07* | the close | — | — | — | The frame and the summarisers against the finished parts (the introduction's part list, `lectures.md` re-derived from the landing pages, the glossary's owner links, the dependency figure); every move's redirect tested by `check_links.py`; `check_deps.py` green; [pass9.md](pass9.md)'s entries checked for shape; the pass's own strikes audited (a strike is a claim); the verdict on whether the pass was productive; pass 6's charter detail written, with the queue's `lecture` kind counted afresh. | **Done:** four reader agents — the introduction, `lectures.md`, **the thirteen landing pages read as one set** (a brief written this session; no session in the project had read them together, because each was rewritten by its own part's session) and the glossary entry by entry. **Twenty corrections**, of which **thirteen were one page contradicting another** and two a page contradicting itself: `entity-anatomy` had `EntityType.trackDeltas` inverted against Part IX; the introduction called three things skipped that the skips page says are taught; four landing pages had a size claim their own generated number denies (the smallest part, the largest thing on the client, the whole of `network/`, most of Part XIII by line); `lectures.md` called Part II a stack where its landing page argues *not a stack but a fan*, sent lighting's dependents to the wrong part, gave a menu broadcast a third place its owner says does not broadcast, and stated the owner's confirmation of the lecture order as a thing that has happened. **Three prose copies said the parts figure draws no arrows out of Parts I and II, and the figure draws two** — corrected on both pages and in `check_deps.py`'s comment. The glossary: eight headwords added, **twenty-seven arrows given anchors** (73 of its links now land on a section), two repointed, four two-owner entries reduced, three senses marked, seven orderings fixed. The audit of the pass's own queue: forty tagged `book` entries still open, of which **twenty-six were settled and never struck**, eight were never open (pass-3 cut logs the guesser routes to `book`), and six were genuinely open — five closed here (`GsonHelper`, the `SpawnCondition` and `SpawnerBlockEntity` hand-forwards, the sculk-spread gap declared, `ConversionType`) and one routed to pass 10 with a reason. `docs/pass9.md`'s own entries were in neither the order nor the heading form it states; both fixed. **The nineteenth tool bug**: `map_source.py`'s `SKIPPED` was missing `net/minecraft/client/multiplayer/chat/report`, so twelve classes the book declares skipped counted toward Parts IX and X in every size sentence and every coverage report. |

**What no session does**: reshape a page's skeleton or vary a device (6);
redraw a figure for legibility (7); hunt a tic or settle a count's wording
(8); change a fact without the decompile open (the standing rule); move a
page after this pass (the last-moves rule).

---

## Part 5 — The plan as it stood at pass 5's close

*Archived from [plan.md](plan.md) by the pass-6 planning session on 2026-09-07, headings demoted one level, so that plan.md is again the current charter and the passes to come. Three sections, as they were: **Where we are** — the fifteen session paragraphs, one per session, and the verdict on whether the pass was worth it; **Pass 5 — the book**, the charter as the 2026-09-05 planning session wrote it and session A amended it in practice; and **the session log from pass 5 onward** — the planning session between passes 4 and 5 (which also did the site admin), sessions A to I in full, and the note that J to O wrote theirs as the session paragraphs above. Every pointer to "below" or "above" in it means plan.md as it then was.*

### Where we are

**Pass 4 is done** (2026-09-05, sessions A–O): everything the book says has
been read against the decompile twice. Fifteen sessions, one adversarial
agent per page, over the 102 system pages, the 13 landing pages, the 21
Reference pages, the introduction, the lecture map and the atlas; 836
corrections in the thirteen sessions that counted them; **every page had at
least one wrong claim**, for a fifteenth consecutive session; fifteen tool
bugs, six of which had published a falsehood. Four gates stand between a
page and the site. The record, the rulings and the log are in
[pass4.md](pass4.md), and so are the three findings that shape everything
below: the errors were never where the writing session expected them (the
checklists came back clean from Part VI on; the errors were in the
illustrations — tables, summaries, Q&A answers, asides, landing pages); a
correction is a claim and a strike is a claim (pass 4 got three of its own
wrong); and the tools are suspected first.

**The ten-pass plan** was set the same day by the owner with the planning
session. Ten passes leave the site finished; a second edition, with a wider
scope, would be a separate project seeded by [pass3.md](pass3.md) §7 and
*what this book skips*. Passes 9 and 10 are the owner's fixed points — the
last fact-check and the last polish. Passes 5 to 8 are four passes of
restructuring and refinement, because pass 3 was the most productive pass so
far and pass 4 left a precise list of where the book is still weak. Each
pass has **one lens**, since pass 4 showed that a session sees what it is
looking for and nothing else: what the writing session knew it had changed
came back clean, and what it did not know was where the errors lived.

**Pass 5 — the book — is done** (2026-09-07, sessions A–O), and its record is
[pass5-brief.md](pass5-brief.md), which holds the charter, the rulings, the
runbook and the schedule with what each session did — the archive a finished
pass gets, kept there rather than in `pass5.md` because that name was already
the queue four passes draw on. Its charter is below at the level of
intent; its brief, runbook, standard and schedule are
[pass5-brief.md](pass5-brief.md), written by the 2026-09-05 planning session
with the tools it names (`pass5_dups.py`, `pass5_coverage.py`,
`check_links.py`, `pass5_queue.py`, `pass5_prompts.py`, and `map_source.py`'s
`PARTS`), each measured against the corpus before the first session ran.
**Session A is done** (2026-09-05): the ownership rule and the landing page's
role are in `TEMPLATE.md`, the through-lines have owners and anchors, the
lecture map has been cut back to the order, and two more checks stand in
`check_deps.py`. Part 3 of the brief is now the record of what was ruled, and
sessions B–N apply it. **Session B is done** (2026-09-05, Parts I and II):
nine pages rewritten, six mechanisms cut to a citation, the feature-flag
coverage gap discharged, both landing pages rewritten to the role — Part I's
figure had been drawing the book rather than the part — two corrections and
one tool bug.
**Session C is done** (2026-09-05, Part III): all six pages rewritten, five
mechanisms cut to a citation, the abstract `Level` written, the landing page
given an argument and a *where the part stops* — and **six corrections**,
four of them pages disagreeing with each other, which is the finding pass 5
was chartered on.
**Session D is done** (2026-09-05, Part IV): all eleven pages and the part's
Reference page rewritten, seven mechanisms cut to a citation and two moved,
thirty-seven anchors where the part had none, and **nine corrections** — five
of them again one page contradicting another. It also found the pass's first
tool bug that was *hiding* failures rather than publishing one: the link gate
could not see a link whose text wrapped across a newline, so 243 links had
never been checked and one was broken. The §7 entry on its row was **ruled
out rather than written** — the world border gets no lecture, and the ruling
says why.
**Session E is done** (2026-09-05, Part V): all seven pages and the part's
Reference page rewritten, seven mechanisms cut to a citation and one moved the
other way, thirty-seven anchors where the part again had none, and **six
corrections** — four of them one page contradicting another, the shape four
sessions running. The queue's standing question came back *yes*: one of the six
spokes had started re-explaining the hub's two update channels. Part V is the
book's lowest-covered part at 40% of lines named, and the session's finding is
that the number is right to be low and no page said so — the landing page now
does, five family sentences discharge what a sentence can reach, and four
mechanisms too big for one (the hopper first among them) go to §7. **No tool
bug**, the first pass-5 part session without one.
**Session F is done** (2026-09-05, Part VI): all nine pages and the part's
Reference page rewritten, and this is the session where the lens paid hardest —
**thirteen corrections**, the most of any pass-5 session, of which **eight were
one page contradicting another** and three were a page contradicting itself.
`authority` had a player's own physics in the wrong phase of the tick, against
its owner in Part VIII. Part VI is the book's largest part and its second
lowest-covered; the session's finding is that the low number is right, because
the bulk is one class per species, and that four things in those packages are
not species and are explained nowhere. **One tool bug**, the eighteenth: the
atlas printed four packages Part VI *includes* as exclusions.
**Session G is done** (2026-09-05, Part VII): all eight pages and the landing
page rewritten, and the book's top duplication pair settled — Part II owns the
component system, Part VII owns the stack, and `items-and-stacks`' own hook had
been Part II's. **Twelve corrections**, four of them page-against-page and three
a page against itself, including a page that denied its own claim twice in the
paragraphs below it. Part VII is the fourth part running to have arrived with
almost no anchors. The part's coverage answer is four families and four systems
that are nobody's — villager trading, brewing, the creative tabs and armour
trims — all four declined in writing. **No tool bug.**
**Session H is done** (2026-09-06, Part VIII): all seven pages and the landing
page rewritten, and this is the session where the part was small enough that
the coverage question came back *yes* — 97% of Part VIII's lines are named
somewhere, and the landing page now makes that its argument instead of leaving
it unsaid. Nine pages in six other parts were edited, because almost
everything a Part VIII page reaches for is owned elsewhere: the
record-and-discard bracket settled between the part's own two trunk pages,
which had been opening on the same surprise two lectures apart; `Consumable`
split with Part VII along rule 1 rather than moved whole, with the session
writing down why the routing rule's default was declined; and the pass's
largest single move so far, `Player.cannotAttack`'s two hooks and projectile
deflection off `reference/non-living-damage`, where a Reference page had been
holding the book's only explanation of a lecture's own method. **Eight
corrections**, three of them a page disagreeing with another page and two a
page disagreeing with a Reference page, plus four suspicions re-derived and
found sound. Part VIII is the fifth part running to arrive with **no anchors
at all**; seventy-one were added. **No tool bug**, the third pass-5 part
session without one.
**Session I is done** (2026-09-06, Part IX): all five pages and the landing
page rewritten, eleven pages in seven other parts edited, and **seventeen
corrections** — eight of them one page contradicting another and **five a page
contradicting itself**, which is the new high. Four of the eight were the one
seam, Part IX against Part III's tick: the flush bracket's scope, what
`PacketListener.onPacketError` actually does, where `Connection.tick` flushes,
and what its first queue holds. The part's shape sentence, open since pass 4,
is decided — *the wire three times, and two things it carries* — and the
landing figure's two arrows, which asserted a dependency the page's own prose
denied, are redrawn with it. Part IX arrived with **7 anchors on 62
cross-part links**, the sixth part running; three pages in three parts had
been citing `the-connection` for the thread hop at an anchor **session A
itself declared** and which is about something else, so the brief's A3 row is
corrected with the reason. The coverage answer is that 84% named is legible
only once the landing page says the part owns the wire and not everything in
`network/`; three passages were written for what is neither a packet nor a
`Component` — the text filter, the per-phase listener interfaces and the
address resolver. **No tool bug.**
**Session J is done** (2026-09-06, Part X): all twelve pages, the landing page
and the part's Reference page rewritten, and this is the session where the
lens found the *part's own boundary* rather than a duplicate. Part X is the
book's third-largest coverage debt — 32,000 lines named nowhere — and **92% of
it is `client/gui`, four fifths of that one more screen or one more widget**,
which `gui-and-screens` already covers as a pattern and no page said so; the
landing page now makes that its second boundary statement, and §7's Part X row
is discharged without a new page. **Fifteen corrections**, six of them one page
contradicting another and three a page contradicting itself, including the
part's own landing page putting the Part X/XI boundary at a different profiler
zone from the three pages that own it. Two of the corrections were in the part's
Reference table, which had a recorded element with no row and a column holding
a condition instead of an answer. Nine suspicions were re-derived and found
sound — the highest ratio of any pass-5 session, and the reason is that the
agents have no source. Both open moves are settled in writing: the GUI watch
order **stands** (the premise was wrong — the stages interleave rather than
run in a different order, because text is baked *during* the record pass), and
`the-gui-render-tree` is **not renamed**, because all eight inbound links call
it the render tree in their own sentences. `check_deps.py` refused the first
landing page for a *before you start* entry the dependency figure had no arrow
for, which is the gate doing its job. **No tool bug**, the fourth pass-5 part
session without one.
**Session K is done** (2026-09-06, Part XI): all eleven pages, the landing page
and `reference/submit-phases` rewritten, and this is the session where the
lens found a *Reference page out-explaining its own lecture* — the merging
rule was fourteen lines of mechanism on the catalogue and three on
`entity-rendering`, and it moved to the lecture with the two phase classes and
`RenderType.canConsolidateConsecutiveGeometry`. **Fourteen corrections**, five
of them one page contradicting another and three a page contradicting itself,
including a Reference row that said a particle group is submitted once where
the code makes two nodes, and a page whose closing sentence denied its own
opening about whether the weather reads the world clock. Part XI is the book's
largest coverage debt in absolute lines, and the answer was the same shape as
Part X's: the number is inflated at *both* ends by a package mapping the book
disagrees with, and the landing page now says so from this side as Part X's
does from the other — the `map_source.py` change is **ruled out in writing**,
because moving a shared package would invalidate the argument session J had
just written. Sixteen ownership moves, of which the largest are three that
went *out* of the part to Part X's client loop and Part II's resource system.
Three homeless pass-3 cuts placed, four proposed cuts all declined with
reasons, and the landing page's argument — *the renderer is not allowed to
look at the world* — written for the first time. **No tool bug**, the fifth
pass-5 part session without one.
**Session L is done** (2026-09-07, Part XII): all ten pages, the landing page
and `reference/density-function-nodes` rewritten, eleven pages in six other
parts edited, and this is the session where the lens found *a page arguing with
itself about a data-pack field*. `terrain` called the carvers' lava level a
constant in the generator four sections after calling it *configured*; it is
`CarverConfiguration.lavaLevel`, a `VerticalAnchor`, and all four shipped
carvers anchor it eight blocks above the world's **bottom** — which is the real
answer to why it does not move with the sea level. **Fifteen corrections**,
five of them one page contradicting another and three a page contradicting
itself, and **two of them on a Part IV page**: `scheduled-ticks`' opening list
of "everything the world does later" offered a bone-mealed sapling and a
budding amethyst, and both are *random* ticks, which is the distinction that
page itself draws. Six suspicions were re-derived and found sound, among them
the landing page's `PlacementContext` sentence — the class really does hand a
placement modifier the carving mask, and it was named on no page in the book.
The part's top duplication pair settled **the same way round as session K's**:
`reference/density-function-nodes` had drifted into lecture prose, and its
36-line *Bounds* section is now an eight-row table plus one paragraph, with the
parse-time story, the min/max warning and the trustworthiness argument back on
the lecture that owns them. The lattice fact was three tellings on two pages
plus a fourth inside `terrain`; `density-functions` keeps the resolutions and
`terrain` keeps the census of eight interpolated terms that neither other page
has. **`terrain` is not renamed**, ruled in writing: read whole the page is not
three statuses but one thing made across them, and every page that cites it
calls it the terrain in its own sentence. §7's `JigsawStructure` entry is
**discharged** — and the shipped data corrected the entry, because six
structures set the expansion hack and not five. The part's biggest structural
finding was `terrain` and `features-and-placement` carrying four Part IV
passages between them as a running commentary on the conveyor, each now a
citation with the cargo's half kept. Part XII arrived with **82 internal links
and not one anchor**, the seventh part running; it now carries 183 links, 158
of them anchored. **No tool bug**, the sixth
pass-5 part session without one.
**Session M is done** (2026-09-07, Part XIII): all ten pages of the part
rewritten and eight pages elsewhere edited, and this is the session where the
lens found *a mechanism the whole book had left out*. The boss bar is
`execute store`'s third sink and about 400 lines of `BossEvent`,
`ServerBossEvent`, `CustomBossEvent`, `CustomBossEvents` and
`BossBarCommands` — and no page named a single one of those classes. Three
earlier sessions had each found one end of it and routed it here;
`scoreboard-and-data` now owns it as a section, because the model *rhymes*
with the page's own: a named server-side thing holding a number, saved with
the world, broadcast to whoever is attached, writable only by a command, and
carrying a persisted `Set<UUID>` beside a live `Set<ServerPlayer>` — the
scoreboard's own *a name is not an entity* trick a second time. That section
discharged three open items at once, so `networking/README`'s *where the part
stops* now cites an owner instead of declaring a gap. **Thirteen
corrections**, six of them one page contradicting another and two a page
contradicting itself: `scoreboard-and-data` said a crash loses a score where
`how-a-server-dies` says a crash saves — the crash path's *finally* reaches
`MinecraftServer.saveAllChunks`, whose first statement stores the scoreboard,
and it is the watchdog and a hard kill that lose it; `brigadier-and-commands`
put a sign among the commands the client vets, and `permissions`' own figure
said the same against its prose four lines below, when a sign runs its command
server-side at a hard-coded gamemaster; `functions-and-macros` called the
function tag the first thing the tick does, where the packet-flush suspension
is; and `resource-system` asserted the stale-command-tree folklore that
`brigadier-and-commands` exists to correct. **Six suspicions re-derived and
found sound**, among them a count that looked self-contradictory and was not.
The coverage answer is that most of the part by line is the catalogue, and the
landing page now says which families the pages above already cover as patterns
and which single omission is deliberate — the three commands that are
*algorithms* rather than doors, ruled out as a lecture in writing. Two more §7
entries discharged and one ruling applied. Twenty queue entries settled in
place. **No tool bug**, the seventh pass-5 part session without one.

**Session N is done** (2026-09-07, Reference, the maps and the frame's
Reference-facing pages): the eleven hand-kept Reference pages read one agent
each, the five maps likewise, three new generated views built, and eleven pages
outside the tier edited. This is the session where the lens found *the two tiers
that exist to be trustworthy each telling a lie about their own
trustworthiness*. `reference/README`'s **parts** column — the one column in the
book claiming which parts lean on which shelf page — was stale in **six of
twenty rows**, missing nine part numerals; and `maps/README` opened with
*nothing here is hand-counted … the pages are regenerated each time the site is
built*, which is true of `src/generated/` and false of every number in the four
map pages' prose, as two independent reads found. Both are fixed the same way:
the shelf's column is now **derived by `check_deps.py`** from the thirteen
landing pages' *Reference this part uses* sections and refuses to publish on a
disagreement (a fourth `F` check, with a probe), and the atlas's landing page
separates its generated half from its hand-written half and says what the
version pass owes the sentences. **The gates grew by truth for the third time in
this pass.** [pass3.md](pass3.md) §7's three `gen_reference.py` views are all
**built and published** — `spawn-reasons` (nineteen reasons, and the finding
that **eight are tested by nothing** while all but two comparisons sit inside
`Mob.finalizeSpawn`), `weapon-helpers` (seven helpers, forty-two items, and
three of the six tool families needing a class of their own only because they
also do something on right-click) and `structure-spawn-overrides` (thirty-four
structures carry the field, **six** fill it in, and **eighteen of the
twenty-three overrides are empty**, which is a ban and not a no-op) — each with
a citer and a landing-page row. **Twenty-one corrections**, eleven of them on
pages outside the tier, which is what a Reference session finds: the shelf holds
the facts the lectures also state. Among them `server-tick`'s taxonomy of the
nine handlers that never hop, which named three kinds and accounted for seven —
the two it missed write listener state on the Netty thread, and the server's
nine are now a table on `reference/threads` beside the client's, which is where
a list belongs. `maps/biggest` had six classes as *one chain of inheritance*
that forks two ways and ends in two leaves; `maps/fanin` had a table of
thirty-two classes described as the thirty and a *quarter* that is under a
third; `naming-drift` had 243 rows and has 245. **Five suspicions re-derived and
found sound**, one sharper than the page knew — a `WorldBorder` built from
`WorldBorder.Settings.DEFAULT` is live at warning time 15, because the
constructor stores the settings without applying them — and one of them a **tool
artefact rather than a finding**: pass 4's *five glossary headwords the corpus
does not use* is four, all four compound noun phrases the corpus writes in
pieces, and the original count came from a search that could not see a headword
wrapped across a line. *Occlusion* is written at last, four senses and four
links, and with it the ruling that the glossary **does** disambiguate; eight
entries added, three second senses, and the two-owner reductions A5 ordered.
**No tool bug**, the eighth pass-5 session without one.

**Session O is done** (2026-09-07, the close), and it is the session that
proves the lens was still finding things on the last day. Four reader agents:
the introduction, `lectures.md`, **the thirteen landing pages read as one set**
— the reading no session in the project had done, because each landing page was
rewritten by its own part's session and no session ever saw all thirteen — and
the glossary entry by entry. **Twenty corrections**, of which **thirteen were
one page contradicting another**, the shape of every session in this pass:
`entity-anatomy` had `EntityType.trackDeltas` inverted against Part IX's page,
calling a predicate that is true of every type but ten "a hard-coded list of
types whose velocity is never sent at all"; the introduction listed the OpenAL
backend, the debug-drawing API and the recipe book as things "in the jar and not
in the parts" where the skips page it summarises says, in its own headings, that
all three are taught; **four landing pages made a size claim their own generated
number denies** — the smallest part of the book is Part I and not Part VIII, the
largest thing on the client is Part XI by classes and Part X by lines, Part IX
is not "the whole of `net/minecraft/network`", and Part XIII's catalogue is
under a third of it and not most; and `lectures.md` called Part II a stack where
its landing page argues *not a stack but a fan*, sent lighting's dependents to
the wrong part, gave a menu broadcast a third place whose owner says it does not
broadcast, and stated the owner's confirmation of the lecture order as something
that has already happened. **Three prose copies said the parts figure draws no
arrows out of Parts I and II, and the figure draws two** — corrected on both
pages and in the gate's own comment. The glossary got eight headwords, **twenty-
seven more anchored arrows** (73 of its links now land on a section rather than
a page top), two arrows repointed, four two-owner entries reduced to one owner
and three senses marked. **The audit of the pass's own queue is the finding
about the pass itself**: of the forty entries still tagged `book` and unstruck,
**twenty-six had been settled by a later session and never struck**, eight were
never open at all (pass-3 cut logs the queue tool's guesser routes to `book`),
and six were genuinely open — five closed here and one routed to pass 10 with a
reason. Pass 4's failure mode was a strike that settled nothing; pass 5's is the
opposite, a settlement never struck. `docs/pass9.md` was in neither the order
nor the heading form it states for itself, and pass 9 reads it first, so both
are fixed. **The nineteenth tool bug of the project, and the second in this pass
that had published a falsehood**: `map_source.py`'s `SKIPPED` was missing
`net/minecraft/client/multiplayer/chat/report`, so twelve classes and 952 lines
the book itself declares skipped were counted into Parts IX and X by every size
sentence, every landing page's coverage answer and every coverage report the
pass ran.

#### What pass 5 did, and whether it was worth it

Fifteen sessions. **171 corrections** in the fourteen that counted them, and the
number that matters is not the total but the shape: session after session, about
half of them were **one page contradicting another**, which is the error a
page-at-a-time reading cannot see and which two fact-checks over 102 pages did
not find. Pass 4 read every page against the source and left 171 places where
two pages disagreed with each other. That is the answer to whether the lens
earned its cost.

Beside the corrections: every part's landing page rewritten to a stated role and
given an argument; the coverage question asked once per part with a tool and
answered in writing, including in the four places the answer was *this is
deliberately not explained, and here is why*; seven parts that arrived with no
anchors at all left with them; the book's duplication pairs settled one at a
time, with the loser keeping a sentence and a link; three new generated
Reference views built and cited; and **the gates grew by truth three times** —
`check_links.py` became a deploy gate on day one, `check_deps.py` gained two
checks in session A and a fourth in session N, and each new check shipped with a
probe proving it fails on the construct it should. Four tool bugs, of which two
had published a falsehood and one had been hiding failures.

What pass 5 did not fix, and named instead: the landing pages grew past their
own budget while gaining their argument (median 127 lines outside the watch
order against a hundred, and the growth is the coverage section every part now
carries); the recognition device became a slot on nine of thirteen; and the
coverage *fraction* is hand-counted on seven landing pages beside a size that is
generated. All three are in [pass5.md](pass5.md) for pass 6.

### Pass 5 — the book (done, 2026-09-07)

**Goal:** the corpus reads as one book. Every idea has one home and one
name and every other mention is a sentence and a link; every seam between
pages is a link in the right direction; every part's landing page is the
part's argument rather than a summary of its pages; nothing in a part's
scope is unmentioned by accident; and after this pass no page moves again.

**Why first:** pass 4 read pages one at a time and found what a page-at-a-
time reading finds. Its two findings that no per-page check could have made
were both cross-page: session N's contradiction check (one phrase, two
numbers, two pages — three times), and session O's glossary sweep (entries
written from sentences another session had corrected). The landing page was
the worst page in its part three parts running, for the same reason: it
summarises, and summaries drift. The corpus is 290,000 words of system
pages written by thirty sessions, and the thing none of them could see is
the book.

#### The jobs

1. **Ownership.** Every mechanism explained in one place. The known
   duplicates: the lattice fact three times across `terrain` and
   `density-functions`; `ContinuationTask.schedule` on the engine page and
   the functions page; `EntityType.create`'s gates on `entity-anatomy` and
   `entity-lifecycle`; the command-tree packet on `permissions` and
   `brigadier-and-commands`; `entity-rendering` against
   `reference/submit-phases.md`; the staircase's *why* said twice on
   `signal-and-dust`; the two update channels, owned once by
   `blocks-and-states` and to be checked on the six pages that link to it.
   The planning session builds a **duplication finder** (shared backticked
   identifiers between page pairs, ranked) so the sessions start from a list
   rather than from memory.
2. **The seams.** The cross-links session A of pass 4 judged missing and
   left (Part X ← `anatomy/anatomy`; Parts IV and XII ← `identifiers-and-
   registries` and `codecs-nbt-json`, Part XII's two still open); the
   hand-forwards; the nine-page dependency table's unstated membership rule;
   Part IV's three orders (`SUMMARY.md`, its landing page and `lectures.md`
   disagree, the only part where they do); the two circular cuts (III ↔ IV,
   V ↔ X) re-judged. `check_deps.py` stays green; a **link checker** over
   every internal link and anchor becomes a tool here and a gate by pass 10.
3. **The through-lines.** The ideas that cross parts — the tick and its
   phases, the four threads, the wire and the hop, authority and
   prediction, the registry freeze and the reload, the data-driven type
   pattern, the ledger — each told once at full length and named the same
   way everywhere else. Whether the introduction, `anatomy`, or a new page
   becomes lecture zero for them is pass 5's decision, made in session A
   with the list in hand.
4. **The summarisers.** The thirteen landing pages get a stated role — the
   part's shape as a figure, its argument in a paragraph, *before you
   start*, the watch order, the Reference it uses, under a hundred lines —
   and are rewritten to it from the pages as they stand, in the part's own
   session, after the part has been read whole. `lectures.md`'s blurbs, the
   glossary's owner links, the maps' and Reference's front pages likewise.
   Session M's finding stands: a landing page's size sentence needs nine
   package names to be reproducible and gives none, so **the atlas generates
   the per-part totals** (a `map_source.py` change for the planning session)
   and no landing page hand-counts again.
5. **The coverage question, once per part** (pass 2's lesson: ask it with a
   tool, per scope). With the atlas as the population — what in the part's
   packages does no page in the part mention, ranked by size — and
   [pass3.md](pass3.md) §7's open entries as the known answers: the abstract
   `Level`, feature flags and `FeatureFlagSet`, `GameProfileArgument` and
   `ScoreHolderArgument`, `JigsawStructure`'s three unnamed fields, the boss
   bar as `execute store`'s third sink, the predicate shape library, the
   three Reference views `gen_reference.py` does not yet have, and the
   material pass 3 cut and gave no home (the `Item.getUseDuration` roster,
   the fortress spawn list and `Structure.spawnOverrides`, the
   fall-attribution threshold, `RenderSystem`'s output overrides, the two
   `endFrame` ring buffers). A section or a Reference row for most; a page
   only where a part's argument has a hole.
6. **The last moves.** Merges, splits, renames and reorders, each decided
   and either done or ruled out: `how-a-server-dies`' two subjects (the
   three endings and the durability page inside it); `signal-and-dust`'s two
   (the lever and the second evaluator); `the-gui-render-tree`'s title;
   `terrain`'s; the GUI stack watched in a different order from the one it
   runs in; `block-entities` as Part V's odd page; the three homeless items
   from `players-and-sessions`; `chunk-storage`'s proposed hand-off of the
   null-parse branch. A move changes `SUMMARY.md`, the landing page,
   `lectures.md`, the glossary and `book.toml` in one commit.
7. **The site stands alone** — the owner's ruling of 2026-09-05, replacing
   the question of whether every page is a lecture. Readers today have only
   the textbook, so nothing on a page may lean on a lecture to make sense;
   the lecture order and any tiering of episodes are the owner's own work,
   not this pass's. The page count is whatever the book needs — a merge or a
   split is judged by the reader who has only the page, never by the number
   of episodes. Everything inside the current scope is explained, concisely:
   the coverage question is real, its answer is usually a section, a
   Reference row or a sentence, and concision governs *how* a thing is
   explained, not *whether*.

**What pass 5 does not do:** it does not reshape a page's internal skeleton
or vary a device (6); it does not redraw a figure for legibility (7); it
does not hunt a tic or settle a count's wording (8); it changes no fact
without the decompile open (the standing rule).

**Sessions** — the runbook and the schedule are in
[pass5-brief.md](pass5-brief.md). A — the standard: the ownership rule and
the landing-page role written into `TEMPLATE.md`, the through-lines' owners
and citation forms, the duplication report routed, Part XIII's landing page
as the exemplar, the frame's own seams. B–N — the parts in sidebar order,
one session each (B takes I and II; N takes Reference and the maps), reading
the part end to end in watching order before changing anything, one
reader-of-the-book agent per page, the part's Reference pages included. O —
the close: the frame and the summarisers against the finished parts, the
lecture map re-derived, the glossary's owner links, the moves' redirects
under the link gate, [pass9.md](pass9.md)'s entries checked for shape, the
pass's own strikes audited, and pass 6's charter detail.

### Session log — pass 5 onward

*(newest last; pass 4's log is at the end of [pass4.md](pass4.md), with the
plan as it stood at its close)*

- **2026-09-05, planning session (Fable, between passes 4 and 5).** No page's
  content touched. **The ten-pass plan** set with the owner and written
  above: 5 the book, 6 the lecture, 7 the figures, 8 the voice, 9 the third
  fact-check, 10 the last polish; the version pass and the owner's read
  beside them; one lens per pass, structure before words, across before
  within, the heavy polish before the fact-check and the light one after.
  Pass 5's detailed brief and tools are the next planning session's.
  **Housekeeping:** the old `plan.md` archived whole into `pass4.md` with
  its headings demoted (this file is now the current charter and the passes
  to come); `pass5.md` retitled as the queue passes 5–8 draw on, with a
  routing preface by kind; `pass9.md` opened with its standing items;
  `CLAUDE.md`, `README.md` and `TEMPLATE.md` brought current (the template
  pointed rewrites at `pass4.md` and rulings at `plan.md`); two published
  sentences that named pass numbers made true (`lectures.md`'s "confirmed in
  pass 6"); the memory culled — five sibling-project memories deleted, seven
  rewritten. **Site admin**, since the owner asked: Open Graph and
  Twitter-card meta on every page through `theme/head.hbs` (mdBook 0.5's
  head partial — the only theme override); `src/robots.txt` pointing at a
  sitemap; `tools/site_index.py`, run by `deploy.sh`, writing
  `book/sitemap.xml` (144 URLs with git last-modified dates) and
  `book/llms.txt` (the index form of the llms.txt convention, one line per
  page with its verified-line scenario) beside `llms-full.txt`; `site-url`
  set so the 404 page keeps absolute links under nested paths. Found and
  recorded: before the site shipped a `robots.txt`, Cloudflare served its
  own content-signals one for the domain (signals unset); Cloudflare Pages
  serves **clean URLs** and answers every `.html` address with a 308 to the
  extension-less one, so the sitemap and `llms.txt` list the clean form
  (the first deploy listed redirects, fixed the same evening); the Pages
  project has **no Web
  Analytics enabled**, and the token cannot enable it (refused on RUM, zone
  settings and bot management; it verifies, edits Pages, and reads the zone
  and DNS), so that click and Google Search Console are the owner's; DNS for
  minecraftdocs.dev is done (a proxied CNAME), which voids an older note.
  26.3 confirmed unreleased from the version manifest (pre-2, 2026-09-04).
  Tag `pass-4-close` on `5cad2d5`. **Rulings:** a queue file keeps its name
  when a pass is renumbered, and a routing preface says which pass takes
  what, because moving 2,000 lines of entries between files is how entries
  get lost; a published page never names a pass number as a promise about
  the future (the rot rule); the coverage question is asked in pass 5 and
  never again, because passes 9 and 10 add nothing.
- **2026-09-05, planning session (Fable), the second sitting — pass 5
  planned.** No system page's content touched. **The brief**:
  [pass5-brief.md](pass5-brief.md) — Part 1 the agent's brief (a reader of
  the book with no source, five questions: ownership, seams, through-lines,
  coverage, moves), Part 2 the runbook, Part 3 session A's standard (the
  ownership rule, the landing page's role, the through-lines with their
  measured spread and proposed owners, the routing rule for cross-part
  pairs, the frame's seams), Part 4 the schedule with what the tools found
  per part. **The owner's ruling** recorded as job 7 above: the site stands
  alone, the page count is the book's to decide, everything in scope is
  explained concisely, the lectures are the owner's. **The tools**, each
  with a `--probe`: `pass5_dups.py` (rare shared names between page pairs,
  weighted 1/df; near-duplicate sentences by shared 5-grams, summariser
  echoes labelled; `--terms` for a through-line's spread), `pass5_coverage.py`
  (the coverage question per part with the atlas as the population),
  `check_links.py` (links, anchors as mdBook slugifies them — validated
  against all 1,318 built heading ids — includes, `SUMMARY.md` both ways,
  `book.toml` redirects; `--inbound` for the seams), `pass5_queue.py`
  (pass5.md routed by kind and page, kinds guessed from section priors and
  words, `[kind=…]` tags win), `pass5_prompts.py`, and `map_source.py`'s
  `PARTS` mapping writing `parts.md` and thirteen `part-<dir>.md` size
  phrases — the *where each part lives* table on `maps/packages.md` is now
  generated from it, and its packages were widened where the hand table
  was short (Part IV gains `material`, `attribute`, `timeline`, `clock`,
  `border`; VI `damagesource`, `effect`; II `world/flag`; X `input`,
  `server`; XI `particle`; XIII `permissions`, `bossevents`, the dialog
  screens). **Measured**: 7,510 links and 12 anchors, none broken, so
  `check_links.py` went into `deploy.sh` as the fifth gate at once (a ruling:
  the gates grow by truth, and it was clean on day one); the queue holds 348
  open units — 114 pass 5's, 75 pass 6's, 28 pass 7's, 131 pass 8's, 185 of
  them guessed; coverage by lines named runs from 40% (Part V) to 100% (Part
  I), the low parts being families of one class each; the top duplicate
  pair in the book is `data-components` ↔ `items-and-stacks`, and the
  charter's named duplicates all surface in the top forty. The introduction's
  gate sentence now names the link check (logged in [pass9.md](pass9.md)).
- **2026-09-05, session A — the standard (pass 5).** The rulings the thirteen
  part sessions apply, made once and written into
  [pass5-brief.md](pass5-brief.md) Part 3, which is now a record of what was
  decided rather than a list of what to decide. **`TEMPLATE.md` gained two
  sections** that are rules about the book rather than about a page: *One home
  per mechanism* (the ownership rule, with the planning session's draft
  amended three ways — the earlier-part rule demoted to a tie-break under *the
  page whose scenario the mechanism answers*; the Reference rule made to bind
  the lecture as well as the catalogue; and *a summariser never explains* given
  three consequences, of which **the summariser is the copy that gets shorter**
  is the new one) and *The landing page* (the argument · the size · the shape ·
  before you start · watch in this order · the Reference it uses). **The
  citation form** is stated for the first time: the parenthetical link the book
  already writes, now carrying **the anchor of the section that is the
  answer** — the eight through-line owner pages take 169 inbound links and
  three carried an anchor. The seven through-lines' owners are confirmed with
  an anchor each, every one checked against the built heading id;
  `anatomy/anatomy` is lecture zero and no new page is written. **Three
  published pages changed.** `src/lectures.md` lost its 102 per-page blurbs
  (662 lines to 469): each was a second copy of a line on a landing page, in
  different words — the drift machine pass 4 found errors in, a hundred times
  over — and what stays is everything about the *order*, including every
  ordering claim that was inside a blurb. Its dependency table has a stated,
  mechanical membership rule at last (two or more landing pages, less the three
  every part assumes), which loses three rows and gains three.
  `src/SUMMARY.md` moves *environment attributes and timelines* to first in
  Part IV, under the general ruling that **the landing page's watch order is
  the book's order and the sidebar and the lecture map follow it**; Part IV was
  the only part of thirteen where they differed. `src/systems/commands/README.md`
  is the exemplar landing page, rewritten to the role, its hand-counted size
  replaced by the include (473 / 43,900 by hand against 470 / 43,126 by the
  atlas) and one sentence cut under the ownership rule rather than moved.
  **The gates grew by truth again**: `check_deps.py` now fails when
  `SUMMARY.md` and a landing page's watch order disagree and when the
  dependency table's membership breaks its own rule — the second reproduced
  pass-4 session A's hand-found list exactly before anything was edited, which
  is the evidence it reads the pages right — and `verify_names.py --index`
  labels a landing page by its own title instead of *README*, which eleven
  pages shared. **Rulings the part sessions inherit**: fifteen declared pairs
  are checked for drift and never merged; the glossary keeps one owner per
  *sense* and does disambiguate, so *Occlusion* gets an entry from session N;
  the landing-page budget is about a hundred lines plus the watch order
  (measured: 45 to 144, median 90), which names two outliers instead of
  eleven; a landing page states a size only where size is part of its
  argument, and then only through the include. Five queue entries struck (two
  overtaken by the blurb cut, two done, one ruled out — the doubled licence
  footer, for the entry's own reason), six findings logged back to
  [pass5.md](pass5.md) and the session's claims to [pass9.md](pass9.md), where
  it recorded **no corrections**: nothing it read was wrong, because every
  finding was about where a claim lives rather than whether it is true.
- **2026-09-05, session B — Parts I and II (pass 5).** Eleven pages read by
  one agent each, both parts read end to end in watching order first. **Nine
  pages rewritten.** The session's shape was the one pass 5 was chartered
  for: almost nothing found was wrong, and almost everything found was in the
  wrong place. **Ownership:** six mechanisms cut to a sentence and a link —
  the two tag tables (to `tags`, whose scenario *is* the swap on a frozen
  registry, leaving `identifiers-and-registries` the freeze proof it owns),
  the GPU-backend retry order (to `rendering/the-window`), the crash relay (to
  `how-a-server-dies`), the empty-server pause (to `server-tick`),
  `MinecraftServer.spin`'s construct-then-start order (to
  `starting-a-server`), and the Netty hop's mechanism (to `the-connection`,
  `anatomy` keeping only the drain-timing contrast its own figure draws).
  `anatomy`'s one 1.21-era callout was spent on `Gui`/`Hud`, a Part X subject
  the page never returns to and which `client/hud` and `reference/naming-drift`
  both already carry; it now spends it on `DeltaTracker`, which the page uses
  three times. On `what-this-book-skips`, three of fifteen "skipped" tours
  were not skips at all — `com/mojang/blaze3d/audio` is taught whole by
  `client/sound-engine`, the statistics criterion parse is
  `scoreboard-and-data`'s near word for word, and the recipe book is
  `items/recipes`' — each reframed as an *address* finding, which is what the
  page is actually for. **Seams:** the citation form applied across both
  parts, with the anchor; the two parts' four through-line owner pages take 75
  inbound links between them and one carried an anchor before this session.
  Three pages assumed a page they never linked (`data-driven-types` leans on
  `resource-system`'s `scanDirectory` four times; `tags` and `codecs-nbt-json`
  name the four threads and never link `anatomy`). Two hand-forwards made
  *to* `resource-system` were unpaid and are now paid: *linkfs* and
  `DownloadQueue` with `DownloadCacheCleaner`. **Coverage:** the charter's
  §7 entry discharged — **feature flags** get a section on
  `identifiers-and-registries`, because what a flag does is filter a
  `HolderLookup.RegistryLookup` over the seven registries in
  `FeatureElement.FILTERED_REGISTRIES`, which is that page's subject; the pack
  half stays on `resource-system` and links it. `GameConfig`, Part I's one
  gap, closed in a clause. **The landing pages, rewritten last.**
  `anatomy/README` was the worst page in its part, for the reason pass 4 found
  three parts running: its figure drew the *book* — the twelve other parts
  fanning off four threads — rather than the part's own two pages, breaking
  `TEMPLATE.md`'s rule and standing as a third, disagreeing statement of Part
  I's place in the parts graph. Redrawn to its two pages; the hook that said
  "a server that ticks and a client that draws" now contrasts the two loops;
  the opening sentence no longer collides with Part II's (both claimed to be
  "the vocabulary the other twelve parts speak", back to back); a *where the
  part stops* paragraph added; and the reason the boundary page is second
  moved in from `lectures.md`. Part II's shape sentence called the part a
  stack while its own figure drew a two-rooted fan. **Two corrections**, both
  re-derived with the decompile open and logged in [pass9.md](pass9.md):
  `MappedRegistry` is keyed **four** ways, not three — `byValue` is an
  identity map and is what `Registry.getKey` reads — and `StreamTagVisitor`'s
  "two fields" is two for `IOWorker` and three for `StructureCheck`. One
  reported contradiction was re-derived and found to be none. **One tool bug**,
  the sixteenth of the project and the first this pass: `map_source.py` and
  `pass5_coverage.py` gave different populations for the same packages (Part I
  as 7 classes and as 6) under a comment in `map_source.py` claiming they
  "can never disagree" — `package-info.java`, counted as a file by the atlas
  and dropped by the coverage tool. Nothing false was published, because no
  landing page states a Part I size; both tools now name their population.
  Five gates green. Six queue entries struck, one §7 entry discharged, and
  what the reading raised for sessions D, E, G, J, K, M and N and for passes 6
  and 8 appended to [pass5.md](pass5.md) rather than left in the log.
- **2026-09-05, session C — Part III · The server (pass 5).** Six pages read
  by one agent each, the part read end to end in watching order first. **All
  six rewritten**, and this was the session where the lens paid twice: five
  mechanisms cut to a citation, and **six corrections** — the most any pass-5
  session has found, all of them at a seam. Reading two pages side by side is
  what a page-at-a-time check cannot do, and four of the six were pages
  disagreeing with each other: `how-a-server-dies` had the autosave at "every
  6000 ticks, five minutes of game clock" where `server-tick` and
  `chunk-storage` both had wall clock (the countdown is
  `tickrate × 300`, floored at 100); `starting-a-server` had a missing
  JSON-RPC secret killing the boot where `what-this-book-skips` had it
  generated (the property's default *is* a generated key, and the throw is
  for a malformed one); `server-tick` had the `/schedule` queue ticking "with
  the dimension's own game time" where its own declared pair had overworld
  only (`ServerLevel.tickTime` is wholly inside the overworld flag); and
  `server-level-tick` had `NaturalSpawner.createState` skipping only
  persistent mobs where `entity-lifecycle` also had `MobCategory.MISC`. The
  other two were unforced: `DerivedLevelData` was credited with sharing the
  time of day, the weather and the world spawn between dimensions, and it
  causes none of the three (they belong to `ServerClockManager`, a
  server-wide `WeatherData`, and `MinecraftServer.effectiveRespawnData`); and
  `ChunkMap.forEachBlockTickingChunk`'s second filter was missing. Six more
  suspicions were re-derived and **found sound**, and are recorded as such,
  because a strike is a claim. **Ownership:** the crash relay cut to a
  citation (session B's ruling, applied), the stopped server's two task doors
  moved to shutdown with *RejectedExecutionException* carried across,
  `session.lock` given wholly to `starting-a-server`, the `level.dat` write
  path ruled the Reference page's and cut from three tellings to one, the
  ticket-persistence half given to `tickets-and-loading` while
  `how-a-server-dies` keeps the sentence that says why its drain loop ends,
  *Done* given to `starting-a-server`, and the flush bracket and the latency
  sweep given to `server-tick`. **Seams:** twenty-eight outbound links gained
  the owner's anchor (Part III had none before this session), and three
  hand-forwards were repointed at pages that actually keep them — login
  encryption to `protocol-phases`, the two-place player tick to
  `the-two-phase-tick`, the permission model to `permissions`.
  **Coverage:** `server/players`' ten-class stored-user-list family and
  `CachedUserNameToIdResolver` — the part's largest unnamed class — get a
  passage on `players-and-sessions`, which was already explaining what those
  files do without naming what reads them; `PlayerDataStorage`'s corrupt-copy
  rescue, promised by a cast cell for two passes, is finally written; and
  `Bootstrap`'s `LoggedPrintStream` explains why `Bootstrap.realStdoutPrintln`
  exists. **The §7 gap closed: the abstract `Level`**, as a paragraph on
  `server-level-tick` rather than a section or a page, because
  `the-client-level` already had half the answer and what was missing was the
  join. The other new passage is the tick's **profiler zone names** in order —
  ten pages in five parts cite the level tick's phases by those names and no
  page defined them. **The landing page**, rewritten last to the role: it now
  argues that almost everything surprising about a server's timing is the
  order of one method, states its size through the include, carries the pair
  claim that `lectures.md` had been keeping for it, and gains a *where the
  part stops* section — 2,522 lines of the part's own packages are taught in
  six other parts and it said nothing about that. **Rulings:**
  `how-a-server-dies`' durability section is a section and not a page (it is
  the comparison table's payoff, and what did not belong to it has gone to
  its owners); `players-and-sessions`' *four ways* heading stands over a
  paragraph naming a fifth, because the concession is what makes it honest.
  Five gates green. Six queue entries struck, one §7 entry discharged, and
  what the reading raised for sessions D, E, F, H, I, L, M and N and for
  passes 6, 7 and 8 appended to [pass5.md](pass5.md) rather than left in the
  log.
- **2026-09-05, session D — Part IV · The world (pass 5).** Eleven pages plus
  the part's Reference page, one agent each, the part read end to end in
  watching order first. **All twelve rewritten**, and four pages in three other
  parts edited because a Part IV page disagreed with them. **Nine corrections**
  — the most of any pass-5 session — of which **five were one page contradicting
  another**, which is now the shape three sessions running: `chunk-anatomy` and
  `chunk-storage` gave incompatible accounts of what an `ImposterProtoChunk`
  delegates (all three of `markUnsaved`, `isLightCorrect` and `setLightCorrect`
  pass through; the two flat falses are `canBeSerialized` and `tryMarkSaved`);
  `lightmap-fog-and-sky` had the lightning lerp at "a fifth" where the owner had
  22% and the decompile has `0.22F`; `what-the-client-is-told` had the
  once-a-second time sync carrying "a map of clock updates" where
  `MinecraftServer.forceGameTimeSynchronization` sends `Map.of()`;
  `server-level-tick` and `scheduled-ticks` named different readers of
  `GameRules.RANDOM_TICK_SPEED` (it is read once per level tick in
  `ServerChunkCache.tickChunks` and handed down); and `level-data-and-rules`
  sent the reader to `server-tick` for day time while the environment page
  claimed it pointed here. The four unforced ones were all *within* a page:
  `chunk-anatomy` said packing "buys a smaller palette, **not** narrower
  entries" and then gave two cases where it narrows them; `lighting` said
  `LightEngine.checkNode` "only decides what to enqueue" and then described it
  writing stored levels — both engines' do; `scheduled-ticks` said "two type
  parameters" where every class declares one; and `chunk-storage` said loading
  "changes hands four times" where four stages share three lanes. **Six more
  suspicions were re-derived and found sound** and are recorded as such,
  including two fours a reader meets four pages apart that really are different
  constants. **Ownership:** seven mechanisms cut to a citation — the ticker
  wrappers to `block-entities`, the random-tick walk and the level tick's own
  second telling of the drain, the worker-pool sizing and *what a
  `ConsecutiveExecutor` is* to `anatomy`, the level→status line and the
  synchronous ask to `tickets-and-loading`, `ChunkStatusTasks.isLighted` to
  `lighting`, the mesh gate and the poll budget out of `lighting`'s client coda,
  and the whole chunk-batch pacing out of `tickets-and-loading` to Part IX,
  which already owned it and said it better. Two mechanisms moved rather than
  cut: the `SavedDataStorage` write path off the Reference shelf onto
  `chunk-storage`, where the copy-encode-write shape already lives, and the
  read path's failure branch — `ChunkMap.handleChunkLoadFailure` and the
  null parse, homeless since pass 3 proposed the move — onto
  `chunk-generation-pipeline`, which settles the last open proposal in the
  part. **Seams:** Part IV carried **no anchor at all** on any outbound link
  before this session and now carries thirty-seven. **Coverage:** the part was
  already 96% named, so the work was the mechanisms rather than the names —
  `ChunkResult` and `PlayerMap` (session C's routing) on `tickets-and-loading`,
  the `world/clock` trio and what the client's copy of a clock does *not*
  receive on the environment page, `util/worldupdate` taken rather than declined
  as *Optimize World* on `chunk-storage`, `LiquidBlockContainer` on `fluids`,
  and the fact the brief asked for with the decompile open: `PoiManager.isVillageCenter`
  reads through the **non-loading** `SectionStorage.get`, so **a village is made
  of loaded sections only**. **The §7 entry the schedule set is a decline, not a
  discharge**: `WorldBorder` is 573 lines whose only explanation is a Reference
  page, and rather than invent a lecture for a mechanism with no scenario,
  session D declared it Reference-only in both places with the reason stated,
  and wrote the ruling into §7 for the second edition to disagree with. **The
  landing page**, rewritten last, gains a *where the part stops* section (2,900
  lines of its own packages taught in six other parts), loses the superlative
  its own figure contradicted, and has five blurbs re-synced word for word to
  the pages they summarise; `lectures.md` follows it on the conveyor's length
  and drops *self-contained* from a page inside a chain. **One tool bug, the
  seventeenth of the project and the first that was hiding failures rather than
  publishing a falsehood:** `check_links.py` scanned line by line, so it could
  not see a link whose text wrapped across a newline — **243 of 7,811 links had
  never been checked**, the gate called this session's own broken anchor clean,
  and on the first run after the fix it caught two real breaks, one of them an
  anchor this session had invented. The number of anchors the gate actually
  checks went from 12 to 174, which is pass 5's own anchor work finally coming
  under it; `--probe` now proves the wrapped case both ways. Five gates green.
  Twelve queue entries struck, one §7 entry ruled out with its reason, and what
  the reading raised for sessions E, F, I, K and N and for passes 6, 7 and 8
  appended to [pass5.md](pass5.md) rather than left in the log.
- **2026-09-05, session E — Part V · Blocks (pass 5).** Seven pages plus the
  part's Reference page, one agent each, the part read end to end in watching
  order first. **All eight rewritten**, and four pages in three other parts
  edited because a Part V page's owner or duplicate lived there. **Six
  corrections**, of which four were again one page contradicting another — the
  shape four sessions running. The Reference page said
  `Block.UPDATE_INVISIBLE` suppressed the broadcast on either side; bit 4 has
  exactly one reader in the game and the test sits inside the client-side arm,
  so a server write carrying it still broadcasts — and `blocks-and-states` had
  it right all along, which makes this a catalogue contradicting its own
  lecture. `scheduled-ticks` had `DiodeBlock.shouldPrioritize`'s condition
  **inverted** (it fires when the diode in front *is* pointing back, not when
  it is not), and the copy that survived the session's own cut is the correct
  one. `block-interaction` had `Minecraft.startUseItem`'s `isDestroying` test
  as a condition on setting the four-tick delay where it wraps the whole method
  body, understating what `prediction-and-acks` already had right. And the
  glossary said a block event "lands late", which inverts the page's argument
  that the queue is a wait for a named phase rather than a delay. The two
  unforced ones were within a page: `diodes-and-observers` said
  `RepeaterBlock.LOCKED` was the only property computed from a redstone reading
  *outside* tick time and then that `DiodeBlock.POWERED` was the only one
  computed from a reading at all — each clause denying the other, where the
  truth is two properties differing in *when* — and `signal-and-dust`'s "all
  three stop early" hung on a table of three direction *arrays*, two of which
  are fan-out orders that never stop early; the claim is true of the three
  reading methods inside the first row. **Seven suspicions were re-derived and
  found sound** and are recorded as such, including two the agents read as
  contradictions and are not: a client write reaches the renderer through
  **two** doors, only one of which is gated on `ModelManager.requiresRender`,
  and `Block.UPDATE_LIMIT` and `CollectingNeighborUpdater.maxChainedNeighborUpdates`
  are genuinely two budgets over two cascades. **Ownership:** the queue's
  standing question — whether any of the six spokes had started re-explaining
  the hub's two update channels — came back **yes**, and
  `block-interaction`:174-180 was restating all three method bodies verbatim;
  cut to the door's consequence and the anchor. Six more mechanisms cut to a
  citation: `Block.updateOrDestroy`'s server-gated destroy (told three times,
  and the flags-3 detail *moved* to the hub rather than dropped), the flag
  word's definition and `Block.UPDATE_LIMIT`'s (the Reference page's own
  opening, reproduced sentence for sentence), the neighbour channel's direction
  order, `SignalGetter.getSignal`'s conductor gate (to `signal-and-dust`), the
  *except*-entity sound rule (to `what-makes-a-sound`), and the block-event
  queue's four rules, which `server-level-tick` and the piston page both
  stated in full and which now live once. The 10.00 duplication pair session D
  handed over — the repeater's booking, near-verbatim on two pages — was cut on
  `scheduled-ticks`' side, because rule 1 gives all three of its bold
  paragraphs to the diode page and rule 4 therefore never applies; what stayed
  is the queue's own half, that a booking cannot be called off. One mechanism
  moved the other way: the fact that `ChunkHolder.broadcastChanges` reads the
  level *again* when it builds the packet — which is what
  `signal-and-dust`'s hook rests on and which its owner in Part IX did not have.
  **Seams:** Part V carried **no anchor on any cross-part link** before this
  session and now carries thirty-seven; one link was landing on the wrong page
  entirely (`blocks-and-states` cited `signal-and-dust` for
  `Level.updateNeighbourForOutputSignal`, a method that page never names).
  **Coverage:** Part V is the book's lowest at 40% of lines named, and the
  session's finding is that the number is mostly right to be low — the 344
  unnamed classes are one `Block` subclass each — but that **no page said so**.
  The landing page now does, and five family sentences discharge what a
  sentence can reach: the three `block/state/` sub-packages and
  `InstantNeighborUpdater`, the redstone sources, the seven block-event raisers
  and `PistonMath`, the `block/entity` family with the hopper's cadence, and
  the use-hook family — for which the count [pass5.md](pass5.md):1734 asked to
  be restored was re-derived (25 blocks override `BlockBehaviour.useItemOn`, 52
  `BlockBehaviour.useWithoutItem`). Four mechanisms are declared too big for a
  sentence and go to §7 for the second edition: **the hopper**, which three
  pages gesture at and none explains; the sculk *spread* machine; the structure
  and command blocks, named nowhere in `src/`; and the beacon, conduit,
  trial-spawner and vault state machines, half-adopted by Parts VI and VII.
  **The §7 block-event entry is discharged and its count corrected** — three
  blocks, not four; the fourth was `ComparatorBlock`, whose override the page
  itself shows is dead. **The landing page**, rewritten last to the role: it now
  opens inside two scenarios rather than on book furniture (a door that swings
  both halves, a lamp that waits), states its size through the include, names
  the four kinds of answer its verified line had promised and no page
  enumerated, and gains a *where the part stops* section — about ten thousand
  lines of its own packages are taught in six other parts. **Rulings:**
  `signal-and-dust`'s experimental evaluator stays as the page's counterfactual
  (no other page can own it, and it answers the question the page's own
  scenario raises), with a pass-6 note to run the same lever and two dust
  through it; `block-entities` needs no fourth clause on the landing page, so
  the queue's *odd page* entry is settled by rewriting the argument rather than
  the part. **The tools found nothing wrong this session** — the first pass-5
  part session with no tool bug. Five gates green. Eight queue entries struck,
  one §7 entry discharged with a corrected count, and what the reading raised
  for sessions G, H, I and K and for passes 6, 7 and 8 appended to
  [pass5.md](pass5.md) rather than left in the log.
- **2026-09-05, session F — Part VI · Entities (pass 5).** Nine pages plus the
  part's Reference page, one agent each, the part read end to end in watching
  order first. **All ten rewritten**, and three pages in three other parts
  edited because a Part VI page's owner or duplicate lived there. **Thirteen
  corrections**, the most of any pass-5 session, of which **eight were one page
  contradicting another** — the shape five sessions running — and three were a
  page contradicting *itself*. The sharpest is the part's own through-line
  owner getting a phase wrong: `authority` had a `ServerPlayer`'s physics
  running "during the entity phase of its tick", where `ServerPlayer.tick` does
  not call up at all and `ServerPlayer.doTick` runs in the **connection** phase,
  after every level has ticked — and it credited the discard to the next
  movement packet, where the bracket itself snaps the player back the moment
  `doTick` returns. `the-two-phase-tick` had both right, so the page four other
  parts cite for the premise was the one telling it wrong. Beside it:
  `damage-and-death` had the invulnerability window **inverted** (the excess
  rule applies in the ten ticks the red flash is showing, not the ten after
  them, and the second ten protect nothing); `attributes` repeated one clause
  twice and got the third wrong, because `Attributes.MOVEMENT_SPEED` and
  `Attributes.ARMOR` are both already in the living base a zombie overrides;
  the Reference page said twelve of the twenty-one inherit `Entity.hurtClient`
  where it is thirteen, and compressed `VehicleEntity`'s creative branch into
  the opposite of what its own lecture says; `authority` said "three of those
  eight read the same member" over a list showing four; `ai-goals-and-brains`
  said "everything it will ever do" of a zombie that gains a thirteenth goal
  when it learns to break doors; and `entity-anatomy` glossed `entity/schedule`
  as "villager day plans" when the package holds `Activity` and nothing else —
  the exact opposite of the AI page's hook. **Five suspicions were re-derived
  and found sound**, including the brief's own claim that `entity-lifecycle`
  links `chunk-anatomy` nowhere, which was overtaken. **Ownership:** eight
  mechanisms cut to a citation — `EntityType.create`'s gates (the charter's
  named duplicate, settled to `entity-anatomy` with the spawner's *consequence*
  kept on `entity-lifecycle`), `EntityReference`, the eight base synched
  accessors, `EntityType.trackDeltas`' ten-type list (which the page's own cast
  had promised not to carry), the pose loop's third telling, the two mob caps
  and the custom-spawner roster off `server-level-tick`, and `AcquirePoi`'s
  mechanics and `SleepInBed`'s conditions off `ai-goals-and-brains` to Part IV,
  which owns the claim as its scenario. Two moved the other way: the update
  intervals to `entity-anatomy`, which owns the type's numbers, and
  "unbounded by distance" into `pathfinding`, which owns the walk. **Seams:**
  Part VI carried **no anchor on any of its 69 outbound links** before this
  session — the third part running — and now carries them throughout; one
  hand-forward pointed at a page that disclaims the thing (`damage-and-death`
  → `player-anatomy` for the respawned object) and one at a page that never
  owned it (`points-of-interest` → `ai-goals-and-brains` for the pathfinder).
  **Coverage:** Part VI is the book's largest part and 61% named by lines, and
  the session's answer is that the shortfall is species — one `Mob` subclass
  each, and the 164 classes of the two AI libraries are one shape each, now
  said once. Three passages were written for what is *not* species: the
  structure spawn-list override and the hard-coded Nether-fortress list in
  front of it (**§7's `Structure.spawnOverrides` entry half-discharged** — the
  mechanism is stated, the table is still session N's view); what an
  `EntitySection` is, so that *findable* means something; and the
  fall-attribution threshold, homeless since pass 3, which is why a death
  message says *was doomed to fall by*. Four mechanisms are declared too big
  for a sentence and go to §7: the minecart's two movement models, the ender
  dragon's sixteen phases, a raid, and villager gossip. **The landing page**,
  rewritten last to the role: it opens on five surprises and one question
  rather than on a book transition, states its size through the include as the
  largest part of the book, gains a *where the part stops* that says why 40% of
  its lines are named nowhere, and corrects `Avatar` from "below `Player`" to
  above — four other pages say between `LivingEntity` and `Player`. **One tool
  bug, the eighteenth of the project:** `map_source.spec_text` rendered a
  part's package set inline, so a subtracted package followed by additions read
  as though *minus* governed the whole tail — Parts VI and IX each printed four
  packages they **include** as exclusions, on `maps/packages.md` and in every
  part's coverage-report header. Two agents caught it independently.
  Subtractions now come last and share one *minus*; `--probe` proves three
  shapes. Five gates green. Six queue entries struck, one §7 entry half-
  discharged and one written, and what the reading raised for sessions H, I, J,
  K, M and N and for passes 6, 7 and 8 appended to [pass5.md](pass5.md) rather
  than left in the log.
- **2026-09-05, session G — Part VII · Items and inventories (pass 5).** Eight
  pages plus the landing page, one agent each, the part read end to end in
  watching order first. **All nine rewritten**, and five pages in three other
  parts edited because a Part VII page's owner or duplicate lived there. This
  is the session that settled **the top duplication pair in the book**:
  `data-components` ↔ `items-and-stacks` at 17.00, which the queue described as
  the same lecture twice and which was worse than that — `items-and-stacks`'
  own opening hook was Part II's mechanism, twice over. The line drawn is that
  **Part II owns the component system's machinery** (the type, the maps, the
  patch's sanitising and copy-on-write, the prototype's two-phase build) and
  **Part VII owns the stack as an object** (its four fields, the five identity
  methods, the two validators, `ItemStackTemplate`, durability, the tick, the
  `ItemEntity`); six mechanisms were cut to a citation on the Part VII side and
  three moved *to* Part II, while the validators, `ItemStackTemplate` and
  `ignoreSwapAnimation` moved the other way and `data-components` was cut to a
  clause on each. The page's hook is now the one thing only it can say — that
  durability is what a client never predicts — and `items/README`:47's promise
  that this part "never re-teaches the component system" is true for the first
  time. **Twelve corrections**, of which **four were one page contradicting
  another** and three were a page contradicting *itself*. The sharpest is
  `enchanting`'s claim that the table, the providers and the loot paths all
  roll in `EnchantmentHelper.selectEnchantment`, which the same page denies
  twice below: the method has four callers, and `SingleEnchantment` — six of
  the seven vanilla providers — and `EnchantRandomlyFunction` roll their own.
  Beside it: `loot-tables`' sequence diagram put `LootTable.createStackSplitter`
  on the pool's return where it wraps the whole fill outside the table's own
  functions (its flowchart and its prose both had it right, so the page
  disagreed with itself in two figures); `containers-and-menus` compared a
  click's traffic as "128 integers" where a `HashedStack` carries one integer
  per *component*; `using-an-item` attached "its only override" to
  `ItemStack.useOnRelease` where `Item.useOnRelease` is the hook; `enchanting`
  and `enchantments` gave flatly opposed accounts of how the anvil decides it
  is holding a book, and both were right about **different slots**, neither
  saying which; `loot-tables` counted thirteen path prefixes and listed twelve;
  `contexts-and-predicates` named three of the four keys `ALL_PARAMS` omits;
  `enchantments` named the guard rather than `SmeltItemFunction` as what cooks
  the loot; `resource-system`'s reload list was short the per-player recipe-book
  re-send that makes a Part VII claim true; and the landing page carried two
  claims its own pages contradict — that the three engines "hand each other
  nothing", and a sword-swing symptom that is Part VIII's hook. **Seven
  suspicions were re-derived and found sound**, including the *two spellings*
  hook (`DataComponents.DAMAGE` at reload time against
  `DataComponents.MAX_DAMAGE` at stack time — genuinely two components) and the
  landing page's unhomed claim that `/reload` never re-reads an enchantment,
  which is true and now has a home on `enchantments`. **Seams:** Part VII
  carried **two anchors on forty-six cross-part links** before this session —
  the fourth part running to start with almost none — and now carries them
  throughout; seven *taught in* cells on `data-driven-types` were re-pointed at
  pages that actually name the element, five of them Part VII's rows, two of
  which had been sending readers to a page where *no* page named the class.
  **Coverage:** Part VII is 64% named by lines, and the answer is four families
  (the `world/item` subclasses, the twenty-nine menus, the loot functions and
  conditions, the special crafting recipes) each said once on the page that
  teaches the machine — plus **four systems that are not a family and are
  explained nowhere**: villager trading (the part's largest unnamed class),
  brewing, the creative tabs, and armour identity and trims, all four named and
  declined on the landing page and written into §7. Two §7 entries were
  discharged: the `Item.getUseDuration` roster, lost prose since pass 3, is now
  a sentence on `using-an-item` with the base method's own three-way answer in
  front of it (a Reference row declined — eight overrides is not a catalogue);
  and the predicate shape library was **ruled rather than moved**, staying a
  table on `advancements` with `contexts-and-predicates` gaining the citation
  it owed. **The landing page**, rewritten last to the role: it gains a *where
  the part stops* section with the size through the include, replaces a Part
  VIII symptom in its argument with one of its own, and stops claiming the
  engines are independent. **The tools found nothing wrong this session** — the
  second pass-5 part session with no tool bug. Five gates green. Eight queue
  entries struck or settled, two §7 entries discharged and one written, and what
  the reading raised for sessions H, I, J, M and N and for passes 6, 7 and 8
  appended to [pass5.md](pass5.md) rather than left in the log.
- **2026-09-06, session H — Part VIII · The player (pass 5).** Seven pages plus
  the landing page, one agent each, the part read end to end in watching order
  first. **All eight rewritten**, and nine pages in six other parts edited,
  because almost everything a Part VIII page reaches for is owned elsewhere.
  The part's own duplicate was the largest: the two trunk pages opened on the
  same surprising fact and both explained the record-simulate-snap-back bracket
  at length, two lectures apart; `the-two-phase-tick` owns it now, taking the
  riding qualifier with it, and `input-to-movement`'s opening ends on its own
  three surprises. Across the seam with Part VII, `Consumable` **split along
  rule 1 rather than routing whole** — the field roster and the five
  `ConsumeEffect`s to `using-an-item`, the `ConsumableListener` walk kept on
  `hunger-and-experience` because it is that page's own hook — with the session
  writing down why the routing rule's default was declined. The pass's largest
  single move: `Player.cannotAttack`'s two hooks and projectile deflection off
  `reference/non-living-damage`, where a Reference page had been holding the
  book's only explanation of `Player.attack`'s own first two gates, onto
  `the-sword-swing`; the sharper reading came back the other way, that the
  wrapper's boolean means *was anything damaged*, not *did the hit land*.
  **Eight corrections**, three of them a page disagreeing with another page and
  two a page disagreeing with a Reference page: `Avatar` does not exist for the
  renderer (it is a server class, and it is what `Player` and `Mannequin`
  share); `postPiercingAttack` is `LivingEntity`'s, which the page's own
  declared pair already said; `getSecondsToDisableBlocking` is conditional, on
  two pages; `MobEffectInstance.compareTo` orders both surfaces and in opposite
  directions; the ambient-particle bound is four and fifteen, not "about four";
  the flying kick's vehicle half runs a second counter; `Player.HELD_ITEM_SLOT`
  is the cursor; `DemoMode` reads the level's clock. Four suspicions re-derived
  and found sound. **Coverage:** the part is small enough that the question came
  back *yes* — 97% of Part VIII's lines are named somewhere — and the landing
  page now makes that its argument instead of leaving it unsaid. Part VIII is
  the fifth part running to arrive with **no anchors at all**; seventy-one were
  added. **No tool bug**, the third pass-5 part session without one. Five gates
  green.
- **2026-09-06, session I — Part IX · Networking (pass 5).** Five pages plus the
  landing page, one agent each, the part read end to end in watching order
  first. **All six rewritten**, and eleven pages in seven other parts edited.
  **Seventeen corrections**, the second-most of any pass-5 session, of which
  **eight were one page contradicting another** and **five a page contradicting
  itself** — the shape seven sessions running, and the self-contradictions are
  the new high. Four of the eight cross-page ones were about the same seam,
  Part IX against Part III: `the-connection` had the flush bracket "around the
  whole server tick" where `MinecraftServer.suspendFlushing` opens it at the
  top of `tickChildren`, so the packet drain is outside it — the thing
  `players-and-sessions` turns on; it had `PacketListener.onPacketError`
  "by default raising a reported crash", which is the interface default and is
  reached by **no listener a drained packet ever arrives at** (the server logs
  and suppresses, the client disconnects), so a reader of that page alone had
  the outcome backwards; and `server-tick` had `Connection.tick` flushing "at
  the end of the connection phase" against its own step list, and called
  `Connection.pendingActions` a "deferred send queue" when it holds closures and
  `Connection` keeps no packet queue at all. The five self-contradictions:
  `what-the-client-is-told` counted "**four** feeds ignore gate 3" over a
  section and a figure naming three, and said gate 2 keeps every distant mob
  silent where its own Q&A says otherwise twice; `packets-and-stream-codecs`
  said trust is "not about direction" and then "the rule is direction", and
  said client-supplied component contents "never cross the wire at all" twenty
  lines under the packet it calls the one that carries an arbitrary item;
  `chat-and-signing` answered that vanilla "never sends" an unsigned copy on a
  page that says twice above that it does. Beside them: the block-entity
  broadcast named the wrong method; the block broadcast was "once a tick"
  where it is inside `ServerChunkCache.tickChunks` and never in a debug world;
  and `player-anatomy` and `player/README` both put a `ProfileKeyPair` on a
  `ServerPlayer`, where there is no such field anywhere in `server/` — what it
  holds is the public half, a `RemoteChatSession`. **Four suspicions re-derived
  and found sound**, including two pages naming the same save read in two
  places, which turn out to be one place. **Ownership:** four mechanisms cut to
  a citation on the Part IX side (the flush bracket, the memory-connection
  crash's sibling copy, the registry-and-tag sync, `PrepareSpawnTask`'s
  internals) and four the other way (keep-alive, the chunk-batch loop, the
  trusted constants and the creative slot's three fences from
  `codecs-nbt-json`), with the chat hop's **fourth** telling cut from
  `brigadier-and-commands`. **The shape sentence, open since pass 4, is
  decided**: Part IX is *the wire three times, and two things it carries*, and
  the landing figure's two unlabelled arrows — which asserted a dependency the
  page's own prose denied and neither target page uses — are redrawn with it.
  **Seams:** Part IX carried **7 anchors on 62 cross-part links** before this
  session, the sixth part running to arrive with almost none, and carries 67
  now plus 23 inside the part; three pages in three parts had been citing
  `the-connection` for the thread hop at an anchor that is about
  `EventLoopGroupHolder`'s event-loop groups — **an anchor session A itself
  declared**, and the brief's A3 row is corrected with the reason. **Coverage:**
  Part IX is 84% named, and the session's finding is that the number is
  legible only once the landing page says **this part owns the wire, not
  everything in `network/`** — `network/chat` is Part II's, much of
  `client/multiplayer` is Part X's, and the largest block is the packet
  classes, which are catalogued rather than narrated. Three passages were
  written for what is none of those: **the text filter**, ~750 lines in the
  part's own `server/network` that `chat-and-signing`'s trace runs straight
  through without naming a class; **the per-phase listener interfaces**, ~700
  lines that are what `Packet.handle` targets and were named nowhere; and
  **`client/multiplayer/resolver`**, the six classes that turn a typed address
  into a socket, where the part's own scenario begins. Three more systems are
  named and declined with a reason on the landing page, and the **boss-bar
  feed** — the part's largest unnamed class, whose sending side has no owner
  anywhere in the book — is written into §7 beside the `execute store` sink it
  is the other end of. **No tool bug**, the fourth pass-5 part session without
  one. Five gates green. Twelve queue entries struck or settled, one §7 entry
  widened, and what the reading raised for sessions J, K, M and N and for
  passes 6, 7 and 8 appended to [pass5.md](pass5.md) rather than left in the
  log.
- *From session J on, a part session's record is the "Session … is done"
  paragraph under **Where we are** above, which is where sessions J to O wrote
  theirs; this list is not continued in parallel.*
- **2026-09-07, session O — the close. Pass 5 is done.** Its record is
  [pass5-brief.md](pass5-brief.md), whole: the charter, the rulings session A
  made, the runbook every session ran, and the schedule with what each of the
  fifteen did. What the pass found, what it left and whether it was worth it are
  under **Where we are** above; what it left for later is in
  [pass5.md](pass5.md) by kind and in [pass9.md](pass9.md) as claims to check
  first. **Pass 6 — the lecture — is next**, and its charter is below with the
  devices counted afresh at the close. The next session is pass 6's planning
  session (Fable), which builds `pass6_prompts.py` and writes the brief.*
