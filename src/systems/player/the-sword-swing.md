# The sword swing

> Verified against **Minecraft 26.2** · Part VIII · Left-click on a pig: the client picks a target and sends one integer, and the server recomputes every part of the hit that matters.

## Responsibility

Melee combat is the place where the client's opinion and the server's
authority meet most often and most visibly. This page follows one attack:
how the client decides what is under the crosshair, what it is allowed to
tell the server, how the server rebuilds the damage from scratch, and what
comes back.

The one sentence a player recognises: *swinging at the right moment does
more damage than mashing.*

The headline for a 1.21-era reader: **attack has its own packet now, and
it carries nothing but an entity id.** `ServerboundInteractPacket` is
right-click only. And reach is no longer just an attribute — it is a data
component on the weapon, with a *minimum* range as well as a maximum.

## The data it owns

- **`Minecraft.hitResult`** and **`Minecraft.crosshairPickEntity`** — the
  client's answer to "what am I looking at", rewritten by
  `Minecraft.pick` once per tick and again per frame.
- **The two attack tickers**, both on `LivingEntity`, not `Player`:
  `LivingEntity.attackStrengthTicker` and `LivingEntity.itemSwapTicker`,
  incremented in `Player.tick`. The vocabulary over them is
  `Player.getAttackStrengthScale`, `Player.getItemSwapScale`,
  `Player.getCurrentItemAttackStrengthDelay` (derived from
  `Attributes.ATTACK_SPEED`), `Player.resetAttackStrengthTicker` (clears
  both) and `Player.resetOnlyAttackStrengthTicker` (clears one).
- **`AttackRange`** (`DataComponents.ATTACK_RANGE`) — a weapon's reach: a
  minimum and maximum, separate creative values, a hitbox margin and a mob
  factor. `AttackRange.isInRange` is the test;
  `AttackRange.defaultFor` falls back to
  `Attributes.ENTITY_INTERACTION_RANGE`.
- **`Weapon`** (`DataComponents.WEAPON`), **`PiercingWeapon`**
  (`DataComponents.PIERCING_WEAPON`),
  `DataComponents.MINIMUM_ATTACK_CHARGE` and
  `DataComponents.DAMAGE_TYPE` — the rest of what makes an item a weapon
  ([items and stacks](../items/items-and-stacks.md)).
- **The swing animation state** on `LivingEntity`: `LivingEntity.swinging`,
  `LivingEntity.swingingArm`, `LivingEntity.swingTime`,
  `LivingEntity.attackAnim`. The duration is a component too —
  `ItemStack.getSwingAnimation` gives a `SwingAnimation`.

## When it runs

Client, once per tick, in this order inside `Minecraft.tick`:
`MultiPlayerGameMode.tick` → **`Minecraft.pick`** → the GUI →
`Minecraft.handleKeybinds`, which drains `Options.keyAttack` into
`Minecraft.startAttack` and finishes with `Minecraft.continueAttack` for
held-down mining. So the hit result a click uses was computed *earlier in
the same tick*. `Minecraft.pick` also runs per frame for the crosshair and
block outline, but that value is not what the attack sees.

Server: the packet is drained from `PacketProcessor` at the **top** of the
tick, before `MinecraftServer.tickServer` and therefore before any level
ticks. That ordering matters — `Player.attack` runs before the victim's
`LivingEntity.tick` decrements `LivingEntity.invulnerableTime` for the
tick. All the resulting feedback packets leave in one flush, because the
connection suspends flushing across `MinecraftServer.tickChildren`.

## The trace: click to damage

```mermaid
sequenceDiagram
    participant MC as Minecraft
    participant LP as LocalPlayer
    participant MG as MultiPlayerGameMode
    participant CL as ServerGamePacketListenerImpl
    participant PL as Player
    participant LE as LivingEntity
    participant SL as ServerLevel

    MC->>LP: raycastHitResult — AttackRange first, else the classic two-range pick
    MC->>MG: attack — only after cannotAttackWithItem, tolerance 0
    MG->>CL: ServerboundAttackPacket — one varint: the entity id
    LP->>CL: ServerboundSwingPacket — sent regardless, even on a miss
    CL->>CL: isWithinAttackRange — AttackRange plus a 3.0 buffer
    CL->>PL: attack — the server recomputes damage from nothing but the id
    PL->>PL: getAttackStrengthScale — the 0.2 + s² × 0.8 ramp on base damage
    PL->>LE: hurtOrSimulate — into Part VI; returns did-it-land
    PL->>PL: causeExtraKnockback, doSweepAttack, itemAttackInteraction, causeFoodExhaustion
    SL->>MC: ClientboundDamageEventPacket — a damage type and two ids, no amount
```

**Picking.** `Minecraft.pick` asks the camera entity, and for the local
player that is `LocalPlayer.raycastHitResult`. If the held item carries an
`AttackRange`, that component's own search runs first; otherwise the
classic algorithm applies — a block clip out to the greater of the two
ranges, an entity sweep with `ProjectileUtil.getEntityHitResult` over the
motion-expanded box, each candidate inflated by `Entity.getPickRadius`
(**zero** for everything but projectiles) — and the entity wins only if it
is strictly nearer than the block. Then `LocalPlayer.filterHitResult`
discards each against *its own* range:
`Attributes.ENTITY_INTERACTION_RANGE` (3.0) for the entity,
`Attributes.BLOCK_INTERACTION_RANGE` (4.5) for the block. That is where
the two reaches diverge.

**Deciding.** `Minecraft.startAttack` is the branch point. It refuses
while `Minecraft.missTime` is running or `LocalPlayer.isHandsBusy`; checks
`Player.cannotAttackWithItem` with a tolerance of **zero**; short-circuits
entirely to `MultiPlayerGameMode.piercingAttack` if the item has
`DataComponents.PIERCING_WEAPON`; and then switches on the hit result —
entity to `MultiPlayerGameMode.attack`, block to
`MultiPlayerGameMode.startDestroyBlock`
([block breaking](../blocks/block-breaking.md)), miss to
`Player.resetAttackStrengthTicker` and a ten-tick `Minecraft.missTime`.
Every branch ends with `LocalPlayer.swing`.

**The packet.** `ServerboundAttackPacket` is a record of one int.
`ServerGamePacketListenerImpl.handleAttack` resolves it with
`ServerLevel.getEntityOrPart`, checks the world border, applies
`Player.isWithinAttackRange` with a **3.0-block server buffer**, rejects a
piercing weapon (that path arrives elsewhere), re-checks
`Player.cannotAttackWithItem` — this time with a tolerance of **five
ticks**, more lenient than the client's zero — and calls `Player.attack`.
Attacking something absurd (an `ItemEntity`, an `ExperienceOrb`, yourself)
is a **disconnect**, not a rejection; failing the range check is a silent
drop.

**The damage.** `Player.attack` is still one method, and the order is
load-bearing:

1. base damage from `Attributes.ATTACK_DAMAGE` (or the riptide value);
2. the `DamageSource` from `ItemStack.getDamageSource`, defaulting to
   `DamageSources.playerAttack`;
3. `Player.getAttackStrengthScale`, captured **once**;
4. the enchantment bonus, as
   `Player.getEnchantedDamage`'s delta scaled **linearly**;
5. base damage scaled by `Player.baseDamageScaleFactor` — a **quadratic**
   ramp. Two different curves in one number;
6. `Player.onAttack` resets the ticker — *after* the scale was read,
   *before* the hit;
7. `Player.deflectProjectile` can end the attack here;
8. sprint knockback if the scale is above 0.9;
9. `Player.canCriticalAttack` — falling, not on the ground, not
   climbing, not in water, not a passenger, **not sprinting** — for ×1.5;
10. `Player.isSweepAttack` — full strength, *not* a crit, *not* sprint
    knockback, on the ground, moving slowly, and holding something in
    `ItemTags.SWORDS`;
11. **`Entity.hurtOrSimulate`**, whose boolean gates everything after it.

If it landed: `Player.causeExtraKnockback` (with
`LivingEntity.getKnockback`, which halves
`Attributes.ATTACK_KNOCKBACK` after enchantments and damps the
attacker's own motion), `Player.doSweepAttack`,
`Player.attackVisualEffects`, `LivingEntity.setLastHurtMob`,
`Player.itemAttackInteraction` (durability, `ItemStack.hurtEnemy`,
`EnchantmentHelper.doPostAttackEffectsWithItemSource`),
`Player.damageStatsAndHearts`, and `Player.causeFoodExhaustion` of 0.1.

`Player.doSweepAttack` is server-only in its body: it damages everything
in a box inflated by (1, 0.25, 1) within three blocks for
`1.0 + Attributes.SWEEPING_DAMAGE_RATIO × base`, calling
`LivingEntity.hurtServer` **directly** rather than through the wrapper,
and sends `ParticleTypes.SWEEP_ATTACK`.

**Into Part VI.** `Entity.hurtOrSimulate` is a deprecated final wrapper
that branches on the side: `Entity.hurtServer` on the server,
`Entity.hurtClient` on the client. Armour, invulnerability frames,
`DataComponents.BLOCKS_ATTACKS` and knockback resistance all belong to
[damage and death](../entities/damage-and-death.md).

## Interfaces

- **Called by:** `Minecraft.handleKeybinds` (client);
  `ServerGamePacketListenerImpl.handleAttack` (server).
- **Calls into:** `LivingEntity.hurtServer`
  ([damage and death](../entities/damage-and-death.md));
  `EnchantmentHelper` ([enchantments](../items/enchantments.md));
  `Attributes` ([attributes](../entities/attributes.md)).
- **Crosses the network as:** `ServerboundAttackPacket` (attack) and
  `ServerboundInteractPacket` (right-click only, carrying a hand, a
  location and a sneak flag); `ServerboundSwingPacket` and
  `ServerboundPlayerActionPacket` for the piercing path; back the other
  way, `ClientboundAnimatePacket` (swing, crit, magic crit),
  `ClientboundDamageEventPacket`, `ClientboundHurtAnimationPacket`,
  `ClientboundSetHealthPacket`, `ClientboundSetEntityMotionPacket`,
  `ClientboundSoundPacket`.
- **Data-driven by:** `DataComponents.ATTACK_RANGE`,
  `DataComponents.WEAPON`, `DataComponents.PIERCING_WEAPON`,
  `DataComponents.DAMAGE_TYPE`, `DataComponents.MINIMUM_ATTACK_CHARGE`,
  and the `ItemTags.SWORDS` tag for sweep.

## Invariants and surprises

- **The attack packet carries one integer.** No hand, no sneak flag, no
  hit position. The server never learns *where* on the hitbox you hit; it
  re-derives the weapon from `LivingEntity.getMainHandItem` and the
  geometry from the two bounding boxes.
- **Reach is an item property with a floor.** `AttackRange` gives a weapon
  a minimum range too, so a weapon can be *too close* to swing, and the
  creative values are separate. The server adds a flat 3.0 blocks of
  leniency on top.
- **The client's own attack is silent.** `ClientLevel.playSeededSound`
  plays a sound only when the excluded player *is* the local player, and
  `Player.playServerSideSound` excludes nobody — so every hit sound the
  attacker hears arrives as a `ClientboundSoundPacket`, one round trip
  late.
- **`Player.getEnchantedDamage` does nothing on `Player`.** It returns its
  argument unchanged; only `ServerPlayer` overrides it. Every client-side
  `Player` — including your own `LocalPlayer` — computes a zero
  enchantment bonus, so client-side prediction systematically
  under-estimates enchanted damage.
- **The cooldown curve is applied twice, differently.** Base damage gets
  a quadratic ramp; the enchantment bonus gets a linear one.
- **The ticker resets mid-method,** and the client resets it a *second*
  time after `Player.attack` returns while the server resets it once.
- **`ClientboundDamageEventPacket` carries no amount.** The victim's red
  flash, hurt sound and twenty-tick invulnerability are all reconstructed
  from a damage-type holder and two entity ids. The client never learns
  how much damage anyone but itself took; health bars come from
  [synched entity data](../entities/synched-entity-data.md).
- **Sweep and knockback are attributes, not enchantments.**
  `Attributes.SWEEPING_DAMAGE_RATIO` defaults to zero, so a vanilla sweep
  does a flat 1.0.
- **There is a second melee path that never touches `Player.attack`.**
  A `PiercingWeapon` short-circuits before the hit-result switch, travels
  as a `ServerboundPlayerActionPacket` with **no target id at all**, and
  the server redoes the raycast itself into `LivingEntity.stabAttack`. For
  those weapons the client's hit result is irrelevant.
- **The swing is not echoed to the swinger.**
  `ServerGamePacketListenerImpl.handleAnimate` broadcasts
  `ClientboundAnimatePacket` to trackers only — but crit particles *are*
  sent back, because they go to the trackers of the **attacker** while
  naming the **victim**.
- **Swing duration is a data component** (`SwingAnimation`), not a
  constant six ticks, and `MobEffects.MINING_FATIGUE` stretches it.

## Where to look

`Minecraft` · `LocalPlayer` · `MultiPlayerGameMode` ·
`ServerboundAttackPacket` · `ServerGamePacketListenerImpl` · `Player` ·
`AttackRange` · `PiercingWeapon` · `Weapon` · `ProjectileUtil` ·
`LivingEntity` · `EnchantmentHelper` · `ClientboundDamageEventPacket` ·
`ClientboundAnimatePacket` · `SwingAnimation`

---

*Rules: names, never code · how the system works, not how the code reads ·
newest version only · every backticked name passes `tools/verify_names.py`.*
