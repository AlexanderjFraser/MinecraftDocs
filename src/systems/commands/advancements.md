# Advancements

> Verified against **Minecraft 26.2** · Part XIII · "Stone Age": a cobblestone lands in an inventory, and one tick later the toast appears — through a listener set that (almost) only ever shrinks, and a packet that never says what the criterion was.

## Responsibility

An advancement is a data-pack-defined goal. It is also, and less obviously,
the game's general-purpose *"tell me when the player does X"* facility: the
recipe book is unlocked by advancements, `PlayerPredicate` reads advancement
progress back out as a loot condition, and every one of the fifty-eight
registered triggers exists because something in the game wanted a hook and
this was the hook that already existed.

The design is worth stating before the classes, because it is the opposite
of what most people assume. There is **no global list of who is listening
for what**. Each player carries their own subscription table, it contains
only the criteria that player has *not yet satisfied*, and it shrinks as
they play. A veteran player is cheaper to run than a new one.

The one sentence a player would recognise: *the yellow box in the corner
that says you have made an advancement.*

## The data it owns

The shared model lives in `net/minecraft/advancements`, the triggers in
`net/minecraft/advancements/triggers` and the predicates in
`net/minecraft/advancements/predicates` (with the entity half a level down,
in `advancements/predicates/entity`). All 112 classes ship in both jars.

- **`Advancement`** — a record and the immutable definition: an optional
  parent id, an optional `DisplayInfo`, an `AdvancementRewards`, the
  criteria map, an `AdvancementRequirements`, a
  `Advancement.sendsTelemetryEvent` flag, and a seventh component most
  readers miss — a pre-rendered display name, built in the compact
  constructor, which is the `[Title]` with hover text that every chat
  announcement and command message quotes. `Advancement.CODEC` is the
  data-pack form, `Advancement.STREAM_CODEC` the (much smaller) wire form.
  There are two `Advancement.validate`s: a private static one the codec runs,
  which cross-checks the requirements against the criteria and **fails the
  load**, and a public one that walks each criterion's trigger instance
  through a `ProblemReporter` and only *warns*.
- **`AdvancementHolder`** — the id plus the advancement. Its equality is
  **id-only**, which matters more than it looks: a map keyed by holder
  survives a data pack changing an advancement's contents without noticing.
- **`AdvancementNode`** and **`AdvancementTree`** — the parent/child graph.
  `AdvancementTree.addAll` is a fixed-point loop over
  `AdvancementTree.tryInsert`, which refuses any advancement whose declared
  parent is not yet a node; it sweeps until a pass inserts nothing and logs
  whatever is left. An orphan is **discarded**, not re-rooted.
  `AdvancementTree.remove` is the recursive counterpart the client uses for
  the packet's removed ids, and `AdvancementNode.children` is an unordered
  hash set — so sibling layout order is hash-dependent, in a tidy-tree
  algorithm. `AdvancementTree.Listener` is how the client's screen follows
  along, and `AdvancementTree.setListener` replays every existing root and
  task at the new listener immediately.
- **`Criterion`** and **`CriterionTrigger`** — a criterion is a trigger
  plus a decoded `CriterionTriggerInstance` (which, alone among these, lives
  in `net/minecraft/advancements` rather than the triggers package), and
  nothing else; it has no name of its own, the name is the map key.
  `Criterion.CODEC` dispatches on a *trigger* field and reads the rest from a
  *conditions* field — the JSON shape a pack author writes.
  `CriterionTrigger` has exactly two members, `CriterionTrigger.codec` and
  `CriterionTrigger.createCriterion` — the trigger object is **stateless**.
  `CriteriaTriggers` registers **fifty-eight** of them into
  `BuiltInRegistries.TRIGGER_TYPES` over **forty-four** classes; the gap is
  re-use, `PlayerTrigger` alone accounting for six registrations.
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
  `AdvancementProgress.getProgressText` returns nothing at all when there is
  one clause, which is why a single-criterion advancement never shows "1/1".
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
  advancement holder plus the criterion name) to the instance. Three more
  sets do the wire bookkeeping: `PlayerAdvancements.visible`,
  `PlayerAdvancements.progressChanged` and `PlayerAdvancements.rootsToUpdate`.
- **`ServerAdvancementManager`** — the reload listener; builds the holder
  map (with a duplicate id aborting the reload outright), builds a fresh
  tree, and runs the layout.
- **`AdvancementVisibilityEvaluator`** — the "how far past your frontier
  can you see" rule, with a depth of two.

## The predicate library

`ContextAwarePredicate` wraps a list of `LootItemCondition` and evaluates
them against a `LootContext`, so a trigger's conditions are exactly the loot
conditions of [loot tables](../items/loot-tables.md), reached through
`EntityPredicate.createContext`. That is the whole of the connection, and it
is where most descriptions of the system stop — but the predicates are not
just a catalogue. Four shapes carry the weight, and each recurs everywhere in
the data-driven half of the game:

- **`MinMaxBounds`** — the numeric-range primitive, with both a codec and a
  `StringReader` grammar, so `3..7` means the same thing in a predicate, in
  an entity selector and in `/random`. It is the most-reused type in the
  package and the one a pack author meets first.
- **Collection matching** — `CollectionPredicate` composes
  `CollectionContentsPredicate` and `CollectionCountsPredicate`, giving one
  generic "N of these match" combinator that the item, slot and effect
  predicates all instantiate rather than reimplementing.
- **Registry-dispatched extension** — `EntitySubPredicate` and
  `EntitySubPredicates` make a per-mob test a *registry element* instead of a
  code branch, which is why the twenty-odd small entity predicates
  (`SheepPredicate`, `RaiderPredicate`, `VehiclePredicate`, …) are each a
  record and a codec and nothing else.
- **Component matching** — `DataComponentMatchers` is how `ItemPredicate`
  tests a stack's data components without knowing what any of them are
  ([data components](../foundations/data-components.md)).

Two details worth knowing because they change behaviour rather than shape.
`EntityPredicate.ADVANCEMENT_CODEC` accepts *either* a condition list or a
bare entity predicate, which is why vanilla's JSON writes the short form.
And `EntityPredicate` declares an explicit type-check-first, NBT-last
ordering for its own sub-tests: a real performance invariant hiding in a
predicate class.

## When it runs

Everything server-side is on the server thread, and the interesting part of
the cycle fits inside one `ServerPlayer.tick`:

- `AbstractContainerMenu.broadcastChanges` is the fifth statement, which is
  where an inventory trigger fires;
- `CriteriaTriggers.TICK` fires mid-tick;
- `PlayerAdvancements.flushDirty` is the **last statement** of the tick.

So every award made between those two points — a pickup, a kill, an
`/advancement grant`, an item granted by another advancement's reward —
coalesces into a single packet at the end. So does everything that arrived
in a packet, because `MinecraftServer.processPacketsAndTick` drains the
inbound queue before the levels tick at all.

But `ServerPlayer.tick` is not the last thing that happens to a player in a
server tick, and the corollary is a real one-tick delay.
`ServerGamePacketListenerImpl.tick` calls `ServerPlayer.doTick` during the
*connection* phase, which in 26.2 runs **after** the levels
([the server tick](../server/server-tick.md)) — i.e. after `PlayerAdvancements.flushDirty` has
already run. `CriteriaTriggers.LOCATION`, which fires there every twenty
ticks and is what most vanilla biome and structure advancements hang on,
therefore always lands in the *next* tick's packet. The client handles that
packet on its own thread after the usual
`PacketUtils.ensureRunningOnSameThread`.

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
    T->>T: SimpleCriterionTrigger.trigger — is this player listening for this trigger?
    T->>T: TriggerInstance.matches — one predicate, so test only the changed stack
    T->>PA: award(mine_stone, "get_stone") — after the sweep, never during
    PA->>PA: unregisterListeners — the criterion is done, stop watching
    PA->>R: grant(player) — EMPTY here; XP, loot, recipes and a function otherwise
    PA->>PA: markForVisibilityUpdate — the root, not the advancement
    SP->>PA: flushDirty — last line of the tick
    PA->>PA: updateTreeVisibility — re-walk the whole story tree
    PA->>CPL: ClientboundUpdateAdvancementsPacket — added, removed, visible progress
    CPL->>CA: update — rebuild the tree, reconcile the progress
    CA->>CA: AdvancementToast — and silent unless it is a CHALLENGE
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
`InventoryChangeTrigger.trigger` walks all forty-three slots (thirty-six
inventory plus seven equipment) to compute the occupied, full and empty
counts *before* it asks whether any criterion is listening. That is the floor
cost of every slot change of every player, forever — and it is the most
expensive trigger per fire, though `CriteriaTriggers.TICK` is by far the most
*frequent*, since it fires unconditionally twenty times a second per player.

**The sweep is the cheap part.** `SimpleCriterionTrigger.trigger` fetches
this trigger's map from `PlayerAdvancements.getTriggerMapForType` and
returns immediately if it is null — and it is null once every criterion for
that trigger is satisfied, because `PlayerAdvancements.removeListener`
deletes the per-trigger map when it empties. When there is work, it builds
**one** `LootContext` and reuses it for the whole sweep, evaluates the
caller's cheap matcher first and the *player* predicate only for matches,
and does not allocate the results list until the first hit. Note the scope:
one player. Nothing here is a broadcast.

**Matches are collected, then awarded.** Awarding calls
`PlayerAdvancements.unregisterListeners`, which mutates the map being
iterated, so the sweep finishes before any award is made.

**Completion is checked against the requirements, not the criteria.**
`AdvancementRequirements.test` is the AND of ORs. Here it is one clause of
one name, so granting the criterion completes the advancement, which fires
the rewards, the chat announcement — built by
`AdvancementType.createAnnouncement`, broadcast to every player, gated on
`GameRules.SHOW_ADVANCEMENT_MESSAGES` — and the visibility dirty flag.

**Visibility is per root, and it gates the wire.**
`PlayerAdvancements.markForVisibilityUpdate` dirties the *root*, and the
flush re-runs `AdvancementVisibilityEvaluator` over that root's entire
subtree. Finishing one advancement in a large tree re-evaluates the whole
tree; only the nodes whose visibility actually flipped go on the wire. And
`PlayerAdvancements.flushDirty` sends progress **only for advancements in
`PlayerAdvancements.visible`**, so progress on something hidden or beyond
your frontier accumulates server-side and reaches the client the moment it
becomes visible.

## The screen at the other end

The client's half is six classes and about eleven hundred lines
(`net/minecraft/client/gui/screens/advancements`), and it is the payoff for
the server-side layout. `ClientAdvancements` consumes
`AdvancementTree.Listener`; `AdvancementsScreen` owns the tab strip;
`AdvancementTab` owns one root's pan-and-scroll bounds, auto-centres on
first render and clamps the drag; `AdvancementWidget` scales the
server-decided coordinates by a fixed factor, draws the connector lines to
its parent, and wraps its own tooltip text. `AdvancementTabType` is the one
with a hard limit in it: four header geometries with room for eight tabs
above, eight below and five on each side, so a data pack's **twenty-seventh
root is silently unreachable**.

## Interfaces

- **Called by:** seventy-nine gameplay sites across forty-nine files, each
  calling one `CriteriaTriggers` constant. The most frequent is
  `CriteriaTriggers.TICK`, once per player per tick; the most expensive is
  `AbstractContainerMenu.broadcastChanges` via `ServerPlayer`'s container
  listener. `AdvancementCommands` is the only *write* interface besides
  gameplay.
- **Calls into:** the loot system for predicates and rewards
  ([loot tables](../items/loot-tables.md)), `ServerRecipeBook` through
  `ServerPlayer.awardRecipesByKey` ([recipes](../items/recipes.md)), and
  `ServerFunctionManager` for a reward function
  ([execution and functions](execution-and-functions.md)).
- **Crosses the network as:** `ClientboundUpdateAdvancementsPacket`
  (server → client; a reset flag, added holders, removed ids, a progress
  map and a "show advancements" flag), `ClientboundSelectAdvancementsTabPacket`
  (server → client, only when the value actually changed, and only for a
  root that has a display) and `ServerboundSeenAdvancementsPacket`
  (client → server).
- **Data-driven by:** `data/<ns>/advancement/<id>.json`, decoded by
  `Advancement.CODEC`. Per-player state is one JSON file at
  `players/advancements/<uuid>.json` (`LevelResource.PLAYER_ADVANCEMENTS_DIR`),
  data-fixed on load through `DataFixTypes.ADVANCEMENTS`.

## The command

`AdvancementCommands` is 312 lines and does more than grant a flag.
`AdvancementCommands.Mode` — *only*, *through*, *from*, *until*,
*everything* — is a graph traversal over the tree node, collecting parents or
children or both; the grant and revoke actions then iterate each collected
advancement's criteria by name. Two behaviours are worth naming:

- **A no-op is a hard failure.** Granting an advancement the player already
  has throws rather than reporting zero, so `/advancement` in a function is a
  usable conditional.
- **`/advancement grant … everything` flushes three times.** It calls
  `PlayerAdvancements.flushDirty` before the loop and again after, both with
  the packet's "show advancements" flag **false** — which is the only purpose
  that flag has, and it exists to suppress a toast storm.

## Invariants and surprises

- **The client is told the requirements but never the criteria.**
  `Advancement.read` reconstructs the record with an empty criteria map and
  `AdvancementRewards.EMPTY`. The only reason a client can render "3/7" is
  that `AdvancementRequirements` *is* on the wire and
  `AdvancementProgress.update` reconciles against it. A client cannot know
  what any criterion tests, or that an advancement grants anything at all.
- **Layout coordinates are computed on the server and shipped.**
  `TreeNodePosition` runs inside `ServerAdvancementManager` and mutates
  `DisplayInfo` in place; the coordinates ride the packet. The advancements
  screen does no *tree* layout — it is drawing positions a data-pack reload
  decided. A root with no `DisplayInfo` is never laid out and never becomes
  a tab, and a display-less node in the middle of a tree is transparent:
  `TreeNodePosition` skips it and adopts its children.
- **The announce-to-chat flag is write-only on the wire.**
  `DisplayInfo.serializeToNetwork` packs three flags into an int and omits
  it; `DisplayInfo.fromNetwork` hard-codes it false while the codec defaults
  it *true*. Nothing on the client reads it, so the decision is made
  entirely on the server — but the client's copy is wrong for the common
  case, not merely unused.
- **`/reload` does not roll back progress; it drops what the pack no longer
  defines.** The order is the point: `MinecraftServer.reloadResources` calls
  `PlayerList.saveAll` and *then* `PlayerList.reloadResources`, so
  `PlayerAdvancements.reload` re-reads a file written moments earlier. What
  is genuinely lost is progress for any advancement the new data pack has
  removed or renamed — logged once per advancement, and invisible to the
  player except as a full reset packet. The selected tab is silently
  forgotten too, with no packet, so the client keeps a stale one.
- **Progress is written only when the player is saved.** There is no write
  on award; `PlayerAdvancements.save` runs from `PlayerList.save`, on
  disconnect, on a save-all, or from the reload above.
- **The listener set shrinks, with two exceptions.**
  `PlayerAdvancements.registerListeners` subscribes only to criteria that are
  not yet done, in advancements that are not yet done, and every award
  unsubscribes — so the cost of the system to a player falls monotonically
  over that player's life *unless* somebody runs `/advancement revoke`, which
  re-subscribes, or `/reload`, which re-subscribes everything unfinished in
  the new pack.
- **`ImpossibleTrigger` has no trigger method at all.** It is the one
  trigger that implements `CriterionTrigger` directly, and it exists so a
  node can anchor a tree while being ungrantable except by command. Vanilla
  uses it for exactly one file: the invisible root of every recipe
  advancement. It has nothing to do with the `/trigger` command, which is a
  scoreboard feature ([scores, teams and stored data](scoreboard-and-data.md)).
- **The recipe book is unlocked by the advancement system.** Every recipe
  advancement is generated with a `RecipeUnlockedTrigger` criterion and an
  `AdvancementRewards` naming the recipe; earning it calls
  `ServerPlayer.awardRecipes`. `RecipeUnlockedTrigger` then closes the
  loop by letting other advancements observe an unlock — and it compares
  the recipe key by **reference identity**, which is safe only because
  `ResourceKey`s are interned.
- **An advancement with no requirement clauses is permanently
  incompletable** — and unloadable. `AdvancementRequirements.test` returns
  false outright for an empty list rather than vacuously true, but the
  codec's own validation rejects a requirements set that does not exactly
  match the criteria, and criteria can never be empty. The only way to hold
  such an object is to decode one off the wire, which is what the client
  does before its first `AdvancementProgress.update`.
- **`PlayerAdvancements.checkForAutomaticTriggers` is dead code, and would
  not do what its name says.** It runs a full pass over every advancement on
  every player load and every reload; the criterion name it awards is the
  empty string, which no progress object contains, so the award always fails
  — while the rewards are granted anyway. `Advancement.CODEC` rejects an
  empty criteria map, so nothing loadable reaches it either way.
- **`ServerboundSeenAdvancementsPacket` has a "closed screen" action that
  the server ignores.** It is serialised, deserialised, and dropped.
- **`Advancement.sendsTelemetryEvent` is consumed only on the client.**
  `WorldSessionTelemetryManager` reads it when an advancement completes, and
  only for advancements in the *minecraft* namespace. That is the whole
  reason a flag rides a wire form that drops the criteria and the rewards
  ([the out-of-scope tour](../appendix/out-of-scope-tour.md)).

## Where to look

`Advancement` and `AdvancementRequirements` for the model;
`PlayerAdvancements` for everything that actually happens — it is the only
class here with interesting state; `SimpleCriterionTrigger` and
`InventoryChangeTrigger` for the hot path; `MinMaxBounds` and
`CollectionPredicate` for the predicate shapes that recur everywhere else;
`AdvancementVisibilityEvaluator` for the one rule nobody guesses right.

---

*Rules: names, never code · how the system works, not how the code reads ·
newest version only · every backticked name passes `tools/verify_names.py`.*
