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
  `Connection.flushQueue` once connected; `Connection.runOnceConnected`
  is the public way in. There is no outbound packet queue; once the
  channel exists, everything goes straight into Netty's own buffer and
  backpressure is Netty's water marks.
- **`Connection.packetListener`** — volatile, the current inbound
  listener. **`Connection.disconnectListener`** is the client's
  connect-attempt fallback: `Connection.initiateServerboundConnection`
  assigns it before the pipeline is configured and
  `Connection.setupInboundProtocol` clears it, so it covers exactly the
  window in which a connection can die before it has a real listener.
- **`Connection.disconnectionDetails`**, `Connection.delayedDisconnect`,
  `Connection.disconnectionHandled`, `Connection.handlingFault` — the
  disconnect bookkeeping. `Connection.sendLoginDisconnect` is a boolean
  beside them, set by `Connection.setupOutboundProtocol` whenever the
  outgoing protocol is `ConnectionProtocol.LOGIN`; it is what decides
  whether a fault is reported with `ClientboundLoginDisconnectPacket` or
  `ClientboundDisconnectPacket`.
- **`Connection.intendedProfileId`** — an identity an embedder can pin on
  a connection before login through `Connection.setIntendedProfileId`,
  checked against the authenticated profile during login. Nothing in the
  tree sets it, so in vanilla that check never fires.
- **Counters** — `Connection.receivedPackets`, `Connection.sentPackets`,
  `Connection.averageReceivedPackets`, `Connection.averageSentPackets`
  and `Connection.tickCount`. `Connection.tickSecond` lerps each average
  three-quarters of the way to the new sample once a second; the constant
  `Connection.AVERAGE_PACKETS_SMOOTHING` names that fraction and is not
  itself referenced. `Connection.bandwidthDebugMonitor` samples inbound
  bytes for the debug charts, and exists only where
  `Connection.setBandwidthLogger` has been called.
- **`Connection.INITIAL_PROTOCOL`** — `HandshakeProtocols.SERVERBOUND`,
  private, and the protocol every fresh pipeline's *live* codec is built
  from.

`Connection` does **not** hold a protocol enum. Where the connection is
in the handshake lives in the `PacketDecoder` and `PacketEncoder`
instances currently in the pipeline, and in the listener; the only thing
`Connection` does with `ConnectionProtocol` is compare it in
`Connection.validateListener` when a new listener is installed.

`RateKickingConnection` is the server's subclass that kicks a client
which talks too fast: it holds
`RateKickingConnection.rateLimitPacketsPerSecond` and overrides
`Connection.tickSecond`. It is **conditional, not the default** — both
`ServerConnectionListener.startTcpServerListener` and
`ServerConnectionListener.acceptChannel` build one only when the server's
rate limit is above zero, and that property defaults to zero, so an
ordinary socket gets a plain `Connection`.

### The listener side

`PacketListener` is the interface every phase's handler implements:
`PacketListener.flow`, `PacketListener.protocol`,
`PacketListener.onDisconnect`, `PacketListener.onPacketError`,
`PacketListener.createDisconnectionInfo`,
`PacketListener.isAcceptingMessages`,
`PacketListener.shouldHandleMessage` and two crash-report hooks.
`ClientboundPacketListener` and `ServerboundPacketListener` are marker
sub-interfaces that fix the direction.

**`TickablePacketListener`** adds `TickablePacketListener.tick`, and it
matters more than it looks: `Connection.tick` calls it, so it is the only
route by which a listener gets time on a game thread without a packet
having arrived. Five classes implement it —
`ServerLoginPacketListenerImpl` (whose tick *is* the server-side login
state machine), `ServerConfigurationPacketListenerImpl`,
`ServerGamePacketListenerImpl`, `ClientConfigurationPacketListenerImpl`
and `ClientPacketListener` — and the keep-alive challenge reaches the
wire through it.

**`PacketProcessor`** is the thread hop. It owns a concurrent queue of
`PacketProcessor.ListenerAndPacket` pairs and the thread that is allowed
to drain it, and exposes `PacketProcessor.isSameThread`,
`PacketProcessor.scheduleIfPossible` and
`PacketProcessor.processQueuedPackets`. It is also closeable: after
`PacketProcessor.close` the queue neither accepts nor drains, and
`PacketProcessor.scheduleIfPossible` throws instead. Both
`MinecraftServer` and `Minecraft` own one.

### The pipeline vocabulary

`HandlerNames` holds the pipeline handler names as constants:
`HandlerNames.SPLITTER`, `HandlerNames.PREPENDER`, `HandlerNames.DECODER`, `HandlerNames.ENCODER`, `HandlerNames.BUNDLER`,
`HandlerNames.UNBUNDLER`, `HandlerNames.COMPRESS`, `HandlerNames.DECOMPRESS`, `HandlerNames.ENCRYPT`, `HandlerNames.DECRYPT`,
`HandlerNames.INBOUND_CONFIG`, `HandlerNames.OUTBOUND_CONFIG`, `HandlerNames.PACKET_HANDLER`, `HandlerNames.TIMEOUT`,
`HandlerNames.LEGACY_QUERY`, `HandlerNames.LATENCY`.

**Nothing references it.** Every name the pipeline is actually built with
is a string literal in `Connection`, `ServerConnectionListener`,
`ProtocolSwapHandler` and `UnconfiguredPipelineHandler`. The class is a
complete and correct index of names that no code reads — which is why it
is worth citing, and why it cannot be trusted to stay in step.

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

**`EventLoopGroupHolder`** owns the event-loop groups. Four instances sit
behind two static accessors: `EventLoopGroupHolder.local`, and
`EventLoopGroupHolder.remote`, which takes a flag and tries KQueue then
Epoll **only if it is set** — otherwise NIO, immediately. The flag is the
client's *use native transport* option or the server property of the same
name, so switching it off really does change transport rather than hint
at it. Each holder lazily creates one group whose threads are daemons
named for its transport. It lives in `server/network`, but the client
uses it too — `ConnectScreen`, `ServerStatusPinger` and the server list
all ask for one.

**`ServerConnectionListener`** is the server's accept side:
`ServerConnectionListener.startTcpServerListener`,
`ServerConnectionListener.startMemoryChannel`,
`ServerConnectionListener.tick`,
`ServerConnectionListener.getConnections`,
`ServerConnectionListener.getSessionId` (a UUID minted once per server
session and handed to the client in `ClientboundLoginFinishedPacket`),
and two shutdowns — `ServerConnectionListener.stop`, and
`ServerConnectionListener.stopTcpServerListener`, which closes only the
non-local binds and is therefore how *Open to LAN* stops listening
without severing singleplayer. `ServerConnectionListener.acceptChannel`
is a third way in, taking an already-open channel and an intended profile
id; **nothing in the tree calls it**, and it is the only assignment of
`Connection.intendedProfileId`. The nested
`ServerConnectionListener.LatencySimulator` is installed on the memory
channel only, and only when the debug latency constants are set.

## The pipeline

Two directions through one list of handlers. Inbound runs head to tail;
outbound runs tail to head. Handlers in *italics* are added later, if at
all.

| inbound order | handler | added by |
|---|---|---|
| 1 | `"timeout"` — a read timeout of thirty seconds | the connect/accept site, before serialization |
| 2 | `"legacy_query"` — `LegacyQueryHandler` | `ServerConnectionListener.startTcpServerListener` only, and only if the server replies to status; removes itself on the first modern byte |
| 3 | *`"decrypt"`* — `CipherDecoder` | `Connection.setEncryptionKey` |
| 4 | `"splitter"` — `Varint21FrameDecoder` | `Connection.configureSerialization` |
| 5 | *`"decompress"`* — `CompressionDecoder` | `Connection.setupCompression`, inserted directly *after* `"splitter"` |
| 6 | an unnamed flow-control handler | `Connection.configureSerialization` |
| 7 | `"decoder"` or `"inbound_config"` | `Connection.configureSerialization` |
| 8 | *`"bundler"`* — `PacketBundlePacker` | `Connection.setupInboundProtocol`, only for a protocol with a bundle |
| 9 | `"packet_handler"` — the `Connection` itself | `Connection.configurePacketHandler` |

Outbound, from the game outwards: `"packet_handler"`, then `"hackfix"` —
an anonymous pass-through that `Connection.configurePacketHandler` adds
immediately before it, whose write method does nothing but call its
superclass — then *`"unbundler"`* (`PacketBundleUnpacker`), `"encoder"`
or `"outbound_config"`, *`"compress"`*, `"prepender"`, *`"encrypt"`*, and
the socket.

Which side gets a live codec at birth is decided by direction: the end
that will *receive* the handshake — the server — is built with a real
`"decoder"` and a dead `"outbound_config"` placeholder; the end that will
*send* it gets a real `"encoder"` and a dead `"inbound_config"`. Only the
live one is built from `Connection.INITIAL_PROTOCOL`. The placeholder is
a bare `UnconfiguredPipelineHandler` holding no protocol at all, which is
the entire point of it.

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
  handler — though by two different mechanisms. Compression is refused at
  the installation sites, which both check
  `Connection.isMemoryConnection`. Encryption is not: neither
  `Connection.setEncryptionKey` nor either side's key handler tests for a
  memory connection. What prevents it sits one gate further up, in
  `ServerLoginPacketListenerImpl`, where the decision to *ask* for
  encryption requires authentication **and** a non-memory connection — so
  `ClientboundHelloPacket` is never sent and the ciphers are never
  reached.
- Everything else is identical. `PacketEncoder` and `PacketDecoder` are
  still there, still running the same `StreamCodec`s. **Singleplayer
  pays the full serialisation cost.**

The local server binds a channel through `EventLoopGroupHolder.local` and
`ServerConnectionListener.startMemoryChannel` hands back an address that
`Connection.connectToLocalServer` dials.

## When it runs

Everything in the pipeline runs on a Netty event-loop thread. Three
things run on a game thread: `Connection.tick`, whatever
`TickablePacketListener.tick` does inside it, and the *handling* of
packets that asked for a hop.

`Connection.tick`, in order: drain `Connection.pendingActions`; tick the
current listener if it is a `TickablePacketListener`; call
`Connection.handleDisconnection` if the channel has died; flush the
channel; every twentieth tick run `Connection.tickSecond`, which rolls
the packet-rate averages and is where `RateKickingConnection`'s kick
lives; and last, sample bandwidth. The flush is in the middle, not at the
end, and the disconnect check happens before it.

Its callers differ by side. The server has one:
`MinecraftServer.tickConnection` walks `ServerConnectionListener.tick`.
The client has three, because the client has more than one connection —
`MultiPlayerGameMode.tick` ticks the play connection, `Minecraft.runTick`
ticks `Minecraft.pendingConnection` (the one still handshaking or logging
in, and therefore the one that drives a login), and `ServerStatusPinger`
ticks the connections it opened to ping the servers in the list.

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
    PP->>SGPL: shouldHandleMessage again, then handle from the top
```

Each arrow is a decision.

**Framing is separate from decoding.** `Varint21FrameDecoder` reads at
most three length bytes and refuses anything wider or a zero length; it
emits exactly one frame or nothing. Everything downstream can assume it
is looking at one whole packet.

**`Connection.channelRead0` calls `Packet.handle` directly, on the Netty
thread.** There is no automatic hop. `PacketListener.shouldHandleMessage`
is consulted first — which is how a listener being torn down ignores what
is still arriving — and `Connection.receivedPackets` counts only the
packets that pass it. The method has three other outcomes: a packet
arriving before any listener is set is an illegal state; a packet whose
listener is of the wrong shape is a cast failure and an
*invalid_packet* kick; and a rejected schedule — the `PacketProcessor`
closed because the game is shutting down — becomes a *server_shutdown*
kick.

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
scheduled tasks and before the frame's client ticks. Packet handling and
*execute*-style task scheduling are now two different queues drained at
two different moments — a real change from 1.21, where they were one.

**The drain re-asks the same question.**
`PacketProcessor.ListenerAndPacket` calls
`PacketListener.shouldHandleMessage` a second time before dispatching,
and logs and drops if the answer has changed. That is the gate that
matters: a packet can wait between the two checks, and a disconnect in
between must not be able to run its handler.

**Errors on re-dispatch go somewhere else.** The drain catches only
checkable exceptions — so a bare out-of-memory error is not caught at all
— and routes what it does catch to `PacketListener.onPacketError`, which by
default raises a reported crash. The one special case is a
`ReportedException` *caused by* an out-of-memory error: that is rethrown,
but not untouched. `PacketUtils.makeReportedException` first decorates
the report with an *Incoming Packet* category naming the type and its
terminal and skippable flags, then lets the listener add its own detail
through `PacketUtils.fillCrashReport`.

## Sending

Outbound is the mirror image and shorter. `Connection.send` reaches
`Connection.sendPacket`, which checks whether the calling thread is
already the channel's event loop and, if not, schedules the write onto
it — so a packet sent from the game thread crosses the same boundary an
inbound packet does, just without a queue of its own.
`Connection.doSendPacket` then chooses between a write and a
write-and-flush, and between a real future and Netty's void promise;
`Connection.flushChannel` performs the same hop for a bare flush.

`PacketSendListener` is the callback type that rides along.
`PacketSendListener.thenRun` runs something once the packet is really on
the wire — which is how compression and the client's encryption are
installed *after* the packet that announced them, and how a disconnect
waits for its own kick message to leave.
`PacketSendListener.exceptionallySend` sends a fallback packet when the
write fails. Both run on the event loop, which is why "disconnect after
sending" is not a game-thread operation.

## Swapping the protocol

The pipeline is **reconfigured by writing a message through it**, not by
editing it from outside.

`Connection.setupInboundProtocol` validates that the new listener's
direction and phase match the `ProtocolInfo`, assigns
`Connection.packetListener`, and then builds an
`UnconfiguredPipelineHandler.InboundConfigurationTask` — a closure that
will replace the current handler with a new `PacketDecoder` and turn
auto-read back on, optionally adding `"bundler"` after it. That task is
*written down the channel*, where `UnconfiguredPipelineHandler.Inbound`
recognises it and runs it with the right context.
`Connection.syncAfterConfigurationChange` blocks the caller until it
completes. `Connection.setupOutboundProtocol` is the mirror image, and
also records whether the new outbound protocol is the login one, for the
benefit of the disconnect path.

Getting back to the unconfigured state is automatic, and it is
asymmetric. `ProtocolSwapHandler.handleInboundTerminalPacket` fires when
a packet whose `Packet.isTerminal` is true passes through
`PacketDecoder`: it turns auto-read *off*, inserts a fresh
`UnconfiguredPipelineHandler.Inbound` under the name `"inbound_config"`,
and removes the decoder.
`ProtocolSwapHandler.handleOutboundTerminalPacket` does the equivalent on
the encoder side — but there is no incoming flow to stop, so it leaves
auto-read alone and simply puts an
`UnconfiguredPipelineHandler.Outbound` in the encoder's place. The
bundler and unbundler remove themselves on the same signal, and
`PacketBundlePacker` treats a terminal packet arriving *inside* a bundle
as a decode error rather than a swap.

So a phase change is: terminal packet, codecs self-destruct and inbound
reads stop, the game thread installs the new protocol, a configuration
task travels the pipeline in order with the byte stream, reads resume.
The unnamed flow-control handler between `"splitter"` and the decoder is
what makes turning auto-read off actually stop delivery mid-batch. The
phases themselves are [protocol phases](protocol-phases.md).

The server's first listener is installed by
`Connection.setListenerForServerboundHandshake`, which refuses if one
already exists and refuses on a connection that is not receiving
serverbound traffic in the handshake protocol — so it is server-side by
construction. The client has no equivalent: its first listener arrives
with the pair of protocols that
`Connection.initiateServerboundConnection` installs around
`ClientIntentionPacket`, and
`Connection.initiateServerboundStatusConnection` is the same code with a
different intent.

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
client does not. The frame ceilings the two handlers enforce are in
[packets and stream codecs](packets-and-stream-codecs.md).

**Encryption** is `Connection.setEncryptionKey`, which inserts
`CipherDecoder` before `"splitter"` and `CipherEncoder` before
`"prepender"` — so decryption is the first thing that happens to inbound
bytes and encryption the last thing before outbound bytes leave. Neither
is ever removed. The server installs its ciphers synchronously the
moment it handles the key packet; the client attaches its own to the
*send* of that packet, so the key packet itself goes out in the clear and
everything after it does not.

## How a connection dies

`Connection.exceptionCaught` is the funnel, and it has four outcomes.

- A `SkipPacketException` is **logged and swallowed**: the codec layer
  has already decided this one packet may be dropped, and the connection
  survives. The machinery that raises it belongs to
  [packets and stream codecs](packets-and-stream-codecs.md); what matters
  here is that it is the one exception class that does not end the
  connection.
- A timeout — the thirty-second read timeout expiring — disconnects with
  *disconnect.timeout*, the "Timed out" a player sees.
- Any other fault, the **first** time: the listener is asked for a
  `DisconnectionDetails` through
  `PacketListener.createDisconnectionInfo`; if this end is the one
  sending clientbound traffic it tries to tell the peer why, with either
  `ClientboundLoginDisconnectPacket` or `ClientboundDisconnectPacket`
  depending on `Connection.sendLoginDisconnect`, and disconnects once
  that packet has gone; then it calls `Connection.setReadOnly`.
- Any other fault, the **second** time — a fault while handling a fault,
  which `Connection.handlingFault` detects — skips all of that and
  disconnects immediately.

`Connection.setReadOnly` is how a pending disconnect ignores the rest of
the stream: it turns auto-read off and leaves the peer's remaining
packets unread. `Connection.handleDisconnection` is the other end of the
story — it runs from `Connection.tick`, only once the channel is really
closed, reports to the listener (or to `Connection.disconnectListener` if
the connection never got one) and is guarded by
`Connection.disconnectionHandled` so it reports exactly once.

## Interfaces

- **Called by:** `ServerConnectionListener` and `PlayerList` on the
  server; `ConnectScreen`, `ClientPacketListener` and
  `ServerStatusPinger` on the client. Every listener sends through
  `Connection.send`.
- **Calls into:** the current `PacketListener`, via `Packet.handle` and
  via `TickablePacketListener.tick`.
- **Crosses the network as:** everything. The framing, compression and
  encryption layers are this page; the packet layer is
  [packets and stream codecs](packets-and-stream-codecs.md).
- **Data-driven by:** nothing. Server properties supply the compression
  threshold, the rate limit and the native-transport choice; the pipeline
  itself is code.

## Invariants and surprises

- **No handshake, status or login packet handler ever hops to a game
  thread — and the login still finishes on one.** None of
  `ServerHandshakePacketListenerImpl`, `ServerStatusPacketListenerImpl`,
  `ServerLoginPacketListenerImpl` or the client's
  `ClientHandshakePacketListenerImpl` contains a single
  `PacketUtils.ensureRunningOnSameThread` call, so encryption setup and
  every state transition happen on the event loop. But
  `ServerLoginPacketListenerImpl` is a `TickablePacketListener`, and its
  tick — on the server thread, through `Connection.tick` — is what runs
  the ban and whitelist checks, switches compression on, and sends the
  terminal packet that ends the phase. Login is a three-thread state
  machine, not a Netty-only one; see
  [protocol phases](protocol-phases.md).
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
  unconditionally, and that runs inside the bracket: everything the levels
  produced leaves there. What rides the later
  `ServerCommonPacketListenerImpl.resumeFlushing` is everything
  `MinecraftServer.tickChildren` does *after* ticking connections — the
  player list, the debug subscribers, the game-test ticker, the server's
  own tickables, and last of all the chunk batch.
- **The suspension only binds the server thread.**
  `ServerCommonPacketListenerImpl.send` suppresses the flush only when
  the flag is set *and* the caller is the server thread. Anything sent
  from another thread flushes immediately, bracket or no bracket.
- **`Connection.disconnect` blocks its caller** on the channel close —
  and its caller is usually the Netty event loop, not the game thread.
  `Connection.channelInactive`, `Connection.exceptionCaught` and every
  `PacketSendListener.thenRun` callback reach it from there; the
  game-thread callers are the deliberate kicks, like the `/kick` and ban
  commands.
- **A disconnection is reported exactly once**, guarded by
  `Connection.disconnectionHandled`, and only once the channel is
  actually closed.
- **Keep-alive is the real timeout on a live connection.**
  `ServerCommonPacketListenerImpl.keepConnectionAlive` sends a challenge
  every `ServerCommonPacketListenerImpl.LATENCY_CHECK_INTERVAL` — fifteen
  seconds — and disconnects if the previous one was never answered, or if
  the answer carries the wrong id, with an exemption for the singleplayer
  host. It stops sending them once the listener has closed itself behind
  a terminal packet; from that moment
  `ServerCommonPacketListenerImpl.checkIfClosed` gives the protocol swap
  another fifteen seconds and then times the connection out. The
  thirty-second read timeout exists only on socket connections.
- **A tick exception on a memory connection crashes the game.**
  `ServerConnectionListener.tick` catches per-connection failures and
  kicks the client — unless `Connection.isMemoryConnection`, in which
  case it raises a fresh reported crash instead.
- **Bandwidth accounting is a client-only, inbound-only, socket-only
  measurement.** `Connection.bandwidthDebugMonitor` is set from
  `ConnectScreen` and the Realms connect path and nowhere else, so no
  server ever has one. `MonitoredLocalFrameDecoder` exists for the
  singleplayer case and is **never installed**: the local pipeline is
  always built with a null monitor.

## Where to look

`Connection` · `HandlerNames` · `PacketListener` ·
`TickablePacketListener` · `PacketProcessor` · `PacketUtils` ·
`PacketSendListener` · `ProtocolInfo` · `UnconfiguredPipelineHandler` ·
`ProtocolSwapHandler` · `PacketDecoder` · `PacketEncoder` ·
`Varint21FrameDecoder` · `CompressionDecoder` · `CipherBase` ·
`EventLoopGroupHolder` · `ServerConnectionListener` ·
`RateKickingConnection` · `DisconnectionDetails` ·
`ServerCommonPacketListenerImpl`

---

*Rules: names, never code · how the system works, not how the code reads ·
newest version only · every backticked name passes `tools/verify_names.py`.*
