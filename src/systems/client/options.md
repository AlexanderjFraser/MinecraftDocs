# Options

> Verified against **Minecraft 26.2** · Part X · the render-distance slider: a value that takes effect on a delay, rebuilds the world on a later frame, and reaches the server only when a screen closes — with no reply.

## Responsibility

One flat file, one listener mechanism, and nine fields the server is ever
told about. This page owns `Options` — how a setting is stored, when it is
written to disk, what happens as a side effect of changing it, and which
handful of settings the server hears about at all. The bindings that also
live on `Options` are [input and keybinds](input-and-keybinds.md).

The one sentence a player would recognise: *turning a setting down and
watching the world redraw.*

The headline: **saving is the event system.** There is no
settings-changed hook. The server learns about a new view distance because
something called `Options.save`, and the set of things that call it is
larger and stranger than "the player pressed Done".

## The data it owns

`Options` stores settings three different ways, and the difference matters:

- **`OptionInstance`** — the modern shape: a value, a codec, an initial
  value, a caption, a listener, and an `OptionInstance.ValueSet` that
  decides both the legal values and the *widget*. The value sets divide into
  `OptionInstance.SliderableValueSet` and
  `OptionInstance.CycleableValueSet`, and that split is why some settings
  save on click and some do not. Concrete sets include
  `OptionInstance.IntRange`, `OptionInstance.ClampingLazyMaxIntRange`,
  `OptionInstance.UnitDouble`, `OptionInstance.Enum`,
  `OptionInstance.LazyEnum`, `OptionInstance.AltEnum` and
  `OptionInstance.SliderableEnum`.
- **Plain fields**, read and written by name in `Options.processOptions`:
  the language code, the resource-pack lists, `Options.tutorialStep`,
  `Options.smoothCamera`, `Options.advancedItemTooltips`,
  `Options.joinedFirstServer`, `Options.startedCleanly` and a dozen others.
  These have no listener and no widget machinery at all — and
  `Options.smoothCamera`, toggled by a keybind, is not persisted anywhere.
- **The key-mapping array**, covered on the input page.

`Options.serverRenderDistance` is the ceiling the server announced, and
`Options.getEffectiveRenderDistance` is the clamp against it.
`Options.graphicsPreset` and `Options.setGraphicsPresetToCustom` are the
preset machinery — a preset writes a batch of settings at once, and almost
every graphics listener flips the preset back to custom.
`Options.buildPlayerInformation` assembles the `ClientInformation` the server
is told, and `Options.broadcastOptions` sends it.
`Options.dumpOptionsForReport` and `Options.processDumpedOptions` are the
smaller subset that goes into crash reports and telemetry.

`ClientInformation` itself is a nine-field record — language, view distance,
chat visibility, chat colours, skin model parts, main hand, text filtering,
listing permission, particle status — and it lives in `server/level`, not in
a client package, because the server is where it is kept.

## When it runs

**Loading happens once**, from the `Options` constructor, before
`Minecraft.running` is set. That timing is the whole of the "loading does not
trigger listeners" behaviour: `OptionInstance.set` checks whether the game is
running, and when it is not it assigns the field and skips both the equality
test and the listener. It is a property of *every* set performed before the
loop starts, not a special path for loading.

**Saving happens often.** `Options.save` writes the file and then calls
`Options.broadcastOptions`, and it is called from about sixteen places: the
constructor, several recovery paths in `Minecraft`, the fullscreen toggle,
the first-server toast, every options screen on close, three debug keys, the
tutorial's step change, and — the one that changes the shape of the system —
`OptionInstance.CycleableValueSet`'s button, on every click.

**Sliders apply late.** A slider whose value is not applied immediately arms
a delay of about six hundred milliseconds, checked during the extract pass;
dismissing the screen inside that window applies it early instead.

## The trace: the render-distance slider

```mermaid
sequenceDiagram
    participant S as OptionInstance.SliderableValueSet
    participant O as Options
    participant LX as LevelExtractor
    participant CPL as ClientPacketListener
    participant SP as ServerPlayer
    participant CM as ChunkMap

    S->>S: drag — the value is not applied yet; a delay is armed
    S->>O: OptionInstance.set — on a later frame, or at once if the screen closes first
    O->>O: listener — for this option, only "the graphics preset is now custom"
    Note over LX: next frame
    LX->>LX: getEffectiveRenderDistance differs from the last one
    LX->>LX: allChanged — tint caches cleared, tracker rebuilt, all geometry invalid
    Note over O: when the screen closes
    O->>O: save — writes options.txt
    O->>CPL: broadcastOptions → ClientInformation (skipped if nothing changed)
    CPL->>SP: ServerboundClientInformationPacket
    SP->>SP: updateOptions — requestedViewDistance and eight other fields
    Note over CM: silently, on a later chunk-map tick
    CM->>CM: getPlayerViewDistance clamps the request and re-tracks
```

Two things about the shape. **The rebuild is not the listener's doing** —
this option's listener only marks the graphics preset custom; the world
rebuilds because the extractor notices, next frame, that the effective
distance changed. Most *other* graphics options are the opposite way round:
their listeners call into the extractor, the window, the sound manager or
the font manager directly.

And **the trace ends at the server**. There is no reply. The only thing that
ever sets `Options.serverRenderDistance` is the server announcing its *own*
view distance — in the login packet, or by broadcasting
`ClientboundSetChunkCacheRadiusPacket` when an operator changes it. A
client's request is clamped and used for chunk tracking, and the client is
never told what it was clamped to.

Cycle options behave differently enough to be worth a second look: a click
sets the value, runs the listener and calls `Options.save` immediately — so
changing chat visibility broadcasts your `ClientInformation` before you have
left the screen.

## Interfaces

- **Called by:** everything. `Options` is read from every part of the
  client.
- **Calls into:** the listener targets — `LevelExtractor` for anything that
  invalidates geometry, `Window` for fullscreen and raw input,
  `SoundManager` for the audio device, `Minecraft` for GUI scale and surface
  reconfiguration, and the font manager for the unicode and Japanese-variant
  toggles.
- **Crosses the network as:** `ServerboundClientInformationPacket`. It is a
  *common* packet: one is sent during configuration, straight from
  `ClientHandshakePacketListenerImpl`, before the play phase exists; every
  later one comes from `Options.broadcastOptions`. Inbound,
  `ClientboundSetChunkCacheRadiusPacket` and
  `ClientboundSetSimulationDistancePacket` are announcements, not replies.
- **Data-driven by:** *options.txt* in the game directory, which carries a
  version line and is run through the data fixer on load.

## Invariants and surprises

- **`Options.save` is the only caller of `Options.broadcastOptions`** — and
  because a cycle button saves on every click, that is a much weaker
  statement than it sounds. The send is skipped when the assembled
  `ClientInformation` is identical to the last one sent.
- **Loading skips every listener because the game is not running yet**, not
  because loading is special. The same rule silences a set performed anywhere
  else before the loop starts.
- **The render-distance slider's maximum depends on the JVM's heap.** The
  option is a lazily-clamped range, and the clamp reads the runtime's
  maximum memory.
- **Simulation distance is never sent to the server — except in
  singleplayer, where it does not need to be.** The record has no field for
  it. But `IntegratedServer.tickServer` reads both the simulation and render
  sliders off the client's options every server tick and pushes them into
  the player list, so in singleplayer both sliders drive the server directly
  and neither travels as client information.
- **Two settings need a restart and say so.** The graphics backend and
  exclusive fullscreen are compared against snapshots taken at startup;
  `Options.isRestartRequiredToApplyVideoSettings` is what the screen asks.
  `Options.startedCleanly` is written false at startup and true once the
  game is up, so a crash during boot can drop the client back to a safe
  backend.
- **Options are per installation, never per world.** That includes the
  tutorial step, so once any world drives the tutorial to the end, no later
  world shows the toasts again — and an unrecognised step name silently
  reads as *finished*.
- **Failure is quiet by design.** A bad line in the file is logged and
  skipped, a bad value for an `OptionInstance` is logged and dropped back to
  the initial value, and a bad number keeps the current one. Nothing about a
  corrupt *options.txt* stops the game starting.
- **Some listeners are far more interesting than their options.** GUI scale
  resizes every screen; vsync invalidates the surface configuration;
  fullscreen toggles the window and then writes the option back from what
  the window actually did; the unicode font toggle throws away every glyph
  atlas; high contrast adds and removes a resource pack; and half a dozen
  graphics options call straight into the level extractor.
- **Names a 1.21-era reader will hunt for and not find:**
  *Options.mouseSensitivity* and the other bare public fields — the modern
  settings are private with accessor methods of the same name — and
  *Options.keyBindings*.

## Where to look

`Options.processOptions` for the settings table — it is the file format and
the field list in one method — and `Options.processDumpedOptions` for the
crash-report subset. `OptionInstance.set` for the listener guard.
`Options.buildPlayerInformation` for the nine fields the server hears.
`ChunkMap.getPlayerViewDistance` for what the server does with the one that
matters, and `IntegratedServer.tickServer` for the singleplayer back door.

---

*Rules: names, never code · how the system works, not how the code reads ·
newest version only · every backticked name passes `tools/verify_names.py`.*
