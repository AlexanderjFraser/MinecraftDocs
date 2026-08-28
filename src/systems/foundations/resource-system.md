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
  subdirectories, which `Pack.open` assembles. `pack.mcmeta` is read as
  `ResourceMetadata` sections — `PackMetadataSection` (description and a
  `PackFormat` range), `FeatureFlagsMetadataSection`, `OverlayMetadataSection`,
  `ResourceFilterSection`.
- **The repository** (`server/packs/repository`). `PackRepository` owns
  the `RepositorySource`s (where packs are discovered), the *available*
  `Pack`s and the *selected* list, in order. `PackRepository.reload`
  rediscovers; `PackRepository.openAllSelected` opens the selected packs into
  `PackResources`. A `Pack` is a discoverable pack with its `Pack.Metadata`
  (description, `PackCompatibility`, requested feature flags, overlays) and
  a `PackSelectionConfig` (required, default position, fixed). Sources:
  `ClientPackSource` and `ServerPacksSource` (the built-ins, both extending
  `BuiltInPackSource`), `FolderRepositorySource` (a directory of user
  packs), `DownloadedPackSource` (server-sent packs, client only).
- **The manager** (`server/packs/resources`). `MultiPackResourceManager`
  is a **snapshot**: constructed from a list of `PackResources`, it builds
  one `FallbackResourceManager` per namespace, each a stack of
  `FallbackResourceManager.PackEntry`s searched top-down. A `Resource` is
  what you get back: its source pack, an `IoSupplier` for the bytes, and a
  lazily-read `ResourceMetadata` found beside it (`.mcmeta`, searched in the
  same pack or one above, never below). `ReloadableResourceManager` is the
  long-lived client façade that holds the current snapshot and the
  `PreparableReloadListener` list; the server has no façade — each reload
  is a fresh `MultiPackResourceManager` inside `MinecraftServer.ReloadableResources`.
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
all the reading is done — the old state stays live throughout.

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
  first, synchronously, on the calling thread; `ProfiledReloadInstance`
  is chosen only when the logger is at debug level.

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
    MC->>PR: reload → openAllSelected — rediscover, then open the selected packs
    MC->>RRM: createReload(backgroundExecutor, Minecraft, packs) — close the old MultiPackResourceManager, build the new snapshot
    RRM->>SRI: create(listeners, …) — prepareSharedState on every listener, then reload on each
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
   from `Minecraft.runTick`; reloads never overlap.
2. **Rediscover, then open.** `PackRepository.reload` re-runs every
   `RepositorySource` and rebuilds the selection: prior choices are kept,
   packs whose `Pack.isRequired` is true are force-inserted at their default
   position (the vanilla *resource* pack is required; the vanilla *data* pack
   is not). `Options.loadSelectedResourcePacks` is what decides the client
   order from `options.txt`, dropping ids that no longer exist or are
   incompatible.
3. **A snapshot, not a view.** `ReloadableResourceManager.createReload`
   closes the previous `MultiPackResourceManager` and builds a new one; every
   `Resource` handed out during this reload comes from that snapshot, so a
   pack edited on disk mid-reload cannot produce a torn read.
4. **Prepare everywhere, apply in order.** `SimpleReloadInstance` wraps both
   executors in counters (that is where the progress bar's numbers come
   from), calls each listener's `PreparableReloadListener.reload`, and hands each a barrier chained to
   the previous listener's completion. The client registers, in order:
   `LanguageManager`, `TextureManager`, `ShaderManager`, `SoundManager`,
   `AtlasManager`, `FontManager`, the grass/foliage colour listeners,
   `ModelManager`, `EquipmentAssetManager`, `EntityRenderDispatcher`,
   `BlockEntityRenderDispatcher`, `ParticleResources`, `LevelExtractor`, the
   cloud renderer, `GpuWarnlistManager`, then the HUD's (`SplashManager`,
   `WaypointStyleManager`). Order matters only for apply; `ModelManager`
   applies after `AtlasManager` because baked models need the atlas.
5. **The overlay is a poll.** `LoadingOverlay` draws the logo from the
   vanilla pack *outside* the reload (via `VanillaPackResources.asProvider`)
   and a bar smoothed from `ReloadInstance.getActualProgress`. On
   `ReloadInstance.isDone` it calls `ReloadInstance.checkExceptions`; a
   failure runs `Minecraft.rollbackResourcePacks` (deselect the offending
   packs and reload again) — `ShaderManager` is constructed with
   `Minecraft.triggerResourcePackRecovery` for exactly this. Success runs
   `LevelExtractor.allChanged`, which is why every chunk section rebuilds
   after F3+T.

## The trace: `/reload`

`ReloadCommand` → `MinecraftServer.reloadResources`, and the shape differs
in three ways from the client's. It reports success **before** the reload
runs (errors arrive later, asynchronously). It opens a fresh
`MultiPackResourceManager` rather than swapping one inside a façade. And the
listener list is only three — `RecipeManager`, `ServerFunctionLibrary`,
`ServerAdvancementManager` (`ReloadableServerResources.listeners`) —
because everything else that used to be a listener is now a registry:
tags are read *before* the reload instance by `TagLoader.loadTagsForExistingRegistries`
and applied after it (page [tags](tags.md)); loot tables, predicates and
item modifiers load as the `RegistryLayer.RELOADABLE` registry layer in
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
— and finally `ServerFunctionManager.replaceLibrary`. A new `Commands`
tree is built each time, so `/reload` can change the command set.

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
  by `ServerResourcePackConfigurationTask` in configuration or at any time
  in play; `ServerboundResourcePackPacket` with a
  `ServerboundResourcePackPacket.Action` back. Packs are keyed by UUID and
  stack. `ServerCommonPacketListenerImpl.handleResourcePackResponse`
  disconnects a client that declines a required pack.
- **Data-driven by:** `pack.mcmeta` (`PackMetadataSection`; formats are
  `PackFormat` major/minor, with min_format/max_format replacing the
  integer pack_format), `options.txt` (`Options.resourcePacks`),
  `level.dat`'s `WorldDataConfiguration` (`DataPackConfig` enabled/disabled
  plus the `FeatureFlagSet`), `server.properties` for the server-sent pack,
  `allowed_symlinks.txt` via `DirectoryValidator`.

## Invariants and surprises

- **Prepare never touches live state; apply never touches a file.** The
  barrier is the whole contract. A listener that reads from the manager in
  `SimplePreparableReloadListener.apply` is reading the *new* snapshot (fine); one that mutates live state
  in `SimplePreparableReloadListener.prepare` is racing the Render thread (a bug).
- **The old world stays up until the last apply.** Nothing is torn down
  when a reload starts; the client keeps rendering with the old atlases
  while the new ones bake, and a failed reload rolls back by reloading
  again, not by restoring.
- **Higher pack wins per file, and metadata follows the file.**
  `FallbackResourceManager` walks its stack from the top; a `.mcmeta` is
  looked for in the winning pack or those above it, never in a pack below —
  so a pack overriding a texture without its `.mcmeta` loses the animation.
  `ResourceFilterSection` lets a pack *hide* lower packs' files by pattern
  without providing replacements.
- **Feature flags are packs.** A feature pack is a built-in pack with a
  `FeatureFlagsMetadataSection`; `MinecraftServer.configurePackRepository`
  auto-selects packs whose requested flags are a subset of the allowed set,
  and the union of selected packs' flags becomes the world's
  `FeatureFlagSet`. Turning on an experiment is enabling a data pack.
- **Overlays are versioned sub-packs.** `OverlayMetadataSection` maps a
  `PackFormat` range to an an overlays subdirectory that `CompositePackResources`
  layers on top of the pack itself, so one zip can carry variants for
  several game versions.
- **The client's vanilla pack cannot be deselected; the server's can.**
  `ClientPackSource` marks vanilla required and bottom; `ServerPacksSource`
  marks it bottom but optional. `PackRepository.rebuildSelected` re-inserts
  required packs even when `options.txt` dropped them.
- **Resource reloads are debug-timed only.** The "Resource reload finished
  after N ms" line and per-listener timings come from
  `ProfiledReloadInstance`, selected only when the logger is at debug.

## Where to look

`PackType` · `PackResources` · `Pack` · `PackRepository` ·
`ServerPacksSource` · `ClientPackSource` · `FolderRepositorySource` ·
`MultiPackResourceManager` · `FallbackResourceManager` ·
`ReloadableResourceManager` · `PreparableReloadListener` ·
`SimplePreparableReloadListener` · `SimpleJsonResourceReloadListener` ·
`SimpleReloadInstance` · `Minecraft.reloadResourcePacks` ·
`LoadingOverlay` · `ReloadCommand` · `MinecraftServer.reloadResources` ·
`ReloadableServerResources` · `WorldLoader` · `DownloadedPackSource`

---

*Rules: names, never code · how the system works, not how the code reads ·
newest version only · every backticked name passes `tools/verify_names.py`.*
