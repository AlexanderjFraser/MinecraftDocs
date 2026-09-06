# The spear

> Verified against **Minecraft 26.2** · Part VIII · Two ways to hit something with the same item: jab it, and the client sends no target at all; charge it and run, and the damage comes from how fast the gap is closing.

A spear is one item with two weapons in it. Left-click and you **stab**: the
client sends a packet with no entity id in it, and the server does its own
raycast and hits *everything* along the ray. Hold right-click and you
**charge**: the spear becomes an item you are using, like a bow, except that
what it does each tick is look for entities in front of you and hurt them in
proportion to the closing speed. Neither path goes anywhere near
`Player.attack`, the method [the sword
swing](the-sword-swing.md#the-damage-one-number-two-curves-one-order) is about,
and the second one has a property no other melee attack in the game has —
**a charging spear ignores the attack-strength cooldown entirely**, because
the code that applies the cooldown curves is skipped for the item you are
currently using.

## The cast

| class | what it decides | thread |
|---|---|---|
| `PiercingWeapon` | the stab: who can be hit along a ray, and what a hit does | server main (sounds: both) |
| `KineticWeapon` | the charge: three speed conditions, and the damage from closing speed | server main |
| `Item.Properties.spear` | the seven spears, and the combat components that make one | — |
| `Minecraft` / `MultiPlayerGameMode` | the client's short-circuit, and the packet with no target | client main |
| `ServerGamePacketListenerImpl` | `ServerboundPlayerActionPacket.Action.STAB`, and the piercing rejection in the ordinary attack handler | server main |
| `LivingEntity.stabAttack` | the shared tail: damage, two knockbacks, dismount, durability | server main |
| `Player.stabAttack` | the override that adds the cooldown curves — sometimes | server main |
| `SpearUseGoal` / `SpearAttack` | how a zombie or a piglin does the same thing | server main |

## What an item needs to be a spear

`Item.Properties.spear` is one builder call per material, and the seven
spears — `Items.WOODEN_SPEAR` through `Items.NETHERITE_SPEAR` — differ
almost only in the numbers it is given; the wooden one gets its own sounds
and the netherite one is additionally fire-resistant. What it attaches is the interesting part,
because it is *both* weapons at once plus the reach to use them:

| component | what the spear gets |
|---|---|
| `DataComponents.PIERCING_WEAPON` | knockback yes, dismount no, a use sound and a hit sound |
| `DataComponents.KINETIC_WEAPON` | a contact cooldown of ten ticks, a delay, three conditions, and a damage multiplier |
| `DataComponents.ATTACK_RANGE` | `AttackRange.minReach` of 2.0 and `AttackRange.maxReach` of 4.5 — 2.0 and 6.5 in creative — with a hitbox margin and a mob factor |
| `DataComponents.MINIMUM_ATTACK_CHARGE` | 1.0: no partial-charge stab |
| `DataComponents.SWING_ANIMATION` | `SwingAnimationType.STAB`, with a per-material duration |
| `DataComponents.DAMAGE_TYPE` | `DamageTypes.SPEAR`, as a delayed holder component |
| `DataComponents.USE_EFFECTS` | the whole component overridden: sprint allowed, vibrations off, speed multiplier one — the only item in the game that does not slow you down while you hold it out |
| `DataComponents.WEAPON` | a durability cost of one per attack |
| attribute modifiers | `Attributes.ATTACK_DAMAGE` from the material, and an `Attributes.ATTACK_SPEED` derived from the swing duration |

Those nine are what makes a spear a *weapon*. The ordinary tool components
come from the material and are not in the table:
`Item.Properties.spear` also calls `Item.Properties.durability`,
`Item.Properties.repairable` and `Item.Properties.enchantable`, so a spear
takes damage, mends on an anvil and accepts enchantments the way any tool
does ([items and stacks](../items/items-and-stacks.md#the-cast) and
[enchanting](../items/enchanting.md#the-one-question-all-five-ask)).

That `UseEffects` override is why a spear feels unlike every other held-down
item — `LocalPlayer.isSlowDueToUsingItem` is the reader it turns off, and
[using an item](../items/using-an-item.md#moving-while-you-use) explains what
the component does for everything else.

## Two entries, one exit

```mermaid
flowchart TD
    CLICK["left-click: Minecraft.startAttack"]
    HAS["main hand has PIERCING_WEAPON?"]
    NORMAL["the ordinary path: MultiPlayerGameMode.attack, then Player.attack"]
    PA["MultiPlayerGameMode.piercingAttack — plays the sound, resets the ticker locally"]
    PKT["ServerboundPlayerActionPacket, Action.STAB — no entity id, a dummy position"]
    SGPL["handlePlayerAction: not a spectator, cannotAttackWithItem with a 5-tick tolerance"]
    PW["PiercingWeapon.attack — the server's own raycast"]
    USE["right-click: Item.use sees KINETIC_WEAPON, startUsingItem for 72000 ticks"]
    TICK["every use tick: ItemStack.onUseTick, server side only"]
    KW["KineticWeapon.damageEntities — ticksUsed, look vector, closing speed"]
    RAY["ProjectileUtil.getHitEntitiesAlong — every entity on the ray, filtered by PiercingWeapon.canHitEntity"]
    STAB["stabAttack — damage, two knockbacks, dismount, durability"]
    CLICK --> HAS
    HAS -- "no" --> NORMAL
    HAS -- "yes" --> PA
    PA --> PKT
    PKT --> SGPL
    SGPL --> PW
    USE --> TICK
    TICK --> KW
    PW --> RAY
    KW --> RAY
    RAY --> STAB
```

Two things in that picture are worth stopping on. The **client tells the
server nothing about the target** on the stab path: the packet is a
`ServerboundPlayerActionPacket` carrying
`ServerboundPlayerActionPacket.Action.STAB`, whose block position and
direction are dummies, and every question about what was hit is answered by
the server's own raycast. And the ordinary attack handler *refuses* a
piercing weapon — `ServerGamePacketListenerImpl.handleAttack` checks for
`DataComponents.PIERCING_WEAPON` and drops out — so the two paths cannot be
confused for one another even by a client that tries.

## The stab

`PiercingWeapon.attack` takes the attacker's `Attributes.ATTACK_DAMAGE`,
the weapon in the given slot and `LivingEntity.getAttackRangeWith`, and
walks `ProjectileUtil.getHitEntitiesAlong` with the block-collider clip
context — so a wall stops the ray, but a crowd does not. **Every** entity
along it is stabbed — in the order the ray walk happened to append them,
which is not sorted by distance — each through `LivingEntity.stabAttack`
with the same damage figure.

`PiercingWeapon.canHitEntity` is the filter, and it is a projectile-shaped
test rather than a melee one: the target must not be
`Entity.isInvulnerableToPiercingWeapon`, must be alive, and must satisfy
`Entity.canBeHitByProjectile`. Player against player defers to
`Player.canHarmPlayer`, and an entity riding the same vehicle as the
attacker is not hit. An `Interaction` short-circuits the whole filter to
*hittable* before any of those tests, same vehicle included.

Afterwards the attacker gets `LivingEntity.onAttack` — which on a `Player`
resets the attack-strength ticker — and `LivingEntity.postPiercingAttack`,
the hook that runs `EnchantmentHelper.doPostPiercingAttackEffects`; only
then does the weapon play `PiercingWeapon.makeHitSound` if anything was hit
and `PiercingWeapon.makeSound` regardless, and swing the arm. The client
half did the swing and `LivingEntity.onAttack` itself a round trip earlier,
but not `LivingEntity.postPiercingAttack`, which does nothing off a
`ServerLevel`.

## The charge

A kinetic weapon is *used*, not swung. `Item.use` sees
`DataComponents.KINETIC_WEAPON`, calls `LivingEntity.startUsingItem` and
plays the sound; `Item.getUseDuration` returns **72000** for it, the same
effectively-endless duration a bow gets, so the charge ends only when you
release ([using an
item](../items/using-an-item.md#the-bow-tick-by-tick)). Starting also
allocates `LivingEntity.recentKineticEnemies`, a server-side map of who has
been hit and when, which `LivingEntity.stopUsingItem` throws away.

Each use tick, `ItemStack.onUseTick` diverts to
`KineticWeapon.damageEntities` — **and skips the item's own
`Item.onUseTick` when it does**. What that method computes is a speed
argument, not a swing:

- **How long you have been charging.** Ticks used must be at least
  `KineticWeapon.delayTicks`; everything below is measured from there.
- **How fast you are going, along your look vector.**
  `KineticWeapon.getMotion` reads `Entity.getKnownSpeed` — the *reported*
  movement from [input to movement](input-to-movement.md) — scaled to
  blocks per second, taking the **root vehicle's** motion for a
  non-player passenger ([input to
  movement](input-to-movement.md#the-trace-w-is-pressed)).
- **How fast the gap is closing.** The target's own projected speed is
  subtracted, floored at zero, and that relative speed is what the damage
  is built from.
- **Whether you already hit them.** `LivingEntity.wasRecentlyStabbed`
  against `KineticWeapon.contactCooldownTicks` — ten for a spear — is why
  running through a crowd does not hit the same mob every tick.

Who is in front of you is answered exactly as it is for the stab:
`ProjectileUtil.getHitEntitiesAlong` walks the weapon's `AttackRange` with
the block-collider clip context and `PiercingWeapon.canHitEntity` filters
what it finds. The two attacks differ in what they compute, never in what
they can reach.

Three independent `KineticWeapon.Condition`s then decide what the hit *is*:
`KineticWeapon.dismountConditions`, `KineticWeapon.knockbackConditions` and
`KineticWeapon.damageConditions`, each a maximum duration and a speed bar —
measured against the attacker's own projected speed for the first two, and
against the closing speed for damage. A spear's three come from the builder
with different windows, and for all seven materials they nest the same way:
damage has the longest window and the lowest bar, dismount the shortest
window and much the highest. So a charge that has run too long can still
hurt when it can no longer knock a target off a horse — a wooden spear
dismounts for five seconds, knocks back for ten and damages for fifteen. If any of the three
passes, the damage is the attacker's **base** `Attributes.ATTACK_DAMAGE`
plus the floor of relative speed × `KineticWeapon.damageMultiplier` — base
value, so the modifiers a sword swing would pick up are not in it.

A landed charge broadcasts an entity event, and it is the part of the
telling that is *about the charge*, alongside the ordinary damage sync,
knockback and durability every hit sends: `LivingEntity.onKineticHit` plays a local hit
sound, throttled to ten ticks by a bare literal in
`LivingEntity.onKineticHit` — the `KineticWeapon.HIT_FEEDBACK_TICKS`
constant that names that number is read by nothing — and
`LivingEntity.getTicksSinceLastKineticHitFeedback` feeds the animation. A
`ServerPlayer` also trips `CriteriaTriggers.SPEAR_MOBS_TRIGGER` with the
number of living entities stabbed this charge.

## The tail, and the cooldown that is not applied

Both paths end in a method called *stabAttack*, which exists twice.
`LivingEntity.stabAttack` is the general one: it returns false off a
`ServerLevel`, runs the damage through `EnchantmentHelper.modifyDamage`,
calls `Entity.hurtServer` — into the same pipeline a sword swing ends in
([damage and death](../entities/damage-and-death.md#the-number-the-arrow-decides))
— applies two knockbacks, a flat one and `LivingEntity.getKnockback`,
dismounts the target if the caller asked, runs `ItemStack.hurtEnemy` and the
post-attack enchantment effects
([enchantments](../items/enchantments.md)), and plays the attack sound.

`Player.stabAttack` overrides it, and the override is where the spear
becomes strange. It computes the enchantment boost the way `Player.attack`
does, and then applies the two cooldown curves — the linear one to the
boost, the quadratic `Player.baseDamageScaleFactor` to the base — **only if
the player is not currently using an item in that slot.** A stab qualifies,
so a stab is charged like a sword swing. A kinetic charge does not: while
you are holding the spear out, both curves are skipped and every tick's hit
lands at full base damage. The rest of the override is the familiar tail —
`Player.deflectProjectile` can still end it, the knockbacks are the same
two, `Player.itemAttackInteraction` applies the durability cost, and
`Player.causeFoodExhaustion` charges the same 0.1 a sword does ([hunger and
experience](hunger-and-experience.md#questions-players-ask)).

## Questions players ask

**Why does the server never ask which mob I stabbed?** Because it does not
trust the answer and does not need it. The stab packet is an action, not a
target: the server raycasts from the player's own look vector with the
weapon's `AttackRange`, and hits everything on the line. That also puts the stab
in the small company of melee attacks whose hit count is not one, beside the
sword's sweep and the spear's own charge.

**Does a spear work while I am moving?** It is the only weapon that
*requires* it. The charge's damage is built from closing speed, and the
`UseEffects` override exists so you can sprint while charging — the two
halves of the same design.

**Why did my charge stop hurting the same mob?**
`KineticWeapon.contactCooldownTicks` remembers it for ten ticks. The map is
allocated when you start using the spear and dropped when you stop, so
releasing and re-charging clears everyone.

**Can a mob do this?** Yes, both ways round, and the split is the ordinary
one ([goals and brains](../entities/ai-goals-and-brains.md#what-holds-the-state)).
`SpearUseGoal` drives the charge for a goal-based mob and `SpearApproach`,
`SpearAttack` and `SpearRetreat` do it for a brain-based one — zombies, zombified piglins and
piglins are the users in the tree, and `Piglin` treats a kinetic weapon like
a crossbow when deciding what it is holding. Both read
`KineticWeapon.computeDamageUseDuration` to know how long to hold it. The
thresholds are easier for them: the speed conditions are scaled by an action
factor of **0.2** for anything that is not a player, against 1.0 for you.

**Is any of this data-driven?** The shape is; the values are not.
`PiercingWeapon` and `KineticWeapon` are ordinary data components with
codecs and stream codecs, so a data pack can describe a weapon without code
— but every built-in spear's numbers are hard-coded in
`Item.Properties.spear`, not read from JSON. One field is not a combat
number at all: `KineticWeapon.forwardMovement` — 0.38 for a spear — is read
**only** by `SpearAnimations`, and only by its *third-person* methods, which
is a rendering offset living in the middle of a combat component.

## Where to look

`PiercingWeapon` · `KineticWeapon` · `KineticWeapon.Condition` ·
`Item.Properties.spear` · `Minecraft.startAttack` ·
`MultiPlayerGameMode.piercingAttack` · `ServerboundPlayerActionPacket` ·
`LivingEntity.stabAttack` · `Player.stabAttack` ·
`LivingEntity.recentKineticEnemies` · `ProjectileUtil.getHitEntitiesAlong` ·
`SpearUseGoal` · `SpearAnimations`

---

*Rules: names, never code · how the system works, not how the code reads ·
newest version only · every backticked name passes `tools/verify_names.py`.*
