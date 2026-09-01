# The connection

> Verified against **Minecraft 26.2** · Part IX · bytes land on a socket; some milliseconds later a method runs on the game thread.

## Responsibility

`Connection` is the object either side holds when it is talking to the
other. It is a Netty channel handler — the last one in the pipeline — and
its job is to own the pipeline, own the current `PacketListener`, get
outbound packets onto the wire and get inbound packets off the event loop
and onto the thread that is allowed to touch the game.

The one sentence a player would recognise: *this is the thing that says
"Timed out" and "Connection lost".*

The headline for a 1.21-era reader: **packets no longer ride the game's
task executor.** There is a dedicated `PacketProcessor` queue, drained in
its own phase before the tick, on both the client and the server. And
**singleplayer still serialises every packet** — the local pipeline
swaps the framing and drops the ciphers, but `PacketEncoder` and
`PacketDecoder` are still in there doing real work.

## The data it owns

### `Connection`

`Connection` extends Netty's inbound handler for packets and holds:

- **`Connection.receiving`** — a `PacketFlow`, fixed at construction, for
  the direction this end *receives*. `Connection.getReceiving` and
  `Connection.getSending` (the opposite) are the accessors. This is the
  only sense in which a connection knows which end of the wire it is.
- **`Connection.channel`** and **`Connection.address`** — set in
  `Connection.channelActive`, not in the constructor. **A `Connection`
  exists before its channel does**, which is why the next field exists.
- **`Connection.pendingActions`** — a queue of actions deferred until the
  channel is up. It is the *only* queue in `Connection`, it holds
  closures rather than packets, and it is drained by
  `Connection.flushQueue` once connected. There is no outbound packet
  queue; once the channel exists, everything goes straight into Netty's
  own buffer and backpressure is Netty's water marks.
- **`Connection.packetListener`** — volatile, the current inbound
  listener. **`Connection.disconnectListener`** is the fallback used to
  report a disconnection that happened before any listener was set.
- **`Connection.disconnectionDetails`**, `Connection.delayedDisconnect`,
  `Connection.disconnectionHandled`, `Connection.handlingFault` — the
  disconnect bookkeeping, and `Connection.sendLoginDisconnect`, which
  decides whether a fault is reported with
  `ClientboundLoginDisconnectPacket` or `ClientboundDisconnectPacket`.
- **Counters** — `Connection.receivedPackets`, `Connection.sentPackets`,
  `Connection.averageReceivedPackets`, `Connection.averageSentPackets`,
  `Connection.tickCount`, smoothed by
  `Connection.AVERAGE_PACKETS_SMOOTHING`. `Connection.bandwidthDebugMonitor`
  samples inbound bytes for the debug charts.
- **`Connection.INITIAL_PROTOCOL`** — `HandshakeProtocols.SERVERBOUND`.
  Every fresh pipeline starts here.

`Connection` does **not** hold a protocol enum. Where the connection is
in the handshake lives in the `PacketDecoder` and `PacketEncoder`
instances currently in the pipeline, and in the listener.

`RateKickingConnection` is the server's subclass for real sockets: it
holds `RateKickingConnection.rateLimitPacketsPerSecond` and overrides
`Connection.tickSecond` to disconnect a client that talks too fast.

### The listener side

`PacketListener` is the interface every phase's handler implements:
`PacketListener.flow`, `PacketListener.protocol`,
`PacketListener.onDisconnect`, `PacketListener.onPacketError`,
`PacketListener.createDisconnectionInfo`,
`PacketListener.isAcceptingMessages`,
`PacketListener.shouldHandleMessage` and two crash-report hooks.
`ClientboundPacketListener` and `ServerboundPacketListener` are marker
sub-interfaces that fix the direction; `TickablePacketListener` adds a
tick.

**`PacketProcessor`** is the thread hop. It owns a concurrent queue of
`PacketProcessor.ListenerAndPacket` pairs and the thread that is allowed
to drain it, and exposes `PacketProcessor.isSameThread`,
`PacketProcessor.scheduleIfPossible` and
`PacketProcessor.processQueuedPackets`. Both `MinecraftServer` and
`Minecraft` own one.

### The pipeline vocabulary

`HandlerNames` holds the pipeline handler names as constants:
`HandlerNames.SPLITTER`, `HandlerNames.PREPENDER`, `HandlerNames.DECODER`, `HandlerNames.ENCODER`, `HandlerNames.BUNDLER`,
`HandlerNames.UNBUNDLER`, `HandlerNames.COMPRESS`, `HandlerNames.DECOMPRESS`, `HandlerNames.ENCRYPT`, `HandlerNames.DECRYPT`,
`HandlerNames.INBOUND_CONFIG`, `HandlerNames.OUTBOUND_CONFIG`, `HandlerNames.PACKET_HANDLER`, `HandlerNames.TIMEOUT`,
`HandlerNames.LEGACY_QUERY`, `HandlerNames.LATENCY`.

The handlers themselves: `Varint21FrameDecoder` and
`Varint21LengthFieldPrepender` for socket framing; `LocalFrameDecoder`,
`LocalFrameEncoder`, `MonitoredLocalFrameDecoder` and `HiddenByteBuf` for
in-memory framing; `CompressionDecoder` and `CompressionEncoder`;
`CipherDecoder`, `CipherEncoder` and their shared `CipherBase`;
`PacketDecoder` and `PacketEncoder`; `PacketBundlePacker` and
`PacketBundleUnpacker`; `UnconfiguredPipelineHandler` with its nested
`UnconfiguredPipelineHandler.Inbound` and
`UnconfiguredPipelineHandler.Outbound`; and `ProtocolSwapHandler`, an
interface with nothing but two static methods.

**`EventLoopGroupHolder`** owns the event-loop groups. It has four
instances behind `EventLoopGroupHolder.remote` (which picks KQueue, then
Epoll, then NIO) and `EventLoopGroupHolder.local`, each lazily creating
one group whose threads are daemons named for their transport. It lives
in `server/network` but the client uses it too — `ConnectScreen`,
`ServerStatusPinger` and the server list all ask for one.

**`ServerConnectionListener`** is the server's accept side:
`ServerConnectionListener.startTcpServerListener`,
`ServerConnectionListener.startMemoryChannel`,
`ServerConnectionListener.acceptChannel`,
`ServerConnectionListener.tick`,
`ServerConnectionListener.getConnections`, plus a nested
`ServerConnectionListener.LatencySimulator` used only when the debug
latency constants are set.

## The pipeline

Two directions through one list of handlers. Inbound runs head to tail;
outbound runs tail to head. Handlers in *italics* are added later, if at
all.

| inbound order | handler | added by |
|---|---|---|
| 1 | `"timeout"` — a read timeout of thirty seconds | the connect/accept site, before serialization |
| 2 | `"legacy_query"` — `LegacyQueryHandler` | server only, and only if it replies to status; removes itself on the first modern byte |
| 3 | *`"decrypt"`* — `CipherDecoder` | `Connection.setEncryptionKey` |
| 4 | `"splitter"` — `Varint21FrameDecoder` | `Connection.configureSerialization` |
| 5 | an unnamed flow-control handler | `Connection.configureSerialization` |
| 6 | *`"decompress"`* — `CompressionDecoder` | `Connection.setupCompression` |
| 7 | `"decoder"` or `"inbound_config"` | `Connection.configureSerialization` |
| 8 | *`"bundler"`* — `PacketBundlePacker` | `Connection.setupInboundProtocol`, only for a protocol with a bundle |
| 9 | `"packet_handler"` — the `Connection` itself | `Connection.configurePacketHandler` |

Outbound, from the game outwards: `"packet_handler"`, then a nameless
pass-through handler, then *`"unbundler"`* (`PacketBundleUnpacker`),
`"encoder"` or `"outbound_config"`, *`"compress"`*, `"prepender"`,
*`"encrypt"`*, and the socket.

Which side gets a live codec at birth is decided by direction: the end
that will *receive* the handshake — the server — is built with a real
`"decoder"` and a dead `"outbound_config"` placeholder; the end that will
*send* it gets a real `"encoder"` and a dead `"inbound_config"`. Both are
built from `Connection.INITIAL_PROTOCOL`.

### The local pipeline

`Connection.configureInMemoryPipeline` builds the singleplayer variant,
and the differences are smaller than most people assume:

- `"splitter"` and `"prepender"` become `LocalFrameDecoder` and
  `LocalFrameEncoder`, which do nothing but `HiddenByteBuf.pack` and
  `HiddenByteBuf.unpack` — no length prefix, because the buffer never
  becomes a byte stream.
- **No read timeout on either side**, so a wedged integrated server
  hangs rather than disconnecting.
- No legacy query handler, and **never** any cipher or compression
  handler: every site that would install one checks
  `Connection.isMemoryConnection` first.
- Everything else is identical. `PacketEncoder` and `PacketDecoder` are
  still there, still running the same `StreamCodec`s. **Singleplayer
  pays the full serialisation cost.**

The local server binds a channel through `EventLoopGroupHolder.local` and
`ServerConnectionListener.startMemoryChannel` hands back an address that
`Connection.connectToLocalServer` dials.

## When it runs

Everything in the pipeline runs on a Netty event-loop thread. Only two
things run on a game thread: `Connection.tick` (once per game tick, from
`ServerConnectionListener.tick` on the server and from
`MultiPlayerGameMode.tick` on the client) and the *handling* of packets
that asked for a hop.

`Connection.tick` drains `Connection.pendingActions`, flushes the
channel, rolls the packet-rate averages, samples bandwidth and calls
`Connection.handleDisconnection` if the channel has died.
`Connection.tickSecond` is where the rate-kick check lives.

## The trace: bytes to a handler

```mermaid
sequenceDiagram
    participant NET as (socket)
    participant SP as Varint21FrameDecoder
    participant PD as PacketDecoder
    participant CN as Connection
    participant PP as PacketProcessor
    participant SGPL as ServerGamePacketListenerImpl
    participant MS as MinecraftServer

    NET->>SP: a TCP read, on the Netty event loop
    SP->>SP: read the length VarInt; wait until the whole frame is present
    SP->>PD: exactly one frame
    PD->>PD: codec().decode — VarInt id, then the packet's STREAM_CODEC
    PD->>CN: channelRead0 — still the Netty thread
    CN->>SGPL: shouldHandleMessage, then Packet.handle(listener)
    SGPL->>PP: ensureRunningOnSameThread — wrong thread, so enqueue
    SGPL-->>CN: throw RunningOnDifferentThreadException (caught and dropped)
    MS->>PP: processQueuedPackets, before the tick
    PP->>SGPL: handle again, from the top, on the server thread
```

Each arrow is a decision.

**Framing is separate from decoding.** `Varint21FrameDecoder` reads at
most three length bytes and refuses anything wider or a zero length; it
emits exactly one frame or nothing. Everything downstream can assume it
is looking at one whole packet.

**`Connection.channelRead0` calls `Packet.handle` directly, on the Netty
thread.** There is no automatic hop. `PacketListener.shouldHandleMessage`
is consulted first, which is how a listener that is being torn down
ignores what is still arriving.

**The hop is the handler's own first line.**
`PacketUtils.ensureRunningOnSameThread` asks the `PacketProcessor`
whether this is the right thread. If not, it enqueues the
listener-and-packet pair and throws the singleton
`RunningOnDifferentThreadException` — a stackless exception that
`Connection.channelRead0` catches and drops. **The handler body then runs
again from the top** on the game thread, which is why handler methods
must have no side effects before that line.

**The drain has its own phase.** The server runs
`PacketProcessor.processQueuedPackets` inside
`MinecraftServer.processPacketsAndTick`, before the tick proper; the
client runs it in `Minecraft.runTick`, immediately before its ordinary
scheduled tasks. Packet handling and *execute*-style task scheduling are
now two different queues drained at two different moments — a real
change from 1.21, where they were one.

**Errors on re-dispatch go somewhere else.** A failure inside
`PacketProcessor` routes to `PacketListener.onPacketError`, which by
default raises a reported crash — except that an out-of-memory error is
rethrown untouched.

## Swapping the protocol

The pipeline is **reconfigured by writing a message through it**, not by
editing it from outside.

`Connection.setupInboundProtocol` validates that the new listener's
direction and phase match the `ProtocolInfo`, assigns
`Connection.packetListener`, and then builds an
`UnconfiguredPipelineHandler.InboundConfigurationTask` — a closure that
will replace the current handler with a new `PacketDecoder` and turn
auto-read back on, optionally adding `"bundler"` after it. That task is
*written down the channel*, where
`UnconfiguredPipelineHandler.Inbound` recognises it and runs it with the
right context. `Connection.syncAfterConfigurationChange` blocks the
caller until it completes. `Connection.setupOutboundProtocol` is the
mirror image.

Getting back to the unconfigured state is automatic.
`ProtocolSwapHandler.handleInboundTerminalPacket` fires when a packet
whose `Packet.isTerminal` is true passes through `PacketDecoder`: it
turns auto-read *off*, inserts a fresh
`UnconfiguredPipelineHandler.Inbound` under the name
`"inbound_config"`, and removes the decoder.
`ProtocolSwapHandler.handleOutboundTerminalPacket` does the same on the
encoder side, and the bundler and unbundler remove themselves on the
same signal.

So a phase change is: terminal packet, codecs self-destruct and reads
stop, the game thread installs the new protocol, a configuration task
travels the pipeline in order with the byte stream, reads resume. The
unnamed flow-control handler between `"splitter"` and the decoder is what
makes turning auto-read off actually stop delivery mid-batch. The phases
themselves are [protocol phases](protocol-phases.md).

The very first listener is installed by
`Connection.setListenerForServerboundHandshake`, which refuses if one
already exists.

## Compression and encryption

**Compression** is `Connection.setupCompression`, which inserts
`CompressionDecoder` after `"splitter"` and `CompressionEncoder` after
`"prepender"`, or just re-thresholds them if they already exist; a
negative threshold removes both. The server turns it on during login,
sending `ClientboundLoginCompressionPacket` with a send-listener that
installs the handlers only *after* that packet is on the wire. The
client installs its own side when it handles the packet. Both sides skip
it entirely on a memory connection. Note the asymmetry: the server
validates that a compressed frame really was above the threshold; the
client does not.

**Encryption** is `Connection.setEncryptionKey`, which inserts
`CipherDecoder` before `"splitter"` and `CipherEncoder` before
`"prepender"` — so decryption is the first thing that happens to inbound
bytes and encryption the last thing before outbound bytes leave. Neither
is ever removed. The server installs its ciphers synchronously the
moment it handles the key packet; the client attaches its own to the
*send* of that packet, so the key packet itself goes out in the clear and
everything after it does not.

## Interfaces

- **Called by:** `ServerConnectionListener` and `PlayerList` on the
  server; `ConnectScreen`, `ClientPacketListener` and
  `ServerStatusPinger` on the client. Every listener sends through
  `Connection.send`.
- **Calls into:** the current `PacketListener`, via `Packet.handle`.
- **Crosses the network as:** everything. The framing, compression and
  encryption layers are this page; the packet layer is
  [packets and stream codecs](packets-and-stream-codecs.md).
- **Data-driven by:** nothing. Server properties supply the compression
  threshold and the rate limit; the pipeline itself is code.

## Invariants and surprises

- **The handshake, login and status phases are handled entirely on the
  Netty thread.** `ServerHandshakePacketListenerImpl`,
  `ServerLoginPacketListenerImpl`, `ServerStatusPacketListenerImpl` and
  the client's `ClientHandshakePacketListenerImpl` contain no thread hop
  at all. Encryption setup, compression setup and protocol switching all
  happen off the game thread. Only the common, configuration and play
  listeners hop.
- **`Connection` holds no protocol.** There is no field and no getter for
  "which phase am I in". The answer is distributed between the two codec
  handlers in the pipeline and the listener object.
- **There is no outbound packet queue.** `Connection.pendingActions`
  holds closures and matters only in the window before the channel
  exists. Once connected, Netty owns the buffering.
- **Flushing is batched per tick, deliberately — into two flushes, not one.**
  `Connection.send` can write without flushing, and
  `ServerCommonPacketListenerImpl.suspendFlushing` /
  `ServerCommonPacketListenerImpl.resumeFlushing` bracket the whole server
  tick to make it do so. But `Connection.tick` flushes the channel
  unconditionally at the end of its own body, and that runs inside the
  bracket: everything the levels and the player's own tick produced leaves
  there, and `ServerCommonPacketListenerImpl.resumeFlushing` afterwards
  carries only the chunk batch.
- **`Connection.disconnect` blocks the calling thread** on the channel
  close. It is called from the game thread.
- **A disconnection is reported exactly once**, guarded by
  `Connection.disconnectionHandled`, and only once the channel is
  actually closed. A connection that dies with no listener ever set
  falls back to `Connection.disconnectListener`.
- **Keep-alive is the real timeout on a live connection.**
  `ServerCommonPacketListenerImpl.keepConnectionAlive` sends a challenge
  every fifteen seconds and disconnects if the previous one was never
  answered, or if the answer carries the wrong id — with an exemption for
  the singleplayer host. The thirty-second read timeout only exists on
  socket connections.
- **`Connection.setReadOnly` is how a pending disconnect ignores the
  rest of the stream** — it turns auto-read off and leaves the peer's
  remaining packets unread.
- **A tick exception on a memory connection crashes the game.**
  `ServerConnectionListener.tick` catches per-connection failures and
  kicks the client — unless it is the integrated server's own
  connection, in which case it rethrows.
- **Bandwidth accounting is inbound-only.** There is a monitored local
  frame *decoder* and no monitored encoder, because nothing measures what
  the game sends itself.

## Where to look

`Connection` · `HandlerNames` · `PacketListener` · `PacketProcessor` ·
`PacketUtils` · `ProtocolInfo` · `UnconfiguredPipelineHandler` ·
`ProtocolSwapHandler` · `PacketDecoder` · `PacketEncoder` ·
`Varint21FrameDecoder` · `CompressionDecoder` · `CipherBase` ·
`EventLoopGroupHolder` · `ServerConnectionListener` ·
`RateKickingConnection` · `ServerCommonPacketListenerImpl`

---

*Rules: names, never code · how the system works, not how the code reads ·
newest version only · every backticked name passes `tools/verify_names.py`.*
