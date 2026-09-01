# Data components

> Generated from the **26.2** decompile by `tools/gen_reference.py`. Do not edit by hand.

Every `DataComponentType` registered in `DataComponents`. *Persistent* components have a `Codec` and are written to disk; *synced* ones have a `StreamCodec` and are sent to the client; *cache-encoded* ones use the shared `EncoderCache`. A type that is neither persistent nor synced is transient and lives only in memory. See [Data components](../systems/foundations/data-components.md).

111 components

| id | value type | persistent | synced |
|---|---|---|---|
| `custom_data` (`DataComponents.CUSTOM_DATA`) | `CustomData` | yes |  |
| `max_stack_size` (`DataComponents.MAX_STACK_SIZE`) | `Integer` | yes | yes |
| `max_damage` (`DataComponents.MAX_DAMAGE`) | `Integer` | yes | yes |
| `damage` (`DataComponents.DAMAGE`) | `Integer` | yes | yes |
| `unbreakable` (`DataComponents.UNBREAKABLE`) | `Unit` | yes | yes |
| `use_effects` (`DataComponents.USE_EFFECTS`) | `UseEffects` | yes | yes |
| `custom_name` (`DataComponents.CUSTOM_NAME`) | `Component` | yes (cached) | yes |
| `minimum_attack_charge` (`DataComponents.MINIMUM_ATTACK_CHARGE`) | `Float` | yes | yes |
| `damage_type` (`DataComponents.DAMAGE_TYPE`) | `Holder<…>` | yes | yes |
| `item_name` (`DataComponents.ITEM_NAME`) | `Component` | yes (cached) | yes |
| `item_model` (`DataComponents.ITEM_MODEL`) | `Identifier` | yes (cached) | yes |
| `lore` (`DataComponents.LORE`) | `ItemLore` | yes (cached) | yes |
| `rarity` (`DataComponents.RARITY`) | `Rarity` | yes | yes |
| `enchantments` (`DataComponents.ENCHANTMENTS`) | `ItemEnchantments` | yes (cached) | yes |
| `can_place_on` (`DataComponents.CAN_PLACE_ON`) | `AdventureModePredicate` | yes (cached) | yes |
| `can_break` (`DataComponents.CAN_BREAK`) | `AdventureModePredicate` | yes (cached) | yes |
| `attribute_modifiers` (`DataComponents.ATTRIBUTE_MODIFIERS`) | `ItemAttributeModifiers` | yes (cached) | yes |
| `custom_model_data` (`DataComponents.CUSTOM_MODEL_DATA`) | `CustomModelData` | yes | yes |
| `tooltip_display` (`DataComponents.TOOLTIP_DISPLAY`) | `TooltipDisplay` | yes (cached) | yes |
| `repair_cost` (`DataComponents.REPAIR_COST`) | `Integer` | yes | yes |
| `creative_slot_lock` (`DataComponents.CREATIVE_SLOT_LOCK`) | `Unit` |  | yes |
| `enchantment_glint_override` (`DataComponents.ENCHANTMENT_GLINT_OVERRIDE`) | `Boolean` | yes | yes |
| `intangible_projectile` (`DataComponents.INTANGIBLE_PROJECTILE`) | `Unit` | yes |  |
| `food` (`DataComponents.FOOD`) | `FoodProperties` | yes (cached) | yes |
| `consumable` (`DataComponents.CONSUMABLE`) | `Consumable` | yes (cached) | yes |
| `use_remainder` (`DataComponents.USE_REMAINDER`) | `UseRemainder` | yes (cached) | yes |
| `use_cooldown` (`DataComponents.USE_COOLDOWN`) | `UseCooldown` | yes (cached) | yes |
| `damage_resistant` (`DataComponents.DAMAGE_RESISTANT`) | `DamageResistant` | yes (cached) | yes |
| `tool` (`DataComponents.TOOL`) | `Tool` | yes (cached) | yes |
| `weapon` (`DataComponents.WEAPON`) | `Weapon` | yes (cached) | yes |
| `attack_range` (`DataComponents.ATTACK_RANGE`) | `AttackRange` | yes (cached) | yes |
| `enchantable` (`DataComponents.ENCHANTABLE`) | `Enchantable` | yes (cached) | yes |
| `equippable` (`DataComponents.EQUIPPABLE`) | `Equippable` | yes (cached) | yes |
| `repairable` (`DataComponents.REPAIRABLE`) | `Repairable` | yes (cached) | yes |
| `glider` (`DataComponents.GLIDER`) | `Unit` | yes | yes |
| `tooltip_style` (`DataComponents.TOOLTIP_STYLE`) | `Identifier` | yes (cached) | yes |
| `death_protection` (`DataComponents.DEATH_PROTECTION`) | `DeathProtection` | yes (cached) | yes |
| `blocks_attacks` (`DataComponents.BLOCKS_ATTACKS`) | `BlocksAttacks` | yes (cached) | yes |
| `piercing_weapon` (`DataComponents.PIERCING_WEAPON`) | `PiercingWeapon` | yes (cached) | yes |
| `kinetic_weapon` (`DataComponents.KINETIC_WEAPON`) | `KineticWeapon` | yes (cached) | yes |
| `swing_animation` (`DataComponents.SWING_ANIMATION`) | `SwingAnimation` | yes | yes |
| `additional_trade_cost` (`DataComponents.ADDITIONAL_TRADE_COST`) | `Integer` |  | yes |
| `stored_enchantments` (`DataComponents.STORED_ENCHANTMENTS`) | `ItemEnchantments` | yes (cached) | yes |
| `dye` (`DataComponents.DYE`) | `DyeColor` | yes | yes |
| `dyed_color` (`DataComponents.DYED_COLOR`) | `DyedItemColor` | yes | yes |
| `map_color` (`DataComponents.MAP_COLOR`) | `MapItemColor` | yes | yes |
| `map_id` (`DataComponents.MAP_ID`) | `MapId` | yes | yes |
| `map_decorations` (`DataComponents.MAP_DECORATIONS`) | `MapDecorations` | yes (cached) |  |
| `map_post_processing` (`DataComponents.MAP_POST_PROCESSING`) | `MapPostProcessing` |  | yes |
| `charged_projectiles` (`DataComponents.CHARGED_PROJECTILES`) | `ChargedProjectiles` | yes (cached) | yes |
| `bundle_contents` (`DataComponents.BUNDLE_CONTENTS`) | `BundleContents` | yes (cached) | yes |
| `potion_contents` (`DataComponents.POTION_CONTENTS`) | `PotionContents` | yes (cached) | yes |
| `potion_duration_scale` (`DataComponents.POTION_DURATION_SCALE`) | `Float` | yes (cached) | yes |
| `suspicious_stew_effects` (`DataComponents.SUSPICIOUS_STEW_EFFECTS`) | `SuspiciousStewEffects` | yes (cached) | yes |
| `writable_book_content` (`DataComponents.WRITABLE_BOOK_CONTENT`) | `WritableBookContent` | yes (cached) | yes |
| `written_book_content` (`DataComponents.WRITTEN_BOOK_CONTENT`) | `WrittenBookContent` | yes (cached) | yes |
| `trim` (`DataComponents.TRIM`) | `ArmorTrim` | yes (cached) | yes |
| `debug_stick_state` (`DataComponents.DEBUG_STICK_STATE`) | `DebugStickState` | yes (cached) |  |
| `entity_data` (`DataComponents.ENTITY_DATA`) | `TypedEntityData<…>` | yes | yes |
| `bucket_entity_data` (`DataComponents.BUCKET_ENTITY_DATA`) | `CustomData` | yes | yes |
| `block_entity_data` (`DataComponents.BLOCK_ENTITY_DATA`) | `TypedEntityData<…>` | yes | yes |
| `instrument` (`DataComponents.INSTRUMENT`) | `InstrumentComponent` | yes (cached) | yes |
| `provides_trim_material` (`DataComponents.PROVIDES_TRIM_MATERIAL`) | `Holder<…>` | yes (cached) | yes |
| `ominous_bottle_amplifier` (`DataComponents.OMINOUS_BOTTLE_AMPLIFIER`) | `OminousBottleAmplifier` | yes | yes |
| `jukebox_playable` (`DataComponents.JUKEBOX_PLAYABLE`) | `JukeboxPlayable` | yes | yes |
| `provides_banner_patterns` (`DataComponents.PROVIDES_BANNER_PATTERNS`) | `HolderSet<…>` | yes (cached) | yes |
| `recipes` (`DataComponents.RECIPES`) | `List<…>` | yes (cached) |  |
| `lodestone_tracker` (`DataComponents.LODESTONE_TRACKER`) | `LodestoneTracker` | yes (cached) | yes |
| `firework_explosion` (`DataComponents.FIREWORK_EXPLOSION`) | `FireworkExplosion` | yes (cached) | yes |
| `fireworks` (`DataComponents.FIREWORKS`) | `Fireworks` | yes (cached) | yes |
| `profile` (`DataComponents.PROFILE`) | `ResolvableProfile` | yes (cached) | yes |
| `note_block_sound` (`DataComponents.NOTE_BLOCK_SOUND`) | `Identifier` | yes | yes |
| `banner_patterns` (`DataComponents.BANNER_PATTERNS`) | `BannerPatternLayers` | yes (cached) | yes |
| `base_color` (`DataComponents.BASE_COLOR`) | `DyeColor` | yes | yes |
| `pot_decorations` (`DataComponents.POT_DECORATIONS`) | `PotDecorations` | yes (cached) | yes |
| `container` (`DataComponents.CONTAINER`) | `ItemContainerContents` | yes (cached) | yes |
| `block_state` (`DataComponents.BLOCK_STATE`) | `BlockItemStateProperties` | yes (cached) | yes |
| `bees` (`DataComponents.BEES`) | `Bees` | yes (cached) | yes |
| `sulfur_cube_content` (`DataComponents.SULFUR_CUBE_CONTENT`) | `SulfurCubeContent` | yes (cached) | yes |
| `lock` (`DataComponents.LOCK`) | `LockCode` | yes |  |
| `container_loot` (`DataComponents.CONTAINER_LOOT`) | `SeededContainerLoot` | yes |  |
| `break_sound` (`DataComponents.BREAK_SOUND`) | `Holder<…>` | yes (cached) | yes |
| `villager/variant` (`DataComponents.VILLAGER_VARIANT`) | `Holder<…>` | yes | yes |
| `wolf/variant` (`DataComponents.WOLF_VARIANT`) | `Holder<…>` | yes | yes |
| `wolf/sound_variant` (`DataComponents.WOLF_SOUND_VARIANT`) | `Holder<…>` | yes | yes |
| `wolf/collar` (`DataComponents.WOLF_COLLAR`) | `DyeColor` | yes | yes |
| `fox/variant` (`DataComponents.FOX_VARIANT`) | `Fox.Variant` | yes | yes |
| `salmon/size` (`DataComponents.SALMON_SIZE`) | `Salmon.Variant` | yes | yes |
| `parrot/variant` (`DataComponents.PARROT_VARIANT`) | `Parrot.Variant` | yes | yes |
| `tropical_fish/pattern` (`DataComponents.TROPICAL_FISH_PATTERN`) | `TropicalFish.Pattern` | yes | yes |
| `tropical_fish/base_color` (`DataComponents.TROPICAL_FISH_BASE_COLOR`) | `DyeColor` | yes | yes |
| `tropical_fish/pattern_color` (`DataComponents.TROPICAL_FISH_PATTERN_COLOR`) | `DyeColor` | yes | yes |
| `mooshroom/variant` (`DataComponents.MOOSHROOM_VARIANT`) | `MushroomCow.Variant` | yes | yes |
| `rabbit/variant` (`DataComponents.RABBIT_VARIANT`) | `Rabbit.Variant` | yes | yes |
| `pig/variant` (`DataComponents.PIG_VARIANT`) | `Holder<…>` | yes | yes |
| `pig/sound_variant` (`DataComponents.PIG_SOUND_VARIANT`) | `Holder<…>` | yes | yes |
| `cow/variant` (`DataComponents.COW_VARIANT`) | `Holder<…>` | yes | yes |
| `cow/sound_variant` (`DataComponents.COW_SOUND_VARIANT`) | `Holder<…>` | yes | yes |
| `chicken/variant` (`DataComponents.CHICKEN_VARIANT`) | `Holder<…>` | yes | yes |
| `chicken/sound_variant` (`DataComponents.CHICKEN_SOUND_VARIANT`) | `Holder<…>` | yes | yes |
| `zombie_nautilus/variant` (`DataComponents.ZOMBIE_NAUTILUS_VARIANT`) | `Holder<…>` | yes | yes |
| `frog/variant` (`DataComponents.FROG_VARIANT`) | `Holder<…>` | yes | yes |
| `horse/variant` (`DataComponents.HORSE_VARIANT`) | `Variant` | yes | yes |
| `painting/variant` (`DataComponents.PAINTING_VARIANT`) | `Holder<…>` | yes | yes |
| `llama/variant` (`DataComponents.LLAMA_VARIANT`) | `Llama.Variant` | yes | yes |
| `axolotl/variant` (`DataComponents.AXOLOTL_VARIANT`) | `Axolotl.Variant` | yes | yes |
| `cat/variant` (`DataComponents.CAT_VARIANT`) | `Holder<…>` | yes | yes |
| `cat/sound_variant` (`DataComponents.CAT_SOUND_VARIANT`) | `Holder<…>` | yes | yes |
| `cat/collar` (`DataComponents.CAT_COLLAR`) | `DyeColor` | yes | yes |
| `sheep/color` (`DataComponents.SHEEP_COLOR`) | `DyeColor` | yes | yes |
| `shulker/color` (`DataComponents.SHULKER_COLOR`) | `DyeColor` | yes | yes |
