# The weapon helpers on `Item.Properties`

> Generated from the **26.2** decompile by `tools/gen_reference.py`. Do not edit by hand.

The seven `Item.Properties` methods that turn a bare item into something you can hit with, what each one installs, and every item built by one. `Item.Properties.tool` is the shared body: `pickaxe`, `axe`, `hoe` and `shovel` are it with a mining tag and a shield-disable time filled in; `sword` and `spear` go their own way. Three of the six tool families need a class of their own because they also do something on right-click, and three are plain `Item`s the helper alone describes. See [items and stacks](../systems/items/items-and-stacks.md) and [data components](../systems/foundations/data-components.md).

| helper | delegates to | components it sets | attributes |
|---|---|---|---|
| `Item.Properties.tool` | `applyToolProperties` | `DataComponents.TOOL`, `DataComponents.WEAPON` | `Attributes.ATTACK_DAMAGE`, `Attributes.ATTACK_SPEED` (through `ToolMaterial`) |
| `Item.Properties.pickaxe` | `tool` | `DataComponents.TOOL`, `DataComponents.WEAPON` | `Attributes.ATTACK_DAMAGE`, `Attributes.ATTACK_SPEED` (through `ToolMaterial`) |
| `Item.Properties.axe` | `tool` | `DataComponents.TOOL`, `DataComponents.WEAPON` | `Attributes.ATTACK_DAMAGE`, `Attributes.ATTACK_SPEED` (through `ToolMaterial`) |
| `Item.Properties.hoe` | `tool` | `DataComponents.TOOL`, `DataComponents.WEAPON` | `Attributes.ATTACK_DAMAGE`, `Attributes.ATTACK_SPEED` (through `ToolMaterial`) |
| `Item.Properties.shovel` | `tool` | `DataComponents.TOOL`, `DataComponents.WEAPON` | `Attributes.ATTACK_DAMAGE`, `Attributes.ATTACK_SPEED` (through `ToolMaterial`) |
| `Item.Properties.sword` | `applySwordProperties` | `DataComponents.TOOL`, `DataComponents.WEAPON` | `Attributes.ATTACK_DAMAGE`, `Attributes.ATTACK_SPEED` (through `ToolMaterial`) |
| `Item.Properties.spear` | — | `DataComponents.DAMAGE_TYPE`, `DataComponents.KINETIC_WEAPON`, `DataComponents.PIERCING_WEAPON`, `DataComponents.ATTACK_RANGE`, `DataComponents.MINIMUM_ATTACK_CHARGE`, `DataComponents.SWING_ANIMATION`, `DataComponents.USE_EFFECTS`, `DataComponents.WEAPON` | `Attributes.ATTACK_DAMAGE`, `Attributes.ATTACK_SPEED` |

## The 42 items built by one

*damage* and *speed* are the two baselines the call passes; the material adds its own attack-damage bonus on top.

| item | helper | material | damage baseline | speed baseline |
|---|---|---|---:|---:|
| `Items.WOODEN_SWORD` | `Item.Properties.sword` | `ToolMaterial.WOOD` | 3.0 | -2.4 |
| `Items.WOODEN_SHOVEL` | shovel (`ShovelItem`) | `ToolMaterial.WOOD` | 1.5 | -3.0 |
| `Items.WOODEN_PICKAXE` | `Item.Properties.pickaxe` | `ToolMaterial.WOOD` | 1.0 | -2.8 |
| `Items.WOODEN_AXE` | axe (`AxeItem`) | `ToolMaterial.WOOD` | 6.0 | -3.2 |
| `Items.WOODEN_HOE` | hoe (`HoeItem`) | `ToolMaterial.WOOD` | 0.0 | -3.0 |
| `Items.COPPER_SWORD` | `Item.Properties.sword` | `ToolMaterial.COPPER` | 3.0 | -2.4 |
| `Items.COPPER_SHOVEL` | shovel (`ShovelItem`) | `ToolMaterial.COPPER` | 1.5 | -3.0 |
| `Items.COPPER_PICKAXE` | `Item.Properties.pickaxe` | `ToolMaterial.COPPER` | 1.0 | -2.8 |
| `Items.COPPER_AXE` | axe (`AxeItem`) | `ToolMaterial.COPPER` | 7.0 | -3.2 |
| `Items.COPPER_HOE` | hoe (`HoeItem`) | `ToolMaterial.COPPER` | -1.0 | -2.0 |
| `Items.STONE_SWORD` | `Item.Properties.sword` | `ToolMaterial.STONE` | 3.0 | -2.4 |
| `Items.STONE_SHOVEL` | shovel (`ShovelItem`) | `ToolMaterial.STONE` | 1.5 | -3.0 |
| `Items.STONE_PICKAXE` | `Item.Properties.pickaxe` | `ToolMaterial.STONE` | 1.0 | -2.8 |
| `Items.STONE_AXE` | axe (`AxeItem`) | `ToolMaterial.STONE` | 7.0 | -3.2 |
| `Items.STONE_HOE` | hoe (`HoeItem`) | `ToolMaterial.STONE` | -1.0 | -2.0 |
| `Items.GOLDEN_SWORD` | `Item.Properties.sword` | `ToolMaterial.GOLD` | 3.0 | -2.4 |
| `Items.GOLDEN_SHOVEL` | shovel (`ShovelItem`) | `ToolMaterial.GOLD` | 1.5 | -3.0 |
| `Items.GOLDEN_PICKAXE` | `Item.Properties.pickaxe` | `ToolMaterial.GOLD` | 1.0 | -2.8 |
| `Items.GOLDEN_AXE` | axe (`AxeItem`) | `ToolMaterial.GOLD` | 6.0 | -3.0 |
| `Items.GOLDEN_HOE` | hoe (`HoeItem`) | `ToolMaterial.GOLD` | 0.0 | -3.0 |
| `Items.IRON_SWORD` | `Item.Properties.sword` | `ToolMaterial.IRON` | 3.0 | -2.4 |
| `Items.IRON_SHOVEL` | shovel (`ShovelItem`) | `ToolMaterial.IRON` | 1.5 | -3.0 |
| `Items.IRON_PICKAXE` | `Item.Properties.pickaxe` | `ToolMaterial.IRON` | 1.0 | -2.8 |
| `Items.IRON_AXE` | axe (`AxeItem`) | `ToolMaterial.IRON` | 6.0 | -3.1 |
| `Items.IRON_HOE` | hoe (`HoeItem`) | `ToolMaterial.IRON` | -2.0 | -1.0 |
| `Items.DIAMOND_SWORD` | `Item.Properties.sword` | `ToolMaterial.DIAMOND` | 3.0 | -2.4 |
| `Items.DIAMOND_SHOVEL` | shovel (`ShovelItem`) | `ToolMaterial.DIAMOND` | 1.5 | -3.0 |
| `Items.DIAMOND_PICKAXE` | `Item.Properties.pickaxe` | `ToolMaterial.DIAMOND` | 1.0 | -2.8 |
| `Items.DIAMOND_AXE` | axe (`AxeItem`) | `ToolMaterial.DIAMOND` | 5.0 | -3.0 |
| `Items.DIAMOND_HOE` | hoe (`HoeItem`) | `ToolMaterial.DIAMOND` | -3.0 | 0.0 |
| `Items.NETHERITE_SWORD` | `Item.Properties.sword` | `ToolMaterial.NETHERITE` | 3.0 | -2.4 |
| `Items.NETHERITE_SHOVEL` | shovel (`ShovelItem`) | `ToolMaterial.NETHERITE` | 1.5 | -3.0 |
| `Items.NETHERITE_PICKAXE` | `Item.Properties.pickaxe` | `ToolMaterial.NETHERITE` | 1.0 | -2.8 |
| `Items.NETHERITE_AXE` | axe (`AxeItem`) | `ToolMaterial.NETHERITE` | 5.0 | -3.0 |
| `Items.NETHERITE_HOE` | hoe (`HoeItem`) | `ToolMaterial.NETHERITE` | -4.0 | 0.0 |
| `Items.WOODEN_SPEAR` | `Item.Properties.spear` | `ToolMaterial.WOOD` | 0.65 | 0.7 |
| `Items.STONE_SPEAR` | `Item.Properties.spear` | `ToolMaterial.STONE` | 0.75 | 0.82 |
| `Items.COPPER_SPEAR` | `Item.Properties.spear` | `ToolMaterial.COPPER` | 0.85 | 0.82 |
| `Items.IRON_SPEAR` | `Item.Properties.spear` | `ToolMaterial.IRON` | 0.95 | 0.95 |
| `Items.GOLDEN_SPEAR` | `Item.Properties.spear` | `ToolMaterial.GOLD` | 0.95 | 0.7 |
| `Items.DIAMOND_SPEAR` | `Item.Properties.spear` | `ToolMaterial.DIAMOND` | 1.05 | 1.075 |
| `Items.NETHERITE_SPEAR` | `Item.Properties.spear` | `ToolMaterial.NETHERITE` | 1.15 | 1.2 |
