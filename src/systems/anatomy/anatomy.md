# Anatomy

> Verified against **Minecraft 26.2** · Part I · From `main()` to a running singleplayer world: which threads exist, which loop each one runs, and how the two halves of the game talk.

## Responsibility

Java Minecraft is one codebase that runs as two programs. The **client** is a
window, a frame loop and a copy of the world it is told about. The **server**
is the world itself: a 20 Hz tick loop that owns every chunk, entity and block
and is the only thing allowed to change them. In singleplayer both run in the
same JVM, on different threads, and talk to each other through a real Netty
connection that never touches a socket. A dedicated server is the same server
class with the client half absent.

The one sentence a player recognises: *the server is the game; the client is
a view of it.*

## The data it owns

- `Minecraft` (client, one instance, `Minecraft.getInstance`) owns the window
  (`Window`), the resource system (`ReloadableResourceManager` and every
  manager registered on it — `TextureManager`, `ShaderManager`, `ModelManager`,
  `AtlasManager`, `FontManager`, `SoundManager`), the renderers (`GameRenderer`,
  `LevelRenderer`, `EntityRenderDispatcher`, `BlockEntityRenderDispatcher`,
  `ParticleEngine`), input (`MouseHandler`, `KeyboardHandler`), the HUD (`Gui`)
  and `Options`. Three fields are nullable and define "are we in a world":
  `Minecraft.level` (a `ClientLevel`), `Minecraft.player` (a `LocalPlayer`) and
  `Minecraft.gameMode` (a `MultiPlayerGameMode`). A fourth,
  `Minecraft.singleplayerServer`, is the `IntegratedServer` when one is running.
- `MinecraftServer` (abstract; `IntegratedServer` and `DedicatedServer` are the
  two concrete kinds) owns the levels (`ServerLevel`, one per dimension), the
  `PlayerList`, the `ServerConnectionListener`, the `ServerFunctionManager`, the
  `ServerTickRateManager` and a `PacketProcessor`.
- Nothing on the client writes server state and nothing on the server writes
  client state, ever, even in singleplayer. Everything crosses as a packet.

## When it runs

There are two loops and they are not the same shape.

**The client loop** runs on the *Render thread* — the JVM main thread, renamed
in `Main` before `Minecraft` is constructed, and the thread `RenderSystem`
guards with `RenderSystem.assertOnRenderThread`. `Minecraft.run` loops on
`Minecraft.runTick` once per **frame**, as fast as vsync or the frame-rate
limit allow. Inside each frame a `DeltaTracker.Timer` (20 ticks per second)
says how many whole game ticks have elapsed since the last frame — usually 0
or 1, at most 10 are run — and `Minecraft.tick` is called that many times.
The fractional remainder is `partialTick`, which the renderers use to
interpolate between the last two tick states. So the client *has* a 20 Hz
tick, but it is a sub-step of the frame loop, not a loop of its own.

**The server loop** runs on the *Server thread*, created by
`MinecraftServer.spin`. `MinecraftServer.runServer` loops on
`MinecraftServer.tickServer` at a fixed 50 ms cadence tracked in nanoseconds:
after each tick it calls `MinecraftServer.waitUntilNextTick`, which spends the
slack running queued tasks and then blocks until the next tick is due. If a
tick overruns, the next one starts immediately; if the server falls more than
two seconds (one second plus 20 ticks) behind it logs *Can't keep up!* and skips ahead rather than
trying to catch up. There is no frame and no `partialTick` on the server.

Both loops are **event loops** first and game loops second. `MinecraftServer`
extends `ReentrantBlockableEventLoop`, and `Minecraft` embeds the same idea:
each is an `Executor` whose queue drains on its own thread, so any other thread
that wants to touch game state submits a task and waits. The blocking form,
`BlockableEventLoop.managedBlock`, is how the owning thread waits for a
future without deadlocking — it keeps draining its own queue while it waits.

## The threads

| Thread | Made by | Runs | Notes |
|---|---|---|---|
| **Render thread** | JVM main, renamed in `client/main/Main` | `Minecraft.run` | Also the client "game thread": `Minecraft.gameThread` is this thread. Priority 10 on machines with more than 4 cores. |
| **Server thread** | `MinecraftServer.spin` | `MinecraftServer.runServer` | One per server, so singleplayer has exactly one. Priority 8. |
| **Netty IO** | `EventLoopGroupHolder` | the Netty pipeline | Named "Netty NIO IO #n" (or Epoll/Kqueue when native transport is on); "Netty Local IO #n" for the in-process singleplayer channel. Decode, encrypt, compress; never game logic. |
| **Worker-Main-n** | `Util.backgroundExecutor` | a `ForkJoinPool` sized to the core count | The shared CPU pool. Chunk generation and lighting (`ChunkMap` through `ChunkTaskDispatcher`), section meshing (`SectionRenderDispatcher`), resource reloads, chunk serialisation all run here. |
| **IO-Worker-n** | `Util.ioPool` | region-file reads and writes | Fed through `IOWorker`, one `PriorityConsecutiveExecutor` per storage kind so writes to one file stay ordered. `Util.nonCriticalIoPool` is the same idea for downloads. |
| **Sound engine** | `SoundEngineExecutor` | a `BlockableEventLoop` for OpenAL | The client's third event loop. |
| **Server Watchdog** | `DedicatedServer.initServer` | `ServerWatchdog` | Dedicated only. Kills the JVM if a tick exceeds `DedicatedServerProperties.maxTickTime` (default one minute). |
| **Server console handler** | `DedicatedServer.initServer` | reads stdin | Commands typed at the console are queued to the server thread, not run on this one. |
| Timer hack thread | `Util.startTimerHackThread` | sleeps forever | A daemon thread that does nothing but sleep — the long-standing workaround for keeping the JVM's timer resolution high while a sleeping thread exists. Both `Main` classes start it. |

Everything else that matters is *serialised onto* one of these. The two
`ConsecutiveExecutor` classes in `util/thread` are the mechanism: a queue that
promises to run its tasks one at a time on a pool that otherwise runs many —
which is how "worldgen", "light" and the IO workers stay ordered without
owning a thread.

## The trace: launching the game and opening a singleplayer world

```mermaid
sequenceDiagram
    participant Main as Main (client/main)
    participant MC as Minecraft
    participant RS as RenderSystem
    participant IS as IntegratedServer
    participant MS as MinecraftServer
    participant SCL as ServerConnectionListener
    participant C as Connection

    Main->>Main: tryDetectVersion, loadLibraries, Bootstrap.bootStrap — registries frozen before anything else exists
    Main->>RS: initRenderThread — this thread is now the Render thread
    Main->>MC: new Minecraft(GameConfig) — pick a GpuBackend, open the Window, register every reload listener, start the first resource reload
    Main->>MC: run — the frame loop; never returns until quit
    loop every frame
        MC->>MC: runTick — drain PacketProcessor, then 0..n × tick, then render with partialTick
    end
    MC->>MS: doWorldLoad → spin(IntegratedServer) — the Server thread is born here
    MS->>IS: runServer → initServer → loadLevel, prepareLevels
    MC->>SCL: startMemoryChannel — a Netty LocalServerChannel, no socket
    MC->>C: connectToLocalServer — the client's side of the same channel
    C->>SCL: handshake → login → configuration → play, as packets
    loop every 50 ms on the Server thread
        MS->>MS: tickServer — packets, then tickChildren (each ServerLevel.tick), then tickConnection
        MS->>MS: waitUntilNextTick — run queued tasks, sleep the remainder
    end
    Note over MC,IS: IntegratedServer.tickServer pauses the world when Minecraft.isPaused and nobody else is connected
```

Narrated:

1. **Bootstrap before anything.** `SharedConstants.tryDetectVersion` reads
   `version.json`; `Bootstrap.bootStrap` builds and freezes the static
   registries (blocks, items, entity types — the things that cannot be
   data-driven because the data loader itself needs them); `ClientBootstrap`
   does the client-only equivalents. Both `Main` classes do this first, which
   is why nothing in `world/` can be touched from a static initialiser.
2. **The GPU backend is chosen in the constructor.** `PreferredGraphicsApi`
   from `Options` decides the order `PreferredGraphicsApi.getBackendsToTry`
   returns: OpenGL first by default, Vulkan first only if the player opts in;
   the first `GpuBackend` (`GlBackend` or `VulkanBackend`) that can create a
   `Window` wins, and from then on the renderer only ever sees the `GpuDevice`
   abstraction in `com/mojang/blaze3d`.
3. **Construction registers, it does not load.** The constructor creates each
   manager and registers it on the `ReloadableResourceManager`; the actual
   loading is one `ReloadInstance` run on `Util.backgroundExecutor` with the
   `LoadingOverlay` on screen. Resource reloads (F3+T) are the same path
   re-run.
4. **`Minecraft.run` is the frame loop.** `Minecraft.runTick` polls GLFW events, drains
   the `PacketProcessor`, advances the `DeltaTracker`, runs the tick(s), and
   renders. Every frame does all of these; a tick is merely a thing that
   happens in some frames.
5. **Opening a world spins a server.** `Minecraft.doWorldLoad` calls
   `MinecraftServer.spin`, which creates the Server thread and constructs the
   `IntegratedServer` *on the caller's thread* handing it the new thread
   object; the thread then runs `MinecraftServer.runServer`, which calls
   `IntegratedServer.initServer` and enters the loop.
6. **The client connects like any other client.**
   `ServerConnectionListener.startMemoryChannel` binds a Netty `LocalAddress`;
   `Connection.connectToLocalServer` connects to it; the client then walks the
   same handshake → login → configuration → play state machine it would with a
   remote server, via `ClientHandshakePacketListenerImpl`. Nothing in the play
   path knows it is singleplayer.
7. **Pause is a server decision.** `IntegratedServer.tickServer` checks
   `Minecraft.isPaused` and whether other players are connected; when paused it
   runs `IntegratedServer.tickPaused` — connections only, no world tick — and
   saves once on the transition. A published LAN world therefore never pauses.

## Interfaces

- **Called by:** the JVM. `client/main/Main` for the client, `server/Main` for the
  dedicated server; the data generator has a third `Main`
  under `client/data`.
- **Calls into:** everything; this page is the frame the rest hang on. The
  first lane of every later diagram is one of the thread names above.
- **Crosses the network as:** nothing of its own — but the *thread crossing*
  for packets is defined here and every networking page relies on it. A packet
  arrives on a Netty IO thread and `Connection.channelRead0` hands it to the
  current `PacketListener`; handlers that touch game state call
  `PacketUtils.ensureRunningOnSameThread`, which, when off-thread, queues the
  packet on the owning side's `PacketProcessor` and aborts the handler with
  `RunningOnDifferentThreadException`. The queue is drained at the top of the
  next tick (`PacketProcessor.processQueuedPackets`, first thing in both
  `Minecraft.runTick` and `MinecraftServer.processPacketsAndTick`). Sending is
  the reverse: `Connection.send` writes to the channel from any thread and
  Netty flushes on its own.
- **Data-driven by:** `version.json` (`SharedConstants`), `options.txt`
  (`Options`), `server.properties` (`DedicatedServerProperties`).

## Invariants and surprises

- **The Render thread *is* the game thread.** There is no separate client
  logic thread; `Minecraft.gameThread` and the thread `RenderSystem` asserts
  on are the same one. A slow client tick costs frames directly.
- **The server never renders and the client never simulates authoritatively.**
  `ClientLevel` does tick entities and block entities (`Minecraft.tick` calls
  `ClientLevel.tickEntities`) but only to predict and animate; the server's
  packets overwrite whatever the prediction got wrong.
- **Singleplayer is multiplayer with a loopback.** `IntegratedServer` is a
  `MinecraftServer`; the connection is a Netty `LocalChannel`; the packets are
  real. The only singleplayer special cases are pausing and the view/simulation
  distance following `Options`.
- **One worker pool, many queues.** `Util.backgroundExecutor` is a single
  `ForkJoinPool`; the ordering guarantees the game needs (worldgen steps in
  order, light before mesh, one writer per region file) come from
  `ConsecutiveExecutor` and `PriorityConsecutiveExecutor` layered on top,
  never from dedicated threads.
- **`MinecraftServer.haveTime` is the budget.** `MinecraftServer.tickServer` receives a
  `BooleanSupplier` (`MinecraftServer.haveTime`) and passes it down to
  `ServerLevel.tick`; chunk loading and other deferrable work check it and
  stop when the 50 ms are spent. While sprinting (`/tick sprint`) the supplier
  is always false, so nothing deferrable runs and ticks go as fast as they can.
- **The tick rate is a server field, not a constant.** `ServerTickRateManager`
  (shared base `TickRateManager`) owns the nanoseconds-per-tick, freeze and
  sprint state that `/tick` manipulates; the client mirrors it in
  `ClientLevel` so `DeltaTracker` can freeze too.
- **Crashes are collected, not thrown.** Both loops catch everything, wrap it
  in a `CrashReport`, and on the client try an emergency save first; a
  background thread that dies reports through `BlockableEventLoop.delayCrash`
  so the crash surfaces on the owning thread.

## Where to look

`client/main/Main` · `Minecraft` · `DeltaTracker` · `MinecraftServer` ·
`IntegratedServer` · `server/Main` · `DedicatedServer` ·
`BlockableEventLoop` · `Util` (the executors) · `PacketProcessor` ·
`PacketUtils` · `EventLoopGroupHolder` · `ServerConnectionListener` ·
`Connection` · `PreferredGraphicsApi` · `GpuBackend`
