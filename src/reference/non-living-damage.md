# Damage outside `LivingEntity`

> Verified against **Minecraft 26.2** · Reference · Hand-kept from
> `net/minecraft/world/entity/**`.

`Entity.hurtServer` is **abstract**, so every branch has to answer for itself.
The twenty-one classes are every non-`LivingEntity` class that declares it, and
they answer with rules that share nothing with `LivingEntity`'s — no armour, no
invulnerability window, no `CombatTracker`, no death sequence. The lecture that
frames them is [damage and
death](../systems/entities/damage-and-death.md#twenty-one-classes-with-no-pipeline-at-all);
this is the per-class table.

The last column is the client half. `Entity.hurtClient` has a default — it
returns false — and **thirteen** of the twenty-one inherit it unchanged; seven
declare their own and `MinecartTNT` inherits `VehicleEntity`'s. It never reads
the damage amount, because there is none on that side: it answers only whether
a client-side swing should play its own effects.

Two gates run before any of them is asked anything — `Player.cannotAttack`
and `Player.deflectProjectile` — and they are why several rows below read
*nothing*: the class was never reached ([the sword
swing](../systems/player/the-sword-swing.md#the-damage-one-number-two-curves-one-order)
owns both). `Entity.hurtOrSimulate` is what `Player.attack` calls after them,
and it picks `Entity.hurtServer` or `Entity.hurtClient` off the level.

| class | what it checks first | what it does | returns | `Entity.hurtClient` |
|---|---|---|---|---|
| `AreaEffectCloud` | — | nothing | false | false |
| `Display` | — | nothing | false | false |
| `Interaction` | — | nothing; the attacker was already recorded in `Entity.skipAttackInteraction` | false | false |
| `LightningBolt` | — | nothing | false | false |
| `Marker` | — | nothing | false | false |
| `OminousItemSpawner` | — | nothing | false | false |
| `PrimedTnt` | — | nothing: a lit TNT block cannot be shot out of the air | false | false |
| `EvokerFangs` | — | nothing | false | false |
| `EyeOfEnder` | — | nothing | false | false |
| `AbstractHurtingProjectile` | — | nothing — a fireball or a wind charge is deflected before this is reached, and the rest are unhittable by `Entity.isPickable` | false | false |
| `Projectile` | `Entity.isInvulnerableToBase` | `Entity.markHurt` only, so the client sees a flinch and nothing changes | false | false |
| `FallingBlockEntity` | `Entity.isInvulnerableToBase` | `Entity.markHurt` only | false | false |
| `ExperienceOrb` | `Entity.isInvulnerableToBase` | subtracts the damage from an int of health, `Entity.discard` at zero | true | not invulnerable |
| `ItemEntity` | `Entity.isInvulnerableToBase`, then a `Mob` source under `GameRules.MOB_GRIEFING`, then `ItemStack.canBeHurtBy` | same int of health, plus `GameEvent.ENTITY_DAMAGE`, and `ItemStack.onDestroyed` before the discard | true | not invulnerable, and `ItemStack.canBeHurtBy` agrees |
| `BlockAttachedEntity` | `Entity.isInvulnerableToBase`, then a `Mob` source under `GameRules.MOB_GRIEFING` | `Entity.kill`, `Entity.markHurt`, and drops its item — one hit, whatever the amount | true | not invulnerable |
| `ItemFrame` | `ItemFrame.fixed` gates everything: a fixed frame is hurt only by `DamageTypeTags.BYPASSES_INVULNERABILITY` or a creative player | a non-explosion hit on a frame **holding** something pops the item and stops there; otherwise it falls through to `BlockAttachedEntity` and the frame breaks | true | the fixed gate first, then not invulnerable |
| `EndCrystal` | `Entity.isInvulnerableToBase`, then **is the source an `EnderDragon`** | removes itself with `Entity.RemovalReason.KILLED` and explodes with power 6 — unless the source was already an explosion — then `EndCrystal.onDestroyedBy` | true | not invulnerable, and not the dragon |
| `ShulkerBullet` | — | plays `SoundEvents.SHULKER_BULLET_HURT`, spawns fifteen `ParticleTypes.CRIT`, destroys itself | true | **true**, unconditionally |
| `EnderDragonPart` | `Entity.isInvulnerableToBase` | forwards the whole call to `EnderDragon.hurt` with itself as the part that was hit | the parent's answer | false |
| `VehicleEntity` | already removed, then `Entity.isInvulnerableToBase` | `VehicleEntity.setDamage` adds *damage × 10*, after flipping the hurt direction and setting ten ticks of hurt time; past 40 it is destroyed. A creative player gets all of that too — the flag only redirects the destruction to `Entity.discard`, which drops nothing | true | **true**, unconditionally |
| `MinecartTNT` | a **burning** `AbstractArrow` as the direct entity explodes it, scaled by the arrow's speed | on that path, nothing else: the explosion calls `Entity.discard`, so `VehicleEntity.hurtServer` returns at its already-removed test. Any other source falls through to everything `VehicleEntity` does | true | inherited: true |

Six patterns account for all of it: *nothing happens* (ten classes), *a
flinch and nothing else* (two), *an int of health with no armour and no
window* (two), *one hit destroys* (four), *an accumulator* (two), and
*forward it to something else* (one, the dragon part). The classes that read
the damage **amount** at all are the pair with an int of health, the
accumulator pair, and `EnderDragonPart`, which hands the number to the dragon;
everything else is a yes-or-no.

---

*Rules: names, never code · how the system works, not how the code reads ·
newest version only · every backticked name passes `tools/verify_names.py`.*
