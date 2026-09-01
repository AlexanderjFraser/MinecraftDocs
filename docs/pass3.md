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

### Part III · The server

*(session B)* **Four pages that are already a pipeline, and the pipeline is
the part's best feature — but the entry point is in the wrong place.**

The four pages read, in `SUMMARY.md` order: the server tick → the level tick
→ players and sessions → server lifecycle. Three of those hand off cleanly:
the server tick's `MinecraftServer.tickChildren` calls the level tick, and
the level tick ends with packets the players page explains the destination
of. The lifecycle page is the odd one, and it is odd in a specific way:
**it contains the beginning of the story and is filed last.** A viewer
watching in page order sees a tick loop for two lectures before being told
where the loop came from.

Two ways out, and pass 3 should pick one deliberately:

- **Lifecycle first.** Startup → the tick → the level tick → players. This
  matches the code's chronology and gives the part a genuine cold open
  ("java -jar server.jar"). The cost is that the startup lecture has to name
  `ServerLevel`, `PlayerList` and `ChunkMap` before any of them are
  explained.
- **Lifecycle last, but split.** Keep the tick pages first and let the
  lifecycle page become the part's *closing* lecture on failure and
  teardown — which, after session B's fact-check, is where its most
  interesting material now is (see below).

**Recommendation: the second.** `anatomy` (Part I) already covers enough of
startup that a viewer is not lost, and the teardown material is a better
ending than an opening.

One more part-level observation: **Part III is the part where the corpus's
thread vocabulary is actually earned.** `anatomy` names the threads; Part III
is the first place a viewer sees one of them do a full lap. Whatever the
final lecture order, nothing between `anatomy` and `server-tick` should
assume the Server thread has been demonstrated, because it has not.

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
- **`server-lifecycle`'s split seam is not the one the pass-2 table
  predicted.** The table proposed "startup and `/stop` vs the side threads
  (RCON, query, management server)". Session B did **not** split it, and
  after the fact-check that proposal looks wrong: the side threads are four
  short bullets with no trace of their own, and a page made of them would
  violate rule 4 outright. The real seam runs the other way — the page holds
  **two traces**, `/stop` (which it draws) and startup (which it narrates as
  a numbered list because there was no room for a second diagram). If the
  page splits, it splits into *bringing a server up* and *taking one down*,
  and the side threads stay with whichever half creates them (startup) or
  stops them (shutdown) — they are created in one and stopped in the other,
  which is itself an argument for keeping one page. *(session B)*
- **`server-lifecycle` gained a second subject that is better than either
  half: the two failure paths.** Session B established that a tick-loop
  crash saves the world and a watchdog kill does not — `System.exit` runs
  the shutdown hook, which joins the Server thread, which is the wedged
  thread, so `Runtime.halt` fires ten seconds later with nothing written.
  That is a lecture: *how a Minecraft server dies*, with three endings
  (`/stop`, crash, watchdog) and one diagram comparing them. It is currently
  three bullets in "Invariants and surprises". Strongest new page candidate
  found in Part III. *(session B)*
- **`server-tick` is one page and should stay one**, but its "when it runs"
  section now carries a genuine sub-lecture: the event loop
  (`BlockableEventLoop`, `TickTask`, `shouldRun`, `managedBlock`, the
  budget's suspension while blocked, what can and cannot unpark the thread).
  That machinery is cited by Part IV, Part IX and Part X. Pass 3 should
  decide whether it is a box-out inside `server-tick` or a short shared page
  those parts link to; today every part re-explains a piece of it.
  *(session B)*
- **`players-and-sessions` is the longest page in the part and is two
  audiences, not two subjects.** The join trace is a *sequence* lecture; the
  respawn / dimension-change / disconnect section is a *comparison* — three
  paths differing in what survives. The seam is clean and the second half
  answers the question people actually ask ("what happens to my stuff"). If
  Part III gains a page, this is the second candidate after the death-of-a-
  server one. *(session B)*

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

### Diagram-shape notes from session B

- **`server-level-tick`'s diagram is the best-shaped in the part and the
  hardest to read**, because it is one lane (`ServerLevel`) talking to itself
  for a third of its height. The tick genuinely is one method calling its own
  private methods, so a sequence diagram is honest — but the *interesting*
  structure is the gating: which steps are behind `runsNormally`, which
  behind `emptyTime < 300`, which behind `isDebug`, which behind nothing.
  Three nested guards over twenty steps. Consider a second diagram — a
  flowchart of the guards — rather than trying to encode them in arrow
  labels. Session B added the guards to the prose and deliberately left the
  diagram alone.
- **`server-tick`'s diagram now has an `alt` block** (sprint vs the overload
  check) because they are exclusive branches of one *if*, which the old
  linear diagram misrepresented. Worth a corpus-wide look in pass 3: how many
  other sequence diagrams draw a branch as two consecutive arrows?
- **`server-lifecycle` has one diagram for two traces.** `/stop` is drawn;
  startup is a numbered list. Whichever way the split question goes, startup
  deserves a diagram — it is the only place in the corpus where the *JVM main
  thread* is a lane, and that lane handing off to the Server thread and never
  appearing again is the visual point.
- **`players-and-sessions`'s join diagram has nine lanes** and is the widest
  in the corpus. Three of them (`PlayerDataStorage`, `ChunkMap`,
  `ServerLevel`) appear twice each. It probably wants to be two diagrams —
  configuration/spawn-prep, then `placeNewPlayer`'s packet burst — split at
  the same seam the fact-check found interesting (the tasks are strictly
  sequential, so the diagram's implied concurrency is wrong anyway).

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

*(session B additions)*

- **`server-lifecycle`** — startup vs teardown vs the two failure paths. See
  section 2; the failure paths are the most lecture-shaped material the page
  has and are currently bullets.
- **`players-and-sessions`** — the join sequence vs the three exit paths
  (death, dimension change, disconnect). Different shapes, different
  audiences.

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

*(session B)*

- **`anatomy` → `server-tick` → everything server-side.** The Server thread
  is *named* in `anatomy` and *demonstrated* in `server-tick`; Parts IV–VIII
  all assume the demonstration. `server-tick` is the second-most load-bearing
  page in the corpus after `anatomy`.
- **`server-tick` → `server-level-tick` is the tightest coupling in the
  corpus.** The second page is literally one step of the first, and both
  pages had to be corrected together in session B (the flush count, the
  `haveTime` budget, the freeze gates). If any two pages in Part III merge,
  it is these — though session B's view is that they should not: the level
  tick is long enough on its own and the seam (`tickChildren` calls
  `ServerLevel.tick`) is exactly one call.
- **Part III → Part IV is a forward dependency the pages currently paper
  over.** `server-level-tick` names `ServerChunkCache`, `ChunkMap`,
  `DistanceManager`, `TicketStorage`, `FullChunkStatus` and `ChunkLevel`, and
  links forward for all of them. The level tick cannot be understood without
  knowing what "entity-ticking range" means. Either Part IV moves before
  Part III, or `server-level-tick` gets a two-sentence definition of the
  three ranges up front. **Recommendation: the second** — the full chunk
  pipeline is far too big to precede the tick loop.
- **`server-lifecycle` → `environment-attributes-and-timelines` is *not* a
  dependency, but `server-level-tick` now is.** The level tick's first
  statement is `EnvironmentAttributeSystem.invalidateTickCache`, and sky
  brightness is read out of that system. That makes **six** dependants on
  session C's unwritten page (the five session A counted, plus this one), and
  one of them is in Part III — earlier in the order than any of the others.
  This strengthens session A's recommendation that the page come early.
  *(session B)*

## 6 · Open questions for pass 3

- Does `math-and-primitives` move to `src/reference/`? *(session A)*
- Is `src/reference/threads.md` kept, given `anatomy` duplicates it?
  Session A had to fix the same errors in both. *(session A)*
- Do the reference pages appear in the lecture order at all, or are they
  explicitly "not watched"? The answer decides how much of Part II is a
  lecture. *(session A)*
- Does Part III open with the lifecycle page or close with it? See the Part
  III note in section 1. *(session B)*
- Is there a *how a server dies* lecture, and if so does it take the failure
  material out of `server-lifecycle` or does `server-lifecycle` become it?
  *(session B)*
- Where does the event-loop machinery (`BlockableEventLoop`, `TickTask`,
  `managedBlock`) actually live? Four parts cite it and none owns it.
  *(session B)*
- Part III's diagrams use `MS`, `SL`, `PL`, `SCC`, `CM`, `G`/`SGPL` — the
  `G` for `ServerGamePacketListenerImpl` in `players-and-sessions` is the
  odd one out and should become `SGPL` when the standard lands. *(session B)*
