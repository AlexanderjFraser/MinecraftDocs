# Loot tables

> Verified against **Minecraft 26.2** · Part VII · A player opens a dungeon chest: the chest is genuinely empty on disk, the table rolls at the moment of opening, and whoever touches the block first — player or hopper — commits the roll.

## Responsibility

A loot table is a data-pack description of "roll some items". The system
loads those descriptions into registries, evaluates them against a bag of
typed parameters, and hands the results to whoever asked. Blocks, mobs,
chests, fishing, brushing, bartering, villager gifts, advancements and
commands all ask.

The one sentence a player recognises: *what a chest has in it, and what
a mob drops.*

The headline: **loot parameters are not loot-specific.** The keys and
sets are the general-purpose `ContextKey`, `ContextKeySet` and
`ContextMap`, living outside the loot package, and the same machinery is
what [enchantments](enchantments.md) use to decide whether an effect
fires. This is Minecraft's data-driven predicate and effect engine;
generating items is one of its clients, and the others are named in the
table below.

## The data it owns

- **`LootTable`** — a parameter set, an optional random-sequence
  identifier, a list of pools, table-level functions pre-composed into
  one, and the container-filling entry points `LootTable.fill` and
  `LootTable.getRandomItems`.
- **`LootPool`** — entries, conditions, functions, and two number
  providers: `LootPool.rolls` and `LootPool.bonusRolls`.
- **`LootPoolEntryContainer`** and its expansion. `ComposableEntryContainer.expand`
  returns a boolean — "did I contribute" — and that is what makes the
  composites work: `AlternativesEntry` is an or, `SequentialEntry` is an
  and, `EntryGroup` runs everything. The leaves are `LootItem`,
  `TagEntry`, `NestedLootTable`, `DynamicLoot`, `EmptyLootItem` and
  `SlotLoot`. `TagEntry` has two modes: expanded, where the tag becomes
  one weighted entry per item, and unexpanded, where a single entry emits
  *every* item in the tag.
- **`LootPoolSingletonContainer`** — weight and quality.
  `LootPoolSingletonContainer.EntryBase.getWeight` is
  *weight + quality × luck*, floored at zero.
- **`LootItemFunction`** — a function from stack to stack, extending
  `LootContextUser` and a plain bi-function. Forty-three of them, from
  `SetItemCountFunction` and `EnchantWithLevelsFunction` to
  `SetContainerLootTable`, `ApplyBonusCount` and `ApplyExplosionDecay`.
  `ApplyBonusCount`, `EnchantedCountIncreaseFunction`,
  `BonusLevelTableCondition` and
  `LootItemRandomChanceWithEnchantedBonusCondition` are between them
  Fortune and Looting — and they key off
  `LootContextParams.ENCHANTMENT_LEVEL` and `LootContextParams.TOOL`, not
  luck.
- **`LootItemCondition`** — a predicate over a `LootContext`. The usual
  suspects plus `EnchantmentActiveCheck` and `EnvironmentAttributeCheck`.
- **`NumberProvider`** — `ConstantValue`, `UniformGenerator`,
  `BinomialDistributionGenerator`, `ScoreboardValue`, `StorageValue`,
  `Sum`, `EnchantmentLevelProvider`, `EnvironmentAttributeValue`. A bare
  float works wherever one is expected.
- **`LootContext`** — the per-invocation state: the params, the chosen
  random source, a resolver for references, and a **stack** of visited
  elements used as the recursion guard.
- **`LootParams`** — the immutable inputs: the level, a `ContextMap`, the
  dynamic-drop callbacks and the luck value.
- **`LootContextParams`** — the fifteen keys, including
  `LootContextParams.THIS_ENTITY`, `LootContextParams.ORIGIN`,
  `LootContextParams.BLOCK_STATE`, `LootContextParams.TOOL` (typed as
  `ItemInstance`, the read-only item view),
  `LootContextParams.DAMAGE_SOURCE`,
  `LootContextParams.ATTACKING_ENTITY`,
  `LootContextParams.EXPLOSION_RADIUS` and
  `LootContextParams.ENCHANTMENT_LEVEL`.
- **`LootContextParamSets`** — the twenty-six named sets. Notable ones:
  `LootContextParamSets.BLOCK`, `LootContextParamSets.ENTITY`,
  `LootContextParamSets.CHEST`, `LootContextParamSets.FISHING`,
  `LootContextParamSets.ARCHAEOLOGY`, `LootContextParamSets.SHEARING`,
  `LootContextParamSets.GIFT`, `LootContextParamSets.VAULT`,
  `LootContextParamSets.EMPTY` and the catch-all
  `LootContextParamSets.ALL_PARAMS`, which is what a table with no
  declared type gets — and which is not actually *all* of them: it omits
  the interacting and target entities and the two enchantment keys.
- **`LootDataType`** — the three loot registries as data:
  `LootDataType.TABLE`, `LootDataType.PREDICATE`,
  `LootDataType.MODIFIER`.
- **`BuiltInLootTables`** — the hardcoded keys for chests, gameplay,
  shearing, brushing, equipment and spawners.

Loot tables **are a registry of data-pack objects**: `Registries.LOOT_TABLE`,
with predicates and item modifiers as siblings. They live in the
reloadable registry layer, and code reaches them through the server's
reloadable-registry holder rather than a manager class. Tags work on all
three, loaded per registry during the reload.

### Named random sequences

A table may declare a random-sequence identifier. When it does,
`LootContext` resolves it through the server's per-world `RandomSequences`
store rather than using the level's random — which is what makes "the same
table, at the same place, in this world" reproducible across restarts.
The villager trade path uses the same mechanism for its own selection.

## When it runs

**A background executor thread** for loading and validation.
`ReloadableServerRegistries` schedules one load per loot data type,
populates a registry each, freezes them and then validates.

**Server main thread** for every roll. The mechanical guarantee is not a
thread check but a type one: `LootParams` is built from a `ServerLevel`
and `LootContext` dereferences the server off it, so a `ClientLevel`
cannot produce one at all.

**Chunk generation** writes the *seed*, onto the live block entity, when
a structure piece places a container. The seed reaches NBT only on the
next save — and from then on, loading that block entity finds a loot
table key and **skips loading items entirely**. The chest on disk is
empty by design.

## The trace: a chest generates

```mermaid
sequenceDiagram
    participant SPGM as ServerPlayerGameMode
    participant CB as ChestBlock
    participant SP as ServerPlayer
    participant RC as RandomizableContainer
    participant LT as LootTable
    participant LP as LootPool
    participant CM as ChestMenu

    SPGM->>CB: useItemOn → useWithoutItem → getMenuProvider
    CB->>SP: Player.openMenu
    SP->>RC: createMenu → canOpen → unpackLootTable(player)
    RC->>RC: setLootTable(null) BEFORE rolling — one shot
    RC->>LT: fill(container, LootParams on the CHEST set, seed)
    LT->>LP: addRandomItems per pool — rolls + floor(bonusRolls × luck)
    LP->>LP: expand entries, weight = weight + quality × luck, pick
    LT->>LT: shuffleAndSplitItems — split stacks across the free slots
    SP->>CM: initMenu → ClientboundContainerSetContentPacket
```

1. **The click.** `ServerPlayerGameMode.useItemOn` reaches
   `ChestBlock.useWithoutItem`
   ([block interaction](../blocks/block-interaction.md)), which resolves
   a menu provider. A single chest is its own block entity; a double
   chest gets an anonymous provider over a `CompoundContainer` that
   requires *both* halves to unlock and unpacks *both* loot tables
   itself, never entering the block entity's own menu factory.
2. **Opening.** `ServerPlayer.openMenu` calls the provider. For the
   single chest that is
   `RandomizableContainerBlockEntity.createMenu`, which checks
   `RandomizableContainerBlockEntity.canOpen` — a spectator is refused
   while a table is still pending, and the lock check happens here too —
   and then unpacks.
3. **The unpack.** `RandomizableContainer.unpackLootTable` looks the
   table up (a missing key yields `LootTable.EMPTY`, never null), fires
   `CriteriaTriggers.GENERATE_LOOT` for a `ServerPlayer`, and **clears
   the stored key before rolling**. It builds a `LootParams` with the
   origin, and — only if a player is present — that player's luck and
   entity.
4. **The random source.** `LootTable.fill` uses the stored seed if it is
   non-zero; a zero seed means "unseeded", falling back to the table's
   named random sequence or the level's own random.
   `LootTable.RANDOMIZE_SEED` names the zero, though nothing reads the
   constant.
5. **The pools.** Each pool tests its condition, then rolls
   *rolls + floor(bonusRolls × luck)* times.
6. **The draw.** Each roll expands every entry — this is where
   `AlternativesEntry`, `TagEntry` and `NestedLootTable` fan out — keeps
   the entries whose weight is above zero, sums, picks and walks. A pool
   left with exactly one candidate takes it without consuming any
   randomness at all.
7. **The functions.** Entry functions, then pool functions, then table
   functions, each short-circuiting on its own conditions.
8. **The splitter.** `LootTable.createStackSplitter` drops
   feature-disabled items and splits anything at or over its maximum
   stack size. A nested table's own results are *not* split twice: the
   nested entry deliberately calls the raw variant and lets the outer
   splitter do it.
9. **The scatter.** `LootTable.fill` does not simply place the results:
   `LootTable.getAvailableSlots` shuffles the empty slots, and
   `LootTable.shuffleAndSplitItems` repeatedly splits multi-count stacks —
   each time taking a random amount up to half — until they roughly fill
   the slot count. That is why one rolled stack of arrows arrives as
   three partial ones. Running out of slots logs a warning **and silently
   discards** everything still in hand.
10. **The screen.** The menu is created, `ClientboundOpenScreenPacket`
    goes out, and then `ServerPlayer.initMenu` attaches the synchronizer,
    whose attachment sends the freshly rolled contents as one
    `ClientboundContainerSetContentPacket`
    ([containers and menus](containers-and-menus.md)).

## Interfaces

Who calls loot tables, and with which parameter set:

| caller | set | when |
|---|---|---|
| `BlockBehaviour.BlockStateBase.getDrops` | `LootContextParamSets.BLOCK` | any block break ([block breaking](../blocks/block-breaking.md)) |
| `Block.dropFromBlockInteractLootTable` | `LootContextParamSets.BLOCK_INTERACT` | beehives, cave vines, carving a pumpkin, sweet berries |
| `LivingEntity.dropFromLootTable` | `LootContextParamSets.ENTITY` | death ([damage and death](../entities/damage-and-death.md)) |
| `LivingEntity.dropFromShearingLootTable` | `LootContextParamSets.SHEARING` | sheep, mooshrooms, snow golems, bogged |
| `LivingEntity.dropFromGiftLootTable` | `LootContextParamSets.GIFT` | villager hero gifts, cat gifts, chicken eggs, sniffer digs |
| `LivingEntity.dropFromEntityInteractLootTable` | `LootContextParamSets.ENTITY_INTERACT` | brushing an armadillo |
| `RandomizableContainer.unpackLootTable` | `LootContextParamSets.CHEST` | first touch of a structure container |
| `ContainerEntity.unpackChestVehicleLootTable` | `LootContextParamSets.CHEST` | first touch of a chest minecart or chest boat |
| `FishingHook.retrieve` | `LootContextParamSets.FISHING` | reeling in; luck is the hook's plus the owner's |
| `BrushableBlockEntity` | `LootContextParamSets.ARCHAEOLOGY` | brushing suspicious sand |
| `PiglinAi.getBarterResponseItems` | `LootContextParamSets.PIGLIN_BARTER` | bartering |
| `EquipmentUser.equip` | `LootContextParamSets.EQUIPMENT` | mob spawn equipment |
| `VaultBlockEntity` | `LootContextParamSets.VAULT` | trial chamber vaults |
| `TrialSpawner.ejectReward` | `LootContextParamSets.EMPTY` | a trial spawner's reward and its dispensed items |
| `AdvancementRewards.grant` | `LootContextParamSets.ADVANCEMENT_REWARD` | advancement loot |
| `Enchantment.damageContext` and its siblings | the four enchanted sets plus `LootContextParamSets.HIT_BLOCK` | an enchantment effect's condition |
| `LootCommand` | block, entity, chest or fishing | `/loot` |
| `ItemCommands.applyModifier` | `LootContextParamSets.COMMAND` | `/item … with` |

Five sets have no loot caller at all, and they are the ones that show
what the engine really is: `ExecuteCommand` uses
`LootContextParamSets.COMMAND` for `/execute if predicate`,
`EntitySelectorOptions` uses `LootContextParamSets.SELECTOR` for a
selector's *predicate* argument, `EntityPredicate.matches` uses
`LootContextParamSets.ADVANCEMENT_ENTITY`, the location triggers use
`LootContextParamSets.ADVANCEMENT_LOCATION` and
`LootContextParamSets.BLOCK_USE`, and `AbstractVillager` uses
`LootContextParamSets.VILLAGER_TRADE` to filter trades.

- **Crosses the network as:** nothing. The three loot registries live in
  the reloadable layer, which is structurally excluded from registry
  synchronisation, and no client class references the package at all.
  What crosses is the *result* — container packets, item entities — and,
  as a wrinkle, `DataComponents.CONTAINER_LOOT`: declared persistent with
  no explicit network codec, it falls back to an NBT codec and therefore
  *does* reach the client, which is how a picked-up shulker box can show
  an unknown loot table in its tooltip.
- **Data-driven by:** `Registries.LOOT_TABLE`, `Registries.PREDICATE`,
  `Registries.ITEM_MODIFIER`, plus the type registries for entries,
  functions, conditions and the three provider families.

### Missing parameters, three ways

Building a `ContextMap` throws on both extra and absent required
parameters — so the enforcement point is the *caller's* declared set, not
the table's. Reading a required parameter that is not there throws;
reading it optionally returns nothing, and most conditions and functions
degrade quietly. And at load time the validator merely *reports* that an
element referenced a parameter its set does not provide — logged as a
warning.

## Invariants and surprises

- **A table's declared type is never checked at runtime.** It is read
  only during load-time validation; the roll itself never compares it
  against the incoming parameters, and `TrialSpawner` passes the empty
  set to chest-shaped tables.
- **The loot table key is cleared *before* the roll**, and the container
  read methods on a randomizable block entity unpack first — so a hopper
  or a comparator generates the loot with **no player and no luck**,
  permanently. The first observer wins, and need not be a player. Note
  which methods those are: emptiness, item read, both removals and item
  *write*. Clearing the container and asking its size do not unpack, and
  neither does saving it — which is why `/data get block` on an unopened
  chest reports the loot table key rather than committing the roll.
- **A seed of zero means "unseeded"** and is indistinguishable from
  having no seed at all, re-rolling freshly each time. It is also never
  written to NBT.
- **The recursion guard is a stack, not a ledger.** A table pushes itself
  while it draws and pops afterwards, so referencing the same table twice
  in one draw — from two pools, or across two rolls — yields items every
  time. Only genuine re-entrancy trips it, and it is logged as an
  infinite loop rather than passing silently.
- **Luck touches exactly two things**: bonus rolls, and entry quality.
  And because the weight is floored at zero and zero-weight entries are
  discarded, a negative quality with high luck removes an entry from the
  pool rather than merely making it rare.
- **Composites are boolean short-circuits, not weighted choices** — and
  the validator will tell you when an unconditioned alternative makes a
  later one unreachable.
- **`LootTable.fill` redistributes as well as places**, splitting stacks
  to spread across the free slots.
- **Validation failures are warnings, never errors.** A table that
  references a missing predicate, uses a parameter it cannot have, or
  recurses will load fine and misbehave later. The two hard validators
  are the ones a codec applies: villager trades, and the enchantment
  effect components.
- **A missing table yields `LootTable.EMPTY`, never null** — and one
  caller, the equipment path, compares against it by identity to skip
  work.
- **Standalone predicate and item-modifier files are validated against
  the all-parameters set — which is not all of them.** A standalone
  predicate that asks whether an enchantment is active, or about the
  interacting or target entity, *is* flagged; most other conditions are
  not, while the same condition inlined in a block table would be.
- **Functions mutate the stack in place and return it.** Both styles work
  because composition threads the return value, and it is safe because
  the leaf entries construct fresh stacks — with one exception,
  `DynamicLoot`, whose callback may hand back a live container stack
  uncopied.

## Where to look

`LootTable` · `LootPool` · `LootContext` · `LootParams` · `ContextMap` ·
`ContextKeySet` · `LootContextParams` · `LootContextParamSets` ·
`LootPoolEntryContainer` · `LootPoolSingletonContainer` ·
`ComposableEntryContainer` · `AlternativesEntry` · `NestedLootTable` ·
`DynamicLoot` · `TagEntry` ·
`LootItemFunction` · `LootItemCondition` · `NumberProvider` ·
`LootDataType` · `BuiltInLootTables` · `ReloadableServerRegistries` ·
`RandomizableContainer` · `RandomizableContainerBlockEntity` ·
`ContainerEntity` ·
`SeededContainerLoot` · `LootCommand`

---

*Rules: names, never code · how the system works, not how the code reads ·
newest version only · every backticked name passes `tools/verify_names.py`.*
