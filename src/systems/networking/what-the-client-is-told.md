# What the client is told

> Verified against **Minecraft 26.2** · Part IX · a creeper walks into view: everything the server decides to say, in order, and everything it decides not to.

## Responsibility

The server has the world. The client has a copy, and the copy is
deliberately incomplete. This page is about the choosing: which chunks a
player is sent and how fast, which entities they are told about, what
counts as a change worth a packet, and what the client invents to fill
the gaps.

The one sentence a player would recognise: *the world loads in, and mobs
appear when they get close enough.*

The headline for a 1.21-era reader: **`ClientLevel` is not a cache, it is
a fiction that is periodically corrected.** It never admits a chunk is
missing, it ticks entities it does not own — while refusing to simulate
their movement or their AI — it computes its own light, and it guesses at
block placements and rolls them back. And the introduction packet for a
new entity describes not where the entity *is* but where the tracker last
*said* it was.

## The data it owns

### On the server

- **`PlayerChunkSender`** — one per connection, reachable as
  `ServerGamePacketListenerImpl.chunkSender`. It holds
  `PlayerChunkSender.pendingChunks` (packed positions),
  `PlayerChunkSender.desiredChunksPerTick` (what the *client* asked
  for), `PlayerChunkSender.batchQuota` (a fractional budget
  accumulator), and `PlayerChunkSender.unacknowledgedBatches` against
  `PlayerChunkSender.maxUnacknowledgedBatches`. The clamps are
  `PlayerChunkSender.MIN_CHUNKS_PER_TICK` and
  `PlayerChunkSender.MAX_CHUNKS_PER_TICK`.
- **`ChunkTrackingView`** — the set of chunks a player has been sent.
  `ChunkTrackingView.Positioned` is a centre and a radius, and
  `ChunkTrackingView.difference` is what turns a movement into an
  enter/leave pair. It is round-cornered rather than
  either a disc or a square: `ChunkTrackingView.isWithinDistance`
  shrinks each axis delta by a small buffer *before* the squared compare,
  so the region reaches a chunk further along each axis than it does
  diagonally. `ChunkTrackingView.Positioned` iterates one chunk beyond
  the view distance for exactly that reason.
- **`ChunkMap.TrackedEntity`** — one per tracked entity, holding the
  `ServerEntity`, the range in blocks, the last section, and
  `ChunkMap.TrackedEntity.seenBy`, an identity set of connections. It
  implements `ServerEntity.Synchronizer`, whose three verbs are
  `ServerEntity.Synchronizer.sendToTrackingPlayers`,
  `ServerEntity.Synchronizer.sendToTrackingPlayersAndSelf` and
  `ServerEntity.Synchronizer.sendToTrackingPlayersFiltered`.
- **`ServerEntity`** — the change detector. It owns the dead-reckoning
  baseline: `ServerEntity.positionCodec` (a `VecDeltaCodec`),
  `ServerEntity.lastSentYRot`, `ServerEntity.lastSentXRot`,
  `ServerEntity.lastSentYHeadRot`, `ServerEntity.lastSentMovement`, plus `ServerEntity.tickCount`,
  `ServerEntity.teleportDelay`, `ServerEntity.lastPassengers`,
  `ServerEntity.wasRiding` and `ServerEntity.wasOnGround`. Its four
  constants are `ServerEntity.TOLERANCE_LEVEL_POSITION`,
  `ServerEntity.TOLERANCE_LEVEL_ROTATION`,
  `ServerEntity.FORCED_POS_UPDATE_PERIOD` and
  `ServerEntity.FORCED_TELEPORT_PERIOD`.
- **`ChunkHolder`** — the per-chunk block-change batch:
  `ChunkHolder.changedBlocksPerSection`, one short set per section,
  plus `ChunkHolder.skyChangedLightSectionFilter` and
  `ChunkHolder.blockChangedLightSectionFilter`. See
  [tickets and loading](../world/tickets-and-loading.md).

`ServerEntity.trackedDataValues` is the cached snapshot of the entity's
non-default synched values, refreshed whenever dirty data is flushed; it
is what a *new* viewer is replayed.

Per-entity tracking parameters are on the type:
`EntityType.clientTrackingRange` (in chunks) and
`EntityType.updateInterval` (in ticks), both builder values.
`EntityType.trackDeltas` looks like a third but is a hardcoded exclusion
list — players, llama spit, the wither, bats, item frames, leash knots,
paintings, end crystals and evoker fangs are out, everything else is in.

Two flags on the entity itself override all of this, and both are public
fields rather than anything ceremonious. **`Entity.needsSync`** forces
the issue at three separate decisions — whether `ChunkMap` calls the
change detector at all, whether the interval gate opens, and whether
velocity is re-sent — and is set by being pushed, by being loaded from
disk, and by a dozen classes for their own reasons.
**`Entity.syncPosition`** does something subtler: it re-phases the call
counter to the next interval boundary, so a bounced entity syncs at once
rather than up to an interval late.

### On the client

- **`ClientPacketListener`** — applies everything. It holds
  `ClientPacketListener.serverChunkRadius`,
  `ClientPacketListener.serverSimulationDistance` and the
  `ChunkBatchSizeCalculator`.
- **`ChunkBatchSizeCalculator`** — the round-trip meter, with
  `ChunkBatchSizeCalculator.aggregatedNanosPerChunk`,
  `ChunkBatchSizeCalculator.oldSamplesWeight` against
  `ChunkBatchSizeCalculator.MAX_OLD_SAMPLES_WEIGHT`, and
  `ChunkBatchSizeCalculator.CLAMP_COEFFICIENT`.
- **`ClientChunkCache`** and its nested `ClientChunkCache.Storage` — a
  fixed **torus** of chunk slots, `ClientChunkCache.Storage.chunks`, an
  atomic array of `(2r+1)²` entries indexed modulo the view range, with
  volatile centre coordinates because the render thread reads them.
- **`ClientLevel`** — `ClientLevel.tickingEntities`,
  `ClientLevel.entityStorage` (a `TransientEntitySectionManager`, not
  the server's persistent one), `ClientLevel.lightUpdateQueue`,
  `ClientLevel.destroyingBlocks`, `ClientLevel.tintCaches`,
  `ClientLevel.clientLevelData`, and the prediction ledger
  `BlockStatePredictionHandler`.

## When it runs

Everything the server sends is decided on the **server main thread**, in
a fixed order within the tick:

1. `ServerLevel.tick` runs `ServerChunkCache.tick`, whose
   `ServerChunkCache.tickChunks` calls
   `ServerChunkCache.broadcastChangedChunks` — one flush of all block
   changes accumulated this tick — and then `ChunkMap.tick`, which
   re-evaluates entity visibility and calls `ServerEntity.sendChanges`.
   Both run **before** the entity-tick phase — but well after the
   scheduled block and fluid ticks, the random ticks and mob spawning.
   So a broadcast carries this tick's block changes and the *previous*
   tick's entity-driven ones.
2. After every level has ticked, `MinecraftServer.tickChildren` runs the
   chunk-sending phase: `PlayerChunkSender.sendNextChunks` once per
   player.
3. Flushing is suspended for the whole tick and resumed at the end of
   that phase, so one tick of traffic to one player is one flush — see
   [the connection](the-connection.md).

On the client the cadence is the other way round.
`PacketProcessor.processQueuedPackets` runs **once per frame**, inside
`Minecraft.runTick` and *before* that frame's client ticks — of which
there may be none, or as many as ten. So a burst of packets is applied in
one lump, but the lump lands between frames, not between ticks: at a high
frame rate the client applies the server's updates far more often than it
ticks.

Eight of `ClientPacketListener`'s handlers never hop at all and run on
the Netty thread. Two of them are on the chunk path —
`ClientPacketListener.handleChunkBatchStart` and
`ClientPacketListener.handleChunkBatchFinished` — and the rest are the
combat-state pair, the custom payload, the debug sample, the pong and
the low-disk-space warning.

## Chunk sending

`ChunkMap.applyChunkTrackingView` diffs the player's old and new tracking
discs; entering chunks are queued with
`PlayerChunkSender.markChunkPendingToSend`; leaving chunks are dropped
with `ClientboundForgetLevelChunkPacket` — unless they were still only
pending, in which case they leave the queue and the client is told
nothing, because it was never told anything.
A chunk that only *becomes* ready is queued by
`ChunkMap.onChunkReadyToSend`. When the centre moves, a
`ClientboundSetChunkCacheCenterPacket` goes first. The radius is the
client's requested view distance clamped between `ChunkMap.MIN_VIEW_DISTANCE`
and the server's own.

`PlayerChunkSender.sendNextChunks` then, each tick:

- stops if too many batches are unacknowledged —
  `PlayerChunkSender.maxUnacknowledgedBatches` **starts at one** and is
  raised to ten on the first acknowledgement, so the first batch after
  login is a hard round-trip barrier;
- accumulates `PlayerChunkSender.batchQuota` by the client's desired
  rate and stops if it is below one;
- takes that many chunks, **nearest first**, from
  `PlayerChunkSender.pendingChunks` — or, on a memory connection or
  whenever fewer are pending than the budget allows, all of them at once;
- brackets them with `ClientboundChunkBatchStartPacket` and
  `ClientboundChunkBatchFinishedPacket`.

The client times the batch in `ChunkBatchSizeCalculator`, clamps the
sample against the running average, folds it into a weighted mean, and
reports back a rate in `ServerboundChunkBatchReceivedPacket`. The server
clamps that and uses it as next tick's budget. It is a closed control
loop whose set point is **seven milliseconds of client time per tick**:
`ChunkBatchSizeCalculator` divides that budget by its running estimate of
nanoseconds per chunk. It starts pessimistic — two milliseconds a chunk,
so the client's opening ask is three and a half chunks a tick against the
server's starting nine.

A chunk packet — `ClientboundLevelChunkWithLightPacket` — carries only
the client-facing heightmaps (the worldgen ones never cross), every
section's paletted block states and biomes, a block-entity entry per
block entity holding `BlockEntity.getUpdateTag` rather than its save
data, and the light layers. See
[chunk anatomy](../world/chunk-anatomy.md) and
[lighting](../world/lighting.md).

## The trace: a creeper walks into view

```mermaid
sequenceDiagram
    participant CM as ChunkMap
    participant TE as ChunkMap.TrackedEntity
    participant SE as ServerEntity
    participant CPL as ClientPacketListener
    participant CL as ClientLevel

    CM->>TE: tick — the creeper changed section, so re-evaluate everyone
    TE->>TE: horizontal distance only, against the smaller of range and view
    TE->>TE: is the creeper's chunk already sent to this player?
    TE->>SE: addPairing — the player is now in seenBy
    SE->>CPL: one ClientboundBundlePacket, applied atomically
    Note over SE,CPL: add entity · entity data · attributes · equipment · passengers
    CPL->>CL: createEntityFromPacket, placed at the tracker's baseline
    SE->>CPL: ClientboundMoveEntityPacket.PosRot — deltas in 1/4096 blocks
    SE->>CPL: ClientboundRotateHeadPacket — always its own packet
    CPL->>CL: moveOrInterpolateTo — smeared over three client ticks
    SE->>CPL: ClientboundSetEntityDataPacket — only the dirty values
    CL->>CL: Creeper.tick runs locally; the swell counter is the client's own
```

Each arrow is a decision.

**Visibility is re-evaluated when something moves.** `ChunkMap.tick`
compares each tracked entity's section against its last, and on a change
re-tests against every player. Players who changed section are re-tested
against every entity. `ChunkMap.move` does the same eagerly when a player
moves.

**The test is horizontal.** `ChunkMap.TrackedEntity.updatePlayer`
compares squared *x/z* distance against the smaller of the entity's
effective range and the player's view distance. **Y is ignored** — an
entity directly above you at any height is in range.

**Range is the maximum over the whole vehicle stack.**
`ChunkMap.TrackedEntity.getEffectiveRange` takes the largest range among
the entity and all its passengers, then scales it by
`MinecraftServer.getScaledTrackingDistance`, which both server classes
override: `DedicatedServer` applies the
*entity-broadcast-range-percentage* property, and `IntegratedServer`
applies the client's own **Entity Distance** video option. In
singleplayer a graphics slider decides how far away mobs are tracked.

**An entity is never sent before its chunk.** The visibility test is
three conjuncts, not two: the horizontal range, `ChunkMap.isChunkTracked`
— false while the chunk is still pending, so the ordering is guaranteed
rather than hoped for — and `Entity.broadcastToPlayer`, the per-entity
veto that a few types use to hide themselves from some viewers.

**The introduction is one bundle.** `ServerEntity.addPairing` collects
what `ServerEntity.sendPairingData` produces and sends it as a single
`ClientboundBundlePacket`, which the client applies inside one task —
so the creeper can never be rendered half-initialised. The order is:
add-entity, then `ClientboundSetEntityDataPacket` with the non-default
synched values ([synched entity data](../entities/synched-entity-data.md)),
then `ClientboundUpdateAttributesPacket` with only the syncable
attributes ([attributes](../entities/attributes.md)), then
`ClientboundSetEquipmentPacket`, then passenger and leash links.

**The add packet describes the tracker's baseline, not the entity — with
two exceptions and one refusal.** Paintings and item frames build their
own `ClientboundAddEntityPacket` from their real position, bypassing
`ServerEntity` entirely, because a block-attached entity has no dead
reckoning to agree about; and `Marker` throws outright if anyone tries,
which nobody does, because its tracking range is zero and `ChunkMap`
never tracks it. For everything else
`ClientboundAddEntityPacket` reads position from
`ServerEntity.getPositionBase` and rotations and motion from the
last-sent fields. Those are stale by at least the update interval and,
for an entity that is loaded but not being ticked and has not changed
section, by no bounded amount at all. Every viewer therefore starts dead
reckoning from an identical base, however old.

**Then only changes, behind two gates that are not the one you would
guess.** `ChunkMap.tick` calls `ServerEntity.sendChanges` at all when
*any* of three things is true: the entity changed section, its
`Entity.needsSync` flag is set, or its chunk is in entity-ticking range.
Inside, the position work runs when *any* of three more is true: the
call count is a multiple of `EntityType.updateInterval`,
`Entity.needsSync` again, or the synched data is dirty. The call counter
advances on every call, gate or no gate, so
`ServerEntity.FORCED_POS_UPDATE_PERIOD` counts calls;
`ServerEntity.teleportDelay` advances only inside the gate and so counts
gated ones. Position goes relative
(`ClientboundMoveEntityPacket` with short deltas of 1/4096 block) unless
something forces an absolute `ClientboundEntityPositionSyncPacket`. Head
yaw is always its own `ClientboundRotateHeadPacket`. Synched data and
attributes go only when dirty.

**The client interpolates the position — if the entity is one of the ten
kinds that can.** `Entity.moveOrInterpolateTo` asks the entity for an
`InterpolationHandler` and gets **null** by default, in which case it
sets the position outright. `LivingEntity` supplies the standard
three-tick handler, and `Display`, `ExperienceOrb`, `Shulker`,
`FishingHook`, boats and minecarts supply their own; an arrow, a
thrown potion, a primed TNT and a dropped item all snap. Where there is a
handler it smears the update over three client ticks — the
client does *not* re-run a tracked entity's physics to fill the gap
(see [movement and collision](../entities/movement-and-collision.md)).
What it does run is the rest of the tick: `ClientLevel.tickEntities`
calls `Creeper.tick` locally, and the swell counter is the client's own:
of the creeper's three synched values — swell direction, powered and
ignited — none is the counter itself. The fuse length is never sent
either, so the client always animates against the default.

## Position sync in detail

| condition | result |
|---|---|
| squared position delta below `ServerEntity.TOLERANCE_LEVEL_POSITION` and rotation within `ServerEntity.TOLERANCE_LEVEL_ROTATION` | nothing sent |
| otherwise, and no forcing condition | `ClientboundMoveEntityPacket.Pos`, `.Rot` or `.PosRot` |
| every `ServerEntity.FORCED_POS_UPDATE_PERIOD` gated calls | a position packet regardless |
| delta beyond what a short can hold (about eight blocks) | absolute sync |
| `ServerEntity.teleportDelay` past `ServerEntity.FORCED_TELEPORT_PERIOD` | absolute sync |
| the entity just dismounted, or its ground flag flipped | absolute sync |
| `Entity.getRequiresPrecisePosition` | absolute sync |
| the entity is a passenger | rotation only; the base is silently re-set and the next free tick forces an absolute sync |

Rotations are single bytes — one unit is a little over a degree. The
dead-reckoning base advances only when something was actually sent,
which is what keeps the two sides' arithmetic identical. An arrow is the
one shape that never takes a partial path: `AbstractArrow` is excluded
from the position-only and rotation-only branches, so every gate-open
sends it a full position-and-rotation packet.

**Velocity is a separate channel.** When the entity wants deltas — it is
in the `EntityType.trackDeltas` set, `Entity.needsSync` is set, or it is
a `LivingEntity` currently elytra-flying — `ServerEntity` compares the
current delta movement against `ServerEntity.lastSentMovement` and sends
`ClientboundSetEntityMotionPacket`, bundled with
`ClientboundProjectilePowerPacket` for a hurtling projectile.
`Entity.hurtMarked` sends the same packet outside every gate, to the
trackers *and* the entity itself, which is why knockback is immediate.

**Minecarts have a parallel protocol.** A cart on the new movement
behaviour is diverted by `ServerEntity.handleMinecartPosRot` into
`ClientboundMoveMinecartPacket`, carrying a list of steps rather than one
position, and never touches the decision table above.

**And one entity broadcasts outside its own audience.** Every ten ticks,
an `ItemFrame` holding a map iterates *every player in the level* — not
its trackers — to tick the map's carried state and push map updates.

## Block updates

`ServerLevel.sendBlockUpdated` does not send anything. It marks a section
dirty on the `ChunkHolder` and adds the holder to a set on
`ServerChunkCache` — unless the chunk is loaded but not ticking, in which
case `ChunkHolder.blockChanged` records nothing and the change is never
broadcast to anyone. Once per tick `ChunkHolder.broadcastChanges` drains
the set:

- **Light first, to a smaller audience.** If either light filter is
  non-empty, one `ClientboundLightUpdatePacket` goes only to players for
  whom this chunk is on the *border* of their sent region
  (`ChunkMap.isChunkOnTrackedBorder`). A player in the middle of their
  own loaded area is never sent light for the chunk they are standing in
  — their own light engine is expected to derive it. See
  [lighting](../world/lighting.md).
- **Then blocks, to everyone tracking the chunk.** Exactly one changed
  block in a section becomes a `ClientboundBlockUpdatePacket`; two or
  more become a `ClientboundSectionBlocksUpdatePacket`. All changes
  within one tick collapse into at most one packet per section.
- **And block entities alongside the blocks, not after them.** The
  block-entity check runs inside the same per-section loop, immediately
  after that section's own update packet — interleaved, not a third
  pass.
  `ChunkHolder.broadcastBlockEntityIfNeeded` calls
  `BlockEntity.getUpdatePacket`, which returns null by default. Only
  overriding types produce a `ClientboundBlockEntityDataPacket`. And the
  fallback is not "it rides the chunk packet instead": the chunk packet
  carries `BlockEntity.getUpdateTag`, which is *also* empty by default,
  and an empty tag is stored as nothing at all. A block entity that
  overrides neither sends the client its position and its type and
  nothing else — which is why chest contents are invisible until the
  chest is opened. See [block entities](../blocks/block-entities.md).

The rest of the block-shaped traffic:
`ClientboundBlockEventPacket` from the deferred event set
([redstone](../blocks/redstone.md)),
`ClientboundBlockDestructionPacket` for other players' mining progress,
`ClientboundBlockChangedAckPacket`, sent at most once per connection per
tick and on any tick where the client sent a block action, a use-on or a
use — **including an unsequenced abort, which produces an ack of zero and
settles nothing** — and `ClientboundChunksBiomesPacket` when biomes are
re-sent. The prediction rules themselves belong to
[prediction and acknowledgement](../client/prediction-and-acks.md).

## The rest of the push

Entities and chunks are the two big feeds; the level itself has several
small ones, all on `ServerLevel` and all bypassing the change detectors
entirely.

- **Time**, once a second: `MinecraftServer.tickChildren` calls
  `MinecraftServer.forceGameTimeSynchronization` every twentieth tick,
  and the packet now carries a game time plus a map of clock updates
  rather than a single day-time number
  ([environment attributes and timelines](../world/environment-attributes-and-timelines.md)).
- **Weather**, on change: `ServerLevel.advanceWeatherCycle` broadcasts
  rain- and thunder-level changes and the start/stop pair as
  `ClientboundGameEventPacket`s, and `PlayerList` re-sends the same set
  to a joining player.
- **Sounds, level events, particles and entity events**, each with its
  own helper and its own audience. Two radii are worth naming because
  they are not the tracking distance: another player's mining progress
  reaches everyone within thirty-two blocks except the miner, and a block
  event reaches sixty-four.
- **View distances**, as `ClientboundSetChunkCacheRadiusPacket` and
  `ClientboundSetSimulationDistancePacket` — the two integers that are
  the client's entire knowledge of the ticket system. Receiving the first
  also rebuilds the client's chunk storage array.
- **The debug feed.** `ServerLevel` owns a set of per-subscriber debug
  synchronizers that push neighbour updates, POI state, chunk sends and
  entity tracking to a client that has opted in. Everything in the next
  section is invisible *except* through that channel.

## What the client is never told

Named concretely, with the server-side owner:

- **All AI.** `Mob.goalSelector`, `Mob.targetSelector`, `Mob.getTarget`,
  the `Brain`, `Mob.navigation` and its `Path`. The client sees the
  creeper's position and its swell direction; it has no idea what the
  creeper is walking toward
  ([AI, goals and brains](../entities/ai-goals-and-brains.md)).
- **Scheduled ticks.** `ServerLevel.blockTicks` and
  `ServerLevel.fluidTicks`. The client's equivalents are empty
  black holes ([block ticks and fluids](../world/block-ticks-and-fluids.md)).
- **Points of interest.** `ChunkMap.poiManager`, except through the
  opt-in debug channel ([game events and POI](../world/game-events-and-poi.md)).
- **The ticket graph.** `TicketStorage`, `DistanceManager`,
  `ChunkHolder.ticketLevel`, `FullChunkStatus`. The client is told only
  a radius and a simulation distance, as two integers.
- **Worldgen.** `ChunkGenerator`, `RandomState`,
  `ServerLevel.structureManager`, every `StructureStart`. **The world
  seed never crosses** — `ClientLevel` gets only a biome zoom seed.
- **The worldgen heightmaps**, and any block-entity field not written
  into `BlockEntity.getUpdateTag` — chest contents, hopper contents,
  spawner internals.
- **Non-syncable attributes**, loot tables and loot seeds, the natural
  spawn state, raids and the dragon fight.
- **Game rules.** They reach the client only on request and only for a
  player with the command permission
  ([level data and rules](../world/level-data-and-rules.md)). An
  ordinary client does not know the game rules.
- **Everything outside the disc**: entities beyond tracking range,
  chunks outside the tracking view, and every other level on the server.

## What the client does on receipt

The client is not a passive applier. `ClientPacketListener.handleMoveEntity`
asks `Entity.isLocalInstanceAuthoritative` first: for an entity the
client owns — its own player — a movement packet updates only the dead
reckoning base and **does not move anything**, because the client's own
simulation is the authority and the server's copy is the stale one. For
everything else it moves or interpolates, except that a jump of more than
sixty-four blocks is snapped rather than smeared, because interpolating
a teleport looks like flight. The authority predicates themselves belong
to [movement and collision](../entities/movement-and-collision.md).

## `ClientLevel` as a lossy copy

The counterpart to everything above is what the receiver does with it, and
that belongs to Part X: the client fakes a great deal
(`ClientLevel.hasChunk` is unconditionally true, `ClientLevel.explode` and
its game-event dispatch are empty), simulates a great deal (its own clock,
its own light engine, full entity ticks on entities it does not own), and
guesses the rest through a sequence-numbered ledger. See
[the client level](../client/the-client-level.md) and
[prediction and acknowledgement](../client/prediction-and-acks.md).

The reason it matters here is the design constraint it puts on this page's
subject: because the client will happily simulate in the absence of data,
**the server's job is not to keep the client correct — it is to choose what
the client is allowed to be wrong about.**

## Interfaces

- **Called by:** `ServerLevel.tick` and `MinecraftServer.tickChildren`.
- **Calls into:** `ServerGamePacketListenerImpl.send`, and thence
  [the connection](the-connection.md).
- **Crosses the network as:** the clientbound half of the play protocol
  — see [reference/packets.md](../../reference/packets.md).
- **Data-driven by:** `EntityType`'s tracking range and update interval;
  the server's view distance, simulation distance and broadcast-range
  percentage.

## Invariants and surprises

- **Light goes to a strictly smaller audience than blocks.** Border
  chunks only. Server light is pushed at the seam, where the client's
  own engine lacks the neighbouring data, and nowhere else.
- **The first chunk batch is a synchronous round trip.** One batch, then
  wait, then up to ten in flight.
- **The chunk-rate loop is measured on the network thread.** The two
  batch handlers are the only chunk-path handlers that do not hop, so
  what is being timed is decode time, not the time to build meshes.
- **The add-entity packet is deliberately stale.** It reports the
  tracker's baseline so every viewer's dead reckoning agrees.
- **An entity in a loaded but un-ticked chunk usually gets no updates —
  but "usually" is doing real work.** The chunk being out of
  entity-ticking range only suppresses the change detector while the
  entity also stays inside its section and leaves `Entity.needsSync`
  clear. Either of those breaks the silence, which is why a distant
  entity can freeze for a long time and then correct itself in one jump.
- **Visibility ignores Y entirely.** The test is a horizontal disc.
- **You never track yourself.** `ChunkMap.TrackedEntity.updatePlayer`
  returns immediately for the player's own entity — which is why the
  self-directed variant of the broadcast verbs exists at all, and why
  damage, knockback and synched data have to use it.
- **`Entity.setRequiresPrecisePosition` has exactly one caller in the
  whole game, and it is a happy ghast.** It is the first term in the
  absolute-versus-relative decision, and the only thing that ever asks
  for it is a ghast on its still timeout — which is a large ridable
  platform, and therefore the one entity whose rounding error a player
  would stand on.
- **Routine movement never uses the teleport packet.**
  `ClientboundTeleportEntityPacket` survives, but `ServerEntity` never
  touches it; absolute position is
  `ClientboundEntityPositionSyncPacket`. The teleport packet is only for
  an explicit transition with riders.
- **Knockback and passengers are checked outside the interval gate.**
  `Entity.hurtMarked` and a changed passenger list are re-sent on every
  call, not every third one — which is why knockback feels immediate on
  an entity whose position otherwise updates slowly.
- **Damage crosses without a number.** `ClientboundDamageEventPacket`
  carries the source, not the amount; the health bar moves because of a
  separate synched value ([damage and death](../entities/damage-and-death.md)).
- **Equipment bypasses the change detector, and skips its wearer.**
  `ClientboundSetEquipmentPacket` comes from
  `LivingEntity.handleEquipmentChanges`, not from
  `ServerEntity.sendChanges`, and it goes to the trackers *without* the
  self-directed variant — a player is never sent their own equipment.
  A straight main-hand/off-hand swap does not even get that far:
  `LivingEntity.handleHandSwap` compresses it into a one-byte entity
  event.

## Where to look

`PlayerChunkSender` · `ChunkTrackingView` · `ChunkMap` ·
`ChunkMap.TrackedEntity` · `ServerEntity` · `VecDeltaCodec` ·
`ChunkHolder` · `ServerChunkCache` · `ClientPacketListener` ·
`ChunkBatchSizeCalculator` · `ClientChunkCache` · `ClientLevel` ·
`BlockStatePredictionHandler` · `InterpolationHandler`

---

*Rules: names, never code · how the system works, not how the code reads ·
newest version only · every backticked name passes `tools/verify_names.py`.*
