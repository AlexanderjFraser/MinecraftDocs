# The HUD

> Verified against **Minecraft 26.2** · Part X · press F1 and the interface goes away — except for the thing that can black out your whole screen.

`Hud.extractRenderState` is a single ordered method wrapped in two
hidden-gated blocks, and one element sits *between* them: the sleep fade. So
F1 hides the hearts, the hotbar, the crosshair, chat and the tab list, and
does not hide the black screen that comes over you when you get into bed.
Four more elements are recorded by `Gui`, after the screen rather than with
the rest of the HUD — the saving indicator, the debug overlay, the deferred
subtitles and the toasts — and only the toasts are outside `Hud`'s own
methods. Only the saving indicator ignores the flag.

That is what this page is: not a tour of hearts and hotbars but a **policy**.
What is drawn over the world, in what order, under exactly which conditions,
and which of those conditions is a surprise. The full per-element table is
[what the HUD draws, and when](../../reference/hud-elements.md) in Reference;
the machinery underneath every one of them is [the GUI render
tree](the-gui-render-tree.md#the-tree-and-where-a-new-element-lands), and
what a *screen* is — the other thing recorded into that tree, and the reason
four of these elements are recorded after rather than with the rest — is [GUI
and screens](gui-and-screens.md#gui-which-is-not-the-hud).

## The cast

| class | what it decides | thread |
|---|---|---|
| `Hud` | the order, the two hidden-gated blocks, and the health animation state | Render thread |
| `Gui` | the four elements recorded *after* the screen | Render thread |
| `ContextualBar` | which of four things occupies the one slot above the hotbar | Render thread |
| `BossHealthOverlay` | the bars, and three questions the world renderer asks it | Render thread |
| `ChatComponent` | the message list, its wrapped lines, and what is faded out | Render thread |
| `DebugScreenEntries` | the F3 registry: what an entry is, and whether it is on | Render thread |
| `DebugScreenEntryList` | the per-entry status, its presets, and its own save file | Render thread |
| `GuiGraphicsExtractor` | everything the HUD records into | Render thread |

## The order, and the two blocks

```mermaid
flowchart TD
    PUB["publish GuiRenderState.isHudHidden — before any check, so the flag is always current"]
    LLS{"is a LevelLoadingScreen up?"}
    STOP["record nothing"]
    H1{"hidden?"}
    A["camera overlays, then the crosshair, then a new stratum, then the hotbar block, effects, boss bars"]
    SLEEP["the sleep fade — ungated"]
    H2{"hidden?"}
    B["demo text, scoreboard sidebar, action bar, title, chat, tab list, subtitles"]
    B2["subtitles only, and only if an in-game-UI screen is up"]
    GUI["Gui continues: saving indicator, toasts, debug overlay, deferred subtitles"]
    PUB --> LLS
    LLS -- "yes" --> STOP
    LLS -- "no" --> H1
    H1 -- "no" --> A --> SLEEP
    H1 -- "yes" --> SLEEP
    SLEEP --> H2
    H2 -- "no" --> B --> GUI
    H2 -- "yes" --> B2 --> GUI
```

Above all of that sit three gates that are not `Hud`'s at all, and a page
about conditions has to name them: `GameRenderer.extract` computes whether
resources are loaded, whether this frame advances game time and whether there
is a level, and `Gui.extractRenderState` applies them, calling into `Hud` only
when they hold. That is why a HUD-less frame is the normal state of a loading
screen rather than a special case of one — and it is also the difference
between the two `Gui`-recorded elements that survive a level and the two that
do not.

Two structural facts follow from the shape. The hidden flag is published
*before* the loading-screen short-circuit, so the renderer's copy is correct
even on a frame where the HUD records nothing. And toasts and the debug
overlay are always **above** a screen, because `Gui` records them after it —
while the deferred subtitles are called from a screen's *background* pass, so
the deferral that fires after the screen finds nothing left to draw and the
subtitles a screen drew for itself sit under that screen's widgets.

`Hud.tick` runs from `Gui.tick` once per client tick and takes a pause flag:
the autosave indicator animates either way, everything else only when the
game is not paused.

The toasts are the one element in that list with arbitration of its own, and
it is a shelf rather than a queue. `ToastManager` holds **five** slots and a
waiting deque; a toast declares how many consecutive slots it wants through
`Toast.occcupiedSlotCount` — Mojang's spelling — and is admitted only when
that many free slots sit next to each other, so a wide toast can wait behind
narrow ones that arrived after it. `Toast.Visibility` is the two-state
animation, each state carrying its own sound, and a toast is asked its wanted
visibility every frame rather than given a lifetime. `Toast.getToken` is what
lets a second advancement replace the first instead of stacking on it. The
implementations are `AdvancementToast`, `RecipeToast`, `TutorialToast`,
`SystemToast`, `FriendToast` and `NowPlayingToast` — the last of which is not
on the shelf at all: it is a field of its own, drawn after the five and
suppressed by the pause screen and by `MusicToastDisplayState`.

## The hidden flag travels two ways

The interesting one is the smaller. `GuiRenderState.isHudHidden` is read by
`GameRenderer` in three places, to suppress the held item, the
three-dimensional crosshair and — the smallest of the three — the totem-pop
animation. The block-in-eyes, water and fire overlays are drawn whatever F1
says. So a 2D flag does change how the *world* is drawn, in three narrow
ways. But `Hud.isHidden` itself is read directly by six other places across
the client, including two entity renderers that suppress name tags.

It is not the only field on the tree the world reads back: a clear-colour
override lives there too, and every site that reads either of them is
`GameRenderer`'s rather than `LevelRenderer`'s — the 2D side never reaches
into the world renderer, only into the thing that drives it. The traffic goes
the other way as well, and this page's own boss bar is the loudest example:
`BossHealthOverlay` reads world fog, the lightmap and the level render state
to answer its three questions.

## Four states, one slot, and an asymmetric rule

`Hud.contextualInfoBar` holds one of four states — nothing, experience, the
locator, a jumpable vehicle — and `Hud.nextContextualInfoState` re-decides
which every frame. It is a rule, not a state machine, and the rule is not
symmetric. With waypoints present, a jumping vehicle or a *recently changed*
experience total beats the locator; with no waypoints, a jumpable vehicle
beats experience unconditionally — so **mounting a horse silently takes your
XP bar away.** The level number is recorded separately from the bar, so it
survives whichever bar wins.

The three implementations are `ExperienceBar`, `LocatorBar` — backed by
`ClientWaypointManager` and styled by `Hud.waypointStyles`, a
`WaypointStyleManager` that is the HUD's own reload listener — and
`JumpableVehicleBar`. `Hud.ContextualInfo` is the enum of the four states.

## The hearts, which are three numbers at once

```mermaid
sequenceDiagram
    participant CPL as ClientPacketListener
    participant LP as LocalPlayer
    participant Hud as Hud
    participant GGE as GuiGraphicsExtractor

    CPL->>LP: handleSetHealth — hurtTo, which sets hurtTime and invulnerableTime
    Note over Hud: next frame
    Hud->>Hud: extractPlayerHealth — health fell while invulnerable
    Hud->>Hud: healthBlinkTime becomes tickCount plus 20 (a heal sets 10)
    Hud->>Hud: displayHealth catches up only once the second has elapsed
    Hud->>Hud: random.setSeed(tickCount times a constant) — the jitter is per tick, not per frame
    Hud->>Hud: extractHearts — one descending pass: container, absorption, ghost, truth
    Hud->>GGE: blitSprite per heart, chosen by HeartType.getSprite
```

**The shake is seeded from the tick counter**, so it jitters at 20 Hz and is
identical across two frames of the same tick — and the same seeded stream
drives the hunger jitter and the air-bubble wobble, which is why they shake
together. **The blink is a square wave** with a three-tick half-period,
running for twenty ticks after damage and ten after a heal, and what it draws
is the *ghost*: the HUD keeps three health numbers at once — last frame's, a
lagging display value that catches up about once a second, and the truth — and
the blinking layer shows the one that is out of date on purpose.

`Hud.HeartType` is six constants, one of which Mojang spells
`Hud.HeartType.POISIONED`, each with eight sprites.

One gate silences four elements at once: armour, hearts, food and air are all
recorded inside `Hud.extractPlayerHealth`, which is gated on the game mode
being able to hurt you — which is why creative has no armour bar either. Food
and mount health share a slot, and the air bubbles shift up when either is
drawn. And the HUD makes a sound of its own, which is the only element in it that
does.

## Questions players ask

**Why does the boss bar change the sky?** The overlay answers three questions
— should the screen darken, should world fog be created, should the End music
play — read from five places between the frame, the fog environment and the
lightmap. The bar itself interpolates against wall-clock time inside
`LerpingBossEvent`, so discrete packet progress becomes a smooth bar.

**Why do subtitles appear under an open chest?** They are deferred past the
screen, along with the tooltip and the pre-edit overlay the extractor holds. The deferral fires when there is no screen at all *or* the screen
declares itself in-game UI — the common case, not the rare one — and the
deferred call is made from a screen's background pass.

**Are the chat HUD and the chat screen the same thing?** The same code in
different modes. The HUD bails out entirely when the chat screen is focused.
Message age is measured in HUD ticks rather than timestamps, and a message the
server asked to delete keeps its original timestamp when it is replaced by a
marker — so the marker fades on the original message's schedule.
`ChatComponent` holds **four** collections, not two: every message and every
wrapped *line* are separate lists with separate caps, and the deletion queue
and the recent-input history are the other two. A fifth, the delay-option
queue, lives on `ChatListener` — the reason a chat-delay setting can hold a
message that has already arrived.

What those lists hold is a `GuiMessage` — the time it arrived in HUD ticks,
the `Component`, the signature if it had one, a `GuiMessageSource` saying
whether a player, the server or this client produced it, and a nullable
`GuiMessageTag`. **The tag is the client's own verdict, drawn as a two-pixel
bar to the *left* of the line**, outside the text entirely, with the reason as
a tooltip when you hover it: system, system-in-singleplayer, not-secure,
modified, error. Only *modified* also carries an icon, and that one goes after
the text rather than beside the bar; each tag additionally carries a short
`GuiMessageTag.logTag` string, which is the only part of it that reaches
`ChatLog` — a separate ring of `LoggedChatEvent`s kept for the reporting
screens rather than for display. Which verdict a message earned is [chat and
signing](../networking/chat-and-signing.md#three-ways-to-say-no)'; this page
owns the bar.

**Is the pumpkin blur hardcoded?** No. The camera overlay list is
data-driven: every equipment slot is asked whether its item declares a camera
overlay.

**Why does the air-bubble pop get louder as I drown?** Because the HUD makes
that sound itself. `Hud.playAirBubblePoppedSound` ramps volume and pitch with
how many bubbles are *gone*, and hands it to [the sound
engine](sound-engine.md#volume-is-three-factors-and-looping-is-three-mechanisms)
like any other client-side sound — one of the few places a drawing pass is
also an audio event.

**Can I turn a debug line on without pressing F3?** Yes, and the game saves
that you did. `DebugScreenEntries` holds every entry by `Identifier`, each a
`DebugScreenEntry` writing lines through a `DebugScreenDisplayer`;
`DebugScreenEntryList`, reachable as `Minecraft.debugEntries`, stores a
`DebugScreenEntryStatus` per entry, ships `DebugScreenProfile` presets and
persists to its own file with its own data-fixer type. The *other* debug
system, the one that asks the server for a villager's brain, is [debugging the
running game](debugging-the-running-game.md#the-idea) — and the two meet here,
because an F3 entry decides whether eleven of the renderers exist and the FPS
charts are what turn the tick-time subscription on. An entry set to
always-on renders with F3 never pressed. The screen that edits it is
suppressed by `Gui`, not by the overlay. The charts are `FpsDebugChart`,
`TpsDebugChart`, `PingDebugChart` and `BandwidthDebugChart` over
`AbstractDebugChart` — plus `ProfilerPieChart`, which is not one of them.

**Why is that F3 shortcut not rebindable?** Because it is not a mapping —
which family a given shortcut belongs to is [input and
keybinds](input-and-keybinds.md#questions-players-ask)'. What is this page's:
several of the mappings that *are* rebindable toggle debug entries printing no
line at all, and exist only to carry a flag the world renderer reads.

**What counts as "HUD state"?** Whatever `Hud.onDisconnected` resets — tab
list, boss bars, toasts, debug overlay, chat and titles, together. It is the
only place that clears the HUD as a whole, and it is a better definition than
any list of fields.

> **For a 1.21-era reader.** `Gui` is not the HUD any more. The class that
> drew the hotbar and hearts is `Hud`; the name `Gui` was reused for the
> screen and overlay manager that used to be fields on `Minecraft`. The
> canonical path is `Gui.hud`. Every *render\** method on `Gui` is now an *extract\** on `Hud`, and gone with them: *LayeredDraw*, *Minecraft.screen*,
> *Minecraft.getToastManager*, *Minecraft.fpsString*, *Options.hideGui*, and
> *DebugScreenOverlay.render* along with its two information-gathering
> methods — the line content moved out into the entry registry.

## Where to look

`Hud.extractRenderState` — the whole HUD is one ordered method, and the two
hidden-gated blocks are visible at a glance. Then `Hud.extractPlayerHealth`
for the most-loved fifty-seven lines in the client,
`Hud.nextContextualInfoState` for the bar arbitration, `Gui.extractRenderState`
for the four recorded after the screen, `DebugScreenEntries` for the F3
registry, and `ChatComponent` for the message list.

---

*Rules: names, never code · how the system works, not how the code reads ·
newest version only · every backticked name passes `tools/verify_names.py`.*
