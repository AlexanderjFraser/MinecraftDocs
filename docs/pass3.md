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

### Part IV · The world

*(session C)* **Part IV is a pipeline with two reference pages bolted to
its side, and it is now nine pages long.** The pipeline is real and reads
in order: a ticket arrives → holders and futures → the generation pyramid →
light → the chunk becomes a `LevelChunk` → it is sent → it is saved →
eventually it unloads. Four pages sit on that line (`tickets-and-loading`,
`chunk-generation-pipeline`, `lighting`, `chunk-storage`) and they hand off
to each other cleanly enough that pass 3 could make the hand-offs explicit
and gain a through-line for free.

The other five are not on it:

- **`chunk-anatomy` is the data page** and has to come first — every other
  page in the part names `LevelChunkSection`, `PalettedContainer` and the
  heightmaps. It is the part's vocabulary page, the way `anatomy` is the
  corpus's.
- **`block-ticks-and-fluids` is two pages wearing one coat**, and session C
  is the first to say so with evidence. The scheduled-tick system
  (`ScheduledTick`, `LevelTicks`, `LevelChunkTicks`, dedup, drain order,
  save/load) is a complete lecture with its own trace, and the fluid model
  (`FlowingFluid`, `getNewLiquid`, the slope search, lava's overrides) is a
  *different* complete lecture that happens to be the tick system's biggest
  customer. The seam is exactly at trace step 5 → 6. Session C did not split
  it because the fact-check did not force the issue, but the page grew again
  here and the split is now the strongest un-executed one in Part IV.
- **`game-events-and-poi` is the split the pass-2 table already names** and
  session C confirms it: the fact-check produced two disjoint reports with
  no shared classes between them. Sculk/vibrations and villager POI share a
  package and nothing else.
- **`level-data-and-rules` is a reference page** — a who-owns-what table
  with a lot of file paths — and it says so itself ("Short, no trace"). It
  belongs with `math-and-primitives` in whatever pass 3 decides reference
  pages are.
- **`environment-attributes-and-timelines` (new, session C) is a genuine
  lecture** and is the best-shaped page in the part: one mechanism, one
  trace, and a second trace on the client that is the *same* trace seen
  from the other side. See section 4.

**Recommendation for pass 3:** the part wants to be read as
`chunk-anatomy` → the four-page pipeline → `environment-attributes` →
`block-ticks-and-fluids` (or its two halves) → `game-events-and-poi` (or
its two halves), with `level-data-and-rules` demoted to reference. That is
also very nearly the current order, which is a good sign.

### Part V · Blocks

*(session D)* **Part V is a hub with four spokes, and the hub is not
where a viewer would expect it.** `blocks-and-states` is the vocabulary
page — `StateDefinition`, `StateHolder`, the flag word, `Level.setBlock`
— and the other four all reach back into it. But it also carries the
part's best *trace* (placing a stair), so it is doing the same double
duty `anatomy` does in Part I: reference material and a lecture sharing
one page.

The four spokes are not equal:

- **`block-interaction` and `block-breaking` are one subject in two
  halves** — right-click and left-click, both under prediction, both
  through `ServerPlayerGameMode`, both reconciled by the same ack. They
  share the prediction ledger, the reach check, the sequence number and
  the packet-ordering argument, and session D had to fix the *same*
  ack-timing sentence in both. Pass 3 should decide whether that is one
  two-part lecture or two lectures with a shared preamble; what it should
  not be is two pages each re-deriving the prediction machinery.
- **`block-entities` is a genuine standalone lecture** and the
  best-shaped page in the part: one object, one trace, and a real
  argument (the furnace tells you nothing; the world state and the menu
  do). It barely depends on the rest of the part.
- **`redstone` is now three lectures in a trench coat.** It was two —
  the dust/neighbour-update cascade and the piston/block-event machinery
  — and session D added a third by filling the diode and observer gap.
  See section 2.

**The part's real dependency**, and the thing pass 3 must not break: the
*two update channels* — shape updates (both sides) versus neighbour
updates (server only) — are established in `block-interaction` and then
assumed by `redstone` and by half of `blocks-and-states`. Whatever order
the part ends up in, that distinction has to be taught before redstone.
It is also, on session D's evidence, the single most error-prone idea in
the part: three of the five pages had it subtly wrong somewhere.

**Recommendation for pass 3:** `blocks-and-states` (or its data half)
first, then interaction and breaking as a pair, then `block-entities`,
then redstone last — which is the current order, and it survives
scrutiny. The open question is whether the part opens with a reference
page.

### Part VI · Entities

*(session E)* **Part VI is a ladder, not a hub, and it has a missing
rung.** The seven pages genuinely build: `entity-anatomy` gives you the
object, `entity-lifecycle` puts it in a world, `synched-entity-data` and
`attributes` are the two channels that describe it, `movement-and-collision`
is what it does, `ai-goals-and-brains` is why, `damage-and-death` is how it
stops. That order survives scrutiny and should not be reshuffled.

The missing rung is **authority**. Session E's largest correction was that a
tracked mob's physics do not run on the client at all — the four predicates
`Entity.isLocalInstanceAuthoritative`, `Entity.canSimulateMovement`,
`Entity.isEffectiveAi` and `Entity.isClientAuthoritative` decide who
simulates, and they invert the naive picture in *both* directions (a mob is
server-authoritative; a player is client-authoritative on both sides). That
idea is currently taught as a new opening subsection of
`movement-and-collision`, but it is a prerequisite for at least four pages
across three parts: this one, Part VIII's `input-to-movement`, Part IX's
`what-the-client-is-told`, and Part X's client-tick material. It is the
Part VI analogue of Part V's two-update-channels distinction — the single
most error-prone idea in the part, and the one that has to be taught before
anything that depends on it. **Pass 3 should decide where it lives.** The
honest options are: a short page of its own at the head of Part VI; a
section of `entity-anatomy` (which is already the part's map page); or
promotion into Part I's `anatomy`, where the client/server split is
introduced. Session E's guess is `entity-anatomy`, because it is the only
one of the three that is already about *what an entity is on each side*.

**Two pages are doing reference work inside a lecture.**
`synched-entity-data` now carries an ordered 43-entry serializer catalogue
with wire ids, and `attributes` carries the 40-attribute catalogue. Both are
tables a viewer would pause the video to read, which is the definition of
something that belongs in `src/reference/` with the page pointing at it.
Neither is a split candidate in the usual sense — the *lecture* halves of
both pages are the right length already.

**`damage-and-death` is the part's longest single trace and it stops
halfway.** It covers `LivingEntity` and never mentions that ~30 non-living
classes override `Entity.hurtServer` with entirely separate rules. That is a
coverage decision pass 3 has to make (section, sibling page, or appendix
table); it is recorded in [pass2.md](pass2.md)'s hand-off.

**Diagram note.** `entity-lifecycle`'s sequence diagram had the light and
spawn-rule checks *after* entity construction, when the decompile runs every
type-level check first and only then builds the mob. Session E fixed it, but
the deeper problem is that a `sequenceDiagram` is the wrong shape for the
spawner: it is a **filter cascade**, not a conversation, and almost every
step is a rejection. A flowchart with the reject arrows drawn would say more
in less space and would make the "one y roll per category per tick" point
visible instead of stated. Same argument, more weakly, for
`ai-goals-and-brains`'s villager day, which is a clock driving a state
filter rather than a call sequence.

### Part VII · Items and inventories

*(session F)* **Part VII is two systems and a shared vocabulary, and the
part currently pretends it is one.** `items-and-stacks` and
`containers-and-menus` are the vocabulary — what a stack *is*, and how two
machines agree about a set of them. `recipes`, `enchantments` and
`loot-tables` are three independent data-driven engines that happen to
produce or decorate stacks. The second three do not depend on each other at
all; the first two are a hard prerequisite for all of them. That is a
**two-tier shape**, not a chain, and the lecture order should say so rather
than running the five as a list.

**`loot-tables` is misnamed for what it is.** The page's own headline is
that the parameter machinery lives outside the loot package and that
predicates are the bigger client — `/execute if predicate`, entity-selector
predicates, advancement conditions, villager trade filters and every
enchantment effect condition all run on it, and **five of the twenty-six
parameter sets have no loot caller at all**. Session F fixed the framing but
left the structure. The honest options for pass 3: rename the page to
something like *predicates and contexts* with loot as its worked example;
split a short `contexts-and-predicates` page out of the front of it and let
Part XIII and the advancement material depend on that instead of on a page
called "loot tables"; or leave it and accept that two later parts point at a
page whose title does not describe what they need from it. Session F's guess
is the split, because the dependants are in different parts.

**`enchantments` is three shapes stacked.** A trace (Fire Aspect), a hook
table (thirty-odd `EnchantmentHelper` entry points, which is the genuinely
useful artefact and is now nearly complete), and a fourth section —
*getting one onto an item* — that is a lecture of its own: the table's
bookshelf walk and seed, the anvil's arithmetic, the grindstone, the
providers, `/enchant`. The trace and the hook table belong together; the
acquisition half is a different subject with a different audience and would
pair naturally with `containers-and-menus`.

**The use pipeline is traced in one direction only.** `items-and-stacks`
follows a *completion* (eating, thirty-two ticks then finish) and mentions
release in a single invariant — yet `ItemStack.useOnRelease` is the third
term in the completion guard and the bow, the crossbow and the trident all
take the other branch, finished by a `ServerboundPlayerActionPacket`. A
*drawing a bow* trace is a real second lecture and it is currently a
sentence.

**Split candidates confirmed, none executed.** `items-and-stacks` grew a
durability section and is now three subjects (the data model, the use
pipeline, the eating trace); `containers-and-menus` grew the creative
parallel protocol and the crafting-result side channel and is now three
(the model, the click protocol, the exceptions). Both seams are real and
both are presentational; the fact-check did not force either.

### Part VIII · The player

*(session F)* **Part VIII has an ordering problem the pages cannot solve
individually: authority has to be taught before any of them.** Session E
identified this from the entity side; session F confirms it from the player
side and can now be specific. `input-to-movement` gained a four-method
matrix (`Entity.isClientAuthoritative`,
`Entity.isLocalInstanceAuthoritative`, `Entity.canSimulateMovement`,
`Entity.isEffectiveAi`) with the per-class answers, because none of the
page's claims are checkable without it; `player-anatomy` gained a shorter
version of the same thing, because its two-phase tick makes no sense
otherwise; and `movement-and-collision` already carries a third. **Three
pages in two parts now teach the same matrix.** Pass 3 must pick one owner.
Session F's recommendation differs from session E's: put it in
`entity-anatomy` as session E suggested *only* if Part VI precedes Part
VIII in the order; otherwise `input-to-movement` is the better host,
because the player is the case where the matrix is counter-intuitive in
both directions at once (client-authoritative everywhere, yet simulated on
the server and discarded).

**`player-anatomy` is a reference page with one excellent trace inside
it.** The class ladder, `Inventory`'s slot arithmetic, `Abilities`,
`GameType` and the persistence list are all lookup material. The
two-phase tick — with the record-simulate-snap-back bracket that session F
added — is a lecture, and it is the one thing on the page nobody would
guess. The split is obvious and was already in the pass-2 table; the
fact-check strengthened it by making the trace half better.

**`the-sword-swing` now documents three melee paths and traces one.**
Ordinary attack, `PiercingWeapon` (its own packet, no target id,
server-side raycast, hits everything along the ray) and `KineticWeapon`
(reached from item *use*, gated on closing speed) all end in damage and only
the first goes through `Player.attack`. The spear is a genuinely different
lecture — it is the 26.2 combat change a viewer will most want explained —
and it is currently two invariants at the bottom of someone else's page.

**`hunger-xp-and-effects` is three pages in a trench coat, and the fact-check
made that worse rather than better.** They share only "the server owns it
and tells you", and after session F each third has its own surprises
(exhaustion's creative no-op; the total-experience-only change detection;
the infinite-effect re-send hole). Status effects in particular have their
own registry, their own instance model with a hidden-effect stack, their own
packets and their own client-side blend — that is a page. Pass 3 should
split at least effects off; the hunger and XP halves are small enough to
stay together, and they do at least meet, in the enchanting seed and in
mending.

**Diagram note.** `player-anatomy`'s tick diagram is the one place in the
corpus where a sequence diagram is *exactly* the right shape and was
previously drawn wrong — the record-and-restore bracket around
`ServerPlayer.doTick` is a conversation with an explicit undo, and it now
shows. By contrast `the-sword-swing`'s trace is really a fourteen-step
*pipeline over one number* (base damage in, total damage out, with two
different curves applied to two different terms), and a sequence diagram
across seven lanes buries that. A left-to-right flow of the damage value,
annotated with what multiplies it where, would teach the whole page in one
picture.

---

---

## 2 · Page-level structure

*Pages that want to be split, merged, reordered internally, or turned
into something other than the standard template. A split that pass 2
executed is recorded in [pass2.md](pass2.md); this section is for the
ones pass 2 deliberately left alone as presentational.*

- **`math-and-primitives` → reference.** See Part II above. It is the
  clearest case in the corpus of a page that is not a lecture.
  *(session A)*
- **`block-ticks-and-fluids` → two pages.** *(session C)* Not in the pass-2
  split table, and it should have been. The tick scheduler and the fluid
  model are independent systems with independent traces; the page's own
  numbered trace changes subject at step 6 and never comes back. The
  scheduler half is also the part's answer to "how does anything happen
  later", which several other parts (redstone, blocks) lean on, so it is
  worth being findable on its own. Fluids keep the bucket trace; the
  scheduler gets a repeater or a sapling.
- **`game-events-and-poi` → two pages, confirmed.** *(session C)* The
  pass-2 table's proposed seam is right and the fact-check found it
  independently: the two halves share no classes, no traces, and no
  invariants. The only thing they share is `world/level/gameevent` sitting
  next to `world/entity/ai/village/poi` in the tree — a packaging fact, not
  a conceptual one.
- **`level-data-and-rules` → reference.** *(session C)* Its header already
  says "Short, no trace"; its body is a table of files. Session C's
  fact-check found eleven wrong *paths* and almost nothing wrong about
  mechanism, which is the signature of a reference page. If pass 3 keeps a
  reference tier, this and `math-and-primitives` are its first two members.
- **`environment-attributes-and-timelines` does not want to move.**
  *(session C)* It was floated as "Part IV or a short part of its own"; the
  answer is Part IV. Everything it explains is per-level state resolved
  through the level, and three of its consumers (`block-ticks-and-fluids`,
  `game-events-and-poi`, `level-data-and-rules`) are its neighbours in the
  part. Making it a part of its own would isolate it from exactly the pages
  that motivate it.
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
- **`redstone` → three pages, and session D made the case worse.**
  *(session D)* The pass-2 table already lists it (the experimental-evaluator
  coda vs the default trace), but that is the wrong seam. The page holds
  three independent mechanisms with three independent traces: the
  **dust/neighbour-update cascade** (a lever, two dust, the seven-position
  hand-issued fan-out, and the two evaluators — the experimental one is a
  coda *to this*, not to the page); the **piston** (block events, the
  one-tick delay, `PistonStructureResolver`, the moving block entity, and
  the client re-simulating from `ClientboundBlockEventPacket`); and the
  **diodes and the observer**, which session D added because the page named
  `DiodeBlock.checkTickOnNeighbor` and nothing else while comparators,
  repeaters and observers were absent entirely. Those three share only
  `SignalGetter`. The clean split is *signal and dust* / *pistons and block
  events* / *diodes, comparators and observers*, with the signal-reading
  primitives in the first. The observer belongs with the diodes for
  circuit-building reasons but is mechanically the odd one out — it fires
  on shape updates — which is a good closing beat for that lecture rather
  than a problem.
- **`block-interaction` + `block-breaking` → possibly one lecture in two
  parts.** *(session D)* See Part V in section 1. They are not too long
  individually; the duplication is conceptual, not textual.
- **`blocks-and-states` → data page + placement trace, still the right
  call.** *(session D)* The pass-2 table's proposed seam is confirmed: the
  first half (`Block` / `BlockBehaviour` / `StateDefinition` / `StateHolder`
  / the flag word) is looked up, the second half (the stair placement) is
  watched. Session D grew both halves and did not split, because the
  fact-check's additions landed on both sides evenly and neither half
  became unwieldy. It is presentational and it is pass 3's call.

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

### Part IV *(session C)*

- **The two best diagrams in the part are the two the new page added**, and
  they are a matched pair: the same value resolved on the server (four
  layers, one clock) and on the client (the same four layers plus spatial
  and partial-tick smoothing). Pass 3 should keep them adjacent and
  consider drawing the *layer stack* itself as a small flowchart above
  them, because the stack is the one thing every reader needs and neither
  sequence diagram shows it as a stack.
- **`tickets-and-loading`'s diagram is the wrong shape.** It is a
  `sequenceDiagram`, but the thing being explained is two graphs relaxing
  and a state machine promoting through `FullChunkStatus`. The sequence
  version has eleven lanes and reads as a list. A flowchart of the ticket →
  level → status → future chain, plus a small state diagram for the three
  full statuses, would replace most of the numbered trace.
- **`chunk-generation-pipeline`'s diagram is the right shape and too
  small.** The pyramid — twelve statuses, a radius each, two variants — is
  the page's real subject and currently lives in a markdown table. It wants
  to be drawn.
- **`lighting` needs a diagram it does not have**: the four-stage batch
  (check nodes → decreases → increases → swap) is a pipeline, and the page
  explains it in prose while the diagram traces a torch. Both are worth
  having.

### Part V *(session D)*

- **The part needs one diagram it does not have: the two update
  channels.** Shape updates versus neighbour updates — who runs them,
  which side, in which of the two direction orders, and where
  `Block.updateOrDestroy` can turn one into the other — is the part's
  load-bearing idea and is currently prose spread over three pages. A
  single flowchart of `Level.setBlock`'s tail (dirty → flag 2 → flag 1 →
  the three shape passes → POI) would serve `blocks-and-states`,
  `block-interaction` and `redstone` at once, and is a better opening
  visual for the part than any of the sequence diagrams.
- **`block-breaking`'s diagram is the right shape.** Two clocks running
  independently with no packets between them is exactly what a sequence
  diagram with a `loop` block shows well, and the loop is the page's whole
  argument.
- **`redstone`'s diagram is the wrong shape for its first half.** Signal
  propagation through a wire network is a graph relaxing, not a sequence;
  the sequence version works only because the trace is a straight line of
  two dust. The piston half, by contrast, is genuinely sequential (queue,
  next tick, two ticks of motion) and should keep its lanes. Another
  argument for the split in section 2.
- **`block-entities`' diagram needed a `Note over` to carry a tick
  boundary** — session D found the page had the furnace's block update and
  its menu data both leaving in the same tick they were produced, when
  block entities tick *after* both the broadcast drain and the entity
  phase. Any diagram in this corpus that crosses a tick boundary should
  mark it; several probably do so silently.

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

### Lectures Part IV would give

*(session C)* Ordered as they should be watched, with the trace each one
follows:

1. **What a chunk is** — `chunk-anatomy`. Trace: one block placed, all the
   way down to the bit storage. Vocabulary page; everything later assumes
   it.
2. **How a chunk comes to exist** — `tickets-and-loading` +
   `chunk-generation-pipeline`. Two recordings or one long one; the seam is
   `scheduleChunkGenerationTask`. Trace: a player walks east.
3. **Light** — `lighting`. Trace: a torch is placed. Self-contained, and
   the only part of the pipeline with its own executor.
4. **How a chunk is saved and forgotten** — `chunk-storage`. Trace: the
   player walks back west.
5. **What the place and the hour decide** —
   `environment-attributes-and-timelines`. Trace: dusk falls. This is the
   part's best standalone lecture and the least like anything a viewer has
   seen before; it is also the one with a **forward** dependency from Part
   III (see section 5), so it may need to move earlier than its page order.
6. **Appointments** — the scheduler half of `block-ticks-and-fluids`.
7. **Fluids** — the other half. Trace: the bucket.
8. **Vibrations** — the sculk half of `game-events-and-poi`.
9. **Villagers and their beds** — the POI half.

`level-data-and-rules` is not on this list, deliberately. It is a look-up.

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
- **`environment-attributes-and-timelines` now exists, and it has six
  dependants across four parts** — `server-level-tick` (Part III),
  `block-ticks-and-fluids`, `game-events-and-poi`, `level-data-and-rules`
  (Part IV), `biomes` (worldgen) and `lightmap-fog-and-sky` (rendering).
  Session C cut the borrowed explanations out of `biomes` and
  `lightmap-fog-and-sky` and pointed them here. That makes it the single
  most-linked-to page written so far, and its own dependencies are tiny:
  it needs registries and codecs (Part II) and nothing else. **It could be
  watched anywhere from Part II onward, and the earliest position that is
  not absurd is probably best.** *(session C)*
- **Part IV's internal order is already a chain.** `chunk-anatomy` →
  `tickets-and-loading` → `chunk-generation-pipeline` → `lighting` →
  `chunk-storage` is a genuine forward-only dependency chain, the first
  one in the corpus. Nothing later in it can be watched first. That is
  worth exploiting in the lecture order rather than fighting. *(session C)*
- **`chunk-anatomy` → Part V.** `blocks-and-states` and `block-entities`
  both assume the section/palette model and the `setBlockState` flag
  vocabulary. Part IV must precede Part V. *(session C)*

- **Authority (`Entity.isLocalInstanceAuthoritative` and its three
  siblings) is now a three-page dependency in two parts** —
  `movement-and-collision`, `player-anatomy` and `input-to-movement` — and
  Part IX's `what-the-client-is-told` and Part X's client-tick material
  both lean on it too. It is the second-most duplicated idea in the corpus
  after the thread table. See the Part VIII note in section 1. *(session F)*
- **`items-and-stacks` → everything in Part VII, and out into Parts V and
  VIII.** Data components, the use pipeline and durability are assumed by
  `containers-and-menus`, `enchantments`, `block-interaction`,
  `block-breaking`, `the-sword-swing` and `hunger-xp-and-effects`. It is
  the part's root and should be watched first within it. *(session F)*
- **`loot-tables`'s context machinery is a dependency of Part XIII, not
  just of Part VII.** `/execute if predicate` and the entity-selector
  predicate argument both run on `ContextKeySet`; the advancement triggers
  use two parameter sets of their own. Whoever owns commands will have to
  either explain contexts again or point back into Part VII. *(session F)*
- **`containers-and-menus` → `recipes`.** The crafting result slot is
  pushed by a hand-written packet that bypasses the menu's own diffing and
  bumps the state id itself; the recipe page cannot explain that without
  the menu page's synchroniser model first. *(session F)*
- **`player-anatomy` → `hunger-xp-and-effects` is a *tick-phase*
  dependency, not a data one.** Every claim on the hunger page about when
  something reaches the client is a claim about which half of the player
  tick it ran in. *(session F)*

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
- Is there a **reference tier** in the systems tree, and if so which pages
  are in it? `math-and-primitives` and `level-data-and-rules` are both
  clear members; `naming-drift` and `glossary` already behave like one.
  *(session C)*
- Does `environment-attributes-and-timelines` move earlier than Part IV,
  given Part III already depends on it? *(session C)*
- Part IV's diagrams use `SL`, `CM`, `CH`, `TS`, `TD`, `LT`, `CT`, `FF`,
  `PM`, `EAS`, `VS`, `ATS` — mostly two- and three-letter, consistent with
  Part III. The new page uses `Probe` and `Cam` for `EnvironmentAttributeProbe`
  and `Camera`, which are words rather than initials; the standard should
  rule on whether a short word is allowed. *(session C)*
- Does the authority matrix live in `entity-anatomy`,
  `movement-and-collision` or `input-to-movement`? Sessions E and F
  disagree, and the answer depends on whether Part VI precedes Part VIII.
  *(session F)*
- Is `loot-tables` renamed, split, or left with a title that undersells it?
  *(session F)*
- Is the spear (`PiercingWeapon` / `KineticWeapon`) its own lecture, or two
  invariants on `the-sword-swing`? *(session F)*
- Does *drawing a bow* exist as a trace, given the release half of the use
  pipeline is currently one sentence? *(session F)*
- Part VII/VIII diagram lanes use `MC`, `MPGM`/`MG`, `SGPL`/`CL`, `SPGM`,
  `IS`, `C`/`CO`, `LE`, `SP`, `FD`, `SCR`, `CM`, `RS`, `SYNC`, `LP`, `KM`,
  `KI`, `PL`, `IN`, `GM`. Two collisions the standard must resolve:
  **`CL` and `SGPL` are both `ServerGamePacketListenerImpl`** within Part
  VIII, and `CM` is `AbstractContainerMenu` on one page and `CraftingMenu`
  on another. *(session F)*
