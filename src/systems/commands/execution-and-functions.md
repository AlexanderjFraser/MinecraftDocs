# Execution and functions

> Verified against **Minecraft 26.2** · Part XIII · A `#minecraft:tick` function runs `execute as @a at @s run …`: a command engine with no Java recursion, a fork that materialises one player at a time, and a `/return` that deletes work out of a queue rather than unwinding a stack.

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

- **`ExecutionContext`** — one per outermost command or function call. It
  owns `ExecutionContext.commandQueue`, `ExecutionContext.newTopCommands`
  (the staging list), the budget (`ExecutionContext.commandQuota` counting
  down from `ExecutionContext.commandLimit`), `ExecutionContext.forkLimit`,
  the profiler, an optional `TraceCallbacks`, and
  `ExecutionContext.MAX_QUEUE_DEPTH` — ten million, the hard cap.
  `ExecutionContext.runCommandQueue` is the driver loop.
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
  "return an int". `/function`, `/return` and `execute if function` are all
  one of these. Their adapter nestings
  implement Brigadier's interfaces with methods that throw, purely so the
  node is registerable.
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
- **`ServerFunctionLibrary`** — the reload listener; holds the volatile
  function and tag maps and the compile-time `PermissionSet`.
- **`ServerFunctionManager`** — the runtime face:
  `ServerFunctionManager.TICK_FUNCTION_TAG`,
  `ServerFunctionManager.LOAD_FUNCTION_TAG`, and
  `ServerFunctionManager.getGameLoopSender`, the source those functions run
  as.
- **`CommandResultCallback`** — a success flag and an integer. This pair is
  what "the result of a command" means everywhere in the game.

## When it runs

`ServerFunctionManager.tick` runs from the server's tick, in a profiler
section of its own, **before any level ticks** — after connections and
players, before the clock and the worlds. It no-ops entirely when the tick
rate manager is not running normally, so `/tick freeze` suspends data
packs. `#minecraft:load` runs once after a reload or start; `#minecraft:tick`
runs every tick from a list snapshotted at reload.

Each function in a tag gets its **own** `ExecutionContext`, so the budget is
per function, not shared across the tag.

Scheduled functions are elsewhere: `/schedule` puts a callback in the
server's timer queue (saved data), which is ticked from a level's own tick,
right after the game time advances.

**Compilation is not on the server thread.** `ServerFunctionLibrary`
parses every `.mcfunction` in parallel on the reload's background executor,
against a compilation source with a null level and a null server; only the
map swap happens on the main thread, which is why those maps are volatile.

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
    CF->>BC: schedule one entry per function line, all sharing that frame
    BC->>BC: walk the stages — "as @a" forks, one cost unit for the whole stage
    BC->>BC: "at @s" moves each source; the forked flag is now set for good
    BC->>CT: reaching the execute stage, schedule the fan-out
    CT->>XC: emit the entry for one source, then re-queue itself behind it
    XC->>XC: spend a cost unit, run the executable, report to the tracer
    CT->>CT: ...and only now is the next player materialised
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
N-element one. Only `CallFunction` and `IsolatedCall` open frames.

**The fan-out is lazy.** For three or more sources, exactly **one** entry is
queued: a `ContinuationTask` that emits the entry for the current source and
then re-queues itself. Because the staging list preserves order, the
per-source entry lands ahead of the self-entry, so source *i* and
everything it spawns runs to completion before source *i+1* is even
materialised. The queue cost is constant in N — and a `/return` mid-fork
discards the self-entry too, which is why returning inside a fork stops the
remaining players from being processed at all.

**Discarding is "depth ≥ d, from the head".** Because the queue is
depth-first, entries deeper than a frame are always in front of that
frame's remaining entries. So popping from the head while the depth is at
least *d* removes exactly the callee's pending work plus the rest of this
frame's body, and nothing older. Depth-zero frames are special: their
control clears the whole queue.

**There is one budget and it is spent in three places.** A cost unit goes
on each ordinary modifier stage, each function call, and each executed
command. When it runs out the loop logs at info and abandons the rest of
the queue — **with no message to the player**.

## `/return`, and what a result is

`/return` does not unwind. `Frame.returnSuccess` pushes the value sideways
into the callback the caller installed on that frame, and `Frame.discard`
splices the abandoned work out of the queue. There is no search and no
exception.

Who installed that callback decides where the value goes.
`ExecutionContext.queueInitialFunctionCall` gives the outermost frame the
caller's callback and `CallFunction` passes it down;
`CallFunction.returnParentFrame` decides whether a `/return` inside also
unwinds the caller. `/return run` chains the inner frame's consumer onto the
outer one's — which is how a value climbs out — and deliberately keeps only
the first source, because a return has one value.

The result of a command is always a pair: a **success flag** and an
**integer**. There is no aggregation anywhere in the engine. A fork over N
players delivers N independent results to N sources, so an `execute store
result` writes N times and the last one wins — there is no success count. A
sum exists in exactly one place: `/function` on a *tag*, and only when the
caller installed a real callback.

A typed command's result is discarded entirely: the chat path passes an
empty callback and returns nothing.

## Functions, compiled and instantiated

A `.mcfunction` file becomes a runnable thing in two steps, and the second
one usually does nothing.

**Compile, at reload.** `CommandFunction.fromLines` walks the lines: a
trailing backslash joins the next line; blanks and `#` comments are
skipped; a leading `/` is a hard error with two different messages
depending on whether you wrote one slash or two; a leading `$` is a macro
line; anything else is parsed by `CommandFunction.parseCommand` into a
`BuildContexts.Unbound` — **a compiled function line is literally a parsed
context chain plus its input string, waiting for a source.** A syntax error
on any line fails the whole file, which is then simply absent from the map.

**Instantiate, per call.** A macro-free function returns itself. A
`MacroFunction` looks up each declared parameter in the argument compound,
stringifies it, and uses the ordered list of strings as a cache key over an
eight-entry LRU. On a miss it substitutes into every macro line and
**re-parses** it, and on a parse failure raises an instantiation exception.

Stringification is worth knowing because it is where macros surprise
people: floats and doubles go through a decimal format with up to fifteen
fraction digits (so `1.0` becomes `1`), the integral types become bare
numbers, a string tag yields its *unquoted* value, and everything else —
including compounds and lists — falls through to SNBT.

One `$` line anywhere makes the whole file a macro function, though the
non-macro lines keep their already-compiled form and are never re-parsed.
And a `$` line containing no substitution at all is a **load-time error**,
not a plain command.

## Interfaces

- **Called by:** `Commands.performCommand` for every typed command;
  `ServerFunctionManager.tick` for the two function tags; the timer queue
  for `/schedule`; `AdvancementRewards` for a reward function
  ([advancements](advancements.md)); an enchantment effect; a game test's
  environment setup ([dialogs and tests](dialogs-and-tests.md)).
- **Calls into:** every command in the game, and through them everything
  else.
- **Crosses the network as:** nothing. Execution is entirely server-side;
  only the *effects* of commands produce packets.
- **Data-driven by:** `data/<ns>/function/*.mcfunction` and
  `data/<ns>/tags/function/*.json` — both **singular** directory names.
  `#minecraft:tick` and `#minecraft:load` are the two hooks. The budgets
  are game rules; the compile-time permission set is a server property.

## Invariants and surprises

- **A function cannot yield.** Work it queues drains inside the same
  driver loop, in the same tick, before the call returns. The
  only escape is `/schedule`.
- **Depth is not bounded.** There is no recursion limit and no depth game
  rule. Recursion is bounded transitively by the cost budget, and fan-out
  by the ten-million queue cap. Depth is only used to order discards and to
  indent the tracer.
- **The budget is spent, not counted.** The method that decrements the
  quota is named as though it increments a cost. When the quota runs out
  the remaining queue is dropped silently — no player-visible message, one
  info line in the log.
- **The fork limit is checked per contributing source, with a
  greater-or-equal comparison**, so the effective ceiling is one below the
  configured value.
- **Conditionals are fork nodes.** `execute at @s`, `execute if block` and
  friends set the forked flag for the rest of the chain — and a forked
  source **suppresses failure messages**. Putting a harmless-looking conditional
  in front of a command silently converts its errors into nothing. They
  still reach the tracer, which is what `/debug function` is for.
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
  type that dereferences the world during parsing would break a reload.
  It is why the function argument type reads only an id and defers the
  lookup.
- **A macro function's instantiated variants all share one synthetic id**,
  derived from the *parameter names* rather than the values.
- **Re-entrancy shares the budget.** The current context is a thread-local:
  a command that starts another top-level execution appends to the running
  queue rather than making a new one, and the limits were read once, by the
  outermost call.
- **A sequence step throws as ordinary control flow** in the neighbouring
  test framework, and this engine has its own version of the same idea: the
  fallthrough marker exists so a frame that produced no value fails rather
  than returning nothing.

## Where to look

`ExecutionContext` and `Frame` first — thirty lines of each explain the
whole design. Then `BuildContexts` for how a parse becomes work, and
`ContinuationTask` for the fan-out. `CommandFunction` for the compiler and
`MacroFunction` for the only part of it that runs per call.
`ServerFunctionManager` for where the tick hooks in.

---

*Rules: names, never code · how the system works, not how the code reads ·
newest version only · every backticked name passes `tools/verify_names.py`.*
