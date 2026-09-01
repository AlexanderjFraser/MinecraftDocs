# Advancements

> Verified against **Minecraft 26.2** · Part XIII · "Stone Age": a cobblestone lands in an inventory, and one tick later the toast appears — through a listener set that only ever shrinks, and a packet that never says what the criterion was.

## Responsibility

An advancement is a data-pack-defined goal. It is also, and less obviously,
the game's general-purpose *"tell me when the player does X"* facility: the
recipe book is unlocked by advancements, `PlayerPredicate` reads advancement
progress back out as a loot condition, and every one of the sixty registered
triggers exists because something in the game wanted a hook and this was the
hook that already existed.

The design is worth stating before the classes, because it is the opposite
of what most people assume. There is **no global list of who is listening
for what**. Each player carries their own subscription table, it contains
only the criteria that player has *not yet satisfied*, and it shrinks
monotonically as they play. A veteran player is cheaper to run than a new
one.

The one sentence a player would recognise: *the yellow box in the corner
that says you have made an advancement.*

## The data it owns

The shared model lives in `net/minecraft/advancements`, the triggers in
`net/minecraft/advancements/triggers` and the predicates in
`net/minecraft/advancements/predicates`. All of it ships in both jars.

- **`Advancement`** — a record and the immutable definition: an optional
  parent id, an optional `DisplayInfo`, an `AdvancementRewards`, the
  criteria map, an `AdvancementRequirements`, and a
  `Advancement.sendsTelemetryEvent` flag. `Advancement.CODEC` is the
  data-pack form, `Advancement.STREAM_CODEC` the (much smaller) wire form,
  and `Advancement.validate` walks each criterion's trigger instance
  through a `ProblemReporter`.
- **`AdvancementHolder`** — the id plus the advancement. Its equality is **id-only**, which matters more than it looks: a map keyed
  by holder survives a data pack changing an advancement's contents without
  noticing.
- **`AdvancementNode`** and **`AdvancementTree`** — the parent/child graph.
  `AdvancementTree.addAll` is a fixed-point loop over
  `AdvancementTree.tryInsert`, which refuses any advancement whose declared
  parent is not yet a node; it sweeps until a pass inserts nothing and logs
  whatever is left. An orphan is **discarded**, not re-rooted.
  `AdvancementTree.Listener` is how the client's screen follows along, and
  `AdvancementTree.setListener` replays every existing root and task at the
  new listener immediately.
- **`Criterion`** and **`CriterionTrigger`** — a criterion is a trigger
  plus a decoded `CriterionTriggerInstance`, and nothing else; it has no
  name of its own, the name is the map key. `CriterionTrigger` has exactly
  two members, `CriterionTrigger.codec` and
  `CriterionTrigger.createCriterion` — the trigger object is **stateless**.
  `CriteriaTriggers` registers sixty of them into
  `BuiltInRegistries.TRIGGER_TYPES` over forty-four classes.
- **`SimpleCriterionTrigger`** — the base class for all but one; it owns
  `SimpleCriterionTrigger.trigger`, the sweep described below, and the
  nested `SimpleCriterionTrigger.SimpleInstance` which adds the optional
  *player* predicate every trigger instance may carry.
- **`AdvancementRequirements`** — a list of lists of criterion names: an
  **AND of ORs**. `AdvancementRequirements.allOf` is pure conjunction (the
  default when the JSON omits the field),
  `AdvancementRequirements.anyOf` pure disjunction, and
  `AdvancementRequirements.Strategy` is the two of them as constants.
  `AdvancementRequirements.size` counts *clauses*, not criteria.
- **`AdvancementProgress`** and **`CriterionProgress`** — the mutable
  half. A `CriterionProgress` is one nullable timestamp: that is the entire
  per-criterion state in the game. `AdvancementProgress.update` reconciles
  the criteria map against a requirements object, which is what lets the
  client rebuild progress from a definition it only half received.
- **`AdvancementRewards`** — experience, loot tables, recipes and an
  optional `CacheableFunction`. `AdvancementRewards.grant` gives the XP,
  rolls each table in the `LootContextParamSets.ADVANCEMENT_REWARD` context
  and adds or drops the stacks, calls `ServerPlayer.awardRecipesByKey`, and
  runs the function with output suppressed.
- **`DisplayInfo`** — title, description, an `ItemStackTemplate` icon, an
  optional background, an `AdvancementType` (the frame), and the toast /
  chat / hidden flags. It also carries mutable *x* and *y* coordinates, which are the
  surprise in the next section.
- **`TreeNodePosition`** — a full tidy-tree layout (three walks, threads,
  ancestors, shifts), run on the **server**, mutating those coordinates in
  place.
- **`PlayerAdvancements`** — the per-player state and the subscription
  table. `PlayerAdvancements.activeTriggers` is an identity map from
  trigger object to a map of `PlayerAdvancements.TriggerInstanceKey` (the
  advancement holder plus the criterion name) to the instance.
- **`ServerAdvancementManager`** — the reload listener; builds the holder
  map, builds a fresh tree, and runs the layout.
- **`AdvancementVisibilityEvaluator`** — the "how far past your frontier
  can you see" rule, with `AdvancementVisibilityEvaluator.VISIBILITY_DEPTH`
  of 2.

The predicates are not a parallel system: `ContextAwarePredicate` wraps a
list of `LootItemCondition` and evaluates them against a `LootContext`.
These are exactly the loot conditions of [loot tables](../items/loot-tables.md),
reached through `EntityPredicate.createContext`.

## When it runs

Everything server-side is on the server thread, and the whole cycle fits
inside one `ServerPlayer.tick`:

- `AbstractContainerMenu.broadcastChanges` runs at the *top* of the tick,
  which is where an inventory trigger fires;
- `CriteriaTriggers.TICK` fires mid-tick;
- `PlayerAdvancements.flushDirty` is the **last statement** of the tick.

So every award made anywhere in that tick — a pickup, a kill, an
`/advancement grant`, an item granted by another advancement's reward —
coalesces into a single packet at the end. The client handles that packet
on the render thread after the usual `PacketUtils.ensureRunningOnSameThread`.

Loading is the ordinary reload path ([the resource system](../foundations/resource-system.md)):
`ServerAdvancementManager` is a `SimpleJsonResourceReloadListener` over
`Registries.ADVANCEMENT`, so the JSON parse is off-thread and the apply —
including the tree build and the layout of every root — is on the reload's
main-thread executor.

## The trace: "Stone Age"

`minecraft:story/mine_stone` has one criterion, *get_stone*, whose trigger
is `minecraft:inventory_changed` and whose condition is a single
`ItemPredicate` over the `#minecraft:stone_tool_materials` tag. It has no
rewards at all.

```mermaid
sequenceDiagram
    participant M as AbstractContainerMenu
    participant SP as ServerPlayer
    participant T as InventoryChangeTrigger
    participant PA as PlayerAdvancements
    participant R as AdvancementRewards
    participant CPL as ClientPacketListener
    participant CA as ClientAdvancements

    M->>M: broadcastChanges — slot differs from lastSlots
    M->>SP: ContainerListener.slotChanged — which slot, which stack
    SP->>T: trigger(player, inventory, stack) — count the 43 slots first
    T->>T: SimpleCriterionTrigger.trigger — is anyone listening for this trigger?
    T->>T: TriggerInstance.matches — one predicate, so test only the changed stack
    T->>PA: award(mine_stone, "get_stone") — after the sweep, never during
    PA->>PA: unregisterListeners — the criterion is done, stop watching
    PA->>R: grant(player) — EMPTY here; XP, loot, recipes and a function otherwise
    PA->>PA: markForVisibilityUpdate — the root, not the advancement
    SP->>PA: flushDirty — last line of the tick
    PA->>PA: updateTreeVisibility — re-walk the whole story tree
    PA->>CPL: ClientboundUpdateAdvancementsPacket — added, removed, progress
    CPL->>CA: update — rebuild the tree, reconcile the progress
    CA->>CA: AdvancementToast — five seconds, and silent unless it is a CHALLENGE
```

Each arrow is a decision.

**Detection is a diff, not an event.** Nothing about advancements happens
when the item is picked up. `AbstractContainerMenu.broadcastChanges`
compares each slot against its remembered copy with `ItemStack.matches`
and reports the difference — the same mechanism that keeps the client's
inventory in sync ([containers and menus](../items/containers-and-menus.md)).
`ServerPlayer` filters out result slots and slots that are not the player's
own `Inventory` before firing.

**Counting comes before knowing whether anyone cares.**
`InventoryChangeTrigger.trigger` walks all forty-three slots to compute the
occupied, full and empty counts *before* it asks whether any criterion is
listening. That is the floor cost of every slot change of every player,
forever.

**The sweep is the cheap part.** `SimpleCriterionTrigger.trigger` fetches
this trigger's map from `PlayerAdvancements.getTriggerMapForType` and
returns immediately if it is null — and it is null once every criterion for
that trigger is satisfied, because `PlayerAdvancements.removeListener`
deletes the per-trigger map when it empties. When there is work, it builds
**one** `LootContext` and reuses it for the whole sweep, evaluates the
caller's cheap matcher first and the *player* predicate only for matches,
and does not allocate the results list until the first hit.

**Matches are collected, then awarded.** Awarding calls
`PlayerAdvancements.unregisterListeners`, which mutates the map being
iterated, so the sweep finishes before any award is made.

**Completion is checked against the requirements, not the criteria.**
`AdvancementRequirements.test` is the AND of ORs. Here it is one clause of
one name, so granting the criterion completes the advancement, which fires
the rewards, the chat announcement — gated on
`GameRules.SHOW_ADVANCEMENT_MESSAGES` — and the visibility dirty flag.

**Visibility is per root.** `PlayerAdvancements.markForVisibilityUpdate`
dirties the *root*, and the flush re-runs
`AdvancementVisibilityEvaluator` over that root's entire subtree. Finishing
one advancement in a large tree re-evaluates the whole tree; only the nodes
whose visibility actually flipped go on the wire.

## Interfaces

- **Called by:** roughly a hundred and forty gameplay sites, each calling
  one `CriteriaTriggers` constant. The busiest by far is
  `AbstractContainerMenu.broadcastChanges` via `ServerPlayer`'s container
  listener; `CriteriaTriggers.TICK` is the once-per-player-per-tick one.
- **Calls into:** the loot system for predicates and rewards
  ([loot tables](../items/loot-tables.md)), `ServerRecipeBook` through
  `ServerPlayer.awardRecipesByKey` ([recipes](../items/recipes.md)), and
  `ServerFunctionManager` for a reward function
  ([execution and functions](execution-and-functions.md)).
- **Crosses the network as:** `ClientboundUpdateAdvancementsPacket`
  (server → client; a reset flag, added holders, removed ids, a progress
  map and a "show advancements" flag), `ClientboundSelectAdvancementsTabPacket`
  (server → client, only when the value actually changed) and
  `ServerboundSeenAdvancementsPacket` (client → server).
- **Data-driven by:** `data/<ns>/advancement/<id>.json`, decoded by
  `Advancement.CODEC`. Per-player state is one JSON file at
  `players/advancements/<uuid>.json` (`LevelResource.PLAYER_ADVANCEMENTS_DIR`),
  data-fixed on load through `DataFixTypes.ADVANCEMENTS`.

## Invariants and surprises

- **The client is told the requirements but never the criteria.**
  `Advancement.read` reconstructs the record with an empty criteria map and
  `AdvancementRewards.EMPTY`. The only reason a client can render "3/7" is
  that `AdvancementRequirements` *is* on the wire and
  `AdvancementProgress.update` reconciles against it. A client cannot know
  what any criterion tests, or that an advancement grants anything at all.
- **Layout coordinates are computed on the server and shipped.**
  `TreeNodePosition` runs inside `ServerAdvancementManager` and mutates
  `DisplayInfo` in place; the the coordinates ride the packet. The advancements
  screen does no layout — it is drawing positions a data-pack reload
  decided. A root with no `DisplayInfo` is never laid out and never becomes
  a tab, and a display-less node in the middle of a tree is transparent:
  `TreeNodePosition` skips it and adopts its children.
- **The announce-to-chat flag is write-only on the wire.**
  `DisplayInfo.serializeToNetwork` packs three flags into an int and omits
  it; `DisplayInfo.fromNetwork` hard-codes it false. The decision is made
  entirely on the server. The client's copy is always a lie.
- **Progress is written only when the player is saved.** There is no write
  on award; `PlayerAdvancements.save` runs from `PlayerList.save`, on
  disconnect or a save-all. And `PlayerAdvancements.reload` — which runs
  for every cached player on `/reload` — clears the in-memory progress and
  **re-reads the file from disk**, so a `/reload` silently rolls back
  everything earned since the last save, and the client gets a full reset
  packet showing it.
- **The listener set only shrinks.** `PlayerAdvancements.registerListeners`
  subscribes only to criteria that are not yet done, in advancements that
  are not yet done; every award unsubscribes. The cost of the advancement
  system to a given player falls monotonically over that player's life.
- **`ImpossibleTrigger` has no trigger method at all.** It is the one
  trigger that implements `CriterionTrigger` directly, and it exists so an
  advancement can be granted *only* by command or by being a parent.
  Vanilla uses it for exactly one file: the invisible root of every recipe
  advancement. It has nothing to do with the `/trigger` command, which is a
  scoreboard feature.
- **The recipe book is unlocked by the advancement system.** Every recipe
  advancement is generated with a `RecipeUnlockedTrigger` criterion and an
  `AdvancementRewards` naming the recipe; earning it calls
  `ServerPlayer.awardRecipes`. `RecipeUnlockedTrigger` then closes the
  loop by letting other advancements observe an unlock — and it compares
  the recipe key by **reference identity**, which is safe only because
  `ResourceKey`s are interned.
- **An advancement with no requirement clauses is permanently
  incompletable.** `AdvancementRequirements.test` returns false outright
  for an empty list, rather than vacuously true.
- **`PlayerAdvancements.checkForAutomaticTriggers` is dead code.** It
  awards any advancement with an empty criteria map — but
  `Advancement.CODEC` rejects an empty criteria map, so nothing loadable
  can ever reach it. It runs a full pass over every advancement on every
  player load and every reload and can never do anything.
- **`ServerboundSeenAdvancementsPacket` has a "closed screen" action that
  the server ignores.** It is serialised, deserialised, and dropped.

## Where to look

`Advancement` and `AdvancementRequirements` for the model;
`PlayerAdvancements` for everything that actually happens — it is the only
class here with interesting state; `SimpleCriterionTrigger` and
`InventoryChangeTrigger` for the hot path;
`AdvancementVisibilityEvaluator` for the one rule nobody guesses right.

---

*Rules: names, never code · how the system works, not how the code reads ·
newest version only · every backticked name passes `tools/verify_names.py`.*
