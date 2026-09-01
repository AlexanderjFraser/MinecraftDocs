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

<!-- one subsection per part, appended by each session -->

### Part I · Anatomy

*(session A)*

### Part II · Foundations

*(session A)*

---

## 2 · Page-level structure

*Pages that want to be split, merged, reordered internally, or turned
into something other than the standard template. A split that pass 2
executed is recorded in [pass2.md](pass2.md); this section is for the
ones pass 2 deliberately left alone as presentational.*

---

## 3 · The diagram plan

*Per part: which diagrams exist, which are the wrong shape (a
`sequenceDiagram` where the truth is a graph or a state machine), and
where a diagram would replace a wall of text. The standing convention
is mermaid-in-page, never images (CLAUDE.md); if that changes it is a
deliberate decision made here.*

### The lane-abbreviation standard

Carried from [pass2.md](pass2.md): sequence-diagram lane names are class
names everywhere, but the same class is abbreviated differently across
parts — `ServerGamePacketListenerImpl` is *SG*, *SGPL*, *CL* and *G* in
different parts; `ClientPacketListener` is *CPL*, *CP* and *CL*.
Sessions 9, 11 and 12 used **`SGPL` / `CPL`**, which makes it the
majority spelling and the default choice. Pass 3 settles it corpus-wide
in one sweep and writes the standard into `TEMPLATE.md`.

---

## 4 · The lecture order

*Raw material for `src/lectures.md`. A "lecture" is one recording, one
trace, one diagram. Pass 2 keeps finding pages that are two lectures and
pages that are half a lecture; note both here, with the trace each one
would follow — the trace is what decides, not the page count.*

### Candidate opening lectures

### Pages that are two lectures

*(the split table in [pass2.md](pass2.md) is the working list; this
section records the ones where the **lecture** boundary differs from the
**page** boundary)*

### Half-lectures that want a neighbour

---

## 5 · Through-lines and dependencies

*Which page must be watched before which. A lecture series is linear
even though the code is a graph; the places where that hurts are worth
knowing before the order is drafted.*

---

## 6 · Open questions for pass 3

