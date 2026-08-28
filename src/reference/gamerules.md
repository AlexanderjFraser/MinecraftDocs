# Game rules

> Generated from the **26.2** decompile by `tools/gen_reference.py`. Do not edit by hand.

Every rule declared in `GameRules`, with its category (`GameRuleCategory`) and default. Integer rules list their minimum after the default where one is declared. Values live per world in a `GameRuleMap` on the level data. See [Level data and rules](../systems/world/level-data-and-rules.md).

59 rules

| rule | type | category | default |
|---|---|---|---|
| `command_block_output` (`GameRules.COMMAND_BLOCK_OUTPUT`) | Boolean | chat | `true` |
| `log_admin_commands` (`GameRules.LOG_ADMIN_COMMANDS`) | Boolean | chat | `true` |
| `send_command_feedback` (`GameRules.SEND_COMMAND_FEEDBACK`) | Boolean | chat | `true` |
| `show_advancement_messages` (`GameRules.SHOW_ADVANCEMENT_MESSAGES`) | Boolean | chat | `true` |
| `show_death_messages` (`GameRules.SHOW_DEATH_MESSAGES`) | Boolean | chat | `true` |
| `block_drops` (`GameRules.BLOCK_DROPS`) | Boolean | drops | `true` |
| `block_explosion_drop_decay` (`GameRules.BLOCK_EXPLOSION_DROP_DECAY`) | Boolean | drops | `true` |
| `entity_drops` (`GameRules.ENTITY_DROPS`) | Boolean | drops | `true` |
| `mob_drops` (`GameRules.MOB_DROPS`) | Boolean | drops | `true` |
| `mob_explosion_drop_decay` (`GameRules.MOB_EXPLOSION_DROP_DECAY`) | Boolean | drops | `true` |
| `projectiles_can_break_blocks` (`GameRules.PROJECTILES_CAN_BREAK_BLOCKS`) | Boolean | drops | `true` |
| `tnt_explosion_drop_decay` (`GameRules.TNT_EXPLOSION_DROP_DECAY`) | Boolean | drops | `false` |
| `allow_entering_nether_using_portals` (`GameRules.ALLOW_ENTERING_NETHER_USING_PORTALS`) | Boolean | misc | `true` |
| `command_blocks_work` (`GameRules.COMMAND_BLOCKS_WORK`) | Boolean | misc | `true` |
| `global_sound_events` (`GameRules.GLOBAL_SOUND_EVENTS`) | Boolean | misc | `true` |
| `max_block_modifications` (`GameRules.MAX_BLOCK_MODIFICATIONS`) | Integer | misc | `32768 (min 1)` |
| `max_command_forks` (`GameRules.MAX_COMMAND_FORKS`) | Integer | misc | `65536 (min 0)` |
| `max_command_sequence_length` (`GameRules.MAX_COMMAND_SEQUENCE_LENGTH`) | Integer | misc | `65536 (min 0)` |
| `max_minecart_speed` (`GameRules.MAX_MINECART_SPEED`) | Integer | misc | `8 (min 1, 1000, FeatureFlagSet.of(FeatureFlags.MINECART_IMPROVEMENTS)` |
| `reduced_debug_info` (`GameRules.REDUCED_DEBUG_INFO`) | Boolean | misc | `false` |
| `spawner_blocks_work` (`GameRules.SPAWNER_BLOCKS_WORK`) | Boolean | misc | `true` |
| `tnt_explodes` (`GameRules.TNT_EXPLODES`) | Boolean | misc | `true` |
| `forgive_dead_players` (`GameRules.FORGIVE_DEAD_PLAYERS`) | Boolean | mobs | `true` |
| `max_entity_cramming` (`GameRules.MAX_ENTITY_CRAMMING`) | Integer | mobs | `24 (min 0)` |
| `mob_griefing` (`GameRules.MOB_GRIEFING`) | Boolean | mobs | `true` |
| `raids` (`GameRules.RAIDS`) | Boolean | mobs | `true` |
| `universal_anger` (`GameRules.UNIVERSAL_ANGER`) | Boolean | mobs | `false` |
| `drowning_damage` (`GameRules.DROWNING_DAMAGE`) | Boolean | player | `true` |
| `elytra_movement_check` (`GameRules.ELYTRA_MOVEMENT_CHECK`) | Boolean | player | `true` |
| `ender_pearls_vanish_on_death` (`GameRules.ENDER_PEARLS_VANISH_ON_DEATH`) | Boolean | player | `true` |
| `fall_damage` (`GameRules.FALL_DAMAGE`) | Boolean | player | `true` |
| `fire_damage` (`GameRules.FIRE_DAMAGE`) | Boolean | player | `true` |
| `freeze_damage` (`GameRules.FREEZE_DAMAGE`) | Boolean | player | `true` |
| `immediate_respawn` (`GameRules.IMMEDIATE_RESPAWN`) | Boolean | player | `false` |
| `keep_inventory` (`GameRules.KEEP_INVENTORY`) | Boolean | player | `false` |
| `limited_crafting` (`GameRules.LIMITED_CRAFTING`) | Boolean | player | `false` |
| `locator_bar` (`GameRules.LOCATOR_BAR`) | Boolean | player | `true` |
| `natural_health_regeneration` (`GameRules.NATURAL_HEALTH_REGENERATION`) | Boolean | player | `true` |
| `player_movement_check` (`GameRules.PLAYER_MOVEMENT_CHECK`) | Boolean | player | `true` |
| `players_nether_portal_creative_delay` (`GameRules.PLAYERS_NETHER_PORTAL_CREATIVE_DELAY`) | Integer | player | `0 (min 0)` |
| `players_nether_portal_default_delay` (`GameRules.PLAYERS_NETHER_PORTAL_DEFAULT_DELAY`) | Integer | player | `80 (min 0)` |
| `players_sleeping_percentage` (`GameRules.PLAYERS_SLEEPING_PERCENTAGE`) | Integer | player | `100 (min 0)` |
| `pvp` (`GameRules.PVP`) | Boolean | player | `true` |
| `respawn_radius` (`GameRules.RESPAWN_RADIUS`) | Integer | player | `10 (min 0)` |
| `spectators_generate_chunks` (`GameRules.SPECTATORS_GENERATE_CHUNKS`) | Boolean | player | `true` |
| `spawn_mobs` (`GameRules.SPAWN_MOBS`) | Boolean | spawning | `true` |
| `spawn_monsters` (`GameRules.SPAWN_MONSTERS`) | Boolean | spawning | `true` |
| `spawn_patrols` (`GameRules.SPAWN_PATROLS`) | Boolean | spawning | `true` |
| `spawn_phantoms` (`GameRules.SPAWN_PHANTOMS`) | Boolean | spawning | `true` |
| `spawn_wandering_traders` (`GameRules.SPAWN_WANDERING_TRADERS`) | Boolean | spawning | `true` |
| `spawn_wardens` (`GameRules.SPAWN_WARDENS`) | Boolean | spawning | `true` |
| `advance_time` (`GameRules.ADVANCE_TIME`) | Boolean | updates | `true` |
| `advance_weather` (`GameRules.ADVANCE_WEATHER`) | Boolean | updates | `true` |
| `fire_spread_radius_around_player` (`GameRules.FIRE_SPREAD_RADIUS_AROUND_PLAYER`) | Integer | updates | `128 (min -1)` |
| `lava_source_conversion` (`GameRules.LAVA_SOURCE_CONVERSION`) | Boolean | updates | `false` |
| `max_snow_accumulation_height` (`GameRules.MAX_SNOW_ACCUMULATION_HEIGHT`) | Integer | updates | `1 (min 0, 8)` |
| `random_tick_speed` (`GameRules.RANDOM_TICK_SPEED`) | Integer | updates | `3 (min 0)` |
| `spread_vines` (`GameRules.SPREAD_VINES`) | Boolean | updates | `true` |
| `water_source_conversion` (`GameRules.WATER_SOURCE_CONVERSION`) | Boolean | updates | `true` |
