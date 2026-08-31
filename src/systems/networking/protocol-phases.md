# Protocol phases

> Verified against **Minecraft 26.2** · Part IX · a login: from clicking a server in the list to standing in the world.

## Responsibility

One TCP connection speaks four different languages in sequence. This page
is about the state machine that decides which — what each phase is for,
which packet moves the connection to the next one, and what the
configuration phase does with the time it takes.

The one sentence a player would recognise: *the loading bar between
"Connecting to the server" and being able to move.*

The headline for a 1.21-era reader: **almost none of a login runs on the
main thread.** The whole server-side login listener runs on the Netty
event loop, and the thing that actually advances it is a tick. And the
`ServerPlayer` — the object, its save data, its spawn position and its
spawn chunks — is built during **configuration**, by a task, before the
play phase begins.

## The data it owns

`ConnectionProtocol` is a bare enum of five constants —
`ConnectionProtocol.HANDSHAKING`, `ConnectionProtocol.STATUS`,
`ConnectionProtocol.LOGIN`, `ConnectionProtocol.CONFIGURATION`,
`ConnectionProtocol.PLAY` — each carrying a string
`ConnectionProtocol.id`. There is no number, no packet table, no
*getById*. It is a label, and everything else lives elsewhere: the codec
in a `ProtocolInfo`, the behaviour in a `PacketListener`.

| phase | serverbound listener | clientbound listener | `ProtocolInfo` |
|---|---|---|---|
| `ConnectionProtocol.HANDSHAKING` | `ServerHandshakePacketListenerImpl`, or `MemoryServerHandshakePacketListenerImpl` in singleplayer | *none — there is no clientbound handshake protocol* | `HandshakeProtocols.SERVERBOUND`, one packet |
| `ConnectionProtocol.STATUS` | `ServerStatusPacketListenerImpl` | reached from `ServerStatusPinger` | `StatusProtocols.SERVERBOUND` binds a **raw buffer**; `StatusProtocols.CLIENTBOUND` a `FriendlyByteBuf` |
| `ConnectionProtocol.LOGIN` | `ServerLoginPacketListenerImpl` | `ClientHandshakePacketListenerImpl` | `LoginProtocols.SERVERBOUND` / `LoginProtocols.CLIENTBOUND` |
| `ConnectionProtocol.CONFIGURATION` | `ServerConfigurationPacketListenerImpl` | `ClientConfigurationPacketListenerImpl` | `ConfigurationProtocols.SERVERBOUND` / `ConfigurationProtocols.CLIENTBOUND` |
| `ConnectionProtocol.PLAY` | `ServerGamePacketListenerImpl` | `ClientPacketListener` | **not pre-bound** — `GameProtocols.SERVERBOUND_TEMPLATE` and `GameProtocols.CLIENTBOUND_TEMPLATE` are bound per connection |

The first four bind their buffers once, at class load, because they need
no registries. The play phase cannot: its codecs write registry ids, so
they are bound per connection with
`RegistryFriendlyByteBuf.decorator` at the configuration-to-play switch,
once the client and server agree on what the registries contain.

`ServerCommonPacketListenerImpl` is the shared base of the server's
configuration and play listeners, and holds everything that is legal in
both: keep-alive, latency, custom payloads, resource-pack responses,
cookies and the flush suspension. `ClientCommonPacketListenerImpl` is
its client counterpart. That inheritance is why the *common* packets in
[reference/packets.md](../../reference/packets.md) belong to no single
phase.

The state carried across a phase change is a `CommonListenerCookie` —
on the server a small record of profile, latency, client information and
a transferred flag; on the client a much larger one carrying registries,
feature flags, cookies, chat state and the server brand.

## When it runs

Handshake, status and login are handled **on the Netty event loop** and
never hop. `ServerLoginPacketListenerImpl` contains no thread hop at all,
which is why its `ServerLoginPacketListenerImpl.state` field is volatile.

What advances the login is `ServerLoginPacketListenerImpl.tick`, reached
from `MinecraftServer.tickConnection` through
`ServerConnectionListener.tick` and `Connection.tick`. It is also where
`ServerLoginPacketListenerImpl.MAX_TICKS_BEFORE_LOGIN` — thirty seconds
— is enforced.

Configuration is mixed: the client-information and code-of-conduct
handlers stay on the event loop, while everything that touches the world
hops to the main thread. `ServerConfigurationPacketListenerImpl.tick`
runs each tick to drive the current `ConfigurationTask` and keep the
spawn chunks loaded.

There are two background threads per login: the server starts a bare
thread named for user authentication to call the session service, and the
client uses its IO pool for the matching call.

## The trace: a login

```mermaid
sequenceDiagram
    participant CH as ClientHandshakePacketListenerImpl
    participant SL as ServerLoginPacketListenerImpl
    participant AUTH as (User Authenticator thread)
    participant SC as ServerConfigurationPacketListenerImpl
    participant CC as ClientConfigurationPacketListenerImpl
    participant PST as PrepareSpawnTask
    participant PL as PlayerList

    CH->>SL: ClientIntentionPacket — version, host, ClientIntent.LOGIN
    CH->>SL: ServerboundHelloPacket — name and profile id, sent immediately
    SL->>CH: ClientboundHelloPacket — RSA public key and a four-byte challenge
    CH->>SL: ServerboundKeyPacket — AES secret and the challenge, RSA-encrypted
    SL->>SL: setEncryptionKey now, before anyone is authenticated
    SL->>AUTH: hasJoinedServer on a fresh thread
    AUTH->>SL: authenticatedProfile; state becomes VERIFYING
    SL->>SL: tick on the server thread: bans, whitelist, compression, duplicates
    SL->>CH: ClientboundLoginFinishedPacket — terminal, LOGIN ends
    CH->>SC: ServerboundLoginAcknowledgedPacket — terminal
    SC->>CC: brand, server links, feature flags, then the task queue
    SC->>CC: SynchronizeRegistriesTask — known packs, registries, tags
    SC->>PST: PrepareSpawnTask — build the ServerPlayer, load its chunks
    SC->>CC: ClientboundFinishConfigurationPacket — terminal
    CC->>SC: ServerboundFinishConfigurationPacket — terminal
    PST->>PL: placeNewPlayer with an already-built player
    PL->>CC: ClientboundLoginPacket, and the world appears
```

Each arrow is a decision.

**The client sends its hello without waiting.** After the intention
packet it immediately sends `ServerboundHelloPacket`; there is no round
trip in between.

**Three branches out of the hello.** If the name matches the
singleplayer profile, verification starts at once with no encryption. If
the server uses authentication and this is not a memory connection, it
goes to the encryption handshake. Otherwise — offline mode — the profile
is minted from the name by `UUIDUtil.createOfflineProfile` and nothing is
encrypted.

**Encryption is set up before authentication finishes.** The client
generates the AES secret, computes a digest over the server id, the
secret and the server's public key, RSA-encrypts the secret and the
challenge with the server's key, and sends them. The server validates the
challenge, recovers the secret, recomputes the same digest, and installs
the ciphers *immediately* — then starts the session-service call. An
unauthenticated connection is already encrypted.

**Authentication is a plain thread that does almost nothing.** It calls
the session service and, on success, stores the profile and flips the
state to `ServerLoginPacketListenerImpl.State.VERIFYING`. Nothing else.

**The tick does the real login.**
`ServerLoginPacketListenerImpl.verifyLoginAndFinishConnectionSetup` runs
on the server thread: `PlayerList.canPlayerLogin` for bans, whitelist and
capacity; the intended-profile check from
`Connection.getIntendedProfileId`; compression; and
`PlayerList.disconnectAllPlayersWithProfile` for a duplicate login — after
which the state machine waits for the old connection to actually die
before continuing.

**Login ends with a terminal packet in each direction.**
`ClientboundLoginFinishedPacket` then `ServerboundLoginAcknowledgedPacket`,
and in between each side installs the configuration codecs. Because both
are terminal, the codecs tear themselves out of the pipeline as they pass
— see [the connection](the-connection.md).

**The configuration task queue is strictly serial.**
`ServerConfigurationPacketListenerImpl.startConfiguration` sends three
things outside the queue — the server's `BrandPayload`,
`ClientboundServerLinksPacket` if there are links, and
`ClientboundUpdateEnabledFeaturesPacket` — then queues, in order:
`SynchronizeRegistriesTask`, a code-of-conduct task if the server has
one, a resource-pack task if it has one, `PrepareSpawnTask`, and
`JoinWorldTask`. Each finishes before the next begins.

**`PrepareSpawnTask` is where the player is born.** It reads the save
file, resolves a spawn position, takes a chunk ticket at
`PrepareSpawnTask.PREPARE_CHUNK_RADIUS` and waits for the chunks — which
is what `ConfigurationTask.tick` exists for. Only when they are ready
does `PrepareSpawnTask.spawnPlayer` construct the `ServerPlayer`, load
it, and hand it to `PlayerList.placeNewPlayer`. See
[players and sessions](../server/players-and-sessions.md), which owns
the rest of that story.

## Registry and tag sync

`SynchronizeRegistriesTask` is the reason configuration exists.

It begins by sending `ClientboundSelectKnownPacks` — a list of
`KnownPack` records naming every pack the server's resource manager has,
by namespace, id and version. The client matches them against its own
bundled vanilla repository through `KnownPacksManager.trySelectingPacks`
and replies with the subset it recognises.

The server then sends one `ClientboundRegistryDataPacket` **per
registry**, walking `RegistryDataLoader.SYNCHRONIZED_REGISTRIES`. Each
element becomes a `RegistrySynchronization.PackedRegistryEntry` whose
data is **omitted** when the element came from a pack the client already
has — that is the entire point of the negotiation. Elements are written
as NBT with each registry's own element codec.

Then one `ClientboundUpdateTagsPacket` covering **all** registries,
static ones included ([tags](../foundations/tags.md)).

On the client, `RegistryDataCollector` accumulates the contents and the
tags and only resolves them at
`ClientConfigurationPacketListenerImpl.handleConfigurationFinished`,
loading them on a background executor against the negotiated packs and
then constructing the `ClientPacketListener` with the finished
`RegistryAccess`. In singleplayer the result is narrowed to the server's
own objects, so both sides share instances.

## Interfaces

- **Called by:** `ServerConnectionListener` on accept; `ConnectScreen` on
  the client, which resolves the address and opens the socket on its own
  thread.
- **Calls into:** `Connection.setupInboundProtocol` and
  `Connection.setupOutboundProtocol` at every transition;
  `PlayerList.placeNewPlayer` at the end.
- **Crosses the network as:** `ClientIntentionPacket`,
  `ServerboundHelloPacket`, `ClientboundHelloPacket`,
  `ServerboundKeyPacket`, `ClientboundLoginCompressionPacket`,
  `ClientboundLoginFinishedPacket`,
  `ServerboundLoginAcknowledgedPacket`, `ClientboundSelectKnownPacks`,
  `ServerboundSelectKnownPacks`, `ClientboundRegistryDataPacket`,
  `ClientboundUpdateTagsPacket`,
  `ClientboundUpdateEnabledFeaturesPacket`,
  `ClientboundCodeOfConductPacket`,
  `ServerboundAcceptCodeOfConductPacket`,
  `ClientboundResourcePackPushPacket`,
  `ServerboundResourcePackPacket`,
  `ClientboundFinishConfigurationPacket`,
  `ServerboundFinishConfigurationPacket`, and for a reconfigure
  `ClientboundStartConfigurationPacket` /
  `ServerboundConfigurationAcknowledgedPacket`.
- **Data-driven by:** the server properties (online mode, compression
  threshold, transfers), the resource-pack settings, and the data packs,
  whose content is precisely what registry sync has to ship.

## Invariants and surprises

- **The server's login handler never touches the main thread, and the
  main thread is what finishes the login.** Packet handlers run on the
  event loop and only set a volatile state; the ban check, the
  compression switch and the finish packet all happen on the next tick.
  A 1.21-era assumption that "packet handlers run on the game thread" is
  exactly backwards here.
- **The connection is encrypted before it is authenticated.** The server
  installs both ciphers while handling the key packet, before the session
  service has been asked anything.
- **The `ServerPlayer` is created by a `ConfigurationTask`,** and so is
  the spawn-chunk load. `PlayerList.placeNewPlayer` receives a finished,
  loaded, positioned player and only wires it up. See
  [players and sessions](../server/players-and-sessions.md).
- **A reconfigure does not re-run configuration.**
  `ServerGamePacketListenerImpl.switchToConfig` sends the client back,
  but `ServerGamePacketListenerImpl.handleConfigurationAcknowledged`
  installs a listener **without** calling
  `ServerConfigurationPacketListenerImpl.startConfiguration`. No
  registries, tags, feature flags or brand are re-sent; the player parks
  in configuration with an empty queue until
  `ServerConfigurationPacketListenerImpl.returnToWorld` is called, which
  queues only the spawn and join tasks. In vanilla the only caller of
  either is `DebugConfigCommand`.
- **Any mismatch in the known-pack negotiation collapses to nothing.**
  If the client's reply is not exactly the requested list, the server
  discards the negotiation entirely and re-sends every registry element
  in full. It is all or nothing, not a per-pack intersection.
- **`ClientboundResetChatPacket` is registered and handled but never
  sent.** Nothing in vanilla constructs it.
- **`ServerLoginPacketListenerImpl.State.NEGOTIATING` is declared and
  never assigned.** The custom-query negotiation path is vestigial:
  `ClientboundCustomQueryPacket` decodes every payload as
  `DiscardedQueryPayload`, and an unexpected answer just disconnects.
- **The creative-inventory packet is filtered at the codec,
  asymmetrically.** The server binds `GameProtocols.Context` to
  `ServerGamePacketListenerImpl`, which answers
  `GameProtocols.Context.hasInfiniteMaterials` from the real player; the
  client's own context answers true unconditionally. So
  `ServerboundSetCreativeModeSlotPacket` is rejected in the decoder, on
  the receiving end only ([packets and stream
  codecs](packets-and-stream-codecs.md)).
- **Compression is enabled asymmetrically.** The server validates that a
  compressed frame really was above the threshold; the client does not.
- **A transfer carries cookies.** `ClientboundTransferPacket` sends the
  client to another server, which sees a `ClientIntent.TRANSFER`
  handshake and a transferred flag in its cookie; the cookies stored by
  `ClientboundStoreCookiePacket` survive the hop, which is how a proxy
  keeps state across servers.
- **Chat session keys are not part of login.** They are negotiated in the
  play phase, after the client learns the server's mode from
  `ClientboundLoginPacket`. See [chat and signing](chat-and-signing.md).

## Where to look

`ConnectionProtocol` · `ProtocolInfo` · `ServerHandshakePacketListenerImpl`
· `ServerLoginPacketListenerImpl` · `ServerConfigurationPacketListenerImpl`
· `ClientHandshakePacketListenerImpl` ·
`ClientConfigurationPacketListenerImpl` · `ConfigurationTask` ·
`SynchronizeRegistriesTask` · `PrepareSpawnTask` · `JoinWorldTask` ·
`RegistrySynchronization` · `KnownPack` · `Crypt` ·
`ServerCommonPacketListenerImpl` · `CommonListenerCookie`

---

*Rules: names, never code · how the system works, not how the code reads ·
newest version only · every backticked name passes `tools/verify_names.py`.*
