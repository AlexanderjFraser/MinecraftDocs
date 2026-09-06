# Passes 5–8 — the queue (opened 2026-09-02 as the polish queue)

*Opened when polish was pass 5 and kept under that name. The ten-pass plan of
2026-09-05 ([plan.md](plan.md)) splits polish into four passes with one lens
each, and this file is the queue all four draw on. Nothing here moves; each
entry is taken by the pass its kind belongs to:*

- *a structural finding — a page carrying two subjects, material that belongs
  on another page, an explanation given twice, a missing cross-link, a
  landing page's shape, a coverage gap — is **pass 5's, the book**;*
- *a page-shape finding — a device become a slot, a shared skeleton, a section
  in the wrong order, a cut, a list that wants to be prose, a heading that
  names a slot — is **pass 6's, the lecture**;*
- *a figure finding — a diagram the wrong shape or too dense, a label that is
  a sentence, an orphan node, two figures for one mechanism, a lane — is
  **pass 7's, the figures**;*
- *wording debt — a hook rewritten around a fix, a tic, a hedge, a term, an
  ambiguous count, a data key's typesetting — is **pass 8's, the voice**.*

*A session strikes an entry (`~~…~~`) when it settles it, whichever pass it
is in; an entry a later pass finds already overtaken by an earlier pass's
rewrite is struck with a word saying so. Every claim a session introduces
while acting on an entry goes to [pass9.md](pass9.md). `tools/pass5_queue.py`
reads this file by kind and by page, guessing each entry's kind from the
section it sits under and its words and marking a guess with `?`; a tag
`[kind=book]`, `[kind=lecture]`, `[kind=figure]` or `[kind=voice]` anywhere
in an entry settles its kind, and a session tags the entries it finds
misrouted as it reads them. Below: the original preface, the standing items,
then the entries, newest first.*

---

*(The original preface, 2026-09-02.)* Pass 5 is the wording pass — voice, consistency, cuts. Its inputs: the
on-spec material and wording debt every pass-2 session logged in
[pass2.md](pass2.md)'s hand-off section (written when polish was still
numbered pass 4 — read "pass 4" there as pass 5), and what passes 3 and 4
append here: cuts pass 3 made and why, material it moved, wording it left
rough on purpose because the shape mattered more, and the tics it noticed.
Nothing here is acted on before pass 4 has checked the page.*

## Standing items

- The "not X but Y" construction — pass 2's most common register error,
  Part XIII its worst offender.
- The named-qualifier hedge ("with two exceptions", "five of the seven") —
  right precision, repetitive phrasing.
- One voice sweep against the best page, chosen in pass 5's first session.
- The glossary as the terminology checklist.

## Entries

## Session D — Part IV · The world (pass 5) *(2026-09-05)*

What this session's reading raised for the sessions and passes that come after
it. Everything it acted on itself is struck in place above, or logged in
[pass9.md](pass9.md).

**Routed to a later part's session.**

- ~~**Session E (V) — the ticker wrappers, now cited rather than told twice.**~~
  **Overtaken** — session D had already cut `chunk-anatomy` to the citation, and
  session E checked the anchor `#loaded-is-not-enough-to-tick` still names the
  section it points at. It does; nothing moved.
- ~~**Session E (V) — the repeater's booking is still told twice.**~~ **Done** —
  the cut fell on `scheduled-ticks`' three bold paragraphs, not on the diode
  page: rule 1 gives each of the three to `diodes-and-observers` (the priorities
  are the row its comparison table draws, the flag-2 exit is the payoff of *A
  diode never writes into its target*), so rule 4 never applied. What stayed on
  `scheduled-ticks` is the queue's own half — that a booking cannot be called
  off, the only removals being the bulk area operations — and the sequence
  diagram, untouched. The cut also turned up a **correction**: the deleted copy
  had `DiodeBlock.shouldPrioritize`'s condition inverted (logged in
  [pass9.md](pass9.md)).
- **Session F (VI) — local difficulty has no lecture.**
  `reference/level-data-and-rules`:283-289 is the book's **only** explanation of
  `DifficultyInstance` and `ServerLevel.getCurrentDifficultyAt`, built from
  `ChunkAccess.getInhabitedTime`, the overworld clock and the moon phase. That
  is a mechanism on the shelf, which A1's Reference rule forbids, and its
  consumers are Part VI's mobs. Part IV names `ChunkAccess.inhabitedTime` and
  cites the level tick for it; Part VI should take the explanation, or say why
  not.
- **Session I (IX) — the send table is now half a table.**
  `tickets-and-loading`'s *What the player is sent, and when* restated the batch
  pacing, the acknowledgement limit and four `PlayerChunkSender` constants that
  `what-the-client-is-told`:260-301 owns and explains better. Cut to the rows
  the ticket system actually decides — which chunks are in a player's set, and
  what makes one eligible — with the promotion row called out as the join
  between the two systems. Nothing was moved *to* Part IX, because Part IX
  already had all of it; session I should check that the three inbound
  citations (`server-tick`:225, `players-and-sessions`:266,
  `player-anatomy`:196) now point where the reader needs.
- **Session K (XI) — the flash layers are a citation now.**
  `lightmap-fog-and-sky`:60-65 explained the two `ClientLevel` lightning layers,
  which is `environment-attributes-and-timelines`' stack, and gave the lerp as
  "a fifth" where the owner says 22%. The decompile says `0.22F`
  (`ClientLevel.java:274`), so the rendering page's copy was both a duplicate
  and wrong; it is now one clause and a link. Session K should confirm the page
  still reads whole where it was cut.
- **Session N (Reference) — three things the shelf is carrying for a lecture.**
  The `SavedDataStorage` write path has moved to `chunk-storage` (the Reference
  page keeps the folder table and what a `SavedData` *is*). Still open:
  `MapItemSavedData`, `MapIndex`, `CustomBossEvents` and `WanderingTraderData`
  are named on `level-data-and-rules` and nowhere else in the corpus outside the
  class index; and the table has a *player data* row but none for the per-player
  *stats/* and *advancements/* files, which are the same kind of fact and have
  owner pages to cite.

**For pass 6, the lecture.**

- `chunk-generation-pipeline` tells the world's edge twice —
  `ChunkPyramid.SAFETY_MARGIN_CHUNKS`, `ChunkPos.isValid` and the
  three-and-a-half-million-block gap appear in the body and again as the fourth
  *Questions players ask*. One of the two is redundant with itself. [kind=lecture]
- `chunk-anatomy`'s *four shapes* section carries two subjects in one paragraph:
  `EmptyLevelChunk`, which the figure draws, and the client chunk cache, which
  no figure on the page draws. [kind=lecture]
- `chunk-storage`'s *Why the server thread never waits, and the three times it
  does* is two sections under one heading: the `IOWorker`'s priorities and
  write-behind map, and the three blocking joins. The heading promises one.
  [kind=lecture]
- `lighting`:145 — "`ThreadedLevelLightEngine.scheduled`, an `AtomicBoolean`,
  keeps exactly one batch in flight" is two sentences away from the
  `tryScheduleUpdate` it qualifies and reads as though it qualified the unload
  kick. A placement fix, not a fact. [kind=lecture]
- `points-of-interest`:233-270 mixes the ticket story with walk-target
  mechanics — the Manhattan rule, the 150-block threshold,
  `MemoryModuleType.LAST_SLEPT`, `WakeUp`'s priority. Every sentence that takes,
  releases or leaves a ticket alone is the page's; the rest is the brain's.
  [kind=lecture]
- `scheduled-ticks`:192's "forty lines below" points at the page's own layout,
  which reads at first as a pointer into the source. [kind=lecture]

**For pass 7, the figures.**

- Part IV's landing figure had `GP -- "a chunk that still needs its light
  finished" --> LI`, which draws lighting as happening *after* the pipeline when
  both light steps are steps nine and ten of the twelve. Session D relabelled it
  *steps nine and ten, on the other executor*; pass 7 should judge whether the
  edge belongs at all, since the conveyor's other edges are hand-offs and this
  one is an inclusion. [kind=figure]
- `chunk-anatomy`'s section figure draws the two containers and the four
  counters but not the light, and the glossary's *Section* entry has to say
  "its light lives in the light engine's own storage, not on the section"
  because no figure does. [kind=figure]

**For pass 8, the voice.**

- `scheduled-ticks`:368 asks the reader to call `TickAccess.hasScheduledTick`
  and :370 says `LevelTicks.hasScheduledTick` "can no longer see" — the same
  method under two names in one paragraph. [kind=voice]
- `scheduled-ticks`:377 — "**Does `/tick freeze` stop scheduled ticks?** Yes,
  and among the tick commands it is the only one that does" is a claim about a
  command set no page enumerates. Re-derived and found *sound* this session
  against `TickRateManager.runsNormally`, but the population is unnamed, which
  is the shape pass 8 is hunting. [kind=voice]
- `tickets-and-loading` names *thirteen* from three different anchors — the
  header line, the walk, and the level-31 ticket. Already logged above as pass-8
  wording debt; still true after this session's edits. [kind=voice]
- `points-of-interest`:192, 228 and 333 spell entity events as bare numbers
  ("entity event 14") where `synched-entity-data`:313 says `EntityEvent`
  declares all 62. The one place the book prefers a magic number to a name.
  [kind=voice]

**A coverage question this session could not close.**

- `world/level/entity`'s six unnamed classes (98 lines) and `server/level`'s
  `ServerEntityGetter` are declared in Part IV's *where the part stops* as Part
  VI's, but Part VI names only four of the seven. Session F decides whether the
  section index wants a passage on `entity-lifecycle` or a declined sentence.

## Session C — Part III · The server (pass 5) *(2026-09-05)*

*What six page reads and one end-to-end reading of Part III turned up and
session C did not act on, routed by kind. The claims it introduced and the
six corrections it made are in [pass9.md](pass9.md).*

### For other part sessions (pass 5)

- **Session I (IX) — the handover between `players-and-sessions` and
  `protocol-phases` is declared twice and in two places.** `players-and-sessions`:30-34
  says "This page starts where that one hands over: with `PlayerList` deciding
  whether the login is allowed at all"; `protocol-phases`:313-315 says it
  hands over at `PlayerList.placeNewPlayer`. The span between the two seams is
  exactly the material both pages explain — the two-run admission gate
  (`players-and-sessions`:59-70 against `protocol-phases`:204-211 and
  308-311), the strictly serial configuration queue
  (`players-and-sessions`:97-104 against `protocol-phases`:248-259, both with
  a figure of the same six steps), and `PrepareSpawnTask`'s two states
  (`players-and-sessions`:106-111 against `protocol-phases`:299-306). Session
  C's recommendation, not applied because the pair is the later part's under
  A4: the gate is `players-and-sessions`' by the scenario rule (*who is
  admitted* is its first section, and it alone has the asymmetry — the
  newcomer wins at login and loses at the second check); the queue and the two
  states are `protocol-phases`' by the same rule, since its hook *is* the
  player being constructed after configuration ends. Two sentences on
  `players-and-sessions` are moves rather than cuts if that split is taken:
  that the client sits in configuration with no idea a world is being
  assembled for it, and that without `PrepareSpawnTask.keepAlive` a slow
  client would arrive to find its spawn chunks expired. Whatever is decided,
  the two handover sentences and `server/README`:91-92 must name one line.
- **Session I (IX) — keep-alive.** `players-and-sessions`:426-433 and
  `the-connection`:370-380 both explain it; the connection owns it (it runs in
  configuration too). Two moves come with the cut: the wrong-id disconnect is
  "immediate rather than ignored" only here, and the latency smoothing —
  three parts old to one part new, so a tab list lags a real change by several
  pings — is on no other page in the book. What `players-and-sessions` keeps
  is the asymmetry its section is actually about: keep-alive is the only one
  of the three kicks that exempts the singleplayer host.
- **Session H (VIII) — the flying kick.** `players-and-sessions`:421-426
  against `input-to-movement`:375-383, which has the gravity scaling, the
  vehicle copy and six suppressions this page lacks; the movement page owns
  it and this one keeps a clause. Note that the idle timeout beside it
  (`MinecraftServer.playerIdleTimeout` and its end-credits exemption) has no
  other home in the book and must stay wherever that section ends up.
- **Session I (IX) — the chunk-batch pacing on a join.**
  `players-and-sessions`:239-245 against
  `what-the-client-is-told`:266-285, which owns both halves of the loop; the
  join page keeps "a joining client is trusted with one batch".
- ~~**Session F (VI) — an inbound link that lands on the wrong page.**
  `damage-and-death`:322 says "[player anatomy] owns the object that comes
  back". It does not: `player-anatomy`:213-216 itself says
  `players-and-sessions` owns it, and the object is
  `players-and-sessions#the-object-and-the-reference-that-outlives-it`.~~
  **Done, session F (pass 5)**: repointed, with the anchor.
- **Session D (IV) — `reference/level-data-and-rules` is now the declared
  owner of the `level.dat` write path** (session C's ruling: three tellings
  cut to one, and both Part III pages now cite
  `#what-is-left-in-leveldat`). Nothing to do unless D disagrees; if it does,
  the two Part III citations move with it. Beside it: `starting-a-server`
  keeps `DirectoryLock` whole, so the Reference row for
  `LevelResource.LOCK_FILE` should cite
  `starting-a-server#taking-the-lock-and-fixing-leveldat-twice` rather than
  explain the lock, and `PlayerDataStorage`'s rescue is now explained on
  `players-and-sessions` rather than wanting a Reference entry (pass5.md:1553's
  third homeless item, discharged). ~~Open.~~ **Agreed, session D (pass 5)** —
  D does not disagree, so the two Part III citations stand as C left them.
- **Session D (IV) — three Part III classes that are Part IV's.**
  `ChunkResult` (110 lines, the success/fail wrapper chunk futures carry) and
  `PlayerMap` (`ChunkMap`'s player index, which
  `players-and-sessions`:233-237 makes a "two player lists" point without
  naming a third) are named nowhere in the book and are Part IV's scope, not
  Part III's; `server/README` now says so under *where the part stops*.
  ~~Open.~~ **Done, session D (pass 5)**: both landed on `tickets-and-loading`
  — `ChunkResult` where the three futures are armed (its failure case *is*
  `ChunkHolder.UNLOADED_LEVEL_CHUNK`), `PlayerMap` in the spectator answer,
  where the point is that the skip is remembered at join rather than re-asked.
- ~~**Session E (V) — the hopper's transfer cooldown.**~~ **Done** — written into
  `block-entities`' *Loaded is not enough to tick* as the one ticker cadence
  worth knowing, with the fact `HopperBlockEntity.MOVE_ITEM_SPEED` is declared
  and read nowhere (both call sites write the literal 8).
  *(original entry)* 
  `HopperBlockEntity.MOVE_ITEM_SPEED` is 8, and the only place the book said
  so was Part III's landing page, which is a summariser. Cut from there;
  `block-entities` is where a ticker's cadence belongs if session E wants it.
- **Session F (VI) — `ServerEntityGetter`** (132 lines, `server/level`), the
  server-side entity-query interface `ServerLevel` implements, is named
  nowhere in the book and is Part VI's vocabulary.
- **Session H (VIII) — `DemoMode`** (102 lines) extends
  `ServerPlayerGameMode` and is named nowhere; `player-anatomy`'s game-mode
  comparison is where it would go, or a declared decline.
- **Session M (XIII) — `ServerBossEvent`** (166 lines, `server/level`) is
  still Part XIII's, as the schedule says; `players-and-sessions`:180 sends
  "boss events" in the join burst without naming a class.
- **Session M (XIII) — a live disagreement.**
  `scoreboard-and-data`:277-278 says "a score set and a crash a tick later is
  a score lost"; `how-a-server-dies` says a tick-loop crash reaches the same
  *finally* and writes what `/stop` writes, and `scoreboard-and-data`:145-146
  puts `ServerScoreboard.storeToSaveDataIfDirty` inside
  `MinecraftServer.saveAllChunks`, which the crash path calls. Either the
  sentence means a watchdog kill or a *kill -9*, or one of the two pages is
  wrong. Also in [pass9.md](pass9.md).
- **Session N (Reference) — `reference/threads` wants three things Part III
  has and it lacks**: a *daemon* column; that `RconThread` and
  `QueryThreadGs4` are `GenericThread`s polling on a half-second timeout so
  they notice `GenericThread.running`; and that `RconThread.create` returns
  nothing when *rcon.password* is empty **or** *rcon.port* is out of range,
  where its row states only the password half. Session C left all three on
  `starting-a-server` rather than move them into a Reference page mid-pass.
- **Session N (Reference) — `reference/README`'s parts column.** Session C
  added III to *Level data and rules*' row, because Part III's landing page
  now points there. The column is still hand-kept and is the one A6 left to
  session N.
- **Session L (XII) — the initial spawn search is split and neither half
  links the other.** `starting-a-server`:269-277 owns *when* it runs (the
  `ServerLevelData.isInitialized` gate, the bonus chest, the flag that stops
  it repeating); `biomes`:194-204 owns the search itself, with
  `Climate.findSpawnPosition` and the 2,048-block cap. One clause each.

### For pass 6 — the lecture

- `server-level-tick` — the falling-sand exception (pass 4's finding at
  pass5.md:1081, still live and re-checked): :304-307 delivers the section's
  punchline and :309-316 immediately qualifies it. Lead with the exception
  and land on the rule. [kind=lecture]
- `players-and-sessions` has no *Questions players ask* closer and is one of
  the pages that most obviously wants one: three of the four `###` sub-heads
  under *Four ways the session changes* are already player questions in
  disguise (why the ender chest survives death, why the Nether keeps effects,
  where the llama goes). [kind=lecture]
- `players-and-sessions`:280-286 — the heading *Four ways the session
  changes* sits above a paragraph naming a fifth (the end credits). Session C
  ruled the heading stays: it names the comparison's four columns and the
  concession is what makes the paragraph honest. Recorded as pass 6's to
  re-judge with the section in hand, not as an open defect. [kind=lecture]
- `how-a-server-dies`:336-369 — *Ctrl-C, the window, and a singleplayer
  world* carries three subjects and the heading promises all three; the
  client's own window-close road is the client loop's. Session C left the
  paragraph because the cut would take the "after an ordinary exit it finds
  `Minecraft.singleplayerServer` already null" fact with it, which the client
  loop lacks. [kind=lecture]
- `starting-a-server`:5-18 — the opening paragraph (pass 4's finding at
  pass5.md:1070) is still the page's densest and now carries one more clause.
  Its "everything else was over before the first one printed" is true of the
  things it enumerates and reads as a claim about the whole boot, which the
  *Done* section then contradicts for query, RCON, the watchdog and JMX.
  Worth two sentences. [kind=lecture]
- `server-tick` — the *Questions players ask* section is where the autosave
  arithmetic now lives, which makes it load-bearing rather than a closer.
  [kind=lecture]

### For pass 7 — the figures

- `server-tick`'s event-loop flowchart (pass5.md:1092's list, re-checked and
  still live): fourteen edges, and its `C` node label is a sentence.
  [kind=figure]
- `starting-a-server`'s sequence figure: 27 items, the largest single diagram
  in the part. [kind=figure]
- `server/README`'s part figure runs Start → Tick → Level → Players → Death,
  which is the runtime order and not the watch order (Tick, Level, Players,
  Start, Death), and the shape sentence above it offers a third ordering. The
  exemplar (`commands/README`) numbers its nodes to the watch order. Session
  C left the figure alone because it is drawing the *runtime* relationship,
  which is the part's shape; pass 7 should decide whether numbering or a
  caption settles it. [kind=figure]
- `server-level-tick` now names the tick's profiler zones in prose. If pass 7
  wants them in the flowchart's node labels instead, the prose sentence is
  the copy to cut. [kind=figure]

### For pass 8 — the voice

- Part III's five pages all end their opening paragraph on a bolded or dashed
  sentence — the tic pass 4's session C logged and this session left.
  [kind=voice]
- `players-and-sessions` calls the packet drain "the scheduled packet
  processing" twice (:170, :192-193), which is the profiler zone's name; the
  book's term is *the drain* (`server-tick`:94-110). One voice, one name.
  [kind=voice]
- `how-a-server-dies` uses *the number* device twice (**Ten seconds** and
  **One millisecond**) where once is the convention; pass5.md:1553's version
  of this entry named the comparison table's "differ in one cell" as the
  second instance and is **overtaken** — that cell now reads "three of the
  eight rows". [kind=voice]
- `server-tick`'s `tickChildren` table has one cell reading "its own counter
  has not passed 600 — so every 601st call, not every 600th tick", the
  longest *skipped when* value in the table. [kind=voice]
- The repeated hedges pass 4's session C logged ("almost nothing", "all but
  the first", "two of the three endings") are unchanged and now joined by
  "over half of those lines" on the landing page. [kind=voice]

## Session B — Parts I and II (pass 5) *(2026-09-05)*

*What eleven page reads and one end-to-end reading of both parts turned up
and session B did not act on, routed by kind. The claims it introduced and
the corrections it made are in [pass9.md](pass9.md).*

### For other part sessions (pass 5)

- **`client/the-client-loop` still does not link `anatomy`** (the session-A
  entry, re-derived): its hook contrasts the two loops and links neither
  `anatomy` nor `server-tick`. The anchor is
  `anatomy.md#two-loops-and-a-wire-between-them`. **Session J.**
- **`world/chunk-generation-pipeline` repeats anatomy's worker-pool sizing**
  (`Util.maxAllowedExecutorThreads`, the *max.bg.threads* property) and links
  no anatomy page. It should keep only "there is no generation thread
  setting", which anatomy does not say, and cite
  `anatomy.md#four-threads-worth-memorising`. Same page's
  `ConsecutiveExecutor` paragraph: anatomy owns *what it is*, the pipeline
  keeps `AbstractConsecutiveExecutor.run`'s re-registration. **Session D.**
  ~~Open.~~ **Done, session D (pass 5)**: the sizing and *what a
  `ConsecutiveExecutor` is* both cut to a citation of
  `anatomy#four-threads-worth-memorising`; the page keeps "there is no
  generation thread setting" and the consequence that the only knob is the
  shared pool's.
- ~~**`data-components` ↔ `items-and-stacks` is the same lecture twice**~~, and
  worse than the 17.00 score suggests: the same hook and nine duplicated
  mechanisms (the prototype built at reload, the sanitising patch,
  copy-on-write, equality, the ten common components, the two validators, the
  wire form), against `items/README`:47's promise that Part VII "never
  re-teaches the component system". One clause is a move to
  `containers-and-menus`: `handleContainerButtonClick` calling
  `broadcastChanges` directly, out of the ordinary tick. **Session G**, which
  the routing rule gives the pair. ~~Open.~~ **Done, session G (pass 5)**: the
  line is Part II owns the component system's own machinery — the type, the
  maps, the patch's sanitising and copy-on-write, the prototype's two-phase
  build — and Part VII owns the stack as an object: its fields, the five
  identity methods, the two validators, `ItemStackTemplate`, durability, the
  tick. Six mechanisms cut to a citation on `items-and-stacks` (including its
  own hook, which was Part II's twice over) and three moved the other way; the
  validators, `ItemStackTemplate` and `ignoreSwapAnimation` moved *to* Part VII
  and `data-components` cut to a clause each. The button-click broadcast moved
  to `containers-and-menus` as recorded.
- ~~**`data-driven-types`' trace runs a page too far.**~~ L278–294 — the roll, the
  scatter, and the three-level function composition — is `items/loot-tables`'
  explanation retold. The pattern page should stop at the object existing.
  **Session G**, with the pair above. **Done, session G (pass 5)**: *The run
  half* now stops at the object existing and cites `loot-tables#one-roll-drawn`.
- **Eleven of the fifty-six rows send the reader to a page that never names
  the element** — **Part VII's three struck, session G (pass 5)**:
  `SlotSource` now points at `contexts-and-predicates` (which names it) rather
  than `loot-tables` (which never did), `EnchantmentProvider` at `enchanting`,
  and `ConsumeEffect` at `using-an-item`; `NbtProvider` and
  `ScoreboardNameProvider` were pointing at `loot-tables` for elements *no*
  page named, and are now both pointed at `contexts-and-predicates`, which
  names them. Sessions E and M keep the rest. Original entry: `Permission` and `PermissionCheck` → Brigadier when
  `commands/permissions` owns them; `EnchantmentProvider` → enchantments when
  `items/enchanting` owns it; `SlotSource`, `ConsumeEffect`, `SpawnCondition`
  and `BLOCK_TYPE` land on pages silent on them. Each *taught in* cell is a
  claim about another part's page, so each part session should check its own
  rows. **Sessions E, G, M** between them.
- **`Gizmos` is explained only on `what-this-book-skips`** and linked from
  none of the pages whose traces end in a debug renderer. The skips page is
  the owner by default and should not be; either a later part takes it or the
  pages that use it cite the skips page. **Sessions J and K.**
- **`text-components`' selector expansion is told three times** — here,
  `networking/chat-and-signing` and `commands/entity-selectors`. **Session I.**
  ~~And the death-message game rule twice, on two pages that never link each
  other (`entities/damage-and-death`).~~ **The death-message half is done,
  session F (pass 5)**: not a duplicate after all — `text-components` owns the
  assembling and `damage-and-death` the consequence of the rule being off (an
  empty component in a packet that still goes) — but the two now link each
  other, and `damage-and-death` gained the fall-attribution rule
  `text-components` was citing without an owner.
- **`codecs-nbt-json` explains five mechanisms other parts own**: the wire
  buffer, region compression, the `BlockEntity` save shells, the serverbound
  fence and the trusted-tag constants. Session B left them: each is one
  column of the page's own four-path table, and cutting them needs the
  owning part's session in the room. **Sessions D, G and I** to judge from
  their side, then the citation form here.
- **`reference/registries` says 153 registry keys and
  `identifiers-and-registries` says 148.** Two populations or one wrong
  number; session B did not re-derive it because the Reference page is
  session N's. **Session N**, and pass 9 if it survives.

### For pass 6 (the lecture)

- `tags`' pay-off, *Prepared, then applied*, is a bold lead-in with no
  heading, so a citation aimed at it lands on a hundred-line section instead.
  Three pages now cite that section. [kind=lecture]
- `tags`' opening paragraph states the three-step apply and the "one thread,
  start to finish" sentence, and L192 states both again nearly verbatim. The
  hook should keep the promise and the section the mechanism. [kind=lecture]
- The *A player recognises this part by its symptom* device opens eight of
  the thirteen landing pages. Session B varied Part I's away from it and left
  Part II's. [kind=lecture]
- `what-this-book-skips` is 476 lines of fifteen tours plus a fifteen-row
  ruling table, and it is the second lecture a reader meets. Its length is a
  cut worth judging as a whole. [kind=lecture]
- `anatomy`'s *Where to look* is twenty names for a page whose cast is eight.
  [kind=lecture]

### For pass 8 (the voice)

- `identifiers-and-registries`' hook says the wire id "is a line number",
  which is a metaphor for the ordinal of the registration statement and false
  read literally. The lecture unpacks it in the next two sentences; the
  landing-page teaser and the verified line do not, and session B left all
  three alone because the metaphor is the page's best sentence. [kind=voice]
  (This restates an open session-A entry; both should be settled together.)
- *the two tag tables* survives as a cast-row phrase on
  `identifiers-and-registries` after the explanation moved to `tags`. Check
  the phrase still earns its place. [kind=voice]

### Coverage routed, not acted on

- `core/dispenser` (13 classes, 1,090 lines) is in Part II's packages by the
  atlas's `PARTS` mapping and is Part V's subject. Either the mapping moves it
  or `blocks/` names the family. **Session E**, with the mapping change if it
  wants one.
- `util/worldupdate` (5 classes, 736 lines — `RegionStorageUpgrader`,
  `UpgradeProgress`) is named nowhere in the book. It is the *Optimize World*
  button, and it is the last sizeable unowned mechanism in Part II's packages.
  Session B's judgement: it belongs beside `world/chunk-storage`, not in
  Foundations. **Session D** to take or decline. ~~Open.~~ **Taken, session D
  (pass 5)**: a section on `chunk-storage`, *Doing all of it at once, with no
  server running* — `WorldUpgrader`'s daemon thread, `RegionStorageUpgrader`'s
  walk of every region file, the optional recreate that compacts a save, and
  `UpgradeProgress` as the bar's counter.
- `util/eventlog` and `util/monitoring/jmx` (571 lines) belong to the skips
  page's boundary, not to a lecture. Session B named `JsonEventLog` in
  passing on `resource-system` and left the rest.
- `GsonHelper` (608 lines, the largest unnamed class in Part II) is the JSON
  reading toolbox; `codecs-nbt-json` names `StrictJsonParser` and
  `LenientJsonParser` and not it. One clause on that page would close it.
  [kind=book]


## Session A — the standard (pass 5) *(2026-09-05)*

*What the standard turned up on its way through the frame. The rulings are in
[pass5-brief.md](pass5-brief.md) Part 3; these are the pieces of work they
create, routed by kind.*

### For the part sessions (pass 5)

- **The ordering paragraph is on two pages, and the two have drifted.** Every
  part states its internal order twice — in its landing page's closing
  ordering paragraph and in its section of `lectures.md` — and neither is a
  copy of the other. The landing page has pairs the map lacks (Part X's ten
  and eleven, *the two halves of sound*; Part VII's seven and eight; Part
  VIII's six and seven) and the map has pairs the landing page lacks (Part
  III's *never apart from it*; Part VI's *attributes* against *synched entity
  data*). Under the ownership rule the landing page owns the ordering claim,
  so a claim the map has and the page lacks **moves to the page**, and the map
  keeps the shorter copy. Each part session re-syncs its own; session O checks
  the thirteen. [kind=book]
- **The citation form is a link's worth of work per page.** The eight
  through-line owner pages take **169 inbound links, and three carried an
  anchor** before session A (`check_links.py --inbound` prints them; the
  exemplar added three more). A part session's cheapest structural win is to
  put the owner's anchor on the through-line links out of its own pages —
  `server-tick#what-minecraftservertickchildren-runs-and-in-what-order` and
  the rest are tabulated in the brief's A3. [kind=book]
- **Two landing pages hand-count a size the atlas now generates**, and one of
  them counts a different population: `worldgen/README`:27 says *451 classes
  and 45,700 lines* against the generated 451 / 45,749 (the same packages,
  rounded — a straight switch to `{{#include}}`), and `rendering/README`:20
  says *1,179 classes and 87,000 lines* for three packages against the
  mapping's 1,254 / 93,012 for four, because `map_source.PARTS` gives Part XI
  `client/particle` as well. Session K decides which population Part XI's
  argument is about and then uses the include. The other ten landing pages
  carry no size sentence, which A2 allows. [kind=book]
- **Two landing pages are over the measured budget** — everything but the
  watch order: `rendering/README` 124 lines and `worldgen/README` 144,
  against a corpus median of 90. Sessions K and L judge; the fix is the
  argument, not the trim. [kind=book]
- **`lectures.md`:296 and `rendering/README`:140 were near-verbatim**, and
  session A shortened the first under the summariser rule. Session K reads
  the pair once to check nothing was lost. [kind=book]

### For pass 8, the voice

- ***Ledger* names three unrelated things.** The prediction ledger
  (`client/prediction-and-acks`, 18 uses), `server-tick`'s *three ledgers* at
  the bottom of a tick, and a loose metaphor on `items/loot-tables` and
  `items/contexts-and-predicates`. The through-line owns the first; the other
  two want a different word or an explicit one. [kind=voice]
- **`rendering/README`:140 says "they were one page until pass 3".** A
  published page naming a pass number a reader cannot resolve; the same
  sentence in `lectures.md` was fixed this session ("two pages that were
  one"). [kind=voice]
- **The data-driven type pattern's terms are ordinary words**, so
  `pass5_dups.py --terms` gives it 11 pages where the other six through-lines
  get 18 to 72. Eleven is a floor, not a count, and no session should quote it
  as one. [kind=voice]

## Session O — the close (pass 4) *(2026-09-05)*

The glossary sweep, the four unactioned Reference catalogues and the tool
re-read each produced material the close verified and deliberately did not act
on. Nothing here is a wrong fact; everything here is a page that is thinner,
looser or more repetitive than it should be.

### The generators' blind spots, now measured

- **`verify_names.py` cannot see inside a mermaid block, and that is the
  corpus's largest unchecked surface.** 453 distinct class-shaped tokens appear
  only in a diagram and in no backtick on their page. Session O found one real
  error in them by hand (`BakedGlyph.renderChar`, which is
  `BakedSheetGlyph`'s) and fixed it; the other 452 are unchecked. Session A
  logged the *index* half of this — 135 class/page pairs and 112 distinct
  classes the class index cannot see, 26 with no row at all. **One parser
  serves both**, and the work is: tokenize dotted `Class.member` forms inside
  ```` ```mermaid ```` fences, feed them to the same resolver, and let the index
  read them too. It will fail on lane ids and nested simple names, so it wants a
  pass over the first run's output, which is why it is pass-5 work and not a
  gate change.
- **23 simple names are shared by two files**, so a `Class.member` backtick
  resolves against the union of both — `Connection` (99 corpus backticks,
  `network/` against `server/jsonrpc/`), `AttributeModifier` (13, and the two
  classes have genuinely different member sets), `EntitySelector`,
  `StructureCheck`, `Input`. The verifier now prints the list on every run. Pass
  5 should either disambiguate the pages or teach the resolver which file a page
  means.
- **`map_source.py`'s line counts are 18.4% blank lines** — 132,608 of 719,302
  — and neither the tool's docstring nor `src/maps/README.md` says so. "719k
  lines" is 587k non-blank. One clause on the atlas's counting rule fixes it.
- **`TEMPLATE.md:112` is stricter than mermaid.** A `;` and a `#` in a
  *flowchart* label both parse and render correctly under 11.6.0; the rule that
  forbids them everywhere is true only of sequence diagrams (`#`) and state
  diagrams (`;`, which silently splits a label into extra states). Relax the
  rule to name the two places it is real — and note that the state-diagram case
  is now a gate, so the rule has teeth where it needs them.

### Completeness, verified and not acted on

Pass 4 does not add material, so these are the classes and mechanisms an
agent's completeness sweep found in a page's scope that the page never
mentions.

- ~~**`reference/non-living-damage.md` wants a `hurtClient` column.** Seven of
  the twenty-one declare one, two return an unconditional `true`, and
  `MinecartTNT` inherits a third; twelve inherit `Entity`'s false.~~ **Done,
  session F (pass 5)** [kind=book], with the count corrected: **thirteen**
  inherit the default, not twelve (7 + 1 + 13 = 21, and the twelve left one row
  unaccounted for). The other two asks were **declined**: the
  `ServerGamePacketListenerImpl.handleAttack` disconnect is already owned and
  better told at `the-sword-swing`:86-88, and writing it here would create the
  duplicate this session was removing; `Entity.isPickable` is named in the
  `AbstractHurtingProjectile` row, and the general *defaults to false* fact is
  the swing's, not the catalogue's. **Session H** should take both.
- **`reference/submit-phases.md`** is missing three things its own sentences
  depend on: `SubmitNodeStorage` (the *order bucket* the page names with no
  antecedent — it is the outer loop of every sweep), `TranslucentSubmit` (the
  marker five of the thirteen records implement, which is why the phase can sort
  by distance at all) and `RenderType.canConsolidateConsecutiveGeometry` (which
  gates **both** merges, independently of `strictlyOrdered`, and is now the
  thing the corrected merging paragraph turns on). `PhaseSubmitGrouper` is
  machinery this page can leave out.
- **`reference/hud-elements.md`** has no row for `SpectatorGui.extractAction`
  (the *else* branch of row 17), and never names `Gui.overlay`/`Gui.screen`, the
  two things recorded between the HUD and rows 28–31, nor the three or four
  strata a screen contributes there.
- **`reference/level-data-and-rules.md`** never names `DirectoryLock` (what
  `session.lock` is for), `LevelVersion` (the *Version* compound and
  *DataVersion* the world-select row reads), `LevelSummary`'s corrupted and
  symlink states, four more `LevelResource` paths (*generated/*, *datapacks/*,
  the world resource pack, the icon), the per-player *advancements/* and
  *stats/* files, or `MinecraftServer.saveAllChunks` — the method that drives
  all three save paths the page describes.
- Seven of that page's eighteen table rows get no prose at all — the
  scoreboard, maps, raids, chunk tickets, the dragon fight, five of the
  boss-bar row's six owners, and player data.

### The glossary's headwords

Five entries are titled with a phrase the corpus does not use, against the
page's own rule that "where a term is a class name, the class name is the
entry":

- **Blend alpha** — the corpus writes plain "alpha" or the JSON name
  *blend_alpha*.
- **Staging buffer** — used once outside the glossary, on its owner page, and
  once elsewhere for an unrelated thing (`section-meshing`'s worker buffer).
  The class-shaped headword is `ExecutionContext.newTopCommands`.
- **Flat level generator preset** — the lowercase phrase appears nowhere; the
  corpus names only the plural bootstrap class, twice, on one page.
- **Batch** — claimed for the game-test meaning, while a reader is likelier to
  have met *chunk batching* in Part IX. Retitle, or add the chunk one beside it.
- **Permission atom** — the two-word phrase appears nowhere; the corpus writes
  "an atom", "the chat atoms", "the entity-selector atom".

Beside them: **Blending data** should be `BlendingData` by the same rule, and
*Occlusion* is a word the corpus uses for four unrelated things across nine
pages with no page owning it — the session left it out rather than write a
five-way pointer, and pass 5 should decide whether the glossary does
disambiguation at all.

### Two counts in this file that were wrong

Session P's own pass-5 notes carry two numbers the close re-derived:

- **The literal `## The trace: …` heading is on twenty pages in eight parts**,
  not "twelve pages in four parts" — and session P's own list named three
  parts while saying four. Both numbers were already true at pass 3's close
  (`git grep -c` at `0255661` gives 20), so pass 4 changed nothing here; the
  note was simply wrong. Parts II, IV, VI, VII, VIII, XI, XII and XIII.
- **The closer device is on 69 of the 102 system pages**, 65 of them as the
  last content section. By part: I 1/2 · II 6/7 · III 2/5 · IV 10/10 · V 7/7 ·
  VI 3/9 · VII 2/8 · VIII 7/7 · IX 3/5 · X 7/12 · XI 6/11 · XII 9/10 ·
  XIII 2/9. Four parts still use it on every page.

### Wording the close rewrote and pass 5 should re-read

Every entry the glossary sweep corrected is a sentence written to be true
rather than to read well, and the five long ones are worth a second pass:
*Packet*, *Permission set*, *Prediction ledger*, *Unattended command* and
*World clock*. The same is true of `math-and-primitives`' coordinate-spaces
paragraph, which lost its thesis and has not yet gained a replacement idea, and
of `submit-phases`' merging paragraph, which is now correct and three sentences
long where it was two.

## Session N — the corpus-wide count sweep (pass 4) *(2026-09-05)*

The sweep's job was numbers, and what it turned up beside them is one tic with
many faces: **a count that is right under one reading of its population and
wrong under another, with the page never saying which**. None of these is a
wrong number, so none was fixed. Pass 5 should pick the reading, say it, or
drop the number.

**A count of one thing described as a count of another.**

- `blocks/blocks-and-states.md:25` — "through **fifty-eight** statics — the
  drops, the particles and the shape-update helpers". 58 is every `static`
  declaration in `Block.java` (23 fields, 34 methods, one nested record); the
  things listed are static *methods*, of which there are 34. And "the
  particles" is `Block.spawnDestroyParticles`, a `protected` **instance**
  method.
- `client/hud.md` — the heading is now *Four states*, and three of the four
  draw. If pass 5 wants "bars" back, the number is three.
- ~~`world/scheduled-ticks.md:81` — "**Two** type parameters" is right for the
  two type *arguments* in play (`Block`, `Fluid`); every class involved
  declares exactly one.~~ **Done, session D (pass 5)**, as a correction.
- ~~`world/chunk-storage.md:281` — "it changes hands **four** times" names four
  stages but only three thread changes.~~ **Done, session D (pass 5)**: "four
  stages across three lanes", with the shared lane said out loud.
- `player/README.md:32,63` — "**eight** classes" is the cast table's eight
  *rows*, which name nine classes (one row holds `ServerPlayerGameMode` /
  `MultiPlayerGameMode`).
- `networking/README.md:35` — "the two the part spends longest on" names
  *what the client is told* and *chat and signing*; by line count the two
  longest are `what-the-client-is-told` (474) and `packets-and-stream-codecs`
  (465), and `chat-and-signing` (326) is the shortest page in the part.

**A superlative that is true only of the sub-population the page stands in.**

- ~~`world/chunk-storage.md:323` — "which **only** `ImposterProtoChunk.markUnsaved`
  does" is true among the saving flags; `ImposterProtoChunk.setLightCorrect`
  delegates unconditionally too, which `chunk-anatomy:102` says itself.~~
  **Done, session D (pass 5)** — a correction, and the two pages had also given
  incompatible *reasons* for the same false. Both now say the same thing.
- `client/text-and-fonts.md:184` — "the one place in the pipeline where a
  character is invented" is true of the wrap path;
  `ComponentRenderUtils.clipText` in the same class appends
  `CommonComponents.ELLIPSIS`.
- `world/points-of-interest.md:124` — "**a dozen** shapes" of read-only query
  is 13 method names / 14 methods. The hedge covers it; *thirteen* reads better.
- ~~`entities/ai-goals-and-brains.md:381,390` — "everything it will ever do" /
  "the twelve": a door-breaking `Zombie` gains a thirteenth goal at
  `Zombie.java:158`, outside `Mob.registerGoals`.~~ **Done, session F (pass
  5)**: re-derived and corrected; the zombie is now the page's own example of
  the exception its general section already allowed for.
- ~~`entities/authority.md:181` — "three of those eight read the same member"
  holds for `Entity.canSimulateMovement` (3);
  `Entity.isLocalInstanceAuthoritative` is read at four of the eight.~~
  **Done, session F (pass 5)**: re-counted in the source and all three members
  given their number, because the sentence read as a maximum its own list
  denied.
- ~~`world/README.md:79` — "the one page here that depends on nothing else in
  the part" is one under *off the conveyor chain*; the part's own figure gives
  two pages no inbound edge.~~ **Done, session D (pass 5)**: the superlative is
  gone, replaced by *off the conveyor, ahead of it*, which is what the figure
  draws.
- `world/chunk-storage.md:203` — "**Three** places do make the server thread
  wait on a disk": a fourth blocking join at `ServerChunkCache.java:126`/`149`
  can end at the disk, though it drives the main-thread queue rather than
  raw-joining the IO lane.
- `client/the-client-level.md:129` — "the chunk cache and **one** packet
  handler call `LevelExtractor` directly" is right for the dirty-marking path;
  three `ClientPacketListener` sites touch `levelExtractor` in all.
- ~~`foundations/identifiers-and-registries.md:75` — "keyed **three** ways"
  names three maps; `MappedRegistry.byValue` is a fourth index.~~ **Done,
  session B** [kind=book] — not an ambiguous count but a wrong one, so it was
  fixed with the decompile open and logged in pass9.md. `byValue` is an
  identity map and is what `Registry.getKey` reads.
- ~~`foundations/codecs-nbt-json.md:259` — "**two** fields" is true of the
  `IOWorker` case cited; `StructureCheck`, in the same sentence, uses three.~~
  **Done, session B** — re-derived (`IOWorker.java:105` two `FieldSelector`s,
  `StructureCheck.java:113` three) and rewritten to name the mechanism
  (`CollectFields` over the selectors the caller wants) rather than a number.
- `blocks/signal-and-dust.md:27,126` — "the three answers a state gives" is
  three of six signal delegators on `BlockBehaviour.BlockStateBase`; "All three
  stop early" is true of the reading methods and false of the direction arrays
  the previous paragraph counts.
- `reference/math-and-primitives.md:116` — "two things called `Axis`" is two
  in scope; there is a third in the datafix tree, which rule 3 excludes.
- `items/loot-tables.md:130` — "a funnel with **three** fan-outs" describes the
  page's own figure, which has four branch nodes.

- `maps/biggest.md:29` — "only **two** concrete mobs make the list" is true of
  the figure's thirty and false of the table's forty (`Panda` 37th,
  `SulfurCube` 40th).
- `maps/fanin.md:24` — "the **thirty** hubs … they are **seven**" has the right
  seven idea rows, but the table's class list is 32 classes, only 24 of them in
  the thirty; six of the thirty appear in no row.
- ~~`lectures.md:220` — "**Two** components on one item" is the two *weapon*
  components; `the-spear`'s own cast lists eight `DataComponents` on it.~~
  **Overtaken** (pass 5, session A): `lectures.md`'s per-page blurbs are cut,
  and that sentence with them. The count is not settled — it survives on
  `player/README`'s watch-order line for *the spear*, which is session H's.
  [kind=book]
- ~~`lectures.md:228` — "**four** languages" is four in a login trace;
  `ConnectionProtocol` has five values and the page's own section is
  *The five phases*.~~ **Overtaken** (pass 5, session A): the blurb is cut.
  The count is not settled — it survives in `networking/README`'s verified
  line ("One socket, four languages") and in Part IX's watch order, which is
  session I's. [kind=book]

- `rendering/post-processing.md:204` — "every chain this game will ever load is
  named by a **constant** in Java, and there are only six of those". Six ids is
  right; only three are `static final` fields
  (`GameRenderer.BLUR_POST_CHAIN_ID`,
  `LevelRenderer.ENTITY_OUTLINE_POST_CHAIN_ID`,
  `LevelRenderer.TRANSPARENCY_POST_CHAIN_ID`) and the other three are inline
  literals in `GameRenderer.checkEntityPostEffect`'s switch. The count holds;
  *constant* does not.
- `rendering/the-window.md:244` — "(**both** reached from `KeyboardHandler`)".
  `ClipboardManager` is a `KeyboardHandler` field; `TextInputManager` is
  `Minecraft.textInputManager` and is reached from `Gui`,
  `AbstractSignEditScreen` and `IMEPreeditOverlay` as well.
- `rendering/entity-rendering.md:189,255` — "half" and "4x4" are right but the
  enumeration is short (`SubmitNodeCollector.submitMovingBlock` also copies only
  the `Matrix4f`; `submitFlame`, `submitShapeOutline` and `submitCustomGeometry`
  also copy the full pose); and "half a dozen others" is seven layers that hang
  something off a posed part, thirteen that call `RenderLayer.getParentModel`
  at all.
- `rendering/models-and-atlases.md:191` — "**twelve** separate layers" of
  fallback: the prose names eleven distinct failure kinds, and twelve only if
  "bakes that throw" counts as its two `ModelBakery` catches.
- `rendering/lightmap-fog-and-sky.md:60` — "a fifth of the way" is `0.22F`
  (`ClientLevel.java:274`), stated as a fraction rather than hedged.

- `commands/functions-and-macros.md:158` — "**three** lines apart" is three
  lines *between* the two declarations (`CommandSourceStack.java` 124 and 128),
  a delta of four.
- `commands/scoreboard-and-data.md:215` — `Player.canHarmPlayer` "**six** call
  sites" is six counting `ServerPlayer`'s own `super.canHarmPlayer`, five
  counting external callers.
- `commands/scoreboard-and-data.md:230` — death-message visibility has "a
  **single** reader" in the behavioural sense (`ServerPlayer.die`, which calls
  the getter three times), plus `TeamCommand`'s unchanged-check: four call
  sites in all.
- `commands/scoreboard-and-data.md:245` — "All **five** go through
  `PlayerList.broadcastAll`" is true of all five, and three of them also ship
  through explicit per-player loops
  (`ServerScoreboard.startTrackingObjective` / `stopTrackingObjective`,
  `PlayerList.updateEntireScoreboard`).
- `commands/permissions.md:224` — "only **one** of those checks is a constant
  the server itself uses" is one under *shared `PermissionCheck` constant*, two
  if `Permissions.COMMANDS_GAMEMASTER` counts, which the server reads inside
  `Commands.LEVEL_GAMEMASTERS`.
- `commands/scoreboard-and-data.md:371` — "the nicest **ten** lines" is not
  verifiable at that precision; decompiled formatting is not the source's.

**Two same-page phrasings of one constant.** `world/points-of-interest.md:235`
says "more than twenty ticks have passed" and
`entities/ai-goals-and-brains.md:335` says "fewer than 21 ticks have passed"
for the same test, `Brain.java:389` (`gameTime - lastScheduleUpdate > 20L`).
Both are true; one wording should win.

**A claim a decompile cannot settle, corpus-wide.** `javac` inlines primitive
`static final` constants at their use sites, so **"declared and never read" is
unverifiable of any primitive constant** — `Channel.attachBufferStream` writes
bare `1` and `4` where the source wrote its two named constants. Session D's
ruling (a dead constant is kept and *said to be dead*) needs the weaker wording
*no reader survives the decompile*. Known instances:
`client/the-client-loop.md:87`, `SoundEngine.MIN_SOURCE_LIFETIME`,
`ClientLevel.NORMAL_LIGHT_UPDATES_PER_FRAME`,
`ClientExplosionTracker.MAX_PARTICLES_PER_TICK`, and
`SharedConstants.TICKS_PER_SECOND` / `SharedConstants.MILLIS_PER_TICK`, which
`anatomy.md:266`'s *Is twenty ticks a second a constant?* answers "no, it is a
server field" without mentioning that both are declared at
`SharedConstants.java:149-150` and that nothing in the tree reads either.

**Hedges that came back a little short.** `client/options.md:80` "a dozen
others" is ten under the enumeration available;
`client/the-gui-render-tree.md:179` "the layering rule is thirty lines" is 27
or 52 depending on the grouping, and decompiled formatting is not the source's;
`player/status-effects.md:150` "divides by about four" is exactly 3.75;
`player/the-spear.md:46` "the one item that lets you run while using it" is one
`Item.Properties.spear` builder across seven items;
`player/player-anatomy.md:3` "five classes deep" is five on the server chain and
six on the client chain the page's own scenario is in;
`player/hunger-and-experience.md:23` lists the enchanting seed twice — it *is*
one of the four experience fields, which `player-anatomy.md:243` words correctly;
`entities/entity-lifecycle.md:131` "the **four** constants that are not the
numbers" is four if `NaturalSpawner.MAGIC_NUMBER` is excluded, five if not;
`entities/entity-anatomy.md:5` "`DefaultedMappedRegistry` overrides **nine**
lookups to hand it back" is nine overrides, six of which hand the default back;
`world/chunk-generation-pipeline.md:211` "passes **seven** of the twelve steps
straight through" is eight literal pass-throughs in `ChunkPyramid`, and seven
only because `ChunkMap.applyStep` turns `ChunkStatus.EMPTY` into the disk read —
which the same page states at :388;
`blocks/block-interaction.md:182` "three outcomes" is three distinct returned
states and four branches;
`blocks/block-entities.md:107` "four steps" of `LevelChunk.removeBlockEntity`
is four *named* steps over five statements.

**Two rules for the word *classes*, corpus-wide.** A package's class count is
one number under two rules — `package-info.java` counted, or not — and the
corpus uses both without always saying which. `anatomy/what-this-book-skips.md`
states the split it uses (tables count files, prose counts classes) and is the
only page that does. Part XIII follows the same split by accident:
`commands/game-tests.md:38` "forty-four classes" and
`commands/permissions.md:33` "eleven classes and 398 lines" exclude the marker
(the atlas says 45 and 12 / 402), while
`commands/scoreboard-and-data.md:52` "sixteen **files** and 1,442 lines"
includes both markers and matches the atlas exactly. But
`worldgen/README.md:27` says **451 classes** and explicitly adopts the atlas
rule ("one class per file … the way the atlas counts everything else"), so
*classes* means the opposite there. Session A logged this as "two size claims,
two rules"; session L settled the Part XII half by adopting the atlas rule; the
corpus still has both. **Pass 5 (or session O) should pick one and say it once**
— the natural rule is the one `what-this-book-skips` already states.

**One editorial number worth a look.**
`world/environment-attributes-and-timelines.md:5` opens on "at tick 12542 … the
sun goes under". 12542 is a real keyframe (*monsters_burn*,
*bees_stay_in_hive*), but the geometric horizon crossing the page's own
sun-angle Bézier implies is ~12782, and sunrise ~23218 against the 23460
keyframe. The gameplay flip is about 240 ticks inside the geometric day at each
end — a better sentence than the one there, if pass 5 wants it.


## Session L — Part XII World generation (pass 4) *(2026-09-05)*

**Hooks and openings rewritten around a corrected fact — re-read all of these
for voice.** Seven were rewritten because the fact under them fell:

- `worldgen/README.md`'s **opening paragraph**, which now carries a
  three-clause qualification ("not because nothing here reads the world … but
  because everything it reads is itself a function of that seed and those
  packs"). It is accurate and it is the longest sentence on the page. The
  premise deserves a shorter shape.
- `jigsaw-and-templates`' **opening**, whose lamp post is gone and whose
  mechanism now needs four sentences where the false version needed two. The
  clause "What the depth limit does is stop offering the asked-for pool at
  all" is doing a lot of work in one line.
- `trees`' **crown paragraph**, which now ends on "the asymmetry is in the
  code and vanilla data cannot express it" — true, and a stranger note to end
  a section on than the section was written for. Its header line
  ("a ceiling the crown's size was decided before") is grammatically awkward
  and was chosen for accuracy, not sound; so were the two blurbs that repeat
  it in `worldgen/README.md` and `lectures.md`.
- `structure-placement`'s **verified line** and its *Whether it is worth
  laying out* section, which now explain a deferral that lasts one statement.
  The section's title still promises a decision the section no longer
  describes.
- `density-functions`' **opening**, which now names two files where it named
  one, and loses some of the "small, honest, readable" rhythm it had.
- `biomes`' **world-spawn answer**, which went from two sentences to five and
  is now the longest *Questions players ask* answer on the page.
- `creating-a-world`'s **hook**, whose "every widget is an edit to it" became
  a clause plus an exception list. The exception list is the kind of
  named-qualifier hedge this pass is meant to hunt.

**Structural findings, not acted on.**

- `worldgen/README.md`'s *Watch in this order* closer now carries three
  separate order rulings (two before three, four reaching forward into five
  and six's status, seven before eight and nine) where it used to carry a
  clean pair. It reads as a list of caveats rather than an instruction.
- `blending`'s **first figure gained a dashed annotation node** to say that
  two of the five consumers never touch the two maps. That is prose smuggled
  into a flowchart, and the page's own text says the same thing thirty lines
  below. One of the two should go.
- `features-and-placement`'s *A feature that is a tree of features* section is
  now about six features of which one is unrelated to the section's subject
  (`Feature.NO_OP` writes nothing but is not a selector). The count and the
  subject want separating.
- `hand-built-structures`' `StructurePiece.placeBlock` cast row is now three
  clauses long and contains a negation ("not a choke point"), which is the
  *not X but Y* tic in a table cell.
- **The *Questions players ask* closer** is on nine of the eleven Part XII
  pages, well over session P's at-most-half rule of thumb. `terrain`,
  `biomes` and `structure-placement` have five, five and six answers each.

**Wording debt of the session's own making.** Several fixes name a file path
or a JSON key in italics where the surrounding prose uses backticks for
everything else (*terrain_adaptation*, *use_expansion_hack*,
*skip_existing_chunks*, *min_clipped_height*, *blending_data*). The convention
is right — `verify_names.py` rejects them backticked — but the mixture inside
one paragraph reads unevenly, and a corpus-wide look at how data keys are
typeset is worth one pass-5 sweep.


## Session K — Part XI Rendering (pass 4) *(2026-09-04)*

**Hooks and openings rewritten around a corrected fact — re-read all of
these for voice.** Six paragraphs were rewritten because the fact under them
fell, and none has had a wording pass:

- `the-frame`'s acquire-failure paragraph and its minimize Q&A (the answer
  went from "three calls' worth" to a paragraph about the ten-frame limiter,
  and it is now the longest Q&A on the page).
- `the-frame`'s partial-tick table gained a sixth row and lost the "five
  partial ticks" heading; the section is now called *six clocks in one frame*,
  which is accurate and may not be the best title.
- `models-and-atlases`' chunk-layer hook, which now carries a nine-line
  qualifier about `force_translucent` where the point is one sentence long.
  **This is the clearest over-long fix in the session.**
- `models-and-atlases`' water-animation Q&A, whose *question* changed — it
  now asks two things at once ("why does lag slow it but the pause menu not
  stop it"), which is a compound question in a slot that wants a simple one.
- `lightmap-fog-and-sky`'s opening, where "only two still read the raw world
  clock" became "only one… and the weather does not ask anybody". The new
  clause is true and the rhythm of the sentence is worse.
- `visibility-and-the-frame-graph`'s opening, which no longer resolves to one
  method and now has to say "not quite at one method" — an admission in a
  position that wants a promise.

**Structural findings (not acted on).**

- `the-window`'s seventh callback (the window-close one) is introduced in a
  section titled *Six callbacks are the entire surface* and then explained
  three sections later, under the shutdown watchdog. Either the heading or the
  ordering is wrong; pass 5 should decide which. Same page: the "rest of the
  package" list omits seven of the package's twenty-six classes, including
  `Transparency` and `TextureUtil`, and the error callback is swapped at least
  four times where the page implies two.
- `block-entity-rendering`'s completeness sweep — the page had never been
  checked, and nineteen in-scope classes and mechanisms go unmentioned. The
  ones worth a sentence each, in the agent's priority order:
  `BlockEntityRendererProvider.Context`, `WallAndGroundTransformations`,
  `BlockModelRenderState`, the crumbling-overlay source, and
  `BlockEntityWithBoundingBoxRenderer`'s game-master permission gate. Also
  unmentioned: `END_GATEWAY` and `COPPER_GOLEM_STATUE` in the built-in special
  list, the `EmptyBlockModel`/`SelectBlockModel` entries in the same table, and
  the five blocks that get a bare wrapper rather than a composite — which is
  why a block-displayed enchanting table is a book with no table under it.
- `entity-rendering` and `reference/submit-phases.md` overlap more than they
  should now that the catalogue is corrected: the lecture names four of the
  fifteen phases and exactly one of the thirteen renderers, so the "three or
  four examples from" framing the Reference page used was already generous.
  Pass 5 should decide whether the lecture wants more of the catalogue or the
  catalogue wants less of a preamble.
- `post-processing`'s per-chain table has a *what a player sees* column that
  is interpretation of GLSL the book does not quote. It survived the
  fact-check because it is not falsifiable from the sources the book uses.
  Pass 5 should decide whether to keep it, and if so to say in the caption
  that it is a reading rather than a citation.
- The landing page's pipeline figure no longer claims to be frame order, and
  the paragraph under it now spends four lines saying what the arrows are
  *not*. That is honest and it is also the longest caption in the part.

**Smaller misleading items, verified but left as they are** (each is true as
written and imprecise in a way that costs a reader nothing at this pass):
`the-frame`'s "all of this is one thread" against a client that has several;
`models-and-atlases`' "twelve separate layers" where the prose enumerates
eleven and the code has more, and its "at different coordinates" for a
same-size sprite replacement that `Stitcher` puts back in the same place;
`blaze3d`'s "applied when the pipeline is bound", its "downgrades twice" for
an if/else-if, and "every drawing class comes through this one shape" naming
two classes that never open a pass; `particles`' "one particle escapes this
system entirely", where only the *draw* escapes; `section-meshing`'s
start-up-only OOM shrink offered as the runtime answer to buffer exhaustion,
and its `hasAllNeighbors` rationale, which explains four cardinal columns
where the check demands eight plus a light test; `visibility`'s walk-trigger
list, which omits `LevelRenderer.resize` and `ViewArea.repositionCamera`;
`block-entity-rendering`'s "the two gates every extraction passes", where
there is a third at `BlockEntityRenderDispatcher.java:67`, and its "nothing
reaches back into the world", which `SignRenderState`'s live `SignText`
references break.

**On-spec material pass 5 may cut**, carried forward from pass 2's session I
and still true after this pass: `the-window` in its entirety (it is a real
gap and a real lecture, and it is also the page a viewer is most likely to
skip — the landing page now says so in as many words); `blaze3d`'s *What
replaced RenderStateShard* and *Resources and uniforms* sections, both of
which are naming-drift work rather than a lecture's; `particles`' explosion
section, a second trace on a page that already has one; and
`entity-rendering`'s thirteen-renderer and fifteen-phase lists, which now
duplicate a Reference page that has been checked row by row.

## Session J — Part X The client (pass 4) *(2026-09-04)*

### Wording to re-read (a fact fix rewrote the sentence around it)

- **`the-client-loop`'s opening paragraph.** "The server never does this. It
  runs late; the client runs *short*" was a clean two-clause contrast and it
  was false. The replacement — the server drops ticks too, but only past the
  overload threshold and never quietly — is three clauses longer and buries
  the punchline ("and says nothing") at the end. The *fact* is now right; the
  sentence is the flabbiest thing on the shortest-feeling page in the part.
  Worth a second look for a shorter true contrast.
- **`input-and-keybinds`' opening paragraph.** "None of that involves the
  tick. All of it has already happened before the tick that observes it runs"
  became a qualified version that has to concede the inventory case mid-hook.
  The concession is the more interesting fact — the drain is inside the tick —
  and pass 5 might be better off building the hook *on* it rather than
  apologising for it.
- **`gui-and-screens`' hook and verified line.** Both now carry "until you
  close it". The page's title promise (a screen the server is never told
  about) survives only for the opening, and the new last sentence — "the
  screen the server is never told about is one the server is told about
  exactly once, at the end" — is a good line that arrives after two
  qualifications. Consider leading with the asymmetry.
- **`what-makes-a-sound`'s third door.** The old paragraph was one mechanism
  stated confidently and wrongly; the new one states the mechanism *and* its
  exception (attack sounds do round trip) in the same breath, which makes the
  "three doors" framing land more slowly. The verified line still promises
  three doors and only one naming the sound, which is still true.
- **`prediction-and-acks`' state-diagram labels.** Both client exits were
  relabelled and are now long enough to crowd the figure — "endPredictionsUpTo(n),
  syncBlockState writes the absorbed state, which is a no-op if it is already
  on screen" is a sentence, not a label. The *diagram* is now true; it is also
  now the wordiest figure in Part X. Same page: the hook lost "in the same
  tick" and gained a because-clause.
- **`the-client-level`'s two weather Q&As.** "Why does thunder arrive late?"
  and "Why does rain stop and start so abruptly?" were both questions whose
  premises the code denies, so both became questions with different subjects
  ("Does the client model the speed of sound?", "Who decides how hard it is
  raining?"). Neither is a question a player actually asks, which is what the
  section is for — pass 5 should either find the player-facing version or move
  the material into the body.
- **The landing page's opening sentence** now spends a clause and two class
  names on the scheduler exception before reaching "no render thread", which
  is the sentence people will quote. Consider a footnote-shaped fix.

### Structural findings (logged, not acted on)

- **The GUI stack is watched in a different order from the one it runs in.**
  The three pages are `gui-and-screens` → `the-gui-render-tree` →
  `text-and-fonts`, but at runtime the text becomes glyphs *before* the tree
  is sorted and batched. The landing page now says so out loud, which is
  honest and clumsy — a part-shape sentence should not have to apologise for
  the watch order. Either the order changes in pass 6, or the sentence gets
  shorter.
- **`hud-elements` now has the contextual bar on two rows** (14 background, 16
  foreground) with the experience level between them, because that is the
  record order. Correct and hard to read; a merged row with a note might serve
  the reader better, if the ordering fact survives the merge.
- **`prediction-and-acks` has two figures that both explain the same
  mechanism** — a state diagram of the two machines and a sequence of the
  refusal — and the fact-check found the argument living in the prose both
  times. One of the two may be redundant.
- **The Part X landing page's verified line says "seven systems"** (the
  figure's seven spokes) over a part of twelve pages. Both are true and the
  reader meets the mismatch immediately.
- **`anatomy/anatomy` is a Part X dependency that no Part X page links.**
  Session A logged the cross-link as pass-5 work (pass4.md:2765); this session
  re-derived that it is genuinely used — `the-client-loop`'s hook contrasts
  the two loops — so the link belongs in that hook's paragraph.


## Session G — Part VII Items and inventories (pass 4) *(2026-09-04)*

### Wording to re-read (a fact fix rewrote the sentence around it)

- **`enchanting`'s title and its opening section.** The H1 was *Enchanting: five
  ways onto an item* and is now *Enchanting: the five paths, and what each one
  is allowed to do*, because the grindstone is a removal; the section *The one
  line all five end on* became *The one question all five ask*, because the
  shared method does not exist and the shared *decision* does. Both are longer
  than what they replace. The verified line still says "picks up enchantments
  four other ways", which is now the only place the old framing survives — check
  it reads right beside the new title.
- **`items/README.md`'s shape paragraph.** "every later page assumes all three"
  was false, and the replacement admits that *contexts and predicates* is the
  outlier and could be watched first. That is a truer paragraph and a wordier
  one; it also now half-contradicts the numbered list's "the first three in
  order, then the engines in any order you like", which was already loose.
- **`items/README.md`'s *before you start*** grew from two ordering facts to
  three when `server/server-tick` was added. The paragraph is now the longest on
  the page.
- **`containers-and-menus`' advancement-channel paragraph.** The claim "nothing
  calls back into the menu" had to be scoped to the chest and the exceptions
  named, which turned one clean sentence into four.
- **`loot-tables`' world-gen paragraph** and its `BuiltInLootTables` category
  list: the list was incomplete and is now longer. It is nine items in a book
  whose budget is seven.
- **`recipes`' reload-window paragraph**, rewritten from "a window that is short
  and, on a reload, real" to an explanation of why nothing can observe it. The
  punchline is gone and the paragraph is longer; it may want cutting to a
  sentence.

### Structural findings (logged, not acted on)

- **`items-and-stacks`' *Two validators, one rule, two spellings* table** now has
  an *on failure* cell that is three clauses long, because the three
  `ItemStack.validateStrict` call sites do not agree. It is the only cell in the
  corpus that has to disambiguate its own row. **Checked, session G (pass 5)**:
  the section is ruled `items-and-stacks`' outright and grew rather than
  shrank, so the cell stands as it is; the fix is a sentence under the table
  rather than a fourth column. [kind=lecture]
- **`enchanting`'s five-path table** is doing too much: after this session two of
  its cells carry three clauses each (the providers-and-loot gate and filter).
  Either the table narrows to the three columns that behave alike, or
  `EnchantRandomlyFunction` gets a sentence of its own. **Session G's note**:
  the sentence now exists — the corrected `selectEnchantment` paragraph names
  which four paths select and which two roll their own — so pass 6 can cut the
  cells to a pointer rather than inventing prose. [kind=lecture]
- **`items/README.md`'s figure** lost an edge (`CM → CP`) and re-sourced another,
  so the second tier now has one node with no incoming arrow. That is *true* —
  contexts and predicates depends on none of the vocabulary — but a flowchart
  with an orphan node reads like an omission. Pass 5 should decide whether the
  figure wants a second, disconnected cluster or a note.
- **`contexts-and-predicates`' figure 1** gained a node outside both subgraphs
  (`SlotSource`). Same question: three groups, or two and a stray.

### Counts that are fine but say nothing

- **`items/README.md`:47** "the four ways one stack is serialised" is a count of
  *destinations* borrowed from `foundations/codecs-nbt-json`, not of anything in
  the decompile — `ItemStack` declares seven public serialisers. Correct as a
  cross-reference, meaningless as a number. Pass 5 may want to drop the number.

### The closer device

Part VII is **2 of 9** on *Questions players ask* (`loot-tables` and
`enchantments`), which is under session P's rule of thumb and needs nothing.

### For the terminology sweep

- The part says *the wire*, *the connection* and *the network* for the same
  thing, sometimes in one page (`containers-and-menus` uses all three).
- *Prototype* means the item's default `DataComponentMap` on `items-and-stacks`
  and nothing else anywhere; the glossary has it, but it reads as jargon on
  first use in `enchanting`.


## Session F — Part VI Entities (pass 4) *(2026-09-04)*

**Rewrites logged for a re-read.** Every fix below replaced a sentence pass
4 falsified; the wording is new and has not been read for voice.

- **`pathfinding`'s hook** — "eight ticks later" became "a hundred ticks
  later", which now agrees with the page's own second paragraph but repeats
  its number in the first two sentences. Worth deciding which of the two says
  it.
- **`pathfinding`'s malus illustration** — the fire/spider pair became a
  three-way lava example (`Strider` 0.0, `ZombifiedPiglin` 8.0, ordinary
  piglin −1). Three species in one clause is a lot for a sentence that is
  already carrying nine constants.
- **`pathfinding`'s `MoveControl` paragraph** grew from four sentences to
  seven, because "the single method" had to become "not the only method, not
  a single call site, and here are both other entrances". It is the longest
  paragraph on the page now and reads like a correction rather than an
  explanation.
- **`synched-entity-data`'s hook** was rewritten whole: the JVM
  static-initialiser claim is gone and the replacement ("written nowhere in
  `Sheep`; one new field on `Entity` would renumber every entity in the
  game") is a better fact but a longer sentence, and it now says in the hook
  what the section at L35-42 says again.
- **`authority`'s fall-damage paragraph** is four sentences where it was
  two, because the true statement needs both sides plus the
  `ServerLevel`-gate reason.
- ~~**`ai-goals-and-brains`'s control-flag paragraph** now carries two
  mechanisms (the five-tick refresh and the leash) where it carried one, and
  the boat sentence has to distinguish *a mob is steering me* from *I am in
  a boat*. Check whether the leash belongs here or in a sentence of its own.~~
  **Done, session F (pass 5)**: a sentence of its own, and the answer to the
  question is that the leash is not a control flag at all — it is a second
  lever on the same lock table, and the page now says so. `Leashable` stays
  `entity-anatomy`'s.
- **`entity-anatomy`'s registry paragraph** gained a second override
  direction (`getOptional` calls `super`), which is the subtlest thing on the
  page and is currently one clause.
- **`damage-and-death`'s blocking sentence** now names `Hoglin` and
  `Ravager` to prove who is knocked back. Good evidence, but it is an aside
  inside an aside.

**Structural findings, not acted on.**

- **`authority` states its own subject with the wrong number in four
  places** ("the four predicates" as a section heading, a closer heading, the
  hook and the cast row). Pass 4 corrected all four to five, but a page whose
  organising count changed is a page whose headings should be re-read
  together.
- **`entity-lifecycle`'s spawn-cascade figure gained a seventh rejection
  edge** to put `isValidSpawnPostitionForType`'s tests in source order. It
  is now sixteen edges and is the densest figure in the part.
- **The *Questions players ask* device**: Part VI is 3 of 10 under the
  literal heading (`ai-goals-and-brains`, `attributes`,
  `synched-entity-data`), which is inside session P's at-most-half rule —
  but two more pages carry the same device under a different name
  (`authority`'s *What the predicates explain*, `pathfinding`'s *Why mobs
  look stupid*), which makes 5 of 10 and is a data point for the *four
  spellings* problem session A logged rather than for the count.
- **`entity-anatomy` and `entity-lifecycle` both explain
  `EntityType.create`'s feature-flag and Peaceful gates**, from opposite
  ends — anatomy as *type to object*, lifecycle as the last filter before a
  mob exists. Not a shared skeleton, but a paragraph pass 5 could cut from
  one of them and cross-link.

## Session E — Part V Blocks (pass 4) *(2026-09-04)*

Wording debt from sixty-one fact fixes across eight pages. Nothing here was
acted on; pass 4 does not polish.

**Rewrites to re-read.** Five fixes grew a sentence into a passage:

- `signal-and-dust`'s **hook**. The old one was a picture ("14, 13, 12, visibly")
  and the true replacement is a picture plus a denial ("that staircase is the
  whole cost of redstone, and nobody has ever seen it"). It reads well but it is
  now the longest opening paragraph in the part, and the *why* — that the packet
  is built once per tick from the world rather than from the writes — is
  repeated three paragraphs later where the flowchart explains it. One of the two
  should go.
- ~~`blocks/README.md`'s **opening**.~~ **Done** — a third option, taken: the landing page now opens inside the two scenarios (a door, a lamp) rather than on book furniture, and the *first of those is a prediction and Part X owns it* clause moved down into the paragraph that is about the V-to-X cut, which is what motivates it. All three feelings survive and the part's first paragraph carries no forward reference.
  *(original entry follows)*  Splitting the three feelings into "the first
  is a prediction and Part X owns it" plus "the other two" costs a sentence and
  puts a forward reference in the part's first paragraph. The alternative is to
  drop the crosshair feeling and open on two, which is tighter but loses the one
  a player notices first.
- ~~`pistons-and-block-events`' **flag table**~~ **Half done** — the paragraph under the table is cut from six lines to two, and the digression about why the 82 row does not fire is folded into the sentence that lands on the placeholders. The table's width is a `custom.css` question and stays for pass 7.
  *(original entry follows)*  went from four rows to five and
  gained a *written by* column, because one of the four was not `moveBlocks`'s.
  The table is now wide enough to want the `custom.css` treatment, and the
  paragraph under it gained four lines explaining why the 82 row does not fire in
  the page's own scenario — true, and a digression inside the page's punchline.
- `block-breaking`'s **durability answer** grew from two sentences to five to
  carry `Item.mineBlock`'s three conditions and the shears exception. It is the
  page's best *Questions players ask* entry and it is now its longest.
- `diodes-and-observers`' **comparator fan-out paragraph** now names two callers
  and says which one the example uses, where it named one. The correction is
  right and the paragraph has lost its shape: the interesting fact
  (`BlockEntity.setChanged` is what makes a comparator notice a chest) is now
  third in the sentence order rather than first.

**The "three differences" tic, and the shape it hides.** `diodes-and-observers`'
comparison table is introduced as five rows because it *has* five rows, which is
honest and flat. The real structure underneath is two axes — repeater against
comparator (four differences, all about arithmetic and priority) and diode
against observer (one difference, the channel) — and the table flattens them into
one grid where the observer column is mostly "nothing". Pass 5 should decide
whether that is one table or two.

**Ambiguities left standing.**

- `diodes-and-observers` says `DiodeBlock.shouldPrioritize` holds for "a diode
  whose own input is not on the far side of it". That is exact and hard to read.
  The colloquial version — "a diode that is not pointing back at this one" — is
  also exactly right, but only under the reading of *pointing* the page spends a
  paragraph arguing against (FACING points at the **input**). Either the page
  needs a word for the output direction or the sentence needs a diagram.
- The same page says a diode "restricts `DiodeBlock.getSignal` to the one
  direction it faces" two paragraphs before establishing that FACING is the
  *input* side. Both sentences are true — the `direction` parameter of `getSignal`
  is the direction from the asker to the answerer, so it equals FACING when the
  output block asks — but a reader meets them in the order that makes them look
  contradictory.
- `block-interaction`'s bit-8 clause now carries a condition ("when the Chunk
  Builder option asks for it") inside the sentence that is supposed to be the
  page's payoff. It may want to be a parenthetical or a footnote instead.

**Structural findings, not acted on.**

- **~~`block-entities` is the part's odd page and the landing page now says so
  awkwardly.**~~ **Done** — the fourth clause is gone. The landing page's argument is now the two channels seen through a door and a lamp, and the part is described as choosing a state, performing a write, or being a block that answers one; `block-entities` is the page about state that outgrew a block state, which needs no clause of its own.
  *(original entry follows)*  It is not about choosing a state, performing a write, or answering
  a neighbour's write; the landing page's opening had to grow a fourth clause
  ("or — once — about the state a position cannot hold at all") to cover it. The
  cleaner reading is that Part V has a hub, two click lectures, a redstone trio,
  and one page about state that outgrew a block state.
- **~~`signal-and-dust` carries two subjects.**~~ **Ruled: it stays, as the page's counterfactual.** No other page can own the experimental evaluator — the flag pages own the flag, not the evaluator — and the question it answers (why the staircase is avoidable) is the one this page's scenario raises. What made it read as a second subject was that it stopped using the trace; a pass-6 note is logged to run the same lever and two dust through it.
  *(original entry follows)*  The default evaluator and the
  experimental one are the same computation with different semantics, and the
  page gives the second a full section plus a closing paragraph. It is the right
  material; it is also the point at which the page stops being about a lever and
  two dust.
- **`blocks-and-states`' write flowchart now has eleven nodes and a subgraph**
  after gaining the no-op branch. It is the most linked-to figure in the part and
  the densest; it may want splitting into the chunk write and the tail, which are
  already two subgraphs.
- **Six Part V pages end on *Questions players ask*** (all but the landing page
  and `blocks-and-states`), against session P's rule of thumb of at most half a
  part. This part is the worst offender per page in the book.

**Corpus-wide, found here.** The corpus has no settled word for the two update
channels' *directions*. `block-interaction` says "the direction pointing from
that neighbour back at the door"; `signal-and-dust`'s table says "which neighbour
is told first"; `diodes-and-observers` says "the one direction it faces". Three
pages, three conventions, one `Direction` parameter. A terminology sweep should
fix the vocabulary before the pages.

## Session D — Part IV The world (pass 4) *(2026-09-04)*

Wording debt from forty-nine fact fixes across eleven pages. Nothing here was
acted on; pass 4 does not polish.

**Rewrites to re-read.** Four fixes grew a sentence into a passage:

- `points-of-interest`'s **hook**. The old one was a clean negative ("two facts
  that never speak to each other") and the true replacement is a direction
  ("speak in one direction only … can only take a claim away"), which costs a
  clause and a sentence in the page's densest paragraph. It is now three
  sentences where it was two. Worth trying as one.
- `environment-attributes-and-timelines`' **easing paragraph** gained four lines
  and three numbers (0.67×, 1.19×, 13,564 against 10,436). The day-length fact
  is the better punchline and probably wants to be *in the hook* rather than two
  thirds of the way down a page whose hook is about colour — a structural call,
  not a wording one.
- `chunk-generation-pipeline`'s **radius-11 derivation** now explains
  `ChunkStep.Builder.getRadiusOfParent` in the middle of a paragraph that was
  already the page's most arithmetical. The true rule ("a debt counts only when
  the step's own parent already sits a ring out") may deserve to be its own
  sentence, or a row in the table above it.
- `chunk-storage`'s **IOWorker priority paragraph** gained five lines saying what
  the shutdown barrier is and why a flush still waits. The section's subject is
  "why the server thread never waits", and this is a digression inside it.

**The dead-constant tic.** Four fixes in this part took the same shape: *the
number is right, the constant that names it has no readers*, so the prose now
says so — `AcquirePoi.SCAN_RANGE`, `SculkSensorBlock.ACTIVE_TICKS`,
`LevelChunkSection.BIOME_CONTAINER_BITS`,
`ThreadedLevelLightEngine.DEFAULT_BATCH_SIZE`, plus
`ChunkStatus.MAX_STRUCTURE_DISTANCE` which the pipeline page already flagged.
Five instances of one aside in one part is a tic. Pass 5 should pick one voice
for it and use it everywhere in the corpus, and probably drop the aside on the
pages where the constant is not otherwise mentioned.

**Named-qualifier debt.** The count corrections replaced round motifs with
awkward ones: "eleven chunks past the edge of view" became "thirteen chunks past
the ticket that asked for it", and "up to 27 sections across nine chunks" became
"up to fourteen sections across seven chunk columns". Both are true and neither
scans. `tickets-and-loading`'s header line was rewritten for the same reason and
lost its scenario ("a chunk eleven chunks away becomes a ticking part of the
world" → "a column of chunks thirteen past the edge of view is asked for"); the
header should get its ticking image back around the true number.

**Structural findings, not acted on.**

- ~~`chunk-anatomy`'s "packing buys a smaller palette, not narrower entries"
  contradicts its own "can demote a container a whole rung" a few lines later.
  Both are true of different cases; the sentence needs splitting, not correcting.~~
  **Done, session D (pass 5)** — and it was a correction, not only a split: the
  head clause is false, because `PalettedContainer.pack` measures the shrunken
  palette against the same ladder and *does* narrow entries in two cases.
  Logged in [pass9.md](pass9.md).
- ~~`lighting` says `SkyLightEngine.checkNode` "only decides what to enqueue" in
  one paragraph and describes it writing stored levels in the next. A clash
  between two paragraphs, not an error in either.~~ **Done, session D (pass 5)**
  — and the general sentence was the wrong one: both engines' `checkNode` writes
  a stored level. Corrected, logged in [pass9.md](pass9.md).
- ~~Part IV's landing page still calls the part "the four side-systems that make
  the world they hold feel alive" in its header while its shape paragraph now
  counts five pages off the conveyor.~~ **Done, session D (pass 5)** — the header
  now names the environment page separately from the four side-systems, and
  `lectures.md`'s conveyor count was made to follow the landing page's.
- ~~`points-of-interest` describes `PoiManager.isVillageCenter`'s predicate without
  saying it reads through the **non-loading** `SectionStorage.get`.~~ **Done,
  session D (pass 5)** — written as its own callout under *What makes a village*,
  re-derived against `PoiManager.java:195` and `SectionStorage.java:121`, with
  the reason it is deliberate (the flood settles every tick and must not touch
  the disk).
- The cross-links session A logged here as pass-5 work are half done:
  `chunk-anatomy` now links `foundations/identifiers-and-registries` (pass 4
  needed it for addition 2). Part XII's two are still open.

## Session C — Part III The server (pass 4) *(2026-09-04)*

Wording debt from twenty-eight fact fixes. Nothing here was acted on; pass 4
does not polish.

**Rewrites to re-read.** Three fixes grew a sentence into a passage and each
should be read again for rhythm rather than for truth:

- `starting-a-server`'s **opening paragraph**. Its frame ("Between those two
  lines the server …") was inverted — five of the six things listed happen
  before *Preparing level* prints — and the fix adds a clause and a second
  sentence to a paragraph that was already the page's densest. The hook is
  untouched. Worth trying as two sentences instead of one long one.
- ~~`server-tick`'s **packet-drain paragraph**~~ **— overtaken. Checked by
  session C of pass 5 against the page: it is three lines, not five, and it
  already points forward ("so chat and commands arrive as *tasks*, drained by
  the event loop below, and not with the packets"). The exception belongs
  beside the rule it qualifies; nothing to move.**
- `server-level-tick`'s **falling-sand exception** is now its own paragraph
  after "The ordering is visible from a client". That is the right place for
  it factually, but it means the section's punchline is immediately
  qualified. Consider leading with the exception and landing on the rule.
  *(Re-checked by session C of pass 5 and still live; it is a section-order
  finding, so pass 6's.)* [kind=lecture]

**Repeated hedges introduced.** "Almost nothing", "almost none", "all but the
first", "two of the three endings", "on this side of the jar" — five new
qualifiers in one part, each earned individually. Read them together; if the
part now reads as hedged, some of them want re-scoping into a positive claim
instead ("`FallingBlockEntity` is the one place that …").

**Structural findings, not acted on.**

- ~~**`how-a-server-dies` carries two subjects.**~~ **Ruled by session C of
  pass 5: a section, not a page.** *What you lose if you kill the process* is
  the answer to the page's own question — it says what each of the three
  endings costs you, which is the comparison table's payoff and exists
  nowhere else in the book, so it cannot leave. What it also held has gone to
  its owners: the autosave cadence to `server-tick`, the per-chunk save
  spacing to `chunk-storage`, `session.lock`'s nature to `starting-a-server`.
  A durability page built from what is left would be a page of other pages'
  material.
- **`server-tick`'s event-loop figure grew from eleven edges to fourteen**
  when the two impossible ones were replaced by a truthful queue-empty exit.
  It is now the densest flowchart in Part III and its `C` node label is long
  enough to be a sentence. Correct, but worth redrawing for shape.
- **`starting-a-server`'s sequence figure gained an arrow** (the pack-opening
  stage moved onto the `Main` lane) and split `spin` into three. At 27 items
  it is now the largest single diagram in the part — `server-level-tick` has
  more in total (35) but across two figures.
- **Part III is 2 of 5 on *Questions players ask*** (`server-tick`,
  `server-level-tick`), which is *inside* session P's rule of thumb and one
  of the better parts on the device — recorded here because the corpus-wide
  pass needs the parts that are already fine as much as the ones that are
  not. The session's own first guess at this number was five, and counting
  it settled the matter; treat every per-part count in this file the same way.

**Small.**

- `players-and-sessions`'s section heading *Four ways the session changes*
  now sits above a paragraph that names a fifth (the end credits). The
  heading is still the right frame for the comparison, but the tension is
  visible; a reader who counts will stop.
- `server-tick`'s `tickChildren` table row about the player-info broadcast
  now reads "its own counter has not passed 600 — so every 601st call, not
  every 600th tick", which is two corrections in one cell and the longest
  *skipped when* value in the table.
- The em dash count in `how-a-server-dies`'s durability section went up by
  four with the watchdog asterisk. Whole-page voice pass.

## Session B — Parts I and II (pass 4) *(2026-09-04)*

Wording debt and structural findings from Part I and Part II's fact-check.
Every factual fix is in `docs/pass4.md`; nothing below was acted on.

**Wording to re-read** (a hook or an argument was rewritten around a
correction):

- `src/systems/anatomy/README.md` — the opening hook and the first *Watch in
  this order* teaser were both rewritten mid-sentence. The hook now says
  "every sequence diagram … lanes that name classes and assume you know
  which thread each class is on", which is true and two clauses longer than
  the sentence it replaced.
- `src/systems/anatomy/anatomy.md` — four paragraphs grew a qualifying
  clause each: the bootstrap ordering, the crash relay, the singleplayer
  differences and *Everything else that matters is serialised onto*. The
  crash paragraph is now the longest answer under *Questions players ask*
  and carries three class names it did not before.
- `src/systems/foundations/identifiers-and-registries.md` — the opening
  paragraph's last sentence was the hook's causal clause and is now two
  sentences. It is true; it no longer lands.
- `src/systems/foundations/tags.md` — the hook's first sentence now carries
  a parenthetical about component prototypes before it reaches
  `Registry.PendingTags`, which is the thing the page is about. Consider
  moving the second swap to *Prepared, then applied* and leaving the hook a
  single clause.
- `src/systems/foundations/data-driven-types.md` — the *Fifty-six of them*
  paragraph gained the criterion's two exclusions and is now the densest
  paragraph on the page. The number is right; the sentence explaining it
  reads like a footnote promoted.
- `src/systems/foundations/codecs-nbt-json.md` — the *homogeneous numeric
  list* sub-section was inverted, so its bolded lead sentence is now a
  double negative ("A numeric array stays an array, but nothing turns a list
  into one"). Worth one more pass.

**Structural findings**, logged and not acted on:

- ~~**`anatomy/README.md`'s root figure is not homogeneous.** Four of its five
  edges point at *parts*; the fifth points at a *page* of Part I (*what this
  book skips*). Either is defensible; the mix is what a reader notices.~~
  **Done, session B** — redrawn as the part's own two pages, which is what
  `TEMPLATE.md`'s landing-page rule requires and what the other twelve do. The
  book-shaped graph it used to draw was a third statement of Part I's place in
  the parts graph, and it disagreed with the other two.
- ~~**`anatomy/README.md`'s hook says "a server that ticks and a client that
  draws".** The client ticks too — 0 to 10 times a frame, which is the
  lecture's own first arithmetic. The shorthand is deliberate and the
  lecture unpacks it two pages later, but as the sentence a reader memorises
  it plants the wrong idea. A pass-5 judgement, not a fact fix.~~
  **Done, session B** — the hook now contrasts the two *loops* rather than
  ticking against drawing: "a server whose whole life is a tick loop, and a
  client whose life is a frame loop with ticks inside it".
- **`identifiers-and-registries`'s "the wire id is the line number".** True
  as a metaphor for the ordinal of the registration statement and false
  read literally (`Items.DIAMOND_SWORD` is at `Items.java:993` and its raw
  id is nowhere near 993). The lecture unpacks it in the next two sentences;
  the landing-page teaser and the verified line do not. Decide whether the
  teaser keeps the metaphor.
- **`reference/class-index.md` is still blind to diagrams** (session A's
  finding) and Parts I and II are among the worst affected: every lane in
  the anatomy, tags and data-components figures is a `participant X as
  ClassName` the index cannot see.
- **Cross-links session A judged missing** and left to pass 5 touch this
  part: ~~Part X ← `anatomy/anatomy`~~ (still open, and session J's: the link
  belongs on `the-client-loop`, not here — session B re-derived it and it is
  the depending page that must change), Part IV and Part XII ←
  `identifiers-and-registries` and `codecs-nbt-json`. Each is a real
  dependency with no link or backticked slug on the depending page.

## Session A — The frame (pass 4) *(2026-09-04)*

Wording debt and structural findings from the frame's fact-check. Nothing
here was acted on; every factual fix is in `docs/pass4.md`.

**Wording to re-read** (a hook or an argument was rewritten around a
correction):

- `src/introduction.md` — the figure paragraph and the skip-list sentence were
  both rewritten mid-sentence; the skip list is now a longer list and reads
  like one.
- `src/lectures.md` — the Part III "watch the environment page first"
  paragraph lost its superlative ("the page with the most dependants in the
  book") and gained a cost argument. It is true now; it is not as good a
  sentence.
- ~~`src/systems/server/README.md` — the *before you start* section grew a long
  second paragraph~~ **— done by session C of pass 5, in the rewrite to the
  landing-page role. The environment-attributes paragraph is cut from three
  sentences of mechanism to one sentence and an anchored link (the mechanism
  is that page's), and the count was wrong anyway: at 200 words it was third,
  behind `networking/README` at 222 and `blocks/README` at 210.**
- `src/maps/fanin.md` — the hook now spends three lines on what the chart does
  not count before it gets to the surprise.
- `src/maps/packages.md` — the `net/minecraft/data` clause became a
  four-line aside with a cross-link.

**Structural findings** (not acted on, per the charter):

- ~~**The nine-page dependency table's membership rule is unstated and
  inconsistent.** By its own criterion — a page two or more landing pages
  assume — three Part II pages qualify and are absent (`resource-system`:
  VII and XI; `text-components`: IX and X; `data-driven-types`: XII and XIII),
  while a one-part dependency (*contexts and predicates*, XIII only) is in it
  and `world/chunk-generation-pipeline` (XII, called "hard" by the page) is
  not. State the rule or fix the membership.~~ **Done** (pass 5, session A):
  the rule is stated above the table — two or more landing pages, less the
  three every part assumes — the membership fixed to it (in:
  `resource-system`, `data-driven-types`, `text-components`; out:
  `blocks-and-states`, `contexts-and-predicates`, `the-client-loop`, each now
  named in the paragraph below the table), and `check_deps.py` fails on a
  mismatch either way. `chunk-generation-pipeline` stays out: only Part XII
  names it. [kind=book]
- ~~**Part IV's sidebar order disagrees with its own landing page.**
  `src/SUMMARY.md` lists *environment attributes and timelines* sixth in Part
  IV; `world/README.md`'s *watch in this order* and `lectures.md` both list it
  first. Part IV is the only part where the three orders differ (checked for
  all thirteen). `lectures.md` was reworded this session to say "Part IV's own
  watch order lists it first", which is true but papers over the split.~~
  **Done** (pass 5, session A): ruled that the landing page's *watch in this
  order* is the book's order and the sidebar and the lecture map follow it;
  `SUMMARY.md` moved, `lectures.md`'s papering-over sentence replaced, and
  `check_deps.py` now fails when the three disagree. Session D may re-judge
  the order itself; it may not leave the three disagreeing. [kind=book]
- ~~**The class index labels every landing page "README".** Eleven distinct
  pages render under that one word; 26 rows carry at least one and nine carry
  two or more — in the `LivingEntity` row the reader sees "README" three times
  with nothing to tell them apart. Label by part.~~ **Done** (pass 5, session
  A): `verify_names.py --index` labels any `README.md` with its own `#`
  heading — *VI · Entities*, *Reference*, *The atlas* — which needs no table
  in the tool and follows a retitling. [kind=book]
- **Teach the class index to read diagrams.** 135 class/page pairs and 112
  classes are named only inside mermaid blocks (51 of them as
  `participant X as ClassName`), and 26 of those classes have no row at all.
  The page now states the limitation; removing it is the better fix.
- **The lane key carries 45 rows no page claims**, against session E's ruling
  that it is pruned to lanes in use. Three appear nowhere but `lanes.md`:
  `PTT`, `TCTD` and (until this session) `TDec`. `PTT` is `TEMPLATE.md`'s
  worked example of the nested-class rule and its pilot page has since become
  a flowchart with no lanes, so the rule's only illustration is unused.
- **Two lanes for one class, on purpose.** `RCPL` and `CPL` are both
  `ClientPacketListener`, because the chat diagram shows the sender's client
  and the recipient's at once. Recorded in `TEMPLATE.md`'s collision prose and
  in a note inside the figure; if pass 5 dislikes it, the alternative is two
  identically-labelled lanes.
- **`reference/submit-phases.md` is a catalogue that needs a paragraph.** Its
  "order bucket" and "may be reordered" language is unexplained without
  `SubmitNodeStorage` and `PhaseSubmitGrouper`; that is a page shape question,
  not a fact.


- **2026-09-03, session M — Part XII.** Eight system pages plus a landing
  page and a Reference page. **Every page landed inside the 260–340 brief or
  below it** — 204 to 288, with the landing page at 143 and the Reference
  page at 152 — and three pages came in under 240, which is the first time a
  part has *undershot*. **Zero bulleted lists across the whole part**, as in
  Part XI. Four cuts, all from the old `worldgen-pipeline`, now `terrain`,
  and none of them a fact the corpus loses: `NoiseSettings.guardY`'s
  multiples-of-sixteen validation (a codec detail with no visible
  consequence); the registries inventory at the foot of the page (the
  data-driven type pattern owns that table and three of its rows now link
  here); the `ChunkStatusTasks` caller list (Part IV owns the conveyor and
  the landing page makes the dependency explicit); and the `Heightmap.Usage`
  taxonomy (the *status, not the step* half survives, and `chunk-anatomy`
  already has the rest). Two more facts were **moved rather than cut** and
  are in [pass4.md](pass4.md) instead: the minus-one default write radius
  and `WorldGenRegion.getChunk` throwing, both now stated only on
  `features-and-placement`, which is where they bite.

  Wording debt:

  - **The *questions players ask* device is on six of the eight pages**,
    which is the ratio session K flagged in Part X and the trap the old
    seven-heading template fell into. It is genuinely the honest home for
    what used to be an invariant wall, which is exactly why it spreads.
    Session P should count it as a *device* becoming a *slot*, and pass 5
    should consider a rule — at most half the pages in a part.
  - **Session K's two formulas are gone from Part XII too.** No page says
    "the one sentence a player recognises" and none carries a
    names-you-will-hunt-for list; two pages use the *for a 1.21-era reader*
    blockquote instead (`density-functions` on the two vocabularies for the
    six climate functions, `jigsaw-and-templates` on the singular
    *structure* folder). With X, XI and XII converted the formulas survive
    only in Part XIII.
  - **Second person, now five parts wide and needing a ruling rather than
    another flag.** `terrain` opens with *you dig into a cave*, `biomes`
    with *walk out of a desert*, `trees` with *plant a single dark-oak
    sapling*, `structure-placement` with *type the locate command*. It is
    the most natural way to start inside a scenario and it is the house
    style now whether or not anyone decided it. Sessions I, J and K all
    flagged the drift.
  - **`terrain`'s title is a compromise.** The page is noise, surface and
    carvers — three statuses — so *Terrain* is broader than its subject,
    while its old name collided with Part IV's *chunk generation pipeline*.
    If pass 5 finds a better name the redirect already exists and a second
    costs nothing.
  - **The lattice fact is stated three times across two pages** — twice in
    `terrain`, at its two resolutions, and once more in `density-functions`
    from the cache side. All three are true and it is the part's best "true
    twice over" observation, but one of the three should become a link.
  - **`jigsaw-and-templates` is the shortest page in the part** at 204
    lines, because the processor stack is described rather than traced. If
    pass 5 wants a section trimmed elsewhere, this is the page that could
    absorb it instead.

- **2026-09-03, session L — Part XI.** Eleven system pages plus a landing
  page and a Reference page. **Every page landed inside the 260–340 brief**
  — 256 to 339, with the landing page at 150 and the Reference page at 81 —
  which is the first part to need no length note at all, and the brief was
  given to the drafters in the prompt rather than corrected afterwards.
  **Zero bulleted lists across the whole part**: every one of the eight old
  pages opened with a field inventory and closed with a twenty-bullet
  invariant wall, and none of that survives. The material is in cast tables,
  decision tables, *Questions players ask* sections and the sentences that
  use each name. `lightmap-fog-and-sky` came *down* from 447 to 339 by
  dissolving the twenty-four-attribute enumeration Part IV already owns.

  The one shape note pass 5 might revisit: **`models-and-atlases` carries a
  single figure over 330 lines.** Its drafter cut a sequence diagram that
  repeated the fan-out flowchart, which was right, and cut an item-model
  flowchart with it, which is arguable — the *How an item picks its model*
  section is where two forward links from Part VII land and it is now the
  page's longest stretch of unbroken prose.

  **Cuts made, all field inventories, no behaviour:** `the-frame` dropped the
  `GameRenderer` field roll-call (eleven fields), most of the `GameRenderState`
  and `CameraRenderState` field lists, and the `CrossFrameResourcePool`
  mention, which asserted only that the pool exists and is three frames deep;
  the `Camera` accessor roll-call is compressed to four examples inside the
  1.21 blockquote. `lightmap-fog-and-sky` dropped the twenty-four-item
  `EnvironmentAttributes` list outright — every constant on it now appears in
  the sentence that consumes it, and the system itself is Part IV's — along
  with the `EnvironmentAttribute` builder and flag inventory and the
  `Timeline`/`ClockTimeMarkers` tour, all of which Part IV already teaches.
  `particles` dropped the nine-class inventory into the cast table.
  `entity-rendering` moved its fifteen-phase and thirteen-renderer catalogues
  out to `src/reference/submit-phases.md` and its render-state ladder to a
  generated figure. `blaze3d`'s naming-drift bullet became a two-column table. And
  `models-and-atlases` dropped a long tail of identifiers with no facts
  attached — the `ModelManager` field and getter roll-call, `ModelBakery`'s
  destroy-stage constants and the two fire sprites, `ModelBakery.BakingResult`'s
  members, the four `ResolvedModel` parent-walking helpers, `Sheets`,
  `SpriteGetter`, `TextureAtlasSprite`, `Stitcher.registerSprite`,
  `Variant`/`VariantMutator`, and the observation that there are two
  `MaterialBaker`s. Nothing behavioural went with them, but that last one was
  the mechanism behind the block-atlas rule the page still states, so pass 5
  should decide whether the rule now floats. `blaze3d` cut its
  `RenderSystem` member roll-call, and one member in it was doing work:
  `RenderSystem.outputColorTextureOverride` and
  `RenderSystem.outputDepthTextureOverride` were the only mention anywhere in
  the corpus of *where the world can be redirected*, and no page names them
  now. `lightmap-fog-and-sky` dropped one behavioural sentence
  with its field inventories: `FogRenderer.endFrame` and
  `CloudRenderer.endFrame` rotating their ring buffers at the close of a
  frame. Worth restoring if a line becomes available, since it is the only
  mention of what ends those two buffers' frames.

  **Wording debt.** The *headline for a 1.21-era reader* formula that opened
  eight of eight Part XI pages is gone as an opening and survives as one
  blockquote at the foot of each — the same move session K made, so the
  device is now consistent across two parts and pass 5 should check it reads
  as a convention rather than a tic. Three pages open on a second-person
  scenario in the present tense (*you fly forward in creative*, *you
  right-click a block into place*, *stand on a hill and watch the light go*),
  which is the strongest opening in the part and also, at three, the point at
  which it becomes a pattern. `particles`' *Where to look* is a
  middle-dot list where every other page's is a sentence; it reads fine and it
  is the only one, so it is either a deliberate variation or a fix.

- **2026-09-02, session F — Part V.** Seven pages at 243–388 lines, which is
  the first part to land inside the 260–340 brief rather than over it — the
  line budget was given to the drafters explicitly this time, mid-flight, and
  it worked. The exception is **`blocks-and-states` at 388**, and it is the
  one page here with a genuine length case to answer: it carries two figures
  (the twelve-class containment figure and the write flowchart the other six
  pages link to), the flag-bit table, and a grounding trace. Its cheapest cuts
  if pass 5 needs them, in order: the *Twelve classes and one Cartesian
  product* figure could lose the three `Property` subclasses to prose; the
  *four decisions, four lookups* section is the most compressible, since
  `StairBlock.getStairsShape`'s corner rules are detail the hook does not
  need; and the `BlockBehaviour.BlockStateBase.initCache` thread-safety
  paragraph is the page's most self-contained.

  **Cuts made, and where they went.** All are names rather than claims.
  `block-interaction` dropped the `InteractionResult.ItemContext` record and
  `InteractionResult.Success.withoutItem`; the full `BlockSetType` component
  roster (fourteen components, seventeen instances, its register/values/codec
  trio) down to what the door needs; the "twenty-four blocks override
  `BlockBehaviour.useItemOn`" count, dropped rather than carried because it
  could not be cheaply re-verified — **worth restoring with a real count**;
  the creative reach modifier, keeping only the server's 1.0 of slack; and the
  alternative door entry points (the redstone path, `DoorBlock.setPlacedBy`,
  the wind-charge path). `block-breaking` dropped the creative-mining branch
  entirely (a fresh START every five ticks, each its own prediction), the
  `ServerPlayerGameMode` anti-desync paths, the `RedStoneOreBlock.attack`
  case — the only left-click that files a ledger entry without breaking
  anything, arguably `prediction-and-acks`' material — the non-player removal
  path through `Level.destroyBlock`, and the note that
  `BlockTags.NEEDS_IRON_TOOL` is a data-generation input never read at
  runtime, which is a good myth-table row for whoever owns tags. The redstone
  split dropped the piston's long tail of special cases: slime reordering,
  the sticky-retract interrupt, `MovingPistonBlock` destruction, and the
  moving hitbox. None of the above is a factual cut; all of it is length, and
  every item is recoverable from the pass-2 `redstone.md` in git.

  **Wording debt.**
  - ~~Three pages used to say some version of "shape updates run on both sides,~~ **Checked, and one had.** `block-interaction`:174-180 was stating all three method bodies over again, verbatim in places. Cut to the door's consequence plus the anchor. The `signal-and-dust` figure node is a mention inside the page's own artefact and stays; the `diodes-and-observers` flowchart draws which channel each block listens on, which is that page's subject.
  *(original entry follows)* 
    neighbour updates are server-only, and here is the exception". That is now
    owned once, by `blocks-and-states`' *The two update channels* section, and
    the other six link to the anchor. **Check in pass 5 that none of them has
    started re-explaining it**; this is the duplication that produced three of
    the part's pass-2 errors.
  - `block-interaction` and `block-breaking` carry an identical four-sentence
    preamble blockquote. That is deliberate (R6) and it should stay identical
    — if either drifts, they stop reading as one lecture in two halves.
  - The reflow around three link edits is untidy: `block-interaction` line
    155, `block-breaking` line 242 and `block-entities` line 96 each have an
    awkward wrap where the `#the-two-update-channels` anchor was added.
    Cosmetic only.
  - `diodes-and-observers` line 52 runs long after
    `HorizontalDirectionalBlock.FACING` replaced the shorter name the
    verifier rejected.
  - The three redstone pages were written by the session rather than by
    drafting agents, so they have had one fewer pair of eyes on their prose
    than the rest of the corpus. They are the pages most likely to be carrying
    the session's own tics.


- **2026-09-02, session E — Part IV.** **The length debt is this session's
  main bequest.** Ten pages, and eight of them landed at 358–417 lines
  against the 260–340 the brief asked for; the two pilots sit at 377 and
  389, so Part IV is now the corpus's fattest part. Every drafter reported
  trimming twice and stopping rather than dropping a verified fact, which is
  the right call under R7 but leaves the bill here. Each names its own
  cheapest cut, and those are the places to start: `chunk-anatomy` — the
  *double indirection* subsection on block-entity tickers (arguably
  `block-entities` material), the *what the client actually receives* answer
  (arguably `what-the-client-is-told`), and the second half of the
  `ImposterProtoChunk` paragraph; `lighting` — the sky-column section, its
  most self-contained; `environment-attributes-and-timelines` — *what
  crosses the wire*, or the *what a type allows* subsection;
  `points-of-interest` — the *who else asks* table; `game-events-and-vibrations`
  — one *Questions players ask* entry. Nothing above is a factual cut; all of
  it is length.

  **Cuts made, all of them names rather than claims.** `chunk-anatomy` drops
  `Block.UpdateFlags` as a named catalogue (the four flags the write path
  actually tests survive; the catalogue belongs to `blocks-and-states`),
  `CarvingMask`'s internal shape, `UpgradeData.EMPTY`, and a dozen field
  names now carried by the sentences that touch them.
  `chunk-generation-pipeline` drops `WorldGenContext`'s six components, the
  `ChunkGenerator` method roll-call (Part XII owns those; `createStructures`
  and `createBiomes` stay because their threading is the point),
  `Blender.of`, `ChunkAccess.isUpgrading` skipping *SPAWN*, and
  `Util.DEFAULT_MAX_THREADS`; it also hands `ServerLevel.updatePOIOnBlockStateChange`'s
  worker-thread posting to `points-of-interest`, **which now owns and
  corrects it**. `lighting` drops the `LightEngine.QueueEntry` constructor
  list, four constants, and the *called by* roll-call, of which only
  `ClientPacketListener.queueLightRemoval` and `ClientLevel.unload` are now
  absent from the corpus. `chunk-storage` drops the thirteen-component
  `SerializableChunkData` inventory, `RecreatingSimpleRegionStorage`, and
  "crosses the network as: nothing" — and **proposes** that the read path's
  null-parse failure branch and `ChunkMap.handleChunkLoadFailure` move to
  `chunk-generation-pipeline`, which pass 5 should either do or drop.
  `scheduled-ticks` drops `ScheduledTick.probe`. `fluids` drops
  `FluidState.AMOUNT_FULL`, `EmptyFluid`, `FluidTags.WATER`/`LAVA`,
  `LiquidBlock.fizz` and the client-packet names.
  `game-events-and-vibrations` drops three private constant *names* (the
  numbers survive in the listener table) and the "there is no *DebugPackets*
  class" aside — **which wants a home in `naming-drift`**.
  `environment-attributes-and-timelines` drops the twenty-one-class *called
  by* roster; its author suggests it becomes a Reference table, and session
  O should rule.

  **Voice debt.** Eight of the ten pages end their opening paragraph on a
  bolded sentence — the same device session C already flagged for Part II,
  now used corpus-wide, and by pass 5 it will be a tic rather than a
  signature. Two hooks are close cousins in shape ("X does not do the thing
  you think, it does Y" — `fluids` and
  `environment-attributes-and-timelines`) and should not sit near each other
  in the lecture order. Three pages now carry a *Questions players ask*
  close (`chunk-anatomy`, `lighting`, `points-of-interest`) plus the pilot's,
  which is four in one part; check whether that reads as a part-level
  convention or a template.

  **`level-data-and-rules`'s Reference framing is provisional.** Session E
  changed only its header, its links and its opening; it still carries a
  `## Responsibility`-era body shape and a "Short, no trace" ancestry.
  Session O owns the reframe.

*(pass-3 and pass-4 sessions append below, newest first: the page, what
was cut or moved, and why)*

- **2026-09-02, session D — Part III.** Five pages, and the register debt
  pass 2 logged against this part is **paid**: the dozen "not X but Y",
  "two, not one" and "and there is no Z" constructions that made Part III
  the corpus's worst offender are gone, restated positively. The three
  bullets opening with "Two …" are gone with the bullet walls — all five
  pages now carry **zero** bulleted lists between them (the budget allows
  three each), which is worth checking is not its own monotony: the
  material became prose, tables and figures, and pass 5 should look for
  paragraphs that would read better as a short list after all.
  *Cuts and moves, per page.*
  **`server-tick`**: the field inventories go (the `ServerTickRateManager`
  sprint bookkeeping — `remainingSprintTicks`, `sprintTickStartTime`,
  `sprintTimeSpend` — and `MinecraftServer.mayHaveDelayedTasks` as a named
  field are no longer listed, only used); `MinecraftServer.spin` and the
  creation of the Server thread move to `starting-a-server`; the crash
  report, `MinecraftServer.constructOrExtractCrashReport`,
  `MinecraftServer.onServerCrash`, the *finally* and `ServerWatchdog` move
  to `how-a-server-dies`, leaving a pointer; `Minecraft.packetProcessor`
  (the client's copy) is left to Part X; `TickRateManager` living in
  `ClientLevel` too is left to `anatomy`, which already says it; the
  *Interfaces* and *Data-driven by* blocks dissolve into the cast row, the
  `tickChildren` table and the questions. The `SampleLogger` /
  `TpsDebugDimensions` paragraph pass 2 flagged as a cut candidate
  **survives**, now inside the bookkeeping section — pass 5 should decide
  again with the page in front of it.
  **`server-level-tick`**: the field inventory and the thirteen-step
  narration go as structures, every fact re-placed; `BlockEventData` and the
  `ServerLevel.customSpawners` / `dragonFight` / `raids` / `sleepStatus`
  fields are no longer named as fields. `ServerChunkCache.onLightUpdate`'s
  off-thread hop is **moved** to `../world/lighting.md`, which already
  narrates it in full (checked). The "Exception ticking world" crash wrapper
  moves to `server-tick`; the `GameRules` package-move note and the
  *DO_DAYLIGHT_CYCLE* / *DO_MOB_SPAWNING* renames move to
  `../world/level-data-and-rules.md`. The pass-2 guard bookkeeping spread
  across six narrated steps is now the flowchart, which is what pass 2
  predicted would let it be cut.
  **`players-and-sessions`**: the `PlayerList` and `ServerPlayer` field
  inventories go. ~~**Three items need a home and have none yet**~~ — **all three settled.
  Checked by session C of pass 5: the `ServerPlayerGameMode` paragraph landed
  on `player-anatomy`:174-179 as the two-sided comparison table, and the
  view-distance packets on `what-the-client-is-told`:381-382, both before
  pass 5 began; `PlayerDataStorage`'s *.dat_old* and corrupt-copy rescue is
  now a passage on `players-and-sessions` itself, where the save file is
  being read, rather than a Reference entry — the cast cell had promised it
  for two passes.** The `ClientboundSetHealthPacket`
  saturation-crossing detail moves to `player-anatomy` by reference; the
  login state machine, the 600-tick login timeout, the auth thread and
  `CommonListenerCookie`'s travel move to `protocol-phases`, linked; the
  permission model is one sentence and a link to `brigadier-and-commands`
  (pass 2 asked session K to check the two had not drifted — they no longer
  can).
  **`starting-a-server`** (was `server-lifecycle`): the field inventories
  go; everything about stopping — `MinecraftServer.halt`, the *finally*, the
  save model, `Util.shutdownExecutors`, the lock release, the three endings,
  the crash-report machinery — moves to `how-a-server-dies`. Only
  `CrashReport.preload` stays, because it happens at boot. The side threads
  became a four-column table (thread · made by · daemon · what it may
  touch), which is the enumerative-beyond-seven rule doing its job.
  *Wording left rough on purpose.* All five pages end their opening
  paragraph on a bolded or dashed sentence — one voice, five times, and the
  same tic session C logged for Part II; a corpus-wide look belongs in pass
  5's voice sweep rather than in any one part. `how-a-server-dies` uses
  *the number* device twice (**Ten seconds**, and the comparison table's
  "differ in one cell") where once is the convention. `server-tick`'s
  *Questions players ask* was trimmed to four questions by moving the
  profiler answer into the bookkeeping section and the worker-crash answer
  into the event-loop section, which is where both belonged; the remaining
  four are the ones a player would actually ask. Part III now has five
  pages where pass 2 had four, so the part is longer, not shorter — the
  length bill for it comes due here.

- **2026-09-02, session A.** `tickets-and-loading`: the *data it owns*
  inventory is gone — `ChunkHolder.queueLevel`, `ChunkMap.unloadQueue`,
  `ChunkMap.serverViewDistance` and `MIN_VIEW_DISTANCE`, `ChunkMap.playerMap`,
  `ChunkMap.getUpdatingChunkIfPresent`, `ServerPlayer.requestedViewDistance`
  / `chunkTrackingView` / `lastSectionPos`, `PlayerList.viewDistance` /
  `simulationDistance`, `ServerChunkCache.CACHE_SIZE` / `lastChunk`,
  `ServerChunkCache.ticketStorage` are no longer named (reason: the cast
  table replaces the inventory; the class index still answers "where");
  the *Called by* list (teleports and `ServerPlayer.doTick` as callers of
  `ChunkMap.move`, `ForceLoadCommand` → `ServerLevel.setChunkForced` at
  `ChunkMap.FORCED_TICKET_LEVEL` loaded synchronously) and the *Calls into*
  list are cut (reason: interfaces survive as one sentence; the forced
  ticket is in the table). `protocol-phases`: the *Crosses the network as*
  packet list is cut in favour of `reference/packets.md`
  (`ClientboundLoginCompressionPacket` is now unnamed — the compression
  switch is described); the *Data-driven by* bullet (server properties,
  resource-pack settings, data packs) is cut; the *Interfaces* callers are
  folded into one sentence. Wording left rough on purpose: both pilots
  still carry em-dash chains in the decision tables' gate cells, and the
  tickets page says "graph" and "tracker" for the same object.


- **2026-09-02, session C — Parts I and II.** Cuts are names, not claims,
  unless marked; the class index still answers "where" for every name here.
  **`anatomy`**: the eleven-row thread table and the situational-threads
  paragraph moved to `reference/threads.md` (already there, verified);
  `Minecraft`'s manager inventory retired (`TextureManager`, `ShaderManager`,
  `ModelManager`, `AtlasManager`, `FontManager`, `SoundManager`,
  `GameRenderer`, `LevelRenderer`, `EntityRenderDispatcher`,
  `BlockEntityRenderDispatcher`, `ParticleEngine`, `MouseHandler`,
  `KeyboardHandler`) and `MinecraftServer`'s (`ServerFunctionManager`,
  `TimerQueue`, `ServerClockManager` — the rest are on `server-tick`); the
  stale-`TickTask`, "Can't keep up!" and flush-bracket invariants cut to a
  link to `server-tick`, which states them; "the server is the game; the
  client is a view of it" and the "this page is the frame" meta-sentence
  cut (the landing page says it); `RconThread`, `QueryThreadGs4`,
  `ManagementServer` dropped from *Where to look*.
  **`what-this-book-skips`**: "Seventy-six pages cover the game" cut (the
  count churns); the four gap lists folded into one table with two prose
  paragraphs for the three entries that needed more than a cell; the four
  "the honest version" / "the detail worth having" tics rephrased.
  **`codecs-nbt-json`**: cut names — `ExtraCodecs.intRange` /
  `nonEmptyList` / `optionalAlwaysPresentFieldOf`, `TagTypes`,
  `NbtIo.readCompressed`, `NbtOps.convertTo`, the three printing visitors
  and the `/data` colouring aside, the five `nbt/visitors` classes,
  `ValueOutput.TypedOutputList`, `StreamEncoder` / `StreamDecoder`,
  `ByteBufCodecs.VAR_INT` / `STRING_UTF8` / `registry` / `holderSet` and
  the `…Trusted` variants, "up to twelve field codecs", `RegionFileVersion`'s
  GZIP/LZ4/none roster; the caller inventory (`PlayerDataStorage`,
  `LevelStorageSource`, `SavedDataStorage`, `SavedDataType`,
  `CommandStorage`, the three NBT command arguments, `Entity.saveWithoutId`
  / `load`); moved to links: the `ComponentSerialization` matrix
  (`text-components`), the `RegistrySynchronization` case
  (`protocol-phases`), `CODEC_WITH_BOUND_COMPONENTS` (`data-components`),
  `RemoteSlot`'s either-or (`containers-and-menus`).
  **`identifiers-and-registries`**: ~~`MappedRegistry.byValue` cut~~
  (restored, session B — the cut is what made the "keyed three ways" count
  wrong); `TagLoader` named only as `TagLoader.buildUpdatedLookups` — carried,
  the tags page names the rest and the registries page cites it.
  **`resource-system`**: `RegistryDataLoader` dropped from its calls-into
  (the registries page owns it) — carried, correct under the ownership rule.
  **`tags`**: nothing cut.
  **`data-components`**: the hashing detail (`HashedStack`,
  `HashedPatchMap`, `RemoteSlot.Synchronized`'s either-or and promotion,
  the creative double guard) moved to `codecs-nbt-json` and
  `containers-and-menus`; three enchanting facts moved *towards* Part VII
  and **not yet present there** — "if the prototype lacks `ENCHANTMENTS`
  the `updateEnchantments` write is skipped", "`clickMenuButton` consumes
  lapis and fires `CriteriaTriggers.ENCHANTED_ITEM`", "`/enchant` is the
  same tail after `Enchantment.canEnchant` and a compatibility check" —
  session H absorbs them into `enchantments`; `RegistryDataCollector`'s
  client-only status no longer stated; `EnchantmentHelper`,
  `ItemEnchantments`, `RemoteSlot`, `HashedStack`, `HashOps` dropped from
  *Where to look*. **`chat-and-signing`**: the `Component` section
  replaced by a pointer paragraph; "new-shaped in 26.2" cut (rule 3).
  Wording left rough on purpose: the seven Part II hooks all end their
  opening paragraph on a bold or dashed sentence — one voice, seven times;
  the comparison and pattern pages carry long table cells that pass 5 may
  want as prose; `what-this-book-skips` still says "the part that
  surprises" where it used to say "the fact worth knowing".

- **2026-09-02, session B — maps.** The four atlas pages and the atlas
  front page are new prose and carry the em-dash chains the corpus is
  prone to; `packages.md`'s part → packages table will duplicate the
  landing pages once all thirteen exist and is a candidate cut then;
  `hierarchy.md`'s *two trees the table shows and the figures do not* is a
  two-sentence section and should either grow a figure or fold into the
  tables' preamble; "the number" device is used once (`biggest.md`) —
  check it reads as intended. Nothing was cut from the old maps: the
  tables are all still there under the figures, at the same URLs.

- **2026-09-03, session G — Part VI Entities.** *Cuts, all of them moves or
  logged losses.*
  **`entity-anatomy`**: the seven-group field inventory and the "smaller
  state families" paragraph (fire, freezing, fluids, portals, naming,
  item-component views) go — the names survive only where the story touches
  them, mostly as the contents of `Entity.baseTick`; the hand-drawn class
  tree is replaced by the atlas's generated SVG, taking the eighteen-name
  list of non-living direct subclasses with it; `Entity.MAX_ENTITY_TAG_COUNT`
  versus the literal 1024 (true, earns nothing on a map page); the
  `Entity.RemovalReason` four-way flag breakdown, **moved to
  `entity-lifecycle`**; `Mob.serverAiStep` being final and alternating on
  `tickCount + id`, **moved to `ai-goals-and-brains`**; `Marker.tick` being
  genuinely empty. The subpackage table stayed and its counts were corrected
  — the old rows summed to 639 of a stated 716.
  **`entity-lifecycle`**: the nineteen-constant `EntitySpawnReason` list
  (four survive, the rest want Reference — logged in pass3.md); the
  `SpawnPlacementTypes` list, folded into a cast row; the game-rule and tag
  roster from *Data-driven by*; and — the largest deliberate cut — the
  **Nether-fortress hard-coded spawn list and `Structure.spawnOverrides`**,
  which are verified true and are now stated **nowhere in the corpus**.
  Session M or O should take them.
  **`synched-entity-data`**: the 43-constant serializer bullet (74 lines) to
  the generated Reference page, leaving three named in prose; the
  `defineId`/`defineSynchedData`/setter roster; the thirty-five-overrider
  list, cut to three examples; `ServerEntity.Synchronizer` compressed to one
  table cell.
  **`attributes`**: the forty-constant catalogue (five themed bullets, 34
  lines) to the generated Reference page, with the count, the clamp rule,
  the eight non-syncable names and the handful of numbers the argument uses
  kept in prose. `Attributes.DEFAULT_ATTACK_SPEED` cut outright because the
  claim about it was false.
  **`movement-and-collision`**: the position-and-teleport family
  (`Entity.absSnapTo`, `Entity.snapTo`, `Entity.setOldPosAndRot`, the
  ±3.0000512E7 clamp, `Entity.setBoundingBox`'s public callers,
  `Entity.getKnownMovement`, `Entity.flyDist`) — these are
  `entity-anatomy`'s or `authority`'s and are currently on **neither**;
  half the outbound packet list and the whole inbound one, which
  `input-to-movement` owns; the data-driven tag inventory.
  **`ai-goals-and-brains`**: the behaviour-package roster cut to eight named
  classes plus a count; `VillagerType`.
  **`damage-and-death`**: the exhaustive `DamageTypes` key list and the
  fifteen-name `DamageTypeTags` list, replaced by the counts (51 and 35)
  with each tag named where it acts — both are Reference material and
  **neither Reference page exists yet**; `DamageSources` pre-building the 25
  entity-less sources; and the *Interfaces* inventory as a category, taking
  with it `Entity.thunderHit`, `LivingEntity.kill`, `/kill` and `/damage` as
  named callers, `CriteriaTriggers` and `Stats` as consumers,
  `MobEffectInstance.onMobHurt`, `ItemStack.hurtAndBreak`,
  `DataComponents.DAMAGE_RESISTANT`, and the two combat-status packets —
  all of which are now **nowhere**. The one substantive cut that needs a
  home is the **fall-attribution threshold** (`CombatTracker` credits a fall
  only when the best one exceeds five, and credits the *previous* entry when
  the fall was not the first — the source of *was doomed to fall by*): it is
  death-*message* machinery rather than damage, and wants a `CombatTracker`
  or death-message Reference page. Also found and deliberately **not** added:
  world-border damage is player-only.
  `damage-and-death` is 395 lines against the 240–390 target, and its
  drafter's verdict is that getting under 390 now costs a claim rather than
  words.
  *Wording debt.* `ai-goals-and-brains` is 420 lines against a 240–390
  target — the comparison table, the `Brain.tick` flowchart and seven
  difference sections cost more than the dissolved bullet walls saved; its
  own drafter names the *Questions players ask* section as the cheapest
  honest cut. **Six** of the nine pages ended on a *Questions players ask*
  section, which is one device used six times in one part and is exactly
  the "second uniformity" risk the charter names. The session renamed three
  of them to headings that say what the section says — *Three things about
  the id*, *What the four predicates explain*, *Why mobs look stupid* —
  leaving three; the question-and-answer form underneath is unchanged, and
  pass 5 should decide whether the form itself wants varying. Session P
  should check the device's distribution across all thirteen parts. The part's hooks all land on a bold or em-dashed final sentence,
  the same tic session C logged for Part II.

- **2026-09-03, session H — Part VII Items and inventories.** Eight pages,
  318–391 lines. **Nothing was cut except by moving it**, but a lot of
  *names* left the pages when the field inventories went, and this is the
  list, because the class index is now their only home.
  **`containers-and-menus`**: the `Container` interface roll-call
  (`Container.getContainerSize`, `Container.removeItem`,
  `Container.startOpen` / `stopOpen`, `ContainerUser`), the guarded
  mutations (`Slot.safeInsert`, `Slot.safeTake`, `Slot.tryRemove`,
  `Slot.safeClone`, `Slot.onQuickCraft`, `Slot.isFake`), the `Slot`
  subclasses (`ArmorSlot`, `FurnaceFuelSlot`, `NonInteractiveResultSlot`,
  `ShulkerBoxSlot`), the `Inventory` slot constants, the
  `AbstractContainerMenu` field list and
  `AbstractContainerScreen.checkHotbarKeyPressed`.
  **`recipes`**: the `Recipe.CommonInfo` / `Recipe.BookInfo` codec-fragment
  paragraph, `NormalCraftingRecipe`'s memoisation, the seven `RecipeType`
  constants enumerated, the `RecipeInput` three shapes
  (`SingleRecipeInput`, `SmithingRecipeInput`), the
  `Registries.RECIPE`-is-a-key-only note, the eleven `SlotDisplay` variants
  and the five `RecipeDisplay` class names (both now counts plus the
  exotic ones), and two recipe-book packets
  (`ServerboundRecipeBookSeenRecipePacket`,
  `ServerboundRecipeBookChangeSettingsPacket`).
  **`enchantments`**: ten of the fifteen entity-effect class names,
  `Enchantment.getFullname`. **`loot-tables`**: `LootDataType`'s three
  constants enumerated, `ContainerEntity.unpackChestVehicleLootTable` and
  the minecart parallel, `LootCommand` and `ItemCommands.applyModifier`
  (all three moved with the caller table to `contexts-and-predicates`), and
  `Registries.LOOT_TABLE` — now only implied through
  `ReloadableServerRegistries`, which pass 5 may want named once.
  ~~**`using-an-item`** deliberately left the full `Item.getUseDuration`
  override roster to nobody.~~ **Done, session G (pass 5)**: written as a
  sentence on `using-an-item`, with the base method's own three-way answer in
  front of it — a Reference row was declined because eight overrides and one
  default is not a catalogue. `Registries.LOOT_TABLE` in the same entry was
  found already named on `contexts-and-predicates`:312, and the
  `LootDataType`, `ContainerEntity` and command-class items with it: the whole
  `loot-tables` half of this entry is **overtaken**.

  **Length.** Every page is over the 200–320 brief: 318, 324, 332, 344,
  346, 358, 389, 391. Five agents reported trimming twice and stopping
  rather than cutting evidence. Part VII is now the longest part per page
  in the corpus and is where pass 5's cutting should start.

  **Wording.** `enchanting`'s comparison table and
  `contexts-and-predicates`' caller table both carry long cells that want
  to be prose. `using-an-item`'s two sequence diagrams are deliberately
  isomorphic, which is the right call for the comparison but makes the
  page's second half read as a repeat — worth a voice pass. Only
  `loot-tables` reached for *Questions players ask*, so session G's
  uniformity risk did not recur here; the eight section-heading sets are
  genuinely different from one another, which is the test.

- **Session I (Part VIII), 2026-09-03.** **Length**: 316, 174, 410, 285, 231,
  250, 176 lines plus a 115-line landing page — six of the seven inside or
  near the 200–320 brief, which is the first time in pass 3, and the splits
  are why. The exception is **`input-to-movement` at 410**, which was not
  split and now carries the longest single section in the part (the server
  half of the trace); it is the part's first candidate if pass 5 wants a cut
  or a split.
  **Cuts and losses, recorded.** The old `player-anatomy` bullet inventory of
  `Player`'s fields became a three-column table; nothing was dropped, but the
  table's middle column is dense and is a candidate for prose or for the class
  index. `hunger-xp-and-effects`' opening headline about `GameRules`' package
  (`world/level/gamerules`, typed `GameRule` lookups) survives only as a
  clause in `hunger-and-experience`; it was a Reference fact wearing a hook's
  clothes. Two `the-sword-swing` sentences about `DataComponents.MINIMUM_ATTACK_CHARGE`
  and `DataComponents.DAMAGE_TYPE` as *the rest of what makes an item a
  weapon* were absorbed into `the-spear`'s component table, so the sword page
  no longer names `MINIMUM_ATTACK_CHARGE` at all.
  **Wording.** `input-to-movement` is the page most obviously mid-conversion:
  its two data subsections are still a bullet wall under a renamed heading,
  and the *what it calls, and what crosses the wire* section is the old
  Interfaces list with a new title. It is the first place a pass-5 voice pass
  should go in this part. `the-spear` uses *stab* and *charge* as the two
  path names throughout; if pass 6 disagrees with those words, they are the
  page's whole vocabulary and change everywhere at once. Three pages now open
  with the second person (*you press W*, *you open your own inventory*, *you
  drink a potion*), which reads well here and is worth a corpus-wide decision
  rather than a per-part accident.

- ~~**2026-09-03, out of band — the licence footer says it twice on one page.**
  `site-footer.js` puts the disclaimer and the CC BY-SA line on every page,
  and the introduction now also closes on *Unofficial, and free to reuse*,
  which says the same two things in prose. Everywhere else the footer is the
  only statement and reads as small print; on `introduction` alone it is a
  restatement two inches below the section it restates. Cheapest fix if pass 5
  agrees it grates: have the footer skip the introduction (it is the one page
  guaranteed to carry the prose version), rather than cutting the prose —
  the prose is what reaches an agent through `llms-full.txt`, which the JS
  footer never does. Not urgent; nobody has complained, and duplication in
  favour of the licence being visible is the right way round to err.~~
  **Ruled out** (pass 5, session A), for the entry's own reason: the JS
  footer never reaches `llms-full.txt` and the prose does, so the two copies
  are not the same copy, and erring towards the licence being visible is
  right. [kind=book]

- **2026-09-03, pass 3 session J — what Part IX's reshape cut.** Logged per
  R7: nothing left a page except by moving or by this entry.
  **From `the-connection`** (550 → 442 lines), all of it enumeration the
  budgets no longer allow and none of it load-bearing: the sixteen
  `HandlerNames` constants named one by one (the class survives, and so does
  the fact that nothing references some of them); the packet-rate smoothing
  constant and its lerp fraction; `Connection.intendedProfileId` with its
  setter and the observation that `ServerConnectionListener.acceptChannel` is
  its only assignment and is itself uncalled; the method-by-method tour of
  `PacketListener`; `ServerConnectionListener.getSessionId`, its two stop
  methods and the *Open to LAN* note; `ServerConnectionListener.LatencySimulator`;
  the five `TickablePacketListener` implementors listed by name (the
  interface's role survives in the cast); and five `Connection` accessors
  named as names. If pass 6 misses any of these, the class index still has
  them and `reference/packets.md` is the catalogue.

- **2026-09-03, session J, the rest of Part IX's cuts and its wording debt.**
  From `what-the-client-is-told`, replaced by naming only what the story
  touches: the `ServerEntity` field list (`lastSentYRot`, `lastSentXRot`,
  `lastSentYHeadRot`, `lastPassengers`, `wasRiding`, `wasOnGround`) and the
  `PlayerChunkSender` field list. Two facts were cut as *duplicates*, not
  losses — the tick-long flush suspension (owned by `the-connection`) and the
  `ChunkMap.MIN_VIEW_DISTANCE` clamp (owned by `tickets-and-loading`'s send
  table) — and both now link instead. The `ClientboundTeleportEntityPacket`
  invariant was not cut: it moved into the page's *for a 1.21-era reader*
  blockquote.
  **Wording debt.** Three of the four rewritten pages open in the second
  person (*you swing*, *you stop the message on its way out*, *someone says
  hello*), which continues the drift session I flagged in Part VIII — the
  corpus-wide decision on the second person is now overdue and would touch
  three parts at once. `chat-and-signing` uses *message*, *chain* and
  *connection* as the names of its three failure outcomes throughout, in the
  prose, the flowchart and the eighteen-row table; if pass 6 disagrees with
  those three words they change everywhere at once, exactly as
  `the-spear`'s *stab* and *charge* do. And `the-connection` and
  `packets-and-stream-codecs` both call the codec table *the phase's one
  codec*, which is precise but is the sort of phrase a viewer hears as a
  singular file rather than a composed dispatcher.

- **2026-09-03, session K, Part X's cuts and its wording debt.**
  **Cuts, all of them moves rather than losses.** `hud`'s twenty-eight-row
  element gate table, which pass 2 had compressed to a paragraph of prose,
  is now `src/reference/hud-elements.md` and the page links to it — the page
  keeps only the two-block *shape* as a flowchart. `the-client-loop` lost its
  *data it owns* field inventory (the timing fields, the profiler apparatus,
  the gizmo collectors) and its *interfaces* list; every field the story
  touches is still named in the sentence that touches it, and the rest is in
  the class index. `the-client-level` lost the same kind of inventory, and
  `prediction-and-acks` lost its enumeration of
  `BlockStatePredictionHandler`'s eight public members as a list — three are
  still named in *Where to look*. Nothing factual was dropped except one
  stale framing sentence in `sound`, which called the sound system "the first
  system after Anatomy"; the lecture order it referred to no longer exists.
  **Wording debt.**
  - **The formula sweep is now overdue and Part X is where it is worst.**
    Session H recorded that three Part X pages opened with "The headline for
    a 1.21-era reader" and four with "The one sentence a player would
    recognise"; session I found Part XI eight for eight. This session
    removed both formulas from all twelve Part X pages — the headline
    material became the *for a 1.21-era reader* blockquote at the foot of
    each page, and the player-recognises sentence was folded into the
    opening paragraph or the verified line. **The formulas now survive
    nowhere in Part X and everywhere in Parts XI to XIII.** Sessions L to N
    should do the same, or pass 5 will be reconciling three different house
    styles.
  - **The *questions players ask* device is now doing a lot of work.** Six of
    the twelve pages use it, because it is the honest home for what used to
    be a bullet wall of invariants. That is one page in two, which is the
    same trap the old seven-heading template fell into. Pass 5 should check
    whether it reads as a device or as a section every page must have — and
    note that on three pages (`the-gui-render-tree`, `text-and-fonts`,
    `sound-engine`) the questions are a reader's rather than a player's, and
    the heading says so, which may be a distinction without a difference.
  - **Second person again.** `input-and-keybinds`, `hud`,
    `what-makes-a-sound` and `the-gui-render-tree` all open in the second
    person (*hold the key*, *press F1*, *you break a block*, *a chest full of
    the same item*). Sessions I and J both flagged the drift; it is now four
    parts wide and the corpus-wide decision cannot wait for pass 6.
  - **`the-gui-render-tree`'s title is still the weakest in the part**
    (session H's note, unresolved). It is really *how the UI is recorded and
    drawn*, and the tree is the mechanism rather than the subject. Not
    renamed this session because a rename costs a redirect and the page's own
    figure now makes the tree the point; pass 5 or pass 6 should settle it.
  - **"Record" and "extract" are used interchangeably across four pages** —
    `gui-and-screens`, `the-gui-render-tree`, `text-and-fonts` and `hud` —
    because the methods are all named *extract* and the concept reads better
    as *record*. The glossary has *extract*. One of the two should win.

## Session N — Part XIII Commands and data packs *(2026-09-03)*

**Cuts, with reasons.** Nine pages from five, and the reshapes dropped
material rather than moving it in these places. None of it is wrong; all of
it lost a fight for space against the page's own story.

- `brigadier-and-commands` lost: `CommandSource` as a named object (the
  output end alone — `CommandSource.NULL`, `CommandSource.acceptsSuccess`,
  `CommandSource.shouldInformAdmins` — and the observation that a command
  block, RCON and the console differ *only* there);
  `Commands.CommandSelection` gating which commands exist at all on an
  integrated versus a dedicated server; `CommandSourceStack`'s fourteen-field
  inventory; the roll-call of the resource-argument family
  (`ResourceArgument`, `ResourceKeyArgument`, `ResourceOrIdArgument`,
  `ResourceOrTagArgument`, `ResourceSelectorArgument` and which of them takes
  a glob); and the note that `IdentifierArgument` is the class a 1.21 reader
  knows under another name, which `reference/naming-drift.md` owns anyway.
  The `CommandSource` row is the one worth restoring if the page ever has
  room — it is the whole answer to "why does a command block not spam chat".
- `advancements` lost: the two `Advancement.validate` methods (a private
  static one the codec runs, which cross-checks requirements against criteria
  and **fails the load**, and a public one that walks each trigger instance
  through a `ProblemReporter` and only *warns*); `AdvancementTree.remove` as
  the recursive counterpart the client uses for the packet's removed ids;
  `ServerAdvancementManager` as a `SimpleJsonResourceReloadListener` over
  `Registries.ADVANCEMENT`, with the JSON parse off-thread and the tree build
  and layout on the reload's main-thread executor; `AdvancementRewards.grant`
  rolling its tables in the `LootContextParamSets.ADVANCEMENT_REWARD`
  context; `DisplayInfo`'s field inventory; and the two call-site counts
  ("seventy-nine gameplay sites across forty-nine files",
  "`AdvancementCommands` is 312 lines"). The reload-listener sentence is the
  loss that matters — the page now says the layout runs on the server without
  saying *when*.
- `the-execution-engine` lost `ExecutionControl` and the
  `EntryAction` / `UnboundEntryAction` pair as named cast rows; both are now
  only implied by `CommandQueueEntry`'s row.
- `scoreboard-and-data` lost: `PlayerScores` (package-private, and the
  observation that `Scoreboard.resetSinglePlayerScore` deletes the whole row
  so the outer map never accumulates empties); `TeamColor`'s sixteen values
  and the unrelated second `TeamColor` in `client/color/item`;
  `DisplaySlot`'s nineteen enumerated; `ScoreHolder.fromGameProfile`; and the
  command-class sizes (`ScoreboardCommand` at 620 lines is the fourth-largest
  command class in the game, which was a nice number).
- `dialogs` and `game-tests` lost the individual names of six packets
  (`ClientboundClearDialogPacket` survives; `ClientboundTestInstanceBlockStatus`,
  `ServerboundSetTestBlockPacket` and `ServerboundTestInstanceBlockActionPacket`
  are now described rather than named). `reference/packets.md` has them.

**Wording debt.**

- **Second person is now five parts wide and past arguing about.** Every one
  of this part's eight content pages opens in it — *type a slash*, *op
  yourself to four*, *write a data pack*, *put a `$`-prefixed line*, *mine a
  stone block*, *look at the sidebar*, *you click a server*, *run
  `/test runall`*. Sessions I, J and K all flagged the drift as a question;
  session N used it deliberately on every page because the shape of the
  opening paragraph the template asks for (*start inside the scenario*)
  pulls hard towards it. Pass 5 should ratify it or reverse it corpus-wide,
  not page by page.
- **The *questions players ask* device is on three more pages** —
  `advancements`, `scoreboard-and-data`, and `the-execution-engine` where it
  is called *questions a data-pack author asks*. That is session K's warning
  coming true: the device is becoming the standard home for what used to be
  the invariant wall, and a corpus where half the pages have one has just
  re-invented the seven-heading template with better headings. Count them in
  pass 5 and cap it.
- **"The one sentence a player would recognise" is gone from all five old
  pages** and was not replaced by anything with a fixed position — the
  recognisable thing is now inside the opening paragraph where it belongs.
  Worth checking the earlier parts still do the same.
- `the-execution-engine` and `functions-and-macros` both explain
  `ContinuationTask.schedule`. The engine page owns the arithmetic and the
  functions page owns the consequence ("a hundred-line function and a
  hundred-player fork are the same shape"), which is one sentence of overlap
  and deliberate — but it is exactly the kind of duplication pass 5 hunts.
- `permissions` and `brigadier-and-commands` both describe the command-tree
  packet, deliberately from two sides (shape versus gating). Read them
  together once for a seam that reads as a repetition.

## Session O — Reference *(2026-09-03)*

- `level-data-and-rules` was reshaped bullet-for-paragraph, so its
  paragraphs are still inventories in prose clothing (the `PrimaryLevelData`
  field list, the `DimensionType` record). A reference page may keep them;
  a polish pass should decide whether the two longest become tables.
- `math-and-primitives`' *What trips people up* is nine bold-led paragraphs
  where the list was; the ninth (`BlockUtil` is in `util`, not `core`) is a
  naming-drift row wearing a surprise's clothes and could move to that
  page.
- `naming-drift` keeps its second-person "the name in your head" voice,
  which is now the only page in Reference that talks to the reader; keep or
  level in the voice sweep.
- `reference/README.md`'s table has a *parts* column written by hand from
  the landing pages; if a tool ever writes it, the column goes generated.
- The glossary's owner links are one page each except *Component*,
  *Level*, *Render state*, *Tick*, *Quart* and *Submit node*, which point at
  two; a polish rule should say whether two is allowed.

## Session P — The lecture order and the close *(2026-09-03)*

The charter asked session P to check the distribution of page shapes ("if
half the corpus chose the trace, the menu failed") and the *Questions
players ask* device's spread (sessions J and M each flagged it in their
part). Two agents classified all ninety-eight system pages by the menu's
rubric — primary shape from the spine, secondary from the borrowed section,
first figure's type, and whether the page ends on a questions section — and
the session read their evidence lines against the pages' headings.

**The menu held.** Primary shapes over ninety-eight pages: **trace 31 ·
vocabulary 25 · pipeline 17 · comparison 10 · policy 7 · pattern 6 · state
machine 2.** The trace is a plurality at just under a third, not the
majority the risk named; the vocabulary page is the surprise at a quarter,
and three of those (`tags`, `signal-and-dust`, `synched-entity-data`) lead
with a figure that belongs to a different shape than their spine. The state
machine is the least-used shape, and the two that exist are both in Part
IX/X (`protocol-phases`, `prediction-and-acks`); Parts I–VII have none as a
primary although three of their pages carry a `stateDiagram` as a secondary
figure (`points-of-interest`, `entity-lifecycle`, `tickets-and-loading`).
Pass 5 should ask, page by page, whether a secondary state diagram is the
page's true picture.

**The closing device did not hold.** Sixty-three of ninety-eight pages end
on a questions section (sixty *Questions players ask* verbatim, three
*Questions a reader asks*, one *Questions the pattern raises*, one
*Questions a data-pack author asks*) and four more carry one that is not
last (`what-the-client-is-told`, `the-client-level`, `advancements`,
`the-execution-engine`). By part: I 1/2 · II 6/7 · III 2/5 · IV 10/10 ·
V 7/7 · VI 3/9 · VII 2/8 · VIII 7/7 · IX 4/5 · X 8/12 · XI 6/10 · XII 8/8
· XIII 3/8. Parts IV, V, VIII and XII use it on every page. This is a
*device* become a *slot*, exactly the second-uniformity risk the charter
named, and it happened for the reason session J gave: the section is the
honest home for what used to be the invariants wall. **Rule of thumb for
pass 5: at most half the pages in a part end on it**, and on the others
the same question-and-answer material either dissolves into the section
where the answer happens (session G's precedent — *Three things about the
id*, *Why mobs look stupid*) or takes a heading that says what the section
says.

**Seven pairs of pages share a skeleton**, which the charter says means
neither is done. Within one part: `server-tick` / `server-level-tick`
(deliberate mirroring — the outer and inner loop — but the tables of
contents are hard to tell apart); `starting-a-server` / `how-a-server-dies`
(one skeleton run forwards and backwards); `chunk-generation-pipeline` /
`chunk-storage` / `scheduled-ticks` (three pipelines: lead flowchart,
per-stage sections, a named trace late, questions); `block-breaking` /
`block-interaction` (both are applications of the same ledger and the
shape does not distinguish them); `attributes` / `synched-entity-data`;
`enchanting` / `using-an-item`; `biomes` / `features-and-placement` /
`jigsaw-and-templates` (Part XII: cast → *The trace: X* → two or three
detail sections → questions → where to look, only the nouns change);
`the-spear` / `the-sword-swing`; `hud` / `options` / `input-and-keybinds` /
`the-gui-render-tree`; `blaze3d` / `section-meshing` / `the-frame` /
`the-window`. Across parts: `data-components` / `text-components` /
`items-and-stacks` (one skeleton three times), and `the-client-loop` /
`the-frame` (one turn of a loop, zones named, what falls off the end — kept
apart mainly by one being a flowchart and the other a sequence). Pass 5
varies one of each pair; the shape need not change, the skeleton must.

**The literal heading `## The trace: …` is on twelve pages** in four
parts (VIII ×4, XII ×4, XIII ×4 — `input-to-movement`, `status-effects`,
`the-sword-swing`, `the-two-phase-tick`, `biomes`,
`features-and-placement`, `hand-built-structures`, `jigsaw-and-templates`,
`advancements`, `dialogs`, `game-tests`, `scoreboard-and-data`), which is
a template slot's name and breaks the *headings say what the section
says* rule from `TEMPLATE.md`. Each wants the scenario as its heading.

**Two structural outliers**, for the same sweep: `functions-and-macros`
has no cast table (it opens on *The pipeline*), and `hand-built-structures`
buries its cast inside *The idea* — both differ from every other page in
their part, and either is fine if it is deliberate.

**Wording debt from the four session-P pages.** All four were drafted by
Opus agents against the shared brief and accepted after the session
re-derived their sharpest claims; none was cut. `block-entity-rendering`
(332 lines) is a comparison whose three-column table is the figure and
whose *why* column on the view-distance table is editorial — pass 5 should
decide whether an inferred reason belongs in a table cell; its
1.21-reader blockquote is eleven lines, the longest in the corpus.
`entity-selectors` (313 lines) ends on *Questions a command author asks*,
the fourth spelling of the device; its twenty-one-row option table is
under budget only because three rows fold *x, y, z* and *dx, dy, dz* and
the rotations together. `blending` (346 lines, the longest of the four and
over the brief) ends on *Questions players ask* — Part XII is now 9 of 10
on the device — and its opening paragraph carries two numbers ("roughly a
hundred blocks", "a hundred and ninety-three") before the reader knows what
a column is; consider moving the 193 down to the *Two maps* paragraph
where it is explained. `creating-a-world` (300 lines) has a
three-column comparison table whose *Re-Create* column is the argument;
the paragraph after the sequence diagram ("Three details in that order are
worth stopping on") is a list in prose clothing and could be three
bold-led paragraphs. All four use the *For a 1.21-era reader* blockquote;
none uses the myth table; three carry a *Questions* closer, so the
session's own pages score 3 of 4 on the device it just flagged.

## From pass-4 session H — Part VIII The player *(2026-09-04)*

**Openings rewritten around a corrected fact — re-read for voice:**

- `status-effects` — the hook was "The client never runs a status effect …
  and that is all", which is false of the movement consequences. It is now
  "The client never runs a `MobEffect` hook", followed by three named
  unguarded reads (`getJumpBoostPower`, the slow-falling gravity clamp,
  levitation in `travel`). The paragraph is longer and the "and that is all"
  cadence is gone; find a shorter shape that keeps the distinction.
- `player-anatomy` — the *whose game mode arrives late* question was
  inverted and is now roughly twice as long, because the true version has to
  say why the other player's window cannot be observed before it can say the
  window is yours. It reads as an argument rather than an answer.
- `the-two-phase-tick` — the Netty-threads paragraph grew from an absolute
  plus a throwaway ("a handful that touch nothing") to a count plus an
  exception plus the chat mechanism. Correct, but it is now the longest
  paragraph in a short section.
- `the-spear` — the *different windows* payoff sentence was replaced by its
  mirror image with the wooden spear's 5/10/15 as illustration. Check the
  numbers earn the extra clause.

**Structural findings (not acted on):**

- `status-effects` names `LivingEntity.effectsDirty` and never says what
  reads it. The consumer is `updateDirtyEffects` ← `updateDataBeforeSync` ←
  `ServerEntity`, i.e. the server's entity-sync pass — which is the actual
  mechanism behind the page's own "swirls and no numbers" answer. Naming a
  field with no reader is the pattern; either say what reads it or drop it.
- `status-effects` lists `MobEffectCategory` in *Where to look* and never
  explains it, though it is why the HUD splits icons into two rows.
- `status-effects` — `MobEffectInstance.compareTo` orders the HUD icons
  reversed and the inventory list un-reversed, so the two surfaces list
  effects in opposite orders. One clause, and it is the kind of thing a
  player notices.
- `the-sword-swing` — `LivingEntity.getSecondsToDisableBlocking` is
  presented as an unconditional read-back; it returns the `Weapon` value
  only when the weapon is also the attacker's *active* item.
- `the-spear` — the component table is headed "every component that makes
  one" (now softened to "the combat components"); the durability three,
  `REPAIRABLE` and `ENCHANTABLE` are still absent. Either the table is
  complete or the header says which subset it is.
- `input-to-movement` — "floating" is used without ever defining the
  condition `clientIsFloating` records, and the jump-inference paragraph sits
  before the field it depends on is introduced.
- `player-anatomy` — the page says `Avatar` "exists for the renderer", but
  `Avatar` is a server class whose other content is the shared player hitbox;
  the renderer is one consumer, not the reason.

## From pass-4 session I (Part IX Networking), 2026-09-04

Wording debt from fixes made in place, and structural findings not acted on.

- `networking/README.md` — the opening's four player-visible failures now
  ends on "a grey bar down its left edge", which is true and duller than the
  red line it replaces. The vivid true version is the *sender's* side —
  `handleMessageDecodeFailure` sends the reason back in red — but that is a
  different sentence about a different player. Re-read the paragraph whole.
- `networking/README.md` — "one wire and three passengers" is still the
  part's shape sentence, and the page contradicts it twenty lines later by
  saying *protocol phases* **is** the wire rather than a passenger. Pass 4
  softened the first sentence rather than choosing; the shape needs deciding.
- `networking/README.md` — the traffic-volume clause added to the *shape*
  section is a fact the section did not previously carry, and reads like a
  footnote. It may belong in *what the client is told* instead.
- `the-connection.md` — the `HandlerNames` paragraph existed to deliver "a
  complete and correct index that no code reads". The index turned out to be
  incomplete, so the paragraph now delivers "an index that has already
  drifted", which is a different and slightly weaker point occupying the same
  space. Consider cutting it to one clause.
- `the-connection.md` — the kick answer is now four sentences where the
  question deserves two. The mechanism took three of them.
- `packets-and-stream-codecs.md` — the "three shapes of packet class"
  paragraph now names all three, and the third (the `StreamCodec.unit`
  singleton) is introduced twice on the page, here and in the bundle section.
  Pick one home.
- `packets-and-stream-codecs.md` — the JSON exception is now a four-line
  aside inside a paragraph about the NBT bridge. It is a good fact and it is
  in the wrong shape; it may want to be its own short paragraph.
- `protocol-phases.md` — "Eight, not four: every phase but handshaking
  declares one per direction" is a correction written as prose. Pass 5 should
  fold the number into the sentence and drop the correction voice.
- `what-the-client-is-told.md` — "Four feeds ignore gate 3" now carries a
  second sentence walking back the scope, and the section heading still says
  *What goes out around the gates*. Heading and content disagree in emphasis.
- `chat-and-signing.md` — the unsigned-`Component` paragraph grew by four
  lines to hold the `MessageArgument` finding, which is the best fact on the
  page and is buried in a paragraph about a field. It may deserve promotion.

Structural findings, not acted on:

- `reference/threads.md` — the never-hop section's population is stated as
  "`ClientPacketListener`", a class, when the honest population is "the
  handlers a client play listener runs". Pass 4 fixed the count and left the
  framing; a Reference section whose population is a class file rather than a
  runtime object will drift again the next time a handler moves up or down
  the hierarchy.
- `networking/README.md` figure — arrows 3 and 4 (`PP → WCT`, `PP → CS`)
  assert a dependency neither target page uses. Pass 4 corrected the prose
  that made the same claim and left the arrows, because the figure is the
  part's watch order rather than a prerequisite graph. If the shape sentence
  above is redecided, the arrows go with it.

### Part XIII, after session M of pass 4 *(2026-09-05)*

Wording debt, all of it created by a fact fix:

- `brigadier-and-commands.md` — the **hook and the whole round-trip section
  were rewritten**, because the page's central claim ("the round trip is not
  the fallback, it is the default") was backwards and its verified-line
  scenario asks the server nothing. The replacement carries three numbers —
  359, 64, 59 — where the old one carried two, and the "why they feel like
  all of them" turn is doing a lot of work in one clause. Pass 5 should read
  the opening and the *A node that asks for suggestions by hand* section
  together and decide whether the argument now takes one paragraph too many.
- `entity-selectors.md` — the **opening scenario was replaced** (a command
  block, because a player typing `/tp @p` always selects themselves) and now
  carries a parenthetical explaining why the obvious version does not work.
  The parenthetical is a correction in the voice of a correction; pass 5
  should either fold it into the paragraph or cut it.
- `entity-selectors.md` — the orphaned "**Four** —" paragraph is now a
  four-line "the query plan is written by eight of the twenty-one names"
  paragraph. It is accurate and it is the third place on the page that
  enumerates the box options. Pass 5 should decide which of the three keeps
  the enumeration.
- `functions-and-macros.md` / `permissions.md` — the union paragraph on both
  pages grew to hold the level-based-versus-not distinction, which is a real
  and necessary qualifier and reads like a footnote promoted into the body.
  The fact belongs on `permissions`; `functions-and-macros` may be able to
  cite it in a clause.
- `permissions.md` — *Asking a question the client cannot answer* now says
  three things the section did not previously have to say (the sign is not on
  this path; `NO_ISSUES` sends silently; the client checks permissions in
  several other places). The section's own punchline — that the client can
  tell "no permission" from "typo" — is now the fourth idea in it.
- `scoreboard-and-data.md` — the "one thing this corpus cannot settle"
  paragraph became an answer, so a paragraph that existed to mark a limit is
  now a paragraph of fact sitting where a caveat used to close a section.
  Check it still belongs at the end.
- `game-tests.md` — the client-writes sentence now ends on a list of four
  serverbound packets that belong to other pages. True, and long. Pass 5
  should consider cutting it back to the narrow claim.
- `commands/README.md` — the *before you start* server-tick entry is now the
  longest of the five and names three classes, because the short version was
  wrong about which phase. It may be shortenable now that it is right.

Structural findings, not acted on:

- `entity-selectors.md` — the page is one of the longest in the part and its
  *Resolve* section carries five bolded claims in a row, three of which are
  about cost rather than about the trace. The page's shape is a pipeline with
  a policy figure; the cost material may want to be a table.
- `commands/README.md` — the part's size sentence now needs nine package
  names to be reproducible and gives none, which is what let a wrong pair
  stand through two passes. Every other landing page has the same shape. A
  standing fix would be for the atlas to generate the per-part totals rather
  than each landing page hand-counting them — that is a tooling change, and
  it belongs to whoever revisits `map_source.py`.

---

## From pass 5, session F (Part VI · Entities), 2026-09-05

*What the reading raised and this session did not act on, tagged by the pass
that takes it. Everything session F did act on is struck above or logged in
[pass9.md](pass9.md).*

**Routed to a later part's session.**

- **Session I (IX) — the send gate is explained twice and neither page links
  the other.** `synched-entity-data`:246-294 (*The gate that holds a packet
  back*, with its own flowchart) and
  `what-the-client-is-told`:146-225 (gates 2 and 3) are the same mechanism.
  Under the routing rule the later part resolves it, so session I decides;
  session F added the missing forward link and left the section standing. Four
  things the Part VI copy has that the owner lacks, and they are moves rather
  than cuts: that the interval gate covers the **data** flush as well as the
  position block (so shearing a sheep sends that sheep's position delta too);
  the `ItemFrame` bypass being the only path to the flush that skips the
  interval test; `ServerEntity.handleMinecartPosRot` calling it from *inside*
  the gate; and `Entity.updateDataBeforeSync`, the hook that opens
  `ServerEntity.sendChanges` ahead of the gate and lets `LivingEntity` dirty
  its own container in the same call — absent from the owner entirely.
  [kind=book]
- **Session I (IX) — a count that disagrees across the seam.**
  `what-the-client-is-told`:213 says "**Four** feeds ignore gate 3" and then
  names three; `synched-entity-data`:280-282 names two plus the item frame.
  The candidate for the fourth is `Entity.updateDataBeforeSync`. Re-derive with
  the decompile. [kind=book]
- **Session I (IX) — `entity-anatomy` now cites
  `what-the-client-is-told#gate-3-and-the-position-it-chooses` for
  `EntityType.trackDeltas`.** The list moved there in principle; check that
  page's own version names the same set (it has nine categories where
  `entity-anatomy` had ten types, "item frames" plural covering two).
  [kind=book]
- **Session H (VIII) — `the-sword-swing` owes two things a Reference page is
  carrying.** `reference/non-living-damage`:20-28 holds the book's only
  explanation of `Player.cannotAttack`'s two hooks (`Entity.isAttackable`,
  `Entity.skipAttackInteraction`) and its only explanation of projectile
  deflection (`Player.deflectProjectile`,
  `EntityTypeTags.REDIRECTABLE_PROJECTILE` — batting a ghast fireball back,
  named on no other page). `TEMPLATE.md` forbids a Reference page owning an
  explanation. Session F left them because moving them means writing Part VIII
  prose. Also `Entity.isPickable` defaulting to false, and the
  `handleAttack` disconnect (see the struck entry above). [kind=book]
- **Session H (VIII) — `the-two-phase-tick`:155-159 is the third full telling
  of the fall-damage gate.** `authority` owns it and now says so; that page's
  version should become one sentence carrying
  `authority#three-cases-read-on-both-sides`. [kind=book]
- **Session J (X) — `the-client-level` and `prediction-and-acks` both answer
  `authority`'s question and only one is named there.** `client/README`:67-70
  says both do; `authority`:19 names only the client level. When Part X
  settles, `authority` should cite `prediction-and-acks#two-state-machines-running-against-each-other`
  at the two places a reader asks *then where does prediction live*
  (`authority`:106-107 and :210-215). [kind=book]
- **Sessions H, I and J — the anchors on `authority`'s inbound links.** Twenty-two
  links from sixteen pages, none carrying an anchor. Part VI's own are done;
  the ones from `input-to-movement`, `the-two-phase-tick`, `player-anatomy`,
  `what-the-client-is-told`, `the-client-level` and the three landing pages want
  `authority#five-predicates-and-the-final-one-the-other-four-hang-off`.
  [kind=book]
- **Session M (XIII) — `entity-selectors` can now cite an owner for the two
  lookups.** `entity-lifecycle#findable-ticking-or-neither` defines
  `EntitySection`, `EntitySectionStorage` and `EntityLookup` as of this
  session; `entity-selectors`:199-212 explains the *query* fork and should
  point back rather than introduce them. [kind=book]
- **Session M (XIII) — the `EntitySpawnReason` and `Structure.spawnOverrides`
  Reference views ([pass3.md](pass3.md) §7) have their citers now.** The
  nineteen reasons are named on `entity-lifecycle#the-other-ways-in`, which is
  what a view of *what each one gates* would hang off; the spawn-override
  table is what `entity-lifecycle`'s new species-list passage cites for *which
  structures override what*. Session N builds the views. [kind=book]
- **Session K (XI) — `synched-entity-data`:238-244 walks the extract and layer
  pipeline with no link.** `entity-rendering` links *here* at its :16 and gets
  nothing back. The sheep-specific payoff (a layer skipped, not a model swap;
  the undercoat ignores the sheared flag) stays; the pipeline should cite
  `entity-rendering#extract-the-live-entity-becomes-a-snapshot`. [kind=book]

**Coverage, routed rather than written.**

- **Four mechanisms in Part VI's packages are bigger than a sentence and are
  explained nowhere**, declared as such on the landing page and carried to
  [pass3.md](pass3.md) §7: the minecart's two movement models
  (`MinecartBehavior`, `NewMinecartBehavior`, `OldMinecartBehavior`,
  `AbstractMinecart` — 1,800 lines that four pages name and none explains); the
  ender dragon's sixteen flight phases (`world/entity/boss/enderdragon/phases`,
  1,283 lines, named nowhere); a raid (`Raid` 898 lines, `Raider` 619, named
  only on `points-of-interest` and `level-data-and-rules`); and villager gossip
  (`GossipContainer`, 274 lines, no owner anywhere). [kind=book]
- **`ConversionType` (195 lines) is named nowhere**, and
  `points-of-interest`:372-373 sends "death and **conversion**" to
  `entity-lifecycle#five-reasons-one-label`, which covers death and not
  conversion. A mob converting is one entity removed and another created, so it
  is lifecycle-shaped; session F left it because the page's cascade is about a
  mob being *born*, not swapped. Second edition, or a later pass with the
  budget. [kind=book]
- **`foundations/data-driven-types`:151 names `entity-lifecycle` as the home of
  `BuiltInRegistries.SPAWN_CONDITION_TYPE`, `SpawnCondition` and
  `SpawnPrioritySelectors`.** The page mentions none of them, and the
  `world/entity/variant` sub-package (11 classes) is unnamed. The variant pick
  runs at `Mob.finalizeSpawn`, so the hand-forward is plausible; it is
  unpaid today. [kind=book]
- **`entity-lifecycle`:168 hands `SpawnerBlockEntity`, `BaseSpawner` and
  `TrialSpawner` to `blocks/block-entities`, which names none of the three.**
  Either that page owes them a sentence or the link goes. Part V is closed, so
  this is pass 10's or a §7 note. [kind=book]

**Pass 6 — the lecture.**

- `ai-goals-and-brains` is 438 lines against a 240–390 target even after this
  session's three cuts, and its verified line still promises *meet at the
  bell*, which the trace never delivers.
- `entity-lifecycle` and `damage-and-death` are the two pages in the part with
  no *Questions players ask* closer, and three of `entity-lifecycle`'s best
  facts are already question-shaped (*name it and it stays*, *a mob alone in a
  world never despawns*, *a wild cow on a hilltop never despawns*).
- `pathfinding`'s verified line promises "a villager decides to walk to its
  bed" — the third consecutive page to open on the same villager — while the
  page's own hook is the mob against the fence. The two halves of the line
  could swap without touching a fact.
- `authority`'s *Where the gates actually sit* is an eight-site inventory in a
  seven-item list, one bullet carrying two. A table with a *which member*
  column is the obvious shape.
- `movement-and-collision`'s *Off it goes* carries two subjects joined only by
  "the tick ends": the crowding pass, which is the trace's last step, and the
  network paragraph, which is two other pages' material cited from here.
- `pathfinding` has three enumerations over the seven-item budget (eleven
  `PathType` constants with costs, seven required-path-length values, twelve
  `MoveControl` callers in eight classes). A fourth Reference page for the 27
  `PathType`s with their default costs and the per-mob malus overrides would
  let the section keep the three sentences that matter.

**Pass 7 — the figures.**

- `authority`'s boat sequence declares `participant SL as ServerLevel` and
  sends no message on that lane; it appears only inside a `Note over`.
- `entity-anatomy`'s figcaption for the generated `Entity` tree omits the key
  `maps/hierarchy`:20 gives the same SVG, so a reader landing here first
  cannot read the numbers.

**Pass 8 — the voice.**

- Three pages phrase the same schedule rule three ways:
  `ai-goals-and-brains`:339 "fewer than 21 ticks", `points-of-interest`:236
  "more than twenty ticks", `environment-attributes-and-timelines`:384 "more
  than 20 game ticks". (This is already logged at :805-809; the third
  spelling is new.)
- `pathfinding`:33-35 and `ai-goals-and-brains`:135-138 share the sentence
  *there is not a future, an executor or a thread anywhere in…* verbatim. The
  two are a declared pair, so the repetition may be deliberate; it reads as an
  accident.
- `client/the-client-level`:195 calls the interpolation window "three-tick"
  where `movement-and-collision`:379 says "three steps". One number, two names.
- `entity-anatomy` uses *frozen* for three unrelated things on one page: the
  registry freeze, an `EntityType`'s frozen dimensions, and
  `Entity.DATA_TICKS_FROZEN`.
- `reference/naming-drift`:414-415 lists *Entity.hurt* as a 1.21 name that is
  gone; `damage-and-death`:337 has it live as a deprecated wrapper. The row
  wants the *still live* form the page already uses elsewhere.
- `maps/biggest.md`:33-34 says `Fox` and `Bee` "are the pages a reader of Part
  VI should expect to be long". Part VI has no `Fox` page and no `Bee` page.

## From pass 5, session E (Part V · Blocks), 2026-09-05

*What the reading raised and this session did not act on, tagged by the pass
that takes it. Everything session E did act on is struck above or logged in
[pass9.md](pass9.md).*

**Routed to a later part's session.**

- **Session I (IX) — `what-the-client-is-told` names the wrong hop.** Its
  :340 has `ChunkHolder.broadcastBlockEntityIfNeeded` calling
  `BlockEntity.getUpdatePacket`; the decompile has the *IfNeeded* form testing
  whether the state has a block entity and delegating to
  `ChunkHolder.broadcastBlockEntity`, which is the one call site.
  `block-entities` names the inner one and is right. Not false enough to fix
  from Part V, but the two pages should name the same method. Session I also
  owns the third copy of the empty-chest answer: `what-the-client-is-told`
  states the two sync defaults at :340-347 *and* again in its Q&A at :428-431,
  and `block-entities#a-furnace-tells-nobody-anything` owns them.
- ~~**Session G (VII) — three pages reach into `containers-and-menus` and one
  chain stops short.**~~ **Done, session G (pass 5)**: `block-entities` gained
  the onward citation of
  `diodes-and-observers#one-int-and-the-fan-out-that-exists-to-deliver-it`,
  `containers-and-menus` and `loot-tables` both now anchor at it, and
  `DataSlot` got its own sub-heading on `containers-and-menus` so
  `block-entities` and `enchanting` can cite the channel rather than the page.
  Original entry: `containers-and-menus`:150-153 cites `block-entities`
  for the comparator re-derivation, and `block-entities` is itself a
  one-sentence citation with no onward link, so the reader stops one page short
  of the owner (`diodes-and-observers#one-int-and-the-fan-out-that-exists-to-deliver-it`).
  Session G should also decide whether `DataSlot` wants a citation *from*
  `block-entities`, which today links containers-and-menus only for *opening* a
  menu. And `items/loot-tables`:275-278 explains that a comparator reading an
  unopened chest commits its loot roll, in substance, without linking either
  redstone page.
- **Session H (VIII) or a ruling — reach has no backward link from either
  click page.** `block-interaction` and `block-breaking` both use
  `Player.isWithinBlockInteractionRange` and its slack without saying what a
  reach range is; `player-anatomy` (Part VIII) owns it and is later. Both
  halves of a declared pair have the same hole, so it wants one ruling rather
  than two per-page fixes.
- **Session K (XI) — `section-meshing` and `block-interaction` describe one
  switch two ways.** Session E re-derived it: `LevelRenderer` is the class that
  reads `PrioritizeChunkUpdates` and decides `rebuildSync`, and the default is
  *NONE* while both fancy presets set *PLAYER_AFFECTED* — so
  `block-interaction` is right on both counts. `section-meshing` attributes the
  same decision to `SectionRenderDispatcher.RenderSection.compileSync` and names
  the option differently; session K should make the two agree, with
  `section-meshing` owning it and Part V citing.

**For pass 6, the lecture.**

- `signal-and-dust`'s *The second implementation* stops using the page's trace:
  the lever and the two dust vanish and the section walks
  `ExperimentalRedstoneWireEvaluator`'s fields in call order. Run the same lever
  and two dust through it and cut to the two differences the hook names. The
  same page's torch answer arrives cold — no torch appears anywhere earlier on
  the page — and its staircase is stated three times (hook, figure coda, Q&A).
- `pistons-and-block-events`' *How a piston decides, and the line that cannot
  fire* carries three subjects under a heading that promises two; splitting the
  trigger paragraph would also give `PistonBaseBlock.TRIGGER_DROP` a heading for
  *two ways to end* to point back at.
- `pistons-and-block-events`' cast promises `PistonHeadBlock` "the arm once the
  motion is over, and forwarding neighbour updates back to the base" and the
  body never returns to it. Deliver it or drop the row; the cast is at its
  ceiling of eight.
- `blocks-and-states` carries two subjects — the state table and the write —
  and its verified line and opening hook promise only the first, so the
  server-gated destroy at the end arrives unheralded. The page should not be
  split (all six sibling links land on its second half, which is the part's
  hub), but the header line and one clause in the opening would carry the
  reader across the seam.
- `block-interaction`'s Q&A entry on breaking a door's bottom half teaches the
  same thing as the body four sections earlier, with the same three method
  names. It is the page's only genuine internal duplicate.
- The *constant nobody reads* device appears several times in Part V
  (`PistonStructureResolver.MAX_PUSH_DEPTH`, `PistonMovingBlockEntity.TICKS_TO_EXTEND`,
  `HopperBlockEntity.MOVE_ITEM_SPEED`, plus the torch's three) and the page that
  explains why a decompile cannot tell is `client/the-client-loop`. None of the
  uses cites it.

**For pass 7, the figures.**

- `pistons-and-block-events`' flag table is five rows with a *written by* column
  and wants the `custom.css` wide treatment.
- `block-entities`' sequence diagram uses three names for one menu — the lane
  *FM as FurnaceMenu*, then `AbstractContainerMenu.broadcastChanges`, then
  `AbstractFurnaceMenu.getLitProgress` — which reads as three objects.
- `diodes-and-observers`' channel flowchart re-derives the two update channels
  in its node labels rather than citing them; that is legitimate for a figure
  that must be readable alone, but the citation is seventy-odd lines away and
  pass 7 should decide whether the labels shorten.

**For pass 8, the voice.**

- Part V says *flags 3* repeatedly and never names `Block.UPDATE_ALL`; the
  catalogue now decomposes all four combinations, so the pages could use either
  form consistently.
- `blocks-and-states`' *The two update channels* heading is cited by six sibling
  pages and by three Part IV pages; if pass 8 rewords it, every one of those
  anchors moves. Same for `block-entities#loaded-is-not-enough-to-tick`.

**Coverage, for [pass3.md](pass3.md) §7 and the second edition.**

- **The hopper is the largest unowned mechanism in Part V.**
  `HopperBlockEntity` (547) with `HopperBlock` (182): the book gestures at it
  from three pages — `containers-and-menus` uses it as *the* example of the
  block-entity phase, `diodes-and-observers` as the thing a comparator notices,
  and `loot-tables` as a way into a chest — and nothing anywhere explains the
  transfer, the five slots, the push-versus-pull asymmetry or the ordering.
  Session E named its cadence on `block-entities` and declined the rest: it is a
  lecture, not a sentence.
- **The sculk spread machine has no home.** `SculkSpreader` (387),
  `SculkBlock` (109), `SculkVeinBlock` (211).
  `world/game-events-and-vibrations` owns the sensor, the shrieker and the
  catalyst; the charge-and-spread machine is named nowhere in the book.
- **Structure and command blocks are named nowhere in `src/`.**
  `StructureBlockEntity` (582), `StructureBlock` (109), `CommandBlock` (261),
  `CommandBlockEntity` (205) — only their two serverbound packets appear, as
  rows in `reference/packets`. Part XIII is the natural home for the command
  block; the structure block belongs beside `jigsaw-and-templates`.
- **Four state machines are half-adopted by other parts.**
  `BeaconBlockEntity` (434), `ConduitBlockEntity` (300), and the *trialspawner*
  (642 unmentioned lines) and *vault* (432) sub-packages, whose outer classes are
  named on Part VI and Part VII pages while their state machines are explained
  nowhere.
- Session E discharged what a sentence could reach: the *state/properties*,
  *state/pattern* and *state/predicate* sub-packages and `InstantNeighborUpdater`
  on `blocks-and-states`; the redstone source blocks on `signal-and-dust`; the
  seven block-event raisers and `PistonMath` on `pistons-and-block-events`; the
  *block/entity* family and the hopper's cadence on `block-entities`; the
  use-hook family, with the count the queue asked for restored (25 override
  `BlockBehaviour.useItemOn`, 52 `BlockBehaviour.useWithoutItem`), on
  `block-interaction`. The four items above are what a sentence cannot reach.

## Session G — Part VII · Items and inventories (pass 5) *(2026-09-05)*

*What nine page reads and one end-to-end reading of the part turned up and
session G did not act on, routed by kind. The claims it introduced and the
corrections it made are in [pass9.md](pass9.md).*

### For other part sessions (pass 5)

- **Session H (VIII) — `Consumable`, `FoodProperties` and `ConsumableListener`
  are defined on a Part VIII page and spent whole by a Part VII one.**
  `using-an-item` runs its entire first scenario on the `Consumable` family and
  the only definition in the book is `player/hunger-and-experience`:88-104.
  `PotionContents` (252 lines, `world/item/alchemy`) and
  `TeleportRandomlyConsumeEffect` (`world/item/consume_effects`) have the same
  shape — a `world/item` component family living on a Part VIII page. Session H
  decides whether the definition moves to Part VII or `using-an-item` cites it;
  the routing rule gives the pair to the later part.
- **Session H (VIII) — `UseEffects` is explained twice.** `using-an-item`:165-176
  owns the slowdown half (it is that page's scenario) and
  `hunger-and-experience`:147-156 states the component and its three fields,
  including the `UseEffects.interactVibrations` half that `using-an-item` only
  gestures at. One owner, one citation, and the vibration half is a move.
- **Session H (VIII) — two landing pages hand `Inventory` to each other.**
  `player/README`:57-59 says Part VII owns "the inventory this part stops at
  the edge of"; `items/README` says the part stops at the slot and Part VIII
  owns the inventory. `player/player-anatomy`:122-137 settles it in Part
  VIII's favour, so Part VIII's sentence is the loose one.
- **Session H (VIII) — `ItemStack.inventoryTick`'s two callers.**
  `items-and-stacks`:293-297 and `player/player-anatomy`:293-298 both explain
  why item ticking needs two callers. `player-anatomy` owns it (the forty-three
  slots are its subject); `items-and-stacks` keeps what the method itself does.
  Left for session H because the cut is on the Part VIII side of a Part VIII
  claim. `items-and-stacks` adds "tells the selected one it is the main hand",
  which is a move.
- **Session H (VIII) — `using-an-item`:180 pointed at `the-sword-swing` for the
  spear and now points at `the-spear`.** Session H should check the round trip:
  `player/README`:57-59 sends readers to Part VII *for* the spear.
- **Session I (IX) — `packets-and-stream-codecs`:368-373 describes the
  `HashedStack` shape, which `containers-and-menus` owns.** The packet page
  names `HashedPatchMap.addedComponents` and `HashedPatchMap.removedComponents`,
  which the click page describes without naming: a move, not a cut. The framing
  claim (*exactly one packet lets a client hand the server an item*) is the
  packet page's and `containers-and-menus` now keeps the handler only.
- **Session J (X) — `client/gui-and-screens` and `containers-and-menus` are
  unlinked in both directions on three shared mechanisms**: the null `MenuType`
  (its hook), `AbstractContainerScreen`'s click resolution, and
  `CreativeModeInventoryScreen`. The glossary's **Menu** entry (`glossary`:391)
  describes only the server's object, where the page insists there are two.
- **Session M (XIII) — `brigadier-and-commands`:255 routes `LootCommand` and
  `ItemCommands` to `loot-tables`, which names neither**; both are on
  `contexts-and-predicates`:233-234. The row's `/item modify` claim is
  `loot-tables`', so the row wants two destinations.
- **Session M (XIII) — `advancements`:7-10 opens on
  `AbstractContainerMenu.broadcastChanges` and links `containers-and-menus`
  nowhere**, and `entity-selectors`:118 and `advancements`:146-150 are each
  half of a fact whose other half is on `contexts-and-predicates`. Four
  inbound links from Part XIII, none anchored.
- **Session M (XIII) — the predicate shape library, ruled.** §7 asks whether
  `MinMaxBounds`, `CollectionPredicate`, `EntitySubPredicate` and
  `DataComponentMatchers` belong here or in a Reference page. Session G's
  ruling, for M to apply or overturn: **they stay a table on `advancements`**.
  They are four classes explained in prose, not an enumeration a tool can
  read, and the page whose scenario invented them owns them;
  `contexts-and-predicates` owns the *context* machinery and not these, and
  now cites `advancements` from its own predicate-package paragraph. A
  generated view is still possible for the two that *are* registries
  (`DataComponentPredicates`, `ENTITY_SUB_PREDICATE_TYPE`) and would not
  replace the table.
- **Session N (Reference) — the glossary has no entry for *loot context*,
  *loot condition* or *parameter set***, all three used unglossed on six pages
  in three parts, all three owned by `contexts-and-predicates`.
- **Session N (Reference) — `reference/attributes`' `Attributes.LUCK` row is
  linked from no system page**, and `loot-tables#one-roll-drawn` is the only
  page that explains what luck does.

### For pass 6 — the lecture

- **Part VII is the longest part per page in the corpus** and this session made
  four of its pages longer, not shorter. `enchantments` is 357 lines with a
  92-line *Questions the pattern raises*; `containers-and-menus` ends on a
  nine-packet enumeration in prose (L372-387); `loot-tables` lists nine entry
  types in prose inside the paragraph that explains the algebra. The length
  bill is still Part VII's. [kind=lecture]
- **Three pages of eight have no *Questions players ask* closer** —
  `containers-and-menus`, `contexts-and-predicates` and `using-an-item` — and
  each has the material for one inline. `contexts-and-predicates` is the sharp
  case, because its declared pair (`loot-tables`) ends on one and it ends on a
  dependency note. [kind=lecture]
- **`enchanting`'s last section carries three subjects** (providers, loot and
  trades, and then the creative tabs) and its heading names two. [kind=lecture]
- **`enchanting`'s *What it costs, and who pays*** spends its second half on
  what the grindstone pays *out*; the heading is right about the anvil only. [kind=lecture]
- **`using-an-item`'s cast says "client main" where the book says Render
  thread** (`anatomy`:61, `reference/threads`:61, and both adjacent pages). [kind=lecture]
- **`recipes` says the `CraftingInput` constructor's accounting twice**, 170
  lines apart in different vocabulary (L152-153 and L324-326). [kind=lecture]
- **`items-and-stacks` explains the pop time twice** (in the fields section and
  again in the tick section). [kind=lecture]

### For pass 7 — the figures

- **`items/README`'s figure draws a chain where the prose claims two tiers**
  (`IS → UI → CM → RE` in a line), and draws no edge between `EC` and `LO`
  though two of enchanting's five paths are loot functions. The prose is right
  about the shape; the figure is the artefact and should carry it. [kind=figure]
- **`items-and-stacks` and `data-components` draw the same object.** Both
  flowcharts run `ItemStack` → `PatchedDataComponentMap` → patch with the
  dotted prototype arrow. After this session's cut the Part VII page should
  draw the `ItemStack` fields and the `Item`'s four and drop the patch
  internals, which are Part II's. [kind=figure]
- **`loot-tables`' funnel flowchart is sixteen edges** and now carries the
  splitter's corrected level as a note; pass 7 should judge whether the
  correction reads at the column width. [kind=figure]

### For pass 8 — the voice

- **`enchantments` says "forty-three" of two unrelated things** 158 lines apart
  (the vanilla enchantments, and the lines of JSON in Fire Aspect's file). [kind=voice]
- **`containers-and-menus`:316 "those four"** counts four categories, one of
  which is itself four slots. [kind=voice]
- **`using-an-item`:328 "five enchantment hooks"** are spread over three
  paragraphs and the fifth is only implicit. [kind=voice]
- **`recipes`:104-105 says "for the first" and "for the second"** over a
  three-item list, leaving the third unaccounted. [kind=voice]
- **`using-an-item`:47 uses *acknowledged*** four rows above a sentence about
  sequence numbers, for something that is not the ledger's acknowledgement. [kind=voice]
- **The *ledger* metaphor** stands on both `loot-tables` and
  `contexts-and-predicates` ("a stack, not a ledger"), which is the pair the
  brief's A3 already logged for pass 8. [kind=voice]
- **`enchantments`:109-112 is near-verbatim with `reference/enchantment-hooks`'
  generated intro** ("the enchantment package barely calls anything and
  everything calls it"); the Reference prose lives in `gen_reference.py`, so
  the page is the copy that should vary. [kind=voice]

