# Pass 6 — the lecture: the agent's brief, the session's runbook, the standard and the schedule

*Written 2026-09-07 by the planning session between pass 5 and pass 6, so that
every pass-6 session (A–O, run on Opus) launches the same read the same way.
Part 1 is handed to the agent verbatim — `tools/pass6_prompts.py` prepends it
to each page's prompt file, and that file carries **nothing else**, because
this pass's agent is a reader with nothing but the page. Part 2 is the
session's own procedure. Part 3 is session A's work: the rulings the part
sessions apply, made once — written here as the planning session's
recommendations with the numbers behind them, for session A to ratify, amend
or reverse and rewrite as a record, the way pass 5's session A rewrote its
Part 3. Part 4 is the schedule, one session per part, with what the tools
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
(at most about half, by A2's test) and **which page of each within-part twin
pair varies** (A7). Run the mechanical checks for the part:

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

## Part 3 — Session A: the standard

*Written by the planning session as recommendations, each with the number
behind it (`pass6_shape.py`, 2026-09-07). Session A ratifies, amends or
reverses each one with the exemplar page open, writes the rulings into
`TEMPLATE.md` where they are rules about a page, and rewrites this part as the
record of what was decided — the way pass 5's session A did. Thirteen part
sessions then apply them rather than re-deciding them.*

### A1. The second person — ratified as a register, refused as a first word

**Measured:** 26 of the 102 system pages open on the word *You*; 41 have a
second-person first sentence; 65 carry *you* somewhere in the opening
paragraph. By part, the second-person first sentence runs from none (I, II) to
all eight pages of Part VII; Parts VI (6 of 9), XI (5 of 11) and XII (5 of
10) are next.

**Recommended ruling.** The second person stays: the verified line is *a
sentence a player could act out*, an opening starts *inside* the scenario, and
putting the reader in it is the plainest way in. What became a slot is not the
person but the entry — *You …* as the first word, on a quarter of the corpus
and on every page of one part. So: any page may open in the second person; no
part opens most of its pages on the word *You*; the thing varied is **how the
reader enters the scenario** — a thing happening, a thing seen, a fact stated
flat, a question — not whether *you* appears. In the body the second person
stays where the reader does the thing (the click, the swing) and out of the
explanation, which is the corpus's usage today. The sentence-level register is
pass 8's.

### A2. The closer — one spelling, at most about half a part, never load-bearing

**Measured:** the closer is on **69 of 102** pages, in **five** spellings
(*Questions players ask* ×63; *Questions a reader asks* ×3, all in Part X;
*Questions the pattern raises*, *Questions a data-pack author asks*, *Questions
a command author asks* ×1 each) — the plan's *seven* was a miscount. Three
parts use it on every page (IV 10/10, V 7/7, VIII 7/7) and two nearly (XII
9/10, II 6/7). On four pages it is not the last content section
(`what-the-client-is-told`, `the-client-level`, `advancements`,
`the-execution-engine`). And **27 links from 25 pages land on a closer's
anchor** — each one an answer some other page needs, sitting in a section
named for questions a player asks; `status-effects`' closer holds three of the
page's real explanations, `server-tick`'s holds the autosave arithmetic.

**Recommended ruling.** (a) One spelling, *Questions players ask*; where the
questioner is a data-pack author or a command author the *question* says so
and the heading does not. (b) Session P's rule of thumb stands — at most about
half the pages of a part end on it — and the test that decides which pages
keep it is this: **a closer stays where every answer in it is a consequence a
player meets, and none is the page's own mechanism.** An answer another page
cites is load-bearing by definition; it moves up under a heading that says
what it says, and the citing link is repointed in the same commit. (c) A
closer that survives is the last content section, holds at most six questions,
and each answer is at most a paragraph. (d) Where the closer goes, its
material dissolves into the section where the answer happens (session G's
precedent: *Three things about the id*, *Why mobs look stupid*) or takes a
heading of its own; nothing is dropped except by the budget rule. (e) A page
without a closer whose best facts are question-shaped (`entity-lifecycle`,
`players-and-sessions`) may gain one if the part is under the half — the
device is still on the menu.

### A3. The 1.21 blockquote — at the foot, short, and only where a name moved

**Measured:** on **39** pages (the plan's 42 counted three pages that mention
a 1.21-era reader in prose without the device). At the foot of the page —
inside the last content section or right before *Where to look* — on 23:
all nine of Part X's and all eleven of Part XI's (sessions K and L of pass 3
moved them there deliberately) and one each in III, IX and XIII. In the body on
16: Part IV's four, Part XII's three, and one or two each in I, II, V, VII,
IX and XIII. The longest is eleven lines (`block-entity-rendering`).

**Recommended ruling.** The foot is its place: the last thing before *Where
to look*, after the closer if there is one — because it addresses a reader the
page is not otherwise written for, who should find it without reading the
page, and because in the body it interrupts the scenario for the reader the
book is for. At most eight lines; one per page; only where a name or a
mechanism actually moved between 1.21 and 26.2 (the template's rule) — a
blockquote that only says *this is new* goes. Its register is pass 8's.

### A4. The literal `## The trace: …` heading — the heading is the scenario

**Measured:** 20 pages in eight parts (VIII ×4, XII ×4, XIII ×4, IV ×3, VI ×2,
II, VII, XI). The template's rule is already that a heading says what the
section says, never which slot it fills.

**Recommended ruling.** Rename each to the scenario — *One click, one
integer, one round trip*, not *The trace: one click…* — with `check_links.py
--inbound` in hand, because the heading is an anchor.

### A5. The opening's last sentence — the hook last, bold spent not defaulted

**Measured:** 28 openings end on a bold sentence (Part IV 6 of 10, Part VII 5
of 8, Part VIII 4 of 7); 34 end on a dash clause.

**Recommended ruling.** The hook stays the last sentence (the template's
rule). Bold on it is a device, not a slot: spent where the sentence is the
page's thesis and the page returns to it — a figure caption or a heading
echoes it — and otherwise not. The two parts where most hooks are bold unbold
first, page by page, as each is read. The dash clause is pass 8's (the
em-dash chain is in its charter).

### A6. The landing page — the seventh section gets a place, and the argument ends on the claim

**Measured:** lines outside *Watch in this order* run 57 (I) · 69 (II) · 94
(IV) · 109 (III) · 128 (X) · 129 (VIII) · 132 (VII) · 133 (XIII) · 134 (V) ·
137 (XI) · 139 (IX) · 142 (VI) · 179 (XII), median **132** against the
template's *about a hundred*. The seventh section — the coverage answer
pass 5 asked every part for — is a heading on nine pages in three positions
(**first**, before the shape: V, VI, VII; **fourth**, before Reference: III,
XIII; **fifth**, after Reference: I, VIII, IX, XII), a headingless paragraph
on three (IV inside the shape section, X and XI inside the Reference section),
and absent on II. The recognition sentence — *a player recognises the part
by …* — is on nine, and on five (II, VII, VIII, IX, X) it is the argument's
last sentence, so the paragraph ends on a list of symptoms instead of a claim.
Four pages hand-count a coverage number beside a size that is generated (VI
*about 40%*, VII *about a third*, VIII *97%*, XII *a quarter*); the generator
now writes all thirteen.

**Recommended ruling.** (a) `TEMPLATE.md`'s landing page gains a seventh
section, ***Where the part stops***, in a fixed place: **after *Watch in this
order* and before *Reference this part uses*** — the reader has just seen the
lectures, the section says what is in the part's packages and not in them and
why, and the shelf closes the page. The exemplar landing page,
`commands/README`, already has it there. (b) It carries the families the pages
above already draw (a clause each), the deliberate omissions with the reason
(a sentence each, each an entry in [pass3.md](pass3.md) §7), the size where
the argument does not already carry it, and the coverage number from
`{{#include ../../generated/coverage-<dir>.md}}` — never hand-counted, so the
four swap theirs. (c) The budget stays *about a hundred lines plus the watch
order* with the seventh section inside it: at most fifteen lines, and what is
longer is either the argument made twice or an explanation that belongs on a
page. The median comes down by the argument, not the trim. (d) The argument
ends on the claim (XI is the model: a claim, three consequences, then the
hook); the recognition sentence may set the claim up mid-paragraph and may not
end it. (e) The phrases that became labels — *the part's closer*, *the part's
policy page*, *and not optionally*, *the vocabulary page* — are pass 8's,
already tagged.

### A7. The twin skeletons — the later page of a within-part pair varies

**Measured** (`pass6_shape.py --twins`, spines as tokens: cast · trace · q ·
look · seq · flow · state · svg · p): **six identical spines** shared by
fifteen pages, none inside one part — `block-breaking` = `codecs-nbt-json` =
`trees`; `block-interaction` = `the-connection` = `section-meshing`;
`chunk-anatomy` = `the-window` = `terrain`; `authority` = `recipes`;
`text-components` = `post-processing`; `models-and-atlases` =
`structure-placement` — and **seventeen within-part pairs one edit apart**,
of which the densest are Part VIII (`input-to-movement` against three of its
own neighbours: session P's *cast → The trace → detail → questions → where to
look, only the nouns change*), Part X's GUI-and-sound group (`gui-and-screens`
↔ `hud` ↔ `options` ↔ `what-makes-a-sound`) and Part XI's `blaze3d` ↔
`models-and-atlases` ↔ `post-processing`. Session P's other groups still hold
in the tokens (`biomes` ↔ `features-and-placement`; `density-functions` ↔
`terrain`; `jigsaw-and-templates` ↔ `trees`; `how-a-server-dies` ↔
`players-and-sessions`; `data-driven-types` ↔ `tags`; `authority` ↔
`entity-anatomy`; `block-entities` ↔ `signal-and-dust`).

**Recommended ruling.** `TEMPLATE.md`'s rule — *a page is not done until it
reads differently from its neighbours* — is about neighbours, so a within-part
pair is the finding and a cross-part identical spine is a note the session
reads and may leave. For each within-part pair **the later page in the watch
order varies**, because the reader meets the earlier one fresh; the exception
is one of pass 5's fifteen declared pairs (`block-breaking` ↔
`block-interaction`, *one lecture in two halves*), where a shared skeleton is
the point and what must read differently is the prose. The variation is
structural — a different order of the same sections, the questions dissolved,
the comparison table as the figure, the trace before the cast — never a
reshuffled heading over the same paragraphs.

### A8. The section order — the rule, then the exception; one subject a section

**From the queue:** `server-level-tick` delivers a punchline and immediately
qualifies it; `the-execution-engine` opens on *there is no recursion limit* and
names the budget in the middle and the two limits at the end; `the-window`
introduces a seventh callback under a heading that says six and explains it
three sections later; `advancements`' coverage section sits between the Q&A
and the page's last trace; a dozen headings promise two subjects of the three
under them.

**Recommended ruling.** A section lands on its rule and the exception follows
it, unless the exception is the page's hook. A section has one subject, and
its heading names it; a heading that names two of three subjects is the
finding. What a page names and does not explain — the coverage passages pass
5 added — sits in one place on every page: last before the closer, or last
before *Where to look* where there is none.

### A9. The cuts — a move or a logged cut, decided by the reader and the hook

**Measured:** thirteen pages are over 450 lines (`what-the-client-is-told`
510, `server-level-tick` 507, `packets-and-stream-codecs` 505,
`identifiers-and-registries` 491, `the-connection` 490, `players-and-sessions`
489, `text-components` 473, `what-this-book-skips` 471, `server-tick` 470,
`ai-goals-and-brains` 469, `entity-lifecycle` 458, `how-a-server-dies` 454,
`containers-and-menus` 453); the corpus median is 356, and by part it runs from
267 (VIII, X) to 490 (IX). 131 sections over forty lines carry neither a
figure nor an H3. Pass 3's drafters each logged their cheapest cut
([pass5.md](pass5.md):2180 for Part IV, :2520 for Part VII).

**Recommended ruling.** No line budget — a count in a queue is a description,
not a target, and the owner reads pages, not line counts. The evidence for a
cut is the reader's *what I skipped* and *the section I would cut first*, and
the test is the hook: a section the page's hook does not need and no other
page cites (`check_links.py --inbound`) is the first cut. A cut is a move —
to its owner page, or to Reference with a sentence and a link kept — or a
logged cut in [pass5.md](pass5.md) tagged `[kind=record]`, never a silence.
A page over 450 lines is read whole for the cut, not trimmed.

### A10. The exemplar — one page rewritten to the standard before the part sessions run

**Measured** (`pass6_shape.py --slots`): ten pages carry four of the fixed
devices at once. The candidate is **`world/environment-attributes-and-timelines`**
— the closer, the literal trace heading, a blockquote in the body and a bold
ending; the first lecture of Part IV, which is 10/10 on the closer; and the
page nine pages in six parts depend on, so its anchors are the test of the
rename discipline in A4 and A7. The alternatives with four:
`world/tickets-and-loading` (pass 3's policy pilot, whose shape was set as a
model then), `foundations/data-driven-types`, `networking/what-the-client-is-told`.

**Recommended.** Session A launches the reader on the candidate, rewrites it to
A1–A9 with the report in hand, and records what changed in
[pass9.md](pass9.md). That page and `commands/README` (the landing exemplar
from pass 5, given its coverage include) are what the part sessions read
before their own part.

### A11. What session A does not do

It does not read a part, does not rewrite a landing page but the exemplar's
own (to A6, as the model), makes no cut on a page it has not read whole, and
changes no fact. Three things are left where they belong: the tick-boundary
bars and the density of the trace figures (pass 7), the register of the 1.21
blockquote and the dash clause (pass 8), and the four Reference catalogues'
completeness lists (session N, job 5).

---

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
| **A** | — | the standard | the exemplar + `TEMPLATE.md` | — | Part 3 above: ratify, amend or reverse A1–A9 and rewrite Part 3 as the record; `TEMPLATE.md` gains the seventh section in its place (A6), the closer's rule and spelling under *The devices* (A2), the blockquote's place (A3), and a line on the second person (A1); the exemplar page rewritten with a reader's report in hand (A10) and `commands/README` given `{{#include ../../generated/coverage-commands.md}}` if its *where the part stops* carries the number; every anchor moved repointed under `check_links.py`. |
| **B** | — | I · Anatomy, II · Foundations | 2 + 7 | 5 + 2 | **I:** `what-this-book-skips` is 471 lines of fifteen tours and a table with no figure and four long sections — the length judged as a whole; `anatomy`'s *Where to look* is twenty names for a cast of eight; `anatomy` carries the book's only closer in the part, with the blockquote in the body. **II:** the closer on 6 of 7 — which three keep it; `tags`' pay-off *Prepared, then applied* is a bold lead-in with no heading that three pages cite; `tags`' opening restates L192; `data-components`' literal trace heading; `text-components` tells the `/say @a` punchline twice (body and Q&A); `codecs-nbt-json` shares its spine with `block-breaking` and `trees`, `text-components` with `post-processing`; within the part `data-driven-types` ↔ `tags` are one edit apart; the part's median is 415 lines. The landing pages: I at 57 with the seventh section after Reference; II at 69 with no seventh section and the argument ending on the recognition list. |
| **C** | — | III · The server | 5 | 11 | The closer on 2 of 5 — and both are the rule's test cases the other way: `server-tick`'s holds the autosave arithmetic (load-bearing, A2) and `players-and-sessions` has none while three of its `###` sub-heads are player questions in disguise; `server-level-tick`'s falling-sand punchline is qualified in the next paragraph (A8); `players-and-sessions`' *Four ways* heading over a paragraph naming a fifth (re-judged, per session C's ruling); `how-a-server-dies`' *Ctrl-C, the window, and a singleplayer world* carries three subjects; `starting-a-server`'s opening is the page's densest and overclaims against its own *Done* section; the part is the book's longest by median (470) — all five pages are over 437 lines, and `how-a-server-dies` ↔ `players-and-sessions` are one edit apart (session P: one skeleton run forwards and backwards for `starting-a-server` / `how-a-server-dies`). The landing page: 109 outside the watch order, the seventh section before Reference, the argument ending bold. |
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
