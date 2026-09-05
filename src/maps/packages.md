# Where the code is

> Verified against **Minecraft 26.2** · Maps · The jar as a treemap of packages: area is lines of decompiled source, colour is which jar ships the package, hatching is what this book skips.

Java Minecraft is 7,055 classes and 719,302 lines of decompiled Java 25,
and the first surprise in it is which half is bigger. Everything a player
sees — every screen, the HUD, the whole renderer, the entity models, both
GPU back-ends, the sound engine, Realms — is the orange near-third of this
picture. The blue seven tenths ship in both jars, and the biggest box
of all, `world/level`, is a fifth of the game by itself: blocks, block
states, chunks, lighting and world generation, all of it code the
dedicated server runs with no window attached.

<figure class="map">
{{#include ../generated/packages-treemap.svg}}
<figcaption>The 26.2 decompile as a treemap. Each outer box is a package directly under <code>net/minecraft</code> or <code>com/mojang</code>, labelled with its share of the lines; the boxes inside are its sub-packages. Hover a box for its counts; click the figure to enlarge it.</figcaption>
</figure>

## Two jars, one tree

The client jar is a strict superset of the server jar, and the split is
clean: the 2,206 client-only classes live in exactly four packages —
`net/minecraft/client` (1,864 classes), `com/mojang/blaze3d` (211),
`com/mojang/realmsclient` (127) and `net/minecraft/realms` (4). Every other
package in the table below ships in both jars, class for class; no
sub-package at this depth is mixed. The client-only side is 212,242
lines, 29.5% of the total, which is the "just under a third" the
introduction quotes.

The consequence for reading this book: when a page says a class is
*client-only* it is saying which package the class lives in, and when a
page in Part IV or V names a class, the dedicated server has it. The class
index in Reference says which side each named class is on; the oracle
behind it is `server-classes.txt`.

## What the big boxes are

**world — 42%.** `world/level` (146,417 lines, 1,312 classes) is Parts
IV, V and XII: chunks, block states, lighting and, under
`world/level/levelgen`, most of world generation — `world/level/biome` is
its sibling rather than part of it. `world/entity`
(109,061 lines, 716 classes) is Parts VI and VIII: the entity hierarchy,
its AI and the player. `world/item` and `world/inventory` (36,363 lines
between them) are Part VII.

**client — 24%.** `client/gui` (59,057 lines) is the screens and the HUD,
Part X; `client/renderer` and `client/model` (61,108 lines together) are
the frame, section meshing and the entity models, Part XI;
`client/multiplayer` (11,169) holds `ClientPacketListener` and
`ClientLevel`, the client's copy of the world. The 41 classes directly in
`net/minecraft/client` — `Minecraft`, `Options`, `KeyMapping`,
`MouseHandler` — are 10,709 lines on their own.

**util — 7%, two thirds of it skipped.** `util/datafix`, `util/filefix`
and `util/profiling` are 34,176 of the package's 53,275 lines and are all
outside this book; the hatched box is the save-migration history. What is
left is the toolbox every part uses — `Mth`, `RandomSource`, `Util` — and
the parsing and debug packages.

**server — 7%.** `server/commands` (12,781) is Part XIII's command
implementations; `server/level` is 42 classes and 11,977 lines — 285 lines a class, nearly
three times the map's average, in a package small enough to list
(`ServerLevel`, `ChunkMap`, `ServerPlayer`), Parts III and IV; `server/network` is the serverbound
packet handlers, Part IX; `server/packs` is the pack system, Part II;
`server/jsonrpc`, the management server, is skipped.

**blaze3d — 4%.** The GPU abstraction has two back-ends behind
`GpuDevice`, and the Vulkan one (`blaze3d/vulkan`, 7,477 lines) is larger
than the OpenGL one (`blaze3d/opengl`, 5,627).

**network — 3%, in 411 classes.** `network/protocol` is 293 classes in
12,934 lines: the packet catalogue is many tiny classes, one per packet.
`network/chat` (4,818) is `Component` and chat signing.

Below 3% the boxes are Part II's foundations — `net/minecraft/core`,
`net/minecraft/nbt`, `net/minecraft/tags`, `net/minecraft/resources`,
`net/minecraft/commands` (the command source, the argument types and the
execution engine, Part XIII) and `net/minecraft/advancements`, plus
`com/mojang/realmsclient` and the skipped `net/minecraft/data`. That last one
is the program that writes the vanilla data pack — and it is not build-time
only: the dedicated server ships all 163 classes, and `Blocks` and
`MinecraftServer` both read `data/worldgen` constants at run time ([what this
book skips](../systems/anatomy/what-this-book-skips.md) has the three
exceptions).

## Where each part lives

The parts follow the tree, but not one box each. This table is the map
from the book's order to the jar's; a part's landing page says the same
thing with the classes named.

| part | packages |
|---|---|
| I · Anatomy | `client/main`, `net/minecraft/server` (the two `Main`s, `MinecraftServer`), `net/minecraft/client` (`Minecraft`) |
| II · Foundations | `net/minecraft/core`, `net/minecraft/resources`, `net/minecraft/tags`, `net/minecraft/nbt`, `core/component`, `server/packs`, `net/minecraft/util` |
| III · The server | `net/minecraft/server`, `server/level`, `server/players`, `server/dedicated` |
| IV · The world | `world/level/chunk`, `world/level/chunk/storage`, `world/level/lighting`, `world/ticks`, `world/level/gameevent`, `world/level/entity`, `server/level` |
| V · Blocks | `world/level/block`, `world/level/block/state`, `world/level/block/entity`, `world/level/redstone` |
| VI · Entities | `world/entity`, `world/entity/ai`, `world/entity/ai/attributes`, `network/syncher`, `world/level/pathfinder` |
| VII · Items and inventories | `world/item`, `world/inventory`, `world/item/crafting`, `world/item/enchantment`, `world/level/storage/loot` |
| VIII · The player | `world/entity/player`, `world/food`, `server/level` (`ServerPlayer`), `client/player` |
| IX · Networking | `net/minecraft/network`, `network/protocol`, `network/codec`, `network/chat`, `server/network`, `client/multiplayer` |
| X · The client | `net/minecraft/client`, `client/gui`, `client/multiplayer`, `client/sounds`, `client/resources`, `client/player` |
| XI · Rendering | `client/renderer`, `client/model`, `client/particle`, `com/mojang/blaze3d` |
| XII · World generation | `world/level/levelgen`, `world/level/biome`, `world/level/levelgen/structure` |
| XIII · Commands and data packs | `net/minecraft/commands`, `server/commands`, `server/dialog`, `net/minecraft/advancements`, `net/minecraft/gametest`, `world/scores` |

## The table

Depth three is the outer boxes of the treemap; depth four is the inner
ones. *client-only* counts the classes not in `server-classes.txt`.

{{#include ../generated/packages-depth3.md}}

{{#include ../generated/packages-depth4.md}}

---

*Rules: names, never code · how the system works, not how the code reads ·
newest version only · every backticked name passes `tools/verify_names.py`.*
