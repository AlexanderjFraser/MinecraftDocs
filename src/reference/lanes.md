# Diagram lanes

Every lane in a sequence diagram is a class name abbreviated once for the whole
corpus. This is the key, generated from `TEMPLATE.md` by
`python tools/check_lanes.py --index`; the initials of the class's CamelCase words,
a one-word class as itself, and a few words for things that are not classes.

| lane | class |
|---|---|
| `ACM` | `AbstractContainerMenu` |
| `AP` | `AcquirePoi` |
| `ATS` | `AttributeTrackSampler` |
| `BEL` | `BlockableEventLoop` |
| `BI` | `BucketItem` |
| `BIR` | `BuiltInRegistries` |
| `BLE` | `BlockLightEngine` |
| `Boot` | `Bootstrap` |
| `Brain` | `Brain` |
| `Camera` | `Camera` |
| `CBE` | `ChestBlockEntity` |
| `CCPL` | `ClientConfigurationPacketListenerImpl` |
| `CGT` | `ChunkGenerationTask` |
| `CH` | `ChunkHolder` |
| `CHelp` | `ContainerHelper` |
| `CHPL` | `ClientHandshakePacketListenerImpl` |
| `CL` | `ClientLevel` |
| `CM` | `ChunkMap` |
| `Comp` | `Component` |
| `Conn` | `Connection` |
| `CPL` | `ClientPacketListener` |
| `CS` | `ComponentSerialization` |
| `CT` | `CombatTracker` |
| `CTD` | `ChunkTaskDispatcher` |
| `CU` | `ComponentUtils` |
| `DCP` | `DataComponentPatch` |
| `DL` | `DirectoryLock` |
| `DM` | `DistanceManager` |
| `DMR` | `DefaultedMappedRegistry` |
| `DS` | `DedicatedServer` |
| `DScr` | `DeathScreen` |
| `EAP` | `EnvironmentAttributeProbe` |
| `EAS` | `EnvironmentAttributeSystem` |
| `EH` | `EnchantmentHelper` |
| `EM` | `EnchantmentMenu` |
| `Entity` | `Entity` |
| `ETL` | `EntityTickList` |
| `EVS` | `EnvironmentAttributeSystem.ValueSampler` |
| `FF` | `FlowingFluid` |
| `Font` | `Font` |
| `GED` | `GameEventDispatcher` |
| `GR` | `GameRenderer` |
| `GS` | `GaussianSampler` |
| `Gui` | `Gui` |
| `HS` | `HashedStack` |
| `Hud` | `Hud` |
| `IOW` | `IOWorker` |
| `IP` | `ItemParser` |
| `IS` | `IntegratedServer` |
| `IStack` | `ItemStack` |
| `Item` | `Item` |
| `Items` | `Items` |
| `JWT` | `JoinWorldTask` |
| `KH` | `KeyboardHandler` |
| `KTS` | `KeyframeTrackSampler` |
| `Language` | `Language` |
| `LB` | `LiquidBlock` |
| `LC` | `LevelChunk` |
| `LCT` | `LoadingChunkTracker` |
| `LCTs` | `LevelChunkTicks` |
| `Level` | `Level` |
| `LIF` | `LootItemFunctions` |
| `LLSS` | `LayerLightSectionStorage` |
| `LO` | `LoadingOverlay` |
| `LP` | `LocalPlayer` |
| `LR` | `LevelRenderer` |
| `LRA` | `LayeredRegistryAccess` |
| `LSA` | `LevelStorageSource.LevelStorageAccess` |
| `LT` | `LootTable` |
| `LTs` | `LevelTicks` |
| `MC` | `Minecraft` |
| `MComp` | `MutableComponent` |
| `Mob` | `Mob` |
| `MPRM` | `MultiPackResourceManager` |
| `MR` | `MappedRegistry` |
| `MS` | `MinecraftServer` |
| `NbtIo` | `NbtIo` |
| `NS` | `NaturalSpawner` |
| `Parrot` | `Parrot` |
| `PCS` | `PlayerChunkSender` |
| `PDec` | `PacketDecoder` |
| `PDM` | `PatchedDataComponentMap` |
| `PDS` | `PlayerDataStorage` |
| `PEnc` | `PacketEncoder` |
| `PESM` | `PersistentEntitySectionManager` |
| `PL` | `PlayerList` |
| `Player` | `Player` |
| `PM` | `PoiManager` |
| `PN` | `PathNavigation` |
| `PP` | `PacketProcessor` |
| `PR` | `PackRepository` |
| `PRL` | `PreparableReloadListener` |
| `PST` | `PrepareSpawnTask` |
| `PTT` | `DistanceManager.PlayerTicketTracker` |
| `RB` | `RepeaterBlock` |
| `RC` | `ReloadCommand` |
| `RDC` | `RegistryDataCollector` |
| `RDL` | `RegistryDataLoader` |
| `RLT` | `RegistryLoadTask` |
| `RMRLT` | `ResourceManagerRegistryLoadTask` |
| `RRM` | `ReloadableResourceManager` |
| `RS` | `RenderSystem` |
| `RSR` | `ReloadableServerResources` |
| `RSReg` | `ReloadableServerRegistries` |
| `RSyn` | `RegistrySynchronization` |
| `SAI` | `SpatialAttributeInterpolator` |
| `SC` | `StopCommand` |
| `SCC` | `ServerChunkCache` |
| `SCD` | `SerializableChunkData` |
| `SCL` | `ServerConnectionListener` |
| `SCM` | `ServerClockManager` |
| `SCPL` | `ServerConfigurationPacketListenerImpl` |
| `Screen` | `Screen` |
| `SCT` | `SimulationChunkTracker` |
| `SGPL` | `ServerGamePacketListenerImpl` |
| `SHPL` | `ServerHandshakePacketListenerImpl` |
| `SIB` | `SleepInBed` |
| `SICF` | `SetItemCountFunction` |
| `SL` | `ServerLevel` |
| `SLPL` | `ServerLoginPacketListenerImpl` |
| `SP` | `ServerPlayer` |
| `SR` | `SkyRenderer` |
| `SRI` | `SimpleReloadInstance` |
| `SRT` | `SynchronizeRegistriesTask` |
| `SSB` | `SculkSensorBlock` |
| `SSPL` | `ServerStatusPacketListenerImpl` |
| `SW` | `ServerWatchdog` |
| `TagP` | `TagParser` |
| `TCTD` | `ThrottlingChunkTaskDispatcher` |
| `TL` | `TagLoader` |
| `TLE` | `ThreadedLevelLightEngine` |
| `TrC` | `TranslatableContents` |
| `TRM` | `ServerTickRateManager` |
| `TS` | `TicketStorage` |
| `TVO` | `TagValueOutput` |
| `VNP` | `ValidateNearbyPoi` |
| `VSel` | `VibrationSelector` |
| `VSL` | `VibrationSystem.Listener` |
| `VST` | `VibrationSystem.Ticker` |
| `WB` | `WorldBorder` |
| `Window` | `Window` |
| `WL` | `WorldLoader` |
| `WS` | `WorldStem` |
| `Auth` | *Auth: not a class* |
| `Disk` | *Disk: not a class* |
| `Hook` | *Hook: not a class* |
| `JVM` | *JVM: not a class* |
| `Main` | *Main: not a class* |
| `Netty` | *Netty: not a class* |
| `Wire` | *Wire: not a class* |
| `Worker` | *Worker: not a class* |
