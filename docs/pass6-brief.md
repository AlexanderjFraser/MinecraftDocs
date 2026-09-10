# Pass 6 — the lecture: the agent's brief, the session's runbook, the standard and the schedule

*Written 2026-09-07 by the planning session between pass 5 and pass 6, so that
every pass-6 session (A–O, run on Opus) launches the same read the same way.
Part 1 is handed to the agent verbatim — `tools/pass6_prompts.py` prepends it
to each page's prompt file, and that file carries **nothing else**, because
this pass's agent is a reader with nothing but the page. Part 2 is the
session's own procedure. Part 3 is **the standard** — the rulings the part
sessions apply, made once: written by the planning session as recommendations
with the numbers behind them, and rewritten by session A on 2026-09-10 as the
record of what was ratified, what was amended and what was added, the way
pass 5's session A rewrote its Part 3. A part session reads it and applies it;
it does not re-decide it. Part 4 is the schedule, one session per part, with what the tools
measured before the first session spent anything, and **the status column the
owner reads to see which sessions are done**. The charter this implements is
in [plan.md](plan.md) under *Pass 6 — the lecture*; the queue it draws on is
[pass5.md](pass5.md), kind `lecture`.*

**What pass 5 left for this pass, in one paragraph.** Pass 5 made the corpus
one book — every mechanism has a home, every seam a link, every landing page an
argument — and in doing so it read across pages and never *down* one. What no
session has asked since pass 3 is whether a page reads as one lecture's notes
from its first sentence to its last: whether the devices the template offered
as a menu have become slots (the *Questions players ask* closer on 69 of the
102 system pages and on every page of three parts; the literal `## The trace`
heading on 20; the 1.21 blockquote on 39; an opening that ends on a bold
sentence on 28 and starts on the word *You* on 26), whether two pages in one
part share a skeleton so that the second reads as the first with the nouns
changed, whether a section states its exception before its rule, and what a
reader in a sitting would skip. Beside the system pages, the thirteen landing
pages grew through pass 5 while gaining their argument — a seventh section
nobody named, in three positions and three forms — and the template has no
place for it yet.

**The owner's ruling of 2026-09-05 still shapes this pass.** The site stands
alone: nothing on a page may lean on a lecture to make sense, the page count is
whatever the book needs, and everything in scope is explained concisely.
Concision governs *how* a thing is explained, not *whether* — so a cut in this
pass is a move or a logged cut, never a silence.

**The tools** (every one ships with `--probe`, which proves it fails on the
construct it should):

| tool | what it answers | run as |
|---|---|---|
| `tools/pass6_shape.py` | **new.** The shape of every page, measured: the opening (second person, bold or dash ending), the spine as tokens, the closer (spelling, position, questions), the literal trace heading, the 1.21 blockquote and where it sits, the cast against *Where to look*, the budgets (lists over seven, sections over forty lines with no figure), the skeleton twins, and the thirteen landing pages (lines outside the watch order, the seventh section, the recognition sentence, a hand-counted number) | `--summary`, `--part world`, `world/lighting`, `--twins`, `--landing`, `--slots` |
| `tools/pass6_prompts.py` | **new.** One prompt file per page for the reader — Part 1 and the path, nothing else — and one *session* file beside it: the page's lecture-kind queue entries, its shape report, its twins, and every inbound link by the anchor it lands on (a renamed heading moves an anchor); per part, `_part-shape-<part>.md` and `_part-notes.md` | `--part world --out DIR` |
| `tools/pass5_queue.py` | [pass5.md](pass5.md) by kind and page. This session added a fifth kind, `[kind=record]`, for units no pass acts on (pass-3 cut logs, re-derived counts), taught it to skip preambles (a bare bold lead-in, an italic preface, a rule), and re-routed 92 guessed units and struck 20 verified settlements: the queue now holds **136 `lecture` units**, 45 still guessed | `--kind lecture --part world`, `--summary`, `--unsure` |
| `tools/pass5_coverage.py` | `--write` is new: one phrase per part into `src/generated/coverage-<dir>.md` — *N% of the part's lines are named on no page in the book* — from the same `PARTS` mapping the size phrases use, run by `deploy.sh`, so a landing page that carries the number includes it and never hand-counts it again | `--write` |
| `tools/check_links.py` | the gate; `--inbound PAGE` is what a session runs before renaming a heading | `--inbound src/systems/world/lighting.md` |

---

## Part 1 — The brief (given to one agent per page)

You are reading one page of MinecraftDocs — a book about how the Java
Minecraft 26.2 codebase works — the way a viewer would read one lecture's
notes: on its own, in one sitting, without the rest of the book open. Every
fact on the page has been checked against the decompiled source twice and read
against the other pages once, so assume the page is true. What nobody has
asked is whether it *reads*: whether a reader who has only this page gets from
its first sentence to its last without getting lost, reading twice, guessing,
or skipping. That is your job. You have no source and no other page, on
purpose, and you change nothing.

### What you have

- **The page**: the path is at the top of your prompt file. Read it start to
  finish once, the way a reader would — not the headings first, not the
  figures first, not a search for anything. Then read it a second time to
  write the report.
- **Nothing else.** Do not open the part's landing page, the glossary, the
  pages the page links to, or the decompile. The book's other pages exist;
  where this page sends you to one, note that it did and whether the sentence
  around the link told you enough to go on without following it. Where the
  page uses a term as though you had met it, say so; the session knows which
  of those the book allows.

### The four questions

1. **Where did you get lost?** The line where the page stopped carrying you: a
   term used before it was explained, a jump from one mechanism to the next
   with no bridge, a figure you could not read against the paragraph under it,
   a paragraph whose subject you could not name, a heading that promised one
   thing and delivered another, a number with no population.
2. **What did you have to read twice?** The sentence or paragraph you went
   back to, and why: it carried two ideas, it stated the exception before the
   rule, its pronoun had no referent, its point was in the middle, its
   parenthesis was longer than its sentence.
3. **What did the page assume you already knew?** Every term, class or
   mechanism used as though you had met it, with the line. For each, say
   whether the page explained it later (then it is out of order), sent you
   elsewhere for it (then say whether the sentence told you enough to go on),
   or neither.
4. **What did you skip?** The sections, lists, tables and asides you would not
   have read in a sitting, and why: an inventory, a list you could not use, a
   second telling of something above, a digression from the scenario, a
   questions section that answered things you had not asked, a note for a
   reader you are not.

### Then three things the session compares against the page's own promises

- **The page in one sentence**, in your words: what it taught you. The session
  compares this to the opening paragraph, which by the book's rule ends on the
  one surprising, true thing the page exists to explain.
- **The section you would cut first**, and what the page would lose.
- **The question you still have** — one the page raised and did not answer, or
  one its scenario made you ask.

### Rules

- **No facts.** You are not fact-checking and you have no source. If a
  sentence reads as false or as contradicting another sentence on the page,
  put it under *Suspected errors* with the two lines; the session re-derives it
  against the decompile. Never propose a rewording that changes what a
  sentence claims.
- **The devices are not findings by themselves.** A questions section at the
  end, a blockquote for a 1.21-era reader, a cast table, a heading that names
  the trace, an opening in the second person: none of these is wrong. Report
  one only where it cost you something — you skipped it, it repeated the body,
  it held an explanation the body needed, it broke the scenario — and say
  what it cost.
- **Quote line numbers** for every finding. A finding without a line is not a
  finding.
- **Do not rewrite the page.** Report; the session decides; the owner judges.
- **Cover the whole page.** A report that stops early says where.

### What to report

A single markdown report in this shape. Nothing else.

```
## Where I got lost
- L<n> — <what happened, in one sentence: the term, the jump, the figure, the heading>

## What I read twice
- L<n> — <why>

## What the page assumed I knew
- L<n> — <term or mechanism> — explained later at L<n> | sent to <page> and the sentence was enough / was not | neither

## What I skipped
- L<n>–L<n> — <what it is> — <why>

## The page in one sentence
<what it taught me>

## The section I would cut first
<section title> — the page would lose <what>

## The question I still have
<the question>

## Suspected errors
- L<n> against L<n> — <what disagrees>   (or: none)

## Could not judge
- <what, and why>
```

---

## Part 2 — The session runbook

One session = one part (Parts I and II share session B), on Opus. Every step
is a command or a rule; the judgement is in steps 6 and 7.

### 1. Read

[plan.md](plan.md) (the charter and this session's line in Part 4 below),
`CLAUDE.md`, this file whole — Part 3 is the standard the session applies —
`TEMPLATE.md`'s *What every page keeps*, *The shapes*, *The devices*, *The
budgets* and *The landing page*, and the part's landing page. Then the part's
queue, which is what earlier passes already know about it:

```
python tools/pass5_queue.py --kind lecture --part world
```

Grep the part for `<!-- Q:` — the owner's questions — and answer each in the
prose before the session ends.

### 2. Generate the prompts

```
python tools/pass6_prompts.py --part world --out <scratchpad>/pass6-world
```

One reader's file per page, `<part>--<slug>.prompt.md` (the brief and the
path), and one session file per page, `<part>--<slug>.session.md` (the queue
entries, the shape report, the twins, the inbound links by anchor); per part,
`_part-shape-<part>.md` (the device table and the landing page's report) and
`_part-notes.md` (queue entries naming no page). The session reads its own
files while the agents run; the agents never see them.

### 3. Launch

One background agent per page, all at once, on Opus. The prompt is one line:
*Read `<prompt file>` and do what it says; the page is at `<path>`. Write your
report to `<scratchpad>/pass6-<part>/<slug>.report.md`.* Reports are not
committed. Brief per page, never per part.

### 4. Read the part whole while they run

**Read the part end to end in watching order**, in one sitting, as pass 5's
sessions did — but this time reading *down* each page rather than across them.
Keep three lists as you go: the pages whose closer holds the page's own
mechanism rather than a player's consequence (Part 3, A2); the pages whose
skeleton you had just read on the page before (A7); and the sections you
skipped yourself. Then decide, with the part's device table open, the two
part-wide questions before any page is touched: **which pages keep the closer**
— the test in A2, page by page, with the half a smell rather than a quota —
and **which page of each within-part twin pair varies** (A7). Run the
mechanical checks for the part:

```
python tools/pass6_shape.py --part world
python tools/check_deps.py
```

### 5. Audit the reports

A reader's report is evidence, not a verdict. For every finding the session
acts on, re-read the passage in the page yourself and say what the reader
tripped on. *What the page assumed I knew* is checked against the landing
page's *before you start* and the page's own links: an allowed dependency
linked at first use is not a finding; one not linked is a seam and gets the
citation form (pass 5's rule, applied in passing); one the book does not
allow — a later part, or nothing — is a sentence the page owes. *Suspected
errors* go to the decompile: if the page is wrong, fix it and log the
correction in [pass9.md](pass9.md) the way a pass-4 session did (what the page
said, what the decompile says, file and line). Take nothing else on trust: a
reader that liked the page is a reader that skimmed it, and a report that says
nothing was skipped on a 470-line page says so.

### 6. Decide, under the rulings

For each page, in this order, with Part 3 open: the closer (keep, dissolve, or
promote its load-bearing answers under headings of their own); the literal
trace heading (renamed to the scenario); the 1.21 blockquote (to the foot, or
cut); the opening (the entry into the scenario varied, the hook last, bold
spent rather than defaulted); the skeleton (varied on the later page of a
twin pair); the section order (the rule before its exception; a section one
subject); the cuts (a move or a logged cut, never a silence; the reader's skip
list and the hook test decide, not a line count). Then the part's landing
page, last, to A6.

### 7. Act

- **A heading is an anchor.** Before renaming one, `python tools/check_links.py
  --inbound src/systems/<part>/<page>.md`; every link that lands on the renamed
  section is repointed in the same commit, and `check_links.py` refuses the
  commit otherwise. An answer promoted out of a closer takes its inbound links
  with it.
- **Nothing is dropped except by moving it or logging the cut** with the
  reason in [pass5.md](pass5.md), tagged `[kind=record]`. A cut that is a move
  goes to its owner page or to Reference and keeps a sentence and a link.
- **The landing page** gets the seventh section in the template's place (A6),
  its coverage number from `{{#include ../../generated/coverage-<dir>.md}}`
  where it carries one, and an argument that ends on the claim; the blurbs in
  *watch in this order* are re-synced to the pages as they now stand.
- **The summarisers** follow: the part's section of `lectures.md` (order
  claims only — it is the copy that gets shorter), the glossary's anchors
  where a heading moved.
- Nothing on a page changes a fact without the decompile open; no figure is
  redrawn for legibility (pass 7) — a reshaped section may need its figure
  moved, not redrawn; no sentence is polished for voice (pass 8). A finding of
  those kinds goes to [pass5.md](pass5.md) tagged `[kind=figure]` or
  `[kind=voice]`.

### 8. Verify and ship

```
python tools/verify_names.py
node tools/check_mermaid.js
python tools/check_lanes.py --strict
python tools/check_deps.py
python tools/check_links.py --quiet
mdbook build
git add <your files, by name> && git commit -F <message file>     # "pass 6, session X — Part N: <summary>"
tools/deploy.sh
```

Run `verify_names.py` and `check_links.py` after each page you touch, not
after all of them. Commit your own files by name, never `add -A`.

### 9. Record

- [pass5.md](pass5.md): strike (`- ~~…~~`, the strike **outside** the bold)
  each lecture-kind entry settled, with a word saying how (done · overtaken ·
  ruled out and why), **in the same commit** — pass 5's close found twenty-six
  settlements nobody struck; tag the entries the tool guessed wrong; append
  what the reading raised for passes 7 and 8, tagged by kind.
- [pass9.md](pass9.md): the session's entry — every page rewritten, every
  claim introduced (a renamed heading's implied claim, a promoted answer, a
  moved section, a re-argued opening), every correction with file and line.
- [plan.md](plan.md): the session log line.
- **This file, Part 4: the session's row** — the status cell, and one line on
  what the session did, in the row's last column.

---

## Part 3 — The standard (session A's record, 2026-09-10)

*The planning session wrote this part as eleven recommendations, each with the
number behind it. Session A read the exemplar and one reader's report on it,
ratified nine, amended one, added one, and wrote the rules about a page into
`TEMPLATE.md`, which is where the part sessions read them. This is the record
of what was decided and why; the numbers are the planning session's,
unchanged, so that a session can read a recommendation and its ruling
together. Thirteen part sessions apply these; none re-decides them.*

**What the exemplar proved about the method, before any ruling.** One reader
with no source, no other page and no measurements found **five factual errors**
on a page that had been fact-checked adversarially twice — the opening pinning
a stretch of 1,800 ticks to one instant, a mob's danger ending at the wrong
end of the night, four numbers said to exist in a record that holds three, a
five-weight kernel over six cells that does not close, and an accessibility
option described as always on. Every one of them was found by a reader
*reading*, not by a reader checking: the sentence contradicted another
sentence, or the arithmetic would not close. That is the error two fact-checks
could not see and pass 5 was not looking for, and it is the strongest argument
so far that this pass earns its cost. It is also why the standing rule stands:
a session that finds one **stops, opens the decompile, re-derives it itself**,
and logs it in [pass9.md](pass9.md) with file and line.

### A1. The second person — **ratified**

The ruling as recommended. Any page may open in the second person; **no part
opens most of its pages on the word *You***; what varies is *how the reader
enters the scenario* — a thing happening, a thing seen, a fact stated flat, a
question — not whether *you* appears. In the body the second person stays
where the reader does the thing and out of the explanation. The
sentence-level register is pass 8's.

Written into `TEMPLATE.md` under *What every page keeps*, item 3. The
exemplar is the entry that is not a person at all — *"Dusk on the overworld
clock is a stretch and not an instant"* — a fact stated flat, which is the
fourth of the four ways in and the one the corpus uses least.

### A2. The closer — **amended: the test stands, the quota goes**

(a), (c), (d) and (e) as recommended: one spelling, *Questions players ask*;
a closer that stays is the last content section, holds at most six questions
and answers each in at most a paragraph; where it goes its material dissolves
into the section where the answer happens or takes a heading of its own; and a
closer-less page whose best facts are question-shaped may gain one.

(b) is **amended**. The recommendation was *at most about half the pages of a
part*, and a quota is the one thing A9 refuses two rulings later — *no line
budget; a count in a queue is a description, not a target*. The same argument
applies here: a quota would force a session to strip a closer off a page where
every answer passes the test, to hit a number. So **the test decides, and
nothing else**:

> A closer stays where every answer in it is a consequence a player meets,
> and none is the page's own mechanism. An answer another page cites is
> load-bearing by definition: it moves up under a heading that says what it
> says, and the citing link is repointed in the same commit.

The half is a **smell, not a target**. A part that comes out of its session
with the closer still on nearly every page has probably not applied the test,
and the session says in its log why each survivor passed. Four parts are in
that position today (IV 10/10, V 7/7, VIII 7/7, XII 9/10).

The exemplar is the test working in both directions on one page. Five
questions: the nether's night and *"does setting the time in the overworld
move the End"* are consequences and stayed; *"why do the server and the client
disagree by a tick"* was the page's own mechanism and moved into the client
section, where it now closes the comparison; *"where did the villager schedule
go"* was half a repeat of the 1.21 blockquote and its real content moved into
*The four timelines*; and the pillager-patrol answer carried the page's only
statement of a mechanism the body needed — *a timeline with no period is not a
cycle* — so the mechanism moved up and the question kept the consequence.
Three questions left, all consequences, and the page is better in the middle
rather than shorter at the end.

Written into `TEMPLATE.md` under *The devices*.

### A3. The 1.21 blockquote — **ratified**

The foot is its place: the last thing before *Where to look*, after the closer
if there is one. At most eight lines; one per page; only where a name or a
mechanism actually moved. A blockquote that only says *this is new* goes. Its
register is pass 8's.

Written into `TEMPLATE.md` under *The devices*. The exemplar's went from
eleven lines in the body to eight at the foot, and lost the clause about the
two `DimensionType` fields that *stayed put* — a blockquote about names that
moved has no room for names that did not.

### A4. The literal `## The trace: …` heading — **ratified, and it takes the verified line with it**

Rename each of the twenty to its scenario, with `check_links.py --inbound` in
hand. One addition: **where the verified line names the slot too, it is
rewritten in the same edit.** Exactly one page did (`environment-attributes-
and-timelines`, whose line began *"The trace: dusk falls — …"*), so this is a
clause, not a job.

The exemplar's heading is now *"Dusk, and the same question asked twice"*. No
inbound link landed on the old anchor, which is worth knowing before the part
sessions start: of the four devices, the trace heading is the cheapest to
rename and the closer the dearest — **27 links from 25 pages land on a
closer's anchor**.

### A5. The opening's last sentence — **ratified**

The hook stays last. Bold on it is spent where the sentence is the page's
thesis and the page comes back to it, and otherwise not. The two parts where
most hooks are bold (IV 6/10, VII 5/8) unbold page by page as each is read.

The exemplar **keeps** its bold, and that is the point of the ruling: *"Night
does not set the sky's colour — it multiplies whatever the biome produced"* is
the page's thesis, and *Arguments, not values* pays it off forty lines later
with the same verb. The rule is not *unbold*; it is *earn it or lose it*.
Written into `TEMPLATE.md` under *What every page keeps*, item 3.

### A6. The landing page's seventh section — **ratified**

`TEMPLATE.md`'s landing page now has seven things, and the seventh is
***Where the part stops***, **after *Watch in this order* and before
*Reference this part uses***: the reader has just seen the lectures, so this
is where they can judge what is left out, and the shelf closes the page. It
carries the families the pages above already draw, the deliberate omissions
with the reason (each an entry in [pass3.md](pass3.md) §7), and the coverage
number from `{{#include ../../generated/coverage-<dir>.md}}`, never
hand-counted. At most fifteen lines, inside the *about a hundred* budget. The
argument ends on the claim, and the recognition sentence may set the claim up
mid-paragraph and may not end the paragraph.

Two facts for the sessions that will move theirs: the heading is
***Where the part stops*** and nothing longer — the two parts that spell it
*"…, and how much of it there is"* (VI, VII) take the short form, because the
number is now inside the section rather than in its title — and
**no page in the corpus links to any of the thirteen anchors**, so every move
and rename in this ruling is free.

`commands/README` is the landing exemplar and now carries the include, the
first page in the book to. Its number is 21%, and the sentence it sits in
keeps the part's own argument about *why*: *"the catalogue is where they
sit"*. The other four hand-counted numbers (VI, VII, VIII, XII) swap for the
include in their own sessions.

### A7. The twin skeletons — **ratified**

A within-part pair is the finding; a cross-part identical spine is a note the
session may leave. For each within-part pair **the later page in the watch
order varies**, and the variation is structural — a different order of the
same sections, the questions dissolved, the comparison table as the figure,
the trace before the cast — never the same paragraphs under reshuffled
headings. The exception is one of pass 5's declared pairs, where the shared
skeleton is the point and the prose is what must differ.

Written into `TEMPLATE.md` beside *a page is not done until it reads
differently from its neighbours*, which is the rule this makes operable by
saying who *neighbours* are.

### A8. The section order — **ratified, with the exemplar's method**

A section lands on its rule and the exception follows, unless the exception is
the page's hook. A section has one subject and its heading names it. What a
page names and does not explain sits in one place: last before the closer, or
last before *Where to look* where there is none.

The exemplar had the corpus's commonest form of this: *Who owns the clock*,
45 lines, no figure and no subsection, carrying three subjects — what a clock
is, what moves it, and how an instant on it is named. **The fix is three H3s
under the existing H2**, which costs four lines, keeps the H2's anchor (two
pages land on it) and clears the forty-line budget at the same time. Part
sessions should reach for that before reaching for a split: 131 sections in
the corpus are over forty lines with neither a figure nor an H3.

Written into `TEMPLATE.md` under *What every page keeps*, item 6.

### A9. The cuts — **ratified**

No line budget. The evidence for a cut is the reader's *what I skipped* and
*the section I would cut first*, and the test is the hook: a section the hook
does not need and no other page cites is the first cut. A cut is a move or a
logged cut in [pass5.md](pass5.md) tagged `[kind=record]`, never a silence. A
page over 450 lines is read whole for the cut.

**And a page may come out longer.** The exemplar took four logged cuts — a
fourteen-name type inventory, a modifier-library roll call, six consumer class
names, and a command's subtree shape — and still went from 414 lines to 444,
because five corrections needed more words to be true and the reader's one
unanswered question was worth a paragraph. A session that reports a part's
line count going up has not failed; a session that trimmed to a number has.

### A10. The exemplar — **ratified and done**

`world/environment-attributes-and-timelines` was read by one agent under
Part 1's brief and rewritten to A1–A9 and A12. What changed is in
[pass9.md](pass9.md). It and `commands/README` are what a part session reads
before its own part: the first for a page, the second for a landing page.

The reader's report is the shape a part session should expect: eight places it
got lost, thirteen it read twice, twenty-odd terms the page assumed, eight
things it skipped, one section it would cut, one question it still had, and
four suspected errors — of which two were real, one was a wording ambiguity
and one was two different tracks the page never distinguished. **Roughly half
of what a reader reports is actionable**, which is why step 5 of the runbook
says a report is evidence and not a verdict.

### A11. What session A does not do — **ratified, with one departure**

It read no part, rewrote no landing page but the landing exemplar's *Where the
part stops*, made no cut on a page it had not read whole, and left the
tick-boundary bars and figure density to pass 7, the blockquote's register and
the dash clause to pass 8, and the four Reference catalogues to session N.

The departure is facts. The brief says session A *changes no fact*; the
reader found five, and the standing rule for passes 5–8 says a session that
finds a real error stops and re-derives it against the decompile itself. The
standing rule wins — a session does not publish a sentence it knows to be
false in order to keep a lens clean. All five are in [pass9.md](pass9.md) with
file and line.

### A12. ***Where to look* is a reading list, not an index** — new, session A's

The planning session measured the cast against *Where to look* and made no
recommendation; the exemplar's reader skipped the section by design and the
schedule flags it under three separate part sessions, so it wants one ruling
rather than thirteen.

**Measured** over the 102 system pages: the median is **18 names**, 61 pages
carry more than fifteen, and **82 pages carry at least one name that appears
nowhere else on the page — 513 names in all**. The leaders are
`contexts-and-predicates` (26), `recipes` (21), `entity-lifecycle` (20),
`features-and-placement` (18), `jigsaw-and-templates` (17), `pathfinding` (16),
`starting-a-server`, `text-components` and `codecs-nbt-json` (15 each).

**Ruling.** *Where to look* is entry-point names in reading order — a reading
list for someone opening the decompile, **not an index of the page**. A name
in it the page never said is a door the reader can still open, so it is
allowed. A dozen of them is the field inventory come back under a new heading,
which is the thing pass 3's template explicitly dropped, and those go to the
class index and Reference where the inventories live. No number is a
threshold; the question a session asks is *would a reader opening the source
start here*, and a name that is only in the list because it is in the package
fails it.

Written into `TEMPLATE.md` under *What every page keeps*, item 7. The exemplar
keeps all nineteen of its names, one of which (`Timeline.createTrackSampler`)
is not in its prose and is a genuine door.


## Part 4 — The schedule

Sessions B–N run in sidebar order, one part each, after A; O closes. The
numbers are what `pass6_shape.py` and `pass5_queue.py` found on 2026-09-07,
before any session ran — they say where the work is, and no count is a target.

**The devices by part** (`pass6_shape.py --summary`; *closer* is the questions
section, *foot* the blockquote's position, *twin* a page whose spine another
page shares exactly):

| part | pages | closer | spellings | `## The trace` | 1.21 (at the foot) | opens 2nd person | ends bold | ends on a dash | in a twin group | long sections | median lines |
|---|---:|---:|---:|---:|---|---:|---:|---:|---:|---:|---:|
| I · anatomy | 2 | 1 | 1 | 0 | 1 (0) | 0 | 0 | 1 | 0 | 5 | 402 |
| II · foundations | 7 | 6 | 1 | 1 | 1 (0) | 0 | 1 | 3 | 2 | 7 | 415 |
| III · server | 5 | 2 | 1 | 0 | 2 (1) | 1 | 0 | 1 | 0 | 4 | 470 |
| IV · world | 10 | 10 | 1 | 3 | 4 (0) | 3 | 6 | 5 | 1 | 10 | 413 |
| V · blocks | 7 | 7 | 1 | 0 | 1 (0) | 4 | 1 | 2 | 2 | 9 | 339 |
| VI · entities | 9 | 3 | 1 | 2 | 0 (0) | 6 | 1 | 4 | 1 | 8 | 408 |
| VII · items | 8 | 2 | 2 | 1 | 2 (0) | 8 | 5 | 3 | 1 | 13 | 372 |
| VIII · player | 7 | 7 | 1 | 4 | 0 (0) | 4 | 4 | 3 | 0 | 10 | 267 |
| IX · networking | 5 | 4 | 1 | 0 | 3 (1) | 2 | 3 | 2 | 1 | 8 | 490 |
| X · client | 12 | 8 | 2 | 0 | 9 (9) | 1 | 1 | 1 | 0 | 15 | 267 |
| XI · rendering | 11 | 6 | 1 | 1 | 11 (11) | 5 | 2 | 5 | 4 | 14 | 358 |
| XII · worldgen | 10 | 9 | 1 | 4 | 3 (0) | 5 | 1 | 1 | 3 | 19 | 317 |
| XIII · commands | 9 | 4 | 3 | 4 | 2 (1) | 2 | 3 | 3 | 0 | 9 | 275 |
| **all** | 102 | 69 | 5 | 20 | 39 (23) | 41 | 28 | 34 | 15 | 131 | 356 |

*Opens 2nd person* counts a second-person first sentence; 26 of the 41 start
on the word *You*. *Long sections* are over forty lines with neither a figure
nor an H3. Links landing on a closer's anchor: 27, from 25 pages.

**The landing pages** (`pass6_shape.py --landing`):

| part | lines outside the watch order | the seventh section | the recognition sentence | a hand-counted number |
|---|---:|---|---|---|
| I | 57 | *Where the part stops*, fifth, after Reference | yes (*the split*), mid-paragraph | — |
| II | 69 | none | yes, the argument's last sentence | — |
| III | 109 | fourth, before Reference | yes, mid | — |
| IV | 94 | no heading — inside the shape section | yes, mid | — |
| V | 134 | first, before the shape | — | — |
| VI | 142 | first (*…and how much of it there is*) | — | *about 40%* |
| VII | 132 | first (*…and how much of it there is*) | yes, last | *about a third* |
| VIII | 129 | fifth, after Reference | yes, last | *97%* |
| IX | 139 | fifth, after Reference | yes, last | — |
| X | 128 | no heading — inside the Reference section | yes, last | — |
| XI | 137 | no heading — inside the Reference section | — | — |
| XII | 179 | fifth, after Reference | yes, mid | *a quarter* |
| XIII | 133 | fourth, before Reference (the exemplar) | — | — |

**The queue by kind** (`pass5_queue.py --summary`, after this session
re-routed it): 444 open units — 38 `book` (pass 5's, now pass 10's or
declared), **136 `lecture`**, 57 `figure`, 183 `voice`, 30 `record`; 45 still
guessed and marked `?`, which each part session tags as it reads. The
`lecture` units by part: I 5 · II 2 · III 11 · IV 11 · V 7 · VI 10 · VII 13 ·
VIII 6 · IX 17 · X 13 · XI 8 · XII 8 · XIII 12 · frame and Reference 13.

### The sessions

The **status** column is the one the owner reads: `—` until the session runs,
then *done <date>*, written by the session itself in step 9. The last column
is what the tools and the queue put in front of the session; the session
appends one line saying what it did.

| session | status | part | pages | queue (lecture) | the charter's named items, and what the tools add |
|---|---|---|---:|---:|---|
| **A** | **done 2026-09-10** | the standard | the exemplar + `TEMPLATE.md` | — | Part 3 above: ratify, amend or reverse A1–A9 and rewrite Part 3 as the record; `TEMPLATE.md` gains the seventh section in its place (A6), the closer's rule and spelling under *The devices* (A2), the blockquote's place (A3), and a line on the second person (A1); the exemplar page rewritten with a reader's report in hand (A10) and `commands/README` given `{{#include ../../generated/coverage-commands.md}}` if its *where the part stops* carries the number; every anchor moved repointed under `check_links.py`. — **Done.** Nine ratified, A2 amended (the test decides; the half is a smell, not a quota — a count in a queue is not a target, which is A9's own argument), **A12 added** (*Where to look* is a reading list, not an index: 82 of 102 pages carry a name that is nowhere else on the page, 513 in all). `TEMPLATE.md` rewritten in seven places. `world/environment-attributes-and-timelines` rewritten to the standard: closer 5 questions → 3 (two moved into the body), the trace heading and the verified line renamed to the scenario, the blockquote 11 lines in the body → 8 at the foot, a 45-line three-subject section given three H3s inside its anchor, four cuts logged, 414 → 444 lines. `commands/README` is the first page to carry a generated coverage number. **Five facts corrected** — all five found by a reader with no source on a page fact-checked twice. |
| **B** | **done 2026-09-10** | I · Anatomy, II · Foundations | 2 + 7 | 5 + 2 | **I:** `what-this-book-skips` is 471 lines of fifteen tours and a table with no figure and four long sections — the length judged as a whole; `anatomy`'s *Where to look* is twenty names for a cast of eight; `anatomy` carries the book's only closer in the part, with the blockquote in the body. **II:** the closer on 6 of 7 — which three keep it; `tags`' pay-off *Prepared, then applied* is a bold lead-in with no heading that three pages cite; `tags`' opening restates L192; `data-components`' literal trace heading; `text-components` tells the `/say @a` punchline twice (body and Q&A); `codecs-nbt-json` shares its spine with `block-breaking` and `trees`, `text-components` with `post-processing`; within the part `data-driven-types` ↔ `tags` are one edit apart; the part's median is 415 lines. The landing pages: I at 57 with the seventh section after Reference; II at 69 with no seventh section and the argument ending on the recognition list. — **Done.** Eleven readers, one per page. **I:** `what-this-book-skips` judged whole and cut 476 → 457 — the nine *covered* and *absorbed* rows of the rulings table (things the book does **not** skip, on the page that draws the boundary) became one paragraph, and its "rule three" citation took the anchor and the rule's name, which was the only mechanism in the book cited by number without one; `anatomy`'s closer lost the two answers that were the page's own mechanism (the crash asymmetry is a section now, the five *main* methods opened the trace) and its *Where to look* went 19 → 12 under A12; its blockquote went to the foot. **II:** the closer went 6 of 7 → 4 on the test alone — `resource-system` kept its five because every one is a thing a player meets, and `identifiers-and-registries` and `data-driven-types` lost theirs entirely because not one of their twelve questions was a consequence, eight of them moving up into the section that needed them (`HolderOwner.canSerializeIn` travelled 363 lines to its first use); two blockquotes moved to the foot and two were *created* out of closer answers written for a 1.21 reader; the within-part twin pair varied on the later page by dissolving its questions; `tags`' pay-off got six H3s inside the H2 its three citing pages already point at, so a citation lands on the paragraph. Both landing pages re-argued to A6 with the seventh section in place and a generated coverage number — Part I's argument now *names* the four threads it promised three times and never listed. **Nine facts corrected**, all nine found by readers with no source, and five of the nine are one sentence contradicting another sentence or a figure **on the same page**. Part I 871 → 869 lines, Part II 3,002 → 2,965. Nineteen units to [pass5.md](pass5.md), eight entries struck and two annotated, one coverage decline to [pass3.md](pass3.md) §7. |
| **C** | **done 2026-09-10** | III · The server | 5 | 11 | The closer on 2 of 5 — and both are the rule's test cases the other way: `server-tick`'s holds the autosave arithmetic (load-bearing, A2) and `players-and-sessions` has none while three of its `###` sub-heads are player questions in disguise; `server-level-tick`'s falling-sand punchline is qualified in the next paragraph (A8); `players-and-sessions`' *Four ways* heading over a paragraph naming a fifth (re-judged, per session C's ruling); `how-a-server-dies`' *Ctrl-C, the window, and a singleplayer world* carries three subjects; `starting-a-server`'s opening is the page's densest and overclaims against its own *Done* section; the part is the book's longest by median (470) — all five pages are over 437 lines, and `how-a-server-dies` ↔ `players-and-sessions` are one edit apart (session P: one skeleton run forwards and backwards for `starting-a-server` / `how-a-server-dies`). The landing page: 109 outside the watch order, the seventh section before Reference, the argument ending bold. | — **Done.** Six readers, one per page. The part arrived *inside* every rule of thumb and the session's finding is that this settles nothing: **both closers failed A2's test in part**. `server-tick` 4 questions → 2 — the autosave arithmetic moved up beside its countdown, and *does freezing stop the server* held the page's only definition of **frozen**, a word its `tickChildren` table uses in three rows 240 lines above, so the mechanism moved under the table and the question kept the consequence; a fourth entry was not a question at all and now closes *An empty server stops ticking*. `server-level-tick` 7 → 4, two of them second tellings of sections fifty lines above and one a 1.21 answer that is the page's blockquote now (3 of 5 pages carry one, all at the foot, none in the body). Three of its headings overclaimed against its own figure and two were renamed; the third was right and the *prose* was uncountable, so the five became the part's only list — which answers the list question pass 3's session D left open. **A7**: `starting-a-server` / `how-a-server-dies` was live and `how-a-server-dies` was one edit from `players-and-sessions` too, so the later page varied by putting its **comparison table before its cast**, and *Three booleans and a question* dissolved into the three sections that use each boolean; no page in the part shares a spine with any other now, in the part or out of it. `players-and-sessions` kept its question-shaped `###` heads and gained no closer (A2 ruled the other way: they already have headings of their own), and *The three kicks* left the *Four ways* H2 it was never one of. **Six facts corrected** — the sharpest being the landing page saying `MinecraftServer` is not counted in this part's size, when the atlas's spec is `net/minecraft/server` itself-only and counts it in both III and I. Four *Where to look* lists 26/33/33/24 → 17/19/19/15 under A12, in each page's own reading order, no name lost from the book. Part III 2,357 → 2,367 lines. Twenty units to [pass5.md](pass5.md), nine entries struck and two annotated. |
| **D** | — | IV · The world | 10 | 11 | The part where A2 bites hardest: the closer on **10 of 10** — which five keep it, with `chunk-generation-pipeline` telling the world's edge in the body and again as the fourth question, and `lighting`'s closer the longest; three literal trace headings (`environment-attributes-and-timelines`, `game-events-and-vibrations`, `points-of-interest`); four blockquotes, all in the body; six of ten hooks bold (A5); the exemplar lives here if A10 stands. From the queue: `chunk-anatomy`'s *four shapes* carries two subjects; `chunk-storage`'s *Why the server thread never waits* is two sections under one heading; `lighting`:145's `scheduled` sentence is two sentences from what it qualifies; `points-of-interest`:233-270 mixes the ticket story with walk-target mechanics; `scheduled-ticks`:192 points at *forty lines below*; pass 3's length bill — eight of ten pages at 358–417 with each drafter's cheapest cut logged at [pass5.md](pass5.md):2180. `chunk-anatomy` shares its spine with `the-window` and `terrain`. The landing page is inside budget (94) with the coverage answer inside the shape section and no heading of its own. |
| **E** | — | V · Blocks | 7 | 7 | The closer on **7 of 7** — which three or four keep it; `block-interaction`'s Q&A on a door's bottom half repeats the body four sections up; `signal-and-dust`'s *The second implementation* leaves the page's own trace (run the lever and two dust through it), its torch answer arrives cold and its staircase is told three times; `pistons-and-block-events`' heading promises two subjects of three and its cast promises `PistonHeadBlock` and never returns; `blocks-and-states` carries two subjects that its verified line and hook do not announce (not split — the hub's second half is what six pages cite — but the header line and one clause carry the reader across); the *constant nobody reads* device several times with no citation of the page that explains why; four second-person openings of seven. `block-breaking` and `block-interaction` are a declared pair one edit apart (A7's exception) and each shares its spine with two other parts' pages; `block-entities` ↔ `signal-and-dust` one edit apart. The landing page: 134 outside, the seventh section **first**, before the shape — and its *one thing belongs to nobody* sentence to re-judge against the hopper and the four block-entity state machines, which session E's log sent to §7 and which the planning session found there only after carrying them itself. |
| **F** | — | VI · Entities | 9 | 10 | The closer on 3 of 9 is inside the rule; the queue asks the other direction — `entity-lifecycle` and `damage-and-death` have none and three of `entity-lifecycle`'s best facts are question-shaped (A2 e). `ai-goals-and-brains` is 469 lines and its verified line promises *meet at the bell*, which the trace never delivers; `pathfinding`'s verified line is the third consecutive villager while its hook is the mob against the fence (swap the halves); `authority`'s *Where the gates actually sit* is an eight-site inventory in a seven-item list (a table), and the page states its own count in four places after a correction changed it (read whole); `movement-and-collision`'s *Off it goes* joins two subjects with *the tick ends*; `pathfinding`'s three enumerations over the seven-item budget (the 27 `PathType`s want a Reference view — route to N); `damage-and-death`'s blocking sentence is an aside inside an aside. Six of nine open in the second person (A1); two literal trace headings; `authority` shares its spine with `recipes` and is one edit from `entity-anatomy`. The landing page: 142 outside, the seventh section first, a hand-counted *about 40%* to swap for the include. |
| **G** | — | VII · Items and inventories | 8 | 13 | The closer on 2 of 8 — but `enchantments`' is a 92-line *Questions the pattern raises* (the spelling, and the length), and session G says three closer-less pages have the material for one inline (`containers-and-menus`, `contexts-and-predicates`, `using-an-item`); `containers-and-menus` ends on a nine-packet enumeration in prose and `loot-tables` lists nine entry types inside the paragraph that explains the algebra (the list budget); `enchanting`'s last section carries three subjects and its heading names two, and its *What it costs, and who pays* is right about the anvil only; `recipes` says the `CraftingInput` accounting twice; `items-and-stacks` explains the pop time twice; `contexts-and-predicates`' literal trace heading and a blockquote in the body; `using-an-item`'s cast says *client main* where the book says Render thread (check, then pass 8). **All eight pages open in the second person** and five hooks are bold — the part where A1 and A5 bite hardest; pass 3's length bill is here too ([pass5.md](pass5.md):2520). `recipes` shares its spine with `authority`. The landing page: 132 outside, the seventh section first, a hand-counted *about a third*, the argument ending on the recognition list. |
| **H** | — | VIII · The player | 7 | 6 | The closer on **7 of 7** and four literal trace headings (`input-to-movement`, `status-effects`, `the-sword-swing`, `the-two-phase-tick`) — and `input-to-movement` is one edit from three of its own neighbours (session P's *only the nouns change*), so A7 lands here first. `status-effects`' closer is over sixty lines against a thirty-line trace and holds three of the page's real explanations, and its verified line's potion is never drunk; `input-to-movement`'s most-cited paragraphs are bold sentences with no heading, so a Part III page lands on `#questions-players-ask`; `the-two-phase-tick`'s Netty section lost two sentences and may want rebalancing; `hunger-and-experience`'s verified line promises a meeting the page never stages, and its own hook is the fourth question; `the-spear`'s tail is five hand-offs in five clauses; `player-anatomy`'s *three sides* is a forty-line field inventory with sixteen names only there. Four of seven open in the second person, four hooks bold. The landing page: 129 outside, the seventh section after Reference, the recognition list last, a hand-counted *97%*. |
| **I** | — | IX · Networking | 5 | 17 | The most queue entries of any part. The closer on 4 of 5, and `what-the-client-is-told`'s is not last and sits under a heading (*What goes out around the gates*) that says *gates* where its content says gate 3; its *The level's own feeds* is five bullets of which one is a forward reference; `packets-and-stream-codecs`' verified line promises a trace the page drops after a quarter (a verified-line change, not a restructure), and its buffer-binding material is one subject in two sections a hundred lines apart; `the-connection`'s second half is the channel's life-cycle rather than the round trip its verified line promises (say so in the opening, or mark a second movement), the read timeout is said twice, the `HandlerNames` paragraph is six lines for one clause and the kick answer four sentences for two; `protocol-phases`' *What the phases leave unused* is two paragraphs whose count describes the figure four sections up, its opening says four languages over five phases, and its cast omits two classes the page explains; `chat-and-signing`'s first four table rows are an ordering claim, three names appear only in *Where to look*, and a question the page raises is unanswered (a closer candidate, with the fact re-derived). The part is the book's longest by median (490) with three pages over 489 lines; `the-connection` shares its spine with `block-interaction` and `section-meshing`. The landing page: 139 outside, the seventh section after Reference, the recognition list last, and a non-dependency inside *before you start* that session O judged and left. |
| **J** | — | X · The client | 12 | 13 | The closer on 8 of 12 in two spellings (*Questions a reader asks* on `the-gui-render-tree`, `text-and-fonts`, `sound-engine`); `the-client-level`'s is not last and four of its six questions are other pages' subjects; the blockquote at the foot on nine of twelve — the model for A3, with Part XI. `the-gui-render-tree`'s recording-verb paragraph is 22 identifiers in prose (a table); `options`' loading guard has no anchor because its only home is a question inside the closer — the shape change session J declined; `prediction-and-acks` opens on the declared four-sentence contract *and* on the authority split (which is the hook); the GUI-and-sound group `gui-and-screens` ↔ `hud` ↔ `options` ↔ `what-makes-a-sound` are each one edit from the next (A7). The shortest pages in the book (median 267): the cut bill is light. The landing page: 128 outside, the coverage answer inside the Reference section with no heading, the argument ending on the recognition list. |
| **K** | — | XI · Rendering | 11 | 8 | The closer on 6 of 11; the blockquote at the foot on all eleven (the model); the three-verb mnemonics on `the-frame`, `visibility-and-the-frame-graph` and `post-processing` — a part-wide slot, judged as a set; `the-window` carries two subjects (the window, `NativeImage`) and says so nowhere — one sentence in the opening declaring the platform layer, and its seventh callback's ordering; `visibility-and-the-frame-graph`'s *One bucket per buffer set* lost its ending in pass 5; `particles`' explosion section is a second trace the book cannot cut and can shorten; `block-entity-rendering`'s blockquote is eleven lines, the longest. Five of eleven open in the second person. Four of the six identical spines touch this part (`the-window`, `section-meshing`, `post-processing`, `models-and-atlases`) and `blaze3d` ↔ `models-and-atlases` ↔ `post-processing` are one edit apart. The landing page: 137 outside, the coverage answer inside the Reference section with no heading. |
| **L** | — | XII · World generation | 10 | 8 | The closer on **9 of 10** — which five keep it (`terrain`, `biomes`, `structure-placement` have five, five and six answers); four literal trace headings (`biomes`, `features-and-placement`, `hand-built-structures`, `jigsaw-and-templates`) and session P's *cast → The trace: X → two or three sections → questions → where to look, only the nouns change*, still true in the tokens: `biomes` ↔ `features-and-placement`, `density-functions` ↔ `terrain`, `jigsaw-and-templates` ↔ `trees` are each one edit apart, and `terrain`, `trees` and `structure-placement` each share a spine with another part; `hand-built-structures` buries its cast inside *The idea*; `blending`'s opening carries two numbers before the reader knows what a column is; `creating-a-world`'s *three details* paragraph is a list in prose clothing; `structure-placement`'s *Whether it is worth laying out* promises a decision the section no longer describes; nineteen long sections, the most of any part. The landing page: **179 outside**, the largest in the book, the seventh section after Reference, a hand-counted *a quarter*. |
| **M** | — | XIII · Commands and data packs | 9 | 12 | The closer on 4 of 9 in **three** spellings (*players ask* ×2, *a command author asks*, *a data-pack author asks*) and two of the four not last (`advancements`, `the-execution-engine`); four literal trace headings (`advancements`, `dialogs`, `game-tests`, `scoreboard-and-data`). `brigadier-and-commands` is the part's largest page and grew in pass 5 — the split question re-asked with the page as it stands, with the seam the page already has at *The tree on the wire*; `scoreboard-and-data` carries four systems and its opening says three (a split or a re-argued opening); `advancements`' coverage section sits between the Q&A and *The screen at the other end* (A8); `the-execution-engine` opens on *no recursion limit* and names the budget in the middle and the two limits at the end; `entity-selectors`' *Resolve* carries five bolded claims, three about cost (a table); `functions-and-macros` has no cast and opens on *The pipeline* — deliberate, or the part's odd page. The landing page: 133 outside, the seventh section before Reference — pass 5's exemplar, the model for A6's position. |
| **N** | — | Reference and the frame | 11 hand-kept + the introduction, `lectures.md`, the atlas | 13 | Job 5, the completeness lists for the four Reference catalogues: three were settled in pass 5 (`non-living-damage` by F, `submit-phases` by K and N, `hud-elements` by J and N); the fourth, `level-data-and-rules`, is checked against the page as it stands ([pass5.md](pass5.md):865 and :872 — `DirectoryLock` is `starting-a-server`'s now and the *session.lock* row cites it; seven table rows had no prose), and its paragraphs are still inventories in prose clothing (:2761). The 27 `PathType`s from F, if session F asks for the view. The frame: the introduction's skip list is a list and its five rules have no anchors (session O's findings); `lectures.md` still writes a page's line in two places and five of its shape paragraphs are near-copies of the landing pages' — the summariser is the copy that gets shorter. The glossary has no lecture-kind work; its headwords are pass 8's. |
| **O** | — | the close | — | — | **The thirteen landing pages read as one set** (where pass 5 found thirteen of its last twenty corrections): the seventh section in its place on all thirteen, the argument ending on a claim, the recognition sentence off the end of five paragraphs, the four hand-counted numbers swapped for the include, the budget; `lectures.md` re-derived from the landing pages; the pass's own strikes audited (a strike is a claim; twenty-six settlements went unstruck in pass 5); [pass9.md](pass9.md)'s entries checked for shape; the devices re-counted with `pass6_shape.py --summary` against this table; the verdict on whether the pass earned its cost; and pass 7's charter detail written with the figures counted afresh (193 mermaid blocks on the system pages today: 99 flowcharts, 88 sequence diagrams, 6 state diagrams). |

**What no session does**: change a fact without the decompile open (the
standing rule); move a page (pass 5's last-moves rule — after pass 5 no page
moves again); redraw a figure for legibility (7); hunt a tic or settle a
count's wording (8); move a mechanism between pages except as a cut's
destination, and then with the citation form (pass 5's rule, still standing).
