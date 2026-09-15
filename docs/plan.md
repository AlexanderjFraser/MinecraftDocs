# The plan — the passes

*Rewritten 2026-09-02 at the start of pass 3, 2026-09-03 at its close,
2026-09-05 at pass 4's close and again that evening by the planning session
that set the ten-pass plan, 2026-09-07 by the planning session between passes 5
and 6, and 2026-09-14 by the planning session between passes 6 and 7. This is
the document every session reads first and ticks last. Each finished pass is
archived whole in its own file — [pass1.md](pass1.md), [pass2.md](pass2.md),
[pass3.md](pass3.md), [pass4.md](pass4.md), and for passes 5 and 6 the brief's
Part 5: [pass5-brief.md](pass5-brief.md) and [pass6-brief.md](pass6-brief.md),
each holding that pass's charter, its session paragraphs and its log beside the
brief, the runbook, session A's rulings and the schedule. The queues:
[pass5.md](pass5.md), opened as the polish queue and now the queue passes 5–8
draw on, each entry taken by the pass its kind belongs to; [pass9.md](pass9.md),
where every pass-5-to-8 session lists the claims it introduced;
[pass3.md](pass3.md) §7, the coverage queue.*

## Where we are

**Passes 1 to 6 are done.** Every page was drafted from the decompile (1),
fact-checked twice with every page found wrong at least once each time (2 and
4), restructured into a book of thirteen parts and eight page shapes (3), read
*across* rather than down — one home per mechanism, the seams, the
through-lines, the thirteen landing pages as arguments (5) — and then read
*down*, one page at a time, as one lecture's notes (6). Pass 5's record is
[pass5-brief.md](pass5-brief.md) and pass 6's is
[pass6-brief.md](pass6-brief.md), each with its charter, its schedule and its
session paragraphs.

**Pass 6 closed on 2026-09-14 after fourteen sessions, A to N**, the owner
calling the pass finished. The devices it was chartered against came down as
measured: the *Questions players ask* closer from 69 of 102 pages to **46**, in
**one** spelling from five, every one of them the last content section; the
literal `## The trace…` heading from 20 to **none**; the 1.21 blockquote from 39
to 43 and from 23 at the foot to **43 of 43**. But the count is not what the
pass was worth. **Around two hundred facts were corrected**, almost all of them
found by readers who had nothing but the page, on a corpus fact-checked
adversarially twice — and the class is one no fact-check looks for: **a sentence
that disagrees with the text beside it.** A lead-in promising four things over
six paragraphs; *nine zones* over sixteen names; *half of them … the other half*
over a table that splits thirteen and ten; four numbers in a record that holds
three. Session I named it, session J widened it from lead-ins to any sentence,
and session N found twenty-one of them in eighteen pages of the frame and the
shelf, where a catalogue's prose has little to say but how many rows there are.
The second finding is A2's: **an answer another page cites is load-bearing**,
and the closers that failed hardest were the ones holding the payoff of their
own page's opening — four pages in Part XII, three in Part XIII.

**Session O, the close, did not run**, and its jobs went three ways. Two were
done by this planning session: **pass 7's charter detail**, which is below and
in [pass7-brief.md](pass7-brief.md), and **the device re-count** against the
brief's Part 4 table, the numbers above. One is pass 7's session O, which reads
the thirteen landing pages' figures as a set and can read the pages with them:
**the thirteen landing pages as one set**, where pass 5 found thirteen of its
last twenty corrections and where five arguments still end on a list of symptoms
([pass5.md](pass5.md):69, :102). The rest — the strike audit, the shape of
[pass9.md](pass9.md)'s entries — is pass 9's own first step, which reads that
file before anything else. Two questions session N left for O are open and are
written into the queue: whether `TEMPLATE.md` should give the two tier front
doors a stated role, and whether *about a hundred lines* still means what it
meant for a landing page.

**Pass 7 — the figures — is running.** It was planned on 2026-09-14 by the
planning session on Fable, which built the four tools the pass needs and wrote
[pass7-brief.md](pass7-brief.md): Part 1 the viewer's brief, Part 2 the runbook,
Part 3 the standard, Part 4 the schedule with **the status column the owner
reads**. **Session A ran on 2026-09-15**: it ruled on the sixteen
recommendations and added two, rewrote Part 3 as the record and `TEMPLATE.md`'s
*Figures* and *Lanes* to it, **adopted the figure theme** — which alone took the
figures showing type under 9px from 89 to 10, and the 88 sequence diagrams to
none, without changing a page — and rewrote the exemplar
`entities/entity-lifecycle`, whose spawn cascade turned out to be wrong about
fourteen of its edges. **Session B ran the same day** over Parts I and II: two
figures split at the mechanism's own joint, the book's first two class diagrams,
nine corrections, and both parts left with no type under 11px anywhere, no
Mojang name broken on screen and no unresolved name in the gate.
**Session C ran the same day** over Part III: ten figures became twelve, the
tallest figure in the book fell 6,010px to 2,311px when its gate clauses moved
into a table beside it, and the part's real fault turned out to be **twelve
messages labelled with the caller's method and drawn arriving at the callee**,
one on every page, every one a gate failure — the shape the remaining part
sessions should look for first. **Session D ran the same day** over Part IV, the
largest part by figures: twenty-four became twenty-seven, four of them splits at
a mechanism's own joint, and the part's fault was Part III's again — fourteen of
its nineteen gate failures were the caller's method on the callee's arrow, which
makes it four parts of four. Its own finding is about the standard rather than
the pages: **a caption that closes its italics mid-way stops matching
`custom.css`'s selector and silently loses its styling and its number**, and
thirteen were live, three of them already shipped in Part III. All fixed, the
rule in `TEMPLATE.md`, and `check_mermaid.js` gates it now — a standard whose
only enforcement is the stylesheet is a standard nothing checks.
**Session E ran the same day** over Part V: ten figures became thirteen, three
pages split at a joint the prose already names, the book's fourth class diagram,
and all thirteen of its gate failures were the caller's-method-on-the-callee
device — five parts of five. Its own finding is a collision between two rulings:
**seven lanes is about 1,650px, which is 10.6px of type at the column**, so F7's
*at most seven* and F1's *nothing under eleven pixels* cannot both hold, and no
amount of label-shortening moves it — only a lane fewer or a split does.
Sessions F to N take the remaining parts in sidebar order; O closes. The charter is below. The latest release
is still 26.2 (26.3 at pre-release 2 of 2026-09-04, checked against the version
manifest on 2026-09-07), so no version pass is due before pass 7.

## The passes

| pass | what | lens | status |
|---|---|---|---|
| **1 — rough draft** | every page drafted from the decompile, names verified | — | done — [pass1.md](pass1.md) |
| **2 — completeness and accuracy** | every claim adversarially fact-checked; gaps filled; pages split and added freely | the adversary with the source | done, 2026-09-01 — [pass2.md](pass2.md) |
| **3 — restructuring** | the site became a book: each part the shape of its system, each page one of eight shapes; the frame, the maps and the Reference tier redone; the lecture order drafted | the shape | done, 2026-09-03 — [pass3.md](pass3.md) |
| **4 — the second fact-check** | pass 2's protocol over everything pass 3 rewrote; the claims pass 3 introduced checked first | the adversary again | done, 2026-09-05 — [pass4.md](pass4.md) |
| **5 — the book** | across pages: one home per idea, the seams, the through-lines, the landing pages as the part's argument, the coverage question once per part, the last moves | the book as one thing | done, 2026-09-07 — record [pass5-brief.md](pass5-brief.md); queue [pass5.md](pass5.md) |
| **6 — the lecture** | one page at a time: the devices that became slots, the twin skeletons, section order, the cuts, the landing pages' seventh section; a page that reads as one lecture's notes | the reader with only the page | done, 2026-09-14, sessions A–N — record [pass6-brief.md](pass6-brief.md); the close's remaining job carried to pass 7's session O |
| **7 — the figures** | every figure as rendered, beside its section: is it true, is it needed, does it show the thing, can it be read; the gate over names inside mermaid blocks | the picture | **current** — planned 2026-09-14; charter below; brief, runbook, the standard for session A and the schedule with each session's status [pass7-brief.md](pass7-brief.md); queue [pass5.md](pass5.md), kind `figure` |
| **8 — the voice** | one voice and one vocabulary: the exemplar, the tics, the terminology sweep, the ambiguous counts, the wording debt | the sentence | after 7 |
| **9 — the third fact-check** | pass 4's protocol plus what pass 4 learned; the claims passes 5–8 introduced first; every fix checked as a claim | the adversary, once more | after 8 — queue [pass9.md](pass9.md) |
| **10 — the last polish** | pass 9's debt, the frame against the finished book, links, the last cuts, the release | the reader, once more | after 9; then the site is finished |

Beside the passes, unnumbered: **the version pass**, chartered below and
run once between passes on each release; and **the owner's read**, which
runs whenever the owner likes and whose questions the current pass answers.

The rules stand for every pass: names never code · how the system works,
not how the code reads · newest version only (26.2) · trace-driven · claims
come from the decompile, never from model memory of 1.21 · the five gates —
`python tools/verify_names.py`, `node tools/check_mermaid.js`,
`python tools/check_lanes.py --strict`, `python tools/check_deps.py`,
`python tools/check_links.py` — clean before every commit that touches a
page, and `tools/deploy.sh` refuses to publish on any failure. A sixth,
`python tools/check_figure_names.py`, runs report-only from pass 7's planning
session and becomes a gate at that pass's close, when the 119 names it finds
have been corrected or ruled. Reasoning over sensing over measuring: no count
in a queue is a target, and the owner judges what lands.

## Why this order

- **Structure before words.** Pass 3 rewrote the prose of nearly every page
  to change its shape, and pass 4 then found 836 errors, most of them in
  sentences the restructuring had written. Polish done before a restructure
  is paid for twice: its sentences are rewritten, and the errors of the
  rewrite have to be found anyway. So the two structural passes (5, 6) come
  first, the wording pass (8) after them, and the fact-check (9) after the
  wording pass, because every pass that touches a sentence puts errors in —
  pass 4's finding, fifteen times over — and the last polish (10) is then
  light enough to put in few.
- **Across before within.** Pass 5 decides what each page owns, what moves
  and what is said once, so that pass 6's work on a page is not undone by a
  move. The summarisers — the thirteen landing pages, `lectures.md`, the
  glossary — are the exception that proves it: they drift every time their
  pages change (session O found five glossary entries written from
  sentences pass 4 had since corrected), so pass 5 gives them their role and
  each later pass re-syncs them at the end of its part session.
- **The figures get a pass of their own** because the diagram is the
  lecture's artefact (rule 4) and nobody has yet looked at one *rendered*:
  every check so far was parse and arrow-by-arrow truth, not shape or
  legibility. That pass also builds the gate over names inside mermaid
  blocks — 453 tokens no gate has ever seen — so that pass 9 checks figures
  under a gate.
- **Two polishes mirror two fact-checks**: the heavy one before the check,
  the light one after; the heavy one (8) is where the tics and the
  terminology are hunted corpus-wide, and the light one (10) is what the
  fact-check leaves.
- **One lens per pass.** A session briefed to fix everything fixes what it
  expects to find. Pass 3's sessions were told to reshape and did; the
  errors went into what they were not told to look at. A pass with one
  question finds what the previous pass could not see.

## The rhythm of a pass

Every pass runs the same way, because it has worked twice:

1. **A planning session** (Fable, between passes): reads the queue, builds
   the pass's tools and writes its brief and runbook — one prompt file per
   page or figure, so the sessions do no planning of their own — and
   measures what the queue actually contains before the first session
   spends anything on it.
2. **Session A — the standard**: the frame, the exemplar, the rulings the
   part sessions will apply (pass 3's session A wrote `TEMPLATE.md` from two
   pilots; pass 4's did the frame and made `check_deps.py` a gate).
3. **Sessions B–N — the parts**, in sidebar order, one part per session on
   Opus: read the charter, this pass's rulings and every queue entry that
   names the part; read the part end to end in watching order before
   changing anything; one background agent per page (never per part — a
   part-wide brief hit the spend limit in pass 3); the session does its own
   work while they run, then re-derives every finding it acts on; the four
   gates; commit `pass N, session X — Part M: <summary>`; deploy; log.
4. **Session O — the close**: the frame against the finished parts, the
   pass's own work audited (a strike is a claim), the pass archived whole
   into its file, the next pass's charter detail written, and a verdict on
   whether the pass was productive — the owner's test for spending more.

Standing rules for passes 5 to 8, the restructuring and refining passes:

- **A fact is not changed without the decompile open.** Agents in passes 5,
  6 and 8 have no source in their briefs — an agent given the source
  re-litigates instead of reading; pass 7's have the figure and its section.
  A session that finds a real error stops, re-derives it against the
  decompile itself, fixes it, and logs the correction in
  [pass9.md](pass9.md) the way a pass-4 session logged one: what the page
  said, what the decompile says, file and line.
- **Every claim a session introduces goes to [pass9.md](pass9.md)** — a
  hook, a moved paragraph, a redrawn arrow, a re-scoped count, a landing
  page's new argument. This is the rule pass 3 kept for pass 4, and it is
  what made pass 4 checkable. A session that cannot say what it changed on
  purpose has not finished.
- **Nothing is dropped except by moving it or logging the cut** with the
  reason (the budget rule in `TEMPLATE.md`); a moved page keeps its URL
  through `book.toml`'s redirects; after pass 5 no page moves again.
- **Every queue entry is checked against the page before it is acted on**:
  passes 5 to 7 rewrite what [pass5.md](pass5.md) describes, and an entry
  that is already overtaken is struck with a word saying so (pass 4's rule —
  an item handed forward is checked, not applied).
- **The gates stand and grow only by truth**: the link checker joined them
  in pass 5's planning session because it was clean on its first run and a
  link resolving is a fact; pass 7 adds names inside mermaid blocks; nothing
  that measures prose is a gate.
- **Commit your own files by name; never `add -A`** while another session
  may be open (session I of pass 3 swept another session's half-written
  change into an unrelated commit).
- **The version pass interrupts nothing**: a release that lands mid-pass
  waits for the pass to close.

---
## Pass 7 — the figures (current)

**Goal:** every figure is the true picture of its system, is needed, shows the
thing its section needs shown, and is legible at the column width without the
zoom — and every name in it is under a gate.

**Why it has a pass of its own.** The diagram is the lecture's artefact (rule 4)
and **nobody has ever looked at one rendered**: every check so far was parse
(`check_mermaid.js`) and arrow-by-arrow truth (pass 4), neither of which sees
shape, size or legibility. Three pass-6 sessions found the same part-wide
pattern independently — *the lead figure the page cannot yet be read against* —
and sent it whole rather than patching. The owner's brief adds the reader's
half: a reader who skims uses the figure as the check on the section, so a
figure that is wrong, unreadable or about something else costs the section, and
the figures are where machine-made work shows first.

**The jobs**, each with the number the planning session measured
(`tools/render_figures.js` in Chrome at the 1,092px reading column,
`tools/pass7_figures.py`, `tools/check_figure_names.py`; the per-part table is
in the brief's Part 4):

1. **Legibility.** 134 of the 194 mermaid figures are shown below their natural
   size, 76 below half, and **89 show type under 9px**; the widest is 5,415px.
   The cause is one thing, not a hundred: a sequence diagram is as wide as its
   longest message and the site's mermaid init does not wrap. A candidate init
   (`tools/pass7/`) takes the sequence diagrams from 70 below half to none and
   from 76 under 9px to none without touching a page; what is still shrunk after
   it is fixed per figure — fewer lanes, shorter labels, a split at the
   mechanism's own joint.
2. **The theme and the visual grammar.** No page carries colour today and none
   should: five semantic classes (`server`, `client`, `netty`, `worker`, `disk`)
   in one stylesheet, one meaning per mark corpus-wide, `TD` and `LR` only
   (the corpus spells the same direction `TD` 51 times and `TB` 27).
3. **What a figure is for.** 115 figures open their section with nothing above
   them, **none has a caption**, and 51 are pointed at by no sentence at all.
   The caption is the italic paragraph after the figure — markdown, so the name
   gate reads it and `llms-full.txt` carries it.
4. **The figure the page cannot be read against.** 139 figures introduce at
   least half their names before the prose does; **151 carry a name the prose
   never says**, 614 tokens in all. A lead figure is drawn in the words of its
   cast; a name the prose never says gets a sentence or leaves the figure.
5. **Density and kind.** Nine flowcharts over fifteen nodes, 42 figures over
   1,200px tall, one 3,766px; 121 figures carry labels that are sentences (312
   of them). The site's mermaid draws twenty-one kinds and the corpus uses
   three: a class diagram for what an object holds, a block or packet diagram
   for a layout, a chart for a quantity are available and unused
   (`render/gallery/` has one of each).
6. **The gate over figures**: 2,619 names inside mermaid blocks, **119
   unresolved**, plus 362 notes whose convention session A sets. Report-only
   through the pass, `--strict` at its close. The same parser gave the class
   index the 139 page pairs it could not see.
7. **Every figure-kind entry in [pass5.md](pass5.md)** — 150 of them, checked
   against the figure before it is acted on.

**The agent** is a viewer with the picture and the section and nothing else,
asked what the figure shows before it reads the section, what it could not read,
what the section needed a picture for, what is in the picture that is not needed
and what is needed that is missing, whether the kind is right, and which words
the figure spends before the page mints them; then the figure it would keep, the
one it would cut, the section that wanted a picture, and a sketch of the worst
one redrawn — with every arrow the sketch changes listed as a claim.

**The rhythm** is pass 6's, which worked twice: session A settles the
corpus-wide rulings, adopts the theme and rewrites one exemplar page
(`entities/entity-lifecycle`, whose three figures exercise nearly every ruling);
B–N take the parts in sidebar order and O closes, flipping the gate to
`--strict`, pruning the lane key, reading the thirteen landing figures as a set
and re-measuring the corpus against Part 4's table.

**An arrow is a claim.** A figure redrawn asserts an ordering; every arrow
added, removed, reversed or relabelled is re-derived against the decompile with
`diagram_arrows.py`'s numbered list in hand and logged in
[pass9.md](pass9.md) — which is why pass 9's standing item reads *the figure
against the section under it first*.

**Not:** facts (an arrow found wrong is re-derived and logged as a correction);
prose beyond a caption, a lead-in and the one sentence a name needs; a figure
added for variety.

## Pass 8 — the voice

**Goal:** one voice, one vocabulary, no tics, and every number says what it
counts.

**The jobs:** the exemplar page and the voice note, chosen in session A; the
tics — "not X but Y", the named-qualifier hedge, the dead-constant aside,
the em-dash chain, the correction written in the voice of a correction,
*record* against *extract*, the three words for an update channel's
direction; the terminology sweep with the glossary as the checklist, and the
glossary's own five headwords, *Occlusion*, and the six two-owner entries;
the fifty-odd counts whose population admits two readings — pick the
reading, say it, or drop the number; the two rules for the word *classes*;
how data keys are typeset; the wording debt logged per part in
[pass5.md](pass5.md), hooks first, wherever passes 5 to 7 have not already
rewritten it; the register of the 1.21 blockquote. Reader agents again, now
with the exemplar. Every changed sentence's claims to [pass9.md](pass9.md).
The planning session builds the tic finders and a terminology checker.

**Not:** structure (a structural finding is ruled out or goes to pass 10's
notes); facts.

## Pass 9 — the third fact-check

Pass 4's charter, protocol and brief (archived in [pass4.md](pass4.md) and
[pass4-brief.md](pass4-brief.md)) run again over the corpus passes 5 to 8
rewrote, with what pass 4 learned made into steps:

1. [pass9.md](pass9.md) first — the claims passes 5 to 8 introduced, and
   their corrections confirmed as fixes rather than re-litigated as
   originals.
2. The illustrations before the mechanisms: tables, one-line summaries, Q&A
   answers, asides, landing pages, the glossary — where pass 4 found the
   errors.
3. **A fix is a claim.** Every correction is re-derived by a second reading
   before it lands, and the close audits the pass's own strikes and
   corrections (session O's job, made a step).
4. The figure against the section under it before either against the
   source.
5. Populations, not rows, for every generated page; call sites, not lines,
   for every count; the population named for every absolute.
6. The names inside figures are under the gate by then; the 23 ambiguous
   simple names settled or the resolver taught which file a page means.
7. The summarisers re-read after their pages are fixed.
8. Pass 9 adds nothing; a gap goes to [pass3.md](pass3.md) §7 for the second
   edition.

Its planning session rewrites `pass4_prompts.py` to read pass9.md.

## Pass 10 — the last polish

Pass 9's wording debt; the frame — introduction, lecture map, the maps' and
Reference's front pages — against the finished book; every internal link
and anchor under the link checker as a gate; the last cuts; the owner's
remaining questions answered and the lecture order confirmed; the
introduction's *verified* paragraph made true of every gate; the release —
a git tag, the site verified against whatever version is current, the
second edition's seed written into §7 and *what this book skips*. Then
nothing more is done to the site except version passes and the corrections
readers file.

## The version pass — rule 3's re-read (chartered, runs on each release)

Rule 3 says newest version only, and every page carries `verified against
26.2` as a test rather than a claim. **As of 2026-09-07 the latest release
is still 26.2; 26.3 is at pre-release 2 (2026-09-04)** — checked against
Mojang's version manifest by the pass-6 planning session, not assumed. This
pass triggers on a release and runs once, in one session, between passes; a
release that lands mid-pass waits for the pass to close. It did not run
inside pass 5, because 26.3 had not shipped by the close; it will most likely
run between two of passes 6 to 8, and again if 26.4 lands before pass 10.

1. Fetch and decompile the release into `reference/<version>/` beside the
   old tree, with its `data/`, `assets/` and `server-classes.txt`, and
   re-run `tools/fetch_libs.sh` (26.3 snapshots already use authlib 10.0.77
   and Brigadier 1.3.11).
2. **`verify_names.py` against the new tree is the mechanical half**: every
   name that stops resolving is a rename or a removal, and the failures name
   the pages that need re-reading. That is the whole point of the gate.
3. Regenerate: `gen_reference.py all`, `map_source.py`, the two indexes.
   Diff every generated page against the old version's and read the diff — a
   population that changed is a page that changed.
4. `claims.py --all --counts` over the pages the first two steps touched: a
   count whose population moved is wrong now.
5. The header line on every page, `CLAUDE.md`, the introduction, `llms.txt`.

A re-read, rarely a rewrite. A system that changed shape rather than names
is a structural finding and goes to [pass5.md](pass5.md) or, after pass 5,
to §7.

## The owner's read

Unnumbered and parallel: the owner reads a part with the decompile open
whenever they like, and leaves questions **in the page** as `<!-- Q: … -->`
comments. The next session that touches the page — whatever pass it is in —
answers each question in the prose (if the owner had to ask, the page was
wrong or missing it) and removes the comment; every part session greps its
part for them at the start. The owner confirms or reorders `lectures.md`
before pass 9, so that pass 9 checks the confirmed order. Nothing is recorded
that the owner has not understood; recording is after pass 10.

## Risks

- **A restructuring pass puts errors back** — pass 3 did, by the hundred.
  [pass9.md](pass9.md) is the answer, and the rule that a session lists what
  it changed on purpose so that pass 9 can read the rest harder.
- **A pass that finds nothing.** A lens that returns clean is a lens too
  wide or an agent that liked the page. Brief per page, evidence for every
  finding, and the close says honestly whether the pass earned its cost.
- **The queue is stale by the time a pass reaches it.** Passes 5 to 7
  rewrite what [pass5.md](pass5.md) describes; every entry is checked
  against the page before it is acted on.
- **A release lands mid-pass.** Finish the pass; run the version pass
  between passes; the final site is verified against whatever is current
  at pass 10.
- **The tools.** Fifteen bugs in pass 4, six of them published; suspect the
  tool first, and every new tool ships with a probe that proves it fails on
  the construct it should.
- **Cost.** About fifteen sessions a pass, about eighty more in all. The
  owner accepts that while passes are productive, and a pass's close is
  where that is judged.
## Session log — pass 7 onward

*(newest last; pass 6's log and its fourteen session paragraphs are in
[pass6-brief.md](pass6-brief.md) Part 5, pass 5's in
[pass5-brief.md](pass5-brief.md) Part 5, and pass 4's at the end of
[pass4.md](pass4.md))*

- **2026-09-14, planning session (Fable, between passes 6 and 7).** No page's
  prose touched. **Pass 6 archived** whole into [pass6-brief.md](pass6-brief.md)
  Part 5 — its charter, its fourteen session paragraphs and its log, headings
  demoted — so this file is again the current charter and the passes to come;
  the close's one remaining job, the thirteen landing pages read as a set, was
  carried to pass 7's session O rather than left implicit. **Pass 7 planned**:
  [pass7-brief.md](pass7-brief.md) — Part 1 the viewer's brief (the picture and
  the section, seven questions per figure and four per page), Part 2 the
  runbook, Part 3 the standard as **sixteen recommendations with the numbers
  behind them** for session A to rule on, Part 4 the schedule with the status
  column. **Four tools, each with a `--probe`**: `render_figures.js` (the built
  site served locally and opened in the machine's own Chrome through
  playwright-core, every figure screenshotted at the reading column's width and
  measured — scale, smallest type, overlapping labels, labels over a shape,
  labels outside their box, edges through a node, crossings, clipping;
  `--init-js`/`--css` try a theme without touching the site, `--html` renders a
  gallery), `pass7_figures.py` (every figure against its page: its place, its
  source, which of its names the prose says before it, only after it or never,
  and the render; plus the sections over forty lines with no figure, and a
  ranking by trouble), `check_figure_names.py` (**the gate the charter asked
  for**: 2,619 names inside mermaid blocks checked against the decompile the way
  `verify_names.py` checks the prose, with inheritance and a message's head
  against the lane it is sent to) and `pass7_prompts.py`. `check_mermaid.js`
  gained a `structuredClone` polyfill and a quiet console, so `pie`,
  `packet-beta` and `radar-beta` parse under it as they do in the browser, and
  it now exports its fence-mapping helpers; `check_lanes.py` gained `--unused`
  (44 key rows of 342 that no page declares); `deploy.sh` runs the new gate
  report-only. **The corpus rendered twice** — as it ships and under a candidate
  theme — and the numbers are in the brief: 134 of 194 figures shrunk, 89 under
  9px, none captioned, 151 carrying a name the prose never says, 119 names
  failing the gate. **One finding of the tool's own**: `verify_names.py --index`
  now merges the figure parser's mentions, so the class index gained **139 page
  pairs** it had been blind to since pass 5 session A logged it — a class named
  only in a diagram had no index entry, because the index reads backticks and a
  mermaid label is not one. `CLAUDE.md`, `README.md`, the memory and this file
  brought current; one queue entry struck with the page open. All five gates
  green; nothing deployed, because no published page changed except the
  regenerated class index. **Rulings**: the pass's own tooling renders into
  `render/`, which is gitignored — a screenshot is a build artefact and the
  index it writes is regenerable, so neither is committed; and a candidate theme
  lives in `tools/pass7/` until session A adopts it, so that the evidence for a
  corpus-wide change is a diff of two renders rather than an argument.

- **2026-09-15, pass 7 session A (Opus) — the standard, the theme and the
  exemplar.** Ruled on the planning session's sixteen recommendations and added
  two the adoption forced: **F17**, a lane name too wide for its box carries its
  own `<br/>` at a CamelCase boundary, and **F18**, the 109 names the wrap still
  breaks in messages and notes, which are the part sessions' work under F4.
  [pass7-brief.md](pass7-brief.md) Part 3 rewritten as the record, and
  `TEMPLATE.md`'s *Figures* and *Lanes* rewritten to it — the marks table, the
  label budgets, the caption device, the tick band, the density rule, the menu
  of kinds and the seven-lane arithmetic. **The theme is adopted**:
  `mermaid-init.js` is committed (out of `.gitignore`, MPL header kept, with a
  warning not to re-run `mdbook-mermaid install` over it) and `custom.css`
  carries the five semantic classes in both palettes and the caption rule.
  Across the 196 mermaid figures, with no page's content changed: the median
  scale 0.61 → **0.82**, figures below half 76 → **6**, type under 9px 89 →
  **10** and under 11px 107 → **31**, the widest 5,415px → 3,859px — and of the
  88 sequence diagrams that were the whole problem, **none** is now below half
  or under 9px. The costs are named rather than left to be found: figures are
  taller (the median sequence diagram 401px → 940px) and mermaid hyphenates a
  word wider than the wrap, which broke 222 Mojang names on screen. The 112 that
  were lane names are fixed corpus-wide by a one-time sweep
  (`tools/pass7/break_lane_names.py`, which reads a render rather than counting
  characters); both gates learned to close the break up, with probes. A
  width-240 theme that would have avoided the break was rendered over the corpus
  and **rejected** — it leaves 71 of 88 sequence diagrams under 11px. The
  exemplar `entities/entity-lifecycle` was rewritten with a viewer's report in
  hand: the 21-node, 39-edge cascade shown at 0.28 with 4.6px type is two
  flowcharts at scale 1 and 16px, its twenty conditions moved into a fifteen-row
  table, and **it loops** — re-deriving it found that fourteen edges the old
  figure drew as dead ends are a `continue` to the next try, that three
  rejections were drawn at the wrong scope, and that two exits were missing
  entirely. The entry sequence gave the page's second half back to the state
  diagram that owns it and gained the callback hop it had been drawing as a call
  `ChunkMap` does not have; the state diagram's sentence labels became
  conditions. Four captions — the book's first. One finding the method threw up
  by itself: **mdBook's floating chapter chevrons have been painted on top of
  the prose at 1440px since pass 3 widened the column**, fixed in `custom.css`
  by moving mdBook's own breakpoint to where the column clears them. All six
  gates green (the figure-name gate still report-only, 113 unresolved of 2,588);
  [pass9.md](pass9.md) has the claims and the six corrections,
  [pass5.md](pass5.md) the six entries this left. Deployed.

- **2026-09-15, pass 7 session B (Opus) — Parts I and II: the figures.** Eleven
  pages, nineteen figures, one viewer agent per page with the picture and the
  section and nothing else. Fourteen figures redrawn, **two split at the
  mechanism's own joint**, one cut back, two given a kind the book had never
  used, and **all nineteen captioned**. The size numbers close: in both parts,
  **no figure shows type under 11px** (from nine shrunk and two under 9px after
  the theme), one is left below 0.75 — `data-driven-types`' trace at 0.73 and
  11.6px, where six lanes and not the labels set the width, and where cutting a
  lane would cost the pattern's own subject — the thirteen Mojang names still
  hyphen-broken on screen are **zero**, and the gate's fourteen unresolved names
  are **zero**.
  The two splits are the pass's method working: `identifiers-and-registries`'
  second figure was two scenarios that shared no lane sitting in one frame — a
  world-load task graph and a configuration handshake, 0.68 with eight names
  broken mid-word — and is now a flowchart and a four-lane sequence, both at
  scale 1; `anatomy`'s two-loops flowchart was 2,184px wide, shown at 0.28 with
  4.5px type, and is now two rings side by side at scale 1, each with an inner
  box for the call that contains the rest — which is also the fix for the queue
  entry that said it drew a nesting as a sequence. **The book's first two class
  diagrams** are here, on `text-components` and `data-components`, which is
  exactly F10's prediction: the vocabulary pages had been drawing conversations
  between objects that do not talk.

  **Nine corrections**, every one a figure disagreeing with the decompile or
  with the prose beside it, all re-derived with the source open and logged in
  [pass9.md](pass9.md). The sharpest is `identifiers-and-registries`' bootstrap
  ladder, where the figure had the ITEM loader triggering `Items` class init and
  `Bootstrap.bootStrap` had already done it two calls earlier, through
  `ComposterBlock.bootStrap`; the page's own prose said so and the figure said
  the other thing. Three more were a message head naming the *caller's* method
  rather than the target's, one was `LootItemFunctions.compose` drawn leaving
  the wrong object, one was `HashedStack` — a record — drawn sending a packet,
  and one was a `LoadingOverlay` arrow that merged a poll of the reload instance
  with a callback into `Minecraft`. **This is the class pass 6 named, found in
  pictures**: a figure that disagrees with the text beside it, on a corpus
  fact-checked twice and read down once.

  One tool change, and it is the session's transferable finding:
  **`check_figure_names.py` did not read a `<br/>` inside a message the way F17
  taught it to read one inside a lane**, so F18's instruction to part sessions —
  break a name too wide for its box at a CamelCase boundary — was unfollowable,
  and doing it made the gate fail the page. One rule (a break tight against the
  text is a name and closes up; a break with a space either side is a clause and
  becomes one) and three probe cases; corpus-wide unresolved names fell 119 →
  **100** with no page outside these two parts changed, so some of the 119 were
  never page errors. Also raised for session O: the renderer counts a `par`
  block's own headers as labels outside their container; `par` itself is a mark
  outside `TEMPLATE.md`'s table, spent once here and captioned, because the
  figure otherwise said the opposite of the paragraph's "Meanwhile"; the jar
  treemap cannot carry the reconciliation `what-this-book-skips` asks of it; and
  **five of the thirteen landing figures still spell a direction F3 rules out** —
  Part II's was one, and is now `TD`, numbered to the watch order and captioned.
  Eight queue entries struck with the page open, seven opened. All six gates
  green (the figure-name gate still report-only). Deployed.

- **2026-09-15, pass 7 session C (Opus) — Part III · The server: the figures.**
  Six pages, ten figures in and twelve out, one viewer agent per page with the
  picture and the section and nothing else. Every figure in the part is now
  **captioned**, pointed at by a sentence, and **legible at the reading column**:
  the two shown below 0.75 are none, the smallest type on screen went 11px →
  **12.4px**, the fifteen sentence labels are **zero**, and the figure-name
  gate's twelve unresolved names and thirteen notes are **zero of each** — the
  first part clean on the notes as well as the failures. Two figures split at
  the mechanism's own joint: `server-tick`'s event loop at
  `MinecraftServer.pollTaskInternal`, where an empty queue and a head that may
  not run turn out to be the same answer, and `starting-a-server`'s boot at the
  note bar it was already drawing.

  The tallest figure in the book fell **6,010px → 2,311px** and its type went
  from a label you read one box at a time to 16px throughout.
  `server-level-tick`'s twenty-two-step chain had a gate clause appended to
  every label — *— running*, *— no gate*, *— running, and not a debug world* —
  which is the half the section leans on and the half a reader cannot scan; the
  gates are a three-column table beside the figure now, one row per step, every
  cell re-derived from `ServerLevel.tick`. Losing the clauses made room for the
  containment the figure had been hiding: six of its boxes are the *insides* of
  `ServerChunkCache.tick`, drawn beside the steps around them as though they
  were siblings, which is why the prose's *five things in one call* and the
  figure's six boxes had been contradicting each other since pass 5. They are a
  box now, and the two counts agree.

  **The part's real fault was not the one the queue named.** Three pass-6
  sessions had sent *the lead figure the page cannot be read against* here as a
  part-wide pattern, and underneath it sat a sharper one: **twelve messages —
  one on every page of the part — labelled with the caller's method and drawn
  arriving at the callee.** `MinecraftServer.saveAllChunks` on an arrow into
  `ServerLevel`, which receives `ServerLevel.save`;
  `ServerLevel.sendBlockUpdated` into `ServerChunkCache`, which receives
  `blockChanged`; `ServerChunkCache.broadcastChangedChunks` into `ChunkHolder`,
  which receives `broadcastChanges`; and nine more. Every one was a gate failure
  and every one was a claim about who does what to whom, which is the thing a
  sequence diagram exists to say. The gate finds the shape mechanically, and
  most of the 88 unresolved names left in the corpus look like it — so this is
  the entry the remaining part sessions should read first.

  **Six corrections**, each re-derived with the source open and logged in
  [pass9.md](pass9.md). The sharpest is `how-a-server-dies`' watchdog figure,
  which had no `Disk` lane: beside figure 1's four writes it said *the watchdog
  writes nothing*, on a page whose own comparison table two screens above reads
  *is a crash report written: **yes***, and `ServerWatchdog.run` does write one,
  to stdout and to *crash-reports/*, before it calls `System.exit`. Next to it:
  `starting-a-server`'s boot had *the stages that must be single-threaded come
  back to main* on the worker's return arrow, which never touches `Main` — the
  arrow that does was labelled with a different call; and `how-a-server-dies`
  drew `saveDataTag` and `SavedDataStorage.saveAndJoin` as siblings of the flush
  save when all three are *inside* `MinecraftServer.saveAllChunks`, so the
  page's hook — *after `level.dat` and not before* — is a property of one call
  and not a claim about three. Drawn as a band, it is structural.

  The queue's one open question is answered: nothing holds a joining player's
  spawn chunks between the ticket being placed and `PrepareSpawnTask.Ready`,
  because nothing has to. `TicketType.PLAYER_SPAWN` carries
  `TicketType.FLAG_LOADING` and nothing else, so `canExpireIfUnloaded` is false
  and its twenty-tick timeout does not begin while the chunks it asked for are
  still on their way — which is exactly why
  `ServerChunkCache.addTicketAndLoadWithRadius` accepts the type at all, since
  it throws for any type that could expire before it loads.

  One tool change, and it is the same shape session B found: **the gate could
  not read the tick band F8 tells every part session to draw.** Part III drew
  the corpus's first four `rect` bands and `check_figure_names.py` read
  `rgba(0, 0, 0, 0.04)` as a call named `rgba` on every one. One rule — a
  `rect`'s remainder is a colour and never a label, a `box`'s leading colour is
  stripped before its label is checked — and two probe cases. Two sessions, two
  tool blindnesses, both found by being the first to use a device the standard
  had ruled: the gate is worth re-probing against each new device a part session
  spends. Twelve queue entries struck with the page open, five opened. All six
  gates green (the figure-name gate still report-only, 88 unresolved of 2,515
  corpus-wide). Deployed.

- **2026-09-15, pass 7 session D (Opus) — Part IV · The world: the figures.**
  Eleven pages, twenty-four figures in and **twenty-seven** out, one viewer agent
  per page with the picture and the section and nothing else. Four of the new ones
  are splits at a mechanism's own joint, and every joint was one the prose already
  named: `game-events-and-vibrations`' twenty-four-node cascade — the worst figure
  in the part at 0.54 and 8.6px, taller than five screens — became the dispatcher's
  walk and one listener's five refusals, both at scale 1; `fluids`' tick became
  *what state should be here* and *what is done about it*; `scheduled-ticks`'
  pipeline became booking and draining, which is that page's own bold claim about
  which of the two is server-thread only; and
  `chunk-generation-pipeline`'s twelve-status chain — a table wearing a flowchart,
  three facts in every node and twelve arrows saying only *next* — became a
  four-column table beside a new figure of four nested rings, which is what the word
  *pyramid* had been doing all along. `chunk-anatomy`'s lead figure is the book's
  third `classDiagram`: its heading promised four shapes, the paragraph under it
  stated a hierarchy, and the old figure drew neither. Across the part: **no type
  under 9px, no figure over fifteen nodes, no lane over seven**, the tallest figure
  4,978px → 2,077px, every figure captioned, every non-lead figure given a lead-in,
  and the figure gate's **nineteen unresolved names and sixty-three notes are none
  of either**.

  **The part's fault was Part III's fault again.** Fourteen of the nineteen gate
  failures were one device — a message labelled with the *caller's* own method and
  drawn arriving at the *callee* — which makes it four parts of four. It is worth
  saying why it keeps being caught: the gate checks a message's head against the
  lane it is sent to, so a caller's method is by construction not a member of that
  lane. What two fact-checks could not see, a mechanical rule sees every time.

  **The session's own finding is about the standard rather than the pages.** A
  caption is the italic paragraph after a figure, and `custom.css` matches it with
  `p:has(> em:only-child)`. An author who closes the italics to set a name and
  reopens them writes *two* `<em>` children, the selector stops matching, and the
  paragraph silently loses its styling and its figure number — in the built page
  alone. The markdown looks right, mermaid parses, `verify_names.py` passes.
  **Thirteen were live when this session looked, and three had already shipped in
  Part III**: the fault outlived the session that invented the caption and the two
  that wrote sixty of them. All thirteen fixed, the rule written into
  `TEMPLATE.md`, and `check_mermaid.js` now gates it with a six-case `--probe`. The
  lesson generalises past captions: **a standard whose only enforcement is the
  stylesheet is a standard nothing checks.**

  Two more render traps, both invisible in source. An explicit `<br/>` turns the
  theme's 180px wrap off for its *whole* label, so F18's instruction to break a long
  name inside a message makes the figure wider unless the name is the whole message
  — four such repairs took `lighting`'s trace from 0.69 to **0.55** and its type
  from 11.1px to 8.8px, and taking them out again put it back. And a subgraph title
  is clipped to one wrapped line, which ate the outer ring of the new pyramid until
  it was cut to twenty-three characters. Both are now in `TEMPLATE.md`, beside the
  `stateDiagram-v2` second-colon parse failure the same page found. One tool change,
  and it is the same shape as B's and C's: `check_figure_names.py` closed up a
  `<br/>` tight on both sides wherever it appeared, so a node label breaking its
  line after a comma welded two names into a third that is in no decompile — one
  rule, two probe cases, the third tool blindness a part session has found in three
  sessions.

  Nine corrections, all in [pass9.md](pass9.md). The sharpest is
  `environment-attributes-and-timelines`, whose stack figure drew the two
  lightning-flash layers as rungs *every* value falls through when `ClientLevel`
  bolts each to **one named attribute**, so they are absent from the other
  forty-six; beside it, the same page's client trace asserted that the whole stack
  re-resolves every frame when the probe resolves once a tick and every later frame
  in that tick only lerps. Also settled: the queue's long-open question about
  whether a secondary state diagram is a page's true picture, answered for both of
  its remaining pages — **yes** on `points-of-interest`, where a ticket's whole life
  is three states and the hook is which transitions are *missing* from them, and
  **no** on `tickets-and-loading`, where it is not the page's picture but is the
  owner of the four statuses, which is what stopped that page drawing one mechanism
  twice. Found and deliberately left: five of the part's figures are still below
  0.75, and every one is a seven-lane sequence diagram with no label over twelve
  words — precisely the arithmetic F7's amendment states. Folding a lane is worth
  about 0.10 and nothing else moves them. Eleven queue entries struck with the page
  open, seven opened. All six gates green (the figure-name gate still report-only,
  69 unresolved of 2,489 corpus-wide). Deployed.

- **2026-09-15, pass 7 session E (Opus) — Part V · Blocks: the figures.** Eight
  pages, ten figures in and **thirteen** out, one viewer agent per page with the
  picture and the section and nothing else. Three pages split one figure at a
  joint the prose already names: `blocks-and-states`' write — the part's
  most-linked figure, 21 nodes and 3,409px with a gate clause appended to ten of
  its labels — is now the chunk write and the tail either side of the re-read,
  with every clause in a thirteen-row *step · side · flags · also needs* table,
  which is session C's `server-level-tick` remedy applied a second time;
  `block-breaking`'s dig is split at the eighth tick, the two machines boxed and
  the loop's body in a `par` so the picture stops asserting an order between two
  clocks the section exists to call independent; and `block-interaction`'s click
  is split at the machine boundary, where `ServerPlayerGameMode` finally has the
  lane the cast always gave it, so the two sides read as the same three-step
  order — which is that section's claim and the thing the single figure had been
  contradicting. `blocks-and-states`' vocabulary figure is the book's **fourth
  `classDiagram`**: twelve nodes in which *extended by* and *builds* were drawn
  with the same arrow, now two inheritance hierarchies meeting in `BlockState`,
  and eleven classes rather than twelve, because the twelfth was a static field
  and the heading had been counting it. Across the part: **no type under 11.9px**
  (five figures were at 10.3–11.1px), nothing below 0.74, sentence labels 38 →
  **0**, bare-number gates 3 figures → **0**, every figure captioned, and the
  figure gate's **thirteen unresolved names and twenty-six notes are none of
  either**.

  **The part-wide fault was Parts III and IV's, a third and fourth time.** All
  thirteen gate failures were the same device — a message labelled with the
  caller's own method and drawn arriving at the callee — which makes it **five
  parts of five**. Five sessions have now found it, none of them looking for it,
  and all of them mechanically.

  **The session's own finding is about a collision between two rulings.** Four of
  Part V's five sequence diagrams had seven lanes, and seven lanes is about
  1,650px, which at the 1,092px column is scale 0.66 and 10.6px of type. So F7's
  *at most seven lanes* and F1's *no label under eleven pixels* are **not both
  satisfiable**: seven lanes is already one too many for the column. What does
  not help is shortening labels — every message already wraps at 180px, so eight
  shortenings moved the width by exactly zero. What helps is one lane fewer
  (`block-entities`' `ServerPlayer` carried one message and decided nothing;
  folding it bought 0.11) or a split (`block-interaction`'s client half is now at
  0.97). Every one of the four is now six lanes or two figures. F7's amendment
  says an *eighth* lane puts everything under eleven pixels; the measurement here
  says the seventh does, and session O should decide whether the key's number
  becomes six.

  Eleven corrections, all in [pass9.md](pass9.md). The sharpest is
  `block-breaking`, where the figure printed the server's progress at STOP as
  **1.07** while the prose two sections below says both sides *arrive at the same
  1.064* — the one number the page exists to say is shared, printed two ways
  inside one picture. Beside it: the tick-1 order in the same figure was
  inverted; `blocks-and-states`' flag lead-in promised **seven** bits and named
  **eight**; the landing page's lead-in said *each arrow* of eleven when it meant
  six; and `pistons-and-block-events`' last note put both sides on tick N+2 when
  the page's own prose gives the client five extra `deathTicks`. Also settled
  without new work: the flag-word question the queue left for this session had
  already been answered by F4, and applying the ruling is what turned the *seven*
  up. Ten queue entries struck with the page open, six opened (three of them for
  session O). All six gates green (the figure-name gate still report-only).
  Deployed.
- **2026-09-15, pass 7 session F (Opus) — Part VI · Entities: the figures.** Ten
  pages, 22 figures in and **26** out, one viewer agent per page with the
  picture and the section and nothing else. Three pages split one figure at a
  joint the prose already names — `synched-entity-data`'s shear at the tick,
  where splitting is what finally gave **the server's container and the
  client's a lane each**, which is the one thing that page exists to say there
  are two of; `entity-anatomy`'s summon at the same boundary, so the page's
  title happens twice, once per machine; and `authority`'s boat by machine,
  with a lane each for the two copies. `damage-and-death` traded its
  three-screen eight-step chain for a short chain carrying only the running
  number and a nine-row *step · owned by · what it does · leaves* table beside
  it — session C's `server-level-tick` remedy a third time — and gained a
  figure under *Death, or not* for the veto one other entity holds over this
  one's loot. `entity-anatomy`'s lead flowchart is the book's **fifth
  `classDiagram`**: eleven boxes to three, because *what an object holds* was
  never a flowchart. Across the part: **no type under 12.6px** (five figures
  were at 9–11px), nothing below 0.79, sentence labels 14 → **2**, every
  figure captioned, and the figure gate's **fourteen unresolved names → none**.

  **The part-wide fault was the same one, a sixth time.** Eleven of the
  fourteen gate failures were a message labelled with the caller's own method
  and drawn arriving at the callee — `tickNonPassenger` at a boat,
  `collideWithShapes` at `Shapes`, `checkFallDamage` at `Block`,
  `actuallyHurt` at `CombatTracker`, `getAttributeValue` at `AttributeMap`,
  `handleSetEntityData` at a container. **Six parts of six**, none of them
  looking for it, and the gate catches every one mechanically. What is new is
  what fixing it costs: on three pages the wrongly-addressed lane had nothing
  else to do, so the fix *removed lanes* — `movement-and-collision` went from
  seven to three — and the figure got legible as a side effect.

  **The session's own finding is a rendering fault two gates were blind to.**
  Mermaid runs a markdown tokenizer over flowchart and state-diagram labels
  and renders only a handful of token types; anything else is replaced, in the
  node, by the literal string *Unsupported markdown: list*. A label beginning
  `1. ` is a markdown list, so it is **erased**. Nine were live: four on
  `ai-goals-and-brains`' lead figure, and **five of the six nodes** on
  `rendering/visibility-and-the-frame-graph`'s, in Part XI. The diagram
  parses, the markdown looks right, `verify_names.py` is happy, and only a
  render shows it — so it survived two fact-checks, a lecture read, and the
  pass whose whole subject is figures, until a viewer agent said *three boxes
  say "Unsupported markdown: list"*. `check_mermaid.js` gates it now, with a
  nine-case probe measured in Chrome. **That is the fourth time this pass a
  gate has been blind to something its own standard cares about, and the
  second time the evidence was a picture nobody had opened.**

  Beside it, the pass's one outstanding tool job: F13's tree emitter, deferred
  to “the two part sessions that carry a tree, or session O”. `svg_tree` now
  lays a tree out repeatedly and keeps the first attempt that fits the reading
  column, shortening only the folded leaf label, because nothing else in a
  tree is elastic and a Mojang name is never shrunk. All **five** trees fixed
  at once: 1,619–2,217px → 810–1,020px, and the `Entity` tree from 0.62 at
  7.5px to **1.00 at 12px**. Parts XI and the frame get theirs for nothing.

  Eighteen corrections, all in [pass9.md](pass9.md). The sharpest is
  `damage-and-death`, where the prose says **eight** arithmetic steps and the
  figure drew **seven**, freezing and the helmet sharing a box — the page's
  own heading counts the eight. Beside it: `attributes` gave
  `permanentModifiers` to `AttributeMap.pack`, which filters nothing, rather
  than to `AttributeInstance.pack`, which is the one that does; `authority`'s
  predicate tree resolved *not client-authoritative* → *Player: always true*,
  the opposite of the page's own table; `ai-goals-and-brains` refused a
  schedule update after **20** ticks where the code and the prose say 21; and
  `entity-anatomy` called four families two and never named `Display` at all.
  Ten queue entries struck with the page open, five opened. All six gates
  green (the figure-name gate still report-only). Deployed.

- **2026-09-15, pass 7 session G (Opus) — Part VII · Items and inventories.**
  Nine viewer agents, one per page. **Seventeen figures became nineteen**: four
  pages split one figure at a joint the prose already names — `using-an-item`'s
  *ending* flowchart, which was two disconnected graphs in one box and is now
  the page's two endings; `recipes`' seven-lane trace, at the tick boundary its
  own note bar drew; `containers-and-menus`' seventeen-node ladder, into a
  four-row table and a five-node fork; and `loot-tables`' twenty-six-node funnel,
  which lost its placement tail to the trace above it and its five entry
  containers to a table. The part gained the book's **sixth `classDiagram`**
  (`items-and-stacks`, whose flowchart had four edgeless boxes and a subgraph
  title clipped mid-phrase on screen), and `enchanting`'s trace is **split by
  machine** with a lane each for the two copies of `EnchantmentMenu` — the page's
  own point, which one lane playing both sides had been hiding. Every figure is
  captioned and pointed at, **nothing below 0.79 and no type under 12.6px**, no
  lane over six, no flowchart over fourteen nodes, and the figure gate's **10
  unresolved names and 31 notes are 0 and 1** — the one a ruled note
  (`LootItemCondition.test` is `java.util.function.Predicate`'s). Nineteen
  corrections, all in [pass9.md](pass9.md), and **fifteen of them are the
  caller's-method-at-the-callee fault, which makes it six parts of six**; the
  sharpest is `loot-tables`' opening trace, which drew `ChestBlockEntity` and
  `RandomizableContainer` as two lanes exchanging a message when
  `RandomizableContainerBlockEntity` *implements* the interface, and had the
  clientbound content packet returning to `ServerPlayer`. **The session's own
  finding is a fifth tool blindness, and the one F10 walked into**:
  `check_figure_names.py` **read nothing at all inside a `classDiagram`** —
  zero names, zero figures — so the five class diagrams sessions B to F drew on
  F10's own recommendation had every name in them unchecked, and
  `pass7_figures.py` was counting the word `classDiagram` as a name the prose
  never says. Both tools now read the kind, with a **member line checked against
  its own class box** the way a message is checked against its lane; seven probe
  cases, and no previously-clean part moved. Beside it, **nine Mojang names the
  theme was hyphen-breaking on screen** (F18) — `AbstractContainerMe-nu`,
  `ClientboundContainerSetDataPack-et`, `doPostAttackEffectsWithItemSour-ce` and
  six more — every one of them the book spelling a name wrong in the picture
  while spelling it right in the prose, and all nine found **mechanically**:
  `render/index.json` records the on-screen text of every label, so a break is
  one regex over the render rather than nine pairs of eyes. Fifteen queue
  entries struck with the page open, one ruled out, twelve opened. All six gates
  green (the figure-name gate still report-only). Deployed.

- **2026-09-15, pass 7 session H (Opus) — Part VIII · The player.** Eight
  viewer agents, one per page. **Ten figures became twelve**, both new ones a
  split at a joint the page's own headings already name: `input-to-movement`'s
  one seven-lane trace is a client figure under *what the client decides and
  sends* and a server figure under *what the server does with the packet it
  gets* — the server half had been drawn ninety lines above the section that
  explains it — and `status-effects`' one trace is a server figure and a client
  figure, because it had **one `LivingEntity` lane standing for two machines**,
  told apart by two `Note over` lines, which is the thing F7 forbids by name.
  Every figure in the part is captioned and pointed at by a sentence; **nothing
  is below 0.80 or under 12.8px** (from four at 0.69 and one at 0.61/9.7px),
  nothing is over 1,200px tall, no lane is over six, and the gate's **1
  unresolved name and 7 notes are 0 and 0**, which makes Part VIII the second
  part clean on the notes as well as the failures. `player-anatomy`'s class
  ladder is the book's **seventh `classDiagram`** and the first drawn for
  inheritance rather than containment: its solid flowchart arrow had meant
  *extends*, a mark outside the grammar, and `<|--` says it natively while
  `<<abstract>>` marks the five rungs the game never instantiates — which also
  settled the reader's complaint that only `Player` carried *— abstract*.
  **The part's own fault is F7's, in the shape this part was always going to
  produce**: four of five sequence diagrams gave **one object two lanes by
  drawing a class-hierarchy rung beside its subclass** — `Player` beside
  `ServerPlayer`, `LivingEntity` beside `LocalPlayer`, `LivingEntity` beside
  `ServerPlayer` twice — on the one part whose whole subject is the inheritance
  chain. Folding them was the entire lane-budget fix; not one label needed
  shortening. Eighteen corrections, all in [pass9.md](pass9.md); the sharpest
  three are `the-two-phase-tick`'s figure, which drew the container check in
  phase one only under a sentence in bold calling it *the only work both halves
  do*; `the-sword-swing`'s, which drew the listener calling its own
  `isWithinAttackRange` when it is `Player`'s and the `Player` lane was already
  in the figure, landed `hurtOrSimulate` on `LivingEntity` when it is
  `Entity`'s and the page's own Reference link is *Damage outside
  `LivingEntity`*, and delivered the damage packet to `Minecraft` rather than
  to the listener that handles it; and `hunger-and-experience`'s regeneration
  figure, which drew **three siblings off one node where the code is an
  if/else-if chain whose order is the whole rule** — the shape was the error,
  and the fourth branch (the timer reset) had never been drawn at all. **The
  session's own finding is a sixth and seventh tool blindness, and this one had
  been there since the gate was written**: `check_figure_names.py`'s token
  regex needs two CamelCase humps, so **every one-word class name in a figure
  was unchecked** — `Entity`, `Avatar`, `Player`, `Mannequin`, `Item`, `Block`,
  `Mob`, `Screen`, `Window` — everywhere but a `participant` line; and its
  relation pattern allowed one character either side of `--`, so `<|--` never
  matched and **an inheritance relation was parsed as nothing at all**. Both
  fixed where the name is structural rather than free text (a `class Foo` box
  and both ends of a relation, with a box id that has a display label read as
  an alias the way a lane abbreviation is), each with a probe case; 43 more
  names checked corpus-wide, three more classes in the index, and no
  previously-clean part moved. Ten queue entries struck with the page open,
  eleven opened. All six gates green (the figure-name gate still report-only).
  Deployed.

- **2026-09-15, pass 7 session I (Opus) — Part IX · Networking.** Six viewer
  agents, one per page. **Twelve figures became eleven**: the buffer flowchart
  on `packets-and-stream-codecs` is a three-row table, because its three arrows
  meant two different things — two bindings and one *extends* — and a table
  carries the bind time the figure had no room for, which is F10's own ruling
  that two or three paths that differ are a table. Every figure in the part is
  captioned and every non-lead figure has a lead-in; **nothing is below 0.77 or
  under 12.3px** (from three figures at 0.38, 0.42 and 0.54 with 6 to 8.6px
  type), no overlap, overflow, clipping or edge through a node anywhere, no
  Mojang name broken on screen (five lines were), and the gate's **1 unresolved
  name and 19 notes are 0 and 0** — the third part clean on both. **The
  part-wide fault is session H's in the mirror**: Part VIII gave one object two
  lanes, and Part IX gives **two objects one lane**, because this part's whole
  subject is two machines running the same classes. `the-connection` drew one
  `Connection` lane for the object at each end and the paragraph beneath it
  *conceded the fault in words* — "which is what the note across the middle says
  and the picture cannot" — instead of the figure being redrawn;
  `chat-and-signing` drew two lanes both reading `ClientPacketListener`, told
  apart by a note naming two mermaid aliases that appear nowhere in the
  rendered picture. Both are fixed the way `authority`'s boat was: a second key
  row for the same class, and a `box` per machine. **And three of the four
  figures on `protocol-phases` were illegible for one reason — `direction
  LR`** — so two of the three fixes were deleting a line: F3 already rules `TD`
  for anything ordered in time, and a state machine is ordered in time. Nine
  corrections, all in [pass9.md](pass9.md); the sharpest are
  `protocol-phases`' configuration flowchart drawing
  `ServerConfigurationPacketListenerImpl.returnToWorld` as the **fifth step of
  the queue** when it is the call that *builds* the queue before any task runs,
  and drawing the client round trip that ends the phase as a plain unlabelled
  arrow — which is precisely the gap the page's own hook lives in;
  `what-the-client-is-told`'s cascade drawing position as a relative/absolute
  binary when the table under it names two further outcomes, *nothing sent* and
  *rotation only*; and `chat-and-signing` labelling the `ChatScreen` arrow with
  `ChatScreen.normalizeChatMessage`'s own work — **the caller's method drawn
  arriving at the callee, on the eighth part of eight**. **Two more tool
  blindnesses, the eighth and ninth of the pass.**
  `check_figure_names.py` read only the first 20 kB of a class file to find
  what it extends: exactly one class in the decompile declares itself past that
  mark — `ClientPacketListener`, at byte 21,133, behind three hundred import
  lines — and it is one of the book's commonest lanes, so every **inherited**
  member on a `CPL` lane was failing a figure that was right. And a `<br/>`
  between a name and the next word was welded shut, so the repair F18 itself
  prescribes made the gate fail: the rule is now F17's own wording — a name
  break is at a CamelCase boundary or at a dot and nowhere else. Four probe
  cases between them; corpus failures 31 → 30 and notes 166 → 148, with no
  previously-clean part moved. Ten queue entries struck with the page open, one
  of them a ruling asked for by name (**may a state machine contain a state
  nothing reaches? No** — a diagram draws the machine as it runs, and
  `NEGOTIATING` is the enum's business and the prose's). All six gates green
  (the figure-name gate still report-only). Deployed.
