# Pass 4 — the second fact-check (queue; opened 2026-09-02)

*Pass 4 re-runs pass 2's adversarial protocol — archived in
[pass2.md](pass2.md) with its twelve lessons — over the corpus pass 3
rewrote. This file is where pass-3 sessions write down what pass 4 must
check hardest: every page rewritten, every claim a rewrite introduced (a
hook, a redrawn ordering, a new section, a landing page's dependency list),
every diagram redrawn. Pass 4 checks everything anyway; this list decides
what it checks first. The charter is written by pass 3's closing session
(P) into [plan.md](plan.md).*

## How to write an entry

Per session: the pages rewritten; per page, the claims introduced (one line
each, quoting the sentence); the diagrams redrawn (which orderings they
assert); anything an agent drafted that the old page did not say. Newest
entry first.

## Standing items

- The landing pages and `lectures.md` are claims about order and
  dependency: check that every *before you start* link is actually assumed
  by the part, and that nothing earlier depends on something later.
- Every redrawn diagram: arrow by arrow, and every tick-boundary bar.
- The generated Reference views pass 3 adds (serializers, attributes, the
  glossary if generated): re-derive one sample by hand per view — pass 2
  found bugs in both generators, and one had reached the prose.
- The lane key in `TEMPLATE.md`: every lane's expansion is a class that
  exists. (If session A writes a lane linter, strike this.)
- Pass 2's twelve lessons apply unchanged; the shape to watch remains the
  confident sentence — orderings, "only", "never", counts, and "X, not Y".
- **Library facts are checkable now and were not in pass 2.**
  `reference/libs/` holds Brigadier, DataFixerUpper and authlib sources
  (`tools/fetch_libs.sh`) and `reference/26.2/assets/` the atlas, font,
  shader and post-effect JSON. Pass 2 took every claim about them on trust;
  pass 4 re-derives them, hardest on: `codecs-nbt-json` (DFU semantics —
  `DataResult` partials, `MapCodec`, `Lifecycle`), `protocol-phases` and
  `players-and-sessions` (authlib's session-server round trip),
  `chat-and-signing` (profile keys and signature validation),
  `brigadier-and-commands`, `execution-and-functions` and
  `scoreboard-and-data` (parse, suggestions, `ContextChain`, the result
  consumer), `models-and-atlases` and `text-and-fonts` (the atlas and font
  JSON), and whatever pass 3 writes about post-processing.
- **The `execute store` question** on `scoreboard-and-data` — what a failing
  ordinary leaf command writes — is now answerable from Brigadier 1.3.10;
  settle it and remove the page's "cannot be settled from the decompile"
  note.

## Entries

- **2026-09-02, session D — Part III The server.** Five pages: four
  rewritten (`server-tick`, `server-level-tick`, `players-and-sessions`,
  `starting-a-server` — the old `server-lifecycle`, renamed) and one written
  from the decompile (`how-a-server-dies`), plus a landing page and Part
  III's section of `lectures.md`. **Check `how-a-server-dies` hardest:
  nothing on it was fact-checked in pass 2**, and its drafting agent's claim
  list is the only record of where each sentence came from. Every rewrite
  was diffed against its old page from the agent's report before acceptance,
  and the corrections marked *(session-verified)* below were re-derived from
  the decompile by the session itself.
  - **Eighteen pass-2 errors found**, the largest crop since pass 2 itself,
    which says the "every page has a wrong claim" result survives one
    fact-check. Re-check each *fix*, not only the old claim.
    - `server-tick` said `MinecraftServer.scheduleExecutables` "rejects new
      work with a *RejectedExecutionException*". It returns false, and
      `BlockableEventLoop.execute` then runs the task **inline on the
      caller's thread**; the exception belongs to the separate
      `MinecraftServer.executeIfPossible`. *(session-verified)*
    - `server-tick` said a server "consistently 40 % late never says so".
      `MinecraftServer.nextTickTimeNanos` advances by a fixed amount every
      lap whatever the work costs, so lateness accumulates and the
      two-second threshold falls in about a hundred laps: such a server
      warns and skips repeatedly. The page's hook — log and skip are one
      condition, so a server that warned recently stays behind — is
      unaffected and stands. *(session-verified)*
    - `server-tick`'s `BlockableEventLoop.delayCrash` framing: the crash
      slot is a **static** field shared JVM-wide, the rethrow happens only
      on a loop built with *propagatesCrashes* (true for `DedicatedServer`,
      false for `IntegratedServer`), and every server-side caller uses
      `BlockableEventLoop.relayDelayCrash`.
    - `server-level-tick` drew and narrated `ServerLevel.runBlockEvents` as
      ungated. It is inside the freeze gate: a frozen world runs no block
      events. *(session-verified in `ServerLevel.tick`)*
    - `server-level-tick` gated `EnderDragonFight.tick` on the empty check
      alone; it is also behind the freeze gate. *(session-verified)*
    - `server-level-tick` mis-scoped both chunk-source gates. In
      `ServerChunkCache.tick` the purge is freeze-gated and
      `ServerChunkCache.runDistanceManagerUpdates` is not; inside
      `ServerChunkCache.tickChunks`, `Level.isDebug` wraps the **whole**
      body including `ServerChunkCache.broadcastChangedChunks`, so a debug
      world drops the block-change broadcast — which no page had said.
      *(session-verified)*
    - `server-level-tick` said `NaturalSpawner.createState` counts mobs
      "across `DistanceManager.getNaturalSpawnChunkCount` chunks". It walks
      `ServerLevel.getAllEntities`; the chunk count is only the cap's
      divisor. *(session-verified)*
    - `server-level-tick` had the light and block packets in the wrong
      order. `ChunkHolder.broadcastChanges` sends
      `ClientboundLightUpdatePacket` **first**, to the border players, before
      the changed-section walk begins. *(session-verified — and note that the
      drafting agent reported this correctly and then drew it wrongly in its
      own new diagram, which the session caught. Pass 4 should assume a
      redrawn figure can contradict the prose beside it, and read both.)*
    - `players-and-sessions` said `IntegratedPlayerList` "pins the view
      distance at 10, never sets a simulation distance at all (so a LAN
      world reports 0)". `IntegratedServer.tickServer` sets both from
      `Options` every unpaused tick, floored at 2, long before anyone joins.
      The claim is cut. *(session-verified)*
    - `players-and-sessions` said `MinecraftServer.getProfilePermissions`
      returns a `PermissionSet`; it returns a `LevelBasedPermissionSet`.
    - `players-and-sessions` said `PlayerList.respawn` chooses
      `Entity.RemovalReason.KILLED` or `CHANGED_DIMENSION`. The reason is its
      third **parameter**, chosen by
      `ServerGamePacketListenerImpl.handleClientCommand`, in the same call
      that selects `ServerPlayer.restoreFrom`'s branch. *(session-verified)*
    - `players-and-sessions` said a respawn "restarts the 60-tick timer".
      Death sets `ServerGamePacketListenerImpl.markClientUnloadedAfterDeath`,
      a flag the countdown never clears; the give-up-after-60-ticks rule
      belongs to the join alone.
    - `players-and-sessions` attributed the *bypasses-player-limit* read to
      `PlayerList.canBypassPlayerLimit`, a constant false on the base class;
      only `DedicatedPlayerList` reads the op entry.
    - `starting-a-server` said `DedicatedServer.convertOldUsers` returning
      false is the second way startup fails. It returns true if any of five
      conversions succeeded and only decides whether the name cache is
      saved; the boot-stopping gate is the separate
      `OldUsersConverter.areOldUserlistsRemoved`, over four files.
      *(session-verified)*
    - `starting-a-server` placed the *Done* log after query, RCON, the
      watchdog, JMX and the flush save. It is logged on the line after
      `MinecraftServer.loadLevel` returns, before all of them.
      *(session-verified)*
    - `starting-a-server` put `CrashReport.preload` "at the very top of
      `server/Main`"; version detection, the option parser, *--help* and
      *--pidFile* all precede it. And "about twenty" mutable
      `DedicatedServerProperties` fields is exactly nineteen.
    - the old `server-lifecycle` credited
      `DedicatedServer.fillServerSystemReport` with the whole report; it
      sets two details and everything listed belongs to
      `MinecraftServer.fillSystemReport`. Its `SuppressedExceptionCollector`
      sentence named packet handlers only: chunk load and chunk save
      failures feed it too.
    - the old `server-lifecycle` implied `level.dat` is written by the flush
      save. `MinecraftServer.saveAllChunks` calls
      `LevelStorageSource.LevelStorageAccess.saveDataTag` on **every** call,
      so an ordinary autosave rewrites it. The new durability section rests
      on this, so check it first. Also `PacketProcessor.close` drops packets
      *already queued*, not only late arrivals; and "the Server thread was
      the only non-daemon thread left" holds only after
      `Util.shutdownExecutors`, because `Util.ioPool`'s *IO-Worker* threads
      are non-daemon while `Util.nonCriticalIoPool`'s are daemons.
      *(session-verified)*
  - **`server-tick`** — the hook (the log *is* the skip, and the missed
    ticks are never run); the warning gate read as fifteen seconds of
    *scheduled* time; the six-lane figure's ordering, and in particular that
    `ServerCommonPacketListenerImpl.resumeFlushing` itself calls
    `Connection.flushChannel` (the second write is that call, not a later
    side effect) and that `Connection.tick` flushes **after** ticking its
    listener; the flush suspension applying only to sends made on the Server
    thread; the `MinecraftServer.tickChildren` order table row by row,
    including which rows are freeze-gated; the event-loop flowchart, which
    asserts the whole `pollTask` → `shouldRun` → `haveTime` decision;
    **the "three things the budget gates" count, re-derived twice this
    session** (`ChunkMap.processUnloads`, `ChunkMap.saveChunksEagerly`,
    `SectionStorage.tick` by way of `PoiManager.tick`) with its new riders —
    the unload queue draining regardless above two thousand entries, eager
    saving capped at twenty chunks and 128 outstanding writes; the sprint
    inversion; `MinecraftServer.emptyTicks` advancing only while not
    sprinting; *pause-when-empty-seconds* being zero on the base class; the
    in-memory connection rethrow; `IntegratedServer.isTickTimeLoggingEnabled`
    being unconditionally true.
  - **`server-level-tick`** — the hook (blocks broadcast before entities
    tick, so an entity's change lands a tick behind a command's); **the
    guard flowchart, the page's primary figure, which asserts a gate on
    every one of its twenty-odd steps — check it against `ServerLevel.tick`
    statement by statement**; the three-range opener (31 / 32, and "loaded
    means a holder exists"); the broadcast sequence diagram's order;
    `ChunkHolder.blockChanged` returning true only on the holder's first
    changed section; `GameRules.RANDOM_TICK_SPEED` at zero stopping ice and
    snow as well; `LocalMobCapCalculator.canSpawn` answering false with no
    player near; spawning chunks coming from
    `DistanceManager.getSpawnCandidateChunks` under a squared-distance test;
    `Level.tickBlockEntities` pruning removed tickers even while frozen; the
    overworld-only *gameTime* flag being the level constructor's last
    argument; commands being handled before `MinecraftServer.tickChildren`
    begins, which is what makes the hook's comparison exact.
  - **`players-and-sessions`** — the hook (death replaces the object, a
    dimension change does not, and both keep the entity id and the same
    listener); **both join diagrams, replacing one nine-lane diagram whose
    implied concurrency was wrong** — especially the claim that the burst
    runs inside `MinecraftServer.processPacketsAndTick`, before
    `MinecraftServer.tickChildren` opens the tick's own flush bracket, which
    is why `PlayerList.placeNewPlayer` brackets itself; the four-column
    comparison table, cell by cell; `ServerLevel.waitForEntities` blocking
    the Server thread; a respawn broadcasting **no**
    `ClientboundPlayerInfoUpdatePacket` *(session-verified)*; everything
    `ServerPlayer.restoreFrom` copies unconditionally, the ender chest
    among them, which makes its survival a field assignment rather than a
    game rule; the `.dat` written before the vehicle and ender-pearl
    removal; `PlayerSpawnFinder`'s coprime-strided search;
    `PlayerDataStorage.load` reading with an unlimited accounter;
    `ServerGamePacketListenerImpl.switchToConfig`'s round trip producing a
    new entity id and a new listener; the flying kick disabled at zero
    gravity.
  - **`starting-a-server`** — the hook (the boot step that loads the world's
    chunks loads none of them: of nine ticket types only
    `TicketType.FORCED` and `TicketType.PORTAL` carry
    `TicketType.FLAG_PERSIST`, *session-verified against all nine*); **the
    sequence diagram, the only one in the corpus with the JVM main thread as
    a lane — check which side of `MinecraftServer.spin` every step falls
    on**; `level.dat` parsed once and datafixed twice;
    `DirectoryLock.create` writing a snowman before taking the lock;
    `Util.blockUntilDone` making the main thread an executor for two stages
    of `WorldLoader.load`; the `MinecraftServer` constructor refusing a stem
    with no overworld `LevelStem`; the console thread building its
    `CommandSourceStack` off the Server thread; the icon and the first
    `ServerStatus` being built after `DedicatedServer.initServer` returns;
    `LevelLoadListener.Stage.START_SERVER` being declared and fired by
    nothing; there being no *spawnChunkRadius* game rule in 26.2
    (`GameRuleRegistryFix` removes it from saves); and the claim that the
    *menu.preparingSpawn* percentage line never runs on an ordinary world.
  - **`how-a-server-dies`** — new, so all of it; the drafting report cites a
    file and line per claim and pass 4 should walk that list. The
    load-bearing ones: the three-column comparison table, cell by cell; the
    `/stop` sequence diagram's order, which asserts players before chunks,
    `level.dat` before the server-wide `SavedDataStorage`, and the lock
    released last; **the watchdog self-deadlock diagram**, the hook drawn —
    `System.exit` runs the hook, the hook joins the wedged thread,
    `Runtime.halt` fires ten seconds later (*session-verified*:
    `ServerWatchdog.run` loops on `MinecraftServer.isRunning`,
    `ServerWatchdog.MAX_SHUTDOWN_TIME` is ten seconds, and the timer is
    scheduled before `System.exit`); the five callers of
    `MinecraftServer.halt` and which of them pass *wait* true; the
    durability section's answer per ending, which depends on the corrected
    autosave-writes-`level.dat` fact; the claim that a server stuck in
    teardown has no watchdog left watching it, because the watchdog loops
    only while `MinecraftServer.running`; and
    `MinecraftServer.reportChunkSaveFailure` writing a
    `ReportType.CHUNK_IO_ERROR` file under *debug/*.
  - **The landing page and `lectures.md`** assert Part III's order and its
    dependencies: that the part can be watched before Part IV because
    `server-level-tick` defines the three ranges itself, that
    `environment-attributes-and-timelines` is best watched before the level
    tick, and that Part I's *two loops* figure is the only earlier
    prerequisite. Each is a claim.
  - **`anatomy` lost two invariants to `server-tick`** — the budget's count
    and the sprint conclusion — and now carries a one-sentence pointer;
    check that the compression lost nothing true.

- **2026-09-02, session C — Part I Anatomy · Part II Foundations.** Nine
  pages rewritten or written (two Part I, seven Part II), three moved to
  Reference, one landing page. Every rewrite was diffed against its old
  page from the drafting agent's report before acceptance; the claims
  below are the ones that report listed as *introduced* or *reworded*, and
  the two pass-2 errors found on the way. Check the two new pages hardest —
  nothing on them was fact-checked in pass 2.
  - **Two pass-2 errors found.** `tags` said "an axe strips anything in
    `#minecraft:logs`". It does not: `AxeItem.STRIPPABLES` is a hard-coded
    `Map` of block to block and stripping never consults a tag; the page
    now opens on the parrot (`Parrot.ParrotWanderGoal` recognises leaves by
    class and logs by tag) and `PunchTreeTutorialStepInstance`. And
    `out-of-scope-tour` said `NoiseRouterData` calls `TerrainProvider` and
    `SurfaceRuleData` "every time a chunk's density functions are built".
    It does not: `NoiseRouterData.overworld` and its siblings are called
    only from `NoiseGeneratorSettings`' bootstrap methods, whose callers
    are `VanillaRegistries` (datagen) and `Commands.validate`;
    `SurfaceRuleData` is referenced by `NoiseGeneratorSettings` alone; the
    running game reads the generated JSON from the built-in pack. Verified
    by the session. The surviving runtime call is
    `NoiseRouterData.peaksAndValleys` → `TerrainProvider` on the F3 biome
    line and in `OverworldBiomeBuilder`'s parameter spans.
  - **`anatomy`** (trace, two figures). The two-loops flowchart is the
    figure Parts III, IX and X now link to; it asserts `Minecraft.runTick`
    = advance the `DeltaTracker` → drain the `PacketProcessor` → run own
    tasks → 0 to 10 ticks → render, and `MinecraftServer.runServer` = set
    the deadline → `processPacketsAndTick` (drain, then `tickServer`) →
    `waitUntilNextTick` (run tasks, then `managedBlock`); the startup
    sequence asserts `spin` constructs the `IntegratedServer` on the
    caller's thread before starting the new one. New: "the second thread
    was created by the first, mid-frame, while the first went on drawing"
    (`Minecraft.doWorldLoad` renders inside its wait loop);
    `PriorityConsecutiveExecutor` "adds a priority to the same idea"; both
    `Main`s read *version.json* through `SharedConstants`. Reworded:
    `DataFixers.optimize` is kicked off "before the registries are built"
    (was "at the very start"). Moved, not cut: `Minecraft.isPaused`'s
    three-part condition now lives only on `the-client-loop`;
    `tickPaused`'s "or the player list is empty" and "one save on the
    transition" only on `server-tick`.
  - **`what-this-book-skips`** (the old `out-of-scope-tour`, moved to
    Part I, the treemap included, the gaps as one table). New: the F3
    biome line runs through `NoiseRouterData.peaksAndValleys` into
    `TerrainProvider`; `NoiseRouterData` and `NoiseGeneratorSettings` are
    compiled against `TerrainProvider` and `SurfaceRuleData`; their
    bootstraps are collected by `VanillaRegistries`, run by the
    data-generator entry point and borrowed by `Commands.validate`; the
    `net/minecraft/realms` row (4 files, 203 lines: three classes and a
    *package-info*); "the table counts files, so *package-info.java*
    counts there and not in the prose" (rcon 9 files / 7 classes, stats 10
    / 9). Every size in the page's tables was checked against
    `src/generated/` and matches. The figcaption's "hatched boxes are the
    packages this page tours" is true of twelve of the fourteen: `gizmos`
    and `realms` are too small for the tool to hatch (a tool limitation,
    logged in pass3.md), and `client/multiplayer/chat/report` is depth 5.
  - **`codecs-nbt-json`** (comparison). New: both sides wrap
    `HashOps.CRC32C_INSTANCE` in a `RegistryOps` (`ClientPacketListener`
    from the received registries, `ServerPlayer` from its own) "because a
    component value can name a registry entry" — the motive is the agent's
    reading, soften if unverifiable; `ServerPlayer`'s container
    synchroniser hashes through a 256-entry cache keyed on
    `TypedDataComponent` (verified by the session); **removals are not
    hashed** — `HashedPatchMap` is a map of added type to int plus a set of
    removed types (verified; sharpens pass 2's "one CRC32C per component");
    a wire decode failure reaches `Connection.exceptionCaught` and drops the
    connection; `ItemParser.SYNTAX_REMOVED_COMPONENT` is the command-line
    spelling of `!minecraft:foo`; the hash path runs on the Render thread
    (`AbstractContainerScreen.slotClicked` → `MultiPlayerGameMode.handleContainerInput`).
    The four short diagrams assert: the disk path never touches a
    `CompoundTag` in the block entity; the wire path is `StreamCodec` all
    the way with the `NullOps` re-encode on exactly one packet; the server
    re-hashes its own stack rather than decoding; the text path builds its
    `TagParser` for the parser's own `RegistryOps`.
  - **`identifiers-and-registries`** (trace, both diagrams kept). The
    world-load diagram's `replaceFrom` arrow now comes from `WorldLoader`,
    not `RegistryDataLoader` (read from `WorldLoader.load`), and
    `RegistryDataLoader.load` is given lookups built by
    `TagLoader.buildUpdatedLookups` over `getAccessForLoading`, not the
    access directly. New cast claims: `RegistryDataLoader` loads JSON on the
    server and NBT from the wire on the client (`NetworkRegistryLoadTask`).
    The freeze rule is now stated in one section and justified nowhere on
    this page; `Registry.PendingTags` and `prepareTagReload` are named only
    on `tags`. Counts unchanged: 148 keys, 147 objects, five intrusive.
  - **`resource-system`** (pipeline, `/reload` as a comparison table).
    New, all from `SimpleReloadInstance`, `Minecraft`, `LoadingOverlay`,
    `MinecraftServer.reloadResources`, `ReloadCommand`,
    `MultiPackResourceManager`, `Pack.Position`: the first listener's
    barrier is chained to the initial task; `PreparationBarrier.wait` posts
    a main-thread task that removes the listener from the preparing set and
    completes the all-preparations future when it empties; a listener that
    never reaches its barrier holds every apply; **twenty** client
    listeners; `AtlasManager` publishes one future per atlas in
    `prepareSharedState`; the overlay fades in over half a second and will
    not fade out before a full second; the recovery reload skips the fade;
    the success continuation is `finishReload` → `DownloadedPackSource.onReloadSuccess`
    → `onResourceLoadFinished`; `abortResourcePackRecovery` drops the
    overlay, disconnects and shows a toast; `triggerResourcePackRecovery`
    "takes the same road" (caveat: `clearResourcePacksOnError` crashes or
    aborts when `isAbleToClearAnyPack` is false — check the sentence);
    `ReloadReason.INITIAL`; `ReloadCommand` at `Commands.LEVEL_GAMEMASTERS`;
    on server failure the new manager is closed and the old stays; filter
    sections are pushed onto the namespace stacks; `Pack.Position.TOP`
    inserts at the back; a new `Commands` inside each
    `ReloadableServerResources`. Reworded: `Pack.Position.BOTTOM` "inserts
    at the front, past any pack already fixed there" (was "at index 0").
    The lattice figure asserts every apply waits on all preparations *and*
    the previous apply, and that the only prepare-to-prepare edge is
    `AtlasManager` → `ModelManager` through shared state.
  - **`tags`** (trace). New: the vanilla *logs* file is three tag
    references (*logs_that_burn*, *crimson_stems*, *warped_stems*),
    *logs_that_burn* nine references including *oak_logs*, *oak_logs* four
    blocks — so *oak_logs* is a grandchild of *logs*, not a direct entry
    (the old page said otherwise); `Registry.PendingTags.lookup` answers as
    if installed; the client rebuilds its fuel table and creative search
    tree on a play-phase tags packet; `Holder.Reference.is` is a
    set-contains on the bound tag set; `FileToIdConverter.json` over the tag
    directory. The diagram's five `Note over` bars (worker pool → server
    thread → configuration → play → a server tick) are ordering claims.
  - **`data-components`** (vocabulary). New: `DataComponentLookup` reads the
    same bound prototypes and is meaningless before the first reload (check
    that its lazy population reads `Holder.components`); "set the
    enchantments back to empty and the entry vanishes" (a worked instance of
    the sanitising rule); `ItemStack.set` is `PatchedDataComponentMap.set`;
    the cast's thread cells. The figure asserts prototype on
    `Holder.Reference` ← `DataComponentInitializers.build`, stack = shared
    prototype + `Optional` patch + `copyOnWrite`; the trace asserts click →
    `transmuteCopy` → `enchant` → `set` → `ensureMapOwnership` → the next
    `ServerPlayer.tick`'s `broadcastChanges` → `ClientboundContainerSetSlotPacket`
    → `fromPatch`.
  - **`text-components`** (new, vocabulary; every claim is new). The hook:
    the death message is sent twice (`ClientboundPlayerCombatKillPacket` to
    the victim, system chat to everyone — verified by the session from
    `ServerPlayer.die`; a team visibility of `NEVER` broadcasts nothing,
    which the page does not say), crosses as a translation key, and is
    worded by the client's `Language` on the first frame that draws it; the
    server logs it through `Language.DEFAULT_INSTANCE` and `Language.inject`
    is called only by `LanguageManager` (verified). The rest of the page —
    the visit order, `getString` with a limit, `TranslatableContents.decompose`'s
    accepted specifiers and its cache by `Language` identity, the keybind
    resolver, the three unresolved kinds, `ObjectContents`' U+FFFC
    placeholder, the eleven `Style` fields and `applyTo`, `TextColor`,
    `shadowColor`, the eight click actions table (`UNSAFE_CODEC` read by
    nothing outside the enum; `OpenFile` built only by `Screenshot`,
    `KeyboardHandler` and `Minecraft`), the flat serialisation (never a
    *type* key on encode), the two NBT budgets and which packets use which
    stream codec, the resolution walk and its depth limit, the death-message
    key rules (`.player`, `.item`, `FALL_VARIANTS`, `INTENTIONAL_GAME_DESIGN`),
    `Entity.getDisplayName`'s shape, the `even_more_magic` fallback,
    `ClientLanguage.loadFrom`'s two-code stack — is one claim per sentence,
    each with a file in the agent's report; two the agent flagged as
    unverified: "merged in stack order" (which end of the pack stack wins
    for language files) and that the dedicated server jar bundles
    *en_us.json*.
  - **`data-driven-types`** (new, pattern; every claim is new). The count
    — **fifty-six** registries in `BuiltInRegistries` that some codec
    dispatches on through `Registry.byNameCodec`: thirty-one bare
    `MapCodec` registries, twenty-three type-object registries, two where
    the type is the behaviour (`Feature`, `WorldCarver`) — was derived by
    grepping dispatch sites; re-derive it. The three tables' *where the
    elements live* and dispatch-key columns (*function*, *condition*,
    *processor_type*, *predicate_type*, *element_type*, *trigger*) are one
    claim per row. The trace asserts the reload half
    (`ReloadableServerResources.loadResources` → `ReloadableServerRegistries.reload`
    on the background executor; `scanDirectory` via `FileToIdConverter.registry`
    over `Registries.elementsDirPath`; a bad file logged and skipped, a
    duplicate id an error; `LootItemFunctions.compose`; `createUpdatedRegistries`
    → `replaceFrom`; validation warns and keeps the element;
    `Lifecycle.experimental`) and the run half (`RandomizableContainerBlockEntity.getItem`
    → `unpackLootTable` → `LootTable.EMPTY` for an unknown key; `fill` →
    `getRandomItems` → `shuffleAndSplitItems`; `decorate` nesting table →
    pool → entry, "a function on the table runs last"; `LootItem.createItemStack`
    → `LootItemConditionalFunction.apply` → `SetItemCountFunction.run`).
    The exceptions section: `Codec.dispatchedMap` for `GameRuleMap` and
    `DataComponentPredicate`; `ENTITY_SUB_PREDICATE_TYPE` holds a plain
    `Codec`; `RECIPE_TYPE` versus `RECIPE_SERIALIZER`; `BLOCK_TYPE` read by
    nothing but `BlockListReport`; `RegistryDataLoader` fails the whole
    load where `scanDirectory` skips one file.
  - **`systems/foundations/README.md`** (new, landing page): the stack
    figure's ten edges are dependency claims; *before you start* names only
    `anatomy`; the seven teasers restate the seven hooks.
  - **`chat-and-signing`**: its `Component` section is now a one-paragraph
    pointer; the three facts it keeps (NBT on the wire, the `OPEN_FILE`
    filter, chat never resolves) are unchanged. **`reference/threads.md`**:
    one clause added — Swing's thread appears only when the dedicated
    server is started without *--nogui*. **`tools/map_source.py`**:
    `com/mojang/blaze3d/audio` added to `SKIPPED` so the treemap hatches
    what the tour tours.

- **2026-09-02, session A (the frame)** — two pilot pages rewritten in new
  shapes, the introduction and Part I's landing page written, the lane key
  seeded. The standing item on the lane key is discharged:
  `tools/check_lanes.py` verifies every key expansion against the decompile
  and runs in `deploy.sh`.
  - **`tickets-and-loading`** (policy shape). *Corrected from pass 2:* the
    keep-dimension-active flag (`TicketType.FLAG_KEEP_DIMENSION_ACTIVE`, 8)
    is on `PLAYER_SIMULATION` (flags 12), `FORCED` (15), `PORTAL` (15) and
    `ENDER_PEARL` (14) — **not** on `PLAYER_LOADING` (2); the old invariant
    "a player-loading ticket keeps the dimension alive" was wrong and the
    table gained a column. Claims introduced: the hook ("a chunk can be
    `ENTITY_TICKING` by every measure the holder knows and tick nothing");
    "timed and `canExpireIfUnloaded` — only `UNKNOWN`" (flags 18 is the only
    one carrying 16); "the four in flight are the four nearest" (inferred
    from priority = distance in `PlayerTicketTracker.onLevelChange` — check
    the dispatcher really orders by that priority); "loading floods in
    Chebyshev rings — every ring is a square"; "a spectator under
    `SPECTATORS_GENERATE_CHUNKS` false is still sent chunks that exist but
    places no tickets" (read from `ChunkMap.updatePlayerStatus`: ignored
    players skip `DistanceManager.addPlayer` but still get
    `updateChunkTracking`). Diagrams redrawn: the flowchart asserts holders
    exist at ≤ 44, futures arm at 33/32/31, and the simulation graph feeds
    only the range questions; the `FullChunkStatus` state diagram asserts
    promotion waits for future success and demotion is immediate (read from
    `ChunkHolder.updateFutures`/`demoteFullChunk`), entry at ≤ 44, exit past
    44 via `toDrop` → `processUnloads`; the six-lane trace asserts the order
    spawn counter → simulation tracker → player ticket tracker → loading
    tracker → two passes over `chunksToUpdateFutures` (read from
    `DistanceManager.runAllUpdates`) and that the crescents are marked
    before `runAllUpdates`. The two decision tables restate pass-2 facts;
    check each row's gate column as an "only" claim.
  - **`protocol-phases`** (state-machine shape). Claims introduced: the
    five-phase diagram — `STATUS` is a dead end, `PLAY` ⇄ `CONFIGURATION`,
    "every transition packet is terminal" (the seven `isTerminal`
    overrides are exactly the seven transition packets: intention, login
    finished, login acknowledged, finish configuration ×2, start
    configuration, configuration acknowledged); the login state diagram —
    `HELLO → KEY` only for online mode over a socket, `HELLO → VERIFYING`
    for the singleplayer profile or offline mode, `KEY → AUTHENTICATING` on
    the key packet, `AUTHENTICATING → VERIFYING` from the thread,
    `VERIFYING → WAITING_FOR_DUPE_DISCONNECT | PROTOCOL_SWITCHING` and
    `WAITING → PROTOCOL_SWITCHING` in `tick`, `PROTOCOL_SWITCHING →
    ACCEPTED` on the acknowledgement, `NEGOTIATING` never assigned (all read
    from the state assignments this session); the three-lane handshake
    sequence (joinServer before the key packet; ciphers attached to the
    send; the server installs ciphers before its own session call); the
    configuration flowchart (registries → code of conduct → resource pack →
    prepare spawn → join world; the finish handler does outbound play, the
    duplicate check, `canPlayerLogin`, then `spawnPlayer` — read from
    `handleConfigurationFinished`); the two "what disconnects a …"
    paragraphs are new syntheses of old facts; "the first
    `PacketUtils.ensureRunningOnSameThread` in a connection's life is in
    configuration" is borrowed from `anatomy`. The three client entry
    points sentence is the old *Called by* bullet, kept.
  - **`introduction`** (new): "just under a third client-only" (2,206 of
    7,055, from `maps/packages.md` and `server-classes.txt`); "0 to 10
    ticks inside a frame" (from `the-frame`); the two-programs figure
    asserts that workers feed both levels.
  - **`systems/anatomy/README.md`** (new, landing page): the root figure is
    a claim about which thread each part starts from — check as an ordering
    claim. **`lectures.md`**: Part I's two entries and the two known
    cross-part dependencies (from the pass-3 notebook).

- **2026-09-02, planning session** — the mermaid syntax fixes were
  syntax-only (labels reworded around `;` and `#`, see the commit diff); no
  claim changed. Nothing to check beyond a glance at that diff.

- **2026-09-02, session B — maps: the atlas.** The atlas is new prose over
  regenerated numbers, and the tool that makes the numbers changed; check
  the tool first, then the prose against a fresh run.
  - **`tools/map_source.py`** (rewritten): the declaration regex now matches
    indented (nested) declarations and record headers, which the old one
    silently did not — every hierarchy count changed (`Entity` 188 → 193,
    `Goal` 70 → 200, `Screen` 153 → 157, `Packet` unlisted → 232), and a
    simple name declared twice now resolves to the top-level class (a nested
    `Block` in blaze3d had claimed the name). Fan-in now counts every
    `com.mojang` import, so `Codec`, `MapCodec`, `RecordCodecBuilder`,
    `Schema`, `DSL` and *LogUtils* appear. Re-derive one number of each
    kind by hand (a package's line count, one class's importers, one root's
    descendants) before trusting the rest.
  - **`maps/packages.md`**: 2,206 client-only classes in exactly four
    packages and no mixed depth-4 package (read off the table's client-only
    column: every row is 0 or all); 212,242 client-only lines = 29.5%;
    `world/level` a fifth of the game; two thirds of `util` skipped (34,176
    of 53,275); Vulkan back-end larger than OpenGL; the **part → packages
    table** is a claim about where each part's classes live and should be
    checked per part as the parts convert (`server/dialog` and
    `world/level/pathfinder` are guesses from package names, not from
    pages); the `SKIPPED` list in the tool must agree with *what this book
    skips* (gametest is deliberately not hatched: covered in Part XIII).
  - **`maps/biggest.md`**: `BlockModelGenerators`' only caller is
    `ModelProvider` (one grep hit); nothing outside `util/datafix` reads
    `BlockStateData` (seven files, all datafix); the sum 62,935 = 8.7%;
    "`Fox` and `Bee`, the two with the most bespoke behaviour" is a
    judgement stated as fact — verify or soften; "`Options` is every
    setting" and "`Hud` is everything drawn over the world" are glosses;
    `OceanMonumentPieces` and `StrongholdPieces` "built by hand in Java
    rather than a template" rests on `hand-built-structures`.
  - **`maps/fanin.md`**: one file in six (1,221 of 7,055); all but ten
    `Schema` importers in `util/datafix` (389, 10 outside); `Minecraft`
    twenty-ninth and the only client-only class in the thirty; the hub →
    page table sends `Component` to "Part II", which has no page until
    session C writes one (R6) — fix the link then; "same-package use is
    not counted" is Java, not a claim about the game.
  - **`maps/hierarchy.md`**: `FeatureElement`'s seven implementers
    (grep-verified: `BlockBehaviour`, `Item`, `EntityType`, `MenuType`,
    `MobEffect`, `Potion`, `GameRule`); `ItemLike` = `Block` + `Item`; the
    per-tree numbers (193/18, 124, 114, 108, thirteen terminal; 293/92, 61
    terminal, 64; 71/51; 157/72, 60 terminal, 27, 23); "over a thousand
    registered items" (1,130 `registerItem`/`registerBlock` lines in
    `Items`, a few of them definitions); "`Items` registers most of the
    game as a plain `Item`" is asserted, not counted; "`BlockBehaviour`
    exists so that behaviour and registry identity can be separate
    classes" is a motive, not a fact — check or cut; `Goal` 130 of 200
    nested; `Packet` 227 direct implementers versus the packets reference's
    count (packet *types* and packet *classes* differ; say which).
  - **`reference/threads.md`** (new figure): every edge asserts a
    direction and a kind (posted task / completed future / hopped handler)
    — "serverbound packets written on the caller's thread", region I/O as
    posted task and completed future through `IOWorker`, sound as posted
    tasks to `SoundEngineExecutor`, console/RCON/query/management as
    posted command lines; all drawn from the page's own table, none
    re-verified against the decompile this session.
  - **`introduction`**: the treemap's hatching is the tool's `SKIPPED`
    list; the "just under a third" now has its figure.
  - **`entities/entity-anatomy.md`**: "193 descendants" (was 188, from
    the old map that could not see nested classes); re-derive with the new
    tool and by hand once.
