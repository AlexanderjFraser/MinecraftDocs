# Entity spawn reasons

> Generated from the **26.3** decompile by `tools/gen_reference.py`. Do not edit by hand.

Every `EntitySpawnReason` constant, in declaration order, with **what each one gates** — the classes that compare against it and so behave differently for that reason — and how many other classes pass it. A reason with an empty *gates* column changes nothing by itself: it is a label the spawn path carries for other code to read. `EntitySpawnReason.isSpawner` folds `SPAWNER` and `TRIAL_SPAWNER` together and `EntitySpawnReason.ignoresLightRequirements` is true of `TRIAL_SPAWNER` alone. See [entity lifecycle](../systems/entities/entity-lifecycle.md#the-other-ways-in).

19 reasons · 13 of them tested somewhere · 41 test sites

| # | reason | what it gates | classes that pass it |
|---:|---|---|---:|
| 0 | `EntitySpawnReason.NATURAL` | `ZombieHorse.finalizeSpawn`; `Drowned.finalizeSpawn`; `Husk.finalizeSpawn`; `Raider.finalizeSpawn` | 4 |
| 1 | `EntitySpawnReason.CHUNK_GENERATION` | *nothing tests it* | 2 |
| 2 | `EntitySpawnReason.SPAWNER` | `Mob.checkMobSpawnRules` (through `EntitySpawnReason.isSpawner`); `SkeletonHorse.checkSkeletonHorseSpawnRules` (through `EntitySpawnReason.isSpawner`); `Endermite.checkEndermiteSpawnRules` (through `EntitySpawnReason.isSpawner`); `Guardian.checkGuardianSpawnRules` (through `EntitySpawnReason.isSpawner`); `Monster.checkSurfaceMonstersSpawnRules` (through `EntitySpawnReason.isSpawner`); `Silverfish.checkSilverfishSpawnRules` (through `EntitySpawnReason.isSpawner`); `Slime.checkSlimeSpawnRules` (through `EntitySpawnReason.isSpawner`); `Stray.checkStraySpawnRules` (through `EntitySpawnReason.isSpawner`); `Drowned.checkDrownedSpawnRules` (through `EntitySpawnReason.isSpawner`) | 3 |
| 3 | `EntitySpawnReason.STRUCTURE` | `PatrollingMonster.finalizeSpawn`; `Piglin.finalizeSpawn`; `Drowned.finalizeSpawn` | 9 |
| 4 | `EntitySpawnReason.BREEDING` | `Villager.finalizeSpawn` | 41 |
| 5 | `EntitySpawnReason.MOB_SUMMONED` | *nothing tests it* | 2 |
| 6 | `EntitySpawnReason.JOCKEY` | *nothing tests it* | 5 |
| 7 | `EntitySpawnReason.EVENT` | `TraderLlama.finalizeSpawn`; `PatrollingMonster.finalizeSpawn` | 5 |
| 8 | `EntitySpawnReason.CONVERSION` | `Husk.finalizeSpawn`; `Zombie.finalizeSpawn`; `Zombie.handleAttributes` | 5 |
| 9 | `EntitySpawnReason.REINFORCEMENT` | `Drowned.checkDrownedSpawnRules` | 1 |
| 10 | `EntitySpawnReason.TRIGGERED` | `Warden.finalizeSpawn` | 12 |
| 11 | `EntitySpawnReason.BUCKET` | `Axolotl.finalizeSpawn` | 1 |
| 12 | `EntitySpawnReason.SPAWN_ITEM_USE` | *nothing tests it* | 4 |
| 13 | `EntitySpawnReason.COMMAND` | *nothing tests it* | 2 |
| 14 | `EntitySpawnReason.DISPENSER` | *nothing tests it* | 5 |
| 15 | `EntitySpawnReason.PATROL` | `PatrollingMonster.finalizeSpawn` | 1 |
| 16 | `EntitySpawnReason.TRIAL_SPAWNER` | `Mob.checkMobSpawnRules` (through `EntitySpawnReason.isSpawner`); `Animal.checkAnimalSpawnRules` (through `EntitySpawnReason.ignoresLightRequirements`); `SkeletonHorse.checkSkeletonHorseSpawnRules` (through `EntitySpawnReason.isSpawner`); `SkeletonHorse.checkSkeletonHorseSpawnRules` (through `EntitySpawnReason.ignoresLightRequirements`); `Endermite.checkEndermiteSpawnRules` (through `EntitySpawnReason.isSpawner`); `Guardian.checkGuardianSpawnRules` (through `EntitySpawnReason.isSpawner`); `Monster.checkMonsterSpawnRules` (through `EntitySpawnReason.ignoresLightRequirements`); `Monster.checkSurfaceMonstersSpawnRules` (through `EntitySpawnReason.isSpawner`); `Silverfish.checkSilverfishSpawnRules` (through `EntitySpawnReason.isSpawner`); `Slime.checkSlimeSpawnRules` (through `EntitySpawnReason.isSpawner`); `Stray.checkStraySpawnRules` (through `EntitySpawnReason.isSpawner`); `Drowned.checkDrownedSpawnRules` (through `EntitySpawnReason.isSpawner`); `Drowned.checkDrownedSpawnRules` (through `EntitySpawnReason.ignoresLightRequirements`) | 3 |
| 17 | `EntitySpawnReason.LOAD` | `Zombie.handleAttributes` | 6 |
| 18 | `EntitySpawnReason.DIMENSION_TRAVEL` | `Zombie.handleAttributes` | 1 |
