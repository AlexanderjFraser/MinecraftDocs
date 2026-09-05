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

The work is in ten passes: a rough draft, an adversarial fact-check of
every claim, a restructuring pass and a second fact-check (all four done);
then four passes of restructuring and refinement with one lens each — the
book, the lecture, the figures, the voice (the book pass is running) — a third
fact-check, and a last polish, after which the site is finished. The owner
reads alongside. [docs/plan.md](docs/plan.md) is the roadmap (the passes,
the current pass's charter and schedule, the session log).
[TEMPLATE.md](TEMPLATE.md) is the page spec: the menu of shapes, the ownership
rule and the lane key. Built with mdBook
(`mdbook serve`); deployed by `tools/deploy.sh` to
[minecraftdocs.dev](https://minecraftdocs.dev).

## Corrections

Corrections are the contribution this project wants most. The pages are
written in passes and every claim is fact-checked against the decompile, but
passes 2 and 4 each found at least one wrong claim on every page, so there
are certainly more.

**Open an issue**, and cite the decompile — the class and method that show
the page is wrong. That is enough; the fix goes into the current pass.
Pull requests that change prose are not merged, however right they are:
nothing is published here that the owner has not read against the source
and understood well enough to say out loud on video, and a merged patch
skips that. Pull requests to `tools/` are welcome as normal.

## Licence

The book — everything in `src/`, its prose and its figures — is
[CC BY-SA 4.0](LICENSE): reuse it, adapt it, quote it, credit
[minecraftdocs.dev](https://minecraftdocs.dev), and keep derivatives under
the same licence. The tooling in [`tools/`](tools/) is [MIT](tools/LICENSE).

That covers the writing and the diagrams, which are the only things here
that are anyone's to license. It does not cover Minecraft: not the game,
not its source, not its assets, and not the Mojang mappings. Those are
Mojang's, this repo contains none of them, and the pages name identifiers
without reproducing code precisely because that is the line the mappings
licence draws.

## Not an official Mojang product

Unofficial and unaffiliated. This is an independent description of how the
game works, not endorsed by, sponsored by or associated with Mojang Studios
or Microsoft. "Minecraft" is a trademark of Mojang Synergies AB.
