# Damage outside `LivingEntity`

> Verified against **Minecraft 26.3** · Reference · Hand-kept from
> `net/minecraft/world/entity/**`.

`Entity.hurtServer` is **abstract**, so every branch has to answer for itself.
The twenty-two classes are every non-`LivingEntity` class that declares it, and
none of them runs `LivingEntity`'s rules itself — no armour, no
hurt cooldown, no `CombatTracker`, no death sequence. The lecture that
frames them is [damage and
death](../systems/entities/damage-and-death.md#twenty-two-classes-with-no-pipeline-at-all);
this is the per-class table.

The last column is the client half. `Entity.hurtClient` has a default — it
returns false — and **thirteen** of the twenty-two inherit it unchanged; eight
declare their own and `MinecartTNT` inherits `VehicleEntity`'s. It is never handed the damage amount — `Entity.hurtOrSimulate` drops it on the client — and it answers whether the client should play a hit's effects itself, for its own swing and for a projectile hit it simulates.

A swing reaches about half of these. The client picks only an entity whose `Entity.isPickable` is true, which among the twenty-two is `Interaction`, `PrimedTnt`, `FallingBlockEntity`, the three projectiles a player can deflect, the attached blocks, `EndCrystal`, `ShulkerBullet`, `EnderDragonPart` and the vehicles. Two gates follow in `Player.attack`, which the client runs as it sends the attack and the server runs again — `Player.cannotAttack` and `Player.deflectProjectile` ([the sword swing](../systems/player/the-sword-swing.md#the-damage-one-number-two-curves-one-order) owns both). The first refuses a class whose `Entity.isAttackable` is false (`EyeOfEnder`, `FallingBlockEntity`, `ExperienceOrb`, `ItemEntity`, and in the projectile row a firework, every arrow and a thrown trident — though the server disconnects a player whose attack names an item, an orb or an arrow before `Player.attack` runs) or whose `Entity.skipAttackInteraction` answers true (`Interaction` while its response flag is off; `BlockAttachedEntity` answers true outright for a player who may not interact at its position, and otherwise by running its own hurt with no damage). The second deflects those three projectiles, except a player's `WindCharge` in its first five ticks, which refuses. Three rows below name their gate in the second column; `PrimedTnt` is the one *nothing* row a swing always reaches, and `Interaction` with its response flag on and a wind charge in its first five ticks reach theirs too; each `Entity.hurtServer` then does nothing. `Entity.hurtOrSimulate` is what `Player.attack` calls after the gates,
and it picks `Entity.hurtServer` or `Entity.hurtClient` off the level.

| class | what it checks first | what it does | returns | `Entity.hurtClient` |
|---|---|---|---|---|
| `AreaEffectCloud` | — | nothing | false | false |
| `Display` | — | nothing | false | false |
| `Interaction` | **not reached** while its response flag is off — `Entity.skipAttackInteraction` answers the flag's negation, after recording the attacker | nothing | false | false |
| `LightningBolt` | — | nothing | false | false |
| `Marker` | — | nothing | false | false |
| `OminousItemSpawner` | — | nothing | false | false |
| `PrimedTnt` | — | nothing: a lit TNT block cannot be shot out of the air | false | false |
| `EvokerFangs` | — | nothing | false | false |
| `EyeOfEnder` | **never reached** — `Entity.isAttackable` returns false | nothing | false | false |
| `AbstractHurtingProjectile` | **not reached** but by a player's wind charge in its first five ticks — a large fireball or a wind charge is otherwise deflected, and the rest are unhittable by `Entity.isPickable` | nothing | false | false |
| `Projectile` | `Entity.isInvulnerableToBase` | `Entity.markHurt` only, so the client is sent the entity's motion again and nothing changes | false | false |
| `FallingBlockEntity` | `Entity.isInvulnerableToBase` | `Entity.markHurt` only | false | false |
| `ExperienceOrb` | `Entity.isInvulnerableToBase` | subtracts the damage from an int of health, `Entity.discard` at zero | true | not invulnerable |
| `ItemEntity` | `Entity.isInvulnerableToBase`, then a `Mob` source under `GameRules.MOB_GRIEFING`, then `ItemStack.canBeHurtBy` | same int of health, plus `GameEvent.ENTITY_DAMAGE`, and `ItemStack.onDestroyed` before the discard | true | not invulnerable, and `ItemStack.canBeHurtBy` agrees |
| `BlockAttachedEntity` | `Entity.isInvulnerableToBase`, then a `Mob` source under `GameRules.MOB_GRIEFING` | `BlockAttachedEntity.kill`, `Entity.markHurt`, and `BlockAttachedEntity.dropItem` — one hit, whatever the amount; a leash knot's drop is only a sound | true | not invulnerable |
| `Cushion` | a `Player` source that may not build, or may not interact at the cushion's position, is refused | otherwise `BlockAttachedEntity`'s one hit | true, or false when refused or under `BlockAttachedEntity`'s own gates | false for a player who may not build, then `BlockAttachedEntity`'s |
| `ItemFrame` | `ItemFrame.fixed` gates everything: a fixed frame is hurt only by `DamageTypeTags.BYPASSES_INVULNERABILITY` or a creative player | a non-explosion hit on a frame **holding** something pops the item and stops there; otherwise it falls through to `BlockAttachedEntity` and the frame breaks | true | the fixed gate first, then not invulnerable |
| `EndCrystal` | `Entity.isInvulnerableToBase`, then **is the source an `EnderDragon`** | removes itself with `Entity.RemovalReason.KILLED` and explodes with power 6 — unless the source was already an explosion — then `EndCrystal.onDestroyedBy` | true | not invulnerable, and not the dragon |
| `ShulkerBullet` | — | plays `SoundEvents.SHULKER_BULLET_HURT`, spawns fifteen `ParticleTypes.CRIT`, destroys itself | true | **true**, unconditionally |
| `EnderDragonPart` | `Entity.isInvulnerableToBase` | forwards the whole call to `EnderDragon.hurt` with itself as the part that was hit | the parent's answer | false |
| `VehicleEntity` | already removed, then `Entity.isInvulnerableToBase` | `VehicleEntity.setDamage` adds *damage × 10*, after flipping the hurt direction and setting ten ticks of hurt time; past 40 it is destroyed. A creative player gets all of that too, and then the vehicle is discarded at once whatever the accumulator reads — `Entity.discard`, which drops nothing | true | **true**, unconditionally |
| `MinecartTNT` | a **burning** `AbstractArrow` as the direct entity explodes it, scaled by the arrow's speed | on that path, nothing else when `GameRules.TNT_EXPLODES` is on or the cart is primed: the explosion calls `Entity.discard`, so `VehicleEntity.hurtServer` returns at its already-removed test. Any other source runs `VehicleEntity.hurtServer`, except that a fire or explosion source or a burning projectile goes straight to `MinecartTNT.destroy`, which lights the fuse, even for a creative player | true | inherited: true |

Six patterns account for all of it: *nothing happens* (ten classes), *a motion resend and nothing else* (two), *an int of health with no armour and no
hurt cooldown* (two), *one hit destroys* (five, though a non-explosion hit on an unfixed frame holding something takes only the item), *an accumulator* (two), and
*forward it to something else* (one, the dragon part). Only **four** classes
read the damage **amount** at all: the pair with an int of health and the
accumulator pair. `EnderDragonPart` passes the number on without looking at it,
and everything else is a yes-or-no.

---

*Rules: names, never code · how the system works, not how the code reads ·
newest version only · every backticked name passes `tools/verify_names.py`.*
