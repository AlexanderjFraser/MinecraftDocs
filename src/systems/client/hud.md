# The HUD

> Verified against **Minecraft 26.2** · Part X · the player takes damage and the hearts shake, blink, and lie about how much health is left.

## Responsibility

Everything drawn over the world when no screen is up: hotbar, hearts,
hunger, the crosshair, effects, boss bars, the scoreboard, the tab list,
chat, titles and the debug screen. Short page; the machinery is
[GUI and screens](gui-and-screens.md), and this is the list of what uses
it.

The one sentence a player would recognise: *the hearts and the hotbar.*

The headline for a 1.21-era reader: **`Gui` is not the HUD any more.**
The class that drew the hotbar and hearts is now `Hud`; the name `Gui`
was reused for the screen and overlay manager that used to be fields on
`Minecraft`. The canonical path to the HUD is `Gui.hud`.

## The data it owns

`Hud` holds the sub-overlays — `Hud.chat` (a `ChatComponent`),
`Hud.bossOverlay` (`BossHealthOverlay`), `Hud.tabList`
(`PlayerTabOverlay`), `Hud.subtitleOverlay` (`SubtitleOverlay`),
`Hud.spectatorGui` (`SpectatorGui`), `Hud.debugOverlay`
(`DebugScreenOverlay`) — and its own animation state:
`Hud.tickCount`, `Hud.random`, `Hud.isHidden`, `Hud.lastHealth`,
`Hud.displayHealth`, `Hud.lastHealthTime`, `Hud.healthBlinkTime`,
`Hud.overlayMessageString`, `Hud.title`, `Hud.subtitle`,
`Hud.toolHighlightTimer`, `Hud.vignetteBrightness`,
`Hud.autosaveIndicatorValue` and the contextual bar in
`Hud.contextualInfoBar`.

Its nested types are `Hud.HeartType` (with `Hud.HeartType.forPlayer` and
`Hud.HeartType.getSprite`) and `Hud.ContextualInfo`.

The chat side is `ChatComponent` over `GuiMessage`, `GuiMessageTag`,
`GuiMessageSource` and `ChatComponent.DisplayMode`, fed by
`ChatListener`. Signing belongs to
[chat and signing](../networking/chat-and-signing.md); this page owns
display only.

The debug screen is now a registry. `DebugScreenEntries` holds every
entry by `Identifier`; each is a `DebugScreenEntry` writing lines through
a `DebugScreenDisplayer`. `DebugScreenEntryList` (reachable as
`Minecraft.debugEntries`) stores a `DebugScreenEntryStatus` per entry,
ships `DebugScreenProfile` presets, and persists to disk. The charts are
`FpsDebugChart`, `TpsDebugChart`, `PingDebugChart`, `BandwidthDebugChart`
over `AbstractDebugChart`, plus `ProfilerPieChart`.

## When it runs

`Hud.tick` runs from `Gui.tick` once per client tick and advances the
animations. `Hud.extractRenderState` runs from `Gui.extractRenderState`
once per frame, and — like everything else in the GUI — records render
states rather than drawing.

The order it records in, which is the order things appear in front of
each other: camera overlays (vignette, spyglass, the equipment-supplied
overlay, powder snow, portal or nausea) → crosshair with its attack
indicator → a new stratum → the hotbar block
(`Hud.extractHotbarAndDecorations`: hotbar, armour, hearts, food, air
bubbles, mount health, the contextual bar, the selected-item name) →
effects → boss bars → the sleep fade → demo text → scoreboard sidebar →
action bar → title → chat → tab list → subtitles. Then, outside the
hidden check, the saving indicator, toasts, the debug overlay and any
deferred subtitles.

## The trace: the hearts shake

```mermaid
sequenceDiagram
    participant CPL as ClientPacketListener
    participant LP as LocalPlayer
    participant H as Hud
    participant GGE as GuiGraphicsExtractor

    CPL->>LP: handleSetHealth — hurtTo, which sets hurtTime and invulnerableTime
    Note over H: next frame
    H->>H: extractPlayerHealth — health fell while invulnerable
    H->>H: healthBlinkTime = tickCount + 20; lastHealthTime = now
    Note over H: displayHealth is NOT updated — only after a second of quiet
    H->>H: random.setSeed(tickCount × a constant) — the shake is per tick, not per frame
    H->>H: extractHearts — containers, then the ghost of the old health, then the truth
    H->>GGE: blitSprite per heart, chosen by HeartType.getSprite
```

Two details worth the diagram. The shake is a random offset applied only
when health is very low, seeded from the HUD's tick counter — so it
jitters at 20 Hz and is identical across two frames of the same tick. And
the blink is a square wave over twenty ticks that draws the *ghost*: the
HUD keeps three different health numbers at once — last frame's, the
lagging display value, and the truth — and the blinking layer shows the
one that is out of date on purpose.

## Interfaces

- **Called by:** `Gui.tick` and `Gui.extractRenderState`.
- **Calls into:** `GuiGraphicsExtractor` for everything it records.
- **Crosses the network as:** it reads the results of
  `ClientboundSetHealthPacket`, `ClientboundSetExperiencePacket`,
  `ClientboundBossEventPacket`, `ClientboundTabListPacket`,
  `ClientboundSetActionBarTextPacket` and the title packets — the
  handlers call `Hud.setOverlayMessage`, `Hud.setTitle`,
  `Hud.setSubtitle`, `Hud.setTimes` and `BossHealthOverlay.update`.
- **Data-driven by:** the GUI atlas; the crosshair's attack indicator by
  `Options.attackIndicator` and `AttackIndicatorStatus`; the hidden state
  by the F1 key binding.

## Invariants and surprises

- **`Gui` and `Hud` are different things.** `Gui` is "what screen is up,
  and the things that outlive screens"; `Hud` is "what is drawn over the
  world". Neither has a *render* method — both have
  an *extract* method.
- ***Options.hideGui* no longer exists.** F1 toggles `Hud.isHidden`,
  which is published to the *renderer* as `GuiRenderState.isHudHidden`
  and read by `GameRenderer` to suppress the held item, the screen
  effects and the three-dimensional crosshair. A HUD flag reaching into
  world rendering through the GUI render state is the surprising
  direction of that dependency.
- **The debug screen is data-driven and persisted.** Entries are
  registered by `Identifier`, each with a three-valued status, and an
  entry set to always-on renders with F3 never pressed. There is a screen
  for editing it, and the overlay hides itself while that screen is open.
- **Every F3 shortcut is a rebindable key mapping.** F3+B and F3+G are
  debug entries that print nothing and exist purely to carry a toggle the
  world renderer reads.
- **Food and mount health share a slot.** The hunger bar is only drawn
  when the mount-health bar is absent, and the air bubbles shift
  accordingly.
- **The experience bar is one of four mutually exclusive bars.** A
  `Hud.ContextualInfo` state machine arbitrates between experience, the
  waypoint locator, a jumpable vehicle and nothing — but the level
  *number* is drawn separately and survives whichever bar wins.
- **Subtitles are extracted twice, conditionally.** When an in-game UI
  screen is open the subtitle work is stashed as a closure and run after
  the screen, so subtitles sit above it. It is the only HUD element with
  two possible positions in a frame.
- **Boss bars have world-rendering consequences.** The overlay answers
  whether the screen should darken and whether world fog should be
  created, and the frame reads both; the bar itself interpolates against
  wall-clock time, so discrete packet progress becomes a smooth bar.
- **The chat HUD and the chat screen are the same code in different
  modes.** The HUD draws the faded background mode and bails out entirely
  when the chat screen is focused — asking the *screen manager* whether
  to draw chat. Message age is measured in HUD ticks, not timestamps.
- **There are two independent chat queues.** The delay-option queue sits
  in front of `ChatComponent` and its size is drawn as a clickable line;
  separately, a message the server asked to delete is held until it has
  been visible for a minimum time, and is then replaced with a marker
  rather than removed.
- **The camera overlay list is data-driven.** The pumpkin blur is no
  longer a hardcoded block check — every equipment slot is asked whether
  its item declares a camera overlay.
- **Names a 1.21-era reader will hunt for and not find:** every
  `Gui.render*` method (now `Hud.extract*`), *LayeredDraw* (ordering is
  now the literal call order plus stratum boundaries),
  *Minecraft.screen*, *Minecraft.getToastManager*,
  *Minecraft.fpsString*, *Options.hideGui*, and
  *DebugScreenOverlay.render* along with its two information-gathering
  methods — the line content moved out into the entry registry.

## Where to look

`Hud.extractRenderState` — the whole HUD is one ordered method. Then
`Hud.extractPlayerHealth` for the most-loved twenty lines in the client,
`DebugScreenEntries` for the debug registry, and `ChatComponent` for the
message list.

---

*Rules: names, never code · how the system works, not how the code reads ·
newest version only · every backticked name passes `tools/verify_names.py`.*
