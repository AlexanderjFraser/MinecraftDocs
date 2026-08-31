# Players and sessions

> Verified against **Minecraft 26.2** · Part III · A player joins: from the end of the login handshake to a `ServerPlayer` standing in a `ServerLevel` with a tab list, a border and chunks on the way — and what happens to that object on death, dimension change and disconnect.

## Responsibility

A *session* is a `Connection` that has reached the play phase; a *player*
is the `ServerPlayer` entity that session drives. `PlayerList` is the
registry of both: it admits a login (bans, whitelist, capacity), builds the
first burst of packets that turn a bare connection into a client that can
render a world, keeps the tab list in sync, and on the way out saves the
player's data. `ServerPlayer` is a `Player` with a *connection*, a
`ServerPlayerGameMode`, per-player stats and advancements, and the
knowledge of which chunks its client has been sent.

The one sentence a player recognises: *the "Joining world" screen ends when
the server has finished this page.*

## The data it owns

- `PlayerList` (abstract; `DedicatedPlayerList` on a dedicated server) —
  `PlayerList.players` and `PlayerList.playersByUUID`, the canonical
  membership; `PlayerList.bans` (`UserBanList`), `PlayerList.ipBans`
  (`IpBanList`), `PlayerList.ops` (`ServerOpList`), `PlayerList.whitelist`
  (`UserWhiteList`) — JSON files next to `server.properties`;
  `PlayerList.stats` (`ServerStatsCounter` per UUID) and
  `PlayerList.advancements` (`PlayerAdvancements` per UUID), created lazily
  by `PlayerList.getPlayerStats` and `PlayerList.getPlayerAdvancements`;
  `PlayerList.playerIo`, the `PlayerDataStorage`; `PlayerList.viewDistance`
  and `PlayerList.simulationDistance`, the server-side caps.
- `PlayerDataStorage` — reads and writes `players/data/<uuid>.dat`
  (`LevelResource.PLAYER_DATA_DIR`), keeping the previous file as
  `.dat_old` and, on a corrupt read, renaming the bad one aside and
  falling back to the old copy; runs `DataFixTypes.PLAYER` on load. The
  save goes through `Entity.saveWithoutId` into a `TagValueOutput`
  ([Part II](../foundations/codecs-nbt-json.md)).
- `ServerPlayer` — `ServerPlayer.connection` (the
  `ServerGamePacketListenerImpl`, public and reassigned on respawn),
  `ServerPlayer.gameMode`, `ServerPlayer.chunkTrackingView` (starts
  `ChunkTrackingView.EMPTY`), `ServerPlayer.respawnConfig`
  (`ServerPlayer.RespawnConfig`: a `LevelData.RespawnData` plus a "forced"
  flag), `ServerPlayer.seenCredits`, `ServerPlayer.isChangingDimension`,
  `ServerPlayer.lastSentHealth` / `ServerPlayer.lastSentFood` /
  `ServerPlayer.lastSentExp` (the sync-on-change memory), `ServerPlayer.disconnected`,
  and the client's `ClientInformation` (`ServerPlayer.requestedViewDistance`
  defaults to 2 until the client says otherwise).
- `ServerLevel.players` is a *different* list from `PlayerList.players`:
  it is maintained by `ServerLevel.EntityCallbacks` (`ServerLevel.EntityCallbacks.onTrackingStart` /
  `ServerLevel.EntityCallbacks.onTrackingEnd`) as the entity manager adds and removes the player
  entity — so it is per level and driven by the entity system, not by
  `PlayerList`.
- `CommonListenerCookie` — the record (profile, latency, client
  information, transferred flag) that travels from login through
  configuration into play.

## When it runs

All on the *Server thread*, but not all in the tick. The login and
configuration listeners are ticked from `ServerConnectionListener.tick`
(the *connection* section of `MinecraftServer.tickChildren`), and the
actual join, `PlayerList.placeNewPlayer`, runs from a configuration task
when the client's `ServerboundFinishConfigurationPacket` is handled — a
queued packet, so at the top of a tick. Respawn is a packet
(`ServerboundClientCommandPacket`); disconnect is
`Connection.handleDisconnection`, again from the connection tick.

Two off-thread pieces: the Mojang session check on a
"User Authenticator" thread spawned by
`ServerLoginPacketListenerImpl.handleKey`, and the spawn-chunk load, which
`PrepareSpawnTask` waits on with tickets rather than blocking. The player
tick is split: `ServerPlayer.doTick` (food, stat and health sync) is driven
by the connection through `ServerGamePacketListenerImpl.tick`, *after* the
levels; `ServerPlayer.tick` (containers, camera, advancement criteria) is
driven by the level's entity loop, and players are ticked there regardless
of their chunk's ticking state.

## The trace: a player joins

```mermaid
sequenceDiagram
    participant L as ServerLoginPacketListenerImpl
    participant PL as PlayerList
    participant CFG as ServerConfigurationPacketListenerImpl
    participant PST as PrepareSpawnTask
    participant PDS as PlayerDataStorage
    participant SP as ServerPlayer
    participant G as ServerGamePacketListenerImpl
    participant SL as ServerLevel
    participant CM as ChunkMap

    L->>PL: canPlayerLogin — ban, whitelist, ip ban, capacity → a reason or null
    L->>PL: disconnectAllPlayersWithProfile — a duplicate is kicked first; wait in WAITING_FOR_DUPE_DISCONNECT
    L->>CFG: handleLoginAcknowledgement — CommonListenerCookie.createInitial, startConfiguration
    CFG->>CFG: brand, server links, enabled features, SynchronizeRegistriesTask (+ tags), optional tasks
    CFG->>PST: start — loadPlayerData for SavedPosition only; none → PlayerSpawnFinder.findSpawn
    PST->>SL: TicketType.PLAYER_SPAWN, radius 3 — chunks load while the client is still configuring
    CFG->>CFG: JoinWorldTask — ClientboundFinishConfigurationPacket; client replies FinishConfiguration
    CFG->>PL: handleConfigurationFinished — re-check duplicate and canPlayerLogin
    CFG->>PST: spawnPlayer → Ready.spawn
    PST->>SL: waitForEntities(spawn chunk, 3)
    PST->>SP: new ServerPlayer(server, level, profile, clientInformation)
    PST->>PDS: load — the full .dat, then ServerPlayer.load
    PST->>PL: placeNewPlayer(connection, player, cookie)
    PL->>G: new ServerGamePacketListenerImpl — player.connection set; suspendFlushing
    PL->>G: ClientboundLoginPacket · ChangeDifficulty · PlayerAbilities · SetHeldSlot · UpdateRecipes
    PL->>G: sendPlayerPermissionLevel (EntityEvent 24–28) · ClientboundCommandsPacket
    PL->>G: initial recipe book · updateEntireScoreboard · "multiplayer.player.joined" to all
    PL->>G: teleport → ClientboundPlayerPositionPacket · sendServerStatus
    PL->>G: ClientboundPlayerInfoUpdatePacket (everyone) — then players.add; everyone gets the newcomer
    PL->>G: sendLevelInfo — border, clocks, default spawn, rain state, LEVEL_CHUNKS_LOAD_START, ticking state
    PL->>SL: addNewPlayer → entityManager.addNewEntity
    SL->>CM: onTrackingStart → updatePlayerStatus — ChunkTrackingView set, chunks queued to PlayerChunkSender
    PL->>G: boss events · active effects · initInventoryMenu · resumeFlushing
    G->>G: ServerboundPlayerLoadedPacket → markClientLoaded (or 60 ticks)
```

Narrated:

1. **Admission is a `Component` or null.** `PlayerList.canPlayerLogin`
   checks `UserBanList`, then `UserWhiteList` (unless
   `PlayerList.canBypassPlayerLimit`), then `IpBanList`, then capacity, and
   returns the disconnect reason. It runs twice: in
   `ServerLoginPacketListenerImpl.verifyLoginAndFinishConnectionSetup` and
   again in `ServerConfigurationPacketListenerImpl.handleConfigurationFinished`,
   because a ban or whitelist change may have landed during configuration.
2. **Duplicates are resolved by eviction.** `PlayerList.disconnectAllPlayersWithProfile`
   kicks any existing player with the same UUID
   (`PlayerList.DUPLICATE_LOGIN_DISCONNECT_MESSAGE`) and the login parks in
   `ServerLoginPacketListenerImpl.State.WAITING_FOR_DUPE_DISCONNECT` until
   the old session is gone.
3. **Configuration does the bulk transfer.** `ServerConfigurationPacketListenerImpl.startConfiguration`
   sends the brand payload, `ClientboundServerLinksPacket`,
   `ClientboundUpdateEnabledFeaturesPacket` and runs `SynchronizeRegistriesTask`
   (registries and tags — [Part II](../foundations/tags.md)), then the
   optional tasks (code of conduct, resource pack). [Protocol
   phases](../networking/protocol-phases.md) owns this phase;
   what matters here is that two tasks are queued last by
   `ServerConfigurationPacketListenerImpl.returnToWorld`: `PrepareSpawnTask`
   and `JoinWorldTask`.
4. **The spawn chunks load before the player exists.**
   `PrepareSpawnTask.start` reads the player's `.dat` once, for
   `ServerPlayer.SavedPosition` only (dimension, position, rotation); a
   new player instead gets `PlayerSpawnFinder.findSpawn`, an asynchronous
   search over up to `PlayerSpawnFinder.ABSOLUTE_MAX_ATTEMPTS` (1024)
   candidates within `GameRules.RESPAWN_RADIUS`, loading each candidate
   chunk with `TicketType.SPAWN_SEARCH`. Then a `TicketType.PLAYER_SPAWN`
   ticket of radius `PrepareSpawnTask.PREPARE_CHUNK_RADIUS` (3) is placed
   and the task ticks until the `ChunkLoadCounter` says they are in.
   The client is meanwhile receiving registries; `JoinWorldTask` sends
   `ClientboundFinishConfigurationPacket` only when both are done.
5. **The `ServerPlayer` is born in a configuration task, not in `PlayerList`.**
   `PrepareSpawnTask.spawnPlayer` → its `PrepareSpawnTask.Ready` state: `ServerLevel.waitForEntities`
   makes sure the spawn chunk's entities are loaded (a vehicle to
   re-mount, say), constructs the `ServerPlayer` — whose constructor
   fetches its `ServerStatsCounter` and `PlayerAdvancements` from
   `PlayerList` — reads the `.dat` a second time for the full
   `Entity.load`, snaps it to the spawn position, and only then calls
   `PlayerList.placeNewPlayer`. Afterwards `ServerPlayer.loadAndSpawnEnderPearls`
   and `ServerPlayer.loadAndSpawnParentVehicle` restore what the player
   took with them when they left.
6. **`PlayerList.placeNewPlayer` is one flush.** It creates the
   `ServerGamePacketListenerImpl` (which sets `ServerPlayer.connection`
   and owns a `PlayerChunkSender`), switches the inbound protocol to play,
   suspends flushing, and sends in this order: `ClientboundLoginPacket`
   (entity id, hardcore flag, the level keys, max players, view and
   simulation distance, the `CommonPlayerSpawnInfo` from
   `ServerPlayer.createCommonSpawnInfo`), `ClientboundChangeDifficultyPacket`,
   `ClientboundPlayerAbilitiesPacket`, `ClientboundSetHeldSlotPacket`,
   `ClientboundUpdateRecipesPacket`; then the permission level as a
   `ClientboundEntityEventPacket` (ids 24–28) and the command tree
   (`Commands.sendCommands` → `ClientboundCommandsPacket`); the recipe book,
   the scoreboard, the join message; the first `ClientboundPlayerPositionPacket`
   via `ServerGamePacketListenerImpl.teleport`; the server status.
7. **The tab list, in a careful order.** The joiner gets a
   `ClientboundPlayerInfoUpdatePacket` listing everyone already present;
   *then* `PlayerList.players`; then everyone (joiner included) gets one listing
   the joiner. `PlayerList.sendLevelInfo` follows: `ClientboundInitializeBorderPacket`,
   the clocks' full sync (`ServerClockManager.createFullSyncPacket`),
   `ClientboundSetDefaultSpawnPositionPacket`, the rain and thunder levels
   as `ClientboundGameEventPacket`s if it is raining,
   `ClientboundGameEventPacket.LEVEL_CHUNKS_LOAD_START`, and
   `ServerTickRateManager.updateJoiningPlayer` (the tick-rate state).
8. **Entering the level starts the chunks.** `ServerLevel.addNewPlayer` →
   `PersistentEntitySectionManager.addNewEntity` → `ServerLevel.EntityCallbacks`
   `ServerLevel.EntityCallbacks.onTrackingStart` adds the player to `ServerLevel.players` and to the
   `ServerChunkCache`, whose `ChunkMap.updatePlayerStatus` registers the
   player with `DistanceManager` (the player ticket) and computes the first
   `ChunkTrackingView`; chunks inside it are marked pending for the
   `PlayerChunkSender`, which sends them in batches at the end of each
   server tick (`PlayerChunkSender.MAX_UNACKNOWLEDGED_BATCHES`, 10, before
   it waits for the client). Part IV's [tickets-and-loading](../world/tickets-and-loading.md)
   page picks up from here.
9. **Loaded means the client said so.** After boss events, active effects
   and `ServerPlayer.initInventoryMenu`, flushing resumes. The client
   answers with `ServerboundPlayerLoadedPacket` → `ServerGamePacketListenerImpl.markClientLoaded`;
   if it has not within `ServerGamePacketListenerImpl.CLIENT_LOADED_TIMEOUT_TIME`
   (60 ticks) the server marks it loaded anyway. Until then the player
   does not take damage or move.

### Respawn, dimension change and disconnect

- **Respawn makes a new object.** `ServerboundClientCommandPacket` with
  `ServerboundClientCommandPacket.Action.PERFORM_RESPAWN` → `PlayerList.respawn`. `ServerPlayer.findRespawnPositionAndUseSpawnBlock`
  turns the `ServerPlayer.RespawnConfig` into a `TeleportTransition` (consuming a bed
  or anchor charge; `TeleportTransition.missingRespawnBlock` if the block is
  gone; `TeleportTransition.createDefault` at the world spawn otherwise —
  both use `MinecraftServer.findRespawnDimension` and
  `ServerLevel.getRespawnData`). The old player is removed from its level
  with `Entity.RemovalReason.KILLED` (or `Entity.RemovalReason.CHANGED_DIMENSION` after the
  credits), a **new** `ServerPlayer` is constructed with the same profile,
  `ServerPlayer.restoreFrom` copies what survives death (everything, if
  *keepInventory*), it takes the old entity id and the same
  `ServerGamePacketListenerImpl`, and the client is told with
  `ClientboundRespawnPacket` (its `ClientboundRespawnPacket.dataToKeep` bits say whether attributes
  and entity data carry over), a position, difficulty, experience,
  effects, `PlayerList.sendLevelInfo` and the permission level again. Anyone holding
  the old `ServerPlayer` reference holds a corpse.
- **Dimension change keeps the object.** `ServerPlayer.teleport` with a
  `TeleportTransition` to another level: `ServerPlayer.isChangingDimension` set,
  `ClientboundRespawnPacket` with `ClientboundRespawnPacket.KEEP_ALL_DATA`, removal from the old
  level with `Entity.RemovalReason.CHANGED_DIMENSION` then `Entity.unsetRemoved`,
  `ServerPlayer.setServerLevel`, the teleport, `ServerLevel.addDuringTeleport`,
  and then the same level-info and inventory re-sync
  (`ServerPlayer.sendAllPlayerInfo`, `ServerPlayer.sendActivePlayerEffects`)
  a join gets, plus `ServerPlayer.teleportSpectators` for anyone
  spectating them. Same-dimension teleports are just
  `ServerGamePacketListenerImpl.teleport` and `ServerPlayer.resetPosition`.
- **Disconnect is a level tick away.** The channel closes on Netty;
  `ServerConnectionListener.tick` notices and calls
  `Connection.handleDisconnection` → `ServerGamePacketListenerImpl.onDisconnect`
  → `ServerGamePacketListenerImpl.removePlayerFromWorld`: the leave
  message, `ServerPlayer.disconnect` (ejects passengers, stops sleeping),
  `PlayerList.remove` — `Stats.LEAVE_GAME`, `PlayerList.save` (the `.dat`,
  the stats JSON, the advancements JSON), and if the player was the sole
  rider the whole vehicle chain and any in-flight ender pearls leave the
  world with `Entity.RemovalReason.UNLOADED_WITH_PLAYER` (they come back
  from the `.dat` on the next join); `ServerLevel.removePlayerImmediately`;
  a `ClientboundPlayerInfoRemovePacket` to everyone. On a singleplayer
  server the owner's disconnect is what calls `MinecraftServer.halt`
  (`ServerCommonPacketListenerImpl.onDisconnect`).

## Interfaces

- **Called by:** `ServerLoginPacketListenerImpl` and
  `ServerConfigurationPacketListenerImpl` (admission and the join),
  `ServerGamePacketListenerImpl` (respawn, disconnect),
  `MinecraftServer.saveEverything` (`PlayerList.saveAll` runs before the
  chunks), `MinecraftServer.tickChildren` (`PlayerList.tick`).
- **Calls into:** `ServerLevel` and `PersistentEntitySectionManager`
  (entity membership), `ChunkMap` / `DistanceManager` (player tickets and
  tracking), `ServerStatsCounter`, `PlayerAdvancements`, `Commands`,
  `ServerScoreboard`, `CustomBossEvents`.
- **Crosses the network as:** the sequence in step 6–7 (clientbound);
  `ClientboundRespawnPacket` on respawn and dimension change;
  `ClientboundPlayerInfoUpdatePacket` / `ClientboundPlayerInfoRemovePacket`
  for the tab list; `ClientboundSetChunkCacheRadiusPacket` and
  `ClientboundSetSimulationDistancePacket` when `PlayerList.setViewDistance`
  / `PlayerList.setSimulationDistance` change; `ClientboundSetHealthPacket`
  from `ServerPlayer.doTick` whenever health, food or saturation moved;
  `ClientboundKeepAlivePacket` every 15 s. Serverbound:
  `ServerboundLoginAcknowledgedPacket`, `ServerboundFinishConfigurationPacket`,
  `ServerboundPlayerLoadedPacket`, `ServerboundClientCommandPacket`,
  `ServerboundKeepAlivePacket`.
- **Data-driven by:** `banned-players.json`, `banned-ips.json`, `ops.json`,
  `whitelist.json` (`PlayerList.USERBANLIST_FILE` and siblings);
  `players/data/<uuid>.dat`; `GameRules.RESPAWN_RADIUS`;
  `server.properties` for view/simulation distance and the forced game
  mode (`MinecraftServer.getForcedGameType` beats the saved mode beats
  `MinecraftServer.getDefaultGameType`, in `ServerPlayer.calculateGameModeForNewPlayer`).

## Invariants and surprises

- **The player `.dat` is read twice on join and written on every save and
  every disconnect.** Position first (to know where to load chunks),
  everything later (once the chunks are there). `ServerPlayer.SavedPosition`
  is the first read's whole result.
- **A respawned player is a new `ServerPlayer`; a player who changed
  dimension is not.** The entity id survives both; the object survives
  only the second.
- **Two player lists.** `PlayerList.players` is "who is on the server";
  `ServerLevel.players` is "whose entity is in this level", maintained by
  the entity manager's callbacks. `PlayerList` never writes the level's
  list.
- **Nothing in the play phase runs before `ServerConfigurationPacketListenerImpl.handleConfigurationFinished`
  re-admits the player.** The whitelist is consulted at login *and* at the
  moment of entering the world.
- **Players are ticked twice, from two places.** `ServerPlayer.doTick` from the
  connection (after the levels), `ServerPlayer.tick` from the level's entity loop — and
  the level loop ticks players even outside entity-ticking range, which is
  how a player standing in an otherwise idle chunk still moves.
- **The owner of a singleplayer world is looked up by the world's stored
  UUID**, not the current profile (`PlayerList.loadPlayerData`), which is
  why switching from offline to online mode does not lose the inventory.
- **Keep-alive is a 15-second pair.** `ServerCommonPacketListenerImpl.keepConnectionAlive`
  sends one every `ServerCommonPacketListenerImpl.LATENCY_CHECK_INTERVAL` and disconnects with
  `ServerCommonPacketListenerImpl.TIMEOUT_DISCONNECTION_MESSAGE` if the previous one is still unanswered;
  latency is smoothed 3:1 toward the new sample.

## Where to look

`PlayerList.placeNewPlayer` · `PlayerList.respawn` · `PlayerList.remove` ·
`PlayerList.canPlayerLogin` · `ServerPlayer.teleport` · `ServerPlayer.restoreFrom` ·
`ServerPlayer.findRespawnPositionAndUseSpawnBlock` · `ServerPlayer.doTick` · `PrepareSpawnTask` · `JoinWorldTask` · `PlayerSpawnFinder` ·
`ServerLoginPacketListenerImpl` · `ServerConfigurationPacketListenerImpl` ·
`ServerGamePacketListenerImpl.onDisconnect` ·
`ServerGamePacketListenerImpl.removePlayerFromWorld` ·
`ServerGamePacketListenerImpl.markClientLoaded` · `ServerCommonPacketListenerImpl` · `PlayerDataStorage`
· `TeleportTransition` · `ChunkMap.updatePlayerStatus` · `PlayerChunkSender`

---

*Rules: names, never code · how the system works, not how the code reads ·
newest version only · every backticked name passes `tools/verify_names.py`.*
