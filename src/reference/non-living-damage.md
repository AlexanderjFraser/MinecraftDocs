# Damage outside `LivingEntity`

> Verified against **Minecraft 26.2** · Reference · Hand-kept from
> `net/minecraft/world/entity/**`.

`Entity.hurtServer` is **abstract**. There is no default behaviour for being
hurt anywhere in the tree, so every branch has to answer for itself, and the
twenty-one classes below answer with rules that share nothing with
`LivingEntity`'s — no armour, no invulnerability window, no `CombatTracker`,
no death sequence. The lecture that frames them is [damage and
death](../systems/entities/damage-and-death.md); this is the per-class table.

Two things happen before any of them. `Player.attack` asks
`Entity.isAttackable` and then `Entity.skipAttackInteraction`, either of
which consumes the click without `Entity.hurtServer` ever being called —
`Interaction` uses that hook to record who hit it, `ArmorStand` and
`BlockAttachedEntity` to run their own rules. And a *false* return is not
"the hit missed": it is "nothing was damaged", which is what stops a
creative-mode swing from being counted.

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
| `AbstractHurtingProjectile` | — | nothing: fireballs, wind charges and the rest are unhittable | false |
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
| `MinecartTNT` | a **burning** `AbstractArrow` as the direct entity explodes it, scaled by the arrow's speed | then everything `VehicleEntity` does | true |

Five patterns account for all of it: *nothing happens* (ten classes), *a
flinch and nothing else* (two), *an int of health with no armour and no
window* (two), *one hit destroys* (five), and *an accumulator* (two). The
only class that reads the damage **amount** at all beyond the accumulator is
the pair with an int of health; everything else is a yes-or-no.

---

*Rules: names, never code · how the system works, not how the code reads ·
newest version only · every backticked name passes `tools/verify_names.py`.*
