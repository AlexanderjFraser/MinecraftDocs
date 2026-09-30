# Data components

> Generated from the **26.3** decompile by `tools/gen_reference.py`. Do not edit by hand.

Every `DataComponentType` registered in `DataComponents`. *Persistent* types have a `Codec` and are written to disk; a type without one is *transient* (`DataComponentType.isTransient`), never saved but sent like the rest. Every type crosses the wire: the *on the wire* column says whether it declares its own `StreamCodec` or is sent as NBT through the one `DataComponentType.Builder.build` derives from its `Codec`, and a type with neither cannot be built. *Cached* persistent codecs share one `EncoderCache`. See [Data components](../systems/foundations/data-components.md).

122 components

| id | value type | persistent | on the wire |
|---|---|---|---|
| `custom_data` (`DataComponents.CUSTOM_DATA`) | `CustomData` | yes | NBT, through its `Codec` |
| `max_stack_size` (`DataComponents.MAX_STACK_SIZE`) | `Integer` | yes | its own `StreamCodec` |
| `max_damage` (`DataComponents.MAX_DAMAGE`) | `Integer` | yes | its own `StreamCodec` |
| `damage` (`DataComponents.DAMAGE`) | `Integer` | yes | its own `StreamCodec` |
| `unbreakable` (`DataComponents.UNBREAKABLE`) | `Unit` | yes | its own `StreamCodec` |
| `use_effects` (`DataComponents.USE_EFFECTS`) | `UseEffects` | yes | its own `StreamCodec` |
| `custom_name` (`DataComponents.CUSTOM_NAME`) | `Component` | yes (cached) | its own `StreamCodec` |
| `minimum_attack_charge` (`DataComponents.MINIMUM_ATTACK_CHARGE`) | `Float` | yes | its own `StreamCodec` |
| `damage_type` (`DataComponents.DAMAGE_TYPE`) | `Holder<…>` | yes | its own `StreamCodec` |
| `item_name` (`DataComponents.ITEM_NAME`) | `Component` | yes (cached) | its own `StreamCodec` |
| `item_model` (`DataComponents.ITEM_MODEL`) | `Identifier` | yes (cached) | its own `StreamCodec` |
| `lore` (`DataComponents.LORE`) | `ItemLore` | yes (cached) | its own `StreamCodec` |
| `rarity` (`DataComponents.RARITY`) | `Rarity` | yes | its own `StreamCodec` |
| `enchantments` (`DataComponents.ENCHANTMENTS`) | `ItemEnchantments` | yes (cached) | its own `StreamCodec` |
| `can_place_on` (`DataComponents.CAN_PLACE_ON`) | `AdventureModePredicate` | yes (cached) | its own `StreamCodec` |
| `can_break` (`DataComponents.CAN_BREAK`) | `AdventureModePredicate` | yes (cached) | its own `StreamCodec` |
| `attribute_modifiers` (`DataComponents.ATTRIBUTE_MODIFIERS`) | `ItemAttributeModifiers` | yes (cached) | its own `StreamCodec` |
| `custom_model_data` (`DataComponents.CUSTOM_MODEL_DATA`) | `CustomModelData` | yes | its own `StreamCodec` |
| `tooltip_display` (`DataComponents.TOOLTIP_DISPLAY`) | `TooltipDisplay` | yes (cached) | its own `StreamCodec` |
| `repair_cost` (`DataComponents.REPAIR_COST`) | `Integer` | yes | its own `StreamCodec` |
| `creative_slot_lock` (`DataComponents.CREATIVE_SLOT_LOCK`) | `Unit` |  | its own `StreamCodec` |
| `enchantment_glint_override` (`DataComponents.ENCHANTMENT_GLINT_OVERRIDE`) | `Boolean` | yes | its own `StreamCodec` |
| `intangible_projectile` (`DataComponents.INTANGIBLE_PROJECTILE`) | `Unit` | yes | NBT, through its `Codec` |
| `food` (`DataComponents.FOOD`) | `FoodProperties` | yes (cached) | its own `StreamCodec` |
| `consumable` (`DataComponents.CONSUMABLE`) | `Consumable` | yes (cached) | its own `StreamCodec` |
| `use_remainder` (`DataComponents.USE_REMAINDER`) | `UseRemainder` | yes (cached) | its own `StreamCodec` |
| `use_cooldown` (`DataComponents.USE_COOLDOWN`) | `UseCooldown` | yes (cached) | its own `StreamCodec` |
| `damage_resistant` (`DataComponents.DAMAGE_RESISTANT`) | `DamageResistant` | yes (cached) | its own `StreamCodec` |
| `tool` (`DataComponents.TOOL`) | `Tool` | yes (cached) | its own `StreamCodec` |
| `weapon` (`DataComponents.WEAPON`) | `Weapon` | yes (cached) | its own `StreamCodec` |
| `attack_range` (`DataComponents.ATTACK_RANGE`) | `AttackRange` | yes (cached) | its own `StreamCodec` |
| `enchantable` (`DataComponents.ENCHANTABLE`) | `Enchantable` | yes (cached) | its own `StreamCodec` |
| `equippable` (`DataComponents.EQUIPPABLE`) | `Equippable` | yes (cached) | its own `StreamCodec` |
| `repairable` (`DataComponents.REPAIRABLE`) | `Repairable` | yes (cached) | its own `StreamCodec` |
| `glider` (`DataComponents.GLIDER`) | `Unit` | yes | its own `StreamCodec` |
| `tooltip_style` (`DataComponents.TOOLTIP_STYLE`) | `Identifier` | yes (cached) | its own `StreamCodec` |
| `death_protection` (`DataComponents.DEATH_PROTECTION`) | `DeathProtection` | yes (cached) | its own `StreamCodec` |
| `blocks_attacks` (`DataComponents.BLOCKS_ATTACKS`) | `BlocksAttacks` | yes (cached) | its own `StreamCodec` |
| `piercing_weapon` (`DataComponents.PIERCING_WEAPON`) | `PiercingWeapon` | yes (cached) | its own `StreamCodec` |
| `kinetic_weapon` (`DataComponents.KINETIC_WEAPON`) | `KineticWeapon` | yes (cached) | its own `StreamCodec` |
| `attack_animation` (`DataComponents.ATTACK_ANIMATION`) | `SwingAnimation` | yes | its own `StreamCodec` |
| `interact_animation` (`DataComponents.INTERACT_ANIMATION`) | `SwingAnimation` | yes | its own `StreamCodec` |
| `additional_trade_cost` (`DataComponents.ADDITIONAL_TRADE_COST`) | `Integer` |  | its own `StreamCodec` |
| `block_transformer` (`DataComponents.BLOCK_TRANSFORMER`) | `Holder<…>` | yes (cached) | its own `StreamCodec` |
| `villager_food` (`DataComponents.VILLAGER_FOOD`) | `VillagerFood` | yes | its own `StreamCodec` |
| `stored_enchantments` (`DataComponents.STORED_ENCHANTMENTS`) | `ItemEnchantments` | yes (cached) | its own `StreamCodec` |
| `dye` (`DataComponents.DYE`) | `DyeColor` | yes | its own `StreamCodec` |
| `dyed_color` (`DataComponents.DYED_COLOR`) | `DyedItemColor` | yes | its own `StreamCodec` |
| `map_id` (`DataComponents.MAP_ID`) | `MapId` | yes | its own `StreamCodec` |
| `map_decorations` (`DataComponents.MAP_DECORATIONS`) | `MapDecorations` | yes (cached) | NBT, through its `Codec` |
| `map_post_processing` (`DataComponents.MAP_POST_PROCESSING`) | `MapPostProcessing` |  | its own `StreamCodec` |
| `charged_projectiles` (`DataComponents.CHARGED_PROJECTILES`) | `ChargedProjectiles` | yes (cached) | its own `StreamCodec` |
| `bundle_contents` (`DataComponents.BUNDLE_CONTENTS`) | `BundleContents` | yes (cached) | its own `StreamCodec` |
| `potion_contents` (`DataComponents.POTION_CONTENTS`) | `PotionContents` | yes (cached) | its own `StreamCodec` |
| `potion_duration_scale` (`DataComponents.POTION_DURATION_SCALE`) | `Float` | yes (cached) | its own `StreamCodec` |
| `suspicious_stew_effects` (`DataComponents.SUSPICIOUS_STEW_EFFECTS`) | `SuspiciousStewEffects` | yes (cached) | its own `StreamCodec` |
| `writable_book_content` (`DataComponents.WRITABLE_BOOK_CONTENT`) | `WritableBookContent` | yes (cached) | its own `StreamCodec` |
| `written_book_content` (`DataComponents.WRITTEN_BOOK_CONTENT`) | `WrittenBookContent` | yes (cached) | its own `StreamCodec` |
| `trim` (`DataComponents.TRIM`) | `ArmorTrim` | yes (cached) | its own `StreamCodec` |
| `debug_stick_state` (`DataComponents.DEBUG_STICK_STATE`) | `DebugStickState` | yes (cached) | NBT, through its `Codec` |
| `entity_data` (`DataComponents.ENTITY_DATA`) | `TypedEntityData<…>` | yes | its own `StreamCodec` |
| `bucket_entity_data` (`DataComponents.BUCKET_ENTITY_DATA`) | `CustomData` | yes | its own `StreamCodec` |
| `block_entity_data` (`DataComponents.BLOCK_ENTITY_DATA`) | `TypedEntityData<…>` | yes | its own `StreamCodec` |
| `instrument` (`DataComponents.INSTRUMENT`) | `InstrumentComponent` | yes (cached) | its own `StreamCodec` |
| `provides_trim_material` (`DataComponents.PROVIDES_TRIM_MATERIAL`) | `Holder<…>` | yes (cached) | its own `StreamCodec` |
| `ominous_bottle_amplifier` (`DataComponents.OMINOUS_BOTTLE_AMPLIFIER`) | `OminousBottleAmplifier` | yes | its own `StreamCodec` |
| `jukebox_playable` (`DataComponents.JUKEBOX_PLAYABLE`) | `JukeboxPlayable` | yes | its own `StreamCodec` |
| `provides_banner_patterns` (`DataComponents.PROVIDES_BANNER_PATTERNS`) | `HolderSet<…>` | yes (cached) | its own `StreamCodec` |
| `recipes` (`DataComponents.RECIPES`) | `List<…>` | yes (cached) | NBT, through its `Codec` |
| `lodestone_tracker` (`DataComponents.LODESTONE_TRACKER`) | `LodestoneTracker` | yes (cached) | its own `StreamCodec` |
| `firework_explosion` (`DataComponents.FIREWORK_EXPLOSION`) | `FireworkExplosion` | yes (cached) | its own `StreamCodec` |
| `fireworks` (`DataComponents.FIREWORKS`) | `Fireworks` | yes (cached) | its own `StreamCodec` |
| `profile` (`DataComponents.PROFILE`) | `ResolvableProfile` | yes (cached) | its own `StreamCodec` |
| `note_block_sound` (`DataComponents.NOTE_BLOCK_SOUND`) | `Identifier` | yes | its own `StreamCodec` |
| `banner_patterns` (`DataComponents.BANNER_PATTERNS`) | `BannerPatternLayers` | yes (cached) | its own `StreamCodec` |
| `base_color` (`DataComponents.BASE_COLOR`) | `DyeColor` | yes | its own `StreamCodec` |
| `pot_decorations` (`DataComponents.POT_DECORATIONS`) | `PotDecorations` | yes (cached) | its own `StreamCodec` |
| `container` (`DataComponents.CONTAINER`) | `ItemContainerContents` | yes (cached) | its own `StreamCodec` |
| `block_state` (`DataComponents.BLOCK_STATE`) | `BlockItemStateProperties` | yes (cached) | its own `StreamCodec` |
| `bees` (`DataComponents.BEES`) | `Bees` | yes (cached) | its own `StreamCodec` |
| `sulfur_cube_content` (`DataComponents.SULFUR_CUBE_CONTENT`) | `SulfurCubeContent` | yes (cached) | its own `StreamCodec` |
| `lock` (`DataComponents.LOCK`) | `LockCode` | yes | NBT, through its `Codec` |
| `container_loot` (`DataComponents.CONTAINER_LOOT`) | `SeededContainerLoot` | yes | NBT, through its `Codec` |
| `break_sound` (`DataComponents.BREAK_SOUND`) | `Holder<…>` | yes (cached) | its own `StreamCodec` |
| `compostable` (`DataComponents.COMPOSTABLE`) | `Compostable` | yes | its own `StreamCodec` |
| `cooking_fuel` (`DataComponents.COOKING_FUEL`) | `CookingFuel` | yes | its own `StreamCodec` |
| `brewing_fuel` (`DataComponents.BREWING_FUEL`) | `BrewingFuel` | yes | its own `StreamCodec` |
| `mob_visibility` (`DataComponents.MOB_VISIBILITY`) | `MobVisibility` | yes | its own `StreamCodec` |
| `villager/variant` (`DataComponents.VILLAGER_VARIANT`) | `Holder<…>` | yes | its own `StreamCodec` |
| `wolf/variant` (`DataComponents.WOLF_VARIANT`) | `Holder<…>` | yes | its own `StreamCodec` |
| `wolf/sound_variant` (`DataComponents.WOLF_SOUND_VARIANT`) | `Holder<…>` | yes | its own `StreamCodec` |
| `wolf/collar` (`DataComponents.WOLF_COLLAR`) | `DyeColor` | yes | its own `StreamCodec` |
| `fox/variant` (`DataComponents.FOX_VARIANT`) | `Fox.Variant` | yes | its own `StreamCodec` |
| `salmon/size` (`DataComponents.SALMON_SIZE`) | `Salmon.Variant` | yes | its own `StreamCodec` |
| `parrot/variant` (`DataComponents.PARROT_VARIANT`) | `Parrot.Variant` | yes | its own `StreamCodec` |
| `tropical_fish/pattern` (`DataComponents.TROPICAL_FISH_PATTERN`) | `TropicalFish.Pattern` | yes | its own `StreamCodec` |
| `tropical_fish/base_color` (`DataComponents.TROPICAL_FISH_BASE_COLOR`) | `DyeColor` | yes | its own `StreamCodec` |
| `tropical_fish/pattern_color` (`DataComponents.TROPICAL_FISH_PATTERN_COLOR`) | `DyeColor` | yes | its own `StreamCodec` |
| `mooshroom/variant` (`DataComponents.MOOSHROOM_VARIANT`) | `MushroomCow.Variant` | yes | its own `StreamCodec` |
| `rabbit/variant` (`DataComponents.RABBIT_VARIANT`) | `Rabbit.Variant` | yes | its own `StreamCodec` |
| `pig/variant` (`DataComponents.PIG_VARIANT`) | `Holder<…>` | yes | its own `StreamCodec` |
| `pig/sound_variant` (`DataComponents.PIG_SOUND_VARIANT`) | `Holder<…>` | yes | its own `StreamCodec` |
| `cow/variant` (`DataComponents.COW_VARIANT`) | `Holder<…>` | yes | its own `StreamCodec` |
| `cow/sound_variant` (`DataComponents.COW_SOUND_VARIANT`) | `Holder<…>` | yes | its own `StreamCodec` |
| `chicken/variant` (`DataComponents.CHICKEN_VARIANT`) | `Holder<…>` | yes | its own `StreamCodec` |
| `chicken/sound_variant` (`DataComponents.CHICKEN_SOUND_VARIANT`) | `Holder<…>` | yes | its own `StreamCodec` |
| `zombie_nautilus/variant` (`DataComponents.ZOMBIE_NAUTILUS_VARIANT`) | `Holder<…>` | yes | its own `StreamCodec` |
| `frog/variant` (`DataComponents.FROG_VARIANT`) | `Holder<…>` | yes | its own `StreamCodec` |
| `horse/variant` (`DataComponents.HORSE_VARIANT`) | `Variant` | yes | its own `StreamCodec` |
| `painting/variant` (`DataComponents.PAINTING_VARIANT`) | `Holder<…>` | yes | its own `StreamCodec` |
| `llama/variant` (`DataComponents.LLAMA_VARIANT`) | `Llama.Variant` | yes | its own `StreamCodec` |
| `axolotl/variant` (`DataComponents.AXOLOTL_VARIANT`) | `Axolotl.Variant` | yes | its own `StreamCodec` |
| `cat/variant` (`DataComponents.CAT_VARIANT`) | `Holder<…>` | yes | its own `StreamCodec` |
| `cat/sound_variant` (`DataComponents.CAT_SOUND_VARIANT`) | `Holder<…>` | yes | its own `StreamCodec` |
| `cat/collar` (`DataComponents.CAT_COLLAR`) | `DyeColor` | yes | its own `StreamCodec` |
| `sheep/color` (`DataComponents.SHEEP_COLOR`) | `DyeColor` | yes | its own `StreamCodec` |
| `shulker/color` (`DataComponents.SHULKER_COLOR`) | `DyeColor` | yes | its own `StreamCodec` |
| `provides_pottery_pattern` (`DataComponents.PROVIDES_POTTERY_PATTERN`) | `Holder<…>` | yes | its own `StreamCodec` |
| `sign_text_front` (`DataComponents.SIGN_TEXT_FRONT`) | `SignText` | yes (cached) | its own `StreamCodec` |
| `sign_text_back` (`DataComponents.SIGN_TEXT_BACK`) | `SignText` | yes (cached) | its own `StreamCodec` |
| `waxed` (`DataComponents.WAXED`) | `Unit` | yes | its own `StreamCodec` |
| `cushion/color` (`DataComponents.CUSHION_COLOR`) | `DyeColor` | yes | its own `StreamCodec` |
