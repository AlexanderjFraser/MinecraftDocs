# The page — a menu of shapes

*Rewritten by pass-3 session A (2026-09-02) from two pilots:
`src/systems/world/tickets-and-loading.md` (a policy page) and
`src/systems/networking/protocol-phases.md` (a state machine). The old
seven-heading skeleton is gone; a page takes the shape of its story, and the
budgets below are the enforceable part. Ruling R2 in section 9 of `docs/pass3.md` is the
authority; this file is its working form. Pass-5 session A (2026-09-05) added
the two sections below it — "One home per mechanism" and "The landing page" —
which are rules about the book rather than about a page; the rulings behind
them are in `docs/pass5-brief.md` Part 3. Pass-6 session A (2026-09-10) wrote
in what the menu had let become slots: the landing page's seventh section,
the closer's one spelling and its test, the 1.21 blockquote's place, the way
into a scenario, bold on the hook, one subject a section, *Where to look* as
a reading list, and which of two look-alike pages varies. Its rulings are in
`docs/pass6-brief.md` Part 3.*

## One home per mechanism

The corpus is one book, written by thirty sessions that each saw one page.
This is the rule that makes it read as one, and it is the rule pass 5
applies everywhere.

**A mechanism is explained on one page** — the page whose scenario the
mechanism is the answer to — and every other page that needs it spends at
most one sentence and a link. *Explained* is not *named*: a backticked name
in passing is a mention; two paragraphs that would teach a reader the same
thing are the duplicate. When two pages both have a claim, in this order:

1. **The scenario decides.** The owner is the page whose story the mechanism
   answers. The prediction ledger belongs to `client/prediction-and-acks`
   even though Part V meets it first, because the block that appears and
   then disappears is that page's whole scenario.
2. **Within a part, the page whose figure draws it** owns it.
3. **A vocabulary page owns what a thing *is*; a trace owns what
   *happens*.**
4. **Between parts, where none of the above decides, the earlier part owns
   it** — later parts assume earlier ones, so a link back costs the reader
   nothing while a link forward is a promise.

**A Reference page owns an enumeration.** It may carry the one paragraph
that makes its table readable, never an explanation a lecture should give.
The converse binds the lecture: a page names the three or four rows its
scenario touches and links the rest, and never reproduces the catalogue.

**A link points from the page that assumes to the page that explains**, at
first use. A link into a *later* part is allowed in two forms only: a
declared dependency — a landing page's *before you start*, which is a dashed
arrow on the parts figure and a paragraph in `src/lectures.md` — or a
sentence that says the later page pays it off. Anything else is a promise
nobody keeps.

**A summariser never explains.** The thirteen landing pages, the lecture
map, the glossary and the introduction restate pages by design. Three rules
follow: a summariser is never a fact's only home; where a summariser
disagrees with its page the page wins, and the summariser is corrected in
the same session, after the page; and where the same thing is said in both,
the summariser is the copy that gets shorter.

**A pair the book declares stays a pair.** Where a landing page or
`src/lectures.md` calls two pages one lecture in two halves, or one the
sequel of the other, a shared preamble is deliberate: it is checked for
drift between the two copies and never merged away. The list of declared
pairs is in `docs/pass5-brief.md` Part 3.

### The citation form

The book's citation is the parenthetical link at the end of the sentence
that needs it — *…so a click and its correction land in the same tick (the
server tick)* — and it carries **the anchor of the section that is the
answer**, so that the reader lands on the paragraph and not on the top of a
four-hundred-line page. One sentence saying what the mechanism means *here*,
then the link, and nothing else. Where the losing explanation says something
the owner's lacks, that is a move and not a cut: the sentence goes to the
owner first.

Seven ideas cross parts — the tick and its phases, the four threads, the
wire and the hop, authority and prediction, the registry freeze and the
reload, the data-driven type pattern, the ledger. Each has one owner page
and one anchor, and every other page cites it in that form; the table is in
`docs/pass5-brief.md` Part 3.

## The landing page

A landing page is a part's **argument**, not a summary of its pages. It is
what the folding sidebar opens on, so it is the first thing a reader of that
part sees and the thing they come back to. Seven things, in this order:

**The argument** — one paragraph saying what the part claims about its
system and what a reader will be able to explain afterwards. It starts
inside a scenario like any other page and ends on the part's hook. It is not
a list of what is coming.

**The size**, where size is part of the argument (Part XI is the largest
thing on the client by a distance; Part XII is a system with no entity and
no tick in it). The number is never hand-counted: it comes from
`{{#include ../../generated/part-<dir>.md}}`, which `tools/map_source.py`
writes from the same `PARTS` mapping the atlas prints and
`tools/pass5_coverage.py` reads, so a landing page's count and the coverage
population cannot disagree; the prose names the packages the way
`src/generated/parts.md` does. A part whose size is not part of its argument
says nothing and leaves the number to the atlas.

**The shape** — *a hub and six spokes*, *a stack of three floors*, *a
conveyor* — as a sentence and as a figure of the part's own pages.

***Before you start*** — true dependencies only, each with the sentence that
says what the part uses it for. A hand-forward, where this part gives a
later one something, lives outside this section: `tools/check_deps.py` reads
every cross-part link here as a dependency and every dependency as an arrow
on the parts figure.

***Watch in this order*** — the pages, with one line each saying what the
page is. **This is the only place that line is written.** `SUMMARY.md`
copies the order, `src/lectures.md` copies the order and adds only what is
about the order, and neither repeats the line. The order itself is the
part's argument in miniature, and `check_deps.py` fails if the three
disagree.

***Where the part stops*** — what is in the part's packages and not in the
lectures, and why. It sits here, after the watch order and before the shelf:
the reader has just seen what the part teaches, so this is where they can
judge what it leaves out, and the shelf then closes the page. It carries the
families the pages above already draw (a clause each), the deliberate
omissions with the reason (a sentence each, and each of those is an entry in
`docs/pass3.md` §7), and the coverage number from
`{{#include ../../generated/coverage-<dir>.md}}` — never hand-counted, the
same rule the size follows. At most fifteen lines: what is longer is either
the argument made a second time or an explanation that belongs on a page.

**The Reference it uses** — one line per page, what the part reads it for.

Then the rules footer. No trace, no cast, and no figure but the part's own
shape. Everything except the watch order runs to about a hundred lines,
*Where the part stops* inside that; a landing page much longer than that is
arguing twice, and the fix is the argument rather than the trim. **The
argument ends on the claim** — where the paragraph carries the recognition
sentence (*a player recognises this part by …*), that sentence sets the claim
up and does not end the paragraph, or the part's argument reads as a list of
symptoms.

## What every page keeps

1. **The title** — the system, not the scenario.
2. **The verified line** — `> Verified against **Minecraft 26.2** · Part N ·
   <the scenario in one line>`. The scenario is a sentence a player could
   act out, not a topic.
3. **The opening paragraph** — starts *inside* the scenario (a player takes a
   step; a server is clicked in the list) and ends on the **hook**: the one
   observable, surprising, true thing the page explains. No "Responsibility"
   heading; the paragraph is the responsibility. The pass-2 findings are the
   hook bank (the block that comes back and vanishes again; lava
   random-ticking twice; the watchdog kill that saves nothing; the minimized
   window rendering frames nobody sees; the player built after the phase
   named for preparing it). **What varies between pages is the way in** — a
   thing happening, a thing seen, a fact stated flat, a question — not
   whether the reader is addressed: the second person is the plainest way
   into a scenario and belongs to any page that wants it, but *You* as the
   first word is an entry, and a part whose pages nearly all start on it has
   one way in rather than a register. In the body the second person stays
   where the reader does the thing (the click, the swing) and out of the
   explanation. **Bold on the hook is a device, not a slot**: spent where
   that sentence is the page's thesis and the page comes back to it, and
   otherwise not.
4. **The cast** — at most eight classes with role and thread, as a small
   table (`| class | what it decides | thread |`) or woven into the
   narration. It replaces the field inventories: a page names the fields
   its story touches, in the sentences that touch them, and the exhaustive
   lists live in the class index and Reference.
5. **At least one figure**, in the shape the page chose (below), with lanes
   from the key.
6. **Headings that say what the section says** — *The two flushes*, *When
   a ticket dies*, *Status, the phase nobody logs in through* — never which
   template slot it fills, so a trace's heading is its scenario (*Dusk, and
   the mob and the camera ask the same question*) and never `The trace: …`.
   A reader should be able to tell two pages apart from their tables of
   contents. **A section has one subject and its heading names it**: a
   heading that names two of the three things under it is the finding, and
   the fix is usually a third heading rather than a longer one. **A section
   lands on its rule and the exception follows**, unless the exception is the
   page's hook. What the page names and does not explain — the coverage
   passage — sits in one place: last before the closer, or last before
   *Where to look* where there is none.
7. ***Where to look*** — entry-point names, one line, in reading order: a
   reading list for someone opening the decompile, **not an index of the
   page**. A name in it that the page never said is a door the reader can
   still open, so it is allowed — but a dozen of them is the field inventory
   come back under a new heading, and those go to the class index and
   Reference where the inventories live. Then
   the rules footer, verbatim:

   `*Rules: names, never code · how the system works, not how the code reads ·
   newest version only · every backticked name passes \`tools/verify_names.py\`.*`

What every page drops: *Responsibility*, *The data it owns*, *When it runs*,
*Interfaces* and *Invariants and surprises* as headings. Their content goes
where the story needs it — the thread in the cast table, the interfaces as
one sentence or one cast row (what crosses the network, as which packets),
the invariants placed where they happen or gathered as answers in a
*Questions players ask* section.

## The shapes

Choose the one whose figure is the true picture of the system. If the
truth is a graph, do not draw a conversation.

| shape | for | its figure | how the sections go | pilot |
|---|---|---|---|---|
| **the trace** | one scenario through the system | a `sequenceDiagram`, at most seven lanes, a shaded band at every tick boundary | narrated as prose in the order things happen, each surprise placed where it happens | (session C onward) |
| **the pipeline** | stages that hand off | a `flowchart` of the stages at the top | a section per stage: what comes in, what is decided, what goes out | — |
| **the state machine** | phases and transitions | `stateDiagram-v2`, transitions labelled with the packets or events; an orphan state drawn as an orphan | a section per state, each ending in *what disconnects / fails / leaves it* | `protocol-phases` |
| **the policy** | who is told what, and when | a decision table or a `flowchart` per decision; the surprises are its rows | one section per decision on the path the opening figure draws; a short trace kept as the grounding | `tickets-and-loading` |
| **the comparison** | two or three paths that differ | a table with the paths as columns; one diagram per path, or one with `alt` | a section per point of difference, not per path | — |
| **the vocabulary page** | the objects and their relations | a figure of the data (`classDiagram`, a containment `flowchart`), then one small trace | a tour by object, each grounded in the trace | — |
| **the pattern** | one idea, many instances | the instances as a table; one instance traced | the idea, the table, the trace, the exceptions | — |
| **the landing page** | a part | the part's shape as a figure of its pages | the argument · the size · the figure · *before you start* · *watch in this order* · *where the part stops* · the Reference pages it uses — the section [The landing page](#the-landing-page) above has the role in full | `src/systems/commands/README.md` |

A page may borrow one section from another shape (the policy pilot keeps a
six-lane trace; the state-machine pilot keeps a three-lane sequence for the
encryption handshake alone). It may not borrow the whole skeleton. **A page
is not done until it reads differently from its neighbours** — its
neighbours being the pages a reader meets around it, which is the pages of
its own part. Where two of them run the same sections in the same order, the
**later page in the watch order varies**, because the reader met the earlier
one fresh; the variation is structural — a different order of the same
sections, the questions dissolved, the comparison table as the figure, the
trace before the cast — never the same paragraphs under reshuffled headings.
Two pages in different parts may share a spine and usually should not be
touched for it. The exception is a pair the book declares (above): there a
shared skeleton is the point, and what has to read differently is the prose.

## The devices

Any page may use these; none must.

- **The myth table** — `| what the forum says | what the decompile does |`.
- **The number** — a count with its owner, set off on its own line:
  `**Four** — player-view chunks loading at once (\`DistanceManager.ticketDispatcher\`).`
- **For a 1.21-era reader** — a blockquote opening `> **For a 1.21-era
  reader.**`, replacing the names-you-will-hunt-for bullets; one per page at
  most, at most eight lines, and only where a name or a mechanism actually
  moved — a blockquote that only says *this is new* is not one. **Its place
  is the foot of the page**: the last thing before *Where to look*, after the
  closer if there is one. It addresses a reader the page is not otherwise
  written for, who should be able to find it without reading the page, and in
  the body it stops the scenario for the reader the book *is* for.
- **Questions players ask** — a section whose bold lead-ins are questions
  and whose paragraphs are the invariants, restated as answers. That
  spelling and no other: where the questioner is a data-pack author or a
  command author, the question says so and the heading does not. **A closer
  holds consequences, never the page's own mechanism.** An answer another
  page needs is load-bearing by definition — it moves up under a heading
  that says what it says, and the link that cited it is repointed in the
  same commit. A closer that stays is the last content section, holds at
  most six questions, and answers each in at most a paragraph. Where it
  goes, its material dissolves into the section where the answer happens or
  takes a heading of its own; nothing is dropped except by the budget rule.
  A part whose every page ends on one has stopped choosing.
- **The same trace from the other side** — a mirrored client/server pair,
  as `environment-attributes-and-timelines` already does.
- **The tick-boundary band** — a shaded `rect` with a `Note over` naming the
  tick or the phase, wherever a sequence crosses a tick; and the explicit *no
  reply* annotation (`-->>` with the word *nothing*) where a packet is
  answered by silence. [Figures](#figures) has the form.

## The budgets

The enforceable part.

- A bulleted or numbered list holds **parallel items of at most two
  sentences, at most seven of them**, and a page has **at most three
  lists**. *Where to look* is not a list; the cast is a table.
- Anything explanatory is prose. Anything enumerative **beyond seven is a
  table**, or a Reference page the text links to.
- A section **passes forty lines only with a figure or a subsection in it**.
- *Interfaces* survives as one sentence or one cast row.
- Nothing is dropped from a page except by moving it (Reference, another
  page) or by logging the cut in `docs/pass5.md` with the reason.
- Every claim a rewrite introduces — a hook, a redrawn ordering, a new
  section — is listed in `docs/pass9.md` by the session that wrote it.

## Figures

A figure is the lecture's artefact: the thing a viewer screenshots, and the
thing a reader who skims uses as the check on the section — *if I understand
the picture, I understand the section*. So a figure answers **one question**,
shows **the thing the words carry badly** (an order, a branch, a boundary, a
containment, a quantity), and is **legible at the column width without the
zoom**. The rules below were settled by pass 7's session A, each against the
whole corpus rendered in a browser at the reading column; `node
tools/render_figures.js` is how any change to one is argued.

### Where a figure sits, and the three sentences around it

- **The lead-in.** The sentence before a figure ends by saying what the figure
  will show. A **lead figure** — the page's own artefact, under the cast — may
  open its section with nothing above it; nothing else may.
- **The caption** is the **italic paragraph directly after the figure**: one
  sentence, in the book's voice, saying what the picture shows and what to look
  for in it. It is markdown, so `verify_names.py` reads its names and
  `llms-full.txt` carries it; `custom.css` styles exactly that paragraph and
  numbers it (*Figure 3.*). A caption is a **claim about what the figure
  shows** and goes to `docs/pass9.md` like any other.
  **It is one italic run from end to end.** The stylesheet matches
  `p:has(> em:only-child)`, so a caption that closes its italics to set a name
  and reopens them has two `<em>`s, stops matching, and silently loses its
  styling and its number in the built page — the markdown looks right and
  mermaid parses. A name inside a caption goes in backticks *within* the
  italics, never outside them; `node tools/check_mermaid.js` fails a caption
  that breaks this.

      *The four gates a spawn attempt passes before a mob object exists; the
      boundary marked* only now *is the one that matters.*

- **The reading sentence.** The paragraph after the caption reads the picture:
  it names the thing the reader should see in it. A figure with no lead-in, no
  caption and no sentence pointing at it is a picture the page never mentions.

### The kind follows the mechanism

If the truth is a graph, do not draw a conversation. The site's mermaid draws
twenty-one kinds; use the one that shows the thing in the fewest marks, never
one for variety.

| the mechanism | the kind |
|---|---|
| a scenario in time, across objects or machines | `sequenceDiagram` |
| a branch, a pipeline of stages, a containment | `flowchart` |
| phases and what moves between them | `stateDiagram-v2` |
| what an object **holds** (the vocabulary page's figure) | `classDiagram` |
| a layout in memory or on the wire | `block-beta`, `packet-beta` |
| a quantity that is a curve | `xychart-beta`, its caption saying whether the numbers are real or illustrative |
| a taxonomy with no order in it | `mindmap` — or, faster, the table |
| two or three paths that differ | **a table.** Not a figure |

`node tools/check_mermaid.js` is the arbiter of what the site's mermaid
accepts, and a diagram that fails it does not publish; a shape the checker
rejects is not available whatever these notes say. Two kinds have traps the
renderer flags: `packet-beta` cuts a long field label, and `quadrantChart` lets
a point label collide with a quadrant label.

### One visual grammar, the same on every page

| the mark | what it means |
|---|---|
| a **rectangle** | a step, or a call |
| a **diamond** | a decision — and its outgoing edge labels are its answers |
| a **cylinder** | storage |
| a **subgraph** | a thread, a machine or a tick, named for it — never a grouping of convenience |
| a **solid arrow** | a call, or a hand-off in time |
| a **dotted arrow** | a return, or a reply |
| **`-x`** | a message dropped |
| **`-)`** | a message nobody waits for |
| a **`Note over`** | a tick boundary or a thread hop, and nothing else |
| a **`box`** | lanes grouped by thread or machine |
| a **`rect` band** | the extent of a tick, a frame or a phase (see below) |

Direction is **`TD`** for anything ordered in time or by decision and **`LR`**
for a pipeline of stages; `TB`, `BT` and `RL` are not written. A figure that
needs a mark outside this table says so in its caption.

**The tick boundary is a band.** A trace that crosses a tick, a frame or a
thread draws the crossing as a shaded band — `rect rgba(0, 0, 0, 0.04)` with a
`Note over` all lanes naming the tick or the phase — so the picture shows the
tick's *extent* and not only its edge; a flowchart that spans ticks puts each
tick in a subgraph named for it. The explicit *no reply* annotation (`-->>`
with the word *nothing*) stays as it is. A trace with no crossing has no band:
the device is spent, not defaulted.

### Labels are not sentences

A label that needs a sentence is a sentence the section owns — the label keeps
the name, the prose keeps the explanation.

- A **node label**: a subject and a verb, at most eight words and two lines
  (`<br/>` where the break matters).
- An **edge label**: the condition, at most four words.
- A **message**: at most twelve words. A **note**: at most sixteen.
- A **gate** carries the constant's name, never a bare number
  (`UPDATE_CLIENTS`, not `2`; `flag 2` only where the page has paired the name
  and the number above the figure).

`python tools/pass7_figures.py --part <part>` counts the sentence labels and
the bare number gates per figure; a session reads its own labels aloud.

### As complex as it needs to be, and as simple as it can be

The test is the viewer's first question — *what does it show?* — answered in
one sentence. Past about **fifteen nodes**, **twenty messages**, or a figure
taller than a screen, split at **the mechanism's own joint, the one the prose
already names** (the spawn cascade at *only now does a `Mob` object exist*),
and give each half its own caption and its own paragraph. Every node is a step
or a decision the prose names; a node that restates the paragraph is cut; a
chain of rejections is one node with a list of conditions only where the
conditions have no order, and an ordered chain is drawn in its order.

**Two figures for one mechanism are one figure.** Within a part, the page whose
figure draws a mechanism owns it. Where two figures show one thing, the one
that shows *its section's* thing stays and the other is redrawn to show a
different thing — the states rather than the order, the objects rather than the
calls — or is a logged cut. A second figure on a page earns its place by
showing what the first cannot.

### A figure names what its section explains

A lead figure is drawn **in the words of the cast**: the class names the cast
table has just given, and verbs for what happens (*asks*, *writes*, *sends the
packet*) — not method names the reader meets 150 lines later. Method names
belong in the section figures that follow their prose. **A name the figure says
and the prose never does** is either given the one sentence the figure was
standing in for, or taken out of the figure. `python
tools/check_figure_names.py` checks every identifier inside a mermaid block
against the decompile the way `verify_names.py` checks the prose — a class, a
dotted `Class.member`, and a sequence message's head against the lane it is
sent to — and a page that fails it does not publish. In a figure as in the
prose: **a member is written `Class.member`**, and a nested class `Outer.Inner`.
The one exception is a **`classDiagram` member line**, which its own class box
qualifies the way a lane qualifies a message: `int popTime` inside
`class ItemStack` is checked as `ItemStack.popTime` and takes no prefix.

### The theme, and no colour in a page

The whole visual grammar lives in `mermaid-init.js` (the wrap, the fonts, the
palettes for the light and dark themes) and in `custom.css` (the semantic
classes, the caption). **`%%{init}%%`, `classDef`, `style` and `linkStyle` do
not go in a page.** A node says which side of the wire it lives on with one of
**five class words** and no `classDef` — mermaid puts the class on the node's
`<g>`, so the colour is a stylesheet rule that follows the reader's theme:

    A["ServerLevel.tick"]:::server      B["ClientLevel.tick"]:::client
    N["Netty event loop"]:::netty       W["Worker-Main-n"]:::worker
    D[("region file")]:::disk           (a state diagram: `class Idle server`)

`server` · `client` · `netty` · `worker` · `disk` are the whole colour
vocabulary, and the same five words are a sequence diagram's `box` labels and
the lane key's word lanes, so a thread is called the same thing in every kind
of figure. A figure that needs a sixth argues for it in the session log.
Everything else is the theme's default. Do not re-run `mdbook-mermaid install`:
it overwrites `mermaid-init.js` with the default, which wraps nothing.

### What mermaid 11.6.0 rejects

- **No `;` in any label** — mermaid ends the statement there. Write `#59;`
  if the character is unavoidable; usually a comma or *then* is better.
- **No `#` in any label** — mermaid reads an entity code and drops the rest
  of the line silently. Write `#35;`.
- **Quote flowchart labels** (`A["…"]`) so parentheses, colons and slashes
  survive; keep `stateDiagram-v2` transition text on one line after the
  colon; a note is `note right of STATE : text`.
- **No second colon in a `stateDiagram-v2` transition.** The text after the
  transition's own colon may not contain another one — the parser stops there
  and the diagram fails. A comma or a dash instead.
- **A subgraph title is clipped to one wrapped line.** Mermaid wraps the title
  at the theme's width and then draws only the first line, silently, so
  anything past about twenty-five characters is lost on screen. Keep a subgraph
  title short and put the rest in the caption; the render is the only check
  that sees this.
- **No flowchart or state-diagram label may begin a markdown block.** Mermaid
  runs a markdown tokenizer over those labels and draws only plain text, bold,
  italic and a few others; anything else is replaced, *in the node*, by the
  literal string `Unsupported markdown: <type>` — so a label starting `1. `,
  `- `, `* `, `> ` or a horizontal rule is **gone from the picture**. The
  diagram parses and the markdown looks right, which is how nine of these
  shipped. Number a step `1 · …` or `Stage 1, …` instead. A sequence-diagram
  message does not go through this path and may start how it likes;
  `node tools/check_mermaid.js` fails the rest, and its probe has the nine
  cases it was measured on.

**A figure two pages share** is written once, as a mermaid block in a file
under `src/figures/`, and each page includes it with `{{#include}}` — the
parts-dependency graph is on the introduction and on `lectures.md` this
way. One source, so the two copies cannot drift; the file is hand-kept and
`verify_names.py` reads it like any page.

**A generated figure** (session B's pipeline, used by the atlas) is an SVG a
tool under `tools/` writes into `src/generated/` — never hand-edited, always
regenerable on the next version — and a page includes it inside an HTML
block so that it inherits the theme:

    <figure class="map">
    {{#include ../generated/<name>.svg}}
    <figcaption>What the figure shows. Click to enlarge.</figcaption>
    </figure>

The SVG carries **classes only** — `class="mapfig"` on the root, and
`shared`, `client`, `lib`, `skip`, `muted`, `fold`, `edge`, `group` on its
parts — and every colour, font and theme rule lives in `custom.css`, with
text as `currentColor`, so the five mdBook themes and the zoom overlay all
read it. It emits no blank line (an HTML block ends at one), sets a
`viewBox` so it scales to the column, and puts a `<title>` on each element
that has a number, so hovering answers what a label could not fit.
`tools/map_source.py` is the worked example: a squarified treemap, bar
charts and a left-to-right tree with counts, each a forty-line function.
`llms_full.py` replaces an SVG include with a one-line note and pastes a
markdown include in, so a generated table beside the figure is what
agents read.

## Lanes

A lane in a sequence diagram is a class name, abbreviated once for the whole
corpus. `python tools/check_lanes.py` reads the key below and every
`participant X as Y` in `src/`, fails if a key entry is not a class in the
decompile or if two key rows share a lane, and reports every page whose
lane means something other than the key says; `--strict` turns the report
into a failure, and `tools/deploy.sh` runs it that way over the whole corpus,
so a page whose lane disagrees with the key does not publish. `--index`
writes the key to `src/reference/lanes.md` for readers.

**How many, and which.** **At most seven lanes**, and the column is the reason:
a lane is about 230px wide, so an eighth puts the type under eleven pixels on
screen for every label in the figure. A lane earns its place by *deciding*
something — a lane that carries one message and decides nothing is folded into
a note or into the label on the arrow. **One object is one lane**: a subclass
and its base share a lane, named for the object. **Two machines are two
lanes** — or a `box` per machine — never a `Note over` saying *now the client*.
**Two objects are never one lane**: a block and its block entity, a container
and the container it mirrors, are two, or the figure is about one of them.
Lane *order* is the order of first use, left to right, so the first message
reads left to right.

**How a lane is derived** when it is not yet in the key: the initials of
the class's CamelCase words (`ServerGamePacketListenerImpl` → `SGPL`),
never fewer than two letters; a one-word class of up to eight letters is
its own lane (`Player`, `Entity`, `Window`), a longer one takes a fixed
prefix recorded here (`Connection` → `Conn`); a nested class takes the
outer initials plus its own (`DistanceManager.PlayerTicketTracker` →
`PTT` is the exception, claimed by the pilot); a collision is resolved by
lengthening the **later** claimant, never by reassigning an existing row.
A short whole word is allowed for a lane that is not a class (`Netty`,
`Main`, `Worker`, `Auth`, `Wire`, `Disk`) and is marked as such below.
**The key is the authority**: add a row when a page introduces a lane, and
never change an existing row's meaning.

**A long lane name carries its own break.** The theme wraps a message at 180px
so the lanes stay close and the type stays readable, and mermaid hyphenates any
word wider than that — `PersistentEntitySectio-nManager`, a Mojang name the
book would be getting wrong on screen. So a class name too wide for the box is
written with `<br/>` at a CamelCase boundary, a nested class at its dot:

    participant PESM as PersistentEntity<br/>SectionManager
    participant TE as ChunkMap.<br/>TrackedEntity

The break is display only: both gates read a lane expansion with it closed up,
so the key still holds the name. **In a message, a break is the last resort and
not the first**: an explicit `<br/>` turns the 180px wrap off for that whole
label, so a message that carries a sentence *and* a break renders the sentence
on one long line and widens the figure. Shorten the message until the name is
the whole of it, then break the name. `python tools/pass7/break_lane_names.py` puts
the break in from a render, and is the check after adding a lane.

### The lane key

| lane | class |
|---|---|
| `MC` | `Minecraft` |
| `MS` | `MinecraftServer` |
| `IS` | `IntegratedServer` |
| `DS` | `DedicatedServer` |
| `SL` | `ServerLevel` |
| `CL` | `ClientLevel` |
| `Level` | `Level` |
| `SP` | `ServerPlayer` |
| `LP` | `LocalPlayer` |
| `Player` | `Player` |
| `Entity` | `Entity` |
| `PL` | `PlayerList` |
| `SGPL` | `ServerGamePacketListenerImpl` |
| `CPL` | `ClientPacketListener` |
| `SHPL` | `ServerHandshakePacketListenerImpl` |
| `SSPL` | `ServerStatusPacketListenerImpl` |
| `SLPL` | `ServerLoginPacketListenerImpl` |
| `SCPL` | `ServerConfigurationPacketListenerImpl` |
| `CHPL` | `ClientHandshakePacketListenerImpl` |
| `CCPL` | `ClientConfigurationPacketListenerImpl` |
| `Conn` | `Connection` |
| `SConn` | `Connection` |
| `SCL` | `ServerConnectionListener` |
| `BEL` | `BlockableEventLoop` |
| `SCC` | `ServerChunkCache` |
| `CM` | `ChunkMap` |
| `CMTE` | `ChunkMap.TrackedEntity` |
| `CH` | `ChunkHolder` |
| `DM` | `DistanceManager` |
| `TS` | `TicketStorage` |
| `LCT` | `LoadingChunkTracker` |
| `SCT` | `SimulationChunkTracker` |
| `PTT` | `DistanceManager.PlayerTicketTracker` |
| `CTD` | `ChunkTaskDispatcher` |
| `TCTD` | `ThrottlingChunkTaskDispatcher` |
| `PCS` | `PlayerChunkSender` |
| `PESM` | `PersistentEntitySectionManager` |
| `PST` | `PrepareSpawnTask` |
| `SRT` | `SynchronizeRegistriesTask` |
| `JWT` | `JoinWorldTask` |
| `RS` | `RenderSystem` |
| `GR` | `GameRenderer` |
| `LR` | `LevelRenderer` |
| `Gui` | `Gui` |
| `Hud` | `Hud` |
| `Screen` | `Screen` |
| `Window` | `Window` |
| `Boot` | `Bootstrap` |
| `BIR` | `BuiltInRegistries` |
| `Items` | `Items` |
| `Item` | `Item` |
| `MR` | `MappedRegistry` |
| `DMR` | `DefaultedMappedRegistry` |
| `WL` | `WorldLoader` |
| `RDL` | `RegistryDataLoader` |
| `RLT` | `RegistryLoadTask` |
| `RMRLT` | `ResourceManagerRegistryLoadTask` |
| `LRA` | `LayeredRegistryAccess` |
| `RDC` | `RegistryDataCollector` |
| `RSyn` | `RegistrySynchronization` |
| `CBE` | `ChestBlockEntity` |
| `TVO` | `TagValueOutput` |
| `CHelp` | `ContainerHelper` |
| `IStack` | `ItemStack` |
| `NbtIo` | `NbtIo` |
| `PEnc` | `PacketEncoder` |
| `PDec` | `PacketDecoder` |
| `DCP` | `DataComponentPatch` |
| `HS` | `HashedStack` |
| `IP` | `ItemParser` |
| `TagP` | `TagParser` |
| `KH` | `KeyboardHandler` |
| `PR` | `PackRepository` |
| `RRM` | `ReloadableResourceManager` |
| `MPRM` | `MultiPackResourceManager` |
| `SRI` | `SimpleReloadInstance` |
| `PRL` | `PreparableReloadListener` |
| `LO` | `LoadingOverlay` |
| `RC` | `ReloadCommand` |
| `TL` | `TagLoader` |
| `RSR` | `ReloadableServerResources` |
| `Parrot` | `Parrot` |
| `EM` | `EnchantmentMenu` |
| `EH` | `EnchantmentHelper` |
| `PDM` | `PatchedDataComponentMap` |
| `ACM` | `AbstractContainerMenu` |
| `Comp` | `Component` |
| `MComp` | `MutableComponent` |
| `CS` | `ComponentSerialization` |
| `CU` | `ComponentUtils` |
| `Language` | `Language` |
| `Font` | `Font` |
| `CT` | `CombatTracker` |
| `DScr` | `DeathScreen` |
| `TrC` | `TranslatableContents` |
| `RSReg` | `ReloadableServerRegistries` |
| `LT` | `LootTable` |
| `LIF` | `LootItemFunctions` |
| `SICF` | `SetItemCountFunction` |
| `PP` | `PacketProcessor` |
| `TRM` | `ServerTickRateManager` |
| `LTs` | `LevelTicks` |
| `EAS` | `EnvironmentAttributeSystem` |
| `NS` | `NaturalSpawner` |
| `ETL` | `EntityTickList` |
| `WB` | `WorldBorder` |
| `PDS` | `PlayerDataStorage` |
| `SW` | `ServerWatchdog` |
| `LSA` | `LevelStorageSource.LevelStorageAccess` |
| `SC` | `StopCommand` |
| `DL` | `DirectoryLock` |
| `WS` | `WorldStem` |
| `LC` | `LevelChunk` |
| `CGT` | `ChunkGenerationTask` |
| `TLE` | `ThreadedLevelLightEngine` |
| `BLE` | `BlockLightEngine` |
| `LLSS` | `LayerLightSectionStorage` |
| `SCD` | `SerializableChunkData` |
| `IOW` | `IOWorker` |
| `LCTs` | `LevelChunkTicks` |
| `FF` | `FlowingFluid` |
| `LB` | `LiquidBlock` |
| `BI` | `BucketItem` |
| `RB` | `RepeaterBlock` |
| `GED` | `GameEventDispatcher` |
| `VSL` | `VibrationSystem.Listener` |
| `VST` | `VibrationSystem.Ticker` |
| `VSel` | `VibrationSelector` |
| `SSB` | `SculkSensorBlock` |
| `SSVU` | `SculkSensorBlockEntity.VibrationUser` |
| `PM` | `PoiManager` |
| `Brain` | `Brain` |
| `AP` | `AcquirePoi` |
| `VNP` | `ValidateNearbyPoi` |
| `SIB` | `SleepInBed` |
| `PN` | `PathNavigation` |
| `EVS` | `EnvironmentAttributeSystem.ValueSampler` |
| `ATS` | `AttributeTrackSampler` |
| `KTS` | `KeyframeTrackSampler` |
| `SCM` | `ServerClockManager` |
| `EAP` | `EnvironmentAttributeProbe` |
| `Camera` | `Camera` |
| `GS` | `GaussianSampler` |
| `SAI` | `SpatialAttributeInterpolator` |
| `SR` | `SkyRenderer` |
| `Mob` | `Mob` |
| `Block` | `Block` |
| `MPGM` | `MultiPlayerGameMode` |
| `SPGM` | `ServerPlayerGameMode` |
| `CNU` | `CollectingNeighborUpdater` |
| `DB` | `DoorBlock` |
| `AFBE` | `AbstractFurnaceBlockEntity` |
| `FM` | `FurnaceMenu` |
| `LevB` | `LeverBlock` |
| `RSWB` | `RedStoneWireBlock` |
| `DRWE` | `DefaultRedstoneWireEvaluator` |
| `PBB` | `PistonBaseBlock` |
| `PSR` | `PistonStructureResolver` |
| `PMBE` | `PistonMovingBlockEntity` |
| `ET` | `EntityType` |
| `SumC` | `SummonCommand` |
| `SE` | `ServerEntity` |
| `ES` | `EntityStorage` |
| `SED` | `SynchedEntityData` |
| `Sheep` | `Sheep` |
| `LE` | `LivingEntity` |
| `CG` | `CollisionGetter` |
| `Shapes` | `Shapes` |
| `AttrI` | `AttributeInstance` |
| `AttrM` | `AttributeMap` |
| `EffC` | `EffectCommands` |
| `ME` | `MobEffect` |
| `AB` | `AbstractBoat` |
| `SAB` | `AbstractBoat` |
| `CSED` | `SynchedEntityData` |
| `AA` | `AbstractArrow` |
| `CR` | `CombatRules` |
| `MTS` | `MoveToTargetSink` |
| `MoveC` | `MoveControl` |
| `NE` | `NodeEvaluator` |
| `PF` | `PathFinder` |
| `PNR` | `PathNavigationRegion` |
| `UAFS` | `UpdateActivityFromSchedule` |
| `Cons` | `Consumable` |
| `BowI` | `BowItem` |
| `ChestM` | `ChestMenu` |
| `CraftM` | `CraftingMenu` |
| `RemS` | `RemoteSlot` |
| `CSync` | `ContainerSynchronizer` |
| `ResultS` | `ResultSlot` |
| `ResultC` | `ResultContainer` |
| `RM` | `RecipeManager` |
| `CI` | `CraftingInput` |
| `TCC` | `TransientCraftingContainer` |
| `SRB` | `ServerRecipeBook` |
| `Ench` | `Enchantment` |
| `Ignite` | `Ignite` |
| `EScr` | `EnchantmentScreen` |
| `CEM` | `EnchantmentMenu` |
| `CMap` | `ContextMap` |
| `LootP` | `LootParams` |
| `LootC` | `LootContext` |
| `LIC` | `LootItemCondition` |
| `LPool` | `LootPool` |
| `RCont` | `RandomizableContainer` |
| `ExecC` | `ExecuteCommand` |
| `Inv` | `Inventory` |
| `FD` | `FoodData` |
| `FP` | `FoodProperties` |
| `KM` | `KeyMapping` |
| `KI` | `KeyboardInput` |
| `MEI` | `MobEffectInstance` |
| `CScr` | `ChatScreen` |
| `CLis` | `ChatListener` |
| `RCPL` | `ClientPacketListener` |
| `CCC` | `ClientChunkCache` |
| `LLE` | `LevelLightEngine` |
| `LX` | `LevelExtractor` |
| `BSPH` | `BlockStatePredictionHandler` |
| `MH` | `MouseHandler` |
| `InvS` | `InventoryScreen` |
| `GGE` | `GuiGraphicsExtractor` |
| `GuiR` | `GuiRenderer` |
| `ChatC` | `ChatComponent` |
| `CRU` | `ComponentRenderUtils` |
| `SSpl` | `StringSplitter` |
| `FBR` | `FormattedBidiReorder` |
| `FSet` | `FontSet` |
| `GStit` | `GlyphStitcher` |
| `SndM` | `SoundManager` |
| `SndE` | `SoundEngine` |
| `SBL` | `SoundBufferLibrary` |
| `ChanA` | `ChannelAccess` |
| `SEE` | `SoundEngineExecutor` |
| `Library` | `Library` |
| `Channel` | `Channel` |
| `LEH` | `LevelEventHandler` |
| `CDS` | `ClientDebugSubscriber` |
| `SDS` | `ServerDebugSubscribers` |
| `LDS` | `LevelDebugSynchronizers` |
| `TDSS` | `TrackingDebugSynchronizer.SourceSynchronizer` |
| `BDR` | `BrainDebugRenderer` |
| `GpuS` | `GpuSurface` |
| `GD` | `GpuDevice` |
| `CE` | `CommandEncoder` |
| `RP` | `RenderPass` |
| `GlCE` | `GlCommandEncoder` |
| `GB` | `GpuBackend` |
| `GLX` | `GLX` |
| `MonM` | `MonitorManager` |
| `SUT` | `SectionUpdateTracker` |
| `SRD` | `SectionRenderDispatcher` |
| `SectC` | `SectionCompiler` |
| `SOG` | `SectionOcclusionGraph` |
| `FGB` | `FrameGraphBuilder` |
| `MM` | `ModelManager` |
| `MB` | `ModelBakery` |
| `AM` | `AtlasManager` |
| `SprL` | `SpriteLoader` |
| `TA` | `TextureAtlas` |
| `ERD` | `EntityRenderDispatcher` |
| `ZR` | `ZombieRenderer` |
| `ZS` | `ZombieRenderState` |
| `ZM` | `ZombieModel` |
| `SNS` | `SubmitNodeStorage` |
| `FRD` | `FeatureRenderDispatcher` |
| `LM` | `Lightmap` |
| `FR` | `FogRenderer` |
| `LRSE` | `LightmapRenderStateExtractor` |
| `Time` | `Timelines` |
| `PE` | `ParticleEngine` |
| `PChain` | `PostChain` |
| `PPass` | `PostPass` |
| `ShadM` | `ShaderManager` |
| `CST` | `ChunkStatusTasks` |
| `ChunkG` | `ChunkGenerator` |
| `NBC` | `NoiseBasedChunkGenerator` |
| `CA` | `ChunkAccess` |
| `LCS` | `LevelChunkSection` |
| `MNBS` | `MultiNoiseBiomeSource` |
| `ClimS` | `Climate.Sampler` |
| `CPList` | `Climate.ParameterList` |
| `CRT` | `Climate.RTree` |
| `FS` | `FeatureSorter` |
| `WR` | `WorldgenRandom` |
| `PlacedF` | `PlacedFeature` |
| `PMod` | `PlacementModifier` |
| `CF` | `ConfiguredFeature` |
| `TF` | `TreeFeature` |
| `TP` | `TrunkPlacer` |
| `FolP` | `FoliagePlacer` |
| `RootP` | `RootPlacer` |
| `TDec` | `TreeDecorator` |
| `WGL` | `WorldGenLevel` |
| `JS` | `JigsawStructure` |
| `JPP` | `JigsawPlacement.Placer` |
| `STP` | `StructureTemplatePool` |
| `PESP` | `PoolElementStructurePiece` |
| `STemp` | `StructureTemplate` |
| `SStart` | `StructureStart` |
| `SStr` | `StrongholdStructure` |
| `SPie` | `StrongholdPieces` |
| `SPB` | `StructurePiecesBuilder` |
| `Cmds` | `Commands` |
| `CSug` | `CommandSuggestions` |
| `CSP` | `ClientSuggestionProvider` |
| `GC` | `GiveCommand` |
| `EC` | `ExecutionContext` |
| `BC` | `BuildContexts` |
| `CallF` | `CallFunction` |
| `ContT` | `ContinuationTask` |
| `SFM` | `ServerFunctionManager` |
| `SFL` | `ServerFunctionLibrary` |
| `PA` | `PlayerAdvancements` |
| `CAdv` | `ClientAdvancements` |
| `ICT` | `InventoryChangeTrigger` |
| `AR` | `AdvancementRewards` |
| `DlgC` | `DialogCommand` |
| `DlgS` | `DialogScreen` |
| `CComPL` | `ClientCommonPacketListenerImpl` |
| `TC` | `TestCommand` |
| `GTR` | `GameTestRunner` |
| `GTT` | `GameTestTicker` |
| `GI` | `GameTestInfo` |
| `RGL` | `ReportGameListener` |
| `TIB` | `TestInstanceBlockEntity` |
| `SS` | `ServerScoreboard` |
| `SA` | `ScoreAccess` |
| `DataC` | `DataCommands` |
| `BERD` | `BlockEntityRenderDispatcher` |
| `ChestR` | `ChestRenderer` |
| `CSR` | `ChestSpecialRenderer` |
| `IIHR` | `ItemInHandRenderer` |
| `IMR` | `ItemModelResolver` |
| `Blender` | `Blender` |
| `BD` | `BlendingData` |
| `NC` | `NoiseChunk` |
| `CWS` | `CreateWorldScreen` |
| `WCUS` | `WorldCreationUiState` |
| `WOF` | `WorldOpenFlows` |
| `Game` | *the game's own code above Blaze3D, not a class* |
| `Main` | *the JVM main thread, running whichever program's Main the diagram is about — the server's or the client's, so not one class* |
| `Netty` | *the Netty event loop, not a class* |
| `Worker` | *the `Util.backgroundExecutor` pool, not a class* |
| `Auth` | *the User Authenticator thread, not a class* |
| `Sess` | *the Mojang session service both machines call over HTTPS, not a class* |
| `Wire` | *the network between the two programs, not a class* |
| `Disk` | *the save on disk, not a class* |
| `JVM` | *the process itself, not a class* |
| `Hook` | *the Server Shutdown Thread JVM hook, not a class* |

Collisions the pass-2 notebook recorded and the rows above settle: `SL` is
`ServerLevel` (not `ServerLoginPacketListenerImpl`, now `SLPL`, nor
`SpriteLoader`); `CL` is `ClientLevel` (not `ClientPacketListener`, `CPL`);
`CM` is `ChunkMap` (the menus take their own initials); `CH` is `ChunkHolder`
(the client handshake listener is `CHPL`); `GR` is `GameRenderer`
(`GuiRenderer` lengthens to `GuiR`); `TD` is retired in favour of `CTD` /
`TCTD` — and `TreeDecorator` itself is `TDec`. Four classes have two lanes on
purpose: `RCPL` is also `ClientPacketListener`, because the chat diagram shows
the sender's client and the recipient's at once and a note in the figure says
which is which, and `SAB` is also `AbstractBoat` and `CSED` also
`SynchedEntityData`, because [authority](systems/entities/authority.md)'s boat
and [synched entity data](systems/entities/synched-entity-data.md)'s container
are each a page's one picture of two copies of one object, and a `box` per
machine says which is which; `SConn` is also `Connection`, because [the
connection](systems/networking/the-connection.md#one-packet-there-and-one-back)'s
round trip has one object at each end and the picture, not a note, has to say
so. Part V (session F) lengthened four later claimants rather than
reassigning a row: `LeverBlock` is `LevB` because `LB` is `LiquidBlock`,
`BlockItem` would be `BItem` because `BI` is `BucketItem`,
`BlockPlaceContext` would be `BPC` because `PC` is `ProtoChunk`, and
`PistonStructureResolver` is `PSR` because `PR` is `PackRepository`. Rows for
`SS`, `ST`, `SP`-as-structure, `TP`, `LX`, `PE` and `C` are left for the part
sessions that own the pages, under the rule above.

Part VI (session G) lengthened five later claimants: `MoveControl` is
`MoveC` because `MC` is `Minecraft`, `SummonCommand` is `SumC` because `SC`
is `StopCommand`, `AttributeMap` is `AttrM` because `AM` is `AtlasManager`
(Part XI), `EffectCommands` is `EffC` because `EC` is `ExecutionContext`
(Part XIII), and `AttributeInstance` follows its map to `AttrI` even though
`AI` is free, because `AI` reads as the AI system on an entities page. Two one-word classes take their own name as a lane under the
short-word rule, `Sheep` and `Shapes`.

Part VII (session H) is the later claimant almost everywhere and lengthened
eleven rows rather than reassigning one: `ChestMenu` is `ChestM`,
`CraftingMenu` `CraftM` and `EnchantmentScreen` `EScr` because `CM` is
`ChunkMap`, `CS` is `ComponentSerialization` and `ES` is `EntityStorage`;
`RemoteSlot` is `RemS` and `ResultSlot` `ResultS` because `RS` is
`RenderSystem`; `ResultContainer` is `ResultC`, `ContainerSynchronizer`
`CSync`, `ContextMap` `CMap`, `LootParams` `LootP`, `LootContext` `LootC`,
`LootPool` `LPool` (`LP` is `LocalPlayer`), `RandomizableContainer` `RCont`
(`RC` is `ReloadCommand`), `ExecuteCommand` `ExecC` (`EC` is
`ExecutionContext`) and `Enchantment` `Ench` (`EH` is `EnchantmentHelper`).
`Consumable` and `BowItem` take `Cons` and `BowI` under the one-word and
collision rules, and `Ignite` takes its own name. `CI`, `RM`, `SRB` and
`LIC` were free. One collision is recorded and **not
yet claimed**: `ES` is `EntityStorage`, so `EntitySection` would have to
lengthen to `ESec` if a later page wants it.

Part X (session K) added twenty-six rows and lengthened seven later
claimants rather than reassigning a row: `SoundEngine` is `SndE` and
`SoundManager` `SndM` because `SE` is `ServerEntity` and `SM` is claimed in
Part XII's prose, `ChannelAccess` is `ChanA` because `CA` means three things
in three unconverted parts, `GuiRenderer` is `GuiR` because `GR` is
`GameRenderer` (the collision the key already recorded), `InventoryScreen`
is `InvS` because `IS` is `IntegratedServer`, `GlyphStitcher` is `GStit`
because `GS` is `GaussianSampler`, and `StringSplitter` is `SSpl` and
`FontSet` `FSet` deliberately — `SS` and `FS` are unkeyed collisions in Part
XII, and leaving them free costs Part X two letters and saves session M a
renaming. `LX` is claimed here for `LevelExtractor`, which five pages in two
parts already use it for, so Part XI's `LightmapRenderStateExtractor` is the
later claimant and lengthens. `Library` and `Channel` take their own names
under the short-word rule.

Part XII (session M) added twenty-eight rows and lengthened seven later
claimants, and deliberately left three contested short forms free. The
lengthenings: `ChunkGenerator` is `ChunkG` because `CG` is `CollisionGetter`,
`RootPlacer` is `RootP` because `RP` is `RenderPass`, `TreeDecorator` is
`TDec` because the key records `TD` as retired, `Climate.Sampler` is `ClimS`
because `CS` is `ComponentSerialization`, `Climate.RTree` is `CRT` because
`RT` is free but reads as nothing, `PlacedFeature` is `PlacedF` because `PF`
is `PathFinder`, and `PlacementModifier` is `PMod` because `PM` is
`PoiManager`. `MultiNoiseBiomeSource` takes its full initials, `MNBS`, rather
than the `MN` its page used. Two rows were claimed against Part XIII, which
is not yet converted, so session N is the later claimant and lengthens:
`CA` is `ChunkAccess` (so `ClientAdvancements` must lengthen) and `CF` is
`ConfiguredFeature` (so `CallFunction` must). And three short forms this part
used to mean several things are now used for none of them: **`SS`** (it meant
`SurfaceSystem`, `StructureStart` and `StrongholdStructure` on three
adjacent pages, and Part XIII wants it for `ServerScoreboard`), **`ST`** and
**`SP`**-as-a-structure. `StructureStart` is `SStart`,
`StrongholdStructure` `SStr`, `StrongholdPieces` `SPie`, and the terrain and
structure-placement pages now use flowcharts with no lanes at all.

Part XIII (session N) added twenty-six rows and took the three short forms
Part XII left free: `SS` is `ServerScoreboard`, and `SP` stays `ServerPlayer`
throughout. Where this part is the later claimant it lengthened rather than
reassigning: `CommandSuggestions` is `CSug` because `CS` is
`ComponentSerialization`, `ClientAdvancements` is `CAdv` because `CA` is
`ChunkAccess`, `CallFunction` is `CallF` because `CF` is `ConfiguredFeature`,
`ContinuationTask` is `ContT` because `CT` is `CombatTracker`,
`GameTestRunner` is `GTR` because `GR` is `GameRenderer`, `DialogScreen` is
`DlgS` because `DScr` is `DeathScreen`, and
`ClientCommonPacketListenerImpl` is `CComPL` because `CCPL` is
`ClientConfigurationPacketListenerImpl`. Two lanes the part's old diagrams
used as bare initials are gone under the two-letter rule: `Commands` is
`Cmds`, `AbstractContainerMenu` takes the existing `ACM`,
`InventoryChangeTrigger` is `ICT` and `AdvancementRewards` is `AR`. One
collision is recorded and deliberately not drawn: **`ExecuteCommand` names
two different classes** — the `/execute` command in
`net/minecraft/server/commands` (the keyed `ExecC`, used by the scoreboard
page) and the leaf task in `commands/execution/tasks`, which the engine page
therefore names only in prose and never as a lane.
