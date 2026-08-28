# Codecs, NBT and JSON

> Verified against **Minecraft 26.2** · Part II · One `ItemStack` written three ways: into a chest's chunk file, into a container packet, and out of the text of a `/give`.

## Responsibility

Minecraft serialises through one abstraction and two wire shapes. The
abstraction is DataFixerUpper's `Codec`: a description of a type that can
encode to or decode from *any* format given a `DynamicOps` for it. The two
formats the game actually uses are **NBT** (`NbtOps`, the binary tree on
disk and the text form SNBT that commands use) and **JSON** (`JsonOps`, the
data packs). Packets are the exception: they do not go through a codec at
all but through a `StreamCodec`, hand-laid bytes on a Netty `ByteBuf`,
because a packet is written once, read once, and must be small.

The one sentence a player recognises: *the thing in square brackets after an
item name in `/give` is the same data that ends up in the chunk file.*

## The data it owns

- **Codecs** (external, in com.mojang.serialization; the game adds
  `ExtraCodecs` in `net/minecraft/util`). `ExtraCodecs.intRange`, `ExtraCodecs.nonEmptyList`,
  `ExtraCodecs.optionalAlwaysPresentFieldOf` and friends are the vocabulary
  most game codecs are built from. A codec that names a registry entry —
  `Item.CODEC_WITH_BOUND_COMPONENTS`, any `Holder` — needs a `RegistryOps`
  (`net/minecraft/resources`), a `DelegatingOps` that carries a `HolderLookup.Provider`;
  `HolderLookup.Provider.createSerializationContext` is how every caller
  makes one. Without it those codecs fail, which is the reason the disk and
  command paths below always start by building a context.
- **NBT** (`net/minecraft/nbt`). `Tag` is a **sealed** interface: `CompoundTag`,
  `CollectionTag` (`ListTag`, `ByteArrayTag`, `IntArrayTag`, `LongArrayTag`),
  `PrimitiveTag` (`StringTag` and the six `NumericTag` records) and
  `EndTag`. The leaves are records; `CompoundTag` owns a map;
  `ListTag` may hold mixed types. `NbtIo` reads and writes streams and
  files (`NbtIo.readCompressed`, `NbtIo.writeCompressed` are GZIP);
  `NbtAccounter` is the read-side byte-and-depth budget every untrusted read
  carries (`NbtAccounter.DEFAULT_NBT_QUOTA` is 2 MiB); `NbtOps.INSTANCE` is
  the `DynamicOps` over tags, and `NbtOps.convertTo` is the bridge to any
  other format. `TagParser` parses SNBT and is generic over the *output*
  ops, so text can decode straight into a registry-aware context;
  `SnbtGrammar` is the packrat grammar behind it, `SnbtOperations` the
  built-in `bool(...)` and `uuid(...)` functions. `StringTagVisitor` and
  `SnbtPrinterTagVisitor` print; `TextComponentTagVisitor` colours for `/data`.
- **The save façade** (`world/level/storage`). `ValueOutput` and
  `ValueInput` are what a `BlockEntity` or `Entity` writes to and reads
  from: `ValueOutput.store` with a codec, `ValueOutput.child`,
  `ValueOutput.list`, and typed getters with defaults on the input side
  (`ValueInput.getIntOr`, `ValueInput.getStringOr`). The only implementations
  are `TagValueOutput` and `TagValueInput`, which wrap a `CompoundTag` plus a
  `DynamicOps`. Every encode or decode failure is *reported*, not thrown,
  through a `ProblemReporter` — `ProblemReporter.ScopedCollector` logs the
  collected tree of problems on close, rooted at `BlockEntity.problemPath`
  or `Entity.problemPath`.
- **Stream codecs** (`net/minecraft/network/codec`, `net/minecraft/network`). `StreamCodec` pairs a
  `StreamEncoder` and a `StreamDecoder`; `StreamCodec.composite` builds one
  from up to twelve field codecs. `ByteBufCodecs` is the catalogue of
  primitives (`ByteBufCodecs.VAR_INT`, `ByteBufCodecs.STRING_UTF8`,
  `ByteBufCodecs.TAG`, `ByteBufCodecs.TRUSTED_TAG` …) and bridges:
  `ByteBufCodecs.fromCodec` sends NBT built by a `Codec`;
  `ByteBufCodecs.registry`, `ByteBufCodecs.holder`, `ByteBufCodecs.holderSet`
  send registry ids. `FriendlyByteBuf` wraps a `ByteBuf` with varints,
  strings, NBT, identifiers and positions; `RegistryFriendlyByteBuf` adds
  `RegistryFriendlyByteBuf.registryAccess`, and exists only in the play
  phase — `RegistryFriendlyByteBuf.decorator` is bound when the protocol
  switches from configuration to play. `IdDispatchCodec` is the packet-id
  table itself.

All of this ships in both jars.

## When it runs

Codecs run wherever data is: the **server thread** for saves initiated by
the tick (`BlockEntity.saveWithFullMetadata` inside chunk serialisation,
`PlayerDataStorage.save`), the **worker pool** for `SerializableChunkData.write`
and for data-pack JSON decoding in reload listeners and registry load tasks,
the **IO workers** for `NbtIo.write` into region files, and the **Netty
threads** for every `StreamCodec` in `PacketEncoder` and `PacketDecoder`.
Nothing here has a tick of its own.

## The trace: one `ItemStack`, three ways

```mermaid
sequenceDiagram
    participant CBE as ChestBlockEntity (server thread)
    participant TVO as TagValueOutput
    participant CH as ContainerHelper
    participant IS as ItemStack.CODEC
    participant NIO as NbtIo (IO worker)
    participant PE as PacketEncoder (Netty)
    participant DCP as DataComponentPatch
    participant IP as ItemParser (server thread)
    participant TP as TagParser

    Note over CBE,NIO: (a) to disk
    CBE->>TVO: saveWithFullMetadata → createWithContext(ProblemReporter, registries) — a RegistryOps over NbtOps
    CBE->>CH: saveAdditional → saveAllItems(output, items)
    CH->>TVO: list("Items", ItemStackWithSlot.CODEC) → TypedOutputList.add per slot
    TVO->>IS: encode — "id" (Item.CODEC_WITH_BOUND_COMPONENTS), "count", "components" (DataComponentPatch.CODEC)
    TVO->>CBE: buildResult → CompoundTag; ScopedCollector.close logs any problem
    CBE->>NIO: SerializableChunkData → RegionFileStorage.write → NbtIo.write
    Note over PE,DCP: (b) to the wire
    PE->>DCP: ItemStack.OPTIONAL_STREAM_CODEC — varint count (0 = empty), Item.STREAM_CODEC id, then DataComponentPatch.STREAM_CODEC
    DCP->>PE: varint added, varint removed, each (type id, value via DataComponentType.streamCodec), then removed ids
    Note over IP,TP: (c) from text
    IP->>TP: /give … [damage=5] → TagParser.create(registryOps).parseAsArgument — SNBT straight into Tag
    IP->>IP: DataComponentType.codecOrThrow.parse(registryOps, tag) → DataComponentPatch.Builder → ItemInput.createItemStack
```

Narrated:

**(a) Disk.** `ItemStack` has no NBT method; there is no *save* or *parse*
on it. `ChestBlockEntity.saveAdditional` receives a `ValueOutput` and calls
`ContainerHelper.saveAllItems`, which opens a typed list under "Items" with
`ItemStackWithSlot.CODEC` — a record of slot plus the stack's `ItemStack.MAP_CODEC`
fields inlined. That map codec writes "id", "count" (defaulting to 1 via
`ExtraCodecs.optionalAlwaysPresentFieldOf`) and "components"
(`DataComponentPatch.CODEC`, removals as `!minecraft:foo`). The
`TagValueOutput` was created by the final shell `BlockEntity.saveWithFullMetadata`
with `TagValueOutput.createWithContext`, so the ops are a `RegistryOps` and
the item id resolves. `BlockEntity.saveWithoutMetadata` adds the block
entity's own "components" (`DataComponentMap.CODEC`) and the metadata
"id", "x", "y", "z". The result joins the chunk's "block_entities",
`NbtUtils.addCurrentDataVersion` stamps the data version, and an IO worker
writes it through `RegionFileStorage.write` with `NbtIo.write` under the
region file's compression (`RegionFileVersion.DEFAULT` is deflate). Load is
the mirror: `BlockEntity.loadStatic` reads "id", `ChestBlockEntity.loadAdditional`
calls `ContainerHelper.loadAllItems` over `ValueInput.listOrEmpty`.

**(b) Wire.** `ClientboundContainerSetSlotPacket` encodes the stack with
`ItemStack.OPTIONAL_STREAM_CODEC`: a varint count where zero means empty and
nothing else follows; `Item.STREAM_CODEC` (a registry id, resolvable because
the buffer is a `RegistryFriendlyByteBuf`); then `DataComponentPatch.STREAM_CODEC`.
`ItemStack.STREAM_CODEC` is the same but refuses an empty stack. Serverbound
is different: `ServerboundSetCreativeModeSlotPacket` uses
`ItemStack.validatedStreamCodec` over `ItemStack.OPTIONAL_UNTRUSTED_STREAM_CODEC`,
where `DataComponentPatch.DELIMITED_STREAM_CODEC` length-prefixes every
component value and the decoded stack is re-encoded through `ItemStack.CODEC`
to prove the persistent codec would accept it. Everything here runs on a
Netty thread inside `PacketEncoder` and `PacketDecoder`.

**(c) Text.** `GiveCommand` asks `ItemArgument` for an `ItemInput`.
`ItemParser` holds a `RegistryOps` over `NbtOps.INSTANCE` and a `TagParser`
created *for that ops*, so `[damage=5]` is parsed by `TagParser.parseAsArgument`
directly into a `Tag`, then each component's `DataComponentType.codecOrThrow`
parses it — the same codec the chunk file used — into a
`DataComponentPatch.Builder`. Data packs are the JSON twin:
`SimpleJsonResourceReloadListener.scanDirectory` and
`ResourceManagerRegistryLoadTask` build a `RegistryOps` over `JsonOps` and
parse with `StrictJsonParser`; an `ItemStack` in a loot table goes through
`ItemStack.CODEC` exactly as on disk. One codec, three formats.

## Interfaces

- **Called by:** every `BlockEntity` and `Entity` save (`BlockEntity.saveAdditional`,
  `BlockEntity.loadAdditional`, `Entity.saveWithoutId`, `Entity.load`),
  `PlayerDataStorage`, `LevelStorageSource` for `level.dat`, `SavedData`
  via `SavedDataType`; every packet's static stream codec; every command
  argument that parses NBT (`CompoundTagArgument`, `NbtTagArgument`,
  `NbtPathArgument`, `ItemArgument`).
- **Calls into:** registries for `RegistryOps`
  ([identifiers-and-registries](identifiers-and-registries.md)); the
  component types for their codecs ([data-components](data-components.md));
  the resource system for files ([resource-system](resource-system.md)).
- **Crosses the network as:** everything — but two ways. Structured data
  is `StreamCodec` fields; opaque data is NBT via `ByteBufCodecs.TAG`
  (clientbound gets `ByteBufCodecs.TRUSTED_TAG`, an unlimited
  `NbtAccounter`; serverbound gets the 2 MiB default). A `Codec` reaches the
  wire only through `ByteBufCodecs.fromCodec` or
  `ByteBufCodecs.fromCodecWithRegistries` — NBT inside the packet.
- **Data-driven by:** nothing; this is the layer the data goes through.
  The save format's *migration* is `DataFixTypes` — the enum of every kind
  of file the game owns (`DataFixTypes.CHUNK`, `DataFixTypes.PLAYER`, `DataFixTypes.LEVEL`, `DataFixTypes.OPTIONS` …), each
  calling `DataFixTypes.updateToCurrentVersion` on the DFU `DataFixer` from
  `DataFixers.getDataFixer` before the codec sees the tag. The fixes
  themselves (`util/datafix`) are out of scope by rule 3.

## Invariants and surprises

- **`Tag` is sealed and the leaves are records.** `IntTag` is a record of
  one int; the old *getAsInt* family is gone and `Tag.asInt`, `Tag.asString`
  etc. return `Optional`. On `CompoundTag`, `CompoundTag.getInt` is
  `Optional` and `CompoundTag.getIntOr` is the defaulted form;
  `CompoundTag.get` is still nullable; the two-argument *contains* with a
  type id no longer exists.
- **Save code never sees a `CompoundTag`.** `BlockEntity.saveAdditional`
  and `Entity` take `ValueOutput`; the `CompoundTag`-returning methods on
  `BlockEntity` are final shells that build a `TagValueOutput`. A codec
  failure inside a save is a logged problem path, never an exception in the
  tick — `TagValueOutput.EncodeToFieldFailedProblem` and its siblings.
- **Registry context is not optional.** `TagValueOutput.createWithoutContext`
  exists and is rare; almost every real codec resolves a `Holder`
  somewhere and fails on plain `NbtOps.INSTANCE`.
- **`TagParser` is generic over its output.** SNBT can decode into any
  `DynamicOps` target without going through a `CompoundTag` first;
  `TagParser.parseCompoundFully` is the plain-string entry point.
  `TagParser.FLATTENED_CODEC` and `TagParser.LENIENT_CODEC` let a JSON
  field hold SNBT text or an object interchangeably.
- **Mixed-type lists are legal.** `NbtOps` list collectors append whatever
  they are given; `ListTag.addAndUnwrap` strips the legacy single-key
  wrapper on read and nothing writes it.
- **"Trusted" means clientbound.** `ByteBufCodecs.TAG` versus
  `ByteBufCodecs.TRUSTED_TAG` differ only in the `NbtAccounter`; the
  structural defence — delimiting and re-validation — is applied to exactly
  one serverbound packet, the creative slot.
- **`RegistryFriendlyByteBuf` is a play-phase decorator.** Configuration
  packets have no registry context, which is why registry data and tags
  are sent as NBT and ids in that phase and why `ByteBufCodecs.holder`
  codecs are play-only.
- **Region compression is per file.** `RegionFileVersion` selects deflate
  by default and also knows GZIP, LZ4 and none; `NbtIo.writeCompressed` (GZIP)
  is for standalone files like `level.dat` and player data.

## Where to look

`ExtraCodecs` · `RegistryOps` · `HolderLookup.Provider.createSerializationContext` ·
`Tag` · `CompoundTag` · `ListTag` · `NbtIo` · `NbtAccounter` · `NbtOps` ·
`TagParser` · `SnbtGrammar` · `ValueOutput` · `ValueInput` ·
`TagValueOutput` · `TagValueInput` · `ProblemReporter` · `BlockEntity` (the
save shells) · `ContainerHelper` · `ItemStackWithSlot` · `ItemStack` (the
codec fields) · `StreamCodec` · `ByteBufCodecs` · `FriendlyByteBuf` ·
`RegistryFriendlyByteBuf` · `PacketEncoder` · `ItemParser` · `DataFixTypes`

---

*Rules: names, never code · how the system works, not how the code reads ·
newest version only · every backticked name passes `tools/verify_names.py`.*
