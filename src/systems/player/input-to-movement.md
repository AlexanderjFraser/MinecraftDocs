# Input to movement

> Verified against **Minecraft 26.2** · Part VIII · W is pressed: the key becomes a boolean, the boolean becomes a velocity, the velocity becomes a packet, and the server decides whether to believe it.

## Responsibility

The player is the one entity the server does not control. Everything in
this page exists to reconcile that: the client simulates its own movement
and reports the result, and the server's job is to decide whether the
reported result is plausible, apply it, and rubber-band the client when it
is not.

The one sentence a player recognises: *I press W and I walk — unless the
server disagrees, and then I snap back.*

The headline for a 1.21-era reader: **the server runs the whole physics
pipeline for a human player every tick and then throws the position
away.** It simulates in order to know what the player's velocity *ought*
to be, because that is the number the anti-cheat check compares against.

## The data it owns

### On the client

- **`KeyMapping`** — one object per bindable action. `KeyMapping.ALL` is
  the by-name registry, `KeyMapping.MAP` the physical-key reverse index
  rebuilt by `KeyMapping.resetMapping`. Each holds `KeyMapping.isDown` and
  `KeyMapping.clickCount`. **`KeyMapping.consumeClick` is a counter drain,
  not an edge test** — call sites loop on it — but the movement keys never
  use it; they are polled with `KeyMapping.isDown`.
  `KeyMapping.Category` is a *record* now, with constants like
  `KeyMapping.Category.MOVEMENT` and a public
  `KeyMapping.Category.register` for mods.
- **`ToggleKeyMapping`** — `Options.keyShift` and `Options.keySprint` are
  these; hold-versus-toggle lives entirely in
  `ToggleKeyMapping.setDown`, driven by `Options.toggleCrouch` and
  `Options.toggleSprint`. Nothing downstream knows the difference.
- **`Options`** — the movement bindings: `Options.keyUp`,
  `Options.keyDown`, `Options.keyLeft`, `Options.keyRight`,
  `Options.keyJump`, `Options.keyShift`, `Options.keySprint`. Plus
  `Options.autoJump` and `Options.sprintWindow` (the double-tap window in
  ticks, default seven, zero to disable).
- **`Input`** (`world/entity/player`) — a **shared** record of seven
  booleans (forward, backward, left, right, jump, shift, sprint) with
  `Input.EMPTY` and an `Input.STREAM_CODEC` that packs all seven into one
  byte (`Input.FLAG_FORWARD` … `Input.FLAG_SPRINT`).
- **`ClientInput`** — `ClientInput.keyPresses` (an `Input`) plus
  `ClientInput.moveVector` (a `Vec2`, where `Vec2.x` is the *left*
  impulse and `Vec2.y` the *forward* one). `ClientInput.makeJump` is how
  auto-jump fakes a press. The subclass that actually reads the keyboard
  is **`KeyboardInput`**, whose `KeyboardInput.tick` builds a fresh
  `Input` from the seven `KeyMapping.isDown` values and normalises the
  axes through `KeyboardInput.calculateImpulse`.
- **`LocalPlayer`** — the send-tracking block: `LocalPlayer.xLast`,
  `LocalPlayer.yLast`, `LocalPlayer.zLast`, `LocalPlayer.yRotLast`,
  `LocalPlayer.xRotLast`,
  `LocalPlayer.lastOnGround`, `LocalPlayer.lastHorizontalCollision`,
  `LocalPlayer.positionReminder` (against
  `LocalPlayer.POSITION_REMINDER_INTERVAL`, twenty),
  `LocalPlayer.lastSentInput`, `LocalPlayer.wasSprinting`,
  `LocalPlayer.sprintTriggerTime`, `LocalPlayer.autoJumpEnabled`,
  `LocalPlayer.autoJumpTime`, `LocalPlayer.crouching`.

`LocalPlayer.input` starts as a bare `ClientInput` and is replaced with a
`KeyboardInput` by `ClientPacketListener` on login and on respawn — which
is why a respawned player's input object is a different one.

### On the server

`ServerGamePacketListenerImpl` holds the whole judgement:
`ServerGamePacketListenerImpl.firstGoodX` and its siblings (where the
tick started), `ServerGamePacketListenerImpl.lastGoodX` and its siblings
(the last accepted position),
`ServerGamePacketListenerImpl.awaitingPositionFromClient`,
`ServerGamePacketListenerImpl.awaitingTeleport`,
`ServerGamePacketListenerImpl.awaitingTeleportTime`,
`ServerGamePacketListenerImpl.clientIsFloating`,
`ServerGamePacketListenerImpl.aboveGroundTickCount`,
`ServerGamePacketListenerImpl.receivedMovePacketCount`,
`ServerGamePacketListenerImpl.knownMovePacketCount`,
`ServerGamePacketListenerImpl.receivedMovementThisTick`, and the vehicle
equivalents (`ServerGamePacketListenerImpl.lastVehicle`,
`ServerGamePacketListenerImpl.vehicleFirstGoodX`,
`ServerGamePacketListenerImpl.vehicleLastGoodX`,
`ServerGamePacketListenerImpl.clientVehicleIsFloating`). `ServerPlayer.lastKnownClientMovement` is the
observed per-tick displacement, and `ServerPlayer.lastClientInput` is the
raw key state.

**There are no named threshold constants.** The numbers in the movement
checks are inline literals; the only named ones nearby are
`ServerGamePacketListenerImpl.MAXIMUM_FLYING_TICKS` (80) and
`ServerGamePacketListenerImpl.CLIENT_LOADED_TIMEOUT_TIME` (60).

## When it runs

Keys are **sampled inside the tick, not pushed from the callback.** The
GLFW callback builds a `KeyEvent` and immediately defers to the render
thread with `Minecraft.execute`; `KeyboardHandler.keyPress` only sets
`KeyMapping.isDown` and bumps `KeyMapping.clickCount`. The read happens
once per game tick, deep inside `LocalPlayer.aiStep`, which calls
`ClientInput.tick`.

Mouse look is the exception: `MouseHandler.handleAccumulatedMovement` runs
**per frame**, in `Minecraft.runTick` after the tick loop, and
`MouseHandler.turnPlayer` calls `Entity.turn` directly. Rotation is
therefore finer-grained than position.

On the server the ordering is the whole story:

1. `MinecraftServer.processPacketsAndTick` drains `PacketProcessor`
   **before** `MinecraftServer.tickServer`. Every movement packet for the
   tick is applied first, ahead of any level ticking.
2. The levels tick.
3. `MinecraftServer.tickChildren` reaches its connection phase, and
   `ServerGamePacketListenerImpl.tick` runs
   `ServerGamePacketListenerImpl.tickPlayer` — the simulate-and-discard
   step, and the place the floating check is enforced.

## The trace: W is pressed

```mermaid
sequenceDiagram
    participant KH as KeyboardHandler
    participant KM as KeyMapping
    participant KI as KeyboardInput
    participant LP as LocalPlayer
    participant LE as LivingEntity
    participant CL as ServerGamePacketListenerImpl
    participant SP as ServerPlayer

    KH->>KM: set — isDown = true; nothing else happens yet
    LP->>KI: tick — from inside aiStep: poll seven keys into one Input
    KI->>LP: applyInput — moveVector becomes xxa/zza, jump becomes jumping
    LP->>LE: travel — travelInAir, then Entity.move: the client is authoritative
    LP->>CL: ServerboundPlayerInputPacket — only when the key set changed
    LP->>CL: ServerboundMovePlayerPacket.PosRot — sendPosition decides which variant
    CL->>CL: moved too quickly? — squared delta vs getDeltaMovement, budget 100 or 300
    CL->>SP: move(MoverType.PLAYER) — the only place the server position advances
    CL->>CL: moved wrongly? — residual over 0.0625, then noCollision / new-collider test
    CL->>LP: ClientboundPlayerPositionPacket — rubber-band, awaiting an ack
    CL->>SP: doTick — simulate the whole tick, then absSnapTo(firstGood…) and discard
```

**The client half.** `KeyboardInput.tick` builds an `Input` from the seven
keys and a normalised `Vec2`. `LocalPlayer.applyInput` — overriding a
`LivingEntity.applyInput` that does nothing but decay them —
turns that into the `LivingEntity.xxa` and `LivingEntity.zza` movement
fields, after passing it through
`LocalPlayer.modifyInput`: the item-use slowdown (from
`LocalPlayer.itemUseSpeedMultiplier`), `Attributes.SNEAKING_SPEED` when
moving slowly, and `LocalPlayer.modifyInputSpeedForSquareMovement`, the
diagonal correction. From there it is ordinary
[movement and collision](../entities/movement-and-collision.md):
`LivingEntity.travel` → `LivingEntity.travelInAir` →
`LivingEntity.moveRelative` → `Entity.move`.

Sprint is decided in `LocalPlayer.aiStep` before that:
`LocalPlayer.canStartSprinting` gates it, and the double-tap is
`LocalPlayer.sprintTriggerTime`, armed with `Options.sprintWindow` when
the forward key *releases* and consumed when it is pressed again.
`LocalPlayer.shouldStopRunSprinting` ends it. Auto-jump is
`LocalPlayer.updateAutoJump` (called from `LocalPlayer.move`) setting
`LocalPlayer.autoJumpTime`, which makes the *next* tick call
`ClientInput.makeJump`.

**What goes on the wire.** `LocalPlayer.sendPosition` picks the variant:
`ServerboundMovePlayerPacket.PosRot` when both changed,
`ServerboundMovePlayerPacket.Pos` or `.Rot` for one,
`ServerboundMovePlayerPacket.StatusOnly` when only the ground or
collision flag changed, and **nothing at all** when nothing changed —
except that a position is re-sent every twenty ticks regardless, via
`LocalPlayer.positionReminder`. The two booleans ride in one byte
(`ServerboundMovePlayerPacket.FLAG_ON_GROUND`,
`ServerboundMovePlayerPacket.FLAG_HORIZONTAL_COLLISION`).
`ServerboundPlayerInputPacket` is sent only when the key set *changes*,
and `ServerboundClientTickEndPacket` — a zero-byte singleton — closes
every client tick.

**The server half.** `ServerGamePacketListenerImpl.handleMovePlayer`
rejects non-finite values outright (disconnect), discards the position
entirely while a teleport is outstanding, clamps to ±3×10⁷ horizontally,
and returns early for a passenger — **riders never move themselves**.
Then two checks:

- *moved too quickly*: the squared distance from `firstGood…` minus
  `Entity.getDeltaMovement().lengthSqr()` against a budget of **100 per
  packet, or 300 while fall-flying**, scaled by how many move packets
  arrived since the last tick. Skipped for the singleplayer host, during a
  dimension change, and when `GameRules.PLAYER_MOVEMENT_CHECK` is off
  (`GameRules.ELYTRA_MOVEMENT_CHECK` covers the elytra case). Failure
  teleports the player back and returns.
- The move is then actually applied —
  `ServerPlayer.move` with `MoverType.PLAYER` — and *moved wrongly*
  measures what is left over: a residual above `0.0625` while not
  changing dimension, sleeping, creative, spectating or inside
  `LivingEntity.isInPostImpulseGraceTime` (the mace and wind-charge
  exemption). A failure only rubber-bands if the old box was in fact
  clear, or if
  `ServerGamePacketListenerImpl.isEntityCollidingWithAnythingNew` says the
  player ended up inside a collider it was not already inside.

Accepting means `ServerPlayer.absSnapTo`, `ServerChunkCache.move`,
`Entity.setOnGroundWithMovement`, `Entity.doCheckFallDamage`,
`ServerGamePacketListenerImpl.handlePlayerKnownMovement` and
`ServerPlayer.checkMovementStatistics` — the walked-distance statistics
are computed from the *client's reported* delta, never from a simulation.

**The teleport handshake.** `ServerGamePacketListenerImpl.teleport` bumps
`ServerGamePacketListenerImpl.awaitingTeleport`, moves the player with `Entity.teleportSetPosition`,
records `ServerGamePacketListenerImpl.awaitingPositionFromClient` and sends
`ClientboundPlayerPositionPacket` (a `PositionMoveRotation` plus a set of
`Relative` flags saying which fields are deltas).
`ServerGamePacketListenerImpl.updateAwaitingTeleport` **re-sends after
twenty ticks** if no acknowledgement arrives, and until it does, every
incoming move packet contributes rotation only. The client replies with
`ServerboundAcceptTeleportationPacket` *and* an immediate
`ServerboundMovePlayerPacket.PosRot`, then calls
`BlockStatePredictionHandler.onTeleport` to drop its outstanding block
predictions ([block interaction](../blocks/block-interaction.md)).
`ClientboundPlayerRotationPacket` is the rotation-only sibling.

## Interfaces

- **Called by:** `Minecraft.tick` (client, via `ClientLevel` and
  `Minecraft.handleKeybinds`); `PacketProcessor` and
  `MinecraftServer.tickChildren` (server).
- **Calls into:** `LivingEntity.travel` and `Entity.move`
  ([movement and collision](../entities/movement-and-collision.md));
  `ServerChunkCache.move`, which is what makes chunks load as you walk
  ([tickets and loading](../world/tickets-and-loading.md)).
- **Crosses the network as:** `ServerboundMovePlayerPacket` and its four
  variants, `ServerboundPlayerInputPacket`,
  `ServerboundPlayerCommandPacket` (with
  `ServerboundPlayerCommandPacket.Action` — sprint, sneak-exit, ride-jump,
  open-inventory, start-fall-flying), `ServerboundMoveVehiclePacket`,
  `ServerboundAcceptTeleportationPacket`,
  `ServerboundClientTickEndPacket`; and back,
  `ClientboundPlayerPositionPacket`, `ClientboundPlayerRotationPacket`,
  `ClientboundMoveVehiclePacket`.
- **Data-driven by:** almost nothing —
  `GameRules.PLAYER_MOVEMENT_CHECK` and `GameRules.ELYTRA_MOVEMENT_CHECK`
  ([level data and rules](../world/level-data-and-rules.md)), plus the
  movement attributes.

## Invariants and surprises

- **The server simulates the player fully, then deletes the answer.**
  `ServerGamePacketListenerImpl.tickPlayer` calls `ServerPlayer.doTick` —
  the whole `LivingEntity.aiStep` / `LivingEntity.travel` / `Entity.move`
  pipeline runs
  server-side — and the very next thing it does is snap the player back to
  where the tick started. The simulation exists for
  `Entity.getDeltaMovement`, which is the *expected* distance the
  anti-cheat subtracts. The authoritative position only ever moves in
  `ServerGamePacketListenerImpl.handleMovePlayer` or through a teleport.
- **The server never uses `ServerboundPlayerInputPacket` to move
  anybody.** `ServerPlayer.setLastClientInput` feeds exactly two
  consumers: `ServerPlayer.getLastClientMoveIntent` and an
  `InputPredicate` for advancements. Boats are steered client-side
  (`LocalPlayer.rideTick` → `AbstractBoat.setInput`) and the *result* is
  shipped as `ServerboundMoveVehiclePacket`.
- **The vertical residual in *moved wrongly* is dead code.** The guard
  that zeroes it is a disjunction that is true for every finite double, so
  the 0.0625 check is horizontal-only in practice — in both the player and
  the vehicle handler.
- **Sending move packets faster makes the check stricter.** The
  per-packet budget normally scales with how many packets arrived, but
  above five the code clamps the count to one — so a flood gets a
  one-packet budget for a many-packet displacement. There is no throttle
  or kick for the flood itself; only chat, commands and item drops have a
  `TickThrottler`.
- **Riders are not checked at all.** A passenger's move packet
  contributes rotation and nothing else; the vehicle's own packet has a
  flat budget of 100, no elytra case, no game rule, and no
  horizontal-collision flag.
- **The flying kick scales with gravity, upward only.**
  `ServerGamePacketListenerImpl.getMaximumFlyingTicks` returns
  an effectively unbounded budget below a gravity of 10⁻⁵ and otherwise stretches the
  eighty-tick budget as gravity falls. `ServerGamePacketListenerImpl.clientIsFloating` is separately
  suppressed by spectator mode, `Abilities.mayfly`, the server's own
  allow-flight setting, `MobEffects.LEVITATION`, fall-flying and riptide.
- **A key tapped between ticks is lost.** Movement polls
  `KeyMapping.isDown`, so a press shorter than a tick never happens —
  unlike the `KeyMapping.consumeClick` keys, where three taps in one tick
  fire three times.
- **`Options.autoJump` is read inside a networking method.**
  `LocalPlayer.autoJumpEnabled` is refreshed in `LocalPlayer.sendPosition`,
  which does not run for a passenger or a non-camera player — so the
  setting quietly stops tracking in those states.
- **`ServerboundPlayerCommandPacket` carries an entity id the server never
  validates** against the sender.

## Where to look

`KeyboardHandler` · `KeyMapping` · `ToggleKeyMapping` · `Options` ·
`ClientInput` · `KeyboardInput` · `Input` · `LocalPlayer` ·
`MouseHandler` · `ServerboundMovePlayerPacket` ·
`ServerboundPlayerInputPacket` · `ServerGamePacketListenerImpl` ·
`ClientboundPlayerPositionPacket` · `PositionMoveRotation` · `Relative` ·
`PacketProcessor` · `TickThrottler`

---

*Rules: names, never code · how the system works, not how the code reads ·
newest version only · every backticked name passes `tools/verify_names.py`.*
