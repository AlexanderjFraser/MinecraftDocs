# Pass 5 — polish (queue; opened 2026-09-02)

*Pass 5 is the wording pass — voice, consistency, cuts. Its inputs: the
on-spec material and wording debt every pass-2 session logged in
[pass2.md](pass2.md)'s hand-off section (written when polish was still
numbered pass 4 — read "pass 4" there as pass 5), and what passes 3 and 4
append here: cuts pass 3 made and why, material it moved, wording it left
rough on purpose because the shape mattered more, and the tics it noticed.
Nothing here is acted on before pass 4 has checked the page.*

## Standing items

- The "not X but Y" construction — pass 2's most common register error,
  Part XIII its worst offender.
- The named-qualifier hedge ("with two exceptions", "five of the seven") —
  right precision, repetitive phrasing.
- One voice sweep against the best page, chosen in pass 5's first session.
- The glossary as the terminology checklist.

## Entries

## Session N — the corpus-wide count sweep (pass 4) *(2026-09-05)*

The sweep's job was numbers, and what it turned up beside them is one tic with
many faces: **a count that is right under one reading of its population and
wrong under another, with the page never saying which**. None of these is a
wrong number, so none was fixed. Pass 5 should pick the reading, say it, or
drop the number.

**A count of one thing described as a count of another.**

- `blocks/blocks-and-states.md:25` — "through **fifty-eight** statics — the
  drops, the particles and the shape-update helpers". 58 is every `static`
  declaration in `Block.java` (23 fields, 34 methods, one nested record); the
  things listed are static *methods*, of which there are 34. And "the
  particles" is `Block.spawnDestroyParticles`, a `protected` **instance**
  method.
- `client/hud.md` — the heading is now *Four states*, and three of the four
  draw. If pass 5 wants "bars" back, the number is three.
- `world/scheduled-ticks.md:81` — "**Two** type parameters" is right for the
  two type *arguments* in play (`Block`, `Fluid`); every class involved
  (`LevelTicks`, `LevelTickAccess`, `LevelChunkTicks`, `ScheduledTick`)
  declares exactly one.
- `world/chunk-storage.md:281` — "it changes hands **four** times" names four
  stages but only three thread changes: `ChunkSerializer.upgradeChunk` and
  `ChunkSerializer.parseChunk` are both on `Util.backgroundExecutor`.
- `player/README.md:32,63` — "**eight** classes" is the cast table's eight
  *rows*, which name nine classes (one row holds `ServerPlayerGameMode` /
  `MultiPlayerGameMode`).
- `networking/README.md:35` — "the two the part spends longest on" names
  *what the client is told* and *chat and signing*; by line count the two
  longest are `what-the-client-is-told` (474) and `packets-and-stream-codecs`
  (465), and `chat-and-signing` (326) is the shortest page in the part.

**A superlative that is true only of the sub-population the page stands in.**

- `world/chunk-storage.md:323` — "which **only** `ImposterProtoChunk.markUnsaved`
  does" is true among the saving flags; `ImposterProtoChunk.setLightCorrect`
  delegates unconditionally too, which `chunk-anatomy:102` says itself.
- `client/text-and-fonts.md:184` — "the one place in the pipeline where a
  character is invented" is true of the wrap path;
  `ComponentRenderUtils.clipText` in the same class appends
  `CommonComponents.ELLIPSIS`.
- `world/points-of-interest.md:124` — "**a dozen** shapes" of read-only query
  is 13 method names / 14 methods. The hedge covers it; *thirteen* reads better.
- `entities/ai-goals-and-brains.md:381,390` — "everything it will ever do" /
  "the twelve": a door-breaking `Zombie` gains a thirteenth goal at
  `Zombie.java:158`, outside `Mob.registerGoals`.
- `entities/authority.md:181` — "three of those eight read the same member"
  holds for `Entity.canSimulateMovement` (3);
  `Entity.isLocalInstanceAuthoritative` is read at four of the eight.
- `world/README.md:79` — "the one page here that depends on nothing else in
  the part" is one under *off the conveyor chain*; the part's own figure gives
  two pages no inbound edge (`chunk-anatomy` and
  `environment-attributes-and-timelines`).
- `world/chunk-storage.md:203` — "**Three** places do make the server thread
  wait on a disk": a fourth blocking join at `ServerChunkCache.java:126`/`149`
  can end at the disk, though it drives the main-thread queue rather than
  raw-joining the IO lane.
- `client/the-client-level.md:129` — "the chunk cache and **one** packet
  handler call `LevelExtractor` directly" is right for the dirty-marking path;
  three `ClientPacketListener` sites touch `levelExtractor` in all.
- `foundations/identifiers-and-registries.md:75` — "keyed **three** ways"
  names three maps; `MappedRegistry.byValue` is a fourth index.
- `foundations/codecs-nbt-json.md:259` — "**two** fields" is true of the
  `IOWorker` case cited; `StructureCheck`, in the same sentence, uses three.
- `blocks/signal-and-dust.md:27,126` — "the three answers a state gives" is
  three of six signal delegators on `BlockBehaviour.BlockStateBase`; "All three
  stop early" is true of the reading methods and false of the direction arrays
  the previous paragraph counts.
- `reference/math-and-primitives.md:116` — "two things called `Axis`" is two
  in scope; there is a third in the datafix tree, which rule 3 excludes.
- `items/loot-tables.md:130` — "a funnel with **three** fan-outs" describes the
  page's own figure, which has four branch nodes.

- `maps/biggest.md:29` — "only **two** concrete mobs make the list" is true of
  the figure's thirty and false of the table's forty (`Panda` 37th,
  `SulfurCube` 40th).
- `maps/fanin.md:24` — "the **thirty** hubs … they are **seven**" has the right
  seven idea rows, but the table's class list is 32 classes, only 24 of them in
  the thirty; six of the thirty appear in no row.
- `lectures.md:220` — "**Two** components on one item" is the two *weapon*
  components; `the-spear`'s own cast lists eight `DataComponents` on it.
- `lectures.md:228` — "**four** languages" is four in a login trace;
  `ConnectionProtocol` has five values and the page's own section is
  *The five phases*.

- `rendering/post-processing.md:204` — "every chain this game will ever load is
  named by a **constant** in Java, and there are only six of those". Six ids is
  right; only three are `static final` fields
  (`GameRenderer.BLUR_POST_CHAIN_ID`,
  `LevelRenderer.ENTITY_OUTLINE_POST_CHAIN_ID`,
  `LevelRenderer.TRANSPARENCY_POST_CHAIN_ID`) and the other three are inline
  literals in `GameRenderer.checkEntityPostEffect`'s switch. The count holds;
  *constant* does not.
- `rendering/the-window.md:244` — "(**both** reached from `KeyboardHandler`)".
  `ClipboardManager` is a `KeyboardHandler` field; `TextInputManager` is
  `Minecraft.textInputManager` and is reached from `Gui`,
  `AbstractSignEditScreen` and `IMEPreeditOverlay` as well.
- `rendering/entity-rendering.md:189,255` — "half" and "4x4" are right but the
  enumeration is short (`SubmitNodeCollector.submitMovingBlock` also copies only
  the `Matrix4f`; `submitFlame`, `submitShapeOutline` and `submitCustomGeometry`
  also copy the full pose); and "half a dozen others" is seven layers that hang
  something off a posed part, thirteen that call `RenderLayer.getParentModel`
  at all.
- `rendering/models-and-atlases.md:191` — "**twelve** separate layers" of
  fallback: the prose names eleven distinct failure kinds, and twelve only if
  "bakes that throw" counts as its two `ModelBakery` catches.
- `rendering/lightmap-fog-and-sky.md:60` — "a fifth of the way" is `0.22F`
  (`ClientLevel.java:274`), stated as a fraction rather than hedged.

- `commands/functions-and-macros.md:158` — "**three** lines apart" is three
  lines *between* the two declarations (`CommandSourceStack.java` 124 and 128),
  a delta of four.
- `commands/scoreboard-and-data.md:215` — `Player.canHarmPlayer` "**six** call
  sites" is six counting `ServerPlayer`'s own `super.canHarmPlayer`, five
  counting external callers.
- `commands/scoreboard-and-data.md:230` — death-message visibility has "a
  **single** reader" in the behavioural sense (`ServerPlayer.die`, which calls
  the getter three times), plus `TeamCommand`'s unchanged-check: four call
  sites in all.
- `commands/scoreboard-and-data.md:245` — "All **five** go through
  `PlayerList.broadcastAll`" is true of all five, and three of them also ship
  through explicit per-player loops
  (`ServerScoreboard.startTrackingObjective` / `stopTrackingObjective`,
  `PlayerList.updateEntireScoreboard`).
- `commands/permissions.md:224` — "only **one** of those checks is a constant
  the server itself uses" is one under *shared `PermissionCheck` constant*, two
  if `Permissions.COMMANDS_GAMEMASTER` counts, which the server reads inside
  `Commands.LEVEL_GAMEMASTERS`.
- `commands/scoreboard-and-data.md:371` — "the nicest **ten** lines" is not
  verifiable at that precision; decompiled formatting is not the source's.

**Two same-page phrasings of one constant.** `world/points-of-interest.md:235`
says "more than twenty ticks have passed" and
`entities/ai-goals-and-brains.md:335` says "fewer than 21 ticks have passed"
for the same test, `Brain.java:389` (`gameTime - lastScheduleUpdate > 20L`).
Both are true; one wording should win.

**A claim a decompile cannot settle, corpus-wide.** `javac` inlines primitive
`static final` constants at their use sites, so **"declared and never read" is
unverifiable of any primitive constant** — `Channel.attachBufferStream` writes
bare `1` and `4` where the source wrote its two named constants. Session D's
ruling (a dead constant is kept and *said to be dead*) needs the weaker wording
*no reader survives the decompile*. Known instances:
`client/the-client-loop.md:87`, `SoundEngine.MIN_SOURCE_LIFETIME`,
`ClientLevel.NORMAL_LIGHT_UPDATES_PER_FRAME`,
`ClientExplosionTracker.MAX_PARTICLES_PER_TICK`, and
`SharedConstants.TICKS_PER_SECOND` / `SharedConstants.MILLIS_PER_TICK`, which
`anatomy.md:266`'s *Is twenty ticks a second a constant?* answers "no, it is a
server field" without mentioning that both are declared at
`SharedConstants.java:149-150` and that nothing in the tree reads either.

**Hedges that came back a little short.** `client/options.md:80` "a dozen
others" is ten under the enumeration available;
`client/the-gui-render-tree.md:179` "the layering rule is thirty lines" is 27
or 52 depending on the grouping, and decompiled formatting is not the source's;
`player/status-effects.md:150` "divides by about four" is exactly 3.75;
`player/the-spear.md:46` "the one item that lets you run while using it" is one
`Item.Properties.spear` builder across seven items;
`player/player-anatomy.md:3` "five classes deep" is five on the server chain and
six on the client chain the page's own scenario is in;
`player/hunger-and-experience.md:23` lists the enchanting seed twice — it *is*
one of the four experience fields, which `player-anatomy.md:243` words correctly;
`entities/entity-lifecycle.md:131` "the **four** constants that are not the
numbers" is four if `NaturalSpawner.MAGIC_NUMBER` is excluded, five if not;
`entities/entity-anatomy.md:5` "`DefaultedMappedRegistry` overrides **nine**
lookups to hand it back" is nine overrides, six of which hand the default back;
`world/chunk-generation-pipeline.md:211` "passes **seven** of the twelve steps
straight through" is eight literal pass-throughs in `ChunkPyramid`, and seven
only because `ChunkMap.applyStep` turns `ChunkStatus.EMPTY` into the disk read —
which the same page states at :388;
`blocks/block-interaction.md:182` "three outcomes" is three distinct returned
states and four branches;
`blocks/block-entities.md:107` "four steps" of `LevelChunk.removeBlockEntity`
is four *named* steps over five statements.

**Two rules for the word *classes*, corpus-wide.** A package's class count is
one number under two rules — `package-info.java` counted, or not — and the
corpus uses both without always saying which. `anatomy/what-this-book-skips.md`
states the split it uses (tables count files, prose counts classes) and is the
only page that does. Part XIII follows the same split by accident:
`commands/game-tests.md:38` "forty-four classes" and
`commands/permissions.md:33` "eleven classes and 398 lines" exclude the marker
(the atlas says 45 and 12 / 402), while
`commands/scoreboard-and-data.md:52` "sixteen **files** and 1,442 lines"
includes both markers and matches the atlas exactly. But
`worldgen/README.md:27` says **451 classes** and explicitly adopts the atlas
rule ("one class per file … the way the atlas counts everything else"), so
*classes* means the opposite there. Session A logged this as "two size claims,
two rules"; session L settled the Part XII half by adopting the atlas rule; the
corpus still has both. **Pass 5 (or session O) should pick one and say it once**
— the natural rule is the one `what-this-book-skips` already states.

**One editorial number worth a look.**
`world/environment-attributes-and-timelines.md:5` opens on "at tick 12542 … the
sun goes under". 12542 is a real keyframe (*monsters_burn*,
*bees_stay_in_hive*), but the geometric horizon crossing the page's own
sun-angle Bézier implies is ~12782, and sunrise ~23218 against the 23460
keyframe. The gameplay flip is about 240 ticks inside the geometric day at each
end — a better sentence than the one there, if pass 5 wants it.


## Session L — Part XII World generation (pass 4) *(2026-09-05)*

**Hooks and openings rewritten around a corrected fact — re-read all of these
for voice.** Seven were rewritten because the fact under them fell:

- `worldgen/README.md`'s **opening paragraph**, which now carries a
  three-clause qualification ("not because nothing here reads the world … but
  because everything it reads is itself a function of that seed and those
  packs"). It is accurate and it is the longest sentence on the page. The
  premise deserves a shorter shape.
- `jigsaw-and-templates`' **opening**, whose lamp post is gone and whose
  mechanism now needs four sentences where the false version needed two. The
  clause "What the depth limit does is stop offering the asked-for pool at
  all" is doing a lot of work in one line.
- `trees`' **crown paragraph**, which now ends on "the asymmetry is in the
  code and vanilla data cannot express it" — true, and a stranger note to end
  a section on than the section was written for. Its header line
  ("a ceiling the crown's size was decided before") is grammatically awkward
  and was chosen for accuracy, not sound; so were the two blurbs that repeat
  it in `worldgen/README.md` and `lectures.md`.
- `structure-placement`'s **verified line** and its *Whether it is worth
  laying out* section, which now explain a deferral that lasts one statement.
  The section's title still promises a decision the section no longer
  describes.
- `density-functions`' **opening**, which now names two files where it named
  one, and loses some of the "small, honest, readable" rhythm it had.
- `biomes`' **world-spawn answer**, which went from two sentences to five and
  is now the longest *Questions players ask* answer on the page.
- `creating-a-world`'s **hook**, whose "every widget is an edit to it" became
  a clause plus an exception list. The exception list is the kind of
  named-qualifier hedge this pass is meant to hunt.

**Structural findings, not acted on.**

- `worldgen/README.md`'s *Watch in this order* closer now carries three
  separate order rulings (two before three, four reaching forward into five
  and six's status, seven before eight and nine) where it used to carry a
  clean pair. It reads as a list of caveats rather than an instruction.
- `blending`'s **first figure gained a dashed annotation node** to say that
  two of the five consumers never touch the two maps. That is prose smuggled
  into a flowchart, and the page's own text says the same thing thirty lines
  below. One of the two should go.
- `features-and-placement`'s *A feature that is a tree of features* section is
  now about six features of which one is unrelated to the section's subject
  (`Feature.NO_OP` writes nothing but is not a selector). The count and the
  subject want separating.
- `hand-built-structures`' `StructurePiece.placeBlock` cast row is now three
  clauses long and contains a negation ("not a choke point"), which is the
  *not X but Y* tic in a table cell.
- **The *Questions players ask* closer** is on nine of the eleven Part XII
  pages, well over session P's at-most-half rule of thumb. `terrain`,
  `biomes` and `structure-placement` have five, five and six answers each.

**Wording debt of the session's own making.** Several fixes name a file path
or a JSON key in italics where the surrounding prose uses backticks for
everything else (*terrain_adaptation*, *use_expansion_hack*,
*skip_existing_chunks*, *min_clipped_height*, *blending_data*). The convention
is right — `verify_names.py` rejects them backticked — but the mixture inside
one paragraph reads unevenly, and a corpus-wide look at how data keys are
typeset is worth one pass-5 sweep.


## Session K — Part XI Rendering (pass 4) *(2026-09-04)*

**Hooks and openings rewritten around a corrected fact — re-read all of
these for voice.** Six paragraphs were rewritten because the fact under them
fell, and none has had a wording pass:

- `the-frame`'s acquire-failure paragraph and its minimize Q&A (the answer
  went from "three calls' worth" to a paragraph about the ten-frame limiter,
  and it is now the longest Q&A on the page).
- `the-frame`'s partial-tick table gained a sixth row and lost the "five
  partial ticks" heading; the section is now called *six clocks in one frame*,
  which is accurate and may not be the best title.
- `models-and-atlases`' chunk-layer hook, which now carries a nine-line
  qualifier about `force_translucent` where the point is one sentence long.
  **This is the clearest over-long fix in the session.**
- `models-and-atlases`' water-animation Q&A, whose *question* changed — it
  now asks two things at once ("why does lag slow it but the pause menu not
  stop it"), which is a compound question in a slot that wants a simple one.
- `lightmap-fog-and-sky`'s opening, where "only two still read the raw world
  clock" became "only one… and the weather does not ask anybody". The new
  clause is true and the rhythm of the sentence is worse.
- `visibility-and-the-frame-graph`'s opening, which no longer resolves to one
  method and now has to say "not quite at one method" — an admission in a
  position that wants a promise.

**Structural findings (not acted on).**

- `the-window`'s seventh callback (the window-close one) is introduced in a
  section titled *Six callbacks are the entire surface* and then explained
  three sections later, under the shutdown watchdog. Either the heading or the
  ordering is wrong; pass 5 should decide which. Same page: the "rest of the
  package" list omits seven of the package's twenty-six classes, including
  `Transparency` and `TextureUtil`, and the error callback is swapped at least
  four times where the page implies two.
- `block-entity-rendering`'s completeness sweep — the page had never been
  checked, and nineteen in-scope classes and mechanisms go unmentioned. The
  ones worth a sentence each, in the agent's priority order:
  `BlockEntityRendererProvider.Context`, `WallAndGroundTransformations`,
  `BlockModelRenderState`, the crumbling-overlay source, and
  `BlockEntityWithBoundingBoxRenderer`'s game-master permission gate. Also
  unmentioned: `END_GATEWAY` and `COPPER_GOLEM_STATUE` in the built-in special
  list, the `EmptyBlockModel`/`SelectBlockModel` entries in the same table, and
  the five blocks that get a bare wrapper rather than a composite — which is
  why a block-displayed enchanting table is a book with no table under it.
- `entity-rendering` and `reference/submit-phases.md` overlap more than they
  should now that the catalogue is corrected: the lecture names four of the
  fifteen phases and exactly one of the thirteen renderers, so the "three or
  four examples from" framing the Reference page used was already generous.
  Pass 5 should decide whether the lecture wants more of the catalogue or the
  catalogue wants less of a preamble.
- `post-processing`'s per-chain table has a *what a player sees* column that
  is interpretation of GLSL the book does not quote. It survived the
  fact-check because it is not falsifiable from the sources the book uses.
  Pass 5 should decide whether to keep it, and if so to say in the caption
  that it is a reading rather than a citation.
- The landing page's pipeline figure no longer claims to be frame order, and
  the paragraph under it now spends four lines saying what the arrows are
  *not*. That is honest and it is also the longest caption in the part.

**Smaller misleading items, verified but left as they are** (each is true as
written and imprecise in a way that costs a reader nothing at this pass):
`the-frame`'s "all of this is one thread" against a client that has several;
`models-and-atlases`' "twelve separate layers" where the prose enumerates
eleven and the code has more, and its "at different coordinates" for a
same-size sprite replacement that `Stitcher` puts back in the same place;
`blaze3d`'s "applied when the pipeline is bound", its "downgrades twice" for
an if/else-if, and "every drawing class comes through this one shape" naming
two classes that never open a pass; `particles`' "one particle escapes this
system entirely", where only the *draw* escapes; `section-meshing`'s
start-up-only OOM shrink offered as the runtime answer to buffer exhaustion,
and its `hasAllNeighbors` rationale, which explains four cardinal columns
where the check demands eight plus a light test; `visibility`'s walk-trigger
list, which omits `LevelRenderer.resize` and `ViewArea.repositionCamera`;
`block-entity-rendering`'s "the two gates every extraction passes", where
there is a third at `BlockEntityRenderDispatcher.java:67`, and its "nothing
reaches back into the world", which `SignRenderState`'s live `SignText`
references break.

**On-spec material pass 5 may cut**, carried forward from pass 2's session I
and still true after this pass: `the-window` in its entirety (it is a real
gap and a real lecture, and it is also the page a viewer is most likely to
skip — the landing page now says so in as many words); `blaze3d`'s *What
replaced RenderStateShard* and *Resources and uniforms* sections, both of
which are naming-drift work rather than a lecture's; `particles`' explosion
section, a second trace on a page that already has one; and
`entity-rendering`'s thirteen-renderer and fifteen-phase lists, which now
duplicate a Reference page that has been checked row by row.

## Session J — Part X The client (pass 4) *(2026-09-04)*

### Wording to re-read (a fact fix rewrote the sentence around it)

- **`the-client-loop`'s opening paragraph.** "The server never does this. It
  runs late; the client runs *short*" was a clean two-clause contrast and it
  was false. The replacement — the server drops ticks too, but only past the
  overload threshold and never quietly — is three clauses longer and buries
  the punchline ("and says nothing") at the end. The *fact* is now right; the
  sentence is the flabbiest thing on the shortest-feeling page in the part.
  Worth a second look for a shorter true contrast.
- **`input-and-keybinds`' opening paragraph.** "None of that involves the
  tick. All of it has already happened before the tick that observes it runs"
  became a qualified version that has to concede the inventory case mid-hook.
  The concession is the more interesting fact — the drain is inside the tick —
  and pass 5 might be better off building the hook *on* it rather than
  apologising for it.
- **`gui-and-screens`' hook and verified line.** Both now carry "until you
  close it". The page's title promise (a screen the server is never told
  about) survives only for the opening, and the new last sentence — "the
  screen the server is never told about is one the server is told about
  exactly once, at the end" — is a good line that arrives after two
  qualifications. Consider leading with the asymmetry.
- **`what-makes-a-sound`'s third door.** The old paragraph was one mechanism
  stated confidently and wrongly; the new one states the mechanism *and* its
  exception (attack sounds do round trip) in the same breath, which makes the
  "three doors" framing land more slowly. The verified line still promises
  three doors and only one naming the sound, which is still true.
- **`prediction-and-acks`' state-diagram labels.** Both client exits were
  relabelled and are now long enough to crowd the figure — "endPredictionsUpTo(n),
  syncBlockState writes the absorbed state, which is a no-op if it is already
  on screen" is a sentence, not a label. The *diagram* is now true; it is also
  now the wordiest figure in Part X. Same page: the hook lost "in the same
  tick" and gained a because-clause.
- **`the-client-level`'s two weather Q&As.** "Why does thunder arrive late?"
  and "Why does rain stop and start so abruptly?" were both questions whose
  premises the code denies, so both became questions with different subjects
  ("Does the client model the speed of sound?", "Who decides how hard it is
  raining?"). Neither is a question a player actually asks, which is what the
  section is for — pass 5 should either find the player-facing version or move
  the material into the body.
- **The landing page's opening sentence** now spends a clause and two class
  names on the scheduler exception before reaching "no render thread", which
  is the sentence people will quote. Consider a footnote-shaped fix.

### Structural findings (logged, not acted on)

- **The GUI stack is watched in a different order from the one it runs in.**
  The three pages are `gui-and-screens` → `the-gui-render-tree` →
  `text-and-fonts`, but at runtime the text becomes glyphs *before* the tree
  is sorted and batched. The landing page now says so out loud, which is
  honest and clumsy — a part-shape sentence should not have to apologise for
  the watch order. Either the order changes in pass 6, or the sentence gets
  shorter.
- **`hud-elements` now has the contextual bar on two rows** (14 background, 16
  foreground) with the experience level between them, because that is the
  record order. Correct and hard to read; a merged row with a note might serve
  the reader better, if the ordering fact survives the merge.
- **`prediction-and-acks` has two figures that both explain the same
  mechanism** — a state diagram of the two machines and a sequence of the
  refusal — and the fact-check found the argument living in the prose both
  times. One of the two may be redundant.
- **The Part X landing page's verified line says "seven systems"** (the
  figure's seven spokes) over a part of twelve pages. Both are true and the
  reader meets the mismatch immediately.
- **`anatomy/anatomy` is a Part X dependency that no Part X page links.**
  Session A logged the cross-link as pass-5 work (pass4.md:2765); this session
  re-derived that it is genuinely used — `the-client-loop`'s hook contrasts
  the two loops — so the link belongs in that hook's paragraph.


## Session G — Part VII Items and inventories (pass 4) *(2026-09-04)*

### Wording to re-read (a fact fix rewrote the sentence around it)

- **`enchanting`'s title and its opening section.** The H1 was *Enchanting: five
  ways onto an item* and is now *Enchanting: the five paths, and what each one
  is allowed to do*, because the grindstone is a removal; the section *The one
  line all five end on* became *The one question all five ask*, because the
  shared method does not exist and the shared *decision* does. Both are longer
  than what they replace. The verified line still says "picks up enchantments
  four other ways", which is now the only place the old framing survives — check
  it reads right beside the new title.
- **`items/README.md`'s shape paragraph.** "every later page assumes all three"
  was false, and the replacement admits that *contexts and predicates* is the
  outlier and could be watched first. That is a truer paragraph and a wordier
  one; it also now half-contradicts the numbered list's "the first three in
  order, then the engines in any order you like", which was already loose.
- **`items/README.md`'s *before you start*** grew from two ordering facts to
  three when `server/server-tick` was added. The paragraph is now the longest on
  the page.
- **`containers-and-menus`' advancement-channel paragraph.** The claim "nothing
  calls back into the menu" had to be scoped to the chest and the exceptions
  named, which turned one clean sentence into four.
- **`loot-tables`' world-gen paragraph** and its `BuiltInLootTables` category
  list: the list was incomplete and is now longer. It is nine items in a book
  whose budget is seven.
- **`recipes`' reload-window paragraph**, rewritten from "a window that is short
  and, on a reload, real" to an explanation of why nothing can observe it. The
  punchline is gone and the paragraph is longer; it may want cutting to a
  sentence.

### Structural findings (logged, not acted on)

- **`items-and-stacks`' *Two validators, one rule, two spellings* table** now has
  an *on failure* cell that is three clauses long, because the three
  `ItemStack.validateStrict` call sites do not agree. It is the only cell in the
  corpus that has to disambiguate its own row.
- **`enchanting`'s five-path table** is doing too much: after this session two of
  its cells carry three clauses each (the providers-and-loot gate and filter).
  Either the table narrows to the three columns that behave alike, or
  `EnchantRandomlyFunction` gets a sentence of its own.
- **`items/README.md`'s figure** lost an edge (`CM → CP`) and re-sourced another,
  so the second tier now has one node with no incoming arrow. That is *true* —
  contexts and predicates depends on none of the vocabulary — but a flowchart
  with an orphan node reads like an omission. Pass 5 should decide whether the
  figure wants a second, disconnected cluster or a note.
- **`contexts-and-predicates`' figure 1** gained a node outside both subgraphs
  (`SlotSource`). Same question: three groups, or two and a stray.

### Counts that are fine but say nothing

- **`items/README.md`:47** "the four ways one stack is serialised" is a count of
  *destinations* borrowed from `foundations/codecs-nbt-json`, not of anything in
  the decompile — `ItemStack` declares seven public serialisers. Correct as a
  cross-reference, meaningless as a number. Pass 5 may want to drop the number.

### The closer device

Part VII is **2 of 9** on *Questions players ask* (`loot-tables` and
`enchantments`), which is under session P's rule of thumb and needs nothing.

### For the terminology sweep

- The part says *the wire*, *the connection* and *the network* for the same
  thing, sometimes in one page (`containers-and-menus` uses all three).
- *Prototype* means the item's default `DataComponentMap` on `items-and-stacks`
  and nothing else anywhere; the glossary has it, but it reads as jargon on
  first use in `enchanting`.


## Session F — Part VI Entities (pass 4) *(2026-09-04)*

**Rewrites logged for a re-read.** Every fix below replaced a sentence pass
4 falsified; the wording is new and has not been read for voice.

- **`pathfinding`'s hook** — "eight ticks later" became "a hundred ticks
  later", which now agrees with the page's own second paragraph but repeats
  its number in the first two sentences. Worth deciding which of the two says
  it.
- **`pathfinding`'s malus illustration** — the fire/spider pair became a
  three-way lava example (`Strider` 0.0, `ZombifiedPiglin` 8.0, ordinary
  piglin −1). Three species in one clause is a lot for a sentence that is
  already carrying nine constants.
- **`pathfinding`'s `MoveControl` paragraph** grew from four sentences to
  seven, because "the single method" had to become "not the only method, not
  a single call site, and here are both other entrances". It is the longest
  paragraph on the page now and reads like a correction rather than an
  explanation.
- **`synched-entity-data`'s hook** was rewritten whole: the JVM
  static-initialiser claim is gone and the replacement ("written nowhere in
  `Sheep`; one new field on `Entity` would renumber every entity in the
  game") is a better fact but a longer sentence, and it now says in the hook
  what the section at L35-42 says again.
- **`authority`'s fall-damage paragraph** is four sentences where it was
  two, because the true statement needs both sides plus the
  `ServerLevel`-gate reason.
- **`ai-goals-and-brains`'s control-flag paragraph** now carries two
  mechanisms (the five-tick refresh and the leash) where it carried one, and
  the boat sentence has to distinguish *a mob is steering me* from *I am in
  a boat*. Check whether the leash belongs here or in a sentence of its own.
- **`entity-anatomy`'s registry paragraph** gained a second override
  direction (`getOptional` calls `super`), which is the subtlest thing on the
  page and is currently one clause.
- **`damage-and-death`'s blocking sentence** now names `Hoglin` and
  `Ravager` to prove who is knocked back. Good evidence, but it is an aside
  inside an aside.

**Structural findings, not acted on.**

- **`authority` states its own subject with the wrong number in four
  places** ("the four predicates" as a section heading, a closer heading, the
  hook and the cast row). Pass 4 corrected all four to five, but a page whose
  organising count changed is a page whose headings should be re-read
  together.
- **`entity-lifecycle`'s spawn-cascade figure gained a seventh rejection
  edge** to put `isValidSpawnPostitionForType`'s tests in source order. It
  is now sixteen edges and is the densest figure in the part.
- **The *Questions players ask* device**: Part VI is 3 of 10 under the
  literal heading (`ai-goals-and-brains`, `attributes`,
  `synched-entity-data`), which is inside session P's at-most-half rule —
  but two more pages carry the same device under a different name
  (`authority`'s *What the predicates explain*, `pathfinding`'s *Why mobs
  look stupid*), which makes 5 of 10 and is a data point for the *four
  spellings* problem session A logged rather than for the count.
- **`entity-anatomy` and `entity-lifecycle` both explain
  `EntityType.create`'s feature-flag and Peaceful gates**, from opposite
  ends — anatomy as *type to object*, lifecycle as the last filter before a
  mob exists. Not a shared skeleton, but a paragraph pass 5 could cut from
  one of them and cross-link.

## Session E — Part V Blocks (pass 4) *(2026-09-04)*

Wording debt from sixty-one fact fixes across eight pages. Nothing here was
acted on; pass 4 does not polish.

**Rewrites to re-read.** Five fixes grew a sentence into a passage:

- `signal-and-dust`'s **hook**. The old one was a picture ("14, 13, 12, visibly")
  and the true replacement is a picture plus a denial ("that staircase is the
  whole cost of redstone, and nobody has ever seen it"). It reads well but it is
  now the longest opening paragraph in the part, and the *why* — that the packet
  is built once per tick from the world rather than from the writes — is
  repeated three paragraphs later where the flowchart explains it. One of the two
  should go.
- `blocks/README.md`'s **opening**. Splitting the three feelings into "the first
  is a prediction and Part X owns it" plus "the other two" costs a sentence and
  puts a forward reference in the part's first paragraph. The alternative is to
  drop the crosshair feeling and open on two, which is tighter but loses the one
  a player notices first.
- `pistons-and-block-events`' **flag table** went from four rows to five and
  gained a *written by* column, because one of the four was not `moveBlocks`'s.
  The table is now wide enough to want the `custom.css` treatment, and the
  paragraph under it gained four lines explaining why the 82 row does not fire in
  the page's own scenario — true, and a digression inside the page's punchline.
- `block-breaking`'s **durability answer** grew from two sentences to five to
  carry `Item.mineBlock`'s three conditions and the shears exception. It is the
  page's best *Questions players ask* entry and it is now its longest.
- `diodes-and-observers`' **comparator fan-out paragraph** now names two callers
  and says which one the example uses, where it named one. The correction is
  right and the paragraph has lost its shape: the interesting fact
  (`BlockEntity.setChanged` is what makes a comparator notice a chest) is now
  third in the sentence order rather than first.

**The "three differences" tic, and the shape it hides.** `diodes-and-observers`'
comparison table is introduced as five rows because it *has* five rows, which is
honest and flat. The real structure underneath is two axes — repeater against
comparator (four differences, all about arithmetic and priority) and diode
against observer (one difference, the channel) — and the table flattens them into
one grid where the observer column is mostly "nothing". Pass 5 should decide
whether that is one table or two.

**Ambiguities left standing.**

- `diodes-and-observers` says `DiodeBlock.shouldPrioritize` holds for "a diode
  whose own input is not on the far side of it". That is exact and hard to read.
  The colloquial version — "a diode that is not pointing back at this one" — is
  also exactly right, but only under the reading of *pointing* the page spends a
  paragraph arguing against (FACING points at the **input**). Either the page
  needs a word for the output direction or the sentence needs a diagram.
- The same page says a diode "restricts `DiodeBlock.getSignal` to the one
  direction it faces" two paragraphs before establishing that FACING is the
  *input* side. Both sentences are true — the `direction` parameter of `getSignal`
  is the direction from the asker to the answerer, so it equals FACING when the
  output block asks — but a reader meets them in the order that makes them look
  contradictory.
- `block-interaction`'s bit-8 clause now carries a condition ("when the Chunk
  Builder option asks for it") inside the sentence that is supposed to be the
  page's payoff. It may want to be a parenthetical or a footnote instead.

**Structural findings, not acted on.**

- **`block-entities` is the part's odd page and the landing page now says so
  awkwardly.** It is not about choosing a state, performing a write, or answering
  a neighbour's write; the landing page's opening had to grow a fourth clause
  ("or — once — about the state a position cannot hold at all") to cover it. The
  cleaner reading is that Part V has a hub, two click lectures, a redstone trio,
  and one page about state that outgrew a block state.
- **`signal-and-dust` carries two subjects.** The default evaluator and the
  experimental one are the same computation with different semantics, and the
  page gives the second a full section plus a closing paragraph. It is the right
  material; it is also the point at which the page stops being about a lever and
  two dust.
- **`blocks-and-states`' write flowchart now has eleven nodes and a subgraph**
  after gaining the no-op branch. It is the most linked-to figure in the part and
  the densest; it may want splitting into the chunk write and the tail, which are
  already two subgraphs.
- **Six Part V pages end on *Questions players ask*** (all but the landing page
  and `blocks-and-states`), against session P's rule of thumb of at most half a
  part. This part is the worst offender per page in the book.

**Corpus-wide, found here.** The corpus has no settled word for the two update
channels' *directions*. `block-interaction` says "the direction pointing from
that neighbour back at the door"; `signal-and-dust`'s table says "which neighbour
is told first"; `diodes-and-observers` says "the one direction it faces". Three
pages, three conventions, one `Direction` parameter. A terminology sweep should
fix the vocabulary before the pages.

## Session D — Part IV The world (pass 4) *(2026-09-04)*

Wording debt from forty-nine fact fixes across eleven pages. Nothing here was
acted on; pass 4 does not polish.

**Rewrites to re-read.** Four fixes grew a sentence into a passage:

- `points-of-interest`'s **hook**. The old one was a clean negative ("two facts
  that never speak to each other") and the true replacement is a direction
  ("speak in one direction only … can only take a claim away"), which costs a
  clause and a sentence in the page's densest paragraph. It is now three
  sentences where it was two. Worth trying as one.
- `environment-attributes-and-timelines`' **easing paragraph** gained four lines
  and three numbers (0.67×, 1.19×, 13,564 against 10,436). The day-length fact
  is the better punchline and probably wants to be *in the hook* rather than two
  thirds of the way down a page whose hook is about colour — a structural call,
  not a wording one.
- `chunk-generation-pipeline`'s **radius-11 derivation** now explains
  `ChunkStep.Builder.getRadiusOfParent` in the middle of a paragraph that was
  already the page's most arithmetical. The true rule ("a debt counts only when
  the step's own parent already sits a ring out") may deserve to be its own
  sentence, or a row in the table above it.
- `chunk-storage`'s **IOWorker priority paragraph** gained five lines saying what
  the shutdown barrier is and why a flush still waits. The section's subject is
  "why the server thread never waits", and this is a digression inside it.

**The dead-constant tic.** Four fixes in this part took the same shape: *the
number is right, the constant that names it has no readers*, so the prose now
says so — `AcquirePoi.SCAN_RANGE`, `SculkSensorBlock.ACTIVE_TICKS`,
`LevelChunkSection.BIOME_CONTAINER_BITS`,
`ThreadedLevelLightEngine.DEFAULT_BATCH_SIZE`, plus
`ChunkStatus.MAX_STRUCTURE_DISTANCE` which the pipeline page already flagged.
Five instances of one aside in one part is a tic. Pass 5 should pick one voice
for it and use it everywhere in the corpus, and probably drop the aside on the
pages where the constant is not otherwise mentioned.

**Named-qualifier debt.** The count corrections replaced round motifs with
awkward ones: "eleven chunks past the edge of view" became "thirteen chunks past
the ticket that asked for it", and "up to 27 sections across nine chunks" became
"up to fourteen sections across seven chunk columns". Both are true and neither
scans. `tickets-and-loading`'s header line was rewritten for the same reason and
lost its scenario ("a chunk eleven chunks away becomes a ticking part of the
world" → "a column of chunks thirteen past the edge of view is asked for"); the
header should get its ticking image back around the true number.

**Structural findings, not acted on.**

- `chunk-anatomy`'s "packing buys a smaller palette, not narrower entries"
  contradicts its own "can demote a container a whole rung" a few lines later.
  Both are true of different cases; the sentence needs splitting, not correcting.
- `lighting` says `SkyLightEngine.checkNode` "only decides what to enqueue" in
  one paragraph and describes it writing stored levels in the next. A clash
  between two paragraphs, not an error in either.
- Part IV's landing page still calls the part "the four side-systems that make
  the world they hold feel alive" in its header while its shape paragraph now
  counts five pages off the conveyor. The header's four is the four
  *side-systems*; environment attributes is a fifth thing and the header does
  not account for it.
- `points-of-interest` describes `PoiManager.isVillageCenter`'s predicate without
  saying it reads through the **non-loading** `SectionStorage.get`, so an
  unloaded section is never a village source whatever is on disk. A real fact the
  page is missing rather than a wrong one — one sentence, and it belongs next to
  the "an unclaimed bed makes no village" callout.
- The cross-links session A logged here as pass-5 work are half done:
  `chunk-anatomy` now links `foundations/identifiers-and-registries` (pass 4
  needed it for addition 2). Part XII's two are still open.

## Session C — Part III The server (pass 4) *(2026-09-04)*

Wording debt from twenty-eight fact fixes. Nothing here was acted on; pass 4
does not polish.

**Rewrites to re-read.** Three fixes grew a sentence into a passage and each
should be read again for rhythm rather than for truth:

- `starting-a-server`'s **opening paragraph**. Its frame ("Between those two
  lines the server …") was inverted — five of the six things listed happen
  before *Preparing level* prints — and the fix adds a clause and a second
  sentence to a paragraph that was already the page's densest. The hook is
  untouched. Worth trying as two sentences instead of one long one.
- `server-tick`'s **packet-drain paragraph** gained five lines explaining
  that chat and commands arrive as tasks rather than as packets. It is true
  and it matters, but it lands in the middle of a section whose subject is
  the drain, and the event-loop section forty lines later is where the other
  door is actually documented. Pass 5 should decide whether the sentence
  points forward instead of explaining in place.
- `server-level-tick`'s **falling-sand exception** is now its own paragraph
  after "The ordering is visible from a client". That is the right place for
  it factually, but it means the section's punchline is immediately
  qualified. Consider leading with the exception and landing on the rule.

**Repeated hedges introduced.** "Almost nothing", "almost none", "all but the
first", "two of the three endings", "on this side of the jar" — five new
qualifiers in one part, each earned individually. Read them together; if the
part now reads as hedged, some of them want re-scoping into a positive claim
instead ("`FallingBlockEntity` is the one place that …").

**Structural findings, not acted on.**

- **`how-a-server-dies` carries two subjects.** The three-endings comparison
  is the lecture; *What you lose if you kill the process* is a durability
  page hiding inside it, and it is where four of the session's nine
  corrections landed — autosave spacing, what `level.dat` actually holds,
  the `SavedData` files, the per-ending answer. It is the strongest material
  on the page and the least connected to its figure. Pass 5 should decide
  whether it is a section or a page.
- **`server-tick`'s event-loop figure grew from eleven edges to fourteen**
  when the two impossible ones were replaced by a truthful queue-empty exit.
  It is now the densest flowchart in Part III and its `C` node label is long
  enough to be a sentence. Correct, but worth redrawing for shape.
- **`starting-a-server`'s sequence figure gained an arrow** (the pack-opening
  stage moved onto the `Main` lane) and split `spin` into three. At 27 items
  it is now the largest single diagram in the part — `server-level-tick` has
  more in total (35) but across two figures.
- **Part III is 2 of 5 on *Questions players ask*** (`server-tick`,
  `server-level-tick`), which is *inside* session P's rule of thumb and one
  of the better parts on the device — recorded here because the corpus-wide
  pass needs the parts that are already fine as much as the ones that are
  not. The session's own first guess at this number was five, and counting
  it settled the matter; treat every per-part count in this file the same way.

**Small.**

- `players-and-sessions`'s section heading *Four ways the session changes*
  now sits above a paragraph that names a fifth (the end credits). The
  heading is still the right frame for the comparison, but the tension is
  visible; a reader who counts will stop.
- `server-tick`'s `tickChildren` table row about the player-info broadcast
  now reads "its own counter has not passed 600 — so every 601st call, not
  every 600th tick", which is two corrections in one cell and the longest
  *skipped when* value in the table.
- The em dash count in `how-a-server-dies`'s durability section went up by
  four with the watchdog asterisk. Whole-page voice pass.

## Session B — Parts I and II (pass 4) *(2026-09-04)*

Wording debt and structural findings from Part I and Part II's fact-check.
Every factual fix is in `docs/pass4.md`; nothing below was acted on.

**Wording to re-read** (a hook or an argument was rewritten around a
correction):

- `src/systems/anatomy/README.md` — the opening hook and the first *Watch in
  this order* teaser were both rewritten mid-sentence. The hook now says
  "every sequence diagram … lanes that name classes and assume you know
  which thread each class is on", which is true and two clauses longer than
  the sentence it replaced.
- `src/systems/anatomy/anatomy.md` — four paragraphs grew a qualifying
  clause each: the bootstrap ordering, the crash relay, the singleplayer
  differences and *Everything else that matters is serialised onto*. The
  crash paragraph is now the longest answer under *Questions players ask*
  and carries three class names it did not before.
- `src/systems/foundations/identifiers-and-registries.md` — the opening
  paragraph's last sentence was the hook's causal clause and is now two
  sentences. It is true; it no longer lands.
- `src/systems/foundations/tags.md` — the hook's first sentence now carries
  a parenthetical about component prototypes before it reaches
  `Registry.PendingTags`, which is the thing the page is about. Consider
  moving the second swap to *Prepared, then applied* and leaving the hook a
  single clause.
- `src/systems/foundations/data-driven-types.md` — the *Fifty-six of them*
  paragraph gained the criterion's two exclusions and is now the densest
  paragraph on the page. The number is right; the sentence explaining it
  reads like a footnote promoted.
- `src/systems/foundations/codecs-nbt-json.md` — the *homogeneous numeric
  list* sub-section was inverted, so its bolded lead sentence is now a
  double negative ("A numeric array stays an array, but nothing turns a list
  into one"). Worth one more pass.

**Structural findings**, logged and not acted on:

- **`anatomy/README.md`'s root figure is not homogeneous.** Four of its five
  edges point at *parts*; the fifth points at a *page* of Part I (*what this
  book skips*). Either is defensible; the mix is what a reader notices.
- **`anatomy/README.md`'s hook says "a server that ticks and a client that
  draws".** The client ticks too — 0 to 10 times a frame, which is the
  lecture's own first arithmetic. The shorthand is deliberate and the
  lecture unpacks it two pages later, but as the sentence a reader memorises
  it plants the wrong idea. A pass-5 judgement, not a fact fix.
- **`identifiers-and-registries`'s "the wire id is the line number".** True
  as a metaphor for the ordinal of the registration statement and false
  read literally (`Items.DIAMOND_SWORD` is at `Items.java:993` and its raw
  id is nowhere near 993). The lecture unpacks it in the next two sentences;
  the landing-page teaser and the verified line do not. Decide whether the
  teaser keeps the metaphor.
- **`reference/class-index.md` is still blind to diagrams** (session A's
  finding) and Parts I and II are among the worst affected: every lane in
  the anatomy, tags and data-components figures is a `participant X as
  ClassName` the index cannot see.
- **Cross-links session A judged missing** and left to pass 5 touch this
  part: Part X ← `anatomy/anatomy`, Part IV and Part XII ←
  `identifiers-and-registries` and `codecs-nbt-json`. Each is a real
  dependency with no link or backticked slug on the depending page.

## Session A — The frame (pass 4) *(2026-09-04)*

Wording debt and structural findings from the frame's fact-check. Nothing
here was acted on; every factual fix is in `docs/pass4.md`.

**Wording to re-read** (a hook or an argument was rewritten around a
correction):

- `src/introduction.md` — the figure paragraph and the skip-list sentence were
  both rewritten mid-sentence; the skip list is now a longer list and reads
  like one.
- `src/lectures.md` — the Part III "watch the environment page first"
  paragraph lost its superlative ("the page with the most dependants in the
  book") and gained a cost argument. It is true now; it is not as good a
  sentence.
- `src/systems/server/README.md` — the *before you start* section grew a long
  second paragraph to carry the environment-attributes dependency and the two
  different cuts. It is the longest *before you start* in the corpus.
- `src/maps/fanin.md` — the hook now spends three lines on what the chart does
  not count before it gets to the surprise.
- `src/maps/packages.md` — the `net/minecraft/data` clause became a
  four-line aside with a cross-link.

**Structural findings** (not acted on, per the charter):

- **The nine-page dependency table's membership rule is unstated and
  inconsistent.** By its own criterion — a page two or more landing pages
  assume — three Part II pages qualify and are absent (`resource-system`:
  VII and XI; `text-components`: IX and X; `data-driven-types`: XII and XIII),
  while a one-part dependency (*contexts and predicates*, XIII only) is in it
  and `world/chunk-generation-pipeline` (XII, called "hard" by the page) is
  not. State the rule or fix the membership.
- **Part IV's sidebar order disagrees with its own landing page.**
  `src/SUMMARY.md` lists *environment attributes and timelines* sixth in Part
  IV; `world/README.md`'s *watch in this order* and `lectures.md` both list it
  first. Part IV is the only part where the three orders differ (checked for
  all thirteen). `lectures.md` was reworded this session to say "Part IV's own
  watch order lists it first", which is true but papers over the split.
- **The class index labels every landing page "README".** Eleven distinct
  pages render under that one word; 26 rows carry at least one and nine carry
  two or more — in the `LivingEntity` row the reader sees "README" three times
  with nothing to tell them apart. Label by part.
- **Teach the class index to read diagrams.** 135 class/page pairs and 112
  classes are named only inside mermaid blocks (51 of them as
  `participant X as ClassName`), and 26 of those classes have no row at all.
  The page now states the limitation; removing it is the better fix.
- **The lane key carries 45 rows no page claims**, against session E's ruling
  that it is pruned to lanes in use. Three appear nowhere but `lanes.md`:
  `PTT`, `TCTD` and (until this session) `TDec`. `PTT` is `TEMPLATE.md`'s
  worked example of the nested-class rule and its pilot page has since become
  a flowchart with no lanes, so the rule's only illustration is unused.
- **Two lanes for one class, on purpose.** `RCPL` and `CPL` are both
  `ClientPacketListener`, because the chat diagram shows the sender's client
  and the recipient's at once. Recorded in `TEMPLATE.md`'s collision prose and
  in a note inside the figure; if pass 5 dislikes it, the alternative is two
  identically-labelled lanes.
- **`reference/submit-phases.md` is a catalogue that needs a paragraph.** Its
  "order bucket" and "may be reordered" language is unexplained without
  `SubmitNodeStorage` and `PhaseSubmitGrouper`; that is a page shape question,
  not a fact.


- **2026-09-03, session M — Part XII.** Eight system pages plus a landing
  page and a Reference page. **Every page landed inside the 260–340 brief or
  below it** — 204 to 288, with the landing page at 143 and the Reference
  page at 152 — and three pages came in under 240, which is the first time a
  part has *undershot*. **Zero bulleted lists across the whole part**, as in
  Part XI. Four cuts, all from the old `worldgen-pipeline`, now `terrain`,
  and none of them a fact the corpus loses: `NoiseSettings.guardY`'s
  multiples-of-sixteen validation (a codec detail with no visible
  consequence); the registries inventory at the foot of the page (the
  data-driven type pattern owns that table and three of its rows now link
  here); the `ChunkStatusTasks` caller list (Part IV owns the conveyor and
  the landing page makes the dependency explicit); and the `Heightmap.Usage`
  taxonomy (the *status, not the step* half survives, and `chunk-anatomy`
  already has the rest). Two more facts were **moved rather than cut** and
  are in [pass4.md](pass4.md) instead: the minus-one default write radius
  and `WorldGenRegion.getChunk` throwing, both now stated only on
  `features-and-placement`, which is where they bite.

  Wording debt:

  - **The *questions players ask* device is on six of the eight pages**,
    which is the ratio session K flagged in Part X and the trap the old
    seven-heading template fell into. It is genuinely the honest home for
    what used to be an invariant wall, which is exactly why it spreads.
    Session P should count it as a *device* becoming a *slot*, and pass 5
    should consider a rule — at most half the pages in a part.
  - **Session K's two formulas are gone from Part XII too.** No page says
    "the one sentence a player recognises" and none carries a
    names-you-will-hunt-for list; two pages use the *for a 1.21-era reader*
    blockquote instead (`density-functions` on the two vocabularies for the
    six climate functions, `jigsaw-and-templates` on the singular
    *structure* folder). With X, XI and XII converted the formulas survive
    only in Part XIII.
  - **Second person, now five parts wide and needing a ruling rather than
    another flag.** `terrain` opens with *you dig into a cave*, `biomes`
    with *walk out of a desert*, `trees` with *plant a single dark-oak
    sapling*, `structure-placement` with *type the locate command*. It is
    the most natural way to start inside a scenario and it is the house
    style now whether or not anyone decided it. Sessions I, J and K all
    flagged the drift.
  - **`terrain`'s title is a compromise.** The page is noise, surface and
    carvers — three statuses — so *Terrain* is broader than its subject,
    while its old name collided with Part IV's *chunk generation pipeline*.
    If pass 5 finds a better name the redirect already exists and a second
    costs nothing.
  - **The lattice fact is stated three times across two pages** — twice in
    `terrain`, at its two resolutions, and once more in `density-functions`
    from the cache side. All three are true and it is the part's best "true
    twice over" observation, but one of the three should become a link.
  - **`jigsaw-and-templates` is the shortest page in the part** at 204
    lines, because the processor stack is described rather than traced. If
    pass 5 wants a section trimmed elsewhere, this is the page that could
    absorb it instead.

- **2026-09-03, session L — Part XI.** Eleven system pages plus a landing
  page and a Reference page. **Every page landed inside the 260–340 brief**
  — 256 to 339, with the landing page at 150 and the Reference page at 81 —
  which is the first part to need no length note at all, and the brief was
  given to the drafters in the prompt rather than corrected afterwards.
  **Zero bulleted lists across the whole part**: every one of the eight old
  pages opened with a field inventory and closed with a twenty-bullet
  invariant wall, and none of that survives. The material is in cast tables,
  decision tables, *Questions players ask* sections and the sentences that
  use each name. `lightmap-fog-and-sky` came *down* from 447 to 339 by
  dissolving the twenty-four-attribute enumeration Part IV already owns.

  The one shape note pass 5 might revisit: **`models-and-atlases` carries a
  single figure over 330 lines.** Its drafter cut a sequence diagram that
  repeated the fan-out flowchart, which was right, and cut an item-model
  flowchart with it, which is arguable — the *How an item picks its model*
  section is where two forward links from Part VII land and it is now the
  page's longest stretch of unbroken prose.

  **Cuts made, all field inventories, no behaviour:** `the-frame` dropped the
  `GameRenderer` field roll-call (eleven fields), most of the `GameRenderState`
  and `CameraRenderState` field lists, and the `CrossFrameResourcePool`
  mention, which asserted only that the pool exists and is three frames deep;
  the `Camera` accessor roll-call is compressed to four examples inside the
  1.21 blockquote. `lightmap-fog-and-sky` dropped the twenty-four-item
  `EnvironmentAttributes` list outright — every constant on it now appears in
  the sentence that consumes it, and the system itself is Part IV's — along
  with the `EnvironmentAttribute` builder and flag inventory and the
  `Timeline`/`ClockTimeMarkers` tour, all of which Part IV already teaches.
  `particles` dropped the nine-class inventory into the cast table.
  `entity-rendering` moved its fifteen-phase and thirteen-renderer catalogues
  out to `src/reference/submit-phases.md` and its render-state ladder to a
  generated figure. `blaze3d`'s naming-drift bullet became a two-column table. And
  `models-and-atlases` dropped a long tail of identifiers with no facts
  attached — the `ModelManager` field and getter roll-call, `ModelBakery`'s
  destroy-stage constants and the two fire sprites, `ModelBakery.BakingResult`'s
  members, the four `ResolvedModel` parent-walking helpers, `Sheets`,
  `SpriteGetter`, `TextureAtlasSprite`, `Stitcher.registerSprite`,
  `Variant`/`VariantMutator`, and the observation that there are two
  `MaterialBaker`s. Nothing behavioural went with them, but that last one was
  the mechanism behind the block-atlas rule the page still states, so pass 5
  should decide whether the rule now floats. `blaze3d` cut its
  `RenderSystem` member roll-call, and one member in it was doing work:
  `RenderSystem.outputColorTextureOverride` and
  `RenderSystem.outputDepthTextureOverride` were the only mention anywhere in
  the corpus of *where the world can be redirected*, and no page names them
  now. `lightmap-fog-and-sky` dropped one behavioural sentence
  with its field inventories: `FogRenderer.endFrame` and
  `CloudRenderer.endFrame` rotating their ring buffers at the close of a
  frame. Worth restoring if a line becomes available, since it is the only
  mention of what ends those two buffers' frames.

  **Wording debt.** The *headline for a 1.21-era reader* formula that opened
  eight of eight Part XI pages is gone as an opening and survives as one
  blockquote at the foot of each — the same move session K made, so the
  device is now consistent across two parts and pass 5 should check it reads
  as a convention rather than a tic. Three pages open on a second-person
  scenario in the present tense (*you fly forward in creative*, *you
  right-click a block into place*, *stand on a hill and watch the light go*),
  which is the strongest opening in the part and also, at three, the point at
  which it becomes a pattern. `particles`' *Where to look* is a
  middle-dot list where every other page's is a sentence; it reads fine and it
  is the only one, so it is either a deliberate variation or a fix.

- **2026-09-02, session F — Part V.** Seven pages at 243–388 lines, which is
  the first part to land inside the 260–340 brief rather than over it — the
  line budget was given to the drafters explicitly this time, mid-flight, and
  it worked. The exception is **`blocks-and-states` at 388**, and it is the
  one page here with a genuine length case to answer: it carries two figures
  (the twelve-class containment figure and the write flowchart the other six
  pages link to), the flag-bit table, and a grounding trace. Its cheapest cuts
  if pass 5 needs them, in order: the *Twelve classes and one Cartesian
  product* figure could lose the three `Property` subclasses to prose; the
  *four decisions, four lookups* section is the most compressible, since
  `StairBlock.getStairsShape`'s corner rules are detail the hook does not
  need; and the `BlockBehaviour.BlockStateBase.initCache` thread-safety
  paragraph is the page's most self-contained.

  **Cuts made, and where they went.** All are names rather than claims.
  `block-interaction` dropped the `InteractionResult.ItemContext` record and
  `InteractionResult.Success.withoutItem`; the full `BlockSetType` component
  roster (fourteen components, seventeen instances, its register/values/codec
  trio) down to what the door needs; the "twenty-four blocks override
  `BlockBehaviour.useItemOn`" count, dropped rather than carried because it
  could not be cheaply re-verified — **worth restoring with a real count**;
  the creative reach modifier, keeping only the server's 1.0 of slack; and the
  alternative door entry points (the redstone path, `DoorBlock.setPlacedBy`,
  the wind-charge path). `block-breaking` dropped the creative-mining branch
  entirely (a fresh START every five ticks, each its own prediction), the
  `ServerPlayerGameMode` anti-desync paths, the `RedStoneOreBlock.attack`
  case — the only left-click that files a ledger entry without breaking
  anything, arguably `prediction-and-acks`' material — the non-player removal
  path through `Level.destroyBlock`, and the note that
  `BlockTags.NEEDS_IRON_TOOL` is a data-generation input never read at
  runtime, which is a good myth-table row for whoever owns tags. The redstone
  split dropped the piston's long tail of special cases: slime reordering,
  the sticky-retract interrupt, `MovingPistonBlock` destruction, and the
  moving hitbox. None of the above is a factual cut; all of it is length, and
  every item is recoverable from the pass-2 `redstone.md` in git.

  **Wording debt.**
  - Three pages used to say some version of "shape updates run on both sides,
    neighbour updates are server-only, and here is the exception". That is now
    owned once, by `blocks-and-states`' *The two update channels* section, and
    the other six link to the anchor. **Check in pass 5 that none of them has
    started re-explaining it**; this is the duplication that produced three of
    the part's pass-2 errors.
  - `block-interaction` and `block-breaking` carry an identical four-sentence
    preamble blockquote. That is deliberate (R6) and it should stay identical
    — if either drifts, they stop reading as one lecture in two halves.
  - The reflow around three link edits is untidy: `block-interaction` line
    155, `block-breaking` line 242 and `block-entities` line 96 each have an
    awkward wrap where the `#the-two-update-channels` anchor was added.
    Cosmetic only.
  - `diodes-and-observers` line 52 runs long after
    `HorizontalDirectionalBlock.FACING` replaced the shorter name the
    verifier rejected.
  - The three redstone pages were written by the session rather than by
    drafting agents, so they have had one fewer pair of eyes on their prose
    than the rest of the corpus. They are the pages most likely to be carrying
    the session's own tics.


- **2026-09-02, session E — Part IV.** **The length debt is this session's
  main bequest.** Ten pages, and eight of them landed at 358–417 lines
  against the 260–340 the brief asked for; the two pilots sit at 377 and
  389, so Part IV is now the corpus's fattest part. Every drafter reported
  trimming twice and stopping rather than dropping a verified fact, which is
  the right call under R7 but leaves the bill here. Each names its own
  cheapest cut, and those are the places to start: `chunk-anatomy` — the
  *double indirection* subsection on block-entity tickers (arguably
  `block-entities` material), the *what the client actually receives* answer
  (arguably `what-the-client-is-told`), and the second half of the
  `ImposterProtoChunk` paragraph; `lighting` — the sky-column section, its
  most self-contained; `environment-attributes-and-timelines` — *what
  crosses the wire*, or the *what a type allows* subsection;
  `points-of-interest` — the *who else asks* table; `game-events-and-vibrations`
  — one *Questions players ask* entry. Nothing above is a factual cut; all of
  it is length.

  **Cuts made, all of them names rather than claims.** `chunk-anatomy` drops
  `Block.UpdateFlags` as a named catalogue (the four flags the write path
  actually tests survive; the catalogue belongs to `blocks-and-states`),
  `CarvingMask`'s internal shape, `UpgradeData.EMPTY`, and a dozen field
  names now carried by the sentences that touch them.
  `chunk-generation-pipeline` drops `WorldGenContext`'s six components, the
  `ChunkGenerator` method roll-call (Part XII owns those; `createStructures`
  and `createBiomes` stay because their threading is the point),
  `Blender.of`, `ChunkAccess.isUpgrading` skipping *SPAWN*, and
  `Util.DEFAULT_MAX_THREADS`; it also hands `ServerLevel.updatePOIOnBlockStateChange`'s
  worker-thread posting to `points-of-interest`, **which now owns and
  corrects it**. `lighting` drops the `LightEngine.QueueEntry` constructor
  list, four constants, and the *called by* roll-call, of which only
  `ClientPacketListener.queueLightRemoval` and `ClientLevel.unload` are now
  absent from the corpus. `chunk-storage` drops the thirteen-component
  `SerializableChunkData` inventory, `RecreatingSimpleRegionStorage`, and
  "crosses the network as: nothing" — and **proposes** that the read path's
  null-parse failure branch and `ChunkMap.handleChunkLoadFailure` move to
  `chunk-generation-pipeline`, which pass 5 should either do or drop.
  `scheduled-ticks` drops `ScheduledTick.probe`. `fluids` drops
  `FluidState.AMOUNT_FULL`, `EmptyFluid`, `FluidTags.WATER`/`LAVA`,
  `LiquidBlock.fizz` and the client-packet names.
  `game-events-and-vibrations` drops three private constant *names* (the
  numbers survive in the listener table) and the "there is no *DebugPackets*
  class" aside — **which wants a home in `naming-drift`**.
  `environment-attributes-and-timelines` drops the twenty-one-class *called
  by* roster; its author suggests it becomes a Reference table, and session
  O should rule.

  **Voice debt.** Eight of the ten pages end their opening paragraph on a
  bolded sentence — the same device session C already flagged for Part II,
  now used corpus-wide, and by pass 5 it will be a tic rather than a
  signature. Two hooks are close cousins in shape ("X does not do the thing
  you think, it does Y" — `fluids` and
  `environment-attributes-and-timelines`) and should not sit near each other
  in the lecture order. Three pages now carry a *Questions players ask*
  close (`chunk-anatomy`, `lighting`, `points-of-interest`) plus the pilot's,
  which is four in one part; check whether that reads as a part-level
  convention or a template.

  **`level-data-and-rules`'s Reference framing is provisional.** Session E
  changed only its header, its links and its opening; it still carries a
  `## Responsibility`-era body shape and a "Short, no trace" ancestry.
  Session O owns the reframe.

*(pass-3 and pass-4 sessions append below, newest first: the page, what
was cut or moved, and why)*

- **2026-09-02, session D — Part III.** Five pages, and the register debt
  pass 2 logged against this part is **paid**: the dozen "not X but Y",
  "two, not one" and "and there is no Z" constructions that made Part III
  the corpus's worst offender are gone, restated positively. The three
  bullets opening with "Two …" are gone with the bullet walls — all five
  pages now carry **zero** bulleted lists between them (the budget allows
  three each), which is worth checking is not its own monotony: the
  material became prose, tables and figures, and pass 5 should look for
  paragraphs that would read better as a short list after all.
  *Cuts and moves, per page.*
  **`server-tick`**: the field inventories go (the `ServerTickRateManager`
  sprint bookkeeping — `remainingSprintTicks`, `sprintTickStartTime`,
  `sprintTimeSpend` — and `MinecraftServer.mayHaveDelayedTasks` as a named
  field are no longer listed, only used); `MinecraftServer.spin` and the
  creation of the Server thread move to `starting-a-server`; the crash
  report, `MinecraftServer.constructOrExtractCrashReport`,
  `MinecraftServer.onServerCrash`, the *finally* and `ServerWatchdog` move
  to `how-a-server-dies`, leaving a pointer; `Minecraft.packetProcessor`
  (the client's copy) is left to Part X; `TickRateManager` living in
  `ClientLevel` too is left to `anatomy`, which already says it; the
  *Interfaces* and *Data-driven by* blocks dissolve into the cast row, the
  `tickChildren` table and the questions. The `SampleLogger` /
  `TpsDebugDimensions` paragraph pass 2 flagged as a cut candidate
  **survives**, now inside the bookkeeping section — pass 5 should decide
  again with the page in front of it.
  **`server-level-tick`**: the field inventory and the thirteen-step
  narration go as structures, every fact re-placed; `BlockEventData` and the
  `ServerLevel.customSpawners` / `dragonFight` / `raids` / `sleepStatus`
  fields are no longer named as fields. `ServerChunkCache.onLightUpdate`'s
  off-thread hop is **moved** to `../world/lighting.md`, which already
  narrates it in full (checked). The "Exception ticking world" crash wrapper
  moves to `server-tick`; the `GameRules` package-move note and the
  *DO_DAYLIGHT_CYCLE* / *DO_MOB_SPAWNING* renames move to
  `../world/level-data-and-rules.md`. The pass-2 guard bookkeeping spread
  across six narrated steps is now the flowchart, which is what pass 2
  predicted would let it be cut.
  **`players-and-sessions`**: the `PlayerList` and `ServerPlayer` field
  inventories go. **Three items need a home and have none yet** — the
  `ServerPlayerGameMode` paragraph (block-breaking state,
  `ServerPlayerGameMode.changeGameModeForPlayer`,
  `ServerPlayer.storeGameTypes`), which belongs with `player-anatomy` or a
  game-mode page; `ClientboundSetChunkCacheRadiusPacket` /
  `ClientboundSetSimulationDistancePacket` on a view-distance change, which
  is server reconfiguration rather than a session event (candidate home:
  `what-the-client-is-told`); and `PlayerDataStorage`'s *.dat_old* and
  *corrupted* rescue, compressed here into one cast-table cell and wanting a
  save-format Reference entry. The `ClientboundSetHealthPacket`
  saturation-crossing detail moves to `player-anatomy` by reference; the
  login state machine, the 600-tick login timeout, the auth thread and
  `CommonListenerCookie`'s travel move to `protocol-phases`, linked; the
  permission model is one sentence and a link to `brigadier-and-commands`
  (pass 2 asked session K to check the two had not drifted — they no longer
  can).
  **`starting-a-server`** (was `server-lifecycle`): the field inventories
  go; everything about stopping — `MinecraftServer.halt`, the *finally*, the
  save model, `Util.shutdownExecutors`, the lock release, the three endings,
  the crash-report machinery — moves to `how-a-server-dies`. Only
  `CrashReport.preload` stays, because it happens at boot. The side threads
  became a four-column table (thread · made by · daemon · what it may
  touch), which is the enumerative-beyond-seven rule doing its job.
  *Wording left rough on purpose.* All five pages end their opening
  paragraph on a bolded or dashed sentence — one voice, five times, and the
  same tic session C logged for Part II; a corpus-wide look belongs in pass
  5's voice sweep rather than in any one part. `how-a-server-dies` uses
  *the number* device twice (**Ten seconds**, and the comparison table's
  "differ in one cell") where once is the convention. `server-tick`'s
  *Questions players ask* was trimmed to four questions by moving the
  profiler answer into the bookkeeping section and the worker-crash answer
  into the event-loop section, which is where both belonged; the remaining
  four are the ones a player would actually ask. Part III now has five
  pages where pass 2 had four, so the part is longer, not shorter — the
  length bill for it comes due here.

- **2026-09-02, session A.** `tickets-and-loading`: the *data it owns*
  inventory is gone — `ChunkHolder.queueLevel`, `ChunkMap.unloadQueue`,
  `ChunkMap.serverViewDistance` and `MIN_VIEW_DISTANCE`, `ChunkMap.playerMap`,
  `ChunkMap.getUpdatingChunkIfPresent`, `ServerPlayer.requestedViewDistance`
  / `chunkTrackingView` / `lastSectionPos`, `PlayerList.viewDistance` /
  `simulationDistance`, `ServerChunkCache.CACHE_SIZE` / `lastChunk`,
  `ServerChunkCache.ticketStorage` are no longer named (reason: the cast
  table replaces the inventory; the class index still answers "where");
  the *Called by* list (teleports and `ServerPlayer.doTick` as callers of
  `ChunkMap.move`, `ForceLoadCommand` → `ServerLevel.setChunkForced` at
  `ChunkMap.FORCED_TICKET_LEVEL` loaded synchronously) and the *Calls into*
  list are cut (reason: interfaces survive as one sentence; the forced
  ticket is in the table). `protocol-phases`: the *Crosses the network as*
  packet list is cut in favour of `reference/packets.md`
  (`ClientboundLoginCompressionPacket` is now unnamed — the compression
  switch is described); the *Data-driven by* bullet (server properties,
  resource-pack settings, data packs) is cut; the *Interfaces* callers are
  folded into one sentence. Wording left rough on purpose: both pilots
  still carry em-dash chains in the decision tables' gate cells, and the
  tickets page says "graph" and "tracker" for the same object.


- **2026-09-02, session C — Parts I and II.** Cuts are names, not claims,
  unless marked; the class index still answers "where" for every name here.
  **`anatomy`**: the eleven-row thread table and the situational-threads
  paragraph moved to `reference/threads.md` (already there, verified);
  `Minecraft`'s manager inventory retired (`TextureManager`, `ShaderManager`,
  `ModelManager`, `AtlasManager`, `FontManager`, `SoundManager`,
  `GameRenderer`, `LevelRenderer`, `EntityRenderDispatcher`,
  `BlockEntityRenderDispatcher`, `ParticleEngine`, `MouseHandler`,
  `KeyboardHandler`) and `MinecraftServer`'s (`ServerFunctionManager`,
  `TimerQueue`, `ServerClockManager` — the rest are on `server-tick`); the
  stale-`TickTask`, "Can't keep up!" and flush-bracket invariants cut to a
  link to `server-tick`, which states them; "the server is the game; the
  client is a view of it" and the "this page is the frame" meta-sentence
  cut (the landing page says it); `RconThread`, `QueryThreadGs4`,
  `ManagementServer` dropped from *Where to look*.
  **`what-this-book-skips`**: "Seventy-six pages cover the game" cut (the
  count churns); the four gap lists folded into one table with two prose
  paragraphs for the three entries that needed more than a cell; the four
  "the honest version" / "the detail worth having" tics rephrased.
  **`codecs-nbt-json`**: cut names — `ExtraCodecs.intRange` /
  `nonEmptyList` / `optionalAlwaysPresentFieldOf`, `TagTypes`,
  `NbtIo.readCompressed`, `NbtOps.convertTo`, the three printing visitors
  and the `/data` colouring aside, the five `nbt/visitors` classes,
  `ValueOutput.TypedOutputList`, `StreamEncoder` / `StreamDecoder`,
  `ByteBufCodecs.VAR_INT` / `STRING_UTF8` / `registry` / `holderSet` and
  the `…Trusted` variants, "up to twelve field codecs", `RegionFileVersion`'s
  GZIP/LZ4/none roster; the caller inventory (`PlayerDataStorage`,
  `LevelStorageSource`, `SavedDataStorage`, `SavedDataType`,
  `CommandStorage`, the three NBT command arguments, `Entity.saveWithoutId`
  / `load`); moved to links: the `ComponentSerialization` matrix
  (`text-components`), the `RegistrySynchronization` case
  (`protocol-phases`), `CODEC_WITH_BOUND_COMPONENTS` (`data-components`),
  `RemoteSlot`'s either-or (`containers-and-menus`).
  **`identifiers-and-registries`**: `MappedRegistry.byValue` cut;
  `TagLoader` named only as `TagLoader.buildUpdatedLookups`.
  **`resource-system`**: `RegistryDataLoader` dropped from its calls-into
  (the registries page owns it). **`tags`**: nothing cut.
  **`data-components`**: the hashing detail (`HashedStack`,
  `HashedPatchMap`, `RemoteSlot.Synchronized`'s either-or and promotion,
  the creative double guard) moved to `codecs-nbt-json` and
  `containers-and-menus`; three enchanting facts moved *towards* Part VII
  and **not yet present there** — "if the prototype lacks `ENCHANTMENTS`
  the `updateEnchantments` write is skipped", "`clickMenuButton` consumes
  lapis and fires `CriteriaTriggers.ENCHANTED_ITEM`", "`/enchant` is the
  same tail after `Enchantment.canEnchant` and a compatibility check" —
  session H absorbs them into `enchantments`; `RegistryDataCollector`'s
  client-only status no longer stated; `EnchantmentHelper`,
  `ItemEnchantments`, `RemoteSlot`, `HashedStack`, `HashOps` dropped from
  *Where to look*. **`chat-and-signing`**: the `Component` section
  replaced by a pointer paragraph; "new-shaped in 26.2" cut (rule 3).
  Wording left rough on purpose: the seven Part II hooks all end their
  opening paragraph on a bold or dashed sentence — one voice, seven times;
  the comparison and pattern pages carry long table cells that pass 5 may
  want as prose; `what-this-book-skips` still says "the part that
  surprises" where it used to say "the fact worth knowing".

- **2026-09-02, session B — maps.** The four atlas pages and the atlas
  front page are new prose and carry the em-dash chains the corpus is
  prone to; `packages.md`'s part → packages table will duplicate the
  landing pages once all thirteen exist and is a candidate cut then;
  `hierarchy.md`'s *two trees the table shows and the figures do not* is a
  two-sentence section and should either grow a figure or fold into the
  tables' preamble; "the number" device is used once (`biggest.md`) —
  check it reads as intended. Nothing was cut from the old maps: the
  tables are all still there under the figures, at the same URLs.

- **2026-09-03, session G — Part VI Entities.** *Cuts, all of them moves or
  logged losses.*
  **`entity-anatomy`**: the seven-group field inventory and the "smaller
  state families" paragraph (fire, freezing, fluids, portals, naming,
  item-component views) go — the names survive only where the story touches
  them, mostly as the contents of `Entity.baseTick`; the hand-drawn class
  tree is replaced by the atlas's generated SVG, taking the eighteen-name
  list of non-living direct subclasses with it; `Entity.MAX_ENTITY_TAG_COUNT`
  versus the literal 1024 (true, earns nothing on a map page); the
  `Entity.RemovalReason` four-way flag breakdown, **moved to
  `entity-lifecycle`**; `Mob.serverAiStep` being final and alternating on
  `tickCount + id`, **moved to `ai-goals-and-brains`**; `Marker.tick` being
  genuinely empty. The subpackage table stayed and its counts were corrected
  — the old rows summed to 639 of a stated 716.
  **`entity-lifecycle`**: the nineteen-constant `EntitySpawnReason` list
  (four survive, the rest want Reference — logged in pass3.md); the
  `SpawnPlacementTypes` list, folded into a cast row; the game-rule and tag
  roster from *Data-driven by*; and — the largest deliberate cut — the
  **Nether-fortress hard-coded spawn list and `Structure.spawnOverrides`**,
  which are verified true and are now stated **nowhere in the corpus**.
  Session M or O should take them.
  **`synched-entity-data`**: the 43-constant serializer bullet (74 lines) to
  the generated Reference page, leaving three named in prose; the
  `defineId`/`defineSynchedData`/setter roster; the thirty-five-overrider
  list, cut to three examples; `ServerEntity.Synchronizer` compressed to one
  table cell.
  **`attributes`**: the forty-constant catalogue (five themed bullets, 34
  lines) to the generated Reference page, with the count, the clamp rule,
  the eight non-syncable names and the handful of numbers the argument uses
  kept in prose. `Attributes.DEFAULT_ATTACK_SPEED` cut outright because the
  claim about it was false.
  **`movement-and-collision`**: the position-and-teleport family
  (`Entity.absSnapTo`, `Entity.snapTo`, `Entity.setOldPosAndRot`, the
  ±3.0000512E7 clamp, `Entity.setBoundingBox`'s public callers,
  `Entity.getKnownMovement`, `Entity.flyDist`) — these are
  `entity-anatomy`'s or `authority`'s and are currently on **neither**;
  half the outbound packet list and the whole inbound one, which
  `input-to-movement` owns; the data-driven tag inventory.
  **`ai-goals-and-brains`**: the behaviour-package roster cut to eight named
  classes plus a count; `VillagerType`.
  **`damage-and-death`**: the exhaustive `DamageTypes` key list and the
  fifteen-name `DamageTypeTags` list, replaced by the counts (51 and 35)
  with each tag named where it acts — both are Reference material and
  **neither Reference page exists yet**; `DamageSources` pre-building the 25
  entity-less sources; and the *Interfaces* inventory as a category, taking
  with it `Entity.thunderHit`, `LivingEntity.kill`, `/kill` and `/damage` as
  named callers, `CriteriaTriggers` and `Stats` as consumers,
  `MobEffectInstance.onMobHurt`, `ItemStack.hurtAndBreak`,
  `DataComponents.DAMAGE_RESISTANT`, and the two combat-status packets —
  all of which are now **nowhere**. The one substantive cut that needs a
  home is the **fall-attribution threshold** (`CombatTracker` credits a fall
  only when the best one exceeds five, and credits the *previous* entry when
  the fall was not the first — the source of *was doomed to fall by*): it is
  death-*message* machinery rather than damage, and wants a `CombatTracker`
  or death-message Reference page. Also found and deliberately **not** added:
  world-border damage is player-only.
  `damage-and-death` is 395 lines against the 240–390 target, and its
  drafter's verdict is that getting under 390 now costs a claim rather than
  words.
  *Wording debt.* `ai-goals-and-brains` is 420 lines against a 240–390
  target — the comparison table, the `Brain.tick` flowchart and seven
  difference sections cost more than the dissolved bullet walls saved; its
  own drafter names the *Questions players ask* section as the cheapest
  honest cut. **Six** of the nine pages ended on a *Questions players ask*
  section, which is one device used six times in one part and is exactly
  the "second uniformity" risk the charter names. The session renamed three
  of them to headings that say what the section says — *Three things about
  the id*, *What the four predicates explain*, *Why mobs look stupid* —
  leaving three; the question-and-answer form underneath is unchanged, and
  pass 5 should decide whether the form itself wants varying. Session P
  should check the device's distribution across all thirteen parts. The part's hooks all land on a bold or em-dashed final sentence,
  the same tic session C logged for Part II.

- **2026-09-03, session H — Part VII Items and inventories.** Eight pages,
  318–391 lines. **Nothing was cut except by moving it**, but a lot of
  *names* left the pages when the field inventories went, and this is the
  list, because the class index is now their only home.
  **`containers-and-menus`**: the `Container` interface roll-call
  (`Container.getContainerSize`, `Container.removeItem`,
  `Container.startOpen` / `stopOpen`, `ContainerUser`), the guarded
  mutations (`Slot.safeInsert`, `Slot.safeTake`, `Slot.tryRemove`,
  `Slot.safeClone`, `Slot.onQuickCraft`, `Slot.isFake`), the `Slot`
  subclasses (`ArmorSlot`, `FurnaceFuelSlot`, `NonInteractiveResultSlot`,
  `ShulkerBoxSlot`), the `Inventory` slot constants, the
  `AbstractContainerMenu` field list and
  `AbstractContainerScreen.checkHotbarKeyPressed`.
  **`recipes`**: the `Recipe.CommonInfo` / `Recipe.BookInfo` codec-fragment
  paragraph, `NormalCraftingRecipe`'s memoisation, the seven `RecipeType`
  constants enumerated, the `RecipeInput` three shapes
  (`SingleRecipeInput`, `SmithingRecipeInput`), the
  `Registries.RECIPE`-is-a-key-only note, the eleven `SlotDisplay` variants
  and the five `RecipeDisplay` class names (both now counts plus the
  exotic ones), and two recipe-book packets
  (`ServerboundRecipeBookSeenRecipePacket`,
  `ServerboundRecipeBookChangeSettingsPacket`).
  **`enchantments`**: ten of the fifteen entity-effect class names,
  `Enchantment.getFullname`. **`loot-tables`**: `LootDataType`'s three
  constants enumerated, `ContainerEntity.unpackChestVehicleLootTable` and
  the minecart parallel, `LootCommand` and `ItemCommands.applyModifier`
  (all three moved with the caller table to `contexts-and-predicates`), and
  `Registries.LOOT_TABLE` — now only implied through
  `ReloadableServerRegistries`, which pass 5 may want named once.
  **`using-an-item`** deliberately left the full `Item.getUseDuration`
  override roster (`BrushItem`, `BundleItem`, `EnderEyeItem`,
  `InstrumentItem` and their numbers) to nobody: neither it nor
  `items-and-stacks` now carries it. It is a Reference-page candidate or a
  sentence; it is currently lost prose, and this is the record of it.

  **Length.** Every page is over the 200–320 brief: 318, 324, 332, 344,
  346, 358, 389, 391. Five agents reported trimming twice and stopping
  rather than cutting evidence. Part VII is now the longest part per page
  in the corpus and is where pass 5's cutting should start.

  **Wording.** `enchanting`'s comparison table and
  `contexts-and-predicates`' caller table both carry long cells that want
  to be prose. `using-an-item`'s two sequence diagrams are deliberately
  isomorphic, which is the right call for the comparison but makes the
  page's second half read as a repeat — worth a voice pass. Only
  `loot-tables` reached for *Questions players ask*, so session G's
  uniformity risk did not recur here; the eight section-heading sets are
  genuinely different from one another, which is the test.

- **Session I (Part VIII), 2026-09-03.** **Length**: 316, 174, 410, 285, 231,
  250, 176 lines plus a 115-line landing page — six of the seven inside or
  near the 200–320 brief, which is the first time in pass 3, and the splits
  are why. The exception is **`input-to-movement` at 410**, which was not
  split and now carries the longest single section in the part (the server
  half of the trace); it is the part's first candidate if pass 5 wants a cut
  or a split.
  **Cuts and losses, recorded.** The old `player-anatomy` bullet inventory of
  `Player`'s fields became a three-column table; nothing was dropped, but the
  table's middle column is dense and is a candidate for prose or for the class
  index. `hunger-xp-and-effects`' opening headline about `GameRules`' package
  (`world/level/gamerules`, typed `GameRule` lookups) survives only as a
  clause in `hunger-and-experience`; it was a Reference fact wearing a hook's
  clothes. Two `the-sword-swing` sentences about `DataComponents.MINIMUM_ATTACK_CHARGE`
  and `DataComponents.DAMAGE_TYPE` as *the rest of what makes an item a
  weapon* were absorbed into `the-spear`'s component table, so the sword page
  no longer names `MINIMUM_ATTACK_CHARGE` at all.
  **Wording.** `input-to-movement` is the page most obviously mid-conversion:
  its two data subsections are still a bullet wall under a renamed heading,
  and the *what it calls, and what crosses the wire* section is the old
  Interfaces list with a new title. It is the first place a pass-5 voice pass
  should go in this part. `the-spear` uses *stab* and *charge* as the two
  path names throughout; if pass 6 disagrees with those words, they are the
  page's whole vocabulary and change everywhere at once. Three pages now open
  with the second person (*you press W*, *you open your own inventory*, *you
  drink a potion*), which reads well here and is worth a corpus-wide decision
  rather than a per-part accident.

- **2026-09-03, out of band — the licence footer says it twice on one page.**
  `site-footer.js` puts the disclaimer and the CC BY-SA line on every page,
  and the introduction now also closes on *Unofficial, and free to reuse*,
  which says the same two things in prose. Everywhere else the footer is the
  only statement and reads as small print; on `introduction` alone it is a
  restatement two inches below the section it restates. Cheapest fix if pass 5
  agrees it grates: have the footer skip the introduction (it is the one page
  guaranteed to carry the prose version), rather than cutting the prose —
  the prose is what reaches an agent through `llms-full.txt`, which the JS
  footer never does. Not urgent; nobody has complained, and duplication in
  favour of the licence being visible is the right way round to err.

- **2026-09-03, pass 3 session J — what Part IX's reshape cut.** Logged per
  R7: nothing left a page except by moving or by this entry.
  **From `the-connection`** (550 → 442 lines), all of it enumeration the
  budgets no longer allow and none of it load-bearing: the sixteen
  `HandlerNames` constants named one by one (the class survives, and so does
  the fact that nothing references some of them); the packet-rate smoothing
  constant and its lerp fraction; `Connection.intendedProfileId` with its
  setter and the observation that `ServerConnectionListener.acceptChannel` is
  its only assignment and is itself uncalled; the method-by-method tour of
  `PacketListener`; `ServerConnectionListener.getSessionId`, its two stop
  methods and the *Open to LAN* note; `ServerConnectionListener.LatencySimulator`;
  the five `TickablePacketListener` implementors listed by name (the
  interface's role survives in the cast); and five `Connection` accessors
  named as names. If pass 6 misses any of these, the class index still has
  them and `reference/packets.md` is the catalogue.

- **2026-09-03, session J, the rest of Part IX's cuts and its wording debt.**
  From `what-the-client-is-told`, replaced by naming only what the story
  touches: the `ServerEntity` field list (`lastSentYRot`, `lastSentXRot`,
  `lastSentYHeadRot`, `lastPassengers`, `wasRiding`, `wasOnGround`) and the
  `PlayerChunkSender` field list. Two facts were cut as *duplicates*, not
  losses — the tick-long flush suspension (owned by `the-connection`) and the
  `ChunkMap.MIN_VIEW_DISTANCE` clamp (owned by `tickets-and-loading`'s send
  table) — and both now link instead. The `ClientboundTeleportEntityPacket`
  invariant was not cut: it moved into the page's *for a 1.21-era reader*
  blockquote.
  **Wording debt.** Three of the four rewritten pages open in the second
  person (*you swing*, *you stop the message on its way out*, *someone says
  hello*), which continues the drift session I flagged in Part VIII — the
  corpus-wide decision on the second person is now overdue and would touch
  three parts at once. `chat-and-signing` uses *message*, *chain* and
  *connection* as the names of its three failure outcomes throughout, in the
  prose, the flowchart and the eighteen-row table; if pass 6 disagrees with
  those three words they change everywhere at once, exactly as
  `the-spear`'s *stab* and *charge* do. And `the-connection` and
  `packets-and-stream-codecs` both call the codec table *the phase's one
  codec*, which is precise but is the sort of phrase a viewer hears as a
  singular file rather than a composed dispatcher.

- **2026-09-03, session K, Part X's cuts and its wording debt.**
  **Cuts, all of them moves rather than losses.** `hud`'s twenty-eight-row
  element gate table, which pass 2 had compressed to a paragraph of prose,
  is now `src/reference/hud-elements.md` and the page links to it — the page
  keeps only the two-block *shape* as a flowchart. `the-client-loop` lost its
  *data it owns* field inventory (the timing fields, the profiler apparatus,
  the gizmo collectors) and its *interfaces* list; every field the story
  touches is still named in the sentence that touches it, and the rest is in
  the class index. `the-client-level` lost the same kind of inventory, and
  `prediction-and-acks` lost its enumeration of
  `BlockStatePredictionHandler`'s eight public members as a list — three are
  still named in *Where to look*. Nothing factual was dropped except one
  stale framing sentence in `sound`, which called the sound system "the first
  system after Anatomy"; the lecture order it referred to no longer exists.
  **Wording debt.**
  - **The formula sweep is now overdue and Part X is where it is worst.**
    Session H recorded that three Part X pages opened with "The headline for
    a 1.21-era reader" and four with "The one sentence a player would
    recognise"; session I found Part XI eight for eight. This session
    removed both formulas from all twelve Part X pages — the headline
    material became the *for a 1.21-era reader* blockquote at the foot of
    each page, and the player-recognises sentence was folded into the
    opening paragraph or the verified line. **The formulas now survive
    nowhere in Part X and everywhere in Parts XI to XIII.** Sessions L to N
    should do the same, or pass 5 will be reconciling three different house
    styles.
  - **The *questions players ask* device is now doing a lot of work.** Six of
    the twelve pages use it, because it is the honest home for what used to
    be a bullet wall of invariants. That is one page in two, which is the
    same trap the old seven-heading template fell into. Pass 5 should check
    whether it reads as a device or as a section every page must have — and
    note that on three pages (`the-gui-render-tree`, `text-and-fonts`,
    `sound-engine`) the questions are a reader's rather than a player's, and
    the heading says so, which may be a distinction without a difference.
  - **Second person again.** `input-and-keybinds`, `hud`,
    `what-makes-a-sound` and `the-gui-render-tree` all open in the second
    person (*hold the key*, *press F1*, *you break a block*, *a chest full of
    the same item*). Sessions I and J both flagged the drift; it is now four
    parts wide and the corpus-wide decision cannot wait for pass 6.
  - **`the-gui-render-tree`'s title is still the weakest in the part**
    (session H's note, unresolved). It is really *how the UI is recorded and
    drawn*, and the tree is the mechanism rather than the subject. Not
    renamed this session because a rename costs a redirect and the page's own
    figure now makes the tree the point; pass 5 or pass 6 should settle it.
  - **"Record" and "extract" are used interchangeably across four pages** —
    `gui-and-screens`, `the-gui-render-tree`, `text-and-fonts` and `hud` —
    because the methods are all named *extract* and the concept reads better
    as *record*. The glossary has *extract*. One of the two should win.

## Session N — Part XIII Commands and data packs *(2026-09-03)*

**Cuts, with reasons.** Nine pages from five, and the reshapes dropped
material rather than moving it in these places. None of it is wrong; all of
it lost a fight for space against the page's own story.

- `brigadier-and-commands` lost: `CommandSource` as a named object (the
  output end alone — `CommandSource.NULL`, `CommandSource.acceptsSuccess`,
  `CommandSource.shouldInformAdmins` — and the observation that a command
  block, RCON and the console differ *only* there);
  `Commands.CommandSelection` gating which commands exist at all on an
  integrated versus a dedicated server; `CommandSourceStack`'s fourteen-field
  inventory; the roll-call of the resource-argument family
  (`ResourceArgument`, `ResourceKeyArgument`, `ResourceOrIdArgument`,
  `ResourceOrTagArgument`, `ResourceSelectorArgument` and which of them takes
  a glob); and the note that `IdentifierArgument` is the class a 1.21 reader
  knows under another name, which `reference/naming-drift.md` owns anyway.
  The `CommandSource` row is the one worth restoring if the page ever has
  room — it is the whole answer to "why does a command block not spam chat".
- `advancements` lost: the two `Advancement.validate` methods (a private
  static one the codec runs, which cross-checks requirements against criteria
  and **fails the load**, and a public one that walks each trigger instance
  through a `ProblemReporter` and only *warns*); `AdvancementTree.remove` as
  the recursive counterpart the client uses for the packet's removed ids;
  `ServerAdvancementManager` as a `SimpleJsonResourceReloadListener` over
  `Registries.ADVANCEMENT`, with the JSON parse off-thread and the tree build
  and layout on the reload's main-thread executor; `AdvancementRewards.grant`
  rolling its tables in the `LootContextParamSets.ADVANCEMENT_REWARD`
  context; `DisplayInfo`'s field inventory; and the two call-site counts
  ("seventy-nine gameplay sites across forty-nine files",
  "`AdvancementCommands` is 312 lines"). The reload-listener sentence is the
  loss that matters — the page now says the layout runs on the server without
  saying *when*.
- `the-execution-engine` lost `ExecutionControl` and the
  `EntryAction` / `UnboundEntryAction` pair as named cast rows; both are now
  only implied by `CommandQueueEntry`'s row.
- `scoreboard-and-data` lost: `PlayerScores` (package-private, and the
  observation that `Scoreboard.resetSinglePlayerScore` deletes the whole row
  so the outer map never accumulates empties); `TeamColor`'s sixteen values
  and the unrelated second `TeamColor` in `client/color/item`;
  `DisplaySlot`'s nineteen enumerated; `ScoreHolder.fromGameProfile`; and the
  command-class sizes (`ScoreboardCommand` at 620 lines is the fourth-largest
  command class in the game, which was a nice number).
- `dialogs` and `game-tests` lost the individual names of six packets
  (`ClientboundClearDialogPacket` survives; `ClientboundTestInstanceBlockStatus`,
  `ServerboundSetTestBlockPacket` and `ServerboundTestInstanceBlockActionPacket`
  are now described rather than named). `reference/packets.md` has them.

**Wording debt.**

- **Second person is now five parts wide and past arguing about.** Every one
  of this part's eight content pages opens in it — *type a slash*, *op
  yourself to four*, *write a data pack*, *put a `$`-prefixed line*, *mine a
  stone block*, *look at the sidebar*, *you click a server*, *run
  `/test runall`*. Sessions I, J and K all flagged the drift as a question;
  session N used it deliberately on every page because the shape of the
  opening paragraph the template asks for (*start inside the scenario*)
  pulls hard towards it. Pass 5 should ratify it or reverse it corpus-wide,
  not page by page.
- **The *questions players ask* device is on three more pages** —
  `advancements`, `scoreboard-and-data`, and `the-execution-engine` where it
  is called *questions a data-pack author asks*. That is session K's warning
  coming true: the device is becoming the standard home for what used to be
  the invariant wall, and a corpus where half the pages have one has just
  re-invented the seven-heading template with better headings. Count them in
  pass 5 and cap it.
- **"The one sentence a player would recognise" is gone from all five old
  pages** and was not replaced by anything with a fixed position — the
  recognisable thing is now inside the opening paragraph where it belongs.
  Worth checking the earlier parts still do the same.
- `the-execution-engine` and `functions-and-macros` both explain
  `ContinuationTask.schedule`. The engine page owns the arithmetic and the
  functions page owns the consequence ("a hundred-line function and a
  hundred-player fork are the same shape"), which is one sentence of overlap
  and deliberate — but it is exactly the kind of duplication pass 5 hunts.
- `permissions` and `brigadier-and-commands` both describe the command-tree
  packet, deliberately from two sides (shape versus gating). Read them
  together once for a seam that reads as a repetition.

## Session O — Reference *(2026-09-03)*

- `level-data-and-rules` was reshaped bullet-for-paragraph, so its
  paragraphs are still inventories in prose clothing (the `PrimaryLevelData`
  field list, the `DimensionType` record). A reference page may keep them;
  a polish pass should decide whether the two longest become tables.
- `math-and-primitives`' *What trips people up* is nine bold-led paragraphs
  where the list was; the ninth (`BlockUtil` is in `util`, not `core`) is a
  naming-drift row wearing a surprise's clothes and could move to that
  page.
- `naming-drift` keeps its second-person "the name in your head" voice,
  which is now the only page in Reference that talks to the reader; keep or
  level in the voice sweep.
- `reference/README.md`'s table has a *parts* column written by hand from
  the landing pages; if a tool ever writes it, the column goes generated.
- The glossary's owner links are one page each except *Component*,
  *Level*, *Render state*, *Tick*, *Quart* and *Submit node*, which point at
  two; a polish rule should say whether two is allowed.

## Session P — The lecture order and the close *(2026-09-03)*

The charter asked session P to check the distribution of page shapes ("if
half the corpus chose the trace, the menu failed") and the *Questions
players ask* device's spread (sessions J and M each flagged it in their
part). Two agents classified all ninety-eight system pages by the menu's
rubric — primary shape from the spine, secondary from the borrowed section,
first figure's type, and whether the page ends on a questions section — and
the session read their evidence lines against the pages' headings.

**The menu held.** Primary shapes over ninety-eight pages: **trace 31 ·
vocabulary 25 · pipeline 17 · comparison 10 · policy 7 · pattern 6 · state
machine 2.** The trace is a plurality at just under a third, not the
majority the risk named; the vocabulary page is the surprise at a quarter,
and three of those (`tags`, `signal-and-dust`, `synched-entity-data`) lead
with a figure that belongs to a different shape than their spine. The state
machine is the least-used shape, and the two that exist are both in Part
IX/X (`protocol-phases`, `prediction-and-acks`); Parts I–VII have none as a
primary although three of their pages carry a `stateDiagram` as a secondary
figure (`points-of-interest`, `entity-lifecycle`, `tickets-and-loading`).
Pass 5 should ask, page by page, whether a secondary state diagram is the
page's true picture.

**The closing device did not hold.** Sixty-three of ninety-eight pages end
on a questions section (sixty *Questions players ask* verbatim, three
*Questions a reader asks*, one *Questions the pattern raises*, one
*Questions a data-pack author asks*) and four more carry one that is not
last (`what-the-client-is-told`, `the-client-level`, `advancements`,
`the-execution-engine`). By part: I 1/2 · II 6/7 · III 2/5 · IV 10/10 ·
V 7/7 · VI 3/9 · VII 2/8 · VIII 7/7 · IX 4/5 · X 8/12 · XI 6/10 · XII 8/8
· XIII 3/8. Parts IV, V, VIII and XII use it on every page. This is a
*device* become a *slot*, exactly the second-uniformity risk the charter
named, and it happened for the reason session J gave: the section is the
honest home for what used to be the invariants wall. **Rule of thumb for
pass 5: at most half the pages in a part end on it**, and on the others
the same question-and-answer material either dissolves into the section
where the answer happens (session G's precedent — *Three things about the
id*, *Why mobs look stupid*) or takes a heading that says what the section
says.

**Seven pairs of pages share a skeleton**, which the charter says means
neither is done. Within one part: `server-tick` / `server-level-tick`
(deliberate mirroring — the outer and inner loop — but the tables of
contents are hard to tell apart); `starting-a-server` / `how-a-server-dies`
(one skeleton run forwards and backwards); `chunk-generation-pipeline` /
`chunk-storage` / `scheduled-ticks` (three pipelines: lead flowchart,
per-stage sections, a named trace late, questions); `block-breaking` /
`block-interaction` (both are applications of the same ledger and the
shape does not distinguish them); `attributes` / `synched-entity-data`;
`enchanting` / `using-an-item`; `biomes` / `features-and-placement` /
`jigsaw-and-templates` (Part XII: cast → *The trace: X* → two or three
detail sections → questions → where to look, only the nouns change);
`the-spear` / `the-sword-swing`; `hud` / `options` / `input-and-keybinds` /
`the-gui-render-tree`; `blaze3d` / `section-meshing` / `the-frame` /
`the-window`. Across parts: `data-components` / `text-components` /
`items-and-stacks` (one skeleton three times), and `the-client-loop` /
`the-frame` (one turn of a loop, zones named, what falls off the end — kept
apart mainly by one being a flowchart and the other a sequence). Pass 5
varies one of each pair; the shape need not change, the skeleton must.

**The literal heading `## The trace: …` is on twelve pages** in four
parts (VIII ×4, XII ×4, XIII ×4 — `input-to-movement`, `status-effects`,
`the-sword-swing`, `the-two-phase-tick`, `biomes`,
`features-and-placement`, `hand-built-structures`, `jigsaw-and-templates`,
`advancements`, `dialogs`, `game-tests`, `scoreboard-and-data`), which is
a template slot's name and breaks the *headings say what the section
says* rule from `TEMPLATE.md`. Each wants the scenario as its heading.

**Two structural outliers**, for the same sweep: `functions-and-macros`
has no cast table (it opens on *The pipeline*), and `hand-built-structures`
buries its cast inside *The idea* — both differ from every other page in
their part, and either is fine if it is deliberate.

**Wording debt from the four session-P pages.** All four were drafted by
Opus agents against the shared brief and accepted after the session
re-derived their sharpest claims; none was cut. `block-entity-rendering`
(332 lines) is a comparison whose three-column table is the figure and
whose *why* column on the view-distance table is editorial — pass 5 should
decide whether an inferred reason belongs in a table cell; its
1.21-reader blockquote is eleven lines, the longest in the corpus.
`entity-selectors` (313 lines) ends on *Questions a command author asks*,
the fourth spelling of the device; its twenty-one-row option table is
under budget only because three rows fold *x, y, z* and *dx, dy, dz* and
the rotations together. `blending` (346 lines, the longest of the four and
over the brief) ends on *Questions players ask* — Part XII is now 9 of 10
on the device — and its opening paragraph carries two numbers ("roughly a
hundred blocks", "a hundred and ninety-three") before the reader knows what
a column is; consider moving the 193 down to the *Two maps* paragraph
where it is explained. `creating-a-world` (300 lines) has a
three-column comparison table whose *Re-Create* column is the argument;
the paragraph after the sequence diagram ("Three details in that order are
worth stopping on") is a list in prose clothing and could be three
bold-led paragraphs. All four use the *For a 1.21-era reader* blockquote;
none uses the myth table; three carry a *Questions* closer, so the
session's own pages score 3 of 4 on the device it just flagged.

## From pass-4 session H — Part VIII The player *(2026-09-04)*

**Openings rewritten around a corrected fact — re-read for voice:**

- `status-effects` — the hook was "The client never runs a status effect …
  and that is all", which is false of the movement consequences. It is now
  "The client never runs a `MobEffect` hook", followed by three named
  unguarded reads (`getJumpBoostPower`, the slow-falling gravity clamp,
  levitation in `travel`). The paragraph is longer and the "and that is all"
  cadence is gone; find a shorter shape that keeps the distinction.
- `player-anatomy` — the *whose game mode arrives late* question was
  inverted and is now roughly twice as long, because the true version has to
  say why the other player's window cannot be observed before it can say the
  window is yours. It reads as an argument rather than an answer.
- `the-two-phase-tick` — the Netty-threads paragraph grew from an absolute
  plus a throwaway ("a handful that touch nothing") to a count plus an
  exception plus the chat mechanism. Correct, but it is now the longest
  paragraph in a short section.
- `the-spear` — the *different windows* payoff sentence was replaced by its
  mirror image with the wooden spear's 5/10/15 as illustration. Check the
  numbers earn the extra clause.

**Structural findings (not acted on):**

- `status-effects` names `LivingEntity.effectsDirty` and never says what
  reads it. The consumer is `updateDirtyEffects` ← `updateDataBeforeSync` ←
  `ServerEntity`, i.e. the server's entity-sync pass — which is the actual
  mechanism behind the page's own "swirls and no numbers" answer. Naming a
  field with no reader is the pattern; either say what reads it or drop it.
- `status-effects` lists `MobEffectCategory` in *Where to look* and never
  explains it, though it is why the HUD splits icons into two rows.
- `status-effects` — `MobEffectInstance.compareTo` orders the HUD icons
  reversed and the inventory list un-reversed, so the two surfaces list
  effects in opposite orders. One clause, and it is the kind of thing a
  player notices.
- `the-sword-swing` — `LivingEntity.getSecondsToDisableBlocking` is
  presented as an unconditional read-back; it returns the `Weapon` value
  only when the weapon is also the attacker's *active* item.
- `the-spear` — the component table is headed "every component that makes
  one" (now softened to "the combat components"); the durability three,
  `REPAIRABLE` and `ENCHANTABLE` are still absent. Either the table is
  complete or the header says which subset it is.
- `input-to-movement` — "floating" is used without ever defining the
  condition `clientIsFloating` records, and the jump-inference paragraph sits
  before the field it depends on is introduced.
- `player-anatomy` — the page says `Avatar` "exists for the renderer", but
  `Avatar` is a server class whose other content is the shared player hitbox;
  the renderer is one consumer, not the reason.

## From pass-4 session I (Part IX Networking), 2026-09-04

Wording debt from fixes made in place, and structural findings not acted on.

- `networking/README.md` — the opening's four player-visible failures now
  ends on "a grey bar down its left edge", which is true and duller than the
  red line it replaces. The vivid true version is the *sender's* side —
  `handleMessageDecodeFailure` sends the reason back in red — but that is a
  different sentence about a different player. Re-read the paragraph whole.
- `networking/README.md` — "one wire and three passengers" is still the
  part's shape sentence, and the page contradicts it twenty lines later by
  saying *protocol phases* **is** the wire rather than a passenger. Pass 4
  softened the first sentence rather than choosing; the shape needs deciding.
- `networking/README.md` — the traffic-volume clause added to the *shape*
  section is a fact the section did not previously carry, and reads like a
  footnote. It may belong in *what the client is told* instead.
- `the-connection.md` — the `HandlerNames` paragraph existed to deliver "a
  complete and correct index that no code reads". The index turned out to be
  incomplete, so the paragraph now delivers "an index that has already
  drifted", which is a different and slightly weaker point occupying the same
  space. Consider cutting it to one clause.
- `the-connection.md` — the kick answer is now four sentences where the
  question deserves two. The mechanism took three of them.
- `packets-and-stream-codecs.md` — the "three shapes of packet class"
  paragraph now names all three, and the third (the `StreamCodec.unit`
  singleton) is introduced twice on the page, here and in the bundle section.
  Pick one home.
- `packets-and-stream-codecs.md` — the JSON exception is now a four-line
  aside inside a paragraph about the NBT bridge. It is a good fact and it is
  in the wrong shape; it may want to be its own short paragraph.
- `protocol-phases.md` — "Eight, not four: every phase but handshaking
  declares one per direction" is a correction written as prose. Pass 5 should
  fold the number into the sentence and drop the correction voice.
- `what-the-client-is-told.md` — "Four feeds ignore gate 3" now carries a
  second sentence walking back the scope, and the section heading still says
  *What goes out around the gates*. Heading and content disagree in emphasis.
- `chat-and-signing.md` — the unsigned-`Component` paragraph grew by four
  lines to hold the `MessageArgument` finding, which is the best fact on the
  page and is buried in a paragraph about a field. It may deserve promotion.

Structural findings, not acted on:

- `reference/threads.md` — the never-hop section's population is stated as
  "`ClientPacketListener`", a class, when the honest population is "the
  handlers a client play listener runs". Pass 4 fixed the count and left the
  framing; a Reference section whose population is a class file rather than a
  runtime object will drift again the next time a handler moves up or down
  the hierarchy.
- `networking/README.md` figure — arrows 3 and 4 (`PP → WCT`, `PP → CS`)
  assert a dependency neither target page uses. Pass 4 corrected the prose
  that made the same claim and left the arrows, because the figure is the
  part's watch order rather than a prerequisite graph. If the shape sentence
  above is redecided, the arrows go with it.

### Part XIII, after session M of pass 4 *(2026-09-05)*

Wording debt, all of it created by a fact fix:

- `brigadier-and-commands.md` — the **hook and the whole round-trip section
  were rewritten**, because the page's central claim ("the round trip is not
  the fallback, it is the default") was backwards and its verified-line
  scenario asks the server nothing. The replacement carries three numbers —
  359, 64, 59 — where the old one carried two, and the "why they feel like
  all of them" turn is doing a lot of work in one clause. Pass 5 should read
  the opening and the *A node that asks for suggestions by hand* section
  together and decide whether the argument now takes one paragraph too many.
- `entity-selectors.md` — the **opening scenario was replaced** (a command
  block, because a player typing `/tp @p` always selects themselves) and now
  carries a parenthetical explaining why the obvious version does not work.
  The parenthetical is a correction in the voice of a correction; pass 5
  should either fold it into the paragraph or cut it.
- `entity-selectors.md` — the orphaned "**Four** —" paragraph is now a
  four-line "the query plan is written by eight of the twenty-one names"
  paragraph. It is accurate and it is the third place on the page that
  enumerates the box options. Pass 5 should decide which of the three keeps
  the enumeration.
- `functions-and-macros.md` / `permissions.md` — the union paragraph on both
  pages grew to hold the level-based-versus-not distinction, which is a real
  and necessary qualifier and reads like a footnote promoted into the body.
  The fact belongs on `permissions`; `functions-and-macros` may be able to
  cite it in a clause.
- `permissions.md` — *Asking a question the client cannot answer* now says
  three things the section did not previously have to say (the sign is not on
  this path; `NO_ISSUES` sends silently; the client checks permissions in
  several other places). The section's own punchline — that the client can
  tell "no permission" from "typo" — is now the fourth idea in it.
- `scoreboard-and-data.md` — the "one thing this corpus cannot settle"
  paragraph became an answer, so a paragraph that existed to mark a limit is
  now a paragraph of fact sitting where a caveat used to close a section.
  Check it still belongs at the end.
- `game-tests.md` — the client-writes sentence now ends on a list of four
  serverbound packets that belong to other pages. True, and long. Pass 5
  should consider cutting it back to the narrow claim.
- `commands/README.md` — the *before you start* server-tick entry is now the
  longest of the five and names three classes, because the short version was
  wrong about which phase. It may be shortenable now that it is right.

Structural findings, not acted on:

- `entity-selectors.md` — the page is one of the longest in the part and its
  *Resolve* section carries five bolded claims in a row, three of which are
  about cost rather than about the trace. The page's shape is a pipeline with
  a policy figure; the cost material may want to be a table.
- `commands/README.md` — the part's size sentence now needs nine package
  names to be reproducible and gives none, which is what let a wrong pair
  stand through two passes. Every other landing page has the same shape. A
  standing fix would be for the atlas to generate the per-part totals rather
  than each landing page hand-counting them — that is a tooling change, and
  it belongs to whoever revisits `map_source.py`.
