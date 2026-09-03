# Creating a world

> Verified against **Minecraft 26.2** · Part XII · *Create New World*: a seed typed in, Superflat chosen, a layer deleted, an experiment switched on, and the settings object that comes out the other end.

You click *Create New World* and nothing happens for a moment. Then a
three-tab screen: a name, a game mode, a seed box, a world-type button, and
buttons for game rules, data packs and experiments. You type a seed, cycle the
type to *Superflat*, open *Customize* and delete the dirt layer, switch on an
experiment, set one game rule, and press *Create*.

That opening pause is what this page is about. Before the screen can draw a
single widget the game has already run a **complete server-side data-pack
load** — the same `WorldLoader.load` a dedicated server runs at startup — on a
background thread, with the client's main thread parked on
`BlockableEventLoop.managedBlock` until it finishes. The object the screen
exists to edit, `WorldGenSettings`, was built halfway through that load, out
of registries the load had just filled. Every widget is an edit to it. Two of
the buttons throw the whole load away and run it again. And *Create* barely
touches it: by the time you press the button, the world's generation settings
have existed in memory for as long as the screen has.

Everything else in [Part XII](README.md) reads that object. This page is where
it comes from, where it goes, and the three different programs that build one.

## The cast

| class | what it owns | its thread |
|---|---|---|
| `WorldGenSettings` | the whole answer: a `WorldOptions` and a `WorldDimensions`, and nothing else. It is a `SavedData` | built on the worker, read on the server thread |
| `WorldOptions` | the seed, *generate structures*, *bonus chest* — four fields, all immutable, each *with*-method returning a new one | — |
| `WorldDimensions` | a map from `LevelStem` key to `LevelStem`, each a dimension type plus a `ChunkGenerator`. Refuses to exist without an overworld | — |
| `WorldLoader` | the data-pack load every path shares, and the seam (`WorldLoader.WorldDataSupplier`) where the caller decides what the settings are | worker, with two hops to the main thread |
| `WorldCreationContext` | the settings *plus* the loaded registries and `ReloadableServerResources` they were parsed against — the screen's whole world | render thread, replaced wholesale |
| `WorldCreationUiState` | the widget-visible state, and the seven listeners that keep the tabs' widgets agreeing with it | render thread |
| `WorldOpenFlows` | every route from the world list into a running server, each one a chain of methods that can interpose a confirmation | render thread |
| `MinecraftServer` | takes the finished object out of the `WorldStem` and hands it to `SavedDataStorage`, which is what puts it on disk | server thread |

## Five stages, and only one of them is the screen

```mermaid
flowchart TB
    A["1 · load — WorldLoader.load opens the packs, fills the WORLDGEN registries, then the LEVEL_STEM registry"]
    A --> B["2 · decide — the WorldDataSupplier callback builds a WorldGenSettings from the registries just loaded"]
    B --> C["3 · finish the load — ReloadableServerResources reads recipes, loot and functions against the dimensions stage 2 chose"]
    C --> D["4 · edit — WorldCreationUiState mutates the object, and any data-pack change restarts at stage 1"]
    D --> E["5 · commit — bake the dimensions, write level.dat, spin MinecraftServer"]
```

The ordering that matters is stage 2 before stage 3. `WorldLoader.load` takes
the settings-building callback as a parameter and calls it **after** the
worldgen registries and the `Registries.LEVEL_STEM` registry are loaded and
**before** `ReloadableServerResources.loadResources` runs. The registry set
that recipes, loot tables and functions are then parsed against includes the
dimension registry that callback produced. So the seed and the dimension list
are settled before a single recipe is read, and they are settled by a lambda
the *caller* supplied — which is the only reason the client's create screen,
the client's world-opener, the dedicated server and the game-test server can
share one loader.

`RegistryDataLoader.DIMENSION_REGISTRIES` is a list of exactly one registry,
`Registries.LEVEL_STEM`, loaded in its own pass because its entries need every
worldgen registry already in hand. That single-entry list is the *dimension/*
folder of a data pack.

## The object, and what is not in it

`WorldGenSettings` has two fields. `WorldOptions` holds the seed, a
*generate structures* flag, a *bonus chest* flag and a string that only a very
old save carries. `WorldDimensions` holds the map of `LevelStem`s. There is no
world name in it, no difficulty, no game mode, no game rule and no data-pack
list — those are `LevelSettings` and `GameRules`, and
[level data and rules](../../reference/level-data-and-rules.md) says which file
each of them ends up in.

A seed is not a number the box gives you. `WorldOptions.parseSeed` trims the
text, returns nothing at all for an empty string, parses a long if it can, and
otherwise returns the Java string hash of what you typed — which is why a seed
of *glacier* is a seed and a seed of *99999999999999999999* is the hash of
that text rather than the number. And *nothing at all* is not zero:
`WorldOptions.withSeed` turns an absent seed into `WorldOptions.randomSeed`,
one draw from a fresh `RandomSource`. The seed field's responder calls
`WorldCreationUiState.setSeed` on every keystroke, so an empty box is
re-rolling a new random world every time you touch it.

> **For a 1.21-era reader.** The seed has left *level.dat*. `WorldGenSettings`
> extends `SavedData` and carries its own `SavedDataType`, so it is written to
> *data/world_gen_settings.dat* beside *raids.dat* — and the game rules to
> *data/game_rules.dat* — by the ordinary saved-data machinery rather than by
> the level-data writer. `PrimaryLevelData` keeps the old key name only as the
> constant `PrimaryLevelData.OLD_WORLD_GEN_SETTINGS`.

## Every widget is an edit to a live object

`WorldCreationUiState` is not a form. It holds the `WorldCreationContext`
itself, rebuilds it on almost every change, and then walks a listener list so
that each widget re-reads what it should now show. The state is also opinionated
about what it returns: `WorldCreationUiState.getDifficulty` reports *hard* in
hardcore whatever the button last set, `WorldCreationUiState.isAllowCommands`
reports true in a debug world and false in hardcore, and
`WorldCreationUiState.isBonusChest` reports false in both. The buttons are
disabled to match, but the state would lie to them anyway.

The world-type button is the destructive one. `WorldCreationUiState.setWorldType`
calls `WorldPreset.createWorldDimensions` and replaces **all** the dimensions
with the preset's, so a trip through *Superflat* and back to *Default* discards
every layer you edited. The button cycles the *normal* world-preset tag — five
presets in 26.2 — and holding Alt swaps it for the *extended* tag, which is the
same five plus *debug_all_block_states*. Seven world presets ship as JSON under
*data/minecraft/worldgen/world_preset/*; the seventh,
`WorldPresets.FLAT_ALL_DIMENSIONS`, is in neither tag and appears on no button:
the only thing that ever selects it is `CreateWorldScreen.testWorld`, behind a
*TW* button the title screen adds when `SharedConstants.IS_RUNNING_IN_IDE`.

*Customize* is rarer than it looks. `PresetEditor.EDITORS` is a two-entry map:
`WorldPresets.FLAT` opens `CreateFlatWorldScreen` and
`WorldPresets.SINGLE_BIOME_SURFACE` opens `CreateBuffetWorldScreen`. For the
other five presets the button is inactive. Both editors end the same way, in
`WorldCreationContext.DimensionsUpdater` lambdas that call
`WorldDimensions.replaceOverworldGenerator` — the overworld only. Nothing in
the create screen can edit the nether or the end.

## The layer editor edits the generator you already have

`FlatLevelGeneratorSettings` is the odd object in a part where everything else
is a record. Its layer list is mutable, its *lakes* and *features* flags are
set by void methods, and `FlatLevelGeneratorSettings.getLayersInfo` hands out
the live list. `PresetEditor` passes `CreateFlatWorldScreen` the settings of
the current overworld generator when that generator is already a
`FlatLevelSource` — the same object, not a copy — and the *Remove Layer* button
removes an entry from that list directly and calls
`FlatLevelGeneratorSettings.updateLayers`.

So **the *Cancel* button on the layer editor does not undo a layer deletion.**
Cancel only skips the `WorldCreationContext.DimensionsUpdater` that would build
a new `FlatLevelSource`; the list it would have been built from has already
changed. The *Presets* screen is the well-behaved half of the same screen:
`PresetFlatWorldScreen` reads and writes the layer stack as a text string and
hands back a *new* settings object through
`FlatLevelGeneratorSettings.withBiomeAndLayers`. Nine flat presets ship as
JSON, one for each key `FlatLevelGeneratorPresets` registers a value for; the
tenth key, `FlatLevelGeneratorPresets.TEST_WORLD`, is declared, never given a
value, and read by nothing in the game.

One thing the flat generator does not do is place all its own blocks.
`FlatLevelGeneratorSettings.adjustGenerationSettings` walks the built layer
stack and, for every layer whose block is not opaque, replaces it with a null
and re-adds it as an inline `Feature.FILL_LAYER` placed feature in the
*TOP_LAYER_MODIFICATION* decoration step. The water in *Water World* arrives as
[a feature](features-and-placement.md), not as terrain.

## An experiment is a data pack, so switching one on reloads everything

`ExperimentsScreen` looks like a toggle list and is a filtered pack browser: it
walks the repository's available packs and keeps only those whose
`Pack.getPackSource` is `PackSource.FEATURE`. Three ship in 26.2 —
*minecart_improvements*, *redstone_experiments* and *trade_rebalance* — one per
non-vanilla flag in `FeatureFlags`. Pressing *Done* rewrites the repository's
selection and lands in `CreateWorldScreen` exactly where the data-pack screen
lands, in `CreateWorldScreen.tryApplyNewDataPacks`.

That method has a fast path and a slow one. If the enabled-pack list and the
feature set both come back unchanged, `WorldCreationUiState.tryUpdateDataConfiguration`
swaps the configuration in and nothing reloads. Otherwise
`CreateWorldScreen.applyNewPackConfig` puts a *validating* message on screen and
runs `WorldLoader.load` again from the top — and it has to carry your settings
across a registry set that is about to be replaced. It does that by
**serialising them**: `WorldGenSettings.CODEC` encodes the current options and
dimensions to JSON using the old registries as context, and re-parses that JSON
against the new ones. Every `Holder` in the object — every biome, every noise
settings, every structure set the flat generator overrides — is written out as
an id and looked up again. If the new packs have no world preset or no biome,
or the re-parse fails, the future completes exceptionally and the player gets a
retry-or-reset confirmation instead of a screen.

The two routes into that method differ in one boolean.
`CreateWorldScreen.tryApplyNewDataPacks` shows
`ConfirmExperimentalFeaturesScreen` only when the requested flags are
experimental **and** the caller was the data-pack screen. Toggling an experiment
in the Experiments screen skips it — that screen carries a red warning line of
its own instead.

Data packs added here do not go into a world folder that does not exist yet.
`CreateWorldScreen.getOrCreateTempDataPackDir` makes a temporary directory
prefixed *mcworld-*, the pack browser is pointed at that, and the directory is
copied into the new world's *datapacks* folder by
`CreateWorldScreen.createNewWorldDirectory` at the very end — or deleted, on
every other exit from the screen.

## What *Create* does

```mermaid
sequenceDiagram
    autonumber
    participant CWS as CreateWorldScreen
    participant WCUS as WorldCreationUiState
    participant WOF as WorldOpenFlows
    participant MC as Minecraft
    participant MS as MinecraftServer
    participant Disk as Disk
    Note over CWS,Disk: render thread
    CWS->>WCUS: read the context one last time
    WCUS-->>CWS: WorldOptions and the selected WorldDimensions
    CWS->>CWS: WorldDimensions.bake into a frozen LEVEL_STEM registry, take its lifecycle
    CWS->>WOF: confirmWorldCreation with that lifecycle
    WOF-->>CWS: proceed, or an experimental or deprecated warning first
    CWS->>Disk: create the world directory, copy the temp datapacks in
    CWS->>WOF: createLevelFromExistingSettings with the WorldStem parts
    WOF->>MC: doWorldLoad
    MC->>Disk: saveDataTag writes level.dat through a temp file
    Note over MC,MS: MinecraftServer.spin builds the server on the render thread, then starts the Server thread
    MC->>MS: new IntegratedServer with the WorldStem and the screen's GameRules
    MS->>MS: savedDataStorage.set marks WorldGenSettings dirty
    Note over MS,Disk: server thread, first save
    MS->>Disk: data/world_gen_settings.dat and data/game_rules.dat
```

Three details in that order are worth stopping on. `CreateWorldScreen.onCreate`
bakes the dimensions to decide the *lifecycle* and the
`PrimaryLevelData.SpecialWorldProperty`, but the `WorldGenSettings` it stores
holds the **unbaked** selection — the bake is what runs, the selection is what
is saved. The warning is skipped when the world is not a re-create and the baked
registries are stable, and `WorldDimensions.checkStability` only asks whether
each of the three built-in keys carries the vanilla dimension type and biome
source; every shipped preset passes, so the experimental warning at this point
comes from data packs, not from the world type. And *level.dat* is written by
the client, in `Minecraft.doWorldLoad`, **before the server thread exists** —
while the settings file is written by the server after it starts, because
`MinecraftServer`'s constructor is the first thing to hand the object to
`SavedDataStorage`.

The game rules take a third path again. `CreateWorldScreen.onCreate` copies the
screen's `GameRules` into an `Optional` that travels through
`CreateWorldCallback`, `WorldOpenFlows.createLevelFromExistingSettings` and
`Minecraft.doWorldLoad` to the `MinecraftServer` constructor, which builds a
fresh rule set from the saved-data default and then overlays the screen's
values on top.

## The same object, from a properties file

The dedicated server never sees a screen, and the comparison is the clearest
way to see which parts of this page are the subject and which are its interface.

| | client create screen | dedicated server | *Re-Create* |
|---|---|---|---|
| who builds it | `CreateWorldScreen.onCreate` | `Main.createNewWorldData` | `WorldOpenFlows.recreateWorldData` |
| the seed | the seed box, per keystroke | *level-seed*, once, in the `DedicatedServerProperties` constructor | copied from the old world's settings |
| the dimensions | a `WorldPreset` plus screen edits | *level-type* as a world-preset id, with *default* and *largebiomes* as legacy aliases | the old world's saved `LevelStem` map |
| customising | `PresetEditor`, overworld only | *generator-settings* JSON, parsed by `FlatLevelGeneratorSettings.CODEC` **and only when the preset is** `WorldPresets.FLAT` | the create screen again |
| game rules | `WorldCreationGameRulesScreen` | nothing — *server.properties* has no rules | read back from *game_rules.dat* |
| when | only if the folder is new | only if there is no *level.dat* | always a new folder |

Both seed paths are the same method. `DedicatedServerProperties` calls
`WorldOptions.parseSeed` on *level-seed* and falls back to
`WorldOptions.randomSeed`, exactly as the seed box does — so an empty
*level-seed* draws its random seed the moment the properties file is parsed,
whether or not a world is about to be created. An unrecognised *level-type* is
a warning in the log and the *normal* preset, not a failure.

*Re-Create* is the interesting column. `WorldOpenFlows.recreateWorldData` reads
the old world with a deliberately **empty** `LevelStem` registry, so the
dimensions come from the saved settings rather than from any pack, then hands
`CreateWorldScreen.createFromExisting` a `LevelSettings` and a context. The
result is a new world folder with the old seed pre-filled. Nothing in the
family edits an existing world's `WorldGenSettings` in place: `EditWorldScreen`
offers a rename, an icon reset, a folder button, a backup and *Optimize World*,
and not one generation setting.

## The rest of the family

`client/gui/screens/worldselection` holds nineteen classes, nine of them
screens. `SelectWorldScreen` is a search box, a `WorldSelectionList` and six
footer buttons; the list's rows are `LevelSummary` objects read by
`LevelStorageSource.readLightweightData`, an NBT parse that deliberately skips
the *Data/Player* and *Data/WorldGenSettings* subtrees so that listing a
hundred worlds never costs a settings parse. `WorldOpenFlows.openWorld` is a
chain of eight methods — itself, then level data, version compatibility, the
world stem, stem compatibility, a bundled resource pack, disk space, and
finally `Minecraft.doWorldLoad` — each of which can stop and put a
confirmation screen in the way. `OptimizeWorldScreen` and `FileFixerProgressScreen` are the
progress bars over save migration, which
[this book does not cover](../anatomy/what-this-book-skips.md).

## Where to look

Start with `net/minecraft/world/level/levelgen`: `WorldGenSettings` is fifty-one
lines and tells you the whole shape, `WorldOptions` and `WorldDimensions` are
the two halves, and `WorldDimensions.bake` is the method that turns a selection
into a registry. Then `net/minecraft/server/WorldLoader` — one method, and the
spine every path shares. Only then
`net/minecraft/client/gui/screens/worldselection`, in the order
`WorldCreationContext`, `WorldCreationUiState`, `CreateWorldScreen` and
`WorldOpenFlows`, with `net/minecraft/client/gui/screens/CreateFlatWorldScreen`
and `net/minecraft/world/level/levelgen/flat` beside them. The comparison is
`DedicatedServerProperties.createDimensions` and `Main.createNewWorldData`, and
the destination is the first forty lines of the `MinecraftServer` constructor.

---

*Rules: names, never code · how the system works, not how the code reads ·
newest version only · every backticked name passes `tools/verify_names.py`.*
