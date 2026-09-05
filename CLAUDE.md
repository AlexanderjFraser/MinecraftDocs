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
proxy": starts sessions, approves nothing technical, judges what lands).
**Ten passes leave the site finished.** Passes 1–4 are done: **1** the rough
draft from the decompile; **2** every claim adversarially fact-checked;
**3** restructuring — the site became a book, each part the shape of its
system, each page one of eight shapes, the frame, maps and Reference tier
redone, the lecture order drafted; **4** the second fact-check, pass 2's
protocol over everything pass 3 rewrote (each archived whole in
`docs/passN.md`; every page had at least one wrong claim in both checks).
Passes 5–8 are four passes of restructuring and refinement with one lens
each: **5 the book** (across pages — ownership, seams, through-lines, the
landing pages as the part's argument, the coverage question, the last
moves; **next**), **6 the lecture** (one page at a time — the devices that
became slots, the twin skeletons, the cuts), **7 the figures** (every figure
as rendered; the fifth gate, names inside mermaid blocks), **8 the voice**
(one voice, the tics, the terminology, the ambiguous counts). Then **9** the
third fact-check and **10** the last polish. Beside them, a **version pass**
runs between passes on each release, and the owner reads whenever they
like, leaving `<!-- Q: … -->` in a page for the next session that touches
it. Nothing is recorded that the owner hasn't understood.

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
7. **Lanes mean one thing.** `python tools/check_lanes.py --strict` checks
   every `participant` in every sequence diagram against the lane key in
   `TEMPLATE.md`; a page whose lane disagrees with the key does not
   publish. Add a row to the key when a page introduces a lane; never
   change a row's meaning.

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
mermaid rules and **the lane key** (rule 7). Over the 102 system pages the
shapes fell out as trace 31, vocabulary 25, pipeline 19, comparison 11,
policy 7, pattern 7, state machine 2; the *Questions players ask* closer is
on 69 of them, which is pass 6's first job. What every page keeps: the
verified line with the part and scenario; an opening paragraph that starts
inside the scenario and ends on the hook (the surprising true thing the page
explains); a cast of at most eight classes instead of field inventories; at
least one figure; headings that say what the section says, not which
template slot it fills; *Where to look*; the rules footer. Budgets: a list
is at most seven items of at most two sentences, at most three lists a
page; anything explanatory is prose, anything enumerative beyond seven is a
table or a Reference page.

## The plan

[docs/plan.md](docs/plan.md) — the ten passes, why they are in that order,
the rhythm every pass follows, the current pass's charter, the standing
rules for passes 5–8, the version pass, the owner's read, and the session
log from pass 5 on. **Read it first; tick it last.** Each finished pass is
archived whole in `docs/passN.md` (charter, rulings, protocol, schedule,
log — still worth grepping; pass 2's fact-check protocol and lessons and
pass 4's additions are what pass 9 runs; the plan as it stood at pass 4's
close is at the end of `docs/pass4.md`). The queues: [docs/pass5.md](docs/pass5.md)
is what passes 5–8 draw on — structural findings to 5, page-shape findings
to 6, figure findings to 7, wording debt to 8, each struck as settled;
[docs/pass9.md](docs/pass9.md) is where every pass-5-to-8 session lists the
claims it introduced and the corrections it made, so pass 9 checks them
first; [docs/pass3.md](docs/pass3.md) §7 is the coverage queue (a system
with no owner page) and seeds a second edition. **A session that leaves
something for later appends to the right one of those, not only to the
log.** Each pass starts with a planning session (Fable) that builds its
tools and brief — pass 4's are the model: [docs/pass4-brief.md](docs/pass4-brief.md)
and `tools/pass4_prompts.py` (one prompt file per page from
`pass4_queue.py`, `claims.py` and `diagram_arrows.py`) — and then runs
sessions A–O on Opus; `tools/check_deps.py` checks the landing pages, the
lecture table and the parts-dependency figure against each other.
`docs/outline.md` is the archived fourteen-lecture map. The lecture order
is drafted (`src/lectures.md`, with the parts-dependency figure) and
confirmed by the owner before pass 9.

## Site

mdBook 0.5 (`book.toml`, `src/SUMMARY.md`) with `mdbook-mermaid`; both are in
`~/.cargo/bin` (not on PATH in Git Bash). Layout: `src/introduction.md`;
`src/maps/` (the atlas: hand-written prose around the figures and tables
that `tools/map_source.py` writes into **`src/generated/`**, which is never
hand-edited and is regenerated by `deploy.sh`; the figure pipeline —
`<figure class="map">` + `{{#include}}` + classes themed in `custom.css` —
is in `TEMPLATE.md` for any page that needs a figure mermaid cannot draw);
`src/systems/<part>/`
(the content; each part's `README.md` is its landing page, which is what
the folding sidebar opens on); `src/reference/` (the shelf: eight views
generated by `tools/gen_reference.py`, two indexes by `verify_names.py
--index` and `check_lanes.py --index`, and the hand-kept catalogues and
look-up pages, which `verify_names.py` checks like any system page — its
README is the tier's landing page); `src/figures/` (a hand-kept mermaid
figure two pages share through `{{#include}}` — today the parts-dependency
graph, on the introduction and `lectures.md`); `src/lectures.md` (the
lecture order and the dependencies between parts); `src/robots.txt` (ships
with the build; points at the sitemap). `theme/head.hbs` is the only theme
override — Open Graph and Twitter-card meta on every page. `custom.css`
widens the column for tables, diagrams and figures and caps prose at 800px;
`diagram-zoom.js` opens any diagram at viewport size on click;
`site-footer.js` puts the licence and the disclaimer on every page.
Moved pages keep their URLs through `[output.html.redirect]` in `book.toml`;
`site-url = "/"` keeps the 404 page's links absolute under nested paths.
`tools/deploy.sh` regenerates the atlas and the eight Reference views, runs
the four gates, builds, writes `llms-full.txt` (the whole corpus in one
file, `tools/llms_full.py`) and `sitemap.xml` + `llms.txt` (the index form,
`tools/site_index.py`), and deploys to Cloudflare Pages project
`minecraftdocs` (https://minecraftdocs.pages.dev, custom domain
**minecraftdocs.dev**, a full Cloudflare zone with DNS done) using the token
at `~/.cloudflare/pvpmod.token` — stored wrapped in quotes, which
`deploy.sh` strips. The token edits Pages and reads the zone; it cannot
touch Web Analytics, which is not enabled and is the owner's click.
`tools/check_mermaid.js` needs node and a one-time `npm install` in `tools/`
(see its header comment).

## Conventions

- Mojang names throughout, said once in the introduction; note the Yarn
  name only where a modder would otherwise not recognise a class.
- Figures: mermaid blocks in the page for anything mermaid 11.6.0 draws;
  **generated** SVG from `tools/` (inlined with `{{#include}}`) for the maps
  and for figures no mermaid type draws; never a hand-drawn or raster image.
- Lanes are class initials, at least two letters, one meaning corpus-wide
  (`SGPL`, `CPL`, `MC`, `MS`, `SL`); the key lives in `TEMPLATE.md`.
- Reasoning > sensing > measuring; the owner judges what lands; no count in
  a queue is a target.
- `verify_names.py`, `check_mermaid.js` and `check_lanes.py --strict`
  before every commit that touches a page, and `check_deps.py` when a
  landing page, `lectures.md` or the dependency figure changes; `deploy.sh`
  runs all four — after regenerating the atlas and the eight Reference
  views — and refuses to publish on a failure.
- A published page never names a pass number as a promise about the
  future; when a pass closes, grep `README.md`, this file, `TEMPLATE.md`
  and the frame pages for the old numbers.
- Commit your own files by name, never `add -A`: two sessions are often
  open at once and pass sessions sweep the tree.
