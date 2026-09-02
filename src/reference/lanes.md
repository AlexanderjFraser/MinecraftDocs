# Diagram lanes

Every lane in a sequence diagram is a class name abbreviated once for the whole
corpus. This is the key, generated from `TEMPLATE.md` by
`python tools/check_lanes.py --index`; the initials of the class's CamelCase words,
a one-word class as itself, and a few words for things that are not classes.

| lane | class |
|---|---|
| `ACM` | `AbstractContainerMenu` |
| `BEL` | `BlockableEventLoop` |
| `BIR` | `BuiltInRegistries` |
| `Boot` | `Bootstrap` |
| `CBE` | `ChestBlockEntity` |
| `CCPL` | `ClientConfigurationPacketListenerImpl` |
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
| `EAS` | `EnvironmentAttributeSystem` |
| `EH` | `EnchantmentHelper` |
| `EM` | `EnchantmentMenu` |
| `Entity` | `Entity` |
| `ETL` | `EntityTickList` |
| `Font` | `Font` |
| `GR` | `GameRenderer` |
| `Gui` | `Gui` |
| `HS` | `HashedStack` |
| `Hud` | `Hud` |
| `IP` | `ItemParser` |
| `IS` | `IntegratedServer` |
| `IStack` | `ItemStack` |
| `Item` | `Item` |
| `Items` | `Items` |
| `JWT` | `JoinWorldTask` |
| `KH` | `KeyboardHandler` |
| `Language` | `Language` |
| `LCT` | `LoadingChunkTracker` |
| `Level` | `Level` |
| `LIF` | `LootItemFunctions` |
| `LO` | `LoadingOverlay` |
| `LP` | `LocalPlayer` |
| `LR` | `LevelRenderer` |
| `LRA` | `LayeredRegistryAccess` |
| `LSA` | `LevelStorageSource.LevelStorageAccess` |
| `LT` | `LootTable` |
| `LTs` | `LevelTicks` |
| `MC` | `Minecraft` |
| `MComp` | `MutableComponent` |
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
| `PP` | `PacketProcessor` |
| `PR` | `PackRepository` |
| `PRL` | `PreparableReloadListener` |
| `PST` | `PrepareSpawnTask` |
| `PTT` | `DistanceManager.PlayerTicketTracker` |
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
| `SC` | `StopCommand` |
| `SCC` | `ServerChunkCache` |
| `SCL` | `ServerConnectionListener` |
| `SCPL` | `ServerConfigurationPacketListenerImpl` |
| `Screen` | `Screen` |
| `SCT` | `SimulationChunkTracker` |
| `SGPL` | `ServerGamePacketListenerImpl` |
| `SHPL` | `ServerHandshakePacketListenerImpl` |
| `SICF` | `SetItemCountFunction` |
| `SL` | `ServerLevel` |
| `SLPL` | `ServerLoginPacketListenerImpl` |
| `SP` | `ServerPlayer` |
| `SRI` | `SimpleReloadInstance` |
| `SRT` | `SynchronizeRegistriesTask` |
| `SSPL` | `ServerStatusPacketListenerImpl` |
| `SW` | `ServerWatchdog` |
| `TagP` | `TagParser` |
| `TCTD` | `ThrottlingChunkTaskDispatcher` |
| `TL` | `TagLoader` |
| `TrC` | `TranslatableContents` |
| `TRM` | `ServerTickRateManager` |
| `TS` | `TicketStorage` |
| `TVO` | `TagValueOutput` |
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
