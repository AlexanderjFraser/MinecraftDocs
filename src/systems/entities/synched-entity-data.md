# Synched entity data

> Verified against **Minecraft 26.2** · Part VI · A player shears a sheep: one byte flips on the server, and the wool disappears on every screen in tracking range.

You right-click a sheep with shears. Somewhere on the server a single byte
changes — bit four of one entry in a nineteen-slot array the sheep carries —
and before that tick ends, every player watching has been told, by a packet
that spends four bytes after the entity id. That array is `SynchedEntityData`,
the channel the server uses to describe an entity to the clients that see it: the
health bar over another player, a sneaking crouch, an armour stand's pose,
an item frame's item, this sheep's wool. It is a numbered array, and the
numbers are the surprising part. **The slot the wool lives in is decided by
the order the JVM happens to run static initialisers in.** Ids are ordinals
handed out down the class tree by a single shared `ClassTreeIdRegistry` as
each entity class initialises: `Entity` takes 0 to 7, `LivingEntity` 8 to
14, `Mob` 15, `AgeableMob` 16 and 17, and `Sheep`, last to load, gets 18.
Nothing names these numbers, nothing writes them down, and they stop at 254
— because on the wire, 255 means *end of packet*.

## The cast

| class | what it decides | thread |
|---|---|---|
| `SynchedEntityData` | one entity's numbered array, and whether anything in it has changed since the last flush | one container per side, confined to that side's main thread |
| `SynchedEntityData.DataItem` | one slot: its value, the default it was built with, and its own dirty flag | with its container |
| `EntityDataAccessor` | the key — an int id and a serializer, equal to another accessor **on the id alone** | immutable, shared by every instance of the class |
| `ClassTreeIdRegistry` | which id a `SynchedEntityData.defineId` call gets, from the last id already taken by an ancestor class | whichever thread first loads the class |
| `EntityDataSerializers` | the 43 registered serializers and the wire id of each, in registration order | a static block, once |
| `ServerEntity` | whether this entity sends anything this tick, and what | the server main thread |
| `ClientboundSetEntityDataPacket` | the wire form: an entity id, then id/serializer/value triples, then 255 | encoded on the Netty pipeline, built on the server thread |
| `ClientPacketListener` | applying an incoming batch to the client's own container | the client main thread |

## Nineteen slots, and where the numbers come from

`SynchedEntityData.defineId` is called from the static initialiser of an
entity class and asks `ClassTreeIdRegistry.define` for a number.
`ClassTreeIdRegistry` keeps one map from class to *last id issued*, and
`ClassTreeIdRegistry.getLastIdFor` walks up the superclass chain until it
finds an entry — so a subclass continues its parent's numbering rather than
starting over. Java's guarantee that a superclass initialises before its
subclass is the entire ordering mechanism. `ClassTreeIdRegistry.getCount` is
the same walk plus one, and it is what sizes the array.

A `Sheep` — `Entity` → `LivingEntity` → `Mob` → `PathfinderMob` →
`AgeableMob` → `Animal` → `Sheep`, of which `PathfinderMob` and `Animal`
define nothing — therefore has exactly nineteen slots:

| id | field | serializer | default |
|---:|---|---|---|
| 0 | `Entity.DATA_SHARED_FLAGS_ID` | `EntityDataSerializers.BYTE` | 0 |
| 1 | `Entity.DATA_AIR_SUPPLY_ID` | `EntityDataSerializers.INT` | `Entity.getMaxAirSupply` |
| 2 | `Entity.DATA_CUSTOM_NAME` | `EntityDataSerializers.OPTIONAL_COMPONENT` | empty |
| 3 | `Entity.DATA_CUSTOM_NAME_VISIBLE` | `EntityDataSerializers.BOOLEAN` | false |
| 4 | `Entity.DATA_SILENT` | `EntityDataSerializers.BOOLEAN` | false |
| 5 | `Entity.DATA_NO_GRAVITY` | `EntityDataSerializers.BOOLEAN` | false |
| 6 | `Entity.DATA_POSE` | `EntityDataSerializers.POSE` | `Pose.STANDING` |
| 7 | `Entity.DATA_TICKS_FROZEN` | `EntityDataSerializers.INT` | 0 |
| 8 | `LivingEntity.DATA_LIVING_ENTITY_FLAGS` | `EntityDataSerializers.BYTE` | 0 |
| 9 | `LivingEntity.DATA_HEALTH_ID` | `EntityDataSerializers.FLOAT` | 1.0 |
| 10 | `LivingEntity.DATA_EFFECT_PARTICLES` | `EntityDataSerializers.PARTICLES` | empty |
| 11 | `LivingEntity.DATA_EFFECT_AMBIENCE_ID` | `EntityDataSerializers.BOOLEAN` | false |
| 12 | `LivingEntity.DATA_ARROW_COUNT_ID` | `EntityDataSerializers.INT` | 0 |
| 13 | `LivingEntity.DATA_STINGER_COUNT_ID` | `EntityDataSerializers.INT` | 0 |
| 14 | `LivingEntity.SLEEPING_POS_ID` | `EntityDataSerializers.OPTIONAL_BLOCK_POS` | empty |
| 15 | `Mob.DATA_MOB_FLAGS_ID` | `EntityDataSerializers.BYTE` | 0 |
| 16 | `AgeableMob.DATA_BABY_ID` | `EntityDataSerializers.BOOLEAN` | false |
| 17 | `AgeableMob.AGE_LOCKED` | `EntityDataSerializers.BOOLEAN` | false |
| 18 | `Sheep.DATA_WOOL_ID` | `EntityDataSerializers.BYTE` | 0 |

The declaration order and the *definition* order are two different lists.
Ids come from where `SynchedEntityData.defineId` sits in the class body; the
values come from the `Entity` constructor, which defines its own eight and
then calls the abstract `Entity.defineSynchedData` that every subclass
overrides and chains up through. `LivingEntity` defines its seven in a
different order from the one that numbered them, and it does not matter,
because `SynchedEntityData.Builder.define` writes each item at
`EntityDataAccessor.id`. `SynchedEntityData.Builder.build` then refuses to
hand over a container with any slot still null, naming the id it is missing —
which is why `SynchedEntityData.get` can index the array with no bounds check
at all.

Four of the nineteen are bitfields, and they are the dense part of the
channel. Slot 0 is `Entity.FLAG_ONFIRE` 0, `Entity.FLAG_SHIFT_KEY_DOWN` 1,
`Entity.FLAG_SPRINTING` 3, `Entity.FLAG_SWIMMING` 4,
`Entity.FLAG_INVISIBLE` 5, `Entity.FLAG_GLOWING` 6 and
`Entity.FLAG_FALL_FLYING` 7 — bit 2 is unnamed and unused — behind
`Entity.getSharedFlag` and `Entity.setSharedFlag`, whose parameter carries a
purpose-built `Entity.Flags` type-use annotation that every call site inside
`Entity` ignores in favour of a bare integer. Slot 8 carries *using an item*,
*off hand* and *spin attack* (`LivingEntity.LIVING_ENTITY_FLAG_IS_USING`,
`LivingEntity.LIVING_ENTITY_FLAG_OFF_HAND`,
`LivingEntity.LIVING_ENTITY_FLAG_SPIN_ATTACK`), slot 15 no-AI, left-handed
and aggressive behind `Mob.setNoAi`, `Mob.setLeftHanded` and
`Mob.setAggressive`, and slot 18 packs a `DyeColor` id into the low nibble
and *sheared* into bit four — `Sheep.getColor`, `Sheep.setColor`,
`Sheep.isSheared`, `Sheep.setSheared`, and the same storage read out as
`DataComponents.SHEEP_COLOR` by `Sheep.get` and written back through
`Sheep.applyImplicitComponents`.

The numbering belongs to the class, not to the concept. `Avatar` — the class
26.2 inserts between `LivingEntity` and `Player` — owns
`Avatar.DATA_PLAYER_MAIN_HAND` and `Avatar.DATA_PLAYER_MODE_CUSTOMISATION`,
so the skin-part toggles belong to every avatar, while
`Player.DATA_PLAYER_ABSORPTION_ID`, `Player.DATA_SCORE_ID` and the two
shoulder parrots (`Player.DATA_SHOULDER_PARROT_LEFT`,
`Player.DATA_SHOULDER_PARROT_RIGHT`, optional ints rather than NBT) sit one
level further down.

## The serializer is the other half of the key

An `EntityDataAccessor` is an id *and* an `EntityDataSerializer`, and the
serializer is what turns the value into bytes. The interface is deliberately
thin: a `StreamCodec` returned by `EntityDataSerializer.codec` — returned,
not extended — paired with an `EntityDataSerializer.copy` that defends the
container against a caller mutating a value it already handed over.
`EntityDataSerializer.ForValueType` is the immutable case, where copying is
identity, and `EntityDataSerializer.forValueType` builds one from a codec
alone.

`EntityDataSerializers` registers 43 of them into a
`CrudeIncrementalIntIdentityHashBiMap`, from a single static block, so
**registration order is the wire id** — `EntityDataSerializers.BYTE` is 0,
`EntityDataSerializers.POSE` is 20, `EntityDataSerializers.HUMANOID_ARM` is
42 and last. Several of them carry `Holder`s of data-pack registries — the
per-species variants, painting variants, resolvable profiles — which is why
the buffer on both sides is a `RegistryFriendlyByteBuf` rather than a plain
one ([codecs](../foundations/codecs-nbt-json.md)). The full list with wire
ids and value types is [the serializer table](../../reference/entity-data-serializers.md).
`EntityDataSerializers.registerSerializer` is public and is the only thing
that fills the bimap: vanilla calls it 43 times from that one block, and
nothing else in the tree ever calls it again. It is a mod extension point
shipped with no caller outside its own file.

## The trace: a sheep is sheared

```mermaid
sequenceDiagram
    participant MPGM as MultiPlayerGameMode
    participant SGPL as ServerGamePacketListenerImpl
    participant Sheep as Sheep
    participant SED as SynchedEntityData
    participant CM as ChunkMap
    participant SE as ServerEntity
    participant CPL as ClientPacketListener

    MPGM->>MPGM: predicts locally with Player.interactOn, unless spectator
    MPGM->>SGPL: ServerboundInteractPacket(entity id, hand, relative location, secondary)
    Note over SGPL: server tick, before MinecraftServer.tickServer runs
    SGPL->>SGPL: Entity.setShiftKeyDown from the packet flag, then range and border checks
    SGPL->>Sheep: Player.interactOn to Entity.interact to Mob.interact
    Sheep->>Sheep: checkAndHandleImportantInteractions, then Entity.interact, then Sheep.mobInteract
    Sheep->>Sheep: Sheep.shear — sound, then dropFromShearingLootTable, then setSheared
    Sheep->>SED: SynchedEntityData.set(Sheep.DATA_WOOL_ID, bit four set)
    SED->>Sheep: Entity.onSyncedDataUpdated, then DataItem.setDirty and isDirty
    Note over SGPL,SE: same tick, ServerLevel.tick chunkSource phase
    CM->>SE: ChunkMap.tick reaches this sheep, ServerEntity.sendChanges
    SE->>SED: isDirty opens the gate, then SynchedEntityData.packDirty
    SED-->>SE: one DataValue — id 18, serializer 0, one payload byte
    SE->>CPL: ClientboundSetEntityDataPacket, queued now and flushed at the end of the tick
    Note over SED: one container per side — the server's above, the client's below
    CPL->>SED: handleSetEntityData to assignValues, per item then the batch
    Note over CPL: next frame — SheepRenderer.extractRenderState reads Sheep.isSheared
```

**The click.** `MultiPlayerGameMode.interact` sends a
`ServerboundInteractPacket` — a flat record of entity id, hand, an
*entity-relative* hit location and the secondary-action flag, attacks having
left for `ServerboundAttackPacket` — and *also* runs the interaction
locally as a prediction, unless the local game mode is spectator.

**The server checks the geometry, not the outcome.**
`ServerGamePacketListenerImpl.handleInteract` confirms the thread with
`PacketUtils.ensureRunningOnSameThread` and that the client has loaded,
resolves the entity with `ServerLevel.getEntityOrPart`, tests the world
border and `Player.isWithinEntityInteractionRange`, and checks the held item
against the level's feature flags. Before any of the geometry, though, it
writes the packet's secondary-action flag straight into
`Entity.setShiftKeyDown` — which is itself a synched-data write on the
*player*, so every interaction packet is also a potential update on slot 0.

**Dispatch down the hierarchy.** `Player.interactOn` calls `Entity.interact`,
which dispatches virtually to the most derived override, `Mob.interact`.
That runs three things in a fixed order: `Mob.checkAndHandleImportantInteractions`
(name tags, spawn eggs), then the superclass hook `Entity.interact` with its
leashing branch, and only if that passes, `Sheep.mobInteract` — the base
hook runs *between* the two mob hooks, not before them. The shears test is
item identity against `Items.SHEARS`, not a tag and not a component, plus
`Sheep.readyForShearing` from the shared `Shearable` interface, whose other
implementors are `MushroomCow`, `SnowGolem`, `Bogged`, `CopperGolem` and
`SulfurCube`. A sheep that is *not* ready returns `InteractionResult.CONSUME`
rather than falling through, which is why shears on an already-sheared sheep
do nothing visible at all.

**The effect, and one byte.** `Sheep.shear` plays `SoundEvents.SHEEP_SHEAR`,
drops wool through `LivingEntity.dropFromShearingLootTable` with
`BuiltInLootTables.SHEAR_SHEEP` — the tool is passed in, so the loot table
can see it — and calls `Sheep.setSheared`, which ors bit four into slot 18.
`SynchedEntityData.set` compares the new value against the current one,
stores it, calls `Entity.onSyncedDataUpdated` for that accessor, and *then*
marks the item and the container dirty. `Sheep` does not override the hook,
and the base implementation reacts to exactly one accessor, `Entity.DATA_POSE`,
by calling `Entity.refreshDimensions`. Back in `Sheep.mobInteract`:
`Entity.gameEvent` with `GameEvent.SHEAR` for the sculk listeners
([game events](../world/game-events-and-vibrations.md)),
`ItemStack.hurtAndBreak` on the shears, and `InteractionResult.SUCCESS_SERVER`.

**The send, in the same tick.** `MinecraftServer.processPacketsAndTick`
drains the queue with `PacketProcessor.processQueuedPackets` and only then
calls `MinecraftServer.tickServer`, so the shear happened before the tick
proper began. `ServerLevel.tick` reaches its *chunkSource* phase after
block and fluid ticks and before block events and entity ticking, and that
phase runs `ChunkMap.tick`, whose loop over `ChunkMap.TrackedEntity` is the
only caller of `ServerEntity.sendChanges` in the tree. The dirty flag opens
the gate, `ServerEntity.sendDirtyEntityData` calls `SynchedEntityData.packDirty`,
and one `ClientboundSetEntityDataPacket` goes to every tracking player and
to the entity itself. After the entity id, the wire carries an unsigned byte
18, a var-int 0 for `EntityDataSerializers.BYTE`, one payload byte and then
the terminator 255 — and that terminator is the whole reason ids stop at
254. Both the pack and the unpack side write and test the literal,
incidentally, so the public `ClientboundSetEntityDataPacket.EOF_MARKER` is
referenced by nothing, exactly like the private
`SynchedEntityData.MAX_ID_VALUE` beside it.

The packet is not on the wire yet. `MinecraftServer.tickChildren` calls
`ServerCommonPacketListenerImpl.suspendFlushing` on every player before it
ticks any level and `ServerCommonPacketListenerImpl.resumeFlushing` at the
end of the tick, so a whole tick's packets leave together.

**The apply, and the frame.** `ClientPacketListener.handleSetEntityData`
looks the entity up in `ClientLevel` and silently drops the entire packet if
the id is unknown, then calls `SynchedEntityData.assignValues`, which checks
that the incoming serializer is the one the accessor was defined with — a
mismatch throws, loudly, on the client — stores each value, fires
`Entity.onSyncedDataUpdated` per item and then the batch overload once.
Nothing tells the renderer. Next frame `LevelExtractor` walks the visible
entities, `EntityRenderDispatcher.extractEntity` builds a `SheepRenderState`,
and `SheepRenderer.extractRenderState` copies `Sheep.isSheared` and
`Sheep.getColor` into it, after which `SheepWoolLayer` draws nothing. The
wool vanishing is a *layer skipped*, not a model swap — and only one layer,
because `SheepWoolUndercoatLayer` tests colour, baby and invisibility but
never the sheared flag, so a sheared coloured sheep still draws its undercoat.

## The gate that holds a packet back

```mermaid
flowchart TD
    IN["ChunkMap.tick: section changed, or Entity.needsSync, or the chunk is in entity-ticking range"] --> SC["ServerEntity.sendChanges, opening with Entity.updateDataBeforeSync"]
    SC -->|"an ItemFrame, every tenth tick — the only bypass"| SEND
    SC --> GATE{"tickCount is a multiple of EntityType.updateInterval, or Entity.needsSync, or SynchedEntityData.isDirty"}
    GATE -->|"yes"| SEND["position, rotation and motion, then ServerEntity.sendDirtyEntityData"]
    GATE -->|"no"| HOLD["nothing goes out, and the dirty flags survive to the next tick"]
```

Two tests stand between a dirty byte and the wire. `ChunkMap.tick` decides
whether `ServerEntity.sendChanges` is called at all; an entity that is
tracked but outside entity-ticking range, and not moving between sections,
simply is not asked, and keeps its dirty data until one of the three
conditions becomes true. Inside `ServerEntity.sendChanges`, the interval gate
covers the position block *and* the usual
`ServerEntity.sendDirtyEntityData` call, which is why shearing a sheep also
sends that sheep's position delta this tick: synched data is, incidentally,
a latency channel for movement.

The interval comes from `EntityType.updateInterval`, fixed when
`ChunkMap.TrackedEntity` constructs the `ServerEntity`. `EntityTypes.PLAYER`
sets 2 and `EntityType.Builder` defaults to 3, but seven types — item frames,
paintings, leash knots and their kin — set something else entirely.

**Integer.MAX_VALUE** — the update interval of `EntityTypes.ITEM_FRAME`,
which is to say its interval branch never fires again after tick zero.

That is exactly why `ServerEntity.sendChanges` has an `ItemFrame` special
case that calls `ServerEntity.sendDirtyEntityData` every tenth tick *before*
the gate: it is the only bypass in the method, and without it a map in a
frame would update only when something else set `Entity.needsSync`.
`ServerEntity.handleMinecartPosRot` calls it too, but from inside the gate,
not around it. `Entity.syncPosition` is the other lever: it
realigns the tracker's own counter so the very next evaluation lands on a
multiple of the interval, which works even when that interval is
*Integer.MAX_VALUE*.

`Entity.updateDataBeforeSync` opens `ServerEntity.sendChanges`, ahead of the
gate, and it is the hook `LivingEntity` overrides to reconcile its effects:
`LivingEntity.updateInvisibilityStatus` and the glowing status write slot 0,
and the swirl list goes into slot 10. A mob effect that expired this tick can
therefore dirty the container and open its own gate, in the same call that
goes on to read the flag.

## Five more channels, all keyed by the same entity id

Synched data is one of six clientbound descriptions of an entity, and
knowing which one a fact travels on answers most *why does the client not
know that* questions. There is no serverbound counterpart to any of them:
the client cannot write to this channel at all.

| channel | packets | note |
|---|---|---|
| synched data | `ClientboundSetEntityDataPacket` | to trackers **and self** — `ServerEntity.Synchronizer.sendToTrackingPlayersAndSelf` |
| attributes | `ClientboundUpdateAttributesPacket` | flushed by the same `ServerEntity.sendDirtyEntityData` ([attributes](attributes.md)) |
| equipment | `ClientboundSetEquipmentPacket` | incremental updates bypass `ServerEntity` entirely — `LivingEntity.handleEquipmentChanges` sends them, to trackers only, not the wearer |
| mob effects | `ClientboundUpdateMobEffectPacket`, `ClientboundRemoveMobEffectPacket` | the authoritative list, unlike the swirl in `LivingEntity.DATA_EFFECT_PARTICLES` |
| position and motion | `ClientboundMoveEntityPacket`, `ClientboundEntityPositionSyncPacket`, `ClientboundTeleportEntityPacket`, `ClientboundRotateHeadPacket`, `ClientboundSetEntityMotionPacket` | the block the synched-data gate shares |
| one-shot events | `ClientboundEntityEventPacket` | a single byte from `ServerLevel.broadcastEntityEvent`, dispatched by `Entity.handleEntityEvent` — `EntityEvent` declares 62 of them |

Pairing a new viewer runs the same machinery once. `ServerEntity.addPairing`
calls `ServerEntity.sendPairingData`, which bundles `ClientboundAddEntityPacket`
with a `ClientboundSetEntityDataPacket`, attributes, equipment, passengers and
a leash link into one `ClientboundBundlePacket`. The data packet is built not
from a fresh pack but from `ServerEntity.trackedDataValues`, a snapshot taken
in the `ServerEntity` constructor from `SynchedEntityData.getNonDefaultValues`
and refreshed only when `SynchedEntityData.packDirty` later returns something. Two consequences:
an entity still entirely at its defaults sends **no** data packet on pairing
at all, and any change made while the tracker sat outside its send gate is
already folded into that cache.

## Questions players ask

**Why is a freshly loaded entity described by so little?** Because defaults
never travel. `SynchedEntityData.getNonDefaultValues` skips any item still
equal to its `SynchedEntityData.DataItem.initialValue`, so pairing describes
only what has changed. Both sides construct their own defaults independently;
if they ever disagreed, no packet would correct it.

**If a value changes twice in a tick, do I get two packets?** No — and not
always for the reason you would guess. `SynchedEntityData.packDirty` clears
each flag as it packs, so one flush carries one value per slot. But the
comparison in `SynchedEntityData.set` is against the *current* value, not
the last one sent: setting A then B then A within a tick dirties the item
twice and then sends A, a value the client already had. The only thing that
never dirties is setting a slot to what it already holds — and even that can
be overridden, because `SynchedEntityData.set` has a three-argument
force-dirty form that skips the comparison entirely. `CopperGolem` uses it to
re-trigger a weathering animation and `Display` to restart an interpolation.

**Why does my client-side change never reach the server?** Nothing stops
`SynchedEntityData.set` on the client — `LocalPlayer` prediction does it
constantly — but `ServerEntity.sendDirtyEntityData` is the only caller of
`SynchedEntityData.packDirty` in the whole tree. The client's dirty flag is read by no one, and
the next server value overwrites the slot ([authority](authority.md)). The
container is not useless to the client, though: `ClientPacketListener.handleRespawn`
copies the old player's non-default values straight into the new one, the
single client-to-client use of the channel.

**Can two mods both add a field to `LivingEntity`?** Only by accident. Ids
are ordinals, so inserting, removing or reordering a `SynchedEntityData.defineId` on a base
class shifts every id below it in every subclass. Two mods claiming the same
number either collide in `SynchedEntityData.Builder.define`, which rejects a
duplicate, or land a value in the wrong slot and throw the serializer check
on the client. `SynchedEntityData.Builder.define` also has an off-by-one in
its bounds test — an id exactly equal to the array length slips past and dies
on the array write instead.

**Does any of this affect the physics the client simulates?** One value does.
`Entity.DATA_POSE` travels on its own `EntityDataSerializers.POSE`, and
`Entity.onSyncedDataUpdated` turns an incoming pose into
`Entity.refreshDimensions` — a synched value resizing a hitbox on both sides.
Everything else on the channel is cosmetic to the client, or read back by
gameplay code that already knew.

Two details that are only visible from the whole tree. The batch overload
`SyncedDataHolder.onSyncedDataUpdated`, fired by
`SynchedEntityData.assignValues` after every packet, is overridden by nothing
in 7,055 classes — it is the only place a client could see a whole update
atomically, and it is dead. And `Display` is the one class that treats
accessor ids as *values*: `Display.RENDER_STATE_IDS` is an int set of the
eight ids that force a render-state rebuild, tested against each incoming
accessor, with `Display.TextDisplay` keeping a second set of its own. It is
the sharpest demonstration in the codebase that these numbers really are
ordinals.

## Where to look

`SynchedEntityData` · `SynchedEntityData.Builder` ·
`SynchedEntityData.DataItem` · `SynchedEntityData.DataValue` ·
`EntityDataAccessor` · `EntityDataSerializer` · `EntityDataSerializers` ·
`ClassTreeIdRegistry` · `Entity.defineSynchedData` ·
`Entity.onSyncedDataUpdated` · `Entity.updateDataBeforeSync` ·
`ServerEntity.sendChanges` · `ServerEntity.sendDirtyEntityData` ·
`ServerEntity.sendPairingData` · `ChunkMap.tick` · `ChunkMap.TrackedEntity` ·
`ClientboundSetEntityDataPacket` · `ClientPacketListener.handleSetEntityData` ·
`Sheep.mobInteract` · `Shearable`

---

*Rules: names, never code · how the system works, not how the code reads ·
newest version only · every backticked name passes `tools/verify_names.py`.*
