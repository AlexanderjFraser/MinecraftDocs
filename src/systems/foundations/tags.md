# Tags

> Verified against **Minecraft 26.2** · Part II · `#minecraft:logs` from a JSON file in a data pack to the `HolderSet` a parrot checks before it perches.

## Responsibility

A tag is a named set of registry entries, defined in data-pack JSON, that
code tests membership against by key. Blocks that count as logs, items that
can be enchanted with Sharpness, biomes where villages spawn, entity types
that arrows pass through — all are tags, and all are one `TagKey` constant in
code plus one file per pack. Tags are how vanilla data reaches into
hard-coded behaviour without the behaviour naming any specific block.

The one sentence a player recognises: *an axe strips anything in
`#minecraft:logs`, and a data pack can put a new block in that set.*

## The data it owns

- `TagKey` — a record of the registry key and an `Identifier`, **interned**
  through a weak interner so `TagKey.create` always returns the canonical
  instance; membership tests are set-contains on identity.
  `BlockTags`, `ItemTags`, `EntityTypeTags`, `BiomeTags`, `FluidTags` and
  their siblings are catalogues of keys and hold no contents. Keys shared by
  a block and its item are declared once as a `BlockItemTagId` in
  `BlockItemTags` and projected into both (`BlockTags.LOGS` is
  `BlockItemTags.LOGS.block()`).
- `TagFile` — the on-disk shape: a list of `TagEntry` and a "replace" flag.
  A `TagEntry` is an element id, a `#`-prefixed reference to another tag, and
  a "required" flag (default true).
- `TagLoader` — the loader, generic over what it resolves to (a `Holder` for
  registries, a `CommandFunction` for function tags). Two instance steps,
  `TagLoader.load` (read every pack's copy of every file into
  `TagLoader.EntryWithSource` lists) and `TagLoader.build` (resolve, in
  dependency order). Its `TagLoader.ElementLookup` decides how an id becomes
  an element; `TagLoader.LoadResult` is the resolved-but-unbound output.
- Inside a `MappedRegistry`: `MappedRegistry.frozenTags` holds the one
  canonical `HolderSet.Named` per key — created on first request and **never
  replaced**, so anyone who cached a `HolderSet.Named` sees new contents after
  a reload — and `MappedRegistry.allTags` is a `MappedRegistry.TagSet` that
  starts out `MappedRegistry.TagSet.unbound`, where every read throws. Each
  `Holder.Reference` carries its own `Set` of `TagKey`s, bound by
  `Holder.Reference.bindTags`; that set is what `Holder.Reference.is` reads.
- `Registry.PendingTags` — a loaded-but-not-applied tag table for one frozen
  registry, with a `Registry.PendingTags.lookup` that answers as if applied
  and a `Registry.PendingTags.apply` that swaps it in.
- `TagNetworkSerialization.NetworkPayload` — the wire form: tag id → list of
  registry **ints**.

Everything in `net/minecraft/tags` ships in both jars. There is no *TagManager* in 26.2
and no tag reload listener; loading is static functions on `TagLoader`
called from `WorldLoader`, `MinecraftServer.reloadResources`,
`ReloadableServerRegistries` and the registry load tasks.

## When it runs

- **World load and `/reload`, worker pool then server thread.**
  `TagLoader.loadTagsForExistingRegistries` runs *before* the reload
  listeners, producing `Registry.PendingTags` for every static registry. The
  pending lookups are made visible to worldgen and loot loading through
  `TagLoader.buildUpdatedLookups`. They are applied — atomically, per
  registry — in `ReloadableServerResources.updateComponentsAndStaticRegistryTags`,
  on the server thread, after every listener has finished. For the duration
  of a reload the old tags are what `Registry.getTags` answers and the new
  tags are what the loading codecs see.
- **Data-pack registries, inside their own load task.** Tags for a biome or
  enchantment registry are loaded by `ResourceManagerRegistryLoadTask`
  after its elements, with `TagLoader.ElementLookup.fromGetters`, and bound
  by `WritableRegistry.bindTags` before that registry freezes.
- **Configuration phase and after `/reload`, over the wire.** One
  `ClientboundUpdateTagsPacket` covering every synced registry, sent by
  `SynchronizeRegistriesTask` after the registry data, and broadcast again by
  `PlayerList.reloadResources`. The client applies it on its main thread.

## The trace: `#minecraft:logs` from JSON to a block check

```mermaid
sequenceDiagram
    participant WL as WorldLoader (worker pool)
    participant TL as TagLoader
    participant MR as MappedRegistry (BLOCK)
    participant RSR as ReloadableServerResources (server thread)
    participant SRT as SynchronizeRegistriesTask
    participant CPL as ClientPacketListener (client thread)
    participant P as Parrot

    WL->>TL: loadTagsForExistingRegistries(resources, STATIC layer)
    TL->>TL: load — every pack's tags/block/logs.json via FileToIdConverter.json; "replace" clears what lower packs contributed
    TL->>TL: build — DependencySorter orders oak_logs before logs; TagEntry.build resolves ids through ElementLookup.fromFrozenRegistry
    TL->>MR: prepareTagReload(LoadResult) — a Registry.PendingTags; nothing visible yet
    Note over WL,MR: worldgen and loot codecs resolve #minecraft:logs through PendingTags.lookup via TagLoader.buildUpdatedLookups
    RSR->>MR: PendingTags.apply — bind every HolderSet.Named, swap allTags, refreshTagsInHolders → Holder.Reference.bindTags on every Block
    SRT->>CPL: ClientboundUpdateTagsPacket — TagNetworkSerialization.serializeTagsToNetwork: registry ints, not names
    CPL->>CPL: handleUpdateTags → prepareTagReload + apply (skipped on a memory connection)
    P->>MR: state.is(BlockTags.LOGS) → TypedInstance.is → Block.builtInRegistryHolder → Holder.Reference.is — a Set.contains
```

Narrated:

1. **Every pack's file, lowest first.** `TagLoader.load` lists resource
   *stacks* (`ResourceManager.listResourceStacks`), so all copies of
   `tags/block/logs.json` across the enabled packs are visited in priority
   order and merged; a "replace" in a higher pack discards what lower packs
   contributed to that id. A pack whose file fails to parse is logged and
   skipped, never fatal.
2. **Tags of tags resolve in dependency order.** `BlockTags.LOGS` is a tag
   whose entries are other tags (`#minecraft:oak_logs` …). `TagLoader.build`
   feeds tag references into a `DependencySorter` and resolves leaves first.
   A tag with one missing *required* reference is dropped whole — not loaded
   minus the missing entry — and is then absent from `Registry.getTags`, so
   neither the network payload nor a lookup will find it. Optional entries
   (`"required": false`) simply resolve to nothing.
3. **Prepared, then applied.** `MappedRegistry.prepareTagReload` refuses a
   registry that is not frozen. It builds the new table reusing the existing
   `HolderSet.Named` objects and returns a `Registry.PendingTags`. The
   `Registry.PendingTags.apply` is one field write of the `MappedRegistry.TagSet` plus a rebind of
   every holder's tag set — there is no moment when half the tags are new.
4. **The client gets integers.** `TagNetworkSerialization.serializeTagsToNetwork`
   walks `RegistrySynchronization.networkSafeRegistries` — every `RegistryLayer.STATIC`
   registry plus the synced dynamic ones — and writes each tag as a list of
   registry ids. That is why the packet must follow `ClientboundRegistryDataPacket`:
   the ids for dynamic registries are only meaningful once the client has
   built the same registry in the same order. `ClientPacketListener.handleUpdateTags`
   does `MappedRegistry.prepareTagReload` then `Registry.PendingTags.apply` per registry, **unless** the
   connection is a memory connection: in singleplayer the integrated server's
   apply already rebound the `BuiltInRegistries` both halves share.
5. **The check is a field read.** `BlockBehaviour.BlockStateBase` is a
   `TypedInstance`; `TypedInstance.is` asks the type holder — for a block,
   `Block.builtInRegistryHolder`, the intrusive holder from
   [identifiers-and-registries](identifiers-and-registries.md) — and
   `Holder.Reference.is` is set-contains on an interned `TagKey`. `Parrot`
   (perch search), `TrunkPlacer` (worldgen) and the client's
   `PunchTreeTutorialStepInstance` all ask this way. `FluidState`, `Entity`
   and `ItemStack` go through the same interface.

## Interfaces

- **Called by:** `WorldLoader.load` and `MinecraftServer.reloadResources`
  (static registries), `ResourceManagerRegistryLoadTask` and
  `ReloadableServerRegistries.reload` (dynamic and reloadable registries),
  `ServerFunctionLibrary` (function tags, the one non-registry user),
  `RegistryDataCollector` and `ClientPacketListener` on the client.
- **Calls into:** the resource system for files (`FileToIdConverter.json`,
  `ResourceManager.listResourceStacks`, page [resource-system](resource-system.md));
  `DependencySorter` for ordering; the registry for binding.
- **Crosses the network as:** `ClientboundUpdateTagsPacket`, a map of
  registry key → `TagNetworkSerialization.NetworkPayload`, in configuration
  and again in play after a server `/reload`.
- **Data-driven by:** `data/<namespace>/tags/<registry path>/<name>.json`
  (`Registries.tagsDirPath`), so *tags/block*, *tags/item*,
  *tags/entity_type*, *tags/worldgen/biome*. There is no plural-name
  fallback in the loader. Vanilla's files are written by the data generator
  (`TagsProvider`, `TagBuilder`), which the running game never calls.

## Invariants and surprises

- **Before the first bind, tags throw, they do not return empty.**
  `MappedRegistry.TagSet.unbound` and an unbound `Holder.Reference` both
  throw on any read, so `is(BlockTags.LOGS)` from a static initialiser is a
  crash. `BuiltInRegistries.freeze` binds every static tag to empty
  precisely so that the game can run between startup and world load.
- **A tag can only name elements of its own registry.** `TagEntry` carries
  an `Identifier`; the registry is fixed by the directory the file is in.
  It *can* name a data-pack element that has not loaded yet: the required
  path creates a placeholder `Holder.Reference` through
  `MappedRegistry.createRegistrationLookup`, and the registry's freeze fails
  with unbound values if the element never arrives.
- **Identity is stable across reloads.** `HolderSet.Named` objects are
  reused; `HolderSet.Named.contains` delegates to the holder's own tag set,
  not the list. A recipe ingredient or loot condition that captured a
  `HolderSet.Named` at load time is correct after `/reload` without
  re-lookup.
- **What the client is never told:** tags of `RegistryLayer.RELOADABLE`-layer registries
  (loot tables, predicates) and of non-synced worldgen registries
  (configured features, structures). `RegistrySynchronization.isNetworkable`
  is the test.
- **Duplicate entries collapse and file order is preserved** —
  `TagLoader.build` collects into an insertion-ordered set — so
  `Registry.getRandom`-style iteration over a tag is deterministic per pack
  stack.
- **Function tags are the odd one out.** `ServerFunctionLibrary` runs its
  own `TagLoader` over `CommandFunction`s with `#load` and `#tick` as the
  consumers; no registry is involved (see Part XII).

## Where to look

`TagKey` · `BlockItemTags` · `BlockTags` · `TagFile` · `TagEntry` ·
`TagLoader` · `MappedRegistry` (the tag half) · `Registry.PendingTags` ·
`HolderSet` · `WorldLoader` · `ReloadableServerResources` ·
`TagNetworkSerialization` · `ClientboundUpdateTagsPacket` ·
`ClientPacketListener` · `TypedInstance`

---

*Rules: names, never code · how the system works, not how the code reads ·
newest version only · every backticked name passes `tools/verify_names.py`.*
