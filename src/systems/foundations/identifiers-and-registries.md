# Identifiers and registries

> Verified against **Minecraft 26.2** · Part II · How `minecraft:diamond_sword` becomes an `Item` before the game exists, and how a data-pack biome becomes a `Holder` the client can be told about.

## Responsibility

Everything in Minecraft that has a name lives in a registry: a table from
`ResourceKey` to object that also assigns each object a small integer for the
wire. Some registries are **built in** — filled by static initialisers before
any world exists and frozen forever (blocks, items, entity types). Others are
**dynamic** — loaded from data-pack JSON when a world opens (biomes,
dimension types, enchantments, loot tables) and sent to the client during the
configuration phase. The `Holder` type is the seam between the two: a
reference to a registry entry that may be handed out before the entry exists
and that the registry binds later.

The one sentence a player recognises: *`/give @s minecraft:diamond_sword`
works because the string on the left is a key in a table the server froze at
startup.*

## The data it owns

- `Identifier` (`net/minecraft/resources`) — namespace and path, a pure value with strict
  character rules (`Identifier.isValidNamespace`, `Identifier.isValidPath`).
  `Identifier.withDefaultNamespace` supplies the "minecraft" namespace; `Identifier.parse`
  and `Identifier.tryParse` are the string entry points; `Identifier.read`
  is the Brigadier one. This is the class 1.21 readers know as
  *ResourceLocation*.
- `ResourceKey` — an `Identifier` paired with the `Identifier` of the
  registry it belongs to. Keys are **interned** through a weak map keyed by
  `ResourceKey.InternKey`, so two keys for the same registry and id are the
  same object; `MappedRegistry` relies on that for its identity maps.
  `Registries` holds the 149 `ResourceKey`s *of registries*
  (`Registries.ITEM`, `Registries.BIOME` …); `ItemIds` and `BlockItemIds`
  (`net/minecraft/references`) hold the per-element keys the static initialisers use.
- `Registry` — the read interface: `Registry.getValue`, `Registry.getKey`,
  `Registry.getId`, `Registry.getTags`, plus codecs (`Registry.byNameCodec`,
  `Registry.holderByNameCodec`). It extends `IdMap`, so every registry is
  also an int ↔ object table. `WritableRegistry` adds
  `WritableRegistry.register` and `WritableRegistry.bindTags`;
  `DefaultedRegistry` (`DefaultedMappedRegistry`) answers a default entry —
  "air" for items and blocks — instead of null.
- `MappedRegistry` — the one real implementation. It owns `MappedRegistry.byId`
  (insertion order **is** the numeric id), `MappedRegistry.byKey`,
  `MappedRegistry.byLocation`, `MappedRegistry.byValue`,
  `MappedRegistry.registrationInfos`, the tag table `MappedRegistry.allTags`
  (`MappedRegistry.TagSet`), the per-element component table
  `MappedRegistry.componentLookup`, and the `MappedRegistry.frozen` flag that
  `MappedRegistry.validateWrite` checks on every mutation.
- `Holder` — a sealed interface with two kinds (`Holder.Kind`).
  `Holder.Reference` is an entry *in* a registry: it knows its
  `HolderOwner`, its key, its tags and its components, and any of those may
  be unbound until the registry binds them (`Holder.Reference.bindValue`,
  `Holder.Reference.bindTags`, `Holder.Reference.bindComponents`).
  `Holder.Direct` is a record wrapping an inline value that belongs to no
  registry — it has no key, is in no tag, and serialises inline.
  `HolderSet` is a set of holders: `HolderSet.Named` is a tag,
  `HolderSet.Direct` is a literal list.
- `HolderGetter` / `HolderLookup` / `HolderOwner` — the read-only views a
  codec sees. `HolderLookup.Provider` is "all the registries I may resolve
  against"; `HolderLookup.RegistryLookup` is one of them. `HolderOwner`
  exists for one question — `HolderOwner.canSerializeIn` — which is how a
  holder from one world refuses to be written by another world's context.
- `RegistryAccess` — a `HolderLookup.Provider` over a set of registries;
  `RegistryAccess.Frozen` is the marker for the finished kind.
  `LayeredRegistryAccess` stacks several, one per `RegistryLayer`:
  **`RegistryLayer.STATIC`, `RegistryLayer.WORLDGEN`, `RegistryLayer.DIMENSIONS`, `RegistryLayer.RELOADABLE`**, in that order.
  `LayeredRegistryAccess.getAccessForLoading` is everything *before* a layer
  (what that layer's JSON may reference); `LayeredRegistryAccess.compositeAccess`
  is everything. The client mirrors this with two layers,
  `ClientRegistryLayer.STATIC` and `ClientRegistryLayer.REMOTE`.
- `RegistrationInfo` — per entry: a `Lifecycle` and the `KnownPack` it came
  from. `RegistrationInfo.BUILT_IN` is what every static registration gets.

All of this is server *and* client: `MappedRegistry`, `BuiltInRegistries`,
`RegistryDataLoader` ship in the dedicated server jar. Only
`ClientRegistryLayer`, `RegistryDataCollector` and `KnownPacksManager` are
client-only.

## When it runs

Three moments, three threads.

1. **Launch, on the launching thread**, before any server or client object
   exists: `Bootstrap.bootStrap` → `BuiltInRegistries.bootStrap`. Both
   `Main` classes do this first (see [Anatomy](../anatomy/anatomy.md)).
   After it returns every built-in registry is frozen and any
   `WritableRegistry.register` throws.
2. **World load, on the worker pool**: `WorldLoader.load` runs
   `RegistryDataLoader.load` on `Util.backgroundExecutor`, with hops back to
   the main thread for resource-manager creation and the final assembly.
   This is where the `RegistryLayer.WORLDGEN`, `RegistryLayer.DIMENSIONS` and `RegistryLayer.RELOADABLE` layers are
   filled. `/reload` re-runs only the `RegistryLayer.RELOADABLE` step.
3. **Configuration phase, on the server thread then the client thread**:
   `SynchronizeRegistriesTask` sends the dynamic registries; the client
   rebuilds its `ClientRegistryLayer.REMOTE` layer in `RegistryDataCollector.collectGameRegistries`
   (decoding on the worker pool, joined on the client thread) before it will
   accept play packets.

## The trace: `minecraft:diamond_sword` becomes an `Item`

```mermaid
sequenceDiagram
    participant Main as Main (server or client)
    participant B as Bootstrap
    participant BIR as BuiltInRegistries
    participant Items as Items
    participant Item as Item
    participant MR as MappedRegistry (ITEM)

    Main->>B: bootStrap — the very first thing the JVM does with the game
    B->>BIR: class init — one empty MappedRegistry per Registries key, each registered into WRITABLE_REGISTRY, each with a loader in LOADERS
    B->>BIR: bootStrap → createContents — run every loader
    BIR->>Items: class init (the ITEM loader touches Items.AIR)
    Items->>Items: registerItem(ItemIds.DIAMOND_SWORD, properties) — Item.Properties.setId stores the key
    Items->>Item: new Item(properties)
    Item->>MR: createIntrusiveHolder — a Holder.Reference with a value but no key yet
    Items->>MR: Registry.register → WritableRegistry.register(key, item, BUILT_IN) — bindKey, numeric id = byId.size()
    BIR->>BIR: freeze — root first, then every registry: bindAllTagsToEmpty, MappedRegistry.freeze
    MR->>MR: freeze — bindValue on every holder, refuse if any holder or tag is unbound, build componentLookup
    BIR->>BIR: validate — no empty registry, every DefaultedRegistry has its default
    Note over Main,MR: Item tags stay empty until a world's data packs load; the client gets them by ClientboundUpdateTagsPacket
```

Narrated:

1. **Registries exist before their contents.** `BuiltInRegistries` class
   init creates every registry empty and records the loader that fills it
   in `BuiltInRegistries.LOADERS`, an insertion-ordered map. `Bootstrap.bootStrap`
   then runs `BuiltInRegistries.createContents` — the loaders in that order —
   which forces the class init of `Items`, `Blocks`, `EntityType` and the
   rest. `Bootstrap.checkBootstrapCalled` is the guard that makes
   "touched `Blocks` from a static initialiser" a crash rather than a
   silent empty registry.
2. **The key travels in the properties.** `Items.registerItem` takes a
   `ResourceKey` from `ItemIds` and calls `Item.Properties.setId` before
   constructing; an `Item` therefore knows its own key at construction time.
   Blocks do the same with `BlockItemIds`.
3. **Intrusive holders.** Five registries — `BuiltInRegistries.BLOCK`, `BuiltInRegistries.ITEM`, `BuiltInRegistries.FLUID`,
   `BuiltInRegistries.ENTITY_TYPE`, `BuiltInRegistries.BLOCK_ENTITY_TYPE` — are created with intrusive holders:
   the constructor asks the registry for a `Holder.Reference`
   (`MappedRegistry.createIntrusiveHolder`) that wraps the object before it
   has a key, and stores it in `Item.builtInRegistryHolder`. Registration
   then binds the key to *that* holder rather than creating a new one, so
   `Item.builtInRegistryHolder` and the registry's own holder are the same
   object and tag checks on it are a field read.
4. **The numeric id is the line number.** `MappedRegistry.register` appends
   to `MappedRegistry.byId`; the wire id of an item is the position of its
   line in `Items`. `Item.STREAM_CODEC` is `ByteBufCodecs.holderRegistry`
   over `Registries.ITEM`, which encodes that integer.
5. **Freeze is a proof.** `MappedRegistry.freeze` binds every holder's value
   and throws if any holder is still unbound, any intrusive holder was
   created but never registered, or any tag declared by a `TagKey` was never
   bound. `BuiltInRegistries.freeze` first binds all tags to empty
   (`MappedRegistry.bindAllTagsToEmpty`) so that this check passes for the
   static registries, whose real tags do not exist until a data pack is read.

## The trace: a data-pack biome becomes a `Holder` and reaches the client

```mermaid
sequenceDiagram
    participant WL as WorldLoader (server, worker pool)
    participant RDL as RegistryDataLoader
    participant T as ResourceManagerRegistryLoadTask (BIOME)
    participant LRA as LayeredRegistryAccess
    participant SCP as ServerConfigurationPacketListenerImpl (server thread)
    participant CCP as ClientConfigurationPacketListenerImpl (client thread)
    participant RDC as RegistryDataCollector

    WL->>WL: RegistryLayer.createRegistryAccess — STATIC filled from BuiltInRegistries.REGISTRY, three empty layers
    WL->>WL: TagLoader.loadTagsForExistingRegistries — static-registry tags read but not yet applied
    WL->>RDL: load(resources, getAccessForLoading(WORLDGEN), WORLDGEN_REGISTRIES, backgroundExecutor)
    RDL->>T: one RegistryLoadTask per RegistryData; every task's ConcurrentHolderGetter is visible to every other
    T->>T: FileToIdConverter.registry lists data/*/worldgen/biome/*.json; decode in parallel; registerElements; loadTagsForRegistry + registerTags
    T->>T: freezeRegistry, validateRegistry
    RDL->>LRA: replaceFrom(WORLDGEN, …) — then again for DIMENSIONS (LEVEL_STEM), later RELOADABLE
    SCP->>CCP: ClientboundSelectKnownPacks — which packs do you already have?
    CCP->>SCP: ServerboundSelectKnownPacks
    SCP->>CCP: ClientboundRegistryDataPacket × N — RegistrySynchronization.packRegistries; entries from a known pack carry no data
    SCP->>CCP: ClientboundUpdateTagsPacket — every synced registry's tags
    SCP->>CCP: ClientboundFinishConfigurationPacket
    CCP->>RDC: collectGameRegistries — RegistryDataLoader.load with NetworkRegistryLoadTasks; missing data re-read from the local pack
    RDC->>CCP: a RegistryAccess.Frozen into CommonListenerCookie.receivedRegistries
    CCP->>SCP: ServerboundFinishConfigurationPacket — play may begin
```

Narrated:

1. **Layers load against the layers before them.** `RegistryDataLoader.load`
   is given `LayeredRegistryAccess.getAccessForLoading`, so a biome JSON may
   reference a placed feature (same layer) or a sound event (`RegistryLayer.STATIC`) but
   never a level stem (`RegistryLayer.DIMENSIONS`, which loads after). The lists
   `RegistryDataLoader.WORLDGEN_REGISTRIES`, `RegistryDataLoader.DIMENSION_REGISTRIES`
   and `RegistryDataLoader.SYNCHRONIZED_REGISTRIES` say which keys belong to
   which step and which subset the client is told about.
2. **Loading is a task graph.** Each registry is one `RegistryLoadTask`
   owning a fresh `MappedRegistry` and a lock-guarded `ConcurrentHolderGetter`.
   `RegistryDataLoader.createContext` hands every task's getter to every
   other, so `Biome.DIRECT_CODEC` decoding on one worker can ask for a
   configured carver that another worker is still registering — the getter
   returns an unbound `Holder.Reference` and the reference is bound when that
   registry freezes. Forward references cost nothing; cycles are impossible
   because layers order the registries.
3. **Provenance is recorded per entry.** `ResourceManagerRegistryLoadTask`
   gives each element a `RegistrationInfo` naming the `KnownPack` it came
   from and a `Lifecycle` — stable if the pack is vanilla, experimental
   otherwise. That is what the "experimental features" warning on world open
   is reading.
4. **The client is told what it does not already have.**
   `SynchronizeRegistriesTask` first asks the client which `KnownPack`s it
   has (`ClientboundSelectKnownPacks`). If the client's answer matches,
   `RegistrySynchronization.packRegistries` sends every element's *id* but
   leaves the NBT payload empty for entries from those packs; the client's
   `NetworkRegistryLoadTask.findAndLoadFromResource` re-decodes the JSON from
   its own jar. A modified biome from a custom data pack is sent in full
   through `Biome.NETWORK_CODEC` — the network codec, which omits generation
   settings the client never needs.
5. **The client rebuilds, it does not patch.** `RegistryDataCollector`
   only accumulates packets; `RegistryDataCollector.collectGameRegistries`
   runs when configuration finishes and builds the entire `ClientRegistryLayer.REMOTE` layer in
   one go, then freezes. The result is a `RegistryAccess.Frozen` that lives
   in `CommonListenerCookie` and is what every `RegistryFriendlyByteBuf` in
   the play phase decodes against. Every reconfiguration (server `/reload`
   does not, but a dimension-set change does) rebuilds it wholesale.

## Interfaces

- **Called by:** everything. `Registry.register` from every static
  initialiser; `RegistryOps` from every codec that names a registry entry;
  `MinecraftServer.registryAccess` and `ClientPacketListener.registryAccess`
  from anything that needs to resolve a key at runtime.
- **Calls into:** the resource system (`FileToIdConverter.registry` over a
  `ResourceManager`, page [resource-system](resource-system.md)), tags
  (`TagLoader`, page [tags](tags.md)), codecs (`RegistryFileCodec`,
  `RegistryFixedCodec`, `RegistryCodecs.homogeneousList`, `HolderSetCodec`,
  page [codecs-nbt-json](codecs-nbt-json.md)).
- **Crosses the network as:** `ClientboundSelectKnownPacks` /
  `ServerboundSelectKnownPacks`, then `ClientboundRegistryDataPacket` (one
  per synchronised registry, entries as `RegistrySynchronization.PackedRegistryEntry`),
  then `ClientboundUpdateTagsPacket`, all in the configuration phase. Built-in
  registries never cross — both sides ran the same static initialisers, which
  is why the wire id of a block is a bare varint.
- **Data-driven by:** `data/<namespace>/<registry path>/*.json` for every
  key in `RegistryDataLoader.WORLDGEN_REGISTRIES` and
  `RegistryDataLoader.DIMENSION_REGISTRIES`; the reloadable set (loot tables,
  predicates, item modifiers) through `ReloadableServerRegistries`. The
  catalogue of which registry is which kind is
  [reference/registries](../../reference/registries.md).

## Invariants and surprises

- **A holder can exist before its entry does.** `Holder.Reference` is a
  promise; `Holder.Reference.value` throws until the registry calls
  `Holder.Reference.bindValue`. Codecs hand these out freely during load and
  the freeze is what makes every promise kept — or fails loudly.
- **Holders carry components now.** `Holder.Direct` is a record of value
  *and* `DataComponentMap`; `Holder.Reference.bindComponents` and
  `MappedRegistry.componentLookup` attach per-entry data components to
  registry elements, built by `BuiltInRegistries.DATA_COMPONENT_INITIALIZERS`.
  This is beyond tags; see [data-components](data-components.md).
- **Numeric ids are an accident of source order.** Nothing in the data
  files decides them; `MappedRegistry.byId` insertion order does. A resource
  pack cannot change a block id; reordering two lines in `Blocks` would.
- **`Registries.DIMENSION` and `Registries.LEVEL_STEM` share the identifier
  `minecraft:dimension`** — two registry keys, one id, different element
  types. `Registries.LEVEL_STEM` is the data-pack registry the `RegistryLayer.DIMENSIONS` layer loads;
  `Registries.DIMENSION` keys the `ServerLevel`s.
- **The vanilla data is not built at runtime.** `RegistrySetBuilder`,
  `BootstrapContext` and `VanillaRegistries` are the data generator that
  *writes* the JSON in the jar; the running game only ever reads JSON. A
  1.21 reader who remembers biomes being registered in code is remembering
  datagen.
- **Lifecycle is provenance.** `ResourceManagerRegistryLoadTask` decides
  stable vs experimental from the pack's `KnownPack`; anything received over
  the network is experimental; the whole `RegistryLayer.RELOADABLE` layer is constructed
  experimental. The registry's own lifecycle is the merge of its entries'.
- **`IdMapper` is not a registry.** It is the standalone `IdMap` used for
  `BlockState` ids (`Block.BLOCK_STATE_REGISTRY`) and similar palettes; the
  two share an interface and nothing else.
- **Tags bind before freeze and never after — except through
  `Registry.PendingTags`.** `MappedRegistry.freeze` refuses a registry whose
  tags are already bound or whose declared tags are unbound;
  `MappedRegistry.prepareTagReload` is the one sanctioned way to swap the tag
  table of a frozen registry, and it swaps atomically.

## Where to look

`Identifier` · `ResourceKey` · `Registries` · `Registry` · `MappedRegistry` ·
`Holder` · `HolderSet` · `HolderLookup` · `BuiltInRegistries` · `Bootstrap` ·
`RegistryLayer` · `LayeredRegistryAccess` · `WorldLoader` ·
`RegistryDataLoader` · `RegistryLoadTask` · `ResourceManagerRegistryLoadTask` ·
`RegistrySynchronization` · `SynchronizeRegistriesTask` ·
`RegistryDataCollector` · `NetworkRegistryLoadTask` · `RegistryOps`

---

*Rules: names, never code · how the system works, not how the code reads ·
newest version only · every backticked name passes `tools/verify_names.py`.*
