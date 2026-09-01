# The server tick

> Verified against **Minecraft 26.2** · Part III · One 50 ms tick on the Server thread: from the moment the clock says "now" to the moment the thread parks again.

## Responsibility

The server tick is the heartbeat every other server-side page lives inside.
Twenty times a second `MinecraftServer` drains the packets that arrived since
last time, advances every `ServerLevel` by one step, flushes what each player
needs to be told, and then spends whatever is left of the 50 ms running
deferred work before parking until the next beat. Everything the server owns
— chunks, entities, block ticks, player sessions — is *committed* from inside
this loop, on this thread. Plenty is computed elsewhere: chunk generation,
lighting and IO all run on pools and post their results back here.

The one sentence a player recognises: *TPS is how many of these the server
finishes per second, and "Can't keep up!" is the server giving up on the
ones it missed.*

## The data it owns

- `MinecraftServer` is the loop, the thread and the event loop in one object:
  it extends `ReentrantBlockableEventLoop` (of `TickTask`), and
  `MinecraftServer.spin` creates the *Server thread* whose body is
  `MinecraftServer.runServer`. Its scheduling state is a handful of fields:
  `MinecraftServer.tickCount` (the tick number, stamped onto every queued
  task), `MinecraftServer.nextTickTimeNanos` (the deadline the loop is
  chasing), `MinecraftServer.delayedTasksMaxNextTickTimeNanos` and
  `MinecraftServer.mayHaveDelayedTasks` (how late deferrable work may run),
  `MinecraftServer.ticksUntilAutosave`, and the tick-time ledger:
  `MinecraftServer.tickTimesNanos` (a 100-slot ring),
  `MinecraftServer.aggregatedTickTimesNanos` (their sum) and
  `MinecraftServer.smoothedTickTimeMillis` (an exponential average,
  `MinecraftServer.AVERAGE_TICK_TIME_SMOOTHING` = 0.8). This ledger is what
  `/tick query` reads, through `MinecraftServer.getAverageTickTimeNanos` and
  `MinecraftServer.getTickTimesNanos`; the debug screen's TPS chart is fed by
  a *different* pipe — the `SampleLogger` stream in step 8.
- `TickTask` — a `Runnable` plus the `MinecraftServer.tickCount` it was
  submitted on. *Every* runnable handed to the server becomes one through
  `MinecraftServer.wrapRunnable`, whichever thread submits it;
  `MinecraftServer.shouldRun` lets a task run when there is spare time *or*
  when it is more than three ticks old (`MinecraftServer.MAX_TICK_LATENCY`)
  — so a saturated server still drains its queue, just late. Submitting from
  the Server thread does not mean running inline:
  `ReentrantBlockableEventLoop.scheduleExecutables` returns true while
  another task is already running, so re-entrant work queues instead of
  nesting. Once the server is stopping, `MinecraftServer.scheduleExecutables`
  rejects new work with a *RejectedExecutionException*.
- `ServerTickRateManager` (extends the shared `TickRateManager`, which the
  client also has inside `ClientLevel`) owns the tick *rate*:
  `TickRateManager.nanosecondsPerTick`, `TickRateManager.isFrozen`,
  `TickRateManager.frozenTicksToRun` (for `/tick step`) and the sprint
  bookkeeping (`ServerTickRateManager.remainingSprintTicks`,
  `ServerTickRateManager.sprintTickStartTime`,
  `ServerTickRateManager.sprintTimeSpend`,
  `ServerTickRateManager.previousIsFrozen`, and
  `ServerTickRateManager.scheduledCurrentSprintTicks` — that last one is what
  `ServerTickRateManager.isSprinting` actually tests). The rate is bounded:
  `TickRateManager.MIN_TICKRATE` is 1.0 and `TickCommand.MAX_TICKRATE` is
  10000. The one bit the rest of the server reads is
  `TickRateManager.runsNormally`: "should game elements advance this tick".
- `PacketProcessor` — a `ConcurrentLinkedQueue` of listener/packet pairs
  (`PacketProcessor.ListenerAndPacket`) that Netty threads fill and the
  Server thread empties. There is one per server
  (`MinecraftServer.packetProcessor`) and one per client
  (`Minecraft.packetProcessor`).
- `ServerClockManager` — world time is a set of clocks stored as saved
  data, ticked from the server, not from the level, and gated on the
  `GameRules.ADVANCE_TIME` rule.
- `MinecraftServer.scheduledEvents` — a `TimerQueue` of `/schedule` entries.
  The server owns it and persists it, but it is ticked from inside
  `ServerLevel.tickTime`, not from here.

## When it runs

On the *Server thread*, always. The loop is `MinecraftServer.runServer`; a
single iteration is one tick plus the wait for the next. The subtlety is
that the thread never idles: the "wait" is `MinecraftServer.waitUntilNextTick`,
which runs `BlockableEventLoop.runAllTasks` and then
`BlockableEventLoop.managedBlock` on the condition "no time left", and
`BlockableEventLoop.managedBlock` keeps polling the task queue while it waits. The chunk
system's main-thread queue (`ServerChunkCache.MainThreadExecutor`, one per
level) is drained from the same place: `MinecraftServer.pollTaskInternal`
polls the server's own queue first and then every level's chunk source when
there is time, is sprinting, or is blocked. So chunk-load results, lighting
results and anything a worker thread posted back land on the Server thread
either during the tick (when a level blocks on a chunk) or in the slack
after it.

The budget is a `BooleanSupplier`, `MinecraftServer.haveTime`, passed down
to `MinecraftServer.tickServer` and from there into every `ServerLevel.tick`.
It is not quite "is now still before the deadline": it is true unconditionally
*while a task is running* (`ReentrantBlockableEventLoop.runningTask`), and only
otherwise compares the clock against
`MinecraftServer.delayedTasksMaxNextTickTimeNanos` or
`MinecraftServer.nextTickTimeNanos`. While sprinting, the supplier
`MinecraftServer.processPacketsAndTick` hands to
`MinecraftServer.tickServer` is a constant false instead, so deferrable work
is skipped and ticks run back to back.

The budget also stops applying the moment the thread *blocks*. Inside
`BlockableEventLoop.managedBlock` the blocking depth is non-zero, so
`BlockableEventLoop.shouldRunAllTasks` is true and
`BlockableEventLoop.pollTask` skips `MinecraftServer.shouldRun` altogether:
every queued task runs, budget and age irrelevant. That is what lets a level
block on a chunk mid-tick without deadlocking — the wait *is* the drain.

## The trace: one 50 ms tick

```mermaid
sequenceDiagram
    participant ST as Server thread (runServer)
    participant TRM as ServerTickRateManager
    participant PP as PacketProcessor
    participant MS as MinecraftServer
    participant SL as ServerLevel (each)
    participant SCL as ServerConnectionListener
    participant PL as PlayerList
    participant EL as BlockableEventLoop (self)

    alt sprinting (checkShouldSprintThisTick)
        ST->>TRM: this tick is 0 ns long; nextTickTimeNanos = now
    else normal
        ST->>ST: more than 1 s + 20 ticks behind AND not warned recently? log "Can't keep up!", skip nextTickTimeNanos forward
    end
    ST->>ST: nextTickTimeNanos += nanosecondsPerTick
    ST->>MS: processPacketsAndTick — the Tracy frame opens here
    MS->>PP: processQueuedPackets — every serverbound packet since last tick, handled now
    MS->>MS: tickServer(haveTime)
    MS->>MS: empty for pause-when-empty-seconds? tickConnection only, return
    MS->>MS: ++tickCount
    MS->>TRM: tick — decide runsNormally, consume one /tick step
    MS->>MS: tickChildren
    MS->>MS: suspendFlushing on every player connection
    MS->>MS: ServerFunctionManager.tick (#load once, then #tick) · ServerClockManager.tick
    MS->>MS: forceGameTimeSynchronization every 20 ticks · updateEffectiveRespawnData
    loop each ServerLevel, overworld first
        MS->>SL: tick(haveTime) — see server-level-tick
    end
    MS->>SCL: tick — Connection.tick per client: flush, keep-alive, ServerGamePacketListenerImpl.tick (the player's own tick)
    MS->>PL: tick — latency broadcast every 600 ticks, nothing else
    MS->>MS: debugSubscribers, GameTestTicker, tickables, then PlayerChunkSender.sendNextChunks + resumeFlushing per player
    MS->>MS: serverActivityMonitor.tick — the last statement of tickChildren
    MS->>MS: rebuild ServerStatus if 5 s old · --ticksUntilAutosave, autoSave at 0 · record tick time
    ST->>ST: mayHaveDelayedTasks = true; delayedTasksMaxNextTickTimeNanos = the slack deadline
    ST->>EL: waitUntilNextTick — runAllTasks, then managedBlock until nextTickTimeNanos (parks in waitForTasks)
    ST->>TRM: endTickWork if sprinting
    ST->>ST: logFullTickTime — measures the whole iteration, tick plus wait; isReady = true
```

Narrated:

1. **The deadline moves first, then the work starts.** `MinecraftServer.runServer` computes
   this tick's length from `ServerTickRateManager` — 50 ms at the default
   rate, zero while sprinting — and adds it to `MinecraftServer.nextTickTimeNanos` *before*
   ticking. Being "behind" means the wall clock has passed that deadline. If
   it has passed by more than one second plus twenty ticks' worth
   (`MinecraftServer.OVERLOADED_THRESHOLD_NANOS` and
   `MinecraftServer.OVERLOADED_TICKS_THRESHOLD`) **and** it has not warned
   within the last ten seconds plus a hundred ticks
   (`MinecraftServer.OVERLOADED_WARNING_INTERVAL_NANOS`), the loop logs the
   overload warning and **advances the deadline past the backlog**. Both
   effects live in the same condition, so a server that warned recently stays
   behind rather than skipping. When it does skip, the missed ticks are gone.
   Sprinting takes the other branch of that same *if* entirely — no overload
   check happens while `ServerTickRateManager.checkShouldSprintThisTick` is
   answering yes.
2. **Packets, all of them, before anything else.** `MinecraftServer.processPacketsAndTick`
   calls `PacketProcessor.processQueuedPackets`. A serverbound packet was
   decoded on a Netty thread and its handler called
   `PacketUtils.ensureRunningOnSameThread`, which queued it here and aborted
   the Netty-side handler by throwing `RunningOnDifferentThreadException`
   ([Anatomy](../anatomy/anatomy.md) has the crossing). Each queued pair is
   re-checked with `PacketListener.shouldHandleMessage` — a player who
   disconnected between arrival and handling is dropped here — and then
   handled. This is the only point in the tick where player input enters.
   A handler that throws does **not** end the tick: `ServerPacketListener`'s
   default `PacketListener.onPacketError` logs and suppresses it, and
   `ServerCommonPacketListenerImpl.onPacketError` additionally files it
   through `MinecraftServer.reportPacketHandlingException` so it appears in
   the next crash report. The one exception is an out-of-memory error, which
   `PacketUtils.makeReportedException` rethrows.
3. **An empty dedicated server does not tick.** `MinecraftServer.tickServer`
   first asks `MinecraftServer.pauseWhenEmptySeconds` (the
   `DedicatedServerProperties` value, default 60; zero on the base class):
   once `MinecraftServer.emptyTicks` reaches it the server autosaves once,
   then runs only `MinecraftServer.tickConnection` and returns without
   incrementing `MinecraftServer.tickCount`. The integrated server has its own version:
   `IntegratedServer.tickServer` sets `IntegratedServer.paused` from
   `Minecraft.isPaused` and the player count, saves on the transition, and
   runs `IntegratedServer.tickPaused` instead.
4. **The rate manager decides what "runs" this tick.** `TickRateManager.tick`
   computes `TickRateManager.runGameElements` — true unless frozen, or frozen with steps left
   from `/tick step` — and decrements the step counter. `MinecraftServer.tickCount` still
   increments while frozen; freezing gates content, not the loop.
5. **`MinecraftServer.tickChildren` is the tick.** In order, each under its own profiler
   section: every player's connection has flushing suspended
   (`ServerCommonPacketListenerImpl.suspendFlushing`); data-pack functions
   (`ServerFunctionManager.tick` runs `#minecraft:load` once after a reload,
   then `#minecraft:tick` every tick — only if `TickRateManager.runsNormally`); the clocks
   (`ServerClockManager.tick`, same gate); a `ClientboundSetTimePacket` to
   everyone every 20 ticks (`MinecraftServer.forceGameTimeSynchronization`);
   then `MinecraftServer.updateEffectiveRespawnData` and **each
   `ServerLevel.tick`** in `MinecraftServer.getAllLevels` order, overworld
   first — the subject of [the level tick](server-level-tick.md). A throwable
   from a level becomes a `ReportedException` ("Exception ticking world") and
   ends the server.
6. **Connections tick after levels — and that is where players tick.**
   `MinecraftServer.tickConnection` → `ServerConnectionListener.tick` walks
   every `Connection` under a lock: `Connection.tick` flushes the outbound
   queue, ticks its `TickablePacketListener` — for a playing client that is
   `ServerGamePacketListenerImpl.tick`, which runs the `ServerPlayer`'s own
   per-tick logic, the spam throttles and the 15-second keep-alive
   (`ServerCommonPacketListenerImpl.LATENCY_CHECK_INTERVAL`) — and drops dead
   connections with `Connection.handleDisconnection`. `DedicatedServer.tickConnection`
   adds `DedicatedServer.handleConsoleInputs`, which is how console and RCON
   commands reach the Server thread. `PlayerList.tick` itself only broadcasts
   a `ClientboundPlayerInfoUpdatePacket` of latencies every
   `PlayerList.SEND_PLAYER_INFO_INTERVAL` (600) ticks.
7. **Chunks go out last, in one flush.** After `ServerDebugSubscribers.tick`,
   `GameTestTicker.tick` and the `MinecraftServer.tickables` (the dedicated
   server GUI's refresh), every player's `PlayerChunkSender.sendNextChunks`
   runs and `ServerCommonPacketListenerImpl.resumeFlushing` releases the
   connection. Everything the tick decided to tell a client — entity
   movement, block changes, chunks — leaves the JVM as one write per client
   per tick.
8. **Bookkeeping.** `MinecraftServer.buildServerStatus` is rebuilt if the
   cached one is over `MinecraftServer.STATUS_EXPIRE_TIME_NANOS` (5 s) old;
   `MinecraftServer.ticksUntilAutosave` counts down to
   `MinecraftServer.autoSave`; the tick's duration replaces its slot in
   `MinecraftServer.tickTimesNanos` and updates the aggregate and the
   smoothed millis. The `SampleLogger` stream is a separate ledger, written
   from three different points, one per `TpsDebugDimensions` slot:
   `MinecraftServer.logTickMethodTime` here
   (`TpsDebugDimensions.TICK_SERVER_METHOD`),
   `MinecraftServer.finishMeasuringTaskExecutionTime` after the wait
   (`TpsDebugDimensions.SCHEDULED_TASKS` and `TpsDebugDimensions.IDLE`), and
   `MinecraftServer.logFullTickTime` at the very bottom of the loop
   (`TpsDebugDimensions.FULL_TICK`), which flushes the whole four-slot sample
   and measures the **entire loop iteration** — tick plus wait — not the tick
   alone. None of it runs unless `MinecraftServer.isTickTimeLoggingEnabled`,
   which on a dedicated server means a client has subscribed to
   `DebugSubscriptions.DEDICATED_SERVER_TICK_TIME`.
9. **The slack is spent, not slept.** `MinecraftServer.runServer` — not
   `MinecraftServer.waitUntilNextTick` — is what sets
   `MinecraftServer.mayHaveDelayedTasks` and computes
   `MinecraftServer.delayedTasksMaxNextTickTimeNanos`, the deadline deferrable
   work may run to; every subsequent poll overwrites the flag with "was there
   more". `MinecraftServer.waitUntilNextTick` itself is two statements:
   `BlockableEventLoop.runAllTasks`, then `BlockableEventLoop.managedBlock` on
   "no time left". `MinecraftServer.waitForTasks` parks the thread with
   `LockSupport` until `MinecraftServer.nextTickTimeNanos`, or 100 µs at a
   time when the loop is not waiting on a tick — and
   `BlockableEventLoop.schedule` unparks it, so a submitted task cuts the park
   short. `PacketProcessor.scheduleIfPossible` pointedly does not: a packet
   that lands during the slack waits for the next tick's drain instead of
   waking the thread. When sprinting, `ServerTickRateManager.endTickWork`
   counts the tick down and `ServerTickRateManager.finishTickSprint` prints
   the measured rate when the sprint ends.

10. **Then the loop's own bookkeeping — including the crash path.**
    `MinecraftServer.isReady` is set at the bottom of *every* iteration (not
    once after the first tick), and `JvmProfiler.onServerTick` is fed the
    smoothed millis. A throwable that escapes anything above leaves the loop
    for good: `MinecraftServer.constructOrExtractCrashReport` unwraps the
    innermost `ReportedException` — or wraps the throwable as "Exception in
    server tick loop" — the report is written to *crash-reports/*,
    `MinecraftServer.onServerCrash` runs, and the *finally* performs exactly
    the shutdown `/stop` performs; see
    [server lifecycle](server-lifecycle.md). Crashes from *other* threads
    arrive here too: `BlockableEventLoop.delayCrash` parks an exception for
    the owning thread and the next `BlockableEventLoop.pollTask` rethrows it,
    so a worker's failure surfaces as a tick-loop crash.

## Interfaces

- **Called by:** `MinecraftServer.runServer` only. `DedicatedServer` and
  `IntegratedServer` override pieces — `DedicatedServer.tickServer` adds the
  JSON-RPC `ManagementServer.tick`, `DedicatedServer.tickConnection` the
  console, `IntegratedServer.tickServer` the pause — never the loop.
- **Calls into:** `ServerLevel.tick` (Part III), `ServerConnectionListener.tick`
  ([the connection](../networking/the-connection.md)), `ServerFunctionManager.tick` (Part XIII), `PlayerList`,
  `ServerClockManager`, `GameTestTicker`.
- **Crosses the network as:** `ClientboundSetTimePacket` (every 20 ticks);
  `ClientboundTickingStatePacket` (rate and frozen flag, sent by
  `ServerTickRateManager.setTickRate` / `ServerTickRateManager.setFrozen`
  and to each joining player by `ServerTickRateManager.updateJoiningPlayer`)
  and `ClientboundTickingStepPacket` (from `ServerTickRateManager.stepGameIfPaused`);
  `ClientboundPlayerInfoUpdatePacket` with latencies every 600 ticks;
  `ClientboundDisconnectPacket` ("Internal server error") when
  `Connection.tick` throws — note that this is the *connection* phase, not the
  packet drain, where a throwing handler is suppressed instead. Sprinting is
  not signalled as such — the client only sees the unfreeze before and the
  refreeze after.
- **Data-driven by:** `server.properties` through `DedicatedServerProperties`
  (`pause-when-empty-seconds`, `max-tick-time`); the `GameRules.ADVANCE_TIME`
  rule; the `#minecraft:tick` and `#minecraft:load` function tags.

## Invariants and surprises

- **"Can't keep up!" is the server *skipping* ticks, not catching up.**
  `MinecraftServer.runServer` moves `MinecraftServer.nextTickTimeNanos` forward over the backlog; there is no
  burst of extra ticks afterwards. And it only logs when more than two
  seconds behind, so a server that is consistently 40 % late never says so.
- **Packets are handled at the top of the tick, in one batch, and player
  ticks happen *after* the levels.** So a player's movement packet is
  applied before the world ticks, but the player entity's own
  `ServerGamePacketListenerImpl.tick` runs under the *connection* section,
  after every `ServerLevel.tick` has already run. Entities in the level
  see the player where the packets put them; the player ticks against the
  world's new state.
- **Outbound packets leave twice per tick per client, not once.**
  `ServerCommonPacketListenerImpl.suspendFlushing` at the top of
  `MinecraftServer.tickChildren` makes each `ServerCommonPacketListenerImpl.send`
  a write without a flush — but `Connection.tick` flushes the channel
  unconditionally, in the *connection* section. So everything the levels and
  the player's own tick produced goes out there, and
  `ServerCommonPacketListenerImpl.resumeFlushing` after chunk sending carries
  whatever `MinecraftServer.tickChildren` produced *after* that point: the
  player list, the debug subscribers, the game-test ticker, the server's own
  tickables, and last the chunk batch. The suspension is defeated in one more case:
  a send from a thread that is not the Server thread flushes immediately.
- **Sprint is a zero-length tick.** Not a shorter one: `TickRateManager.nanosecondsPerTick`
  is unchanged, `MinecraftServer.runServer` just declares this tick 0 ns long, `MinecraftServer.haveTime`
  becomes a constant false, and the overload check is skipped. Sprinting
  also temporarily unfreezes (`ServerTickRateManager.requestGameToSprint`)
  and restores the previous frozen state at the end.
- **Freeze keeps the loop, the connections and the players running.**
  `TickRateManager.isEntityFrozen` exempts players and anything carrying a
  player; everything else that checks `TickRateManager.runsNormally` — functions, clocks,
  weather, block and fluid ticks, other entities, game tests — stops.
- **Autosave is five wall-clock minutes, not 6000 ticks.** The first
  interval is `MinecraftServer.AUTOSAVE_INTERVAL` (6000); every one after is
  `MinecraftServer.computeNextAutosaveInterval` = tick rate × 300, floored
  at `MinecraftServer.MIMINUM_AUTOSAVE_TICKS` (100 — the typo is Mojang's),
  and `MinecraftServer.onTickRateChanged` re-derives it when `/tick rate`
  changes — but only ever *shortens* the pending countdown, so lowering the
  tick rate never pushes the next autosave further out. While sprinting,
  `MinecraftServer.computeNextAutosaveInterval` uses the *measured* rate from
  `MinecraftServer.getAverageTickTimeNanos` rather than the configured one.
- **`ServerLevel.emptyTime` is a per-dimension sleep.** A level with no
  active tickets (`ServerChunkCache.hasActiveTickets`) counts up; after 300
  such ticks it stops ticking entities and block entities entirely, while
  still running chunk-source and block-event work. An empty Nether costs
  almost nothing.
- **The watchdog reads the deadline, not the tick.** `ServerWatchdog`
  compares the wall clock to `MinecraftServer.getNextTickTime`; a single
  tick longer than `DedicatedServerProperties.maxTickTime` (default 60 s)
  halts the JVM. See [Server lifecycle](server-lifecycle.md).
- **The tick loop is instrumented three ways.** `MinecraftServer.tickFrame`
  is a `DiscontinuousFrame` from `TracyClient`, opened in
  `MinecraftServer.processPacketsAndTick` *before* the packet drain and closed
  after `MinecraftServer.tickServer` — so the Tracy frame includes the
  packets. The JFR path is `JvmProfiler.onServerTick`. And every iteration
  gets a fresh `ProfilerFiller` from `MinecraftServer.createProfiler`, which
  composes the `MetricsRecorder`'s profiler with a `SingleTickProfiler`; the
  `/debug start` timer (`MinecraftServer.TimeProfiler`) arms itself at the
  *top* of an iteration through `MinecraftServer.debugCommandProfilerDelayStart`.
- **The slack buys ticket propagation first.** `ServerChunkCache.MainThreadExecutor`
  has its own policy: its `ServerChunkCache.MainThreadExecutor.shouldRun` is unconditionally true — no
  three-tick-latency rule — and its poll runs
  `ServerChunkCache.runDistanceManagerUpdates` before anything else. So the
  first thing the leftover milliseconds are spent on is chunks changing
  status.

## Where to look

`MinecraftServer.runServer` · `MinecraftServer.tickServer` ·
`MinecraftServer.tickChildren` · `MinecraftServer.waitUntilNextTick` ·
`MinecraftServer.haveTime` · `TickTask` · `ReentrantBlockableEventLoop`
· `BlockableEventLoop` · `PacketProcessor` · `PacketUtils` ·
`TickRateManager` · `ServerTickRateManager` · `TickCommand` ·
`ServerConnectionListener` · `ServerCommonPacketListenerImpl` ·
`IntegratedServer` · `DedicatedServer` · `ServerClockManager` ·
`ServerActivityMonitor` · `SampleLogger` · `TpsDebugDimensions`

---

*Rules: names, never code · how the system works, not how the code reads ·
newest version only · every backticked name passes `tools/verify_names.py`.*
