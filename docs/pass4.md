# Pass 4 — the second fact-check (queue; opened 2026-09-02)

*Pass 4 re-runs pass 2's adversarial protocol — archived in
[pass2.md](pass2.md) with its twelve lessons — over the corpus pass 3
rewrote. This file is where pass-3 sessions write down what pass 4 must
check hardest: every page rewritten, every claim a rewrite introduced (a
hook, a redrawn ordering, a new section, a landing page's dependency list),
every diagram redrawn. Pass 4 checks everything anyway; this list decides
what it checks first. The charter is written by pass 3's closing session
(P) into [plan.md](plan.md).*

## How to write an entry

Per session: the pages rewritten; per page, the claims introduced (one line
each, quoting the sentence); the diagrams redrawn (which orderings they
assert); anything an agent drafted that the old page did not say. Newest
entry first.

## Standing items

- The landing pages and `lectures.md` are claims about order and
  dependency: check that every *before you start* link is actually assumed
  by the part, and that nothing earlier depends on something later.
- Every redrawn diagram: arrow by arrow, and every tick-boundary bar.
- The generated Reference views pass 3 adds (serializers, attributes, the
  glossary if generated): re-derive one sample by hand per view — pass 2
  found bugs in both generators, and one had reached the prose.
- The lane key in `TEMPLATE.md`: every lane's expansion is a class that
  exists. (If session A writes a lane linter, strike this.)
- Pass 2's twelve lessons apply unchanged; the shape to watch remains the
  confident sentence — orderings, "only", "never", counts, and "X, not Y".
- **Library facts are checkable now and were not in pass 2.**
  `reference/libs/` holds Brigadier, DataFixerUpper and authlib sources
  (`tools/fetch_libs.sh`) and `reference/26.2/assets/` the atlas, font,
  shader and post-effect JSON. Pass 2 took every claim about them on trust;
  pass 4 re-derives them, hardest on: `codecs-nbt-json` (DFU semantics —
  `DataResult` partials, `MapCodec`, `Lifecycle`), `protocol-phases` and
  `players-and-sessions` (authlib's session-server round trip),
  `chat-and-signing` (profile keys and signature validation),
  `brigadier-and-commands`, `execution-and-functions` and
  `scoreboard-and-data` (parse, suggestions, `ContextChain`, the result
  consumer), `models-and-atlases` and `text-and-fonts` (the atlas and font
  JSON), and whatever pass 3 writes about post-processing.
- **The `execute store` question** on `scoreboard-and-data` — what a failing
  ordinary leaf command writes — is now answerable from Brigadier 1.3.10;
  settle it and remove the page's "cannot be settled from the decompile"
  note.

## Entries

- **2026-09-02, session A (the frame)** — two pilot pages rewritten in new
  shapes, the introduction and Part I's landing page written, the lane key
  seeded. The standing item on the lane key is discharged:
  `tools/check_lanes.py` verifies every key expansion against the decompile
  and runs in `deploy.sh`.
  - **`tickets-and-loading`** (policy shape). *Corrected from pass 2:* the
    keep-dimension-active flag (`TicketType.FLAG_KEEP_DIMENSION_ACTIVE`, 8)
    is on `PLAYER_SIMULATION` (flags 12), `FORCED` (15), `PORTAL` (15) and
    `ENDER_PEARL` (14) — **not** on `PLAYER_LOADING` (2); the old invariant
    "a player-loading ticket keeps the dimension alive" was wrong and the
    table gained a column. Claims introduced: the hook ("a chunk can be
    `ENTITY_TICKING` by every measure the holder knows and tick nothing");
    "timed and `canExpireIfUnloaded` — only `UNKNOWN`" (flags 18 is the only
    one carrying 16); "the four in flight are the four nearest" (inferred
    from priority = distance in `PlayerTicketTracker.onLevelChange` — check
    the dispatcher really orders by that priority); "loading floods in
    Chebyshev rings — every ring is a square"; "a spectator under
    `SPECTATORS_GENERATE_CHUNKS` false is still sent chunks that exist but
    places no tickets" (read from `ChunkMap.updatePlayerStatus`: ignored
    players skip `DistanceManager.addPlayer` but still get
    `updateChunkTracking`). Diagrams redrawn: the flowchart asserts holders
    exist at ≤ 44, futures arm at 33/32/31, and the simulation graph feeds
    only the range questions; the `FullChunkStatus` state diagram asserts
    promotion waits for future success and demotion is immediate (read from
    `ChunkHolder.updateFutures`/`demoteFullChunk`), entry at ≤ 44, exit past
    44 via `toDrop` → `processUnloads`; the six-lane trace asserts the order
    spawn counter → simulation tracker → player ticket tracker → loading
    tracker → two passes over `chunksToUpdateFutures` (read from
    `DistanceManager.runAllUpdates`) and that the crescents are marked
    before `runAllUpdates`. The two decision tables restate pass-2 facts;
    check each row's gate column as an "only" claim.
  - **`protocol-phases`** (state-machine shape). Claims introduced: the
    five-phase diagram — `STATUS` is a dead end, `PLAY` ⇄ `CONFIGURATION`,
    "every transition packet is terminal" (the seven `isTerminal`
    overrides are exactly the seven transition packets: intention, login
    finished, login acknowledged, finish configuration ×2, start
    configuration, configuration acknowledged); the login state diagram —
    `HELLO → KEY` only for online mode over a socket, `HELLO → VERIFYING`
    for the singleplayer profile or offline mode, `KEY → AUTHENTICATING` on
    the key packet, `AUTHENTICATING → VERIFYING` from the thread,
    `VERIFYING → WAITING_FOR_DUPE_DISCONNECT | PROTOCOL_SWITCHING` and
    `WAITING → PROTOCOL_SWITCHING` in `tick`, `PROTOCOL_SWITCHING →
    ACCEPTED` on the acknowledgement, `NEGOTIATING` never assigned (all read
    from the state assignments this session); the three-lane handshake
    sequence (joinServer before the key packet; ciphers attached to the
    send; the server installs ciphers before its own session call); the
    configuration flowchart (registries → code of conduct → resource pack →
    prepare spawn → join world; the finish handler does outbound play, the
    duplicate check, `canPlayerLogin`, then `spawnPlayer` — read from
    `handleConfigurationFinished`); the two "what disconnects a …"
    paragraphs are new syntheses of old facts; "the first
    `PacketUtils.ensureRunningOnSameThread` in a connection's life is in
    configuration" is borrowed from `anatomy`. The three client entry
    points sentence is the old *Called by* bullet, kept.
  - **`introduction`** (new): "just under a third client-only" (2,206 of
    7,055, from `maps/packages.md` and `server-classes.txt`); "0 to 10
    ticks inside a frame" (from `the-frame`); the two-programs figure
    asserts that workers feed both levels.
  - **`systems/anatomy/README.md`** (new, landing page): the root figure is
    a claim about which thread each part starts from — check as an ordering
    claim. **`lectures.md`**: Part I's two entries and the two known
    cross-part dependencies (from the pass-3 notebook).

- **2026-09-02, planning session** — the mermaid syntax fixes were
  syntax-only (labels reworded around `;` and `#`, see the commit diff); no
  claim changed. Nothing to check beyond a glance at that diff.

- **2026-09-02, session B — maps: the atlas.** The atlas is new prose over
  regenerated numbers, and the tool that makes the numbers changed; check
  the tool first, then the prose against a fresh run.
  - **`tools/map_source.py`** (rewritten): the declaration regex now matches
    indented (nested) declarations and record headers, which the old one
    silently did not — every hierarchy count changed (`Entity` 188 → 193,
    `Goal` 70 → 200, `Screen` 153 → 157, `Packet` unlisted → 232), and a
    simple name declared twice now resolves to the top-level class (a nested
    `Block` in blaze3d had claimed the name). Fan-in now counts every
    `com.mojang` import, so `Codec`, `MapCodec`, `RecordCodecBuilder`,
    `Schema`, `DSL` and *LogUtils* appear. Re-derive one number of each
    kind by hand (a package's line count, one class's importers, one root's
    descendants) before trusting the rest.
  - **`maps/packages.md`**: 2,206 client-only classes in exactly four
    packages and no mixed depth-4 package (read off the table's client-only
    column: every row is 0 or all); 212,242 client-only lines = 29.5%;
    `world/level` a fifth of the game; two thirds of `util` skipped (34,176
    of 53,275); Vulkan back-end larger than OpenGL; the **part → packages
    table** is a claim about where each part's classes live and should be
    checked per part as the parts convert (`server/dialog` and
    `world/level/pathfinder` are guesses from package names, not from
    pages); the `SKIPPED` list in the tool must agree with *what this book
    skips* (gametest is deliberately not hatched: covered in Part XIII).
  - **`maps/biggest.md`**: `BlockModelGenerators`' only caller is
    `ModelProvider` (one grep hit); nothing outside `util/datafix` reads
    `BlockStateData` (seven files, all datafix); the sum 62,935 = 8.7%;
    "`Fox` and `Bee`, the two with the most bespoke behaviour" is a
    judgement stated as fact — verify or soften; "`Options` is every
    setting" and "`Hud` is everything drawn over the world" are glosses;
    `OceanMonumentPieces` and `StrongholdPieces` "built by hand in Java
    rather than a template" rests on `hand-built-structures`.
  - **`maps/fanin.md`**: one file in six (1,221 of 7,055); all but ten
    `Schema` importers in `util/datafix` (389, 10 outside); `Minecraft`
    twenty-ninth and the only client-only class in the thirty; the hub →
    page table sends `Component` to "Part II", which has no page until
    session C writes one (R6) — fix the link then; "same-package use is
    not counted" is Java, not a claim about the game.
  - **`maps/hierarchy.md`**: `FeatureElement`'s seven implementers
    (grep-verified: `BlockBehaviour`, `Item`, `EntityType`, `MenuType`,
    `MobEffect`, `Potion`, `GameRule`); `ItemLike` = `Block` + `Item`; the
    per-tree numbers (193/18, 124, 114, 108, thirteen terminal; 293/92, 61
    terminal, 64; 71/51; 157/72, 60 terminal, 27, 23); "over a thousand
    registered items" (1,130 `registerItem`/`registerBlock` lines in
    `Items`, a few of them definitions); "`Items` registers most of the
    game as a plain `Item`" is asserted, not counted; "`BlockBehaviour`
    exists so that behaviour and registry identity can be separate
    classes" is a motive, not a fact — check or cut; `Goal` 130 of 200
    nested; `Packet` 227 direct implementers versus the packets reference's
    count (packet *types* and packet *classes* differ; say which).
  - **`reference/threads.md`** (new figure): every edge asserts a
    direction and a kind (posted task / completed future / hopped handler)
    — "serverbound packets written on the caller's thread", region I/O as
    posted task and completed future through `IOWorker`, sound as posted
    tasks to `SoundEngineExecutor`, console/RCON/query/management as
    posted command lines; all drawn from the page's own table, none
    re-verified against the decompile this session.
  - **`introduction`**: the treemap's hatching is the tool's `SKIPPED`
    list; the "just under a third" now has its figure.
  - **`entities/entity-anatomy.md`**: "193 descendants" (was 188, from
    the old map that could not see nested classes); re-derive with the new
    tool and by hand once.
