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
and not an authority either
([authority](../entities/authority.md#five-predicates-and-the-final-one-the-other-four-hang-off)
is where the five predicates that word stands for are set out): it simulates hard — every block entity ticks
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
| `LevelExtractor` | the main route from the level to the renderer — pushed *and* pulled | Render thread |
| `ClientPacketListener` | the view radius and simulation distance the server announced | Render thread |
| `TransientEntitySectionManager` | entity storage with no persistence, no chunk save, no index to disk | Render thread |
| `Entity` | whether a position update is a snap or an interpolation | Render thread |

## Where the two levels differ

The comparison is the page. Every row but the last is a method both sides
inherit from the shared hierarchy — `Level` itself, or one of the interfaces
above it — and that one side has hollowed out; the last row is a field.

| shared method | on the server | on `ClientLevel` |
|---|---|---|
| `Level.shouldTickBlocksAt` | ticket range | inherited — unconditionally true |
| `ScheduledTickAccess.scheduleTick` | real `LevelTicks` | both lists are `BlackholeTickAccess` |
| `Level.explode` | the real thing | empty override — particles arrive by packet |
| `LevelAccessor.gameEvent` | vibrations, sculk | empty override |
| `LevelReader.getUncachedNoiseBiome` | generates | returns plains |
| `LevelReader.hasChunk` | asks the source | unconditionally true |
| `Level.setBlocksDirty` | empty | the renderer notification |
| `Level.shouldTickDeath` | true | **stricter** — within the server's simulation distance |
| entity storage | persistent: a disk store, known UUIDs, per-chunk load states | transient: the same lookup, none of the bookkeeping |

Three of those deserve their own sentence. `LevelReader.hasChunk` returning
true unconditionally means that particular question is useless on the client —
though `Level.isLoaded` still works, because it goes through the chunk source
instead. `Level.explode` doing nothing is why an explosion you can see is not
a simulation: one `ClientboundExplodePacket` carries the sound, the particle
and the knockback, and the handler plays all of it. And `Level.shouldTickDeath` is the only row where the *client*
is the stricter of the two: it uses the server's announced simulation
distance to decide whether a dying mob plays its death animation.

**Two** — the number of things that read the server's announced simulation
distance off `ClientLevel`. That one, and `LevelExtractor`'s render-stats
string. (The client's own `Options.simulationDistance`, which is a different
number, has its own readers.) The value only
ever arrives from the server, on
`ClientPacketListener.serverSimulationDistance`, beside
`ClientPacketListener.serverChunkRadius`; both are seeded at login, updated
by their own packets, and handed to each new `ClientLevel` at construction.

## What it does simulate: the two cadences

**Per client tick**, from [`Minecraft.tick`](the-client-loop.md#what-a-tick-is-in-order):
`ClientLevel.tickEntities`, then
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
    Note over CL: any ticks this frame owes, which above 20 fps is usually none
    CL->>CL: tickEntities, then Level.tickBlockEntities — the new chunk's block entities tick at once
    Note over CL: still inside the same runTick, in renderFrame
    CL->>CL: update, then pollLightUpdates — the queued lambda finally runs
    CPL->>LLE: applyLightData, then enableChunkLight, whose last act is setSectionRangeDirty over a 3x3 of columns
    CL->>LLE: runLightUpdates (unbounded)
    CCC->>LX: onLightUpdate, then setSectionDirty — straight to the extractor, bypassing the level
```

Three things about the shape. **Blocks and light are separated in the
handler**, so a chunk exists, ticks and can be walked on before it is lit.
**The separation is not a wait**: both notes fall inside the one
`Minecraft.runTick` that handled the packet, and above twenty frames a second
the frame usually owes no tick at all, so the light is applied with nothing
having ticked in between. And **the renderer is reached two ways** —
the level pushes (`ClientLevel.sendBlockUpdated`, `ClientLevel.setBlocksDirty`,
`ClientLevel.setSectionRangeDirty`), but the chunk cache and three of
`ClientPacketListener`'s own handlers reach `LevelExtractor` directly (the
biome resend marks whole sections dirty; login and the game-test highlight
reach through it for the debug renderers), and the extractor also *pulls*:
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
behind you by overwriting it. The array is atomic, the two centre coordinates
are declared *volatile*, and so is the reference to the
`ClientChunkCache.Storage` itself,
because the packet handlers are not the only readers. The section-compile
workers are: a `RenderSectionRegion` resolves biome tint *live* rather than
from its snapshot, so `RenderSectionRegion.getBlockTint` goes through
`ClientLevel.getBlockTint` into the chunk cache from a background thread while
the main thread is moving the origin. The `ThreadLocal` and the read-write
lock inside `BlockTintCache` are the same contract said out loud.

`ClientChunkCache.calculateStorageRange` makes the array a few rings wider
than the view distance, `ClientChunkCache.Storage.inRange` and
`ClientChunkCache.Storage.getIndex` decide where a chunk lands, and
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
— its three-tick window, and the 64-block distance past which
`ClientPacketListener` does not hand it the move at all and snaps instead — belongs to [movement and
collision](../entities/movement-and-collision.md#off-it-goes); what this page
owns is *who has one*. `Entity.isInterpolating` is the question
`ServerboundMoveVehiclePacket` and `PositionMoveRotation` both ask before
deciding whether to publish the interpolation's target or the entity's
current position.

## Questions players ask

**Why do I hear my own footsteps instantly on a laggy server?** Because
`ClientLevel.playSeededSound` is the one method here that plays a sound
*only* when the excluded player is the local one — so your own footsteps are
never on the wire at all, and what lags is what you hear of other people
([who hears it](what-makes-a-sound.md#who-hears-it), which also holds the
handful of sounds this level defers for distance).

**Who decides how hard it is raining?** The server, one hundredth at a
time. Weather on the client is presentation only:
`ClientLevel.tickWeatherEffects` spawns rain particles and picks rain sounds,
while the rain and thunder *levels* are ramped on the server by ±0.01 a tick
and broadcast on every tick they change — about a hundred packets across a
five-second transition. What the client does not do is interpolate *within* a
tick: `Level.setRainLevel` writes the old and new values to the same number,
so the partial tick buys nothing and the level steps twenty times a second
rather than smoothly.

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

`ClientLevel.tickingEntities` is an `EntityTickList`, fed by
`ClientLevel.EntityCallbacks` — the four hooks
`ClientLevel.entityStorage` invokes as a chunk starts and stops ticking. That
storage is a `TransientEntitySectionManager`, which is the comparison table's
last row made concrete: the same section-indexed lookup the server uses, with
the disk store, the UUID index and the per-chunk load states left out, so
nothing in it survives a `ClientLevel` being replaced.
`ClientLevel.tintCaches` holds four `BlockTintCache`s — grass, foliage, dry
foliage, water. `ClientLevel.globallyRenderedBlockEntities` is the set that
draws from anywhere, populated by `ClientLevel.onBlockEntityAdded`.
`ClientLevel.explosionTracker` is a `ClientExplosionTracker`, a per-tick
budget of at most 512 block particles that empties itself every tick rather
than deferring anything. `ClientLevel.blockStatePredictionHandler` is the
ledger [prediction and acknowledgement](prediction-and-acks.md) owns, and
`ClientLevel.levelExtractor` is the push half of the route to the renderer.

The client runs a real light engine — block light always, sky light only
where the dimension has it — and every client-side `Level.setBlock` relights,
under exactly the shared `LightEngine.hasDifferentLightProperties` test the
server uses ([lighting](../world/lighting.md) owns what that test asks; the
consequence here is that a purely cosmetic change to a stair or a slab
relights anyway). Its
collision world, on the other hand,
is one entity wide: `ClientLevel.getPushableEntities` returns at most the
local player.

And `ClientLevel` never notifies `LevelRenderer`. It has no reference to it,
and not one per-block or per-section dirty method is left on `LevelRenderer` —
they are all on `LevelExtractor` now. What `LevelRenderer` keeps is
whole-world invalidation, `LevelRenderer.invalidateCompiledGeometry` and its
neighbours, which the extractor calls.

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
