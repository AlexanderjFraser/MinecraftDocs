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
   it under the ownership rule (the page whose scenario the mechanism is the
   answer to; between parts, the earlier one; within a part, the page whose
   figure draws it; a vocabulary page owns what a thing *is*, a trace owns what
   *happens*; Reference owns lists); and what the other page keeps, which is at
   most one sentence and a link. If the second explanation says something the
   owner lacks, say so: that is a move, not a cut.
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
- **The deliberate pairs stay.** Two pages that share a preamble on purpose
  (the two click lectures of Part V) are one lecture in two halves; report a
  drift between the two copies, not the copy.
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

Session A makes the rulings once so that thirteen part sessions apply them
rather than re-deciding them. Its outputs are edits to `TEMPLATE.md`, to this
file (Part 3's tables, filled in), to the frame, and to one exemplar landing
page. Its checklist:

### A1. The ownership rule, written into `TEMPLATE.md`

The planning session's draft, for session A to confirm or amend:

> **One home per mechanism.** A mechanism is explained on one page — the
> page whose scenario the mechanism is the answer to — and every other page
> that needs it spends at most one sentence and a link to the owner's anchor.
> Between two candidates in different parts, the earlier part owns it,
> because later parts assume earlier ones and a link back costs the reader
> nothing while a link forward is a promise. Within a part, the page whose
> figure draws the mechanism owns it. A vocabulary page owns what a thing
> *is*; a trace owns what *happens*. A Reference page owns an enumeration
> and may carry the one paragraph that makes its table readable, never an
> explanation a lecture should give. **A link points from the page that
> assumes to the page that explains**, at first use; a link into a later part
> is allowed only as a declared dependency (a landing page's *before you
> start*, drawn dashed on the figure) or in a sentence that says the later
> page pays it off. **A summariser never explains**: the landing pages, the
> lecture map, the glossary and the introduction restate pages, and when one
> disagrees with its page the page wins and the summariser is corrected in
> the same session, after the page.

### A2. The landing page's role, written into `TEMPLATE.md`

The shape table's row today says: *one paragraph · the figure · before you
start · watch in this order · the Reference pages it uses; under a hundred
lines, no trace*. Session A expands it into the role the charter names, with
the exemplar beside it:

- **The argument** — one paragraph that says what the part claims about its
  system and what the reader will be able to explain afterwards; the part's
  hook, not a summary of its pages. Starts inside a scenario like any page.
- **The size** — one sentence, its number from
  `{{#include ../../generated/part-<dir>.md}}`, naming the packages the way
  `src/generated/parts.md` does; and the sentence that says what the part
  declines, pointing at *what this book skips*.
- **The shape** — the part's shape as a figure of its pages (a chain, a hub, a
  stack, a ladder), with the sentence that names the shape.
- ***Before you start*** — only true dependencies, each with the sentence that
  says what the part uses it for; a hand-forward lives outside this section.
- ***Watch in this order*** — the pages with a one-sentence blurb each; the
  order is the part's argument in miniature, and `lectures.md` copies it
  (session A decides whether the lecture map keeps blurbs at all — the
  planning session's recommendation is that it keeps the order and the
  dependencies and drops the blurbs, which duplicate every landing page and
  drift every pass).
- **The Reference it uses** — one line per page, what the part reads it for.
- Under a hundred lines; no trace; no cast; the rules footer.

**The exemplar**: Part XIII's landing page is the best-argued today (*a stack
of three floors*, and the dependency runs one way); session A rewrites it to
the role above as the model, size sentence included, and the part sessions
follow it.

### A3. The through-lines: owners and the citation form

Seven ideas cross parts. The planning session measured how many pages carry
each (mentions, by `pass5_dups.py --terms`; the sets are in
`pass5_prompts.py`'s `THROUGH_LINES`, and session A refines them):

| through-line | pages carrying its terms | where it is told most | proposed owner |
|---|---:|---|---|
| the tick and its phases | 26 | `server-tick` (18), `server-level-tick`, `input-to-movement`, `anatomy` | `server/server-tick` — the phase table is the citation target |
| the four threads | 72 | `how-a-server-dies` (25), `anatomy` (24), `reference/threads` (23), `resource-system` | `anatomy/anatomy`, with `reference/threads` as the table |
| the wire and the hop | 28 | `the-connection` (24), `reference/threads`, `anatomy`, `server-tick`, `sound-engine` | `networking/the-connection` |
| authority and prediction | 35 | `authority` (52), `prediction-and-acks` (31), `movement-and-collision`, the glossary | `entities/authority` for authority; `client/prediction-and-acks` for prediction |
| the registry freeze and the reload | 39 | `resource-system` (29), `identifiers-and-registries` (27), `tags` (25), `data-driven-types` | `identifiers-and-registries` for the freeze; `resource-system` for the reload |
| the data-driven type pattern | measured loosely (the terms are common words) | `data-driven-types` (47) and then every part that has an instance | `foundations/data-driven-types` |
| the ledger | 18 | `prediction-and-acks` (35), then the two click lectures at 3 each | `client/prediction-and-acks` |

Session A confirms the owners, decides whether the introduction, `anatomy` or
a new page is *lecture zero* for the ones every part uses (the planning
session's recommendation: no new page — `anatomy` already is lecture zero for
the threads, the loops and the wire, and the introduction stays short), and
writes into this table the **citation form** each other page uses — the one
sentence and the anchor — so the part sessions cut retellings to it.

### A4. The duplication report, routed

`python tools/pass5_dups.py --summary --top 100` is the corpus-wide list.
The routing rule: **a cross-part pair is resolved by the later part's
session**, which reads the earlier page as it then stands; a within-part pair
by the part's session; a pair with a Reference page by the part whose landing
page points at that Reference page. Session A writes the routed list into
Part 4 (the planning session's first cut is there already) and notes any pair
it thinks is a link doing its job, so a part session does not spend an agent
on it.

### A5. The frame's own seams

The introduction, `lectures.md`, the maps' and Reference's front pages, and
`SUMMARY.md` — read as the book's argument:

- The **nine-page dependency table** on `lectures.md`: state its membership
  rule (pass-4 session A's finding — by its own criterion three Part II pages
  qualify and are absent, a one-part dependency is in, and
  `chunk-generation-pipeline` is not) and fix the membership to the rule.
- **Part IV's three orders**: `SUMMARY.md`, `world/README.md` and
  `lectures.md` disagree on where *environment attributes and timelines* sits
  — the only part where they do. Rule which order is the book's and make the
  three agree (session D applies it if it is the sidebar that moves).
- **The two circular cuts** (III ↔ IV, V ↔ X): re-judged with the pages in
  front of you; `check_deps.py` stays green.
- The **lecture map's blurbs** (A2); the **glossary**: whether it does
  disambiguation at all (*Occlusion*, four meanings, no owner) and whether an
  entry may point at two owners (six do); the **class index** labelling every
  landing page *README* (a `verify_names.py --index` change: label by part).
- The published gate sentence: `introduction.md`'s *Verified means tested*
  paragraph now lists the link check (done by the planning session); confirm
  it reads right.

### A6. What session A does not do

It does not read a part (that is B–N), it does not rewrite a system page, and
it makes no ruling a part session could make better with the pages open.

---

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
| **A** | the standard | — | 24 (frame + Reference) | — | Part 3 above, whole |
| **B** | I · Anatomy, II · Foundations | 2 + 7 | 3 + 4 | 0 + 173 | The owners of four through-lines live here (A3). `anatomy` ↔ `reference/threads` (6.07): the page keeps the four threads, the table is Reference's. **Feature flags and `FeatureFlagSet`** (§7): backticked on twelve pages, explained on none — a section on `identifiers-and-registries` (it gates registry contents) or `resource-system`; `world/flag` is in Part II's packages now. Part II's coverage is 173 classes / 12.9k lines: read the sub-package table (`util` is the toolbox every part uses; `core/component` and `server/packs` are the part's own). `identifiers-and-registries` ↔ `tags` (12.45) and ↔ `data-driven-types` (7.07). `text-components` ↔ `chat-and-signing` twins at 270/235. The *not X but Y* and the second person are pass 8's and 6's; leave them. |
| **C** | III · The server | 5 | 6 | 25 | **`how-a-server-dies`' two subjects** (the three endings; the durability page inside it): section or page, decided. `how-a-server-dies` ↔ `starting-a-server` (11.43) and ↔ `server-tick` (6.03). **The three homeless items** from `players-and-sessions`: the `ServerPlayerGameMode` paragraph (→ `player-anatomy`, session H receives it), the view-distance packets (→ `what-the-client-is-told`, session I), `PlayerDataStorage`'s rescue (→ `level-data-and-rules`, session D). `server-tick`'s packet-drain paragraph: point forward to the event-loop section instead of explaining in place. The event-loop machinery (`BlockableEventLoop`, `TickTask`, `managedBlock`) — four parts cite it; confirm `server-tick` owns it and the others cite. **The abstract `Level`** (§7): decide with session D whether it is a section of `server-level-tick`, of `chunk-anatomy`, or a Reference page; the glossary asserts it with nowhere to send the reader. Coverage: `ServerBossEvent` is Part XIII's (session M); `DemoMode`, `ChunkResult`, `ServerEntityGetter` are this part's to place or decline. |
| **D** | IV · The world | 10 | 14 | 27 | **Part IV's three orders**, applied as session A ruled. **`chunk-storage`'s proposed hand-off** of the null-parse branch and `ChunkMap.handleChunkLoadFailure` to `chunk-generation-pipeline`: do it or drop it. The five within-part pairs (`chunk-generation-pipeline` ↔ `tickets-and-loading` 8.30, `chunk-anatomy` ↔ `chunk-generation-pipeline` 7.40, `chunk-anatomy` ↔ `lighting` 6.85) and the three with Part III (`server-level-tick` ↔ `scheduled-ticks` 8.67, ↔ `tickets-and-loading` 6.53, `how-a-server-dies` ↔ `chunk-storage` 6.35): the tick page defines the three ranges by the circular cut and cites the rest. `points-of-interest`'s missing sentence on `PoiManager.isVillageCenter` reading through the non-loading `SectionStorage.get` — a fact, so decompile open. `WorldBorder` (573 lines) is named only on `level-data-and-rules` and `server-level-tick`: a home, or a declared Reference-only. `level-data-and-rules` (this part's Reference page): `DirectoryLock`, `LevelVersion`, `LevelSummary`'s states, the four `LevelResource` paths, the per-player files, `MinecraftServer.saveAllChunks`, and the seven table rows with no prose (pass-4 session O's list). Receives `PlayerDataStorage`'s rescue from C. The landing page's *four side-systems* against five pages off the conveyor. |
| **E** | V · Blocks | 7 | 9 | 343 | **The two update channels**: owned once by `blocks-and-states`; check the six linking pages have not started re-explaining it (the duplication that produced three pass-2 errors). **`signal-and-dust`'s two subjects** (the lever; the second evaluator) and the staircase's *why* said twice on it. **`block-entities` as the part's odd page**: the landing page's fourth clause, or the cleaner reading (a hub, two click lectures, a redstone trio, one page about state that outgrew a block state). `diodes-and-observers` ↔ `scheduled-ticks` (10.00; the repeater's booking near-verbatim at 119/263). `block-entities` ↔ `chunk-anatomy` (6.10): the ticker wrappers move here. Coverage 343 classes / 36k lines: the sub-package table — sixty block entities under one pattern page (a `gen_reference.py` view of block entities and their tickers is the cheap answer), and the large single-mechanism classes (`SculkSpreader`, `RailState`, `MultifaceSpreader`, `BlockPattern`, `BaseFireBlock`) named or declined in a sentence each. The block-event users (§7) stay a paragraph on `pistons-and-block-events`. `block-update-flags` is this part's Reference page. |
| **F** | VI · Entities | 9 | 7 | 417 | **`EntityType.create`'s gates** on `entity-anatomy` and `entity-lifecycle` (8.12): one owner, one link. `ai-goals-and-brains` ↔ `points-of-interest` (10.95): the bed claim from both ends — Part IV owns the index, this part the behaviour. `entity-lifecycle` ↔ `server-level-tick` (9.23), `entity-anatomy` ↔ `synched-entity-data` (9.32), `authority` ↔ `movement-and-collision` (6.70), `damage-and-death` ↔ `non-living-damage` (11.62; the Reference page wants its `hurtClient` column and its `Entity.isPickable` sentence — pass-4 session O's list). **Part VI ← `chunk-anatomy`**: `entity-lifecycle` spends the chunk model throughout and links it nowhere. Homeless material (§7 and the pass-3 cuts): the fall-attribution threshold (death-message machinery — a `CombatTracker` sentence or a Reference row), the position-and-teleport family on neither `entity-anatomy` nor `authority`, `damage-and-death`'s cut *Interfaces* (`DamageTypes`, `DamageTypeTags` — a Reference view), the fortress spawn list and `Structure.spawnOverrides` and the `EntitySpawnReason` constants (§7's three `gen_reference.py` views — session N builds the views, this session says what each page cites). Coverage 417 classes: mobs are a family; the sub-packages (`ai/behavior`, `boss`, `raid`, `schedule`, `variant`) are the mechanisms to name or decline. |
| **G** | VII · Items and inventories | 8 | 4 | 240 | **`data-components` ↔ `items-and-stacks`** (17.00, the top pair in the book): the prototype and the patch — Part II owns what a component *is*, this part what a stack *holds*; decide the line and cut to it. `data-driven-types` ↔ `loot-tables` (11.08) and ↔ `contexts-and-predicates` (9.15): the pattern page owns the pattern, these own the instances. `contexts-and-predicates` ↔ `loot-tables` (8.00), `containers-and-menus` ↔ `recipes` (6.12). **The predicate shape library** (§7: `MinMaxBounds`, `CollectionPredicate`, `EntitySubPredicate`, `DataComponentMatchers`) — a table on `advancements` today; owner here or a Reference page, decided with session M. The `Item.getUseDuration` roster (§7, lost prose): a sentence or a Reference row. `Registries.LOOT_TABLE` named once. The three enchanting facts moved from `data-components` in pass 3: confirm they landed on `enchantments`. The `Item.Properties` weapon helpers view (§7, session N builds). `enchantment-hooks` and `loot-context-params` are this part's Reference pages. |
| **H** | VIII · The player | 7 | 6 | 6 | Receives the `ServerPlayerGameMode` paragraph from C (`block-breaking` ↔ `player-anatomy` 6.42 is the same seam). `using-an-item` ↔ `hunger-and-experience` (8.48): the meal from both ends. `input-to-movement` ↔ `the-two-phase-tick` twins at 28/119 (the fall-damage gate) and `input-to-movement` ↔ `input-and-keybinds` (7.73, resolved by J). `the-spear` ↔ `the-sword-swing` (7.40) is a deliberate sequel: check the second cites the first. `status-effects`' `LivingEntity.effectsDirty` with no reader named, `MobEffectCategory` in *Where to look* unexplained — coverage findings. `the-spear`'s component table: complete, or the heading says which subset. |
| **I** | IX · Networking | 5 | 5 | 120 | **The shape sentence** (*one wire and three passengers* against *protocol phases is the wire*), and the landing figure's arrows 3 and 4 that assert a dependency neither page uses. `codecs-nbt-json` ↔ `packets-and-stream-codecs` (11.57): where the NBT bridge lives. `protocol-phases` ↔ `players-and-sessions` (10.27): the configuration tasks and the join. `what-the-client-is-told` ↔ `tickets-and-loading` (9.48) and ↔ `synched-entity-data` (6.97): the send gates against their owners. The three within-part pairs (9.17, 6.87, 6.85): the lecture map already calls the first two one lecture in two halves. Receives the view-distance packets from C. `reference/threads`' never-hop population framed as a class rather than a runtime object. `packets` (generated) is this part's Reference page. |
| **J** | X · The client | 12 | 5 | 346 | **Part X ← `anatomy/anatomy`** (`the-client-loop`'s hook contrasts the two loops and links nowhere) and **← `entities/authority`** (`the-client-level` opens on *not an authority either*). **The GUI stack watched in a different order from the one it runs in** — a move, decided. **`the-gui-render-tree`'s title** — a rename, decided (the redirect is cheap). `input-and-keybinds` ↔ `input-to-movement` (7.73). `hud` ↔ `hud-elements` twins at 58/69; `hud-elements`' missing `SpectatorGui.extractAction` row and `Gui.overlay`/`Gui.screen`. `prediction-and-acks` owns the ledger through-line; the two click lectures cite it — check the citation form. Coverage 346 classes / 33k lines: `client/gui/screens` is a family; `client/gui/components`, `client/sounds`, `client/resources` have mechanisms to name or decline. |
| **K** | XI · Rendering | 11 | 7 | 743 | **`entity-rendering` against `reference/submit-phases`** (twins at 241/31; the catalogue wants `SubmitNodeStorage`, `TranslucentSubmit` and `RenderType.canConsolidateConsecutiveGeometry` named): whether the lecture wants more of the catalogue or the catalogue less preamble. `post-processing`'s *what a player sees* column: keep with a caption saying it is a reading, or cut. `the-window`'s *rest of the package* list omits seven of twenty-six classes (coverage); its seventh callback's section order is pass 6's. `lightmap-fog-and-sky` ↔ `environment-attributes-and-timelines` (8.27). `blaze3d` ↔ `naming-drift` (6.95). Homeless pass-3 cuts: `RenderSystem.outputColorTextureOverride` / `outputDepthTextureOverride` (the only mention of where the world can be redirected), the two `endFrame` ring buffers, the second `MaterialBaker` behind the block-atlas rule `models-and-atlases` still states. `block-entity-rendering`'s nineteen unmentioned in-scope classes, five worth a sentence each. Coverage 743 classes / 43k lines: renderers and models are families; `blaze3d`'s two backends and `client/renderer/*` sub-packages are the mechanisms. |
| **L** | XII · World generation | 10 | 6 | 189 | **The lattice fact three times** across `terrain` and `density-functions`: one owner, two links. **`terrain`'s title** — a rename, decided. **Part XII ← `identifiers-and-registries` and `codecs-nbt-json`**, the two cross-links still open. `density-functions` ↔ `density-function-nodes` (11.92; twins at 225/122 on the noise bounds): the catalogue's preamble against the lecture. **`JigsawStructure`'s three unnamed fields** (§7: the expansion hack, dimension padding, liquid settings) — a section on `jigsaw-and-templates`. `features-and-placement`'s *tree of features* section with an unrelated sixth member. `blending`'s dashed annotation node saying what the prose says thirty lines below: pass 7 redraws, this pass decides which of the two owns the fact. `Structure.spawnOverrides` (§7; session N's view). |
| **M** | XIII · Commands and data packs | 9 | 14 | 193 | **`ContinuationTask.schedule`** on `the-execution-engine` and `functions-and-macros`: the engine owns the arithmetic, the functions page cites. **The command-tree packet** on `permissions` and `brigadier-and-commands`: shape versus gating, read together once. The permission union paragraph on both `permissions` and `functions-and-macros`: the fact belongs on `permissions`. **`GameProfileArgument` and `ScoreHolderArgument`** (§7): a section on `entity-selectors`. **The boss bar** (§7): a section on `scoreboard-and-data` (`ServerBossEvent`, `CustomBossEvents`, `BossEvent` — 400 lines, no owner). The predicate catalogue and shape library (§7, with G). *Commands that are algorithms* (§7): a Reference page, not a lecture — write it or carry it with the reason. `advancements`' lost reload-listener sentence (when the layout runs) and `brigadier-and-commands`' `CommandSource` row — coverage, decompile open. The landing page's size sentence is the charter's example: it becomes the include. |
| **N** | Reference, maps, the frame's Reference-facing pages | 21 + 5 | 24 (with A) | — | The cross-cutting Reference pages: `threads`, `math-and-primitives`, `naming-drift`, `glossary` (owner links after every part has settled; the two-owner entries as A ruled; *Blending data* → `BlendingData`), `lanes` (pruning is pass 7's), the class index labelled by part. **The three `gen_reference.py` views §7 names** (`EntitySpawnReason` with what each gates; the `Item.Properties` weapon helpers; `Structure.spawnOverrides`), plus whichever the part sessions asked for (block entities and tickers, `DamageTypes`). `reference/README.md`'s hand-written *parts* column: generate it from the landing pages' *Reference this part uses* sections (a `check_deps.py` or `gen_reference.py` change) or re-derive it by hand once. The maps: `packages.md`'s part table is generated now; `hierarchy.md`'s two-sentence section grows a figure or folds. |
| **O** | the close | — | — | — | The frame and the summarisers against the finished parts (the introduction's part list, `lectures.md` re-derived from the landing pages, the glossary's owner links, the dependency figure); every move's redirect tested by `check_links.py`; `check_deps.py` green; [pass9.md](pass9.md)'s entries checked for shape; the pass's own strikes audited (a strike is a claim); the verdict on whether the pass was productive; pass 6's charter detail written, with the queue's `lecture` kind counted afresh. |

**What no session does**: reshape a page's skeleton or vary a device (6);
redraw a figure for legibility (7); hunt a tic or settle a count's wording
(8); change a fact without the decompile open (the standing rule); move a
page after this pass (the last-moves rule).
