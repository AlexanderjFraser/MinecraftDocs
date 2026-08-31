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
missing, it runs full entity logic on entities it does not own, it
computes its own light, and it guesses at block placements and rolls them
back. And the introduction packet for a new entity describes not where
the entity *is* but where the tracker last *said* it was.

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
  enter/leave pair. It is a **disc**, not a square:
  `ChunkTrackingView.isWithinDistance` compares squared horizontal
  distance after shrinking each axis delta by a small buffer.
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

Per-entity tracking parameters are on the type:
`EntityType.clientTrackingRange` (in chunks),
`EntityType.updateInterval` (in ticks) and `EntityType.trackDeltas`.

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
   Both run **before** the entity-tick phase, so a broadcast describes
   the state the *previous* tick left behind.
2. After every level has ticked, `MinecraftServer.tickChildren` runs the
   chunk-sending phase: `PlayerChunkSender.sendNextChunks` once per
   player.
3. Flushing is suspended for the whole tick and resumed at the end of
   that phase, so one tick of traffic to one player is one flush — see
   [the connection](the-connection.md).

On the client, `PacketProcessor.processQueuedPackets` runs **once per
client tick, not per frame**, so a burst of packets is applied in one
lump. Two handlers are exceptions and run on the Netty thread:
`ClientPacketListener.handleChunkBatchStart` and
`ClientPacketListener.handleChunkBatchFinished`.

## Chunk sending

`ChunkMap.applyChunkTrackingView` diffs the player's old and new tracking
discs; entering chunks are queued with
`PlayerChunkSender.markChunkPendingToSend`, leaving chunks are dropped.
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
- takes that many chunks, **nearest first**, from `PlayerChunkSender.pendingChunks` — or
  all of them at once on a memory connection;
- brackets them with `ClientboundChunkBatchStartPacket` and
  `ClientboundChunkBatchFinishedPacket`.

The client times the batch in `ChunkBatchSizeCalculator`, clamps the
sample against the running average, folds it into a weighted mean, and
reports back a rate in `ServerboundChunkBatchReceivedPacket`. The server
clamps that and uses it as next tick's budget. It is a closed control
loop whose set point is a few milliseconds of client time per batch.

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
`MinecraftServer.getScaledTrackingDistance` — identity on an integrated
server, the *entity-broadcast-range-percentage* property on a dedicated
one.

**An entity is never sent before its chunk.** The visibility test
includes `ChunkMap.isChunkTracked`, which is false while the chunk is
still pending, so the ordering is guaranteed rather than hoped for.

**The introduction is one bundle.** `ServerEntity.addPairing` collects
what `ServerEntity.sendPairingData` produces and sends it as a single
`ClientboundBundlePacket`, which the client applies inside one task —
so the creeper can never be rendered half-initialised. The order is:
add-entity, then `ClientboundSetEntityDataPacket` with the non-default
synched values ([synched entity data](../entities/synched-entity-data.md)),
then `ClientboundUpdateAttributesPacket` with only the syncable
attributes ([attributes](../entities/attributes.md)), then
`ClientboundSetEquipmentPacket`, then passenger and leash links.

**The add packet describes the tracker's baseline, not the entity.**
`ClientboundAddEntityPacket` reads position from
`ServerEntity.getPositionBase` and rotations and motion from the
last-sent fields — values that may be up to sixty ticks stale. Every
viewer therefore starts dead-reckoning from an identical base.

**Then only changes.** `ServerEntity.sendChanges` runs on the entity's
`EntityType.updateInterval` — but only if the entity is in a
simulation-range chunk. Position goes relative
(`ClientboundMoveEntityPacket` with short deltas of 1/4096 block) unless
something forces an absolute `ClientboundEntityPositionSyncPacket`. Head
yaw is always its own `ClientboundRotateHeadPacket`. Synched data and
attributes go only when dirty.

**The client interpolates and then simulates.**
`Entity.moveOrInterpolateTo` hands the update to an
`InterpolationHandler`, which smears it over three client ticks. And
`ClientLevel.tickEntities` runs `Creeper.tick` locally: the swell
counter is the client's own, because only its *direction* is synched.
The fuse length is never sent, so the client always animates against the
default.

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
which is what keeps the two sides' arithmetic identical.

## Block updates

`ServerLevel.sendBlockUpdated` does not send anything. It marks a section
dirty on the `ChunkHolder` and adds the holder to a set on
`ServerChunkCache`. Once per tick `ChunkHolder.broadcastChanges` drains
it:

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
- **Then block entities, if they opted in.**
  `ChunkHolder.broadcastBlockEntityIfNeeded` calls
  `BlockEntity.getUpdatePacket`, which returns null by default. Only
  overriding types produce a `ClientboundBlockEntityDataPacket`; every
  other block entity's contents reach the client solely inside the
  initial chunk packet. See [block entities](../blocks/block-entities.md).

The rest of the block-shaped traffic:
`ClientboundBlockEventPacket` from the deferred event set
([redstone](../blocks/redstone.md)),
`ClientboundBlockDestructionPacket` for other players' mining progress,
`ClientboundBlockChangedAckPacket` once per connection per tick to close
out the client's prediction ledger, and `ClientboundChunksBiomesPacket`
when biomes are re-sent. The prediction rules themselves belong to
[block interaction](../blocks/block-interaction.md).

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

## `ClientLevel` as a lossy copy

**What it fakes.** `ClientLevel.hasChunk` returns **true
unconditionally**, and `ClientChunkCache` hands back a shared empty chunk
for anything out of range — so "no data" reads as "air, plains biome",
never as an error. Storage is a fixed torus indexed modulo the view
range; moving the centre silently re-aims the same slots.
`ClientLevel.explode` has an **empty body** — explosions are pure
particles, sound and knockback from `ClientboundExplodePacket`. So does
its game-event dispatch.

**What it simulates.** It advances its own game time every tick and only
corrects on `ClientboundSetTimePacket`. It runs full `Entity.tick` on
entities it does not own. It computes its own light in a queue throttled
per frame. It runs weather and ambient particles off a
time-seeded random. It recomputes biome tint locally.

**What it guesses.** `BlockStatePredictionHandler` stashes the
pre-change state for every block the player places or breaks; incoming
block updates for a predicted position update only the *stored* server
state and leave the visible world alone, until the acknowledgement
packet reconciles the whole range at once — and snaps the player back if
the correction now intersects them.

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
- **An entity in a loaded but unsimulated chunk gets no updates at all.**
  `ServerEntity.sendChanges` is gated on simulation range, so such an
  entity freezes on the client rather than merely stopping.
- **Visibility ignores Y entirely.** The test is a horizontal disc.
- **You never track yourself.** `ChunkMap.TrackedEntity.updatePlayer`
  returns immediately for the player's own entity — which is why the
  self-directed variant of the broadcast verbs exists at all, and why
  damage, knockback and synched data have to use it.
- **`Entity.setRequiresPrecisePosition` has no callers.** It is the first
  term in the absolute-versus-relative decision and nothing in the tree
  sets it.
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
- **Equipment bypasses the change detector.**
  `ClientboundSetEquipmentPacket` is sent from `LivingEntity`'s own
  equipment-diffing, not from `ServerEntity.sendChanges`.

## Where to look

`PlayerChunkSender` · `ChunkTrackingView` · `ChunkMap` ·
`ChunkMap.TrackedEntity` · `ServerEntity` · `VecDeltaCodec` ·
`ChunkHolder` · `ServerChunkCache` · `ClientPacketListener` ·
`ChunkBatchSizeCalculator` · `ClientChunkCache` · `ClientLevel` ·
`BlockStatePredictionHandler` · `InterpolationHandler`

---

*Rules: names, never code · how the system works, not how the code reads ·
newest version only · every backticked name passes `tools/verify_names.py`.*
