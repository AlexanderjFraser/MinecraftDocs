# Pass 3 — the restructuring notebook

*Started 2026-09-01, at the beginning of pass-2 session A, as the file
where pass-2 sessions **wrote pass 3's inputs down as they found them** —
observations you can only make with the decompile open and the page in
front of you. Pass 3 ran 2026-09-02 to 2026-09-03, sessions A–P, and is
**done**; §1–§6 are the evidence its eight rulings were made from, §8 the
notes its sessions left each other, and §9 and §10 its charter and its
session log, archived here from [plan.md](plan.md) at the close. One
section stays live: **§7, the coverage queue** — a system with no owner
page is filed there by any later pass, and a session that writes one
strikes it through. Facts to re-check go to [pass4.md](pass4.md); wording
debt to [pass5.md](pass5.md).*

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

**Closed by session P (2026-09-03).** Every question above that was not
already struck through is answered, and the answers are on the site rather
than here; one line each. *Does `environment-attributes-and-timelines` move
earlier than Part IV?* No — it stays Part IV's first lecture, and
`lectures.md`'s dependency section names it as the one page worth watching
before its part. *The lane collisions* (Part IV's, Parts VII/VIII's, `LX`,
`GR`) are resolved by the key in `TEMPLATE.md`, which `check_lanes.py
--strict` now enforces corpus-wide with zero disagreements. *Does
`the-client-loop` belong in Part I?* No — it stays Part X's hub; three parts
depend on it by link and the dependency table on `lectures.md` says so.
*`prediction-and-acks` in Part IX?* Part X, ruled by session K. *A
`Component` page in Part II?* Yes, `text-components`, session C. *The debug
subscription system* — Part X, session K. *`blaze3d` second or last?* Third,
session L. *A reference-tier table inside a lecture page?* Ruled by session
K: the table moves to Reference when a viewer would pause on it, which is
what `hud`'s did. *`the-window`* — second; *the substrate* — two lectures;
*post-processing* — its own page; *the item model* — a section of
`models-and-atlases`; all session L. *Block-entity rendering* — its own
page, written by session P beside `entity-rendering`. *The permission
model* — its own page, session N. *The registry-element pattern* — Part II's
`data-driven-types`, session C. *The scoreboard* — Part XIII, session N.
*The appendix* — dissolved by R1, session C. *The glossary* — hand-kept,
session O. *`out-of-scope-tour` first or last?* Second: it is Part I's
closer, because the boundary is drawn before the investment, and
`lectures.md` says why the book does not end on it.

## 7 · The coverage queue

*Systems the pass-2 inventories found with no owner. Ruling R7 in
[plan.md](plan.md) lets each part session write at most one of these; the
rest wait here, and session P discharges what budget allows. A session that
writes one strikes it through; a session that rules one out says why, here.*

- **The expansion hack, dimension padding and liquid settings** — three of
  `JigsawStructure`'s ten data-pack fields that no page names, and one of them
  is load-bearing for why a village street stops:
  `JigsawPlacement.Placer` inflates a candidate's bounding box upward by the
  tallest piece its own child pools could need before the collision test, and
  all five villages set *use_expansion_hack* true. `DimensionPadding` rejects
  a start piece too near the world's Y limits and shrinks the growth box;
  `LiquidSettings` decides per structure or per element whether placed blocks
  inherit waterlogging. `jigsaw-and-templates` names one of the three in
  passing after pass 4 and owns none of them. Not a whole page — a section on
  that page, for pass 5 or later. *(session L of pass 4, 2026-09-05)*
- ~~**Post-processing**~~ — **written by session L** as
  `src/systems/rendering/post-processing.md`, the part's closer and its R7
  spend: 996 lines in four classes, six shipped chains, written against the
  JSON in `reference/26.2/assets/` that the planning session staged.
  *(session I, discharged session L)*
- ~~**Block-entity rendering**~~ — **written by session P** as
  `src/systems/rendering/block-entity-rendering.md`, a comparison page
  beside `entity-rendering`: three roads into one collector, not two — an
  item model and a *block state* both reach `renderer/special`, through a
  second model table terrain never reads. Writing it found the hook the
  entry could not: the chest on the ground and the chest in your hand are
  drawn at different partial ticks, and under */tick freeze* only one
  stops. The territory is ~4,300 lines, and 25 of the 26 render states are
  reachable. *(session I, discharged session P)*
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
- ~~**The permission model**~~ — **written by session N** as
  `src/systems/commands/permissions.md`, Part XIII's R7 spend: the split of
  `brigadier-and-commands`, four sessions after the seam was first named.
  Writing it settled what the entry could not — the two universes are not
  symmetric. The server's set is *additive* (a rung, plus exactly one atom,
  unioned upward) and the client's chat set is *subtractive* (all four atoms,
  minus whatever four purely local restrictions remove), so no packet
  carries a `PermissionSet` in either direction and the client can only ever
  learn "this needed some permission" by parsing the same string twice.
  *(sessions 12, K, discharged session N)*
- ~~**The function model**~~ — **written by session N** as
  `src/systems/commands/functions-and-macros.md`, the other half of
  `execution-and-functions` (redirected to `the-execution-engine`). It is a
  four-stage pipeline page, and the seam held exactly as session K predicted:
  the two halves share one class. *(session K, discharged session N)*
- **Writing a game test** — `GameTestHelper`, 1,353 lines. **Ruled by
  session P: not a lecture in this series.** `game-tests` now carries the
  class as a cast row ("the entire surface a test body sees") and its
  trace runs one test; a page on *writing* one is a how-to, which is the
  shape this book does not use, and the owner decides in pass 6 whether
  the series wants a tutorial episode. Stays here as the note of that
  decision. *(session K, ruled session P)*
- ~~**The entity selector grammar**~~ — **written by session P** as
  `src/systems/commands/entity-selectors.md`, a pipeline page on Part
  XIII's parse floor. The count was wrong: five classes and 1,717 lines
  (seven files and 1,725 with the `package-info` stubs). Writing it
  settled what the entry could not — four of the twenty-one options are
  the query plan, not filters, and the player path never gets a box.
  *(session K, discharged session P)*
- ~~**The tree kit**~~ — **written by session M** as
  `src/systems/worldgen/trees.md`, Part XII's R7 spend: one algorithm with
  five pluggable slots, nine trunk placers, eleven foliage placers, one root
  placer and ten decorators. Writing it settled what the entry could not —
  the kit's most visible output is an *asymmetry*, not a variation, because
  `TreeFeature` sizes the crown from the unclipped proposed height and hands
  both placers the clipped one. *(session J, discharged session M)*
- ~~**`Blender` / `BlendingData`**~~ — **written by session P** as
  `src/systems/worldgen/blending.md`, a pattern page: one measurement,
  five consumers at four statuses, two of them outside the density graph.
  The 858 lines were right; the brief's `ProtoChunk.setBlendingData` does
  not exist (the field is final and arrives from the save). *(session J,
  discharged session P)*
- ~~**World creation and the world-select screens**~~ — **written by
  session P** as `src/systems/worldgen/creating-a-world.md`, Part XII's
  closer, in session M's ruling: a pipeline page on the settings object
  with the screens as one stage and the dedicated server as the comparison
  column. Writing it found that `WorldGenSettings` is a `SavedData` in its
  own file, not part of *level.dat*, and that the Superflat layer editor's
  Cancel button does not undo. *(session J, ruled session M, discharged
  session P)*
- ~~**The non-living `Entity.hurtServer` overrides**~~ — **discharged by
  session G** as the closing section of `damage-and-death` (five families)
  plus the per-class table in `src/reference/non-living-damage.md`, which is
  the "Reference table" option this entry offered. The count was wrong: it
  is **21** non-living classes, not ~30, and `Entity.hurtServer` is
  *abstract*, so there is no default behaviour anywhere in the tree.
  *(session E, discharged session G)*
- **Commands that are algorithms** — `SpreadPlayersCommand`,
  `CloneCommands`, `ChaseCommand` (a debug socket protocol between two game
  instances). Part XIII, or Reference. **Session P: carried.** Three
  unrelated algorithms make a Reference page, not a lecture; a
  `gen_reference.py` view cannot write it. Pass 6 decides whether any is
  a lecture. *(session K, carried session P)*
- **The predicate catalogue and the boss bar** — 54 predicate files; the
  boss bar is `execute store`'s third sink and belongs with
  `scoreboard-and-data`. Parts VII and XIII. **Session N confirmed the third
  sink from `ExecuteCommand.wrapStores` — score, bossbar, then the three data
  providers — and corrected `scoreboard-and-data`, which said there were
  two; the page now names the boss-bar sink and points at
  `client/hud.md`, which is still not a page about boss bars.** **Session
  P: carried.** The boss bar is ~400 lines (`BossEvent`,
  `ServerBossEvent`, `CustomBossEvents`) and wants a section of
  `scoreboard-and-data`, which pass 5 can add without a new page; the
  predicate catalogue is a generation candidate with the shape library
  below. *(session K, half-corrected session N, carried session P)*
- **The predicate *shape* library** — `MinMaxBounds`, `CollectionPredicate`
  with its contents/counts pair, `EntitySubPredicate` as registry-dispatched
  extension, and `DataComponentMatchers`. Four shapes the whole data-driven
  half of the game reuses, currently a table on `advancements` because that
  is their biggest consumer. `contexts-and-predicates` owns the *context*
  machinery and not these. A Reference page, most likely generated. *(session
  N)*

- **Reference views `gen_reference.py` does not yet have** — three
  catalogues the part sessions named and session O declined to hand-keep,
  because each is a declaration order the tool could read: the nineteen
  `EntitySpawnReason` constants with what each gates (session G); the
  `Item.Properties` weapon helpers — the components that make an item a
  weapon, for every item (session I); the `Structure.spawnOverrides`
  spawn-list override, which nothing in the corpus states (session G, cut
  from `entity-lifecycle`). And the **block-event users** — four blocks and
  seven block entities with their two int parameters — stay a paragraph on
  `pistons-and-block-events` (session F's weaker candidate; declined by
  session O because the page's argument needs them in place). Reference,
  generated where possible. *(sessions F, G, I; ruled session O)*

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

---

*(session M, 2026-09-03)*

**Section 1's three Part XII questions are all answered, and one of the
answers is a ruling a later session should not silently re-open.**

- *Should `density-functions` open the part or close it?* **Open it**, as R6
  ruled, and against session L's Part XI evidence. The argument that lost is
  a good one — a reader who has seen one frame end to end has a reason to
  care what a `GpuDevice` is — and it loses because Part XII's substrate is
  genuinely prerequisite rather than merely underneath: `biomes` cannot
  explain the climate sampler without it and `terrain`'s aquifer, ore veins
  and beardifier are all density terms. What Part XI bought with its
  *frame* page, this part buys with its **landing page**, which carries the
  one-chunk overview figure. **That is the transferable ruling: in a part
  whose substrate is load-bearing, the overview is the landing page's job
  and no content page is spent on it.**
- *Is the remaining placement/jigsaw seam worth cutting?* **Yes**, and the
  seam that survived contact with the page is not quite the one §1
  proposed. It is not *decision* against *assembly*; it is **what is true of
  all sixteen structure types** (the lottery, `Structure`, `StructureStart`,
  the reference scan, `StructureCheck`, `Beardifier`, the per-chunk write)
  against **one assembler and its output format**. The `.nbt` template
  system therefore went with jigsaw rather than staying in the framework
  page, because a template is how a pool element becomes blocks, and
  `hand-built-structures` reaches it by link — which is what it was already
  claiming from the other side.
- *Does the part become XII-A / XII-B, or does structures get promoted?*
  **Neither.** R1 forbids a new numbered part this pass, and with the split
  executed Part XII is eight pages, the same size as Parts IV and XI. The
  two halves are a landing-page fact.

**The lecture order runs against the execution order, and that is the
part's shape.** Session J's §1 said "biomes → noise/surface/carvers →
structures → features", which is the *status* order for the pieces it names.
It is not quite right: `ChunkStatus.STRUCTURE_STARTS` is the **second**
status, two before `ChunkStatus.BIOMES`, and structures write their blocks
inside `ChunkStatus.FEATURES`. So the structure wing brackets the terrain
pipeline rather than following it. The landing page draws the status ladder
with the lecture numbers on it precisely so a reader sees 1, then 6-7-8,
then 2, 3, 4-5 running down it — and the cost is one forward reference, the
beardifier, which `terrain` names and `structure-placement` owns.

**A page is now allowed to have no lanes at all.** `terrain`,
`density-functions` and `structure-placement` use only flowcharts, which is
what settled three of the part's lane collisions without a rename: nobody
needed `SS` because the pages that fought over it stopped drawing
sequences. Worth knowing for Part XIII, which has the corpus's last seven
lane disagreements.

**For session N (Part XIII).** Two lanes were claimed against you and you
are the later claimant: **`CA` is `ChunkAccess`** (so `ClientAdvancements`
lengthens) and **`CF` is `ConfiguredFeature`** (so `CallFunction` does).
Three short forms were left deliberately free for you, because this part
used them to mean three different things each and stopped: **`SS`** (Part
XIII wants it for `ServerScoreboard`), **`ST`** and **`SP`**. The corpus-wide
count is now **7 disagreements and 1 collision, all of them yours** —
`check_lanes.py --strict` over `src/systems/commands` is the last thing
between the corpus and session P turning `--strict` on everywhere.

**For session O (Reference).** One new hand-kept page,
`src/reference/density-function-nodes.md` — the thirty-four registered node
types in registration order, the six markers and what the per-chunk rewrite
installs for each, the bounds rules, and what vanilla data never uses. It is
a generation candidate if `gen_reference.py` ever learns to read a
bootstrap method's registration order, which is the same wish
`src/reference/submit-phases.md` filed. Also: **the glossary is missing
*quart* and *noise cell***, both of which Part XII now leans on heavily, and
its *Structure* entry now points at `structure-placement` while *Jigsaw*
points at `jigsaw-and-templates` — worth re-reading the six worldgen
entries as a set.

**The coverage queue is down to twelve, and the world-creation entry now has
an owner.** The R7 spend was **the tree kit**, written as
`src/systems/worldgen/trees.md`: fifty classes and about three thousand
lines that `features-and-placement` documented as five contracts and zero
instances. Writing it settled what the queue entry could not — the
distinguishing fact is not that the placers differ, it is that
`TreeFeature` sizes the crown from the *unclipped* proposed height and then
hands both placers the clipped one, so the kit's most visible output is an
asymmetry rather than a variation.

And the ruling session L asked for: ***world creation and the world-select
screens* is one lecture and it belongs to Part XII**, not Part X. The
subject is `WorldGenSettings`, `WorldDimensions`, `WorldOptions`,
`levelgen/flat` and `levelgen/presets`, and `client/gui/screens/worldselection`
is that subject's user interface — a Part X page would have to teach worldgen
settings before it could explain a single screen. It is **not** written this
session (the allowance went to the trees, which is a lecture rather than a
settings tour) and stays queued with Part XII named as its owner, for
session P or pass 6. `Blender` / `BlendingData` also stays queued for Part
XII, unchanged: it is the only part of the density graph with no owner, and
`terrain` and `density-functions` between them now name it four times
without explaining it.

**Lane ledger.** Twenty-eight rows added, seven of them lengthened later
claimants (`ChunkG`, `RootP`, `TDec`, `ClimS`, `CRT`, `PlacedF`, `PMod`),
two claimed against unconverted Part XIII (`CA`, `CF`), and three contested
short forms deliberately left free (`SS`, `ST`, `SP`). Part XII is clean
under `check_lanes.py --strict`, and the corpus-wide count fell from **15
disagreements and 6 collisions to 7 and 1**.

- **Session N (Part XIII).** The part is a stack of three floors and the
  landing page draws it; the two splits and the R7 page are logged in
  [plan.md](plan.md). Four things for later sessions.

  **For session O (Reference).** The glossary's *dialog* and *game test*
  entries now point at `commands/dialogs.md` and `commands/game-tests.md`,
  and its *function* and *macro function* entries at
  `commands/functions-and-macros.md` — re-read those four as a set, because
  the pages either side of the split say different things now. Terms this
  part introduced and the glossary does not carry: **permission atom**,
  **permission set**, **unattended command**, **frame** (in the
  execution-engine sense, which is deliberately *not* a stack frame),
  **staging buffer** and **batch** (a game-test batch, which is an
  environment). And session K's finding stands: the glossary's *permission*
  entry described the integer design, and while this session removed the
  integer from every page, the glossary is generated by nobody and was not
  touched.

  **For session P (the close).** `python tools/check_lanes.py` now reports
  **537 participants, 0 disagreeing with the key and 0 unkeyed collisions,
  corpus-wide** — the gate session A wanted can be turned on unconditionally,
  which is one line in `tools/deploy.sh`. Twenty-six rows were added and one
  collision is recorded in `TEMPLATE.md` and deliberately **not** drawn:
  `ExecuteCommand` names two unrelated classes (the `/execute` command, keyed
  `ExecC`, and the leaf task in `commands/execution/tasks`), which the lane
  key cannot distinguish because it resolves simple names — so
  `the-execution-engine` names the task in prose and never as a lane. If a
  later page needs the task as a lane, the key needs a qualified-name column,
  not a new row.

  **The `execute store` sink count was wrong in the corpus and is fixed.**
  `scoreboard-and-data` said `execute store` has two sinks "which are exactly
  the two models here"; `ExecuteCommand.wrapStores` builds **three** — score,
  boss bar (value or max, sharing the score sink's implementation), and the
  three data providers. This is the fourth session running in which redrawing
  a page found an error in a *count*, and the third in which the wrong count
  was load-bearing for a sentence's argument rather than incidental to it.

  **Two rulings this part needed and did not get its own page for.**
  Advancements' client screen stays a section (the reasoning is in
  [plan.md](plan.md)); and `scoreboard-and-data` stays one page, so the
  question of whether the scoreboard belongs to Part XIII at all — §1 asked
  it — is answered by R6 and by the page's own trace, which is a command.
  The boss bar and the statistics remain the only two candidates for a part
  that does not exist, and neither has an owner page in the corpus.

- **Session O (Reference).** Four things for session P. **The tier is
  name-verified now**: `verify_names.py` checks every page under
  `src/reference/` except the eight `gen_reference.py` views (recognised by
  their *Do not edit by hand* header) and the two indexes — so a hand-kept
  reference page fails the build like a system page, and the sixteen bare
  names the four catalogues carried are fixed. **The reference README is a
  landing page** with a table whose last column says which parts' landing
  pages link each page; if session P's cross-corpus sweep changes a landing
  page's *Reference this part uses*, that column is the place it must also
  change. **The glossary is hand-kept, and eleven entries were added**
  (`authority`, `event loop`, `submit node`, and the eight sessions M and N
  named); the R5 clause about generating it is closed — no page declares
  its terms, and seeding ninety pages by hand is the same work as keeping
  the page. **`lectures.md`** still says nothing about Reference beyond the
  Part II note that `math-and-primitives` is not a lecture; session P should
  add one sentence at the top: nothing in Reference is watched. Also: the
  treemap hatch bug is fixed (`gizmos`, `realms`, `references` hatch as
  whole groups), and `the-connection` had a wrong example — `handlePing`
  hops; the handlers that do not are the eight now listed in `threads.md`.

---

## 9 · The pass-3 charter, rulings, protocol and schedule (archived from plan.md, 2026-09-03)

**Goal:** a reader opens any page and wants to keep reading, and a viewer of
the series can see, from the site alone, what order to watch in and why.
Pass 2 made the corpus true; pass 3 makes it a book. Length is still not the
concern — pass 5 cuts — but *shape* is, everywhere: the shape of the site,
of each part, of each page, and of each figure.

### What is wrong today

Written down so the sessions aim at it. The first four are the owner's,
from reading the live site; the rest are the notebook's, from eleven
sessions of pass 2.

1. **Every page is the same page.** Seventy-nine pages, seven identical H2s
   in identical order (*Responsibility · The data it owns · When it runs ·
   The trace · Interfaces · Invariants and surprises · Where to look*). The
   template served pass 1, which needed a checklist; it now guarantees
   monotony. Its two worst sections are the bullet walls — the data section
   (a class name followed by fifteen field names) and the invariants section
   (twelve bold-led bullets) — and every page has both.
2. **Diagrams fail to render.** A mermaid sequence diagram ends a statement
   at `;` and treats `#` as the start of an entity code, and the pass-1
   style of writing arrow labels as *"call — what it decides; what happens
   next"* put semicolons into dozens of diagrams. Each shows as *Syntax
   error in text mermaid version 11.6.0*. The planning session built
   `tools/check_mermaid.js` — it parses the *built* HTML with the site's own
   mermaid, so its verdict is the browser's — fixed the failures, and made it
   a gate in `tools/deploy.sh`. A diagram that does render is still scaled
   down to the column, and a nine-lane trace is unreadable there;
   `diagram-zoom.js` (planning session) opens any diagram at viewport size on
   click.
3. **Tables scroll sideways with room to spare.** mdBook's reading column is
   750px and cells pad 20px a side, so a four-column table of identifiers
   overflowed on any screen. `custom.css` (planning session) widens the
   column to 1100px for tables, diagrams and figures while capping prose at
   800px, and lets identifiers wrap inside cells.
4. **The sidebar is a flat list of eighty pages.** Sections now fold
   (`[output.html.fold]`, planning session) so only the current part is
   open; the parts themselves are not yet clickable because they have no
   page. Every part gets a landing page in this pass.
5. **The shape of each part is invisible.** The notebook found Part IV is a
   conveyor, Part V a hub, Part VI a ladder, Part IX one pipeline and three
   passengers, Part X a hub and spokes, Parts XI and XII a substrate under a
   pipeline, Part XIII a stack — and nothing on the site says so. Pages that
   are reference material (`math-and-primitives`, `level-data-and-rules`,
   the appendix's tables, the catalogues inside `synched-entity-data`,
   `attributes` and `hud`) sit in the lecture sequence, and the appendix is
   numbered as if it could be watched.
6. **Pages carry two or three lectures**, and the lecture boundary and the
   page boundary disagree: the split table in [pass2.md](pass2.md) has
   nineteen confirmed-not-executed entries. Several ideas have no owner or
   four (the prediction ledger had four until session H; authority has
   three; the event loop is explained in four parts).
7. **The front and back of the book were never revisited.** The introduction
   is three bullets from pass 1; the maps are four generated tables; the
   reference README is a list.
8. **Figures are all one kind.** Seventy-six sequence diagrams and one
   flowchart. The notebook names a dozen that are the wrong shape — state
   machines, filter cascades, trees, graphs and pipelines drawn as
   conversations — and a handful of pages whose real figure is a picture no
   mermaid type draws.

### The rulings

Decided now, so that sixteen sessions build on one frame rather than each
re-deciding it. A session may overrule a ruling with the page in front of
it, but writes down that it did, and why, in the log.

**R1 · Three tiers, and the appendix dissolves.** The site is *Parts*
(numbered I–XIII, watched in order), *Maps* (the atlas: looked at once), and
*Reference* (catalogues: looked up). The appendix stops being Part XIV:
`naming-drift` and `glossary` move to Reference; `out-of-scope-tour` becomes
the closing page of Part I as *what this book skips* — a viewer should know
the boundary before investing in thirteen parts, and its treemap wants to
live beside the maps. No part is renumbered and no new numbered part is
created in this pass; where a part has two halves (Part XII's terrain and
structures, Part VII's two tiers) the landing page says so.

**R2 · The template becomes a menu of shapes.** `TEMPLATE.md` is rewritten
(session A, from two pilots) from a skeleton into a menu. What every page
keeps: the title; the verified line with the part and the scenario; an
**opening paragraph that starts inside the scenario and ends on the hook** —
the one observable, surprising, true thing the page explains (the pass-2
findings are the hook bank: the block that comes back and vanishes again,
lava random-ticking twice, the watchdog kill that saves nothing, the
minimized window rendering frames nobody sees); a **cast** of at most eight
classes with role and thread, as a small table or in the narration, in place
of the field inventories (the exhaustive lists go to the class index, which
already exists); at least one figure; *Where to look* and the rules footer.
Everything between is the page's own, with headings that say what the
section says (*The two flushes*, *Who is told, and when*), never what
template slot it fills. The shapes:

| shape | for | its figure |
|---|---|---|
| **the trace** | one scenario through the system | a sequence diagram, narrated as prose in the order things happen, with each surprise placed where it happens |
| **the pipeline** | stages that hand off | a flowchart of stages at the top; a section per stage: what comes in, what is decided, what goes out |
| **the state machine** | phases and transitions | `stateDiagram-v2`, transitions labelled with the packets or events; a section per state; what can go wrong in each |
| **the policy** | who is told what, when | a decision table or flowchart per decision; the surprises are its rows |
| **the comparison** | two or three paths that differ | a table with the paths as columns; one diagram per path, or one with `alt` |
| **the vocabulary page** | the objects and their relations | a figure of the data (a containment or class diagram, or a flowchart), then a tour by object, grounded by one small trace |
| **the pattern** | one idea, many instances | the instances as a table; one instance traced |
| **the landing page** | a part | the part's shape as a figure of its pages |

Devices any page may use and none must: the myth table (*what the forum
says* / *what the decompile does*); *the number* (a count with its owner,
set off on its own line); the *for a 1.21-era reader* box (a styled
blockquote, replacing the names-you-will-hunt-for bullets); a
question-and-answer section where the surprises are answers to questions
players ask; the same trace seen from the other side (a mirrored
client/server pair, as `environment-attributes-and-timelines` already does);
the tick-boundary bar (`Note over` marking every tick crossed — session D's
rule) and the explicit *no reply* annotation (session H's).

The budgets, which are the enforceable part: a bulleted list holds parallel
items of at most two sentences, at most seven of them, and a page has at
most three lists; anything explanatory is prose; anything enumerative beyond
seven is a table, or Reference; every section has a figure or a subsection
before it passes forty lines; *Interfaces* survives only as a row of the
cast table or one sentence (what crosses the network, and as which
packets). A page is not done until it reads differently from its
neighbours.

**R3 · Every part has a landing page**, `src/systems/<part>/README.md`,
linked from the sidebar as the part itself: one paragraph on what the
system is and the one thing a player would recognise it by; the part's
shape as a figure of its pages (the conveyor, the hub, the ladder — pages
as nodes, what each hands to the next as edges); *before you start* — the
earlier pages this part assumes, by link; *watch in this order* — the
part's lectures with a one-line teaser each, which is the draft lecture
order `lectures.md` assembles; and the Reference pages the part uses. Under
a hundred lines, no trace. The sidebar folds to the current part; the
landing page is what the fold opens on.

**R4 · Figures.** The standing convention becomes: mermaid in the page for
anything mermaid 11.6.0 draws (`sequenceDiagram`, `flowchart`,
`stateDiagram-v2`, `classDiagram`, `timeline`, `block-beta` — the checker is
the arbiter of what the site's version accepts); **generated SVG** from
`tools/` for the maps and for figures no mermaid type draws (a treemap, a
bar chart, a tree with numbers on it), inlined with mdBook's `{{#include}}`
so it inherits the theme; **never a hand-drawn or raster image** — a figure
has to be regenerable on the next version, like a table. Every diagram is
checked by `tools/check_mermaid.js`, which is part of `tools/deploy.sh`.
Lanes: a lane is a class name abbreviated by the initials of its CamelCase
words, at least two letters, one meaning corpus-wide — `SGPL`, `CPL`, `MC`,
`MS`, `SL` — recorded in a lane key in `TEMPLATE.md` that session A writes
and every later session extends; collisions (`GR`, `CL`, `LX`, `SS`, `TP`,
`C`, `CM`, `PE`) are resolved by lengthening the later claimant. A short
whole word is allowed for a lane that is not a class (`Wire`, `Disk`,
`Main`).

**R5 · The Reference tier grows, and the rule for it is "would a viewer
pause the video to read this".** A table a viewer would pause on belongs in
Reference with the page linking to it. Members now: `math-and-primitives`
and `level-data-and-rules` (moved out of Parts II and IV), `naming-drift`
and `glossary` (out of the appendix), `threads` (kept; `anatomy` trims to
the four threads a viewer must hold), and the catalogues extracted from
lecture pages — the serializer list in `synched-entity-data`, the attribute
list in `attributes`, the HUD gate table `hud` compressed to prose, the
`EnchantmentHelper` hook table, the structure-piece families. Generated
where the decompile can generate them (`gen_reference.py` gains views);
hand-kept otherwise, and re-swept in pass 4. The glossary becomes generated
if session O finds a cheap per-page term declaration; otherwise it is
re-swept. The maps become the atlas: figures with prose, not tables alone.

**R6 · Where the shared ideas live.** *Authority*
(`Entity.isLocalInstanceAuthoritative` and its three siblings) gets its own
short page at the head of Part VI after `entity-anatomy`, in the comparison
shape — a mob and a player each taking one step, on each side — and Parts
VIII, IX and X link to it instead of re-teaching it. *The two loops* (the
tick cadence, the frame/tick interleave, the per-frame packet drain) become
a figure in `anatomy`, so Part IX's dependency on the client is a dependency
on Part I; `the-client-loop` stays in Part X as its hub. *The event loop*
(`BlockableEventLoop`, `TickTask`, `managedBlock`) is owned by `server-tick`
as a named section and linked from everywhere else. *The two update
channels* (shape versus neighbour updates) become one flowchart of
`Level.setBlock`'s tail, drawn once in `blocks-and-states` and reused by
reference. *`Component`* gets a Part II page — the object is a foundation,
not a networking detail — so `text-and-fonts` and `chat-and-signing` stop
sharing a subject. *The data-driven type pattern* (a registry of
codec-loaded element types: loot functions, features, density functions,
placement modifiers, dialogs, tests) gets a Part II page as the part's
closer, and `dialogs-and-tests` may then split without losing its argument.
*The scoreboard* stays in Part XIII (its trace is a command) and Part IV's
landing page points at it as level state. *`prediction-and-acks`* stays in
Part X; the Part V pair (`block-interaction`, `block-breaking`) gets one
shared preamble that states the ledger's contract in three sentences and
links forward. *`density-functions`* opens Part XII; *`the-frame`* opens
Part XI, then the substrate (`the-window`, `blaze3d`), then the pipeline.
*`environment-attributes-and-timelines`* stays in Part IV and is placed
early in the lecture order. The cross-part lecture order stays I → XIII as
numbered; `lectures.md` is assembled from the landing pages by session P.

**R7 · What pass 3 writes, and what it does not.** It executes the splits
and merges the notebook confirmed (they are in the schedule, per part); it
writes the owner pages in R6; and each part session may add **at most one**
of the coverage pages the pass-2 inventories found (post-processing,
block-entity rendering, item models, how a server dies, the spear, drawing
a bow, status effects, the permission model, the function model,
`GameTestHelper`, the selector grammar) — the rest go to the coverage queue
in [pass3.md](pass3.md) §7, discharged by session P if there is budget and
otherwise carried forward, written down. Pass 3 may drop material from a
page only by moving it (to Reference, to another page) or by logging the
cut in [pass5.md](pass5.md) with the reason. And **every page pass 3
rewrites is listed in [pass4.md](pass4.md)** with the claims the rewrite
introduced (hooks, redrawn orderings, new sections), because pass 4 checks
those hardest.

**R8 · URLs live forever.** Every moved or renamed page gets an
`[output.html.redirect]` entry in `book.toml`, as the X/XI split did.
`llms-full.txt` follows `SUMMARY.md` and needs nothing.

### Session protocol

One session = one part (large parts may take two; the schedule says
which), except the four site sessions (A, B, O, P). Each part session:

1. **Read** this charter, `CLAUDE.md`, `TEMPLATE.md` (the menu and the lane
   key), the part's notes in [pass3.md](pass3.md) — grep the part in every
   section, not just §1 — the part's rows in [pass2.md](pass2.md)'s split
   table and its hand-off section (the hook bank and the on-spec material),
   and the pages.
2. **Rule before editing.** Write the part's shape, the page list after
   splits/merges/moves/extractions, each page's shape from the menu and its
   hook, into the session's log entry *first*. Decisions first, so the work
   can be checked against them.
3. **Restructure.** Create, split, merge and move files; `SUMMARY.md`;
   redirects; cross-links (grep the corpus for every old link).
4. **Reshape.** Rewrite each page in its shape, hook first, figures redrawn
   where the notebook says the shape is wrong, lanes from the key, the
   bullet budget kept. Agents may draft pages in parallel given the old
   page, the shape, the notebook's notes, the menu and the rules — but the
   session **diffs every draft's claims against the old page** before
   accepting it: a fact reworded is a fact changed until proven otherwise,
   and pass 4 is a net, not a licence. Anything an agent adds that the old
   page did not say goes on the pass4.md list.
5. **The landing page**, and the part's lecture list in `lectures.md`.
6. **Verify and ship.** `python tools/verify_names.py` ·
   `node tools/check_mermaid.js` · `mdbook build` clean · class index
   regenerated if pages moved · commit `pass 3, Part N: <summary>` · deploy.
7. **Log and hand off.** The session log below; [pass4.md](pass4.md) (pages
   rewritten, claims introduced, diagrams redrawn); [pass5.md](pass5.md)
   (wording debt, cuts); [pass3.md](pass3.md) (anything structural found for
   a *later* session — a cross-part consequence, a coverage-queue entry, a
   lane).

Three lessons carried from pass 2 that bite here too: **suspect the tool
once before rewording the page** (the checker, the verifier and the
generators all had bugs in pass 2); **grep the corpus for every moved
claim** — a fact that moves to a new owner page must be removed from its
old hosts, not duplicated; and **a landing page is a claim about order**,
which pass 4 must check like any other.

### Schedule

Tick as done. Sessions A, B, O and P are the site; C–N are the parts, in
sidebar order.

- [x] **Session A — The frame.** *(done 2026-09-02)* Two pilot pages reshaped end to end —
  `tickets-and-loading` (a policy page: eleven lanes today; wants a
  flowchart and a small state diagram) and `protocol-phases` (a state
  machine) — and then `TEMPLATE.md` rewritten from what worked: the menu,
  the devices, the budgets, the lane key. The introduction rewritten as a
  front door (what the game is as a program, in a page; how the site is
  read; the three tiers; the rules; `llms-full.txt`). The landing-page spec
  proven on Part I's. `lectures.md` reduced to a skeleton the parts fill. A
  lane linter if it is cheap (a lane not in the key fails).
- [x] **Session B — Maps: the atlas.** *(done 2026-09-02)* `map_source.py` grows an SVG output
  and the maps become figures with prose: the jar as a treemap by package,
  coloured client-only versus shared (which is also the *two jars* figure
  the introduction wants); the biggest classes and the fan-in hubs as bars;
  the widest hierarchies as trees; the threads as a figure beside
  `reference/threads.md`. This session builds the figure pipeline
  (`{{#include}}`, theming through `custom.css`) every later session
  reuses, which is why it comes second.
- [x] **Session C — Part I Anatomy · Part II Foundations.** *(done 2026-09-02)* `anatomy` split
  into a startup diagram and a steady-state one, the two-loops figure, the
  threads table trimmed to four rows; `out-of-scope-tour` joins Part I as
  *what this book skips*, with the treemap. Part II: `math-and-primitives`
  to Reference; `codecs-nbt-json` leads; the registries/tags/resources knot
  cut where §1 says (state the freeze rule, pay it off in tags); the
  `Component` page and the data-driven-types page written or ruled out with
  the pages open; `resource-system`'s two traces settled as one lecture
  with a coda, or two.
- [x] **Session D — Part III The server.** *(done 2026-09-02)* Lifecycle last and reframed as
  *how a server dies* (three endings, one diagram; startup gets its own
  diagram with the JVM main thread as a lane); the event-loop section in
  `server-tick`; `server-level-tick`'s guard flowchart beside its trace;
  `players-and-sessions` as a join trace plus a three-path comparison, its
  nine-lane diagram split in two.
- [x] **Session E — Part IV The world.** *(done 2026-09-02)* The conveyor made explicit:
  `chunk-anatomy` first, then the four pipeline pages handing off;
  `block-ticks-and-fluids` and `game-events-and-poi` each split in two;
  `level-data-and-rules` to Reference; the pyramid drawn; the light batch
  drawn; `tickets-and-loading` from the pilot re-checked. Probably two
  sessions.
- [x] **Session F — Part V Blocks.** *(done 2026-09-02)* The update-channels flowchart in
  `blocks-and-states`; `block-interaction` + `block-breaking` as one lecture
  in two halves with the shared preamble; `redstone` split three ways
  (signal and dust · pistons and block events · diodes, comparators and the
  observer); `block-entities` kept as the part's model page.
- [x] **Session G — Part VI Entities.** *(done 2026-09-03)* The authority page; the serializer
  and attribute catalogues to Reference (generated); `entity-lifecycle`'s
  spawner as a filter-cascade flowchart; `ai-goals-and-brains` ruled (three
  lectures — pathfinding is the strongest); the non-living `hurtServer` gap
  ruled (section, sibling page, or Reference table).
- [x] **Session H — Part VII Items and inventories.** *(done 2026-09-03)* The two-tier landing
  (vocabulary, then three engines); `loot-tables` split into *contexts and
  predicates* plus loot as its worked example; enchantment acquisition out
  of `enchantments`; the *drawing a bow* trace as the use pipeline's second
  half; item-model ownership settled with session L.
- [x] **Session I — Part VIII The player.** *(done 2026-09-03)* `player-anatomy` split into the
  reference half and the two-phase-tick trace; status effects out of
  `hunger-xp-and-effects`; the spear ruled (own lecture or
  `the-sword-swing`'s coda); `the-sword-swing`'s damage pipeline drawn as a
  flow over one number.
- [x] **Session J — Part IX Networking.** *(done 2026-09-03)* `the-connection` +
  `packets-and-stream-codecs` taught as one lecture with one round-trip
  diagram (merge or shared trace — ruled with the pages open);
  `protocol-phases` from the pilot; `what-the-client-is-told` as a policy
  page with its `ClientLevel` sections handed to Part X; `chat-and-signing`
  with the adversary table. Part IX's three borrowed facts replaced by links
  to Parts I and III.
- [x] **Session K — Part X The client.** *(done 2026-09-03)* The hub-and-spokes landing, each
  spoke named by its cadence; `sound` split (the engine · what makes a
  sound happen); the GUI stack as the part's one internal pipeline,
  `the-gui-render-tree` drawn as a tree; `hud`'s gate table to Reference;
  `prediction-and-acks` as a two-column state diagram;
  `debugging-the-running-game` placed.
- [x] **Session L — Part XI Rendering.** *(done 2026-09-03)* Frame → substrate → pipeline;
  `the-window`'s retry loop as a flowchart; `models-and-atlases`'
  fan-out/barrier drawn; the lane collisions fixed; one of post-processing
  / block-entity rendering / item models written (R7), the others queued.
  Probably two sessions.
- [x] **Session M — Part XII World generation.** *(done 2026-09-03)* `density-functions` first,
  its three-graphs figure as generated SVG or a before/after pair;
  `structures` split into placement and jigsaw beside
  `hand-built-structures`; `worldgen-pipeline`'s nested cell loop drawn as
  nesting; the two halves (terrain · structures) on the landing page.
- [x] **Session N — Part XIII Commands and data packs.** *(done 2026-09-03)* The stack landing
  (parse → execute → what commands are for); the permission model out of
  `brigadier-and-commands`; `execution-and-functions` split into the engine
  and the function model, the queue drawn as snapshots; advancements'
  client screen ruled; `dialogs-and-tests` split if the Part II pattern
  page exists; the scoreboard stays.
- [x] **Session O — Reference.** *(done 2026-09-03)* The moved pages redirected and reframed;
  the extracted catalogues generated (`gen_reference.py` views for
  serializers and attributes at least); the glossary generated or re-swept;
  the reference README as a real page; the class index regenerated;
  `threads` beside its figure.
- [ ] **Session P — The lecture order and the close.** `lectures.md`
  assembled from the landing pages with the cross-part dependencies stated;
  the parts-dependency figure in the introduction; the cross-corpus sweep
  (lane key complete, links, every landing page's *before you start* true,
  redirects); the coverage queue discharged as budget allows; the
  distribution of page shapes checked (if half the corpus chose the trace,
  the menu failed); pass 4's charter written; pass 3 closed.

### Hand-off rules

Three files, three kinds of note. [pass3.md](pass3.md) — structural, for a
later pass-3 session (its §7 is the coverage queue). [pass4.md](pass4.md) —
factual: what pass 4 must re-check, per page. [pass5.md](pass5.md) —
wording debt and cuts. Anything left for later is written when it is
found, not at the end.

---

## 10 · The pass-3 session log (archived from plan.md, 2026-09-03)

- **2026-09-02, planning session** — pass 2 closed: its charter, protocol
  and session log archived into [pass2.md](pass2.md); this plan rewritten
  for passes 3–6 (the second fact-check inserted as pass 4; polish and the
  owner's read renumbered). Pass 3 chartered above with eight rulings and
  sixteen sessions. Site mechanics that no ruling depends on were fixed at
  once: `[output.html.fold]` collapses the sidebar to the current part;
  `custom.css` widens the column for tables and diagrams and caps prose at
  800px; `tools/check_mermaid.js` parses every built diagram with the
  site's own mermaid and is a gate in `tools/deploy.sh` — **41 of the 77
  diagrams were failing**, every one from a `;` in a label, and three more
  were silently truncated at a `#`; all fixed with syntax-only edits (75
  lines in 40 pages, `;` → `#59;` and `#` → `#35;`).
  [pass4.md](pass4.md) and [pass5.md](pass5.md) opened; `CLAUDE.md`,
  `README.md`, `TEMPLATE.md` and `lectures.md` brought current.
  **Second half, on two owner notes.** Diagrams that render are still too
  small to read: `diagram-zoom.js` opens any diagram at viewport size on
  click, on the page's own background. And the fact base was widened
  *before* pass 3 rather than after it: session K had recorded one question
  the decompile could not settle because Brigadier is not in the tree, and
  that was the visible tip of a larger gap — pass 2 took every claim about
  Brigadier, DataFixerUpper and authlib on trust, and every data-driven claim
  (atlases, fonts, post-effect chains, shaders) against a tree that held the
  jar's `data/` but not its `assets/`. Now staged, all gitignored: the jar's
  `assets/` minus textures beside `data/`; Brigadier 1.3.10 and
  DataFixerUpper 10.0.21 from their published source jars; authlib 9.0.75
  decompiled from the launcher's jar with the PvP mod's Vineflower — by the
  new `tools/fetch_libs.sh`. `verify_names.py` indexes `reference/libs/` and
  twenty-seven allow-list entries were retired, so library names are now
  checked at member level; all 19,745 names still resolve. The `execute
  store` question is answerable and is on pass 4's list. Also noted: this
  machine has 26.3 snapshots 8 and 9 installed, on authlib 10.0.77 and
  Brigadier 1.3.11 — the 26.3 risk is near, and `fetch_libs.sh` carries the
  versions to bump.
- **2026-09-02, session A — the frame.** *Rulings, written before editing.*
  **`tickets-and-loading` takes the policy shape.** Its questions are
  decisions — what level a chunk gets, which graph answers which question,
  when a holder is promoted or demoted, what a player is sent and when a
  ticket dies — so the page becomes one figure per decision: a flowchart of
  ticket → level → status → future, a `stateDiagram-v2` of the four
  `FullChunkStatus` values, three decision tables, and one six-lane trace of
  the walk east kept as the grounding. Hook: two graphs share one ticket
  store, so a chunk can be entity-ticking by holder status and tick nothing.
  The field inventories go (logged in pass5.md); the nine-row ticket table
  stays, because nine is past the list budget and the table is the
  reference. **`protocol-phases` takes the state-machine shape.** Two
  `stateDiagram-v2`s — the five `ConnectionProtocol`s with the terminal
  packets as transitions, and `ServerLoginPacketListenerImpl.State` with
  its orphan — one small sequence diagram for the encryption handshake
  alone, one flowchart for the configuration task queue; a section per
  phase ending in what disconnects it. Hook: the `ServerPlayer` is built
  after the client has acknowledged the end of the phase named for
  preparing it. **`TEMPLATE.md`** becomes the menu (R2) with the two
  pilots named as its worked examples, the devices, the budgets, the
  mermaid rules the checker enforces, and the lane key — seeded with the
  hubs whose spelling is already the majority, the two pilots' lanes and
  Part I's; one-word classes take a fixed prefix of two or more letters
  (`Conn`), not one initial. **`tools/check_lanes.py`** is the lane linter:
  every key expansion must be a class in the decompile (hard), a lane in
  the key must mean the same class on every page (report-only until session
  P; `--strict` fails; `--pages` scopes it to a part). **The introduction**
  becomes the front door with one figure of the two programs and the wire;
  the two-jars treemap (B) and the parts-dependency figure (P) are named
  as placeholders, not drawn. **Part I's landing page** is written as the
  R3 proof: its figure is a root, `anatomy` handing a thread to every part.
  **`lectures.md`** becomes a skeleton, one section per part, Part I filled.
  No page moves this session, so no redirects.
  *Done.* Both pilots rewritten and shipped: `tickets-and-loading` at 330
  lines with a flowchart, a state diagram, three decision tables, a six-lane
  trace (was eleven) and a *questions players ask* close;
  `protocol-phases` with two state diagrams, a three-lane handshake, the
  task-queue flowchart and a section per phase. The reshaping surfaced one
  pass-2 error: the keep-dimension-active flag is on the player
  *simulation* ticket, not the loading tickets (pass4.md has it).
  `TEMPLATE.md` is the menu, with the two pilots as its worked examples;
  `tools/check_lanes.py` is written and in `deploy.sh` (key verified
  against the decompile, page drift report-only until session P) and
  generates `src/reference/lanes.md` so readers see the key; the
  introduction is the front door with the two-programs figure; Part I's
  landing page is the R3 proof and the sidebar's Part I now opens on it;
  `lectures.md` is the skeleton. 84 diagrams checked, 0 failed; all names
  resolve; hand-offs in pass3.md §8, pass4.md and pass5.md.
- **2026-09-02, session B — maps: the atlas.** *Rulings, written before
  editing.* **One generated directory.** Everything a page includes that a
  tool wrote lives in `src/generated/` — the SVG figures and the markdown
  tables — and nothing there is hand-edited; `python tools/map_source.py`
  with no argument rewrites all of it, so regenerating on the next version
  can never clobber prose. `llms_full.py` expands the markdown includes and
  replaces an SVG include with a one-line note, so agents get the tables.
  **The figure pipeline** is `<figure class="map">` + `{{#include
  ../generated/<name>.svg}}` + `<figcaption>`, with the SVG carrying only
  classes (`svg.mapfig`, `.shared`, `.client`, `.skip`, `.lib`) and all
  colour, font and theme in `custom.css`; text is `currentColor`, so the
  five mdBook themes and the zoom overlay all read. **The atlas is four
  maps and a front page**, each a figure with prose then the table it
  summarises: *where the code is* (`packages`: the jar as a treemap of
  packages, area by lines, colour by jar, the out-of-scope packages
  hatched — which is also the two-jars figure the introduction wanted and
  the treemap `out-of-scope-tour` wants in session C); *where the mass is*
  (`biggest`: bars); *what everything imports* (`fanin`: bars, with the
  library classes the old table could not see — `Codec` was not counted —
  now counted and marked); *what extends what* (`hierarchy`: trees with
  numbers on them for the roots the parts teach, and the table split into
  class roots and interface roots, because the old table's top was mixin
  interfaces). File names and URLs do not change (R8); sidebar titles do.
  **The threads figure is mermaid** (R4: mermaid for what mermaid draws): a
  flowchart beside `reference/threads.md` of every thread a lecture leans
  on and the three ways work crosses between them — a posted task, a
  completed future, a hopped packet handler — drawn from the pass-2
  verified table, no new fact. **The verifier stops skipping `maps/`** now
  that the atlas has prose; it skips `generated/` instead. The atlas pages
  say how each number was counted (a class is one `.java` file, a line is a
  line of decompiled source, client-only is absence from
  `server-classes.txt`, fan-in is import statements), because pass 4 will
  re-derive them.
  *Done.* `tools/map_source.py` rewritten: it writes `src/generated/` —
  six markdown tables and seven SVGs (the treemap, two bar charts, four
  trees) — and `deploy.sh` runs it first, so the atlas cannot drift from
  the decompile. Rewriting it found two bugs in the old view: nested
  classes and records were invisible to the hierarchy parser (every count
  moved; `Goal` went from 70 to 200 because two thirds of its subclasses
  are nested in the mobs that use them; `Packet` appeared at 232), and the
  import count ignored `com.mojang.*`, which hid the best fact on the map:
  `Codec` is the second most-imported class in the game. The five atlas
  pages are prose over figures over tables — *where the code is*, *where
  the mass is*, *what everything imports*, *what extends what*, and a front
  page that says how every number is counted. The treemap is in the
  introduction as the two-jars figure; `reference/threads.md` has its
  mermaid figure of the eight threads and the three ways work crosses
  between them; `verify_names.py` now checks the atlas prose (all 19,895
  names resolve); `llms_full.py` expands includes; the figure recipe is in
  `TEMPLATE.md` and `CLAUDE.md`. Rendered and looked at in the light and
  navy themes with headless Chrome before shipping. 85 diagrams, 0 failed.
  Hand-offs in pass3.md §8 (session C's treemap include, the `SKIPPED`
  list), pass4.md (every number, the tool itself, `entity-anatomy`'s
  corrected 193) and pass5.md.
- **2026-09-02, session C — Part I Anatomy · Part II Foundations.**
  *Rulings, written before editing.* **Part I is a root of two pages.**
  `anatomy` keeps the trace shape but takes **two figures**: a startup
  sequence (the JVM main thread becoming the Render thread, the Server
  thread born in `MinecraftServer.spin`, the in-process channel) and the
  two-loops figure R6 asks for — a flowchart of the frame loop and the tick
  loop side by side with the packet drain in each, which Parts III, IX and
  X then link to instead of restating. Hook: the client walks the same
  handshake against the server in its own process as against one across
  the world, and the one thing that leaks between them is a setting —
  pause is decided on the client and enforced by the server, so a
  published LAN world never pauses. The threads table trims to the four a
  viewer must hold (Render, Server, Netty, workers) and defers the rest to
  `reference/threads.md`, which already carries every row; the situational
  paragraph goes with it. The invariants that belong to Part III (the
  `haveTime` budget, sprinting, the stale `TickTask`, the overload
  warning, the flush bracket) are already owned by `server-tick` and are
  cut here to a link, logged in pass5.md as moved. **`out-of-scope-tour`
  becomes `systems/anatomy/what-this-book-skips.md`** (R1; redirect from
  the appendix URL), opening on the treemap with the skipped packages
  hatched, a section per skipped thing as today, and the four-way rulings
  list compressed to one table. Hook: vanilla's own content is a data pack,
  and the generator that writes it ships in the server jar and is called
  by the running game. **The appendix dissolves now, not in session O**:
  `naming-drift` and `glossary` move to `src/reference/` with redirects
  and their headers corrected, because a Part XIV of two look-up pages is
  not a part (R1); session O reframes them. **Part II is a stack**, drawn
  on its landing page bottom-up: codecs (how anything becomes data) →
  registries (how anything gets a name and a number) → the resource system
  (where data comes from and when) → tags (data reaching into code) → data
  components and text components (data on an object) → the data-driven
  type pattern (the closer, which every data-pack file is an instance of).
  `math-and-primitives` moves to `src/reference/` (redirect; header
  reframed; the notebook's coordinate-spaces figure left for session O).
  Page shapes and hooks: **`codecs-nbt-json`** leads and takes the
  **comparison** shape — one `ItemStack` four ways is four paths that
  differ, so a table with the paths as columns and one short diagram per
  path replace the ten-lane conversation; hook: the click on a chest slot
  sends the server no item data at all, only a checksum per component.
  **`identifiers-and-registries`** keeps the **trace** shape with its two
  diagrams (the notebook calls them the model for the corpus); hook: the
  wire id of a diamond sword is the line number of its registration in
  `Items`; it states the freeze rule (contents never change; tags and
  components do) without justifying it. **`resource-system`** is one
  lecture in the **pipeline** shape — discover, snapshot, prepare in
  parallel, apply in order, finish or roll back — with the prepare/apply
  lattice drawn as a flowchart with three listeners explicit (the
  notebook's clearest wrong-shape case), F3+T as the grounding trace and
  `/reload` as a comparison coda (what differs, as a table); hook: a reload
  that fails does not find the bad pack, it deselects every pack and
  reloads again. **`tags`** keeps the **trace** shape and pays the freeze
  rule off; hook: a frozen registry's contents cannot change, and yet
  `/reload` changes what `#minecraft:logs` contains — the tag table is the
  one part of a frozen registry that is swapped, in three ordered steps
  with no lock. **`data-components`** takes the **vocabulary** shape — a
  figure of prototype, patch and map, a tour by object, the enchanting
  trace cut to the grounding so Part VII keeps the enchanting table; hook:
  an item's prototype is built on every reload with the world's registries
  in hand, not in its constructor, which is why a stack cannot be decoded
  before the first reload. **`text-components`** is written (R6): the
  **vocabulary** shape — contents, style, siblings as a figure; the seven
  contents kinds as the table; one small trace of a death message crossing
  the wire as a translation key and being worded on the client; hook: the
  client receives the death message before anyone knows what it says. The
  `Component` section of `chat-and-signing` moves here and that page links
  (grep-the-corpus rule); `text-and-fonts` points here. **`data-driven-types`**
  is written (R6) as the part's closer in the **pattern** shape: the idea
  (a `type` field is a lookup in a registry data packs cannot extend), the
  instances as a table drawn from every `Registry<MapCodec<? extends …>>`
  and every `…Type<?>` registry in `BuiltInRegistries`, one instance traced
  from JSON to object; hook: `type` is the most important key in a data
  pack. `dialogs-and-tests` keeps its own statement of the pattern until
  session N links here. Lanes: 45 rows added to the key before drafting;
  `CH`, `MC`, `IS`, `PE`, `TP` collisions in Part II resolved by lengthening
  the later claimant (`CHelp`, `IStack`, `PEnc`, `TagP`); expansions are the
  bare class name, thread in the cast. Agents draft in parallel; every
  draft's claims are diffed against the old page before acceptance.
  *Done.* Part I: `anatomy` rewritten as a trace with two figures — the
  startup sequence (seven lanes, the JVM main thread becoming the Render
  thread, the Server thread born in `spin`) and the two-loops flowchart
  Parts III, IX and X now link to — the threads table cut to four rows
  with `reference/threads.md` carrying the rest, the Part III invariants
  cut to a link; `out-of-scope-tour` became `what-this-book-skips` in Part
  I with the treemap and the rulings as one table; `naming-drift` and
  `glossary` moved to Reference and the appendix is gone from the sidebar
  (four redirects). Part II: seven pages in a stack, drawn on a new
  landing page — `codecs-nbt-json` leads in the comparison shape (a
  four-column table and four short diagrams for the ten-lane one),
  `identifiers-and-registries` keeps its two traces and states the freeze
  rule, `resource-system` is a pipeline with the prepare/apply lattice
  drawn and `/reload` as a comparison table, `tags` pays the freeze rule
  off, `data-components` is a vocabulary page with the enchanting trace
  cut to its Part II core, and two R6 pages were written from the decompile:
  `text-components` (the death message worded on the client) and
  `data-driven-types` (fifty-six registries of kinds, `set_count` traced
  from JSON to a chest). `math-and-primitives` is Reference.
  `chat-and-signing`'s `Component` section is a pointer; `text-and-fonts`
  points here. Fifty-two lane rows added; `check_lanes --strict` is clean
  for both parts. **Two pass-2 errors caught by drafting agents**: the axe
  does not strip by tag (`AxeItem.STRIPPABLES` is a map), and
  `NoiseRouterData` does not call `TerrainProvider` per chunk (its
  bootstraps are datagen and `Commands.validate`); both verified by the
  session and logged in pass4.md. 97 diagrams, 0 failed; 19,720 names
  resolve. Hand-offs in pass3.md §8 (the two Part III invariants still on
  `anatomy`, the three enchanting facts for session H, the treemap's
  hatch limitation, the pattern page's *taught in* obligations), pass4.md
  (every introduced claim, per page) and pass5.md (every cut name).
  Process note: nine pages drafted by parallel agents against a shared
  brief, each report diffed by the session; three agents lost to an
  interrupt were relaunched on Opus with no visible loss — the part
  sessions from D on should run on Opus, with Fable kept for O, P and the
  inter-pass planning.
- **2026-09-02, session D — Part III The server.** *Rulings, written before
  editing.* **Part III is a line into a loop and out again**, and the
  landing page draws exactly that: `starting-a-server` runs into
  `server-tick`, which turns with `server-level-tick`, with
  `players-and-sessions` hanging off the loop as who is in it, and
  `how-a-server-dies` at the exit. **The part gains one page** — R7's
  allowance, spent on the coverage queue's *how a server dies* — and
  `server-lifecycle` splits, which **overrules the schedule line** ("lifecycle
  last and reframed … startup gets its own diagram"): the schedule asked for
  one page with two traces, and one page with two traces is precisely the
  lecture/page mismatch this pass exists to fix (charter §*What is wrong
  today* item 6). Session B's own note called *how a server dies* "the
  strongest new page candidate found in Part III". The side threads, which
  span both halves, are described where they are **created** (startup) and
  their non-daemon consequence is stated where it **bites** (the death page's
  `onServerExit`). `server-lifecycle.md` becomes
  `starting-a-server.md` with a redirect (R8); nothing outside Part III
  linked to it. **The five pages, their shapes and their hooks.**
  **`server-tick`** keeps the **trace** shape but takes a seven-lane
  sequence that ends on the wire, so the two flushes are visible rather
  than asserted, plus a small flowchart of the budget for the **event-loop
  section R6 gives it to own** (`BlockableEventLoop`, `TickTask`,
  `shouldRun`, `managedBlock`) — the section four parts link to instead of
  re-explaining. Hook: "Can't keep up!" is not a warning that the server is
  skipping ticks, it *is* the skip, and the same condition holds the log, so
  a server that complained recently stays behind instead. It also absorbs
  the two Part I invariants `anatomy` still carries (the `haveTime` "gates
  exactly three things" claim, the sprint-polls-chunk-sources conclusion),
  cut there to a link. **`server-level-tick`** trades its twelve-lane
  conversation for the **guard flowchart** the notebook asked for — the
  fourteen phases with their gates (`runsNormally`, `emptyTime`, `isDebug`,
  none) on the arrows, which carries the ordering and the gating at once —
  plus a four-lane sequence of the block-change broadcast alone. It opens by
  defining the three chunk ranges in two sentences (pass3 §5's
  recommendation) so the page does not borrow Part IV's vocabulary
  unexplained. Hook: the tick broadcasts its block changes *before* it ticks
  its entities, so a change an entity makes always reaches the client a tick
  later than a change a command makes. **`players-and-sessions`** becomes a
  **trace** and a **comparison** with the seam the notebook found: the join
  as two diagrams (admission and configuration, then `placeNewPlayer`'s
  packet burst) in place of the nine-lane one whose implied concurrency was
  wrong anyway, then the exits as a four-column table (respawn · dimension
  change · disconnect · `switchToConfig`) with the question people actually
  ask as its headings. Hook: dying destroys and rebuilds your `ServerPlayer`
  while a trip to the Nether does not, and both keep the entity id and the
  same connection object. **`starting-a-server`** is the **trace** shape
  with the diagram the notebook asked for: the only figure in the corpus
  where the **JVM main thread is a lane**, handing off to the Server thread
  and never appearing again. Hook: the step the loading screen calls
  preparing the world loads no chunks at all on an ordinary world —
  `prepareLevels` re-arms persisted tickets, and only `/forceload` and
  portal tickets persist. **`how-a-server-dies`** is the **comparison**
  shape: three endings (`/stop`, a tick-loop crash, a watchdog kill) as the
  columns, `/stop` traced in full because the other two are differences from
  it, and a four-lane sequence of the watchdog's self-deadlock. Hook: a
  crash saves your world and the watchdog does not — `System.exit` runs a
  hook that joins the very thread that is wedged. **Lanes**: the Part III
  rows go into the key before drafting; `G` becomes `SGPL` (the notebook's
  odd one out), `LevelTicks` lengthens to `LTs` because session C's
  `LT` is `LootTable`, and `SL`/`MS` lose their parenthetical labels so the
  linter can read them. `check_lanes.py --strict --pages src/systems/server`
  before shipping.
  *Done.* Part III is five pages in a line-into-a-loop, drawn on a new
  landing page the sidebar's Part III opens on. `server-tick` is a
  six-lane trace that ends on the wire, so the two writes per client are
  visible rather than asserted, and it now owns **the event loop** (R6) as
  a named section with a flowchart of `pollTask` → `shouldRun` →
  `haveTime` and the `managedBlock` suspension — the section four parts
  will link to instead of re-explaining; `anatomy`'s two Part III
  invariants moved here and are a pointer there. `server-level-tick`
  traded its twelve-lane conversation for the **guard flowchart** the
  notebook asked for, twenty-odd phases each labelled with the gate it
  sits behind, plus a four-lane sequence of the block-change broadcast
  that is the page's hook drawn; it opens by defining the three chunk
  ranges, so Part III no longer needs Part IV in front of it.
  `players-and-sessions` is a trace and a comparison at the seam session B
  found: two join diagrams in place of the corpus's widest one, then the
  four exits as a table with sections per point of difference (*what comes
  across when you die*, *why the Nether keeps your potion effects*,
  *where your llama goes when you log out*). `server-lifecycle` split:
  `starting-a-server` is the boot trace with the only diagram in the book
  that has the JVM main thread as a lane, and **`how-a-server-dies` is the
  part's closer** — three endings as columns, `/stop` traced in full, and
  the watchdog's self-deadlock drawn in four lanes.
  **Eighteen pass-2 errors found**, the largest crop since pass 2 itself,
  twelve of them re-derived by the session from the decompile: among them
  `ServerLevel.runBlockEvents` is freeze-gated (the old figure said
  otherwise by omission), a debug world drops the block-change broadcast,
  `ChunkHolder.broadcastChanges` sends light *before* blocks,
  `NaturalSpawner.createState` walks every entity rather than a chunk
  window, `MinecraftServer.scheduleExecutables` runs a late task inline
  instead of throwing, `PlayerList.respawn` is handed its removal reason
  rather than choosing it, `IntegratedServer` does set a simulation
  distance, the *Done* line is logged before RCON and the watchdog exist,
  and an ordinary autosave rewrites `level.dat` — which is what the new
  durability section rests on. All are in pass4.md with the fixes flagged
  for re-checking.
  Thirteen lane rows added plus two word lanes;
  `check_lanes --strict --pages src/systems/server` is clean, 103 diagrams
  render, 19,659 names resolve, and the old `server-lifecycle` URL
  redirects. Hand-offs in pass3.md §8 (the event loop's owner, the
  three-ranges opener session E must keep in step, two wrong link labels
  for sessions I and N), pass4.md and pass5.md.
  Process note: five pages drafted by parallel Opus agents against a shared
  brief and diffed by the session. **One agent reported a corrected
  ordering in its prose and then drew the old ordering in its own new
  diagram**; the session caught it against the decompile. A drafting
  report is not evidence about the figure — later sessions should read
  every redrawn diagram separately, and pass 4 has been told the same.
- **2026-09-02, session E — Part IV The world.** *Rulings, written before
  editing.* **Part IV is a conveyor with a vocabulary page in front of it and
  three lectures hanging off the side**, and the landing page draws exactly
  that: `chunk-anatomy` defines the thing, then four pages hand a chunk along
  a line — a ticket asks for it (`tickets-and-loading`), the pyramid builds
  it (`chunk-generation-pipeline`), the light engine finishes it
  (`lighting`), the region file forgets it (`chunk-storage`) — and
  `environment-attributes-and-timelines`, the two tick pages and the two
  index pages are about the world the conveyor delivers, not about the
  conveyor. **The part goes from nine pages to ten**, and both changes are
  the notebook's confirmed splits rather than R7's new-page allowance, which
  this session does not spend (Part IV has no coverage-queue entry).
  `block-ticks-and-fluids` splits at its own trace step 5 → 6 into
  **`scheduled-ticks`** and **`fluids`**; `game-events-and-poi` splits into
  **`game-events-and-vibrations`** and **`points-of-interest`**, the seam the
  pass-2 fact-check found by producing two reports with no shared class in
  them. `level-data-and-rules` moves to `src/reference/` (R5), which leaves
  Part IV with no page that says of itself "short, no trace". Four redirects
  (R8).
  **The ten pages, their shapes and their hooks.**
  **`chunk-anatomy`** takes the **vocabulary** shape: two figures of the data
  (the four shapes a chunk takes, and the containment from chunk down to bit
  storage) and a tour by object grounded in one small trace, one block
  written. Hook: a section holding two block states costs exactly what one
  holding sixteen costs, on disk as well as in memory — and the block that
  makes it seventeen re-encodes all 4,096 entries.
  **`tickets-and-loading`** is session A's policy pilot and is not rewritten;
  it is re-read against `server-level-tick`'s new three-ranges opener so the
  two agree.
  **`chunk-generation-pipeline`** takes the **pipeline** shape the notebook
  asked for, and **the pyramid is drawn** — twelve statuses, the radius each
  needs, the four that fork off the worldgen executor — instead of living in
  a markdown table; a section per stage; the ten-lane trace comes down to
  seven. Hook: asking for one chunk asks for 529, and eleven chunks of that
  ring will never become chunks you can stand on.
  **`lighting`** keeps the **trace** shape and gains the figure the notebook
  says it lacks: the four-stage batch (check nodes, decreases, increases,
  swap) as a pipeline flowchart beside the torch trace, which also comes down
  to seven lanes. Hook: there is no light thread and no light phase of the
  tick — the light engine runs because the server thread had nothing else to
  do.
  **`chunk-storage`** keeps the **trace** shape with a three-lane hand-off
  figure in front of it (the server thread copies, the worker encodes, the IO
  lane writes), and its eleven-lane diagram splits: the unload and the write
  are two pictures. Hook: almost every write of your world is one nobody
  asked for — a chunk you touched is written about every ten seconds by a
  background sweep, and the autosave is five minutes of wall clock whatever
  `/tick rate` says.
  **`scheduled-ticks`** is the **pipeline** shape: schedule, index, collect,
  drain, run, with a section per phase and a repeater as the grounding trace
  (the notebook's suggestion; it is also what Part V will link to). Hook:
  dedup is by type and position only, so a second, *sooner* tick for the same
  block is dropped — "rescheduling moves the tick" is folklore.
  **`fluids`** is the **trace** shape on the bucket, with
  `FlowingFluid.getNewLiquid`'s three branches drawn as a decision flowchart
  — the ordering pass 2 found wrong is exactly the thing a flowchart cannot
  fudge. Hook: water finds a hole four blocks away because every side runs
  its own depth-first search, and a side the water cannot even enter still
  votes on where the rest of it goes.
  **`game-events-and-vibrations`** is the **trace** shape (the footstep) with
  the filter cascade drawn — every test that drops a vibration, in order,
  which is the page's real subject and today is prose. Hook: a sensor always
  hears you one tick late by design, and the wool box only works if all six
  rays hit wool — but standing *on* the sensor skips the whole cascade,
  sneaking included.
  **`points-of-interest`** is the **trace** shape (the villager and the bed).
  Hook: the bed is claimed the moment a path to it exists, up to 48 blocks
  away, and the claim and the *occupied* flag are two facts that never speak
  to each other.
  **`environment-attributes-and-timelines`** is the best-shaped page in the
  part and keeps its mirrored server/client pair; it gains the third figure
  the notebook asked for — **the layer stack drawn as a stack** above the two
  sequence diagrams — and the frame every page now keeps (hook first, cast
  table, headings that say what they say). Hook: the night does not set the
  sky's colour, it multiplies whatever the biome produced — every timeline
  track carries a modifier argument, not a value, which is the one decision
  the whole system rests on.
  **`level-data-and-rules`** becomes Reference: the who-owns-what table is
  the page, the header stops promising a lecture, and Part IV's landing page
  points at it as the part's look-up.
  **Lanes**: the Part IV rows go into the key before drafting. Three
  collisions with existing rows are resolved by lengthening the later
  claimant, as the rule says — `LevelChunkTicks` cannot be `LCT`
  (`LoadingChunkTracker`, session A) and becomes `LCTs`; `PoiRecord` cannot
  be `PR` (`PackRepository`, session C) and becomes `PRec`; and
  `PalettedContainer` yields `PC` to `ProtoChunk` and becomes `PCon`. `VS` is
  claimed for `VibrationSystem`, and `EnvironmentAttributeSystem.ValueSampler`
  is recorded as `EVS` under the nested-class exception. `check_lanes.py
  --strict --pages src/systems/world` before shipping.
  *Done.* Part IV is ten pages in a conveyor, drawn on a new landing page
  the sidebar's Part IV opens on: `chunk-anatomy` defines the thing, four
  pages hand it along the line, and five are about the world the line
  delivers. `chunk-anatomy` is a vocabulary page with two figures — the four
  shapes a chunk takes and where each is made, and the containment from
  chunk down to the bit storage, which is the hook drawn — in place of a
  415-line field inventory. `chunk-generation-pipeline` **draws the
  pyramid** the notebook has asked for since session C: twelve statuses,
  the radius each sweeps, and which of them leave the worldgen executor,
  with its ten-lane conversation cut to seven. `lighting` gained the
  four-stage batch as a pipeline figure beside the torch trace, and now
  says plainly that the light engine runs because the server thread went
  idle. `chunk-storage`'s eleven-lane monster became three figures — the
  three-thread hand-off, the unload, and `RegionFile.write`'s sector dance,
  whose in-file and sidecar branches commit in opposite orders. Both
  confirmed splits were executed: `block-ticks-and-fluids` at its own trace
  step 5 → 6 into **`scheduled-ticks`** (a pipeline, traced on a repeater,
  which is what Part V will link to) and **`fluids`** (the bucket, with
  `FlowingFluid.getNewLiquid`'s three branches drawn as a decision
  flowchart, because the ordering is what pass 2 got wrong);
  `game-events-and-poi` into **`game-events-and-vibrations`** (the filter
  cascade drawn, which the old page carried as a numbered list with no
  figure at all) and **`points-of-interest`** (the villager and the bed,
  with the life of one ticket as a state diagram).
  `environment-attributes-and-timelines` kept its matched server/client
  pair and gained the layer stack drawn as a stack.
  `level-data-and-rules` is Reference.
  **Twelve pass-2 errors found**, seven of them re-derived by the session
  from the decompile. The largest is `lighting`'s: the light packet goes to
  **border players only** — `ChunkHolder.broadcastChanges` passes
  *borderOnly* true for light and false for blocks — where the old page
  said "with border players included", exactly inverting it. Two more
  overturned claims this session's own rulings had repeated: POI records
  appear **synchronously** on the server thread (`MinecraftServer.scheduleExecutables`
  is false outside a queued task, so `BlockableEventLoop.execute` runs the
  body inline), and the vetoing side in `FlowingFluid.getSpread` is one the
  water may enter but not *replace*, and it clears the collected winners as
  well as lowering the minimum. Also: the scheduled-tick drain **does** run
  during `/tick step`; biomes have no four-bit linear palette rung; the
  nether has no day timeline at all; a positional attribute no layer makes
  positional is memoised like any other; and a vibration arrives
  ⌊distance⌋ − 1 ticks after selection, not ⌊distance⌋.
  Two release paths for a villager's bed that no page had.
  **One tool bug**: `check_lanes.py --pages src/systems/world` also matched
  `src/systems/worldgen`, so it was reporting nine Part XII pages as Part IV
  failures — a plain `startswith` on paths, fixed with a separator-aware
  check that session M would otherwise have hit.
  Thirty-three lane rows added and twenty-nine speculative ones pruned
  before shipping, on the principle that a key row is a claim on a lane and
  claiming one a page does not use pre-empts a session that has not run;
  `check_lanes --strict --pages src/systems/world` is clean, 117 diagrams
  render, 19,215 names resolve, and four old URLs redirect. Twenty pages
  across nine other parts were re-pointed at the right half of each split.
  Hand-offs in pass3.md §8 (the tool bug, the lane ledger, the four
  collisions later sessions must lengthen, and what Parts V, VI and O
  inherit), pass4.md and pass5.md.
  Process note: nine pages drafted by parallel Opus agents against a shared
  brief, each report diffed by the session. **Three agents overruled the
  session's own rulings with evidence** — the fluid hook's wording, the POI
  deferral, and the brief's "four steps leave the worldgen executor" (it is
  five) — which is the protocol working as intended; a ruling written
  before the pages are open is a hypothesis. The session read every redrawn
  diagram against the source separately from its page's prose, per session
  D's lesson, and that caught four figure-level problems the reports did not
  mention: a `getNewLiquid` flowchart that implied `FlowingFluid.spread` is
  not called on an empty result, a pyramid caption asserting radius 11 for
  *EMPTY* without saying the first sweep is the loading pyramid's 1, a
  containment figure showing the block-state palette ladder on a node shared
  with biomes, and a lane carrying a parenthetical the linter cannot read.
- **2026-09-02, session F — Part V Blocks.** *Rulings, written before
  editing.* **Part V is a hub and six spokes, and the hub's second half is
  the part's real subject.** `blocks-and-states` is the vocabulary page every
  other page reaches back into, and the thing they reach for is not the state
  table but **the tail of a write**: what `LevelChunk.setBlockState` and
  `Level.setBlock` do after the section has been written. R6 puts the *two
  update channels* flowchart there and this session draws it as one figure
  spanning both methods, because the split runs through the middle of them —
  `BlockEntity.preRemoveSideEffects`,
  `BlockBehaviour.BlockStateBase.affectNeighborsAfterRemoval` and
  `BlockBehaviour.BlockStateBase.onPlace` are inside the **chunk** write
  (session E's correction), while the broadcast, the neighbour fan-out and the
  three shape passes are in `Level.setBlock`'s tail. Every other page in the
  part links to that one figure instead of restating it, which is the fix for
  the notebook's finding that three of five pages had the distinction subtly
  wrong.
  **The part goes from five pages to seven**, all of it the schedule's own
  work: `redstone` splits three ways, and R7's new-page allowance is **not
  spent** — Part V has no entry in the coverage queue, which therefore still
  stands at fifteen items. `blocks-and-states` is **not** split, overruling
  nothing (pass 2 left it as pass 3's call): its two halves are the state
  table and the write, and the write is what the other six pages need, so
  cutting between them would put the part's load-bearing figure on a page
  nobody is sent to. One redirect (R8): the old `redstone` URL goes to
  `signal-and-dust`.
  **The seven pages, their shapes and their hooks.**
  **`blocks-and-states`** takes the **vocabulary** shape with two figures — a
  containment figure of the objects (`Block`, `BlockBehaviour`,
  `StateDefinition`, `Property`, `StateHolder`,
  `BlockBehaviour.BlockStateBase`, `BlockState`) and the two-channel flowchart
  of a write — and the stair placement kept as the grounding trace, cut to
  the state *choice* and the write, since the click that led to it is the
  next page's. Hook: every state the game will ever have is built before any
  world exists, and the world stores an index into that table, so setting a
  property allocates nothing and a client that disagrees with the server
  about a block's properties does not throw — it sees air.
  **`block-interaction`** and **`block-breaking`** are **one lecture in two
  halves** (R6): both keep the **trace** shape and both open with the *same*
  preamble stating the prediction ledger's contract — the ack is a receipt
  for a number and not a verdict, and correctness comes from the ordering —
  with the mechanism left to `prediction-and-acks`. Neither page re-derives
  the ledger again. `block-interaction`'s hook: opening a door fires no
  neighbour update at all, and the other half follows anyway, through the
  one channel the client also runs. `block-breaking`'s hook is the hook bank's
  block that comes back and vanishes again: releasing the button does not
  cancel a break, and nothing the client does between the two can stop it.
  **`block-entities`** keeps the **trace** shape and the furnace, reshaped to
  the frame; the notebook calls it the best-shaped page in the part and this
  session does not go looking for a reason to change it. Hook: a furnace
  tells nobody anything — the fire is a block state, the arrow is four ints
  from a menu, and both are a tick late because block entities tick last.
  **`signal-and-dust`** takes the **trace** shape (lever, two dust) but the
  notebook's wrong-shape finding is honoured in the figure: the cascade is
  drawn as a **flowchart of one wire's recomputation and its hand-issued
  fan-out**, not as a conversation, and the experimental evaluator is the
  coda it belongs to rather than a page of its own. Hook: a line of dust
  turning off counts down through every intermediate value because each wire
  recomputes from scratch and then hand-notifies forty-two positions — and
  the game ships a second implementation, behind a feature flag, that does
  not. It owns the third direction order, `SignalGetter.DIRECTIONS`, and the
  weak/strong distinction.
  **`pistons-and-block-events`** keeps its **lanes** — the notebook says this
  half is genuinely sequential — and owns the block-event queue, which is the
  part's only *deferral* mechanism and is what makes the piston a tick late.
  Hook: the moving blocks are never sent. The client re-runs the push itself
  from one event packet, the placeholders are written with the tell-clients
  bit deliberately clear, and no correction ever follows.
  **`diodes-and-observers`** takes the **comparison** shape — repeater,
  comparator and observer as three columns of *what it reads*, *how it books
  its turn*, *how it outputs* — because that is exactly how they differ and
  the old section read as three unrelated paragraphs. Hook: the observer, the
  block whose whole job is noticing that something changed, is not on the
  channel that carries change notifications, and neither is the repeater's
  lock — both listen on the shape channel.
  **What Part V no longer teaches.** `scheduled-ticks` (Part IV) owns the
  appointment book, the priorities and the repeater's pulse extension;
  `fluids` owns `LiquidBlock` and waterlogging; `prediction-and-acks` owns the
  ledger; `game-events-and-vibrations` owns `GameEvent` posting;
  `chunk-anatomy` owns the section and palette. The diodes page links to the
  first for delay and priority rather than restating either.
  **Lanes**: the Part V rows go into the key after drafting, from the
  diagrams that actually exist, not before (session E's rule that a key row
  is a claim). Four collisions with existing rows are resolved by lengthening
  the later claimant: `LeverBlock` cannot be `LB` (`LiquidBlock`, session E)
  and becomes `LevB`; `BlockItem` cannot be `BI` (`BucketItem`, session E) and
  becomes `BItem`; `BlockPlaceContext` cannot be `PC` (`ProtoChunk`, session
  E) and becomes `BPC`; `PistonStructureResolver` cannot be `PR`
  (`PackRepository`, session C) and becomes `PSR`.
  `check_lanes.py --strict --pages src/systems/blocks` before shipping.
  *Done.* Part V is seven pages in a hub and six spokes, drawn on a new
  landing page the sidebar's Part V opens on. **The hub's second half is the
  part's real payload**: `blocks-and-states` now draws the tail of a write as
  one flowchart spanning `LevelChunk.setBlockState` and `Level.setBlock`,
  with every server-only step and its flag gate marked, and the other six
  pages link to that anchor instead of restating the shape-versus-neighbour
  distinction — the fix for the notebook's finding that three of five Part V
  pages had it subtly wrong. `block-interaction` and `block-breaking` are one
  lecture in two halves, opening with an identical four-sentence statement of
  the prediction contract and leaving the machinery to
  `prediction-and-acks`; the landing page rules that Part V is watched
  *before* it, resolving the circular dependency section 5 flagged.
  `block-entities` kept the furnace and gained the tick bars it needed.
  **`redstone` split three ways** — `signal-and-dust` (the cascade drawn as a
  flowchart rather than a conversation, with the experimental evaluator as
  its coda), `pistons-and-block-events` (block events as a general mechanism,
  then the piston) and `diodes-and-observers` (the repeater, comparator and
  observer as a comparison table of what each reads, how each books its turn
  and how each outputs) — and the old URL redirects to the first. R7's
  new-page allowance was not spent, so the coverage queue still stands at
  fifteen.

  **The session was interrupted and lost five drafting agents**, four pages
  in. The four drafted pages were complete on disk, but **two of the four
  agent reports did not survive**, which is the part that matters: a page
  whose claim-diff never arrived cannot be said to have been diffed.
  `pass4.md` records the four classes of evidence explicitly and tells pass 4
  to treat `blocks-and-states` and `block-entities` as unaudited and to diff
  them against their pass-2 versions in git. The three redstone pages were
  then written by the session itself from the decompile, method by method,
  with every diagram read separately from its prose.

  **Nine corrections re-derived by the session.** The largest is that
  **block events are not "a tick late"** — the old `redstone` diagram said so,
  but packets are drained before `MinecraftServer.tickServer` and the
  *blockEvents* phase precedes *entities*, so an event queued by a packet
  handler or a scheduled tick drains in the same tick, and only the entity
  and block-entity phases push one over the boundary. `reference/glossary.md`
  already had it right, so the corpus had been contradicting itself.
  Next: **`RepeaterBlock.LOCKED` does not survive on a client** and the old
  page's stated reason for saying it did was backwards —
  `RepeaterBlock.updateShape` and `ObserverBlock.startSignal` both refuse to
  run client-side, and a client keeps no appointment book to fire into.
  Also: `blocks-and-states`' new hook overclaimed *you get air* and was
  narrowed, because `ClientboundBlockUpdatePacket.STREAM_CODEC` throws on an
  unknown id where `Block.stateById` does not; dust powers the block **below**
  it and never the one above; `LeverBlock.pull` is handed a null player so
  the clicker hears the server's sound, unlike the door; a diode's `FACING`
  points at its **input**; `PistonBaseBlock.checkIfExtend` resolves as a dry
  run before it queues anything; `ComparatorBlock.checkTickOnNeighbor` books
  on a condition the repeater has no analogue of; and `SignalGetter.getSignal`
  is a maximum of weak and strong power rather than a choice between them.
  The one agent report the session did fully re-derive,
  `block-interaction`'s, found six more, including that a player mid-use has
  their queued right-clicks **discarded** rather than delivered.

  Thirteen lane rows added and four collisions lengthened;
  `check_lanes --strict --pages src/systems/blocks` is clean, **122 diagrams
  render**, 18,194 names resolve, the class index is regenerated, the old
  `redstone` URL redirects, and four cross-part links plus three glossary
  entries were re-pointed at the right half of the split. Seven pages at
  243–388 lines — the first part to land inside the length brief rather than
  over it. Hand-offs in pass3.md (the shared anchor six pages depend on, the
  split seams other parts link across, two Reference candidates for session O,
  the lane ledger), pass4.md and pass5.md.
- **2026-09-03, session G — Part VI Entities.** *Rulings, written before
  editing.* **Part VI is a ladder with a missing rung, and the rung goes in
  second.** The notebook's order survives — object, world, the channels that
  describe it, what it does, why, how it stops — and R6's authority page is
  inserted directly after `entity-anatomy`, where it is a prerequisite for
  everything above it and for Parts VIII, IX and X. The landing page draws
  the ladder and says so.
  **The part goes from seven pages to nine.** One page is R6's
  (`authority`); one is the notebook's confirmed split of
  `ai-goals-and-brains`. R7's new-page allowance is **not** spent as a page:
  Part VI's single coverage-queue entry, the non-living `Entity.hurtServer`
  overrides, is discharged as **a named closing section in
  `damage-and-death` plus a Reference table** — the queue itself offered
  that as one of its three options, and a twenty-one-row table of "what
  this class does when you hit it" is the definition of something a viewer
  pauses on (R5). Two catalogues move to Reference **generated**, as the
  schedule asks: the 43 entity-data serializers with their wire ids and the
  40 attributes with their defaults, ranges and syncable flags —
  `gen_reference.py` gains two views, so both are re-derived on the next
  version rather than re-checked by hand.
  **`ai-goals-and-brains` splits in two, not three**, which is this
  session's answer to the schedule's *ruled*. The page's argument is that
  two decision systems coexist and are identical below the waterline;
  cutting between goals and brains would destroy the one comparison the
  page exists to make. The seam the notebook actually found is the
  waterline itself — `MoveControl.setWantedPosition` — so the cut is there:
  **`ai-goals-and-brains`** keeps goals, brains, activities, the villager
  day and the zombie (and its URL, so no redirect), and **`pathfinding`** is
  new and takes navigation, the A\* and its budget, the node evaluator and
  path types, the region snapshot, stuck detection and the four controls.
  **`entity-anatomy` is not split** (pass 2 confirmed the seam and left the
  call here): it is the part's map page and its two halves are what an
  entity *is* and what the tree *looks like*, which is one lecture. But its
  hand-drawn mermaid class tree goes, replaced by the atlas's **generated**
  `tree-Entity.svg` (R4: a figure has to be regenerable, and session B
  already draws this one with real counts).
  **The nine pages, their shapes and their hooks.**
  **`entity-anatomy`** takes the **vocabulary** shape: a containment figure
  of what an entity is made of, the generated tree, and the registry-to-live-object
  trace kept as the grounding. Hook: the entity registry's default is a
  pig, and that default reaches the network and not your save file — a bad
  id on the wire is a pig, a bad id in a region file is a *Skipping Entity*
  line and a hole where the entity was.
  **`authority`** is new (R6) and takes the **comparison** shape: a mob and
  a player, each taking one step, on each side, as the columns; the four
  predicates as the rows; a section per point of difference. Hook: the
  client runs no physics at all for the zombie chasing you, and it runs
  full physics for the player standing beside you — while the server runs
  that player's physics too and throws the answer away. Parts VIII, IX and
  X link here instead of re-teaching the matrix, and
  `movement-and-collision` loses its opening section to it.
  **`entity-lifecycle`** keeps the **trace** shape (a zombie's life) and
  gains the two figures the notebook asked for: the spawn attempt as a
  **filter cascade** — every test that rejects, in order, with the
  rejections drawn — and `Visibility` as a small state diagram. Hook: the
  spawner rolls **one** height per category per chunk per tick, uniform
  from the world bottom to the surface, so every category gets its own
  horizontal slice and a taller world thins the surface out.
  **`synched-entity-data`** keeps the **trace** shape (the sheep) with the
  43-serializer catalogue gone to Reference and the sheep's nineteen slots
  kept, because that table *is* the lecture. Hook: the id of the sheep's
  wool byte is decided by the order the JVM runs static initialisers in,
  and the packet stops at 254 because 255 means stop.
  **`attributes`** takes the **vocabulary** shape — the five objects, the
  three-pass arithmetic, the sync gate — with the Strength II trace as its
  grounding and the forty-attribute catalogue gone to Reference. Hook:
  Strength II sends no packet at all, because eight of the forty attributes
  are not syncable and attack damage is one of them.
  **`movement-and-collision`** keeps the **trace** shape (the falling
  zombie) and hands its authority section to the new page. Hook: the mover
  answers *what did I walk through* after the fact, by replaying the tick's
  movement in the same axis order the collision used — which is why fire
  and water touched in the same step always end in the extinguish.
  **`ai-goals-and-brains`** takes the **comparison** shape: the goal
  selector and the brain as two columns of *what holds the state*, *what
  decides*, *what arbitrates* and *what persists*, with the villager day
  as the brain's trace and the zombie as the goal selector's. Hook:
  schedules are gone — a villager goes to bed because it asks the world
  what time it is *where it is standing*.
  **`pathfinding`** is new and takes the **pipeline** shape: walk target →
  navigation → region snapshot → node evaluator → A\* → path → move
  control, a section per stage. Hook: giving up is machinery — every node
  carries a timeout derived from its distance and the mob's speed, and
  three overruns abandon the path, so the mob you watch walk into a wall
  and then wander off is running a scheduled surrender.
  **`damage-and-death`** keeps the **trace** shape (the arrow) and gains
  the closing section it has been missing: **the five families of
  non-living damage**, with the per-class table in Reference. Hook stays
  the i-frame one — a hit inside the red flash that *does* land is
  invisible: health drops and nothing else happens.
  **Reference.** `reference/entity-data-serializers.md` and
  `reference/attributes.md` are generated by two new `gen_reference.py`
  views; `reference/non-living-damage.md` is hand-kept and re-swept in pass
  4. All three are in `SUMMARY.md` and the reference README.
  **Lanes** go into the key *after* drafting, from the diagrams that exist
  (session E's rule); collisions are resolved by lengthening the later
  claimant. `check_lanes.py --strict --pages src/systems/entities` before
  shipping.
  *Done.* Part VI is nine pages in a ladder, drawn on a new landing page the
  sidebar's Part VI opens on. **The missing rung went in second**:
  `authority` is a comparison of three cases — a tracked mob, a player and a
  ridden boat, each read on both sides — with the four predicates as its
  rows, the six gates inside `Entity.move` and `LivingEntity.aiStep` that
  read them, and the vehicle case nothing in the corpus had: both base
  client-authority predicates delegate to the *controlling passenger*, which
  is the whole vehicle model, and `ClientboundMoveVehiclePacket` turns out to
  be a rejection notice rather than a routine update. Sessions I, J and K now
  link there instead of re-teaching the matrix, and
  `movement-and-collision` is already cut to three sentences and a link.
  **`ai-goals-and-brains` split in two, not three** — the ruling the schedule
  asked for. The page's argument is that two decision systems coexist and are
  identical below the waterline, so cutting between goals and brains would
  have destroyed the one comparison it exists to make; the cut is at the
  waterline itself, `MoveControl.setWantedPosition`. Goals and brains keep the
  URL (no redirect) and became a **comparison** with seven rows of
  difference; **`pathfinding`** is new and took navigation, the A\* and its
  budget, the node evaluator, the region snapshot, stuck detection and the
  four controls. `entity-lifecycle` got the **filter cascade** the notebook
  has asked for since session E — every rejection in source order, with the
  only-now-is-the-mob-constructed boundary drawn — plus `Visibility` as a
  state diagram; `entity-anatomy` traded its hand-drawn class tree for the
  atlas's generated `tree-Entity.svg`, the first system page to use session
  B's figure pipeline. Both reference catalogues moved out **generated**:
  `gen_reference.py` grew `entity-data-serializers` (43 rows, registration
  order, which is the wire id) and `attributes` (40 rows with range, syncable
  and sentiment). R7's allowance was **not** spent as a page: Part VI's one
  coverage-queue entry, the non-living `Entity.hurtServer` overrides, became
  a five-family closing section in `damage-and-death` plus the hand-kept
  `reference/non-living-damage.md` — and the count was wrong twice over, at
  21 classes rather than "about thirty", with `Entity.hurtServer` **abstract**
  so there is no default behaviour anywhere in the tree. The queue drops to
  fourteen.
  **Twenty-two pass-2 errors found**, eight of them re-derived by the session
  itself. The largest is that **only `Villager` has a schedule**:
  `Brain.setSchedule` has two call sites, both in `Villager`, and the other
  nineteen brain mobs use `Brain.setActiveActivityToFirstValid` — the old
  page called that the exception used by three mobs. Then: the spawner's
  biome energy budget runs *before* construction, not after;
  `INSCRIBED_SQUARE_SPAWN_DISTANCE_CHUNK` is 5, not 8, and feeds only
  `DistanceManager.hasPlayersNearby`'s fast-yes arm;
  `EntityTypes.ITEM_FRAME`'s update interval is `Integer.MAX_VALUE`, which is
  *why* `ServerEntity` has an item-frame bypass — and that bypass is the only
  one, where the old page named two; the *chunkSource* phase is mid-tick, not
  near its start; `LivingEntity.shouldTravelInFluid` reads the cached flags,
  not the live fluid state; `Attributes.DEFAULT_ATTACK_SPEED` has no callers
  at all; `EntitySpawnRequest.ignoreChecks` is never true;
  `entity-anatomy`'s subpackage table summed to 639 of a stated 716; and
  — the one that would have embarrassed the new page most — the old
  `damage-and-death` opened its list of classes that "never touch armour,
  i-frames or the combat tracker" with `ArmorStand`, which is a
  `LivingEntity`.
  **One tool bug**: `gen_reference.py`'s *gamerules* blurb still linked to
  the pre-session-E path for `level-data-and-rules`, so **regenerating the
  reference tier reintroduced a broken link somebody had fixed by hand** —
  found by a link sweep, fixed in the tool.
  Twenty-two lane rows added and five later claimants lengthened (`MoveC`,
  `SumC`, `AttrM`, `AttrI`, `EffC`); `check_lanes --strict --pages
  src/systems/entities` is clean, **135 diagrams render**, 18,015 names
  resolve, and every relative link in `src/` resolves. Nine pages at 118–420
  lines, two of them over the length brief and logged in pass5.md. Three of the six identical *Questions players ask* headings were
  varied in-session, which is the "second uniformity" risk showing up for the
  first time. Hand-offs in pass3.md §8 (the authority owner and its four
  dependants, the AI seam, the `SE` lane session K must lengthen, the
  Nether-fortress material that now lives nowhere), pass4.md and pass5.md.
  Process note: seven pages drafted by parallel Opus agents against a shared
  brief, every report diffed by the session. `damage-and-death`'s report ran
  long, and rather than wait the session audited that page against the
  decompile itself — so when the report did arrive there were **two
  independent audits of one page, and they agreed**, which is a cheap check
  worth repeating on the page a part cares most about. Three agents overruled
  the session's own rulings with evidence — the spawner's budget ordering, the
  claim in the brief that `ServerEntity.handleMinecartPosRot` bypasses the
  send gate, and the brief's own roster of non-living damage classes, whose
  first entry — `ArmorStand` — is a `LivingEntity` — which is the protocol
  working: a ruling written before the pages are open is a hypothesis.
- **2026-09-03, session H — Part VII Items and inventories.** *Rulings,
  written before editing.* **Part VII is two tiers, and the part currently
  pretends it is a chain.** Tier one is the vocabulary — what a stack *is*,
  what happens when you use one, and how two machines agree about a set of
  them — and every page of it is a hard prerequisite for everything above.
  Tier two is three data-driven engines that produce or decorate stacks —
  recipes, enchantments, loot — which depend on tier one completely and on
  each other not at all. The landing page draws the two tiers rather than a
  list, and says that the three engines may be watched in any order.
  **The part goes from five pages to eight**, all three additions being
  splits the notebook confirmed. `items-and-stacks` sheds the use pipeline
  to **`using-an-item`**, which is also where R7's allowance is spent: the
  coverage queue's *drawing a bow* is not a new subject but the **second
  half** of that page, because the release branch and the completion branch
  are one guard read two ways. `loot-tables` sheds its front to
  **`contexts-and-predicates`**, so that Part XIII and the advancement
  material depend on a page whose title describes what they need — the
  notebook's own preferred option, because the dependants are in another
  part. `enchantments` sheds its fourth section to **`enchanting`**, the
  acquisition lecture, which is a menus story and belongs beside the anvil
  and the grindstone rather than behind a hook table. No page changes URL,
  so no redirects.
  **The eight pages, their shapes and their hooks.**
  **`items-and-stacks`** takes the **vocabulary** shape: a containment
  figure of what a stack is made of, a tour by object, and one small trace
  — a pickaxe losing its last point of durability — as the grounding. Hook:
  an `Item` holds almost no data and an `ItemStack` holds a *diff*, against
  a prototype map that does not exist until the first data-pack load.
  **`using-an-item`** is new and takes the **comparison** shape: the meal
  and the bow as two columns over one guard. Hook: the client's countdown
  does not stop at zero, the meal ends because one byte arrives, and the
  bow never ends that way at all — `ItemStack.useOnRelease` is the third
  term of the completion guard, so a bow is finished by the packet the
  eating path treats as an abandonment.
  **`containers-and-menus`** keeps the **trace** shape (the shift-click)
  and gains the resync ladder as a **flowchart**, because the page's
  argument is a decision the server makes about the client's claim. Hook
  stays: agreement is silence — one packet up and zero down, because the
  server adopted the client's *belief object*, never its data, as the new
  baseline. Not split: the model and the protocol are one lecture, and the
  seam the notebook found is presentational.
  **`recipes`** keeps the **trace** shape (eight planks) and gains a
  figure of the load and its four derived indexes. Hook stays: no recipe
  ever crosses the wire, and what the client is denied is the *identity*,
  not the contents.
  **`enchantments`** takes the **pattern** shape — one idea (a named
  modifier is a map of effect components other systems ask about) with the
  hooks as its instance table and Fire Aspect as the traced instance. The
  thirty-odd-row `EnchantmentHelper` table goes to Reference **generated**
  (R5), because "which class calls which hook" is a question the decompile
  can answer on every version.
  **`enchanting`** is new and takes the **comparison** shape: the table,
  the anvil, the grindstone, the providers and `/enchant` as columns over
  the same questions — what it costs, what it may add, what it checks.
  Hook: the enchanting seed is per player, saved, sent to the client, and
  re-rolled by nothing but the table itself. It absorbs the three
  enchanting facts pass-5 recorded as homeless.
  **`contexts-and-predicates`** is new and takes the **vocabulary** shape:
  the five objects (`ContextKey`, `ContextKeySet`, `ContextMap`,
  `LootParams`, `LootContext`), the twenty-six sets as a Reference table
  **generated** from the decompile, and one small trace —
  `/execute if predicate` — as the grounding. Hook: five of the
  twenty-six sets have no loot caller at all, and the enforcement point is
  the *caller's* declared set, never the table's.
  **`loot-tables`** keeps the **trace** shape (the dungeon chest) and
  becomes the worked example of the page above it, with the draw drawn as
  a flowchart. Hook stays: the chest is empty on disk, the key is cleared
  *before* the roll, and the first toucher — which need not be a player —
  commits it with no luck, permanently.
  **Two coverage-queue entries are answered.** *Drawing a bow* is
  discharged inside `using-an-item`. *How an item picks its model* is
  **ruled to Part XI** (session L's call to make it a page or a section of
  `models-and-atlases`): the trace starts at an `ItemStack` but everything
  it touches — `ItemModelResolver`, the baked models, the atlas, the
  render state — is Part XI's, and Part VII owns the stack, not its
  appearance. Part VII links forward instead.
  **Lanes** go into the key after drafting, from the diagrams that exist;
  Part VII is the later claimant everywhere, so `ItemStack` is `IStack`
  (`IS` is `IntegratedServer`), the menus take word-plus-initial forms
  (`ChestM`, `CraftM`, `InvM`, `AnvilM`) because `CM` is `ChunkMap`, and
  `RemoteSlot`, `ResultSlot`, `LootPool` and `RandomizableContainer`
  lengthen off `RS` (`RenderSystem`), `LP` (`LocalPlayer`) and `RC`
  (`ReloadCommand`). `check_lanes.py --strict --pages src/systems/items`
  before shipping.
  *Done.* Part VII is eight pages in two tiers, drawn on a new landing page
  the sidebar's Part VII opens on. **The three splits went in as ruled, and
  each of the three new pages found its own reason to exist.**
  **`using-an-item`** took the use pipeline out of `items-and-stacks` and
  put the bow opposite the meal — and writing the bow settled the question
  the coverage queue had been carrying: the release branch is not chosen by
  `ItemStack.useOnRelease` at all. **`CrossbowItem` is its only override in
  the tree**, and the bow and trident are release-ended only because their
  duration is 72000 and their `Item.releaseUsing` does the work. What
  `useOnRelease` actually buys is one *extra* tick — `LivingEntity.releaseUsingItem`
  re-enters `LivingEntity.updatingUsingItem` when it is true, so a crossbow
  gets a final `CrossbowItem.onUseTick` to latch its charge. The old page
  named three items for a predicate that has one. **`contexts-and-predicates`**
  took the front off `loot-tables` and, counting the call sites from
  scratch, overruled this session's own hook: not five sets without a loot
  caller but **twelve of the twenty-six that never roll a `LootTable`** —
  the old sentence had listed six under a count of five and included a set
  that does have one. **`enchanting`** took acquisition out of
  `enchantments` and turned four paragraphs into the part's densest page:
  the table charges the *slot index plus one* rather than the displayed
  cost, the clue is a genuine member of the list you will receive, and every
  one of the five paths ends on the same
  `ItemStack.enchant` → `EnchantmentHelper.updateEnchantments` tail.
  **`containers-and-menus` was not split**, against the notebook's offered
  seam: the model and the protocol are one lecture. It gained the resync
  ladder as a flowchart, which is where four of its six outcomes turn out
  to be *nothing sent*.
  **Two Reference catalogues, both generated.** `gen_reference.py` gained
  `enchantment-hooks` — every `EnchantmentHelper` entry point with the
  classes that call it, scanned across the whole tree, **50 entry points, 47
  called from outside the class** — and `loot-context-params`, the
  twenty-six sets with their required and optional keys. The hook table was
  the largest artefact in the old Part VII and is now re-derivable on every
  version; the page keeps a seven-row *families* table and the five
  annotated highlights.
  **Nine pass-2 errors found**, one of them audited twice. Besides the three
  above: `Item.Properties.repairable` is **eager**, not delayed, so the old
  page's example of a tag-dependent delayed component was wrong;
  `Inventory.tick` is reached from `Player.aiStep`, not `Player.tick`;
  `DecoratedPotRecipe` is a `CustomRecipe`, making **nine** of fourteen
  crafting serializers special rather than eight, and eleven `SlotDisplay`
  variants exist rather than eight; **twenty-four** of the thirty-one
  enchantment effect components carry the decode-time validator, not ten;
  `/enchant` does *not* skip the supported-items and level rules — it is
  **stricter** about levels than the anvil, which clamps where the command
  refuses; and Fortune and Looting do not read
  `LootContextParams.ENCHANTMENT_LEVEL` at all — they read
  `LootContextParams.TOOL` and `LootContextParams.ATTACKING_ENTITY`, and
  `ENCHANTMENT_LEVEL` is written only by the five enchantment effect
  contexts. `loot-tables`' trace also had two orderings wrong: a single
  chest's menu provider **is** the block entity, and
  `ClientboundOpenScreenPacket` precedes `ServerPlayer.initMenu`.
  **The `useOnRelease` correction has two independent audits**: the session
  read the release path in the decompile while the agents were drafting, and
  the agent's report, arriving last, agreed line for line. That is session
  G's cheap check repeated, and it worked the same way.
  R7's allowance was spent on `using-an-item`, so the queue drops to
  thirteen; *how an item picks its model* was **ruled to Part XI** rather
  than written, with both Part VII references pointing forward at
  `models-and-atlases` for session L to land.
  Twenty-one lane rows added and fourteen later claimants lengthened, so
  Part VII takes no single-letter lane at all —
  `check_lanes --strict --pages src/systems/items` is clean, **148 diagrams
  render**, 18,201 names resolve, every relative link in `src/` resolves,
  and the class index is regenerated. Eight pages at 318–391 lines, all over
  the length brief and logged in pass5.md with the names that left them.
  Hand-offs in pass3.md §8 (the two-tier claim, `contexts-and-predicates` as
  Part XIII's dependency, the item-model ruling for session L, what session
  I should read first), pass4.md and pass5.md.
  Process note: eight pages drafted by parallel Opus agents against one
  shared brief, every report diffed by the session before acceptance. Three
  agents overruled the session's rulings with evidence — the twelve-sets
  count, the `useOnRelease` roster and `/enchant`'s real gates — which is
  the protocol working for the second session running. The one thing to do
  differently: eight concurrent agents each ran `mdbook build`, and they
  raced each other's output directory; one agent hit a spurious `ENOENT` and
  had to re-run with `--no-build`. A future session should tell agents to
  verify names only and leave the build to the session.
- **2026-09-03, session I — Part VIII The player.** *Rulings, written before
  editing.* **Part VIII is a trunk and four branches**, not a chain: two
  pages say what a player is and when it runs, and everything else is one
  thing a player *does*. So the part grows from four pages to seven.
  **`player-anatomy` splits** as the pass-2 table and the notebook both
  asked: the vocabulary half keeps the URL, and the two-phase tick —
  record, simulate, snap back — becomes **`the-two-phase-tick`**, a trace
  page, because it is the one thing on the old page nobody would guess.
  **`hunger-xp-and-effects` splits** at the seam the notebook named: status
  effects take **`status-effects`** (own registry, the hidden-effect stack,
  two synched values, the client blend), and the hunger and experience
  halves stay together in **`hunger-and-experience`** — a rename, so the old
  URL is redirected. **The spear gets its own lecture** (`the-spear`),
  discharging the coverage-queue entry: two data components, two entry
  points, two implementations of `LivingEntity.stabAttack`, a mob AI that
  uses it and a first-person animation that reads a combat field — it is
  far more than the two invariants it was, and it is the 26.2 combat change
  a viewer will most want explained. `the-sword-swing` keeps the ordinary
  path and hands both spear paths forward. **`the-sword-swing`'s figure
  becomes a flow over one number** (base damage in, total damage out) as the
  notebook asked, with the sequence kept only for the round trip.
  **The authority matrix leaves Part VIII entirely**: session G gave it a
  page, so `input-to-movement`'s four-method table and `player-anatomy`'s
  authority section are cut to a link, the way `movement-and-collision` was.
  *Done.* **Part VIII is seven pages, up from four**, with a landing page the
  sidebar's Part VIII now opens on. Both splits were free in the sense that
  matters: the material was already written, inside a page doing something
  else, and taking it out put both hosts inside the length brief.
  **`the-two-phase-tick`** took the *when it runs* half and the
  record–simulate–snap-back bracket out of `player-anatomy`, which is the one
  thing on that page nobody would guess and was buried under a class ladder;
  **`status-effects`** took the third of `hunger-xp-and-effects` that shared
  nothing with the other two but a sentence, leaving
  **`hunger-and-experience`** — a rename, so pass 3's first content-page
  redirect. **`the-spear` was written from the decompile**, the session's one
  piece of new research and the only page here pass 2 has never seen: two data
  components (`PiercingWeapon`, `KineticWeapon`) on one item, two entry points
  (a `ServerboundPlayerActionPacket.Action.STAB` carrying **no target id**,
  and item *use* with a 72000-tick duration), one shared filter, and two
  implementations of `stabAttack`. Writing it found the hook the coverage
  queue could not: **`Player.stabAttack` applies the two cooldown curves only
  when the player is not currently using an item in that slot**, so a stab is
  charged like a sword swing and a charging spear ignores the attack cooldown
  entirely. Also worth the trip: `KineticWeapon.forwardMovement` is a combat
  component field read only by the first-person animation, and the non-player
  action factor of 0.2 *lowers* the speed thresholds, so a zombie needs a
  fifth of the closing speed a player does.
  **One pass-2 error found while redrawing.** `the-sword-swing`'s numbered
  damage list gave the crit gate as `Player.canCriticalAttack`; it is
  `fullStrengthAttack && canCriticalAttack`, so the 0.9 scale is part of the
  crit condition. The page's new figure — the damage as a **flow over one
  number**, as the notebook asked — is what exposed it: drawing an ordering
  forces you to say where each factor enters, and the old prose had not.
  **The authority matrix is gone from Part VIII.** Session G gave it a page;
  session I deleted the last two copies (`input-to-movement`'s four-method
  table and `player-anatomy`'s section) in favour of a link plus the two
  consequences each page's own story needs. That closes the notebook's
  three-pages-in-two-parts finding and answers its open question with a
  fourth answer: none of the three candidates — its own page.
  **Lanes.** Six rows added (`Inv`, `FD`, `FP`, `KM`, `KI`, `MEI`) and five
  mis-keyed lanes corrected in the old diagrams — `CL` meaning
  `ServerGamePacketListenerImpl`, `PL` meaning `Player`, `CM` meaning
  `AbstractContainerMenu`, `IS` meaning `ItemStack`, `MG` meaning
  `MultiPlayerGameMode`, each of which already meant something else corpus-wide.
  `check_lanes --strict --pages src/systems/player` is clean, **154 diagrams
  render**, 18,240 names resolve, every relative link in `src/` resolves, and
  the reference indexes are regenerated. Seven pages at 174–410 lines, six of
  them inside the brief for the first time in pass 3; `input-to-movement` is
  the outlier and its seam (client half / server judgement) is logged for
  pass 5. Hand-offs in pass3.md §8, pass4.md and pass5.md.
  Process note: written by the session directly rather than by parallel
  drafting agents, because everything but `the-spear` was pass-2 prose being
  re-cut and the diffing step is the expensive half of that protocol. The one
  page that needed research was researched first, before any page was written,
  which is what made the seven-page rewrite affordable.

- **2026-09-03, out of band — the repo went public-safe.** Not a pass session;
  triggered by the first fork (and star) of the GitHub repo, which made the
  question *what does a stranger get when they clone this* worth answering
  properly. **Nothing was leaking.** `git log --all --diff-filter=A` over the
  whole history finds no file under `reference/`, no jar, zip or class, no
  secret; `tools/deploy.sh` reads the Cloudflare token from `~/.cloudflare/`
  at run time and has never contained one; there are no ```` ```java ```` blocks
  in any of the 132 tracked files, so rule 1 is holding by practice and not
  only by intent. The file most likely to be a problem, `class-index.md` at
  372 KB, is a book index — 2,560 class names against the pages that discuss
  them, no obfuscated pairs, no member signatures — and is not a mappings
  extract.
  **What was missing was a licence.** The repo was all-rights-reserved by
  default, which is the worst of both: a good-faith reader has no safe way to
  quote a page, and a bad-faith one gets to say it looked open. Now
  **CC BY-SA 4.0** for `src/` (the prose and the figures) and **MIT** for
  `tools/`. The owner chose BY-SA over BY-NC-SA on the argument that the real
  threat is an unattributed mirror outranking minecraftdocs.dev, which
  attribution and share-alike prevent and a non-commercial clause does not —
  NC does not even forbid an ad-free mirror, and it costs citations and wiki
  reuse. The cost accepted: someone may build their own videos from these
  notes, but only with visible credit. `LICENSE` is the canonical CC text with
  no preamble so GitHub's detector recognises it; the scope note lives in the
  README instead.
  **The Mojang carve-out is now stated, not assumed.** README and
  introduction both say the licence covers the writing and the figures and
  not the game, its source, its assets or the mappings, and tie that to why
  the pages name identifiers and never reproduce code. `site-footer.js` puts
  that line plus the unofficial/trademark disclaimer on **every** page
  (mdBook has no footer setting, so it appends to each page's `<main>`) —
  every page rather than the introduction alone, because pages are linked to
  and quoted individually and a mirror has to actively strip a footer.
  **Two smaller things.** The introduction's *verified means tested* rule now
  says what the check does **not** prove — that the sentence around the name
  is true — and points at the passes; publishing the pass notebooks means
  that admission is public anyway, and stating it first turns it from a
  gotcha into the method. And the README now has a corrections policy:
  issues with a decompile citation are the wanted contribution, prose PRs are
  not merged, because nothing publishes here that the owner has not read
  against the source, and a merged patch routes around exactly that.
  Process note: session I was running concurrently and its add-all commit
  (`a520d6c`) absorbed the half of this change that existed at the time, so
  the licensing lands in two commits — `a520d6c` and `185f16b`, whose message
  names the first. Worth knowing for pass 4, when sessions may again overlap:
  commit named files as soon as the checks pass rather than batching.

- **2026-09-03, pass 3 session J — Part IX Networking. The ruling, written
  before any edit.** *(the record of what was done follows below)*
  **The part's shape: one wire, three passengers.** The notebook's finding
  (§1, session G) stands with the pages open — Part IX is not two pipelines
  meeting at the wire, it is one pipeline that three unrelated systems ride.
  The landing page draws it that way: a spine of two pages that carry bytes,
  and three pages hanging off it that each have a different shape and a
  different reason to exist.
  **The page list: no splits, no merges, no new pages, no renames** — and so
  no redirects. Five pages, reordered, four of them rewritten.
  1. `the-connection` — **the trace**, and it takes the merge's dividend
     without the merge: the notebook wanted one round-trip diagram, and this
     page gets it (client value → codec → wire → server handler → back),
     because a single picture of the thread hop *and* the codec layer is the
     artefact the pair exists for. Splitting a 550-line page and a 448-line
     one into one 1,000-line page would have failed the length brief on its
     own; the pair becomes **one lecture in two halves** by sharing one
     diagram and one continuous story instead. Half one is the transport.
  2. `packets-and-stream-codecs` — half two, and a **vocabulary page**: what
     a packet *is*, once you know how it travels. It does not redraw the
     journey; its figure is the codec layer itself. Moved to second in the
     sidebar so the two halves are adjacent.
  3. `protocol-phases` — untouched in shape (session A's pilot, a **state
     machine**); re-checked for borrowed facts and links only.
  4. `what-the-client-is-told` — the **policy** page it always was. The
     creeper trace's gate cascade becomes a flowchart of one entity's tick;
     the sequence diagram keeps only the pairing bundle. Its client-coping
     sections go to Part X as links (session G's guess, taken).
  5. `chat-and-signing` — a **protocol with an adversary**, and its figure is
     the three-column table of what each check catches and what dies:
     message, chain, or connection. Its `Component` paragraph becomes a link
     to Part II's `text-components`, which session C wrote.
  **The three borrowed facts are replaced by links, not restated.** The
  broadcast in the chunk-source phase → Part III's `server-level-tick`; the
  second flush after `MinecraftServer.tickChildren` → Part III's
  `server-tick`; the per-frame packet drain → Part I's `anatomy` two-loops
  figure, with Part X's `the-client-loop` as the deeper reference. Session I
  named the first two as Part III's to own; this session is the caller that
  stops restating them.
  **No coverage page.** R7 allows one; the queue holds none for Part IX (the
  debug-subscription question is session K's, since `debugging-the-running-game`
  already lives in Part X), and the budget is better spent on the round-trip
  diagram.

  **What was done.** Five pages, four rewritten, one landing page written,
  no splits and no renames — so no redirects, and the sidebar changed only
  in order: the wire pair is now adjacent and `protocol-phases` follows it
  rather than sitting between its halves. `the-connection` (550→442) is the
  trace and carries the round-trip diagram the merge was wanted for: six
  lanes, four thread boundaries marked, a value leaving the client's main
  thread and the reply arriving back at a drain that runs once per frame.
  Its hook is the one the pair had been sitting on all along — **singleplayer
  serialises every packet to bytes and parses them back**, through a real
  encoder and a real decoder, with the in-memory pipeline differing only in
  the framing and in never installing a cipher.
  `packets-and-stream-codecs` (448→449) is the second half and a vocabulary
  page: it does not redraw the journey, its figure is the codec composition,
  and its hook is that **a packet's id is the position of one line in a chain
  of registration calls** — so the same packet type is a different number in
  each phase it appears in. `what-the-client-is-told` (546→461) became the
  policy page it always was, the buried gate cascade drawn as a flowchart of
  one entity's tick and the old trace reduced to the pairing bundle, which is
  the only part of it that was really a conversation; its client half went to
  Part X. `chat-and-signing` (365→316) is the adversary page: three ways to
  say no, drawn, then eighteen checks in a table whose third column has
  exactly three values — the message dies, the chain dies, or the connection
  dies.
  **The lane ruling was overruled once, correctly.** The session proposed
  `PktE`/`PktD` for the packet encoder and decoder to avoid `PE`
  (`ParticleEngine`); the drafting agent found the key already had
  `PEnc`/`PDec` from `codecs-nbt-json`, satisfying the actual constraint, and
  used those instead of putting two abbreviations on one class. Three
  standing Part IX lane disagreements are now gone; the details are in
  [pass3.md](pass3.md).
  **What went wrong, and what it cost.** Two of the four drafting agents hit
  the account's spend limit *after* writing their pages and *before*
  reporting, so `packets-and-stream-codecs` and `chat-and-signing` were
  accepted on the session's own checks — names, lanes, mermaid, budgets,
  shape, and four load-bearing claims spot-checked by hand — without the
  claim-by-claim diff against pass 2's text that step 4 of the protocol
  requires. That is a real gap, it is written down as one at the head of
  [pass4.md](pass4.md)'s session-J entry, and pass 4 re-checks those two
  pages whole rather than targeting a list. The lesson for the remaining part
  sessions: **an agent's page is worth nothing until its claim list is in
  hand**, so ask for the list first and the prose second, or budget for
  losing the last agent in a fan-out.
  Checks at commit: 18,034 names resolve, 158 diagrams pass, Part IX clean
  under `check_lanes.py --strict`, class index and lane index regenerated.

- **2026-09-03, pass 3 session K — Part X The client. The ruling, written
  before any page was opened.**
  **The part's shape is a hub and its spokes, and every spoke is named by
  its cadence.** Session H's finding, taken as-is: Part X is not a pipeline
  and must not pretend to be. `the-client-loop` is the hub — the one page
  that says when anything on the client runs — and every other page in the
  part answers "when in that loop does *this* happen": per tick, per frame,
  per event, per packet, per sound, per subscription. The landing page's
  figure is that hub with its spokes labelled by cadence, not by hand-off
  order. The one internal pipeline is the GUI stack
  (`gui-and-screens` → `the-gui-render-tree` → `text-and-fonts`), taught
  consecutively, with `hud` as its fourth page — the other recorder.
  **Thirteen pages after one split.** `sound` becomes `sound-engine` (the
  machine: five threads, one OpenAL device, one hop the sound cannot skip)
  and `what-makes-a-sound` (the content model: the three doors a sound comes
  through, and the fact that most world sounds are an int). `sound.md` is
  deleted and redirects to `sound-engine.md`. Session A found the material
  was two pages' worth and did not split; after session H every other page
  in the part is one cadence and one subject, and sound was the only page
  still carrying an engine and a content model. No other splits, no merges,
  no renames.
  **The order, hub first, then the spokes grouped by cadence:**
  `the-client-loop` · `the-client-level` · `prediction-and-acks` ·
  `input-and-keybinds` · `options` · `gui-and-screens` ·
  `the-gui-render-tree` · `text-and-fonts` · `hud` · `sound-engine` ·
  `what-makes-a-sound` · `debugging-the-running-game`. Unchanged from the
  sidebar's order except that the sound pair replaces one page.
  **The shapes, one per page, chosen so no two neighbours read alike:**

  | page | shape | its hook |
  |---|---|---|
  | `README` | landing | — |
  | `the-client-loop` | trace, figure overruled to a **flowchart** | the frame that earns fifteen ticks runs ten and loses five |
  | `the-client-level` | **comparison** — the same `Level` class, two authorities — grounded by the chunk-arrival trace | the client's tick lists accept a schedule, drop it, and then answer *no* when asked whether one is pending |
  | `prediction-and-acks` | **state machine** — a two-column state diagram, ledger entry against server counter | the receipt is for a number, and it is sent for the actions the server refused |
  | `input-and-keybinds` | trace — **holding sneak**, not pressing E | a key press is fully processed before the tick that observes it |
  | `options` | **policy** — saving *is* the event system | a cycle button broadcasts your client information on every click |
  | `gui-and-screens` | **vocabulary page**, grounded by pressing E | the survival inventory is opened entirely client-side, and its menu has no `MenuType` |
  | `the-gui-render-tree` | **vocabulary page** — a figure of the tree, not of time | layering is inferred from bounding boxes and never declared |
  | `text-and-fonts` | **pipeline** — six stages from a `Component` to a quad | measuring text bakes a glyph and uploads a texture |
  | `hud` | **policy** — what is drawn, when, and what F1 does not hide | F1 does not hide the sleep fade |
  | `sound-engine` | trace — a block placed near you, through five threads | a sound always starts at least one hop after the packet, even on a cache hit |
  | `what-makes-a-sound` | **comparison** — three doors | most world sounds are an int, and your own sounds never round-trip |
  | `debugging-the-running-game` | **the pattern** — one subscription, sixteen instances, one traced | none of it is stripped from the shipped jar; the client simply never asks |

  **Two diagram-shape overrules, both session H's.** `the-client-loop`'s
  trace is a *loop* and a sequence diagram cannot say so — its most
  important fact, that ticks are dropped, was living in a label on a bounded
  block. It becomes a flowchart with the clamp as a decision node and the
  drop as its own box. `the-gui-render-tree`'s subject is a tree with a
  placement rule, and its sequence diagram was a flowchart in a sequence
  diagram's clothes; it becomes two flowcharts, one of the data and one of
  the draw pass. `prediction-and-acks` gains the two-column state diagram
  session H asked for and keeps the refusal sequence as its second figure —
  the one page in the part with two figures of different kinds, because the
  ledger's *state* and the packet *ordering* are two different claims.
  **`hud`'s gate table goes to Reference**, as `src/reference/hud-elements.md`
  — the twenty-two elements of the HUD in record order with the condition
  each is gated on, which is exactly the thing R5 says a viewer would pause
  the video to read. `hud` keeps the two-block structure as a flowchart and
  links.
  **`prediction-and-acks` and `text-and-fonts` stay in Part X**, overruling
  session H's own observation that they would sit equally well in Parts IX
  and XI. The packaging argument is weak, but the *watching* argument is
  not: Part V's landing page already rules that Part V is watched before
  `prediction-and-acks`, so moving the page into Part IX would put it before
  its own two applications, and `text-and-fonts` is the only page a viewer
  can watch after Part II's `text-components` without having seen a single
  render pass. Both are recorded as answered open questions in
  [pass3.md](pass3.md) §6.
  **`debugging-the-running-game` is placed, and stays where it is.** Session
  H asked whether the debug subscription system belongs to Part IX (a server
  push), Part X (the client draws it) or a part of its own. It is Part X's,
  as the part's closer, for the reason the page already gives: the
  machinery ships on the dedicated server, but the client is the only thing
  that ever asks and the only thing that draws, and the page's trace ends in
  a renderer. It is the part's one **pattern** page, which is also why it
  closes rather than opens.
  **No coverage page.** R7 allows one; the queue's only Part X entry is
  *world creation and the world-select screens*, ~5,100 lines that session J
  found spanning Parts X and XII. It is ruled **not this session's**: half of
  it is worldgen's world-creation settings and half is a screen family, and
  splitting the subject across two part sessions is how the corpus grew its
  duplications. It stays in the queue with that reason, for session M and
  session P to co-rule. The sound split is a confirmed split, not new
  coverage, and spends no allowance.
  **What session J handed over is checked, not assumed.** Session J's
  hand-off lists six `ClientLevel` facts that left `what-the-client-is-told`
  for Part X; each is confirmed present in `the-client-level` or added, and
  the one with no owner anywhere in the corpus —
  `Entity.moveOrInterpolateTo` and which entity families supply an
  `InterpolationHandler` — is written into `the-client-level` this session.

  **What was done.** Thirteen pages where there were eleven: twelve system
  pages plus a landing page, one split, one new Reference page, and no
  renames beyond the split — so one redirect (`sound.html` to
  `sound-engine.html`) and a sidebar that now folds onto a real page. Every
  page lost the seven-heading skeleton, the field inventories and the
  invariants bullet wall; the material went into a cast table, into the
  sentence that touches it, or into a *questions players ask* section, and
  the *headline for a 1.21-era reader* formula that opened seven of the
  eleven pages became a blockquote at the foot of each. Six shapes are in
  use across the twelve pages — trace, comparison, state machine, policy,
  vocabulary, pipeline and pattern — and no two neighbours share one.
  **Three diagrams were the wrong shape and are now right.**
  `the-client-loop`'s loop is a flowchart with the ten-tick clamp as a
  decision node and the dropped ticks as their own box, which is where its
  hook now lives instead of in a label on a bounded block. `prediction-and-acks`
  gained the two-column `stateDiagram-v2` session H asked for — a ledger
  entry's five transitions against a connection counter's three — and kept
  the refusal sequence beside it, because the ledger's *state* and the
  packet *ordering* are two different claims and only the second is a
  conversation. `the-gui-render-tree` became two flowcharts, one of the data
  and one of the draw pass, in place of a sequence diagram that was a
  flowchart in disguise.
  **Redrawing the loop found a real error.** The old sequence diagram put
  `FramerateLimiter.limitDisplayFPS` at the end of `Minecraft.runTick`,
  after *Post render*. It is inside `Minecraft.renderFrame`, after the
  present and before *Post render*. Session B's lesson holds — suspect the
  page, not only the tool — and the correction is at the head of
  [pass4.md](pass4.md)'s session-K entry so pass 4 checks it first, along
  with `the-frame`, which may have inherited the same mistake.
  **Session J's hand-off was checked rather than assumed, and one item was
  missing.** Five of the six `ClientLevel` facts handed over from
  `what-the-client-is-told` were present. The sixth —
  `Entity.moveOrInterpolateTo` and which entity families supply an
  `InterpolationHandler` — had no owner anywhere in the corpus and is now a
  table in `the-client-level`: seven overrides against a default that
  returns null and therefore snaps, which is why a dropped item moves
  differently from a mob over the same connection. Two smaller gaps were
  filled at the same time: `ClientPacketListener.serverChunkRadius` and
  `ClientPacketListener.serverSimulationDistance`, and the torus's
  `AtomicReferenceArray` and volatile centre.
  **`hud`'s gate table is the R5 precedent.** Twenty-two HUD elements plus
  the four `Gui` records after them, in record order, with the condition
  each is gated on: `src/reference/hud-elements.md`. It answers section 6's
  open question about reference-tier tables inside lecture pages with *no,
  a Reference page and a link* — which is the answer session L needs for the
  render-state hierarchy and session N for the selector grammar.
  **No coverage page, deliberately.** The queue's only Part X entry spans
  Parts X and XII, so it is deferred to session M with the worldgen half in
  front of it rather than declined; the reason is written into
  [pass3.md](pass3.md) §7's discipline note rather than only here.
  Checks at commit: 17,869 names resolve, 165 diagrams pass, Part X clean
  under `check_lanes.py --strict`, the corpus-wide lane count down from 25
  disagreements and 16 collisions to 19 and 10, class index and lane index
  regenerated, `mdbook build` clean and no broken internal links.
- **2026-09-03, session L — Part XI Rendering.** *Rulings, written before
  editing.* **The part is a substrate under a pipeline, and the order is
  R6's.** `the-frame` opens — it is the part's trace and its shortest page,
  and a reader who has seen one frame end to end has a reason to care what a
  `GpuDevice` is — then the substrate (`the-window`, `blaze3d`), then the
  pipeline. Session I's two open questions are closed with it: **the
  substrate is two lectures, not one** (a GLFW window, its six callbacks and
  `NativeImage` are a different subject from a graphics API with two
  backends, and neither hook survives being merged with the other), and
  **`the-window` stays in Part XI**, second, rather than moving to Part I —
  it is a rendering prerequisite, not a program-anatomy one, and Part I is
  deliberately two pages.
  **`level-rendering` splits, and it is the corpus's oldest deferred seam.**
  Four sessions (10, H, I and the split table) confirmed *meshing* against
  *visibility and the frame graph* and none executed it; pass 3 is the pass
  that executes splits, and the page fails the cast budget twice over — its
  two halves share `LevelRenderer` and nothing else. The halves are
  **`visibility-and-the-frame-graph`** (what the frame draws: the occlusion
  BFS over an `Octree`, the frustum, the pass declaration order, the
  multi-draw batching and the translucency resort) and **`section-meshing`**
  (where the triangles came from: the dirty halo, the 27-section snapshot,
  the worker compile, the staging buffer and the late atomic swap).
  Visibility comes first, because it continues `the-frame` — which ends at
  `LevelRenderer.render` — and because meshing is gated on it. The old URL
  redirects to the visibility half (R8).
  **The R7 page is post-processing**, session I's strongest candidate: 996
  lines in four classes named on no page, six `post_effect` chains now in
  `reference/26.2/assets/` to write it against, and the only place in the
  game where user-authored shaders are first class. It is the part's closer,
  because its instances are spread across every page before it — two chains
  declared inside `LevelRenderer.render`, three chosen by
  `GameRenderer.checkEntityPostEffect`, one behind a pause screen.
  Block-entity rendering stays queued; **"how an item picks its model"
  becomes a named section of `models-and-atlases`**, not a page, which is
  what session H's hand-off requires — Part VII's two forward links now land
  on a heading rather than a page that only mentions `ItemModelResolver` in
  passing.
  **Shapes, one per page, no two neighbours alike.** `the-frame` the trace;
  `the-window` the trace with the retry loop drawn as the flowchart the
  notebook asked for; `blaze3d` the **vocabulary page** (the façade and its
  four objects, grounded by one draw); `visibility-and-the-frame-graph` the
  pipeline; `section-meshing` the trace; `models-and-atlases` the pipeline,
  with the fan-out/barrier figure the notebook asked for; `entity-rendering`
  the pipeline (extract, submit, prepare, execute); `lightmap-fog-and-sky`
  the **pattern** — one question (*what is this attribute worth, here,
  now?*) asked by five renderers, which is what lets the page stop
  re-teaching Part IV's system; `particles` the **policy**, because its
  subject is five gates that disagree with each other; `post-processing` the
  pipeline.
  **Two Reference extractions, on session K's precedent** (a reference-tier
  table is a Reference page and a link, never a table inside a lecture):
  `entity-rendering`'s fifteen submit phases and thirteen feature renderers
  become `src/reference/submit-phases.md`, and its render-state hierarchy
  becomes a **generated** tree figure — `EntityRenderState` joins
  `TREE_ROOTS` in `map_source.py`, the pattern session G set with
  `tree-Entity.svg`. `lightmap-fog-and-sky`'s twenty-four-attribute
  enumeration is not extracted but dissolved: the page names the attributes
  in the sentences that use them and links to Part IV for the system.
  **Lanes: eleven collisions fixed, all by lengthening the later claimant.**
  `SectionCompiler` → `SectC` (`SC` is `StopCommand`), `Timelines` → `Time`
  (`TL` is `TagLoader`), `LightmapRenderStateExtractor` → `LRSE` (`LX` is
  `LevelExtractor`, keyed by session K), `SpriteLoader` → `SprL` (`SL` is
  `ServerLevel`), `GlCommandEncoder` → `GlCE` and `GpuBackend` → `GB` (`B`
  is `Block`, which particles should have been using), `MonitorManager` →
  `MonM` (`MM` is `ModelManager`), `GpuSurface` → `GpuS` (`GS` is
  `GaussianSampler`), `EnvironmentAttributeProbe` → `EAP` (keyed already;
  `P` was wrong), `Minecraft` → `MC` and `Window` → `Window` (both keyed
  already; `M` and `W` were wrong), and `(worker)` takes the existing word
  lane `Worker`.

  **What was done.** Thirteen pages where there were eight: eleven system
  pages, a landing page and a new Reference page. One split executed
  (`level-rendering` → `visibility-and-the-frame-graph` + `section-meshing`,
  one redirect), one page written from nothing (`post-processing`), one
  section written to discharge a ruling (*How an item picks its model*, which
  Part VII's two forward links now reach by anchor), one catalogue extracted
  (`src/reference/submit-phases.md`) and one figure generated
  (`tree-EntityRenderState.svg`, from `EntityRenderState` added to
  `map_source.py`'s `TREE_ROOTS`). Every page lost the seven-heading
  skeleton, and the part now has **zero bulleted lists in it** — eight pages
  each opened with a field inventory and closed with a twenty-bullet
  invariant wall, and all of that is now cast tables, decision tables,
  *Questions players ask* sections and the sentences that use each name.
  **Every page landed inside the 260–340 brief**, 256 to 339, which is a
  first; the brief went to the drafters in the prompt rather than as a
  correction. Six shapes across eleven pages — trace, vocabulary, pipeline,
  pattern, policy and the landing page — and no two neighbours share one.

  **Redrawing found two errors, which is three sessions in a row.** The first
  is the more instructive. `the-window` said that three of the six
  operating-system callbacks reach the game through `WindowEventHandler`;
  **only two do**, and the interface's third method, `resizeGui`, is never
  called by `Window` at all — its callers are `Minecraft` and `Options`,
  calling the game on itself. The old claim was an inference from three
  method names lining up with three callbacks, and it survived pass 2 because
  nobody had to *draw* it. The second: `level-rendering` gave
  `SectionOcclusionGraph.invalidateIfNeeded`'s triggers (an eight-block
  camera move, a field-of-view change, the smart-cull toggle) as the reason
  `LevelExtractor.applyFrustum` re-runs. Those schedule the **full walk**;
  the frustum step has its own gate, and the common half of it is the
  camera's pitch or yaw crossing a **two-degree** step — so turning your head
  re-applies the frustum without touching the walk. Both are fixed in the
  pages and are at the head of [pass4.md](pass4.md)'s session-L entry. The
  lesson for the remaining part sessions: **a figure asserts more than the
  prose it was drawn from**, which is the argument for drawing them.

  **The R7 page is `post-processing`, and it earned the slot.** 996 lines in
  four classes that no page named, six shipped chains, written against the
  JSON the planning session staged in `reference/26.2/assets/`. Its findings
  are the kind a coverage queue entry cannot predict: a chain's uniforms are
  packed and uploaded **once, at load**, so anything that has to vary per
  frame — the blur radius, for one — cannot be a chain uniform at all and has
  to come through the global block; the per-entry *name* in the JSON is read
  by no codec, only the type and the value, and members match the GLSL
  positionally; a resource pack can rewrite all six chains and add none,
  because the six ids are constants in Java; and the two chains that go
  through the deprecated `PostChain.process` door build a throwaway frame
  graph with no inspector, so **the pause blur and the spectator shaders
  appear in no slice of the F3 pie chart**.

  **Two more numbers were corrected in passing**, both cases of a page
  disagreeing with the corpus rather than with the decompile. `blaze3d`
  compared the backends at 7,461 lines against 5,623; they are 7,477 and
  5,627, and `what-this-book-skips` was already saying 7,477. And the landing
  page could not reproduce session I's "1,187 classes / 97,864 lines" for the
  rendering tree — the inventory never said which packages it counted — so
  the page states its own package set and counting rule and gives 1,179 and
  87,000, which is CLAUDE.md's own table added up.

  Checks at commit: 17,694 names resolve, 174 diagrams pass, Part XI clean
  under `check_lanes.py --strict` with thirty-three lane rows added (the
  pass's largest single addition, eleven of them lengthened later claimants),
  the corpus-wide lane count down from 19 disagreements and 10 collisions to
  15 and 6, class index and lane index regenerated, `mdbook build` clean and
  no broken internal links.
- **2026-09-03, session M — Part XII World generation.** *Rulings, written
  before editing.*

  **The part is a substrate, a pipeline and a wing.** Session J's §1 read is
  confirmed with the pages open: `density-functions` is not a step, it is the
  material every other page is made of, and the genuine sequence underneath
  it is biomes → noise/surface/carvers → features. What §1 did not name is
  that the three structure pages are not a fourth stage of that pipeline —
  they are a parallel wing that starts *earlier* than any of it
  (`ChunkStatus.STRUCTURE_STARTS` is the second status, two before
  `ChunkStatus.BIOMES`) and finishes inside `ChunkStatus.FEATURES`. So the
  part has two halves, terrain and structures, exactly as the schedule says,
  and the landing page draws them against the status ladder so that the
  lecture order and the execution order are visibly not the same thing.

  **`density-functions` still opens the part, against session L's
  evidence.** R6 ruled it and session L offered Part XI's counter-argument
  (open with the trace, then the substrate, then the pipeline, because a
  reader who has seen one frame end to end has a reason to care about
  `GpuDevice`). It is a real argument and it loses here for the reason
  session L itself gave: Part XII's substrate is genuinely prerequisite
  rather than merely underneath. `biomes` cannot explain the climate sampler
  without it, and `terrain`'s aquifer, ore veins and beardifier are all
  density terms. What Part XI's *frame* page bought — the whole shape before
  the abstract part — is bought here by the **landing page**, which carries
  the one-chunk overview figure. That is the ruling: the overview is the
  landing page's job in a part whose substrate is load-bearing, and no
  content page is spent on it.

  **Part XII stays one part.** §1 raised Part XII-A / XII-B, or promoting
  structures. R1 forbids a new numbered part this pass, and with the split
  executed the part is eight pages — the same size as Parts IV and XI — so
  the halves are a landing-page fact, not a numbering one.

  **The page list after the session** (eight content pages, one landing
  page, one new Reference page):

  | page | shape | hook |
  |---|---|---|
  | `README.md` *(new)* | the landing page | the status ladder, and why the lecture order runs against it |
  | `density-functions.md` | the pipeline (three rewrites) | the graph in the registry never runs as written, and a caching marker does not cache |
  | `biomes.md` | the trace, with one comparison section | there are two biome borders a couple of blocks apart, and block tint is on the side nobody guesses |
  | `terrain.md` *(renamed from `worldgen-pipeline.md`)* | the pipeline (noise · surface · carvers) | the carver does not choose the block it carves — the aquifer does |
  | `features-and-placement.md` | the trace (a stream of positions) | two biomes that disagree about feature order make the world refuse to open *(landed here rather than on count-then-scatter — see below)* |
  | `trees.md` *(new — the R7 spend)* | the pattern | the dark-oak sapling that never grows alone, which is an `Optional` left empty |
  | `structure-placement.md` *(from `structures.md`)* | the policy | the grid never looks at the world, and absence is stored as a hole rather than a marker |
  | `jigsaw-and-templates.md` *(from `structures.md`)* | the trace (a village) | a village stops growing because at the depth limit the assembler is offered only the fallback pool |
  | `hand-built-structures.md` | the pattern (four families, one traced) | a stronghold is a rejection sampler — no portal room, and the whole thing is thrown away and regenerated |
  | `src/reference/density-function-nodes.md` *(new)* | Reference | — |

  **`structures` splits three ways, not two.** The schedule says placement
  and jigsaw beside `hand-built-structures`, and the seam that survives
  contact with the page is: everything that is true of all sixteen structure
  types goes to `structure-placement` (the lottery, `StructureSet`,
  `StructurePlacement`, `ChunkGeneratorStructureState`, `Structure`,
  `StructureStart`, the reference scan, `StructureCheck`,
  `StructureManager`, `Beardifier`, `/locate`, and the per-chunk write), and
  the `.nbt` template system goes with **jigsaw** rather than staying in the
  framework page, because a template is how a pool element becomes blocks
  and the hand-built families reach it by link. `hand-built-structures`
  already declared that boundary from the other side and now points at the
  right page.

  **`worldgen-pipeline` is renamed `terrain`.** Two pages called *pipeline*,
  one the conveyor (Part IV) and one the cargo (Part XII), is a name
  collision that costs a reader the whole distinction the split was made
  for. Redirect kept under R8.

  **The catalogue extraction is the node families**, to
  `src/reference/density-function-nodes.md` — §1's "the rewrite story is the
  lecture, the node families are reference", executed. Hand-kept, for
  session O's sweep.

  **The R7 spend is the tree kit** (`trees.md`), the coverage queue's
  "probably the most watchable page in Part XII": fifty classes and ~3,000
  lines of `TrunkPlacer` / `FoliagePlacer` / `RootPlacer` / `TreeDecorator`
  implementations that `features-and-placement` documents as five contracts
  and zero instances. It also relieves that page, which is over-budget with
  tree material.

  **The world-creation ruling session L asked for.** *World creation and the
  world-select screens* (~5,100 lines, zero citations) is **one lecture and
  it belongs to Part XII**, not Part X: the subject is `WorldGenSettings`,
  `WorldDimensions`, `WorldOptions`, `levelgen/flat` and `levelgen/presets`,
  and `client/gui/screens/worldselection` is that subject's user interface —
  a Part X page would have to teach worldgen settings before it could
  explain a single screen. It is **not** written this session (the R7
  allowance went to the trees, which is a lecture rather than a settings
  tour) and stays in the queue with Part XII named as its owner, for session
  P or pass 6.

  **What was done.** Ten pages where there were six: eight system pages, a
  landing page and a new Reference page. One split executed (`structures`
  → `structure-placement` + `jigsaw-and-templates`), one page renamed
  (`worldgen-pipeline` → `terrain`), two redirects, one page written from
  nothing (`trees`, the R7 spend) and one catalogue extracted
  (`src/reference/density-function-nodes.md`). Every page lost the
  seven-heading skeleton and the part now has **zero bulleted lists in it**.
  Lengths 204 to 288 against the 260–340 brief — the first part to
  *undershoot* it, three pages under 240, which is worth noticing rather
  than fixing: the structure pages are short because the split gave each of
  them one subject.

  **Two hooks moved off the plan above while writing.**
  `features-and-placement` was slated for count-then-scatter and opens on
  the global sort instead — a data pack that makes the world refuse to open
  is the more surprising true thing, and count-then-scatter survives as a
  named paragraph. `trees`, whose hook the table could not name before the
  source inventory came back, opens on `TreeGrower.DARK_OAK`: the
  best-known growth rule in the game, that a lone dark-oak sapling never
  grows, is implemented as an `Optional` left empty.

  **Redrawing found two errors, which is four sessions in a row, and both
  are counts.** `features-and-placement` said sixty-three features are
  registered; it is **61**. And it called `CountOnEveryLayerPlacement` "the
  fifteenth" of the fifteen placement modifier types — there are fifteen,
  but it is **ninth** in declaration order, so the ordinal is wrong where
  the count is right. Both are fixed and both head
  [pass4.md](pass4.md)'s session-M entry. The generalisation for the
  remaining sessions: pass 2 checked counts and did not check **ordinals**,
  and an ordinal is a count with an extra claim in it.

  **The R7 page is `trees`, and the coverage queue's own framing was
  wrong.** The entry promised "how one species of tree differs from
  another" and the page that came out is mostly about what they *share*: one
  `final` algorithm with five codec-dispatched slots, and an asymmetry
  inside it that no configuration can reach — `TreeFeature` samples a
  proposed height, sizes the foliage height and leaf radius from it, and
  only then runs the clearance scan, so a clipped tree grows a short trunk
  under a full-size crown and every one of the eleven foliage placers
  ignores the clipped height it is handed. Three more findings the queue
  could not have predicted: `FancyTrunkPlacer`'s crown-candidates-per-level
  count is pinned at one by a minimum against one, so its named density
  constant does nothing at any height; `CherryFoliagePlacer`'s codec gives
  its *corner hole chance* field a getter that returns the *wide bottom
  layer* field, so decoding is right and any encode writes one value into
  both; and `TreeGrower.PALE_OAK` points at the decorator-free bone-meal
  variant, so a player-grown pale oak gets neither moss nor a creaking
  heart.

  **Three of the part's lane collisions were settled by not drawing a
  sequence.** `terrain`, `density-functions` and `structure-placement` all
  chose flowcharts, and `SS` — which meant `SurfaceSystem`, `StructureStart`
  and `StrongholdStructure` on three adjacent pages — is now used by none of
  them and left free for Part XIII's `ServerScoreboard`. Twenty-eight rows
  added, seven lengthened later claimants, two claimed against unconverted
  Part XIII (`CA`, `CF`). Part XII is clean under `check_lanes.py --strict`
  and the corpus-wide count fell from 15 disagreements and 6 collisions to
  **7 and 1, every one of them in Part XIII**.

  **The world-creation ruling** session L asked for is above and is recorded
  against the queue entry in [pass3.md](pass3.md) §7: one lecture, Part
  XII's, not written this session.

  Checks at commit: 17,335 names resolve, 179 diagrams pass, Part XII clean
  under `check_lanes.py --strict`, class index and lane index regenerated,
  `mdbook build` clean and no broken internal links across `src/`.

- **2026-09-03, session N — Part XIII Commands and data packs.** *(rulings
  written before any editing, per protocol step 2.)*

  **The part is a stack with three floors**, and the landing page says so:
  *parse* (`brigadier-and-commands`, `permissions`) → *execute*
  (`the-execution-engine`, `functions-and-macros`) → *what commands are for*
  (`advancements`, `scoreboard-and-data`, `dialogs`, `game-tests`). The
  dependency is strictly one-directional, which is why the third floor's four
  pages are peers rather than a sequence.

  **Nine pages where there were five**, with the shape and the hook decided
  first:

  | page | shape | hook |
  |---|---|---|
  | `README.md` | landing | — (the three floors, drawn) |
  | `brigadier-and-commands` | trace — `/give` | the client parses every keystroke against a real dispatcher and throws the answer away; the round trip is the default, not the fallback (62 of 67 providers) |
  | `permissions` **(new, the R7 spend)** | vocabulary | an op does not have everything: `LevelBasedPermissionSet` grants exactly one atom, and a permission failure is reported as an unknown command |
  | `the-execution-engine` | trace + queue snapshots | `/return` deletes work out of a queue instead of unwinding a stack, and a fork creates no frames at all |
  | `functions-and-macros` | pipeline — file → compiled → instantiated → queued | a macro function reached with no arguments fails silently, every tick, forever |
  | `advancements` | trace — "Stone Age" | the subscription table only ever shrinks, and the client is told the requirements but never the criteria |
  | `dialogs` | trace | a server can put a form in front of you *before you are in a world*, and the pause validation then runs on the client |
  | `game-tests` | vocabulary | the annotations are gone, a batch **is** an environment, and the shipped jar contains exactly one test |
  | `scoreboard-and-data` | trace — `execute store` | a player's score is keyed by their name and a mob's by its UUID, in one flat map |

  **Three splits, all confirmed by the notebook and named in the schedule:**
  `brigadier-and-commands` → + `permissions`; `execution-and-functions` →
  `the-execution-engine` + `functions-and-macros`; `dialogs-and-tests` →
  `dialogs` + `game-tests`, which is now safe because
  [the data-driven type pattern](../src/systems/foundations/data-driven-types.md)
  exists in Part II and owns the argument that held the page together.

  **The R7 allowance is spent on `permissions`** — it is in the coverage
  queue, it is the biggest API break in the corpus and four sessions running
  named it as the cleanest seam. The function model and the dialogs/tests
  split are executed as *splits* (§2's split table), not as coverage
  additions. The **selector grammar** and **`GameTestHelper`** stay queued.

  **Advancements' client screen stays a section**, and becomes the page's
  closing one. It is six classes of user interface whose only mechanism —
  a tree the server laid out and shipped — is already the page's subject; a
  page of its own would be a screen tour, and Part X owns screens. What it
  gets instead is the last word, where a viewer sees the data structure they
  already know from playing.

  **The predicate-shape library stays on `advancements`**, trimmed.
  `contexts-and-predicates` (Part VII) owns the context machinery and does
  not own `MinMaxBounds`, `CollectionPredicate`, `EntitySubPredicate` or
  `DataComponentMatchers`; advancements is their biggest consumer, so they
  stay where they are read and go to [pass3.md](pass3.md) §7 as a Reference
  candidate for a later pass.

  **`scoreboard-and-data` stays one page**, and the scoreboard stays in Part
  XIII (R6). The scores/teams and paths/storage halves are joined by
  `execute store`, which is the page's only trace; split them and neither
  half has one.

  **What was done.** Nine pages where there were five: eight system pages
  and a landing page. Two splits executed (`execution-and-functions` →
  `the-execution-engine` + `functions-and-macros`; `dialogs-and-tests` →
  `dialogs` + `game-tests`), both redirected under R8; one page written from
  nothing (`permissions`, the R7 spend); and the remaining four pages
  rewritten end to end. Every page lost the seven-heading skeleton and every
  diagram in the part is new or redrawn. The part now has **one bulleted
  list in it** — a two-item list on the engine page — where it had eleven
  bullet walls.

  Lengths 131 to 371 against the 260–340 brief, and the distribution is the
  honest result of the splits: `dialogs` (174), `game-tests` (178) and
  `functions-and-macros` (189) undershoot because each now has exactly one
  subject, and `scoreboard-and-data` (371) is the one page that overshoots —
  which is the split this session declined, arguing back. The part's total is
  2,129 lines against the old 2,150, so nothing grew; it redistributed.

  **The R7 page is `permissions`, and writing it changed the claim.** The
  queue promised "the biggest API break in the corpus" and that is true, but
  the page's actual subject turned out to be an asymmetry nobody had named:
  the server's permission model is **additive** — a rung, plus exactly one
  hard-coded atom, unioned upward, and `LevelBasedPermissionSet.union` of two
  level sets is just the higher of the two — while the client's chat model is
  **subtractive**, starting from all four chat atoms granted and letting each
  of four purely local `ChatRestriction`s remove some. No packet carries a
  `PermissionSet` in either direction. The consequence is the page's second
  half: the client can only ever learn *"this needed some permission"*, and
  it learns even that by parsing the same string twice, once with its own set
  and once with `PermissionSet.NO_PERMISSIONS`, and reading the difference.
  One exception proves the rule — `GameModeCommand.PERMISSION_CHECK` is
  exported so that `KeyboardHandler` and `GameModeSwitcherScreen` can run a
  *server* check locally, which is why the F3+F4 switcher greys out.

  **Rewriting found three count errors, which is five sessions in a row.**
  Pass 2's "all ninety-four *requires* calls in the game use
  `Commands.hasPermission`" was a true statement about the server made as a
  statement about the game: `.requires(` appears 245 times, and 150 of those
  are `ShapelessRecipeBuilder.requires`. There are **95**
  `Commands.hasPermission` call sites — 94 server-side registrations plus
  one on the *client*. `advancements` said the client half was "six classes
  … (`net/minecraft/client/gui/screens/advancements`)", which counted
  `package-info.java` and put `ClientAdvancements` in the wrong package; it
  is five classes there plus `ClientAdvancements` in `client/multiplayer`,
  about 1,240 lines. And the worst of the three, because a sentence's
  argument rested on it: `scoreboard-and-data` said `execute store` has
  **two** sinks "which are exactly the two models here". It has **three** —
  `ExecuteCommand.wrapStores` builds score, boss bar, and the three data
  providers. The generalisation to carry: pass 2 checked counts inside a
  page's own scope and did not check counts used as *arguments for the page's
  shape*, which are the ones a restructure leans on hardest.

  **Two rulings the schedule asked for.** *Advancements' client screen* stays
  a section and becomes the page's closing one — six classes of user
  interface whose only mechanism is a tree the server laid out, which is
  already the page's subject; a page of its own would be a screen tour, and
  Part X owns screens. *`scoreboard-and-data` stays one page*, which also
  answers §1's older question about whether the scoreboard belongs to Part
  XIII at all: R6 said it stays, and the page's only trace is a command. The
  boss bar and the statistics are still the two subjects with no owner
  anywhere in the corpus.

  **The lane gate is now green corpus-wide.** Twenty-six rows added, and
  Part XIII took the three short forms Part XII deliberately left free (`SS`
  for `ServerScoreboard`; `SP` stays `ServerPlayer`). Seven later claimants
  lengthened (`CSug`, `CAdv`, `CallF`, `ContT`, `GTR`, `DlgS`, `CComPL`) and
  four bare-initial lanes the old diagrams used were retired under the
  two-letter rule (`C`, `M`, `T`, `R`). `python tools/check_lanes.py` reports
  **537 participants, 0 disagreeing and 0 colliding, across the whole
  corpus** — session P can turn `--strict` on unconditionally. One collision
  is recorded and deliberately not drawn: `ExecuteCommand` names two
  unrelated classes, and the key resolves simple names, so the engine page
  names the task in prose and never as a lane.

  Checks at commit: 17,056 names resolve, 184 diagrams pass, Part XIII **and
  the whole corpus** clean under `check_lanes.py --strict`, class index and
  lane index regenerated, `mdbook build` clean, and no broken internal links
  across `src/`. Hand-offs written to [pass4.md](pass4.md) (the three count
  corrections first, then thirteen new source-derived claims and every
  redrawn figure), [pass5.md](pass5.md) (the cuts, and second person now five
  parts wide) and [pass3.md](pass3.md) (two queue entries discharged, one
  opened, and the notes for sessions O and P).
- **2026-09-03, session O — Reference.** *(rulings written before any
  editing, per protocol step 2.)*

  **The Reference tier's shape is a shelf, not a sequence**, and the README
  becomes its landing page in the landing-page shape: one paragraph on what
  the tier is for (the rule is R5's — *would a viewer pause the video to
  read this*), a figure of the shelf with the pages grouped by **how each is
  kept** — generated from the decompile by `gen_reference.py`,
  generated from the corpus by `verify_names.py --index` and
  `check_lanes.py --index`, or hand-kept and therefore re-swept every pass —
  no *watch in this order* (nothing here is watched), and instead *which
  parts lean on which page*, from the landing pages' own *Reference this
  part uses* sections. Under a hundred lines.

  **The tier gets name-verified.** `verify_names.py` has skipped every page
  under `reference/` except `threads.md` since pass 1, so the four hand-kept
  catalogues the part sessions wrote this pass (`non-living-damage`,
  `hud-elements`, `submit-phases`, `density-function-nodes`) and the four
  look-up pages have never been checked. The rule becomes: a reference page
  is checked unless its header says the tool wrote it; `class-index` and
  `lanes` are the two other exceptions. A dry run finds sixteen failures,
  all in the four catalogues, all qualification (`hurtServer` for
  `Entity.hurtServer`, the five marker types bare, ids in backticks).

  **The glossary is re-swept, not generated.** A per-page term declaration
  would be a new convention across ninety pages, seeded by hand once and
  then checked by pass 4 exactly as a hand-kept glossary is; the cheap
  mechanism R5 hoped for does not exist. One agent audits every entry
  against its owner page and the decompile and lists the missing terms
  (sessions M and N named eight); the session applies the sweep. The
  glossary stays the terminology checklist for pass 5.

  **The moved pages are reframed, not rewritten.** `math-and-primitives`
  gets the coordinate-spaces figure session A asked for — the spaces as
  nodes, the conversions as edges, drawn from its own table — and headings
  that say what the section says; `level-data-and-rules` is reshaped around
  its who-owns-what table (the table first, one prose section per row group
  after it, the surprises placed where they happen); `naming-drift` and
  `glossary` lose the *Responsibility* heading and keep their tables.
  Every claim carried; the figure is the only addition.

  **The eight `ClientPacketListener` handlers that never hop go to
  `threads.md`** (session J's deferred question, twice handed on), as a
  short table beside the Netty row, because an enumeration a viewer pauses
  on is Reference and the rule is already stated on `the-connection`. The
  decompile confirms the count: 115 handlers call
  `PacketUtils.ensureRunningOnSameThread` and 8 do not.

  **One extraction executed, four declined.** The update-flag bit table
  leaves `blocks-and-states` for `reference/block-update-flags.md`
  (session F's stronger candidate; ten rows plus the named combinations,
  hand-kept, `Block`'s declaration lines). The block-event users stay a
  paragraph on `pistons-and-block-events`; the nineteen
  `EntitySpawnReason` constants, the spawn-list override and the predicate
  shape library go to the coverage queue as Reference candidates — three of
  the four are generation candidates and want `gen_reference.py` views, not
  hand-kept tables.

  **The hand-kept catalogues are not re-swept here.** R5 says pass 4; each
  was read one class at a time by its part session within the last two
  days, and a second read today would be the same reader. They go to
  pass4.md as a standing item with the verifier now behind them.

  **Tool fixes in passing:** the treemap hatches a skipped depth-3 package
  that draws no leaf (session B's note; `gizmos` and `realms` today), so the
  figcaption on *what this book skips* becomes true; `gen_reference.py
  all` re-run and every blurb's link checked; the class index and lane
  index regenerated.

  **What was done.** Twenty-one reference pages where there were twenty,
  and a landing page where there was a list. `reference/README.md` is a
  landing page in the landing-page shape: the shelf drawn as a figure of
  who writes each page, and a table of every page with what it lists, how
  it is kept, and which parts' landing pages point at it. One page written
  from an extraction (`block-update-flags`, session F's candidate, moved
  verbatim out of `blocks-and-states`, which keeps two sentences and a
  link). Four pages reframed: `level-data-and-rules` drafted by an agent
  around its table — the who-owns-what table first, six prose sections and
  two subsections behind it, the eleven surprises merged into the sections
  where they happen, zero bullets where there were six lists, 294 lines
  where there were 294, and a claim-diff that found one reworded sentence
  worth pass 4's eye (game time "comes to be shared" through
  `DerivedLevelData`); `math-and-primitives` with the coordinate-spaces
  figure session A asked for — seven spaces, seventeen edges, each a named
  conversion, drawn from the page's own table — and its surprises list
  dissolved into nine bold-led paragraphs; `threads.md` with the eight
  `ClientPacketListener` handlers that never hop as a table (session J's
  question, handed on twice), with `the-connection` and
  `what-the-client-is-told` now linking to it; `naming-drift` and
  `glossary` with their template headings gone. The glossary was swept by
  hand after the audit agent hit the spend limit: eleven entries added
  (*authority* — R6's page had none — *event loop*, *submit node*, and the
  eight sessions M and N named), one moved to alphabetical order, every
  owner link checked to exist, and the entries the splits touched read as
  sets (dialog, game test, function, macro; the worldgen nine; permission
  level) and found already correct.

  **Two tool fixes that outlast the session.** `verify_names.py` now checks
  every hand-kept page under `src/reference/` — it had skipped the whole
  directory except `threads.md` since pass 1, so the four catalogues the
  part sessions wrote this pass had never been verified; the dry run found
  sixteen failures, all qualification, all fixed (`Entity.hurtServer`, the
  six `DensityFunctions.Marker.Type` constants, ids to italics,
  `LivingEntity.getArmorValue` for the `Player` the page had named). And
  `map_source.py` hatches a skipped depth-3 package too small for a leaf,
  so *what this book skips*' "hatched boxes" is true of `gizmos`, `realms`
  and `references` now.

  **One factual correction in passing.** `the-connection` gave "the ping
  reply" as its example of a handler that runs on Netty; `handlePing` hops.
  The example is now the pong bookkeeping, which does not.

  Checks at commit: 18,520 names resolve (the reference tier included),
  186 diagrams pass, 537 lane participants with 0 disagreeing and 0
  colliding, `gen_reference.py all` re-run with no diff, class and lane
  indexes regenerated, `mdbook build` clean. Hand-offs in
  [pass4.md](pass4.md) (the handler count, the figure's shift counts, the
  glossary's eleven sentences, the README's parts column, and the
  hand-kept catalogues as a standing item), [pass5.md](pass5.md) (the
  reshaped page's inventories-in-prose, the voice of `naming-drift`) and
  [pass3.md](pass3.md) (the queue gains the three generation candidates;
  session P's four notes).

- **2026-09-03, session P — The lecture order and the close.** Pass 3 is
  closed. **Rulings first.** *The lecture order is the sidebar order with one
  departure* — the environment page before the level tick — and the
  dependency graph between parts is drawn once, in
  `src/figures/parts-dependency.md`, included by both the introduction and
  `lectures.md` (one source, so the two cannot drift; `TEMPLATE.md` records
  the device). Twenty-two solid arrows, each a landing page's *before you
  start* entry, two dashed ones for the places a part reaches forward (III →
  IV, cut by definition and by order; X → V, cut at Part V by the identical
  preambles), and Parts I and II left off because they would touch every
  node. *What this book skips* stays second, not last, and the notebook's
  twenty open questions are closed in §6 with one line each. *Nothing in
  Reference is watched* is now the first thing `lectures.md` says after its
  premise. **The sweep** found the corpus cleaner than expected: zero broken
  links or anchors over 145 pages, all twenty-four redirects resolving to
  built pages, every landing page's watch order identical to its
  `lectures.md` section, the reference README's parts column matching the
  landing pages, and the two label bugs session D flagged already fixed by
  sessions I and N. The lane gate is on: `deploy.sh` runs `check_lanes.py
  --strict` corpus-wide, and the introduction's *Verified means tested* now
  names three gates. **The shape audit** (two agents over ninety-eight
  pages, rubric from the menu): trace 31 · vocabulary 25 · pipeline 17 ·
  comparison 10 · policy 7 · pattern 6 · state machine 2 — the menu held,
  and the trace is a plurality at under a third. The uniformity that did
  not hold is the closer: 63 of 98 pages end on a *Questions players ask*
  section and four more carry one, with Parts IV, V, VIII and XII at every
  page; seven pairs of pages share a skeleton; twelve pages carry the
  literal heading *The trace: …*. All of it is in pass5.md with a rule of
  thumb (at most half the pages in a part). **Four coverage pages written**,
  each by an Opus agent against a shared brief and accepted after the
  session re-derived its sharpest claims from the decompile:
  `rendering/block-entity-rendering` (comparison, 332 lines — three roads
  into one collector, and the chest in your hand drawn at a different
  partial tick from the chest on the ground); `commands/entity-selectors`
  (pipeline, 313 — four of twenty-one options are the query plan, and *@p*
  crosses dimensions); `worldgen/blending` (pattern, 346 — one measurement,
  five consumers, and a seam where the terrain splines are switched off);
  `worldgen/creating-a-world` (pipeline with a comparison, 300 — the create
  screen is a finished data-pack load with widgets on it, and the Superflat
  editor's Cancel does not undo). Each corrected its own queue entry: the
  selector package is five classes and 1,717 lines, not six and 2,136;
  `ProtoChunk.setBlendingData` does not exist; `WorldGenSettings` is a
  `SavedData` in its own file, not part of *level.dat*; 25 of the 26
  block-entity render states are reachable. Eleven sibling pages gained a
  sentence or a link and lost a duplicate paragraph; fifteen glossary
  entries and eleven lane rows were added. The queue is down to five, each
  with a ruling: *writing a game test* is a how-to and not a lecture (pass
  6 decides); *commands that are algorithms* and the *predicate catalogue
  and boss bar* are carried as Reference candidates, the boss bar as a
  section pass 5 can add; the *predicate shape library* and the three
  `gen_reference.py` views are generation work. **The close.** Pass 3's
  charter, rulings, protocol, schedule and this log moved from `plan.md` to
  §9 and §10 here; `plan.md` is 280 lines and carries pass 4's charter,
  written by this session: pass 2's protocol with eight additions (the
  pass4.md checklist first; landing pages, the lecture map and the figure as
  claims about order; diagrams arrow by arrow; every count re-counted;
  populations named; libraries and data JSON; Reference row by row; the
  four never-checked pages), fifteen sessions A–O with a corpus-wide count
  sweep as session N, and the rule that pass 4 fixes facts in place and
  restructures nothing. `CLAUDE.md` and the memory say pass 4 is current.
  Checks at commit: 18,986 names resolve, 196 diagrams pass, 331 class
  lanes with 0 disagreements and 0 collisions, `mdbook build` clean, 102
  system pages in thirteen parts, 21 Reference pages. Two process notes
  for pass 4: a drafting agent's report is worth its claims list more than
  its page — all four reports listed sixty-plus claims with file and line,
  which is the pass4.md entry ready-made — and a bare `cd` in a shell call
  moves the session's working directory for every later call.
