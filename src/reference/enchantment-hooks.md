# Enchantment hooks

> Generated from the **26.2** decompile by `tools/gen_reference.py`. Do not edit by hand.

Every public entry point of `EnchantmentHelper`, with the classes that call it. The enchantment package barely calls anything and everything calls it, so this table is the system's real interface: each row is a moment at which some other system asks whether an enchantment wants to change what happens. Callers are the declaring files, one per class, excluding `EnchantmentHelper` itself. See [Enchantments](../systems/items/enchantments.md) for what an enchantment is and [Enchanting](../systems/items/enchanting.md) for the selection half.

50 entry points, 47 of them called from outside the class

| entry point | overloads | called from |
|---|---:|---|
| `EnchantmentHelper.canStoreEnchantments` | 1 | `AnvilMenu` |
| `EnchantmentHelper.createBook` | 1 | `CreativeModeTabs` |
| `EnchantmentHelper.doPostAttackEffects` | 1 | `AbstractCubeMob`, `AbstractWindCharge`, `Bee`, `ChargeAttack`, `EnderDragon`, `EvokerFangs`, `HoglinBase`, `IronGolem`, `LargeFireball`, `LivingEntity`, `LlamaSpit`, `Mob`, `Player`, `RamTarget`, `ShulkerBullet`, `SmallFireball`, `WitherSkull` |
| `EnchantmentHelper.doPostAttackEffectsWithItemSource` | 1 | `AbstractArrow`, `Player` |
| `EnchantmentHelper.doPostAttackEffectsWithItemSourceOnBreak` | 1 | `ThrownTrident` |
| `EnchantmentHelper.doPostPiercingAttackEffects` | 1 | `LivingEntity` |
| `EnchantmentHelper.enchantItem` | 2 | `EnchantWithLevelsFunction` |
| `EnchantmentHelper.enchantItemFromProvider` | 1 | `EnderMan`, `Mob`, `Pillager`, `SkeletonTrapGoal`, `Vindicator` |
| `EnchantmentHelper.filterCompatibleEnchantments` | 1 | *nothing outside the class* |
| `EnchantmentHelper.forEachModifier` | 2 | `ItemStack` |
| `EnchantmentHelper.getAvailableEnchantmentResults` | 1 | *nothing outside the class* |
| `EnchantmentHelper.getDamageProtection` | 1 | `LivingEntity` |
| `EnchantmentHelper.getEnchantmentCost` | 1 | `EnchantmentMenu` |
| `EnchantmentHelper.getEnchantmentLevel` | 1 | `EnchantedCountIncreaseFunction`, `LootItemRandomChanceWithEnchantedBonusCondition` |
| `EnchantmentHelper.getEnchantmentsForCrafting` | 1 | `AnvilMenu`, `EnchantCommand`, `GrindstoneMenu`, `RepairItemRecipe` |
| `EnchantmentHelper.getFishingLuckBonus` | 1 | `FishingRodItem` |
| `EnchantmentHelper.getFishingTimeReduction` | 1 | `FishingRodItem` |
| `EnchantmentHelper.getHighestLevel` | 1 | *nothing outside the class* |
| `EnchantmentHelper.getItemEnchantmentLevel` | 1 | `ApplyBonusCount`, `BonusLevelTableCondition` |
| `EnchantmentHelper.getPiercingCount` | 1 | `AbstractArrow` |
| `EnchantmentHelper.getRandomItemWith` | 1 | `ExperienceOrb` |
| `EnchantmentHelper.getTridentReturnToOwnerAcceleration` | 1 | `ThrownTrident` |
| `EnchantmentHelper.getTridentSpinAttackStrength` | 1 | `TridentItem` |
| `EnchantmentHelper.has` | 1 | `AbstractHorse`, `Allay`, `ArmorSlot`, `ArmorStand`, `Equippable`, `Mob`, `Piglin`, `Player`, `ZombieVillager` |
| `EnchantmentHelper.hasAnyEnchantments` | 1 | `GrindstoneMenu` |
| `EnchantmentHelper.hasTag` | 1 | `BeehiveBlock`, `DecoratedPotBlock`, `IceBlock`, `InfestedBlock` |
| `EnchantmentHelper.isEnchantmentCompatible` | 1 | `EnchantCommand` |
| `EnchantmentHelper.isImmuneToDamage` | 1 | `LivingEntity` |
| `EnchantmentHelper.modifyArmorEffectiveness` | 1 | `CombatRules` |
| `EnchantmentHelper.modifyCrossbowChargingTime` | 1 | `CrossbowItem` |
| `EnchantmentHelper.modifyDamage` | 1 | `AbstractArrow`, `LivingEntity`, `Mob`, `ServerPlayer`, `ThrownTrident` |
| `EnchantmentHelper.modifyDurabilityToRepairFromXp` | 1 | `ExperienceOrb` |
| `EnchantmentHelper.modifyFallBasedDamage` | 1 | `MaceItem` |
| `EnchantmentHelper.modifyKnockback` | 1 | `AbstractArrow`, `LivingEntity` |
| `EnchantmentHelper.onHitBlock` | 1 | `AbstractArrow`, `ServerPlayerGameMode`, `ThrownTrident` |
| `EnchantmentHelper.onProjectileSpawned` | 1 | `Projectile` |
| `EnchantmentHelper.pickHighestLevel` | 1 | `CrossbowItem`, `TridentItem` |
| `EnchantmentHelper.processAmmoUse` | 1 | `ProjectileWeaponItem` |
| `EnchantmentHelper.processBlockExperience` | 1 | `Block` |
| `EnchantmentHelper.processDurabilityChange` | 1 | `ItemStack` |
| `EnchantmentHelper.processEquipmentDropChance` | 1 | `Mob` |
| `EnchantmentHelper.processMobExperience` | 1 | `LivingEntity` |
| `EnchantmentHelper.processProjectileCount` | 1 | `ProjectileWeaponItem` |
| `EnchantmentHelper.processProjectileSpread` | 1 | `ProjectileWeaponItem` |
| `EnchantmentHelper.runLocationChangedEffects` | 2 | `LivingEntity`, `ServerPlayer` |
| `EnchantmentHelper.selectEnchantment` | 1 | `EnchantmentMenu`, `EnchantmentsByCost`, `EnchantmentsByCostWithDifficulty` |
| `EnchantmentHelper.setEnchantments` | 1 | `AnvilMenu` |
| `EnchantmentHelper.stopLocationBasedEffects` | 2 | `LivingEntity`, `ServerPlayer` |
| `EnchantmentHelper.tickEffects` | 1 | `LivingEntity` |
| `EnchantmentHelper.updateEnchantments` | 1 | `GrindstoneMenu`, `ItemStack`, `RepairItemRecipe`, `SetEnchantmentsFunction` |
