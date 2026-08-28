# Threads

> Verified against **Minecraft 26.2** · Hand-written from [Anatomy](../systems/anatomy/anatomy.md); the one reference page that is not generated.

Every thread the game creates, who creates it, what runs on it, and what
is *allowed* to run on it. The last column is the rule the rest of the
documentation leans on: game state belongs to exactly one thread, and
anything else submits a task to that thread's event loop.

| thread | made by | runs | may touch |
|---|---|---|---|
| **Render thread** (client) | the JVM main thread, renamed in `client/main/Main` | `Minecraft.run` → `Minecraft.runTick` once per frame; `Minecraft.tick` 0–10 times inside it | Everything client-side: `ClientLevel`, `LocalPlayer`, the GPU (`RenderSystem.assertOnRenderThread`), screens, options. It is also the client's event loop (`Minecraft` is a `ReentrantBlockableEventLoop`), so packet handlers run here after `PacketUtils.ensureRunningOnSameThread`. |
| **Server thread** | `MinecraftServer.spin` | `MinecraftServer.runServer` → `MinecraftServer.tickServer` every 50 ms; `MinecraftServer.waitUntilNextTick` drains the task queue in the slack | Every `ServerLevel`, every chunk, entity and block entity, the `PlayerList`. Serverbound packet handlers run here, not on Netty. One per server; singleplayer has exactly one. |
| **Netty IO** (`Netty NIO IO #n`, `Netty Epoll IO #n`, `Netty Local IO #n`) | `EventLoopGroupHolder` | the `Connection` pipeline: split, decrypt, decompress, decode; encode, compress, encrypt | Bytes and `Packet` objects only. A handler that needs game state re-posts to the owning thread. *Local* is the in-process channel of singleplayer. |
| **Worker-Main-n** | `Util.backgroundExecutor` — a `ForkJoinPool` sized to the core count | chunk generation and lighting via `ChunkTaskDispatcher`; section meshing via `SectionRenderDispatcher`; resource-reload *prepare* phases; chunk serialisation | Its own inputs. Results return to the owning thread as a `CompletableFuture` completed onto that thread's executor. Never `Level` state directly. |
| **IO-Worker-n** | `Util.ioPool` | region file reads and writes through `IOWorker`, one `PriorityConsecutiveExecutor` per storage so writes to one file stay ordered | Files. `Util.nonCriticalIoPool` is the same shape for downloads and telemetry. |
| **Sound engine** | `SoundEngineExecutor` | a `BlockableEventLoop` that owns OpenAL | The `SoundEngine` and its `Library`; see [Sound](../systems/client/sound.md). |
| **Server Watchdog** | `DedicatedServer.initServer` (dedicated only) | `ServerWatchdog` | Nothing; it reads the tick timestamp and kills the JVM after `DedicatedServerProperties.maxTickTime`. |
| **Server console handler** | `DedicatedServer.initServer` | reads stdin | Queues each line to the server thread as a command; runs nothing itself. |
| Timer hack thread | `Util.startTimerHackThread` | sleeps forever | Nothing. Keeps the JVM's timer resolution high by existing. |

## The rules that follow

- **Two owners, one wire.** Client state is the Render thread's; server state
  is the Server thread's; in singleplayer they share a JVM and still only
  talk through packets over the local channel.
- **Handlers hop.** A packet is decoded on Netty and *handled* on the owning
  game thread; `PacketUtils.ensureRunningOnSameThread` is the hop.
- **Workers compute, owners commit.** Chunk generation, lighting and meshing
  produce results on the worker pool; only the owning thread installs them.
- **Waiting drains.** An owning thread never blocks idle: `BlockableEventLoop.managedBlock`
  keeps running its own queue while it waits on a future, which is why a
  server tick that waits for a chunk does not deadlock the chunk that needs
  the server tick.
