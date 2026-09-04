# Registries

> Generated from the **26.2** decompile by `tools/gen_reference.py`. Do not edit by hand.

Every registry key declared in `Registries`. **Built-in** registries are populated from static code in `BuiltInRegistries` at class-load time and frozen; **data-pack** registries are loaded per world by `RegistryDataLoader` from JSON (`WORLDGEN_REGISTRIES`, or `DIMENSION_REGISTRIES` for level stems); **synced** ones are sent to the client in the configuration phase (`SYNCHRONIZED_REGISTRIES`). A key that is none of these is a registry *type* the game reasons about without a global instance (e.g. per-world or client-side). See [Identifiers and registries](../systems/foundations/identifiers-and-registries.md).

148 keys · 95 built-in · 47 data-pack · 29 synced

| key | element type | kind | synced |
|---|---|---|---|
| `activity` (`Registries.ACTIVITY`) | `Activity` | built-in |  |
| `advancement` (`Registries.ADVANCEMENT`) | `Advancement` | — |  |
| `attribute` (`Registries.ATTRIBUTE`) | `Attribute` | built-in |  |
| `attribute_type` (`Registries.ATTRIBUTE_TYPE`) | `AttributeType<…>` | built-in |  |
| `banner_pattern` (`Registries.BANNER_PATTERN`) | `BannerPattern` | data-pack | yes |
| `block` (`Registries.BLOCK`) | `Block` | built-in |  |
| `block_entity_type` (`Registries.BLOCK_ENTITY_TYPE`) | `BlockEntityType<…>` | built-in |  |
| `block_predicate_type` (`Registries.BLOCK_PREDICATE_TYPE`) | `BlockPredicateType<…>` | built-in |  |
| `block_type` (`Registries.BLOCK_TYPE`) | `MapCodec<…>` | built-in |  |
| `cat_sound_variant` (`Registries.CAT_SOUND_VARIANT`) | `CatSoundVariant` | data-pack | yes |
| `cat_variant` (`Registries.CAT_VARIANT`) | `CatVariant` | data-pack | yes |
| `chat_type` (`Registries.CHAT_TYPE`) | `ChatType` | data-pack | yes |
| `chicken_sound_variant` (`Registries.CHICKEN_SOUND_VARIANT`) | `ChickenSoundVariant` | data-pack | yes |
| `chicken_variant` (`Registries.CHICKEN_VARIANT`) | `ChickenVariant` | data-pack | yes |
| `chunk_status` (`Registries.CHUNK_STATUS`) | `ChunkStatus` | built-in |  |
| `command_argument_type` (`Registries.COMMAND_ARGUMENT_TYPE`) | `ArgumentTypeInfo<…>` | built-in |  |
| `consume_effect_type` (`Registries.CONSUME_EFFECT_TYPE`) | `ConsumeEffect.Type<…>` | built-in |  |
| `cow_sound_variant` (`Registries.COW_SOUND_VARIANT`) | `CowSoundVariant` | data-pack | yes |
| `cow_variant` (`Registries.COW_VARIANT`) | `CowVariant` | data-pack | yes |
| `creative_mode_tab` (`Registries.CREATIVE_MODE_TAB`) | `CreativeModeTab` | built-in |  |
| `custom_stat` (`Registries.CUSTOM_STAT`) | `Identifier` | built-in |  |
| `damage_type` (`Registries.DAMAGE_TYPE`) | `DamageType` | data-pack | yes |
| `data_component_predicate_type` (`Registries.DATA_COMPONENT_PREDICATE_TYPE`) | `DataComponentPredicate.Type<…>` | built-in |  |
| `data_component_type` (`Registries.DATA_COMPONENT_TYPE`) | `DataComponentType<…>` | built-in |  |
| `debug_subscription` (`Registries.DEBUG_SUBSCRIPTION`) | `DebugSubscription<…>` | built-in |  |
| `decorated_pot_pattern` (`Registries.DECORATED_POT_PATTERN`) | `DecoratedPotPattern` | built-in |  |
| `dialog` (`Registries.DIALOG`) | `Dialog` | data-pack | yes |
| `dialog_action_type` (`Registries.DIALOG_ACTION_TYPE`) | `MapCodec<…>` | built-in |  |
| `dialog_body_type` (`Registries.DIALOG_BODY_TYPE`) | `MapCodec<…>` | built-in |  |
| `dialog_type` (`Registries.DIALOG_TYPE`) | `MapCodec<…>` | built-in |  |
| `dimension` (`Registries.DIMENSION`) | `Level` | — |  |
| `dimension` (`Registries.LEVEL_STEM`) | `LevelStem` | data-pack (dimension) |  |
| `dimension_type` (`Registries.DIMENSION_TYPE`) | `DimensionType` | data-pack | yes |
| `enchantment` (`Registries.ENCHANTMENT`) | `Enchantment` | data-pack | yes |
| `enchantment_effect_component_type` (`Registries.ENCHANTMENT_EFFECT_COMPONENT_TYPE`) | `DataComponentType<…>` | built-in |  |
| `enchantment_entity_effect_type` (`Registries.ENCHANTMENT_ENTITY_EFFECT_TYPE`) | `MapCodec<…>` | built-in |  |
| `enchantment_level_based_value_type` (`Registries.ENCHANTMENT_LEVEL_BASED_VALUE_TYPE`) | `MapCodec<…>` | built-in |  |
| `enchantment_location_based_effect_type` (`Registries.ENCHANTMENT_LOCATION_BASED_EFFECT_TYPE`) | `MapCodec<…>` | built-in |  |
| `enchantment_provider` (`Registries.ENCHANTMENT_PROVIDER`) | `EnchantmentProvider` | data-pack |  |
| `enchantment_provider_type` (`Registries.ENCHANTMENT_PROVIDER_TYPE`) | `MapCodec<…>` | built-in |  |
| `enchantment_value_effect_type` (`Registries.ENCHANTMENT_VALUE_EFFECT_TYPE`) | `MapCodec<…>` | built-in |  |
| `entity_sub_predicate_type` (`Registries.ENTITY_SUB_PREDICATE_TYPE`) | `Codec<…>` | built-in |  |
| `entity_type` (`Registries.ENTITY_TYPE`) | `EntityType<…>` | built-in |  |
| `environment_attribute` (`Registries.ENVIRONMENT_ATTRIBUTE`) | `EnvironmentAttribute<…>` | built-in |  |
| `float_provider_type` (`Registries.FLOAT_PROVIDER_TYPE`) | `MapCodec<…>` | built-in |  |
| `fluid` (`Registries.FLUID`) | `Fluid` | built-in |  |
| `frog_variant` (`Registries.FROG_VARIANT`) | `FrogVariant` | data-pack | yes |
| `game_event` (`Registries.GAME_EVENT`) | `GameEvent` | built-in |  |
| `game_rule` (`Registries.GAME_RULE`) | `GameRule<…>` | built-in |  |
| `height_provider_type` (`Registries.HEIGHT_PROVIDER_TYPE`) | `HeightProviderType<…>` | built-in |  |
| `incoming_rpc_methods` (`Registries.INCOMING_RPC_METHOD`) | `IncomingRpcMethod<…>` | built-in |  |
| `input_control_type` (`Registries.INPUT_CONTROL_TYPE`) | `MapCodec<…>` | built-in |  |
| `instrument` (`Registries.INSTRUMENT`) | `Instrument` | data-pack | yes |
| `int_provider_type` (`Registries.INT_PROVIDER_TYPE`) | `MapCodec<…>` | built-in |  |
| `item` (`Registries.ITEM`) | `Item` | built-in |  |
| `item_modifier` (`Registries.ITEM_MODIFIER`) | `LootItemFunction` | — |  |
| `jukebox_song` (`Registries.JUKEBOX_SONG`) | `JukeboxSong` | data-pack | yes |
| `loot_condition_type` (`Registries.LOOT_CONDITION_TYPE`) | `MapCodec<…>` | built-in |  |
| `loot_function_type` (`Registries.LOOT_FUNCTION_TYPE`) | `MapCodec<…>` | built-in |  |
| `loot_nbt_provider_type` (`Registries.LOOT_NBT_PROVIDER_TYPE`) | `MapCodec<…>` | built-in |  |
| `loot_number_provider_type` (`Registries.LOOT_NUMBER_PROVIDER_TYPE`) | `MapCodec<…>` | built-in |  |
| `loot_pool_entry_type` (`Registries.LOOT_POOL_ENTRY_TYPE`) | `MapCodec<…>` | built-in |  |
| `loot_score_provider_type` (`Registries.LOOT_SCORE_PROVIDER_TYPE`) | `MapCodec<…>` | built-in |  |
| `loot_table` (`Registries.LOOT_TABLE`) | `LootTable` | — |  |
| `map_decoration_type` (`Registries.MAP_DECORATION_TYPE`) | `MapDecorationType` | built-in |  |
| `memory_module_type` (`Registries.MEMORY_MODULE_TYPE`) | `MemoryModuleType<…>` | built-in |  |
| `menu` (`Registries.MENU`) | `MenuType<…>` | built-in |  |
| `mob_effect` (`Registries.MOB_EFFECT`) | `MobEffect` | built-in |  |
| `number_format_type` (`Registries.NUMBER_FORMAT_TYPE`) | `NumberFormatType<…>` | built-in |  |
| `outgoing_rpc_methods` (`Registries.OUTGOING_RPC_METHOD`) | `OutgoingRpcMethod<…>` | built-in |  |
| `painting_variant` (`Registries.PAINTING_VARIANT`) | `PaintingVariant` | data-pack | yes |
| `particle_type` (`Registries.PARTICLE_TYPE`) | `ParticleType<…>` | built-in |  |
| `permission_check_type` (`Registries.PERMISSION_CHECK_TYPE`) | `MapCodec<…>` | built-in |  |
| `permission_type` (`Registries.PERMISSION_TYPE`) | `MapCodec<…>` | built-in |  |
| `pig_sound_variant` (`Registries.PIG_SOUND_VARIANT`) | `PigSoundVariant` | data-pack | yes |
| `pig_variant` (`Registries.PIG_VARIANT`) | `PigVariant` | data-pack | yes |
| `point_of_interest_type` (`Registries.POINT_OF_INTEREST_TYPE`) | `PoiType` | built-in |  |
| `pos_rule_test` (`Registries.POS_RULE_TEST`) | `PosRuleTestType<…>` | built-in |  |
| `position_source_type` (`Registries.POSITION_SOURCE_TYPE`) | `PositionSourceType<…>` | built-in |  |
| `potion` (`Registries.POTION`) | `Potion` | built-in |  |
| `predicate` (`Registries.PREDICATE`) | `LootItemCondition` | — |  |
| `recipe` (`Registries.RECIPE`) | `Recipe<…>` | — |  |
| `recipe_book_category` (`Registries.RECIPE_BOOK_CATEGORY`) | `RecipeBookCategory` | built-in |  |
| `recipe_display` (`Registries.RECIPE_DISPLAY`) | `RecipeDisplay.Type<…>` | built-in |  |
| `recipe_serializer` (`Registries.RECIPE_SERIALIZER`) | `RecipeSerializer<…>` | built-in |  |
| `recipe_type` (`Registries.RECIPE_TYPE`) | `RecipeType<…>` | built-in |  |
| `rule_block_entity_modifier` (`Registries.RULE_BLOCK_ENTITY_MODIFIER`) | `RuleBlockEntityModifierType<…>` | built-in |  |
| `rule_test` (`Registries.RULE_TEST`) | `RuleTestType<…>` | built-in |  |
| `sensor_type` (`Registries.SENSOR_TYPE`) | `SensorType<…>` | built-in |  |
| `slot_display` (`Registries.SLOT_DISPLAY`) | `SlotDisplay.Type<…>` | built-in |  |
| `slot_source_type` (`Registries.SLOT_SOURCE_TYPE`) | `MapCodec<…>` | built-in |  |
| `sound_event` (`Registries.SOUND_EVENT`) | `SoundEvent` | built-in |  |
| `spawn_condition_type` (`Registries.SPAWN_CONDITION_TYPE`) | `MapCodec<…>` | built-in |  |
| `stat_type` (`Registries.STAT_TYPE`) | `StatType<…>` | built-in |  |
| `sulfur_cube_archetype` (`Registries.SULFUR_CUBE_ARCHETYPE`) | `SulfurCubeArchetype` | data-pack | yes |
| `test_environment` (`Registries.TEST_ENVIRONMENT`) | `TestEnvironmentDefinition<…>` | data-pack | yes |
| `test_environment_definition_type` (`Registries.TEST_ENVIRONMENT_DEFINITION_TYPE`) | `MapCodec<…>` | built-in |  |
| `test_function` (`Registries.TEST_FUNCTION`) | `Consumer<…>` | built-in |  |
| `test_instance` (`Registries.TEST_INSTANCE`) | `GameTestInstance` | data-pack | yes |
| `test_instance_type` (`Registries.TEST_INSTANCE_TYPE`) | `MapCodec<…>` | built-in |  |
| `ticket_type` (`Registries.TICKET_TYPE`) | `TicketType` | built-in |  |
| `timeline` (`Registries.TIMELINE`) | `Timeline` | data-pack | yes |
| `trade_set` (`Registries.TRADE_SET`) | `TradeSet` | data-pack |  |
| `trial_spawner` (`Registries.TRIAL_SPAWNER_CONFIG`) | `TrialSpawnerConfig` | data-pack |  |
| `trigger_type` (`Registries.TRIGGER_TYPE`) | `CriterionTrigger<…>` | built-in |  |
| `trim_material` (`Registries.TRIM_MATERIAL`) | `TrimMaterial` | data-pack | yes |
| `trim_pattern` (`Registries.TRIM_PATTERN`) | `TrimPattern` | data-pack | yes |
| `villager_profession` (`Registries.VILLAGER_PROFESSION`) | `VillagerProfession` | built-in |  |
| `villager_trade` (`Registries.VILLAGER_TRADE`) | `VillagerTrade` | data-pack |  |
| `villager_type` (`Registries.VILLAGER_TYPE`) | `VillagerType` | built-in |  |
| `wolf_sound_variant` (`Registries.WOLF_SOUND_VARIANT`) | `WolfSoundVariant` | data-pack | yes |
| `wolf_variant` (`Registries.WOLF_VARIANT`) | `WolfVariant` | data-pack | yes |
| `world_clock` (`Registries.WORLD_CLOCK`) | `WorldClock` | data-pack | yes |
| `worldgen/biome` (`Registries.BIOME`) | `Biome` | data-pack | yes |
| `worldgen/biome_source` (`Registries.BIOME_SOURCE`) | `MapCodec<…>` | built-in |  |
| `worldgen/block_state_provider_type` (`Registries.BLOCK_STATE_PROVIDER_TYPE`) | `BlockStateProviderType<…>` | built-in |  |
| `worldgen/carver` (`Registries.CARVER`) | `WorldCarver<…>` | built-in |  |
| `worldgen/chunk_generator` (`Registries.CHUNK_GENERATOR`) | `MapCodec<…>` | built-in |  |
| `worldgen/configured_carver` (`Registries.CONFIGURED_CARVER`) | `ConfiguredWorldCarver<…>` | data-pack |  |
| `worldgen/configured_feature` (`Registries.CONFIGURED_FEATURE`) | `ConfiguredFeature<…>` | data-pack |  |
| `worldgen/density_function` (`Registries.DENSITY_FUNCTION`) | `DensityFunction` | data-pack |  |
| `worldgen/density_function_type` (`Registries.DENSITY_FUNCTION_TYPE`) | `MapCodec<…>` | built-in |  |
| `worldgen/feature` (`Registries.FEATURE`) | `Feature<…>` | built-in |  |
| `worldgen/feature_size_type` (`Registries.FEATURE_SIZE_TYPE`) | `FeatureSizeType<…>` | built-in |  |
| `worldgen/flat_level_generator_preset` (`Registries.FLAT_LEVEL_GENERATOR_PRESET`) | `FlatLevelGeneratorPreset` | data-pack |  |
| `worldgen/foliage_placer_type` (`Registries.FOLIAGE_PLACER_TYPE`) | `FoliagePlacerType<…>` | built-in |  |
| `worldgen/material_condition` (`Registries.MATERIAL_CONDITION`) | `MapCodec<…>` | built-in |  |
| `worldgen/material_rule` (`Registries.MATERIAL_RULE`) | `MapCodec<…>` | built-in |  |
| `worldgen/multi_noise_biome_source_parameter_list` (`Registries.MULTI_NOISE_BIOME_SOURCE_PARAMETER_LIST`) | `MultiNoiseBiomeSourceParameterList` | data-pack |  |
| `worldgen/noise` (`Registries.NOISE`) | `NormalNoise.NoiseParameters` | data-pack |  |
| `worldgen/noise_settings` (`Registries.NOISE_SETTINGS`) | `NoiseGeneratorSettings` | data-pack |  |
| `worldgen/placed_feature` (`Registries.PLACED_FEATURE`) | `PlacedFeature` | data-pack |  |
| `worldgen/placement_modifier_type` (`Registries.PLACEMENT_MODIFIER_TYPE`) | `PlacementModifierType<…>` | built-in |  |
| `worldgen/pool_alias_binding` (`Registries.POOL_ALIAS_BINDING`) | `MapCodec<…>` | built-in |  |
| `worldgen/processor_list` (`Registries.PROCESSOR_LIST`) | `StructureProcessorList` | data-pack |  |
| `worldgen/root_placer_type` (`Registries.ROOT_PLACER_TYPE`) | `RootPlacerType<…>` | built-in |  |
| `worldgen/structure` (`Registries.STRUCTURE`) | `Structure` | data-pack |  |
| `worldgen/structure_piece` (`Registries.STRUCTURE_PIECE`) | `StructurePieceType` | built-in |  |
| `worldgen/structure_placement` (`Registries.STRUCTURE_PLACEMENT`) | `StructurePlacementType<…>` | built-in |  |
| `worldgen/structure_pool_element` (`Registries.STRUCTURE_POOL_ELEMENT`) | `StructurePoolElementType<…>` | built-in |  |
| `worldgen/structure_processor` (`Registries.STRUCTURE_PROCESSOR`) | `MapCodec<…>` | built-in |  |
| `worldgen/structure_set` (`Registries.STRUCTURE_SET`) | `StructureSet` | data-pack |  |
| `worldgen/structure_type` (`Registries.STRUCTURE_TYPE`) | `StructureType<…>` | built-in |  |
| `worldgen/template_pool` (`Registries.TEMPLATE_POOL`) | `StructureTemplatePool` | data-pack |  |
| `worldgen/tree_decorator_type` (`Registries.TREE_DECORATOR_TYPE`) | `TreeDecoratorType<…>` | built-in |  |
| `worldgen/trunk_placer_type` (`Registries.TRUNK_PLACER_TYPE`) | `TrunkPlacerType<…>` | built-in |  |
| `worldgen/world_preset` (`Registries.WORLD_PRESET`) | `WorldPreset` | data-pack |  |
| `zombie_nautilus_variant` (`Registries.ZOMBIE_NAUTILUS_VARIANT`) | `ZombieNautilusVariant` | data-pack | yes |
