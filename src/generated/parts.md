| part | packages | classes | client-only | lines |
|---|---|---:|---:|---:|
| I · Anatomy | `client/main`, `Minecraft`, `Main`, `MinecraftServer` | 7 | 5 | 6,817 |
| II · Foundations | `core`, `resources`, `tags`, `nbt`, `server/packs`, `util`, `world/flag` | 468 | 0 | 48,809 |
| III · The server | `server` (itself only), `server/level`, `server/players`, `server/dedicated` | 95 | 0 | 21,900 |
| IV · The world | `world/level/chunk`, `world/level/lighting`, `world/ticks`, `world/level/gameevent`, `world/level/entity`, `world/level/material`, `world/attribute`, `world/timeline`, `world/clock`, `world/level/border`, `server/level`, `world/level/blockscan` | 229 | 0 | 31,913 |
| V · Blocks | `world/level/block`, `world/level/redstone` | 484 | 0 | 58,507 |
| VI · Entities | `world/entity`, `network/syncher`, `world/level/pathfinder`, `world/damagesource`, `world/effect`, minus `world/entity/player` | 766 | 0 | 112,091 |
| VII · Items and inventories | `world/item`, `world/inventory`, `world/level/storage/loot` | 581 | 0 | 49,245 |
| VIII · The player | `world/entity/player`, `world/food`, `ServerPlayer`, `client/player` | 32 | 11 | 8,460 |
| IX · Networking | `network`, `server/network`, `client/multiplayer`, minus `network/syncher` | 490 | 51 | 38,711 |
| X · The client | `client` (itself only), `client/gui`, `client/multiplayer`, `client/sounds`, `client/resources`, `client/player`, `client/input`, `client/server` | 689 | 689 | 94,527 |
| XI · Rendering | `client/renderer`, `client/model`, `client/particle`, `com/mojang/blaze3d`, `com/mojang/renderpearl` | 1,291 | 1,291 | 98,283 |
| XII · World generation | `world/level/levelgen`, `world/level/biome` | 477 | 0 | 49,303 |
| XIII · Commands and data packs | `commands`, `server/commands`, `server/dialog`, `server/permissions`, `server/bossevents`, `advancements`, `gametest`, `world/scores`, `client/gui/screens/dialog` | 481 | 17 | 44,083 |
| **the thirteen parts, with the shared packages counted twice** | | 6,090 | 2,064 | 662,649 |
