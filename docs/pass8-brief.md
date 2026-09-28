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
  question of fact a reader of an earlier pass asked about this page and no
  session answered (the `[kind=fact]` units of `docs/pass5.md`); (3) every
  caption on the page; (4) the figure gate's notes for the page; (5) the
  page's confident sentences by category; (6) every diagram on the page as a
  numbered list of arrows. Those six are your opening work; the rest of the
  page is the second half. Two things about them the rehearsal on the
  exemplar found: a ledger entry's decompile lines are the release its
  session read (26.2 or earlier), so re-locate each in this tree rather than
  trusting the number; and a confident sentence's line (`L5`) is its
  paragraph's first line, so report the sentence's own line.
- **Another release's tree** (`reference/26.2/`, the sibling project's
  1.21.11) may be opened only to tell whether an error is new; it never
  settles a claim about this page.

### The order of work

1. **The ledger first.** Every entry is a claim a session introduced or a
   correction it made. Report on every one, with the file and line in the
   decompile that settles it, before you read the rest of the page. A
   *correction* is checked as a claim in its own right — confirm the fix, not
   the original — and then check that **the sentence beside it still agrees
   with it**, because a fix that made one sentence true often left the next
   one wrong. Where a later entry overturns an earlier one, the later entry is
   the claim. An entry that quotes a claim is re-derived from the decompile,
   never re-read for plausibility. Then **the readers' questions**, the same
   way: each is a question an earlier reader asked and nobody answered, so
   answer it from the decompile with the file and line, or call it
   *overtaken* with the page line that shows its premise is gone.
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
   lane, or the lane's own inner class; a bare lower-case head that is a word
   rather than a member, *claim* or *load*, is prose on its owner's lane). A
   caption that counts arrows is checked against the arrows one by one. A note or bar naming a tick phase is
   checked against the tick method that runs that phase; a flowchart branch
   against the condition that decides it; a state transition against the code
   that triggers it. One verdict per number. A number you cannot settle is
   *unverifiable*, not silence.
5. **Every count, re-counted.** For each count in the *count* list, name the
   population (the enum, the registry, the class list, the callers) and quote
   how you enumerated it (`grep -c`, the file and lines — call sites, not
   lines), and **say what you counted as one**: comparisons or methods, the
   class's own helpers in or out. The exemplar's spawn-reason count was 11
   or 13 depending on exactly that, and the page's number was right only
   under a definition it never stated. Report the number you got even when it matches. A count of
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
    header is the only version that exists; and **a claim about Mojang's source
    that the decompile cannot see**. The decompile is the compiled game: a
    `static final` primitive or `String` initialized with a literal is a
    compile-time constant, and javac writes its value in at every use site, so
    every such constant looks unread in the decompile whatever the source did.
    A sentence saying such a constant is unread, unused or referenced by
    nothing, or that the code "writes the literal instead of" it, is WRONG — it
    reports the compiler, not the game — and so is anything inferred from it
    (that the two can drift apart, that the constant is dead). Quote the
    declaration's line. A field computed when the class loads, or an object,
    is visible to the decompile and is checked like any other claim.
11. **The completeness question** is not asked in pass 8 (ruling R10: the
    pass adds nothing), and no prompt asks it; skip it.

### What to report

A single markdown report in this shape. Nothing else.

```
## The ledger
- [pass N, session X] — <the entry, shortened> — CONFIRMED | WRONG | UNVERIFIABLE | MISLEADING
  evidence: <path relative to the decompile>:<line>, <what it says in one sentence>
  beside it: <the sentence next to the corrected one, and whether it still agrees>

## The readers' questions
- pass5.md:N — <the question, shortened> — ANSWERED: <the answer in one sentence> | OVERTAKEN
  evidence: <path relative to the decompile>:<line>, or the page line that removed the premise

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
- L<page line> — WRONG | MISLEADING | UNVERIFIABLE — <what the page says> — <what the decompile says> — <file:line> — severity: <what stands and what falls with it>

## Names
Every backticked identifier that is declared somewhere other than where the
page attributes it, or does not exist: <name> — page says <class>, declared in <class> (<file:line>)

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
ledger entries (a bullet names its page itself, or under a `###` sub-heading or
bold lead-in that names it — session A taught `pass8_queue.py` the last two,
which routed 115 entries the planning session's count left page-less), the
readers' questions of fact from the queue, its captions, the figure gate's
notes for it, its confident sentences (`claims.py`) and its diagrams arrow by
arrow (`diagram_arrows.py`).
Beside each, `<part>--<slug>.session.md` for the session alone: the page's
open queue units of every kind, its voice measure with every sentence listed,
and every inbound link by anchor. `_part-notes.md` carries the ledger's and the
queue's part-wide notes, which the session routes by hand; `_part-voice.md`
the part's voice table. The frame session uses `--part frame` and
`--part reference`.

### 3. Launch

One background agent per page, on Opus, in waves of at most twenty (the
harness's ceiling on concurrent agents). The prompt is one line: *Read
`<prompt file>` and do what it says; the page is at `<path>`. Do not edit any
file; return your whole report, in the brief's shape, as your final message.*
Agents here cannot write files, so the session saves each report as
`<scratchpad>/pass8-<part>/<slug>.report.md` when it arrives (session A's
rehearsal). Reports are not committed. One agent per page, never per part — a
part-wide brief hit the spend limit in pass 3.

### 4. Read the part whole while they run

Every page of the part, landing page first, in watch order, in one sitting.
Before opening a single report, write down every sentence that disagrees with
another sentence in the part — a count, a name, an ordering, a direction, an
owner, a thread — and every place a page contradicts its own figure, table or
opening. Then read `_part-notes.md` and decide which page each note belongs to,
or that it is *(no claim)*; a note that names pages only on its continuation
lines is usually several pages' and is checked on each. This list is the
session's own checklist and is worked before the reports are, because it is the
class the reports cannot see. Two things no agent sees are the session's here:
the landing page's generated size and coverage phrases (the agent reads the
`{{#include}}` line, not the number), each read in `src/generated/` and its
population re-derived once from `map_source.py`'s `PARTS`; and every page's
statements about another page, which is where the whole-part read finds what
the agents cannot (session A's read of the exemplar found one: *Ending two*'s
"three clauses decide the whole file" against `chunk-storage`'s list, where
`Player` overrides the method).

### 5. Audit the reports

For every WRONG that changes a trace, a hook, a count in an argument, an
invariant or a caption: **open the decompile yourself before touching the
page.** Pass 3's drafting agents were wrong in about a third of their own
corrections, pass 2's cited methods that do not exist, and the ledger's own
corrections were wrong three times in pass 4's audit. Suspect the tool once
(`verify_names.py`, the generators, the extractors), then the agent once, then
the page. Take the completeness findings on trust; take nothing else on trust.

Pass 7's close found nine of its thirteen ledger entries could not be walked
item by item, and four workarounds bind here ([pass9.md](pass9.md), *Pass 7,
session O*): **captions** claimed and not listed (B, C, D, E, I, J, L) are
read from the page, which is what the prompt's caption list already does; a
**correction with no decompile file** (J's eighteen; C and D's bare `:NNN`; E,
I and N's methods with no line) is usually the figure against its own prose,
and is re-derived from the page first; **G's and H's figure bullets are their
corrections**, since neither wrote a list; and eight **figures called redrawn
with no orderings** — J's `text-and-fonts` f2 and f3 and `input-and-keybinds`
f1, I's `protocol-phases` f2, L's `structure-placement` f1, `terrain` f2 and
`worldgen/README` f1, C's `starting-a-server` f1 — have their orderings
re-derived from the figure, which the agent's arrow list already asks.

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

## Part 4 — The standard (the record: what session A ruled, 2026-09-26)

*The planning session wrote this part as seventeen recommendations with the
numbers behind them. Session A ruled on each — ratified, amended or reversed —
against the exemplar and against the sentences the counts point at, and
rewrote the part as **the record**, in pass 7's Part 3's form: what a part
session applies and why it says what it says. The working form is
`TEMPLATE.md`'s new section, **Voice**, with the three devices it amends (the
number, the 1.21 blockquote, the caption); a session works from there and
reads this for the reasons. Eleven were ratified, five amended, and **one
reversed (V6)**, whose reversal is the session's main finding and a fact, not
a register: it is written into Part 2 as an instruction to every agent. Every
number below was re-measured on 2026-09-26 after V2 (`python
tools/pass8_voice.py --summary`: 19,319 sentences on 137 pages), where the
planning session's were taken before V1 and V2 rewrote 133 pages.*

**What session A did, in one paragraph.** It ruled the seventeen recommendations and added one (V18), wrote them into `TEMPLATE.md` as *Voice* and amended three devices; checked the exemplar under Part 2 and polished it after, and the page three passes had rewritten to their standards turned out to carry **twenty-nine errors**; reversed V6 into a fact every agent now carries, after finding that every constant the book calls unread is one javac writes in at its uses; rehearsed Part 2 on the exemplar and amended it from the agent's own account of where the brief failed it; routed the ledger's 56 frame-level notes (19 to their pages, 21 struck with verdicts) and taught the router the two forms that had kept 115 entries from their pages and 65 from every count; tagged the queue's 75 guessed kinds, which found a sixth kind, the reader's question of fact, and sent it to the agents; and wrote pass 7's ledger-shape workarounds into Part 3 where they bind a session.

### V1. The exemplar — **ratified: `entities/entity-lifecycle`**

**Measured.** The exemplar was checked under Part 2 by its own agent — 111 tool calls, a file and
line for every verdict — and read against Part VI's landing page, `server/server-level-tick` and
`world/chunk-storage`. The page passes 6 and 7 rewrote to their standards carried **twenty-nine
errors**, each re-derived in the tree before it was fixed ([pass9.md](pass9.md), *Pass 8, session
A*): four in its figures and captions (a state diagram missing an edge the code takes, a caption
counting two arrows where its figure has three); two that were an earlier release's shape or a
26.3 change V1 and V2 did not see (the spawn cost is now an environment attribute; `Mob.checkDespawn`
no longer returns early for a persistent mob); a *not dead code* that was dead code (the local cap's
no-player branch); a generated view whose population made the page contradict its own light-rule
paragraph (the spawn reasons); and the section V6 reverses. The agent found all twenty-nine, one
of them incompletely (seven of the eight `Animal` overrides); the session had found two before its
report arrived — the javac constants from the voice counts, and `Entity.shouldBeSaved` by the
whole-part read against `chunk-storage`'s list. Passes 2 and 4 found at least one wrong claim on every page; the exemplar says
that has not changed, and that the part sessions' agents will be busy.

**The ruling:** the exemplar stands, checked and then polished under V2–V17, and it is the page a
part session reads before its own. **The rehearsal of Part 2** amended the brief in seven places,
each from the agent's own *About the brief*: the readers' questions (V18); what a decompile cannot
settle (V6); what counts as one call site, since the spawn-reason count was 11 or 13 by that alone;
a prose message head on its owner's lane; another release's tree for diagnosis only; no
completeness question in this pass; and a severity on every WRONG. It also found the prompt
showing each ledger entry's first line only, and 65 paragraph-form entries no tool counted —
both fixed in `pass8_queue.py`, so every later prompt carries more than the exemplar's first one did.

### V2. The contrast — **ratified**

**Measured.** 56 *not X but Y*, 638 *rather than* and *instead of*. On the
exemplar, nine *rather than*s and no *not X but Y*; read one by one, eight are
the plain way to say a choice or name a belief the reader holds (*a veto
rather than a budget*, beside a cap that is a budget), and one was imprecise
rather than a tic — *bans the category inside the box rather than replacing
its list*, where an empty override *does* replace the list, with nothing.

**The ruling** (`TEMPLATE.md`, *State what is*): a contrast earns its place
where the reader would otherwise believe X — the forum's belief, the 1.21
fact, the obvious reading of a name, the case the page has just stated — and
X is then named as that belief; elsewhere the sentence states Y. The tool's
list is read, not hunted.

### V3. The hedge — **ratified**

**Measured.** 641. The exemplar's nine each have their population in the
sentence or the table beside it (*almost every step … is a rejection*, over a
fourteen-row table that shows it). **The ruling** (*A hedge names its
population*): as recommended; a count that admits two readings says which
once.

### V4. The em-dash chain — **ratified**

**Measured.** 41 sentences with three or more dashes, none on the exemplar.
**The ruling** (*One aside a sentence*): at most one dash pair a sentence.

### V5. The correction in the voice of a correction — **ratified, amended to what it measures**

**Measured.** 156, and **151 of them are *actually*** (*despite the name* 6,
*contrary to* 1, *not what it looks* 1). Read as a set, *actually* is almost
never a correction: it is an intensifier (*the subclass that actually reads
the keyboard*, *what it actually gates*). **The ruling** (*State what is*):
*actually* stays only where the sentence corrects a belief the page or the
sentence has just stated, and goes elsewhere; the rest of the family follows
it. Never in a heading or in link text that quotes a heading: those are
anchors (V15). The exemplar's one — *what the server actually did is smaller
and stranger than it looks*, after a sentence that says a zombie *appears* —
is the sanctioned case and stays, and its heading *Entry: what addFreshEntity
actually does* is an anchor.

### V6. The dead-constant aside — **reversed: the book never says a constant is unread**

**Measured.** The tool's regex finds 20 sentences, about half of them not
about constants at all (*no reader of light ever waits*). Read for the claim
rather than the words, the population is **twenty-odd sentences on sixteen
pages** that say a named constant is unread, *referenced by nothing*, or that
the code "writes the literal instead" — and **every constant they name is a
compile-time constant**: a `static final` primitive or `String` initialized
with a literal, which javac writes in at every use site. The decompile shows
every such constant unread whatever Mojang's source did; the claims report
the compiler, not the game. The exemplar's own section proves it: of
`NaturalSpawner`'s five distance constants, the page said the three *nobody
reads* are `MIN_SPAWN_DISTANCE`, `SPAWN_DISTANCE_CHUNK` and
`SPAWN_DISTANCE_BLOCK` (each `static final int` = a literal) and the two
that *are* read are `MAGIC_NUMBER` and `INSCRIBED_SQUARE_SPAWN_DISTANCE_CHUNK`
(each computed by a method call when the class loads) — the split is exactly
javac's. One page already knew: `client/the-client-loop` says *a decompile can
never tell a documented constant from a dead one*, beside a sentence that
tells one anyway.

**The ruling** (`TEMPLATE.md`, *The decompile is the compiled game*): the book
never says a constant is unread, unused or dead. It gives the number, with the
constant's name where a reader would grep for it (*the thirteen pixels
`Item.MAX_BAR_WIDTH` names*). A field the decompile can see read or not — an
object, a value computed when the class loads — may be called unread only
where that is the page's point. The planning session's recommendation (keep
the name once as *`X.FOO`, which nothing reads*) is reversed, and with it the
exemplar's *Three constants nobody reads*, whose heading was false and is
corrected. **It is a fact, not a register**, so it is also in Part 2's step 10:
an agent that greps for a reader and finds none would otherwise CONFIRM every
one of these.

**For the part sessions — the sentences, by page** (each re-read against its
declaration; the fix is the number with the name, and whatever the sentence
inferred from the missing reader goes with it):

| session | page | the claim |
|---|---|---|
| D | `world/chunk-anatomy`:223 | `LevelChunkSection.BIOME_CONTAINER_BITS`, *no reader of the constant survives* |
| D | `world/chunk-generation-pipeline`:134 | `ChunkStatus.MAX_STRUCTURE_DISTANCE`, *the pyramid writes the literal each time* |
| D | `world/game-events-and-vibrations`:323 | `SculkSensorBlock.ACTIVE_TICKS`, *which nothing reads* |
| D | `world/lighting`:160 | `ThreadedLevelLightEngine.DEFAULT_BATCH_SIZE`, *the test is written as a literal* |
| C | `server/starting-a-server`:311 | `MinecraftServer.SPAWN_POSITION_SEARCH_RADIUS`, *spells it as literals rather than reading it* |
| E | `blocks/block-entities`:292 | `HopperBlockEntity.MOVE_ITEM_SPEED`, *nothing reads it* |
| E | `blocks/pistons-and-block-events`:209, :286 | `PistonStructureResolver.MAX_PUSH_DEPTH` *read nowhere*; `PistonMovingBlockEntity.TICKS_TO_EXTEND`, *no reader survives* |
| F | `entities/synched-entity-data`:282 | `ClientboundSetEntityDataPacket.EOF_MARKER` and `SynchedEntityData.MAX_ID_VALUE`, *referenced by nothing* |
| G | `items/items-and-stacks`:269 | `Item.MAX_BAR_WIDTH`, *spells the number out* |
| G | `items/loot-tables`:305 | `LootTable.RANDOMIZE_SEED`, *nothing in the game reads the constant* |
| H | `player/hunger-and-experience`:60–64, :69–70, :299 | **the bold claim** that no `FoodConstants` field *is referenced by anything* and that the file and the behaviour *can drift apart*; `FoodConstants.EXHAUSTION_WALK` *documents an intent nothing reads*; *the joke* in *Where to look* |
| H | `player/README`:110 | the landing page's summary of the same claim, *because `FoodData` writes each number as a literal instead* |
| H | `player/input-to-movement`:117–121 | *almost none of the thresholds have names*, and `ServerGamePacketListenerImpl.CLIENT_LOADED_TIMEOUT_TIME` *not read by anything* |
| H | `player/the-spear`:213 | `KineticWeapon.HIT_FEEDBACK_TICKS`, *read by nothing* |
| I | `networking/the-connection`:188–189 | `HandlerNames`, *nothing references it* — its drift (*no entry for hackfix*) is visible and stays; its unread-ness is not |
| J | `client/the-client-loop`:116 | `Minecraft.MAX_TICKS_PER_UPDATE`: the page's own javac sentence is the true one; *written as a literal* is not |
| M | `worldgen/density-functions`:302 | three constants *nothing anywhere reads*, *the routers spelling the same numbers as literals* |

A reader's claim that a *literal in the source* is a literal (`networking/protocol-phases`:116,
*below protocol 754 — a literal in the source*) is the same mistake in
the other direction, and I's session reads it too.

### V7. The terminology — **ratified, amended: the spelling half is already met**

**Measured.** `--terms` lists twenty-six glossary headwords spelled two ways,
and read for position, **no page hyphenates a noun**: every hyphenated form is
the compound used as a modifier (*a data-pack field*, *built-in, data-pack,
synced*), which is English. The spelling rule is ratified and needs no sweep.
The senses table is ratified with three rows amended against the pages as
they stand: *the hop* (the sound engine's verified line says *one hop the
sound cannot skip*, and V16 forbids touching a verified line, so the ruling is
that *the hop* unqualified is the packet's and any other crossing names where
it goes); *the shared worker pool* (it is shared — chunk work, meshing and the
reload's prepare phases all run on `Util.backgroundExecutor` — so *shared*
stays where the sentence says with what); and `Registries.X` against
`BuiltInRegistries.X`, whose sentence is already on
`foundations/identifiers-and-registries`:67 (the glossary line is session O's).
The page-local rows — *game time* on the clock page, *batch*, *context*,
*inert* and *lane* on `game-tests`, `contexts-and-predicates`, `enchantments`
and `chunk-storage` — are ratified as the brief wrote them and are those
sessions'. `TEMPLATE.md`'s table carries the corpus-wide rows.

### V8. The possessive on a link — **ratified**

**Measured.** 92 (97 before V2). None on the exemplar. **The ruling** (*The
possessive never hangs on a link*): as recommended.

### V9. The number device — **ratified, amended: the device changes now, the twenty-four in their parts**

**Measured.** 24, one to two a part, none on the exemplar. Six already carry
their noun in the bold (*One millisecond*, *Sixty-four blocks*) and read
cleanly; the eighteen bare numbers are the fault. **The ruling:**
`TEMPLATE.md`'s device is amended — the number and the noun it counts are one
bold phrase and the sentence runs on from it (`**Two writes** to the socket
per client per tick: …`). The twenty-four are rewritten by their part sessions
in step 7, not here: each is a count the fact-check reads first, and a
rewrite that restates a count is a claim.

### V10. The counts that rot — **ratified, amended: a size, not a population**

**Measured.** 147 by the tool, which cannot tell a size (*102 classes*, *573
lines*) from a population (*seven classes override it*). The exemplar's two
are populations — how many classes override `Mob.getMaxSpawnClusterSize`, how
many override `LevelWriter.addFreshEntity` — and are facts the agent
re-counts, not sizes that rot. **The ruling** (*Counts say what they count, and
sizes rot*): a size in prose comes from a generated include or gives way to
the atlas link unless it is the page's argument; a population stays and is
re-counted.

### V11. The long sentence — **ratified**

**Measured.** 1,227 over forty-five words; 17 on the exemplar, of which none
hid a step of reasoning. **The ruling:** no rule on length (*Long sentences
are a place to look*).

### V12. The figures' register — **ratified, amended: at most two sentences**

**Measured.** 204 captions: **63 are one sentence, 102 two, 37 three, 2
four** — the one-sentence form the recommendation (and pass 7's F5) asked for
is what the corpus did least, and the exemplar's own four run two, three, two
and two. The two-sentence caption is the job done: what the picture shows,
then what to look for. A handful point at their own figure (*so the figure asks …*); the
*above* and *below* the tool counts (41) are almost all a later figure or
section and are fine. **The ruling** (`TEMPLATE.md`, *Figures*): a caption is
at most two sentences in the present tense, one italic run, the first saying
what the picture shows (its shape first where the shape is the point) and the
second what to look for; it never points at its own figure. The thirty-nine
of three or more are cut to two by their part sessions. The figure-label and
gate-note half of the recommendation is ratified as written, and Part XI's
missing captions are session K's.

### V13. The 1.21 blockquote — **ratified**

**Measured.** 55 blockquotes, every one opening in the one spelling; **13 run
past eight lines**, nine of them Part XI's (`entity-rendering` 15,
`lightmap-fog-and-sky` 14, `models-and-atlases` 19, `particles` 13,
`post-processing` 15, `section-meshing` 12, `the-frame` 13,
`visibility-and-the-frame-graph` 15, `block-entity-rendering` 9), two Part X's
(`gui-and-screens` 9, `text-and-fonts` 10), one Part VI's (`ai-goals-and-brains`
9) and one Part II's (`identifiers-and-registries` 9). The exemplar has none,
correctly: nothing on it moved in a way a 1.21 reader would hunt for.
**The ruling** (`TEMPLATE.md`, the device): the recommended form, and 26.3's
drift goes in the same blockquote and nowhere else on the page.

### V14. The second person — **ratified: A1 stands**

**Measured.** 43 pages open on *you*. No change.

### V15. Headings are anchors — **ratified, and exercised**

The exemplar's *Three constants nobody reads* was false (V6), so it was
corrected as the ruling says a false heading is: `check_links.py --inbound`
first (no link lands on it), then the new heading, which says what the section
now says.

### V16. What the polish never does — **ratified**

### V17. Every polished sentence is a claim — **ratified**

### V18. The reader's question of fact — **new**

Reading the queue's seventy-five guessed units found eleven that are neither a
lens nor a record: a question of fact a reader of an earlier pass asked and no
session answered (*does the autosave floor break the five-minute claim?*, *does
the shadow colour inherit?*, the exemplar's own *two biomes and four types*).
They had been guessed *voice* or *book*, and the session file is the only place
a queue unit reached — so nobody with the decompile open was ever asked them.
**The ruling:** they are tagged `[kind=fact]`, a sixth kind that is pass 8's;
`pass8_prompts.py` puts a page's in its agent prompt beside the ledger, and
Part 2 asks the agent to answer each or call it overtaken.

---

## Part 5 — The rulings (standing; session A adds to them and never removes one)

- **R1 · Truth first, then plainness.** A change in this pass is one of: a
  false claim made true; a false arrow redrawn; a frame page made accurate; a
  ledger entry struck; a queue unit settled or ruled; a sentence polished
  under Part 4 as ratified. Anything else is out of scope, however small.
- **R2 · The whole-part read is not optional.** It is step 4 of every part
  session, and its findings are logged even when the ledger is empty for the
  page, because that is where passes 5 and 6 found half their corrections.
- **R3 · The ledger closes on itself.** Every one of the 1,398 entries (1,333
  by the planning session's count; session A's router found 65 paragraph-form
  entries it missed) is struck by the close, each with its verdict (`python tools/pass8_queue.py
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
| **V1** | **the version pass, mechanical.** `python tools/version_pass.py 26.3` has run (the tree is at `reference/26.3/`; run it again and it skips what is present); `git tag pass-8-start` before any page changes; `python tools/version_pass.py 26.3 --flip` and `python tools/mc_version.py`; `map_source.py`'s `PARTS` given `com/mojang/renderpearl` (Part XI) and read against 26.3's new packages (`level/blockscan`, `item/slot`, `attribute/modifier`); `python tools/map_source.py`, `gen_reference.py all`, `pass5_coverage.py --write`, `check_deps.py --write-figure`, and **the diff of `src/generated/` read** — a population that moved is a page that changed; `verify_names.py` and `check_figure_names.py --strict`: every rename resolved to the 26.3 name with the smallest edit, every removed name replaced by what does its work or the sentence cut, on the sixty pages outside V2's five; `claims.py --counts` over the touched pages; the header line on every page, `CLAUDE.md`, `README.md`, the introduction, `book.toml`, the issue template's placeholder, `fetch_libs.sh`'s defaults; the gates; deploy; every change logged in [pass9.md](pass9.md) under *Pass 8, session V1*, and every section whose *mechanism* changed listed for V2 or the part session | 517 names on 65 pages; 32 in figures | — | — | — | done 2026-09-26 | The tools read 26.3 and check each page against the release its own header names, so the site deployed with every header true: **91 pages moved to 26.3** (71 corrections, every finding re-derived; four history claims found false against the 1.21.11 tree; one heading corrected) and **42 left at 26.2 for V2**, with what changed under each in the ledger. Found on the way: the planning session's staging had dropped every `@Override` (26.3 re-decompiled with McDeob's own options), two generator bugs, and a release far larger than 517 names — SDL3 in place of GLFW, the reloadable registries, the swing and dig packets, entity movement sync |
| **V2** | **the version pass, the systems that changed shape — the scope V1 set (2026-09-26): the 42 pages still verified against 26.2**, listed by system in [pass9.md](pass9.md) under *Pass 8, session V1*, *For session V2*, with what 26.3 does instead under each: world generation (the brief's four plus `features-and-placement`, `blending`, `biomes`, `structure-placement`, `trees`, Part XII's landing page), the reloadable registries (`identifiers-and-registries`, `resource-system`, `contexts-and-predicates`, `recipes`, `loot-tables`, `advancements`, Part VII's landing page, and the brief's two codec pages), the swing and the dig (`the-sword-swing`, `using-an-item`, `block-breaking`, `particles`), the window and the renderer (SDL3, `renderpearl`, OIT: `blaze3d`, Part XI's landing page, `the-window`, `the-frame`, `post-processing`, `visibility-and-the-frame-graph`, `lightmap-fog-and-sky`, `block-entity-rendering`, `submit-phases`, `the-client-loop`, `input-and-keybinds`), the singleplayer seam (`anatomy`, `permissions`), `packets-and-stream-codecs`, `items-and-stacks`, `chunk-storage`, `signal-and-dust`, `density-function-nodes` (hand-kept, not generated), and the summarisers (`glossary`, `what-this-book-skips`), read last. `python tools/verify_names.py --current` passes when none is left. The brief's original list, for the record: `worldgen/terrain`, `worldgen/density-functions`, `world/chunk-generation-pipeline` (the status ladder without `CARVERS` and `SURFACE`; the surface rules and carvers gone or moved), `rendering/blaze3d` and Part XI's landing page (`renderpearl`: `api`, `backend`, `frontend`, `util`), `foundations/codecs-nbt-json` and `data-driven-types` (the registry codecs), `world/chunk-storage` (`level/storage`), `blocks/signal-and-dust` (`RedStoneWireBlock`), `player/the-sword-swing` and the introduction (`ServerboundSwingPacket`), `items/using-an-item` (`ItemInHandRenderer`), `reference/density-function-nodes` regenerated and its prose re-read. Each page made true of 26.3 with the decompile open, figures included, in the smallest rewrite; what the part session must re-read deeper is written into the ledger under *Pass 8, session V2*; the 1.21 blockquotes gain the 26.3 drift where a reader would hunt for the old name (V13); `naming-drift` gains the rows. Gates, deploy, the paragraph | 42 pages; 455 names and 30 in figures still unresolved against 26.3 | — | — | — | done 2026-09-26 | **Every page says 26.3** and `verify_names.py --current` passes: the forty-two pages rewritten in one session (the owner set no split), one agent per page with every diff audited — 681 ledger entries, sixteen false headings corrected with their links, the lane key's removed classes replaced, sixty-four naming-drift rows. Found beyond V1's list: eight more 26.3 changes on pages V1 had moved (the hurt cooldown, `LocalPlayer.sendChanges`, `MoveSimulationType` among them), and two probable upstream bugs, written as what the code does (blending's carving filter, the delayed dig) |
| **A** | **the standard.** Part 4 ruled against the exemplar (`entities/entity-lifecycle`: its own agent under Part 2, its polish under V2–V17), the rulings written into `TEMPLATE.md` as *Voice* and the device amended (V9), Part 4 rewritten as the record; the ledger's 56 frame-level notes (`pass8_queue.py --part Frame`) struck *(no claim)* or routed to a page; pass 7's close's audit of the ledger's shape ([pass9.md](pass9.md), session O's entry) read and its workarounds written into Part 3 where they bind a session; the queue's routing tags checked (`pass5_queue.py --unsure`) so that R8's count is honest; Part 2 rehearsed on the exemplar and amended if the report's shape failed it | 56 | — | 3·2·1·0 | 5.2k | done 2026-09-26 | Part 4 ruled (11 ratified, 5 amended, V6 reversed, V18 new) and written into `TEMPLATE.md` as *Voice*; **the exemplar carried twenty-nine errors**, all fixed and re-derived; the book's *constant nobody reads* asides found to be javac's inlining, listed by page for the part sessions and written into Part 2; Part 2 amended in seven places from the rehearsal; the router taught two page forms and paragraph entries (the ledger is 1,398 entries); the queue's 75 guesses tagged, a sixth kind (*fact*) sent to the agents |
| **B** | I · Anatomy, II · Foundations and the Maps | 25+3 · 61 · 24 | 4·2·3·9 / 3·0·0·13 / maps in frame | 14·18·2·2 / 29·34·7·6 | 32.5k | done 2026-09-26 | **293 corrections on sixteen pages** two fact-checks had passed, every one re-derived in the tree (54 inside a figure or a caption, nine of them 26.3 changes V1 and V2 missed); the 115 ledger entries struck, 36 wrong in whole or in part; 44 queue units settled; the queue router's part numerals fixed; the record's own audit found eight more errors beside the session's corrections; items handed to G, L, O and P |
| **C** | III · The server | 81+3 | 6·1·1·22 | 28·34·5·11 | 20.9k | done 2026-09-26 | **176 corrections on six pages** (22 inside a figure or a caption, nine of them 26.3 changes V1 missed), every one re-derived in the tree; the 84 ledger entries struck, 41 of 83 wrong in whole or in part; 31 queue units settled; the record drafted by one agent per page and audited, which found **38 more errors, 15 of them in sentences the session had just written**; three probable upstream bugs written as mechanism (a relayed crash that skips the flush save, a lapsed ban's first login, the spawn search's stride); items handed to D, F, I, M, N and O |
| **D** | IV · The world | 88+8 | 5·5·0·25 | 51·52·17·9 | 38.8k | done 2026-09-27 | **284 corrections on eleven pages** (43 inside a figure or a caption, seven of them 26.3 changes V1 and V2 missed), every one re-derived in the tree; the 114 ledger entries struck, 27 of 111 wrong in whole or in part; 47 queue units settled; the record audited by one agent per page, which found **76 of the errors, 55 of them in sentences the session had just written**; one probable upstream bug written as mechanism (lava's slower spread, booked and then dropped as a duplicate); four pages in other parts corrected with it; items handed to E, F, I, J, L, M and O |
| **E** | V · Blocks | 48+52 | 10·0·1·28 | 32·34·9·4 | 24.3k | done 2026-09-27 | **237 corrections on eight pages** (29 inside a figure or a caption; four 26.3 changes V1 and V2 missed, and three sentences the version pass left beside a fact it moved), every one re-derived in the tree; the 112 ledger entries struck; Part V's queue closed; the record audited by one agent per page, which found **73 of them, 45 in sentences the session had just written**; the write figure redrawn (D's handoff); sculk spread and four more unowned mechanisms into pass3.md §7; eight pages outside the part corrected with it; items handed to J, L, N, O and P |
| **F** | VI · Entities | 95+3 | 7·4·0·24 | 55·56·15·9 | 33.8k | done 2026-09-27 | **307 corrections on ten pages** (44 inside a figure or a caption, twenty-one of them 26.3 changes V1 and V2 did not carry into the sentence), every one re-derived in the tree; the 109 ledger entries struck, 19 of 83 claims wrong in whole or in part; 43 queue units struck and eleven shared ones noted; the record audited by one agent per page, which found **80 of them, 54 in sentences the session had just written**; `authority`'s predicate figure redrawn for 26.3's move-simulation type (V2's handoff); seven pages outside the part corrected with it; items handed to H, I, J, O and P |
| **G** | VII · Items and inventories | 74+2 | 2·4·0·21 | 53·56·14·1 | 29.8k | done 2026-09-28 | **255 corrections on nine pages** (31 inside a figure or a caption; two 26.3 changes the version pass did not reach; six false headings, four of them on `enchantments`), every one re-derived in the tree; the 77 ledger entries struck, 4 wrong or wrong in part; the part's queue settled; the record audited by one agent per page, which found **71 of them, 45 in sentences the session had just written**; every caption's doubled *Figure:* gone; one probable upstream bug written as mechanism (a thrown click leaves remote updates suppressed); four pages outside the part corrected with it; items handed to H, I, J, N, O and P |
| **H** | VIII · The player | 84+12 | 5·1·0·21 | 29·27·9·8 | 20.1k | done 2026-09-28 | **241 corrections on eight pages** (19 inside a figure or a caption; five 26.3 changes the version pass did not reach — phase one's `Entity.commonTick`, the hurt cooldown on the two-phase tick, `ServerGamePacketListenerImpl.handlePlayerPositionChange`, the teleport acknowledgement's position, the per-client-tick position kick), every one re-derived in the tree; the 96 ledger entries struck, 8 wrong in whole or in part; the part's queue settled (34 struck, seven shared units noted); one false heading (the food bar's *pile of literals*, V6); the record audited by one agent per page, which found **50 of them, 44 in sentences the session had just written**; four pages outside the part corrected with it; items handed to I, J, L, N, O and P |
| **I** | IX · Networking | 73+30 | 6·1·0·16 | 30·43·12·13 | 21.7k | done 2026-09-28 | **220 corrections on six pages** (15 inside a figure or a caption; `the-connection`'s lead figure redrawn, the swing's answer going to the players watching and never back to the swinger; its false heading on `Connection.tick` corrected twice with its two links), every one re-derived in the tree; the 103 ledger entries struck, 39 wrong in whole or in part or beside a wrong sentence; the part's queue settled; the record audited by one agent per page, which found **71 of them, 52 in sentences the session had just written** — about one in three; two queue-router bugs fixed; three pages outside the part corrected with it; items handed to N, O and P |
| **J** | X · The client — the largest ledger; may split at the GUI stack (pages 1–5, 6–12) | 118+17 | 6·3·4·27 | 59·71·10·9 | 29.6k | — | |
| **K** | XI · Rendering, **the figures** — pass 7's session K: its runbook, its viewer brief, its gate; the part's 20 figures rendered and read against their sections; the 19 captions written; the three eight-lane traces split or folded; the 17 figure-kind queue units; recorded in [pass7-brief.md](pass7-brief.md) Part 4 as well as here | — | ·   ·17·   | — | — | — | |
| **L** | XI · Rendering — the check and the polish, after K | 82+8 | 1·5·0·25 | 82·72·21·21 | 35.7k | — | |
| **M** | XII · World generation — the part V2 rewrote most; its agents read V2's ledger entries first | 77 | 6·1·0·18 | 69·61·19·2 | 30.7k | — | |
| **N** | XIII · Commands and data packs | 72+24 | 6·7·1·22 | 39·38·14·0 | 25.6k | — | |
| **O** | **Reference and the frame** — the introduction, `lectures.md`, the atlas's prose, `reference/README` and the hand-kept Reference pages, read *after* the parts (the summarisers are read last); the glossary against every owner page; `what-this-book-skips` and every *where the part stops* against [pass3.md](pass3.md) §7; and the eleven generated Reference views, which no other row names (session A's routing, 2026-09-26): each generator's typed prose in `gen_reference.py` read against the tree — V2 found two stale — and one population per view re-derived | 85 · 28+56 | 18·8·1·49 | 43·38·7·2 / 17·12·1·0 | 55k + 9k | — | |
| **P** | **the second reading.** `python tools/pass8_diff.py` — every sentence changed since `pass-8-start`, by page, read against the decompile by a session that changed none of them; the ledger's *Polished* sections read against the pages; thirty strikes and thirty corrections audited (R4); `pass8_queue.py --unstruck` and `pass5_queue.py --summary` at zero, or the gaps listed for Q | — | — | — | — | — | |
| **Q** | **the release.** `version_pass.py --latest` (R6; if 26.4 has shipped, a version session runs first and Q waits); the introduction's *verified* paragraph made true of every gate; the pass-number sweep of `README.md`, `CLAUDE.md`, `TEMPLATE.md` and the frame pages (R5); the lecture order as the owner confirmed it; the maintenance note in `README.md` and [plan.md](plan.md) — what is true of the site while nobody works on it, what a release triggers, how a reader's correction arrives and who answers it; `README.md`'s corrections paragraph rewritten for a site with no current pass; the tag `release-26.3`; deploy; pass 8 archived whole into this file's Part 8 and [plan.md](plan.md) closed with the verdict on whether the pass earned its cost | — | — | — | — | — | |

**The owner's part.** Two things only the owner does: confirm the lecture
order in `src/lectures.md` before session Q (a read of the lecture map and a
yes, or a reordering); and the
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

**Session V1 — the version, mechanical (2026-09-26).** The tools read 26.3, and **each page is now checked
against the release its own verified line names** (`reference/<version>`, with that release's pinned
libraries), so a version pass moves the book a page at a time with every header true; `--current` on the
gates is the release's test. Ninety-one pages say 26.3 — seventy-one corrections in them, each re-derived
against the tree, plus the frame, the atlas and the Reference landing page — and forty-two say 26.2, checked
against 26.2, for V2. Ledger entries checked: none (V1 strikes nothing; its 121 entries are session P's).
The three worst corrections: `the-connection`'s opening hook named a packet 26.3 no longer has
(`ServerboundSwingPacket`; the client now sends a field-less `ServerboundPunchPacket` and the server
broadcasts `ClientboundSwingAnimationPacket`); `data-components` said axes, shovels and hoes still exist as
classes (they are the data-driven `DataComponents.BLOCK_TRANSFORMER`); and the atlas's fan-in hook, which
rested on the codec vocabulary's ranks and on `Minecraft` being the one client-only class in the thirty
(`Holder` climbed; `Minecraft` fell to thirty-first). What the research found that the brief's plan did
not: **26.3 is much larger than its 517 names** — the name gate cannot see a mechanism change whose names
survive, and five agents over the tree found forty-two pages where the smallest true edit is a paragraph, a
section or a figure (SDL3 in place of GLFW; order-independent transparency; the reloadable registries; the
swing and dig packets; entity movement sync; a world-generation rewrite deeper than the carvers). Four
history claims ("the class 26.2 put in the middle", "the two 26.2 arrivals", "renamed to match in 26.2", "the
26.2 combat change") were false against the sibling project's 1.21.11 tree, one of them a heading, corrected
with its two links. Also found and fixed: the planning session's 26.3 staging had run the decompiler without
McDeob's options and dropped all 16,652 `@Override`s, shrinking every line count for no game reason (the tree
is re-staged, 71.5% of shared files byte-identical to 26.2); the registries view had silently dropped to "1
data-pack registry" and the spawn-override view had crashed and left its page empty. Left for V2: the
forty-two pages, by system, in the ledger. Left for the part sessions: the entity movement-sync rework
(F, I, J) and the other items under *For the part sessions*. **The owner's decision** the brief anticipated
is now about forty-two pages, not five: V2 as one session, split by system, or some pages declared in their
1.21 blockquotes and left at 26.2 until the return (the per-page gate makes that honest).

**Session V2 — the version, the systems that changed shape (2026-09-26).** The owner's instruction named the
session and set no split, so all forty-two pages ran in one: **every page now says 26.3**, and `verify_names.py
--current` passes. One background agent per page — the thirty-seven system and Reference pages first, then the
three landing pages, the glossary and `what-this-book-skips` after the pages they summarise — each given V2's
brief, its lines from V1's list as claims to check, its names that no longer resolved, and a page map (every
class the page names, and whether 26.3 left its file identical, changed, moved or gone). The agents edited
their pages; the session read every diff and re-derived each page's load-bearing claims in the tree before
accepting it, and fixed what failed it (one redrawn figure at 10.3px, now 12.1). 681 ledger entries under
*Pass 8, session V2*; ledger entries checked: none struck (V2's entries are session P's to read). The three
worst corrections: `world/chunk-generation-pipeline` and `worldgen/terrain` taught three chunk statuses 26.3
removed (*noise*, *surface*, *carvers*; one *terrain* task does their work), so the ladder, three figures and
three headings were false; `worldgen/density-functions` taught a rewrite that installs six caches, where 26.3
compiles the graph once per dimension into samplers with one kind of cache (`DensityFunctionCompiler`); and
`rendering/the-window` taught GLFW's six callbacks, where 26.3's SDL3 window polls nineteen event kinds (four
headings). What the agents found that V1's research did not: **eight more 26.3 changes
on pages V1 had already moved**, every one with names that still resolve (the hurt cooldown is
`LivingEntity.damageCooldownTime`; the client's movement leaves from `LocalPlayer.sendChanges`; which side
simulates an entity is its `MoveSimulationType`; the feature dispatcher's eight drains; the atlas count; the
first-person hand; two generators' typed prose), which is why [plan.md](plan.md)'s version pass now designs
the per-page class map for the next planning session. And **two probable upstream bugs**, written on their
pages as what the code does: beside a chunk an older version generated, 26.3 keeps carving only near the old
ground (`worldgen/blending`), and the delayed dig passes its start tick where an elapsed count is expected, so
a block flickers back for a tick (`blocks/block-breaking`). Left for the part sessions: each entry's closing
note; four 1.21 blockquotes now past eight lines (L); `entities/authority`'s figure, which still draws
`Player`'s answer as a branch (F); the glossary's entries settled while their owners were being rewritten (O).
Left for session K: three Part XI figures still under 11px, none of them V2's drawing (`entity-rendering` f2
and `lightmap-fog-and-sky` f1, eight lanes each, and `models-and-atlases` f1, a flowchart 1,743px wide).

**Session A — the standard (2026-09-26).** Part 4 is now the record: eleven recommendations ratified,
five amended to what their counts actually measure, one reversed and one added, all written into
`TEMPLATE.md` as *Voice* with the number device, the 1.21 blockquote and the caption amended. The
exemplar was checked first, by its own agent under Part 2 and by a read of Part VI's landing page and
the two pages that restate its mechanics, and **the page passes 6 and 7 had rewritten to their
standards carried twenty-nine errors**, every one re-derived and fixed. Ledger entries checked: the
exemplar's 25 and two Reference entries that state its numbers (11 confirmed, 2 overtaken, 1 no claim,
13 confirmed only in part or wrong), and the 56 frame-level notes (19 routed to their pages, 21 struck, one of whose
claims — that three saved-data classes were queued in pass3.md §7 — was false and is now true). The
three worst corrections: the local mob cap's no-player branch was called live because *near* meant two
things, where it is one test over the same players in the same tick; the visibility state diagram
drew *up is one step at a time* and the page read an asymmetry off it, where a chunk promoted straight
to entity-ticking takes its sections from hidden to ticking in one call; and the spawn-reason counts
(eleven tested, eight labels) came from a generator that did not count `EntitySpawnReason`'s own
helpers, so the page called `TRIAL_SPAWNER` a label a paragraph after saying the light rule exempts
it. **The finding that reaches past the exemplar** is V6's: every constant the book calls unread —
about twenty sentences on sixteen pages, one of them a bold claim on `player/hunger-and-experience`
and its landing page — is a compile-time constant javac writes in at every use, so the decompile
cannot show whether anything reads it; the ruling is reversed, the sentences are listed by page in
Part 4 for sessions C to M, and Part 2's step 10 now tells every agent, which would otherwise have
confirmed each one. What the whole-part read found that the report did not: nothing the report
missed, but it found `Entity.shouldBeSaved`'s false absolute from `chunk-storage`'s list before the
report arrived, which is the method working. The rehearsal of Part 2 went as the charter hoped: the
agent's own account of where the brief failed it gave seven amendments, and two tool defects — the
prompt showed each ledger entry's first line only, and 65 entries written as paragraphs were counted
by nothing, so the ledger is 1,398 entries, not 1,333. The queue's 75 guessed kinds were tagged,
which found eleven questions of fact nobody with the decompile had been asked; they are a sixth kind
now and go to the agents. The polish on the exemplar changed five sentences whose meaning could move
(listed in the ledger) and one caption's length. Also corrected: one landing page count
(`entities/README`, six labels, not eight) and one generator (`gen_reference.py`'s spawn reasons). Left
for the part sessions: V6's list, V9's twenty-four number devices, V12's thirty-nine long captions,
V13's thirteen long blockquotes (nine of them L's), and the other rulings as each page is polished;
for session O, the eleven generated views, which no row had. Left for session P: session A's 46 ledger
items, and the exemplar's diff.

**Session B — Parts I · Anatomy and II · Foundations, and the Maps (2026-09-26).** Sixteen pages, each checked
under Part 2 by its own agent while the session read each part whole; every prompt carried the page's pass 5–7
ledger entries and, added by hand because `pass8_prompts.py` leaves pass 8's out, V1's and V2's as claims to
check. **293 corrections** — the atlas 45, Part I 61, Part II 185, `reference/README` 2 — each re-derived in the
tree before it was made; 54 are inside a figure or a caption. Ledger entries checked: the 115 pass 5–7 entries
on these pages (61 checked, 35 checked except a part, 1 wrong, 12 overtaken, 6 no claim), and the 106 V1 and V2
entries as claims in the prompts, whose strikes are session P's. The three worst corrections: `foundations/tags`
answered its own hook wrongly — the tag swap was *safe because one thread runs it start to finish with nothing
else looking*, where worldgen reads tags on the worker pool during a `/reload` and the Render thread reads the
same holders in singleplayer, and what makes it safe is that each step is one reference write of an immutable
collection; `anatomy/anatomy` rested its packet rule on *nothing on the client writes server world state*, where
the options screen's direct calls set a player's game mode on the integrated server, and a switch to spectator
respawns the shoulder parrots and dismounts the player; and `foundations/text-components`' caption had
`Style.applyTo` merge a parent's style over a child's, the inverse of the code and of the page's own prose. What
the whole-part read found that the reports did not: eight corrections, marked *(the session's)* in the ledger —
among them the Foundations landing page's *type line at the top of most JSON files* (fewer than half have one), a
figure's forward-reference pair drawn as a biome and a carver where no carver names a biome, and the Reference
landing page's lanes row still counting nine. **The record's audit found eight more**: six agents drafted the
ledger entry from the diff and the reports, the session read it against both, and every one of the eight was a
sentence the session had written or left beside a correction — a figure still drawing the claim the prose had
corrected, a cast cell the body's correction had not reached, a caption beside a fixed paragraph. That is pass
6's finding, *a sentence that disagrees with the text beside it*, made by the session correcting it; a part
session should read its corrections' neighbours before it writes the record. Nine corrections are 26.3 changes
V1 and V2 did not see: five on `tags` (the reloadable registries' tags, the unused void overload,
*poplar_logs*, the fuel table, configured features), three on `data-components` (`Removed.INSTANCE`, twenty-six
deferred call sites, eleven common components) and the atlas's `package-info` count. The polish: twenty-one
sentences whose meaning could move, each quoted in the ledger with its evidence (captions cut to two sentences,
*client thread* made *Render thread*, and eight queue units settled by a clause — the Netty gloss, *blank lines
included*, the wire id's teaser and the shadow colour's inheritance among them), and by kind possessive on a link
8, *actually* cut 6, em-dash chain 4, caption cut to two sentences 4, number device 3. Also corrected: the queue
router's part numerals (every part-wide unit under *Part VII · Items* had also routed to Part I, and a plural
heading reached only its first part), the atlas trees' titles, the lanes index's intro and a `map_source.py`
comment. Left for session G: `items/containers-and-menus`' *the one write whose answer does not wait for a
phase* (a slot click, pick-block and the creative slot broadcast inside their handlers too). For L:
`rendering/models-and-atlases`' *baking overlap stitching* (loading overlaps it; baking waits on it). For O: two
thread names missing from `reference/threads`; `reference/README`'s generated views that *re-derive* rather than
re-read; `reference/components`' header and *synced* column, which mark seven types unsynced that go over the
wire as NBT; and two descendant counts `map_source.py` trades between a pair of interfaces. For P: the 106 V1 and
V2 entries, and V1's *1,218* items (the count of `Items`' fields; 1,658 items are registered). Written on its page
as mechanism, one probable upstream bug: the component reverse index keeps its answers across a `/reload`
(`foundations/data-components`).

**Session C — Part III · The server (2026-09-26).** Six pages, each checked under Part 2 by its own agent while
the session read the part whole; the prompts carried the pages' pass 5–7 ledger entries and, by hand, V1's one
entry here and session A's V6 item. **176 corrections**, every one re-derived in `reference/26.3` before it was
made; 22 are inside a figure or a caption, and nine are 26.3 changes V1 did not see (the command-suggestion
handler no longer hops, so `server-tick`'s *fifty-two of sixty-one* is fifty-one of sixty-one and the listener's
tick does four things, not three; `RandomState.garbageCollect` is the level tick's new last step;
`Entity.commonTick` does what `ServerLevel.tickNonPassenger` used to; falling sand sends a second packet; loot
tables, recipes and advancements load as reloadable registries at boot; the spawn origin comes from
`ChunkGenerator.getOrigin`). Ledger entries checked: the 84 on these pages (40 checked, 37 checked except a
part, 4 wrong, 2 overtaken, 1 no claim — 41 of the 83 that made a claim wrong in whole or in part). The three
worst corrections: `how-a-server-dies` taught that *a crash saves your world* for every crash, where a crash
relayed from a worker thread is never cleared, is thrown again by the shutdown's own drain, and ends the
teardown before the flush save — no entities, `level.dat` or saved data (a probable upstream bug, the same in
26.2) — and its list of what crashes a tick named commands and packet handlers, both of which are caught;
`starting-a-server` ran boot on *the JVM main thread*, where `java -jar server.jar` opens a bundler that unpacks
the libraries and starts `Main.main` on a thread named *ServerMain*, a fact the decompile cannot show (read from
the jar); and `server-level-tick`'s closer answered *why does a mob that spawns this tick not move until the
next one?* with a mechanism that does not apply, since a natural spawn is added before the entity walk and
ticks at once. What the whole-part read found that the reports did not: three, one of them a contradiction
between pages (the level's packets leaving *at the end of the server tick*, where `server-tick` has them in the
connection phase's flush); it also found, before the reports, four cross-page errors the reports then shared
(`how-a-server-dies`' crash causes against `server-tick`'s suppressed handler errors, `/stop`'s tick
*finishing its entities*, `server-tick`'s *submits and waits* that session B had fixed on `anatomy`, and the
level tick's command timing against `server-tick`'s commands-as-tasks). **The record's audit is this session's
finding**: one agent per page re-derived every changed sentence and read its neighbours and the corpus, and
found 38 more errors, 15 of them in sentences the session had just written (a credits screen with a
*Respawn* button it does not have, a lapsed-ban player shown a message the login protocol cannot carry, a
relayed crash said to leave the chunks unwritten when the drain's first pass writes them, the login
authenticator listed as non-daemon, the landing page's new sentence naming the very class it said no page
names) and 23 beside a correction it had not reached. Session B's lesson held at five times B's rate: a
correcting session's own new sentences carry errors, and a second agent reading them against the tree finds
them. The polish: the three bare number devices (V9), eleven possessives on a link, one em-dash chain, one
*actually*, *ledger* and *door* and *border* each kept to one sense, three one-clause glosses, and every caption
at most two sentences; each sentence whose meaning could move is quoted in the ledger. Also corrected:
`reference/threads` (the handler count, the dedicated server's boot thread, RCON's conditions) and
`TEMPLATE.md`'s `Main` lane row; `ServerEntityGetter` and nine other unnamed classes queued in pass3.md §7. Left
for D, F, I, M, N and O: the fourteen sentences on other parts' pages that repeat a claim corrected here, listed
in the ledger's *For later sessions*. For P: V1's entry on `starting-a-server`, and this session's diff.

**Session D — Part IV · The world (2026-09-27).** Eleven pages, each checked under Part 2 by its own agent while
the session read the part whole; the prompts carried the pages' pass 5–7 ledger entries and, by hand, the V1 and
V2 entries on these pages, session C's four handoffs and session A's four V6 constants. **284 corrections**,
every one re-derived in `reference/26.3` before it was made; 43 are inside a figure or a caption, seven are 26.3
changes V1 and V2 did not see (a fourth attribute flag and the new mob-spawn settings type; a generating region
that now reads the place, where the page had it answering every attribute with its default; thirteen attributes
over sixty-seven biome files; the heightmaps' block tags; `AttributeType.toInt`; the Nether's fifteenth
attribute), and four are sentences the version pass moved the fact under and left (*twelve statuses* twice,
*forty-six*, and V2's *five of the ten*, which is six). Ledger entries checked: the 114 on these pages (83
checked, 24 checked except a part, 3 wrong, 1 overtaken, 3 no claim — 27 of the 111 that made a claim wrong in
whole or in part). The three worst corrections: `game-events-and-vibrations`' bold hook, *the sensor always hears
you at least one tick late by design*, which is true of a mob and false of a player, whose movement packet is
handled before the level tick moves the clock on, so the sensor chooses a player's footstep in the same server
tick; `tickets-and-loading`'s bold *nothing is ever sent that the server is not also simulating*, where a chunk
becomes sendable on the loading graph and ticks on the simulation graph, so past simulation distance a player is
sent chunks that do nothing (the page's own hook, which the bold sentence contradicted); and
`chunk-generation-pipeline`'s closer, *why does adding cores not speed up world generation?*, answered as if
nothing ran in parallel, where the biome fill and the terrain job fork onto the worker pool and run many chunks
at once. What the whole-part read found before the reports: thirteen sentences that disagreed with another
sentence in the part (two left by the version pass, two owners for the warden's brain, the key's thread names
spelled six ways), every one now corrected. **The record's audit was again the session's
finding**: one agent per page re-derived every changed sentence against the record and read its neighbours and
the corpus, and found **76 of the 284, 55 of them in sentences this session had just written** (the new hook's
figure still drawing a refusal for a player; a spectator said to load nothing, where every joining player's
spawn ticket loads chunks before its game mode exists; an autosave said to wait for the disk only on a flush,
where it writes `level.dat` and every player's file on the Server thread; the torch said to light a tick late
for a player at the edge, where every client lights it when the block arrives and only the server's light comes
later). C's lesson held at a higher rate than C's: a part session's own corrections carry about one error in
four, and a second reading against the tree finds them. The polish: the four bare number devices (V9), the four
V6 constants (each now *the number X names*), the key's thread names everywhere, nine possessives on a link,
eight *actually*, four em-dash chains, and every caption at most two sentences. Also corrected where a
correction here made them disagree: `server/starting-a-server`, `server/server-tick`, the glossary's *Timeline*
and *Heightmap*, and `rendering/lightmap-fog-and-sky`'s *free-running* End flash; `world/level/blockscan` and the
modifier classes queued in pass3.md §7. One black-wall question cut from `lighting` because its answer could not
produce its symptom, and left to the second edition. Written on its page as mechanism, one probable upstream
bug: lava's ×4 spread delay is booked after the write and dropped as a duplicate of the plain delay
`LiquidBlock.onPlace` already booked (`fluids`). Left for E, F, I, J, L, M and O: the sentences on their pages
listed in the ledger's *For later sessions*. For P: the V1 and V2 entries on these pages, and this session's
diff.

**Session E — Part V · Blocks (2026-09-27).** Eight pages, each checked under Part 2 by its own agent while the session
read the part whole; the prompts carried the pages' pass 5–7 ledger entries and, by hand, the V1 and V2 entries on these
pages (V2's per-page sections and its *For the part session (E)* lines included), D's handoff on the write's guards and
session A's V6 constants. **237 corrections**, every one re-derived in `reference/26.3` before it was made; 29 are inside
a figure or a caption. Four are 26.3 changes V1 and V2 did not see (`Block` lost two statics; fuel is no longer read from
the door tag; a second caller of `BlockEntity.getUpdatePacket`; the chunk packet's empty tag), and three are sentences the
version pass left beside a fact it moved (the landing page's summary of V2's dig, the paragraph after V2's rewritten
arithmetic, *obsidian and its three relatives*). Ledger entries checked: the 112 on these pages (54 checked, 39 checked
with a part or the sentence beside it wrong, 13 wrong in whole or in part, 4 overtaken, 2 no claim). The three worst corrections:
`blocks-and-states`' write figure and the paragraph that reads it — the guard inside the chunk write tests the *block*
and the re-read in `Level.setBlock` the *state*, so the two diamonds are different questions, and the block-entity step
runs only if `onPlace` has not replaced the block (D's handoff; the figure is redrawn with two no-op tests, the guard on
the block and a gated block-entity step); `block-breaking`'s hook, **releasing the button does not cancel a break** —
releasing before finishing sends ABORT, which does, and what cannot be cancelled is the deferral after a STOP that came
too early, which since V2's finding finishes in the same server tick for almost every dig; and `block-interaction`'s
*which the fancy graphics preset does and the default does not* — fancy is the preset a new client starts on, so a door
you open is remeshed inline by default (which makes `rendering/section-meshing`'s opening wrong for a new client, handed
to L). What the whole-part read found that no report had: one — the piston closer asked *why does a piston push a block
that is powering it?* over an answer saying the block in front never powers it. It also found, before the reports, a
fifth javac-constant sentence session A's list had missed (`RedstoneTorchBlock`'s three) and the landing page's *fewest
lectures of any part this size*, both of which the agents then found too. **The record's audit was again the session's
finding**: eight agents re-derived every changed sentence and found **73 of the 237, 45 in sentences this session had just
written** — about one in four, D's rate — among them the cast's *copies most of its values out* (a third), a stuck dig
said to end only when the block turns to air (a faster tool breaks it too), *four flag words on this page* (six), and a
strike script that had written ten paragraph strikes in the ledger as `*~~*` (its bullet regex read a bold's first `*`).
The polish: the two bare number devices (V9), five em-dash chains, four possessives on a link, three *actually*, the key's
thread names, every caption at most two sentences, and five queue units settled by a clause. Also: 52 queue units struck
and five shared ones noted, so Part V has no open unit; sculk spread, declared on the landing page since pass 6 and never
entered, and four more lecture-sized unowned mechanisms (rails, the shelf, the beehive, fire spread) into pass3.md §7.
Corrected where a correction here made them disagree: `world/fluids`, `networking/what-the-client-is-told` (three),
`client/prediction-and-acks` (two), `rendering/section-meshing`, `server/server-level-tick`, `items/using-an-item`,
`lectures.md` and `reference/block-update-flags`. Left for J, L, N, O and P: the items in the ledger's *For later
sessions*, `section-meshing`'s opening chief among them. For P: the V1 and V2 entries on these pages, and this session's
diff.

**Session F — Part VI · Entities (2026-09-27).** Ten pages, each checked under Part 2 by its own agent while the session
read the part whole; the prompts carried the pages' pass 5–7 ledger entries and, by hand, the V1 and V2 entries on these
pages (V2's handoff on `authority`'s first figure included), C's handoffs on the entity tick and the tick list's copy, D's
on the villager schedule and `SleepInBed`, and session A's V6 constants. **307 corrections**, every one re-derived in
`reference/26.3` before it was made; 44 are inside a figure or a caption. Twenty-one are 26.3 changes the version pass did
not carry into the sentence: `Entity.commonTick` does the old per-tick bookkeeping and the client's interpolation, the
`Integer.MAX_VALUE` types get `UpdateInterval.NEVER` and never send a periodic position, `Entity.canSimulateMovement` is
final and reads the type, `CombatTracker.recheckStatus` moved to `LivingEntity.remove`, a fifth fall-reducing block
property, 44 serializers, 64 entity events, 36 damage tags, 115 memory types, and `Cushion`, a twenty-second non-living
damage class. Ledger entries checked: the 109 on these pages, 84 of them struck here (62 checked, 18 of those naming a
neighbour this session corrected; 11 checked except a part; 8 wrong or wrong in part; 2 overtaken; one tool note). The
three worst corrections: `authority`'s predicates and their figure were 26.2's — `Player` overrides three of the five, not
four, and a dropped item, a projectile, lit TNT and a few more simulate on both sides by their type whatever the root
answers (V2's handoff; the figure redrawn, 13.6px and no crossing); `synched-entity-data`'s and `entity-anatomy`'s
*never fires again after tick zero* — under 26.3's `UpdateInterval.NEVER` the branch never fires at all, so
`Entity.syncPosition` does nothing for those types, and for a living entity other than a shulker the stepped tracker takes
that flag first; and `movement-and-collision`'s *at least 1,200 ticks* for the forced position refresh, which is at most
that, and then only for an entity tracked every tick (overturning pass 5's listed claim). The whole-part read, written
before any report was opened, listed 25 items: 23 became corrections and two polish, and one of them sat open until the
record (`entity-anatomy`'s *on the base class exactly two things*, the second of which is `LivingEntity`'s). **The
record's audit was again the session's finding**: ten agents re-derived every changed sentence and found **80 of the 307,
54 in sentences this session had just written** — about one in four, D's and E's rate — among them
*CHANGED_DIMENSION rebuilds anything but a player* (a player is rebuilt on its way out of the End), *like the sky's light
level* (the one environment attribute that is not per-position; now the sky's colour), the group limit only a tropical fish
reaches (only one that does not school), and a four-block fall after a skeleton's arrow as *hit the ground too hard* (it is
*while trying to escape*). The polish: nine possessives on a link, eleven *actually*, five em-dash chains, one number device
(V9), the thread names on eight pages (V7), every caption at most two sentences. Also: 43 queue units struck and eleven
shared ones noted, so Part VI's row in `pass5_queue.py --summary` counts only shared units other parts hold open.
Corrected where a correction here made them disagree: `player/status-effects`, `player/the-two-phase-tick`,
`networking/what-the-client-is-told` (three), `lectures.md` (two), `reference/glossary` (two), `reference/non-living-damage`
and `reference/README`. Left for H, I, J, O and P: the items in the ledger's *For later sessions* — the passenger diff's
*filtered*, which 26.3 does not filter, and `chunk-storage`'s account of what the unload filter turns away among them.
For P: the V1 and V2 entries on these pages, and this session's diff.

**Session G — Part VII · Items and inventories (2026-09-28).** Nine pages, each checked under Part 2 by its own agent while the
session read the part whole; the prompts carried the pages' pass 5–7 ledger entries and, by hand, the V1 and V2 entries on these
pages (V2's *For the part session (G)* lines included), session B's handoff on `containers-and-menus` and session A's V6 constants.
An interruption stopped five of the agents mid-check; each was resumed from its transcript, and the session's cancelled edits were
re-applied by scripts that assert every target before writing. **255 corrections**, every one re-derived in `reference/26.3`
before it was made; 31 are inside a figure or a caption. Two are 26.3 changes the version pass did not reach (villager trades are a
registry of records and `VillagerTrades` the bootstrap that writes them, so the landing page's *not a family* was false;
`LootPredicates` is a fifth file naming `Enchantments`' keys), three are V6 (a third constant session A's list missed,
`Item.APPROXIMATELY_INFINITE_USE_DURATION`), and one is B's handoff (the button click is answered in its handler like any click).
Ledger entries checked: the 77 on these pages (64 checked, 36 of them naming a neighbour this session corrected; 4 wrong or wrong
in part; 7 overtaken; 2 notes). The three worst corrections: `enchantments`' *The three famous ones that have no effect
component* — Mending's `repair_with_xp` doubles the durability each point of experience buys and Looting has `equipment_drops`,
so only Fortune has none, and the claim sat on the landing page and `loot-tables` too (a false heading, corrected with its link);
`enchanting`'s second figure, whose last two arrows drew *three fresh offers from the new seed* after a click, where an enchanted
item fails `ItemStack.isEnchantable` and the costs are zeroed, and whose `Player.onEnchantmentPerformed` note sat after the enchant
loop it precedes; and `containers-and-menus`' *every mispredicted slot corrected*, which a click that throws breaks — the handler
never reaches `AbstractContainerMenu.resumeRemoteUpdates`, so that menu sends the client nothing until a later click succeeds (a
probable upstream bug, written as mechanism). What the whole-part read found before the reports: eighteen items, fifteen of them
corrections the agents then found too, and one the agents did not flag as a whole: every Part VII caption opened on a literal
*Figure:* after the stylesheet's own *Figure N.*, so all nineteen rendered *Figure 3. Figure: …* (the only part that did). **The
record's audit was again the session's finding**: nine agents re-derived every changed sentence and found **71 of the 255, 45 in
sentences this session had just written** — the one-in-four rate of C to F for a fifth session — most of them a correction that
named a population and not all of it (*those three* menus where five reach the base, three functions that return a new stack
where seven do, *the one debt* between two engines that link each other four ways), and one an outright error (*the tags … are
bound before it is even decoded*, where they are read then and bound only when the reload is applied, which `foundations/tags`
says). The audit also reversed one of the session's own polish moves: dropping *three* from *three engines* made every engine page
an engine, and the three are now named. The polish: the thread names on eight pages (V7), seven *actually*, one possessive on a
link, the caption prefix on nineteen, and nine voice units settled by a clause. Also: the part's queue settled (35 struck, settling
39 units: done 19, record 7, ruled 5, overtaken 2, second edition 2) and a note on the seven units other parts share. Corrected
where a correction here made them disagree: `player/the-spear`, `foundations/data-driven-types`, `lectures.md` (two) and
`reference/glossary` (two). Left for H, I, J, N, O and P: the items in the ledger's *For later sessions*, among them
`gen_reference.py`'s intros for `reference/loot-context-params` (*every key is read … with `LootContext.getOptional`*, and a
history claim) and `reference/enchantment-hooks`, which session O owns. For P: the V1 and V2 entries on these pages, and this
session's diff.

**Session H — Part VIII · The player (2026-09-28).** Eight pages, each checked under Part 2 by its own agent while the session
read the part whole; the prompts carried the pages' pass 5–7 ledger entries and, by hand, the V1 and V2 entries on these pages
(V2's twelve on `the-sword-swing`, its hurt-cooldown finding and its *For the part session (H)* lines, and its note on where the
client's movement leaves), F's three handoffs, G's two notes and session A's V6 constants. **241 corrections**, every one
re-derived in `reference/26.3` before it was made; 19 are inside a figure or a caption. Five are 26.3 changes the version pass
did not reach: the level runs `Entity.commonTick` on a player before `ServerPlayer.tick`, so *the first half never calls up past
`ServerPlayer`* was false; phase one counts down the hurt cooldown, not invulnerability; the movement judgements moved into a new
private `ServerGamePacketListenerImpl.handlePlayerPositionChange`, which the teleport acknowledgement also runs; that
acknowledgement now carries the position and no PosRot follows it; and a second position inside one client tick is a
disconnect, so *there is no kick for the flood itself* was false. Seven are V6, one of them a sentence session A's list missed
(`Player.DEFAULT_*_INTERACTION_RANGE`), and the food bar's heading *four numbers and a pile of literals* rested on the same
inference and is corrected with its three links. Ledger entries checked: the 96 on these pages (80 checked, 37 of them naming a
neighbour this session corrected; 8 wrong in whole or in part; 4 overtaken; 4 no claim). The three worst corrections:
`the-two-phase-tick`'s hook paragraph, whose *each of the four declares its own tick and its own aiStep* and *the first half never
calls up past `ServerPlayer`* were both false (Avatar is a fifth rung, aiStep is two classes', and 26.3 runs `Entity.commonTick`
first); `input-to-movement`'s release paragraph, where pass 5 session J's correction — a screen that consumes a release returns
before it is recorded — had never reached the page and pass 5 session H had called the wrong claim sound; and the landing page's
argument, *the player is the one object the server is not allowed to be right about*, where anything a player steers borrows its
authority. What the whole-part read found before the reports: 37 items, 33 of them corrections, most of which the agents then
found too — `player-anatomy` and `the-sword-swing` putting `LivingEntity` *one rung up* from `Player` four times against their own
ladder, a flowchart node naming a `PiercingWeapon.stabAttack` that does not exist — and one they did not: `status-effects` sending
a reader to a page for a class that page does not name. **The record's audit was again the session's finding**: eight agents re-derived every changed sentence and
found **50 more, 44 in sentences this session had just written** — a little under one in four, the rate of C to G — most of them a
correction still absolute (*the one time a client runs an effect's hooks* is also a turtle helmet and a parrot's cookie; *four
packets* beside the meal's broadcast sounds; *until you release it or the spear leaves your hand* beside death and a portal), and
one a withdrawal: the landing page's *most pages rest on authority* was wrong the other way, the spear and the food bar resting on
client-reported movement too. The polish: the thread names in seven casts (V7), eight possessives on a link, eight em-dash chains,
seven *actually*, four sizes (V10), and *charge* kept to the spear's right-click hold. Also: the part's queue settled (34 struck,
seven shared units noted), so `pass5_queue.py --summary` has no Part VIII row. Corrected where a correction here made them
disagree: `world/tickets-and-loading` (the move's call chain), `items/using-an-item` and `items/enchantments` (the charge's hits
and its `stabAttack`), and the glossary's *Status effect*. Left for I, J, L, N, O and P: the items in the ledger's *For later
sessions* — `rendering/entity-rendering`'s *four textures*, `reference/non-living-damage`'s *exactly three rows never reached*
and the glossary's two live `Player` subclasses among them. For P: the V1 and V2 entries on these pages, and this session's diff.

**Session I — Part IX · Networking (2026-09-28).** Six pages, each checked under Part 2 by its own agent while the session read the
part whole; the prompts carried the pages' pass 5–7 ledger entries and, by hand, every pass 8 entry on these pages (V2's eleven on
`packets-and-stream-codecs` and its handoffs, V1's movement-sync note, C's three handoffs, D's, E's, F's four, G's and H's two) and
session A's two V6 items. **220 corrections**, every one re-derived in `reference/26.3` before it was made; 15 are inside a figure or
a caption. Ledger entries checked: the 103 on these pages (55 checked, 28 checked with a part or the sentence beside it wrong, 11 wrong
in whole or in part, 5 overtaken, 2 no claim, 2 readers' questions answered). The three worst corrections: `the-connection`'s lead
figure drew the swing's answer back into the swinger's own client, *written, not flushed*, where `LivingEntity.swing` sends it only to
the players tracking you and a packet sent from the drain is flushed at once — the redraw sends it to *a player watching you* and folds
the client's `Connection` into a note to stay at six lanes; `what-the-client-is-told`'s hook had every viewer dead-reckon the creeper
from its last position and velocity, where a creeper is `MoveSimulationType.AUTHORITATIVE_SIDE` and no client moves it at all, and
what makes the base matter is that each relative move is decoded against the client's copy of it (the page's *far-off mob that
freezes and then jumps* and its *knockback is immediate on a creeper* rested on the same reading, and the landing page's symptom
list with them); and the landing page's argument, *each of which treats what arrives from the other as a claim*, with *the one
protocol written against a peer that lies* beside it, where the client takes the server's state as fact outside chat and the server's
movement and reach checks are written against a lying client. What the whole-part read found before the reports: 37 items, 30 of them
corrections, and every one of those a report found too but the landing page's broadcast sentence, which the reports passed and the
audit caught — the part's agents were as thorough as its reader this time (the login figure's note giving the authenticator's edge
to Netty, *the three states the tick moves through* naming two the tick never sets, and `ClientboundBossEventPacket` as *the part's
largest single class*, fifteenth, were each on both lists). **The record's audit was
again the session's finding**: six agents re-derived every changed sentence and found **71 of the 220, 52 in sentences this session
had just written** — about one in three, above the one in four of C to H — among them the heading on `Connection.tick` twice (*the one
call from a game thread*, then the session's own *the one periodic call*, while `resumeFlushing` flushes every player's connection each
tick), a new parenthesis saying the server installs a protocol on a game thread from configuration on (its return to configuration
swaps on Netty), a new `/kick` answer too narrow (a Netty-side kick stalls its event loop), and a redrawn chat figure whose band, moved
to cover the broadcast, spread over the recipient's lane in the render. The polish: thirteen possessives on a link, seven em-dash
chains, nine *actually*, two number devices (V9), seven sizes (V10), the thread names and *tick phase* (V7). Also: two queue-router
bugs — a `###` heading naming its own session and part now owns its units (three of Part XIII's had sat under Part IX), and
`--summary` files a unit naming pages in several parts under the part whose session runs last, which it had chosen by set order, so
the by-part rows changed from run to run; the lane key's `SConn` row retired; the part's queue settled (25 struck, three shared units
noted), so `pass5_queue.py --summary` has no Part IX row. Corrected where a correction here made them disagree: `server/server-tick`
(the heading's link, twice), `lectures.md` (two), `entities/movement-and-collision`, `entities/damage-and-death` and
`world/environment-attributes-and-timelines`. Left for N, O and P: the items in the ledger's *For later sessions*, among them a
probable chat-window drift the audit found in the code and nobody has run (a client without a sender's session strips the signature,
records nothing, and can fail its next checksum). For P: the V1 and V2 entries on these pages, and this session's diff.
