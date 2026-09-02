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
| `DM` | `DistanceManager` |
| `DMR` | `DefaultedMappedRegistry` |
| `DS` | `DedicatedServer` |
| `DScr` | `DeathScreen` |
| `EH` | `EnchantmentHelper` |
| `EM` | `EnchantmentMenu` |
| `Entity` | `Entity` |
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
| `LT` | `LootTable` |
| `MC` | `Minecraft` |
| `MComp` | `MutableComponent` |
| `MPRM` | `MultiPackResourceManager` |
| `MR` | `MappedRegistry` |
| `MS` | `MinecraftServer` |
| `NbtIo` | `NbtIo` |
| `Parrot` | `Parrot` |
| `PCS` | `PlayerChunkSender` |
| `PDec` | `PacketDecoder` |
| `PDM` | `PatchedDataComponentMap` |
| `PEnc` | `PacketEncoder` |
| `PESM` | `PersistentEntitySectionManager` |
| `PL` | `PlayerList` |
| `Player` | `Player` |
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
| `TagP` | `TagParser` |
| `TCTD` | `ThrottlingChunkTaskDispatcher` |
| `TL` | `TagLoader` |
| `TrC` | `TranslatableContents` |
| `TS` | `TicketStorage` |
| `TVO` | `TagValueOutput` |
| `Window` | `Window` |
| `WL` | `WorldLoader` |
| `Auth` | *Auth: not a class* |
| `Disk` | *Disk: not a class* |
| `Main` | *Main: not a class* |
| `Netty` | *Netty: not a class* |
| `Wire` | *Wire: not a class* |
| `Worker` | *Worker: not a class* |
