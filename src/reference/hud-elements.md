# What the HUD draws, and when

> Verified against **Minecraft 26.2** · Reference · Hand-kept from
> `Hud.extractRenderState` and `Gui.extractRenderState`.

The HUD is one ordered method, and almost every element in it is behind a
condition — the contextual bar is the exception, recorded unconditionally and
made to draw nothing by an empty state object instead.
The lecture that frames this is [the HUD](../systems/client/hud.md); this is
the table it is built on, in **record order** — which is also the order
things appear in front of each other, since [the GUI render
tree](../systems/client/the-gui-render-tree.md) infers layering from call
order and bounding boxes.

Three gates sit above everything below and none of them belongs to `Hud` —
resources loaded, the frame advancing game time, a level existing; [the
HUD](../systems/client/hud.md#the-order-and-the-two-blocks) is where they are
explained. Below them `Hud.extractRenderState` short-circuits entirely while a
`LevelLoadingScreen` is up, publishing `GuiRenderState.isHudHidden` before it
does.

*Hidden* in the last column means `Hud.isHidden`, which `Options.keyToggleGui`
— F1 — flips.

| # | element | recorded by | hidden by F1? | its own condition |
|---:|---|---|---|---|
| 1 | vignette | `Hud.extractVignette` | yes | `Options.vignette` is on |
| 2 | spyglass overlay | `Hud.extractSpyglassOverlay` | yes | first-person camera **and** the player is scoping |
| 3 | equipment camera overlay | `Hud.extractTextureOverlay` | yes | first-person, not scoping, and some equipped item's `Equippable` declares a camera overlay for the slot it is in |
| 4 | powder-snow outline | `Hud.extractTextureOverlay` | yes | `Entity.getTicksFrozen` above zero |
| 5 | portal overlay | `Hud.extractPortalOverlay` | yes | the interpolated portal intensity is above zero |
| 6 | nausea overlay | `Hud.extractConfusionOverlay` | yes | *else*: no portal effect, a nausea blend above zero, and `Options.screenEffectScale` below one |
| 7 | crosshair | `Hud.extractCrosshair` | yes | first-person; either not a spectator or a hit result a spectator may see; **and** the F3 three-dimensional-crosshair entry is off |
| — | *new stratum* | `GuiGraphicsExtractor.nextStratum` | — | a hard layering barrier — everything below is above everything above. `Hud` calls it ten times in all; this is the one that separates the overlays from the rest, and there is another inside the crosshair |
| 8 | hotbar | `Hud.extractItemHotbar` | yes | a camera player exists — replaced by `SpectatorGui.extractHotbar` in spectator mode |
| 9 | armour | `Hud.extractArmor` | yes | inside the health block, and `LivingEntity.getArmorValue` above zero |
| 10 | hearts | `Hud.extractHearts` | yes | inside the health block |
| 11 | food | `Hud.extractFood` | yes | inside the health block, **and** the vehicle contributes no hearts |
| 12 | air bubbles | `Hud.extractAirBubbles` | yes | inside the health block, and the player's eyes are in water or the air supply is below its maximum |
| 13 | mount health | `Hud.extractVehicleHealth` | yes | a ridden `LivingEntity` with a non-zero heart count — **outside** the health block, so creative shows it |
| 14 | contextual bar, background | `ContextualBar.extractBackground` | yes | always recorded, but which of four states it is in is re-decided every frame by `Hud.nextContextualInfoState` |
| 15 | experience level | `ContextualBar.extractExperienceLevel` | yes | the game mode has experience **and** the level is above zero — recorded between the bar's two passes, so it survives whichever bar wins |
| 16 | contextual bar, foreground | `ContextualBar.extractRenderState` | yes | always recorded; empty in `ContextualBar.EMPTY`, `ExperienceBar` and `JumpableVehicleBar`, so `LocatorBar` is the only one of the four states that draws anything here |
| 17 | selected item name | `Hud.extractSelectedItemName` | yes | not a spectator, `Hud.toolHighlightTimer` above zero, and the stack is not empty |
| 17b | spectator action name | `SpectatorGui.extractAction` | yes | *else*: the game mode is spectator **and** the player is one — the same slot as row 17, and the second of the two places `SpectatorGui` replaces a `Hud` element |
| 18 | status effects | `Hud.extractEffects` | yes | the player has effects, no screen is showing them itself, and the instance sets `MobEffectInstance.showIcon` |
| 19 | boss bars | `BossHealthOverlay` | yes | the overlay has events |
| 20 | **sleep fade** | `Hud.extractSleepOverlay` | **no** | `Player.getSleepTimer` above zero — the one element between the two hidden-gated blocks |
| 21 | demo text | `Hud.extractDemoOverlay` | yes | `Minecraft.isDemo` |
| 22 | scoreboard sidebar | `Hud.displayScoreboardSidebar` | yes | a display objective for the team's colour slot, else for `DisplaySlot.SIDEBAR` |
| 23 | action bar | `Hud.extractOverlayMessage` | yes | `Hud.overlayMessageString` is set and its timer has not run out |
| 24 | title and subtitle | `Hud.extractTitle` | yes | `Hud.title` is set and `Hud.titleTime` is above zero |
| 25 | chat | `ChatComponent.extractRenderState` | yes | a player exists and the chat *screen* is not focused |
| 26 | tab list | `PlayerTabOverlay.extractRenderState` | yes | `Options.keyPlayerList` is down, and either this is not a local server, or more than one player is listed, or a `DisplaySlot.LIST` objective exists |
| 27 | subtitles | `SubtitleOverlay` | yes, with one exception | `Options.showSubtitles` is on, and a subtitle-carrying sound has played within its own range — a *distance* test, not a volume one, so a category muted to silence still puts its subtitle on screen. Deferred when there is no screen or the screen declares itself in-game UI, and recorded even while hidden if such a screen is up — which is the exception |

The four elements a reader expects at the end of that list are not on
`Hud.extractRenderState`'s list at all — three of them are still `Hud` methods,
and only the toasts are outside `Hud`. `Gui.extractRenderState` records them,
and the overlay or the screen goes in between:

| # | element | its own condition | hidden by F1? |
|---:|---|---|---|
| — | *the overlay, or else the screen* | an `Overlay` if there is one; otherwise, and only once resources are loaded, `Gui.screen` through `Screen.extractRenderStateWithTooltipAndSubtitles` — never both | — |
| 28 | saving indicator | `Options.showAutosaveIndicator` is on, the frame is drawing a level, and a save is still animating | **no** |
| 29 | toasts | resources are loaded | checks the flag itself |
| 30 | debug overlay | the current screen is not `DebugOptionsScreen` | checks the flag itself |
| 31 | deferred subtitles | row 27 deferred them — but only when no screen is up: a screen draws them itself from `Screen.extractBackground`, below its own widgets, and this call then finds nothing left | — |

---

*Rules: names, never code · how the system works, not how the code reads ·
newest version only · every backticked name passes `tools/verify_names.py`.*
