# Execution and functions

> Verified against **Minecraft 26.2** · Part XIII · A `#minecraft:tick` function runs `execute as @a at @s run …`: a command engine with no Java recursion, a fan-out that materialises one source at a time, and a `/return` that deletes work out of a queue rather than unwinding a stack.

## Responsibility

Once a command has been parsed ([Brigadier and commands](brigadier-and-commands.md)),
something has to *run* it — and in Minecraft "it" is rarely one command. A
single line can be a function that calls a function that forks over every
player and conditionally calls another function. Doing that with the Java
call stack is how you get a data pack that crashes the server with a
`StackOverflowError`, which is exactly what used to happen.

So the engine is a **trampoline**. Every construct that used to nest —
`/execute … run`, `/function`, `execute if function`, `/return run` — is
expressed as *queued work* on a heap-allocated queue. The consequences are
worth stating before the classes, because they are the whole design:

- A data pack cannot exhaust the Java stack. A million-deep recursion costs
  a million queue entries and a million cost units, and dies on a budget.
- "Abandon everything this function was going to do" becomes a *splice*
  out of a queue, which is what makes `/return` implementable.
- Tracing (`/debug function`) is a first-class hook rather than a stack
  walk.
- Nothing can yield. A function runs to completion inside the tick that
  started it, or is cut off by the budget.

The one sentence a player would recognise: *the data pack that runs every
tick.*

## The data it owns

The engine is `net/minecraft/commands/execution`, the function model is
`net/minecraft/commands/functions`, and both are entirely server-side.

- **`ExecutionCommandSource`** — the interface the whole engine is generic
  over, and the reason none of it mentions `CommandSourceStack`. It declares
  `ExecutionCommandSource.withCallback`, `ExecutionCommandSource.callback`,
  `ExecutionCommandSource.handleError` and
  `ExecutionCommandSource.isSilent`, plus the static consumer that Brigadier's
  dispatcher is wired to. Every claim below about suppressed failures and
  stored results bottoms out here and in
  `CommandSourceStack.handleError`, which reports to the tracer
  unconditionally and to the player only when the source is not forked.
- **`ExecutionContext`** — one per *thread-locally* outermost command or
  function call. It owns `ExecutionContext.commandQueue`,
  `ExecutionContext.newTopCommands` (the staging list), the budget
  (`ExecutionContext.commandQuota` counting down from
  `ExecutionContext.commandLimit`), `ExecutionContext.forkLimit`, the
  profiler, an optional `TraceCallbacks`, and the ten-million cap on staged
  plus queued entries. `ExecutionContext.runCommandQueue` is the driver loop;
  `ExecutionContext.queueNext`, `ExecutionContext.pushNewCommands`,
  `ExecutionContext.discardAtDepthOrHigher`,
  `ExecutionContext.frameControlForDepth` and
  `ExecutionContext.incrementCost` are the five methods everything else on
  this page is made of.
- **`CommandQueueEntry`** — a `Frame` and an `EntryAction`. That is the
  entire unit of work.
- **`Frame`** — *not* a stack frame. A record of a depth, a
  `CommandResultCallback` that a `/return` in that frame feeds, and a
  `Frame.FrameControl` that knows how to delete the frame's pending work.
  One `Frame` object is shared by reference across every entry produced on
  behalf of one function body. `Frame.returnSuccess`,
  `Frame.returnFailure` and `Frame.discard` are the whole interface.
- **`EntryAction`** and **`UnboundEntryAction`** — an action, and an action
  that still needs a source. `UnboundEntryAction.bind` curries the source
  in. A compiled function line is an `UnboundEntryAction`.
- **`ExecutionControl`** — the narrow face an in-flight command sees:
  queue something, read or set the tracer, ask for the current frame.
- **`ChainModifiers`** — two bits: forked, and in-return-mode. Set once in
  a chain and carried for the rest of it.
- **`CustomCommandExecutor`** and **`CustomModifierExecutor`** — the escape
  hatches for a command that wants the engine instead of Brigadier's plain
  "return an int". There are exactly six implementors:
  `FunctionCommand.FunctionCustomExecutor` (`/function`),
  `ReturnCommand.ReturnValueCustomExecutor` and
  `ReturnCommand.ReturnFailCustomExecutor` (`/return <value>` and
  `/return fail`), `DebugCommand.TraceCustomExecutor` (`/debug function`),
  `ExecuteCommand.ExecuteIfFunctionCustomModifier` (`execute if function`)
  and `ReturnCommand.ReturnFromCommandCustomModifier` (`/return run`).
  `CustomCommandExecutor.WithErrorHandling` is the shared base that routes a
  thrown `CommandSyntaxException` to both the source's error handler and its
  callback. Their adapter nestings implement Brigadier's interfaces with
  methods that throw, purely so the node is registerable.
- **The tasks** (`commands/execution/tasks`) — `BuildContexts` walks the
  stages of a parsed chain (with `BuildContexts.TopLevel`,
  `BuildContexts.Continuation` and `BuildContexts.Unbound`);
  `ExecuteCommand` is the leaf that actually runs one executable;
  `CallFunction` opens a frame for a function body; `ContinuationTask` is
  the lazy fan-out; `IsolatedCall` makes a sub-execution whose `/return`
  cannot reach the caller; `FallthroughTask` is the "nothing returned a
  value" marker.
- **`CommandFunction`** — the compiled, uninstantiated function.
  `CommandFunction.fromLines` is the compiler and
  `CommandFunction.parseCommand` is the per-line step.
  `CommandFunction.shouldConcatenateNextLine` implements the trailing
  backslash, and `CommandFunction.checkCommandLineLength` the two-million
  character cap.
- **`InstantiatedFunction`** — an id and an ordered list of unbound
  actions. That is the entire runnable representation of a function.
- **`PlainTextFunction`** — a macro-free function; it is both the compiled
  and the instantiated form, so instantiating one allocates nothing.
- **`MacroFunction`**, **`StringTemplate`** and **`FunctionBuilder`** — the
  macro half. `MacroFunction.cache` is an eight-entry LRU of instantiated
  variants; `MacroFunction.MAX_CACHE_ENTRIES` is that eight.
  `StringTemplate` owns the `$(name)` syntax:
  `StringTemplate.isValidVariableName` allows letters, digits and
  underscores, a `$` not followed by a bracket passes through literally, and
  an unterminated variable is a compile error.
- **`FunctionInstantiationException`** — carries a `Component`, which is why
  `/function` can render an instantiation failure and the tick loop can
  swallow one.
- **`ServerFunctionLibrary`** — the reload listener; holds the volatile
  function and tag maps and the compile-time `PermissionSet`.
- **`ServerFunctionManager`** — the runtime face:
  `ServerFunctionManager.TICK_FUNCTION_TAG`,
  `ServerFunctionManager.LOAD_FUNCTION_TAG`, and
  `ServerFunctionManager.getGameLoopSender`, the source those functions run
  as.
- **`CommandResultCallback`** — a success flag and an integer. This pair is
  what "the result of a command" means everywhere in the game.
  `CommandResultCallback.chain` short-circuits on
  `CommandResultCallback.EMPTY`, which is what makes an unwatched result
  free.

## When it runs

`ServerFunctionManager.tick` is the **first** thing
`MinecraftServer.tickChildren` does after suspending every player's outbound
flush — before the clocks, before the time sync, before any level ticks, and
therefore long before connections and players tick, which in 26.2 happen
*after* the levels ([the server tick](../server/server-tick.md)). It no-ops
entirely when the tick rate manager is not running normally, so `/tick
freeze` suspends data packs. `#minecraft:load` runs once after a reload or
start; `#minecraft:tick` runs every tick from a list snapshotted at reload.

Each function in a tag gets its **own** `ExecutionContext`, so the budget is
per function, not shared across the tag.

Scheduled functions are elsewhere, and the gate matters: `/schedule` puts a
callback in the server's timer queue — server-wide saved data, not per level
— and `ServerLevel.tickTime` advances it right after setting the game time.
That whole method is behind the level's own *tickTime* flag, which only the
overworld has, so a scheduled function fires once per tick rather than once
per dimension.

**Compilation is not on the server thread.** `ServerFunctionLibrary`
parses every `.mcfunction` in parallel on the reload's background executor,
against a compilation source with a null level and a null server; only the
map swap happens on the main thread. The maps are volatile because the
library object itself is built on a background thread and read from several.

## The trace: a function forks over every player

The function contains one line: `execute as @a at @s run say hi`.

```mermaid
sequenceDiagram
    participant SFM as ServerFunctionManager
    participant C as Commands
    participant EC as ExecutionContext
    participant CF as CallFunction
    participant BC as BuildContexts
    participant CT as ContinuationTask
    participant XC as ExecuteCommand

    SFM->>C: executeCommandInContext — a source at gamemaster, output suppressed
    C->>EC: new context; limits read from the level's game rules
    EC->>CF: queue the initial call, in a depth-zero frame
    CF->>CF: spend a cost unit, open a frame at depth one
    CF->>CT: schedule the function's lines — one entry, or a continuation if three or more
    CT->>BC: emit the entry for one line, then re-queue itself behind it
    BC->>BC: walk the stages — "as @a" forks, one cost unit for the whole stage
    BC->>BC: "at @s" moves each source; the forked flag was set at "as"
    BC->>CT: reaching the execute stage, schedule the fan-out
    CT->>XC: emit the entry for one source, then re-queue itself behind it
    XC->>XC: spend a cost unit, run the executable, report to the tracer
    CT->>CT: ...and only now is the next source materialised
```

Each arrow is a decision.

**The queue is a stack with a staging buffer.** Entries are always taken
from the front and always pushed to the front — but an action does not push
directly. It appends to `ExecutionContext.newTopCommands` while it runs, and
`ExecutionContext.pushNewCommands` splices that list onto the head
afterwards, in order. That two-phase move is what makes the semantics
depth-first: what the current action spawned runs before what was already
pending. An `ArrayDeque` used this way is a call stack made of heap
objects — with the extra power that you can inspect and delete entries.

**A fork does not create frames.** All N sources share one `Frame`.
`BuildContexts.execute` walks the non-execute stages inside a *single*
queue entry, spending one cost unit per stage regardless of how many
sources it produces, and turning a one-element source list into an
N-element one. Frames are opened in exactly three places:
`ExecutionContext.createTopFrame`, `CallFunction` and `IsolatedCall`.

**A chain can split across entries, and only a custom modifier does it.**
When the stage walk meets a `CustomModifierExecutor` it hands off and
returns mid-walk; the rest of the chain resumes later as a
`BuildContexts.Continuation`. That is how `execute if function` and
`/return run` interrupt a chain that otherwise runs to its leaf inside one
entry.

**The fan-out is lazy — and so is a function body.** `ContinuationTask.schedule`
queues nothing for an empty list, one entry for one element, two for two,
and for **three or more** queues exactly **one**: a `ContinuationTask` that
emits the entry for the current element and then re-queues itself. Because
the staging list preserves order, the per-element entry lands ahead of the
self-entry, so element *i* and everything it spawns runs to completion
before element *i+1* is even materialised. The queue cost is constant in N.
Both `CallFunction` (over a function's lines) and `BuildContexts` (over a
chain's sources) go through it, so a hundred-line function and a
hundred-player fork are the same shape in the queue — which is also what
makes `/return` cheap, because discarding one self-entry abandons every line
not yet materialised.

**Discarding is "depth ≥ d, from the head".** Because the queue is
depth-first, entries deeper than a frame are always in front of that
frame's remaining entries. So popping from the head while the depth is at
least *d* removes exactly the callee's pending work plus the rest of this
frame's body, and nothing older. Depth-zero frames are special: their
control clears the whole queue.

**There is one budget and it is spent in exactly three places** —
`BuildContexts` on a modifier stage, `CallFunction` on a function call, and
`ExecuteCommand` on an executed command. The first has a gate worth knowing:
the increment happens only when the stage carries a non-null redirect
modifier, and only after the custom-modifier hand-off has been ruled out. So
a plain `execute run` costs nothing for its redirect, and **`execute if
function` and `/return run` are free** — neither custom modifier ever
reaches the counter. A `ContinuationTask` is free too, so an N-way fan-out
costs N, not N+1.

## Two ways to die

The engine has two failure paths and they are not the same event.

**The quota runs out.** `ExecutionContext.runCommandQueue` logs at *info*
and breaks out of the loop. The queue is not cleared; it is simply abandoned
with the context. Nothing reaches the player.

**The queue overflows.** `ExecutionContext.queueNext` trips when staged plus
queued entries exceed ten million, and
`ExecutionContext.handleQueueOverflow` clears *both* lists and sets a latch
that silently drops every subsequent queue attempt. The driver then logs at
**error**. Different level, different clean-up, and a latch the quota path
has no equivalent of.

## `/return`, and what a result is

`/return` does not unwind. `Frame.returnSuccess` pushes the value sideways
into the callback the caller installed on that frame, and `Frame.discard`
splices the abandoned work out of the queue. There is no search and no
exception. `/return fail` is the same mechanism with
`Frame.returnFailure`, and `/return run` discards the current frame's
remaining work *before* queueing its continuation.

Who installed that callback decides where the value goes.
`ExecutionContext.createTopFrame` gives the outermost frame whatever the
entry point supplied — and the sole caller of
`ExecutionContext.queueInitialFunctionCall`, in `ServerFunctionManager`,
supplies `CommandResultCallback.EMPTY`. The frame a `/return` in the
function *body* sees is a different one, opened by `CallFunction` with its
own callback; `CallFunction.returnParentFrame` decides whether that frame
reuses the *caller's* frame control, which is what lets a `/return` inside
also abandon the caller's remaining work.

Two things the page's shape invites getting backwards. First, the
single-source reduction on the `/return run` path lives in
`BuildContexts.execute`, not in `ReturnCommand`, and it is gated twice: on
return mode, and on the leaf *not* being a `CustomCommandExecutor`. So
`return run execute as @a run function foo` queues one function call per
player with no reduction at all. Second, the chaining runs the other way
than "inner onto outer": what gets chained is the *source's own* callback
with the current frame's return consumer, and on the
`/return run function` path the outer frame's consumer is chained *into* the
inner frame.

The result of a command is always a pair: a **success flag** and an
**integer**. There is no aggregation anywhere in the engine. A fork over N
players delivers N independent results to N sources, so an `execute store
result` writes N times and the last one wins — there is no success count. A
sum exists in exactly one place: `/function` on a *tag*, and only when the
caller installed a real callback. A typed command's *frame* callback is
empty and `Commands.performCommand` returns nothing — but the result still
reaches the source's own callback, which is how `execute store` works on a
command typed in chat.

`FallthroughTask` exists so that a chain which produced no sources still
*fails* rather than returning nothing — and it is a return-mode device: every
site that queues it is inside a return or a conditional.

## Functions, compiled and instantiated

A `.mcfunction` file becomes a runnable thing in two steps, and the second
one usually does nothing.

**Compile, at reload.** `CommandFunction.fromLines` walks the lines: a
trailing backslash joins the next line (and a continuation at end of file is
an error); blanks and `#` comments are skipped; a leading `/` is a hard
error with two different messages depending on whether you wrote one slash
or two; a leading `$` is a macro line; anything else is parsed by
`CommandFunction.parseCommand` into a `BuildContexts.Unbound` — **a compiled
function line is literally a parsed context chain plus its input string,
waiting for a source.** A syntax error on any line fails the whole file,
which is logged at error and then absent from the map.

**Instantiate, per call.** A macro-free function returns itself. A
`MacroFunction` looks up each declared parameter in the argument compound,
stringifies it, and uses the ordered list of strings as a cache key over an
eight-entry LRU. On a miss it substitutes into every macro line and
**re-parses** it, and on a parse failure raises a
`FunctionInstantiationException`.

Stringification is worth knowing because it is where macros surprise
people. `MacroFunction` has explicit cases for floats and doubles (a decimal
format with up to fifteen fraction digits, so `1.0` becomes `1`), for byte,
short and long, and for strings (the *unquoted* value). Everything else —
including integers, compounds and lists — falls through to SNBT; integers
merely happen to render bare, while byte, short and long need their own
cases precisely because SNBT would suffix them.

One `$` line anywhere makes the whole file a macro function, though the
non-macro lines keep their already-compiled form and are never re-parsed.
And a `$` line containing no substitution at all is a **load-time error**,
not a plain command.

## Interfaces

- **Called by:** `Commands.performCommand` for every typed command;
  `ServerFunctionManager.tick` for the two function tags; the timer queue
  for `/schedule` (`FunctionCallback` and `FunctionTagCallback`);
  `AdvancementRewards` for a reward function
  ([advancements](advancements.md)); the `RunFunction` enchantment effect
  ([enchantments](../items/enchantments.md)); and
  `TestEnvironmentDefinition.Functions` for a game test's environment setup
  ([dialogs and tests](dialogs-and-tests.md)). That list is exhaustive.
- **Calls into:** every command in the game, and through them everything
  else.
- **Crosses the network as:** nothing. Execution is entirely server-side;
  only the *effects* of commands produce packets.
- **Data-driven by:** `data/<ns>/function/*.mcfunction` and
  `data/<ns>/tags/function/*.json` — both **singular** directory names.
  `#minecraft:tick` and `#minecraft:load` are the two hooks. The budgets are
  the game rules `GameRules.MAX_COMMAND_SEQUENCE_LENGTH` and
  `GameRules.MAX_COMMAND_FORKS`, both defaulting to 65536; the compile-time
  permission set is the *function-permission-level* server property,
  defaulting to gamemaster.

## The engine's other two commands

`/execute` and `/function` are the front doors, and two more classes are
part of the engine rather than users of it.

- **`ExecuteCommand.scheduleFunctionConditionsAndTest`** is how `execute if
  function` works, and it is the cleverest thing in the area: instantiate
  each function once, wrap every source in an `IsolatedCall` whose callback
  appends that source to a list, then queue a `BuildContexts.Continuation`
  over *the same mutable list*, which the isolated calls fill before the
  continuation reads it. The staging order is what makes that safe. The inner
  `CallFunction` opens against the isolated frame, which is why a `/return`
  inside a condition function cannot reach the caller.
- **`DebugCommand.Tracer`** installs itself on the whole `ExecutionContext`
  rather than per frame, so it traces everything in that context; it refuses
  to nest and refuses return mode; and it implements `CommandSource` as
  well, so the traced function's chat output lands in the trace file
  alongside the call lines.

`ScheduleCommand` is a user rather than part of the engine, but two of its
gates are worth naming: it refuses a macro function outright, and it refuses
a delay of zero.

## Invariants and surprises

- **A function cannot yield.** Work it queues drains inside the same
  driver loop, in the same tick, before the call returns. The
  only escape is `/schedule`.
- **Depth is not bounded.** There is no recursion limit and no depth game
  rule. Recursion is bounded transitively by the cost budget, and fan-out
  by the ten-million entry cap. Depth is only used to order discards and to
  indent the tracer.
- **The cap is on queue *length*, not depth.** `ExecutionContext`'s constant
  is named as though it bounded depth, is never read by name, and is
  compared against staged plus queued entries.
- **The budget is spent, not counted.** The method that decrements the
  quota is named as though it increments a cost. When the quota runs out
  the remaining queue is dropped silently — no player-visible message, one
  info line in the log.
- **The fork limit is checked per contributing source, with a
  greater-or-equal comparison**, so the effective ceiling is one below the
  configured value. When it trips, the handler returns without queueing even
  a `FallthroughTask`, so a `/return run` chain that hits the fork limit
  yields nothing at all rather than a failure.
- **Conditionals are fork nodes.** `execute as @s`, `execute at @s`,
  `execute if block` and friends set the forked flag for the rest of the
  chain — and a forked source **suppresses failure messages**. Putting a
  harmless-looking conditional in front of a command silently converts its
  errors into nothing. They still reach the tracer, which is what
  `/debug function` is for.
- **A `/return` inside a fork does not stop the other sources** — except in
  return mode. `/function` dispatches its N sources eagerly in a plain Java
  loop, each opening its own frame at the next depth, so a `/return` in one
  discards only that callee. It is `return run …` that sets
  `CallFunction.returnParentFrame`, making the inner discard run at the
  outer frame's depth and delete the siblings.
- **"Maximum permission" grants; it does not cap.** The wither that raises
  a function body to at least gamemaster is a *union*, so it can only ever
  add. A more privileged caller is never lowered. The name reads exactly
  backwards.
- **A macro function reached without arguments fails silently, forever.**
  The manager's execute path swallows the instantiation exception with an
  empty catch. A macro function in `#minecraft:tick` fails every single
  tick with nothing logged, printed or counted. Only the `/function`
  command surfaces the error.
- **Every function is compiled against a null level and a null server.**
  Function loading is genuinely parallel across files, and any argument
  type that dereferenced the world during parsing would break a reload.
  It is why `FunctionArgument` reads only an id and defers the lookup — and
  in fact no argument type in 26.2 tests the constraint, since the four that
  parse against a source consult only its permissions.
- **A macro function's instantiated variants all share one synthetic id**,
  derived from the *parameter names* rather than the values.
- **Re-entrancy shares the budget.** `Commands.CURRENT_EXECUTION_CONTEXT` is
  a thread-local: a command that starts another top-level execution appends
  to the running queue rather than making a new one, and the limits were
  read once, by the outermost call. Its top frame is nested one depth deeper,
  so its discards cannot eat the outer queue.

## Where to look

`ExecutionContext` and `Frame` first — thirty lines of each explain the
whole design. Then `BuildContexts` for how a parse becomes work, and
`ContinuationTask` for the laziness that both the fan-out and the function
body ride on. `CommandFunction` for the compiler and `MacroFunction` for the
only part of it that runs per call. `ServerFunctionManager` for where the
tick hooks in, and `ExecutionCommandSource` for why none of it names a
command source.

---

*Rules: names, never code · how the system works, not how the code reads ·
newest version only · every backticked name passes `tools/verify_names.py`.*
