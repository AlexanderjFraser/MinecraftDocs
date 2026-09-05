# The plan — the passes

*Rewritten 2026-09-02 at the start of pass 3, 2026-09-03 at its close,
2026-09-05 at pass 4's close, and again the same evening by the planning
session that set the ten-pass plan. This is the document every session reads
first and ticks last. Each finished pass is archived whole in its own file —
[pass1.md](pass1.md), [pass2.md](pass2.md), [pass3.md](pass3.md),
[pass4.md](pass4.md): the charter, rulings, protocol, schedule and log, and
at the end of pass4.md the plan as it stood at pass 4's close. The queues:
[pass5.md](pass5.md), opened as the polish queue and now the queue passes
5–8 draw on, each entry taken by the pass its kind belongs to;
[pass9.md](pass9.md), where every pass-5-to-8 session lists the claims it
introduced; [pass3.md](pass3.md) §7, the coverage queue.*

## Where we are

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

**Pass 5 — the book — is running.** Its charter is below at the level of
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

## The passes

| pass | what | lens | status |
|---|---|---|---|
| **1 — rough draft** | every page drafted from the decompile, names verified | — | done — [pass1.md](pass1.md) |
| **2 — completeness and accuracy** | every claim adversarially fact-checked; gaps filled; pages split and added freely | the adversary with the source | done, 2026-09-01 — [pass2.md](pass2.md) |
| **3 — restructuring** | the site became a book: each part the shape of its system, each page one of eight shapes; the frame, the maps and the Reference tier redone; the lecture order drafted | the shape | done, 2026-09-03 — [pass3.md](pass3.md) |
| **4 — the second fact-check** | pass 2's protocol over everything pass 3 rewrote; the claims pass 3 introduced checked first | the adversary again | done, 2026-09-05 — [pass4.md](pass4.md) |
| **5 — the book** | across pages: one home per idea, the seams, the through-lines, the landing pages as the part's argument, the coverage question once per part, the last moves | the book as one thing | **running** — session A done 2026-09-05; charter below; queue [pass5.md](pass5.md) |
| **6 — the lecture** | one page at a time: the devices that became slots, the twin skeletons, section order, the cuts; a page that reads as one lecture's notes | the reader with only the page | after 5 |
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

## Pass 5 — the book (next)

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

### The jobs

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

## Pass 6 — the lecture

**Goal:** each page is one lecture's notes — in the shape of its story,
opening inside the scenario on a hook that holds, its trace the spine and
its figure the artefact, reading differently from its neighbours, speakable
in a sitting.

**The jobs:** the devices that became slots — the *Questions players ask*
closer on 69 of the 102 pages in five spellings (four parts use it on every
page; session P's rule of thumb, at most half a part, stands until a session
says why not), the literal `## The trace: …` heading on twenty pages, the
bold or dashed sentence that ends the opening paragraph on most of the
corpus, the *for a 1.21-era reader* blockquote as a fixed slot, and the
second person, which opens more than half the pages and is ratified or
reversed corpus-wide in session A, not page by page; the skeleton groups
session P listed, varied one of each; the section order, where a fact fix
left the exception before the rule or the concession inside the hook; the
cuts — the length bill pass 2 deferred and pass 3 recorded page by page,
with each drafter's own cheapest cut already logged and Parts IV and VII
fattest; the completeness lists for the four Reference catalogues; every
page-shape finding in [pass5.md](pass5.md). The agent is **a reader with
nothing but the page**, asked four questions — where did you get lost, what
did you have to read twice, what did the page assume you already knew, and
what did you skip — and the session decides. Each part session ends by
re-syncing the landing page's and `lectures.md`'s blurbs to the pages as
they now stand.

**Not:** facts; a figure beyond what a reshaped section needs; voice.

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
26.2` as a test rather than a claim. **As of 2026-09-05 the latest release
is still 26.2; 26.3 is at pre-release 2 (2026-09-04)** — checked against
Mojang's version manifest, not assumed. This pass triggers on a release and
runs once, in one session, between passes; a release that lands mid-pass
waits for the pass to close. It will most likely run first inside pass 5,
and again if 26.4 lands before pass 10.

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

## Session log — pass 5 onward

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
