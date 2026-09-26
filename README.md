# MinecraftDocs

How Java Minecraft works — system-level documentation of the **current**
version, written as the notes for a video lecture series.

- One page per lecture; each follows one scenario through the system, in
  the shape of its story (a trace, a state machine, a policy…), with a
  figure whose lanes are class names.
- **Names, never code.** Pages name classes and methods (Mojang's official
  names) and explain what they own and when they run; they never reproduce
  source. Decompile it yourself if you need the code.
- Newest version only. Every page says what it was verified against, and
  six gates prove it before anything publishes: every named identifier exists
  in the decompile, in the prose and inside every figure; every diagram
  parses; every lane means one thing; every internal link and anchor lands;
  and the landing pages, the sidebar, the lecture map and the dependency
  figure agree with each other.
- For agents, every page is also served as markdown at its `.md` address,
  `llms.txt` is the index and `llms-full.txt` is the whole book in one file.

The work is in eight passes: a rough draft, an adversarial fact-check of
every claim, a restructuring into a book and a second fact-check; then three
passes of refinement with one lens each — the book read across its pages, each
page read down as one lecture's notes, every figure looked at rendered (all
seven done); and the eighth, the release, which is running: the move to the
current game version, a third fact-check over the ledger of every claim the
refining passes introduced, a polish over the exact wording, and a tagged
release, after which the site is left stable. The owner reads alongside.
[docs/plan.md](docs/plan.md) is the roadmap (the passes, the current pass's
charter, the session log); [docs/pass8-brief.md](docs/pass8-brief.md) is the
current pass's brief and schedule. [TEMPLATE.md](TEMPLATE.md) is the page
spec: the menu of shapes, the ownership rule, the figure standard and the lane
key. Built with mdBook (`mdbook serve`); deployed by `tools/deploy.sh` to
[minecraftdocs.dev](https://minecraftdocs.dev).

## Corrections

Corrections are the contribution this project wants most. The pages are
written in passes and every claim is fact-checked against the decompile, but
the first two fact-checks each found at least one wrong claim on every page,
the pass that read the pages against *each other* found 171 more, the pass
that read each page alone found about two hundred, and the pass that looked
at the figures rendered found about 180 inside the pictures — so there are
certainly others.

**Open an issue** with the correction template, and cite the decompile — the
class and member, or the file and line, that show the page is wrong, in the
version the page names. That is enough; the fix goes into the current pass,
and after the release into the next version pass. A report without a location
in the source is answered with a request for one, not investigated. Pull
requests that change prose are not merged, however right they are: nothing is
published here that the owner has not read against the source and understood
well enough to say out loud on video, and a merged patch skips that. Pull
requests to `tools/` are welcome as normal.

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
