# Diagram lanes

Every lane in a sequence diagram is a class name abbreviated once for the whole
corpus. This is the key, generated from `TEMPLATE.md` by
`python tools/check_lanes.py --index`; the initials of the class's CamelCase words,
a one-word class as itself, and a few words for things that are not classes.

| lane | class |
|---|---|
| `BEL` | `BlockableEventLoop` |
| `CCPL` | `ClientConfigurationPacketListenerImpl` |
| `CH` | `ChunkHolder` |
| `CHPL` | `ClientHandshakePacketListenerImpl` |
| `CL` | `ClientLevel` |
| `CM` | `ChunkMap` |
| `Conn` | `Connection` |
| `CPL` | `ClientPacketListener` |
| `CTD` | `ChunkTaskDispatcher` |
| `DM` | `DistanceManager` |
| `DS` | `DedicatedServer` |
| `Entity` | `Entity` |
| `GR` | `GameRenderer` |
| `Gui` | `Gui` |
| `Hud` | `Hud` |
| `IS` | `IntegratedServer` |
| `JWT` | `JoinWorldTask` |
| `LCT` | `LoadingChunkTracker` |
| `Level` | `Level` |
| `LP` | `LocalPlayer` |
| `LR` | `LevelRenderer` |
| `MC` | `Minecraft` |
| `MS` | `MinecraftServer` |
| `PCS` | `PlayerChunkSender` |
| `PESM` | `PersistentEntitySectionManager` |
| `PL` | `PlayerList` |
| `Player` | `Player` |
| `PST` | `PrepareSpawnTask` |
| `PTT` | `DistanceManager.PlayerTicketTracker` |
| `RS` | `RenderSystem` |
| `SCC` | `ServerChunkCache` |
| `SCL` | `ServerConnectionListener` |
| `SCPL` | `ServerConfigurationPacketListenerImpl` |
| `Screen` | `Screen` |
| `SCT` | `SimulationChunkTracker` |
| `SGPL` | `ServerGamePacketListenerImpl` |
| `SHPL` | `ServerHandshakePacketListenerImpl` |
| `SL` | `ServerLevel` |
| `SLPL` | `ServerLoginPacketListenerImpl` |
| `SP` | `ServerPlayer` |
| `SRT` | `SynchronizeRegistriesTask` |
| `SSPL` | `ServerStatusPacketListenerImpl` |
| `TCTD` | `ThrottlingChunkTaskDispatcher` |
| `TS` | `TicketStorage` |
| `Window` | `Window` |
| `Auth` | *Auth: not a class* |
| `Disk` | *Disk: not a class* |
| `Main` | *Main: not a class* |
| `Netty` | *Netty: not a class* |
| `Wire` | *Wire: not a class* |
| `Worker` | *Worker: not a class* |
