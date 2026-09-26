# Pass 8 — the release: the version, the third fact-check, the polish, and the tag

*Planned 2026-09-26 by the planning session that followed the owner's post-pass-7
read, and rewritten the same day after the owner's second instruction: the pass
is the final fact-check, using the ledger every session since pass 5 has kept
for it, **and** a final polish over the exact wording — the voice pass is not
dropped after all, it is folded in. This is the last pass before the site is
left stable while the production process is rebuilt on another subject, so it
is planned to make the book as good as this process can make it, not merely
stable. Part 1 is the charter, Part 2 the brief given to each fact-check agent,
Part 3 the runbook a session follows, Part 4 the standard as recommendations
with the numbers behind them for session A to rule on, Part 5 the standing
rulings, Part 6 the schedule with the status column the owner reads, Part 7 the
charters this pass replaces, Part 8 the session paragraphs.*

## Part 1 — The charter

**Why one pass.** On 2026-09-16 the owner read the site as better than a free
wiki and not yet a textbook, and decided the *process* was the ceiling: linear
passes, each finding the errors at the edges of the last. The process is being
rebuilt from first principles on a new subject (`D:\DjangoDocs`, whose
`docs/brief.md` records the reasoning). Until that returns here,
minecraftdocs.dev is to be **stable**: verified against the current release,
every claim checked a third time, every sentence read once for its wording,
the frame truthful, the queues closed, a tagged release, and nothing half-done.
Three passes were planned for that. This one does what they would have done
that a stable book needs, in the order the plan always argued for — the
wording touched only after the facts are settled, and every touched sentence
read again by someone who did not touch it.

**What the pass does, in order of weight.**

0. **The version.** Minecraft **26.3 shipped on 2026-09-15**, so the site's
   *verified against 26.2* stopped being true eleven days before this brief
   was written, and rule 3 and ruling R6 put the version pass first. The
   planning session staged the 26.3 decompile (`tools/version_pass.py`,
   `reference/26.3/`: 7,301 classes against 26.2's 7,055 — 271 removed, 517
   added; 5,037 server classes; protocol 777) and measured it: **517 names on
   65 pages no longer resolve**, and 32 inside figures. Most are one of three
   changes of shape rather than five hundred renames — Blaze3D's GPU
   abstraction moved wholesale into a new `com/mojang/renderpearl` package
   (146 classes; `com/mojang/blaze3d` keeps `RenderSystem` and 85 others);
   world generation's `levelgen` lost 78 classes and gained 104, with the
   surface rules, the carvers and the `CARVERS` and `SURFACE` chunk statuses
   gone and the density-function nodes reworked; and `level/storage` lost 17
   and gained 82. Beside those, single names the book leans on:
   `ServerboundSwingPacket` (the introduction's own sentence), `RedStoneWireBlock`,
   `ItemInHandRenderer`, `NameTagFeatureRenderer`, the registry codecs
   (`RegistryFileCodec`, `RegistryFixedCodec`, `HolderSetCodec`,
   `KeyDispatchDataCodec`), `ContextAwarePredicate`, `NumberProvider`,
   `TreeConfiguration`, `BedBlock.OCCUPIED`. By part: XII 202, Reference 76
   (61 of them in the generated density-function view, which regenerates),
   II 62, XI 42, V 35, VII 34, IV 24, IX 11, VIII 9, and single digits
   elsewhere. Part XI's coverage as the atlas counts it falls from 60% to 56%
   only because `renderpearl` is in no part's package list yet; Part XII's
   falls from 80% to 68% because the new `levelgen` classes are named nowhere.
   This is two sessions, V1 and V2, before anything else: the plan's version
   pass was chartered as *a re-read, rarely a rewrite*, and 26.3 is a re-read
   of sixty pages and a rewrite of the sections on five.
1. **The third fact-check.** [pass9.md](pass9.md) is the ledger every session
   of passes 5, 6 and 7 wrote its claims and corrections into so that this
   check would read them first, and nobody has. `python tools/pass8_queue.py`
   routes its **1,333 entries**: 1,115 name a page (137 pages), 162 are a part
   session's notes naming no page (routed to that part), 56 are the standard,
   frame and close sessions' notes (session A's). Passes 2 and 4 found at least
   one wrong claim on every page they checked, and pass 6's finding — **a
   sentence that disagrees with the text beside it** — is the class a writing
   session cannot see in its own work. The check is pass 4's protocol
   ([pass4-brief.md](pass4-brief.md)): one adversarial agent per page with the
   decompile open, given the ledger as its opening checklist (Part 2 below),
   while the session reads the whole part into context and lists every place
   one sentence disagrees with another — which is where passes 5 and 6 found
   half their corrections and what a page-at-a-time check cannot find.
2. **The polish.** One voice and one vocabulary, every number saying what it
   counts, and no tic that a reader trips on twice. It is done **after** the
   check on each part, under rulings session A makes from counts rather than
   from memory (`python tools/pass8_voice.py`, Part 4): over 19,094 sentences,
   650 hedges of the *five of the seven* shape, 650 *rather than*s, 163
   corrections written in the voice of a correction, 97 possessives hung on a
   link, 43 em-dash chains, 20 dead-constant asides, 150 counts of classes,
   files or lines that rot at every release, 1,178 sentences over forty-five
   words, twenty-six glossary headwords spelled two ways, and the 320 open voice
   entries in [pass5.md](pass5.md) that four passes of readers left. The
   figures' register belongs here too: the 203 captions read as one set and
   the 19 Part XI figures that have none, the 48 figures still carrying 69
   sentence labels. Every sentence the polish changes is a claim: the session
   re-derives its own, and **session P reads every changed sentence in the
   corpus** (`python tools/pass8_diff.py`, off git) against the decompile
   before the release, because every pass that touches a sentence puts errors
   in — pass 4's finding, fifteen times over.
3. **Part XI's figures.** Pass 7's session K, Part XI · Rendering, never ran
   (the close ran before it at the owner's request). Part XI's figures are the
   corpus's worst by the render and the only part whose figures were never read
   against their sections: 19 uncaptioned, 17 figures with sentence labels, the
   book's only three eight-lane traces. It is session K here and runs pass 7's
   runbook and viewer brief ([pass7-brief.md](pass7-brief.md)), not this one's,
   against the 26.3 tree.
4. **The release.** The introduction's *verified* paragraph made true of every
   gate; `README.md`, `CLAUDE.md`, `TEMPLATE.md` and the frame pages swept for
   pass numbers promised as futures; the lecture order confirmed by the owner;
   the version line checked against Mojang's manifest on the day; the queues
   closed — every ledger entry struck, every open unit in pass5.md settled or
   ruled; a maintenance note that says what is true of the site while nobody
   is working on it; the tag `release-26.3`; the docs archived.

**What is dropped, and why.** Pass 10's *last cuts* and the 215 long sections
with no figure: both are the rebuilt process's business, and a cut made in the
last pass is checked by nobody. **Pass 8 adds nothing**: a gap goes to
[pass3.md](pass3.md) §7, the coverage queue, which seeds the second edition,
and `what-this-book-skips` and each landing page's *where the part stops* say
so honestly. The departments, the opinion layer and the recorded traces the
2026-09-16 conversation asked for are the new process's, not a polish's.

**What is new in the method.** Five things the earlier passes did not have.
The corpus's system pages are about 460k tokens and a part 27k to 52k, so **a
session reads its whole part into context before it checks a single entry**.
**The ledger is checked against itself**: a pass-7 correction that overturned
a pass-5 claim is one check, at the later entry, which `pass8_queue.py --part`
shows in order. **The polish comes after the check** on every part and every
changed sentence is read a second time by a session that did not write it.
**The version is one constant** (`tools/mc_version.py`) and the staging of a
release is one script (`tools/version_pass.py`), so the version pass is a
procedure rather than a day. And **the queues close**: pass5.md's entries have
been carried from pass to pass since 2026-09-02 and this is the pass that
settles or rules every one, so that a return finds two files — the ledger and
the queue — with nothing open in either.

## Part 2 — The brief (given to one agent per page)

You are fact-checking one page of MinecraftDocs, a book about how the Java
Minecraft codebase works, against the decompiled source of the version the
page's header names. Your job is to **falsify** the page, not to confirm it.
Every page checked in passes 2 and 4 had at least one wrong claim, and the
errors lived in the confident sentences and in the illustrations — the tables,
the one-line summaries, the captions, the closers, the asides. Assume this page
has errors, find them, and quote the evidence.

### What you have

- **The page**: the path is at the top of your prompt file. Read all of it.
- **The decompile**: the path is at the top of your prompt file (Mojang
  names; the client jar, a superset of the server jar). Beside it,
  `server-classes.txt` lists every class the dedicated server ships — the
  oracle for server-side versus client-only. Nothing under
  `net/minecraft/client/`, `com/mojang/blaze3d/` or `com/mojang/renderpearl/`
  is in it.
- **The data and assets**: `data/` (the built-in data packs: worldgen JSON,
  tags, loot tables, recipes, advancements) and `assets/` (models,
  blockstates, items, atlases, fonts, particles, post-effect chains, shaders)
  under the same tree. A claim about JSON is checked against the JSON, not
  against the class that reads it.
- **The libraries**: `reference/libs/` — Brigadier, DataFixerUpper and
  authlib as source, at the versions the game pins. A claim about how a
  codec, a command parse or a session-server call behaves is checked there.
- **The checklist**: the prompt file carries, after this brief, (1) every
  entry in the ledger `docs/pass9.md` that names this page — the claims the
  writing sessions of passes 5, 6 and 7 introduced and the corrections they
  made, oldest pass first, each with the session that wrote it; (2) every
  caption on the page; (3) the figure gate's notes for the page; (4) the
  page's confident sentences by category; (5) every diagram on the page as a
  numbered list of arrows. Those five are your opening work; the rest of the
  page is the second half.

### The order of work

1. **The ledger first.** Every entry is a claim a session introduced or a
   correction it made. Report on every one, with the file and line in the
   decompile that settles it, before you read the rest of the page. A
   *correction* is checked as a claim in its own right — confirm the fix, not
   the original — and then check that **the sentence beside it still agrees
   with it**, because a fix that made one sentence true often left the next
   one wrong. Where a later entry overturns an earlier one, the later entry is
   the claim. An entry that quotes a claim is re-derived from the decompile,
   never re-read for plausibility.
2. **The page against itself.** Before the source: every count in a lead-in
   against the list, table or paragraphs that follow it; every *both*, *the
   two*, *all three* against what is actually enumerated; every figure
   against the section under it and against the page's opening; every table
   against the prose that summarises it; every closer's answer against the
   section that owns the mechanism. Passes 5 and 6 found about half their
   corrections this way, and the prose was right and the summary wrong nearly
   every time. Report these under their own heading.
3. **The captions.** Each is a claim about what its figure shows. Read it
   against the figure above it and the section under it; a caption that names
   a count, an order or a boundary is checked like any sentence.
4. **The diagrams, arrow by arrow.** For each numbered arrow: a sequence
   arrow is a call — name the method that makes it and the method it lands in,
   in that order relative to its neighbours, and ask of every message **whose
   method is this, and whose lane is it on**: a message labelled with the
   caller's own method and drawn arriving at the callee is the commonest fault
   the figure pass found, in eleven parts of eleven, and the gate's notes in
   your prompt mark where it can hide (a qualified head on a lane that owns
   neither class is legitimate only for a static helper, an object with no
   lane, or the lane's own inner class). A note or bar naming a tick phase is
   checked against the tick method that runs that phase; a flowchart branch
   against the condition that decides it; a state transition against the code
   that triggers it. One verdict per number. A number you cannot settle is
   *unverifiable*, not silence.
5. **Every count, re-counted.** For each count in the *count* list, name the
   population (the enum, the registry, the class list, the callers) and quote
   how you enumerated it (`grep -c`, the file and lines — call sites, not
   lines). Report the number you got even when it matches. A count of
   classes, files or lines is checked against the tree, and its population
   said (with or without `package-info.java`, with or without nested types).
6. **Every only, never, always, all, none, every**: name the population the
   claim ranges over, say how you enumerated it, and list the members that
   break the claim if any do.
7. **Every "X, not Y", "X rather than Y", "X is a fallback / the exception"**:
   check both halves separately. The second half is a claim about the
   distribution or the other cases; pass 2 found these confirmed on the first
   half and never tested on the second.
8. **Every ordering** (before, after, then, same tick, next tick): find the
   two call sites and say which runs first, and whether the order is fixed by
   code or by data (a registration order, a list order).
9. **Every side or thread claim**: which side runs the code, and — the
   question pass 2 learned to ask — which side is *authoritative*, and what
   the other side does with the same code instead.
10. **Then the rest of the page**, sentence by sentence, for anything the
    lists above did not catch: a class said to own state it does not own; a
    field or method attributed to the wrong class (the name gate only checks
    that the token appears somewhere in the named class's file); a causal
    *so* or *because* whose reason is not in the code; a fact that was true of
    an earlier version and is not true of this one — the version in the page's
    header is the only version that exists.
11. **The completeness question** (asked only when the prompt says so): what
    is in this page's scope in the decompile that the page never mentions?
    Name the classes and what they do, one line each.

### What to report

A single markdown report in this shape. Nothing else.

```
## The ledger
- [pass N, session X] — <the entry, shortened> — CONFIRMED | WRONG | UNVERIFIABLE | MISLEADING
  evidence: <path relative to the decompile>:<line>, <what it says in one sentence>
  beside it: <the sentence next to the corrected one, and whether it still agrees>

## The page against itself
- L<page line> against L<page line> — <what the two say> — AGREE | DISAGREE (<which is right, and the evidence>)

## The captions
- figure N — <the caption's claim> — CONFIRMED | WRONG | UNVERIFIABLE — <evidence>

## Figures
### Figure 1 (<type>, page line N)
- 1 — CONFIRMED | WRONG | UNVERIFIABLE — <evidence: file:line>; head: <whose method, whose lane>
- 2 — ...

## Counts
- L<page line> — "<the sentence's number and what it counts>" — page says N, decompile says M — <how counted: file, grep, lines; the population>

## Absolutes
- L<page line> — "<the claim>" — population: <what and how enumerated> — CONFIRMED | WRONG (<the members that break it>)

## Contrasts and orderings
- L<page line> — "<the claim>" — first half: <verdict, evidence>; second half: <verdict, evidence>

## Sides and threads
- L<page line> — "<the claim>" — runs on: <side/thread, evidence>; authoritative: <side, evidence>

## Everything else
- L<page line> — WRONG | MISLEADING | UNVERIFIABLE — <what the page says> — <what the decompile says> — <file:line>

## Names
Every backticked identifier that is declared somewhere other than where the
page attributes it, or does not exist: <name> — page says <class>, declared in <class> (<file:line>)

## Completeness (only if asked)
- <class or mechanism> — <what it does in one line> — <file>

## Could not verify
- <claim> — <what you looked for and where>
```

Rules for the report:

- **Quote evidence for every verdict**, CONFIRMED included: a path under the
  decompile and a line number. A CONFIRMED without evidence is not a verdict.
  An empty WRONG list from a report with no evidence is a failed check.
- **Your names are as suspect as the page's.** Every method or field you cite
  must be one you opened. Do not cite from memory of any earlier version; the
  game renames and reworks classes every release (`ResourceLocation` is
  `Identifier`, `LightTexture` is `Lightmap`, `Timer` is `DeltaTracker`, the
  GPU abstraction is under `com/mojang/renderpearl`), and a name that resolves
  in the tree is the only kind that counts.
- **Count the call sites.** For any "the only", "exactly one", "N of M": list
  the members. `grep -rn` across the decompile is the tool, and the report
  says what was grepped.
- **Mark the severity of a WRONG**: whether the sentence around it — the
  hook, an invariant, a diagram's argument, a caption — still stands, or
  falls with it.
- **Do not rewrite the page.** Report; the session fixes.
- **Do not judge the wording.** Register, tics and terminology are the
  session's business after your report; a sentence that is true and clumsy
  is CONFIRMED.
- **Do not stop early.** If the page is long, the ledger, the page against
  itself and the figures come first and the rest follows; a report that
  covers only part of the page says which part it did not reach.

---

## Part 3 — The runbook

One session = one part (Part XI is two: its figures, then its check and
polish), on Opus, with the decompile at `reference/26.3/` — sessions V1 and V2
put it there and flip the tools to it, and no later session runs before they
have. Every step is a command or a rule; the judgement is in steps 6, 7 and 8.

### 1. Read

[plan.md](plan.md) (the charter and this session's row in Part 6 below),
`CLAUDE.md`, this file whole — Part 4 as session A ratified it and Part 5 are
the rulings the session applies — `TEMPLATE.md`'s *Voice* section (session A
writes it, from Part 4), and the two standing standards that still bind:
[pass6-brief.md](pass6-brief.md) Part 3 (the page's devices: the second
person, the closer, the blockquote, the opening) and [pass7-brief.md](pass7-brief.md)
Part 3 (the figures). Then the part's landing page. Then:

```
python tools/mc_version.py                       # says 26.3 and that the tree is present, or stop
git tag --list pass-8-start                      # V1 placed it before touching a page, or stop
python tools/pass8_queue.py --part VI            # the ledger, by page, oldest pass first; then the part-wide notes
python tools/pass5_queue.py --part entities      # the queue, every kind: what four passes of readers left here
python tools/pass8_voice.py --part entities      # the voice, measured, one row per page
grep -rn "<!-- Q:" src/systems/entities          # the owner's questions; each answered in the prose before the session ends
```

### 2. Generate the prompts

```
python tools/pass8_prompts.py --part entities --out <scratchpad>/pass8-entities
```

One file per page, `<part>--<slug>.prompt.md`: Part 2 above, then the page's
ledger entries, its captions, the figure gate's notes for it, its confident
sentences (`claims.py`) and its diagrams arrow by arrow (`diagram_arrows.py`).
Beside each, `<part>--<slug>.session.md` for the session alone: the page's
open queue units of every kind, its voice measure with every sentence listed,
and every inbound link by anchor. `_part-notes.md` carries the ledger's and the
queue's part-wide notes, which the session routes by hand; `_part-voice.md`
the part's voice table. The frame session uses `--part frame` and
`--part reference`.

### 3. Launch

One background agent per page, all at once, on Opus. The prompt is one line:
*Read `<prompt file>` and do what it says; the page is at `<path>`. Write your
report to `<scratchpad>/pass8-<part>/<slug>.report.md`.* Reports are not
committed. One agent per page, never per part — a part-wide brief hit the
spend limit in pass 3.

### 4. Read the part whole while they run

Every page of the part, landing page first, in watch order, in one sitting.
Before opening a single report, write down every sentence that disagrees with
another sentence in the part — a count, a name, an ordering, a direction, an
owner, a thread — and every place a page contradicts its own figure, table or
opening. Then read `_part-notes.md` and decide which page each note belongs to,
or that it is *(no claim)*. This list is the session's own checklist and is
worked before the reports are, because it is the class the reports cannot see.

### 5. Audit the reports

For every WRONG that changes a trace, a hook, a count in an argument, an
invariant or a caption: **open the decompile yourself before touching the
page.** Pass 3's drafting agents were wrong in about a third of their own
corrections, pass 2's cited methods that do not exist, and the ledger's own
corrections were wrong three times in pass 4's audit. Suspect the tool once
(`verify_names.py`, the generators, the extractors), then the agent once, then
the page. Take the completeness findings on trust; take nothing else on trust.

### 6. Fix

In place, sentence by sentence, in the smallest edit that makes the sentence
true; nothing else on the page changes in this step. A wrong hook is replaced
by a true one even when the opening has to be rewritten around it. A false
arrow is redrawn under pass 7's standard and rendered (`node
tools/render_figures.js --no-build --pages systems/<part>`) before it is
committed. **Grep the corpus for every corrected claim** — a wrong fact stated
once was usually leaned on elsewhere — and fix the landing page, `lectures.md`
and the glossary in the same commit where they repeat it. A structural finding
is struck *second edition* in [pass5.md](pass5.md) with the reason; a system
with no owner page goes to [pass3.md](pass3.md) §7.

### 7. Polish, after the facts

Only now. From the session file's voice list and the page's open voice units,
under Part 4 as ratified and `TEMPLATE.md`'s *Voice*: the tics, the hedges
without a population, the corrections written as corrections, the two
spellings of one term, the possessive on a link, the caption and label
register, the blockquote's form. The smallest edit that makes the sentence
plain; **no heading is reworded** (an anchor moves every link that lands on
it), no paragraph is restructured, no list re-budgeted, nothing cut except a
sentence that says what the sentence beside it says, no fact changes without
the decompile open. A session that finds itself rewriting a paragraph for its
voice has left the pass, and stops. The book and lecture units in the queue
are settled here only where the fix is wording-sized; otherwise struck *second
edition* with a word saying why.

### 8. Re-derive

Every correction the session made, and every polished sentence whose meaning
could have moved — a count restated, a hedge given its population, a term
replaced, a caption reworded — is read once more from the file against the
decompile before the commit (R4). The rest of the polish is session P's.

### 9. Strike

In [pass9.md](pass9.md), every entry the session checked: struck (`- ~~…~~`,
the strike outside the bold) when found right; struck and followed by a
correction under this session's own heading when found wrong, in the form the
file's head prescribes; struck *(no claim)* when it was a note. In
[pass5.md](pass5.md), every unit the session settled: *done*, *overtaken*,
*ruled* with why, or *second edition* with why. Both in the same commit as the
pages.

### 10. Verify and ship

```
python tools/verify_names.py
node tools/check_mermaid.js
python tools/check_lanes.py --strict
python tools/check_figure_names.py --strict
python tools/check_links.py --quiet
python tools/check_deps.py                        # if a landing page, lectures.md or the figure changed
mdbook build
git add <your files, by name> && git commit -F <message file>     # "pass 8, session X — Part N: <summary>"
tools/deploy.sh
```

Run `verify_names.py` after each page, not after all of them. Commit your own
files by name, never `add -A`; two sessions are often open.

### 11. Record

- [pass9.md](pass9.md): the session's entry under `## Pass 8, session X — Part N`,
  in the head's form: *Corrections* (one numbered item per fact — page:line,
  what it said, what is true, file:line, or *(page-internal)*), *Figures
  changed* with their orderings, *Captions written*, and **Polished**: every
  sentence whose meaning could have moved, quoted; the rest by kind with a
  count (*hedge 14, contrast 9, possessive 3*).
- [pass5.md](pass5.md): nothing new is appended for a later pass; what the
  session cannot settle is struck *second edition* where it stands.
- [plan.md](plan.md): the session log line.
- **This file, Part 6: the session's row** — the status cell flips to *done
  <date>*, and one line in the last column says what the session did; then
  the paragraph in Part 8: entries checked, found wrong, corrections made with
  the three worst quoted, what the whole-part read found that the reports did
  not, what the polish changed by kind, and anything left for session P or Q.

### The two sessions that run a different runbook

**V1 and V2, the version pass**, run [plan.md](plan.md)'s version pass with the
tools this planning session built; their rows in Part 6 are the procedure.
**Session K, Part XI's figures**, runs [pass7-brief.md](pass7-brief.md)'s Part 1
and Part 2 whole — the viewer agents with the picture and the section, the
render, the gate — and records in that file's Part 4 as well as this one's;
its polish is only what pass 7's rulings already allow (captions, lead-ins,
labels).

---

## Part 4 — The standard (recommendations with the numbers behind them, for session A)

*The planning session's recommendations, each with the count from
`python tools/pass8_voice.py --summary` on 2026-09-26 over 19,094 sentences on
137 pages, and where the count came from in the queue. Session A ratifies,
amends or rejects each one against the exemplar and writes the rulings into
`TEMPLATE.md` under a new section, *Voice*, which is where the part sessions
read them; this Part becomes the record of what was decided and why, in pass
7's Part 3's form. No count below is a target: a tic is kept wherever it earns
its place, and the session says so in its log when it keeps one the ruling
would remove.*

### V1. The exemplar

`entities/entity-lifecycle` again — the page passes 6 and 7 rewrote to their
standards, so it is the one page where every device is already ruled and only
the sentences are left. Session A checks it under Part 2 first (its own
agent, its own whole-part read of Part VI's landing page and neighbours),
polishes it under V2–V17, and writes the voice from what the polishing
decided. Its measure today: 9 hedges, 9 *rather than*s, 1 correction-voice,
0 dead-constant asides by the tool's regex (its *Three constants nobody reads*
section is the page's own finding and stays), 0 possessive links, 2 counts
that rot, 17 sentences over forty-five words, in 232 sentences.

### V2. The contrast — 57 *not X but Y*, 650 *rather than* and *instead of*

Pass 2's most common register error, and Part XIII was its worst offender;
by now the bare *not X but Y* is down to 57, and the milder spelling is
everywhere. **Recommendation:** a contrast earns its place only where the
reader would otherwise assume X — the forum's belief, the 1.21 fact, the
obvious reading — and then X is named as that belief (*the wiki says…*, *a
reader who knows 1.21 expects…*); elsewhere the sentence states Y. The 650
are read, not hunted: most *rather than*s are the plain way to say a choice
and stay. The tool lists them; the ruling is the test, not a number.

### V3. The hedge — 650 of the *five of the seven* shape

The named-qualifier hedge (*with two exceptions*, *all but the first*, *five
of the seven*) is right precision in repetitive phrasing, and the queue's
readers found its real fault: the population is often unnamed (*among the
tick commands it is the only one*, over a command set no page enumerates;
*ninety-one gates that name a level constant*, excluding two the next sentence
explains without saying so). **Recommendation:** a hedge names its exception
or its population — in the sentence, or in the table beside it — or becomes
the plain rule. *Five of the seven* beside a seven-row table stays; *five of
the seven* two screens from the seven is rewritten to name them or to drop the
count. A count that admits two readings (the fifty-odd pass 5's close found;
`claims.py --counts` lists every count) names its population once.

### V4. The em-dash chain — 43 sentences with three or more dashes

Pass 3's pilots left them in the decision tables' gate cells and the frame's
new prose carried more. **Recommendation:** at most one dash pair a sentence;
a second aside becomes a sentence or a parenthesis. Forty-three is a morning.

### V5. The correction written in the voice of a correction — 163

*Actually* (150 of the 163), *in fact*, *contrary to*, *it turns out*,
*despite its name*, and the parenthetical explaining why the obvious version
does not work — the residue of two fact-checks whose fixes were written as
fixes. **Recommendation:** the page states what is. Where the wrong belief is
common enough to be worth naming, the myth table or the closer holds it; in
the body, *actually* goes unless the sentence is contrasting a belief the
page has just stated.

### V6. The dead-constant aside — 20, on ten pages

*The number is right; the constant that names it has no reader* — four to a
part in Part IV, a Part VII habit, four on one page in Part VI; every reader
skipped every one as a note about how the source reads. **Recommendation, to
decide once:** the book names a constant nothing reads only where the page's
number *is* that constant's value and a reader would grep for the name; then
the name is given once, in the sentence with the number, as *`X.FOO`, which
nothing reads* — and the sentence-long aside goes. A page whose finding is
the dead constant (the exemplar's *Three constants nobody reads*) keeps its
section; that is a fact about the system, not a tic.

### V7. The terminology — the glossary is the checklist

`python tools/pass8_voice.py --terms` finds **twenty-six glossary headwords the
corpus spells two ways**, space against hyphen (*data pack* on 46 pages and
*data-pack* on 31, *block entity* 33 and 18, *frame graph* 11 and 13, *old
chunk* 5 and 7, *density function* 2 and 5). Most hyphens are the compound
used as a modifier (*a data-pack field*), which is English, not drift.
**Recommendation:** the noun takes the glossary's spelling everywhere; the
hyphen is allowed only in the attributive position, and a page that uses the
noun form hyphenated is corrected. And the words the queue found carrying two
senses, with the ruling proposed for each:

| word | the two senses | the recommendation |
|---|---|---|
| *extract* / *record* | `GuiGraphicsExtractor` and the render-state *extract* against the same stage called the *record pass* on four Part X pages | **extract**, because it is Mojang's word and the glossary's headword; *record* stays only as a plain verb |
| *the hop* | a packet reaching the game thread (`ensureRunningOnSameThread`, `reference/threads`) against the post *out* to the sound thread (`sound-engine`) | *the hop* is the packet's crossing only; the sound engine's is *the post* |
| *ledger* | the prediction ledger (18 uses, the through-line's) against `server-tick`'s *three ledgers* and a loose metaphor on two Part VII pages | the ledger is the prediction ledger; the other two want their own word (*the three tallies*; *a stack*) |
| *level* | a ticket level that counts *down* toward loaded, on three Part IV pages, against the world and an enchantment's level on `loot-tables` | one sentence where a reader first meets the ticket level, on `tickets-and-loading`; `loot-tables` says *enchantment level* and *the world* |
| *phase* | a `ConnectionProtocol` against a step of the server tick, both on `the-connection` | *protocol phase* and *tick phase* wherever the page has both |
| *classes* / *files* | a package's count with or without `package-info.java`, three conventions inside Part XIII | the atlas's rule — a class is a file, nested types not counted — and the word is *classes*; a page that counts something else says what |
| *client thread* / *Render thread* | the same thread on three Part XI pages, against their own cast tables | *Render thread*, the key's and `reference/threads`' name |
| `Registries.X` / `BuiltInRegistries.X` | the same registry named both ways two hundred lines apart | one sentence on `identifiers-and-registries` saying which is the key and which the instance, and a glossary line |
| *game time* / a clock's total ticks | the exemplar of pass 6's wire section | the clock page's own terms, `Timelines` and the game-time attribute, and *game time* only for `Level.getGameTime` |
| *the shared worker pool* | shared with what — four pages, none says | *the worker pool* with the anatomy anchor, once per page |
| *batch*, *context*, *inert*, *lane* | one word, two senses on one page each (`game-tests`, `contexts-and-predicates`, `enchantments`, `chunk-storage`) | the second sense gets a different word or a qualifier on that page |

`pass8_voice.py --list terms --part <dir>` prints every sentence carrying one
of these words, per page, so a session reads them for sense rather than
searching.

### V8. The possessive on a link — 97

*"is [the server tick](…)'s"* — the citation form pass 5 settled, which three
readers across three pages read as a typo before they parsed it and one
reported as an error; one instance was missing its *s*. **Recommendation:**
the possessive never hangs on a link's closing bracket. *Belongs to [the
server tick](…)*, *is the server tick's ([the server tick](…))*, or the noun
inside the link — whichever the sentence takes.

### V9. The number device — 24

`**Two** — writes to the socket per client per tick`: the noun the number
counts arrives after the dash, so the bold word is unattached until the reader
has read past it; both readers who met it said so. **Recommendation:** amend
`TEMPLATE.md`'s device so the number and its noun are one phrase —
`**Two writes** to the socket per client per tick (…)` — and rewrite the
twenty-four. The device stays; its form changes.

### V10. The counts that rot — 150 counts of classes, files or lines in prose

A count in a sentence survives an edit; an empty table cell does not (pass 6's
lesson), and a count of classes or lines survives a *release* while going
wrong — 26.3 moved 788 classes. **Recommendation:** a class, file or line
count in prose either comes from a generated include (the size and coverage
phrases already do) or is dropped in favour of the atlas link, unless the
number is the page's argument (*one file of static methods*, *573 lines the
book explains nowhere*), and then it is checked by the fact-check agent as a
population and left. `pass8_voice.py --list rot` is the list.

### V11. The long sentence — 1,178 over forty-five words

A pacing signal, not a fault: the queue's readers named four passages they
read slowest, and each was three or four steps of reasoning in as many
clauses. **Recommendation:** no ruling on length. The session reads its part's
longest sentences (the tool ranks them) and splits the ones where a step of
reasoning is hidden in a subordinate clause; a long sentence that is one idea
stays. This is the one recommendation where the count is only a place to
look.

### V12. The figures' register — 203 captions, 19 missing, 69 sentence labels on 48 figures

Pass 7 wrote the captions one part at a time and never read them as a set;
the close found four spellings of the caption on the thirteen landing figures
alone. **Recommendation:** a caption is one sentence in the present tense
saying what the picture shows and what to look for, one italic run end to end
(the gate checks the run); it names the shape first where the shape is the
point; it never says *this figure* or *the diagram above*. The 48 figures with
sentence labels are cut to F4's budgets where the label's sentence has a home
in the prose, and left where the figure pass ruled them (three in Part I and
II are ruled). The gate's 62 notes — bare-verb heads and third-class heads —
are read by each part session with the caller's-method question (Part 2, step
4) and stay notes where the head is a verb the lane does. Part XI's 19 missing
captions are session K's.

### V13. The 1.21 blockquote — 47 pages

Pass 6 put every one at the foot; its register was left to this pass.
**Recommendation:** one form corpus-wide — `> **For a 1.21-era reader.**` then
what moved, as *X is now Y* or *X is gone; Y does its work* — at most eight
lines, nothing that only says *this is new*, and no row that `naming-drift`
already carries unless the page's mechanism depends on it (`blaze3d` restates
six of the table's rows and `the-window` repeats one of them). After V2, the
26.3 changes go in the same blockquotes where a 1.21 reader would hunt for the
old name, and nowhere else: rule 3 allows a drift note, not a version history.

### V14. The second person — A1 stands, and is not re-decided

44 pages open on *you*. Pass 6's ruling A1 says what varies is the way in, not
whether the reader is addressed; no part opens most of its pages on the word.
**Recommendation:** no corpus-wide change. A part whose session finds four or
more of its pages opening on the same word varies one or two, as A1 already
allows, and says so in its log.

### V15. Headings are anchors — never reworded

27 links land on closers' anchors alone, and `blocks-and-states`' *The two
update channels* is cited by nine pages. **Recommendation, as a rule:** the
polish never rewords a heading. A heading that is *false* is a correction,
made with `check_links.py --inbound` in hand and every link repointed in the
same commit.

### V16. What the polish never does

No paragraph restructured, no section reordered, no list re-budgeted, no
figure redrawn for its look, no cut beyond a sentence that repeats its
neighbour, no fact changed without the decompile open, no heading reworded, no
device added, no *Questions players ask* opened or closed (A2 is settled), no
change to the verified line's scenario, no page moved. The rebuilt process is
meant to produce the voice; this pass makes the present voice consistent and
plain, and stops there.

### V17. Every polished sentence is a claim

The session re-derives every polished sentence whose meaning could have moved
before its commit (R4), lists those in [pass9.md](pass9.md) under *Polished*,
and counts the rest by kind. Session P then reads **every** sentence changed
since `pass-8-start`, from git (`python tools/pass8_diff.py`), against the
decompile, page by page — the second reading nothing in passes 3 to 7 had, and
the reason the polish is allowed into the last pass at all.

---

## Part 5 — The rulings (standing; session A adds to them and never removes one)

- **R1 · Truth first, then plainness.** A change in this pass is one of: a
  false claim made true; a false arrow redrawn; a frame page made accurate; a
  ledger entry struck; a queue unit settled or ruled; a sentence polished
  under Part 4 as ratified. Anything else is out of scope, however small.
- **R2 · The whole-part read is not optional.** It is step 4 of every part
  session, and its findings are logged even when the ledger is empty for the
  page, because that is where passes 5 and 6 found half their corrections.
- **R3 · The ledger closes on itself.** Every one of the 1,333 entries is
  struck by the close, each with its verdict (`python tools/pass8_queue.py
  --unstruck` is the test), and the pass's own corrections and polish are
  listed in the same file under its own headings, so that a return reads one
  file to know what was checked, by whom, and what was changed on purpose.
- **R4 · A correction is a claim, and so is a polished sentence.** Re-derived
  once more from the file before commit, by the session that made it; every
  changed sentence read again by session P; the close audits a sample of
  thirty strikes and thirty corrections.
- **R5 · No pass number is a promise.** After the release, no published page,
  `README.md`, `CLAUDE.md` or `TEMPLATE.md` names a pass as a future. The
  passes are history, recorded in `docs/`.
- **R6 · The version line is a test.** The release states the version the
  site is verified against, checked that day against Mojang's manifest
  (`python tools/version_pass.py --latest`). 26.3 is that version; if 26.4
  ships before session Q (the cadence is quarterly — 26.1 on 2026-03-24, 26.2
  on 2026-06-16, 26.3 on 2026-09-15, and 26.4-snapshot-1 on 2026-09-22 — so it
  is unlikely before December), the version pass runs again as a session
  before Q, and Q waits for it.
- **R7 · A reader's correction has an evidence rule.** The issue template
  (`.github/ISSUE_TEMPLATE/correction.yml`) asks for the page, the sentence,
  what the decompile says and where; a report without a location is answered
  with a request for one, not investigated.
- **R8 · The queue closes.** Every open unit in [pass5.md](pass5.md) — 603
  on 2026-09-26: 85 book, 42 lecture, 28 figure, 320 voice, and 128 record
  that no pass acts on — is struck by the close as *done*, *overtaken*,
  *ruled* or *second edition*, each with a word saying why, and `python
  tools/pass5_queue.py --summary` at zero open is the release's test. Nothing
  is appended to it for a later pass, because there is none.
- **R9 · The polish is after the check, under the rulings, and stops at the
  sentence.** Part 3 step 7 says what it may do; a session that has to
  restructure to make a sentence plain leaves the sentence and logs the
  finding as *second edition*.
- **R10 · Pass 8 adds nothing.** A gap goes to [pass3.md](pass3.md) §7 and
  is declared where the book says what it skips. A new page written in the
  last pass would be checked by nobody.
- **R11 · The version pass runs first and in full.** No page is fact-checked
  or polished against 26.2 after 2026-09-26; sessions V1 and V2 finish, deploy
  and flip the tools before session A begins, and every later session's first
  command is `python tools/mc_version.py`.

---

## Part 6 — The schedule

The counts are the tools' on 2026-09-26: the ledger by `pass8_queue.py`
(named entries plus the part's own page-less notes), the queue by
`pass5_queue.py --summary` (book · lecture · figure · voice), the voice by
`pass8_voice.py` (hedges · contrasts · corrections-as-corrections · possessive
links, the four kinds most worth a session's time), the words by `wc`. Sessions
run in the order of the table, one context window each, on Opus; the **status**
column is the one the owner reads — `—` until the session runs, then *done
<date>*, written by the session itself in step 11 — and the last column is
what the session did, in one line. Nineteen sessions where the 2026-09-26
morning's brief had thirteen; the six are the version (two), the polish's
second reading (one), Parts I and II given their own session instead of
sharing A's, and Parts V and VI and Part XI's two halves given the session
each that every earlier pass gave them. The owner may merge V1 into
V2, or B into A, if either runs short.

| session | scope | ledger | queue (b·l·f·v) | voice (h·c·cv·p) | words | status | what the session did |
|---|---|---:|---|---|---:|---|---|
| **V1** | **the version pass, mechanical.** `python tools/version_pass.py 26.3` has run (the tree is at `reference/26.3/`; run it again and it skips what is present); `git tag pass-8-start` before any page changes; `python tools/version_pass.py 26.3 --flip` and `python tools/mc_version.py`; `map_source.py`'s `PARTS` given `com/mojang/renderpearl` (Part XI) and read against 26.3's new packages (`level/blockscan`, `item/slot`, `attribute/modifier`); `python tools/map_source.py`, `gen_reference.py all`, `pass5_coverage.py --write`, `check_deps.py --write-figure`, and **the diff of `src/generated/` read** — a population that moved is a page that changed; `verify_names.py` and `check_figure_names.py --strict`: every rename resolved to the 26.3 name with the smallest edit, every removed name replaced by what does its work or the sentence cut, on the sixty pages outside V2's five; `claims.py --counts` over the touched pages; the header line on every page, `CLAUDE.md`, `README.md`, the introduction, `book.toml`, the issue template's placeholder, `fetch_libs.sh`'s defaults; the gates; deploy; every change logged in [pass9.md](pass9.md) under *Pass 8, session V1*, and every section whose *mechanism* changed listed for V2 or the part session | 517 names on 65 pages; 32 in figures | — | — | — | — | |
| **V2** | **the version pass, the systems that changed shape:** `worldgen/terrain`, `worldgen/density-functions`, `world/chunk-generation-pipeline` (the status ladder without `CARVERS` and `SURFACE`; the surface rules and carvers gone or moved), `rendering/blaze3d` and Part XI's landing page (`renderpearl`: `api`, `backend`, `frontend`, `util`), `foundations/codecs-nbt-json` and `data-driven-types` (the registry codecs), `world/chunk-storage` (`level/storage`), `blocks/signal-and-dust` (`RedStoneWireBlock`), `player/the-sword-swing` and the introduction (`ServerboundSwingPacket`), `items/using-an-item` (`ItemInHandRenderer`), `reference/density-function-nodes` regenerated and its prose re-read. Each page made true of 26.3 with the decompile open, figures included, in the smallest rewrite; what the part session must re-read deeper is written into the ledger under *Pass 8, session V2*; the 1.21 blockquotes gain the 26.3 drift where a reader would hunt for the old name (V13); `naming-drift` gains the rows. Gates, deploy, the paragraph | the same 517, the deep half | — | — | — | — | |
| **A** | **the standard.** Part 4 ruled against the exemplar (`entities/entity-lifecycle`: its own agent under Part 2, its polish under V2–V17), the rulings written into `TEMPLATE.md` as *Voice* and the device amended (V9), Part 4 rewritten as the record; the ledger's 56 frame-level notes (`pass8_queue.py --part Frame`) struck *(no claim)* or routed to a page; pass 7's close's audit of the ledger's shape ([pass9.md](pass9.md), session O's entry) read and its workarounds written into Part 3 where they bind a session; the queue's routing tags checked (`pass5_queue.py --unsure`) so that R8's count is honest; Part 2 rehearsed on the exemplar and amended if the report's shape failed it | 56 | — | 3·2·1·0 | 5.2k | — | |
| **B** | I · Anatomy, II · Foundations and the Maps | 25+3 · 61 · 24 | 4·2·3·9 / 3·0·0·13 / maps in frame | 14·18·2·2 / 29·34·7·6 | 32.5k | — | |
| **C** | III · The server | 81+3 | 6·1·1·22 | 28·34·5·11 | 20.9k | — | |
| **D** | IV · The world | 88+8 | 5·5·0·25 | 51·52·17·9 | 38.8k | — | |
| **E** | V · Blocks | 48+52 | 10·0·1·28 | 32·34·9·4 | 24.3k | — | |
| **F** | VI · Entities | 95+3 | 7·4·0·24 | 55·56·15·9 | 33.8k | — | |
| **G** | VII · Items and inventories | 74+2 | 2·4·0·21 | 53·56·14·1 | 29.8k | — | |
| **H** | VIII · The player | 84+12 | 5·1·0·21 | 29·27·9·8 | 20.1k | — | |
| **I** | IX · Networking | 73+30 | 6·1·0·16 | 30·43·12·13 | 21.7k | — | |
| **J** | X · The client — the largest ledger; may split at the GUI stack (pages 1–5, 6–12) | 118+17 | 6·3·4·27 | 59·71·10·9 | 29.6k | — | |
| **K** | XI · Rendering, **the figures** — pass 7's session K: its runbook, its viewer brief, its gate; the part's 20 figures rendered and read against their sections; the 19 captions written; the three eight-lane traces split or folded; the 17 figure-kind queue units; recorded in [pass7-brief.md](pass7-brief.md) Part 4 as well as here | — | ·   ·17·   | — | — | — | |
| **L** | XI · Rendering — the check and the polish, after K | 82+8 | 1·5·0·25 | 82·72·21·21 | 35.7k | — | |
| **M** | XII · World generation — the part V2 rewrote most; its agents read V2's ledger entries first | 77 | 6·1·0·18 | 69·61·19·2 | 30.7k | — | |
| **N** | XIII · Commands and data packs | 72+24 | 6·7·1·22 | 39·38·14·0 | 25.6k | — | |
| **O** | **Reference and the frame** — the introduction, `lectures.md`, the atlas's prose, `reference/README` and the hand-kept Reference pages, read *after* the parts (the summarisers are read last); the glossary against every owner page; `what-this-book-skips` and every *where the part stops* against [pass3.md](pass3.md) §7 | 85 · 28+56 | 18·8·1·49 | 43·38·7·2 / 17·12·1·0 | 55k + 9k | — | |
| **P** | **the second reading.** `python tools/pass8_diff.py` — every sentence changed since `pass-8-start`, by page, read against the decompile by a session that changed none of them; the ledger's *Polished* sections read against the pages; thirty strikes and thirty corrections audited (R4); `pass8_queue.py --unstruck` and `pass5_queue.py --summary` at zero, or the gaps listed for Q | — | — | — | — | — | |
| **Q** | **the release.** `version_pass.py --latest` (R6; if 26.4 has shipped, a version session runs first and Q waits); the introduction's *verified* paragraph made true of every gate; the pass-number sweep of `README.md`, `CLAUDE.md`, `TEMPLATE.md` and the frame pages (R5); the lecture order as the owner confirmed it; the maintenance note in `README.md` and [plan.md](plan.md) — what is true of the site while nobody works on it, what a release triggers, how a reader's correction arrives and who answers it; `README.md`'s corrections paragraph rewritten for a site with no current pass; the tag `release-26.3`; deploy; pass 8 archived whole into this file's Part 8 and [plan.md](plan.md) closed with the verdict on whether the pass earned its cost | — | — | — | — | — | |

**The owner's part.** Three things only the owner does: confirm the lecture
order in `src/lectures.md` before session Q (a read of the lecture map and a
yes, or a reordering); decide, after V1's row is filled, whether V2's five
rewrites are what they want written in this pass or declared in the
blockquotes and left to the return (the brief assumes written); and the
dashboard items the 2026-09-26 morning listed (Search Console, the analytics
permission, the Pages metrics toggle), which are not this pass's but are what
makes the stable site observable.

### What the tools measured (2026-09-26)

**The ledger** (`pass8_queue.py`): 1,333 entries, none struck — 1,115 naming
a page (137 pages), 162 a part session's notes naming no page, 56 the
standard, frame and close sessions' notes. By part: Frame 28, Maps 24, I 25+3,
II 61, III 81+3, IV 88+8, V 48+52, VI 95+3, VII 74+2, VIII 84+12, IX 73+30,
X 118+17, XI 82+8, XII 77, XIII 72+24, Reference 85. Pass 7's close audited
the ledger's shape and found nine of thirteen pass-7 entries not walkable item
by item (captions claimed and not listed; corrections without a file and
line; figures called redrawn with no orderings; source quoted); its
workarounds are in session O's entry at the file's head, and `pass8_prompts.py`
lists every caption from the pages rather than from the entries.

**The queue** (`pass5_queue.py --summary`): 603 open units — 85 book, 42
lecture, 28 figure (17 in Part XI), 320 voice, 128 record; 460 name a page,
143 are part-wide; 75 are the tool's guess and session A tags them.

**The voice** (`pass8_voice.py --summary`), over 19,094 sentences:

| kind | count | where it is thickest |
|---|---:|---|
| *not X but Y* | 57 | VII 8, V 7, XI 6 |
| *rather than*, *instead of* | 650 | XI 72, X 71, XII 61 |
| the hedge | 650 | XI 82, XII 69, X 59 |
| the em-dash chain (three or more) | 43 | Reference 8, V 6, IX 5 |
| the correction as a correction | 163 | XI 21, XII 19, IV 17 |
| the dead-constant aside | 20 | IV 4, on ten pages |
| the possessive on a link | 97 | XI 21, IX 13, III 11 |
| the number device | 24 | one or two a part |
| pages opening on *you* | 44 | VI 7, VII 6, XII 6 |
| sentences over forty-five words | 1,178 | VI 113, IV 111, XI 109, XII 109 |
| counts of classes, files or lines | 150 | XIII 21, Maps 20, VI 18 |
| glossary headwords spelled two ways | 26 | *data pack* 46/31, *block entity* 33/18, *frame graph* 11/13 |

**The figures** (`pass7_figures.py --summary`, `captions.py`,
`check_figure_names.py --notes`): 222 figures, 203 captioned, 19 not (all
Part XI's); 48 figures with 69 sentence labels, 17 of them in Part XI; three
sequence diagrams over seven lanes, all Part XI's; the gate at 0 unresolved and
62 notes against 26.2, 32 unresolved against 26.3.

**The version** (`version_pass.py 26.3 --check`): above, in the charter.

---

## Part 7 — What this pass replaces

The charters of passes 8, 9 and 10 as [plan.md](plan.md) carried them until
2026-09-26, kept because Part 2 and Part 4 descend from them and a return may
want the lists.

### Pass 8 — the voice (as chartered; now Part 4)

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

### Pass 9 — the third fact-check (as chartered; now Parts 2 and 3)

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

### Pass 10 — the last polish (as chartered; the truth half is session Q)

Pass 9's wording debt; the frame against the finished book; every internal
link and anchor under the link checker as a gate (done since pass 5); the last
cuts; the owner's remaining questions answered and the lecture order
confirmed; the introduction's *verified* paragraph made true of every gate;
the release — a git tag, the site verified against whatever version is
current, the second edition's seed written into §7 and *what this book
skips*. Then nothing more is done to the site except version passes and the
corrections readers file.

### The 2026-09-26 morning's brief (superseded the same day)

Thirteen sessions, the fact-check by part with the session as the only
checker, Part XI's figures inside session I, the voice pass dropped on the
reasoning that the rebuilt process would produce the voice. The owner's
instruction that afternoon — the pass is the final fact-check *and* a final
polish over the exact wording — is why Part 4 exists and why the agents and
the second reading are back. The morning's charter paragraph on stability and
its three weights are kept in Part 1 as written.

---

## Part 8 — Session paragraphs

*(newest last; one per session, written by the session at its close)*
