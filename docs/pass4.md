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

- ~~The landing pages and `lectures.md` are claims about order and
  dependency: check that every *before you start* link is actually assumed
  by the part, and that nothing earlier depends on something later.~~ Done
  in full by session A (2026-09-04); `tools/check_deps.py` is the fourth
  deploy gate and green, and the six remaining report-only entries are
  judged in session A's entry below.
- Every redrawn diagram: arrow by arrow, and every tick-boundary bar.
- ~~The eight generated Reference views (pass 3 added serializers,
  attributes, enchantment hooks and loot-context sets to the four pass 2
  had; the glossary stayed hand-kept): re-derive one sample by hand per
  view — pass 2 found bugs in both generators, and one had reached the
  prose.~~ Session A re-derived one sample and one population count per
  view; all eight confirmed (listed in its entry below). The hand-written
  *blurbs* on those pages are not generated and are not covered by this —
  their counts go to session N.
- ~~The lane key in `TEMPLATE.md`: every lane's expansion is a class that
  exists.~~ `tools/check_lanes.py` checks it on every deploy, `--strict`
  corpus-wide since session P.
- **Every count is re-counted** (session P's addition 4 in the charter):
  pass-3 sessions K, L, M and N each found a wrong count while redrawing a
  page, three of them load-bearing. Session N of pass 4 is a corpus-wide
  count sweep with one brief.
- **The four session-P pages have never been checked** —
  `rendering/block-entity-rendering`, `commands/entity-selectors`,
  `worldgen/blending`, `worldgen/creating-a-world`. Their claims lists are
  under session P's entry; they get pass 2's completeness question too.
- **The parts-dependency figure** (`src/figures/parts-dependency.md`,
  included by the introduction and `lectures.md`) and the dependency table
  on `lectures.md` are claims: every arrow is a landing page's *before you
  start* entry, and every entry must be used by a sentence in the part.
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
  `brigadier-and-commands`, `the-execution-engine`, `functions-and-macros`
  and `scoreboard-and-data` (parse, suggestions, `ContextChain`, the result
  consumer), `models-and-atlases` and `text-and-fonts` (the atlas and font
  JSON), and `post-processing` (the six chains' JSON).
- **The `execute store` question** on `scoreboard-and-data` — what a failing
  ordinary leaf command writes — is now answerable from Brigadier 1.3.10;
  settle it and remove the page's "cannot be settled from the decompile"
  note.

- **The tooling reads this file** *(planning session, 2026-09-03)*.
  `tools/pass4_queue.py` cuts it into units (a heading, or a list item with
  its continuation lines) and gives each page every unit that names it as
  `` `slug` ``, `part/slug` or `slug.md`, plus every unit under a heading
  that names it; a unit that names no page is a *part-wide* note, routed by
  the session from `_part-notes.md`. So: **name the page in backticks when
  you write a note**, one page per line where you can, and **strike a
  settled line as `~~…~~` at the start of the line** — the tool drops
  struck units, so the next session's checklist is only what is open.
  Corrections logged by a pass-4 session go under a `## Session X — Part N
  (pass 4)` heading at the top of *Entries*.
- ~~**`tools/check_deps.py`'s first run** (2026-09-03) is session A's opening
  list: two lecture-table rows the landing pages do not support, three
  forward links with no dashed arrow, and per part the *before you start*
  entries no page in the part links or names — all in the plan's schedule
  line for session A.~~ All settled by session A; the checker is green and
  is now `deploy.sh`'s fourth gate.

## Entries

## Session G — Part VII Items and inventories (pass 4) *(2026-09-04)*

Eight pages and the landing page, one adversarial agent each; the order work,
the part-wide notes and every *wrong* re-derived by the session before a
sentence moved. **All nine had at least one wrong claim** — pass 2's result for
an eighth time. Sixty corrections. Session H's checklist held almost entirely
(every one of its nine pass-2 corrections re-confirmed, and most of its
introduced claims), so — as in Part VI — the errors were not where pass 3 knew
it had changed something.

### The four that carry a lecture

- **`enchanting`'s shared tail does not exist.** The section *The one line all
  five end on* rested on "All of them end at `ItemStack.enchant`", and three of
  the five do: the table (`EnchantmentMenu.java:191`), `/enchant`
  (`EnchantCommand.java:71`) and `EnchantRandomlyFunction` (`:93`). The
  grindstone and the providers call `EnchantmentHelper.updateEnchantments`
  themselves (`GrindstoneMenu.java:200,217`; `EnchantmentHelper.java:712`), and
  the **anvil is outside even that** — it builds an `ItemEnchantments.Mutable`
  and writes with `EnchantmentHelper.setEnchantments`
  (`AnvilMenu.java:138,291`). What all five *do* share is one private line,
  `EnchantmentHelper.getComponentType` (`EnchantmentHelper.java:91-93`), which
  both `setEnchantments` (`:84`) and `updateEnchantments` (`:63`) call — and it
  is the routing-by-item-identity the section was about, so the argument
  survives and the section is now named for the question rather than the
  method.
- **`loot-tables`' trace opens the wrong menu.** Figure 1 arrow 10 said
  `ChestMenu.sixRows`; a single chest — which arrow 1 establishes as the
  scenario — opens `ChestMenu.threeRows` (`ChestBlockEntity.java:229-231`,
  `getContainerSize()` = 27), and `sixRows` has exactly one caller in the game,
  `ChestBlock.java:111`, inside the **double**-chest anonymous provider. The
  arrow contradicted its own figure.
- **`contexts-and-predicates` undercounts its own keys, and the missing two
  make its argument.** "The fifteen that exist are the static fields of
  `LootContextParams`" — there are **seventeen** `ContextKey`s;
  `SlotDisplayContext.FUEL_VALUES` and `.REGISTRIES`
  (`world/item/crafting/display/SlotDisplayContext.java:12-13`) are the other
  two, and `SlotDisplayContext.fromLevel` builds a `ContextMap` from **six
  client files** (recipe book, stonecutter screen, recipe toast, search trees).
  So the page's *util/context knows nothing about loot* thesis has a second,
  client-side user it never named — and the cast table's "server main" for
  `ContextMap` was wrong.
- **`recipes`' reload window is not what the page says, and cannot be
  observed.** "Between the swap and that call the four derived indexes still
  describe the recipe set that was there before — a window that is short and,
  on a reload, real." A reload builds a **fresh** `RecipeManager`
  (`ReloadableServerResources.java:39`), whose constructor sets all four to
  their *empty* values (`RecipeManager.java:84-89`); and the swap
  (`MinecraftServer.java:1700`) and `finalizeRecipeLoading` (`:1706`) are five
  statements apart in one synchronous main-thread lambda.

### Two more punchlines fell

- **`items-and-stacks`' creative-slot door does not check contained sizes.**
  "`ItemStack.validateContainedItemSizes` makes it recursive … so a shulker box
  full of impossible stacks is rejected at the door" — the method is reached
  only from `ItemStack.validateComponents` (`ItemStack.java:245-288`), itself
  reached only from `ItemStack.validateStrict` (`:130-131`), which the same
  paragraph had just excluded from the network path.
  `ItemStack.validatedStreamCodec` (`:169-187`) re-encodes through
  `ItemStack.CODEC` and runs no validator. It is also one level deep, not
  recursive.
- **`enchantments`' "No other item can be made to behave like one" is false.**
  Only `EnchantmentHelper.getComponentType` keys on `Items.ENCHANTED_BOOK`.
  `ItemStack.java:924` puts `DataComponents.STORED_ENCHANTMENTS` in *any*
  stack's tooltip, and `AnvilMenu.java:145` sets `usingBook` from the
  **component**, not the item — which relaxes the same-item rule and halves the
  fee for anything carrying it.

### The order work (addition 2)

`check_deps.py` green throughout; Part VII had no *entries no page links* line.
All six *before you start* entries are used by a sentence, not merely linked:
`foundations/data-components` (`items-and-stacks:10`, `enchanting:77`,
`loot-tables:284`), `foundations/codecs-nbt-json` (`containers-and-menus:226`,
`recipes:255`), `foundations/identifiers-and-registries` and
`foundations/resource-system` (`contexts-and-predicates:318`, `recipes:37`,
`loot-tables:247`), `server/server-level-tick` (`containers-and-menus:277`) and
`blocks/block-interaction` (`containers-and-menus:35`, `loot-tables:91`,
`using-an-item:34`).

**One missing entry: `server/server-tick`**, added. `containers-and-menus`'
whole *Where in the tick a broadcast happens* section rests on "packets are
drained **before any level ticks**", which is `server-tick`'s fact, and
`lectures.md:239` already said Part VII assumes Part III — the landing page
listed only the level tick. Same finding as session E's on Part V.

Judged **pointers rather than dependencies** and left out: `foundations/tags`
(`enchanting:227`, `recipes:245` — two parentheticals), `blocks/block-breaking`
(`items-and-stacks:296`, `loot-tables:296`, `contexts-and-predicates:209` — all
*who calls this* pointers) and `blocks/block-entities`
(`containers-and-menus:148`).

Three **order claims on the landing page and `lectures.md` were wrong**, and
all three are fixed in the same commit:

- "every later page assumes **all three**" of the vocabulary pages. No engine
  page links all three; `enchantments` and `contexts-and-predicates` link
  *none* of them (corpus grep, zero hits each), and
  `contexts-and-predicates`' trace is a command, not a stack.
- "all three engines are **reload-time citizens of the same machinery**".
  Recipes are a reload listener (`RecipeManager` is a
  `SimplePreparableReloadListener`); loot tables are the
  `RegistryLayer.RELOADABLE` layer; **enchantments are neither** —
  `Registries.ENCHANTMENT` is in `RegistryDataLoader.WORLDGEN_REGISTRIES`
  (`:84`) and `SYNCHRONIZED_REGISTRIES` (`:86`), a world-load dynamic registry
  that `MinecraftServer.reloadResources` never re-reads. **`/reload` does not
  change an enchantment.**
- "four and five are the pair to keep together" — in the page's own numbered
  list four is *Recipes*; the pair is five and six, as `lectures.md:229-232`
  already had it.

The landing-page figure's arrows 4 and 5 carried *items-and-stacks* and
*loot-tables* justifications on `CM → EN` and `CM → CP`; the modifier edge is
re-sourced from `IS` and the unsupported `CM → CP` edge is gone, which is what
the fact-check found and what the prose now says.

### The rest, per page

**`items/README.md`** (landing page)

- ~~"every later page assumes all three" · "all three engines are reload-time
  citizens" · "four and five are the pair" · figure arrows 4 and 5~~ — all four
  above.
- ~~"half this part's timing surprises are claims about which phase something
  ran in" — one page, two lines (`containers-and-menus:276,283`).~~ Narrowed to
  the hopper's late delivery.
- ~~"the five ways one lands on an item" — one of the five (the grindstone) is a
  *removal*, and `RepairItemRecipe.java:77-88` is a sixth writer, copying every
  curse from both inputs onto the combined tool.~~ Fixed here, in
  `lectures.md`, and in `enchanting`'s own title and opening.
- ~~"the ledger behind the click you have already seen happen is *prediction and
  acknowledgement*" — the same shape session F fixed on Part VI's landing page.
  `ServerboundContainerClickPacket` has **no sequence field** (`:14`) and
  `prediction-and-acks.md:173` says every container verb opens no window.~~
  Replaced with the distinction itself.
- **Not acted on:** "the one where the two programs disagree most often and
  most cheaply" is unverifiable — no population, no measure. Left as rhetoric;
  for pass 5 if it grates.

**`items/items-and-stacks.md`**

- ~~`validateContainedItemSizes` at the network door and "recursive"~~ — above.
- ~~"read by `GuiGraphicsExtractor` while it is above zero" — the pop time's
  only reader is `Hud.extractSlot` (`client/gui/Hud.java:1220-1236`,
  `1.0F + pop / 5.0F`); `GuiGraphicsExtractor` draws the icon and, separately,
  the bar.~~
- ~~"`ItemStack.hurtAndBreak` is the **only** way in" —
  `ItemStack.hurtWithoutBreaking` (`:477-491`) reaches `applyDamage` directly,
  and `Mob.burnUndead` (`Mob.java:539-553`) is a second break path entirely, via
  `setDamageValue` plus `onEquippedItemBroken`. The page names
  `hurtWithoutBreaking` itself two paragraphs later.~~ Narrowed.
- ~~Figure 1's dotted "prototype, borrowed and never written" arrow pointed at
  `Holder.Reference`; the prototype is the `DataComponentMap` one node on.~~
- ~~The validator table's *on failure* cell said "logs, and yields
  `ItemStack.EMPTY`" for all three `validateStrict` sites; `ItemInput`
  **throws** (`ItemInput.java:29-33`).~~
- ~~`Item.mineBlock` has a third condition the page omitted:
  `tool.damagePerBlock() > 0` (`Item.java:289`).~~
- ~~`Item.MAX_BAR_WIDTH` is a **dead constant** — `Item.getBarWidth` (`:250-252`)
  spells 13 out and nothing reads it. Kept and said to be dead (session D's
  ruling, now five times).~~
- ~~Every count re-derived clean: 1177 `Items` fields, 4 + 4 instance fields, ten
  `COMMON_ITEM_COMPONENTS` entries, twenty `delayedComponent` call sites (4 in
  `Item`, 16 in `Items`), two `inventoryTick` overrides, entity event 47, five
  break particles, the 6000-tick lifetime, and the single serverbound
  `ItemStack` packet.~~

**`items/using-an-item.md`**

- ~~"The bow, the trident and the spyglass … their `Item.getUseDuration` is an
  hour long" — `SpyglassItem.getUseDuration` returns **1200**
  (`SpyglassItem.java:21-23`), which the page's own closing paragraph says. The
  spyglass genuinely completes by countdown.~~
- ~~"refuses outright if … on cooldown, **and otherwise** opens a prediction
  window" — reversed. `MultiPlayerGameMode.useItem` calls `startPrediction`
  first (`:417`); the cooldown test is at `:420` *inside* the lambda, and the
  packet is built at `:418` and returned and sent either way (`:422`). The
  cooldown suppresses the local `ItemStack.use`, not the report.~~
- ~~Cast row `ProjectileWeaponItem` "only ever on the server" — `draw` and
  `useAmmo` run on the client, outside `BowItem.releaseUsing`'s `ServerLevel`
  test (`BowItem.java:41-42`), which is the whole basis of the page's own
  `DataComponents.INTANGIBLE_PROJECTILE` paragraph.~~
- ~~"four enchantment hooks" on the server path — **five**;
  `ItemStack.hurtAndBreak` reaches `EnchantmentHelper.processDurabilityChange`,
  and the page names `hurtAndBreak` in the next sentence.~~
- ~~"Everything the client learns about its own shot arrives … on **later
  ticks**: the arrow as a spawn packet …" — the arrow is not later.
  `ChunkMap.addEntity` calls `TrackedEntity.updatePlayers` immediately
  (`ChunkMap.java:1293-1294`), inside the same handler, and the packet drain
  precedes `tickServer` (`MinecraftServer.java:1121-1124`). Only the container
  update and the entity data wait.~~
- ~~Figure 2's "tick 32, the server only" bar spanned a `Wire→LP` arrow.~~
  Reworded to what the bar actually marks.
- ~~"the one item that can end either way" for the spyglass — narrowed to what
  the single `Item.finishUsingItem` override is for.~~
- ~~The session-H checklist held in full: `CrossbowItem.useOnRelease` the sole
  override, the five extra `LivingEntity.releaseUsingItem` call sites
  (`completeUsingItem`, `CrossbowAttack`, `RangedCrossbowAttackGoal`,
  `BrushItem` twice), the unacked release, the phantom client arrow, the double
  `onProjectileSpawned`, the skipped `sendAllDataToRemote`, *items/bow.json*,
  and the spear's `UseEffects`.~~
- **For pass 5:** `Consumable.emitParticlesAndSounds` is called with **5** per
  tick (`ItemStack.java:1174`) and **16** at completion (`Consumable.java:62`);
  the page gives only the five. And 26.2's `KINETIC_WEAPON` branch in
  `ItemStack.onUseTick` (`:1177-1182`) means "the base body is empty" no longer
  covers every stack, though it still covers the bow.

**`items/containers-and-menus.md`** — the checklist and **both figures came back
clean, arrow by arrow**; every error was in prose the checklist did not cover.

- ~~"no mutation during a click reaches either, because **nothing calls back
  into the menu**" — `AbstractContainerMenu.slotsChanged` is a bare
  `broadcastChanges` (`:720-722`), and `CrafterSlot.setChanged` (`:21-23`) and
  `ItemCombinerMenu`'s input and result slots (`:21-30,104-113`, the anvil and
  the smithing table) all call it. True of the chest, not of menus.~~ Scoped.
- ~~"on the client it is a **no-op by construction**" — only the wire half is.
  `BeaconScreen`, `ItemCombinerScreen`, `LecternScreen` and the creative
  inventory register real `ContainerListener`s; the anvil's rename field
  repopulates through one.~~
- ~~`ContainerSynchronizer` as "**the only** thing that writes menu state to the
  connection" — `CraftingMenu.java:69` sends its own packet, which the page says
  itself two sections later.~~
- ~~"`SimpleContainer.stillValid` returns true unconditionally — **so** a client
  never closes its own menu" — both halves true, the causal false: every call
  site of `AbstractContainerMenu.stillValid` is on the server.~~
- ~~`Inventory` "present as slots in **every** menu that opens" — `LecternMenu`
  adds one slot, the book.~~
- ~~The out-of-range click "caught by the click's own try/catch" — that
  try/catch **rethrows** as a `ReportedException`; `PacketProcessor` swallows it
  and logs at ERROR, so the path is loudly logged, at odds with the section's
  "nothing logged" framing. "Neither corrected nor fatal" stands.~~
- ~~"their packets carry **no id at all**" —
  `ClientboundContainerSetDataPacket` carries a container id; only the state id
  is absent.~~
- ~~"`BlockEntity.setChanged` only marks the chunk" — it also re-derives the
  comparator output, which the page states correctly a hundred lines earlier.~~
- ~~The closing transfer's shared set is **four** slot ranges, not three — the
  crafting result is a fourth unshared pair.~~
- ~~"the one packet in the game whose *data* the server adopts" — true of *item*
  data only; a rename, a sign and a jigsaw block are adopted as text.~~
- ~~`ContainerInput.QUICK_MOVE`'s "0 or 1, both behave the same" — false at
  `AbstractContainerMenu.SLOT_CLICKED_OUTSIDE`, where it shares `PICKUP`'s
  drop-all/drop-one branch (`:473-484`).~~
- ~~`ServerboundContainerButtonClickPacket` is the **loom's and the
  stonecutter's** too, not just the lectern's and the enchanting table's — four
  `clickMenuButton` overrides.~~
- ~~Every count re-derived clean: seven `ContainerInput` values, three
  `incrementStateId` call sites, the 15-bit mask, `containerCounter % 100 + 1`,
  `Container.getMaxStackSize` = 99, the 128-slot codec cap, the 256-entry hash
  cache.~~

**`items/recipes.md`**

- ~~The reload window~~ — above.
- ~~"one button in the book cycles through **six** kinds of plank" — **twelve**
  recipes carry `"group": "planks"`, all in the *building* category, so all
  twelve land in one `RecipeCollection`.~~
- ~~"a single recipe can occupy a **dozen** consecutive ids" —
  `TransmuteRecipe.MAX_MATERIAL_COUNT` is **8**.~~
- ~~`AbstractFurnaceMenu` "or `RecipePropertySet.CAMPFIRE_INPUT`" — that set
  reaches no menu; its only reader is `CampfireBlock.java:97`, on a right-click.
  Campfires have no menu.~~
- ~~Cast row `Recipe` "read on both sides" — no client class imports `Recipe` or
  `RecipeHolder`, which is the page's own hook.~~
- ~~"a result leaves **only** through `Recipe.assemble` or `Recipe.display`" —
  `StonecutterRecipe.resultDisplay` is read straight by
  `RecipeManager.java:132-133` and shipped to the client.~~
- ~~"which is why the next thing `ResultSlot.onTake` does is look the recipe up
  all over again: the holder … no longer exists" —
  `ResultSlot.getRemainingItems` (`:83-89`) never reads the stored holder on any
  path, and runs identically for special recipes, where the holder is not
  nulled.~~
- ~~Figure 2 arrows 9 and 10 landed in the `SRB` lane; `checkTakeAchievements` is
  `ResultSlot`'s own and `awardUsedRecipes` and the nulling are the
  `ResultContainer`'s — a lane the diagram already had.~~
- ~~`CraftingContainer.asCraftInput` "with the offset remembered" — it
  *discards* the offset (`:16-18`); `asPositionedCraftInput` keeps it, and that
  is what `ResultSlot.onTake` uses.~~
- ~~Gate six tests `PlacementInfo.isImpossibleToPlace`, not identity with
  `PlacementInfo.NOT_PLACEABLE`.~~
- ~~The auto-fill's hint comes from `CraftingMenu.finishPlacingRecipe`; the base
  `AbstractCraftingMenu.finishPlacingRecipe` is a no-op, so the 2×2 grid never
  gets one.~~
- ~~`StackedContents.RecipePicker` is private; `ShapelessRecipe.matches` reaches
  it through `StackedItemContents.canCraft`.~~
- ~~`ServerRecipeBook` stores **four** things, not three — the display resolver
  is a field (`ServerRecipeBook.java:33`).~~
- ~~Every count re-derived clean: 21 serializers, 14 crafting, 9 `CustomRecipe`,
  11 `SlotDisplay`, 5 `RecipeDisplay`, 4 `RecipeBookType` values, 5 concrete
  `RecipeBookMenu` menus, 7 gates, `RecipeCache(10)` static on `CrafterBlock`,
  and `ClientboundUpdateRecipesPacket` from exactly two sites, both in
  `PlayerList` (`:171`, `:949`).~~

**`items/enchantments.md`** — all twelve checklist lines CONFIRMED, and the Fire
Aspect trace clean arrow by arrow.

- ~~"No other item can be made to behave like one"~~ — above.
- ~~"**Every** row of that table is the same shape underneath" — the flag row is
  not: `EnchantmentHelper.has` and `.hasTag` build no `LootContext` and run no
  condition. Figure 1's `Enchantment.matchingSlot` node has the same defect —
  the one-stack walk (`EnchantmentHelper.java:146`), used by `modifyDamage`,
  `modifyKnockback` and `has`, applies **no** slot filter.~~
- ~~Cast row `EnchantedItemInUse` "handed to **every** effect" —
  `EnchantmentValueEffect.process(int, RandomSource, float)` never receives one,
  and neither does `DamageImmunity`. It is built only by the slot-aware walk
  (`:163`).~~
- ~~"`PiercingWeapon.attack` will happily call `LivingEntity.stabAttack` for an
  off-hand slot" — its only caller hardcodes `EquipmentSlot.MAINHAND`
  (`ServerGamePacketListenerImpl.java:1427`). The off-hand path is
  `KineticWeapon.damageEntities` from `ItemStack.onUseTick` (`:1180`). The
  paragraph's conclusion is right by a different route.~~
- ~~"`MultiPlayerGameMode.useItem` runs `TridentItem.use` locally, which asks
  `EnchantmentHelper.getTridentSpinAttackStrength`" — `TridentItem.use` does no
  such thing; the read is in `TridentItem.releaseUsing` (`:68`), reached through
  `MultiPlayerGameMode.releaseUsingItem`.~~
- ~~"thirty-odd lines of JSON" for Fire Aspect — forty-three.~~
- ~~"twenty-nine tags in five families" — the 29 is right; the five families
  account for 25, leaving `TRADEABLE`, `DOUBLE_TRADE_PRICE`, `TREASURE` and
  `NON_TREASURE` unplaced.~~
- ~~"a `PlaySoundEffect` **picking** one of three sounds" — indexed by level
  (`PlaySoundEffect.java:28`), not shuffled.~~
- **An agent finding rejected on re-derivation:** "could not verify the *render
  thread* half of the Quick Charge claim". `reference/threads.md:61` names the
  client's JVM main thread the **Render thread** corpus-wide; the claim is in
  the book's own vocabulary and stands.
- ~~Every count re-derived clean: 43 enchantments (keys and JSON files), 31
  effect components with 24 conditional lists and 7 plain, the 6/15/16
  registries with `EnchantmentAttributeEffect` the odd one out, 29
  `EnchantmentTags`, and Fire Aspect's whole JSON.~~

**`items/enchanting.md`**

- ~~The shared tail~~ — above.
- ~~"only the grindstone and `SetEnchantmentsFunction` reach for
  `ItemEnchantments.Mutable.set`" — the grindstone never calls it (it uses
  `upgrade` and `removeIf`); the **anvil** does, at `AnvilMenu.java:227`, where
  it clamps an over-maximum level down.~~
- ~~"**Only** the table's selection path uses the narrow one
  [`Enchantment.isPrimaryItem`]" —
  `EnchantmentHelper.getAvailableEnchantmentResults` is `selectEnchantment`'s
  own, so the cost-based providers and chest loot use it too. The page's own
  table row and its providers section said so.~~
- ~~"**Only** the table and the provider and loot paths roll dice" — the anvil
  rolls for the chip (`AnvilMenu.java:108`) and the grindstone for the refund
  bonus (`GrindstoneMenu.java:108`), as the page says a hundred lines earlier.
  The table's *randomness* row said "none" for both.~~
- ~~"**Three** different predicates are doing the work" — two.
  `Enchantment.isSupportedItem` reduces to the same test as
  `Enchantment.canEnchant` and has no caller but `isPrimaryItem`.~~
- ~~"above a cost of **forty-nine** the first extra is certain" — certain *at*
  49: `random.nextInt(50) <= enchantmentCost` (`EnchantmentHelper.java:646`).~~
- ~~The grindstone refund's bonus is up to *half minus one*
  (`halfAmount + nextInt(halfAmount)`), not "up to that half again".~~
- ~~The prior-work spiral doubles the **larger** of the two inputs'
  `DataComponents.REPAIR_COST` (`AnvilMenu.java:281-287`), not the result's own,
  and a pure rename skips the step.~~
- ~~"the plain book, which has one random entry deleted from its list" — guarded
  by `list.size() > 1` (`EnchantmentMenu.java:234`), so a one-entry list
  survives whole.~~
- ~~"that lookup is the **only reason** the enchantment registry has to be
  synchronised at all" — `ItemEnchantments.STREAM_CODEC` composes
  `Enchantment.STREAM_CODEC` (`ItemEnchantments.java:39`,
  `Enchantment.java:68`), so every enchanted stack sent to a client needs it.~~
- ~~Figure 1 arrow 7: the ten `ClientboundContainerSetDataPacket` values go out
  at menu open, through `ContainerSynchronizer.sendInitialData`; the
  post-`slotsChanged` broadcast **diffs**, and sends at most nine.~~
- ~~The providers-and-loot column's gate and filter cells missed
  `EnchantRandomlyFunction`, a second exception to `DataComponents.ENCHANTABLE`
  that filters with `Enchantment.canEnchant`.~~
- ~~"`GrindstoneMenu` | the only removal in the game" — `SetEnchantmentsFunction`
  at level 0 removes too.~~
- ~~Every count re-derived clean: 32 bookshelf offsets (the outer ring of a 5×5
  at two heights, `|x| == 2 || |z| == 2`), exactly five narrower primary sets
  with the axes/mace/Thorns split holding, 6 of 7 `SingleEnchantment` providers,
  the ten data slots (3 costs, 1 seed, 3 enchantment clues, 3 level clues),
  `buttonId + 1` as the charge, the seed's whole lifecycle, and the anvil's
  40/39.~~

**`items/contexts-and-predicates.md`**

- ~~The seventeen keys and the client's `ContextMap`~~ — above; the callers list
  and the cast row's thread cell both fixed.
- ~~"`LootTable.getParamSet`, whose only **other** reader is the builder that set
  it" — `LootDataType.java:20` is its only caller in the game;
  `LootTable.Builder` never reads it.~~
- ~~"**Everything** in `net/minecraft/advancements/predicates` … ends up as one
  of these" — false for `ItemPredicate` and `LocationPredicate`, which trigger
  instances hold and test directly with no `LootContext`
  (`ConsumeItemTrigger.java:31,50`; `DistanceTrigger.java:31,50`). The
  `EntityPredicate.wrap` half stands.~~
- ~~"both applied by a codec through `Validatable.validatorForContext`" — the
  enchantment effects use the list form, `Validatable.listValidatorForContext`
  (`EnchantmentEffectComponents.java:124`); only `VillagerTrade` uses the
  singular (`VillagerTrade.java:52`).~~
- ~~"**Two** families, both extending `LootContextUser`" — seven sub-interfaces;
  two carry the traffic, and the page names a third one sentence later.~~
- ~~Figure 1 drew `SlotSource` inside the loot-package subgraph while the prose
  says it is outside it.~~
- ~~**The re-count the charter asked for.** "Twelve of the twenty-six parameter
  sets never roll a loot table" — **CONFIRMED**, derived twice independently
  (once by the session from the page's own caller table, once by the agent from
  a per-set grep across the decompile, minus `net/minecraft/data/**`). The
  twelve: `COMMAND`, `SELECTOR`, `VILLAGER_TRADE`, `ADVANCEMENT_ENTITY`,
  `ADVANCEMENT_LOCATION`, `BLOCK_USE`, `ALL_PARAMS` and the five enchantment
  sets. The 6 + 5 + 1 breakdown is exact, and the same sentence on
  `reference/loot-context-params.md:5` is confirmed with it — settling the count
  session A left for session N.~~
- ~~The rest re-derived clean: 27 `getReferencedContextParams` overriders (29
  files less the `LootContextUser` declaration and the `ValidationContext`
  caller), 20 conditions, 8 number providers, `ALL_PARAMS`' eleven required keys
  and the four it omits, both codec-leniency rules, the three-way random
  precedence, and both figures arrow by arrow.~~

**`items/loot-tables.md`**

- ~~Figure 1 arrow 10~~ — above.
- ~~"makes up to **two** attempts at a chest position" —
  `MonsterRoomFeature.java:104` `while (dx < 2)` is two *chests*; `:108`
  `if (dy < 3)` is up to **three** position attempts each. pass4.md's "two chest
  attempts" carried the same conflation.~~
- ~~"plus **a** per-dye-colour set for sheep" — two: `BuiltInLootTables.SHEEP`
  (`:78`) and `SHEAR_DYED_SHEEP` (`:123`). The checklist had it right and the
  page did not. The category list also missed four of the thirteen path
  prefixes.~~
- ~~"`ComposableEntryContainer.and` and `.or` are what `CompositeEntryBase` folds
  a child list down with" — `CompositeEntryBase.compose` is **abstract**
  (`:45`); each subclass switches on child count and uses `and`/`or` only in the
  exactly-two case (`AlternativesEntry.java:46`, `SequentialEntry.java:34`).
  Zero and one children take other paths, three or more a hand-written loop, and
  `EntryGroup` never uses either. The boolean-not-weighted argument survives on
  `ComposableEntryContainer.expand`'s return type.~~
- ~~Cast row "the **only** place in the whole system where luck reaches a choice"
  — `LootPool.java:111` is the second, as the page's own *Luck touches exactly
  two things* says.~~
- ~~Cast row "the **two** ways out" — `LootTable.getRandomItemsRaw` (`:89,93`) is
  a third public exit, and the page uses it itself.~~
- ~~"That is where the **lock check** and the spectator check live:
  `RandomizableContainerBlockEntity.canOpen`" — the lock check is
  `BaseContainerBlockEntity.canOpen` (`:72-74`), reached through `super`.~~
- ~~"safe **only** because `LootItem` and `TagEntry` construct fresh stacks" —
  `SlotLoot.createItemStack` emits `itemCopies()` and is equally safe.~~
- ~~"arrives as **three** partial ones in three unrelated slots" — an
  illustration stated as fact; nothing fixes the piece count.~~
- ~~"a chest given a loot table by command **re-rolls freshly every time**" — no
  chest rolls twice; the key is nulled on the first unpack either way. The claim
  is about reproducibility.~~
- ~~"The client cannot resolve the table … **so**
  `SeededContainerLoot.addToTooltip` prints the unknown-contents line instead" —
  it prints it unconditionally (`SeededContainerLoot.java:20-23`), on either
  side. No resolve attempt, no fallback.~~
- ~~"a hopper pointing *into* the chest commits the roll **by writing**" — it
  reads first, `HopperBlockEntity.java:164` → `container.getItem`, so the unpack
  fires on the read.~~
- ~~An expanded `TagEntry`'s per-item candidates are built bare
  (`TagEntry.java:59-68`) and skip the entry's own functions — the one exception
  to Figure 2's *the entry's own functions* node.~~
- ~~Every count re-derived clean: 43 function types with 42 extending
  `LootItemConditionalFunction` (`SequenceFunction` the odd one out), 9 entry
  types, 117 `BuiltInLootTables` keys, 3 loot registries, 5 unpacking overrides,
  26 parameter sets, two luck sites, two `MinecraftServer.getRandomSequence`
  callers, and the clear-before-roll and
  `ClientboundOpenScreenPacket`-before-`initMenu` orderings.~~

### The Reference catalogues, a second sample each

Session H asked pass 4 to re-derive a row of each of the part's two generated
views by hand rather than reading the table; session A had already done one
sample each. Both re-confirmed:

- **`reference/loot-context-params.md`** — 26 sets re-counted from
  `LootContextParamSets.java:74-150`. `LootContextParamSets.SHEARING`: required
  `ORIGIN`, `THIS_ENTITY`, `TOOL`; no optional. Matches.
- **`reference/enchantment-hooks.md`** — 50 distinct public entry points in
  `EnchantmentHelper`, three of them marked *nothing outside the class*, so 47.
  Three rows re-derived: `doPostAttackEffectsWithItemSource` (1 overload,
  `AbstractArrow` + `Player`), `enchantItemFromProvider` (1, five callers) and
  `enchantItem` (2 overloads, `EnchantWithLevelsFunction` only). All match.

### The tool bug — the eighth of pass 4

Found by suspecting the tool first, when striking session H's entry made the
part's checklists *grow*. `pass4_queue.py` resets its "current unit" on a blank
line — correct, because a blank line ends a paragraph — but session H and
session I wrote their entries as **one long bullet with blank-line-separated
paragraphs**, and each paragraph after the first therefore lost the parent's
strike. Session C fixed the same inheritance *within* an unbroken run; this is
the same bug across a blank line, and it meant striking session H's bullet
settled only its first paragraph. The splitter now keeps the enclosing
top-level list item across blank lines and an indented continuation inherits
its strike; the corpus-wide effect is exactly Part VII's nine pages and one
`lectures.md` line and nothing else (620 open units → 596, all in this part).

One **routing** wart recorded rather than fixed: a note written as a bare
`` `README` `` in session F's entry matched Part VII's landing page as well as
Part VI's, because the alias table matches the bare word. Session A's ruling
already says to qualify a landing-page note as `` `items/README.md` ``; the
queue tool could also refuse a bare `README`.

The **checklist was wrong once** — session H recorded
`MonsterRoomFeature`'s "two chest attempts", which is two chests of up to three
attempts each — and an **agent once**, rejected on re-derivation: the arrow's
spawn packet does leave on the release tick, because `ChunkMap.addEntity`
broadcasts inside the handler; the report reasoned from `level.tick()` running
before `tickConnection()`, which is not the drain point that matters.

### Rulings

- A hook or a section title whose named mechanism is wrong but whose *argument*
  is right is renamed for the argument, not deleted: `enchanting`'s *The one
  line all five end on* became *The one question all five ask*, and the section
  is stronger for it.
- A figure edge whose label justifies a **different** edge is re-sourced to the
  edge the label is true of, rather than relabelled — the landing page's
  modifier arrow now leaves `IS`, where the mechanism lives.
- A count or superlative that a page's own later text contradicts is narrowed to
  what the later text says. Four times this session (the luck superlative, the
  two ways out, the only-way-in, the reload-time citizens), which is sessions D,
  E and F's precedent again.

### For other parts' sessions

- **Part X** — `client/prediction-and-acks.md:173` ("every container verb open
  no window at all") is **correct** and was the page this session's landing-page
  fix was checked against. `ServerboundContainerClickPacket` has no sequence
  field. Session J should keep that sentence.
- **Part XIII** — `contexts-and-predicates` is the page Part XIII comes back
  for, and its `LootContextParamSets.COMMAND` / `SELECTOR` rows and the
  parse-time-versus-silent-false contrast were all re-confirmed here; session M
  can lean on them.
- **Session N (counts)** — every count on all eight pages plus the landing page
  was re-counted this session and is struck above; the only number left open is
  the landing page's "the four ways one stack is serialised", which is a count
  of *destinations* named on `foundations/codecs-nbt-json` and of nothing in the
  decompile (`ItemStack` declares seven public serialisers). Judged fine as a
  cross-reference and left.


## Session F — Part VI Entities (pass 4) *(2026-09-04)*

Nine pages and the landing page, one adversarial agent each; the order work,
the part-wide notes and every *wrong* re-derived by the session before a
sentence moved. **All ten had at least one wrong claim** — pass 2's result
for a seventh time. Sixty-two corrections. The part's own session-G
checklist came back almost entirely clean (twenty of its twenty-one
corrections re-confirmed, every count on `attributes` and
`synched-entity-data` right, all fifteen figures checked arrow by arrow with
only four arrows wrong) — so this part's errors were not in what pass 3 knew
it had changed, but in the *illustrations* attached to mechanisms it had got
right.

### The four that carry a lecture

- **`authority` is wrong about the player on the client, and its closer is
  wrong twice.** Page: "`Entity.isLocalInstanceAuthoritative` … is false for
  a player on **both** sides — so no player anywhere takes fall damage from
  the mover." Decompile: on the client `LocalPlayer.isLocalPlayer` returns
  true (`client/player/LocalPlayer.java:394`), so
  `Player.isLocalClientAuthoritative` (`Player.java:1259`) is true and
  `Entity.java:823` calls `checkFallDamage` for your own player every tick;
  it does no damage only because `LivingEntity.checkFallDamage` needs a
  `ServerLevel` (`LivingEntity.java:346`). The page's own table row said as
  much. Part VIII's two survivors of the deleted matrix
  (`input-to-movement.md:33`, `the-two-phase-tick.md:146`) scope it to
  `ServerPlayer` and are the correct ones — settling session I's pass4.md
  note the other way round from how it was written.
- **The *NoAI* answer was exactly backwards.** Page: "It does not stop
  `LivingEntity.travel` … so a *NoAI* mob still falls." Decompile:
  `LivingEntity.java:3311` gates `travel` on `canSimulateMovement() &&
  isEffectiveAi()`, and `Mob.java:1425` makes the second false under *NoAI*
  — with `travel` skipped nothing reaches `Entity.move`, so a *NoAI* mob
  does not fall. The page's own gate list four paragraphs earlier had it
  right.
- **The 0.98 coast does not exist**, on three pages' worth of sentences.
  `LivingEntity.java:3212` scales a tracked mob's stored `deltaMovement` by
  0.98 when `canSimulateMovement` is false — and nothing then applies that
  delta, because only `LivingEntity.travel` reaches `Entity.move` and it is
  gated off. A tracked mob is moved **only** by `InterpolationHandler`, and
  stands perfectly still when the interpolation runs out.
- **`pathfinding`'s hook invented a number.** "…and eight ticks later it is
  standing still against a fence": there is no eight-tick give-up anywhere.
  The two timers are `> 100` ticks (`PathNavigation.java:310`) and three
  times a per-node budget (`:338`), which the page's own second paragraph
  states. → **a hundred ticks**.

### Two more punchlines fell

- **`synched-entity-data`'s hook was contradicted by its own next section.**
  "The slot the wool lives in is decided by the order the JVM happens to run
  static initialisers in" — but `ClassTreeIdRegistry.getLastIdFor`
  (`util/ClassTreeIdRegistry.java:15-35`) walks only the **superclass**
  chain, and the JLS fixes superclass-before-subclass, which the page says
  at its own L40. 18 is fully determined by the hierarchy. → the hook now
  states the true and sharper thing: the number is written nowhere in
  `Sheep`, and one new field on `Entity` would renumber every entity in the
  game.
- **`pathfinding`'s malus illustration was wrong on both halves.** "a
  zombified piglin walks through fire and a spider does not":
  `ZombifiedPiglin.java:65` overrides `PathType.LAVA`, not `FIRE`, and
  `Spider` sets no malus at all, so it uses the default `FIRE` = 16 —
  passable, merely expensive. → rewritten around lava, where the same
  constant is 0.0 for a `Strider` (`Strider.java:97`), 8.0 for a
  `ZombifiedPiglin` and the default −1 for an ordinary piglin.

### The queue itself was wrong once, and an agent once

- **`EntitySpawnRequest.ignoreChecks` is not "never true".** Session G
  struck the old page's claim that it builds the spawner's display mob; it
  is true at exactly two sites, `BaseSpawner.java:348` and
  `TrialSpawnerStateData.java:266`, **both building a display entity**. The
  old page was right and the correction was wrong. No current page repeats
  the error, so nothing needed fixing — but this is the second pass-4
  session to find a *session-verified* pass-3 correction false.
- **One agent finding rejected on re-derivation.** The `attributes` agent
  reported "there is no packet queue at the top of the server tick;
  `tickConnection` runs after the levels". `MinecraftServer.processPacketsAndTick`
  calls `packetProcessor.processQueuedPackets()` at `:1122` and `tickServer`
  at `:1124`, and `PacketUtils.ensureRunningOnSameThread` schedules onto
  exactly that processor — so the page is right. The
  `synched-entity-data` agent had confirmed the same ordering independently.

### The rest, per page

- **`README`** (landing page): the shape figure said "one of **five**
  channels", `synched-entity-data` tables **six** → six. "The prediction
  ledger behind your own **movement** is Part X" — the ledger is
  `BlockStatePredictionHandler`, keyed by `BlockPos`; `prediction-and-acks`
  says outright that movement is a different mechanism → *the blocks you
  place*. The same wrong premise was in the *shape of the part* paragraph
  and in `lectures.md:611`, both rewritten around the Part X page that does
  lean on `authority` — `the-client-level`, which opens on "not an authority
  either". The attribute-lateness reason turned on the wrong phase (it is
  `ServerEntity.sendDirtyEntityData` inside *chunkSource*, plus the packet
  drain before `tickServer`, not the block-change broadcast). "Whether an
  entity ticks at all is a property of the chunk" — except `ServerPlayer`,
  exempted at `ServerLevel.java:414`. Red-flash closer corrected to match
  `LivingEntity.java:1283` (a weaker or equal hit does not drop health at
  all).
- **`authority`**: "four predicates" is **five** (`Entity.java:3857, 3861,
  3867, 3873, 3877`) and `Player` overrides **four** of them, not three of
  four; "two classes narrow the AI predicate" is three, and the page names
  three; "six places in `Entity.move` and `LivingEntity.aiStep`, each a
  different member" is **eight sites, nine reads**, three of which read the
  same member — and the bullet list omitted the 0.98 gate, which is the one
  the mob section is about. The boat row claimed `LivingEntity.travel`;
  `AbstractBoat` is not a `LivingEntity` and runs `floatBoat`/`controlBoat`/
  `move` (`AbstractBoat.java:241-246`). Figure 2's first two arrows had the
  boat ticked by `LocalPlayer` (it is `ClientLevel.tickEntities`) and called
  `travel`. `Entity.applyEffectsFromBlocks` was listed among the gates "in
  `Entity.move`", which never calls it. The Part X link was
  `the-client-loop`, a page that never mentions authority.
- **`pathfinding`**: `PathNavigation.setMaxVisitedNodesMultiplier` does not
  scale "one search" — it persists until
  `PathNavigation.resetMaxVisitedNodesMultiplier`, and only `Bee` uses
  either. "A villager can find a bed 48 blocks away because one **attribute**
  is 48" — `Villager` never touches `Attributes.FOLLOW_RANGE`; 48 is its
  `PathNavigation.setRequiredPathLength`, and the page's own closer had it
  right. "Bounded by a node count, **not by a distance**" is false and the
  page says so two sections earlier: `PathFinder.java:111` and `:121` both
  bound by `maxPathLength`. "A null return means only that the node list
  came out empty" — that branch is unreachable; a null means one of
  `createPath`'s four early exits. "Ties go to the path with the fewest
  nodes" — fewest-nodes is the *sole* comparator for reached targets and
  only a tie-break for the rest. "`MoveControl.setWantedPosition` is the
  single method where any decision becomes movement" — `MoveControl.strafe`
  and `MoveControl.setWait` are two more entrances; "eight places" is twelve
  call sites in eight classes; and the "tempted animal drifts in a straight
  line" clause belongs to `TemptGoal.ForNonPathfinders`, used by two mobs,
  not to the base `TemptGoal`, which path-finds. `BodyRotationControl`
  swings the body **immediately** past fifteen degrees; it is the head that
  waits ten stable ticks. The mover gets `zza` through `Mob.setSpeed`, and
  `xxa` only in the strafe branch. Nine of the twenty-seven `PathType`
  constants are −1, not the seven listed. Figure 2's arrow 11 had
  `MoveControl.tick`'s three steps in reverse order.
- **`movement-and-collision`**: "its client copy never reaches `Entity.move`
  at all" — `PistonMovingBlockEntity.java:191` and
  `ShulkerBoxBlockEntity.java:143` both call it from client-side block-entity
  ticks. "The predicate that decides is
  `Entity.isLocalInstanceAuthoritative`, **never** 'am I the client'" —
  `Player`'s overrides are literally `!isClientSide() || isLocalPlayer()`,
  and two gates the page quotes later are client-test-*or*-authority. "It
  calls `Block.stepOn` first and **then** drains
  `Entity.movementThisTick`" — reversed (`Entity.java:953-963` before
  `:1007`). "Boats, shulkers and **minecarts**" answer
  `Entity.canBeCollidedWith` — a minecart overrides `canCollideWith`, the
  *mover's* side; the fourth declarer is `HappyGhast`. "Sixteen block visits
  per segment" caps the sweep's *iteration index*, not blocks. Figure 2's
  GATHER node said "once" (the step-up branch re-gathers block colliders
  over a larger box) and its HEIGHTS node "every Y face". `checkBelowWorld`
  does not kill a `LivingEntity`, which takes 4 damage a tick instead. The
  jump branch is skipped on `LivingEntity.jumping`, before `onGround` is
  consulted. `Blocks.FROSTED_ICE` was missing from the friction row; powder
  snow from the `stuckSpeedMultiplier` pair; the PISTON exemption is from
  the *multiply* only. `ServerEntity.wasOnGround` is "since the last
  absolute sync", not "since the last send".
- **`synched-entity-data`**: "the client cannot write to this channel at
  all" — `ServerboundClientInformationPacket` reaches
  `ServerPlayer.updateOptions` (`:1973-1974`), which sets the two slots the
  page itself introduces. "Seven types set something else entirely" — 37
  types set the interval explicitly; the seven are the ones that set
  `Integer.MAX_VALUE`. `ClientboundTeleportEntityPacket` is not in
  `ServerEntity`'s block at all (its only senders are `Entity.java:3366,
  3368`); `ClientboundMoveMinecartPacket` is, and was missing.
  `MultiPlayerGameMode.interact` sends **then** predicts. `CopperGolem`'s two
  force-dirty writes are redundant (always a different value); only
  `Display`'s is genuine. The `ItemFrame` bypass calls
  `sendDirtyEntityData` only, not the position block, and two other *sends*
  sit outside the gate. `Sheep.applyImplicitComponent` (singular) is where
  the colour is written back.
- **`attributes`**: the registry's default movement speed of 0.7 is not
  "otherwise unused" — the wandering trader, the phantom and the slime are
  registered through the bare `Mob`/`Monster` builders, neither of which
  sets a speed. `Zombie.createAttributes` does not override "the movement
  speed that came from two levels further up"; nothing set one. "Everything
  in vanilla that might double up removes by id first" — three mobs and
  `AttributeCommand` guard with `AttributeInstance.hasModifier` instead. A
  dirty attribute set opens none of `ServerEntity.sendChanges`'s three gate
  conditions, so it waits for the next *interval* multiple, not simply "the
  next tick".
- **`damage-and-death`**: "`AbstractArrow.onHitEntity` builds the number
  before it builds the source" — backwards; the source is built at `:449`
  and passed to `EnchantmentHelper.modifyDamage` at `:457`. "A non-projectile
  block knocks the **attacker** back through `LivingEntity.blockedByItem`" —
  the knockback lands on the **blocker** (`LivingEntity.java:1487, 1491`),
  which is what `Hoglin` throwing the player who blocked it and `Ravager`
  stunning itself both show. "No health is ever changed on a client" —
  `handleEntityEvent` byte 3 and `LocalPlayer.hurtTo` both set it; the true
  claim is that no damage is *calculated* there. "Every link owns exactly one
  multiplication" — three of the eight are subtractions, by the figure's own
  node text. "Something always lands" — Resistance IV multiplies by zero,
  which the figure also says. `CombatTracker.recheckStatus` has four call
  sites, not two. `DamageEffects` picks the hurt sound for **players only**.
  The crit bonus is up to `damage/2 + 1`, not half again. `BlocksAttacks`
  durability is charged for a blocking `Player` only. The `Entity.killedEntity`
  veto does not exist when there is no causing entity. Figure 1's N7 listed
  `setHealth` before `recordDamage`, the reverse of `LivingEntity.java:2089-2090`.
- **`ai-goals-and-brains`**: "Into a goal selector, **one** thing" — the
  leash is a second (`Mob.java:1404`, `PathfinderMob.java:67`). The boat
  answer was wrong: `Mob.updateControlFlags` (`Mob.java:396-402`) takes
  `MOVE` and `LOOK` from *is a `Mob` steering me* and only `JUMP` from the
  boat test, so a mob alone in a boat keeps two of the three; the three-flag
  shutdown is the ridden case. "`VillagerProfession` and `PoiType` are data"
  — both are code-bootstrapped `BuiltInRegistries` (`:236, :237`) with no
  directory under the built-in pack; only `Timeline` is data. "The one mob
  with no goals at all" — a brain mob typically registers none. "There is one
  exception" to the `*Ai` convention — there are two: eighteen `*Ai` classes
  for twenty brain mobs, with `Zoglin` inline as well as
  `VillagerGoalPackages`. "Four packages carry no such behaviour" — five of
  ten (core, panic and hide have nothing at 99; pre-raid and raid have
  `ResetRaidStatus`), and the punchline "nothing is asking the clock" is
  false: `VillagerCalmDown` sits at priority 0 in the panic package and calls
  `Brain.updateActivityFromSchedule` itself once the fear memories clear,
  as `SetHiddenState` does for hide. The work `RunOne` is six entries, not
  five (`StrollToPoiList` was missing). `GoalSelector` does not "seed" its
  lock table — `NO_GOAL` is a `getOrDefault` default, never inserted. "On the
  client, nothing above runs" contradicted the sentence above it.
- **`entity-anatomy`**: "`DefaultedMappedRegistry` overrides **only**
  `byId` and `getValue`" — it overrides nine methods, and one of them,
  `getOptional`, is overridden precisely so it does **not** default (it calls
  `super.getValue`); the untouched lookup `EntityType.CODEC` resolves through
  is `Registry.get`. "Pose is **the one** synched value that changes physics"
  — a dozen subclasses have their own. "The hook paintings and item frames
  use to re-snap" is backwards: `BlockAttachedEntity.java:146` returns
  **false**, the corpus's only override, so those are exactly the entities
  that skip the extra `reapplyPosition`. "Nothing entity-related runs on a
  worker pool" — `ChunkStatus.SPAWN` runs
  `NaturalSpawner.spawnMobsForChunkGeneration` on the worldgen executor, so a
  chunk's first animals are built and finalised off the main thread; no
  entity is ever *ticked* there, which is the sentence's real point. "Only
  three things refresh the dimension caches unasked" — two do it for every
  entity and ten subclasses do it for a value of their own. `setPos` is not
  the constructor's last act. The non-living branches are 66 of 191, a third,
  not "the short half". `/summon` with no position uses the source's feet,
  not a look ray. `Mob.updateControlFlags` is server-only, inside a section
  headed *the tick both sides share*.
- **`entity-lifecycle`**: "`Mob.removeWhenFarAway`, the per-species veto that
  tamed animals, villagers and anything holding a job **override**" —
  `Animal.removeWhenFarAway` returns false for *every* animal, tamed or not
  (`animal/Animal.java:131`), and `Villager` for every villager (`:543`);
  only `Cat` and `Ocelot` are tame-dependent. "Four mobs, unless a species
  **raises** it" — three of the seven overrides *lower* it to 1 (`Ghast`,
  `HappyGhast`, `Pillager`), and the sentence conflated
  `Mob.getMaxSpawnClusterSize` (returns, killing all three group attempts)
  with `Mob.isMaxGroupSizeReached` (breaks the current one). "Each
  [`CustomSpawner`] stamps a **different** one of the nineteen
  `EntitySpawnReason` constants" — phantoms and cats are both *natural*,
  sieges and wandering traders both *event*. "Only `MAGIC_NUMBER` is
  genuinely read" is contradicted by the next sentence. "Those **four**
  callbacks" — the figure crosses five of `LevelCallback`'s seven. "Anything
  trying to upgrade a removal silently does nothing" — only the reason
  *field* is guarded; `Entity.setRemoved` still drops passengers and fires
  `EntityInLevelCallback.onRemove` with the new reason. The three light tests
  are `Monster.isDarkEnoughToSpawn`'s, not
  `Monster.checkMonsterSpawnRules`'. The chicken-jockey rolls are `else if`,
  and the box is 5 × 3 × 5. Figure 1's cascade had far-from-player third
  where `NaturalSpawner.java:272` tests it second, and two exit-node labels
  claimed the whole tick or the whole chunk where the code drops one
  category's attempt.

### Addition 2 — order and dependency

Done in full. All five *before you start* entries are used by a sentence
rather than merely linked, and **one entry was missing**:
`world/points-of-interest`, which `ai-goals-and-brains` spends throughout —
`PoiManager` is a diagram lane, and `AcquirePoi`, `PoiManager.take` and
`ValidateNearbyPoi` carry the villager's day — and which `lectures.md:194`
already said the lecture assumes. `world/chunk-anatomy` was used (the
spawner's heightmap test) but had no page-level link; it now has one, which
settles the Part VI half of session A's pass4.md:1517. The Part X half of the
same note is settled too, by `authority`'s link moving from
`the-client-loop` to `the-client-level`. The three cross-part links
`check_deps.py` reports (`block-entities`, `pistons-and-block-events`,
`codecs-nbt-json`) are all one-line asides, not dependencies. `check_deps.py`
has no Part VI line left.

### No tool bug this session

The second pass-4 session without one, after session D. `pass4_queue.py`,
`claims.py`, `diagram_arrows.py` and `check_deps.py` were all exercised over
ten pages and behaved.

### Rulings

- **A hook that invents a number the page then contradicts is replaced with
  the page's own number**, not merely softened (`pathfinding`'s eight ticks
  → a hundred). Session D's precedent, now twice.
- **An illustration wrong on both halves is replaced, not repaired.**
  `pathfinding`'s fire/spider pair became a lava triple drawn from one
  constant, because the mechanism sentence above it was right and needed an
  example that shows the same table three ways.
- **A "never" the page's own later text contradicts is narrowed to what the
  later text says**, and the later text is the authority — three times this
  session (`movement-and-collision`'s two, `authority`'s NoAI answer).
- **A wrong fact on another part's page is logged, not fixed** (sessions A,
  B and C's precedent): see *For other parts' sessions*.

### For other parts' sessions

- **Part VIII** — nothing to fix; `input-to-movement.md:33-37` and
  `the-two-phase-tick.md:146-148` are **correct** and were the pages this
  session's `authority` fix was checked against. Session I's pass4.md note
  said the survivors agree with Part VI; they did not, and they were right.
- **Part X** — `client/the-client-level.md` is now the Part X page Part VI
  hands `authority` forward to, in both the landing page and `lectures.md`.
  `client/prediction-and-acks.md` should be checked for whether it needs a
  Part VI dependency at all: it never mentions authority, and its ledger is
  `BlockStatePredictionHandler`, keyed by `BlockPos`.
- **Session N (counts)** — `entity-anatomy`'s "18 direct subclasses and 191
  descendants", `entity-lifecycle`'s 289 and 17², `attributes`' 40/8/26,
  `synched-entity-data`'s 43/19/62/8 and `damage-and-death`'s 51/35/21 were
  all re-counted this session and all hold.

## Session E — Part V Blocks (pass 4) *(2026-09-04)*

Seven pages and the landing page, one adversarial agent each; the order work,
the part-wide notes and every *wrong* re-derived by the session before a
sentence moved. **All eight had at least one wrong claim** — pass 2's result for
a sixth time, and this part had the worst provenance in the corpus: two of its
pages were drafted by agents whose reports were lost, one by an agent whose
twelve corrections were never re-derived, and three by the pass-3 session
itself. Sixty-one corrections. The four gates are green and `check_deps.py` has
no Part V line left.

**The four that carry a lecture.**

- **`signal-and-dust`'s staircase is real and invisible, and the page said you
  could see it.** The hook was "a long line does not go dark all at once — it
  counts down, 14, 13, 12, **visibly**, one value per wire", and the first
  *Questions players ask* entry asked why it flickers. Nobody has ever seen it.
  The whole cascade runs synchronously inside one packet handler
  (`MinecraftServer.processPacketsAndTick` drains packets *before*
  `tickServer`, `MinecraftServer.java:1122,1124`), and `Level.setBlock`'s
  flag-2 broadcast only records the section-relative position in a
  `ShortOpenHashSet` on the `ChunkHolder` (`ChunkHolder.java:130-149`). The
  packet is built later in the same tick by `ChunkHolder.broadcastChanges`,
  which re-reads `level.getBlockState(pos)` (`:219`) or the live section
  (`:224`) — so a position written five times in a tick is sent **once**, with
  the value it ended on. The number survives: seven `Level.updateNeighborsAt`
  from a `Sets.newHashSet` (`DefaultRedstoneWireEvaluator.java:28-46`) times six
  directions, because `ServerLevel.updateNeighborsAt` passes a null
  *skipDirection* into `CollectingNeighborUpdater.MultiNeighborUpdate`
  (`ServerLevel.java:1240`, `NeighborUpdater.java:19`), is **forty-two**. The
  hook is now that the staircase costs neighbour updates rather than frames, and
  the landing page's item 5 says the same.
- **`pistons-and-block-events`' motion is off by one tick, all the way through.**
  The diagram put the two motion ticks at N+1 and N+2 and the landing at N+3.
  The placeholders' block entities are registered during the *blockEvents* phase
  of tick N, and `Level.addBlockEntityTicker` puts a ticker straight into
  `blockEntityTickers` whenever `tickingBlockEntities` is false
  (`Level.java:424-426`) — which it is outside `tickBlockEntities` — so the
  *blockEntities* phase later in **the same tick** already walks it. Motion is N
  and N+1; the landing is N+2, when `progressO >= 1.0F` first holds
  (`PistonMovingBlockEntity.java:311`). The *Questions players ask* answer
  ("two ticks of motion afterwards, plus a third") went with it.
- **The block-event census was wrong and the odd block out is the interesting
  one.** "Four blocks raise events directly — `PistonBaseBlock`, `NoteBlock`,
  `PotentSulfurBlock` and, through its block entity, `ComparatorBlock`" is
  **three**. Grepping `.blockEvent(` across the decompile gives thirteen sites:
  one client re-dispatch, three blocks and seven block entities.
  **`ComparatorBlock` never raises one**; it declares a *receiving*
  `triggerEvent` override (`ComparatorBlock.java:197-203`) that forwards to
  `ComparatorBlockEntity`, which does not override `BlockEntity.triggerEvent`
  (`BlockEntity.java:315-317`, `return false`) — so the override is dead in both
  directions, and the page now says so.
- **Quasi-connectivity is not the piston's alone.** "That upward reach is
  implemented nowhere else in the game, which is why quasi-connectivity is a
  piston quirk rather than a redstone rule" is **wrong**:
  `DispenserBlock.neighborChanged:134` is
  `level.hasNeighborSignal(pos) || level.hasNeighborSignal(pos.above())`,
  inherited by `DropperBlock`, and `DoorBlock.getStateForPlacement:130` is the
  same construct. Three blocks, each writing the reach out by hand, and the
  piston's *form* — a per-direction sweep of the block above skipping DOWN — is
  what is unique.

**Two more punchlines that fell.**

- **`diodes-and-observers`' comparison table is introduced as "exactly three
  places" and has five rows**, every one of them a real difference, with about
  fifteen more at override level; the observer is not even a `DiodeBlock` but a
  `DirectionalBlock` with a six-way facing. Two absolutes beside it: the
  comparator is **not** "the only redstone block with a block entity"
  (`SculkSensorBlock.getAnalogOutputSignal:267` answers from
  `SculkSensorBlockEntity`'s last vibration frequency, every container answers
  from its contents, and `DaylightDetectorBlockEntity` stores nothing at all),
  and `RepeaterBlock.LOCKED` is not "the only diode property not computed from a
  redstone reading at tick time" — `POWERED` is the only one computed from a
  reading at all, and LOCKED's distinction is that it is computed *outside* tick
  time.
- **`block-breaking`'s "nothing crosses the wire" is false in one direction.**
  `Minecraft.java:1795` swings on every dig tick and `LocalPlayer.java:340` sends
  a `ServerboundSwingPacket` for every swing. Server-to-breaker is genuinely
  silent; client-to-server is not. The figure's loop label carried the same
  claim. Its sibling: "the client's clock passes 1.0 first" is backwards — the
  server's recomputed value runs a tick *ahead* throughout and its live branch
  simply discards it (`ServerPlayerGameMode.java:135,141-143`); what is true is
  that the client is the only side that acts on 1.0.

**The rest, by page** — what the page said, then what the decompile says.

- `blocks-and-states`: "the client runs the identical `BlockItem.place` … **what
  differs is entirely inside the write**" → `BlockItem.place` branches on side
  twice more after the write, at `updateCustomBlockEntityTag` (`:155-157`) and
  the `CriteriaTriggers.PLACED_BLOCK` trigger (`:79-83`); neither affects the
  state that lands, and the sentence now says so. · "several hundred statics" on
  `Block` → **fifty-eight** (36 methods, 22 fields). · `BlockBehaviour.Properties`
  "read once, in the `BlockBehaviour` constructor" → the constructor *keeps* the
  object (`BlockBehaviour.java:115`) and reads it later at `:392,396,874,876,947`;
  hardness and map colour are never copied out. Same error on the figure's first
  arrow. · "the id order follows the sorted map, **which is why** the codec writes
  properties alphabetically" → a non-sequitur (both come from walking the same
  map), and the encoded form is not alphabetical: `CompoundTag` is a `HashMap`
  written in hash order (`CompoundTag.java:186,197`); the one alphabetical form
  is the *command* text, from `BlockStateParser`. · "a **stored**, sent or
  serialised state" → on disk a state is `BlockState.CODEC`'s name and properties
  plus packed *local* indices, never the global id. · "returns false in four
  cases" → three `return false` statements, the third of which has three causes.
  · The write flowchart drew **no edge out of `SEC`**, hiding the commonest route
  to `FALSE`; it now has the no-op branch. · "all four heightmaps" → four of six,
  the two worldgen ones untouched. · "which is why nothing generated during
  worldgen is ever broadcast" → worldgen never reaches `Level.setBlock` at all.
  · **"a door dropping its other half"** as the example of
  `affectNeighborsAfterRemoval` → `DoorBlock` does not override it (29 classes
  do; it is not among them); the top half goes down the *shape* channel, which is
  `block-interaction`'s whole subject, and the hub page had it on the wrong one of
  its own two channels. · `StateDefinition.Builder.add` rejects a fourth thing (a
  *value* name breaking the pattern); `BlockItem.getPlacementState` refuses on two
  conditions; `StairBlock.canTakeShape` probes a lateral third position, not "the
  far side"; the half is measured against the position the stair goes into.
- `block-interaction`: bit 8's "**buys the section a priority remesh**" → only
  when the *Chunk Builder* option is `NEARBY` or `PLAYER_AFFECTED`
  (`LevelRenderer.java:593-599`); the option defaults to `NONE` and the fancy
  preset sets it. This is the payoff clause of "Ten is the whole story of the
  page". · "`InteractionResult.consumesAction` is what every branch tests" →
  `Minecraft` has no `consumesAction()` call site and matches on the record types.
  · "`DoorBlock.updateShape` has three outcomes" → four of the six directions get
  a fourth, `super.updateShape`, unchanged, because the method is behind a
  vertical-axis test. · "two of them lie" → **one** of the eight gate rows carries
  a false reason. · The hit-location gate is a 2×2×2 box round the centre, not the
  block. · The sound *pitch* comes from `Level.getRandom`, only the seed from
  `Level.soundSeedGenerator`. · `ServerLevel.sendBlockUpdated` scans all of
  `ServerLevel.navigatingMobs` and asks a midpoint-sphere question, not "whose
  path crosses the position". · `Level.gameEvent` is declared on `LevelAccessor`.
  · `Minecraft.startAttack` hands off to `MultiPlayerGameMode.startDestroyBlock`,
  which owns the prediction and the packet. · `MultiNeighborUpdate` is a mutable
  class, not a record, because it resumes mid-walk. · **The duplicated swing
  branch is real control flow**, not a decompiler artefact: the second guard
  subsumes the first, the two run in sequence, and the shape occurs exactly once
  in 7,055 classes — so a `SwingSource.SERVER` block use calls
  `ServerPlayer.swing` twice and sends two `ClientboundAnimatePacket`s
  (`LivingEntity.java:2142`'s guard admits the second because `swingTime` is
  −1). The door is unaffected; the page describes the behaviour and needed no
  change. Settled.
- `block-breaking`: "**Swords are the item that uses all three rule shapes**" →
  the sword uses `minesAndDrops` + `overrideSpeed` twice, and **no item in the
  game** uses all three: `deniesDrops` and `overrideSpeed` never share a `Tool`.
  The "one of exactly three whose `Tool.canDestroyBlocksInCreative` is false"
  half is right (sword, mace, trident). · The durability answer was wrong twice:
  `Item.mineBlock:289` also requires a `DataComponents.TOOL`, a
  `Tool.damagePerBlock` above zero and the server side, and `ShearsItem` — the
  only override — tests no hardness at all, so shears **do** pay on zero-hardness
  grass; "grass" also had to be named (`Blocks.SHORT_GRASS`, not
  `Blocks.GRASS_BLOCK` at 0.6). · "`ItemStack.mineBlock` runs unconditionally —
  it awards `Stats.ITEM_USED`" → the call is unconditional, the award is not. ·
  "only if the remembered answer was yes" → `if (changed && canDestroy)`. · "the
  one input that could drift is which slot is selected" → one of several
  client-reported inputs. · "the server never has to disagree" about a creative
  sword → it does send a correcting block update; it is a no-op because the
  client predicted nothing. · The figure's "the connection phase" label covers
  three different phases and is now split. All ten of the never-re-derived
  pass-3 leads at pass4.md:2326 came back CONFIRMED.
- `block-entities`: "**Every block entity in the game is created and destroyed
  inside one method**" → `LevelChunk.getBlockEntity` in `IMMEDIATE` mode creates
  one on a *read* (`:417-421`), which is the mode every `Level.getBlockEntity`
  asks for (`Level.java:498`); `promotePendingBlockEntity`, `replaceWithPacketData`
  and `SerializableChunkData.postLoadChunk` create them too, and
  `PistonMovingBlockEntity` destroys itself through `Level.removeBlockEntity`. ·
  "that is the whole of the interface" → **block events are a third clientbound
  channel**, and they drive the very chest lid the page discusses two sections
  later. · The figure's last arrow said two `ClientboundContainerSetDataPacket`s
  on the tick it traces; on that tick both lit fields move as well, so it is
  **three** — the pass-2 page had this right and pass 3 replaced it with the
  steady state. · "`LevelChunk.removeBlockEntity` runs regardless: [four things]"
  → three of the four sit inside `if (isInLevel())`; only the ticker rebind is
  unconditional. · `saveWithoutMetadata`'s "the two below" → six external callers
  besides; `saveCustomOnly`'s caller is really thirteen of the nineteen
  `getUpdateTag` overrides; `saveWithId` has two named callers. · "The network
  reuses that path exactly" → it joins at `loadWithComponents` and never reads
  *id*. · The `BoundTickingBlockEntity` gate list is four conditions of which two
  are server-only. · **Every count on the page re-derived and right**: 19 packet
  overriders, 49 registrations, 20 synced types, 2
  `shouldChangedStateKeepBlockEntity` blocks, 8 `preRemoveSideEffects`
  overriders, 200 ticks, 1600 for coal.
- `signal-and-dust`, beyond the hook: "the corpus has three fixed direction
  arrays" → 21 `Direction[]` constants, only two custom-ordered, and
  `SignalGetter.DIRECTIONS` is `Direction.values()`. · "`getBestNeighborSignal`,
  `getDirectSignalTo` and `hasNeighborSignal` **all walk it, and all stop early on
  a 15**" → one walks the array, the other two are hand-unrolled in the same
  order, and `hasNeighborSignal` stops at the first answer **above zero**. · "a
  block merely *touched* by dust does not [power dust]" is true for the wrong
  reason: such a block *is* strongly powered — that is why the piston fires — and
  what hides it from other dust is `RedStoneWireBlock.shouldSignal`, seventy
  lines later. · "the lever is the one place in this trace where the client does
  nothing at all" contradicts the page's own Figure 1: the wire and the piston
  both open on `!isClientSide()` too. · Figure 1 drew `BLK → WIRE`
  unconditionally where `calculateTargetStrength` short-circuits on a block
  signal of 15 — the page's own first dust — and omitted the wire-source gate. ·
  Figure 2 attributed the first dust's `neighborChanged` to
  `LeverBlock.updateNeighbours`; the flags-3 write fanned out first and, with
  `count` at zero, drained the entire cascade before `updateNeighbours` issued
  its two. · `FeatureFlags.REDSTONE_EXPERIMENTS` is a flag, not a data pack (a
  pack that ships nothing else turns it on). · `updatedWires` is pruned before the
  fan-out reads it; the 128 bit is omitted for the first wire on the place path;
  "connected" in `causeNeighborUpdates` means the four horizontals plus DOWN
  always and UP never. · The three redstone-torch constants are all dead and the
  60 lives in a different method from the 8.
- `pistons-and-block-events`, beyond the two above: the flag table said
  `PistonBaseBlock.moveBlocks` "writes four kinds of position" and listed the
  base-at-67, which `PistonBaseBlock.triggerEvent:200` writes after `moveBlocks`
  returns, while omitting the 276 write at `:295`. · The **82 row never fires in
  the page's own scenario**: `deleteAfterMove` is seeded with `toPush` and then
  has every destination and the arm removed (`:346`, `:358`), which for a
  straight push empties it. · The null-*except* `playSound` is
  `triggerEvent`'s, not `moveBlocks`'s. · "The one thing the client does not do
  is play the sound" → it also skips the crushed block's drops, the game event
  and `affectNeighborsAfterRemoval`. · "A piston is the only block in the game
  that cannot act when it is asked" → `NoteBlock` and `PotentSulfurBlock` do
  nothing but raise an event either, and "every other block in Part V answers by
  writing a state there and then" is false of the whole of
  `diodes-and-observers`. · "a five-value record" → `BlockEventData` has four
  components, as the page's own cast table says. · `NOCLIP` is set around one
  entity's move and holds a `Direction`. · `MAX_PUSH_DEPTH` is dead, one of six
  dead constants in the package. · `isPushable` also refuses a push down at the
  world floor or up at its ceiling, and skips two of its tests for a piston. ·
  `addBlockLine` walks backwards along the axis too and *fails* rather than
  stopping. · `TRIGGER_DROP` also requires the moving piston to face the same way.
  · `isSourcePiston` is set on the arm **and** on a contracting piston's own
  placeholder.
- `diodes-and-observers`, beyond the table: `Block.getStateForPlacement` was
  credited with the horizontal reversal — it returns the default state;
  `DiodeBlock.getStateForPlacement:168-170` does it. · "`Level.setBlock`'s own
  fan-out never runs" on a flag-2 write → the *neighbour* fan-out does not, the
  three shape passes do, on a page whose whole argument is that the two channels
  are different. · The item-frame rule is wrong in both places it is stated: the
  direction filter is applied *inside* `getEntitiesOfClass` and the `size() == 1`
  test after it, so a second frame facing another way changes nothing. ·
  Container fullness divides by `Container.getMaxStackSize(itemStack)`, the
  smaller of the container's cap (99 by default) and the stack's own maximum. ·
  `Level.updateNeighbourForOutputSignal` is **not** called "from the tail of every
  `Level.setBlock`" — it sits inside the flag-1 branch and behind
  `!isClientSide()` — and the page's own example, an item entering a chest, does
  not go through `setBlock` at all: it goes through `BlockEntity.setChanged`,
  which calls it unconditionally. · The reach-one-further branch is an *else*, not
  an *and*. · `RepeaterBlock.updateShape`'s "off-axis — the two sides" is four
  directions, up and down included. · `checkTickOnNeighbor` is wrapped in
  `!isLocked`, which the page omitted for the diode and over-sold for the
  comparator (which has no lock to consult). · The observer's own
  `updateNeighborsInFront` differs from the diode's in its orientation hint.
- `blocks/README.md` (the landing page): the **hook's first member was wrong** —
  "the block that appears under the crosshair before the server has heard about
  it" comes from `BlockStatePredictionHandler`, not from the neighbour/shape
  split; the other two feelings do come from it, and the page now says which is
  which. · "the one mechanism in the part that defers work to a named phase of
  the tick" → scheduled ticks drain in *tickPending*, and the same landing page
  calls the diode lecture "a change that books a turn"; `lectures.md` item 6
  carried the same absolute and is fixed with it. · "The moving blocks are never
  sent to anybody" → true of block updates only; `PistonMovingBlockEntity`
  overrides `getUpdateTag`, so a chunk send carries the moved state. · "nothing
  you do in between can stop it" → the block going to air does. · The **figure
  drew four spokes for a hub and six**, and three of its labels named reaches the
  pages do not make; `BS → PE`, `BS → DO` and `BE → PE` added, three labels
  rewritten to what the target page actually reaches for, and
  `diodes-and-observers` gained the two links (to `signal-and-dust` and
  `block-entities`) that its two inter-spoke edges assert. · "Every page here is
  either about choosing that state, about the write itself, or about a block that
  reacts" → `block-entities` is none of the three. · Two smaller ones: only
  `DataComponents.TOOL` of the three named data components is used by the part,
  and `registries.md`'s rows are keyed `Registries.BLOCK`, not
  `BuiltInRegistries.BLOCK`.

**The shared preamble, and Part X.** The dependency ruling holds — the two click
pages' contract statement is character-identical but for the self-reference, and
it is sufficient for both lectures — but its **fourth sentence described a
comparison that does not exist**. `BlockStatePredictionHandler.updateKnownServerState`
*overwrites* the remembered state with the server's correction (`:27-36`), so by
settle time there is one value, and `endPredictionsUpTo` hands that to
`ClientLevel.syncBlockState`, which compares it against **the world**
(`ClientLevel.java:219-231`). Rewritten on both pages, still four sentences, and
`prediction-and-acks.md:82-90` already had the mechanism right.

**Addition 2, done in full.** All four *before you start* entries are used by a
sentence, and two of the reasons given were wrong: `world/fluids` is reached
through `StateHolder` being shared with `FluidState` and through waterlogging,
not through "the flowing block that this part keeps writing around", which
matches no sentence in the part; and `world/chunk-anatomy` is used for the
section write, the heightmaps and the light check, not for the palette. One entry
was **missing**: `server/server-tick`, which `pistons-and-block-events` leans on
for "packets are drained before the levels tick" and `block-interaction` for "the
receipt goes out when `tickChildren` reaches connections" — both facts belong to
that page and to no other, and both pages now link it. `check_deps.py` has no
Part V line left. "Two Part IV pages are load-bearing" was three (chunk anatomy
is Part IV as well) and now reads "two more".

**The tool bug — the seventh of pass 4.** `pass4_queue.py`'s `STRUCK_RE` matched a
strike only after a `-`/`*` bullet or a heading, so a **numbered** list item could
never be settled: session F's four provenance classes are `1.`–`4.`, and striking
them left the unit open for ever. The regex now takes `\d+[.)]` too. Found the
same way as the previous six — by suspecting the tool when the queue disagreed
with the file.

**Verified by counting, and right.** Forty-two, and both its factors · seven
positions, seven per `checkCornerChangeAt` · eighty stair states · 19 / 49 / 20 /
2 / 8 on `block-entities` · the ten flag bits and 324 / 82 / 67 / 18 / 276 ·
1,357 and 643 and twenty lines · 124 `BlockStateProperties` · three concrete
`Property` kinds · eight `ServerboundPlayerActionPacket.Action`s · 30 and 100,
level squared plus 1, 1 + 0.2 × (amplifier + 1), the four mining-fatigue factors,
0.2, divide by five · 0.7 and 1.07 · 32, 64, 400 and every twentieth tick ·
±0.25, 0.005, ten ticks · 12 · obsidian and its three relatives · five
`deathTicks` · three priorities.

**Rulings.** A hook falsified by an *observable* the code does not produce is
replaced by the true statement of the same fact — the staircase is real, it is
just not visible — rather than deleted, because the mechanism it introduced is
still the page's subject. A figure that draws four edges for a claim of six is
fixed by adding the two edges and correcting the labels, not by softening the
claim, which the six links support (session C's precedent). A *before you start*
entry whose stated reason no sentence supports has the reason rewritten to what
the part actually leans on, rather than being struck (session D's precedent). And
a pass-3 session's own provenance grading is a claim like any other: the ten
never-re-derived leads on `block-breaking` were all correct, and the two pages
whose reports were lost were the two carrying the worst errors in the part.

**Left for other sessions.** `client/the-client-level.md:44` attributes
`gameEvent` to `Level`; it is declared on `LevelAccessor` and `ClientLevel`
overrides it — Part X's session. `pass4.md:1552` and `:1821` (session P's
`entity-rendering` / `block-entity-rendering` siblings) are Part XI's; `:1850` is
the Reference tier's. Wording debt is in [pass5.md](pass5.md).

## Session D — Part IV The world (pass 4) *(2026-09-04)*

Ten pages and the landing page, one adversarial agent each; every *wrong*
re-derived by the session before a sentence moved. **All eleven had at least
one wrong claim** — pass 2's finding for a fifth time. Forty-nine corrections.
The four gates are green and `check_deps.py` has no Part IV line left.

**The four that carry a lecture.**

- ~~**`tickets-and-loading`'s eleven was two rings short, and its opening
  paragraph named the wrong status.** "Eleven chunks past the edge of view"
  and the bolded callout "**Eleven** — chunks past a level-31 ticket that get
  a holder" are both **thirteen**: eleven is `ChunkLevel.RADIUS_AROUND_FULL_CHUNK`,
  the reach past a level-**33** chunk, and a `TicketType.PLAYER_LOADING`
  ticket sits at 31 (`DistanceManager.PLAYER_TICKET_LEVEL` =
  `ChunkLevel.byStatus(ENTITY_TICKING)`, `DistanceManager.java:40`), so the
  flood needs two more rings to reach `ChunkLevel.MAX_LEVEL` 44. And a level-44
  holder is not "running the first noise pass": replaying
  `ChunkStep.Builder.buildAccumulatedDependencies` over
  `ChunkPyramid.GENERATION_PYRAMID` gives the FULL step's twelve-entry list as
  *SPAWN, INITIALIZE_LIGHT, CARVERS, BIOMES, STRUCTURE_STARTS × 8* — so 44 maps
  to `ChunkStatus.STRUCTURE_STARTS`, and `ChunkStatus.NOISE` appears on that
  list **nowhere**. Both fixed, and the plateau is now stated.~~
- ~~**`chunk-generation-pipeline`'s own derivation of the 11 did not add up.**
  The page named two radius-1 rows (*NOISE*→*BIOMES*, *FEATURES*→*CARVERS*) on
  top of *STRUCTURE_STARTS* at 8, which is 10. Five requirements have radius 1;
  **three** widen the accumulated list, because
  `ChunkStep.Builder.getRadiusOfParent` counts a debt only when the step's own
  parent already sits a ring out. The missing term is
  *LIGHT*→*INITIALIZE_LIGHT* (`ChunkPyramid.java:31`); *SURFACE* and *SPAWN*,
  which also ask for *BIOMES* within 1, add nothing. Sizes: 9 → 10 → 11 → **12**.
  The same page's hook called 11 "the length of `ChunkStep.accumulatedDependencies`"
  when it is the length minus one (`ChunkDependencies.getRadius`), contradicting
  its own figure.~~
- ~~**`lighting`'s "up to 27 sections across nine chunks" is 14 across seven,
  and 27 is geometrically impossible.** A torch floods to taxicab distance 13;
  `SectionPos.aroundAndAtBlockPos` dilates each written position by one block in
  L∞. Exhaustive enumeration over all 4,096 in-section placements gives **14
  sections** and **7 chunk columns** as the maxima (both reached at section
  offset 13,15,11). 27 cannot happen: the (−,−,−) corner section needs the
  torch's section-relative coordinates to sum to at most 13 and the (+,+,+)
  corner needs them to sum to at least 32. The 27 in the code is
  `LayerLightSectionStorage.markSectionAndNeighborsAsAffected`'s 3×3×3, which is
  the path the paragraph names in order to rule it out.~~
- ~~**`points-of-interest`'s hook was contradicted by its own state diagram.**
  "The claim and the *occupied* flag are two facts that never speak to each
  other" — but `ValidateNearbyPoi` reads `BedBlock.OCCUPIED` and calls
  `PoiManager.release` (`ValidateNearbyPoi.java:36-41,56-60`), an edge the page
  draws forty lines later. Replaced with the true asymmetry: **the flag can only
  take a claim away, never make or confirm one.** The landing page's lecture-10
  blurb carried the same sentence and is fixed with it.~~

**Two more punchlines that fell.**

- ~~**`environment-attributes-and-timelines`' badlands sky is blue.**
  *data/minecraft/worldgen/biome/badlands.json* sets *visual/sky_color*
  `#6eb1ff`, **bluer** than taiga's `#7da3ff`; enumerating all 66 biome files
  shows every declared overworld sky colour is a blue except pale garden's grey
  `#b9b9b9`. The hook's "slides from orange towards black" is now pale garden's
  grey. And "the day timeline's sun … Bézier, which is why the sun visibly slows
  near the horizon" is backwards: *sun_angle*'s two keyframes both sit at tick
  6000, so the baked segment runs noon→noon under
  `cubic_bezier [0.362, 0.241, 0.638, 0.759]`. Numerically the rate is **0.67×**
  linear at noon, **1.19×** at midnight and **1.07×** at the horizon — the sun
  lingers at its zenith, which is why the horizon crossings fall at ticks 12782
  and 23218 and a day is **13,564** ticks of sun against **10,436** of night.~~
- ~~**`chunk-storage`'s flush is not the lane's lowest priority.**
  `IOWorker.synchronize(true)` submits its flush through
  `submitThrowingTask`, i.e. `Priority.FOREGROUND` (`IOWorker.java:180, 219`);
  `Priority.SHUTDOWN` has exactly one user in the game,
  `IOWorker.waitForShutdown` (`:281`). The flush does land behind the writes,
  but because it first waits on every `IOWorker.PendingStore` future, not
  because of its priority.~~

**The rest, by page** — what the page said, then what the decompile says.

- ~~`chunk-storage`: "a no-save world … never lets go of a chunk at all,
  because `unloadQueue` and `toDrop` are drained nowhere else" — two callers of
  `ChunkMap.processUnloads` (`:473`, `:448`); the second is inside
  `saveAllChunks(true)` on an always-true budget, reached on a no-save level by
  `/save-all flush` (`MinecraftServer.saveAllChunks` suppresses `noSave` when
  *force* is set) and by `ServerChunkCache.close`, which never consults it ·
  "every entity is removed with `UNLOADED_TO_CHUNK`" — the
  `EntityAccess::shouldBeSaved` filter runs first
  (`PersistentEntitySectionManager.java:207-209`), excluding players,
  `EnderDragonPart`, passengers and single-player-crewed vehicles · "Two places
  make the server thread wait on a disk" — three; `StructureCheck.tryLoadFromStorage`
  joins `IOWorker.scanChunk` (`:116`) on the server thread for `/locate`, an eye
  of ender, a dolphin and the explorer map · figure 3's sidecar branch put the
  temp-file write before the allocation — `RegionFile.write:322-324` allocates
  first · "both subclasses override `forceSynchronousWrites`" — three subclasses,
  two override; `GameTestServer` keeps the base true · "`ImposterProtoChunk`
  answers false **because** it defers its dirty flag" — only `markUnsaved`
  delegates; the rest are hard falses · "`RegionFile.getTimestamp` writes" — it
  reads; `RegionFile.write` does the writing · `VERSION_CUSTOM` is refused in
  `createChunkInputStream`, not `getChunkDataInputStream` · the 2000-task drain
  is only the excess above 2000 · an autosave still wants an accessible, ready,
  unsaved `LevelChunk`/`ImposterProtoChunk` · `synchronized` on the `RegionFile`,
  not the channel · `computeNextAutosaveInterval` uses the tick rate only while
  not sprinting · figure 2's `save` arrows were in the `SerializableChunkData`
  lane when they are `ChunkMap.save`'s.~~
- ~~`tickets-and-loading`: the cast row's "the same flood-fill as **the light
  engine** (`DynamicGraphMinFixedPoint`)" — a 1.21-era fact; the class has
  exactly two subclasses corpus-wide, `ChunkTracker` and `SectionTracker`, and
  `LightEngine` is its own hierarchy — `lighting.md` already said so in its
  1.21 note, the third time this pass one page has convicted another ·
  "`ChunkLevel` is derived, not declared" — 31/32/33 are declared literals; only
  the ceiling is derived · "the simulation graph 0 … 33 because nothing above 33
  can tick" — nothing above **32** ticks; 33 is the tracker's *absent* sentinel ·
  "`ClientboundSetChunkCacheCenterPacket` — always" — only when the chunk column
  changed (`ChunkMap.updateChunkTracking`, `applyChunkTrackingView`) · "mob
  spawning obeys none of the numbers a player can set" — true of the radius-8
  tracker, but `ChunkMap.collectSpawningChunks` also wants a ticking chunk and a
  non-spectating player within 128 blocks · "`purgeStaleTickets` runs once per
  tick" — gated on `runsNormally() || !tickChunks` · "singleplayer ignores the
  quota entirely" — it skips the batch *size* cap; the acknowledgement and quota
  gates still apply · `TicketStorage.addTicket` notifies with the new ticket's
  own level when it is lower, and it is *removal* that recomputes a minimum ·
  "nothing ever asks is this chunk loaded" — `ChunkLevel.isLoaded` is exactly
  that.~~
- ~~`chunk-anatomy`: "a resize **and a `PalettedContainer.read` from the wire**
  each swap in a whole new record" — `createOrReuseData` returns the *existing*
  record when the configuration matches (`:84-85`) and `read` then mutates
  palette and long array in place, which is the ordinary client case and the
  sentence that justifies the lock-free `get` · "Only block states resize in
  place" — true of the *published* container; `fillBiomesFromNoise` grows a
  scratch container through the same `onResize` before swapping it in ·
  `LevelChunkSection.BIOME_CONTAINER_BITS` has zero readers; the 2 that matters
  is the literal in `Strategy.createForBiomes` · "writes are dropped unless
  *allowWrites*" — both construction sites pass **false**, so every write to an
  imposter is dropped in 26.2 · step 6's skip column omitted the
  `useShapeForLightOcclusion` disjunct · `BulkSectionAccess` has one user,
  `OreFeature`; `NoiseBasedChunkGenerator` acquires its whole noise range, not
  "its own section".~~
- ~~`chunk-generation-pipeline`: "how far from spawn you are allowed to build" —
  `ChunkPyramid.MAX_CHUNK_COORDINATE_VALUE` is about 33.55 M blocks, three and a
  half million **outside** `Level.MAX_LEVEL_SIZE`'s ±30 000 000, so the safety
  margin can never be the limit a player meets; the closing Q&A said it was ·
  "`ChunkLoadCounter` … drives nothing" — it is
  `MinecraftServer.prepareLevels`' loop condition · "the pool only gets used in
  parallel for the biome and noise forks, the disk parse, and the second
  dimension" — also the per-level *light* `ConsecutiveExecutor`, the datafix and
  the POI prefetch · "No thread ever blocks waiting for a neighbour" — no
  *worldgen* thread; `ServerChunkCache.getChunk` blocks the server thread, as the
  page says elsewhere · `scheduleFullChunkPromotion` is called inside
  `updateFutures`, not "separately and later".~~
- ~~`lighting`: "does exactly one thing about light" — three calls, as the page's
  own next section says · `hasDifferentLightProperties` is an **or** on shape
  occlusion, not a disagreement · "`SkyLightSectionStorage.getLightValue` walks
  upward … above the top" — above `topSection` it answers 15 immediately; the
  walk is for a data gap *below* it · the F3 answer was wrong end to end:
  `DebugEntryLight` prints **three** numbers and its combined one is already
  `getRawBrightness(pos, 0)`, darkening explicitly zeroed · `SpatialLongSet` has
  no callers at all · `hasAllNeighbors` checks chunk presence as well as the light
  flag · `scheduleUnload` kicks after *queuing* the nulling ·
  `DEFAULT_BATCH_SIZE` has no readers · "nothing else ever waits on the light
  engine" against the page's own `waitForLightBeforeSending`.~~
- ~~`scheduled-ticks`: session E's own *session-verified* ruling that "the sprint
  path never touches the flag" is **false** —
  `ServerTickRateManager.requestGameToSprint` calls `setFrozen(false)` and
  `finishTickSprint` restores it; the conclusion (a sprint runs the drain) stands,
  the reason did not · "`/tick freeze` … the only thing that does" — a debug world
  skips the section too, as the page says at its drain section ·
  "`rescheduleLeftoverContainers` … so the next level tick collects it first" —
  `LevelTicks.CONTAINER_DRAIN_ORDER` is `INTRA_TICK_DRAIN_ORDER` on the heads and
  has **no time term**; being overdue buys no place in the order · the container
  hand-off: the re-queue arm also needs budget left, and a container drained empty
  goes to neither queue nor index · "`ScheduledTickAccess.scheduleTick` and
  nothing else" — eight members · "nothing in the game moves or cancels a pending
  tick" — `LevelChunkTicks.removeIf` through `LevelTicks.clearArea`, which the page
  describes forty lines later · the `hasScheduledTick` list missed
  `DriedGhastBlock` and `SpeleothemBlock` (seven, not five) ·
  `BlackholeTickAccess` is not client-only — `ImposterProtoChunk` uses it on the
  server · `getGameTime` is declared on `LevelAccessor`.~~
- ~~`fluids`: "`LiquidBlock` … every place a fluid tick is booked" and "Three
  other places book the same appointment" — **61 call sites over 52 classes**,
  because every waterloggable block books water's tick from its own
  `updateShape`, including `WaterloggedTransparentBlock`, which the page names
  two paragraphs earlier · "`Fluids.FLOWING_WATER` … reads **both** from
  `FlowingFluid.LEVEL`" — `WaterFluid.Flowing.isSource` returns a constant false ·
  "the only fluid code a client runs is `FluidState.animateTick`" —
  `FluidRenderer` and `EntityFluidInteraction` both call `FluidState.getFlow` ·
  "every block the water later touches arrives as a `ClientboundBlockUpdatePacket`"
  — `ChunkHolder` sends that only for a section with exactly one change; a
  spreading flow is the `ClientboundSectionBlocksUpdatePacket` case · the pool
  drain: only the outermost block comes back empty; every ring behind re-levels
  one lower · `LavaFluid.spreadTo`'s `LiquidBlock` test guards the **stone**
  alone — the fizz and the blocked spread happen for any water target ·
  `FlowingFluid.spreadTo` skips `beforeDestroyingBlock` on air, so lava into air
  does not fizz · the cast row credited `LavaFluid` with three
  liquid-to-rock overrides when two are `LiquidBlock.shouldSpreadLiquid`'s, as the
  page's own body says · `BucketItem`'s evaporation branch returns before the
  waterlogging is done.~~
- ~~`game-events-and-vibrations`: session E's note that
  `DynamicGameEventListener.move` "does nothing at all if either chunk is not
  loaded to FULL" is **false** — the unregister and the register are guarded
  independently and `lastSection` advances either way, so a half-loaded move
  leaves a stale registration or drops the listener out of the world
  (`DynamicGameEventListener.java:34-58`) · the calibrated sensor is active for
  **10** ticks, not "the same" 30 (`CalibratedSculkSensorBlock.getActiveTicks`),
  and `SculkSensorBlock.ACTIVE_TICKS` has no readers · "the warden is the one
  entity whose `Entity.dampensVibrations` is true" — `ItemEntity` too, which the
  page itself invokes twenty lines later; the warden is the one that dampens
  *unconditionally* · `GameEventListener` is four methods, not three · the
  footstep cadence is `Entity.applyMovementEmissionAndPlaySound`'s
  `moveDist`/`nextStep` test, not `vibrationAndSoundEffectsFromBlock` · figure 2's
  `onReceiveVibration` carries a distance, and lands in the block entity's
  `VibrationSystem.User` · a column the dispatcher skipped is *not* on the debug
  channel, because the broadcast happens only where a listener was visited.~~
- ~~`points-of-interest`: "every releaser checks `getType` or `exists` first" —
  `VillagerMakeLove.java:76` checks neither · "`Villager.releasePoi` does both" —
  `getType` plus the `POI_MEMORIES` predicate · "`take` — alone in the query
  family in having no `Occupancy` parameter" — alone among the *radius searches*;
  the page's own query-family list names `exists` and `getType`, which take none ·
  "The claim itself is three statements" — five · "the only thing a client ever
  learns" — the debug channel is fed from the same block · "checked once every
  twenty seconds" — the 400-tick cap is never reached, because the marker is swept
  on the tick it would first apply · `SetWalkTargetFromBlockMemory` beyond 150
  still writes a walk target, toward a random intermediate position ·
  `bedIsOccupied`'s third term is "*this* body is not asleep", not "somebody else
  occupies it" · `AcquirePoi.SCAN_RANGE` has no callers ·
  `updatePOIOnBlockStateChange` is not the only door
  (`checkConsistencyWithBlocks` is the other) · the zero-ticket types are six of
  twenty-one, not "half", and none is in `PoiTypeTags.VILLAGE` anyway ·
  `GoToPotentialJobSite.stop` does release a ticket · `LivingEntity.startSleeping`
  sets the flag; `SleepInBed.start` records `LAST_SLEPT` and erases the walk
  target itself.~~
- ~~`environment-attributes-and-timelines`: "every consumer of a visual attribute
  goes through [the probe]" — the clock item and `ClientLevel`'s ambient particles
  read `environmentAttributes()` directly · "exactly three `getDimensionValue` call
  sites" — a fourth names no attribute, `EnvironmentAttributeReader`'s
  loot-context dispatch · the periodic wrap interpolates across the wrap, which on
  this clock is **dawn**, not midnight · the `keyframeLerp` row holds only for an
  override track; a modifier-argument track uses
  `AttributeModifier.argumentKeyframeLerp` · "weather always gets the last word" —
  on the client the two flash layers sit above it.~~
- ~~The landing page: "the server thread waits for none of it" — the *save path*
  does · figure arrow "read by all four" — fluids and the villagers only; nothing
  under `world/ticks` or `world/level/gameevent` names an environment attribute ·
  "everything happens on the Server thread or on a worker the loop is waiting for"
  — the IO lane is neither · "Game rules — most of which this part reads" — five ·
  the shape paragraph accounted for nine of the ten pages.~~

**Addition 2, done in full.** All four *before you start* entries are used by a
sentence. `foundations/identifiers-and-registries` was listed and linked by no
page: the dependency is real (`Block.BLOCK_STATE_REGISTRY` and the biome registry
behind the global palette, `BuiltInRegistries.CHUNK_STATUS`,
`Registries.WORLD_CLOCK`, `BuiltInRegistries.FLUID`), so the link now sits on
`chunk-anatomy`'s global-palette sentence rather than the entry being struck —
which settles the Part IV half of session A's pass4.md:907 note, logged there as
pass-5 work. One entry was **missing**: `foundations/tags`, which
`game-events-and-vibrations` and `points-of-interest` spend throughout, and it is
added. `reference/block-update-flags` was likewise missing from *Reference this
part uses* while three pages spend the flag word. `check_deps.py` has no Part IV
line left.

**Verified by counting, and right.** 529 · twelve statuses · the twelve-entry
FULL row · 44 and 45 · the four `FullChunkStatus` values and all nine ticket
types with every flag column · 20/128/10 000 ms/300 s · the region-file layout
(4096, two header sectors, 1024 entries, the sector-number packing, 256) · 48
environment attributes, 66 biome files, 11 biome-layer attributes · 61 game
events with 15 resonance frequencies · 21 POI types with every
`maxTickets`/`validRange` pair · 37 fluid states, the 4/2/4 and 7/3/7 rows, the
120 positions per side · 65536 per `LevelTicks.tick` call · the buffer of two,
eleven on the axes and nine on the diagonal.

**Rulings.** A hook the page's own figure contradicts is replaced rather than
softened (`points-of-interest`), and the replacement states the asymmetry the
figure draws. A dead constant that names the right number is kept and *said to
be dead* rather than deleted, because a reader grepping for it will find it
anyway — `AcquirePoi.SCAN_RANGE`, `SculkSensorBlock.ACTIVE_TICKS`,
`LevelChunkSection.BIOME_CONTAINER_BITS`, `ThreadedLevelLightEngine.DEFAULT_BATCH_SIZE`,
four of them in one part. And a pass-4 note from a pass-3 session is a claim like
any other: two of session E's *session-verified* corrections were themselves
wrong (the sprint path and the `DynamicGameEventListener.move` guard), which is
the re-derive rule earning its place against the queue rather than against an
agent.

**Left for other sessions.** `rendering/lightmap-fog-and-sky` still says the
lightning flash "whitens" SKY_COLOR where this part says it lerps toward a named
colour — Part XI's session. `reference/level-data-and-rules`' paths and
who-owns-what table are still unstruck from session E and belong to the Reference
tier. Wording debt is in [pass5.md](pass5.md).

## Session C — Part III The server (pass 4) *(2026-09-04)*

Six pages (five system pages and the landing page), one adversarial agent
each, on Opus. **Every one of the six had at least one wrong claim** — pass
2's finding holding for a fourth time, and this time on the two pages the
rest of the book cites most. Twenty-eight corrections, three of them
load-bearing enough to change what a lecture says. Every *wrong* was
re-derived by the session from the decompile before a sentence moved, and
two agent findings were rejected on that re-derivation.

### The three findings that carry a lecture

- ~~**The event-loop figure on `server-tick` had two impossible edges.** It
  drew `RUN --> C` ("pollTaskInternal *then* offers every level's chunk
  source a turn") and `L --> W` ("leave it queued" to `waitForTasks`).
  `MinecraftServer.pollTaskInternal` offers the chunk sources a turn **only
  in the else** — when `super.pollTask()` ran nothing
  (`MinecraftServer.java:993-1011`); and `BlockableEventLoop.waitForTasks`
  has exactly one call site, `managedBlock` (`BlockableEventLoop.java:149`),
  which is the *blocked* side, where `shouldRunAllTasks()` is
  `blockingCount > 0` and so no task is ever left queued for want of budget
  (`:125-140`). The figure is redrawn with the queue-empty exit the old one
  lacked, and the prose that repeated the "then" is fixed with it.~~
- ~~**`server-tick`'s packet-drain punchline was false.** "This is the only
  point in a tick where player input enters the world" —
  `ServerGamePacketListenerImpl.handleChat` never calls
  `PacketUtils.ensureRunningOnSameThread`; it runs on the Netty thread and
  posts through `tryHandleChat` to `this.server.execute(chatHandler)`
  (`ServerGamePacketListenerImpl.java:1678-1683, 1829-1838`), as do both
  command packets (`:1707, :1729`). Chat and commands arrive as **tasks**,
  drained by the event loop the same page documents two sections later.~~
- ~~**`server-level-tick`'s "nothing sends a block update at the moment a
  block changes" has a counter-example, and the page had made it an
  example.** `FallingBlockEntity` calls `Level.setBlock` and on the next
  line `ChunkMap.sendToTrackingPlayers` with its own
  `ClientboundBlockUpdatePacket` (`FallingBlockEntity.java:206-207`), so
  falling sand lands in the *same* tick. The page's one concrete
  "visible from a client" test named a piston head **and** a falling sand
  block; the piston half stands, the sand half is now the section's
  exception. The landing page carried the same sentence and is fixed with it.~~

### `server/server-tick.md`

- ~~"This is the only point in a tick where player input enters the
  world."~~ WRONG — above.
- ~~"Each row below is its own profiler section."~~ WRONG. Row 1 (suspend
  flushing) has no `profiler.push` at all and row 8 is three sections
  (*debugSubscribers*, *gameTests*, *server gui refresh*);
  `MinecraftServer.serverActivityMonitor` ticks after the final `pop`
  (`MinecraftServer.java:1206-1286`). Now "all but the first are a profiler
  section of their own; the debug row is three".
- ~~The keep-alive's position in `ServerGamePacketListenerImpl.tick`.~~
  WRONG: it runs **first** of the four, not last, and all four sit inside
  `if (server.isPaused() || !tickPlayer())`
  (`ServerGamePacketListenerImpl.java:300-315`).
- ~~"`DedicatedServer.handleConsoleInputs`, the only way a console or RCON
  command reaches the Server thread."~~ WRONG for RCON:
  `RconClient` to `DedicatedServer.runCommand` to `executeBlocking`
  (`DedicatedServer.java:780-786`, `RconClient.java:76`) — the task queue,
  not the console list.
- ~~"a sprint … doing none of the housekeeping".~~ Contradicted by the
  page's own rider two sections earlier: `ChunkMap.processUnloads` drains
  `unloadQueue.size() - 2000` entries whether `haveTime` is true or not
  (`ChunkMap.java:496-501`). Now "almost none … the exception being the
  unload queue".
- ~~The player-info interval, "not a multiple of
  `PlayerList.SEND_PLAYER_INFO_INTERVAL`, 600 ticks".~~ WRONG twice: it is
  `if (++this.sendAllPlayerInfoIn > 600)` — a counter, not a `tickCount`
  modulo, and therefore every 601st call (`PlayerList.java:493-497`). The
  constant itself is declared and never referenced. Matching sentence on
  `players-and-sessions` fixed.
- ~~**Verified clean and worth keeping**: `MinecraftServer.haveTime`'s three
  ways to yes and `shouldRun`'s age rule (`:942-943, :982-983`), the three
  things the budget gates, the `tickChildren` row order, the two writes per
  client, and `anatomy`'s compression (session B's open line) — the budget's
  count and the sprint conclusion both survive.~~

### `server/server-level-tick.md`

- ~~"Nothing in the game sends a block update at the moment a block
  changes."~~ WRONG — above; scoped to "almost nothing", with the exception
  named where the page tests it.
- ~~"a piston head or a falling sand block lands in the tick after the one
  that moved it."~~ WRONG on the sand half — above.
- ~~Figure 2's "EntityTickList.forEach, a piston extends and changes a
  block".~~ WRONG lane of the tick: a piston moves from
  `Level.tickBlockEntities` via `MovingPistonBlock.getTicker` to
  `PistonMovingBlockEntity.tick` (`MovingPistonBlock.java:65-66`), and its
  first half comes from `runBlockEvents`. The arrow's *conclusion* survives
  — both run after the broadcast — so only the named step changed.
- ~~"The first statement of the tick … is
  `EnvironmentAttributeSystem.invalidateTickCache`."~~ WRONG: it is the
  third, after `Profiler.get()` and `handlingTick = true`
  (`ServerLevel.java:329-333`). "Before the border, before the weather" is
  right (`:337-341`). Now "the first thing the tick does to the world". Same
  wording fixed on the landing page and softened on `lectures.md:77`.

### `server/players-and-sessions.md`

- ~~"`TeleportTransition.createDefault` falls back to the world spawn. That
  last branch is the expensive one."~~ WRONG on the second half — the
  pass-2 shape exactly. `missingRespawnBlock` and `createDefault` differ in
  one boolean and both build their position with `findAdjustedSharedSpawnPos`
  to `ServerPlayer.adjustSpawnLocation` (`TeleportTransition.java:39-53`), so
  both block the Server thread on the same search.
- ~~"the four paths that take a player out of a `ServerLevel`."~~ There is a
  fifth: `ServerPlayer.showEndCredits` removes the player with
  `Entity.RemovalReason.CHANGED_DIMENSION` (`ServerPlayer.java:1197-1199`),
  and it is the departure leg of the end-credits respawn the page makes its
  centrepiece. Named, without disturbing the four-way comparison.
- ~~"The `ChunkLoadCounter` … feeds nothing but the client's progress
  bar."~~ Only true of the integrated server; on a dedicated server the
  listener is the `LoggingLevelLoadListener` boot already closed
  (`DedicatedServer.java:96`), and nothing reaches a remote client.
- ~~"`PlayerList.isOp`, which also admits the singleplayer owner."~~ Dead
  branch on the only list where `DedicatedPlayerList.isWhiteListed` runs:
  `DedicatedServer.isSingleplayerOwner` returns constant `false`
  (`DedicatedServer.java:795-797`).
- ~~"The singleplayer owner is exempt from all of it" (the three kicks).~~
  WRONG: only `ServerCommonPacketListenerImpl.keepConnectionAlive` asks
  (`:127`); the idle kick and both flying kicks have no owner test
  (`ServerGamePacketListenerImpl.java:311, 328, 347`).
- ~~"three handlers hopping to Server" in the cast.~~ Four —
  `ServerConfigurationPacketListenerImpl.java:151, 167` and the two it
  inherits at `ServerCommonPacketListenerImpl.java:104, 110`.
- ~~"Entering the level is the last step."~~ Five calls follow
  `ServerLevel.addNewPlayer` inside `PlayerList.placeNewPlayer`
  (`PlayerList.java:198-203`), the last of them `resumeFlushing` — and the
  page's own Figure 2 already drew them.

### `server/starting-a-server.md`

- ~~The opening paragraph's frame: "Between those two lines the server
  opened a data pack stack, built every registry … and started listening on
  25565."~~ WRONG. Between *Preparing level* (`DedicatedServer.java:250`)
  and *Done* (`:256`) exactly one statement runs — `loadLevel()` at `:251`.
  Five of the six were over before the first line printed. The hook survives
  and the frame is inverted; the rewrite is logged in `pass5.md`.
- ~~"`MinecraftServer.forceDifficulty` (empty here, overridden by the
  integrated server)."~~ **Backwards.** `IntegratedServer` has no override;
  `DedicatedServer.forceDifficulty` is the sole one and pushes
  *server.properties*' difficulty onto the world every boot
  (`MinecraftServer.java:447`, `DedicatedServer.java:367-370`).
  `reference/level-data-and-rules.md:266` already had this right.
- ~~"they are the only non-daemon threads besides the Server thread
  itself."~~ WRONG: `Util.IO_POOL = makeIoExecutor("IO-Worker-", false)` —
  `false` is the daemon flag (`util/Util.java:110`), and the pool is
  squarely in the boot path. `GenericThread.start` never sets the flag, so
  the RCON/query half of the claim is right (`GenericThread.java:22-31`).
- ~~"Only one diagram in this book has the JVM main thread as a lane."~~
  Three do (`anatomy.md:50`, `identifiers-and-registries.md:119`, this
  page) — and the page names `anatomy`'s one sentence later. Deleted rather
  than re-scoped, per session A's and B's precedent.
- ~~Figure arrow 7, "packs opened" on the Worker lane.~~ WRONG:
  `WorldLoader.load` runs `PackConfig::createResourceManager` on the
  **main-thread** executor (`WorldLoader.java:33`), which the page's own
  prose says. Split into its own arrow.
- ~~Figure arrows 11 and 12, the `DedicatedServer` constructor before
  `spin`.~~ Inverted: the constructor is the factory `spin` calls, after it
  has built the `Thread` and set priority 8 (`MinecraftServer.java:305-323`,
  `server/Main.java:214-228`) — which the page's prose already said.
- ~~`JsonRpc.create` **throws** `IllegalStateException` on a bad secret rather
  than skipping the listener (`JsonRpc.java:26-29`) — it kills the boot; now
  said. And `MinecraftServer.SPAWN_POSITION_SEARCH_RADIUS` is declared and
  never referenced — `setInitialSpawn` spells 5 and 11 as literals
  (`MinecraftServer.java:212, 536-541`); the value is right, the causal link
  was not.~~

### `server/how-a-server-dies.md`

The page pass 2 never saw. Its three-way argument holds — `/stop` and a
crash really do run the same `finally`, and the watchdog really does not —
but nine claims around it did not.

- ~~"A server stuck on *Saving chunks* is stuck with no watchdog left
  watching it."~~ WRONG after a crash, which is one of the two endings the
  sentence covers. `ServerWatchdog.run` loops on `isRunning()`, and
  `MinecraftServer.running` is cleared **only** by `MinecraftServer.halt`
  (`:771-772`) — which the crash path never calls. The drain loop resets
  `nextTickTimeNanos` every pass (`:719`); the flush save that follows
  resets nothing, so a slow enough save after a crash can be shot mid-write.
  The durability answer now carries the asterisk.
- ~~"the world clock, the weather, the spawn point and the game rules"
  written by `level.dat`.~~ A 1.21-era fact. `PrimaryLevelData.setTagData`
  writes no weather and no game rules (`PrimaryLevelData.java:95-118`);
  weather is `WeatherData` (*weather*), rules are `GameRuleMap`
  (*game_rules*), the clock is `ServerClockManager` (*world_clocks*), all
  `SavedData` written by `SavedDataStorage` alongside. The conclusion
  survives — `saveAllChunks` schedules that write on every call — and
  `reference/level-data-and-rules.md:26-30, 47` already had it right.
- ~~"a departing player's tickets go with them, which is what lets the next
  step ever finish."~~ Unsupported: `PlayerList.removeAll` only calls
  `connection.disconnect` (`PlayerList.java:765-770`), and its index loop
  would skip players if `remove` ran inside it. What terminates the drain is
  `ServerChunkCache.deactivateTicketsOnClosing` (`MinecraftServer.java:724`),
  as the page says fifteen lines later.
- ~~"Closing the game window … goes through the 'Client Shutdown Thread'
  hook."~~ WRONG: `Window.shouldClose` to `Minecraft.stop`
  (`Minecraft.java:1202-1203`) ends the frame loop and `Main` then calls
  `exitWorldAndClose` (`client/main/Main.java:283`). The hook is the
  kill-signal backstop and finds `singleplayerServer` already null
  (`:240-251`).
- ~~"every dirty chunk that has waited out its per-chunk spacing."~~
  `ChunkMap.saveAllChunks`'s non-flush branch opens with
  `nextChunkSaveTime.clear()` (`ChunkMap.java:453`), so the ten-second
  spacing never gates an autosave. Makes the durability conclusion stronger.
- ~~"Four other places call the same method."~~ Five on this side of the jar
  — the page missed `GameTestServer.halt(false)` (`:230`) and named the
  JSON-RPC entry point one layer too high
  (`MinecraftServerStateServiceImpl.java:45`); the client adds three.
- ~~`ChunkMap.hasWork`'s disjuncts.~~ Nine, not the eight listed: the page
  omitted `unloadQueue` (`ChunkMap.java:479-481`).
- ~~`SuppressedExceptionCollector` "accumulating every … since boot".~~ It
  keeps the latest **eight** in full plus counts
  (`SuppressedExceptionCollector.java:29-30`).
- ~~The drain's ordering, in figure 1 arrow 9 and the prose.~~ The one
  millisecond deadline is set **before** the per-level calls, not after
  (`MinecraftServer.java:719-729`).
- ~~*multiplayer.disconnect.server-shutdown*~~ is *server_shutdown*
  (`PlayerList.java:767`). Italicised, so `verify_names.py` cannot see it.
- ~~The cast's "two process-wide pools".~~ `Util` has three
  (`BACKGROUND_EXECUTOR`, `IO_POOL`, `DOWNLOAD_POOL`); `shutdownExecutors`
  stops two (`util/Util.java:109-111, 295-298`).
- ~~**Verified clean**: both sequence diagrams arrow by arrow (19 of 19 and
  11 of 11); `PacketProcessor.close` dropping packets already queued
  (`PacketProcessor.java:34-46`) and being `stopServer`'s first statement
  (`MinecraftServer.java:688`); `MinecraftServer.reportChunkSaveFailure`'s
  four consequences (`:2500-2506`); `ServerWatchdog.exit`'s ten-second
  `Runtime.halt` (`ServerWatchdog.java:108-124`).~~

### `server/README.md` (the landing page)

- ~~"a change an entity makes always reaches you a tick later than a change a
  command makes."~~ WRONG at both ends. A console or RCON command runs in
  `DedicatedServer.tickConnection`, which `tickChildren` calls **after** the
  levels loop (`MinecraftServer.java:1251-1253`,
  `DedicatedServer.java:469-471`), so it is exactly as late as a piston; and
  falling sand sends its own packet immediately. Only a *player's* command
  packet, handled in `processQueuedPackets` before `tickServer`, is early.
- ~~Figure arrow 6, "the loop's finally, however it is reached".~~ Two of
  the three endings reach it; the watchdog's `System.exit` leaves the Server
  thread wedged inside the loop (`MinecraftServer.java:875-887`,
  `ServerWatchdog.java:108-124`) — which is the page's own hook three lines
  below.
- ~~"`ServerLevel.tick` throws away in its very first statement."~~ Third —
  above.
- **Addition 2, done in full.** All five *before you start* entries are used
  by a sentence, not merely linked (`tickets-and-loading` seven times,
  `anatomy` four, `environment-attributes` twice, codecs and registries once
  each), and `check_deps.py` is green. One entry was **missing**:
  `starting-a-server.md:151` leans on `foundations/resource-system` for the
  staged load, and the section named only codecs and registries, so it is
  added. `lectures.md`'s two Part III counts re-derived and both right:
  seven later parts assume the tick pair (IV, V, VI, VII, VIII, IX, XIII),
  and Part III is the earliest of the six other parts that lean on the
  environment page (III, VI, IX, X, XI, XII).
- **Rejected after re-derivation**: the agent called
  `networking/protocol-phases` a missing dependency because the page "uses
  phase vocabulary undefined here". It does not — *phase* appears on
  `players-and-sessions` only in the cast row and in the hand-off paragraph
  itself, which says outright "this page starts where that one hands over".
  That is the pointer shape session A ruled belongs outside *before you
  start*.

### The tool bug — the sixth of pass 4

Found by suspecting the tool first, when four settled notes would not leave
the checklist. `pass4_queue.py` deliberately splits a continuation line that
opens on a page marker into its own unit, for the style sessions H and I
used inside one long bullet. But it applied that to *any* continuation line
beginning with a backticked slug and a dash — including one mid-sentence —
and the split-off unit did not inherit its parent's strike. So **striking a
bullet could never settle it**: the phantom child came back on every later
checklist for ever, starting mid-sentence. Session D's entry alone spawned
four. Fixed: a unit split out of a struck parent inherits the strike.

### For other parts' sessions

- **Part IX** — `protocol-phases` owns the login and configuration handlers
  this part hands to. Nothing found here contradicts it, but session I
  should know that `handleChat` and both chat-command packets are *not*
  `ensureRunningOnSameThread` handlers, which is a claim about the phase's
  thread discipline.
- **Reference** — `reference/threads.md` marks RCON and query **non-daemon**
  and is right, but says nothing about `Util.ioPool`'s *IO-Worker* threads
  being non-daemon too, which is what makes "no non-daemon thread is left"
  depend on `Util.shutdownExecutors`. A completeness gap, not an error; for
  session O.
- **The plan's session C line** said "the four-path comparison in
  `players-and-sessions` against authlib". Those are two different things:
  the four paths are join, death, dimension and disconnect and have no
  authlib in them, and the page's only authlib surface is `GameProfile` (the
  session-server round trip belongs to Part IX's `protocol-phases`). The
  standing *library facts* item should name Part IX for that, not this page.

## Session B — Part I Anatomy · Part II Foundations (pass 4) *(2026-09-04)*

Ten pages, one adversarial agent each on Opus; the order work, the tool
audit and every *wrong* re-derived by the session before a sentence moved.
Session C's eleven per-page bullets are struck below. **Every one of the ten
pages had at least one wrong claim**, pass 2's finding holding for a third
time.

### The finding that crossed three pages

**A frozen registry has two things swapped after the freeze, not one.**
`tags.md:17`, `foundations/README.md`'s figure edge 4 and — by implication —
`identifiers-and-registries.md`'s freeze section all said the tag table was
*the one part*. It is not:
`ReloadableServerResources.updateComponentsAndStaticRegistryTags` applies
the pending tags on one line and the pending **component prototypes** on the
next (`server/ReloadableServerResources.java:83-86`), and
`Holder.Reference.bindComponents` (`core/Holder.java:263`) carries no frozen
guard. Found independently by the `tags` and `foundations/README` agents and
verified by the session; the figure was self-contradictory, since its own
edge 5 named the second swap. All three fixed.

### `anatomy/README.md`

- ~~"It has **one** lecture" → Part I has two; `lectures.md:21-25` numbers
  both and `:640` calls the second "the second lecture". Now "its first
  lecture names four threads".~~
- ~~The hook, "**every diagram** in this book has lanes that assume you know
  which thread each one is on" → 195 mermaid blocks, of which 89 are
  sequence diagrams; and a lane is a **class**, not a thread
  (`reference/lanes.md`: 332 class lanes, 9 word lanes). Now "every sequence
  diagram … lanes that name classes and assume you know which thread each
  class is on". Same error in the *Diagram lanes* blurb.~~
- ~~"the **one worker pool** that everything else is serialised onto" →
  `util/Util.java:109-111` declares three pools, and `IOWorker.java:45`
  serialises region-file IO onto `Util.ioPool()`. The page's own lecture
  says "the pools". Now "the one CPU pool that chunk generation, lighting
  and section meshing all share" (`ChunkMap.java:187,190`;
  `LevelRenderer.java:772`).~~
- ~~The root figure claimed to cover every later part and omitted **Part
  II**, whose own landing page starts from the worker pool (reload *prepare*
  on `Util.backgroundExecutor()`, `Minecraft.java:698,1071`). Part II added
  to that arrow.~~
- ~~"The maps — *where the mass is*" is the title of `maps/biggest.md`, not
  of the atlas → "where everything is".~~

### `anatomy/anatomy.md`

- ~~**The login state machine does not run start to finish on Netty.**
  `ServerLoginPacketListenerImpl` is a `TickablePacketListener`
  (`server/network/ServerLoginPacketListenerImpl.java:50`) whose `tick()`
  (`:77-89`) finishes verification, does the dupe-disconnect wait and counts
  the 600-tick slow-login timeout — driven from the **Server thread** by
  `MinecraftServer.tickConnection` (`MinecraftServer.java:1295`) →
  `Connection.tick` (`network/Connection.java:391`). The *handlers* never
  hop, which is the true and narrower claim. Fixed on the figure's arrow and
  the Netty table row; **`reference/threads.md` said it in three places and
  is fixed too**. `networking/protocol-phases.md:11` and `:372` still say it
  — see *For other parts' sessions*.~~
- ~~The bootstrap ordering: "After argument parsing and crash-report
  preloading, `SharedConstants.tryDetectVersion` reads *version.json*" →
  `tryDetectVersion` is the **first statement of both mains**
  (`client/main/Main.java:64`, `server/Main.java:76`), before the option
  parser exists; `loadLibraries` (`:134`) precedes `CrashReport.preload`
  (`:168`); and `ClientBootstrap.bootstrap` (`:172`) runs **between**
  `Bootstrap.bootStrap` (`:171`) and `Bootstrap.validate` (`:174`), so the
  figure's arrow had the last two swapped. Both fixed.~~
- ~~"A background thread that dies reports through
  `BlockableEventLoop.delayCrash`, which parks the exception for the owning
  thread so the crash surfaces where the state it damaged lives" → wrong
  method and backwards rationale. The path is `Util.onThreadException`
  (`util/Util.java:326`) → `BlockableEventLoop.relayDelayCrash` (`:344`),
  and the delayed crash is a **single static slot**
  (`util/thread/BlockableEventLoop.java:29`) rethrown only where
  *propagatesCrashes* is set — `Minecraft` (`Minecraft.java:382`) and
  `DedicatedServer` (`DedicatedServer.java:96`), never `IntegratedServer`
  (`:77`). So a worker that dies in singleplayer surfaces on the
  **client**.~~
- ~~"nothing in the play path knows it is singleplayer" →
  `ClientPacketListener.handleUpdateTags` branches on
  `!connection.isMemoryConnection()` at `ClientPacketListener.java:1900`.
  Now "almost nothing", with the exception named.~~
- ~~"`IntegratedServer` … **disables native transport**" → it returns the
  client's own option (`IntegratedServer.java:230-232`), default **true**
  (`Options.java:1071`). And the packet rate limit is **not** relaxed:
  `IntegratedServer.getRateLimitPacketsPerSecond` returns 0 and
  `DedicatedServerProperties.java:150` defaults *rate-limit* to 0 as well.
  The chat and command spam thresholds *are* relaxed (0 against 10,
  `DedicatedServerProperties.java:152`). Sentence rebuilt around what is
  true.~~
- ~~"Everything else that matters is serialised onto **one of the four**" →
  broken by the page's own example: `IOWorker` runs on `Util.ioPool()`, its
  own *IO-Worker-n* pool. Reworded to "serialised onto a pool rather than
  given a thread".~~
- ~~The "Can't keep up" thresholds are **not** inside
  `processPacketsAndTick` or `waitUntilNextTick`; they are decided in
  `MinecraftServer.runServer` itself (`MinecraftServer.java:803-810`) from
  how far behind the deadline already is. The pointer sentence to *the
  server tick* now says so.~~
- ~~"One of **five**" entry points → the tree has six *main* methods; the
  sixth, `SnbtDatafixer`, starts nothing, and the page now says so.
  `client/data/Main` adds four providers, not three — `AtlasProvider` was
  missing.~~
- ~~"**Three** of `Minecraft`'s fields are nullable" reads as a count of the
  class's nullable fields, of which there are ten; reworded to "three of
  `Minecraft`'s nullable fields between them mean". The cast table's "in
  four fields, whether we are in a world at all" → three, since
  `Minecraft.singleplayerServer` answers *am I the host*.~~
- ~~`RenderSystem.initBackendSystem` does not install the clock: it
  **returns** it, and `Minecraft.java:460` calls `Util.setTimeSource`. The
  "entire notion of time" is a client fact, now scoped.~~
- ~~The cast's `BlockableEventLoop` thread cell said "one instance per
  owning thread"; the Server thread owns `MinecraftServer` **and** one
  `ServerChunkCache.MainThreadExecutor` per level, which the page says
  itself twenty lines later.~~
- ~~Verified clean and worth keeping: both loops arrow by arrow
  (`Minecraft.runTick` at `Minecraft.java:1216-1252`;
  `MinecraftServer.runServer` at `:783-834`), `spin`'s construct-then-start
  (`:305-323`), the 0-to-10 clamp, priority 10/8 above four cores, the
  8-player cap, *pause-when-empty-seconds* 60, and the memory channel.~~
- ~~**Still open**: pass4.md's session-D note asking whether `anatomy`'s
  compression of two `server-tick` invariants lost anything true. The
  `anatomy` half is checked — the pointer sentence was wrong and is fixed —
  and the `server-tick` half is session C's, so the line is left unstruck.~~
  Settled by session C: the budget's count (three) and the sprint conclusion
  both survive re-derivation on `server-tick`, so the compression lost
  nothing true.'

### `anatomy/what-this-book-skips.md`

- ~~`DataFixTypes.wrapCodec`'s examples were inverted: chunk storage and
  player data read the version themselves and never call it. Its only two
  callers are `PlayerAdvancements.java:75` and
  `DebugScreenEntryList.java:43`. And `updateToCurrentVersion` has **13**
  call sites outside its own declaration, not fifteen.~~
- ~~"the only callers are the server's own entry point and `DedicatedServer`"
  → true of *rcon*, which only `DedicatedServer` reaches; *jsonrpc* is
  referenced by six files including `BuiltInRegistries` and `Registries`,
  which the client loads at bootstrap. Rewritten to say which is which.~~
- ~~`BlockItemIds` is "six times the size of either" → 770 keys against
  `BlockIds`' 111 (7×) and `ItemIds`' 438 (1.8×).~~
- ~~The ten external users of `net/minecraft/references` are right in number
  and wrong in composition: `Blocks`, `Items`, five tag providers,
  `GrassBlock`, `MyceliumBlock` and `DecoratedPotPatterns` — two blocks and
  a block-entity class, not "three blocks".~~
- ~~The file-fixer "writes a move journal and a marker file" → one file,
  *upgrade_in_progress.json*
  (`util/filefix/FileFixerUpper.java:60,127,310`).~~
- ~~Session C's note that the treemap hatches "twelve of the fourteen" is
  **stale**: `net/minecraft/gizmos` and `com/mojang/realmsclient` both carry
  skip rects in the current `src/generated/packages-treemap.svg`. The one
  toured package still not drawn is `client/multiplayer/chat/report`, at
  depth 5. The figcaption stands.~~
- ~~Verified clean: all 16 sizes-table rows, all 15 side labels,
  7,055/719,302, 300 schemas / 420 fixes, the six post-effect chains, 996
  `PostChain` lines and the whole gizmos/rcon/legacy-ping/realms/audio
  section.~~

### `foundations/README.md`

- ~~"the other **eleven** parts" → twelve (thirteen parts, minus this one);
  `anatomy/README.md` gets the parallel sentence right.~~
- ~~"the *type* line at the top of **every** JSON file in a data pack" → tag
  files have no *type* (`data/minecraft/tags/block/logs.json` is a bare
  *values* list), and the direct-codec worldgen files (*biome*,
  *dimension_type*, *noise*) have none either. → "most of".~~
- ~~Figure edge 1, "**every** registry element is decoded by a codec" → 95
  of the 148 registries are built-in and their elements are constructed in
  Java (`Items.java:1692`). → "every **data-pack** registry element".~~
- ~~Figure edge 4 — the freeze finding above.~~
- ~~Figure edge 6, "**every** component value has a codec" → three of the
  111 `DataComponentType`s are transient and their codec is null:
  *creative_slot_lock*, *additional_trade_cost*, *map_post_processing* (the
  three `DataComponents` registrations with no persistent codec). → "every
  **persistent** component value".~~
- ~~Figure edge 7 and `codecs-nbt-json.md:341`, "`ComponentSerialization`
  is the **most-used codec in the game**" → unsupportable under any
  population the session tried: by files, `Codec.STRING` 96 >
  `Identifier.CODEC` 84 > `ComponentSerialization` 79; by raw occurrences
  the order flips, which is what makes it a superlative rather than a fact.
  Dropped on both pages, the substance kept.~~
- ~~Figure edge 10's second half, "the element registry is dynamic" → only
  11 of the 56 have a dynamic element registry at all; the rest are written
  inline. → "the elements come from the packs".~~
- ~~Teaser 1, "**The click sends no item data at all**" →
  `HashedStack.ActualItem` is a `Holder<Item>`, an int count and a
  `HashedPatchMap` (`network/HashedStack.java:44-46`): the item and the
  count cross in the clear and only the component values are hashed. The
  linked page said "component" and the teaser had degraded it. Fixed on
  both.~~
- ~~Teaser 3, "A failed reload deselects every pack" sat after a clause
  about the **server**, where a failed reload deselects nothing
  (`MinecraftServer.java:1700` is inside the success continuation). Scoped
  to the client.~~
- ~~Teaser 7, "the whole reason a pack can compose the game's behaviours" →
  at least four of the fifty-six are unreachable from a data pack. → "are
  why".~~

### `foundations/codecs-nbt-json.md`

- ~~"**A homogeneous numeric list is not a list.** `NbtOps`' list collectors
  start specialised" → backwards. `NbtOps.createCollector`
  (`nbt/NbtOps.java:697-734`) returns a generic collector for an empty list
  and reaches for the array collectors only when handed an existing array
  tag, and those degrade back to generic on a mismatch (`:842`). A codec
  building a fresh list gets a `ListTag`. Sub-section rewritten.~~
- ~~"`RegionFileVersion.VERSION_CUSTOM` is the marker meaning a chunk grew
  too big and lives in its own external file" → `VERSION_CUSTOM` is id 127,
  a custom-**compression** marker (`RegionFileVersion.java:43`,
  `RegionFile.java:186`); the external-file marker is `RegionFile`'s 128
  flag (`RegionFile.java:38`).~~
- ~~`BlockEntity.saveWithId` listed among the `CompoundTag`-returning final
  shells → it has only the `ValueOutput` form
  (`world/level/block/entity/BlockEntity.java:143`); the three with a
  `CompoundTag` shell are `saveWithFullMetadata` (`:114`),
  `saveWithoutMetadata` (`:148`) and `saveCustomOnly` (`:177`).~~
- ~~`ByteBufCodecs.TRUSTED_COMPOUND_TAG` "carries block-entity update
  payloads, chat components and dialogs" → **one** call site,
  `ClientboundBlockEntityDataPacket.java:18`.~~
- ~~"Two of the **four ops in the table above**" named `NullOps`, which is
  in no table on the page.~~
- ~~"There are **two ways** to make a `RegistryOps`" → the two named are
  routes; both end at `RegistryOps.create`
  (`resources/RegistryOps.java:22,26`), which other callers reach
  directly.~~
- ~~The hook, as on the landing page.~~

### `foundations/identifiers-and-registries.md`

- ~~**The hook's causal clause.** "registered in sorted order of their ids,
  which is exactly why the client can rebuild the same numbers from the same
  list of names" → the server sorts
  (`ResourceManagerRegistryLoadTask.java:54`), and the client **does not**:
  `NetworkRegistryLoadTask.load`
  (`resources/NetworkRegistryLoadTask.java:45-64`) iterates the entries in
  the order the packet lists them and registers them in that order.
  Rewritten: the sort makes the *server's* numbering independent of which
  file finished first.~~
- ~~"`BuiltInRegistries.createContents` … **forces the class init** of
  `Items`, `Blocks`, `EntityType` and the rest" → all three are already
  initialised: `Bootstrap.bootStrap` (`server/Bootstrap.java:46-66`) runs
  `FireBlock.bootStrap`, `EntityTypes.PLAYER` and
  `CauldronInteractions.bootStrap` **before** `BuiltInRegistries.bootStrap`.
  The registering class is `EntityTypes`, not `EntityType`.~~
- ~~"there is a **third data-driven directory** …
  `Registries.componentsDirPath`" → it is a datagen **reports** path with
  one caller (`data/PackOutput.java:38`) and no directory under
  `reference/26.2/data/`.~~
- ~~"with **id 0 reserved** so that an inline `Holder.Direct` can be sent
  instead", said of every registry element → true only of
  `ByteBufCodecs.holder` (`network/codec/ByteBufCodecs.java:647-670`), which
  writes id + 1. `ByteBufCodecs.holderRegistry` (`:643`), which
  `Item.STREAM_CODEC` uses, writes the raw id — as the page's own hook
  requires.~~
- ~~"**Only** `ClientRegistryLayer`, `RegistryDataCollector` and
  `KnownPacksManager` are client-only" → six of the page's classes are,
  adding `ClientPacketListener`, `ClientConfigurationPacketListenerImpl` and
  `IntegratedServer` (checked against `server-classes.txt`).~~
- ~~"**Most** dynamic registries also carry a `RegistryValidator`" → **13 of
  47**, every one an entity-variant registry and every one
  `RegistryValidator.nonEmpty` (enumerated from
  `resources/RegistryDataLoader.java`'s registry-data entries).~~
- ~~The figure's "one empty registry per `Registries` key" → 95 registries
  for 148 keys.~~
- ~~"`MappedRegistry.validateWrite` throws on **every mutation**" after the
  freeze → `MappedRegistry.prepareTagReload` requires the frozen flag, and
  the components are rebound beside the tags. Softened to "every ordinary
  write" with both exceptions named.~~
- ~~"The tag half of that proof is **why** there are two tag tables" →
  causality reversed; the two tables are what make the proof possible.~~
- ~~Counts re-derived and **all three confirmed**: 148 keys, 147 distinct
  strings (*dimension* is `DIMENSION` and `LEVEL_STEM`), five intrusive
  registries (five intrusive-holder registrations, five
  `createIntrusiveHolder` callers).~~

### `foundations/resource-system.md`

- ~~The command is **/serverpack push|pop**, not */resourcepack*
  (`server/commands/ServerPackCommand.java:22`); no */resourcepack* exists.
  Both occurrences fixed.~~
- ~~Figure 3 placed `setOverlay` after the prepare and apply;
  `Minecraft.java:1071` sets it in the same statement as `createReload`.~~
- ~~"the first listener to throw **aborts the whole reload rather than
  letting the rest finish**" → `Util.sequenceFailFast`
  (`util/Util.java:753`) cancels nothing; the game has
  `Util.sequenceFailFastAndCancel` (`:760`) and does not use it here. What
  never happens is the applies.~~
- ~~"a pack edited on disk mid-reload is **absolutely observable**" → true
  of a folder pack; `FilePackResources` holds its zip open.~~
- ~~"the test pack" among the built-ins → `BuiltInPackSource.TESTS_ID`
  (`:29`) is referenced nowhere else.~~
- ~~"(built-ins never produce one)" of `CompositePackResources` → true of
  the vanilla pack only.~~
- ~~"*allowed_symlinks.txt* is read through `DirectoryValidator`" →
  `LevelStorageSource.parseValidator` reads it (`Minecraft.java:403`).~~
- ~~"`TextureManager` does exactly this" in a sentence about
  `SimplePreparableReloadListener` → `TextureManager` implements
  `PreparableReloadListener` (`TextureManager.java:29`).~~
- ~~The count of **twenty** client reload listeners, the registration order,
  the barrier semantics, the *.mcmeta* rule, both pack-format pairs and the
  server's three listeners all re-derive exactly.~~

### `foundations/tags.md`

- ~~The hook — the freeze finding above.~~
- ~~The cast's `Registry.PendingTags` row said "built on a worker" → only at
  world load; `/reload` builds on the server thread
  (`MinecraftServer.java:1688`) and the client on its game thread
  (`ClientPacketListener.java:1889`). The row contradicted the `TagLoader`
  row above it.~~
- ~~**The apply does not run on the Server thread at world load.**
  `WorldLoader.load` applies on its main-thread executor
  (`server/WorldLoader.java:54-56`), which is `Util.blockUntilDone`'s queue
  on a dedicated server (`server/Main.java:183`) — the Server thread does
  not exist yet — and `Minecraft` on the client
  (`WorldOpenFlows.java:196`). Only `/reload` applies on the Server thread.
  The diagram's bar and both "it is safe because the server thread…"
  sentences fixed.~~
- ~~The required-flag wrinkle was the wrong wrinkle: `TagEntry.build`
  (`tags/TagEntry.java:65-85`) returns *not required* on a miss
  **whichever** lookup it was given, so an optional entry never kills a tag.
  What the two element lookups differ on is where a *required* id is looked
  up (`tags/TagLoader.java:223-237`).~~
- ~~"**The cycle is broken silently** … with no diagnostic at all" → both
  tags are dropped and both are logged. `TagLoader.build`'s tag lookup reads
  the new-tags map, which the not-yet-built partner is absent from, so each
  fails as a missing required reference and logs *Couldn't load tag*
  (`tags/TagLoader.java:125-153`).~~
- ~~"the reloadable layer has tags too" → `ReloadableServerRegistries.java:66`
  calls the **void** overload (`tags/TagLoader.java:168-170`), which
  discards the map; nothing binds them, so a loot registry answers empty for
  every tag key.~~
- ~~"The **two throws**" → three distinct messages.~~
- ~~`ResourceSelectorArgument` listed among the *#tag* argument types → it
  is a glob over ids (`commands/arguments/ResourceSelectorArgument.java:30`,
  examples *minecraft:\**) and contains no hash at all.~~
- ~~Confirmed: the 3/9/4 *logs* JSON counts, the twenty key catalogues, the
  three ordered apply steps, `AxeItem.STRIPPABLES`, and 12 of the 14 diagram
  arrows.~~

### `foundations/data-components.md`

- ~~**The binding asymmetry is inverted.** The page said a *multiplayer*
  client binds only networkable registries. It is the **singleplayer**
  client that does: `ClientConfigurationPacketListenerImpl.java:177` passes
  `connection.isMemoryConnection()` into
  `RegistryDataCollector.collectGameRegistries`, whose parameter is
  *tagsAndComponentsForSynchronizedRegistriesOnly* and which negates it into
  the *includeSharedRegistries* of `updateComponents`
  (`RegistryDataCollector.java:142-167`). As written, no multiplayer client
  could decode a stack. Fixed, with the reason singleplayer can skip them.~~
- ~~Figure 2's "the next `ServerPlayer.tick`" and the "**Once a tick**, the
  menu compares" heading → for this trace,
  `ServerGamePacketListenerImpl.handleContainerButtonClick` (`:2271-2275`)
  calls `broadcastChanges` synchronously as soon as
  `AbstractContainerMenu.clickMenuButton` accepts.~~
- ~~The trace's set of `DataComponents.ENCHANTMENTS` → for the enchanted
  book the diagram itself transmutes to,
  `EnchantmentHelper.getComponentType` (`:91-93`) writes
  `DataComponents.STORED_ENCHANTMENTS`.~~
- ~~"built … on the reload worker" is a server fact; the client binds during
  configuration.~~
- ~~All ten counts re-derived clean (111 component types, 3 transient, 29
  slash ids, 10 common, 15 predicate kinds).~~

### `foundations/text-components.md` *(never fact-checked before)*

- ~~"`DeathMessageType.FALL_VARIANTS` and `INTENTIONAL_GAME_DESIGN` take the
  other **two** branches" → `CombatTracker.getDeathMessage`
  (`world/damagesource/CombatTracker.java:92-112`) has four: an empty combat
  log is *death.attack.generic*, and the fall branch is taken only when
  `CombatTracker.getMostSignificantFall` returns non-null.~~
- ~~"parses **every** at-sign into a `MessageArgument.Part`" →
  `MessageArgument.java:146-165` skips one whose selector parse fails on a
  missing or unknown selector type and leaves it as text.~~
- ~~"**Every setter** returns a new `Style`" → `Style.withBold` and its
  siblings return the same object when the value is unchanged
  (`network/chat/Style.java:123-129`).~~
- ~~"The server reads the message once, for its log" → only on the
  `PlayerList.broadcastSystemMessage` path. A victim on a team whose
  death-message visibility is not *always* goes through
  `PlayerList.broadcastSystemToTeam` or
  `PlayerList.broadcastSystemToAllExceptTeam`
  (`ServerPlayer.java:997-1004`), neither of which logs, and
  `Team.Visibility.NEVER` matches neither branch, so the message reaches
  nobody at all.~~
- ~~**Both claims session C flagged as unverified are settled.** The **top**
  of the pack stack wins a language key —
  `FallbackResourceManager.getResourceStack` returns the reversed list and
  `ClientLanguage.appendFrom` puts in that order, so later overwrites
  earlier. And the dedicated server **does** bundle *en_us.json*:
  `net/minecraft/locale/Language` is in `server-classes.txt` and its static
  default instance reads the file off the classpath.~~
- ~~All 26 counts re-counted correct; the "never a *type* key on encode"
  absolute confirmed down to `NbtOps.compressMaps`.~~

### `foundations/data-driven-types.md` *(never fact-checked before)*

- ~~**The fifty-six is right and its stated criterion was not.** Re-derived
  by the session: a `Registry.byNameCodec` dispatch on a `BuiltInRegistries`
  field has **57** distinct registries. The page's three tables list 56; the
  difference is `GAME_RULE` and `STAT_TYPE` (in the grep, filed under *what
  does not follow the pattern* because the registry name is a map **key**,
  not a field's value) and `TRIGGER_TYPES` (in the tables, dispatching
  through `ExtraCodecs.dispatchOptionalValue` instead). The criterion is now
  stated as *the value of a field*, with both exclusions named. The 31/23/2
  split stands.~~
- ~~"**Four** of the instances accept a bare value" → seven: the page's four
  plus `FloatProviders.CODEC` (`valueproviders/FloatProviders.java:12`),
  `NbtProviders.CODEC` and `ScoreboardNameProviders.CODEC`. "**Two** accept
  a bare list" → three, adding `SlotSources` through
  `GroupSlotSource.INLINE_CODEC` (`world/item/slot/SlotSources.java:21`),
  which is not a loot instance.~~
- ~~"the ones that are not fall into **three groups**" → four registries sit
  outside all three (`TICKET_TYPE`, `MAP_DECORATION_TYPE`,
  `POINT_OF_INTEREST_TYPE`, `VILLAGER_TYPE`), now named.~~
- ~~`BuiltInRegistries.ATTRIBUTE_TYPE` listed as "a key, not a kind" →
  `AttributeTypes.CODEC` (`world/attribute/AttributeTypes.java:38`) has **no
  reader in the tree**; the attribute name a file uses as a key belongs to
  `BuiltInRegistries.ENVIRONMENT_ATTRIBUTE`
  (`world/attribute/EnvironmentAttributeMap.java:20`).~~
- **Not acted on, for the record**: the agent also reports
  `LOOT_SCORE_PROVIDER_TYPE`'s and `SLOT_SOURCE_TYPE`'s *where the elements
  live* cells wrong, `POSITION_SOURCE_TYPE`'s "one enchantment effect" a
  name collision with `SpawnParticlesEffect`'s own nested position source,
  the *features and placement* trace not walking "all nine" tree
  sub-objects, and 13 of the 29 synchronized registries using a distinct
  network codec rather than the direct codec. Four table cells and one
  premise; **left for session N or a follow-up**, since each needs the
  owning part's page open beside it.

### The tool bug — the fifth of pass 4

`tools/gen_reference.py`'s built-in regex spelled the register helpers out
and so missed `registerSimpleWithIntrusiveHolders`, the one
`BuiltInRegistries.BLOCK_ENTITY_TYPE` uses (`BuiltInRegistries.java:202`).
`src/reference/registries.md` therefore published **94 built-in** and a
blank *kind* cell for *block_entity_type*. The regex now matches any
register helper, the count is **95**, and the row is right. No page cited
the 94. Found by re-deriving the population behind the landing page's figure
edge 1 — the tool suspected first, as the charter asks.

### Order and dependency (addition 2)

`check_deps.py` green. Part I's *before you start* is "Nothing" and its four
cross-part links are all forward hand-offs in `anatomy.md`'s body, which
session A's ruling puts outside the section. Part II's single entry
(`anatomy/anatomy`) is used at `identifiers-and-registries.md:139`. Both
parts' `lectures.md` sections match their landing pages' order and hooks.

### For other parts' sessions

- ~~**Part IX** — `networking/protocol-phases.md:11` ("every server-side
  handler in the handshake and login phases runs on the Netty thread") and
  `:372` ("handshake and login listeners run to completion on the Netty
  thread") carry the login-tick error corrected on `anatomy.md` and
  `reference/threads.md` above. The fix is the same: the *handlers* never
  hop; the login listener's `tick` runs on the Server thread.~~
- ~~**Part VII** — `data-driven-types`'s four wrong table cells (above) point
  at the loot and slot pages.~~

## Session A — The frame (pass 4) *(2026-09-04)*

The introduction, the atlas, `lectures.md`, the parts-dependency figure, the
thirteen landing pages as claims about order, and the Reference tier. The
order work (the charter's addition 2) and the generated views' one-sample
check were the session's own; one adversarial agent per page did the rest.

### Addition 2 — order and dependency, done in full

`tools/check_deps.py` opened with two failures and three forward-link
reports. All five were real, and all five are fixed. The checker is green
and is now `tools/deploy.sh`'s **fourth gate**, after names, mermaid and
lanes.

- **`lectures.md`:618 — the environment attributes row.** Table said the
  page is assumed by Parts III, VI and XI; the landing pages said only XI.
  The table was right and two landing pages were missing the entry.
  Part III uses it: `server-level-tick.md` opens the tick on
  `EnvironmentAttributeSystem.invalidateTickCache`
  (`ServerLevel.tick`, `server/level/ServerLevel.java:333` — the statement
  before the world border and the weather) and has
  `Level.updateSkyBrightness` read `EnvironmentAttributes.SKY_LIGHT_LEVEL`
  out of it rather than deriving sky light from the time of day
  (`world/level/Level.java:532-534`). Part VI uses it:
  `ai-goals-and-brains.md` takes the villager schedule from a data-pack
  `Timeline` and says the page "only asks it a question". → **added to both
  landing pages** (`entities/attributes.md`'s mention is a
  same-words disambiguation, not a use, and was not counted). Part III's
  entry states the cut the way the lecture map states it: tickets and
  loading keeps until Part IV, the environment page does not.
- ~~**`lectures.md`:619 — the blocks and states row.** Table said Parts VI and
  VII; no page in Part VII links or leans on `blocks-and-states`, and Part
  VII's landing page assumes `block-interaction` instead — which is what
  the row's own gloss ("how a chest is opened") was describing. → **row
  corrected to VI**, gloss narrowed to the collision shapes.~~ Re-derived and
  CONFIRMED by session E.
- **Three forward links in *before you start* with no dashed arrow.** All
  three were hand-forwards or pointers, not dependencies, so the fix was to
  move them out of the section, not to draw an arrow.
  - ~~Part IV listed `blocks-and-states` in a sentence that says outright
    "It does hand two things forward" → moved to the end of *the shape of
    the part*.~~ CONFIRMED by session E.
  - Part VI listed `prediction-and-acks` to say the dependency runs the
    other way ("watch this part first") → moved to *the shape of the part*.
  - Part IX listed `the-client-loop` as "the deeper version" of anatomy's
    two-loops figure. Both Part IX pages that name it cite anatomy as the
    shape and the client loop as "the detail" / "the arithmetic"
    (`the-connection.md:105`, `what-the-client-is-told.md:442`) — a pointer,
    not a prerequisite → de-linked in that section, and
    **`lectures.md`:623's third column lost "and IX's deeper version"**.
- **A fourth: Part VI's *before you start* linked `scheduled-ticks` only to
  say it is *not* needed.** An anti-dependency read by the tool as a
  dependency → de-linked (the words stay).
- **A count, in the sentence over the dependency table.** "Nine pages carry
  most of the graph … a viewer who has watched these nine" — the table has
  nine rows but ten pages, because the first row is the server tick *and*
  the level tick. → **ten**, with the reason said.
- **`tools/check_deps.py` had a bug** (suspect the tool first): the
  *unlisted* half excluded `/README` targets and the *unused* half did not,
  so every "read Part N first" entry — six of them — was reported as an
  unused dependency by construction, because no page in a part ever links
  another part's landing page. Fixed.
- **The six remaining report-only entries are judged real**, and are
  unlinked rather than unused: Part X ← `anatomy/anatomy` (the-client-loop
  is about nothing else) and `entities/authority` (`the-client-level` opens
  on "not an authority either"); Part VI ← `world/chunk-anatomy`
  (`entity-lifecycle` spends the chunk model throughout — spawnable chunks,
  "no ticking chunk there", the unload queue); Part IV ←
  `identifiers-and-registries` and Part XII ← that and `codecs-nbt-json`
  (both parts use them on most pages). `mentions()` sees a link or a
  backticked slug and none of these has one; **adding the missing
  cross-links is pass-5 work** and is logged there.

### The eight generated Reference views — one sample each, all confirmed

Re-derived by hand from the decompile, against `tools/gen_reference.py`'s
output. Paths relative to `reference/26.2/net/minecraft/`.

| view | sample re-derived | verdict |
|---|---|---|
| packets | `login` group: 5 clientbound, 4 serverbound (`network/protocol/login/LoginPacketTypes.java:10-18`) | CONFIRMED |
| registries | 148 keys, and `attribute_type` → `AttributeType<?>`, built-in (`core/registries/Registries.java:182`; `BuiltInRegistries`). The 149th `ResourceKey<Registry<` in the file is `createRegistryKey`'s own signature | CONFIRMED |
| components | 111 registrations, and `max_damage` → `Integer`, persistent **and** synced (`core/component/DataComponents.java:116-118` — `persistent(…).networkSynchronized(…)`) | CONFIRMED |
| gamerules | 59 rules (47 `registerBoolean` + 12 `registerInteger`), and `command_block_output` → Boolean, chat, default `true` (`world/level/gamerules/GameRules.java:31`) | CONFIRMED |
| entity data serializers | wire id 3 = `FLOAT`, from the static block's registration order (`network/syncher/EntityDataSerializers.java:149-152`) | CONFIRMED |
| attributes | 40 registrations, 32 `setSyncable(true)`, and `attack_damage` default 2 / min 0 / max 2048 and **not** syncable (`world/entity/ai/attributes/Attributes.java:14`) | CONFIRMED |
| loot context param sets | 26 sets, and `ADVANCEMENT_LOCATION` requires THIS_ENTITY, ORIGIN, TOOL, BLOCK_STATE and nothing optional (`world/level/storage/loot/parameters/LootContextParamSets.java:116-118`) | CONFIRMED |
| enchantment hooks | `EnchantmentHelper.canStoreEnchantments` called from `AnvilMenu` and nothing else (corpus grep for the qualified call) | CONFIRMED |

The *blurbs* on those pages are hand-written into `gen_reference.py` and are
**not** covered by this check. One is a count worth a look in session N:
loot-context-params says "Twelve of these twenty-six sets never roll a
`LootTable` at all".

### The pages, corrected

Twenty agents, one per page: the introduction, `lectures.md`, the five atlas
pages and the thirteen Reference pages that are not pure `gen_reference.py`
views. Fixed in place this session:

- **`introduction.md`** — "the two shared foundations are left off [the
  figure]" (the figure draws both boxes and three of their arrows; what is left
  off is their *other* edges); "each cut by a definition rather than a
  reordering" (`lectures.md` says the second is cut *by order*); "the atlas is
  four figures ... and the table it was drawn from" (four *views* over four
  pages, seven figures, six tables); "a page that fails any of the three"
  (there are four gates now); "the only thing allowed to change" a chunk
  (the client changes its copy freely — it is the only copy allowed to
  *decide*); "the first page of the book, Anatomy" (the first *lecture*);
  and the skip list, which called `stats`, `blaze3d/audio` and `util/filefix`
  "packages nobody will recognise" — only `gizmos` and `references` are.
- **`lectures.md`** — the six fixes listed above, plus: *authority* is linked
  back by three later parts, not four (the page says three thirty lines
  later); Part VIII is "a trunk and four branches" over **five** lectures;
  Part XI assumes **two** Part X pages (`the-client-loop` and
  `the-client-level`), not "only that page"; Part XII also assumes the
  data-driven type pattern; "*EMPTY* to *FULL* in twelve steps" (twelve
  statuses, eleven steps); the client-loop row's "the only page that says when
  a frame happens" (Part I's anatomy says it too).
- **`maps/packages.md`** — `net/minecraft/data` "writes the vanilla data pack
  rather than anything that runs in a game": the dedicated server ships all
  163 classes and both `Blocks` and `MinecraftServer` read `data/worldgen`
  constants at run time — `what-this-book-skips.md` says so in bold, so two
  pages of the book disagreed. Also the quarter/third slide against the page's
  own 29.5%; `world/level/biome` is `levelgen`'s sibling, not part of it;
  `net/minecraft/commands` is more than Brigadier's argument types;
  `realmsclient` restored to the below-3% list. `server/level` "the smallest
  package with the largest classes" was replaced with a rate — **the session's
  own first replacement was wrong too** (it is fourth by lines per class, not
  first), which is the re-derive rule catching the session rather than an agent.
- **`maps/fanin.md`** and **`maps/README.md`** — the fan-in chart counts
  *net.minecraft* and *com.mojang* imports only; unrestricted, the nullability
  annotation (1,668) and `List` (1,455) outrank its number one, so the page's
  hook rested on a filter it did not mention. Stated on the page, in the figure
  caption and in the tool's docstring. The counting-rules table also now says
  that a class is a `.java` file including the 542 `package-info.java` markers,
  and states the new descendant rule.
- **`maps/hierarchy.md`** and **`entity-anatomy.md`** — `Entity` 193 to **191**,
  `Screen` 157 to **158**, `AbstractContainerEventHandler` 158 to **159**,
  `Packet` "227 direct implementers" to **236 descendants from 227**, after the
  resolver fix. Everything else the prose quotes survived re-derivation:
  `FeatureElement` 386/7, `ItemLike` 366, `LivingEntity` 124, `Mob` 114,
  `PathfinderMob` 108, `BaseEntityBlock` 64, `AbstractContainerScreen` 27,
  `RealmsScreen` 23, `Projectile` 26, `VehicleEntity` 15, `Goal` 200/99, and
  the thirteen terminal direct subclasses of `Entity`.
- **`maps/biggest.md`** — three attributions: `DensityFunctions` is the node
  types, not the vanilla noise graph (that is `NoiseRouterData` and the JSON);
  `Hud` is the in-world overlay inside the wider `Gui`; the two packet
  switchboards do not handle the packets their phases share, which are one
  class up in the two common listener impls.
- **`reference/README.md`** — the shelf figure said the eight views are
  "rewritten on every deploy" and nothing ran `gen_reference.py` on a deploy;
  it does now, which makes the label true. Also: the rule is pass 3's, not
  `plan.md`'s; twenty rows classify twenty pages, not twenty-one; the packets
  row's parts were out of numeric order; *every* `EnchantmentHelper` entry
  point is every **public** one; and the lanes and class-index rows oversold
  those pages the same way the pages did.
- ~~**`reference/block-update-flags.md`** and **`blocks-and-states.md`** — the
  flag word is `Level.setBlock`'s **third** argument; the four-argument
  overload takes an update limit after it. Bit 16 has two readers, not one
  (`Level.setBlock` and `BlockInput.place`); bit 32 is masked out of the word
  as it propagates (`& -34` to the neighbours at `Level.java:249`, `& -33` into
  the recursive write at `Block.java:245`), which is the interesting thing
  about it; and on the client bit 2's "broadcast" is
  `LevelExtractor.blockChanged`, a re-mesh
  (`ClientLevel.java:832`).~~ Every clause CONFIRMED by session E **except the
  bit-16 count, which is three**: `WorldGenRegion.setBlock:337` reads it too,
  to suppress the post-processing mark. `block-update-flags.md` corrected.
- **`reference/threads.md`** — `ClientPacketListener.handleCustomPayload` was
  listed among the handlers that never leave the Netty thread. It is the
  *payload* dispatcher (`ClientPacketListener.java:2296`), and its caller runs
  `PacketUtils.ensureRunningOnSameThread`
  (`ClientCommonPacketListenerImpl.java:165`) before delegating at `:172`, so
  it is on the Render thread. Seven handlers, not eight — **`plan.md`'s session
  I line still says eight**.
- **`reference/naming-drift.md`** — three rows whose "old" name is still live
  in 26.2: *doLimitedCrafting* (a `ClientboundLoginPacket` component and a
  `LocalPlayer` field), *Recipe.getIngredients* (off the interface, still on
  `ShapedRecipe`), and *isCritArrow*, which was never a `Player` method and is
  live on `AbstractArrow`.
- **`reference/math-and-primitives.md`** — `AABB` has **six** public final
  doubles, not eight; `Vec2` as a look direction is (xRot, yRot), and only the
  *Rotation* NBT tag stores it the other way (`Entity.java:2207` against
  `:2779`); `Mth.nextGaussian` does not exist (it is
  `RandomSource.nextGaussian`, and `verify_names.py` passed it because the
  token appears inside `Mth.java`); `Rotations` has one user.
- **`reference/density-function-nodes.md`** — "the answers are computed at
  construction and propagated upward" is true only of the arithmetic family,
  which stores them as record components; every other node recomputes on each
  call, by delegation or by walking its list again.
- **`reference/glossary.md`** and **`creating-a-world.md`** — *world gen
  settings* is written to *data/minecraft/world_gen_settings.dat* (namespaced,
  as `level-data-and-rules.md` already had it), and the same path was wrong
  twice on `creating-a-world.md`, once inside a diagram. *Permission set* (the
  client carries a level-based set too), *unattended command* (a clean one is
  sent with no prompt) and *window* (six window callbacks; the input ones are
  registered elsewhere) each contradicted their own owner page.

### Open — what session A did not reach

The reports are not committed, so what is still open is written out here. All
of it is *verified finding, unactioned*, not *unchecked*.

- **`reference/math-and-primitives.md`** — the figure's thesis at L14 ("every
  conversion is a named static method on the type you are converting *to*") is
  broken by six of its seventeen edges; `breadthFirstTraversal` allocates and
  is not an iterator (L60-61); the occlusion shape is not in the `Cache`, which
  is skipped for dynamic-shape blocks (L133-137); `MinecartCollisionContext` is
  an `EntityCollisionContext` from `CollisionContext.of` (L142-143); Xoroshiro
  does not share `BitRandomSource` and not every implementation is in
  `levelgen` (L149-152); "the other seven" (L112). Plus eight MISLEADINGs, the
  sharpest being that four of the seven built-in noise settings opt into the
  legacy random source, so "the default for world generation" (L162) is not.
- **`reference/hud-elements.md`**, **`reference/level-data-and-rules.md`**,
  **`reference/non-living-damage.md`**, **`reference/submit-phases.md`** — each
  checked row by row with findings outstanding. `non-living-damage` needs a
  `hurtClient` column (seven of the twenty-one override it, two returning an
  unconditional `true`), and `Entity.hurtOrSimulate` is the dispatcher most
  callers actually invoke; four of the twenty-one also return false from
  `Entity.isAttackable`, which makes their `hurtServer` unreachable from melee.
  `submit-phases` is complete as a list — fifteen phases, thirteen renderers,
  both re-derived and confirmed — and is missing `SubmitNodeStorage`, the two
  marker interfaces, `PhaseSubmitGrouper` and
  `RenderType.canConsolidateConsecutiveGeometry`, without which "order bucket"
  and "may be reordered" are unexplained.
- **`reference/glossary.md`** — four WRONGs fixed; about a dozen MISLEADINGs
  open, each named with its owner page in the report and worth settling when
  that part's session runs: *world clock*, *integrated server*, *objective*,
  *authority*, *connection*, *selector head*, *blending data*, *heightmap*,
  *activity*, *ticket*, *world gen settings*, *environment attribute*.
- **`reference/class-index.md`** — the index is blind to diagrams: **135
  class/page pairs and 112 distinct classes** are named only inside a mermaid
  block, 26 of them with no row at all, and 51 are `participant X as ClassName`
  declarations. The page now says so; teaching the generator to read mermaid
  blocks would add at least 51 cells and 6 rows, and is **pass-5 work**.
- **`verify_names.py` has a hole**: its token pattern excludes `(`, so the 19
  backticks of the form *Class.method(Arg)* in the corpus are neither verified
  nor indexed. Session O.
- **The lane key** — 45 of its 340 rows are claimed by no page, and three
  (`PTT`, `TCTD`, `TDec` before this session) appear nowhere but `lanes.md`,
  against session E's ruling that the key is pruned to lanes in use. `PTT` is
  the documented nested-class exception in `TEMPLATE.md`, and its pilot page is
  now a flowchart with no lanes. Logged in `pass5.md`.

### For other parts' sessions

- **Part IX** — `plan.md`'s session I line says "the eight handlers that never
  hop"; it is seven (above).
- **Part VI** — `authority.md:27` says `Player` overrides "three of the four"
  predicates; it overrides four
  (`Player.java:1254,1259,1268,1273`), and the glossary's "four predicates"
  framing needs settling with `authority.md:26,34`.
- **Part XII** — `blending.md:121` says the measurement is taken from "the
  neighbour's" blocks; `BlendingData` measures the chunk that owns it.
- **Part XIII** — `lectures.md:513` and `commands/README.md:83` both say
  "sixty-two of the sixty-seven suggestion providers ask the server". **Neither
  number could be reproduced** under five populations tried
  (`SuggestionProviders` registers three; `.suggests(` has 65 call sites, none
  naming `ASK_SERVER`; `ArgumentTypeInfos` has 59 registrations). Session M
  must state the population or the claim goes.
- **Part XI** — `rendering/README.md:15-19` states its size rule as "one class
  per file", but its 1,179 classes / 87,000 lines includes 133
  `package-info.java` markers, while Part XII's 423 excludes them. Two size
  claims, two rules.
- ~~**The queue tool** — a note written as a bare `` `README.md` `` routes to all
  fifteen landing pages; `pass4.md`'s Part V and Part XIII notes both landed on
  `reference/README.md`. Qualify landing-page notes as `` `blocks/README.md` ``.~~
  Both notes qualified by session C, which also found the second half of this
  bug (a struck bullet's continuation lines came back unstruck) and fixed it.


## Session P — The lecture order and the close *(2026-09-03)*

Session P wrote no part; it wrote the lecture map's dependency section and
the parts-dependency figure, four coverage pages, and one sentence or link
on each of eleven sibling pages. Everything below is new to the corpus and
has been checked once by the session and never by an adversary.

### `lectures.md` and `src/figures/parts-dependency.md` — claims about order

- ~~**Every solid arrow in the figure is a landing page's *before you start*
  entry**, and the section says so; check each of the twenty-two arrows
  against the landing page it came from, and each landing-page entry
  against a sentence in the part that uses it (the charter's addition 2).
  The two omitted foundations (Part I anatomy, Part II codecs and
  registries) are asserted to be assumed by every part.~~ CONFIRMED after
  four fixes (session A) — `check_deps.py` proves the arrows and the entries
  match each other; the entries were judged against the parts by hand.
- ~~**"No solid arrow points at an earlier part"** — true by construction of
  the figure; the claim to check is that no landing page lists a later
  part's page that the figure left out. Candidates: Part IX names *the
  client loop* (Part X) as "the deeper version" and the session drew that
  as no arrow.~~ WRONG in three places, all fixed (session A): Parts IV, VI
  and IX each listed a later part's page under *before you start* with no
  arrow. Drawing the arrow would have been wrong in all three — each was a
  hand-forward or a pointer, not a dependency — so each moved out of the
  section instead.
- ~~**The two dashed arrows**: Part III → Part IV (tickets and loading; the
  environment page), cut "by definition" — `server-level-tick.md` defines
  entity-ticking and block-ticking range before using them — and "by
  order"; Part X → Part V (prediction), cut at Part V by the two identical
  preambles. Both restate landing-page rulings by sessions D/E and F/K.~~
  The Part X → Part V arrow CONFIRMED. The Part III → Part IV arrow named
  two pages and Part III's landing page listed only one; the environment
  half is now on the landing page with the cut stated the way the lecture
  map states it (session A).
- ~~**The nine-page table**: each row's "parts whose landing pages assume it"
  was read off the landing pages by the session; re-derive the column by
  grep. In particular: *environment attributes* ← III, VI, XI (Part X's
  `what-makes-a-sound` also names it and Part X's landing page does not);
  *the connection* ← X, XIII; *chunk anatomy* ← V, VI, XII.~~ Two rows
  WRONG, both fixed (session A); the count above the table was wrong too
  (nine rows, ten pages). *The connection* ← X, XIII and *chunk anatomy* ←
  V, VI, XII CONFIRMED. The Part X parenthetical CONFIRMED and its
  conclusion with it: both Part X links are see-also pointers inside
  naming-drift asides, not dependencies.
- ~~**"Watched straight through, the sidebar order needs one departure from
  itself"** — that the environment page is the only backward dependency a
  straight viewer meets.~~ CONFIRMED (session A): it is the only *before you
  start* entry pointing at a later part that is not cut by definition or by
  a shared preamble, and it is `watch in this order` item 1 in Part IV, so
  the departure is one lecture long.
- ~~**The Part I ruling**: *what this book skips* second, game tests last
  "because nothing later depends on them" — check that no landing page
  assumes `game-tests`.~~ CONFIRMED (session A); it is `check_deps.py`'s
  check 5 and is now a deploy gate.
- ~~The intro sentence "Nothing in Reference is watched, and nothing in the
  maps is" — check no landing page lists a Reference page in *watch in this
  order* (session O's note).~~ CONFIRMED (session A); it is
  `check_deps.py`'s check 4 and is now a deploy gate.

### `rendering/block-entity-rendering.md` — new, 332 lines, comparison

Drafted by an agent from the decompile; the session re-derived the 26
registrations against 49 `BlockEntityTypes` and the 13 `ID_MAPPER.put`
calls (`grep -c`), the 0.3 fade gate (`LevelExtractor.java:274`), the
equality gate in `BlockEntityRenderDispatcher.tryExtractRenderState`, the
frozen partial tick (`DeltaTracker.getGameTimeDeltaPartialTick` returns 1.0
when frozen and not ignored; `Camera.getCameraEntityPartialTicks` passes
`true`; `GameRenderer.extract` passes `false`), and the three Christmas
implementations (`ChestRenderer` constructor, `IsXmas`, *items/chest.json*'s
*local_time*). Everything else is the agent's evidence. Paths relative to
`reference/26.2/net/minecraft/client/`.

- **The hook**: "the two are drawn at different partial ticks and only one
  of them respects the freeze" — `renderer/GameRenderer.java:407, 416`,
  `renderer/extract/LevelExtractor.java:175, 262` (one world partial tick
  for every block entity); `LevelExtractor.java:222` (per-entity
  `isEntityFrozen`); `Camera.java:138-140`; `GameRenderer.java:619`;
  `world/TickRateManager.java:72-74` (never freezes a `Player`).
  Session-confirmed the three partial-tick sources; "keeps swaying with
  your view bob" is the agent's phrasing of the consequence.
- Counts: 26 of 49 (`BlockEntityRenderers.java` static block;
  `BlockEntityTypes.java`); 24 renderer classes (`ChestRenderer` serves
  three types); the other 23 include FURNACE, HOPPER, BARREL, BEEHIVE; 26
  state classes (27 files with `package-info`); `BedRenderState` the only
  orphan (corpus grep); 13 special renderers under 13 ids; nine implement
  `NoDataSpecialModelRenderer`; eleven import `renderer/blockentity` (all
  but Trident and CopperGolemStatue); three hold a block-entity renderer
  instance (Banner, DecoratedPot, ShulkerBox); `getViewDistance` overridden
  in five files so nineteen take the default 64
  (`blockentity/BlockEntityRenderer.java:27`); `shouldRenderOffScreen`
  overridden in exactly three (`BeaconRenderer.java:128`,
  `BlockEntityWithBoundingBoxRenderer.java:172`,
  `TestInstanceRenderer.java:77`); five states carry another pipeline's
  snapshot (Spawner, Shelf, Campfire, BrushableBlock, Vault).
- Orderings and mechanism: never frustum-tested (`LevelExtractor.java:262-300`
  vs `isEntityVisible` 242-256); fade zeroed within √768 ≈ 27.7 blocks or
  for a previously empty section (`renderer/LevelRenderer.java:588-606`;
  ramp `renderer/chunk/SectionRenderDispatcher.java:253-257`); the chest
  contributes zero quads and adds itself to the section's list
  (`renderer/chunk/SectionCompiler.java:83-88, 97-98`;
  *blockstates/chest.json* → *models/block/chest.json*, particle only);
  **two model tables** (`resources/model/ModelManager.java:91, 95, 110,
  326-327`; `SectionCompiler.java:36`; `renderer/block/BlockModelResolver.java:19-22`)
  and `BlockModelResolver`'s callers are all entity renderers (ten named)
  — note `BlockEntityRendererProvider.Context` carries a
  `blockModelResolver` no block-entity renderer uses; the equality gate
  (`ClientLevel.java:199-206`; `BlockEntityRenderDispatcher.java:68`);
  `BlockEntityRenderer.shouldRender` is a centre-distance test (31-33) vs
  `EntityRenderer.java:66-70` and `Entity.java:2158-2174`; beacon
  horizontal-only (`BeaconRenderer.java:137-140`), view distance = render
  distance × 16 (132-135), `beamRadiusScale` and the scoping reset (47-51),
  `MAX_RENDER_Y = 2048` (25); distances 68 / 96 / 256 / max-of-two
  (`PistonHeadRenderer.java:93-95`, `BlockEntityWithBoundingBoxRenderer.java:176-178`,
  `TheEndGatewayRenderer.java:55-57`, `TestInstanceRenderer.java:82-84`);
  no `finalizeRenderState` counterpart (`BlockEntityRenderer.java` vs
  `EntityRenderer.java:162-172, 313`); the base state five fields
  (`state/BlockEntityRenderState.java:16-20, 27-34`);
  `MovingBlockRenderState` holds the light engine by reference
  (`PistonHeadRenderer.java:86-90`; `entity/state/FallingBlockRenderState.java`);
  `AbstractSignRenderer` calls `Font.split` in submit (53); the spawner
  overwrites the display entity's light (`TrialSpawnerRenderer.java:43-44`);
  the pose pre-translated (`LevelRenderer.java:653-659` vs 634-639); the
  held chest in `handAndScreenSubmitNodeStorage`
  (`GameRenderer.java:367-386, 619-622`); a layer has quads or a special
  renderer, never both (`item/ItemStackRenderState.java:242-253`).
- The Christmas triple: `ChestRenderer.java:46-56` and
  `BlockEntityRenderDispatcher.java:101-105` (constructor runs only on
  reload); *items/chest.json* and `renderer/item/properties/select/LocalTime.java:25`
  (`UPDATE_INTERVAL_MS`); `BuiltInBlockModels.createXmasChest`,
  `block/model/properties/conditional/IsXmas.java`,
  `ConditionalBlockModel.java:22-25`. **"Two of the three notice midnight
  almost at once. The one you are standing in front of does not"** is the
  page's most inference-shaped sentence; check it hardest.
- Editorial: the *why* column of the view-distance table (68 = "a moving
  block starts outside the block it is drawn from"; the structure block;
  the gateway) is the agent's reasoning, not a source comment.
- **Unsettled by the agent**: whether the 0.3 gate is observable at the
  default *chunk section fade-in time*; whether `EnchantTableRenderer`'s
  book and `BuiltInBlockModels.createEnchantingTable`'s `BookSpecialRenderer`
  can both draw for one object; whether a block entity added before the
  first resource reload can be permanently excluded from the global set
  (`ClientLevel.onBlockEntityAdded` with a null renderer).
- **Where the queue entry and session L were wrong**: "26 render states"
  is a file count and 25 are reachable; the territory is ~4,300 lines
  (3,353 + 973), not ~3,300; the extract/submit split is *shorter* than the
  entity side (no finalize); `renderer/special` is reached by two roads
  (item model and block state via `SpecialBlockModelWrapper` in a table
  terrain never reads), which no page said; "a stricter visibility rule
  enforced twice" conflated the section walk + fade + flat radius with the
  off-screen flag's double-draw guard.
- Siblings: `entity-rendering.md`'s *Block entities* paragraph cut to one
  sentence and a link; `block-entities.md` (Part V) and
  `models-and-atlases.md` gained a link each.

### `commands/entity-selectors.md` — new, 313 lines, pipeline with a policy figure

Drafted by an agent from the decompile; the session re-derived the seven
`setWorldLimited` callers and the twenty-one `register` calls
(`grep -c`), the box rule in `EntitySelectorParser.getSelector`, the six
heads' `selectOnlyAlive` / `includesEntities` settings, the linear player
walk in `EntitySelector.findPlayers`, and the seven reads of
`Permissions.COMMANDS_ENTITY_SELECTORS` plus the one grant. Everything else
is the agent's evidence. Paths relative to `reference/26.2/net/minecraft/`.

- **The hook**: "*@p* is not 'the nearest player in this world' … chosen
  from the list of everybody on the server" — case `'p'` sets no
  `worldLimited` (`EntitySelectorParser.java:274-279`); `findPlayers` with
  `isWorldLimited()` false walks `PlayerList.getPlayers()`
  (`EntitySelector.java:240-254`); `ORDER_NEAREST` is `distanceToSqr` with
  no dimension term (`EntitySelectorParser.java:64-68`). Session-confirmed
  the walk; the "raw x, y, z" wording is the agent's.
- Counts: twenty-one names (`EntitySelectorOptions.bootStrap` 92-615);
  seven world-limiting options (lines 117, 138, 144, 150, 156, 162, 168);
  three always-available options *tag*, *nbt*, *predicate* (393, 428, 613);
  four `SetOnceOptionState` options *limit*, *sort*, *scores*,
  *advancements* (`EntitySelectorParser.java:106-112`); thirty-two parser
  fields; thirteen `EntitySelector` fields (57-69, constructor 71); five
  classes and 1,717 lines — **excludes two `package-info.java` stubs**; the
  atlas convention would say seven files and 1,725 lines, and pass 4 should
  pick one convention for the corpus; seven reads of the permission
  (`EntityArgument.java:134`, `GameProfileArgument.java:87`,
  `MessageArgument.java:101`, `ScoreHolderArgument.java:41`,
  `EntitySelector.java:108`, `EntitySelectorParser.java:130, 143`) and the
  grant at `LevelBasedPermissionSet.java:20`; eight `EnderDragonPart`
  sub-entities (`EnderDragon.java:100-108`).
- Orderings: `finalizePredicates` adds rotation and level tests last
  (190-214, called at 525); `EntitySelector.getPredicate` appends
  feature-flag, exact box, range in that order (265-300); `Util.allOf`
  evaluates in order and short-circuits, so the range test runs after an
  *nbt* comparison; `EntitySelectorOptions.get` (628-638) refuses a
  repeated option before its handler runs (`parseOptions:379`).
- Only/never: six heads and the default throws (239-293); only *@e* and
  *@n* add `isAlive` (266, 272, applied 295); `LivingEntity.isAlive`
  (1848-1850) vs `Entity.isAlive` (2386-2388); **no index by entity type**
  (`world/level/entity/EntityLookup.java:23-37` iterates `byId.values()`
  with `EntityTypeTest.tryCast`); **players never get a box**
  (`EntitySelector.java:207-259`; `ServerLevel.getPlayers` 995-1012 is a
  linear walk); the three vanilla commands with a selector-capable argument
  and no `requires` — `MsgCommand`, `EmoteCommands`, `TeamMsgCommand` — from
  46 files under `server/commands/` naming the four argument types;
  `MessageArgument` treats refusal as formatting (139-142) and swallows only
  `ERROR_MISSING_SELECTOR_TYPE` / `ERROR_UNKNOWN_SELECTOR_TYPE` (156-163);
  `EntitySelector.usesSelector` set only by `parseSelector` (229);
  `COMPILABLE_CODEC` compiles with selectors unconditionally allowed
  (45-55); `ServerStatusPinger`'s `ResolutionContext` has no source
  (`client/multiplayer/ServerStatusPinger.java:51-53`;
  `SelectorContents.java:33-36` returns empty); all five classes in
  `server-classes.txt`; the name `EntitySelector` used twice
  (`world/entity/EntitySelector.java`).
- X-not-Y: `getResultLimit` returns the parsed limit only for arbitrary
  order (192-194), consumed at 180 and 235; the box path offers
  `EnderDragon.getSubEntities()` (`Level.java:602-635`) and the walk does
  not (`ServerLevel.java:978-989`); the two structures behind
  `LevelEntityGetterAdapter`; *dx=0* is one block wide and the cube for 8
  spans −8 to +9 (`createAabb:176-188`, `getSelector:148-156`); the delta
  branch beats *distance* (148); *distance=8..* gives no box (150);
  `MinMaxBounds.Doubles.matchesSqr` compares squares
  (`advancements/predicates/MinMaxBounds.java:231, 261`);
  `InvertableSetOptionState`'s two terminal states; `EntityArgument`
  rejects on shape at parse time with *@s* exempt (107-124);
  `EntityArgument.listSuggestions` (128-146) and
  `ClientSuggestionProvider.getSelectedEntities` (77-79); `ORDER_RANDOM` is
  `Collections.shuffle` with no `RandomSource` (73-75); `Bootstrap.bootStrap`
  fills the options once (`server/Bootstrap.java:59`); *gamemode*, *level*,
  *advancements* call `setIncludesEntities(false)` (275, 133, 585).
- **Unsettled by the agent**: whether `Collections.shuffle(List)` is
  unseeded per call (JDK source not in the tree; the page says only that no
  world seed reaches it); whether any vanilla writer puts a
  `SelectorContents` in a status description; whether option-suggestion
  order is stable (Brigadier's `Suggestions.create` sorts, so it should
  be). Two field names for one fact — `EntitySelector.usesSelector` and
  `EntitySelectorParser.usesSelectors` — are both correct and should not be
  "fixed" to match.
- **The queue entry's count was wrong**: "six classes, ~2,136 lines" is
  five classes and 1,717 lines (seven files and 1,725 with the stubs).
- Sibling: `brigadier-and-commands.md`'s selector paragraph shrank to a
  link, dropping four backticked selector strings and the "667 lines"
  aside; its claim "thirteen final fields" is the new page's.

### `worldgen/blending.md` — new, 346 lines, pattern

Drafted by an agent from the decompile; the session re-derived the 193
positions (enumerated dx, dz in −7..7 with dx²+dz² ≤ 64; `Blender.java:76-82`),
the three blendable router functions and their targets
(`NoiseRouterData.java:34-35, 120-123`), the absence of any
`setBlendingData` in the tree, the single `sideByGenerationAge` call with
*false* (`BlendingData.java:101, 108`), and the data-pack counts
(*blend_density* in all 7 noise settings; *blend_alpha* in 9 density
function files; *blend_offset* in 3). Everything else is the agent's
evidence. Paths relative to `reference/26.2/net/minecraft/`.

- **The hook**: "The three splines that shape overworld terrain are swapped
  out for a ground height the game read off the old chunk's blocks…, the
  constant ten, and zero" — `NoiseRouterData.java:34, 35, 120, 121, 123,
  324`; `Blender.java:119-121` (alpha 0 on an exact hit) and 148-150 (alpha
  → 0 as distance → 0). Session-confirmed the targets; the "hardly generated
  at all" framing is the agent's.
- Counts and constants: inner 3×3 for density (`Blender.java:59, 87-89`);
  radius seven derived from the 27-cell range (`Blender.java:56-57`;
  `core/QuartPos.java:25, 29`); 27 cells / 108 blocks and smoothstep over
  28 (132, 148-150); inverse fourth power (137); density lerp within two
  cells, alpha over three (181, 197-198); Y difference doubled (178);
  biome: twelve cells of shift noise, over 28, threshold one half
  (264-267); sixteen columns = 7 inside + 9 outside
  (`BlendingData.java:44-49`, fills 127-165); `BlendingData.Packed` codec
  validates 16 (396-401); eleven surface block types (51); fifteen blocks
  per density cell (206-208, 228-230); 25 columns in the `NoiseChunk`
  constructor (`NoiseChunk.java:123-135`; `forChunk:64`); 1,024-chunk region
  scan and cache (`world/level/chunk/storage/IOWorker.java:41, 86, 97-113`);
  *DataVersion* below 4882 or a *blending_data* compound (129-131); four Y
  levels across 256 columns (`Blender.java:287-296`); within four blocks of
  the box after shift noise ×4 (358-363); box eight wide (395-397).
- Orderings: `NoiseChunk` created at *BIOMES* and cached
  (`NoiseBasedChunkGenerator.java:92-94`; `ChunkAccess.java:438-443`; no
  `noiseChunk = null` anywhere); the flat caches filled before
  `router.mapAll` (`NoiseChunk.java:120-135` vs 141-142); identity swap
  (483); empty blender skips the swap and replaces *blend_density* with its
  child (117, 138-140, 458-459); `ChunkStatusTasks.generateFeatures` primes
  heightmaps before decorating and calls `generateBorderTicks` after
  (`ChunkStatusTasks.java:115, 120, 123`; read at `Blender.java:307`);
  `Blender.of` asks the save first (69-72).
- Only/never/not: `ChunkAccess.blendingData` is `protected final`
  (`ChunkAccess.java:74`), `isOldNoiseGeneration` returns its presence
  (388-390); a neighbour yields data only with a `BlendingData` and
  `getHighestGeneratedStatus` ≥ *BIOMES* (`BlendingData.java:100`); only
  heights are saved — density *transient* (56), `pack` (79-94), codec (395);
  a chunk measures itself once (53, 127, 166); exactly three router
  functions are blendable, all in `registerTerrainNoises` whose three
  callers are the overworld variants (`NoiseRouterData.java:100, 104, 105`);
  `postProcess` wraps every dimension's router (224-227; 253, 287, 295,
  301, 310); the water table follows the old ground
  (`preliminarySurfaceLevel` 249, 335-343; `Aquifer.java:403`);
  `generateBorderTicks` returns unless the generated chunk itself is old
  (`Blender.java:279`) — so the neighbour test at 299 reduces to "not old";
  carvers skip masked positions (`CarvingMask.java:38-40, 52-54`;
  `WorldCarver.java:98`); `Blender.empty` is an anonymous subclass (39-53);
  four `Blender.of` call sites, three eager
  (`ChunkStatusTasks.java:70, 77`; `NoiseBasedChunkGenerator.java:237, 274`);
  the biome answer is a holder or null (267); three cave biomes in
  `BelowZeroRetrogen` (44; resolver 104-116); *Blending: Old* on the debug
  screen (`client/gui/components/debug/DebugEntryChunkGeneration.java:65-66`).
- Deliberately softened: seven "sits inside" the radius-eight window
  (`ChunkPyramid.java:19`; `WorldGenRegion.java:126-133`) — eight would fit
  too, so no claim that seven is maximal.
- **Unsettled by the agent**: how a chunk first acquires *blending_data*
  (three fixers under `util/datafix/fixes/`, out of scope by rule 3; one
  strips the key outside the overworld, so blending is in practice
  overworld-only — a fact the page does *not* state; pass 4 rules whether it
  is sayable); three declared-but-unused constants in `Blender` and a
  cluster in `BlendingData`; the cost of the region scan (asserted as what
  the code does, not measured).
- **Where the queue entry and the brief were wrong**: `ProtoChunk.setBlendingData`
  does not exist; `ChunkSerializer` is `SerializableChunkData`; there are
  five consumers, not three; `generateBorderTicks` fires on the *old* chunk,
  not the new one. 858 lines confirmed (439 + 419).
- Siblings: `terrain.md`'s boundary question now points here (and lost the
  phrase "from four years ago"); `density-functions.md` gained two links;
  `biomes.md` one sentence; `chunk-generation-pipeline.md` and
  `chunk-anatomy.md` one link each; `what-this-book-skips.md` dropped the
  three now-written systems from *Named for a later pass to place*.

### `worldgen/creating-a-world.md` — new, 300 lines, pipeline with a comparison

Drafted by an agent from the decompile; the session re-derived the parked
main thread (`CreateWorldScreen.openCreateWorldScreen` →
`Minecraft.managedBlock`), the live layer list behind *Cancel*
(`PresetEditor.EDITORS` passes `FlatLevelSource.settings()`;
`CreateFlatWorldScreen`'s Cancel calls only `onClose` and `updateLayers`)
and `WorldGenSettings extends SavedData` with its own `SavedDataType`.
Everything else below is the agent's evidence, unchecked by the session.
Paths relative to `reference/26.2/net/minecraft/`.

- **The hook**: "Before the screen can draw a single widget the game has
  already run a complete server-side data-pack load … with the client's
  main thread parked on `BlockableEventLoop.managedBlock`" —
  `client/gui/screens/worldselection/CreateWorldScreen.java:150-168`.
- "`WorldLoader.load` … calls it **after** the worldgen registries and the
  `Registries.LEVEL_STEM` registry are loaded and **before**
  `ReloadableServerResources.loadResources` runs" — `server/WorldLoader.java:38-48`.
- "The registry set that recipes, loot tables and functions are then parsed
  against includes the dimension registry that callback produced" —
  `WorldLoader.java:45-47`.
- "*level.dat* is written by the client, in `Minecraft.doWorldLoad`, before
  the server thread exists — while the settings file is written by the
  server after it starts" — `client/Minecraft.java:2223-2240`;
  `server/MinecraftServer.java:355`, `646-648`.
- "`CreateWorldScreen.onCreate` bakes the dimensions to decide the
  lifecycle … but the `WorldGenSettings` it stores holds the **unbaked**
  selection" — `CreateWorldScreen.java:245-268`.
- "the `MinecraftServer` constructor … builds a fresh rule set from the
  saved-data default and then overlays the screen's values" —
  `MinecraftServer.java:367-370`.
- Counts: three experiments (`data/minecraft/datapacks/`, `FeatureFlags.java:42-45`);
  five presets in the *normal* tag, plus *debug_all_block_states* in
  *extended*; seven world presets as JSON (`WorldPresets.java:39-45`);
  `PresetEditor.EDITORS` two entries; nine flat presets as JSON and ten keys
  (`FlatLevelGeneratorPresets.java:27-36`, `run()` 79-88; `TEST_WORLD` has
  no reader); `RegistryDataLoader.DIMENSION_REGISTRIES` one entry
  (`resources/RegistryDataLoader.java:85`); `WorldOptions` four fields;
  nineteen classes, nine screens, in `worldselection`; six footer buttons on
  `SelectWorldScreen` (79-106; the debug re-create button is in the header);
  `WorldOpenFlows.openWorld` a chain of eight (`WorldOpenFlows.java:248, 257,
  295, 409, 444, 463, 487, 508`); seven listeners in `CreateWorldScreen`;
  `WorldGenSettings` fifty-one lines.
- **"The *Cancel* button on the layer editor does not undo a layer
  deletion"** — `CreateFlatWorldScreen.java:100-103, 177-187`;
  `FlatLevelSource.java:60-62`. Session-confirmed. The agent's further
  inference, *not* on the page: the mutated settings object is the one held
  by the `WORLD_PRESET` registry's `LevelStem`. Pass 4 should say whether
  the next reload rebuilds it.
- "`WorldCreationUiState.setWorldType` … replaces **all** the dimensions";
  "the overworld only. Nothing in the create screen can edit the nether or
  the end" — `PresetEditor.flatWorldConfigurator` / `fixedBiomeConfigurator`
  both call `WorldDimensions.replaceOverworldGenerator`.
- "shows `ConfirmExperimentalFeaturesScreen` only when the requested flags
  are experimental **and** the caller was the data-pack screen" —
  `CreateWorldScreen.java:362, 380, 384-397`.
- "`WorldOptions.parseSeed` … otherwise returns the Java string hash" and
  "an empty box is re-rolling a new random world every time you touch it" —
  `WorldOptions.java:71-88`; `CreateWorldScreen.java:747-749`.
- **"`WorldDimensions.checkStability` only asks whether each of the three
  built-in keys carries the vanilla dimension type and biome source; every
  shipped preset passes"** — `WorldDimensions.java:120-190`. An inference
  from what the method does *not* check (`isStableOverworld` examines noise
  parameters only for `MultiNoiseBiomeSource`); re-derive adversarially.
- "*generator-settings* JSON, parsed … **only when the preset is**
  `WorldPresets.FLAT`" — `server/dedicated/DedicatedServerProperties.java:310-322`;
  "*server.properties* has no rules" — no game-rule read there.
- "Nothing in the family edits an existing world's `WorldGenSettings` in
  place" — `EditWorldScreen.java:44-52`; `WorldSelectionList.java:692-728`.
- "`WorldOpenFlows.recreateWorldData` reads the old world with a
  deliberately **empty** `LevelStem` registry" — `WorldOpenFlows.java:168-170`.
- "an NBT parse that deliberately skips the *Data/Player* and
  *Data/WorldGenSettings* subtrees" — `world/level/storage/LevelStorageSource.java:418-420`.
- "the water in *Water World* arrives as a feature, not as terrain" —
  `FlatLevelGeneratorSettings.java:165-173`; preset at
  `FlatLevelGeneratorPresets.java:82`.
- "the only thing that ever selects it is `CreateWorldScreen.testWorld`" —
  grep of `FLAT_ALL_DIMENSIONS`; `client/gui/screens/TitleScreen.java:183-188`.
- "`WorldGenSettings.CODEC` encodes … to JSON using the old registries as
  context, and re-parses that JSON against the new ones" —
  `CreateWorldScreen.java:411-425`.
- `getDifficulty` hard in hardcore; `isAllowCommands` true in debug, false
  in hardcore; `isBonusChest` false in both — `WorldCreationUiState.java`.
- The *mcworld-* temp directory copied in or deleted —
  `CreateWorldScreen.java:74, 342-355, 464-499, 508-560`.
- **Unsettled by the agent**: whether enabling an experiment makes any
  registry lifecycle non-stable (so whether the create-time warning ever
  fires for an experiment alone); whether the registry-held flat settings
  mutation survives the next reload; the exact save at which
  *data/world_gen_settings.dat* first hits disk (the page says "the first
  save"). `LevelStorageSource.writeWorldGenSettings` and `writeGameRules`
  exist with no callers under `net/` and are not on the page.

### Sibling sentences the session wrote (one line each, all new claims)

- `rendering/entity-rendering.md` — *Block entities* paragraph replaced by
  one sentence: "a different visibility policy, a different partial tick
  and an empty block model".
- `blocks/block-entities.md` — "why a chest's block model is empty".
- `rendering/models-and-atlases.md` — "where those thirteen get their
  geometry".
- `commands/brigadier-and-commands.md` — the selector paragraph now says
  "thirteen final fields" and "resolved against a `CommandSourceStack` much
  later".
- `worldgen/terrain.md` — the boundary answer now calls `BelowZeroRetrogen`
  "the world-deepening path that rides the same hooks".
- `worldgen/biomes.md` — "The two wrappers in the second arrow only do
  anything beside chunks an older version generated".
- ~~`server/starting-a-server.md` — "where the stem was built, by a screen
  or by *server.properties*".~~ CONFIRMED (session C):
  `Main.createNewWorldData` takes the `DedicatedServerSettings` and is the
  no-world-data branch of `WorldLoader.load` (`server/Main.java:194, 243`).
- `reference/level-data-and-rules.md` — "creating a world is who writes
  it".
- `introduction.md` — the lane gate added to *Verified means tested*; the
  dependency-figure caption ("each cut by a definition rather than a
  reordering").
- The glossary gained fifteen entries (five per Part XII page, three each
  for the other two, one shared): *experiment*, *flat level generator
  preset*, *world gen settings*, *world preset*, *world stem*, *compiled
  query*, *selector head*, *world-limited*, *built-in block model*,
  *globally-rendered block entity*, *special model renderer*, *blending
  data*, *blend alpha*, *border tick*, *old chunk*. Each is one sentence
  written from the agent's report; check each against its owner page.

## Session O — Reference *(2026-09-03)*

**Pages rewritten or reshaped.** `reference/README.md` (new, a landing
page), `reference/level-data-and-rules.md` (reshaped around its table),
`reference/math-and-primitives.md` (figure added, surprises list dissolved
to prose), `reference/threads.md` (a new section), `reference/glossary.md`
(eleven entries added, one reordered), `reference/naming-drift.md`
(headings only), `reference/block-update-flags.md` (new, extracted from
`blocks/blocks-and-states.md`, which now links to it).

**Claims introduced, check first.**

- `threads.md`, *The eight client handlers that never hop*: "In
  `ClientPacketListener` 115 handlers do that and eight do not" — counted by
  splitting the class at every `public void handle…(` and testing each body
  for `ensureRunningOnSameThread`; re-derive, and check the common
  listener's thirteen handlers are correctly excluded (`handlePing` hops;
  `the-connection` used to say the ping reply ran on Netty and was corrected
  to *the pong bookkeeping*). Every row's "what it does" is one method body
  read once; `handleLowDiskSpaceWarning` → `Minecraft.sendLowDiskSpaceWarning`
  → `Minecraft.execute` is the row that makes a claim about a second class.
- `math-and-primitives.md`, the coordinate-spaces figure: every edge is a
  named method and every shift count is a claim — `ChunkPos.containing`
  shift 4, `QuartPos.fromBlock` shift 2, `ChunkPos.getRegionX` shift 5 (the
  old page said "32 chunks" and never "shift 5"), `SectionPos.of` from a
  `ChunkPos` plus a section y, and the three packings' bit widths (26/12/26,
  22/20/22, 32/32) copied from the page's own *Three long keys* section.
  Also the new intro sentences: "each a power of two apart from its
  neighbour" and "every conversion is a named static method on the type you
  are converting *to*" — a generalisation the old page did not make; check
  it against every edge in the figure.
- `level-data-and-rules.md`: no new facts, but eleven surprises were
  merged into the sections; the drafting agent's report listed every
  rewording. Two to read closely: "That forwarding is how game time comes
  to be shared by every level" (a causal sentence built from two old ones),
  and "So every level reports the same spawn, and it is not the one
  *level.dat* holds" (the old text said "not the stored one").
- `reference/README.md`, the table's last column: which parts' landing
  pages link each reference page, read off the landing pages today (grep
  `reference/` in `src/systems/*/README.md`); a landing-page edit in a
  later session silently dates it. And "two of these pages (submit phases,
  density-function nodes) are nothing but declaration order".
- `glossary.md`, the eleven new entries — *authority*, *batch*, *event
  loop*, *frame*, *noise cell*, *permission atom*, *permission set*,
  *quart*, *staging buffer*, *submit node*, *unattended command* — each
  written from one sentence of its owner page; the confident ones are
  "an operator's level-based set grants exactly one [atom]", "No packet
  carries one in either direction", "the client parses twice more", and
  "`Minecraft` and `MinecraftServer` are both one" (event loop).
- ~~`block-update-flags.md`: the table moved verbatim; the new opening
  sentence claims `fluids` and `pistons-and-block-events` "mean the same
  bits" when they pass a flag word.~~ CONFIRMED for the Part V half by session
  E: 324, 82, 67, 18 and 276 all decompose exactly as the table names them.

**Standing item added.** The five hand-kept catalogues
(`non-living-damage`, `hud-elements`, `submit-phases`,
`density-function-nodes`, `block-update-flags`) are name-verified from this
session on but have had one reader each; re-sweep every row against the
decompile, hardest on the two that are declaration orders. Strike the
"glossary if generated" clause above — it is hand-kept.

**Diagrams redrawn.** One added (`math-and-primitives`, the coordinate
graph — seventeen edges, each a conversion claim); one added
(`reference/README.md`, the shelf — asserts which tool writes which page).

- **2026-09-03, session L — Part XI Rendering.** Twelve pages: eight
  rewritten (`the-frame`, `the-window`, `blaze3d`, `models-and-atlases`,
  `entity-rendering`, `lightmap-fog-and-sky`, `particles`, and
  `level-rendering` in the act of splitting), two produced by that split
  (`visibility-and-the-frame-graph`, `section-meshing`), one written from
  nothing (`post-processing`), plus a landing page, a new Reference page
  (`submit-phases`), a generated figure and Part XI's section of
  `lectures.md`. `level-rendering.md` is gone and its URL redirects to the
  visibility half.

  **Two errors were found by redrawing, and both are already fixed in the
  pages — check the fixes, not the old claims.**

  1. **`the-window` said three of the six operating-system callbacks reach
     the game through `WindowEventHandler`. Only two do.** `Window`
     registers six GLFW callbacks; `onFramebufferResize` calls
     `WindowEventHandler.framebufferSizeChanged` and `onEnter` calls
     `WindowEventHandler.cursorEntered`, while `onMove`, `onResize` and
     `onIconify` write a field and stop. The interface's third method,
     `WindowEventHandler.resizeGui`, is never called by `Window` at all —
     its callers are `Minecraft` and `Options`. `framebufferSizeChanged` is
     also raised directly by `Window.updateFullscreenIfChanged` and
     `Window.changeFullscreenVideoMode`, so it is not only a callback path.
     The old claim was an inference from three method names lining up with
     three callbacks; verify the new one against `Window`'s registrations
     and its `eventHandler` call sites.
  2. **`level-rendering` conflated two different triggers.** It said
     `LevelExtractor.applyFrustum` re-runs when "the occlusion graph
     invalidates on a camera move quantised to eight blocks, on a
     field-of-view change and on the smart-cull toggle". Those three are the
     triggers for `SectionOcclusionGraph.invalidateIfNeeded`, which schedules
     the **full walk**. The **frustum step** has its own gate:
     `SectionOcclusionGraph.consumeFrustumUpdate` — set by a completed full
     walk and by a partial walk that added a section inside the offset
     frustum — **or** the camera's pitch or yaw crossing a two-degree step.
     `visibility-and-the-frame-graph` now states both clocks separately;
     check both. Corrected in the same paragraph: the old page presented
     "three sections" and "sixty blocks" as two independent numbers, and they
     are one — `MINIMUM_ADVANCED_CULLING_SECTION_DISTANCE` is
     `MINIMUM_ADVANCED_CULLING_DISTANCE` converted to section coordinates.

  **The split.** `level-rendering` became `visibility-and-the-frame-graph`
  and `section-meshing`. Nothing was cut, but the material was divided, and
  pass 4 should read the two together once against the old page, which is in
  git history at commit `03712d1`. The seam: visibility owns `LevelRenderer`,
  `SectionOcclusionGraph`, `Octree`/`VisGraph`/`VisibilitySet`, `Frustum`,
  `LevelExtractor.applyFrustum`, `FrameGraphBuilder` and the pass list,
  `LevelRenderer.prepareChunkRenders` and `ChunkSectionsToRender`, the
  translucency budget and `CardinalLighting`; meshing owns the dirty API,
  `SectionUpdateTracker`, `RotatingSectionStorage`, `RenderRegionCache`,
  `SectionRenderDispatcher`, `SectionCompiler`, `BlockModelLighter`,
  `ChunkSectionLayer`, the `UberGpuBuffer` arenas, the upload callback and
  the fade-in. Two facts are deliberately stated on both pages, once each,
  and must not have drifted: *only visible sections are re-meshed*, and
  *terrain is drawn before the sections queued this frame are compiled*.

  **Claims introduced, by page.** These are what the rewrites added that the
  old pages did not contain. Each was checked against the decompile before
  the session accepted it, which is exactly the level of checking pass 2
  proved insufficient.

  - `the-window`: the candidate loop ends in `MessageBox.error` and the game
    never starts; `RenderSystem.initRenderer` happens *inside* the loop on
    the success path, not after it; `GpuBackend.handleWindowCreationErrors`
    is handed a captured GLFW error and throws `BackendCreationException`;
    the two-of-six callback pairing above; `ClientShutdownWatchdog` is
    started from the window-close callback. Flagged as unverified by the
    drafter: where `Window.getRefreshRate`'s number originates.
  - `the-frame`: the blit is described as going *to the acquired surface
    texture*, where the old page said only "from the main render target".
  - `blaze3d`: two numbers were **corrected**, not introduced. The old page
    compared the backends at "7,461 lines against 5,623"; measured today the
    two trees are **7,477 and 5,627** (40 classes and 28), and 7,477 is also
    what `what-this-book-skips` already claimed for the Vulkan tree, so the
    two pages disagreed. The page now states both counts and the class
    counts. Also corrected: the old page's "Outside `com/mojang/blaze3d/opengl`
    — fourteen files in all" reads as if that package holds fourteen files.
    It holds twenty-eight; *fourteen* is the number of files anywhere in the
    game that import LWJGL's OpenGL bindings, thirteen of them in that
    package plus the native-library bootstrap. Introduced: that changing the
    Graphics API setting needs a restart (`Options.preferredGraphicsBackend`
    adds `Options.TOOLTIP_NEEDS_RESTART` when it differs from the value at
    startup).
  - `visibility-and-the-frame-graph`: the walk may step into a neighbour only
    if the two faces can see each other through that section's geometry
    (`SectionOcclusionGraph.runUpdates`); `FrameGraphBuilder.execute` culls
    before it orders; the *clear* pass wipes colour and depth on the main
    target; the depth copy inside the main pass goes to the translucent,
    item-entity and particle targets; `LevelRenderer.viewArea` is what a
    by-position lookup goes through; and **the entity-outline chain is added
    only when the prepared frame reports an outline** — `LevelRenderer`
    around line 199, `featureFrame.hasAnyOutline()` and a non-null chain. By
    the same evidence the drafter reports that the sky pass and the *always
    on top* pass are conditional too, which the old page's flat "in
    declaration order" list obscured. **Check the conditionality of all four
    passes.**
  - `section-meshing`:
    `SectionUpdateTracker.SectionDirtyState.isDirtyFromPlayer` is what
    *prioritise chunk updates* keys off, travelling through
    `SectionUpdateRenderState` to `LevelRenderer`'s synchronous-rebuild
    decision — and there are two settings, `PrioritizeChunkUpdates.NEARBY`
    (which also takes anything within a near radius) and `.PLAYER_AFFECTED`;
    the rationale given for `SectionUpdateTracker.hasAllNeighbors`, that a
    mesher decides a face by reading the block on the other side of it; and
    "a newly homed slot starts dirty". The drafter also found three things it
    kept *out* of the page, each a possible old-page error worth checking:
    that `LevelExtractor.blockChanged` is itself the halo path while the
    public `LevelExtractor.setBlockDirty` is the `ModelManager.requiresRender`-gated
    entry; that `LevelExtractor.setBlocksDirty` expands its box by one block
    on each side; and that `LevelExtractor.allChanged` also clears tint
    caches and rebuilds `SectionUpdateTracker` at the current render
    distance.
  - `models-and-atlases`: the whole *How an item picks its model* section is
    new — `ItemModelResolver` reading `DataComponents.ITEM_MODEL`, both
    lookups falling back rather than failing, `ClientItem.Properties`
    carrying the hand-swap animation and the GUI-overflow flag, and
    **`ItemModels` registering eight kinds of unbaked item model of which
    only one draws anything itself**. That count and that characterisation
    are the two hardest claims on the page. Also new: the fan-out is
    described as **sixteen** parallel pieces of work — thirteen stitches plus
    three listings — where the old page said thirteen stitches "plus" the
    listings without counting them together.
  - `entity-rendering` and `reference/submit-phases.md`: the Reference page
    is almost entirely new fact and is the largest single body of unchecked
    claims this session produced — the declaration order of the fifteen
    phases, which three are a `TranslucentFeatureRenderPhase` (and that
    `SubmitNodeCollection.translucentCustomGeometry` is *not*, despite the
    name), what files into each phase and on what condition, that a
    see-through name tag emits two nodes, that a quad-particle group lands in
    `SubmitNodeCollection.solid` and `SubmitNodeCollection.afterTerrain` at
    once, the registration order of the thirteen feature renderers, the three
    sweeps `FeatureRenderDispatcher.PreparedFrame.executeTranslucent` makes
    and which phases each drains, and one line per renderer on what it
    writes. **Check this page row by row.** The drafter also contradicts two
    old-page claims that are still standing in the lecture prose: that
    "batching is by feature type, then by `RenderType`" (only batchable
    submit types have a batch key at all — everything else merges by
    adjacency), and that "translucency opts out of reordering rather than of
    merging" (the translucent phase does reorder, by depth-sorting; what it
    opts out of is the *grouper's* reordering).
  - `particles`: the destroy event is raised on the server side too, so the
    trace gains a server-side arrow — `Block.playerWillDestroy` is called
    from both `MultiPlayerGameMode` and `ServerPlayerGameMode`; the broadcast
    is 64 blocks, same dimension, excluding the source when it is a `Player`
    (`ServerLevel.levelEvent`); a level event carries no particle type, which
    is why the override flag cannot apply to it; and
    `ParticleEngine.clearParticles` is the named reload callback. Two
    interpretive glosses with no new mechanism: that the two independent
    32-block checks can disagree because the camera moves while the packet is
    in flight, and that the reservoir's squared probability makes a particle
    storm degrade gradually rather than hit a wall. Carried over verbatim and
    **not** re-verified: "eight call sites in all" bypass
    `ClientLevel.addParticle`.
  - `lightmap-fog-and-sky`: dissolving the attribute enumeration meant
    pinning each constant to the thing that reads it, and those *mappings*
    are new even though the constants are not — which fog environment reads
    which of the eight fog attributes (`AtmosphericFogEnvironment` and
    `WaterFogEnvironment`), which of the lightmap's four colours comes from
    which attribute (`LightmapRenderStateExtractor`),
    `EnvironmentAttributes.STAR_ANGLE` as one of the sky's three angles, and
    `ClientLevel.animateTick` scattering
    `EnvironmentAttributes.AMBIENT_PARTICLES`. Also: the raw-clock claim in
    the hook is asserted of exactly two renderers, `CloudRenderer` (drift
    from game time) and `WeatherEffectRenderer` (the column seed) — check
    that no third renderer reads the clock. And a counting nuance: the old
    page said the sky can be skipped "five different ways" and then added the
    boss-bar suppression "on top of that"; the new page keeps five for
    `LevelRenderer.addSkyPass`'s own conditions and makes the boss bar a
    separate sixth. Confirm which reading is right.

  - **`post-processing` is entirely new and nothing has ever checked it.**
    It is the one page in the corpus written from the decompile with no
    pass-2 history behind it, so pass 4 should treat it as a pass-2 subject
    rather than a pass-3 one: falsify every sentence, not just the ones
    listed here. Five of its load-bearing claims were verified by the session
    itself before it shipped, and those five are the *least* likely to be
    wrong: the six chain ids are the only ones ever requested
    (`GameRenderer.BLUR_POST_CHAIN_ID`, `LevelRenderer.ENTITY_OUTLINE_POST_CHAIN_ID`,
    `LevelRenderer.TRANSPARENCY_POST_CHAIN_ID`, plus three built from the
    camera entity's class in `GameRenderer.checkEntityPostEffect` — those are
    all five `ShaderManager.getPostChain` call sites); every post-processing
    draw is **three vertices** (`PostPass`, one `RenderPass.draw` of three);
    the six chains declare **twenty-six passes** between them (blur 6, spider
    10, entity_outline 4, creeper 2, invert 2, transparency 2 — counted from
    the JSON in `reference/26.2/assets/minecraft/post_effect/`, which also
    confirms spider's four internal targets and blur's one);
    `PostChain.process` carries `@Deprecated`, builds its own
    `FrameGraphBuilder` and imports one target named *main*, and its only two
    callers are in `GameRenderer`; and a pass's custom uniforms are packed
    with `Std140Builder` and uploaded in `PostPass`'s **constructor**, so
    they are written once at load and never again.

    Everything else on the page is unchecked, and these are the claims most
    worth attacking because the page's argument rests on them: that a
    JSON-declared uniform's per-entry *name* is read by no codec and members
    match the GLSL positionally; that *blur.json* declares a radius of zero
    and *box_blur* falls back to a member of the *Globals* block that
    `GlobalSettingsUniform.update` rewrites each frame from
    `OptionsRenderState.menuBackgroundBlurriness`; that an input's sampler
    name gets *Sampler* appended when the `BindGroupLayout` is built; that
    two inputs on one pass sharing a sampler name is rejected at load; that
    the internal/external target distinction is enforced by subtracting the
    chain's own targets from `PostChainConfig.Pass.referencedTargets` and
    requiring the remainder to be a subset of the caller's allowed set; that
    none of the six shipped chains asks for a persistent target; that a
    compilation failure is cached as a permanent absence and reported to
    `Minecraft.triggerResourcePackRecovery`; that the cache key is the chain
    id alone and not the id plus the allowed target set; that the outline
    chain's first pass detects edges in **alpha**; that
    `LevelRenderer.doEntityOutline` composites outside the graph after
    `GameRenderer.renderLevel` returns; that the blur runs inside
    `GuiRenderer.draw` with the depth buffer cleared between the two halves
    of the GUI, bounded by `Screen.extractBlurredBackground` calling
    `GuiGraphicsExtractor.blurBeforeThisStratum` only when
    `Options.getMenuBackgroundBlurriness` is at least one; that neither
    deprecated-door caller passes an inspector, so the blur and the spectator
    shaders appear in no F3 profiler slice; and that `Minecraft.setCameraEntity`
    is what clears the effect when you leave first person. The per-chain
    table's *what a player sees* column is interpretation of GLSL the book
    does not quote, and should be read as such.

    One consequence for other pages: `post-processing` states that the
    transparency chain is gated on `OptionsRenderState.improvedTransparency`
    and not on any graphics preset, and that there is no *Fabulous* setting
    any more. If that is right, check whether `options` in Part X says
    otherwise. And one thing to re-check on the next version bump
    rather than now: `ShaderManager.CompilationCache` keys a loaded chain by
    its id alone and not by the allowed target set it was validated against,
    so two callers wanting one chain under different permissions would share
    whichever object was built first. No two callers do today.
  **What `lightmap-fog-and-sky` gave back to Part IV.** The page's opening
  hundred lines re-taught `EnvironmentAttribute`, its flags and builder, a
  twenty-four-item enumeration of `EnvironmentAttributes` constants,
  `EnvironmentAttributeSystem`'s layer stack, `Timeline`, `Timelines` and
  `ClockTimeMarkers`. All of it is **deleted, not moved**: Part IV's
  `environment-attributes-and-timelines` already owned every one of those
  subjects, and the session confirmed each name is still present there before
  deleting — `AttributeTypes`, `ColorModifier`, `Timeline.Builder`,
  `ClockTimeMarkers`, `EnvironmentAttribute.isSpatiallyInterpolated` and
  `Timelines.EARLY_GAME` all checked. **Pass 4 should confirm nothing was
  lost across that seam** and should read the two pages together. Kept on the
  Part XI side because they are its own: `ClientLevel`'s two extra attribute
  layers are the lightning flash, `DimensionType.skybox` and its three
  values, and `BiomeSpecialEffects` hollowed out to water, grass and foliage.

  **The diagrams.** Every figure in the part is new or redrawn, and each one
  asserts an ordering. New flowcharts: the substrate-under-pipeline figure on
  the landing page, whose arrow labels are hand-off claims; the backend retry
  loop and the six-callback figure in `the-window`; the façade-over-backend
  figure in `blaze3d`; the five-stage pipeline and the pass-order figure in
  `visibility-and-the-frame-graph`, the second of which is a declaration-order
  claim *and* a conditionality claim; the sixteen-fan barrier figure in
  `models-and-atlases`; the four-stage figure in `entity-rendering`; the
  admission flowchart in `particles`; and in `post-processing`, the
  parse-compile-declare-draw figure. Redrawn with corrected lanes, and in one case with its `rect` blocks
  removed: one frame in `the-frame`, one draw in `blaze3d`, a block placed in
  `section-meshing`, a zombie in `entity-rendering`, the sun going down in
  `lightmap-fog-and-sky`, the break puff in `particles`. One generated
  figure, `tree-EntityRenderState.svg`, whose counts — 98 render states, 70
  of them living — come from `map_source.py` and want re-deriving like the
  atlas's other numbers.

  **The landing page and `lectures.md`** claim that Part XI is a substrate
  under a pipeline; that `the-frame` is watchable before the substrate it
  stands on; that the only hard prerequisite is Part X's `the-client-loop`,
  with `resource-system` (Part II) and `environment-attributes-and-timelines`
  (Part IV) as per-lecture ones; and that lectures four and five are one
  journey seen from two ends. The landing page also states the renderer's
  size as 1,179 classes and 87,000 lines against `net/minecraft/server`'s 420
  and 53,000 — **re-derive both**. Session I's inventory reported 1,187 and
  97,864 for "the rendering tree" without saying which packages it counted,
  this session could not reproduce it, and the page now states its own
  package set and counting rule rather than inheriting the number.

- ~~**2026-09-02, session F — Part V Blocks.** Seven pages: four rewritten
  (`blocks-and-states`, `block-interaction`, `block-breaking`,
  `block-entities`) and three produced by the notebook's confirmed three-way
  split of `redstone` (`signal-and-dust`, `pistons-and-block-events`,
  `diodes-and-observers`), plus a landing page and Part V's section of
  `lectures.md`. `redstone.md` is gone and its URL redirects to
  `signal-and-dust`.

  ~~**Read the provenance note before trusting anything below.** The session
  was interrupted after four pages had been drafted: two of the four agent
  reports arrived, two did not, and the three redstone pages were then
  written by the session itself directly from the decompile. The pages divide
  into four classes of evidence and pass 4 should weight them differently.~~

  1. ~~**`block-interaction`** — agent-drafted, report received, and every
     correction in it **re-derived by the session** against the source.~~
  2. ~~**`block-breaking`** — agent-drafted, report received, corrections
     **not** independently re-derived (the interrupt landed first). Treat its
     twelve claimed corrections as unverified leads, not as findings.~~
  3. ~~**`blocks-and-states`** and **`block-entities`** — agent-drafted, **no
     report survived**, so nothing is recorded about what they changed
     relative to the old page beyond the session's own read of the finished
     text. These two need the full protocol, starting with a diff against
     their pass-2 versions in git.~~
  4. ~~**The three redstone pages** — session-written, every claim derived from
     the decompile in this session, and every diagram read separately from
     its prose.~~

  - ~~**Corrections the session derived itself, method by method.**~~
    - ~~**Block events are not "a tick late".** The old `redstone` diagram
      carried a *next tick* bar over `ServerLevel.runBlockEvents`, and that is
      wrong for the common cases. `MinecraftServer.processPacketsAndTick`
      drains queued packets and *then* calls `MinecraftServer.tickServer` in
      the same lap, and the *blockEvents* section of `ServerLevel.tick` sits
      after *tickPending* and *chunkSource* and before *entities* — so an
      event queued by a packet handler or by a scheduled tick drains in the
      **same** tick, and `ServerLevel.runBlockEvents` loops until its set is
      empty, so an event queued during the drain does too. Only the entity and
      block-entity phases, and a chunk that is not block-ticking, push one to
      the next tick. `reference/glossary.md` already said "usually within the
      same tick", so the corpus contradicted itself.
      `pistons-and-block-events` now states all five cases.
      **Re-derive the phase order and each case.**~~
    - ~~**`RepeaterBlock.LOCKED` does not survive on the client, and the old
      page's reason for saying so was wrong.** It claimed locking "is a shape
      update, which is why it survives on a client that never runs neighbour
      updates". `RepeaterBlock.updateShape` recomputes the lock only when the
      level is not client-side, and `ObserverBlock.startSignal` returns
      immediately on a `ClientLevel` — both shape hooks opt out of the client
      explicitly, and a client keeps no appointment book to fire into anyway.
      `diodes-and-observers` gives the real reason the shape channel is the
      right one: it carries a neighbour's state change even when the neighbour
      issued no neighbour update.~~
    - ~~**`blocks-and-states`' opening overclaimed and was narrowed.** Its own
      closing question is right and its hook was not: `Block.getId` and
      `Block.stateById` are tolerant, but
      `ClientboundBlockUpdatePacket.STREAM_CODEC` reads the same table through
      `ByteBufCodecs.idMapper`, which is `IdMap.byIdOrThrow`. Check the
      narrowed sentence, and check the Q&A's account of which paths use which
      lookup.~~
    - ~~**Dust powers the block below it and never the one above.**
      `RedStoneWireBlock.getSignal` answers zero for `Direction.DOWN` and
      answers full power for `Direction.UP` with no connection test. This is
      nowhere in the pass-2 corpus.~~
    - ~~**`LeverBlock.pull` is handed a null player**, so — unlike the door —
      nobody is excluded from the sound and the clicker hears the server's
      copy. And `LeverBlock.useWithoutItem` writes no state at all on a
      `ClientLevel`, so a lever is not predicted.~~
    - ~~**`PistonBaseBlock.checkIfExtend` runs a dry-run
      `PistonStructureResolver.resolve` before queueing** an extend event, so
      a piston with an immovable wall in front of it queues nothing at all.~~
    - ~~**A diode's `HorizontalDirectionalBlock.FACING` points at its input**,
      and `DiodeBlock.updateNeighborsInFront` acts on the opposite side. Any
      sentence in the corpus saying a diode "faces its output" is wrong.~~
    - ~~**`ComparatorBlock.checkTickOnNeighbor` books on a second condition**
      the repeater has no analogue of: whenever the computed output differs
      from the int held in the `ComparatorBlockEntity`, not only when the
      powered flag disagrees with the input.~~
    - ~~**`SignalGetter.getSignal` is a maximum, not a choice.** For a redstone
      conductor it takes the larger of the block's own weak signal and
      `SignalGetter.getDirectSignalTo`. Three Part V pages used to phrase this
      as one *or* the other.~~

  - ~~**Claims the rewrite introduced, per page.** Check these first and
    hardest.~~
    - ~~**`signal-and-dust`** (session-written): *the number* — **forty-two**
      neighbour updates per changed wire, derived as seven
      `Level.updateNeighborsAt` calls (the position plus its six neighbours,
      collected in a hash set in
      `DefaultRedstoneWireEvaluator.updatePowerStrength`) times six directions
      per `CollectingNeighborUpdater.MultiNeighborUpdate` — **re-derive both
      factors**. Also: the framing that the staircase of intermediate values
      follows from the recursion terminating on *value* rather than on
      distance; the three-direction-order table; the claim that
      `RedStoneWireBlock.getConnectionState`'s completion pass, not
      `RedStoneWireBlock.shouldConnectTo`, is what points dust into a piston;
      `RedstoneTorchBlock.isToggledTooFrequently` burning out on the eighth
      surviving entry using a literal rather than
      `RedstoneTorchBlock.MAX_RECENT_TOGGLES`. The flowchart asserts an
      ordering from arrival to fan-out.~~
    - ~~**`pistons-and-block-events`** (session-written): the five-case tick
      analysis above; the census of block-event users — four blocks
      (`PistonBaseBlock`, `NoteBlock`, `PotentSulfurBlock`,
      `ComparatorBlock`) plus seven block entities through
      `BaseEntityBlock.triggerEvent` — **counted by grep and worth
      re-counting**; the flag table (324 for the placeholders and the arm, 82
      for vacated positions, 67 for the base, 18 for a destroyed block) and
      the claim that only the first of those omits `Block.UPDATE_CLIENTS`;
      that the crushed-block particle event in `PistonBaseBlock.moveBlocks` is
      raised on the **client** side only; that the middle
      `SignalGetter.hasSignal` in `PistonBaseBlock.getNeighborSignal` is dead
      code because `Blocks.pistonProperties` declares a piston never a
      redstone conductor; that `PistonMovingBlockEntity.finalTick` writes
      flags 3 and writes **air** for the source piston, against
      `PistonMovingBlockEntity.tick`'s 67; that
      `PistonMovingBlockEntity.TICKS_TO_EXTEND` is declared and never read.
      The sequence diagram asserts four tick boundaries.~~
    - ~~**`diodes-and-observers`** (session-written): the whole comparison
      table, which is a claim about *three* differences and no others; "a
      diode never writes into its target"; that the signal leaves through
      `DiodeBlock.onPlace` rather than through `Level.setBlock`'s fan-out,
      because `DiodeBlock.tick` writes with flag 2 alone; the priority account
      (`TickPriority.EXTREMELY_HIGH` / `VERY_HIGH` / `HIGH` for the repeater,
      only `HIGH` / `NORMAL` for the comparator, and `NORMAL` only from
      `DiodeBlock.setPlacedBy`); the item-frame rule (exactly one, facing the
      comparator's way, else neither reading is taken); container fullness as
      each stack's count over **that stack's own** maximum; the claim that an
      observer sees a door opened by hand. The flowchart asserts which channel
      each of the three listens on.~~
    - ~~**`block-interaction`** (agent, session-verified): bit 8 read as
      *player-caused* by `LevelExtractor.blockChanged`; the copper door as
      proof the path never reads `BlockTags.WOODEN_DOORS`; `InteractWithDoor`
      reading `BlockTags.MOB_INTERACTABLE_DOORS` while the older goals read
      `DoorBlock.isWoodenDoor`; that opening a door makes navigating mobs
      repath through `ServerLevel.sendBlockUpdated`; that a disabled item
      aborts the whole hand loop; the eight-row gate table's *what the client
      gets* column, including "nothing, not even the receipt" for
      `ServerGamePacketListenerImpl.hasClientLoaded`; the chain-limit count
      resetting in a `finally`. The agent also flagged a **duplicated swing
      branch** in `ServerGamePacketListenerImpl.handleUseItemOn` — the
      server-swing test appears twice in structurally identical arms — which
      reads like a decompiler artefact. The page describes the behaviour
      rather than the shape. Settle it.~~
    - ~~**`block-breaking`** (agent, **not** session-verified): the plus-one
      identity, i.e. that `ServerPlayerGameMode.incrementDestroyProgress`'s
      *(elapsed + 1)* is exactly the client's first `Minecraft.continueAttack`
      in the same client tick as `Minecraft.startAttack`; "about two ticks of
      slack" at the 0.7 bar for stone; that the delayed path calls
      `ServerPlayerGameMode.destroyBlock` rather than
      `ServerPlayerGameMode.destroyAndAck`, so a failure there sends no
      correction; that the first crack stage broadcast is 1 rather than 0;
      that `LevelExtractor` picks the deepest crack within 32 blocks **of the
      camera**. Plus its twelve claimed corrections — among them that reach
      and the height check sit outside the action switch and so gate ABORT and
      STOP too, that `MobEffectUtil.getDigSpeedAmplification` returns the
      maximum of haste and conduit power rather than stacking them, that
      `Block.popResource` jitters on all three axes, that the durability cost
      is skipped because hardness is zero rather than because
      `Tool.damagePerBlock` is zero, and that three blocks override
      `BlockBehaviour.attack` rather than one. **None of these were
      re-derived.**~~
    - ~~**`blocks-and-states`** and **`block-entities`** (agent, **no report**):
      unknown. Diff both against their pass-2 versions in git before checking.
      Claims the session noticed while reading and did not verify: that
      exactly two blocks override
      `BlockBehaviour.BlockStateBase.shouldChangedStateKeepBlockEntity`
      (`CopperChestBlock` and `CopperGolemStatueBlock`); that
      `CopperGolemStatueBlockEntity` overrides the update *packet* but not the
      *tag*; that eight classes override
      `BlockEntity.preRemoveSideEffects`; the nineteen-classes / twenty-types
      sync count; `Level.setBlock`'s four false-returning cases; and that
      `LevelExtractor.setBlockDirty` re-meshes only when
      `ModelManager.requiresRender` says the two states look different. The
      session did verify one of `block-entities`' orderings: the client's
      block-entity pass runs after its entity pass and before
      `ClientLevel.tick`, in `Minecraft.tick`.~~

  - ~~**The landing page and the lecture order.** Part V's `blocks/README.md` claims
    the part is a hub and six spokes, that `blocks-and-states` is what the
    other six reach into, and that the interaction/breaking pair is one
    lecture in two halves. It also makes a **dependency ruling pass 4 should
    test**: Part V is watched *before* Part X's `prediction-and-acks`, on the
    grounds that the two click pages' shared preamble is all either lecture
    needs. Check that the preamble is sufficient and that it contradicts
    nothing in `prediction-and-acks`.~~


- ~~**2026-09-02, session E — Part IV The world.** Ten pages: five rewritten
  (`chunk-anatomy`, `chunk-generation-pipeline`, `lighting`, `chunk-storage`,
  `environment-attributes-and-timelines`), four produced by the two confirmed
  splits (`scheduled-ticks` + `fluids` from `block-ticks-and-fluids`,
  `game-events-and-vibrations` + `points-of-interest` from
  `game-events-and-poi`), and `level-data-and-rules` reframed as Reference —
  plus a landing page and Part IV's section of `lectures.md`.
  `tickets-and-loading` was session A's pilot and was not rewritten.
  **Check the four split pages hardest**: a split re-attributes every fact,
  and a fact that changes owner is a fact that moved without a diff. Every
  draft was diffed against its old page from the agent's report before
  acceptance; the corrections marked *(session-verified)* were re-derived
  from the decompile by the session itself, method by method.~~

  - ~~**Twelve pass-2 errors found.** Re-check each *fix*, not only the old
    claim.~~
    - ~~`lighting` had the light broadcast **backwards**. It said the packet
      goes to the watching players "with border players included";
      `ChunkHolder.broadcastChanges` passes *borderOnly* **true** for the
      light packet and false for block changes, and
      `ChunkMap.isChunkOnTrackedBorder` keeps only players for whom some
      neighbour of the chunk is untracked. Light updates reach the edge of a
      player's tracking view **only**. The old page's "up to nine packets
      for one torch" went with it. *(session-verified)*~~
    - ~~`game-events-and-poi` said POI updates are "deferred through the
      server's task queue, **even from the server thread**", so "a record
      appears a task later than its block and any read in between sees the
      old answer". False for the ordinary case:
      `MinecraftServer.scheduleExecutables` is *running a task or not on this
      thread, and not stopped*, so on the Server thread outside a queued task
      `BlockableEventLoop.execute` runs the body **inline** and the record
      appears synchronously. Deferral is the worldgen-worker case and the
      nested-task case. *(session-verified)*~~
    - ~~`scheduled-ticks` (from `block-ticks-and-fluids`): the tick drain was
      said to be skipped "whenever `TickRateManager.runsNormally` is false,
      which covers stepping and sprinting as well as a plain freeze".
      `TickRateManager.tick` sets its flag to *not frozen, or frozen with
      ticks left to run*, so `/tick step` **runs** the drain, and the sprint
      path never touches the flag. *(session-verified)*~~
    - ~~`chunk-anatomy`'s palette tier table put biomes' one-, two- and
      three-bit linear rungs on the same *1–4 bits* row as block states.
      `Strategy.createForBiomes` has linear rungs at 1, 2 and 3 only and is
      `Configuration.Global` from 4 bits up — no four-bit linear rung for
      biomes and no hashmap tier at all. *(session-verified)*~~
    - ~~`chunk-anatomy` said of `LevelChunk.setBlockState` that "neighbour
      *updates* are not here — they are `Level.setBlock`'s job". Partly
      false: `BlockBehaviour.BlockStateBase.affectNeighborsAfterRemoval` runs
      inside `LevelChunk.setBlockState`, on a `ServerLevel`, when the block
      changed or the new block is a `BaseRailBlock`, and the flags carry
      `Block.UPDATE_NEIGHBORS` or a piston move. *(session-verified)*~~
    - ~~`chunk-anatomy` also conflated the two halves of the block-entity
      removal gate — `BlockEntity.preRemoveSideEffects` is what the client
      and `Block.UPDATE_SKIP_BLOCK_ENTITY_SIDEEFFECTS` skip, not the removal
      — and "a client section's `LevelChunkSection.isRandomlyTicking` is
      false forever" is over-strong, because a client-side write does move
      `LevelChunkSection.tickingBlockCount`. *(agent, re-read by the session)*~~
    - ~~`environment-attributes-and-timelines` said "the night curve can dim a
      nether-red fog and a taiga-blue fog by the same factor". **The nether
      has no day timeline**: its dimension type's *timelines* is
      *#minecraft:in_nether*, which resolves through *#minecraft:universal*
      to `Timelines.VILLAGER_SCHEDULE` alone. Only the overworld tag adds
      day, moon and early game. *(session-verified)*~~
    - ~~`environment-attributes-and-timelines` said a positional read
      "recomputes the whole layer stack on **every call**, every time". The
      sampler's positional flag is computed from whether any *layer* is an
      `EnvironmentAttributeLayer.Positional`, **not** from the attribute's
      own flag, so a nominally positional attribute that no biome mentions
      is memoised for the tick like any other. *(session-verified)*~~
    - ~~`environment-attributes-and-timelines`, four more: "`TimeCommand` is
      the only class outside `world/clock` that touches `ServerClockManager`
      directly" — false; "the two positionless readers" — there are three
      `EnvironmentAttributeSystem.getDimensionValue` call sites; "all of it
      scoped to a clock through `/time of`" — the same subtree is registered
      directly on `/time` against `DimensionType.defaultClock`; and
      "`ServerLevel.tick`'s very first statement". *(agent)*~~
    - ~~`chunk-generation-pipeline` was self-inconsistent about the noise fork:
      one section said "biomes and noise fork to the pool" flatly while its
      step 8 said only `NoiseBasedChunkGenerator` does. Only the latter is
      true, and the old page's stated *reason* for the biome fork ("it is on
      the base `ChunkGenerator.createBiomes`, so every generator forks") is
      wrong, because `NoiseBasedChunkGenerator` overrides it. *(agent)*~~
    - ~~`chunk-generation-pipeline` singled out "*SURFACE*'s distance-0
      requirement on *NOISE*" as "the one that matters most". That is the
      automatic parent requirement every step carries and distinguishes
      nothing; the radius-1 rows are what stack into the 11. *(agent)*~~
    - ~~`fluids` (from `block-ticks-and-fluids`): "seven blocks out
      `FlowingFluid.getNewLiquid` reaches zero, nothing is rescheduled"
      conflates two stopping mechanisms — the front stops because
      `FlowingFluid.spreadToSides`' gate computes zero at amount 1, while
      `getNewLiquid` returning empty is what happens when the *supply* is
      cut. And `LavaFluid.spreadTo` turns the target to stone only when that
      block is a `LiquidBlock`. *(agent)*~~
    - ~~`game-events-and-poi`: arrival is **⌊distance⌋ − 1** ticks after
      selection, not ⌊distance⌋ — `VibrationSystem.Ticker.tick` decrements
      the travel time inside the same call that selected the candidate, so
      anything under two blocks arrives on the selecting tick.
      `VibrationSystem.User.requiresAdjacentChunksToBeTicking` is true for
      the shrieker as well as the sensor, and its test also requires each of
      the nine columns to come back non-null from
      `ServerChunkCache.getChunkNow`. *(session-verified for the decrement)*~~
    - ~~`game-events-and-poi` gave `ValidateNearbyPoi` for *HOME* as running
      "each tick within 16 blocks". It is in the **rest** package at
      priority 3, so it only runs while `Activity.REST` is active — which
      means the stale-`GlobalPos` answer needs *and it is night* too.
      *(agent)*~~

  - ~~**The claims each rewrite introduced**, per page. None was fact-checked
    in pass 2.~~
    - ~~**`chunk-anatomy`** — the hook (a two-state section costs what a
      sixteen-state one costs, and the seventeenth re-encodes 4,096 entries)
      rests on three legs: `Strategy.createForBlockStates`' always-four-bits
      rung, `PalettedContainer.pack` taking its width off the same ladder,
      and `LinearPalette.idFor` → `PalettedContainer.onResize` →
      `PalettedContainer.Data.copyFrom`. Then: `SerializableChunkData.read`
      on the server thread while only `SerializableChunkData.parse` is on the
      pool; `read` returning a `ProtoChunk` in every case; `ImposterProtoChunk`
      and `EmptyLevelChunk` being subclasses of the two lines rather than
      four peers; `EmptyLevelChunk.getFullStatus` flat `FullChunkStatus.FULL`;
      `LevelChunk.getBlockState` answering air from
      `LevelChunkSection.hasOnlyAir` without a palette; `BulkSectionAccess`
      as the second `LevelChunkSection.acquire` holder; `SectionCopy` storing
      null for an air-only section; `SingleValuePalette.idFor` jumping 0 → 4
      bits in one step; `LevelChunkSection.recalcBlockCounts` reachable only
      from the two-container constructor, whose only caller is
      `SerializableChunkData`; `LevelChunkSection.isRandomlyTicking` having
      exactly one reader outside its class;
      `LevelChunk.EntityCreationType.QUEUED` having **no caller anywhere**;
      `LevelChunk.getBlockEntity` promoting pending NBT on any creation type;
      `ChunkStatus.FINAL_HEIGHTMAPS`; and the twelve ordered steps of the
      write path as a table — check that table row by row.~~
    - ~~**`chunk-generation-pipeline`** — the hook (529 holders claimed before
      a step runs) and: `ChunkGenerationTask.create` taking the generation
      pyramid's radius **unconditionally**, before any disk read; the
      per-layer sweep radii 11, 11, 3, 3, 2, 2, 2, 1, 1, 0, 0, 0 (derived by
      replaying `ChunkStep.Builder` — re-derive these); the loading pyramid's
      accumulated FULL requirement being *SPAWN* at 0 and *INITIALIZE_LIGHT*
      at 1; `ChunkStatusTasks.full` unwrapping an existing
      `ImposterProtoChunk` and replacing nothing in that case;
      `GenerationChunkHolder.replaceProtoChunk` throwing on a changed slot;
      the dispatcher's four-priority bookkeeping queue;
      `ChunkTaskPriorityQueue.PRIORITY_LEVEL_COUNT` being derived from
      `ChunkLevel.MAX_LEVEL` rather than the literal 46;
      `ChunkPyramid.SAFETY_MARGIN_CHUNKS` computing to **90** chunks;
      *STRUCTURE_STARTS* needing *EMPTY* at 0 (the old table said "—"); the
      second *EMPTY* sweep reading only chunks the first missed because
      `GenerationChunkHolder.acquireStatusBump` fails for holders already
      there; and **five** steps leaving the worldgen executor, six inline,
      plus *EMPTY* — the figure asserts all of it, so check it node by node.
      *(The session verified `ChunkGenerationTask.getRadiusForLayer` picks
      the pyramid from the task's needs-generation flag, so the figure's
      radii are the generation-pyramid ones and `EMPTY`'s first sweep is the
      loading pyramid's 1; the caption now says so.)*~~
    - ~~**`lighting`** — the hook (no light thread, no light phase; the kick is
      the idle poll) and: the border-only broadcast above; the queued light
      task's runnable running on the light executor, not the server thread;
      `LevelLightEngine.runLightUpdates` running the block engine to
      completion then the sky engine, so the four stages happen **twice** per
      batch; `ThreadedLevelLightEngine.runUpdate` taking a window of
      min(size, 1000) and the POST pass removing that same window;
      `ChunkMap.scheduleUnload` as the second caller of
      `ThreadedLevelLightEngine.tryScheduleUpdate`;
      `ChunkHolder.sectionLightChanged` returning false with no bit set when
      there is no ticking chunk, *after* marking unsaved;
      `ClientPacketListener.applyLightData` ending in
      `LevelLightEngine.setLightEnabled`; enabling being inside
      `LightEngine.propagateLightSources` rather than
      `ThreadedLevelLightEngine.lightChunk`; the 27-section figure deriving
      from a flood reaching **thirteen** blocks plus the one-block halo; and
      `SectionUpdateTracker.hasAllNeighbors` checking the eight surrounding
      columns.~~
    - ~~**`chunk-storage`** — the hook (the eager sweep and the wall-clock
      autosave) and: `ChunkMap.setChunkUnsaved` being installed only at the
      moment a chunk becomes full, so the eager set never holds a generating
      chunk; `/save-all` forcing a write on a no-save world while an autosave
      does not; `ImposterProtoChunk` never being written;
      `ChunkMap.saveChunkIfNeeded` accepting only `LevelChunk` and
      `ImposterProtoChunk`, so a `ProtoChunk` is written only by the unload
      path; the in-file/sidecar ordering asymmetry stated as a principle
      (**session-verified against `RegionFile.write`**: allocate, write,
      headers, `RegionFile.writeHeader`, commit, free — the sidecar's commit
      being the move); `RegionFileVersion.VERSION_GZIP` having a null option
      name so it is readable but unselectable (**session-verified**); the
      `StrictQueue.FixedPriorityQueue` ordinal scan behind `IOWorker`'s three
      lanes; the unload task **re-arming** on a new sync future rather than
      only re-checking; `EntityStorage.loadEntities` running its datafix on
      the server thread; and `ChunkMap.saveAllChunks` with flush computing
      its holder list once and looping until a pass saves none.~~
    - ~~**`scheduled-ticks`** — the hook (dedup by type and position only) and:
      the dedup slot being released in the **collect** phase, not at run;
      `LevelTicks.hasScheduledTick` and `LevelTicks.willTickThisTick`
      answering different questions, with their caller lists; two further
      comparators the old page did not name
      (`LevelTicks.CONTAINER_DRAIN_ORDER`, `LevelChunkTicks.SUB_TICK_ORDERING`);
      the gate being per **chunk**, not per position; random ticks stopping
      one ring sooner than scheduled ticks because
      `ChunkMap.forEachBlockTickingChunk` wraps
      `DistanceManager.forEachEntityTickingChunk`; the budget being per
      `LevelTicks.tick` call, so 65536 each for blocks and fluids; the
      **inference** that a block tick booking a delay-0 fluid tick is caught
      in the same level tick while the reverse waits — flagged by its own
      author as the page's one inference rather than a reading;
      `LevelTicks.clearArea` / `LevelTicks.copyAreaFrom` touching block ticks
      only, with gametest rather than structure placement as the caller;
      `SavedTick.filterTickListForChunk`; the repeater priorities
      (`TickPriority.HIGH` on, `TickPriority.VERY_HIGH` off,
      `TickPriority.EXTREMELY_HIGH` under `DiodeBlock.shouldPrioritize`,
      `TickPriority.NORMAL` only from `DiodeBlock.setPlacedBy`) —
      **session-verified**, as are the two-tick delay and the placement of
      the turn-off booking inside `DiodeBlock.tick`'s *not on* branch; and
      lava being the only randomly-ticking fluid.~~
    - ~~**`fluids`** — the hook (four independent slope searches, and a side
      that cannot be *replaced* still votes) is **session-verified against
      `FlowingFluid.getSpread`**: a strictly better score clears the
      collected winners **before** the `FluidState.canBeReplacedWith` test
      and the running minimum is updated regardless, so an unreplaceable near
      neighbour both empties the map and suppresses the rest. Then:
      thirty-seven fluid states and roughly 120 positions per side (both
      **derived arithmetic** — re-derive); `LiquidBlock.getFluidState`
      clamping the level so `FlowingFluid.getLegacyLevel` is lossy for
      falling flows; a waterlogged block reporting a **source** and therefore
      never being drained by a fluid tick; `WaterloggedTransparentBlock`
      being the only block that reports a falling source;
      `EnvironmentAttributes.WATER_EVAPORATES` read positionally while
      `EnvironmentAttributes.FAST_LAVA` is not; the nether's dimension type
      setting both; `LiquidBlock.shouldSpreadLiquid` being a no-op for water
      because its whole body sits inside a lava test;
      `LiquidBlock.updateShape` scheduling with no `shouldSpreadLiquid` gate;
      and the reach figures (water 7, lava 3, fast lava 7 — derived).~~
    - ~~**`game-events-and-vibrations`** — the hook (one tick late, six rays,
      and `SculkSensorBlock.stepOn` bypassing the cascade —
      **session-verified**: `stepOn` tests `SculkSensorBlock.canActivate` and
      not-a-warden, calls `VibrationSystem.User.canReceiveVibration`, then
      `VibrationSystem.Listener.forceScheduleVibration`, which goes straight
      to `VibrationSelector.addCandidate` past
      `VibrationSystem.User.isValidVibration` and
      `VibrationSystem.Listener.isOccluded`). Then: the arrival correction
      above; `LevelChunk.getListenerRegistry` creating a registry for any
      section merely queried; `DynamicGameEventListener.move` doing nothing
      when either chunk is not `ChunkStatus.FULL`; the allay carrying **two**
      listeners; the position source resolving between the two validity
      gates; `isOccluded` short-circuiting on the first clear ray; the
      redstone distance recomputed from block positions at arrival; the full
      step condition (`Entity.moveDist` past `Entity.nextStep`, and on ground
      *or* climbable *or* crouching-with-zero-clip *or* on rails) replacing
      the old "on the ground and not swimming"; resonance posting at the
      **neighbour's** position before tendrils-clicking; and the four tag
      contents read from the data pack.~~
    - ~~**`points-of-interest`** — the hook (claimed when a path exists, and the
      ticket and the *occupied* flag never speak) and: **two release paths
      the old page missed** —
      `SetWalkTargetFromBlockMemory` calling `Villager.releasePoi` when the
      dimension differs, when the cant-reach memory exceeds 1200 ticks, or
      after a thousand failed intermediate-position tries
      (**session-verified**), and `VillagerMakeLove` claiming a bed for a
      baby and releasing it if the birth fails; `PoiTypes.TEST_INSTANCE`
      missing from the old catalogue; zero-ticket types never being occupied
      and therefore never village centres; `PoiSection.refresh` reusing
      existing records so a repair does not reset ticket counts;
      `AcquirePoi` taking at radius 1 around the path target and
      **discarding** the take's result; `PoiManager.isVillageCenter` using
      the non-loading getter, so the village graph only sees sections already
      in memory; and the whole *who else asks* table of radii, every number
      new.~~
    - ~~**`environment-attributes-and-timelines`** — the layer-stack figure is
      new and asserts the whole order; the corrections above; plus the
      biome-layer count (eleven attributes across sixty-six biome files,
      *visual/sky_color* in fifty-six), the nine weather attributes and the
      *rain minus thunder* blend, the client flash layer's fixed lerp toward
      a named colour rather than "toward white", `Timelines.EARLY_GAME` using
      `BooleanModifier.AND`, all four vanilla timelines running on the
      overworld clock, the `/time` rate range, and the routine time broadcast
      being every **twenty** ticks with an empty clock map.~~

  - ~~**The landing page and `lectures.md` are claims about order.** Part IV's
    landing page asserts that the first five lectures are a forward-only
    chain, that `environment-attributes-and-timelines` depends on nothing
    else in the part, that Part IV needs Part III in front of it and nothing
    after it, and that render distance, simulation distance and the
    mob-spawning radius are three different radii of which only two are
    settings. Each is checkable.~~

  - **`level-data-and-rules` moved to Reference** and its body was *not*
    re-verified this session — only its header, its links and its framing
    changed. Pass 2 found eleven wrong file paths on it; re-check the paths
    and the who-owns-what table again.

  - ~~**Two claims their own authors flagged as unverified**, both worth a
    direct read: `scheduled-ticks`' delay-0 cross-queue inference, and
    `points-of-interest`' statement that a consistency repair never resets
    tickets, which was confirmed for the reuse-by-key path but not for a
    position whose *type* changed between the record and the block.~~


- ~~**2026-09-02, session D — Part III The server.** Five pages: four
  rewritten (`server-tick`, `server-level-tick`, `players-and-sessions`,
  `starting-a-server` — the old `server-lifecycle`, renamed) and one written
  from the decompile (`how-a-server-dies`), plus a landing page and Part
  III's section of `lectures.md`. **Check `how-a-server-dies` hardest:
  nothing on it was fact-checked in pass 2**, and its drafting agent's claim
  list is the only record of where each sentence came from. Every rewrite
  was diffed against its old page from the agent's report before acceptance,
  and the corrections marked *(session-verified)* below were re-derived from
  the decompile by the session itself.~~ Settled in full by pass-4 session C
  (2026-09-04).
  - ~~**Eighteen pass-2 errors found**, the largest crop since pass 2 itself,
    which says the "every page has a wrong claim" result survives one
    fact-check. Re-check each *fix*, not only the old claim.~~
    - ~~`server-tick` said `MinecraftServer.scheduleExecutables` "rejects new
      work with a *RejectedExecutionException*". It returns false, and
      `BlockableEventLoop.execute` then runs the task **inline on the
      caller's thread**; the exception belongs to the separate
      `MinecraftServer.executeIfPossible`. *(session-verified)*~~
    - ~~`server-tick` said a server "consistently 40 % late never says so".
      `MinecraftServer.nextTickTimeNanos` advances by a fixed amount every
      lap whatever the work costs, so lateness accumulates and the
      two-second threshold falls in about a hundred laps: such a server
      warns and skips repeatedly. The page's hook — log and skip are one
      condition, so a server that warned recently stays behind — is
      unaffected and stands. *(session-verified)*~~
    - ~~`server-tick`'s `BlockableEventLoop.delayCrash` framing: the crash
      slot is a **static** field shared JVM-wide, the rethrow happens only
      on a loop built with *propagatesCrashes* (true for `DedicatedServer`,
      false for `IntegratedServer`), and every server-side caller uses
      `BlockableEventLoop.relayDelayCrash`.~~
    - ~~`server-level-tick` drew and narrated `ServerLevel.runBlockEvents` as
      ungated. It is inside the freeze gate: a frozen world runs no block
      events. *(session-verified in `ServerLevel.tick`)*~~
    - ~~`server-level-tick` gated `EnderDragonFight.tick` on the empty check
      alone; it is also behind the freeze gate. *(session-verified)*~~
    - ~~`server-level-tick` mis-scoped both chunk-source gates. In
      `ServerChunkCache.tick` the purge is freeze-gated and
      `ServerChunkCache.runDistanceManagerUpdates` is not; inside
      `ServerChunkCache.tickChunks`, `Level.isDebug` wraps the **whole**
      body including `ServerChunkCache.broadcastChangedChunks`, so a debug
      world drops the block-change broadcast — which no page had said.
      *(session-verified)*~~
    - ~~`server-level-tick` said `NaturalSpawner.createState` counts mobs
      "across `DistanceManager.getNaturalSpawnChunkCount` chunks". It walks
      `ServerLevel.getAllEntities`; the chunk count is only the cap's
      divisor. *(session-verified)*~~
    - ~~`server-level-tick` had the light and block packets in the wrong
      order. `ChunkHolder.broadcastChanges` sends
      `ClientboundLightUpdatePacket` **first**, to the border players, before
      the changed-section walk begins. *(session-verified — and note that the
      drafting agent reported this correctly and then drew it wrongly in its
      own new diagram, which the session caught. Pass 4 should assume a
      redrawn figure can contradict the prose beside it, and read both.)*~~
    - ~~`players-and-sessions` said `IntegratedPlayerList` "pins the view
      distance at 10, never sets a simulation distance at all (so a LAN
      world reports 0)". `IntegratedServer.tickServer` sets both from
      `Options` every unpaused tick, floored at 2, long before anyone joins.
      The claim is cut. *(session-verified)*~~
    - ~~`players-and-sessions` said `MinecraftServer.getProfilePermissions`
      returns a `PermissionSet`; it returns a `LevelBasedPermissionSet`.~~
    - ~~`players-and-sessions` said `PlayerList.respawn` chooses
      `Entity.RemovalReason.KILLED` or `CHANGED_DIMENSION`. The reason is its
      third **parameter**, chosen by
      `ServerGamePacketListenerImpl.handleClientCommand`, in the same call
      that selects `ServerPlayer.restoreFrom`'s branch. *(session-verified)*~~
    - ~~`players-and-sessions` said a respawn "restarts the 60-tick timer".
      Death sets `ServerGamePacketListenerImpl.markClientUnloadedAfterDeath`,
      a flag the countdown never clears; the give-up-after-60-ticks rule
      belongs to the join alone.~~
    - ~~`players-and-sessions` attributed the *bypasses-player-limit* read to
      `PlayerList.canBypassPlayerLimit`, a constant false on the base class;
      only `DedicatedPlayerList` reads the op entry.~~
    - ~~`starting-a-server` said `DedicatedServer.convertOldUsers` returning
      false is the second way startup fails. It returns true if any of five
      conversions succeeded and only decides whether the name cache is
      saved; the boot-stopping gate is the separate
      `OldUsersConverter.areOldUserlistsRemoved`, over four files.
      *(session-verified)*~~
    - ~~`starting-a-server` placed the *Done* log after query, RCON, the
      watchdog, JMX and the flush save. It is logged on the line after
      `MinecraftServer.loadLevel` returns, before all of them.
      *(session-verified)*~~
    - ~~`starting-a-server` put `CrashReport.preload` "at the very top of
      `server/Main`"; version detection, the option parser, *--help* and
      *--pidFile* all precede it. And "about twenty" mutable
      `DedicatedServerProperties` fields is exactly nineteen.~~
    - ~~the old `server-lifecycle` credited
      `DedicatedServer.fillServerSystemReport` with the whole report; it
      sets two details and everything listed belongs to
      `MinecraftServer.fillSystemReport`. Its `SuppressedExceptionCollector`
      sentence named packet handlers only: chunk load and chunk save
      failures feed it too.~~
    - ~~the old `server-lifecycle` implied `level.dat` is written by the flush
      save. `MinecraftServer.saveAllChunks` calls
      `LevelStorageSource.LevelStorageAccess.saveDataTag` on **every** call,
      so an ordinary autosave rewrites it. The new durability section rests
      on this, so check it first. Also `PacketProcessor.close` drops packets
      *already queued*, not only late arrivals; and "the Server thread was
      the only non-daemon thread left" holds only after
      `Util.shutdownExecutors`, because `Util.ioPool`'s *IO-Worker* threads
      are non-daemon while `Util.nonCriticalIoPool`'s are daemons.
      *(session-verified)*~~
  - ~~**`server-tick`** — the hook (the log *is* the skip, and the missed
    ticks are never run); the warning gate read as fifteen seconds of
    *scheduled* time; the six-lane figure's ordering, and in particular that
    `ServerCommonPacketListenerImpl.resumeFlushing` itself calls
    `Connection.flushChannel` (the second write is that call, not a later
    side effect) and that `Connection.tick` flushes **after** ticking its
    listener; the flush suspension applying only to sends made on the Server
    thread; the `MinecraftServer.tickChildren` order table row by row,
    including which rows are freeze-gated; the event-loop flowchart, which
    asserts the whole `pollTask` → `shouldRun` → `haveTime` decision;
    **the "three things the budget gates" count, re-derived twice this
    session** (`ChunkMap.processUnloads`, `ChunkMap.saveChunksEagerly`,
    `SectionStorage.tick` by way of `PoiManager.tick`) with its new riders —
    the unload queue draining regardless above two thousand entries, eager
    saving capped at twenty chunks and 128 outstanding writes; the sprint
    inversion; `MinecraftServer.emptyTicks` advancing only while not
    sprinting; *pause-when-empty-seconds* being zero on the base class; the
    in-memory connection rethrow; `IntegratedServer.isTickTimeLoggingEnabled`
    being unconditionally true.~~
  - ~~**`server-level-tick`** — the hook (blocks broadcast before entities
    tick, so an entity's change lands a tick behind a command's); **the
    guard flowchart, the page's primary figure, which asserts a gate on
    every one of its twenty-odd steps — check it against `ServerLevel.tick`
    statement by statement**; the three-range opener (31 / 32, and "loaded
    means a holder exists"); the broadcast sequence diagram's order;
    `ChunkHolder.blockChanged` returning true only on the holder's first
    changed section; `GameRules.RANDOM_TICK_SPEED` at zero stopping ice and
    snow as well; `LocalMobCapCalculator.canSpawn` answering false with no
    player near; spawning chunks coming from
    `DistanceManager.getSpawnCandidateChunks` under a squared-distance test;
    `Level.tickBlockEntities` pruning removed tickers even while frozen; the
    overworld-only *gameTime* flag being the level constructor's last
    argument; commands being handled before `MinecraftServer.tickChildren`
    begins, which is what makes the hook's comparison exact.~~
  - ~~**`players-and-sessions`** — the hook (death replaces the object, a
    dimension change does not, and both keep the entity id and the same
    listener); **both join diagrams, replacing one nine-lane diagram whose
    implied concurrency was wrong** — especially the claim that the burst
    runs inside `MinecraftServer.processPacketsAndTick`, before
    `MinecraftServer.tickChildren` opens the tick's own flush bracket, which
    is why `PlayerList.placeNewPlayer` brackets itself; the four-column
    comparison table, cell by cell; `ServerLevel.waitForEntities` blocking
    the Server thread; a respawn broadcasting **no**
    `ClientboundPlayerInfoUpdatePacket` *(session-verified)*; everything
    `ServerPlayer.restoreFrom` copies unconditionally, the ender chest
    among them, which makes its survival a field assignment rather than a
    game rule; the `.dat` written before the vehicle and ender-pearl
    removal; `PlayerSpawnFinder`'s coprime-strided search;
    `PlayerDataStorage.load` reading with an unlimited accounter;
    `ServerGamePacketListenerImpl.switchToConfig`'s round trip producing a
    new entity id and a new listener; the flying kick disabled at zero
    gravity.~~
  - ~~**`starting-a-server`** — the hook (the boot step that loads the world's
    chunks loads none of them: of nine ticket types only
    `TicketType.FORCED` and `TicketType.PORTAL` carry
    `TicketType.FLAG_PERSIST`, *session-verified against all nine*); **the
    sequence diagram, the only one in the corpus with the JVM main thread as
    a lane — check which side of `MinecraftServer.spin` every step falls
    on**; `level.dat` parsed once and datafixed twice;
    `DirectoryLock.create` writing a snowman before taking the lock;
    `Util.blockUntilDone` making the main thread an executor for two stages
    of `WorldLoader.load`; the `MinecraftServer` constructor refusing a stem
    with no overworld `LevelStem`; the console thread building its
    `CommandSourceStack` off the Server thread; the icon and the first
    `ServerStatus` being built after `DedicatedServer.initServer` returns;
    `LevelLoadListener.Stage.START_SERVER` being declared and fired by
    nothing; there being no *spawnChunkRadius* game rule in 26.2
    (`GameRuleRegistryFix` removes it from saves); and the claim that the
    *menu.preparingSpawn* percentage line never runs on an ordinary world.~~
  - ~~**`how-a-server-dies`** — new, so all of it; the drafting report cites a
    file and line per claim and pass 4 should walk that list. The
    load-bearing ones: the three-column comparison table, cell by cell; the
    `/stop` sequence diagram's order, which asserts players before chunks,
    `level.dat` before the server-wide `SavedDataStorage`, and the lock
    released last; **the watchdog self-deadlock diagram**, the hook drawn —
    `System.exit` runs the hook, the hook joins the wedged thread,
    `Runtime.halt` fires ten seconds later (*session-verified*:
    `ServerWatchdog.run` loops on `MinecraftServer.isRunning`,
    `ServerWatchdog.MAX_SHUTDOWN_TIME` is ten seconds, and the timer is
    scheduled before `System.exit`); the five callers of
    `MinecraftServer.halt` and which of them pass *wait* true; the
    durability section's answer per ending, which depends on the corrected
    autosave-writes-`level.dat` fact; the claim that a server stuck in
    teardown has no watchdog left watching it, because the watchdog loops
    only while `MinecraftServer.running`; and
    `MinecraftServer.reportChunkSaveFailure` writing a
    `ReportType.CHUNK_IO_ERROR` file under *debug/*.~~
  - ~~**The landing page and `lectures.md`** assert Part III's order and its
    dependencies: that the part can be watched before Part IV because
    `server-level-tick` defines the three ranges itself, that
    `environment-attributes-and-timelines` is best watched before the level
    tick, and that Part I's *two loops* figure is the only earlier
    prerequisite. Each is a claim.~~
  - ~~**`anatomy` lost two invariants to `server-tick`** — the budget's count
    and the sprint conclusion — and now carries a one-sentence pointer;
    check that the compression lost nothing true.~~

- **2026-09-02, session C — Part I Anatomy · Part II Foundations.** Nine
  pages rewritten or written (two Part I, seven Part II), three moved to
  Reference, one landing page. Every rewrite was diffed against its old
  page from the drafting agent's report before acceptance; the claims
  below are the ones that report listed as *introduced* or *reworded*, and
  the two pass-2 errors found on the way. Check the two new pages hardest —
  nothing on them was fact-checked in pass 2.
  - ~~**Two pass-2 errors found.** `tags` said "an axe strips anything in
    `#minecraft:logs`". It does not: `AxeItem.STRIPPABLES` is a hard-coded
    `Map` of block to block and stripping never consults a tag; the page
    now opens on the parrot (`Parrot.ParrotWanderGoal` recognises leaves by
    class and logs by tag) and `PunchTreeTutorialStepInstance`. And
    `out-of-scope-tour` said `NoiseRouterData` calls `TerrainProvider` and
    `SurfaceRuleData` "every time a chunk's density functions are built".
    It does not: `NoiseRouterData.overworld` and its siblings are called
    only from `NoiseGeneratorSettings`' bootstrap methods, whose callers
    are `VanillaRegistries` (datagen) and `Commands.validate`;
    `SurfaceRuleData` is referenced by `NoiseGeneratorSettings` alone; the
    running game reads the generated JSON from the built-in pack. Verified
    by the session. The surviving runtime call is
    `NoiseRouterData.peaksAndValleys` → `TerrainProvider` on the F3 biome
    line and in `OverworldBiomeBuilder`'s parameter spans.~~
  - ~~**`anatomy`** (trace, two figures). The two-loops flowchart is the
    figure Parts III, IX and X now link to; it asserts `Minecraft.runTick`
    = advance the `DeltaTracker` → drain the `PacketProcessor` → run own
    tasks → 0 to 10 ticks → render, and `MinecraftServer.runServer` = set
    the deadline → `processPacketsAndTick` (drain, then `tickServer`) →
    `waitUntilNextTick` (run tasks, then `managedBlock`); the startup
    sequence asserts `spin` constructs the `IntegratedServer` on the
    caller's thread before starting the new one. New: "the second thread
    was created by the first, mid-frame, while the first went on drawing"
    (`Minecraft.doWorldLoad` renders inside its wait loop);
    `PriorityConsecutiveExecutor` "adds a priority to the same idea"; both
    `Main`s read *version.json* through `SharedConstants`. Reworded:
    `DataFixers.optimize` is kicked off "before the registries are built"
    (was "at the very start"). Moved, not cut: `Minecraft.isPaused`'s
    three-part condition now lives only on `the-client-loop`;
    `tickPaused`'s "or the player list is empty" and "one save on the
    transition" only on `server-tick`.~~
  - ~~**`what-this-book-skips`** (the old `out-of-scope-tour`, moved to
    Part I, the treemap included, the gaps as one table). New: the F3
    biome line runs through `NoiseRouterData.peaksAndValleys` into
    `TerrainProvider`; `NoiseRouterData` and `NoiseGeneratorSettings` are
    compiled against `TerrainProvider` and `SurfaceRuleData`; their
    bootstraps are collected by `VanillaRegistries`, run by the
    data-generator entry point and borrowed by `Commands.validate`; the
    `net/minecraft/realms` row (4 files, 203 lines: three classes and a
    *package-info*); "the table counts files, so *package-info.java*
    counts there and not in the prose" (rcon 9 files / 7 classes, stats 10
    / 9). Every size in the page's tables was checked against
    `src/generated/` and matches. The figcaption's "hatched boxes are the
    packages this page tours" is true of twelve of the fourteen: `gizmos`
    and `realms` are too small for the tool to hatch (a tool limitation,
    logged in pass3.md), and `client/multiplayer/chat/report` is depth 5.~~
  - ~~**`codecs-nbt-json`** (comparison). New: both sides wrap
    `HashOps.CRC32C_INSTANCE` in a `RegistryOps` (`ClientPacketListener`
    from the received registries, `ServerPlayer` from its own) "because a
    component value can name a registry entry" — the motive is the agent's
    reading, soften if unverifiable; `ServerPlayer`'s container
    synchroniser hashes through a 256-entry cache keyed on
    `TypedDataComponent` (verified by the session); **removals are not
    hashed** — `HashedPatchMap` is a map of added type to int plus a set of
    removed types (verified; sharpens pass 2's "one CRC32C per component");
    a wire decode failure reaches `Connection.exceptionCaught` and drops the
    connection; `ItemParser.SYNTAX_REMOVED_COMPONENT` is the command-line
    spelling of `!minecraft:foo`; the hash path runs on the Render thread
    (`AbstractContainerScreen.slotClicked` → `MultiPlayerGameMode.handleContainerInput`).
    The four short diagrams assert: the disk path never touches a
    `CompoundTag` in the block entity; the wire path is `StreamCodec` all
    the way with the `NullOps` re-encode on exactly one packet; the server
    re-hashes its own stack rather than decoding; the text path builds its
    `TagParser` for the parser's own `RegistryOps`.~~
  - ~~**`identifiers-and-registries`** (trace, both diagrams kept). The
    world-load diagram's `replaceFrom` arrow now comes from `WorldLoader`,
    not `RegistryDataLoader` (read from `WorldLoader.load`), and
    `RegistryDataLoader.load` is given lookups built by
    `TagLoader.buildUpdatedLookups` over `getAccessForLoading`, not the
    access directly. New cast claims: `RegistryDataLoader` loads JSON on the
    server and NBT from the wire on the client (`NetworkRegistryLoadTask`).
    The freeze rule is now stated in one section and justified nowhere on
    this page; `Registry.PendingTags` and `prepareTagReload` are named only
    on `tags`. Counts unchanged: 148 keys, 147 objects, five intrusive.~~
  - ~~**`resource-system`** (pipeline, `/reload` as a comparison table).
    New, all from `SimpleReloadInstance`, `Minecraft`, `LoadingOverlay`,
    `MinecraftServer.reloadResources`, `ReloadCommand`,
    `MultiPackResourceManager`, `Pack.Position`: the first listener's
    barrier is chained to the initial task; `PreparationBarrier.wait` posts
    a main-thread task that removes the listener from the preparing set and
    completes the all-preparations future when it empties; a listener that
    never reaches its barrier holds every apply; **twenty** client
    listeners; `AtlasManager` publishes one future per atlas in
    `prepareSharedState`; the overlay fades in over half a second and will
    not fade out before a full second; the recovery reload skips the fade;
    the success continuation is `finishReload` → `DownloadedPackSource.onReloadSuccess`
    → `onResourceLoadFinished`; `abortResourcePackRecovery` drops the
    overlay, disconnects and shows a toast; `triggerResourcePackRecovery`
    "takes the same road" (caveat: `clearResourcePacksOnError` crashes or
    aborts when `isAbleToClearAnyPack` is false — check the sentence);
    `ReloadReason.INITIAL`; `ReloadCommand` at `Commands.LEVEL_GAMEMASTERS`;
    on server failure the new manager is closed and the old stays; filter
    sections are pushed onto the namespace stacks; `Pack.Position.TOP`
    inserts at the back; a new `Commands` inside each
    `ReloadableServerResources`. Reworded: `Pack.Position.BOTTOM` "inserts
    at the front, past any pack already fixed there" (was "at index 0").
    The lattice figure asserts every apply waits on all preparations *and*
    the previous apply, and that the only prepare-to-prepare edge is
    `AtlasManager` → `ModelManager` through shared state.~~
  - ~~**`tags`** (trace). New: the vanilla *logs* file is three tag
    references (*logs_that_burn*, *crimson_stems*, *warped_stems*),
    *logs_that_burn* nine references including *oak_logs*, *oak_logs* four
    blocks — so *oak_logs* is a grandchild of *logs*, not a direct entry
    (the old page said otherwise); `Registry.PendingTags.lookup` answers as
    if installed; the client rebuilds its fuel table and creative search
    tree on a play-phase tags packet; `Holder.Reference.is` is a
    set-contains on the bound tag set; `FileToIdConverter.json` over the tag
    directory. The diagram's five `Note over` bars (worker pool → server
    thread → configuration → play → a server tick) are ordering claims.~~
  - ~~**`data-components`** (vocabulary). New: `DataComponentLookup` reads the
    same bound prototypes and is meaningless before the first reload (check
    that its lazy population reads `Holder.components`); "set the
    enchantments back to empty and the entry vanishes" (a worked instance of
    the sanitising rule); `ItemStack.set` is `PatchedDataComponentMap.set`;
    the cast's thread cells. The figure asserts prototype on
    `Holder.Reference` ← `DataComponentInitializers.build`, stack = shared
    prototype + `Optional` patch + `copyOnWrite`; the trace asserts click →
    `transmuteCopy` → `enchant` → `set` → `ensureMapOwnership` → the next
    `ServerPlayer.tick`'s `broadcastChanges` → `ClientboundContainerSetSlotPacket`
    → `fromPatch`.~~
  - ~~**`text-components`** (new, vocabulary; every claim is new). The hook:
    the death message is sent twice (`ClientboundPlayerCombatKillPacket` to
    the victim, system chat to everyone — verified by the session from
    `ServerPlayer.die`; a team visibility of `NEVER` broadcasts nothing,
    which the page does not say), crosses as a translation key, and is
    worded by the client's `Language` on the first frame that draws it; the
    server logs it through `Language.DEFAULT_INSTANCE` and `Language.inject`
    is called only by `LanguageManager` (verified). The rest of the page —
    the visit order, `getString` with a limit, `TranslatableContents.decompose`'s
    accepted specifiers and its cache by `Language` identity, the keybind
    resolver, the three unresolved kinds, `ObjectContents`' U+FFFC
    placeholder, the eleven `Style` fields and `applyTo`, `TextColor`,
    `shadowColor`, the eight click actions table (`UNSAFE_CODEC` read by
    nothing outside the enum; `OpenFile` built only by `Screenshot`,
    `KeyboardHandler` and `Minecraft`), the flat serialisation (never a
    *type* key on encode), the two NBT budgets and which packets use which
    stream codec, the resolution walk and its depth limit, the death-message
    key rules (`.player`, `.item`, `FALL_VARIANTS`, `INTENTIONAL_GAME_DESIGN`),
    `Entity.getDisplayName`'s shape, the `even_more_magic` fallback,
    `ClientLanguage.loadFrom`'s two-code stack — is one claim per sentence,
    each with a file in the agent's report; two the agent flagged as
    unverified: "merged in stack order" (which end of the pack stack wins
    for language files) and that the dedicated server jar bundles
    *en_us.json*.~~
  - ~~**`data-driven-types`** (new, pattern; every claim is new). The count
    — **fifty-six** registries in `BuiltInRegistries` that some codec
    dispatches on through `Registry.byNameCodec`: thirty-one bare
    `MapCodec` registries, twenty-three type-object registries, two where
    the type is the behaviour (`Feature`, `WorldCarver`) — was derived by
    grepping dispatch sites; re-derive it. The three tables' *where the
    elements live* and dispatch-key columns (*function*, *condition*,
    *processor_type*, *predicate_type*, *element_type*, *trigger*) are one
    claim per row. The trace asserts the reload half
    (`ReloadableServerResources.loadResources` → `ReloadableServerRegistries.reload`
    on the background executor; `scanDirectory` via `FileToIdConverter.registry`
    over `Registries.elementsDirPath`; a bad file logged and skipped, a
    duplicate id an error; `LootItemFunctions.compose`; `createUpdatedRegistries`
    → `replaceFrom`; validation warns and keeps the element;
    `Lifecycle.experimental`) and the run half (`RandomizableContainerBlockEntity.getItem`
    → `unpackLootTable` → `LootTable.EMPTY` for an unknown key; `fill` →
    `getRandomItems` → `shuffleAndSplitItems`; `decorate` nesting table →
    pool → entry, "a function on the table runs last"; `LootItem.createItemStack`
    → `LootItemConditionalFunction.apply` → `SetItemCountFunction.run`).
    The exceptions section: `Codec.dispatchedMap` for `GameRuleMap` and
    `DataComponentPredicate`; `ENTITY_SUB_PREDICATE_TYPE` holds a plain
    `Codec`; `RECIPE_TYPE` versus `RECIPE_SERIALIZER`; `BLOCK_TYPE` read by
    nothing but `BlockListReport`; `RegistryDataLoader` fails the whole
    load where `scanDirectory` skips one file.~~
  - ~~**`systems/foundations/README.md`** (new, landing page): the stack
    figure's ten edges are dependency claims; *before you start* names only
    `anatomy`; the seven teasers restate the seven hooks.~~
  - **`chat-and-signing`**: its `Component` section is now a one-paragraph
    pointer; the three facts it keeps (NBT on the wire, the `OPEN_FILE`
    filter, chat never resolves) are unchanged. **`reference/threads.md`**:
    one clause added — Swing's thread appears only when the dedicated
    server is started without *--nogui*. **`tools/map_source.py`**:
    `com/mojang/blaze3d/audio` added to `SKIPPED` so the treemap hatches
    what the tour tours.

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
  - ~~**`entities/entity-anatomy.md`**: "193 descendants" (was 188, from the old map that could not see nested classes); re-derive with the new tool and by hand once.~~ Settled by session F: the page says **191**, which is what the fixed `map_source.py` and a hand count both give.

- **2026-09-03, session G — Part VI Entities.** Nine pages, seven of them
  rewrites and two new, plus three Reference pages. Everything below is a
  claim pass 3 *introduced*; pass 4 checks these first and hardest.

  **Corrections this session made to pass-2 text — re-check the fix, not
  just the old claim.** Each was re-derived from the decompile by the
  session as well as by the drafting agent.
  - ~~`NaturalSpawner`: the biome **energy budget runs before the mob is constructed**, as the second conjunct of the pre-construction guard in `NaturalSpawner.spawnCategoryForPosition`, not after the `Mob.checkSpawnRules` pair as the old page (and this session's own ruling) said.~~
  - ~~`NaturalSpawner.INSCRIBED_SQUARE_SPAWN_DISTANCE_CHUNK` is `Mth.floor(8.0F / Mth.SQRT_OF_TWO)` = **5**, and its only reader is `DistanceManager.hasPlayersNearby`, as the ≤5 fast-yes arm of a `TriState` whose >8 arm is a literal. The old page said it "drives the eight-chunk square".~~
  - ~~`EntitySpawnRequest.ignoreChecks` is **never true** anywhere in 26.2; the old page said it was used to build the spawner's display mob.~~
  - ~~`EntityTypes.ITEM_FRAME`'s `EntityType.updateInterval` is `Integer.MAX_VALUE` (seven types are), so the interval branch never fires again after tick zero — which is *why* `ServerEntity.sendChanges` has an item-frame bypass. The old page said the interval "is why an item frame updates slower than a player".~~
  - ~~`ServerEntity.handleMinecartPosRot` does **not** bypass the send gate; it is called from inside it. There is exactly **one** bypass, the `ItemFrame` branch. The old page named two.~~
  - ~~`ServerLevel.tick`'s *chunkSource* phase is **after** block and fluid ticks and before block events and entities — the old page said "near its start". Session-verified from the profiler pushes.~~
  - ~~`LivingEntity.shouldTravelInFluid` reads the **cached** in-water and in-lava flags; the live `FluidState` is used only by `Entity.canStandOnFluid`. The old page said it reads the live state.~~
  - ~~`Attributes.FRICTION_MODIFIER` scales only the block-friction term; both the 0.91 and the 0.98 are scaled by `Attributes.AIR_DRAG_MODIFIER`.~~
  - ~~`Attributes.DEFAULT_ATTACK_SPEED` has **no callers**; weapons write the subtraction as a literal. The old page built a sentence on it.~~
  - ~~`Mob.getApproximateAttributeWith` is `ItemAttributeModifiers.compute`'s only caller but is itself called from six sites, armour as well as weapons.~~
  - ~~**Only `Villager` has a schedule.** `Brain.setSchedule` has two call sites, both in `Villager`; the other **nineteen** brain mobs use `Brain.setActiveActivityToFirstValid`. The old page framed that as the exception used by three mobs. Session-verified by grepping every caller.~~
  - ~~The profiler listing's nesting: *jump* and *travel* are **siblings** of *ai*, not children of it.~~
  - ~~`SummonCommand` goes through `ServerLevel.tryAddFreshEntityWithPassengers`, which refuses on a duplicate UUID anywhere in the passenger stack — a gate no page had.~~
  - ~~`entity-anatomy`'s subpackage table summed to 639 of a stated 716 (`world/entity` itself and `entity/schedule` were missing); rebuilt to twelve rows summing to 716.~~
  - ~~The non-living `Entity.hurtServer` population is **21**, not "about thirty"; 55 files declare the method and 33 of those are `LivingEntity` descendants. `Entity.hurtServer` is **abstract**.~~
  - ~~`Sheep`'s `Shearable` siblings are five, not three (`CopperGolem` and `SulfurCube` were missing).~~
  - ~~Eight direct callers of `MoveControl.setWantedPosition` bypass the pathfinder, not six — `Fox` and `Rabbit` were missing.~~
  - ~~**`ArmorStand` is a `LivingEntity`**, so the old page's roster of classes that "override `Entity.hurtServer` directly and never touch armour, i-frames or the combat tracker" led with a class on the wrong side of its own split; an armour stand does go through the reduction pipeline, and the old page's closing claim that the armour-stand damage-type tags "exist only for that code" went with it.~~
  - ~~`AbstractArrow.onHitEntity` applies `EnchantmentHelper.modifyDamage` to `AbstractArrow.baseDamage` **first** and multiplies by speed after, so Power raises the base rather than the product. The old page had the two the other way round.~~
  - ~~`CombatTracker` expiry is **not** only a background timer: `CombatTracker.recordDamage` calls `CombatTracker.recheckStatus` as its first statement, so it is also a side effect of the next hit. The old page said explicitly that it was not.~~
  - ~~The third genuinely positional damage source is `ExplodeEffect`, an **enchantment** effect, positional only when it is not attributed to its user — not "a loot-table explode effect".~~
  - ~~An ownerless `AbstractArrow` is its **own** causing entity, not a null one, which is what `ServerPlayer.hurtServer`'s unwrap re-asks about.~~

  **New pages, whose every claim is new.**
  - ~~**`authority.md`** — the whole page. Highest-risk items: that `Entity.isLocalInstanceAuthoritative` is final and unoverridden; the three-column table (a tracked mob, a player, a ridden boat, each read on both sides) — **eight rows, each a separate claim**; that both base client-authority predicates delegate to the controlling passenger, which is the vehicle model; that `ClientboundMoveVehiclePacket` is sent only on a **rejection** and that the client applies it only for a vehicle it is authoritative for, then echoes back; that `ClientPacketListener.handleEntityPositionSync` and `ClientPacketListener.handleMoveEntity` update the position codec and do **not** move a locally authoritative entity; that `SweetBerryBushBlock.entityInside` picks its movement measure off `Entity.isClientAuthoritative`; and the six-gate list at the end (each gate names a different predicate — check them one at a time).~~
  - ~~**`pathfinding.md`** — the whole page. Highest-risk: the budget is `Attributes.FOLLOW_RANGE`'s **base** value times sixteen at construction and the **modified** value (or `PathNavigation.setRequiredPathLength`, whichever is larger) times sixteen afterwards, and the same number is the region radius plus an 8 or 16 offset; the seven classes that raise the required length and their values; that the A\* **heuristic is multiplied by 1.5**, so the search is deliberately greedy and the result is not the shortest path; that a failed search still returns a best-effort path with `Path.canReach` false; that the closed set is accumulated only while something is subscribed to `DebugSubscriptions.ENTITY_PATHS`; the two give-up timers and their arithmetic (100-tick stuck check at speed times 100 times 0.25, with the speed *squared* below 1.0; per-node timeout at three times distance over speed times 20); and that `PathType`'s negative malus means impassable across 27 constants.~~
  - ~~**`reference/non-living-damage.md`** — twenty-one rows, hand-kept, each read one class at a time. Check the `ItemFrame` two-hit rule, the `EndCrystal` dragon immunity, the `VehicleEntity` accumulator and its creative-player discard, and the claim that `Player.attack` consults `Entity.isAttackable` and `Entity.skipAttackInteraction` before `Entity.hurtServer` is reached at all. `ShulkerBullet.hurtServer` checks **nothing at all**, not even `Entity.isInvulnerableToBase`, and always returns true — the one row with no guard.~~
  - ~~**`reference/attributes.md`** and **`reference/entity-data-serializers.md`** are generated by two new `gen_reference.py` views. Check the **regexes**, not only the output: pass 2 found that three of the four existing views had silently dropped rows to an over-narrow pattern. The attribute regex assumes every registration is a single-line `new RangedAttribute(...)`; the serializer view reads declaration order and registration order as two separate lists and reports any declared-but-unregistered serializer.~~

  ~~**Rewritten pages: the hooks, which are the sharpest new claims.**
  `entity-anatomy` — the pig default reaches the network and not the save
  file, with the whole path (`ByteBufCodecs.registry` →
  `IdMap.byIdOrThrow` → `DefaultedMappedRegistry.byId` never null, versus
  `EntityType.CODEC` = `Registry.byNameCodec` through the `Optional`
  lookup). `entity-lifecycle` — one y roll per category per chunk per tick,
  uniform from the world bottom to `Heightmap.Types.WORLD_SURFACE` plus one,
  with only x and z jittered across three group attempts.
  `synched-entity-data` — ids are `ClassTreeIdRegistry` ordinals with the
  spans `Entity` 0–7, `LivingEntity` 8–14, `Mob` 15, `AgeableMob` 16–17,
  `Sheep` 18, and both `SynchedEntityData.MAX_ID_VALUE` and
  `ClientboundSetEntityDataPacket.EOF_MARKER` are declared and unused.
  `attributes` — Strength II sends no packet, and the eight non-syncable
  names. `movement-and-collision` — the inside-block replay's ordering and
  the `InsideBlockEffectType` flush order, and that `Entity.visitedBlocks`
  dedupes across the whole replay rather than per segment.
  `ai-goals-and-brains` — the schedule is an `EnvironmentAttribute` looked
  up **by position**, and the within-tick priority claim that
  `UpdateActivityFromSchedule` at priority 99 runs after every behaviour it
  could affect, so a switch never bites in the tick it lands.
  `damage-and-death` — the silent-partial-hit flag, and the five families.~~

  ~~**Every diagram in the part was redrawn.** Fifteen figures across nine
  pages, and each arrow is an ordering claim: check them arrow by arrow,
  separately from the prose. The three most load-bearing are
  `entity-lifecycle`'s **spawn filter cascade** (every rejection in source
  order, with the only-now-is-the-mob-constructed boundary drawn),
  `attributes`' two-dirty-set flowchart (which set a change lands in, and
  that they are not a partition), and `damage-and-death`'s reduction
  flowchart (a dozen links, each owning one multiplication, with the running
  number on every edge).~~

  ~~**Process note.** All seven rewrites arrived with a full claim-diff from
  their drafting agent. `damage-and-death`'s came last and was **also**
  audited independently by the session against the decompile before it
  arrived — its non-living section, reduction pipeline, blocking path and
  `CombatRules` constants were re-derived here and the two accounts agree.
  That page is the one in the part with two independent audits.~~

- ~~**2026-09-03, session H — Part VII Items and inventories.** Eight pages,
  five rewritten and three new, every one drafted by an agent against the
  old page and diffed on arrival. **Fifteen figures, thirteen of them new or
  redrawn.** The part's two Reference catalogues are generated
  (`enchantment-hooks`, `loot-context-params`), so pass 4 should re-derive
  one row of each by hand rather than reading the table.

  **Nine pass-2 errors were found and corrected while rewriting.** These are
  the corrected claims, and pass 4 should confirm the corrections rather
  than the originals:
  `items-and-stacks` — `Item.Properties.repairable` is **eager**, not a
  delayed component (it takes a bootstrap registration lookup at class-init
  and stores an unresolved `HolderSet`), and `Inventory.tick` is reached
  from `Player.aiStep`, not `Player.tick`.
  `using-an-item` — **`CrossbowItem.useOnRelease` is the only override of
  `Item.useOnRelease` in the tree**; the old page said the bow, the crossbow
  and the trident all take that branch. The bow and trident are
  release-ended because their duration is 72000 and their
  `Item.releaseUsing` does the work, not because a predicate says so. *This
  one was audited twice: the session read it independently before the
  agent's report arrived, and the two agree.*
  `containers-and-menus` — the state id is compared before the click is
  applied and **branched on after**; and the two `AbstractContainerMenu.doClick`
  branches with no floor check are `ContainerInput.SWAP` and the painting
  phase of `ContainerInput.QUICK_CRAFT`, not the four the old page implied.
  `recipes` — `DecoratedPotRecipe` is a `CustomRecipe`, so **nine** of the
  fourteen crafting serializers are special, not eight; and eleven
  `SlotDisplay` variants are registered, not the eight listed.
  `enchantments` — **twenty-four** of the thirty-one effect components carry
  the decode-time validator, not ten; the three effect registries hold 6,
  15 and 16 entries, so it is fifteen of the sixteen location-based effects
  that are the entity effects, not fourteen of fifteen.
  `enchanting` — `/enchant` does **not** skip the supported-items and level
  rules: it rejects a level above the maximum outright (where the anvil
  clamps) and applies the same `Enchantment.canEnchant` predicate. What it
  skips is the *primary*-items filter, `DataComponents.ENCHANTABLE` and the
  cost.
  `loot-tables` — Fortune and Looting do **not** read
  `LootContextParams.ENCHANTMENT_LEVEL`: `ApplyBonusCount` and
  `BonusLevelTableCondition` read `LootContextParams.TOOL`,
  `EnchantedCountIncreaseFunction` and
  `LootItemRandomChanceWithEnchantedBonusCondition` read
  `LootContextParams.ATTACKING_ENTITY`; `ENCHANTMENT_LEVEL` is written only
  by the five enchantment effect contexts and read only by
  `EnchantmentLevelProvider`. Also, the single chest's menu provider **is**
  the block entity — the old trace drew `ChestBlock` handing to
  `ServerPlayer`.
  `contexts-and-predicates` — the old "five sets have no loot caller"
  sentence listed six sets under a count of five and included
  `LootContextParamSets.COMMAND`, which does have one
  (`ItemCommands.applyModifier`). The replacement claim, which pass 4 should
  re-count from scratch: **twelve of the twenty-six sets never roll a
  `LootTable`**. And `EntityPredicate.matches` builds no context;
  `EntityPredicate.createContext` does.

  **Claims introduced, per page** — the rewrites' new material, which pass 4
  checks hardest.
  `items-and-stacks`: the pop time as the five-tick hotbar squeeze and its
  writers; `DataComponents.COMMON_ITEM_COMPONENTS` as ten entries including
  an empty `ItemEnchantments`; twenty `delayedComponent` call sites in the
  whole game; `PatchedDataComponentMap.remove` storing an empty optional as
  a **tombstone**; `DataComponents.DAMAGE` as the only
  `ignoreSwapAnimation` component; the mining entry point
  (`ServerPlayerGameMode.destroyBlock` → `ItemStack.mineBlock` →
  `Tool.damagePerBlock`) and the copy taken before the damage; the break as
  entity event 47 with `LivingEntity.breakItem` re-deriving
  `DataComponents.BREAK_SOUND`; thirteen pixels of durability bar; exactly
  two `Item.inventoryTick` overrides (`CompassItem`, `MapItem`); the client
  binding components through `RegistryDataCollector`.
  `using-an-item`: what `useOnRelease` actually buys (a final
  `CrossbowItem.onUseTick` through the re-entry in
  `LivingEntity.releaseUsingItem`); five further call sites of
  `LivingEntity.releaseUsingItem`; the release carrying **no sequence
  number and no acknowledgement**, and `handleUseItem` snapping the
  rotation where `handlePlayerAction` does not — so the shot uses the
  server's last-known rotation; the client's draw spending no ammo and
  shooting nothing (`DataComponents.INTANGIBLE_PROJECTILE`);
  `EnchantmentHelper.onProjectileSpawned` running twice when ammo and
  weapon differ; the bow's shoot sound reaching the shooter only as the
  server's broadcast; `ServerPlayerGameMode.useItem` skipping
  `AbstractContainerMenu.sendAllDataToRemote` mid-use; the bow's three-stage
  pull as *assets/minecraft/items/bow.json*; the bow inheriting
  `UseEffects.DEFAULT` while `Item.Properties.spear` overrides it;
  `EntityEvent.USE_ITEM_COMPLETE` as the name of event 9.
  `containers-and-menus`: `HashedPatchMap.matches` owning the removed-set
  and per-component comparison (not `HashedStack.matches`);
  `HashOps.CRC32C_INSTANCE` and the 256-entry cache reaching each
  `RemoteSlot.Synchronized` through `ContainerSynchronizer.createSlot`;
  `CraftingMenu.finishPlacingRecipe` as a **third** caller of
  `CraftingMenu.slotChangedCraftingGrid`; `TransientCraftingContainer`
  calling back from `Container.setItem` always and `Container.removeItem`
  only on a real removal (so "on every write" was too strong); the click
  table's per-kind button semantics; the client never generating a state id;
  the 128-slot cap as the codec's; the closing transfer's shared set stated
  as the 36 main and hotbar slots (a derivation — check it).
  `recipes`: no `CustomRecipe` overriding `Recipe.display`;
  `TransmuteRecipe` returning one display per legal material count, so one
  recipe occupies many consecutive ids; `RecipeDisplayEntry.canCraft`
  returning false for an absent ingredient list and true for an empty one;
  `AbstractCraftingMenu.finishPlacingRecipe` as the hint parameter's real
  caller; the `RecipeCache` at ten entries, static on `CrafterBlock`;
  exactly five `RecipeBookMenu` subclasses while `RecipeBookCategories`
  still declares stonecutter and smithing; `Inventory.isUsableForCrafting`
  gating the pull as well as the tally; `ClientboundUpdateRecipesPacket`
  sent from exactly two places; `SelectableRecipe.SingleInputEntry.noRecipeCodec`
  writing the ingredient **and** the display.
  `enchantments`: forty-three vanilla enchantments; Fire Aspect's numbers
  from its JSON; `TargetedConditionalEffect.equipmentDropsCodec` pinning the
  affected target to `EnchantmentTarget.VICTIM`; the chain by which
  `ItemStack.getDamageSource` always reaches the single-entity constructor,
  which is why `DamageSource.isDirect` holds; `Player.itemAttackInteraction`
  running only on a true return from `Entity.hurtOrSimulate`;
  `Entity.baseTick` skipping the burn in lava and clearing fire for a
  fire-immune entity; five client callers of `CrossbowItem.getChargeDuration`
  (the old page said four); Fortune having **no** effect component and
  Looting exactly one; `LivingEntity.activeLocationDependentEnchantments` as
  the per-slot store; Lunge's impulse scaled flat.
  `enchanting`: the table charging the **slot index plus one**, not the
  displayed cost; the bottom slot's cost floored at twice the shelf count;
  thirty-two bookshelf offsets; the clue being a genuine member of the list
  you will receive, with the plain-book path deleting one entry at random
  first; every path transmuting `Items.BOOK` before enchanting, which
  changes which component the write lands in;
  `ItemStack.enchant` → `EnchantmentHelper.updateEnchantments` as the shared
  tail of all five paths; the anvil's four price components, the prior-work
  tax on both inputs, the flat 40 firing only when an enchantment actually
  transfers, the rename cap at 39 and the 40-and-over withholding; the
  grindstone paying its refund as orbs at the block; five vanilla
  enchantments declaring a narrower primary set; `SetEnchantmentsFunction`
  as the only ceiling-breaker; `/enchant` accepting level 0 and doing
  nothing; six of seven `VanillaEnchantmentProviders` entries being
  `SingleEnchantment`, which never asks whether the item supports the
  enchantment; villager trades running loot functions; `CreativeModeTabs` as
  a sixth producer; the ten data slots' split (3 costs, 1 seed, 3
  enchantment clues, 3 level clues); `EnchantmentNames.initSeed` running
  once per frame.
  `contexts-and-predicates`: validation comparing against
  `ContextKeySet.allowed` rather than `required`, so an element reading an
  optional key passes load-time validation and can still throw;
  `LootContextParamSets.ALL_PARAMS` never building a `ContextMap` at all;
  twenty-seven overriders of `getReferencedContextParams`; the two hard
  validators building a resolver-less `ValidationContext`, so a
  `ConditionReference` is rejected outright; `LootContextArg` and the three
  target enums; the predicate resolved at parse time by
  `ResourceOrIdArgument` where the selector option looks its own up and
  returns a silent false; both command call sites pre-seeding the recursion
  guard; the three-way random-sequence precedence on
  `LootContext.Builder.create`; twenty condition types and eight number
  providers, with the two codec-leniency rules; `SlotSource` as a third
  `LootContextUser` family; the network exclusion restated as absence from
  `RegistryDataLoader.SYNCHRONIZED_REGISTRIES`.
  `loot-tables`: forty-two of the forty-three functions extending
  `LootItemConditionalFunction`, whose failed condition is a **no-op, not a
  veto**; nine entry types; 117 named keys in `BuiltInLootTables` plus two
  colour families; `MonsterRoomFeature`'s two chest attempts;
  `StructurePiece.createChest` as the structure-side seed writer;
  `trySaveLootTable` writing the seed only when non-zero; the weight being
  floored **and then** discarded at or below zero, which are two steps;
  `ByteBufCodecs.fromCodecWithRegistries` as the fallback that carries
  `DataComponents.CONTAINER_LOOT` to the client;
  `AbstractVillager.addOffersFromTradeSet` using `TradeSet.randomSequence`;
  two callers of `MinecraftServer.getRandomSequence`;
  `ShulkerBoxBlock.getDrops` and `DecoratedPotBlock` as the only dynamic
  drops.

  **The diagrams.** Fifteen figures: two containment and pattern flowcharts
  (`items-and-stacks`, `enchantments`), five decision flowcharts (the
  server's resync ladder, the ending guard, one roll, `selectEnchantment`,
  the recipe load and its four indexes), and eight sequence diagrams. Check
  arrow by arrow, and in particular: `loot-tables`' trace, whose two
  orderings were corrected this session (the block entity is its own menu
  provider; `ClientboundOpenScreenPacket` precedes `ServerPlayer.initMenu`);
  `enchantments`' Fire Aspect trace, whose closing packet arrow became a
  note because `SynchedEntityData` does not send through the packet
  listener; and `using-an-item`'s two traces, which are deliberately
  isomorphic — if one is wrong the other probably is too.

  **The landing page and `lectures.md`** claim that the three engines depend
  on the vocabulary and on nothing of each other, and that Part XIII needs
  `contexts-and-predicates`. Both are orderings to check.

- **Session I (Part VIII The player), 2026-09-03.** Seven pages: two rewritten
  in place (`player-anatomy`, `the-sword-swing`), one edited hard
  (`input-to-movement`), one renamed (`hunger-xp-and-effects` →
  `hunger-and-experience`) and three new (`the-two-phase-tick`,
  `status-effects`, `the-spear`), plus the landing page. Everything except
  `the-spear` is pass-2 prose re-cut; **`the-spear` is entirely new material
  and should be checked first and hardest**, because no pass-2 agent has ever
  read those classes.

  **`the-spear`'s claims, all from `PiercingWeapon`, `KineticWeapon`,
  `Item.Properties.spear`, `LivingEntity.stabAttack`, `Player.stabAttack`,
  `Minecraft.startAttack`, `MultiPlayerGameMode.piercingAttack`,
  `ServerGamePacketListenerImpl.handlePlayerAction` and `ItemStack.onUseTick`:**
  that `Item.Properties.spear` attaches nine components and the two attribute
  modifiers listed in the table (check the `AttackRange` numbers 2.0 / 4.5 /
  2.0 / 6.5 against the record's field order — `minReach`, `maxReach`,
  `minCreativeReach`, `maxCreativeReach`, `hitboxMargin`, `mobFactor` — and
  the seven materials); that the stab packet carries no entity id and dummy
  position and direction; that `handleAttack` refuses a piercing weapon while
  the `STAB` case requires a non-spectator and a five-tick
  `Player.cannotAttackWithItem` tolerance; that `PiercingWeapon.attack` uses
  the **attribute value** of `Attributes.ATTACK_DAMAGE` and hits every entity
  along the ray under `ClipContext.Block.COLLIDER`; that
  `PiercingWeapon.canHitEntity` is the shared filter for **both** components;
  that `Item.getUseDuration` is 72000 for a kinetic weapon and
  `LivingEntity.startUsingItem` allocates `recentKineticEnemies` server-side
  only; that `ItemStack.onUseTick` **replaces** `Item.onUseTick` for a kinetic
  weapon; that `KineticWeapon.damageEntities` uses the **base** value of
  `Attributes.ATTACK_DAMAGE` and `Entity.getKnownSpeed` scaled by twenty,
  taking the root vehicle for a non-player passenger; that the three
  `KineticWeapon.Condition`s are independent and any one of them produces a
  hit; that the non-player action factor is 0.2 and therefore *lowers* the
  thresholds; that the hit feedback is entity event 2 → `LivingEntity.onKineticHit`,
  throttled by `KineticWeapon.HIT_FEEDBACK_TICKS`; that
  `CriteriaTriggers.SPEAR_MOBS_TRIGGER` counts living entities stabbed; and
  the page's hook — **`Player.stabAttack` skips both cooldown curves when the
  player is currently using an item in that slot**, so a charge is uncharged
  and a stab is not. Also check the mob roster (`SpearUseGoal`,
  `SpearApproach`, `SpearAttack`, `SpearRetreat`; `Zombie`, `ZombifiedPiglin`,
  `PiglinAi`) and the claim that `KineticWeapon.forwardMovement` is read only
  by `SpearAnimations`.

  **One pass-2 claim was corrected while redrawing.** `the-sword-swing`'s old
  numbered list gave `Player.canCriticalAttack` as the crit gate; the crit is
  `fullStrengthAttack && canCriticalAttack`, so the attack-strength scale
  above 0.9 is part of the crit condition and the page now says so. Re-derive
  it, and with it the whole flowchart, which is the session's one figure that
  asserts an arithmetic **order**: base and boost are scaled separately, the
  item bonus is added to the base *before* the ×1.5, and the boost is added
  after it.

  **Claims moved rather than written.** The authority matrix was **deleted**
  from `input-to-movement` and `player-anatomy` and replaced by a link to
  `entities/authority.md` plus two named consequences (fall damage via
  `Entity.doCheckFallDamage`; the ground flag). Check that nothing true was
  lost in the deletion, and that the surviving two sentences agree with the
  Part VI page. The record–simulate–snap-back bracket and the whole *when it
  runs* material moved from `player-anatomy` to `the-two-phase-tick`; the
  effects third of `hunger-xp-and-effects` moved whole to `status-effects`,
  and `UseEffects` stayed with the hunger page while `the-spear` links to it.

  **The diagrams.** Seven figures. New: the class ladder
  (`player-anatomy`, a flowchart replacing an ASCII tree), the damage flow
  (`the-sword-swing`), the two-entries-one-exit flowchart (`the-spear`), the
  `FoodData.tick` chain (`hunger-and-experience`), the part-shape flowchart
  (landing page). Redrawn: the two-phase sequence (lanes corrected, and it
  now shows the bracket), the Poison trace (`status-effects`, new). Check the
  `FoodData.tick` flowchart's *at most one of three* claim and the ordering
  inside the two-phase diagram arrow by arrow.

  **The landing page and `lectures.md`** claim that only the sword swing and
  the spear have an internal order, that Part VIII depends on Part VI's
  authority above everything, and that the spear needs `using-an-item`.

- **2026-09-03, pass 3 session J — Part IX Networking.** Four of the five
  pages rewritten (`the-connection` 550→442, `packets-and-stream-codecs`
  448→449, `what-the-client-is-told` 546→461, `chat-and-signing` 365→316);
  `src/systems/networking/README.md` new; `protocol-phases` unchanged except
  three sentences of hand-off links. All five diagrams below are new or
  redrawn.

  **Two of the four pages have no list of introduced claims, and pass 4 must
  treat them as unlisted.** The drafting agents for
  `packets-and-stream-codecs` and `chat-and-signing` both finished writing
  and then died on a rate limit before reporting, so the session accepted
  two finished pages without the claim-by-claim diff the protocol requires.
  The session's own checks passed on them (names, lanes, mermaid, budgets,
  shape) and it spot-checked four load-bearing claims by hand —
  `detectRateSpam`'s operator and singleplayer-host exemptions, the 4,096
  pending-message disconnect threshold, the id-is-a-registration-position
  hook, and the *three ways to say no* branch — but **the other pages'
  guarantee that every reworded sentence was diffed against pass 2's text
  does not hold for these two.** Re-check them whole, at the sentence level,
  against `git show b597a2a~1:src/systems/networking/<page>.md`.
  `chat-and-signing` is the higher risk of the two: it is a security page,
  its central artefact is a new eighteen-row table of *which failure kills
  the message, the chain, or the connection*, and every row is a claim about
  a specific outcome that pass 2 never stated in that form.

  **Claims introduced in `the-connection`, listed by its agent with cites.**
  A handler touching no game state omits `PacketUtils.ensureRunningOnSameThread`
  and runs on Netty (`handlePong` and `handleCustomPayload` are empty bodies
  — the session verified this one). The `PacketProcessor` queue is unbounded
  and each drain empties it (verified). The client's handling latency is a
  frame, not a tick — the borrowed fact restated as this page's consequence.
  The singleplayer host has neither the read timeout nor the keep-alive
  running against it — a *composition* of two old-page facts and therefore
  the one to re-derive. And the diagram's note that there is one encoder and
  one decoder instance at each end.

  **Claims introduced in `what-the-client-is-told`, listed by its agent.**
  That the cascade is three gates and each is a three-term test (a
  conjunction, then two disjunctions) — a synthesis across `ChunkMap` and
  `ServerEntity`, and the assertion the new flowchart rests on, so it is the
  first thing to check. `PlayerChunkSender.START_CHUNKS_PER_TICK` and
  `MAX_UNACKNOWLEDGED_BATCHES` named as the constants behind "nine" and
  "ten". Two `ChunkBatchSizeCalculator` constants attached to the clamp and
  the weighted mean. That the forced absolute sync is rarer than the forced
  position packet by however long the interval gate stays shut — an
  inference from two counters, one inside the gate and one outside. That the
  passenger-list packet is the filtered one, so a mounting player is told
  from their own point of view. And that equipment, passengers and leash
  links appear in the pairing bundle only when non-empty.

  **The diagrams.** New: the round-trip sequence in `the-connection` (six
  lanes, four thread boundaries marked, the reply returning to a second
  drain — the pair's whole reason to exist, and every arrow an ordering
  claim); the gate flowchart in `what-the-client-is-told`; the codec
  composition flowchart in `packets-and-stream-codecs` (which asserts that
  nothing above the `ProtocolInfoBuilder.addPacket` line knows about ids and
  nothing below it knows about chat); the *three ways to say no* flowchart in
  `chat-and-signing`; the part-shape flowchart on the landing page. Trimmed:
  the pairing-bundle sequence, which is all that survives of
  `what-the-client-is-told`'s old trace.

  **Claims deleted rather than rewritten.** `what-the-client-is-told` lost
  its whole client half to Part X (the list is in [pass3.md](pass3.md) for
  session K). Check that nothing true was lost in that deletion and that the
  surviving one-paragraph hand-off agrees with `the-client-level` and
  `prediction-and-acks` once session K has been over them.

  **The landing page and `lectures.md`** claim that the first two lectures
  are one lecture in two halves, that lectures four and five are independent
  of each other and both assume three, that Part IX assumes Part III and
  Part I's two loops, and that Part IX is a prerequisite of Part X. Three
  are orderings, which pass 2 found is where this corpus is most confidently
  wrong.

- **2026-09-03, pass 3 session K — Part X The client.** Twelve pages
  rewritten in shape, one page split into two, one landing page and one
  Reference page written. The whole part is on this list; below is what
  pass 4 should check *hardest*, being what the rewrite introduced.

  **One ordering the rewrite corrected, which is the first thing to
  re-check.** `the-client-loop`'s old sequence diagram put
  `FramerateLimiter.limitDisplayFPS` after the *Post render* section, i.e.
  at the end of `Minecraft.runTick`. It is not there: it is inside
  `Minecraft.renderFrame`, after the present and before *Post render*, and
  it is gated on `GameRenderState`'s framerate limit being below 260 rather
  than on the tracker being asked again at that moment. The new flowchart
  says so. Confirm both halves of that correction.

  **The hooks, one per page, all new or newly load-bearing.** The frame that
  earns fifteen ticks runs ten and loses five (`the-client-loop` — the claim
  was in the old page's invariants, it is now the opening paragraph). The
  client's tick lists accept a schedule and then answer *no* when asked
  whether one is pending, so a predicted repeater looks inert
  (`the-client-level` — the *repeater* is the session's example and is not
  in the decompile as such: check that a repeater actually reschedules
  itself through the black-holed path). The receipt is for a number and is
  sent for refusals (`prediction-and-acks`, unchanged in substance). A
  toggle-sneak press flips the mapping and the *release* is swallowed
  entirely, and a screen closing turns the toggle back on
  (`input-and-keybinds` — new scenario this session, read from
  `ToggleKeyMapping` and `KeyMapping.restoreToggleStatesOnScreenClosed`). A
  cycle button broadcasts your `ClientInformation` on every click
  (`options`, unchanged). Pressing E sends and receives nothing
  (`gui-and-screens`, unchanged). Layering is inferred from bounding boxes
  (`the-gui-render-tree`, unchanged). Measuring bakes (`text-and-fonts`,
  unchanged). F1 does not hide the sleep fade (`hud`, unchanged). A sound
  always starts at least one hop after the packet (`sound-engine`,
  unchanged). Most world sounds are an int (`what-makes-a-sound`,
  unchanged). Nothing is stripped from the shipped jar
  (`debugging-the-running-game`, unchanged).

  **Facts added this session, which had no owner before.**
  `Entity.moveOrInterpolateTo` and the seven overrides of
  `Entity.getInterpolation` — `LivingEntity`, `Display`, `ExperienceOrb`,
  `Shulker`, `FishingHook`, `AbstractBoat`, `AbstractMinecart` — against a
  default that returns null and therefore snaps; the page's *snaps* column
  names `AbstractArrow`, `PrimedTnt`, `ItemEntity` and `FallingBlockEntity`
  as examples of the default, which is an inference from *does not override*
  and should be spot-checked. `ClientPacketListener.serverChunkRadius` and
  `ClientPacketListener.serverSimulationDistance`, seeded at login and handed
  to each new `ClientLevel`. `ClientChunkCache.Storage` as an
  `AtomicReferenceArray` with volatile centre coordinates, and the claim
  that the reason is the render thread reading them — a *why*, and therefore
  weaker than the *what*. `Entity.isInterpolating` being read by
  `ServerboundMoveVehiclePacket` and `PositionMoveRotation`. And
  `DebugSubscriptions.DEDICATED_SERVER_TICK_TIME` named properly, replacing
  the old page's awkward reference to a `RemoteDebugSampleType` constant; the
  count of sixteen was re-derived by counting the fields, and the four
  expiring kinds now carry their tick counts (60, 100, 200, 200).

  **The new Reference page is thirty rows of gate, and every row is a
  claim.** `src/reference/hud-elements.md` was read one method at a time out
  of `Hud.extractRenderState` and `Gui.extractRenderState`. Two rows are
  inferences rather than transcriptions and should be checked first: row 13,
  that mount health sits *outside* the can-hurt-you block and so shows in
  creative; and row 26, the two different paths by which subtitles are
  recorded when the HUD is hidden. Also check the preamble's claim that
  `GuiRenderState.isHudHidden` is published before the loading-screen
  short-circuit.

  **The diagrams.** New and asserting orderings: the one-turn flowchart in
  `the-client-loop` (every edge is an ordering claim, and the clamp is a
  decision node); the two-column `stateDiagram-v2` in `prediction-and-acks`
  (five client transitions and three server ones, and the claim that no
  transition anywhere is "the server said no"); the setting-change flowchart
  in `options`; the containment flowchart in `gui-and-screens`; two
  flowcharts in `the-gui-render-tree`, one of the data and one of the draw
  pass; the six-stage pipeline flowchart in `text-and-fonts`; the record-order
  flowchart in `hud`, which asserts exactly where the sleep fade sits; the
  three-doors flowchart in `what-makes-a-sound`; the hub-and-spokes figure on
  the landing page, whose seven arrow labels are cadence claims. Redrawn:
  the sneak trace in `input-and-keybinds` (a different scenario from the old
  page's, so it is a new diagram not an edited one). Kept and re-checked:
  the chunk-arrival sequence in `the-client-level`, the refusal sequence in
  `prediction-and-acks`, the inventory sequence in `gui-and-screens`, the
  chat-line sequence in `text-and-fonts`, the hearts sequence in `hud`, the
  villager-brain sequence in `debugging-the-running-game`, and the
  block-placed sequence now in `sound-engine`.

  **The split.** `sound.md` became `sound-engine.md` and
  `what-makes-a-sound.md`. Nothing was cut in the split, but material moved
  across the seam and pass 4 should read the two together once: the engine
  page keeps `SoundInstance`, the threads, the channel limits, the volume
  arithmetic, looping and the device, and the content page keeps
  `SoundEvent`, `SoundSource`, `sounds.json`, level events, the local-player
  prediction, propagation delay and the environment-attribute music model.
  The one claim that was *sharpened* rather than moved: a server can name a
  sound in no registry (inline `SoundEvent` in the stream codec) while data
  packs cannot register one — the old page said this in passing and the new
  one makes it a table row.

  **The landing page and `lectures.md`** claim that Part X is a hub and
  spokes rather than a pipeline, that only the GUI stack is internally
  ordered, that Part IX and Part V are both prerequisites, and that
  `the-client-loop` is a prerequisite of Part XI. All four are orderings.

---

## Session M — Part XII World generation *(2026-09-03)*

**Two errors found while rewriting, which is four part-sessions in a row.**
Both are counts, and both had survived pass 2 because nobody had recounted
them against the registration site.

- **`features-and-placement` said sixty-three features are registered into
  `BuiltInRegistries.FEATURE`. It is 61** (`Feature.java`, counting the
  registering assignments). Fixed in place. The page's separate observation
  that being a `Feature` subclass does not imply being registered — the
  dragon fight's podium feature — is unchanged and still true.
- **The same page called `CountOnEveryLayerPlacement` "the fifteenth" of the
  fifteen placement modifier types.** There are fifteen, but it is **ninth**
  in `PlacementModifierType`'s declaration order, so "the fifteenth" reads
  as an ordinal and is wrong. Reworded to "one of the fifteen". Pass 4
  should treat every *ordinal* in the corpus the way it treats counts.

**Claims this session introduced, hardest first.**

- **The overworld noise cell is four blocks wide, four deep and eight tall,
  and a chunk holds 768 of them** (`terrain`, stated as *the number*).
  Derived from `NoiseSettings.OVERWORLD_NOISE_SETTINGS` (horizontal size 1,
  vertical size 2) through `NoiseSettings.getCellWidth` and
  `NoiseSettings.getCellHeight`, which multiply by four via
  `QuartPos.toBlock`, and from `NoiseBasedChunkGenerator.fillFromNoise`'s
  cell counts (16 / 4 = 4 each way, 384 / 8 = 48 up). No page said any of
  this before.
- **1,225 corner samples per interpolated density term, per chunk**
  (`terrain`, the second *number*). Five slices, five Z, forty-nine Y: read
  off `NoiseChunk.fillSlice` (which loops the horizontal cell count plus
  one) and the slice-filling context provider (which loops the vertical cell
  count plus one), plus the five slices that
  `NoiseChunk.initializeForFirstCellX` and four `NoiseChunk.advanceCellX`
  calls fill. Check the slice count first: it is the one step in the
  arithmetic that is an inference from loop structure rather than a literal.
- **The six-deep nesting figure in `terrain`** asserts the exact loop order
  of the noise fill: cell X, cell Z, cell Y *descending*, block Y
  *descending*, block X, block Z — and that `NoiseChunk.advanceCellX` fills
  the next slice while `NoiseChunk.swapSlices` drops the old one at the end
  of each X column. Every level of that nesting is an ordering claim.
- **The three-forms figure in `density-functions`** asserts what survives
  each rewrite: that `RandomState`'s wiring visitor fills noise holders and
  rebuilds `BlendedNoise` and the end-islands node while leaving
  `DensityFunctions.Marker` and `DensityFunctions.HolderHolder` **intact**,
  and that only `NoiseChunk.wrapNew` resolves those two. It also asserts
  that the parsed form is sampled by nothing at all — the F3 readout samples
  `RandomState.router`, the *once*-rewritten form, which corrects the old
  page's framing rather than its facts.
- **`DensityFunctions.FindTopSurface` is a node type the corpus had never
  named**, and it is the thirty-fourth and last registration. The claims to
  check: that there are exactly **34** registered types (four by name, six
  markers, nine by name, seven mapped, four arithmetic, four last), and that
  its declared bounds are **Y coordinates rather than densities**, which
  makes it the one node whose range is on a different scale from the rest of
  the catalogue.
- **`DensityFunctions.shift` — the three-dimensional domain warp — has no
  callers and appears in no shipped file** (`density-functions`, and the
  Reference page's closing section). Also: *constant*, *cache_all_in_cell*
  and *beardifier* are never written as typed objects in vanilla data, the
  last two being added in code by `NoiseChunk`'s constructor.
- **`DensityFunction.NoiseHolder` reports a maximum of 2.0 while its noise
  is null**, so the parsed graph reports wider noise bounds than the seeded
  graph it becomes. New, and the kind of claim one test would settle.
- **`DensityFunctions.Spline` has a hand-written equality that ignores its
  derived sampler**, offered as the *mechanism* behind the old page's "the
  rewrite memo is structural, not by reference". The old claim was about
  records generally; this names the one node that is not a record and still
  merges.
- **`NoiseChunk.BlendOffset` reports infinite bounds where the data-side
  `DensityFunctions.BlendOffset` reports zero** — in the Reference page
  only, and never checked by pass 2.

**`trees` is a new page and every claim in it is new.** It was written from a
source inventory of `TreeFeature`, `TreeConfiguration`, the four placer
packages, the feature-size package, `TreeFeatures` and `TreeGrower`, and
five of its claims were re-read against the decompile by hand before
publishing. Those five: that `TreeFeature.doPlace` derives the foliage
height and the leaf radius from the **unclipped** proposed height and passes
the *clipped* height to both placers, so a clipped tree keeps a full-size
crown; that the clearance scan returns *two below* the first blocked layer;
that `FancyTrunkPlacer`'s crown-candidates-per-level count is pinned at one
by a minimum against one over an expression that is never below one, making
the named density constant inert; that `CherryFoliagePlacer`'s codec gives
the *corner hole chance* field a getter returning the **wide bottom layer**
field, so any encode writes one value into both; and that
`TreeGrower.DARK_OAK` declares only a mega tree, which is why a lone
dark-oak sapling never grows, with `TreeGrower.PALE_OAK` doing the same and
pointing at the decorator-free bone-meal variant.

The rest of that page is inventory-sourced and wants checking row by row:
the nine trunk placers, the eleven foliage placers, the ten decorators, the
five-species table with its numeric configurations, the mangrove root
recursion that "succeeds by failing" (and the muddy-roots branch that skips
its moss carpet), and the bucketed leaf-distance walk whose pre-marked
decoration and root sets *block* propagation. Counts to re-derive: 9 trunk
placers, 11 foliage placers, 1 root placer, 2 feature sizes, 10 decorators —
and the claim that `MegaJungleFoliagePlacer` is registered under a *jungle*
id rather than a *mega jungle* one.

**The split, and where material crossed the seam.** `structures.md` became
`structure-placement.md` (redirected) and `jigsaw-and-templates.md`. Read the
two together once: placement keeps the lottery,
`ChunkGeneratorStructureState`, `Structure`, `StructureStart`, the reference
scan, `StructureCheck`, both `StructureManager`s, `Beardifier`,
`TerrainAdjustment`, the locate command and the per-chunk write; jigsaw keeps
the pools, the assembly loop, the template system and the whole processor
stack — which `hand-built-structures` now reaches by link rather than owning
a share of. Three framework facts moved from the old page's invariant wall
onto `structure-placement` and should be re-read in their new context: that
the reference position comes from **piece zero**, that
`Structure.adjustBoundingBox` inflates the box by twelve, and that
`StructurePiece.postProcess` runs once per overlapping chunk and must be
idempotent. Two facts moved *off* `terrain` because
`features-and-placement` already owned them better — the minus-one default
write radius and `WorldGenRegion.getChunk` throwing — and pass 4 should
confirm they are not now stated nowhere.

**Diagrams, all of them new or redrawn.** The status-ladder figure on the
landing page, whose whole point is that the lecture order runs *against* the
execution order — every subgraph placement is a claim about which status owns
which page. The four-status hand-off flowchart and the six-deep nesting
figure in `terrain`. The three-forms figure in `density-functions`. The
four-decision flowchart in `structure-placement`, which asserts that
`ChunkStatus.STRUCTURE_STARTS` is the second status and two before
`ChunkStatus.BIOMES`. The modifier-fold flowchart in
`features-and-placement`, whose eight stages are an ordering claim about a
*vanilla* chain rather than a required one. The five-lane sequence in
`trees`. Redrawn on the same subject: the biome trace (six lanes now, the
two read paths moved out of the diagram into a comparison table) and the
village and stronghold traces (relabelled, and the village one now stops at
the pieces rather than running on into the blocks). Nothing in the part
survives unredrawn.

**The landing page and `lectures.md`** claim: that the part is a substrate, a
pipeline and a wing; that the structure wing is decided at
`ChunkStatus.STRUCTURE_STARTS` and written at `ChunkStatus.FEATURES`; that
biomes and terrain are independent statuses and can be watched in either
order; that jigsaw and hand-built are alternatives rather than a sequence;
that Part IV's chunk-generation pipeline is a hard prerequisite; and that
`world/level/levelgen` plus `world/level/biome` come to **423 classes and
45,600 lines** (counted this session, one class per file, package markers
excluded; pass 2 said 429 and 46,628 for a boundary it never stated).

## Session N — Part XIII Commands and data packs *(2026-09-03)*

Nine pages where there were five, and **every one of them was rewritten**.
Two splits (`execution-and-functions` → `the-execution-engine` +
`functions-and-macros`; `dialogs-and-tests` → `dialogs` + `game-tests`), one
page written from nothing (`permissions`, the R7 spend), one landing page,
and four whole-page reshapes. Nothing in the part survives unredrawn either:
every diagram in Part XIII is new or redrawn.

**Check first and hardest: the counts this session re-derived, because they
disagree with pass 2 in three places and the disagreements are the kind pass
2's lesson predicts.**

- `permissions` says **95** `Commands.hasPermission` call sites, of which 94
  are server-side command registrations and the ninety-fifth is
  `ClientPacketListener`'s node builder. Pass 2 said "all ninety-four
  *requires* calls in the game use it", which was a true statement about the
  server and a false one about the total: `.requires(` appears 245 times in
  `net/minecraft`, and the other 150 are `ShapelessRecipeBuilder.requires`,
  an unrelated method. The re-derivation to run is
  `.requires(Commands.hasPermission(` against every `Commands.hasPermission(`.
- The per-level gate counts are stated as **66 gamemaster, 16 admin, 9
  owner**, counted as `requires(Commands.hasPermission(Commands.LEVEL_X))`.
  Raw occurrences of `Commands.LEVEL_GAMEMASTERS` are **68**, and the two
  extra are the ternaries in `SeedCommand` and `VersionCommand`. Pass 2's 66
  was right; the arithmetic that reconciles 95 = 66 + 16 + 9 + 2 (the
  `LEVEL_ALL` ternaries) + 2 (the two non-constant checks) is new and should
  be re-run as a whole.
- The **two non-constant permission checks** are new material:
  `ClientPacketListener.RESTRICTED_COMMAND_CHECK` and
  `GameModeCommand.PERMISSION_CHECK`. The second carries a page-level claim —
  that it is read by `KeyboardHandler`, `GameModeSwitcherScreen` and
  `ServerGamePacketListenerImpl`, i.e. that the F3+F4 switcher greys out by
  running a *server* permission check locally against `LocalPlayer`'s own
  set. Five call sites; count them.
- `advancements` now says the client half is **five classes in
  `client/gui/screens/advancements` plus `ClientAdvancements` in
  `client/multiplayer`, about 1,240 lines**. Pass 2 said "six classes and
  about eleven hundred lines (`net/minecraft/client/gui/screens/advancements`)",
  which counted `package-info.java` as a class and put `ClientAdvancements`
  in the wrong package. The screens package is 1,112 lines over five classes;
  `ClientAdvancements` is 128.
- The landing page says the part is **442 classes and 43,800 lines** over
  nine packages (`commands`, `server/commands`, `server/permissions`,
  `advancements`, `world/scores`, `server/dialog`, `gametest`, and the two
  client screen packages), counted one class per file with package markers
  excluded, the way session M counted Part XII. Nothing in pass 2 states a
  boundary for this part, so this is a new claim end to end.
- `permissions` says `net/minecraft/server/permissions` is **eleven classes
  and 398 lines**; the old page said "twelve files", which included
  `package-info.java`.

**New claims the rewrite introduced, from re-reading the source.** All of
these are this session's, not pass 2's, and none has been checked by anyone
else:

- `PermissionSet` is a **functional interface** with one method, so every set
  in the game except `ChatAbilities`' is a lambda or a tiny object, and there
  is no set-of-permissions data structure anywhere else.
- `LevelBasedPermissionSet.union` of two level-based sets returns **the
  higher of the two** rather than a `PermissionSetUnion`. This is the
  mechanism `functions-and-macros` then leans on for its "the method whose
  name reads like a ceiling can only add" paragraph.
- `PermissionLevel.byId` uses `ByIdMap.OutOfBoundsStrategy.CLAMP`, so an
  *ops.json* hand-edited to level 9 is an owner and −1 is rung zero.
- `Permission.CODEC` accepts an atom written as a **bare identifier** as well
  as the full dispatched form.
- `MinecraftServer.getProfilePermissions` returns a `LevelBasedPermissionSet`
  in every branch, and `ServerPlayer.permissions` calls it afresh every time
  — nothing is cached on the player. The cascade as restated: not on the op
  list → `ALL`; on it → the op entry's own set, else singleplayer owner →
  `OWNER`, else singleplayer → `OWNER` or `ALL` by the allow-cheats-for-others
  toggle, else the *op-permission-level* property.
- `PermissionSetUnion` holds a **reference** set (`ReferenceArraySet`), so
  identity, not equality, decides whether unioning the same set twice
  duplicates it.
- `ChatAbilities` is built **by subtraction**: it starts from all four of
  `Permissions.CHAT_PERMISSIONS` and each `ChatRestriction` removes some.
  There are four restrictions and **all four are local decisions** (two chat
  options, the launcher, the account profile) — no server grants a client
  chat permission. This is a structural claim about the whole enum; check
  that no fifth value and no server-driven route exists.
- `ClientPacketListener`'s ordinary suggestions provider has the player's own
  set **OR-ed with** the synthetic restricted atom, and
  `restrictedSuggestionsProvider` is the `NO_PERMISSIONS` one — the field
  name reads backwards from what it holds.
- `ClientPacketListener.verifyCommand` has **four** outcomes
  (`NO_ISSUES`, `PARSE_ERRORS`, `SIGNATURE_REQUIRED`, `PERMISSIONS_REQUIRED`)
  and the flowchart on `permissions` asserts their order: parse with
  permissions, then signable-argument test, then parse *without* permissions.
  Every branch of that figure is an ordering claim.
- `functions-and-macros` says `ServerFunctionManager.execute` swallows only
  `FunctionInstantiationException` with an empty catch, and logs **any other
  exception at warn**. Pass 2 recorded the empty catch and not the warn arm.
- `ServerFunctionManager.getGameLoopSender` uses
  `CommandSourceStack.withPermission` (a **replacement**) with gamemaster over
  a server source that is `LevelBasedPermissionSet.OWNER`, while
  `FunctionCommand` and `DebugCommand` use
  `CommandSourceStack.withMaximumPermission` (a **union**). The page claims
  the tick and load tags therefore run *lower* than the console does; check
  both directions.
- `game-tests` says `/test` sits at `Commands.LEVEL_GAMEMASTERS` and
  `TestCommand.TEST_FULL_SEARCH_RADIUS` is 250, with the radius subcommand
  clamping a user-supplied radius to 0–1024.
- `the-execution-engine` restates `ContinuationTask.schedule`'s arithmetic
  with the **two-element case made explicit** (nothing / one entry / *two
  entries* / one self-entry), which the old page elided.
- `scoreboard-and-data` adds that `ScoreContents` and `NbtContents` resolve
  on the server and put the *result* on the wire — restated from pass 2's
  invariant, now framed as a third route by which a score reaches a client.

**Redrawn and new diagrams, each an ordering claim.**

- `commands/README.md`'s three-floor figure: that the dependency is strictly
  one-directional and that the four top-floor pages are peers.
- `brigadier-and-commands`'s six-lane trace, with the Netty-thread note moved
  onto the diagram as a `Note over`.
- `permissions`' containment figure (question / answer / check) and its
  four-outcome `verifyCommand` cascade — both new.
- `the-execution-engine`'s **queue-snapshot figure**, which is the most
  load-bearing new diagram in the part: four panels claiming that
  `BuildContexts` walks *all* non-execute stages inside entry one, that the
  fan-out becomes a single `ContinuationTask`, and that element *i+1* is not
  materialised until element *i* has finished. Check panel by panel.
- `functions-and-macros`' four-stage pipeline flowchart, including the claim
  that the TRIGGER arrow lands on *instantiate* rather than on *compile*.
- `advancements`' trace, relaned and with a tick-boundary note added.
- `dialogs`' trace (unchanged in substance, relaned) and `game-tests`' two
  figures — a new containment flowchart (declaration / run / world) and the
  old runner sequence, relaned.
- `scoreboard-and-data`'s trace, relaned, with `EntityDataAccessor` folded
  into `DataCommands`.

**The landing page and `lectures.md`** claim: that Part XIII is a stack of
three floors; that nothing in advancements, scoreboards, dialogs or game
tests is needed to understand the parser or the engine, and that all four
need both; that the four top-floor lectures are watchable in any order; and
that the part's stated prerequisites are Part III's server tick (for two
distinct reasons), Part II's codecs and data-driven type pattern, Part IX's
connection, and Part VII's contexts and predicates for advancements alone.

**Material that moved, and must not now be stated nowhere or twice.** The
permission model left `brigadier-and-commands` entirely; that page keeps the
tree's *serialisation* (templates, the unknown-argument-type stub, the one
call site) and `permissions` took the *meaning* of the filtering (absent
versus flagged, the null-source inspector, the client's two sources). Read
the two together once. The `/schedule` gate, the two function tags and the
compile-time permission set left the engine page for
`functions-and-macros`. `dialogs-and-tests`' "the pattern, stated once"
section was **deleted, not moved** — Part II's
`foundations/data-driven-types.md` owns that argument and both new pages
link to it; confirm nothing true was lost with it.
