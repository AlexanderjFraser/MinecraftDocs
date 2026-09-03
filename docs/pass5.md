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
