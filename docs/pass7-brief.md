# Pass 7 — the figures: the viewer's brief, the session's runbook, the standard and the schedule

*Written 2026-09-14 by the planning session between pass 6 and pass 7, so that
every pass-7 session (A–O, run on Opus) launches the same look the same way.
Part 1 is handed to the agent verbatim — `tools/pass7_prompts.py` prepends it to
each page's prompt file, together with the page's path and, for each figure, the
picture of it as the site shows it — and that file carries **nothing else**,
because this pass's agent is a viewer with the picture and the section. Part 2
is the session's own procedure. Part 3 is **the standard** — the rulings the part
sessions apply, made once: written by the planning session as recommendations
with the numbers behind them, for session A to ratify, amend or reverse and then
rewrite as the record, the way pass 6's session A rewrote its Part 3. A part
session reads it and applies it; it does not re-decide it. Part 4 is the
schedule, one session per part, with what the tools measured before the first
session spent anything, and **the status column the owner reads to see which
sessions are done**. The charter this implements is in [plan.md](plan.md) under
*Pass 7 — the figures*; the queue it draws on is [pass5.md](pass5.md), kind
`figure`.*

**What pass 6 left for this pass, in one paragraph.** Pass 6 read every page
down, as one lecture's notes, and found the sentence that contradicts the
sentence beside it — 198 corrections, none of them a fact a fact-check would
query. What it could not judge it sent here, in 93 queue units on top of the 57
already waiting, and the reason is in its own logs: **nobody has ever looked at a
figure rendered**. Every check so far was parse (`check_mermaid.js`) and
arrow-by-arrow truth (pass 4); no session has seen a figure at the width a reader
gets it, beside the section it sits in. Sessions C, D and F each found, on their
own, a part-wide pattern — *the lead figure the page cannot yet be read against*,
a picture that names five or nine mechanisms whose prose is below it — and each
sent it whole rather than patching a page. Session E found four pages spending a
flag number the page had not minted, fixed the prose half and sent the figures.
Sessions J and K found figures that were wrong (no screen-close edge; particles
routed past the queue) and figures that said the same thing twice. The owner's
brief for this pass says the rest: the diagrams are where a reader sees
machine-made writing first — text under other text, pictures the wrong size,
figures so dense they cannot be read even enlarged — and a reader who skims uses
the figure as the check on the section: *if I understand the picture, I
understand the section*. So the questions are not only *is it true* but *is it
needed*, *does it show the thing the section needs shown*, and *is it as complex
as it needs to be and as simple as it can be*.

**What the tools found, in one paragraph.** 206 figures on 125 pages — 88
sequence diagrams, 101 flowcharts, 6 state diagrams and 11 generated SVGs — and
every system page carries at least one. Rendered in Chrome at the desktop column
(1,092px), **134 of the 194 mermaid figures are shrunk below their natural size,
76 to less than half, and 89 show type under 9px**; the widest is 5,415px wide
and shown at a fifth. That is one cause, not a hundred: a sequence diagram is as
wide as its longest message, and the site's mermaid init does not wrap. A
candidate init (`tools/pass7/`) that wraps messages and sets the site's font
takes the sequence diagrams from 70 below half to none and from 76 under 9px to
none, without touching a page. Beside the size: 115 figures open their section
with nothing but the heading above them, none has a caption, 51 are pointed at
by no sentence at all; 139 introduce most of their names before the prose does
and 151 carry names the prose never says; 121 carry labels that are sentences;
the parts-dependency figure has 26 edge crossings; and a gate that did not exist
this morning finds **119 names in figures that are not in the decompile as
written**, out of 2,619 checked.

**What a textbook from the future looks like, as far as this pass can reach.**
Every figure is true, and gated — its names checked like the prose's, its arrows
re-derived when they change. Every figure is legible where it stands, at the
width the reader has, without the zoom. Every figure speaks one visual language
with every other: the same shape means the same thing on every page, the same
colour means the same thread, and the colours live in one stylesheet rather
than in the pages. Every figure answers one question, and its caption says
which. Every figure is data — text in the page, diffable, regenerable from the
source where the source can draw it — never a picture pasted in. And the kind of
figure follows the mechanism: a conversation for a trace, boxes and arrows for a
branch, states for phases, a class diagram for what an object holds, a byte
layout for a packet, a curve for a number that is a curve — the site's mermaid
draws twenty-one kinds and the corpus uses three.

**The tools** (every one ships with `--probe`, which proves it fails on the
construct it should):

| tool | what it answers | run as |
|---|---|---|
| `tools/render_figures.js` | **new.** Every figure as the reader sees it: the built site served locally, opened in the Chrome or Edge already on the machine, every `pre.mermaid` and `figure.map` SVG screenshotted at the column width and measured — natural and displayed size and the scale between them, the smallest type on screen, labels overlapping labels, labels over a shape not their own, labels outside their box, edges through a node they do not connect, crossings, anything clipped, and the counts. Writes `render/<page>--f<n>.png` and `render/index.json`. `--init-js` and `--css` try a candidate theme without touching the site; `--html` renders a standalone gallery | `--no-build`, `--pages systems/world`, `--theme navy`, `--init-js tools/pass7/mermaid-init.candidate.js --css tools/pass7/figure-classes.candidate.css --out render/candidate`, `--html tools/pass7/gallery.html --out render/gallery`, `--probe` |
| `tools/pass7_figures.py` | **new.** Every figure measured against its page: where it sits (the section, whether it opens it, the lead-in, the caption, whether a sentence points at it, before or after the cast), what its source is (lanes, messages, tick bars, nodes, edges, sentence labels, flag-number gates, colour in the page), which of its names the prose says *before* it, only *after* it, or *never*, and — with `render/index.json` — how it renders; the sections over forty lines with no figure; a ranking by trouble | `--summary`, `--part world`, `world/lighting`, `--rank --top 40`, `--candidates`, `--json --out FILE`, `--probe` |
| `tools/check_figure_names.py` | **new — the gate over figures.** Every identifier-shaped token inside a mermaid block, checked against the decompile the way `verify_names.py` checks the prose: a class, a dotted member (inherited members allowed), and a sequence message's head against the lane it is sent to; a nested class named bare and an unqualified member in a flowchart label are *notes*, not failures, until session A rules. Report-only through the pass; `--strict` at the close. Its parser also feeds `verify_names.py --index`, so a class named only in a figure reaches the class index (139 page pairs added on 2026-09-14) | `--pages src/systems/world`, `--notes`, `--strict`, `--mentions`, `--probe` |
| `tools/pass7_prompts.py` | **new.** One prompt file per page for the viewer — Part 1, the path, and each figure's number, line, section and picture — and one *session* file beside it: the figure-kind queue, the page's figure report, the gate's failures and notes, every figure arrow by arrow, the figure-less long sections, and the inbound links by anchor; per part, `_part-figures-<part>.md` (the table and the ranking) and `_part-notes.md` | `--part world --out DIR` |
| `tools/check_lanes.py --unused` | the key rows no page declares (44 of 342 today) | `--unused` |
| `tools/check_mermaid.js` | the parse gate, unchanged in verdict; it now exports its fence-mapping helpers, keeps `block-beta`'s lexer quiet, and gives the jsdom window a `structuredClone`, so `pie`, `packet-beta` and `radar-beta` parse under it as they do in the browser | as before |
| `tools/pass7/` | **new.** `mermaid-init.candidate.js` (the site font, `sequence.wrap`, the `base` theme read off mdBook's light and navy palettes, no mirrored actors), `figure-classes.candidate.css` (the five semantic classes and the caption style), `gallery.html` (one figure of each of twelve kinds, rendered to `render/gallery/`) — session A's evidence, adopted or not | see the files' headers |
| `tools/diagram_arrows.py` | pass 4's arrow-by-arrow listing, reused: the numbered list a session re-derives against when it redraws | `src/systems/world/lighting.md` |

---

## Part 1 — The brief (given to one agent per page)

You are looking at the figures of one page of MinecraftDocs — a book about how
the Java Minecraft 26.2 codebase works — the way a reader does: rendered, at the
width the site shows them, beside the section each one sits in. Every fact on
the page has been checked against the decompiled source twice and read against
the other pages once, and the prose has been read as one lecture's notes; assume
the words are true. What nobody has asked is whether the *pictures* work:
whether a reader who looks at the figure first — most do — can read it, can tell
what it shows, and gets from it the one thing the section needed a picture for.
That is your job. You have the page and the pictures, on purpose nothing else,
and you change nothing.

### What you have

- **The page**: the path is at the top of your prompt file. Its figures are
  listed there by number, with the line each one's source starts on, the section
  it sits in, and **the picture** — a PNG of exactly what the site's reading
  column shows, at the size it shows it. Look at each picture *before* you read
  its section, the way a reader does, and then read the section with the picture
  beside it.
- **Nothing else.** Do not open other pages, the decompile, or any tool. Where a
  figure uses a word the page has not given you, say so; the session knows which
  the book allows.

### The questions, per figure

1. **What does it show?** Before reading the section, say in one sentence what
   the picture is telling you — the order, the branch, the cycle, the boundary,
   the shape. If you cannot say, say that, and say what stopped you.
2. **What could you not read?** Type too small to read at this size; a label
   under another label, over a box, or cut off at an edge; an arrow you could
   not follow to its end; two arrows you could not tell apart; a lane or a box
   whose meaning you could not tell. Name the label or the arrow.
3. **What did the section need a picture for?** After reading the section: the
   one thing in it that words carry badly — an order of events, a branch with
   its conditions, a loop, a boundary between threads or machines, a
   containment, a quantity. Does the figure show *that* thing, and is it the
   first thing your eye lands on? If the figure shows something else, say what.
4. **What is in the picture that the section does not need, and what does the
   section need that the picture lacks?** A box the prose never mentions; a
   label that explains what the prose explains better; an arrow that restates
   the paragraph. And the other way: a step the prose walks through that the
   figure skips, a condition the prose names that the figure hides in a label.
5. **Is it the right kind of picture?** A conversation between lanes for a
   sequence in time; boxes and arrows for a branch or a pipeline; states for
   phases; a table for a comparison; a tree for a hierarchy. Would a different
   kind show the same thing in fewer marks? Would a table?
6. **Does it speak words the section had not given you yet?** Method names, flag
   numbers, terms — used in the figure as though you knew them, explained (if at
   all) further down. List them.
7. **If the page has more than one figure, do they divide the work?** Two figures
   showing one mechanism; a later figure restating the first in more boxes; a
   figure whose job the table beside it does faster.

### Then, per page

- **The figure you would keep** if the page could have only one, and why.
- **The figure you would cut first**, and what the page would lose — or nothing.
- **The section that wanted a picture and has none**: the one place you read an
  order, a branch or a shape in prose and wished for a figure. Say what it would
  show. If no section did, say so.
- **A sketch of the worst one, redrawn** — in words, or as a mermaid block —
  showing what you would put in front of a reader instead. Mark it *proposal*.
  It changes nothing by itself: **every arrow it adds, removes or reverses is a
  claim** the session must check against the decompile, so list those arrows
  under the sketch as a numbered list.

### Rules

- **No facts.** You are not fact-checking and you have no source. If a figure
  reads as contradicting the prose beside it — an arrow the paragraph describes
  the other way, a lane the text calls by another name, a count that does not
  match — put it under *Suspected errors* with the figure number and the line;
  the session re-derives it. Never propose relabelling an arrow to say something
  the page does not say.
- **Legibility is judged at the size you were given.** The site can enlarge a
  figure on a click; a figure that is only readable enlarged has failed, and you
  say so.
- **The devices are not findings by themselves.** A note bar for a tick
  boundary, a lane per class, a diamond for a decision, a subgraph for a thread:
  none of these is wrong. Report one only where it cost you something, and say
  what.
- **Quote figure numbers and line numbers** for every finding. A finding
  without one is not a finding.
- **Do not rewrite the page.** Report; the session decides; the owner judges.
- **Cover every figure.** A report that skips one says which and why.

### What to report

A single markdown report in this shape. Nothing else.

```
## Figure <n> — <its section>
- **Shows**: <one sentence, written before reading the section>
- **Could not read**: <label or arrow — why>   (or: everything)
- **The section needed**: <the thing> — shown: yes / partly / no — <why>
- **In the picture, not needed**: <what>   **Needed, not in the picture**: <what>
- **Kind**: right / would be better as <kind> — <why>
- **Words not yet given**: <list>   (or: none)
- **With the page's other figures**: <divide the work / say the same thing / …>

## The figure I would keep
<n> — <why>

## The figure I would cut first
<n> — the page would lose <what>   (or: none)

## The section that wanted a picture
<heading, line> — it would show <what>   (or: none)

## Proposal — figure <n> redrawn
<words, or a mermaid block>
Arrows this changes (claims for the session):
1. <from → to: added / removed / reversed / relabelled>

## Suspected errors
- figure <n>, L<n> against L<n> — <what disagrees>   (or: none)

## Could not judge
- <what, and why>
```

---

## Part 2 — The session runbook

One session = one part (Parts I and II share session B; the frame and
Reference share session N), on Opus. Every step is a command or a rule; the
judgement is in steps 6 and 7.

### 1. Read

[plan.md](plan.md) (the charter and this session's line in Part 4 below),
`CLAUDE.md`, this file whole — Part 3 is the standard the session applies —
`TEMPLATE.md`'s *The shapes*, *The devices*, *Figures* and *Lanes* (session A
rewrites *Figures* and *Lanes* to Part 3; until then Part 3 wins where they
differ), and the part's landing page. Then the part's queue, which is what
earlier passes already know about its figures:

```
python tools/pass5_queue.py --kind figure --part world
```

Grep the part for `<!-- Q:` — the owner's questions — and answer each in the
prose or the figure before the session ends.

### 2. Render

```
mdbook build
node tools/render_figures.js --no-build
```

The whole book, not the part: the JSON is one file and a page's figures are
compared against the corpus. About a minute. `--pages systems/world` re-renders
a part after an edit, in a few seconds.

### 3. Generate the prompts

```
python tools/pass7_prompts.py --part world --out <scratchpad>/pass7-world
```

One viewer's file per page, `<part>--<slug>.prompt.md` (the brief, the path,
the figures and their pictures), and one session file per page,
`<part>--<slug>.session.md` (the queue entries, the figure report, the gate's
failures and notes, every figure arrow by arrow, the long figure-less sections,
the inbound links by anchor); per part, `_part-figures-<part>.md` (the table,
the ranking, the candidates) and `_part-notes.md` (queue entries naming no
page). The session reads its own files while the agents run; the agents never
see them.

### 4. Launch

One background agent per page, all at once, on Opus. The prompt is one line:
*Read `<prompt file>` and do what it says; the page is at `<path>`. Write your
report to `<scratchpad>/pass7-<part>/<slug>.report.md`.* Reports are not
committed. Brief per page, never per part.

### 5. Look at the part's figures as a set while they run

Open every PNG of the part in watching order, in one sitting, before reading a
report — the way a viewer flipping through the part sees them. Keep three lists:
the figures you could not read at this size (Part 3, F1); the figures that are
the same picture twice, on one page or on two (F11); and the figures whose kind
is not the mechanism's (F10). Then read `_part-figures-<part>.md`: the table,
the ranking, the gate's failures for the part. Decide the two part-wide
questions before any page is touched: **which figures are the part's own
artefacts** — the one picture a viewer of that lecture would keep — and **where
the part's visual vocabulary is inconsistent with itself** (the same thread
drawn as a subgraph here and a lane there; the same call drawn solid here and
dotted there). Run the mechanical checks for the part:

```
python tools/pass7_figures.py --part world
python tools/check_figure_names.py --pages src/systems/world --notes
python tools/check_deps.py
```

### 6. Audit the reports

A viewer's report is evidence, not a verdict. For every finding the session acts
on, look at the picture yourself and say what the viewer tripped on. *Could not
read* is checked against the render numbers (the scale, the smallest type, the
overlap list): a figure the viewer could not read and the tool measured at a
third of its size is one finding, not two. *The section needed* is the report's
centre: where the viewer's one sentence and the section's own subject disagree,
the figure is showing the wrong thing, and no amount of legibility fixes that.
*Words not yet given* is checked against the figure report's *names* line. A
*proposal* is read as a sketch: it may be right about the shape and wrong about
an arrow, and the arrows are re-derived before any of it lands. *Suspected
errors* go to the decompile: if the figure is wrong, fix it and log the
correction in [pass9.md](pass9.md) the way a pass-4 session did (what the figure
said, what the decompile says, file and line). Take nothing else on trust: a
viewer that liked every figure has not looked.

### 7. Decide, under the rulings

For each figure, in this order, with Part 3 open: **is it needed** (F11, F14 —
a figure showing what the table beside it shows, or what another figure on the
page shows, goes; a section that is an order or a branch in prose may gain one);
**is it the right kind** (F10); **does it show the thing** (F6 — the lead figure
drawn in the words of the cast, the names the prose never says either added to
the prose or taken out of the figure); **can it be read** (F1, F7, F9 — the
lanes, the density, the splitting at the mechanism's own joints); **the labels**
(F4, F3); **the caption and the lead-in** (F5); **the tick boundaries** (F8);
**the names** (F12 — every gate failure on the page resolved or ruled). Then the
part's landing page figure (F13's second half: the part's shape, numbered to the
watch order or captioned to say what the arrows mean), last.

### 8. Act

- **A figure is edited in the page's own mermaid block**, then re-rendered and
  looked at — `node tools/render_figures.js --no-build --pages systems/<part>`
  — before anything else. A figure nobody looked at after editing is the thing
  this pass exists to stop.
- **An arrow is a claim.** An arrow added, removed, reversed or relabelled is
  re-derived against the decompile with `diagram_arrows.py`'s list in hand and
  logged in [pass9.md](pass9.md): the redrawn figures and which orderings they
  assert. An arrow found wrong is a correction, logged as one.
- **A name in a figure is checked**: `python tools/check_figure_names.py
  --pages src/systems/<part>/<page>.md` after each page, and every failure on
  the page is resolved — the name corrected, qualified, or the label reworded —
  or ruled, with the ruling in the session's log. The gate is report-only until
  the close; a part session leaves its part clean anyway.
- **A lane is a key row**: `python tools/check_lanes.py --strict` after each
  page; a lane the page introduces gets its row; a lane the page drops is left
  in the key for session O's prune.
- **Prose changes are captions, lead-ins and the one sentence a figure's name
  needs** (F5, F6). A section reshaped around a figure keeps its heading and
  its anchor; where it cannot, `python tools/check_links.py --inbound` first and
  every link repointed in the same commit. No sentence is polished for voice
  (pass 8); no fact changes without the decompile open.
- **The theme is session A's** and no part session edits `mermaid-init.js`,
  `custom.css` or `book.toml`; a part that needs a device the theme lacks logs
  it for session O.
- **Nothing is dropped except by moving it or logging the cut** with the reason
  in [pass5.md](pass5.md), tagged `[kind=record]`: a figure cut is a logged cut,
  and a label's fact that leaves the figure goes into the prose or is logged.

### 9. Verify and ship

```
python tools/verify_names.py
node tools/check_mermaid.js
python tools/check_lanes.py --strict
python tools/check_figure_names.py --pages src/systems/<part>
python tools/check_deps.py
python tools/check_links.py --quiet
node tools/render_figures.js --no-build --pages systems/<part>     # and look at the PNGs once more
mdbook build
git add <your files, by name> && git commit -F <message file>     # "pass 7, session X — Part N: <summary>"
tools/deploy.sh
```

Run `check_mermaid.js` and `check_figure_names.py` after each page you touch,
not after all of them. Commit your own files by name, never `add -A`.

### 10. Record

- [pass5.md](pass5.md): strike (`- ~~…~~`, the strike **outside** the bold)
  each figure-kind entry settled, with a word saying how (done · overtaken ·
  ruled out and why), **in the same commit**; tag the entries the tool guessed
  wrong; append what the looking raised for pass 8 (a label's wording, a
  caption's register) tagged `[kind=voice]`, and for pass 10 tagged
  `[kind=book]`.
- [pass9.md](pass9.md): the session's entry — every figure redrawn and the
  orderings it asserts, every caption written (a caption is a claim about what
  the figure shows), every correction with file and line.
- [plan.md](plan.md): the session log line.
- **This file, Part 4: the session's row** — the status cell, and one line on
  what the session did, in the row's last column.

---

## Part 3 — The standard (the planning session's recommendations, for session A to rule on)

*Each recommendation is written with the number behind it, measured on
2026-09-14 by `render_figures.js` (Chrome, a 1,440px viewport, the 1,092px
reading column, the light theme), `pass7_figures.py` and `check_figure_names.py`
over the 206 figures. Session A rewrites this part as the record of what was
ratified, amended and added, and writes the rules about a figure into
`TEMPLATE.md`'s *Figures* and *Lanes*, which is where the part sessions read
them. No count here is a target; the test in each ruling decides, and the
number says where the work is.*

### F1. Legible where it stands — the column is the test, not the zoom

**Measured.** Mermaid scales a diagram wider than the column down to fit, and
the column is 1,092px. 134 of the 194 mermaid figures are shown below their
natural size; 76 below half; the median scale is 0.61. Because the base type is
16px, 89 figures show type under 9px and 107 under 11px; the smallest is 3.2px
(`identifiers-and-registries` figure 2, natural width 5,415px, shown at 0.20).
The 88 sequence diagrams are the cause: 87 are shrunk below 0.75 and 70 below
half, against 26 and 5 of the 101 flowcharts, because a sequence diagram's
width is the sum of its longest message between each pair of lanes and the
site's mermaid init does not wrap. The four generated hierarchy trees are the
maps' version of the same: shown at 0.50–0.67 with 6–8px type (`entity-anatomy`,
`entity-rendering`, `maps/hierarchy`).

**Recommendation.** A figure is legible at the column width without the zoom:
no label under 11px on screen, which at 16px base type means a scale no lower
than about 0.7. Two moves make it, in this order. **First, the theme** (F2):
the candidate init in `tools/pass7/` turns on `sequence.wrap` at 180px, sets the
site's font and drops the mirrored actor row; rendered over the whole corpus it
takes the sequence diagrams from 70 below half to **none** and from 76 under 9px
to **none** (11 under 11px), the widest from 5,415px to 1,844px — and no page
changes. The cost is height: the median sequence diagram goes from 401px to
940px tall, because a message that was one long line is now three short ones,
and three figures gain a wrapped note or block label that runs past its box.
**Second, per figure**: what is still shrunk after the theme (46 sequence
diagrams at 0.6–0.75; 22 flowcharts, five below half) is fixed in the page —
fewer lanes (F7), shorter labels (F4), a split at the mechanism's joint (F9), a
flowchart turned from `LR` to `TD`. The render is the check: a part session
re-renders after editing and reads the scale and the smallest type off
`pass7_figures.py --part`. A slide is not a separate test — the lightbox shows a
figure at 96% of the viewport, so what is legible at the column is legible
enlarged, and the recording's screen is the column.

### F2. One theme, in one file, and no colour in a page

**Measured.** No page carries a `%%{init}%%` directive and no page carries a
`classDef`, `style` or `linkStyle` line — the corpus has kept its colour out of
the pages without a rule saying so. The site ships mdbook-mermaid's default init
(mermaid's own lilac palette, Trebuchet, no wrapping), gitignored because
`mdbook-mermaid install` writes it. Verified in Chrome: a flowchart node written
`A["…"]:::server` renders with `class="node default server"` **without any
`classDef`**, and a state written `class Idle server` likewise, so a stylesheet
rule colours it and follows the theme, the way the atlas SVGs already work; a
sequence diagram's `box transparent Server thread` draws a labelled frame around
its lanes; `rect rgba(0,0,0,0.04)` draws a shaded band; a YAML `title:` renders
as a title and `accTitle`/`accDescr` become the SVG's `<title>` and `<desc>` for
a screen reader.

**Recommendation.** The theme lives in `mermaid-init.js` (committed, out of
`.gitignore`) and `custom.css`, and nowhere else: `%%{init}%%`, `classDef`,
`style` and `linkStyle` are banned in pages, and `check_mermaid.js` learns to
refuse them at the close. Session A adopts the candidate init and the candidate
stylesheet as drafted or amended — the palette read off mdBook's light and navy
themes so a figure looks like part of the page in both — after looking at
`render/candidate/` beside `render/`, and `render/gallery/` for the kinds the
corpus does not use yet. **Five semantic classes**, `server`, `client`, `netty`,
`worker`, `disk`, are the whole colour vocabulary of a flowchart, and the same
five words are a sequence diagram's `box` labels and the lane key's word lanes;
a figure that needs a sixth argues for it in the session log. Everything else
is the theme's default.

### F3. One visual grammar, corpus-wide

**Measured.** 51 flowcharts are `TD` and 27 `TB` — the same direction spelled
two ways — 20 `LR` and 3 `BT`, one of them under a heading that says the value
*falls* (`environment-attributes-and-timelines`, queue :5020). The queue names
figures where one arrow means two things (`authority`'s predicate flowchart,
`packets-and-stream-codecs`' buffer figure, `permissions`' taxonomy wired with
pipeline arrows, `the-execution-engine`'s `---` and `-.-` with no stated
meaning, `worldgen/README`'s one undirected link) and where a `Note over` stands
for a machine boundary the lanes do not draw (`synched-entity-data`,
`status-effects`, `codecs-nbt-json`).

**Recommendation.** Written into `TEMPLATE.md`'s *Figures* as a table, one row
per mark, the same on every page: a **rectangle** is a step or a call; a
**diamond** is a decision and its outgoing edge labels are its answers; a
**cylinder** is storage; a **subgraph** is a thread, a machine or a tick — never
a grouping of convenience — and carries one of the five class words or a tick's
name; a **solid arrow** is a call or a hand-off in time, a **dotted arrow** a
return or a reply, `-x` a message dropped, `-)` a message nobody waits for; a
**`Note over`** is a tick boundary or a thread hop (F8) and nothing else; a
**`box`** groups lanes by thread; direction is `TD` for anything ordered in
time or by decision and `LR` for a pipeline of stages, and `TB`, `BT` and `RL`
are not written. A figure that needs a mark outside the table says so in its
caption.

### F4. Labels are not sentences

**Measured.** 312 labels on 121 figures read as sentences — over twelve words,
or a full stop inside — 204 of them in flowcharts, 103 in sequence diagrams; the
median figure's longest label is 14 words; `server-tick`'s event loop puts a
24-word sentence in a diamond, `entity-lifecycle`'s spawn cascade has nine
sentence labels, `blocks-and-states`' write figure ten, and Part V's gate labels
carry the flag numbers the page has not minted (four figures, queue :5325). A
long label is also the width problem of F1 in another form.

**Recommendation.** A node label is a subject and a verb, at most eight words and
two lines (`<br/>` where the break matters); an edge label is the condition, at
most four words; a message is at most twelve words and a note at most sixteen. A
label that needs a sentence is a sentence the section owns: the label keeps the
name and the prose keeps the explanation. A gate carries the constant's name,
never a bare number (`UPDATE_CLIENTS`, not `2`; `flag 2` only where the page
has paired the name and the number above the figure). `pass7_figures.py` counts
the sentence labels and the number gates per figure; a session reads its own
labels aloud.

### F5. Every figure has a caption, and the section reads it

**Measured.** No figure in the book has a caption. 115 of 206 open their section
— a heading directly above, nothing between — and 118 have no lead-in sentence;
132 are pointed at by a sentence in their section (*the figure*, *the bar*,
*read it as*, *above*, *below*) and 74 are not; **51 have no lead-in, no caption
and no sentence pointing at them** — a picture the page never mentions. The
built HTML puts a `<p>` directly after each figure's `<pre class="mermaid">`, so
the paragraph after a figure is addressable by a stylesheet; verified with
mdBook that a `<figure>` wrapper with blank lines around the fence also works,
but its `<figcaption>` is raw HTML, whose backticks the name gate cannot read.

**Recommendation.** The caption is **the italic paragraph directly after the
figure** — one sentence in the book's voice: what the picture shows and what to
look for in it (*The four gates a spawn attempt passes before a mob object
exists; the boundary marked* only now *is the one that matters.*). It is
markdown, so `verify_names.py` reads its names and `llms-full.txt` carries it;
`custom.css` styles exactly that paragraph (`pre.mermaid + p:has(> em:only-child)`,
in the candidate stylesheet) and numbers it with a CSS counter, so an
uncaptioned figure looks as it does today until it gets one. The sentence
*before* a figure ends by saying what the figure will show, unless the figure
opens its section — a lead figure may — and then its caption does that job. The
paragraph after the caption reads the picture: it names the thing the reader
should see. `pass7_figures.py` measures all three (the lead-in, the caption, the
pointer), and a figure with none of them is the first thing a session looks at.

### F6. The figure the page cannot yet be read against

**Measured.** This is the pattern sessions C, D and F of pass 6 each found and
sent whole, and it is now a number: for every identifier-shaped token in a
figure's labels, whether the prose says it *before* the figure, only *after* it,
or *never*. **139 of the 195 mermaid figures introduce at least half of their
names before the prose does**; of the 120 lead figures, 87 do, and 69 open their
section with nothing above them. **151 figures carry a name the prose never
says — 614 tokens — and 88 carry three or more**: `entity-lifecycle`'s spawn
cascade names fifteen methods that appear nowhere in the page's prose,
`server-tick`'s lap sequence fourteen of its nineteen names after the figure.
Those figures are the only home of those facts, and they are the ones pass 4's
standing rule says to read first ("the figure against the section under it").

**Recommendation.** A figure names what its section explains. A lead figure —
the page's artefact, sitting under the cast — is drawn **in the words of the
cast**: the class names the cast table has just given, and verbs for what
happens (*asks*, *writes*, *sends the packet*), not method names the reader
meets 150 lines later; the method names belong in the section figures that
follow their prose. A name the prose never says is either given one sentence in
the prose — the sentence the figure was standing in for — or taken out of the
figure. The test is the report's *names* line: a lead figure at 90% first-met
has been drawn from the decompile rather than from the page.

### F7. Lanes: at most seven, each earning its place, one meaning corpus-wide

**Measured.** Lanes per sequence diagram: eight on 7, seven on 39, six on 25,
five on 9, four on 5, three on 2, two on 1 — `TEMPLATE.md` says at most seven.
The queue names four lanes that carry one message and decide nothing
(`scheduled-ticks`' `LevelChunk`, `input-to-movement`'s `LE`, `authority`'s
`SL` used only in a note, `starting-a-server`'s `Worker` with no cast row), two
lanes standing for two objects (`synched-entity-data`'s one `SED` for both
containers; `status-effects`' one `LE` for two machines; `game-events`' one
`SculkSensorBlock` for the block and its block entity), and one object given
two lanes (`anatomy`'s `MinecraftServer` and `IntegratedServer`). The key has
342 rows, 298 in use and **44 no page declares** (`check_lanes.py --unused`),
among them `PTT`, the template's worked example of the nested-class rule, whose
pilot page has since become a flowchart; `RCPL` is the one class with two lanes
on purpose. Messages between lanes cross intermediate lifelines 573 times, which
mermaid draws under the text; the candidate theme's wrapping triples that count
and is the reason F1's theme needs F7's lanes.

**Recommendation.** At most seven lanes; a lane that carries one message and
decides nothing is folded into a note or a label on the arrow; one object is one
lane (a subclass and its base are one lane, named for the object); two machines
are two lanes, or one lane in a `box` for each machine, never a `Note over`
saying *now the client*. The key is pruned to lanes in use at the close, `PTT`'s
replacement chosen then, and `check_lanes.py --unused` joins `deploy.sh` as a
report. Lane *order* is the order of first use, left to right, so that the first
message reads left to right.

### F8. The tick boundary is a band, and every trace that crosses a tick shows one

**Measured.** 111 notes on 58 of the 88 sequence diagrams name a tick, a frame
or *later*; **30 sequence diagrams have no tick bar at all**, and the queue names
traces that cross a tick without one (`status-effects`, whose two machines read
as sequential; `the-client-loop`'s flowchart, the part's most-cited picture,
with no tick marking on the page that is about the tick). `TEMPLATE.md`'s device
is `Note over X: a later tick`; Chrome renders a `rect` band with a note inside
it, which shows the tick's *extent* and not only its edge (`render/gallery/
gallery--f1.png`).

**Recommendation.** A trace that crosses a tick, a frame or a thread shows the
crossing as a **shaded band** (`rect`, the theme's one band colour) with a
`Note over` all lanes naming the tick or the phase; a flowchart that spans ticks
puts each tick in a subgraph named for it. The *no reply* annotation (`-->>`
with *nothing*) stays as the template has it. A trace with no crossing has no
bar — the device is spent, not defaulted.

### F9. As complex as it needs to be, as simple as it can be — the density budgets

**Measured.** Flowcharts: a median of 10 nodes, nine over 15, a maximum of 26
(`loot-tables`' funnel) and 39 edges (`entity-lifecycle`'s cascade); 42 figures
are over 1,200px tall on screen and `blocks-and-states`' write figure is 3,766px
— three and a half screens. Sequence diagrams: a median of 12 messages, one over
20 (`starting-a-server`, 26), notes up to eight in one band
(`post-processing`). The parts-dependency figure — thirteen nodes, 27 edges —
has **26 edge crossings**; `math-and-primitives`' coordinate figure has 5 on 8
nodes.

**Recommendation.** No budget is a target, and the test is the viewer's first
question — *what does it show?* — answered in one sentence. But a flowchart over
about fifteen nodes, a sequence over about twenty messages, or a figure taller
than a screen is split **at the mechanism's own joint**, the one the prose
already names (the spawn cascade at *only now does a Mob object exist*: the type
filter and the object filter; the write figure at *back in `Level.setBlock`*:
the chunk write and the tail), and each half gets its own caption and its own
paragraph. Every node is a step or a decision the prose names; a node that
restates the paragraph is cut; a chain of rejections is one node with a list of
conditions only where the conditions have no order, and an ordered chain
(`hunger-and-experience`'s if/else-if regen) is drawn in its order. A dependency
graph with 26 crossings is redrawn by rank (the parts in the order they are
watched, arrows only downward) or generated.

### F10. The true shape — the kind of figure follows the mechanism

**Measured.** 88 sequence diagrams, 101 flowcharts, 6 state diagrams, 11
generated SVGs. The site's mermaid parses **twenty-one kinds** (the checker's
harness now agrees with the browser on `pie`, `packet-beta` and `radar-beta`);
the corpus uses three, and `TEMPLATE.md` names a fourth, `classDiagram`, for
vocabulary pages, which no page uses. `render/gallery/` holds one of each kind
that a page here could want, in the candidate theme: a class diagram of what a
chunk section holds; a memory layout as `block-beta`; a packet's bytes as
`packet-beta`; a tick's phases against the clock as a `gantt`; a number that is
a curve as an `xychart` (the sword's attack-strength scale); a 2×2 of who decides
and who predicts as a `quadrantChart`; the Reference shelf as a `mindmap` where a
flowchart's arrows would assert an order that does not exist; a session's phases
as a `timeline`. Three secondary state diagrams (`points-of-interest`,
`tickets-and-loading`, `entity-lifecycle`) may be their page's true picture
(session P's question, queue :3167); the queue names figures whose kind is
wrong outright — `pathfinding` drawing the same pipeline as a flowchart and as a
sequence, `permissions`' taxonomy as a pipeline, `reference/README`'s taxonomy
that its own table carries faster, `the-gui-render-tree`'s two pictures in one
frame.

**Recommendation.** `TEMPLATE.md`'s shapes table keeps its rule — *if the truth
is a graph, do not draw a conversation* — and gains the menu with a picture per
row: a trace is a sequence diagram; a branch or a pipeline a flowchart; phases a
state diagram; what an object *holds* a class diagram (the vocabulary page's
figure, at last); a layout in memory or on the wire a block or packet diagram; a
quantity a chart, with its numbers real and its caption saying whether they are
illustrative; a taxonomy a mind map or, better, the table; a comparison a table
and never a figure. Two kinds have traps the gallery shows — `packet-beta` cuts
a long field label, `quadrantChart` lets a point label collide with a quadrant
label — and the renderer flags both. A new kind is used where it shows the thing
in fewer marks than the old one, not for variety; diversity is the consequence
of drawing the mechanism, not the aim.

### F11. Two figures for one mechanism are one figure

**Measured.** The queue names five: `prediction-and-acks` (a state diagram of the
two machines and a sequence of the refusal, the argument living in the prose
both times); `pathfinding` (a flowchart at the top and a sequence two thirds
down of the same pipeline); `entity-rendering` (a four-stage flowchart and a
zombie sequence saying the same thing twice, the second in more detail, and both
disagreeing with the cast); `items-and-stacks` and `data-components` (two pages
drawing the same object); `containers-and-menus` (a ladder flowchart restating
the trace in its bottom four boxes). 68 pages carry two or more figures.

**Recommendation.** One mechanism, one figure, on the page that owns the
mechanism (`TEMPLATE.md`'s ownership rule, applied to pictures: *within a part,
the page whose figure draws it owns it*). Where two figures show one thing, the
one that shows the section's thing (F5, question 3) stays and the other is a
logged cut, or is redrawn to show a *different* thing — the states rather than
the order, the objects rather than the calls. A second figure on a page earns
its place by showing what the first cannot.

### F12. The gate over names in figures

**Measured.** `check_figure_names.py` reads 2,619 identifier-shaped tokens in
the 195 blocks — participant expansions, node and edge labels, messages, notes,
subgraph titles, state names — and checks them against the decompile as
`verify_names.py` checks the prose, with inherited members accepted and a
sequence message's head checked against the lane it is sent to. **119 do not
resolve as written** (Part VI 20, IV 19, II 13, V 13, III 12, VII 10, X 10, XI
10, XII 4, XIII 4, I 1, VIII 1, IX 1, Reference 1): a class that does not exist
(`ChunkBuffer`, `WorldDataSupplier`, `PreparedFrame`), a message naming a
method its target lane does not have (`SL->>CH: broadcastChangedChunks`,
`DS->>SL: createLevels`), a member no class has. Beside them, **362 notes** the
gate does not fail, because the convention is session A's to set: 157
unqualified members in flowchart node labels (`runAllTasks`, with no class
beside it), 82 messages whose bare lower-case head is not a member of the lane
it is sent to (`load`, `spin` — English or a method, the label cannot say), 47
unqualified members in sequence notes, 25 nested classes named without their
outer class (`YClampedGradient` for `DensityFunctions.YClampedGradient`,
`SpawnState`, `PlayerTicketTracker`), 21 in state-diagram edge labels, 20 in
flowchart edge labels, 5 in subgraph titles, 5 calls. The gate's parser also
gave the class index the **139 page pairs** it could not see (pass 5, session
A's finding); `verify_names.py --index` merges them on every deploy.

**Recommendation.** The gate runs report-only through the pass — `deploy.sh`
already prints it — and `--strict` at the close, when every one of the 119 has
been corrected or ruled. The conventions, for session A: **(a)** a sequence
message that names a method names one of the lane it is sent to, inheritance
included, and the message's head is that method — where the call really goes
elsewhere, the lane is wrong; **(b)** a member in a flowchart, state or note
label is written `Class.member`, as the prose writes it, because nothing else
qualifies it (157 + 47 + 21 + 20 to rewrite, most of them the fix F4 makes
anyway); **(c)** a nested class is `Outer.Inner` in a figure as in the prose;
**(d)** a bare lower-case message head that is not a member is prose (*load,
wrapped in Util.blockUntilDone*) and stays, or becomes the qualified call it
stands for. Under (b) and (c) the notes become failures, and the gate at the
close is the same test the prose has passed since pass 1: **verified against
26.2 is a test, not a claim — for the figures too.**

### F13. The generated figures, and the landing pages' own

**Measured.** Eleven generated SVGs: the packages treemap (three pages, 9px
labels with hover titles, at scale 1), the two bar charts, the four hierarchy
trees (0.50–0.67, type 6–8px on every label) and the render-state tree (0.49,
5.9px). The thirteen landing-page figures are hand-drawn flowcharts of the
part's pages; the queue names five (`server/README`'s order that is neither the
watch order nor the shape sentence's; `world/README`'s conveyor drawn as a
cycle; `items/README`'s chain where the prose claims two tiers and its orphan
node; `rendering/README`'s arrows that need a disclaimer; `worldgen/README`'s
undirected link) and the exemplar `commands/README` numbers its nodes to the
watch order. `reference/README`'s shelf figure and `maps/README`'s pipeline
figure are the only figures in their tiers that are not generated; four
hand-kept Reference pages have no figure and the queue asks that the tier's
exemption be said once (:6259).

**Recommendation.** `map_source.py`'s tree emitter folds or wraps so that a
tree is shown at scale 1 with 12px labels — the entity tree in two columns, or
the deepest branches folded with a count — a tool job for session A or the two
part sessions that include one (VI, XI), regenerated by `deploy.sh` as today. A
landing page's figure is the part's shape **numbered to the watch order** (the
exemplar's device) with a caption saying what an arrow means (*what the next
page can assume*), so the shape sentence, the figure and the order agree; a
landing figure that needs a disclaimer is the wrong figure. The Reference tier's
one-figure exemption is one sentence on `reference/README`, and its shelf figure
is a table or a mind map (F10).

### F14. A figure for the section that has none

**Measured.** 214 sections over forty lines carry no figure, on 102 pages; 111 of
them have no H3 either; 100 carry twenty or more order, branch, cycle or
containment words per hundred lines — *then, before, after, first, last; if,
unless, otherwise, refuses; again, every tick, loop; contains, inside, owns,
tree* — which is the prose form of a picture. The densest: `functions-and-macros`'
*What calls a function, and when* (54 per hundred), `block-breaking`'s *Remove,
damage, roll, drop*, `advancements`' *The screen at the other end*,
`what-the-client-is-told`'s *The rate the client asks for*, `the-two-phase-tick`'s
*The bracket, and what survives it*, `jigsaw-and-templates`' *The assembly loop*
(`pass7_figures.py --candidates`). Every system page has at least one figure, so
this is about sections, not pages.

**Recommendation.** A section gains a figure where the viewer asked for one
(Part 1, *the section that wanted a picture*) and the session can draw the
section's claim in ten nodes or fewer; the candidates list is where to look, not
a quota, and a section whose order is three steps is better as three sentences.
A figure added is a figure under every other ruling here: captioned, in the
words of the section, its names gated, its arrows logged in [pass9.md](pass9.md)
as claims.

### F15. The exemplar

**Recommendation.** `entities/entity-lifecycle`, rewritten end to end under
F1–F14 by session A with one viewer's report in hand. It has three figures of
three kinds — the spawn cascade (the densest flowchart in the book: 21 nodes,
39 edges, nine sentence labels, shown at 0.28 with 4.5px type, fifteen names the
prose never says, six gate failures, and a queue entry saying its three group
attempts cannot be read off it because it never loops), the entry sequence
(twelve names the prose never says, shrunk to 0.43) and the visibility state
diagram (the queue's question of whether a secondary state diagram is the page's
true picture) — so one page exercises the size ruling, the density ruling and
the split at *only now*, the labels ruling, the names ruling, the caption, the
kind, and the gate. `server/server-tick` is the second candidate if session A
wants a trace as the exemplar instead: the 7-lane lap at 0.29 with fourteen of
its nineteen names first met there, and the event loop with the 24-word diamond
and the two converging edges that mean opposite things. The part sessions read
the exemplar before their own part, the way pass 6's read
`environment-attributes-and-timelines`.

### F16. What session A does not do

It reads no part and redraws no figure but the exemplar's; it changes no fact
without the decompile open (an arrow found wrong on the exemplar is re-derived
and logged, the standing rule); it writes no prose beyond captions, lead-ins
and the one sentence a name needs; it moves no page. It does adopt or amend the
theme (F2), which is the one change that touches every page at once and is why
it is session A's and no part session's; it rewrites `TEMPLATE.md`'s *Figures*
and *Lanes* to Part 3 as ratified; and it leaves the lane key's prune, the gate's
`--strict`, the tree emitter and the frame's figures to session O and the part
sessions that own them.

---

## Part 4 — The schedule

Sessions B–N run in sidebar order, one part each, after A; O closes. The numbers
are what `render_figures.js`, `pass7_figures.py`, `check_figure_names.py` and
`pass5_queue.py` found on 2026-09-14, before any session ran — they say where the
work is, and no count is a target.

**The figures by part** (`pass7_figures.py --summary`, the render at 1,440px;
*most names first met here* is a figure introducing at least half of its names
before the prose does; *gate* is `check_figure_names.py`'s unresolved names and
notes; *queue* is the open `figure` units):

| part | pages | figures | seq / flow / state / map | shrunk below 0.75 | type under 9px | overlap, overflow or through | opens its section | most names first met here | three or more names never in prose | sentence labels | lanes over 7 | nodes over 15 | over 1200px tall | gate: unresolved / notes | queue |
|---|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|
| I · anatomy | 3 | 4 | 1 / 2 / 0 / 1 | 2 | 2 | 0 | 1 | 2 | 1 | 3 | 0 | 0 | 0 | 1 / 6 | 4 |
| II · foundations | 8 | 17 | 11 / 6 / 0 / 0 | 15 | 11 | 2 | 13 | 13 | 6 | 11 | 0 | 0 | 0 | 13 / 24 | 6 |
| III · server | 6 | 10 | 7 / 3 / 0 / 0 | 7 | 5 | 1 | 6 | 7 | 1 | 4 | 0 | 1 | 2 | 12 / 25 | 12 |
| IV · world | 11 | 24 | 10 / 12 / 2 / 0 | 14 | 12 | 2 | 18 | 17 | 13 | 18 | 0 | 1 | 7 | 19 / 63 | 10 |
| V · blocks | 8 | 10 | 5 / 5 / 0 / 0 | 6 | 5 | 2 | 5 | 6 | 5 | 8 | 0 | 1 | 3 | 13 / 26 | 11 |
| VI · entities | 10 | 22 | 9 / 11 / 1 / 1 | 14 | 12 | 0 | 8 | 17 | 13 | 14 | 0 | 1 | 6 | 20 / 63 | 12 |
| VII · items | 9 | 17 | 8 / 9 / 0 / 0 | 9 | 7 | 2 | 7 | 10 | 7 | 6 | 0 | 3 | 6 | 10 / 31 | 15 |
| VIII · player | 8 | 10 | 5 / 5 / 0 / 0 | 5 | 5 | 0 | 5 | 5 | 3 | 2 | 1 | 0 | 1 | 1 / 7 | 10 |
| IX · networking | 6 | 12 | 4 / 6 / 2 / 0 | 7 | 5 | 4 | 10 | 10 | 5 | 5 | 0 | 1 | 2 | 1 / 19 | 10 |
| X · client | 13 | 18 | 8 / 9 / 1 / 0 | 10 | 6 | 5 | 11 | 15 | 12 | 15 | 2 | 0 | 5 | 10 / 26 | 10 |
| XI · rendering | 12 | 20 | 8 / 11 / 0 / 1 | 10 | 9 | 4 | 8 | 16 | 9 | 17 | 3 | 0 | 5 | 10 / 23 | 14 |
| XII · worldgen | 11 | 15 | 7 / 8 / 0 / 0 | 8 | 6 | 8 | 10 | 10 | 6 | 7 | 1 | 1 | 1 | 4 / 35 | 8 |
| XIII · commands | 10 | 13 | 5 / 8 / 0 / 0 | 6 | 5 | 5 | 8 | 9 | 5 | 10 | 0 | 0 | 4 | 4 / 7 | 7 |
| Reference | 3 | 3 | 0 / 3 / 0 / 0 | 3 | 1 | 2 | 1 | 2 | 2 | 1 | 0 | 0 | 0 | 1 / 7 | 21 (with the frame) |
| the frame | 7 | 11 | 0 / 3 / 0 / 8 | 6 | 4 | 1 | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 / 0 | — |
| **all** | 125 | 206 | 88 / 101 / 6 / 11 | 122 | 95 | 38 | 115 | 139 | 88 | 121 | 7 | 9 | 42 | 119 / 362 | 150 |

No figure carries a caption; 51 are pointed at by nothing. Lanes per sequence
diagram: eight on 7, seven on 39, six on 25, five on 9, four on 5, three on 2,
two on 1. Flowchart nodes: median 10, maximum 26; directions `TD` 51, `TB` 27,
`LR` 20, `BT` 3. Tick bars: 111 notes on 58 of 88 sequence diagrams; 30 have
none. Under the candidate theme, the sequence diagrams' *shrunk below 0.75* falls
from 87 to 46 and *type under 9px* from 76 to 0. The 21 frame-and-Reference
queue units include the lane key's 44 unused rows, the four figure-less
Reference pages, the two tier figures, and the parts-dependency figure's 26
crossings.

### The sessions

The **status** column is the one the owner reads: `—` until the session runs,
then *done <date>*, written by the session itself in step 10. The last column
is what the tools and the queue put in front of the session; the session
appends one line saying what it did.

| session | status | part | pages | figures | queue | the charter's named items, and what the tools add |
|---|---|---|---:|---:|---:|---|
| **A** | — | the standard | the exemplar + `TEMPLATE.md` + the theme | 3 | — | Part 3 above: ratify, amend or reverse F1–F16 and rewrite Part 3 as the record; **the theme** (F2) — look at `render/candidate/` beside `render/` and `render/gallery/`, adopt or amend `tools/pass7/mermaid-init.candidate.js` and `figure-classes.candidate.css` into `mermaid-init.js` (committed, out of `.gitignore`) and `custom.css`, re-render the corpus and record the numbers; `TEMPLATE.md`'s *Figures* rewritten to the visual grammar (F3), the label budgets (F4), the caption device (F5), the tick band (F8), the density rule (F9) and the menu of kinds with the gallery's pictures (F10), and its *Lanes* to F7; the mermaid rules corrected to what 11.6.0 rejects (pass 4's session O measured it; `check_mermaid.js` now parses the `structuredClone` kinds); the exemplar `entities/entity-lifecycle` rewritten with a viewer's report in hand (F15) — the cascade split at *only now*, every label a subject and a verb, three captions, the names gated clean; its entry in [pass9.md](pass9.md). |
| **B** | — | I · Anatomy, II · Foundations | 3 + 8 | 4 + 17 | 4 + 6 | **I:** `anatomy`'s start-up sequence gives `MinecraftServer` and `IntegratedServer` two lanes for one object (:5073), and its two-loops flowchart draws `runTick` beside the four calls that happen *inside* it — a nesting drawn as a sequence (:5079), at 0.28. **II:** 15 of 17 figures shrunk, 11 with type under 9px, and the widest figure in the book (`identifiers-and-registries` figure 2, 5,415px); 13 of 17 open their section; `codecs-nbt-json`'s four-path table *is* the figure and explains five mechanisms other parts own (:234), and its Checksum figure spans two machines with one arrow crossing from client to server with no lane between (:5092); `data-components` and `items-and-stacks` draw the same object (:4409, decide here with VII's session) and `data-components`' shape figure runs an edge back into the subgraph it reads away from (:5106); `data-driven-types`' trace gives `unpackLootTable` to a `ChestBlockEntity` lane where the prose has `RandomizableContainer` — two arrows to re-derive (:5096); `tags`' six sentence labels (:5088) and its lead figure of a shape not the page's (:3167); `text-components`' `ComponentSerialization` standing for the codec and the wire (:5101); 13 gate failures. |
| **C** | — | III · The server | 6 | 10 | 12 | The part-wide pattern named first here: the lead figures the page cannot be read against — `server-tick`'s lap (fourteen of nineteen names first met there), `server-level-tick`'s, `players-and-sessions`' join sequence (:5176). `server-tick`'s event loop: fourteen edges, node `C` a 24-word sentence in a diamond, two converging edges meaning opposite things (:703, :2085, :5170); `server-level-tick`'s twenty-node vertical chain with a gate clause on every label (:5164) and the profiler zones as prose or as labels (:715); `starting-a-server`: 27 items, the largest single diagram in the part (:706, :2089), a `Worker` lane with no cast row and a `Worker-->>WL` arrow labelled as going to `Main` (:5185); `how-a-server-dies`' `/stop` figure asserting five things explained in the six H3s below it (:5188); `players-and-sessions`' `PLAYER_SPAWN` ticket question (:5262); `server/README`'s part figure in the runtime order rather than the watch order — numbering or a caption (:708); 12 gate failures, among them `DS->>SL: createLevels` and `SL->>CH: broadcastChangedChunks`. |
| **D** | — | IV · The world | 11 | 24 | 10 | The largest part by figures: 24, of which 18 open their section, 17 introduce most of their names first, seven are over 1,200px tall, and 19 names fail the gate. Three lead figures the page cannot yet be read against — `chunk-storage`'s flowchart, `chunk-generation-pipeline`'s pyramid with radius 11 on its `EMPTY` node, `fluids`' bucket sequence (:367); `environment-attributes-and-timelines`' `flowchart BT` under a heading that says the value *falls* (:5020 — the figure is the cheaper end, the heading is an anchor seven pages land on); `game-events-and-vibrations`' fifteen-node gate flowchart with edge labels of five and six conditions (:378, 2,395px tall) and its trace's one lane for the block and its block entity (:381); `lighting`'s batch flowchart missing `checkNode` (:385); `scheduled-ticks`' `LevelChunk` lane that decides nothing (:388); `chunk-anatomy`'s two graphs over five names (:393) and its section figure without the light (:472); `world/README`'s conveyor drawn as a cycle (:390); whether `points-of-interest`'s and `tickets-and-loading`'s secondary state diagrams are the page's true picture (:3167). |
| **E** | — | V · Blocks | 8 | 10 | 11 | **The flag words** (:5325): four lead figures label their gates with bare flag numbers the page has not minted; session E fixed the prose half and this session decides whether a gate may carry a constant's name (F4), on `blocks-and-states`' write figure first — 3,766px tall, 21 nodes, ten sentence labels, the most-linked figure in the part, two subgraphs already (:1942, :5333: no paragraph beside its build-time figure, which introduces four classes the cast omits). `block-interaction`'s sequence: eight arrows that are later sections in shorthand (:5337); `block-entities`' three names for one menu (:4071) and `ServerChunkCache.blockChanged` on the `ServerLevel` lane (:5341); `signal-and-dust`'s sequence showing only the *on* case where the hook is the line going dark — a third dust (:5344); `diodes-and-observers`' channel flowchart re-deriving the channels in its labels (:4074, :5350 — the figure was the only definition on the page); `pistons-and-block-events`' flag table wanting the wide treatment (:4069); 13 gate failures. |
| **F** | — | VI · Entities | 10 | 22 | 12 | The exemplar lives here (F15): session A's `entity-lifecycle` is read first and the part is judged against it. The most gate failures of any part (20) and 13 figures with three or more names the prose never says. `authority`'s predicate flowchart draws two relations with one arrow — *what the root asks* and *what defaults to the root* (:5460); its boat sequence declares an `SL` lane and sends nothing on it (:3919); `entity-anatomy`'s lead flowchart names nine mechanisms below it (:5487) and its figcaption for the generated tree omits the key (:3921) — and the tree itself is shown at 0.62 with 7.5px type (F13); `pathfinding` draws the same pipeline twice, the sequence running past its own section (:5481); `synched-entity-data`'s one `SED` lane for two containers (:5475) and its gate flowchart drawing one of three callers (:5479); `movement-and-collision`'s two edges from `MORE` both labelled *no* (:5466); `ai-goals-and-brains`' node `K` holding the explanation the prose gives four paragraphs later (:5484). |
| **G** | — | VII · Items and inventories | 9 | 17 | 15 | The most queue units of any part. `items/README`'s figure: a chain where the prose claims two tiers, an orphan node that is true and reads like an omission, no edge between `EC` and `LO` (:1747, :4367, :4405 — a landing figure numbered to the watch order, F13); `containers-and-menus`' shift-click sequence before every paragraph that explains it, off by one step against the prose (:4330), and its ladder flowchart restating the trace (:4339); `loot-tables`' opening sequence with no client lane and an arrow that reads the wrong way (:4342), its sixteen-edge funnel and the note that carries a correction (:4414), and *three fan-outs* over four (:1246); `items-and-stacks`' `ItemStack` figure with edgeless `count` and `popTime` and the dotted arrow to a node defined two lines down (:4363), and the same object drawn on `data-components` (:4409); `enchanting`'s 50 that appears only in the figure (:4360); `enchantments`' hook flowchart omitting the flag row the paragraph points at (:4352); `recipes`' three senses of *enabled* (:4356); `using-an-item`'s two disconnected graphs in one box (:4348); `contexts-and-predicates`' stray node (:1752); `the-spear`'s label compressing two sides into one (:3568). |
| **H** | — | VIII · The player | 8 | 10 | 10 | The lightest part by the gate (one failure) and the numbers; the queue is about shape. `hunger-and-experience`'s regen flowchart: three branches from one node whose *order is the rule* — a numbered chain, or one arrow (:5592); its sequence labels a packet *sent first* and draws it second, from a lane that has not acted, and one arrow runs on both sides that one set of lanes cannot show (:5597); `status-effects`' one `LE` lane for two machines and no tick bar, so the two branches read as sequential (:3576, :5601 — F7 and F8 together); `input-to-movement`'s `LE` lane with one arrow and no cast row (:5613); `the-spear`'s flowchart missing the second thing the prose stops on (:5609) and its label compressing two sides (:3568); `the-sword-swing`'s data nodes and control nodes on the same arrows and its `GATE` that asks *either term above zero?* without naming the two (:5605), and the swing packet the body now mentions (:5615); `player/README`'s edge labels (:3573). |
| **I** | — | IX · Networking | 6 | 12 | 10 | `what-the-client-is-told`'s sixteen-node cascade carrying the page's whole argument (:4566), with the `FREE` node branching off before gate 3 is drawn — a forward reference inside the figure (:5715); `packets-and-stream-codecs`' seven-node chain of twenty-word labels (:4569), four of its boxes explained 80–150 lines later (:5729), and its buffer figure's three arrows meaning two things — *binds* and *extends* (:5725); `protocol-phases`' `NEGOTIATING` with no edge in or out — may a state machine contain a state nothing reaches? (:5733) — and its `W` box naming objects by position (:5737); `the-connection`'s note handing over six handler names ninety lines early (:5741); `chat-and-signing`'s flowchart omitting the one refusal that does not close the connection (:5720); `networking/README`'s fourteen-word edge label between two subgraphs (:4562); 10 of 12 figures open their section; four figures with an overlap or overflow. |
| **J** | — | X · The client | 13 | 18 | 10 | Twelve figures with three or more names the prose never says, the most after IV and VI. `the-gui-render-tree`'s first flowchart is two pictures in one frame, `UP` and `WALK` pointing at no node (:5829); `the-client-loop`'s one-turn flowchart, the part's most-cited picture, has no tick-boundary marking on the page that is about the tick (:5841 — F8 for flowcharts); `prediction-and-acks`' two figures for one mechanism (:1664) and its state-diagram exits that are sentences (:1621); `options`' eleven-node flowchart with two labelled branches out of `LISTEN` (:5838); `text-and-fonts`' `Font->>FSet: getGlyph` — true as an object interaction, misleading as a call (:4694, :5843); `the-client-level`'s `applyLightData` drawn after the queued lambda, one arrival or two (:5834); `sound-engine` figure 1 at 0.23, the second-widest in the book, eight lanes and three sentence labels. |
| **K** | — | XI · Rendering | 12 | 20 | 14 | Three figures with eight lanes, the most of any part. `entity-rendering`'s two figures say the same thing twice (:4787) and disagree with the prose and the cast on where the frustum test sits and who drives two of the four stages (:5930); `rendering/README`'s pipeline figure declares its arrows reading order only and two of them a frame's reverse (:5953 — the wrong figure, F13); `lightmap-fog-and-sky`'s trace draws three of the five askers its table promises (:5924); `the-window`'s six-callback flowchart under a section discussing seven (:4790) and its retry flowchart making the error verdict look inert (:5935); `visibility-and-the-frame-graph`'s six-node figure under *Five stages* (:4793) and its outline chain as one node where the prose has four passes (:5948); `post-processing`'s eight-line note band doing the work four arrows would (:5944) and its *what a player sees* column (:1549); `particles`' server branch starting from a lane with no incoming arrow (:5940); `blaze3d`'s cluster labels over its nodes (the renderer's overlap list); `models-and-atlases`' single figure over 330 lines (:2367); the render-state tree at 0.49 (F13). |
| **L** | — | XII · World generation | 11 | 15 | 8 | Eight figures with an overlap or an overflow, the most of any part, most of them subgraph titles drawn over their first node: `density-functions`' three panels, whose root node is `Ap2` in all three, a name glossed nowhere (:6073); `terrain`'s cell-loop figure and its *Four statuses* flowchart with five boxes (:6067); `blending`'s dashed annotation node that the prose now owns (:1450, :6063 — remove it) and its *the two maps* named a paragraph below the figure; `biomes`' return from `Climate.RTree` skipping two lanes (:6059); `trees`' `UNCLIPPED` twenty lines before it is defined and `leafRadius` for the prose's `foliageRadius` (:6070); `hand-built-structures`' `findCollisionPiece` addressed to the builder where the prose addresses the accessor (:6076) and its two loop labels outside their boxes; `jigsaw-and-templates`' block label outside its box; `worldgen/README`'s undirected link (:6081). |
| **M** | — | XIII · Commands and data packs | 10 | 13 | 7 | `entity-selectors`' *Resolve* flowchart routes the players-only branch past both decisions the prose makes — the **shape** is wrong (:6143); `permissions`' first figure is a taxonomy wired with pipeline arrows, `Q --> S --> C` asserting a becoming, and its `CL` node the densest label on the page (:6151); `brigadier-and-commands`' trace opening on two `CSug->>CPL` arrows that read as messages sent under a paragraph whose point is that the parse never leaves the machine (:6156), and its node saying `performCommand` reads limits *from the level's game rules* (:4894 — reword the node); `the-execution-engine`'s four-panel queue figure with `---` and `-.-` unexplained on a page whose subject is queue order (:6161) and its three reserved lanes no page uses (:4890 — session O's prune); `game-tests`' nesting figure with unlabelled edges between subgraphs and one subgraph with no internal edge (:6165); `commands/README` is the landing exemplar for numbering (:708) and its subgraph title overlaps a node. |
| **N** | — | the frame and Reference | the introduction, `lectures.md`, the atlas, the hand-kept Reference pages | 14 | 21 | The parts-dependency figure — shared by the introduction and `lectures.md` — has **26 edge crossings** on thirteen nodes, the worst object in the book: redrawn by rank in the watch order, or generated by `check_deps.py`'s reading of the landing pages (F9); the introduction's two-programs figure draws `Worker-Main-n` with no sentence introducing it and dashed arrows nobody explains (:6247); `maps/README`'s pipeline figure, the one atlas figure that is not generated (:6245); `reference/README`'s shelf taxonomy with sentence-long subgraph titles, no caption, and a table beside it that says it faster (:6240), and the tier's one-figure exemption said once for the four figure-less pages (:6259); `math-and-primitives`' eight-node, eighteen-edge coordinate figure with sentence labels and five crossings (:6252); `threads`' edge label of a kind the section is not about (:6255); `maps/hierarchy`'s same SVG (:3922) and the four trees' size (F13, with `map_source.py`); the lane key's 44 unused rows (:2256, :4890) and `lanes.md`; the class index, blind to diagrams until this planning session (:2178 — struck by it). |
| **O** | — | the close | — | — | — | **The gate flipped**: every one of the 119 unresolved names corrected or ruled, the F12 conventions applied so the notes are failures, `deploy.sh` runs `check_figure_names.py --strict`, and `CLAUDE.md`'s rule 5 says the figures are under it; `check_mermaid.js` refuses `%%{init}%%`, `classDef`, `style` and `linkStyle` in a page (F2); the lane key pruned to lanes in use and `PTT`'s replacement chosen, `check_lanes.py --unused` in `deploy.sh`; the theme's final form and the caption counter; `TEMPLATE.md`'s *Figures* and *Lanes* read against the finished parts; the thirteen landing figures read as one set, numbered to the watch order and captioned; the corpus re-rendered and re-measured against Part 4's table (scale, type, overlaps, captions, names first met, the gate) and the difference written down; the pass's own strikes audited (a strike is a claim); [pass9.md](pass9.md)'s entries checked for shape — every redrawn figure listed with its orderings; the verdict on whether the pass earned its cost; pass 8's charter detail written with the wording debt the figures raised (captions' register, label wording) counted afresh; this file's Part 5 left for the pass-8 planning session to archive. |

**What no session does**: change a fact without the decompile open (the
standing rule — an arrow is a claim); move a page (after pass 5 no page moves);
edit the theme after session A (a device the theme lacks is logged for O);
polish a sentence for voice (8); add a figure for variety (F10's last sentence);
draw from the decompile what the page's prose does not say (F6 — the figure
names what its section explains, and a fact the figure alone carried is given
its sentence or logged as a cut).
