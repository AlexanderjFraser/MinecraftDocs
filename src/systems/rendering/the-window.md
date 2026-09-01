# The window

> Verified against **Minecraft 26.2** · Part XI · before the first frame: a window is created, a backend is chosen against it, and every event the operating system will ever send arrives through six callbacks.

## Responsibility

Everything in *com/mojang/blaze3d/platform*: the GLFW window the game
lives in, the monitors and video modes it can occupy, the six callbacks
through which the operating system speaks to it, the clipboard and text
input, the cursor, the icon — and `NativeImage`, the CPU-side image
format that every texture, skin and screenshot passes through on its way
in or out.

Everything else in Part XI assumes this page has already happened.
[The frame](the-frame.md) begins with a surface that has already been
acquired; [input and keybinds](../client/input-and-keybinds.md) begins
with a callback that has already fired; [blaze3d](blaze3d.md) begins with
a `GpuDevice` that has already been created. All three of those start
here.

The one sentence a player would recognise: *dragging the window to the
other monitor, and pressing F11.*

The headline for a 1.21-era reader: **the window and the graphics backend
are created together, and neither can go first.** `Window`'s constructor
takes a `GpuBackend`, calls `GpuBackend.setWindowHints` before creating
the GLFW window and hands the failure to
`GpuBackend.handleWindowCreationErrors` if it does not appear — because
an OpenGL window and a Vulkan window need different hints. *Window.updateDisplay*
and *Window.setVsync* are gone; presentation is
[blaze3d](blaze3d.md)'s `GpuSurface` protocol now.

## The data it owns

- **`Window`** — the handle and everything hung off it. `Window.handle`,
  `Window.backend`, `Window.getWidth` / `Window.getHeight` (the
  framebuffer), `Window.getScreenWidth` / `Window.getScreenHeight` (the
  window, which differs under DPI scaling),
  `Window.getGuiScaledWidth` / `Window.getGuiScaledHeight` and
  `Window.setGuiScale` / `Window.calculateScale`, `Window.getX` /
  `Window.getY`, `Window.isFullscreen`, `Window.isFocused`,
  `Window.isIconified`, `Window.isMinimized`, `Window.getRefreshRate`,
  `Window.setTitle`, `Window.setIcon`, `Window.shouldClose`. The two
  base constants `Window.BASE_WIDTH` and `Window.BASE_HEIGHT` are what
  the GUI scale is computed against.
- **`DisplayData`** — the record the window is asked for: a size, an
  optional fullscreen size, and a fullscreen flag, with
  `DisplayData.withSize` and `DisplayData.withFullscreen` for the
  transitions.
- **`WindowEventHandler`** — a three-method interface
  (`WindowEventHandler.framebufferSizeChanged`,
  `WindowEventHandler.resizeGui`, `WindowEventHandler.cursorEntered`)
  that `Minecraft` implements. This is the whole of what the window is
  allowed to tell the game.
- **`MonitorManager`**, **`Monitor`**, **`VideoMode`** — monitor
  enumeration and mode negotiation. `Monitor` is a record of a name, a
  handle, its list of `VideoMode`s, the current one and its position;
  `Monitor.getPreferredVidMode` picks the closest match to a saved
  preference, and `MonitorManager.findBestMonitor` decides which monitor
  a window is "on" by overlap. `Window.getPreferredFullscreenVideoMode`,
  `Window.setPreferredFullscreenVideoMode`,
  `Window.changeFullscreenVideoMode`, `Window.toggleFullScreen`,
  `Window.setWindowed` and `Window.updateFullscreenIfChanged` are the
  transitions.
- **`NativeImage`** — the CPU-side image. A `NativeImage.Format`, a
  width, a height and a native pointer, with `NativeImage.read` (STB
  decode from a stream, a byte array or a NIO buffer),
  `NativeImage.writeToFile`, `NativeImage.getPixel` /
  `NativeImage.setPixel`, `NativeImage.copyRect`,
  `NativeImage.resizeSubRectTo`, `NativeImage.fillRect`,
  `NativeImage.mappedCopy`, `NativeImage.copyFromFont` (a FreeType face
  rasterised straight into it) and `NativeImage.computeTransparency` —
  which is the method [models and atlases](models-and-atlases.md) leans
  on to decide a quad's chunk layer.
- **`InputConstants`** — the key and mouse-button vocabulary that
  `KeyMapping` is written in. See
  [input and keybinds](../client/input-and-keybinds.md).
- **The small platform corners** — `ClipboardManager` and
  `TextInputManager` (copy, paste and IME text, both reached from
  `KeyboardHandler`), `CursorType` and `CursorTypes` with
  `Window.selectCursor` and `Window.setAllowCursorChanges`, `IconSet`,
  `MessageBox` (the native dialog shown when the game cannot start),
  `MacosUtil`, `GLX` (`GLX._initGlfw`, `GLX._getCpuInfo`,
  `GLX._getLWJGLVersion`, `GLX.getGlfwPlatform`),
  `NativeLibrariesBootstrap`, `DebugMemoryUntracker`,
  `FramerateLimitTracker` and `ClientShutdownWatchdog`.

## When it runs

Almost all of it at startup, on the main thread, before there is a game
to speak of: `GLX._initGlfw` initialises GLFW,
`NativeLibrariesBootstrap` probes for the GL and Vulkan loaders,
`MonitorManager` enumerates the monitors, and then `Minecraft` tries each
candidate `GpuBackend` in turn, constructing a `Window` against it until
one succeeds.

After that the window is touched in exactly two places per frame, both in
`Minecraft.renderFrame`: `Window.updateFullscreenIfChanged` at the very
top of the *update window* zone, and the surface reconfigure-and-acquire
immediately after it. Everything else is callback-driven.

`FramerateLimitTracker` is the one piece that runs continuously: it
watches focus and idle time and overrides the frame limit — down to ten
frames a second for an iconified or long-idle window, thirty for a short
idle, sixty in a menu with no level — which the frame then spends.

## The trace: the game gets a window

```mermaid
sequenceDiagram
    participant M as Minecraft
    participant GLX as GLX
    participant MM as MonitorManager
    participant B as GpuBackend
    participant W as Window
    participant RS as RenderSystem

    M->>GLX: _initGlfw — and a MessageBox if it fails
    M->>MM: enumerate monitors, each with its VideoModes
    loop over PreferredGraphicsApi.getBackendsToTry
        M->>B: setWindowHints — GL and Vulkan want different ones
        M->>W: new Window(handler, DisplayData, mode, title, monitors, backend)
        W->>W: createGlfwWindow; on failure, backend.handleWindowCreationErrors
        W->>W: register six callbacks: framebufferSize, pos, size, focus, cursorEnter, iconify
        M->>B: createDevice(handle, shader source, debug options)
        Note over M,B: first backend that survives both steps wins
    end
    M->>RS: initRenderer — device, sampler cache, dynamic uniforms
    M->>W: setIcon, setTitle, setDefaultErrorCallback
```

Two things in that trace are the point. First, **the loop encloses both
the window and the device**: a backend that cannot make a window and a
backend that cannot make a device fail the same way, and the next
candidate gets a fresh window. Second, **six callbacks is the entire
surface**. Framebuffer resize, window move, window resize, focus, cursor
enter and iconify — that is everything the operating system tells the
window, and only three of those reach the game at all, through
`WindowEventHandler`. Every *input* callback is registered elsewhere, by
`KeyboardHandler` and `MouseHandler`.

## Interfaces

- **Called by:** `Minecraft` at startup and twice per frame;
  `KeyboardHandler` and `MouseHandler` for the input callbacks and the
  clipboard; `VideoSettingsScreen` for the fullscreen and video-mode
  controls; `Screenshot` and `TextureManager` for `NativeImage`.
- **Calls into:** GLFW and STB, through LWJGL, and nothing else in the
  game. `Window` holds a `GpuBackend` but never a `GpuDevice`.
- **Crosses the network as:** nothing.
- **Data-driven by:** `Options` — the saved window size and position, the
  fullscreen flag and video-mode string, exclusive fullscreen, GUI scale,
  and the graphics-API preference.

## Invariants and surprises

- **The window is created once per backend attempt, not once.** A failed
  Vulkan device leaves a window behind that is destroyed before OpenGL is
  tried, because the window hints are already wrong for the second
  attempt.
- **There are three different "sizes" and the game uses all of them.**
  The framebuffer size is what the renderer targets, the screen size is
  what the operating system reports, and the GUI-scaled size is the
  framebuffer divided by an integer scale — which
  `Window.calculateScale` derives from the framebuffer against
  `Window.BASE_WIDTH` and `Window.BASE_HEIGHT`, with a floor when the
  font needs unicode. A high-DPI display makes the first two differ, and
  every misplaced GUI element is a confusion between them.
- **A minimized window still renders.** `Window.isMinimized` suppresses
  the surface acquisition, and the frame runs to completion regardless —
  see [the frame](the-frame.md). What actually saves the work is
  `FramerateLimitTracker` dropping the limit to ten.
- **The error callback is swapped three times over the game's life.**
  A boot-crash handler during startup, `Window.setDefaultErrorCallback`
  once running, and a null on close — and `Window.setErrorSection` tags
  whatever GLFW complains about with what the game was doing at the time.
- **`NativeImage` is the seam between "a file" and "a texture", and it
  is not only textures.** The same class decodes a PNG, receives a
  FreeType glyph bitmap, assembles an atlas, holds a downloaded skin
  while it is being validated, and receives a screenshot read back from
  the GPU. It is native memory with an explicit `NativeImage.close`, and
  `NativeImage.untrack` exists for the cases where something else takes
  ownership.
- **The cursor is a resource the game can lose.**
  `Window.setAllowCursorChanges` exists because a cursor change during a
  drag misbehaves on some platforms, and `CursorType.createStandardCursor`
  takes a fallback for the shapes a platform does not provide.
- **A shutdown that hangs is killed from outside.**
  `ClientShutdownWatchdog` starts a thread that will force the process
  down if the main thread does not finish stopping, and it waits a fixed
  grace period first so that a crash report still has time to be written.
- **Nothing here is server-side, and that is a rule rather than an
  observation.** `server-classes.txt` contains no entry under
  `com/mojang/blaze3d/` at all.
- **Names a 1.21-era reader will hunt for and not find:**
  *Window.updateDisplay* and *Window.setVsync* (presentation is
  `GpuSurface` now, and vsync is a `GpuSurface.PresentMode`),
  *Window.setupGuiState*, and *ScreenManager* — which never existed;
  monitor handling is `MonitorManager`.

## Where to look

`Window`'s constructor for the order in which a window and a backend come
into being, then `Window.updateFullscreenIfChanged` for the only thing
the window does per frame. `MonitorManager.findBestMonitor` and
`Monitor.getPreferredVidMode` for the fullscreen negotiation.
`NativeImage.read` and `NativeImage.computeTransparency` for the image
type the rest of Part XI is built on.

---

*Rules: names, never code · how the system works, not how the code reads ·
newest version only · every backticked name passes `tools/verify_names.py`.*
