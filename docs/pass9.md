# Pass 9 — the third fact-check (queue; opened 2026-09-05)

*Pass 9 re-runs pass 4's adversarial protocol — archived in
[pass4.md](pass4.md) with its charter, its agent brief
([pass4-brief.md](pass4-brief.md)) and its lessons — over the corpus passes
5–8 rewrite. This file is where every pass-5, -6, -7 and -8 session writes
down what pass 9 must check first: every page it rewrote, every claim a
rewrite introduced (a hook, a moved paragraph, a redrawn arrow, a re-scoped
count, a new section, a landing page's new argument), and every correction
it made with the decompile open. Pass 9 checks everything anyway; this list
decides what it checks first. It is also what made pass 4 checkable: from
Part VI on, the errors were in what the writing session did not know it had
changed, so a session lists what it changed on purpose and pass 9 reads the
rest harder.*

## How to write an entry

Per session, newest first, under `## Session X — Part N (pass M)`: the pages
rewritten; per page, one line per claim introduced, quoting the sentence;
the figures redrawn, and which orderings they assert; the material moved,
from where to where; and, under *Corrections*, every fact changed with the
decompile open — what the page said, what the decompile says, file and line.
Name the page in backticks on every line so a queue tool can route it.
Strike nothing here; pass 9 strikes.

## Standing items

- **A correction is a claim.** Pass 9 confirms the fix, not the original,
  and its close audits the pass's own strikes — session O of pass 4 found a
  strike that had settled nothing and a correction that was the error.
- **The summarisers are read last.** The thirteen landing pages,
  `lectures.md`, the glossary and the introduction are re-read after the
  pages they summarise are fixed, never before.
- **The figure against the section under it first**, before either is read
  against the source: nine pages in pass 4 had a diagram contradicting its
  own paragraph, and the prose was right every time.
- **Counts are call sites, not `grep -c` lines**; a generated page is
  checked by re-deriving the population, never a row.
- **Names inside mermaid blocks** are under a gate from pass 7's close; the
  23 ambiguous simple names the verifier prints are settled by pass 8 or in
  the tool.
- **Pass 9 adds nothing.** A gap it finds goes to [pass3.md](pass3.md) §7,
  the coverage queue, which seeds the second edition.

## Entries

## Pass 7, session M — Part XIII · Commands and data packs: the figures *(2026-09-16)*

Ten pages, 13 figures (the count unchanged). Every figure captioned, every
caption one italic run; the figure-name gate is **0 unresolved and 2 notes**
for the part (was 4 and 7; the two are bare-word message heads, F12(d));
nothing is below **0.78** or under **12.5px** (was 0.69 and 11.1px); no lane
is over six (was seven on `advancements` and `scoreboard-and-data`); no label
overlaps another or sits on a node (was four figures); and **no Mojang name is
hyphen-broken on screen** (eight were). Two figures changed kind to
`classDiagram` (`permissions` f1, `game-tests` f1), the book's ninth and
tenth.

### Figures redrawn, and the orderings they assert

- **`commands/README` figure 1** — `TD` with the four systems on the top floor,
  as the prose calls it (`TB` drew them at the bottom); the floors' internal
  `---` links, a mark outside F3's table, are layout-only; the two arrows read
  *is built on*; titles short enough not to be clipped. Asserts nothing about
  the game. Caption: *nothing on the top floor points at another box there*.
- **`brigadier-and-commands` figure 1** — Client and Server boxes; the
  ask-server round trip in an `opt` frame; the server thread as a band.
  Asserts, in order: `CommandSuggestions` gets the dispatcher from
  `ClientPacketListener.getCommands` and parses on every keystroke
  (`CommandSuggestions.updateCommandInfo`); only for an ask-server node,
  `ClientSuggestionProvider.customSuggestion` sends
  `ServerboundCommandSuggestionPacket`, the reply lands on
  `ClientPacketListener` and is forwarded to
  `ClientSuggestionProvider.completeCustomSuggestions`; on Enter
  `ClientPacketListener.sendCommand` parses again and sends
  `ServerboundChatCommandPacket`; `ServerGamePacketListenerImpl.tryHandleChat`
  runs on the Netty thread; then, on the server thread,
  `ServerGamePacketListenerImpl.parseCommand`, `Commands.performCommand`, the
  registered lambda, `GiveCommand.giveItem`. Caption: *`/give` has none* (no
  ask-server node).
- **`permissions` figure 1** — a flowchart of three bands wired
  question → answer → check becomes a class diagram. Asserts:
  `PermissionProviderCheck` holds a `PermissionCheck`; `PermissionCheck.Require`
  and `PermissionCheck.AlwaysPass` implement it; `Require` holds a `Permission`
  and asks the source's `PermissionSet`; `Permission.Atom` and
  `Permission.HasCommandLevel` implement `Permission`;
  `LevelBasedPermissionSet` extends `PermissionSet`; `PermissionSetUnion`
  implements it; `ChatAbilities` **holds** one. The `ClientPacketListener`
  node (its two sets) is gone.
- **`permissions` figure 2** — `TD`. Asserts the order of
  `ClientPacketListener.verifyCommand`'s tests — parse with your own set, then
  signable arguments, then parse with `PermissionSet.NO_PERMISSIONS` — and that
  the parse-error and permissions outcomes open a `ConfirmScreen` whose button
  sends, the signature outcome one whose button suggests or copies, and only
  the clean outcome sends with no screen.
- **`entity-selectors` figure 1** — titles shortened so neither is clipped
  (*at parse time*, *per execution*); the compile box's three products no
  longer joined by an unexplained `---`.
- **`entity-selectors` figure 2** — redrawn. Asserts: a bare name goes to
  `PlayerList.getPlayerByName` whatever the scope; a UUID goes to
  `ServerLevel.getEntity` level by level when non-players are in scope and to
  `PlayerList.getPlayer` when not; *@s* tests the source's own entity; the
  three shortcuts return with no sort and no cut; otherwise world-limited
  picks this level or every level, then players-only walks a player list and
  the rest take the box query or the lookup walk; every walk ends in *sort
  unless arbitrary, then cut*.
- **`the-execution-engine` figure 1** — four panels, `TD`, titles short;
  the starting entry (`BuildContexts.TopLevel`, depth 0) is in the lead-in.
  Asserts the queue after entry 1 ran (a `ContinuationTask` alone), after the
  task ran (A's entry, then the task behind it), after A's entry ran (the task
  alone, B not yet made), after the task ran again (B's entry, then the task);
  all at depth 0 in the top frame. Caption: `ExecuteCommand` is the leaf task
  in `commands/execution/tasks`.
- **`functions-and-macros` figure 1** — eight sentence boxes become a decision
  flowchart. Asserts: one dollar line makes a `MacroFunction`, otherwise a
  `PlainTextFunction`; instantiating a plain one returns itself; a macro one
  fails with `FunctionInstantiationException` when arguments are missing or
  the substituted text does not parse; `/function` reports that and a tag
  swallows it; the `InstantiatedFunction` is queued by `CallFunction`.
- **`advancements` figure 1** — seven lanes to six (`AdvancementRewards`
  folded), Server and Client boxes, the server half one `ServerPlayer.tick`
  band. Asserts: `ServerPlayer` calls
  `AbstractContainerMenu.broadcastChanges`; the menu calls
  `ContainerListener.slotChanged` on the player's own listener; the player
  fires `InventoryChangeTrigger.trigger`; the sweep, the test, `award` after
  the sweep; `PlayerAdvancements.unregisterListeners` then the rewards; the
  root marked; `PlayerAdvancements.flushDirty` last in the tick, then
  `PlayerAdvancements.updateTreeVisibility`; the packet; then
  `ClientAdvancements.update` rebuilds, reconciles and adds the toast.
- **`scoreboard-and-data` figure 1** — seven lanes to six (`Commands`
  dropped), Server and Client boxes. Asserts: the *as @a* fork in
  `BuildContexts`; the store modifier once per source, with
  `ExecuteCommand.storeValue` chaining the callback; the leaf
  `DataCommands.getData` once per source, building the whole save tag, then
  the path and the collapse; the result returns to the source's callback;
  `ExecuteCommand` calls `ServerScoreboard.getOrCreatePlayerScore` **and then
  `ScoreAccess.set` itself**; `ScoreAccess` calls
  `ServerScoreboard.onScoreChanged` only if changed or new; the packet only
  for a displayed objective; `ClientPacketListener.handleSetScore` builds a
  name-only holder.
- **`dialogs` figure 1** — `RegistryDataLoader` lane dropped, a
  `DialogControlSet` lane added (key row `DCS`), Server and Client boxes.
  Asserts: `DialogCommand` → `ServerPlayer.openDialog` →
  `ClientboundShowDialogPacket` (a holder id or inline) →
  `ClientCommonPacketListenerImpl.handleShowDialog`, which builds the screen;
  `DialogScreen` → `DialogControlSet.addInput` per input; at the click the
  control set's action reads the getters, then `DialogScreen.runAction`, then
  `DialogConnectionAccess.sendCustomAction` → the listener →
  `ServerboundCustomClickActionPacket` → `MinecraftServer.handleCustomClickAction`.
- **`game-tests` figure 1** — three bands become a class diagram. Asserts:
  `GameTestInstance` holds `TestData` (`info`) and has
  `GameTestInstance.run`; `TestData` names the environment;
  `GameTestBatch` is keyed by an environment and holds up to fifty
  `GameTestInfo`s; `GameTestInfo` holds its test and its
  `TestInstanceBlockEntity` and makes a new `GameTestHelper` at tick zero;
  `GameTestHelper` holds its `GameTestInfo`. `TestBlock` left to its section.
- **`game-tests` figure 2** — the tick-driven half is a band. Asserts:
  `GameTestRunner` calls `GameTestInfo.prepareTestStructure` for each run,
  which calls `TestInstanceBlockEntity.placeStructure` then
  `TestInstanceBlockEntity.encaseStructure`; **then** the environment is
  activated; then the placed runs are added to `GameTestTicker`; each tick
  `GameTestTicker` ticks the run; at zero `GameTestInfo.startTest`; succeed or
  fail; `GameTestListener.testPassed` or `GameTestListener.testFailed`;
  `TestInstanceBlockEntity.setSuccess` or
  `TestInstanceBlockEntity.setErrorMessage`; chat, then `GlobalTestReporter`.
  Caption: the beam is *green, red, or orange for an optional test that
  failed*.

### Captions written (claims about what each figure shows)

Thirteen, one per figure; each is quoted in the page directly under its
figure. The ones that state a fact beyond the drawing: `brigadier-and-commands`
(*`/give` has none*); `functions-and-macros` (*only the macro branch can fail
there*); `advancements` (*everything on the server happens inside the tick
that saw the slot change*); `dialogs` (*a handler that, in vanilla, writes a
debug log line and nothing else*); `game-tests` f2 (orange);
`the-execution-engine` (every entry at depth 0 in the top frame).

### Prose added (the one sentence a figure's name needed)

- `brigadier-and-commands`: the client's dispatcher is the one
  `ClientPacketListener.getCommands` hands the widget; the reply lands on
  `ClientPacketListener.handleCommandSuggestions`, which forwards it;
  `ChatScreen` calls `ClientPacketListener.sendCommand`; the plain packet is
  `ServerboundChatCommandPacket`; `ServerGamePacketListenerImpl.tryHandleChat`
  refuses illegal characters on the Netty thread; the server's parse is
  `ServerGamePacketListenerImpl.parseCommand`; the lambda calls
  `GiveCommand.giveItem`.
- `permissions`: a paragraph on `SignableCommand.hasSignableArguments` — an
  unattended command cannot be signed, so its `ConfirmScreen` offers to put it
  in the chat box or, when a screen is to follow or chat commands are off, to
  copy it (`ClientPacketListener.openSignedCommandSendConfirmationWindow`).
- `entity-selectors`: *Three shortcuts come first* (name, UUID, *@s*; none is
  sorted or cut).
- `the-execution-engine`: the lead-in names the starting entry.
- `functions-and-macros`: a lead-in.
- `advancements`: the slot change reaches the trigger through the player's own
  `ContainerListener`; the flush is one `ClientboundUpdateAdvancementsPacket`
  and runs `PlayerAdvancements.updateTreeVisibility` once per dirty root;
  `ClientAdvancements.update` removes and adds nodes, reconciles progress,
  and adds an `AdvancementToast` for each now-done advancement whose display
  asks for one, with a sound only for a challenge. *Each arrow is a decision*
  became *The paragraphs below take its arrows in order*.
- `scoreboard-and-data`: a lead-in naming `BuildContexts`; the same
  *take its arrows in order* change; `ClientPacketListener.handleSetScore`
  builds only a name-only holder.
- `dialogs`: `DialogControlSet.addInput` registers the getters; the click goes
  through `DialogScreen.runAction` and
  `DialogConnectionAccess.sendCustomAction`; the play-phase packet names a
  registered dialog by holder id and sends an unregistered one inline, and
  the configuration-phase packet is always inline.
- `game-tests`: *The structure comes first, then the environment*;
  `GameTestInfo.startTest` hands the body a new helper; the listener chain's
  two calls and the block entity's two setters.

### Corrections

- **`brigadier-and-commands` figure 1** — drew `getCompletionSuggestions`
  arriving at `ClientPacketListener`; it is `CommandDispatcher`'s, called by
  `CommandSuggestions.updateCommandInfo` on the dispatcher it fetched with
  `ClientPacketListener.getCommands` (`CommandSuggestions.java`:225–235,
  `ClientPacketListener.java`:2770).
- **`brigadier-and-commands` figure 1** — the suggestion reply ended on
  `ClientPacketListener`; `ClientPacketListener.handleCommandSuggestions`
  forwards it to `ClientSuggestionProvider.completeCustomSuggestions`, where
  the id is matched (`ClientPacketListener.java`:1755–1757).
- **`brigadier-and-commands` figure 1** — the prose under it says all three
  parses are *in there*; the figure drew two. The second,
  `ClientPacketListener.sendCommand`, called from `ChatScreen`
  (`ChatScreen.java`:351), is drawn now.
- **`brigadier-and-commands` figure 1** — drew the server's parse on
  `Commands`; it is `ServerGamePacketListenerImpl.parseCommand`, and
  `performUnsignedChatCommand` then calls `Commands.performCommand`
  (`ServerGamePacketListenerImpl.java`:1713–1720, :1823). The Netty-side
  check is `tryHandleChat`, which then calls `server.execute` (:1829–1837).
- **`brigadier-and-commands` figure 1** — a self-message on `GiveCommand`
  named `Inventory.add` and `CommandSourceStack.sendSuccess`; they are called
  from `GiveCommand.giveItem` (`GiveCommand.java`:38, :58, :80), which the
  label now names.
- **`permissions` figure 1** — listed `ChatAbilities` among the sets that
  answer; it is a plain class that holds a `PermissionSet`, a lambda over a
  literal set (`ChatAbilities.java`:14, :18, :34).
- **`permissions` figure 2** — drew all three non-clean outcomes converging
  on one *the player decides* screen; the signature outcome's confirmation
  never sends — its button suggests the command into chat or copies it
  (`ClientPacketListener.java`:2890–2903), while the other two send
  (:2883–2887).
- **`entity-selectors` figure 2** — the players-only branch skipped the name,
  UUID, *@s* and world-limited decisions `EntitySelector.findPlayers` makes
  (`EntitySelector.java`:207–258).
- **`entity-selectors` figure 2** — the UUID leaf on the entities branch said
  `PlayerList.getPlayer`; `EntitySelector.findEntities` looks the UUID up in
  every level with `ServerLevel.getEntity` (`EntitySelector.java`:131–146);
  `PlayerList.getPlayer` is the players-only branch's (:214).
- **`the-execution-engine` figure 1** — the fourth panel's title (*A's say hi
  is done*) sat over the queue one step later, after the task had run again;
  at that moment the queue is the task alone (`ContinuationTask.java`:23–29).
- **`the-execution-engine`**, prose — *one cost unit per stage* and *the
  modifier stage that forked … was the single unit charged*;
  `BuildContexts.execute` charges only a stage whose redirect modifier is
  non-null, after the custom-modifier hand-off (`BuildContexts.java`, the
  stage loop: `if (modifier != null) { context.incrementCost(); …`), so this
  chain pays for *as @a* and *at @s*, not *run* — two units. Both sentences
  now say so.
- **`advancements` figure 1** — the toast self-message said *silent unless it
  is a CHALLENGE*; `ClientAdvancements.update` adds the toast whenever the
  packet allows and `DisplayInfo.shouldShowToast` says so
  (`ClientAdvancements.java`:61–70), and only its sound depends on
  `AdvancementType.CHALLENGE` (`AdvancementToast.java`:56, :62).
- **`scoreboard-and-data` figure 1** — drew `ServerScoreboard` calling
  `ScoreAccess.set`; the store callback made by `ExecuteCommand.storeValue`
  calls `getOrCreatePlayerScore` and then `ScoreAccess.set` itself
  (`ExecuteCommand.java`:284–298).
- **`scoreboard-and-data` figure 1** — put the display-slot condition on the
  `ScoreAccess` → `ServerScoreboard` arrow; that arrow's gate is *changed or
  new*, and the display-slot gate is inside `ServerScoreboard.onScoreChanged`
  (`ServerScoreboard.java`:60–66) — two gates, now on two arrows.
- **`dialogs` figure 1** — drew `DialogScreens.createFromData` arriving at
  `DialogScreen`; it is called inside
  `ClientCommonPacketListenerImpl.showDialog`, after `handleShowDialog`
  (`ClientCommonPacketListenerImpl.java`:270–293).
- **`dialogs` figure 1** — put `DialogControlSet.addInput` and
  `Action.createAction` on the `DialogScreen` lane; `DialogControlSet` is its
  own object — `DialogScreen` calls `addInput` on it (`DialogScreen.java`:82)
  and its bound action calls `Action.createAction` at the click, then
  `DialogScreen.runAction` (`DialogControlSet.java`:48–66).
- **`dialogs` figure 1** — drew the reply from `DialogScreen` straight to
  `MinecraftServer`; it goes `DialogScreen.handleDialogClickEvent` →
  `DialogConnectionAccess.sendCustomAction` (`DialogScreen.java`:220) →
  `ClientCommonPacketListenerImpl`'s access, which sends the packet (:522–524),
  → `ServerCommonPacketListenerImpl.handleCustomClickAction` →
  `MinecraftServer.handleCustomClickAction` (:103–105; `MinecraftServer.java`:2352).
- **`game-tests` figure 2** — drew `succeed` arriving at
  `ReportGameListener`; `GameTestInfo.succeed` is the run's own
  (`GameTestInfo.java`:271), and the listener hears `testPassed` or
  `testFailed` from `GameTestInfo.tick` (:116–125) — the caller's method at
  the callee, **eleven parts of eleven**.
- **`game-tests` figure 2** — drew `TestEnvironmentDefinition.setup` as
  `GameTestRunner`'s own step; the runner calls
  `TestEnvironmentDefinition.activate` (`GameTestRunner.java`:109), which
  calls `setup` and keeps what it returns (`TestEnvironmentDefinition.java`:58–59).
- **`game-tests` figure 2** — *green, red or orange* with orange explained
  nowhere; orange is a failed optional test
  (`TestInstanceBlockEntity.java`:64–66, :219–228). In the caption.

### Tool change

- **`tools/check_figure_names.py`** — a `classDiagram` member line was read
  as a declaration only if its name had two CamelCase humps, so a one-word
  method (`boolean check(PermissionSet)`) became a *note* and was never
  checked against its box. It now reads a parenthesised one-word name too;
  two probe cases; the only corpus change is that note, on `permissions`.

## Pass 7, session L — Part XII · World generation: the figures *(2026-09-16)*

Eleven pages, 15 figures (the count unchanged: `density-functions`' three
repeated panels became one four-node flowchart and a table beside it). Every
figure captioned, every caption one italic run; the figure-name gate is **0
unresolved and 7 notes** for the part (was 4 and 35; the seven are bare
lower-case self-message heads, F12(d)); nothing is below **0.756** or under
**12.1px** (was 0.61 and 9.7px); no lane is over six (was eight on `biomes`,
seven on `features-and-placement`); no label overlaps another or sits on a
node (was eight figures); and **no name is hyphen-broken on screen** (one
file name and one ordinary word were).

### Figures redrawn, and the orderings they assert

- **`biomes` figure 1** — eight lanes to six: `ChunkStatusTasks` is a note and
  `Climate.RTree` is inside `Climate.ParameterList`'s self-message. Asserts:
  the generator builds the `NoiseChunk` and wraps the resolver *before*
  `ChunkAccess.fillBiomesFromNoise`; `ChunkAccess` loops over sections and
  calls `LevelChunkSection.fillBiomesFromNoise` once per section; each of 64
  quart cells goes `LevelChunkSection` → `MultiNoiseBiomeSource.getNoiseBiome`
  → `Climate.Sampler.sample` → `Climate.ParameterList.findValue` →
  `Climate.ParameterList.findValueIndex`, and the holder returns through the
  biome source into the new container. Caption: *no block is read and none is
  written*.
- **`blending` figure 1** — the dotted annotation node cut; the five consumers
  on one row in status order, the two direct ones on arrows labelled *read
  directly*. Asserts: carving mask and border ticks read `BlendingData`
  without a blender; *blend_density* wraps the final density.
- **`blending` figure 2** — two shaded bands, *BIOMES* and *NOISE*. Asserts:
  `Blender.of` asks `ChunkMap.isOldChunkAround` through the region; the
  193-position loop calls `BlendingData.getOrUpdateBlendingData`; the generator
  calls `NoiseChunk.forChunk`, whose constructor calls
  `Blender.blendOffsetAndFactor` for 25 columns, *then* asks
  `Blender.getBiomeResolver`; at *NOISE* a second blender is built and not
  used, and the cached `NoiseChunk` calls `Blender.blendDensity`.
- **`creating-a-world` figure 1** — stages 1–3 inside a *worker thread*
  subgraph; stage 4 loops back to 1 on *packs or flags changed*; *Create* goes
  to 5.
- **`creating-a-world` figure 2** — `autonumber` removed (its 9.7px digits were
  the only small type, and the prose cites no number); the `MinecraftServer`
  lane is now `IntegratedServer`, the object constructed; two bands. Asserts:
  `IntegratedServer`'s construction, and with it the hand-off of
  `WorldGenSettings` to its `SavedDataStorage`, happen on the render thread
  after `level.dat` is written; the two settings files are written by the
  server thread's first save.
- **`density-functions` figure 1** — the three 1,729px panels are a four-node
  `LR` flowchart (parsed → seeded → wrapped, and seeded → `RandomState.sampler`)
  plus a node × form table. Asserts: three visitors, not two; the pointer is
  resolved only in the wrapped form; the null noise leaf answers 0.0; the F3
  readout samples the seeded form.
- **`features-and-placement` figure 1** — edge labels carry the count of
  positions; direction `TD`. Order unchanged (it is `trees_plains`' shipped
  order, with a rarity roll added at the head, which the caption now says).
- **`features-and-placement` figure 2** — seven lanes to five
  (`ChunkStatusTasks` a note, `FeatureSorter` in a self-message), with nested
  loops per step, per placed feature, per modifier and per surviving position.
  Asserts: `ChunkGenerator.featuresPerStep` is read, not recomputed;
  `WorldgenRandom.setFeatureSeed` runs before every feature; structures come
  first in each step.
- **`hand-built-structures` figure 1** — `StructureStart` lane cut, the drain
  loop driven from `StrongholdStructure`. Asserts, in order per try: `clear`,
  reseed, `StrongholdPieces.resetPieces`, `addPiece` of a new start piece,
  `addChildren` on the start piece, then *while the pending list is not empty*
  `addChildren` on a randomly removed piece, whose own code picks, runs
  `findCollisionPiece`, and adds to the builder *and* the pending list; then
  `moveBelowSeaLevel`; the outer loop ends only when the start piece has
  recorded a portal room; `build` is called by the structure after the loop.
- **`jigsaw-and-templates` figure 1** — a `JigsawPlacement` lane added (key row
  `JP`), `StructureTemplatePool` lane cut, an `alt` for the depth limit, a
  *FEATURES* band. Asserts: `JigsawPlacement.addPieces` makes the centre and
  the stub; the stub's consumer builds the free-space shape and runs the
  placer; inside the loop, below the limit the target pool then the fallback
  is offered, at the limit the fallback only; `getFirstFreeHeight` is asked
  unless both pieces are rigid; a junction is added to both pieces; the child
  is queued by placement priority. At *FEATURES*, `postProcess` reaches the
  piece through `StructureStart.placeInChunk` and `placeInWorld` is called
  through the pool element.
- **`structure-placement` figure 1** — the statuses between the five decisions
  written on the edges, `BIOMES` and `NOISE` no longer one box.
- **`terrain` figure 1** — edge labels shortened; asserts the `NoiseChunk` is
  built at *BIOMES* and interpolation is disarmed after *NOISE*; the fifth box
  is labelled as a later page's.
- **`terrain` figure 2** — subgraph titles cut to what fits on one line (the
  old ones were clipped and overlapped), the method names moved to a six-row
  table beside it with a *samples the graph* column.
- **`trees` figure 1** — a shaded band for *nothing written yet*, holding all
  three ways out; the scan drawn as a loop of `TrunkPlacer.isFree` calls; lanes
  reordered by first use. Asserts: `RootPlacer.placeRoots` simulates in full
  before writing, and its roots are the first write; `TreeFeature.updateLeaves`
  is the feature's own last step.
- **`worldgen/README` figure 1** — `TD`, short subgraph titles, the undirected
  link removed, the *is made of* arrow dashed and labelled, and a dashed
  *pieces become blocks* arrow from the structure box to *FEATURES*.

### Corrections — re-derived against the decompile before the fix

- `biomes` figure 1: `CPList->>CRT: findValueIndex` drew
  `Climate.ParameterList`'s own method arriving at the tree, and the holder
  returned from the tree straight to `LevelChunkSection`.
  `Climate.ParameterList.findValue` calls its own `findValueIndex`, which calls
  `index.search` (Climate.java:251–280); `MultiNoiseBiomeSource.getNoiseBiome`
  returns the holder (MultiNoiseBiomeSource.java:65–72). The caller's method
  at the callee, **Part XII, the tenth part of ten**.
- `features-and-placement` figure 2: `ChunkG->>FS: featuresPerStep` drew
  `ChunkGenerator`'s memoised field (ChunkGenerator.java:88, :100) as a call
  into `FeatureSorter` on every chunk; it is read at :329.
- `features-and-placement`: *the chain above has used ten of them* — the chain
  has seven; ten is the page's count of modifiers named. Reworded.
- `jigsaw-and-templates` figure 1: `JS->>JPP: findGenerationPoint` —
  `JigsawStructure.findGenerationPoint` samples the start height and calls the
  static `JigsawPlacement.addPieces` (JigsawStructure.java:118–124), not the
  placer, which is built later inside the stub's consumer
  (JigsawPlacement.java:104–112, :149–158); the free-space shape is built there
  too, not after the stub by the placer.
- `jigsaw-and-templates` figure 1: *loop until the priority queue drains,
  depth within the limit* — a child at the limit is still queued
  (`depth + 1 <= maxDepth`, JigsawPlacement.java:377) and offered only the
  fallback (:263), which is the page's own opening; the loop runs until the
  queue drains.
- `jigsaw-and-templates` figure 1: `PESP->>STemp: placeInWorld` — the call is
  made by the pool element (`PoolElementStructurePiece.place` →
  `SinglePoolElement.place` → `StructureTemplate.placeInWorld`,
  PoolElementStructurePiece.java:96–101, SinglePoolElement.java:143–147); now
  labelled *through its pool element*.
- `trees` figure 1: `TF->>WGL: updateLeaves` — `TreeFeature.updateLeaves` is
  `TreeFeature`'s private static (TreeFeature.java:171, :181); `FoliageAttachments`
  is no class (`FoliagePlacer.FoliageAttachment`, :85); `leafRadius` is a local
  holding `FoliagePlacer.foliageRadius` (:69).
- `hand-built-structures` figure 1: `SPB-->>SStart: build` —
  `Structure.generate` calls `StructurePiecesBuilder.build` and constructs the
  `StructureStart` (Structure.java:94–95); the drain loop is
  `StrongholdStructure`'s (StrongholdStructure.java:38–45), the start piece's
  `addChildren` runs once before it (:37), and each new piece goes onto
  `StrongholdPieces.StartPiece`'s pending list (StrongholdPieces.java:189–190),
  not the builder's.
- `terrain`: *the two outer levels are where the sampling happens* — the cell
  row level samples nothing; the samples are at the cell column
  (`NoiseChunk.advanceCellX` → `fillSlice`, NoiseChunk.java:258) and the cell
  (`NoiseChunk.selectCellYZ` fills every *cache_all_in_cell* term,
  NoiseChunk.java:296–319). Reworded, and the figure's title *advanceCellX
  fills the next corner slice* is now a table row.
- `terrain` figure 1: SURFACE handing *a preliminary surface level* to
  CARVERS — the value is the `NoiseChunk`'s, computed during the noise fill
  (the page's own :100 and :187); the label is gone.
- `density-functions` figure 1: *as wrapped — the only form that runs*
  disagreed with the page's F3 readout paragraph; *a second visitor* for
  `NoiseChunk.forChunk` disagreed with the page's *second* visitor, which is
  the climate flattener — `RandomState`'s constructor runs two
  (RandomState.java:94, :95–119), so the per-chunk one is the third.
- `blending` figure 2: `Blender->>CM: isOldChunkAround` — `Blender.of` asks
  the `WorldGenRegion` (Blender.java:72), which asks `ChunkMap`
  (WorldGenRegion.java:106–107); now labelled *through the region*. The
  generator's self-message *wrap the biome resolver* is
  `Blender.getBiomeResolver` (NoiseBasedChunkGenerator.java:96), now an arrow.
- `blending` figure 1: *the final slide* — `NoiseRouterData.postProcess` wraps
  its argument named `slide` in `blend_density` (NoiseRouterData.java:224–225);
  *the final density* is the book's word.
- `creating-a-world` figure 2: the `MinecraftServer` lane received
  `new IntegratedServer`; the lane is now the object. `saveDataTag` is
  `LevelStorageSource.LevelStorageAccess`'s (LevelStorageSource.java:614,
  called at Minecraft.java:2233), not a message the disk receives; relabelled
  *level.dat, through a temp file*.

### Checked and found sound

- `features-and-placement` figure 1's order — block predicate before biome
  filter — is `trees_plains.json`'s shipped order; the code's
  `VegetationPlacements.treePlacement` with a sapling puts it after. Both
  ship, as the page says.
- `jigsaw-and-templates`: `getFirstFreeHeight` is asked exactly when not both
  pieces are rigid (JigsawPlacement.java:328–368).
- `hand-built-structures`: the builder is the accessor
  (`StructurePiecesBuilder.findCollisionPiece`, StructurePiecesBuilder.java:24),
  so the stronghold figure's label is right.

## Pass 7, session J — Part X · The client: the figures *(2026-09-15)*

Thirteen pages, 20 figures (18 before: `options`' one flowchart became two and
`text-and-fonts`' one eight-lane sequence became two). Every figure captioned
and every caption one italic run; the figure-name gate is **0 unresolved and 0
notes** for the part (was 10 and 26); nothing is below **0.776** or under
**12.4px** (was 0.59 and 9.5px, with six figures below 0.75 and three under
11px); no lane is over six; and **no Mojang name is broken on screen** —
fifteen were, more than any other part and more than a third of the corpus's
forty-one.

### Figures redrawn, and the orderings they assert

- **`sound-engine` figure 1** — eight lanes at 0.59 rebuilt as six in three
  `box`es (Render thread · Sound engine thread · Download pool). Asserts:
  `SoundEngine.play` calls `ChannelAccess.createHandle`, which posts to
  `SoundEngineExecutor` and returns a future the Render thread **joins**; the
  acquire runs on the sound thread as `Library.acquireChannel`;
  `ChannelAccess.ChannelHandle.execute` posts the parameters and, later,
  attach-and-play; and the continuation of
  `SoundBufferLibrary.getCompleteBuffer` belongs to **`SoundEngine`**, not to
  the buffer library. The server half (`ServerLevel`, `PlayerList`) is a
  **logged cut**: the page hands that story to `what-makes-a-sound` in its own
  second paragraph.
- **`the-client-level` figure 1** — the two one-lane notes became one `rect`
  band over all five lanes, asserting that the whole trace is inside one
  `Minecraft.runTick`. Three arrows re-derived; see *Corrections*.
- **`the-client-loop` figure 1** — a `Minecraft.runTick` subgraph now contains
  everything but `RenderSystem.pollEvents`. Asserts the boundary the page
  already argues twice in prose (each iteration is `pollEvents` then `runTick`;
  input lands in no profiler zone). The `DROP` node is folded into the clamp's
  yes-edge: it was a consequence drawn as a step, with an inbound and an
  outbound arrow, i.e. as something that runs.
- **`gui-and-screens` figure 1** — a flowchart of containment became a
  **`classDiagram`**, the book's eighth. Asserts `Gui` *holds* `Screen`,
  `Overlay` and `Hud`; `Screen` holds `AbstractWidget` and three typed lists;
  `AbstractContainerScreen` **extends** `Screen` and holds an
  `AbstractContainerMenu`; `Layout` only *positions* a widget (dashed). The old
  figure drew all four relations with one arrowhead. `ToastManager`,
  `ChatListener` and `SplashManager` are a **logged cut** — three names in one
  node that the page's prose says nowhere.
- **`gui-and-screens` figure 2** — two `rect` bands, asserting that everything
  that makes the screen exist happens in the tick that spends the key and
  nothing is drawn until the frame after. `Tutorial.onOpenInventory`, a
  `Tutorial` call drawn as a `Minecraft` self-message, is cut (a second object
  on that lane, and a name the prose never says); the `Gui` self-call is folded
  into the `setScreen` arrow it was already inside.
- **`the-gui-render-tree` figure 1** — the tree and the placement decision,
  drawn side by side with two dead-end boxes, are one picture. Asserts both
  outcomes land on a node **of the current stratum**: the fast path goes up one
  node with no intersection test, and the walk stops just above the highest box
  it touches and may not cross the barrier `GuiRenderState.nextStratum` set.
- **`the-gui-render-tree` figure 2** — a flat twelve-box chain became nested
  subgraphs. Asserts that pictures-in-picture, items, text,
  `GuiRenderState.sortElements` and `GuiRenderer.addElementToMesh` all run
  **inside `GuiRenderer.prepare`**, that `GuiRenderer.draw` is `prepare`'s
  sibling and not its successor, that the vertex-buffer upload sits between
  them, and that only `Gui.extractRenderState` and `GuiRenderer.endFrame` are
  outside `GuiRenderer.render`.
- **`text-and-fonts` figure 1** — the six stages, drawn as one unbroken chain,
  became two boxes. Asserts stages 1–3 run when the text changes and 4–6 inside
  `Font.prepareText`; the dotted edge from stage 2 to stage 4 stays.
- **`text-and-fonts` figures 2 and 3** — one eight-lane sequence split at the
  frame boundary its own notes named: four lanes before the frame, five in it,
  with two bands for record and draw.
- **`options` figures 1 and 2** — one fourteen-node, 2,081px flowchart split at
  the joint the page names. Figure 2 asserts that a **cycle saves on the
  click** and a slider at `OptionsSubScreen.removed`; see *Corrections*.
- **`prediction-and-acks` figure 1** — every edge label cut to the condition and
  qualified `Class.member`. Asserts both exits from *Retained* are the same call.
- **`input-and-keybinds` figure 1** — seven lanes to five, two bands. The
  screen's `keyPressed` now lands on a `Screen` lane rather than on `Gui`; the
  two-ends-of-a-screen's-life housekeeping is a **logged cut** from this figure
  (it has its own section, *The bulk operations, and their single callers*).
- **`debugging-the-running-game` figure 1** — a `box` per machine and full-width
  bands. Asserts the two-tick lag: the request is stored on the tick it arrives,
  the subscriber set read at the end of the next, the synchronizers woken on the
  one after. `ClientPacketListener` is a **logged cut** (a lane carrying two
  messages and deciding nothing); the packet reaches `ClientDebugSubscriber`
  through it as any packet does, which the caption says.
- **`what-makes-a-sound` figure 1** — door 3 now runs through
  `ClientLevel.playSeededSound` instead of past it; see *Corrections*.
- **`client/README` figure 1** — `TD` to `LR`, and the seven spokes numbered to
  the watch order (F13).

### Corrections — re-derived against the decompile before the fix

1. **`the-client-level`, figure 1**: `CPL->>LLE: applyLightData, then
   enableChunkLight, whose last act is setSectionRangeDirty over a 3x3 of
   columns`. Both `applyLightData` and `enableChunkLight` are
   **`ClientPacketListener`'s own private methods** — the caller's methods drawn
   arriving at the callee — and `enableChunkLight`'s last act is
   `this.level.setSectionRangeDirty(...)`, a call on **`ClientLevel`**, not on
   the light engine. Now two arrows: the light engine gets `setLightEnabled` and
   `updateSectionStatus`, `ClientLevel` gets `setSectionRangeDirty`.
2. **`the-client-level`, figure 1**: `CCC->>LX: onLightUpdate, then
   setSectionDirty`. `onLightUpdate` is **`ClientChunkCache`'s** own method;
   what it calls on the extractor is `setSectionDirty`. Head corrected.
3. **`the-client-level`, prose**: the page never said whether the light was one
   arrival or two. It is **one**:
   `ClientPacketListener.handleLevelChunkWithLight` queues a single lambda that
   runs `applyLightData` and then, if the chunk is there, `enableChunkLight`.
   Said now.
4. **`options`, figure 1**: the cycle path ran through
   `Screen.removed — Options.save`. A cycle button calls `Options.save` **in its
   own click handler**, before the value-changed listener
   (`OptionInstance.CycleableValueSet.createButton`); `Screen.removed` is where
   a *slider* saves. Redrawn as two entrances to one exit.
5. **`options`, figure 1**: `Screen.onClose` and `Screen.removed`.
   `Screen.removed` is an empty base method; the one that saves is
   **`OptionsSubScreen.removed`**, and `OptionsSubScreen.onClose` is what
   applies an armed timer. The page's prose already had it right. Corrected.
6. **`what-makes-a-sound`, figure 1**: door 3 (your own place and break) went
   straight to `SoundManager.play`, bypassing `ClientLevel.playSeededSound` —
   while its own box said *the same shared call*. It does **not** bypass it:
   `ClientLevel.playSeededSound` plays only when the excluded entity *is* the
   local player, which is exactly why one method serves the packet and the local
   call. Rewired to converge with door 1, which is the page's argument.
7. **`sound-engine`, figure 1**: `SBL-->>ChanA: thenAccept, then
   ChannelHandle.execute — attachStaticBuffer, play`. The continuation is
   `SoundEngine`'s own lambda, inside `SoundEngine.play`; `SoundBufferLibrary`
   calls nothing on `ChannelAccess`. Split into two arrows.
8. **`sound-engine`, figure 1**: `CPL->>CL: handleSoundEvent, then
   playSeededSound`. `handleSoundEvent` is the **listener's** method; the
   callee's is `playSeededSound`. Dropped with the lane.
9. **`sound-engine`, figure 1**: `SL->>SL: BlockItem.place` — `BlockItem` as a
   second object on the `ServerLevel` lane; and `PL-->>CPL:
   ClientboundSoundPacket` drawn as mermaid's **dashed reply arrow** for a packet
   crossing between two machines. Both cut with the server half.
10. **`hud`, figure 2**: `CPL->>LP: handleSetHealth — hurtTo`.
    `handleSetHealth` is `ClientPacketListener`'s; the callee's method is
    `LocalPlayer.hurtTo`. Head corrected; the caller's method is named in the
    caption, where it belongs.
11. **`prediction-and-acks`, figure 2**: `MPGM->>CL: performUseItemOn, then
    ItemStack.useOn, then setBlock`. `performUseItemOn` is **`MultiPlayerGameMode`'s
    own private method**; the chain's only `ClientLevel` call is `setBlock`.
    Reordered so the head is the callee's.
12. **`input-and-keybinds`, figure 1**: `keyDebugModifier` drawn as a
    `KeyboardHandler` member. It is **`Options.keyDebugModifier`** —
    `KeyboardHandler.keyPress` reads `options.keyDebugModifier`. Qualified.
13. **`input-and-keybinds`, figure 1**: `screen keyPressed` drawn arriving at the
    **`Gui`** lane. `keyPressed` is a `Screen` method; `Gui` is only where the
    screen is reached from. The figure gained a `Screen` lane and lost two
    others. (`Minecraft.handleGlobalKeyPress`, which a viewer suspected of being
    invented, is **real and correctly placed** — `KeyboardHandler.keyPress`
    calls `this.minecraft.handleGlobalKeyPress(...)`.)
14. **`text-and-fonts`, prose**: "why stage six alone is left for the draw
    pass". Stage six — the emit into a `Font.PreparedText` — runs **inside
    `Font.prepareText`**, at record time. What waits for the draw pass is the
    *expansion* of that finished object into one `GlyphRenderState` a glyph,
    which is after stage six, not stage six. Reworded.
15. **`text-and-fonts`, figure 2**: `CRU->>FBR: Language.getVisualOrder(line)` —
    `getVisualOrder` is `Language`'s, and `FormattedBidiReorder`'s own method is
    the static `reorder`. Head corrected, the route kept in the label.
16. **`debugging-the-running-game`, figure 1**: three self-messages naming a
    third class's method on a lane that owns neither —
    `ServerPlayer.requestDebugSubscriptions` on the `SGPL` lane (the handler is
    `ServerGamePacketListenerImpl.handleDebugSubscriptionRequest`),
    `Mob.registerDebugValues` on the synchronizer's, and a `Gizmos` call on the
    renderer's. The first two corrected; the third kept, `Gizmos` being a static
    façade the renderer calls, and named as such.
17. **`the-gui-render-tree`, figure 2**: the flat chain asserted that
    pictures-in-picture, items, text, the sort and the mesh happen *after*
    `GuiRenderer.prepare`, and that `GuiRenderer.draw` happens after them. All
    five are inside `prepare`; `draw` is its sibling. Also missing: the
    vertex-buffer upload between the two. Redrawn as nesting.
18. **`sound-engine`, prose**: a stray `'` after a link, which rendered.

### Claims introduced

Every caption listed above is a claim about what its figure shows. Beyond them,
four prose additions this session made to give figure-only names their sentence
(F6), each to be checked like any other claim: `the-client-loop`'s paragraph on
the four methods that appear only in the figure — the two-call drain, and that
`SoundManager.updateSource` and `MouseHandler.handleAccumulatedMovement` run
after the ticks and before the frame; `hud`'s paragraph naming the seven steps
of the heart pass and which fields `LocalPlayer.hurtTo` touches;
`debugging-the-running-game`'s paragraph naming the figure's methods in its
order; and `options`' two, asserting that the save asymmetry comes from
`OptionInstance.CycleableValueSet.createButton` carrying `Options.save` while
`OptionInstance.SliderableValueSet` carries no such call anywhere, and that
`ClientPacketListener.broadcastClientInformation` compares against the last
`ClientInformation` sent and sends nothing when they match — which the figure
had always drawn and the prose had never said.

### Tool blindness — the tenth of the pass, and the second the standard created

`tools/pass7_figures.py` closed a `<br/>` up **only on a `participant` line**
and turned it into a space everywhere else. F17 rules the break for a lane;
**F18 sends every part session to break a name in a message or node label the
same way** — so each repair a session made split one Mojang name into two
halves and counted both as *names the prose never says*. The measurement got
worse every time a session fixed a figure, and the two tools disagreed about
the same label: `check_figure_names.py` has read the break correctly since
session I. `pass7_figures.py` now uses session I's own reading — a name break is
at a CamelCase boundary or at a dot and nowhere else — with two probe cases that
fail on the old behaviour. Part X's *never in prose* count fell by fourteen on
the re-measure with no page changed: those were never names.

## Pass 7, session I — Part IX · Networking: the figures *(2026-09-15)*

Six pages, 11 figures (12 before: `packets-and-stream-codecs`' buffer flowchart
became a table). Every figure captioned, every caption one italic run; the
figure-name gate clean on the part (**1 unresolved name → 0, 19 notes → 0** —
the third part clean on both); **no figure below 0.77 and no type under
12.3px**, from three figures at 0.38–0.54 with 6–8.6px type; no overlap,
overflow, clipping or edge through a node anywhere in the part; **no Mojang
name hyphen-broken on screen** (5 lines were). One figure is still over
1,200px tall and that is deliberate: `what-the-client-is-told`'s cascade is
the page's own artefact, and splitting it at the joint would destroy the one
picture the page says *is* the page.

**The part-wide fault is F7's, in the mirror image of session H's.** Session
VIII's pages gave *one object two lanes*; Part IX's give **two objects one
lane**, because the part's subject is two machines running the same classes.
`the-connection` drew one `Connection` lane for the object at each end — and
the paragraph under it *conceded the fault in words* ("which is what the note
across the middle says and the picture cannot") rather than the figure being
redrawn — and `chat-and-signing` drew two lanes both labelled
`ClientPacketListener`, told apart by a note naming two mermaid aliases that
appear nowhere in the rendered picture. Both are fixed the way pass 5's
`authority` and `synched-entity-data` were: a second lane row for the same
class, and a `box` per machine.

**Three of the four figures on `protocol-phases` were illegible for one
reason: `direction LR`.** At 0.54, 0.38 and 0.42 with 6–8.6px type, they were
the three worst figures in the part, and two of the three fixes were *deleting
one line*. F3 already says `TD` for anything ordered in time; a state machine
is ordered in time, and a state diagram's default is `TB`. The lesson for the
sessions after this one: on a state diagram or a chain of stages, the direction
line is worth checking before any label is shortened.

### The figures redrawn, and what each asserts

- **`networking/README`, figure 1** — the two subgraph titles were being
  clipped on screen (mermaid draws only the first wrapped line of a title), so
  the figure's whole argument — the 3 + 2 split — was the only thing a reader
  could not read. Titles shortened to *the wire, three times* and *inside the
  play phase*; the five nodes numbered to the watch order (F13); the
  fourteen-word edge label from the wire group to the pair became the caption,
  and the arrow re-anchored from the group `W` to lecture **3**, which is what
  the prose says ("the last two both sit inside the final language").
  **Asserts**: lectures 1 → 2 → 3 in that order, and that 4 and 5 run inside
  the phase lecture 3 ends on.
- **`the-connection`, figure 1** — redrawn. Six lanes in **two `box` groups**,
  one per machine; the `Wire` relay lane removed and the crossing drawn
  encoder → decoder; the return leg drawn right-to-left as one labelled arrow;
  the two drains marked with `rect` bands (F8). 16 messages → 11, 1,580px →
  1,141px. **Asserts**: `Connection.send` on the client's main thread;
  `sendPacket` joining the Netty loop; one whole frame from the client's
  `PacketEncoder` to the server's `PacketDecoder`; `channelRead0` at the tail
  of the pipeline; `shouldHandleMessage` then `Packet.handle`;
  `ensureRunningOnSameThread` queuing and aborting; the second
  `shouldHandleMessage` inside the drain; the reply written and not flushed;
  `Connection.tick` flushing; the client's drain once per frame.
- **`the-connection`, the pipeline table** — not a figure, but the figure's
  removed note went here: a fourth column, *its outbound mirror*, so the
  reverse order is read off the table instead of out of an eight-item
  sentence. **Asserts**: five of the nine inbound handlers have an outbound
  mirror and four do not.
- **`packets-and-stream-codecs`, figure 1** — the build chain cut at the
  `ProtocolInfoBuilder.addPacket` line, one subgraph either side, named for
  what each half knows (*knows chat, not ids* / *knows ids, not chat*) — which
  is the sentence directly under the figure. 1,900px → 902px. **Asserts**: the
  two fields' codecs compose into the packet's `STREAM_CODEC`; one `addPacket`
  call pairs it with a `PacketType`; `StreamCodec.mapStream` wraps it at bind;
  the `IdDispatchCodec` holds the wrapped entry — **and the caption states
  that this is build order and that at send time the dispatch codec runs
  outermost**, which is what `IdDispatchCodec.encode` does
  (`net/minecraft/network/codec/IdDispatchCodec.java:47`).
- **`packets-and-stream-codecs`, figure 2** — cut, replaced by a three-row
  table. **Asserts**: status serverbound binds the identity function, four
  phases bind `FriendlyByteBuf` at class-load, play binds
  `RegistryFriendlyByteBuf` per connection at the switch into play.
- **`protocol-phases`, figure 1** — `direction LR` removed; 0.54 → 1.00.
  **Asserts**: unchanged from the figure it replaces.
- **`protocol-phases`, figure 2** — `direction LR` removed, labels cut to the
  packet that causes each transition, and `NEGOTIATING` taken out. 0.38 → 1.00.
  **Asserts**: the same ten transitions as before, none added, removed or
  reversed.
- **`protocol-phases`, figure 3** — the `Auth` lane, which was labelled *User
  Authenticator thread* and yet received the **client's** `joinServer` call,
  is now a `Sess` lane for the session service both machines call, with the
  thread named in each message instead; the two listeners are in a `box` each.
  **Asserts**: the client calls `joinServer` before it sends the key packet;
  the server installs both ciphers on receiving it; the server calls
  `hasJoinedServer` after that.
- **`protocol-phases`, figure 4** — redrawn `TD` with the five queued tasks in
  a `the serial queue` subgraph, the three out-of-queue packets above it, and
  the **client round trip** that ends the phase drawn as two arrows.
  0.42 → 1.00. **Asserts**: the three packets precede the queue;
  `SynchronizeRegistriesTask` is first and the two optional tasks follow it;
  `PrepareSpawnTask` then `JoinWorldTask`; `ClientboundFinishConfigurationPacket`
  out and `ServerboundFinishConfigurationPacket` back before the player is
  built.
- **`chat-and-signing`, figure 1** — three `box` groups (the sender's client,
  the server, every recipient's client), the normalisation moved to a
  self-message on `ChatScreen`, `sendChat` on the arrow to the listener, and
  the Server-thread note replaced by a `rect` band bounded to the two server
  lanes. **Asserts**: `ChatScreen.normalizeChatMessage` is the sender's own
  work, not the listener's; the band covers the unpack, the filter-and-decorate
  and the broadcast and nothing on the recipient's machine.
- **`chat-and-signing`, figure 2** — redrawn **by outcome** rather than by
  order: all five Netty-thread checks in one diamond, the Server-thread unpack
  in another, and three terminals, with *the message dies* reached from both.
  **Asserts**: the window checks and the character check close the connection;
  the chat-visibility refusal kills the message only; no signature or an
  expired key kills the message; out of order or an invalid signature kills the
  chain.
- **`what-the-client-is-told`, figure 1** — the tail below gate 3 cut (it is
  the table's job, and see the correction below), the labels cut to the
  budget, and the three gates left as the cascade. 18 nodes → 13, 2,644px →
  1,740px. **Asserts**: `ChunkMap.tick` walks every tracked entity; a section
  change re-tests every player; gate 1 is a conjunction and gates 2 and 3 are
  disjunctions; three feeds skip gate 3.
- **`what-the-client-is-told`, figure 2** — captioned, and the word *veto*
  removed from the self-message, because the paragraph 30 lines below exists
  to say `Entity.broadcastToPlayer` is **not** a hiding hook.

### Corrections — re-derived against the decompile before the fix

- **`protocol-phases`, the terminal-packet count.** The page said "Seven
  packets in the game carry the terminal flag, and **six of them are on this
  diagram**; `ClientIntentionPacket` is the seventh." `ClientIntentionPacket`
  labels **two** of the diagram's arrows. The seven classes that override
  `Packet.isTerminal` to return true are `ClientIntentionPacket`,
  `ClientboundLoginFinishedPacket`, `ServerboundLoginAcknowledgedPacket`,
  `ClientboundFinishConfigurationPacket`, `ServerboundFinishConfigurationPacket`,
  `ClientboundStartConfigurationPacket` and
  `ServerboundConfigurationAcknowledgedPacket` — every one of them on the
  figure. Now reads "every one of them labels an arrow above.
  `ClientIntentionPacket` labels two".
- **`protocol-phases`, `returnToWorld` drawn as a queue entry.** The figure had
  `returnToWorld appends the last two` as the **fifth step** of the chain,
  after the resource-pack task. `ServerConfigurationPacketListenerImpl.returnToWorld`
  (`net/minecraft/server/network/ServerConfigurationPacketListenerImpl.java:104`)
  appends `PrepareSpawnTask` and `JoinWorldTask` and calls `startNextTask`, and
  it is called from the **last line of `startConfiguration`** (:101), before
  any task has run. A queue-building call drawn as a queue entry; the box is
  gone and the queue is a subgraph.
- **`protocol-phases`, the unlabelled arrow at the end of configuration.** The
  `JoinWorldTask → handleConfigurationFinished` arrow looked like the six
  before it. `handleConfigurationFinished` (:166) runs on the client's
  `ServerboundFinishConfigurationPacket`, so the arrow was a round trip drawn
  as a step — and the page's own hook, the server holding a ticket on chunks
  for a player that does not exist, lives in exactly that gap. Now two arrows
  through a client node, and the gap is the caption's subject.
- **`chat-and-signing`, "two of those five close the connection".** Four do:
  the three window checks and the character check
  (`ServerGamePacketListenerImpl.tryHandleChat`,
  `net/minecraft/server/network/ServerGamePacketListenerImpl.java:1829`,
  disconnects on `isChatMessageIllegal` and the page's own table marks the
  three window rows **connection**); the chat-visibility refusal is the only
  one of the five that does not, and it sends a red system line instead
  (:1832). The sentence was counting the old figure's *diamonds*, which
  collapsed the three window checks into one.
- **`chat-and-signing`, the caller's method on the callee's arrow.** The
  `ChatScreen → ClientPacketListener` arrow was labelled "whitespace squeezed,
  cut to 256 characters", which is `ChatScreen.normalizeChatMessage`'s own work
  (`net/minecraft/client/gui/screens/ChatScreen.java:359`, called at :344
  before `connection.sendChat` at :353). The eighth part of eight to carry this
  fault. Now a self-message on `ChatScreen`, and the arrow says `sendChat`.
- **`chat-and-signing`, the Server-thread note's reach.** "everything below is
  a task queued on the Server thread" spanned the rest of the diagram,
  including the recipient client's own work, which the page's cast table puts
  on the Render thread. The band now covers the server's two lanes only.
- **`what-the-client-is-told`, position drawn as a binary.** The figure's `D1`
  node made every opened gate 3 send either a relative or an absolute position
  packet. The page's own table names two further outcomes: **nothing sent**
  inside `ServerEntity.TOLERANCE_LEVEL_POSITION` and
  `ServerEntity.TOLERANCE_LEVEL_ROTATION`, and **rotation only** for a
  passenger. An omission the drawing turned into a claim; the tail is cut and
  the table owns the outcomes.
- **`the-connection`, "the connection phase flushes the channel".** The page
  has no such term. `Connection.tick`
  (`net/minecraft/network/Connection.java`, `public void tick()`) calls
  `flushQueue`, ticks a `TickablePacketListener`, and then calls
  `channel.flush()`. The note names `Connection.tick`, which the page does
  define, 235 lines below.
- **`the-connection`, `processQueuedPackets` in a note.** A real method
  (`net/minecraft/network/PacketProcessor.java:35`) and a spelling the page's
  prose never uses — it says `PacketProcessor` and *the drain*. The note now
  says both of those.

### The tool blindnesses — the eighth and ninth of this pass

- **`check_figure_names.py` read only the first 20,000 characters of a class
  file to find what it extends.** Exactly one class in the decompile declares
  itself past that mark — `ClientPacketListener`, at byte 21,133, behind three
  hundred import lines — and it is one of the most-used lanes in the book. So
  the gate believed `ClientPacketListener` extended nothing, and **every
  inherited member on a `CPL` lane failed**: `shouldHandleMessage`, which
  `ClientCommonPacketListenerImpl` overrides
  (`net/minecraft/client/multiplayer/ClientCommonPacketListenerImpl.java:145`),
  was reported as a bad name on a figure that was right. Fixed by reading the
  whole file, with a probe case that is exactly this class and this member.
  Corpus failures 31 → 30.
- **A `<br/>` between a name and the next word welded them.** Sessions B and D
  taught the gate to close up a break *inside* a name and to split one *after
  punctuation*; nobody had told it that `ensureRunningOnSameThread<br/>queues
  the pair` is a name meeting a word. It read `ensureRunningOnSameThreadqueues`
  and failed the page — the fix F18 itself prescribes made the gate fail.
  The rule is now F17's own wording: **a name break is at a CamelCase boundary
  or at a dot, and nowhere else**, so a break followed by a lower-case letter,
  or one whose preceding word is all lower-case, is a line break. Three probe
  cases; corpus **notes 166 → 148** and no previously-clean part moved.

## Pass 7, session H — Part VIII · The player: the figures *(2026-09-15)*

Eight pages, 12 figures (10 before; `input-to-movement`'s single trace became a
client figure and a server figure at the wire, and `status-effects`' single
trace became a server figure and a client figure at the machine boundary its
own heading names). Every figure captioned, every caption one italic run; the
figure-name gate clean on the part (1 unresolved name → 0, 7 notes → 0); no
type under 12.8px, nothing below 0.80, nothing over 1,200px tall, no lane over
six, **no Mojang name hyphen-broken on screen**, and no overlap, overflow or
clipping in the part. One flowchart became the book's **seventh `classDiagram`**.

### The figures redrawn, and what each asserts

- `player/README` — the part figure is numbered 1–7 to the watch order (F13)
  and captioned to say what an arrow means. **No arrow added, removed or
  reversed.** Two edge labels that described a *node* ("eight classes,
  forty-three slots" on `PA → TT`; "and two other melee paths" on `SS → SP`)
  moved into the nodes they describe, and the one edge that carries a real
  constraint is now the only labelled one — the claim being the section's own
  sentence, that the four branches off *the two-phase tick* are independent of
  one another and the spear is the sword swing's sequel.
- `player-anatomy` figure 1 — the inheritance tree was a `flowchart TD` whose
  solid arrow meant *extends*, a mark outside `TEMPLATE.md`'s table. It is now a
  `classDiagram` with `<|--`, which says *extends* natively. **No relation
  added, removed or reversed**: the nine edges are the same nine. What is new is
  the `<<abstract>>` annotation on `Entity`, `LivingEntity`, `Avatar`, `Player`
  and `AbstractClientPlayer` — five claims, each checked at the class
  declaration (all `public abstract class`) — and the caption's claim that the
  five unmarked boxes (`ServerPlayer`, `LocalPlayer`, `RemotePlayer`,
  `Mannequin`, `ClientMannequin`) are the only ones the game instantiates, each
  checked as `public class`. **Correction to the prose:** the lead said "six
  rungs … stand **between** `Entity` and the object on your own screen, and five
  between `Entity` and the one the server holds", while the counts are inclusive
  and the figure shows four and three strictly between; now "six rungs … reach
  **from** `Entity` **down to** …".
- `the-two-phase-tick` figure 1 — eight lanes to six, 0.61/9.7px to
  0.82/13.1px. **Lanes folded:** `Player` (a `ServerPlayer` *is* a `Player`, so
  one object had two lanes — F7) and `Inventory` (one message, and
  `player-anatomy` owns the forty-three slots). **Devices added:** two `rect`
  bands with a `Note over` all lanes, replacing two `Note over` a *single* lane
  that left half the figure unmarked. **Arrow added — and it is a correction:**
  `SP->>ACM: stillValid` in phase two. The page says in bold that the container
  check "is the only work both halves do" and the figure showed it in phase one
  only; `ServerPlayer.doTick` re-runs `this.containerMenu.stillValid(this)`
  (`ServerPlayer.java:729`). **Name corrected:** the inventory message named
  `ItemStack.inventoryTick`, which appears nowhere in the page's prose (the
  prose says `Inventory.tick`); the lane is gone with it. The label
  `absSnapTo(firstGood)` is now `absSnapTo — back to firstGood`, because the
  fields are `firstGoodX`, `firstGoodY`, `firstGoodZ` and there is no
  `firstGood`.
- `input-to-movement` figures 1 and 2 — one seven-lane trace spanning both
  machines became a five-lane client figure and a three-lane server figure,
  split at the wire, each in the section that owns it (the server half had been
  drawn ninety lines above the section that explains it). 0.69/11.1px to
  0.92/14.7px and 1.00/16px. **Lane cut:** `LivingEntity` — `LocalPlayer`'s own
  base class, one arrow, no cast row (F7). **Arrow corrected:** `KI->>LP:
  applyInput` drew `KeyboardInput` calling `LocalPlayer.applyInput`; the caller
  is `LivingEntity.aiStep` on itself (`LivingEntity.java:3250`), so it is a
  self-message. **Arrow added:** `KI->>KM: isDown, once for each of seven
  mappings` — `KeyboardInput.tick` reads `this.options.keyUp.isDown()` and six
  more (`KeyboardInput.java:21`), which is what makes `KeyMapping` a lane that
  decides something rather than one that carries a single message. **Head
  corrected:** `KH->>KM: keyPress` labelled the message with the *caller's*
  method; `KeyboardHandler` calls `KeyMapping.set` then `KeyMapping.click`
  (`KeyboardHandler.java:638-639`). **The server figure asserts** the branch
  structure of `ServerGamePacketListenerImpl.handleMovePlayer` as an `alt` /
  `opt`: the speed failure teleports and returns
  (`ServerGamePacketListenerImpl.java:1270-1271`), and the rubber-band is
  optional after the move is applied (`…:1309`) — the page's own disjunction,
  drawn as conditional for the first time. Two `rect` bands assert that the
  drain and the connection phase are different phases of one server tick, which
  is the page's numbered list at *Sampled once a tick*.
- `the-sword-swing` figure 1 — seven lanes to six, in two `box transparent`
  machines, 0.69/11.0px to 0.80/12.8px. **Three corrections, all arrows:**
  (1) `SGPL->>SGPL: isWithinAttackRange` drew the listener calling its own
  method — it is `this.player.isWithinAttackRange(…)`
  (`ServerGamePacketListenerImpl.java:2031`), declared on `Player`
  (`Player.java:2009`), and the `Player` lane was already in the figure;
  (2) `Player->>LE: hurtOrSimulate` landed on a `LivingEntity` lane, but the
  method is `Entity.hurtOrSimulate` (`Entity.java:2044`) and the page's own
  Reference link is *Damage outside `LivingEntity`* — the lane is now `Entity`;
  (3) `SL->>MC: ClientboundDamageEventPacket` drew the packet arriving at
  `Minecraft`, and the handler is `ClientPacketListener.handleDamageEvent`
  (`ClientPacketListener.java:1287`) — the receiving lane is now `CPL`, and the
  sender is the hurt entity, whose own path calls `Level.broadcastDamageEvent`
  (`LivingEntity.java:1306`). **Node added:** `ServerLevel.getEntityOrPart` as a
  self-message, the one `ServerLevel` fact the prose gives and the figure had
  dropped when it dropped the lane. **Label corrected:** `hurtOrSimulate — into
  Part VI; returns was-anything-damaged` carried a cross-part reference inside a
  message.
- `the-sword-swing` figure 2 — the damage walk. **The gate is a diamond** with
  both terms named and its answers on its edges (`baseDamage > 0.0F ||
  magicBoost > 0.0F`, `Player.java:941`), where it had been a rectangle asking
  "either term above zero?" without saying which two. **Node added:** the sprint
  knockback step (`Player.java:945-951`), which the prose already ties the item
  bonus to ("it is the step the item bonus is added immediately after") and
  which the figure did not contain — so the sentence pointed at a node that was
  not there. **Node added:** *nothing below runs*, the gate's own else. **Fact
  moved to prose:** "or the riptide value while auto-spinning" left the base
  node for a sentence naming `Player.autoSpinAttackDmg` (`Player.java:932`) —
  F6, a name the prose never said. **Correction to the prose:** "the item-bonus
  node in the figure **below**" — the figure is above it.
- `the-spear` figure 1 — **name corrected:** `Action.STAB` was the gate's one
  unresolved name in the part; `Action` is a nested enum and the prose writes it
  `ServerboundPlayerActionPacket.Action.STAB`
  (`ServerboundPlayerActionPacket.java:68-70`), which the figure now does.
  **Label corrected:** "every use tick: ItemStack.onUseTick, server side only"
  said the wrong thing about the wrong method — `ItemStack.onUseTick` runs on
  both sides and only the divert to `KineticWeapon.damageEntities` is behind
  `!level.isClientSide()` (`ItemStack.java:1179-1180`); *server side only* now
  sits on the `damageEntities` node. **Label corrected:** "startUsingItem for
  72000 ticks" put the number on the wrong method — 72000 is
  `Item.getUseDuration`'s, which the prose says. **Node added:** the ordinary
  attack handler's refusal of a piercing weapon
  (`ServerGamePacketListenerImpl.java:2033`) — the second of the two things the
  prose says the picture is worth stopping on, and the only thing the *no*
  branch had to end in. The decision is a diamond; five unqualified members are
  qualified.
- `hunger-and-experience` figure 1 — the regeneration chain. **The shape is the
  correction:** three sibling branches off one node drew a *set* where
  `FoodData.tick` is an if / else-if chain tested in order
  (`FoodData.java:50-77`), which is what makes the three exclusive and why a
  full bar heals six times faster than one at eighteen. Now three numbered
  diamonds, each reached only by the one above saying no. **Node added:** the
  fourth branch, `else { this.tickTimer = 0; }` (`FoodData.java:75-76`), which
  the figure had never drawn. Four sentence labels moved to a four-row table
  beside it; the game rule's asymmetry (branches 1 and 2 gated on
  `GameRules.NATURAL_HEALTH_REGENERATION`, branch 3 not) is a table column.
- `hunger-and-experience` figure 2 — seven lanes to six in two `box
  transparent` machines, 0.69/11.1px to 0.80/12.8px. **Lane folded:**
  `LivingEntity` and `ServerPlayer` were one object in this scenario (F7).
  **Ordering corrected in the drawing, not the fact:** the entity event was
  labelled *sent first* and drawn second, from a lane that had not acted;
  `ServerPlayer.completeUsingItem` sends `ClientboundEntityEventPacket(9)`
  *before* `super.completeUsingItem()` (`ServerPlayer.java:1706-1710`), so it is
  now drawn where it happens. **Arrow added:** the client's re-run of the same
  walk, unguarded — the section's own surprise ("the client replays the meal …
  and runs `FoodProperties.onConsume` and its `FoodData.eat` locally, with no
  side guard"), which the figure had omitted while drawing a
  `ClientPacketListener` lane that never acted.
- `status-effects` figures 1 and 2 — one trace with **one `LivingEntity` lane
  standing for two machines**, told apart by two `Note over` lines, became two
  figures, one per machine, both at 1.00/16px. **Lane cut:**
  `AttributeInstance` — the modifier's landing is `attributes`' in Part VI, and
  the page links out to it. **Arrow added, and it is the page's central fact:**
  the 600-tick correction. `LivingEntity.onEffectUpdated` fires when the
  remaining duration divides by six hundred and `ServerPlayer.onEffectUpdated`
  sends `ClientboundUpdateMobEffectPacket` (`ServerPlayer.java:1794-1796`); the
  opening paragraph and the first *Questions players ask* answer both rest on it
  and no figure showed it. **Arrow added:** `CPL->>LE: forceAddEffect — a fresh
  instance, with nothing under it`, checked at
  `ClientPacketListener.java:1876-1882`, where the instance is built with a
  `null` hidden effect. **The client figure has no `MobEffect` lane**, which is
  the claim the caption makes and the page's thesis. Re-derived and **kept**:
  "four flag bits" (`FLAG_AMBIENT`, `FLAG_VISIBLE`, `FLAG_SHOW_ICON`,
  `FLAG_BLEND`, `ClientboundUpdateMobEffectPacket.java:14-17`) and
  `MobEffect.addAttributeModifiers` called from `LivingEntity.onEffectAdded`
  behind `!this.level().isClientSide()` (`LivingEntity.java:1113-1117`).

### The captions

Twelve captions, each a claim about what its figure shows and each written this
session; the load-bearing ones are `the-two-phase-tick`'s ("the only lane the
first band and the second both touch"), `status-effects` figure 2's ("there is
no `MobEffect` lane here, and that absence is the page"),
`hunger-and-experience` figure 1's ("a chain, not a fan"), `the-sword-swing`
figure 2's (the left branch scaled once and left alone, the right one scaled,
gated, added to and multiplied) and `player-anatomy`'s (the five unmarked boxes
are the only ones the game instantiates).

### Two tool blindnesses, with probes

`check_figure_names.py` could not see a one-word class name anywhere but a
`participant` line (its `CAMEL` token needs two humps), and its `CLASS_REL`
never matched `<|--` at all, so an inheritance relation's ends and label were
unread. Both fixed with probe cases; corpus-wide the gate now checks 43 more
names and three more classes reach the index, and **no previously-clean part
moved on failures**. Nothing already in the corpus was found wrong by either
fix — but `player-anatomy`'s new class diagram has ten class names in it that
the gate would not have read at all.

## Pass 7, session G — Part VII · Items and inventories: the figures *(2026-09-15)*

Nine pages, 19 figures (17 before; `using-an-item`'s single *ending* flowchart
became two, `recipes`' one trace became two at the tick boundary it already
drew, `containers-and-menus`' seventeen-node ladder became a four-row table and
a five-node fork, and `loot-tables`' twenty-six-node funnel lost its placement
tail to the trace above it). Every figure captioned, every caption one italic
run; the figure-name gate clean on the part (10 unresolved names → 0, 31 notes
→ 1, the one ruled below); no type under 12.6px, nothing below 0.79, no lane
over six, no flowchart over fourteen nodes, **no Mojang name hyphen-broken on
screen** and no overlap, overflow or clipping anywhere in the part.

### The figures redrawn, and what each asserts

- `items/README` — the part figure gains two subgraphs (*the vocabulary*, *the
  three engines*) and its eight nodes are numbered to the watch order. **No arrow
  added, removed or reversed**: the six edges and their sentences are the page's
  own, unchanged. The claim the subgraphs assert is the section's own sentence
  ("What is left is **two tiers**"), drawn rather than only said. The queue's
  standing request for an `EC → LO` edge (:4491) is **ruled out**: the prose says
  the engines lean on the vocabulary and not on each other, and an arrow here
  means *what the next page can now assume*, which loot tables does not owe
  enchanting.
- `items-and-stacks` figure 1 — the flowchart is now the book's **sixth
  `classDiagram`**, and it is the shape the section's heading promised (*Four
  fields*). `count` and `popTime` were edgeless boxes in a subgraph whose title
  was **clipped mid-phrase on screen** (*ItemStack — the object in*); they are
  now fields of the `ItemStack` box. **Arrows removed**: `PDM --> PATCH` (the
  patch internals, which Part II's `data-components` owns since session B).
  **Arrows kept, re-parented**: `ItemStack --> Holder.Reference`, `Holder.Reference
  --> Item`, and the dotted `PatchedDataComponentMap ..> Holder.Reference`
  labelled *reads the defaults, never writes them* — the page's thesis arrow,
  whose label had drifted onto the neighbouring solid edge in the render. The
  `Item` box lists the four fields the opening paragraph names, verified at
  `Item.java:120-123`, and the `ItemStack` box the four at `ItemStack.java:123-128`.
- `containers-and-menus` figure 1 — the `ContainerSynchronizer` lane **cut**
  (seven lanes → six), and with it the two arrows that drew *the absence of a
  packet as a packet*. **Correction, not a simplification**: `RemS-->>CSync:
  nothing, sendSlotChange is never reached` named the wrong caller —
  `ContainerSynchronizer.sendSlotChange` is called by
  `AbstractContainerMenu.synchronizeSlotToRemote`
  (`AbstractContainerMenu.java:300-307`), never by a `RemoteSlot`. Both are now
  one note asserting that the synchronizer is not reached in the agreeing case.
  A `rect` band marks the server tick that drains the packet (F8); `matches?`
  is `matches`, the form the prose uses; *predicted on the twin* is *on the
  client's own copy*, the page's own phrase.
- `containers-and-menus` figure 2 — split at `IX -->|passes|`. The four gates are
  a two-column table (*the test* · *what a failure does*), and the figure is the
  five nodes the section is actually about. **Nodes removed**: `BC` → `AG` →
  `SIL` / `ONE`, which redrew figure 1's ending. **Correction**: the figure drew
  **six** decision diamonds under a sentence that calls the handler *four tests
  and a fork* — `RemoteSlot.matches` is inside `AbstractContainerMenu.broadcastChanges`
  and not in the handler at all (`ServerGamePacketListenerImpl.handleContainerClick`,
  four tests then one `fullResyncNeeded` fork). The sentence pointing at "the
  order of the last two boxes" now points at a figure whose last two boxes are
  the ones it means.
- `contexts-and-predicates` figure 1 — **`LCtx -->|getParameter and
  getOptionalParameter| Users` reversed and then cut**: the users call the
  context (`DamageSourceCondition.java:31-32`), and the five of them belong to
  *What reads a context*, 180 lines below. `SlotSource` **cut**: declared outside
  both subgraphs, mermaid drew it *inside* the loot box, contradicting its own
  label (*in world/item/slot*). **Arrows added**: `Callers --> ContextKeySet`
  (*each brings its own key set*) and `SlotDisplayContext --> ContextMap`
  (*builds a ContextMap of its own*) — both the section's own sentences
  ("everything *above* them is whoever wants a question answered… and, on the
  *client*, `SlotDisplayContext`, which builds a `ContextMap` of its own"). The
  loot subgraph is gone and its two nodes carry the `server` class instead: its
  title was being drawn over the arrow entering it.
- `contexts-and-predicates` figure 2 — `CMap-->>LootP` **relabelled** from
  *throws on an unexpected key, or on an absent required one* to *the checked
  map, or a throw on a bad key*: the old label drew a conditional throw as an
  unconditional return, against the prose's three-moments account.
- `enchanting` figure 1 — the five sentence labels are gone and the bare **50**
  is paired with its meaning in the lead-in above the figure (F4). No arrow
  changed: the loop, the two diamonds and the two exits are the same claims.
- `enchanting` figure 2 — **split by machine**, with a lane each for the two
  copies of `EnchantmentMenu` (`CEM` and `EM`, a new key row, session F's
  `AbstractBoat` precedent). **Correction**: `EM->>SP: broadcastChanges` and
  `SP-->>EScr: broadcastChanges` put the same method on two arrows in two
  directions, and it is the menu's own
  (`AbstractContainerMenu.java:236-244`); the data slots reach the client as
  `ClientboundContainerSetDataPacket` through `ContainerSynchronizer.sendDataChange`
  (`AbstractContainerMenu.java:300-307`, `ServerPlayer.java:348-355`), so both
  are now `EM->>Wire`. `Player` and `ServerPlayer` **cut** to two notes;
  `SGPL` cut, the packets going through the `Wire` lane the split gave the
  figure. The assertion the split makes is the section's own: the client's copy
  answers the click before any packet is sent.
- `enchantments` figure 1 — **arm added**: `EnchantmentHelper.has,
  EnchantmentHelper.hasTag → ask the record: is the key there at all`, and the
  entry point is now a diamond. The paragraph above the figure calls the flag row
  "the exception and… the reason the shape is worth drawing" and the figure did
  not draw it.
- `enchantments` figure 2 — **two corrections of the caller's-method-at-the-callee
  shape**: `SGPL->>Player: handleAttack…` is `attack`
  (`ServerGamePacketListenerImpl.java:2020-2053` — `handleAttack` is the
  listener's own and `this.player.attack(target)` is what reaches the player);
  `Entity->>SED: baseTick sets shared flag zero` is `set`, on
  `Entity.DATA_SHARED_FLAGS_ID` bit 0, from `Entity.baseTick` through
  `Entity.setSharedFlagOnFire` (`Entity.java:583, 606-607, 2985-2991`). The
  `SynchedEntityData` lane is folded (one message, no decision) and the fire
  ticking is a `rect` band — the prose puts it on later ticks and the figure drew
  it as the next moment.
- `items/loot-tables` figure 1 — redrawn at six lanes with a `Wire` lane, and
  **five corrections**: `ChestBlockEntity` and `RandomizableContainer` were two
  lanes for one object (`RandomizableContainerBlockEntity implements
  RandomizableContainer`, `:20`); `SP->>ChestM: ClientboundOpenScreenPacket goes
  first, then initMenu` drew a clientbound packet arriving at the menu and named
  `ServerPlayer`'s own method (`ServerPlayer.java:1469`); `ChestM-->>SP:
  sendAllDataToRemote` drew the menu's own method as a return to the player when
  it is reached from `ServerPlayer.initMenu` → `AbstractContainerMenu.setSynchronizer`
  (`ServerPlayer.java:621-624`) and sends to the client;
  `LT->>LT: createStackSplitter wraps the whole fill` sat *after* the pool
  returned, though the splitter is the consumer `LootTable.getRandomItemsRaw` is
  called with and so is installed before any pool runs (`LootTable.java:114-122`);
  and `setItem` was a `LootTable` self-call when it writes into the container
  (`LootTable.java:166-172`). The opening arrow's `ChestBlock.useWithoutItem`
  label — a class with no lane — is a note.
- `items/loot-tables` figure 2 — **the placement tail cut** (`R` → `X`, seven
  nodes: the three function tiers, the splitter, the shuffle and the write),
  which the trace above now carries; and the five entry containers folded from
  five nodes and five edges into one *expand* node plus a two-column table.
  26 nodes → 14, 2,025px → 1,771px, and no arrow's direction changed.
- `recipes` figure 1 — the four sentence labels are gone, the two threads are the
  `worker` and `server` classes rather than the words *Worker:* and *server
  main:* inside labels, the empty window is a dotted edge, and the three
  feature-flag conditions leave the edge labels for one sentence (the queue's
  three senses of *enabled*, :4442). **No arrow's direction changed**; the
  `A -.-> F` edge is the one the section is about.
- `recipes` figure 2 — **split at the tick boundary the figure already noted**,
  into the tick the plank lands (five lanes) and the later tick the result is
  clicked (six). Both carry `rect` bands. **Four corrections of the same shape**:
  `CraftM->>CI: asCraftInput` drew the product as the callee — `asCraftInput` is
  `CraftingContainer`'s (`CraftingContainer.java:16`), and the container, not the
  `CraftingInput`, is the lane (`TCC`, a new key row); `ResultS->>ResultC:
  checkTakeAchievements first, then awardUsedRecipes` headed the arrow with
  `ResultSlot`'s own method, and what reaches the container is `awardUsedRecipes`
  (`ResultSlot.java:59-68`); `ResultC->>SRB: addRecipes` skipped
  `ServerPlayer.awardRecipes` between them (`RecipeCraftingHolder.java:23`,
  `ServerPlayer.java:1645-1646`); and `ResultS->>CraftM: removeItem` sent a
  `Container` method to the menu when the call is `craftSlots.removeItem` on the
  `TransientCraftingContainer` (`ResultSlot.java:111`, `AbstractCraftingMenu.java:17-24`).
- `using-an-item` figure 1 — **split into the two endings the page is about**,
  which is what the old figure's two disconnected graphs in one box already
  were. **Arrow added**: `G -. the byte lands .-> X`, a new node
  *`Player.handleEntityEvent` replays `Player.completeUsingItem`*, and `W --> X`
  — the client's countdown branch had **no exit at all**, and the packet node
  sent a byte no arrow received. `Player.handleEntityEvent` calls
  `completeUsingItem` on id 9 and nothing else on that side does, which is the
  page's own hook ("the meal ends when a single byte arrives"). In the second
  half, `S --> Q2` added: the client's local release is a *sibling* of the
  packet, not downstream of `handlePlayerAction`.
- `using-an-item` figures 3 and 4 — `Minecraft` cut from both (one message, no
  decision) and, in the bow, `BowItem` cut, because **one lane was standing for
  both machines' copies** and the page's point is that the same method runs twice
  and gets nowhere on one side; both releases are now self-messages on `LP` and
  `SP`. **Corrections**: `MC->>MPGM: startUseItem` named the caller's method —
  `Minecraft.startUseItem` calls `MultiPlayerGameMode.useItem`
  (`Minecraft.java:1880-1930`, `MultiPlayerGameMode.java:410`); `Cons->>LP:
  startConsuming` likewise — `Consumable.startConsuming` is Consumable's own and
  what reaches the player is `startUsingItem` (`Consumable.java:42-49`); and the
  meal's tick label said *five particles every fourth tick* with no mention of
  the delay the prose states, though `Consumable.shouldEmitParticlesAndSounds`
  gates on **both** `CONSUME_EFFECTS_START_FRACTION` and the interval. Three
  `rect` bands per figure replace the bare note bars.

### Corrections

Every one above marked *correction* is a fact changed with the decompile open;
nineteen in all, and **fifteen of them are one shape**: a message labelled with
the caller's own method and drawn arriving at the callee, or the same fault in a
flowchart edge. That is **six parts of six**, and every one was found by
`check_figure_names.py` mechanically rather than by reading.

Beside them, nine **Mojang names hyphen-broken on screen** (F18) —
`AbstractContainerMe-nu`, `EnchantmentNames.i-nitSeed`,
`ClientboundContainerSetDataPack-et`, `doPostAttackEffectsWithItemSour-ce`,
`TargetedConditionalEffe-ct`, `RandomizableContain-er`,
`ClientboundContainerSetContentP-acket`, `checkTakeAchievements-`,
`ProjectileWeaponItem.dr-aw` — every one of them a name the book was getting
wrong in the picture while getting it right in the prose. All nine fixed, and
**found mechanically**: `render/index.json` records the on-screen text of every
label, so a name broken by the theme is one regex over the render.

### Claims the captions make

Nineteen captions, one per figure, each a claim about what its figure shows.
The five that assert something the prose does not state in the same words, and
which pass 9 should check first: `containers-and-menus` f1 (*agreement is
silence* — the synchronizer is not reached in the agreeing case);
`items-and-stacks` f1 (*a stack reads defaults it can never touch*);
`loot-tables` f1 (*the contents exist before the screen is asked for*);
`using-an-item` f2 (*only the server's run reaches a `ServerLevel` and so an
arrow*); `enchanting` f2 (*the client answers the click out of the ten numbers
on the left, which is every number it has*).

### Ruled

- `contexts-and-predicates` f2's message head `test` stays a gate **note**:
  `LootItemCondition extends Predicate<LootContext>`, so `test` is
  `java.util.function.Predicate`'s and outside every tree `verify_names.py`
  indexes. F12(d)'s prose-head allowance covers it; session O should not read it
  as unresolved.

## Pass 7, session F — Part VI · Entities: the figures *(2026-09-15)*

Ten pages, 26 figures (22 before; three pages split one figure into two, one
page gained a figure, one page traded a flowchart for a table beside a
shorter one). Every mermaid figure captioned, every caption one italic run;
the figure-name gate clean on the part (14 unresolved names → 0, 55 notes →
8, all eight the prose message heads F12(d) allows); no type under 12.6px and
nothing below 0.79.

### The figures redrawn, and what each asserts

- `entities/README` — the part figure is `TD` rather than `BT`, its nine nodes
  numbered to the watch order, and it gains one edge: `2 · Authority → Parts
  VIII, IX and X`, labelled *and so does the rest of the book*. **The claim is
  the landing page's own** (“the second rung — *authority* — is the one
  everything else leans on, including Parts VIII, IX and X”), drawn rather than
  only said. No other arrow changed direction or meaning; the eight edge
  sentences are the same claims, shortened.
- `entities/ai-goals-and-brains` figure 1 — redrawn from *the four phases of
  `Brain.tick`* to *one behaviour through one `Brain.tick`*. **Arrows removed**:
  `A→B→C→D` (the phase chain, now a sentence above the figure), `F→I` and
  `H→I`. **Arrows added**: `G -- either test fails --> X` (a behaviour whose
  `Behavior.tryStart` fails stays `STOPPED`), and `H→S→J` through a new node
  *phase three ends, phase four begins*. The assertion is that phases three
  and four are **two complete sweeps over the set, not one pass per
  behaviour** — `Brain.tick` calls `Brain.startEachNonRunningBehavior` and then
  `Brain.tickEachRunningBehavior`, each with its own loop
  (`Brain.java:456-459`, `489-527`). The old `F→I`/`H→I` arrows asserted the
  opposite by implication.
- `entities/ai-goals-and-brains` figure 2 — the `PoiManager` lane and its three
  messages **cut** (the scan is [points of
  interest](../src/systems/world/points-of-interest.md)'s, as the prose beside
  the figure already says). `AP→PM: take(pos), then set POTENTIAL_JOB_SITE`
  **retargeted** to `AP→Brain: writes POTENTIAL_JOB_SITE`: `AcquirePoi` calls
  `poiManager.take(...)` and then writes the memory through the accessor, which
  is the brain's (`AcquirePoi.java:89-92`). `SIB→SIB: startSleeping, record
  LAST_SLEPT, clear the walk target` **replaced** by `Brain→SIB: tickOrStop,
  and again every tick until dawn`: `startSleeping` is the villager's, not
  `SleepInBed`'s (`SleepInBed.java:88`), and the new message asserts what the
  prose calls the page's counter-example — `SleepInBed` overrides
  `Behavior.canStillUse`, so it is still running the tick after the one that
  started it. Two `rect` bands added for the two ticks.
- `entities/attributes` figure 1 — the three modifier indices **cut** to the
  section that owns them; the two dirty sets **re-parented** from
  `AttributeInstance` to `AttributeMap`, through a new
  `AttributeMap.onAttributeModified` node. The assertion: `attributesToSync`
  and `attributesToUpdate` are fields of `AttributeMap`
  (`AttributeMap.java:20-21`) and `AttributeMap.onAttributeModified` is what
  adds to them (`:28-32`). `SUP -- createInstance --> MAP` **relabelled** to
  `MAP -- AttributeMap.getInstance --> INST`, because the call runs
  map→supplier and the product is the instance (`AttributeMap.java:50-52`).
  The dotted `getSyncableAttributes` edge is now solid and labelled *when
  tracking starts*.
- `entities/attributes` figure 3 — `AttrM→AttrI: createInstance` **relabelled**
  `replaceFrom, inside AttributeSupplier.createInstance`
  (`AttributeSupplier.java:48-58`); `LE→AttrM: getAttributeValue`
  **relabelled** `getValue`, since `LivingEntity.getAttributeValue` delegates
  to `AttributeMap.getValue` (`LivingEntity.java:2329-2331`); the two
  `AttrI-->>AttrM` **dashed returns turned solid**, because
  `AttributeInstance.setDirty` calling the map's consumer is a call, not a
  return; `removeModifier` restored to the modifier message
  (`MobEffect.java:184-185`); a return leg `AttrM-->>LE` added so the value
  comes back the way it went. A `rect` band marks the following tick.
- `entities/authority` figure 1 — **`Q→SIM` and `Q→AI` reversed** to
  `SIM→Q` and `AI→Q`, labelled *by default*, so every arrow in the figure
  means one thing: *is answered by*. This is the queue's :5528 and the
  assertion is the heading's own — the other four hang off the final one.
  `CAP` **relabelled** from *Player: always true* to *Player: true, so the root
  is false*, because the parent node is the negation and a reader following
  *not X* to *always true* got the opposite of the page's table.
- `entities/authority` figure 2 — **split by machine, with a lane each for the
  two copies of the boat** (`SAB`, a new key row). `CL→AB: tickNonPassenger`
  **removed** and made a note: `tickNonPassenger` is `ClientLevel`'s, and what
  arrives at the boat is `Entity.tick` (`ClientLevel.java:477-487`). The two
  `SGPL→AB` messages **retargeted** to the server's copy. The accept and the
  reject are now an `alt` — the figure's one mark outside `TEMPLATE.md`'s
  table, said so in the caption — and the echo is its own `CPL→Wire` arrow
  rather than a clause on an arrow pointing the other way.
- `entities/damage-and-death` figure 1 — the eight-step chain keeps only the
  step names, with the running number on the arrows, and the owners and the
  arithmetic move to a nine-row table beside it. **Freezing and the helmet are
  now two steps, not one**, which is the correction below. A terminal *2.12*
  is asserted as what reaches health in this scenario.
- `entities/damage-and-death` figure 2 — **`ServerPlayer` and `LivingEntity`
  merged into one lane**, because they are one object (F7); the three
  `hurtServer` messages are now self-messages naming the class whose override
  runs. `LE→CT: actuallyHurt` **split** into a self-message and
  `SP→CT: recordDamage`, because `LivingEntity.actuallyHurt` is the caller's
  and only `CombatTracker.recordDamage` reaches the tracker. The death tail
  **cut** to figure 3 and the prose; `resolveMobResponsibleForDamage` and
  `resolvePlayerResponsibleForDamage` are now one message each so the name
  fits without a hyphen.
- `entities/damage-and-death` figure 3 — **new**, under *Death, or not*.
  Every arrow re-derived from `LivingEntity.die` (`LivingEntity.java:1565-1601`):
  the totem test guards the whole of it; kill credit,
  `LivingEntity.handleKillingBlow` and `CombatTracker.recheckStatus` run
  unconditionally; the veto is `sourceEntity == null ||
  sourceEntity.killedEntity(...)` and it guards the game event,
  `LivingEntity.dropAllDeathLoot` and the wither rose only; the entity-event
  byte is **outside** the veto; `Pose.DYING` is set **after** the byte.
- `entities/entity-anatomy` figure 1 — the eleven-box flowchart is now the
  book's **fifth `classDiagram`**, three classes. `EntityType --> EntityDimensions`
  (*holds one, built once*), `EntityType ..> Entity` (*`EntityType.create`
  calls the factory*), `EntityDimensions ..> Entity` (*copied into the two
  caches, and recopied on a pose change*). The nine former boxes are field
  rows; no relation is asserted that the old figure did not draw.
- `entities/entity-anatomy` figure 3 — **split at the tick note**: the server
  half keeps five lanes, and a second figure of three lanes draws the client
  building **a second live object** from the packet. The claim the split
  asserts is the page's title happening twice.
- `entities/movement-and-collision` figure 1 — **seven lanes to three**. The
  `CollisionGetter`, `Shapes` and `Block` lanes **cut**: every message sent to
  them was headed with `Entity`'s own method (`Entity.collide`,
  `Entity.collideWithShapes`, `Entity.setOnGroundWithMovement`,
  `Entity.checkFallDamage`), and the inside of `Entity.move` is the next
  section's figure. `LivingEntity` and `Entity` **merged into one lane**, each
  message naming the class whose half runs. `SL→Entity: tickNonPassenger`
  **relabelled** `tick` for the same reason as `authority`'s. A `rect` band
  marks the next tick.
- `entities/movement-and-collision` figure 2 — **a new diamond**,
  `NEXT{"a candidate height left?"}`, so the loop's exhaustion is not drawn as
  an answer to *more horizontal distance than the flat attempt?*. Re-derived
  from `Entity.java:1198-1225`: the exits are the `for` ending (→ the flat
  result) and the `return` inside it (→ the stepped one). `HEIGHTS`
  **relabelled** *less the one already tried*, which is the correction below.
- `entities/pathfinding` figure 1 — redrawn from the pipeline (which figure 2
  draws, with the callers) to **the two entrances and the two endings**.
  `WORLD→GATE` **added**: `PathNavigation.recomputePath` is the other
  entrance, which the prose names and the figure never drew.
  `GIVEUP -- no --> RUN` **added** so the follow is a loop.
- `entities/pathfinding` figure 2 — `NE→PNR: getPathTypeFromState`
  **relabelled and split**: `getPathTypeFromState` is
  `PathfindingContext`'s, not the region's
  (`PathfindingContext.java:31-35`), and what the evaluator gets from the
  region is a block state (`:37-39`). Now `NE→PNR: getBlockState, through
  PathfindingContext` with a note that `PathTypeCache` memoises the
  `PathType` per position, server-side only.
- `entities/synched-entity-data` figure 1 — **split at the tick the prose
  names**, so **each half has one `SynchedEntityData` lane meaning one
  container**; the second half boxes them by machine and adds `CSED`, a second
  key row. `SGPL→Sheep: Player.interactOn` **relabelled** `Mob.interact`;
  `CM→SE: ChunkMap.tick` **cut** with the `ChunkMap` lane, its decision being
  figure 3's; `CPL→SED: handleSetEntityData` **relabelled**
  `SynchedEntityData.assignValues` and retargeted to the client's container.
  `SED→SED: SynchedEntityData.DataItem.setDirty` **added after** the callback
  to `Sheep`, which is the ordering the prose italicises and the figure had
  been flattening onto one arrow.
- `entities/synched-entity-data` figure 3 — `IN` **turned from a box into a
  diamond** and given its false exit to `HOLD`, so both tests fail into the
  same place, which is the section's claim.

### Captions

Twenty-five captions written, one per mermaid figure in the part; each is a
claim about what its figure shows and pass 9 should read each against its
figure. The two that assert most: `entities/movement-and-collision` figure 1
(“gravity is subtracted **after** the move, not before it, so the delta a
tick moves the mob by was built by the tick before”) and
`entities/damage-and-death` figure 2 (“the three `hurtServer` messages at the
top are one virtual call going down the override chain”).

### Corrections

- `src/systems/entities/ai-goals-and-brains.md`:353 — the figure said
  `updateActivityFromSchedule` is “refused unless **20** ticks have passed
  since the last one”; the prose two paragraphs below says 21, “the test is a
  strict *greater than* 20”. `Brain.java:389` is
  `gameTime - this.lastScheduleUpdate > 20L`, so the prose is right and the
  figure was wrong. The clause is out of the figure and the prose keeps it.
- `src/systems/entities/ai-goals-and-brains.md`:351 — the figure drew
  `POTENTIAL_JOB_SITE` being written to `PoiManager`. `AcquirePoi.java:89-92`
  writes it through the memory accessor, which is the brain's.
- `src/systems/entities/ai-goals-and-brains.md`:360 — `startSleeping` drawn
  as `SleepInBed`'s own; `SleepInBed.java:88` calls `body.startSleeping(...)`,
  so it is the villager's.
- `src/systems/entities/attributes.md`:49 — the figure said
  `permanentModifiers` is “the subset **`AttributeMap.pack`** writes to
  disk”. `AttributeMap.java:156-167` packs **every** instantiated instance and
  filters nothing; it is `AttributeInstance.pack`
  (`AttributeInstance.java:207-209`) that writes the base value and the
  permanent modifiers only. The node is cut with the two others that belong to
  the next section, and the prose there already had it right.
- `src/systems/entities/attributes.md`:50-51 — `attributesToUpdate` and
  `attributesToSync` were drawn hanging off `AttributeInstance`;
  `AttributeMap.java:20-21` makes them the map's.
- `src/systems/entities/attributes.md`:58 — the arrow
  `AttributeSupplier → AttributeMap` was labelled “`createInstance` copies a
  prototype into a fresh instance”, which reverses the call and misplaces the
  product: `AttributeMap.getInstance` calls `supplier.createInstance` and the
  product is an `AttributeInstance` (`AttributeMap.java:50-52`).
- `src/systems/entities/authority.md`:86-89 — the node *not
  `Entity.isClientAuthoritative`* had a child reading *Player: always true*,
  so the figure resolved to *true on the server for a player* while the page's
  own table (“server, player, false”) says the opposite. The leaf now states
  what it resolves to.
- `src/systems/entities/damage-and-death.md`:106 against :114 — the prose says
  “**eight** arithmetic steps — five multiplications and three subtractions”
  and the figure drew **seven** boxes after the source, freezing and the helmet
  sharing one. They are two steps (×5 and ×0.75) and are now drawn and tabled
  as two; the count in the sentence is the one that was right.
- `src/systems/entities/damage-and-death.md`:273 — the message read
  “`hurtServer` — PvP and teams”, where *PvP* is neither a class nor a method;
  the prose names `ServerPlayer.canHarmPlayer` as the gate, and the figure
  now does too.
- `src/systems/entities/entity-anatomy.md`:63 — the figure carried
  “`clientTrackingRange` in chunks (default 5), `updateInterval` in ticks
  (default 3)” and the two defaults appeared nowhere in the page's prose.
  They are right (`EntityType.java:504-505`, the `Builder` constructor) and
  the sentence that owns the two fields now says them.
- `src/systems/entities/entity-anatomy.md`:193 — the prose said the 66 outside
  `LivingEntity`'s branch are “**two families** and a scattering” and named
  `Projectile` and `VehicleEntity`; the generated tree beside it draws **four**
  — `BlockAttachedEntity` (5) and `Display` (3) as well — and 27 + 16 + 6 + 4
  + 13 is the 66. `Display` was named nowhere on the page.
- `src/systems/entities/movement-and-collision.md`:177 — `HEIGHTS` said
  “**every** Y face of every candidate shape inside `maxUpStep`”;
  `Entity.java:1240` is `relativeCoord >= 0.0F && relativeCoord !=
  stepHeightToSkip`, so the height the flat attempt already tried is skipped,
  which is what the prose says.
- `src/systems/entities/movement-and-collision.md`:186 — the `MORE` diamond
  had two outgoing edges labelled *no*, one of them the `for` loop ending
  rather than an answer to the question in it (`Entity.java:1212-1224`).
- `src/systems/entities/pathfinding.md`:217 — `getPathTypeFromState` drawn
  arriving at `PathNavigationRegion`; it is `PathfindingContext`'s, and the
  context holds both the region and the cache
  (`PathfindingContext.java:13-14`, `31-35`).
- `src/systems/entities/synched-entity-data.md`:181 — the figure put
  `Entity.onSyncedDataUpdated` and `DataItem.setDirty` on one arrow, in that
  order, arriving at `Sheep`. The prose italicises the ordering — *and then*
  marks the item dirty — and the two are now two messages, the second a
  self-message on the container.
- `src/systems/entities/entity-lifecycle.md`:85 — the caption said “only
  three of **the eight** leave the loop at all”, a count nothing in the figure
  lets a reader check: three arrows reach the terminal box, but *the eight* is
  not a set the picture draws. Now “only three arrows leave the loop at all —
  the three that reach the box at the foot”. **The exemplar's figure is
  otherwise untouched and one real gap in it is logged for session O**
  ([pass5.md](pass5.md)): it draws neither of the two rejections the prose
  under it says end a group attempt.
- `src/systems/entities/entity-lifecycle.md`:312 — the message read
  “`addFreshEntity`, once per **passenger**” while the prose says
  `ServerLevel.addFreshEntityWithPassengers` walks `Entity.getSelfAndPassengers`
  **vehicle first**; a reader of the figure alone concludes the vehicle is not
  one of the bodies. Now “once per body, the vehicle first”.
- `src/systems/rendering/visibility-and-the-frame-graph.md`:51-55 — five node
  labels beginning `1. ` … `5. ` rendered on the live site as the literal
  string *Unsupported markdown: list*, so five of the figure's six nodes were
  blank on the page. Out of this part, fixed anyway, and gated (see
  [pass5.md](pass5.md)). Only where a line ends changed; no arrow, no name,
  no claim.

### Tools

- `tools/check_mermaid.js` gained `erasedLabels` and a nine-case probe.
- `tools/map_source.py`'s `svg_tree` gained a width retry and a probe case;
  the five generated trees are regenerated and **the fold labels of the
  deepest branches now show a count instead of example names**, which is a
  change to what five pages' figures say. `entity-anatomy`'s figcaption
  states the key.

## Pass 7, session E — Part V · Blocks: the figures *(2026-09-15)*

Eight pages, thirteen figures (ten before; three pages split one figure into
two). Every figure captioned and every caption one italic run; every non-lead
figure given a lead-in; **thirteen gate failures and twenty-six gate notes to
none of either**, and no figure in the part now shows type under 11.9px (five
were at 10.3–11.1px). No page moved and no theme file was touched.

### The figures redrawn, and the orderings they assert

**`blocks/README` figure 1 — the part's shape.** Seven nodes numbered to the
watch order, eleven sentence-length edge labels cut to three or four words, a
caption. No arrow added, removed or reversed. One claim in the prose beside it
was **wrong and is corrected**: the lead-in read *Each arrow below is labelled
with what the hub hands that spoke*, and five of the eleven arrows do not touch
the hub. It now distinguishes the six hub arrows from the five between spokes.

**`blocks-and-states` figure 1 — the vocabulary, as a `classDiagram`.** Was a
twelve-node `flowchart TB` in which inheritance and construction were the same
arrow. Now the book's fourth class diagram, asserting: `BlockBehaviour` is
abstract and `Block` extends it; `Property` is abstract and is extended by
`BooleanProperty`, `IntegerProperty` and `EnumProperty` **and by nothing else**
(verified: those are the only three `extends Property<` in
`world/level/block/state/properties/`); `StateHolder` is extended by
`BlockBehaviour.BlockStateBase`, which is extended by `BlockState`; `Block`
holds one `StateDefinition`, built in its own constructor; `StateDefinition`
holds the properties and produces one `BlockState` per cell;
`StateDefinition.fillNeighborsForState` fills `StateHolder`'s table.
`Block.BLOCK_STATE_REGISTRY` left the figure as a node and is a field line
inside `Block` — it is a static field, not a class, and the heading is
therefore now *Eleven classes and one Cartesian product*, not twelve. **The
caption is a claim**: the two hierarchies meet in `BlockState`, joined by the
one arrow that is neither an extends nor a holds.

**`blocks-and-states` figures 2 and 3 — the write, split at the re-read.** The
part's most-linked figure was 21 nodes and 3,409px with ten sentence labels and
every gate clause inside a node. Split at the joint the prose already names
(*two half-writes with a re-read between them*), with the gate clauses moved to
a thirteen-row table (*step · side · flags · also needs*), each derived from
`Level.setBlock` (`world/level/Level.java:217-262`) and
`LevelChunk.setBlockState`. Arrows changed: **`IN --> FALSE` added** —
`Level.setBlock` returns false at `Level.java:219` (out of bounds) and `:221`
(the server side of a debug world), which the prose already asserted and the
figure gave no exit for. The `TRUE` node's own text (*returns true, having
skipped its entire tail*) **was false on one of its two inbound edges** and is
now plain *returns true*, with the clause on the edge it belongs to. Three
steps carry `:::server`: `BlockEntity.preRemoveSideEffects`,
`BlockBehaviour.BlockStateBase.affectNeighborsAfterRemoval` and
`BlockBehaviour.BlockStateBase.onPlace`. Every other edge is unchanged.

**`block-breaking` figures 1 and 2 — one dig, split at the eighth tick.** Was
seven lanes at 0.65 with four Mojang names hyphen-broken on screen. Now six
lanes each, boxed `Client` and `Server`, with the loop's body in a `par` so the
picture stops asserting an order between two things the section exists to call
independent. Six messages were **labelled with the caller's own method and
drawn arriving at the callee** — `startAttack` and `continueAttack` (both
`Minecraft`'s, `Minecraft.java:1777`/`:1806`), `continueDestroyBlock`
(`MultiPlayerGameMode`'s), `destroyAndAck` (`ServerPlayerGameMode`'s),
`mineBlock` (`ItemStack`'s, called at `ServerPlayerGameMode.java` inside
`destroyBlock`) and `popResource` — and each now names the method of the lane
it arrives at. **`ServerboundSwingPacket` added** inside the loop:
`Minecraft.continueAttack` calls `LocalPlayer.swing`, which sends it
(`LocalPlayer.java:338-341`); the loop's own label had asserted it in words and
drawn nothing, which is what made the silence across the boxes unreadable.

**`block-interaction` figures 1 and 2 — one click, split at the machine
boundary.** `ServerPlayerGameMode` gained the lane the cast already gave it, so
the two sides read as the same three-step order, which is the section's claim.
Four caller-headed messages relabelled: `startUseItem` (`Minecraft`'s) →
`useItemOn`; `canOpenByHand` (`BlockSetType`'s) → `setBlock`;
`updateNeighbourShapes` (`BlockBehaviour.BlockStateBase`'s) → `shapeUpdate`,
which is what `CollectingNeighborUpdater` actually receives
(`CollectingNeighborUpdater.java:37`); `updateOrDestroy` (`Block`'s static,
`Block.java:238`) → `setBlock`, which is what it calls on the level at
`Block.java:245`. `endPredictionsUpTo` — a name the page never says, and a
`BlockStatePredictionHandler` method drawn on the `ClientLevel` lane — became
`handleBlockChangedAck`, which is `ClientLevel`'s own
(`ClientLevel.java:190-196`). The two `ClientboundBlockUpdatePacket`s are now
drawn as two, the count the prose gives. The swing packet became a note.

**`block-entities` figure 1.** `tickBlockEntities` (`Level`'s) → the wrapper it
actually reaches, `LevelChunk.BoundTickingBlockEntity.tick`
(`LevelChunk.java:911`). **One message added**:
`updateNeighbourForOutputSignal`, the second of the two writes the prose counts
and the figure drew one of — `BlockEntity.setChanged` reaches it at
`BlockEntity.java:270-276`, called from `AbstractFurnaceBlockEntity.serverTick`
at `:220`. **One note added**: tick N's chunk-source phase, drawn *above* the
block-entities phase, which is the whole cause of the lag and had been carried
in four words of one message label. The `ChunkHolder` self-reply that said
*gets nothing* became a note — a dashed arrow is a reply and there was no
reply. The `ServerPlayer` lane, which carried one message and decided nothing,
folded into a note.

**`pistons-and-block-events` figure 1.** Two caller-headed messages:
`doBlockEvent` is `ServerLevel`'s (`ServerLevel.java:1344`) and is now a
self-message with `triggerEvent` as the arrow into `PistonBaseBlock`;
`moveBlocks` is `PistonBaseBlock`'s own (`PistonBaseBlock.java:291`) and the
arrow into `ServerLevel` is the `setBlock` it makes. **`PSR-->>PBB` added** —
the dry run's answer: `PistonBaseBlock.checkIfExtend` queues the block event
only if `new PistonStructureResolver(...).resolve()` is true (`:116-117`), so
the resolver's refusal is what stops anything being queued. **`setBlockEntity`
added** — `moveBlocks` injects one `PistonMovingBlockEntity` per placeholder by
hand (`:349`, `:360`), which gave the lane its origin. **An `opt` frame added**
around everything from the second `getNeighborSignal` to the client's re-run:
`PistonBaseBlock.triggerEvent` returns false at `:189` when the wire is no
longer powered, and `ServerLevel.runBlockEvents` sends
`ClientboundBlockEventPacket` **only if `doBlockEvent` returned true**
(`ServerLevel.java:1333-1334`), so the packet and the whole of the client's
share really are inside the conditional.

**`signal-and-dust` figure 1.** **`OUT --> IN` added**, the loop back from the
forty-two outgoing updates to `RedStoneWireBlock.neighborChanged` — the
recursion the page's hook is about, which had existed only in the prose. The
`canSurvive`/`dropResources` limb was **cut** (a logged cut: three nodes of a
story the page tells nowhere). `flag 2` became `Block.UPDATE_CLIENTS`.

**`signal-and-dust` figure 2.** `getBlockSignal` (`RedStoneWireBlock`'s) headed
a message into `DefaultRedstoneWireEvaluator`; the call that actually arrives
there is `updatePowerStrength` (`RedStoneWireBlock.java:267-271`,
`DefaultRedstoneWireEvaluator.java:20`). `LeverBlock.updateNeighbours` headed a
message into `ServerLevel`; it is `Level.updateNeighborsAt`. `SL->>CNU` now
names `updateNeighborsAtExceptFromFacing`, which is what
`ServerLevel.updateNeighborsAt` calls (`ServerLevel.java:1241`).

**`diodes-and-observers` figure 1.** Four node labels that were sentences
became names, with their conditions on the edges. **Three arrows added**:
`RL --> DONE` (the repeater's lock is written inside the shape update and books
nothing — drawn as a named dead end rather than an arrow that stops); and
`BOOK` now forks to `DiodeBlock.tick` and `ObserverBlock.tick` separately,
because the two leave by **different routes** — `DiodeBlock.tick` writes
`POWERED` under flag 2 and never calls `updateNeighborsInFront` itself
(`DiodeBlock.java:56-71`), so its pulse leaves through `DiodeBlock.onPlace`
inside that write (`DiodeBlock.java:181-183`), while `ObserverBlock.tick` calls
`ObserverBlock.updateNeighborsInFront` directly after its own write
(`ObserverBlock.java:51-61`). One `TICK` node had been carrying both.

### The corrections

1. **`block-breaking` figure 1, the server's progress at STOP.** The figure
   said *own progress 1.07*; the prose two sections below says the server
   *arrives at the same 1.064*, and that identity is the section's whole
   argument. The one number the page is about was printed two ways inside one
   figure. Now 1.064. (`ServerPlayerGameMode.handleBlockBreakAction`: the
   per-tick fraction times `ticksSpentDestroying + 1`.)
2. **`block-breaking` figure 1, the order of tick 1.** The figure drew
   `continueDestroyBlock`'s first 0.133 *before* the stage −1 crack clear.
   `MultiPlayerGameMode.startDestroyBlock` sets `destroyProgress` to zero and
   calls `ClientLevel.destroyBlockProgress` with `getDestroyStage()` — which is
   −1 at progress zero (`MultiPlayerGameMode.java:583-585`) — at `:202`, and
   only then does `Minecraft.continueAttack` run `continueDestroyBlock` on the
   same lap (`Minecraft.java:2170`, `:2192`), which adds 0.133 and calls
   `destroyBlockProgress` again at `:282`, this time at stage 1. The figure now
   draws all three, in that order.
3. **`blocks-and-states`, the flag-word lead-in: *seven* for eight.** *Here are
   the seven it gates on* was followed by eight bits (1, 2, 4, 16, 32, 64, 256,
   512), and the page's own later sentence says *those eight bits*. Corrected
   to eight. Found independently by two viewers.
4. **`blocks-and-states` figure 2, the `TRUE` node.** *Level.setBlock returns
   true, having skipped its entire tail* was the text of one inbound edge
   printed on a node that both edges arrive at, so it was false for the path
   that had just run the tail.
5. **`blocks/README`, the figure's lead-in.** *Each arrow below is labelled
   with what the hub hands that spoke* described six of eleven arrows.
6. **`pistons-and-block-events` figure 1, the landing tick.** The note read
   *tick N plus 2, block-entities phase* and spanned `ServerLevel` to
   `ClientLevel`, directly under a note that said *both sides* — so the figure
   said both sides land on N+2. The page's own prose says the client holds five
   extra `PistonMovingBlockEntity.deathTicks` first. The note now names the two
   timings separately.
7. **`signal-and-dust` figure 2, who asks whom at the piston.** The label read
   *the piston asks only whether the wire's east side is above zero*. The prose
   says the piston asks nothing of the kind: the wire's east side is
   `RedstoneSide` *SIDE* by the completion pass, and
   `RedStoneWireBlock.getSignal` *asks about the side, not about the neighbour*
   — so the wire answers, and the side is a three-valued property, not a number
   that can be above zero. The label now says the wire answers from its east
   side.
8. **`signal-and-dust` figure 2, an unnamed count.** *…and the count resets* —
   no count is named in that section or anywhere on the page. Removed.
9. **`block-entities` figure 1, one write of two.** *Two writes leave the block
   entity* sat forty-five lines under a figure that drew one. The second is now
   drawn (see above).
10. **`block-breaking` figure 1, two words the page never says.** `gameTicks`
    (a real `ServerPlayerGameMode` field, but not prose on this page) and *the
    ledger* (the page's blockquote calls it *the entry*) left the figure for
    the page's own words. `MultiPlayerGameMode.startDestroyBlock`, which the
    figure needed, gained its sentence in the prose instead.
11. **`block-breaking` figure 1, a number without its unit.** *within 32*,
    where the prose says *within 32 blocks* and the other numbers in the same
    figure (0.133, 1.064, 2001, 11, 3) are five different kinds of thing.

### What a pass-9 session should read hardest here

The thirteen-row gate table on `blocks-and-states` is new prose carrying
thirteen conditions that used to be inside figure labels; every row is a claim
and every one was derived from `Level.setBlock` and `LevelChunk.setBlockState`
on 2026-09-15. The `opt` frame on `pistons-and-block-events` asserts that
*nothing* inside it happens when the second `getNeighborSignal` fails,
including the sound packet — check that `runBlockEvents`' single `if` really is
the only gate on both packets. And the `OUT --> IN` loop on `signal-and-dust`
is the page's hook drawn for the first time: it asserts that a wire among the
forty-two re-enters `neighborChanged`, which is the prose's claim and not a
claim about the *number* of re-entries.

## Pass 7, session D — Part IV · The world: the figures *(2026-09-15)*

Eleven pages, twenty-seven figures (twenty-four before; four were split and one
became a table plus a new figure). Every figure captioned and every caption one
italic run; every non-lead figure given a lead-in; every name in every figure
resolved against the decompile — **nineteen gate failures and sixty-three gate
notes to none of either**. No page moved and no theme file was touched.

### The part-wide finding, which is the entry pass 9 should read first

**Nineteen names failed the figure gate and fourteen of them were the same
device Part III named** — a message labelled with the *caller's* own method and
drawn arriving at the *callee*. It is now four parts of four, and the shape is
mechanical: the gate finds it because a message's head is checked against the
lane it is sent to, and the caller's method is by construction not a member of
that lane. Each was re-derived and fixed by naming what actually arrives.

1. `fluids` — `BucketItem.emptyContents` on an arrow into `ServerLevel`. What
   arrives is `Level.setBlock` (`BucketItem.java:123`).
2. `fluids` — `FlowingFluid.spreadTo` into `ServerLevel`; the message is the
   `setBlock` inside it.
3. `lighting` — `ServerChunkCache.pollTask` into `ThreadedLevelLightEngine`; the
   call is `ThreadedLevelLightEngine.tryScheduleUpdate` (`:208`).
4. `lighting` — `LightEngine.propagateDecreases` and `propagateIncreases` into
   `LayerLightSectionStorage`; what that lane receives is
   `LayerLightSectionStorage.setStoredLevel` (`:88`).
5. `lighting` — `ServerChunkCache.broadcastChangedChunks` into `ChunkHolder`;
   the call is `ChunkHolder.broadcastChanges` (`:187`).
6. `chunk-generation-pipeline` — three `ChunkMap` methods
   (`ChunkMap.prepareAccessibleChunk` at `:783`, `ChunkMap.getChunkRangeFuture`,
   `ChunkMap.scheduleGenerationTask`) on an arrow into `ChunkGenerationTask`;
   what happens there is `ChunkGenerationTask.create` (`:35`).
7. `chunk-generation-pipeline` — `ChunkMap.runGenerationTasks` (`:736`) into
   `ChunkTaskDispatcher`.
8. `chunk-generation-pipeline` — `ChunkTaskDispatcher.scheduleForExecution`
   (`:93`) into `ChunkGenerationTask`.
9. `chunk-generation-pipeline` — `ChunkGenerationTask.releaseClaim` (`:81`)
   into `ChunkMap`; what `ChunkMap` is asked for is `ChunkMap.releaseGeneration`
   (`:673`).
10. `chunk-storage` — `ChunkMap.scheduleUnload` into `ChunkHolder`; the call is
    `ChunkHolder.getSaveSyncFuture`.
11. `scheduled-ticks` — `DiodeBlock.updateNeighborsInFront` (`:193`) into
    `ServerLevel`; that method calls `Level.neighborChanged` and
    `Level.updateNeighborsAtExceptFromFacing`, which is what the arrow carries.
12. `scheduled-ticks` — `DiodeBlock.shouldTurnOn` into `LevelTicks`; the booking
    is `ServerLevel.scheduleTick`, and the arrow now goes through `ServerLevel`
    like the page's other booking.
13. `points-of-interest` — `Player.startSleeping` into `ServerLevel`; the
    message is the `setBlock` that sets `BedBlock.OCCUPIED`.
14. `tickets-and-loading` — `PlayerChunkSender.sendNextChunks` (`:56`) into
    `ServerGamePacketListenerImpl`; that method sends
    `ClientboundChunkBatchStartPacket`, the chunk packets and
    `ClientboundChunkBatchFinishedPacket` (`PlayerChunkSender.java:71-81`).

Four more were a member named on the wrong owner:
`environment-attributes-and-timelines`'s `EnvironmentAttribute.sanitizeValue`
drawn on a *return* to `Mob` (the value is what returns) and its
`AttributeType.partialTickLerp` left unqualified; `chunk-storage`'s
`IOWorker.PendingStore` named bare; and `scheduled-ticks`'s
`LevelChunkTicks.onTickAdded`, which is the container's own callback field —
what runs on `LevelTicks` is `LevelTicks.updateContainerScheduling`
(`LevelTicks.java:55-58`).

**One the gate flagged that was not wrong**, checked and left as drawn:
`tickets-and-loading`'s `ChunkMap` to `PlayerChunkSender`,
`markChunkPendingToSend`. Both classes really have that method
(`ChunkMap.java:930`, `PlayerChunkSender.java:45`) and `ChunkMap`'s calls the
sender's.

### Corrections

- **`environment-attributes-and-timelines`, the stack figure.** It drew the two
  lightning-flash layers as two more rungs, so every value passed through them
  before the clamp. They are neither general rungs nor merely client-only:
  `ClientLevel` adds each with
  `EnvironmentAttributeSystem.Builder.addTimeBasedLayer` against **one named
  attribute** — `EnvironmentAttributes.SKY_COLOR` and
  `EnvironmentAttributes.SKY_LIGHT_FACTOR` — so they are two entries in two
  attributes' stacks and absent from the other forty-six
  (`ClientLevel.java:269-279`). The figure is a branch now and the prose says it.
- **`environment-attributes-and-timelines`, the client trace.** Everything under
  *between ticks, once per frame* asserted that the whole stack re-resolves each
  frame. `EnvironmentAttributeProbe.ValueProbe.get` resolves only when its
  `newValue` is null and `ValueProbe.tick` nulls it once a tick, so **the first
  frame of a tick that asks pays for the whole tick and every later frame only
  lerps** (`EnvironmentAttributeProbe.java:68-86`). Drawn as an `opt` block, with
  a sentence added to the prose.
- **`game-events-and-vibrations`, the trace.** The *tick T plus 1* band never
  ended, so arrival was drawn inside T+1 while the figure's own note and the
  prose put it eight blocks and seven further ticks away. A third band, *tick T
  plus 8*.
- **`game-events-and-vibrations`, the trace's lane.** One `SculkSensorBlock` lane
  stood for the block *and* the block entity, and its own message text said so.
  `VibrationSystem.Ticker` calls
  `SculkSensorBlockEntity.VibrationUser.onReceiveVibration` (`:115`), which calls
  `SculkSensorBlock.activate` (`:209`), which does the `setBlock`. Two lanes now,
  and `SSVU` is a new lane-key row.
- **`scheduled-ticks`, the pipeline figure.** `LevelTicks.cleanupAfterTick` was
  drawn emptying three collections where the prose a hundred lines below names
  **four**, `LevelTicks.toRunThisTickSet` included. The figure says four.
- **`points-of-interest`, the state figure.** Three `Held` to `Free` edges
  against the four release call sites the prose names (`ValidateNearbyPoi`,
  `Villager.releaseAllPois`, `SetWalkTargetFromBlockMemory`, `VillagerMakeLove`).
  One edge now, and the prose keeps the four.
- **`points-of-interest`, the trace.** `VillagerGoalPackages.validateBedPoi` was
  on `PoiManager`'s return arrow; the prose has `AcquirePoi` running it after the
  five come back. A self-message on `AcquirePoi`.
- **`chunk-generation-pipeline`, the pyramid figure.** The prose says *the six
  plain boxes run inline* and the figure drew **seven** square boxes, the seventh
  being the accumulation annotation wearing a step's shape. The twelve steps are
  a table now and the arithmetic is prose.
- **`fluids`, the trace.** A fluid tick was booked two ways inside one figure —
  through `ServerLevel` for the source and straight into `LevelTicks` for the
  four new blocks. `LiquidBlock.onPlace` calls `ServerLevel.scheduleTick` in both
  cases; both arrows go through the level now.

### New claims — the figures redrawn, and the orderings they assert

- **`world/README`** — the part figure is numbered to the watch order, and its
  caption asserts three things: that the five ring boxes hand a chunk along and
  the sixth arrow closes the ring; that the pipeline-to-lighting edge is an
  *inclusion* (lighting is two of the pipeline's twelve statuses,
  `ChunkStatus.INITIALIZE_LIGHT` and `ChunkStatus.LIGHT`, run on a different
  executor) and not a hand-off like the others; and that lecture one is off the
  ring. The environment-attributes edge no longer carries a label naming three
  readers, two of which are other boxes in the same figure.
- **`chunk-anatomy` figure 1** — a `classDiagram`, the book's third. It asserts
  the hierarchy (`ChunkAccess` abstract with two direct concrete lines,
  `ImposterProtoChunk` extending `ProtoChunk`, `EmptyLevelChunk` extending
  `LevelChunk`, all four verified), one dashed dependency for the promotion by
  `ChunkStatusTasks.full`, and one association for the wrap. The origin branch
  was cut and logged in [pass5.md](pass5.md).
- **`chunk-anatomy` figure 2** — asserts that each `PalettedContainer` has its
  **own** `PalettedContainer.Data` and the two never share one, where the figure
  before drew both containers into one box; and its caption asserts that a
  section's light is not on the section.
- **`chunk-generation-pipeline` figure 1** — a new figure of four nested rings,
  asserting `ChunkStep.accumulatedDependencies` for FULL as `ChunkStatus.SPAWN`
  at distance 0, `ChunkStatus.INITIALIZE_LIGHT` at 1, `ChunkStatus.CARVERS` at 2,
  `ChunkStatus.BIOMES` at 3 and `ChunkStatus.STRUCTURE_STARTS` from 4 out to 11
  — so radius 11, and 529 chunks. The twelve steps with their radius, executor
  and write radius are the table beside it, carried over unchanged from the
  figure it replaced.
- **`tickets-and-loading` figure 1** — redrawn to the page's hook: the two graphs
  are two arms that **join**, and a chunk is alive only where both agree. The
  arms are `ChunkMap.updateChunkScheduling` into `ChunkHolder.updateFutures`, and
  `DistanceManager.inBlockTickingRange` with `inEntityTickingRange`
  (`DistanceManager.java:164,168`). The three thresholds it used to draw are
  figure 2's alone now.
- **`game-events-and-vibrations` figures 1 and 2** — the 24-node cascade split at
  the joint the prose names: the dispatcher's walk, then one listener's five
  refusals in the order they run, with one shared sink and the step-on arm drawn
  as the short path it is. That arm asserts that `SculkSensorBlock.stepOn`
  reaches `VibrationSelector.addCandidate` through
  `VibrationSystem.Listener.forceScheduleVibration` (`VibrationSystem.java:305`)
  having asked only *not a warden*, `SculkSensorBlock.canActivate` and
  `VibrationSystem.User.canReceiveVibration` (`SculkSensorBlock.java:104-121`).
- **`lighting` figure 2** — redrawn around the two maps: all three stages
  (`LightEngine.checkNode`, `LightEngine.propagateDecreases`,
  `LightEngine.propagateIncreases`) write
  `LayerLightSectionStorage.updatingSectionData`, and the single arrow out of it
  is the publish. The `checkNode` edge is the one the queue said was missing.
  Also checked and left: *a window of up to 1,000* is `runUpdate`'s own
  `Math.min` against 1000 (`ThreadedLevelLightEngine.java:219`).
- **`fluids` figures 2 and 3** — split at `FlowingFluid.tick`'s own two halves.
  Figure 3 asserts that an **empty** answer never reaches the same-state
  comparison the other two must pass, which is the structure of the if/else-if at
  `FlowingFluid.java:450-459`, and that only the changed-state arm books another
  tick.
- **`scheduled-ticks` figures 1 and 2** — split at the page's own bold claim,
  *the drain is server-thread only and booking is not*. Figure 1 draws the dedup
  refusal as an arrow of its own; figure 2 asserts that the two ways back to the
  index — the chunk not ticking, and the budget spent — are both *late, never
  lost*.
- **`chunk-storage` figure 1** — the three threads are the three semantic colour
  words (`server`, `worker`, `disk`), and the caption asserts that the server's
  share ends at the snapshot.
- **`chunk-storage` figure 3** — its caption asserts the content-and-pointer
  asymmetry: the under-256-sector arm writes the bytes before the header that
  names them, the 256-or-more arm writes the header first at a stub and lands the
  payload when the temp file is moved, and both meet at *the old sectors are
  freed last*.
- **Twenty-seven captions and nine lead-ins**, each a claim about what its figure
  shows.

## Pass 7, session C — Part III · The server: the figures *(2026-09-15)*

Six pages, twelve figures (ten before; two were split). Every figure captioned;
every figure now pointed at by a sentence; every name in every figure resolved
against the decompile (twelve gate failures and thirteen gate notes to none).
Nothing was moved between pages. The prose changed only where a caption, a
lead-in, or the one sentence a figure's name needed required it — plus the three
answers under *Corrections* and *New claims in prose*, each with the decompile
open.

### The part-wide finding, which is the entry pass 9 should read first

**Twelve messages across all six pages were labelled with the *caller's* method
and drawn arriving at the *callee*.** Every one failed `check_figure_names.py`,
and every one was a claim about who does what. Each is now the receiver's own
method, re-derived:

- `server/how-a-server-dies` — `MS->>SL: saveAllChunks` → `save`.
  `MinecraftServer.saveAllChunks` calls `level.save(null, flush, …)`
  (`MinecraftServer.java:637`); `ChunkMap.saveAllChunks` is two calls further
  down and stays in the label as prose.
- `server/server-level-tick` ×2 — `SL->>SCC: sendBlockUpdated` → `blockChanged`.
  `ServerLevel.sendBlockUpdated` calls `this.getChunkSource().blockChanged(pos)`
  (`ServerLevel.java:1200`).
- `server/server-level-tick` — `SCC->>CH: broadcastChangedChunks` →
  `broadcastChanges`. `ServerChunkCache.broadcastChangedChunks`
  (`ServerChunkCache.java:365`) calls `ChunkHolder.broadcastChanges`
  (`ChunkHolder.java:187`).
- `server/players-and-sessions` — `SL->>CM: onTrackingStart` → `addEntity`, then
  `updatePlayerStatus`. `ServerLevel.EntityCallbacks.onTrackingStart`
  (`ServerLevel.java:2048`) calls `ServerChunkCache.addEntity`, which reaches
  `ChunkMap.addEntity` (`ChunkMap.java:1280`); `ChunkMap.updatePlayerStatus` is
  `ChunkMap.java:1141`.
- `server/players-and-sessions` — `PL->>SGPL: sendLevelInfo` → the packets
  themselves. `PlayerList.sendLevelInfo` (`PlayerList.java:700`) is the caller.
- `server/players-and-sessions` — `SLPL->>SCPL: handleLoginAcknowledgement` →
  `startConfiguration`. `ServerLoginPacketListenerImpl.handleLoginAcknowledgement`
  (`ServerLoginPacketListenerImpl.java:264`) is the caller.
- `server/players-and-sessions` — `SCPL->>PST: returnToWorld` → `start`.
  `ServerConfigurationPacketListenerImpl.returnToWorld`
  (`ServerConfigurationPacketListenerImpl.java:104`) builds the task, appends a
  `JoinWorldTask` and calls `startNextTask`.
- `server/players-and-sessions` — `SCPL->>PL: handleConfigurationFinished` → the
  two checks it makes. The method is SCPL's own
  (`ServerConfigurationPacketListenerImpl.java:166`).
- `server/server-tick` — `MS->>Conn: resumeFlushing` moved to a new `SGPL` lane.
  `resumeFlushing` is `ServerCommonPacketListenerImpl.java:157`, reached as
  `player.connection.resumeFlushing()` (`MinecraftServer.java:1281`), where
  `ServerPlayer.connection` is a `ServerGamePacketListenerImpl` and not a
  `Connection`.
- `server/starting-a-server` ×2 — `MS->>SL: createLevels` / `prepareLevels` →
  what `ServerLevel` actually receives. Both are `MinecraftServer`'s own
  (`MinecraftServer.java:449`, `:580`), and `MinecraftServer.loadLevel` is three
  calls, not two (`:425`).

**`spawnPlayer` was the one that looked wrong and was right**:
`PrepareSpawnTask.spawnPlayer` is real
(`server/network/config/PrepareSpawnTask.java:123`) and calls
`PlayerList.placeNewPlayer` at `:242`. The queue had it down as a naming slip.

### Corrections (a figure against the decompile, or against the page beside it)

- `server/server-level-tick`, figure 1 — the node read
  *`ServerLevel.runBlockEvents`, then `handlingTick` goes false — **running***.
  `ServerLevel.handlingTick = false` sits **outside** the `runs` guard
  (`ServerLevel.java`, after the `blockEvents` push): only `runBlockEvents` is
  gated. The gates table now carries them as two rows, one ticked and one blank.
- `server/starting-a-server`, figure 1 — the `Worker-->>WL` return was labelled
  *the stages that must be single-threaded come back to main*. It does not reach
  `Main`: the arrow that does is `WL->>Main`, which was labelled
  `createResourceManager`. `WorldLoader.load` takes a background executor and a
  main-thread executor, and it is the main-thread one that runs the pack-opening
  stage and the final assembly (the page says so at *The world load turns the
  main thread into an executor*). The two labels are swapped to what their own
  arrows carry.
- `server/how-a-server-dies`, figure 1 — `saveDataTag` and
  `SavedDataStorage.saveAndJoin` were drawn as siblings of the flush save. All
  three are **inside** `MinecraftServer.saveAllChunks`
  (`MinecraftServer.java:628–665`): the per-level `save`, then
  `storageSource.saveDataTag`, then `savedDataStorage.saveAndJoin()` under
  `if (flush)`. Redrawn as a shaded band naming the one call, which is what
  makes *after `level.dat` and not before* structural rather than asserted.
- `server/how-a-server-dies`, figure 2 — the watchdog figure had **no `Disk`
  lane**, so beside figure 1's four writes it read as *the watchdog writes
  nothing*, which contradicts the page's own comparison table (*is a crash
  report written: yes*). `ServerWatchdog.run` does both
  `Bootstrap.realStdoutPrintln` and `report.saveToFile(…/crash-reports/…)`
  before `exit()` (`ServerWatchdog.java:61–68`). A `Disk` lane and one message
  added; the closing note now says *nothing **more*** is written.
- `server/how-a-server-dies`, figure 1 — the drain loop's single arrow put
  `MinecraftServer`'s own deadline push on `ServerChunkCache`'s lane and omitted
  `MinecraftServer.waitUntilNextTick`, which the prose calls part of the same
  loop body. The real body is three steps (`MinecraftServer.java:714–730`) and
  is drawn as three.
- `server/players-and-sessions`, figure 2 — the tab-list order was one arrow.
  `PlayerList.placeNewPlayer` sends `createPlayerInitializing(this.players)`,
  **then** `this.players.add(player)`, **then**
  `broadcastAll(createPlayerInitializing(List.of(player)))`
  (`PlayerList.java:194–196`) — and the middle step is the one the page calls
  deliberate. Drawn as three beats, the middle one a self-message.

### Orderings the redrawn figures assert

- `server/README` figure 1 — the nodes are numbered to the **watch** order
  (tick, level, players, start, death) and the arrows are the **run-time**
  hand-off; the caption says which is which. Claim: `Start → Tick`,
  `Tick ⇄ Level`, `Tick ⇄ Players`, `Tick → Death`, and that the loop's
  *finally* is what two of the three endings reach.
- `server/server-tick` figure 1 — six lanes; `ServerGamePacketListenerImpl`
  replaces `PlayerChunkSender` (which the cast never listed, while the listener
  it does). Asserted: `suspendFlushing` on every player before the levels;
  `ServerLevel.tick` per dimension; `ServerConnectionListener.tick` reaching
  `Connection.tick`, which does `Connection.flushQueue`, then the listener's own
  `tick`, then the channel flush (**flush one**); then per player the chunk batch
  and `resumeFlushing`, which itself calls `Connection.flushChannel` (**flush
  two**). The band is `MinecraftServer.tickChildren`'s extent
  (`MinecraftServer.java:1205–1282`).
- `server/server-tick` figures 2 and 3 — the old fourteen-edge cascade split at
  `MinecraftServer.pollTaskInternal`'s own joint. Figure 2 asserts that
  `BlockableEventLoop.pollTask` runs the head for exactly three reasons —
  blocking depth above zero, older than three ticks, or `haveTime` — and that an
  empty queue and a head that may not run reach the same outcome. Figure 3
  asserts the guard `isSprinting() || shouldRunAllTasks() || haveTime()` before
  any level's chunk source is offered a turn (`MinecraftServer.java:994–1011`).
- `server/server-level-tick` figure 1 — the twenty-two steps in order, with the
  six inside `ServerChunkCache.tick` drawn as a subgraph. Claim: those six and
  only those six are that call's insides
  (`ServerChunkCache.java:324–343`; `clearCache` is the seventh and is not a
  step of the world advancing, so it is not drawn — a deliberate omission).
  The gates table beside it is twenty-one rows of three columns, every cell
  re-derived from `ServerLevel.tick`.
- `server/server-level-tick` figure 2 — three bands (before the tick, inside
  `ServerChunkCache.tick`, several steps later); the `ChunkMap` lane is gone and
  its one message is a note. Claim: `ChunkHolder.broadcastChanges` emits the
  light packet **only if either light filter has anything in it** — the prose
  said so and the old figure drew it unconditional.
- `server/players-and-sessions` figure 1 — the ticket message is now
  `PLAYER_SPAWN at radius 3, through its chunk source`; the wait is a band.
- `server/starting-a-server` — one figure became two, split at the note bar the
  old figure already drew. Figure 2 asserts `MinecraftServer.loadLevel` is
  `createLevels`, `forceDifficulty`, `prepareLevels` — three calls, where the
  old figure drew two — and that the optional listeners are each conditional.

### New claims in prose (three sentences, each with the decompile open)

- `server/players-and-sessions` — "`TicketType.PLAYER_SPAWN` is registered with
  a timeout of twenty ticks and with `TicketType.FLAG_LOADING` as its only flag,
  so `TicketType.canExpireIfUnloaded` is false and the timeout does not begin
  while the chunks it asked for are still on their way — which is what lets
  `ServerChunkCache.addTicketAndLoadWithRadius` accept this type at all, since
  it throws for any type that could expire before it loads."
  (`TicketType.java:18, 48`; `ServerChunkCache.java:514–520`.) This answers
  pass5.md's open question about what holds the chunks before `Ready`.
- `server/players-and-sessions` — "The last thing `PlayerList.sendLevelInfo`
  sends after it is `ClientboundGameEventPacket.LEVEL_CHUNKS_LOAD_START`, which
  is the client's signal to stop waiting and start drawing whatever terrain
  arrives." (`PlayerList.java:712`.) The name was in the figure and nowhere in
  the prose.
- `server/players-and-sessions` — the disambiguation that
  `NotificationManager.playerJoined` (`PlayerList.java:202`) is **not** the chat
  join message, which is broadcast at `:185`, twenty lines above and before
  `addNewPlayer`. The page used near-identical words for both.
- `server/how-a-server-dies` — the parked-ticket map "is the map that the flush
  save below writes out as the dimension's *chunk_tickets* saved data, under
  `TicketStorage.TYPE`" (`TicketStorage.java:41`). The figure asserted
  *chunk_tickets* and no sentence on the page did.

### Not a correction, recorded because a reader will ask

`MinecraftServer.MAX_TICK_LATENCY` is declared `= 3` (`MinecraftServer.java:217`)
and **read nowhere**: `MinecraftServer.shouldRun` uses the literal
(`:982–983`). The page's *older than `MinecraftServer.MAX_TICK_LATENCY` (three)
ticks* is true in value and names the policy, so it stands; the figure's edge
label now says *older than three ticks*. This is the same shape as
`entity-lifecycle`'s *three constants nobody reads*, and pass 9 may want to
decide whether the book states it here too.

## Pass 7, session B — Parts I and II: the figures *(2026-09-15)*

Every figure on the eleven pages of Parts I (anatomy) and II (foundations) was
looked at rendered, at the reading column, beside its section — eighteen mermaid
figures and one generated map. Fourteen were redrawn, two were split in two, one
was cut back, two gained a kind the book had never used, and all nineteen gained
a caption. **A caption is a claim about what the figure shows**, so every one of
the nineteen is on this list by being a caption; below are the ones where
something else changed too.

### Corrections — the figure disagreed with the decompile

1. **`systems/foundations/identifiers-and-registries.md`, figure 1.** The figure
   had `BuiltInRegistries` triggering `Items` class init, labelled *the ITEM
   loader touches `Items.AIR`*. The decompile has `Bootstrap.bootStrap` calling
   `FireBlock.bootStrap` and `ComposterBlock.bootStrap` — the latter reading
   `Items.JUNGLE_LEAVES` and eighteen more leaf items — before it calls
   `BuiltInRegistries.bootStrap` at all, so `Items` is already initialised when
   `BuiltInRegistries.createContents` runs the ITEM loader: the loader *reads*
   `Items.AIR`, it does not trigger the class init. The page's own prose said so
   and the figure said the other thing.
   `net/minecraft/server/Bootstrap.java:46-66`,
   `net/minecraft/core/registries/BuiltInRegistries.java:195-197, 382-386`,
   `net/minecraft/world/level/block/ComposterBlock.java:68-85`. Fixed in the
   figure (a note naming the two bootstraps) and in the prose, which now names
   `ComposterBlock.bootStrap` in its list and says what `createContents` finds.
2. **`systems/foundations/identifiers-and-registries.md`, figure 2 (now 3).**
   Three of the four configuration packets were drawn leaving
   `ServerConfigurationPacketListenerImpl`. `SynchronizeRegistriesTask` sends
   `ClientboundSelectKnownPacks`, every `ClientboundRegistryDataPacket` and
   `ClientboundUpdateTagsPacket`; only `ClientboundFinishConfigurationPacket` is
   the listener's.
   `net/minecraft/server/network/config/SynchronizeRegistriesTask.java:33, 36-49`,
   `net/minecraft/server/network/ServerConfigurationPacketListenerImpl.java:150-168`.
   The task is now a lane, which the key already held as `SRT`.
3. **`systems/foundations/data-driven-types.md`, figure 2.**
   `LootItemFunctions.compose` was drawn as an arrow *from*
   `SetItemCountFunction`. It is called by the `LootTable` constructor.
   `net/minecraft/world/level/storage/loot/LootTable.java:60-66`,
   `net/minecraft/world/level/storage/loot/functions/LootItemFunctions.java:77`.
   Queue entry [pass5.md](pass5.md):5108, re-derived and fixed.
4. **`systems/foundations/data-components.md`, figure 1.** One arrow, pointing
   one way, labelled *asPatch and fromPatch*, and leaving the patch field.
   `PatchedDataComponentMap.asPatch` is an instance method returning a
   `DataComponentPatch`; `PatchedDataComponentMap.fromPatch` is a static factory
   taking a prototype and a patch and returning the map. Two operations, two
   directions, and both on the map.
   `net/minecraft/core/component/PatchedDataComponentMap.java:35, 240`.
5. **`systems/foundations/resource-system.md`, figure 3.** One arrow carried
   *isDone, checkExceptions, then allChanged or rollbackResourcePacks* from
   `LoadingOverlay` to `Minecraft`. `LoadingOverlay` calls `ReloadInstance.isDone`
   and `ReloadInstance.checkExceptions` on the instance and only then accepts the
   callback into `Minecraft` — two targets merged into one message.
   `net/minecraft/client/gui/screens/LoadingOverlay.java:133-138`,
   `net/minecraft/server/packs/resources/ReloadInstance.java:11-15`. Also in that
   figure: `SimpleReloadInstance`'s construction was drawn *after* `setOverlay`,
   where `net/minecraft/client/Minecraft.java:1071` evaluates `createReload` as
   the argument to it; and the barrier resolution was drawn `Worker` to
   `Minecraft`, where the barrier is the reload instance's and its `wait` posts
   the task.
6. **`systems/anatomy/anatomy.md`, figure 1.** `MinecraftServer` and
   `IntegratedServer` were two lanes exchanging *runServer calls initServer* — a
   virtual dispatch drawn as a message between two objects. `spin` is static on
   `MinecraftServer`, `runServer` is `MinecraftServer`'s and `initServer` is
   abstract there and implemented on `IntegratedServer`: one object.
   `net/minecraft/server/MinecraftServer.java:305, 392, 783-785`,
   `net/minecraft/client/server/IntegratedServer.java:86`. Queue entry
   [pass5.md](pass5.md):5085.
7. **`systems/anatomy/anatomy.md`, figure 1.** The figure's last two arrows had
   the handshake and the login walk arriving at `ServerConnectionListener`, which
   binds channels and installs pipelines and handles no packet.
   `net/minecraft/server/network/ServerConnectionListener.java:60-148`. The walk
   is now a self-message on `Connection`, which is what swaps the listener, and
   `protocol-phases` still owns the phases themselves.
8. **`systems/foundations/codecs-nbt-json.md`, figure 1.** Two message heads
   named the *caller's* method: `saveWithFullMetadata` on an arrow to
   `TagValueOutput` (the call there is `TagValueOutput.createWithContext`) and
   `saveAdditional` on an arrow to `ContainerHelper` (the call is
   `ContainerHelper.saveAllItems`).
   `net/minecraft/world/level/storage/TagValueOutput.java:31, 192`,
   `net/minecraft/world/level/block/entity/ChestBlockEntity.java:128-132`,
   `net/minecraft/world/ContainerHelper.java:25-29`.
9. **`systems/foundations/codecs-nbt-json.md`, figure 3.** `HashedStack` was
   drawn sending a `ServerboundContainerClickPacket`; the sender is
   `MultiPlayerGameMode`
   (`net/minecraft/client/multiplayer/MultiPlayerGameMode.java:512`). And
   `createSerializationContext` was drawn as something `ClientPacketListener`
   does to itself: it is the registry access's, called the same way on both sides
   — `net/minecraft/client/multiplayer/ClientPacketListener.java:452` and
   `net/minecraft/server/level/ServerPlayer.java:316` — which is the paragraph's
   bolded claim and was the half the figure did not show.

### Claims the redrawing asserts

- **`anatomy.md` figure 1** now asserts, in a two-branch `par`, that the Render
  thread's `BlockableEventLoop.managedBlock` loop and
  `IntegratedServer.initServer` run *at the same time*. The prose says
  "Meanwhile"; the old figure's strict top-to-bottom order said the opposite. The
  two `box` frames assert that `Main`, `Minecraft` and the client's `Connection`
  are the client and that `IntegratedServer` and `ServerConnectionListener` are
  the server. The `RenderSystem` lane and its one message were cut to a note.
- **`anatomy.md` figure 2** asserts two nestings: `Minecraft.runTick` contains
  the delta-tracker read, `PacketProcessor.processQueuedPackets`,
  `BlockableEventLoop.runAllTasks`, `Minecraft.tick` and `Minecraft.renderFrame`
  (`net/minecraft/client/Minecraft.java:1201-1310`); and
  `MinecraftServer.processPacketsAndTick` contains the queue drain and
  `MinecraftServer.tickServer`
  (`net/minecraft/server/MinecraftServer.java:1116-1128`). The wire and its four
  crossing arrows were **cut** from the figure and are carried by the paragraph
  that owns them; the loss is logged in [pass5.md](pass5.md). Two names the
  figure alone had carried — `Minecraft.renderFrame` and
  `BlockableEventLoop.runAllTasks` — were given their sentence in *The frame
  loop*.
- **`foundations/README.md`**'s figure asserts the same ten dependencies as
  before with every label shortened; nothing was added, removed or reversed, and
  the direction went `BT` to `TD` with each arrow still running from the
  machinery to the page that takes it for granted.
- **`identifiers-and-registries.md` figure 2 (new)** asserts that
  `RegistryDataLoader.load` makes one `RegistryLoadTask` per `RegistryData`, that
  any task's `ConcurrentHolderGetter` is reachable from any other and hands back
  an unbound `Holder.Reference`, and that the freeze is where those promises are
  bound — the page's own *Loading is a task graph* paragraph, drawn instead of
  told in a label. It also asserts `LayeredRegistryAccess.replaceFrom` is the one
  call that installs both layers, and puts it outside the *on the worker pool*
  note, which the old figure had covering it.
- **`identifiers-and-registries.md` figure 3** adds one claim the old figure
  stopped short of: with an `IntegratedServer`, the `RegistryAccess.Frozen` the
  client just built is discarded for the server's, filtered to the same key set
  (`net/minecraft/client/multiplayer/ClientConfigurationPacketListenerImpl.java:174-184`).
  The prose already said it.
- **`resource-system.md` figure 1** adds two edge labels (*checkExceptions finds
  none* and *a listener threw*) and one edge: the rollback runs the reload again
  from discover. **Figure 2** adds a `prepareSharedState` node before the prepare
  box, splits the one dotted *shared state* edge into two (published in the first
  pass, completed during prepare), replaces three edges from the gate to the
  three applies with one edge into the apply box, and adds a *seventeen more
  listeners* node. **Figure 3** drops the `PackRepository` lane into a
  self-message.
- **`tags.md` figure 1** asserts nothing new. Two lanes and two notes were
  **cut** — the client's buffering at configuration and its apply after a
  `/reload` — because the *four moments* section above owns them and
  `identifiers-and-registries` figure 3 draws the packet. The closing note
  asserts an absence: the parrot's check reaches no registry.
  `MappedRegistry.refreshTagsInHolders`, which the figure alone had named, is now
  in *Prepared, then applied*.
- **`text-components.md` figure 1** is a `classDiagram`, the book's first, and
  asserts the triple: `MutableComponent` owns one `ComponentContents` and one
  `Style` and aggregates a list of `Component`. The codec node was **cut** — it
  is not one of the three things the heading counts, which is what the old figure
  got wrong about its own section — and so was the seven-kind subgraph, which the
  table below it carries with a column the figure could not.
- **`text-components.md` figure 2** puts the two `Language` lookups in the order
  the walk runs them (the killer's name is visited before the finished sentence
  returns) and adds a note that the server's only wording is
  `Component.getString` for the console log.
- **`data-components.md` figure 1** is the second `classDiagram`, and asserts
  that many stacks read one prototype and none may write it. **Figure 2** drops
  the `AbstractContainerMenu` lane on F7's rule that a subclass and its base are
  one lane: `EnchantmentMenu` is the menu that was clicked and the menu that
  broadcasts. `DataComponents.STORED_ENCHANTMENTS`, which the figure alone had
  named, is now in *The menu owns the mutation*, with
  `EnchantmentHelper.getComponentType` as its authority
  (`net/minecraft/world/item/enchantment/EnchantmentHelper.java:91-93`).
- **`data-driven-types.md` figure 2** adds one return arrow (the built function
  object back to the `LootTable`) so that `compose` can leave the table rather
  than the function.

### Not a page: the gate

`tools/check_figure_names.py` now reads a `<br/>` written tight against the text
on both sides as closed up (a name broken at a CamelCase boundary or a dot, which
F17 ruled and F18 sends part sessions to write in messages) and one with a space
on either side as a space (a clause break). Three probe cases prove it.
Corpus-wide unresolved names went 119 to 100 without a page outside Parts I and
II changing, so some of the 119 were the gate's misreading rather than the pages'.
Recorded in [pass5.md](pass5.md) for session O.

## Pass 7, session A — the standard, the theme and the exemplar *(2026-09-15)*

Ruled on F1–F16, added F17 and F18, rewrote [pass7-brief.md](pass7-brief.md)
Part 3 as the record, rewrote `TEMPLATE.md`'s *Figures* and *Lanes* to it,
adopted the figure theme (`mermaid-init.js`, now committed, and `custom.css`),
and rewrote the exemplar `systems/entities/entity-lifecycle`. **The exemplar is
where the claims are**: two of its three figures were replaced and one was cut
back, and every arrow that changed was re-derived against
`net/minecraft/world/level/NaturalSpawner.java`,
`net/minecraft/server/level/ServerChunkCache.java`,
`net/minecraft/server/level/ChunkMap.java`,
`net/minecraft/world/level/entity/PersistentEntitySectionManager.java` and
`net/minecraft/server/level/ServerLevel.java`.

### Claims introduced

- `systems/entities/entity-lifecycle` — **the spawn cascade is now two
  figures, and the second one loops.** The old figure drew every rejection
  below the position roll as a dead end into one sink, *this attempt is
  dropped*. The new figure 2 asserts a two-level loop: `while (groupCount < 3)`
  around an inner `while` bounded by `max`, so **most rejections cost one try
  and not one of the three group attempts** (`NaturalSpawner.spawnCategoryForPosition`,
  `NaturalSpawner.java:167-250`). Every arrow in it is one of these orderings:
  a failing test does `++ll; continue` (to *the next try*); an empty
  `NaturalSpawner.getRandomSpawnMobAt` and `Mob.isMaxGroupSizeReached` do
  `break label53` (to *the next group attempt*); a null from
  `NaturalSpawner.getMobForSpawn` and `clusterSize >= Mob.getMaxSpawnClusterSize`
  `return` (to *this category on this chunk is over*).
- `systems/entities/entity-lifecycle` — **the four scopes of a rejection**, the
  new figure 1 and the fourth column of the new table. The claim per scope:
  `NaturalSpawner.getFilteredSpawningCategories` drops a category for the whole
  tick (`ServerChunkCache.tickChunks` builds the list once,
  `ServerChunkCache.java:395`); `ChunkMap.collectSpawningChunks` and
  `ServerLevel.canSpawnEntitiesInChunk` drop a chunk for every category
  (`ChunkMap.java:1017`, `ServerChunkCache.java:440`); everything from
  `NaturalSpawner.SpawnState.canSpawnForCategoryLocal` down is inside
  `NaturalSpawner.spawnForChunk`'s per-category loop and so ends only this
  category on this chunk (`NaturalSpawner.java:130-150`).
- `systems/entities/entity-lifecycle` — **the new table, *What each test drops,
  in the order it runs*, is fifteen claims**, one per row: the test, the
  condition, and the scope. Thirteen of the conditions were the old figure's
  edge labels, moved word for word; two are new (`Mob.isMaxGroupSizeReached`
  and `Mob.getMaxSpawnClusterSize`, which the prose already had at *What
  finalizeSpawn settles* but the figure did not).
- `systems/entities/entity-lifecycle` — the opening paragraph now says each of
  the three group attempts "makes a handful of tries that jitter only x and z",
  where it said the three attempts themselves jitter. The inner bound is
  `Mth.ceil(level.random.nextFloat() * 4.0F)` until a species is picked and the
  group-size roll after it (`NaturalSpawner.java:180, 205`).
- `systems/entities/entity-lifecycle` — **the entry sequence now draws the
  callback hop**: `PersistentEntitySectionManager.startTracking` and
  `.startTicking` are private and raise `LevelCallback.onTrackingStart` and
  `LevelCallback.onTickingStart`, which `ServerLevel.EntityCallbacks` implements
  as `ServerChunkCache.addEntity` and `EntityTickList.add`
  (`PersistentEntitySectionManager.java:124-139`, `ServerLevel.java:2040-2049`).
  The old figure sent `startTracking` straight to the `ChunkMap` lane, which
  named a method `ChunkMap` does not have.
- `systems/entities/entity-lifecycle` — **four captions, and a caption is a
  claim**: figure 1's *three sizes of giving up*; figure 2's *only three of the
  eight leave the loop at all* and *a new group attempt puts x and z back at the
  roll*; figure 3's *the client is told in the middle: tracking, then the
  packet, then ticking*; figure 4's *these are a section's states, not an
  entity's*.

### Corrections (the decompile open)

- `systems/entities/entity-lifecycle`, the spawn figure — **the scope of three
  rejections was wrong.** `LocalMobCapCalculator.canSpawn` failing, the y roll
  landing at the world bottom and the redstone conductor at the rolled position
  were all drawn into *this chunk is skipped*. All three are inside
  `NaturalSpawner.spawnForChunk`'s loop over `spawningCategories`, so each ends
  **this category on this chunk** and the next category is still tried
  (`NaturalSpawner.java:130-157`, `ServerChunkCache.java:441`).
- `systems/entities/entity-lifecycle`, the spawn figure — **fourteen rejections
  were drawn as dead ends that are not.** Everything under the three group
  attempts except the two `break`s and the two `return`s is `++ll; continue`
  (`NaturalSpawner.java:243-245`), and the figure had no edge back at all.
- `systems/entities/entity-lifecycle`, the spawn figure — **two exits were
  missing**: `clusterSize >= mob.getMaxSpawnClusterSize()` returns from the
  whole call and `mob.isMaxGroupSizeReached(groupSize)` ends the group
  (`NaturalSpawner.java:227-232`). The prose had both at *What finalizeSpawn
  settles*; the figure ended at `Mob.finalizeSpawn`.
- `systems/entities/entity-lifecycle`, the entry sequence against the sentence
  under it — the page said "five of `LevelCallback`'s seven appear in the
  figure". One did: `LevelCallback.onCreated`. The other four were drawn under
  the manager's own private method names. `LevelCallback` declares seven
  (`LevelCallback.java`); the sentence now says which two the figure raises and
  what they reach.
- `systems/entities/entity-lifecycle`, the entry sequence — `startTicking` was
  drawn as `PersistentEntitySectionManager → EntityTickList`. The manager does
  not hold the tick list: `ServerLevel.EntityCallbacks.onTickingStart` does
  `ServerLevel.entityTickList.add` (`ServerLevel.java:2040-2042`). The arrow now
  goes through the `ServerLevel` lane.
- `systems/entities/entity-lifecycle`, the visibility state diagram against the
  sentence above it — the page says in italics that status is a property of a
  **section**, and all five transition labels said *it*, meaning one entity. The
  caption now says whose states they are.

### Cut, with the reason

- `systems/entities/entity-lifecycle`, the entry sequence — **the second half
  was cut** (`checkDespawn`, `tickNonPassenger`, `stopTicking`, `stopTracking`,
  `ClientboundRemoveEntitiesPacket`, `storeEntities`, and the three later note
  bars). It was the page's whole second half drawn three sections early, and
  the same transitions are the state diagram's subject (F11). Every fact in it
  is in the prose of *The tick it gets*, *Ending two* and the state diagram; the
  `Mob` and `EntityStorage` lanes went with it.
- `systems/entities/entity-lifecycle`, the state diagram — the `note right of H`
  ("hidden is not written yet…") was cut: mermaid drew it at the far left of the
  figure joined by a long dashed line, and *Ending two* says the same thing in
  prose. Its point is now the last clause of the figure's caption.

## Pass 7, the planning session — between passes 6 and 7 *(2026-09-14)*

**No page's prose was touched and no claim about the game was introduced.** One
generated page changed and one tool now feeds it, which is what pass 9 checks.

### The one change to a published page

- `src/reference/class-index.md` is **regenerated from two sources now** instead
  of one. `verify_names.py --index` still reads every backticked name on every
  hand-written page; it now also merges `check_figure_names.py`'s mentions —
  every class named inside a mermaid block, as a lane's expansion, a node label,
  a message, a note, a subgraph title or a state name. **139 page pairs were
  added** (750 classes are named in figures, across 109 pages), and the page's
  own preamble was rewritten to say so: it used to state that a class named only
  in a diagram is outside the index, which was true and is now false. **What
  pass 9 should check**: that the added rows are real — that the class exists
  (the figure parser resolves every name against the same decompile index, and
  119 names in figures do *not* resolve and are therefore absent from the
  index, which is the gate's own report), and that the preamble's two sentences
  match what the two parsers actually do.

### Claims introduced elsewhere, all of them about the book rather than the game

- [pass7-brief.md](pass7-brief.md) Part 3 and Part 4 carry **the measurements**:
  206 figures, 134 of 194 mermaid figures shrunk below their natural size, 89
  with type under 9px, 115 opening their section, 0 captioned, 51 pointed at by
  nothing, 139 introducing most of their names before the prose does, 151
  carrying a name the prose never says, 121 with a label that reads as a
  sentence, 119 names failing the new gate, 44 unused lane-key rows, 214
  figure-less sections over forty lines. Each is a tool's output at a stated
  revision and is re-derivable by re-running the tool; none is a claim about
  26.2. A pass-7 session that quotes one quotes it as *measured on 2026-09-14*.
- [plan.md](plan.md)'s *Where we are* states pass 6's device outcome — the
  closer 69 → 46 in one spelling, the trace heading 20 → 0, the blockquote 39 →
  43 all at the foot — from `pass6_shape.py --summary` run on the same day.

### Corrections

None. No fact about the game was changed.

## Pass 6, session N — the frame and Reference *(2026-09-14)*

Eighteen pages read, one agent each, under `docs/pass6-brief.md` Part 1: the
eleven hand-kept Reference pages, `src/introduction.md`, `src/lectures.md` and
the four atlas pages. The generated Reference views and the two indexes were
not read (they are rewritten on every deploy).

**The class to check first.** Most of what follows is one kind of error: **a
sentence that counts the text beside it and gets the count wrong**. Twenty-one
of them, in eighteen pages. None is a claim about the game, so pass 4's
protocol would not have caught any; each is checkable by counting the table
under it, which is what pass 9 should do on every page in this list before it
re-derives a game fact.

### Corrections — the counts, each re-derived by counting the page

- `src/reference/README.md`:9 — *Half of them are rewritten from the source on
  every deploy … the other half are read by a person* against a table of 23
  rows that splits **13 generated / 10 hand-kept**. Now stated as thirteen and
  ten, and `src/introduction.md` (which said *rather more than half*) now says
  the same two numbers.
- `src/reference/README.md`:84 — *It disagreed in six of twenty rows when the
  check was written*. `check_deps.reference_column` compares every row matching
  `REF_ROW`, which is all twenty-three today; the twenty was the table's size
  on the day pass 5's session N wrote it. Now *six rows on the day the check
  was written*, with no phantom population.
- `src/reference/README.md`:45–69 — the *kept by* column carried four values
  (*generated*, *hand-kept*, *generated from the lane key*, *generated from the
  pages*) where the figure above it draws three groups and the prose splits two
  ways. Now three values matching the figure: *generated · decompile*,
  *generated · corpus*, *hand-kept*.
- `src/reference/level-data-and-rules.md`:13 — *the rest are one line each
  because one line is all there is*. Every section after the table is
  multi-paragraph prose; no section is one line. Now names the six sections and
  says what a row with no section below it means.
- `src/reference/level-data-and-rules.md`:197 — *is the one entry below that is
  not a packet* indexes a list that is not on the page.
- `src/reference/level-data-and-rules.md`:65 — *about ten fields*, then ten
  named. `PrimaryLevelData` has **eleven** instance fields
  (`PrimaryLevelData.java`:39–49); the eleventh,
  `PrimaryLevelData.worldGenSettingsLifecycle`, is now named.
- `src/reference/level-data-and-rules.md`:178 — *the two rules screens*, only
  one of which (`InWorldGameRulesScreen`) the page ever names. The other is
  `WorldCreationGameRulesScreen`; both extend `AbstractGameRulesScreen`.
- `src/reference/block-update-flags.md`:29 — *the two large ones are worth
  decomposing here rather than in the reader's head*, above a table whose *the
  bits* column decomposes all four.
- `src/reference/hud-elements.md`:6 — *The HUD is one ordered method* against
  the page's own header (*from `Hud.extractRenderState` **and**
  `Gui.extractRenderState`*) and its second table.
- `src/reference/hud-elements.md`:22 — *Hidden in the last column* describes the
  second table's column order while standing over the first, where the column
  is fourth of five.
- `src/reference/hud-elements.md`:57 — *three of them are still `Hud` methods*,
  above a table that names no method. They are `Hud.extractSavingIndicator`,
  `Hud.extractDebugOverlay` and `Hud.extractDeferredSubtitles`
  (`Gui.java`, `extractRenderState`); the fourth is
  `ToastManager.extractRenderState`.
- `src/reference/density-function-nodes.md`:99 — *three unregistered
  singletons*, naming `DensityFunctions.BlendAlpha`,
  `DensityFunctions.BlendOffset` and `DensityFunctions.BeardifierMarker`, all
  three of which the page's own main table lists as **registered** ids
  (*blend_alpha*, *blend_offset*, *beardifier*). The word *unregistered* also
  means something else twenty lines above, where it is right. What is true of
  the three is that they are singletons resolved by object identity.
- `src/reference/naming-drift.md`:42 and :385 — *two hundred and forty-five
  rows*; counting every data row in the thirteen drift tables gives **247**.
- `src/reference/naming-drift.md`:44 and :284 — the rendering table at
  *twenty-seven rows*; it has **28**.
- `src/reference/naming-drift.md`:385 — *a dozen of these rows are one design
  change each*, introducing **seven** bullets.
- `src/maps/README.md`:7 — *Each map is a figure … and then the table the
  figure was drawn from*, against a figure on the same page saying eight SVGs
  and six tables. The truth is eight SVGs (seven of them the atlas's — the
  eighth, `tree-EntityRenderState.svg`, belongs to `entity-rendering`) and
  **seven** generated tables.
- `src/maps/biggest.md`:3 — the header says *the thirty largest classes*; the
  page's table is **forty** rows and only the figure is thirty.
- `src/maps/fanin.md`:45 — *Three rows of the chart are worth a second look*,
  introducing five names, two of which are in the table the sentence excludes.
  The page's own arithmetic was sound (24 of the thirty in the table, three in
  each of two paragraphs); the words were not.
- `src/maps/fanin.md`:25 — the grouping table was said to hold twenty-four of
  the thirty; it holds **thirty-two names**, the extra eight being ranks 31–60
  kept so a family is not broken (re-derived from `src/generated/fanin.md`).
- `src/maps/packages.md`:5 — *the first surprise in it is which half is bigger*,
  answered in the next clause with a near-third and seven tenths.
- `src/maps/packages.md`:24 against :50 — `net/minecraft/client` given as 1,864
  classes and then as 41, thirty lines apart, without the page saying that the
  second is the *itself only* count its own convention paragraph defines.
- `src/maps/hierarchy.md`:5 — *`Block` has 293 subclasses* against :39 *92
  direct subclasses* and :47 *`Block` is [`BlockBehaviour`'s] only subclass*.
  293 is the descendant count, which is the word both tables use.
- `src/lectures.md`:19 against :461 — two lists both claiming to be *the three
  worth taking out of turn*, differing in their first member (*environment
  attributes and timelines* against *blocks and states*). There is one
  departure from the sidebar order and three pages a single-part viewer fetches.
- `src/lectures.md`:80 against :96 — *the last four can be watched in any order*
  against the entry two lines below saying fluids assumes scheduled ticks.
- `src/lectures.md`:196 — *Two groups have an internal order*, one of which
  (player anatomy → the two-phase tick) is the trunk and not one of the four.
- `src/lectures.md`:246 — *With one exception, nothing here hands off to
  anything*; the exception is never named.
- `src/lectures.md`:320 against :340 — Part XII partitioned as *a substrate, a
  pipeline, and a wing* and then as 1–6 / 7–9 / 10, which do not cover the same
  ten lectures: lecture ten is in none of the first three.
- `src/introduction.md`:52 — *Four threads carry nearly all of it* above a
  figure that labels three threads and draws the connection as *the wire*.
  Fixed in the figure's label rather than in the sentence.
- `src/introduction.md`:95 — *Twenty-three pages* followed by a list of about a
  dozen items, which reads as the twenty-three.

### Corrections — facts, re-derived against the decompile

- `src/reference/level-data-and-rules.md`:305 — **"so peaceful stops the
  spawner rather than the mobs" is the wrong way round in 26.2.**
  `MinecraftServer.setDifficulty` does call
  `MinecraftServer.updateMobSpawningFlags`, but that method pushes
  `ServerLevel.isSpawningMonsters` into each level, and `ServerLevel.java`:1901–1903
  shows it is `GameRules.SPAWN_MOBS && GameRules.SPAWN_MONSTERS` and reads the
  difficulty nowhere. Difficulty is spent on the mobs instead: `Mob.checkDespawn`
  (`Mob.java`:759–761) discards a mob that is not
  `EntityType.isAllowedInPeaceful` on its next despawn check, and
  `EntityType.java`:284 gates the spawn attempt. So peaceful empties the world
  and the two game rules empty the spawner. **This is a 1.21 fact surviving
  inside a chain of correct 26.2 method names**, which is why two fact-checks
  kept it.
- `src/reference/level-data-and-rules.md`:197 — *it pushes the two spawn flags
  down instead*. `Level.setSpawnSettings` (`Level.java`:537) takes **one**
  boolean; the *two* are the two game rules `ServerLevel.isSpawningMonsters`
  ANDs into it.
- `src/reference/math-and-primitives.md`:182 — *so most of a new world's
  generation is legacy, not Xoroshiro*. The four shipped noise settings with
  `legacy_random_source: true` are *caves*, *end*, *floating_islands* and
  *nether* (`reference/26.2/data/minecraft/worldgen/noise_settings/`); the
  overworld, *amplified* and *large_biomes* are false. An ordinary world's
  overworld is Xoroshiro and the two dimensions behind a portal are legacy, so
  a count of four in seven does not support a claim about *most of a new
  world's generation*. Line 248 stated the same fact more narrowly and was also
  not quite right (*which the nether and the end have* implies the rest do not
  opt in; two presets do).
- `src/reference/threads.md`:54 — *Four kinds of thread on a dedicated server
  are non-daemon*, against the page's own **main (dedicated)** row marked
  daemon **no**. Five rows are non-daemon; main returns immediately after
  `Runtime.getRuntime().addShutdownHook` (`server/Main.java`:236) and cannot
  hold the JVM open.
- `src/reference/threads.md`:73 — the same row said main runs
  *`MinecraftServer.spin` and the shutdown hook*. It **registers** the hook;
  the hook runs on its own *Server Shutdown Thread* (`server/Main.java`:228–236),
  which the page's own *Situational threads* paragraph already knew.
- `src/reference/non-living-damage.md`:68 — *they are why several rows below
  read `nothing`: the class was never reached*, with no row marked. Exactly
  three of the ten are: `Interaction` (`Entity.skipAttackInteraction`),
  `EyeOfEnder` (`EyeOfEnder.java`, `isAttackable()` returns false — the page's
  row gave no reason at all) and `AbstractHurtingProjectile` (deflected by
  `Player.deflectProjectile`, which fires only for
  `EntityTypeTags.REDIRECTABLE_PROJECTILE`). `PrimedTnt` overrides
  `Entity.isPickable`, not either gate, and the other six are reached and do
  nothing.
- `src/reference/density-function-nodes.md`:88 — *All six installed classes
  implement `DensityFunctions.MarkerOrMarked`, so … the graph would
  re-serialise unchanged*, stated without the exception the table two lines
  below states: `NoiseChunk.wrapNew`'s `BlendDensity` case installs the
  marker's own child when the level's `Blender` is empty, and a child does not
  re-serialise as *blend_density*.
- `src/maps/hierarchy.md`:11 — *so it inherits the whole block tree and the
  whole item tree at once*, of `FeatureElement`, an interface. Its implementers
  inherit from it; what sweeps up the two trees is its **descendant count**.
- `src/reference/naming-drift.md`:151 against :511 — *Material* given two
  verdicts, *gone* and *survived and changed meaning*. Both are true of
  different classes: the block property is gone, and
  `net/minecraft/client/resources/model/sprite/Material` exists. The drift row
  now says so.
- `src/reference/glossary.md` *Render state* against *Extract* — the same rule
  stated with its exception in one entry and without it in the other (*the
  drawing half reads no game object* against *no live game object from
  `LevelRenderer.render` down — the top of the render half still does*).
- `src/reference/glossary.md` *Batch* — *a group of game tests keyed by the
  environment they share* and then *a batch **is** an environment*.
- `src/reference/submit-phases.md`:100 — *That list is the answer to what can
  be drawn in a level*, dropping the five exclusions the page's own opening
  makes (sky, clouds, weather, world border, terrain).

### Claims introduced

**`src/introduction.md`.**

- *This site is the notes for a video lecture series* — new, and the page's
  largest previously unstated premise. Also *nothing on it leans on the video
  to make sense*, which restates the owner's 2026-09-05 ruling.
- *It ticks too, nought to ten times inside each frame, catching its own copy
  up to the same twenty-a-second clock* — new in the opening, reconciling the
  prose with the figure's *0 to 10 ticks*. Check against `Minecraft.runTick`.
- *Just under a third of **those lines** is client-only* — the population
  named. `src/maps/packages.md` says 212,242 lines, 29.5%.
- The skip list re-sorted into three kinds: *version differences by definition*
  (datafix, filefix), *not the game* (Realms, telemetry, the profiler, the
  management server, RCON, the data generators), *the game's bookkeeping rather
  than its behaviour* (statistics, player reporting, the id constants). Every
  membership is a claim.
- *Thirteen of the twenty-three … the other ten* for the Reference split.

**`src/lectures.md`.** Four per-part shape paragraphs cut to their order
claims (IV, XI, XII, XIII), each of which now asserts the order and no longer
the shape: Part IV *of the last four, 7 comes before 8*; Part II *3 to 7 have
no order among themselves — except that 7 … reads best last*; Part VIII *only
one of the four has an internal order*; Part X *nothing here hands off to
anything except lecture seven, which draws what lecture six opens*; Part XIII
*lectures 1 to 3, then 4 and 5, then the last four*. The *points of interest*
blurb is now an order claim: *Part VI's AI lecture reads this index*.

**`src/reference/README.md`.** *Nobody arrives at this shelf by walking it*;
*the table below is sorted for the one question a reader of a catalogue should
ask of it*; the three-value *kept by* taxonomy; *eleven of them from the
decompile's declaration lines … the other two are read off this book instead*.

**`src/reference/level-data-and-rules.md`.** A new section, *One method saves
all three*, asserting the order inside `MinecraftServer.saveAllChunks`
(`MinecraftServer.java`:628–664): the `ScoreboardSaveData` flush first, then
every level's chunks, then *level.dat* through
`LevelStorageSource.LevelStorageAccess.saveDataTag`, then
`SavedDataStorage.saveAndJoin` or `SavedDataStorage.scheduleSave` on the flush
flag; and that `MinecraftServer.saveEverything` wraps it with
`PlayerList.saveAll`. Also new: `LevelVersion`'s five components and what the
world-select screen reads from them; `LevelSummary.CorruptedLevelSummary` and
`LevelSummary.SymlinkLevelSummary`; and the `DimensionType` record as a
**sixteen**-component table in four groups, of which the glosses are claims —
`DimensionType.logicalHeight` as the ceiling `PortalForcer` and
`TeleportRandomlyConsumeEffect` clamp to, and `DimensionType.MonsterSettings`'s
two light tests.

**`src/reference/block-update-flags.md`.** The opening now states two surprises
as the hook: `Block.UPDATE_NONE` is 260 and not zero, and 512 is both
`Block.UPDATE_SKIP_ON_PLACE` and `Block.UPDATE_LIMIT`. New glosses: *none*
suppressing the client gate and the block entity's side effects, and
`Block.UPDATE_SKIP_ALL_SIDEEFFECTS` as what a structure or data-pack write
passes — both worth checking.

**`src/reference/threads.md`.** *Every lane in the figure has a row in the
table; two rows have no lane* — a claim about the figure and the table
together.

**`src/maps/`.** `maps/README`: *four figures and two tables on what extends
what, one and one on the two bar charts, one and three on where the code is*,
and *take them in any order; none of the four needs another*. `maps/fanin`:
the thirty-two / twenty-four / eight accounting. `maps/packages`: *the hatched
boxes are those three, and much the largest of them is the save-migration
history* — check against the treemap.

### For pass 9's attention, found and not fixed

- `src/reference/level-data-and-rules.md` — the *world spawn* row names
  `PrimaryLevelData.respawnData` while *The spawn every level reports is the
  server's* says every level reports `MinecraftServer.effectiveRespawnData`.
  Both are true (stored against reported) and the table gives no hint which it
  means.
- `src/reference/submit-phases.md`:91 — *twenty-four steps out and twenty-four
  back for its two faces, a hundred vertices in all*; 48 and 100 do not
  reconcile without a per-step vertex count the cell does not give.
- `src/reference/non-living-damage.md`:102 — *Only four classes read the damage
  amount at all*, counting `MinecartTNT`, whose own `MinecartTNT.hurtServer`
  reads only the arrow's speed and passes the amount straight to
  `VehicleEntity`. Re-derived and left: the fall-through does read it, and the
  page's row says so.
- `src/reference/density-function-nodes.md`:21 — *four arithmetic* in the
  census against :110's *the arithmetic family — the two-argument nodes, the
  mapped ones and clamp*. Two populations, one word.
- `src/maps/hierarchy.md`:80 — *Two trees the table shows and the figures do
  not* names `Goal` and `Packet`; the section heading is about the page's own
  apparatus rather than about the game.

## Pass 6, session M — Part XIII · Commands and data packs *(2026-09-14)*

All nine system pages rewritten and the landing page re-synced. Ten readers
under Part 1's brief, one per page, no source. **Six corrections**, four of
them found by a reader with no source; the rest is claims introduced.

### Corrections

- `advancements`:3 — the verified line said *"a cobblestone lands in your
  inventory and **one tick later** the toast appears"*, and the trace's own
  note four sections down says *"still the same tick"*. The decompile agrees
  with the note: in `ServerPlayer.tick`
  (`net/minecraft/server/level/ServerPlayer.java`), `broadcastChanges` is the
  fifth statement and `this.advancements.flushDirty(this, true)` is the last,
  so the award and the packet are the same tick. The one-tick delay the page
  *does* demonstrate belongs to `CriteriaTriggers.LOCATION`, which fires in
  `ServerPlayer.doTick` during the connection phase, after the flush has run —
  a different scenario. The line now reads *"the toast is on its way before
  that same tick ends"*.
- `advancements`:303 (was :254) — the page said `DisplayInfo`'s type is one of
  four. `AdvancementType` (`net/minecraft/advancements/AdvancementType.java`)
  is an enum of **three**: `TASK`, `CHALLENGE`, `GOAL`. Written as three, with
  the claim the sentence now carries: `AdvancementToast.getSoundEvent` returns
  `SoundEvents.UI_TOAST_CHALLENGE_COMPLETE` for a challenge and **null**
  otherwise, so a task and a goal toast in silence
  (`client/gui/components/toasts/AdvancementToast.java`:55–62); the same class
  gives a challenge its own title colour at :72.
- `entity-selectors`:96 — "a player sitting on the death screen is invisible
  to *@e* and still a target for *@a* and *@p*". Both `@e` and `@n` set
  `selectOnlyAlive` in `EntitySelectorParser.parseSelector`
  (`commands/arguments/selector/EntitySelectorParser.java`:262–273), and `@a`,
  `@p` and `@r` do not. Now "invisible to *@e* and *@n*, and still a target
  for *@a*, *@p* and *@r*".
- `entity-selectors`, the *Resolve* flowchart — the players-only node read
  "findPlayers — a linear walk of a player list, **always**", which a reader
  took as "players are not world-limited". `EntitySelector.findPlayers`
  (`commands/arguments/selector/EntitySelector.java`:234–253) branches on
  `isWorldLimited()` exactly as the entity path does — `sender.getLevel()
  .getPlayers` or `PlayerList.getPlayers` — and both branches are linear. The
  label now says "one level or every level, but a linear walk of a player list
  either way". **The figure's shape is still wrong** (it also skips the
  bare-name and UUID branches `findPlayers` takes) and is logged for pass 7.
- `permissions`:148–158 — "of the **ninety-one** gates that name a level
  constant … while `Commands.LEVEL_ALL` appears exactly twice" left two of the
  ninety-five unaccounted, with no sentence saying a remainder existed. The
  ninety-five `Commands.hasPermission` call sites are 66 `LEVEL_GAMEMASTERS`,
  16 `LEVEL_ADMINS`, 9 `LEVEL_OWNERS`, 2 ternaries (`SeedCommand`,
  `VersionCommand`), 1 `GameModeCommand.PERMISSION_CHECK` and 1
  `ClientPacketListener.RESTRICTED_COMMAND_CHECK`. The census now divides four
  ways and closes.
- `permissions`:115–118 — "the ops-file entry's own **stored set** wins" read
  against "*ops.json* stores a number" six lines later. Both are true of
  different things: `ServerOpListEntry`
  (`server/players/ServerOpListEntry.java`) holds a `LevelBasedPermissionSet`
  in memory, built in its JSON constructor from the integer `level` field, and
  serialises that integer back. Said so.

### Claims introduced

**`advancements`** — the trace heading is now *From a slot that changed to a
toast* (`glossary.md`:754 repointed). New: a bolded trace paragraph claiming
`AdvancementRewards` holds experience, loot tables, recipes and a function,
that the recipe field is how the recipe book is filled, and that the function
reward is a `CacheableFunction` resolved once (the last was moved from
`functions-and-macros`' citation target, which now points here). New section
*The table only shrinks, and the two things that refill it*, claiming
`/advancement revoke` and `/reload` are the only two things that re-subscribe
and that nothing the game does on its own does — moved out of the closer, with
`ImpossibleTrigger` and `PlayerAdvancements.checkForAutomaticTriggers` moved
in beside them. The tree-layout paragraph moved into *The screen at the other
end* and now asserts the layout is *why* every client sees the same tree.
Section order changed: client half, coverage note, closer, *Where to look*.
The cast's trailing sentence now claims the *side* column says where a class
runs rather than which jar holds it, and that `PlayerAdvancements` is outside
the 112.

**`brigadier-and-commands`** — split question re-asked and answered no (see
[pass5.md](pass5.md)). New claims: the three registered suggestion providers
are named as *ask_server*, *available_sounds* and *summonable_entities*, and
the five nodes that name one name **one of the two that mean anything** (3
available_sounds, 2 summonable_entities), the other 62 defaulting to
ask_server — a re-scoped statement of the same 67/5/62 count. New sentence
counting off the three parsers of the title. New: *context-aware* glossed at
first use as "the wire form carries no data of its own and the far side builds
the parser". The 38-vs-57 comparison re-scoped: 38 classes directly in
`commands/arguments` against 57 **entries** in `ArgumentTypeInfos`, with the
claim that one class may register several and a nested one none. *Where a
command's output goes* is now its own section; *The tree on the wire* gained
four H3s (anchor kept); `ClientboundCustomChatCompletionsPacket` moved from
the door section into the packet section.

**`dialogs`** — verified line's last clause changed from "it is not part of
Minecraft" to "no vanilla server will ever send it to you". New: the four
dialog registries named. New claim about `ActionTypes.bootstrap`
(`server/dialog/action/ActionTypes.java`:11–16): **seven** kinds are
registered in a loop over the click-event kinds and **two** by hand, under
*dynamic/run_command* and *dynamic/custom* — replacing "that set of nine is
derived from the click-event enum". New: the three packets registered in both
protocols named together. Trace heading *From a JSON file to a click the
server reads*. The four ways a dialog opens are now four bolded items; the
parts inventory moved to a new section *What a dialog is made of* (the
`functions-and-macros` citation repointed to it). *Game tests* named as the
other of the two clearest instances.

**`entity-selectors`** — the 1.21 blockquote moved from the body to the foot.
Two closer answers promoted to sections: *Four argument shapes, enforced on
the query and not on the text*, and *The client parses selectors and cannot
resolve one* (which now claims to be what the cast's "that matters later"
meant). New closer question claiming **`/kill @e[type=item,limit=1]` resolves
in the overworld** unless there is nothing there: `MinecraftServer.levels` is
a `LinkedHashMap` (`MinecraftServer.java`:335) with the overworld put in first
(:460) and the rest in registry order (:501), `getAllLevels` iterates it, and
an arbitrary-order limit reaches the level query as an early abort — so a
sort removes the bias. Cast cell re-scoped: `SetOnceOptionState` covers the
four options with **no parsed field to test for emptiness**, and the other
nine once-only options check their own field
(`EntitySelectorOptions.java`:111–177). Closer respelled to *Questions players
ask*.

**`functions-and-macros`** — the opening no longer calls the figure a
two-step model: two steps and a hand-off, and `## 3 · Queue` is now *Then:
queued, and gone* (`brigadier-and-commands` repointed). The cast table gained
its own heading. New paragraph in *What calls a function, and when* claiming
the page's own hook: nothing in `ServerFunctionManager.tick` carries an
argument compound, the snapshot means the failure repeats every tick, and
`/function` is the only way to see it. The *four that parse against a source*
lost its implied population.

**`game-tests`** — trace heading *One test, from a command to a green block*.
New: the four registries named (`Registries.TEST_INSTANCE`,
`Registries.TEST_ENVIRONMENT`, `BuiltInRegistries.TEST_INSTANCE_TYPE`,
`BuiltInRegistries.TEST_ENVIRONMENT_DEFINITION_TYPE`). New: the seven
environment kinds named and divided five / one / one
(`TestEnvironmentDefinition.java`:43–49). New claim resolving the page's
apparent self-contradiction about timeouts: `GameTestSequence.tickAndContinue`
catches `GameTestAssertException` only (`GameTestSequence.java`:92–97), while
a timeout is a `GameTestTimeoutException` raised by `GameTestInfo`
(`GameTestInfo.java`:156–164) and caught nowhere there. **New section
paragraph** *What a test leaves behind is not undone*: a passing test has its
barriers removed (`GameTestRunner.java`:142) and nothing else; a failing one
keeps its shell; the pasted blocks, the test instance block and the
force-loaded chunks (`TestInstanceBlockEntity.java`:404–412) stay; `/test
clearall` (`TestCommand.java`:334) clears space, removes barriers and breaks
the block. Heading *Two things a running server should know* → *Three*.
Reporting's "four places" named.

**`permissions`** — new cast row for `Permissions` (four rungs, five atoms),
and the hook's first identifier glossed in place. The package sentence now
claims every cast row but `ChatAbilities` is one of the eleven. The union
paragraph reordered rule-before-exception. The client-side-gates paragraph
moved into *What the client is allowed to believe* as its fourth bolded
source, with the section's count changed three → four and a new claim that
`GameModeCommand.PERMISSION_CHECK` is **the one object both universes read**;
its five references are now enumerated including the command's own
registration. New closing paragraph claiming the opening operator's `/msg`
**goes through**, because no server-side node asks for
`Permissions.CHAT_SEND_COMMANDS`. The unexplained *waxed* dropped, and the
sign's exemption re-argued as "the client was never told what the text does".

**`scoreboard-and-data`** — the opening re-argued from three systems to four,
built outward from `execute store`'s three sinks. Trace heading *One command,
two models, and a number that lands in a third place*. The
failing-command-writes-0 paragraph moved from the closer into the trace
commentary (`the-execution-engine` still cites the engine's anchor, not this
one). New section *Names that belong to nobody, and the `#` that hides them*,
promoted out of the closer with the `entity-selectors` citation repointed to
it, and claiming the two `#` mechanisms are unrelated. `forAllObjectives`'
seven call sites enumerated as seven rather than as thirteen criteria
(`ServerPlayer.java`:972, 1019, 1056, 1059, 1078, 1633, 1641). The locator bar
re-argued as a sixth **consumer** and explicitly not a reader, so the
heading's *five systems read* stands. Number formats and
`Attributes.BELOW_NAME_DISTANCE` moved into *What the client is ever told*,
which gained two H3s; saving split out as *What survives a restart, and what
does not*.

**`the-execution-engine`** — the opening now names the budget in its second
sentence and claims it is what stopped the self-calling function. *Two ways to
die* → *What actually stops a command*, with two H3s. Three closer answers
promoted into it: both game rules named with their 65536 default and the
read-once claim, the depth answer (unbounded structurally, bounded by the
budget transitively), and the thread-local per-context budget. The ten-million
stub folded into the overflow paragraph and re-scoped as queue length not
depth. *No aggregation anywhere* re-worded to admit its own exception. Cast
row for `ContinuationTask` re-scoped from "N players cost N entries" to "one
queue entry at a time". Figure panel 4 now draws the `ExecuteCommand` its
caption claims. Six-class roll-call cut to four (logged in
[pass5.md](pass5.md)). Closer respelled and moved last, behind *The two
commands that are part of the engine*.

**`commands/README`** — the hook's *queue* now carries a clause saying what
one is. The nine-package roster re-argued into three groups, which changes a
claim: `net/minecraft/server/commands` is the **catalogue**, not the
machinery, and `server/bossevents` belongs to `world/scores` rather than to
the machinery. New parenthetical distinguishing an argument *type* (57) from
an argument *node* (459). Four *watch in this order* blurbs re-synced to the
pages as rewritten.

## Pass 6, session L — Part XII · World generation *(2026-09-14)*

Ten system pages and the landing page rewritten under A1–A9 and A12; eleven
readers, one per page, none with the source. The closer went **9 of 10 → 5**,
four trace headings were renamed, and all three 1.21 blockquotes moved to the
foot.

### Corrections (re-derived against the decompile by this session)

- `src/systems/worldgen/terrain.md` — the page said *"all four shipped
  configured carvers anchor it eight blocks above the world's **bottom**"*.
  **Three** do. `reference/26.2/data/minecraft/worldgen/configured_carver/`:
  *cave*, *cave_extra_underground* and *canyon* each carry
  `"lava_level": {"above_bottom": 8}`; *nether_cave* carries
  `{"above_bottom": 10}` — and that fourth value is read by nothing, because
  `NetherWorldCarver.carveBlock`
  (`net/minecraft/world/level/levelgen/carver/NetherWorldCarver.java:38-52`)
  overrides the carve path and writes lava directly at or below
  `context.getMinGenY() + 31`, so `WorldCarver.getCarveState` and the
  configuration's `lavaLevel` are never reached. The page now says *the three
  overworld configured carvers*, and says in the carving section that the
  nether one's lava level is read by nothing.
- `src/systems/worldgen/terrain.md` — the page said *"Three carvers are
  registered"* and, seventy lines later, *"all four shipped configured
  carvers"*, with nothing distinguishing the populations. Both counts are
  right: `WorldCarver.java:33-35` registers `CAVE`, `NETHER_CAVE` and `CANYON`,
  and four configured carvers ship because the cave carver is configured twice
  (*cave* and *cave_extra_underground* both declare `"type": "minecraft:cave"`;
  `data/minecraft/worldgen/biome/plains.json` lists all three of the overworld
  ones). The page now says so where the three are named.
- `src/systems/worldgen/biomes.md` — the page said `ChunkStatus.BIOMES`
  *"precedes `ChunkStatus.NOISE`, and the two do not depend on each other at
  all"*, three lines under its own figure captioning BIOMES as *"which NOISE
  and SURFACE both require"*.
  `net/minecraft/world/level/chunk/status/ChunkPyramid.java:20-23`:
  `NOISE` and `SURFACE` each `addRequirement(ChunkStatus.BIOMES, 1)`. The
  dependency is real and enforced; what is true is that the **noise fill never
  reads a biome** — what the noise step collects from the biome step is the
  chunk's `NoiseChunk` workspace. Rewritten to that.
- `src/systems/worldgen/features-and-placement.md` — the page filed
  `SurfaceRelativeThresholdFilter` with the modifiers that *"move a position
  rather than counting or filtering it"*. It is a filter:
  `net/minecraft/world/level/levelgen/placement/SurfaceRelativeThresholdFilter.java:1`
  reads `public class SurfaceRelativeThresholdFilter extends PlacementFilter`,
  making **five** `PlacementFilter` subclasses, not the four the page names.
  The fifteen are now accounted for as 5 filters + 3 repeating + 2 height +
  4 movers + 1 deprecated.
- `src/systems/worldgen/blending.md` — the cast row gave `Blender` *"the four
  answers — the height alpha and offset, the blended density, the biome
  override, and where carvers may not dig"*, which the page's own body
  contradicts sixty lines later. `Blender.java` has **three** instance
  answering methods (`blendOffsetAndFactor`:116, `blendDensity`:164,
  `getBiomeResolver`:236); `generateBorderTicks`:271 and
  `addAroundOldChunksCarvingMaskFilter`:336 are **static** and read
  `BlendingData` off the chunks directly. Cast row rewritten to three, saying
  the other two never ask an instance anything.
- `src/systems/worldgen/creating-a-world.md` — the page said
  `WorldDimensions.checkStability` *"asks, per key, whether the built-in three
  carry the vanilla dimension type, the vanilla noise settings **and** the
  vanilla biome source"*. It asks a different question of the overworld.
  `net/minecraft/world/level/levelgen/WorldDimensions.java:129-147`
  (`isStableOverworld`) tests the dimension type, then tests the parameter list
  **only if** the biome source `instanceof MultiNoiseBiomeSource`; it never
  looks at the noise settings. `isStableNether`:149-175 and its End counterpart
  do require a `NoiseBasedChunkGenerator` on the vanilla noise settings *and* a
  vanilla-parameter-list `MultiNoiseBiomeSource`.
- `src/systems/worldgen/creating-a-world.md` — following from the above, the
  page said the stability warning *"does come from a world type as well as from
  data packs"*. No preset a player can select raises it. Every preset in the
  *normal* and *extended* tags keeps the vanilla nether and end noise
  generators (`data/minecraft/worldgen/world_preset/*.json`); the only shipped
  preset that fails is *flat_all_dimensions*, which is in neither tag
  (`data/minecraft/tags/worldgen/world_preset/normal.json`, `extended.json`)
  and is reachable only through `CreateWorldScreen.testWorld`. Rewritten to say
  the warning is in practice a data-pack warning.
- `src/systems/worldgen/README.md` — the hand-counted coverage number said
  *"A quarter of the part's lines are named on no page here"*. The generated
  phrase says **19%** (`src/generated/coverage-worldgen.md`, written by
  `pass5_coverage.py --write` from the same `PARTS` mapping the size phrase
  uses). Replaced with the include; the page no longer hand-counts.
- `src/systems/worldgen/trees.md` — the opening glossed `TreeGrower`'s six
  slots as *"a normal tree and a mega tree, each with a secondary variant, plus
  two flowering variants"*, and this session first rewrote *secondary* as the
  bone-meal variant, which is wrong.
  `net/minecraft/world/level/block/grower/TreeGrower.java:57` names the six as
  `megaTree`, `secondaryMegaTree`, `tree`, `secondaryTree`, `flowers`,
  `secondaryFlowers`, and `getConfiguredFeature`:69-80 shows *secondary* is the
  probability alternative (`random.nextFloat() < this.secondaryChance`) while
  *flowers* is the near-a-flower pair. The published sentence says that.
  `TreeGrower.java:207` confirms `DARK_OAK` fills only the mega slot.

### Claims introduced, by page

- `density-functions` — **new section** *What a bound is worth, and which form
  told you*, asserting that the two rewrites move a bound in opposite
  directions (seeding widens, wrapping changes), and that
  `NoiseChunk.BlendAlpha` / `NoiseChunk.BlendOffset` are inner classes of the
  chunk distinct from the `DensityFunctions` singletons they replace
  (`NoiseChunk.java:120`, `:546`, `:483`; `DensityFunctions.java:273`).
  **New section** *What nothing reaches*, leading on the *shift*/*offset*
  naming and holding the three dead names. **New section** *The two nodes that
  read the world*, whose closing claim — that the graph is a function of the
  seed and the packs *because* its only two world-reading nodes read work that
  seed already produced — is this session's sentence and is new.
  A promoted paragraph in *Seed* asserts the memo merges structurally identical
  subgraphs because the nodes are records. A promoted paragraph asserts
  `NoiseBasedChunkGenerator.addDebugScreenInfo` is the one production path that
  samples the seeded form.
- `biomes` — heading `## The trace: a chunk's biomes` → `## Deciding a chunk's
  biomes, cell by cell` (four inbound anchors repointed; one, from
  `density-functions`, sent to `#the-search-and-the-axis-that-is-not-sampled`
  instead). New: the six climate numbers named in the cast
  (`Climate.java:159`), *quart cell* defined in the opening, the data-pack
  answer moved into *The search*, the client's hollow `Biome` and the
  per-dimension layer cost moved into *What a biome still owns*.
- `terrain` — the opening now says *four* chunk statuses where it said three.
  Two promoted passages in *Four statuses*: the beardifier as a density term
  built with the workspace, and the blender/`BelowZeroRetrogen` pair. New
  arithmetic claim: *"four by four by forty-eight cells have five by five by
  forty-nine corners between them"*. The heightmap-liveness paragraph and the
  superflat paragraph are promoted closer answers. The aquifer's four noises
  are now named individually (`NoiseRouter` barrier, floodedness, spread, lava).
- `blending` — the opening was re-entered on a thing seen rather than the word
  *You*, and now names *offset*, *factor* and *jaggedness* where it used to say
  *the three splines*; it asserts **"At the seam the overworld's terrain splines
  are not consulted"**, which is a restatement of the body's alpha-zero claim.
  *old area* is now defined as the band between the minimum and maximum
  sections (`BlendingData.java:50`, `:69-72`); *quart* is defined. A promoted
  paragraph closes *What the blender actually answers* with the two ways a
  visible edge survives. Three H3s under that H2.
- `features-and-placement` — **new section** *The order is a graph, and a graph
  can have a cycle*, which is the hook's mechanism promoted out of the closer.
  **A7 variation**: the fold flowchart now leads the page as *The chain, before
  anything else*, ahead of the cast, with a new claim that list order *is* the
  meaning. Heading renamed to *One chunk's decoration, from the corner
  outward* (three inbound repointed). The value-type ladder is re-argued as
  four rungs with six types on them. The neighbour-writes paragraph and the
  structures-share-the-step-loop paragraph are promoted closer answers.
- `trees` — the six `TreeGrower` slots re-glossed (see Corrections). New: the
  foliage *offset* defined as how far below the attachment the rows start, and
  the signed-then-folded skip test explained. The ten decorators re-grouped as
  6 + 1 + 2 + 1, a regrouping this session made. The shared-machinery paragraph
  moved from the closer into *The decorators*.
- `structure-placement` — the opening lost its second hook (*"the difference is
  a cache"*) and now lands on the arithmetic alone. **New section** *What
  `/locate` asks, and what it answers with*, holding three promoted closer
  answers; this is the target `hand-built-structures` now cites, which breaks
  the citation loop between the two closers. Four headings renamed (eight
  inbound anchors repointed, all eight on the beardifier heading). New claim:
  *"a presence question costs a centre and never a layout"*, re-scoping what
  *the layout is run once* meant. The cast row for
  `ChunkGeneratorStructureState` now splits its clock between the main thread
  and the background pool (`ChunkGeneratorStructureState.java:146-161`).
  The *terrain_adaptation* paragraph now names the desert pyramid and the
  mineshaft as the twenty-three's examples, which the old text referred to
  without ever giving.
- `jigsaw-and-templates` — heading renamed (one inbound repointed). **New
  section** *The boxes drawn round the loop*, split out of *The assembly loop*.
  New claims: the five things written on a jigsaw block, listed once in the
  cast; **two** priorities, selection and placement, both real
  (`SinglePoolElement.java:43` sorts by selection priority,
  `JigsawPlacement.java:268,380` queues by placement priority); one shared
  shrinking `VoxelShape` travelling in each `JigsawPlacement.PieceState`, with
  a fresh private shape when a jigsaw points inside its own piece's box
  (`JigsawPlacement.java:250-259`, `:396`). `getFirstFreeHeight` promoted into
  the loop. The processor sections were **reordered** so what a processor is
  precedes the section that orders them. The blockquote moved to the foot.
- `hand-built-structures` — heading `## The trace: a stronghold` → `## A
  stronghold, built twice if it has to be`. The closer dissolved whole: the
  static-state paragraph, the portal-pointer/exit-condition paragraph, the
  deprecation paragraph and a new H3 *What a Java piece keeps that a template
  cannot* (ocean monument, saved boxes, template jigsaw cleanup) are all
  promoted. New claim: `StructurePiecesBuilder` **is** the
  `StructurePieceAccessor` every piece asks
  (`structure/pieces/StructurePiecesBuilder.java:12`). Four H3s under *The
  idea*. New answer to the reload question, re-asked: the monument comes back
  *identical*, not different (`OceanMonumentStructure.java:66-85`).
- `creating-a-world` — the *world_gen_settings.dat* fact moved out of the
  blockquote into the body, the blockquote trimmed and moved to the foot.
  New: the seven presets counted out against the two tags; the
  `isStableOverworld` asymmetry (see Corrections); *The rest of the family*
  cut from thirteen lines to two classes; heading *The same object, from a
  properties file* → *The same object, built two other ways*; the stage-4
  figure label now says *a change to the enabled packs or the feature set*
  rather than *any data-pack change*.
- `worldgen/README` — **A6**: *Where the part stops* moved from after
  *Reference this part uses* to before it, and its hand-counted *a quarter*
  replaced by `{{#include ../../generated/coverage-worldgen.md}}`. The figure
  key sentence moved above the figure. *A substrate, a pipeline, and a wing*
  now says which is which, and *the substrate arrow* is re-named as *the arrow
  out of lecture one*. The `PatrolSpawner` / `PhantomSpawner` correction kept;
  the Xoroshiro correction moved into *Reference this part uses*, where it
  reads as a pointer rather than a caveat. Lecture 5's blurb gained *"and which
  a data pack can make impossible"*.

### Names

Three restored into prose after the A12 token diff —
`MangroveRootPlacement` and `ThreeLayersFeatureSize` on `trees`,
`WorldSelectionList` on `creating-a-world`. Twelve left the book deliberately
and are logged in [pass5.md](pass5.md) under this session.

## Pass 6, session K — Part XI · Rendering *(2026-09-14)*

Eleven system pages and the landing page, twelve readers, one each.

**Corrections — each re-derived against the decompile by this session.**

- `the-window`:36 — *"Every row but the first two lives in
  com/mojang/blaze3d/platform"*, while the same sentence exempts `Minecraft`
  (row 1) and `GpuBackend` (row 3). `Window` is row 2 and *is* in *platform*
  (`com/mojang/blaze3d/platform/Window.java`). Rewritten as *two of those rows
  live outside the package and the other six in it*.
- `the-window`:158 — *"the two methods run the other way round from their
  names"*. `Window.calculateScale` calculates and returns; `Window.setGuiScale`
  stores and derives. Neither is inverted. What is true and more interesting is
  that the option is a **ceiling the result may miss in both directions**: the
  loop stops below it when the framebuffer would fall under `Window.BASE_WIDTH`
  × `Window.BASE_HEIGHT` (320×240), and the unicode round-up can push the
  answer one *above* it (`Window.java`, `calculateScale`). Rewritten.
- `the-window`:101 — *"is the subject of the last section"* for the seventh
  callback, which was in the closer; the last section is *Where to look*. The
  callback is now explained where it is introduced and the forward reference is
  gone.
- `the-window`:86 — *"the server's watchdog"* read as contradicting *"none of
  it exists on the server"*. Both are true and the sentence hid why:
  `ClientShutdownWatchdog` is in *blaze3d/platform* (client-only;
  `server-classes.txt` has no *com/mojang/blaze3d* entry at all) and calls
  `ServerWatchdog.createWatchdogCrashReport`. Named exactly.
- `the-frame`:37 — *"Nine zones"* over a sentence naming sixteen. Nine is right
  for the frame's top-level zones but not for what the sentence listed, and the
  sentence also hid that **`Minecraft.renderFrame` pushes only eight of them**:
  *render* is pushed by `GameRenderer.render`, and *camera* — which the page
  never named at all — by `GameRenderer.update` (`Minecraft.java` `renderFrame`;
  `GameRenderer.java` `update`, `render`). Rebuilt as a table with a *pushed by*
  column, so no count sits in a sentence.
- `visibility-and-the-frame-graph`:64 — *"both are budgeted rather than
  complete"* of stages one and five. Stage five is budgeted; stage one is not.
  `SectionOcclusionGraph.runPartialUpdate` drains its whole propagation queue
  with no slice or quota (`SectionOcclusionGraph.java`). Rewritten as *the first
  is a cache, the fifth is a budget*.
- `lightmap-fog-and-sky`:297 — the weather said to be *"seeded from the clock"*.
  `WeatherEffectRenderer` seeds each column's `RandomSource` from a hash of its
  own *x* and *z*; `level.getGameTime()` is passed separately and only scrolls
  the streaks (`WeatherEffectRenderer.java`). This also contradicted the page's
  own opening, which had it right. Heading and sentence rewritten, and the
  consequence — two clients see the same drops in the same places with nothing
  sent between them — is now stated.
- `particles` figure — the flowchart routed unlimited particles straight to
  `ParticleGroup.add`, past the queue. `ParticleEngine.add` puts **every**
  surviving particle in `ParticleEngine.particlesToAdd`; the limit decides
  whether it is queued at all, not whether it is deferred
  (`ParticleEngine.java`). Arrow redrawn.
- `block-entity-rendering`:266 — `ShelfRenderState.items` said to reach
  `ChestSpecialRenderer`. It is an array of three `ItemStackRenderState`
  submitted through `ItemStackRenderState.submit`, so it reaches whatever
  special renderer *that item's own model* names — a chest only if the shelved
  item is one (`ShelfRenderer.java`, `ShelfRenderState.java`). Rewritten.
- `models-and-atlases`:196 — *"**twelve** separate layers"* of soft failure,
  enumerating eleven at most. Replaced with a two-column table (*what goes
  wrong* · *what you get instead*) and no numeral, which is the shape that
  cannot go stale.
- `models-and-atlases`:216 — *"Only now does the Render thread do anything"*
  against the page's own figure, which puts `AtlasManager.prepareSharedState`
  on the Render thread before any task runs. Rewritten to name that one prior
  step.
- `models-and-atlases`:84 — *"Two properties of that packing"* followed by
  three. Reworded to two properties and a setting that rides on both.
- `entity-rendering`:199 — *"exactly one layer in the game asks for a
  **negative** order"* and never named it. It is `SulfurCubeInnerLayer`
  (`SulfurCubeInnerLayer.java`, `order(-1)`). Named.
- `blaze3d`:115 — *"Vulkan leaks upward in two places, not one … The two
  exemptions are one, granted twice"*, which named three things and resolved to
  nothing. Re-derived: exactly two files outside `com/mojang/blaze3d/vulkan`
  import Vulkan bindings (`NativeLibrariesBootstrap` and `RenderPass`),
  mirroring OpenGL's two; and `BackendCreationException.Reason` has ten
  constants of which seven are Vulkan-named. Rewritten with the two facts
  separated.
- `block-entity-rendering`:339 — *"the six ways the table above records"*; the
  nearest table has six rows recording one thing, and the comparison table
  seven. Replaced with what the renderers actually differ in.
- `block-entity-rendering` — *"the two gates"* named three different pairs on
  one page (the cast row, *Two extra gates*, *Where to look*). There are
  **three** gates: the section fade in `LevelExtractor`, the off-screen flag
  equality and the distance test, the last two both in
  `BlockEntityRenderDispatcher.tryExtractRenderState`. Said once, as three.
- `entity-rendering`:101 — *"three tests in two places"* followed by a list that
  reads as three inside `EntityRenderer.shouldRender`. `Entity.shouldRender`
  *is* the distance test, and the frustum is the second
  (`EntityRenderer.java`). Repunctuated so the appositive cannot be read as a
  third item.
- `entity-rendering`:277 — *"thirteen kinds of submit"* sitting against a
  nine-name list. Both are right and they are different populations: thirteen
  `FeatureRendererType` constants, of which only `ModelFeatureRenderer.Submit`
  and `CustomFeatureRenderer.Submit` implement `BatchableSubmit`. The list is
  now said to be nine of the thirteen, with the other four named.
- `post-processing` — four target counts (seven names, one/two/six, six of the
  caller's, five internal) all correct and never reconciled. `MAIN_TARGETS` is
  1, `OUTLINE_TARGETS` 2, `SORTING_TARGETS` 6, and `LevelRenderer` creates five
  internal targets (`LevelTargetBundle.java`, `LevelRenderer.java`); one clause
  now says the six are the main target plus those five.
- Part-wide — **"client thread" and "Render thread" used for one thread**, 17
  of the corpus's 23 uses of the first being in this part, on the four pages
  where a worker/main split is the subject. `src/reference/threads.md` settles
  it: the Render thread *is* the client's JVM main thread, renamed. Normalised
  to *Render thread* throughout the part.

**Claims this session introduced.**

- `the-frame`'s zone table: the *pushed by* column for all twelve rows, the
  *camera* zone as `GameRenderer.update`'s, and the claim that *gpuAsync* is
  closed before the drawing starts.
- `the-frame`'s *What a minimized client actually stops doing*, promoted whole
  out of the closer, with its claim that the three statements that drop out are
  the acquire and the two guarded ones.
- `the-frame`'s definition of a **non-ticking frame** and its three call sites,
  moved up out of the closer into *Update and extract*.
- `the-window`'s opening paragraph declaring the page the **platform layer**,
  and its claim that the three subjects share a role rather than a scenario.
- `the-window`'s *The list is never one candidate long*, *How the loop knows why
  a window did not appear* (the `GLFWErrorScope` / `GLFWErrorCapture` pairing as
  the mechanism behind `GpuBackend.handleWindowCreationErrors`) and *The
  seventh, which is not the constructor's*, all promoted out of the closer.
- `the-window`'s *The corners the story does not pass through*: the claim that
  `TextureUtil.solidify` and `TextureUtil.fillEmptyAreasWithDarkColor` are why
  mip averaging cannot bleed a colour that was never in the texture.
- `blaze3d`'s claim that `BackendCreationException` naming seven Vulkan failures
  out of ten means the neutral façade layer knows a great deal about one of its
  two APIs; and the `GlHeuristics` sniffing and the two-deep submit fence,
  promoted out of the closer, the second under *How a frame reaches the screen*.
- `visibility-and-the-frame-graph`: the cache/budget distinction for stages one
  and five.
- `section-meshing`'s *Why "prioritise chunk updates" still costs you a frame*,
  promoted out of the closer; and the claim that `SectionCompiler` builds **two**
  `BlockQuadOutput` callbacks per compile and picks between them per block.
- `models-and-atlases`: the ten-row soft-failure table; the
  `BlockStateModel` / `BlockModel` trap moved to first use; the atlas dump named
  as `Options.keyDebugDumpDynamicTextures` → `TextureManager.dumpAllSheets`,
  plus `SharedConstants.DEBUG_DUMP_TEXTURE_ATLAS`.
- `block-entity-rendering`: the claim that 26 types are served by 24 classes
  because `ChestRenderer` takes three of them.
- `particles`: `ParticleRenderType`'s four constants named as the population
  every *four* on the page counts against.
- `post-processing`: the opening's reframing of the sixth chain as the *improved
  transparency* option, and the claim that a seventh file parses, loads and is
  never asked for.
- `rendering/README`: the claim that Part XI's coverage figure is the
  **second-highest in the book after Part V's** — written first as *the
  highest*, which the regenerated phrases disproved within the session (blocks
  48%, rendering 41%), and corrected before the commit. The argument reversed
  onto the claim **nothing you see on screen is the world; it is a copy of the
  world, and every seam a player notices is two copies disagreeing**; the figure's arrows declared to be
  reading order only, with two of them the reverse of a frame's order; the
  substrate-to-frame edge reversed; and *Where the part stops* written as a
  section with the coverage include.
- `src/lectures.md`: Part XI's paragraph re-argued as the one inversion in the
  book's order made for the viewer rather than for the dependencies.
- `src/reference/naming-drift.md`: a row for the four `Camera` accessors that
  lost their *get* prefix, which the trimmed `the-frame` blockquote released.

## Pass 6, session J — Part X · The client *(2026-09-14)*

Twelve system pages and the landing page, thirteen readers, one each. Part X
arrived with the closer on 8 of 12 in two spellings and no literal trace
heading at all, and the work turned out to be neither of those: it was
**counts**, again, and this time not only in lead-in sentences. Session I's
lesson was that a lead-in naming a number is a claim about the page; Part X
adds the wider form — **a sentence that names a number, anywhere, is a claim
about the text beside it, and nothing in the toolchain can see when the text
changes underneath it.** Eleven of the corrections below are of that shape, and
every one was found by a reader who counted because a sentence told them to.

### Corrections — every one re-derived against the decompile before the fix

1. `the-client-loop`:159 — *"Four queues and one re-entry that is not a
   queue"*, over six bullets of which five are ways off the thread. Counted
   against the section: packets, tasks, section meshing, timers and fenced GPU
   work are five, and `BlockableEventLoop.managedBlock` is the re-entry.
   Rewritten as *five ways off this thread*, and the re-entry given its own
   paragraph so it is not a sixth bullet.
2. `the-client-loop`:123–139 — *What a tick is, in order* was seventeen ordered
   steps in one semicolon chain, and its gates did not survive the sentence.
   Rebuilt as a thirteen-row table with a *what gates it* column, read off
   `Minecraft.tick` (`net/minecraft/client/Minecraft.java`). Writing the column
   found three claims the prose had implied and the source denies:
   `Minecraft.pick`, `Tutorial.onLookAt` and the GUI block are **not** gated on
   a level, and the keybind drain is gated on no screen and no overlay and on
   nothing about a level. Five of the thirteen rows are ungated, which is now
   the section's point.
3. `the-client-loop`:26 — *"There is no render thread, and there never was one
   in this version"*, three lines after saying the thread is named
   `"Render thread"`. The claim is about a *separate* thread and the sentence
   withheld the word; said now, and tied to every *Render thread* cell in the
   part's cast tables.
4. `the-client-loop`:250–252 — *"which is why every `OptionInstance.set`
   performed while loading silently skips its listener"* rested on a premise
   the page never states, that a listener fires only while `Minecraft.running`
   is true (`OptionInstance.set`, `net/minecraft/client/OptionInstance.java`).
   Premise supplied, and the citation repointed at the new section on
   `options`.
5. `the-client-loop`:237–242 — *"three different measurements"*, of which the
   third was "the graph" and was never named or placed. Said which of the three
   appears on which line of the overlay.
6. `the-client-level`:37–39 — the comparison table's lead-in said every row but
   the last is a method *one side has hollowed out*; `Level.shouldTickDeath` is
   the row where the **client** is stricter, which is the opposite. Lead-in now
   counts: seven hollowings, one the other way, and a last row that is storage
   rather than a method.
7. `the-client-level`:49 vs :277 — the table said `Level.setBlocksDirty` on the
   client is *"the renderer notification"* while the page's last section says
   `ClientLevel` never notifies `LevelRenderer`. Both true; the row now names
   `LevelExtractor`.
8. `the-client-level`:62–69 — *"two things read the server's announced
   simulation distance **off `ClientLevel`**"*, against a paragraph saying the
   value lives on `ClientPacketListener`. The level does hold its own copy,
   `ClientLevel.serverSimulationDistance`, seeded at construction and updated
   by `ClientLevel.setServerSimulationDistance`
   (`net/minecraft/client/multiplayer/ClientLevel.java`:179, 1137). Said.
9. `prediction-and-acks`:67 — *"the three destroy actions of
   `ServerboundPlayerActionPacket` but not its other five"*, with none of the
   three, the five or the two use packets named.
   `ServerboundPlayerActionPacket.Action` has eight values
   (`net/minecraft/network/protocol/game/ServerboundPlayerActionPacket.java`:70),
   so the arithmetic was right; all of them are now named, and the three
   `ackBlockChangesUpTo` call sites with them.
10. `prediction-and-acks`:162 vs :125 — `MultiPlayerGameMode.startPrediction`
    and `BlockStatePredictionHandler.startPredicting` were used
    interchangeably. They are two methods on two classes: the first is the
    window (private, six call sites), the second the pre-increment of
    `BlockStatePredictionHandler.currentSequenceNr`. Distinguished.
11. `gui-and-screens`:110 vs :113 — *"`Screen.init` is **final**"* against
    *"the overridable `Screen.init` hook"*. There are two methods of that name:
    `Screen.init(int,int)` is final at `Screen.java`:451 and `Screen.init()` is
    the hook at :496. Said, once, before either is used.
12. `gui-and-screens`:206 — *"Those **seven** names are examples"* over a table
    carrying nine backticked class names and four unbackticked ones. The number
    taught nothing, so it is gone rather than corrected — the lesson of this
    session applied to itself.
13. `gui-and-screens`:211 — *"the widget and layout families **below**"*,
    pointing down at families that are eighty lines above.
14. `gui-and-screens`:88 — *"**Two** of its behaviours"* introducing three
    claims in the same form.
15. `gui-and-screens`:231–234 — *"once **two clocks** have passed"* followed by
    three intervals. `Screen.handleDelayedNarration` tests two clocks
    (`Screen.java`:630) and three constants arm them
    (`NARRATE_DELAY_MOUSE_MOVE` 750, `NARRATE_DELAY_KEYBOARD_ACTION` 200,
    `NARRATE_SUPPRESS_AFTER_INIT_TIME` two seconds). Both numbers stated, and
    which is which.
16. `gui-and-screens`:203 — *"Three entities implement
    `HasCustomInventoryScreen` … two use the mount packet and one falls back"*,
    naming none of the three. They are `AbstractHorse`, `AbstractNautilus` and
    `AbstractChestBoat`; named, and `AbstractChestBoat` opens an ordinary menu
    through `Player.openMenu` rather than a distinct packet.
17. `the-gui-render-tree`:31 — the cast said a `GuiRenderState.Node` is *"a
    list of elements and a separate list of glyphs"*; it holds **five** lists
    (`net/minecraft/client/renderer/state/gui/GuiRenderState.java`:303–307),
    which the page's own figure already said.
18. `the-gui-render-tree`:93–98 — `GuiRenderState.addBlitToCurrentLayer` and
    `GuiRenderState.addGlyphToCurrentLayer` were listed among *"the recording
    verbs"* twenty lines after the page said the draw pass calls the glyph one.
    Neither has a caller in a recorder: the only call sites are `GuiRenderer`
    and `PictureInPictureRenderer`. The prose became a table with a *who calls
    it* column.
19. `the-gui-render-tree`:140–142 — *"The three sort comparators"*. There is
    **one**: `GuiRenderer.ELEMENT_SORT_COMPARATOR`, composed of
    `SCISSOR_COMPARATOR`, the pipeline's own sort key and `TEXTURE_COMPARATOR`
    (`GuiRenderer.java`:69–71) — which is why the figure's three sort *keys* and
    the prose's three *comparators* would not line up.
20. `the-gui-render-tree`:155 — *"three conditions gate it"* for
    `Screen.extractBlurredBackground`, which contains exactly one
    (`Screen.java`:522). The other two are facts about reaching it; separated.
21. `the-gui-render-tree`:107 — *"they are the one place 3D drawing happens
    inside a 2D pass"* of the picture-in-picture family, against the item atlas
    two paragraphs above and the 1.21 box below. Both are; said so.
22. `the-gui-render-tree`:101 — `PanoramaRenderState` was listed among the node
    states. It is a nullable **field** on `GuiRenderState`
    (`GuiRenderState.java`:28), assigned by `Panorama` and drawn by
    `GuiRenderer.render` before the tree is resolved.
23. `options`:29 — the cast said `IntegratedServer` reads the sliders *"every
    tick"*; the body says every **unpaused** server tick, and the body is right.
24. `options`:35–61 — the figure had no screen-close edge, so every route
    through it saved and broadcast immediately, which the paragraph under it
    contradicted. Redrawn against `OptionsSubScreen.onClose` and
    `OptionsSubScreen.removed`
    (`net/minecraft/client/gui/screens/options/OptionsSubScreen.java`:72–83) and
    `OptionInstance.OptionInstanceSliderButton`
    (`OptionInstance.java`:462–498): a cycle button saves on click, a slider's
    value lands on release or 600 ms later, and `Options.save` happens once,
    when the screen is removed.
25. `options`:110–111 — *"Seven of the other quality options … Nine are not"*
    with no population. Counted in `Options.java`: sixteen listeners touch the
    graphics preset, seven of them also call `operateOnLevelExtractor` (cloud
    range, cutout leaves, improved transparency, ambient occlusion, anisotropic
    filtering, texture filtering, biome blend radius) and nine do nothing else.
    Population named and the seven listed.
26. `hud`:67–68 — *"the difference between the two `Gui`-recorded elements that
    survive a level and the two that do not"*, which the page never resolved
    and which is not two and two. Read off `Gui.extractRenderState`
    (`net/minecraft/client/gui/Gui.java`:165–250): the saving indicator needs a
    level, the toasts need resources loaded, the debug overlay and the deferred
    subtitles are ungated. Four elements, three depths; now a table, with what
    each does under F1 beside it — where the debug overlay turned out to have a
    fourth behaviour the page lacked, being hidden by F1 *unless a screen is
    open* (`DebugScreenOverlay.java`:96).
27. `hud`:153–154 vs :145 — *"three health numbers"* against a figure drawing a
    four-item descending pass. Both are right and they are different lists:
    `Hud.lastHealth`, `Hud.displayHealth` and the truth are the numbers
    (`Hud.java`:169–172); container, absorption, ghost and truth are the
    layers. Said, and the ghost identified as `Hud.displayHealth`.
28. `hud`:165 — *"the HUD makes a sound of its own, which is the only element
    in it that does"*, against `Toast.Visibility` carrying a sound per state
    eighty lines above. Scoped to `Hud.extractRenderState`, with the toasts'
    sounds excluded by name.
29. `sound-engine`:46 vs :226 — the thread table said the sound thread takes
    *"every per-source AL call"* and the closer named two exceptions. Scoped to
    *while the game is running*, which is what makes the teardown exceptions
    safe.
30. `sound-engine`:84 — the figure's *"then drop a silent one"* against the
    body's *unless it is music*. Qualified in the figure.
31. `sound-engine`:245 — *"Three things"* followed by two extensions, an ALC
    version and HRTF. `Library.init` throws for exactly three
    (`com/mojang/blaze3d/audio/Library.java`:76, 113, 118) and HRTF is
    conditional, not required; separated, and *ALC_EXT_disconnect* added as the
    other optional one.
32. `what-makes-a-sound`:16 vs :44 — **the page named its three doors two
    different ways.** The opening's third door was the prediction path; the
    figure's and the table's third column was client-side ambience. Both are
    the same door — *nothing crosses the wire* — with two inhabitants. The
    opening, the figure and the table now agree, and the figure gained the
    local-prediction branch it lacked.
33. `what-makes-a-sound`:52 — the figure routed the named-packet path through a
    node labelled *"plays only when the excluded entity is the local player"*,
    which reads as a bystander hearing nothing.
    `ClientPacketListener.handleSoundEvent` passes `minecraft.player` as that
    argument (`ClientPacketListener.java`:2225), so the test always passes on
    the packet path. The inversion is now stated in the prose and the figure
    label says who supplies the argument.
34. `what-makes-a-sound`:103 — *"two kinds of silence"* followed by four named
    things, two of which make sound audible or visible rather than silent.
    Split into the two kinds and the two development constants.
35. `debugging-the-running-game`:86 — *"half the renderers below reach for the
    singleplayer server directly"*. Exactly **two** do
    (`ChunkDebugRenderer`, `EntityHitboxDebugRenderer`; grep over
    `client/renderer/debug`). Corrected to two.
36. `debugging-the-running-game`:72 vs :84 — *"Four collectors are installed
    anywhere in the game"* and then a fifth install site in the next paragraph.
    Five places install one; four of them collect. Said.
37. `debugging-the-running-game`:16 vs :260 — *"about two dozen renderers"*
    against *"eleven of the twenty-five"*. `DebugRenderer.refreshRendererList`
    adds twenty-five, eleven of them gated on a debug-screen entry; the vague
    one now says twenty-five.
38. `debugging-the-running-game`:88 — a heading reading *The sixteen instances*
    over a fourteen-row table, with the two double rows unremarked.
39. `debugging-the-running-game`:107 — *"those four expiring rows"* sorted into
    two event kinds and two pushed-value kinds without saying which is which;
    `REDSTONE_WIRE_ORIENTATIONS` was assignable only by elimination. All four
    named into their buckets.
40. `debugging-the-running-game`:229 — the heading *The sample path, which
    shares only the subscriber map* promised a shared thing the section never
    delivers. Renamed to what it does share, which is the idea and one
    subscription.
41. `debugging-the-running-game`:249 — *"Six packets carry all of this"*, where
    *this* had by then included two tag-query packets that are not among the
    six. Scoped, and the exclusion said.
42. `input-and-keybinds`:100 vs :181 — *"nineteen times over"* against *"Twenty
    debug shortcuts"*. `Options.debugKeys` holds twenty
    (`Options.java`:1263) and `KeyboardHandler.handleDebugKeys` makes
    twenty-two `KeyMapping.matches` calls, the extra two being the overlay and
    modifier keys. Both numbers corrected and the two populations separated.
43. `input-and-keybinds`:121 — the `KeyMapping.setAll` row said when it happens
    and never what it does. It asks the window which keys are physically down
    and sets each willing mapping to match (`KeyMapping.java`:60–70).
44. `README`:139 — *"ten of these twelve pages carry a *for a 1.21-era reader*
    box"*. Nine do.
45. `README`:50 — *"Everything else in the part is independent of everything
    else in the part"*, four lines above the page naming a dependency between
    two of those pages. Rewritten to say what the exceptions are.

### Claims introduced

- **The client loop.** The tick table's thirteen rows and their gate column;
  *five of the thirteen rows are gated on nothing*; the five ungated rows being
  what a client with no world still does; that `Minecraft.pick`'s tick call is
  row four and the frame's is elsewhere; that the frame-time graph is the only
  one of the three measurements fed after the limiter.
- **The client level.** *The clock and the weather run themselves, and neither
  interpolates* as a section, assembled from three dissolved closer answers;
  that the breaking sweep and `ClientLevel.animateTick` are coarse *in the same
  way*; *The four tint caches, and the soft biome edge* as a heading, with the
  claim that nothing on the server knows the edge is soft and that a chunk
  arriving is what invalidates all four.
- **Prediction and acknowledgement.** The opening re-argued so the ordering
  rule is the hook and the receipt claim leads into it (the queue asked which
  of the two openings was the hook; this is the answer); the word *cascade*
  defined at first use; *What one ack does, and the numbers that are not
  sequences* as a section, with the claim that the recorded player position is
  read by the snap and by nothing else.
- **Input and keybinds.** *The two debug-key families, and which one is
  bindable* and *Almost nothing here sends a packet* as sections; the claim
  that the twenty-two tests over twenty shortcuts are explained by the overlay
  and modifier keys being tested in the same method.
- **Options.** *The guard that silences every setting at startup* as a section
  — the queue's standing entry, acted on; the claim that a setting whose only
  effect is in its listener does nothing until you change it in the interface;
  the figure's three-way split of when a value is applied.
- **GUI and screens.** That the two `Screen.init` methods are the framework's
  style in miniature, stated before the finals list.
- **The GUI render tree.** The opening's claim that the inference buys the
  chest twice over — one layer, one atlas entry; the verb table's *who calls
  it* column; that the two current-layer verbs are why a resolved thing never
  jumps in front of what recorded it.
- **The HUD.** The figure moved above the cast, and the opening re-entered
  through the scenario (A7); the four-element gate table; the boss bar promoted
  into *The hidden flag travels two ways* with the claim that a dragon changes
  the sky because a HUD element asked the world to; *What a debug line is, and
  who turns one on* as a section.
- **Sound: the engine.** *The sound thread is not the mixer, and the device is
  not its* as a section (A7's variation for this page, and A2's promotion of
  two closer answers); the claim that the two teardown exceptions are safe
  because the thread is already joined.
- **What makes a sound happen.** The third door redefined as *nothing crosses
  the wire* with two inhabitants; the cast moved below the figure and the table
  (A7); the claim that one client method serves both the packet path and the
  local path because the handler supplies the local player as the excluded
  entity.
- **Debugging the running game.** That five places install a collector and four
  collect; that the sample path shares nothing but the idea and one
  subscription.
- **The landing page.** The argument reversed off the symptom list onto the
  claim that *everything that looks like the client falling behind is one
  thread deciding what to spend a frame on*; the figure's seven spokes
  explained against twelve pages; *Where the part stops* as a heading in A6's
  place with the generated coverage include.

### For pass 9's attention, found and not fixed

- `hud`'s *"six other places across the client"* read `Hud.isHidden` — counted
  by an earlier pass, not re-counted here.
- `gui-and-screens`'s *"Forty-one screens override
  `Screen.repositionElements`"* and *"two hundred-odd classes in
  `client/gui/screens` and its eighteen sub-packages"* — one exact and one
  round on the same page, neither re-counted.
- `the-client-loop`'s *"the overload threshold plus twenty ticks"* names no
  value, so the contrast with the client's ten cannot be felt; the value is
  `server-tick`'s to supply.

## Pass 6, session I — Part IX · Networking *(2026-09-14)*

Five system pages and the landing page, six readers, one each. Every
correction below was found by a reader with no source and no other page, and
every one was re-derived against `reference/26.2` before the fix.

### Corrections — decompile open

- `what-the-client-is-told`:415 — *"Everything in the next section is
  invisible **except** through that channel"*, of the debug feed. **False, and
  by a wide margin.** `DebugSubscriptions` registers sixteen subscriptions
  (`net/minecraft/util/debug/DebugSubscriptions.java`:16-31) — brains, goal
  selectors, entity paths, POIs, raids, structures, neighbour updates, game
  events, village sections, the three bee/breeze debuggers, redstone-wire
  orientations, entity/block intersections, game-event listeners and dedicated
  tick time. Nothing in that list exposes the world seed, loot tables, game
  rules, scheduled ticks, the ticket graph, non-syncable attributes or the
  creeper's swell counter, all of which the *never told* table lists. Now
  stated with its scope and its count.
- `what-the-client-is-told`:211 — *"The first term in that decision"*, of
  `Entity.getRequiresPrecisePosition`. The **prose was right and the figure and
  the table were both wrong**: `ServerEntity.java`:182 tests
  `!getRequiresPrecisePosition() && !deltaTooBig && teleportDelay <= 400 &&
  !wasRiding && wasOnGround == onGround()`, so precision is the first
  conjunct. The figure's edge label listed it second and the table listed it
  seventh; both are now in the source's order, and the table gained a sentence
  saying the order is the source's and why that matters.
- `what-the-client-is-told`, the gate-3 table — *"every
  `ServerEntity.FORCED_POS_UPDATE_PERIOD` calls, gated or not | a position
  packet regardless"*. The counter advances on every call
  (`ServerEntity.java`:265) but the packet is built inside the gate
  (`ServerEntity.java`:138 and :174), so a forced position packet still needs
  an open gate. Row rewritten.
- `chat-and-signing`:172 — `MinecraftServer.enforceSecureProfile` *"governs
  only the decoder used before one does"*. **False, and the page's own table
  said so six rows later**: besides selecting the pre-session decoder
  (`ServerGamePacketListenerImpl.java`:295), the flag gates
  `ServerGamePacketListenerImpl.performUnsignedChatCommand` (:1716). Row
  rewritten to name both.
- `chat-and-signing`:80 — *"Four things in that picture are worth naming"*
  over five bolded paragraphs. Counted; now five.
- `the-connection`:69 — *"Four things in that picture are worth stopping on:
  the framing, the hop, the drain, and the fact that `Connection` appears once
  but exists twice"*, over six bolded paragraphs, **the fourth of which the
  page never delivered at all**. The lead-in now names the six and states the
  two-`Connection` fact in place.
- `packets-and-stream-codecs`:56 — *"the five chat-shaped packets"*.
  `ClientboundTagQueryPacket` carries a `CompoundTag` and answers `/data get`
  (`ClientboundTagQueryPacket.java`:14); it is not chat-shaped. What the five
  share is a payload composed at run time rather than assembled from fixed
  fields. Rewritten. *(Also a self-correction: the session's first fix claimed
  all five carry a `Component`, which is true of four.)*
- `packets-and-stream-codecs`:336 — *"The frame limit does most of the work,
  and it is not on this page"*, three paragraphs above a limits table with the
  frame limit in it. Rewritten to say whose the limit is and why the table
  carries it anyway.

### Claims introduced

- `the-connection`, the opening: the swing is now cashed.
  **`ServerboundSwingPacket` carries the hand and nothing else;
  `ServerGamePacketListenerImpl.handleAnimate` calls `Player.swing(hand)`;
  `LivingEntity.swing`'s one-argument form passes `sendToSwingingEntity =
  false`, so `ClientboundAnimatePacket` reaches every tracker and not the
  swinger** (`LivingEntity.java`:2141-2155,
  `ServerGamePacketListenerImpl.java`:1913). Also the new last paragraph of
  the opening, which declares the page's second movement — a structural
  claim, not a factual one.
- `the-connection`, new section *A throw out of `Connection.tick`, and why the
  channel decides what it costs* — promoted out of the closer, same content.
  New sections *What a terminal packet does to the codecs* (renamed from
  *Getting back to unconfigured, which nobody asks for*), *The first listener,
  and who is allowed to install it* (split out of it), and *What the client
  dials is not what the player typed* (split out of *The threads underneath
  it*). The gloss on *auto-read* — "Netty's own switch for whether a channel
  keeps pulling bytes off the socket without being asked" — is new.
- `protocol-phases`, the opening: **status is the fifth phase and a login
  never enters it** — reconciling *four languages* against *five phases*,
  which the page previously left to a section a hundred lines down.
- `protocol-phases`: **configuration has no deadline, and that is
  deliberate.** `ServerConfigurationPacketListenerImpl.tick` (:195-196) calls
  the common base's `keepConnectionAlive` before the current task, so a stuck
  configuration is closed by an unanswered keep-alive rather than by a
  phase-specific timeout — unlike login's six hundred ticks. New paragraph,
  and the sentence explaining *why* ("a slow login is the client's fault, and
  a slow configuration is usually the server still finding chunks") is the
  session's reading, not the source's.
- `protocol-phases`: **protocol 754 is 1.16.4's number** and the two refusals
  are asymmetric (`ServerHandshakePacketListenerImpl.java`:65). The clause
  "the oldest that can render a modern kick screen" is an inference from the
  two branches' behaviour and should be checked.
- `protocol-phases`, the login figure: `HELLO --> VERIFYING` split into two
  edges, because the prose promises three branches and the figure drew two.
- `protocol-phases`, cast: two rows folded into one and a new row for
  `ServerCommonPacketListenerImpl` · `CommonListenerCookie`; the client row's
  thread cell now reads "the client's main thread for the last step" where it
  read "Render".
- `protocol-phases`: **`ServerboundClientInformationPacket` carries language,
  view distance and skin-part settings** (`ClientInformation.java`:8).
- `what-the-client-is-told`: **`EntityType.updateInterval` defaults to three
  and thirty types override it — one for the three `Display` entities, twenty
  for arrows, experience orbs, dropped items, falling blocks, tridents and
  spectral arrows** (`EntityType.java`:505 for the default; thirty call sites,
  15 at 10, 6 at 20, 4 at 2, 3 at 1, one each at 4 and 5). The reading — "the
  thing moving fastest is told least often, because a ballistic path is
  something the client can extrapolate exactly" — is the session's.
- `what-the-client-is-told`: **`PlayerChunkSender.MAX_UNACKNOWLEDGED_BATCHES`
  is ten** (`PlayerChunkSender.java`:33), moved into the body from the
  dissolved closer, which was the only place the page ever gave the number.
  The gloss on *dead reckoning* is new.
- `chat-and-signing`: **the first five rows of the check table run on the
  Netty thread, in that order** — three inside
  `ServerGamePacketListenerImpl.unpackAndApplyLastSeen` (the offset, the
  acknowledged-bits walk, then `verifyChecksum` at
  `LastSeenMessagesValidator.java`:74), then the character check and the
  chat-visibility refusal inside `tryHandleChat` (:1830-1833), which posts to
  the server only after both.
- `chat-and-signing`: **`MessageSignatureCache.push` has exactly two call
  sites and they are the two ends of one connection** —
  `ServerGamePacketListenerImpl.java`:1983 and
  `ClientPacketListener.java`:1082 — and it inserts the last-seen list with
  the new signature behind it, newest-first, shuffling back displaced entries
  the batch did not contain (`MessageSignatureCache.java`:38-66).
- `chat-and-signing`: **a broken chain survives death.**
  `signedMessageDecoder` is assigned in the constructor and in
  `resetPlayerChatState` only (`ServerGamePacketListenerImpl.java`:295,
  :2437); `PlayerList.respawn` reuses the listener (`PlayerList.java`:413)
  and `ServerPlayer.restoreFrom` copies the chat session
  (`ServerPlayer.java`:1729). New closer answer.
- `chat-and-signing`: **the chat throttler's ceiling is twenty per configured
  second** — `TickThrottler(20, 20 * getChatSpamThresholdSeconds())` (:286) —
  and *chat-spam-threshold-seconds* defaults to ten
  (`DedicatedServerProperties.java`:152), so 200 points; commands have an
  independent budget from *command-spam-threshold-seconds*, also ten (:151).
  "About ten messages sent faster than the decay" is arithmetic, not a source
  claim.
- `chat-and-signing`, the heading *Three ways to say no* → *Three ways to say
  no, and one way not to ask*, with a new paragraph making `ChatAbilities` the
  fourth. Two citations repointed.
- `packets-and-stream-codecs`: **`ClientboundBundleDelimiterPacket` is the one
  subclass of the abstract `BundleDelimiterPacket`** — the page named both and
  never related them. The reading of the two `JsonOps` packets ("both are read
  by a client that may not share this build's registries") is an inference the
  session drew and should be checked.
- `packets-and-stream-codecs`, two new sections out of the dissolved closer:
  *What a skippable packet actually costs* and *One type, several encodings*.
  The latter's closing clause — "the same message, written differently
  depending on whether a `RegistryAccess` exists yet to write it against" — is
  a new claim about *why* the two codecs differ.
- `networking/README`: the part's argument now ends on a claim rather than on
  the symptom list — **"the wire is not a pipe between two halves of one
  machine but a border between two machines, each of which treats what arrives
  from the other as a claim rather than a fact."**
- **Six *Where to look* lists became prose reading routes** under A12, and
  each carries claims about what a file is like to read: `Connection` "in
  three sittings", `LastSeenMessagesValidator` "sixty lines of suspicion",
  `ServerHandshakePacketListenerImpl` "sixty lines and one switch",
  `ConfigurationTask` "a three-method interface", `Packet` "four methods",
  `PacketReport` "thirty lines", `VecDeltaCodec` "forty lines". These are
  claims about file sizes and shapes and pass 9 should spot-check them. The
  token diff over the class index showed the routes releasing seven names and
  gaining six. Two of the seven were rescued back into prose —
  `ServerboundKeyPacket`, which the compression above had dropped from
  `protocol-phases`, and `ClientboundBossEventPacket`, whose "the part's
  largest single class" is a scope fact the landing page's trim had taken with
  it. The five released on purpose (`ChatListener`, `CipherBase`,
  `GamePacketTypes`, `KnownPack` and `RegistrySynchronization`, plus
  `ProtocolInfoBuilder` losing `protocol-phases`) were each in a list and in no
  sentence, and each has a home page that still carries it.

### Anchors and citations

Four headings renamed, and the link gate caught three citations on the first:
`the-connection#getting-back-to-unconfigured-which-nobody-asks-for` →
`#what-a-terminal-packet-does-to-the-codecs`, repointed from
`packets-and-stream-codecs`:62 and `protocol-phases`:10 and :225 — all three
wanted the general mechanism and none wanted the rare return path the old
heading named. `networking/README`'s citation of
`the-connection#the-threads-underneath-it` was repointed to
`#what-the-client-dials-is-not-what-the-player-typed`, which is what its
sentence actually wanted. `chat-and-signing#three-ways-to-say-no` →
`#three-ways-to-say-no-and-one-way-not-to-ask`, repointed from
`client/hud`:206 and `commands/brigadier-and-commands`:137. Two closers
dissolved whole (`what-the-client-is-told`, `packets-and-stream-codecs`) and
no link landed on either anchor.

### For pass 9's attention, found and not fixed

- `packets-and-stream-codecs`: a reader asked what happens to a packet already
  queued or already on the wire at the configuration-to-play switch — which
  chain numbers it. Not answered on the page and not re-derived; a genuine
  gap.
- `what-the-client-is-told`: the page says the client runs `Creeper.tick`
  locally "swell counter and all" and that neither the fuse nor the counter is
  ever sent. A reader asked what makes the explosion line up. Not answered.
- `the-connection`: "the nine handlers that never hop" is a count whose
  population lives on `reference/threads.md`; not re-counted this session.
- `chat-and-signing`: the cast row calls `SignedMessageValidator.KeyBased` and
  `ChatTrustLevel` "Render" thread. Two readers flagged *Render* as a term the
  page never glosses; whether it is the right thread name was not checked.

## Pass 6, session H — Part VIII · The player *(2026-09-13)*

Seven system pages and the landing page, eight readers, one each. Every
correction below was found by a reader with no source and no other page, and
re-derived by the session against `reference/26.2` before it landed. Two were
found by the session while re-deriving another, and are marked.

### Corrections — what the page said, what the decompile says

1. **`player-anatomy`** called `PlayerSkin` "a record of four textures — body,
   cape, elytra": three nouns for four textures, on the same line.
   `PlayerSkin.java:12` — the record is `(ClientAsset.Texture body,
   ClientAsset.Texture cape, ClientAsset.Texture elytra, PlayerModelType model,
   boolean secure)`. **Three** textures, and the page's own list was right. Now
   three.
2. **`player-anatomy`**'s verified line said a player is "five classes deep".
   The line addresses a reader opening *their own* inventory, so the chain is
   `Entity` → `LivingEntity` → `Avatar` → `Player` → `AbstractClientPlayer` →
   `LocalPlayer` (`Entity.java:164`, `LivingEntity.java:142`, `Avatar.java:13`,
   `Player.java:129`, `AbstractClientPlayer.java:20`, `LocalPlayer.java:109`) —
   **six** on the client, and five only on the server, where `ServerPlayer`
   (`:213`) extends `Player` directly. The line now says six on your own screen,
   and the opening states both numbers, which is the fact the ladder section
   exists for.
3. **`player-anatomy`**'s opening claimed "**the main-hand item is not stored
   anywhere**", and its own payoff eighty lines later says the held item "is not
   stored *twice*". The second is what `PlayerEquipment.java:16–22` shows:
   `EquipmentSlot.MAINHAND` resolves to `Inventory.getSelectedItem`, so the item
   is stored once, in the hotbar slot. The hook now says the main-hand item has
   no storage *of its own*, which is both true and the thing that is
   surprising.
4. **`player-anatomy`** said the `Mannequin` repeats "the same server/client
   split `Player` has, **one class lower**", two paragraphs after calling the
   mannequin a *sibling* of `Player`. `Mannequin` extends `Avatar`
   (`Mannequin.java`), so it is on `Player`'s own rung, and its split is one
   class deep (`ClientMannequin`) where `Player`'s is two
   (`AbstractClientPlayer` → `LocalPlayer` / `RemotePlayer`). Now: the split is
   repeated on its own branch, in one class instead of two.
5. **`player-anatomy`**'s closer said "**Can a data pack redefine any of this?**
   Almost none of it", then named two things that *are* set from data, then
   ended "the player is one of the few systems in the game a data pack cannot
   redefine" — flatter than the *almost* it opened with. Both halves are true
   of different things, so the paragraph now names the two data-driven pieces
   (`Player.createAttributes`; game rules and server properties setting the
   starting `GameType`) and then makes the flat claim about the rest.
   Reader-found contradiction, no code change needed to resolve it.
6. **`the-spear`** said that when any of the three `KineticWeapon.Condition`s
   passes, "the damage is the attacker's base `Attributes.ATTACK_DAMAGE` plus
   the floor of relative speed × `KineticWeapon.damageMultiplier`". That is what
   the damage *figure* is, but it is only dealt when the **damage** condition
   passed. `KineticWeapon.java` (`damageEntities`) computes `dealsDismount`,
   `dealsKnockback` and `dealsDamage` separately and calls
   `livingEntity.stabAttack(slot, target, damageDealt, dealsDamage,
   dealsKnockback, dealsDismount)` if *any* is true;
   `LivingEntity.java:3056` then reads `boolean dealtDamage = dealsDamage &&
   target.hurtServer(...)`, and `Player.java:1203` the same
   (`totalDamage = dealsDamage ? baseDamage + magicBoost : 0.0F`). Each of the
   three gates its own effect. The page now says so, with the consequence a
   player would notice: a charge can knock a target off a horse and do nothing
   to it.
7. **`the-two-phase-tick`**'s closer said "the one thing that stops phase two is
   `MinecraftServer.isPaused`", which its own phase-two section contradicts
   thirty lines earlier ("a gate that a spectator in unloaded chunks fails").
   Two different things, both real:
   `ServerGamePacketListenerImpl.java:306` short-circuits the whole bracket when
   the server is paused, and `ServerPlayer.doTick` opens with
   `if (!this.isSpectator() || !this.touchingUnloadedChunk())`, which skips
   `super.tick()`, the container check, `FoodData.tick` and the play-time
   statistics — but **not** the forty-three-slot sweep or any of the last-sent
   comparisons, which run regardless. Both are now stated, and the gate is named
   and its contents listed, which is what the page had been vague about.
8. **`the-two-phase-tick`**'s cast row for `Player` read "`Player.tick` and
   `Player.aiStep`, reached only from phase two", thread "both".
   `LocalPlayer.tick` (`LocalPlayer.java:338 region`) calls `super.tick()`, so
   on the client they are reached from the client's single tick. The row now
   says: on the server, phase two only; on the client, from `LocalPlayer.tick`.
9. **`the-two-phase-tick`** placed `Entity.rideTick` twice — as phase one's
   caller for a mounted player, and as the reason a rider is the exception to
   *the authoritative position never moves inside the bracket* — without saying
   they are the same placement. `ServerLevel.java:875–886`
   (`tickPassenger` → `entity.rideTick()`) and `Entity.java:2552–2557`
   (`rideTick` ticks, then `getVehicle().positionRider(this)`): a rider's real
   position is written in **phase one**, before the bracket opens. Said once
   now, in the bracket section.
10. **`input-to-movement`** gave `ServerGamePacketListenerImpl.MAXIMUM_FLYING_TICKS`
    (80) and `ServerGamePacketListenerImpl.CLIENT_LOADED_TIMEOUT_TIME` (60) as a
    pair of named constants, and a reader asked what the 60 was measured in.
    `ServerGamePacketListenerImpl.java:2479` decrements
    `clientLoadedTimeoutTimer` once per tick from `ServerPlayer.tick`, so it is
    **ticks**. Session-found while checking that: the constant is not read by
    anything either — `restartClientLoadTimerAfterRespawn` arms the timer with a
    bare `60` — which makes it a second instance of the page's own theme.
    Corrected and the dead constant named. *(Session-found.)*
11. **`input-to-movement`** said the mouse-look gates are "the three gates on
    it", after naming two. `MouseHandler.java:291–343`: the enclosing test is
    `minecraft.isWindowActive()`, and `turnPlayer` is reached only when no
    screen is open and the mouse is grabbed. The count was not re-derivable as
    *three* from the page's own two, and the number was doing no work, so it is
    gone rather than replaced — the sensitivity curve and its gates are [input
    and keybinds]'s, which the sentence already said.
12. **`the-sword-swing`** said `Player.cannotAttack` and `Player.deflectProjectile`
    "run before the target is asked anything at all", and then, in the next
    sentence, that `Player.cannotAttack` "puts two questions to *it*" — the
    target. `Player.java:1002–1004`: `cannotAttack` is
    `!entity.isAttackable() ? true : entity.skipAttackInteraction(this)` —
    both questions are put to the target. The page now says the first two gates
    are asked of the target rather than of the attacker, which is the real
    distinction and the one the section goes on to use.
13. **`the-sword-swing`** placed `Item.getAttackDamageBonus` "between the sprint
    check and the multiplication", in the paragraph telling the reader to read
    the flowchart above — which has no sprint check in it. `Player.java:946–953`
    confirms the placement in the code (the sprint-knockback block, then
    `baseDamage += ...getAttackDamageBonus(...)`), so the fact is right and the
    figure is what is missing it. The prose now says *before the ×1.5 rather
    than after it*, and a new paragraph names the sprint-knockback step in the
    body where the figure can be read against it.
14. **`the-sword-swing`**'s closer answered "why does my swing look different"
    by saying "the swing is not echoed to the swinger", leaving a reader unable
    to say what moves their own arm — with a `ServerboundSwingPacket` in the
    figure the body never mentioned. `LocalPlayer.java:338–341`:
    `LocalPlayer.swing` overrides `LivingEntity.swing` to call the base method
    *and* send `ServerboundSwingPacket`; `LivingEntity.java:2141–2155` then
    broadcasts `ClientboundAnimatePacket` to trackers only. A new answer says
    so, and the figure's arrow now has a sentence behind it. *(Session-found,
    from the reader's unanswered question.)*
15. **`hunger-and-experience`**'s cast row said `FoodData` is "the food bar,
    saturation and exhaustion — and by type, only on the server", which its own
    prediction paragraph contradicts ("the client replays the meal … and runs
    `FoodProperties.onConsume` and its `FoodData.eat` locally"). Both sides hold
    a `FoodData`; what is server-only by type is `FoodData.tick`, whose
    signature is `tick(ServerPlayer)` (`FoodData.java:34`). The row now says
    that, with the narrowing in the thread column where it belongs.
16. **`hunger-and-experience`**'s regen flowchart says "then at most one of the
    three" and the paragraph under it never says what makes them exclusive.
    `FoodData.java:49–73` is an `if / else if / else if` chain, so the **order**
    is the rule, and *heal fast* (`saturationLevel > 0 && isHurt &&
    foodLevel >= 20`) and *heal slowly* (`foodLevel >= 18 && isHurt`) both hold
    at twenty food. The prose now states the order and names the consequence.
    Not a wrong claim; an unstated one that no reader could supply.
17. **`status-effects`**'s opening said the client's duration "is corrected by a
    re-send every six hundred ticks", and its closer said the re-send fires
    "whenever the remaining duration divides by six hundred", then rested the
    page's own hook on the second reading (−1 divides by nothing). Both describe
    `LivingEntity.java:888` (`effect.getDuration() % 600 == 0`), but only the
    divisibility form makes the −1 argument work, and the opening was the half
    the reader met first. The opening now states the test and then says what it
    amounts to for a finite effect.
18. **`status-effects`** wrote its pulse rhythms as "*25 ≫ amplifier* ticks",
    with no reader able to tell a right shift from *much greater than*.
    `PoisonMobEffect.java:25` — `int interval = 25 >> amplification`. It is a
    right shift, and the page's own scenario is Poison II, which the page never
    connected to an amplifier of 1. Now written out: halved per level, floored
    at one tick, with 25 for Poison I and 12 for the Poison II of the scenario.
19. **`status-effects`** counted its vocabulary as three and then introduced
    `MobEffects` in the same bolded form, and then said "behind those three is a
    fourth" — leaving `MobEffects` uncounted and a reader doing arithmetic. No
    fact wrong; the counting is now off the page, with `MobEffects` named as the
    registry that *uses* the three rather than as a fourth of them.
20. **`player/README`**'s argument said a player "aliases an eighth" slot after
    saying its inventory "reports seven slots it does not store".
    `Inventory.java:39` — `EQUIPMENT_SLOT_MAPPING` has exactly seven entries
    (four armour, offhand, body, saddle), and `getContainerSize` (`:438`) is
    `items.size() + EQUIPMENT_SLOT_MAPPING.size()` = 43. The alias is
    `EquipmentSlot.MAINHAND`, which is **not** one of the forty-three at all —
    so "an eighth" describes a slot the container never reports. The clause is
    gone and the seven kept; the alias is *player anatomy*'s to explain, and the
    landing page now says so.
21. **`player/README`**'s verified line promised "the four things it does that
    the rest of the world does differently" against a figure with four branches
    and a watch order with **five** doing-pages (input to movement, the sword
    swing, the spear, hunger and experience, status effects). The figure's
    branches are four only because the spear hangs off the sword swing. Five.
22. **`player/README`**'s *Where the part stops* said "two things inside these
    packages are nobody's, and both are **declined** rather than missed", and
    then, two sentences later, "nobody explains the walk between them", which is
    a third thing and is missed rather than declined. Now three, with two
    declined and one admitted.
23. **`player/README`** hand-counted "97% of those lines are named somewhere in
    the book". `tools/pass5_coverage.py --part player` on the same mapping:
    **100%** by line, one class unnamed (`ProfilePublicKey` is named on
    `chat-and-signing`; only `ProfileKeyPair`, 19 lines, is named nowhere). The
    sentence now carries
    `{{#include ../../generated/coverage-player.md}}` and hand-counts nothing,
    which is the fifth of the five hand-counted landing-page numbers to go.

### Claims this session introduced

**New sections, each an assertion about where a mechanism belongs.**

- `player-anatomy` *Why the forty-three need two ticking calls* (H3) — claims
  `Inventory.tick` runs from `Player.aiStep` over the thirty-six and
  `EntityEquipment.tick` from `LivingEntity.aiStep` over the other seven, and
  that a third walk crosses all forty-three in phase two for
  `ServerPlayer.synchronizeSpecialItemUpdates`. Promoted out of the closer
  because `the-two-phase-tick` cites it; that link now lands here.
- `player-anatomy` *What crosses between them* (H3) — the eight packets that
  carry a player, moved out of the closer unchanged.
- `player-anatomy`'s `Avatar` paragraph now claims that "no instance fields"
  and "owns two synched values" are consistent because the `DATA_*` names are
  static `EntityDataAccessor` keys onto storage `Entity` owns. Every reader of
  the page stopped on the apparent contradiction; the resolution is a claim
  about what an accessor is.
- `the-sword-swing` *The two clocks a swing is charged against* (H2) — the
  ticker vocabulary promoted out of the closer, because `player-anatomy`'s cast
  table cites it. The link now lands here. New assertion inside it: the two
  clocks are distinguished by `Player.onAttack` clearing one and leaving the
  other.
- `input-to-movement` *Floating, and everything exempted from it* (H2) —
  promoted out of the closer because `players-and-sessions` cites it as "a list
  of exemptions the movement page owns". Claims the definition of floating is
  *no blocks anywhere below* and that the suppression list is six items.
- `input-to-movement` *What the server does with the packet it gets* (H2) plus
  six H3s — a structural split of the old trace section, not a new claim, but
  every H3 title is an assertion about what its paragraphs are about.
- `the-spear` *What a mob does with the same item* and *What a data pack can
  and cannot change here* (H2s) — the last two closer answers promoted whole.
- `hunger-and-experience` — the exhaustion economy moved to in front of the
  flowchart it explains, and the total-only change detection moved into *The
  other bar, and the number it is really watching*, which is the hook's payoff.
  New assertion in the second: every call site that changes a level without
  changing the total poisons `ServerPlayer.lastSentExp` by hand, and one that
  forgot would leave a stale client level.
- `status-effects` — three promotions into the body (the hidden-effect chain
  and the packet that cannot carry it; the blend state; the ambient-particle
  probability). New assertion in the third, derived this session from
  `LivingEntity.java:903–911`: a **visible** wholly-ambient entity rolls one in
  **twenty** (`bound` 4 × `ambientFactor` 5), which the page had left to the
  reader while working out only the invisible case.
- `hunger-and-experience`'s new first answer claims a golden carrot carries
  14.4 saturation (nutrition 6 × modifier 1.2 × 2, from
  `FoodConstants.saturationByModifier` and `Foods.java:26`) and that eating one
  on an empty bar leaves six food and six saturation, because
  `FoodData.add` clamps saturation to the **new** food level
  (`FoodData.java:22–25`). Arithmetic, re-derived; worth a second reading.

**Renamed headings (each a claim that the new title says what the section
says), with every inbound link repointed in the same commit.**

- `input-to-movement`: `## The trace: W is pressed` → *W, held down: what the
  client decides and sends*, with the server half split out. `authority` and
  `the-spear` had both been landing on the old anchor and wanted different
  halves; they now land on *What the server does with the packet it gets* and
  *Where the velocity everything downstream reads comes from*.
- `status-effects`: `## The trace: Poison II, on both sides at once` →
  *Poison II counting down on two machines*. No inbound link.
- `the-sword-swing`: `## The trace: one click, one integer, one round trip` →
  *One click, one integer, one round trip*. No inbound link.
- `the-two-phase-tick`: `## The trace: one player, one tick, twice` → *Both
  halves, in the order they run*; `players-and-sessions` repointed.
- `hunger-and-experience`: `## The other bar` → *The other bar, and the number
  it is really watching*; four inbound links repointed.
- Four links that had been landing on a closer's anchor now land on a section:
  `the-two-phase-tick` → `player-anatomy#why-the-forty-three-need-two-ticking-calls`,
  `player-anatomy` → `the-sword-swing#the-two-clocks-a-swing-is-charged-against`,
  `players-and-sessions` → `input-to-movement#floating-and-everything-exempted-from-it`,
  and `the-spear` and `the-sword-swing` → `hunger-and-experience#the-food-bar-is-four-numbers-and-a-pile-of-literals`
  for the 0.1 melee exhaustion, which the closer they had been citing never
  mentioned.

**Rewritten arguments.**

- `player/README`'s argument now ends on the claim *the player is the one
  object the server is not allowed to be right about*, with the four symptoms
  moved to the front as the way in. That claim is a summary of
  `authority`'s ruling applied to this part, and pass 9 should check it as a
  claim rather than as rhetoric.
- `player/README`'s *The shape of the part* now claims the inventory needs no
  lecture because the interesting thing about it is that seven of its
  forty-three slots are stored elsewhere — an answer to a reader who could not
  find the inventory in the figure or the watch order.
- Seven *Where to look* lists became prose reading routes under A12. No name
  left the book: checked by diffing every backticked token on each page against
  `HEAD` and then against all of `src/`, which caught eighteen on
  `player-anatomy` and four on `input-to-movement` and put them back into prose
  with a verb attached.
- Four watch-order blurbs on `player/README` re-synced to the pages as they now
  stand (1, 4, 6 and 7), each one a fresh one-sentence claim about its page.

## Pass 6, session G — Part VII · Items and inventories *(2026-09-13)*

Eight system pages and the landing page, nine readers, one each. Every
correction below was found by a reader with no source and no other page, and
re-derived by the session against `reference/26.2` before it landed. Two of the
fifteen were found by the session while re-deriving another, and are marked.

### Corrections — what the page said, what the decompile says

1. **`items-and-stacks`**' hook said durability's method "demands a
   `ServerLevel`, and the convenient overloads that do not have one silently do
   nothing at all", which claims the overloads never work. `ItemStack.java:493`
   and `:497`: the `LivingEntity` overloads test `owner.level() instanceof
   ServerLevel` and forward when it is one. They do nothing *on a client*, which
   is what the body had always said (and what makes the hook true). The hook now
   says so.
2. **`items-and-stacks`**' *Two validators* table listed
   `ItemStack.validateStrict`'s callers as `ItemInput`,
   `ItemStackTemplate.create` and `ItemStack.applyComponentsAndValidate`, while
   the prose named `ItemStackTemplate.apply` as a fourth. There are three call
   sites in the tree (`ItemInput.java:29`, `ItemStack.java:824`,
   `ItemStackTemplate.java:73`), and the third is a private `validate` that
   **both** `ItemStackTemplate.create` (`:68`) and `ItemStackTemplate.apply`
   (`:88`) go through. The cell now says that.
3. **`using-an-item`**'s bow diagram said the client's release produces "no ammo
   and **no arrow**", while the prose 20 lines later says it produces "a single
   phantom arrow marked `DataComponents.INTANGIBLE_PROJECTILE`". The prose is
   right: `ProjectileWeaponItem.useAmmo` (`:126–164`) reaches `ammoToUse == 0`
   off a client level and returns `projectile.copyWithCount(1)` with the
   component set. No *entity* is spawned, because `ProjectileWeaponItem.shoot`
   is inside a `ServerLevel` test. The label now distinguishes the stack from
   the entity.
4. **`using-an-item`** said `SpyglassItem.finishUsingItem` is "reached either at
   its 1200-tick duration or, like any use, the moment you let go". Letting go
   reaches `ItemStack.releaseUsing` → `Item.releaseUsing`, never
   `Item.finishUsingItem`. The spyglass gets its sound on release from a
   **second override**, `SpyglassItem.releaseUsing` (`SpyglassItem.java:44`),
   which the page never mentioned — the fourth and last override of
   `Item.releaseUsing` in the tree, after `BowItem`, `CrossbowItem` and
   `TridentItem`. Corrected and the second override named.
5. **`using-an-item`** said the server's release runs "five enchantment hooks"
   and named four. The fifth is `EnchantmentHelper.getPiercingCount`, asked by
   the `AbstractArrow` constructor (`AbstractArrow.java:114`) rather than by
   anything in `ProjectileWeaponItem`. Five is right; the fifth is now named.
6. **`using-an-item`** used *`EntityEvent.USE_ITEM_COMPLETE`* and *event 9* as
   two names for one thing and never equated them.
   `EntityEvent.java:13`: `USE_ITEM_COMPLETE = 9`. The opening now says so once.
7. **`using-an-item`** called `UseEffects.DEFAULT`'s value "the famous twenty
   per cent" without saying it is a multiplier. `UseEffects.java:11`:
   `DEFAULT = (false, true, 0.2F)`, and `LocalPlayer.modifyInput` (`:763`)
   *scales* the input by it — so you move at a fifth of your speed, not
   four-fifths. Stated.
8. **`enchantments`** said the third post-attack branch is "a slotless pass with
   no filter at all, reached through
   `EnchantmentHelper.doPostAttackEffectsWithItemSourceOnBreak`", and later that
   the same method "hands `EquipmentSlot.MAINHAND` to the slot filter regardless
   of where the weapon came from". Both are true of *different branches of one
   method* (`EnchantmentHelper.java:265–289`): the living-attacker branch at
   `:277` passes `MAINHAND`, the non-living branch at `:283` uses the two-arg
   overload with a null slot, and it only runs when a break callback was
   supplied. The two sentences are now one paragraph that says which is which.
9. **`enchantments`** said the effect codecs are "one of only two places in the
   game where a context mismatch is a hard error at decode time" and never named
   the other. Grepped: `Validatable.validatorForContext` /
   `listValidatorForContext` have exactly two users —
   `EnchantmentEffectComponents.java:124` and `VillagerTrade.java:52`. Named.
10. **`recipes`**' loading figure said that between `RecipeManager.apply` and
    `finalizeRecipeLoading` the four indexes "still describe the PREVIOUS recipe
    set", while the prose 20 lines below says they are **empty**. The prose is
    right: `ReloadableServerResources.java:39` builds a fresh `RecipeManager`
    per reload and its constructor (`RecipeManager.java:85–89`) sets all four to
    empty. The node now says empty, and the prose says *empty rather than
    stale*, which is the distinction the figure had inverted.
11. **`recipes`** listed the nine `CustomRecipe`s as eight class names plus "its
    fade sibling", so the count could not be checked against the list. The ninth
    is `FireworkStarFadeRecipe` (`RecipeSerializers.java:20`), now named; and
    the *named special* distinction is now stated as what it is — eight register
    under ids beginning *crafting_special_*, `DecoratedPotRecipe` does not.
    Verified: 21 serializers, 14 with `crafting_` ids, 9 extending
    `CustomRecipe`.
12. **`recipes`** said "exactly five menus extend `RecipeBookMenu`" and named
    two. The five are `CraftingMenu` and `InventoryMenu` under
    `AbstractCraftingMenu`, and `FurnaceMenu`, `BlastFurnaceMenu` and
    `SmokerMenu` under `AbstractFurnaceMenu`. All five named, with the two
    abstract halves that explain why four `RecipeBookType` values need five
    menus.
13. **`enchanting`** promised "ten integers" in its opening and accounted for
    four of them ("three `DataSlot.shared` views onto the cost array, one
    `DataSlot.standalone` holding the seed"). `EnchantmentMenu.java:95–104`:
    nine shared views over **three** arrays of three — `costs`, `enchantClue`
    and `levelClue` — plus the one standalone seed. A clue is a *pair*, which is
    why three offers cost six slots. All ten now accounted for, and the reader's
    unanswered question with them.
14. **`loot-tables`**' cast called `LootItemFunction` "forty-three
    stack-to-stack transforms" while the body says the forty-third,
    `SequenceFunction`, "is a list of functions rather than a transform".
    `LootItemFunctions.java` registers 43; 42 extend `LootItemConditionalFunction`
    and `SequenceFunction.java:13` implements `LootItemFunction` directly. The
    cast now says forty-three registered kinds, forty-two of them transforms.
15. **`items/README`** listed "the chest whose contents appear a tick late"
    among the small lies produced by predicting locally and confirming
    afterwards — and the same page says four paragraphs later that the container
    click is *not* on the prediction ledger. The tick-late chest is not a
    prediction at all: it is
    `containers-and-menus`' block-entity-phase fact, a broadcast that missed its
    phase. The argument now sorts the four symptoms into the three that are
    guesses and the one that is not, and makes the distinction the part's
    subject. *(Found by the landing page's reader; it is the error class pass 5
    hunted — one page contradicting itself across four paragraphs.)*
16. **`items/README`** said "about a third of those lines are named on no page",
    hand-counted. `pass5_coverage.py` gives **24%**. Replaced with
    `{{#include ../../generated/coverage-items.md}}`. *(Found by the session,
    not by a reader — the fourth hand-counted landing-page number in the book
    and the third to be wrong.)*
17. **`recipes`** — while restoring `RecipeInput` under A12 the session wrote
    "the seven cooking and stonecutting kinds"; there are three `RecipeInput`
    implementations in the game (`CraftingInput`, `SingleRecipeInput`,
    `SmithingRecipeInput`) and five one-slot kinds, not seven. Corrected before
    the commit. *(Found by the session: a count introduced and killed inside one
    edit, and the reason the A12 restoration is not free.)*

### Claims introduced

**New body sections, each holding material promoted out of a closer or a
figure.** Every one is a re-statement of a fact the page already carried, so
pass 9 should check the *scoping* rather than re-derive the mechanism.

- `enchantments` — four new H2s out of the dissolved *Questions the pattern
  raises*: *The three famous ones that have no effect component* (Fortune,
  Looting, Mending), *What runs on the client, and why it is only ever a number*
  (the claim that the cast row's "some read-only entry points" is exactly two
  values and three kinds of drawing), *Where the forty-three live, and when they
  are read* (the `/reload` claim, plus what crosses the wire), and *One JSON
  file, four effect objects, no Java* (`Enchantments.LUNGE` as the pattern
  entire). The closer keeps two questions.
- `loot-tables` — *What counts as reading it*, which is the hook's payoff moved
  into the body, and it carries **one genuinely new claim**: breaking an
  unopened chest commits the roll, via
  `BlockEntity.preRemoveSideEffects` (`BlockEntity.java:306–311`) walking
  `Container.getItem` over every slot into `Containers.dropContents`. Verified;
  its reader had asked exactly this and the page had never answered it. Also
  new: *A loot table that travels inside an item*, out of the closer's
  shulker-box answer.
- `containers-and-menus` — *What the client does with a correction, and what
  closing rescues*, answering its reader's unanswered question. The claim is
  that `ClientPacketListener.handleContainerSetSlot` (`:1454–1490`) writes the
  one slot and stores the state id, with no rollback path, **and** that no
  mispredicted slot is ever left standing because `broadcastChanges` compares
  every slot rather than only the claimed ones.
- `items-and-stacks` — a paragraph saying the durability bar does not creep as
  you mine but jumps at the next slot update, which follows from the page's own
  facts and answers its reader's question. And *The hundred classes, and why
  ninety-eight of them are almost empty*, split out of the tick section, with
  the population stated (100 files in `world/item`'s own directory, of which
  `Item` and `ItemStack` are two).
- `recipes` — a paragraph at the head of *What the client actually gets*
  claiming that `RecipeAccess` is a two-method interface with exactly two
  implementations (`RecipeManager`, `ClientRecipeContainer`), neither returning
  a `Recipe`. That is the page's thesis restated as an interface, and it pays
  off a cast row the body had never delivered.

**Re-argued, renamed and re-scoped.**

- `items/README`'s argument ends on a new claim (an item is the thing that is
  never simply somewhere; every page is about a container and about which
  program may believe its contents), and the seventh section moved from first to
  its A6 place under the short heading *Where the part stops*, with the borders
  paragraph moved into *The shape of the part*.
- `contexts-and-predicates` — `## The trace: /execute if predicate` renamed to
  *Four facts about a question with two keys in it*; `## None of this crosses
  the wire` renamed to *Three registries, rebuilt on `/reload`, and none of them
  networkable*, because two thirds of it was never about the wire. No inbound
  link landed on either.
- `contexts-and-predicates` — a new claim in *Three ways a parameter can be
  missing*: of the twenty registered `LootItemCondition` types, every one that
  reads a parameter uses the optional accessor **except** `EnchantmentActiveCheck`
  (`:18`), which uses the throwing one — so a predicate asking `/execute` for a
  block state is quietly false rather than fatal. Verified by grep over
  `storage/loot/predicates`.
- `loot-tables` — the opening no longer says the region file holds "a table key
  and a seed" flatly; a seed is written only when non-zero
  (`RandomizableContainer.java:72`), which the body already said.
- Eight *Where to look* lists became prose reading routes (A12). Each names
  fewer classes and asserts a **reading order**, which is a claim of a kind pass
  9 has not had to check before: that a named class is a sensible entry point.
- New H3s inside existing anchors on `using-an-item` (3), `recipes` (3) and
  `enchanting` (5). No anchor moved.

### Openings varied (A1)

Six of eight pages opened on the word *You*. Two were varied — `containers-and-menus`
to a thing seen and `contexts-and-predicates` to a fact stated flat — leaving
four, which is no longer *most*. Both rewrites restate the page's scenario and
neither changes a fact.

## Pass 6, session F — Part VI · Entities *(2026-09-13)*

Nine system pages and the landing page, ten readers, one each. Every correction
below was found by a reader with no source and no other page, and re-derived by
the session against `reference/26.2` before it landed.

### Corrections — what the page said, what the decompile says

1. **`entity-anatomy`** said `DefaultedMappedRegistry` "overrides **nine**
   lookups to hand [the default] back", and then named a tenth that does not
   (`getOptional`). `DefaultedMappedRegistry.java:20–80` has **nine overrides
   in total**, of which **six** substitute the default on a miss — `getId`,
   `getKey`, `getValue`, `getAny`, `byId`, `getRandom` — while `register` sets
   the default, `getDefaultKey` returns its key, and `getOptional` deliberately
   answers empty. The page now says nine overrides, six of which substitute.
2. **`entity-anatomy`** read as 190 against its own 191: it said "`LivingEntity`
   and its 124 descendants are two thirds of that; the non-living branches are
   the other 66", then "`LivingEntity` holds 124 of the 191", then "the other
   66". `src/generated/hierarchy-classes.md` gives `Entity` 191 descendants and
   `LivingEntity` 124, so the sum closes only if `LivingEntity` itself is the
   125th. Rewritten to say so, and the second telling of the count removed.
3. **`entity-lifecycle`** said "**seven species change** [the cluster size] —
   horses to 6, fish and wolves to 8, and ghasts, happy ghasts and pillagers
   down to 1", naming six. Seven **classes** override
   `Mob.getMaxSpawnClusterSize`: `AbstractHorse` 6, `Wolf` 8, `AbstractFish` 8,
   `AbstractSchoolingFish` (its own school size), `Ghast` 1, `HappyGhast` 1,
   `Pillager` 1. The seventh is the schooling-fish override, now named.
4. **`entity-lifecycle`**'s *Two rules decide what is in that file* was followed
   by three, the third introduced as "the clause that is easy to miss".
   `Entity.shouldBeSaved` (`Entity.java:4243`) is three clauses. Now *three
   clauses*.
5. **`entity-lifecycle`** said `Entity.setRemoved` fires
   `EntityInLevelCallback.onRemove` "with the *new* reason" one sentence after
   saying a second call cannot change the reason, which reads as a
   contradiction. `Entity.java:4219–4231`: the dismount branch tests
   `this.removalReason` (the **stored** one) and `onRemove`/`onRemoval` are
   passed the **argument**. Both are true and the page now says which is which.
6. **`damage-and-death`** said "only **four** classes" read the damage number
   and named three, while
   [`reference/non-living-damage.md`](../src/reference/non-living-damage.md)
   said five by counting `EnderDragonPart`. `EnderDragonPart.java:51` forwards
   `damage` to `EnderDragon.hurt` without using it; `MinecartTNT.java:72` reads
   the arrow's speed and then calls `VehicleEntity.hurtServer`, which is where
   the number is spent. Four, and the fourth named, on both pages.
7. **`damage-and-death`**'s cast gave `DamageType` "the hurt sound".
   `Player.java:571` — `source.type().effects().sound()` — is the **only**
   reader of it in the tree, which the body says 40 lines later. The cast row
   now says *a player's* hurt sound.
8. **`damage-and-death`**'s armour formula had two legal parses ("the armour
   points *minus the incoming damage divided by two plus a quarter of
   toughness*") and `CombatRules.ARMOR_PROTECTION_DIVIDER` was never valued, so
   the worked example's "48 per cent off" could not be derived where it was
   claimed. `CombatRules.java:20–45`: `toughness = 2 + armorToughness/4`,
   `realArmor = clamp(totalArmor − damage/toughness, totalArmor*0.2, 20)`,
   fraction `= realArmor/25`. Re-parenthesised, and 0.2, 20 and 25 given.
9. **`authority`** said "**Sixteen** pages link back to this one". Nineteen
   pages under `src/systems` contain a link to `authority.md` (three of them
   landing pages); `lectures.md`, the glossary, `SUMMARY.md` and the class index
   are excluded. Now nineteen, with the population implied by *in this book*.
10. **`authority`** said `Player.isClientAuthoritative` is "the member **three
    later pages** quote". One other page in the corpus names it,
    `player/the-two-phase-tick`. The count is gone; the member stays.
11. **`authority`** said `LivingEntity.travelRidden` "carries a **ninth
    reading** of its own", two paragraphs after an inventory whose own
    arithmetic (four + three + two, one site reading a pair) already accounts
    for nine readings at eight sites. `LivingEntity.java:2793` is a ninth
    **site** and a tenth reading. Now *a ninth site*.
12. **`ai-goals-and-brains`**'s figure said `updateActivityFromSchedule` is
    "refused if under 21 ticks old", which reads as the mob's age.
    `Brain.java:389` is `gameTime - this.lastScheduleUpdate > 20L` — ticks since
    the last **update**. Label rewritten; the prose was already right.
13. **`entities/README`** said "**Three** were written for this part" over a
    list of five. All five (`attributes`, `entity-data-serializers`,
    `spawn-reasons`, `structure-spawn-overrides`, `non-living-damage`) are cited
    from an entities page and from nowhere else first. Now five.
14. **`entities/README`** carried a hand-counted "about **40%** of those lines
    are named on no page". `pass5_coverage.py` says **34%**. Replaced with
    `{{#include ../../generated/coverage-entities.md}}`, so it cannot drift
    again.
15. **`entities/README`** said "Two of the **nine rungs** are pairs rather than
    sequels" and then described two pairs, i.e. four rungs. There are eight
    steps between nine rungs and two of the steps are pairings. Rewritten.

### Claims introduced

**`entity-anatomy`.** New: the two doors framed as *number* versus *string*
(the packet carries a registry index, the region file an id string) — a
reframing of facts the page already had, not a new fact. New sections ***The
id, and what compares equal*** and ***The two numbers frozen onto the type***,
both built from dissolved closer answers; the second is what the cast row
"the two numbers that decide how it reaches clients" had been promising.
New claim: `SummonCommand` tests the peaceful rule itself *and* does not set
`EntitySpawnRequest.ignoreChecks`, so `EntityType.canSpawn` tests it again
(`SummonCommand.java:55`, `:62`; `EntityType.java:283–292`) — both gates fire,
the command's only for the message.

**`authority`.** Restructured: the three-case table moved above the cast, the
three case sections promoted from H3 to H2 (anchors unchanged), and *Where the
gates actually sit* rewritten from seven bullets to an eight-row table whose
*which member* column is new. New claims: that the eight sites carry nine
readings because `LivingEntity.travel` reads a pair; that an entity nobody
rides and nothing steers (a dropped item, an arrow) reaches the base
implementations and is a fourth shape; that *a tracked mob* means one the
server has told your client about. The `SweetBerryBushBlock` paragraph became
its own section, ***Authority is also about which of two numbers is real***.
The unused `ServerLevel` lane was dropped from the boat sequence.

**`entity-lifecycle`.** New material: the biome crowding budget explained —
`MobSpawnSettings.MobSpawnCost` is a *charge* and an *energy budget*,
`PotentialCalculator` is the field, and **two** shipped biomes declare
`spawn_costs` (soul sand valley: ghast, skeleton, enderman; warped forest:
enderman, strider), derived from `reference/26.2/data/minecraft/worldgen/biome/`
over all 66 files. New claim: the local cap's no-nearby-player branch is
reachable because *near* means the chunk-centre 128 blocks in
`ChunkMap.playerIsCloseEnoughForSpawning` and the spawn-chunk neighbourhood in
`LocalMobCapCalculator` — two different populations. Two figure labels
rewritten to stop *persistent* meaning two things three lines apart.

**`synched-entity-data`.** Trace heading renamed to its scenario. Three H3s
inside the existing `#nineteen-slots-and-where-the-numbers-come-from` anchor.
New claim, stated in prose for the first time: there is one container **per
side**, built independently from the same class chain. The mods-and-ordinals
answer and the `Display.RENDER_STATE_IDS` paragraph moved up together as the
hook's payoff. New claim: `Entity.needsSync` is the flag `Entity.syncPosition`
sets, read by both gate tests.

**`attributes`.** Trace heading renamed (one inbound link repointed). Heading
*Five objects* → *Four objects, two dirty sets, and one list that is neither*,
with new prose naming the four and explaining
`AttributeMap.getSyncableAttributes`, which the figure drew and the prose never
mentioned (one inbound link repointed). New claim: both sides run the same
`Attributes` initialiser and build the same `DefaultAttributes` prototypes, so
the client's unsyncable value is the prototype's rather than absent. The
frozen-mob example moved out of the closer into the dirty-sets section.

**`movement-and-collision`.** New claim: the four booleans are
`Entity.horizontalCollision`, `Entity.verticalCollision`,
`Entity.verticalCollisionBelow` and `Entity.minorHorizontalCollision`, the
header having promised four and the page having named none; and
`Entity.isHorizontalCollisionMinor` is false on the base class, overridden by
`LocalPlayer` alone, which is also its only reader
(`Entity.java:1063`, `LocalPlayer.java:979`). New claim: `Entity.onGround` is
not one of the four. New claim: `Entity.collideBoundingBox` is the flat attempt
itself, called once before the step-up test (`Entity.java:1192`, `:1256`).
*Off it goes* split into two sections (one inbound link repointed). The scenario
is now stated as the landing tick.

**`ai-goals-and-brains`.** Verified line no longer promises *meet at the bell*.
New claim: the schedule's numbers are the ticks each activity **starts**, not
durations. A **1.21-era blockquote created** at the foot out of the opening's
*Schedule does not exist* clause, and it asserts: no *Schedule* class and no
*schedule* registry in 26.2; `Brain.setSchedule` takes an
`EnvironmentAttribute` (`Brain.java:284`); `Registries.TIMELINE` exists
(`Registries.java:280`); `world/entity/schedule` holds one class, `Activity`.
The unreachable-workstation answer moved into the villager's-day section with
`PoiCompetitorScan` and `ValidateNearbyPoi`. New claim: `Brain.Provider` builds
the brain and asks its `Brain.ActivitySupplier` per body.

**`pathfinding`.** Verified line's halves swapped. New claim: the *maximum path
length* is named before use — the larger of the follow range and the required
path length, in blocks — and the node budget is that times sixteen, which the
page previously called "the same" number at two different scales. New claim:
`PathNavigation.moveTo`'s position and entity overloads call
`PathNavigation.createPath` themselves (`PathNavigation.java:183–195`). The
happy-ghast sentence rescoped: it has a navigation and one goal does not use it.
*Two independent timers* re-attributed to the two halves of
`PathNavigation.doStuckDetection`.

**`damage-and-death`.** Heading *One number, a dozen owners* → *One number,
eight steps, and no step that knows another*, which is what the figure draws
(one inbound link repointed). New claim: the three entity ids in
`ClientboundDamageEventPacket` are the victim, the causing entity and the direct
one. The four `CombatTracker` reset call sites listed as four.

**`entities/README`.** Re-argued to A6. New claim: the part's argument now names
`Entity` — the base class it had never named — and ends on the claim that every
surprise on its list is one of five mechanisms answering a question another was
thought to have settled. *Where the part stops* moved from first to its template
place and cut to 21 lines. New claim in the shape section: Parts VIII, IX and X
are the three later parts that link back to *authority* (the count was there,
the parts were not). Two figure edge labels rewritten (`xxa`/`zza` was
unglossable on a landing page). *Watch in this order* blurbs re-synced for
`ai-goals-and-brains` and `pathfinding`.

### Reference

**`reference/non-living-damage.md`**'s pattern summary changed from five classes
reading the damage amount to four, to agree with `damage-and-death`; see
correction 6.

## Pass 6, session E — Part V · Blocks *(2026-09-13)*

Seven system pages and the landing page, eight readers, one each. Every
correction below was found by a reader with no source and no other page, and
re-derived by the session against `reference/26.2` before it landed.

### Corrections — what the page said, what the decompile says

1. **`blocks/README`** said "**One** thing in those ten thousand lines belongs
   to nobody… `SculkSpreader`'s charges… the one mechanism in Part V's two
   packages that no page in this book explains". There are three, and
   [pass3.md](pass3.md) §7 has carried the other two since 2026-09-07: the
   hopper (`HopperBlockEntity` 547 lines with `HopperBlock` 182) and the four
   half-adopted block-entity state machines (`BeaconBlockEntity`,
   `ConduitBlockEntity`, trialspawner, vault). The section now names all three
   and carries the generated coverage number instead of implying the gap is one
   mechanism wide. This is the sentence pass 6's planning session flagged for
   this session.
2. **`blocks/README`**'s verified line said "the four kinds of **block** that
   answer back" while the body said "the four kinds of **answer** a block can
   give" twice. The four are a neighbour update, a shape update, a block event
   and a scheduled tick — answers, not kinds of block. The verified line was
   wrong; it now says *answer*.
3. **`blocks/README`** said the tail of a write is "drawn there as the part's
   **one** flowchart". The part has four flowcharts (two on `blocks-and-states`,
   one each on `signal-and-dust` and `diodes-and-observers`) and the landing page
   itself has a fifth. Now "the part's largest flowchart".
4. **`block-breaking`**'s hook said "**neither clock is ever mentioned on the
   wire** — no progress reports, no heartbeat". The server's clock *is* on the
   wire: `ServerLevel.destroyBlockProgress`
   (`net/minecraft/server/level/ServerLevel.java`:1094) sends a
   `ClientboundBlockDestructionPacket` to every player in the level within 32
   blocks whose entity id is not the breaker's (`player.getId() != id`, squared
   distance under 1024). The page's own *The cracks belong to everyone but you*
   said so, and its closer said so plainly. Scoped: "neither clock is ever
   mentioned on **the breaker's own connection**", with the exception stated in
   the same sentence.
5. **`block-breaking`** said "three of **the four** send the true state back
   while spawn protection sends only its message", over an enumeration of
   **five** exits two paragraphs above.
   `ServerPlayerGameMode.handleBlockBreakAction`
   (`net/minecraft/server/level/ServerPlayerGameMode.java`:161-192) has five
   refusals: out of reach sends nothing at all; above the build height,
   `ServerLevel.mayInteract` and `Player.blockActionRestricted` each send a
   `ClientboundBlockUpdatePacket`; spawn protection sends only
   `ServerPlayer.sendSpawnProtectionMessage`. The count now names its population
   and all five.
6. **`block-breaking`** said the server's number "is in fact a tick *ahead* of
   the client's all the way down" in a section headed *Why the two answers
   match*, whose first sentence is that they "land on the same number". Both are
   true of different moments and the page never joined them.
   `ServerPlayerGameMode.tick` does `++this.gameTicks` before
   `incrementDestroyProgress` (`ServerPlayerGameMode.java`:112-152), so the live
   branch runs one fraction ahead and discards it; the STOP is handled in the
   packet drain, *before* that tick's increment, so
   `ticksSpentDestroying = gameTicks - destroyProgressStart` spans exactly the
   ticks the client counted and both sides reach 0.133 × 8. The section now
   states the rule, then the timing, then the discarded value — and says the
   agreement is the packet drain running before the levels, which is the part's
   own recurring fact.
7. **`block-breaking`** said `Tool.Rule.deniesDrops` and
   `Tool.Rule.overrideSpeed` "never appear in the same `Tool`, because the items
   that deny drops on a tag are exactly the ones that name their own speed on
   another" — over a table whose iron pickaxe plainly has a deny rule *and* a
   6.0 speed rule. The claim is true and the reason given is not: the pickaxe's
   second rule is `Tool.Rule.minesAndDrops`
   (`net/minecraft/world/item/ToolMaterial.java`:37), and
   `Tool.Rule.overrideSpeed` is used only by `ShearsItem`
   (`net/minecraft/world/item/ShearsItem.java`:37) and
   `ToolMaterial.applySwordProperties` (`ToolMaterial.java`:47), neither of which
   denies anything. The three rule shapes are now named, so "all three rule
   shapes" has a population, and the reason is the true one.
8. **`block-entities`** said the save shells were "one of the **five** save
   shells" while its own heading said *four ways out* over a five-row table. Four
   of the five rows are shells (`saveCustomOnly`, `saveWithoutMetadata`,
   `saveWithId`, `saveWithFullMetadata`); the fifth,
   `BlockEntity.saveAdditional`, is the subclass hook they wrap, and the table's
   own *who calls it* cell says "nobody directly". Now four.
9. **`diodes-and-observers`**' closer said two item frames make "the count two
   and **the method returns nothing** rather than choosing".
   `ComparatorBlock.getItemFrame` returns null on a count other than one, but
   `ComparatorBlock.getInputSignal`
   (`net/minecraft/world/level/block/ComparatorBlock.java`:88-111) then keeps
   `itemFrameOrBlockSignal` at `Integer.MIN_VALUE` and leaves `resultSignal` as
   the ordinary front reading from `super.getInputSignal`. It returns the
   redstone reading, not nothing. The closer is cut; the body now says what it
   falls back to.
10. **`diodes-and-observers`**' cast said the comparator decides "**one
    arithmetic operation**", and the page never said what a comparator computes
    at all — the reader's largest hole. `ComparatorBlock.MODE` holds one of two
    `ComparatorMode` values (`ComparatorMode.java`:7), and
    `ComparatorBlock.calculateOutputSignal` returns 0 when the side beats the
    front, else front minus side in `ComparatorMode.SUBTRACT` and the front
    value **unchanged** in `ComparatorMode.COMPARE` — so the comparing mode does
    no arithmetic. The cast row now says "two modes over one pair of inputs" and
    a new H3 states both, with `ComparatorBlock.shouldTurnOn`'s tie rule beside
    them.
11. **`diodes-and-observers`** said "The output half is the least-known part of
    all three blocks, and it is **shared**", against its own table's
    "`ObserverBlock.updateNeighborsInFront`, an independent copy".
    `ObserverBlock.updateNeighborsInFront` (`ObserverBlock.java`:79-86) is a
    separate method making the same two calls as
    `DiodeBlock.updateNeighborsInFront` (`DiodeBlock.java`:193-200), differing
    only in the third argument to `ExperimentalRedstoneUtils.initialOrientation`
    (null against `Direction.UP`). Now: shared by the two diodes, copied by the
    observer, which is the one place their machinery converges.
12. **`pistons-and-block-events`** said `DispenserBlock`, `DropperBlock` and
    `DoorBlock.getStateForPlacement` reach up "but **each of the three writes
    the reach out by hand**". Two do: `DispenserBlock.neighborChanged`
    (`DispenserBlock.java`:134) and `DoorBlock.getStateForPlacement`
    (`DoorBlock.java`:130) each spell out
    `hasNeighborSignal(pos) || hasNeighborSignal(pos.above())`, and those are the
    only two occurrences of that pair in the tree; `DropperBlock extends
    DispenserBlock` (`DropperBlock.java`:23) and overrides nothing. Now "three
    blocks reach up and only two write it down".
13. **`pistons-and-block-events`**' closer said the piston's reach-up is "the
    **only** place in the game anything does", 150 lines after the body named
    three other blocks that do. The closer is cut; the body's corrected count
    stands.
14. **`pistons-and-block-events`** named `PotentSulfurBlock` beside the piston
    and the note block with no gloss, and the session added one — checking it
    first, because the obvious guess was wrong. It is the geyser:
    `PotentSulfurBlock.onPlace` (`PotentSulfurBlock.java`:107) raises
    `level.blockEvent(pos, this, 0, 0)` when placed erupting or continuous, and
    `PotentSulfurBlock.triggerEvent` (:133) only stamps
    `PotentSulfurBlockEntity.eruptionTick` with the game time. The gloss says
    that.
15. **`signal-and-dust`**'s lead flowchart explained its client branch as
    "nothing at all. `Level.updateNeighborsAt` and `Level.neighborChanged` are
    empty on Level" — two true facts wrongly joined, since if those are empty the
    branch is never reached. `RedStoneWireBlock.neighborChanged`
    (`RedStoneWireBlock.java`:358-359) opens with its own
    `!level.isClientSide()`. The node now says what the method does, and the
    prose beside the figure says the branch is belt and braces.

### Claims introduced

**`blocks/README`** — re-argued to A6, and the argument is new.

- The four answers are now *named and defined* in the argument (neighbour
  update, shape update, block event, scheduled tick) and the claim is that two
  of them are the two channels a write can leave by, one server-only and one on
  both sides. Pass 5 left the landing page promising "two entirely different
  ways a block hears that its neighbour changed" and never saying which two of
  the four they were; the binding existed only inside two mermaid edge labels.
- "Half the surprises in this part are that sentence in another costume" — a new
  claim about the part, replacing an enumeration of its own pages.
- The hub figure's prose now says each arrow is labelled with *what the hub
  hands that spoke*, where it had said "what the spokes reach back into it for"
  against a figure whose arrows all point outward from the hub.
- *Where the part stops* carries
  `{{#include ../../generated/coverage-blocks.md}}` — 50%, generated, in place
  of a hand-written implication that the gap was one mechanism wide.
- *Before you start* now says **five** pages are load-bearing and gives one
  reason each; it had run four names into a ninety-word verbless sentence.
- "Part X is also where the third thing a player notices about this part lives,
  after the door and the lamp above" — the back-count is now closed.

**`blocks-and-states`**

- The verified line and the opening now announce the page's second subject: "the
  write is where a block state stops being a value and becomes an event, and the
  two channels it can leave by are not the same channel on both sides of the
  game". The claim that six lectures are applications of that one figure.
- A legend before the write figure pairing eight bit numbers with their
  constants, and decomposing placement's 11 as neighbours + clients + immediate
  (`Block.UPDATE_ALL_IMMEDIATE`). The claim is that those eight are the bits the
  figure gates on.
- New H3 **`#the-id-that-answers-air`** carrying the hook's payoff out of the
  closer: the tolerance is a property of `Block.getId` and `Block.stateById` and
  not of the id, and the wire is stricter in both directions.
- New paragraph after the chunk write, stating that the figure's two diamonds are
  not the same test: the first answers false when the state has moved, the second
  answers **true** and skips the tail. The three statements that return false are
  named.
- "Three things follow" (was two, over three).
- "The **next two** are the two update channels proper" (was "the last three"),
  with `Level.updatePOIOnBlockStateChange` named as the tail's fifth step and
  pointed at `points-of-interest`.
- The property-identity throw is now stated in *The state, a twenty-line leaf*.
- *The kind, three classes deep* now names `BlockBehaviour.Properties` as the
  third.

**`block-interaction`**

- New H3 **`#the-sound-only-you-hear`**, promoted out of the closer because
  `client/what-makes-a-sound`:147 cited it at `#questions-players-ask` (A2's
  load-bearing rule). The citation is repointed in this commit. It gains one
  claim: a lever passes a null *except* entity, so the clicker hears the
  server's packet — the mirror of the door, cited to `signal-and-dust`.
- Flags 10 decomposed as 2 + 8 with 1 absent, each named, plus the claim that
  nothing sets bit 16 and that this is what the next section is about.
- The prediction ledger belongs to `ClientLevel`, not to
  `MultiPlayerGameMode`: `ClientLevel.setBlock` hands every state it overwrites
  while predicting to a `BlockStatePredictionHandler`, so **both** halves of the
  door are recorded and both are restored together
  (`net/minecraft/client/multiplayer/ClientLevel.java`:238-251, `:195`).
- "The reach the **third** gate measures" (was "the first of them", against a
  table that makes it third).
- New H2 *The other half of the same lecture*, which was a trailing paragraph
  inside the closer; it now claims the two pages are deliberately the same shape
  and that what changes between them is the clock.

**`block-breaking`**

- The figure's loop is now "client ticks 2-8" with tick 1's add shown
  separately, because the old labels showed seven adds and then acted on 1.0
  with no eighth. The claim: `startAttack` and the first `continueAttack` are the
  same lap of `Minecraft.handleKeybinds`
  (`net/minecraft/client/Minecraft.java`:2170, :2192), and
  `MultiPlayerGameMode.startDestroyBlock` sets progress to zero, so tick 1 ends
  holding one fraction.
- "recomputes 0.133 x (elapsed + 1) **and discards it**" on the server's loop
  arrow.
- The three rule shapes named with their factories.
- `ItemStack.mineBlock`'s four conditions named on the page (a `DataComponents.TOOL`
  at all, the server side, non-zero hardness, damage-per-block above zero), where
  the page had deferred all four and its closer then explained two.

**`block-entities`**

- The four hooks are now *two pairs*, and the claim is that the disk pair's
  emptiness is an absence and the network pair's is a decision.
- "there are nineteen of those too, and it is a different nineteen" — verified:
  19 `getUpdatePacket` overriders and 19 `getUpdateTag` overriders among
  `BlockEntity` classes, differing by exactly `CopperGolemStatueBlockEntity`
  (packet only) and `PistonMovingBlockEntity` (tag only).
- *Create, keep, replace, remove* now says the two decisions happen in the
  opposite order to the heading, and why: removal must precede
  `BlockBehaviour.BlockStateBase.onPlace` and creation follows it.
- **The two hundred has a population**: `AbstractFurnaceBlockEntity.cookingTotalTime`
  is the recipe's *cookingtime*, and `SmeltingRecipe.MAP_CODEC` defaults that
  field to 200 (`net/minecraft/world/item/crafting/SmeltingRecipe.java`:12),
  which `iron_ingot_from_smelting_raw_iron.json` does not override. And the timer
  runs backwards two a tick with the fire out and either slot empty, clamped at
  zero (`AbstractFurnaceBlockEntity.java`:168-171) — the reader's unanswered
  question.
- "The tick that lights the fire moves three of them, because data 1 is the
  fuel's total burn duration; after that only 0 and 2 change" — reconciling the
  prose with the figure, which had said 0, 1 and 2 then 0 and 2.
- The furnace calls the base `preRemoveSideEffects` *first*
  (`AbstractFurnaceBlockEntity.java`:417-418), so it drops like everything else
  and then pops the experience. The page had read as though overriding meant not
  dropping.
- Three H3s inside `#loaded-is-not-enough-to-tick` (the anchor three pages cite,
  unchanged): the two gates, the list that prunes itself, three cadences.

**`signal-and-dust`**

- The forty-two is now **derived** in the opening (seven `Level.updateNeighborsAt`
  calls, six neighbours each) rather than asserted and then repeated in a
  pull-out.
- The verified line flips the lever **both ways**, because the hook and the
  staircase are about the line going dark and the traced scenario was only the
  line coming on.
- "the whole of the reach: a wire fed at 15 is at 1 fifteen blocks later and at
  0 on the sixteenth, which is a dark block rather than a shorter line" — the
  section is headed *Dust, and how far it reaches* and never stated a reach.
- `RedStoneWireBlock.shouldSignal` now closes the page's own forward reference:
  it is why no other dust can see a strongly powered block.
- *The second implementation* is re-argued on the page's own lever and two dust,
  with the two differences the hook names as its two bolded claims: nothing is
  written until the network is computed (so the near dust goes straight to zero
  rather than stepping down), and the fan-out is per connected side instead of
  seven positions. The claim that the piston east of the two dust is still told,
  and told once.
- The torch's burnout mechanism moved into the source census as the one source
  that keeps state the contract cannot see.
- The 1.21 blockquote at the foot, and it now says *why* the nullable
  `Orientation` matters: it is what lets the experimental evaluator order a
  fan-out relative to where the update came from.

**`pistons-and-block-events`**

- A four-flag-word legend before the sequence figure (324, 276, 67, 3), with the
  claim that only 67 and 3 tell a client anything.
- Three H3s inside *How a piston decides*, and the third states what
  `TRIGGER_DROP` does, which no page did: both retraction events run the same
  branch and the sticky pull is guarded on the event being
  `PistonBaseBlock.TRIGGER_CONTRACT` (`PistonBaseBlock.java`:237), so a drop
  leaves the carried block standing.
- New H3 *Who else uses the channel* over the census, and *The other way to end*
  over `finalTick`.
- `PistonHeadBlock` delivered: `PistonHeadBlock.neighborChanged`
  (`PistonHeadBlock.java`:107-110) forwards to the base behind it and
  `PistonHeadBlock.affectNeighborsAfterRemoval` (:84-90) destroys that base, so
  an arm cannot be mined off a piston and left behind.
- "the motion's first tick is the tick the piston was told about, not the one
  after, which is why a piston is not 'a tick late' so much as three ticks
  long" — promoted out of the closer.
- `MovingPistonBlock.newMovingBlockEntity` named as the static factory beside
  `MovingPistonBlock.newBlockEntity` returning null, which removes a body-against-
  reading-list name mismatch.
- Flags 3 on `finalTick` glossed as plain neighbours and clients, without the
  moved-by-piston bit.

**`diodes-and-observers`**

- The comparison table's heading is now *The observer shares one row with the
  other two* (was *Three blocks, five rows*), and the lead paragraph claims the
  grid is two comparisons: columns one against two for four rows, the third
  against either for one.
- New H3 *What it does with the two numbers*, stating both comparator modes,
  the zero-when-the-side-wins rule and `ComparatorBlock.shouldTurnOn`'s tie
  behaviour — with the consequence that a subtract comparator with equal inputs
  goes dark and a compare comparator with equal inputs stays lit at full value.
- **Both channels defined in prose** before the figure that had been their only
  definition, with the claim that the shape channel's promise is stronger because
  it arrives whether or not the neighbour meant to tell anybody.
- The item-frame fallback: the ordinary front reading, not nothing.

### Anchors moved (every citation repointed in this commit)

- `block-interaction#questions-players-ask` → `#the-sound-only-you-hear`
  (cited by `client/what-makes-a-sound`:147).
- `block-entities#one-save-hook-four-ways-out` → `#two-hundred-ticks-nobody-watches`
  on `items/containers-and-menus`:186 — **not** an anchor this session moved: the
  citation was for `BlockEntity.setChanged` and
  `Level.updateNeighbourForOutputSignal`, which the save-hook section has never
  explained and the furnace trace does. A mis-pointed citation, corrected in
  passing.
- `diodes-and-observers#three-blocks-five-rows` renamed with no inbound links
  (checked with `check_links.py --inbound`).
- **No link in the book landed on any Part V closer anchor** except the
  `what-makes-a-sound` one above, which is why three closers could dissolve
  whole.

## Pass 6, session D — Part IV · The world *(2026-09-10)*

Ten system pages and the landing page, all eleven read first by one agent each
under the pass-6 brief (a reader with the page and nothing else). Every fact
below was re-derived against `reference/26.2` — or against
`reference/26.2/data` where the claim is about a data pack — by this session
before it was written.

### Corrections — what the page said, what the decompile says

- `src/systems/world/chunk-generation-pipeline.md`:230-233 — "`ChunkPyramid.LOADING_PYRAMID`
  passes seven of the twelve steps straight through and only four do anything".
  Seven plus four is eleven. `ChunkPyramid.java`:37-60: of the twelve loading
  steps, seven call no `setTask` (*STRUCTURE_REFERENCES*, *BIOMES*, *NOISE*,
  *SURFACE*, *CARVERS*, *FEATURES*, *SPAWN*), four set one
  (`ChunkStatusTasks.loadStructureStarts`, `initializeLight`, `light`, `full`)
  and the twelfth is *EMPTY*, which `ChunkMap.applyStep` special-cases into the
  disk read. The page's own closer had it right at five; the body was the
  telling that did not close. Now stated as seven, four and the disk read, with
  the seven named. Found by a reader doing the arithmetic.
- `src/systems/world/chunk-anatomy.md`:300 — "Four of the twelve steps are
  skipped by a bit of the caller's flag word". `LevelChunk.java`:285-380 reads
  the flag word four times but in **three** steps: `flags & 256` inside step 7
  (and there it skips only `BlockEntity.preRemoveSideEffects`, not the
  removal), `flags & 1` with `flags & 64` in step 8, and `flags & 512` with
  `flags & 64` in step 10. Now three, with the partial one called out.
- `src/systems/world/lighting.md`:203 — the block flood stops "when the next
  level would be 1". `BlockLightEngine.java`:77-80: `setStoredLevel` runs
  unconditionally in that branch and only the **re-enqueue** is gated on
  `newToLevel > 1`. A level of 1 is written; it just does not propagate — which
  is what makes the page's own "thirteen blocks" (L322, L379) true from an
  emission of 14. Found by a reader who could not reconcile the two.
- `src/systems/world/lighting.md`:286-288 — `ChunkHolder.sectionLightChanged`
  described as marking the chunk unsaved, then giving up with no ticking chunk.
  `ChunkHolder.java`:151-171 has **two** gates with the bookkeeping between
  them: it returns at once if `getChunkIfPresent(ChunkStatus.INITIALIZE_LIGHT)`
  is null, *then* marks unsaved, *then* returns if `getTickingChunk()` is null.
  So a chunk still generating is not marked dirty at all. The page's own figure
  had the first gate and not the second; the prose had the second and not the
  first. Both now say both.
- `src/systems/world/lighting.md`:385-386 (in the closer, since cut) —
  "Sections above the sky column's top have no `DataLayer` at all and answer 15
  by walking upward". `SkyLightSectionStorage.java`:23-46: at or above
  `topSection` the method returns 15 from the `else` branch **without
  looking**; the upward walk is the case *below* the top with no layer. The
  page's body (L98-101) was right and the closer contradicted it.
- `src/systems/world/scheduled-ticks.md`:176-179 — "A container that is
  overtaken, or that still has something due when the budget is spent, goes
  back into the container queue". `LevelTicks.java`:158-166: a container with a
  still-due head goes back into `containersToTick` **only if
  `canScheduleMoreTicks`**; with the budget spent it takes the `else` branch
  into `updateContainerScheduling`, the index. Now three fates keyed on the
  budget as well as the head, and `rescheduleLeftoverContainers` described as
  emptying what the drain left in the queue.
- `src/systems/world/points-of-interest.md`:14-16 — the hook's "the single
  behaviour that reads the flag back can only take a claim away". **Three**
  read `BedBlock.OCCUPIED`: `SleepInBed.java`:52 (an entry condition),
  `ValidateNearbyPoi.java`:59 and `VillagerGoalPackages.java`:48 (the
  `AcquirePoi` filter). Only `ValidateNearbyPoi` turns the flag into a change
  in the record. The hook now says that.
- `src/systems/world/points-of-interest.md`:262-264 — the release rule stated
  as "this villager is not itself the sleeper". `ValidateNearbyPoi.java`:59 is
  `!body.isSleeping()` — asleep anywhere, not asleep *here*. And the exception
  is a second question asked of the world (`bedIsOccupiedByVillager`, an AABB
  search for a sleeping `Villager`), not of the block, which is why it does not
  swallow the rule: the flag and a sleeping villager can disagree. Both now
  said.
- `src/systems/world/environment-attributes-and-timelines.md`:9 — mobs stop
  burning "until dawn", against the page's own "true again at 23460" (L288) and
  "tick 0 … is dawn" (L325). `data/minecraft/timeline/day.json`:
  *gameplay/monsters_burn* is false at 12542 and true at 23460, and tick 0 is
  where the 24000-tick period closes and `ClockTimeMarkers.WAKE_UP_FROM_SLEEP`
  sits — no marker in the file is called dawn. The opening now gives the tick
  and the wrap sentence names the marker. A correction on session A's own
  exemplar, found by a reader with no source.

### Claims introduced

- **`chunk-anatomy` loses its closer entirely** (A2). All six answers were the
  page's own mechanism, and each is now a claim in the section that owns it:
  the write permit and `ThreadingDetector` as an H3 under *Sections and their
  four counters*; the client's two dead counters in the same section; the
  shared-section array under *The four shapes a chunk takes*;
  `LevelChunkSection.maybeHas` under *The palette and the ladder it climbs*
  (which is where `points-of-interest` already cited it, at an anchor whose
  prose never mentioned it); the wire form as a new H3, *The third form, and
  what the client is handed*; and `ChunkAccess.pendingBlockEntities` under
  *What step 11 leaves behind*. The cast row for `PalettedContainer` now says a
  second writer is detected rather than blocked.
- **`fluids` loses its closer entirely** (A2). `LiquidBlock.tick` and bubble
  columns moved into *The block underneath the water*; the occlusion cache
  became *Why the wall test is affordable*, an H3 beside the test it explains,
  and the glossary's *Occlusion* entry now lands there instead of on
  `#questions-players-ask`. The two remaining answers were second tellings of
  bold body sentences and are logged as cuts in [pass5.md](pass5.md).
- Six closers trimmed: `chunk-generation-pipeline` 4→3 (the world's edge, told
  twice), `chunk-storage` 5→3 (the proto-over-full guard promoted to a section
  of its own, the timestamps answer moved into *Inside a region file*),
  `lighting` 5→3, `scheduled-ticks` 5→3 (the `hasScheduledTick` /
  `willTickThisTick` distinction moved into *What one drain actually does*),
  `tickets-and-loading` 6→5 (the `PlayerMap` remembered-gate mechanism moved
  into *What a ticket asks for*), `game-events-and-vibrations` 4→3 (the
  `SculkSensorBlock.stepOn` shortcut given prose where its own figure draws it
  as two orphan nodes).
- **Two headings renamed under A4**, both literal trace headings, with three
  inbound links repointed in the same commit: `game-events-and-vibrations`
  *The trace: one footstep, several ticks* → *One footstep, and the ticks it
  takes to arrive* (glossary:669); `points-of-interest` *The trace: a villager
  claims a bed* → *Noon, and a bed forty-eight blocks away*
  (`ai-goals-and-brains`:378, `pathfinding`:109), which also stopped the
  heading being a verbatim copy of the verified line.
- **Four headings renamed under A8**, each because its own section contradicted
  or under-described it: `chunk-storage` *Three folders…* → *Four folders,
  three of them the same shape* (its own list has four and calls *data/* the
  fourth); *Why the server thread never waits, and the three times it does* →
  *Why the server thread never waits*, with the three joins as an H3
  (`structure-placement`:118 repointed); `game-events-and-vibrations` *The
  dispatcher never queues* → *The broadcast is a nested loop, and one listener
  is the exception* (`block-breaking`:257 and `block-interaction`:162
  repointed — the section's own last paragraph is
  `GameEventDispatcher.handleGameEventMessagesInQueue`), and *One tick,
  structurally* → *One slot, one tick late, and one refusal that waits*.
- **Three 1.21 blockquotes moved to the foot** (A3): `lighting` (also trimmed
  from ten lines to eight), `scheduled-ticks` (which gained a clause about
  every waterloggable block booking through `updateShape`, a fact the body
  never states), `tickets-and-loading`. Part IV now has four, all at the foot.
- **`game-events-and-vibrations`' opening re-argued under A5**: three bold
  claims became one — the tick of latency, which *One slot, one tick late* pays
  off. The wool box and the crouch are now named as gates the body reaches
  rather than promised in the hook.
- **`chunk-generation-pipeline`'s radius-11 derivation rewritten**: the rule is
  now stated as *how far out this step still demands its own immediate
  predecessor*, with *SURFACE* worked as the negative case, and the 529 is
  derived where the 11 is (a radius of 11 is a list of twelve and a square 23
  on a side). The claim is that `ChunkStep.Builder.getRadiusOfParent` walks
  `directDependenciesByRadius` from the outside in for the first ring at or
  after the parent status (`ChunkStep.java`:135-143), which gives 1 for *NOISE*,
  *FEATURES* and *LIGHT* and 0 for *SURFACE* and *SPAWN*.
- **`chunk-generation-pipeline`'s `canLoadWithoutGeneration` split into its two
  gates**: the centre against the target, then the square against
  `LOADING_PYRAMID`'s FULL accumulated dependencies, which this session
  computed to be `[SPAWN, INITIALIZE_LIGHT]` — a 3×3 in which the centre is
  checked a second time and more weakly. Its figure's last inline line no
  longer says *the steps that may write* over three of the four (*NOISE*, on
  the line above, is the fourth).
- **`chunk-storage`**: the autosave row's chain now names
  `ChunkMap.saveAllChunks`, which its holdback column already cited; the unload
  row and the figure note now agree that past 2,000 queued tasks the drain
  ignores the tick budget (`ChunkMap.java`:496-500); and the entity filter says
  why a vehicle with exactly one player rider is skipped —
  `ServerPlayer.java`:486-493 writes it into the player file under
  *RootVehicle* under exactly that condition.
- **`fluids`**: the opening's "doing nothing for the rest of the session" now
  says *never spread it a single block*, because the page's own client
  paragraph gives the client `FluidState.animateTick` and `FluidState.getFlow`;
  the basalt case states its outcome (`LiquidBlock.java`:237-241) instead of
  leaving it to be inferred from the name; the lava section's opening says two
  of the three leave a block behind, because `LavaFluid.spreadTo`
  (`LavaFluid.java`:204-215) places `Blocks.STONE` only when the target was a
  `LiquidBlock`; and the trace's packet line says *four block changes, in one
  section packet*, which is what the prose beneath it already claimed.
- **`points-of-interest`**: the four releasers are named rather than counted;
  the `CatSpawner` row says its condition follows `ServerLevel.isCloseToVillage`
  at two sections (`CatSpawner.java`:42-59); and *After the claim: the night
  shift* now separates what each behaviour does to the *record* from where it
  sends the villager, which is `ai-goals-and-brains`'.
- **The landing page** gained *Where the part stops* in the template's place
  with `{{#include ../../generated/coverage-world.md}}`, which is where the
  world border's absence is now explained — giving the *Reference this part
  uses* sentence's "for the reason just given" an antecedent it had lost. Its
  verified line and argument no longer promise a lecture on *sending* (the
  packet is Part IX's; this part stops at eligibility); the shape paragraph now
  says which box in its figure is not a page; the watch order no longer says
  the last four are free of each other, because `fluids` assumes
  `scheduled-ticks` and `lectures.md` already said so; and the tenth blurb no
  longer names a flag the reader has not met.
- **Eight *Where to look* lists rewritten to A12**, each in the page's own
  reading order with a phrase saying what each run is for: 21→13
  (`chunk-anatomy`), 24→13 (`chunk-generation-pipeline`), 26→17 (`lighting`),
  27→16 (`scheduled-ticks`), 23→13 (`tickets-and-loading`), 18→13 (`fluids`),
  17→12 (`points-of-interest`), 23→16 (`game-events-and-vibrations`). No name
  left the book; `scheduled-ticks` dropped three that appear nowhere on the
  page and belong to the random-tick tangent rather than to its own trace.
- **Six H3s added inside existing H2 anchors** to clear the forty-line budget
  without moving an anchor: two on `lighting`, two on
  `chunk-generation-pipeline`, one on `fluids`, one on `chunk-storage`. Part IV
  went from ten long sections to none.
- **`tools/pass6_shape.py` fixed**: `QLEAD` and `QMARK` used `[^*]`, so a bold
  lead-in containing italics — `**Why is my *entities/* folder…?**` — counted
  as neither a lead-in nor a question. Now non-greedy, with a probe case. Every
  closer count this pass has published was measured with the old regex and may
  be low by one wherever a question names a file or a field in italics.

## Pass 6, session C — Part III · The server *(2026-09-10)*

Five system pages and the landing page, all six read first by one agent each
under the pass-6 brief (a reader with the page and nothing else). Every fact
below was re-derived against `reference/26.2`, or against
`tools/map_source.py`'s `PARTS` mapping where the claim is about the atlas,
by this session before it was written.

### Corrections — what the page said, what the decompile says

- `src/systems/server/README.md`:24-26 — "`MinecraftServer` is not among
  them — it sits a package up, in `net/minecraft/server`, which is why the
  atlas counts it under Part I". It **is** among them. Part III's spec in
  `tools/map_source.py`:90-92 is `net/minecraft/server/.` (the package
  itself-only), `server/level`, `server/players` and `server/dedicated`, and
  the itself-only entry holds `MinecraftServer.java` — re-derived by running
  `map_source.part_files` over that spec: 95 files, `MinecraftServer.java`
  among them at 2,633 lines, the largest single file in the part. Part I
  counts it as well, because the atlas's parts deliberately overlap (Part IV
  also claims `server/level`; Part VIII claims `ServerPlayer.java`). The page
  now names the four packages, says `MinecraftServer` is the largest of the
  ninety-five, and says plainly that a class can belong to two parts. Found
  by a reader who could not tell which lecture owns the class the part's
  central claim is about.
- `src/systems/server/README.md`:3 — the verified line promised "from the
  command line that starts it to the exception that ends it", while the
  page's own watch order (item 5) compares **three** endings and the first,
  `/stop`, is not an exception. Now "to the three different ways it stops".
- `src/systems/server/server-level-tick.md`:145 — the heading *Sleeping is
  the one thing a freeze cannot stop* against the page's own figure, which
  marks nine of its twenty steps *no gate*. Re-derived at
  `ServerLevel.java`:345-363: the sleep block and `updateSkyBrightness()` sit
  outside `if (runs)` and `tickTime()` sits inside it, so the section's two
  paragraphs are a contrast rather than a superlative. The heading is *A
  freeze stops the clock and not the sleep check*, which is what they say.
  Three inbound links repointed in the same commit.
- `src/systems/server/server-level-tick.md`:408 — the heading *The two steps
  that always run*, over the same figure's nine ungated nodes. It means the
  last two; it says so now — *After the entities: the manager's drain and the
  debug feed*. No inbound links.
- `src/systems/server/players-and-sessions.md`:47 —
  "`PlayerList.canPlayerLogin` returns the reason to refuse, or null", under a
  heading promising a `Component` the prose never delivered.
  `PlayerList.java`:348 declares
  `@Nullable Component canPlayerLogin(SocketAddress, NameAndId)`. The type is
  in the sentence now.
- `src/systems/server/players-and-sessions.md`:52 — "the `ServerOpList` the
  **next paragraph** turns on". The op list is turned on in the same
  paragraph, seven lines further down; the next paragraph is about the second
  run of the gate. Now "that both surprises below turn on".

### Claims introduced

- `server-tick`, the opening — the hook's second half now says *why* a server
  that has complained recently keeps running behind: "that branch will not
  fire again for a further ten seconds and a hundred ticks of the server's own
  scheduled time". The two constants are the page's own at :69-73
  (`OVERLOADED_WARNING_INTERVAL_NANOS` plus
  `OVERLOADED_TICKS_WARNING_INTERVAL` ticks' worth); the claim promoted into
  the opening is that the *since-last-warning* gate, not the backlog gate, is
  what keeps a warned server behind. A reader with no source could not follow
  the hook without it.
- `server-tick`, *The deadline moves before the work starts* — "the other arm
  of the loop's opening *if*, the one the overload check sits inside". Asserts
  that the sprint is the *then* arm and the overload check lives in the
  *else*: `MinecraftServer.java`:795-810.
- `server-tick`, after the `tickChildren` table — **moved up from the
  closer**, the definition of *frozen* (`TickRateManager.runsNormally` false;
  `/tick freeze` sets `isFrozen`; `TickRateManager.tick` derives
  `runGameElements` unless `/tick step` left `frozenTicksToRun` above zero).
  New claim in the move: "**Three** rows say *frozen*" — the functions row,
  the clocks row and the debug/game-tests row of that table.
- `server-tick`, *The bookkeeping at the bottom* — **moved up from the
  closer**, the whole autosave arithmetic, beside the
  `MinecraftServer.ticksUntilAutosave` countdown it is about. Nothing in it is
  new; the claim the move asserts is that the countdown and its arithmetic are
  one subject.
- `server-tick`, *An empty server stops ticking* — **moved from inside the
  closer** (where it was a paragraph that was not a question), the
  `IntegratedServer`/`DedicatedServer` override paragraph, with one new
  sentence joining it to the integrated pause above it: "That pause is the
  pattern for every difference between the two servers on this page."
- `server-level-tick`, *Three ranges, before we need them* — new: the number
  line "counts *outwards*: a low level is a chunk somebody is standing in and
  a high one is a chunk at the edge of what the server bothers with, up to
  `ChunkLevel.MAX_LEVEL`". `ChunkLevel.java`:11-16. The page had never said
  which direction the number runs and a reader inferred it from a later
  sentence.
- `server-level-tick`, *The chunk source does five things in one call* — the
  running paragraph is a five-item numbered list, each item naming its gate.
  Two claims are sharper than the prose was: item 3 says the third thing is
  "one call holding two halves, both skipped in a debug world"
  (`ServerChunkCache.tickChunks` wraps the spawning work *and*
  `broadcastChangedChunks` in a not-debug test), and item 4 says
  `ChunkMap.tick` is ungated (`ServerChunkCache.java`:333-337 puts it inside
  `if (tickChunks)` and outside the debug test).
- `server-level-tick`, *What the tick does before anything can move* — a new
  H2 over two H3s, the first keeping the old anchor. The claim the grouping
  asserts: the environment-cache drop, the border and the weather cycle are
  the tick's work on the level's own environment, before anything in it moves.
  Second H3 heading, new: *The weather is the server's; only the fade is the
  level's*.
- `server-level-tick`, the foot — a **1.21-era blockquote made out of a closer
  answer** ("Where did the day–night cycle go?"), which was written for a
  reader who remembers the level owning the time. Claim added in the move: the
  weather countdowns went the same way, into one `WeatherData` on the
  `MinecraftServer` — which is the page's own :136-138.
- `players-and-sessions`, *What comes across when you die* — **moved from the
  section opening**, the end-credits concession, with a new framing claim:
  the end credits are "not a way a session changes so much as the one place
  two of them meet", since `ServerPlayer.showEndCredits` removes with
  `CHANGED_DIMENSION` like a dimension change and then hands to
  `PlayerList.respawn` like a death. That is the page's own :349-352 read the
  other way round.
- `players-and-sessions` — *The three kicks that come from the tick* promoted
  from `###` to `##`, out from under *Four ways the session changes*. Implied
  claim: the three kicks are not one of the four ways. The anchor is unchanged
  and its three inbound links still land.
- `players-and-sessions` — four new H3s (*Four questions, and the two ways
  past them*, *The gate runs twice, and disagrees with itself*, *Between the
  two reads, the player is built*, *Two rescues wired into the read*) under
  two existing H2s whose anchors are unchanged. Each names what was already
  under it; the second asserts that the two runs of the gate disagree, which
  is the paragraph's own duplicate-login contrast.
- `starting-a-server`, the opening — "Every other item on that list was over
  before the first one printed … It is not a claim about the whole boot:
  query, RCON, the watchdog and JMX are all started *after* that line". The
  page's own *Done comes before the loop* is the source; the claim is the
  scoping. The same paragraph now cites `tickets-and-loading` at the hook's
  *nine ticket types*, its first use, 285 lines before the payoff.
- `starting-a-server`, *The Server thread wakes up, and can still fail twice*
  — new: "a false there is not a quiet exit: `MinecraftServer.runServer` calls
  it inside its own *try* and throws an *IllegalStateException* on false".
  `MinecraftServer.java`:783-787. The page had `runServer` throwing into its
  own catch with the bridge missing, which read as nonsense to a reader with
  no source.
- `how-a-server-dies` — **the comparison table moved above the cast** (A7's
  structural variation for the later page of a twin pair). No claim in the
  move; the first cell of the table lost the six-caller list it duplicated
  from *The command is a flag* below, and now says "called with *wait* false
  by `StopCommand` and by five other callers below".
- `how-a-server-dies` — *Three booleans and a question* **dissolved**. Claims
  it carried and where they are now: `MinecraftServer.running` is volatile and
  the loop's only condition (into *The command is a flag*, where the flag is
  set); `MinecraftServer.stopped` is a plain field other threads read through
  `isStopped` (into the teardown paragraph that sets it); the
  `isShutdown`-versus-`isStopped` contrast (into *Singleplayer ends on a
  poll*, which is the only thing on the page that turns on it, with a new
  clause: a screen driven by `isStopped` "would come down before the world was
  written"). `MinecraftServer.isReady` was cut — `starting-a-server`'s *Done
  comes before the loop* owns it and says the same thing.
- `how-a-server-dies` — *The endings that are `/stop` under another name*, a
  renamed H2 over two new H3s. The renaming asserts that Ctrl-C, SIGTERM, the
  GUI button and singleplayer *Save and Quit* all clear
  `MinecraftServer.running` and reach the same *finally*, which is what the
  section already said of each separately.
- `how-a-server-dies` — three new H3s under *What you lose if you kill the
  process*, the third of which (*What you lose with no ending at all*) asserts
  that the quiet per-chunk save failure belongs to the same subject.
- `server/README`, *Where the part stops* — rewritten to A6 and now carrying
  `{{#include ../../generated/coverage-server.md}}`. Two claims: that 2% is
  "after Parts I and VIII … as close to complete as the book gets" (checked
  against all thirteen `src/generated/coverage-*.md`: anatomy 0%, player 0%,
  server 2%, world 3%), and that what the part leaves out it leaves to a named
  other part rather than to nothing. The nine-class inventory the reader
  skipped is gone, replaced by the families.
- `server/README`, *The shape of the part* — new: "The figure is the shape of
  the part and not the order to watch it in", because the figure runs
  Start → Tick → Level → Players → Death and the watch order puts *Starting a
  server* fourth, and nothing said so. The "seven later parts" count now names
  its population (IV, V, VI, VII, VIII, IX, XIII) and matches
  `lectures.md`:449's "seven of the eight later parts that run on the Server
  thread".
- `server/README`, *Watch in this order* — two blurbs re-synced: item 3 no
  longer says "the configuration phase" (a term Part III's reader has not met
  at that point) and item 5 says what the watchdog is.

### Cuts, and what released them

Four *Where to look* lists cut under A12, from 26, 33, 33 and 24 names to 17,
19, 19 and 15, each now in the page's own reading order and introduced by the
order it is in. Every name removed is still in the page's prose, so nothing
left the book: `server-tick` released `MinecraftServer.shouldRun`,
`MinecraftServer.pollTask`, `TickTask`, `ReentrantBlockableEventLoop`,
`TickCommand`, `ChunkMap.processUnloads`, `ServerClockManager`, `SampleLogger`
and `TpsDebugDimensions`; `server-level-tick` fourteen leaf members of classes
the list still names; `starting-a-server` thirteen, of which `ServerWatchdog`
was the one name that appeared nowhere else on the page and is
`how-a-server-dies`'; `how-a-server-dies` nine.

## Pass 6, session B — Parts I · Anatomy and II · Foundations *(2026-09-10)*

Nine system pages and two landing pages, all eleven read first by one agent
each under the pass-6 brief (a reader with the page and nothing else). Every
fact below was re-derived against `reference/26.2` by this session before it
was written.

### Corrections — what the page said, what the decompile says

- `src/systems/anatomy/anatomy.md`:15-21 — the opening said pause is decided
  by `Minecraft.isPaused` and enforced by `IntegratedServer.tickServer`,
  "which is why a world published to LAN never pauses". Nothing on the page
  joined the two: on its own account the options menu should still pause a
  published world. `Minecraft.java`:1323 sets
  `pause = hasSingleplayerServer() && gui.isPausing() &&
  !singleplayerServer.isPublished()`, so publishing is a term in the
  *client's* decision rather than something the server overrides. The page
  now says so. (`IntegratedServer.java`:136 is the enforcement half:
  `paused = Minecraft.getInstance().isPaused() || players.isEmpty()`.)
- `src/systems/foundations/identifiers-and-registries.md`:86-92 — "It holds
  the same entries in **four** indexes at once and every lookup direction is
  one of them", followed by five named maps. `MappedRegistry.java`:36-40
  declares five: `byId`, `toId`, `byLocation`, `byKey`, `byValue`. Corrected
  to five, with `toId`'s −1 behaviour folded in from the closer.
- `src/systems/foundations/tags.md`:154 — the trace's last arrow was
  `Parrot->>MR` (the `MappedRegistry` lane) for the membership test, and the
  paragraph explaining that same chain ends "No registry is consulted."
  `Holder.Reference.is(TagKey)` reads the reference's own `Set<TagKey<T>>`
  field, bound by `Holder.Reference.bindTags` (`Holder.java`, the `Reference`
  class); no registry call. The arrow is now a self-message on the `Parrot`
  lane saying so. This is a figure disagreeing with its own prose, not a
  wrong fact in the prose.
- `src/systems/foundations/tags.md`:35 — the cast gave `MappedRegistry` the
  thread "Server; Render on the client", while the page's own apply paragraph
  says that at world load the Server thread does not exist yet and the apply
  runs on the launching thread or the Render thread. The cell now says "read
  from any; written only by whichever thread is applying".
- `src/systems/foundations/codecs-nbt-json.md`:99 — "Nothing on this path is
  a `Codec`", in a paragraph whose second half has the serverbound half
  re-encoding through `ItemStack.CODEC` into `NullOps`. Scoped to "nothing on
  the clientbound half of this path".
- `src/systems/anatomy/what-this-book-skips.md` — "`com/mojang/blaze3d/audio`
  is **the one** package in this tour that is hatched for its *address*
  rather than for being unread", ten paragraphs after `net/minecraft/gizmos`
  is described in the same terms. Rewritten to name the pair.
- `src/systems/anatomy/what-this-book-skips.md` — "Four profilers, two of
  them in this package" against four subsections all of which live under
  `util/profiling`. The split is package-level: `ActiveProfiler` and
  `TracyZoneFiller` sit in `util/profiling` itself, *jfr* and *metrics* are
  subpackages of it (`reference/26.2/net/minecraft/util/profiling/`). Said
  plainly now, and the heading names what the section says.
- `src/systems/foundations/resource-system.md`:47 — "Five stages" over a
  figure drawing six nodes. The sixth is the rollback branch off *apply*; the
  sentence now says so.
- `src/systems/foundations/data-driven-types.md`:296-298 — "most of the ones
  that are **not** [registries of kinds] fall into three groups", where the
  third group is headed *A registry of kinds with nothing to load*. The lead
  now separates the three groups from the fourth case.

### Claims introduced

- `anatomy` — **new section** *A crash in singleplayer surfaces on the wrong
  half*, promoted out of the closer under A2. Claim: only a loop constructed
  to propagate crashes rethrows a parked report and `IntegratedServer` is not
  one, so a worker dying on the server's work takes down the client. The
  sentences are pass 5's, moved; the framing is new.
- `anatomy` — the five *main* methods moved from the closer to the head of
  *From main to a world*, and the bootstrap paragraph's "both *main* methods"
  became "every one of those *main* methods". The count claim is new:
  `SharedConstants.tryDetectVersion` opens more than two of them.
- `anatomy` — "the textbook case of *waiting drains*" replaced by the
  mechanism it named: a thread blocking on this half keeps running that
  half's queue, which is why the wait cannot deadlock.
- `anatomy` — the closer's tick-rate answer now says `ServerTickRateManager`
  is the server's **subclass** of `TickRateManager`
  (`ServerTickRateManager.java`:11) rather than sitting "over the shared"
  one, and the budget answer names `MinecraftServer.haveTime` as one boolean.
- `anatomy` — *Where to look* cut from nineteen names to twelve under A12.
- `what-this-book-skips` — the nine *covered* and *absorbed* rows of the
  rulings table became one paragraph claiming that **ten** systems once on
  the list are now taught. Count it.
- `what-this-book-skips` — the `client/animation` decline is now a table row
  of its own, claiming 16 of its 23 classes are keyframe definitions.
- `what-this-book-skips` — three uncovered corners (`client/resources/server`,
  *linkfs*, `DownloadQueue` with `DownloadCacheCleaner`) moved into *Named,
  and not yet written*.
- `identifiers-and-registries` — the `Registries.DIMENSION` /
  `Registries.LEVEL_STEM` identity, the interning-matters answer, the
  `HolderOwner.canSerializeIn` answer, the `RegistrationInfo` contents and
  the components-are-not-in-the-freeze answer all moved out of the dissolved
  closer into the body sections that needed them. The dynamic-numbering
  paragraph is **re-argued**: the client never derives a number, but the
  server's sort makes the order reproducible rather than accidental. That
  sentence is new, and it resolves a contradiction the reader found between
  the opening and the closer.
- `identifiers-and-registries` — new 1.21 blockquote at the foot, carrying
  the datagen answer and the `Block.BLOCK_STATE_REGISTRY` / `IdMapper`
  answer.
- `resource-system` — `DownloadQueue` moved from *Discover* to *Across the
  wire*, and its cap re-scoped: `DownloadQueue.MAX_KEPT_PACKS` is 20 and
  `DownloadCacheCleaner.vacuumCacheDir` counts **files**
  (`DownloadCacheCleaner.java`:30-46), so "the last twenty servers" holds
  only at one file per pack. The page now says which unit it means.
- `resource-system` — *namespace* glossed in place at its first load-bearing
  use, as the first half of an id.
- `tags` — the opening no longer carries the apply mechanism; its last
  sentence is now the claim *nothing is unfrozen and no lock is taken*.
- `tags` — the two `TagLoader.ElementLookup` forms are explained where they
  are first used, with the placeholder-`Holder.Reference` consequence
  (`MappedRegistry.createRegistrationLookup`) that used to sit 85 lines later
  in the closer.
- `tags` — the four-moments section's third moment is now stated to be a
  *different* path, with a write lock and no swap, which resolves the
  opening's "no lock" against `RegistryLoadTask.registerTags`.
- `tags` — new 1.21 blockquote at the foot carrying the *TagManager* absence
  and the singular directory; the body's version of both was cut, so check
  the blockquote rather than the body for those two claims.
- `tags` — closer cut from eight questions to four; *Where to look* from
  twenty names to ten.
- `data-components` — trace heading renamed to *Sharpness onto a sword, and
  how the client is told*; the book branch moved out of the trace's first
  arrow into a note. New claim in *The readers and the predicates*: `/give`'s
  square brackets become a `DataComponentPatch` through `ItemParser` reading
  each `DataComponentType`'s own codec.
- `data-components` — the prototype section now opens on *recorded once,
  built many times*, a framing claim about its two halves.
- `text-components` — the 256-character truncation is re-attributed: the
  `PacketSendListener.exceptionallySend` fallback fires on a failed send and
  the failure it exists for is a message too large to encode
  (`ServerPlayer.java`:985-993, where the local is named
  `truncatedMessageSize` and the hover key is
  *death.attack.message_too_long*). The forward reference in the walk
  paragraph is gone.
- `codecs-nbt-json` — new section *JSON, the third format in the title and
  the smallest on the wire*; the paragraph is unchanged, only rehoused. The
  opening's "the fourth is the one worth stopping on" became "the click",
  and "carries no component data at all" became "no component **values** at
  all", which is what the same sentence's own aside describes.
- `data-driven-types` — the loader contrast (`SimpleJsonResourceReloadListener`
  drops one file, `RegistryDataLoader` fails the whole load) and the
  one-kind-name-in-three-places fact moved from the dissolved closer into the
  traced instance. `Codec.either` is now named where the bare-value rule is
  stated.
- **`src/systems/anatomy/README.md` — re-argued.** The claims: four threads
  worth memorising, *named* (Render, Server, Netty event loop, shared worker
  pool); nine lanes in the corpus are not classes; the part's own packages
  are wholly named, from the generated include.
- **`src/systems/foundations/README.md` — re-argued.** The claim is new: the
  seven pages are not seven mechanisms but three used again — a codec
  describes a value, a registry names and numbers it, a pack stack decides
  which copy wins. Also new: a *Where the part stops* section claiming
  `net/minecraft/util` is a grab-bag named only where a page needs it, and
  that `net/minecraft/core/dispenser` is thirteen dispense behaviours the
  book names nowhere. Both come from `pass5_coverage.py` rather than a hand
  count; the *thirteen* wants checking against `core/dispenser`.
- Ten figure edge labels on `foundations/README` rewritten to drop class
  names the part has not introduced (`Holder.Reference`,
  `ComponentSerialization`, `HolderSet`). No arrow changed direction.

### Anchors moved (every citation repointed in the same commit)

- `tags` gained six H3s in *From JSON to a parrot's decision*;
  `identifiers-and-registries`:195 and :348 and `worldgen/trees`:101 were
  repointed at `#the-check-is-a-field-read` and `#prepared-then-applied`.
- `data-components`'s `#the-trace-sharpness-at-the-enchanting-table` and
  `text-components`'s `#eight-clicks-three-hovers-one-refusal` were renamed;
  no page cited either.
- `identifiers-and-registries` and `data-driven-types` lost
  `#questions-players-ask`; no page cited either.

## Pass 6, session A — the standard and the exemplar *(2026-09-10)*

*Two pages rewritten: `world/environment-attributes-and-timelines` (the
exemplar, rewritten whole to the pass-6 standard) and
`commands/README` (one paragraph, for the coverage include). `TEMPLATE.md`
and `docs/pass6-brief.md` Part 3 changed too and are not pages.*

### Corrections — every one re-derived against the decompile

- `world/environment-attributes-and-timelines` — the opening said *"At tick
  12542 on the overworld clock the sun goes under, and three things a player
  would never connect happen at once"*, and only one of the three is at 12542.
  `data/minecraft/timeline/day.json`: the *visual/sky_color* track is a
  **multiply** whose keyframes hold `#ffffff` to tick 11867 and reach
  `#000000` at 13670, so the sky slides across that stretch;
  *gameplay/monsters_burn* flips false at 12542 and true at 23460; and the
  sun crosses the horizon at ≈12782 by the page's own sun-angle Bézier (see
  the next item). Now: *"Dusk on the overworld clock is a stretch and not an
  instant. Between tick 11867 and tick 13670 … part-way through, at tick
  12542 …"*.
- `world/environment-attributes-and-timelines` — the same sentence said mobs
  *"stop being in danger of burning at dawn"*, which reads as the danger
  ending at dawn. `day.json`'s *gameplay/monsters_burn* keyframes are
  `{12542: false}`, `{23460: true}`, modifier *or* — burning resumes at dawn.
  Now *"until dawn"*.
- `world/environment-attributes-and-timelines` — *"the same four numbers
  exist twice more as records"*. `ClockState.java:7` is
  `record ClockState(long totalTicks, float partialTick, float rate, boolean
  paused)`; `ClockNetworkState.java:7` is `record ClockNetworkState(long
  totalTicks, float partialTick, float rate)` — three, not four. The page now
  says `ClockState` carries all four and `ClockNetworkState` three, with the
  paused flag as the whole of what the client does not get (which the page
  already said in the next sentence, contradicting itself).
- `world/environment-attributes-and-timelines` — *"a 1-4-6-4-1 kernel lerped
  by the sub-cell offset on each axis"*. `GaussianSampler.java:10` is a
  **seven**-entry array `{0, 1, 4, 6, 4, 1, 0}`, and `:23` lerps between
  entries *i+1* and *i* by the sub-cell offset for each of the six taps on an
  axis (`GAUSSIAN_SAMPLE_BREADTH = 6`, `GAUSSIAN_SAMPLE_RADIUS = 2`). Five
  weights over six cells does not close, which is what the reader caught.
- `world/environment-attributes-and-timelines` — *"both read the flash
  through the accessibility option Hide Lightning Flashes, which reports a
  flash time of zero"* — as written the option always reports zero.
  `ClientLevel.java:976`: `getSkyFlashTime` returns 0 **when the option is
  on** and `skyFlashTime` otherwise. Now *"reports a flash time of zero while
  it is switched on — so the two layers are still there and simply never
  fire"*.

### Claims introduced — `world/environment-attributes-and-timelines`

- The verified line is new: *"dusk falls over a taiga, and one value is
  resolved through a stack of layers — on the server for a mob, and again on
  the client for the sky"* (it said *"The trace: dusk falls — …"*).
- *The cast* gains a lead: *"Eight classes carry a value from the data pack
  to the sky. The first two thirds of this page is the machinery, object by
  object; the last third runs dusk through it twice, once on each side."* A
  claim about the page, not the game — check it still describes the page.
- The `EnvironmentAttribute` cast row now names the three flags —
  *positional*, *spatially interpolated*, *syncable*
  (`EnvironmentAttribute.java:14-16`, and the row already claimed *three*).
- *positional* is now defined at first use: *"an attribute is positional
  unless its builder says otherwise — positional meaning its answer is
  allowed to differ from block to block"*
  (`EnvironmentAttribute.Builder`'s default `isPositional = true`,
  `EnvironmentAttribute.java:71`).
- *"`AttributeTypes` registers fourteen of them, in four families: two
  boolean kinds, three numeric, two colour, and seven enumerations a data
  pack picks a name from"* — the grouping is new (`AttributeTypes.java`:
  boolean, tri_state · float, angle_degrees, integer · rgb_color, argb_color
  · moon_phase, activity, bed_rule, particle, ambient_particles,
  background_music, ambient_sounds).
- *"six logic gates for a boolean, six arithmetic ones for a float, four ways
  to combine two colours"* — the same counts the page gave per modifier
  class, now stated per type family.
- The `Timelines.MOON` period cell says **192000 — eight days** where it said
  `24000 × MoonPhase.COUNT` (`data/minecraft/timeline/moon.json`:
  `period_ticks: 192000`).
- New paragraph in *The four timelines*: *"a timeline with no period is not a
  cycle at all — its track runs once against the clock's total ticks and then
  holds its last value forever"* — moved up out of the closer's pillager
  answer, which now states only the consequence.
- The villager-schedule paragraph (`Brain.setSchedule`, the two tracks,
  `Brain.updateActivityFromSchedule`'s 20-game-tick throttle, the link to
  points of interest) moved from the closer into *The four timelines*
  unchanged in substance.
- New paragraph in *What crosses the wire*, all of it new: **syncable** is
  the third flag; *"Thirty-three of the 48 carry it: every one of the 24
  visual/ attributes and all four audio/ ones, and five of the gameplay flags
  — sky_light_level, fast_lava, water_evaporates, piglins_zombify,
  creaking_active. The fifteen left behind are gameplay decisions the server
  makes alone"*, and *"the client's stack is shorter than the server's, and
  identical everywhere the client actually looks"*
  (`EnvironmentAttributes.java`, counted by `.syncable()` on each
  `register(…)`: 33 of 48, the 15 without it all `gameplay/`).
- The trace heading is now *"Dusk, and the same question asked twice"* (was
  *"The trace: dusk falls"*), and its lead sentence changed to *"Both go
  through the stack above, and this is the machinery running."* No inbound
  link landed on the old anchor.
- *"The step that reads oddly is the fifth"* is now named rather than
  numbered — *"the one where the sampler asks whether any layer of the
  attribute is positional and finds that none is"*.
- Re-scoped appositive: *"`LavaFluid.isFastLava` and `Entity` …, the two
  sites that between them decide how fast lava flows and how hard it
  shoves"* — `LavaFluid.java:237` reads `FAST_LAVA` for the fluid's own
  spread, `Entity.java:1756` for the push scale (0.007 against
  0.0023333333333333335). The old sentence's *"the pair"* read as the two
  attributes.
- The six probe consumers are now a clause — *"everything that draws the sky
  goes through it — the sky, the lightmap, the two fog environments, the
  clouds and the music"* — so `LightmapRenderStateExtractor`,
  `AtmosphericFogEnvironment`, `WaterFogEnvironment` and `LevelExtractor` are
  no longer named on the page (logged in [pass5.md](pass5.md)).
- The server/client one-tick disagreement moved from the closer into *The
  same value on the client*, with a new framing sentence: *"The last
  difference is a tick wide, and it is the reason the two sides can disagree
  about the sky for one tick at dusk."* The mechanism is unchanged.
- `TimeCommand`'s two registrations are now *"Everything `TimeCommand` offers
  is offered twice, once against the source level's
  `DimensionType.defaultClock` and once under `/time of` against a clock the
  player names"*; the six subcommand names and the `/time query gametime`
  exception are cut (logged).
- The 1.21 blockquote moved to the foot, 11 lines to 8, and asserts something
  the old one only implied: *"ultrawarm has become two of them,
  `EnvironmentAttributes.FAST_LAVA` and
  `EnvironmentAttributes.WATER_EVAPORATES`"* — by elimination against
  `DimensionTypes.java:39`, where the nether sets `BED_RULE`,
  `RESPAWN_ANCHOR_WORKS`, `WATER_EVAPORATES`, `FAST_LAVA` and
  `PIGLINS_ZOMBIFY` for the four old booleans. `DimensionType.hasFixedTime`
  and `DimensionType.ambientLight` "stayed put" is cut from the blockquote.
- The closer keeps three questions (the nether's night, `/time` and the End,
  the pillager patrols) and loses two to the body. Every answer left is a
  consequence a player meets — the A2 test, applied.

### Claims introduced — `commands/README`

- *Where the part stops* now opens on
  `{{#include ../../generated/coverage-commands.md}}` — **21% of the part's
  lines are named on no page in the book**, from `pass5_coverage.py --write`
  over `map_source.py`'s `PARTS`. The sentence around it is new: *"the
  catalogue is where they sit: not quite a third of this part by line is
  command registrations rather than machinery"* (12,781 of 43,126 lines by
  `map_source.py packages`, which is 29.6%). The claim that the unexplained
  lines are mostly the catalogue is the old sentence's and is unchecked.

## Pass 6, the planning session — between passes 5 and 6 *(2026-09-07)*

*No page's prose was touched. What this session introduced that pass 9
should know about, because each is a claim:*

- **`src/generated/coverage-<dir>.md`**, thirteen generated phrases — *N% of
  the part's lines are named on no page in the book* — written by
  `pass5_coverage.py --write` from the atlas's `PARTS` mapping, with a name
  that appears only inside a figure counted as unnamed. A generated page is
  checked by re-deriving its population: `map_source.PARTS` less `SKIPPED`,
  a class being a file, `package-info.java` excluded. Included on no page yet;
  pass 6's sessions swap the four hand-counted numbers for it (`entities/README`
  *about 40%* against a generated 34%, `items/README` *about a third* against
  24%, `player/README` *97% named* against 0% unnamed, `worldgen/README` *a
  quarter* against 19%) — each swap is a correction of the prose to the
  population, and the part session logs it here.
- **Twenty strikes in [pass5.md](pass5.md)**, each a claim that an entry is
  settled, verified before striking: `the-client-loop`:12 and :21 link
  `anatomy`; `chunk-generation-pipeline` no longer names
  `Util.maxAllowedExecutorThreads`; `Gizmos` is on
  `debugging-the-running-game`; `scoreboard-and-data` names `ServerBossEvent`;
  `reference/submit-phases` names `SubmitNodeStorage`; `maps/biggest`:38 says
  *make the thirty*; the glossary's *Quart* and *Render state* carry one link
  each; `reference/level-data-and-rules` has no *Responsibility*-era heading;
  four Part XII pages link the two Part II pages; `check_deps.py`'s header
  lists the Reference-parts-column check; the other nine are settlements the
  entries' own last lines record (*Done, session …*).
- **Two entries carried to [pass3.md](pass3.md) §7** that session E's log said
  were there and were not: the hopper, and four block-entity state machines.
  The claim beside them — that `blocks/README`'s *Where the part stops* names
  only the sculk spread as belonging to nobody — is read from the page's
  second paragraph under that heading.
- **The charter's device counts corrected from the tool**: five closer
  spellings (an H2 starting *Questions*), not seven; 39 pages carry the 1.21
  blockquote by its own form (`> **For a 1.21-era reader.**`), not 42.

## Pass 5, session O — the close: the frame, the summarisers and the pass's own queue *(2026-09-07)*

*Pass 5's closing session. Four reader agents: one on the introduction, one on
`lectures.md`, one on the thirteen landing pages read as one set (a brief
written this session — no session in the project has read all thirteen
together), and one on the glossary's owner links entry by entry. The session's
own work was the audit: the forty explicitly-tagged `[kind=book]` entries still
open in [pass5.md](pass5.md) checked one at a time against the corpus, and
`docs/pass9.md`'s own shape. Everything below is either a claim this session
introduced or a correction it made with the decompile open; the corrections
come first.*

### Corrections — what the page said, what the decompile says

1. **`entities/entity-anatomy`:393 — what `EntityType.trackDeltas` is.** The
   page called it "a hard-coded list of types whose velocity is never sent at
   all". `EntityType.trackDeltas` (`EntityType.java`:447-449) is a method
   returning `true` for every type *except* ten named ones, so the page had the
   sense of the name inverted; and velocity is not "never sent" for those ten,
   because `ServerEntity.sendChanges` takes the delta branch when
   `Entity.needsSync` is set or a `LivingEntity` is elytra-flying
   (`ServerEntity.java`:206-217), and `Entity.hurtMarked` sends a motion packet
   outside the branch entirely (:267-269). Page against page:
   `networking/what-the-client-is-told`:222 had it right as "a hardcoded
   exclusion list". Now "a third parameter, `EntityType.trackDeltas`, which is
   true of every type but ten", with the roster left to its owner.

2. **`introduction`:148 — three things called skipped that the skips page says
   are taught.** The introduction listed "the data generators, statistics and
   the recipe book, the OpenAL audio backend and two packages nobody will
   recognise" as "all in the jar and not in the parts".
   `anatomy/what-this-book-skips` says the opposite of three of them, in its own
   headings: `com/mojang/blaze3d/audio` is "hatched for its *address* rather
   than for being unread" and "is taught, in Part X, by the sound engine"
   (:363-376); `net/minecraft/gizmos` "is taught where its output is, in Part X"
   (:272-283); and `RecipeBook`, `RecipeBookSettings` and `ServerRecipeBook`
   "are not skipped, they are recipes'" (:263-268). The frame is the summariser
   and the page wins: the introduction's list now names player reporting and the
   id-constant tables instead, and a following sentence says the page tours
   three things that are not skipped and why.

3. **`anatomy/README`:11 — what a non-class lane stands for.** "The handful
   that are not stand for a thread." `check_lanes.py --strict` prints nine word
   lanes, and four of them are not a thread: `Disk` (the save on disk), `Game`
   (the game's own code above Blaze3D), `JVM` (the process) and `Wire` (the
   network between the two programs). `reference/README`:68 already said "the
   nine that mean a thread, a process or a boundary instead". Now "the nine that
   are not are a thread, a process, or the boundary between the two programs".

4. **`server/README`:23 — `MinecraftServer` among `server/level`'s forty-two.**
   The sentence read "over half of those lines are `net/minecraft/server/level`'s
   forty-two classes … One of them, `MinecraftServer`, is most of this part's
   first three pages." `MinecraftServer.java` is in `net/minecraft/server`, one
   package up, and `map_source.py`'s `PARTS` counts it under Part I. Now says so
   explicitly and keeps the point.

5. **`player/README`:125 — "the smallest part of the book".** Part VIII is 29
   classes and 8,135 lines; Part I is **7 classes and 6,770 lines**, smaller by
   both measures (`src/generated/part-player.md`, `part-anatomy.md`). Now "the
   smallest part of the book with a system in it", naming Part I as the
   exception.

6. **`rendering/README`:24 — "the largest thing on the client by a distance".**
   Part XI is 1,254 classes and 93,012 lines; Part X is 677 and **93,640**. By
   lines Part X is larger; by classes Part XI is nearly double. Now "the largest
   thing on the client, by classes and by a distance — nearly twice Part X's, in
   about the same number of lines". (The comparison the sentence goes on to make,
   420 classes and 53,000 lines for the whole of `net/minecraft/server`, was
   re-derived and is right: 420 files, 52,720 lines.)

7. **`networking/README`:125 — "the whole of `net/minecraft/network`".**
   `map_source.py`'s Part IX subtracts `net/minecraft/network/syncher` and gives
   it to Part VI, which `entities/README`:21 states from its side. "Whole" is
   what made it false rather than loose; now "less `network/syncher`, which is
   Part VI's".

8. **`commands/README`:126 — "Most of this part by line is the catalogue".**
   The catalogue the page sizes four lines earlier is 102 files and 12,781 lines
   of a part that is 43,126 — under a third. Now "Not quite a third of this part
   by line is the catalogue rather than the machinery, and it is where the
   unexplained lines are."

9. **`lectures.md`:88 — lighting's consumer is not Part XI.** "Inside the
   chain, but nothing later in this part assumes it; Part XI does."
   `check_links.py --inbound src/systems/world/lighting.md` lists twelve links
   from eight pages and **no page under `systems/rendering/`** among them;
   `rendering/README`'s *before you start* does not name it either. The pages
   that lean on it are `networking/what-the-client-is-told` (twice) and
   `client/the-client-level`. Now "Parts IX and X do".

10. **`lectures.md`:171 — the three places a menu broadcast happens.** The map
    said containers and menus "needs all three of Part III's and Part VIII's
    tick pages … the drain, the level's entity phase, and the player's second
    half". `items/containers-and-menus`:325-336 gives the third place as
    `ServerPlayer.doTick`, "driven by the connection after every level has
    finished", which "repeats only the `AbstractContainerMenu.stillValid`
    distance test, **without a broadcast**". Two broadcasts, both Part III's.
    Now "needs both of Part III's tick pages … the packet drain at the top of
    the tick, and the level's entity phase".

11. **`lectures.md`:322 — "two statuses before the biomes and terrain".**
    `worldgen/README`:74 says "two statuses before the biomes it will stand in
    exist"; terrain (`ChunkStatus.NOISE`) is further down the ladder than
    `ChunkStatus.BIOMES`, so one count cannot cover both. "And terrain" dropped.

12. **`lectures.md`:325 — "costs one forward reference".**
    `worldgen/README`:80-83 prices the same trade at "three of the six pages
    before the structure arc reach for the beardifier before the page that owns
    it". Now "costs three of the earlier pages a forward topic".

13. **`lectures.md`:37 — Part II called a stack.** `foundations/README`:15 says
    "Part II is **not a stack but a fan**. Codecs and registries are underneath
    everything else here, and the five pages above them are largely independent
    of one another — which is why the figure has two roots and no single
    column", and its figure has two roots. The only place in the book where two
    copies of a shape sentence contradicted rather than merely differed. The map
    now says fan, and Part XIII keeps *a stack of three floors* alone.

14. **`lectures.md`:195 — Part VIII's groups with an internal order.** "Only
    one group has an internal order — the spear is the sword swing's sequel",
    three lines above the map's own entry "the two-phase tick — watch it
    immediately after *player anatomy*", and against `player/README`:104-106,
    which declares two pairs. Now "Two groups have an internal order".

15. **`lectures.md`:242 — "Nothing here hands off to anything".**
    `client/README`:18 says the same sentence "with one exception, noted below",
    the exception being the GUI stack, which the map itself then describes.
    Corrected, and "except the two pairs noted below" became "the three groups",
    because `client/README`:123-126 declares three (two and three; six to nine;
    ten and eleven, the two halves of sound).

16. **`lectures.md`:396 and `introduction`:76 — the figure's own arrows.** Both
    said Parts I and II are drawn "as boxes but not as edges" / "left off".
    `src/figures/parts-dependency.md`:16 is `P1 --> P2 --> P3`, and both edges
    are real declared dependencies (`foundations/README`:45,
    `server/README`:53-59) that `check_deps.py`'s first check requires. Three
    prose copies against one figure. Both pages now say the two keep their boxes
    and the one arrow each along the spine and have the rest left off; the same
    correction went into `check_deps.py`'s comment at :392.

17. **`lectures.md`:457 — "Three more pages are a single part's dependency".**
    Read against the thirteen landing pages, about a dozen pages are named by
    exactly one; the sentence claimed an enumeration and meant a selection.
    Rewritten as a selection with the reason for the three it names.

18. **`lectures.md`:8 — the lecture order "is confirmed by the owner".** Stated
    in the present tense as a completed fact; [plan.md](plan.md) books the
    owner's confirmation for **before pass 9**. Now written as what happens
    rather than what has happened.

19. **`reference/glossary`:461 — occlusion "a shape question a `BlockState`
    caches".** `reference/math-and-primitives`:141 says the occlusion shape is
    **not** in `BlockBehaviour.BlockStateBase.Cache`; the decompile agrees —
    `BlockBehaviour.BlockStateBase.initCache` builds the `Cache` only for a
    block without a dynamic shape (`BlockBehaviour.java`:896-897) and sets
    `occlusionShape` on the state itself unconditionally (:901-915). Now "a
    shape question every `BlockState` precomputes — a field on the state itself
    rather than anything in its shape cache", with the link to the page that
    owns the distinction.

20. **`blocks/README`:29 — "the sculk family is game events and vibrations'".**
    That page owns the sensor, the shrieker and the catalyst as *listeners*;
    `SculkSpreader` (387), `SculkVeinBlock` (211), `SculkBlock` (109) and
    `SculkBehaviour` (54) are named on no page in the book. Corrected to name
    the three the other page owns, and the gap declared (below).

### The claims this session introduced

**`introduction`** — the part list names all thirteen parts, where it named ten
systems for thirteen and called Part III by the title of one of its pages; the
landing page's role is stated as the six things `TEMPLATE.md` requires, where it
stated three; the Maps paragraph now separates the generated figure and table
from the hand-written prose, which is the distinction `maps/README`:10-20 makes
load-bearing; the Reference paragraph says twenty-three pages (the count
`reference/README`:9 states and `SUMMARY.md` lists), links the tier's own front
page, `reference/threads` and `reference/class-index` for the first time, and
says "rather more than half" are regenerated (thirteen of twenty-three, per
`reference/README`'s own figure); the gates paragraph names the sidebar and the
Reference shelf's *parts* column, which `check_deps.py` gained in pass 5's
sessions A and N; the anatomy link takes the owner's anchor.

**`anatomy/what-this-book-skips`** — a new clause saying the table has fifteen
top-level rows against the treemap's fourteen hatched boxes, because the map's
smallest box is a package four levels deep and
`net/minecraft/client/multiplayer/chat/report` is six.

**`entities/entity-lifecycle`** — a new subsection, *The variant that same
method picks*: seven species (`Chicken`, `Cow`, `Pig`, `Cat`, `Frog`, `Wolf`,
`ZombieNautilus`) call `VariantUtils.selectVariantToSpawn` from their own
override of `Mob.finalizeSpawn`; `PriorityProvider.select` unpacks every
variant's `SpawnPrioritySelectors`, sorts by priority descending and keeps only
entries at or above the highest priority whose condition passed, and
`PriorityProvider.pick` then chooses uniformly at random among those; a selector
with no condition always matches; `SpawnConditions` registers `BiomeCheck`,
`StructureCheck` and `MoonBrightnessCheck`; and the shipped
*cat_variant/all_black.json* uses priority 1 for the swamp-hut structure and 0
for a moon brightness of at least 0.9. The `Entity.RemovalReason.DISCARDED` row
gained "a `ConversionType.SINGLE` conversion (`Mob.convertTo` adds the new mob,
then discards the old — `ConversionType.SPLIT_ON_DEATH` keeps it)", which pays
off `points-of-interest`:375's link.

**`blocks/block-entities`** — a new passage in *Loaded is not enough to tick*:
`SpawnerBlockEntity` holds an anonymous `BaseSpawner` and hands it the tick, the
delay and spawn count and required player range and rolled `SpawnData` live on
the `BaseSpawner`, which is not a `BlockEntity`; `BaseSpawner.serverTick` and
`BaseSpawner.clientTick` are different methods and the client one runs its own
copy of the countdown to spin the cube and drop smoke and flame, both gated on
`BaseSpawner.isNearPlayer`; and `TrialSpawnerBlockEntity` is the same
arrangement with `TrialSpawnerState` and `TrialSpawnerStateData` on top.

**`foundations/codecs-nbt-json`** — a new clause: `GsonHelper` is sixty-nine
static helpers, each pulling one typed field out of a parsed object and naming
the field in the exception, and it is called from 109 places outside its own
file that were never converted to codecs.

**`blocks/README`** — a new paragraph declaring the sculk spread machine as the
one mechanism in Part V's two packages that no page explains, with the reason
(its scenario is a mob dying on sculk, not a block hearing a neighbour) and the
size (about 760 lines).

**`reference/glossary`** — eight headwords added (*Feature flag*, *ItemStack*,
*LivingEntity*, *MinecraftServer*, *Particle*, *Player*, *Random tick*,
*Widget*), each a sentence drawn from the owner page and an anchored arrow;
**twenty-seven more arrows given anchors**, so 73 of the file's links now land on
a section instead of a page top; two arrows repointed (*Loot context* to
`#inputs-then-one-invocation`, *ServerEntity* to
`#one-entitys-tick-and-the-gates-it-does-not-pass`); four two-owner entries
reduced to one owner (*Chunk layer* to `models-and-atlases`, *NoiseChunk* to
`density-functions`, *StructurePiece* to `hand-built-structures`, *ServerPlayer*
to `player-anatomy`), each keeping the loser's distinct half as a clause; three
headwords marked for sense (*Batch* (game tests), *Trigger* (advancements),
*Sensor* (brains)) with a link to the other sense; seven headwords moved into
alphabetical order. 171 headwords, from 163.

**`items/README`** — the Reference link that read "Enchantment helpers" is *The
weapon helpers*, its real title, and "Two were written for it" introduced three.

**`lectures.md`** — the two Reference asides cut (the rule is stated once at the
top for all of Reference); the Part V/X cut reduced to a clause and a link to
the section that states it in full; Part VI's dependency clause now leads with
Part III; the *authority* blurb's "the one page most often skipped" replaced,
because nothing in the project can know what a viewer skips; the three pages
worth taking out of turn are linked at first mention and the one that is a
departure from the sidebar order is distinguished from the two that are not.

**`map_source.py`** — `net/minecraft/client/multiplayer/chat/report` added to
`SKIPPED`, so the twelve classes and 952 lines the book declares skipped stop
counting toward Parts IX and X. Part X moves from 689/93,640 to 677/92,688 and
Part IX from 496/39,434 to 484/38,482; `parts.md` and both `part-*.md` phrases
are regenerated. This is a claim about the population every landing-page size
sentence and every coverage report is built on, so pass 9 should check it first.

### The pass's own strikes, audited

Forty entries in [pass5.md](pass5.md) carried an explicit `[kind=book]` tag and
were still unstruck at the pass's close. Read one at a time against the corpus:
**twenty-six were settled by a later session and never struck** (among them the
`authority` ↔ `prediction-and-acks` citation session F routed to J, which J
made at `authority`:22 and :116; the twenty-two anchors on `authority`'s inbound
links, of which thirty links from twenty-one pages now carry one and only the
summarisers do not; `reference/threads`' server-side never-hop table, built by
session N; the two landing pages that hand-counted a size, both now
`{{#include}}`; `util/worldupdate`, placed on `chunk-storage`:320-326 by session
D; the boss bar, settled twice over by session M). **Eight were never open**:
they are pass-3 cut logs and pass-3 session records that `pass5_queue.py`'s
guesser routes to `book` because of the words in them. **Six were genuinely
open**, and this session closed five (`GsonHelper`, the `SpawnCondition`
hand-forward, the `SpawnerBlockEntity` hand-forward, the sculk gap, the
`level-data-and-rules` ruling) and routed one forward with a reason. No strike
this session examined had settled nothing — the failure mode in pass 5's queue
was the opposite of pass 4's, an entry settled in the pages and left standing in
the file.

### The file's own shape

`docs/pass9.md` said its entries are written "per session, newest first" and
held them in the order I, H, G, F, E, D, M, A, planning, B, C, J, K, L, N —
sessions appended at the top for six sessions and at the bottom for six more.
Reordered to the stated rule, and the six headings written in three other forms
normalised to `## Pass 5, session X — <part> *(date)*`. No entry's text changed.
Pass 9 reads this file first, so its order is a claim like any other.

## Pass 5, session N — Reference, the maps, and the frame's Reference-facing pages *(2026-09-07)*

Sixteen pages read by one agent each — the eleven hand-kept Reference pages and
the five maps; the ten generated Reference views were not read, because a
generated page's claims are its generator's. Three new generated views were
built. **Pages changed: 24.** Eleven of the corrections are on pages outside the
tier, because almost everything the shelf holds is a fact some lecture also
states.

### Corrections (what the page said · what the decompile says · where)

1. **`maps/README`:9-11** said "Nothing here is hand-counted … the pages are
   regenerated with the figures each time the site is built, so a number on a
   map cannot drift." Only `src/generated/` is regenerated (`tools/deploy.sh`:9,
   `tools/map_source.py`); every number in the four map pages' **prose** is typed
   by a session. Found independently by the `maps/README` and `maps/hierarchy`
   reads. The paragraph now separates the generated half from the hand-written
   half and says the version pass owes the sentences a re-read.
2. **`maps/biggest`:29-30** — "`Entity`, `LivingEntity`, `Player`, `ServerPlayer`,
   `LocalPlayer` and `Mob` are one chain of inheritance … each is the base of
   everything below it." `Entity.java`, `LivingEntity.java`, `Avatar.java`,
   `Mob.java`, `Player.java`, `ServerPlayer.java`, `LocalPlayer.java`: `Mob` and
   `Avatar` are two of `LivingEntity`'s direct subclasses, `Player extends
   Avatar`, `LocalPlayer extends AbstractClientPlayer`, and neither player leaf
   is the base of anything. Rewritten as a trunk and a fork.
3. **`maps/biggest`:33-34** — "the pages a reader of Part VI should expect to be
   long" promises `Fox` and `Bee` pages the book does not have and has ruled out
   (`systems/entities/README`:26-31). Re-aimed at that ruling.
4. **`maps/biggest`:33** — "Only two concrete mobs make **the list**" is true of
   the thirty the figure draws; the table below has forty rows and three more
   mobs (`Panda`, `AbstractHorse`, `SulfurCube`). Now "the thirty".
5. **`maps/fanin`:24-26** — "The thirty hubs … are seven, and Part II is the
   first six of them." The table names 32 classes, 24 of them in the thirty; six
   of the thirty are in no row; and by the table's own last column Part II
   teaches three of the seven, Reference two and Part IX one. All three claims
   corrected, and `maps/README`:19 carried the same "vocabulary Part II teaches"
   sentence and was corrected with it.
6. **`maps/fanin`:42-43** — "the client's hub is a hub for a quarter of the code,
   and the shared three quarters never name it." The client-only side is 2,206 of
   7,055 files (31%) and 212,242 of 719,302 lines (29.5%), both from
   `maps/packages`:22-27. Now "under a third" and "the shared seven tenths".
7. **`reference/README`:44-63** — the *parts* column was stale in **six of twenty
   rows**, missing nine part numerals (registries ← IV; non-living-damage ← VIII;
   threads ← VI; level-data-and-rules ← IX; naming-drift ← VII, X; glossary ← II,
   V, VI). Derived from the thirteen landing pages' `## Reference this part uses`
   sections and now enforced by `check_deps.py`.
8. **`tools/gen_reference.py`, the registries blurb** — "Every registry key
   declared in `Registries`", printed above a total of **153**. 148 are declared
   in `Registries.java`; five are declared by their own class with the public
   `ResourceKey.createRegistryKey` (`ServerFunctionLibrary`, `ClockTimeMarkers`,
   `RecipePropertySet`, `EquipmentAssets`, `WaypointStyleAssets`) — which the
   tool's own comment already recorded. The blurb now names them and cites the
   lecture's 148.
9. **`reference/threads`:69** — RCON starts "when *enable-rcon* **and**
   *rcon.password* is set". `RconThread.create` (`RconThread.java`:61-76) also
   returns null when *rcon.port* is outside 1–65535, and tests the port **first**.
10. **`reference/threads`:65** — `Util.nonCriticalIoPool` is "the same shape" as
    `Util.ioPool`. `Util.java`:110-111 passes `daemon=false` for *IO-Worker-* and
    `daemon=true` for *Download-*, which is the one difference the new column is
    about.
11. **`server/server-tick`:107-117** — "the nine that do not divide into three
    kinds", then a taxonomy accounting for **seven**. The nine are
    `handlePingRequest`, `handleCustomPayload`, `handleChat`, `handleChatCommand`,
    `handleSignedChatCommand`, `handleSignUpdate`, `handleEditBook`,
    `handleChatAck` and `handleConfigurationAcknowledged`
    (`ServerGamePacketListenerImpl.java`); the last two write listener state on
    the Netty thread and were in no kind. Four kinds now.
12. **`reference/level-data-and-rules`:219-221** — 29,999,984 attributed to the
    integrated server. `MinecraftServer.getAbsoluteMaxWorldSize`
    (`MinecraftServer.java`:1632) returns it; `DedicatedServer` overrides.
13. **`reference/level-data-and-rules`:16-21** — "Four parts point here"; five do
    (`networking/README`:117 is the fifth), which `check_deps.py` now enforces
    from the shelf's side.
14. **`worldgen/creating-a-world`:96-97** — `world_gen_settings.dat` is written
    "beside *raids.dat*". `WorldGenSettings` goes into `MinecraftServer`'s
    server-global `savedDataStorage` (`MinecraftServer.java`:355); `Raids` goes
    into `ServerLevel.getDataStorage()` (`ServerLevel.java`:259), which is
    per-dimension. Different folders; the clause is cut.
15. **`reference/naming-drift`:42 and :383** — "Two hundred and forty-three rows",
    twice. The thirteen part tables hold **245** (3+4+31+18+12+18+30+9+24+20+27+13+36).
16. **`reference/naming-drift`:416-417** — the bullet still italicised
    *Entity.hurt* as a name that is gone, against its own corrected table row.
    `Entity.java`:2031-2040: `Entity.hurt` is a `@Deprecated` **final returning
    void** that forwards to `Entity.hurtServer` only.
17. **`reference/naming-drift`:290** — "`ByteBufferBuilder` → `MeshData`".
    `BufferBuilder.build`/`buildOrThrow` produce the `MeshData`
    (`BufferBuilder.java`:68-78); `ByteBufferBuilder` is the memory under it, which
    is what `blaze3d`:354 says.
18. **`reference/naming-drift`:496** — backticked `Minecraft.setScreen`, which
    does not exist in 26.2 (`Minecraft.java` has only `setScreenAndShow`, and the
    field lives on `Gui`). Italicised, as the page's own rule requires.
19. **`rendering/the-window`:302-303** — "*ScreenManager*, which never existed
    here" against `naming-drift`:313, which lists it as a rename. Whether an older
    tree used the name is outside rule 3; the sentence now states only what 26.2
    settles (monitor handling is `MonitorManager`) and cites the rename table.
20. **`reference/math-and-primitives`:116** — "two things called `Axis`". Three:
    `Direction.Axis`, `com/mojang/math/Axis`, `ChunkPalettedStorageFix.Axis`. Now
    "two in scope", with the third named as out of it.
21. **`reference/level-data-and-rules`:94-97** — `LevelResource.MAP_RESOURCE_FILE`
    glossed nowhere and then, in this session's own first draft, as the map-id
    counter. It is `resourcepacks/resources.zip` (`LevelResource.java`:15). Caught
    before publishing and recorded because a fix is a claim.

### Suspicions re-derived and found sound (no change, or a sharpening only)

- **`reference/level-data-and-rules`:211-212** — "a fresh `WorldBorder` starts
  with a warning time of 15, not 300." True and sharper than it looks:
  `WorldBorder(Settings)` (`WorldBorder.java`:44-53) sets `warningTime = 15` and
  stores the settings **without applying them**, so even a border built from
  `WorldBorder.Settings.DEFAULT` (whose `warning_time` is 300) is live at 15.
- **`maps/fanin`:45** — "all but ten of the files that import `Schema` are in
  `util/datafix`." Exactly ten, and all ten are in its sibling `util/filefix`;
  the page now says where they are.
- **`maps/biggest`:44** — `SoundEvents` grouped with the catalogues-written-as-code.
  1,668 `SoundEvent` constants, one `register(...)` per line.
- **`maps/biggest`:42** — "`FriendlyByteBuf` is the buffer both read from."
  `RegistryFriendlyByteBuf extends FriendlyByteBuf`, so play's buffer is one.
- **`reference/glossary`, the "five headwords the corpus does not use"** (pass-4
  session O). Re-measured with whitespace normalised: **four**, not five, and all
  four are compound noun phrases the corpus writes in pieces. Ruled to stand; the
  original count was a line-wrap artefact.

### Claims introduced (check these first)

**Three new generated views** (`tools/gen_reference.py`, each read off the
decompile or the shipped data on every deploy; the numbers below are what the
generator printed on 26.2 and will move on a version bump):

- `reference/spawn-reasons.md` — 19 reasons, **11 tested somewhere, 20 test
  sites**, and a *classes that pass it* count per reason. The claim behind the
  view is that a "test" is a comparison against the constant and everything else
  is a pass-through; the enclosing method is found by walking up to the nearest
  access-modifier-led signature. **Eight reasons are tested by nothing**, and all
  but two comparisons are inside `Mob.finalizeSpawn` — both stated on
  `entities/entity-lifecycle`.
- `reference/weapon-helpers.md` — 7 helpers, **42 items**. The claim: an item
  reaches a helper directly (`sword`, `pickaxe`, `spear`) or through the class
  that wraps it (`AxeItem`, `HoeItem`, `ShovelItem` each call theirs in `super`),
  and "components it sets" follows one hop into `ToolMaterial`.
- `reference/structure-spawn-overrides.md` — **34 structures carry
  `spawn_overrides`, six fill it in, 23 overrides, 18 of them empty.** The claim
  that an empty spawn list is a *ban* rather than a no-op is the view's argument
  and is stated on `entities/entity-lifecycle` too.

**New prose claims:**

- `reference/threads` — a *daemon* value for every row: Render thread and *main*
  no (they are the JVM's), Server thread no (`MinecraftServer.spin`), Netty yes
  (`EventLoopGroupHolder.createThreadFactory` sets it), Worker-Main yes
  (`ForkJoinPool`, and `how-a-server-dies`:217-220 already said so), IO-Worker
  **no** and Download yes (`Util.java`:110-111), sound engine yes
  (`SoundEngineExecutor.createThread`), watchdog/console/management yes, timer
  hack yes, RCON and query **no**. Plus: RCON and query poll on a **500 ms**
  socket timeout (`RconThread.java`:82, `QueryThreadGs4.java`:277) and
  `RconClient` sets `setSoTimeout(0)`, so it does not poll at all.
- `reference/threads` — a new *main* row for the dedicated server, and a nine-row
  table of the server handlers that never hop, with what each does on Netty.
- `reference/threads` — the closing section cut from four rules to one paragraph
  with three citations; the claim introduced is that `BlockableEventLoop.managedBlock`
  is `server-tick`'s to own, not this page's.
- `reference/level-data-and-rules` — a thirteen-row `LevelResource` table.
- `reference/submit-phases` — `TranslucentSubmit` declares one method,
  `TranslucentSubmit.distanceToCameraSq`, and **five** of the thirteen renderers'
  nested *Submit* records implement it (`BlockModelFeatureRenderer`,
  `ItemFeatureRenderer`, `ModelFeatureRenderer`, `MovingBlockFeatureRenderer`,
  `NameTagFeatureRenderer`).
- `reference/glossary` — eight new entries (*Occlusion* with four senses, *Loot
  context*, *Loot condition*, *Parameter set*, *Data-driven type*, *ServerPlayer*,
  *Status effect*) and second senses added to *Frame*, *Criterion* and *Level*.
  The *Occlusion* entry's four senses are each a claim.
- `reference/README` — the tier's argument re-aimed from *what regenerates it* to
  *how it survives a version bump*, and a paragraph saying the last column is
  gated.
- `maps/README` — a new mermaid figure of the atlas's own pipeline, whose node
  labels ("eight SVG figures", "six tables", "the thirteen per-part size
  phrases") are counts of `src/generated/`.
- `reference/hud-elements` — "this is the whole of what a screen contributes to
  the record", which answers pass-4 session O's *three or four strata* question
  in the negative and is the session's own reading of `Gui.java`:183-207.

### Rulings

- **The shelf's *parts* column is derived, not kept.** `check_deps.py` gained a
  fourth `F` check with a probe; the rule is the column header's own words.
- **`hud-elements`' contextual bar keeps two rows.** The ordering *is* the fact.
- **The glossary disambiguates**, for a word the corpus itself uses in more than
  one sense, and the entry is the disambiguation (A5's rule, applied to
  *Occlusion*, *Frame*, *Criterion* and *Level*).
- **`MapItemSavedData`, `MapIndex` and `WanderingTraderData` stay named-only** —
  declared on the table rather than given a lecture. To [pass3.md](pass3.md) §7.
- **`starting-a-server` keeps its boot thread table**; only the per-thread
  properties moved to the shelf.

## Pass 5, session M — Part XIII · Commands and data packs *(2026-09-07)*

All ten pages of the part rewritten — `commands/README`,
`commands/brigadier-and-commands`, `commands/permissions`,
`commands/entity-selectors`, `commands/the-execution-engine`,
`commands/functions-and-macros`, `commands/advancements`,
`commands/scoreboard-and-data`, `commands/dialogs`, `commands/game-tests` —
plus eight pages elsewhere: `foundations/data-driven-types`,
`foundations/resource-system`, `items/contexts-and-predicates`,
`networking/README`, `blocks/README`, `client/hud`, `reference/glossary` and
`src/lectures.md`. The part owns no hand-kept Reference page of its own.

### Claims introduced

**`commands/scoreboard-and-data` — a new section, *The third sink is a boss
bar, and it is this page's shape again*.** Every sentence in it is new to the
book; `BossEvent`, `ServerBossEvent`, `CustomBossEvent`, `CustomBossEvents`
and `BossBarCommands` were named on no page before this session.

- "A boss bar is a named server-side thing holding a number, saved with the
  world, broadcast to the players attached to it, and writable only by a
  command."
- `BossEvent` is "an id, a name, a *progress* float from zero to one, a
  `BossEvent.BossBarColor`, a `BossEvent.BossBarOverlay`, and three booleans
  that ask the client to darken the screen, play the boss music and draw the
  world fog" (`BossEvent.java`:11–18).
- `ServerBossEvent` "adds the live membership — a `Set<ServerPlayer>` — and
  turns every setter into a broadcast" (`ServerBossEvent.java`:18, 29–101).
- "one `ClientboundBossEventPacket` with six operations, add and remove and
  one update apiece for progress, name, style and properties"
  (`ClientboundBossEventPacket.java`:118–122, the `OperationType` enum).
- "There is no serverbound counterpart, exactly as there is none for a score."
- "Four things in the game own one: `WitherBoss`, `Raid`, `EnderDragonFight`
  — and `CustomBossEvent`" (the four files that name `ServerBossEvent`).
- `CustomBossEvent` "keeps an integer `CustomBossEvent.value` and an integer
  `CustomBossEvent.max`, derives the float progress from them on every write"
  (`CustomBossEvent.java`:26–27, 77–87).
- The membership claim: a persisted `Set<UUID>` beside the superclass's live
  set, `CustomBossEvent.onPlayerConnect` re-attaching a player whose UUID is
  on the list and `CustomBossEvent.onPlayerDisconnect` calling the
  superclass's removal "deliberately so that the UUID stays"
  (`CustomBossEvent.java`:25, 211–219). **The word *deliberately* is an
  inference from the shape of the override; pass 9 should decide whether the
  book may say it.**
- `CustomBossEvents` is "the `SavedData` that holds them, one file at
  *data/minecraft/custom_boss_events.dat*", with capitalised NBT field names
  (`CustomBossEvents.java`:38; `CustomBossEvent.Packed.CODEC`).
- `ExecuteCommand.storeValue` is "a sibling of the score sink rather than the
  same code" — which **corrects** the parenthetical it replaces.
- `BossBarCommands` is "the write surface, at gamemaster"
  (`BossBarCommands.java`:57).

**`commands/entity-selectors` — a new section, *Two more argument types write
the same fork by hand*** (discharges a `pass3.md` §7 entry).

- `GameProfileArgument` "resolves to profiles, not entities"; an `@` "is
  rejected outright if it includes non-players"; the literal side is "read to
  the next space and looked up in the server's name-to-id cache — so `/ban`,
  `/whitelist` and `/op` name a player who has never joined this session"
  (`GameProfileArgument.java`:51–77; the five callers are `BanPlayerCommands`,
  `DeOpCommands`, `OpCommand`, `PardonCommand`, `WhitelistCommand`).
- "That lookup is the only thing on this page that leaves the game's own
  data." **An absolute over this page's scope; pass 9 should test it.**
- `ScoreHolderArgument`'s four literal branches "in order", the wildcard alone
  throwing (`ScoreHolderArgument.java`:102–170).
- "both enforce their single-or-many shape on the compiled selector rather
  than on the text".
- Elsewhere on the page: `EntityTypeTest` glossed as "the one-method 'is this
  the type I asked for, and give it to me typed' the whole entity-fetching API
  is generic over"; `Permissions.COMMANDS_ENTITY_SELECTORS` called "the **only
  permission in the game checked in two different phases**" (moved here from
  `commands/permissions`, where it was already asserted).

**`commands/brigadier-and-commands`.**

- A new paragraph on `SharedSuggestionProvider`: implemented by
  `CommandSourceStack` and `ClientSuggestionProvider`; "most of its 355 lines
  are static helpers"; `SharedSuggestionProvider.customSuggestion` "is the
  packet on the client and a completed empty future on the server"
  (`SharedSuggestionProvider.java`:32–50, and the two implementors).
- A new paragraph on `CommandSource`, restoring what pass-3 session N cut:
  four methods and four implementations; `RconConsoleSource.shouldInformAdmins`
  deferring to *broadcast-rcon-to-ops*; `BaseCommandBlock`'s source gated on
  `GameRules.SEND_COMMAND_FEEDBACK` and `GameRules.COMMAND_BLOCK_OUTPUT`,
  "which is what those two game rules *are*"; "a command block that has been
  broken accepts nothing at all" (the `closed` field);
  `CommandSource.NULL` refusing everything. Files:
  `CommandSource.java`:7–25, `RconConsoleSource.java`:44–56,
  `BaseCommandBlock.java`:202–214, `MinecraftServer.java`:1889–1899.
- **"The command block is `BaseCommandBlock` plus the `CommandBlockEntity`
  that holds one: a `CommandSource`, a stored string and a redstone edge, and
  no machinery of its own beyond this page's."** This is the sentence that
  pays off `blocks/README`'s promise; it is a *scope* claim as much as a fact.
- A new paragraph on the resource-argument family: six types "over the same
  idea", differing in what they hand back and "in whether they accept a glob.
  Only `ResourceSelectorArgument` does, which is why `/test run *` works and
  `/give @s *` does not." Also the five `commands/synchronization/brigadier`
  classes as "the only argument types in the game the game did not write".
- `WorldCoordinates` as "three `WorldCoordinate`s, each a value plus a *is
  this relative* flag".
- A sign's click command "is never checked by the client, because it never
  reaches the client at all" (the correction below).

**`commands/advancements` — a new section, *What the package holds that this
page does not name*.** The two family claims (thirty-five unnamed triggers;
the concrete predicates as instances of the four shapes) and
`CriterionProgress` as "a nullable timestamp, which is why the wire form can
carry progress without carrying a single condition"
(`CriterionProgress.java`:9). Also new: `TreeNodePosition` runs "in its
*apply* half — the half a reload runs on the main thread, once per root,
after the JSON has been read on a background one"
(`SimplePreparableReloadListener.java`:14–23,
`ServerAdvancementManager.java`:24, 36, 53).

**`commands/functions-and-macros`.** The macro variable-name rule stated in
prose for the first time — "inside `$(…)`, letters, digits and underscore and
nothing else" (`StringTemplate.java`:50–55) — and the claim that a dialog's
input keys obey the same rule. The caller list re-scoped (below).

**`commands/the-execution-engine`.** `ExecutionControl` as "the (context,
frame) pair with two methods … that pair is the whole privilege an action
has" (`ExecutionControl.java`:6–25). And the reconciliation the book lacked:
"the thread-local is null again the moment a queue drains, so two commands run
back to back each open their own context, which is why every function in
`#minecraft:tick` gets a budget of its own"
(`Commands.java`:406–410, `ServerFunctionManager.java`:58–84).

**`commands/permissions`.** `Permissions`' own nine, split "four to five"
(`Permissions.java`:7–15). And the second route to a client's op level:
"except on an integrated server, where
`IntegratedServer.updatePermissionAndChatAbilities` writes the host's own
`LocalPlayer` directly and no packet is involved"
(`IntegratedServer.java`:343–353).

**`commands/dialogs`.** The five dialog screens named as one family; the three
bootstraps (`DialogBodyTypes`, `InputControlTypes`, `ActionTypes`),
`StaticAction` and `DialogCommand` named.

**`commands/game-tests`.** `TestCommand` at "572 lines of subcommands";
`TestFinder` turning a subcommand's argument into `Registries.TEST_INSTANCE`
ids; "the glob in `/test run *` is `ResourceSelectorArgument`, the one
argument type in the game that takes one"
(`TestCommand.java`:296–299); `GameTestTicker` and `TestInstanceBlock` named.

**`commands/README` — a new *Where the part stops* section**, with three
family declines and one written-out omission: "three unrelated routines do not
make one lecture" (`SpreadPlayersCommand`, `CloneCommands`, `FillCommand`).
Its packages sentence now names all nine, and its *Reference this part uses*
paragraph re-scopes the traffic claim (below).

**`reference/glossary` — a new headword, *Boss bar*.**

**`src/lectures.md`** — Part XIII's dependency paragraph shortened to what is
about the order, and its Part VII clause re-scoped from "for advancements
alone" to advancements plus the selector's *predicate* option.

### Corrections

1. **`commands/scoreboard-and-data`** said "a score set and a crash a tick
   later is a score lost". A tick-loop crash is not that ending:
   `MinecraftServer.java`:877's *finally* runs `stopServer()` (:689), which
   calls `saveAllChunks` (:733), whose **first statement** is
   `this.scoreboard.storeToSaveDataIfDirty(…)` (:629). `how-a-server-dies`
   says so in as many words at its opening and in *What you lose if you kill
   the process*. Now: the watchdog kill, a *kill -9* or a power cut, with the
   link to that section.
2. **`commands/brigadier-and-commands`** listed a sign among the commands the
   client vets through `ClientPacketListener.sendUnattendedCommand`.
   `SignBlockEntity.executeClickCommandsIfPresent` calls
   `Commands.performPrefixedCommand` **on the server** with a source it builds
   itself at `LevelBasedPermissionSet.GAMEMASTER`
   (`SignBlockEntity.java`:201–247) — which `commands/permissions` already
   said. Now: a dialog button and a chat click event, with the sign named as
   the exception.
3. **`commands/permissions`' own figure** listed "a sign" in its entry node,
   four lines above prose saying a sign does not come that way. Same evidence;
   the node now reads "a dialog button, a chat click event".
4. **`commands/functions-and-macros`** said `ServerFunctionManager.tick` "is
   the **first** thing `MinecraftServer.tickChildren` does".
   `MinecraftServer.java`:1206–1213: the method first suspends packet flushing
   on every player, *then* opens the *commandFunctions* zone. `server-tick`'s
   order table has the suspension as row one. Now: "the first profiler zone …
   with only the suspension of every player's packet flushing ahead of it".
5. **`commands/dialogs`** called `WaitingForResponseScreen`'s button an
   "escape button" in one paragraph and a "Back button" in another. It is
   built from `CommonComponents.GUI_BACK`
   (`WaitingForResponseScreen.java`:14, 26). Now: Back, once.
6. **`foundations/resource-system`** said connected clients after a `/reload`
   "complete against the tree they were given until they reconnect". Both
   server-side parses read `MinecraftServer.getCommands`
   (`MinecraftServer.java`:1854–1856 → `this.resources.managers.getCommands()`;
   `ServerGamePacketListenerImpl.java`:610 for suggestions), so a newly added
   function *does* complete after a reload — which
   `commands/brigadier-and-commands` says and this page contradicted. Now: it
   is the tree's *shape* that goes stale, with the link.
7. **`items/contexts-and-predicates`** said Part XIII's commands "own
   `/execute if predicate`". No page in Part XIII mentions it; that page owns
   its own trace of it. Now: the page owns the command, Part XIII owns the
   engine it runs in and the selector option that is the second caller.
8. **`commands/brigadier-and-commands`**' door table routed `LootCommand` and
   `ItemCommands` to `loot-tables`, which names neither;
   `contexts-and-predicates`:247–248 names both. Repointed, with
   `loot-tables` kept for the functions themselves. *(pass5.md:3349,
   session G)*
9. **`foundations/data-driven-types`** routed `BuiltInRegistries.PERMISSION_TYPE`
   and `PERMISSION_CHECK_TYPE` to `brigadier-and-commands`, which names
   neither identifier; `commands/permissions` owns both. Repointed with
   anchors. *(the last live row of pass5.md:424)*
10. **`commands/brigadier-and-commands`** said `net/minecraft/server/commands`
    is "a hundred classes and 12,800 lines" where the landing page and the
    atlas say 102. Both count files; 102 is the generated number, and the
    package has a `data/` subpackage that a flat `ls` misses. Now: "102 files",
    naming the atlas as the population.
11. **`commands/README`** said the part's traffic "is almost all server →
    client". Its own `game-tests` page names two serverbound packets and
    `advancements` a third, besides the two command packets. Now: the two
    reporting systems are one-way and everything a player does comes back.
12. **`commands/functions-and-macros`** called its caller list "short and
    exhaustive" while omitting `execute if function` and `/return run
    function`, both of which the engine page explains. Now: named, with the
    link.
13. **`commands/functions-and-macros`** cited `items/enchantments` for
    `RunFunction`, which that page never names. Now: `RunFunction` is named
    here as one of the `EnchantmentEntityEffect`s, with the link pointing at
    the section that explains the effect families.

### Suspicions re-derived and found sound

- `commands/permissions`' "ninety-one gates that name a level constant,
  sixty-six … sixteen … nine" against the same page's 95
  `Commands.hasPermission` call sites. Both right: the arguments to those 95
  calls are 66 gamemaster, 16 admin, 9 owner, two ternaries in `SeedCommand`
  and `VersionCommand`, `GameModeCommand.PERMISSION_CHECK` and
  `ClientPacketListener.RESTRICTED_COMMAND_CHECK`. **For pass 8:** whether the
  two ternary gates "name a level constant" is left to the reader, and they do.
- `commands/advancements`' "its only users are the six component predicates in
  `core/component/predicates`". Exactly six of that package's classes
  reference `CollectionPredicate`.
- `commands/dialogs`' "thirty-one classes across four packages" — 35 files
  less four `package-info.java`. Sound.
- `commands/game-tests`' "forty-four classes" for `gametest/framework` — 45
  files less one `package-info.java`. Sound. The 47 on
  `anatomy/what-this-book-skips` is the atlas's file convention over the whole
  `gametest` tree, not a disagreement. **For pass 8** (the two rules for the
  word *classes*), not a correction.
- `commands/game-tests`' `/test run *`. `TestCommand` registers `run`,
  `runmultiple`, `runfailed`, `runthat`, `runthese` and `runclosest`; there is
  no `runall`, and `run` takes a `ResourceSelectorArgument`.
- `commands/permissions`' "three sources of belief". Sound as a taxonomy; the
  integrated server's direct write is a second route into the first source,
  and is now a clause rather than a fourth entry.

### For pass 9's attention, found and not fixed

- `commands/brigadier-and-commands` says the client's dispatcher is built
  "from a tree the server sent you when you joined" and later that the tree's
  only sender is `PlayerList.sendPlayerPermissionLevel`. Both were checked in
  pass 4; the join path reaching that method was not re-derived here.
- `commands/scoreboard-and-data`'s *Where to look* calls
  `NbtPathArgument.NbtPath` "the nicest ten lines in the area", and
  `commands/functions-and-macros` no longer says "three lines apart" — both
  are line-level claims about decompiled formatting, which is not the
  source's. The second is retired; the first is not, and is rule 2's problem
  rather than a fact.
- Two class-name collisions the book does not acknowledge:
  `EntityDataAccessor` (`DataCommands`' accessor against the syncher key on
  `entities/synched-entity-data`) and `EntitySelector` (the compiled query
  against the predicate bag in `world/entity`, two pages apart in this part).
  `commands/entity-selectors` names the second in *Where to look*; nothing
  names the first. The verifier lists both among its 25 ambiguous names.
- `commands/scoreboard-and-data` is linked from `foundations/data-driven-types`
  for `BuiltInRegistries.NUMBER_FORMAT_TYPE` and names `NumberFormatTypes` but
  not `NumberFormatType`; the page states the three kinds without stating the
  pattern. Left as it stands.


## Pass 5, session L — Part XII · World generation *(2026-09-07)*

*All ten system pages, the landing page and `reference/density-function-nodes`
rewritten; eleven pages in six other parts edited. Twelve reader agents, one
per page; every finding acted on was re-derived by reading both pages, and
every fact below was changed with the decompile open.*

### Corrections

- `worldgen/terrain`:231–233 said the carvers' lava level "is a constant in the
  generator, not a data-pack field", **and the same page's own carve-state
  paragraph at :210 called it *configured***. `CarverConfiguration.lavaLevel`
  is a `VerticalAnchor` field on the configured carver
  (`world/level/levelgen/carver/CarverConfiguration.java`:35, read at
  `WorldCarver.java`:153). All four shipped configured carvers set it to
  *above_bottom: 8* (`data/minecraft/worldgen/configured_carver/*.json`), which
  is why it does not move with the sea level — it is anchored to the world's
  bottom, not below its sea. The answer is rewritten to say that; :210 now
  names the field.
- `worldgen/terrain`:41–43 said `NoiseBasedChunkGenerator` "overrides
  [`createBiomes`] only to use the chunk's cached sampler". The override
  (`NoiseBasedChunkGenerator.java`:85–99) forks *and* builds the chunk's
  `NoiseChunk` *and* wraps the biome resolver in `Blender` and
  `BelowZeroRetrogen`. The whole fork inventory was Part IV's and is now a
  citation; the three jobs are stated on `worldgen/biomes` instead.
- `worldgen/biomes`:75 said "Only the noise generator does the above", where
  "the above" includes the *init_biomes* fork drawn in the figure directly
  over it. The base `ChunkGenerator.createBiomes`
  (`ChunkGenerator.java`:121–126) forks for every generator; the override is
  about the three lines below the fork. Rewritten, and it now agrees with
  `terrain`.
- `worldgen/density-functions`:17–18 called `DensityFunctions` "the library of
  thirty-four node types you build one out of". Thirty-four is a count of
  registered **ids** (`DensityFunctions.bootstrap`), not of classes: six ids
  are one `DensityFunctions.Marker`, seven are one `DensityFunctions.Mapped`,
  and *old_blended_noise* is `BlendedNoise`, which is not a `DensityFunctions`
  member (`DensityFunctions.java`:56). Rewritten.
- `worldgen/density-functions`'s *The six caches, and the three a single point
  may use* named **two** single-point-safe classes in a section whose heading
  promises three, and never named the sixth cache at all. The third is
  `NoiseChunk.BlendDensity` (`NoiseChunk.java`:892–922), which tests no context
  and answers from anywhere. Written in, with what it is.
- `worldgen/blending`:320–322 said "Height and biome are **averaged** over
  every measured column", where the page's own :260–268 says the biome answer
  "is not a blend" and :328 calls it a threshold. Rewritten: both are drawn
  from the same map at the same radius, the height averaged over it and the
  biome taken from the nearest entry in it.
- `worldgen/hand-built-structures`:90 called `MineshaftStructure`'s pre-filled
  builder "the only *Either.right* in the game". `Either.right` is an everyday
  idiom across the corpus; what is unique is the right branch of
  `Structure.GenerationStub`'s own `Either` (`Structure.java`:250–253 — every
  other construction takes the left). Rescoped.
- `worldgen/structure-placement`:131 said "almost every later step in the
  generation pyramid requires structure starts within eight", against
  `terrain`'s "six of the generation steps". Six of the twelve, and they are
  contiguous: `ChunkPyramid.GENERATION_PYRAMID` declares
  `addRequirement(ChunkStatus.STRUCTURE_STARTS, 8)` on *STRUCTURE_REFERENCES*
  through *FEATURES* and nowhere else. Rewritten as that range.
- `worldgen/README`:14 said "the surface pass reads its neighbours' biomes" as
  an example of generation reading the world. The pass that reads a
  *neighbourhood* is the carvers (17×17 source chunks, `terrain`:191–197);
  `SurfaceSystem.buildSurface` reads one biome per column, through
  `biomeManager::getBiome` (`SurfaceSystem.java`:103, 114). Replaced with the
  carvers.
- `worldgen/biomes`' two-borders table listed the jittered read's users without
  world generation. The surface rules read the biome through
  `BiomeManager.getBiome`, the jittered entry point (`SurfaceSystem.java`:103).
  The row gains the surface pass, and `terrain` now states which read it is.
- `world/scheduled-ticks`:13 offered "a sapling sprouting after bonemeal" as an
  example of a scheduled tick. `SaplingBlock.performBonemeal` calls
  `SaplingBlock.advanceTree` in the same call (`SaplingBlock.java`:81–82) and
  the un-bonemealed path is a *random* tick (:48) — the page's own contrast.
  The same list's "a piece of amethyst budding" is also a random tick
  (`BuddingAmethystBlock.java`:28). Replaced with a dispenser firing
  (`DispenserBlock.java`:138) and a redstone torch burning out.
- `worldgen/README`:170 said the level-data Reference page is "which lecture
  nine links to"; the page that links it is lecture **ten**,
  `creating-a-world`.
- `worldgen/README` and `src/lectures.md` disagreed about how many statuses lie
  between a structure being decided and its blocks being written — three
  against four, from unstated baselines. Both now count from named statuses:
  decided at `ChunkStatus.STRUCTURE_STARTS`, written at
  `ChunkStatus.FEATURES`, three statuses after the noise fill.
- `foundations/data-driven-types`:190 said the trace on
  `features-and-placement` "walks a tree through all" nine feature sub-object
  rows; five of the nine carry *trees* in their own *taught in* column and the
  trace walks none of them. Split between the two pages.
- `blocks/README`:34 handed "the command and structure blocks" to Part XIII,
  which names neither. Split: the structure block to
  `jigsaw-and-templates#where-a-template-comes-from` (written this session),
  the command block left to Part XIII.
- `reference/density-function-nodes`' deck advertised two of the page's four
  sections; `reference/README`:56 and `worldgen/README`:160 copied the same
  omission. All three corrected.

### Suspicions re-derived and found sound (no change)

- `worldgen/blending`:47 "the scan runs on the background executor" — correct.
  `IOWorker.createOldDataForRegion` submits to `Util.backgroundExecutor()`
  (`IOWorker.java`:98–126) and joins `scanChunk` from inside it; the IO lane is
  underneath, not the submitting pool.
- `worldgen/README`:12 "the decoration step reads block states, heights and the
  carving mask through `PlacementContext`" — correct, and the class was named
  on no page. `PlacementContext` has `getBlockState`, `getHeight`,
  `getCarvingMask` and `topFeature`, and extends `WorldGenerationContext`.
  Named on `features-and-placement` this session.
- `features-and-placement`:222 "a structure and a feature at the same index in
  the same step draw the *same* feature seed" — correct.
  `WorldgenRandom.setFeatureSeed` is *seed + index + 10000 × step*
  (`WorldgenRandom.java`:59–63) with no structure/feature discriminator, and
  `ChunkGenerator.applyBiomeDecoration` restarts the index at zero for each
  half (`ChunkGenerator.java`:356, 415).
- `jigsaw-and-templates`:156 "never structure void, which
  `JigsawReplacementProcessor` handles instead" — correct as far as it went,
  and now stated more precisely: structure void never reaches a template,
  because `StructureBlockEntity` excludes it when it saves
  (`StructureBlockEntity.java`:380).
- `hand-built-structures`:206 "the forty shipped processor lists between them
  use four types" — correct. Forty files under
  *data/minecraft/worldgen/processor_list/*, using rule (35), protected blocks
  (7), block rot (6) and capped (4). Moved to `jigsaw-and-templates` with the
  counts and the two class names the corpus lacked.
- `trees`' "thirty-nine configured tree features" against
  `what-this-book-skips`' "50 tree kits" — both correct, different
  populations: 39 shipped *configured_feature* files of type *minecraft:tree*,
  50 `ResourceKey<ConfiguredFeature>` constants on `TreeFeatures`. `trees` now
  says which it counts and why the other number exists.

### Claims introduced

**`worldgen/density-functions`** — the fifteen router functions partition
6 climate / 5 aquifer (its four noises plus *preliminary_surface_level*, which
`Aquifer.NoiseBasedAquifer` samples per column) / 3 ore veins / 1 final
density; `PerlinSimplexNoise`'s only three instances are `Biome`'s fixed-seed
temperature noises; `SimplexNoise` is the End islands node's;
`NoiseUtils.biasTowardsExtreme` has no callers, making it the fourth dead
thing in the Q&A; all six installed classes carry `DensityFunction.fillArray`
and `CacheOnce` keeps a second counter for it; the beardifier splice's
consequence ("every noise dimension is beardified whether or not its router
JSON mentions one") moved here from `terrain`.

**`reference/density-function-nodes`** — *Bounds* rewritten from 36 lines of
prose to an eight-row table plus one paragraph; the three wrap singletons
became a table; two unregistered `DensityFunctions` members named as absent
from the catalogue; the deck rewritten to admit four sections.

**`worldgen/terrain`** — the aquifer reads five router functions, named; the
surface rule tree is two registries of dispatched types
(`SurfaceRules.RuleSource`, `SurfaceRules.ConditionSource`) and branches on
the *jittered* biome read; `CaveWorldCarver`, `CanyonWorldCarver`,
`CaveCarverConfiguration`, `CanyonCarverConfiguration` and
`CarverDebugSettings` named; ore veins contrasted with `OreFeature`; the
noise fill "holds every section across its noise range" (cited to
`chunk-anatomy`).

**`worldgen/biomes`** — `BiomeSources.bootstrap` registers four sources, all
four named with what each is for; `BiomeResolver` named as the interface;
`MultiNoiseBiomeSourceParameterList` and `MultiNoiseBiomeSourceParameterLists`
named, two presets; `FillBiomeCommand` named; the probe's Gaussian pass is
unconditional and the server passes no interpolator (moved to
`world/environment-attributes-and-timelines`); the box blur moved to
`client/the-client-level`; `BiomeColors` reaches the effects through four
`ColorResolver`s with no probe in the path.

**`worldgen/blending`** — the *For a 1.21-era reader* box moved to
`reference/naming-drift`'s Part IV table as a row; the three counts (five
consumers, four answers, three questions) reconciled in one clause.

**`worldgen/features-and-placement`** — `PlacementContext` and
`FeaturePlaceContext` named and what each carries; the fourth value-type rung
(`BlockStateProvider`) added, with registered counts 14 / 6 / 8 for the
predicate, height and state families; `SurfaceRelativeThresholdFilter` named as
the fifteenth modifier; `PlacementFilter` defined over the chain's four
filters; `FeatureCountTracker` behind `SharedConstants.DEBUG_FEATURE_COUNT`;
*/place feature* named as the third door into `Feature.place`; the
sixty-three-algorithm tail declined in writing; `Feature.NO_OP` separated from
the five selectors.

**`worldgen/jigsaw-and-templates`** — §7's three unnamed `JigsawStructure`
fields written, with the shipped-data census: six structures set the expansion
hack (five villages and the pillager outpost) and **exactly one** — trial
chambers — sets either `DimensionPadding` (10) or `LiquidSettings`
(*ignore_waterlogging*), and no shipped pool element overrides the latter;
`JigsawStructure.MaxDistance` and `JigsawStructure.MAX_TOTAL_STRUCTURE_RANGE`
explained as the free-space box and its load-time validation; the processors
given their own section with the forty-list census, `ProtectedBlockProcessor`,
`CappedProcessor`, `RuleTest`, `PosRuleTest` and `RuleBlockEntityModifier`; the
three `TemplateSource`s and `TemplatePathFactory` written as *Where a template
comes from*, with the first-source-wins rule; the **structure block** taken
(save mode excludes structure void, load mode builds a `StructurePlaceSettings`
with a `BlockRotProcessor` for integrity); `PoolAliasBindings`' three kinds;
the debug flag named.

**`worldgen/structure-placement`** — `StructurePlacement.getLocatePos` moved in
from `hand-built-structures` as its own Q&A; the presence cache split into its
own section, with the second feed (`ChunkStatusTasks.loadStructureStarts`)
named; the per-chunk write split into its own section; `StructureType` and
`StructurePlacementType` named; the figure's five boxes and the heading's count
reconciled.

**`worldgen/hand-built-structures`** — the `*Structure` wrapper family named as
settings wrappers, with `RuinedPortalStructure`'s five decay setups and
`DesertPyramidStructure.afterPlace`'s five-to-seven suspicious sand;
`BuriedTreasurePieces` given a row in the four-families table;
`WoodlandMansionPieces`' double membership explained; `StructurePieceType`
named in the cast; "chunk workers" settled to the worldgen executor.

**`worldgen/trees`** — the thirty-nine/fifty count scoped; the five registry
type classes named; two counted headings renamed (*The trunk placers*, *The
foliage placers*) so a release cannot break an anchor; the decorator heading
corrected — the leaf pass does not undo the decorators, it is blocked by them.

**`worldgen/creating-a-world`** — the stage list cut to a citation and the
*consequence* kept; `FlatLayerInfo` and `FixedBiomeSource` named;
`WorldOpenFlows.openWorld` given its own section, with `ChunkGenerator.validate`
identified as one of its eight links; *Optimize World* pointed at
`chunk-storage` rather than left with the declined half.

**`worldgen/README`** — the size sentence is the include, with two boundary
corrections (`PatrolSpawner`/`PhantomSpawner`, the Xoroshiro sources); the
order argument made once instead of three times; the closer rewritten as an
instruction; a *Where the part stops* section with the coverage answer — a
quarter of the part's lines are one shape, an algorithm that writes blocks and
adds no mechanism, and the head of each family is named; the verified line
rewritten off lecture one's hook; the pass-number sentence cut.

### For pass 9's attention, found and not fixed

- `worldgen/blending`:162 says `BlendingData.pack` "omits the heights entirely
  if none of them was ever measured", thirty lines after saying the codec
  "validates the saved height array against" sixteen slots. Consistent only if
  the field is optional; neither sentence says so.
- `worldgen/jigsaw-and-templates` states 188 shipped pool files; the other two
  data censuses on the part's structure pages (34 structure files, 40 processor
  lists) were re-derived this session and this one was not.
- `worldgen/creating-a-world`:280 hand-counts nineteen classes in
  `client/gui/screens/worldselection`, which nothing regenerates.
- `worldgen/biomes`:32's attribute counts ("twenty gameplay attributes … the
  sixty-six vanilla biome files touch three … fifty-one touch none") against
  `world/environment-attributes-and-timelines`:80 ("eleven attributes across
  sixty-six biome files, with *visual/sky_color* in fifty-six of them"). The
  two are reconcilable only under a silent *gameplay* scoping that neither
  states. Both are data-pack censuses; pass 9 re-derives.
- `worldgen/creating-a-world`:285 reaches a `LevelSummary` through
  `LevelStorageSource.readLightweightData`, `reference/level-data-and-rules`:92
  through `LevelStorageSource.readLevelSummary`, and
  `server/starting-a-server`:156 through
  `LevelStorageSource.LevelStorageAccess.fixAndGetSummaryFromTag`. Probably one
  chain; the book does not say.

## Pass 5, session K — Part XI · Rendering *(2026-09-06)*

*Thirteen reader-of-the-book agents — one per page, the landing page and
`reference/submit-phases` — and one whole-part read in watching order. Every
finding acted on was re-derived against `reference/26.2` by the session
itself. Corrections first, then the claims the session introduced, which pass
9 checks before anything else.*

### Corrections — what the page said, what the decompile says

1. **`rendering/entity-rendering`:97** said "Visibility is **two tests in two
   places**. The frustum test is `EntityRenderer.shouldRender`". That method
   runs *two* tests, in order: `Entity.shouldRender(camX, camY, camZ)`, a
   distance test scaled by the entity's bounding box, and only then
   `Frustum.isVisible` (`EntityRenderer.java`:66–78). `block-entity-rendering`
   :162 had it right and the entity page had it half right, so the sibling
   taught the entity rule better than the entity page. Now **three tests in
   two places**, with the distance half stated.
2. **`rendering/post-processing`:12** said "every chain this game will ever
   load is named by a constant in Java, and there are only six of those",
   while its own :251 said three of the six are "built inside
   `GameRenderer.checkEntityPostEffect`". Three are `static final` fields
   (`LevelRenderer.java`:99–100, `GameRenderer.java`:92); the other three are
   inline `Identifier.withDefaultNamespace` literals in a switch
   (`GameRenderer.java`:213–223). The page contradicted itself; the claim it
   wants — the set of ids is closed and written in Java — survives, and now
   says three constants and three literals.
3. **`reference/submit-phases`:64** said a quad-particle group is submitted
   **once** and lands in two phases. `SubmitNodeCollection.submitQuadParticleGroup`
   (`SubmitNodeCollection.java`:250–253) builds **two** separate
   `QuadParticleFeatureRenderer.Submit` records, one into `solid` and one into
   `afterTerrain`. `particles`:287 said twice and was right; the Reference page
   said once and was wrong. Now "reaches the collector in one call and becomes
   two nodes".
4. **`rendering/the-window`:197** said "An atlas is assembled into one with
   `NativeImage.copyRect`, `NativeImage.resizeSubRectTo` and
   `NativeImage.fillRect`". None of the three assembles an atlas.
   `copyRect`/`fillRect` are used by `Unstitcher` (a sprite *source*, before
   any stitch), `CubeMapTexture` and `SkinTextureDownloader`;
   `resizeSubRectTo` has exactly one caller in the game,
   `GameRenderer.java`:512, the world-icon downscale. The atlas is assembled
   on the GPU, which `models-and-atlases`:219 already said. Rewritten to what
   the methods do, with a sentence saying what an atlas is *not*.
5. **`rendering/visibility-and-the-frame-graph`:61** said
   `LevelExtractor.applyFrustum` "is the last thing *extract* does".
   `LevelExtractor.extract` (`LevelExtractor.java`:96–141) runs it near the
   *top*, right after `prepareDispatchers`, and everything after it —
   entities, block entities, dirty sections — reads the list it just filled.
   Three other pages depend on that order. Rewritten to "runs near the top of
   extract", and the consequence stated as the finding it is.
6. **`rendering/models-and-atlases`:298** said the display block-model table
   is used by "item frames, **block entities** and ten entity renderers". No
   block-entity renderer reads it. `BlockModelResolver` reaches the
   block-entity side only as a field of `BlockEntityRendererProvider.Context`
   (`BlockEntityRenderDispatcher.java`:102), which nothing under
   `renderer/blockentity` or `renderer/special` calls. Eleven entity
   renderers read it and nothing else does. The sentence is cut (the table is
   now `block-entity-rendering`'s) and the owner states the `Context` fact.
7. **`rendering/lightmap-fog-and-sky`:324** said "the weather reads neither
   clock nor attribute, seeding each column from its own coordinates" — while
   the same page's opening (:15) said the rain's texture scrolls off the raw
   world clock. `WeatherEffectRenderer` passes `level.getGameTime()` into both
   `createRainColumnInstance` and `createSnowColumnInstance`
   (`WeatherEffectRenderer.java`:93–95), and the snow's `vOffset` is
   built from `ticks & 511L` (:236). The *seed* is coordinates, the *scroll*
   is the clock. The page was contradicting itself and the closing sentence
   was the wrong half.
8. **`rendering/the-window`:36** said "All of it lives in
   *com/mojang/blaze3d/platform*" of a cast table whose first two rows are
   `Minecraft` (`net/minecraft/client`) and `GpuBackend`
   (`com/mojang/blaze3d/systems`). Now "every row but the first two".
9. **`rendering/the-window`:244** claimed the *rest of the package* and
   omitted seven of the twenty-five classes in it, `TextureUtil` (288 lines)
   the largest. Five of the seven are pipeline state and belong to
   `blaze3d`; the sentence now says so and `TextureUtil` is explained.
10. **`rendering/the-frame`:78** described the *update window* zone as
    "reconfigures the surface if it needs it and then calls
    `GpuSurface.acquireNextTexture`". `Minecraft.java`:1341–1342 opens the zone
    with `Window.updateFullscreenIfChanged`, which `the-window`:166 states and
    `the-frame` omitted. The zone now has three statements and the first is
    cited to its owner.
11. **`reference/naming-drift`:396** said the frame "builds an immutable
    render state **on the game thread**". Both halves run on the Render thread
    (`Minecraft.renderFrame`), and the glossary already retired *immutable*
    for the top-level states. Reworded to "copies the live game into render
    state and then draws from that copy, both halves on the Render thread".
12. **`world/lighting`:354** cited `section-meshing#a-click-and-the-flag-it-leaves-behind`
    for the `hasAllNeighbors` light gate, which is two sections later under
    *The sweep that only looks at what you can see*. The anchor existed, so
    `check_links.py` passed it; repointed.
13. **`rendering/section-meshing`:282** said *BlockRenderDispatcher* is
    "gone", while `reference/naming-drift`:302 gives `ModelBlockRenderer` as
    its successor. Both are true of different things; the drift box now says
    the name is gone and `ModelBlockRenderer` does the tesselating, and
    `BlockAndTintGetter.getShade` is separated out as the one with no
    successor at all.
14. **`reference/submit-phases`:31** said three phases are a
    `TranslucentFeatureRenderPhase` without saying which. They are rows 4, 7
    and 8 — `seeThroughNameTags`, `translucentBlocksAndItems`,
    `translucentModels` (`SubmitNodeCollection.java`:55–69) — and not the ones
    the names suggest. The count was an unenumerated assertion on a page whose
    whole job is enumeration.

### Suspicions re-derived and found sound — a strike is a claim

- `post-processing`:239, the F3 pie chart. The camera-entity chain runs in
  `GameRenderer.render` *after* `renderLevel` has returned
  (`GameRenderer.java`:443–449), so it is inside the *world* zone but outside
  all five of `renderLevel`'s sub-zones, *screenEffects* included. Both pages
  were right and neither needed changing.
- `the-frame`:137, `TickRateManager.isEntityFrozen` "excludes anything with a
  player aboard", against `block-entity-rendering`:263, "never freezes a
  `Player`". `TickRateManager.java`:73 excludes both, and each page states the
  half its own scenario needs. No contradiction.
- `the-window`:221, the error callback "swapped three times over the game's
  life". True as a lifecycle statement (`Window.java`:312, 335, 346); the
  scoped swaps are a fourth *kind*, now written as such rather than as a
  correction to the count.
- `the-window`:256, "*ScreenManager*, which never existed here", against
  `naming-drift`:312. Left: rule 3 makes the page a claim about 26.2, and the
  drift row is a claim about where a 1.21 reader should look. Logged for pass
  9 rather than settled here.

### Claims introduced

**Ownership moves, each stated once and cited everywhere else.**

- The **merging rule** moved from `reference/submit-phases`:31–44 to
  `entity-rendering`'s *prepare* section, with the two phase classes, the
  batch-key explanation, `RenderTypeFeatureRenderer.Group` and
  `RenderType.canConsolidateConsecutiveGeometry` moving with it. The Reference
  page keeps the 12:3 split, now enumerated, and a link.
- The **two baked block-model tables** settled to `block-entity-rendering`
  (its scenario, its figure); `models-and-atlases` keeps the `BlockModel`
  naming trap and a link.
- The **`prepareSharedState` handshake** cut to a citation of
  `resource-system#the-shared-state-channel`; `models-and-atlases` keeps only
  which end of it it is (thirteen published, two awaited).
- **Directional shading and `CardinalLighting`** moved off `visibility` onto
  `lightmap-fog-and-sky`'s *What is not an attribute*.
- **The compile ordering** (`compileSections` after `FrameGraphBuilder.execute`)
  split: `visibility` keeps where the call sits, `section-meshing` keeps what
  it costs, each citing the other.
- **The wall** cut on `visibility` to one sentence and an anchor into
  `the-frame`.
- **The frame cap** cut on `the-frame` and `the-window` to citations of
  `the-client-loop`, which receives the *iconified, not unfocused* distinction.
- **`ClientShutdownWatchdog`** cut on `the-window` to the one arming it owns;
  `the-client-loop` receives the fifteen-second sleep, the daemon thread and
  the report-only-versus-halt difference.
- **The minimised-window answer** won by `the-frame`; `the-window` cut to
  `Window.isMinimized` plus the anchor.
- **The backend-choice answer** won by `the-window` — its figure draws the
  retry loop — and it receives the ordered pair, `GlBackend`/`VulkanBackend`,
  the OpenGL-first default and the unclean-shutdown double downgrade from
  `blaze3d`, which keeps one sentence.
- **The static-pipeline precompile** and **the two-stage GLSL preprocessing**
  won by `blaze3d`, which receives the reload phase, the thread and the
  all-or-nothing cache swap; `post-processing` cut to citations.
- **The *Globals* block's seven members** moved to `blaze3d` and enumerated
  from `GlobalSettingsUniform.UBO_SIZE`; `post-processing` keeps the
  consequence.
- **`CrossFrameResourcePool`'s three-frame hold** moved off the part's last
  page onto `visibility`, beside `createInternal`.
- **The frame-graph inspector** moved from `post-processing` onto `visibility`,
  which owns `FrameGraphBuilder.execute`; `post-processing` keeps the contrast.
- **The spectator-chain answer** won by `post-processing`; `the-frame` cut to
  one clause and an anchor. **The UI lightmap** won by `lightmap-fog-and-sky`,
  which receives the `levelLightmap`/`uiLightmap` pair; `the-frame`'s Q&A cut
  to the answer and a link.
- **The hand's second submit storage** won by `the-frame`, which now names
  `ItemInHandRenderer` and `ScreenEffectRenderer` and pays off the hand-forward
  `entity-rendering`:293 had been making to it; `block-entity-rendering` cut to
  a citation. **The six partial ticks** stay `the-frame`'s and
  `block-entity-rendering` keeps only its own difference, which is the declared
  pair's business.

**Coverage written.**

- `models-and-atlases`: the three branching item models and **thirty-three
  properties in three registries** (10 numeric, 10 select, 13 conditional),
  `NeedleDirectionHelper`'s per-stack damped compass needle and its
  *wobble: false* opt-out, `LocalTime`'s once-a-second re-read, and
  `DisplayContext`. This discharges `what-this-book-skips`' promise that the
  `client/renderer/item` properties subtree is covered as a section here.
- `models-and-atlases`: the chunk-layer decision made exact — `Transparency`
  is two booleans and `ChunkSectionLayer.byTransparency` reads them
  translucent-first — with `Sheets` named as where the item render type comes
  from.
- `block-entity-rendering`: `BlockModelRenderState` as why one entry holds
  quads *and* a renderer; the built-in table's four other model kinds
  (`EmptyBlockModel`, `SelectBlockModel`, `ConditionalBlockModel`,
  `CompositeBlockModel`) and the **five bare wrappers** — bell, conduit, end
  gateway, end portal, and the enchanting table, whose built-in model is a
  book with no table under it; `WallAndGroundTransformations`;
  `BlockEntityWithBoundingBoxRenderer`'s `Player.canUseGameMasterBlocks` gate;
  and the crumbling overlay's one construction site, with
  `BlockDestructionProgress` ordering on stage before digger id.
- `entity-rendering`: `EntityRenderers` and `EntityRendererProvider` as where
  a shared renderer comes from; `DisplayRenderer`; and **the skin pipeline's
  drawing half**, which pays off `player-anatomy`:118's "Drawing any of it is
  Part XI's" — `AvatarRenderState` carries the whole `PlayerSkin` by value and
  seven booleans, one per `PlayerModelPart`, while `PlayerModelType` never
  reaches the state because the dispatcher used it to pick the renderer.
- `the-window`: `TextureUtil`'s two pre-mipmap repairs (`TextureUtil.solidify`,
  `TextureUtil.fillEmptyAreasWithDarkColor`) and why they exist;
  `GLFWErrorScope` and `GLFWErrorCapture` as the scoped fourth kind of callback
  swap and the four places that use them.
- `lightmap-fog-and-sky`: `Lighting` — one UBO, five `Lighting.Entry` slices,
  four written once in the constructor and only `LEVEL` rewritten — and
  `WorldBorderRenderer` as the second thing in the weather pass.
- `visibility-and-the-frame-graph`: `ChunkSectionLayerGroup` as
  SOLID-and-CUTOUT against TRANSLUCENT; `ViewArea` as a
  `RotatingSectionStorage` of `RenderSection`s, the same ring the dirty flags
  use; and `TranslucencyPointOfView` as three integers clamped to minus one,
  zero or plus one — **twenty-seven possible values** — with
  `TranslucencyPointOfView.isAxisAligned` reading zero on any axis.
- `section-meshing`: `ModelBlockRenderer.tesselateBlock` and `BlockQuadOutput`
  as how a model becomes quads, and `ModelBlockRenderer.forceOpaque` as which
  of the compiler's two callbacks a leaf block gets.
- `blaze3d`: `GlTransientMemory`/`VulkanTransientMemory` and
  `GlConst`/`VulkanConst`; and the homeless pass-3 cut
  `RenderSystem.outputColorTextureOverride` /
  `RenderSystem.outputDepthTextureOverride`, written as the one thing that
  redirects where a draw lands, with the GUI item atlas and picture-in-picture
  as its only setters.
- `particles`: the eighty-odd `Particle` subclasses as a family, with
  `ParticleProvider` in the cast, `DripParticle` and `FireworkParticles` named
  as nests of variants, and `ParticleOptions` written — which pays off
  `data-driven-types`:186's hand-forward.
- `the-frame`: `TimerQuery` as the GPU stopwatch that brackets the frame and is
  only restarted once the last one has been collected.

**The landing page**, rewritten to the role. Its argument is now stated:
*the renderer is not allowed to look at the world*, and every seam a player
notices is a disagreement about which copy something got. Its size sentence is
the generated include over the mapping's four packages (1,254 / 93,012)
instead of a hand count of three (1,179 / 87,000). The ten-line caption
disowning its own figure is four lines, and the contradiction between "in the
order things happen inside one frame" and "the pipeline arrows are not frame
order" is resolved in favour of the second, with `lectures.md` re-synced to
match. Its coverage answer is the part's boundary stated twice — packages
other parts own that count against Part XI, and `client/resources/model`,
which counts against Part X and is this part's subject.

### Rulings made in writing

- **The `map_source.py` `PARTS` change is declined** (queue pass5.md:3499).
  `client/resources/model` is billed to Part X and is `models-and-atlases`'
  subject; moving it would change both parts' generated totals and invalidate
  the coverage argument session J had just written into Part X's landing page.
  The mapping is by package, the package is genuinely shared, and both landing
  pages now say so in prose. No page moves, no tool changes.
- **The *what a player sees* column stays** on `post-processing`, with a
  sentence above the table saying it is a reading of the shaders rather than a
  citation, and the *transparency* row reworded because it was the one cell
  doing a different job.
- **`the-window` is not cut.** The pass-2 suggestion that the whole page might
  go is overtaken: the landing page now argues its place, and three pages open
  on state it creates.
- **`particles`' explosion section is not cut.** It is the book's only home for
  the client explosion budget.

### For pass 9's attention, found and not fixed

- `blaze3d`:206 names `StagedVertexBuffer` in the chunk-meshing staging chain;
  `the-frame`:167 and `submit-phases`:77 describe it as the feature and GUI
  buffer. One of the three is describing the wrong buffer.
- `models-and-atlases`' "**twelve** separate layers" of soft failure, where the
  prose enumerates eleven. Third pass to record it; it is a count assertion, so
  it is pass 9's rather than pass 8's.
- `entity-rendering`:191 and :257 — the pose-copy split and "half a dozen
  others" are both stated as if exhaustive and are not (pass5.md:823).
- `section-meshing`'s "the pool plus one" ceiling conflates concurrent compiles
  with existing meshes.
- `resource-system`:242 names `ParticleResources` as a second consumer of
  `AtlasManager.PENDING_STITCH`; `models-and-atlases`' figure shows one.

## Pass 5, session J — Part X · The client *(2026-09-06)*

*Twelve reader-of-the-book agents, one per page plus the landing page, and
one whole-part read in watching order. Every finding acted on was re-derived
against `reference/26.2` by the session itself. Corrections first, then the
claims the session introduced, which pass 9 checks before anything else.*

### Corrections — what the page said, what the decompile says

1. **`client/the-client-level`:129** said the renderer is reached directly by
   "the chunk cache and **one** packet handler". `ClientPacketListener` has
   five references to `Minecraft.levelExtractor`
   (`ClientPacketListener.java`:538, 550, 940, 1329, 2677): two hand it to a
   `ClientLevel` constructor, and **three** are calls on it —
   `handleChunksBiomes` marking sections dirty (:940), `handleLogin`
   refreshing the debug renderer list (:550) and `handleGameTestHighlightPos`
   (:2677). Session N had flagged the count as right only for the
   dirty-marking path (pass5.md:770); it is. The sentence now says three and
   names what each does.
2. **`client/sound-engine`'s verified line** said the trace crosses "five
   threads". The page's own table lists five threads that *take part in the
   system*, but `Util.ioPool` appears in no step of the trace — it polls the
   ALC device list beside it (`AbstractDeviceTracker.tick`). A block placed
   near you crosses four: Server, Render, the sound engine's, and
   `Util.nonCriticalIoPool`. The landing page had it right and the page did
   not. Corrected to "four of the system's five threads", with a sentence
   saying which one is the odd one.
3. **`client/options`:354** said "the one thing a client-information packet
   can provoke is a hat-visibility broadcast".
   `ServerGamePacketListenerImpl.handleClientInformation` does broadcast the
   hat, but `ServerPlayer.updateOptions` also writes two of the nine fields
   into synched data — `ServerPlayer.DATA_PLAYER_MODE_CUSTOMISATION` and
   `ServerPlayer.DATA_PLAYER_MAIN_HAND` — which reach every tracker.
   `entities/synched-entity-data`:303-305 already said so, so this was a page
   contradicting another page. Rewritten as two outward effects and still no
   reply, with the link.
4. **`client/gui-and-screens`:35** called `MenuScreens` "the only registry of
   screens in the game" and :232 on the same page called `DialogScreens` "the
   second one". A page contradicting itself. The cast row now says what
   `MenuScreens` is *for* — the registry the menu packets look a screen up in.
5. **`client/gui-and-screens`:96** said "`Gui.isPausing` **is** what stops the
   integrated server". `Minecraft.runTick` (`Minecraft.java`:1321) recomputes
   `Minecraft.pause` as a conjunction of three: a singleplayer server, the
   GUI saying it is pausing, and the world not being published. Against
   `the-client-loop`, which had it right. Rewritten as the screen's *vote*,
   with the loop cited for the other two — and the overlay fact, which the
   loop page lacks, kept here.
6. **`client/README`:135-139** put the Part X/XI boundary at
   `Minecraft.renderFrame`'s *extract* zone, with "the handful of statements
   before that zone" still Part X's. The *frame* zone is pushed in
   `Minecraft.runTick` (`Minecraft.java`:1308) around the whole of
   `renderFrame`, so *update window*, *update* and *extract* are all inside
   it — there are no statements before it. `the-client-loop`,
   `rendering/the-frame` and `rendering/README` all say the *frame* zone, so
   the landing page was the outlier. Rewritten to the *frame* zone, keeping
   the real point: a few Part X cadences run inside it and stay Part X's for
   what they decide, not where they sit.
7. **`client/the-client-loop`:29** called `TickRateManager` "a *server*
   object". It is `net.minecraft.world.TickRateManager` — shared; the server
   subclass is `ServerTickRateManager`, and `ClientLevel` holds a plain one
   fed by packets. The cast row now says a shared class carrying numbers only
   the server sets.
8. **`client/the-client-loop`:140** said `ServerboundClientTickEndPacket`
   goes out "once per unpaused client tick that has a connection". The send
   (`Minecraft.java`:2064) is inside `Minecraft.tick`'s level block, so it
   also needs a level — a client still in configuration sends none. Corrected.
9. **`client/the-client-loop`:234** presented `Main.main`'s arming of
   `ClientShutdownWatchdog.startShutdownWatchdog` as the only one. There are
   two: `Main.java`:291 (post-main) and `Minecraft.java`:545, the window-close
   callback, armed against the game thread while the game is still running.
   Corrected, with what the second one catches.
10. **`player/input-to-movement`:296-298** said the client calls
    `BlockStatePredictionHandler.onTeleport` "to drop its outstanding block
    predictions". `BlockStatePredictionHandler.java`:70 assigns
    `lastTeleportSequence = currentSequenceNr`, and :49 uses it only to pass a
    null player position to `ClientLevel.syncBlockState` — it suppresses the
    *position snap*, and the predictions settle normally.
    `prediction-and-acks` had it right. Corrected, and the citation repointed
    from `#the-six-windows` to `#the-four-writes`.
11. **`player/input-to-movement`:131-132** said "Releases are always
    delivered". `KeyboardHandler.keyPress` (`KeyboardHandler.java`:527-534)
    returns early when `Screen.keyReleased` consumes the event, before the
    unconditional `KeyMapping.set(key, false)` at :602 — so a screen can
    swallow a release, which is the asymmetry `input-and-keybinds`:117-120 is
    built on. Corrected to: a release is recorded whether or not a screen is
    open, but a screen that consumes one swallows it.
12. **`world/fluids`:167-171** said the client ran `BucketItem.use` inside
    the prediction window, "holding the write until the server's
    acknowledgement arrives", and then said in its own next clause that the
    source appears with no round trip. The window holds the *old* state, not
    the write. Corrected.
13. **`reference/hud-elements`** — three defects in the table, all found by
    reading `Hud.extractRenderState` and `Gui.extractRenderState` against it.
    (a) `SpectatorGui.extractAction` (`Hud.java`:615) is a recorded element
    and had no row; it is the *else* of the selected-item-name row. Added as
    17b. (b) Row 27's *hidden by F1* cell held a condition instead of an
    answer, so the table never said whether subtitles are hidden — they are,
    with the in-game-UI exception the same row's last cell describes; and
    "something audible is playing" describes a *distance* test
    (`SubtitleOverlay.Subtitle.isAudibleFrom`), not a volume one, which is
    what `sound-engine`'s hook turns on. Both rewritten. (c) The second table
    said `Gui` records four elements "after the overlay or screen" without
    ever giving the overlay or screen a row, so the record order had a hole
    in it. Added as a dash row.
14. **`reference/glossary`:370-371** defined *Level* as the two subclasses
    "sharing an abstract `Level` and remarkably little else", where
    `the-client-level`'s whole comparison is of methods both sides *inherit*
    and one side hollows out. Rewritten to say that.
15. **`anatomy/what-this-book-skips`:375** wrote "the channel pool" and "the
    channel pools" in the passage that forwards to a page whose own heading is
    *The channel limits are counters, not pools*. Reworded, and the forward
    now carries that section's anchor; the binaural-rendering promise in the
    same sentence is now qualified to what the page actually pays off
    (`Options.directionalAudio`).

### Suspicions re-derived and found sound (no change)

- `what-makes-a-sound`:124 "the seed … so that every client picks the same
  variant **and the same pitch**" against `block-interaction`:306-308 "each
  side draws its own pitch from its own `Level.getRandom`". Both true and
  about different paths: `ClientboundSoundPacket` carries an explicit pitch
  field *and* `AbstractSoundInstance.getPitch` multiplies it by
  `Sound.getPitch().sample(this.random)` off the seeded random, so recipients
  agree; the *predicting* client generates its own seed and does not.
  Session J made the wording say which is which rather than changing either.
- `debugging-the-running-game`:71 `DebugSubscriptions.RAIDS` fed by
  `LevelChunk.registerDebugValues` — confirmed at `LevelChunk.java`:758.
- `debugging-the-running-game`:69-70 against `points-of-interest`:330-332 on
  the `POIS` feeder: both right, at two levels of the same call —
  `LevelDebugSynchronizers.registerPoi` delegates to
  `TrackingDebugSynchronizer.PoiSynchronizer`.
- `the-client-loop`:241-244 on the out-of-memory path: confirmed at
  `Minecraft.java`:908-949 — `oomRecovery` makes every later iteration call
  `runTick(false)`, and a second `OutOfMemoryError` rethrows.
- `client/options`:357-360 "the only thing that ever sets
  `Options.serverRenderDistance`": confirmed, two call sites, both the server
  announcing its own radius (`ClientPacketListener.java`:564 and :2560).
- `input-and-keybinds`:34 "the four mappings that can behave as toggles" and
  :73-75 "with default bindings, sneak and sprint": both right.
  `Options.java` constructs four `ToggleKeyMapping`s, and
  `ToggleKeyMapping.shouldRestoreStateOnScreenClosed` additionally requires
  the current binding to be a `KEYSYM`, which attack and use are not by
  default.
- `input-and-keybinds`:132-138 against `input-to-movement`:139-142 on whether
  `MouseHandler.handleAccumulatedMovement` is gated on the mouse being
  grabbed: the screen half and the turn half are tested separately
  (`MouseHandler.java`), and the reset runs outside both. Both pages right
  about their own half.
- `the-client-level`:55-57 on `ClientboundExplodePacket` carrying the sound,
  the particle and the knockback — confirmed against the record's seven
  components.
- `debugging-the-running-game`'s renderer count: 25 `renderers.add(new …)`
  calls in `DebugRenderer.refreshRendererList`. The page said "about two
  dozen" in one place and "twenty-five" in another; the hedge is now the
  count.

### Claims this session introduced

**Written from the decompile, and therefore pass 9's first targets.**

- `client/hud` — the toast shelf: five slots (`ToastManager.SLOT_COUNT`), a
  waiting deque, `Toast.occcupiedSlotCount` requiring *consecutive* free
  slots via `ToastManager.findFreeSlotsIndex`, `Toast.Visibility` as a
  two-state animation each carrying a sound, `Toast.getToken` for
  replacement, and `NowPlayingToast` as a separate field suppressed by
  `PauseScreen` and `MusicToastDisplayState`. Six implementations named.
- `client/hud` — the chat-GUI family: `GuiMessage`'s five fields including
  the signature; `GuiMessageTag`'s five instances (system,
  system-singleplayer, not-secure, modified, error), the two-pixel indicator
  bar drawn at x −4..−2 (`ChatComponent.handleTag`) — to the *left* of the
  line, outside the text — the hover tooltip, the icon on *modified* only and
  placed after the text (`GuiMessage.Line.getTagIconLeft`), and `logTag` as
  the only part reaching `ChatLog`.
- `client/hud` — the three gates above the whole HUD, moved here from
  `reference/hud-elements` and restated: `GameRenderer.extract` computes
  them, `Gui.extractRenderState` applies them.
- `client/hud` — the clear-colour override beside `GuiRenderState.isHudHidden`
  and the claim that every reading site of either is `GameRenderer`'s rather
  than `LevelRenderer`'s, moved here from `the-gui-render-tree`.
- `client/debugging-the-running-game` — the whole *Nothing in the game draws
  a gizmo* section, moved from `anatomy/what-this-book-skips` and extended:
  the thread-local collector, `Gizmos.addGizmo` throwing with none installed,
  the seven shape records, and the four collectors table
  (`Minecraft.collectPerTickGizmos`,
  `LevelExtractor.collectPerFrameMainThreadGizmos`,
  `LevelRenderer.collectPerFrameRenderThreadGizmos`, and `IntegratedServer`'s
  around its packet-and-tick step) with `GameTestServer` installing
  `GizmoCollector.NOOP` and a dedicated server installing none.
- `client/debugging-the-running-game` — the whole *The other query* section:
  `Options.keyDebugCopyRecreateCommand`, the shift modifier choosing the
  client's own NBT over the server's, `DebugQueryHandler`'s single
  transaction id and single callback, the two query packets, the gamemaster
  permission gate on including NBT, and the reduced-debug-info gate.
- `client/gui-and-screens` — `GameNarrator` as a wrapper over *text2speech*
  with `NarratorStatus` in front of it and two tempers (queued against
  `GameNarrator.saySystemNow`).
- `client/gui-and-screens` — the coverage claim: two hundred-odd classes in
  `client/gui/screens` and its eighteen sub-packages (measured: 224 files, 18
  directories), covered as one pattern with four routes; seven previously
  English-only examples given their class names.
- `client/text-and-fonts` — the five provider kinds named as classes
  (`BitmapProvider`, `TrueTypeGlyphProviderDefinition` with `FreeTypeUtil`,
  `UnihexProvider`, `SpaceProvider`, `ProviderReferenceDefinition`) and
  `SpecialGlyphs` as the not-from-a-file case; and the other two of the four
  ICU sites named (`CreateBuffetWorldScreen`, `LocalTime` — measured by
  grepping `com.ibm.icu`, which hits exactly four files).
- `client/the-gui-render-tree` — the definition of *stratum*; the note that
  `GuiGraphicsExtractor.nextStratum` and `GuiRenderState.nextStratum` are the
  same barrier under two names; the blur section's three gates
  (`Screen.extractBlurredBackground` as the only caller, the throw on a second
  request, the option, the in-game-UI opt-out) and the claim that the
  darkening tint is sharp because it is recorded after the boundary;
  `DynamicAtlasAllocator` as what runs out of room; `IMEPreeditOverlay` named;
  and the `PictureInPictureRenderer` half of the pip family.
- `client/what-makes-a-sound` — the reorganised *Who hears it*: both
  `ClientLevel.playSeededSound` overloads carrying the excluded-player rule,
  the two qualifications (`Player.playServerSideSound` excluding nobody; the
  predicting client drawing its own seed from `Level.soundSeedGenerator`), and
  `SoundType` described as the five-sound group on
  `BlockBehaviour.Properties`. Also `SoundEventRegistrationSerializer` named
  as what parses a `sounds.json` entry.
- `client/the-client-loop` — the two timers as a fifth bullet in the
  queues-and-re-entries list (`PeriodicNotificationManager` and
  `RemoteFriendListUpdateHandler`, each hopping back with
  `BlockableEventLoop.execute`), moved from the Part X landing page, which
  was the book's only explanation of either.
- `client/the-client-level` — `ClientLevel.EntityCallbacks` as the four hooks
  and `TransientEntitySectionManager` as the comparison table's last row made
  concrete.
- `client/README` — the part's coverage answer: nine tenths of what no page
  names is one more screen or widget (measured from `pass5_coverage.py`'s
  sub-package table — 27,146 of 29,360 unmentioned lines are under
  `client/gui`, 23,731 of them screens and widgets), plus the two declared
  exceptions (the model tree, player reporting).
- `src/figures/parts-dependency.md` — a new solid arrow **VII → X**, because
  the landing page now lists `containers-and-menus` under *before you start*
  for lecture six. `check_deps.py` caught the missing arrow and refused the
  first version of the page, which is the gate doing its job.

### Ownership decisions, for the record

- The excluded-player sound rule: `what-makes-a-sound#who-hears-it` owns it;
  `the-client-level` cut to one sentence; `block-interaction` and
  `using-an-item` keep copies that add something.
- The distance delay ("sound has a speed"): `what-makes-a-sound` owns it;
  `the-client-level`'s Q&A cut.
- The music fade against the music slider: `sound-engine` owns it;
  `what-makes-a-sound` cut to a clause and a link.
- The pause predicate: `the-client-loop` owns it; `gui-and-screens` keeps the
  screen's vote and the overlay default.
- The un-rebindable F3 shortcut: `input-and-keybinds` owns it; `hud` cut to a
  citation plus its own half.
- The blur split: `the-gui-render-tree` owns the *barrier*,
  `post-processing` owns the *chain that runs in the gap*; both rewritten,
  both linked.
- `Gizmos`: moved to `debugging-the-running-game`; `what-this-book-skips`
  keeps the address, which is that page's job.
- The frame cap, `ClientShutdownWatchdog` and the fenced-task queue were
  reported as duplicates with Part XI pages and **left for session K**, which
  owns the other half of each.

## Pass 5, session I — Part IX · Networking *(2026-09-06)*

*Five pages plus the landing page, one reader-of-the-book agent each; the part
read end to end in watching order first. All six rewritten, and eleven pages
in seven other parts edited because a Part IX page's owner or duplicate lived
there. Everything below is either a claim this session introduced or a
correction it made with the decompile open; the corrections come first.*

### Corrections — what the page said, what the decompile says

1. **`networking/the-connection`:236 — the flush bracket's scope.** The page
   said "The bracket is opened around the whole server tick".
   `MinecraftServer.suspendFlushing` is called at the top of
   `MinecraftServer.tickChildren` (`MinecraftServer.java`:1209-1211) and
   `resumeFlushing` at its end (:1281), so the packet drain that runs before
   `tickChildren` is **outside** the bracket — which is what
   `server-tick`:215 and `players-and-sessions`:212-213 both turn on. Page
   against two other pages. The section is now cut to a citation and says the
   bracket opens at the top of `tickChildren`.
2. **`networking/the-connection`:122-124 — `PacketListener.onPacketError`.**
   The page said it "by default raises a reported crash", which is the
   interface default (`PacketListener.java`:19-21) and is reached by **no
   listener a drained packet arrives at**: `ServerPacketListener`
   (`ServerPacketListener.java`:13-16) overrides it to log *"suppressing
   error"* and return, `ServerCommonPacketListenerImpl` (:78-81) adds
   `MinecraftServer.reportPacketHandlingException`, and
   `ClientCommonPacketListenerImpl` (:113-120) overrides it the other way,
   storing a disconnection report and calling `Connection.disconnect`. A
   reader of the page alone concluded a bad packet crashes the server. Page
   against `server-tick`:122-126.
3. **`server/server-tick`:221-222 — where `Connection.tick` flushes.** The
   page said "at the end of the connection phase". `Connection.tick`
   (`Connection.java`:387-411) flushes fourth of six steps, after the
   disconnect check and before `tickSecond` — which its own step list at
   :186-188 already had right and `the-connection`:241 states as the point.
   Page against itself and against Part IX. (This was logged for pass 9 by
   session C at [pass9.md](pass9.md); it is fixed rather than carried.)
4. **`server/server-tick`:186 — "flush the deferred send queue".**
   `Connection.tick`'s first step is `Connection.flushQueue`, which drains
   `Connection.pendingActions`, a queue of **closures** (`Connection.java`:388);
   `Connection` holds no outbound packet queue at all, which is
   `the-connection`:406-408's own claim. The step is now named for what it
   drains.
5. **`networking/what-the-client-is-told`:213 — "**Four** feeds ignore gate
   3".** Outside the gate-3 block of `ServerEntity.sendChanges`
   (`ServerEntity.java`:92-271) there are **three** sends — the passenger diff
   (:96-101), the `ItemFrame` tenth-call branch (:105-131) and
   `Entity.hurtMarked` (:266-269) — plus `Entity.updateDataBeforeSync` (:93),
   which is a hook and not a feed. The page's own figure named three and
   `synched-entity-data`:281-283 counts the sends as two with the item frame
   called out separately. Corrected to three, with
   `Entity.updateDataBeforeSync` named in front of them.
6. **`networking/what-the-client-is-told`:346 — the block-entity hop.** The
   page had `ChunkHolder.broadcastBlockEntityIfNeeded` calling
   `BlockEntity.getUpdatePacket`. `ChunkHolder.java`:240-245 has *IfNeeded*
   testing `BlockState.hasBlockEntity` and delegating to
   `ChunkHolder.broadcastBlockEntity` (:247-258), which is the one call site
   of `getUpdatePacket`. `block-entities` named the inner one and was right.
   Page against page.
7. **`networking/what-the-client-is-told`:317 — "Once a tick".**
   `ServerChunkCache.broadcastChangedChunks` is called from
   `ServerChunkCache.tickChunks` (`ServerChunkCache.java`:345-362), inside the
   `!level.isDebug()` guard and only when the caller passed `tickChunks`, so
   it is once per *chunk-ticking* tick and never in a debug world — which
   `lighting`:293-295 and `server-level-tick`:86 both carry and this page did
   not. Page against two pages.
8. **`networking/what-the-client-is-told`:214-215 — "none of them helps a mob
   outside entity-ticking range".** Gate 2 is a disjunction, so a mob out of
   entity-ticking range still passes it on a section change or with
   `Entity.needsSync` set — which the page states twice below (:167-170,
   :430-432). Page against itself; the sentence now names the mob that fails
   *all three* disjuncts.
9. **`networking/chat-and-signing`:266-268 — "vanilla never sends one".** The
   Q&A said no unsigned copy is ever sent, contradicting the page's own
   :44-46 and :219-220. `MessageArgument.resolveChatMessage`
   (`MessageArgument.java`:46-58) calls `PlayerChatMessage.withUnsignedContent`
   with the resolved component on every message-argument command. Page against
   itself; the claim is now that the *decorator* never produces one.
10. **`networking/chat-and-signing`:44-46 — "sets it on every message it
    resolves".** `PlayerChatMessage.withUnsignedContent`
    (`PlayerChatMessage.java`:44-48) keeps the copy only when it differs from
    `Component.literal(signedContent)`, so a command message with no selector
    in it carries none. Corrected to "differs exactly when a selector
    expanded".
11. **`player/player-anatomy`:245 — `ProfileKeyPair` on a `ServerPlayer`.**
    There is no `ProfileKeyPair` anywhere under `net/minecraft/server`; what
    `ServerPlayer` holds is `ServerPlayer.chatSession`, a `RemoteChatSession`
    (`ServerPlayer.java`:281), and the key pair lives on the client inside a
    `LocalChatSession`. Page against `chat-and-signing`:286-290.
    `player/README`:143 said the same thing and is corrected with it.
12. **`networking/packets-and-stream-codecs`:367-375 — an absolute "never".**
    "Client-supplied component *contents* never cross the wire at all" is
    falsified twenty lines above by the creative slot, which the same page
    calls the one packet that carries an arbitrary item. Scoped to the
    container click.
13. **`networking/packets-and-stream-codecs`:302-305 — a broken sentence** on
    a numeric claim ("with `BundlerInfo.BUNDLE_SIZE_LIMIT` caps a bundle at
    4,096"). Rewritten; 4,096 re-derived (`BundlerInfo.java`:13), and
    `BundlePacket`'s relation to `ClientboundBundlePacket` stated (abstract
    class and its one subclass, `ClientboundBundlePacket.java`:7).
14. **`networking/packets-and-stream-codecs`:335-344 — trust and direction.**
    The paragraph said trust is "about the read budget rather than about
    direction" and then "The rule is direction". Both halves are true of
    different things and the page asserted and denied one claim; now the
    *mechanism* is a budget and the *rule for choosing* is direction.
15. **`networking/README`:84-86 — "the only system in the book designed
    against an adversary".** False against page two of its own part, which has
    a section headed *What stops a hostile sender*. Narrowed to a *lying*
    peer against a malformed one, which is the real difference.
16. **`networking/README`:78-80 against :106-108 — an internal
    contradiction.** The watch-order line said the player object is built in
    this part; *where the part stops* said how a `ServerPlayer` comes to exist
    is Part III's. Both now say the same thing.
17. **`networking/protocol-phases`:60 — a table cell naming the wrong kind of
    thing.** The status row's clientbound listener was "reached from
    `ServerStatusPinger`" where every other cell names a listener; it is an
    anonymous `ClientStatusPacketListener` inside that class
    (`ServerStatusPinger.java`:71).

**Four suspicions re-derived and found sound**, recorded because a strike is a
claim: `IdDispatchCodec`'s "not a table the encoder walks" (it is a
`Object2IntMap` lookup and then an indexed list, `IdDispatchCodec.java`:46-67 —
no walk, so the sentence stands); the five-minute server and seven-minute
client chat expiries (`PlayerChatMessage.java`:30-31, exactly 5 and 5+2);
`ServerEntity.FORCED_TELEPORT_PERIOD` as 400 gated calls
(`ServerEntity.java`:59); and the two places the join reads the whole save
file, which `protocol-phases` put in `spawnPlayer` and `players-and-sessions`
in `PrepareSpawnTask.Ready` — both right, since `spawnPlayer` delegates to
`Ready.spawn` (`PrepareSpawnTask.java`:123-131, 225-240); the two pages now
name it the same way.

### Claims introduced

**`networking/README` (rewritten to the role).**
- The part's shape sentence is now "**the wire three times, and two things it
  carries**", replacing "one wire and three passengers", which the page
  contradicted twenty lines below and which `lectures.md` carried in its
  un-softened form. The claim is that lectures 1–3 are all descriptions of the
  wire and 4–5 are applications of the play phase.
- **The figure is redrawn** to two subgraphs — *the wire, described three
  ways* over the chain `TC → PSC → PP`, and *what it carries* over `WCT` and
  `CS` — with one labelled edge between them replacing the two unlabelled
  arrows `PP --> WCT` and `PP --> CS`, which asserted a dependency the page's
  own :88-91 denies. Verified before redrawing that neither target page names
  `protocol-phases`, `ConnectionProtocol` or `ProtocolInfo`.
- The opening's four player-visible failures are replaced: two of the old four
  (the rubber-band, the block that comes back) are paid off only in Parts VIII
  and X, and one (the grey bar) nowhere in the book. The new four —
  *Connection lost*, the mob that freezes and jumps, the chest that says
  nothing until opened, the red chat line that takes the rest of the session
  with it — are each answered on a page of this part.
- The traffic-volume clause is kept and re-purposed as the reason two of five
  lectures take most of the part's length.
- **A new *Where the part stops* section** with the size through
  `{{#include ../../generated/part-networking.md}}`, and the coverage
  argument: **this part owns the wire, not everything in `network/`** —
  `network/chat` is Part II's, much of `client/multiplayer` is Part X's, and
  the largest block is the packet classes, which are catalogued and not
  narrated. Three systems are named and declined with a reason: player
  reporting (already out of scope on `what-this-book-skips`), the server list
  and its screen (Part XI's to draw), and the boss-bar feed, whose sending
  side has no owner anywhere in the book.
- *Reference this part uses* now lists `level-data-and-rules`, which a page of
  the part actually cites, and drops nothing.

**`networking/the-connection`.**
- Keep-alive is stated as the *common* listener's, so it runs in
  configuration, and takes in two facts from `players-and-sessions`: that a
  wrong-id answer disconnects immediately rather than being ignored, and that
  the round trip is smoothed three parts old to one part new, so a tab list
  lags a real latency change by several pings.
- The memory-connection crash answer takes both disconnect strings in from
  `server-tick` and states them as one catch with two branches.
- **New coverage passage**: `client/multiplayer/resolver` —
  `ServerAddress.parseString`, `ServerNameResolver`, `ServerRedirectHandler`'s
  `_minecraft._tcp` SRV lookup, `AddressCheck` and `ResolvedServerAddress` —
  written from `ServerNameResolver.java`:21-38 and
  `ServerRedirectHandler.java`:42. Plus `ServerList`/`ServerData` named in the
  clause that already described them, `LegacyServerPinger` as the client half
  of the legacy-query row, and `Varint21LengthFieldPrepender` named in the
  outbound pipeline list where only the string `"prepender"` stood.

**`networking/packets-and-stream-codecs`.**
- **New passage on the per-phase listener interfaces** —
  `ClientGamePacketListener` and `ServerGamePacketListener` (390 lines
  between them), the common pair, the six phase pairs and the two roots — as
  what `Packet.handle` targets, which the page asserted and never named. The
  claim that a listener of the wrong shape is the cast failure
  `the-connection` describes.
- **New clause on the login-phase payload family** (`CustomQueryPayload`,
  `CustomQueryAnswerPayload` and the discarding forms), because the section
  called `CustomPacketPayload` "the one seam" and the login twin exists.
- The trusted pairs now carry their call-site counts, moved in from
  `codecs-nbt-json`: `TRUSTED_COMPOUND_TAG` has exactly one
  (`ClientboundBlockEntityDataPacket`), `TRUSTED_TAG` none at all, and
  `ComponentSerialization.TRUSTED_STREAM_CODEC` is used by every clientbound
  chat packet — which pays off `text-components`:236's inbound promise and is
  the codec the page's own figure draws (verified against
  `ClientboundSystemChatPacket.java`:13 and
  `ClientboundPlayerChatPacket.java`:22).
- The three-layer serverbound defence, moved in from `codecs-nbt-json`, and
  `ItemStack.CODEC` named as what the validating re-encode runs;
  `ServerGamePacketListenerImpl` named as the server's creative context.
- **"the other *eight* templates — nine in all"** stated once here, where the
  page had "every other template" and `protocol-phases` had a bare correction.

**`networking/protocol-phases`.**
- The registry-and-tag-sync passage is cut to what belongs to a *phase* — the
  order and the count of packets — with the mechanism cited to
  `identifiers-and-registries#when-a-world-opens`. The claim retained here is
  that nothing is applied as it arrives.
- The play-binding paragraph is cut to one sentence whose claim is new in this
  form: the configuration-to-play switch is **the only transition in a
  connection's life that changes what a packet number means as well as which
  packets are legal**.
- `PrepareSpawnTask`'s internals are cut to the two states and the hook, with
  the page keeping "everything between the join task and that handler is a
  server holding a ticket on chunks for a player that does not exist" as its
  own.
- `ClientboundCodeOfConductPacket` and `ServerboundAcceptCodeOfConductPacket`
  named, and `ServerboundCustomQueryAnswerPacket` named where the page had
  only the request side.
- The creative filter and the compression asymmetry are cut to one clause and
  a citation each.

**`networking/what-the-client-is-told`.**
- **`Entity.updateDataBeforeSync` added to the prose and the figure**, ahead
  of the gate-3 branch, with the claim that an effect expiring this tick can
  dirty the container and open its own gate in the same call.
- **New paragraph after the gate-3 table**: the interval gate covers the
  synched-data flush as well as the position block; the `ItemFrame` branch is
  the *only* path to that flush which skips the interval test; and
  `ServerEntity.handleMinecartPosRot` reaches it from inside the gate. All
  three moved from `synched-entity-data` (session F's routed list, discharged).
- Two table rows gain the numbers `movement-and-collision` had and this page
  did not: `FORCED_TELEPORT_PERIOD` as four hundred *gated* calls, "at least
  1,200 ticks on the default interval", and that the ground-flag row is the
  common case.
- `VecDeltaCodec` named in the prose as the object holding the dead-reckoning
  base, where it had appeared only in *Where to look*;
  `ClientboundSetPassengersPacket` and `ClientboundSetEntityLinkPacket` named
  in the feeds and the pairing bundle.
- The chunk enter/leave section and the view's shape are cut to two sentences
  citing `tickets-and-loading`, keeping only `ChunkTrackingView.Positioned`,
  which no other page names; the light audience is cut to one sentence citing
  `lighting`; both block-entity default statements are cut to the consequence
  citing `block-entities`.

**`networking/chat-and-signing`.**
- **New passage on the text filter** — `TextFilter`, `TextFilter.DUMMY`,
  `MinecraftServer.createTextFilterForPlayer`,
  `ServerTextFilter.createFromConfig` and its two implementations,
  `FilteredText` and `Filterable` — with the claim that a vanilla server has
  no filter at all and that filtering here is never destructive, because a
  `FilterMask` travels with the message and is applied per recipient. Written
  from `ServerTextFilter.java`:72-108, `TextFilter.java`:9-19,
  `FilteredText.java`, `Filterable.java`:11 and `MinecraftServer.java`:2290
  against `DedicatedServer.java`:826-828.
- `ChatTypeDecoration` named as the translation key and argument list behind
  the *someone said* wrapper, with the claim that the phrasing around a line
  is data and the line is not.
- `LastSeenTrackedEntry` named as the twenty slots, and `LocalChatSession` as
  what holds the key pair on the client.
- The selector-expansion fact is given one home on the page — the *Commands*
  section — with the mechanism cited to `text-components` and the enumeration
  of which commands to `brigadier-and-commands`; the opening keeps only the
  security consequence.
- The `ChatAbilities` paragraph is cut to a sentence and a link, with the four
  atoms' effects moved to `commands/permissions`.

**Pages in other parts, edited because they held or contradicted Part IX
material.**
- `server/players-and-sessions`: the chunk-batch pacing cut to "a joining
  client is trusted with one batch" plus the claim that the first batch is a
  hard round trip; the keep-alive mechanism cut to a citation, keeping the
  asymmetry the section is about; the reconfigure cut to *a leave that keeps
  the socket* with the phase half cited to `protocol-phases`.
- `server/server-tick`: `Connection.tick`'s step list corrected (above), the
  chunk-pacing citation repointed from `tickets-and-loading` to
  `what-the-client-is-told#the-rate-the-client-asks-for` (the first of the two
  citations `pass5.md`:89-95 left for this session; the second is
  `players-and-sessions`:266, done above), and the memory-connection sentence
  cut to a citation.
- `foundations/identifiers-and-registries`: takes two facts from
  `protocol-phases` — that `PackLocationInfo.knownPackInfo` is an optional, so
  a world's own datapack is absent from the request, and that the client's
  load is dispatched to a background executor and then blocked on.
- `foundations/codecs-nbt-json`: the *Trusted, untrusted and validated*
  section rewritten to what this page owns — that the serverbound path is the
  only one of its four where a codec is run for its errors rather than its
  output, and that the persistent codec is used as a validator for the wire
  one. The trusted-pair enumeration and the three fences moved to Part IX.
- `commands/permissions`: gains what the four chat atoms *do*
  (`ChatAbilities.java`:71-83).
- `commands/brigadier-and-commands`: the fourth telling of the chat Netty hop
  cut to a citation of `server-tick` and `chat-and-signing`, keeping the claim
  that matters for a command — the validation that can disconnect you runs
  before the parse.
- `commands/dialogs`:8-9 repointed: `ClientboundShowDialogPacket`'s two
  protocols are `packets-and-stream-codecs`', not `protocol-phases`'.
- `entities/entity-anatomy`:38's `ServerEntity` row repointed from gate 1 to
  gate 3, which is the section that answers it.
- `anatomy/anatomy`:128 now sends the memory channel to `the-connection` as
  well as the phase walk; `reference/threads` gains a link to
  `protocol-phases#login` for the state machine it was explaining.
- `player/player-anatomy` and `player/README`: correction 11.
- `src/lectures.md` and `src/reference/glossary.md` re-synced: the Part IX
  shape paragraph follows the landing page, the jitter clause follows its
  owner (`the-client-loop` says *most*), *Protocol phase* spells
  *handshaking* as the page does, and *Packet* drops the unsupported "roughly
  half the implementations are records" for "three shapes", which is what the
  owner says. Six glossary owner links gain anchors.

**Anchors.** Part IX carried **7 anchors on 62 cross-part links** before this
session — the sixth part running to arrive with almost none — and carries 67
now, plus 23 within the part. Each asserts that the named section is the
answer; `check_links.py` proves only that the heading exists.

### For pass 9's attention, found and not fixed

- `reference/glossary`:437-440 previously said "roughly half the
  implementations [of `Packet`] are records", which no page supports; it now
  says "three shapes", which the owner page does support but does not count.
  A count either page could state and neither does.
- `chat-and-signing`:139-140 counts "the first fifteen rows" of its check
  table by hand; correct as it stands, and wrong the moment a row is added.
- `chat-and-signing`:100-101 uses "expired" for `hasExpiredServer`, which is
  five minutes; the number appears only in the Q&A at :262-263. True but
  stated in two places in two vocabularies.
- Whether a respawn clears a broken chat chain. `ServerPlayer.restoreFrom`
  copies `chatSession` (`ServerPlayer.java`:1729) but the chain decoder lives
  on `ServerGamePacketListenerImpl` (:274), which survives a respawn — so a
  broken chain almost certainly survives dying. Not written, because it is a
  new claim and the page did not raise it; logged in
  [pass5.md](pass5.md) for pass 6.
- `foundations/text-components` tells the `/say @a` punchline twice on its own
  page (:274-275 body and :425-432 Q&A). Part II's, and a page-shape finding;
  logged for pass 6.

## Pass 5, session H — Part VIII · The player *(2026-09-06)*

All seven pages of Part VIII touched plus the landing page:
`src/systems/player/README.md` (rewritten to the landing-page role, gaining a
*where the part stops*), `player-anatomy.md`, `the-two-phase-tick.md`,
`input-to-movement.md`, `the-sword-swing.md`, `the-spear.md`,
`hunger-and-experience.md`, `status-effects.md`. Nine pages in six other parts
edited because a Part VIII page's owner or duplicate lived there:
`entities/README.md`, `entities/attributes.md`, `entities/damage-and-death.md`,
`blocks/block-interaction.md`, `server/players-and-sessions.md`,
`server/server-tick.md`, `items/using-an-item.md`,
`foundations/data-driven-types.md`, `reference/non-living-damage.md`. Plus
`reference/glossary.md`, the Part VIII block of `src/lectures.md` and
`reference/level-data-and-rules.md`'s *four parts* paragraph. Part VIII has no
hand-kept Reference page of its own; `reference/non-living-damage.md` is Part
VI's and was edited here only to take an explanation off it.

### Corrections — the page was wrong, and the decompile says so

- **`player-anatomy`: `Avatar` does not exist for the renderer.** The page
  said "It exists for the renderer", and `Avatar` is in
  `server-classes.txt` (line 2363) — a server class. `Avatar.java` is 57
  lines holding the player-shaped `POSES`/dimensions, the 1.62 eye height,
  the two cosmetic synched values and the abstract `Avatar.getProfile`, and
  its two subclasses are `Player` (`Player.java`:129) and `Mannequin`
  (`Mannequin.java`:28). `AvatarRenderer` (`AvatarRenderer.java`:52) being
  generic over `Avatar & ClientAvatarEntity` is a consequence of the rung,
  not its cause. Rewritten to say the rung is what `Player` and `Mannequin`
  share, and reconciled with the other two accounts in the book
  (`entity-anatomy`:185 "its point is `Mannequin`", `attributes`:132 "the
  player-shaped hitbox but not the attribute set").
- **`the-sword-swing`: `Player.postPiercingAttack` is `LivingEntity`'s.**
  The method is declared once, at `LivingEntity.java`:1799, and `Player` has
  no override; `Player.java`:989 calls it. `the-spear` and
  `items/enchantments` already spelled it `LivingEntity.postPiercingAttack`,
  so the page disagreed with its own declared pair. Fixed, with a clause
  saying why a *piercing* hook closes an ordinary swing.
- **`the-sword-swing` and `entities/damage-and-death`:
  `LivingEntity.getSecondsToDisableBlocking` is conditional.**
  `LivingEntity.java`:4238-4243 returns `Weapon.disableBlockingForSeconds`
  only when `weaponItem == this.getActiveItem()`; both pages presented it as
  an unconditional read-back. Fixed on both, in the same wording. (Confirmed
  the practical scope: `getActiveItem` is the main-hand stack when nothing is
  being used, so an ordinary axe swing still disables a shield; the condition
  bites while the attacker is using something else.)
- **`player-anatomy`: `Player.HELD_ITEM_SLOT` is the cursor, not the selected
  slot.** Written new this session and corrected before it landed:
  `Player.java`:1710-1726 makes 499 the `containerMenu` carried stack.
- **`status-effects`: `MobEffectInstance.compareTo` orders both surfaces, in
  opposite directions.** The page said it "orders the icons in the HUD".
  `Hud.java`:537 sorts with `Ordering.natural().reverse()`;
  `EffectsInInventory.java`:66 sorts with `Ordering.natural()`. Corrected
  and the consequence stated. (Carried the standing queue entry at
  `pass5.md`:2536.)
- **`status-effects`: the ambient-particle numbers are exact.** "divides by
  about four" was 3.75. `LivingEntity.java`:908-911 has
  `bound = isInvisible() ? 15 : 4` and `ambientFactor = isAmbient ? 5 : 1`,
  rolled as `nextInt(bound * ambientFactor) == 0`. Rewritten as the two
  bounds and their product. (Carried `pass5.md`:858's Part VIII row.)
- **`server/players-and-sessions`: the flying kick's numbers moved, and the
  vehicle half was incomplete on both pages.**
  `ServerGamePacketListenerImpl.java`:346-355 runs a second counter,
  `aboveGroundVehicleTickCount`, against its own `getMaximumFlyingTicks(vehicle)`
  and only for the controlling passenger. `input-to-movement` now says so and
  Part III keeps a clause. (Carried `pass5.md`:209.)
- **`player-anatomy`: `DemoMode` written from the source.** Introduced this
  session, so listed as a claim: `MinecraftServer.java`:2295 constructs it
  (not `PlayerList`), and `DemoMode.java`:26-90 reads the level's *gameTime*,
  not a clock of its own; past `TOTAL_PLAY_TICKS` it overrides
  `handleBlockBreakAction` and `useItem` to answer with a reminder.

### Suspicions re-derived and found sound — no change made

- `the-two-phase-tick`:151, "the one thing that stops phase two is
  `MinecraftServer.isPaused`". `ServerGamePacketListenerImpl.java`:306 is
  `if (this.server.isPaused() || !this.tickPlayer())`. The claim stands.
- `input-to-movement`, "position must have moved by more than 2×10⁻⁴ blocks".
  `LocalPlayer.java`:285 compares `Mth.lengthSquared(...)` against
  `Mth.square(2.0E-4D)`, so the threshold really is 2×10⁻⁴ of distance, not
  of its square.
- `input-to-movement`:131, "Releases are always delivered".
  `KeyboardHandler.java`:602-603 calls `KeyMapping.set(key, false)` outside
  the `handlesGameInput` gate that presses sit behind. The claim stands, and
  it does not contradict `client/input-and-keybinds`, whose "swallowed
  release" is `ToggleKeyMapping`'s and a screen's `KeyMapping.releaseAll`.
- `the-spear`'s figure node "server side only" against
  `using-an-item`:8-9's "runs every tick on both sides".
  `ItemStack.java`:1170-1184 shows both: the method runs on both sides, and
  the divert to `KineticWeapon.damageEntities` is server-gated. No
  contradiction; logged for pass 7 as a compressed label.

### Claims introduced — the ownership cuts

Every trimmed sentence is a new claim, and every anchor asserts that the
named section is the answer. The cuts, each *from* → *to*:

- **The record–simulate–snap-back bracket**, from `input-to-movement`'s
  Q&A to `the-two-phase-tick#the-bracket-and-what-survives-it` — the page
  named after it. The riding qualifier (`Entity.rideTick` repositions a
  passenger every tick, so "never here" is an *on foot* claim) **moved** to
  the owner, and so did the naming of the pipeline
  (`LivingEntity.aiStep` / `LivingEntity.travel` / `Entity.move`).
- **The twin hook.** `the-two-phase-tick` and `input-to-movement` opened on
  the same surprising fact, two consecutive lectures apart.
  `input-to-movement`'s opening now ends on its own three surprises, which
  were already on the page.
- **The authority preamble**, told three times in the book. Both Part VIII
  copies cut to one sentence plus
  `authority#five-predicates-and-the-final-one-the-other-four-hang-off`;
  the fall-damage gate — its third full telling, `pass5.md`:2710 — cut to
  one sentence plus `authority#three-cases-read-on-both-sides` on both
  `the-two-phase-tick` and `input-to-movement`.
- **The Netty-thread survey**, from `the-two-phase-tick` to
  `server-tick#every-packet-since-last-time-in-one-drain`, which owns the
  rule. The count **moved** with it and was re-derived:
  `ServerGamePacketListenerImpl` declares 61 `public void handle*` methods
  and 52 call `PacketUtils.ensureRunningOnSameThread`; the nine that do not
  are `handleEditBook`, `handleChat`, `handleChatCommand`,
  `handleSignedChatCommand`, `handleChatAck`, `handlePingRequest`,
  `handleSignUpdate`, `handleConfigurationAcknowledged` and
  `handleCustomPayload`.
- **`Player.cannotAttack`'s two hooks and `Player.deflectProjectile`**, from
  `reference/non-living-damage` — where a Reference page held the book's
  only explanation, against `TEMPLATE.md` — **onto** `the-sword-swing`'s gate
  paragraph, with `Entity.isAttackable`, `Entity.skipAttackInteraction`,
  `Interaction`, `BlockAttachedEntity`, `EntityTypeTags.REDIRECTABLE_PROJECTILE`
  and the ghast fireball. The Reference page keeps one sentence and a link,
  and its `AbstractHurtingProjectile` row lost the same explanation.
  (`pass5.md`:2700, the oldest open entry on the page.)
- **`Entity.hurtOrSimulate`'s boolean**, the reverse move: the Reference
  page's sharper reading — *was anything damaged*, not *did the hit land* —
  is now on `the-sword-swing`, and both of that page's figures say the same.
- **The `hurtClient` roll-call**, cut from eight names to its count and its
  pattern, with the table cited. **The four-step client-tick order**, cut to
  its consequence with `the-client-loop#what-a-tick-is-in-order` cited.
  **The excluded-player sound rule** (its fourth telling), cut to a citation
  of `what-makes-a-sound`. **The i-frame counter's decrementers**, cut to a
  citation of `damage-and-death`.
- **`UseEffects`**, from `hunger-and-experience` to
  `using-an-item#moving-while-you-use`. Its vibration half **moved** with it
  and was written from the source: `ItemStack.causeUseVibration`
  (`ItemStack.java`:781-788) gates `Entity.gameEvent` on
  `UseEffects.interactVibrations`, called by `LivingEntity` at both ends of a
  use and by `FishingRodItem` and `BoneMealItem` for themselves.
  (`pass5.md`:2980.)
- **`Consumable`'s field roster and the five `ConsumeEffect` implementations**,
  from `hunger-and-experience` to `using-an-item`, which spends the component
  through its whole lecture and never defined it. `hunger-and-experience`
  keeps the *walk* — `ConsumableListener` and `Consumable.onConsume` — because
  the walk is its hook, and keeps `FoodProperties` and `FoodData.eat`. The
  ruling is written out in `pass5.md`. `foundations/data-driven-types`:184's
  `CONSUME_EFFECT_TYPE` row now points at the section that names them.
  (`pass5.md`:2969.)
- **The client replay of a meal**, cut on `hunger-and-experience` to a clause
  plus `using-an-item#the-meal-tick-by-tick`; the page keeps
  `ClientPacketListener.handleSetHealth`, which is the overwrite and its own.
- **Item ticking's two callers** and **the one-orb-per-tick sweep**, cut on
  `the-two-phase-tick` to their placement plus links to `player-anatomy` and
  `hunger-and-experience`. Session G's ruling that `player-anatomy` owns the
  forty-three-slot reason is kept; the page-VIII reader agent's counter-call
  for `items-and-stacks` was declined, in writing, in `pass5.md`.
- **The effect→attribute reload sentence**, the one move *into* Part VIII:
  `attributes`:213 explained that effects are restored from NBT without the
  apply hook running. `status-effects` now has a section for it, written from
  `LivingEntity.java`:762-765 and :818-828, and `attributes` keeps the
  half-sentence it needs.

### Claims introduced — coverage and new material

- `status-effects`: the per-effect `MobEffect` subclass family (`world/effect`
  holds nineteen classes, of which sixteen are one small subclass per effect
  plus `InstantaneousMobEffect`); `MobEffectCategory`'s three constants and
  its two readers (`PotionContents.java`:189 for tooltip colour,
  `Hud.java`:551 for the two-row split, which asks `MobEffect.isBeneficial`
  and so puts *neutral* on the bottom row with a blue tooltip); the reader of
  `LivingEntity.effectsDirty` (`LivingEntity.updateDirtyEffects`, from
  `Entity.updateDataBeforeSync` at the top of `ServerEntity.sendChanges`,
  `ServerEntity.java`:93 and :310); and the six-hundred-tick re-send named at
  last (`LivingEntity.java`:888, a bare literal).
- `player-anatomy`: the skin family — `PlayerSkin` (four textures, a
  `PlayerModelType` of `SLIM` or `WIDE`, a *secure* flag) and
  `PlayerModelPart`'s seven bits, read through
  `Avatar.DATA_PLAYER_MODE_CUSTOMISATION`; `DemoMode`; `Player.getSlot`'s
  command-facing addressing; `LocalPlayerResolver` as the tab-list-first
  profile lookup; `ProfileKeyPair` cross-linked to `chat-and-signing`; and
  `StackedContents` named as `items/recipes`' though it lives in this
  package.
- `the-spear`: the component table now says which subset it is — the nine
  are the *weapon*, and `Item.Properties.spear` also calls
  `durability`, `repairable` and `enchantable` from the material
  (`Item.java`:510). The spear's `UseEffects` row now states all three
  fields, which is its own component. And the charge's targets are named in
  prose for the first time — `KineticWeapon.damageEntities`
  (`KineticWeapon.java`:74-76) walks `ProjectileUtil.getHitEntitiesAlong`
  with `PiercingWeapon.canHitEntity` and the block-collider clip, exactly as
  the stab does; only the figure had said so. (`pass5.md`:2543.)
- `entities/README`: one clause declaring that `world/effect` is in Part VI's
  packages and its lecture is Part VIII's — the ruling is below.
- `player/README`: a *where the part stops* section, which the part had none
  of, with the size include, the upward border at `Avatar`, five outward
  borders, and two declared declines (`Hotbar`/`HotbarManager` as the
  creative screen's; the player half of sleep as a real gap, sent to §7).

### Seams repointed, which are claims about who owns what

- `input-to-movement`'s `BlockStatePredictionHandler.onTeleport` link went to
  `block-interaction`, which never names the handler; now
  `prediction-and-acks#the-six-windows`.
- `player-anatomy`'s `ServerPlayer.chunkTrackingView` link went to
  `tickets-and-loading`; what the client *has been sent* is Part IX's, so it
  now points at `what-the-client-is-told#chunks-arrive-on-a-loop-the-client-paces`.
- `player-anatomy`'s slot-addressing row hand-forwarded to "commands and
  containers" in plain text, and no page named `Player.getSlot`; the page now
  pays it off itself.
- `status-effects`' hand-forward for `PotionContents` and its siblings went
  to `using-an-item`, which names none of them; split between the machinery
  (`using-an-item#the-meal-tick-by-tick`) and the components
  (`hunger-and-experience#eating-is-a-component-walk`).
- `block-interaction`'s reach gate now cites `player-anatomy#what-player-owns`
  — the ruling for `pass5.md`:2861, taken once on the first half of the
  declared pair rather than twice.
- **Anchors on 71 of Part VIII's links, where the part had none at all** —
  the fifth part running to arrive with zero. Plus the anchors on the six
  cross-part edits above.

### Summariser drift corrected

- `player/README`:57-59 said Part VII owns the inventory; `items/README`:38-41
  and `player-anatomy` say Part VIII does. The landing page and
  `src/lectures.md`:211-212 both fixed in Part VIII's favour. (`pass5.md`:2983.)
- `reference/glossary.md`: **Avatar** led on the renderer, which the page no
  longer says; **LocalPlayer** claimed "its own prediction", which
  `player-anatomy`:190 explicitly denies (`MultiPlayerGameMode.startPrediction`
  reaches `ClientLevel.getBlockStatePredictionHandler` per call). Both
  rewritten to the pages, with anchors.
- `reference/level-data-and-rules`:16-19 sent readers to Part VIII "for the
  spawn"; no Part VIII page explains spawn or respawn. Repointed to what
  Part VIII actually reads there — the two movement game rules.
- `player/README`'s figure node called the spear "the same hit, twice"; the
  page says two different attacks sharing a tail. Node reworded.

### For pass 9's attention, found and not fixed

- `Weapon.AXE_DISABLES_BLOCKING_FOR_SECONDS` (5.0) is declared at
  `Weapon.java`:12 and read by nothing — `ToolMaterial.java`:37 passes the
  value through a parameter. Another dead constant, of the shape
  `FoodConstants` and `MinecraftServer.AUTOSAVE_INTERVAL` already have.
- `LivingEntity.TAG_ACTIVE_EFFECTS` (`LivingEntity.java`:145) is likewise
  declared and unread; `:764` and `:820` write the literal *active_effects*.
  The new `status-effects` section names the tag, not the constant, for that
  reason.
- `the-sword-swing` names `Player.attackVisualEffects` and
  `Player.damageStatsAndHearts` in the tail order and no page in the book
  explains either. `ServerPlayer.wardenSpawnTracker` and `ServerPlayer.camera`
  are named on `player-anatomy` and explained nowhere. All four sent to
  `pass3.md` §7 rather than written here.
- `the-sword-swing`:219-221's three attack-ticker resets were re-derived as a
  set and reconcile (`Player.java`:1834 `Player.onAttack` →
  `resetOnlyAttackStrengthTicker`; `MultiPlayerGameMode.java`:462;
  `ServerPlayer.java`:2085), but it is three named resets on two sides in one
  answer and is worth a second reading.

## Pass 5, session G — Part VII · Items and inventories *(2026-09-05)*

All eight pages of Part VII touched plus the landing page:
`src/systems/items/README.md` (rewritten to the landing-page role),
`items-and-stacks.md`, `using-an-item.md`, `containers-and-menus.md`,
`recipes.md`, `enchantments.md`, `enchanting.md`, `contexts-and-predicates.md`,
`loot-tables.md`. Five pages in three other parts edited because a Part VII
page's owner or duplicate lived there: `foundations/data-components.md`,
`foundations/data-driven-types.md`, `foundations/resource-system.md`,
`blocks/block-breaking.md`, `blocks/block-entities.md`. Plus the Part VII block
of `src/lectures.md`. Both of the part's Reference pages
(`reference/enchantment-hooks.md`, `reference/loot-context-params.md`) are
generated and were not edited.

### Corrections — re-derived against the decompile before the fix

- **`enchanting`: which paths roll in `EnchantmentHelper.selectEnchantment`.**
  The page said "only the table and the provider and loot paths roll one to
  decide *what you get*, and they roll it in the same place:
  `EnchantmentHelper.selectEnchantment`", and then contradicted itself twice
  below. The decompile: `selectEnchantment` has four callers —
  `EnchantmentMenu.java`:232, `EnchantmentsByCost.java`:28,
  `EnchantmentsByCostWithDifficulty.java`:31 and `EnchantmentHelper.enchantItem`
  (`EnchantmentHelper.java`:610, which `EnchantWithLevelsFunction.java`:72
  calls). `SingleEnchantment.enchant` samples a level for a named enchantment
  and never selects (`SingleEnchantment.java`:22-24), and
  `EnchantRandomlyFunction.run` picks with `Util.getRandomSafe` off
  `LootContext.getRandom` (`EnchantRandomlyFunction.java`:65-87). Now: four
  callers named, and the two that roll their own said so.
- **`loot-tables`: where `LootTable.createStackSplitter` sits in the call.**
  The sequence diagram put it on the pool's return ("stacks, each through
  createStackSplitter"). The decompile: `LootTable.fill` calls the private
  `getRandomItems(context)` (`LootTable.java`:157 → :137-143), which calls
  `getRandomItems(context, result::add)` (:121-123), which wraps the consumer
  in `createStackSplitter` and hands it to `getRandomItemsRaw` — where the
  *table's* composite function is layered inside it (:93-103). The splitter is
  therefore the outermost wrapper, applied once per fill and after the table's
  own functions, which is what the flowchart and the prose already said. The
  diagram now says so, and the load-bearing consequence (a nested table is
  split once) is unchanged.
- **`containers-and-menus`: the size of a click's traffic.** The page said "the
  traffic is 128 integers rather than 128 full `DataComponentPatch`es". A
  `HashedStack.ActualItem` carries an item holder, a count, one CRC32C integer
  per *added* component and the plain set of removed ones — the page says so
  itself two sentences earlier — so 128 claimed slots is not 128 integers.
  `ServerboundContainerClickPacket.java`:16-17 caps the map at 128 entries.
  Now: "each claimed slot costs an integer per component rather than a
  re-encoded `DataComponentPatch`".
- **`using-an-item`: which method has one override.** The page said
  "**`CrossbowItem.useOnRelease` is its only override in the tree**" of
  `ItemStack.useOnRelease`. `ItemStack.useOnRelease` (`ItemStack.java`:790-791)
  delegates to `Item.useOnRelease` (`Item.java`:367), and it is the latter that
  `CrossbowItem.java`:264 overrides. Now: the delegation is stated and the
  count attaches to the hook.
- **`loot-tables`: the thirteen path prefixes.** The count is right — the
  literal `register` calls in `BuiltInLootTables` fall under thirteen top-level
  prefixes (chests, gameplay, shearing, charged_creeper, archaeology,
  spawners, harvest, equipment, dispensers, pots, entities, carve, brush) — but
  the list beside it named twelve, missing `entities`, which is the sheep
  colour set (`BuiltInLootTables.java`:78-80). The list now names it.
- **`contexts-and-predicates`: the keys `ALL_PARAMS` omits.** L109-112 names
  the four keys the set leaves out and the consequence sentence beneath it
  named three, silently dropping `LootContextParams.ENCHANTMENT_LEVEL`.
  `LootContextParams` declares fifteen keys and `ALL_PARAMS` requires eleven
  (`LootContextParamSets.java`), so all four behave alike. The consequence now
  names four.
- **`enchanting` against `enchantments`: the anvil's two book tests.**
  `enchanting`:158 said the anvil tests `Items.ENCHANTED_BOOK` by identity;
  `enchantments`:300 said it tests `DataComponents.STORED_ENCHANTMENTS`
  instead. Both are true of *different slots*: `AnvilMenu.java`:204 tests
  `input.is(Items.ENCHANTED_BOOK)` on the left-hand target, and
  `AnvilMenu.java`:145 tests `addition.has(DataComponents.STORED_ENCHANTMENTS)`
  on the right-hand addition for the halved price. Neither page said which
  side; both now do.
- **`enchantments`: what cooks the loot.** "That is a loot-table condition on
  `EnchantmentTags.SMELTS_LOOT`" named the guard, not the mechanism. In the
  data the cooking is the `minecraft:furnace_smelt` function
  (`SmeltItemFunction`) behind an `any_of` condition testing *this* entity's
  on-fire flag or the direct attacker's main-hand enchantment tag
  (`data/minecraft/loot_table/entities/cow.json` and its siblings, built by
  `EntityLootSubProvider.java`:60). `EnchantmentTags.SMELTS_LOOT` has one
  member, Fire Aspect (`VanillaEnchantmentTagsProvider.java`:35). Now the
  function is named and the condition is described as the guard.
- **`foundations/resource-system`: a missing step in the reload's completion
  list.** The row said `PlayerList.reloadResources` "re-reads every player's
  advancements and broadcasts `ClientboundUpdateTagsPacket` and
  `ClientboundUpdateRecipesPacket`". It also calls
  `ServerRecipeBook.sendInitialRecipeBook` for every player
  (`PlayerList.java`:956), which is what makes `recipes`:74's claim about
  shifted display ids true. The step is now in the list.
- **`items/README`: two claims the part's own pages contradict.** "the three
  engines … hand each other nothing" — two of enchanting's five paths are loot
  functions (`enchanting`:332-347), `RepairItemRecipe` carries curses
  (`enchanting`:21-23), and the recipe auto-fill refuses enchanted stacks
  (`recipes`:320-327). And "the sword that swings before the server has heard
  about it" is `player/the-sword-swing`'s hook, in Part VIII, and no page of
  this part pays it off. Both replaced.
- **`using-an-item`: `Item.APPROXIMATELY_INFINITE_USE_DURATION` "in all but
  name".** The constant exists (`Item.java`:119) and has no reader in the tree;
  `BowItem.getUseDuration` and the base body both write the literal. Now stated
  that way, in the new roster paragraph.

### Suspicions re-derived and found sound (a strike is a claim)

- `items-and-stacks`' *two spellings*: the reload-time validator installed by
  `Item.Properties.finalizeInitializer` reads `DataComponents.DAMAGE`
  (`Item.java`, the `addValidator` lambda), and `ItemStack.validateComponents`
  reads `DataComponents.MAX_DAMAGE` (`ItemStack.java`:245-247). The two really
  are different components, and the section's hook stands.
- `containers-and-menus`' mount-menu generalisation:
  `AbstractMountInventoryMenu.java`:20 passes `(MenuType) null` to super, and
  `ServerPlayer.openHorseInventory` sends `ClientboundMountScreenOpenPacket`.
  `AbstractChestBoat.openCustomInventoryScreen` calls `player.openMenu(this)`
  and is not a mount menu, which the page now says so a reader crossing to
  `client/gui-and-screens`' wider `HasCustomInventoryScreen` claim is not
  confused.
- `recipes`' "the server re-sends the player's whole book": true, and the gap
  was on `resource-system` (above).
- `using-an-item`'s two `completeUsingItem` spellings:
  `ServerPlayer.completeUsingItem` sends event 9 and calls super
  (`ServerPlayer.java`:1704-1711); `Player.handleEntityEvent` calls
  `completeUsingItem` on id 9 (`Player.java`:404-407). Both sentences correct.
- `enchantments`' `RegistrySynchronization.packRegistry`: a real private
  per-registry method (`RegistrySynchronization.java`:34) beside the public
  `packRegistries` loop (:28). Two methods, two pages, no drift.
- `enchanting`'s "the grindstone and the providers call
  `EnchantmentHelper.updateEnchantments` themselves": the provider path reaches
  it through `EnchantmentHelper.enchantItemFromProvider`
  (`EnchantmentHelper.java`:708-717), which is inside the helper. The
  three-way split of write entry points stands.
- `items/README`'s "enchantments are a world-load dynamic registry that
  `/reload` never re-reads": `Registries.ENCHANTMENT` and
  `Registries.ENCHANTMENT_PROVIDER` are both in
  `RegistryDataLoader.WORLDGEN_REGISTRIES` and neither is in
  `RegistryLayer.RELOADABLE`. Sound — and the claim now has a home on
  `enchantments`, which is the new claim below.

### Claims this session introduced

- **`items-and-stacks`' new hook**: durability is the one thing a client never
  predicts, because `ItemStack.hurtAndBreak`'s working overload demands a
  `ServerLevel` and the `LivingEntity` overloads silently do nothing without
  one. (The page already carried the fact at its old L256-259; it is now the
  opening claim.)
- **`items-and-stacks`**: `ItemStackTemplate` holds a raw, never-sanitised
  patch, so it is the one thing that can carry a value equal to the item's own
  default and send it verbatim (moved from `data-components`, which stated the
  premise without the consequence). The validator section gains the
  one-level/nesting-not-followed rule and the bundle-weight test, both moved
  from `data-components`. New family sentence: the ninety-eight remaining
  `world/item` classes exist for a behaviour hook no component can express,
  and `AxeItem`/`ShovelItem`/`HoeItem` survive for block-side verbs.
- **`data-components`**: the twenty `delayedComponent` call sites and their
  roster, `Item.Properties.repairable` as the eager near miss, and the
  class-init half of the two-phase build (all moved from `items-and-stacks`);
  the claim that the deferral exists for twenty entries and everything else is
  deferred with them because the map is built in one pass.
- **`containers-and-menus`**: `ContainerLevelAccess.NULL` runs nothing and
  returns an empty optional, so a client menu's body is skipped wholesale and
  only the guard in front of it is real (moved in from `recipes` and
  `enchanting`); the menu-open sequence in order (moved in from `loot-tables`);
  a menu-button click is the third place a broadcast happens and does not wait
  for a phase (moved in from `data-components`); the twenty-nine-menu family
  sentence; `AbstractMountInventoryMenu` and the chest-boat exception; a
  `DataSlot` is either a `shared` view or a `standalone` int and each costs its
  own packet (moved in from `enchanting`).
- **`recipes`**: the nine `CustomRecipe`s named (verified against the tree —
  `BannerDuplicateRecipe`, `BookCloningRecipe`, `DecoratedPotRecipe`,
  `FireworkRocketRecipe`, `FireworkStarFadeRecipe`, `FireworkStarRecipe`,
  `MapExtendingRecipe`, `RepairItemRecipe`, `ShieldDecorationRecipe`), with
  `RepairItemRecipe`'s curse behaviour named so `enchanting`'s hand-forward is
  paid; `SingleItemRecipe`, `SmithingTransformRecipe` and `SmithingTrimRecipe`
  named as the stations' recipe shapes; the claim that the ordinary route into
  the recipe book is an advancement reward rather than a craft.
- **`using-an-item`**: the whole `Item.getUseDuration` roster — the base body's
  three-way answer (a `Consumable`'s ticks, else the hour for
  `BLOCKS_ATTACKS`/`KINETIC_WEAPON`, else zero) and the eight overrides with
  their numbers, `EnderEyeItem`'s zero making it the one item instant by
  declaration. (§7's *lost prose* entry, discharged.)
- **`enchantments`**: the new reload paragraph (above); the anvil's
  addition-side test named as such; `SmeltItemFunction` named;
  `LootItemRandomChanceWithEnchantedBonusCondition` moved in from `loot-tables`
  so the Fortune/Looting answer names all four classes.
- **`enchanting`**: the four `selectEnchantment` callers and the two paths that
  roll their own (the correction above, stated positively); the anvil's
  left-slot/right-slot split; `Registries.ENCHANTMENT_PROVIDER` as a
  world-load registry and `EnchantmentProviderTypes` as its dispatch;
  *local difficulty* replacing *regional difficulty*, which is the book's term
  everywhere else.
- **`contexts-and-predicates`**: the six `LootContextUser` sub-interfaces named
  (verified: `SlotSource`, `LootItemFunction`, `LootItemCondition`,
  `NbtProvider`, `NumberProvider`, `ScoreboardNameProvider`); the `SlotSource`
  family — six registered kinds, answering a `SlotCollection`, with `SlotLoot`
  its one consumer; `LootContext.popVisitedElement` and
  `LootContext.Builder.withOptionalRandomSeed` moved in from `loot-tables`;
  `AbstractVillager.addOffersFromTradeSet` moved into the sequence sentence;
  the claim that a registry's tags load before its elements are validated, so a
  predicate naming an item tag has it resolved by validation time.
- **`loot-tables`**: `SequenceFunction` named as the forty-third function, the
  one that is not a `LootItemConditionalFunction` (verified against
  `LootItemFunctions`); `LootPoolEntry` named as the candidate the funnel
  weighs; `SetContainerLootTable` and `SetContainerContents` named as where a
  `SeededContainerLoot` comes from; the claim that no client class references
  the loot package at all (moved from a clause to the section's punchline).
- **`items/README`**: the whole *Where the part stops* section is new — the
  size through the include, the four family sentences, the four declines
  (villager trading, brewing, the creative tabs, armour identity and trims),
  and the *an item is where another system surfaces* claim with its five
  examples. The shape paragraph's engines-touch-at-the-boundaries claim, with
  its three crossings, replaces "hand each other nothing".
- **`data-driven-types`**: *The run half* now stops at the object existing and
  cites `loot-tables#one-roll-drawn`; seven *taught in* cells re-pointed
  (`LOOT_CONDITION_TYPE`, `LOOT_NUMBER_PROVIDER_TYPE`, `LOOT_NBT_PROVIDER_TYPE`,
  `LOOT_SCORE_PROVIDER_TYPE` and `SLOT_SOURCE_TYPE` to
  `contexts-and-predicates`; `ENCHANTMENT_PROVIDER_TYPE` to `enchanting`;
  `CONSUME_EFFECT_TYPE` to `using-an-item`). Each cell is a claim about which
  page names the element; each was checked by grep before it moved.
- **Anchors**: forty-six cross-part links in Part VII carried two anchors before
  this session and now carry them throughout. Every anchor is an implied claim
  that the named section is the answer; `check_links.py` proves the anchor
  exists, not that it answers.

## Pass 5, session F — Part VI · Entities *(2026-09-05)*

Pages rewritten: all nine of Part VI (`entities/README`, `entity-anatomy`,
`authority`, `entity-lifecycle`, `synched-entity-data`, `attributes`,
`movement-and-collision`, `ai-goals-and-brains`, `pathfinding`,
`damage-and-death`) and the part's Reference page
`reference/non-living-damage`. Four pages in three other parts edited because
a Part VI page's owner or duplicate lived there: `server/server-level-tick`,
`world/points-of-interest`, `foundations/text-components`, plus
`src/lectures.md`.

### Corrections — every one re-derived against the decompile

- **`authority`:113-122 put a player's own physics in the wrong phase.** The
  page had the server's copy running `LivingEntity.travel` "during the entity
  phase of its tick". `ServerPlayer.tick` — the half the level's entity loop
  calls — does **not** call the superclass tick (`ServerPlayer.java`:653); the
  half that does is `ServerPlayer.doTick` (`:725`, calling up at `:728`), whose
  only caller is `ServerGamePacketListenerImpl.tickPlayer`
  (`ServerGamePacketListenerImpl.java`:323), which runs in the *connection*
  phase — `MinecraftServer.tickChildren` ticks every level and only then calls
  `tickConnection` (`MinecraftServer.java`:1228-1254). `the-two-phase-tick`
  had it right all along, which makes this a page contradicting its own owner.
- **`authority`:121-122 misattributed the discard.** It had the next
  `ServerboundMovePlayerPacket` overwriting the server's simulated position.
  The discard is inside the bracket: `tickPlayer` records the position, calls
  `doTick`, then snaps straight back to the recorded one with `Entity.absSnapTo`
  (`ServerGamePacketListenerImpl.java`:319-325). Both are cut to a citation of
  `the-two-phase-tick#the-bracket-and-what-survives-it`.
- **`authority`:181-183, "three of those eight read the same member".** True
  but the weaker of two readings, and the page's own bullet list shows the
  stronger. Counted in the source: `Entity.move` reads
  `Entity.isLocalInstanceAuthoritative` three times and
  `Entity.canSimulateMovement` once; `LivingEntity.aiStep` reads
  `canSimulateMovement` twice, `Entity.isEffectiveAi` twice and
  `isLocalInstanceAuthoritative` once — eight call sites, one of which reads a
  pair, so **four** read the root predicate, three `canSimulateMovement`, two
  `isEffectiveAi`. (This is [pass5.md](pass5.md):706, struck.)
- **`authority`:104-106 was too strong about `Entity.move`.** "the only thing
  that would is `Entity.move`, which on this side only `LivingEntity.travel`
  reaches" — `PistonMovingBlockEntity.java`:191 and
  `ShulkerBoxBlockEntity.java`:143 both call the mover directly, and block
  entities tick on the client. Scoped to *nothing in the mob's own tick*, which
  is what `movement-and-collision`:36-37 already said; the two pages disagreed.
- **`attributes`:116-119 said the same clause twice and got the third wrong.**
  "overrides the attack damage the monster builder added, the follow range the
  mob builder added and the follow range the mob builder added — the movement
  speed it also declares has no earlier entry to beat".
  `Zombie.createAttributes` (`Zombie.java`:132-134) names five;
  `LivingEntity.createLivingAttributes` (`LivingEntity.java`:334-336) already
  contains **both** `Attributes.MOVEMENT_SPEED` and `Attributes.ARMOR`, so four
  of the five are overrides and only `Attributes.SPAWN_REINFORCEMENTS_CHANCE`
  is new. The page contradicted itself fifteen lines later, where `Mannequin`
  gets "the plain living set, including the registry's default movement speed".
- **`damage-and-death`:158-161 had the invulnerability window backwards.** It
  said the red flash is "only half the window" and "the other half is the
  silent one". `LivingEntity.hurtServer` takes the partial branch on
  `invulnerableTime` still being above ten (`LivingEntity.java`:1281), and a
  full hit sets that counter to 20 and the flash to 10 together — so the excess
  rule applies in exactly the ten ticks the flash is *showing*, and the second
  ten protect nothing at all. The page's own hook, its figure node N3 and the
  landing page all had it right; this paragraph alone had it inverted.
- **`entity-anatomy`:212 glossed `entity/schedule` as "villager day plans".**
  The package holds `Activity.java` and `package-info.java` and nothing else;
  the day plan is a `Timeline`. The gloss read as the opposite of
  `ai-goals-and-brains`' hook, which is that *Schedule* does not exist in 26.2.
- **`reference/non-living-damage`:8, "twelve of the rows below inherit it
  unchanged".** Thirteen. There are nine declarations of `Entity.hurtClient`,
  one of them the base default; seven of the eight overriders are rows in this
  table (`RemotePlayer` is a `LivingEntity`), `MinecartTNT` inherits
  `VehicleEntity`'s, and 21 − 7 − 1 = 13. ([pass5.md](pass5.md):578 carried the
  same wrong arithmetic and is corrected in place.)
- **`reference/non-living-damage`:46 compressed the creative branch past
  truth.** "a creative player skips to `Entity.discard`" —
  `VehicleEntity.hurtServer` (`VehicleEntity.java`:36-73) applies the hurt
  direction, the hurt timer, `Entity.markHurt` and the ×10 accumulator *before*
  the creative test, which only redirects the destruction.
  `damage-and-death`:384-386 had it right; the catalogue contradicted its own
  lecture.
- **`ai-goals-and-brains`:383 said "everything it will ever do".** A zombie
  gains a thirteenth goal outside `Mob.registerGoals`:
  `Zombie.setCanBreakDoors` inserts a `BreakDoorGoal` at priority 1
  (`Zombie.java`:152-166), rolled at spawn against local difficulty (`:493`).
  The page's own general section eleven lines earlier already allowed for
  "the few mobs that add or remove a goal on a state change".
  ([pass5.md](pass5.md):703, struck.)
- **`ai-goals-and-brains`:341-348 had a dangling *the three*.** Five of the ten
  villager packages carry no `UpdateActivityFromSchedule`: core, panic and hide
  have nothing at priority 99, pre-raid and raid have `ResetRaidStatus` there
  (`VillagerGoalPackages.java`:35-101). The page then gave three escape hatches
  for what read as those five. Core needs none — it is always active alongside
  one other activity — so the pinning applies to the other four.
- **`movement-and-collision`:369 counted ticks where the code counts gated
  calls.** `ServerEntity.teleportDelay` is incremented at
  `ServerEntity.java`:170, inside the interval gate that opens at `:137`, and
  tested against 400 at `:182`. `what-the-client-is-told`:161-164 already said
  so; for an entity on the default interval the real bound is at least 1,200
  ticks.
- **`movement-and-collision`:379-380 named the wrong branch.**
  `LivingEntity.aiStep` opens with an interpolate branch and an *else if* that
  scales the stored delta by 0.98 — the handler is the interpolate branch and
  the 0.98 decay is the coast branch, which `authority`:102-106 had right.
- **`damage-and-death`:322 handed the respawned object to the wrong page.**
  `player-anatomy`:213-216 itself says `players-and-sessions` owns it; the
  section is
  `players-and-sessions#the-object-and-the-reference-that-outlives-it`.
  ([pass5.md](pass5.md):220, struck.)

### Suspicions re-derived and found sound — a strike is a claim

- `synched-entity-data`:284-287 on `Entity.syncPosition` ("realigns the
  tracker's own counter") against `movement-and-collision`:373 ("forces the
  next send outright"). Both describe `ServerEntity.java`:133-135, which
  re-phases the tracker's tick count to the next multiple of the interval
  immediately before the gate — so the send does happen at that evaluation.
  Not a contradiction; `movement-and-collision` now uses the owner's wording.
- `synched-entity-data`:270-271's "seven of those… set *Integer.MAX_VALUE*"
  against `entity-anatomy`:383's `EntityTypes.AREA_EFFECT_CLOUD`. Both true:
  the seven are the area-effect cloud, the end crystal, both item frames, the
  leash knot, the lightning bolt and the painting, and 37 types set an interval
  at all. The gloss "item frames, paintings, leash knots and their kin" was
  loose, not wrong; the list now lives once, on `entity-anatomy`.
- `entity-lifecycle` "spends the chunk model throughout and links it nowhere"
  ([pass5-brief.md](pass5-brief.md) Part 4, session F's row): **overtaken**.
  The page links `chunk-anatomy` at :83 for the heightmap, and now with the
  anchor.
- `pathfinding`:99-102's villager follow range against `entity-lifecycle`:148's
  `Mob.finalizeSpawn` bonus: the sentence was about which of two numbers
  `PathNavigation.updatePathfinderMaxVisitedNodes` takes the larger of, and 48
  wins either way. Reworded to say the constructor sets it rather than that the
  attribute is untouched.
- `SleepInBed` "never times out": `SleepInBed.timedOut` returns false and the
  class overrides `Behavior.canStillUse` (`SleepInBed.java`:58, :95-98). Sound,
  and it is the page's own counter-example to the default.

### Claims introduced

- **`entity-anatomy`.** The non-living half of the tree, which the page had
  left to the atlas: `Projectile` with 26 descendants, `VehicleEntity` with 15,
  thirteen childless direct subclasses (the numbers are `maps/hierarchy`'s).
  `TamableAnimal` named as a rung, with an owner reference and a tame bit. The
  `Avatar` paragraph cut to the tree fact plus a citation of `player-anatomy`.
  The eight base synched accessors cut to a citation. `EntityType.trackDeltas`'
  ten-type list cut to a citation of `what-the-client-is-told` — the page's own
  cast promises it will not carry the packets after the first — and the seven
  *Integer.MAX_VALUE* intervals named in its place. The section heading *Three
  things about the id* renamed *The id, the box, and the numbers on the type*:
  it carried seven questions and only two were about the id (no page linked the
  old anchor).
- **`authority`.** "four other pages depend on it" replaced by four *parts* and
  the measured sixteen. `Player.isClientAuthoritative` named for the first time
  on the page three others cite for it. The `travelRidden` fork cut to the
  ninth predicate reading, the fork itself cited.
- **`entity-lifecycle`.** Two new passages. The species list has a data-driven
  override and a hard-coded one in front of it: `ChunkGenerator.getMobsAt`
  (`ChunkGenerator.java`:481-511) replaces the biome's list with a structure's
  `StructureSpawnOverride` for the first structure at the position that
  declares one for the category, by piece or by whole start; ahead of it
  `NaturalSpawner.isInNetherFortressBounds` (`NaturalSpawner.java`:305-315)
  returns `NetherFortressStructure.FORTRESS_ENEMIES` for `MobCategory.MONSTER`
  on `Blocks.NETHER_BRICKS` anywhere inside a fortress's bounds — a wider box
  than the fortress's own override, which declares the same list. And
  *findable* is now defined: entities live in `EntitySection`s keyed by
  `SectionPos`, held by `EntitySectionStorage`, each section carrying its own
  `Visibility` and a `ClassInstanceMultiMap`. Also: a raid named as a spawn
  source in *the other ways in*, and the overworld-only fact moved in from
  `server-level-tick`.
- **`ai-goals-and-brains`.** The leash given its own paragraph (it is a lever
  that takes `Goal.Flag.MOVE` away, not a control flag), with
  `Leashable.tickLeash` cited to `entity-anatomy`. A family paragraph for the
  two big libraries: 103 behaviour classes, 61 goal classes, 26 sensors,
  eighteen `*Ai` classes, each an instance of a shape the page has already
  described. `AcquirePoi`'s mechanics and `SleepInBed`'s entry conditions cut
  to citations of `points-of-interest`; the job-site half kept, because it is
  the villager's day, and `SleepInBed`'s never-times-out kept, because it is
  this page's counter-example.
- **`pathfinding`.** The budget's trigger, which the owner could not state:
  `Mob.onAttributeUpdated` on `Attributes.FOLLOW_RANGE` **or**
  `Attributes.TEMPT_RANGE`. `PathComputationType`'s three values, and that the
  four controls implement `Control` and re-specialise by movement mode the way
  the evaluators do. "unbounded by distance" moved in from `block-interaction`.
- **`damage-and-death`.** The non-living roster cut from five families naming
  all twenty-one classes to the argument plus four classes, and the heading
  renamed *Twenty-one classes with no pipeline at all* — the lecture and the
  catalogue had been partitioning the same twenty-one two ways (five families
  against six patterns, the lecture filing a forwarder under *destroys*). New
  section *Who gets the credit for a fall*, discharging the homeless
  fall-attribution threshold: `CombatTracker.getMostSignificantFall`
  (`CombatTracker.java`:114-150) credits the entry *before* the biggest fall
  unless the fall is first, keeps a `FallLocation`-carrying alternative, and
  returns nothing unless the fall exceeded five blocks or the alternative's
  damage did. The `Entity.hurtServer` side-enforcement stated in place instead
  of handed forward to `authority`, which never explained it.
- **`reference/non-living-damage`.** An `Entity.hurtClient` column, twenty-one
  rows, from the seven declarations plus the inherited default.
- **`server-level-tick`.** The census kept as the tick's own cost ("walking
  every entity in the dimension is what this step costs, once a tick") with the
  cap arithmetic cut to a citation.
- **`entities/README`, rewritten to the role.** New argument: five surprises,
  one question, asked about everything not in the grid. A *where the part
  stops* section with the size through the include — the largest part of the
  book — and the coverage answer: about 40% of its lines are named nowhere and
  that is right, because the bulk is one class per species. Four mechanisms
  declared too big for a sentence and sent to §7. `Avatar` corrected from
  "below `Player`" to **above** (four other pages say between `LivingEntity`
  and `Player`). The attribute-lag blurb corrected from "a tick late" to what
  `attributes` actually says, and the ids-stop-at-254 blurb from "the packet
  stops at 254". The pair claim for *synched entity data* ↔ *attributes* moved
  in from `lectures.md`, whose "first of the two channels" contradicted both
  the page and the landing figure's *one of six*.

### Anchors and citations

Part VI carried **no anchor on any of its 69 outbound links** before this
session — the same shape as Parts IV and V. Every link out of the nine pages
and the landing page now carries the owner's anchor where one answers the
sentence. The 22 inbound links to `authority` from sixteen pages are still
bare; the ones from Parts VIII, IX and X are sessions H, I and J's.

### The tool bug — the eighteenth of the project

`map_source.spec_text` rendered a part's package set inline, so a subtracted
package followed by additions read as though *minus* governed the whole tail.
Part VI printed as "`world/entity`, minus `world/entity/player`,
`network/syncher`, `world/level/pathfinder`, `world/damagesource`,
`world/effect`" — four packages the part **includes**, shown as exclusions —
and Part IX had the same shape. Published on `maps/packages.md` and copied
into every part's coverage report header, where two agents caught it
independently. Subtractions now come last and share one *minus*, and
`map_source.py --probe` proves the three shapes.

## Pass 5, session E — Part V · Blocks *(2026-09-05)*

Pages rewritten: all seven of Part V (`blocks/README`, `blocks-and-states`,
`block-interaction`, `block-breaking`, `block-entities`, `signal-and-dust`,
`pistons-and-block-events`, `diodes-and-observers`) and the part's Reference
page `reference/block-update-flags`. Four pages in three other parts edited
because a Part V page's owner or duplicate lived there: `world/scheduled-ticks`,
`server/server-level-tick`, `networking/what-the-client-is-told`,
`reference/glossary`, plus `src/lectures.md`.

### Corrections — decompile open

- **`reference/block-update-flags`, bit 4.** The row said
  `Block.UPDATE_INVISIBLE` "suppresses whichever of those the side does",
  i.e. on both sides. `Level.java`:237 is the only reader of bit 4 in the
  game and the test sits inside the client-side arm:
  `(updateFlags & 2) != 0 && (!isClientSide() || (updateFlags & 4) == 0) &&
  (isClientSide() || chunk.getFullStatus()…)`. The server's extra condition is
  the chunk status, never bit 4, so a *server* write carrying bit 4 still
  broadcasts. The row now says so. `blocks-and-states`:291-295 already had it
  right, so this was a Reference page contradicting its own lecture.
- **`world/scheduled-ticks`, `DiodeBlock.shouldPrioritize`.** The deleted
  paragraph said `TickPriority.EXTREMELY_HIGH` is picked "when the block it
  powers is itself a diode **that is not pointing straight back at it**".
  `DiodeBlock.java`:214-219 returns `isDiode(oppositeState) &&
  oppositeState.getValue(FACING) != direction`, where `direction` is the way
  this diode outputs and a diode's *FACING* points at its **input**. A diode
  pointing straight back at this one has *FACING* equal to
  `direction.getOpposite()`, so it satisfies the test — the condition was
  inverted, and the excluded case is the diode aimed the *same* way. The
  surviving copy, `diodes-and-observers`:123-126 ("a diode whose own input is
  not on the far side of it"), is right and stands.
- **`blocks/diodes-and-observers`:177-179 was self-contradicting.** It said
  `RepeaterBlock.LOCKED` "is the only diode property computed from a redstone
  reading *outside* tick time — `DiodeBlock.POWERED` is the only one computed
  from a reading at all", which denies its own first clause.
  `RepeaterBlock.java`:98 declares four properties and exactly two are computed
  from a reading: *POWERED* at tick time (`DiodeBlock.tick`) and *LOCKED* inside
  `RepeaterBlock.updateShape`:61-62. Rewritten to say two, and that the
  difference between them is *when*.
- **`blocks/block-interaction`, the `isDestroying` gate.** The page had
  `Minecraft.rightClickDelay` set "only when `MultiPlayerGameMode.isDestroying`
  is false", which reads as a condition on the assignment.
  `Minecraft.java`:1880-1883 wraps the **whole method body** in
  `if (!this.gameMode.isDestroying())`, so a use press arriving mid-dig is
  discarded entirely rather than merely losing its delay.
  `client/prediction-and-acks`:243-244 already said "gated on", so this was a
  Part V page understating what a Part X page had right.
- **`blocks/signal-and-dust`, "All three stop early".** The sentence followed a
  table whose three rows are three *direction arrays*, two of which
  (`NeighborUpdater.UPDATE_ORDER`, `BlockBehaviour.UPDATE_SHAPE_ORDER`) do not
  stop early at all — they are fan-out orders. The claim is true of the three
  *reading methods* named inside the first row:
  `SignalGetter.getBestNeighborSignal` and `SignalGetter.getDirectSignalTo`
  return at ≥ 15 (`SignalGetter.java`:22-30, 86-88) and
  `SignalGetter.hasNeighborSignal` at > 0 (:73-74). The antecedent is now the
  methods, and the sentence says explicitly that a fan-out never stops early.
  This is [pass5.md](pass5.md):727's second half, confirmed.
- **`reference/glossary`, *Block event*.** Said the queue means a block event
  "lands late, usually within the same tick", which inverts
  `pistons-and-block-events`' argument ("a block event is a tick late" is only
  sometimes true; the queue is a wait for a named phase, not a delay). The
  entry now says a wait for a phase, and carries the owner's anchor. The page
  won, per the summariser rule.

### Suspicions re-derived and found sound — a strike is a claim

- `blocks-and-states`:288-290's re-mesh gate. An agent read it against
  `rendering/section-meshing` as a contradiction. Both are true: a client write
  goes through **two** doors — `Level.setBlocksDirty` →
  `LevelExtractor.setBlockDirty`, gated on `ModelManager.requiresRender`
  (`LevelExtractor.java`:463-466), and the bit-2 `sendBlockUpdated` →
  `LevelExtractor.blockChanged`, ungated (:437-438). The sentence is true of the
  method it names. Not changed.
- `blocks-and-states`'s `Block.UPDATE_LIMIT` against
  `block-interaction`'s `CollectingNeighborUpdater.maxChainedNeighborUpdates`.
  Genuinely two budgets: the first is the shape cascade's recursion depth,
  passed down `Level.setBlock`/`Block.updateOrDestroy` (`Level.java`:248-253),
  the second counts *requests* into the updater (`CollectingNeighborUpdater.java`:57-60).
  Both pages right; both now say which cascade they mean.
- `block-interaction`:151-156's priority-remesh claim. `LevelRenderer.java`:595-598
  is what reads `PrioritizeChunkUpdates` and sets `rebuildSync`; `Options.java`:952
  defaults it to *NONE* and `GraphicsPreset.java` sets *PLAYER_AFFECTED* in both
  fancy presets. The class and the preset claim are both right; a Part XI page
  describes the same switch differently and is the one to change (logged in
  [pass5.md](pass5.md) for session K).
- `block-entities`' three counts. `getUpdatePacket` overriders: **19**
  (20 files under `block/entity/` less the base). `getUpdateTag` overriders:
  **19** as well (18 under `block/entity/` plus `PistonMovingBlockEntity` under
  `block/piston/`; `TrialSpawnerStateData.getUpdateTag(TrialSpawnerState)` is a
  different signature, not an override). The two lists differ by exactly two,
  and they are the two the page names. Of the nineteen tag overriders,
  **thirteen** call `BlockEntity.saveCustomOnly`. `getUpdatePacket` has exactly
  **one** call site in the game (`ChunkHolder.java`:251). All four counts stand.
- `pistons-and-block-events`' *three blocks raise events directly*.
  `PistonBaseBlock`, `NoteBlock`, `PotentSulfurBlock` override
  `triggerEvent`, plus `BaseEntityBlock` (which forwards) and `ComparatorBlock`
  (dead, as the page says). Three is right; [pass3.md](pass3.md) §7's "four
  blocks" is the stale count and was carrying `ComparatorBlock`.
- `pistons-and-block-events`' `PistonMovingBlockEntity.deathTicks` of five.
  `PistonMovingBlockEntity.java`:312-313, `entity.deathTicks < 5`. Sound.
- `signal-and-dust`'s "for every wire but sometimes the first". True, and now
  precise: `ExperimentalRedstoneWireEvaluator.java`:48 sets bit 128 unless
  `shapeUpdateWiresAroundInitialPosition && initialWire`, and of the three call
  sites only `RedStoneWireBlock.onPlace`:302 passes true.

### Claims introduced

- **`blocks/README` — a new argument, and two new sections.** The opening now
  claims that a door's other half and a lamp's delay "are the same event
  underneath" and differ only by channel; that seven lectures is the fewest of
  any part this size *on purpose*; and that "the four kinds of answer a block
  can give" are a neighbour update, a shape update, a block event and a
  scheduled tick — a four the verified line already promised and no page
  enumerated. A *Where the part stops* section claims "about ten thousand
  lines" of the part's own two packages are taught elsewhere (the coverage
  tool's figure is 59 classes / 10,535 lines named only on other parts' pages)
  and names six destinations. The size sentence is now the include.
- **`blocks-and-states`** gains: the *state/properties* sub-package is "the axes
  and their values" and nothing else; `BlockPattern`/`BlockPatternBuilder` match
  an arrangement of `BlockInWorld` and are "how the game recognises a built
  wither or an iron golem"; `BlockStatePredicate` is "a `StateDefinition` turned
  into a test"; `InstantNeighborUpdater` is the other `NeighborUpdater` and is
  "used by nothing the game ships"; and the rail exception to
  `affectNeighborsAfterRemoval` is explained for the first time — a rail carries
  its geometry in a property, and `BaseRailBlock.affectNeighborsAfterRemoval`
  (`BaseRailBlock.java`:136-148) updates above when the old shape was a slope,
  and its own position and below when the rail is straight. It also receives
  the flags-3 and `GameEvent.BLOCK_DESTROY` detail moved off `block-interaction`.
- **`block-interaction`** gains the use-hook family: **25** blocks override
  `BlockBehaviour.useItemOn` and **52** `BlockBehaviour.useWithoutItem`
  (counted as files declaring the signature under `world/level/block/`, less the
  base declaration in `BlockBehaviour.java`), with six named examples and the
  claim that a block overriding neither "is not interactive at all". This
  restores the count [pass5.md](pass5.md):1734 asked for.
- **`block-breaking`** gains a paragraph claiming the two click lectures answer
  the same two gates oppositely, and that the reason is the pipeline: a
  placement's two corrective updates sit in one branch below the build-height
  test and go out for every outcome that reaches it, while a break has no such
  branch and each refusal decides for itself — three of the four sending the
  true state (`ServerPlayerGameMode.java`:165, 178, 189) and spawn protection
  sending only its message (:172-174).
- **`block-entities`** gains the hopper's cadence — one item then a cooldown,
  "two and a half items a second however often it is ticked", the eight written
  as a literal at both sites (`HopperBlockEntity.java`:130, 415) while
  `HopperBlockEntity.MOVE_ITEM_SPEED` is read nowhere — and the claim that every
  other block entity in the sub-package is the shapes on that page with
  different fields in the middle.
- **`signal-and-dust`** gains the sources family: `ButtonBlock` books a
  scheduled tick to turn off, `BasePressurePlateBlock` and its two subclasses
  re-read what stands on them, `DetectorRailBlock` and `TripWireHookBlock` watch
  for entities, `DaylightDetectorBlock` reads the sky
  (`DaylightDetectorBlock.java`:57-58 uses `getEffectiveSkyBrightness` and
  *SUN_ANGLE*), and the two torches invert what they are attached to — "none of
  them needs a section of its own". Its cast row is re-scoped to "the three
  answers *this trace* asks a state for", naming the analog pair as the
  comparator's ([pass5.md](pass5.md):727's first half).
- **`pistons-and-block-events`** names the seven block-entity raisers
  individually, claims "the other forty-odd block entities in the game raise
  none", names `PistonMath` as what computes the swept box
  (`PistonMath.getMovementArea`), and adds that `PistonMovingBlockEntity`'s
  `getUpdateTag` override means a player loading the chunk mid-push receives the
  placeholder and its cargo in the chunk packet — which pays off
  `block-entities`:52-54's citation, previously landing on a page that did not
  carry the fact.
- **`reference/block-update-flags`** gains a second table decomposing all four
  named combinations (3 = 1+2, 11 = 1+2+8, 260 = 4+256, 816 = 16+32+256+512,
  all read off `Block.java`:95-108) with a *where the book meets it* column
  claiming 260 and 816 are spent nowhere in the corpus; bit 128's row now says
  the skip is keyed on the **target** and that only the experimental evaluator
  sets it; and `Block.UPDATE_LIMIT`'s paragraph now names the distinction from
  the chain budget. Its opener stops enumerating three of the seven pages that
  spend a flag word.
- **`networking/what-the-client-is-told`** receives the fact that
  `ChunkHolder.broadcastChanges` "reads the level again when it builds the
  packet", so the set holds positions and not values and a whole cascade is
  broadcast as one state per position — moved from `signal-and-dust`, which
  stated it twice and now cites it once.
- **`world/scheduled-ticks`** now claims "a booking cannot be called off:
  nothing in the game cancels a single scheduled tick, the only removals being
  the bulk area operations" — `LevelTicks.clearArea`/`copyAreaFrom`, which the
  page describes thirty lines above. It also says a block *chooses* its
  priority from seven (`TickPriority.java`:7 declares seven values), where the
  page previously implied five.
- **`server/server-level-tick`**'s block-event section is cut to the phase
  claim plus a citation; it no longer states the queue's four rules.

### Anchors and citations

Thirty-seven links across Part V gained the owner's anchor — the part carried
none on any cross-part link before this session, the same shape session D found
in Part IV. One link was landing on the wrong page:
`blocks-and-states`:308-310 cited `signal-and-dust` for
`Level.updateNeighbourForOutputSignal`, which that page never names; it now
points at `diodes-and-observers#one-int-and-the-fan-out-that-exists-to-deliver-it`.
Six missing backward links added (feature flags from two pages, the level tick
from `block-entities`, `tickets-and-loading`'s number line, `pathfinding`'s
*one place the world pushes back*, `what-makes-a-sound`'s *who hears it*). Each
anchor asserts that the named section is the answer; `check_links.py` proves
only that the heading exists.


## Pass 5, session D — Part IV · The world *(2026-09-05)*

Eleven Part IV pages plus `reference/level-data-and-rules`, read by one agent
each; the part read end to end in watching order first. Four pages outside the
part were edited, each because a Part IV page disagreed with it:
`server/server-level-tick`, `server/server-tick`,
`networking/what-the-client-is-told`, `rendering/lightmap-fog-and-sky`. One
tool bug, and it had been hiding broken links.

### Corrections — every one re-derived against the decompile

- `world/chunk-anatomy`:247 said "Packing therefore buys a smaller palette,
  **not narrower entries**: unreferenced entries are dropped, which can demote
  a container a whole rung, and a `Configuration.Global` container shrinks from
  `Configuration.bitsInMemory` to `Configuration.bitsInStorage`." The head
  clause is false and the two tails contradict it.
  `PalettedContainer.pack` (`PalettedContainer.java:255-281`) re-encodes into a
  fresh `HashMapPalette`, asks `Strategy.getConfigurationForPaletteSize` for
  the *shrunken* palette's configuration, and writes at
  `Configuration.bitsInStorage`. `Configuration.Simple` reports one width for
  both (`Configuration.java:40-47`) and `Configuration.Global` two, so packing
  narrows entries in exactly two cases: a smaller palette landing a rung lower,
  and a global container's storage width. **Now:** what packing recomputes is
  the palette, and narrower entries are the consequence in those two cases,
  each named.
- `world/chunk-storage`:334 said `ImposterProtoChunk` "does not defer to the
  `LevelChunk` it wraps, which **only** `ImposterProtoChunk.markUnsaved` does".
  `ImposterProtoChunk.java:157-158, 248-254`: `markUnsaved`, `isLightCorrect`
  **and** `setLightCorrect` all delegate unconditionally, which
  `chunk-anatomy`:112 already said — the two pages disagreed. The two flat
  falses are `canBeSerialized` and `tryMarkSaved`
  (`ImposterProtoChunk.java:162-169`). **Now:** all three delegating members are
  named, both pages say the same thing, and `chunk-storage` cites
  `chunk-anatomy`'s anchor.
- `world/chunk-storage`:281 said loading "changes hands **four** times" and
  then named four stages. `ChunkMap.java:582-610` and `997-1001`: the stages are
  the IO lane, *upgradeChunk* and *parseChunk* on `Util.backgroundExecutor`, and
  `SerializableChunkData.read` on the main-thread executor — four stages across
  **three** lanes, two of them sharing one. **Now:** "four stages across three
  lanes", with the shared lane said out loud. The same sentence's
  `SimpleRegionStorage.upgradeChunkTag` is now `ChunkMap.upgradeChunkTag`, which
  is the call `ChunkMap.readChunk` actually makes (`ChunkMap.java:999`), so the
  two Part IV pages name one member for one hop.
- `world/scheduled-ticks`:81 said "**Two type parameters**, two parallel
  worlds". `LevelTicks.java:34`, `LevelChunkTicks.java:17`,
  `LevelTickAccess.java:5` and `ScheduledTick.java:8` each declare exactly one
  parameter. **Now:** "Two type *arguments*", with the one-parameter fact stated
  and `Block` and `Fluid` named as what fills it.
- `world/lighting`:184 said `LightEngine.checkNode` "only decides what to
  enqueue", two paragraphs before describing the sky engine writing stored
  levels. Both engines' `checkNode` writes: `BlockLightEngine.java:36`
  (`setStoredLevel(blockNode, 0)` when emission dropped below the stored level)
  and `SkyLightEngine.java:73`, plus `updateSourcesInColumn` →
  `removeSourcesBelow`/`addSourcesAbove` at `SkyLightEngine.java:108, 135`.
  **Now:** "zeroes the stored level where the light that is there must go and
  enqueues the rest as work".
- `world/fluids`:275 attributed lava's slope numbers through
  `WaterFluid.getSlopeFindDistance` while its own table at :338 used
  `FlowingFluid.getSlopeFindDistance`. `FlowingFluid.java:353` declares it
  abstract; `WaterFluid.java:86` and `LavaFluid.java:154` override.
  **Now:** `FlowingFluid.getSlopeFindDistance` in both places.
- `rendering/lightmap-fog-and-sky`:61 said the lightning layer lerps
  `EnvironmentAttributes.SKY_COLOR` "**a fifth** of the way";
  `environment-attributes-and-timelines`:92 says 22%. `ClientLevel.java:274` is
  `ARGB.srgbLerp(0.22F, …)`, so the owner page is right. **Now:** the rendering
  page's whole duplicate paragraph is one clause and a link, so the number is
  stated once.
- `networking/what-the-client-is-told`:368 said the once-a-second time sync
  "carries a game time plus **a map of clock updates**".
  `MinecraftServer.java:1299-1305` broadcasts
  `new ClientboundSetTimePacket(this.overworld().getGameTime(), Map.of())` — an
  **empty** map, which is what `environment-attributes-and-timelines`:221 says.
  **Now:** the networking page says the map is empty and that clock state travels
  only on a change or a join, with the owner's anchor.
- `reference/level-data-and-rules`:47 sent the reader to `server/server-tick`
  for day time; that page does not own it, `environment-attributes-and-timelines`
  does, and the environment page was claiming this Reference page pointed at it.
  **Now:** repointed to `#who-owns-the-clock`, so the hand-forward is paid.

### Suspicions re-derived and found sound — a strike is a claim

- `chunk-generation-pipeline`:190's "the dispatcher's own **four-slot** queue"
  is real: `ChunkTaskDispatcher.DISPATCHER_PRIORITY_COUNT` is 4 and the four
  users are resort 0, release 1, submit 2, poll 3
  (`ChunkTaskDispatcher.java:18, 38, 51, 63, 80`), so a re-sort really does
  outrank a new submission. Unchanged, and it is a *different* four from the
  ticket throttle's.
- `chunk-generation-pipeline`:211's two requirements on the centre chunk are
  both real and not in conflict: `ChunkGenerationTask.java:92-118` wants the
  persisted status at or past the target **and** every chunk of the loading
  pyramid's square at or past what its distance requires. Unchanged.
- `tickets-and-loading`:346's purge gate — "unless the level is frozen and
  chunk ticking is on" — is exactly `ServerChunkCache.java:328`
  (`runsNormally() || !tickChunks`). Unchanged; `server-level-tick`'s shorter
  "running" is a table compressing it.
- `scheduled-ticks`:364's "only `/clone` and the gametest framework do, in bulk"
  distributes correctly: `CloneCommands.java:248` calls `copyAreaFrom`, which
  only reads (`LevelTicks.java:301-326`), and `GameTestInfo.java:81` /
  `StructureUtils.java:107` call `clearArea`, which removes. Unchanged.
- `chunk-anatomy`:126's double-buffered added and removed sets really are
  `ClientChunkCache.Storage`'s fields (`ClientChunkCache.java:220-221`), with
  the accessors and `flipUpdateTrackingSets` on the cache. Unchanged.
- `points-of-interest`:316's "`PoiManager.loadedChunks` never forgets" holds:
  `PoiManager.java:49, 263` is a `LongSet` only ever added to. Unchanged.

### Claims introduced

- `world/README` — the header now says "the five pages off that line — what the
  place and the hour decide, and the four systems that make the world the line
  delivers feel alive", which is a claim that the environment page is neither
  conveyor nor side-system. A new ***Where the part stops*** section claims that
  about 2,900 lines of the part's packages are taught in six other parts, and
  names each family and its owner part; and it **declares the world border
  Reference-only**, with the reason (no scenario, and what a reader needs of it
  is enumerable). *Watch in this order* entry 1 no longer claims the environment
  page is "the one page here that depends on nothing else in the part" — it says
  *off the conveyor, ahead of it*, which is what the figure draws. Five blurbs
  re-synced word for word to their pages (fluids' two halves, chunk storage's
  "almost every write", the sensor's "at least one tick", the tickets page's
  "nothing asks for a chunk *because* it is loaded", chunk anatomy's *distinct*).
  The Reference list gains `reference/registries.md` with the claim that three
  of the part's mechanisms are registry-backed.
- `src/lectures.md` — Part IV's shape paragraph now counts the conveyor the way
  the landing page does (four pages plus a vocabulary page, not five), and
  lighting's blurb no longer says *self-contained*: it says nothing later in the
  part assumes it and Part XI does.
- `world/tickets-and-loading` — a new paragraph claims `ChunkResult` is the
  two-case type all three holder futures carry and that
  `ChunkHolder.UNLOADED_LEVEL_CHUNK` is simply its shared failure, whose message
  is *Unloaded level chunk*. The spectator answer gains a claim that the skip is
  **remembered** in a `PlayerMap` at join rather than re-asked. The renamed
  section *Which chunks a player is owed, and what makes one eligible* claims
  that the BLOCK_TICKING row is the join between the two systems — nothing is
  sent that the server is not also simulating.
- `world/chunk-generation-pipeline` — a new paragraph on the *EMPTY* step
  claims that a null parse and a thrown load both end at
  `ChunkMap.createEmptyChunk`, that the position is marked replaceable in
  `ChunkMap.chunkTypeCache`, and therefore that **an unreadable chunk is
  regenerated, not skipped**. Three passages cut to citations now claim their
  owners: the level→status line to `tickets-and-loading#the-number-line`, the
  synchronous ask to `#when-the-graphs-run`, the pool sizing to
  `anatomy#four-threads-worth-memorising` with the new claim that "the only knob
  is the pool's, and widening the pool widens everything else that shares it".
- `world/chunk-storage` — a new section *The other store under* data/ claims
  `SavedDataStorage` encodes on the caller's thread and writes on the IO pool,
  at most `Util.maxAllowedExecutorThreads` at a time, chained through
  `SavedDataStorage.pendingWriteFuture`, with `SavedDataStorage.saveAndJoin` the
  only wait — moved from `reference/level-data-and-rules`, which now cites it.
  A new section *Doing all of it at once, with no server running* claims
  `WorldUpgrader` runs one daemon thread named *World Upgrader*, hands each of
  the three stores to a `RegionStorageUpgrader`, optionally recreates region
  files (which compacts a fragmented save), and reports through
  `UpgradeProgress` — and that nothing there loads, generates or consults a
  status.
- `world/environment-attributes-and-timelines` — a new paragraph claims
  `ClockState` is the saved form and `PackedClockStates` the saved map,
  `ClockNetworkState` the wire form, that **the difference between the two is
  the paused flag**, and that `ClockManager` is a one-method interface which is
  why `AttributeTrackSampler` is the same class on both sides.
- `world/points-of-interest` — a new callout, ***A village is made of loaded
  sections only***, claims `PoiManager.isVillageCenter` alone in the query
  family reads through the non-loading `SectionStorage.get`, treats its null as
  *not a centre*, and that this is deliberate because the flood settles every
  tick and must not touch the disk.
- `world/scheduled-ticks` — the random-tick section is cut to the contrast and
  now claims two things as its own: that at the edge of simulation distance
  there is **a ring of chunks where appointments come due and nothing is chosen
  at random**, and that a random tick's eligibility is baked in at
  `BlockBehaviour.BlockStateBase.initCache` **before the world exists**, unlike
  an appointment, which is checked against the world when it comes due.
- `world/chunk-anatomy` — the ticker section, renamed *What step 11 leaves
  behind, and what the chunk goes on holding*, claims the handle belongs to the
  chunk and outlives the block entity in it. The step-8/9 paragraph now claims
  step 9 is "the only step whose whole job is to notice that the world moved
  underneath it".
- `world/fluids` — claims `LiquidBlockContainer` is the interface
  `SimpleWaterloggedBlock` narrows to water, and that the client holds the
  predicted bucket write until the acknowledgement arrives (a citation of
  `prediction-and-acks#the-six-windows`, added where the page previously said
  only "with no round trip").
- `world/lighting` — claims a section is not meshed at all until
  `LevelLightEngine.lightOnInColumn` is true for each of its eight surrounding
  columns, so a light flag decides whether a section may have a mesh (the same
  claim as before, now stated once and cited rather than told twice).
- `server/server-level-tick` — now claims `ServerChunkCache.tickChunks` reads
  `GameRules.RANDOM_TICK_SPEED` once per level tick and hands it down (the page
  previously attributed the read to `ServerLevel.tickChunk`); and its
  scheduled-tick section claims only what belongs to the tick — the two calls,
  their order and their budget — citing `scheduled-ticks` for the drain order
  and the cancellation rule.
- `reference/level-data-and-rules` — claims four parts point at it (III, IV,
  VIII, XII) where it previously named only Part IV and the level tick; claims
  *the border has no lecture* and says why. Its game-rule ids no longer carry
  hand-copied defaults, because `gamerules.md` generates them.
- **Eighteen cross-part and nineteen within-part citations gained the owner's
  anchor.** Part IV carried **none** before this session. Each anchor is a claim
  that the named section is the answer; pass 9 should spot-check that the
  section under each anchor says what the citing sentence says it says.

### The tool bug — the seventeenth of the project, and the first that was hiding failures

`tools/check_links.py` scanned each page **line by line**, and its link regex
cannot match across a newline. The corpus hard-wraps its prose, so a link
written as `[tickets and\nloading](…)` was invisible to the gate: **243 of the
corpus's 7,811 links had never been checked**, and one of them was broken by
this session's own heading rename — `server/server-tick`:225 pointed at
`tickets-and-loading#what-the-player-is-sent-and-when` after the heading
changed, and the gate said clean. Fixed by matching against the whole page
outside its fences with a character-to-line map, so a link is still reported on
the line its `[` sits on. On the first run the fixed gate caught **two** real
broken anchors — that one and `world/README`'s `#packing-a-position`, an anchor
this session had invented and which the old gate would have published. The
number of anchors the gate actually checks went from 12 at pass 5's planning
session to 174, which is mostly this pass's own anchor work finally coming under
the gate. `--probe` now writes a wrapped link with a bad anchor and a wrapped
link with a good one, and fails if either is misjudged.

**For pass 9:** every anchor added by pass-5 sessions A, B and C was written
while the gate was blind to wrapped links. They are checked now, but they were
not checked when they were written.

*(pass-5 sessions append below, newest first)*

## Pass 5, session C — Part III · The server *(2026-09-05)*

All six pages of Part III touched: `src/systems/server/README.md` (rewritten
to the landing-page role), `server-tick.md`, `server-level-tick.md`,
`players-and-sessions.md`, `starting-a-server.md`, `how-a-server-dies.md`.
Also one line each in `src/lectures.md` and `src/reference/README.md`.

### Corrections — re-derived against the decompile before the fix

- **`how-a-server-dies`: the autosave interval.** The page said the autosave
  runs "every 6000 ticks — five minutes of game clock, floored at 100 ticks".
  The decompile: `MinecraftServer.ticksUntilAutosave` starts at 6000 ticks
  (`MinecraftServer.java`:337) and is thereafter
  `computeNextAutosaveInterval` = `Math.max(100, (int)(ticksPerSecond *
  300.0F))` (`MinecraftServer.java`:1149-1162), i.e. **300 seconds of wall
  clock at the current rate**, not 6000 ticks and not game clock. Now "on the
  countdown the tick keeps … five wall-clock minutes, whatever the tick
  rate", citing `server-tick#the-bookkeeping-at-the-bottom`, which owns the
  arithmetic. This agrees with `server-tick`:403-412 and
  `chunk-storage`:311-316, which were already right.
- **`starting-a-server`: a missing management secret.** The page said
  `JsonRpc.create` "throws, ending the boot, if it is set and the secret is
  not forty alphanumeric characters rather than quietly going without one",
  which reads as *absent secret kills the boot*. The decompile:
  `DedicatedServerProperties`:132 resolves *management-server-secret* with
  `SecurityConfig.generateSecretKey()` as its **default**, and `Settings.get`
  puts the resolved value back into the properties map, which
  `DedicatedServerSettings.forceSave` writes — so an absent secret is
  generated and saved. `JsonRpc.create` throws only when the secret present
  fails `SecurityConfig.isValid` (non-empty, exactly forty alphanumerics —
  `SecurityConfig.java`:9-11). This also settles the disagreement with
  `what-this-book-skips`:180-181 ("generating one if absent"), which was the
  right half.
- **`starting-a-server`: what `DerivedLevelData` causes.** The page said the
  derived data is "why the time of day, the weather, the difficulty and the
  world spawn are one set of numbers every dimension shares". The decompile:
  `DerivedLevelData.java`:18-80 forwards game time, level name, game type,
  hardcore, allow-commands, initialised, difficulty and the difficulty lock,
  and swallows every setter but `setSpawn`. It carries **no** day time and
  **no** weather — day time is `ServerClockManager`'s and weather is one
  server-wide `WeatherData` — and the spawn a level reports comes from
  `MinecraftServer.effectiveRespawnData` through `ServerLevel.getRespawnData`
  (`ServerLevel.java`:1523-1524, `MinecraftServer.java`:1289-1292,
  1884-1885). Three of the four attributions were wrong; the paragraph now
  claims difficulty (and the rest of the forwarded set) and names the real
  owners of the other three, citing
  `level-data-and-rules#the-spawn-every-level-reports-is-the-servers-not-each-levels`.
- **`server-tick`: what ticks the `/schedule` queue.** The page said it
  "ticks from inside `ServerLevel.tickTime`, with the dimension's own game
  time". The decompile: `ServerLevel.tickTime` is wholly inside
  `if (this.tickTime)` (`ServerLevel.java`:458-466), the flag only the
  overworld is constructed with, and it passes the overworld's incremented
  game time to `getScheduledEvents().tick`. Now "which runs in the overworld
  alone and off the overworld's *gameTime*", citing the level tick. This was
  a disagreement with its own declared pair (`server-level-tick`:135-141),
  which was right.
- **`server-level-tick`: what the mob count walks.** The page said
  `NaturalSpawner.createState` walks every entity "skipping mobs that require
  persistence". The decompile (`NaturalSpawner.createState`) also skips every
  entity whose category is `MobCategory.MISC` — items, projectiles, armour
  stands — which is most entities in a busy world. Now states both skips.
  `entity-lifecycle`:41 had both and was right.
- **`server-level-tick`: the second chunk set.** The page said
  `ChunkMap.forEachBlockTickingChunk` walks the entity-ticking set and "each
  of those chunks gets `ServerLevel.tickChunk`". The decompile: it also drops
  any position whose `ChunkHolder` is absent or whose
  `ChunkHolder.getTickingChunk` is null. Now "keeps only those whose
  `ChunkHolder` has a live `ChunkHolder.getTickingChunk`".
  `scheduled-ticks`:295-297 had the filter.

**Re-derived and found sound** (a strike is a claim, so these are recorded
too): `starting-a-server`'s "the tickets the last shutdown parked" —
`TicketStorage.fromPacked` loads every persisted ticket into the
*deactivated* map, so "parked" is exactly the loaded state;
`players-and-sessions`' "`MinecraftServer.saveAllChunks` stamps the current
owner's id into the level data" — `MinecraftServer.java`:642-644 passes
`getSingleplayerProfile().id()` to `saveDataTag`; `server-level-tick`'s
`Player.isAlwaysTicking` — declared on `EntityAccess`, false on `Entity`,
overridden true on `Player` alone, so both this page's and
`entity-lifecycle`'s spellings are right; `server-level-tick`'s ticket-purge
gate — `ServerChunkCache.java`:328 is `runsNormally() || !tickChunks`, and
the page's scope is the level tick, where `tickChunks` is true;
`server-tick`'s *clocks* and *command functions* table rows — both guards are
inside the called method (`ServerClockManager.tick`,
`ServerFunctionManager.tick`), which is what the *skipped when* column
describes; the landing page's "five side threads" — `reference/threads.md`
has exactly five dedicated-only rows.

### Claims introduced

- **`src/systems/server/README.md` rewritten to the landing-page role.** New
  claims: the part's argument, that "almost everything surprising about a
  server's timing is the order of one method", and that a reader who finishes
  can answer *when* for four named things; the size paragraph, which is the
  atlas include plus "over half of those lines are
  `net/minecraft/server/level`'s forty-two classes, at nearly three hundred
  lines apiece" (42 / 11,977 from `map_source.py packages`); the pair claim
  moved in from `lectures.md` ("seven later parts assume one of them or the
  other"), which is `lectures.md`'s own count and is now stated once; a new
  *where the part stops* section, asserting that `ChunkGenerationTask`,
  `ChunkTaskDispatcher`, `ChunkTaskPriorityQueue` and `WorldGenRegion` belong
  to Part IV, `ServerPlayerGameMode` to Parts V and VIII, `ServerScoreboard`,
  `ServerFunctionLibrary` and `ServerAdvancementManager` to Part XIII, and
  `ReloadableServerRegistries` to Part II (each from the coverage report's
  *named on pages of other parts* table); and the *Game rules* line, now "the
  fourteen these five pages name, out of fifty-nine" — counted by grep over
  the five pages and against `gamerules.md`'s own 59.
  **Cut:** "a hopper moves one item per eight of them", which was true
  (`HopperBlockEntity.MOVE_ITEM_SPEED` is 8) and had no home but this
  summariser; logged to [pass5.md](pass5.md) for session E.
  **Moved out:** "a console command … is as late as the piston", now a
  sentence on `server-level-tick`'s broadcast section, where the rule it
  qualifies lives.
- **`server-level-tick`: two new passages.** A paragraph after the cast on
  what the abstract `Level` holds and leaves abstract, and what `ServerLevel`
  adds — the §7 gap, discharged; every member named was read
  (`Level.java`:110-134 for the fields, its nineteen abstract declarations,
  `ServerLevel.java`:202-216 for the four additions), and `getChunkSource` is
  deliberately *not* claimed for `Level`, because it is declared on
  `LevelAccessor`. And a sentence naming the tick's profiler zones in order —
  *world border*, *weather*, *tickPending* (*blockTicks*, *fluidTicks*),
  *raid*, *chunkSource*, *blockEvents*, *entities* (*dragonFight*,
  *checkDespawn*, *tick*), *blockEntities*, *entityManagement*,
  *debugSynchronizers* — read off `ServerLevel.tick`'s own `push`/`popPush`
  calls. Ten pages in five parts already cite these names; this is the first
  page that defines them.
- **`players-and-sessions`: three coverage additions.** The stored-user-list
  family (`StoredUserList` as a JSON file of `StoredUserEntry` records,
  subclassed as `UserBanList`, `IpBanList`, `ServerOpList`, `UserWhiteList`;
  `BanListEntry`'s source, reason and expiry; and **the expiry swept on
  read** — `StoredUserList.get` calls `removeExpired` before answering, so a
  temporary ban lapses when somebody asks rather than on a timer). The
  identity cache named as `CachedUserNameToIdResolver` over *usercache.json*
  with `ProfileResolver` behind it (`Services.java`:17-22). And
  `PlayerDataStorage`'s rescue, which the cast cell had promised and the page
  never gave: a failed *.dat* read copies the file aside under a
  *_corrupted_* name and then tries the *.dat_old* twin
  (`PlayerDataStorage.java`:69-114). The clause that a player with neither is
  "built from nothing, which is a new spawn rather than an error" is the
  session's inference from `load` returning empty, and is the line on this
  page to check hardest.
- **`starting-a-server`: one coverage addition.** `Bootstrap.bootStrap`'s
  last act installs `LoggedPrintStream` (or `DebugLoggedPrintStream` when
  debug logging is on) over `System.out` and `System.err`, keeping the
  original as `Bootstrap.STDOUT` — `Bootstrap.java`:39, 63-64, 146-155. That
  is why `Bootstrap.realStdoutPrintln` exists for the watchdog report.
- **Ownership cuts, each now one sentence and an anchored link.** The crash
  relay, from `server-tick` to `how-a-server-dies#the-crash-that-saves`
  (session B's ruling, applied); what a stopped server does with a submitted
  task, from `server-tick` to
  `how-a-server-dies#the-front-door-closes-the-guests-do-not-leave`, with
  *RejectedExecutionException* **moved** into that page rather than dropped;
  `session.lock`'s nature, from `how-a-server-dies` to
  `starting-a-server#taking-the-lock-and-fixing-leveldat-twice`; the
  `level.dat` write path, from both Part III pages to
  `level-data-and-rules#what-is-left-in-leveldat` (three tellings to one, and
  `how-a-server-dies` keeps `NbtIo.writeCompressed`, which the Reference page
  lacks); the ticket-persistence half, from `how-a-server-dies` to
  `tickets-and-loading#what-a-ticket-asks-for`, keeping only *why the drain
  loop ends*; *Done* against `MinecraftServer.isReady`, from
  `how-a-server-dies` to `starting-a-server#done-comes-before-the-loop`; the
  flush bracket and the 601st-call latency sweep, from `players-and-sessions`
  to `server-tick`; the per-chunk save spacing, from `how-a-server-dies` to
  `chunk-storage#the-four-moments-a-chunk-is-written`; the thread table's
  *what it may touch* framing, from `starting-a-server` to
  `reference/threads#the-threads-a-lecture-leans-on`. **Every trimmed
  sentence is a new claim** — pass 4's finding — and these are where to look
  first.
- **Seams repointed, which are claims about who owns what.**
  `starting-a-server`'s login-encryption hand-forward now goes to
  `protocol-phases#login` instead of `players-and-sessions`, which never
  explained it; `players-and-sessions`' two-place tick hand-forward now goes
  to `the-two-phase-tick#the-trace-one-player-one-tick-twice` instead of
  `player-anatomy`, which does not contain `ServerPlayer.doTick`; its
  permission-model link now goes to `permissions#where-a-set-comes-from`
  instead of `brigadier-and-commands`, which owns the packet and not the set;
  and `how-a-server-dies`' claim about connections with no `ServerPlayer` now
  cites `protocol-phases#configuration` rather than `players-and-sessions`.
- **`players-and-sessions`: `GameRules.KEEP_INVENTORY` re-scoped.** "decides
  only whether `ServerPlayer.transferInventoryXpAndScore` runs" is now
  "decides only whether `ServerPlayer.restoreFrom` runs" it, with a link to
  `damage-and-death` for what the same rule decides on the way out. The rule
  is read in three places (`ServerPlayer.java`:1749, `Player.java`:551 and
  `Player.java`:1609); the *only* was true of `restoreFrom` and read as
  global.
- **Anchors on twenty-eight outbound links across the six pages.** An anchor
  asserts that the named section is the answer; `check_links.py` proves the
  heading exists and not that it answers.
- **`src/lectures.md`** loses the pair claim (moved to the landing page), and
  its III-to-IV paragraph now says the level tick's first step "throws away a
  cache" rather than that its "first statement about the day-night cycle"
  rests on the environment page — the page's dependency is the cache, per
  `server-level-tick`:94-105. **`src/reference/README.md`** adds III to
  *Level data and rules*' parts column, which the landing page now points at.

### For pass 9's attention, found and not fixed

- `server-tick`:403-412 says the autosave countdown "starts at
  `MinecraftServer.AUTOSAVE_INTERVAL` (6000)". The value is right and the
  constant exists, but the constructor writes the literal 6000
  (`MinecraftServer.java`:337) and nothing reads `AUTOSAVE_INTERVAL` — a dead
  constant the page presents as the source of the number.
- `server-tick`:211-212 has `Connection.tick` flushing "at the end of the
  connection phase"; the flush is inside each connection's own tick, so it is
  true of the phase as a whole and not of any one call.
- `server-tick`'s *clocks* row gives *skipped when* as "frozen, or
  `GameRules.ADVANCE_TIME` is off", where only the first is a skip of the
  call and the second is a no-op inside it. Same shape as the *command
  functions* row, so the two are at least consistent.
- `commands/scoreboard-and-data`:277-278 says "a score set and a crash a tick
  later is a score lost", which contradicts `how-a-server-dies`' hook (a
  tick-loop crash writes what `/stop` writes) unless it means a watchdog kill
  or a *kill -9*. Session M's page, flagged in [pass5.md](pass5.md).

## Pass 5, session B — Parts I and II *(2026-09-05)*

Eleven pages read by one agent each, both parts read end to end, nine pages
rewritten (`anatomy/README.md`, `anatomy/anatomy.md`,
`anatomy/what-this-book-skips.md`, `foundations/README.md`,
`foundations/identifiers-and-registries.md`, `foundations/resource-system.md`,
`foundations/tags.md`, `foundations/codecs-nbt-json.md`,
`foundations/data-driven-types.md`) plus one-clause link edits on
`data-components.md` and `text-components.md`.

### Corrections — re-derived against the decompile before the fix

- `foundations/identifiers-and-registries.md` — said `MappedRegistry` "is
  keyed three ways (`byKey`, `byLocation` and the insertion-ordered
  `byId`)". **There are four.** `MappedRegistry.java:40` declares
  `private final Map<T, Holder.Reference<T>> byValue`, an `IdentityHashMap`
  built at :65 and written at :129; `getKey` (:141) and `getResourceKey`
  (:148) both read it, so the object-to-name direction goes through `byValue`
  and not through the three the page named. `toId` (:37) is the parallel
  identity map to the number. Now: four indexes, one per lookup direction.
- `foundations/codecs-nbt-json.md` — said `StreamTagVisitor` and its
  neighbours "let `NbtIo.parse` pull **two** fields out of a region chunk",
  then named three consumers. Two is right for one of them only:
  `IOWorker.java:105` builds a `CollectFields` of two `FieldSelector`s
  (*DataVersion*, *blending_data*); `StructureCheck.java:113` builds one of
  three (*DataVersion*, *Level/Structures/Starts*, *structures/starts*). Now
  stated as the mechanism — a `CollectFields` over whatever selectors the
  caller wants — with both counts attributed.
- **Checked and found correct, so no change:** `data-components.md`:183-191
  and `identifiers-and-registries.md`:306-311 were reported as contradicting
  each other on the singleplayer component binding. They do not.
  `ClientConfigurationPacketListenerImpl.java:177` passes
  `connection.isMemoryConnection()` as
  `tagsAndComponentsForSynchronizedRegistriesOnly`, and
  `RegistryDataCollector.java:166` negates it into `updateComponents`'
  `includeSharedRegistries` (:142-148), so a memory connection binds only the
  `RegistrySynchronization.isNetworkable` registries. Both pages say that.

### Claims introduced

- **A new section, `identifiers-and-registries.md` §*Feature flags: the same
  registry, narrowed*** — the largest new claim of the session, discharging
  a coverage entry. Each sentence, with where it came from:
  `FeatureFlagSet` is a *long* mask plus a `FeatureFlagUniverse`, cap
  `MAX_CONTAINER_SIZE` = 64 (`FeatureFlagSet.java:9-18`); one universe,
  *main*, and four flags — `VANILLA`, `TRADE_REBALANCE`,
  `REDSTONE_EXPERIMENTS`, `MINECART_IMPROVEMENTS` (`FeatureFlags.java:37-48`);
  `isExperimental` is "not a subset of `VANILLA_SET`" (:34-36);
  `FeatureElement` has one method and seven implementors — `Item`,
  `BlockBehaviour`, `EntityType`, `GameRule`, `MenuType`, `Potion`,
  `MobEffect`; `FILTERED_REGISTRIES` names those seven registries
  (`FeatureElement.java:10`);
  `HolderLookup.RegistryLookup.filterFeatures` returns *this* for a registry
  not in the set and a filtering delegate for one that is
  (`HolderLookup.java:82-87`); **"the registry underneath is not touched, and
  neither is its numbering — a disabled item keeps its wire id"** is the
  inference from that delegation and is the sentence most worth re-deriving;
  the consumers are `CommandBuildContext.java:22`, `GameRules.java:109`,
  `MinecraftServer.java:373` and `LevelReader.java:232-235`; the set is
  `WorldDataConfiguration.enabledFeatures`.
- **`resource-system.md`, the two `server/packs` corners** the skips page had
  been promising it: *linkfs* as `LinkFileSystem` / `LinkFSProvider` /
  `LinkFSPath`, and `DownloadQueue` — one directory per pack UUID, one at a
  time on a `ConsecutiveExecutor` over `Util.nonCriticalIoPool`, a
  `JsonEventLog` per attempt, and `DownloadCacheCleaner.vacuumCacheDir` at
  construction trimming to `MAX_KEPT_PACKS` = 20 (`DownloadQueue.java:37-47`,
  `DownloadCacheCleaner.java:30-60`). **"newest kept, one per directory
  before any directory's second"** is a reading of `prioritizeFilesInDirs` and
  the two comparators, and is the claim here to check.
- **`anatomy.md`, the packet-drain contrast.** The hop paragraph now ends
  "so a client at 200 frames a second takes the server's updates ten times
  more often than it ticks" — arithmetic over the page's own 20 Hz tick, and
  a restatement of `what-the-client-is-told.md`:442. Check the framing, not
  the numbers.
- **`anatomy.md`, the 1.21-era callout** was replaced: out went the
  `Gui`/`Hud` box (owned by `client/hud` and `reference/naming-drift`), in
  came `DeltaTracker` was *Timer*, which restates
  `reference/naming-drift.md`:52 and :68.
- **`anatomy.md`, `GameConfig`** — new clause: the client's `Main` parses its
  command line into a `GameConfig` the `Minecraft` constructor is built from.
  Closes the part's one coverage gap; check against `client/main/Main`.
- **`anatomy/README.md` is rewritten to the landing-page role** and its
  figure redrawn from the twelve other parts to the part's own two pages.
  New claims: that the part's argument is the two loops rather than "a server
  that ticks and a client that draws"; that the boundary page is second
  because a boundary is drawn before the investment (moved from
  `lectures.md`:466-468, which keeps it as an ordering claim); and *where the
  part stops*, which asserts that Parts III, IX and X take the three threads
  onward. The lane sentence is now "nearly every lane ... is a class, and the
  handful that are not stand for a thread", which is
  `reference/lanes.md`:5-10 and `check_lanes.py`'s own count (333 and 9).
- **`foundations/README.md`** — "Part II is not a stack but a fan ... the
  figure has two roots and no single column" replaces "Part II is a stack".
  A claim about the figure directly above it, and checkable against it.
- **`what-this-book-skips.md`, three reframings.** `com/mojang/blaze3d/audio`
  is no longer presented as skipped — `client/sound-engine` teaches all of it
  (its cast carries `Library` and `AbstractDeviceTracker`; :129 the thirty
  channels, :240 HRTF), so the section keeps only the address argument. The
  statistics page's criterion-parse paragraph became a citation of
  `scoreboard-and-data`:158-162, which owns it. The recipe book is stated as
  `items/recipes`' rather than as skipped. **The hatching in the generated
  treemap was not changed to match**, so the figure and the prose should be
  read together at pass 9.
- **Ownership moves that changed what a page asserts** (each now one sentence
  and a link where it was an explanation): the two tag tables, from
  `identifiers-and-registries` to `tags`; the GPU-backend retry order, to
  `rendering/the-window`; the crash relay, to `how-a-server-dies`; the
  empty-server pause, to `server-tick`; `MinecraftServer.spin`'s order, to
  `starting-a-server`; the Netty hop's mechanism, to `the-connection`. In
  each case check that the surviving sentence is still true on its own — a
  trimmed sentence is a new claim.
- **Outbound links gained anchors** across the nine pages. An anchor is a
  claim that the named section is the answer; all resolve under
  `check_links.py`, which proves the heading exists and not that it answers.

### Tool bug

- `tools/map_source.py` and `tools/pass5_coverage.py` reported different
  populations for the same packages — Part I as 7 classes / 6,770 lines and
  6 / 6,766 — while `map_source.py`'s own comment claimed they "can never
  disagree". The difference is `package-info.java`, which the atlas counts as
  a file and the coverage tool drops. No published page states either number
  today (Part I's landing page carries no size), so nothing false was
  published. Both tools now say which population they mean, and the false
  comment is gone. Every part with a `package-info.java` reads one class
  larger in the atlas than in its coverage report.

## Pass 5, session A — the standard *(2026-09-05)*

Three published pages rewritten — `src/lectures.md`, `src/SUMMARY.md` and
`src/systems/commands/README.md` — plus `TEMPLATE.md` and two tools. No
system page touched, no fact changed, and **no correction made**: nothing
this session read was found wrong against the decompile, and nothing was
re-derived, because every finding was about where a claim lives rather than
whether it is true. The claims introduced:

**`src/lectures.md`**

- The dependency table gained a **membership rule** and three rows and lost
  three. The rule is a claim about the corpus, checkable without the
  decompile: *a page two or more landing pages name under **before you
  start***, less `anatomy/anatomy`, `foundations/codecs-nbt-json` and
  `foundations/identifiers-and-registries`. `tools/check_deps.py` re-derives
  it on every run and fails on a mismatch, so pass 9's job here is to check
  the rule is the right rule, not the rows.
- Three new rows carry a new third-column phrase each, and each is a claim
  about why a part depends on the page, re-derived from the depending
  landing pages' own sentences: **`resource-system`** — "the staged load and
  its barrier: a server's own data at startup, where recipes and loot tables
  come from, and the reload the atlases are built by" (from `server/README`,
  `items/README`, `rendering/README`); **`data-driven-types`** — "the *type*
  field in a data-pack file and the registry it dispatches on; these two
  parts own most of its instances" (from `worldgen/README`,
  `commands/README`; the "most" rests on `worldgen/README`'s existing
  twenty-six-of-fifty-six claim); **`text-components`** — "what a chat
  message and a screen's label are before anything draws them" (from
  `networking/README`, `client/README`).
- "Watched straight through, the sidebar order still needs one departure
  from itself, and it is now as small as it can be" — the claim is that
  moving *environment attributes and timelines* to first in Part IV leaves
  exactly one out-of-order watch (Part IV lecture 1 before Part III lecture
  2) and that no other part's order departs. `check_deps.py` checks the
  three orders agree; the "one departure" is the session's own reading of
  the graph.
- **102 blurbs cut.** Each was a second copy of a line on a landing page.
  The ordering claims inside them were kept and are quoted unchanged; the
  descriptions were dropped, not moved, because the landing page has them.
  Pass 9 should read the kept clauses against the landing pages rather than
  against the source: the risk is a clause that lost its subject in the cut,
  not a fact that changed.
- The new second paragraph ("Because the subject here is the order, nothing
  below describes a lecture…") is a claim about the page itself.
- "one page until this pass" became "two pages that were one" — a
  pass-number rot fix, no claim.

**`src/SUMMARY.md`** — *environment attributes and timelines* is now first
in Part IV. Nothing else moved; no URL changed (mdBook derives the path from
the file, not the summary).

**`src/systems/commands/README.md`** (the exemplar landing page)

- The size sentence is now `{{#include ../../generated/part-commands.md}}`
  and reads **470 classes and 43,126 lines**, against the hand-count it
  replaced (473 / 43,900). The prose's population is now "the nine packages
  the atlas lists for this part", which is `map_source.PARTS` — check the
  nine, and the `#where-each-part-lives` anchor.
- New: "the command catalogue alone (`net/minecraft/server/commands`) is 102
  classes and 12,800 lines" — the old sentence said "a hundred command
  classes and 12,800 lines" without naming the package.
  `src/generated/packages-depth4.md` gives 102 / 12,781.
- New in the argument: "**None of those four needs any of the others.**" —
  moved up from the shape section, which says "none of them needs another".
  The sentence after it ("a reader who has those two can explain any of the
  four from them") is new and is a claim about the part, not about the game.
- **Cut, not moved**: "one of only two parts of a save that go through the
  data fixer as JSON, the other being advancement progress".
  `anatomy/what-this-book-skips`:252 owns it and this page links there.
- Three *before you start* links now carry an anchor
  (`server-tick#what-minecraftservertickchildren-runs-and-in-what-order`,
  `data-driven-types#the-idea-stated-once`,
  `the-connection#the-threads-underneath-it`). The claim in an anchored link
  is that the named section is where the thing is explained; all three were
  checked against the built heading ids.

**`TEMPLATE.md`** — two new sections, *One home per mechanism* and *The
landing page*. The only measured claim in them is the landing-page budget
("about a hundred lines plus the watch order"), derived from the thirteen
pages on 2026-09-05.

**`tools/check_deps.py`, `tools/verify_names.py`** — two new failing checks
and the index label; see `docs/pass5-brief.md` A5. A tool is suspected
first, twice over: `check_deps.py`'s membership check reproduced pass-4
session A's hand-found list exactly (three absent, three present that should
not be) before anything was edited, which is the evidence that it reads the
pages right; and `check_deps.py --probe` now proves both new checks fail on
the constructs they are for — a reordered sidebar, a short sidebar, a
qualifying page with no row, a row for a page one part assumes, a row for a
page nobody assumes, and a universal that takes a row — and pass on the
shapes they must accept.

## Pass 5, the planning session — between passes 4 and 5 *(2026-09-05)*

No system page rewritten. Three claims introduced, all in the frame and the
atlas:

- `src/introduction.md` — the *Verified means tested* paragraph now says
  "every link and anchor between pages is checked to land" and "a page that
  fails any of those does not go up": the claim is that `tools/check_links.py`
  runs in `tools/deploy.sh` before the build and exits non-zero on a broken
  link, anchor, include, `SUMMARY.md` entry or redirect (`tools/deploy.sh`,
  the line after `check_deps.py`).
- `src/maps/packages.md` — the *Where each part lives* table is now
  `src/generated/parts.md`, written from `map_source.py`'s `PARTS`. The
  mapping is a set of claims about which packages each part covers, and it
  differs from the hand table it replaced: Part IV adds `world/level/material`,
  `world/attribute`, `world/timeline`, `world/clock`, `world/level/border`;
  Part VI adds `world/damagesource`, `world/effect` and subtracts
  `world/entity/player`; Part II adds `world/flag`; Part IX subtracts
  `network/syncher` (Part VI's); Part X adds `client/input`, `client/server`
  and counts `net/minecraft/client` itself only; Part XI adds
  `client/particle`; Part XIII adds `server/permissions`, `server/bossevents`
  and `client/gui/screens/dialog`. The paragraph above the table says how
  it is counted (no prefix, *itself only*, shared packages counted twice,
  skipped packages left out) — check each against `map_source.in_part`.
  Every landing page's size sentence will quote its row once the part
  sessions switch them to the include; until then a landing page's hand
  count and its row may differ (Part XIII: 473 / 43,900 by hand, 470 /
  43,126 by the atlas).
- `docs/pass5-brief.md` Part 4 — the measured tables (coverage per part, the
  queue by kind, the duplication pairs) are the tools' output on 2026-09-05
  and are claims about the corpus on that day, not about the game; pass 9
  need not check them.
