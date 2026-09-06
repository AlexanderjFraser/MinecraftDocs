# Level data and rules

> Verified against **Minecraft 26.2** · Reference · Who owns the seed, the spawn, the rules, the border and the dimensions, where each is saved, and what tells the client — looked up, not watched.

The facts about a world that are not blocks or entities: its seed and
dimensions, its spawn, its game time, its difficulty, its rules, its
border, its scoreboard and maps. In 26.2 about half of them have left
*level.dat* — `PrimaryLevelData` is a stub and everything else is
a `SavedData` file under a *data/* folder, one server-global and one per
dimension — so the question this page answers is always the same one:
*which file remembers this, and who is allowed to change it.* The table
under [who owns what](#who-owns-what) is the page; the sections after it are
the prose behind the rows that need it, and the rest are one line each because
one line is all there is.

Four parts point here — [III](../systems/server/README.md) for what a boot
reads, [IV](../systems/world/README.md) for what the world is made of,
[VIII](../systems/player/README.md) for the two game rules that decide
whether the server checks your movement, and
[XII](../systems/worldgen/README.md) for the seed — and [the level
tick](../systems/server/server-level-tick.md) is where most of them are read.

## Who owns what

| datum | owner | saved as | told to the client by |
|---|---|---|---|
| seed, structures, bonus chest, dimension list | `WorldGenSettings` (`MinecraftServer.getWorldGenSettings`) | *data/minecraft/world_gen_settings.dat* | the obfuscated seed in `CommonPlayerSpawnInfo`, the dimension list in `ClientboundLoginPacket`; structures and the bonus chest, nothing |
| world spawn | `PrimaryLevelData.respawnData` | *level.dat* | `ClientboundSetDefaultSpawnPositionPacket` |
| game time | `PrimaryLevelData.gameTime` (shared by every level) | *level.dat* | `ClientboundSetTimePacket` |
| day time | `ServerClockManager` | *data/minecraft/world_clocks.dat* | `ClientboundSetTimePacket` |
| difficulty, lock, hardcore | `LevelSettings.DifficultySettings` | *level.dat* | `ClientboundChangeDifficultyPacket` — hardcore alone rides in `ClientboundLoginPacket` |
| game type, allow-commands, name, data packs | `LevelSettings` | *level.dat* | the game type only as a new player's default, through `CommonPlayerSpawnInfo`; the enabled features at the configuration phase; the name and allow-commands, nothing |
| game rules | `GameRuleMap` via `GameRules` | *data/minecraft/game_rules.dat* | five rules only, plus `ClientboundGameRuleValuesPacket` on request |
| weather | `WeatherData` | *data/minecraft/weather.dat* | `ClientboundGameEventPacket` |
| world border | `WorldBorder`, one per `ServerLevel` | *dimensions/minecraft/…/data/minecraft/world_border.dat* | `ClientboundInitializeBorderPacket` and the five `ClientboundSetBorder…` packets |
| scoreboard | `ServerScoreboard` (`MinecraftServer.scoreboard`), buffered by `ScoreboardSaveData` at save time | *data/minecraft/scoreboard.dat* | `ClientboundSetObjectivePacket`, `ClientboundSetScorePacket`, `ClientboundSetPlayerTeamPacket` |
| maps | `MapItemSavedData` per `MapId`, `MapIndex` for the counter | *data/minecraft/maps/\<n\>.dat*, *data/minecraft/maps/last_id.dat* | `ClientboundMapItemDataPacket` |
| raids | `Raids` per level | *dimensions/minecraft/…/data/minecraft/raids.dat* | boss bars |
| chunk tickets | `TicketStorage` per level ([tickets](../systems/world/tickets-and-loading.md)) | *dimensions/minecraft/…/data/minecraft/chunk_tickets.dat* | — |
| dragon fight | `EnderDragonFight`, where `DimensionType.hasEnderDragonFight` | *dimensions/minecraft/…/data/minecraft/ender_dragon_fight.dat* | boss bars |
| boss bars, scheduled functions, random sequences, stopwatches, trader timers, command storage | `CustomBossEvents`, `TimerQueue`, `RandomSequences`, `Stopwatches`, `WanderingTraderData`, `CommandStorage` | *data/minecraft/\<id\>.dat*, and one *data/\<namespace\>/command_storage.dat* per namespace | boss bars only |
| player data | `PlayerDataStorage` | *players/data/\<uuid\>.dat* | — |

## What is left in *level.dat*

`LevelData` is the read-only interface every `Level` exposes, and it is
small: `LevelData.getRespawnData`, `LevelData.getGameTime`,
`LevelData.isHardcore`, `LevelData.getDifficulty` and
`LevelData.isDifficultyLocked`. No day time — that has left level data
entirely for `ServerClockManager` ([who owns the
clock](../systems/world/environment-attributes-and-timelines.md#who-owns-the-clock)) —
no weather, no rules, no border. `LevelData.RespawnData` is the world
spawn as a `GlobalPos` with yaw *and* pitch — it carries a dimension, so
`/setworldspawn` can point anywhere. `WritableLevelData` adds
`WritableLevelData.setSpawn`; `ServerLevelData` adds eight more — the level
name, the game type and its setter, `ServerLevelData.isInitialized` and its
setter, `ServerLevelData.isAllowCommands` and its setter, and
`ServerLevelData.setGameTime`; `WorldData` is the server-wide view
(`WorldData.getLevelSettings`, `WorldData.getDataConfiguration`,
`WorldData.enabledFeatures`, `WorldData.wasModded`,
`WorldData.getKnownServerBrands`, `WorldData.overworldData`).

`PrimaryLevelData` implements all of them — the overworld's level data and
the whole server's — with about ten fields: `PrimaryLevelData.settings` (a
`LevelSettings`: name, `GameType`, a `LevelSettings.DifficultySettings` of
difficulty, hardcore and lock, allow-commands, `WorldDataConfiguration`),
`PrimaryLevelData.respawnData`, `PrimaryLevelData.gameTime`,
`PrimaryLevelData.initialized`, `PrimaryLevelData.knownServerBrands`,
`PrimaryLevelData.wasModded`, `PrimaryLevelData.removedFeatureFlags`,
`PrimaryLevelData.singlePlayerUUID`, `PrimaryLevelData.version`, and
`PrimaryLevelData.specialWorldProperty` (`PrimaryLevelData.SpecialWorldProperty.FLAT`
/ `PrimaryLevelData.SpecialWorldProperty.DEBUG` / none). That is the whole
stub: seed, dimensions, rules, border, weather, dragon fight, boss bars,
scheduled events and trader timers are all `SavedData` files.
`PrimaryLevelData.createTag` builds the payload — flat, no wrapper — and
it is `LevelStorageSource.LevelStorageAccess.saveDataTag` that nests it
under *Data*; `PrimaryLevelData.parse` reads it back.

`DerivedLevelData` is what every other `ServerLevel` gets, built in
`MinecraftServer.createLevels`: spawn, game time and initialised state
forwarded to the overworld's data, and everything the whole server shares —
name, game type, hardcore, allow-commands, difficulty and its lock — read
straight off the `WorldData`. Only `DerivedLevelData.setSpawn` writes
anything; `DerivedLevelData.setGameTime`, `DerivedLevelData.setGameType`,
`DerivedLevelData.setAllowCommands` and `DerivedLevelData.setInitialized` are
no-ops. That forwarding is how game
time comes to be shared by every level.

The file is written by `LevelStorageSource.LevelStorageAccess.saveDataTag`
→ `LevelStorageSource.LevelStorageAccess.saveLevelData`: a temp file, then
`Util.safeReplaceFile` renames the old *level.dat* to `level.dat_old` and
the temp into place, ten retries per step with a rollback. `LevelSummary`
(the world-select row) is read from it by
`LevelStorageSource.readLevelSummary`. `LevelResource` names the paths:
`LevelResource.LEVEL_DATA_FILE`, `LevelResource.DATA`,
`LevelResource.PLAYER_DATA_DIR` (*players/data/*, a new sub-folder),
`LevelResource.LOCK_FILE`.

### The spawn every level reports is the server's, not each level's

`ServerLevel.getRespawnData` forwards to `MinecraftServer.getRespawnData`,
which returns `MinecraftServer.effectiveRespawnData` — recomputed by
`MinecraftServer.updateEffectiveRespawnData` through
`Level.getWorldBorderAdjustedRespawnData`, which **relocates a spawn that
has fallen outside the border** to the border centre's surface, and by
`MinecraftServer.findRespawnDimension`, which falls back to the overworld
when the stored dimension no longer exists. So every level reports the same
spawn, and it need not be the one *level.dat* holds: it is the stored one
wherever that is still inside the border and its dimension still exists, and a
recomputed one where it is not.

## Two saved-data storages, neither of them the overworld's

`SavedData` is one flag, `SavedData.dirty` (`SavedData.setDirty`); a
`SavedDataType` is an id, a constructor, a `Codec` and a `DataFixTypes`.
`SavedDataStorage` caches them per folder
(`SavedDataStorage.computeIfAbsent`, `SavedDataStorage.get`,
`SavedDataStorage.set`) and writes `<id>.dat` as *{ data, DataVersion }*,
gzip-compressed. How a dirty entry reaches the disk — encoded on the caller's
thread, written on the IO pool, and joined at shutdown — is the same
copy-then-encode-then-write shape a chunk takes, and it is [chunk
storage](../systems/world/chunk-storage.md#the-other-store-under-data)'s.

The id is an `Identifier`, so every saved-data file lives under a namespace
folder — the path is *data/\<namespace\>/\<path\>.dat* — and vanilla's are
all under *data/minecraft/*. Command storage is the one place the namespace
is not *minecraft*: each gets its own *data/\<namespace\>/command_storage.dat*.

There are two storages. `MinecraftServer.savedDataStorage`
(`MinecraftServer.getDataStorage`) is server-global at *\<world\>/data/*;
maps, scoreboard, rules, weather and clocks are server-wide.
`ServerChunkCache.savedDataStorage` (`ServerChunkCache.getDataStorage`,
forwarded by `ServerLevel.getDataStorage`) is per dimension at
*dimensions/\<namespace\>/\<path\>/data/* — the overworld included
([chunk storage](../systems/world/chunk-storage.md)); raids, tickets, the
border and the dragon fight are per dimension, the overworld's under
*dimensions/* like everyone else's. Neither is "the overworld's".

## Game rules are a registry

`GameRule` is a registry entry in `Registries.GAME_RULE` /
`BuiltInRegistries.GAME_RULE`, bootstrapped by `GameRules.bootstrap`:
`GameRule.category` (a `GameRuleCategory` — `GameRuleCategory.PLAYER`,
`GameRuleCategory.MOBS`, `GameRuleCategory.SPAWNING`, `GameRuleCategory.DROPS`,
`GameRuleCategory.UPDATES`, `GameRuleCategory.CHAT`, `GameRuleCategory.MISC`),
`GameRule.gameRuleType` (`GameRuleType.INT` or `GameRuleType.BOOL`),
`GameRule.argument` (a Brigadier type), `GameRule.valueCodec`,
`GameRule.defaultValue` and `GameRule.requiredFeatures`. Ids are
snake_case and namespaceable — `GameRules.ADVANCE_TIME`, `GameRules.SPAWN_MOBS`,
`GameRules.SPAWN_MONSTERS`, `GameRules.KEEP_INVENTORY`,
`GameRules.RANDOM_TICK_SPEED`, `GameRules.PLAYERS_SLEEPING_PERCENTAGE`,
`GameRules.RESPAWN_RADIUS`, `GameRules.MAX_ENTITY_CRAMMING`,
`GameRules.MAX_SNOW_ACCUMULATION_HEIGHT`,
`GameRules.MAX_MINECART_SPEED` (feature-gated) … fifty-nine of them, with
their defaults, in [the generated table](gamerules.md); the old names and the
nested value classes have rows in [naming drift](naming-drift.md).

The values are saved data, not level data: a `GameRuleMap` — `SavedData`,
*game_rules.dat*, server-global — wrapped by the `GameRules` instance in
`MinecraftServer.gameRules`. `ServerLevel.getGameRules` returns the
server's: **one set for every dimension**, and `Level` has no rules
accessor at all, so no `ClientLevel` can read a rule — the client's only
`GameRules` objects belong to the two rules screens, and neither drives
gameplay. The accessors are
`GameRules.get`, `GameRules.set` (which calls
`MinecraftServer.onGameRuleChanged`) and `GameRules.visitGameRuleTypes`
(how `GameRuleCommand.register` builds **two** literals per rule — the
bare id and the namespaced one).

### What the client hears

Five rules, and everything else is server-only. All three of
`GameRules.REDUCED_DEBUG_INFO`, `GameRules.LIMITED_CRAFTING` and
`GameRules.IMMEDIATE_RESPAWN` ride in `ClientboundLoginPacket` at join (the
last inverted, as *showDeathScreen*); a change afterwards goes as a
`ClientboundEntityEventPacket` for the first and a `ClientboundGameEventPacket`
for the other two (`ClientboundGameEventPacket.LIMITED_CRAFTING`,
`ClientboundGameEventPacket.IMMEDIATE_RESPAWN`); `GameRules.LOCATOR_BAR` through
`ServerWaypointManager`; and `GameRules.ADVANCE_TIME`, which broadcasts a
full clock sync because a paused clock is expressed on the wire as rate 0
([environment attributes](../systems/world/environment-attributes-and-timelines.md)).
`MinecraftServer.updateMobSpawningFlags` sends nothing; it only calls
`Level.setSpawnSettings`, which forwards to `ServerChunkCache.setSpawnSettings`.

New is an in-game editor: `ServerboundClientCommandPacket.Action.REQUEST_GAMERULE_VALUES`
→ `ServerGamePacketListenerImpl.sendGameRuleValues` →
`ClientboundGameRuleValuesPacket` → `InWorldGameRulesScreen`, and edits
back as `ServerboundSetGameRulePacket` → `ServerGamePacketListenerImpl.handleSetGameRule`
(gated on `Permissions.COMMANDS_GAMEMASTER`).

## The border is per dimension

*The border has no lecture.* It is the one mechanism in Part IV's packages
whose home is this page rather than a page of the part: it sits on no
conveyor, it belongs to none of the four side-systems, and what a reader needs
of it is a set of numbers, a pair of extents and a list of packets — which is
what a Reference page is for. Part IV's landing page declares it as such.

`WorldBorder` is `SavedData` — *world_border.dat*, **per dimension**,
fetched by `ServerLevel.getWorldBorder` through the cache on every call.
Nothing scales the Nether's border by `DimensionType.coordinateScale` —
each dimension's file has its own values, so the Nether has the same
numbers unless someone sets them.

`WorldBorder.settings` (`WorldBorder.Settings`: centre, damage per block,
safe zone, warning blocks and time, size, lerp time and target;
`WorldBorder.Settings.DEFAULT` is 0,0 / 0.2 / 5 / 5 / 300 / `WorldBorder.MAX_SIZE`)
is the *loaded* snapshot, never written again;
`WorldBorder.applyInitialSettings` pushes it into the live fields once,
restarting a lerp in progress, and saving reads the live fields back out.
The live defaults are not the persisted ones — a fresh `WorldBorder`
starts with a warning time of 15, not 300.

The live extent is a `WorldBorder.BorderExtent` — `WorldBorder.StaticBorderExtent`
or `WorldBorder.MovingBorderExtent`, which `WorldBorder.tick` advances
([the level tick](../systems/server/server-level-tick.md)). A moving border
re-saves itself every tick: `WorldBorder.MovingBorderExtent` marks the
saved data dirty on every advance, and a stationary one never does.
`WorldBorder.MAX_SIZE` is 59,999,968; `MinecraftServer.getAbsoluteMaxWorldSize`
is applied to every level's border in `MinecraftServer.createLevels` —
29,999,984 on the integrated server, but `DedicatedServer` overrides it
with *max-world-size*. `WorldBorder.isWithinBounds`, `WorldBorder.clampToBounds`,
`WorldBorder.getDistanceToBorder`, `WorldBorder.getCollisionShape` are
the readers; `BorderStatus` colours the client's wall.

For sync, `PlayerList.addWorldborderListener` registers a `BorderChangeListener`
per level that broadcasts, dimension-scoped, `ClientboundSetBorderSizePacket`,
`ClientboundSetBorderLerpSizePacket`, `ClientboundSetBorderCenterPacket`,
`ClientboundSetBorderWarningDelayPacket` and `ClientboundSetBorderWarningDistancePacket`;
`PlayerList.sendLevelInfo` sends `ClientboundInitializeBorderPacket` on
join and dimension change. `ClientLevel.worldBorder` is a plain
`WorldBorder` ticked in `ClientLevel.tick`.

## Dimensions and the seed

`DimensionType` is a record: `DimensionType.hasSkyLight`,
`DimensionType.hasCeiling`, `DimensionType.hasFixedTime`,
`DimensionType.hasEnderDragonFight` (the dragon fight is a dimension flag
now, not hard-wired to `Level.END`), `DimensionType.coordinateScale`,
`DimensionType.minY`, `DimensionType.height`, `DimensionType.logicalHeight`,
`DimensionType.infiniburn`, `DimensionType.ambientLight`,
`DimensionType.monsterSettings`, `DimensionType.skybox` (`DimensionType.Skybox`),
`DimensionType.cardinalLightType`, `DimensionType.attributes` (an
`EnvironmentAttributeMap`), `DimensionType.timelines` and
`DimensionType.defaultClock` (a
`WorldClock` holder; `WorldClocks.OVERWORLD`, `WorldClocks.THE_END`). The
gameplay booleans a 1.21-era reader will look for here went to the first of
those three ([the stack a value falls
through](../systems/world/environment-attributes-and-timelines.md#the-stack-a-value-falls-through)),
and [naming drift](naming-drift.md) has the row for each.
`DimensionType.getStorageFolder` names the on-disk folder.
Defaults are `DimensionDefaults` (`DimensionDefaults.OVERWORLD_MIN_Y` −64,
`DimensionDefaults.OVERWORLD_LEVEL_HEIGHT` 384,
`DimensionDefaults.NETHER_LOGICAL_HEIGHT` 128); the built-in keys are
`BuiltinDimensionTypes.OVERWORLD`, `BuiltinDimensionTypes.NETHER`,
`BuiltinDimensionTypes.END`, `BuiltinDimensionTypes.OVERWORLD_CAVES`.

`LevelStem` is a `DimensionType` holder plus a `ChunkGenerator`
(`LevelStem.OVERWORLD`, `LevelStem.NETHER`, `LevelStem.END`).
`Registries.LEVEL_STEM` and `Registries.DIMENSION` share the id
*dimension* ([identifiers and registries](../systems/foundations/identifiers-and-registries.md));
`Level.OVERWORLD`, `Level.NETHER`, `Level.END` are `ResourceKey`s under
the latter, and `Level.dimension` / `Level.dimensionType` are the
accessors. `Level.canHaveWeather` is sky light, no ceiling, not the End.

The seed and the dimension list are `WorldGenSettings` — `SavedData`,
*world_gen_settings.dat*, server-global, and written not at world creation but
by the `MinecraftServer` constructor, which pushes it into the storage on every
boot ([creating a world](../systems/worldgen/creating-a-world.md) is where it
comes from) — holding
`WorldOptions`
(`WorldOptions.seed`, `WorldOptions.generateStructures`,
`WorldOptions.generateBonusChest`) and `WorldDimensions` (the stem map;
`WorldDimensions.bake` produces the registry). It is read before the
server exists by `LevelStorageSource.getLevelDataAndDimensions` and
pushed in with `SavedDataStorage.set`; if the file is missing or
unreadable the loader logs an error and substitutes a whole default
`WorldGenSettings` — a random seed, structures on, no bonus chest, and the
data packs' dimension list in place of the saved one — then carries on loading
the world. `MinecraftServer.createLevels` makes one
`ServerLevel` per stem; `MinecraftServer.levelKeys` go out in
`ClientboundLoginPacket`, the dimension type via registry sync, and the
biome-zoom-obfuscated seed in `CommonPlayerSpawnInfo`.

## Difficulty and weather

`Difficulty` (`Difficulty.PEACEFUL` … `Difficulty.HARD`) sits in
`LevelSettings.DifficultySettings`. `MinecraftServer.setDifficulty` writes
it, `MinecraftServer.updateMobSpawningFlags`, and
`MinecraftServer.sendDifficultyUpdate` → `ClientboundChangeDifficultyPacket`.
`DedicatedServer.forceDifficulty` applies *server.properties* at boot
with the lock ignored; there is no *getForcedDifficulty*.
`DifficultyInstance` — local difficulty — is built by
`ServerLevel.getCurrentDifficultyAt` from `ChunkAccess.getInhabitedTime`,
`Level.getOverworldClockTime` and the moon phase (an environment
attribute, `EnvironmentAttributes.MOON_PHASE`, indexed into
`DimensionType.MOON_BRIGHTNESS_PER_PHASE` — the one piece of the old moon
logic still on `DimensionType`; see
[environment attributes](../systems/world/environment-attributes-and-timelines.md)).

`WeatherData` — server-global `SavedData`, `MinecraftServer.getWeatherData`
— was covered in [the level tick](../systems/server/server-level-tick.md).
`PrimaryLevelData` stores no rain fields.

## Where to look

`PrimaryLevelData.setTagData` · `DerivedLevelData` · `LevelSettings` ·
`LevelStorageSource.getLevelDataAndDimensions` ·
`LevelStorageSource.LevelStorageAccess.saveDataTag` · `SavedDataStorage.scheduleSave` ·
`SavedDataType` · `MinecraftServer.createLevels` · `MinecraftServer.getDataStorage` ·
`ServerChunkCache.getDataStorage` · `GameRules.bootstrap` · `GameRules.set` ·
`MinecraftServer.onGameRuleChanged` · `GameRuleMap` · `GameRuleCommand.register` ·
`WorldBorder.applyInitialSettings` · `WorldBorder.tick` ·
`PlayerList.addWorldborderListener` · `DimensionType` · `LevelStem` ·
`WorldGenSettings` · `WorldDimensions.bake` · `MinecraftServer.setDifficulty` ·
`ServerLevel.getCurrentDifficultyAt`

---

*Rules: names, never code · how the system works, not how the code reads ·
newest version only · every backticked name passes `tools/verify_names.py`.*
