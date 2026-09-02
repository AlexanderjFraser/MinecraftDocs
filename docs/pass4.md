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
