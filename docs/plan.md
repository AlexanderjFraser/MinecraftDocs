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

**Pass 5 — the book — is next.** Its charter is below at the level of
intent. Its detailed brief, its tools and its session runbook are written by
the planning session before it starts, the way the 2026-09-03 planning
session built pass 4's ([pass4-brief.md](pass4-brief.md) is the model).

## The passes

| pass | what | lens | status |
|---|---|---|---|
| **1 — rough draft** | every page drafted from the decompile, names verified | — | done — [pass1.md](pass1.md) |
| **2 — completeness and accuracy** | every claim adversarially fact-checked; gaps filled; pages split and added freely | the adversary with the source | done, 2026-09-01 — [pass2.md](pass2.md) |
| **3 — restructuring** | the site became a book: each part the shape of its system, each page one of eight shapes; the frame, the maps and the Reference tier redone; the lecture order drafted | the shape | done, 2026-09-03 — [pass3.md](pass3.md) |
| **4 — the second fact-check** | pass 2's protocol over everything pass 3 rewrote; the claims pass 3 introduced checked first | the adversary again | done, 2026-09-05 — [pass4.md](pass4.md) |
| **5 — the book** | across pages: one home per idea, the seams, the through-lines, the landing pages as the part's argument, the coverage question once per part, the last moves | the book as one thing | **next** — charter below; queue [pass5.md](pass5.md) |
| **6 — the lecture** | one page at a time: the devices that became slots, the twin skeletons, section order, the cuts; a page that reads as one lecture's notes | the reader with only the page | after 5 |
| **7 — the figures** | every figure as rendered, beside its section: the true shape, legibility, lanes, labels; the fifth gate, names inside mermaid blocks | the picture | after 6 |
| **8 — the voice** | one voice and one vocabulary: the exemplar, the tics, the terminology sweep, the ambiguous counts, the wording debt | the sentence | after 7 |
| **9 — the third fact-check** | pass 4's protocol plus what pass 4 learned; the claims passes 5–8 introduced first; every fix checked as a claim | the adversary, once more | after 8 — queue [pass9.md](pass9.md) |
| **10 — the last polish** | pass 9's debt, the frame against the finished book, links, the last cuts, the release | the reader, once more | after 9; then the site is finished |

Beside the passes, unnumbered: **the version pass**, chartered below and
run once between passes on each release; and **the owner's read**, which
runs whenever the owner likes and whose questions the current pass answers.

The rules stand for every pass: names never code · how the system works,
not how the code reads · newest version only (26.2) · trace-driven · claims
come from the decompile, never from model memory of 1.21 · the four gates —
`python tools/verify_names.py`, `node tools/check_mermaid.js`,
`python tools/check_lanes.py --strict`, `python tools/check_deps.py` — clean
before every commit that touches a page, and `tools/deploy.sh` refuses to
publish on any failure. Reasoning over sensing over measuring: no count in a
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
- **The four gates stand and grow only by truth**: pass 7 adds the fifth
  (names inside mermaid blocks); nothing that measures prose is a gate.
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
7. **Is every page a lecture?** The book says one page per lecture and has
   102 pages. The owner decides whether the series records all of them or a
   tier of them; pass 5 proposes the tiering if asked (a page can be the
   notes a lecture links to without being an episode), and the site is
   complete either way.

**What pass 5 does not do:** it does not reshape a page's internal skeleton
or vary a device (6); it does not redraw a figure for legibility (7); it
does not hunt a tic or settle a count's wording (8); it changes no fact
without the decompile open (the standing rule).

**Sessions.** A — the standard: the landing-page role written into
`TEMPLATE.md`, the through-lines list, the duplication finder's corpus-wide
report routed to parts, the exemplar landing page, the frame's own seams.
B–N — the parts, one session each, reading the part end to end and every
page it links into. O — the close: the frame and the summarisers against
the finished parts, the lecture map re-derived, the glossary's owner links,
the moves' redirects, [pass9.md](pass9.md)'s entries checked for shape, and
pass 6's charter detail.

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
tick-boundary bars. **The fifth gate:** names inside mermaid blocks — 453
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
introduction's *verified* paragraph made true of three checks; the release —
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
