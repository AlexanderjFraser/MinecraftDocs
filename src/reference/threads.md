# Threads

> Verified against **Minecraft 26.3** · Reference · Hand-kept from `net/minecraft/util/thread` and every `Thread` the game starts, beside [Anatomy](../systems/anatomy/anatomy.md)'s four — looked up, not watched.

Every thread the game creates, who creates it, what runs on it, and what
is *allowed* to run on it. The last column is the rule the rest of the
documentation leans on: game state belongs to exactly one thread, and anything else hands its work to that thread rather than doing it itself, apart from the unlocked readers and the Netty-side handlers this page names.

## Three ways work crosses a thread boundary

Two threads own game state — the Render thread owns the client's, the
Server thread owns the world's — and everything else is a way of getting
work to them or from them. Work crosses a thread boundary in exactly three
ways, and the figure names which on every edge that is one of them: a **posted task** (a
`Runnable` handed to the executor that will run it — the owner's `BlockableEventLoop`, a worker pool, or the connection's Netty event loop, which is where `Connection.sendPacket` puts a packet sent from any other thread; a console line, left in a list the tick drains, is the same shape), a **completed future** (a
worker's result, completed onto the owner's executor), or a **hopped
handler** (a packet decoded on Netty and re-posted to its owner by
`PacketUtils.ensureRunningOnSameThread`).

```mermaid
flowchart TD
    RT["Render thread: Minecraft.runTick"]:::client
    NET["Netty IO: Connection"]:::netty
    ST["Server thread: MinecraftServer.runServer"]:::server
    WK["Worker-Main-n: Util.backgroundExecutor"]:::worker
    IO["IO-Worker-n: Util.ioPool"]:::worker
    SND["Sound engine: SoundEngineExecutor"]:::client
    LST["console, RCON, management: dedicated only"]:::server
    WD["Server Watchdog, query: dedicated only"]:::server
    RT -- "posted task" --> NET
    ST -- "posted task" --> NET
    NET -- "play packets: hopped" --> RT
    NET -- "play packets: hopped" --> ST
    RT -- "posted task" --> WK
    ST -- "posted task" --> WK
    WK -. "completed future" .-> RT
    WK -. "completed future" .-> ST
    ST -- "posted task" --> IO
    IO -. "completed future" .-> ST
    RT -- "posted task" --> SND
    LST -- "posted task" --> ST
    WD -. "reads, unsynchronised" .-> ST
```

*The threads that carry work, coloured by the side each serves, and every edge between them labelled with how work crosses it: a posted task out, a completed future back, a play packet hopped onto its owner, and the one edge that is none of the three, the watchdog and the query listener reading the Server thread's state without a lock.*

The *daemon* column is the one that decides how the process ends, because a
non-daemon thread holds the JVM open until something stops it. Six rows of
the table are non-daemon; on a dedicated server, which has no Render thread,
that is five, and only four of them can hold it open: **ServerMain**
returns the moment it has registered the shutdown hook, long before anything
needs stopping, which leaves the Server thread, `Util.ioPool`'s workers, and
the RCON and query listeners. The first two are retired
deliberately — the Server thread by returning, the IO pool by
`Util.shutdownExecutors` — and the other two are `GenericThread`s, stopped by clearing `GenericThread.running` and joining: the query listener polls its socket every half second and notices the flag, and `RconThread.stop` closes its socket first, so the RCON accept ends at once. Everything else in the table is a daemon and simply stops existing; *Server Connector*, Swing's event dispatch thread, Realms's threads and the chat filter's workers the Server thread starts, among the situational threads below, are not (a worker a sign or book edit starts from Netty inherits Netty's daemon flag), and nor are the two *java.util.Timer* threads the client's notifications and the watchdog's exit start
([how a server dies](../systems/server/how-a-server-dies.md#the-closes-and-the-last-thread)).

Every box in the figure has a row in the table — the listeners' box has three, the watchdog's two —
and two rows have no box,
because **ServerMain** has stopped existing before any of these edges are busy and
the timer-hack thread does nothing at all. Netty is drawn once and shared because
it is: in singleplayer the client's `Connection` and the integrated
server's run on the same `Netty Local IO` threads, and the packets between
them are real.

## The threads a lecture leans on

| thread | made by | daemon | runs | may touch |
|---|---|---|---|---|
| **Render thread** (client) | the JVM main thread, renamed in `client/main/Main` | no — it *is* main | `Minecraft.run` → `Minecraft.runTick` once per frame; `Minecraft.tick` 0–10 times inside it | Everything client-side: `ClientLevel`, `LocalPlayer`, the GPU (`RenderSystem.assertOnRenderThread`), screens, options. It is also the client's event loop (`Minecraft` is a `ReentrantBlockableEventLoop`), so packet handlers run here after `PacketUtils.ensureRunningOnSameThread`. |
| **ServerMain** (dedicated) | the jar's bundler, which unpacks the libraries on the JVM's main thread and starts this one | no | the whole of boot: the properties, the EULA, the `ManagementServer`, `session.lock`, the `WorldLoader`, then `MinecraftServer.spin`, which constructs the `DedicatedServer` before it starts the Server thread, and finally registering the *Server Shutdown Thread* as a JVM shutdown hook — which is a separate thread and not this one | Everything, until the Server thread exists; after that, nothing ([starting a server](../systems/server/starting-a-server.md#everything-main-does-before-there-is-a-second-thread)) |
| **Server thread** | `MinecraftServer.spin` | no | `MinecraftServer.runServer` → `MinecraftServer.processPacketsAndTick` every `TickRateManager.nanosecondsPerTick` (50 ms by default); `MinecraftServer.waitUntilNextTick` drains the task queue in the slack | Every `ServerLevel`, every chunk, entity and block entity, the `PlayerList`. Serverbound *play* packet handlers run here, all but the ten in the table below and the three they inherit that never hop. One per server; singleplayer has exactly one. |
| **Netty IO** (`Netty NIO IO #n`, `Netty Epoll IO #n`, `Netty Kqueue IO #n`, `Netty Local IO #n`) | `EventLoopGroupHolder` | yes | the `Connection` pipeline: split, decrypt, decompress, decode; encode, compress, encrypt — **and the handshake and login handlers** | Bytes and `Packet` objects — plus, in handshake and login, the handlers themselves: `ServerHandshakePacketListenerImpl` and `ServerLoginPacketListenerImpl` never hop. The login *state machine* is not all theirs, though: `ServerLoginPacketListenerImpl` is a `TickablePacketListener`, so the Server thread advances it once a tick ([protocol phases](../systems/networking/protocol-phases.md#login) walks that state machine) through `MinecraftServer.tickConnection`. A *play* handler that needs game state re-posts to the owning thread. *Local* is the in-process channel of singleplayer. |
| **Worker-Main-n** | `Util.backgroundExecutor` — a `ForkJoinPool` sized to the JDK's available-processor count minus one, clamped by `Util.maxAllowedExecutorThreads` and capped by the *max.bg.threads* property (`Util.getMaxThreads`) | yes | chunk generation and lighting via `ChunkTaskDispatcher`; section meshing via `SectionRenderDispatcher`; resource-reload *prepare* phases; chunk serialisation | Its own inputs, and during generation the chunks its step may write — the one being generated and, while features are placed, its eight neighbours — the generated chunk's first mobs included, which the Server thread builds again from their saved tags when the chunk goes full. Results return to the owning thread as a `CompletableFuture` completed onto that thread's executor, or, for a mesh with geometry, through the upload the Render thread runs — a mesh with nothing to draw the worker installs itself. |
| **IO-Worker-n** | `Util.ioPool` | **no** | region file reads and writes through `IOWorker`, one `PriorityConsecutiveExecutor` per storage so writes to one file stay ordered | Files. `Util.nonCriticalIoPool` (`Download-n`) is a second pool of the same kind, for downloads, profile and account-service lookups, and sound decoding, and the one difference is this column: its threads *are* daemons, so nothing waits for them. |
| **Sound engine** | `SoundEngineExecutor` | yes | a `BlockableEventLoop` that owns the per-source OpenAL calls | The `SoundEngine`'s channels; see [the sound engine](../systems/client/sound-engine.md). Device open/close and the deletion of cached static buffers stay on the Render thread. |
| **Server Watchdog** | `DedicatedServer.initServer` (dedicated only, positive limit only) | yes | `ServerWatchdog` | Writes nothing, but *reads* game state unsynchronised while the Server thread is mid-tick — the game rules and every level's `ServerLevel.getWatchdogStats`, for the crash report. It kills the JVM past `DedicatedServerProperties.maxTickTime`, and with the tick wedged that kill does **not** save the world. |
| **Server console handler** | `DedicatedServer.initServer` | yes | reads stdin | Queues each line to the server thread as a command; runs nothing itself. |
| **RCON Listener #n** / **RCON Client** | `RconThread.create` from `DedicatedServer.initServer`, when *enable-rcon* is on **and** `RconThread.create` gets past its own gates: it returns nothing if *rcon.port* is outside 1–65535, if *rcon.password* is empty, or if the socket cannot be opened | **no** | accepts RCON sockets on a 500 ms timeout, though `RconThread.stop` closes the socket before it joins, so the accept ends at once; one `RconClient` thread per connection, which blocks with no timeout | Sockets. Each command is queued to the server thread. Dedicated only. `DedicatedServer.onServerExit` must stop it or the JVM will not exit ([how a server dies](../systems/server/how-a-server-dies.md#the-closes-and-the-last-thread)). |
| **Query Listener #n** | `QueryThreadGs4.create` from `DedicatedServer.initServer`, when *enable-query* | **no** | the GS4 query protocol, on a 500 ms socket timeout, so it notices `GenericThread.running` going false within half a second | Its full-status reply, rebuilt at most every five seconds from the player count and names it reads off the live `PlayerList` without a lock; the basic reply reads the count afresh on every request. Dedicated only, and stopped by the same call as RCON. |
| **Management server IO #n** | `ManagementServer`, built by `JsonRpc` in `server/Main` | yes | a second, independent Netty event-loop group: the JSON-RPC/WebSocket management API and its heartbeat | Its own pipeline; management calls reach the game through the server's task queue. Dedicated only. |
| Timer hack thread | `Util.startTimerHackThread` | yes | sleeps forever | Nothing. Keeps the JVM's timer resolution high by existing. |

## The handlers that never hop

`Connection.channelRead0` calls a packet's handler on the Netty thread, and
a handler's first line is normally `PacketUtils.ensureRunningOnSameThread`,
which re-posts it to the owning thread and aborts
([the connection](../systems/networking/the-connection.md#one-packet-there-and-one-back)). The client's play listener has nine handlers that omit it, two of them inherited; the server's declares ten, and inherits three more that never hop (the keep-alive, the pong and the cookie response). They differ in kind: most of the client's run to completion on Netty, and six of the server's ten use the Netty thread only to hand the work somewhere else.

Nine on the client, then. Seven are declared in
`ClientPacketListener` itself; the last two are inherited from
`ClientCommonPacketListenerImpl` and are the two that matter most, because a keep-alive is answered, and a disconnect's channel closed, from the Netty thread. Three rows reach the Render thread after all: the low-disk warning by a posted task, a keep-alive deferred to its next tick, and a disconnect, whose `Connection.handleDisconnection` that thread's tick runs.

| handler | what it does on the Netty thread |
|---|---|
| `ClientPacketListener.handlePlayerCombatEnter` | nothing — the body is empty |
| `ClientPacketListener.handlePlayerCombatEnd` | nothing — the body is empty |
| `ClientPacketListener.handleChunkBatchStart` | starts the `ChunkBatchSizeCalculator`'s clock |
| `ClientPacketListener.handleChunkBatchFinished` | stops it and sends `ServerboundChunkBatchReceivedPacket` with the chunks-per-tick it now wants — so the loop in [what the client is told](../systems/networking/what-the-client-is-told.md) times the batch's arrival and decode on Netty, not mesh building |
| `ClientPacketListener.handleDebugSample` | hands the sample to `DebugScreenOverlay.logRemoteSample` |
| `ClientPacketListener.handlePongResponse` | records the round trip in `PingDebugMonitor` |
| `ClientPacketListener.handleLowDiskSpaceWarning` | calls `Minecraft.sendLowDiskSpaceWarning`, which posts the toast to the Render thread itself — one of the three that cross after all, by `Minecraft.execute` rather than by the hop |
| `ClientCommonPacketListenerImpl.handleKeepAlive` | replies with `ServerboundKeepAlivePacket` through `ClientCommonPacketListenerImpl.sendWhen`, deferred while the window is frozen at `RenderSystem.isFrozenAtPollEvents` — so the answer goes at once from the Netty thread unless the Render thread is stuck in the poll, and then waits for its next tick |
| `ClientCommonPacketListenerImpl.handleDisconnect` | calls `Connection.disconnect` straight from the event loop, which closes the channel; the Render thread's next tick finds it closed and runs `Connection.handleDisconnection` |

Ten on the server, out of `ServerGamePacketListenerImpl`'s sixty-one game
handlers — the other fifty-one open on the hop
([the server tick](../systems/server/server-tick.md#every-packet-since-last-time-in-one-drain)
has what that costs the tick). They fall into four kinds: two that touch nothing, four that post a
task, two that wait on a future, and two that write listener state on Netty
because nothing else can be asked to.

| handler | what it does on the Netty thread |
|---|---|
| `ServerGamePacketListenerImpl.handlePingRequest` | sends `ClientboundPongResponsePacket` back with the time it arrived, and nothing else |
| `ServerGamePacketListenerImpl.handleCustomPayload` | nothing — the body is empty |
| `ServerGamePacketListenerImpl.handleChat` | advances the acknowledgement window under the `LastSeenMessagesValidator`'s lock, then `ServerGamePacketListenerImpl.tryHandleChat`: illegal characters disconnect, a hidden chat visibility answers with a system message, and everything else resets the last-action time and posts the work through `MinecraftServer.execute` |
| `ServerGamePacketListenerImpl.handleChatCommand` | the same door without a signature — `ServerGamePacketListenerImpl.tryHandleChat` posts the parse and the run |
| `ServerGamePacketListenerImpl.handleSignedChatCommand` | the same, the signed arguments collected inside the posted task |
| `ServerGamePacketListenerImpl.handleCustomCommandSuggestions` | hands the request to the player's `ServerCommandSuggestionsProvider`, which keeps only the latest and answers at most one a tick, posting the work through `MinecraftServer.execute` or leaving it for the listener's own tick |
| `ServerGamePacketListenerImpl.handleSignUpdate` | strips formatting and sends the four lines to the text filter; the result comes back on the server's own executor |
| `ServerGamePacketListenerImpl.handleEditBook` | the same shape for a book's title and pages, and the same hand-back |
| `ServerGamePacketListenerImpl.handleChatAck` | applies the offset to `LastSeenMessagesValidator` under a lock, and disconnects the player if it does not validate — real listener state, written off the main thread |
| `ServerGamePacketListenerImpl.handleConfigurationAcknowledged` | swaps the inbound protocol and installs a `ServerConfigurationPacketListenerImpl`, so the return to configuration begins on the network thread ([protocol phases](../systems/networking/protocol-phases.md#configuration)) |

## Situational threads

Real, but nothing in the corpus hangs on them: *User Authenticator* (one per login that asks the session server), *Chat-Filter-Worker*, *Server Pinger* and
*Server Connector* (the multiplayer screen), *Telemetry-Sender*,
`LanServerPinger` and its detector, *World Upgrader*, *Datafixer Bootstrap*
(priority 1, so it yields to everything), the client and server shutdown hooks, `ClientShutdownWatchdog` once the client is closing, Swing's event dispatch
thread when a dedicated server is started without *--nogui* and runs its
`MinecraftServerGui` and its *Server log monitor*, *Latency Simulator #n* behind a debug latency flag, the *Friends List* fetcher the client starts when its friend list is on,
and `ChaseServer`'s two threads and `ChaseClient`'s one, which exist only
behind `SharedConstants.DEBUG_CHASE_COMMAND` and the */chase* command it
registers. Realms starts eight more — seven in *com/mojang/realmsclient* and `RealmsConnect`'s connect task — and is out of scope with the rest of
*com/mojang/realmsclient*.

## The rule the last column is stating

Two threads own game state and everything else is a way of getting work to
them: client state is the Render thread's, server state is the Server thread's,
and in singleplayer they share a JVM and still talk about the *world* only
through packets over the local channel
([anatomy](../systems/anatomy/anatomy.md#four-threads-worth-memorising) has
the four to memorise, and the settings that do cross by direct call). Three
consequences run through the table and each is owned by a lecture, not here: a
play packet is decoded on Netty and *handled* on its owner's thread
([the connection](../systems/networking/the-connection.md#one-packet-there-and-one-back));
workers compute and owners commit, so a generated chunk is installed by the thread that owns it, never by the pool
([the level tick](../systems/server/server-level-tick.md#the-chunk-source-does-five-things-in-one-call));
and an owning thread waiting on a future keeps draining its own queue through
`BlockableEventLoop.managedBlock`, which is why a tick that waits for a chunk
does not deadlock the chunk that needs the tick
([the server tick](../systems/server/server-tick.md#the-event-loop-and-what-a-ticks-spare-time-buys)).

## Where to look

`Util.backgroundExecutor` · `Util.ioPool` · `Util.startTimerHackThread` ·
`MinecraftServer.spin` · `EventLoopGroupHolder` · `GenericThread` ·
`SoundEngineExecutor` · `ServerWatchdog` ·
`PacketUtils.ensureRunningOnSameThread` · `BlockableEventLoop.managedBlock`

---

*Rules: names, never code · how the system works, not how the code reads ·
newest version only · every backticked name passes `tools/verify_names.py`.*
