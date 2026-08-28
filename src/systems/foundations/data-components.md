# Data components

> Verified against **Minecraft 26.2** · Part II · Sharpness III lands on a sword at the enchanting table: what the patch looks like, and how the client finds out.

## Responsibility

A data component is one typed, keyed piece of data attached to an item stack
— its damage, its enchantments, its lore, the food it is, the armour slot it
goes in. The item *type* supplies a **prototype** map of components; a stack
carries only a **patch** against that prototype. Everything that used to be
"the NBT on an item" is a component with a codec, and everything that used to
be a subclass of `Item` carrying behaviour (a sword, an axe, a piece of
armour) is now a kit of components on a plain `Item`.

The one sentence a player recognises: *`/give @s diamond_sword[enchantments={sharpness:3}]`
— the part in square brackets is the patch.*

## The data it owns

- `DataComponentType` — the key. Built by `DataComponentType.Builder`:
  `DataComponentType.Builder.persistent` gives the disk/JSON codec,
  `DataComponentType.Builder.networkSynchronized` a hand-written wire codec.
  A type with no persistent codec is **transient** (`DataComponentType.isTransient`):
  never saved, only sent. The 111 vanilla types are registered in
  `DataComponents` into `BuiltInRegistries.DATA_COMPONENT_TYPE`; the
  catalogue is [reference/components](../../reference/components.md).
  `DataComponents.COMMON_ITEM_COMPONENTS` is the ten-entry map every item's
  prototype starts from — notably it puts an *empty* `ItemEnchantments` on
  every item.
- `DataComponentMap` — an immutable, identity-keyed map; `DataComponentMap.Builder`
  builds one, `DataComponentMap.composite` layers two as a view.
- `PatchedDataComponentMap` — the map an `ItemStack` actually owns:
  a `PatchedDataComponentMap.prototype` (shared with every stack of that
  item), a `PatchedDataComponentMap.patch` whose values are `Optional`
  (empty = *removed from the prototype*), and a `PatchedDataComponentMap.copyOnWrite`
  flag. `PatchedDataComponentMap.set` stores nothing when the value equals
  the prototype's; `PatchedDataComponentMap.remove` stores a removal marker
  only if the prototype had the key.
- `DataComponentPatch` — the serialisable form of the patch: additions and
  removals, `DataComponentPatch.CODEC` writes removals as `!minecraft:foo`,
  `DataComponentPatch.STREAM_CODEC` writes two counts then the entries.
  `DataComponentPatch.DELIMITED_STREAM_CODEC` is the length-prefixed variant
  for untrusted input.
- `DataComponentGetter` (read one), `DataComponentHolder` (read one, has a
  map — implemented only by `ItemStack`), `TypedDataComponent` (a type with
  its value). `ItemInstance` is the new read-only face over `ItemStack` and
  `ItemStackTemplate` (item, count, patch — a record) that predicates and
  recipes take.
- `DataComponentInitializers` — the deferred prototype builder (see below).
  `Item.Properties.component` and its convenience methods
  (`Item.Properties.durability`, `Item.Properties.food`,
  `Item.Properties.equippable`, `Item.Properties.sword`, …) only *record*
  an initializer; the map is built later.
- Predicates: `DataComponentExactPredicate` (every listed component must
  equal) and the partial `DataComponentPredicate` family under
  `core/component/predicates` (`DataComponentPredicates`, 15 kinds), joined
  by `DataComponentMatchers` for `ItemPredicate`.
- Value types live in `world/item/component` (`Consumable`, `Tool`, `Weapon`,
  `BlocksAttacks`, `ItemLore`, `CustomData`, `TooltipDisplay`,
  `ItemContainerContents`, `BundleContents`, `TypedEntityData` …) and
  neighbours (`Equippable` in `world/item/equipment`; `ItemEnchantments`,
  `Enchantable`, `Repairable` in `world/item/enchantment`).

Everything here ships in both jars; only `ClientPacketListener` and
`RegistryDataCollector` in the trace are client-only.

## When it runs

- **Prototype binding, on reload.** An `Item` constructor registers its
  initializer in `BuiltInRegistries.DATA_COMPONENT_INITIALIZERS`. The maps
  are built with full registry context — tags, damage types, jukebox songs
  resolvable — by `DataComponentInitializers.build` and installed with
  `Holder.Reference.bindComponents`: on the server in
  `ReloadableServerResources.updateComponentsAndStaticRegistryTags` (server
  thread, after every reload including `/reload`), on the client in
  `RegistryDataCollector` at the end of configuration. `Item.components`
  throws before that, and `Item.CODEC_WITH_BOUND_COMPONENTS` refuses to
  decode a stack until then.
- **Stack mutation, on whichever thread owns the stack** — the server thread
  for anything in a container or inventory; the client thread for its
  mirror.
- **Container sync, once per server tick.** `AbstractContainerMenu.broadcastChanges`
  runs from `ServerPlayer.doTick` and compares every slot against what the
  client was last told (`RemoteSlot.Synchronized`).

## The trace: Sharpness is applied at the enchanting table

```mermaid
sequenceDiagram
    participant SGPL as ServerGamePacketListenerImpl (server thread)
    participant EM as EnchantmentMenu
    participant IS as ItemStack
    participant EH as EnchantmentHelper
    participant PDM as PatchedDataComponentMap
    participant ACM as AbstractContainerMenu
    participant CPL as ClientPacketListener (client thread)

    SGPL->>EM: handleContainerButtonClick → clickMenuButton(player, 2) — ServerboundContainerButtonClickPacket
    EM->>IS: (if a book) transmuteCopy(Items.ENCHANTED_BOOK) — same patch, new prototype
    EM->>IS: enchant(holder, level) for each EnchantmentInstance
    IS->>EH: updateEnchantments(stack, mutable → upgrade)
    EH->>IS: set(DataComponents.ENCHANTMENTS, ItemEnchantments)
    IS->>PDM: set — ensureMapOwnership clones the shared map; value ≠ prototype's EMPTY, so patch.put
    Note over PDM: patch is now {minecraft:enchantments ⇒ {sharpness: 3}}
    SGPL->>ACM: broadcastChanges — RemoteSlot.Synchronized.matches fails (isSameItemSameComponents)
    ACM->>CPL: ClientboundContainerSetSlotPacket — ItemStack.OPTIONAL_STREAM_CODEC: count, item id, DataComponentPatch.STREAM_CODEC
    CPL->>CPL: decode → new ItemStack(holder, count, patch) → PatchedDataComponentMap.fromPatch against the client's Item.components
    CPL->>CPL: handleContainerSetSlot → AbstractContainerMenu.setItem; tooltip via ItemEnchantments.addToTooltip
```

Narrated:

1. **The menu owns the mutation.** `EnchantmentMenu.clickMenuButton` runs
   under `ContainerLevelAccess.execute` on the server thread; for a book it
   first calls `ItemStack.transmuteCopy` — a new stack with the *same patch*
   applied to the enchanted book's prototype — then `ItemStack.enchant` per
   chosen `EnchantmentInstance`, consumes lapis and fires
   `CriteriaTriggers.ENCHANTED_ITEM`. `/enchant` (`EnchantCommand`) is the
   same tail after `Enchantment.canEnchant` and a compatibility check.
2. **Enchantments are a value, not a list on the stack.**
   `EnchantmentHelper.updateEnchantments` reads the current
   `ItemEnchantments` (choosing `DataComponents.STORED_ENCHANTMENTS` for an
   enchanted book), edits an `ItemEnchantments.Mutable`, and writes the
   immutable result back with `ItemStack.set`. If the prototype lacks the
   component entirely the read returns `ItemEnchantments.EMPTY` and the
   write is skipped — which is why `ItemStack.isEnchantable` requires
   `DataComponents.ENCHANTMENTS` to be present *and* empty, and why
   `DataComponents.COMMON_ITEM_COMPONENTS` puts it on everything.
3. **The first write pays for the copy.** `PatchedDataComponentMap.ensureMapOwnership`
   clones the backing map only when `PatchedDataComponentMap.copyOnWrite` is set; `ItemStack.copy`,
   `PatchedDataComponentMap.asPatch` and `ItemStack.transmuteCopy` all alias the same
   map and set the flag, so copying a stack is O(1) until someone writes.
   `ItemStack.applyComponentsAndValidate` relies on that: it snapshots with
   `PatchedDataComponentMap.asPatch`, applies, runs `ItemStack.validateStrict`, and on failure
   `PatchedDataComponentMap.restorePatch`.
4. **Equality is prototype plus patch.** `ItemStack.isSameItemSameComponents`
   bottoms out in `PatchedDataComponentMap.equals`. Because setting a value
   equal to the prototype default *removes* it from the patch, two stacks
   that reached the default by different routes compare equal, and the wire
   patch never contains defaults.
5. **Only the patch crosses.** `ItemStack.OPTIONAL_STREAM_CODEC` writes the
   count, `Item.STREAM_CODEC` (a registry id) and the patch; the client
   rebuilds with `PatchedDataComponentMap.fromPatch` against *its own* bound
   prototype. That is the reason components must be bound on the client
   before the play phase — an unbound `Item.components` would throw in a
   packet decoder on a Netty thread.
6. **The client answers with hashes, not stacks.** `ServerboundContainerClickPacket`
   carries a `HashedStack` — item, count and a `HashedPatchMap` of CRC32C
   per component (`HashOps.CRC32C_INSTANCE`). `RemoteSlot.Synchronized`
   keeps the last stack *and* its hash so the server can tell whether the
   client's view drifted without the client ever sending component data. The
   creative-mode slot packet is the exception and is guarded twice:
   `DataComponentPatch.DELIMITED_STREAM_CODEC` and
   `ItemStack.validatedStreamCodec`, which round-trips the decoded stack
   through `ItemStack.CODEC` before accepting it.

## Interfaces

- **Called by:** every item behaviour — `ItemStack.get`, `ItemStack.getOrDefault`,
  `ItemStack.has`, `ItemStack.set`, `ItemStack.update`, `ItemStack.remove`;
  loot functions (`CopyComponentsFunction`), commands (`/give`, `/item`),
  recipes and predicates through `ItemInstance`.
- **Calls into:** the registry for prototypes (`Holder.Reference.components`,
  [identifiers-and-registries](identifiers-and-registries.md)); codecs for
  every value ([codecs-nbt-json](codecs-nbt-json.md)); `EncoderCache`
  (`DataComponents.ENCODER_CACHE`) for types built with
  `DataComponentType.Builder.cacheEncoding`.
- **Crosses the network as:** the patch inside every `ItemStack` in
  `ClientboundContainerSetSlotPacket`, `ClientboundContainerSetContentPacket`,
  `ClientboundSetCursorItemPacket`, `ClientboundSetPlayerInventoryPacket`,
  `ClientboundSetEquipmentPacket`; hashes in `ServerboundContainerClickPacket`;
  a full validated stack in `ServerboundSetCreativeModeSlotPacket`.
- **Data-driven by:** nothing directly — component *types* are code — but
  prototypes resolve data-pack registries at bind time (an item's
  `DataComponents.JUKEBOX_PLAYABLE` or `DataComponents.DAMAGE_RESISTANT`
  names an entry a data pack can change), and `CustomData` carries arbitrary
  NBT for data packs to use.

## Invariants and surprises

- **Prototypes bind at reload, not in constructors.** `Item.Properties`
  accumulates a `DataComponentInitializers.Initializer`; nothing is a map
  until `DataComponentInitializers.build` runs with registries in hand. A
  `/reload` rebinds every item's prototype. Every registry element gets a
  component map (`DataComponentMap.EMPTY` if it had no initializer), so
  `EntityType` holders have one too.
- **`DataComponentType.Builder.networkSynchronized` is not a gate.** Without it, `DataComponentType.Builder.build`
  derives a wire codec from the persistent codec (NBT over the wire); with
  neither it throws. The only real switch is transient-vs-persistent, and it
  gates *saving*. Three types exist only on the wire:
  `DataComponents.CREATIVE_SLOT_LOCK`, `DataComponents.ADDITIONAL_TRADE_COST`,
  `DataComponents.MAP_POST_PROCESSING`.
- **The component registry is shared by items, block entities and entities.**
  `BlockEntity.applyComponentsFromItemStack` hands subclasses a *recording*
  `DataComponentGetter`: whatever `BlockEntity.applyImplicitComponents`
  reads is forgotten from the patch (`DataComponentPatch.forget`) and only
  the leftovers persist as opaque `BlockEntity.components` — implicit vs
  stored is decided by observation, not a declared list.
  `Entity` implements `DataComponentGetter` with no map at all:
  `Entity.get` answers `DataComponents.CUSTOM_NAME` and
  `DataComponents.CUSTOM_DATA` by hand, and the 33 `<mob>/variant`-style
  types are answered by subclass overrides (`Sheep`, `Wolf`, `Villager` …)
  with `Entity.applyImplicitComponent` as the spawn-egg write path.
- **`Item` subclasses no longer carry combat.** `Weapon`, `BlocksAttacks`,
  `KineticWeapon`, `PiercingWeapon`, `AttackRange`, `SwingAnimation` and
  `Tool` are components; `Item.Properties.sword`, `Item.Properties.spear`
  and `Item.Properties.humanoidArmor` build whole kits. *SwordItem* and
  *AxeItem* as behaviour carriers are gone.
- **`ItemStack.validateStrict` is the one structural rule**: no
  `DataComponents.MAX_DAMAGE` alongside a `DataComponents.MAX_STACK_SIZE`
  above one, recursively into containers, bundles and charged projectiles.
- **`DataComponents.DAMAGE` alone is built with `DataComponentType.Builder.ignoreSwapAnimation`** —
  so durability ticking down does not replay the held-item swap on the
  client.

## Where to look

`DataComponentType` · `DataComponents` · `DataComponentMap` ·
`PatchedDataComponentMap` · `DataComponentPatch` · `DataComponentInitializers` ·
`Item.Properties` · `ItemStack` · `ItemInstance` · `EnchantmentHelper` ·
`ItemEnchantments` · `EnchantmentMenu` · `AbstractContainerMenu` ·
`RemoteSlot` · `HashedStack` · `BlockEntity` · `Entity` (the getter half)

---

*Rules: names, never code · how the system works, not how the code reads ·
newest version only · every backticked name passes `tools/verify_names.py`.*
