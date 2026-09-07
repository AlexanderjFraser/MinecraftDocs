# The plan — the passes

*Rewritten 2026-09-02 at the start of pass 3, 2026-09-03 at its close,
2026-09-05 at pass 4's close and again that evening by the planning session
that set the ten-pass plan, and 2026-09-07 by the planning session between
passes 5 and 6. This is the document every session reads first and ticks
last. Each finished pass is archived whole in its own file —
[pass1.md](pass1.md), [pass2.md](pass2.md), [pass3.md](pass3.md),
[pass4.md](pass4.md), and for pass 5 [pass5-brief.md](pass5-brief.md), whose
Part 5 is the plan as it stood at pass 5's close: the fifteen session
paragraphs, the charter and the log, beside the brief, the runbook, session
A's rulings and the schedule. The queues: [pass5.md](pass5.md), opened as the
polish queue and now the queue passes 5–8 draw on, each entry taken by the
pass its kind belongs to; [pass9.md](pass9.md), where every pass-5-to-8
session lists the claims it introduced; [pass3.md](pass3.md) §7, the coverage
queue.*

## Where we are

**Passes 1 to 5 are done.** Every page was drafted from the decompile (1),
fact-checked twice with every page found wrong at least once each time (2 and
4), restructured into a book of thirteen parts and eight page shapes (3), and
then read *across* rather than down — one home per mechanism, the seams, the
through-lines, the thirteen landing pages as arguments, the coverage question
once per part (5). Pass 5 closed on 2026-09-07 with 171 corrections in
fourteen counting sessions, about half of them one page contradicting another,
which is the error two fact-checks could not see; every landing page was
rewritten to a stated role; seven parts that arrived with no anchors left with
them; and the gates grew by truth three times. Its whole record is
[pass5-brief.md](pass5-brief.md): Parts 1–4 the brief, the runbook, session
A's rulings and the schedule with what each session did; Part 5 the plan as it
stood at the close, with the session paragraphs and the log.

**Pass 6 — the lecture — is planned** (2026-09-07, the planning session on
Fable), and its next session is A. The charter is below; the brief, the
runbook, the standard session A rules on, and **the schedule with each
session's status** are [pass6-brief.md](pass6-brief.md) — Part 4's table is
where the owner sees which sessions are done. The planning session built
`tools/pass6_shape.py` (the devices, the skeletons, the budgets and the
landing pages, measured the same way every time) and `tools/pass6_prompts.py`
(a reader with nothing but the page; the measurements go to the session
instead), taught `pass5_queue.py` a `record` kind and to skip preambles,
re-routed 92 guessed queue units and struck 20 settlements no session had
struck, added `pass5_coverage.py --write` so a landing page's coverage number
is generated like its size, and re-counted every device: the closer is on 69
of 102 pages in **five** spellings (the charter had said seven), the 1.21
blockquote on **39** (it had said 42), 26 openings start on the word *You*,
and **27 links land on a closer's anchor** — the measurable form of a device
become load-bearing. The queue holds 136 `lecture` units. The latest release
is still 26.2 (26.3 at pre-release 2 of 2026-09-04, checked against the
version manifest), so no version pass is due before pass 6.

## The passes

| pass | what | lens | status |
|---|---|---|---|
| **1 — rough draft** | every page drafted from the decompile, names verified | — | done — [pass1.md](pass1.md) |
| **2 — completeness and accuracy** | every claim adversarially fact-checked; gaps filled; pages split and added freely | the adversary with the source | done, 2026-09-01 — [pass2.md](pass2.md) |
| **3 — restructuring** | the site became a book: each part the shape of its system, each page one of eight shapes; the frame, the maps and the Reference tier redone; the lecture order drafted | the shape | done, 2026-09-03 — [pass3.md](pass3.md) |
| **4 — the second fact-check** | pass 2's protocol over everything pass 3 rewrote; the claims pass 3 introduced checked first | the adversary again | done, 2026-09-05 — [pass4.md](pass4.md) |
| **5 — the book** | across pages: one home per idea, the seams, the through-lines, the landing pages as the part's argument, the coverage question once per part, the last moves | the book as one thing | done, 2026-09-07 — record [pass5-brief.md](pass5-brief.md); queue [pass5.md](pass5.md) |
| **6 — the lecture** | one page at a time: the devices that became slots, the twin skeletons, section order, the cuts, the landing pages' seventh section; a page that reads as one lecture's notes | the reader with only the page | **current** — planned 2026-09-07; charter below; brief, runbook, standard and the schedule with each session's status [pass6-brief.md](pass6-brief.md); queue [pass5.md](pass5.md), kind `lecture` |
| **7 — the figures** | every figure as rendered, beside its section: the true shape, legibility, lanes, labels; the gate over names inside mermaid blocks | the picture | after 6 |
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
page, and `tools/deploy.sh` refuses to publish on any failure. Reasoning over sensing over measuring: no count in a
queue is a target, and the owner judges what lands.

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
## Pass 6 — the lecture (current)

**Goal:** each page is one lecture's notes — in the shape of its story,
opening inside the scenario on a hook that holds, its trace the spine and
its figure the artefact, reading differently from its neighbours, speakable
in a sitting.

**The brief, the runbook, the standard and the schedule** are
[pass6-brief.md](pass6-brief.md), written by the planning session on
2026-09-07: Part 1 the reader's brief, Part 2 the runbook, Part 3 the rulings
session A makes — written as the planning session's recommendations with the
number behind each — and Part 4 the schedule, sessions A–O, one part each,
with a **status** column each session fills in itself. That table is the one
place the owner reads to see which sessions are done.

**The queue it draws on:** [pass5.md](pass5.md) holds **136 units of kind
`lecture`** after the planning session re-routed the guessed kinds (I 5 · II 2
· III 11 · IV 11 · V 7 · VI 10 · VII 13 · VIII 6 · IX 17 · X 13 · XI 8 · XII 8
· XIII 12 · the frame and Reference 13); 45 units in the file are still
guesses, and a session tags what it finds misrouted as it reads. `python
tools/pass5_queue.py --kind lecture --part <dir>` is the per-part checklist,
and `[kind=record]` marks a unit no pass acts on.

**The jobs**, each with the number the planning session measured
(`tools/pass6_shape.py`; the per-part tables are in the brief's Part 4):

1. **The devices that became slots.** The *Questions players ask* closer on
   **69 of 102** system pages in five spellings, on every page of Parts IV, V
   and VIII and nine of ten in XII, not the last section on four pages, and
   cited from other pages by **27 links** — an answer another page needs,
   sitting in a slot named for questions a player asks; the literal `## The
   trace…` heading on **20**; the *for a 1.21-era reader* blockquote on **39**,
   at the foot of the page on 23 (all of Parts X and XI) and in the body on
   16; the opening ending on a bold sentence on **28** and on a dash clause on
   34; the second person in **41** first sentences, **26** of them the word
   *You*, on all eight pages of Part VII. Ratified or reversed corpus-wide in
   session A, not page by page. On the landing pages, two more: the
   recognition sentence on nine of thirteen, and on five the argument's last
   sentence; and the phrases that became labels, which are pass 8's.
2. **The skeletons.** Six identical spines shared by fifteen pages, none
   inside one part; seventeen within-part pairs one edit apart, densest in
   Parts VIII, X and XI; session P's groups still hold in the tokens. The later
   page of a within-part pair varies, unless the pair is one pass 5 declared.
3. **The section order**, where a fact fix left the exception before the rule
   or the concession inside the hook, and where a heading names two of a
   section's three subjects.
4. **The cuts.** Thirteen pages over 450 lines and a corpus median of 356;
   pass 3's per-page cheapest cuts still logged; and the thirteen landing
   pages, which run 57 to 179 lines outside the watch order (median 132)
   against the template's about a hundred, almost all of the growth being the
   seventh section — the coverage answer — which is a heading on nine in three
   positions, a headingless paragraph on three and absent on one. **The seventh
   section gets its place in `TEMPLATE.md` in session A** and the trim follows
   from the shape; its number comes from `src/generated/coverage-<dir>.md` and
   is hand-counted on four pages today. No line count is a target: the reader's
   skip list and the hook decide a cut, and a cut is a move or a logged cut.
5. **The completeness lists** for the four Reference catalogues: three settled
   in pass 5, the fourth (`level-data-and-rules`) session N's.
6. **Every page-shape finding in [pass5.md](pass5.md)**, checked against the
   page before it is acted on.

**The agent** is a reader with nothing but the page — no source and no other
page, on purpose — asked four questions: where did you get lost, what did you
have to read twice, what did the page assume you already knew, and what did
you skip; then the page in one sentence, the section it would cut first and
the question it still has. The session decides, with the measurements the
agent never sees.

**The rhythm** is pass 5's, which worked: session A settles the corpus-wide
rulings — the second person, the closer's rule and spelling, the blockquote's
place, the trace heading, the hook's bold, the landing page's seventh section,
the twin rule, the section order, the cuts — and rewrites one exemplar page to
them; B–N take the parts in sidebar order and O closes. Each part session ends
by re-syncing its landing page and its section of `lectures.md`, and **session
O checks the thirteen**, which is where pass 5 found thirteen of its last
twenty corrections.

**Two warnings from pass 5's close, both about the queue.** A settlement that
is not struck is invisible: twenty-six of pass 5's forty open `book` entries
had been done and left standing, and the planning session found twenty more
that pass 5's own sessions had settled and not struck — so **a session strikes
as it settles, in the same commit**. And a strike sits outside the bold —
`- ~~**text**~~`, not `- **~~text**~~` — or `pass5_queue.py` cannot see it.

**Not:** facts; a figure beyond what a reshaped section needs; voice; a page
moving.

## Pass 7 — the figures

**Goal:** every figure is the true picture of its system, legible at the
column width and on a slide, and every name in it is under a gate.

**The jobs:** render every diagram — the 195 mermaid blocks, the generated
SVGs, the parts-dependency figure — and put each beside the section under it
in front of an agent that has the picture and the section and not the
source: is this the shape (a trace whose truth is a graph; a secondary state
diagram that is really the page's picture; two figures for one mechanism, as
on `prediction-and-acks`); the lanes (at most seven; the 45 key rows no page
claims, pruned; the one class with two lanes); labels that are sentences;
density (the sixteen-edge spawn cascade, the fourteen-edge event loop, the
27-item start-up sequence); whether figures carry captions; the
tick-boundary bars. **The gate over figures:** names inside mermaid blocks — 453
tokens no gate has seen, and the same parser gives the class index its 135
missing page pairs — built by the planning session, report-only through the
pass, a deploy gate at its close. `TEMPLATE.md`'s mermaid rules corrected to
what 11.6.0 actually rejects (session O of pass 4 measured it). The
generated Reference views' table shapes. Rendering needs a real browser, not
jsdom, and the planning session chooses one.

**Not:** facts (an arrow found wrong is re-derived and logged as a
correction); prose beyond a caption.

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
## Session log — pass 6 onward

*(newest last; pass 5's log — the planning session between passes 4 and 5,
sessions A to I in full, and the note on where J to O wrote theirs — is in
[pass5-brief.md](pass5-brief.md) Part 5, and pass 4's at the end of
[pass4.md](pass4.md))*

- **2026-09-07, planning session (Fable, between passes 5 and 6).** No page's
  prose touched. **Pass 6 planned**: [pass6-brief.md](pass6-brief.md) — Part 1
  the reader's brief (nothing but the page; four questions and three
  comparisons), Part 2 the runbook, Part 3 the standard as eleven
  recommendations with the numbers behind them for session A to rule on, Part
  4 the schedule with a **status column** the owner reads. **The tools**, each
  with a `--probe`: `pass6_shape.py` (per page: the opening's person and
  ending, the spine as tokens, the closer's spelling and position and
  questions, the literal trace heading, the 1.21 blockquote and its place, the
  cast against *Where to look*, the list and long-section budgets; per corpus:
  the skeleton twins, the slots ranking; per landing page: lines outside the
  watch order, the seventh section, the recognition sentence, a hand-counted
  number), `pass6_prompts.py` (the brief and the path for the reader; the queue,
  the shape report, the twins and the inbound links by anchor for the session),
  `pass5_queue.py` (a `record` kind for units no pass acts on; preambles no
  longer counted as entries), `pass5_coverage.py --write` (thirteen generated
  coverage phrases, `src/generated/coverage-<dir>.md`, run by `deploy.sh`
  after the atlas). **The queue re-measured and re-routed**: 92 guessed units
  tagged and 20 settlements struck after each was verified against the page or
  the log it names; the guesses fell from 198 to 45 and the `lecture` count
  from 158 to 136, the difference being preambles and misroutes that had been
  counted as work. **Two findings about the record itself**: session E's log
  said the hopper and four block-entity state machines went to §7, and they
  had not — carried now, with the note that `blocks/README` still says one
  thing in the part belongs to nobody, for Part V's pass-6 session; and the
  charter's device counts were wrong in two places against the tool (seven
  closer spellings is five; 42 blockquotes is 39), corrected. **Housekeeping**:
  the pass-5 narrative moved out of this file into
  [pass5-brief.md](pass5-brief.md) Part 5, headings demoted, so this file is
  again the current charter and the passes to come; `CLAUDE.md`, `README.md`,
  `pass5.md`'s preface, `pass9.md` and the memory brought current; the version
  manifest re-checked (26.2 is the latest release; 26.3 at pre-release 2). All
  five gates green; nothing deployed, because no published page changed.
  **Rulings**: a queue unit no pass acts on is tagged `record` rather than left
  to be counted as open work; the schedule's status column is the one place the
  owner reads for which sessions are done, and each session writes its own
  cell in step 9; a planning session may strike a queue entry only with the
  page or the log open, and says which in the strike.
