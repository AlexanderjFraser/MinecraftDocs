# Server lifecycle

> Verified against **Minecraft 26.2** · Part III · `/stop` on a dedicated server: from a flag flipped on the Server thread to the JVM exiting with every chunk written and `session.lock` released — and the startup that put it all there.

## Responsibility

Everything between "java -jar server.jar" and the process ending. Startup
is a fixed sequence — properties, EULA, the world lock, data packs and
registries, the `DedicatedServer` object, the Server thread, the levels, the
persisted tickets, the listeners — and shutdown is its mirror, run entirely
on the Server thread from the loop's *finally*. Saving has two entry points,
not one: `MinecraftServer.saveEverything` (players then chunks) for autosave,
`/save-all` and the integrated server's pause, and `MinecraftServer.saveAllChunks`
on its own, which is what shutdown calls after saving players by hand. The
dedicated-only side threads — console, watchdog, RCON, query, JSON-RPC — each
get a paragraph because each is a one-class system.

The one sentence a player recognises: *"Saving chunks…" is the server
refusing to die until the world is on disk.*

## The data it owns

- `MinecraftServer` — the state machine is three booleans:
  `MinecraftServer.running` (volatile, the loop condition;
  `MinecraftServer.halt` clears it), `MinecraftServer.stopped` (plain, set in
  the *finally*, read from other threads through `MinecraftServer.isStopped`)
  and `MinecraftServer.isReady` (volatile, set at the bottom of every loop
  iteration). `MinecraftServer.isReady` is not what prints "Done" — that is
  logged in `DedicatedServer.initServer`, before the loop is entered. Its two
  readers are the client's world-load screen and the JSON-RPC server-state
  method. `MinecraftServer.isShutdown` is not a flag at all: it asks whether
  the Server thread is still alive.
  Also `MinecraftServer.levels` (a `LinkedHashMap` keyed by level
  `ResourceKey`, overworld inserted first), `MinecraftServer.worldData`
  (the `WorldData`; `PrimaryLevelData` on disk), `MinecraftServer.storageSource`
  (the `LevelStorageSource.LevelStorageAccess`), `MinecraftServer.playerDataStorage`,
  `MinecraftServer.savedDataStorage` (the server-wide `SavedDataStorage`),
  `MinecraftServer.resources` (the `MinecraftServer.ReloadableResources`
  from the `WorldStem`), `MinecraftServer.connection`
  (the `ServerConnectionListener`).
- `LevelStorageSource` — the saves directory; `LevelStorageSource.createAccess`
  / `LevelStorageSource.validateAndCreateAccess` open one world as a
  `LevelStorageSource.LevelStorageAccess`, which holds the `DirectoryLock`
  on `session.lock` for its lifetime and knows the layout through
  `LevelStorageSource.LevelDirectory` and `LevelResource` (`LevelResource.LEVEL_DATA_FILE`
  `level.dat`, `LevelResource.OLD_LEVEL_DATA_FILE` `level.dat_old`, `LevelResource.PLAYER_DATA_DIR`
  *players/data*, `LevelResource.PLAYER_STATS_DIR`, `LevelResource.PLAYER_ADVANCEMENTS_DIR`, `LevelResource.DATAPACK_DIR`,
  `LevelResource.DATA` for saved data). Per-dimension folders come from
  `DimensionType.getStorageFolder` and hold *region/*, *entities/*, *poi/*.
- `DirectoryLock` — `FileChannel.tryLock` on `session.lock`
  (`DirectoryLock.LOCK_FILE`). An OS advisory lock, not file contents:
  a crashed JVM releases it; a second server on the same world fails with
  `DirectoryLock.LockException`; the client's world list greys out a world
  whose lock `DirectoryLock.isLocked` reports held.
- `DedicatedServerSettings` / `DedicatedServerProperties` — `server.properties`
  as typed fields (`DedicatedServerProperties.maxTickTime`, `DedicatedServerProperties.serverPort`,
  `DedicatedServerProperties.pauseWhenEmptySeconds`, `DedicatedServerProperties.enableRcon`, `DedicatedServerProperties.enableQuery`, `DedicatedServerProperties.syncChunkWrites`,
  `DedicatedServerProperties.regionFileComression` — the typo is Mojang's — and the
  `DedicatedServerProperties.managementServerEnabled` family for JSON-RPC). `Eula` reads `eula.txt`.
- `ServerWatchdog` — a `Runnable` holding `ServerWatchdog.maxTickTimeNanos`
  and the `DedicatedServer` it watches (it needs the server to read the tick
  deadline and to build its crash report).

## When it runs

- **Startup:** `server/Main` on the JVM main thread up to
  `MinecraftServer.spin`; the world load partly on `Util.backgroundExecutor`;
  then `MinecraftServer.runServer` → `DedicatedServer.initServer` →
  `MinecraftServer.loadLevel` on the *Server thread* before the first tick.
- **Save:** always on the Server thread. `MinecraftServer.saveEverything` is
  called by `MinecraftServer.autoSave` (which the pause-when-empty transition
  also goes through), by `SaveAllCommand`, once at the end of
  `DedicatedServer.initServer`, twice from `IntegratedServer`, and by the
  JSON-RPC save method. Shutdown does not call it — it does
  `PlayerList.saveAll` and `MinecraftServer.saveAllChunks` itself. The one
  asynchronous piece is the region-file write, which the chunk storage hands
  to `IOWorker` (Part IV, [chunk-storage](../world/chunk-storage.md)); a save
  with *flush* true joins it.
- **Shutdown:** `/stop` runs `StopCommand` on the Server thread and flips
  `MinecraftServer.running`; the loop exits; `MinecraftServer.stopServer` and
  `MinecraftServer.onServerExit` run in `MinecraftServer.runServer`'s *finally* — on the
  same thread, and *also after a crash*, so a crashed server still saves and
  unlocks. Ctrl-C or SIGTERM arrive on the "Server Shutdown Thread" JVM
  hook, which calls `MinecraftServer.halt` with *wait* true and blocks until
  the Server thread has finished.

## The trace: `/stop`

```mermaid
sequenceDiagram
    participant SC as StopCommand
    participant MS as MinecraftServer (Server thread)
    participant DS as DedicatedServer
    participant PP as PacketProcessor
    participant SCL as ServerConnectionListener
    participant PL as PlayerList
    participant SL as ServerLevel (each)
    participant SCC as ServerChunkCache
    participant CM as ChunkMap
    participant LSA as LevelStorageAccess
    participant JVM as JVM

    SC->>MS: halt(false) — running = false; nothing else
    MS->>MS: current tick finishes; runServer's while loop exits; stopped = true
    MS->>DS: stopServer — NotificationManager.serverShuttingDown
    DS->>MS: super.stopServer
    MS->>PP: close — late packets are rejected, not queued
    MS->>SCL: stop — the bound listening channels close; accepted connections do not
    MS->>PL: saveAll, then removeAll — every player written, then disconnected
    MS->>SL: noSave = false on every level (/save-off is overridden)
    loop while any ChunkMap.hasWork
        MS->>SCC: deactivateTicketsOnClosing · tick — unloads drain with 1 ms slices
    end
    MS->>MS: saveAllChunks(silent=false, flush=true, force=false)
    MS->>SL: save → saveLevelData, ServerChunkCache.save(flush) → ChunkMap.saveAllChunks(true) — every holder accessed since last save, repeated until nothing is left; the POI storage flushed; IOWorker synchronized
    MS->>LSA: saveDataTag(worldData) — level.dat via temp file, previous → level.dat_old
    MS->>MS: savedDataStorage.saveAndJoin — the server-wide saved data, after level.dat
    MS->>SL: close — ServerChunkCache.close (save again, light engine, ChunkMap.close), entityManager.close
    MS->>MS: savedDataStorage.close · resources.close
    MS->>LSA: close — session.lock released
    DS->>DS: Util.shutdownExecutors — the Worker-Main and IO-Worker pools stop
    MS->>DS: onServerExit — text filter, GUI, RconThread.stop, the query thread, ManagementServer.stop
    DS->>JVM: the Server thread ends; every other thread is a daemon; the JVM exits
```

Narrated:

1. **`MinecraftServer.halt` is a flag.** `StopCommand` (permission `Commands.LEVEL_OWNERS`,
   so a console line, an RCON command or an owner-level player) calls
   `MinecraftServer.halt` with *wait* false. It sets `MinecraftServer.running` to false
   and returns; the tick in progress completes normally and the loop
   condition fails at the top of the next.
2. **Teardown is the *finally*.** `MinecraftServer.runServer` sets `MinecraftServer.stopped`, then calls
   `MinecraftServer.stopServer`. `DedicatedServer.stopServer` wraps the base with a
   `NotificationManager.serverShuttingDown` notification (the JSON-RPC
   feed) and, afterwards, `Util.shutdownExecutors`.
3. **Inputs close first — but only the front door.** `PacketProcessor.close`
   makes `PacketProcessor.scheduleIfPossible` throw, so a Netty thread that
   decodes a packet now cannot queue it. `ServerConnectionListener.stop`
   then closes the *bound* channels, and only those: closing a Netty parent
   channel does not close the connections it accepted. Live sessions are
   severed one step later by `PlayerList.removeAll`, which is why a connection
   still in handshake, login or configuration — one with no `ServerPlayer` —
   is closed by neither, and simply dies with the process.
4. **Players before chunks.** `PlayerList.saveAll` writes every player's
   `.dat`, stats and advancements; `PlayerList.removeAll` disconnects them.
   A player's chunk tickets go away with them, which is what lets the next
   step finish.
5. **Every level is forced saveable and drained.** `ServerLevel.noSave` is
   cleared on every level — `/save-off` does not survive `/stop` — and then
   the loop: while any `ChunkMap.hasWork`, `ServerChunkCache.deactivateTicketsOnClosing`
   (persistent tickets are *deactivated* and written, not dropped, so
   `MinecraftServer.prepareLevels` can re-arm them next boot), `ServerChunkCache.tick`, and
   `MinecraftServer.waitUntilNextTick` with the deadline one millisecond
   out, so unloads proceed in slices and the main-thread queue keeps
   draining chunk results.
6. **The flush save.** `MinecraftServer.saveAllChunks` with *flush* true:
   the scoreboard to saved data; per level `ServerLevel.save` →
   `ServerLevel.saveLevelData` (`SavedDataStorage.saveAndJoin`) and
   `ServerChunkCache.save`, which runs the distance manager once more and
   `ChunkMap.saveAllChunks` in flush mode — every `ChunkHolder` that
   `ChunkHolder.wasAccessibleSinceLastSave`, repeated until no chunk is
   dirty, the `PoiManager`'s sections through `SectionStorage.flushAll`, the
   unloads processed, and the `IOWorker` synchronised; then the entity
   storage. Finally `LevelStorageSource.LevelStorageAccess.saveDataTag`
   writes `level.dat` through `PrimaryLevelData.createTag` to a temp file
   and `Util.safeReplaceFile` rotates the previous into `level.dat_old`.
   The server-wide `SavedDataStorage` is joined *after* that, not before. Note
   there are two tiers of saved data: this one, and a per-level
   `SavedDataStorage` reached through the chunk source, which is what
   `ServerLevel.saveLevelData` flushes.
7. **Close everything that owns a file.** `ServerLevel.close` →
   `ServerChunkCache.close` (one more `ServerChunkCache.save`, the `ThreadedLevelLightEngine`,
   `ChunkMap.close`) and the entity manager; the server-wide
   `SavedDataStorage`; the `MinecraftServer.ReloadableResources`; and at last
   `LevelStorageSource.LevelStorageAccess.close`, which releases the `DirectoryLock`.
8. **The pools die with the server.** `Util.shutdownExecutors` shuts the
   background and IO pools with a three-second grace each. After
   `DedicatedServer.onServerExit` stops the RCON, query and management
   threads, the Server thread simply returns. No `System.exit` on a clean
   stop: the Server thread was the only non-daemon thread left.

### Startup, in order

1. **`Main`** (JVM main thread): `SharedConstants.tryDetectVersion`,
   arguments (`--nogui`, `--port`, `--universe`, `--world`, `--forceUpgrade`,
   `--initSettings`…), `Bootstrap.bootStrap` and `Bootstrap.validate`,
   `Util.startTimerHackThread`. Then `DedicatedServerSettings`
   (`server.properties`, rewritten with `DedicatedServerSettings.forceSave`
   so new keys appear), `RegionFileVersion.configure` from the compression
   property, and `Eula` — no agreement means *main* returns; no thread was
   ever spun.
2. **JSON-RPC binds before the world exists.** `Services.create`, a
   `NotificationManager`, and `JsonRpc.create` starts the `ManagementServer`
   (its own Netty group, "Management server IO") on the management port if
   enabled. It outlives the world and is stopped last.
3. **The lock.** `LevelStorageSource.createDefault` on the universe
   directory, `LevelStorageSource.validateAndCreateAccess` on the level
   name: the `DirectoryLock` is taken in the constructor. If the world
   exists, `LevelStorageSource.LevelStorageAccess.getUnfixedDataTagWithFallback` reads
   `level.dat` (or `level.dat_old`, restoring it), `LevelStorageSource.LevelStorageAccess.fixAndGetSummaryFromTag`
   yields a `LevelSummary` and the `LevelSummary.requiresManualConversion`
   / `LevelSummary.isCompatible` gates apply.
4. **Packs, registries, resources — `WorldLoader.load`.** `ServerPacksSource.createPackRepository`
   over the world's *datapacks/*; a `WorldLoader.InitConfig`; then the
   stages [Part II](../foundations/identifiers-and-registries.md) described:
   the resource manager, the static registries and their pending tags,
   `RegistryDataLoader` for the worldgen then dimension registries, the
   `WorldLoader.WorldDataSupplier` (reads `level.dat` into a
   `PrimaryLevelData` via `LevelStorageSource.getLevelDataAndDimensions`,
   or `Main.createNewWorldData`), `ReloadableServerResources.loadResources`,
   and a `WorldStem` at the end. `Util.blockUntilDone` waits for it on the
   main thread. `--forceUpgrade` (and `--recreateRegionFiles`) runs
   `WorldUpgrader` here — and then
   `LevelStorageSource.LevelStorageAccess.saveDataTag` rewrites `level.dat`
   **unconditionally**, upgrade or not, before the server object exists.
5. **`MinecraftServer.spin`.** The `DedicatedServer` is constructed on the
   main thread inside the factory (port, demo, id, the Swing GUI via
   `DedicatedServer.showGui` unless headless); its constructor already does
   real work — the text filter, the server links, and the code-of-conduct
   folder, which throws if *enable-code-of-conduct* is set and the directory
   is missing. Then `MinecraftServer.spin` starts the Server thread (at
   priority 8 on a machine with more than four processors) and returns; back
   in `Main`, a "Server Shutdown Thread" hook is registered and *main*
   returns. The client registers its own, separate "Client Shutdown Thread".
6. **`DedicatedServer.initServer`** (Server thread): the "Server console
   handler" daemon thread (reads stdin into `DedicatedServer.consoleInput`
   as `ConsoleInput` entries; `DedicatedServer.handleConsoleInputs` runs them
   each tick); properties into fields; the key pair;
   `ServerConnectionListener.startTcpServerListener` — a bind failure
   returns false and `MinecraftServer.runServer` throws "Failed to initialize
   server"; `DedicatedServer.convertOldUsers`, which retries each of five
   legacy-file conversions twice with a five-second wait and returns false if
   `OldUsersConverter` still finds the old *.txt* lists (the second way
   startup fails); a `DedicatedPlayerList`; then
   **`MinecraftServer.loadLevel`**.
7. **`MinecraftServer.loadLevel`** = `MinecraftServer.createLevels` → `MinecraftServer.forceDifficulty`
   → `MinecraftServer.prepareLevels`. `MinecraftServer.createLevels` builds the overworld
   `ServerLevel` first (with the custom spawners), pulls the scoreboard,
   command storage and stopwatches out of saved data, and if
   `ServerLevelData.isInitialized` is false runs `MinecraftServer.setInitialSpawn`
   (a spiral over `MinecraftServer.SPAWN_POSITION_SEARCH_RADIUS` chunks,
   the bonus chest); then one `ServerLevel` per remaining `LevelStem` with a
   `DerivedLevelData` (the Nether and End share the overworld's `LevelData`).
   `MinecraftServer.prepareLevels` does **not** load a fixed spawn radius: it calls
   `TicketStorage.activateAllDeactivatedTickets` — the tickets written at
   the last shutdown — under a `ChunkLoadCounter`, and spins
   `MinecraftServer.waitUntilNextTick` in 10 ms slices (`MinecraftServer.PREPARE_LEVELS_DEFAULT_DELAY_NANOS`)
   until nothing is pending, reporting through the `LevelLoadListener`
   stages (`LevelLoadListener.Stage.LOAD_INITIAL_CHUNKS`).
8. **"Done".** Back in `DedicatedServer.initServer`: `QueryThreadGs4.create` if
   `DedicatedServerProperties.enableQuery`, `RconThread.create` if `DedicatedServerProperties.enableRcon`, the watchdog thread
   if `DedicatedServer.getMaxTickLength` is positive, JMX if enabled, an
   immediate `MinecraftServer.saveEverything` with *flush* and *force*, and
   `NotificationManager.serverStarted`. `MinecraftServer.runServer` enters the loop; after
   the first tick `MinecraftServer.isReady` is set.

### The side threads

- **Watchdog.** `ServerWatchdog.run` sleeps until the next moment a
  violation is possible, wakes, and compares `Util.getNanos` with
  `MinecraftServer.getNextTickTime`. Past
  `DedicatedServerProperties.maxTickTime` (default 60 000 ms; ≤ 0 removes the
  thread entirely) it writes a crash report
  (`ServerWatchdog.createWatchdogCrashReport`, with every thread's stack and
  the Server thread's grafted onto the error), calls `System.exit`, and
  schedules `Runtime.halt` ten seconds later
  (`ServerWatchdog.MAX_SHUTDOWN_TIME`) in case the shutdown hook is stuck. It
  *writes* no game state, but it reads plenty unsynchronised — the game
  rules, every level's `ServerLevel.getWatchdogStats` — off-thread, while the
  Server thread is mid-tick.
- **Console.** A daemon thread reading `System.in`; each line becomes a
  `ConsoleInput` in a synchronized list drained by
  `DedicatedServer.handleConsoleInputs` from `DedicatedServer.tickConnection`.
  The command runs on the Server thread.
- **RCON.** `RconThread` (a `GenericThread`) accepts TCP on *rcon.port*
  (25575), one `RconClient` per connection; a command becomes
  `DedicatedServer.runCommand`, which `BlockableEventLoop.executeBlocking`s
  it onto the Server thread with a `RconConsoleSource` that captures the
  output. `RconThread.create` returns nothing — logging that RCON is disabled
  — when *rcon.password* is empty or the port is out of range, so
  *enable-rcon* alone is not enough. `QueryThreadGs4` is the UDP GameSpy4
  status protocol on *query.port*, read-only. Both are **non-daemon** threads
  with a half-second accept timeout so they notice `GenericThread.running`
  going false; that is precisely why `DedicatedServer.onServerExit` has to
  stop them for the JVM to exit at all.
- **JSON-RPC.** New this generation: `server/jsonrpc` — `ManagementServer`
  over WebSocket, TLS by default, a secret in `server.properties`, with
  `JsonRpcNotificationService` pushing the `NotificationManager` events
  (`NotificationManager.serverStarted`, `NotificationManager.serverSaveStarted`, `NotificationManager.serverSaveCompleted`,
  `NotificationManager.playerJoined`…) and `MinecraftApi` exposing the management calls. Ticked
  from `DedicatedServer.tickServer`. The appendix's out-of-scope tour has
  the rest.

## Interfaces

- **Called by:** the JVM (`server/Main`); `StopCommand`; the shutdown hook;
  `ServerWatchdog` (indirectly, by killing the process); the singleplayer
  client through `IntegratedServer.halt` from `Minecraft.disconnect`; the
  singleplayer *owner's* disconnect, through
  `ServerCommonPacketListenerImpl.onDisconnect`; closing the
  `MinecraftServerGui` window; and the JSON-RPC management API, which can
  both save and stop the server.
- **Calls into:** `WorldLoader` / `WorldStem` (Part II), `ServerLevel.save`
  and `ServerChunkCache` / `ChunkMap` / `TicketStorage` (Part IV),
  `PlayerList` (previous page), `SavedDataStorage`, `IOWorker` through the
  chunk storage.
- **Crosses the network as:** nothing of its own — `ServerConnectionListener.stop`
  closes channels without a packet; players are disconnected by
  `PlayerList.removeAll` with a `ClientboundDisconnectPacket` from the
  ordinary disconnect path.
- **Data-driven by:** `server.properties`, `eula.txt`, `level.dat`, the
  command-line options; `ServerLinks` (`ServerLinks.KnownLinkType`) from
  the bug-report property.
- **Reports out as:** a `CrashReport` in *crash-reports/*, named by
  `Util.getFilenameFormattedDateTime`, with a `SystemReport` filled by
  `MinecraftServer.fillSystemReport` and
  `DedicatedServer.fillServerSystemReport` — running state, player count,
  data packs, feature flags, the world seed and the exceptions
  `SuppressedExceptionCollector` gathered from failed packet handlers.
  `CrashReport.preload` runs at the very top of `server/Main` so that even an
  out-of-memory failure can still be written.

## Invariants and surprises

- **Shutdown runs on the Server thread, even after a crash.**
  `MinecraftServer.halt` is nothing but a flag; everything that matters is in
  `MinecraftServer.runServer`'s *finally*, which runs after an exception out
  of the tick loop just as it does after `/stop`. What a hard kill loses is
  the save, not the lock — the OS releases `session.lock` whichever way the
  process dies.
- **`/save-off` is overridden by `/stop`.** `MinecraftServer.stopServer` clears
  `ServerLevel.noSave` on every level before the final save.
- **`Util.shutdownExecutors` kills the JVM-wide pools** inside
  `DedicatedServer.stopServer`, before `DedicatedServer.onServerExit`. Nothing
  may need a worker after that point. It shuts `Util.backgroundExecutor` and
  `Util.ioPool` with a three-second grace each; `Util.nonCriticalIoPool` is
  left alone, surviving only because its threads are daemons. The integrated
  server does not call it at all — `Minecraft` does, at the very end of the
  client's life.
- **The management server outlives the world in both directions** — bound
  in `Main` before `session.lock`, stopped last in
  `DedicatedServer.onServerExit`. (`MinecraftServer.onServerExit` itself is
  empty; everything the phrase describes is the dedicated override.)
- **Startup loads what shutdown deactivated — and there is no spawn ticket.**
  `MinecraftServer.prepareLevels` re-arms the tickets `TicketStorage`
  persisted, and only two ticket types persist at all: `TicketType.FORCED`
  (`/forceload`) and `TicketType.PORTAL`. Nothing keeps the world spawn
  loaded, so on an ordinary world this step loads no chunks whatsoever and
  finishes immediately. `TicketType.PLAYER_SPAWN` and `TicketType.SPAWN_SEARCH`
  are transient, and belong to a player joining, not to boot.
- **The lock is advisory.** `DirectoryLock` is an OS file lock; a crashed
  JVM releases it; copying a world directory copies a meaningless
  `session.lock`.
- **`server.properties` is not read-once.** Around twenty
  `DedicatedServerProperties` fields are `Settings.MutableValue`, and every
  matching `DedicatedServer` setter rewrites the file on disk through
  `DedicatedServerSettings.update` — so `/difficulty`, `/whitelist` and the
  JSON-RPC settings calls all edit the properties file at runtime.
- **Singleplayer's "Saving world" screen is a liveness poll.**
  `Minecraft.disconnect` calls `IntegratedServer.halt` (which first
  disconnects every non-host player) and keeps rendering frames until
  `MinecraftServer.isShutdown` — "is the Server thread dead yet".
- **A dedicated server has no `System.exit` on a clean stop.** The Server
  thread was the only non-daemon thread left once the RCON and query threads
  were stopped, so returning from `MinecraftServer.runServer` is enough.
- **A tick-loop crash saves; a watchdog kill does not.** The two failure
  paths look alike and are not. An exception out of the tick reaches
  `MinecraftServer.runServer`'s catch, writes a crash report and falls into
  the same *finally* `/stop` uses — the world is saved. `ServerWatchdog`
  instead calls `System.exit`, which runs the "Server Shutdown Thread" hook,
  which calls `MinecraftServer.halt` with *wait* true and joins the Server
  thread — the very thread that is wedged in the tick that tripped the
  watchdog. The join blocks, and ten seconds later the watchdog's scheduled
  `Runtime.halt` kills the JVM with nothing written. The watchdog is a
  liveness backstop, not a safe stop.

## Where to look

`server/Main` · `DedicatedServer.initServer` · `DedicatedServer.stopServer` ·
`DedicatedServer.onServerExit` · `MinecraftServer.spin` · `MinecraftServer.runServer` ·
`MinecraftServer.loadLevel` · `MinecraftServer.createLevels` · `MinecraftServer.prepareLevels` ·
`MinecraftServer.saveEverything` · `MinecraftServer.saveAllChunks` ·
`MinecraftServer.stopServer` · `MinecraftServer.halt` ·
`StopCommand` · `LevelStorageSource` · `LevelStorageSource.LevelStorageAccess`
· `DirectoryLock` · `LevelResource` · `WorldLoader` · `WorldStem` ·
`DedicatedServerProperties` · `ServerWatchdog` · `RconThread` ·
`QueryThreadGs4` · `ManagementServer` · `IntegratedServer`

---

*Rules: names, never code · how the system works, not how the code reads ·
newest version only · every backticked name passes `tools/verify_names.py`.*
