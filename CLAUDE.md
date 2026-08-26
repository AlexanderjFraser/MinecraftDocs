# MinecraftDocs — how Java Minecraft works

**What this is:** system-level documentation of the Java Minecraft codebase
— the *current* version only — written as the notes for a video lecture
series. One page per lecture, each following one thing through the system
(a tick, a placed block, a chunk coming into view, a packet, a frame, a sword
swing) with a sequence diagram whose lanes are class names. The site is the
notes; the video is the lecture. Readers are humans who'd rather watch and
agents who'd rather fetch the whole corpus at once.

**Owner:** Alexander Fraser (`AlexanderjFraser`). The lectures are the main
product and the owner has to *learn* each system to record it — so a page is
drafted by Claude from the decompile, then read against the source and
corrected by the owner before it is published or recorded. Nothing ships
that the owner hasn't understood.

## The rules

1. **Names, never code.** A page names classes, methods, fields and packages
   (Mojang's official names, as the decompile uses them) and explains what
   they own, when they run and how they interact. It never reproduces source
   — not a method body, not a snippet. Anyone who needs the code decompiles
   it themselves; this is also the line the Mojang mappings licence draws.
2. **How the system works, not how the code reads.** Object-level analysis is
   fine (this class owns that state; this call happens on that thread);
   line-level walkthroughs are not. Code makes boring video and dates fast.
3. **Newest version only.** Every page states `verified against <version>`
   in its header. No version-difference sections, no "in 1.x this was…".
   When a release lands, re-verify the pages (a re-read, rarely a rewrite).
   Currently **1.21.11**.
4. **Trace-driven.** A lecture follows a scenario through the system; the
   trace is the spine and the diagram is the artefact. A package tour is
   the boring version and the one you learn least from.
5. **Verified names.** `python tools/verify_names.py` checks that every
   backticked identifier on every page exists in the decompile. A page that
   fails does not publish. "Verified against 1.21.11" is a test, not a claim.

## The source

The McDeob-remapped decompile is **not in this repo** (it can't be — this
repo is public). It lives at `d:\pvpmod\reference\minecraft` on the owner's
machine and `MC_SOURCE` points at it; `d:\pvpmod\tools\decompile_mc.py`
regenerates it from the remapped client on any machine. ~6,600 classes.

Where the game is (class counts, 1.21.11):

| package | classes | |
|---|---|---|
| `world/level` | 1,291 | blocks, block states, chunks, lighting, world generation |
| `world/entity` | 698 | the entity hierarchy, AI, attributes, players |
| `client/renderer` + `client/model` | 859 | the frame, chunk meshing, entity models, shaders |
| `client/gui` | 429 | screens, HUD |
| `world/item` + `world/inventory` | 370 | items, containers, data components |
| `network/protocol` | 288 | the packet catalogue (machinery in `network/`, `server/network`) |
| `server/commands` + `commands/*` | ~190 | Brigadier, execution |
| `util/datafix` | 384 | save migration — **out of scope by rule 3** |
| gametest, telemetry, profiling, jsonrpc, advancements… | ~1,100 | one sentence each in the appendix |

## The page skeleton (`TEMPLATE.md`)

Responsibility · the data it owns · when it runs (tick/frame, thread) · the
trace (sequence diagram) · interfaces (who calls it, what it calls, what
crosses the network) · invariants and surprises · where to look (entry-point
class names only).

## The lecture map

[docs/outline.md](docs/outline.md) — fourteen lectures ordered by
dependency and sized to the packages. The owner plans each lecture in its own
session; the outline is the map, not a schedule.

## Site

mdBook (`book.toml`, `src/SUMMARY.md`), with a mermaid preprocessor for the
diagrams and a single-file export for agents (`llms.txt` / `llms-full.txt`).
Hosted on Cloudflare Pages; the domain is the owner's to buy. The prototype
game's `tools/deploy_site.py` (in `d:\pvpmod`) is the model for the deploy.

## Conventions

- Mojang names throughout, said once in the introduction; note the Yarn
  name only where a modder would otherwise not recognise a class.
- Diagrams are mermaid `sequenceDiagram` / `flowchart` blocks in the page,
  never images.
- Reasoning > sensing > measuring; the owner judges what lands.
- `verify_names.py` before every commit that touches a page.
