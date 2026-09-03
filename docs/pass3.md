# Pass 3 — the restructuring notebook

*Started 2026-09-01, at the beginning of pass-2 session A, as the file
where pass-2 sessions **wrote pass 3's inputs down as they found them** —
observations you can only make with the decompile open and the page in
front of you. **Pass 3 started on 2026-09-02.** Its charter, its eight
rulings (R1–R8) and its session schedule are in [plan.md](plan.md); this
file is the evidence those were made from, and it stays open: a pass-3
session that finds something structural for a* later *pass-3 session (a
cross-part consequence, a lane, a page that belongs elsewhere) appends it
here, and §7 — new — is the coverage queue ruling R7 refers to. Facts to
re-check go to [pass4.md](pass4.md); wording debt to [pass5.md](pass5.md).*

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

### Part IX · Networking

*(session G)* **The plan's sketch says Part IX is "two connected pipelines
meeting at the wire and should read like one". Session G's evidence is that
it is not two pipelines — it is one pipeline and three passengers, and the
pipeline is the smallest part of it.** `the-connection` and
`packets-and-stream-codecs` really are one subject read from two ends: a
byte becomes a frame becomes a packet becomes a handler call, and the only
reason they are two pages is that one of them is about threads and the
other about codecs. They share a trace, they cite each other eight times,
and every correction session G made to one had a counterpart in the other
(the skip machinery, the terminal flag, the singleplayer serialisation
cost, the frame ceilings). **Pass 3's strongest option for this part is to
teach them as one lecture in two halves with a single continuous trace**,
rather than as two pages each with its own diagram of the same journey.

The other three are not pipeline pages at all and should stop pretending.
`protocol-phases` is a **state machine**; `what-the-client-is-told` is a
**policy** (who is told what, and how often); `chat-and-signing` is a
**protocol with an adversary**. Three different shapes, three different
diagrams, and none of them is "follow a packet".

**Part IX has the corpus's worst ordering dependency, and it points
backwards.** Every one of these pages assumes the server tick's phase
order, and two of them assume the client's frame/tick interleave — which
lives in Part X. `what-the-client-is-told` cannot be understood without
knowing that broadcasts happen in the chunk-source phase, before entities
tick; `the-connection`'s two-flush invariant is a `MinecraftServer.tickChildren`
fact; and the whole "once per frame, not once per tick" correction is a
Part X fact stated in Part IX. **Part IX must follow Part III and at least
the client-tick half of Part X**, or those three facts have to be taught
here, badly, for the third time.

**One page is doing another part's job.** `what-the-client-is-told`'s
closing sections — *`ClientLevel` as a lossy copy*, the prediction ledger,
the client's own light — are Part X material that ended up here because
Part IX was written first. After the X/XI split (sessions H–I), pass 3
should decide whether this page keeps them or hands them over and links
back. Session G's guess is *hand them over*: the page is already 553 lines
and its subject is the **server's choosing**, not the client's coping.

---

---

### Part X · The client · and Part XI · Rendering

*(session H)* **The split landed, and the seam is sharper than the plan
assumed.** The plan's default allocation put `the-frame` in Part XI as its
opening trace. That was right for the *frame* and wrong for the *loop*:
`Minecraft.run` / `runTick` and `Minecraft.renderFrame` are two different
subjects that happened to live in one method chain, and once separated
(`the-client-loop` in X, `the-frame` in XI) almost every ordering
dependency in the corpus resolved. **Part IX's stated dependency — "the
client's frame/tick interleave has to be taught before
`what-the-client-is-told`" — is now a dependency on one short page, not on
the whole of Part X.** That is the most useful consequence of the split and
pass 3 should protect it: keep `the-client-loop` early and keep it short.

**Part X is not a pipeline and should not pretend to be.** It is a **hub
and five spokes**: the loop is the hub, and `the-client-level`,
`prediction-and-acks`, input/options, the GUI stack and sound all hang off
"when in the loop does this run". Every one of them is defined by its
cadence — per tick, per frame, per event, per packet — and that is the
through-line, not a hand-off order. The one genuine internal pipeline is
the GUI stack (`gui-and-screens` → `the-gui-render-tree` →
`text-and-fonts`), which *is* three stages of one journey and should be
taught consecutively.

**Part XI is a pipeline and already reads like one.** Frame → blaze3d →
level rendering → models → entities → lightmap/fog/sky → particles is close
to the order things happen in. Session I should check whether `blaze3d`
wants to be *second* or *last*: it is the substrate, so teaching it early
means teaching an abstraction before anything uses it, and teaching it last
means six pages of forward references. Session H has no evidence either
way, only the observation that every rendering page cites it.

**Two pages in Part X are not lectures about the client at all.**
`prediction-and-acks` is a *protocol* page that happens to live on the
client, and `text-and-fonts` is a *typesetting* page that happens to be
rendered by it. Both would sit equally well in Part IX and Part XI
respectively. They are in X because that is where their owning objects
live, which is a packaging argument — exactly the kind pass 3 is allowed to
overrule.

*(session I)* **Part XI is a pipeline for five of its pages and a substrate
for three, and the split is cleaner than "second or last".** Session H asked
whether `blaze3d` goes second or last. The fact-check answers a different
question instead: Part XI contains **two substrate pages and one genuine
pipeline**. `the-window` (new this session) and `blaze3d` are what the
renderer stands on — neither has a trace through the world, both are cited by
every other page — while `the-frame` → `level-rendering` → `models-and-atlases`
→ `entity-rendering` → `lightmap-fog-and-sky` → `particles` really is the
order things happen in. The lecture question is therefore not where `blaze3d`
goes but **whether the substrate is one lecture or two, and whether it opens
or closes the part**. Session I's own answer, weakly held: open with
`the-frame` (it is the part's trace and its shortest page), then the
substrate, then the pipeline — because a reader who has seen one frame
end-to-end has a reason to care what `GpuDevice` is.

**`the-window` is new, and it discharges session H's deferred ruling.**
Session H left "does `blaze3d/platform` get absorbed or a page?" to session I.
It is a page: 25 classes and ~3,800 lines that no page explained, and three
pages in two parts all began *after* it (`the-frame` starts at an acquired
surface, `input-and-keybinds` at a fired callback, `blaze3d` at a created
device). It is currently third in the part; whether it belongs first, third,
or beside `anatomy` in Part I is a pass-3 call, and it is the same question as
session H's open one about `the-client-loop`.

**Part XI has three more whole systems with no owner, all found by counting
rather than reading.** The session's inventory measured the tree at 1,187
classes / 97,864 lines and found 58% of it by line count named nowhere. Three
of the gaps are coherent systems rather than catalogues, and each is a
candidate page:
  - **Post-processing** — `PostChain`, `PostPass`, `PostChainConfig`,
    `UniformValue`, ~1,000 lines, named on no page. Data-driven GLSL chains
    loaded from JSON that add their own passes to the same `FrameGraphBuilder`
    `level-rendering` explains. It is the answer to "how do the spectator mob
    shaders and the menu blur work", and the only place user-authored shaders
    are first-class. Strongest single candidate.
  - **Block-entity rendering** — `renderer/blockentity` plus its 26 render
    states, ~3,300 lines, of which only the dispatcher is named. In 26.2 it
    has the *same* extract/submit split as entities, which no page says. The
    parallel to `entity-rendering` is exact, which argues for a page rather
    than a section. `renderer/special` (the item-side twin — why a chest in
    your hand looks right with an empty model) belongs with it.
  - **How an item picks its model** — `renderer/item` plus the 42 classes
    under `item/properties/**`, the whole successor to *ItemOverrides*. This
    one is arguably Part VII's, not Part XI's: the trace starts at an
    `ItemStack`. Decide the owner before writing it.

**Two diagram-shape notes.** `the-window`'s trace is a **retry loop** — the
backend loop encloses both window creation and device creation — and a
sequence diagram renders that as an awkward `loop` block; it wants a
flowchart. And `models-and-atlases`' trace is the corpus's clearest
**fan-out/barrier** shape (thirteen parallel stitches and a parallel bake
meeting at one barrier), which the `par`/`and` block understates.

**Lane abbreviations, Part XI.** `M`, `S` (`GpuSurface`), `GR`
(`GameRenderer`), `LR` (`LevelRenderer`), `GUI` (`GuiRenderer`), `D`, `CE`,
`RP`, `B` (`GlCommandEncoder`), `G` (game code), `MPGM`, `CL`, `LX`, `SUT`,
`SRD`, `W`, `SC`, `KH`, `AM`, `SL`, `MM`, `MB`, `TA`, `ERD`, `ZR`, `ZS`,
`SNS`, `FRD`, `ZM`, `TL`, `EAS`, `P`, `FR`, `SR`, `LM`, `PE`, `B` (`Block`),
`PL`, `CPL`, `GLX`, `MM` (`MonitorManager`), `RS`. **Three collisions inside
the part now**, worse than session H's two: `M` is `Minecraft` in four
diagrams and `ModelManager`'s neighbour `MM` collides with `MonitorManager`;
`B` is both `GlCommandEncoder` and `Block`; `LX` is `LevelExtractor` here and
`LightmapRenderStateExtractor` in `lightmap-fog-and-sky`'s own trace. The
last is the worst — same part, adjacent pages. Plus session H's standing
`GR` collision (`GuiRenderer` in X, `GameRenderer` in XI) is now live in
both parts at once.

### Part XII · World generation

*(session J)* **The part is a pipeline with a substrate underneath it, and
the current page order half-admits it.** `density-functions` is not step
two of anything — it is the *material* every other page is made of, the way
`blaze3d` is for Part XI. The genuine sequence is
biomes → noise/surface/carvers → structures → features, which is chunk
status order, and the part already has a page per stage. Two consequences
for pass 3:

- **`density-functions` should open the part or close it, not sit second.**
  Session I settled the same question for `blaze3d` by observing that a
  substrate page read *before* the pipeline teaches vocabulary with no
  motivation, and read *after* it explains machinery the reader has already
  formed a wrong model of. Part XII has it worse than Part XI, because the
  density graph is genuinely prerequisite: `worldgen-pipeline`'s aquifer,
  ore veins and beardifier are all density terms, and `biomes` cannot
  explain the climate sampler without it. **Recommendation: open with it**,
  and accept that the first lecture is the abstract one. The counter-case
  is that "the seed" is the best hook in the part and it is in that page.
- **The through-line to protect is the chunk status ladder**, which is
  owned by Part IV's `chunk-generation-pipeline`. Part XII is the cargo of
  four statuses and Part IV is the conveyor. That split is right, but it
  means **Part XII cannot be lectured before Part IV's pipeline page**, and
  the dependency should be stated in the lecture order rather than
  rediscovered.

**The split candidates both survive, and one of them grew a third page.**

- **`structures` is now three subjects, not two.** The pass-2 table
  proposed placement-decision vs jigsaw-assembly, and that seam is real and
  clean. Session J's inventory found a third: the **hand-built piece-graph
  assembler** (`levelgen/structure/structures`, 30 classes / 10,012 lines,
  98% of it named nowhere in the corpus), which fifteen of the sixteen
  structure types still use and which is a genuinely different mechanism
  from jigsaw — recursive `StructurePiece.addChildren` growth with
  collision against the pieces placed so far, rather than pool draws
  against a free-space shape. Session J wrote it as its own page; pass 3
  should decide whether the *remaining* placement/jigsaw seam is also worth
  cutting, and if so the part is five pages of worldgen plus three of
  structures, which is probably one part too many and argues for a
  **Part XII-A / XII-B** shape or for promoting structures to its own part.
- **`density-functions`' own split** (node catalogue vs the two rewrites)
  is still presentational and still correct. The rewrite story is the
  lecture; the node families are reference. Session J grew the rewrite half
  and left the catalogue alone, so the imbalance is now more obvious, not
  less.

**Diagram shape.** Two of the five traces are the wrong shape:

- `worldgen-pipeline`'s sequence diagram is really a **pipeline with a
  nested loop**, and mermaid renders the cell walk as four indistinguishable
  self-calls on one lane. The interesting structure — cell corners
  interpolated, blocks filled inside the cell, two filler passes per block
  — is a diagram about *nesting depth*, not about message order. A flowchart
  or a simple annotated figure would teach it better.
- `density-functions`' trace is **three graphs and two rewrites**, which a
  sequence diagram cannot show at all: the whole point is that the same
  tree exists in three forms. This wants a before/after tree figure, and it
  is the strongest candidate in the corpus for the "static image" question
  the diagram plan defers.
- `biomes`' trace is fine and is the part's best diagram, because the
  generation path and the two read paths genuinely are three sequences.

**Lane abbreviations, for the corpus-wide decision.** Part XII currently
uses `CST` (`ChunkStatusTasks`), `NBC`/`CG` (both for chunk generators —
`CG` is `ChunkGenerator` in `structures` and `NoiseBasedChunkGenerator` in
`biomes`, **a collision inside the part**), `NC`, `MRL`, `AQ`, `OV`, `SS`
(`SurfaceSystem` in one page, `StructureStart` in another — **a second
collision**), `WC`, `PC`, `MN`, `CS`, `RT`, `BM`, `EAS`, `FS`, `WR`, `PF`,
`PM`, `CF`, `TF`, `TP` (`TrunkPlacer`/`FoliagePlacer` in one page,
`StructureTemplate` in another — **a third**), `ST`, `SP`, `JS`, `JP`,
`SM`, `BD`. Three internal collisions, same as Part XI. `SS` and `TP` are
the ones that will actually mislead.

### Part XIII · Commands and data packs

*(session K)* **The part is a stack, and its current order reads as a list.**
The four pages are not four peers: `brigadier-and-commands` is the parser and
the permission model, `execution-and-functions` is the engine that runs what
the parser produced, and the other two are *consumers* of both. The dependency
is strictly one-directional — nothing in advancements or dialogs is needed to
understand the engine, and both need it — so the part is
**parse → execute → what commands are used for**, which is what the page order
already is by accident. Pass 3 should make it deliberate and say so at the top
of each page, because a viewer arriving at `advancements` has no way to know
it is the third floor of a building.

Four structural observations:

- **`brigadier-and-commands` is now the largest page in the part and carries
  four subjects**: the parse (client and server), the permission model, the
  argument-type catalogue, and the wire form of the tree. Session K added two
  more sections to it — the arguments that resolve against the source
  (coordinates, selectors, function ids) and the packrat grammar — because
  each answers a question the page already raised. That is four sessions of
  "confirmed overloaded, not split". The seam that has held up best is
  **the permission model**: it is a lecture with its own trace (a click-event
  command being confirmed), it is the single biggest API break in the corpus,
  and it is currently a section inside a page whose trace is `/give`. If
  Part XIII splits one page, that is the one.
- **`execution-and-functions` splits cleanly and the split has got cleaner.**
  The engine half (queue, `Frame`, discards, `/return`, the two failure paths)
  and the function half (compile, macros, tags, `/schedule`) share exactly one
  class, and session K's additions all landed on the engine side. The second
  half is the one data-pack authors want and it is now the shorter of the two.
- **Advancements is two lectures and the second one is a screen.** The server
  half is a subscription system; the client half is a tree the server laid out
  and a tab strip with a hard cap of twenty-six. Session K absorbed the client
  half as a section rather than a page, but it is the most *watchable* material
  in the part — the one place a viewer sees a data structure they already know
  from playing.
- **`dialogs-and-tests` is two pages held together by an argument, not a
  system.** The argument ("this is the registry-element pattern, twice") is a
  good one and the corpus makes it nowhere else at this altitude. Pass 3's
  choice is between promoting that argument to a Part II page about the pattern
  itself — with dialogs and tests as its two examples, which would also serve
  loot tables, features and density functions — and splitting the page in two
  and losing it. The first is better and is a bigger change than it looks.

**A fifth page arrived in this pass:** `scoreboard-and-data`, covering the
scoreboard, teams, command storage, NBT paths and `execute store`. It is here
because its trace is a command, but two of its four subjects are not command
subjects at all — `PlayerTeam` is read by collision and by nametag rendering,
and the scoreboard is per-world saved data with four packets of its own. Pass 3
has a genuine placement question: **does the scoreboard belong to Part XIII,
to Part IV (it is level state), or to a part of its own with the boss bar and
the statistics?** The `execute store` seam argues for XIII; everything else
argues against.

### Part XIV · Appendix

*(session K)* **The appendix behaves like a reference tier and should be named
one.** All three pages have "No trace" in their header, none follows the
template, and two of them (`naming-drift`, `glossary`) are lookup tables that
a viewer would never watch and a reader would use constantly. Session C
already asked whether a reference tier exists; the appendix answers yes, and
`math-and-primitives`, `level-data-and-rules` and the generated
`src/reference/` pages are its other members. Two consequences:

- **The appendix is not a part, it is the end of the book.** Numbering it XIV
  puts it in the lecture sequence, which it can never be. Pass 3 should decide
  whether the numbered parts stop at XIII and the appendix sits outside them.
- **`out-of-scope-tour` is the one appendix page that *is* a lecture** — "here
  is everything in the jar that this series will not teach you, and why" is a
  real fifteen minutes, and it is the natural *first* or *last* video rather
  than an appendix entry. Its gaps list, now a ruling list, is also the only
  place the corpus states its own boundary.
- **The glossary should be regenerated, not maintained.** It drifted badly:
  session K found five stale entries describing designs 26.2 no longer has
  (the permission integer chief among them) and fifteen missing terms, all of
  them from pages written after it. A term is owned by exactly one page; if
  each page declared its terms, the glossary would be a build artefact like
  `class-index`. That is a tools decision, not a prose one, and it belongs to
  pass 3 or 4.

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

- **`sound` is now the odd page out in Part X.** *(session H)* Session A
  found it was two pages' worth of material and did not split it; after
  session H, every other page in the part is one cadence and one subject,
  and `sound` is the only one still carrying an engine and a content model.
  The split session A described (engine · what makes a sound happen) is now
  the *consistent* choice rather than a nicety.
- **`the-client-loop` and `the-frame` must not both grow a "when it runs"
  section.** *(session H)* They are one method chain split in two, and the
  temptation on both sides is to restate the other's half for context. The
  rule that worked while writing them: X stops at the profiler's *frame*
  zone, XI starts at the surface acquisition, and each links once.
- **`the-gui-render-tree` is the best candidate in the corpus for a
  non-sequence diagram.** *(session H)* Its subject is a *tree with a
  placement rule*; the page currently uses a sequence diagram with an
  alternative block for the fast path, which is a flowchart wearing a
  sequence diagram's clothes. Draw the strata and node structure and the
  "above the highest box I intersect" rule as a diagram of the data, not of
  time.
- **`hud` wants a table, not prose, for its record order.** *(session H)*
  The fact-check produced a per-element gate table of twenty-eight rows and
  the page had to compress it to prose to stay readable. The table is the
  honest artefact, and pass 3 should decide whether the corpus admits a
  reference-tier table inside a lecture page.
- **`prediction-and-acks` closed a four-way duplication.** *(session H)*
  The ledger was described in `client-world-and-options`, `block-breaking`,
  `block-interaction` and `what-the-client-is-told`, and the four
  disagreed. It now has one owner and the others link to it. Pass 3 should
  look for the same pattern elsewhere: **the corpus's duplications are
  where its errors were.**

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

### Part IX *(session G)*

- **The two "follow a packet" diagrams are the same diagram drawn from
  opposite ends,** and both are the right shape. `the-connection` traces
  bytes → handler with lanes for the pipeline handlers;
  `packets-and-stream-codecs` traces value → bytes → value with lanes for
  the codecs. If the two pages merge (section 1), they merge into **one
  round-trip diagram**, which is strictly better than either: the thread
  hop and the codec layer are the two things a viewer wants to see happen
  in the same picture.
- **`protocol-phases`' diagram is a sequence diagram of a state machine,
  and it fought the correction session G made to it.** The login has three
  threads, four phases, and a step whose whole point is that it happens
  *later than you think* — the player is built after the client's finish
  packet, two arrows below where the old diagram put it. A sequence
  diagram can show that, but the phase boundaries are invisible in it.
  The honest shape is a **state diagram with the packets as transitions**,
  possibly beside a smaller sequence diagram for the encryption handshake
  alone. At minimum the phase changes need `Note over` bars — this is the
  page where a silent tick-style boundary does the most damage.
- **`what-the-client-is-told` wants a decision table, not a sequence.**
  Its best artefact is already a table (position sync: condition →
  packet), and its worst passage is the one the creeper trace has to carry
  — three gates to reach the change detector, three more inside it. Draw
  that as a **flowchart of one entity's tick**, and let the sequence
  diagram keep only the part it is good at: the pairing bundle.
- **`chat-and-signing` has the corpus's only diagram with an adversary in
  it, and does not show them.** The interesting picture is not the happy
  path (typed → signed → broadcast → displayed, which the sequence diagram
  does fine) but **what each check would catch**: which failures kill the
  message, which kill the chain, and which kill the connection. That is a
  three-column table or an annotated flow, and it is the lecture.
- **Lane abbreviations, for the standard in this file above:** Part IX
  uses `CN` for `Connection`, `PP` for `PacketProcessor`, `PD`/`PE` for
  the decoder/encoder, `SGPL`/`CPL` for the two play listeners, and
  `SL`/`SH`/`SC`/`CC`/`CH` across the login trace. `PE` collides with
  Part X's `ParticleEngine`. Session G kept `SGPL`/`CPL`, which is what
  the carried-over item recommends settling on.

---

### Parts X and XI *(session H)*

Part X's new pages use `M` (`Minecraft`), `DT` (`DeltaTracker.Timer`), `PP`
(`PacketProcessor`), `T` (`Minecraft.tick`), `FL` (`FramerateLimiter`),
`CPL`, `CCC` (`ClientChunkCache`), `CL` (`ClientLevel`), `LLE`
(`LevelLightEngine`), `LX` (`LevelExtractor`), `MPGM`, `BSPH`
(`BlockStatePredictionHandler`), `SGPL`, `SPGM`, `KH` (`KeyboardHandler`),
`KM` (`KeyMapping`), `MH` (`MouseHandler`), `G` (`Gui`), `H` (`Hud`),
`GGE`, `GRS`, `GR` (`GuiRenderer`), and `S`/`O`/`SP`/`CM` in the options
trace. **Two collisions the standard must resolve:** `CL` is `ClientLevel`
here and `ServerGamePacketListenerImpl` in Part VIII; `GR` is `GuiRenderer`
here and `GameRenderer` in Part XI. Both are worse than the Part VII/VIII
collisions session F found, because they are between *neighbouring* parts.

Three diagram-shape notes:

- **`the-client-loop`'s trace is a loop, and a sequence diagram cannot say
  so.** The bounded tick block carries the page's most important fact —
  ticks are dropped — in a label. It wants a flowchart with a decision, or
  a timeline.
- **`options`'s trace ends at the server with no return arrow,
  deliberately.** The old version of this diagram had two fabricated return
  arrows; the absence is now the point, and a reader will read a missing
  arrow as an omission unless the diagram says otherwise. Worth an explicit
  "no reply" annotation convention.
- **`prediction-and-acks` is the corpus's clearest candidate for a
  two-column state diagram** — client ledger state against server counter
  state — rather than a sequence.

### Parts XIII and XIV *(session K)*

Part XIII's lanes are the most consistent in the corpus and confirm the
`SGPL`/`CPL` majority: `CS` (`CommandSuggestions`), `CSP`
(`ClientSuggestionProvider`), `CPL`, `SGPL`, `C` (`Commands`), `EC`
(`ExecutionContext`), `CF`, `BC`, `CT`, `XC`, `SFM`, `PA`
(`PlayerAdvancements`), `CA` (`ClientAdvancements`), `M`
(`AbstractContainerMenu`), `SP`, `T`, `R`, `RDL`, `DC`, `CCPL`, `DS`, `MS`,
`TC`, `GR`, `TIB`, `GT`, `GI`, `RL`. One internal collision worth noting:
**`C` is `Commands` here and `Container` in Part VII**, and **`GR` is
`GameTestRunner` here and `GameRenderer` in Parts X and XI** — the second is
the same clash session I flagged, now with a third claimant.

Two diagram-shape notes:

- `brigadier-and-commands`'s trace is a sequence diagram and should probably
  stay one, but the *permission model* section wants a small state or
  containment diagram (a `PermissionSet` is a union of atoms and a level, and
  the prose spends four bullets saying so).
- `execution-and-functions`'s trace is the one diagram in the corpus that is
  really about a **data structure over time** — the queue, with entries being
  spliced onto and off the head. A sequence diagram cannot show that, and it
  is why the page needs five hundred words of prose after the diagram to
  explain the staging buffer. This is the strongest candidate in the corpus for
  a non-sequence, non-flowchart visual: three or four snapshots of the queue.
  Worth deciding deliberately, because it is also the page where a wrong
  mental model is most expensive.
- The appendix has no diagrams and wants none, except possibly one: a treemap
  or bar of the jar by package, in `out-of-scope-tour`, where the size table
  currently does that job in fifteen rows of numbers.

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
- **Part IX depends on Part III's tick order and Part X's frame order,
  in both directions** *(session G)*. Three separate Part IX claims are
  really facts about somebody else's loop: the broadcast happens in the
  chunk-source phase (Part III), the second flush carries what
  `MinecraftServer.tickChildren` does after ticking connections (Part
  III), and the client applies packets once per frame before that frame's
  ticks (Part X). Part IX currently restates all three. Whatever order
  pass 3 picks, **the client's frame/tick interleave has to be taught
  before `what-the-client-is-told`**, or that page teaches it a second
  time and gets it wrong again — it already did once.
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

- **The client loop is now a prerequisite of three parts, and it is
  cheap.** *(session H)* Part III wants it for the tick contrast, Part IX
  needs the per-frame packet drain, and all of Parts X and XI assume the
  cadence. It is the smallest page with the widest fan-in in the corpus
  after the thread table — which argues for teaching it very early, perhaps
  even beside `anatomy` in Part I rather than at the head of Part X.
- **`prediction-and-acks` → Part V, both ways.** *(session H)*
  `block-breaking` and `block-interaction` are its applications and cannot
  be taught without it; it in turn is unreadable without Part V's notion of
  a block update. Whichever comes first has to forward-reference the other,
  and pass 3 should pick deliberately rather than by part number.
- **`text-and-fonts` → `chat-and-signing` (Part IX).** *(session H)* The
  text page starts from "you have a `Component`", and what a `Component` is
  lives in Part IX. That is a backwards dependency across five parts, and
  it is the strongest argument in the corpus for a `Component` page in Part
  II — the object is a foundation, not a networking detail.
- **`the-gui-render-tree` → `blaze3d` (Part XI).** *(session H)* The GUI
  page explains batching and pipelines a whole part before the pipeline
  page exists.

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
- ~~Does the authority matrix live in `entity-anatomy`,
  `movement-and-collision` or `input-to-movement`?~~ **None of the three**:
  session G gave it `entities/authority.md`, and session I deleted the last
  two copies, from `input-to-movement` and `player-anatomy`.
  *(session F, answered sessions G and I)*
- ~~Is `loot-tables` renamed, split, or left with a title that undersells
  it?~~ **Split** by session H: `contexts-and-predicates` takes the engine,
  `loot-tables` keeps the pools, the entries and the chest as its worked
  example. *(session F, answered session H)*
- ~~Is the spear (`PiercingWeapon` / `KineticWeapon`) its own lecture, or two
  invariants on `the-sword-swing`?~~ **Its own lecture**, and the strongest
  in Part VIII. *(session F, answered session I)*
- ~~Does *drawing a bow* exist as a trace?~~ **Yes**, as the second half of
  `using-an-item`, opposite the meal. *(session F, answered session H)*
- Part VII/VIII diagram lanes use `MC`, `MPGM`/`MG`, `SGPL`/`CL`, `SPGM`,
  `IS`, `C`/`CO`, `LE`, `SP`, `FD`, `SCR`, `CM`, `RS`, `SYNC`, `LP`, `KM`,
  `KI`, `PL`, `IN`, `GM`. Two collisions the standard must resolve:
  **`CL` and `SGPL` are both `ServerGamePacketListenerImpl`** within Part
  VIII, and `CM` is `AbstractContainerMenu` on one page and `CraftingMenu`
  on another. *(session F)*
- Does `the-client-loop` belong in Part I beside `anatomy`, given three
  parts depend on it and it is two hundred lines? *(session H)*
- Does `prediction-and-acks` belong in Part IX rather than Part X? It is a
  protocol, and its two applications are in Part V. *(session H)*
- Is there a `Component` page in Part II, so that `text-and-fonts` and
  `chat-and-signing` stop sharing a subject? *(session H)*
- Where does the debug subscription system live — Part IX (it is a server
  push), Part X (the client draws it), or a part of its own? It is the only
  system in the corpus whose two halves are in different parts by nature.
  *(session H)*
- `blaze3d` second or last within Part XI? *(session H)*
- Does the corpus admit a reference-tier **table inside** a lecture page —
  `hud`'s gate table, `the-client-loop`'s zone list? *(session H)*
- Does `the-window` open Part XI, sit third as it does now, or move to Part I
  beside `anatomy`? Same question as `the-client-loop`'s, and they may want
  the same answer. *(session I)*
- Is the Part XI substrate (`the-window` + `blaze3d`) one lecture or two?
  *(session I)*
- Does post-processing get its own page, or a section of `the-frame`? It is
  ~1,000 lines with a JSON format and no owner. *(session I)*
- Who owns "how an item picks its model" — Part VII, whose `ItemStack` starts
  the trace, or Part XI, where the resolution happens? *(session I)*
- Does block-entity rendering get a page beside `entity-rendering`, given the
  two now share one extract/submit machine? *(session I)*
- `LX` means two different extractors on adjacent pages of Part XI, and `GR`
  means two different renderers across Parts X and XI. The lane standard has
  to break at least one of them. *(session I)*
- Does the **permission model** become its own page? It is the biggest API
  break in the corpus, it has a trace of its own, and it is currently a
  section. *(session K, agreeing with session 12)*
- Does the **registry-element pattern** become a Part II page, with dialogs,
  tests, loot tables, features and density functions as its examples? If yes,
  `dialogs-and-tests` can split without losing its argument. *(session K)*
- Who owns the **scoreboard** — Part XIII (its trace is a command), Part IV
  (it is per-world saved data), or a new part with boss bars and statistics?
  *(session K)*
- Does the **appendix stay numbered as a part**, or move outside the numbered
  sequence as the book's back matter? *(session K)*
- Should the **glossary be generated** from per-page term declarations rather
  than maintained by hand? It drifted by five wrong entries and fifteen
  missing ones in one pass. *(session K)*
- Is `out-of-scope-tour` the **first** lecture or the last? It is the only page
  that states the series' boundary, and it works as either an opening
  ("here is the shape of the thing, and here is what we are skipping") or a
  closing. *(session K)*
- `GR` now means `GameTestRunner`, `GameRenderer` and `GpuDevice`-adjacent
  things across three parts. *(session K, extending session I)*

## 7 · The coverage queue

*Systems the pass-2 inventories found with no owner. Ruling R7 in
[plan.md](plan.md) lets each part session write at most one of these; the
rest wait here, and session P discharges what budget allows. A session that
writes one strikes it through; a session that rules one out says why, here.*

- ~~**Post-processing**~~ — **written by session L** as
  `src/systems/rendering/post-processing.md`, the part's closer and its R7
  spend: 996 lines in four classes, six shipped chains, written against the
  JSON in `reference/26.2/assets/` that the planning session staged.
  *(session I, discharged session L)*
- **Block-entity rendering** — `renderer/blockentity` with its 26 render
  states, plus `renderer/special`, ~3,300 lines; the same extract/submit
  split as entities, which no page says. Part XI. *(session I)*
- ~~**How an item picks its model**~~ — **ruled and written by session L as a
  named section of `models-and-atlases`**, not a page: *How an item picks its
  model*, which Part VII's two forward links now land on by anchor. A page
  would have spent the part's R7 allowance on the weaker of two candidates,
  and the section's own material — the component *is* the decision, eight
  kinds of unbaked item model of which one draws anything, and the
  single-atlas rule that throws — sits naturally under the bake pipeline that
  produced it. The tree is 63 classes, not the 42 the entry estimated.
  *(session I, ruled session H, discharged session L)*
- ~~**How a server dies**~~ — **written by session D** as
  `src/systems/server/how-a-server-dies.md`, a comparison page with the
  three endings as columns and the watchdog's self-deadlock drawn.
  *(session B, discharged session D)*
- ~~**The spear**~~ — **written by session I** as
  `src/systems/player/the-spear.md`, a comparison page: two components on one
  item, a stab whose packet carries no target and a charge whose damage is
  closing speed. Writing it found the hook the queue entry could not:
  `Player.stabAttack` skips both cooldown curves while the player is using an
  item in that slot, so a charging spear ignores the attack cooldown.
  *(session F, discharged session I)*
- ~~**Drawing a bow**~~ — **written by session H** as the second half of
  `src/systems/items/using-an-item.md`, the split of `items-and-stacks`'s
  use pipeline: the meal and the bow as one machine read two ways. Writing
  it settled what the queue entry could not: the release branch is not
  selected by `ItemStack.useOnRelease` at all — only `CrossbowItem`
  overrides it. *(session F, discharged session H)*
- ~~**Status effects**~~ — **written by session I** as
  `src/systems/player/status-effects.md`, the split of `hunger-xp-and-effects`;
  the remainder is `hunger-and-experience` (renamed, redirected).
  *(session F, discharged session I)*
- **The permission model** — `PermissionSet`, `Permission`,
  `PermissionCheck`, `LevelBasedPermissionSet`; the biggest API break in the
  corpus, a section today. Part XIII, as a split. *(sessions 12, K)*
- **The function model** — compile, macros, tags, `/schedule`. Part XIII, as
  the other half of `execution-and-functions`. *(session K)*
- **Writing a game test** — `GameTestHelper`, 1,353 lines and one bullet.
  Part XIII. *(session K)*
- **The entity selector grammar** — six classes, ~2,136 lines, a section
  today and the most-asked question in the part. Part XIII. *(session K)*
- **The tree kit** — the `TrunkPlacer` / `FoliagePlacer` implementations,
  3,219 lines, probably the most watchable page in Part XII. *(session J)*
- **`Blender` / `BlendingData`** — named in five pages, explained in none,
  858 lines. Part XII. *(session J)*
- **World creation and the world-select screens** — ~5,100 lines spanning
  Parts X and XII. *(session J)*
- ~~**The non-living `Entity.hurtServer` overrides**~~ — **discharged by
  session G** as the closing section of `damage-and-death` (five families)
  plus the per-class table in `src/reference/non-living-damage.md`, which is
  the "Reference table" option this entry offered. The count was wrong: it
  is **21** non-living classes, not ~30, and `Entity.hurtServer` is
  *abstract*, so there is no default behaviour anywhere in the tree.
  *(session E, discharged session G)*
- **Commands that are algorithms** — `SpreadPlayersCommand`,
  `CloneCommands`, `ChaseCommand` (a debug socket protocol between two game
  instances). Part XIII, or Reference. *(session K)*
- **The predicate catalogue and the boss bar** — 54 predicate files; the
  boss bar is `execute store`'s third sink and belongs with
  `scoreboard-and-data`. Parts VII and XIII. *(session K)*

---

## 8 · Notes from pass-3 sessions for later pass-3 sessions

*(appended by the pass-3 sessions themselves; structural only)*

- **Session A (the frame).** The lane key is seeded in `TEMPLATE.md` (45
  class lanes, 6 word lanes) and `tools/check_lanes.py` reports 41
  participants disagreeing with it and 49 unkeyed lanes colliding across
  the unconverted pages; each part session runs `python tools/check_lanes.py
  --strict --pages src/systems/<part>` before shipping and adds its rows to
  the key. Rows deliberately left open: `SS`, `ST`, `TP`, `LX`, `PE`, `C`,
  `SE`, `SM`, `SC`, `T`, `W`. The introduction names two figures it does
  not draw — the two-jars treemap (session B) and the parts-dependency
  figure (session P) — and links `out-of-scope-tour`, `naming-drift` and
  `glossary` at their **appendix** paths; sessions C and O must update the
  introduction, `systems/anatomy/README.md` and `lectures.md` when those
  pages move. Part I's landing page lists *what this book skips* as its
  second lecture already, marked as arriving in session C. Two of the eight
  shapes are now exemplified (policy, state machine); the trace shape has
  no pilot yet and session C's first trace page should be written against
  the menu with care, since it is the shape most likely to reproduce the
  old template. `check_mermaid.js` now maps a part's `index.html` to
  `README.md`.

- **Session B (maps: the atlas).** **The figure pipeline exists**:
  `src/generated/` holds everything a tool writes (never hand-edited,
  regenerated by `deploy.sh`), a page includes an SVG inside
  `<figure class="map">` (the recipe is in `TEMPLATE.md` § Figures), the
  SVG carries classes only and `custom.css` themes them, `llms_full.py`
  expands markdown includes and notes SVG ones. `tools/map_source.py` is
  the worked example — `svg_open`/`write`/`esc`/`text_w` are reusable
  helpers, `squarify`, `svg_bars` and `svg_tree` are forty-line shapes.
  **For session C:** *what this book skips* should include the treemap
  (`{{#include ../../generated/packages-treemap.svg}}`) — its hatching is
  the tool's `SKIPPED` list, which was taken from the tour's size table
  plus `net/minecraft/realms`, with gametest left unhatched because Part
  XIII covers it; keep the two in step. The introduction now carries the
  treemap; only the parts-dependency figure (session P) is still a
  placeholder. **For session M:** the density-functions three-graphs
  figure is a generated-SVG candidate through this pipeline (a graph, not
  a tree — `svg_tree` will not do it as is). **For session O:** the
  serializer and attribute catalogues can be generated the same way the
  atlas tables are (a `.md` fragment under `src/generated/`, included by a
  hand-written page), which keeps prose and generated rows apart;
  `verify_names.py` now checks `maps/` prose and skips `generated/`, so a
  generated fragment with unverifiable names costs nothing. **Numbers
  moved:** the old hierarchy view could not see nested classes or records;
  one system page quoted a count (`entity-anatomy`'s 188 descendants of `Entity`, now 193 — corrected in place and listed for pass 4), and `reference/packets.md`'s
  count and the atlas's 227 direct `Packet` implementers are different
  things (types versus classes) and pass 4 should say which is which.
  **Sidebar titles** for the maps changed; file names and URLs did not.

- **Session C (Part I Anatomy · Part II Foundations).** **The appendix is
  gone**: `naming-drift` and `glossary` are in `src/reference/` with
  redirects, headers corrected, otherwise untouched — session O reframes
  them (the glossary's link targets now point at `../systems/…`, checked).
  `math-and-primitives` is at `src/reference/math-and-primitives.md`; its
  coordinate-spaces figure (the §3 note) is session O's. **The two-loops
  figure exists** in `anatomy` (*Two loops, and a wire between them*) —
  sessions D, J and K link to it instead of restating the frame/tick
  interleave and the per-frame packet drain. **Two Part I invariants
  belong to Part III and are still on `anatomy`**: the `haveTime` "gates
  exactly three things" claim and the sprint-polls-chunk-sources
  conclusion; `server-tick` has the pieces but not the framing. Session D
  moves both and cuts them here to a link. **Part II is seven pages**, a
  stack: codecs → registries → resources → tags → components → text
  components → the data-driven type pattern; the landing page draws it.
  **`text-components` exists** (R6): `text-and-fonts` and
  `chat-and-signing` point at it, and `chat-and-signing`'s `Component`
  section is a pointer paragraph — session J reshapes that page knowing
  the subject is gone. **`data-driven-types` exists** (R6) with a
  fifty-six-row instance table whose *taught in* column assumes the parts
  cover those instances: loot (H), features, density functions, structures
  (M), enchantments and recipes (H), spawn conditions (G), dialogs and
  tests (N), advancements and permissions (N). `dialogs-and-tests` keeps
  its own *The pattern, stated once* until session N links here and
  decides the split R6 allows. **Seven of the eight shapes now have a
  worked example**: the trace (`identifiers-and-registries`, `tags`), the
  comparison (`codecs-nbt-json`), the pipeline (`resource-system`), the
  vocabulary page (`data-components`, `text-components`), the pattern
  (`data-driven-types`), plus session A's policy and state machine;
  `what-this-book-skips` is a map page outside the menu (figure, then a
  tour by package) and `TEMPLATE.md` may want to name that shape.
  **Lanes**: fifty-two rows added to the key; `CT` is `CombatTracker`
  (matching `damage-and-death`), so `execution-and-functions`'
  `ContinuationTask` and `block-ticks-and-fluids`' `LevelChunkTicks`
  lengthen when sessions N and E convert; `PE` and `TP` are still open
  (this session took `PEnc` and `TagP`). **Three enchanting facts** moved
  out of `data-components` are not yet on `enchantments` (pass5.md) —
  session H absorbs them. **The treemap's hatching** (session O or P):
  `svg_treemap` hatches leaf cells only, and a depth-3 package with no
  sub-packages and fewer lines than the title strip (`gizmos` at 569,
  `realms` at 203) draws no leaf and so no hatch; the figcaption on
  `what-this-book-skips` says "hatched boxes" and two are not.
  `client/multiplayer/chat/report` is depth 5 and can never be hatched as
  drawn. `blaze3d/audio` was added to `SKIPPED` this session. **The
  drafting protocol that worked**: one shared brief file in the
  scratchpad, one agent per page with the ruling in its prompt, a report
  in six fixed sections (figures, claims introduced, claims reworded, cut
  or moved, new lanes, check output); the session reads the page and
  spot-checks two or three of the report's sharpest claims in the
  decompile. Nine drafts, none rejected, two pass-2 errors caught by
  agents (the axe and the logs tag; `NoiseRouterData` and the datagen
  bootstrap). The first three agents were lost to an interrupt and
  relaunched on Opus; their reports were as usable as the six on the
  session's own model, which is the evidence for running the part sessions
  on Opus from here.

- **Session D (Part III The server).** **Part III is five pages**, not four:
  `server-lifecycle` split into `starting-a-server.md` (redirect from the old
  URL) and the new `how-a-server-dies.md`, which spends R7's one-page
  allowance on the coverage queue's *how a server dies*. §7's entry for it is
  discharged; strike it. The part's shape is **a line into a loop and out
  again** and the landing page draws it. **The event-loop section now exists
  and has an owner** (R6): `server-tick`'s *The event loop, and what a tick's
  spare time buys*, with a flowchart of `pollTask` → `shouldRun` →
  `haveTime` and the `managedBlock` suspension. Sessions E, J and K should
  link to it rather than re-explain `BlockableEventLoop`,
  `MinecraftServer.managedBlock` or `TickTask`; the one-sentence uses already
  in `the-client-loop`, `resource-system`, `chunk-generation-pipeline` and
  `tickets-and-loading` are fine as they stand and only want a link.
  **`anatomy`'s two Part III invariants are moved and cut to a pointer**, so
  §8's session-C hand-off on that is discharged too. **Lanes**: thirteen rows
  added (`PP`, `TRM`, `LTs`, `EAS`, `NS`, `ETL`, `WB`, `PDS`, `SW`, `LSA`,
  `SC`, `DL`, `WS`) plus the word lanes `JVM` and `Hook`;
  `ServerGamePacketListenerImpl` is `SGPL` everywhere now, settling the
  notebook's odd-one-out `G`. **`LT` was already `LootTable`** (session C),
  so `LevelTicks` took `LTs` — the first time the lengthen-the-later-claimant
  rule has bitten, and worth expecting again in Parts IV and V, which both
  want `LT`. `check_lanes --strict --pages src/systems/server` is clean.
  **For session E (Part IV)**: `server-level-tick` now opens by defining
  entity-ticking, block-ticking and loaded in two sentences with the two
  `ChunkLevel` numbers, so Part IV no longer has to precede Part III — but
  Part IV owns the real explanation and the two must agree, so re-read that
  opener when `tickets-and-loading` is re-checked. Session D also found that
  a **debug world drops the block-change broadcast** (the `Level.isDebug`
  guard wraps all of `ServerChunkCache.tickChunks`), which no Part IV page
  says either. And `lighting.md` is now the sole owner of
  `ServerChunkCache.onLightUpdate`'s off-thread hop.
  **For session I (Part VIII)** and **session N (Part XIII)**: two link
  labels elsewhere in the corpus point at Part III pages under the wrong
  name — `player-anatomy.md` calls `server-tick.md` "the connection", and
  `scoreboard-and-data.md` calls `server-level-tick.md` "the server tick".
  Both are label bugs, not target bugs; fix them when those parts are
  reshaped, or session P sweeps them.
  **Process**: five pages drafted by parallel agents on Opus against a shared
  brief, each report diffed by the session, which re-derived twelve of the
  eighteen corrections from the decompile itself. One lesson worth carrying:
  an agent reported a corrected ordering in its prose **and then drew the old
  ordering in its new diagram** (light before block packets in
  `ChunkHolder.broadcastChanges`). A drafting report is not evidence about
  the figure; read the figure separately.

- **Session E (Part IV The world).** **`tools/check_lanes.py --pages` was
  matching the wrong directory.** It filtered with a plain `startswith` on
  absolute paths, so `--pages src/systems/world` also picked up
  `src/systems/worldgen` and reported nine unconverted Part XII pages as
  Part IV failures. Fixed with a `_under` helper that requires a path
  separator; **session M would have hit this head-on**, and any later
  session scoping to a directory whose name is a prefix of another should
  now be safe. This is the third pass-3 session to find a bug in a tool
  before finding one in a page — the "suspect the tool once" lesson is
  holding.
  **The lane key is now pruned to lanes in use.** Session E added 62 rows
  before drafting and then removed the 29 no page introduced, because a key
  row is a claim on a lane corpus-wide and claiming one speculatively
  pre-empts a session that has not run. Rows *not* claimed, and therefore
  still open for the sessions that own those pages: `CA`, `PC`, `IPC`,
  `LCS`, `PCon`, `HM`, `CCC`, `GCH`, `CST`, `CG`, `CP`, `WGR`, `LLE`,
  `SLE`, `CSLS`, `DLay`, `RFS`, `RF`, `ES`, `SS`, `SDS`, `PCT`, `WF`, `LF`,
  `EGELR`, `VS`, `SSBE`, `PS`, `PRec`. Rows Part IV **did** claim, which
  later sessions must lengthen around: `LC`, `SCD`, `IOW`, `LCTs`, `LTs`,
  `FF`, `LB`, `BI`, `RB`, `GED`, `VSL`, `VST`, `VSel`, `SSB`, `PM`, `PN`,
  `AP`, `VNP`, `SIB`, `Brain`, `BLE`, `TLE`, `LLSS`, `EAP`, `EVS`, `ATS`,
  `KTS`, `SCM`, `GS`, `SAI`, `SR`, `Camera`, `Mob`, `CGT`. Three collisions
  were resolved by lengthening the later claimant, as the rule says:
  `LevelChunkTicks` → `LCTs` (`LCT` is session A's `LoadingChunkTracker`),
  `PoiRecord` → `PRec` (`PR` is session C's `PackRepository`) — though
  `PRec` was then pruned unused — and `PalettedContainer` → `PCon`, also
  pruned. **Four page lanes now collide with unconverted parts** and those
  sessions will have to lengthen: `PM` (`PlacementModifier` in
  `features-and-placement`), `GS` (`GlyphStitcher` in `text-and-fonts`),
  `CG` was not claimed but `biomes` uses it for `NoiseBasedChunkGenerator`,
  and `LB` (`LeverBlock` in `redstone`) — **session F should expect to
  rename that one**, since `LB` is `LiquidBlock` now.
  **A part-session pattern worth repeating.** Both Part IV splits were
  drafted by two agents working from the same source page in parallel, each
  told where the seam was, which classes were theirs, and what to hand over
  in one clause plus a link. Neither duplicated the other and both reported
  the seam facts they had handed over — but **both also flagged that they
  could not see the sibling page while writing**, so the cross-links were
  written blind and the session had to check them. A future split session
  should either sequence the two halves or plan a link-check pass; session E
  did the latter.
  **For session F (Part V Blocks).** Three things landed in Part IV that
  Part V now links into rather than re-teaching. `scheduled-ticks` owns the
  appointment book and traces a **repeater** specifically so `redstone` can
  link to it for the delay, the priorities and the pulse-extension
  behaviour; `redstone.md`'s link was re-pointed there this session.
  `fluids` owns `LiquidBlock`, waterlogging and the flow model, and
  `blocks-and-states`' `Fluid`/`FluidState` link now points at it.
  `game-events-and-vibrations` owns `GameEvent` posting, and the three
  Part V links (`block-breaking`, `block-interaction`, `blocks-and-states`)
  were re-pointed. Also: `chunk-anatomy` now states that
  `BlockBehaviour.BlockStateBase.affectNeighborsAfterRemoval` runs **inside**
  `LevelChunk.setBlockState` — the old page denied it — so R6's
  *two update channels* flowchart, which session F draws in
  `blocks-and-states`, must place that call inside the chunk write, not in
  `Level.setBlock`'s tail.
  **For session G (Part VI Entities).** `points-of-interest` names the
  villager memories and behaviours its trace passes through and links to
  `ai-goals-and-brains` for the brain itself; it also corrects
  `ValidateNearbyPoi` to the rest package, so the brain page's activity
  story and this one must agree. `game-events-and-vibrations` owns the
  warden's and allay's listener behaviour at the vibration level only.
  **For session O (Reference).** `level-data-and-rules` is now
  `src/reference/level-data-and-rules.md` with a redirect and a corrected
  header, and is listed in the reference README and `SUMMARY.md`; **its body
  is still a systems page's body** and wants the same reframe
  `math-and-primitives` will get. Two extraction candidates arrived with it:
  `environment-attributes-and-timelines`' twenty-one-class *called by*
  roster, and Part IV's POI catalogue, both of which are class-index
  material rather than lecture material.
  **The coverage queue is unchanged.** Part IV has no entry in §7 and
  session E spent no R7 allowance — its two new pages are the notebook's
  confirmed splits, not new coverage. The queue still stands at fifteen
  items.

### Session F (Part V Blocks) — for later sessions

**A part session can lose its drafting agents, and the recovery is cheap if
the seams were written down first.** This session was interrupted with four
of seven pages drafted; five agents were killed and could not be resumed. The
four drafted pages were all complete on disk, but two of the four reports
were lost, which is the real cost — a page whose claim-diff never arrived is
a page pass 4 has to treat as unaudited (recorded in
[pass4.md](pass4.md)). The three undrafted pages were then written by the
session directly from the decompile, which cost about as much as reviewing
three drafts would have. **The lesson for the remaining part sessions: the
per-page seam rulings in the log are what made the recovery possible, so keep
writing them before dispatching, and consider having agents report
incrementally rather than only at the end.**

**Part V's shape settled as a hub and six spokes, and the hub is the write,
not the state table.** The notebook called `blocks-and-states` the hub
because everything reaches back into it; what they actually reach for is the
tail of `Level.setBlock` and `LevelChunk.setBlockState`, now drawn once as a
single flowchart under the anchor
`blocks-and-states.md#the-two-update-channels`. Six pages link to that
anchor. **Any later session that moves or renames that section breaks six
links**, and Parts VI, IX and X are all likely to want to link to it too.

**The redstone split is executed and is three pages**, `signal-and-dust`
(signal reading, the wire, both evaluators, the torch), `pistons-and-block-events`
(the block-event mechanism in general, then the piston) and
`diodes-and-observers` (repeater, comparator, observer as a comparison).
`redstone.md` is deleted and redirects to the first. Note where the seams
landed, because other parts link across them: **`pistons-and-block-events`
owns block events as a general mechanism**, which nothing else in the corpus
explains and which Part X's `what-the-client-is-told` and the glossary both
point at now; **`signal-and-dust` owns weak versus strong power and the third
direction order**; **`diodes-and-observers` owns
`Level.updateNeighbourForOutputSignal`'s meaning**, though its call site is
drawn in `blocks-and-states`' flowchart.

**For session G (Part VI Entities).** `pistons-and-block-events` names
`MoverType.PISTON` and `PistonMovingBlockEntity.moveCollidedEntities` and
links to `movement-and-collision.md` for both — that link was re-pointed from
the old `redstone.md` this session. `block-breaking` hands `ItemEntity` and
`ExperienceOrb` to Part VI as before.

**For session K (Part X The client).** `prediction-and-acks` is now the owner
of the ledger for real: both Part V click pages carry an identical
four-sentence preamble stating the contract and nothing else, and neither
re-derives the machinery. **If session K changes what the contract says, the
two preambles must change with it, and they must stay identical to each
other.** Part V's landing page also rules that Part V is watched *before*
`prediction-and-acks`, resolving the circular dependency the notebook flagged
in section 5 — session P should carry that ruling into `lectures.md`'s
cross-part section.

**For session O (Reference).** Two catalogue candidates surfaced and were
deliberately not written: the **block-event users** (four blocks and seven
block entities, with their two int parameters), currently a paragraph in
`pistons-and-block-events`; and the **update-flag bit table**, currently a
ten-row table in `blocks-and-states` that four other pages reference in
prose. The flag table is the stronger Reference candidate of the two — it is
exactly the thing a viewer would pause the video to read.

**The coverage queue is unchanged at fifteen items.** Part V has no entry in
section 7 and session F spent no R7 allowance: its two extra pages are the
notebook's confirmed split, not new coverage.

**Lane ledger.** Thirteen rows added to the key in `TEMPLATE.md` (`Block`,
`MPGM`, `SPGM`, `CNU`, `DB`, `AFBE`, `FM`, `LevB`, `RSWB`, `DRWE`, `PBB`,
`PSR`, `PMBE`), all of them used by a diagram that exists. Four collisions
were resolved by lengthening the later claimant and are recorded under the
key: `LeverBlock` is `LevB` (`LB` is `LiquidBlock`), `BlockItem` would be
`BItem` (`BI` is `BucketItem`), `BlockPlaceContext` would be `BPC` (`PC` is
`ProtoChunk`), and `PistonStructureResolver` is `PSR` (`PR` is
`PackRepository`). The last two of those are recorded but **not yet used by
any page** — a later session may claim them or free them.

### Session G (Part VI Entities) — for later sessions

**Authority has an owner now, and four pages are expected to link to it
rather than re-derive it.** `src/systems/entities/authority.md` is the R6
page: the four predicates (`Entity.isLocalInstanceAuthoritative`, which is
**final**, plus `Entity.isLocalClientAuthoritative`,
`Entity.isClientAuthoritative`, `Entity.canSimulateMovement` and
`Entity.isEffectiveAi`), a three-column comparison of a tracked mob, a
player and a ridden vehicle read on both sides, and the six gates inside
`Entity.move` and `LivingEntity.aiStep` that read them.
`movement-and-collision` has already been cut back to three sentences and a
link. **Sessions I, J and K should do the same**: `input-to-movement` and
`player-anatomy` (Part VIII) each carry a version of the matrix,
`what-the-client-is-told` (Part IX) leans on it, and Part X's client-tick
material does too. The page also owns the vehicle case, which nothing else
did: the base implementations of both client-authority predicates delegate
to the **controlling passenger**, which is the whole vehicle model, and it
is why `ClientboundMoveVehiclePacket` is a rejection notice rather than a
routine update.

**The AI split landed as two pages, not three, and the seam is the
waterline.** `ai-goals-and-brains` keeps its URL (no redirect needed) and
owns goals, brains, memories, sensors, behaviours, activities and the
villager day; **`pathfinding` is new** and owns `PathNavigation`,
`PathFinder`, `NodeEvaluator`, `PathType`, `PathTypeCache`,
`PathNavigationRegion`, the node budget, stuck detection, the four controls
(`MoveControl`, `LookControl`, `JumpControl`, `BodyRotationControl`) and
`ServerLevel.sendBlockUpdated`'s push into `ServerLevel.navigatingMobs`.
Other parts link across that seam: **anything about a mob's *decision* goes
to the first, anything about a wanted position becoming movement goes to the
second.** `attributes` and `movement-and-collision` were re-pointed this
session.

**`entity-anatomy` now includes a generated figure**, `tree-Entity.svg` from
session B's atlas, in place of a hand-drawn mermaid class tree. That is the
first system page to use the figure pipeline, and it is the pattern for any
other page whose figure is really a tree with numbers on it — Part XI's
render-state hierarchy and Part XII's structure-piece families are the
obvious candidates.

**For session K (Part X The client): one lane must be lengthened.**
`SE` is now `ServerEntity` in the key, used by four Part VI pages;
`systems/client/sound.md` uses `SE` for `SoundEngine` and is the later
claimant, so it becomes `SndE` or similar when session K rewrites it. Two
more collisions were resolved *away* from the obvious spelling and later
sessions should not re-take them: `AM` stays `AtlasManager` (Part XI), so
`AttributeMap` is `AttrM`, and `EC` stays `ExecutionContext` (Part XIII), so
`EffectCommands` is `EffC`. `ES` is `EntityStorage`, which means
`EntitySection` would have to lengthen to `ESec`.

**For session O (Reference): three new pages, two of them generated.**
`gen_reference.py` grew two views — `entity-data-serializers` (43 rows in
registration order, which is the wire id) and `attributes` (40 rows with
default, range, syncable and sentiment) — so both regenerate on the next
version like the other four. `non-living-damage.md` is **hand-kept** and
wants the same re-sweep the other hand-kept pages get; its twenty-one rows
were read one class at a time this session. Also fixed in passing: the
`gamerules` view's blurb still linked to the old
`systems/world/level-data-and-rules.md` path, so **regenerating the
reference tier used to reintroduce a broken link that session E had fixed by
hand**. The tool is the fix; check the other blurbs' links when the pages
they point at move.

**Two extraction candidates surfaced and were not written.** The nineteen
`EntitySpawnReason` constants, currently named three at a time across
`entity-lifecycle`, and the `Nether fortress` / `Structure.spawnOverrides`
spawn-list override, which is verified true and was cut from
`entity-lifecycle` for budget — it belongs on a Part XII page or in
Reference, and **nothing in the corpus says it now**.

**The coverage queue drops to fourteen.** Part VI's entry — the non-living
`Entity.hurtServer` overrides — is discharged as the closing section of
`damage-and-death` plus `reference/non-living-damage.md`, which is one of
the three options the queue itself offered. R7's new-page allowance was
therefore **not** spent: both of the part's extra pages are R6's owner page
and the notebook's confirmed split.

### Part VII, for the sessions that follow *(session H)*

**The two-tier shape held, and it is a claim later sessions rely on.** The
vocabulary (`items-and-stacks` → `using-an-item` → `containers-and-menus`)
is a hard prerequisite of all five engine pages; the three engines
(`recipes` · `enchantments` + `enchanting` · `contexts-and-predicates` +
`loot-tables`) depend on each other not at all, and the landing page and
`lectures.md` both say so. If a later part discovers a dependency between
two engines, that is the claim to revisit.

**`contexts-and-predicates` is now the page other parts should link to, and
Part XIII in particular.** `/execute if predicate`, the entity selector's
*predicate* option and the advancement predicate library all run on
`ContextKeySet` and `LootContext`, and the page owns them, including the
`/execute if predicate` trace. Session N should link rather than re-explain;
`advancements` and `scoreboard-and-data` were already re-pointed there this
session, as was `brigadier-and-commands`'s `EnchantCommand` sentence (now
`enchanting`). **Twelve of the twenty-six parameter sets never roll a loot
table** — the old page's "five" was wrong twice over — and the counted
version is the one to quote.

**Two Reference views are generated and both have a Part VII page behind
them**: `enchantment-hooks` (every `EnchantmentHelper` entry point plus the
classes that call it, scanned from the whole tree — the pattern generalises
to any static seam class, and `Block`/`ItemStack` would answer the same way)
and `loot-context-params` (the sets with their required and optional keys).
Session O should keep both in the reference README and re-run
`gen_reference.py all` after any decompile bump.

**Session L inherits a ruling, not a question.** *How an item picks its
model* is Part XI's (see §7); `items-and-stacks` and the Part VII landing
page both link forward to `models-and-atlases`, so session L needs to make
that link land on something — a page or a named section.

**Session I (Part VIII) should read `using-an-item` first.** The spear's
`Item.Properties.spear` override of `UseEffects`, the
`ServerboundPlayerActionPacket.Action.STAB` path and `LivingEntity.stabAttack`
are all named there in passing, and `the-sword-swing` should not re-derive
the use pipeline to explain them. `hunger-xp-and-effects`' eating link was
re-pointed to `using-an-item` this session.

**Lanes.** Twenty-one rows added to the key, eleven of them the later
claimant lengthened (`ChestM`, `CraftM`, `EScr`, `RemS`, `ResultS`,
`ResultC`, `CSync`, `CMap`, `LootP`, `LootC`, `LPool`, `RCont`, `ExecC`,
`Ench`). Part VII takes no single-letter lane at all, which resolves the
`C`-is-`Container`-here collision session K recorded from the other side:
`C` is free for `Commands` when session N converts Part XIII.

**One page was not split although the notebook offered the seam.**
`containers-and-menus` keeps the storage model, the click protocol and the
exceptions in one lecture, because the protocol is unreadable without the
model and the model is pointless without the protocol; the exceptions
(creative's parallel protocol, the crafting-result side channel) are a named
closing section instead. It is the part's longest page at 389 lines and the
first candidate if pass 5 wants a split after all.

### Part VIII, for the sessions that follow *(session I)*

**The authority matrix now exists once, and Part VIII is the proof it can be
deleted.** `input-to-movement` and `player-anatomy` each carried a copy; both
are gone, replaced by a link to `entities/authority.md` and two named
consequences (fall damage on the packet path, the ground flag). **Sessions J
and K should do the same** — `what-the-client-is-told` and the client-tick
material are the last two leaners — and the shape that worked is: link, then
state only the consequences *this* page's story needs, in the paragraph that
needs them, never as a table.

**The part grew from four pages to seven, and both splits were free.** The
two-phase tick and status effects were each already written, inside a page
that was doing something else; splitting cost no new research and took both
host pages under the length brief. That is now three sessions running
(G, H, I) where the notebook's proposed seam was real. The one page session I
did **not** split is `input-to-movement` at 410 lines, and its seam is
visible: everything before *the trace* is the client, everything after is the
server's judgement, and the second half is a policy page wearing a trace's
clothes. Pass 5, or a later pass-3 session with budget, should look at it.

**For session J (Part IX).** `the-two-phase-tick` now owns the sentence that
the connection tick runs after every level has ticked, and
`the-sword-swing` owns the attack packet's drain at the top of the tick,
before `MinecraftServer.tickServer`. Both are Part III facts stated in Part
VIII because the story needs them; Part IX restates the same two. If session
J wants them stated once, Part III is the owner and these three pages are the
callers.

**For session K (Part X).** Part VIII links forward twice to
`prediction-and-acks` — from `player-anatomy`, for the ledger
`MultiPlayerGameMode` does not hold, and from the landing page — and
`the-sword-swing` states `Minecraft.pick`'s per-frame versus per-tick split,
which is a Part X fact. Check that all three land on something that agrees.

**For session O (Reference).** `hunger-xp-and-effects.html` now redirects to
`hunger-and-experience.html` — the first content-page rename in pass 3, as
opposed to a move. Nothing else pointed at it but the generated class index
and three body links, all repointed. Also: the spear's component table is the
kind of thing `gen_reference.py` could generate for every `Item.Properties`
helper, if a later session wants the *what makes an item a weapon* view.

**A tool note.** `check_lanes.py --index` reports the corpus-wide state, and
it is currently **28 disagreements and 17 collisions** across the parts not
yet converted. Six lane rows were added for Part VIII (`Inv`, `FD`, `FP`,
`KM`, `KI`, `MEI`); every Part VIII diagram that used a mis-keyed lane —
`CL` for `ServerGamePacketListenerImpl`, `PL` for `Player`, `CM` for
`AbstractContainerMenu`, `IS` for `ItemStack`, `MG` for `MultiPlayerGameMode`
— was corrected, which is most of what the old pages got wrong.

### Part IX, after session J — what session K inherits

*(session J, 2026-09-03)* `what-the-client-is-told` handed its client half
to Part X and kept a one-paragraph link, per session G's guess. **Session K
owns the following, and should check each one is actually present in
`the-client-level` rather than assume the hand-off landed** — a fact that
moves to a new owner must arrive there, not merely leave here:

- The `ClientLevel` field inventory: `tickingEntities`, `entityStorage` as a
  `TransientEntitySectionManager`, `lightUpdateQueue`, `destroyingBlocks`,
  the tint caches, `clientLevelData` and `BlockStatePredictionHandler`.
- `ClientChunkCache.Storage` as a torus — an atomic array of (2r+1)² indexed
  modulo the view range, with volatile centre coordinates because the render
  thread reads them. The page has a chunk-cache section; the atomic and
  volatile details are what to confirm.
- `ClientPacketListener.serverChunkRadius` and
  `ClientPacketListener.serverSimulationDistance`.
- **`Entity.moveOrInterpolateTo` and the interpolation table — this one has
  no other owner in the corpus.** The default returns a null
  `InterpolationHandler`; `LivingEntity`, `Display`, `ExperienceOrb`,
  `Shulker`, `FishingHook`, boats and minecarts supply one; arrows, thrown
  potions, primed TNT and dropped items snap. `movement-and-collision`
  already owns the three-tick handler and the 64-block snap, but not the list
  of who interpolates.
- `ClientLevel.hasChunk` unconditionally true, and `ClientLevel.explode` and
  its game-event dispatch empty.
- The eight `ClientPacketListener` handlers that never hop, as an
  enumeration. Session J softened its own wording to *among the handful* and
  kept only the two chunk-batch handlers, because they are the ones on the
  chunk path. The full eight belong either in `the-connection` or in
  `reference/threads.md` — session O should be asked which.

Two smaller notes for session K. `the-connection`'s round-trip diagram now
asserts that the client's drain runs **once per frame** and links
`anatomy#two-loops-and-a-wire-between-them` with `the-client-loop` as the
deeper reference; if session K moves or renames that heading, three Part IX
links break. And Part IX's landing page states that Part IX is a prerequisite
of Part X — Part X's *before you start* has to agree, or one of the two is
wrong about the watch order.

**Lanes settled in Part IX** *(session J)*. The part's three key
disagreements are gone: `Varint21FrameDecoder` no longer appears as a
participant (the old diagram went with the rewrite, so no `VFD` row was
needed), `ChunkMap.TrackedEntity` is now keyed as `CMTE` — outer initials
plus its own, the nested-class rule, replacing an unkeyed `TE` — and
`ChatScreen` is `CScr` beside the corpus's existing `EScr` and `DScr`, with
`ChatListener` as `CLis`. `PacketEncoder`/`PacketDecoder` kept the key's
existing `PEnc`/`PDec` rather than the session's proposed `PktE`/`PktD`: the
rows already existed for `codecs-nbt-json`, they satisfy the real constraint
(not `PE`, which is `ParticleEngine`), and adding a second abbreviation for
one class would break the key's own rule of one meaning corpus-wide. Part IX
is clean under `check_lanes.py --strict`; the corpus-wide count is still 25
disagreements and 16 collisions, all in parts sessions K–N have not reached.

### Part X, after session K — what sessions L, M, O and P inherit

*(session K, 2026-09-03)*

**Four open questions from section 6 are answered, and the answers are
rulings a later session should not silently re-open.**

- *Does `prediction-and-acks` belong in Part IX rather than Part X?*
  **No.** It stays. Its two applications are Part V pages, and Part V's
  landing page already rules that Part V is watched first; moving it into
  Part IX would put the machinery two parts before the vocabulary it needs.
- *Does `text-and-fonts` belong in Part XI?* **No**, same shape of answer.
  It is the only page a viewer can watch straight after Part II's
  `text-components` without having seen a render pass, and it ends at a
  `Font.PreparedText` rather than at a draw call. Session L should link to
  it from `entity-rendering` rather than re-teach the glyph pipeline.
- *Where does the debug subscription system live?* **Part X, as its
  closer**, and it is the part's one *pattern* page. The machinery ships on
  the dedicated server, but the client is the only thing that asks and the
  only thing that draws, and the trace ends in a renderer.
- *Does the corpus admit a reference-tier table inside a lecture page?*
  **No** — it admits a Reference *page* and a link.
  `src/reference/hud-elements.md` is the worked example: thirty rows, in
  record order, with the condition each element is gated on. Session L has
  the same question with the render-state hierarchy and session N with the
  selector grammar, and this is the precedent.

**`sound` is split, and the seam is *machine* against *content*.**
`sound-engine.md` owns the five threads, `ChannelAccess`, the channel
limits, the volume arithmetic, the three looping mechanisms, the device and
the decode stack. `what-makes-a-sound.md` owns `SoundEvent`, `SoundSource`,
`sounds.json`, the three doors (a named sound, a level event, client-side
ambience), the local-player prediction, propagation delay and the
environment-attribute music model. `sound.md` is deleted and redirects to the
engine. **Other parts link across that seam**: anything about *how* a sound
is produced goes to the first, anything about *what decides a sound happens*
to the second. `reference/threads.md`, `what-this-book-skips` and `blaze3d`
were re-pointed this session.

**For session L (Part XI Rendering).** Three things Part X now asserts that
Part XI has to agree with. `the-client-loop` stops at the profiler's *frame*
zone and states that `FramerateLimiter.limitDisplayFPS` runs **inside**
`Minecraft.renderFrame`, after the present — the old diagram had it after
*Post render*, and `the-frame` should be checked for the same error.
`the-client-level` states that `LevelExtractor` is reached three ways — the
level pushes, the chunk cache calls it directly, and the extractor pulls
three collections per frame with no notification — which is a claim about
Part XI's entry points. And `the-gui-render-tree` states that
`GuiRenderer.endFrame` is called by `GameRenderer` rather than by
`GuiRenderer.render`, and that `GuiRenderState.isHudHidden` is read by
`GameRenderer` in three places, with a clear-colour override on the same
object read alongside it. Also: **`LX` is now keyed as `LevelExtractor`**, which five pages in
two parts already used it for, so Part XI's `LightmapRenderStateExtractor`
is the later claimant and must lengthen.

**For session O (Reference).** One new hand-kept page,
`src/reference/hud-elements.md`, wanting the same re-sweep the other
hand-kept pages get. And session J's deferred question is still open and is
**not** Part X's to answer: the eight `ClientPacketListener` handlers that
never hop belong either in `the-connection` or in `reference/threads.md`,
and session O should pick. Part X does not state the list.

**The coverage queue is unchanged at fifteen items, and Part X's entry is
explicitly deferred rather than declined.** *World creation and the
world-select screens*, ~5,100 lines, spans Parts X and XII: half of it is
worldgen's world-creation settings and half is a screen family. Splitting
one subject across two part sessions is how this corpus grew its
duplications, so session K spent no R7 allowance on it. **Session M should
rule on it with the worldgen half in front of it**, and session P discharges
whatever is left. The sound split is a confirmed split, not new coverage.

**Lane ledger.** Twenty-six rows added, seven of them lengthened later
claimants and two of those lengthened *pre-emptively*: `StringSplitter` is
`SSpl` and `FontSet` `FSet` although `SS` and `FS` are unkeyed, because both
short forms are contested in Part XII and leaving them free costs Part X two
letters. The others: `SndE`/`SndM` (`SE` is `ServerEntity`, `SM` is
contested), `ChanA` (`CA` means three things in three unconverted parts),
`GuiR` (the key's own recorded collision with `GameRenderer`), `InvS` (`IS`
is `IntegratedServer`) and `GStit` (`GS` is `GaussianSampler`). `Library` and
`Channel` take their own names under the short-word rule. Part X is clean
under `check_lanes.py --strict`; the corpus-wide count fell from 25
disagreements and 16 collisions to **19 and 10**, all of them in Parts XI to
XIII.

---

*(session L, 2026-09-03)*

**Five open questions from section 6 are answered, and the answers are
rulings a later session should not silently re-open.**

- *Does `the-window` open Part XI, sit third, or move to Part I?* **Second**,
  and it stays in Part XI. R6 already ruled that `the-frame` opens the part;
  the window is the first thing the frame assumed, so it follows immediately.
  Part I is deliberately two pages and a GLFW window is not program anatomy.
- *Is the substrate one lecture or two?* **Two.** `the-window` and `blaze3d`
  share only the word *substrate*: one is GLFW, monitors, six callbacks and
  `NativeImage`, the other is a graphics API with two backends, and their
  hooks do not survive being merged.
- *Does post-processing get its own page, or a section of `the-frame`?* **A
  page**, and the part's R7 spend — see §7.
- *Who owns "how an item picks its model"?* **Part XI, as a named section of
  `models-and-atlases`** rather than a page — see §7. Part VII's two forward
  links now carry the anchor.
- *`LX` and `GR` mean two things each.* Fixed by lengthening the later
  claimant in every case: `LightmapRenderStateExtractor` is `LRSE` because
  session K keyed `LX` as `LevelExtractor`, and `GuiRenderer` was already
  `GuiR` so `GR` stays `GameRenderer` unopposed.

**`level-rendering` is split, and it was the corpus's oldest deferred seam.**
Sessions 10, H and I all confirmed *meshing* against *visibility and the
frame graph* and none executed it. It is executed now:
`visibility-and-the-frame-graph.md` (the occlusion walk, the frustum step,
the pass declarations, the multi-draw batching, the translucency budget) and
`section-meshing.md` (the dirty halo, the 27-section snapshot, the worker
compile, the staging buffer, the late atomic swap). Visibility comes first
because it continues `the-frame` and because meshing is gated on it; the old
URL redirects there. **The evidence for splitting was the cast budget, not
the line count** — the two halves shared `LevelRenderer` and nothing else,
and a later session facing the same call (`brigadier-and-commands`,
`blocks-and-states`, `entity-anatomy`) should count casts rather than lines.

**Redrawing found two errors in pass-2 prose, which is now three parts in a
row** (session K's frame limiter, session J's, and these). Both are in
[pass4.md](pass4.md) at the head of the session-L entry. The first is the
one worth generalising: `the-window` claimed six operating-system callbacks
of which three reach the game through `WindowEventHandler`. Only **two** do;
the interface's third method is called by `Minecraft` and `Options` on
themselves and never by `Window` at all. The old claim was an inference from
three method names lining up with three callbacks, and it was drawn as a
figure before anyone opened `Window`'s registrations. **A figure asserts
more than the prose it was drawn from**, which is exactly why pass 3 draws
them.

**For session M (Part XII World generation).** Part XII asks Part XI's
question and section 1 already noticed: is `density-functions` a substrate
like `blaze3d`, and does a substrate open a part or close it? Part XI's
answer, now tested on two pages: **open with the part's trace, then the
substrate, then the pipeline** — a reader who has seen one frame end to end
has a reason to care what a `GpuDevice` is, and the same argument makes
`worldgen-pipeline` before `density-functions` worth considering against §1's
recommendation. Session L holds it weakly and Part XII's substrate is more
genuinely prerequisite than Part XI's was, so this is evidence and not a
ruling. Also: `SM`, `SS` and `FS` are still free and still contested in Part
XII's prose, as session K left them.

**For session O (Reference).** One new hand-kept page,
`src/reference/submit-phases.md` — the fifteen `SubmitNodeCollection` phases
in declaration order with what lands in each and which execute method drains
it, and the thirteen feature renderers with what each writes. It is the
richest of the hand-kept pages and the one most likely to drift on a version
bump, because both orders are declaration orders. It wants the same re-sweep
the others get, and it is a candidate for generation if `gen_reference.py`
ever learns to read a constructor's registration order.

**And one generated figure**, `tree-EntityRenderState.svg`:
`EntityRenderState` joins `TREE_ROOTS` in `map_source.py`, on session G's
`tree-Entity.svg` precedent, and `entity-rendering` includes it in place of a
hand-drawn class ladder. **98 render states, 70 of them living.** The other
candidate §8 named — Part XII's structure-piece families — is still open.

**Lane ledger.** Thirty-three rows added, the largest single addition in the
pass, and eleven of them lengthened later claimants: `SectC`
(`SC` is `StopCommand`), `Time` for `Timelines` (`TL` is `TagLoader`), `LRSE`
(`LX` is `LevelExtractor`), `SprL` (`SL` is `ServerLevel`), `GlCE` and `GB`
(`B` is `Block`, which `particles` should have been using all along), `MonM`
(`MM` went to `ModelManager`, which more pages cite), `GpuS` (`GS` is
`GaussianSampler`), and `EAP`, `MC` and `Window` where the old pages had
simply used `P`, `M` and `W` for classes the key already named. `Game` is a
new word lane for the game's own code above Blaze3D. Part XI is clean under
`check_lanes.py --strict`; the corpus-wide count fell from **19 disagreements
and 10 collisions to 15 and 6**, all now in Parts XII and XIII.

**The coverage queue is down to thirteen and Part XI's remaining entry is
sharpened.** Block-entity rendering (`renderer/blockentity` plus
`renderer/special`, ~3,300 lines) stays queued, and writing
`entity-rendering` confirmed why it is a page rather than a section: the two
now share one extract/submit/prepare/execute machine, so the page that would
be written is *the differences*, and the differences are real — a stricter
visibility rule enforced twice, per-renderer view distances, and
`renderer/special` existing so that a chest in your hand looks right with an
empty model. Session P should write it if there is budget.
