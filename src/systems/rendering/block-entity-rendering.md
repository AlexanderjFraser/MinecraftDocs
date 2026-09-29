# Block-entity rendering

> Verified against **Minecraft 26.3** · Part XI · a chest on the ground and a chest in your hand, drawn in the same frame by two renderers that share one model definition.

You place a chest, step back, and hold a second one up in front of your face.
Both are chests, both are lit, both open the same lid on the same hinge — and
almost nothing about how they got onto the screen is shared. The one on the
ground is a *block entity*: the terrain mesh at its position contains no
geometry at all, and everything you can see of it was extracted from the live
world by `ChestRenderer` a few microseconds ago. The one in your hand is an
*item*: it has no block entity, it is extracted as part of your player, and it
is drawn by a class in a different package that exists for chests that are
not block entities. The seam shows if you type */tick freeze*. The chest
on the ground is nailed to its last tick; the chest in your hand keeps
swaying with your view bob, because the two are drawn at **different partial
ticks** and only one of them respects the freeze.

This page is the sibling of [entity rendering](entity-rendering.md), and does
not re-teach it. Four stages run here exactly as they run there — **extract**
reads the live world into a value object, **submit** describes what ought to
be drawn without drawing it, **prepare** groups every description in the frame
and sorts the translucent phases back to front, and **execute** is the frame graph's passes issuing the draws —
along with render states that hold no live entity, `SubmitNodeCollector`, and
the phases a submission can land in. All of that is that page's, and
all of it is true here. What follows is only the differences, and they are
larger than the shared machinery suggests.

## The cast

| class | what it decides | thread |
|---|---|---|
| `LevelExtractor` | which block entities are candidates at all — the two lists it walks | Render thread |
| `BlockEntityRenderDispatcher` | the renderer for a type, and two of the three gates an extraction passes | Render thread |
| `BlockEntityRenderer` | the geometry, and its own answers to *how far* and *off screen* | Render thread |
| `BlockEntityRenderState` | one block entity's whole frame: position, block state, type, light, break progress | a value object |
| `ClientLevel` | membership of the globally-rendered set, decided once when the block entity is added | Render thread |
| `SpecialModelRenderer` | the thirteen shapes an item model cannot express, drawn without a block entity | Render thread |
| `SpecialModelWrapper` | how an item model reaches one — the item road into `renderer/special` | Render thread |
| `BuiltInBlockModels` | how a *block state* reaches one, in a model table terrain never reads | a worker thread, on every resource reload |

## Three roads to the same collector

```mermaid
flowchart TD
    BE["A chest placed in the world"]
    IT["A chest as an item: held, shelved or dropped"]
    BD["A chest block shown by an entity"]
    SEC["LevelExtractor walks the visible sections, then the globally-rendered set"]
    BERD["BlockEntityRenderDispatcher — one shared ChestRenderer, one fresh ChestRenderState"]
    IMR["ItemModelResolver finds the stack's item model"]
    SMW["SpecialModelWrapper opens a layer with its renderer"]
    BMR["BlockModelResolver reads the built-in block-model table"]
    SBM["SpecialBlockModelWrapper sets its renderer on a BlockModelRenderState"]
    CSR["a ChestSpecialRenderer, from renderer/special"]
    COL["SubmitNodeCollector — the same phases, the same feature renderers, the same vertices"]
    BE --> SEC
    SEC --> BERD
    BERD --> COL
    IT --> IMR
    IMR --> SMW
    SMW --> CSR
    BD --> BMR
    BMR --> SBM
    SBM --> CSR
    CSR --> COL
```

*Three ways a chest reaches the collector: its own block entity on the left,
and two roads that end in the same special renderer class on the right. Only
the left road's chest is a block entity; the other two are drawn by whatever
holds them.*

Two of the three roads end in `renderer/special`, and that is the package's
whole reason to exist: a chest that is not a block entity still has to look
like a chest. Only the left-hand road has a visibility policy of its own, or an
extract stage that reads the live world.

| | entity | block entity | special model |
|---|---|---|---|
| what is walked | the level's renderable entities | the visible sections' meshes, then a global set | nothing — it is reached from a model |
| the visibility test | a frustum, plus a size-scaled distance | the *section* is visible, then a per-renderer radius | whatever drew the thing holding it |
| the stages | extract, finalize, submit | extract, submit | resolved in its holder's extract, submitted in its holder's submit |
| the state | an `EntityRenderState` subclass | a `BlockEntityRenderState` subclass | a layer of an `ItemStackRenderState`, or a `BlockModelRenderState` |
| the partial tick | one computed per entity | one for every block entity in the world | its holder's — in your hand, the player's, then the camera entity's |
| where the pose comes from | the dispatcher, from the state's position | `LevelRenderer`, translated to the block | the item transform for the display context, or the block model's own |
| how many | one renderer per entity type, or per skin model for a player or a mannequin | 26 of the 49 types, served by 24 classes — `ChestRenderer` takes three of them | 13 renderers under 13 ids |

## The chest, both halves, one frame

Followed through one frame, band by band, the two chests take these routes:

```mermaid
sequenceDiagram
    participant LX as LevelExtractor
    participant FPHAI as FirstPersonHands<br/>AndItems
    participant BERD as BlockEntity<br/>RenderDispatcher
    participant ChestR as ChestRenderer
    participant LR as LevelRenderer
    participant FPHAIR as FirstPersonHands<br/>AndItemsRenderer

    rect rgba(0, 0, 0, 0.04)
    Note over LX,FPHAIR: extract — the hand at the player's partial tick, the block entities at the world's
    LX->>FPHAI: extractRenderState, at the player's own partial tick
    FPHAI->>FPHAI: the held chest resolved — a special renderer, no quads
    LX->>BERD: tryExtractRenderState, for a block entity in a visible section
    BERD->>ChestR: createRenderState, then extractRenderState, past the off-screen and distance gates
    end
    rect rgba(0, 0, 0, 0.04)
    Note over LX,FPHAIR: submit — into the level's storage, then the hand's own
    LR->>BERD: submit, the pose translated to the block
    BERD->>ChestR: submit — one model, one sprite, no world access
    FPHAIR->>FPHAIR: the held stack's layer submits to the ChestSpecialRenderer
    end
```

*Both chests in one frame, extract then submit: the ground chest goes through
the block-entity classes, the held one through the hand's. They have separate
renderers, states and storages, and share the chest model's layer definition.*

The two chests are not two runs of one pipeline. The world's block entities
go through `LevelRenderer.submitFeatures` into the frame graph. The held
chest is extracted with the player, by `FirstPersonHandsAndItems`, and
`FirstPersonHandsAndItemsRenderer` submits it into [the hand's own submit
storage](the-frame.md#the-hand-and-the-screen-effects-in-a-storage-the-level-never-sees),
drained after the whole world is already on the screen. They never share a
submit node.

## The chest's block model is empty, and there are two tables of them

Open *blockstates/chest.json* and it names one model for every state. Open
that model and it declares a particle texture and no elements. So when
`SectionCompiler` walks the section and tesselates every block whose render
shape is *MODEL*, the chest contributes exactly zero quads to the terrain
mesh — and, in the same pass, adds itself to the section's list of block
entities. Everything you see of a placed chest is drawn one stage later, by a
renderer, from a snapshot.

That is what a block entity renderer is *for*: the shapes that a cuboid model
cannot express, and the state that a block state cannot hold. Only 26 of the
49 entries in `BlockEntityTypes` have a renderer registered in
`BlockEntityRenderers`, and the other 23 — furnaces, hoppers, barrels,
beehives — are drawn entirely by their block models, like any other block.
Having a block entity does not make a block interesting to look at.

There are **two** baked block-model tables, and confusing them is easy.
`ModelManager.getBlockStateModelSet` is the one built from the resource
packs, and it is the one `SectionCompiler` reads: a chest is empty in it.
`ModelManager.getBlockModelSet` is built on top of that one and merged with
`BuiltInBlockModels.createBlockModels`, which attaches a
`SpecialBlockModelWrapper` to every state of every chest, banner, skull,
shulker box, conduit, decorated pot, bell, enchanting table, end gateway, end
portal and copper golem statue in the game. Nothing in terrain ever reads
that table — that is the whole of the separation, and it is membership rather
than behaviour. `BlockModelResolver` is its one reader, and every caller that
reads it is an *entity* renderer: item frames, block displays, minecart
contents, the golems, the block an enderman is carrying, and a few more. It reaches the
block-entity side too, as a field of `BlockEntityRendererProvider.Context` —
the record the block-entity renderers are constructed from — where nothing
reads it, because a block entity already has a renderer and does not need to
find one through a model. When an entity renderer draws a chest it gets
whatever quads the block has, which for a chest is none, **and** the special
renderer, because that road draws whatever it finds; terrain simply never asks this table, and reads `BlockStateModelSet`
instead, where the chest's entry is empty.

### What one entry in the built-in table actually holds

The reason one entry can hold quads *and* a renderer is the object the road
resolves into. `BlockModelResolver` hands the model a
`BlockModelRenderState`, which has a slot for each: a list of
`BlockStateModelPart`, a transformation, a `RenderType`, a
`SpecialModelRenderer` with a transformation of its own, and the tint layers
and light. Every `BlockModel` implementation writes into that one object, and
what comes out is submitted in one go.

Not every entry in it is a wrapped block, either. The three airs are an
`EmptyBlockModel`; wildflowers and pink petals are a `SelectBlockModel` that
branches on the display context; and the two ordinary chests are a
`CompositeBlockModel` whose special half is a `ConditionalBlockModel` — the
Christmas switch this page comes back to. Most of the rest are a
`CompositeBlockModel` too: the block's own quads *and* the
special renderer stacked. **Five are not**, and get the renderer alone with
no quads under it — the bell, the conduit, the end gateway, the end portal
and the enchanting table, whose built-in model is `BookSpecialRenderer` and
nothing else. Put an enchanting table in a block display and you get a book
hanging in the air.

## Frustum-culled by section, not one by one

A block entity is never frustum-tested on its own.
`LevelExtractor.extractVisibleBlockEntities` starts from
`LevelRenderer.visibleSections` — the sections of the reachability walk that
survived the frustum, which [visibility and the frame
graph](visibility-and-the-frame-graph.md) describes — and takes each section's compiled list of block entities whole.
Culling has already happened, one section at a time.

**Three gates of visibility decide whether a block entity is extracted from a section**, and only
the first belongs to the walk. The other two are stricter than they look, and
`BlockEntityRenderDispatcher.tryExtractRenderState` holds both. The first is
the section's own fade-in: a freshly uploaded section reports a visibility
ramping from zero to one over a duration the *chunk section fade-in time*
option sets, and `LevelExtractor` skips its block entities until that number
reaches **0.3**. Terrain fades in from the first frame, and the chests inside
it appear about a third of the way through — furniture arriving after the
room. The ramp starts at a section's first upload and a recompile never
restarts it, so the gate bites on arriving terrain at any distance, and never
on a chest you place in terrain already drawn.

The second is the off-screen flag, which the section after this one is about.
The third is a distance test with the same name as the entity one and only
half of its behaviour. `EntityRenderer.shouldRender` does a size-scaled
distance test *and* a frustum intersection. `BlockEntityRenderer.shouldRender`
keeps the distance half alone: a camera position, and whether the block's
centre is within `BlockEntityRenderer.getViewDistance`.

**Sixty-four blocks** — the default, taken by nineteen of the twenty-four
renderer classes, and it does not scale with your render distance the way
`Entity.shouldRender` does.

| renderer | how far | why |
|---|---|---|
| the other nineteen | 64 | the interface default |
| `PistonHeadRenderer` | 68 | a moving block starts outside the block it is drawn from |
| `BlockEntityWithBoundingBoxRenderer` | 96 | the structure block's outline is a build tool — and its extraction sets a visibility flag from `Player.canUseGameMasterBlocks` or spectator mode, so its output, and the box the test-instance renderer draws through it, depends on your permissions |
| `TheEndGatewayRenderer` | 256 | the beam is the thing you are looking for |
| `BeaconRenderer` | the render distance in blocks | and measured **horizontally only** |
| `TestInstanceRenderer` | the larger of its two delegates | it wraps a beacon and a bounding box |

The beacon is the interesting row twice over. Its `BlockEntityRenderer.shouldRender` flattens both
positions onto the horizontal plane before comparing, so altitude never costs
you the beam — you can be at build height above a beacon at bedrock and still
see it. And its extraction scales the beam's radius by the horizontal distance
divided by 96, floored at one, so **the beam gets visibly wider the further
away you stand**, which is why a distant beacon does not thin into nothing.
Raising a spyglass resets the scale to one, because `BeaconRenderer` checks
whether the local player is scoping. The topmost beam segment is drawn
`BeaconRenderer.MAX_RENDER_Y` tall, 2048 blocks up from where it starts.

### Off screen means off *this* list

`BlockEntityRenderer.shouldRenderOffScreen` picks which of two lists a block
entity is drawn from, and it is enforced twice.
`ClientLevel.onBlockEntityAdded` puts a block entity into
`ClientLevel.getGloballyRenderedBlockEntities` only if its renderer says yes,
and `BlockEntityRenderDispatcher.tryExtractRenderState` throws the extraction
away unless the flag it was called with **equals** the renderer's answer. The
second check is what stops double-drawing: a beacon inside a visible section
is in that section's list *and* in the global set, and the equality test is
the only thing that picks one. Exactly three renderers say yes —
`BeaconRenderer`, `BlockEntityWithBoundingBoxRenderer` and
`TestInstanceRenderer`, which says yes because either of its two delegates
does.

## What a block entity's snapshot carries

`blockentity/state` holds 26 classes: the base and twenty-five subclasses. The
base is five fields wide — the position, the block state, the type, packed
light sampled from the level, and the crumbling overlay — and it is filled by
one static method, `BlockEntityRenderState.extractBase`, that every renderer
calls before adding its own. There is no `EntityRenderer.finalizeRenderState`
counterpart here: `BlockEntityRenderer` declares one extraction method, not
two, so there is no second extraction step; the two live handles this page
comes to are held by reference instead.

The crumbling overlay is the fifth field and the only one built outside the
renderer. `LevelExtractor` looks the block position up in
`ClientLevel.destructionProgress`, takes the *last* entry of the sorted set —
`BlockDestructionProgress` orders on the stage first and the digger's entity
id only to break a tie, so two players on one block show whichever crack is
further along — and wraps that stage and a pose into a
`ModelFeatureRenderer.CrumblingOverlay`. This is the only place
in the game a non-null one is made, which is why [a mob is never
crumbled](entity-rendering.md#why-the-zombie-is-animated-more-than-once) and
a chest being mined is. The global list is extracted with a null overlay
outright, so a beacon someone is breaking gets its cracks from its block
model alone, never from its renderer.

Twenty-five subclasses, twenty-six classes: `BedRenderState` is reachable from
nothing in the game. There is no bed block entity in `BlockEntityTypes` and no
bed renderer, and a corpus-wide search for the name finds only its own file.
It is the only orphan in the package.

### The five states that carry another pipeline's snapshot

Five states carry another pipeline's snapshot inside them, which is where the machines touch — and **two** of the five carry an *entity* state, not
an item one. `SpawnerRenderState.displayEntity` is a whole
`EntityRenderState`, extracted through `EntityRenderDispatcher` from a display
entity the spawner creates client-side — a mob that `LevelExtractor` never
sees, never frustum-tests, and whose light the spawner overwrites with the
block's. `VaultRenderState.displayItem` reads like the item cases and is not
one: it is an `ItemClusterRenderState`, which extends `EntityRenderState`, and
the vault submits it through `ItemEntityRenderer` — the same renderer that
draws a dropped item lying on the ground. The three genuine item carriers are
`ShelfRenderState.items`, an array of three `ItemStackRenderState` — so a
shelved item is resolved and submitted by the *item* road, from inside a
block-entity render state, and lands on whichever special renderer its own
model names — and `CampfireRenderState.items` and
`BrushableBlockRenderState.itemState` for what is cooking and what is buried.

Two live handles survive into snapshots, and the first is not unique to this
side:
`MovingBlockRenderState` is a one-block fake world that holds the level's
`MovingBlockRenderState.lightEngine` and `MovingBlockRenderState.cardinalLighting`
by reference, so a moving block is lit at *prepare* time rather than at
extract. `PistonHeadRenderState` carries up to two of them, and the entity
side's `FallingBlockRenderState` carries one.

Signs are the second. `SignRenderState` stores the block entity's own two
`SignText` objects rather than laid-out glyphs, and `AbstractSignRenderer`
calls `Font.split` during **submit** when that text has no lines cached for
the current filtering setting — a stage later than the rest of the snapshot.

## One partial tick for the whole world

This is the difference a player can see. [Six partial ticks are in play in
one frame](the-frame.md#update-and-extract-six-clocks-in-one-frame), and
block entities take the row that has no exception in it. The entity side is
asked per entity, `TickRateManager.isEntityFrozen` at a time, so a mob exempt
from a freeze keeps interpolating while its neighbours stop. Block entities
get no such question: they all receive the single
`DeltaTracker.getGameTimeDeltaPartialTick` value the world got, which returns
exactly 1.0 while the game is frozen. Every block entity in the world is
therefore pinned to its last completed tick, with no per-block exemption
anywhere in the path.

The held chest is asked the entity side's question, twice:
`FirstPersonHandsAndItems.extractRenderState` runs at the local player's own
partial tick, and the hand is posed at submit off
`Camera.getCameraEntityPartialTicks`, which puts the same question to the
camera entity. The frozen check never freezes a `Player`, so under
*/tick freeze* the item in your hand is redrawn from a live partial tick while
every chest lid in the world is stopped dead. A mob exempt from the freeze, a chest lid and the chest in your hand: three
things drawn in one frame, and whether each one moves depends only on which
question it was allowed to ask.

The same split shows up in the Christmas textures, which the game implements
three times. `ChestRenderer` reads `SpecialDates.isExtendedChristmas` **once,
in its constructor**, and its constructor runs only when
`BlockEntityRenderDispatcher.onResourceManagerReload` rebuilds every renderer
— so a placed chest that was ordinary at 23:59 on the 23rd stays ordinary
until the next resource reload. The item model in *items/chest.json* selects on
the *minecraft:local_time* property, whose `LocalTime` implementation re-checks
the clock at most once a second. And the built-in block model wraps its two
chests in a `ConditionalBlockModel` whose `IsXmas` property calls the same
static method live, every time the model is resolved. Two of the three notice
midnight almost at once. The one you are standing in front of does not.

## Where `renderer/special` borrows its geometry

`SpecialModelRenderers.bootstrap` registers thirteen renderers under thirteen
ids, dispatched by a codec, and the package holds exactly thirteen renderer
classes to match. Nine of them implement `NoDataSpecialModelRenderer` and read
nothing at all from the stack; the other four — banner, decorated pot, player
head and shield — pull what they need out of it through
`SpecialModelRenderer.extractArgument`, which is the closest thing this road
has to an extract stage.

Eleven of the thirteen reach into `client/renderer/blockentity` for their
geometry. Three hold an instance of the block-entity renderer outright
(`BannerSpecialRenderer`, `DecoratedPotSpecialRenderer`,
`ShulkerBoxSpecialRenderer`); the rest call a static submit or name a static
texture or model layer on one — `SkullBlockRenderer.submitSkull`,
`AbstractEndPortalRenderer.submitSpecial`, `BannerRenderer.submitPatterns`,
`ChestRenderer.LAYERS`. Only `TridentSpecialRenderer` and
`CopperGolemStatueSpecialRenderer` stand alone. The chest in your hand really
is a `ChestModel`, baked from the same `ModelLayerLocation`, posed at a
fixed openness instead of an interpolated one.

`ChestRenderer` aside, this page teaches the shape of the twenty-four rather
than the instances, because a family is what they are: each is one
`BlockEntityRenderer.extractRenderState` and one `BlockEntityRenderer.submit`,
and the interesting ones differ in how far they can be seen and from which
list, both above, and in what they put in their render state — the structure
block drawing gizmos instead of submitting geometry, and the test instance
drawing gizmos beside a submitted beacon beam. The shared piece
worth naming is
`WallAndGroundTransformations`, which is how a skull, a banner or a sign
answers *am I on the floor or on a wall* — one transformation per
`Direction` for the wall case and an array indexed by rotation segment for
the free-standing one, built once into a static field of the renderer rather
than per frame.

### How an empty item model turns into a chest

Reaching a special renderer from an item is one indirection: `SpecialModelWrapper` is an
`ItemModel` like any other, and its baked form puts the renderer into a layer
of the `ItemStackRenderState` through
`ItemStackRenderState.LayerRenderState.setupSpecialModel`. A layer either has
quads or has a special renderer, never both, and the layer's submit picks
whichever it has. That is the entire mechanism by which an empty item model
turns into a chest.

> **For a 1.21-era reader.** *BedRenderer* is gone, and so is the bed's
> block entity: a bed is drawn by its block models like any other block, and
> the `BedRenderState` the renderer filled is left in `blockentity/state` with
> nothing to fill it.

## Where to look

`BlockEntityRenderDispatcher.tryExtractRenderState` first — it contains two of
the three visibility gates. Then
`LevelExtractor.extractVisibleBlockEntities` for the two lists it walks, and `ChestRenderer` as the clearest renderer in the package, since its
counterpart in `renderer/special` is the one this page compares it with. For the
other road, `SpecialModelWrapper` and `ItemStackRenderState.LayerRenderState`,
then `BuiltInBlockModels` for the block-state road nobody expects to exist.
[Submit phases and feature renderers](../../reference/submit-phases.md) is the
catalogue everything here submits into.

---

*Rules: names, never code · how the system works, not how the code reads ·
newest version only · every backticked name passes `tools/verify_names.py`.*
