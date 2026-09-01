# The plan — the passes

*Rewritten 2026-09-01, at the end of pass 1. This is the document every
session reads first and ticks last. Pass 1's catalogue, protocol and
session log are archived in [pass1.md](pass1.md); the running work queue
for the current pass is [pass2.md](pass2.md).*

## Where we are

Pass 1 is done: fifty-six pages, thirteen parts, twelve sessions, all
deployed, every name verified. What pass 1 could not guarantee is that
the *claims* attached to those names are true (the verifier checks
existence, not truth), that nothing in scope was missed, or that the
uniform page-per-system format is the most interesting shape for each
part. That is what the remaining AI passes are for — the corpus gets
correct, then complete, then well-shaped, then well-written, and only
then does the owner spend reading time on it.

The planned pass-1 closing session (16) never ran; its to-dos are folded
into pass 2's queue in [pass2.md](pass2.md).

## The passes

| pass | what | status |
|---|---|---|
| **1 — rough draft** | every page drafted from the decompile, names verified | done — [pass1.md](pass1.md) |
| **2 — completeness and accuracy** | every claim fact-checked against the decompile; gaps filled; pages split/added freely — length is not a concern here | **current** |
| **3 — restructuring** | each part gets the shape of the system it explains; diagram/image plan; lecture order drafted | next |
| **4 — polish** | wording, per page; corpus-wide consistency sweep; cut what pass 2 over-added | after 3 |
| **5+ — human feedback** | the owner reads part by part with the decompile open; `<!-- Q: … -->` comments answered in the prose; lecture order confirmed; then voice and cuts | after 4 |

The rules stand for every pass: names never code · how the system works,
not how the code reads · newest version only (26.2) · trace-driven ·
`python tools/verify_names.py` clean before every commit that touches a
page. And the pass-1 addition still stands: claims come from the
decompile, never from model memory of 1.21.

---

## Pass 2 — completeness and accuracy (current)

**Goal:** everything the corpus should say is on the site, and everything
the site says is true. Do not worry about page length — add and split
freely in the name of completeness; pass 4 cuts.

### Accuracy: the fact-check protocol

`verify_names.py` proves a name exists; it cannot prove a claim true. So
each page gets an **adversarial fact-check**: one agent per page, given
the page and access to `reference/26.2`, whose brief is to *falsify*,
not confirm — re-derive from the decompile every checkable claim (which
thread runs it, who calls whom in what order, what crosses the wire and
when, which class owns which state, every "invariant and surprise") and
return a discrepancy list: **wrong** (the decompile disagrees),
**unverifiable** (the page asserts something the agent could not find),
or **misleading** (true but the emphasis implies something false). The
session fixes the page from the list. An empty discrepancy list from an
agent that quotes no decompile evidence is a failed check, not a pass.

The *Load-bearing facts* section of [pass2.md](pass2.md) — each stated
once, in one page — is the seed list: those get checked hardest, because
every other page leans on them.

### Completeness: the inverse question

The same agent answers: *what is in this page's scope in the decompile
that the page never mentions?* — plus the standing queue in
[pass2.md](pass2.md): the split candidates, the catalogue gaps needing
a ruling (the debug cluster, `client/resources`, `client/animation`,
`util/parsing`, Blaze3D's Vulkan/platform halves), and the pass-1
closing-session leftovers. Known new-page work already agreed:

- **`environment-attributes-and-timelines`** — the most load-bearing gap:
  four written pages explain `world/attribute` / `world/timeline`
  piecemeal without owning it. Write it (Part IV, or a short part of its
  own), then cut the borrowed paragraphs out of `biomes` and
  `lightmap-fog-and-sky`.
- **The rendering split.** Part X currently holds two subjects. It
  becomes **Part X · The client** (the loop and tick/frame interleave,
  `ClientLevel`, input and options, GUI and screens, the HUD, sound) and
  a new **Part XI · Rendering** (`the-frame` as the opening trace,
  `blaze3d`, `level-rendering`, `models-and-atlases`, `entity-rendering`,
  `lightmap-fog-and-sky`, `particles`), with new pages where pass 1
  found lectures hiding inside pages — the text/font engine out of
  `gui-and-screens`, and possibly the frame graph out of
  `level-rendering`. Later parts renumber (worldgen → XII, commands →
  XIII, appendix → XIV); the exact page allocation is the client
  sessions' call, this is the default.
- Splits from the [pass2.md](pass2.md) table are executed in this pass
  **when the fact-check adds material and the page is carrying two
  subjects anyway**; splits that are purely about presentation wait for
  pass 3.

### Session protocol

One session = one part (small parts bundle, as in pass 1). Each session:

1. **Read** this file, `CLAUDE.md`, and the part's entries in
   [pass2.md](pass2.md) (split candidates, load-bearing facts, gaps).
2. **Check** — spawn one fact-check agent per page, in parallel, with
   the brief above. Fact-check output is not committed.
3. **Fix** — correct every *wrong*, resolve every *unverifiable* (fix
   the page or confirm against the decompile and keep it), add what the
   completeness question surfaced, execute this part's agreed splits and
   new pages.
4. **Verify** — `verify_names.py` clean; `mdbook build` clean;
   `SUMMARY.md` and cross-links updated; regenerate `class-index` if
   pages moved.
5. **Ship** — commit (`pass 2, Part N: <summary>`), deploy, tick the
   part in the schedule below, log below. Anything left for passes 3–5
   (structural observations, wording debt, things added on spec that
   pass 4 may cut) appends to [pass2.md](pass2.md)'s hand-off section.

### Schedule

Part order as in pass 1, with the pass-1 leftovers first. Tick as done.

- [ ] **Session A** — Part I `anatomy` (re-read against the finished
  corpus: the render-thread claim, the threads table vs
  `reference/threads.md`) + `sound` (predates the extract/render split)
  + Part II Foundations.
- [ ] **Session B** — Part III The server.
- [ ] **Session C** — Part IV The world, plus the new
  `environment-attributes-and-timelines` page.
- [ ] **Session D** — Part V Blocks.
- [ ] **Session E** — Part VI Entities.
- [ ] **Session F** — Part VII Items · Part VIII The player.
- [ ] **Session G** — Part IX Networking.
- [ ] **Session H** — Part X: the client half, and the X/XI split lands
  here (SUMMARY, renumbering, redirects if any).
- [ ] **Session I** — Part XI Rendering: the render half plus its new
  pages.
- [ ] **Session J** — Part XII World generation.
- [ ] **Session K** — Part XIII Commands · Part XIV Appendix (the gaps
  list gets its rulings here; naming-drift and glossary re-swept after
  every earlier session's changes).

---

## Pass 3 — restructuring (sketch; charter written when it starts)

Is each part presented in the most interesting shape? The uniform
template served pass 1; pass 3 lets the structure of the documentation
mirror the structure of the code. Small self-contained systems (blocks,
foundations) stay short self-contained pages. Long sequential systems
(rendering, worldgen, the chunk pipeline) should *read like a pipeline*
— a part-level through-line where each page hands off to the next.
Networking is two connected pipelines meeting at the wire and should
read like one. Also in this pass:

- **Diagrams and images.** Plan visuals part by part: where a diagram
  replaces a wall of text, which existing diagrams are wrong-shaped
  (sequence where the truth is a graph). The standing convention is
  mermaid-in-page, never images; if static images are wanted, that is a
  deliberate decision here — pipeline, format, theming, where they live
  — not a drift.
- The **lane-abbreviation standard** for sequence diagrams (`SGPL`/`CPL`
  is the pass-1 majority; settle it corpus-wide).
- **Draft the lecture order** into `src/lectures.md` — restructuring and
  lecture order are the same judgement. The owner confirms it in pass 5.

## Pass 4 — polish (sketch)

Per page: does it read well, is everything needed explained and nothing
more? This is where pass 2's "don't worry about length" bill comes due —
cut what over-grew, using pass 2's on-spec log. Corpus-wide: one
terminology sweep (the glossary is the checklist), one voice sweep
against the best page, links and cross-references complete.

## Pass 5+ — the owner reads

Unchanged from the original conception: part by part, decompile open,
questions left **in the page** as `<!-- Q: … -->` comments; a session
answers each in the prose — if the owner had to ask, the page was wrong
or missing it — and removes the comment. The owner confirms or reorders
`lectures.md`. Then voice and cuts, and recording.

## Risks

- **The rubber-stamp fact-check.** An agent that confirms instead of
  falsifies makes pass 2 worthless. The brief demands discrepancies or
  quoted evidence; sessions should distrust clean reports on pages the
  split table already calls overloaded.
- **Growth without limit.** Pass 2 adds freely by design; passes 3–4
  must actually cut. Every session logs what it added speculatively.
- **26.3 lands mid-pass.** Finish the current pass on 26.2; re-verify
  the whole corpus once, in one session, between passes.
- **Renumbering churn.** The X/XI split renumbers three parts; do it in
  one session (H), everywhere at once, or links rot.

## Session log — pass 2 onward

- **2026-09-01, planning session** — pass 1 closed out and archived to
  [pass1.md](pass1.md); this plan written (passes 2–5); pass2.md
  repurposed from "the owner's read" to the pass-2 work queue (the
  owner's read is now pass 5); CLAUDE.md updated to match. Decisions:
  closing session 16 folded into pass 2; adversarial per-page
  fact-check protocol; rendering split out of Part X into its own part;
  `environment-attributes-and-timelines` page approved; lecture order
  drafted in pass 3 rather than deferred to the owner.
