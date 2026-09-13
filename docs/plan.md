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

**Pass 6 — the lecture — is running.** It was planned on 2026-09-07 by the
planning session on Fable; **session A set the standard on 2026-09-10, with
sessions B (Parts I and II), C (Part III) and D (Part IV) the same day and E
(Part V), F (Part VI), G (Part VII) and H (Part VIII) on 2026-09-13**, so the
next session is I (Part IX · Networking). The charter is below; the brief, the
runbook, **the standard as session A settled it** and **the schedule with each
session's status** are [pass6-brief.md](pass6-brief.md) — Part 3 is what a part
session applies rather than re-decides, and Part 4's table is where the owner
sees which sessions are done. The planning session built
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
| **6 — the lecture** | one page at a time: the devices that became slots, the twin skeletons, section order, the cuts, the landing pages' seventh section; a page that reads as one lecture's notes | the reader with only the page | **current** — planned 2026-09-07, sessions A to D done 2026-09-10 and E, F, G and H on 2026-09-13; charter below; brief, runbook, the settled standard and the schedule with each session's status [pass6-brief.md](pass6-brief.md); queue [pass5.md](pass5.md), kind `lecture` |
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

**Pass 6, session H — Part VIII · The player** *(2026-09-13).* Seven system
pages and the landing page, eight readers, one each. The part arrived at
**7 of 7** on the closer and **four** literal trace headings, the joint-worst
pair of numbers in the book, and it took session G's parting advice first:
`check_links.py --inbound` on all seven pages before deciding anything. That
found four citations landing on a device's anchor, and **not one of them wanted
the section it named**. Two pages cited `hunger-and-experience`'s closer for a
0.1 exhaustion figure that closer never mentions. `player-anatomy` cited the
sword swing's closer for the two combat clocks, which were the back half of an
answer about mashing. `the-two-phase-tick` cited `player-anatomy`'s closer for
why item ticking needs two callers. Each was promoted to a section and
repointed. Then, after the four trace headings were renamed, the link gate
turned up a fifth and sixth of the same kind: `authority` and `the-spear` had
both been landing on `input-to-movement`'s single trace anchor and wanting
opposite halves of a 150-line section. The closer went **7 of 7 → 6**, and the
one that dissolved whole was `the-spear`'s, whose five answers were three
second tellings and two body sections wearing a question mark — the cast table
had promised the mob path 190 lines earlier and only the closer delivered it.
Four other closers lost their load-bearing answer and kept their consequences.
**Twenty-three facts corrected**, twenty-one of them found by a reader with no
source, and the class is by now familiar and still undiminished: a record of
"four textures — body, cape, elytra"; a player "five classes deep" whose own
figure draws six; a hook saying the main-hand item "is not stored anywhere"
against its own payoff saying "not stored *twice*"; a closer saying the *one*
thing that stops phase two against a gate the same page names thirty lines
above; a landing page whose "four things it does" sits over a watch order with
five; a mannequin's split "one class lower" than a class the page calls its
sibling. The sharpest is `the-spear`'s: *if any of the three conditions passes,
the damage is…* — three conditions that in fact gate three different effects,
so a charge can knock a target off a horse and do nothing to it. The fifth and
last hand-counted landing-page number went to the include, and was wrong like
the other four (*97%*, in fact 100%). Seven *Where to look* lists became prose
reading routes under A12, with twenty-two names rescued back into prose by the
token diff. **A7** was the queue's fourth stale twin entry running: the pair it
named (`the-spear` / `the-sword-swing`) had dissolved, and what was live was
`input-to-movement` one edit from *three* of its own neighbours — a hub, not a
pair. It varied by splitting its trace section into two H2s and promoting six
bold lead-ins to H3s, which is the same edit the queue had asked for
separately, on the grounds that nothing could anchor to them. Part VIII's seven pages 2,081 → 2,328 lines, and
its landing page 164 → 179. Thirty-one units appended to [pass5.md](pass5.md) (seven logged
cuts, seven for pass 7, six for pass 8, three for pass 9, and one structural
note for session O); nine entries struck and three annotated; the session's
entry in [pass9.md](pass9.md). All five gates green; deployed.
**What the session would tell the next one**: sessions F and G found that a
renamed closer and an inbound link into a closer are both invisible to the
tools. Part VIII adds the reason they are, and it generalises past closers:
**an anchor that names a device rather than a subject collects citations that
mean different things, and nothing can see the mismatch, because a link
resolves against a heading and not against a sentence.** The link checker only
ever catches it at the moment the heading moves — which turns A4's rename from
a tidying job into a diagnostic, and is an argument for renaming the trace
headings in Parts XII and XIII even where nothing else on those pages needs it.
One caveat for session O: renaming them **changes what `pass6_shape.py`
measures**, because its spine alphabet reads the literal `## The trace` as its
own token; Part VIII came out of the rename with a measured identical pair that
was an artefact, and the tool cannot see an H3 at all.

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

- **2026-09-10, session A (Opus) — the standard and the exemplar.** Pass 6's
  rulings made once, and one page rewritten to them. **Nine of the eleven
  recommendations ratified; A2 amended and A12 added.** A2's *at most about
  half a part* became a **smell rather than a quota** — a quota would strip a
  closer off a page whose every answer passes the test, and A9 refuses exactly
  that reasoning two rulings later ("a count in a queue is a description, not
  a target"); the test alone decides, and a part that finishes its session
  still at 10/10 says in its log why each survivor passed. **A12** is session
  A's own: ***Where to look* is a reading list, not an index** — measured over
  the 102 system pages, the median is 18 names, 61 pages carry more than
  fifteen, and **82 pages carry at least one name that appears nowhere else on
  the page, 513 in all**, which is the field inventory pass 3 dropped coming
  back under a new heading. `TEMPLATE.md` rewritten in seven places: the
  landing page's seventh section ***Where the part stops*** in its fixed place
  (after the watch order, before the shelf) and the argument ending on the
  claim; the closer's one spelling and its test; the blockquote's place, length
  and reason; the way into a scenario and bold on the hook; one subject a
  section and the rule before its exception; *Where to look*; and who a page's
  *neighbours* are, which is what makes the twin rule operable.
  **The exemplar**, `world/environment-attributes-and-timelines`, read by one
  agent under Part 1's brief and rewritten: the closer 5 questions → 3, the two
  that carried the page's own mechanism moved into the body where they teach;
  the literal trace heading and the verified line renamed to the scenario; the
  1.21 blockquote 11 lines in the body → 8 at the foot; a 45-line
  three-subject section given three H3s **inside its existing anchor**; a
  two-sentence signpost in the cast for the reader who "had stopped expecting
  a trace" 230 lines in; four cuts logged; 414 → 444 lines, and A9 now says in
  writing that a page may come out longer. `commands/README` is the first page
  in the book to carry a generated coverage number
  (`{{#include ../../generated/coverage-commands.md}}`). **Five facts
  corrected**, every one found by a reader with no source, no other page and no
  measurements, on a page fact-checked adversarially twice: a stretch of 1,800
  ticks pinned to one instant, a danger ending at the wrong end of the night,
  four numbers in a record that holds three, a five-weight kernel over six
  cells that does not close, and an accessibility option described as always
  on. That is the pass's first evidence that it earns its cost. Fifteen units
  appended to [pass5.md](pass5.md) (four logged cuts, two for the part
  sessions, three for pass 7, six for pass 8); the session's entry in
  [pass9.md](pass9.md). All five gates green; deployed. **Rulings**: the test
  decides and no count in this pass is a target (A2, restating A9); a session
  that finds a real error stops and re-derives it even when its own brief says
  it changes no facts (A11's departure) — a lens is never kept clean by
  publishing a sentence known to be false.

**Pass 6, session C — Part III · The server** *(2026-09-10).* Five system
pages and the landing page, six readers, one each. Part III arrived as the
part that was already *inside* the rules — 2 of 5 on the closer, no literal
trace heading, a median of 470 lines — and the session's finding is that
being inside a rule of thumb settles nothing: **both closers failed A2's test
in part**, and every one of the six pages had something a reader with no
source could not get past. `server-tick` went 4 questions to 2 and then to 3
sections richer: the autosave arithmetic moved up beside the countdown it is
about, and *does freezing stop the server* turned out to hold the page's only
definition of **frozen** — a word its `tickChildren` table uses in three rows,
240 lines above — so the mechanism went up under the table and the question
kept the consequence. A fourth thing in that closer was not a question at all
and is now the close of *An empty server stops ticking*.
`server-level-tick` went 7 to 4: two answers were second tellings of sections
the reader had passed within fifty lines, and *where did the day–night cycle
go* was written for a 1.21 reader, so it is the page's blockquote now — the
third page in the part to gain or move one to the foot, which makes 3 of 5 at
the foot and none in the body. Three of that page's headings overclaimed
against its own figure (*the one thing a freeze cannot stop* over nine ungated
steps; *the two steps that always run* over the same nine; *five things in one
call* over a figure that splits the third), and the fix for the third was not
the heading — `ServerChunkCache.tick` really is five statements — but the
prose, which became the part's only list, answering a question pass 3's
session D left open in 2026-09-02. **A7 bit here**: `starting-a-server` /
`how-a-server-dies` were one skeleton run forwards and backwards, and
`how-a-server-dies` was one edit from `players-and-sessions` as well, so the
later page varied by putting its **comparison table before its cast** — the
page's artefact is the three-way table its hook promises and it was sitting
behind eight rows of cast. Its *Three booleans and a question* dissolved into
the three sections that use each boolean. No page in the part now shares a
spine with any other, in the part or out of it. **Six facts corrected**, the
sharpest on the landing page: it said `MinecraftServer` was not counted in
Part III's size, which is why the atlas counts it under Part I — and the
atlas's Part III spec is `net/minecraft/server` itself-only, so it is counted
in both, which is the answer to the question the reader ended the page with.
Four *Where to look* lists came down from 26, 33, 33 and 24 names to 17, 19,
19 and 15 under A12, each in the page's own reading order, with no name lost
from the book. Part III went 2,357 lines to 2,367 — up, as A9 says a part may
be. Twenty units appended to [pass5.md](pass5.md) (five for pass 7, nine for
pass 8, five for pass 9, one on the list question); nine queue entries struck
and two annotated; the session's entry in [pass9.md](pass9.md). All five gates
green; deployed. **What the session would tell the next one**: three of the
five pages open on a figure the page cannot yet be read against — the lead
sequence or flowchart names five or six mechanisms whose prose is below it,
and every reader said so independently. That is a part-wide pattern rather
than three pages' bad luck, and it is pass 7's, so it went to the queue whole
rather than being patched a page at a time.

**Pass 6, session B — Parts I · Anatomy and II · Foundations** *(2026-09-10).*
Nine system pages and two landing pages, eleven readers, one per page. The
part-wide judgements first: the closer went from 6 of 7 Part II pages to 4,
and from Part I's one page to none of its own mechanism, under A2's test
rather than a quota — `resource-system` keeps its five because every answer
is a thing a player meets (a texture stops animating, a datapack appears and
a resource pack does not, every pack turns itself off, `/reload` freezes the
server, vanilla cannot be disabled), and `identifiers-and-registries` and
`data-driven-types` lost theirs entirely because not one of their twelve
questions was a consequence: they were the page's own mechanism wearing a
question mark, and eight of the twelve moved up into the section that needed
them, `HolderOwner.canSerializeIn` travelling 363 lines to the sentence that
first uses it. Two blockquotes moved to the foot and two more were *created*
out of closer answers and body asides addressed to a 1.21 reader (`tags`'
missing *TagManager*, the registries page's datagen answer), which is the
device used as a device rather than filled as a slot. The one within-part
twin pair, `tags` ↔ `data-driven-types`, was varied on the later page by
dissolving its questions — three edits between the spines where there was
one. `tags`' pay-off finally has an anchor: six H3s inside the H2 the three
citing pages already point at, so a citation lands on the paragraph rather
than on a hundred-line section. `what-this-book-skips` was judged whole and
came down 476 → 457 by cutting the nine *covered* and *absorbed* rows of its
rulings table — nine rows about things the book does **not** skip, on the
page that draws the boundary — to one paragraph, and its citation of "rule
three" now names the rule and takes the anchor, which was the only mechanism
in the book cited by number without one. Both landing pages were re-argued to
A6 with the seventh section in its place and a generated coverage number:
Part I's argument now *names* the four threads it had promised three times
and never listed, and Part II's says what its seven pages have in common
instead of ending on a list of symptoms. **Nine facts corrected**, all nine
found by readers with no source: four indexes that are five, an arrow to a
registry the prose says is never consulted, a thread cell its own page
contradicts, a scoping error that made a paragraph deny its second half, two
"the one" claims with a second instance ten paragraphs away, a stage count
against its own figure, and a section whose lead excludes its own third
group. Part I came out at 869 lines against 871 and Part II at 2,965 against 3,002. Nineteen units
appended to [pass5.md](pass5.md) (eight for pass 7, eight for pass 8, two for
pass 9, one coverage decline to [pass3.md](pass3.md) §7); eight queue entries
struck and two annotated; the session's entry in [pass9.md](pass9.md). All
five gates green; deployed. **What the session would tell the next one**: the
readers' single most valuable output was not a list of confusions but the
*count* disagreements — five of the nine corrections are one sentence
contradicting another sentence or a figure on the same page, which is the
error class pass 5 could not see because it read across pages and pass 4
could not see because it checked each claim alone.

**Pass 6, session D — Part IV · The world** *(2026-09-10).* Ten system pages
and the landing page, eleven readers, one each. Part IV arrived as the part
where A2 bites hardest — the closer on **10 of 10** — and the test took it to
**8**, because two pages turned out to be answering themselves.
`chunk-anatomy` lost its closer entirely: not one of its six answers was a
consequence a player meets, and every one of them was a thing the body already
needed. The section permit and `ThreadingDetector` were used in the cast table
and again 170 lines later and explained only at the foot; the client's two dead
counters belong beside the four counters; `LevelChunkSection.maybeHas` was
**cited by `points-of-interest`** at an anchor whose prose never mentioned it,
which is A2's load-bearing rule in its purest form; and the chunk's wire form is
its third serialised shape beside memory and disk, so it became an H3 that Part
IX's own summary now points at. `fluids` lost its closer for the mirror reason:
two answers were the page's machinery (the block tick that is really bubble
columns, the occlusion cache the *body* wanted 180 lines earlier — and the
glossary's *Occlusion* entry cited it, so it moved up under a heading and the
citation was repointed in the same commit), and the other two were second
tellings of bold sentences. Six more closers came down 4→3, 5→3, 5→3, 5→3, 6→5
and 4→3. **Both literal trace headings are gone**, three inbound links
repointed; four more headings were renamed because their own sections
contradicted them — `chunk-storage`'s *Three folders* over a list of four, and
*The dispatcher never queues* over a section whose last paragraph is
`GameEventDispatcher.handleGameEventMessagesInQueue`. All four 1.21 blockquotes
are at the foot now, from none. The part went from ten long sections to none,
on six H3s inside existing anchors. **Nine facts corrected**, every one found
by a reader with no source: a pyramid count where seven plus four is eleven
(the page's own closer had it right and the body did not); *four of the twelve
steps* where the flag word touches three; a light flood said to stop at level 1
when it stops *propagating* at 1 and writes it; `sectionLightChanged` with two
gates where the figure had one and the prose the other; a sky column answering
15 by walking upward where the body says, correctly, without looking; a
container sent back to the wrong queue when the budget runs out; and on
`points-of-interest` a hook that says *the single behaviour that reads the flag*
where three do. The ninth is on **session A's own exemplar**: mobs stop burning
"until dawn" against the page's own 23460 and its own "tick 0 is dawn", and
`day.json` has no marker called dawn. The landing page gained *Where the part
stops* — the first thing in the book to explain the world border's absence,
which gave a dangling "for the reason above" the antecedent it had lost — and
stopped promising a lecture on *sending*, which is Part IX's. Eight *Where to
look* lists came down from 17–27 names to 12–17 under A12, each in its page's
own reading order, no name lost from the book. Ten pages 4,160 → 4,185 lines.
**One tool bug**: `pass6_shape.py`'s question regexes used `[^*]`, so a bold
lead-in with italics inside it counted as neither a lead-in nor a question —
fixed, with a probe, and every closer count this pass has published may be low
by one. Twenty-eight units appended to [pass5.md](pass5.md) (seven for pass 7,
eight for pass 8, seven logged cuts, six part-wide answers); eight entries
struck and four annotated; the session's entry in [pass9.md](pass9.md). All
five gates green; deployed. **What the session would tell the next one**: the
readers' most valuable output was again the count that does not close. Five of
the nine corrections are one sentence disagreeing with another sentence or a
figure **on the same page** — the same class session B named — and three of
those five were found by a reader simply doing the arithmetic the page invited.
A page that shows its working is a page that can be caught.

**Pass 6, session E — Part V · Blocks** *(2026-09-13).* Seven system pages and
the landing page, eight readers, one each. Part V arrived at **7 of 7** on the
closer — the worst per page in the book — and came out at **4**, with three
dissolving whole rather than being trimmed. `blocks-and-states` lost all three of
its questions *upward*: the `Level.setBlock`-returns-false answer became the only
prose in the book that reads the two diamonds in its own write figure, the
property-identity throw went beside the reference comparison that causes it, and
the third was the payoff of **the page's own hook** — an unknown state quietly
becoming air — which the body never developed at all and which now has an H3.
`signal-and-dust` lost three second tellings and moved its torch burnout up to
the source census where a torch is first named, which is also the A7 variation
that pulled it apart from `block-entities`. `diodes-and-observers` lost four
second tellings, and the one line worth rescuing turned out to be **false**. The
survivors went 4→2, 4→3, 4→2 and 5→2, and every one of the eight questions left
is a consequence a player meets that the body does not state.
**The part-wide finding is the flag word.** Four of eight readers independently
said the lead figure spends a flag word the page has not minted:
`blocks-and-states` hands the reader *flags 11*, then gates eight bare numbers
through a flowchart, and names a bit for the first time 150 lines later in a
section that defers the whole legend to Reference. The prose half is fixed on all
four pages — a legend before the figure, name paired with number — and the figures
went to the queue whole, because whether a flowchart gate may carry a constant
name is pass 7's ruling and not four pages' patching. **Fifteen facts
corrected**, every one found by a reader with no source, and three of them are
counts that do not close against the page's own enumeration — the error class
sessions B and D both named. The sharpest is on `block-breaking`, where the hook
says neither clock is ever mentioned on the wire and the page's own section says
the server broadcasts its clock to everyone within 32 blocks but the breaker;
next to it, the same page called the two clocks *a tick apart* and *the same
number* in one section, and the reconciliation — the STOP is handled in the packet
drain, before that tick's increment, so the server measures the span the client
counted — is the part's own recurring fact and was nowhere on the page. The
landing page was re-argued to A6 with *Where the part stops* in its place, a
generated coverage number, and an argument that at last **names** the four
answers a block can give and binds two of them to the two channels: pass 5 had
left that binding inside two mermaid edge labels, so a reader finished the page
unable to say what it had promised. Its *one thing belongs to nobody* sentence
became three, which is what [pass3.md](pass3.md) §7 has carried since the
planning session. Eight *Where to look* lists became prose reading routes under
A12, with no name lost from the book — checked by diffing every backticked token
against `HEAD` and then against all of `src/`, which caught four and put them
back into prose. Part V 2,530 → 2,646 lines. Fifty-one units appended to
[pass5.md](pass5.md) (eleven logged cuts, six for pass 7, eight for pass 8, four
for pass 9); eight entries struck and two annotated; the session's entry in
[pass9.md](pass9.md). All five gates green; deployed. **What the session would
tell the next one**: the readers earned their cost twice over, but not where the
brief expected. Their four questions produced good structural findings; their
*Suspected errors* section produced fifteen corrections, and the ones that
mattered were never "this sentence is false" but "these two sentences cannot both
be true". Nine of the fifteen are one sentence against another sentence, a
figure, or an enumeration **on the same page**. A part session should read that
section first and treat the rest as evidence.

**Pass 6, session F — Part VI · Entities** *(2026-09-13).* Nine system pages and
the landing page, ten readers, one each. The part arrived measured at 3 of 9 on
the closer, which looked like the most comfortable part in the book, and **the
measurement was the finding**: three more pages carry the identical device under
a name of their own — `entity-anatomy`'s *The id, the box, and the numbers on
the type*, `authority`'s *What the predicates explain*, `pathfinding`'s *Why
mobs look stupid*, all three renamed by pass 2's own session to make the part
look less uniform. Six of nine, then, and the test took it to **one**.
`authority` keeps three answers that are consequences a player meets; the other
five dissolved, and the two promotions are A2's load-bearing rule at its
sharpest. `entity-anatomy`'s two-numbers answer became a section its **own cast
row had been promising for 350 lines** ("the two numbers that decide how it
reaches clients") and which `synched-entity-data` cites at that anchor; and
`synched-entity-data`'s *can two mods both add a field* was the payoff of the
page's own hook — one new field on `Entity` renumbers every entity in the game —
sitting at the foot of the page under a question mark, and is now an H3 inside
the anchor eight pages land on, with the `Display.RENDER_STATE_IDS` paragraph
moved up beside it as its evidence. **A7's pair was not the one the queue named**:
`attributes` / `synched-entity-data` had come apart in pass 5, and what the tool
found live was `entity-anatomy` ↔ `authority` inside the part, with `authority`
identical to `items/recipes` across parts. `authority` varied by **leading with
its three-case comparison table** — the artefact its hook promises, which was
sitting behind a cast table every reader skipped, a flowchart, and two
paragraphs of predicates the table would have explained. The part's **first 1.21
blockquote** was created rather than moved, out of the *Schedule does not exist*
clause that was costing `ai-goals-and-brains` its opening. Eight long sections
went to none on eleven H3s inside existing anchors. Nine *Where to look* lists
became prose reading routes under A12 — Part VI had a median of **30** names,
the worst in the book — with no name lost, checked by diffing every backticked
token against `HEAD` and then against all of `src/`, which caught six and put
them back into prose. **Fifteen facts corrected**, every one found by a reader
with no source: six overrides described as nine, a tree that reads as 190
against its own 191, seven species named as six, two rules that are three, four
classes named as three, an armour formula with two legal parses and an unvalued
divisor, *sixteen pages* that are nineteen, *three later pages* that are one, a
ninth reading that is a ninth site, a figure label that dates the mob instead of
the call, and on the landing page three counts at once — three reference pages
that are five, a hand-counted 40% that is 34%, two rungs that are four. The
landing page was re-argued to A6 with *Where the part stops* moved from first to
its place and cut to 21 lines, a generated coverage number, and an argument that
at last **names `Entity`**, the base class the part is about and had never
named, and ends on the claim rather than on four shared things. Part VI 3,752 →
3,861 lines. Thirty-three units appended to [pass5.md](pass5.md) (nine logged
cuts, eight for pass 7, eight for pass 8, five for pass 9, three answers a page
still owes); nine entries struck and two annotated; the session's entry in
[pass9.md](pass9.md). All five gates green; deployed. **What the session would
tell the next one**: a device that has been *renamed* is still the device, and
the tool cannot see it. A2(a)'s one spelling is usually read as a tidiness rule;
it is the measuring instrument, and Part VI is where it earned that — the part
that looked half-clear was the second most uniform in the book. The other half
of the lesson is A12's: nine lists at a median of thirty names, and six names
that existed nowhere in the corpus except inside them, which is the field
inventory not merely come back but become the *only* home. Run the token diff —
and run it against hand-written pages only: the first pass of it missed three
names because `class-index.md` is generated *from* the pages and still listed
them. Regenerate the index before the commit, not after.

**Pass 6, session G — Part VII · Items and inventories** *(2026-09-13).* Eight
system pages and the landing page, nine readers, one each. The part arrived
measured at **2 of 8** on the closer — the most comfortable-looking part since
III — and the queue asked the opposite question, whether three closer-less
pages should *gain* one. Both readings were wrong, and in opposite directions.
The three were **ruled out**: A2(e) is permissive, none of the three had a fact
that was lost rather than a promise unpaid, and adding closers to a part
measured at 2 of 8 would manufacture the uniformity A2 exists to break. Mean-
while the two that existed did not survive the test. `enchantments`' was 103
lines and **nine** questions under a name of its own, and **three of its answers
were cited from three other pages, each landing on a different answer inside the
one anchor** — A2's load-bearing rule at its sharpest so far, because no reading
of the closer as a whole could have found it and no tool sees a link's
destination *within* a section. Four answers became body sections, three inbound
links were repointed, and two consequences stayed. `loot-tables`' dissolved
whole: its first question was **the page's own hook's payoff**, sitting at the
foot under a question mark while the body never delivered what the opening
promised, and the section it became answers the reader's question the closer had
not — that breaking an unopened chest commits the roll too, luckless, through
`BlockEntity.preRemoveSideEffects`.
**Fifteen facts corrected**, thirteen of them found by a reader with no source,
and the sharpest is on `items/README`: the recognition list called the tick-late
chest one of the part's prediction lies, four paragraphs above the page's own
statement that the container click is not on the prediction ledger. Sorting the
four symptoms into the three that are guesses and the one that is not turned out
to *be* the argument the landing page was missing, so A6's reversal of the
recognition sentence paid for itself in a way no session had seen. Beside it a
fourth hand-counted landing-page number went to the include and was wrong again
(*about a third*, in fact 24%). The rest are the error class sessions B, D, E and
F all named: a diagram that says *no arrow* where the prose says *a phantom
arrow*; nine `CustomRecipe`s listed as eight names and a sibling; a figure node
that says *stale* where the code says *empty*; "five menus" with two named; "five
enchantment hooks" with four; ten data slots with four accounted for; two
sentences about one method's two branches, each true, reading as a
contradiction.
Eight *Where to look* lists became prose reading routes under A12 — Part VII's
median was **27** names, second worst in the book — and **every one of the nine
readers skipped its page's list**, five of them saying in almost the same words
that it was an index of the page's own backticks rather than a place to start.
That is A12 arrived at independently, nine times, by readers who had never seen
the ruling. The token diff (hand-written pages only, the `class-index.md` trap)
found five names that would have left the book, all put back into prose — and
writing the sentence that restored two of them introduced a count error the
session then had to correct, which is worth saying out loud: the A12 check is
not free. One literal trace heading renamed, both 1.21 blockquotes moved to the
foot, two openings varied off the word *You* (six of eight, the worst in the
book), eleven new H3s inside existing anchors, and three logged cuts. Part VII
3,207 → 3,478 lines. Twenty-two units appended to [pass5.md](pass5.md) (three
logged cuts, nine for pass 7, five for pass 8, one for pass 9, and the ruling
that closed the three-closers question); eleven entries struck and four
annotated; the session's entry in [pass9.md](pass9.md). All five gates green;
deployed. **What the session would tell the next one**: session F said a renamed
closer is still a closer and no tool sees it. The other half of that is here — an
*inbound link* into a closer is not visible either, because `check_links.py`
reports the anchor and the anchor is the whole section. Three links landed on
one anchor and meant three different answers inside it, and the only way to find
that out is to read the citing sentence at the other end. Run
`check_links.py --inbound` on every page of the part *before* deciding which
closers keep, and read what each citing sentence actually wanted.
