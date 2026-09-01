# The resource system

> Verified against **Minecraft 26.2** · Part II · F3+T on the client and `/reload` on the server: how a stack of packs becomes a snapshot, and how every manager rebuilds from it without stalling the thread that owns it.

## Responsibility

Everything the game reads from a file — textures, models, sounds, language
strings, recipes, advancements, loot tables, tags, worldgen JSON — comes
through one system: a **stack of packs** merged into a **resource manager**,
and a list of **reload listeners** that each rebuild their world from it.
The client's stack is resource packs (`PackType.CLIENT_RESOURCES`, the
*assets* tree); the server's is data packs (`PackType.SERVER_DATA`, the
*data* tree). Same classes, two instances, two directories.

The one sentence a player recognises: *F3+T reloads resource packs;
`/reload` reloads data packs; both show the same "which pack wins" rule.*

## The data it owns

Three layers, bottom up.

- **Packs** (`server/packs`). `PackResources` is the raw file source:
  `PackResources.getResource`, `PackResources.listResources`,
  `PackResources.getNamespaces`, and its `PackLocationInfo` (id, title,
  `PackSource`, optional `KnownPack`). `VanillaPackResources` is the jar's own
  assets and data; `FilePackResources` a zip; `PathPackResources` a
  directory; `CompositePackResources` a pack plus its *overlays*
  subdirectories, which the `Pack.ResourcesSupplier` assembles for zip and
  folder packs (built-ins never produce one). `pack.mcmeta` is read as
  `ResourceMetadata` sections — `PackMetadataSection` (description and a
  `PackFormat` range), `FeatureFlagsMetadataSection`, `OverlayMetadataSection`,
  `ResourceFilterSection`. Discovery is guarded: `DirectoryValidator`,
  `ForbiddenSymlinkInfo` and `PackDetector` decide what a folder is allowed
  to be, and `packs/linkfs` is the exploded-pack filesystem used in
  development.
- **The repository** (`server/packs/repository`). `PackRepository` owns
  the `RepositorySource`s (where packs are discovered), the *available*
  `Pack`s and the *selected* list, in order. `PackRepository.reload`
  rediscovers; `PackRepository.openAllSelected` opens the selected packs into
  `PackResources`. A `Pack` is a discoverable pack with its `Pack.Metadata`
  (description, `PackCompatibility`, requested feature flags, overlays) and
  a `PackSelectionConfig` (required, default `Pack.Position`, fixed), with
  `Pack.Position` owning the insertion algorithm that makes a fixed pack
  stick. Sources: `ClientPackSource` and `ServerPacksSource` (the built-ins,
  both extending `BuiltInPackSource`, which also lists the packs bundled
  *inside* the vanilla pack — the art packs, the accessibility packs, the
  test pack and every feature pack), `FolderRepositorySource` (a directory of
  user packs), `DownloadedPackSource` (server-sent packs, client only).
- **The manager** (`server/packs/resources`). `MultiPackResourceManager`
  is a **snapshot of the pack list** — not of the bytes. Constructed from a
  list of `PackResources`, it builds one `FallbackResourceManager` per
  namespace, each a stack searched from the **last** selected pack down. A
  `Resource` is what you get back: its source pack, an `IoSupplier` for the
  bytes — opened lazily, at read time — and a lazily-read `ResourceMetadata`
  found beside it (`.mcmeta`, searched in the winning pack or one above it,
  never below). `ReloadableResourceManager` is the long-lived client façade
  that holds the current snapshot and the `PreparableReloadListener` list;
  the server has no façade — each reload is a fresh `MultiPackResourceManager`
  inside `MinecraftServer.ReloadableResources`. `ResourceManager.Empty` is
  the do-nothing manager handed to code that must run without packs.
- **Listeners.** `PreparableReloadListener.reload` takes a
  `PreparableReloadListener.SharedState` (which carries the
  `ResourceManager`), a background executor, a
  `PreparableReloadListener.PreparationBarrier` and a main-thread executor.
  `SimplePreparableReloadListener` splits that into
  `SimplePreparableReloadListener.prepare` (background) and
  `SimplePreparableReloadListener.apply` (main thread);
  `SimpleJsonResourceReloadListener` is the "every JSON file in a directory
  through one codec" specialisation, using `FileToIdConverter` to map
  `data/ns/recipe/foo.json` to `ns:foo`; `ResourceManagerReloadListener` is
  the apply-only shape.

## When it runs

The reload is a **prepare/apply pipeline** scheduled by
`SimpleReloadInstance`. Every listener's prepare runs concurrently on the
worker pool; listener N's apply runs on the owning thread only after
*every* listener has finished preparing *and* listener N−1 has finished
entirely. So registration order is apply order, and no apply starts until
all the reading is done — each listener's own live state stays usable
throughout.

- **Client:** `ReloadableResourceManager.createReload` is called with
  `Util.backgroundExecutor` (named "resourceLoad") and `Minecraft` itself as
  the main-thread executor — apply runs on the Render thread, interleaved
  with frames, while `LoadingOverlay.tick` polls `ReloadInstance.isDone`.
- **Server:** `ReloadableServerResources.loadResources` is called with
  `Util.backgroundExecutor` and `MinecraftServer` — apply runs on the Server
  thread. If `/reload` is issued *from* the server thread the method blocks
  it with `BlockableEventLoop.managedBlock` until done: `/reload` stalls the
  tick.
- `PreparableReloadListener.prepareSharedState` for every listener runs
  first, synchronously, on whatever thread started the reload — the Render
  thread on the client, but a worker on the server, because the server's
  reload instance is created from inside an already-async chain.
  `ProfiledReloadInstance` is chosen only when the logger is at debug level.

### The shared-state channel

`PreparableReloadListener.prepareSharedState` is a separate first pass for a reason: it is the one
place a listener can publish something for *another* listener's prepare to
consume, keyed by a `PreparableReloadListener.StateKey`. The game declares
exactly one — `AtlasManager.PENDING_STITCH`. `ModelManager` and
`ParticleResources` pull the pending sprite futures out of it and join them
**inside their own prepare**, so model baking overlaps atlas stitching
rather than queueing behind it. This is why the model/atlas dependency is
*not* an apply-order dependency, and why reasoning about it from the
registration list gets the wrong answer.

## The trace: F3+T

```mermaid
sequenceDiagram
    participant KH as KeyboardHandler (Render thread)
    participant MC as Minecraft
    participant PR as PackRepository
    participant RRM as ReloadableResourceManager
    participant SRI as SimpleReloadInstance
    participant L as each PreparableReloadListener
    participant W as Worker-Main-n
    participant LO as LoadingOverlay

    KH->>MC: handleDebugKeys → reloadResourcePacks
    MC->>PR: reload → openAllSelected — rediscover, keep the current selection, then open it
    MC->>RRM: createReload(backgroundExecutor, Minecraft, packs) — close the old MultiPackResourceManager, build the new snapshot
    RRM->>SRI: create(listeners, …) — prepareSharedState on every listener first, then reload on each
    L->>W: prepare — read files, decode JSON, build textures off-thread
    W-->>L: PreparationBarrier.wait — resolved on the Render thread once all prepares are done and the previous listener has applied
    L->>MC: apply — swap the manager's live state (atlases, models, sounds, fonts)
    MC->>LO: setOverlay(LoadingOverlay) — logo and progress bar from ReloadInstance.getActualProgress
    LO->>MC: tick → isDone → checkExceptions → onFinish — success: levelExtractor.allChanged; failure: rollbackResourcePacks
```

Narrated:

1. **The key does nothing but ask.** `KeyboardHandler.handleDebugKeys`
   matches `Options.keyDebugReloadResourcePacks` and calls
   `Minecraft.reloadResourcePacks`. If a reload is already showing an
   overlay, the request is parked in `Minecraft.pendingReload` and drained
   from `Minecraft.runTick`, and a second request while one is parked simply
   returns the same future. The one path that bypasses the guard is a
   *recovery* reload after a failure.
2. **Rediscover, then open.** `PackRepository.reload` re-runs every
   `RepositorySource` and rebuilds the selection: prior choices are kept and
   packs whose `Pack.isRequired` is true are force-inserted at their default
   position (the vanilla *resource* pack is required; the vanilla *data* pack
   is not). Reading the order out of `options.txt` is a *startup* step —
   `Options.loadSelectedResourcePacks` runs once in the `Minecraft`
   constructor, not on every F3+T.
3. **A snapshot of the list, not of the bytes.**
   `ReloadableResourceManager.createReload` immediately closes the previous
   `MultiPackResourceManager` — with every file handle it held — and builds a
   new one. What is frozen is *which packs are in the stack*; a `Resource`
   still opens its file when it is read, so a pack edited on disk mid-reload
   is absolutely observable.
4. **Prepare everywhere, apply in order.** `SimpleReloadInstance` wraps both
   executors in counters (that is where the progress bar's numbers come
   from — prepare and apply tasks weigh double, listeners-completed single,
   smoothed by the overlay), calls each listener's
   `PreparableReloadListener.reload`, and hands each a barrier chained to the
   previous listener's completion. It sequences fail-fast: the first listener
   to throw aborts the whole reload rather than letting the rest finish. The
   client registers, in order: `LanguageManager`, `TextureManager`,
   `ShaderManager`, `SoundManager`, `AtlasManager`, `FontManager`, the three
   colour listeners (`GrassColorReloadListener`, `FoliageColorReloadListener`,
   `DryFoliageColorReloadListener`), `ModelManager`, `EquipmentAssetManager`,
   `EntityRenderDispatcher`, `BlockEntityRenderDispatcher`,
   `ParticleResources`, `LevelExtractor`, the cloud renderer,
   `GpuWarnlistManager`, a `PeriodicNotificationManager`, then `SplashManager`
   from `Gui` and `WaypointStyleManager` from `Hud`.
5. **The overlay is a poll.** `LoadingOverlay` draws the logo from the
   vanilla pack *outside* the reload (via `VanillaPackResources.asProvider`)
   and a smoothed bar from `ReloadInstance.getActualProgress`. On
   `ReloadInstance.isDone` it calls `ReloadInstance.checkExceptions`; a
   failure runs `Minecraft.rollbackResourcePacks`, which does **not** find
   the offending pack — it deselects *every* resource pack, clears the
   options lists, saves, and reloads again, and if vanilla was the only
   selected pack it rethrows and crashes instead. `ShaderManager` is
   constructed with `Minecraft.triggerResourcePackRecovery` for exactly this.
   Success runs `LevelExtractor.allChanged`, which is why every chunk section
   rebuilds after F3+T. Throughout, `ResourceLoadStateTracker` records what
   kind of reload this was and with which packs, so a crash report can say.

## The trace: `/reload`

`ReloadCommand` → `MinecraftServer.reloadResources`, and the shape differs
in several ways from the client's. It **discovers new packs first** —
`ReloadCommand.discoverNewPacks` selects every available pack not in the
world's disabled list, which is how a datapack dropped into the folder is
picked up. It reports success **before** the reload runs (errors arrive
later, asynchronously). The packs are opened on the *server thread* before
any background work starts. It opens a fresh `MultiPackResourceManager`
rather than swapping one inside a façade. And the listener list is only
three — `RecipeManager`, `ServerFunctionLibrary`, `ServerAdvancementManager`
(`ReloadableServerResources.listeners`) — because everything else that used
to be a listener is now a registry: tags are read *before* the reload
instance by `TagLoader.loadTagsForExistingRegistries` and applied after it
(page [tags](tags.md)); loot tables, predicates and item modifiers load as
the `RegistryLayer.RELOADABLE` registry layer in
`ReloadableServerRegistries.reload` (page [identifiers-and-registries](identifiers-and-registries.md));
item component prototypes rebind through `BuiltInRegistries.DATA_COMPONENT_INITIALIZERS`
(page [data-components](data-components.md)). When the future completes on
the server thread: close the old `MinecraftServer.ReloadableResources`,
install the new, `PackRepository.setSelected`, write the new
`WorldDataConfiguration` into level data,
`ReloadableServerResources.updateComponentsAndStaticRegistryTags`,
`RecipeManager.finalizeRecipeLoading`, `PlayerList.saveAll`, then
`PlayerList.reloadResources` — which re-reads every player's advancements
and broadcasts `ClientboundUpdateTagsPacket` and `ClientboundUpdateRecipesPacket`
— then `ServerFunctionManager.replaceLibrary`,
`StructureTemplateManager.onResourceManagerReload`, and finally a rebuilt
fuel table.

## Interfaces

- **Called by:** `Minecraft` (constructor and `Minecraft.reloadResourcePacks`),
  `MinecraftServer.reloadResources`, `WorldLoader.load` (world open —
  `WorldLoader.PackConfig.createResourceManager` runs
  `MinecraftServer.configurePackRepository` and builds the first snapshot),
  `DownloadedPackSource` (a server-sent pack is just one more
  `RepositorySource`, and it triggers an ordinary `Minecraft.reloadResourcePacks`).
- **Calls into:** every manager that registered itself; `TagLoader`,
  `RegistryDataLoader`, `ReloadableServerRegistries` on the server side of
  world load.
- **Crosses the network as:** `ClientboundResourcePackPushPacket` (id,
  URL, hash, required, prompt) and `ClientboundResourcePackPopPacket`, sent
  by `ServerResourcePackConfigurationTask` in the configuration phase and by
  `ServerPackCommand` (`/resourcepack push|pop`) at any time in play; with a
  `ServerboundResourcePackPacket` and its
  `ServerboundResourcePackPacket.Action` back. Packs are keyed by UUID and
  stack, and a server-sent pack pins itself to the top of the selection.
  `ServerCommonPacketListenerImpl.handleResourcePackResponse` disconnects a
  client that declines — but the "required" it consults is
  `MinecraftServer.isResourcePackRequired`, a **server-wide**
  server.properties setting, not the flag on the individual pack, so a
  declined `/resourcepack push` can disconnect you on a server whose
  properties pack is required.
- **Data-driven by:** `pack.mcmeta` (`PackMetadataSection`; formats are
  `PackFormat` major/minor, with min_format/max_format replacing the
  integer pack_format), `options.txt` (`Options.resourcePacks`),
  `level.dat`'s `WorldDataConfiguration` (`DataPackConfig` enabled/disabled
  plus the `FeatureFlagSet`), `server.properties` for the server-sent pack,
  `allowed_symlinks.txt` via `DirectoryValidator`.

## Invariants and surprises

- **Prepare never touches live state.** That is the whole contract, and it
  is one-directional: a listener that reads from the manager in
  `SimplePreparableReloadListener.apply` is reading the *new* snapshot and
  that is fine (`TextureManager` does exactly this), while one that mutates
  live state in `SimplePreparableReloadListener.prepare` is racing the
  Render thread.
- **The old world stays up until the last apply — but the old files do
  not.** Nothing a listener owns is torn down when a reload starts; the
  client keeps rendering with the old atlases while the new ones bake. The
  previous `MultiPackResourceManager` and its open handles, however, are
  closed at the very start.
- **The *last* pack in the selected list wins.** `FallbackResourceManager`
  searches its stack from the end backwards, and `Pack.Position.BOTTOM`
  inserts at index 0 — which is why vanilla is BOTTOM and why "higher in the
  UI" means "later in the list". A `.mcmeta` is looked for in the winning
  pack or those above it, never in one below, so a pack overriding a texture
  without its `.mcmeta` loses the animation. `ResourceFilterSection` lets a
  pack *hide* lower packs' files by pattern without providing replacements.
- **Some loaders want every copy, not the winner.**
  `ResourceManager.getResourceStack` and `ResourceManager.listResourceStacks`
  return all packs' copies **bottom-first**, which is how languages, tags and
  atlas sources merge instead of overriding.
- **Feature flags are packs, but not auto-selected ones.** A feature pack is
  a built-in pack carrying a `FeatureFlagsMetadataSection`, and its
  `PackSource` deliberately reports that it must *not* be added
  automatically. `MinecraftServer.enableForcedFeaturePacks` force-selects the
  ones matching the world's forced features, and the world's flag set is the
  selected packs' requested flags joined with those forced ones. Turning on
  an experiment is enabling a data pack — through a different door than
  ordinary packs use.
- **Compatibility is a range, not a number.** `PackMetadataSection` carries
  an inclusive range of `PackFormat` major/minor pairs and
  `PackCompatibility` reports too old, too new, unknown or compatible against
  the game's own — resource **88.0** and data **107.1** in 26.2. Above
  `PackFormat.lastPreMinorVersion` (64 for assets, 81 for data) the
  min_format/max_format fields are mandatory and the old integer
  pack_format is not enough. A `pack.mcmeta` the strict codec rejects gets
  one more chance through a description-only fallback so the pack can at
  least be listed as incompatible.
- **Overlays are versioned sub-packs.** `OverlayMetadataSection` maps a
  `PackFormat` range to an overlays subdirectory that `CompositePackResources`
  layers on top of the pack itself, so one zip can carry variants for
  several game versions.
- **The client's vanilla pack cannot be deselected; the server's can.**
  `ClientPackSource` marks vanilla required and bottom; `ServerPacksSource`
  marks it bottom but optional.
- **`/reload` changes the command tree only for future connections.** A new
  `Commands` is built each time, but nothing re-sends it, so connected
  clients complete against the tree they were given until they reconnect.
- **Resource reloads are debug-timed only.** The "Resource reload finished
  after N ms" line, the per-listener timings and the total-blocking-time
  figure all come from `ProfiledReloadInstance`, selected only when the
  logger is at debug.

## Where to look

`PackType` · `PackResources` · `Pack` · `PackRepository` · `PackCompatibility` ·
`PackFormat` · `ServerPacksSource` · `ClientPackSource` · `BuiltInPackSource` ·
`FolderRepositorySource` · `MultiPackResourceManager` ·
`FallbackResourceManager` · `ReloadableResourceManager` ·
`PreparableReloadListener` · `SimplePreparableReloadListener` ·
`SimpleJsonResourceReloadListener` · `SimpleReloadInstance` ·
`ResourceLoadStateTracker` · `Minecraft.reloadResourcePacks` ·
`LoadingOverlay` · `ReloadCommand` · `MinecraftServer.reloadResources` ·
`ReloadableServerResources` · `WorldLoader` · `DownloadedPackSource` ·
`ServerPackManager`

---

*Rules: names, never code · how the system works, not how the code reads ·
newest version only · every backticked name passes `tools/verify_names.py`.*
