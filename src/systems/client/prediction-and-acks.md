# Prediction and acknowledgement

> Verified against **Minecraft 26.2** · Part X · a block placed against a wall the server will not allow: the client shows it, the server refuses it, and a numbered receipt decides when the lie ends.

## Responsibility

The client cannot wait a round trip to show you the block you just placed, so
it places it locally and tells the server afterwards. This page owns the
machinery that makes that safe: one ledger per level, one sequence counter,
six windows in which a prediction can be opened, three packets that carry a
sequence number, and one acknowledgement packet that says how far the server
has got. Part V's [block interaction](../blocks/block-interaction.md) and
[block breaking](../blocks/block-breaking.md) are the two applications;
[what the client is told](../networking/what-the-client-is-told.md) is the
server's side of the conversation.

The one sentence a player would recognise: *the block that appears, then
disappears.*

The headline, and the thing most descriptions of this system get wrong:
**the acknowledgement is a receipt for a number, not a verdict on an
action.** It is sent for actions the server rejected exactly as it is sent
for actions it accepted. Correctness comes from an ordering rule instead —
any correction the server intends travels in the same tick and earlier in the
stream than the receipt.

## The data it owns

`MultiPlayerGameMode` is the client's half of the game mode, and the only
class that can open a prediction: `ClientLevel.getBlockStatePredictionHandler`
is package-private, so nothing outside `client/multiplayer` can reach the
ledger. Its predicting verbs are `MultiPlayerGameMode.startDestroyBlock`,
`MultiPlayerGameMode.continueDestroyBlock`, `MultiPlayerGameMode.useItemOn`
and `MultiPlayerGameMode.useItem`, all funnelling through the private
`MultiPlayerGameMode.startPrediction`, which takes a `PredictiveAction` — a
one-method interface whose `PredictiveAction.predict` receives the sequence
number and returns the packet to send. Its non-predicting verbs matter too,
because the list of what is *not* predicted is half the page:
`MultiPlayerGameMode.attack`, `MultiPlayerGameMode.interact`,
`MultiPlayerGameMode.stopDestroyBlock`,
`MultiPlayerGameMode.releaseUsingItem`, `MultiPlayerGameMode.piercingAttack`
and every container verb.

`BlockStatePredictionHandler` is the ledger: a map from packed block position
to `BlockStatePredictionHandler.ServerVerifiedState` — a block state, a
sequence number, and the player's position at the time — plus
`BlockStatePredictionHandler.currentSequenceNr`,
`BlockStatePredictionHandler.isPredicting` and
`BlockStatePredictionHandler.lastTeleportSequence`. It is auto-closeable,
and all eight of its public members are load-bearing:
`BlockStatePredictionHandler.startPredicting` (which pre-increments, so the
first real sequence is one and zero is never a prediction),
`BlockStatePredictionHandler.currentSequence`,
`BlockStatePredictionHandler.isPredicting`,
`BlockStatePredictionHandler.retainKnownServerState`,
`BlockStatePredictionHandler.updateKnownServerState`,
`BlockStatePredictionHandler.endPredictionsUpTo`,
`BlockStatePredictionHandler.onTeleport` and
`BlockStatePredictionHandler.close`.

On the server there is one integer per connection,
`ServerGamePacketListenerImpl.ackBlockChangesUpTo` — which is also the name
of the method that raises it. The method takes the maximum of the current
value and the incoming sequence; the field is emitted and reset in
`ServerGamePacketListenerImpl.tick`.

## The three writes

Everything the ledger does happens through three methods on `ClientLevel`,
and the difference between them is the whole mechanism.

- **`ClientLevel.setBlock`** — the ordinary write. While a prediction is
  open, and only if the write succeeded, it calls
  `BlockStatePredictionHandler.retainKnownServerState` with the state that
  was there *before*. If the position already has an entry, only the
  sequence is refreshed: the ledger keeps the **first** pre-change state it
  ever saw for that position, and the player position recorded with it.
- **`ClientLevel.setServerVerifiedBlockState`** — every inbound block update
  goes through here. If the position is in the ledger it overwrites the
  entry and the world is not touched, so the prediction stays on screen. If
  it is **not** in the ledger — the common case, for blocks the player did
  not touch — it writes the world immediately.
- **`ClientLevel.syncBlockState`** — the settle. Applies the recorded state
  only if it differs from what is there, with flags
  `Block.UPDATE_NEIGHBORS` + `Block.UPDATE_CLIENTS` +
  `Block.UPDATE_KNOWN_SHAPE`. That third flag suppresses the shape pass, and
  neighbour updates are inert on the client anyway — so the restore is a
  bare state write plus a remesh. The cascade that produced the prediction
  does not re-run on the way back. Reconciliation is correct only because
  every position the cascade touched got its own ledger entry on the way
  out.

## When it runs

A prediction window is a few microseconds long and entirely synchronous: on
the client thread, inside one call from `Minecraft.tick`. The counter is
raised, the local effect runs, the packet is built with the new sequence and
sent, and the window closes — in that order, so the packet is constructed
while the ledger is still recording.

The settle is a packet handler like any other, applied on the client thread
during the frame's drain. The server's half runs in
`ServerGamePacketListenerImpl.tick`, which the server reaches **after**
ticking its levels — so the block updates a level broadcast this tick are
already in the stream ahead of the receipt.

## The trace: a placement the server refuses

```mermaid
sequenceDiagram
    participant MPGM as MultiPlayerGameMode
    participant BSPH as BlockStatePredictionHandler
    participant CL as ClientLevel
    participant SGPL as ServerGamePacketListenerImpl
    participant SPGM as ServerPlayerGameMode

    MPGM->>BSPH: startPredicting — currentSequenceNr becomes n
    MPGM->>CL: performUseItemOn → ItemStack.useOn → setBlock
    CL->>BSPH: retainKnownServerState(pos, air, playerPos) — the truth, filed under n
    MPGM->>SGPL: ServerboundUseItemOnPacket(hand, hit, n)
    MPGM->>BSPH: close — the window shuts; the block is on screen
    SGPL->>SGPL: hasClientLoaded? then ackBlockChangesUpTo(n) — first statement
    SGPL->>SPGM: useItemOn — refused (protection, or a stale hit)
    SGPL->>CL: ClientboundBlockUpdatePacket — the true state of the position
    CL->>BSPH: updateKnownServerState — the entry is overwritten, the world is not
    Note over SGPL: end of the server tick
    SGPL->>CL: ClientboundBlockChangedAckPacket(n)
    CL->>BSPH: endPredictionsUpTo(n) → syncBlockState — air goes back
    BSPH->>CL: Entity.absSnapTo — only if the restored block now intersects the player
```

Four things worth the diagram. The ack is recorded **before** the action is
attempted, so it is already promised. The correction is an ordinary block
update that the ledger *absorbs* rather than applies. The settle is what
finally moves the world, and it is a no-op when the prediction was right — a
correct prediction costs one map removal. And the snap only happens when the
restored block is inside the player.

The ordering is not the same for every packet. `ServerGamePacketListenerImpl.handleUseItemOn` and
`ServerGamePacketListenerImpl.handleUseItem` record the ack as their first statement;
`ServerGamePacketListenerImpl.handlePlayerAction` records it **after** running the break action, which is why the correction
from a refused break is always ahead of the receipt in the stream.

## The six windows

| where | what it predicts locally | what it sends |
|---|---|---|
| `MultiPlayerGameMode.startDestroyBlock`, creative | the block removed at once | `ServerboundPlayerActionPacket` START |
| `MultiPlayerGameMode.startDestroyBlock`, survival | `BlockBehaviour.attack`, then removal if the block breaks instantly | START |
| `MultiPlayerGameMode.continueDestroyBlock`, creative | removal, every five ticks | START |
| `MultiPlayerGameMode.continueDestroyBlock`, at full progress | removal | STOP |
| `MultiPlayerGameMode.useItemOn` | `MultiPlayerGameMode.performUseItemOn` — the block's hook, the empty-hand hook, `ItemStack.useOn` | `ServerboundUseItemOnPacket` |
| `MultiPlayerGameMode.useItem` | `ItemStack.use`, including a transformed held item | `ServerboundUseItemPacket` |

So the ledger covers rather more than "blocks the player placed or broke": it
covers **every** `ClientLevel.setBlock` performed inside one of those
windows. That includes the second half of a door, every position a shape
cascade revisits, and — the only case of its own — `RedStoneOreBlock.attack`,
whose lighting change is not side-gated and therefore files a ledger entry
when you merely left-click redstone ore.

## What the ledger does not cover

- **Breaking progress.** `MultiPlayerGameMode.destroyProgress` and its
  companions are a plain parallel clock with no sequence and no
  reconciliation; the crack overlay is written straight into the client
  level. Only the final removal is predicted.
- **Item use.** `MultiPlayerGameMode.useItem` opens a ledger window, but a
  consumed item, a started use and a cooldown are not block states and the
  ack does nothing for them. They are corrected by other means entirely: the
  living-entity flags in synched data, `ClientboundCooldownPacket`, and the
  menu resend the server performs when the stack changed.
- **Dropping.** `LocalPlayer.drop` predicts the removal from the selected
  slot and sends its action packet with sequence **zero** — a local mutation
  with no rollback path at all.
- **Movement.** Rubber-banding is a different mechanism: an id-matched
  teleport handshake with no sequence and no ledger, described in
  [input to movement](../player/input-to-movement.md). The two systems touch
  at exactly one point — `ClientPacketListener.handleMovePlayer` calls
  `BlockStatePredictionHandler.onTeleport`, so that a teleport disarms the
  ledger's position snap.

## Interfaces

- **Called by:** `Minecraft.handleKeybinds` and `Minecraft.startUseItem` on
  the client; `ServerGamePacketListenerImpl` on the server.
- **Calls into:** `ClientLevel.setBlock` and the two verified-state writes;
  `ServerPlayerGameMode` for the authoritative version of the same action.
- **Crosses the network as:** outbound `ServerboundPlayerActionPacket`,
  `ServerboundUseItemOnPacket` and `ServerboundUseItemPacket`, each carrying
  a sequence; inbound `ClientboundBlockChangedAckPacket`, plus every
  ordinary `ClientboundBlockUpdatePacket` and
  `ClientboundSectionBlocksUpdatePacket`, which pass through the ledger on
  their way to the world.
- **Data-driven by:** nothing. This is protocol, not content.

## Invariants and surprises

- **The ack is sent for actions the server refused.** A break rejected for
  distance, a placement rejected above the build limit, an abort — all of
  them still raise the counter and produce a receipt. Only the ordering rule
  makes the system correct.
- **An unsequenced action produces an ack of zero.** The three-argument
  `ServerboundPlayerActionPacket` constructor defaults the sequence to zero,
  and releasing the mouse mid-dig uses it — so the server sends
  `ClientboundBlockChangedAckPacket` with zero, which settles nothing,
  because no real prediction is ever numbered zero.
- **One ack settles many entries, and can do four different things.** For
  each entry at or below the acknowledged sequence: nothing; remove the
  entry and leave the world alone (the correct prediction); write the state;
  or write the state and snap the player. A single ack can produce all four
  across the map in one pass.
- **Acks collapse.** `ServerGamePacketListenerImpl.ackBlockChangesUpTo`
  takes a maximum and the field is emitted once per connection tick, so five
  sequenced actions in one tick produce one receipt carrying the highest
  number.
- **The ledger keeps the first state, not the latest.** A second prediction
  at a position it already holds refreshes only the sequence. The recorded
  player position is likewise the one from the first retain.
- **One teleport suppresses a whole batch of snaps.**
  `BlockStatePredictionHandler.lastTeleportSequence` is compared against the
  *acknowledged* sequence, not against each entry's, and it is never reset.
- **A too-early stop makes the block come back.** A break released below the
  server's progress threshold changes no block that tick but is still
  acknowledged — so the client settles the entry, restores the stone, and
  the block reappears until the server's own delayed destroy completes and
  broadcasts air.
- **There is no timeout and no cap.** Nothing clears the ledger except a
  settle. While the server considers the client not yet loaded, sequenced
  packets are dropped *before* the ack is recorded, so predictions
  accumulate and the client's guess stands indefinitely. The only reset is a
  new `ClientLevel`.
- **The outbound write and the inbound restore use different flags.** The
  predicted removal in `MultiPlayerGameMode.destroyBlock` writes with
  `Block.UPDATE_IMMEDIATE` in the mix; the restore writes with
  `Block.UPDATE_KNOWN_SHAPE`. One cascades, the other deliberately does not.
- **You cannot open a use window while a dig is running.**
  `Minecraft.startUseItem` is gated on `MultiPlayerGameMode.isDestroying`.
- **Spectators are asymmetric.** `MultiPlayerGameMode.useItem` returns early
  for a spectator, before the window opens; `MultiPlayerGameMode.useItemOn`
  returns *inside* it, so the sequence is burned and the packet is sent
  anyway.

## Where to look

`MultiPlayerGameMode.startPrediction` — the whole client side is that one
private method and its six call sites. `BlockStatePredictionHandler` end to
end; it is under a hundred lines and every one of them matters.
`ClientLevel.setBlock`, `ClientLevel.setServerVerifiedBlockState` and
`ClientLevel.syncBlockState` for the three writes.
`ServerGamePacketListenerImpl.ackBlockChangesUpTo` and
`ServerGamePacketListenerImpl.tick` for the receipt.

---

*Rules: names, never code · how the system works, not how the code reads ·
newest version only · every backticked name passes `tools/verify_names.py`.*
