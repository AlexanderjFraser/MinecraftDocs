# Player anatomy

> Verified against **Minecraft 26.2** · Part VIII · One server tick of one player, which happens twice: once from the level's entity loop and once from the connection.

## Responsibility

A player is an entity that a human is steering through a socket. Almost
everything else follows from that sentence. The class ladder exists to
separate *what any living thing does* from *what a thing with an inventory
and a game mode does* from *what a thing with a connection does*, and the
tick is split in two because half of a player's update depends on packets
having arrived and half does not.

The one sentence a player recognises: *me.*

The headline for a 1.21-era reader: **there is a new abstract class between
`LivingEntity` and `Player`, and `Inventory` is no longer three lists.**
`Avatar` is a rendering seam that lets a non-player entity wear a skin, and
`Inventory` is now thirty-six slots plus a window onto the same
`EntityEquipment` a zombie has.

## The data it owns

### The ladder

```
Entity
 └ LivingEntity
    └ Avatar
       ├ Player
       │  ├ ServerPlayer
       │  └ AbstractClientPlayer
       │     ├ LocalPlayer
       │     └ RemotePlayer
       └ Mannequin
```

`Entity` and `LivingEntity` belong to
[Part VI](../entities/entity-anatomy.md). The four layers below them:

- **`Avatar`** (`world/entity`) — fifty-seven lines and **no instance
  fields at all**. It owns the player-shaped dimensions (`Avatar.POSES`,
  `Avatar.STANDING_DIMENSIONS`, `Avatar.CROUCH_BB_HEIGHT`,
  `Avatar.SWIMMING_BB_WIDTH`, `Avatar.SWIMMING_BB_HEIGHT`), the 1.62 eye
  height (`Avatar.DEFAULT_EYE_HEIGHT`), the two cosmetic synched values
  (`Avatar.DATA_PLAYER_MAIN_HAND`, `Avatar.DATA_PLAYER_MODE_CUSTOMISATION`)
  with `Avatar.getMainArm` / `Avatar.isModelPartShown`, and one abstract
  method, `Avatar.getProfile`, returning a `ResolvableProfile`. That is the
  whole class.
- **`Mannequin`** (`world/entity/decoration`) — the other subclass, a
  posable skinned dummy that is a sibling of `ArmorStand`, not of `Player`.
  It has a profile (`Mannequin.DATA_PROFILE`), an immovable flag
  (`Mannequin.DATA_IMMOVABLE`), a description
  (`Mannequin.DATA_DESCRIPTION`) and a fixed set of legal poses
  (`Mannequin.VALID_POSES`).
- **`Player`** (`world/entity/player`) — abstract, and where everything
  a reader means by "the player" actually lives.
- **`ServerPlayer`** (`server/level`) and **`AbstractClientPlayer`** /
  **`LocalPlayer`** / **`RemotePlayer`** (`client/player`) — the two
  sides, below.

`Avatar` exists for the renderer. `AvatarRenderer` is generic over
"an `Avatar` that is also a `ClientAvatarEntity`", which is exactly
`AbstractClientPlayer` and `Mannequin`; that is how a decoration entity
gets the full `PlayerModel` and skin pipeline. There is **no
*PlayerRenderer*** any more.

### `Player`

- **`Player.inventory`** and **`Player.enderChestInventory`**
  (a `PlayerEnderChestContainer`).
- **`Player.inventoryMenu`** (the `InventoryMenu`, final) and
  **`Player.containerMenu`** (whatever is open; it *is*
  `Player.inventoryMenu` when nothing is). [Containers and menus](../items/containers-and-menus.md)
  owns what happens inside them.
- **`Player.abilities`** — an `Abilities`, below.
- **`Player.foodData`** — a `FoodData`, owned by
  [hunger, XP and effects](hunger-xp-and-effects.md).
- **Experience**: `Player.experienceLevel`, `Player.experienceProgress`,
  `Player.totalExperience`, `Player.enchantmentSeed`,
  `Player.lastLevelUpTime`, `Player.takeXpDelay`.
- **`Player.cooldowns`** — an `ItemCooldowns`, built by
  `Player.createItemCooldowns` so each side can subclass it.
- **`Player.gameProfile`**, `Player.lastDeathLocation`,
  `Player.sleepCounter`, `Player.fishing`, `Player.reducedDebugInfo`,
  `Player.lastItemInMainHand`, `Player.hurtDir`, `Player.jumpTriggerTime`,
  `Player.wasUnderwater`.
- **Synched data it declares**: `Player.DATA_PLAYER_ABSORPTION_ID`,
  `Player.DATA_SCORE_ID`, `Player.DATA_SHOULDER_PARROT_LEFT`,
  `Player.DATA_SHOULDER_PARROT_RIGHT` — four, and none of them is the
  hand or the skin, which went up to `Avatar`.
- **Slot offsets** for command and container addressing:
  `Player.ENDER_SLOT_OFFSET` (200), `Player.HELD_ITEM_SLOT` (499),
  `Player.CRAFTING_SLOT_OFFSET` (500), decoded by `Player.getSlot`.
- **Reach**: `Player.DEFAULT_BLOCK_INTERACTION_RANGE` (4.5) and
  `Player.DEFAULT_ENTITY_INTERACTION_RANGE` (3.0) are the *attribute*
  defaults; `Player.blockInteractionRange` and
  `Player.entityInteractionRange` read
  `Attributes.BLOCK_INTERACTION_RANGE` and
  `Attributes.ENTITY_INTERACTION_RANGE`
  ([attributes](../entities/attributes.md)), and
  `Player.isWithinBlockInteractionRange` /
  `Player.isWithinEntityInteractionRange` are the checks the server makes.

`Player` is abstract for one method above all: **`Player.gameMode`**,
which returns a nullable `GameType`. It also implements `ContainerUser`,
which is how a chest decides whether the player is still close enough to
keep it open (`Player.getContainerInteractionRange`).

A long tail of `Player` methods are empty hooks that exist so the two
sides can disagree — `Player.onUpdateAbilities`, `Player.awardStat`,
`Player.triggerRecipeCrafted`, `Player.crit`, `Player.magicCrit`,
`Player.sendSystemMessage`, `Player.doCloseContainer`,
`Player.openTextEdit`, `Player.sendMerchantOffers`,
`Player.handleCreativeModeItemDrop`. On `Player` they do nothing; the
subclass that has somewhere to send a packet overrides them.

### `Abilities` and `GameType`

`Abilities` is five public booleans and two floats:
`Abilities.invulnerable`, `Abilities.flying`, `Abilities.mayfly`,
`Abilities.instabuild`, `Abilities.mayBuild`, plus
`Abilities.getFlyingSpeed` / `Abilities.getWalkingSpeed`. It does not
serialise itself by hand — it packs into the record `Abilities.Packed`
and `Abilities.Packed.CODEC` does the work, via `Abilities.pack` and
`Abilities.apply`.

`GameType` is the four-constant enum (`GameType.SURVIVAL`,
`GameType.CREATIVE`, `GameType.ADVENTURE`, `GameType.SPECTATOR`) with
`GameType.DEFAULT_MODE`, a `GameType.CODEC` and a `GameType.STREAM_CODEC`.
The important method is **`GameType.updatePlayerAbilities`**: it is the
single place in the game that decides which abilities a mode grants, and
both sides call it. `GameType.isBlockPlacingRestricted` is what sets
`Abilities.mayBuild`, and `GameType.isSurvival` is true for
`GameType.ADVENTURE` too.

### `Inventory`

`Inventory` still implements `Container`, but its shape changed. It is
**one `Inventory.items` list of thirty-six stacks
(`Inventory.INVENTORY_SIZE`) plus a reference to the player's
`EntityEquipment`.** Slots at or above thirty-six are not stored here at
all: `Inventory.EQUIPMENT_SLOT_MAPPING` routes them into the equipment
object — the four armour indices, `Inventory.SLOT_OFFHAND` (40),
`Inventory.SLOT_BODY_ARMOR` (41) and `Inventory.SLOT_SADDLE` (42). So
`Inventory.getContainerSize` is forty-three, and a player carries the
same equipment container a horse does.

`Player.createEquipment` returns a **`PlayerEquipment`**, which overrides
the map so that `EquipmentSlot.MAINHAND` resolves to
`Inventory.getSelectedItem`. The held item is not stored twice; the main
hand *is* the selected hotbar slot, viewed through the equipment
interface.

The rest of the class is the vocabulary the whole game uses to put things
in a player: `Inventory.add`, `Inventory.getFreeSlot`,
`Inventory.getSlotWithRemainingSpace`,
`Inventory.placeItemBackInInventory`, `Inventory.findSlotMatchingItem`,
`Inventory.contains`, `Inventory.removeItem`,
`Inventory.clearOrCountMatchingItems`, `Inventory.dropAll`,
`Inventory.getSuitableHotbarSlot`, `Inventory.addAndPickItem` and
`Inventory.pickSlot` (pick-block), `Inventory.fillStackedContents`
(the recipe book). It saves as sparse slot/stack pairs through
`Inventory.save` and `Inventory.load`, and `Inventory.setSelectedSlot`
throws rather than accept a non-hotbar index.

### `ServerPlayer`

Everything that needs a server. `ServerPlayer.connection` (the
`ServerGamePacketListenerImpl`), `ServerPlayer.gameMode` (a
`ServerPlayerGameMode`), `ServerPlayer.advancements`, `ServerPlayer.stats`,
`ServerPlayer.recipeBook` (a `ServerRecipeBook`),
`ServerPlayer.chunkTrackingView` and `ServerPlayer.lastSectionPos` (what
the client has been sent — [tickets and loading](../world/tickets-and-loading.md)),
`ServerPlayer.respawnConfig`, `ServerPlayer.camera`,
`ServerPlayer.textFilter`, `ServerPlayer.wardenSpawnTracker`,
`ServerPlayer.enderPearls`, `ServerPlayer.containerSynchronizer`, and a
row of *last sent* fields — `ServerPlayer.lastSentHealth`,
`ServerPlayer.lastSentFood`, `ServerPlayer.lastSentExp`,
`ServerPlayer.lastRecordedArmor` and friends — that exist only so the
server can notice a change and send one packet.
[Players and sessions](../server/players-and-sessions.md) owns the
lifecycle of this object; it is constructed during the *configuration*
phase by `PrepareSpawnTask`, before the play listener exists.

It also remembers what the client *said*: `ServerPlayer.lastClientInput`
(an `Input`) and `ServerPlayer.lastKnownClientMovement`, which
[input to movement](input-to-movement.md) explains.

### The client side

`AbstractClientPlayer` adds three things: `AbstractClientPlayer.playerInfo`
(the tab-list entry, fetched lazily from the connection),
`AbstractClientPlayer.clientAvatarState` (the per-frame animation state
`AvatarRenderer` reads), and `AbstractClientPlayer.getSkin`. Its
`AbstractClientPlayer.gameMode` implementation is the surprising one —
see below.

`LocalPlayer` is the one the human steers: `LocalPlayer.connection`
(a `ClientPacketListener`), **`LocalPlayer.input`** (a `ClientInput`),
`LocalPlayer.lastSentInput`, the last-sent position block used to decide
whether to send a movement packet, `LocalPlayer.recipeBook` (a
`ClientRecipeBook`), `LocalPlayer.dropSpamThrottler`,
`LocalPlayer.permissions`, `LocalPlayer.autoJumpEnabled`,
`LocalPlayer.startedUsingItem`, and the view-bob fields
`LocalPlayer.yBob` / `LocalPlayer.xBob`.

`RemotePlayer` is every *other* player on the client: it sets
`Entity.noPhysics`,
interpolation through `RemotePlayer.lerpDeltaMovement`, and — tellingly —
an **empty `RemotePlayer.updatePlayerPose`**. Another player's pose is
told to you; it is not derived.

`LocalPlayer` does **not** hold the game-mode object. `Minecraft.gameMode`
does, and it is a `MultiPlayerGameMode`.

### The two game-mode objects

| | `ServerPlayerGameMode` (`server/level`) | `MultiPlayerGameMode` (`client/multiplayer`) |
|---|---|---|
| owns the mode | `ServerPlayerGameMode.getGameModeForPlayer` | `MultiPlayerGameMode.getPlayerMode` |
| changes it | `ServerPlayerGameMode.changeGameModeForPlayer` | `MultiPlayerGameMode.setLocalMode` |
| breaking state | `ServerPlayerGameMode.isDestroyingBlock`, `ServerPlayerGameMode.destroyProgressStart`, `ServerPlayerGameMode.hasDelayedDestroy` | `MultiPlayerGameMode.isDestroying`, `MultiPlayerGameMode.destroyProgress`, `MultiPlayerGameMode.destroyDelay` |
| the block hooks | `ServerPlayerGameMode.handleBlockBreakAction`, `ServerPlayerGameMode.useItemOn`, `ServerPlayerGameMode.useItem` | `MultiPlayerGameMode.startDestroyBlock`, `MultiPlayerGameMode.continueDestroyBlock`, `MultiPlayerGameMode.useItemOn`, `MultiPlayerGameMode.useItem` |
| attacking | — (`ServerGamePacketListenerImpl` handles it) | `MultiPlayerGameMode.attack`, `MultiPlayerGameMode.interact` |
| containers | — | `MultiPlayerGameMode.handleContainerInput` |

[Block interaction](../blocks/block-interaction.md) and
[block breaking](../blocks/block-breaking.md) own the block halves of both
columns, including the prediction ledger — which, note,
`MultiPlayerGameMode` does not hold: `MultiPlayerGameMode.startPrediction`
reaches for `ClientLevel.getBlockStatePredictionHandler` per call.

## When it runs

On the server, a player is ticked **twice per tick, by two different
callers, and the two halves do not overlap**.

- **`ServerPlayer.tick`** is called by the level's entity loop
  (`ServerLevel.tickNonPassenger`, from `EntityTickList`), and players are
  ticked there whether or not their chunk is entity-ticking
  ([the level tick](../server/server-level-tick.md)). It does **not** call
  `Player.tick` at all. It runs `ServerPlayerGameMode.tick`, decrements
  invulnerability, broadcasts the open menu
  (`AbstractContainerMenu.broadcastChanges`) and closes it if it is no
  longer valid, drags the camera entity along in spectator mode, fires the
  per-tick advancement criteria, and calls
  `ServerPlayer.updatePlayerAttributes`.
- **`ServerPlayer.doTick`** is called by
  `ServerGamePacketListenerImpl.tickPlayer`, from the connection tick,
  *after* the levels have ticked. This is the half that calls
  up into `Player.tick` and `LivingEntity.tick`, so
  **all of the player's physics happen here**. It then ticks
  `FoodData.tick`, the play-time statistics, the map-update sweep over
  every inventory slot, and every *has this changed since I last sent it*
  comparison that produces `ClientboundSetHealthPacket` and
  `ClientboundSetExperiencePacket`.

`Player.aiStep` — reached from `ServerPlayer.doTick` — is where
`Inventory.tick` runs
(so item ticking is once per tick, on whichever side is simulating),
along with the item and experience-orb pickup sweep and the shoulder
parrots.

On the client, `LocalPlayer.tick` runs from `ClientLevel`'s entity tick on
the main thread, gated on the connection reporting that the level has
loaded; `Minecraft.gameMode` is ticked separately from `Minecraft.tick`;
`ClientInput.tick` is called from inside `LocalPlayer.aiStep`, so input is
*sampled inside the tick*, not pushed from the key callback.

Netty threads never touch player state: every handler starts by deferring
to the owning thread ([the connection](../server/server-tick.md) covers
the mechanism).

## The trace: one server tick of one player

```mermaid
sequenceDiagram
    participant SL as ServerLevel
    participant SP as ServerPlayer
    participant GM as ServerPlayerGameMode
    participant CM as AbstractContainerMenu
    participant CL as ServerGamePacketListenerImpl
    participant PL as Player
    participant IN as Inventory
    participant FD as FoodData

    Note over SL: phase 1 — the entity loop
    SL->>SP: tick — no super.tick; the connection-free half
    SP->>GM: tick — block-breaking progress and delayed destroy
    SP->>CM: broadcastChanges — diff the open menu, then stillValid
    SP->>SP: updatePlayerAttributes — creative reach modifiers on/off

    Note over CL: phase 2 — the connection tick, after every level
    CL->>SP: doTick — via tickPlayer, bracketed by the position checks
    SP->>PL: Player.tick — then LivingEntity.tick: the physics half
    PL->>IN: tick — ItemStack.inventoryTick for all 36 slots
    SP->>FD: tick — hunger, regeneration, starvation
    SP->>CL: ClientboundSetHealthPacket — only if lastSentHealth differs
```

Read the two phases as answering different questions. Phase one asks
*what does the world do to this player* — the menu is diffed against what
the client was told, the breaking timer advances, the spectator camera
follows. It runs inside the level, in entity order, and it is the half
that still happens for a player whose connection has gone quiet.

Phase two asks *what did this player do*, and it can only run after the
packets for the tick have been processed. `ServerGamePacketListenerImpl`
brackets the call: it resets the player's position to the last accepted
one, runs `ServerPlayer.doTick` — which is where `Player.tick` finally
happens and the player actually moves, falls, drowns and burns — and then
applies the floating and flying checks. Everything the client must be
*told* about its own player leaves at the end of phase two, one packet per
field that changed.

The ordering matters for one thing above all: a container's contents are
broadcast in phase one but the click that changed them was handled before
phase one, and the health that phase two computes is compared against
`ServerPlayer.lastSentHealth`, not re-sent every tick.

## Interfaces

- **Called by:** `ServerLevel` (entity loop) and
  `ServerGamePacketListenerImpl` (connection tick) on the server;
  `ClientLevel` and `Minecraft` on the client. `PlayerList` creates,
  saves, respawns and removes `ServerPlayer`
  ([players and sessions](../server/players-and-sessions.md)).
- **Calls into:** `Inventory` / `EntityEquipment`
  ([items and stacks](../items/items-and-stacks.md)), `AbstractContainerMenu`
  ([containers and menus](../items/containers-and-menus.md)),
  `ServerPlayerGameMode` → `BlockBehaviour`
  ([block interaction](../blocks/block-interaction.md)), `FoodData`,
  `PlayerAdvancements`, `ServerStatsCounter`, and all of `LivingEntity`
  ([entity anatomy](../entities/entity-anatomy.md)).
- **Crosses the network as:** `ClientboundLoginPacket` and
  `ClientboundRespawnPacket`, both carrying a `CommonPlayerSpawnInfo`
  built by `ServerPlayer.createCommonSpawnInfo`;
  `ClientboundPlayerAbilitiesPacket` and the returning
  `ServerboundPlayerAbilitiesPacket`;
  `ClientboundGameEventPacket.CHANGE_GAME_MODE` and
  `ClientboundPlayerInfoUpdatePacket.Action.UPDATE_GAME_MODE` for a mode
  change; `ClientboundSetHeldSlotPacket` and the serverbound
  `ServerboundSetCarriedItemPacket` for the hotbar;
  `ClientboundSetPlayerInventoryPacket` (built by
  `Inventory.createInventoryUpdatePacket`);
  `ClientboundSetHealthPacket` and `ClientboundSetExperiencePacket`.
- **Data-driven by:** almost nothing. `Player.createAttributes` supplies
  the attribute defaults; game rules and server properties set the
  starting `GameType`. The player is one of the few systems in the game
  that a data pack cannot redefine.

## Invariants and surprises

- **`ServerPlayer.tick` never calls up into `Player.tick`.** The two halves are
  genuinely disjoint: physics lives in `ServerPlayer.doTick`, driven by
  the connection. A player whose packets have stopped keeps having menus
  diffed and breaking progress ticked while not moving or falling.
- **`Player.isCreative` and `Player.isSpectator` do not read
  `Abilities`.** They compare `Player.gameMode` against `GameType`
  constants. Only `Player.hasInfiniteMaterials` and
  `Player.preventsBlockDrops` still consult `Abilities.instabuild`.
- **On the client, a player's game mode comes from the tab list.**
  `AbstractClientPlayer.gameMode` resolves through
  `AbstractClientPlayer.getPlayerInfo`, so it is null until that entry has
  arrived — and the *only* reason the client knows anyone's mode is
  `ClientboundPlayerInfoUpdatePacket`.
- **`Avatar` holds no state.** It is a rendering seam, not a state seam,
  and it exists so `Mannequin` can be drawn by `AvatarRenderer` with the
  full skin pipeline. Everything one would call player anatomy is still on
  `Player`.
- **The main hand is not stored.** `PlayerEquipment` aliases
  `EquipmentSlot.MAINHAND` to `Inventory.getSelectedItem`, so
  `LivingEntity.getMainHandItem` and the selected hotbar slot are the same
  bytes.
- **`Inventory` has forty-three slots, not forty-one** — the player
  carries a body-armour and a saddle slot because it shares
  `EntityEquipment` with mobs.
- **`Abilities.mayBuild` never goes on the wire.**
  `ClientboundPlayerAbilitiesPacket` carries four flag bits and two
  floats; the client recomputes the build permission by calling
  `GameType.updatePlayerAbilities` itself.
- **`Abilities` saves under keys that do not match its fields** —
  `Abilities.Packed.CODEC` writes *flySpeed* and *walkSpeed*. And one
  constant is misspelled in the source: `Abilities.DEFAULY_FLYING`.
- **`RemotePlayer.updatePlayerPose` is empty.** Poses for other players
  are synched state, not a local derivation — which is why a desynced
  swimming animation stays wrong until the server says otherwise.
- **There is no *PlayerRenderer*, and no *setPickedItem* on `Inventory`.**
  The renderer is `AvatarRenderer`; pick-block is
  `Inventory.addAndPickItem`.

## Where to look

`Player` · `Avatar` · `ServerPlayer` · `AbstractClientPlayer` ·
`LocalPlayer` · `RemotePlayer` · `Inventory` · `PlayerEquipment` ·
`Abilities` · `GameType` · `ServerPlayerGameMode` · `MultiPlayerGameMode` ·
`ServerGamePacketListenerImpl` · `PrepareSpawnTask` · `Mannequin` ·
`AvatarRenderer` · `ClientAvatarEntity`

---

*Rules: names, never code · how the system works, not how the code reads ·
newest version only · every backticked name passes `tools/verify_names.py`.*
