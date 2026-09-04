# Data components

> Verified against **Minecraft 26.2** · Part II · A player types `/give @s diamond_sword[enchantments={sharpness:3}]`, and later rolls Sharpness onto a plain sword at the enchanting table: what the square brackets are, and how the client finds out.

A player types `/give @s diamond_sword[enchantments={sharpness:3}]`. The
part in square brackets is a **patch**: one keyed, typed value laid over
the sword. A data component is exactly that — one typed, keyed piece of
data attached to an item stack: its damage, its enchantments, its lore, the
food it is, the armour slot it goes in. The item *type* supplies a
**prototype** map of components; a stack carries only a patch against that
prototype. Everything that used to be "the NBT on an item" is a component
with a codec, and most of what used to be a subclass of `Item` carrying
behaviour (a sword, a piece of armour) is now a kit of components on a
plain `Item`. The surprise is where the prototype comes from. It is not
built in the item's constructor: `Item.Properties` only *records* an
initializer, and the map is built again on every reload with the world's
registries in hand — `DataComponentInitializers.build` on the reload
worker, `Holder.Reference.bindComponents` on the owning thread. That is
why a data pack can change what a jukebox plays without touching the item,
and why a stack cannot even be decoded before the first reload:
`Item.CODEC_WITH_BOUND_COMPONENTS` guards on `Holder.areComponentsBound`.

## The cast

| class | what it decides | thread |
|---|---|---|
| `DataComponentType` | the key: which codec writes the value to disk, which to the wire, and whether it is saved at all | static, registered at bootstrap |
| `DataComponentMap` | an immutable, identity-keyed map — the prototype's shape | any; never mutated |
| `PatchedDataComponentMap` | what an `ItemStack` actually owns: a shared prototype, a patch, and whether the patch is still someone else's | whichever thread owns the stack |
| `DataComponentPatch` | the serialisable form of the patch: additions and removals | Netty for packets; server and workers for saves |
| `DataComponentInitializers` | builds every registry element's prototype, from the recorded initializers, once the registries exist | reload worker |
| `Holder.Reference` | holds the bound prototype for one registry element, and throws until it has one | bound on the server thread after a reload; on the client at the end of configuration |
| `ItemStack` | the writes (`ItemStack.set`, `ItemStack.update`, `ItemStack.remove`, `ItemStack.copyFrom`) and the reads it inherits from `DataComponentHolder` | whichever thread owns the stack |
| `DataComponentLookup` | the reverse index: which elements of a registry carry this component value | built at freeze, populated lazily |

Everything here ships in both jars; in the trace below only
`ClientPacketListener` is client-only.

## The shape of a stack

```mermaid
flowchart LR
    DCI["DataComponentInitializers.build, on the reload worker, with the registries in hand"] --> HR
    subgraph ITEM["Item, one per registry element"]
        HR["Holder.Reference, bindComponents at reload"] --> PROTO["the prototype: a DataComponentMap, immutable and identity-keyed"]
    end
    subgraph STACK["ItemStack"]
        PDM["PatchedDataComponentMap"] --> PATCH["patch: type to Optional value, empty meaning removed from the prototype"]
        PDM --> COW["copyOnWrite: the map is still shared with the stack it was copied from"]
    end
    PDM -. "prototype, shared by every stack of the item" .-> PROTO
    PATCH -- "asPatch and fromPatch" --> DCP["DataComponentPatch: added values and removed keys, the form on disk and on the wire"]
    KEY["DataComponentType: the key, with a persistent codec, a network codec, or only the latter"] --> PATCH
    KEY --> PROTO
```

Read it left to right. The item's prototype is built by
`DataComponentInitializers` and bound onto the item's `Holder.Reference`.
A stack points at that shared prototype and owns only a patch over it,
whose values are `Optional` — an empty value is a removal. The patch's
serialisable twin is a `DataComponentPatch`, and the key of every entry in
all of them is a `DataComponentType`. The rest of the page is a tour of
those objects, each grounded in one small trace: Sharpness III arriving on
a sword at the enchanting table.

## The key: `DataComponentType`

A type is built by `DataComponentType.Builder`. `DataComponentType.Builder.persistent`
gives the disk and JSON codec; `DataComponentType.Builder.networkSynchronized`
a hand-written wire codec. A type with no persistent codec is **transient**
(`DataComponentType.isTransient`): never saved, only sent.
`DataComponentType.Builder.networkSynchronized` is not a gate — without it,
`DataComponentType.Builder.build` derives a wire codec from the persistent
codec (NBT over the wire), and with neither it throws. The only real switch
is transient-versus-persistent, and it gates *saving*. Three types exist
only on the wire: `DataComponents.CREATIVE_SLOT_LOCK`,
`DataComponents.ADDITIONAL_TRADE_COST`, `DataComponents.MAP_POST_PROCESSING`.

**111** — vanilla types, registered in `DataComponents` into
`BuiltInRegistries.DATA_COMPONENT_TYPE`; 29 of them have slash-shaped ids
(*villager/variant* and its siblings). The catalogue is
[reference/components](../../reference/components.md). Component *types*
are code, in a registry data packs cannot extend; what data packs reach is
the prototype (below) and `CustomData`, which carries arbitrary NBT for
them to use.

Two more flags live on the builder. `DataComponentType.Builder.cacheEncoding`
routes a type's encodes through `EncoderCache` (`DataComponents.ENCODER_CACHE`).
`DataComponentType.Builder.ignoreSwapAnimation` is set on exactly one type,
`DataComponents.DAMAGE` — so durability ticking down does not replay the
held-item swap on the client. Underneath, `DataComponentType.PERSISTENT_CODEC`
and `DataComponentType.VALUE_MAP_CODEC` are the shared dispatch machinery
that `DataComponentMap.CODEC` and the predicates are built on.

## The maps

`DataComponentMap` is immutable and identity-keyed; `DataComponentMap.Builder`
builds one and can carry a `DataComponentMap.Builder.addValidator`, which is
where the prototype-time structural rule lives (below). `DataComponentMap.EMPTY`
is the map every registry element gets when nothing declared one.
`DataComponentMap.composite` is dead API: it exists, and nothing in 26.2
calls it; the layering that actually happens is `PatchedDataComponentMap`'s
prototype-plus-patch.

`PatchedDataComponentMap` is the map an `ItemStack` actually owns: a
`PatchedDataComponentMap.prototype` shared with every stack of that item, a
`PatchedDataComponentMap.patch` whose values are `Optional` (empty means
*removed from the prototype*), and a `PatchedDataComponentMap.copyOnWrite`
flag. It sanitises on every write: `PatchedDataComponentMap.set` stores
nothing when the value equals the prototype's, and
`PatchedDataComponentMap.remove` stores a removal marker only if the
prototype had the key. In the trace, the sword's prototype carries an
*empty* `ItemEnchantments` (every item's does, through
`DataComponents.COMMON_ITEM_COMPONENTS`), so Sharpness III differs from the
prototype and the patch gains one entry. Set the enchantments back to empty
and the entry vanishes rather than becoming an explicit default.

**The first write pays for the copy.** `PatchedDataComponentMap.ensureMapOwnership`
clones the backing map only when `PatchedDataComponentMap.copyOnWrite` is
set; `ItemStack.copy`, `PatchedDataComponentMap.asPatch` and
`ItemStack.transmuteCopy` all alias the same map and set the flag, so
copying a stack is O(1) until someone writes. `ItemStack.applyComponentsAndValidate`
relies on that: it snapshots with `PatchedDataComponentMap.asPatch`,
applies, runs `ItemStack.validateStrict`, and on failure
`PatchedDataComponentMap.restorePatch`.

**Equality is prototype plus patch.** `ItemStack.isSameItemSameComponents`
bottoms out in `PatchedDataComponentMap.equals`. Because setting a value
equal to the prototype default *removes* it from the patch, two stacks that
reached the default by different routes compare equal.

## The patch, on the wire and on disk

`DataComponentPatch` is the serialisable form: additions and removals.
`DataComponentPatch.CODEC` writes removals as `!minecraft:foo`;
`DataComponentPatch.STREAM_CODEC` writes two counts then the entries;
`DataComponentPatch.DELIMITED_STREAM_CODEC` is the length-prefixed variant
for untrusted input; and `DataComponentPatch.split` is the added/removed
decomposition that the hashing and block-entity paths are both built on.
`TypedDataComponent` — a type with its value — has its own "type id then
value" stream codec, distinct from the patch encoding, for the places one
value travels alone.

**The wire patch never contains defaults — for a real stack.** Because
`PatchedDataComponentMap` sanitises on every write, a value equal to the
prototype's is dropped rather than sent. `ItemStackTemplate` is the
exception: it holds a raw `DataComponentPatch` straight from the builder,
which does no such comparison, and sends it verbatim.

On the network the patch travels inside every `ItemStack` in
`ClientboundContainerSetSlotPacket`, `ClientboundContainerSetContentPacket`,
`ClientboundSetCursorItemPacket`, `ClientboundSetPlayerInventoryPacket` and
`ClientboundSetEquipmentPacket`; the client answers ordinary clicks with
hashes, not stacks, and the creative slot alone sends a full, re-validated
stack — [codecs, NBT and JSON](codecs-nbt-json.md) owns the four
serialisations of a stack, and [containers and menus](../items/containers-and-menus.md)
owns what the server does with a hash. On disk an item is saved as a
*patch* (`ItemStack.MAP_CODEC`'s "components", with transient types
silently dropped), but a block entity as a full `DataComponentMap` — the
two are not symmetric.

## The prototype, and why it is built at reload

An `Item` constructor registers its initializer in
`BuiltInRegistries.DATA_COMPONENT_INITIALIZERS`. `Item.Properties.component`
and its convenience methods (`Item.Properties.durability`,
`Item.Properties.food`, `Item.Properties.equippable`, `Item.Properties.sword`,
…) only *record* a `DataComponentInitializers.Initializer`; nothing is a
map yet. `Item.Properties.delayedComponent` and
`Item.Properties.delayedHolderComponent` are the reason it must be
deferred: they name registry entries that do not exist until a world's
registries do — an item's `DataComponents.JUKEBOX_PLAYABLE` or
`DataComponents.DAMAGE_RESISTANT` names an entry a data pack can change.

The maps are *built* with full registry context — tags, damage types,
jukebox songs resolvable — by `DataComponentInitializers.build` on the
reload worker on the server, and *installed* with
`Holder.Reference.bindComponents` on the owning thread: on the server in
`ReloadableServerResources.updateComponentsAndStaticRegistryTags` (server
thread, after every reload including `/reload`), on the client in
`RegistryDataCollector` at the end of configuration. A `/reload` therefore
rebinds every item's prototype. Every registry element gets a component
map (`DataComponentMap.EMPTY` if it had no initializer), so `EntityType`
holders have one too — with one asymmetry, and it runs the way round you
would not guess. `ClientConfigurationPacketListenerImpl` passes
`Connection.isMemoryConnection` into `RegistryDataCollector.collectGameRegistries`,
which negates it, so a **singleplayer** client binds only the registries
`RegistrySynchronization.isNetworkable` accepts and a **multiplayer** client
binds every one. Singleplayer can skip the rest because it shares
`BuiltInRegistries` with the integrated server, whose own apply has already
bound them.

Before binding, reading a registry element's components throws, and the
failure is a null-check, not a friendly error: `Item.components` merely
delegates, the throw comes from `Holder.Reference.components`, and the
non-throwing question is `Holder.areComponentsBound`.
`Item.CODEC_WITH_BOUND_COMPONENTS` guards on it and refuses to decode a
stack until then.

**Ten** — entries in `DataComponents.COMMON_ITEM_COMPONENTS`, the map every
item's prototype starts from. Notably it puts an *empty* `ItemEnchantments`
on every item, which is what `ItemStack.isEnchantable` depends on: it gates
first on `DataComponents.ENCHANTABLE` being present, and *then* on
`DataComponents.ENCHANTMENTS` being present and empty.

**There are two structural rules, at two different times.** At
prototype-build time a validator installed by `Item.Properties` rejects an
item that is both damageable and stackable. At stack time
`ItemStack.validateStrict` rejects a `DataComponents.MAX_DAMAGE` alongside a
`DataComponents.MAX_STACK_SIZE` above one, a count above the stack's own
maximum, an over-weight bundle, and contained items whose counts exceed
their own limits. That last check reaches exactly **one** level into
containers, bundles and charged projectiles and does not re-run the full
validation there — nesting is not followed.

## The reverse index: `DataComponentLookup`

Every frozen `MappedRegistry` builds one (`Registry.componentLookup`): a
lazily-populated reverse index answering "which elements carry this
component value?", which is how the game finds the spawn egg for an entity
type or the item for a dye colour. It reads the same bound prototypes the
holders carry, so it too is meaningless before the first reload.

## The readers and the predicates

`DataComponentGetter` reads one component; `DataComponentHolder` reads one
and has a map, and is implemented only by `ItemStack`, which is where
`DataComponentHolder.get`, `DataComponentHolder.getOrDefault` and
`DataComponentHolder.has` come from. `ItemInstance` is the read-only face
over `ItemStack` and `ItemStackTemplate` (item, count, patch — a record)
that predicates and recipes take. Beyond item behaviour, the callers are
loot functions (`CopyComponentsFunction`) and the `/give` and `/item`
commands.

The predicates come in two strengths. `DataComponentExactPredicate` requires
every listed component to equal. The partial `DataComponentPredicate`
family under `core/component/predicates` — `DataComponentPredicates`, **15**
kinds, in their own `BuiltInRegistries.DATA_COMPONENT_PREDICATE_TYPE`
registry — matches a shape rather than a value, and `DataComponentMatchers`
joins the two for `ItemPredicate`.

## The values, by package

| package | value types |
|---|---|
| `world/item/component` | `Consumable`, `Tool`, `Weapon`, `BlocksAttacks`, `ItemLore`, `CustomData`, `TooltipDisplay`, `ItemContainerContents`, `BundleContents`, `TypedEntityData` … |
| `world/item/equipment` | `Equippable` |
| `world/item/enchantment` | `ItemEnchantments`, `Enchantable`, `Repairable` |

`Item` subclasses no longer carry combat. `Weapon`, `BlocksAttacks`,
`KineticWeapon`, `PiercingWeapon`, `AttackRange`, `SwingAnimation` and
`Tool` are components; `Item.Properties.sword`, `Item.Properties.spear` and
`Item.Properties.humanoidArmor` build whole kits, and *SwordItem* is gone.
But the tools that act *on a block* are not: `AxeItem`, `ShovelItem` and
`HoeItem` still exist as classes, purely for stripping, path-making and
tilling — their combat and mining live in components like everything else.

## The trace: Sharpness at the enchanting table

```mermaid
sequenceDiagram
    participant EM as EnchantmentMenu
    participant IStack as ItemStack
    participant PDM as PatchedDataComponentMap
    participant ACM as AbstractContainerMenu
    participant CPL as ClientPacketListener

    Note over EM: server thread, ServerboundContainerButtonClickPacket has arrived
    EM->>IStack: transmuteCopy(Items.ENCHANTED_BOOK) if the input is a book, same patch over a new prototype
    EM->>IStack: enchant(holder, level) for each chosen EnchantmentInstance
    IStack->>IStack: EnchantmentHelper.updateEnchantments, then set of STORED_ENCHANTMENTS for a book, ENCHANTMENTS otherwise
    IStack->>PDM: set: ensureMapOwnership clones the shared map, the value differs from the prototype's empty set, so patch.put
    Note over PDM: patch is now {minecraft:enchantments to {sharpness: 3}}
    Note over ACM: still inside the packet handler, which calls broadcastChanges itself once the click is accepted
    ACM->>ACM: broadcastChanges, RemoteSlot.Synchronized.matches fails for this slot
    ACM->>CPL: ClientboundContainerSetSlotPacket: count, item id, DataComponentPatch.STREAM_CODEC
    CPL->>CPL: decode: new ItemStack(holder, count, patch), fromPatch against the client's own bound prototype
    CPL->>CPL: handleContainerSetSlot, AbstractContainerMenu.setItem, tooltip via ItemEnchantments.addToTooltip
```

**The menu owns the mutation.** `EnchantmentMenu.clickMenuButton` runs
under `ContainerLevelAccess.execute` on the server thread. For a book it
first calls `ItemStack.transmuteCopy` — a new stack with the *same patch*
applied to the enchanted book's prototype — then `ItemStack.enchant` per
chosen `EnchantmentInstance`. `ItemStack.enchant` hands the edit to
`EnchantmentHelper.updateEnchantments`, which reads the current
`ItemEnchantments`, edits a mutable copy and writes the immutable result
back with `ItemStack.set`; the enchanting rules, the lapis, the seed and
`/enchant` are [Part VII's](../items/enchanting.md). What matters here is
that enchantments are a value, not a list on the stack: one component, one
write.

**One write, one patch entry.** `ItemStack.set` is `PatchedDataComponentMap.set`.
The map the sword owned was shared with whatever it was copied from, so
`PatchedDataComponentMap.ensureMapOwnership` clones it now; the new
`ItemEnchantments` differs from the prototype's empty one, so the patch
gains its single entry. A book that was transmuted a moment earlier carries
the same patch over a different prototype, which is the whole meaning of
`ItemStack.transmuteCopy`.

**The menu compares, and here it does not wait for the tick.**
`AbstractContainerMenu.broadcastChanges` compares every slot against what
the client was last told (`RemoteSlot.Synchronized`). It runs from
`ServerPlayer.tick` in the ordinary case — but a menu-button click is not
the ordinary case: `ServerGamePacketListenerImpl.handleContainerButtonClick`
calls it directly, in the same handler, as soon as
`AbstractContainerMenu.clickMenuButton` accepts. The sword's slot no longer
matches, so `ClientboundContainerSetSlotPacket` goes out, and only the patch
crosses: `ItemStack.OPTIONAL_STREAM_CODEC` writes the count,
`Item.STREAM_CODEC` (a registry id) and the patch. The client answers later
clicks with a `HashedStack` of CRC32C checksums rather than stacks
([codecs, NBT and JSON](codecs-nbt-json.md) for the hashing,
[containers and menus](../items/containers-and-menus.md) for the click
protocol).

**The client rebuilds against its own prototype.** The decoder constructs
`ItemStack` from holder, count and patch, and that constructor is
`PatchedDataComponentMap.fromPatch` against the client's *own* bound
prototype — the map `RegistryDataCollector` bound at the end of
configuration. That is the reason components must be bound on the client
before the play phase: an unbound prototype would throw in a packet decoder
on a Netty thread. `ClientPacketListener.handleContainerSetSlot` then hands
the stack to `AbstractContainerMenu.setItem`, and the tooltip's purple line
is `ItemEnchantments.addToTooltip` reading the same component.

## Components on things that are not items

**Block entities, both directions.** Placing runs
`BlockEntity.applyComponentsFromItemStack`, which hands subclasses a
*recording* `DataComponentGetter`: whatever `BlockEntity.applyImplicitComponents`
reads is forgotten from the patch (`DataComponentPatch.forget`) and only the
leftovers persist as opaque `BlockEntity.components`. Two types are
pre-seeded into that forget set regardless of whether anything reads them
— `DataComponents.BLOCK_ENTITY_DATA` and `DataComponents.BLOCK_STATE` — and
only the *added* half of the resulting patch is kept, so removals are
discarded. Breaking or picking runs the reverse,
`BlockEntity.collectComponents` over `BlockEntity.collectImplicitComponents`,
with `BlockEntity.removeComponentsFromTag` de-duplicating what was
promoted; `BlockItem.setBlockEntityData` is the write path for the opaque
blob.

**Entities, read-only.** `Entity` implements `DataComponentGetter` with no
patch of its own: `Entity.get` answers `DataComponents.CUSTOM_NAME` and
`DataComponents.CUSTOM_DATA` by hand, lets subclass overrides (`Sheep`,
`Wolf`, `Villager` …) answer the variant-shaped types, and otherwise falls
through to its `EntityType` holder's bound prototype — the same map every
registry element gets. `Entity.applyComponentsFromItemStack` is the write
path, and it is not only spawn eggs: any item-to-entity spawn, an arrow
picking up its stack, a lingering potion's cloud and `BlockItem` all take
it.

## Where to look

`DataComponentType` · `DataComponents` · `DataComponentMap` ·
`PatchedDataComponentMap` · `DataComponentPatch` · `DataComponentInitializers` ·
`Holder.Reference` · `DataComponentLookup` · `Item.Properties` · `ItemStack` ·
`ItemInstance` · `ItemStackTemplate` · `EnchantmentMenu` ·
`AbstractContainerMenu` · `BlockEntity` · `Entity` (the getter half)

---

*Rules: names, never code · how the system works, not how the code reads ·
newest version only · every backticked name passes `tools/verify_names.py`.*
