# Entity data serializers

> Generated from the **26.2** decompile by `tools/gen_reference.py`. Do not edit by hand.

Every `EntityDataSerializer` in `EntityDataSerializers`, in **registration order, which is the wire id** — `EntityDataSerializers.registerSerializer` pushes each one into a `CrudeIncrementalIntIdentityHashBiMap` that hands out the next int. A `SynchedEntityData.DataValue` on the wire is an unsigned byte accessor id, this var-int, and the encoded value. *For value type* marks the ones built by `EntityDataSerializer.forValueType`, the immutable case where `EntityDataSerializer.copy` is identity. See [Synched entity data](../systems/entities/synched-entity-data.md).

43 serializers, wire ids 0 to 42

| id | constant | value type | built by |
|---:|---|---|---|
| 0 | `EntityDataSerializers.BYTE` | `Byte` | for value type |
| 1 | `EntityDataSerializers.INT` | `Integer` | for value type |
| 2 | `EntityDataSerializers.LONG` | `Long` | for value type |
| 3 | `EntityDataSerializers.FLOAT` | `Float` | for value type |
| 4 | `EntityDataSerializers.STRING` | `String` | for value type |
| 5 | `EntityDataSerializers.COMPONENT` | `Component` | for value type |
| 6 | `EntityDataSerializers.OPTIONAL_COMPONENT` | `Optional<Component>` | for value type |
| 7 | `EntityDataSerializers.ITEM_STACK` | `?` | `EntityDataSerializer.?` |
| 8 | `EntityDataSerializers.BOOLEAN` | `Boolean` | for value type |
| 9 | `EntityDataSerializers.ROTATIONS` | `Rotations` | for value type |
| 10 | `EntityDataSerializers.BLOCK_POS` | `BlockPos` | for value type |
| 11 | `EntityDataSerializers.OPTIONAL_BLOCK_POS` | `Optional<BlockPos>` | for value type |
| 12 | `EntityDataSerializers.DIRECTION` | `Direction` | for value type |
| 13 | `EntityDataSerializers.OPTIONAL_LIVING_ENTITY_REFERENCE` | `Optional<EntityReference<LivingEntity>>` | for value type |
| 14 | `EntityDataSerializers.BLOCK_STATE` | `BlockState` | for value type |
| 15 | `EntityDataSerializers.OPTIONAL_BLOCK_STATE` | `Optional<BlockState>` | for value type |
| 16 | `EntityDataSerializers.PARTICLE` | `ParticleOptions` | for value type |
| 17 | `EntityDataSerializers.PARTICLES` | `List<ParticleOptions>` | for value type |
| 18 | `EntityDataSerializers.VILLAGER_DATA` | `VillagerData` | for value type |
| 19 | `EntityDataSerializers.OPTIONAL_UNSIGNED_INT` | `OptionalInt` | for value type |
| 20 | `EntityDataSerializers.POSE` | `Pose` | for value type |
| 21 | `EntityDataSerializers.CAT_VARIANT` | `Holder<CatVariant>` | for value type |
| 22 | `EntityDataSerializers.CAT_SOUND_VARIANT` | `Holder<CatSoundVariant>` | for value type |
| 23 | `EntityDataSerializers.COW_VARIANT` | `Holder<CowVariant>` | for value type |
| 24 | `EntityDataSerializers.COW_SOUND_VARIANT` | `Holder<CowSoundVariant>` | for value type |
| 25 | `EntityDataSerializers.WOLF_VARIANT` | `Holder<WolfVariant>` | for value type |
| 26 | `EntityDataSerializers.WOLF_SOUND_VARIANT` | `Holder<WolfSoundVariant>` | for value type |
| 27 | `EntityDataSerializers.FROG_VARIANT` | `Holder<FrogVariant>` | for value type |
| 28 | `EntityDataSerializers.PIG_VARIANT` | `Holder<PigVariant>` | for value type |
| 29 | `EntityDataSerializers.PIG_SOUND_VARIANT` | `Holder<PigSoundVariant>` | for value type |
| 30 | `EntityDataSerializers.CHICKEN_VARIANT` | `Holder<ChickenVariant>` | for value type |
| 31 | `EntityDataSerializers.CHICKEN_SOUND_VARIANT` | `Holder<ChickenSoundVariant>` | for value type |
| 32 | `EntityDataSerializers.ZOMBIE_NAUTILUS_VARIANT` | `Holder<ZombieNautilusVariant>` | for value type |
| 33 | `EntityDataSerializers.OPTIONAL_GLOBAL_POS` | `Optional<GlobalPos>` | for value type |
| 34 | `EntityDataSerializers.PAINTING_VARIANT` | `Holder<PaintingVariant>` | for value type |
| 35 | `EntityDataSerializers.SNIFFER_STATE` | `Sniffer.State` | for value type |
| 36 | `EntityDataSerializers.ARMADILLO_STATE` | `Armadillo.ArmadilloState` | for value type |
| 37 | `EntityDataSerializers.COPPER_GOLEM_STATE` | `CopperGolemState` | for value type |
| 38 | `EntityDataSerializers.WEATHERING_COPPER_STATE` | `WeatheringCopper.WeatherState` | for value type |
| 39 | `EntityDataSerializers.VECTOR3` | `Vector3fc` | for value type |
| 40 | `EntityDataSerializers.QUATERNION` | `Quaternionfc` | for value type |
| 41 | `EntityDataSerializers.RESOLVABLE_PROFILE` | `ResolvableProfile` | for value type |
| 42 | `EntityDataSerializers.HUMANOID_ARM` | `HumanoidArm` | for value type |
