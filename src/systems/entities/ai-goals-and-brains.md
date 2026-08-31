# AI: goals, brains and pathfinding

> Verified against **Minecraft 26.2** · Part VI · A villager's day — wake, claim a job site, work, socialise at the bell, walk home to bed — and the same machinery under a zombie that has none of it.

## Responsibility

Two decision systems coexist. The **goal selector** is the old one: a bag of
`Goal` objects, each asked every other tick whether it wants to run, with a
four-flag lock table deciding who wins. The **brain** is the newer one:
memories filled by sensors, behaviours grouped into activities, and one
activity active at a time. Every mob has both fields; most mobs use exactly
one of them. Below the waterline they are identical — both end at
`MoveControl.setWantedPosition`, and both get there through the same
pathfinder.

The one sentence a player recognises: *a zombie chases you because it keeps
re-asking "can I see a player"; a villager goes to bed at dusk because the
world told it what time it is.*

## The headline: schedules are gone

*Schedule* does not exist in 26.2. A `Brain` holds an
`EnvironmentAttribute` of `Activity` — a pointer into the *world*, not a
table on the mob — and `Brain.updateActivityFromSchedule` asks
`EnvironmentAttributeSystem` (reached through `Level.environmentAttributes`)
what that attribute's value is *at this position, at this time*. The value
comes from `EnvironmentAttributes.VILLAGER_ACTIVITY` or
`EnvironmentAttributes.BABY_VILLAGER_ACTIVITY`, whose keyframes live in a
data-pack `Timeline`: `Timelines.VILLAGER_SCHEDULE`, a 24000-tick loop whose
adult track reads *10 idle, 2000 work, 9000 meet, 11000 idle, 12000 rest*.

So the villager day is world data now, editable by a data pack, and — since
the lookup is positional — in principle able to differ by location. The
environment-attribute system is a page of its own; this one only asks it a
question.

## The data it owns

### Goals

- **`GoalSelector`** holds `GoalSelector.availableGoals` — an
  insertion-ordered set of `WrappedGoal`, never sorted — a lock table of
  `Goal.Flag` to the goal currently holding it, and a set of disabled flags.
  A `Mob` has two: `Mob.goalSelector` and `Mob.targetSelector`.
- **`Goal`** declares its flags (`Goal.Flag.MOVE`, `Goal.Flag.LOOK`,
  `Goal.Flag.JUMP`, `Goal.Flag.TARGET`) and answers `Goal.canUse`,
  `Goal.canContinueToUse`, `Goal.isInterruptable` and
  `Goal.requiresUpdateEveryTick`, with `Goal.start`, `Goal.tick` and
  `Goal.stop` as the lifecycle.
- **`WrappedGoal`** adds the priority and the running flag, and
  `WrappedGoal.canBeReplacedBy` is the arbitration rule: the incumbent must
  be interruptable and the challenger's priority number must be **lower**.
- Sixty-one goal classes plus ten targeting ones — `MeleeAttackGoal`,
  `RandomStrollGoal`, `LookAtPlayerGoal`, `FloatGoal`, `PanicGoal`,
  `TemptGoal`, `BreedGoal`, `OpenDoorGoal`, `NearestAttackableTargetGoal`,
  `HurtByTargetGoal` and the rest.
- **`Sensing`** — not to be confused with `Sensor` — is the goal system's
  line-of-sight memo, cleared once per tick and consulted by every goal that
  asks whether the mob can see something.

### Brains

- **`Brain`** holds: the memory map, the sensor map, and
  `Brain.availableBehaviorsByPriority`, a sorted map from priority to
  activity to behaviour set. Plus the schedule attribute, per-activity
  memory requirements, the core activities, the currently active ones and a
  default (`Activity.IDLE`).
- **Memories.** `MemoryModuleType` — 116 constants, of which **53 have a
  codec and are saved and 63 are transient**. The live cell is
  `MemorySlot` (value, time-to-live, tick-down); `ExpirableValue` is now
  only the serialisation shape. `MemoryStatus` is the three-way condition a
  behaviour states: `MemoryStatus.VALUE_PRESENT`,
  `MemoryStatus.VALUE_ABSENT`, `MemoryStatus.REGISTERED`.
- **Sensors.** `Sensor` self-throttles — `Sensor.DEFAULT_SCAN_RATE` is 20
  ticks, and `Sensor.randomlyDelayStart` staggers mobs at construction so
  they do not all scan on the same tick. `SensorType` has 24 constants.
  `GolemSensor` scans every 200 ticks, `SecondaryPoiSensor` every 40.
- **Behaviours.** `BehaviorControl` is the interface; `Behavior` is the
  timed abstract class (whose `Behavior.canStillUse` defaults to *false*, so
  a plain behaviour runs one tick unless it says otherwise); `OneShot` is
  the shape `BehaviorBuilder` produces, and `BehaviorBuilder` is the
  declarative front end where a behaviour *states* the memories it needs and
  gets its requirement set for free. Composites: `GateBehavior` with its
  `GateBehavior.OrderPolicy` and `GateBehavior.RunningPolicy`, and `RunOne`.
- **Activities.** `Activity` — 26 constants, `Activity.CORE`,
  `Activity.IDLE`, `Activity.WORK`, `Activity.PLAY`, `Activity.REST`,
  `Activity.MEET`, `Activity.PANIC`, `Activity.RAID`, `Activity.FIGHT`,
  `Activity.ADMIRE_ITEM`, `Activity.ROAR`, `Activity.DIG` and so on.
- **`ActivityData`** is new: a record of an activity, its prioritised
  behaviour list, its memory requirements and the memories to erase when it
  stops — returned **per body** by `Brain.ActivitySupplier`, which is how a
  villager's profession selects its work package at construction.
- **`Brain.Packed`** is the save shape, produced by `Brain.pack` and
  consumed by `Brain.Provider.makeBrain`.

Twenty-one classes override `LivingEntity.makeBrain`: `Villager`, `Allay`,
`Armadillo`, `Axolotl`, `Camel`, `Frog`, `Goat`, `Sniffer`, `Piglin`,
`PiglinBrute`, `Hoglin`, `Zoglin`, `Warden`, `Breeze`, `Creaking`,
`HappyGhast`, `CopperGolem` and the rest. Their behaviour packages are
`PiglinAi`, `WardenAi`, `FrogAi` and so on — with one exception:
`VillagerGoalPackages`, still named after goals, for the one mob that has
none.

### Pathfinding

- **`PathNavigation`** — the per-mob controller: the current `Path`, the
  speed modifier, stuck detection, the recompute cooldown
  (`PathNavigation.MAX_TIME_RECOMPUTE`, 20 ticks) and the node budget. Four
  subclasses: `GroundPathNavigation`, `WaterBoundPathNavigation`,
  `FlyingPathNavigation`, `AmphibiousPathNavigation`, plus
  `WallClimberNavigation`.
- **`PathFinder`** — plain A* over a `BinaryHeap`, bounded by a node count
  derived from `Attributes.FOLLOW_RANGE` × 16 and scaled by
  `PathNavigation.maxVisitedNodesMultiplier`.
- **`NodeEvaluator`** decides what a block *is* for walking:
  `WalkNodeEvaluator`, `SwimNodeEvaluator`, `FlyNodeEvaluator`,
  `AmphibiousNodeEvaluator`. The verdict is a `PathType` — 27 constants,
  each with a cost, and **a negative cost means impassable**, not expensive.
  Per-mob overrides live in `Mob.getPathfindingMalus` /
  `Mob.setPathfindingMalus`.
- **`PathTypeCache`** — a fixed 4096-entry cache owned by
  `ServerLevel.getPathTypeCache` and invalidated from
  `ServerLevel.sendBlockUpdated`; `PathfindingContext` only attaches it on a
  server level.
- **`PathNavigationRegion`** — a snapshot of chunk references around the
  search, built with `ChunkSource.getChunkNow`, so a path search never
  forces a chunk load and never blocks.

### Controls

`MoveControl` (and `FlyingMoveControl`, `SmoothSwimmingMoveControl`),
`LookControl`, `JumpControl`, `BodyRotationControl`. These are the only
things that actually turn a decision into rotation and speed.

## When it runs

Server main thread, all of it: there is not a single future, executor or
thread anywhere in the AI packages or the pathfinder, and every behaviour
and sensor entry point takes a `ServerLevel`. `Mob` only registers its goals
when the level is a server level, and `LivingEntity.aiStep` gates the whole
block on not being client-side. The client runs the debug renderers and
nothing else.

The order inside one mob tick, with the profiler section names, because they
are what a profile actually shows:

```
LivingEntity.aiStep → "ai"
  Mob.serverAiStep → "newAi"
    "sensing"        Sensing.tick — clear the line-of-sight memo
    "targetSelector" ┐ GoalSelector.tick on even (tickCount + id),
    "goalSelector"   ┘ tickRunningGoals only on odd
    "navigation"     PathNavigation.tick → "pathfind" / "find_path" on demand
    "mob tick"       Mob.customServerAiStep → "villagerBrain" → Brain.tick
    "controls"       "move" / "look" / "jump"
  "travel"           LivingEntity.travel — the body actually moves
"headTurn"           Mob.tickHeadTurn → BodyRotationControl.clientTick
```

**Goals are re-evaluated every *other* tick, staggered by entity id.** On
the off tick only goals that ask for it are ticked at all. `Brain.tick`
runs in four fixed phases: expire memories, tick sensors, try to start every
non-running behaviour in priority order, tick the running ones.

## The trace: a villager's day

```mermaid
sequenceDiagram
    participant EA as EnvironmentAttributeSystem
    participant BR as Brain
    participant AP as AcquirePoi
    participant PM as PoiManager
    participant MT as MoveToTargetSink
    participant NAV as PathNavigation
    participant MC as MoveControl
    participant SB as SleepInBed

    BR->>EA: updateActivityFromSchedule(system, gameTime, position)
    EA-->>BR: Timelines.VILLAGER_SCHEDULE → Activity at this tick
    BR->>BR: setActiveActivityIfPossible — requirements met? else IDLE
    AP->>PM: findAllClosestFirstWithType(job sites, 48, HAS_SPACE)
    AP->>NAV: createPath to the five best — reachable?
    AP->>PM: take(pos) → Brain.setMemory(JOB_SITE, GlobalPos)
    BR->>MT: WALK_TARGET present, PATH absent → createPath → moveTo
    NAV->>MC: tick → setWantedPosition(next node, speed)
    MC->>MC: setYRot · setSpeed · maybe JumpControl.jump
    BR->>SB: dusk: REST → SleepInBed → startSleeping, LAST_SLEPT
```

1. **Construction.** `LivingEntity.makeBrain` is called with an empty
   `Brain.Packed`, or with the packed memories read from disk.
   `Brain.Provider.makeBrain` asks `Brain.ActivitySupplier` for this
   villager's activity list — the work package depends on the profession, so
   the list is per-body — registers the nine villager sensors, auto-registers
   every memory the sensors and behaviours declare, replays the saved
   memories, sets `Activity.CORE` as always-on and defaults to
   `Activity.IDLE`. Then the schedule attribute is attached and consulted
   once.
2. **Dawn.** The rest package's schedule behaviour (priority 99 — the last
   thing tried) flips the activity to `Activity.IDLE`; the core `WakeUp`
   behaviour sees the villager still sleeping outside `Activity.REST` and
   calls `LivingEntity.stopSleeping`.
3. **Claiming a job site.** `AcquirePoi` runs from the core package. It asks
   `PoiManager.findAllClosestFirstWithType` for free points of interest
   matching the profession within 48 blocks
   ([points of interest](../world/game-events-and-poi.md)), takes the best
   five, and **pathfinds to each** — only a POI the villager can actually
   *reach* is claimed with `PoiManager.take` and written to
   `MemoryModuleType.JOB_SITE`. Failures go into a jittered retry list so
   they are not re-tried every scan. `AssignProfessionFromJobSite` turns a
   potential site into a profession; `PoiCompetitorScan` compares experience
   between two villagers claiming the same block and erases the loser's
   memory; `ValidateNearbyPoi` erases it if the block is gone.
4. **Work.** At tick 2000 the schedule says `Activity.WORK`, and the brain
   checks that activity's requirement — `MemoryModuleType.JOB_SITE` present.
   With no job site the switch silently fails and the villager falls back to
   the default activity; with one, the work package runs a weighted
   `RunOne` over `WorkAtPoi` (or `WorkAtComposter`), `StrollAroundPoi`,
   `StrollToPoi`, `HarvestFarmland` and `UseBonemeal`. `WorkAtPoi` needs 300
   ticks since the last check and to be within 1.73 blocks of the
   workstation; it writes `MemoryModuleType.LAST_WORKED_AT_POI`, plays the
   work sound and restocks trades.
5. **Walking anywhere.** `SetWalkTargetFromBlockMemory` turns a remembered
   position into `MemoryModuleType.WALK_TARGET`. The core `MoveToTargetSink`
   — whose entry condition is *walk target present, path absent* — calls
   `PathNavigation.createPath`, which builds a `PathNavigationRegion` around
   the mob and runs `PathFinder.findPath` inside the *pathfind* profiler
   section. The resulting `Path` goes into `MemoryModuleType.PATH` and into
   the navigation. Every tick after that, `PathNavigation.tick` advances to
   the next node and calls `MoveControl.setWantedPosition` — **the single
   line where any decision, goal or brain, becomes movement.**
   `InteractWithDoor` opens doors on the way and remembers to close them.
6. **The bell.** At 9000 the schedule says `Activity.MEET`, gated on
   `MemoryModuleType.MEETING_POINT`, which the core `AcquirePoi` supplies
   from the bell. The meet package strolls around the bell, socialises,
   shows trades to nearby players and gives gifts to a raid hero. At 11000
   it returns to idle: interacting with other villagers, breeding, jumping
   on beds, doing nothing.
7. **Bed.** At 12000 the activity is `Activity.REST`, which has no memory
   requirement and therefore always takes. The rest package walks to
   `MemoryModuleType.HOME` and runs `SleepInBed`, which needs a bed within
   two blocks, unoccupied, in the right dimension, and at least 100 ticks
   since it was last woken. It closes the doors it opened, calls
   `LivingEntity.startSleeping`, records the time and clears the walk
   target. `SleepInBed` never times out — it ends because
   `Brain.isActive` for `Activity.REST` goes false at dawn. A villager with
   no home instead wanders towards the nearest village.
8. **Interruptions.** `HurtBySensor`, `VillagerHostilesSensor` and
   `GolemSensor` fill their memories at their own scan rates;
   `VillagerPanicTrigger` in the core package switches the activity to
   `Activity.PANIC`. The panic package deliberately has **no** schedule
   behaviour, so the clock cannot reclaim the villager until it calms down.

### The zombie, in one paragraph

A `Zombie` has a `Brain` — the field is never null — but it is empty, with
no sensors, memories or behaviours, and it reports itself brain-dead.
Everything it does comes from `Mob.registerGoals`, called once in the
constructor: an attack goal, a move-through-village goal, a stroll goal and
two look goals in `Mob.goalSelector`; a hurt-by-target goal and four
nearest-attackable-target goals in `Mob.targetSelector`. Every other tick,
every goal's `Goal.canUse` is re-asked and the flag table decides: the
target goal holds `Goal.Flag.TARGET` and writes `Mob.setTarget`, the attack
goal holds `Goal.Flag.MOVE` and `Goal.Flag.LOOK` and drives the navigation,
the look goals want `Goal.Flag.LOOK` and lose to it on priority. No
activity, no schedule, nothing persisted, and nothing the world can push
into it — the zombie's state is a handful of running flags and one target
field. Below that line it is the same navigation, the same move control, the
same physics.

## Interfaces

- **Called by:** `Mob.serverAiStep` for the selectors, the navigation and
  the controls; `Mob.customServerAiStep` for the brain (each brain mob
  pushes its own profiler section); `Mob.tickHeadTurn` for body rotation;
  `ServerLevel.sendBlockUpdated`, which invalidates the path-type cache and
  asks every mob in `ServerLevel.navigatingMobs` whether the changed block
  is near its path — the one place the world pushes into AI.
- **Calls into:** `MoveControl.setWantedPosition` → `LivingEntity.travel`
  ([movement](movement-and-collision.md)); `PoiManager`
  ([points of interest](../world/game-events-and-poi.md)); `Mob.setTarget`
  and, for damage, the paths in [damage and death](damage-and-death.md);
  `Attributes.FOLLOW_RANGE` and `Attributes.TEMPT_RANGE`
  ([attributes](attributes.md)).
- **Crosses the network as:** *nothing*. There is no AI packet. What the
  client sees are consequences — `ClientboundRotateHeadPacket`,
  `ClientboundSetEntityMotionPacket`, position deltas, pose changes, and the
  occasional entity-event byte for particles. `Path` does have a stream
  codec, but only for the debug channel: `DebugSubscriptions.BRAINS`,
  `DebugSubscriptions.GOAL_SELECTORS`, `DebugSubscriptions.ENTITY_PATHS`
  and `DebugSubscriptions.POIS`, registered from `Mob.registerDebugValues`,
  and the pathfinder only retains its open and closed sets when someone is
  subscribed.
- **Data-driven by:** the villager day (`Timelines.VILLAGER_SCHEDULE` in
  `Registries.TIMELINE`); `VillagerProfession` and `VillagerType`;
  `PoiType`; trades (Part VII). **Behaviours and goals are code** — plain
  Java lists in `VillagerGoalPackages` and the `*Ai` classes, not
  registered, not addressable from data. `Activity`, `MemoryModuleType` and
  `SensorType` are code registries too.

## Invariants and surprises

- **Goals are re-evaluated, not sequenced.** There is no state machine. The
  only persistent state is which goals are running and which flags are held.
- **The flag table, not the priority list, is the arbiter.** The goal set is
  insertion-ordered and never sorted; priority only decides who wins a
  contested flag. Two goals with no shared flag run at once whatever their
  priorities; two with a shared flag never do. Lower number wins, and a
  non-interruptable goal cannot be replaced at all.
- **An activity is a filter, not a mode.** The brain's active set is always
  the core activities plus exactly one other, so `Activity.CORE` behaviours
  run at every hour and the day only swaps the second half.
- **A schedule change that fails its requirements falls back silently.** A
  jobless villager is not "off schedule"; it is idle by construction.
- **The schedule only advances when a behaviour asks it to**, at most once
  every 20 ticks, from a behaviour sitting at priority 99 in every
  non-emergency package. Panic and hide packages omit it — which is exactly
  how they pin the villager.
- **Memories expire on the brain's clock**, and only the 53 with a codec
  survive a save. Reading a memory the brain never registered throws;
  declaring it in a behaviour or sensor is what registers it.
- **`AcquirePoi` pathfinds before it claims.** A job site is not a distance
  query — a bell across a ravine is invisible to a villager.
- **Pathfinding is synchronous, bounded and load-free.** One A* call on the
  tick thread, capped by the follow-range-derived node budget, reading only
  already-loaded chunks. A recompute is refused more often than every 20
  ticks and deferred to the next tick instead.
- **`BodyRotationControl.clientTick` runs on the server.** The name is a
  leftover; it is called from the head-turn section of the server tick, and
  it is what makes a mob's body swing to follow its head after ten stable
  ticks.
- **Six shared static targeting conditions are re-ranged on every sensor
  fire.** Every brain mob in the world uses the same objects — correct only
  because AI is strictly single-threaded, and a good demonstration that it
  is.
- **`Mob.getTarget` is a filtered read, not a field read**, re-validating
  every call; brain mobs source it from `Mob.getTargetFromBrain` and the
  attack-target memory instead.
- **`VillagerGoalPackages` is genuinely the 26.2 name** — the sole survivor
  of the old convention, on the one mob with no goals at all.

## Where to look

`GoalSelector` · `Goal` · `Goal.Flag` · `WrappedGoal` · `Sensing` ·
`Mob.serverAiStep` · `Mob.registerGoals` · `Brain` · `Brain.tick` ·
`Brain.Provider` · `Brain.Packed` · `ActivityData` · `Activity` ·
`MemoryModuleType` · `MemorySlot` · `Sensor` · `SensorType` ·
`BehaviorControl` · `Behavior` · `OneShot` · `BehaviorBuilder` ·
`GateBehavior` · `VillagerGoalPackages` · `AcquirePoi` · `WorkAtPoi` ·
`SleepInBed` · `MoveToTargetSink` · `PathNavigation` · `PathFinder` ·
`NodeEvaluator` · `PathType` · `PathTypeCache` · `PathNavigationRegion` ·
`MoveControl` · `BodyRotationControl` · `TargetingConditions`

---

*Rules: names, never code · how the system works, not how the code reads ·
newest version only · every backticked name passes `tools/verify_names.py`.*
