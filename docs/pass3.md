# Pass 3 — the restructuring notebook (open while pass 2 runs)

*Started 2026-09-01, at the beginning of pass-2 session A. Pass 3 is the
restructuring pass defined in [plan.md](plan.md): each part takes the
shape of the system it explains, the diagram plan is drawn, and the
lecture order is drafted into `src/lectures.md`. This file is where
pass-2 sessions **write pass 3's inputs down as they find them** —
observations you can only make with the decompile open and the page in
front of you, which would otherwise be lost by the time pass 3 starts.*

**How to use this file.** Every pass-2 session appends here. A note
belongs in this file (rather than in [pass2.md](pass2.md)'s hand-off
section) when it is about **shape** — what order things should be
explained in, what a page or part should *be*, what a diagram should
look like, where a lecture starts and stops. Notes about correctness,
completeness or wording go to [pass2.md](pass2.md) instead. When in
doubt, put it here and let pass 3 discard it; the expensive thing is
the note that was never written.

Each note names the session that wrote it, so pass 3 can weigh a note
against the part it came from.

---

## 1 · Part shapes

*Does this part want to be a sequence of pages, a pipeline with a
through-line, a hub-and-spokes, or a single long page? Written per part
as pass 2 works through it.*

### Part I · Anatomy

*(session A)* **One page, and it should stay one page — but it is doing
two jobs and only one of them is a lecture.**

The lecture is the trace: main() → bootstrap → window → world load → the
two loops → the local channel. That is a genuinely good opening
recording, because every later part's first diagram lane is a thread
named here.

The *threads table* is the other job, and it is reference material. It
already exists twice — the page and `src/reference/threads.md` — and
session A had to fix the same errors in both. Two options for pass 3:
either the page keeps a four-row table (Render, Server, Netty, workers)
and defers the rest to the reference page, or the reference page goes
away and the page owns it. **Recommendation: the first.** The lecture
only needs the four threads a viewer must hold in their head; RCON,
query, the management server and the situational list are look-up.

The other structural note: `anatomy` is now the page that says
"singleplayer is multiplayer with a loopback — *and here are the
exceptions*". That exception list (pause, view distance, publishing,
gizmos) is load-bearing for Parts IX and X and currently only lives
here. Check in pass 3 that the lecture order puts it before anything
that relies on it.

### Part II · Foundations

*(session A)* **Six pages that are not the same kind of thing, and
pretending they are is the part's main structural problem.**

Sorted by what they actually are:

- **`identifiers-and-registries`** — a genuine lecture with two traces
  (an item at bootstrap; a biome to the client). Strongest page in the
  part, and the one every other part cites.
- **`tags`** — a genuine lecture, one trace, clean.
- **`resource-system`** — a genuine lecture with two traces (F3+T and
  `/reload`) that are *the same mechanism seen twice*. Pass 3 should
  decide whether that is one lecture with a coda or two.
- **`data-components`** — a lecture, but its trace (enchanting) is
  really Part VII material borrowed to illustrate a Part II mechanism.
  Watch for a collision when Part VII is restructured.
- **`codecs-nbt-json`** — half lecture, half catalogue. The trace ("one
  `ItemStack`, four ways") is excellent and should probably *lead* the
  part rather than sit third; the `ByteBufCodecs` / `ExtraCodecs`
  inventory around it is reference.
- **`math-and-primitives`** — **not a lecture at all**, and it says so
  in its own header ("No trace — a table of who owns which space").
  After session A it is longer and even more reference-shaped.

**Recommendation for pass 3:** stop treating Part II as six equal pages.
`math-and-primitives` is a *reference appendix* the other parts link
into, and it should either move to `src/reference/` or be explicitly
badged as "look this up, don't watch it". That frees Part II to be four
or five real lectures with an obvious order: identifiers/registries →
tags → resources → codecs → components.

There is also a **dependency knot** worth drawing before the order is
fixed: registries need tags to explain freezing, tags need registries to
explain binding, both need the resource system to explain *when*, and
the resource system's `/reload` trace needs all three. Session A pushed
each page to link rather than re-explain, but the cycle is real and the
lecture order has to break it somewhere. The cheapest cut is probably to
let the registries lecture state the freeze rule without justifying it,
and let tags pay it off.

---

## 2 · Page-level structure

*Pages that want to be split, merged, reordered internally, or turned
into something other than the standard template. A split that pass 2
executed is recorded in [pass2.md](pass2.md); this section is for the
ones pass 2 deliberately left alone as presentational.*

- **`math-and-primitives` → reference.** See Part II above. It is the
  clearest case in the corpus of a page that is not a lecture.
  *(session A)*
- **`anatomy`'s threads table → trim to four rows**, deferring the rest
  to `src/reference/threads.md`. *(session A)*
- **`sound` is two pages' worth of material in one**, and the seam is
  clean: (1) the engine — threads, channels, buffers, the OpenAL
  wrapper; (2) what makes a sound happen — the two wire paths (sound
  packet vs level event), prediction, music and ambience. Session A did
  **not** split it, because the fact-check's additions landed on both
  halves roughly evenly and neither half is over-long alone. But it is
  now the best-argued split candidate outside the pass-2 table, and half
  (2) is the half a viewer actually wants. *(session A)*
- **`codecs-nbt-json`'s trace should probably open Part II**, whatever
  order the pages land in — it is the most concrete thing in the part and
  everything else is machinery for it. *(session A)*

---

## 3 · The diagram plan

*Per part: which diagrams exist, which are the wrong shape (a
`sequenceDiagram` where the truth is a graph or a state machine), and
where a diagram would replace a wall of text. The standing convention
is mermaid-in-page, never images (CLAUDE.md); if that changes it is a
deliberate decision made here.*

### Wrong-shaped diagrams found in session A

- **`resource-system`'s F3+T diagram is a sequence diagram of something
  that is not a sequence.** The interesting structure is the
  prepare/apply *lattice* — N listeners preparing concurrently, each
  apply gated on both "all prepares done" and "previous listener done" —
  and a sequence diagram with one generic lane cannot show it. This
  wants a flowchart, or a sequence with three listeners drawn
  explicitly. The clearest diagram-shape problem session A saw.
- **`math-and-primitives` has no diagram and arguably needs one**: the
  coordinate spaces and their conversions are a graph (block ↔ chunk ↔
  section ↔ quart ↔ region), and the table makes the reader assemble it
  themselves.
- **`anatomy`'s trace mixes a startup sequence with two steady-state
  loops** in one diagram. The loops are drawn as `loop` blocks inside
  the startup sequence, which reads oddly — the world-load spin and the
  two tick loops are concurrent, not sequential. Consider splitting into
  "startup" and "steady state".
- **`identifiers-and-registries`'s two traces are the right shape** and
  are a good model for the rest of the corpus: one bootstrap-time trace,
  one runtime trace, same subject.

### The lane-abbreviation standard

Carried from [pass2.md](pass2.md): sequence-diagram lane names are class
names everywhere, but the same class is abbreviated differently across
parts — `ServerGamePacketListenerImpl` is *SG*, *SGPL*, *CL* and *G* in
different parts; `ClientPacketListener` is *CPL*, *CP* and *CL*.
Sessions 9, 11 and 12 used **`SGPL` / `CPL`**, which makes it the
majority spelling and the default choice. Pass 3 settles it corpus-wide
in one sweep and writes the standard into `TEMPLATE.md`.

Session A adds one open sub-question: `sound` uses long abbreviations
(`CPL`, `SM`, `SE`, `SBL`, `CA`) while `anatomy` uses very short ones
(`MC`, `MS`, `RS`, `IS`, `C`). Both are internally consistent. The
standard has to say whether one- and two-letter lanes are allowed at all
when the class name is already short.

---

## 4 · The lecture order

*Raw material for `src/lectures.md`. A "lecture" is one recording, one
trace, one diagram. Pass 2 keeps finding pages that are two lectures and
pages that are half a lecture; note both here, with the trace each one
would follow — the trace is what decides, not the page count.*

### Candidate opening lectures

- **`anatomy`.** Confirmed by session A: it is the only page whose
  vocabulary (thread names) every other page's diagrams already use. It
  has to be first, and it has to be watched rather than looked up.
  *(session A)*

### Pages that are two lectures

*(the split table in [pass2.md](pass2.md) is the working list; this
section records the ones where the **lecture** boundary differs from the
**page** boundary)*

- **`sound`** — the engine vs what makes a sound happen. See section 2.
  *(session A)*
- **`resource-system`** — F3+T and `/reload` are one mechanism, but they
  have different *audiences* (pack authors vs data-pack authors). That
  may be a lecture boundary even though it is not a page boundary.
  *(session A)*

### Half-lectures that want a neighbour

- **`math-and-primitives`** is not half a lecture, it is zero lectures —
  see section 2. If it stays in the systems tree it should be paired
  with something as "the reference interlude". *(session A)*

---

## 5 · Through-lines and dependencies

*Which page must be watched before which. A lecture series is linear
even though the code is a graph; the places where that hurts are worth
knowing before the order is drafted.*

- **`anatomy` → everything.** Thread names are the shared vocabulary.
  *(session A)*
- **The Part II knot.** registries ↔ tags ↔ resource-system is a genuine
  cycle; see the Part II note above for where to cut it. *(session A)*
- **`data-components` ← `identifiers-and-registries`.** Prototypes are
  bound onto `Holder.Reference`s, so components cannot be explained
  before holders. Session A made both pages say this; the order must
  respect it. *(session A)*
- **`sound` → `environment-attributes-and-timelines` (session C's new
  page).** Sound now depends on the environment-attribute stack for
  music and ambience, joining `biomes`, `lightmap-fog-and-sky`,
  `level-data-and-rules` and `ai-goals-and-brains`. That is **five**
  dependants for a page that does not exist yet — more load-bearing than
  the pass-2 queue assumed, and it should come early in the order rather
  than late. *(session A)*

---

## 6 · Open questions for pass 3

- Does `math-and-primitives` move to `src/reference/`? *(session A)*
- Is `src/reference/threads.md` kept, given `anatomy` duplicates it?
  Session A had to fix the same errors in both. *(session A)*
- Do the reference pages appear in the lecture order at all, or are they
  explicitly "not watched"? The answer decides how much of Part II is a
  lecture. *(session A)*
