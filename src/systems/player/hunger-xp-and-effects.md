# Hunger, XP and effects

> Verified against **Minecraft 26.2** · Part VIII · Three counters the server owns outright and the client is merely told about: the food bar, the experience bar, and the list of things currently happening to you.

## Responsibility

Three small systems that share one property: **the client computes none of
them.** Hunger, experience and status effects are all server-authoritative
state that arrives as a number in a packet. They are grouped here because
they are the rest of what a player *is*, after the inventory and the
position.

The one sentence a player recognises: *the two bars above the hotbar, and
the swirls.*

The headline for a 1.21-era reader: **the natural-regeneration game rule
has been renamed** — it is `GameRules.NATURAL_HEALTH_REGENERATION` now, and
`GameRules` itself has moved to `world/level/gamerules` with typed
`GameRule` lookups
([level data and rules](../world/level-data-and-rules.md)). Also: nothing
named *eat* exists on `Player` or `LivingEntity` any more.

## The data it owns

### Hunger

**`FoodData`** (`world/food`) is a value bag with no back-reference to the
player: `FoodData.foodLevel` (20), `FoodData.saturationLevel` (5.0),
`FoodData.exhaustionLevel` and `FoodData.tickTimer`. Its whole surface is
`FoodData.eat`, `FoodData.addExhaustion` (which caps at 40),
`FoodData.needsFood`, `FoodData.hasEnoughFood`, `FoodData.setFoodLevel`,
`FoodData.setSaturation` and `FoodData.tick` — whose signature is
`FoodData.tick(ServerPlayer)`, **server-only by type**. It saves as four
loose keys in the player tag, not a sub-compound.

**`FoodConstants`** is the interesting one: it names every threshold —
`FoodConstants.MAX_FOOD`, `FoodConstants.HEAL_LEVEL`,
`FoodConstants.HEALTH_TICK_COUNT`,
`FoodConstants.HEALTH_TICK_COUNT_SATURATED`,
`FoodConstants.EXHAUSTION_DROP`, `FoodConstants.EXHAUSTION_HEAL`,
`FoodConstants.EXHAUSTION_SPRINT`, `FoodConstants.EXHAUSTION_MINE`,
`FoodConstants.EXHAUSTION_ATTACK`, `FoodConstants.SPRINT_LEVEL`,
`FoodConstants.SATURATION_FLOOR` and the saturation-quality ladder from
`FoodConstants.FOOD_SATURATION_POOR` to
`FoodConstants.FOOD_SATURATION_SUPERNATURAL` — and **almost none of them
is referenced by anything.** Only `FoodConstants.saturationByModifier` has
call sites; `FoodData` writes every threshold as an inline literal.

### Eating

**`FoodProperties`** (`DataComponents.FOOD`) is now only three things:
nutrition, saturation and *can always eat*. The duration moved to
**`Consumable`** (`DataComponents.CONSUMABLE`), which owns
`Consumable.consumeSeconds`, the `ItemUseAnimation`, the sound, the
particles and a list of `ConsumeEffect`s —
`ApplyStatusEffectsConsumeEffect`, `RemoveStatusEffectsConsumeEffect`,
`ClearAllStatusEffectsConsumeEffect`, `TeleportRandomlyConsumeEffect`,
`PlaySoundConsumeEffect`. `FoodProperties` reaches the player by
implementing **`ConsumableListener`**: `Consumable.onConsume` walks every
component of that type on the stack.

**`UseEffects`** (`DataComponents.USE_EFFECTS`) is the eat-slowdown, and
it is on *every* item — `UseEffects.canSprint`,
`UseEffects.interactVibrations`, `UseEffects.speedMultiplier`. It is read
only by `LocalPlayer.isSlowDueToUsingItem` and
`LocalPlayer.itemUseSpeedMultiplier`, so the slowdown is **client-side and
data-driven**. Spears override it so you can sprint while charging.

### Experience

`Player.experienceLevel`, `Player.experienceProgress`,
`Player.totalExperience` and `Player.enchantmentSeed`, plus
`Player.takeXpDelay`. The arithmetic is `Player.giveExperiencePoints`,
`Player.giveExperienceLevels` and `Player.getXpNeededForNextLevel` (the
three-segment curve at levels 15 and 30).

**`ExperienceOrb`** is an `Entity` with `ExperienceOrb.DATA_VALUE`
synched and everything else — `ExperienceOrb.count`, `ExperienceOrb.age`,
`ExperienceOrb.health`, `ExperienceOrb.followingPlayer` — server-side.
`ExperienceOrb.award` splits an amount into denominations via
`ExperienceOrb.getExperienceValue`, and `ExperienceOrb.tryMergeToExisting`
folds each into a nearby orb of equal value. Merging is by **count, not
value**: an orb carries one value and a multiplicity, and
`ExperienceOrb.ORB_GROUPS_PER_AREA` buckets candidates by entity id so the
scan is not quadratic.

### Effects

**`MobEffect`** is the behaviour singleton: a category, a colour, a
particle factory, blend durations and a map of attribute templates. Its
hooks are `MobEffect.applyEffectTick` (returning false ends the effect),
`MobEffect.shouldApplyEffectTickThisTick` (**false by default**),
`MobEffect.applyInstantaneousEffect`, `MobEffect.onEffectStarted`,
`MobEffect.onEffectAdded`, `MobEffect.onMobHurt`,
`MobEffect.onMobRemoved`. Attribute modifiers go on as
`AttributeInstance.addPermanentModifier` with an amount linear in
amplifier + 1 ([attributes](../entities/attributes.md)).

**`MobEffectInstance`** holds duration, amplifier, the ambient,
visible and show-icon flags, a **`MobEffectInstance.hiddenEffect`** — the stack that lets a
stronger, shorter effect temporarily mask a weaker, longer one — and a
private blend state. It serialises through a nested private record with a
recursive codec. `MobEffectInstance.compareTo` is what orders the HUD.

**`MobEffects`** is forty entries, and every one is a
`Holder<MobEffect>`, not a bare `MobEffect`. New in 26.2:
`MobEffects.BREATH_OF_THE_NAUTILUS`. Some old effects point at new
attributes — `MobEffects.JUMP_BOOST` now modifies
`Attributes.SAFE_FALL_DISTANCE`, and `MobEffects.INVISIBILITY` modifies
`Attributes.WAYPOINT_TRANSMIT_RANGE`.

On the entity: `LivingEntity.activeEffects` (a plain unordered map),
`LivingEntity.effectsDirty`, and two synched values —
`LivingEntity.DATA_EFFECT_PARTICLES`, which is a **list of
`ParticleOptions`**, not a packed colour, and
`LivingEntity.DATA_EFFECT_AMBIENCE_ID`.

## When it runs

All three hang off the player tick, and *which* player tick matters
([player anatomy](player-anatomy.md)). `ServerPlayer.tick` — the entity
loop's tick — touches none of them. Everything here is under
`ServerPlayer.doTick`, the connection-driven half:

1. `Player.tick` → `LivingEntity.tick` →
   `LivingEntity.baseTick` → **`LivingEntity.tickEffects`**;
2. still in `LivingEntity.tick`, `LivingEntity.updatingUsingItem`
   finishes an eaten item — **server-side only**;
3. `Player.aiStep` → `ServerPlayer.tickRegeneration`, the Peaceful
   refill;
4. back in `ServerPlayer.doTick`, **`FoodData.tick`**;
5. then the change-detection block that emits the packets.

So a Hunger effect's exhaustion and a meal eaten this tick are both
visible to `FoodData.tick` in the same tick.

**The client ticks effects but not hunger.** `LivingEntity.tickEffects`'
client branch only counts durations down, unhides hidden effects, advances
the blend factor and spawns ambient particles; it never calls
`MobEffect.applyEffectTick` and never touches an attribute. It does not
even remove an expired effect — it keeps a zero-duration instance until
told otherwise. `FoodData.tick` has exactly one call site, on the server;
the client's `FoodData` is a mirror written by
`ClientPacketListener.handleSetHealth`.

## The trace: eating bread on a full stomach's edge

```mermaid
sequenceDiagram
    participant LE as LivingEntity
    participant IS as ItemStack
    participant CO as Consumable
    participant FP as FoodProperties
    participant FD as FoodData
    participant SP as ServerPlayer
    participant CP as ClientPacketListener

    LE->>LE: updateUsingItem — useItemRemaining hits zero, server side only
    LE->>IS: finishUsingItem — the item decides what finishing means
    IS->>CO: onConsume — walks every ConsumableListener on the stack
    CO->>FP: onConsume — the food component is one such listener
    FP->>FD: eat — nutrition and pre-multiplied saturation, clamped
    CO->>CO: onConsumeEffects — potions, teleports, sounds; then consume(1)
    SP->>FD: tick — exhaustion drain, then regen or starvation
    SP->>CP: ClientboundSetHealthPacket — only when health, food or zero-saturation changed
```

`Consumable.canConsume` gates the whole thing on `Player.canEat`:
creative, *can always eat*, or `FoodData.needsFood`. An item whose
`Consumable.consumeTicks` is zero is consumed instantly with no animation.
After the food lands, `ItemStack.finishUsingItem` applies
`DataComponents.USE_REMAINDER` and `DataComponents.USE_COOLDOWN`
([items and stacks](../items/items-and-stacks.md)).

`FoodData.tick` then runs four rules in order: drain exhaustion above 4.0
into saturation, or into the food bar if saturation is spent and the
difficulty is not `Difficulty.PEACEFUL`; heal fast off saturation at a
full bar; heal slowly at 18 or more; and starve at zero — where the
`Difficulty` decides the floor, ten hearts on Easy, half a heart on
Normal, death on Hard. `DamageTypes.STARVE` is declared with zero
exhaustion so starving does not feed itself.

## Interfaces

- **Called by:** `ServerPlayer.doTick` for all three;
  `ExperienceOrb.playerTouch` for XP pickup;
  `LivingEntity.addEffect` from every source of an effect.
- **Calls into:** `LivingEntity.hurtServer` (starvation, poison, wither —
  [damage and death](../entities/damage-and-death.md)); `AttributeMap`
  ([attributes](../entities/attributes.md)); `EnchantmentHelper` for
  mending.
- **Crosses the network as:** `ClientboundSetHealthPacket` (health, food
  and saturation together, to that player only),
  `ClientboundSetExperiencePacket` (progress, level and total),
  `ClientboundUpdateMobEffectPacket` and
  `ClientboundRemoveMobEffectPacket`, plus
  `LivingEntity.DATA_EFFECT_PARTICLES` for other entities' swirls and
  `ClientboundTakeItemEntityPacket` for the orb pickup animation.
- **Data-driven by:** `DataComponents.FOOD`,
  `DataComponents.CONSUMABLE`, `DataComponents.USE_EFFECTS`,
  `Registries.CONSUME_EFFECT_TYPE`, `BuiltInRegistries.MOB_EFFECT`,
  `EnchantmentEffectComponents.REPAIR_WITH_XP`,
  `GameRules.NATURAL_HEALTH_REGENERATION`, `GameRules.KEEP_INVENTORY`,
  `GameRules.MOB_DROPS`.

## Invariants and surprises

- **Walking and crouching cost exactly zero exhaustion, and the code says
  so out loud.** `ServerPlayer.checkMovementStatistics` still multiplies
  distance by a literal zero on both branches, and
  `FoodConstants.EXHAUSTION_WALK` documents the intent while being
  referenced by nothing. The exhaustion economy is sprinting, jumping,
  swimming, mining, attacking and being hurt — the last of which is
  data-driven, since `DamageSource.getFoodExhaustion` reads the damage
  type.
- **`FoodConstants` is almost entirely dead.** `FoodData` duplicates every
  threshold inline, so the constants file and the behaviour can drift
  apart without a compile error.
- **Mending takes the orb before you do, and recurses.**
  `ExperienceOrb.playerTouch` runs `ExperienceOrb.repairPlayerItems`
  first and only the remainder becomes experience; that method calls
  itself with the leftover, so one large orb can repair several tools.
- **One orb entity can be picked up many times.** It carries a count,
  decremented per touch behind a two-tick `Player.takeXpDelay`.
- **The enchanting seed is re-rolled by enchanting.**
  `Player.onEnchantmentPerformed` subtracts the level cost *and* re-rolls
  `Player.enchantmentSeed`; `AnvilMenu`, which also spends levels, does
  not. And a seed that loads back as zero is re-rolled on read.
- **The client never runs a status effect.** All of
  `LivingEntity.onEffectAdded`, `LivingEntity.onEffectUpdated` and
  `LivingEntity.onEffectsRemoved` are server-guarded, so no attribute modifier is ever applied
  client-side; attribute values arrive by their own sync. The client's
  durations desync harmlessly and are corrected by a re-send every 600
  ticks.
- **`ClientboundUpdateMobEffectPacket` never carries the hidden-effect
  chain** — only one instance, plus a bit saying whether to blend in. The
  client rebuilds with no hidden effect at all.
- **Blending is a pure render quantity.** `MobEffectInstance`'s blend
  state ticks only on the client and is never saved or sent; only
  `MobEffects.NAUSEA` and `MobEffects.DARKNESS` use it.
- **A concurrent-modification error in effect ticking is caught and
  silently dropped** by `LivingEntity.tickEffects` — an effect that adds
  or removes another quietly aborts the rest of that tick's processing.
- **An infinite effect pulses off a different clock.**
  `MobEffectInstance.tickServer` counts an infinite-duration effect's
  pulses off the entity's age and a finite one off its own countdown.
- **The Peaceful refill bypasses the clamp.**
  `ServerPlayer.tickRegeneration` calls `FoodData.setFoodLevel` directly,
  skipping the rule that ties saturation to the food level.
- **Saturation is sent but not change-detected.**
  `ClientboundSetHealthPacket` carries a full float, yet the server only
  notices whether saturation became *zero* — so the client's saturation
  lags until health or food moves.

## Where to look

`FoodData` · `FoodConstants` · `FoodProperties` · `Consumable` ·
`ConsumableListener` · `ConsumeEffect` · `UseEffects` · `Foods` ·
`ExperienceOrb` · `Player` · `MobEffect` · `MobEffectInstance` ·
`MobEffects` · `MobEffectCategory` · `MobEffectUtil` · `LivingEntity` ·
`ClientboundSetHealthPacket` · `ClientboundUpdateMobEffectPacket`

---

*Rules: names, never code · how the system works, not how the code reads ·
newest version only · every backticked name passes `tools/verify_names.py`.*
