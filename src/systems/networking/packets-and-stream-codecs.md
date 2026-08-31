# Packets and stream codecs

> Verified against **Minecraft 26.2** · Part IX · one packet, from three fields on a record to bytes in a frame and back again.

## Responsibility

A packet is the unit of everything the two sides say to each other. This
page is about the *machinery*: what a packet class has to declare, how
its fields become bytes, how the receiving side knows which class to
build, and what stops a hostile sender from allocating a gigabyte. The
catalogue of which packets exist is generated — see
[reference/packets.md](../../reference/packets.md), 225 packet types
across eight declaring classes.

The one sentence: *every message is a small immutable value, and a
`StreamCodec` is the function that turns it into bytes.*

The headline for a 1.21-era reader: **`Packet` no longer knows how to
write itself.** There is no *write* method on the interface.
Serialisation is a *STREAM_CODEC* static field that the *protocol* reads,
not something the packet is obliged to have — and a packet's numeric id
is written down nowhere. It is the position of that packet in a fluent
registration chain.

## The data it owns

### The contract

`Packet` is an interface with four methods and nothing else:

- **`Packet.type`** — returns a `PacketType`, always a constant from one
  of the eight `*PacketTypes` classes.
- **`Packet.handle`** — hands the packet to exactly one named method on the
  phase's listener interface.
- **`Packet.isSkippable`** — default false. True for the chat-shaped
  packets (`ClientboundSystemChatPacket`,
  `ClientboundPlayerChatPacket`, `ClientboundDisguisedChatPacket`,
  `ClientboundPlayerCombatKillPacket`, `ClientboundTagQueryPacket`):
  a failure to encode one is dropped rather than fatal.
- **`Packet.isTerminal`** — default false. True for exactly eight
  packets, the ones that end a protocol phase:
  `ClientIntentionPacket`, `ClientboundLoginFinishedPacket`,
  `ServerboundLoginAcknowledgedPacket`,
  `ClientboundFinishConfigurationPacket`,
  `ServerboundFinishConfigurationPacket`,
  `ClientboundStartConfigurationPacket`,
  `ServerboundConfigurationAcknowledgedPacket` and
  `ServerboundResourcePackPacket`. What that flag *does* to the pipeline
  is [the connection](the-connection.md)'s business.

There is also a static `Packet.codec`, which is `StreamCodec.ofMember`
under a friendlier name.

**`PacketType` is a record of two things** — a `PacketFlow` and an
`Identifier`. A direction and a name; *no number*. `PacketFlow` is the
two-constant enum `PacketFlow.SERVERBOUND` / `PacketFlow.CLIENTBOUND`,
with `PacketFlow.getOpposite` and `PacketFlow.id`.

Two shapes of packet class coexist. The modern one is a record whose
*STREAM_CODEC* is a `StreamCodec.composite` naming each component's codec
and accessor — `ClientboundSystemChatPacket` is one. The older one is a
plain class with a private buffer constructor and a private write method,
joined by `Packet.codec`; `ServerboundSwingPacket`,
`ClientboundKeepAlivePacket` and `ClientboundSetHealthPacket` are these.
`StreamMemberEncoder` exists solely so that second form can bind a
member reference.

### The codec layer

`net/minecraft/network/codec` is small and does all the work.

- **`StreamCodec`** — one interface extending `StreamEncoder` and
  `StreamDecoder`, so `StreamDecoder.decode` takes a buffer and returns a
  value and `StreamEncoder.encode` takes a buffer and a value.
- The constructors and combinators: `StreamCodec.of`,
  `StreamCodec.ofMember`, `StreamCodec.unit`, `StreamCodec.map`,
  `StreamCodec.mapStream`, `StreamCodec.apply`, `StreamCodec.dispatch`,
  `StreamCodec.recursive`, `StreamCodec.cast`, and
  **`StreamCodec.composite` in twelve arities** — one through twelve
  pairs of (codec, getter) plus a constructor. Fields encode and decode
  strictly in argument order, and that ordering *is* the format
  specification. `StreamCodec.CodecOperation` is the functional
  interface that lets `StreamCodec.apply` read left to right.
  `StreamCodec.dispatch` is how registry-dispatched values travel —
  `ConsumeEffect.STREAM_CODEC`, `SlotDisplay.STREAM_CODEC` and
  `RecipeDisplay.STREAM_CODEC` are built with it.
- **`ByteBufCodecs`** — the primitive library. SCREAMING\_CASE constants
  for fixed things (`ByteBufCodecs.BOOL`, `ByteBufCodecs.BYTE`, `ByteBufCodecs.SHORT`,
  `ByteBufCodecs.UNSIGNED_SHORT`, `ByteBufCodecs.INT`, `ByteBufCodecs.VAR_INT`, `ByteBufCodecs.LONG`, `ByteBufCodecs.VAR_LONG`, `ByteBufCodecs.FLOAT`,
  `ByteBufCodecs.DOUBLE`, `ByteBufCodecs.BYTE_ARRAY`, `ByteBufCodecs.LONG_ARRAY`, `ByteBufCodecs.STRING_UTF8`, `ByteBufCodecs.TAG`,
  `ByteBufCodecs.COMPOUND_TAG`, `ByteBufCodecs.VECTOR3F`, `ByteBufCodecs.QUATERNIONF`, `ByteBufCodecs.CONTAINER_ID`,
  `ByteBufCodecs.GAME_PROFILE`, `ByteBufCodecs.GAME_PROFILE_PROPERTIES`, `ByteBufCodecs.PLAYER_NAME`, `ByteBufCodecs.RGB_COLOR`)
  and lowerCamel factories for parameterised ones
  (`ByteBufCodecs.stringUtf8`, `ByteBufCodecs.byteArray`, `ByteBufCodecs.optional`, `ByteBufCodecs.collection`,
  `ByteBufCodecs.list`, `ByteBufCodecs.map`, `ByteBufCodecs.either`, `ByteBufCodecs.lengthPrefixed`, `ByteBufCodecs.idMapper`, `ByteBufCodecs.registry`,
  `ByteBufCodecs.holder`, `ByteBufCodecs.holderRegistry`, `ByteBufCodecs.holderSet`, `ByteBufCodecs.lenientJson`). Two worth
  naming: `ByteBufCodecs.ROTATION_BYTE` is one byte that means a degree,
  and `ByteBufCodecs.OPTIONAL_VAR_INT` spends zero for absent and
  value-plus-one otherwise.
- **`IdDispatchCodec`** — the one that makes a protocol out of a pile of
  codecs. It holds a list of serialisers and a type-to-int map, writes a
  var-int id and delegates. `IdDispatchCodec.DontDecorateException` is
  the marker that says "rethrow me as I am, do not wrap me".

The bridge to the disk and JSON codecs of
[codecs, NBT and JSON](../foundations/codecs-nbt-json.md) is
`ByteBufCodecs.fromCodec` and its relatives: a `Codec` becomes a
`StreamCodec` by serialising through NBT. There are trusted and untrusted
variants; see *Invariants*.

### The buffers

`FriendlyByteBuf` is a `ByteBuf` decorator with a hundred convenience
readers and writers — `FriendlyByteBuf.readVarInt`,
`FriendlyByteBuf.writeUtf`, `FriendlyByteBuf.readIdentifier`,
`FriendlyByteBuf.writeResourceKey`, `FriendlyByteBuf.readNbt`,
`FriendlyByteBuf.readCollection`, `FriendlyByteBuf.readEnumSet`,
`FriendlyByteBuf.readBlockPos`, `FriendlyByteBuf.readBlockHitResult`,
`FriendlyByteBuf.readWithCodec` and so on. It holds the two length
constants `FriendlyByteBuf.MAX_STRING_LENGTH` and
`FriendlyByteBuf.MAX_COMPONENT_STRING_LENGTH`.

**`RegistryFriendlyByteBuf`** extends it and adds exactly one field: a
`RegistryAccess`, behind `RegistryFriendlyByteBuf.registryAccess`. It
exists because a numeric registry id means nothing on its own — item
number 37 is only an item relative to the registry set the server sent
during configuration ([identifiers and
registries](../foundations/identifiers-and-registries.md)). Every codec
that writes a registry id needs one: `ByteBufCodecs.registry`,
`ByteBufCodecs.holderRegistry`, `ByteBufCodecs.holder`,
`ByteBufCodecs.holderSet`, `ByteBufCodecs.fromCodecWithRegistries`,
`ByteBufCodecs.registryFriendlyLengthPrefixed` — and therefore
`ItemStack.STREAM_CODEC`, `DataComponentPatch.STREAM_CODEC`
([data components](../foundations/data-components.md)),
`ComponentSerialization.STREAM_CODEC` and `HashedStack.STREAM_CODEC`.

The low-level encodings live in `VarInt`, `VarLong`, `Utf8String` and
`LpVec3`, a quantised position used by `Vec3.LP_STREAM_CODEC`.

### The protocol description

`ProtocolInfo` is what a configured connection actually holds:
`ProtocolInfo.id` (a `ConnectionProtocol`), `ProtocolInfo.flow`,
`ProtocolInfo.codec` — a *single* `StreamCodec` for the whole phase —
and a nullable `ProtocolInfo.bundlerInfo`.
`ProtocolInfo.DetailsProvider` and `ProtocolInfo.Details` exist so
tooling can enumerate a phase; `ProtocolInfo.Details.PacketVisitor` is
handed each `PacketType` with its network id.

It is built by `ProtocolInfoBuilder`, whose
`ProtocolInfoBuilder.addPacket` and
`ProtocolInfoBuilder.withBundlePacket` are the registration calls and
whose `ProtocolInfoBuilder.buildUnbound` yields an `UnboundProtocol` or
`SimpleUnboundProtocol` — a protocol that knows everything except which
buffer type to wrap the bytes in. `UnboundProtocol.bind` supplies that.
`ProtocolCodecBuilder` is the inner layer that talks to
`IdDispatchCodec`, and `CodecModifier` is the hook for a codec whose
behaviour depends on the connection.

## When it runs

Encoding and decoding both run **on the Netty event loop**, inside
`PacketEncoder` and `PacketDecoder` — never on a game thread. By the time
`Packet.handle` is called the object is fully built; by the time
`PacketEncoder` sees a packet the sending thread has already let go of
it. The handoff in each direction is
[the connection](the-connection.md)'s subject.

The protocol descriptions themselves are built **once, at class-load**,
for the phases that need no registries — handshaking, status, login and
configuration bind their buffers eagerly — and **per connection at the
configuration-to-play transition** for the play phase, because that is
the first moment a `RegistryAccess` exists to bind against.

## The trace: a block update becomes bytes

```mermaid
sequenceDiagram
    participant CH as ChunkHolder
    participant CN as Connection
    participant PE as PacketEncoder
    participant IDC as IdDispatchCodec
    participant SC as (the packet's STREAM_CODEC)
    participant PD as PacketDecoder
    participant CPL as ClientPacketListener

    CH->>CN: send(ClientboundBlockUpdatePacket) — a value, no bytes yet
    CN->>PE: the packet reaches the "encoder" handler
    PE->>IDC: codec().encode — one codec for the whole phase
    IDC->>IDC: type to int, VarInt.write — the id is a registration index
    IDC->>SC: delegate; mapStream wraps the output in a fresh RegistryFriendlyByteBuf
    SC->>SC: BlockPos.STREAM_CODEC, then idMapper over Block.BLOCK_STATE_REGISTRY
    PE-->>PD: "prepender" writes the frame length; "splitter" reassembles it
    PD->>IDC: codec().decode — read the id, bounds-check it
    IDC->>SC: build the value
    PD->>PD: the buffer must now be empty, or it is a protocol error
    PD->>CPL: handle, then a hop to the client main thread
```

Each arrow is a decision.

**`ChunkHolder` sends a value.** Nothing about the packet knows its own
id or its own byte layout. It is three fields.

**One codec serves the entire phase.** `ProtocolInfo.codec` is a single
`IdDispatchCodec`, not a table the encoder walks. Encoding looks the
`PacketType` up in a map; a type that was never registered in *this*
protocol is an encoder error naming the unknown packet — which is how a
configuration-phase packet sent during play fails.

**The id is a registration index.** `ProtocolCodecBuilder.add` appends to
a list, and `IdDispatchCodec.Builder.build` walks that list assigning 0,
1, 2 in call order. A packet's wire number is literally its position in
the `ProtocolInfoBuilder.addPacket` chain in `GameProtocols`,
`ConfigurationProtocols`, `LoginProtocols`, `StatusProtocols` or
`HandshakeProtocols`. `ProtocolCodecBuilder.add` also asserts that the
type's `PacketFlow` matches the protocol's, so a clientbound type cannot
be registered into a serverbound protocol.

**`StreamCodec.mapStream` wraps the buffer per call.**
`ProtocolInfoBuilder` applies the buffer decorator —
`RegistryFriendlyByteBuf.decorator` for the play phase — with
`StreamCodec.mapStream`, so a fresh view is constructed around the raw
buffer for every single encode and decode. It is a throwaway, not a
pipeline object.

**Decoding must consume the frame exactly.** `PacketDecoder` checks that
the buffer is empty afterwards and raises an error naming how many extra
bytes it found. A packet that under-reads would otherwise corrupt
nothing visible until much later, so it is caught here.

**Then, and only then, a thread hop.** The listener method's first act is
`PacketUtils.ensureRunningOnSameThread`. Decoding is Netty's; handling is
the game's.

## Interfaces

- **Called by:** every system that sends anything — `ServerEntity`,
  `ChunkHolder`, `PlayerChunkSender`, `AbstractContainerMenu`,
  `ServerGamePacketListenerImpl`, and the client's mirror of each.
- **Calls into:** `IdDispatchCodec`, then the packet's *STREAM_CODEC*,
  then `ByteBufCodecs`, then `FriendlyByteBuf`, then Netty.
- **Crosses the network as:** all of it. This page *is* the crossing.
- **Data-driven by:** nothing. The packet set is code, fixed at compile
  time. The *values* inside packets are frequently registry ids, and
  those are data-driven — which is exactly why
  `RegistryFriendlyByteBuf` has to exist.

Custom payloads are the one extension point: `CustomPacketPayload`, with
`CustomPacketPayload.Type`, `CustomPacketPayload.createType` and
`CustomPacketPayload.codec`, carried by
`ClientboundCustomPayloadPacket` and `ServerboundCustomPayloadPacket`.
An unrecognised payload decodes to `DiscardedPayload`, which keeps the
bytes and does nothing with them. `BrandPayload` is vanilla's own use of
the mechanism.

## Invariants and surprises

- **A packet's number is not written down.** It is the index of its
  `ProtocolInfoBuilder.addPacket` call. Reordering two lines in
  `GameProtocols` renumbers the protocol. Because the *common*, *cookie*
  and *ping* types are registered into several phases, **the same
  `PacketType` has a different number in each phase**.
- **`ClientboundBundlePacket` has a `PacketType` but no wire id.**
  `ProtocolInfoBuilder.withBundlePacket` registers only the *delimiter*,
  `ClientboundBundleDelimiterPacket`, serialised with
  `StreamCodec.unit` — an id and a zero-byte body. A bundle on the wire
  is two empty markers around ordinary packets.
  `PacketBundleUnpacker` explodes an outgoing bundle into
  delimiter-packets-delimiter; `PacketBundlePacker` collects an incoming
  run back up. `BundlerInfo` holds the logic and
  `BundlerInfo.BUNDLE_SIZE_LIMIT` caps it at 4,096 sub-packets.
  `BundleDelimiterPacket.handle` is final and throws — a delimiter must
  never reach a listener. Only the clientbound play protocol declares a
  bundle at all.
- **A bundle's guarantee is atomicity against the client's tick.**
  `ClientPacketListener.handleBundlePacket` hops to the main thread once
  for the whole bundle and then handles the sub-packets inline, so the
  client can never tick or render with half a bundle applied. There are
  only two senders: `ServerEntity.sendPairingData`, so an entity never
  appears mid-initialisation ([what the client is
  told](what-the-client-is-told.md)), and `ServerEntity`'s
  motion-plus-power pair.
- **One packet class may have several codecs.**
  `ClientboundCustomPayloadPacket` declares
  `ClientboundCustomPayloadPacket.GAMEPLAY_STREAM_CODEC` and
  `ClientboundCustomPayloadPacket.CONFIG_STREAM_CODEC`;
  `ClientboundShowDialogPacket` declares
  `ClientboundShowDialogPacket.STREAM_CODEC` and
  `ClientboundShowDialogPacket.CONTEXT_FREE_STREAM_CODEC`. The same
  `PacketType` is registered with the first in `GameProtocols` and the
  second in `ConfigurationProtocols`. Type and encoding are genuinely
  separate things.
- **"Trusted" is a real distinction in the codec library.**
  `ByteBufCodecs.fromCodecTrusted` gives the NBT reader an unlimited heap
  budget; plain `ByteBufCodecs.fromCodec` gives it the default quota.
  Hence the pairs `ByteBufCodecs.TAG` / `ByteBufCodecs.TRUSTED_TAG`,
  `ByteBufCodecs.COMPOUND_TAG` /
  `ByteBufCodecs.TRUSTED_COMPOUND_TAG`, and
  `ComponentSerialization.STREAM_CODEC` /
  `ComponentSerialization.TRUSTED_STREAM_CODEC`. The rule is direction:
  the server wrote it, so the client may trust it.
- **Exactly one packet lets a client hand the server an arbitrary item,
  and it is fenced three ways.**
  `ServerboundSetCreativeModeSlotPacket` uses
  `ItemStack.OPTIONAL_UNTRUSTED_STREAM_CODEC`, which differs from the
  ordinary one only in using
  `DataComponentPatch.DELIMITED_STREAM_CODEC` — every individual
  component's payload is length-prefixed, so one component that fails to
  decode can be skipped without desynchronising the rest of the stack.
  That is wrapped in `ItemStack.validatedStreamCodec`, which re-encodes
  the decoded stack against `NullOps` purely to validate it. And the
  packet carries `GameProtocols.HAS_INFINITE_MATERIALS`, a
  `CodecModifier` that throws `SkipPacketDecoderException` when the
  connection is not in creative — the packet is rejected *in the
  decoder*, before any handler exists to be fooled.
- **Container clicks send hashes, not items.**
  `ServerboundContainerClickPacket` carries `HashedStack` — either
  `HashedStack.EMPTY` or `HashedStack.ActualItem`, with an item holder, a
  count and a `HashedPatchMap` of component type to int. The server
  compares with `HashedStack.matches`. Client-supplied component
  *contents* never cross the wire at all; see
  [containers and menus](../items/containers-and-menus.md).
- **`SkipPacketException` is a marker, and skipping means draining.**
  `SkipPacketEncoderException` and `SkipPacketDecoderException`
  implement it and `IdDispatchCodec.DontDecorateException`.
  `PacketEncoder` turns a failure on a `Packet.isSkippable` packet into
  one, so a malformed chat message does not kill the connection;
  `PacketDecoder` reacts by skipping the rest of the frame so the byte
  stream stays aligned.
- **The frame limit does most of the security work.** A frame length is
  at most three var-int bytes — `Varint21FrameDecoder` rejects a wider
  prefix outright, and a zero length too. On top of that
  `ByteBufCodecs.MAX_INITIAL_COLLECTION_SIZE` clamps the *allocation* of
  a decoded collection to 65,536 entries even when the declared cap is
  unbounded, so a hostile count cannot force a huge array up front.
  `ByteBufCodecs.lengthPrefixed` goes further and hands the inner codec a
  slice, so it physically cannot read past its own region.
- **`FriendlyByteBuf.readCollection` has no cap.** Unlike
  `ByteBufCodecs.collection` it applies its constructor to the raw
  decoded count; only the frame limit bounds it. A packet written the
  modern way is safer than a packet written the old way, and the old way
  is still in the tree.

The limits in one table:

| limit | value | where |
|---|---|---|
| frame length prefix | three var-int bytes | `Varint21FrameDecoder` |
| compressed frame | 2 MiB | `CompressionDecoder.MAXIMUM_COMPRESSED_LENGTH` |
| decompressed frame | 8 MiB | `CompressionDecoder.MAXIMUM_UNCOMPRESSED_LENGTH` |
| default string | 32,767 chars | `FriendlyByteBuf.MAX_STRING_LENGTH` |
| component as string | 262,144 | `FriendlyByteBuf.MAX_COMPONENT_STRING_LENGTH` |
| player name | 16 | `ByteBufCodecs.PLAYER_NAME` |
| collection allocation | 65,536 | `ByteBufCodecs.MAX_INITIAL_COLLECTION_SIZE` |
| sub-packets in a bundle | 4,096 | `BundlerInfo.BUNDLE_SIZE_LIMIT` |
| slots in one click | 128 | `ServerboundContainerClickPacket.MAX_SLOT_COUNT` |
| var-int / var-long | 5 / 10 bytes | `VarInt.read`, `VarLong.read` |

## Where to look

`Packet` · `PacketType` · `PacketFlow` · `StreamCodec` · `ByteBufCodecs`
· `IdDispatchCodec` · `ProtocolInfo` · `ProtocolInfoBuilder` ·
`GameProtocols` · `GamePacketTypes` · `FriendlyByteBuf` ·
`RegistryFriendlyByteBuf` · `PacketEncoder` · `PacketDecoder` ·
`BundlerInfo` · `PacketBundlePacker` · `CustomPacketPayload` ·
`HashedStack`

---

*Rules: names, never code · how the system works, not how the code reads ·
newest version only · every backticked name passes `tools/verify_names.py`.*
