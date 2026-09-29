# The client level

> Verified against **Minecraft 26.3** · Part X · the same `Level` class the server runs, with its authority removed: what the client really simulates, and what it only pretends to.

Place a repeater on the client and it is *there* — drawn, collidable, part of
the world. Ask the client whether that repeater has a tick scheduled and it
will tell you, confidently, that it does not. `ClientLevel`'s two scheduled-tick lists are the empty list `BlackholeTickAccess` hands out: it accepts a schedule, drops it, reports
*no* when asked whether a tick is pending, and counts zero. Shared block code
that consults the level therefore gets a wrong answer rather than an error,
and anything that reschedules itself looks inert until the server speaks.

That is the shape of the whole class. `ClientLevel` is not a passive receiver
and not an authority either: it simulates hard — every block entity with a client ticker ticks regardless of distance, every local block change that alters how light passes is relit locally, it keeps
its own clock and free-runs between corrections — while inheriting a set of
shared `Level` methods that have been quietly reduced to constants. Reading
`ClientLevel` is largely a matter of noticing which overrides are empty.
(*Authority* is a word with five predicates behind it, and
[authority](../entities/authority.md#five-predicates-and-the-final-one-the-other-four-hang-off)
is where they are set out; this page needs only the root, `Entity.isLocalInstanceAuthoritative`, which decides whose positions arrive from the server at all, and one fact about blocks: the server alone decides a block's state.)

## The cast

| class | what it decides | thread |
|---|---|---|
| `ClientLevel` | what the client simulates, and what it answers when asked | Render thread |
| `ClientChunkCache` | which chunks exist, in a fixed-size array a few chunks wider than the view diameter, indexed modulo its side | Render thread |
| `ClientLevel.ClientLevelData` | the client's own game time, difficulty, horizon height and void darkness | Render thread |
| `LevelLightEngine` | the light the client computes for itself, unbudgeted | Render thread |
| `LevelExtractor` | the main route from the level to the renderer — pushed *and* pulled | Render thread |
| `ClientPacketListener` | the view radius and simulation distance the server announced | Render thread |
| `TransientEntitySectionManager` | entity storage with no persistence, no chunk save, no index to disk | Render thread |
| `Entity` | whether a position update is a snap or an interpolation | Render thread |

## Where the two levels differ

The comparison is the page. Every row but the last is a method both sides
inherit from the shared hierarchy — `Level` itself, or one of the interfaces
above it — and that the two sides answer differently; the last row is not a
method but the storage behind one. Seven of the nine rows are the client hollowing something out, the storage among them. Two run the other way — `Level.setBlocksDirty`, empty on the server and real here, and `Level.shouldTickDeath`.

| shared method | on the server | on `ClientLevel` |
|---|---|---|
| `Level.shouldTickBlocksAt` | ticket range | inherited — unconditionally true |
| `ScheduledTickAccess.scheduleTick` | real `LevelTicks` | both lists are `BlackholeTickAccess.emptyLevelList` |
| `Level.explode` | the real thing | empty override — particles arrive by packet |
| `LevelAccessor.gameEvent` | vibrations, sculk | empty override |
| `LevelReader.getUncachedNoiseBiome` | generates | returns plains |
| `LevelReader.hasChunk` | asks the source | unconditionally true |
| `Level.setBlocksDirty` | empty | real — and it notifies `LevelExtractor`, never `LevelRenderer` |
| `Level.shouldTickDeath` | true | **stricter** — within the server's simulation distance |
| entity storage | persistent: a disk store, known UUIDs, per-chunk load states | transient: the same lookup, none of the bookkeeping |

Three of those deserve their own sentence. `LevelReader.hasChunk` returning
true unconditionally means that particular question is useless on the client —
though `Level.isLoaded` still works, because it goes through the chunk source
instead. `Level.explode` doing nothing is why an explosion you can see is not
a simulation: one `ClientboundExplodePacket` carries the sound, the particle and the knockback, and the handler plays all of it, the sound when the packet's flag asks. And `Level.shouldTickDeath` is the only row where the *client*
is the stricter of the two: it uses the server's announced simulation
distance to decide whether a dying mob plays its death animation.

That last row is also one of only **two** things in the client that read the
server's announced simulation distance: the death-animation test, and
`LevelExtractor`'s render-stats string. (The client's own
`Options.simulationDistance` is a different number with its own readers.) The
level keeps its own copy in `ClientLevel.serverSimulationDistance`, but never
decides it: the value arrives from the server on
`ClientPacketListener.serverSimulationDistance`, beside
`ClientPacketListener.serverChunkRadius` — both seeded at login and updated by
their own packets — and is handed to each new `ClientLevel` at construction
and thereafter through `ClientLevel.setServerSimulationDistance`.

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

So "ticks regardless of distance" is true of *distance* and false of `/tick freeze`: `Level.shouldTickBlocksAt` is unconditionally true
here, but `Level.tickBlockEntities` still checks the tick rate manager, and
the loop skips the whole tick while paused.

**Per frame**, and only per frame: `ClientLevel.update`, which calls
`ClientLevel.pollLightUpdates` and then runs the light engine. It is gated on
the game being loaded, the level existing, and the frame being one that
advances game time — so the blocking loops that draw a frame without ticking
do no lighting either.

The light budget is a slope that ends in a cliff, and it budgets the wrong half of the work on purpose. Below `ClientLevel.LIGHT_UPDATE_QUEUE_SIZE_THRESHOLD`
the frame runs a tenth of `ClientLevel.lightUpdateQueue`, floored at
`ClientLevel.NORMAL_LIGHT_UPDATES_PER_FRAME`; at the threshold or above it
runs the entire queue. Then `LevelLightEngine.runLightUpdates` drains the
engine's own propagation queue **completely, every frame, with no budget at
all**. The budget controls how fast the client accepts the *server's* light,
not how fast it computes its own — so a burst of chunks below a thousand queued updates is spread over frames, a tenth of the queue (at least ten) each frame, and only a queue of a thousand or more is taken in one long frame.

## A chunk arrives

The grounding trace, and the one place the whole class is visible at once. The
shaded band is what the figure is for: everything in it is one turn of `Minecraft.runTick`, so the light that arrives at the foot is not a later frame's work — while the queue ahead of it fits the frame's share.

```mermaid
sequenceDiagram
    participant CPL as ClientPacketListener
    participant CCC as ClientChunkCache
    participant CL as ClientLevel
    participant LLE as LevelLightEngine
    participant LX as LevelExtractor

    rect rgba(0, 0, 0, 0.04)
    Note over CPL,LX: one Minecraft.runTick
    CPL->>CPL: handleLevelChunk<br/>WithLight, on the Render thread
    CPL->>CCC: replaceWithPacketData — blocks now
    CCC->>CL: unload, if the torus slot was taken
    CCC->>CL: onChunkLoaded — tint caches, ticking
    CPL->>CL: queueLightUpdate — light later
    CL->>CL: tickEntities, then tickBlockEntities
    CL->>CL: update, then pollLightUpdates
    CPL->>LLE: the queued lambda — setLightEnabled, updateSectionStatus
    CPL->>CL: then setSectionRangeDirty, a 3x3 of columns
    CL->>LLE: runLightUpdates, unbudgeted
    CCC->>LX: setSectionDirty, from onLightUpdate
    end
```

*One packet, one `Minecraft.runTick`, and the light arriving at the bottom of it while the light queue is short: the band is the whole span, so the gap between the blocks and the light is not a wait. Note that the last arrow leaves the chunk cache, not the level.*

Four things about the shape. **Blocks and light are separated in the
handler**, so a chunk exists, ticks and can be walked on before it is lit.
**The separation is not a wait** while the light queue is short: the whole band is the one `Minecraft.runTick` that handled the packet, and above forty frames a second the frame usually owes no tick at all, so the light is applied with nothing having ticked in between. In a burst below a thousand queued updates the frame takes only its share, and the rest waits for later frames. It is also **one arrival, not two**: the lambda `ClientLevel.queueLightUpdate` files runs both
`ClientPacketListener.applyLightData` and
`ClientPacketListener.enableChunkLight`, which is why the listener's lane
wakes up again at the foot of the figure. And **the renderer is reached two
ways** —
the level pushes (`ClientLevel.sendBlockUpdated`, `ClientLevel.setBlocksDirty`,
`ClientLevel.setSectionRangeDirty`), but the chunk cache and four of `ClientPacketListener`'s own handlers reach `LevelExtractor` directly (the biome resend marks whole sections dirty, a transient block is queued through it, and login and the game-test highlight reach through it for the debug renderers), and the extractor also *pulls*:
`ClientLevel.entitiesForRendering`, `ClientLevel.destructionProgress` and
`ClientLevel.getGloballyRenderedBlockEntities` are read each frame and are
mutated with no notification at all.

Unloading is the same trace backwards: `ClientChunkCache.drop` clears the slot, `ClientLevel.unload` clears the chunk's block entities, switches its light off and stops ticking its entities, and the removal of its light data is queued behind the other light updates.

## The chunk cache is a torus

`ClientChunkCache` is not a map. `ClientChunkCache.Storage` is a flat
`AtomicReferenceArray` whose side is the view diameter plus a margin, indexed by the chunk coordinates *modulo* that side — so moving the origin evicts the ring
behind you by overwriting it. The array is atomic, the two centre coordinates
are declared *volatile*, and so is the reference to the
`ClientChunkCache.Storage` itself,
because the packet handlers are not the only readers. The section-compile
workers are: a `RenderSectionRegion` resolves biome tint *live* rather than
from its snapshot, so `RenderSectionRegion.getBlockTint` goes through
`ClientLevel.getBlockTint` into the chunk cache from a background thread while
the Render thread is moving the origin. The `ThreadLocal` and the read-write
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
entity's position. `Entity.moveOrInterpolateTo` hands it as a target to the
entity's `InterpolationHandler` (`Entity.getInterpolation`), and if the
handler declines, the position, yaw and pitch are assigned directly. The base
`Entity.createInterpolationHandler` returns `InterpolationHandler.NO_OP`, which
declines everything, so the default across the entity tree is to snap; seven classes override it, and six opt in (a minecart only outside the minecart-improvements experiment).

| supplies an `InterpolationHandler` | snaps |
|---|---|
| `LivingEntity` — so nearly every mob and every remote player | `AbstractArrow` and every other projectile but `FishingHook` |
| `Display` | `PrimedTnt` |
| `ExperienceOrb` | `ItemEntity` — a dropped item |
| `FishingHook` | `FallingBlockEntity` |
| `AbstractBoat` and `AbstractMinecart` | `Shulker`, whose override hands back the no-op |
| | everything else that does not override |

That table is the reason a dropped item's movement looks different from a
mob's over the same connection: nothing is smoothing it. The handler itself
— its window (for a living entity, as many steps as its type's update interval: three by default, two for a player, an allay or a mannequin; for the others a fixed three, or a display's teleport duration), and the 64-block distance past which
`ClientPacketListener` does not hand it the move at all and snaps instead — belongs to [movement and
collision](../entities/movement-and-collision.md#and-the-tick-after-what-this-one-costs-on-the-wire); what this page
owns is *who has one*. `Entity.getClientPositionAndRotation` is what `ServerboundMoveVehiclePacket` and `PositionMoveRotation` both ask, and it answers with the interpolation's target when there is one or the entity's current position.

## The clock and the weather run themselves, and neither interpolates

Two of the things in that tick are the client keeping numbers the server also
keeps, and both are worth a sentence because both are the class's character in
miniature: it free-runs, and it is corrected rather than told.

**The clock.** `ClientLevel.tickTime` increments `ClientLevel.ClientLevelData.gameTime` every tick the tick rate manager runs normally and hands the
result to a `ClientClockManager` — owned by `ClientPacketListener`, reached
through `ClientLevel.clockManager`, and the thing anything asking the client what time it is asks. `ClientPacketListener.handleSetTime` is the only correction: it is the only caller of `ClientLevel.setTimeFromServer`, and it also hands the clocks their updates. So the
time in a screenshot is the client's own count since the last correction, not
the server's.

**The weather.** Weather on the client is presentation only:
`ClientLevel.tickWeatherEffects` spawns rain particles and picks rain sounds,
while the rain and thunder *levels* are ramped on the server by ±0.01 a tick
and broadcast on every tick they change — about a hundred packets across a
five-second transition. What the client does not do is interpolate *within* a
tick: `Level.setRainLevel` writes the old and new values to the same number, so
the partial tick buys nothing and the level steps twenty times a second rather
than smoothly.

Two more numbers in that tick are deliberately coarse in the same way. The
breaking-progress sweep over `ClientLevel.destroyingBlocks` and
`ClientLevel.destructionProgress` runs only on every twentieth tick, and drops a crack nobody has updated for twenty seconds, which is what clears one left by someone who disconnected mid-dig (an abandoned dig is cleared at once by the server's -1); the progress itself is applied the moment its packet arrives. And
`ClientLevel.animateTick` samples 667 positions at radius sixteen and another
667 at radius thirty-two every tick regardless of the machine, with
`ClientLevel.doAddParticle` culling by distance afterwards and able to
downgrade the particle setting stochastically on top.

The one thing in the class that is *not* coarse is the sound of your own footsteps, which `LocalPlayer.playSound` plays straight through `ClientLevel.playLocalSound` while the server leaves you out of its broadcast, so what lags is what you hear of other people ([who hears
it](what-makes-a-sound.md#who-hears-it) owns the exclusion rule and the sounds this level defers for distance).

## What else it holds

`ClientLevel.tickingEntities` is an `EntityTickList`, fed by `ClientLevel.EntityCallbacks`, whose ticking pair `ClientLevel.entityStorage` calls as a chunk starts and stops ticking and as an entity arrives in, crosses into or out of, or leaves a ticking one. Three more fields are each the
whole of a mechanism another page owns:
`ClientLevel.globallyRenderedBlockEntities` is the set that draws from
anywhere, `ClientLevel.blockStatePredictionHandler` is the ledger [prediction
and acknowledgement](prediction-and-acks.md) owns, and
`ClientLevel.explosionTracker` is a per-tick budget of at most 512 block
particles that empties itself every tick rather than deferring anything.

### The four tint caches, and the soft biome edge

`ClientLevel.tintCaches` holds four `BlockTintCache`s — grass, foliage, dry
foliage, water — and each is what makes a biome colour boundary look softer
than the biome boundary is. `ClientLevel.calculateBlockTint` box-blurs the
per-block answer over the columns the *biome blend radius* option names and
caches that, over a lookup that is itself on the ragged side of the two biome
borders ([biomes](../worldgen/biomes.md#the-two-borders)). The blur is the
client's, entirely: nothing on the server knows the edge is soft. That is also why a chunk arriving invalidates all four of them at once, in the trace above.

The client runs a real light engine — block light always, sky light only
where the dimension has it — and every client-side `Level.setBlock` that passes
the shared `LightEngine.hasDifferentLightProperties` test the
server uses relights ([lighting](../world/lighting.md) owns what that test asks; the
consequence here is that a purely cosmetic change to a stair or a slab
relights anyway). Its push list, on the other hand, is one entity wide: `ClientLevel.getPushableEntities` returns at most the local player.

And `ClientLevel` never notifies `LevelRenderer`. It has no reference to it,
and not one per-block or per-section dirty method is left on `LevelRenderer` —
they are all on `LevelExtractor` now. What `LevelRenderer` keeps is
whole-world invalidation, `LevelRenderer.invalidateCompiledGeometry` and its
neighbours, which the extractor calls.

> **For a 1.21-era reader.** Gone: *ClientLevel.levelRenderer*, every dirty
> method on *LevelRenderer* (now on `LevelExtractor`), and
> *ClientLevel.getStarBrightness* and *ClientLevel.effects* (both now
> `EnvironmentAttribute` lookups — see [environment attributes and
> timelines](../world/environment-attributes-and-timelines.md)).

## Where to look

`ClientLevel.tick` and `ClientLevel.update` for the two cadences.
`ClientChunkCache.Storage` for the torus, and
`ClientChunkCache.replaceWithPacketData` for what a chunk packet does. `ClientLevel.pollLightUpdates` for the budget arithmetic.
`ClientLevel.tickEntities` for the entity walk and `ClientLevel.EntityCallbacks`
for what joins the ticking set. `Entity.moveOrInterpolateTo` for the
snap-or-smooth fork. Then read the empty overrides — `ClientLevel.explode`,
`ClientLevel.gameEvent`, `ClientLevel.getBlockTicks` — because they are the
page in miniature.

---

*Rules: names, never code · how the system works, not how the code reads ·
newest version only · every backticked name passes `tools/verify_names.py`.*
