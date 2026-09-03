# Pass 5 — polish (queue; opened 2026-09-02)

*Pass 5 is the wording pass — voice, consistency, cuts. Its inputs: the
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
  - Three pages used to say some version of "shape updates run on both sides,
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
  inventories go. **Three items need a home and have none yet** — the
  `ServerPlayerGameMode` paragraph (block-breaking state,
  `ServerPlayerGameMode.changeGameModeForPlayer`,
  `ServerPlayer.storeGameTypes`), which belongs with `player-anatomy` or a
  game-mode page; `ClientboundSetChunkCacheRadiusPacket` /
  `ClientboundSetSimulationDistancePacket` on a view-distance change, which
  is server reconfiguration rather than a session event (candidate home:
  `what-the-client-is-told`); and `PlayerDataStorage`'s *.dat_old* and
  *corrupted* rescue, compressed here into one cast-table cell and wanting a
  save-format Reference entry. The `ClientboundSetHealthPacket`
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
  **`identifiers-and-registries`**: `MappedRegistry.byValue` cut;
  `TagLoader` named only as `TagLoader.buildUpdatedLookups`.
  **`resource-system`**: `RegistryDataLoader` dropped from its calls-into
  (the registries page owns it). **`tags`**: nothing cut.
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
  **`using-an-item`** deliberately left the full `Item.getUseDuration`
  override roster (`BrushItem`, `BundleItem`, `EnderEyeItem`,
  `InstrumentItem` and their numbers) to nobody: neither it nor
  `items-and-stacks` now carries it. It is a Reference-page candidate or a
  sentence; it is currently lost prose, and this is the record of it.

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

- **2026-09-03, out of band — the licence footer says it twice on one page.**
  `site-footer.js` puts the disclaimer and the CC BY-SA line on every page,
  and the introduction now also closes on *Unofficial, and free to reuse*,
  which says the same two things in prose. Everywhere else the footer is the
  only statement and reads as small print; on `introduction` alone it is a
  restatement two inches below the section it restates. Cheapest fix if pass 5
  agrees it grates: have the footer skip the introduction (it is the one page
  guaranteed to carry the prose version), rather than cutting the prose —
  the prose is what reaches an agent through `llms-full.txt`, which the JS
  footer never does. Not urgent; nobody has complained, and duplication in
  favour of the licence being visible is the right way round to err.

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
