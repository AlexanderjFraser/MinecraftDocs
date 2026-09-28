# Items and stacks

> Verified against **Minecraft 26.3** · Part VII · A diamond pickaxe sits in a hotbar slot, is compared against its neighbours, is sent to a client, and finally loses its last point of durability.

A diamond pickaxe is in your hotbar. The `Item` behind it,
`Items.DIAMOND_PICKAXE`, is a single object shared by every diamond pickaxe
that has ever existed on this server, and it holds four fields: a description
id, a crafting remainder, a feature-flag set, and its own registry holder —
`Item.descriptionId`, `Item.craftingRemainingItem`, a `FeatureFlagSet` in
`Item.requiredFeatures`, and `Item.builtInRegistryHolder`. Not
the stack size. Not the mining speed. Not the durability. All of that is data
components — and they do not live on the `Item` either. They live on the
item's `Holder.Reference` in `BuiltInRegistries.ITEM`, as a prototype map
built at the first data-pack load and rebuilt at every one after ([data
components](../foundations/data-components.md#the-prototype-and-why-it-is-built-at-reload)),
and the *stack* borrows that map read-only and stores only the ways it
differs from it. This page is the object in the slot rather than the
component system behind it: what an `ItemStack` is made of, what makes two of
them the same stack, what a stack may legally hold, and what happens to one
that runs out of durability. That last is the odd one out in a part where
almost everything is predicted locally and corrected afterwards.
**A client never even guesses at the durability an item spends** — the method that spends it demands a `ServerLevel` outright, and the convenient overloads
that take a `LivingEntity` instead look its level up and silently do nothing
when the answer is a client's.

## The cast

| class | what it decides | thread |
|---|---|---|
| `Item` | the behaviour hooks, and four fields that are not components | both |
| `Item.Properties` | the builder — which produces an *initializer*, never a component map | class-init, wherever the bootstrap runs |
| `Holder.Reference` | where an item's default components live, and whether they exist yet | written by the thread loading the world, on the Server thread at each `/reload`, and on the Render thread for a joining client |
| `DataComponentInitializers` | the pile of pending default maps, one entry per registered item | built on the worker pool on the server, on the Render thread on a joining client |
| `ItemStack` | a holder, a count, a pop time and a patched map — the mutable thing in a slot | both |
| `PatchedDataComponentMap` | prototype plus patch, and the copy-on-write flag that makes copying a stack cheap | wherever its stack is |
| `ItemStackTemplate` | the immutable stack: what a stack looks like inside a component, a particle or a recipe | both |
| `ItemEntity` | a stack that is an entity, with a five-minute clock and a merge rule | Server, mirrored on the Render thread |

## Four fields, and only one of them is really data

`ItemStack` is a final class holding exactly four things: two ints, a registry
holder, and the interesting one.

```mermaid
classDiagram
    class ItemStack {
        int count
        int popTime
        Holder~Item~ item
        PatchedDataComponentMap components
    }
    class Item {
        String descriptionId
        ItemStackTemplate craftingRemainingItem
        FeatureFlagSet requiredFeatures
        Holder.Reference builtInRegistryHolder
    }
    class Reference["Holder.Reference, in BuiltInRegistries.ITEM"] {
        the Item
        the item's default DataComponentMap
    }
    class PatchedDataComponentMap {
        the prototype, borrowed
        the patch, owned
    }
    ItemStack *-- PatchedDataComponentMap : the only mutable half
    ItemStack --> Reference : every stack of this item, the one holder
    Reference --> Item
    PatchedDataComponentMap ..> Reference : reads the defaults, never writes them
```

*`ItemStack`'s four fields and `Item`'s four, and the arrows between the classes. The dotted one is the shape of the
whole system — a stack reads defaults it can never touch.*

A stack does not own its defaults and cannot change them: it points at a
holder, and the holder owns one `DataComponentMap` shared by every stack of that item in both
programs (a reload rebinds it, and a stack made before keeps the map it was made
with). What the patch is made of, and why copying a stack is cheap, belong to [data
components](../foundations/data-components.md#the-prototype-and-why-it-is-built-at-reload).

The holder field the figure calls *item* is read through
`ItemStack.typeHolder`, and it answers `Items.AIR`'s holder rather than null
for an empty stack, which is why `ItemStack.getItem` never returns null
either. The
pop time — `ItemStack.popTime` — is the odd one out: it is the five-tick
squeeze the hotbar icon does
when something lands in it, set to 5 by `Inventory` when a stack grows or a damaged item lands in an empty
slot, and by
`ClientPacketListener.handleContainerSetSlot` when a slot update makes a
hotbar stack larger, counted down by `ItemStack.inventoryTick` on **both**
sides, and read by `Hud.extractSlot`, which scales the icon while it is above
zero and hands the drawing to `GuiGraphicsExtractor` either way. It is
ordinary shared state that only the client has any use for — and
`ItemStack.copy` carries it across, so the animation survives being copied
into a menu slot.

`Item.Properties` is the builder used at class-init, and its output is not a
component map. `Item.Properties.component` and every convenience over it —
`Item.Properties.stacksTo`, `Item.Properties.durability`,
`Item.Properties.food`, `Item.Properties.tool`, `Item.Properties.spear`,
`Item.Properties.equippable`, `Item.Properties.useCooldown` — fold one more
step onto a `DataComponentInitializers.Initializer`, a function that will be
run against a `DataComponentMap.Builder` later, with a
`HolderLookup.Provider` in hand. The ones that make a weapon are a different seven — `Item.Properties.tool`,
`Item.Properties.spear` and five named for what they make — and between them they
build forty-two items out of a registry of over a thousand
([the weapon helpers](../../reference/weapon-helpers.md)).

Between the two halves of that arrangement an `Item` is a live object with no
components at all: the constructor registers an initializer and the map is not
built until a reload builds it, so `Item.components` throws until then and
`Item.CODEC_WITH_BOUND_COMPONENTS` exists to refuse an item whose components
are not bound yet. When and on which thread that happens, on the server and on
a joining client alike, is [data
components](../foundations/data-components.md#the-prototype-and-why-it-is-built-at-reload).

## What copying a stack costs, and what crosses the wire

Two properties of that borrowed map do work on the rest of this page, and
both belong to [data components](../foundations/data-components.md#the-maps).
The patch is **sanitised on every write**, so it can never hold a value the
item already had — which is what makes the equality table below behave. And
the patch map is **shared until someone writes to it**: `ItemStack.copy` hands
out the same map and sets a copy-on-write flag, and the fork happens on the
first mutation. Copying a stack is therefore something the game does without
thinking about it, and it does — menus, recipes and `ServerPlayerGameMode.destroyBlock` all copy constantly, and
each copy allocates two small objects and no component data.

The wire form falls out of the same shape and is the second of the four serialisations [codecs, NBT and
JSON](../foundations/codecs-nbt-json.md#the-four-paths-side-by-side) lays side
by side: `ItemStack.OPTIONAL_STREAM_CODEC` writes the count, the item holder
and the patch, never the prototype, because the receiver has the same
prototype bound to the same holder. A count of zero is the whole encoding of
an empty stack.

## When two stacks are the same stack

Five static methods on `ItemStack` answer five different versions of that
question, and menus, recipes and the first-person hand each want a different
one.

| method | compares | used for |
|---|---|---|
| `ItemStack.isSameItem` | the item holder only | *is this the same kind of thing* |
| `ItemStack.isSameItemSameComponents` | the item, then the whole `PatchedDataComponentMap` | stacking, and every *are these interchangeable* test |
| `ItemStack.matches` | the count as well | container synchronisation ([containers and menus](containers-and-menus.md#the-ladder-the-server-climbs-before-it-believes-you)) |
| `ItemStack.matchesIgnoringComponents` | everything except the component types a predicate excuses | the held-item swap animation |
| `ItemStack.hashItemAndComponents` | the item's hash and the effective component map's | keying stacks in hash sets |

The second row is where the borrowed map pays off. Comparing two stacks of the
same item amounts to comparing their patches, and because a patch never holds
a value equal to the prototype's, two pickaxes with the same damage are equal
whether one reached that state by being set explicitly or by never being
touched.

The fourth row exists for one component. `DataComponents.DAMAGE` is the only
component type in the game declared with
`DataComponentType.Builder.ignoreSwapAnimation`, and
`FirstPersonHandsAndItems.shouldInstantlyReplaceVisibleItem` passes exactly
that flag as the predicate — which is why a pickaxe losing a point of
durability does not re-play the lower-and-raise animation. And a trap sits
under all five rows: `ItemStack.EMPTY` is a singleton but is not identified
by reference, because `ItemStack.isEmpty` also answers true for `Items.AIR`
and for any count at or below zero.

## Two validators, one rule, two spellings

Durability and stackability are mutually exclusive, and the game says so
twice — in different places, at different times, against different
components.

| | the reload validator | `ItemStack.validateStrict` |
|---|---|---|
| installed by | `Item.Properties.finalizeInitializer` | — |
| rejects | `DataComponents.DAMAGE` on a stackable item | `DataComponents.MAX_DAMAGE` on a stackable item, and a count over the maximum |
| runs inside | `DataComponentMap.Builder.build` | `ItemInput`, `ItemStack.applyComponentsAndValidate`, and `ItemStackTemplate.create` and `ItemStackTemplate.apply` through one private step they share |
| when | at reload, on the worker pool (a joining client's on the Render thread) | when a command, a template or a component patch builds a stack |
| on failure | throws, failing the reload | depends on the caller: `ItemInput` throws a command syntax error, the other two log and yield `ItemStack.EMPTY` or restore the previous patch |

Neither is reached from a network decode. Exactly **one** serverbound packet
in the protocol carries an `ItemStack` at all, the creative slot's, and it is
proved a third way — re-encoded rather than validated ([codecs, NBT and
JSON](../foundations/codecs-nbt-json.md#trusted-untrusted-and-validated)).

The strict validator reaches one level into a stack's contents and no further.
`ItemStack.validateContainedItemSizes` runs inside `ItemStack.validateStrict`
over `DataComponents.CONTAINER`, `DataComponents.BUNDLE_CONTENTS` and
`DataComponents.CHARGED_PROJECTILES`, checking each contained stack's count
against its own maximum — and it does **not** re-run the full validation there, so nesting is not followed;
a shulker box full of impossible stacks is caught by a command, and not at the
creative slot's door, which never runs the strict validator at all. The bundle is the one that gets a second test of its own: a `BundleContents` whose
weight cannot be computed fails too, though one merely over its capacity passes.

## An item, a count, some components — said three ways

`ItemInstance` is the read-only contract the contents check is written against: `ItemInstance.count`, `ItemInstance.getMaxStackSize`, and — through
`TypedInstance` and `DataComponentGetter` — five `TypedInstance.is` overloads
for tags, holder sets, raw items, holders and resource keys, to which
`ItemStack.is` adds a sixth taking a predicate. Its default
`ItemInstance.getMaxStackSize` answers **1** when
`DataComponents.MAX_STACK_SIZE` is missing — which for a bound item never
happens, because the common set puts 64 there.

Two classes implement it. `ItemStack` is the mutable one that lives in slots.
`ItemStackTemplate` is an immutable record of a `Holder<Item>`, a count and a **raw** `DataComponentPatch` — one the template itself never sanitises against a
prototype, so a template read from data can carry a component value equal to the
item's own default, which no `ItemStack` can. It is what a stack becomes when it is stored *inside* something
else: `ItemContainerContents` (so a shulker box's contents are
templates, not stacks), `BundleContents`, `ChargedProjectiles`,
`ItemParticleOption`, `HoverEvent`, `UseRemainder`, the recipe classes, and
`Item`'s own crafting remainder. Its constructor refuses a count of zero or
`Items.AIR`, so there is no empty template; but
`ItemStackTemplate.create` and `ItemStackTemplate.apply`, which materialise a
real stack, run `ItemStack.validateStrict` on the result and answer
`ItemStack.EMPTY` with a log line rather than throwing.

## A pickaxe's last point of durability

Durability is not one component: `ItemStack.isDamageableItem` demands
`DataComponents.MAX_DAMAGE` present, `DataComponents.UNBREAKABLE` absent, and
`DataComponents.DAMAGE` present. Take a diamond pickaxe one block short of
breaking, and mine that block.

`ServerPlayerGameMode.destroyBlock` copies the held stack *before* touching it
— that copy is what `Block.playerDestroy` later hands the loot table, so the
drops are decided by the tool as it was — then calls `ItemStack.mineBlock`,
which delegates to `Item.mineBlock` and awards `Stats.ITEM_USED` if the item
claims the block. The base `Item.mineBlock` is pure component work: it reads
`DataComponents.TOOL`, does nothing without one, and damages the stack by
`Tool.damagePerBlock` only on a server level, only when that number is above
zero, and only when the block's destroy speed is not zero — so instant-break
plants cost a tool nothing, and neither does a tool that declares no per-block
damage.

`ItemStack.hurtAndBreak` is the way in for almost everything, and the overload
that does the work demands a `ServerLevel` outright. The overloads taking a `LivingEntity`
pattern-match on the entity's level and **silently do nothing** on the client,
which is why a client never predicts the durability an item spends. The amount then goes through
`EnchantmentHelper.processDurabilityChange`
([enchantments](enchantments.md#seven-families-of-moment)), which is how Unbreaking turns a point of
damage into no damage at all, and a player with `Player.hasInfiniteMaterials`
short-circuits to zero before even that. If anything survives, the stack fires
`CriteriaTriggers.ITEM_DURABILITY_CHANGED` for a real player, writes the new
`DataComponents.DAMAGE`, and — this being the last point — finds
`ItemStack.isBroken` true, **shrinks itself by one**, and calls the break hook
it was handed. For equipment that hook is `LivingEntity.onEquippedItemBroken`,
which strips the item's attribute modifiers and broadcasts an entity event
(47 for the main hand); `ServerPlayer.onEquippedItemBroken` adds
`Stats.ITEM_BROKEN` on top.

### What the client is told, and what it draws

The client is told in one byte. `LivingEntity.handleEntityEvent` turns event
47 into `LivingEntity.breakItem`, which plays `DataComponents.BREAK_SOUND`
from the stack still in that slot and spawns five item particles; the empty
slot itself arrives separately, as a container update. Two siblings round the
family out: `ItemStack.hurtWithoutBreaking` clamps one short of the maximum,
and `ItemStack.hurtAndConvertOnBreak` transmutes rather than vanishing.

What the player watched was three methods on `Item`.
`Item.isBarVisible` is *is this stack damaged*, `Item.getBarWidth` scales the
damage over the thirteen pixels `Item.MAX_BAR_WIDTH` names, and
`Item.getBarColor`
sweeps a hue from green to red. `GuiGraphicsExtractor` draws the two-pixel bar
under the icon from those three answers and nothing else.

All three read the client's own copy of the stack, and the client never wrote
to it. So the bar does not creep as you mine: it sits at whatever the last
slot update said, and jumps when the next one arrives. The one point of
durability you just spent is invisible until the server sends the slot back.

## The tick a stack gets, and the stack that is an entity

`ItemStack.inventoryTick` runs on both sides and does exactly one thing there:
decrement the pop time. It forwards to `Item.inventoryTick` only for a
`ServerLevel` — the hook's parameter is declared as one, so it cannot be
otherwise — and exactly two items override that hook, `CompassItem` and
`MapItem`. It has two callers: `Inventory.tick`, from `Player.aiStep`, walks
the thirty-six ordinary slots and tells the selected one it is the main hand;
`EntityEquipment.tick`, from `LivingEntity.aiStep`, walks the worn and held
slots of every living entity. A stack that leaves an inventory altogether
becomes an `ItemEntity`, which keeps it in a synched data entry
([synched entity data](../entities/synched-entity-data.md#nineteen-slots-and-where-the-numbers-come-from)) rather than a
plain field, counts up to a 6000-tick lifetime, and folds itself into
neighbours through `ItemEntity.mergeWithNeighbours` — a merge that keeps the
*smaller* of the two ages, so a fresh drop rejuvenates an old one. Blocks
reach it through `Block.popResource`
([block breaking](../blocks/block-breaking.md#remove-damage-roll-drop)).

## The seventy-nine classes, and why sixty-seven of them are almost empty

`world/item`'s own directory holds seventy-nine classes beside its records,
enums and interfaces. Two of them are `Item` and `ItemStack` and ten are
helpers such as `Items` and `ItemCooldowns`; the other sixty-seven are one `Item` subclass each, and all but two exist for the
same reason — a behaviour hook that no component can express (`BannerItem` adds
only an accessor, and `ProjectileWeaponItem` is the bow's and the crossbow's
shared base). `BoneMealItem`, `HoneycombItem`,
`EnderEyeItem`, `DebugStickItem`, `LeadItem` and thirty-four more override
`Item.use`, `Item.useOn` or `Item.interactLivingEntity` and hold no state of
their own. Axes, shovels and hoes are plain `Item`s: stripping, path-making
and tilling are one component, `DataComponents.BLOCK_TRANSFORMER`, that the
base `Item.useOn` reads and runs. That is why a registry of over a thousand
items has so few classes behind it ([the class
hierarchy](../../maps/hierarchy.md)).

## What this page hands off

Everything a stack *does* when a player holds down the use key — the
prediction, the countdown, the consumable and cooldown components, the
completion packet — is the next lecture: [using an item](using-an-item.md#the-two-paths-side-by-side).
How two machines agree about a set of stacks in a screen is
[containers and menus](containers-and-menus.md#one-shift-click-end-to-end); the
component system itself is [data
components](../foundations/data-components.md#the-key-datacomponenttype), catalogued in the
[components reference](../../reference/components.md). And how an item picks
the model, texture and tint you see in the slot is **not** this part's subject
at all: it is Part XI's, in [models and atlases](../rendering/models-and-atlases.md#how-an-item-picks-its-model).

> **For a 1.21-era reader.** *AxeItem*, *ShovelItem* and *HoeItem* are gone:
> `DataComponents.BLOCK_TRANSFORMER` does their work, naming a
> `BlockTransformer` from a data registry. *ItemInHandRenderer* is gone too;
> `FirstPersonHandsAndItems` decides the swap animation.

## Where to look

Open `ItemStack` first and read its four fields; everything else on this page
is a consequence of them. `PatchedDataComponentMap` beside it is where the
copy-on-write flag and the sanitising live, and it is the shortest way to see
why two pickaxes with the same damage are equal.

Then `Item` and `Item.Properties`, in that order, for the gap between a live
item and its components: the builder's output is a
`DataComponentInitializers.Initializer`, and where it eventually lands is
`Holder.Reference` in `BuiltInRegistries.ITEM`. `Items` is the roll call of
what was built.

For the durability trace, `ServerPlayerGameMode.destroyBlock` is the entry
point and `ItemStack.hurtAndBreak` is where it ends up. For the immutable
twin, `ItemStackTemplate`; for the contract both stacks answer,
`ItemInstance`. `ItemEntity` is the stack that left the inventory, and
`Inventory.tick` and `EntityEquipment.tick` are the two walks that tick the
stacks that did not.

---

*Rules: names, never code · how the system works, not how the code reads ·
newest version only · every backticked name passes `tools/verify_names.py`.*
