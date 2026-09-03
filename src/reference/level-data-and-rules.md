# Level data and rules

> Verified against **Minecraft 26.2** · Reference · Who owns the seed, the spawn, the rules, the border and the dimensions, where each is saved, and what tells the client — looked up, not watched.

The facts about a world that are not blocks or entities: its seed and
dimensions, its spawn, its game time, its difficulty, its rules, its
border, its scoreboard and maps. In 26.2 almost none of them live in
*level.dat* any more — `PrimaryLevelData` is a stub and everything else is
a `SavedData` file under a *data/* folder, one server-global and one per
dimension — so the question this page answers is always the same one:
*which file remembers this, and who is allowed to change it.* The table
under [who owns what](#who-owns-what) is the page; the sections after it
are the prose behind its rows.

[Part IV](../systems/world/README.md) is where these things are used;
[the level tick](../systems/server/server-level-tick.md) is where most of
them are read.

## Who owns what

| datum | owner | saved as | told to the client by |
|---|---|---|---|
| seed, structures, bonus chest, dimension list | `WorldGenSettings` (`MinecraftServer.getWorldGenSettings`) | *data/minecraft/world_gen_settings.dat* | `CommonPlayerSpawnInfo`, `ClientboundLoginPacket` |
| world spawn | `PrimaryLevelData.respawnData` | *level.dat* | `ClientboundSetDefaultSpawnPositionPacket` |
| game time | `PrimaryLevelData.gameTime` (shared by every level) | *level.dat* | `ClientboundSetTimePacket` |
| day time | `ServerClockManager` | *data/minecraft/world_clocks.dat* | `ClientboundSetTimePacket` |
| difficulty, lock, hardcore | `LevelSettings.DifficultySettings` | *level.dat* | `ClientboundChangeDifficultyPacket` — hardcore alone rides in `ClientboundLoginPacket` |
| game type, allow-commands, name, data packs | `LevelSettings` | *level.dat* | `CommonPlayerSpawnInfo`; configuration phase |
| game rules | `GameRuleMap` via `GameRules` | *data/minecraft/game_rules.dat* | five rules only, plus `ClientboundGameRuleValuesPacket` on request |
| weather | `WeatherData` | *data/minecraft/weather.dat* | `ClientboundGameEventPacket` |
| world border | `WorldBorder`, one per `ServerLevel` | *dimensions/minecraft/…/data/minecraft/world_border.dat* | `ClientboundInitializeBorderPacket` and the five `ClientboundSetBorder…` packets |
| scoreboard | `ServerScoreboard` (`MinecraftServer.scoreboard`), buffered by `ScoreboardSaveData` at save time | *data/minecraft/scoreboard.dat* | `ClientboundSetObjectivePacket`, `ClientboundSetScorePacket`, `ClientboundSetPlayerTeamPacket` |
| maps | `MapItemSavedData` per `MapId`, `MapIndex` for the counter | *data/minecraft/maps/\<n\>.dat*, *data/minecraft/maps/last_id.dat* | `ClientboundMapItemDataPacket` |
| raids | `Raids` per level | *dimensions/minecraft/…/data/minecraft/raids.dat* | boss bars |
| chunk tickets | `TicketStorage` per level ([tickets](../systems/world/tickets-and-loading.md)) | *dimensions/minecraft/…/data/minecraft/chunk_tickets.dat* | — |
| dragon fight | `EnderDragonFight`, where `DimensionType.hasEnderDragonFight` | *dimensions/minecraft/…/data/minecraft/ender_dragon_fight.dat* | boss bars |
| boss bars, scheduled functions, random sequences, stopwatches, trader timers, command storage | `CustomBossEvents`, `TimerQueue`, `RandomSequences`, `Stopwatches`, `WanderingTraderData`, `CommandStorage` | *data/\<id\>.dat* | boss bars only |
| player data | `PlayerDataStorage` | *players/data/\<uuid\>.dat* | — |

## What is left in *level.dat*

`LevelData` is the read-only interface every `Level` exposes, and it is
small: `LevelData.getRespawnData`, `LevelData.getGameTime`,
`LevelData.isHardcore`, `LevelData.getDifficulty` and
`LevelData.isDifficultyLocked`. No day time — that has left level data
entirely for `ServerClockManager` ([the server tick](../systems/server/server-tick.md)) —
no weather, no rules, no border. `LevelData.RespawnData` is the world
spawn as a `GlobalPos` with yaw *and* pitch — it carries a dimension, so
`/setworldspawn` can point anywhere. `WritableLevelData` adds
`WritableLevelData.setSpawn`; `ServerLevelData` adds the game type,
`ServerLevelData.isInitialized`, `ServerLevelData.isAllowCommands` and
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
forwarded to the overworld's data, name and difficulty from the
`WorldData`; `DerivedLevelData.setGameTime` and
`DerivedLevelData.setGameType` are no-ops. That forwarding is how game
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

### The spawn every level reports is not the stored one

`ServerLevel.getRespawnData` forwards to `MinecraftServer.getRespawnData`,
which returns `MinecraftServer.effectiveRespawnData` — recomputed by
`MinecraftServer.updateEffectiveRespawnData` through
`Level.getWorldBorderAdjustedRespawnData`, which **relocates a spawn that
has fallen outside the border** to the border centre's surface, and by
`MinecraftServer.findRespawnDimension`, which falls back to the overworld
when the stored dimension no longer exists. So every level reports the
same spawn, and it is not the one *level.dat* holds.

## Two saved-data storages, neither of them the overworld's

`SavedData` is one flag, `SavedData.dirty` (`SavedData.setDirty`); a
`SavedDataType` is an id, a constructor, a `Codec` and a `DataFixTypes`.
`SavedDataStorage` — the class that *was* *DimensionDataStorage* — caches
them per folder (`SavedDataStorage.computeIfAbsent`, `SavedDataStorage.get`,
`SavedDataStorage.set`), writes `<id>.dat` as *{ data, DataVersion }*,
gzip-compressed, and saves through `SavedDataStorage.scheduleSave`: dirty
entries are encoded on the caller's thread and written on `Util.ioPool` in
at most `Util.maxAllowedExecutorThreads` tasks, chained through
`SavedDataStorage.pendingWriteFuture`; `SavedDataStorage.saveAndJoin`
waits.

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
`GameRules.SPAWN_MONSTERS`, `GameRules.KEEP_INVENTORY`, `GameRules.RANDOM_TICK_SPEED`
(3), `GameRules.PLAYERS_SLEEPING_PERCENTAGE` (100), `GameRules.RESPAWN_RADIUS`
(10), `GameRules.MAX_ENTITY_CRAMMING` (24), `GameRules.MAX_SNOW_ACCUMULATION_HEIGHT`
(1), `GameRules.MAX_MINECART_SPEED` (feature-gated) … fifty-nine of them,
all in [the reference](gamerules.md). The 1.21 names
(*doDaylightCycle*, *doMobSpawning*) and the *GameRules.BooleanValue* /
*IntegerValue* / *Key* classes are gone.

The values are saved data, not level data: a `GameRuleMap` — `SavedData`,
*game_rules.dat*, server-global — wrapped by the `GameRules` instance in
`MinecraftServer.gameRules`. `ServerLevel.getGameRules` returns the
server's: **one set for every dimension**, and `Level` has no rules
accessor at all, so the client has no game-rules object. The accessors are
`GameRules.get`, `GameRules.set` (which calls
`MinecraftServer.onGameRuleChanged`) and `GameRules.visitGameRuleTypes`
(how `GameRuleCommand.register` builds **two** literals per rule — the
bare id and the namespaced one).

### What the client hears

Five rules, and everything else is server-only. `GameRules.REDUCED_DEBUG_INFO`
goes as a `ClientboundEntityEventPacket`; `GameRules.LIMITED_CRAFTING` and
`GameRules.IMMEDIATE_RESPAWN` as `ClientboundGameEventPacket`
(`ClientboundGameEventPacket.LIMITED_CRAFTING`, `ClientboundGameEventPacket.IMMEDIATE_RESPAWN`)
and as fields of `ClientboundLoginPacket` (`GameRules.IMMEDIATE_RESPAWN`
inverted, as *showDeathScreen*); `GameRules.LOCATOR_BAR` through
`ServerWaypointManager`; and `GameRules.ADVANCE_TIME`, which broadcasts a
full clock sync because a paused clock is expressed on the wire as rate 0
([environment attributes](../systems/world/environment-attributes-and-timelines.md)).
`MinecraftServer.updateMobSpawningFlags` sends nothing; it only flips
`ServerChunkCache.setSpawnSettings`.

New is an in-game editor: `ServerboundClientCommandPacket.Action.REQUEST_GAMERULE_VALUES`
→ `ServerGamePacketListenerImpl.sendGameRuleValues` →
`ClientboundGameRuleValuesPacket` → `InWorldGameRulesScreen`, and edits
back as `ServerboundSetGameRulePacket` → `ServerGamePacketListenerImpl.handleSetGameRule`
(gated on `Permissions.COMMANDS_GAMEMASTER`).

## The border is per dimension

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
`EnvironmentAttributeMap` — where *ultrawarm*, *natural*, *bed_works*,
*respawn_anchor_works*, *piglin_safe*, *has_raids* and the fast-lava flag
went), `DimensionType.timelines` and `DimensionType.defaultClock` (a
`WorldClock` holder; `WorldClocks.OVERWORLD`, `WorldClocks.THE_END`). That
is where `DimensionType` lost its booleans: to the attribute map and the
timelines. `DimensionType.getStorageFolder` names the on-disk folder.
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
*world_gen_settings.dat*, server-global — holding `WorldOptions`
(`WorldOptions.seed`, `WorldOptions.generateStructures`,
`WorldOptions.generateBonusChest`) and `WorldDimensions` (the stem map;
`WorldDimensions.bake` produces the registry). It is read before the
server exists by `LevelStorageSource.getLevelDataAndDimensions` and
pushed in with `SavedDataStorage.set`; if the file is missing or
unreadable the loader logs an error and substitutes a **random seed**,
then carries on loading the world. `MinecraftServer.createLevels` makes one
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
