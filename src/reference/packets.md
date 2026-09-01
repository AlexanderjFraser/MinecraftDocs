# Packets

> Generated from the **26.2** decompile by `tools/gen_reference.py`. Do not edit by hand.

Every packet the game defines, by the `PacketTypes` class that declares it. `common`, `cookie` and `ping` packets are shared by more than one protocol phase; the exact phase→packet bindings are in the `*Protocols` classes next to each `PacketTypes` class (`GameProtocols`, `ConfigurationProtocols`, `LoginProtocols`, `StatusProtocols`, `HandshakeProtocols`). See [Packets and stream codecs](../systems/networking/packets-and-stream-codecs.md).

| group | clientbound | serverbound |
|---|---:|---:|
| `common` (`CommonPacketTypes`) | 13 | 6 |
| `configuration` (`ConfigurationPacketTypes`) | 6 | 3 |
| `cookie` (`CookiePacketTypes`) | 1 | 1 |
| `game` (`GamePacketTypes`) | 127 | 61 |
| `handshake` (`HandshakePacketTypes`) | 0 | 1 |
| `login` (`LoginPacketTypes`) | 5 | 4 |
| `ping` (`PingPacketTypes`) | 1 | 1 |
| `status` (`StatusPacketTypes`) | 1 | 1 |
| **total** | | **232** |

## `common` — `CommonPacketTypes` — shared across phases

| id | direction | class |
|---|---|---|
| `clear_dialog` | clientbound | `ClientboundClearDialogPacket` |
| `custom_payload` | clientbound | `ClientboundCustomPayloadPacket` |
| `custom_report_details` | clientbound | `ClientboundCustomReportDetailsPacket` |
| `disconnect` | clientbound | `ClientboundDisconnectPacket` |
| `keep_alive` | clientbound | `ClientboundKeepAlivePacket` |
| `ping` | clientbound | `ClientboundPingPacket` |
| `resource_pack_pop` | clientbound | `ClientboundResourcePackPopPacket` |
| `resource_pack_push` | clientbound | `ClientboundResourcePackPushPacket` |
| `server_links` | clientbound | `ClientboundServerLinksPacket` |
| `show_dialog` | clientbound | `ClientboundShowDialogPacket` |
| `store_cookie` | clientbound | `ClientboundStoreCookiePacket` |
| `transfer` | clientbound | `ClientboundTransferPacket` |
| `update_tags` | clientbound | `ClientboundUpdateTagsPacket` |
| `client_information` | serverbound | `ServerboundClientInformationPacket` |
| `custom_click_action` | serverbound | `ServerboundCustomClickActionPacket` |
| `custom_payload` | serverbound | `ServerboundCustomPayloadPacket` |
| `keep_alive` | serverbound | `ServerboundKeepAlivePacket` |
| `pong` | serverbound | `ServerboundPongPacket` |
| `resource_pack` | serverbound | `ServerboundResourcePackPacket` |

## `configuration` — `ConfigurationPacketTypes`

| id | direction | class |
|---|---|---|
| `code_of_conduct` | clientbound | `ClientboundCodeOfConductPacket` |
| `finish_configuration` | clientbound | `ClientboundFinishConfigurationPacket` |
| `registry_data` | clientbound | `ClientboundRegistryDataPacket` |
| `reset_chat` | clientbound | `ClientboundResetChatPacket` |
| `select_known_packs` | clientbound | `ClientboundSelectKnownPacks` |
| `update_enabled_features` | clientbound | `ClientboundUpdateEnabledFeaturesPacket` |
| `accept_code_of_conduct` | serverbound | `ServerboundAcceptCodeOfConductPacket` |
| `finish_configuration` | serverbound | `ServerboundFinishConfigurationPacket` |
| `select_known_packs` | serverbound | `ServerboundSelectKnownPacks` |

## `cookie` — `CookiePacketTypes` — shared across phases

| id | direction | class |
|---|---|---|
| `cookie_request` | clientbound | `ClientboundCookieRequestPacket` |
| `cookie_response` | serverbound | `ServerboundCookieResponsePacket` |

## `game` — `GamePacketTypes`

| id | direction | class |
|---|---|---|
| `add_entity` | clientbound | `ClientboundAddEntityPacket` |
| `animate` | clientbound | `ClientboundAnimatePacket` |
| `award_stats` | clientbound | `ClientboundAwardStatsPacket` |
| `block_changed_ack` | clientbound | `ClientboundBlockChangedAckPacket` |
| `block_destruction` | clientbound | `ClientboundBlockDestructionPacket` |
| `block_entity_data` | clientbound | `ClientboundBlockEntityDataPacket` |
| `block_event` | clientbound | `ClientboundBlockEventPacket` |
| `block_update` | clientbound | `ClientboundBlockUpdatePacket` |
| `boss_event` | clientbound | `ClientboundBossEventPacket` |
| `bundle` | clientbound | `ClientboundBundlePacket` |
| `bundle_delimiter` | clientbound | `ClientboundBundleDelimiterPacket` |
| `change_difficulty` | clientbound | `ClientboundChangeDifficultyPacket` |
| `chunk_batch_finished` | clientbound | `ClientboundChunkBatchFinishedPacket` |
| `chunk_batch_start` | clientbound | `ClientboundChunkBatchStartPacket` |
| `chunks_biomes` | clientbound | `ClientboundChunksBiomesPacket` |
| `clear_titles` | clientbound | `ClientboundClearTitlesPacket` |
| `command_suggestions` | clientbound | `ClientboundCommandSuggestionsPacket` |
| `commands` | clientbound | `ClientboundCommandsPacket` |
| `container_close` | clientbound | `ClientboundContainerClosePacket` |
| `container_set_content` | clientbound | `ClientboundContainerSetContentPacket` |
| `container_set_data` | clientbound | `ClientboundContainerSetDataPacket` |
| `container_set_slot` | clientbound | `ClientboundContainerSetSlotPacket` |
| `cooldown` | clientbound | `ClientboundCooldownPacket` |
| `custom_chat_completions` | clientbound | `ClientboundCustomChatCompletionsPacket` |
| `damage_event` | clientbound | `ClientboundDamageEventPacket` |
| `debug/block_value` | clientbound | `ClientboundDebugBlockValuePacket` |
| `debug/chunk_value` | clientbound | `ClientboundDebugChunkValuePacket` |
| `debug/entity_value` | clientbound | `ClientboundDebugEntityValuePacket` |
| `debug/event` | clientbound | `ClientboundDebugEventPacket` |
| `debug_sample` | clientbound | `ClientboundDebugSamplePacket` |
| `delete_chat` | clientbound | `ClientboundDeleteChatPacket` |
| `disguised_chat` | clientbound | `ClientboundDisguisedChatPacket` |
| `entity_event` | clientbound | `ClientboundEntityEventPacket` |
| `entity_position_sync` | clientbound | `ClientboundEntityPositionSyncPacket` |
| `explode` | clientbound | `ClientboundExplodePacket` |
| `forget_level_chunk` | clientbound | `ClientboundForgetLevelChunkPacket` |
| `game_event` | clientbound | `ClientboundGameEventPacket` |
| `game_rule_values` | clientbound | `ClientboundGameRuleValuesPacket` |
| `game_test_highlight_pos` | clientbound | `ClientboundGameTestHighlightPosPacket` |
| `hurt_animation` | clientbound | `ClientboundHurtAnimationPacket` |
| `initialize_border` | clientbound | `ClientboundInitializeBorderPacket` |
| `level_chunk_with_light` | clientbound | `ClientboundLevelChunkWithLightPacket` |
| `level_event` | clientbound | `ClientboundLevelEventPacket` |
| `level_particles` | clientbound | `ClientboundLevelParticlesPacket` |
| `light_update` | clientbound | `ClientboundLightUpdatePacket` |
| `login` | clientbound | `ClientboundLoginPacket` |
| `low_disk_space_warning` | clientbound | `ClientboundLowDiskSpaceWarningPacket` |
| `map_item_data` | clientbound | `ClientboundMapItemDataPacket` |
| `merchant_offers` | clientbound | `ClientboundMerchantOffersPacket` |
| `mount_screen_open` | clientbound | `ClientboundMountScreenOpenPacket` |
| `move_entity_pos` | clientbound | `ClientboundMoveEntityPacket.Pos` |
| `move_entity_pos_rot` | clientbound | `ClientboundMoveEntityPacket.PosRot` |
| `move_entity_rot` | clientbound | `ClientboundMoveEntityPacket.Rot` |
| `move_minecart_along_track` | clientbound | `ClientboundMoveMinecartPacket` |
| `move_vehicle` | clientbound | `ClientboundMoveVehiclePacket` |
| `open_book` | clientbound | `ClientboundOpenBookPacket` |
| `open_screen` | clientbound | `ClientboundOpenScreenPacket` |
| `open_sign_editor` | clientbound | `ClientboundOpenSignEditorPacket` |
| `place_ghost_recipe` | clientbound | `ClientboundPlaceGhostRecipePacket` |
| `player_abilities` | clientbound | `ClientboundPlayerAbilitiesPacket` |
| `player_chat` | clientbound | `ClientboundPlayerChatPacket` |
| `player_combat_end` | clientbound | `ClientboundPlayerCombatEndPacket` |
| `player_combat_enter` | clientbound | `ClientboundPlayerCombatEnterPacket` |
| `player_combat_kill` | clientbound | `ClientboundPlayerCombatKillPacket` |
| `player_info_remove` | clientbound | `ClientboundPlayerInfoRemovePacket` |
| `player_info_update` | clientbound | `ClientboundPlayerInfoUpdatePacket` |
| `player_look_at` | clientbound | `ClientboundPlayerLookAtPacket` |
| `player_position` | clientbound | `ClientboundPlayerPositionPacket` |
| `player_rotation` | clientbound | `ClientboundPlayerRotationPacket` |
| `projectile_power` | clientbound | `ClientboundProjectilePowerPacket` |
| `recipe_book_add` | clientbound | `ClientboundRecipeBookAddPacket` |
| `recipe_book_remove` | clientbound | `ClientboundRecipeBookRemovePacket` |
| `recipe_book_settings` | clientbound | `ClientboundRecipeBookSettingsPacket` |
| `remove_entities` | clientbound | `ClientboundRemoveEntitiesPacket` |
| `remove_mob_effect` | clientbound | `ClientboundRemoveMobEffectPacket` |
| `reset_score` | clientbound | `ClientboundResetScorePacket` |
| `respawn` | clientbound | `ClientboundRespawnPacket` |
| `rotate_head` | clientbound | `ClientboundRotateHeadPacket` |
| `section_blocks_update` | clientbound | `ClientboundSectionBlocksUpdatePacket` |
| `select_advancements_tab` | clientbound | `ClientboundSelectAdvancementsTabPacket` |
| `server_data` | clientbound | `ClientboundServerDataPacket` |
| `set_action_bar_text` | clientbound | `ClientboundSetActionBarTextPacket` |
| `set_border_center` | clientbound | `ClientboundSetBorderCenterPacket` |
| `set_border_lerp_size` | clientbound | `ClientboundSetBorderLerpSizePacket` |
| `set_border_size` | clientbound | `ClientboundSetBorderSizePacket` |
| `set_border_warning_delay` | clientbound | `ClientboundSetBorderWarningDelayPacket` |
| `set_border_warning_distance` | clientbound | `ClientboundSetBorderWarningDistancePacket` |
| `set_camera` | clientbound | `ClientboundSetCameraPacket` |
| `set_chunk_cache_center` | clientbound | `ClientboundSetChunkCacheCenterPacket` |
| `set_chunk_cache_radius` | clientbound | `ClientboundSetChunkCacheRadiusPacket` |
| `set_cursor_item` | clientbound | `ClientboundSetCursorItemPacket` |
| `set_default_spawn_position` | clientbound | `ClientboundSetDefaultSpawnPositionPacket` |
| `set_display_objective` | clientbound | `ClientboundSetDisplayObjectivePacket` |
| `set_entity_data` | clientbound | `ClientboundSetEntityDataPacket` |
| `set_entity_link` | clientbound | `ClientboundSetEntityLinkPacket` |
| `set_entity_motion` | clientbound | `ClientboundSetEntityMotionPacket` |
| `set_equipment` | clientbound | `ClientboundSetEquipmentPacket` |
| `set_experience` | clientbound | `ClientboundSetExperiencePacket` |
| `set_health` | clientbound | `ClientboundSetHealthPacket` |
| `set_held_slot` | clientbound | `ClientboundSetHeldSlotPacket` |
| `set_objective` | clientbound | `ClientboundSetObjectivePacket` |
| `set_passengers` | clientbound | `ClientboundSetPassengersPacket` |
| `set_player_inventory` | clientbound | `ClientboundSetPlayerInventoryPacket` |
| `set_player_team` | clientbound | `ClientboundSetPlayerTeamPacket` |
| `set_score` | clientbound | `ClientboundSetScorePacket` |
| `set_simulation_distance` | clientbound | `ClientboundSetSimulationDistancePacket` |
| `set_subtitle_text` | clientbound | `ClientboundSetSubtitleTextPacket` |
| `set_time` | clientbound | `ClientboundSetTimePacket` |
| `set_title_text` | clientbound | `ClientboundSetTitleTextPacket` |
| `set_titles_animation` | clientbound | `ClientboundSetTitlesAnimationPacket` |
| `sound` | clientbound | `ClientboundSoundPacket` |
| `sound_entity` | clientbound | `ClientboundSoundEntityPacket` |
| `start_configuration` | clientbound | `ClientboundStartConfigurationPacket` |
| `stop_sound` | clientbound | `ClientboundStopSoundPacket` |
| `system_chat` | clientbound | `ClientboundSystemChatPacket` |
| `tab_list` | clientbound | `ClientboundTabListPacket` |
| `tag_query` | clientbound | `ClientboundTagQueryPacket` |
| `take_item_entity` | clientbound | `ClientboundTakeItemEntityPacket` |
| `teleport_entity` | clientbound | `ClientboundTeleportEntityPacket` |
| `test_instance_block_status` | clientbound | `ClientboundTestInstanceBlockStatus` |
| `ticking_state` | clientbound | `ClientboundTickingStatePacket` |
| `ticking_step` | clientbound | `ClientboundTickingStepPacket` |
| `update_advancements` | clientbound | `ClientboundUpdateAdvancementsPacket` |
| `update_attributes` | clientbound | `ClientboundUpdateAttributesPacket` |
| `update_mob_effect` | clientbound | `ClientboundUpdateMobEffectPacket` |
| `update_recipes` | clientbound | `ClientboundUpdateRecipesPacket` |
| `waypoint` | clientbound | `ClientboundTrackedWaypointPacket` |
| `accept_teleportation` | serverbound | `ServerboundAcceptTeleportationPacket` |
| `attack` | serverbound | `ServerboundAttackPacket` |
| `block_entity_tag_query` | serverbound | `ServerboundBlockEntityTagQueryPacket` |
| `bundle_item_selected` | serverbound | `ServerboundSelectBundleItemPacket` |
| `change_difficulty` | serverbound | `ServerboundChangeDifficultyPacket` |
| `change_game_mode` | serverbound | `ServerboundChangeGameModePacket` |
| `chat` | serverbound | `ServerboundChatPacket` |
| `chat_ack` | serverbound | `ServerboundChatAckPacket` |
| `chat_command` | serverbound | `ServerboundChatCommandPacket` |
| `chat_command_signed` | serverbound | `ServerboundChatCommandSignedPacket` |
| `chat_session_update` | serverbound | `ServerboundChatSessionUpdatePacket` |
| `chunk_batch_received` | serverbound | `ServerboundChunkBatchReceivedPacket` |
| `client_command` | serverbound | `ServerboundClientCommandPacket` |
| `client_tick_end` | serverbound | `ServerboundClientTickEndPacket` |
| `command_suggestion` | serverbound | `ServerboundCommandSuggestionPacket` |
| `configuration_acknowledged` | serverbound | `ServerboundConfigurationAcknowledgedPacket` |
| `container_button_click` | serverbound | `ServerboundContainerButtonClickPacket` |
| `container_click` | serverbound | `ServerboundContainerClickPacket` |
| `container_close` | serverbound | `ServerboundContainerClosePacket` |
| `container_slot_state_changed` | serverbound | `ServerboundContainerSlotStateChangedPacket` |
| `debug_subscription_request` | serverbound | `ServerboundDebugSubscriptionRequestPacket` |
| `edit_book` | serverbound | `ServerboundEditBookPacket` |
| `entity_tag_query` | serverbound | `ServerboundEntityTagQueryPacket` |
| `interact` | serverbound | `ServerboundInteractPacket` |
| `jigsaw_generate` | serverbound | `ServerboundJigsawGeneratePacket` |
| `lock_difficulty` | serverbound | `ServerboundLockDifficultyPacket` |
| `move_player_pos` | serverbound | `ServerboundMovePlayerPacket.Pos` |
| `move_player_pos_rot` | serverbound | `ServerboundMovePlayerPacket.PosRot` |
| `move_player_rot` | serverbound | `ServerboundMovePlayerPacket.Rot` |
| `move_player_status_only` | serverbound | `ServerboundMovePlayerPacket.StatusOnly` |
| `move_vehicle` | serverbound | `ServerboundMoveVehiclePacket` |
| `paddle_boat` | serverbound | `ServerboundPaddleBoatPacket` |
| `pick_item_from_block` | serverbound | `ServerboundPickItemFromBlockPacket` |
| `pick_item_from_entity` | serverbound | `ServerboundPickItemFromEntityPacket` |
| `place_recipe` | serverbound | `ServerboundPlaceRecipePacket` |
| `player_abilities` | serverbound | `ServerboundPlayerAbilitiesPacket` |
| `player_action` | serverbound | `ServerboundPlayerActionPacket` |
| `player_command` | serverbound | `ServerboundPlayerCommandPacket` |
| `player_input` | serverbound | `ServerboundPlayerInputPacket` |
| `player_loaded` | serverbound | `ServerboundPlayerLoadedPacket` |
| `recipe_book_change_settings` | serverbound | `ServerboundRecipeBookChangeSettingsPacket` |
| `recipe_book_seen_recipe` | serverbound | `ServerboundRecipeBookSeenRecipePacket` |
| `rename_item` | serverbound | `ServerboundRenameItemPacket` |
| `seen_advancements` | serverbound | `ServerboundSeenAdvancementsPacket` |
| `select_trade` | serverbound | `ServerboundSelectTradePacket` |
| `set_beacon` | serverbound | `ServerboundSetBeaconPacket` |
| `set_carried_item` | serverbound | `ServerboundSetCarriedItemPacket` |
| `set_command_block` | serverbound | `ServerboundSetCommandBlockPacket` |
| `set_command_minecart` | serverbound | `ServerboundSetCommandMinecartPacket` |
| `set_creative_mode_slot` | serverbound | `ServerboundSetCreativeModeSlotPacket` |
| `set_game_rule` | serverbound | `ServerboundSetGameRulePacket` |
| `set_jigsaw_block` | serverbound | `ServerboundSetJigsawBlockPacket` |
| `set_structure_block` | serverbound | `ServerboundSetStructureBlockPacket` |
| `set_test_block` | serverbound | `ServerboundSetTestBlockPacket` |
| `sign_update` | serverbound | `ServerboundSignUpdatePacket` |
| `spectator_action` | serverbound | `ServerboundSpectatorActionPacket` |
| `swing` | serverbound | `ServerboundSwingPacket` |
| `teleport_to_entity` | serverbound | `ServerboundTeleportToEntityPacket` |
| `test_instance_block_action` | serverbound | `ServerboundTestInstanceBlockActionPacket` |
| `use_item` | serverbound | `ServerboundUseItemPacket` |
| `use_item_on` | serverbound | `ServerboundUseItemOnPacket` |

## `handshake` — `HandshakePacketTypes`

| id | direction | class |
|---|---|---|
| `intention` | serverbound | `ClientIntentionPacket` |

## `login` — `LoginPacketTypes`

| id | direction | class |
|---|---|---|
| `custom_query` | clientbound | `ClientboundCustomQueryPacket` |
| `hello` | clientbound | `ClientboundHelloPacket` |
| `login_compression` | clientbound | `ClientboundLoginCompressionPacket` |
| `login_disconnect` | clientbound | `ClientboundLoginDisconnectPacket` |
| `login_finished` | clientbound | `ClientboundLoginFinishedPacket` |
| `custom_query_answer` | serverbound | `ServerboundCustomQueryAnswerPacket` |
| `hello` | serverbound | `ServerboundHelloPacket` |
| `key` | serverbound | `ServerboundKeyPacket` |
| `login_acknowledged` | serverbound | `ServerboundLoginAcknowledgedPacket` |

## `ping` — `PingPacketTypes` — shared across phases

| id | direction | class |
|---|---|---|
| `pong_response` | clientbound | `ClientboundPongResponsePacket` |
| `ping_request` | serverbound | `ServerboundPingRequestPacket` |

## `status` — `StatusPacketTypes`

| id | direction | class |
|---|---|---|
| `status_response` | clientbound | `ClientboundStatusResponsePacket` |
| `status_request` | serverbound | `ServerboundStatusRequestPacket` |

