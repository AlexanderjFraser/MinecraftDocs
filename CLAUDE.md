# MinecraftDocs — how Java Minecraft works

**What this is:** system-level documentation of the Java Minecraft codebase
— the *current* version only — written as the notes for a video lecture
series. One page per lecture, each following one thing through the system
(a tick, a placed block, a chunk coming into view, a packet, a frame, a sword
swing) with a diagram whose lanes are class names. The site is the notes;
the video is the lecture. Readers are humans who'd rather watch and agents
who'd rather fetch the whole corpus at once.

**Owner:** Alexander Fraser (`AlexanderjFraser`). The owner has to *learn*
each system to record it, so the work is in passes (the owner is the "meat
proxy": starts sessions, approves nothing technical): **pass 1** — Claude
drafted every page from the decompile (done; `docs/pass1.md`); **pass 2** —
completeness and accuracy: every claim adversarially fact-checked against
the decompile, and every page had at least one wrong claim (done;
`docs/pass2.md`); **pass 3** — restructuring: the site becomes a book — each
part takes the shape of its system, each page the shape of its story, the
frame, introduction, maps and reference tier redone, the lecture order
drafted (**current**); **pass 4** — the second fact-check, pass 2's protocol
over everything pass 3 rewrote; **pass 5** — polish: wording, consistency,
cuts; **pass 6+** — the owner reads each page against the source, asks
questions in the page, and confirms the lecture order; then voice and cuts.
Nothing is recorded that the owner hasn't understood.

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
6. **Diagrams render.** `node tools/check_mermaid.js` parses every diagram in
   the built site with the site's own mermaid (11.6.0). A diagram that
   fails does not publish — mermaid ends a statement at `;` and reads `#` as
   an entity code, so neither goes in a label.

## The source

The Mojang-mapped decompile is **not in this repo** (it can't be — this repo
is public and the EULA/mappings licence forbids redistributing it). It lives
at `reference/26.2/` (gitignored; the zips it came from are gitignored too)
and `tools/verify_names.py` / `tools/map_source.py` default to it; `MC_SOURCE`
overrides. The client jar is a strict superset of the server jar, so
`reference/26.2/` is the client decompile plus `server-classes.txt`, the list
of classes the dedicated server also ships — the oracle for "is this class
server-side or client-only". 7,055 classes, 719k lines, Java 25.

Beside it, also gitignored: **`reference/26.2/data/` and
`reference/26.2/assets/`** — the jar's data packs and its non-texture assets
(models, blockstates, items, atlases, fonts, particles, the six `post_effect`
chains and the shader tree), the fact base for every data-driven claim; and
**`reference/libs/`** — the Mojang libraries the game depends on, staged by
`tools/fetch_libs.sh`: Brigadier 1.3.10 and DataFixerUpper 10.0.21 (MIT,
published source jars) and authlib 9.0.75 (decompiled from the launcher's
jar, like the game). `verify_names.py` checks library names at member level
from those trees, so `CommandDispatcher.execute` or `Codec.STRING` is
verified, not allow-listed. A fact-check agent should read them rather than
take a library's behaviour on trust.

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
| gametest, telemetry, profiling, jsonrpc, advancements… | ~1,000 | | one sentence each in *what this book skips* |

Naming drift a 1.21-era reader will trip on: `ResourceLocation` is now
`Identifier`; `Util` lives in `net.minecraft.util`; `LightTexture` is
`Lightmap`; `Timer` is `DeltaTracker`; `Gui` and `Hud` both exist.

## The page (`TEMPLATE.md`)

`TEMPLATE.md` is a **menu of shapes** (trace · pipeline · state machine ·
policy · comparison · vocabulary · pattern · landing page), written by
pass-3 session A from two pilots — `tickets-and-loading` (policy) and
`protocol-phases` (state machine) — with the devices, the budgets, the
mermaid rules and **the lane key**, which `python tools/check_lanes.py`
enforces (key expansions must exist in the decompile; page drift is
reported, `--strict --pages src/systems/<part>` per part as sessions
convert). What every page keeps:
the verified line with the part and scenario; an opening paragraph that
starts inside the scenario and ends on the hook (the surprising true thing
the page explains); a cast of at most eight classes instead of field
inventories; at least one figure; headings that say what the section says,
not which template slot it fills; *Where to look*; the rules footer.
Budgets: a list is at most seven items of at most two sentences, at most
three lists a page; anything explanatory is prose, anything enumerative
beyond seven is a table or a Reference page.

## The plan

[docs/plan.md](docs/plan.md) — the passes, the current pass's charter,
rulings, session protocol and schedule, and the session log. **Read it
first; tick it last.** [docs/pass3.md](docs/pass3.md) is the restructuring
notebook (eleven sessions of pass-2 evidence on part shapes, splits,
diagram shapes, dependencies and open questions, plus §7 the coverage
queue); [docs/pass4.md](docs/pass4.md) is where pass-3 sessions list what
the second fact-check must re-check; [docs/pass5.md](docs/pass5.md) collects
wording debt and cuts. **A session that leaves something for later appends
to the right one of those, not only to the log.** `docs/pass1.md` and
`docs/pass2.md` are the archived passes (charter, protocol, queue, log —
still worth grepping); `docs/outline.md` is the archived fourteen-lecture
map. The lecture order is drafted in pass 3 (`src/lectures.md`) and
confirmed by the owner in pass 6.

## Site

mdBook 0.5 (`book.toml`, `src/SUMMARY.md`) with `mdbook-mermaid`; both are in
`~/.cargo/bin` (not on PATH in Git Bash). Layout: `src/introduction.md`;
`src/maps/` (the atlas, generated by `tools/map_source.py`); `src/systems/<part>/`
(the content; each part gets a `README.md` landing page in pass 3, which is
what the folding sidebar opens on); `src/reference/` (generated by
`tools/gen_reference.py`, `verify_names.py --index` and `check_lanes.py
--index`, plus the hand-kept look-up pages); `src/lectures.md` (the lecture order). `custom.css` widens
the column for tables, diagrams and figures and caps prose at 800px;
`diagram-zoom.js` opens any diagram at viewport size on click.
Moved pages keep their URLs through `[output.html.redirect]` in `book.toml`.
`tools/deploy.sh` verifies names, checks diagrams, builds, writes
`llms-full.txt` (the whole corpus in one file, via `tools/llms_full.py`) and
deploys to Cloudflare Pages project `minecraftdocs`
(https://minecraftdocs.pages.dev, custom domain **minecraftdocs.dev**) using
the token at `~/.cloudflare/pvpmod.token`. `tools/check_mermaid.js` needs
node and a one-time `npm install` in `tools/` (see its header comment).

## Conventions

- Mojang names throughout, said once in the introduction; note the Yarn
  name only where a modder would otherwise not recognise a class.
- Figures: mermaid blocks in the page for anything mermaid 11.6.0 draws;
  **generated** SVG from `tools/` (inlined with `{{#include}}`) for the maps
  and for figures no mermaid type draws; never a hand-drawn or raster image.
- Lanes are class initials, at least two letters, one meaning corpus-wide
  (`SGPL`, `CPL`, `MC`, `MS`, `SL`); the key lives in `TEMPLATE.md`.
- Reasoning > sensing > measuring; the owner judges what lands.
- `verify_names.py`, `check_mermaid.js` and `check_lanes.py --strict --pages
  <the part>` before every commit that touches a page.
