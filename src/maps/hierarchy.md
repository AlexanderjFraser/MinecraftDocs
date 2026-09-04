# What extends what

> Verified against **Minecraft 26.2** · Maps · The widest inheritance trees, four of them drawn with the number of descendants on every node.

`Block` has 293 subclasses and `Entity` 191, and those are the two trees a
reader of this book will climb most often. But neither is the widest
hierarchy in the game. That is `FeatureElement`, with 386 descendants from
seven implementers — and it is not a hierarchy at all. It is a marker
interface for *anything that can be put behind a feature flag*, and its
seven implementers are `BlockBehaviour`, `Item`, `EntityType`, `MenuType`,
`MobEffect`, `Potion` and `GameRule`, so it inherits the whole block tree
and the whole item tree at once. `ItemLike`, second at 366, is `Block` plus
`Item`. The interface table is a list of which mix-ins reach furthest; the
class table is where the real trees are, and four of them are drawn below.

## Entity

<figure class="map">
{{#include ../generated/tree-Entity.svg}}
<figcaption>The <code>Entity</code> tree to three levels. The number is how many types descend from the node; subclasses with no subclasses of their own are folded into one italic line per parent. Click to enlarge.</figcaption>
</figure>

The shape is a spine with a few branches. `LivingEntity` holds 124 of the
191, `Mob` 114 of those, `PathfinderMob` 108 of those: a mob is four
classes deep before it is a species, and Part VI's
[entity anatomy](../systems/entities/entity-anatomy.md) is that spine.
The non-living entities are two families and a scattering — `Projectile`
(26) and `VehicleEntity` (15), then hanging things, displays, and
thirteen direct subclasses of `Entity` with no children of their own, from
`ItemEntity` to `LightningBolt`.

## Block

<figure class="map">
{{#include ../generated/tree-Block.svg}}
<figcaption>The <code>Block</code> tree to three levels; 61 of its 92 direct subclasses have no subclasses of their own and are folded into the last line. Click to enlarge.</figcaption>
</figure>

`Block` is wide and shallow: 92 direct subclasses, most of them terminal.
The one deep branch is `BaseEntityBlock` (64), the blocks that own a
block entity, which is Part V's
[block entities](../systems/blocks/block-entities.md) page in tree form.
The table's first row, `BlockBehaviour` at 294, is the same tree seen from
one class higher — `Block` is its only subclass, and it exists so that a
block's behaviour and its registry identity can be separate classes.

## Item

<figure class="map">
{{#include ../generated/tree-Item.svg}}
<figcaption>The <code>Item</code> tree to three levels. Click to enlarge.</figcaption>
</figure>

Seventy-one subclasses for over a thousand registered items. The tree is
small because an item's behaviour mostly is not in its class: what a stack
does is in its data components, and `Items` registers most of the game
as a plain `Item` with a `Item.Properties` describing it. Part VII's
[items and stacks](../systems/items/items-and-stacks.md) is why the tree
is this shape.

## Screen

<figure class="map">
{{#include ../generated/tree-Screen.svg}}
<figcaption>The <code>Screen</code> tree to three levels; 60 of its 72 direct subclasses have no subclasses of their own. Click to enlarge.</figcaption>
</figure>

`Screen` (158) is `Block`'s shape again — 72 direct subclasses, 60 of
them terminal — with one deep branch, `AbstractContainerScreen` (27), the
screens that show a menu, and one branch that is not in this book,
`RealmsScreen` (23). The row above it in the table,
`AbstractContainerEventHandler` at 159, is `Screen`'s parent with `Screen`
as its only subclass, the same one-class-higher effect as
`BlockBehaviour`.

## Two trees the table shows and the figures do not

`Goal` has 200 descendants from 99 direct subclasses, and 130 of the 200
are nested classes inside the mob they serve — a fox's goals are declared
in `Fox`, not in `world/entity/ai/goal`. `Packet` is an interface with 236 descendants from 227
direct implementers, and almost nothing below them: the packet catalogue is
flat, and the [packets](../reference/packets.md) reference is its list.

## The tables

Class roots first, then interface roots; a root needs fifteen descendants
to appear. *direct* is the number of immediate subclasses or implementers;
*where* is the package of the root.

{{#include ../generated/hierarchy-classes.md}}

{{#include ../generated/hierarchy-interfaces.md}}

---

*Rules: names, never code · how the system works, not how the code reads ·
newest version only · every backticked name passes `tools/verify_names.py`.*
