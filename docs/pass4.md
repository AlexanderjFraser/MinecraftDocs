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
- The eight generated Reference views (pass 3 added serializers,
  attributes, enchantment hooks and loot-context sets to the four pass 2
  had; the glossary stayed hand-kept): re-derive one sample by hand per
  view — pass 2 found bugs in both generators, and one had reached the
  prose.
- ~~The lane key in `TEMPLATE.md`: every lane's expansion is a class that
  exists.~~ `tools/check_lanes.py` checks it on every deploy, `--strict`
  corpus-wide since session P.
- **Every count is re-counted** (session P's addition 4 in the charter):
  pass-3 sessions K, L, M and N each found a wrong count while redrawing a
  page, three of them load-bearing. Session N of pass 4 is a corpus-wide
  count sweep with one brief.
- **The four session-P pages have never been checked** —
  `rendering/block-entity-rendering`, `commands/entity-selectors`,
  `worldgen/blending`, `worldgen/creating-a-world`. Their claims lists are
  under session P's entry; they get pass 2's completeness question too.
- **The parts-dependency figure** (`src/figures/parts-dependency.md`,
  included by the introduction and `lectures.md`) and the dependency table
  on `lectures.md` are claims: every arrow is a landing page's *before you
  start* entry, and every entry must be used by a sentence in the part.
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
  `brigadier-and-commands`, `the-execution-engine`, `functions-and-macros`
  and `scoreboard-and-data` (parse, suggestions, `ContextChain`, the result
  consumer), `models-and-atlases` and `text-and-fonts` (the atlas and font
  JSON), and `post-processing` (the six chains' JSON).
- **The `execute store` question** on `scoreboard-and-data` — what a failing
  ordinary leaf command writes — is now answerable from Brigadier 1.3.10;
  settle it and remove the page's "cannot be settled from the decompile"
  note.

## Entries

## Session P — The lecture order and the close *(2026-09-03)*

Session P wrote no part; it wrote the lecture map's dependency section and
the parts-dependency figure, four coverage pages, and one sentence or link
on each of eleven sibling pages. Everything below is new to the corpus and
has been checked once by the session and never by an adversary.

### `lectures.md` and `src/figures/parts-dependency.md` — claims about order

- **Every solid arrow in the figure is a landing page's *before you start*
  entry**, and the section says so; check each of the twenty-two arrows
  against the landing page it came from, and each landing-page entry
  against a sentence in the part that uses it (the charter's addition 2).
  The two omitted foundations (Part I anatomy, Part II codecs and
  registries) are asserted to be assumed by every part.
- **"No solid arrow points at an earlier part"** — true by construction of
  the figure; the claim to check is that no landing page lists a later
  part's page that the figure left out. Candidates: Part IX names *the
  client loop* (Part X) as "the deeper version" and the session drew that
  as no arrow.
- **The two dashed arrows**: Part III → Part IV (tickets and loading; the
  environment page), cut "by definition" — `server-level-tick.md` defines
  entity-ticking and block-ticking range before using them — and "by
  order"; Part X → Part V (prediction), cut at Part V by the two identical
  preambles. Both restate landing-page rulings by sessions D/E and F/K.
- **The nine-page table**: each row's "parts whose landing pages assume it"
  was read off the landing pages by the session; re-derive the column by
  grep. In particular: *environment attributes* ← III, VI, XI (Part X's
  `what-makes-a-sound` also names it and Part X's landing page does not);
  *the connection* ← X, XIII; *chunk anatomy* ← V, VI, XII.
- **"Watched straight through, the sidebar order needs one departure from
  itself"** — that the environment page is the only backward dependency a
  straight viewer meets.
- **The Part I ruling**: *what this book skips* second, game tests last
  "because nothing later depends on them" — check that no landing page
  assumes `game-tests`.
- The intro sentence "Nothing in Reference is watched, and nothing in the
  maps is" — check no landing page lists a Reference page in *watch in this
  order* (session O's note).

### `rendering/block-entity-rendering.md` — new, 332 lines, comparison

Drafted by an agent from the decompile; the session re-derived the 26
registrations against 49 `BlockEntityTypes` and the 13 `ID_MAPPER.put`
calls (`grep -c`), the 0.3 fade gate (`LevelExtractor.java:274`), the
equality gate in `BlockEntityRenderDispatcher.tryExtractRenderState`, the
frozen partial tick (`DeltaTracker.getGameTimeDeltaPartialTick` returns 1.0
when frozen and not ignored; `Camera.getCameraEntityPartialTicks` passes
`true`; `GameRenderer.extract` passes `false`), and the three Christmas
implementations (`ChestRenderer` constructor, `IsXmas`, *items/chest.json*'s
*local_time*). Everything else is the agent's evidence. Paths relative to
`reference/26.2/net/minecraft/client/`.

- **The hook**: "the two are drawn at different partial ticks and only one
  of them respects the freeze" — `renderer/GameRenderer.java:407, 416`,
  `renderer/extract/LevelExtractor.java:175, 262` (one world partial tick
  for every block entity); `LevelExtractor.java:222` (per-entity
  `isEntityFrozen`); `Camera.java:138-140`; `GameRenderer.java:619`;
  `world/TickRateManager.java:72-74` (never freezes a `Player`).
  Session-confirmed the three partial-tick sources; "keeps swaying with
  your view bob" is the agent's phrasing of the consequence.
- Counts: 26 of 49 (`BlockEntityRenderers.java` static block;
  `BlockEntityTypes.java`); 24 renderer classes (`ChestRenderer` serves
  three types); the other 23 include FURNACE, HOPPER, BARREL, BEEHIVE; 26
  state classes (27 files with `package-info`); `BedRenderState` the only
  orphan (corpus grep); 13 special renderers under 13 ids; nine implement
  `NoDataSpecialModelRenderer`; eleven import `renderer/blockentity` (all
  but Trident and CopperGolemStatue); three hold a block-entity renderer
  instance (Banner, DecoratedPot, ShulkerBox); `getViewDistance` overridden
  in five files so nineteen take the default 64
  (`blockentity/BlockEntityRenderer.java:27`); `shouldRenderOffScreen`
  overridden in exactly three (`BeaconRenderer.java:128`,
  `BlockEntityWithBoundingBoxRenderer.java:172`,
  `TestInstanceRenderer.java:77`); five states carry another pipeline's
  snapshot (Spawner, Shelf, Campfire, BrushableBlock, Vault).
- Orderings and mechanism: never frustum-tested (`LevelExtractor.java:262-300`
  vs `isEntityVisible` 242-256); fade zeroed within √768 ≈ 27.7 blocks or
  for a previously empty section (`renderer/LevelRenderer.java:588-606`;
  ramp `renderer/chunk/SectionRenderDispatcher.java:253-257`); the chest
  contributes zero quads and adds itself to the section's list
  (`renderer/chunk/SectionCompiler.java:83-88, 97-98`;
  *blockstates/chest.json* → *models/block/chest.json*, particle only);
  **two model tables** (`resources/model/ModelManager.java:91, 95, 110,
  326-327`; `SectionCompiler.java:36`; `renderer/block/BlockModelResolver.java:19-22`)
  and `BlockModelResolver`'s callers are all entity renderers (ten named)
  — note `BlockEntityRendererProvider.Context` carries a
  `blockModelResolver` no block-entity renderer uses; the equality gate
  (`ClientLevel.java:199-206`; `BlockEntityRenderDispatcher.java:68`);
  `BlockEntityRenderer.shouldRender` is a centre-distance test (31-33) vs
  `EntityRenderer.java:66-70` and `Entity.java:2158-2174`; beacon
  horizontal-only (`BeaconRenderer.java:137-140`), view distance = render
  distance × 16 (132-135), `beamRadiusScale` and the scoping reset (47-51),
  `MAX_RENDER_Y = 2048` (25); distances 68 / 96 / 256 / max-of-two
  (`PistonHeadRenderer.java:93-95`, `BlockEntityWithBoundingBoxRenderer.java:176-178`,
  `TheEndGatewayRenderer.java:55-57`, `TestInstanceRenderer.java:82-84`);
  no `finalizeRenderState` counterpart (`BlockEntityRenderer.java` vs
  `EntityRenderer.java:162-172, 313`); the base state five fields
  (`state/BlockEntityRenderState.java:16-20, 27-34`);
  `MovingBlockRenderState` holds the light engine by reference
  (`PistonHeadRenderer.java:86-90`; `entity/state/FallingBlockRenderState.java`);
  `AbstractSignRenderer` calls `Font.split` in submit (53); the spawner
  overwrites the display entity's light (`TrialSpawnerRenderer.java:43-44`);
  the pose pre-translated (`LevelRenderer.java:653-659` vs 634-639); the
  held chest in `handAndScreenSubmitNodeStorage`
  (`GameRenderer.java:367-386, 619-622`); a layer has quads or a special
  renderer, never both (`item/ItemStackRenderState.java:242-253`).
- The Christmas triple: `ChestRenderer.java:46-56` and
  `BlockEntityRenderDispatcher.java:101-105` (constructor runs only on
  reload); *items/chest.json* and `renderer/item/properties/select/LocalTime.java:25`
  (`UPDATE_INTERVAL_MS`); `BuiltInBlockModels.createXmasChest`,
  `block/model/properties/conditional/IsXmas.java`,
  `ConditionalBlockModel.java:22-25`. **"Two of the three notice midnight
  almost at once. The one you are standing in front of does not"** is the
  page's most inference-shaped sentence; check it hardest.
- Editorial: the *why* column of the view-distance table (68 = "a moving
  block starts outside the block it is drawn from"; the structure block;
  the gateway) is the agent's reasoning, not a source comment.
- **Unsettled by the agent**: whether the 0.3 gate is observable at the
  default *chunk section fade-in time*; whether `EnchantTableRenderer`'s
  book and `BuiltInBlockModels.createEnchantingTable`'s `BookSpecialRenderer`
  can both draw for one object; whether a block entity added before the
  first resource reload can be permanently excluded from the global set
  (`ClientLevel.onBlockEntityAdded` with a null renderer).
- **Where the queue entry and session L were wrong**: "26 render states"
  is a file count and 25 are reachable; the territory is ~4,300 lines
  (3,353 + 973), not ~3,300; the extract/submit split is *shorter* than the
  entity side (no finalize); `renderer/special` is reached by two roads
  (item model and block state via `SpecialBlockModelWrapper` in a table
  terrain never reads), which no page said; "a stricter visibility rule
  enforced twice" conflated the section walk + fade + flat radius with the
  off-screen flag's double-draw guard.
- Siblings: `entity-rendering.md`'s *Block entities* paragraph cut to one
  sentence and a link; `block-entities.md` (Part V) and
  `models-and-atlases.md` gained a link each.

### `commands/entity-selectors.md` — new, 313 lines, pipeline with a policy figure

Drafted by an agent from the decompile; the session re-derived the seven
`setWorldLimited` callers and the twenty-one `register` calls
(`grep -c`), the box rule in `EntitySelectorParser.getSelector`, the six
heads' `selectOnlyAlive` / `includesEntities` settings, the linear player
walk in `EntitySelector.findPlayers`, and the seven reads of
`Permissions.COMMANDS_ENTITY_SELECTORS` plus the one grant. Everything else
is the agent's evidence. Paths relative to `reference/26.2/net/minecraft/`.

- **The hook**: "*@p* is not 'the nearest player in this world' … chosen
  from the list of everybody on the server" — case `'p'` sets no
  `worldLimited` (`EntitySelectorParser.java:274-279`); `findPlayers` with
  `isWorldLimited()` false walks `PlayerList.getPlayers()`
  (`EntitySelector.java:240-254`); `ORDER_NEAREST` is `distanceToSqr` with
  no dimension term (`EntitySelectorParser.java:64-68`). Session-confirmed
  the walk; the "raw x, y, z" wording is the agent's.
- Counts: twenty-one names (`EntitySelectorOptions.bootStrap` 92-615);
  seven world-limiting options (lines 117, 138, 144, 150, 156, 162, 168);
  three always-available options *tag*, *nbt*, *predicate* (393, 428, 613);
  four `SetOnceOptionState` options *limit*, *sort*, *scores*,
  *advancements* (`EntitySelectorParser.java:106-112`); thirty-two parser
  fields; thirteen `EntitySelector` fields (57-69, constructor 71); five
  classes and 1,717 lines — **excludes two `package-info.java` stubs**; the
  atlas convention would say seven files and 1,725 lines, and pass 4 should
  pick one convention for the corpus; seven reads of the permission
  (`EntityArgument.java:134`, `GameProfileArgument.java:87`,
  `MessageArgument.java:101`, `ScoreHolderArgument.java:41`,
  `EntitySelector.java:108`, `EntitySelectorParser.java:130, 143`) and the
  grant at `LevelBasedPermissionSet.java:20`; eight `EnderDragonPart`
  sub-entities (`EnderDragon.java:100-108`).
- Orderings: `finalizePredicates` adds rotation and level tests last
  (190-214, called at 525); `EntitySelector.getPredicate` appends
  feature-flag, exact box, range in that order (265-300); `Util.allOf`
  evaluates in order and short-circuits, so the range test runs after an
  *nbt* comparison; `EntitySelectorOptions.get` (628-638) refuses a
  repeated option before its handler runs (`parseOptions:379`).
- Only/never: six heads and the default throws (239-293); only *@e* and
  *@n* add `isAlive` (266, 272, applied 295); `LivingEntity.isAlive`
  (1848-1850) vs `Entity.isAlive` (2386-2388); **no index by entity type**
  (`world/level/entity/EntityLookup.java:23-37` iterates `byId.values()`
  with `EntityTypeTest.tryCast`); **players never get a box**
  (`EntitySelector.java:207-259`; `ServerLevel.getPlayers` 995-1012 is a
  linear walk); the three vanilla commands with a selector-capable argument
  and no `requires` — `MsgCommand`, `EmoteCommands`, `TeamMsgCommand` — from
  46 files under `server/commands/` naming the four argument types;
  `MessageArgument` treats refusal as formatting (139-142) and swallows only
  `ERROR_MISSING_SELECTOR_TYPE` / `ERROR_UNKNOWN_SELECTOR_TYPE` (156-163);
  `EntitySelector.usesSelector` set only by `parseSelector` (229);
  `COMPILABLE_CODEC` compiles with selectors unconditionally allowed
  (45-55); `ServerStatusPinger`'s `ResolutionContext` has no source
  (`client/multiplayer/ServerStatusPinger.java:51-53`;
  `SelectorContents.java:33-36` returns empty); all five classes in
  `server-classes.txt`; the name `EntitySelector` used twice
  (`world/entity/EntitySelector.java`).
- X-not-Y: `getResultLimit` returns the parsed limit only for arbitrary
  order (192-194), consumed at 180 and 235; the box path offers
  `EnderDragon.getSubEntities()` (`Level.java:602-635`) and the walk does
  not (`ServerLevel.java:978-989`); the two structures behind
  `LevelEntityGetterAdapter`; *dx=0* is one block wide and the cube for 8
  spans −8 to +9 (`createAabb:176-188`, `getSelector:148-156`); the delta
  branch beats *distance* (148); *distance=8..* gives no box (150);
  `MinMaxBounds.Doubles.matchesSqr` compares squares
  (`advancements/predicates/MinMaxBounds.java:231, 261`);
  `InvertableSetOptionState`'s two terminal states; `EntityArgument`
  rejects on shape at parse time with *@s* exempt (107-124);
  `EntityArgument.listSuggestions` (128-146) and
  `ClientSuggestionProvider.getSelectedEntities` (77-79); `ORDER_RANDOM` is
  `Collections.shuffle` with no `RandomSource` (73-75); `Bootstrap.bootStrap`
  fills the options once (`server/Bootstrap.java:59`); *gamemode*, *level*,
  *advancements* call `setIncludesEntities(false)` (275, 133, 585).
- **Unsettled by the agent**: whether `Collections.shuffle(List)` is
  unseeded per call (JDK source not in the tree; the page says only that no
  world seed reaches it); whether any vanilla writer puts a
  `SelectorContents` in a status description; whether option-suggestion
  order is stable (Brigadier's `Suggestions.create` sorts, so it should
  be). Two field names for one fact — `EntitySelector.usesSelector` and
  `EntitySelectorParser.usesSelectors` — are both correct and should not be
  "fixed" to match.
- **The queue entry's count was wrong**: "six classes, ~2,136 lines" is
  five classes and 1,717 lines (seven files and 1,725 with the stubs).
- Sibling: `brigadier-and-commands.md`'s selector paragraph shrank to a
  link, dropping four backticked selector strings and the "667 lines"
  aside; its claim "thirteen final fields" is the new page's.

### `worldgen/blending.md` — new, 346 lines, pattern

Drafted by an agent from the decompile; the session re-derived the 193
positions (enumerated dx, dz in −7..7 with dx²+dz² ≤ 64; `Blender.java:76-82`),
the three blendable router functions and their targets
(`NoiseRouterData.java:34-35, 120-123`), the absence of any
`setBlendingData` in the tree, the single `sideByGenerationAge` call with
*false* (`BlendingData.java:101, 108`), and the data-pack counts
(*blend_density* in all 7 noise settings; *blend_alpha* in 9 density
function files; *blend_offset* in 3). Everything else is the agent's
evidence. Paths relative to `reference/26.2/net/minecraft/`.

- **The hook**: "The three splines that shape overworld terrain are swapped
  out for a ground height the game read off the old chunk's blocks…, the
  constant ten, and zero" — `NoiseRouterData.java:34, 35, 120, 121, 123,
  324`; `Blender.java:119-121` (alpha 0 on an exact hit) and 148-150 (alpha
  → 0 as distance → 0). Session-confirmed the targets; the "hardly generated
  at all" framing is the agent's.
- Counts and constants: inner 3×3 for density (`Blender.java:59, 87-89`);
  radius seven derived from the 27-cell range (`Blender.java:56-57`;
  `core/QuartPos.java:25, 29`); 27 cells / 108 blocks and smoothstep over
  28 (132, 148-150); inverse fourth power (137); density lerp within two
  cells, alpha over three (181, 197-198); Y difference doubled (178);
  biome: twelve cells of shift noise, over 28, threshold one half
  (264-267); sixteen columns = 7 inside + 9 outside
  (`BlendingData.java:44-49`, fills 127-165); `BlendingData.Packed` codec
  validates 16 (396-401); eleven surface block types (51); fifteen blocks
  per density cell (206-208, 228-230); 25 columns in the `NoiseChunk`
  constructor (`NoiseChunk.java:123-135`; `forChunk:64`); 1,024-chunk region
  scan and cache (`world/level/chunk/storage/IOWorker.java:41, 86, 97-113`);
  *DataVersion* below 4882 or a *blending_data* compound (129-131); four Y
  levels across 256 columns (`Blender.java:287-296`); within four blocks of
  the box after shift noise ×4 (358-363); box eight wide (395-397).
- Orderings: `NoiseChunk` created at *BIOMES* and cached
  (`NoiseBasedChunkGenerator.java:92-94`; `ChunkAccess.java:438-443`; no
  `noiseChunk = null` anywhere); the flat caches filled before
  `router.mapAll` (`NoiseChunk.java:120-135` vs 141-142); identity swap
  (483); empty blender skips the swap and replaces *blend_density* with its
  child (117, 138-140, 458-459); `ChunkStatusTasks.generateFeatures` primes
  heightmaps before decorating and calls `generateBorderTicks` after
  (`ChunkStatusTasks.java:115, 120, 123`; read at `Blender.java:307`);
  `Blender.of` asks the save first (69-72).
- Only/never/not: `ChunkAccess.blendingData` is `protected final`
  (`ChunkAccess.java:74`), `isOldNoiseGeneration` returns its presence
  (388-390); a neighbour yields data only with a `BlendingData` and
  `getHighestGeneratedStatus` ≥ *BIOMES* (`BlendingData.java:100`); only
  heights are saved — density *transient* (56), `pack` (79-94), codec (395);
  a chunk measures itself once (53, 127, 166); exactly three router
  functions are blendable, all in `registerTerrainNoises` whose three
  callers are the overworld variants (`NoiseRouterData.java:100, 104, 105`);
  `postProcess` wraps every dimension's router (224-227; 253, 287, 295,
  301, 310); the water table follows the old ground
  (`preliminarySurfaceLevel` 249, 335-343; `Aquifer.java:403`);
  `generateBorderTicks` returns unless the generated chunk itself is old
  (`Blender.java:279`) — so the neighbour test at 299 reduces to "not old";
  carvers skip masked positions (`CarvingMask.java:38-40, 52-54`;
  `WorldCarver.java:98`); `Blender.empty` is an anonymous subclass (39-53);
  four `Blender.of` call sites, three eager
  (`ChunkStatusTasks.java:70, 77`; `NoiseBasedChunkGenerator.java:237, 274`);
  the biome answer is a holder or null (267); three cave biomes in
  `BelowZeroRetrogen` (44; resolver 104-116); *Blending: Old* on the debug
  screen (`client/gui/components/debug/DebugEntryChunkGeneration.java:65-66`).
- Deliberately softened: seven "sits inside" the radius-eight window
  (`ChunkPyramid.java:19`; `WorldGenRegion.java:126-133`) — eight would fit
  too, so no claim that seven is maximal.
- **Unsettled by the agent**: how a chunk first acquires *blending_data*
  (three fixers under `util/datafix/fixes/`, out of scope by rule 3; one
  strips the key outside the overworld, so blending is in practice
  overworld-only — a fact the page does *not* state; pass 4 rules whether it
  is sayable); three declared-but-unused constants in `Blender` and a
  cluster in `BlendingData`; the cost of the region scan (asserted as what
  the code does, not measured).
- **Where the queue entry and the brief were wrong**: `ProtoChunk.setBlendingData`
  does not exist; `ChunkSerializer` is `SerializableChunkData`; there are
  five consumers, not three; `generateBorderTicks` fires on the *old* chunk,
  not the new one. 858 lines confirmed (439 + 419).
- Siblings: `terrain.md`'s boundary question now points here (and lost the
  phrase "from four years ago"); `density-functions.md` gained two links;
  `biomes.md` one sentence; `chunk-generation-pipeline.md` and
  `chunk-anatomy.md` one link each; `what-this-book-skips.md` dropped the
  three now-written systems from *Named for a later pass to place*.

### `worldgen/creating-a-world.md` — new, 300 lines, pipeline with a comparison

Drafted by an agent from the decompile; the session re-derived the parked
main thread (`CreateWorldScreen.openCreateWorldScreen` →
`Minecraft.managedBlock`), the live layer list behind *Cancel*
(`PresetEditor.EDITORS` passes `FlatLevelSource.settings()`;
`CreateFlatWorldScreen`'s Cancel calls only `onClose` and `updateLayers`)
and `WorldGenSettings extends SavedData` with its own `SavedDataType`.
Everything else below is the agent's evidence, unchecked by the session.
Paths relative to `reference/26.2/net/minecraft/`.

- **The hook**: "Before the screen can draw a single widget the game has
  already run a complete server-side data-pack load … with the client's
  main thread parked on `BlockableEventLoop.managedBlock`" —
  `client/gui/screens/worldselection/CreateWorldScreen.java:150-168`.
- "`WorldLoader.load` … calls it **after** the worldgen registries and the
  `Registries.LEVEL_STEM` registry are loaded and **before**
  `ReloadableServerResources.loadResources` runs" — `server/WorldLoader.java:38-48`.
- "The registry set that recipes, loot tables and functions are then parsed
  against includes the dimension registry that callback produced" —
  `WorldLoader.java:45-47`.
- "*level.dat* is written by the client, in `Minecraft.doWorldLoad`, before
  the server thread exists — while the settings file is written by the
  server after it starts" — `client/Minecraft.java:2223-2240`;
  `server/MinecraftServer.java:355`, `646-648`.
- "`CreateWorldScreen.onCreate` bakes the dimensions to decide the
  lifecycle … but the `WorldGenSettings` it stores holds the **unbaked**
  selection" — `CreateWorldScreen.java:245-268`.
- "the `MinecraftServer` constructor … builds a fresh rule set from the
  saved-data default and then overlays the screen's values" —
  `MinecraftServer.java:367-370`.
- Counts: three experiments (`data/minecraft/datapacks/`, `FeatureFlags.java:42-45`);
  five presets in the *normal* tag, plus *debug_all_block_states* in
  *extended*; seven world presets as JSON (`WorldPresets.java:39-45`);
  `PresetEditor.EDITORS` two entries; nine flat presets as JSON and ten keys
  (`FlatLevelGeneratorPresets.java:27-36`, `run()` 79-88; `TEST_WORLD` has
  no reader); `RegistryDataLoader.DIMENSION_REGISTRIES` one entry
  (`resources/RegistryDataLoader.java:85`); `WorldOptions` four fields;
  nineteen classes, nine screens, in `worldselection`; six footer buttons on
  `SelectWorldScreen` (79-106; the debug re-create button is in the header);
  `WorldOpenFlows.openWorld` a chain of eight (`WorldOpenFlows.java:248, 257,
  295, 409, 444, 463, 487, 508`); seven listeners in `CreateWorldScreen`;
  `WorldGenSettings` fifty-one lines.
- **"The *Cancel* button on the layer editor does not undo a layer
  deletion"** — `CreateFlatWorldScreen.java:100-103, 177-187`;
  `FlatLevelSource.java:60-62`. Session-confirmed. The agent's further
  inference, *not* on the page: the mutated settings object is the one held
  by the `WORLD_PRESET` registry's `LevelStem`. Pass 4 should say whether
  the next reload rebuilds it.
- "`WorldCreationUiState.setWorldType` … replaces **all** the dimensions";
  "the overworld only. Nothing in the create screen can edit the nether or
  the end" — `PresetEditor.flatWorldConfigurator` / `fixedBiomeConfigurator`
  both call `WorldDimensions.replaceOverworldGenerator`.
- "shows `ConfirmExperimentalFeaturesScreen` only when the requested flags
  are experimental **and** the caller was the data-pack screen" —
  `CreateWorldScreen.java:362, 380, 384-397`.
- "`WorldOptions.parseSeed` … otherwise returns the Java string hash" and
  "an empty box is re-rolling a new random world every time you touch it" —
  `WorldOptions.java:71-88`; `CreateWorldScreen.java:747-749`.
- **"`WorldDimensions.checkStability` only asks whether each of the three
  built-in keys carries the vanilla dimension type and biome source; every
  shipped preset passes"** — `WorldDimensions.java:120-190`. An inference
  from what the method does *not* check (`isStableOverworld` examines noise
  parameters only for `MultiNoiseBiomeSource`); re-derive adversarially.
- "*generator-settings* JSON, parsed … **only when the preset is**
  `WorldPresets.FLAT`" — `server/dedicated/DedicatedServerProperties.java:310-322`;
  "*server.properties* has no rules" — no game-rule read there.
- "Nothing in the family edits an existing world's `WorldGenSettings` in
  place" — `EditWorldScreen.java:44-52`; `WorldSelectionList.java:692-728`.
- "`WorldOpenFlows.recreateWorldData` reads the old world with a
  deliberately **empty** `LevelStem` registry" — `WorldOpenFlows.java:168-170`.
- "an NBT parse that deliberately skips the *Data/Player* and
  *Data/WorldGenSettings* subtrees" — `world/level/storage/LevelStorageSource.java:418-420`.
- "the water in *Water World* arrives as a feature, not as terrain" —
  `FlatLevelGeneratorSettings.java:165-173`; preset at
  `FlatLevelGeneratorPresets.java:82`.
- "the only thing that ever selects it is `CreateWorldScreen.testWorld`" —
  grep of `FLAT_ALL_DIMENSIONS`; `client/gui/screens/TitleScreen.java:183-188`.
- "`WorldGenSettings.CODEC` encodes … to JSON using the old registries as
  context, and re-parses that JSON against the new ones" —
  `CreateWorldScreen.java:411-425`.
- `getDifficulty` hard in hardcore; `isAllowCommands` true in debug, false
  in hardcore; `isBonusChest` false in both — `WorldCreationUiState.java`.
- The *mcworld-* temp directory copied in or deleted —
  `CreateWorldScreen.java:74, 342-355, 464-499, 508-560`.
- **Unsettled by the agent**: whether enabling an experiment makes any
  registry lifecycle non-stable (so whether the create-time warning ever
  fires for an experiment alone); whether the registry-held flat settings
  mutation survives the next reload; the exact save at which
  *data/world_gen_settings.dat* first hits disk (the page says "the first
  save"). `LevelStorageSource.writeWorldGenSettings` and `writeGameRules`
  exist with no callers under `net/` and are not on the page.

### Sibling sentences the session wrote (one line each, all new claims)

- `rendering/entity-rendering.md` — *Block entities* paragraph replaced by
  one sentence: "a different visibility policy, a different partial tick
  and an empty block model".
- `blocks/block-entities.md` — "why a chest's block model is empty".
- `rendering/models-and-atlases.md` — "where those thirteen get their
  geometry".
- `commands/brigadier-and-commands.md` — the selector paragraph now says
  "thirteen final fields" and "resolved against a `CommandSourceStack` much
  later".
- `worldgen/terrain.md` — the boundary answer now calls `BelowZeroRetrogen`
  "the world-deepening path that rides the same hooks".
- `worldgen/biomes.md` — "The two wrappers in the second arrow only do
  anything beside chunks an older version generated".
- `server/starting-a-server.md` — "where the stem was built, by a screen
  or by *server.properties*".
- `reference/level-data-and-rules.md` — "creating a world is who writes
  it".
- `introduction.md` — the lane gate added to *Verified means tested*; the
  dependency-figure caption ("each cut by a definition rather than a
  reordering").
- The glossary gained fifteen entries (five per Part XII page, three each
  for the other two, one shared): *experiment*, *flat level generator
  preset*, *world gen settings*, *world preset*, *world stem*, *compiled
  query*, *selector head*, *world-limited*, *built-in block model*,
  *globally-rendered block entity*, *special model renderer*, *blending
  data*, *blend alpha*, *border tick*, *old chunk*. Each is one sentence
  written from the agent's report; check each against its owner page.

## Session O — Reference *(2026-09-03)*

**Pages rewritten or reshaped.** `reference/README.md` (new, a landing
page), `reference/level-data-and-rules.md` (reshaped around its table),
`reference/math-and-primitives.md` (figure added, surprises list dissolved
to prose), `reference/threads.md` (a new section), `reference/glossary.md`
(eleven entries added, one reordered), `reference/naming-drift.md`
(headings only), `reference/block-update-flags.md` (new, extracted from
`blocks/blocks-and-states.md`, which now links to it).

**Claims introduced, check first.**

- `threads.md`, *The eight client handlers that never hop*: "In
  `ClientPacketListener` 115 handlers do that and eight do not" — counted by
  splitting the class at every `public void handle…(` and testing each body
  for `ensureRunningOnSameThread`; re-derive, and check the common
  listener's thirteen handlers are correctly excluded (`handlePing` hops;
  `the-connection` used to say the ping reply ran on Netty and was corrected
  to *the pong bookkeeping*). Every row's "what it does" is one method body
  read once; `handleLowDiskSpaceWarning` → `Minecraft.sendLowDiskSpaceWarning`
  → `Minecraft.execute` is the row that makes a claim about a second class.
- `math-and-primitives.md`, the coordinate-spaces figure: every edge is a
  named method and every shift count is a claim — `ChunkPos.containing`
  shift 4, `QuartPos.fromBlock` shift 2, `ChunkPos.getRegionX` shift 5 (the
  old page said "32 chunks" and never "shift 5"), `SectionPos.of` from a
  `ChunkPos` plus a section y, and the three packings' bit widths (26/12/26,
  22/20/22, 32/32) copied from the page's own *Three long keys* section.
  Also the new intro sentences: "each a power of two apart from its
  neighbour" and "every conversion is a named static method on the type you
  are converting *to*" — a generalisation the old page did not make; check
  it against every edge in the figure.
- `level-data-and-rules.md`: no new facts, but eleven surprises were
  merged into the sections; the drafting agent's report listed every
  rewording. Two to read closely: "That forwarding is how game time comes
  to be shared by every level" (a causal sentence built from two old ones),
  and "So every level reports the same spawn, and it is not the one
  *level.dat* holds" (the old text said "not the stored one").
- `reference/README.md`, the table's last column: which parts' landing
  pages link each reference page, read off the landing pages today (grep
  `reference/` in `src/systems/*/README.md`); a landing-page edit in a
  later session silently dates it. And "two of these pages (submit phases,
  density-function nodes) are nothing but declaration order".
- `glossary.md`, the eleven new entries — *authority*, *batch*, *event
  loop*, *frame*, *noise cell*, *permission atom*, *permission set*,
  *quart*, *staging buffer*, *submit node*, *unattended command* — each
  written from one sentence of its owner page; the confident ones are
  "an operator's level-based set grants exactly one [atom]", "No packet
  carries one in either direction", "the client parses twice more", and
  "`Minecraft` and `MinecraftServer` are both one" (event loop).
- `block-update-flags.md`: the table moved verbatim; the new opening
  sentence claims `fluids` and `pistons-and-block-events` "mean the same
  bits" when they pass a flag word.

**Standing item added.** The five hand-kept catalogues
(`non-living-damage`, `hud-elements`, `submit-phases`,
`density-function-nodes`, `block-update-flags`) are name-verified from this
session on but have had one reader each; re-sweep every row against the
decompile, hardest on the two that are declaration orders. Strike the
"glossary if generated" clause above — it is hand-kept.

**Diagrams redrawn.** One added (`math-and-primitives`, the coordinate
graph — seventeen edges, each a conversion claim); one added
(`reference/README.md`, the shelf — asserts which tool writes which page).

- **2026-09-03, session L — Part XI Rendering.** Twelve pages: eight
  rewritten (`the-frame`, `the-window`, `blaze3d`, `models-and-atlases`,
  `entity-rendering`, `lightmap-fog-and-sky`, `particles`, and
  `level-rendering` in the act of splitting), two produced by that split
  (`visibility-and-the-frame-graph`, `section-meshing`), one written from
  nothing (`post-processing`), plus a landing page, a new Reference page
  (`submit-phases`), a generated figure and Part XI's section of
  `lectures.md`. `level-rendering.md` is gone and its URL redirects to the
  visibility half.

  **Two errors were found by redrawing, and both are already fixed in the
  pages — check the fixes, not the old claims.**

  1. **`the-window` said three of the six operating-system callbacks reach
     the game through `WindowEventHandler`. Only two do.** `Window`
     registers six GLFW callbacks; `onFramebufferResize` calls
     `WindowEventHandler.framebufferSizeChanged` and `onEnter` calls
     `WindowEventHandler.cursorEntered`, while `onMove`, `onResize` and
     `onIconify` write a field and stop. The interface's third method,
     `WindowEventHandler.resizeGui`, is never called by `Window` at all —
     its callers are `Minecraft` and `Options`. `framebufferSizeChanged` is
     also raised directly by `Window.updateFullscreenIfChanged` and
     `Window.changeFullscreenVideoMode`, so it is not only a callback path.
     The old claim was an inference from three method names lining up with
     three callbacks; verify the new one against `Window`'s registrations
     and its `eventHandler` call sites.
  2. **`level-rendering` conflated two different triggers.** It said
     `LevelExtractor.applyFrustum` re-runs when "the occlusion graph
     invalidates on a camera move quantised to eight blocks, on a
     field-of-view change and on the smart-cull toggle". Those three are the
     triggers for `SectionOcclusionGraph.invalidateIfNeeded`, which schedules
     the **full walk**. The **frustum step** has its own gate:
     `SectionOcclusionGraph.consumeFrustumUpdate` — set by a completed full
     walk and by a partial walk that added a section inside the offset
     frustum — **or** the camera's pitch or yaw crossing a two-degree step.
     `visibility-and-the-frame-graph` now states both clocks separately;
     check both. Corrected in the same paragraph: the old page presented
     "three sections" and "sixty blocks" as two independent numbers, and they
     are one — `MINIMUM_ADVANCED_CULLING_SECTION_DISTANCE` is
     `MINIMUM_ADVANCED_CULLING_DISTANCE` converted to section coordinates.

  **The split.** `level-rendering` became `visibility-and-the-frame-graph`
  and `section-meshing`. Nothing was cut, but the material was divided, and
  pass 4 should read the two together once against the old page, which is in
  git history at commit `03712d1`. The seam: visibility owns `LevelRenderer`,
  `SectionOcclusionGraph`, `Octree`/`VisGraph`/`VisibilitySet`, `Frustum`,
  `LevelExtractor.applyFrustum`, `FrameGraphBuilder` and the pass list,
  `LevelRenderer.prepareChunkRenders` and `ChunkSectionsToRender`, the
  translucency budget and `CardinalLighting`; meshing owns the dirty API,
  `SectionUpdateTracker`, `RotatingSectionStorage`, `RenderRegionCache`,
  `SectionRenderDispatcher`, `SectionCompiler`, `BlockModelLighter`,
  `ChunkSectionLayer`, the `UberGpuBuffer` arenas, the upload callback and
  the fade-in. Two facts are deliberately stated on both pages, once each,
  and must not have drifted: *only visible sections are re-meshed*, and
  *terrain is drawn before the sections queued this frame are compiled*.

  **Claims introduced, by page.** These are what the rewrites added that the
  old pages did not contain. Each was checked against the decompile before
  the session accepted it, which is exactly the level of checking pass 2
  proved insufficient.

  - `the-window`: the candidate loop ends in `MessageBox.error` and the game
    never starts; `RenderSystem.initRenderer` happens *inside* the loop on
    the success path, not after it; `GpuBackend.handleWindowCreationErrors`
    is handed a captured GLFW error and throws `BackendCreationException`;
    the two-of-six callback pairing above; `ClientShutdownWatchdog` is
    started from the window-close callback. Flagged as unverified by the
    drafter: where `Window.getRefreshRate`'s number originates.
  - `the-frame`: the blit is described as going *to the acquired surface
    texture*, where the old page said only "from the main render target".
  - `blaze3d`: two numbers were **corrected**, not introduced. The old page
    compared the backends at "7,461 lines against 5,623"; measured today the
    two trees are **7,477 and 5,627** (40 classes and 28), and 7,477 is also
    what `what-this-book-skips` already claimed for the Vulkan tree, so the
    two pages disagreed. The page now states both counts and the class
    counts. Also corrected: the old page's "Outside `com/mojang/blaze3d/opengl`
    — fourteen files in all" reads as if that package holds fourteen files.
    It holds twenty-eight; *fourteen* is the number of files anywhere in the
    game that import LWJGL's OpenGL bindings, thirteen of them in that
    package plus the native-library bootstrap. Introduced: that changing the
    Graphics API setting needs a restart (`Options.preferredGraphicsBackend`
    adds `Options.TOOLTIP_NEEDS_RESTART` when it differs from the value at
    startup).
  - `visibility-and-the-frame-graph`: the walk may step into a neighbour only
    if the two faces can see each other through that section's geometry
    (`SectionOcclusionGraph.runUpdates`); `FrameGraphBuilder.execute` culls
    before it orders; the *clear* pass wipes colour and depth on the main
    target; the depth copy inside the main pass goes to the translucent,
    item-entity and particle targets; `LevelRenderer.viewArea` is what a
    by-position lookup goes through; and **the entity-outline chain is added
    only when the prepared frame reports an outline** — `LevelRenderer`
    around line 199, `featureFrame.hasAnyOutline()` and a non-null chain. By
    the same evidence the drafter reports that the sky pass and the *always
    on top* pass are conditional too, which the old page's flat "in
    declaration order" list obscured. **Check the conditionality of all four
    passes.**
  - `section-meshing`:
    `SectionUpdateTracker.SectionDirtyState.isDirtyFromPlayer` is what
    *prioritise chunk updates* keys off, travelling through
    `SectionUpdateRenderState` to `LevelRenderer`'s synchronous-rebuild
    decision — and there are two settings, `PrioritizeChunkUpdates.NEARBY`
    (which also takes anything within a near radius) and `.PLAYER_AFFECTED`;
    the rationale given for `SectionUpdateTracker.hasAllNeighbors`, that a
    mesher decides a face by reading the block on the other side of it; and
    "a newly homed slot starts dirty". The drafter also found three things it
    kept *out* of the page, each a possible old-page error worth checking:
    that `LevelExtractor.blockChanged` is itself the halo path while the
    public `LevelExtractor.setBlockDirty` is the `ModelManager.requiresRender`-gated
    entry; that `LevelExtractor.setBlocksDirty` expands its box by one block
    on each side; and that `LevelExtractor.allChanged` also clears tint
    caches and rebuilds `SectionUpdateTracker` at the current render
    distance.
  - `models-and-atlases`: the whole *How an item picks its model* section is
    new — `ItemModelResolver` reading `DataComponents.ITEM_MODEL`, both
    lookups falling back rather than failing, `ClientItem.Properties`
    carrying the hand-swap animation and the GUI-overflow flag, and
    **`ItemModels` registering eight kinds of unbaked item model of which
    only one draws anything itself**. That count and that characterisation
    are the two hardest claims on the page. Also new: the fan-out is
    described as **sixteen** parallel pieces of work — thirteen stitches plus
    three listings — where the old page said thirteen stitches "plus" the
    listings without counting them together.
  - `entity-rendering` and `reference/submit-phases.md`: the Reference page
    is almost entirely new fact and is the largest single body of unchecked
    claims this session produced — the declaration order of the fifteen
    phases, which three are a `TranslucentFeatureRenderPhase` (and that
    `SubmitNodeCollection.translucentCustomGeometry` is *not*, despite the
    name), what files into each phase and on what condition, that a
    see-through name tag emits two nodes, that a quad-particle group lands in
    `SubmitNodeCollection.solid` and `SubmitNodeCollection.afterTerrain` at
    once, the registration order of the thirteen feature renderers, the three
    sweeps `FeatureRenderDispatcher.PreparedFrame.executeTranslucent` makes
    and which phases each drains, and one line per renderer on what it
    writes. **Check this page row by row.** The drafter also contradicts two
    old-page claims that are still standing in the lecture prose: that
    "batching is by feature type, then by `RenderType`" (only batchable
    submit types have a batch key at all — everything else merges by
    adjacency), and that "translucency opts out of reordering rather than of
    merging" (the translucent phase does reorder, by depth-sorting; what it
    opts out of is the *grouper's* reordering).
  - `particles`: the destroy event is raised on the server side too, so the
    trace gains a server-side arrow — `Block.playerWillDestroy` is called
    from both `MultiPlayerGameMode` and `ServerPlayerGameMode`; the broadcast
    is 64 blocks, same dimension, excluding the source when it is a `Player`
    (`ServerLevel.levelEvent`); a level event carries no particle type, which
    is why the override flag cannot apply to it; and
    `ParticleEngine.clearParticles` is the named reload callback. Two
    interpretive glosses with no new mechanism: that the two independent
    32-block checks can disagree because the camera moves while the packet is
    in flight, and that the reservoir's squared probability makes a particle
    storm degrade gradually rather than hit a wall. Carried over verbatim and
    **not** re-verified: "eight call sites in all" bypass
    `ClientLevel.addParticle`.
  - `lightmap-fog-and-sky`: dissolving the attribute enumeration meant
    pinning each constant to the thing that reads it, and those *mappings*
    are new even though the constants are not — which fog environment reads
    which of the eight fog attributes (`AtmosphericFogEnvironment` and
    `WaterFogEnvironment`), which of the lightmap's four colours comes from
    which attribute (`LightmapRenderStateExtractor`),
    `EnvironmentAttributes.STAR_ANGLE` as one of the sky's three angles, and
    `ClientLevel.animateTick` scattering
    `EnvironmentAttributes.AMBIENT_PARTICLES`. Also: the raw-clock claim in
    the hook is asserted of exactly two renderers, `CloudRenderer` (drift
    from game time) and `WeatherEffectRenderer` (the column seed) — check
    that no third renderer reads the clock. And a counting nuance: the old
    page said the sky can be skipped "five different ways" and then added the
    boss-bar suppression "on top of that"; the new page keeps five for
    `LevelRenderer.addSkyPass`'s own conditions and makes the boss bar a
    separate sixth. Confirm which reading is right.

  - **`post-processing` is entirely new and nothing has ever checked it.**
    It is the one page in the corpus written from the decompile with no
    pass-2 history behind it, so pass 4 should treat it as a pass-2 subject
    rather than a pass-3 one: falsify every sentence, not just the ones
    listed here. Five of its load-bearing claims were verified by the session
    itself before it shipped, and those five are the *least* likely to be
    wrong: the six chain ids are the only ones ever requested
    (`GameRenderer.BLUR_POST_CHAIN_ID`, `LevelRenderer.ENTITY_OUTLINE_POST_CHAIN_ID`,
    `LevelRenderer.TRANSPARENCY_POST_CHAIN_ID`, plus three built from the
    camera entity's class in `GameRenderer.checkEntityPostEffect` — those are
    all five `ShaderManager.getPostChain` call sites); every post-processing
    draw is **three vertices** (`PostPass`, one `RenderPass.draw` of three);
    the six chains declare **twenty-six passes** between them (blur 6, spider
    10, entity_outline 4, creeper 2, invert 2, transparency 2 — counted from
    the JSON in `reference/26.2/assets/minecraft/post_effect/`, which also
    confirms spider's four internal targets and blur's one);
    `PostChain.process` carries `@Deprecated`, builds its own
    `FrameGraphBuilder` and imports one target named *main*, and its only two
    callers are in `GameRenderer`; and a pass's custom uniforms are packed
    with `Std140Builder` and uploaded in `PostPass`'s **constructor**, so
    they are written once at load and never again.

    Everything else on the page is unchecked, and these are the claims most
    worth attacking because the page's argument rests on them: that a
    JSON-declared uniform's per-entry *name* is read by no codec and members
    match the GLSL positionally; that *blur.json* declares a radius of zero
    and *box_blur* falls back to a member of the *Globals* block that
    `GlobalSettingsUniform.update` rewrites each frame from
    `OptionsRenderState.menuBackgroundBlurriness`; that an input's sampler
    name gets *Sampler* appended when the `BindGroupLayout` is built; that
    two inputs on one pass sharing a sampler name is rejected at load; that
    the internal/external target distinction is enforced by subtracting the
    chain's own targets from `PostChainConfig.Pass.referencedTargets` and
    requiring the remainder to be a subset of the caller's allowed set; that
    none of the six shipped chains asks for a persistent target; that a
    compilation failure is cached as a permanent absence and reported to
    `Minecraft.triggerResourcePackRecovery`; that the cache key is the chain
    id alone and not the id plus the allowed target set; that the outline
    chain's first pass detects edges in **alpha**; that
    `LevelRenderer.doEntityOutline` composites outside the graph after
    `GameRenderer.renderLevel` returns; that the blur runs inside
    `GuiRenderer.draw` with the depth buffer cleared between the two halves
    of the GUI, bounded by `Screen.extractBlurredBackground` calling
    `GuiGraphicsExtractor.blurBeforeThisStratum` only when
    `Options.getMenuBackgroundBlurriness` is at least one; that neither
    deprecated-door caller passes an inspector, so the blur and the spectator
    shaders appear in no F3 profiler slice; and that `Minecraft.setCameraEntity`
    is what clears the effect when you leave first person. The per-chain
    table's *what a player sees* column is interpretation of GLSL the book
    does not quote, and should be read as such.

    One consequence for other pages: `post-processing` states that the
    transparency chain is gated on `OptionsRenderState.improvedTransparency`
    and not on any graphics preset, and that there is no *Fabulous* setting
    any more. If that is right, check whether `options` in Part X says
    otherwise. And one thing to re-check on the next version bump
    rather than now: `ShaderManager.CompilationCache` keys a loaded chain by
    its id alone and not by the allowed target set it was validated against,
    so two callers wanting one chain under different permissions would share
    whichever object was built first. No two callers do today.
  **What `lightmap-fog-and-sky` gave back to Part IV.** The page's opening
  hundred lines re-taught `EnvironmentAttribute`, its flags and builder, a
  twenty-four-item enumeration of `EnvironmentAttributes` constants,
  `EnvironmentAttributeSystem`'s layer stack, `Timeline`, `Timelines` and
  `ClockTimeMarkers`. All of it is **deleted, not moved**: Part IV's
  `environment-attributes-and-timelines` already owned every one of those
  subjects, and the session confirmed each name is still present there before
  deleting — `AttributeTypes`, `ColorModifier`, `Timeline.Builder`,
  `ClockTimeMarkers`, `EnvironmentAttribute.isSpatiallyInterpolated` and
  `Timelines.EARLY_GAME` all checked. **Pass 4 should confirm nothing was
  lost across that seam** and should read the two pages together. Kept on the
  Part XI side because they are its own: `ClientLevel`'s two extra attribute
  layers are the lightning flash, `DimensionType.skybox` and its three
  values, and `BiomeSpecialEffects` hollowed out to water, grass and foliage.

  **The diagrams.** Every figure in the part is new or redrawn, and each one
  asserts an ordering. New flowcharts: the substrate-under-pipeline figure on
  the landing page, whose arrow labels are hand-off claims; the backend retry
  loop and the six-callback figure in `the-window`; the façade-over-backend
  figure in `blaze3d`; the five-stage pipeline and the pass-order figure in
  `visibility-and-the-frame-graph`, the second of which is a declaration-order
  claim *and* a conditionality claim; the sixteen-fan barrier figure in
  `models-and-atlases`; the four-stage figure in `entity-rendering`; the
  admission flowchart in `particles`; and in `post-processing`, the
  parse-compile-declare-draw figure. Redrawn with corrected lanes, and in one case with its `rect` blocks
  removed: one frame in `the-frame`, one draw in `blaze3d`, a block placed in
  `section-meshing`, a zombie in `entity-rendering`, the sun going down in
  `lightmap-fog-and-sky`, the break puff in `particles`. One generated
  figure, `tree-EntityRenderState.svg`, whose counts — 98 render states, 70
  of them living — come from `map_source.py` and want re-deriving like the
  atlas's other numbers.

  **The landing page and `lectures.md`** claim that Part XI is a substrate
  under a pipeline; that `the-frame` is watchable before the substrate it
  stands on; that the only hard prerequisite is Part X's `the-client-loop`,
  with `resource-system` (Part II) and `environment-attributes-and-timelines`
  (Part IV) as per-lecture ones; and that lectures four and five are one
  journey seen from two ends. The landing page also states the renderer's
  size as 1,179 classes and 87,000 lines against `net/minecraft/server`'s 420
  and 53,000 — **re-derive both**. Session I's inventory reported 1,187 and
  97,864 for "the rendering tree" without saying which packages it counted,
  this session could not reproduce it, and the page now states its own
  package set and counting rule rather than inheriting the number.

- **2026-09-02, session F — Part V Blocks.** Seven pages: four rewritten
  (`blocks-and-states`, `block-interaction`, `block-breaking`,
  `block-entities`) and three produced by the notebook's confirmed three-way
  split of `redstone` (`signal-and-dust`, `pistons-and-block-events`,
  `diodes-and-observers`), plus a landing page and Part V's section of
  `lectures.md`. `redstone.md` is gone and its URL redirects to
  `signal-and-dust`.

  **Read the provenance note before trusting anything below.** The session
  was interrupted after four pages had been drafted: two of the four agent
  reports arrived, two did not, and the three redstone pages were then
  written by the session itself directly from the decompile. The pages divide
  into four classes of evidence and pass 4 should weight them differently.

  1. **`block-interaction`** — agent-drafted, report received, and every
     correction in it **re-derived by the session** against the source.
  2. **`block-breaking`** — agent-drafted, report received, corrections
     **not** independently re-derived (the interrupt landed first). Treat its
     twelve claimed corrections as unverified leads, not as findings.
  3. **`blocks-and-states`** and **`block-entities`** — agent-drafted, **no
     report survived**, so nothing is recorded about what they changed
     relative to the old page beyond the session's own read of the finished
     text. These two need the full protocol, starting with a diff against
     their pass-2 versions in git.
  4. **The three redstone pages** — session-written, every claim derived from
     the decompile in this session, and every diagram read separately from
     its prose.

  - **Corrections the session derived itself, method by method.**
    - **Block events are not "a tick late".** The old `redstone` diagram
      carried a *next tick* bar over `ServerLevel.runBlockEvents`, and that is
      wrong for the common cases. `MinecraftServer.processPacketsAndTick`
      drains queued packets and *then* calls `MinecraftServer.tickServer` in
      the same lap, and the *blockEvents* section of `ServerLevel.tick` sits
      after *tickPending* and *chunkSource* and before *entities* — so an
      event queued by a packet handler or by a scheduled tick drains in the
      **same** tick, and `ServerLevel.runBlockEvents` loops until its set is
      empty, so an event queued during the drain does too. Only the entity and
      block-entity phases, and a chunk that is not block-ticking, push one to
      the next tick. `reference/glossary.md` already said "usually within the
      same tick", so the corpus contradicted itself.
      `pistons-and-block-events` now states all five cases.
      **Re-derive the phase order and each case.**
    - **`RepeaterBlock.LOCKED` does not survive on the client, and the old
      page's reason for saying so was wrong.** It claimed locking "is a shape
      update, which is why it survives on a client that never runs neighbour
      updates". `RepeaterBlock.updateShape` recomputes the lock only when the
      level is not client-side, and `ObserverBlock.startSignal` returns
      immediately on a `ClientLevel` — both shape hooks opt out of the client
      explicitly, and a client keeps no appointment book to fire into anyway.
      `diodes-and-observers` gives the real reason the shape channel is the
      right one: it carries a neighbour's state change even when the neighbour
      issued no neighbour update.
    - **`blocks-and-states`' opening overclaimed and was narrowed.** Its own
      closing question is right and its hook was not: `Block.getId` and
      `Block.stateById` are tolerant, but
      `ClientboundBlockUpdatePacket.STREAM_CODEC` reads the same table through
      `ByteBufCodecs.idMapper`, which is `IdMap.byIdOrThrow`. Check the
      narrowed sentence, and check the Q&A's account of which paths use which
      lookup.
    - **Dust powers the block below it and never the one above.**
      `RedStoneWireBlock.getSignal` answers zero for `Direction.DOWN` and
      answers full power for `Direction.UP` with no connection test. This is
      nowhere in the pass-2 corpus.
    - **`LeverBlock.pull` is handed a null player**, so — unlike the door —
      nobody is excluded from the sound and the clicker hears the server's
      copy. And `LeverBlock.useWithoutItem` writes no state at all on a
      `ClientLevel`, so a lever is not predicted.
    - **`PistonBaseBlock.checkIfExtend` runs a dry-run
      `PistonStructureResolver.resolve` before queueing** an extend event, so
      a piston with an immovable wall in front of it queues nothing at all.
    - **A diode's `HorizontalDirectionalBlock.FACING` points at its input**,
      and `DiodeBlock.updateNeighborsInFront` acts on the opposite side. Any
      sentence in the corpus saying a diode "faces its output" is wrong.
    - **`ComparatorBlock.checkTickOnNeighbor` books on a second condition**
      the repeater has no analogue of: whenever the computed output differs
      from the int held in the `ComparatorBlockEntity`, not only when the
      powered flag disagrees with the input.
    - **`SignalGetter.getSignal` is a maximum, not a choice.** For a redstone
      conductor it takes the larger of the block's own weak signal and
      `SignalGetter.getDirectSignalTo`. Three Part V pages used to phrase this
      as one *or* the other.

  - **Claims the rewrite introduced, per page.** Check these first and
    hardest.
    - **`signal-and-dust`** (session-written): *the number* — **forty-two**
      neighbour updates per changed wire, derived as seven
      `Level.updateNeighborsAt` calls (the position plus its six neighbours,
      collected in a hash set in
      `DefaultRedstoneWireEvaluator.updatePowerStrength`) times six directions
      per `CollectingNeighborUpdater.MultiNeighborUpdate` — **re-derive both
      factors**. Also: the framing that the staircase of intermediate values
      follows from the recursion terminating on *value* rather than on
      distance; the three-direction-order table; the claim that
      `RedStoneWireBlock.getConnectionState`'s completion pass, not
      `RedStoneWireBlock.shouldConnectTo`, is what points dust into a piston;
      `RedstoneTorchBlock.isToggledTooFrequently` burning out on the eighth
      surviving entry using a literal rather than
      `RedstoneTorchBlock.MAX_RECENT_TOGGLES`. The flowchart asserts an
      ordering from arrival to fan-out.
    - **`pistons-and-block-events`** (session-written): the five-case tick
      analysis above; the census of block-event users — four blocks
      (`PistonBaseBlock`, `NoteBlock`, `PotentSulfurBlock`,
      `ComparatorBlock`) plus seven block entities through
      `BaseEntityBlock.triggerEvent` — **counted by grep and worth
      re-counting**; the flag table (324 for the placeholders and the arm, 82
      for vacated positions, 67 for the base, 18 for a destroyed block) and
      the claim that only the first of those omits `Block.UPDATE_CLIENTS`;
      that the crushed-block particle event in `PistonBaseBlock.moveBlocks` is
      raised on the **client** side only; that the middle
      `SignalGetter.hasSignal` in `PistonBaseBlock.getNeighborSignal` is dead
      code because `Blocks.pistonProperties` declares a piston never a
      redstone conductor; that `PistonMovingBlockEntity.finalTick` writes
      flags 3 and writes **air** for the source piston, against
      `PistonMovingBlockEntity.tick`'s 67; that
      `PistonMovingBlockEntity.TICKS_TO_EXTEND` is declared and never read.
      The sequence diagram asserts four tick boundaries.
    - **`diodes-and-observers`** (session-written): the whole comparison
      table, which is a claim about *three* differences and no others; "a
      diode never writes into its target"; that the signal leaves through
      `DiodeBlock.onPlace` rather than through `Level.setBlock`'s fan-out,
      because `DiodeBlock.tick` writes with flag 2 alone; the priority account
      (`TickPriority.EXTREMELY_HIGH` / `VERY_HIGH` / `HIGH` for the repeater,
      only `HIGH` / `NORMAL` for the comparator, and `NORMAL` only from
      `DiodeBlock.setPlacedBy`); the item-frame rule (exactly one, facing the
      comparator's way, else neither reading is taken); container fullness as
      each stack's count over **that stack's own** maximum; the claim that an
      observer sees a door opened by hand. The flowchart asserts which channel
      each of the three listens on.
    - **`block-interaction`** (agent, session-verified): bit 8 read as
      *player-caused* by `LevelExtractor.blockChanged`; the copper door as
      proof the path never reads `BlockTags.WOODEN_DOORS`; `InteractWithDoor`
      reading `BlockTags.MOB_INTERACTABLE_DOORS` while the older goals read
      `DoorBlock.isWoodenDoor`; that opening a door makes navigating mobs
      repath through `ServerLevel.sendBlockUpdated`; that a disabled item
      aborts the whole hand loop; the eight-row gate table's *what the client
      gets* column, including "nothing, not even the receipt" for
      `ServerGamePacketListenerImpl.hasClientLoaded`; the chain-limit count
      resetting in a `finally`. The agent also flagged a **duplicated swing
      branch** in `ServerGamePacketListenerImpl.handleUseItemOn` — the
      server-swing test appears twice in structurally identical arms — which
      reads like a decompiler artefact. The page describes the behaviour
      rather than the shape. Settle it.
    - **`block-breaking`** (agent, **not** session-verified): the plus-one
      identity, i.e. that `ServerPlayerGameMode.incrementDestroyProgress`'s
      *(elapsed + 1)* is exactly the client's first `Minecraft.continueAttack`
      in the same client tick as `Minecraft.startAttack`; "about two ticks of
      slack" at the 0.7 bar for stone; that the delayed path calls
      `ServerPlayerGameMode.destroyBlock` rather than
      `ServerPlayerGameMode.destroyAndAck`, so a failure there sends no
      correction; that the first crack stage broadcast is 1 rather than 0;
      that `LevelExtractor` picks the deepest crack within 32 blocks **of the
      camera**. Plus its twelve claimed corrections — among them that reach
      and the height check sit outside the action switch and so gate ABORT and
      STOP too, that `MobEffectUtil.getDigSpeedAmplification` returns the
      maximum of haste and conduit power rather than stacking them, that
      `Block.popResource` jitters on all three axes, that the durability cost
      is skipped because hardness is zero rather than because
      `Tool.damagePerBlock` is zero, and that three blocks override
      `BlockBehaviour.attack` rather than one. **None of these were
      re-derived.**
    - **`blocks-and-states`** and **`block-entities`** (agent, **no report**):
      unknown. Diff both against their pass-2 versions in git before checking.
      Claims the session noticed while reading and did not verify: that
      exactly two blocks override
      `BlockBehaviour.BlockStateBase.shouldChangedStateKeepBlockEntity`
      (`CopperChestBlock` and `CopperGolemStatueBlock`); that
      `CopperGolemStatueBlockEntity` overrides the update *packet* but not the
      *tag*; that eight classes override
      `BlockEntity.preRemoveSideEffects`; the nineteen-classes / twenty-types
      sync count; `Level.setBlock`'s four false-returning cases; and that
      `LevelExtractor.setBlockDirty` re-meshes only when
      `ModelManager.requiresRender` says the two states look different. The
      session did verify one of `block-entities`' orderings: the client's
      block-entity pass runs after its entity pass and before
      `ClientLevel.tick`, in `Minecraft.tick`.

  - **The landing page and the lecture order.** Part V's `README.md` claims
    the part is a hub and six spokes, that `blocks-and-states` is what the
    other six reach into, and that the interaction/breaking pair is one
    lecture in two halves. It also makes a **dependency ruling pass 4 should
    test**: Part V is watched *before* Part X's `prediction-and-acks`, on the
    grounds that the two click pages' shared preamble is all either lecture
    needs. Check that the preamble is sufficient and that it contradicts
    nothing in `prediction-and-acks`.


- **2026-09-02, session E — Part IV The world.** Ten pages: five rewritten
  (`chunk-anatomy`, `chunk-generation-pipeline`, `lighting`, `chunk-storage`,
  `environment-attributes-and-timelines`), four produced by the two confirmed
  splits (`scheduled-ticks` + `fluids` from `block-ticks-and-fluids`,
  `game-events-and-vibrations` + `points-of-interest` from
  `game-events-and-poi`), and `level-data-and-rules` reframed as Reference —
  plus a landing page and Part IV's section of `lectures.md`.
  `tickets-and-loading` was session A's pilot and was not rewritten.
  **Check the four split pages hardest**: a split re-attributes every fact,
  and a fact that changes owner is a fact that moved without a diff. Every
  draft was diffed against its old page from the agent's report before
  acceptance; the corrections marked *(session-verified)* were re-derived
  from the decompile by the session itself, method by method.

  - **Twelve pass-2 errors found.** Re-check each *fix*, not only the old
    claim.
    - `lighting` had the light broadcast **backwards**. It said the packet
      goes to the watching players "with border players included";
      `ChunkHolder.broadcastChanges` passes *borderOnly* **true** for the
      light packet and false for block changes, and
      `ChunkMap.isChunkOnTrackedBorder` keeps only players for whom some
      neighbour of the chunk is untracked. Light updates reach the edge of a
      player's tracking view **only**. The old page's "up to nine packets
      for one torch" went with it. *(session-verified)*
    - `game-events-and-poi` said POI updates are "deferred through the
      server's task queue, **even from the server thread**", so "a record
      appears a task later than its block and any read in between sees the
      old answer". False for the ordinary case:
      `MinecraftServer.scheduleExecutables` is *running a task or not on this
      thread, and not stopped*, so on the Server thread outside a queued task
      `BlockableEventLoop.execute` runs the body **inline** and the record
      appears synchronously. Deferral is the worldgen-worker case and the
      nested-task case. *(session-verified)*
    - `scheduled-ticks` (from `block-ticks-and-fluids`): the tick drain was
      said to be skipped "whenever `TickRateManager.runsNormally` is false,
      which covers stepping and sprinting as well as a plain freeze".
      `TickRateManager.tick` sets its flag to *not frozen, or frozen with
      ticks left to run*, so `/tick step` **runs** the drain, and the sprint
      path never touches the flag. *(session-verified)*
    - `chunk-anatomy`'s palette tier table put biomes' one-, two- and
      three-bit linear rungs on the same *1–4 bits* row as block states.
      `Strategy.createForBiomes` has linear rungs at 1, 2 and 3 only and is
      `Configuration.Global` from 4 bits up — no four-bit linear rung for
      biomes and no hashmap tier at all. *(session-verified)*
    - `chunk-anatomy` said of `LevelChunk.setBlockState` that "neighbour
      *updates* are not here — they are `Level.setBlock`'s job". Partly
      false: `BlockBehaviour.BlockStateBase.affectNeighborsAfterRemoval` runs
      inside `LevelChunk.setBlockState`, on a `ServerLevel`, when the block
      changed or the new block is a `BaseRailBlock`, and the flags carry
      `Block.UPDATE_NEIGHBORS` or a piston move. *(session-verified)*
    - `chunk-anatomy` also conflated the two halves of the block-entity
      removal gate — `BlockEntity.preRemoveSideEffects` is what the client
      and `Block.UPDATE_SKIP_BLOCK_ENTITY_SIDEEFFECTS` skip, not the removal
      — and "a client section's `LevelChunkSection.isRandomlyTicking` is
      false forever" is over-strong, because a client-side write does move
      `LevelChunkSection.tickingBlockCount`. *(agent, re-read by the session)*
    - `environment-attributes-and-timelines` said "the night curve can dim a
      nether-red fog and a taiga-blue fog by the same factor". **The nether
      has no day timeline**: its dimension type's *timelines* is
      *#minecraft:in_nether*, which resolves through *#minecraft:universal*
      to `Timelines.VILLAGER_SCHEDULE` alone. Only the overworld tag adds
      day, moon and early game. *(session-verified)*
    - `environment-attributes-and-timelines` said a positional read
      "recomputes the whole layer stack on **every call**, every time". The
      sampler's positional flag is computed from whether any *layer* is an
      `EnvironmentAttributeLayer.Positional`, **not** from the attribute's
      own flag, so a nominally positional attribute that no biome mentions
      is memoised for the tick like any other. *(session-verified)*
    - `environment-attributes-and-timelines`, four more: "`TimeCommand` is
      the only class outside `world/clock` that touches `ServerClockManager`
      directly" — false; "the two positionless readers" — there are three
      `EnvironmentAttributeSystem.getDimensionValue` call sites; "all of it
      scoped to a clock through `/time of`" — the same subtree is registered
      directly on `/time` against `DimensionType.defaultClock`; and
      "`ServerLevel.tick`'s very first statement". *(agent)*
    - `chunk-generation-pipeline` was self-inconsistent about the noise fork:
      one section said "biomes and noise fork to the pool" flatly while its
      step 8 said only `NoiseBasedChunkGenerator` does. Only the latter is
      true, and the old page's stated *reason* for the biome fork ("it is on
      the base `ChunkGenerator.createBiomes`, so every generator forks") is
      wrong, because `NoiseBasedChunkGenerator` overrides it. *(agent)*
    - `chunk-generation-pipeline` singled out "*SURFACE*'s distance-0
      requirement on *NOISE*" as "the one that matters most". That is the
      automatic parent requirement every step carries and distinguishes
      nothing; the radius-1 rows are what stack into the 11. *(agent)*
    - `fluids` (from `block-ticks-and-fluids`): "seven blocks out
      `FlowingFluid.getNewLiquid` reaches zero, nothing is rescheduled"
      conflates two stopping mechanisms — the front stops because
      `FlowingFluid.spreadToSides`' gate computes zero at amount 1, while
      `getNewLiquid` returning empty is what happens when the *supply* is
      cut. And `LavaFluid.spreadTo` turns the target to stone only when that
      block is a `LiquidBlock`. *(agent)*
    - `game-events-and-poi`: arrival is **⌊distance⌋ − 1** ticks after
      selection, not ⌊distance⌋ — `VibrationSystem.Ticker.tick` decrements
      the travel time inside the same call that selected the candidate, so
      anything under two blocks arrives on the selecting tick.
      `VibrationSystem.User.requiresAdjacentChunksToBeTicking` is true for
      the shrieker as well as the sensor, and its test also requires each of
      the nine columns to come back non-null from
      `ServerChunkCache.getChunkNow`. *(session-verified for the decrement)*
    - `game-events-and-poi` gave `ValidateNearbyPoi` for *HOME* as running
      "each tick within 16 blocks". It is in the **rest** package at
      priority 3, so it only runs while `Activity.REST` is active — which
      means the stale-`GlobalPos` answer needs *and it is night* too.
      *(agent)*

  - **The claims each rewrite introduced**, per page. None was fact-checked
    in pass 2.
    - **`chunk-anatomy`** — the hook (a two-state section costs what a
      sixteen-state one costs, and the seventeenth re-encodes 4,096 entries)
      rests on three legs: `Strategy.createForBlockStates`' always-four-bits
      rung, `PalettedContainer.pack` taking its width off the same ladder,
      and `LinearPalette.idFor` → `PalettedContainer.onResize` →
      `PalettedContainer.Data.copyFrom`. Then: `SerializableChunkData.read`
      on the server thread while only `SerializableChunkData.parse` is on the
      pool; `read` returning a `ProtoChunk` in every case; `ImposterProtoChunk`
      and `EmptyLevelChunk` being subclasses of the two lines rather than
      four peers; `EmptyLevelChunk.getFullStatus` flat `FullChunkStatus.FULL`;
      `LevelChunk.getBlockState` answering air from
      `LevelChunkSection.hasOnlyAir` without a palette; `BulkSectionAccess`
      as the second `LevelChunkSection.acquire` holder; `SectionCopy` storing
      null for an air-only section; `SingleValuePalette.idFor` jumping 0 → 4
      bits in one step; `LevelChunkSection.recalcBlockCounts` reachable only
      from the two-container constructor, whose only caller is
      `SerializableChunkData`; `LevelChunkSection.isRandomlyTicking` having
      exactly one reader outside its class;
      `LevelChunk.EntityCreationType.QUEUED` having **no caller anywhere**;
      `LevelChunk.getBlockEntity` promoting pending NBT on any creation type;
      `ChunkStatus.FINAL_HEIGHTMAPS`; and the twelve ordered steps of the
      write path as a table — check that table row by row.
    - **`chunk-generation-pipeline`** — the hook (529 holders claimed before
      a step runs) and: `ChunkGenerationTask.create` taking the generation
      pyramid's radius **unconditionally**, before any disk read; the
      per-layer sweep radii 11, 11, 3, 3, 2, 2, 2, 1, 1, 0, 0, 0 (derived by
      replaying `ChunkStep.Builder` — re-derive these); the loading pyramid's
      accumulated FULL requirement being *SPAWN* at 0 and *INITIALIZE_LIGHT*
      at 1; `ChunkStatusTasks.full` unwrapping an existing
      `ImposterProtoChunk` and replacing nothing in that case;
      `GenerationChunkHolder.replaceProtoChunk` throwing on a changed slot;
      the dispatcher's four-priority bookkeeping queue;
      `ChunkTaskPriorityQueue.PRIORITY_LEVEL_COUNT` being derived from
      `ChunkLevel.MAX_LEVEL` rather than the literal 46;
      `ChunkPyramid.SAFETY_MARGIN_CHUNKS` computing to **90** chunks;
      *STRUCTURE_STARTS* needing *EMPTY* at 0 (the old table said "—"); the
      second *EMPTY* sweep reading only chunks the first missed because
      `GenerationChunkHolder.acquireStatusBump` fails for holders already
      there; and **five** steps leaving the worldgen executor, six inline,
      plus *EMPTY* — the figure asserts all of it, so check it node by node.
      *(The session verified `ChunkGenerationTask.getRadiusForLayer` picks
      the pyramid from the task's needs-generation flag, so the figure's
      radii are the generation-pyramid ones and `EMPTY`'s first sweep is the
      loading pyramid's 1; the caption now says so.)*
    - **`lighting`** — the hook (no light thread, no light phase; the kick is
      the idle poll) and: the border-only broadcast above; the queued light
      task's runnable running on the light executor, not the server thread;
      `LevelLightEngine.runLightUpdates` running the block engine to
      completion then the sky engine, so the four stages happen **twice** per
      batch; `ThreadedLevelLightEngine.runUpdate` taking a window of
      min(size, 1000) and the POST pass removing that same window;
      `ChunkMap.scheduleUnload` as the second caller of
      `ThreadedLevelLightEngine.tryScheduleUpdate`;
      `ChunkHolder.sectionLightChanged` returning false with no bit set when
      there is no ticking chunk, *after* marking unsaved;
      `ClientPacketListener.applyLightData` ending in
      `LevelLightEngine.setLightEnabled`; enabling being inside
      `LightEngine.propagateLightSources` rather than
      `ThreadedLevelLightEngine.lightChunk`; the 27-section figure deriving
      from a flood reaching **thirteen** blocks plus the one-block halo; and
      `SectionUpdateTracker.hasAllNeighbors` checking the eight surrounding
      columns.
    - **`chunk-storage`** — the hook (the eager sweep and the wall-clock
      autosave) and: `ChunkMap.setChunkUnsaved` being installed only at the
      moment a chunk becomes full, so the eager set never holds a generating
      chunk; `/save-all` forcing a write on a no-save world while an autosave
      does not; `ImposterProtoChunk` never being written;
      `ChunkMap.saveChunkIfNeeded` accepting only `LevelChunk` and
      `ImposterProtoChunk`, so a `ProtoChunk` is written only by the unload
      path; the in-file/sidecar ordering asymmetry stated as a principle
      (**session-verified against `RegionFile.write`**: allocate, write,
      headers, `RegionFile.writeHeader`, commit, free — the sidecar's commit
      being the move); `RegionFileVersion.VERSION_GZIP` having a null option
      name so it is readable but unselectable (**session-verified**); the
      `StrictQueue.FixedPriorityQueue` ordinal scan behind `IOWorker`'s three
      lanes; the unload task **re-arming** on a new sync future rather than
      only re-checking; `EntityStorage.loadEntities` running its datafix on
      the server thread; and `ChunkMap.saveAllChunks` with flush computing
      its holder list once and looping until a pass saves none.
    - **`scheduled-ticks`** — the hook (dedup by type and position only) and:
      the dedup slot being released in the **collect** phase, not at run;
      `LevelTicks.hasScheduledTick` and `LevelTicks.willTickThisTick`
      answering different questions, with their caller lists; two further
      comparators the old page did not name
      (`LevelTicks.CONTAINER_DRAIN_ORDER`, `LevelChunkTicks.SUB_TICK_ORDERING`);
      the gate being per **chunk**, not per position; random ticks stopping
      one ring sooner than scheduled ticks because
      `ChunkMap.forEachBlockTickingChunk` wraps
      `DistanceManager.forEachEntityTickingChunk`; the budget being per
      `LevelTicks.tick` call, so 65536 each for blocks and fluids; the
      **inference** that a block tick booking a delay-0 fluid tick is caught
      in the same level tick while the reverse waits — flagged by its own
      author as the page's one inference rather than a reading;
      `LevelTicks.clearArea` / `LevelTicks.copyAreaFrom` touching block ticks
      only, with gametest rather than structure placement as the caller;
      `SavedTick.filterTickListForChunk`; the repeater priorities
      (`TickPriority.HIGH` on, `TickPriority.VERY_HIGH` off,
      `TickPriority.EXTREMELY_HIGH` under `DiodeBlock.shouldPrioritize`,
      `TickPriority.NORMAL` only from `DiodeBlock.setPlacedBy`) —
      **session-verified**, as are the two-tick delay and the placement of
      the turn-off booking inside `DiodeBlock.tick`'s *not on* branch; and
      lava being the only randomly-ticking fluid.
    - **`fluids`** — the hook (four independent slope searches, and a side
      that cannot be *replaced* still votes) is **session-verified against
      `FlowingFluid.getSpread`**: a strictly better score clears the
      collected winners **before** the `FluidState.canBeReplacedWith` test
      and the running minimum is updated regardless, so an unreplaceable near
      neighbour both empties the map and suppresses the rest. Then:
      thirty-seven fluid states and roughly 120 positions per side (both
      **derived arithmetic** — re-derive); `LiquidBlock.getFluidState`
      clamping the level so `FlowingFluid.getLegacyLevel` is lossy for
      falling flows; a waterlogged block reporting a **source** and therefore
      never being drained by a fluid tick; `WaterloggedTransparentBlock`
      being the only block that reports a falling source;
      `EnvironmentAttributes.WATER_EVAPORATES` read positionally while
      `EnvironmentAttributes.FAST_LAVA` is not; the nether's dimension type
      setting both; `LiquidBlock.shouldSpreadLiquid` being a no-op for water
      because its whole body sits inside a lava test;
      `LiquidBlock.updateShape` scheduling with no `shouldSpreadLiquid` gate;
      and the reach figures (water 7, lava 3, fast lava 7 — derived).
    - **`game-events-and-vibrations`** — the hook (one tick late, six rays,
      and `SculkSensorBlock.stepOn` bypassing the cascade —
      **session-verified**: `stepOn` tests `SculkSensorBlock.canActivate` and
      not-a-warden, calls `VibrationSystem.User.canReceiveVibration`, then
      `VibrationSystem.Listener.forceScheduleVibration`, which goes straight
      to `VibrationSelector.addCandidate` past
      `VibrationSystem.User.isValidVibration` and
      `VibrationSystem.Listener.isOccluded`). Then: the arrival correction
      above; `LevelChunk.getListenerRegistry` creating a registry for any
      section merely queried; `DynamicGameEventListener.move` doing nothing
      when either chunk is not `ChunkStatus.FULL`; the allay carrying **two**
      listeners; the position source resolving between the two validity
      gates; `isOccluded` short-circuiting on the first clear ray; the
      redstone distance recomputed from block positions at arrival; the full
      step condition (`Entity.moveDist` past `Entity.nextStep`, and on ground
      *or* climbable *or* crouching-with-zero-clip *or* on rails) replacing
      the old "on the ground and not swimming"; resonance posting at the
      **neighbour's** position before tendrils-clicking; and the four tag
      contents read from the data pack.
    - **`points-of-interest`** — the hook (claimed when a path exists, and the
      ticket and the *occupied* flag never speak) and: **two release paths
      the old page missed** —
      `SetWalkTargetFromBlockMemory` calling `Villager.releasePoi` when the
      dimension differs, when the cant-reach memory exceeds 1200 ticks, or
      after a thousand failed intermediate-position tries
      (**session-verified**), and `VillagerMakeLove` claiming a bed for a
      baby and releasing it if the birth fails; `PoiTypes.TEST_INSTANCE`
      missing from the old catalogue; zero-ticket types never being occupied
      and therefore never village centres; `PoiSection.refresh` reusing
      existing records so a repair does not reset ticket counts;
      `AcquirePoi` taking at radius 1 around the path target and
      **discarding** the take's result; `PoiManager.isVillageCenter` using
      the non-loading getter, so the village graph only sees sections already
      in memory; and the whole *who else asks* table of radii, every number
      new.
    - **`environment-attributes-and-timelines`** — the layer-stack figure is
      new and asserts the whole order; the corrections above; plus the
      biome-layer count (eleven attributes across sixty-six biome files,
      *visual/sky_color* in fifty-six), the nine weather attributes and the
      *rain minus thunder* blend, the client flash layer's fixed lerp toward
      a named colour rather than "toward white", `Timelines.EARLY_GAME` using
      `BooleanModifier.AND`, all four vanilla timelines running on the
      overworld clock, the `/time` rate range, and the routine time broadcast
      being every **twenty** ticks with an empty clock map.

  - **The landing page and `lectures.md` are claims about order.** Part IV's
    landing page asserts that the first five lectures are a forward-only
    chain, that `environment-attributes-and-timelines` depends on nothing
    else in the part, that Part IV needs Part III in front of it and nothing
    after it, and that render distance, simulation distance and the
    mob-spawning radius are three different radii of which only two are
    settings. Each is checkable.

  - **`level-data-and-rules` moved to Reference** and its body was *not*
    re-verified this session — only its header, its links and its framing
    changed. Pass 2 found eleven wrong file paths on it; re-check the paths
    and the who-owns-what table again.

  - **Two claims their own authors flagged as unverified**, both worth a
    direct read: `scheduled-ticks`' delay-0 cross-queue inference, and
    `points-of-interest`' statement that a consistency repair never resets
    tickets, which was confirmed for the reuse-by-key path but not for a
    position whose *type* changed between the record and the block.


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

- **2026-09-03, session G — Part VI Entities.** Nine pages, seven of them
  rewrites and two new, plus three Reference pages. Everything below is a
  claim pass 3 *introduced*; pass 4 checks these first and hardest.

  **Corrections this session made to pass-2 text — re-check the fix, not
  just the old claim.** Each was re-derived from the decompile by the
  session as well as by the drafting agent.
  - `NaturalSpawner`: the biome **energy budget runs before the mob is
    constructed**, as the second conjunct of the pre-construction guard in
    `NaturalSpawner.spawnCategoryForPosition`, not after the
    `Mob.checkSpawnRules` pair as the old page (and this session's own
    ruling) said.
  - `NaturalSpawner.INSCRIBED_SQUARE_SPAWN_DISTANCE_CHUNK` is
    `Mth.floor(8.0F / Mth.SQRT_OF_TWO)` = **5**, and its only reader is
    `DistanceManager.hasPlayersNearby`, as the ≤5 fast-yes arm of a
    `TriState` whose >8 arm is a literal. The old page said it "drives the
    eight-chunk square".
  - `EntitySpawnRequest.ignoreChecks` is **never true** anywhere in 26.2;
    the old page said it was used to build the spawner's display mob.
  - `EntityTypes.ITEM_FRAME`'s `EntityType.updateInterval` is
    `Integer.MAX_VALUE` (seven types are), so the interval branch never
    fires again after tick zero — which is *why* `ServerEntity.sendChanges`
    has an item-frame bypass. The old page said the interval "is why an
    item frame updates slower than a player".
  - `ServerEntity.handleMinecartPosRot` does **not** bypass the send gate;
    it is called from inside it. There is exactly **one** bypass, the
    `ItemFrame` branch. The old page named two.
  - `ServerLevel.tick`'s *chunkSource* phase is **after** block and fluid
    ticks and before block events and entities — the old page said "near
    its start". Session-verified from the profiler pushes.
  - `LivingEntity.shouldTravelInFluid` reads the **cached** in-water and
    in-lava flags; the live `FluidState` is used only by
    `Entity.canStandOnFluid`. The old page said it reads the live state.
  - `Attributes.FRICTION_MODIFIER` scales only the block-friction term;
    both the 0.91 and the 0.98 are scaled by `Attributes.AIR_DRAG_MODIFIER`.
  - `Attributes.DEFAULT_ATTACK_SPEED` has **no callers**; weapons write the
    subtraction as a literal. The old page built a sentence on it.
  - `Mob.getApproximateAttributeWith` is `ItemAttributeModifiers.compute`'s
    only caller but is itself called from six sites, armour as well as
    weapons.
  - **Only `Villager` has a schedule.** `Brain.setSchedule` has two call
    sites, both in `Villager`; the other **nineteen** brain mobs use
    `Brain.setActiveActivityToFirstValid`. The old page framed that as the
    exception used by three mobs. Session-verified by grepping every caller.
  - The profiler listing's nesting: *jump* and *travel* are **siblings**
    of *ai*, not children of it.
  - `SummonCommand` goes through `ServerLevel.tryAddFreshEntityWithPassengers`,
    which refuses on a duplicate UUID anywhere in the passenger stack — a
    gate no page had.
  - `entity-anatomy`'s subpackage table summed to 639 of a stated 716
    (`world/entity` itself and `entity/schedule` were missing); rebuilt to
    twelve rows summing to 716.
  - The non-living `Entity.hurtServer` population is **21**, not "about
    thirty"; 55 files declare the method and 33 of those are `LivingEntity`
    descendants. `Entity.hurtServer` is **abstract**.
  - `Sheep`'s `Shearable` siblings are five, not three (`CopperGolem` and
    `SulfurCube` were missing).
  - Eight direct callers of `MoveControl.setWantedPosition` bypass the
    pathfinder, not six — `Fox` and `Rabbit` were missing.
  - **`ArmorStand` is a `LivingEntity`**, so the old page's roster of
    classes that "override `Entity.hurtServer` directly and never touch
    armour, i-frames or the combat tracker" led with a class on the wrong
    side of its own split; an armour stand does go through the reduction
    pipeline, and the old page's closing claim that the armour-stand
    damage-type tags "exist only for that code" went with it.
  - `AbstractArrow.onHitEntity` applies `EnchantmentHelper.modifyDamage` to
    `AbstractArrow.baseDamage` **first** and multiplies by speed after, so
    Power raises the base rather than the product. The old page had the two
    the other way round.
  - `CombatTracker` expiry is **not** only a background timer:
    `CombatTracker.recordDamage` calls `CombatTracker.recheckStatus` as its
    first statement, so it is also a side effect of the next hit. The old
    page said explicitly that it was not.
  - The third genuinely positional damage source is `ExplodeEffect`, an
    **enchantment** effect, positional only when it is not attributed to its
    user — not "a loot-table explode effect".
  - An ownerless `AbstractArrow` is its **own** causing entity, not a null
    one, which is what `ServerPlayer.hurtServer`'s unwrap re-asks about.

  **New pages, whose every claim is new.**
  - **`authority.md`** — the whole page. Highest-risk items: that
    `Entity.isLocalInstanceAuthoritative` is final and unoverridden; the
    three-column table (a tracked mob, a player, a ridden boat, each read on
    both sides) — **eight rows, each a separate claim**; that both base
    client-authority predicates delegate to the controlling passenger, which
    is the vehicle model; that `ClientboundMoveVehiclePacket` is sent only
    on a **rejection** and that the client applies it only for a vehicle it
    is authoritative for, then echoes back; that
    `ClientPacketListener.handleEntityPositionSync` and
    `ClientPacketListener.handleMoveEntity` update the position codec and do
    **not** move a locally authoritative entity; that
    `SweetBerryBushBlock.entityInside` picks its movement measure off
    `Entity.isClientAuthoritative`; and the six-gate list at the end (each
    gate names a different predicate — check them one at a time).
  - **`pathfinding.md`** — the whole page. Highest-risk: the budget is
    `Attributes.FOLLOW_RANGE`'s **base** value times sixteen at construction
    and the **modified** value (or `PathNavigation.setRequiredPathLength`,
    whichever is larger) times sixteen afterwards, and the same number is
    the region radius plus an 8 or 16 offset; the seven classes that raise
    the required length and their values; that the A\* **heuristic is
    multiplied by 1.5**, so the search is deliberately greedy and the result
    is not the shortest path; that a failed search still returns a
    best-effort path with `Path.canReach` false; that the closed set is
    accumulated only while something is subscribed to
    `DebugSubscriptions.ENTITY_PATHS`; the two give-up timers and their
    arithmetic (100-tick stuck check at speed times 100 times 0.25, with the
    speed *squared* below 1.0; per-node timeout at three times distance over
    speed times 20); and that `PathType`'s negative malus means impassable
    across 27 constants.
  - **`reference/non-living-damage.md`** — twenty-one rows, hand-kept, each
    read one class at a time. Check the `ItemFrame` two-hit rule, the
    `EndCrystal` dragon immunity, the `VehicleEntity` accumulator and its
    creative-player discard, and the claim that `Player.attack` consults
    `Entity.isAttackable` and `Entity.skipAttackInteraction` before
    `Entity.hurtServer` is reached at all. `ShulkerBullet.hurtServer` checks
    **nothing at all**, not even `Entity.isInvulnerableToBase`, and always
    returns true — the one row with no guard.
  - **`reference/attributes.md`** and
    **`reference/entity-data-serializers.md`** are generated by two new
    `gen_reference.py` views. Check the **regexes**, not only the output:
    pass 2 found that three of the four existing views had silently dropped
    rows to an over-narrow pattern. The attribute regex assumes every
    registration is a single-line `new RangedAttribute(...)`; the serializer
    view reads declaration order and registration order as two separate
    lists and reports any declared-but-unregistered serializer.

  **Rewritten pages: the hooks, which are the sharpest new claims.**
  `entity-anatomy` — the pig default reaches the network and not the save
  file, with the whole path (`ByteBufCodecs.registry` →
  `IdMap.byIdOrThrow` → `DefaultedMappedRegistry.byId` never null, versus
  `EntityType.CODEC` = `Registry.byNameCodec` through the `Optional`
  lookup). `entity-lifecycle` — one y roll per category per chunk per tick,
  uniform from the world bottom to `Heightmap.Types.WORLD_SURFACE` plus one,
  with only x and z jittered across three group attempts.
  `synched-entity-data` — ids are `ClassTreeIdRegistry` ordinals with the
  spans `Entity` 0–7, `LivingEntity` 8–14, `Mob` 15, `AgeableMob` 16–17,
  `Sheep` 18, and both `SynchedEntityData.MAX_ID_VALUE` and
  `ClientboundSetEntityDataPacket.EOF_MARKER` are declared and unused.
  `attributes` — Strength II sends no packet, and the eight non-syncable
  names. `movement-and-collision` — the inside-block replay's ordering and
  the `InsideBlockEffectType` flush order, and that `Entity.visitedBlocks`
  dedupes across the whole replay rather than per segment.
  `ai-goals-and-brains` — the schedule is an `EnvironmentAttribute` looked
  up **by position**, and the within-tick priority claim that
  `UpdateActivityFromSchedule` at priority 99 runs after every behaviour it
  could affect, so a switch never bites in the tick it lands.
  `damage-and-death` — the silent-partial-hit flag, and the five families.

  **Every diagram in the part was redrawn.** Fifteen figures across nine
  pages, and each arrow is an ordering claim: check them arrow by arrow,
  separately from the prose. The three most load-bearing are
  `entity-lifecycle`'s **spawn filter cascade** (every rejection in source
  order, with the only-now-is-the-mob-constructed boundary drawn),
  `attributes`' two-dirty-set flowchart (which set a change lands in, and
  that they are not a partition), and `damage-and-death`'s reduction
  flowchart (a dozen links, each owning one multiplication, with the running
  number on every edge).

  **Process note.** All seven rewrites arrived with a full claim-diff from
  their drafting agent. `damage-and-death`'s came last and was **also**
  audited independently by the session against the decompile before it
  arrived — its non-living section, reduction pipeline, blocking path and
  `CombatRules` constants were re-derived here and the two accounts agree.
  That page is the one in the part with two independent audits.

- **2026-09-03, session H — Part VII Items and inventories.** Eight pages,
  five rewritten and three new, every one drafted by an agent against the
  old page and diffed on arrival. **Fifteen figures, thirteen of them new or
  redrawn.** The part's two Reference catalogues are generated
  (`enchantment-hooks`, `loot-context-params`), so pass 4 should re-derive
  one row of each by hand rather than reading the table.

  **Nine pass-2 errors were found and corrected while rewriting.** These are
  the corrected claims, and pass 4 should confirm the corrections rather
  than the originals:
  `items-and-stacks` — `Item.Properties.repairable` is **eager**, not a
  delayed component (it takes a bootstrap registration lookup at class-init
  and stores an unresolved `HolderSet`), and `Inventory.tick` is reached
  from `Player.aiStep`, not `Player.tick`.
  `using-an-item` — **`CrossbowItem.useOnRelease` is the only override of
  `Item.useOnRelease` in the tree**; the old page said the bow, the crossbow
  and the trident all take that branch. The bow and trident are
  release-ended because their duration is 72000 and their
  `Item.releaseUsing` does the work, not because a predicate says so. *This
  one was audited twice: the session read it independently before the
  agent's report arrived, and the two agree.*
  `containers-and-menus` — the state id is compared before the click is
  applied and **branched on after**; and the two `AbstractContainerMenu.doClick`
  branches with no floor check are `ContainerInput.SWAP` and the painting
  phase of `ContainerInput.QUICK_CRAFT`, not the four the old page implied.
  `recipes` — `DecoratedPotRecipe` is a `CustomRecipe`, so **nine** of the
  fourteen crafting serializers are special, not eight; and eleven
  `SlotDisplay` variants are registered, not the eight listed.
  `enchantments` — **twenty-four** of the thirty-one effect components carry
  the decode-time validator, not ten; the three effect registries hold 6,
  15 and 16 entries, so it is fifteen of the sixteen location-based effects
  that are the entity effects, not fourteen of fifteen.
  `enchanting` — `/enchant` does **not** skip the supported-items and level
  rules: it rejects a level above the maximum outright (where the anvil
  clamps) and applies the same `Enchantment.canEnchant` predicate. What it
  skips is the *primary*-items filter, `DataComponents.ENCHANTABLE` and the
  cost.
  `loot-tables` — Fortune and Looting do **not** read
  `LootContextParams.ENCHANTMENT_LEVEL`: `ApplyBonusCount` and
  `BonusLevelTableCondition` read `LootContextParams.TOOL`,
  `EnchantedCountIncreaseFunction` and
  `LootItemRandomChanceWithEnchantedBonusCondition` read
  `LootContextParams.ATTACKING_ENTITY`; `ENCHANTMENT_LEVEL` is written only
  by the five enchantment effect contexts and read only by
  `EnchantmentLevelProvider`. Also, the single chest's menu provider **is**
  the block entity — the old trace drew `ChestBlock` handing to
  `ServerPlayer`.
  `contexts-and-predicates` — the old "five sets have no loot caller"
  sentence listed six sets under a count of five and included
  `LootContextParamSets.COMMAND`, which does have one
  (`ItemCommands.applyModifier`). The replacement claim, which pass 4 should
  re-count from scratch: **twelve of the twenty-six sets never roll a
  `LootTable`**. And `EntityPredicate.matches` builds no context;
  `EntityPredicate.createContext` does.

  **Claims introduced, per page** — the rewrites' new material, which pass 4
  checks hardest.
  `items-and-stacks`: the pop time as the five-tick hotbar squeeze and its
  writers; `DataComponents.COMMON_ITEM_COMPONENTS` as ten entries including
  an empty `ItemEnchantments`; twenty `delayedComponent` call sites in the
  whole game; `PatchedDataComponentMap.remove` storing an empty optional as
  a **tombstone**; `DataComponents.DAMAGE` as the only
  `ignoreSwapAnimation` component; the mining entry point
  (`ServerPlayerGameMode.destroyBlock` → `ItemStack.mineBlock` →
  `Tool.damagePerBlock`) and the copy taken before the damage; the break as
  entity event 47 with `LivingEntity.breakItem` re-deriving
  `DataComponents.BREAK_SOUND`; thirteen pixels of durability bar; exactly
  two `Item.inventoryTick` overrides (`CompassItem`, `MapItem`); the client
  binding components through `RegistryDataCollector`.
  `using-an-item`: what `useOnRelease` actually buys (a final
  `CrossbowItem.onUseTick` through the re-entry in
  `LivingEntity.releaseUsingItem`); five further call sites of
  `LivingEntity.releaseUsingItem`; the release carrying **no sequence
  number and no acknowledgement**, and `handleUseItem` snapping the
  rotation where `handlePlayerAction` does not — so the shot uses the
  server's last-known rotation; the client's draw spending no ammo and
  shooting nothing (`DataComponents.INTANGIBLE_PROJECTILE`);
  `EnchantmentHelper.onProjectileSpawned` running twice when ammo and
  weapon differ; the bow's shoot sound reaching the shooter only as the
  server's broadcast; `ServerPlayerGameMode.useItem` skipping
  `AbstractContainerMenu.sendAllDataToRemote` mid-use; the bow's three-stage
  pull as *assets/minecraft/items/bow.json*; the bow inheriting
  `UseEffects.DEFAULT` while `Item.Properties.spear` overrides it;
  `EntityEvent.USE_ITEM_COMPLETE` as the name of event 9.
  `containers-and-menus`: `HashedPatchMap.matches` owning the removed-set
  and per-component comparison (not `HashedStack.matches`);
  `HashOps.CRC32C_INSTANCE` and the 256-entry cache reaching each
  `RemoteSlot.Synchronized` through `ContainerSynchronizer.createSlot`;
  `CraftingMenu.finishPlacingRecipe` as a **third** caller of
  `CraftingMenu.slotChangedCraftingGrid`; `TransientCraftingContainer`
  calling back from `Container.setItem` always and `Container.removeItem`
  only on a real removal (so "on every write" was too strong); the click
  table's per-kind button semantics; the client never generating a state id;
  the 128-slot cap as the codec's; the closing transfer's shared set stated
  as the 36 main and hotbar slots (a derivation — check it).
  `recipes`: no `CustomRecipe` overriding `Recipe.display`;
  `TransmuteRecipe` returning one display per legal material count, so one
  recipe occupies many consecutive ids; `RecipeDisplayEntry.canCraft`
  returning false for an absent ingredient list and true for an empty one;
  `AbstractCraftingMenu.finishPlacingRecipe` as the hint parameter's real
  caller; the `RecipeCache` at ten entries, static on `CrafterBlock`;
  exactly five `RecipeBookMenu` subclasses while `RecipeBookCategories`
  still declares stonecutter and smithing; `Inventory.isUsableForCrafting`
  gating the pull as well as the tally; `ClientboundUpdateRecipesPacket`
  sent from exactly two places; `SelectableRecipe.SingleInputEntry.noRecipeCodec`
  writing the ingredient **and** the display.
  `enchantments`: forty-three vanilla enchantments; Fire Aspect's numbers
  from its JSON; `TargetedConditionalEffect.equipmentDropsCodec` pinning the
  affected target to `EnchantmentTarget.VICTIM`; the chain by which
  `ItemStack.getDamageSource` always reaches the single-entity constructor,
  which is why `DamageSource.isDirect` holds; `Player.itemAttackInteraction`
  running only on a true return from `Entity.hurtOrSimulate`;
  `Entity.baseTick` skipping the burn in lava and clearing fire for a
  fire-immune entity; five client callers of `CrossbowItem.getChargeDuration`
  (the old page said four); Fortune having **no** effect component and
  Looting exactly one; `LivingEntity.activeLocationDependentEnchantments` as
  the per-slot store; Lunge's impulse scaled flat.
  `enchanting`: the table charging the **slot index plus one**, not the
  displayed cost; the bottom slot's cost floored at twice the shelf count;
  thirty-two bookshelf offsets; the clue being a genuine member of the list
  you will receive, with the plain-book path deleting one entry at random
  first; every path transmuting `Items.BOOK` before enchanting, which
  changes which component the write lands in;
  `ItemStack.enchant` → `EnchantmentHelper.updateEnchantments` as the shared
  tail of all five paths; the anvil's four price components, the prior-work
  tax on both inputs, the flat 40 firing only when an enchantment actually
  transfers, the rename cap at 39 and the 40-and-over withholding; the
  grindstone paying its refund as orbs at the block; five vanilla
  enchantments declaring a narrower primary set; `SetEnchantmentsFunction`
  as the only ceiling-breaker; `/enchant` accepting level 0 and doing
  nothing; six of seven `VanillaEnchantmentProviders` entries being
  `SingleEnchantment`, which never asks whether the item supports the
  enchantment; villager trades running loot functions; `CreativeModeTabs` as
  a sixth producer; the ten data slots' split (3 costs, 1 seed, 3
  enchantment clues, 3 level clues); `EnchantmentNames.initSeed` running
  once per frame.
  `contexts-and-predicates`: validation comparing against
  `ContextKeySet.allowed` rather than `required`, so an element reading an
  optional key passes load-time validation and can still throw;
  `LootContextParamSets.ALL_PARAMS` never building a `ContextMap` at all;
  twenty-seven overriders of `getReferencedContextParams`; the two hard
  validators building a resolver-less `ValidationContext`, so a
  `ConditionReference` is rejected outright; `LootContextArg` and the three
  target enums; the predicate resolved at parse time by
  `ResourceOrIdArgument` where the selector option looks its own up and
  returns a silent false; both command call sites pre-seeding the recursion
  guard; the three-way random-sequence precedence on
  `LootContext.Builder.create`; twenty condition types and eight number
  providers, with the two codec-leniency rules; `SlotSource` as a third
  `LootContextUser` family; the network exclusion restated as absence from
  `RegistryDataLoader.SYNCHRONIZED_REGISTRIES`.
  `loot-tables`: forty-two of the forty-three functions extending
  `LootItemConditionalFunction`, whose failed condition is a **no-op, not a
  veto**; nine entry types; 117 named keys in `BuiltInLootTables` plus two
  colour families; `MonsterRoomFeature`'s two chest attempts;
  `StructurePiece.createChest` as the structure-side seed writer;
  `trySaveLootTable` writing the seed only when non-zero; the weight being
  floored **and then** discarded at or below zero, which are two steps;
  `ByteBufCodecs.fromCodecWithRegistries` as the fallback that carries
  `DataComponents.CONTAINER_LOOT` to the client;
  `AbstractVillager.addOffersFromTradeSet` using `TradeSet.randomSequence`;
  two callers of `MinecraftServer.getRandomSequence`;
  `ShulkerBoxBlock.getDrops` and `DecoratedPotBlock` as the only dynamic
  drops.

  **The diagrams.** Fifteen figures: two containment and pattern flowcharts
  (`items-and-stacks`, `enchantments`), five decision flowcharts (the
  server's resync ladder, the ending guard, one roll, `selectEnchantment`,
  the recipe load and its four indexes), and eight sequence diagrams. Check
  arrow by arrow, and in particular: `loot-tables`' trace, whose two
  orderings were corrected this session (the block entity is its own menu
  provider; `ClientboundOpenScreenPacket` precedes `ServerPlayer.initMenu`);
  `enchantments`' Fire Aspect trace, whose closing packet arrow became a
  note because `SynchedEntityData` does not send through the packet
  listener; and `using-an-item`'s two traces, which are deliberately
  isomorphic — if one is wrong the other probably is too.

  **The landing page and `lectures.md`** claim that the three engines depend
  on the vocabulary and on nothing of each other, and that Part XIII needs
  `contexts-and-predicates`. Both are orderings to check.

- **Session I (Part VIII The player), 2026-09-03.** Seven pages: two rewritten
  in place (`player-anatomy`, `the-sword-swing`), one edited hard
  (`input-to-movement`), one renamed (`hunger-xp-and-effects` →
  `hunger-and-experience`) and three new (`the-two-phase-tick`,
  `status-effects`, `the-spear`), plus the landing page. Everything except
  `the-spear` is pass-2 prose re-cut; **`the-spear` is entirely new material
  and should be checked first and hardest**, because no pass-2 agent has ever
  read those classes.

  **`the-spear`'s claims, all from `PiercingWeapon`, `KineticWeapon`,
  `Item.Properties.spear`, `LivingEntity.stabAttack`, `Player.stabAttack`,
  `Minecraft.startAttack`, `MultiPlayerGameMode.piercingAttack`,
  `ServerGamePacketListenerImpl.handlePlayerAction` and `ItemStack.onUseTick`:**
  that `Item.Properties.spear` attaches nine components and the two attribute
  modifiers listed in the table (check the `AttackRange` numbers 2.0 / 4.5 /
  2.0 / 6.5 against the record's field order — `minReach`, `maxReach`,
  `minCreativeReach`, `maxCreativeReach`, `hitboxMargin`, `mobFactor` — and
  the seven materials); that the stab packet carries no entity id and dummy
  position and direction; that `handleAttack` refuses a piercing weapon while
  the `STAB` case requires a non-spectator and a five-tick
  `Player.cannotAttackWithItem` tolerance; that `PiercingWeapon.attack` uses
  the **attribute value** of `Attributes.ATTACK_DAMAGE` and hits every entity
  along the ray under `ClipContext.Block.COLLIDER`; that
  `PiercingWeapon.canHitEntity` is the shared filter for **both** components;
  that `Item.getUseDuration` is 72000 for a kinetic weapon and
  `LivingEntity.startUsingItem` allocates `recentKineticEnemies` server-side
  only; that `ItemStack.onUseTick` **replaces** `Item.onUseTick` for a kinetic
  weapon; that `KineticWeapon.damageEntities` uses the **base** value of
  `Attributes.ATTACK_DAMAGE` and `Entity.getKnownSpeed` scaled by twenty,
  taking the root vehicle for a non-player passenger; that the three
  `KineticWeapon.Condition`s are independent and any one of them produces a
  hit; that the non-player action factor is 0.2 and therefore *lowers* the
  thresholds; that the hit feedback is entity event 2 → `LivingEntity.onKineticHit`,
  throttled by `KineticWeapon.HIT_FEEDBACK_TICKS`; that
  `CriteriaTriggers.SPEAR_MOBS_TRIGGER` counts living entities stabbed; and
  the page's hook — **`Player.stabAttack` skips both cooldown curves when the
  player is currently using an item in that slot**, so a charge is uncharged
  and a stab is not. Also check the mob roster (`SpearUseGoal`,
  `SpearApproach`, `SpearAttack`, `SpearRetreat`; `Zombie`, `ZombifiedPiglin`,
  `PiglinAi`) and the claim that `KineticWeapon.forwardMovement` is read only
  by `SpearAnimations`.

  **One pass-2 claim was corrected while redrawing.** `the-sword-swing`'s old
  numbered list gave `Player.canCriticalAttack` as the crit gate; the crit is
  `fullStrengthAttack && canCriticalAttack`, so the attack-strength scale
  above 0.9 is part of the crit condition and the page now says so. Re-derive
  it, and with it the whole flowchart, which is the session's one figure that
  asserts an arithmetic **order**: base and boost are scaled separately, the
  item bonus is added to the base *before* the ×1.5, and the boost is added
  after it.

  **Claims moved rather than written.** The authority matrix was **deleted**
  from `input-to-movement` and `player-anatomy` and replaced by a link to
  `entities/authority.md` plus two named consequences (fall damage via
  `Entity.doCheckFallDamage`; the ground flag). Check that nothing true was
  lost in the deletion, and that the surviving two sentences agree with the
  Part VI page. The record–simulate–snap-back bracket and the whole *when it
  runs* material moved from `player-anatomy` to `the-two-phase-tick`; the
  effects third of `hunger-xp-and-effects` moved whole to `status-effects`,
  and `UseEffects` stayed with the hunger page while `the-spear` links to it.

  **The diagrams.** Seven figures. New: the class ladder
  (`player-anatomy`, a flowchart replacing an ASCII tree), the damage flow
  (`the-sword-swing`), the two-entries-one-exit flowchart (`the-spear`), the
  `FoodData.tick` chain (`hunger-and-experience`), the part-shape flowchart
  (landing page). Redrawn: the two-phase sequence (lanes corrected, and it
  now shows the bracket), the Poison trace (`status-effects`, new). Check the
  `FoodData.tick` flowchart's *at most one of three* claim and the ordering
  inside the two-phase diagram arrow by arrow.

  **The landing page and `lectures.md`** claim that only the sword swing and
  the spear have an internal order, that Part VIII depends on Part VI's
  authority above everything, and that the spear needs `using-an-item`.

- **2026-09-03, pass 3 session J — Part IX Networking.** Four of the five
  pages rewritten (`the-connection` 550→442, `packets-and-stream-codecs`
  448→449, `what-the-client-is-told` 546→461, `chat-and-signing` 365→316);
  `src/systems/networking/README.md` new; `protocol-phases` unchanged except
  three sentences of hand-off links. All five diagrams below are new or
  redrawn.

  **Two of the four pages have no list of introduced claims, and pass 4 must
  treat them as unlisted.** The drafting agents for
  `packets-and-stream-codecs` and `chat-and-signing` both finished writing
  and then died on a rate limit before reporting, so the session accepted
  two finished pages without the claim-by-claim diff the protocol requires.
  The session's own checks passed on them (names, lanes, mermaid, budgets,
  shape) and it spot-checked four load-bearing claims by hand —
  `detectRateSpam`'s operator and singleplayer-host exemptions, the 4,096
  pending-message disconnect threshold, the id-is-a-registration-position
  hook, and the *three ways to say no* branch — but **the other pages'
  guarantee that every reworded sentence was diffed against pass 2's text
  does not hold for these two.** Re-check them whole, at the sentence level,
  against `git show b597a2a~1:src/systems/networking/<page>.md`.
  `chat-and-signing` is the higher risk of the two: it is a security page,
  its central artefact is a new eighteen-row table of *which failure kills
  the message, the chain, or the connection*, and every row is a claim about
  a specific outcome that pass 2 never stated in that form.

  **Claims introduced in `the-connection`, listed by its agent with cites.**
  A handler touching no game state omits `PacketUtils.ensureRunningOnSameThread`
  and runs on Netty (`handlePong` and `handleCustomPayload` are empty bodies
  — the session verified this one). The `PacketProcessor` queue is unbounded
  and each drain empties it (verified). The client's handling latency is a
  frame, not a tick — the borrowed fact restated as this page's consequence.
  The singleplayer host has neither the read timeout nor the keep-alive
  running against it — a *composition* of two old-page facts and therefore
  the one to re-derive. And the diagram's note that there is one encoder and
  one decoder instance at each end.

  **Claims introduced in `what-the-client-is-told`, listed by its agent.**
  That the cascade is three gates and each is a three-term test (a
  conjunction, then two disjunctions) — a synthesis across `ChunkMap` and
  `ServerEntity`, and the assertion the new flowchart rests on, so it is the
  first thing to check. `PlayerChunkSender.START_CHUNKS_PER_TICK` and
  `MAX_UNACKNOWLEDGED_BATCHES` named as the constants behind "nine" and
  "ten". Two `ChunkBatchSizeCalculator` constants attached to the clamp and
  the weighted mean. That the forced absolute sync is rarer than the forced
  position packet by however long the interval gate stays shut — an
  inference from two counters, one inside the gate and one outside. That the
  passenger-list packet is the filtered one, so a mounting player is told
  from their own point of view. And that equipment, passengers and leash
  links appear in the pairing bundle only when non-empty.

  **The diagrams.** New: the round-trip sequence in `the-connection` (six
  lanes, four thread boundaries marked, the reply returning to a second
  drain — the pair's whole reason to exist, and every arrow an ordering
  claim); the gate flowchart in `what-the-client-is-told`; the codec
  composition flowchart in `packets-and-stream-codecs` (which asserts that
  nothing above the `ProtocolInfoBuilder.addPacket` line knows about ids and
  nothing below it knows about chat); the *three ways to say no* flowchart in
  `chat-and-signing`; the part-shape flowchart on the landing page. Trimmed:
  the pairing-bundle sequence, which is all that survives of
  `what-the-client-is-told`'s old trace.

  **Claims deleted rather than rewritten.** `what-the-client-is-told` lost
  its whole client half to Part X (the list is in [pass3.md](pass3.md) for
  session K). Check that nothing true was lost in that deletion and that the
  surviving one-paragraph hand-off agrees with `the-client-level` and
  `prediction-and-acks` once session K has been over them.

  **The landing page and `lectures.md`** claim that the first two lectures
  are one lecture in two halves, that lectures four and five are independent
  of each other and both assume three, that Part IX assumes Part III and
  Part I's two loops, and that Part IX is a prerequisite of Part X. Three
  are orderings, which pass 2 found is where this corpus is most confidently
  wrong.

- **2026-09-03, pass 3 session K — Part X The client.** Twelve pages
  rewritten in shape, one page split into two, one landing page and one
  Reference page written. The whole part is on this list; below is what
  pass 4 should check *hardest*, being what the rewrite introduced.

  **One ordering the rewrite corrected, which is the first thing to
  re-check.** `the-client-loop`'s old sequence diagram put
  `FramerateLimiter.limitDisplayFPS` after the *Post render* section, i.e.
  at the end of `Minecraft.runTick`. It is not there: it is inside
  `Minecraft.renderFrame`, after the present and before *Post render*, and
  it is gated on `GameRenderState`'s framerate limit being below 260 rather
  than on the tracker being asked again at that moment. The new flowchart
  says so. Confirm both halves of that correction.

  **The hooks, one per page, all new or newly load-bearing.** The frame that
  earns fifteen ticks runs ten and loses five (`the-client-loop` — the claim
  was in the old page's invariants, it is now the opening paragraph). The
  client's tick lists accept a schedule and then answer *no* when asked
  whether one is pending, so a predicted repeater looks inert
  (`the-client-level` — the *repeater* is the session's example and is not
  in the decompile as such: check that a repeater actually reschedules
  itself through the black-holed path). The receipt is for a number and is
  sent for refusals (`prediction-and-acks`, unchanged in substance). A
  toggle-sneak press flips the mapping and the *release* is swallowed
  entirely, and a screen closing turns the toggle back on
  (`input-and-keybinds` — new scenario this session, read from
  `ToggleKeyMapping` and `KeyMapping.restoreToggleStatesOnScreenClosed`). A
  cycle button broadcasts your `ClientInformation` on every click
  (`options`, unchanged). Pressing E sends and receives nothing
  (`gui-and-screens`, unchanged). Layering is inferred from bounding boxes
  (`the-gui-render-tree`, unchanged). Measuring bakes (`text-and-fonts`,
  unchanged). F1 does not hide the sleep fade (`hud`, unchanged). A sound
  always starts at least one hop after the packet (`sound-engine`,
  unchanged). Most world sounds are an int (`what-makes-a-sound`,
  unchanged). Nothing is stripped from the shipped jar
  (`debugging-the-running-game`, unchanged).

  **Facts added this session, which had no owner before.**
  `Entity.moveOrInterpolateTo` and the seven overrides of
  `Entity.getInterpolation` — `LivingEntity`, `Display`, `ExperienceOrb`,
  `Shulker`, `FishingHook`, `AbstractBoat`, `AbstractMinecart` — against a
  default that returns null and therefore snaps; the page's *snaps* column
  names `AbstractArrow`, `PrimedTnt`, `ItemEntity` and `FallingBlockEntity`
  as examples of the default, which is an inference from *does not override*
  and should be spot-checked. `ClientPacketListener.serverChunkRadius` and
  `ClientPacketListener.serverSimulationDistance`, seeded at login and handed
  to each new `ClientLevel`. `ClientChunkCache.Storage` as an
  `AtomicReferenceArray` with volatile centre coordinates, and the claim
  that the reason is the render thread reading them — a *why*, and therefore
  weaker than the *what*. `Entity.isInterpolating` being read by
  `ServerboundMoveVehiclePacket` and `PositionMoveRotation`. And
  `DebugSubscriptions.DEDICATED_SERVER_TICK_TIME` named properly, replacing
  the old page's awkward reference to a `RemoteDebugSampleType` constant; the
  count of sixteen was re-derived by counting the fields, and the four
  expiring kinds now carry their tick counts (60, 100, 200, 200).

  **The new Reference page is thirty rows of gate, and every row is a
  claim.** `src/reference/hud-elements.md` was read one method at a time out
  of `Hud.extractRenderState` and `Gui.extractRenderState`. Two rows are
  inferences rather than transcriptions and should be checked first: row 13,
  that mount health sits *outside* the can-hurt-you block and so shows in
  creative; and row 26, the two different paths by which subtitles are
  recorded when the HUD is hidden. Also check the preamble's claim that
  `GuiRenderState.isHudHidden` is published before the loading-screen
  short-circuit.

  **The diagrams.** New and asserting orderings: the one-turn flowchart in
  `the-client-loop` (every edge is an ordering claim, and the clamp is a
  decision node); the two-column `stateDiagram-v2` in `prediction-and-acks`
  (five client transitions and three server ones, and the claim that no
  transition anywhere is "the server said no"); the setting-change flowchart
  in `options`; the containment flowchart in `gui-and-screens`; two
  flowcharts in `the-gui-render-tree`, one of the data and one of the draw
  pass; the six-stage pipeline flowchart in `text-and-fonts`; the record-order
  flowchart in `hud`, which asserts exactly where the sleep fade sits; the
  three-doors flowchart in `what-makes-a-sound`; the hub-and-spokes figure on
  the landing page, whose seven arrow labels are cadence claims. Redrawn:
  the sneak trace in `input-and-keybinds` (a different scenario from the old
  page's, so it is a new diagram not an edited one). Kept and re-checked:
  the chunk-arrival sequence in `the-client-level`, the refusal sequence in
  `prediction-and-acks`, the inventory sequence in `gui-and-screens`, the
  chat-line sequence in `text-and-fonts`, the hearts sequence in `hud`, the
  villager-brain sequence in `debugging-the-running-game`, and the
  block-placed sequence now in `sound-engine`.

  **The split.** `sound.md` became `sound-engine.md` and
  `what-makes-a-sound.md`. Nothing was cut in the split, but material moved
  across the seam and pass 4 should read the two together once: the engine
  page keeps `SoundInstance`, the threads, the channel limits, the volume
  arithmetic, looping and the device, and the content page keeps
  `SoundEvent`, `SoundSource`, `sounds.json`, level events, the local-player
  prediction, propagation delay and the environment-attribute music model.
  The one claim that was *sharpened* rather than moved: a server can name a
  sound in no registry (inline `SoundEvent` in the stream codec) while data
  packs cannot register one — the old page said this in passing and the new
  one makes it a table row.

  **The landing page and `lectures.md`** claim that Part X is a hub and
  spokes rather than a pipeline, that only the GUI stack is internally
  ordered, that Part IX and Part V are both prerequisites, and that
  `the-client-loop` is a prerequisite of Part XI. All four are orderings.

---

## Session M — Part XII World generation *(2026-09-03)*

**Two errors found while rewriting, which is four part-sessions in a row.**
Both are counts, and both had survived pass 2 because nobody had recounted
them against the registration site.

- **`features-and-placement` said sixty-three features are registered into
  `BuiltInRegistries.FEATURE`. It is 61** (`Feature.java`, counting the
  registering assignments). Fixed in place. The page's separate observation
  that being a `Feature` subclass does not imply being registered — the
  dragon fight's podium feature — is unchanged and still true.
- **The same page called `CountOnEveryLayerPlacement` "the fifteenth" of the
  fifteen placement modifier types.** There are fifteen, but it is **ninth**
  in `PlacementModifierType`'s declaration order, so "the fifteenth" reads
  as an ordinal and is wrong. Reworded to "one of the fifteen". Pass 4
  should treat every *ordinal* in the corpus the way it treats counts.

**Claims this session introduced, hardest first.**

- **The overworld noise cell is four blocks wide, four deep and eight tall,
  and a chunk holds 768 of them** (`terrain`, stated as *the number*).
  Derived from `NoiseSettings.OVERWORLD_NOISE_SETTINGS` (horizontal size 1,
  vertical size 2) through `NoiseSettings.getCellWidth` and
  `NoiseSettings.getCellHeight`, which multiply by four via
  `QuartPos.toBlock`, and from `NoiseBasedChunkGenerator.fillFromNoise`'s
  cell counts (16 / 4 = 4 each way, 384 / 8 = 48 up). No page said any of
  this before.
- **1,225 corner samples per interpolated density term, per chunk**
  (`terrain`, the second *number*). Five slices, five Z, forty-nine Y: read
  off `NoiseChunk.fillSlice` (which loops the horizontal cell count plus
  one) and the slice-filling context provider (which loops the vertical cell
  count plus one), plus the five slices that
  `NoiseChunk.initializeForFirstCellX` and four `NoiseChunk.advanceCellX`
  calls fill. Check the slice count first: it is the one step in the
  arithmetic that is an inference from loop structure rather than a literal.
- **The six-deep nesting figure in `terrain`** asserts the exact loop order
  of the noise fill: cell X, cell Z, cell Y *descending*, block Y
  *descending*, block X, block Z — and that `NoiseChunk.advanceCellX` fills
  the next slice while `NoiseChunk.swapSlices` drops the old one at the end
  of each X column. Every level of that nesting is an ordering claim.
- **The three-forms figure in `density-functions`** asserts what survives
  each rewrite: that `RandomState`'s wiring visitor fills noise holders and
  rebuilds `BlendedNoise` and the end-islands node while leaving
  `DensityFunctions.Marker` and `DensityFunctions.HolderHolder` **intact**,
  and that only `NoiseChunk.wrapNew` resolves those two. It also asserts
  that the parsed form is sampled by nothing at all — the F3 readout samples
  `RandomState.router`, the *once*-rewritten form, which corrects the old
  page's framing rather than its facts.
- **`DensityFunctions.FindTopSurface` is a node type the corpus had never
  named**, and it is the thirty-fourth and last registration. The claims to
  check: that there are exactly **34** registered types (four by name, six
  markers, nine by name, seven mapped, four arithmetic, four last), and that
  its declared bounds are **Y coordinates rather than densities**, which
  makes it the one node whose range is on a different scale from the rest of
  the catalogue.
- **`DensityFunctions.shift` — the three-dimensional domain warp — has no
  callers and appears in no shipped file** (`density-functions`, and the
  Reference page's closing section). Also: *constant*, *cache_all_in_cell*
  and *beardifier* are never written as typed objects in vanilla data, the
  last two being added in code by `NoiseChunk`'s constructor.
- **`DensityFunction.NoiseHolder` reports a maximum of 2.0 while its noise
  is null**, so the parsed graph reports wider noise bounds than the seeded
  graph it becomes. New, and the kind of claim one test would settle.
- **`DensityFunctions.Spline` has a hand-written equality that ignores its
  derived sampler**, offered as the *mechanism* behind the old page's "the
  rewrite memo is structural, not by reference". The old claim was about
  records generally; this names the one node that is not a record and still
  merges.
- **`NoiseChunk.BlendOffset` reports infinite bounds where the data-side
  `DensityFunctions.BlendOffset` reports zero** — in the Reference page
  only, and never checked by pass 2.

**`trees` is a new page and every claim in it is new.** It was written from a
source inventory of `TreeFeature`, `TreeConfiguration`, the four placer
packages, the feature-size package, `TreeFeatures` and `TreeGrower`, and
five of its claims were re-read against the decompile by hand before
publishing. Those five: that `TreeFeature.doPlace` derives the foliage
height and the leaf radius from the **unclipped** proposed height and passes
the *clipped* height to both placers, so a clipped tree keeps a full-size
crown; that the clearance scan returns *two below* the first blocked layer;
that `FancyTrunkPlacer`'s crown-candidates-per-level count is pinned at one
by a minimum against one over an expression that is never below one, making
the named density constant inert; that `CherryFoliagePlacer`'s codec gives
the *corner hole chance* field a getter returning the **wide bottom layer**
field, so any encode writes one value into both; and that
`TreeGrower.DARK_OAK` declares only a mega tree, which is why a lone
dark-oak sapling never grows, with `TreeGrower.PALE_OAK` doing the same and
pointing at the decorator-free bone-meal variant.

The rest of that page is inventory-sourced and wants checking row by row:
the nine trunk placers, the eleven foliage placers, the ten decorators, the
five-species table with its numeric configurations, the mangrove root
recursion that "succeeds by failing" (and the muddy-roots branch that skips
its moss carpet), and the bucketed leaf-distance walk whose pre-marked
decoration and root sets *block* propagation. Counts to re-derive: 9 trunk
placers, 11 foliage placers, 1 root placer, 2 feature sizes, 10 decorators —
and the claim that `MegaJungleFoliagePlacer` is registered under a *jungle*
id rather than a *mega jungle* one.

**The split, and where material crossed the seam.** `structures.md` became
`structure-placement.md` (redirected) and `jigsaw-and-templates.md`. Read the
two together once: placement keeps the lottery,
`ChunkGeneratorStructureState`, `Structure`, `StructureStart`, the reference
scan, `StructureCheck`, both `StructureManager`s, `Beardifier`,
`TerrainAdjustment`, the locate command and the per-chunk write; jigsaw keeps
the pools, the assembly loop, the template system and the whole processor
stack — which `hand-built-structures` now reaches by link rather than owning
a share of. Three framework facts moved from the old page's invariant wall
onto `structure-placement` and should be re-read in their new context: that
the reference position comes from **piece zero**, that
`Structure.adjustBoundingBox` inflates the box by twelve, and that
`StructurePiece.postProcess` runs once per overlapping chunk and must be
idempotent. Two facts moved *off* `terrain` because
`features-and-placement` already owned them better — the minus-one default
write radius and `WorldGenRegion.getChunk` throwing — and pass 4 should
confirm they are not now stated nowhere.

**Diagrams, all of them new or redrawn.** The status-ladder figure on the
landing page, whose whole point is that the lecture order runs *against* the
execution order — every subgraph placement is a claim about which status owns
which page. The four-status hand-off flowchart and the six-deep nesting
figure in `terrain`. The three-forms figure in `density-functions`. The
four-decision flowchart in `structure-placement`, which asserts that
`ChunkStatus.STRUCTURE_STARTS` is the second status and two before
`ChunkStatus.BIOMES`. The modifier-fold flowchart in
`features-and-placement`, whose eight stages are an ordering claim about a
*vanilla* chain rather than a required one. The five-lane sequence in
`trees`. Redrawn on the same subject: the biome trace (six lanes now, the
two read paths moved out of the diagram into a comparison table) and the
village and stronghold traces (relabelled, and the village one now stops at
the pieces rather than running on into the blocks). Nothing in the part
survives unredrawn.

**The landing page and `lectures.md`** claim: that the part is a substrate, a
pipeline and a wing; that the structure wing is decided at
`ChunkStatus.STRUCTURE_STARTS` and written at `ChunkStatus.FEATURES`; that
biomes and terrain are independent statuses and can be watched in either
order; that jigsaw and hand-built are alternatives rather than a sequence;
that Part IV's chunk-generation pipeline is a hard prerequisite; and that
`world/level/levelgen` plus `world/level/biome` come to **423 classes and
45,600 lines** (counted this session, one class per file, package markers
excluded; pass 2 said 429 and 46,628 for a boundary it never stated).

## Session N — Part XIII Commands and data packs *(2026-09-03)*

Nine pages where there were five, and **every one of them was rewritten**.
Two splits (`execution-and-functions` → `the-execution-engine` +
`functions-and-macros`; `dialogs-and-tests` → `dialogs` + `game-tests`), one
page written from nothing (`permissions`, the R7 spend), one landing page,
and four whole-page reshapes. Nothing in the part survives unredrawn either:
every diagram in Part XIII is new or redrawn.

**Check first and hardest: the counts this session re-derived, because they
disagree with pass 2 in three places and the disagreements are the kind pass
2's lesson predicts.**

- `permissions` says **95** `Commands.hasPermission` call sites, of which 94
  are server-side command registrations and the ninety-fifth is
  `ClientPacketListener`'s node builder. Pass 2 said "all ninety-four
  *requires* calls in the game use it", which was a true statement about the
  server and a false one about the total: `.requires(` appears 245 times in
  `net/minecraft`, and the other 150 are `ShapelessRecipeBuilder.requires`,
  an unrelated method. The re-derivation to run is
  `.requires(Commands.hasPermission(` against every `Commands.hasPermission(`.
- The per-level gate counts are stated as **66 gamemaster, 16 admin, 9
  owner**, counted as `requires(Commands.hasPermission(Commands.LEVEL_X))`.
  Raw occurrences of `Commands.LEVEL_GAMEMASTERS` are **68**, and the two
  extra are the ternaries in `SeedCommand` and `VersionCommand`. Pass 2's 66
  was right; the arithmetic that reconciles 95 = 66 + 16 + 9 + 2 (the
  `LEVEL_ALL` ternaries) + 2 (the two non-constant checks) is new and should
  be re-run as a whole.
- The **two non-constant permission checks** are new material:
  `ClientPacketListener.RESTRICTED_COMMAND_CHECK` and
  `GameModeCommand.PERMISSION_CHECK`. The second carries a page-level claim —
  that it is read by `KeyboardHandler`, `GameModeSwitcherScreen` and
  `ServerGamePacketListenerImpl`, i.e. that the F3+F4 switcher greys out by
  running a *server* permission check locally against `LocalPlayer`'s own
  set. Five call sites; count them.
- `advancements` now says the client half is **five classes in
  `client/gui/screens/advancements` plus `ClientAdvancements` in
  `client/multiplayer`, about 1,240 lines**. Pass 2 said "six classes and
  about eleven hundred lines (`net/minecraft/client/gui/screens/advancements`)",
  which counted `package-info.java` as a class and put `ClientAdvancements`
  in the wrong package. The screens package is 1,112 lines over five classes;
  `ClientAdvancements` is 128.
- The landing page says the part is **442 classes and 43,800 lines** over
  nine packages (`commands`, `server/commands`, `server/permissions`,
  `advancements`, `world/scores`, `server/dialog`, `gametest`, and the two
  client screen packages), counted one class per file with package markers
  excluded, the way session M counted Part XII. Nothing in pass 2 states a
  boundary for this part, so this is a new claim end to end.
- `permissions` says `net/minecraft/server/permissions` is **eleven classes
  and 398 lines**; the old page said "twelve files", which included
  `package-info.java`.

**New claims the rewrite introduced, from re-reading the source.** All of
these are this session's, not pass 2's, and none has been checked by anyone
else:

- `PermissionSet` is a **functional interface** with one method, so every set
  in the game except `ChatAbilities`' is a lambda or a tiny object, and there
  is no set-of-permissions data structure anywhere else.
- `LevelBasedPermissionSet.union` of two level-based sets returns **the
  higher of the two** rather than a `PermissionSetUnion`. This is the
  mechanism `functions-and-macros` then leans on for its "the method whose
  name reads like a ceiling can only add" paragraph.
- `PermissionLevel.byId` uses `ByIdMap.OutOfBoundsStrategy.CLAMP`, so an
  *ops.json* hand-edited to level 9 is an owner and −1 is rung zero.
- `Permission.CODEC` accepts an atom written as a **bare identifier** as well
  as the full dispatched form.
- `MinecraftServer.getProfilePermissions` returns a `LevelBasedPermissionSet`
  in every branch, and `ServerPlayer.permissions` calls it afresh every time
  — nothing is cached on the player. The cascade as restated: not on the op
  list → `ALL`; on it → the op entry's own set, else singleplayer owner →
  `OWNER`, else singleplayer → `OWNER` or `ALL` by the allow-cheats-for-others
  toggle, else the *op-permission-level* property.
- `PermissionSetUnion` holds a **reference** set (`ReferenceArraySet`), so
  identity, not equality, decides whether unioning the same set twice
  duplicates it.
- `ChatAbilities` is built **by subtraction**: it starts from all four of
  `Permissions.CHAT_PERMISSIONS` and each `ChatRestriction` removes some.
  There are four restrictions and **all four are local decisions** (two chat
  options, the launcher, the account profile) — no server grants a client
  chat permission. This is a structural claim about the whole enum; check
  that no fifth value and no server-driven route exists.
- `ClientPacketListener`'s ordinary suggestions provider has the player's own
  set **OR-ed with** the synthetic restricted atom, and
  `restrictedSuggestionsProvider` is the `NO_PERMISSIONS` one — the field
  name reads backwards from what it holds.
- `ClientPacketListener.verifyCommand` has **four** outcomes
  (`NO_ISSUES`, `PARSE_ERRORS`, `SIGNATURE_REQUIRED`, `PERMISSIONS_REQUIRED`)
  and the flowchart on `permissions` asserts their order: parse with
  permissions, then signable-argument test, then parse *without* permissions.
  Every branch of that figure is an ordering claim.
- `functions-and-macros` says `ServerFunctionManager.execute` swallows only
  `FunctionInstantiationException` with an empty catch, and logs **any other
  exception at warn**. Pass 2 recorded the empty catch and not the warn arm.
- `ServerFunctionManager.getGameLoopSender` uses
  `CommandSourceStack.withPermission` (a **replacement**) with gamemaster over
  a server source that is `LevelBasedPermissionSet.OWNER`, while
  `FunctionCommand` and `DebugCommand` use
  `CommandSourceStack.withMaximumPermission` (a **union**). The page claims
  the tick and load tags therefore run *lower* than the console does; check
  both directions.
- `game-tests` says `/test` sits at `Commands.LEVEL_GAMEMASTERS` and
  `TestCommand.TEST_FULL_SEARCH_RADIUS` is 250, with the radius subcommand
  clamping a user-supplied radius to 0–1024.
- `the-execution-engine` restates `ContinuationTask.schedule`'s arithmetic
  with the **two-element case made explicit** (nothing / one entry / *two
  entries* / one self-entry), which the old page elided.
- `scoreboard-and-data` adds that `ScoreContents` and `NbtContents` resolve
  on the server and put the *result* on the wire — restated from pass 2's
  invariant, now framed as a third route by which a score reaches a client.

**Redrawn and new diagrams, each an ordering claim.**

- `README.md`'s three-floor figure: that the dependency is strictly
  one-directional and that the four top-floor pages are peers.
- `brigadier-and-commands`'s six-lane trace, with the Netty-thread note moved
  onto the diagram as a `Note over`.
- `permissions`' containment figure (question / answer / check) and its
  four-outcome `verifyCommand` cascade — both new.
- `the-execution-engine`'s **queue-snapshot figure**, which is the most
  load-bearing new diagram in the part: four panels claiming that
  `BuildContexts` walks *all* non-execute stages inside entry one, that the
  fan-out becomes a single `ContinuationTask`, and that element *i+1* is not
  materialised until element *i* has finished. Check panel by panel.
- `functions-and-macros`' four-stage pipeline flowchart, including the claim
  that the TRIGGER arrow lands on *instantiate* rather than on *compile*.
- `advancements`' trace, relaned and with a tick-boundary note added.
- `dialogs`' trace (unchanged in substance, relaned) and `game-tests`' two
  figures — a new containment flowchart (declaration / run / world) and the
  old runner sequence, relaned.
- `scoreboard-and-data`'s trace, relaned, with `EntityDataAccessor` folded
  into `DataCommands`.

**The landing page and `lectures.md`** claim: that Part XIII is a stack of
three floors; that nothing in advancements, scoreboards, dialogs or game
tests is needed to understand the parser or the engine, and that all four
need both; that the four top-floor lectures are watchable in any order; and
that the part's stated prerequisites are Part III's server tick (for two
distinct reasons), Part II's codecs and data-driven type pattern, Part IX's
connection, and Part VII's contexts and predicates for advancements alone.

**Material that moved, and must not now be stated nowhere or twice.** The
permission model left `brigadier-and-commands` entirely; that page keeps the
tree's *serialisation* (templates, the unknown-argument-type stub, the one
call site) and `permissions` took the *meaning* of the filtering (absent
versus flagged, the null-source inspector, the client's two sources). Read
the two together once. The `/schedule` gate, the two function tags and the
compile-time permission set left the engine page for
`functions-and-macros`. `dialogs-and-tests`' "the pattern, stated once"
section was **deleted, not moved** — Part II's
`foundations/data-driven-types.md` owns that argument and both new pages
link to it; confirm nothing true was lost with it.
