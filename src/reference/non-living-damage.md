# Damage outside `LivingEntity`

> Verified against **Minecraft 26.2** · Reference · Hand-kept from
> `net/minecraft/world/entity/**`.

`Entity.hurtServer` is **abstract**, so every branch has to answer for itself.
(`Entity.hurtClient`, the other half of the pair, does have a default: it
returns false, and twelve of the rows below inherit it unchanged.) The
twenty-one classes are every non-`LivingEntity` class that declares
`Entity.hurtServer`, and they answer with rules that share nothing with
`LivingEntity`'s — no armour, no invulnerability window, no `CombatTracker`,
no death sequence. The lecture that frames them is [damage and
death](../systems/entities/damage-and-death.md); this is the per-class table.

Two things happen before any of them. `Player.cannotAttack` asks
`Entity.isAttackable` and then `Entity.skipAttackInteraction`, either of which
can end the swing before the entity is asked anything — `Interaction` uses that
hook to record who hit it and `BlockAttachedEntity` to re-enter through
`Entity.hurtOrSimulate` with zero damage. `Entity.hurtOrSimulate` is what
`Player.attack` calls, and it picks `Entity.hurtServer` or `Entity.hurtClient`
off the level;
its answer is not "did the hit land" but "was anything damaged", and it is what
gates the knockback, the sweep, the durability loss and the hit particles.

| class | what it checks first | what it does | returns |
|---|---|---|---|
| `AreaEffectCloud` | — | nothing | false |
| `Display` | — | nothing | false |
| `Interaction` | — | nothing; the attacker was already recorded in `Entity.skipAttackInteraction` | false |
| `LightningBolt` | — | nothing | false |
| `Marker` | — | nothing | false |
| `OminousItemSpawner` | — | nothing | false |
| `PrimedTnt` | — | nothing: a lit TNT block cannot be shot out of the air | false |
| `EvokerFangs` | — | nothing | false |
| `EyeOfEnder` | — | nothing | false |
| `AbstractHurtingProjectile` | — | nothing — but a fireball or a wind charge is *deflected* before this is reached, since `Player.attack` calls `Player.deflectProjectile` first for anything in `EntityTypeTags.REDIRECTABLE_PROJECTILE`; the rest are unhittable by `Entity.isPickable` | false |
| `Projectile` | `Entity.isInvulnerableToBase` | `Entity.markHurt` only, so the client sees a flinch and nothing changes | false |
| `FallingBlockEntity` | `Entity.isInvulnerableToBase` | `Entity.markHurt` only | false |
| `ExperienceOrb` | `Entity.isInvulnerableToBase` | subtracts the damage from an int of health, `Entity.discard` at zero | true |
| `ItemEntity` | `Entity.isInvulnerableToBase`, then a `Mob` source under `GameRules.MOB_GRIEFING`, then `ItemStack.canBeHurtBy` | same int of health, plus `GameEvent.ENTITY_DAMAGE`, and `ItemStack.onDestroyed` before the discard | true |
| `BlockAttachedEntity` | `Entity.isInvulnerableToBase`, then a `Mob` source under `GameRules.MOB_GRIEFING` | `Entity.kill`, `Entity.markHurt`, and drops its item — one hit, whatever the amount | true |
| `ItemFrame` | `ItemFrame.fixed` gates everything: a fixed frame is hurt only by `DamageTypeTags.BYPASSES_INVULNERABILITY` or a creative player | a non-explosion hit on a frame **holding** something pops the item and stops there; otherwise it falls through to `BlockAttachedEntity` and the frame breaks | true |
| `EndCrystal` | `Entity.isInvulnerableToBase`, then **is the source an `EnderDragon`** | removes itself with `Entity.RemovalReason.KILLED` and explodes with power 6 — unless the source was already an explosion — then `EndCrystal.onDestroyedBy` | true |
| `ShulkerBullet` | — | plays `SoundEvents.SHULKER_BULLET_HURT`, spawns fifteen `ParticleTypes.CRIT`, destroys itself | true |
| `EnderDragonPart` | `Entity.isInvulnerableToBase` | forwards the whole call to `EnderDragon.hurt` with itself as the part that was hit | the parent's answer |
| `VehicleEntity` | already removed, then `Entity.isInvulnerableToBase` | flips `VehicleEntity.getHurtDir`, sets ten ticks of hurt time, adds *damage × 10* to `VehicleEntity.getDamage`, and destroys past 40 — a creative player skips to `Entity.discard` | true |
| `MinecartTNT` | a **burning** `AbstractArrow` as the direct entity explodes it, scaled by the arrow's speed | on that path, nothing else: the explosion calls `Entity.discard`, so `VehicleEntity.hurtServer` returns at its already-removed test. Any other source falls through to everything `VehicleEntity` does | true |

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
