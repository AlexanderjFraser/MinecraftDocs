# Attributes

> Generated from the **26.2** decompile by `tools/gen_reference.py`. Do not edit by hand.

Every attribute registered in `Attributes`. All of them are `RangedAttribute`s, so every one clamps to its range once, at the end of `AttributeInstance.calculateValue`. **Syncable** attributes are the only ones `ClientboundUpdateAttributesPacket` ever carries: a mutation to one of the others changes the server's number and never reaches the client at all. The sentiment decides tooltip colour and nothing else. Defaults here are the registry's, and most entity types override them in their own `AttributeSupplier`. See [Attributes](../systems/entities/attributes.md).

40 attributes, 32 syncable and 8 not

| id | constant | default | min | max | syncable | sentiment |
|---|---|---:|---:|---:|---|---|
| `air_drag_modifier` | `Attributes.AIR_DRAG_MODIFIER` | 1 | 0 | 2048 | yes | positive |
| `armor` | `Attributes.ARMOR` | 0 | 0 | 30 | yes | positive |
| `armor_toughness` | `Attributes.ARMOR_TOUGHNESS` | 0 | 0 | 20 | yes | positive |
| `attack_damage` | `Attributes.ATTACK_DAMAGE` | 2 | 0 | 2048 |  | positive |
| `attack_knockback` | `Attributes.ATTACK_KNOCKBACK` | 0 | 0 | 5 |  | positive |
| `attack_speed` | `Attributes.ATTACK_SPEED` | 4 | 0 | 1024 | yes | positive |
| `below_name_distance` | `Attributes.BELOW_NAME_DISTANCE` | 10 | 0 | 512 | yes | positive |
| `block_break_speed` | `Attributes.BLOCK_BREAK_SPEED` | 1 | 0 | 1024 | yes | positive |
| `block_interaction_range` | `Attributes.BLOCK_INTERACTION_RANGE` | 4.5 | 0 | 64 | yes | positive |
| `bounciness` | `Attributes.BOUNCINESS` | 0 | 0 | 1 | yes | positive |
| `burning_time` | `Attributes.BURNING_TIME` | 1 | 0 | 1024 | yes | negative |
| `camera_distance` | `Attributes.CAMERA_DISTANCE` | 4 | 0 | 32 | yes | positive |
| `entity_interaction_range` | `Attributes.ENTITY_INTERACTION_RANGE` | 3 | 0 | 64 | yes | positive |
| `explosion_knockback_resistance` | `Attributes.EXPLOSION_KNOCKBACK_RESISTANCE` | 0 | 0 | 1 | yes | positive |
| `fall_damage_multiplier` | `Attributes.FALL_DAMAGE_MULTIPLIER` | 1 | 0 | 100 | yes | negative |
| `flying_speed` | `Attributes.FLYING_SPEED` | 0.4 | 0 | 1024 | yes | positive |
| `follow_range` | `Attributes.FOLLOW_RANGE` | 32 | 0 | 2048 |  | positive |
| `friction_modifier` | `Attributes.FRICTION_MODIFIER` | 1 | 0 | 2048 | yes | positive |
| `gravity` | `Attributes.GRAVITY` | 0.08 | -1 | 1 | yes | neutral |
| `jump_strength` | `Attributes.JUMP_STRENGTH` | 0.42 | 0 | 32 | yes | positive |
| `knockback_resistance` | `Attributes.KNOCKBACK_RESISTANCE` | 0 | -2 | 1 |  | positive |
| `luck` | `Attributes.LUCK` | 0 | -1024 | 1024 | yes | positive |
| `max_absorption` | `Attributes.MAX_ABSORPTION` | 0 | 0 | 2048 | yes | positive |
| `max_health` | `Attributes.MAX_HEALTH` | 20 | 1 | 1024 | yes | positive |
| `mining_efficiency` | `Attributes.MINING_EFFICIENCY` | 0 | 0 | 1024 | yes | positive |
| `movement_efficiency` | `Attributes.MOVEMENT_EFFICIENCY` | 0 | 0 | 1 | yes | positive |
| `movement_speed` | `Attributes.MOVEMENT_SPEED` | 0.7 | 0 | 1024 | yes | positive |
| `name_tag_distance` | `Attributes.NAME_TAG_DISTANCE` | 64 | 0 | 512 | yes | positive |
| `oxygen_bonus` | `Attributes.OXYGEN_BONUS` | 0 | 0 | 1024 | yes | positive |
| `safe_fall_distance` | `Attributes.SAFE_FALL_DISTANCE` | 3 | -1024 | 1024 | yes | positive |
| `scale` | `Attributes.SCALE` | 1 | 0.0625 | 16 | yes | neutral |
| `sneaking_speed` | `Attributes.SNEAKING_SPEED` | 0.3 | 0 | 1 | yes | positive |
| `spawn_reinforcements` | `Attributes.SPAWN_REINFORCEMENTS_CHANCE` | 0 | 0 | 1 |  | positive |
| `step_height` | `Attributes.STEP_HEIGHT` | 0.6 | 0 | 10 | yes | positive |
| `submerged_mining_speed` | `Attributes.SUBMERGED_MINING_SPEED` | 0.2 | 0 | 20 | yes | positive |
| `sweeping_damage_ratio` | `Attributes.SWEEPING_DAMAGE_RATIO` | 0 | 0 | 1 | yes | positive |
| `tempt_range` | `Attributes.TEMPT_RANGE` | 10 | 0 | 2048 |  | positive |
| `water_movement_efficiency` | `Attributes.WATER_MOVEMENT_EFFICIENCY` | 0 | 0 | 1 | yes | positive |
| `waypoint_receive_range` | `Attributes.WAYPOINT_RECEIVE_RANGE` | 0 | 0 | 60000000 |  | neutral |
| `waypoint_transmit_range` | `Attributes.WAYPOINT_TRANSMIT_RANGE` | 0 | 0 | 60000000 |  | neutral |
