# MinecraftDocs — how Java Minecraft works

**What this is:** system-level documentation of the Java Minecraft codebase
— the *current* version only — written as the notes for a video lecture
series. One page per lecture, each following one thing through the system
(a tick, a placed block, a chunk coming into view, a packet, a frame, a sword
swing) with a diagram whose lanes are class names. The site is the notes;
the video is the lecture. Readers are humans who'd rather watch and agents
who'd rather fetch the whole corpus at once (every page is also served as
markdown at its `.md` address, and `llms-full.txt` is the whole book).

**Owner:** Alexander Fraser (`AlexanderjFraser`). The owner has to *learn*
each system to record it, so the work is in passes (the owner is the "meat
proxy": starts sessions, approves nothing technical, judges what lands by
reading the live site). Nothing is recorded that the owner hasn't understood.

**Where the work is (2026-09-26).** Seven passes are done: **1** the rough
draft from the decompile; **2** every claim adversarially fact-checked;
**3** the restructuring into a book of thirteen parts and eight page shapes;
**4** the second fact-check; **5** the book, read across pages (171
corrections, half of them one page contradicting another); **6** the lecture,
each page read down by a reader with nothing but the page (about two hundred
corrections, almost all *a sentence that disagrees with the text beside it*);
**7** the figures, every one looked at rendered for the first time (about 180
facts corrected inside figures; its standing finding *a message labelled with
the caller's method and drawn arriving at the callee*, which the figure gate
now catches). Each is archived whole — `docs/passN.md` for 1–4, the brief's
Part 5 for 5–7. **Pass 8, the release, is current** and is the last pass
before the site is left stable: the version (26.3 shipped 2026-09-15), the
third fact-check over the ledger in `docs/pass9.md`, a polish over the exact
wording done after the check and read again by a session that changed
nothing, Part XI's figures (pass 7's one unrun session), the queues closed,
the tag `release-26.3`. Its brief is `docs/pass8-brief.md`; its schedule
(sessions V1, V2, A–Q, nineteen) with the status column the owner reads is
that file's Part 6; **V1, V2, A, B and C have run** (the tools read 26.3 and every
page says 26.3; V2 rewrote the 42 pages whose systems 26.3 reshaped; A ruled the
voice into `TEMPLATE.md` and found the book's *constant nobody reads* asides to
be javac's inlining, not the game; B made 293 corrections on Parts I and II and
the atlas; C made 176 on Part III, and the audit of its own record found 38
more, 15 of them in sentences C had just written), and session D is next. After it the
production process is rebuilt from first
principles on a new subject (`D:\DjangoDocs`, its `docs/brief.md`) and
returns here with what it learned; until then only a version pass the owner
asks for and the corrections readers file touch the site. Beside the passes,
the owner reads whenever they like, leaving `<!-- Q: … -->` in a page for the
next session that touches it.

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
   in its header. No version-difference sections, no "in 1.x this was…"
   (the one allowed drift note is the *For a 1.21-era reader* blockquote at a
   page's foot). When a release lands, the version pass re-verifies the pages
   (`docs/plan.md`, *The version pass*; `tools/version_pass.py` stages the
   tree). **The tools read 26.3 (2026-09-15), and each page is checked against
   the release its own header names** (built in pass 8's session V1, so a
   version pass moves the book a page at a time with every header true); since
   session V2 every page says 26.3, and `verify_names.py --current`, which
   fails any page left behind, passes. The version is one constant,
   `tools/mc_version.py`.
4. **Trace-driven.** A lecture follows a scenario through the system; the
   trace is the spine and the diagram is the artefact. A package tour is
   the boring version and the one you learn least from.
5. **Verified names.** `python tools/verify_names.py` checks that every
   backticked identifier on every page exists in the decompile of the release
   the page's header names (library names in the versions that release pins).
   A page that fails does not publish. "Verified against 26.3" is a test, not
   a claim.
   `python tools/check_figure_names.py --strict` asks the same of every
   name *inside* a mermaid block — a lane, a node, a message, a class box —
   and has been a gate since pass 7's close: a member is `Class.member` in a
   figure as in the prose, and a message's head is checked against the lane it
   arrives at.
6. **Diagrams render, and are legible where they stand.** `node
   tools/check_mermaid.js` parses every diagram in the built site with the
   site's own mermaid (11.6.0). A diagram that fails does not publish —
   mermaid ends a statement at `;` and reads `#` as an entity code, so neither
   goes in a label. Parsing is not the test a reader applies:
   `node tools/render_figures.js` shows every figure at the reading column, and
   since pass 7 a figure is legible there **without the zoom**. The whole visual
   grammar — the wrap, the palettes, the five semantic classes, the caption —
   is in `mermaid-init.js` and `custom.css`, and a page carries no
   `%%{init}%%`, `classDef`, `style` or `linkStyle` (`check_mermaid.js` fails
   one); `TEMPLATE.md`'s *Figures* is the rest.
7. **Lanes mean one thing.** `python tools/check_lanes.py --strict` checks
   every `participant` in every sequence diagram against the lane key in
   `TEMPLATE.md`; a page whose lane disagrees with the key does not
   publish. Add a row to the key when a page introduces a lane; never
   change a row's meaning.
8. **Links resolve.** `python tools/check_links.py` checks every internal
   link, anchor, include, `SUMMARY.md` entry and `book.toml` redirect; a
   broken one does not publish. An anchor is a heading's mdBook id, so a
   heading that moves takes its links with it or breaks the build — which is
   why no pass rewords a heading for its wording.

## The source

The Mojang-mapped decompile is **not in this repo** (it can't be — this repo
is public and the EULA/mappings licence forbids redistributing it). It lives
under `reference/` (gitignored, with the jars it came from), one tree per
version: `reference/26.3/`, the book's, and `reference/26.2/`, which no gate
needs now that every page says 26.3 (kept for diffing the two releases); each tree's
`libraries.json` names the library versions its release pins. Every tool reads
the tree `tools/mc_version.py` names (`MC_SOURCE` overrides). Since 26.x the
game jar ships with Mojang's names in it, so a tree is a plain Vineflower
decompile of the client jar — `python tools/version_pass.py <version>` does
the whole staging from Mojang's manifest in about ten minutes, with the
decompiler bundled in the sibling project's McDeob jar, run with McDeob's own
options (without them every `@Override` is dropped and every line count shrinks). The client jar is a
strict superset of the server jar, so a tree is the client decompile plus
`server-classes.txt`, the list of classes the dedicated server also ships —
the oracle for "is this class server-side or client-only". 26.2: 7,055
classes, 719k lines, Java 25; 26.3: 7,301 classes, 741k lines, 271 removed and
517 added, 5,037 server classes, protocol 777.

Beside the Java in each tree: **`data/` and `assets/`** — the jar's data
packs and its non-texture assets (models, blockstates, items, atlases, fonts,
particles, the post-effect chains and the shader tree), the fact base for
every data-driven claim; and **`reference/libs/`** — the Mojang libraries the
game depends on, staged by `tools/fetch_libs.sh` at the versions the game
pins: Brigadier and DataFixerUpper (MIT, published source jars) and authlib
(decompiled from Mojang's library jar, like the game). `verify_names.py`
checks library names at member level from those trees, so
`CommandDispatcher.execute` or `Codec.STRING` is verified, not allow-listed. A
fact-check agent reads them rather than taking a library's behaviour on trust.

Where the game is (26.3, from `python tools/map_source.py packages`; the
full tables are in `src/maps/`, regenerated on every deploy):

| package | classes | lines | |
|---|---:|---:|---|
| `world/level` | 1,418 | 151k | blocks, block states, chunks, lighting, world generation |
| `world/entity` | 727 | 111k | the entity hierarchy, AI, attributes, players |
| `client/gui` | 445 | 60k | screens, HUD |
| `client/renderer` + `client/model` | 983 | 63k | the frame, section meshing, entity models, render pipelines |
| `com/mojang/renderpearl` + `com/mojang/blaze3d` | 146 + 86 | 19k + 10k | the GPU abstraction: `renderpearl`'s `api` interfaces, `frontend` implementations and `opengl` **and `vulkan`** backends behind `GpuDevice`; `blaze3d` keeps the window, the frame graph, the vertex formats and `RenderSystem` |
| `world/item` + `world/inventory` | 387 | 38k | items, containers, data components |
| `network/protocol` | 298 | 13k | the packet catalogue (machinery in `network/`, `server/network`) |
| `server/level` | 42 | 12k | `ServerLevel`, `ChunkMap`, tickets — small package, huge classes |
| `server/commands` + `commands/*` | 235 | 27k | Brigadier, execution |
| `util/datafix` + `util/filefix` | 468 | 31k | save migration — **out of scope by rule 3** |
| `com/mojang/realmsclient` | 137 | 15k | Realms UI — out of scope |
| gametest, telemetry, profiling, jsonrpc, advancements… | ~1,000 | | one sentence each in *what this book skips* |

Naming drift a 1.21-era reader will trip on: `ResourceLocation` is now
`Identifier`; `Util` lives in `net.minecraft.util`; `LightTexture` is
`Lightmap`; `Timer` is `DeltaTracker`; `Gui` and `Hud` both exist. 26.3 adds
to the list: the GPU abstraction is `renderpearl`; the window and input layer
is SDL3, not GLFW; world generation's configured features, surface rules and
the `NOISE`, `SURFACE` and `CARVERS` chunk statuses are gone (`TERRAIN` does
their work; surface rules are `levelgen/material`); loot tables, predicates,
recipes and advancements are reloadable registries read by `RegistryDataLoader`;
`level/storage` is reworked; `ServerboundSwingPacket` is `ServerboundPunchPacket`
up and `ClientboundSwingAnimationPacket` down; `RedStoneWireBlock` is
`RedstoneWireBlock`; and `ItemInHandRenderer`, `ConfiguredFeature` and
`NameTagFeatureRenderer` are gone. Beside them, changes whose names survive,
so no gate sees them: density functions are compiled once per dimension
(`DensityFunctionCompiler`); improved transparency is order-independent and
drawn inside the main pass; the hurt cooldown is `LivingEntity.damageCooldownTime`
(`Entity.invulnerableTime` is now full invulnerability); the client's movement
leaves from `LocalPlayer.sendChanges`; and which side simulates an entity's
movement is its `MoveSimulationType`. The registry codecs (`RegistryFileCodec`,
`RegistryFixedCodec`, `HolderSetCodec`) only moved, to `core/registries/codec`.

## The page (`TEMPLATE.md`)

`TEMPLATE.md` is a **menu of shapes** (trace · pipeline · state machine ·
policy · comparison · vocabulary · pattern · landing page), written by
pass-3 session A from two pilots — `tickets-and-loading` (policy) and
`protocol-phases` (state machine) — with the devices, the budgets, the
mermaid rules and **the lane key** (rule 7). Pass 5's session A added the two
rules that are about the book rather than a page: **one home per mechanism**
(who owns a mechanism, what the other page keeps, and the citation form — a
parenthetical link carrying the owner's *anchor*) and **the landing page's
role** (the argument · the size · the shape · before you start · watch in
this order · where the part stops · the Reference it uses). Pass 6's session
A wrote in the devices that had become slots (the closer's one spelling and
its test, the 1.21 blockquote at the foot, the way into a scenario); pass 7's
rewrote *Figures* and *Lanes* to the figure standard (six lanes, the caption
as one italic run, no colour in a page, the marks table); pass 8's session A
added *Voice*, the wording rulings (state what is; a hedge names its
population; the book never calls a compile-time constant unread; one word, one
sense; sizes rot and populations do not), and amended the number device, the
blockquote's form and the caption (at most two sentences). What
every page keeps: the verified line with the part and scenario; an opening
paragraph that starts inside the scenario and ends on the hook (the
surprising true thing the page explains); a cast of at most eight classes
instead of field inventories; at least one figure, captioned; headings that
say what the section says, not which template slot it fills; *Where to look*;
the rules footer. Budgets: a list is at most seven items of at most two
sentences, at most three lists a page; anything explanatory is prose,
anything enumerative beyond seven is a table or a Reference page. Over the
102 system pages the shapes fell out as trace 31, vocabulary 25, pipeline 19,
comparison 11, policy 7, pattern 7, state machine 2.

## The plan

[docs/plan.md](docs/plan.md) — the eight passes, why they are in that order,
the rhythm every pass follows, the current pass's charter, the standing rules
for passes 5–8, the version pass, the owner's read, the risks, and the session
log from pass 8 on. **Read it first; tick it last.** Each finished pass is
archived whole (`docs/passN.md` for 1–4; `docs/passN-brief.md` Part 5 for
5–7) — still worth grepping: pass 2's fact-check protocol and lessons and pass
4's additions are what pass 8's agent brief descends from. **Pass 8's are
[docs/pass8-brief.md](docs/pass8-brief.md)** — Part 1 the charter, Part 2 the
agent brief, Part 3 the runbook, Part 4 the voice standard as session A ruled
it (the record, with the numbers), Part 5 the rulings, Part 6 the schedule
with the status column, Part 7 the charters it replaces — and its tools, each
with a `--probe` that proves it fails on the construct it should:
`tools/version_pass.py` (a release staged from Mojang's manifest, then
measured with `--check`, then `--flip`), `tools/mc_version.py` (the one
constant), `tools/pass8_queue.py` (the ledger routed by page, part and
session; `--unstruck` is the close's test), `tools/pass8_voice.py` (the tics,
hedges, terms and devices counted per page; `--terms` for the glossary's
two spellings), `tools/pass8_prompts.py` (one prompt per page for the
fact-check agent, one session file beside it) and `tools/pass8_diff.py`
(every sentence changed since the tag `pass-8-start`, for the second
reading). The two queues: [docs/pass9.md](docs/pass9.md) is the ledger every
session since pass 5 wrote the claims it introduced and the corrections it
made into, which pass 8 checks and strikes entry by entry (1,333 entries);
[docs/pass5.md](docs/pass5.md) is the queue passes 5–8 drew on by kind, which
pass 8 closes — every open unit settled or ruled *second edition* by its close.
[docs/pass3.md](docs/pass3.md) §7 is the coverage queue (a system with no
owner page) and seeds a second edition; it is the one queue that stays open.
The earlier passes' briefs and tools — `pass4_prompts.py`, `pass5_queue.py`,
`pass6_shape.py`, `pass7_figures.py`, `render_figures.js` — still run and are
what pass 8's tools import. `docs/outline.md` is the archived fourteen-lecture
map. The lecture order is drafted (`src/lectures.md`, with the
parts-dependency figure) and confirmed by the owner before the release.

## Site

mdBook 0.5 (`book.toml`, `src/SUMMARY.md`) with `mdbook-mermaid`; both are in
`~/.cargo/bin` (not on PATH in Git Bash). Layout: `src/introduction.md`;
`src/maps/` (the atlas: hand-written prose around the figures and tables
that `tools/map_source.py` writes into **`src/generated/`**, which is never
hand-edited and is regenerated by `deploy.sh` — the atlas tables and SVGs,
`parts.md`, the thirteen `part-<dir>.md` size phrases and the thirteen
`coverage-<dir>.md` phrases that `pass5_coverage.py --write` derives from the
same mapping; the figure pipeline —
`<figure class="map">` + `{{#include}}` + classes themed in `custom.css` —
is in `TEMPLATE.md` for any page that needs a figure mermaid cannot draw);
`src/systems/<part>/`
(the content; each part's `README.md` is its landing page, which is what
the folding sidebar opens on); `src/reference/` (the shelf: eleven views
generated by `tools/gen_reference.py`, two indexes by `verify_names.py
--index` and `check_lanes.py --index`, and the hand-kept catalogues and
look-up pages, which `verify_names.py` checks like any system page — its
README is the tier's landing page); `src/figures/` (a figure two pages share
through `{{#include}}` — today the parts-dependency graph, on the introduction
and `lectures.md`, an SVG `check_deps.py --write-figure` draws from the
landing pages into `src/generated/`); `src/lectures.md` (the lecture order
and the dependencies between parts); `src/robots.txt` (ships with the build;
points at the sitemap); `src/_headers` (serves the markdown twins as
`text/markdown`, cross-origin). `theme/head.hbs` is the only theme override —
Open Graph and Twitter-card meta on every page; `mermaid-init.js` is
committed and is **the figure theme** (not the file `mdbook-mermaid install`
writes, which must never be run over it). `custom.css` widens the column for
tables, diagrams and figures and caps prose at 800px; `diagram-zoom.js` opens
any diagram at viewport size on click; `site-footer.js` puts the licence and
the disclaimer on every page. Moved pages keep their URLs through
`[output.html.redirect]` in `book.toml`; `site-url = "/"` keeps the 404 page's
links absolute under nested paths. `tools/deploy.sh` regenerates the atlas,
the eleven Reference views, the coverage phrases and the dependency figure,
runs the six gates, builds, writes `llms-full.txt` (the whole corpus in one
file, `tools/llms_full.py`) and `sitemap.xml` + `llms.txt` (the index form,
`tools/site_index.py`), **publishes every page's markdown twin** beside its
HTML (`tools/md_twins.py`; `llms.txt` links them), **rewrites every built
`<head>`** (`tools/page_meta.py`: the page's own title and part, a description
from its scenario line, a canonical at the clean URL, the markdown alternate,
Open Graph with `src/og.png` from `tools/og_image.py`, JSON-LD; it fails the
deploy if any page lacks a canonical or shares a description), and deploys to
Cloudflare Pages project `minecraftdocs` (https://minecraftdocs.pages.dev,
custom domain **minecraftdocs.dev**, a full Cloudflare zone with DNS done)
using the token at `~/.cloudflare/pvpmod.token` — stored wrapped in quotes,
which `deploy.sh` strips. The token edits Pages and reads the zone; it cannot
touch Web Analytics or AI Crawl Control, which are the owner's clicks.
`tools/check_mermaid.js` needs node and a one-time `npm install` in `tools/`
(see its header comment). A reader's correction arrives as a GitHub issue
through `.github/ISSUE_TEMPLATE/correction.yml`, which asks for the decompile
location that shows the claim false.

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
- `verify_names.py`, `check_mermaid.js`, `check_lanes.py --strict`,
  `check_figure_names.py --strict` and `check_links.py` before every commit
  that touches a page, and `check_deps.py` when a landing page, `SUMMARY.md`,
  `lectures.md` or the dependency figure changes; `deploy.sh` runs all six —
  after regenerating the atlas and the eleven Reference views — and refuses
  to publish on a failure.
- A landing page states a size only where size is part of its argument, and
  then from `{{#include ../../generated/part-<dir>.md}}`, which the atlas
  writes from `map_source.py`'s `PARTS` mapping (the same mapping
  `pass5_coverage.py` reads), and a coverage number likewise from
  `{{#include ../../generated/coverage-<dir>.md}}`; no landing page hand-counts.
  The order in *watch in this order* is the book's: `SUMMARY.md` and
  `lectures.md` follow it, and `check_deps.py` fails when the three disagree.
- A published page never names a pass number as a promise about the
  future; when a pass closes, grep `README.md`, this file, `TEMPLATE.md`
  and the frame pages for the old numbers.
- Commit your own files by name, never `add -A`: two sessions are often
  open at once and pass sessions sweep the tree.
- A script with a backslash in it is written with the Write tool and run
  from a file; this machine's Bash heredocs eat one level of escaping.
