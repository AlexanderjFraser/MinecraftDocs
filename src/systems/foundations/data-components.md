# Data components

> Verified against **Minecraft 26.2** · Part II · Sharpness III lands on a sword at the enchanting table: what the patch looks like, and how the client finds out.

## Responsibility

A data component is one typed, keyed piece of data attached to an item stack
— its damage, its enchantments, its lore, the food it is, the armour slot it
goes in. The item *type* supplies a **prototype** map of components; a stack
carries only a **patch** against that prototype. Everything that used to be
"the NBT on an item" is a component with a codec, and most of what used to be
a subclass of `Item` carrying behaviour (a sword, a piece of armour) is now a
kit of components on a plain `Item`.

The one sentence a player recognises: *`/give @s diamond_sword[enchantments={sharpness:3}]`
— the part in square brackets is the patch.*

## The data it owns

- `DataComponentType` — the key. Built by `DataComponentType.Builder`:
  `DataComponentType.Builder.persistent` gives the disk/JSON codec,
  `DataComponentType.Builder.networkSynchronized` a hand-written wire codec.
  A type with no persistent codec is **transient** (`DataComponentType.isTransient`):
  never saved, only sent. The 111 vanilla types are registered in
  `DataComponents` into `BuiltInRegistries.DATA_COMPONENT_TYPE`; 29 of them
  have slash-shaped ids (*villager/variant* and its siblings). The catalogue
  is [reference/components](../../reference/components.md).
  `DataComponents.COMMON_ITEM_COMPONENTS` is the ten-entry map every item's
  prototype starts from — notably it puts an *empty* `ItemEnchantments` on
  every item. `DataComponentType.PERSISTENT_CODEC` and
  `DataComponentType.VALUE_MAP_CODEC` are the shared dispatch machinery
  underneath `DataComponentMap.CODEC` and the predicates.
- `DataComponentMap` — an immutable, identity-keyed map;
  `DataComponentMap.Builder` builds one and can carry a
  `DataComponentMap.Builder.addValidator` (see the surprises).
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
  for untrusted input, and `DataComponentPatch.split` is the added/removed
  decomposition that the hashing and block-entity paths are both built on.
- `DataComponentGetter` (read one), `DataComponentHolder` (read one, has a
  map — implemented only by `ItemStack`), `TypedDataComponent` (a type with
  its value, and its own "type id then value" stream codec, distinct from the
  patch encoding). `ItemInstance` is the read-only face over `ItemStack` and
  `ItemStackTemplate` (item, count, patch — a record) that predicates and
  recipes take.
- `DataComponentInitializers` — the deferred prototype builder (see below).
  `Item.Properties.component` and its convenience methods
  (`Item.Properties.durability`, `Item.Properties.food`,
  `Item.Properties.equippable`, `Item.Properties.sword`, …) only *record*
  an initializer; the map is built later.
  `Item.Properties.delayedComponent` and
  `Item.Properties.delayedHolderComponent` are the reason it must be
  deferred: they name registry entries that do not exist until a world's
  registries do.
- `DataComponentLookup` — the other direction. Every frozen `MappedRegistry`
  builds one (`Registry.componentLookup`): a lazily-populated reverse index
  answering "which elements carry this component value?", which is how the
  game finds the spawn egg for an entity type or the item for a dye colour.
- Predicates: `DataComponentExactPredicate` (every listed component must
  equal) and the partial `DataComponentPredicate` family under
  `core/component/predicates` (`DataComponentPredicates`, 15 kinds, in their
  own `BuiltInRegistries.DATA_COMPONENT_PREDICATE_TYPE` registry), joined
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
  are *built* with full registry context — tags, damage types, jukebox songs
  resolvable — by `DataComponentInitializers.build` on the reload worker, and
  *installed* with `Holder.Reference.bindComponents` on the owning thread: on
  the server in `ReloadableServerResources.updateComponentsAndStaticRegistryTags`
  (server thread, after every reload including `/reload`), on the client in
  `RegistryDataCollector` at the end of configuration. Before that, reading a
  registry element's components throws;
  `Item.CODEC_WITH_BOUND_COMPONENTS` guards on `Holder.areComponentsBound`
  and refuses to decode a stack until then.
- **Stack mutation, on whichever thread owns the stack** — the server thread
  for anything in a container or inventory; the client thread for its
  mirror.
- **Container sync, once per server tick.** `AbstractContainerMenu.broadcastChanges`
  runs from `ServerPlayer.tick` and compares every slot against what the
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
    SGPL->>ACM: broadcastChanges — RemoteSlot.Synchronized.matches fails
    ACM->>CPL: ClientboundContainerSetSlotPacket — ItemStack.OPTIONAL_STREAM_CODEC: count, item id, DataComponentPatch.STREAM_CODEC
    CPL->>CPL: decode → new ItemStack(holder, count, patch) → PatchedDataComponentMap.fromPatch against the client's bound prototype
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
   write is skipped. `ItemStack.isEnchantable` gates first on
   `DataComponents.ENCHANTABLE` being present, and *then* on
   `DataComponents.ENCHANTMENTS` being present and empty — which is what
   `DataComponents.COMMON_ITEM_COMPONENTS` exists to guarantee.
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
   that reached the default by different routes compare equal.
5. **Only the patch crosses.** `ItemStack.OPTIONAL_STREAM_CODEC` writes the
   count, `Item.STREAM_CODEC` (a registry id) and the patch; the client
   rebuilds with `PatchedDataComponentMap.fromPatch` against *its own* bound
   prototype. That is the reason components must be bound on the client
   before the play phase — an unbound prototype would throw in a packet
   decoder on a Netty thread.
6. **The client answers with hashes, not stacks.** `ServerboundContainerClickPacket`
   carries a `HashedStack` — item, count and a `HashedPatchMap` of CRC32C
   per component (`HashOps.CRC32C_INSTANCE`). `RemoteSlot.Synchronized`
   keeps **either** the last stack the server sent **or** the last hash the
   client sent — never both, and setting one clears the other — and on a
   hash match it promotes the local copy to a full stack so later comparisons
   are exact. The creative-mode slot is the exception and is guarded twice:
   `DataComponentPatch.DELIMITED_STREAM_CODEC` inside
   `ItemStack.OPTIONAL_UNTRUSTED_STREAM_CODEC`, and
   `ItemStack.validatedStreamCodec`, which re-*encodes* the decoded stack
   through `ItemStack.CODEC` into `NullOps` and keeps only the errors.

## Components on things that are not items

- **Block entities, both directions.** Placing runs
  `BlockEntity.applyComponentsFromItemStack`, which hands subclasses a
  *recording* `DataComponentGetter`: whatever `BlockEntity.applyImplicitComponents`
  reads is forgotten from the patch (`DataComponentPatch.forget`) and only
  the leftovers persist as opaque `BlockEntity.components`. Two types are
  pre-seeded into that forget set regardless of whether anything reads them
  — `DataComponents.BLOCK_ENTITY_DATA` and `DataComponents.BLOCK_STATE` —
  and only the *added* half of the resulting patch is kept, so removals are
  discarded. Breaking or picking runs the reverse,
  `BlockEntity.collectComponents` over `BlockEntity.collectImplicitComponents`,
  with `BlockEntity.removeComponentsFromTag` de-duplicating what was
  promoted; `BlockItem.setBlockEntityData` is the write path for the opaque
  blob.
- **Entities, read-only.** `Entity` implements `DataComponentGetter` with no
  patch of its own: `Entity.get` answers `DataComponents.CUSTOM_NAME` and
  `DataComponents.CUSTOM_DATA` by hand, lets subclass overrides (`Sheep`,
  `Wolf`, `Villager` …) answer the variant-shaped types, and otherwise falls
  through to its `EntityType` holder's bound prototype — the same map every
  registry element gets. `Entity.applyComponentsFromItemStack` is the write
  path, and it is not only spawn eggs: any item-to-entity spawn, an arrow
  picking up its stack, a lingering potion's cloud and `BlockItem` all take
  it.

## Interfaces

- **Called by:** every item behaviour, through the read methods `ItemStack`
  inherits from `DataComponentHolder` (`DataComponentHolder.get`,
  `DataComponentHolder.getOrDefault`, `DataComponentHolder.has`) and the
  writes it declares itself (`ItemStack.set`, `ItemStack.update`,
  `ItemStack.remove`, `ItemStack.copyFrom`); loot functions
  (`CopyComponentsFunction`), commands (`/give`, `/item`), recipes and
  predicates through `ItemInstance`.
- **Calls into:** the registry for prototypes (`Holder.Reference.components`,
  [identifiers-and-registries](identifiers-and-registries.md)); codecs for
  every value ([codecs-nbt-json](codecs-nbt-json.md)); `EncoderCache`
  (`DataComponents.ENCODER_CACHE`) for types built with
  `DataComponentType.Builder.cacheEncoding`.
- **Crosses the network as:** the patch inside every `ItemStack` in
  `ClientboundContainerSetSlotPacket`, `ClientboundContainerSetContentPacket`,
  `ClientboundSetCursorItemPacket`, `ClientboundSetPlayerInventoryPacket`,
  `ClientboundSetEquipmentPacket`; hashes in `ServerboundContainerClickPacket`;
  a full validated stack in `ServerboundSetCreativeModeSlotPacket`; and a
  whole typed component through `TypedDataComponent` where one value travels
  alone.
- **Saved as:** a *patch* for an item (`ItemStack.MAP_CODEC`'s "components",
  with transient types silently dropped), but a full `DataComponentMap` for a
  block entity — the two are not symmetric.
- **Data-driven by:** nothing directly — component *types* are code, in a
  registry data packs cannot extend — but prototypes resolve data-pack
  registries at bind time (an item's `DataComponents.JUKEBOX_PLAYABLE` or
  `DataComponents.DAMAGE_RESISTANT` names an entry a data pack can change),
  and `CustomData` carries arbitrary NBT for data packs to use.

## Invariants and surprises

- **Prototypes bind at reload, not in constructors.** `Item.Properties`
  accumulates a `DataComponentInitializers.Initializer`; nothing is a map
  until `DataComponentInitializers.build` runs with registries in hand, and
  a `/reload` rebinds every item's prototype. Every registry element gets a
  component map (`DataComponentMap.EMPTY` if it had no initializer), so
  `EntityType` holders have one too — though on a **multiplayer** client the
  binding is applied only for networkable registries, so a client's
  non-networkable elements stay unbound.
- **The failure before binding is a null-check, not a friendly error.**
  `Item.components` merely delegates; the throw comes from
  `Holder.Reference.components`, and the non-throwing question is
  `Holder.areComponentsBound`.
- **`DataComponentType.Builder.networkSynchronized` is not a gate.** Without it, `DataComponentType.Builder.build`
  derives a wire codec from the persistent codec (NBT over the wire); with
  neither it throws. The only real switch is transient-vs-persistent, and it
  gates *saving*. Three types exist only on the wire:
  `DataComponents.CREATIVE_SLOT_LOCK`, `DataComponents.ADDITIONAL_TRADE_COST`,
  `DataComponents.MAP_POST_PROCESSING`.
- **There are two structural rules, at two different times.** At
  *prototype-build* time a validator installed by `Item.Properties` rejects
  an item that is both damageable and stackable. At *stack* time
  `ItemStack.validateStrict` rejects a `DataComponents.MAX_DAMAGE` alongside
  a `DataComponents.MAX_STACK_SIZE` above one, a count above the stack's own
  maximum, an over-weight bundle, and contained items whose counts exceed
  their own limits. That last check reaches exactly **one** level into
  containers, bundles and charged projectiles and does not re-run the full
  validation there — nesting is not followed.
- **`Item` subclasses no longer carry combat.** `Weapon`, `BlocksAttacks`,
  `KineticWeapon`, `PiercingWeapon`, `AttackRange`, `SwingAnimation` and
  `Tool` are components; `Item.Properties.sword`, `Item.Properties.spear`
  and `Item.Properties.humanoidArmor` build whole kits, and *SwordItem* is
  gone. But the tools that act *on a block* are not: `AxeItem`, `ShovelItem`
  and `HoeItem` still exist as classes, purely for stripping, path-making
  and tilling — their combat and mining live in components like everything
  else.
- **The wire patch never contains defaults — for a real stack.**
  `PatchedDataComponentMap` sanitises on every write, so a value equal to the
  prototype's is dropped rather than sent. `ItemStackTemplate` is the
  exception: it holds a raw `DataComponentPatch` straight from the builder,
  which does no such comparison, and sends it verbatim.
- **`DataComponents.DAMAGE` alone is built with `DataComponentType.Builder.ignoreSwapAnimation`** —
  so durability ticking down does not replay the held-item swap on the
  client.
- **`DataComponentMap.composite` is dead API.** It exists, and nothing in
  26.2 calls it; the layering that actually happens is
  `PatchedDataComponentMap`'s prototype-plus-patch.

## Where to look

`DataComponentType` · `DataComponents` · `DataComponentMap` ·
`PatchedDataComponentMap` · `DataComponentPatch` · `DataComponentInitializers` ·
`DataComponentLookup` · `Item.Properties` · `ItemStack` · `ItemInstance` ·
`ItemStackTemplate` · `EnchantmentHelper` · `ItemEnchantments` ·
`EnchantmentMenu` · `AbstractContainerMenu` · `RemoteSlot` · `HashedStack` ·
`HashOps` · `BlockEntity` · `Entity` (the getter half)

---

*Rules: names, never code · how the system works, not how the code reads ·
newest version only · every backticked name passes `tools/verify_names.py`.*
