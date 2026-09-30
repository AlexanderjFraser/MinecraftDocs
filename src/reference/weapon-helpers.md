# The weapon helpers on `Item.Properties`

> Generated from the **26.3** decompile by `tools/gen_reference.py`. Do not edit by hand.

The seven `Item.Properties` methods that turn a bare item into something you can hit with, what each one installs, and every item built by one. The *components* column names what a helper sets by name; through `Item.Properties.durability`, `Item.Properties.repairable`, `Item.Properties.enchantable` and `Item.Properties.attributes` every one also sets the durability components and a stack size of one, and the repair, enchantability and attribute-modifier components. `Item.Properties.tool` is the shared body: `pickaxe`, `axe`, `hoe` and `shovel` are it with a mining tag and a shield-disable time filled in; `sword` and `spear` go their own way. None of the six needs a class of its own: `axe`, `hoe` and `shovel` add `DataComponents.BLOCK_TRANSFORMER`, which the base `Item.useOn` runs on a right-click, so every item a helper builds is a plain `Item`. See [items and stacks](../systems/items/items-and-stacks.md) and [data components](../systems/foundations/data-components.md).

| helper | delegates to | components it sets | attributes |
|---|---|---|---|
| `Item.Properties.tool` | `applyToolProperties` | `DataComponents.TOOL`, `DataComponents.WEAPON` | `Attributes.ATTACK_DAMAGE`, `Attributes.ATTACK_SPEED` (through `ToolMaterial`) |
| `Item.Properties.pickaxe` | `tool` | `DataComponents.TOOL`, `DataComponents.WEAPON` | `Attributes.ATTACK_DAMAGE`, `Attributes.ATTACK_SPEED` (through `ToolMaterial`) |
| `Item.Properties.axe` | `tool` | `DataComponents.BLOCK_TRANSFORMER`, `DataComponents.TOOL`, `DataComponents.WEAPON` | `Attributes.ATTACK_DAMAGE`, `Attributes.ATTACK_SPEED` (through `ToolMaterial`) |
| `Item.Properties.hoe` | `tool` | `DataComponents.BLOCK_TRANSFORMER`, `DataComponents.TOOL`, `DataComponents.WEAPON` | `Attributes.ATTACK_DAMAGE`, `Attributes.ATTACK_SPEED` (through `ToolMaterial`) |
| `Item.Properties.shovel` | `tool` | `DataComponents.BLOCK_TRANSFORMER`, `DataComponents.TOOL`, `DataComponents.WEAPON` | `Attributes.ATTACK_DAMAGE`, `Attributes.ATTACK_SPEED` (through `ToolMaterial`) |
| `Item.Properties.sword` | `applySwordProperties` | `DataComponents.TOOL`, `DataComponents.WEAPON` | `Attributes.ATTACK_DAMAGE`, `Attributes.ATTACK_SPEED` (through `ToolMaterial`) |
| `Item.Properties.spear` | — | `DataComponents.DAMAGE_TYPE`, `DataComponents.KINETIC_WEAPON`, `DataComponents.PIERCING_WEAPON`, `DataComponents.ATTACK_RANGE`, `DataComponents.MINIMUM_ATTACK_CHARGE`, `DataComponents.ATTACK_ANIMATION`, `DataComponents.USE_EFFECTS`, `DataComponents.WEAPON` | `Attributes.ATTACK_DAMAGE`, `Attributes.ATTACK_SPEED` |

## The 42 items built by one

*damage* and *speed* are the two baselines a tool or sword call passes; the material adds its own attack-damage bonus on top. A spear's call passes an attack duration and a damage multiplier instead, so its row leaves both cells empty.

| item | helper | material | damage baseline | speed baseline |
|---|---|---|---:|---:|
| `Items.WOODEN_SWORD` | `Item.Properties.sword` | `ToolMaterial.WOOD` | 3.0 | -2.4 |
| `Items.WOODEN_SHOVEL` | `Item.Properties.shovel` | `ToolMaterial.WOOD` | 1.5 | -3.0 |
| `Items.WOODEN_PICKAXE` | `Item.Properties.pickaxe` | `ToolMaterial.WOOD` | 1.0 | -2.8 |
| `Items.WOODEN_AXE` | `Item.Properties.axe` | `ToolMaterial.WOOD` | 6.0 | -3.2 |
| `Items.WOODEN_HOE` | `Item.Properties.hoe` | `ToolMaterial.WOOD` | 0.0 | -3.0 |
| `Items.COPPER_SWORD` | `Item.Properties.sword` | `ToolMaterial.COPPER` | 3.0 | -2.4 |
| `Items.COPPER_SHOVEL` | `Item.Properties.shovel` | `ToolMaterial.COPPER` | 1.5 | -3.0 |
| `Items.COPPER_PICKAXE` | `Item.Properties.pickaxe` | `ToolMaterial.COPPER` | 1.0 | -2.8 |
| `Items.COPPER_AXE` | `Item.Properties.axe` | `ToolMaterial.COPPER` | 7.0 | -3.2 |
| `Items.COPPER_HOE` | `Item.Properties.hoe` | `ToolMaterial.COPPER` | -1.0 | -2.0 |
| `Items.STONE_SWORD` | `Item.Properties.sword` | `ToolMaterial.STONE` | 3.0 | -2.4 |
| `Items.STONE_SHOVEL` | `Item.Properties.shovel` | `ToolMaterial.STONE` | 1.5 | -3.0 |
| `Items.STONE_PICKAXE` | `Item.Properties.pickaxe` | `ToolMaterial.STONE` | 1.0 | -2.8 |
| `Items.STONE_AXE` | `Item.Properties.axe` | `ToolMaterial.STONE` | 7.0 | -3.2 |
| `Items.STONE_HOE` | `Item.Properties.hoe` | `ToolMaterial.STONE` | -1.0 | -2.0 |
| `Items.GOLDEN_SWORD` | `Item.Properties.sword` | `ToolMaterial.GOLD` | 3.0 | -2.4 |
| `Items.GOLDEN_SHOVEL` | `Item.Properties.shovel` | `ToolMaterial.GOLD` | 1.5 | -3.0 |
| `Items.GOLDEN_PICKAXE` | `Item.Properties.pickaxe` | `ToolMaterial.GOLD` | 1.0 | -2.8 |
| `Items.GOLDEN_AXE` | `Item.Properties.axe` | `ToolMaterial.GOLD` | 6.0 | -3.0 |
| `Items.GOLDEN_HOE` | `Item.Properties.hoe` | `ToolMaterial.GOLD` | 0.0 | -3.0 |
| `Items.IRON_SWORD` | `Item.Properties.sword` | `ToolMaterial.IRON` | 3.0 | -2.4 |
| `Items.IRON_SHOVEL` | `Item.Properties.shovel` | `ToolMaterial.IRON` | 1.5 | -3.0 |
| `Items.IRON_PICKAXE` | `Item.Properties.pickaxe` | `ToolMaterial.IRON` | 1.0 | -2.8 |
| `Items.IRON_AXE` | `Item.Properties.axe` | `ToolMaterial.IRON` | 6.0 | -3.1 |
| `Items.IRON_HOE` | `Item.Properties.hoe` | `ToolMaterial.IRON` | -2.0 | -1.0 |
| `Items.DIAMOND_SWORD` | `Item.Properties.sword` | `ToolMaterial.DIAMOND` | 3.0 | -2.4 |
| `Items.DIAMOND_SHOVEL` | `Item.Properties.shovel` | `ToolMaterial.DIAMOND` | 1.5 | -3.0 |
| `Items.DIAMOND_PICKAXE` | `Item.Properties.pickaxe` | `ToolMaterial.DIAMOND` | 1.0 | -2.8 |
| `Items.DIAMOND_AXE` | `Item.Properties.axe` | `ToolMaterial.DIAMOND` | 5.0 | -3.0 |
| `Items.DIAMOND_HOE` | `Item.Properties.hoe` | `ToolMaterial.DIAMOND` | -3.0 | 0.0 |
| `Items.NETHERITE_SWORD` | `Item.Properties.sword` | `ToolMaterial.NETHERITE` | 3.0 | -2.4 |
| `Items.NETHERITE_SHOVEL` | `Item.Properties.shovel` | `ToolMaterial.NETHERITE` | 1.5 | -3.0 |
| `Items.NETHERITE_PICKAXE` | `Item.Properties.pickaxe` | `ToolMaterial.NETHERITE` | 1.0 | -2.8 |
| `Items.NETHERITE_AXE` | `Item.Properties.axe` | `ToolMaterial.NETHERITE` | 5.0 | -3.0 |
| `Items.NETHERITE_HOE` | `Item.Properties.hoe` | `ToolMaterial.NETHERITE` | -4.0 | 0.0 |
| `Items.WOODEN_SPEAR` | `Item.Properties.spear` | `ToolMaterial.WOOD` | — | — |
| `Items.STONE_SPEAR` | `Item.Properties.spear` | `ToolMaterial.STONE` | — | — |
| `Items.COPPER_SPEAR` | `Item.Properties.spear` | `ToolMaterial.COPPER` | — | — |
| `Items.IRON_SPEAR` | `Item.Properties.spear` | `ToolMaterial.IRON` | — | — |
| `Items.GOLDEN_SPEAR` | `Item.Properties.spear` | `ToolMaterial.GOLD` | — | — |
| `Items.DIAMOND_SPEAR` | `Item.Properties.spear` | `ToolMaterial.DIAMOND` | — | — |
| `Items.NETHERITE_SPEAR` | `Item.Properties.spear` | `ToolMaterial.NETHERITE` | — | — |
