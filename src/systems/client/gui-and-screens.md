# GUI and screens

> Verified against **Minecraft 26.2** · Part X · pressing E: a screen that the server is never told about, recorded once and drawn once.

## Responsibility

Everything drawn in two dimensions that is not the HUD: menus, container
screens, widgets, layouts, tooltips, and the text engine underneath all
of it. This page is the screen lifecycle, the two-phase render model that
replaced immediate-mode drawing, and how a `Component` becomes glyphs.

The one sentence a player would recognise: *opening your inventory.*

The headline for a 1.21-era reader: **there is no *GuiGraphics*.** The
class is `GuiGraphicsExtractor`, and it draws nothing — every call
appends a *render state* to a tree, and `GuiRenderer` sorts, batches and
draws that tree later in the same frame. The old *Screen.render* is now
`Screen.extractRenderState`. And `Minecraft.screen` is gone: the current
screen belongs to `Gui`.

## The data it owns

### The screen manager

`Gui` owns `Gui.screen` (through `Gui.screen` / `Gui.setScreen`),
`Gui.overlay`, `Gui.hud`, `Gui.toastManager`, `Gui.chatListener`,
`Gui.splashManager` and the one `Gui.guiRenderState`. Its two per-frame
verbs are `Gui.tick` and `Gui.extractRenderState`;
`Gui.handleKeybinds` and `Gui.isPausing` are the rest of its surface.
`Minecraft.setScreenAndShow` survives as a wrapper.

### Screens and widgets

`Screen` holds `Screen.children`, `Screen.renderables`,
`Screen.narratables`, `Screen.width`, `Screen.height` and
`Screen.narrationState`. Its lifecycle is `Screen.init` (final, calling
the overridable `Screen.init` hook or `Screen.repositionElements`),
`Screen.rebuildWidgets`, `Screen.added`, `Screen.tick`, `Screen.removed`
and `Screen.onClose`; widgets are registered with
`Screen.addRenderableWidget` and friends. Its render entry point is the
final `Screen.extractRenderStateWithTooltipAndSubtitles`.

`Renderable` has exactly one method,
`Renderable.extractRenderState`. `AbstractWidget` implements it as final
and hands subclasses `AbstractWidget.extractWidgetRenderState`; the same
final-wrapper pattern governs `AbstractButton.extractContents`,
`AbstractWidget.updateNarration` and `AbstractContainerScreen.containerTick`.
The widget family is `Button`, `EditBox`, `Checkbox`,
`AbstractSelectionList`, `ObjectSelectionList`, `Tooltip`,
`MultiLineLabel` and the rest.

Layout is `Layout` over `LayoutElement`: `LinearLayout`, `GridLayout`,
`FrameLayout`, `EqualSpacingLayout`, `HeaderAndFooterLayout`,
`SpacerElement`, configured by `LayoutSettings` and resolved by
`Layout.arrangeElements` and `Layout.visitWidgets`.

Input arrives as records — `KeyEvent`, `MouseButtonEvent`,
`CharacterEvent`, `PreeditEvent` — through `GuiEventListener` and
`ContainerEventHandler`, with focus expressed as a `ComponentPath` and
moved by a `FocusNavigationEvent`. Geometry is `ScreenRectangle`,
`ScreenPosition`, `ScreenAxis`, `ScreenDirection`.

### The render state tree

`GuiRenderState` is a list of *strata*, each a chain of
`GuiRenderState.Node`. The recording verbs are
`GuiRenderState.addGuiElement`, `.addText`, `.addItem`,
`.addPicturesInPictureState`, `.addBlitToCurrentLayer` and
`.addGlyphToCurrentLayer`; the structural ones are
`GuiRenderState.nextStratum` and `GuiRenderState.blurBeforeThisStratum`.
The states themselves are `BlitRenderState`, `TiledBlitRenderState`,
`ColoredRectangleRenderState`, `GuiTextRenderState`, `GlyphRenderState`,
`GuiItemRenderState` and the `PictureInPictureRenderState` family
(`GuiEntityRenderState`, `GuiSkinRenderState`, `GuiBookModelRenderState`,
`GuiBannerResultRenderState`, `GuiProfilerChartRenderState`).

`GuiRenderer` owns the draw side: `GuiRenderer.prepare`,
`GuiRenderer.draw`, `GuiRenderer.endFrame`, the `GuiRenderer.Draw` list,
a `GuiItemAtlas`, the picture-in-picture renderers, and the sort
comparators `GuiRenderer.ELEMENT_SORT_COMPARATOR`,
`GuiRenderer.SCISSOR_COMPARATOR` and `GuiRenderer.TEXTURE_COMPARATOR`.

### Text

`Font` prepares; it cannot draw. `Font.prepareText` produces a
`Font.PreparedText` that is walked with a `Font.GlyphVisitor`;
`Font.width`, `Font.split` and `Font.getSplitter` are the measuring API,
and `Font.bidirectionalShaping` the reordering one. Glyphs come from a
`GlyphSource` per `FontDescription`, resolved by `FontManager` into a
`FontSet`, stitched into a `FontTexture` by `GlyphStitcher`, and rendered
as a `TextRenderable`. `StringSplitter`, `FormattedCharSequence` and
`SubStringSource` do the line-breaking and bidi work.

### Container screens

`AbstractContainerScreen` holds `AbstractContainerScreen.menu`,
`AbstractContainerScreen.leftPos`, `.topPos`, `.hoveredSlot` and the
quick-craft state. Its extract chain is
`AbstractContainerScreen.extractContents` →
`AbstractContainerScreen.extractLabels` →
`AbstractContainerScreen.extractSlots` →
`AbstractContainerScreen.extractCarriedItem` →
`AbstractContainerScreen.extractTooltip`, and a click
goes `AbstractContainerScreen.slotClicked` →
`MultiPlayerGameMode.handleContainerInput` — see
[containers and menus](../items/containers-and-menus.md) for what happens
next. `MenuScreens` maps a `MenuType` to a screen class;
`InventoryScreen` and its `EffectsInInventory` helper are the survival
inventory.

## When it runs

Two phases, one thread, one `Minecraft.runTick`. It is a *data* split,
not a thread split: the recording phase touches game state, the drawing
phase touches only the recorded objects and the GPU.

**Record.** `Gui.extractRenderState` resets the state tree, builds a
fresh `GuiGraphicsExtractor` for the frame, and calls the contributors in
a fixed order: the HUD, then the overlay *or* the screen, then the saving
indicator, then toasts, then the debug overlay, then deferred subtitles.
Toasts and the debug overlay are therefore always on top of a screen.

**Resolve and draw.** `GuiRenderer.render` runs
`GuiRenderer.preparePictureInPicture` (3D content rendered to textures
and blitted back), `GuiRenderer.prepareItemElements` (items rendered into
a dynamic atlas), `GuiRenderer.prepareText` (prepared text expanded to
per-glyph states), then sorts each node's elements and coalesces them
into as few draws as possible.

## The trace: pressing E

```mermaid
sequenceDiagram
    participant KH as KeyboardHandler
    participant KM as KeyMapping
    participant M as Minecraft
    participant G as Gui
    participant IS as InventoryScreen
    participant GGE as GuiGraphicsExtractor
    participant GRS as GuiRenderState
    participant GR as GuiRenderer

    KH->>KM: click — no screen is open, so it is a game input
    Note over M: next client tick
    M->>M: handleKeybinds — consumeClick on the inventory key
    M->>M: isServerControlledInventory? false for a player on foot
    M->>G: setScreen(new InventoryScreen(player))
    Note over IS: the menu is Player.inventoryMenu, which already existed
    G->>IS: added, then Screen.init(width, height)
    IS->>IS: init — leftPos/topPos centred, recipe-book button placed
    Note over G: next frame, record
    G->>IS: extractRenderStateWithTooltipAndSubtitles
    IS->>GGE: extractBackground — gradient, the inventory texture, the player model
    IS->>GGE: extractContents — labels, slots, hovered highlight
    GGE->>GRS: every call appends a state; nothing is drawn
    IS->>GGE: extractCarriedItem, then the deferred tooltip, each in its own stratum
    Note over GR: same frame, draw
    G->>GR: render — pictures-in-picture, item atlas, glyphs, sort, batch, draw
```

The point of the trace: **the survival inventory is entirely client-side
and no packet is sent to open it.** `Player.inventoryMenu` has existed
since the player was constructed, it has no `MenuType`, and
`MenuScreens` could never produce an `InventoryScreen` from a server
packet. The one exception is riding a mount with its own inventory, which
does take a server round trip. Slot *clicks* are a different matter, and
belong to Part VII.

## Interfaces

- **Called by:** `GameRenderer.extract` and `GameRenderer.render` — see
  [the frame](the-frame.md).
- **Calls into:** [blaze3d](blaze3d.md) for the draws;
  `ItemModelResolver` for item icons — see
  [models and atlases](models-and-atlases.md); the entity render pipeline
  for the player model in the inventory.
- **Crosses the network as:** `ServerboundContainerClickPacket` and
  `ServerboundContainerClosePacket` from container screens (Part VII);
  `ClientboundOpenScreenPacket` opens everything *except* the survival
  inventory.
- **Data-driven by:** *font/* definitions and the GUI atlas from resource
  packs; `Options.guiScale` and the narrator settings.

## Invariants and surprises

- **Nothing in a screen draws.** Every method on
  `GuiGraphicsExtractor` appends a state object that captures a *copy* of
  the current transform and scissor, so pushing and popping afterwards
  cannot disturb it.
- **Layering is inferred from bounding boxes, not from a Z value.** A new
  element is placed above the highest existing element whose bounds it
  intersects; elements that do not overlap may share a node and be
  reordered freely by the batching sort. `GuiRenderState.nextStratum` is
  the only hard barrier, and it is what container screens use before
  drawing the cursor-held item.
- **An element with no bounds is silently discarded** — which is exactly
  why glyphs, whose bounds are deliberately null, must be added through
  the layer-bypassing verb and are emitted after their node's geometry.
- **Items are drawn through a dynamic GPU atlas.** Each distinct item
  model is rendered once per frame into `GuiItemAtlas` and then blitted
  like any other sprite, so a chest full of identical stacks costs one 3D
  render. Changing the GUI scale throws the atlas away, and an atlas that
  cannot grow logs that some items will be skipped.
- **`Screen.init` runs again on every resize and GUI-scale change.**
  Every widget object is discarded and rebuilt, so anything that must
  survive a resize has to live in a field.
- **Tooltips are deferred to the end of the frame** and drawn in their
  own stratum, which is why they are always above the screen that asked
  for them.
- **Blur is a once-per-frame stratum boundary**, implemented by splitting
  the draw list, clearing depth and running a post effect in between. A
  second request in one frame throws. Container screens are never
  blurred — they take the transparent-background path.
- **The framework fixes the outer shape.** `Screen.init`,
  `AbstractWidget.extractRenderState`,
  `AbstractButton.extractWidgetRenderState`,
  `AbstractWidget.updateNarration` and `AbstractContainerScreen.tick` are
  all final, each handing the subclass one inner hook.
- **`Font` cannot draw anything.** A `Component` becomes glyphs in four
  steps: visual-order reordering for bidi, a `FormattedCharSequence`, a
  `Font.PreparedText` built per codepoint with advances and bold and
  shadow offsets, and finally per-glyph render states produced a phase
  later by `GuiRenderer`.
- **There are debug switches for exactly the failure modes above.** One
  draws a rectangle per layer; another shuffles each node's element list
  and re-seeds the sort keys, to shake out accidental order dependence.
- **Names a 1.21-era reader will hunt for and not find:**
  *GuiGraphics* (now `GuiGraphicsExtractor`), *Font.drawInBatch* and
  every *drawString* variant, *Screen.render* and *renderBackground* and
  *renderDirtBackground*, *AbstractContainerScreen.renderBg* /
  *renderLabels* / *renderSlot*, *AbstractWidget.renderWidget*,
  *GuiGraphics.renderTooltip*, *ClickType* (now `ContainerInput`),
  *MultiPlayerGameMode.handleInventoryMouseClick* (now
  `MultiPlayerGameMode.handleContainerInput`), *Minecraft.screen* and
  *setScreen*, and `PoseStack` in GUI code — the GUI transform is now a
  2D affine stack. `MultiLineLabel`, `MenuScreens`, `ComponentPath`,
  `ScreenRectangle` and all the layout classes survive.

## Where to look

`Gui.extractRenderState` for the frame's contributor order, then
`Screen.extractRenderStateWithTooltipAndSubtitles` for a screen's.
`GuiRenderState.nextStratum` and the node-placement logic for how
layering is decided. `GuiRenderer.prepare` for where items, text and
picture-in-picture content are resolved. `Font.prepareText` for the text
engine, and `AbstractContainerScreen.extractContents` for the busiest
screen in the game.

---

*Rules: names, never code · how the system works, not how the code reads ·
newest version only · every backticked name passes `tools/verify_names.py`.*
