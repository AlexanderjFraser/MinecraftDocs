# MinecraftDocs

How Java Minecraft works — system-level documentation of the **current**
version (26.2), written as the notes for a video lecture series.

- One page per lecture; each follows one scenario through the system, in
  the shape of its story (a trace, a state machine, a policy…), with a
  figure whose lanes are class names.
- **Names, never code.** Pages name classes and methods (Mojang's official
  names) and explain what they own and when they run; they never reproduce
  source. Decompile it yourself if you need the code.
- Newest version only. Every page says what it was verified against,
  `tools/verify_names.py` proves every named identifier exists there, and
  `tools/check_mermaid.js` proves every diagram renders.

The work is in passes: a rough draft, an adversarial fact-check of every
claim, a restructuring pass (current), a second fact-check, polish, and the
owner's own read. [docs/plan.md](docs/plan.md) is the roadmap (the passes,
the current pass's charter and schedule, the session log).
[TEMPLATE.md](TEMPLATE.md) is the page spec: the menu of shapes and the lane key. Built with mdBook
(`mdbook serve`); deployed by `tools/deploy.sh` to
[minecraftdocs.dev](https://minecraftdocs.dev).
