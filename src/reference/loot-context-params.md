# Loot context parameter sets

> Generated from the **26.3** decompile by `tools/gen_reference.py`. Do not edit by hand.

Every `ContextKeySet` registered in `LootContextParamSets`, with the keys its `ContextKeySet.Builder` declared. The set a roll is checked against belongs to the **caller**: `ContextMap.Builder.buildAndValidate` throws both on a required key that is absent and on a key the set does not declare at all, so this table is the contract each call site has to satisfy. A loot table names a set of its own, its *type*, but that one is checked only when the table loads. A loot element reads a key with `LootContext.getOptional`, which answers null for a key that is not there, or asks only whether it is there, with `LootContext.hasParameter`. Seventeen of these thirty-one sets never roll a `LootTable` at all — the engine is wider than the loot package. See [Contexts and predicates](../systems/items/contexts-and-predicates.md).

31 parameter sets

| set | id | required | optional |
|---|---|---|---|
| `LootContextParamSets.ADVANCEMENT_ENTITY` | *advancement_entity* | `LootContextParams.THIS_ENTITY`, `LootContextParams.ORIGIN` | — |
| `LootContextParamSets.ADVANCEMENT_LOCATION` | *advancement_location* | `LootContextParams.THIS_ENTITY`, `LootContextParams.ORIGIN`, `LootContextParams.TOOL`, `LootContextParams.BLOCK_STATE` | `LootContextParams.BLOCK_ENTITY` |
| `LootContextParamSets.ADVANCEMENT_REWARD` | *advancement_reward* | `LootContextParams.THIS_ENTITY`, `LootContextParams.ORIGIN` | — |
| `LootContextParamSets.ARCHAEOLOGY` | *archaeology* | `LootContextParams.ORIGIN`, `LootContextParams.THIS_ENTITY`, `LootContextParams.TOOL` | — |
| `LootContextParamSets.PIGLIN_BARTER` | *barter* | `LootContextParams.THIS_ENTITY` | — |
| `LootContextParamSets.BLOCK` | *block* | `LootContextParams.BLOCK_STATE`, `LootContextParams.ORIGIN`, `LootContextParams.TOOL` | `LootContextParams.THIS_ENTITY`, `LootContextParams.BLOCK_ENTITY`, `LootContextParams.EXPLOSION_RADIUS` |
| `LootContextParamSets.BLOCK_INTERACT` | *block_interact* | `LootContextParams.BLOCK_STATE`, `LootContextParams.ORIGIN` | `LootContextParams.BLOCK_ENTITY`, `LootContextParams.INTERACTING_ENTITY`, `LootContextParams.TOOL` |
| `LootContextParamSets.BLOCK_USE` | *block_use* | `LootContextParams.THIS_ENTITY`, `LootContextParams.ORIGIN`, `LootContextParams.BLOCK_STATE` | — |
| `LootContextParamSets.CHEST` | *chest* | `LootContextParams.ORIGIN` | `LootContextParams.THIS_ENTITY` |
| `LootContextParamSets.COMMAND` | *command* | `LootContextParams.ORIGIN` | `LootContextParams.THIS_ENTITY` |
| `LootContextParamSets.COMMAND_COMPUTE_DEFAULT` | *command_compute_default* | `LootContextParams.ORIGIN` | `LootContextParams.THIS_ENTITY` |
| `LootContextParamSets.COMMAND_COMPUTE_ENTITY` | *command_compute_entity* | `LootContextParams.ORIGIN`, `LootContextParams.TARGET_ENTITY` | `LootContextParams.THIS_ENTITY` |
| `LootContextParamSets.COMMAND_COMPUTE_POSITION` | *command_compute_position* | `LootContextParams.ORIGIN`, `LootContextParams.BLOCK_STATE` | `LootContextParams.THIS_ENTITY`, `LootContextParams.BLOCK_ENTITY` |
| `LootContextParamSets.COMMAND_SLOT_SOURCE` | *command_slot_source* | `LootContextParams.ORIGIN`, `LootContextParams.CONTAINER` | `LootContextParams.THIS_ENTITY` |
| `LootContextParamSets.CONTAINER_PROCESS` | *container_process* | `LootContextParams.BLOCK_ENTITY`, `LootContextParams.BLOCK_STATE`, `LootContextParams.CONTAINER`, `LootContextParams.ORIGIN` | — |
| `LootContextParamSets.EMPTY` | *empty* | — | — |
| `LootContextParamSets.ENCHANTED_DAMAGE` | *enchanted_damage* | `LootContextParams.THIS_ENTITY`, `LootContextParams.ENCHANTMENT_LEVEL`, `LootContextParams.ORIGIN`, `LootContextParams.DAMAGE_SOURCE` | `LootContextParams.DIRECT_ATTACKING_ENTITY`, `LootContextParams.ATTACKING_ENTITY` |
| `LootContextParamSets.ENCHANTED_ENTITY` | *enchanted_entity* | `LootContextParams.THIS_ENTITY`, `LootContextParams.ENCHANTMENT_LEVEL`, `LootContextParams.ORIGIN` | — |
| `LootContextParamSets.ENCHANTED_ITEM` | *enchanted_item* | `LootContextParams.TOOL`, `LootContextParams.ENCHANTMENT_LEVEL` | — |
| `LootContextParamSets.ENCHANTED_LOCATION` | *enchanted_location* | `LootContextParams.THIS_ENTITY`, `LootContextParams.ENCHANTMENT_LEVEL`, `LootContextParams.ORIGIN`, `LootContextParams.ENCHANTMENT_ACTIVE` | — |
| `LootContextParamSets.ENTITY` | *entity* | `LootContextParams.THIS_ENTITY`, `LootContextParams.ORIGIN`, `LootContextParams.DAMAGE_SOURCE` | `LootContextParams.ATTACKING_ENTITY`, `LootContextParams.DIRECT_ATTACKING_ENTITY`, `LootContextParams.LAST_DAMAGE_PLAYER` |
| `LootContextParamSets.ENTITY_INTERACT` | *entity_interact* | `LootContextParams.TARGET_ENTITY`, `LootContextParams.TOOL` | `LootContextParams.INTERACTING_ENTITY` |
| `LootContextParamSets.EQUIPMENT` | *equipment* | `LootContextParams.ORIGIN`, `LootContextParams.THIS_ENTITY` | — |
| `LootContextParamSets.FISHING` | *fishing* | `LootContextParams.ORIGIN`, `LootContextParams.TOOL` | `LootContextParams.THIS_ENTITY` |
| `LootContextParamSets.ALL_PARAMS` | *generic* | `LootContextParams.THIS_ENTITY`, `LootContextParams.LAST_DAMAGE_PLAYER`, `LootContextParams.DAMAGE_SOURCE`, `LootContextParams.ATTACKING_ENTITY`, `LootContextParams.DIRECT_ATTACKING_ENTITY`, `LootContextParams.ORIGIN`, `LootContextParams.BLOCK_STATE`, `LootContextParams.BLOCK_ENTITY`, `LootContextParams.TOOL`, `LootContextParams.EXPLOSION_RADIUS`, `LootContextParams.ADDITIONAL_COST_COMPONENT_ALLOWED`, `LootContextParams.CONTAINER`, `LootContextParams.INTERACTING_ENTITY`, `LootContextParams.TARGET_ENTITY`, `LootContextParams.ENCHANTMENT_ACTIVE`, `LootContextParams.ENCHANTMENT_LEVEL` | — |
| `LootContextParamSets.GIFT` | *gift* | `LootContextParams.ORIGIN`, `LootContextParams.THIS_ENTITY` | — |
| `LootContextParamSets.HIT_BLOCK` | *hit_block* | `LootContextParams.THIS_ENTITY`, `LootContextParams.ENCHANTMENT_LEVEL`, `LootContextParams.ORIGIN`, `LootContextParams.BLOCK_STATE` | — |
| `LootContextParamSets.SELECTOR` | *selector* | `LootContextParams.ORIGIN`, `LootContextParams.THIS_ENTITY` | — |
| `LootContextParamSets.SHEARING` | *shearing* | `LootContextParams.ORIGIN`, `LootContextParams.THIS_ENTITY`, `LootContextParams.TOOL` | — |
| `LootContextParamSets.VAULT` | *vault* | `LootContextParams.ORIGIN` | `LootContextParams.THIS_ENTITY`, `LootContextParams.TOOL` |
| `LootContextParamSets.VILLAGER_TRADE` | *villager_trade* | `LootContextParams.ORIGIN`, `LootContextParams.THIS_ENTITY`, `LootContextParams.ADDITIONAL_COST_COMPONENT_ALLOWED` | — |
