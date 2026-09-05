# Prediction and acknowledgement

> Verified against **Minecraft 26.2** · Part X · a block placed against a wall the server will not allow: the client shows it, the server refuses it, and a numbered receipt decides when the lie ends.

The client cannot wait a round trip to show you the block you just placed, so
it places it locally and tells the server afterwards. Everybody who has
described this system has described it as a rollback: the client guesses, the
server judges, the ack says yes or no. That is not what happens.
**`ClientboundBlockChangedAckPacket` is a receipt for a number, not a verdict
on an action.** It is sent for actions the server refused exactly as it is
sent for actions it allowed, and for an aborted dig it is sent carrying zero.
What makes the system correct is an ordering rule instead: any correction the
server intends travels *earlier in the stream* than the receipt for it,
because the correction is sent from inside the handler while the receipt is
only a number the connection flushes later.

Part V's [block interaction](../blocks/block-interaction.md) and [block
breaking](../blocks/block-breaking.md) are the two applications, and both
carry the same four-sentence statement of that contract. This page is the
machinery underneath: one ledger per level, one counter per connection, six
windows in which a prediction can be opened, and four methods that between
them decide whether the world moves.

## The cast

| class | what it decides | thread |
|---|---|---|
| `MultiPlayerGameMode` | when a prediction window opens, and what goes in it | Render thread |
| `BlockStatePredictionHandler` | the ledger: what was there before, under which sequence number | Render thread |
| `ClientLevel` | the four writes — the prediction, the absorbed correction, the trigger, the settle | Render thread |
| `PredictiveAction` | a one-method interface: given the sequence, produce the packet | Render thread |
| `ServerGamePacketListenerImpl` | one integer per connection, and when it is emitted | Server thread |
| `ServerPlayerGameMode` | the authoritative version of the same action | Server thread |

## Two state machines, running against each other

The whole mechanism is one small state machine on each side, and neither
knows the other's state. The client's runs per *position*; the server's runs
per *connection*.

```mermaid
stateDiagram-v2
    state "Client — one position in the ledger" as CLIENT {
        [*] --> Absent
        Absent --> Retained : setBlock inside a window, filed under sequence n
        Retained --> Retained : setBlock again here, only the sequence is refreshed
        Retained --> Corrected : setServerVerifiedBlockState, the entry is overwritten and the world is untouched
        Retained --> [*] : endPredictionsUpTo(n), nothing overwrote it, so syncBlockState puts the old state back
        Corrected --> [*] : endPredictionsUpTo(n), syncBlockState writes the absorbed state, which is a no-op if it is already on screen
    }
    state "Server — one integer per connection" as SERVER {
        [*] --> Idle
        Idle --> Raised : ackBlockChangesUpTo(n), the maximum of current and incoming
        Raised --> Raised : another acked action in the same tick
        Raised --> Idle : emitted at the head of ServerGamePacketListenerImpl.tick, then back to minus one
    }
```

Read the two columns as running at different rates. The client's machine
advances several times per tick, once per position touched. The server's
advances on every packet that reaches a
`ServerGamePacketListenerImpl.ackBlockChangesUpTo` call — the two
use packets, and the three destroy actions of `ServerboundPlayerActionPacket`
but not its other five — and *empties* once per connection tick, which is why
five acked actions in one tick produce one receipt carrying the highest
number, and why one ack can drive a dozen positions out of the ledger at once.

Note what the diagram does not contain: any transition on which the server
says *no*. There is none. Both of the client's exit transitions are driven by
the same packet, and which of the two a position takes is decided entirely by
whether a block update reached it first.

## The four writes

Everything the ledger does happens through four methods on `ClientLevel`, and
the difference between them is the whole mechanism.

**`ClientLevel.setBlock`** — the ordinary write. While a prediction is open,
and only if the write succeeded, it calls
`BlockStatePredictionHandler.retainKnownServerState` with the state that was
there *before*. If the position already has an entry, only the sequence is
refreshed: the ledger keeps the **first** pre-change state it ever saw for
that position, and the player position recorded with it.

**`ClientLevel.setServerVerifiedBlockState`** — every inbound block update
goes through here. If the position is in the ledger it overwrites the entry
and the world is not touched, so the prediction stays on screen. If it is
**not** in the ledger — the common case, for blocks the player did not touch
— it writes the world immediately. The absorption is per position, not per
packet.

**`ClientLevel.handleBlockChangedAck`** — the trigger. The ledger's only
entry point from the network: it hands the receipt's number straight to
`BlockStatePredictionHandler.endPredictionsUpTo`, which removes every entry at
or below it and passes each one's recorded state to the settle.

**`ClientLevel.syncBlockState`** — the settle. Applies the recorded state
only if it differs from what is there, with flags `Block.UPDATE_NEIGHBORS`
plus `Block.UPDATE_CLIENTS` plus `Block.UPDATE_KNOWN_SHAPE`. That third flag
suppresses the shape pass, and neighbour updates are inert on the client
anyway — so the restore is a bare state write plus a remesh. **The cascade
that produced the prediction does not re-run on the way back.**
Reconciliation is correct only because every position the cascade touched got
its own ledger entry on the way out.

## A placement the server refuses

The state diagram says what the states are; this says what order the packets
arrive in, which is the part correctness actually rests on.

```mermaid
sequenceDiagram
    participant MPGM as MultiPlayerGameMode
    participant BSPH as BlockStatePredictionHandler
    participant CL as ClientLevel
    participant SGPL as ServerGamePacketListenerImpl
    participant SPGM as ServerPlayerGameMode

    MPGM->>BSPH: startPredicting — currentSequenceNr becomes n
    MPGM->>CL: performUseItemOn, then ItemStack.useOn, then setBlock
    CL->>BSPH: retainKnownServerState(pos, air, LocalPlayer) — the truth, filed under n
    MPGM->>SGPL: ServerboundUseItemOnPacket(hand, hit, n)
    MPGM->>BSPH: close — the window shuts and the block is on screen
    SGPL->>SGPL: hasClientLoaded? then ackBlockChangesUpTo(n) — the first statement
    SGPL->>SPGM: useItemOn — the place fails canPlace, so nothing changes
    SGPL->>CL: two ClientboundBlockUpdatePackets, sent whatever the outcome — the clicked block and the one past its face
    CL->>BSPH: updateKnownServerState — the entry is overwritten, the world is not
    Note over SGPL: the connection phase of the next tickChildren
    SGPL->>CL: ClientboundBlockChangedAckPacket(n)
    CL->>BSPH: endPredictionsUpTo(n), then syncBlockState — air goes back
    CL->>CL: Entity.absSnapTo on the LocalPlayer — only if the restored block now intersects it
```

The ack is recorded **before** the action is attempted, so by the time the
refusal happens the receipt is already promised. The correction is not the
ordinary chunk broadcast but a targeted pair of resends the handler makes
unconditionally, which is what actually puts it ahead of the receipt: the
resends go out inside the handler, while the ack is only a field assignment
that `ServerGamePacketListenerImpl.tick` flushes later. The settle is what
finally moves the world, and it is a no-op when the absorbed state is already
what is on screen. And the snap only happens when the restored block turns
out to be inside the player.

Because the ack is buffered rather than sent, *where* a handler records it
does not affect stream order — `ServerGamePacketListenerImpl.handleUseItemOn`
and `ServerGamePacketListenerImpl.handleUseItem` record it as their first
statement, `ServerGamePacketListenerImpl.handlePlayerAction` after running the
break action, and in both cases the correction still reaches the client first.

## The six windows

A window is a few microseconds long and entirely synchronous: on the client
thread, inside one call from `Minecraft.tick`. The counter is raised, the
local effect runs, the packet is built with the new sequence and sent, and the
window closes — in that order, so the packet is constructed while the ledger
is still recording. `MultiPlayerGameMode.startPrediction` is the private
method all six go through, and `ClientLevel.getBlockStatePredictionHandler`
is package-private, so nothing outside `client/multiplayer` can reach the
ledger at all.

| where | what it predicts locally | what it sends |
|---|---|---|
| `MultiPlayerGameMode.startDestroyBlock`, creative | the block removed at once | `ServerboundPlayerActionPacket` START |
| `MultiPlayerGameMode.startDestroyBlock`, survival | `BlockBehaviour.attack`, then removal if the block breaks instantly | START |
| `MultiPlayerGameMode.continueDestroyBlock`, creative | removal, every sixth tick | START |
| `MultiPlayerGameMode.continueDestroyBlock`, at full progress | removal | STOP |
| `MultiPlayerGameMode.useItemOn` | `MultiPlayerGameMode.performUseItemOn` — the block's hook, the empty-hand hook, `ItemStack.useOn` | `ServerboundUseItemOnPacket` |
| `MultiPlayerGameMode.useItem` | `ItemStack.use`, including a transformed held item | `ServerboundUseItemPacket` |

So the ledger covers rather more than "blocks the player placed or broke": it
covers **every** `ClientLevel.setBlock` performed inside one of those windows.
That includes the second half of a door, every position a shape cascade
revisits, and — the only case of its own — `RedStoneOreBlock.attack`, whose
lighting change is not side-gated and therefore files a ledger entry when you
merely left-click redstone ore.

## What the ledger does not cover

Half the value of this page is the list of things people assume it handles.
`MultiPlayerGameMode`'s non-predicting verbs are the giveaway:
`MultiPlayerGameMode.attack`, `MultiPlayerGameMode.interact`,
`MultiPlayerGameMode.stopDestroyBlock`,
`MultiPlayerGameMode.releaseUsingItem`,
`MultiPlayerGameMode.piercingAttack` and every container verb open no window
at all.

- **Breaking progress.** `MultiPlayerGameMode.destroyProgress` and its
  companions are a plain parallel clock with no sequence and no
  reconciliation; the crack overlay is written straight into the client
  level. Of the progress clock itself nothing is predicted — only the
  removals at either end of it are.
- **Item use.** `MultiPlayerGameMode.useItem` opens a window, but a consumed
  item, a started use and a cooldown are not block states and the ack does
  nothing for them. They are corrected by other means: the living-entity
  flags in synched data, `ClientboundCooldownPacket`, and the menu resend the
  server performs when the stack changed.
- **Dropping.** `LocalPlayer.drop` predicts the removal from the selected
  slot and sends its action packet with sequence **zero** — a local mutation
  with no rollback path at all.
- **Movement.** Rubber-banding is a different mechanism entirely: an
  id-matched teleport handshake with no sequence and no ledger, described in
  [input to movement](../player/input-to-movement.md). The two systems touch
  at one point in each direction — `ClientPacketListener.handleMovePlayer`
  calls `BlockStatePredictionHandler.onTeleport`, so a teleport disarms the
  ledger's position snap, and the settle calls `Entity.absSnapTo` on the
  `LocalPlayer` when
  the restored block is inside you.

## Questions players ask

**Why does the block come back and then vanish again?** Your client finished
its own progress clock first. It fires the STOP window and removes the block
locally, but the server recomputes the progress itself, finds it under
`0.7F`, and takes the delayed-destroy branch instead of breaking anything.
The action is acknowledged all the same, so the client settles the entry,
restores the stone, and the block reappears — until the server's own delayed
destroy completes a few ticks later and broadcasts air. Releasing the mouse
does *not* do this: that is `MultiPlayerGameMode.stopDestroyBlock`, which
opens no window at all.

**Why did that ack arrive with a zero in it?** The three-argument
`ServerboundPlayerActionPacket` constructor defaults the sequence to zero,
and aborting a dig uses it. The server dutifully sends
`ClientboundBlockChangedAckPacket` carrying zero, which settles nothing —
`BlockStatePredictionHandler.startPredicting` pre-increments, so the first
real sequence is one and no genuine prediction is ever numbered zero.

**Can a wrong guess get stuck on screen forever?** Yes. There is no timeout
and no cap: nothing clears the ledger except a settle, and while the server
considers the client not yet loaded, sequenced packets are dropped *before*
the ack is recorded. Predictions accumulate and the client's guess stands.
The only reset is a new `ClientLevel`.

**Does one ack do one thing?** It does three. Every entry at or below the
acknowledged sequence is removed and handed to the settle, and there the
paths part: write nothing, because the recorded state is already on screen
(the correct prediction); write the state; or write the state and snap the
player. A single ack can produce all three across the map in one pass. And
`BlockStatePredictionHandler.lastTeleportSequence` is compared against the
*acknowledged* sequence rather than each entry's, and is never reset, so one
teleport suppresses a whole batch of snaps.

**Why can I not right-click while mining?** `Minecraft.startUseItem` is gated
on `MultiPlayerGameMode.isDestroying`. Spectators are the odd case in the
other direction and are asymmetric about it:
`MultiPlayerGameMode.useItem` returns early, before the window opens, while
`MultiPlayerGameMode.useItemOn` returns *inside* it — so the sequence is
burned and the packet is sent anyway.

One last asymmetry worth carrying away: the outbound write and the inbound
restore use different flags. The predicted removal in
`MultiPlayerGameMode.destroyBlock` writes with `Block.UPDATE_IMMEDIATE` in
the mix; the restore writes with `Block.UPDATE_KNOWN_SHAPE`. One cascades,
the other deliberately does not.

## Where to look

`MultiPlayerGameMode.startPrediction` — the whole client side is that one
private method and its six call sites. `BlockStatePredictionHandler` end to
end; it is under a hundred lines and every one of them matters, including
`BlockStatePredictionHandler.currentSequence`,
`BlockStatePredictionHandler.isPredicting` and
`BlockStatePredictionHandler.close`. `ClientLevel.setBlock`,
`ClientLevel.setServerVerifiedBlockState`, `ClientLevel.handleBlockChangedAck`
and `ClientLevel.syncBlockState` for the four writes. `ServerGamePacketListenerImpl.ackBlockChangesUpTo` and
`ServerGamePacketListenerImpl.tick` for the receipt — the field and the
method that raises it share a name.

---

*Rules: names, never code · how the system works, not how the code reads ·
newest version only · every backticked name passes `tools/verify_names.py`.*
