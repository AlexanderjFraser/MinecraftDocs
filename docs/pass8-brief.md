# Pass 8 — the release (passes 8, 9 and 10 in one)

*Planned 2026-09-26 by the session that followed the owner's post-pass-7 read.
This is the last pass before the site is left stable: the third fact-check over
everything passes 5 to 7 introduced, the one session of pass 7 that never ran,
and the release. The voice pass is dropped on purpose. Part 1 is the charter,
Part 2 the runbook a session follows, Part 3 the rulings, Part 4 the schedule
with a status column, which is where the owner sees what is done.*

## Part 1 — the charter

**Why one pass.** On 2026-09-16 the owner read the site as better than a free
wiki and not yet a textbook, and decided the *process* was the ceiling: linear
passes that each found the errors at the edges of the last one. The process is
being rebuilt from first principles on a new subject (the sibling repository
`DjangoDocs`, whose `docs/brief.md` records the reasoning). Until that returns
here, minecraftdocs.dev is to be **stable**: every claim checked, the frame
truthful, a tagged release, and nothing half-done. Three passes were planned
for that; one is enough if it does only what stability needs.

**What stability needs.** Three things, in order of weight.

1. **The unchecked claims.** [pass9.md](pass9.md) is the ledger where every
   session of passes 5, 6 and 7 wrote the claims it introduced and the
   corrections it made, so a later fact-check would read them first. Nobody
   has. `python tools/pass8_queue.py` routes its 1,064 bullets: **866 name a
   page** (117 pages), 455 are session-level notes and standing items, and
   seven name a package rather than a page. Passes 2 and 4 found at least one
   wrong claim on every page they checked; there is no reason to think the
   writing sessions of 5 to 7 were different, and pass 6's own finding — a
   sentence that disagrees with the text beside it — is the class a writing
   session cannot see in its own work.
2. **Part XI's figures.** Pass 7's session K, Part XI · Rendering, never ran
   (the close ran before it at the owner's request and handed K the part).
   Part XI's figures are the corpus's worst by the render — the planning
   session's own count, [pass7-brief.md](pass7-brief.md) Part 4 — and the
   only part whose figures were never read against their sections. It is
   session I here, and it runs pass 7's runbook, not this one's.
3. **The release.** Pass 10's jobs that are about truth rather than polish:
   the introduction's *verified* paragraph made true of every gate, including
   the two added on 2026-09-26; `README.md`, `CLAUDE.md`, `TEMPLATE.md` and the
   frame pages swept for pass numbers promised as futures; the lecture order
   confirmed by the owner; the version line checked against Mojang's manifest;
   a git tag; and a *maintenance* note that says what happens while nobody is
   working here — what runs, what a new release triggers, how a reader's
   correction arrives.

**What is dropped, and why.** Pass 8's voice work (the tics, the terminology
sweep, the 203 captions read as one set, the fifty-odd ambiguous counts) and
pass 10's last cuts. The rebuilt process is meant to *produce* the voice; a
voice pass over prose that process will rewrite is spent twice. The wording
debt stays where it is, in [pass5.md](pass5.md), as an archive a return can
draw on, and nothing in it is struck by this pass. A structural finding goes
to the same place. **Pass 8 adds nothing**: a gap goes to [pass3.md](pass3.md)
§7, the coverage queue, which seeds the second edition.

**What is new in the method.** Two things the earlier passes did not have.
The corpus's system pages are about 460k tokens and a part about 35k, so **a
session reads its whole part into context before it checks a single entry**,
and lists every place one page of the part disagrees with another — the error
class passes 5 and 6 found most of, and the one a page-at-a-time check cannot
find. And the third fact-check checks the ledger *against itself*: a pass-7
correction that overturned a pass-5 claim is one check, at the later entry,
which `pass8_queue.py --part` shows in order.

## Part 2 — the runbook

A session takes one part (Part 4 says which), on Opus, with the decompile at
`reference/26.2/` open. In order:

1. **Read the part whole.** Every page of the part, landing page first, in one
   read. Before opening the queue, write down every sentence that disagrees
   with another sentence in the part — a count, a name, an ordering, a
   direction, an owner — and every place a page contradicts its own figure or
   table. These are checked first, because they are the errors the writing
   sessions could not see.
2. **Walk the queue.** `python tools/pass8_queue.py --part <numeral>` prints
   the part's entries by page, oldest pass first, with the session that wrote
   each. Pass 4's protocol applies to every entry ([pass4-brief.md](pass4-brief.md),
   and the eight steps of pass 9's charter in [plan.md](plan.md) as it stood
   before this pass, archived in Part 5 below): the figure against the section
   under it before either against the source; illustrations — tables, one-line
   summaries, closers, asides, the landing page — before mechanisms; a count
   checked as a population, never as a row; a name checked as `Class.member`.
   An entry that quotes a claim is re-derived from the decompile, not re-read
   for plausibility. An entry that records a correction is checked as a claim:
   the fix is what the decompile says, and the correction did not break the
   sentence beside it.
3. **Fix with the decompile open.** A wrong claim is corrected on the page, in
   the smallest edit that makes it true; nothing else on the page changes.
   No caption is rewritten for register, no list re-budgeted, no figure
   redrawn unless an arrow is false. A false arrow is redrawn under pass 7's
   standard ([pass7-brief.md](pass7-brief.md) Part 3 and `TEMPLATE.md`
   *Figures*) and rendered (`node tools/render_figures.js --page …`) before
   it is committed.
4. **Strike the ledger.** This pass is the fact-check the ledger was kept
   for, so it strikes: an entry checked and found right is struck through
   (`~~…~~`); an entry found wrong is struck and followed by a correction line
   in this pass's own section of [pass9.md](pass9.md), in the form pass 7's
   close prescribed (`page`:line — what it said — what is true —
   `path/File.java`:line). A session-level note that needed no check is struck
   with *(no claim)*. When the pass closes, nothing in the file is unstruck.
5. **The gates, then commit by name.** `verify_names.py`, `check_mermaid.js`,
   `check_lanes.py --strict`, `check_figure_names.py --strict`,
   `check_links.py`; `check_deps.py` if a landing page moved; every changed
   page, the ledger and the brief, staged by name (two sessions are often
   open). Deploy with `tools/deploy.sh`, which also refuses a page without its
   own description or markdown twin.
6. **The session paragraph.** Under Part 4: entries checked, entries found
   wrong, corrections made (with the three worst quoted), what the whole-part
   read found that the queue did not, and anything left for the release
   session. The status column flips to *done*.

**Reader agents** are not used in this pass, except in session I, which runs
pass 7's viewer brief over Part XI. The checker is the session itself, with
the decompile; a second reading of every correction before it lands is step 3
of pass 9's old charter and is kept: the session re-derives each of its own
fixes once, from the file, before the commit.

## Part 3 — the rulings

- **R1 · Truth over everything.** A change in this pass is one of: a false
  claim made true, a false arrow redrawn, a frame page made accurate, a
  ledger entry struck. Anything else is out of scope, however small.
- **R2 · The whole-part read is not optional.** It is step 1 of every part
  session and its findings are logged even when the queue is empty for the
  page, because that is where passes 5 and 6 found half their corrections.
- **R3 · The ledger closes on itself.** Every one of the 1,064 entries is
  struck by the close, each with its verdict, and the pass's own corrections
  are listed in the same file under its own heading, so that a return to
  this site reads one file to know what was checked and by whom.
- **R4 · A correction is a claim.** Re-derived once more from the file before
  commit, by the session that made it. The close audits a sample of thirty.
- **R5 · No pass number is a promise.** After the release, no published page,
  `README.md`, `CLAUDE.md` or `TEMPLATE.md` names a pass as a future. The
  passes are history, recorded in `docs/`.
- **R6 · The version line is a test.** The release states the version the
  site is verified against, checked that day against Mojang's version
  manifest; if a release has landed, the version pass ([plan.md](plan.md))
  runs first and the release waits for it.
- **R7 · A reader's correction has an evidence rule.** The issue template
  (`.github/ISSUE_TEMPLATE/correction.yml`) asks for the page, the sentence,
  what the decompile says and where; a report without a location is answered
  with a request for one, not investigated.

## Part 4 — the schedule

The queue numbers are `python tools/pass8_queue.py` on 2026-09-26. Sessions
B to L take the parts in sidebar order; each is one context window. Session
I carries pass 7's session K in addition to its queue, and is the longest.

| session | scope | queue entries | pages | status |
|---|---|---:|---:|---|
| A | rulings rehearsed on Parts I, II and the Maps; the 455 session-level notes triaged (struck as *(no claim)* or routed to a page); the seven package names resolved; pass 7 session O's audit of the ledger's shape read and its workarounds applied | 52 | 14 | not started |
| B | III · The server | 68 | 5 | not started |
| C | IV · The world | 76 | 10 | not started |
| D | V · Blocks and VI · Entities | 97 | 16 | not started |
| E | VII · Items and inventories | 66 | 8 | not started |
| F | VIII · The player | 72 | 7 | not started |
| G | IX · Networking | 67 | 5 | not started |
| H | X · The client | 114 | 12 | not started |
| I | XI · Rendering — **pass 7's session K first** (its runbook, its viewer brief, its gate), then this pass's queue | 79 | 11 | not started |
| J | XII · World generation | 61 | 10 | not started |
| K | XIII · Commands and data packs | 69 | 9 | not started |
| L | Reference and the frame (introduction, lecture map, the maps' and Reference's front pages) against the finished book | 45 | 10 | not started |
| M | the release: the introduction's *verified* paragraph true of every gate; the pass-number sweep (R5); the version line against the manifest (R6); the lecture order confirmed by the owner; the maintenance note written into `README.md` and [plan.md](plan.md); the close's audit of thirty corrections (R4); every ledger entry struck (R3); the tag `release-26.2`; deploy | — | — | not started |

**The owner's part.** Two things only the owner does: confirm the lecture
order in `src/lectures.md` before session M (a read of the lecture map and a
yes, or a reordering), and the dashboard items the 2026-09-26 session listed
(Search Console, the analytics permission, the Pages metrics toggle), which
are not this pass's but are what makes the stable site observable.

## Part 5 — what this pass replaces

The charters of passes 8, 9 and 10 as [plan.md](plan.md) carried them until
2026-09-26, kept here because Part 2 cites pass 9's steps and a return may
want pass 8's list of the voice's tics.

### Pass 8 — the voice (as chartered; dropped)

Goal: one voice, one vocabulary, no tics, and every number says what it
counts. The jobs: the exemplar page and the voice note; the tics — "not X but
Y", the named-qualifier hedge, the dead-constant aside, the em-dash chain, the
correction written in the voice of a correction, *record* against *extract*,
the three words for an update channel's direction; the terminology sweep with
the glossary as the checklist; the fifty-odd counts whose population admits
two readings; the two rules for the word *classes*; how data keys are typeset;
the wording debt per part in [pass5.md](pass5.md); the register of the 1.21
blockquote; the 203 captions read as one set (`python tools/pass7/captions.py`);
69 figure labels on 48 figures that are still sentences; the bare-verb message
heads; thirteen voice entries from pass 7's part sessions.

### Pass 9 — the third fact-check (as chartered; this pass's sessions A to L)

1. pass9.md first — the claims passes 5 to 8 introduced, and their
   corrections confirmed as fixes rather than re-litigated as originals.
2. The illustrations before the mechanisms: tables, one-line summaries, Q&A
   answers, asides, landing pages, the glossary.
3. A fix is a claim: every correction re-derived by a second reading before
   it lands, and the close audits the pass's own strikes and corrections.
4. The figure against the section under it before either against the source.
5. Populations, not rows, for every generated page; call sites, not lines,
   for every count; the population named for every absolute.
6. The names inside figures are under the gate; the ambiguous simple names
   settled or the resolver taught which file a page means.
7. The summarisers re-read after their pages are fixed.
8. Pass 9 adds nothing; a gap goes to pass3.md §7 for the second edition.

### Pass 10 — the last polish (as chartered; the truth half is session M)

Pass 9's wording debt; the frame against the finished book; every internal
link and anchor under the link checker as a gate (done since pass 5); the last
cuts; the owner's remaining questions answered and the lecture order
confirmed; the introduction's *verified* paragraph made true of every gate;
the release — a git tag, the site verified against whatever version is
current, the second edition's seed written into §7 and *what this book
skips*. Then nothing more is done to the site except version passes and the
corrections readers file.

## Part 6 — session paragraphs

*(newest last; one per session, written by the session at its close)*
