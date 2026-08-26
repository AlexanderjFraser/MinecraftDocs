# MinecraftDocs

How Java Minecraft works — system-level documentation of the **current**
version (1.21.11), written as the notes for a video lecture series.

- One page per lecture; each follows one scenario through the system with a
  sequence diagram whose lanes are class names.
- **Names, never code.** Pages name classes and methods (Mojang's official
  names) and explain what they own and when they run; they never reproduce
  source. Decompile it yourself if you need the code.
- Newest version only. Every page says what it was verified against, and
  `tools/verify_names.py` proves every named identifier exists there.

[docs/outline.md](docs/outline.md) is the lecture map. [TEMPLATE.md](TEMPLATE.md)
is the page skeleton. Built with mdBook (`mdbook serve`).
