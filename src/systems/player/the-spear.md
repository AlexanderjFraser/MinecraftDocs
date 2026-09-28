# The spear

> Verified against **Minecraft 26.3** · Part VIII · Two ways to hit something with the same item: jab it, and the client sends no target at all; charge it and run, and the damage comes from how fast the gap is closing.

A spear is one item with two weapons in it. Left-click and you **stab**: the
client sends a packet with no entity id in it, and the server does its own
raycast and hits *everything* along the ray. Hold right-click and you
**charge**: the spear becomes an item you are using, like a bow, except that
what it does each tick is look for entities in front of you and hurt them by
an amount that grows with the closing speed. Neither path enters `Player.attack`, the
method [the sword
swing](the-sword-swing.md#the-damage-one-number-two-curves-one-order) is
about, and the second has a property no other melee attack in the game has.
Every ordinary swing is scaled by how far the attack-strength clock has
recharged — quadratically on the base damage, linearly on the enchantment
bonus, so a sword swung at half charge does 40% of its base damage ([the two
clocks](the-sword-swing.md#the-two-clocks-a-swing-is-charged-against)).
**A charging spear ignores that scaling entirely**, because the code that
applies the two curves is skipped for the item you are currently using, and a
charge is a use.

## The cast

| class | what it decides | thread |
|---|---|---|
| `PiercingWeapon` | the stab — and, through its filter, who *either* weapon is allowed to hit along a ray | Server (its attack sound plays on both sides) |
| `KineticWeapon` | the charge: three speed conditions, and the damage from closing speed | Server |
| `Item.Properties.spear` | the seven spears, and the combat components that make one | — |
| `Minecraft` / `MultiPlayerGameMode` | the client's short-circuit, and the packet with no target | Render |
| `ServerGamePacketListenerImpl` | `ServerboundPlayerActionPacket.Action.STAB`, and the piercing rejection in the ordinary attack handler | Server |
| `LivingEntity.stabAttack` | the general tail — damage, two knockbacks, dismount — which only a mob's charge runs | Server |
| `Player.stabAttack` | a player's whole tail instead, durability included, with the cooldown curves — sometimes | Server |
| `SpearUseGoal` / `SpearAttack` | how a zombie or a piglin runs the charge | Server |

## What an item needs to be a spear

`Item.Properties.spear` is one builder call per material, and the seven
spears — `Items.WOODEN_SPEAR` through `Items.NETHERITE_SPEAR` — differ
almost only in the numbers it is given; the wooden one gets its own sounds
and burns as fuel, and the netherite one is fire-resistant. What it attaches is the interesting part,
because it is *both* weapons at once plus the reach to use them:

| component | what the spear gets |
|---|---|
| `DataComponents.PIERCING_WEAPON` | knockback yes, dismount no, an attack sound and a hit sound |
| `DataComponents.KINETIC_WEAPON` | a contact cooldown of ten ticks, a delay, three conditions, and a damage multiplier |
| `DataComponents.ATTACK_RANGE` | `AttackRange.minReach` of 2.0 and `AttackRange.maxReach` of 4.5 — 2.0 and 6.5 in creative — with a hitbox margin and a mob factor |
| `DataComponents.MINIMUM_ATTACK_CHARGE` | 1.0: no stab before the attack clock is full |
| `DataComponents.ATTACK_ANIMATION` | `SwingAnimationType.STAB`, with a per-material duration |
| `DataComponents.DAMAGE_TYPE` | `DamageTypes.SPEAR`, as a delayed holder component |
| `DataComponents.USE_EFFECTS` | the whole component overridden: sprint allowed, vibrations off, speed multiplier one — the one definition in the game, shared by the seven spears, that does not slow you down while you hold it out |
| `DataComponents.WEAPON` | a durability cost of one per attack |
| attribute modifiers | `Attributes.ATTACK_DAMAGE` from the material, and an `Attributes.ATTACK_SPEED` derived from the swing duration |

Four of those rows are what the rest of this page is about — the two weapon
components, the reach they share, and the `UseEffects` override. The other
five are what stops a spear behaving oddly in the hand: no stab before the
attack clock is full, a stab animation rather than a slash, its own damage type in the death
message, a durability cost of one per attack, and the attack damage and speed
its attribute modifiers set.

The ordinary tool components come from the material and are not in the table:
`Item.Properties.spear` also calls `Item.Properties.durability`,
`Item.Properties.repairable` and `Item.Properties.enchantable`, so a spear
takes damage, mends on an anvil and accepts enchantments the way any tool
does ([items and stacks](../items/items-and-stacks.md#the-cast) and
[enchanting](../items/enchanting.md#the-one-question-all-five-ask)).

That `UseEffects` override is why a spear feels unlike every other held-down
item — `LocalPlayer.itemUseSpeedMultiplier` and
`LocalPlayer.isSlowDueToUsingItem` are the readers it turns off, and
[using an item](../items/using-an-item.md#moving-while-you-use) explains what
the component does for everything else.

## Two entries, one exit

```mermaid
flowchart TD
    CLICK["left-click: Minecraft.startAttack"]
    HAS{"main hand:<br/>PIERCING_WEAPON?"}
    NORMAL["the ordinary path: MultiPlayerGameMode.attack, then Player.attack"]
    REFUSE["and ServerGamePacketListenerImpl.handleAttack refuses a piercing weapon"]
    PA["MultiPlayerGameMode.piercingAttack — the sound, and the ticker locally"]
    PKT["ServerboundPlayerActionPacket.Action.STAB — no entity id, a dummy position"]
    SGPL["ServerGamePacketListenerImpl.handlePlayerAction — not a spectator, and Player.cannotAttackWithItem with a 5-tick tolerance"]
    PW["PiercingWeapon.attack — the server's own raycast"]
    USE["right-click: Item.use sees KINETIC_WEAPON, then LivingEntity.startUsingItem"]
    TICK["ItemStack.onUseTick, every use tick of the 72000"]
    KW["KineticWeapon.damageEntities — server side only: the ticks used, the look vector, the closing speed"]
    RAY["ProjectileUtil.getHitEntitiesAlong — every entity on the ray, filtered by PiercingWeapon.canHitEntity"]
    STAB["Player.stabAttack — or a mob's LivingEntity.stabAttack"]
    CLICK --> HAS
    HAS -- "no" --> NORMAL
    NORMAL --> REFUSE
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

*Two entries — a click on the left, a held right-click on the right — meeting
at one raycast, and the only place the two columns touch is that meeting: the
left column's refusal node is the reason a client cannot route a stab down the
ordinary path.*

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
along it is stabbed — in the order the search of the box around the ray
returned them, which is not sorted by distance — each through the attacker's
`Player.stabAttack` with the same damage figure.

`PiercingWeapon.canHitEntity` is the filter, and it is a projectile-shaped
test rather than a melee one: the target must not be
`Entity.isInvulnerableToPiercingWeapon`, must be alive, and must satisfy
`Entity.canBeHitByProjectile`. Player against player defers to
`Player.canHarmPlayer`, and an entity riding the same vehicle as the
attacker is not hit. An `Interaction` — the invisible click-target entity a
data pack places to catch hits — short-circuits the rest of the filter to
*hittable* once it is alive and not immune, same vehicle included. And
`Player.stabAttack` still puts the melee gate, `Player.cannotAttack`, to every
target the filter lets through.

Afterwards the attacker gets `LivingEntity.onAttack` — which on a `Player`
resets the attack-strength ticker — and `LivingEntity.postPiercingAttack`,
the hook that runs `EnchantmentHelper.doPostPiercingAttackEffects`; only
then does the weapon play `PiercingWeapon.makeHitSound` if anything was hit
and `PiercingWeapon.makeSound` regardless, and swing the arm. The client
half did the swing and `LivingEntity.onAttack` itself as it sent the packet,
and called `LivingEntity.postPiercingAttack` too, which does nothing off a
`ServerLevel`.

## The charge

A spear's kinetic weapon is built on speed: its damage comes from how fast the
gap is closing, its dismount and knockback need you to be moving, and the
`UseEffects` override above exists so that you can sprint while charging. The
two halves are one design.

A kinetic weapon is also *used*, not swung. `Item.use` sees
`DataComponents.KINETIC_WEAPON`, calls `LivingEntity.startUsingItem` and
plays the sound; `Item.getUseDuration` returns **72000** for it, the same effectively-endless duration a bow gets, so in play the charge runs
until you release it, the spear leaves your hand, or you die or change
dimension ([using an
item](../items/using-an-item.md#the-bow-tick-by-tick)). Starting also
allocates `LivingEntity.recentKineticEnemies`, a server-side map of who the
charge has reached and when, which `LivingEntity.stopUsingItem` throws away.

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
  movement](input-to-movement.md#where-the-velocity-everything-downstream-reads-comes-from)).
- **How fast the gap is closing.** The target's own projected speed is
  subtracted, floored at zero, and that relative speed is what the damage
  is built from.
- **Whether you already reached them.** `LivingEntity.wasRecentlyStabbed`
  against `KineticWeapon.contactCooldownTicks` — ten for a spear — is why
  running through a crowd does not hit the same mob every tick.

Who is in front of you is answered exactly as it is for the stab:
`ProjectileUtil.getHitEntitiesAlong` walks the weapon's `AttackRange` with
the block-collider clip context and `PiercingWeapon.canHitEntity` filters
what it finds. The two attacks differ in what they compute, never in what
they can reach.

Three independent `KineticWeapon.Condition`s then decide what the hit *is*,
and the point is that each gates its own effect rather than the hit as a
whole: `KineticWeapon.dismountConditions`, `KineticWeapon.knockbackConditions`
and `KineticWeapon.damageConditions`. Each is a maximum duration and two speed
bars, one on the attacker's own projected speed and one on the closing speed;
a spear's first two set the first bar and its damage condition the second. If **any** of the three passes the
attack happens at all; then the dismount only dismounts if its own condition
passed, the knockbacks only fire if theirs did, and **the damage is only
dealt if the damage condition passed**. A charge can knock a target off a horse and deal it no damage.

A spear's three come from the builder with different windows, and for all
seven materials they nest the same way: damage has the longest window and the
lowest threshold (on the closing speed), dismount the shortest window and much
the highest. A wooden spear
dismounts for five seconds, knocks back for ten and damages for fifteen — so
a charge that has run too long can still hurt when it can no longer unseat
anyone. When the damage does land it is the attacker's **base**
`Attributes.ATTACK_DAMAGE` plus the floor of relative speed ×
`KineticWeapon.damageMultiplier` — the base value, so the modifiers a sword
swing would pick up are not in it.

A landed charge broadcasts an entity event, and it is the part of the
telling that is *about the charge*, alongside the ordinary damage sync,
knockback and, for a player, durability that every hit sends:
`LivingEntity.onKineticHit` plays a local hit sound, never within ten ticks of
the last — the number `KineticWeapon.HIT_FEEDBACK_TICKS` names — and
`LivingEntity.getTicksSinceLastKineticHitFeedback` feeds the animation. A
`ServerPlayer` also trips `CriteriaTriggers.SPEAR_MOBS_TRIGGER` with the
number of living entities the charge has reached.

## The tail, and the cooldown that is not applied

Both paths end in a method called *stabAttack*, which exists twice.
`LivingEntity.stabAttack` is the general one, and a mob's charge is the only
thing that runs it: it returns false off a
`ServerLevel`, runs the damage through `EnchantmentHelper.modifyDamage`,
calls `Entity.hurtServer` — into the same pipeline a sword swing ends in
([damage and death](../entities/damage-and-death.md#the-number-the-arrow-decides))
— applies two knockbacks, a flat one and `LivingEntity.getKnockback`, and
dismounts the target, each of the three behind its own flag. Two things then
run on different conditions again: `ItemStack.hurtEnemy` for any living
target whether or not the damage landed, and the post-attack enchantment
effects ([enchantments](../items/enchantments.md)) only if it did. The attack
sound plays once anything at all happened.

`Player.stabAttack` overrides it whole, never calling it, and the override is
where the spear becomes strange. It computes the enchantment boost the way `Player.attack`
does, and then applies the two cooldown curves — the linear one to the
boost, the quadratic `Player.baseDamageScaleFactor` to the base — **only if
the player is not currently using an item in that slot.** A stab qualifies,
so a stab is charged like a sword swing. A kinetic charge does not: while
you are holding the spear out, both curves are skipped and every tick's hit
lands at full base damage. The rest of the override is the familiar tail —
`Player.deflectProjectile` can still end it, the knockbacks are the same
two, `Player.itemAttackInteraction` applies the durability cost, and
`Player.causeFoodExhaustion` charges the same 0.1 a sword does ([hunger and
experience](hunger-and-experience.md#the-food-bar-is-four-numbers-and-a-file-of-constants)).

## What a mob does with the same item

A mob runs only the charge — the stab reaches `PiercingWeapon.attack` only
from a player's packet — and the split between the two ways it can run it is
the ordinary one ([goals and brains](../entities/ai-goals-and-brains.md#what-holds-the-state)).
`SpearUseGoal` drives the charge for a goal-based mob; `SpearApproach`,
`SpearAttack` and `SpearRetreat` do it for a brain-based one. Zombies,
zombified piglins and piglins are the users in the tree, and `Piglin` treats
a kinetic weapon like a crossbow when deciding what it is holding. Both
paths read `KineticWeapon.computeDamageUseDuration` — the delay plus the
damage condition's window — to know how long to hold the charge for.

The thresholds are far easier for them than for you. Every speed bar in the
three conditions is multiplied by an action factor of **0.2** for anything
that is not a player, against 1.0 for you: a mob charging at a fifth of your
speed clears the same bar.

## What a data pack can and cannot change here

The shape is data-driven; the values are not. `PiercingWeapon` and
`KineticWeapon` are ordinary data components with codecs and stream codecs,
so a data pack can describe a weapon of either kind without code — but every
built-in spear's numbers are hard-coded (the shared ones in
`Item.Properties.spear`, the per-material ones where `Items` registers each
spear and in its `ToolMaterial`) rather than read from JSON, which is why the seven differ almost only
in arithmetic.

One field in `KineticWeapon` is not a combat number at all.
`KineticWeapon.forwardMovement` — 0.38 for a spear — is read **only** by
`SpearAnimations`, and only by its *third-person* methods: a rendering offset
living in the middle of a combat component, shipped to every client that
receives the item.

## Where to look

**`Item.Properties.spear`** is one statement and is the whole definition of
the weapon — read it first, with the numbers for one material in hand. Then
the two components it hangs on: **`PiercingWeapon`**, whose
`PiercingWeapon.canHitEntity` filter serves both attacks, and
**`KineticWeapon`**, whose `KineticWeapon.damageEntities` is the charge end
to end and whose nested **`KineticWeapon.Condition`** is three fields and one
test.

The exit is worth reading as a pair: **`LivingEntity.stabAttack`** for what a
mob's charge does to a target, then **`Player.stabAttack`** for the override a
player runs instead, which puts the cooldown curves back — and the one
condition that skips them. On the way in,
**`MultiPlayerGameMode.piercingAttack`** and
**`ServerboundPlayerActionPacket`** show how little the client sends, and
**`Minecraft.startAttack`** is where the short-circuit sits. Two doors this
page only points at: **`SpearUseGoal`** for the mob side, and
**`SpearAnimations`**, which turns out to be the only reader of a field in
the combat component.

---

*Rules: names, never code · how the system works, not how the code reads ·
newest version only · every backticked name passes `tools/verify_names.py`.*
