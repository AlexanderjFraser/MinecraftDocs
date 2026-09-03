# The client level

> Verified against **Minecraft 26.2** · Part X · the same `Level` class the server runs, with its authority removed: what the client really simulates, and what it only pretends to.

Place a repeater on the client and it is *there* — drawn, collidable, part of
the world. Ask the client whether that repeater has a tick scheduled and it
will tell you, confidently, that it does not. `ClientLevel`'s two scheduled-tick
lists are a `BlackholeTickAccess`: it accepts a schedule, drops it, reports
*no* when asked whether a tick is pending, and counts zero. Shared block code
that consults the level therefore gets a wrong answer rather than an error,
and anything that reschedules itself looks inert until the server speaks.

That is the shape of the whole class. `ClientLevel` is not a passive receiver
and not an authority either: it simulates hard — every block entity ticks
regardless of distance, every local block change is relit locally, it keeps
its own clock and free-runs between corrections — while inheriting a set of
shared `Level` methods that have been quietly reduced to constants. Reading
`ClientLevel` is largely a matter of noticing which overrides are empty.

## The cast

| class | what it decides | thread |
|---|---|---|
| `ClientLevel` | what the client simulates, and what it answers when asked | Render thread |
| `ClientChunkCache` | which chunks exist, in a fixed-size array indexed modulo the view diameter | Render thread |
| `ClientLevel.ClientLevelData` | the client's own game time, difficulty, horizon height and void darkness | Render thread |
| `LevelLightEngine` | the light the client computes for itself, unbudgeted | Render thread |
| `LevelExtractor` | the only route from the level to the renderer — pushed *and* pulled | Render thread |
| `ClientPacketListener` | the view radius and simulation distance the server announced | Render thread |
| `TransientEntitySectionManager` | entity storage with no persistence, no chunk save, no index to disk | Render thread |
| `Entity` | whether a position update is a snap or an interpolation | Render thread |

## Where the two levels differ

The comparison is the page. Every row is a shared `Level` or `LevelReader`
method that both sides inherit and one side has hollowed out.

| shared method | on the server | on `ClientLevel` |
|---|---|---|
| `Level.shouldTickBlocksAt` | ticket range | inherited — unconditionally true |
| `ScheduledTickAccess.scheduleTick` | real `LevelTicks` | both lists are `BlackholeTickAccess` |
| `Level.explode` | the real thing | empty override — particles arrive by packet |
| `Level.gameEvent` | vibrations, sculk | empty override |
| `LevelReader.getUncachedNoiseBiome` | generates | returns plains |
| `Level.hasChunk` | asks the source | unconditionally true |
| `Level.setBlocksDirty` | empty | the renderer notification |
| `Level.shouldTickDeath` | true | **stricter** — within the server's simulation distance |
| entity storage | persistent, UUID-indexed | transient, no disk |

Three of those deserve their own sentence. `Level.hasChunk` returning true
unconditionally means shared code cannot use the client to ask whether a
column is loaded. `Level.explode` doing nothing is why an explosion you can
see is a set of particles and sounds that arrived separately, not a
simulation. And `Level.shouldTickDeath` is the only row where the *client*
is the stricter of the two: it uses the server's announced simulation
distance to decide whether a dying mob plays its death animation.

**Two** — the number of things on the client that read simulation distance
at all. That one, and `LevelExtractor`'s render-stats string. The value only
ever arrives from the server, on
`ClientPacketListener.serverSimulationDistance`, beside
`ClientPacketListener.serverChunkRadius`; both are seeded at login, updated
by their own packets, and handed to each new `ClientLevel` at construction.

## What it does simulate: the two cadences

**Per client tick**, from `Minecraft.tick`: `ClientLevel.tickEntities`, then
`Level.tickBlockEntities`, then `ClientLevel.tick` — which does
`Level.updateSkyBrightness` unconditionally and then, **only if the tick rate
manager is running normally**, the world border, the clock, the weather
*effects* and the breaking-progress sweep. After that, unconditionally again:
the sky flash countdown, the End flash state, and the explosion tracker.
`ClientLevel.animateTick` and `ParticleEngine.tick` follow, both gated on the
game not being frozen.

So "every block entity ticks, at any distance" is true of *distance* and
false of `/tick freeze`: `Level.shouldTickBlocksAt` is unconditionally true
here, but `Level.tickBlockEntities` still checks the tick rate manager, and
the loop skips the whole tick while paused.

**Per frame**, and only per frame: `ClientLevel.update`, which calls
`ClientLevel.pollLightUpdates` and then runs the light engine. It is gated on
the game being loaded, the level existing, and the frame being one that
advances game time — so the blocking loops that draw a frame without ticking
do no lighting either.

The light budget is a cliff rather than a slope, and it budgets the wrong
half of the work on purpose. Below `ClientLevel.LIGHT_UPDATE_QUEUE_SIZE_THRESHOLD`
the frame runs a tenth of `ClientLevel.lightUpdateQueue`, floored at
`ClientLevel.NORMAL_LIGHT_UPDATES_PER_FRAME`; at the threshold or above it
runs the entire queue. Then `LevelLightEngine.runLightUpdates` drains the
engine's own propagation queue **completely, every frame, with no budget at
all**. The budget controls how fast the client accepts the *server's* light,
not how fast it computes its own — and a chunk-load burst therefore produces
one long frame rather than a hundred slightly late ones.

## A chunk arrives

The grounding trace, and the one place the whole class is visible at once.

```mermaid
sequenceDiagram
    participant CPL as ClientPacketListener
    participant CCC as ClientChunkCache
    participant CL as ClientLevel
    participant LLE as LevelLightEngine
    participant LX as LevelExtractor

    CPL->>CPL: handleLevelChunkWithLight — already hopped to the client thread
    CPL->>CCC: replaceWithPacketData — blocks now
    CCC->>CCC: inRange? out-of-range chunks are logged and thrown away
    CCC->>CL: unload(old) if the torus slot was occupied
    CCC->>CL: onChunkLoaded — four tint caches invalidated, entityStorage.startTicking
    CPL->>CL: queueLightUpdate(lambda) — light later
    Note over CL: next tick
    CL->>CL: tickEntities, then Level.tickBlockEntities — the new chunk's block entities tick at once
    Note over CL: next frame
    CL->>CL: update, then pollLightUpdates — the queued lambda finally runs
    CL->>LLE: applyLightData, enableChunkLight, then runLightUpdates (unbounded)
    CL->>LX: setSectionRangeDirty over the column
    CCC->>LX: onLightUpdate, then setSectionDirty — straight to the extractor, bypassing the level
```

Three things about the shape. **Blocks and light are separated in the
handler**, so a chunk exists, ticks and can be walked on before it is lit.
**The two cadences are visible as two notes**: the chunk's block entities
tick before its light is applied. And **the renderer is reached two ways** —
the level pushes (`ClientLevel.sendBlockUpdated`, `ClientLevel.setBlocksDirty`,
`ClientLevel.setSectionRangeDirty`), but the chunk cache and one packet
handler call `LevelExtractor` directly, and the extractor also *pulls*:
`ClientLevel.entitiesForRendering`, `ClientLevel.destructionProgress` and
`ClientLevel.getGloballyRenderedBlockEntities` are read each frame and are
mutated with no notification at all.

Unloading is the same trace backwards: `ClientChunkCache.drop` clears the
slot, `ClientLevel.unload` clears the chunk's block entities and stops
ticking its entities, and a light removal is queued for a later frame.

## The chunk cache is a torus

`ClientChunkCache` is not a map. `ClientChunkCache.Storage` is a flat
`AtomicReferenceArray` whose side is the view diameter, indexed by the chunk
coordinates *modulo* that diameter — so moving the origin evicts the ring
behind you by overwriting it. The array is atomic and the two centre
coordinates are declared *volatile* for one reason: the render thread reads them while
the packet handlers write them, and this is one of the few places on the
client where two threads look at the same field.

`ClientChunkCache.calculateStorageRange` makes the array a few rings wider
than the view distance, `ClientChunkCache.inRange` and
`ClientChunkCache.getIndex` decide where a chunk lands, and
`ClientChunkCache.updateViewCenter` moves the origin by assigning two
integers. Its verbs are `ClientChunkCache.replaceWithPacketData`,
`ClientChunkCache.drop`, `ClientChunkCache.replaceBiomes`,
`ClientChunkCache.updateViewRadius` and `ClientChunkCache.onLightUpdate`,
and it keeps four delta sets — `ClientChunkCache.addedEmptySections`,
`ClientChunkCache.removedEmptySections`, `ClientChunkCache.addedLoadedChunks`
and `ClientChunkCache.removedLoadedChunks` — double-buffered by
`ClientChunkCache.flipUpdateTrackingSets` so the renderer can ask what
changed since last frame.

## Who interpolates, and who snaps

An entity position arriving from the server does not simply become the
entity's position. `Entity.moveOrInterpolateTo` asks
`Entity.getInterpolation` for an `InterpolationHandler`; if there is one the
new position is handed to it as a target, and if there is not the position,
yaw and pitch are assigned directly. The base implementation returns
**null**, so the default across the entity tree is to snap, and interpolation
is opted into by exactly seven overrides.

| supplies an `InterpolationHandler` | snaps |
|---|---|
| `LivingEntity` — so every mob and every remote player | `AbstractArrow` and the other projectiles |
| `Display` | `PrimedTnt` |
| `ExperienceOrb` | `ItemEntity` — a dropped item |
| `Shulker` | `FallingBlockEntity` |
| `FishingHook` | everything else that does not override |
| `AbstractBoat` and `AbstractMinecart` | |

That table is the reason a dropped item's movement looks different from a
mob's over the same connection: nothing is smoothing it. The handler itself
— its three-tick window and the 64-block distance past which it gives up and
snaps anyway — belongs to [movement and
collision](../entities/movement-and-collision.md); what this page owns is
*who has one*. `Entity.isInterpolating` is the question
`ServerboundMoveVehiclePacket` and `PositionMoveRotation` both ask before
deciding whether to publish the interpolation's target or the entity's
current position.

## Questions players ask

**Why does thunder arrive late?** `ClientLevel.playSeededSound` defers a
distant sound by a number of ticks derived from its distance. Nobody sends a
timestamp; the client invents the delay. It is the only place in the game
where propagation delay is modelled — see [the sound
engine](sound-engine.md).

**Why do I hear my own footsteps instantly on a laggy server?**
`ClientLevel.playSeededSound` plays a sound locally when the *excluded*
player is the local one. The server tells everyone else and the client
produces its own copy. What lags is what you hear of other people.

**Why does rain stop and start so abruptly?** Weather on the client is
presentation only. `ClientLevel.tickWeatherEffects` spawns rain particles and
picks rain sounds, but the rain and thunder *levels* are set wholesale by
game-event packets, with no interpolation on either side.

**Why does the clock in a screenshot disagree with the server's?** The
client keeps its own. `ClientLevel.tickTime` increments
`ClientLevel.ClientLevelData.gameTime` unconditionally every tick and hands
the result to a `ClientClockManager` owned by `ClientPacketListener` and
reached through `ClientLevel.clockManager`.
`ClientLevel.setTimeFromServer` is the only correction, and its only caller
is `ClientPacketListener.handleSetTime`.

**Why does the crack overlay on someone else's block lag?** The
breaking-progress sweep over `ClientLevel.destroyingBlocks` and
`ClientLevel.destructionProgress` only runs on every twentieth tick. It is
approximate by construction.

**Why does the ambient particle load not scale with my machine?**
`ClientLevel.animateTick` samples 667 positions at radius sixteen and another
667 at radius thirty-two, every tick, regardless. `ClientLevel.doAddParticle`
culls by distance afterwards and can stochastically downgrade the particle
setting further.

## What else it holds, and what it will not tell you

`ClientLevel.tickingEntities` is an `EntityTickList` over
`ClientLevel.entityStorage`, a `TransientEntitySectionManager`.
`ClientLevel.tintCaches` holds four `BlockTintCache`s — grass, foliage, dry
foliage, water. `ClientLevel.globallyRenderedBlockEntities` is the set that
draws from anywhere, populated by `ClientLevel.onBlockEntityAdded`.
`ClientLevel.explosionTracker` is a `ClientExplosionTracker`, a queue of
delayed block particles. `ClientLevel.blockStatePredictionHandler` is the
ledger [prediction and acknowledgement](prediction-and-acks.md) owns, and
`ClientLevel.levelExtractor` is the push half of the route to the renderer.

The client runs a real light engine — block light always, sky light only
where the dimension has it — and every client-side `Level.setBlock` relights,
but only when the new state actually differs in emission or opacity; a
cosmetic state change queues nothing. Its collision world, on the other hand,
is one entity wide: `ClientLevel.getPushableEntities` returns at most the
local player.

And `ClientLevel` never notifies `LevelRenderer`. It has no reference to it,
and `LevelRenderer` has no invalidation API left at all.

> **For a 1.21-era reader.** Gone: *ClientLevel.levelRenderer*, every dirty
> method on *LevelRenderer* (now on `LevelExtractor`),
> *ClientLevel.getStarBrightness* and *ClientLevel.effects* (both now
> `EnvironmentAttribute` lookups — see [environment attributes and
> timelines](../world/environment-attributes-and-timelines.md)), and
> *ClientChunkCache.ChunkArray*.

## Where to look

`ClientLevel.tick` and `ClientLevel.update` for the two cadences.
`ClientChunkCache.Storage` for the torus, and
`ClientChunkCache.replaceWithPacketData` for what a chunk packet actually
does. `ClientLevel.pollLightUpdates` for the budget arithmetic.
`ClientLevel.tickEntities` for the entity walk and `ClientLevel.EntityCallbacks`
for what joins the ticking set. `Entity.moveOrInterpolateTo` for the
snap-or-smooth fork. Then read the empty overrides — `ClientLevel.explode`,
`ClientLevel.gameEvent`, `ClientLevel.getBlockTicks` — because they are the
page in miniature.

---

*Rules: names, never code · how the system works, not how the code reads ·
newest version only · every backticked name passes `tools/verify_names.py`.*
