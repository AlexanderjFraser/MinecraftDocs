# Chat and signing

> Verified against **Minecraft 26.2** · Part IX · one message: typed, signed, validated, decorated, broadcast, validated again, displayed — and reportable afterwards.

## Responsibility

Two systems share this page because they are inseparable in the code.
`Component` is the text type the whole game uses — every name, tooltip,
title, disconnect reason and chat line. And chat is the one place where
text is **cryptographically attributed**: a message carries a signature
proving that a specific account, in a specific session, said exactly
those characters with exactly that conversational context in front of
them.

The one sentence a player would recognise: *the "Not Secure" tag, and
being able to report someone.*

The headline for a 1.21-era reader: **vanilla never decorates chat.**
`MinecraftServer.getChatDecorator` is hard-coded to
`ChatDecorator.PLAIN`, so the entire decorate-and-re-sign apparatus —
unsigned content on the wire, the *modified* trust level, the hover that
shows you the original — exists purely for servers that are not vanilla.

## The data it owns

### `Component`

`Component` is an interface with three abstract accessors —
`Component.getStyle`, `Component.getContents`, `Component.getSiblings` —
and exactly **one** implementation, `MutableComponent`. A component is a
triple: one `ComponentContents`, one `Style`, and an ordered list of
sibling components. Style inheritance happens during traversal, not in
storage.

There are seven kinds of contents, each with a static factory on
`Component`:

| kind | class | made by |
|---|---|---|
| text | `PlainTextContents`, with `PlainTextContents.LiteralContents` | `Component.literal` |
| translatable | `TranslatableContents` | `Component.translatable` |
| keybind | `KeybindContents` | `Component.keybind` |
| score | `ScoreContents` | `Component.score` |
| selector | `SelectorContents` | `Component.selector` |
| nbt | `NbtContents` | `Component.nbt` |
| object | `ObjectContents` | `Component.object` |

`ObjectContents` is new-shaped in 26.2: it puts atlas sprites and player
heads *inside* text, through `ObjectInfo` and its implementations
`AtlasSprite` and `PlayerSprite`.

`Style` holds eleven nullable fields: `Style.color` (a `TextColor`),
`Style.shadowColor`, the five booleans, `Style.clickEvent`,
`Style.hoverEvent`, `Style.insertion` and `Style.font` (a
`FontDescription`). `ClickEvent` and `HoverEvent` are sealed families of
records; `ClickEvent.Action.allowFromServer` is what keeps
`ClickEvent.Action.OPEN_FILE` off the wire.

**Serialisation** is one recursive codec, `ComponentSerialization.CODEC`,
whose shape is a three-way choice: a bare string becomes a literal, a
list becomes its first element with the rest appended, and an object is
the full record. Contents are matched by an explicit *type* field if one
is present and otherwise by trying each contents codec in turn — which
is why an untyped component still round-trips. `Component.tryCollapseToString`
is what lets a plain unstyled literal encode as a bare string.

On the wire, **components travel as NBT, not JSON**:
`ComponentSerialization.STREAM_CODEC` is built over the NBT ops. There
are trusted variants —
`ComponentSerialization.TRUSTED_STREAM_CODEC` and its siblings — that
lift the NBT budget, and **every clientbound chat packet uses them**
([packets and stream codecs](packets-and-stream-codecs.md)).

Resolution — turning selectors, scores and NBT paths into text — is
`ComponentUtils.resolve` against a `ResolutionContext`, which carries the
command source, a depth limit and a `ResolutionContext.LimitBehavior`.
**Chat never resolves anything**: chat content is a plain string all the
way to `Component.literal`.

### Signing

- **`PlayerChatMessage`** — the whole message: a `SignedMessageLink`, a
  `MessageSignature`, a `SignedMessageBody`, an optional unsigned
  (decorated) `Component`, and a `FilterMask`.
- **`SignedMessageBody`** — what is signed: the content string, the
  timestamp, the salt, and the `LastSeenMessages` list.
- **`SignedMessageLink`** — the chain position: an index, the sender's
  id and the session id. `SignedMessageLink.root` starts a chain,
  `SignedMessageLink.advance` moves it on, and
  `SignedMessageLink.isDescendantOf` is the ordering check.
- **`MessageSignature`** — a fixed 256 bytes, so 2048-bit RSA, with no
  length prefix on the wire. `MessageSignature.Packed` is the wire form:
  a cache index, or a marker meaning a full signature follows.
- **`SignedMessageChain`** with its `SignedMessageChain.Encoder` and
  `SignedMessageChain.Decoder`; `SignedMessageChain.DecodeException`
  enumerates every way it can go wrong.
- **`SignedMessageValidator`**, the receiving client's checker, with the
  `SignedMessageValidator.KeyBased` implementation plus the two
  degenerate ones, `SignedMessageValidator.ACCEPT_UNSIGNED` and
  `SignedMessageValidator.REJECT_ALL`.
- **`RemoteChatSession`** (a session id and a `ProfilePublicKey`) and
  **`LocalChatSession`** (a session id and the key pair). The key itself
  is signed by Mojang: `ProfilePublicKey.Data` carries an expiry, the
  key and a signature over both, validated against the services key.
- **`MessageSignatureCache`** — the shared dictionary that keeps
  twenty full signatures off every packet.
- **`ChatType`** — a data-driven pair of `ChatTypeDecoration`s, one for
  display and one for narration, with `ChatType.Bound` carrying the
  resolved sender and target names. The vanilla keys are
  `ChatType.CHAT`, `ChatType.SAY_COMMAND`, `ChatType.EMOTE_COMMAND` and
  the message and team variants. It is a synced registry, so a data pack
  can add one.
- **`FilterMask`** — which characters the server's text filter redacted.

### The last-seen window

`LastSeenMessages` holds up to `LastSeenMessages.LAST_SEEN_MESSAGES_MAX_LENGTH`
signatures — twenty, and the same twenty appears on both sides and in
the bit set on the wire. The client keeps a
`LastSeenMessagesTracker`, a ring of `LastSeenTrackedEntry` with a
running offset; the server keeps a mirror, `LastSeenMessagesValidator`.
`LastSeenMessages.Update` is what crosses: an offset, a twenty-bit
acknowledgement set, and a one-byte checksum.

## When it runs

Asymmetrically, and this is where the surprises live.

- **Client `ClientPacketListener.sendChat`** — including the RSA signature — runs on the
  client main thread, straight out of `ChatScreen`.
- **Server `ServerGamePacketListenerImpl.handleChat`** runs on the **Netty event loop**. It
  deliberately does *not* hop: the last-seen validation happens there,
  under a lock, as do the illegal-character and chat-visibility checks.
- **Signature verification** happens on the **server main thread**,
  inside the task that handler schedules.
- **Text filtering** is asynchronous, and ordering is restored by
  `FutureChain`, which runs its continuations on the server executor.
- **Client `ClientPacketListener.handlePlayerChat`** — including RSA verification — runs on
  the client main thread.
- The profile key is fetched on a client IO pool and picked up by
  polling in `ClientPacketListener.tick`; report upload is on another
  pool.

## What is actually signed

`PlayerChatMessage.updateSignature` feeds the signature, in order:

1. a version constant;
2. the link — sender id, session id, index;
3. the body — salt, timestamp **in seconds**, the content length, the
   content bytes, then the count of last-seen signatures followed by
   each one's raw bytes.

So the signature binds the text *and* the conversational context the
sender had in front of them. **Not** signed: the decorated component, the
filter mask, the `ChatType.Bound`, and the global index.

The session key is signed one level up: `ProfilePublicKey.Data` is
verified against Mojang's services key over the profile id, the expiry
**in milliseconds** and the encoded key.

## The trace: one message

```mermaid
sequenceDiagram
    participant CS as ChatScreen
    participant CPL as ClientPacketListener
    participant SGPL as ServerGamePacketListenerImpl
    participant PLL as PlayerList
    participant RCPL as (recipient) ClientPacketListener
    participant CLIS as ChatListener

    CS->>CPL: sendChat — trim to 256 characters
    CPL->>CPL: build the body; sign it with the session key
    CPL->>SGPL: ServerboundChatPacket — content, timestamp, salt, signature, last-seen
    SGPL->>SGPL: Netty thread: apply the last-seen update, check characters
    SGPL->>SGPL: main thread: unpack through SignedMessageChain.Decoder
    SGPL->>SGPL: text filter (async), then ChatDecorator.PLAIN (a no-op)
    SGPL->>PLL: broadcastChatMessage, bound to ChatType.CHAT
    PLL->>RCPL: ClientboundPlayerChatPacket — signatures packed to cache ids
    RCPL->>RCPL: check the global index; unpack the cache ids; verify the signature
    RCPL->>CLIS: handlePlayerChatMessage — trust level, blocks, the delay queue
    CLIS->>CPL: markMessageAsProcessed; eventually ServerboundChatAckPacket
```

Each arrow is a decision.

**The client signs before it sends.** It takes the current time, a random
salt and the current last-seen window, and produces the signature on the
main thread. The window it signs is also the window it now considers
acknowledged.

**The server validates the window before anything else, on the network
thread.** `LastSeenMessagesValidator` checks the offset and the twenty
acknowledgement bits against its own mirror and compares the checksum. A
mismatch is not a rejected message — it is a **disconnect**, because the
two sides' idea of the conversation has diverged and no later signature
could be checked.

**Verification breaks the chain, permanently.**
`SignedMessageChain.Decoder` fails with a specific reason — missing key,
expired key, broken chain, out-of-order, invalid signature — and for
most of them nulls the chain. The sender gets a red message and stays
connected, but **every subsequent message fails too** until a new session
key resets it.

**Decoration is a no-op in vanilla, and that shows on the wire.**
Because `ChatDecorator.PLAIN` returns the same text,
`PlayerChatMessage.withUnsignedContent` drops the decorated copy
entirely, so vanilla always sends a null unsigned content.

**Broadcast is per recipient, and gated.** `PlayerList.broadcastChatMessage`
logs the line — marked as insecure if the message has no signature or has
expired — and then sends only to players whose chat visibility accepts
it. A recipient whose copy was fully filtered causes the *sender* to be
told so.

**Signatures are packed against the cache.** `SignedMessageBody.pack`
replaces each last-seen signature with a `MessageSignatureCache` index
where it can. Both sides push into their cache identically.

**The receiving client checks an index first.** A gap in the global chat
index is a disconnect; an unknown cache id is a disconnect. Only then is
the signature verified, by `SignedMessageValidator.KeyBased`, whose
failure latches — once a sender's chain is invalid, it stays invalid.

**Display is where trust becomes visible.** `ChatListener` evaluates a
`ChatTrustLevel`, checks the social blocklist and the filter mask, and
tags the line. Then it goes into the chat delay queue, the HUD, the
narrator and the `ChatLog`.

**Acknowledgement is separate from sending.**
`ClientPacketListener.markMessageAsProcessed` advances the tracker, and
when the accumulated offset gets large enough the client sends a bare
`ServerboundChatAckPacket`. A player who only listens still has to
acknowledge, or the server's pending list grows until the connection is
dropped.

## Commands

Commands split into two packets. `ClientPacketListener.sendCommand`
parses locally and builds a `SignableCommand`; if no argument needs
signing it sends `ServerboundChatCommandPacket`, which carries nothing
but the string. If one does, it sends
`ServerboundChatCommandSignedPacket` with `ArgumentSignatures` — **one
signature per argument**, each consuming its own chain index while
sharing a timestamp, salt and window.

"Signable" means the argument type implements `SignedArgument`, and in
26.2 there is exactly one such type: `MessageArgument`, behind the
message-shaped commands. The server re-parses and compares argument names
positionally; a mismatch is refused. It also refuses an *unsigned*
command that its own parse says should have had signatures — which is
how a client cannot simply strip them.

A command message with no signed argument becomes a
`ClientboundDisguisedChatPacket`: chat-type decorated, unsigned, and not
reportable.

## Interfaces

- **Called by:** `ChatScreen` and the command dispatcher on the client;
  `ServerGamePacketListenerImpl` and `PlayerList` on the server;
  every system in the game that builds a `Component`.
- **Calls into:** `Signer` and `SignatureValidator` over the JDK's RSA;
  the text filter service; the session service for the profile key.
- **Crosses the network as:** `ServerboundChatPacket`,
  `ServerboundChatCommandPacket`,
  `ServerboundChatCommandSignedPacket`, `ServerboundChatAckPacket`,
  `ServerboundChatSessionUpdatePacket`;
  `ClientboundPlayerChatPacket`, `ClientboundSystemChatPacket`,
  `ClientboundDisguisedChatPacket`, `ClientboundDeleteChatPacket`,
  `ClientboundCustomChatCompletionsPacket`, and the chat-session entry
  in `ClientboundPlayerInfoUpdatePacket`.
- **Data-driven by:** `ChatType`, a synced registry, so a data pack can
  add message formats. The *signing* is not data-driven at all.

## Invariants and surprises

- **Chat sessions are negotiated in the play phase, not at login.** The
  client only fetches a key if `ClientboundLoginPacket` says the server
  is in online mode, and announces it later with
  `ServerboundChatSessionUpdatePacket`. See
  [protocol phases](protocol-phases.md).
- **A signature-cache desync silently invalidates signatures.** The
  last-seen list is *signed in full* but *sent as cache indices*. If the
  two caches diverge, the receiver reconstructs a different body and the
  verification fails with no crypto-level explanation — which is exactly
  why `LastSeenMessages.Update` carries a checksum whose failure message
  is about desynchronisation.
- **The client's private key is only written to disk in a development
  environment.** In a shipped client the key file is deleted on every
  refresh path, so every launch re-fetches from the account service.
- **A non-default font counts as tampering.** `ChatTrustLevel` treats any
  style whose font is not the default as *modified*, so a server that
  styles chat with a custom font gets every line flagged.
- **`ClientboundDeleteChatPacket` is never sent by vanilla.** It is
  handled fully — including the deferred deletion of a message too fresh
  to vanish silently — but nothing constructs it.
- **Failing to verify does not disconnect; failing to keep the window in
  sync does.** An invalid signature costs the sender their chain and
  gets them a red message. A last-seen mismatch, a bad chat index, or an
  unknown cache id ends the connection.
- **A silent listener is on a timer.** The server tracks every signed
  message it has sent a player, and past a few thousand unacknowledged
  it disconnects them — which is what the bare acknowledgement packet
  exists to prevent.
- **Signed and unsigned coexist.** Without a session, the encoder
  produces no signature; if `enforce-secure-profile` is off the server
  accepts it, recipients fall back to accepting unsigned messages, and
  the line is tagged insecure. With it on, every such message is
  rejected at the chain.
- **Only signed messages are reportable.** The client's `ChatLog` records
  everything, but a log entry can only be reported if it carries a
  signature from the reported player. System messages never can.
- **A report carries the signed material, not the rendered text.** The
  evidence includes the chain index, session id, timestamp, salt, the
  last-seen signatures and the *signed* content — enough for Mojang to
  re-verify the signature independently and to see the context the
  reporter saw. `ChatReportContextBuilder` walks the last-seen links
  backwards to gather that context.

## Where to look

`Component` · `MutableComponent` · `ComponentContents` ·
`ComponentSerialization` · `Style` · `ChatType` · `PlayerChatMessage` ·
`SignedMessageBody` · `SignedMessageLink` · `SignedMessageChain` ·
`SignedMessageValidator` · `MessageSignature` · `MessageSignatureCache`
· `LastSeenMessages` · `LastSeenMessagesValidator` · `RemoteChatSession`
· `ProfilePublicKey` · `ChatListener` · `ChatTrustLevel` ·
`ReportingContext`

---

*Rules: names, never code · how the system works, not how the code reads ·
newest version only · every backticked name passes `tools/verify_names.py`.*
