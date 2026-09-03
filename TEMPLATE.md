# The page — a menu of shapes

*Rewritten by pass-3 session A (2026-09-02) from two pilots:
`src/systems/world/tickets-and-loading.md` (a policy page) and
`src/systems/networking/protocol-phases.md` (a state machine). The old
seven-heading skeleton is gone; a page takes the shape of its story, and the
budgets below are the enforceable part. Ruling R2 in `docs/plan.md` is the
authority; this file is its working form.*

## What every page keeps

1. **The title** — the system, not the scenario.
2. **The verified line** — `> Verified against **Minecraft 26.2** · Part N ·
   <the scenario in one line>`. The scenario is a sentence a player could
   act out, not a topic.
3. **The opening paragraph** — starts *inside* the scenario (a player takes a
   step; a server is clicked in the list) and ends on the **hook**: the one
   observable, surprising, true thing the page explains. No "Responsibility"
   heading; the paragraph is the responsibility. The pass-2 findings are the
   hook bank (the block that comes back and vanishes again; lava
   random-ticking twice; the watchdog kill that saves nothing; the minimized
   window rendering frames nobody sees; the player built after the phase
   named for preparing it).
4. **The cast** — at most eight classes with role and thread, as a small
   table (`| class | what it decides | thread |`) or woven into the
   narration. It replaces the field inventories: a page names the fields
   its story touches, in the sentences that touch them, and the exhaustive
   lists live in the class index and Reference.
5. **At least one figure**, in the shape the page chose (below), with lanes
   from the key.
6. **Headings that say what the section says** — *The two flushes*, *When
   a ticket dies*, *Status, the phase nobody logs in through* — never which
   template slot it fills. A reader should be able to tell two pages apart
   from their tables of contents.
7. ***Where to look*** — entry-point names, one line, in reading order — and
   the rules footer, verbatim:

   `*Rules: names, never code · how the system works, not how the code reads ·
   newest version only · every backticked name passes \`tools/verify_names.py\`.*`

What every page drops: *Responsibility*, *The data it owns*, *When it runs*,
*Interfaces* and *Invariants and surprises* as headings. Their content goes
where the story needs it — the thread in the cast table, the interfaces as
one sentence or one cast row (what crosses the network, as which packets),
the invariants placed where they happen or gathered as answers in a
*Questions players ask* section.

## The shapes

Choose the one whose figure is the true picture of the system. If the
truth is a graph, do not draw a conversation.

| shape | for | its figure | how the sections go | pilot |
|---|---|---|---|---|
| **the trace** | one scenario through the system | a `sequenceDiagram`, at most seven lanes, `Note over` at every tick boundary | narrated as prose in the order things happen, each surprise placed where it happens | (session C onward) |
| **the pipeline** | stages that hand off | a `flowchart` of the stages at the top | a section per stage: what comes in, what is decided, what goes out | — |
| **the state machine** | phases and transitions | `stateDiagram-v2`, transitions labelled with the packets or events; an orphan state drawn as an orphan | a section per state, each ending in *what disconnects / fails / leaves it* | `protocol-phases` |
| **the policy** | who is told what, and when | a decision table or a `flowchart` per decision; the surprises are its rows | one section per decision on the path the opening figure draws; a short trace kept as the grounding | `tickets-and-loading` |
| **the comparison** | two or three paths that differ | a table with the paths as columns; one diagram per path, or one with `alt` | a section per point of difference, not per path | — |
| **the vocabulary page** | the objects and their relations | a figure of the data (`classDiagram`, a containment `flowchart`), then one small trace | a tour by object, each grounded in the trace | — |
| **the pattern** | one idea, many instances | the instances as a table; one instance traced | the idea, the table, the trace, the exceptions | — |
| **the landing page** | a part | the part's shape as a figure of its pages | one paragraph · the figure · *before you start* · *watch in this order* · the Reference pages it uses; under a hundred lines, no trace | `src/systems/anatomy/README.md` |

A page may borrow one section from another shape (the policy pilot keeps a
six-lane trace; the state-machine pilot keeps a three-lane sequence for the
encryption handshake alone). It may not borrow the whole skeleton. **A page
is not done until it reads differently from its neighbours.**

## The devices

Any page may use these; none must.

- **The myth table** — `| what the forum says | what the decompile does |`.
- **The number** — a count with its owner, set off on its own line:
  `**Four** — player-view chunks loading at once (\`DistanceManager.ticketDispatcher\`).`
- **For a 1.21-era reader** — a blockquote opening `> **For a 1.21-era
  reader.**`, replacing the names-you-will-hunt-for bullets; one per page at
  most, and only where a modder would reach for a name that has moved.
- **Questions players ask** — a section whose bold lead-ins are questions
  and whose paragraphs are the invariants, restated as answers.
- **The same trace from the other side** — a mirrored client/server pair,
  as `environment-attributes-and-timelines` already does.
- **The tick-boundary bar** — `Note over X: a later tick` (or the tick
  phase by name) wherever a sequence crosses a tick; and the explicit *no
  reply* annotation (`-->>` with the word *nothing*) where a packet is
  answered by silence.

## The budgets

The enforceable part.

- A bulleted or numbered list holds **parallel items of at most two
  sentences, at most seven of them**, and a page has **at most three
  lists**. *Where to look* is not a list; the cast is a table.
- Anything explanatory is prose. Anything enumerative **beyond seven is a
  table**, or a Reference page the text links to.
- A section **passes forty lines only with a figure or a subsection in it**.
- *Interfaces* survives as one sentence or one cast row.
- Nothing is dropped from a page except by moving it (Reference, another
  page) or by logging the cut in `docs/pass5.md` with the reason.
- Every claim a rewrite introduces — a hook, a redrawn ordering, a new
  section — is listed in `docs/pass4.md` by the session that wrote it.

## Figures

Mermaid in the page for anything mermaid 11.6.0 draws; generated SVG from
`tools/` (inlined with `{{#include}}`) for the maps and for figures no mermaid
type draws; never a hand-drawn or raster image. `node tools/check_mermaid.js`
is the arbiter of what the site's mermaid accepts, and a diagram that fails
it does not publish. The three rules it enforces most often:

- **No `;` in any label** — mermaid ends the statement there. Write `#59;`
  if the character is unavoidable; usually a comma or *then* is better.
- **No `#` in any label** — mermaid reads an entity code and drops the rest
  of the line silently. Write `#35;`.
- **Quote flowchart labels** (`A["…"]`) so parentheses, colons and slashes
  survive; keep `stateDiagram-v2` transition text on one line after the
  colon; a note is `note right of STATE : text`.

Shapes that render under 11.6.0 and are in use: `sequenceDiagram`,
`flowchart`, `stateDiagram-v2`. Others the checker accepts may be added;
a shape the checker rejects is not available whatever the docs say.

**A generated figure** (session B's pipeline, used by the atlas) is an SVG a
tool under `tools/` writes into `src/generated/` — never hand-edited, always
regenerable on the next version — and a page includes it inside an HTML
block so that it inherits the theme:

    <figure class="map">
    {{#include ../generated/<name>.svg}}
    <figcaption>What the figure shows. Click to enlarge.</figcaption>
    </figure>

The SVG carries **classes only** — `class="mapfig"` on the root, and
`shared`, `client`, `lib`, `skip`, `muted`, `fold`, `edge`, `group` on its
parts — and every colour, font and theme rule lives in `custom.css`, with
text as `currentColor`, so the five mdBook themes and the zoom overlay all
read it. It emits no blank line (an HTML block ends at one), sets a
`viewBox` so it scales to the column, and puts a `<title>` on each element
that has a number, so hovering answers what a label could not fit.
`tools/map_source.py` is the worked example: a squarified treemap, bar
charts and a left-to-right tree with counts, each a forty-line function.
`llms_full.py` replaces an SVG include with a one-line note and pastes a
markdown include in, so a generated table beside the figure is what
agents read.

## Lanes

A lane in a sequence diagram is a class name, abbreviated once for the whole
corpus. `python tools/check_lanes.py` reads the key below and every
`participant X as Y` in `src/`, fails if a key entry is not a class in the
decompile or if two key rows share a lane, and reports every page whose
lane means something other than the key says; `--strict` turns the report
into a failure (used per part as sessions convert them, corpus-wide from
session P), and `--index` writes the key to `src/reference/lanes.md` for
readers.

**How a lane is derived** when it is not yet in the key: the initials of
the class's CamelCase words (`ServerGamePacketListenerImpl` → `SGPL`),
never fewer than two letters; a one-word class of up to eight letters is
its own lane (`Player`, `Entity`, `Window`), a longer one takes a fixed
prefix recorded here (`Connection` → `Conn`); a nested class takes the
outer initials plus its own (`DistanceManager.PlayerTicketTracker` →
`PTT` is the exception, claimed by the pilot); a collision is resolved by
lengthening the **later** claimant, never by reassigning an existing row.
A short whole word is allowed for a lane that is not a class (`Netty`,
`Main`, `Worker`, `Auth`, `Wire`, `Disk`) and is marked as such below.
**The key is the authority**: add a row when a page introduces a lane, and
never change an existing row's meaning.

### The lane key

| lane | class |
|---|---|
| `MC` | `Minecraft` |
| `MS` | `MinecraftServer` |
| `IS` | `IntegratedServer` |
| `DS` | `DedicatedServer` |
| `SL` | `ServerLevel` |
| `CL` | `ClientLevel` |
| `Level` | `Level` |
| `SP` | `ServerPlayer` |
| `LP` | `LocalPlayer` |
| `Player` | `Player` |
| `Entity` | `Entity` |
| `PL` | `PlayerList` |
| `SGPL` | `ServerGamePacketListenerImpl` |
| `CPL` | `ClientPacketListener` |
| `SHPL` | `ServerHandshakePacketListenerImpl` |
| `SSPL` | `ServerStatusPacketListenerImpl` |
| `SLPL` | `ServerLoginPacketListenerImpl` |
| `SCPL` | `ServerConfigurationPacketListenerImpl` |
| `CHPL` | `ClientHandshakePacketListenerImpl` |
| `CCPL` | `ClientConfigurationPacketListenerImpl` |
| `Conn` | `Connection` |
| `SCL` | `ServerConnectionListener` |
| `BEL` | `BlockableEventLoop` |
| `SCC` | `ServerChunkCache` |
| `CM` | `ChunkMap` |
| `CMTE` | `ChunkMap.TrackedEntity` |
| `CH` | `ChunkHolder` |
| `DM` | `DistanceManager` |
| `TS` | `TicketStorage` |
| `LCT` | `LoadingChunkTracker` |
| `SCT` | `SimulationChunkTracker` |
| `PTT` | `DistanceManager.PlayerTicketTracker` |
| `CTD` | `ChunkTaskDispatcher` |
| `TCTD` | `ThrottlingChunkTaskDispatcher` |
| `PCS` | `PlayerChunkSender` |
| `PESM` | `PersistentEntitySectionManager` |
| `PST` | `PrepareSpawnTask` |
| `SRT` | `SynchronizeRegistriesTask` |
| `JWT` | `JoinWorldTask` |
| `RS` | `RenderSystem` |
| `GR` | `GameRenderer` |
| `LR` | `LevelRenderer` |
| `Gui` | `Gui` |
| `Hud` | `Hud` |
| `Screen` | `Screen` |
| `Window` | `Window` |
| `Boot` | `Bootstrap` |
| `BIR` | `BuiltInRegistries` |
| `Items` | `Items` |
| `Item` | `Item` |
| `MR` | `MappedRegistry` |
| `DMR` | `DefaultedMappedRegistry` |
| `WL` | `WorldLoader` |
| `RDL` | `RegistryDataLoader` |
| `RLT` | `RegistryLoadTask` |
| `RMRLT` | `ResourceManagerRegistryLoadTask` |
| `LRA` | `LayeredRegistryAccess` |
| `RDC` | `RegistryDataCollector` |
| `RSyn` | `RegistrySynchronization` |
| `CBE` | `ChestBlockEntity` |
| `TVO` | `TagValueOutput` |
| `CHelp` | `ContainerHelper` |
| `IStack` | `ItemStack` |
| `NbtIo` | `NbtIo` |
| `PEnc` | `PacketEncoder` |
| `PDec` | `PacketDecoder` |
| `DCP` | `DataComponentPatch` |
| `HS` | `HashedStack` |
| `IP` | `ItemParser` |
| `TagP` | `TagParser` |
| `KH` | `KeyboardHandler` |
| `PR` | `PackRepository` |
| `RRM` | `ReloadableResourceManager` |
| `MPRM` | `MultiPackResourceManager` |
| `SRI` | `SimpleReloadInstance` |
| `PRL` | `PreparableReloadListener` |
| `LO` | `LoadingOverlay` |
| `RC` | `ReloadCommand` |
| `TL` | `TagLoader` |
| `RSR` | `ReloadableServerResources` |
| `Parrot` | `Parrot` |
| `EM` | `EnchantmentMenu` |
| `EH` | `EnchantmentHelper` |
| `PDM` | `PatchedDataComponentMap` |
| `ACM` | `AbstractContainerMenu` |
| `Comp` | `Component` |
| `MComp` | `MutableComponent` |
| `CS` | `ComponentSerialization` |
| `CU` | `ComponentUtils` |
| `Language` | `Language` |
| `Font` | `Font` |
| `CT` | `CombatTracker` |
| `DScr` | `DeathScreen` |
| `TrC` | `TranslatableContents` |
| `RSReg` | `ReloadableServerRegistries` |
| `LT` | `LootTable` |
| `LIF` | `LootItemFunctions` |
| `SICF` | `SetItemCountFunction` |
| `PP` | `PacketProcessor` |
| `TRM` | `ServerTickRateManager` |
| `LTs` | `LevelTicks` |
| `EAS` | `EnvironmentAttributeSystem` |
| `NS` | `NaturalSpawner` |
| `ETL` | `EntityTickList` |
| `WB` | `WorldBorder` |
| `PDS` | `PlayerDataStorage` |
| `SW` | `ServerWatchdog` |
| `LSA` | `LevelStorageSource.LevelStorageAccess` |
| `SC` | `StopCommand` |
| `DL` | `DirectoryLock` |
| `WS` | `WorldStem` |
| `LC` | `LevelChunk` |
| `CGT` | `ChunkGenerationTask` |
| `TLE` | `ThreadedLevelLightEngine` |
| `BLE` | `BlockLightEngine` |
| `LLSS` | `LayerLightSectionStorage` |
| `SCD` | `SerializableChunkData` |
| `IOW` | `IOWorker` |
| `LCTs` | `LevelChunkTicks` |
| `FF` | `FlowingFluid` |
| `LB` | `LiquidBlock` |
| `BI` | `BucketItem` |
| `RB` | `RepeaterBlock` |
| `GED` | `GameEventDispatcher` |
| `VSL` | `VibrationSystem.Listener` |
| `VST` | `VibrationSystem.Ticker` |
| `VSel` | `VibrationSelector` |
| `SSB` | `SculkSensorBlock` |
| `PM` | `PoiManager` |
| `Brain` | `Brain` |
| `AP` | `AcquirePoi` |
| `VNP` | `ValidateNearbyPoi` |
| `SIB` | `SleepInBed` |
| `PN` | `PathNavigation` |
| `EVS` | `EnvironmentAttributeSystem.ValueSampler` |
| `ATS` | `AttributeTrackSampler` |
| `KTS` | `KeyframeTrackSampler` |
| `SCM` | `ServerClockManager` |
| `EAP` | `EnvironmentAttributeProbe` |
| `Camera` | `Camera` |
| `GS` | `GaussianSampler` |
| `SAI` | `SpatialAttributeInterpolator` |
| `SR` | `SkyRenderer` |
| `Mob` | `Mob` |
| `Block` | `Block` |
| `MPGM` | `MultiPlayerGameMode` |
| `SPGM` | `ServerPlayerGameMode` |
| `CNU` | `CollectingNeighborUpdater` |
| `DB` | `DoorBlock` |
| `AFBE` | `AbstractFurnaceBlockEntity` |
| `FM` | `FurnaceMenu` |
| `LevB` | `LeverBlock` |
| `RSWB` | `RedStoneWireBlock` |
| `DRWE` | `DefaultRedstoneWireEvaluator` |
| `PBB` | `PistonBaseBlock` |
| `PSR` | `PistonStructureResolver` |
| `PMBE` | `PistonMovingBlockEntity` |
| `ET` | `EntityType` |
| `SumC` | `SummonCommand` |
| `SE` | `ServerEntity` |
| `ES` | `EntityStorage` |
| `SED` | `SynchedEntityData` |
| `Sheep` | `Sheep` |
| `LE` | `LivingEntity` |
| `CG` | `CollisionGetter` |
| `Shapes` | `Shapes` |
| `AttrI` | `AttributeInstance` |
| `AttrM` | `AttributeMap` |
| `EffC` | `EffectCommands` |
| `ME` | `MobEffect` |
| `AB` | `AbstractBoat` |
| `AA` | `AbstractArrow` |
| `CR` | `CombatRules` |
| `MTS` | `MoveToTargetSink` |
| `MoveC` | `MoveControl` |
| `NE` | `NodeEvaluator` |
| `PF` | `PathFinder` |
| `PNR` | `PathNavigationRegion` |
| `UAFS` | `UpdateActivityFromSchedule` |
| `Cons` | `Consumable` |
| `BowI` | `BowItem` |
| `ChestM` | `ChestMenu` |
| `CraftM` | `CraftingMenu` |
| `RemS` | `RemoteSlot` |
| `CSync` | `ContainerSynchronizer` |
| `ResultS` | `ResultSlot` |
| `ResultC` | `ResultContainer` |
| `RM` | `RecipeManager` |
| `CI` | `CraftingInput` |
| `SRB` | `ServerRecipeBook` |
| `Ench` | `Enchantment` |
| `Ignite` | `Ignite` |
| `EScr` | `EnchantmentScreen` |
| `CMap` | `ContextMap` |
| `LootP` | `LootParams` |
| `LootC` | `LootContext` |
| `LIC` | `LootItemCondition` |
| `LPool` | `LootPool` |
| `RCont` | `RandomizableContainer` |
| `ExecC` | `ExecuteCommand` |
| `Inv` | `Inventory` |
| `FD` | `FoodData` |
| `FP` | `FoodProperties` |
| `KM` | `KeyMapping` |
| `KI` | `KeyboardInput` |
| `MEI` | `MobEffectInstance` |
| `CScr` | `ChatScreen` |
| `CLis` | `ChatListener` |
| `CCC` | `ClientChunkCache` |
| `LLE` | `LevelLightEngine` |
| `LX` | `LevelExtractor` |
| `BSPH` | `BlockStatePredictionHandler` |
| `MH` | `MouseHandler` |
| `InvS` | `InventoryScreen` |
| `GGE` | `GuiGraphicsExtractor` |
| `GuiR` | `GuiRenderer` |
| `ChatC` | `ChatComponent` |
| `CRU` | `ComponentRenderUtils` |
| `SSpl` | `StringSplitter` |
| `FBR` | `FormattedBidiReorder` |
| `FSet` | `FontSet` |
| `GStit` | `GlyphStitcher` |
| `SndM` | `SoundManager` |
| `SndE` | `SoundEngine` |
| `SBL` | `SoundBufferLibrary` |
| `ChanA` | `ChannelAccess` |
| `Library` | `Library` |
| `Channel` | `Channel` |
| `LEH` | `LevelEventHandler` |
| `CDS` | `ClientDebugSubscriber` |
| `SDS` | `ServerDebugSubscribers` |
| `LDS` | `LevelDebugSynchronizers` |
| `TDSS` | `TrackingDebugSynchronizer.SourceSynchronizer` |
| `BDR` | `BrainDebugRenderer` |
| `Main` | *the JVM main thread, not a class* |
| `Netty` | *the Netty event loop, not a class* |
| `Worker` | *the `Util.backgroundExecutor` pool, not a class* |
| `Auth` | *the User Authenticator thread, not a class* |
| `Wire` | *the network between the two programs, not a class* |
| `Disk` | *the save on disk, not a class* |
| `JVM` | *the process itself, not a class* |
| `Hook` | *the Server Shutdown Thread JVM hook, not a class* |

Collisions the pass-2 notebook recorded and the rows above settle: `SL` is
`ServerLevel` (not `ServerLoginPacketListenerImpl`, now `SLPL`, nor
`SpriteLoader`); `CL` is `ClientLevel` (not `ClientPacketListener`, `CPL`);
`CM` is `ChunkMap` (the menus take their own initials); `CH` is `ChunkHolder`
(the client handshake listener is `CHPL`); `GR` is `GameRenderer`
(`GuiRenderer` lengthens to `GuiR`); `TD` is retired in favour of `CTD` /
`TCTD`. Part V (session F) lengthened four later claimants rather than
reassigning a row: `LeverBlock` is `LevB` because `LB` is `LiquidBlock`,
`BlockItem` would be `BItem` because `BI` is `BucketItem`,
`BlockPlaceContext` would be `BPC` because `PC` is `ProtoChunk`, and
`PistonStructureResolver` is `PSR` because `PR` is `PackRepository`. Rows for
`SS`, `ST`, `SP`-as-structure, `TP`, `LX`, `PE` and `C` are left for the part
sessions that own the pages, under the rule above.

Part VI (session G) lengthened five later claimants: `MoveControl` is
`MoveC` because `MC` is `Minecraft`, `SummonCommand` is `SumC` because `SC`
is `StopCommand`, `AttributeMap` is `AttrM` because `AM` is `AtlasManager`
(Part XI), `EffectCommands` is `EffC` because `EC` is `ExecutionContext`
(Part XIII), and `AttributeInstance` follows its map to `AttrI` even though
`AI` is free, because `AI` reads as the AI system on an entities page. Two one-word classes take their own name as a lane under the
short-word rule, `Sheep` and `Shapes`.

Part VII (session H) is the later claimant almost everywhere and lengthened
eleven rows rather than reassigning one: `ChestMenu` is `ChestM`,
`CraftingMenu` `CraftM` and `EnchantmentScreen` `EScr` because `CM` is
`ChunkMap`, `CS` is `ComponentSerialization` and `ES` is `EntityStorage`;
`RemoteSlot` is `RemS` and `ResultSlot` `ResultS` because `RS` is
`RenderSystem`; `ResultContainer` is `ResultC`, `ContainerSynchronizer`
`CSync`, `ContextMap` `CMap`, `LootParams` `LootP`, `LootContext` `LootC`,
`LootPool` `LPool` (`LP` is `LocalPlayer`), `RandomizableContainer` `RCont`
(`RC` is `ReloadCommand`), `ExecuteCommand` `ExecC` (`EC` is
`ExecutionContext`) and `Enchantment` `Ench` (`EH` is `EnchantmentHelper`).
`Consumable` and `BowItem` take `Cons` and `BowI` under the one-word and
collision rules, and `Ignite` takes its own name. `CI`, `RM`, `SRB` and
`LIC` were free. One collision is recorded and **not
yet claimed**: `ES` is `EntityStorage`, so `EntitySection` would have to
lengthen to `ESec` if a later page wants it.

Part X (session K) added twenty-six rows and lengthened seven later
claimants rather than reassigning a row: `SoundEngine` is `SndE` and
`SoundManager` `SndM` because `SE` is `ServerEntity` and `SM` is claimed in
Part XII's prose, `ChannelAccess` is `ChanA` because `CA` means three things
in three unconverted parts, `GuiRenderer` is `GuiR` because `GR` is
`GameRenderer` (the collision the key already recorded), `InventoryScreen`
is `InvS` because `IS` is `IntegratedServer`, `GlyphStitcher` is `GStit`
because `GS` is `GaussianSampler`, and `StringSplitter` is `SSpl` and
`FontSet` `FSet` deliberately — `SS` and `FS` are unkeyed collisions in Part
XII, and leaving them free costs Part X two letters and saves session M a
renaming. `LX` is claimed here for `LevelExtractor`, which five pages in two
parts already use it for, so Part XI's `LightmapRenderStateExtractor` is the
later claimant and lengthens. `Library` and `Channel` take their own names
under the short-word rule.
