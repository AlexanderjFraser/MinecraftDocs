# MinecraftDocs — how Java Minecraft works

**What this is:** system-level documentation of the Java Minecraft codebase
— the *current* version only — written as the notes for a video lecture
series. One page per lecture, each following one thing through the system
(a tick, a placed block, a chunk coming into view, a packet, a frame, a sword
swing) with a sequence diagram whose lanes are class names. The site is the
notes; the video is the lecture. Readers are humans who'd rather watch and
agents who'd rather fetch the whole corpus at once.

**Owner:** Alexander Fraser (`AlexanderjFraser`). The owner has to *learn*
each system to record it, so the work is in passes: **pass 1** — Claude
drafts every page from the decompile (the owner is the "meat proxy": starts
sessions, approves nothing technical); **pass 2** — the owner reads each
page against the source, asks questions in the page, and the docs are
corrected and the lecture order chosen; pass 3 is voice and cuts. Nothing is
recorded that the owner hasn't understood.

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
   Currently **26.2**.
4. **Trace-driven.** A lecture follows a scenario through the system; the
   trace is the spine and the diagram is the artefact. A package tour is
   the boring version and the one you learn least from.
5. **Verified names.** `python tools/verify_names.py` checks that every
   backticked identifier on every page exists in the decompile. A page that
   fails does not publish. "Verified against 26.2" is a test, not a claim.

## The source

The Mojang-mapped decompile is **not in this repo** (it can't be — this repo
is public and the EULA/mappings licence forbids redistributing it). It lives
at `reference/26.2/` (gitignored; the zips it came from are gitignored too)
and `tools/verify_names.py` / `tools/map_source.py` default to it; `MC_SOURCE`
overrides. The client jar is a strict superset of the server jar, so
`reference/26.2/` is the client decompile plus `server-classes.txt`, the list
of classes the dedicated server also ships — the oracle for "is this class
server-side or client-only". 7,055 classes, 719k lines, Java 25.

Where the game is (26.2, from `python tools/map_source.py packages`; the
full tables are in `src/maps/`):

| package | classes | lines | |
|---|---:|---:|---|
| `world/level` | 1,312 | 146k | blocks, block states, chunks, lighting, world generation |
| `world/entity` | 716 | 109k | the entity hierarchy, AI, attributes, players |
| `client/gui` | 444 | 59k | screens, HUD |
| `client/renderer` + `client/model` | 968 | 61k | the frame, section meshing, entity models, render pipelines |
| `com/mojang/blaze3d` | 211 | 26k | the GPU abstraction — `opengl` **and `vulkan`** backends behind `GpuDevice` |
| `world/item` + `world/inventory` | 378 | 36k | items, containers, data components |
| `network/protocol` | 293 | 13k | the packet catalogue (machinery in `network/`, `server/network`) |
| `server/level` | 42 | 12k | `ServerLevel`, `ChunkMap`, tickets — small package, huge classes |
| `server/commands` + `commands/*` | ~220 | 26k | Brigadier, execution |
| `util/datafix` + `util/filefix` | 453 | 30k | save migration — **out of scope by rule 3** |
| `com/mojang/realmsclient` | 127 | 13k | Realms UI — out of scope |
| gametest, telemetry, profiling, jsonrpc, advancements… | ~1,000 | | one sentence each in the appendix |

Naming drift a 1.21-era reader will trip on: `ResourceLocation` is now
`Identifier`; `Util` lives in `net.minecraft.util`; `LightTexture` is
`Lightmap`; `Timer` is `DeltaTracker`; `Gui` and `Hud` both exist.

## The page skeleton (`TEMPLATE.md`)

Responsibility · the data it owns · when it runs (tick/frame, thread) · the
trace (sequence diagram) · interfaces (who calls it, what it calls, what
crosses the network) · invariants and surprises · where to look (entry-point
class names only).

## The plan

[docs/plan.md](docs/plan.md) — pass 1: fifty-six system pages in thirteen
parts, a generated reference layer, sixteen sessions, one part per
session, the per-session protocol (fact sheets from the decompile → pages →
verify → deploy) and the session log. **Read it first; tick it last.**
`docs/outline.md` is the archived fourteen-lecture map; the lecture order
is decided in pass 2, after the owner has read the pages.

## Site

mdBook (`book.toml`, `src/SUMMARY.md`) with `mdbook-mermaid`; both are in
`~/.cargo/bin` (not on PATH in Git Bash). Layout: `src/maps/` (generated by
`tools/map_source.py`), `src/reference/` (generated by `tools/gen_reference.py`
and `verify_names.py --index`), `src/systems/<part>/<page>.md` (the content),
`src/lectures.md` (the lecture order, decided in pass 2). `tools/deploy.sh` verifies, builds and deploys
to Cloudflare Pages project `minecraftdocs` (https://minecraftdocs.pages.dev,
custom domain **minecraftdocs.dev**) using the token at
`~/.cloudflare/pvpmod.token`, and writes `llms-full.txt` (the whole corpus in
one file, via `tools/llms_full.py`).

## Conventions

- Mojang names throughout, said once in the introduction; note the Yarn
  name only where a modder would otherwise not recognise a class.
- Diagrams are mermaid `sequenceDiagram` / `flowchart` blocks in the page,
  never images.
- Reasoning > sensing > measuring; the owner judges what lands.
- `verify_names.py` before every commit that touches a page.
