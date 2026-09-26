# The plan — the passes

*Rewritten 2026-09-02 at the start of pass 3, 2026-09-03 at its close,
2026-09-05 at pass 4's close and again that evening by the planning session
that set the ten-pass plan, 2026-09-07 by the planning session between passes 5
and 6, 2026-09-14 by the one between passes 6 and 7, and 2026-09-26 by the one
that chartered pass 8 — the last pass — after the owner's read. This is the
document every session reads first and ticks last. Each finished pass is
archived whole: [pass1.md](pass1.md), [pass2.md](pass2.md), [pass3.md](pass3.md)
and [pass4.md](pass4.md) for the first four, and for passes 5, 6 and 7 the
brief's Part 5 — [pass5-brief.md](pass5-brief.md), [pass6-brief.md](pass6-brief.md),
[pass7-brief.md](pass7-brief.md) — each holding that pass's charter, its session
paragraphs and its log beside the brief, the runbook, session A's rulings and
the schedule. The queues: [pass5.md](pass5.md), opened as the polish queue on
2026-09-02, drawn on by passes 5, 6 and 7 by kind, and **closed by pass 8** —
every open unit settled or ruled by its close; [pass9.md](pass9.md), the ledger
where every session since pass 5 has listed the claims it introduced and the
corrections it made, which pass 8 checks and strikes; [pass3.md](pass3.md) §7,
the coverage queue, which seeds the second edition and is the one queue that
stays open.*

## Where we are

**2026-09-26.** Seven passes are done, bar one session of the seventh (K,
Part XI's figures, which runs inside pass 8), and the plan below has changed
shape twice this month. On 2026-09-16 the owner read the site as *better than
a free wiki, not yet a textbook* and judged the process, not the form, to be
the ceiling: linear passes, each finding the errors at the edges of the last.
Their decision was to collapse the three remaining passes into one that leaves
minecraftdocs.dev stable, then to rebuild the production process from first
principles on a new subject (`D:\DjangoDocs`; its `docs/brief.md` holds the
reasoning) and return here with what it learned. On 2026-09-26 they said what
that one pass is: **the final fact-check, using the ledger every session since
pass 5 kept for it, and a final polish over the exact wording**, planned to
make the book as good as this process can make it.

The same day, two facts moved. **Minecraft 26.3 shipped on 2026-09-15**, so
every page's *verified against 26.2* has been untrue for eleven days; the
planning session staged the 26.3 decompile beside the old one
(`tools/version_pass.py`, one script now) and measured it — 517 names on 65
pages no longer resolve, and three systems changed shape (the GPU abstraction
moved to `com/mojang/renderpearl`, world generation's surface rules and carvers
and two chunk statuses are gone, `level/storage` was reworked) — so the version
pass is pass 8's first two sessions rather than a re-read between passes. And
the site became readable by agents that morning: every page at its `.md`
address, every built `<head>` carrying its own title, description, canonical
and structured data (`tools/page_meta.py`, `tools/md_twins.py`).

**Pass 8 — the release — is current**, chartered in [pass8-brief.md](pass8-brief.md):
nineteen sessions, V1 and V2 the version, A the standard, B to N the parts, K
Part XI's figures under pass 7's runbook, O the Reference and the frame, P the
second reading of every sentence the pass changed, Q the release and the tag
`release-26.3`. None has run. After it, nothing more is done here except a
version pass when the owner asks for one and the corrections readers file,
until the rebuilt process returns.

**What the seven passes found, one line each**, because it is what a
newcomer needs to know about this book. The rough draft (1) was written from
the decompile per page, and the first fact-check (2) found at least one wrong
claim on every page — the errors lived in the confident sentences. The
restructuring (3) made the site a book of thirteen parts and eight page
shapes, and the second fact-check (4) found 836 errors, most of them in
sentences the restructuring had written: every pass that touches a sentence
puts errors in. Reading *across* pages (5) found 171 more, half of them one
page contradicting another. Reading each page *down* as one lecture's notes,
by a reader with nothing but the page (6), found about two hundred, almost all
**a sentence that disagrees with the text beside it** — the class no
fact-check looks for. Looking at every figure *rendered* (7), for the first
time, found about 180 facts wrong inside figures on a corpus fact-checked
twice, most of them one shape — a message labelled with the caller's method
and drawn arriving at the callee — which a gate now catches mechanically. Each
pass's finding was unpredicted by the pass before it; that is the owner's
diagnosis of the process, and the reason the process is being rebuilt
elsewhere before it is used again.

## The passes

| pass | what | lens | status |
|---|---|---|---|
| **1 — rough draft** | every page drafted from the decompile, names verified | — | done — [pass1.md](pass1.md) |
| **2 — completeness and accuracy** | every claim adversarially fact-checked; gaps filled; pages split and added freely | the adversary with the source | done, 2026-09-01 — [pass2.md](pass2.md) |
| **3 — restructuring** | the site became a book: each part the shape of its system, each page one of eight shapes; the frame, the maps and the Reference tier redone; the lecture order drafted | the shape | done, 2026-09-03 — [pass3.md](pass3.md) |
| **4 — the second fact-check** | pass 2's protocol over everything pass 3 rewrote; the claims pass 3 introduced checked first | the adversary again | done, 2026-09-05 — [pass4.md](pass4.md) |
| **5 — the book** | across pages: one home per idea, the seams, the through-lines, the landing pages as the part's argument, the coverage question once per part, the last moves | the book as one thing | done, 2026-09-07 — record [pass5-brief.md](pass5-brief.md); queue [pass5.md](pass5.md) |
| **6 — the lecture** | one page at a time: the devices that became slots, the twin skeletons, section order, the cuts, the landing pages' seventh section; a page that reads as one lecture's notes | the reader with only the page | done, 2026-09-14, sessions A–N — record [pass6-brief.md](pass6-brief.md) |
| **7 — the figures** | every figure as rendered, beside its section: is it true, is it needed, does it show the thing, can it be read; the gate over names inside mermaid blocks | the picture | done, 2026-09-16, sessions A–J and L–O — record [pass7-brief.md](pass7-brief.md); **K (Part XI) runs inside pass 8** |
| **8 — the release** | the version (26.3); the third fact-check, over the ledger every session since pass 5 kept; the polish over the exact wording, after the check, with every changed sentence read a second time; Part XI's figures; the frame, the queues closed, the tag | the adversary, then the sentence, then a reader who changed nothing | **current** — planned 2026-09-26; brief, agent brief, runbook, the standard for session A and the schedule with each session's status [pass8-brief.md](pass8-brief.md); ledger [pass9.md](pass9.md); queue [pass5.md](pass5.md), closed by the close |

Passes 8, 9 and 10 of the 2026-09-05 plan — the voice, the third fact-check,
the last polish — are this one pass; their charters are archived in the
brief's Part 7. Beside the passes, unnumbered: **the version pass**, chartered
below and now two sessions of pass 8; and **the owner's read**, which runs
whenever the owner likes and whose questions the current pass answers.

The rules stand for every pass: names never code · how the system works,
not how the code reads · newest version only · trace-driven · claims come
from the decompile, never from model memory of an earlier version · the six
gates — `python tools/verify_names.py`, `node tools/check_mermaid.js`,
`python tools/check_lanes.py --strict`, `python tools/check_figure_names.py
--strict`, `python tools/check_deps.py`, `python tools/check_links.py` —
clean before every commit that touches a page, and `tools/deploy.sh` refuses
to publish on any failure. The version the tools read is one constant,
`tools/mc_version.py`. Reasoning over sensing over measuring: no count in a
queue is a target, and the owner judges what lands.

## Why this order

- **Structure before words.** Pass 3 rewrote the prose of nearly every page
  to change its shape, and pass 4 then found 836 errors, most of them in
  sentences the restructuring had written. Polish done before a restructure
  is paid for twice: its sentences are rewritten, and the errors of the
  rewrite have to be found anyway. So the two structural passes (5, 6) came
  first, the figures (7) after them, and the words last.
- **Across before within.** Pass 5 decided what each page owns, what moves
  and what is said once, so that pass 6's work on a page was not undone by a
  move. The summarisers — the thirteen landing pages, `lectures.md`, the
  glossary — are the exception that proves it: they drift every time their
  pages change, so pass 5 gave them their role and every later pass re-syncs
  them at the end of its part session, and pass 8 reads them last.
- **The figures got a pass of their own** because the diagram is the
  lecture's artefact (rule 4) and nobody had looked at one *rendered*: every
  check before it was parse and arrow-by-arrow truth, not shape or
  legibility. That pass also built the gate over names inside mermaid
  blocks, so that pass 8 checks figures under a gate.
- **The check before the polish, and the check of the polish.** The
  2026-09-05 plan mirrored two polishes on two fact-checks — the heavy one
  before the check, the light one after. Collapsed into one pass, the order
  inside each part session is the same argument at a smaller scale: the facts
  are settled first, so the polish works on true sentences and smooths the
  corrections; the polish is constrained to the sentence (no heading, no
  paragraph, no list); and every sentence it changed is read again by a
  session that changed none of them, from git, before the release. That last
  step is what passes 3 to 7 never had, and it is the price of polishing in
  the last pass.
- **One lens per pass.** A session briefed to fix everything fixes what it
  expects to find. Pass 3's sessions were told to reshape and did; the
  errors went into what they were not told to look at. A pass with one
  question finds what the previous pass could not see — which is also why
  pass 8's agent is told to judge nothing about the wording, and its polish
  step is told to change nothing about the facts.

## The rhythm of a pass

Every pass has run the same way, because it worked the first time and every
time since:

1. **A planning session** (Fable, between passes): reads the queue, builds
   the pass's tools and writes its brief and runbook — one prompt file per
   page, so the sessions do no planning of their own — and measures what the
   queue actually contains before the first session spends anything on it.
2. **Session A — the standard**: the frame, the exemplar, the rulings the
   part sessions will apply (pass 3's session A wrote `TEMPLATE.md` from two
   pilots; pass 4's did the frame and made `check_deps.py` a gate; pass 7's
   adopted the figure theme; pass 8's rules on the voice from counts).
3. **Sessions B–N — the parts**, in sidebar order, one part per session on
   Opus: read the charter, this pass's rulings and every queue entry that
   names the part; read the part end to end in watching order before
   changing anything; one background agent per page (never per part — a
   part-wide brief hit the spend limit in pass 3); the session does its own
   work while they run, then re-derives every finding it acts on; the six
   gates; commit `pass N, session X — Part M: <summary>`; deploy; log.
4. **Session O — the close**: the frame against the finished parts, the
   pass's own work audited (a strike is a claim), the pass archived whole
   into its file, the next pass's charter detail written, and a verdict on
   whether the pass was productive — the owner's test for spending more.
   Pass 8 has no next pass, so its close is two sessions: the second reading
   (P) and the release (Q).

Standing rules for passes 5 to 8, the restructuring and refining passes:

- **A fact is not changed without the decompile open.** The reader agents of
  passes 5, 6 and 7 had no source in their briefs — an agent given the
  source re-litigates instead of reading; pass 8's agents are fact-checkers
  and have it, as pass 4's did. A session that finds a real error stops,
  re-derives it against the decompile itself, fixes it, and logs the
  correction in [pass9.md](pass9.md) the way a pass-4 session logged one:
  what the page said, what the decompile says, file and line.
- **Every claim a session introduces goes to [pass9.md](pass9.md)** — a
  hook, a moved paragraph, a redrawn arrow, a re-scoped count, a landing
  page's new argument, and in pass 8 a polished sentence whose meaning could
  have moved. This is the rule pass 3 kept for pass 4, and it is what made
  pass 4 checkable. A session that cannot say what it changed on purpose has
  not finished.
- **Nothing is dropped except by moving it or logging the cut** with the
  reason (the budget rule in `TEMPLATE.md`); a moved page keeps its URL
  through `book.toml`'s redirects; after pass 5 no page moves again.
- **Every queue entry is checked against the page before it is acted on**:
  an entry that is already overtaken is struck with a word saying so (pass
  4's rule — an item handed forward is checked, not applied). Pass 8 strikes
  every entry in both queues by its close.
- **The gates stand and grow only by truth**: the link checker joined them
  in pass 5's planning session because it was clean on its first run and a
  link resolving is a fact; the figure-name gate joined at pass 7's close;
  nothing that measures prose is a gate, and `pass8_voice.py` is not one.
- **Commit your own files by name; never `add -A`** while another session
  may be open (session I of pass 3 swept another session's half-written
  change into an unrelated commit).
- **The version pass interrupts nothing**: a release that lands mid-pass
  waits for the pass to close — except at the very end, where ruling R6 makes
  the release wait for the version.

---
## Pass 8 — the release (current)

**Planned 2026-09-26**, twice: in the morning as *the release* (the third
fact-check and the tag, the voice pass dropped), and in the afternoon, after
the owner's instruction, as the final fact-check **and** the final polish over
the exact wording. The charter, the agent brief, the runbook, the standard as
recommendations with numbers, the rulings and the schedule are
[pass8-brief.md](pass8-brief.md); this section is the summary a session reads
before it.

**What it does, in order of weight.** (0) **The version**: 26.3 shipped
2026-09-15; the tree is staged at `reference/26.3/` and the tools read one
constant; sessions V1 (mechanical — the flip, the atlas's mapping given
`renderpearl`, the regenerated views diffed, every rename resolved, the header
line on every page) and V2 (the five pages whose systems changed shape,
rewritten in the smallest true rewrite, with what the part session must re-read
written into the ledger). (1) **The third fact-check**: pass 4's protocol —
one adversarial agent per page with the decompile, given the ledger's entries
for the page as its opening checklist (1,333 entries; `tools/pass8_queue.py`
routes them by page and part) — while the session reads the whole part into
context and lists every sentence that disagrees with another, the class
passes 5 and 6 found most of. (2) **The polish**, after the check on each
part, under rulings session A makes from `tools/pass8_voice.py`'s counts:
the tics, the hedges without a population, the corrections written as
corrections, the two spellings and two senses of one word, the possessive on a
link, the captions' and labels' register, the blockquote's form — the smallest
edit, never a heading, never a paragraph. (3) **Part XI's figures**, pass 7's
session K, under pass 7's runbook. (4) **The release**: the frame true of every
gate, the pass numbers swept, the lecture order confirmed, the version line
against the manifest, the queues closed (`pass8_queue.py --unstruck` and
`pass5_queue.py --summary` at zero), the maintenance note, the tag
`release-26.3`, the pass archived.

**New in the method**: the whole-part read; the ledger checked against
itself; the polish after the check and **every changed sentence read a second
time** by session P from git (`tools/pass8_diff.py`); the version as one
constant and one script; the queues closed rather than carried.

**Dropped**: pass 10's last cuts and the 215 long sections with no figure
(the rebuilt process's); anything new (a gap goes to [pass3.md](pass3.md) §7
and is declared where the book says what it skips). The charters this pass
replaces are archived in the brief's Part 7.

**The owner's part**: confirm the lecture order before session Q; decide after
V1 whether V2's five rewrites are written in this pass (the brief assumes
yes); the dashboards.

## The version pass — rule 3's re-read (chartered; 26.3 is due and runs first)

Rule 3 says newest version only, and every page carries `verified against
<version>` as a test rather than a claim. **As of 2026-09-26 the latest
release is 26.3 (2026-09-15); 26.4-snapshot-1 exists (2026-09-22)** — checked
against Mojang's manifest by `python tools/version_pass.py --latest`, which
is what any session runs to ask. The cadence is quarterly (26.1 on
2026-03-24, 26.2 on 2026-06-16, 26.3 on 2026-09-15), so 26.4 is unlikely
before December. The pass triggers on a release and runs once, between
passes — except now, where it is pass 8's sessions V1 and V2, because a last
pass verified against a superseded version would leave the site false on the
day it was called stable. Its steps, each now a command:

1. **Stage** — `python tools/version_pass.py <version>`: Mojang's manifest to
   the version JSON to the client and server jars; the client's classes
   decompiled with the Vineflower bundled in the sibling project's McDeob jar
   (the jar ships with Mojang's names since 26.x, so no mapping step); `data/`
   whole, `assets/` without textures, `version.json`, `server-classes.txt`
   from the server bundler's inner jar; the libraries at the versions the
   JSON pins, through `tools/fetch_libs.sh`. Into `reference/<version>/`,
   beside the old tree, gitignored. About ten minutes; done for 26.3.
2. **Measure** — `python tools/version_pass.py <version> --check`: the name
   gate and the figure gate against the new tree, the failures by page and
   part. **That is the mechanical half of the pass**: every name that stops
   resolving is a rename or a removal, and the failures name the pages that
   need re-reading. 26.3: 517 names on 65 pages, 32 in figures.
3. **Flip** — `git tag pass-8-start` (this time), then
   `python tools/version_pass.py <version> --flip`, which rewrites the one
   constant in `tools/mc_version.py`; every tool reads it. `map_source.py`'s
   `PARTS` mapping is read against the new packages (26.3 adds
   `com/mojang/renderpearl`, `world/level/blockscan`, `world/item/slot`,
   `world/attribute/modifier`).
4. **Regenerate and diff** — `map_source.py`, `gen_reference.py all`,
   `pass5_coverage.py --write`, `check_deps.py --write-figure`, and the diff
   of `src/generated/` and the generated Reference views *read*: a population
   that changed is a page that changed.
5. **Re-read** — the pages the gates named, with the decompile open: a rename
   in the smallest edit; a removed name replaced by what does its work or the
   sentence cut; a system that changed shape rewritten in the smallest true
   rewrite (V2's job); `claims.py --all --counts` over the touched pages,
   because a count whose population moved is wrong now. Every change logged
   in the ledger.
6. **The header line** on every page, `CLAUDE.md`, `README.md`, the
   introduction, `book.toml`, the issue template's placeholder,
   `fetch_libs.sh`'s defaults; the 1.21 blockquotes gain the new drift where a
   reader would hunt for the old name (the brief's V13); `naming-drift` gains
   the rows. The gates; deploy.

A system that changed shape rather than names is also a structural finding
for [pass3.md](pass3.md) §7 where the book's existing page cannot carry it.
**After the release**, the version pass runs when the owner asks for it, and
not otherwise; until then the site says what version it was verified against
and when, which is a dated fact rather than a live claim, and the maintenance
note session Q writes says so.

## The owner's read

Unnumbered and parallel: the owner reads a part with the decompile open
whenever they like, and leaves questions **in the page** as `<!-- Q: … -->`
comments. The next session that touches the page answers each question in the
prose (if the owner had to ask, the page was wrong or missing it) and removes
the comment; every part session greps its part for them at the start. The
owner confirms or reorders `lectures.md` before session Q, so that the release
carries the confirmed order. Nothing is recorded that the owner has not
understood; recording is after the release.

## Risks

- **A pass that touches sentences puts errors back** — pass 3 did, by the
  hundred, and pass 8's polish touches thousands. The answer is the order
  (facts first), the constraint (the sentence, never the paragraph), the rule
  that a session lists what it changed on purpose, and session P reading every
  changed sentence from git.
- **A pass that finds nothing.** A lens that returns clean is a lens too
  wide or an agent that liked the page. Brief per page, evidence for every
  finding, and the close says honestly whether the pass earned its cost.
- **The version is bigger than a re-read.** 26.3 moved 788 classes and
  changed the shape of three systems; V2's five rewrites are the largest
  unchecked writing in the pass, which is why their part sessions (D, L, M)
  run after them with fresh agents and V2's ledger entries first.
- **A release lands mid-pass.** 26.4 is unlikely before December; if it
  ships before session Q, a version session runs first and Q waits (R6).
- **The tools.** Fifteen bugs in pass 4, six of them published; eleven gate
  blindnesses in pass 7; the 26.3 staging found one more at once (a new
  top-level package that no part's mapping names). Suspect the tool first, and
  every tool built since pass 5 ships with a probe that proves it fails on the
  construct it should — the four built for this pass do.
- **Cost.** Nineteen sessions, three passes' worth of work in one; the
  planning session's estimate, and the owner's to cut (the brief says which
  sessions can merge). After it, nothing until the process returns.

## Session log — pass 8 onward

*(newest last; pass 7's log and its session paragraphs are in
[pass7-brief.md](pass7-brief.md) Part 5, pass 6's in
[pass6-brief.md](pass6-brief.md) Part 5, pass 5's in
[pass5-brief.md](pass5-brief.md) Part 5, and pass 4's at the end of
[pass4.md](pass4.md))*

- **2026-09-26, planning session, morning (Fable, after the owner's post-pass-7
  read).** No page's prose touched. **The site made readable by agents**: every
  page published as its markdown twin (`tools/md_twins.py`, `src/_headers`
  serving `text/markdown` cross-origin, `llms.txt` linking the twins) and every
  built `<head>` rewritten per page — the page's own title and part, a
  description from its scenario line (every page had shared `book.toml`'s), a
  canonical at the clean URL, the markdown alternate, Open Graph with
  `src/og.png`, JSON-LD (`tools/page_meta.py`, a gate in `deploy.sh`). The edge
  probed with nine AI user agents: none blocked. A correction issue template
  with an evidence rule. **Passes 8–10 collapsed into pass 8, the release**, its
  queue tool `tools/pass8_queue.py`, pass 7's session K carried into it.
  **`D:\DjangoDocs` seeded** with the reasoning of the 2026-09-16 conversation
  and the memories that transfer. Deployed.

- **2026-09-26, planning session, afternoon (Fable).** No page's prose touched;
  nothing deployed. The owner's instruction reversed the morning's one dropped
  job: pass 8 is the final fact-check **and** a final polish over the exact
  wording, planned for the best book this process can make. **The version
  found due**: Mojang's manifest says 26.3 shipped 2026-09-15, so the tree was
  staged the same afternoon with a new script (`tools/version_pass.py`:
  manifest, jars, Vineflower, data, assets, `server-classes.txt`, the
  libraries at 26.3's pins — authlib 10.0.77, Brigadier 1.3.11) and measured:
  7,301 classes, 517 names on 65 pages unresolved, 32 in figures, `renderpearl`
  new and unmapped, `levelgen` and `level/storage` reworked. **The version made
  one constant** (`tools/mc_version.py`; eight tools that carried their own
  copy now read it; every gate green after the change). **Four tools built,
  each with a probe**: `pass8_queue.py` rewritten to read the page forms the
  ledger actually uses (1,333 entries routed where the morning's read 1,064,
  page-less notes routed to their session's part, `--unstruck` for R3, `--pass
  8` for the second reading); `pass8_voice.py` (the tics, hedges, corrections-
  as-corrections, dead-constant asides, possessive links, the number device,
  openings on *you*, long sentences, counts that rot, and the ambiguous terms,
  per page and per part, plus `--terms` for glossary headwords spelled two
  ways — 26); `pass8_prompts.py` (one prompt per page: the agent brief, the
  page's ledger entries, its captions, the gate's notes, its claims and its
  arrows; and a session file: the queue units of every kind, the voice measure,
  the inbound links); `pass8_diff.py` (every sentence changed since a tag, from
  git, for session P). **The brief rewritten** — Part 2 the agent brief (pass
  4's, with the ledger as the checklist and the page-against-itself section),
  Part 3 the runbook (check, then polish, then re-derive, then strike), Part 4
  the standard as seventeen recommendations with counts, Part 5 eleven
  rulings, Part 6 nineteen sessions (V1, V2, A–Q) with what the tools measured.
  **Pass 7 archived** whole into [pass7-brief.md](pass7-brief.md) Part 5; this
  file, `CLAUDE.md`, `README.md`, the heads of [pass9.md](pass9.md) and
  [pass5.md](pass5.md), and the memory brought current — the memory's plan
  entry cut from what the repo already records to what it cannot derive.
