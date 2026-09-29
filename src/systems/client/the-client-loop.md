# The client loop

> Verified against **Minecraft 26.3** · Part X · one turn of `Minecraft.run`: how much simulated time a frame owes, what it spends it on, and what happens to the time it cannot afford.

The client has one loop and no schedule. A tick is not a timer callback and
not a thread — it is something the loop does on its way to a frame, as many
times as the clock says it owes. The clock is asked once per iteration, it
answers in whole ticks, and the loop then runs at most **ten** of them. A
frame that earned fifteen runs ten and loses five — and the five are not
deferred. The clock keeps its leftover as a fraction of a tick and hands out
whole ticks as they come due; a tick that has been counted has left that
leftover for good, so nothing will ever run the five, and the world you are
standing in has skipped forward without simulating the gap. That the two programs keep
different clocks at all is [the two loops](../anatomy/anatomy.md#two-loops-and-a-wire-between-them),
and the contrast is sharpest here: the server drops ticks too, but only once
it is more than the overload threshold plus twenty ticks behind, and it logs
*Can't keep up!* when it does ([the server
tick](../server/server-tick.md#the-event-loop-and-what-a-ticks-spare-time-buys)).
The client does it on any frame that needs to, at a ceiling of ten, and says
nothing.

The loop on this page runs on one thread, and it is the client's in [the four threads](../anatomy/anatomy.md#four-threads-worth-memorising). `Main.main` renames the JVM's main thread to `"Render thread"` and `RenderSystem.initRenderThread` claims it, so
`Minecraft.gameThread`, `BlockableEventLoop.isSameThread` and
`RenderSystem.assertOnRenderThread` all agree about that one thread. **The name
is the trap.** There is no *separate* render thread — no second thread drawing
while the first one ticks — and there never was one in this version. What the
stack traces call *Render thread* is the thread that runs the loop, ticks and draws, and it is
what every *Render thread* in this part's cast tables means.

## The cast

| class | what it decides | thread |
|---|---|---|
| `Minecraft` | the loop itself, and — being a `ReentrantBlockableEventLoop` — the main thread's task queue | Render thread |
| `DeltaTracker.Timer` | how many whole ticks this frame owes, and what the leftover fraction is | Render thread |
| `PacketProcessor` | where packets decoded on Netty threads wait to be applied | filled on Netty, drained here |
| `TickRateManager` | the tick rate the Timer's target comes from — a shared class the client holds one of, whose rate and freeze only the server sets | read here, decided there |
| `FramerateLimitTracker` | what the frame cap actually is, which is not always the option | Render thread |
| `FramerateLimiter` | the park that enforces it | Render thread |
| `Main` | the process: the config, the shutdown hook, the thread's name | JVM main = Render thread |

## One turn of the loop

`Minecraft.run` spins until `Minecraft.running` goes false, and each
iteration is `RenderSystem.pollEvents` followed by `Minecraft.runTick`. The
figure is that iteration. It is drawn as a flowchart rather than a
conversation because the fact worth having is a *decision* — the clamp, and
what falls off the end of it.

```mermaid
flowchart TD
    POLL["RenderSystem.pollEvents — SDL events, inline"]
    subgraph RT["Minecraft.runTick"]
        PRE["Pre render: Window.shouldClose, then a pending reload"]
        ASK["DeltaTracker.Timer.advanceGameTime — whole ticks owed"]
        DRAIN["PacketProcessor.processQueuedPackets, then BlockableEventLoop.runAllTasks"]
        TEX["TextureManager.tick, once if a tick is owed and the world is not frozen"]
        CLAMP{"more than ten ticks owed?"}
        TICK["Minecraft.tick, up to ten times"]
        PREFRAME["Render: SoundManager.updateSource, then MouseHandler.handleAccumulatedMovement"]
        FRAME["Minecraft.renderFrame, then the limiter parks"]
        POST["Post render: recompute Minecraft.pause, the timer's pause and freeze"]
        PRE --> ASK --> DRAIN --> TEX --> CLAMP
        CLAMP -- "no" --> TICK
        CLAMP -- "yes: the excess already left the residual" --> TICK
        TICK --> PREFRAME --> FRAME --> POST
    end
    POLL --> PRE
    POST -- "Minecraft.run, next iteration" --> POLL
```

*One iteration, with the boundary drawn: only `RenderSystem.pollEvents` is
outside `Minecraft.runTick`, which is why a key press lands in no profiler
zone. Both answers to the clamp reach the same node, which is the point: at most ten run either way, and what differs is what became of the rest.*

Read it as **owe, spend, draw, settle**. The clock says how much simulated
time has passed; the loop spends it on packets, tasks and up to ten ticks;
the frame draws whatever the world looks like afterwards; and only then does
the loop notice whether the game is now paused — which is why the first
frame of a pause is drawn unpaused.

Two of the figure's nodes need unpacking. The drain is two calls, not one — `PacketProcessor.processQueuedPackets` takes
the packets Netty decoded, `BlockableEventLoop.runAllTasks` takes everything
else the thread was handed — and the pair between the ticks and the frame is
`SoundManager.updateSource`, which sends the camera to the OpenAL listener on the sound thread, then `MouseHandler.handleAccumulatedMovement`, which turns the mouse delta into rotation. Both of the second pair run **after** the ticks and before the frame, so an iteration's ticks run on the old rotation and its frame shows the new one.

*Pre render*, *Render* and *Post render*, which head three of the figure's
nodes, are `Window.setErrorSection` calls — the crash report's breadcrumb, so a
client that dies takes whichever of the three it was in to the report with it. What happens inside the frame is [the
frame](../rendering/the-frame.md#the-zones-a-frame-is-made-of);
this page does not follow the loop inside the profiler's *frame* zone, and every zone inside
it is that page's. Note where the frame limiter sits: inside `Minecraft.renderFrame`,
after the present, with only the *fpsUpdate* zone after it, and *before* the
pause is recomputed.

## The ten, and the arithmetic behind it

`DeltaTracker.Timer.advanceGameTime` takes the elapsed milliseconds, divides
by whatever `DeltaTracker.Timer.targetMsptProvider` returns for
`DeltaTracker.Timer.msPerTick`, adds the result to
`DeltaTracker.Timer.deltaTickResidual`, takes the whole part out and returns
it. The fraction that stays behind is the partial tick everything
interpolates against. The clamp then happens in the loop, not in the Timer —
so the ticks above ten are not deferred to the next frame, because they left
the residual when they were counted.

**Ten ticks** is the ceiling, the number `Minecraft.MAX_TICKS_PER_UPDATE` names. The clamp in `Minecraft.runTick` shows the number rather than the name because *javac* writes a `static final int` set to a literal in at every use site, so a decompile can never tell a documented constant from a dead one.

The divisor is not the client's to choose. `DeltaTracker.Timer` gets its
target from `DeltaTracker.Timer.targetMsptProvider`, which is
`Minecraft.getTickTargetMillis`, which asks the level's `TickRateManager`
for `TickRateManager.millisecondsPerTick` whenever it
`TickRateManager.runsNormally`, and never less than fifty milliseconds. **`/tick rate` is a server command that changes the arithmetic inside the client's frame loop** — when it slows the world down; a faster rate leaves the client at twenty ticks a second. `/tick freeze` is
a different lever — under it the Timer's divisor falls back to fifty milliseconds — and the loop reads it directly rather
than through the Timer: `Minecraft.isLevelRunningNormally` asks the level's
`TickRateManager` again, and that is what stops `TextureManager.tick` — which
is why freezing the world freezes the water texture — and what gates
`ClientLevel.animateTick` and `ParticleEngine.tick` inside the tick. The
Timer is *told* the same answer at the end of the iteration, through
`DeltaTracker.Timer.updateFrozenState`, so that the partial tick it hands out
stops moving too.

Alongside the game clock the Timer runs a second, unpausable one.
`DeltaTracker.Timer.advanceRealTime` produces
`DeltaTracker.getRealtimeDeltaTicks`, which the menus' panorama and the autosave indicator animate against, so they move when game time does not. The two constants `DeltaTracker.ZERO` and
`DeltaTracker.ONE` — two instances of the one nested `DeltaTracker.DefaultValue`
— exist so that code which needs a partial tick can be handed *no*
interpolation or *complete* interpolation without a branch.

## What a tick is, in order

`Minecraft.tick` is one long method, its order is a dependency order, and the
column that matters is the third: most of it is inside a gate, and two of the things that are not are the reason the main menu has music.

| in order | what runs | what gates it |
|---|---|---|
| 1 | `Minecraft.clientTickCount` advances | nothing |
| 2 | `TickRateManager.tick` | a level, and not paused |
| 3 | the game mode | a level, and not paused |
| 4 | `Minecraft.pick`, at a partial tick of one | nothing |
| 5 | `Tutorial.onLookAt`, with what the pick found | nothing |
| 6 | `Gui.tick` — `Minecraft.missTime` pinned high while a screen is open | nothing |
| 7 | the keybind drain, `Minecraft.handleKeybinds` | neither a screen nor an overlay — **and nothing about a level** |
| 8 | `GameRenderer.tick`, `ClientLevel.tickEntities`, `Level.tickBlockEntities`, then `LocalPlayer.sendChanges` — the input and movement packets | a level, and not paused |
| 9 | the music and sound managers | nothing |
| 10 | the first-server toast, `Tutorial.tick`, then `ClientLevel.tick` alone inside a crash-report handler | a level, and not paused |
| 11 | `ClientLevel.animateTick`, `ParticleEngine.tick` | a level, not paused, and the tick rate manager running normally |
| 12 | `ServerboundClientTickEndPacket` | a level, a connection, and not paused |
| 13 | `KeyboardHandler.tick`, where the F3+C crash countdown lives | nothing |

Six of the thirteen rows are gated on nothing where they are called, and four of them are what a client with no world is still doing: it counts ticks, it runs the interface, it plays music, and it runs the F3+C crash countdown. The pick and the tutorial's look are called too, and each returns at once without a level.
Everything that is the *world* is inside `level != null && !pause`. With no
level that middle collapses — but not into one branch. Two separate *else*
arms at two points in the method clear the spectated entity's post-effect and
tick the pending connection, with row nine running between them.

Two of those rows are load-bearing elsewhere in the book. Row twelve is why
a client still in configuration sends no tick-end packet at all: it sits
inside the level block, and the server reads the packets it does get to decide
that a player who sent no movement this tick is standing still. And row four
is only half of `Minecraft.pick`, which runs **once per tick and once per
frame** — the tick's call at a partial tick of one, the
frame's at the real one, and it is the frame's result the crosshair and the
block outline use. A frame that runs three ticks calls it four times; a frame
that runs none calls it once.

## Where work leaves this thread, and where it comes back

Five ways off this thread, and one re-entry that is not a way off it.

- **Packets** decoded on Netty threads are parked by
  `PacketProcessor.scheduleIfPossible` and drained in the
  *scheduledPacketProcessing* zone — once per frame, not once per tick. That
  single fact is behind most of what looks like network jitter; [the
  connection](../networking/the-connection.md) is the other side of it.
- **Tasks** from other threads land in *scheduledExecutables* through
  `BlockableEventLoop.execute`. From *this* thread the same call usually runs
  inline instead of queueing — but not while a task is already running, inline or queued, because `ReentrantBlockableEventLoop.scheduleExecutables` returns true for
  the whole of `ReentrantBlockableEventLoop.doRunTask`, which is what stops a
  task from re-entering itself. SDL events, dispatched by `SDLEventHandler.pollEvents`
  inside `RenderSystem.pollEvents`, are not inside one, so they execute *before*
  the tick that will observe them — see [input and keybinds](input-and-keybinds.md).
- **Section meshing** goes to `Util.backgroundExecutor` and is collected by
  `SectionRenderDispatcher` (Part XI).
- **Timers**, of which the client has exactly two, and neither changes the game from its own thread. `PeriodicNotificationManager` and
  `RemoteFriendListUpdateHandler` each own a scheduler, and each hops back here with `BlockableEventLoop.execute` before touching the game (the friends list swaps its own fetched data in on its own thread) — which is why nothing in the client's simulation is ever driven by a timer callback.
- **GPU work** registered with `RenderSystem.queueFencedTask` is picked up by
  `RenderSystem.executePendingTasks`, which stops at the first unsignalled
  fence rather than waiting. It looks general and is not: the one thing in
  the tree that queues a fenced task is the OpenGL backend's asynchronous
  texture readback.

The re-entry is `BlockableEventLoop.managedBlock`, which pumps that second
queue while the loop is *blocked* waiting for the integrated server or for a world's resources to load — so work
runs on this thread at a moment when the thread is not running its loop at all.
The mechanism is [the server
tick](../server/server-tick.md#the-event-loop-and-what-a-ticks-spare-time-buys).

The profiler wraps all of it. `Minecraft.constructProfiler` picks one per iteration — `InactiveProfiler`, or the frame-profile `ContinuousProfiler` behind the F3 pie chart — combined with the `MetricsRecorder`'s profiler while it records and a `SingleTickProfiler` when a debug flag asks for one, and `Minecraft.finishProfilers` ends the single-tick one and posts the pie chart's results. `RenderSystem.pollEvents` is
inside the profiler scope but outside `Minecraft.runTick`, so **input polling
lands in no named zone** and shows up on the pie chart as unspecified time.
That is not why
`RenderSystem.isFrozenAtPollEvents` exists, though: its one caller is
`ClientCommonPacketListenerImpl.handleKeepAlive`, which holds the keep-alive reply back while a poll has been stuck for more than 200 milliseconds and sends it from the connection's first tick after the poll returns — so a game stuck in the poll by a window drag reaches the server as latency.

## Pausing, which is a field the screen votes on

`Minecraft.pauseIfInactive`, called during the frame, opens the pause menu when no screen is up, the window has been unfocused for more than half a second and `Options.pauseOnLostFocus` is on — and the menu pauses the game only through its vote. `Minecraft.pause` — the field — is
recomputed at the very end of `Minecraft.runTick` as a conjunction of three:
*singleplayer*, and the GUI says we are pausing, and the world is not open to
LAN. Only the middle one is a question about the interface — `Gui.isPausing`
asks the current screen and overlay, and `Screen.isPauseScreen` defaults to
**true**, which is why the options screen stops a singleplayer world and a
chest does not ([GUI and
screens](gui-and-screens.md#gui-which-is-not-the-hud) owns the vote and the
override a container screen casts). On the rising edge the loop calls `SoundManager.pauseAllExcept`, sparing music and UI sounds, and every iteration it hands the state to `DeltaTracker.Timer.updatePauseState`.

## The frame cap is usually the option, and sometimes is not

`FramerateLimitTracker.getFramerateLimit` returns the option unchanged
normally; caps it at thirty after a minute idle; replaces it with ten when
the window is iconified or after ten minutes idle; and replaces it with
**sixty** in a menu with no level — which can be *more* than the player
asked for. The iconified case is **iconified, not unfocused** — a different
state with a different consequence, one section above — except in exclusive
fullscreen, where an unfocused window counts as iconified. The two idle
cases apply only when `Options.inactivityFpsLimit` is set to the AFK
behaviour, and the iconified test wins over both.
`FramerateLimiter.limitDisplayFPS` is skipped entirely at or above 260 — the
option's own maximum, i.e. "unlimited"; below it, it parks for most of the
remainder, correcting for how much the JDK's park habitually overshoots, and
busy-spins the last fraction. The profiler notices too, though it does not
stop: `FramerateLimitTracker.isHeavilyThrottled` is the `ContinuousProfiler`'s
*suppress warnings* predicate, so a throttled client still measures itself but
stops complaining that its frames are slow.

The frame's timing is three different measurements, two of them on the F3 screen, and it is worth knowing which is which. `Minecraft.fps` is a static field sampled once a
second, and is the one printed as *fps*. `Minecraft.frameTimeNs` is a CPU span
that stops at the blit, before the present and before the limiter, and is read
by nothing but telemetry — so it appears on no line of the overlay. The third
has no name of its own: the frame-time *graph* is fed wall-clock between
frames, measured *after* the limiter, so it includes the sleep — as the frame count does and `Minecraft.frameTimeNs` does not.

## Starting, and the three ways of stopping

`Main.main` builds a `GameConfig` from the command line, installs a shutdown
hook, renames the thread, calls `RenderSystem.initRenderThread` and
constructs `Minecraft`; a `SilentInitException` out of that constructor exits
quietly rather than crashing. `Minecraft.running` is set true inside that
constructor, but five statements *after* the `Options` are read from disk. A
setting's listener only fires while that flag is true, so every
`OptionInstance.set` performed while loading *options.txt* silently skips its
own — [the loading
guard](options.md#the-guard-that-silences-settings-loaded-at-startup) is that
rule and what it costs. `Main.main` then
calls `Minecraft.exitWorldAndClose`, and its last statement arms
`ClientShutdownWatchdog.startShutdownWatchdog` over what follows. That is the
second of two armings, not the only one: the window-close callback arms the same watchdog against the Render thread while the game is still running, so a close the window is asked for is watched from the moment of the request, where a Quit button's is not watched until `Main.main` arms it after `Minecraft.exitWorldAndClose` returns. The two do not have the same powers, either.
Both start a daemon thread that sleeps fifteen seconds and, unless a later arming has moved the counter on by then, builds a crash report from the main
thread's stack — but the close-callback arming stops there, at *report only*,
while the one after `Minecraft.run` has returned goes on to take the process
down — unless the close-callback watchdog has already fired, which leaves the counter where no later arming can start.

Stopping has three doors and one corridor. `Minecraft.stop` sets
`Minecraft.running` false, and is what `Window.shouldClose` triggers at the
top of `Minecraft.runTick`. `Minecraft.emergencySaveAndCrash` is where a
`ReportedException` or any other throwable from the loop body ends up, by way
of `Minecraft.emergencySave`, which releases the reserved memory block, halts
the integrated server and shows the saving screen. And an out-of-memory error
does not necessarily end anything: the first one makes `Minecraft.run` stop
advancing game time altogether — GUI only, no ticks, no packets, no world —
after an emergency save; a second one rethrows.

The corridor is `Minecraft.exitWorldAndClose` and then `Minecraft.close`,
which tears down in a fixed order — the time source first, outside the try,
then an offline presence to the friends service, the friends list, the timer
query, telemetry, compliancies, the atlas and font managers, the game renderer,
the shader manager, the level renderer, the sound manager, the three texture
managers, resources, the Tracy capture, the narrator, FreeType, the surface and
the renderer — and then, in a finally block, only the window, the graphics
backend's library, SDL's own shutdown and the executors. There is no *Minecraft.destroy*.

> **For a 1.21-era reader.** Names to stop hunting for:
> *Minecraft.getPartialTick*, *Minecraft.noRender*, *Minecraft.tell*,
> *Minecraft.destroy*, *Minecraft.screen* and *Minecraft.setScreen* (both now
> on `Gui`), *Timer* (now `DeltaTracker.Timer`), *GLFW* and its callbacks (now SDL
> events, drained by `SDLEventHandler.pollEvents`), and *initGameThread* /
> *isOnGameThread*, which do not exist because the second thread they distinguished does not either.

## Where to look

`Minecraft.run` and `Minecraft.runTick` — the loop is those two methods.
`DeltaTracker.Timer.advanceGameTime` for the tick arithmetic and
`Minecraft.getTickTargetMillis` for who sets its rate. `Minecraft.tick` for
the ordered contents of a tick. `FramerateLimitTracker.getFramerateLimit` for
the frame cap that is not the option. `Main.main` for how the process starts,
and `Minecraft.close` for the order in which it comes apart.

---

*Rules: names, never code · how the system works, not how the code reads ·
newest version only · every backticked name passes `tools/verify_names.py`.*
