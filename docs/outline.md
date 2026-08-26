# The lecture map

Fourteen lectures, ordered by dependency (each assumes the ones before it)
and sized to where the code actually is. One page each; every page traces
one scenario. The owner plans each lecture in its own session — this is the
map, not the schedule.

| # | Lecture | Traces | Packages |
|---|---|---|---|
| 1 | **Anatomy** | One codebase, three processes (client, integrated server, dedicated server). The threads: Render, Server, Netty IO, the worker pool (chunk gen + IO), Sound. The *two* loops — the client's frame loop with a 20 Hz tick inside it and `partialTick` bridging them; the server's 20 Hz tick with overload catch-up. The source map. | `client/Minecraft`, `server/MinecraftServer`, `client/server/IntegratedServer` |
| 2 | **The tick** | `MinecraftServer.tickServer` → `ServerLevel.tick` → chunks, block ticks, entities, network flush; `Minecraft.runTick` on the client. The spine every later lecture hangs a lane on. | `server/level`, `world/level/Level` |
| 3 | **The data-driven core** | Registries (static vs dynamic, `ResourceKey`/`Holder`), `Codec`s and NBT/JSON, resource packs vs data packs, tags. Why half the game is JSON. | `core`, `resources`, `server/packs`, `data` |
| 4 | **Blocks** | `Block` vs `BlockState` (the state table, properties), block entities, a placement/interaction from click to world. | `world/level/block` |
| 5 | **The world** | Chunks and sections, palette storage, region files, the **ticket system** (why chunks load), the sky/block light engines, save and load. | `world/level/chunk`, `world/level/lighting`, `server/level` |
| 6 | **Entities** | The hierarchy, `SynchedEntityData` (what the client is told), attributes and modifiers, AI: goal selectors vs the brain/behaviour system. | `world/entity` |
| 7 | **Items and inventories** | `Item` vs `ItemStack`, data components (the 1.20.5 rewrite that replaced NBT on items), containers and the click protocol. | `world/item`, `world/inventory`, `core/component` |
| 8 | **Movement and combat** | Movement is client-authoritative with server sanity checks; attack cooldown, knockback, hit detection, i-frames, sprint hits — a sword swing from click to damage. | `world/entity/player`, `world/entity/LivingEntity`, `client/player` |
| 9 | **Networking** | The Netty pipeline, the five protocol phases (handshake, status, login, configuration, play), `StreamCodec`, what is synced when, what the client's copy of the world actually is — and why vanilla gives the high-ping player what it gives them. | `network`, `network/protocol`, `server/network`, `client/multiplayer` |
| 10 | **Rendering I — the frame** | `GameRenderer` → `LevelRenderer`, section meshing on the worker pool, render types and the shader pipeline, the lightmap. Where the frame time goes. | `client/renderer` |
| 11 | **Rendering II — everything else on screen** | Entity models and animation, the GUI and HUD, particles, the sound engine. | `client/model`, `client/gui`, `client/particle`, `client/sounds` |
| 12 | **World generation** | Density functions, the noise router, biomes, features and structures. High-level by necessity — the most data-driven system in the game. | `world/level/levelgen`, `data/worldgen` |
| 13 | **Commands and data-pack "scripting"** | Brigadier, functions, predicates, loot tables, advancements — the programming model with no compiler. | `commands`, `server/commands`, `world/level/storage/loot`, `advancements` |
| 14 | **Epilogue — how mods hook in** | Obfuscation and mappings (why Yarn and Mojang names differ), mixins, why the loaders diverge. Last, not fourth: it is about the ecosystem, not the source, and it is the one topic already documented elsewhere. | — |

**Appendix, one sentence each:** `util/datafix` (save migration between
versions), `gametest`, `client/telemetry`, `util/profiling`, `server/jsonrpc`,
`server/dialog`.

Folded rather than standalone: particles and sound (11), player input (1 and
8), modding APIs (14). The old outline's lecture 2 was three lectures (3, 7
and half of 9).
