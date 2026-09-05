# Pass 9 — the third fact-check (queue; opened 2026-09-05)

*Pass 9 re-runs pass 4's adversarial protocol — archived in
[pass4.md](pass4.md) with its charter, its agent brief
([pass4-brief.md](pass4-brief.md)) and its lessons — over the corpus passes
5–8 rewrite. This file is where every pass-5, -6, -7 and -8 session writes
down what pass 9 must check first: every page it rewrote, every claim a
rewrite introduced (a hook, a moved paragraph, a redrawn arrow, a re-scoped
count, a new section, a landing page's new argument), and every correction
it made with the decompile open. Pass 9 checks everything anyway; this list
decides what it checks first. It is also what made pass 4 checkable: from
Part VI on, the errors were in what the writing session did not know it had
changed, so a session lists what it changed on purpose and pass 9 reads the
rest harder.*

## How to write an entry

Per session, newest first, under `## Session X — Part N (pass M)`: the pages
rewritten; per page, one line per claim introduced, quoting the sentence;
the figures redrawn, and which orderings they assert; the material moved,
from where to where; and, under *Corrections*, every fact changed with the
decompile open — what the page said, what the decompile says, file and line.
Name the page in backticks on every line so a queue tool can route it.
Strike nothing here; pass 9 strikes.

## Standing items

- **A correction is a claim.** Pass 9 confirms the fix, not the original,
  and its close audits the pass's own strikes — session O of pass 4 found a
  strike that had settled nothing and a correction that was the error.
- **The summarisers are read last.** The thirteen landing pages,
  `lectures.md`, the glossary and the introduction are re-read after the
  pages they summarise are fixed, never before.
- **The figure against the section under it first**, before either is read
  against the source: nine pages in pass 4 had a diagram contradicting its
  own paragraph, and the prose was right every time.
- **Counts are call sites, not `grep -c` lines**; a generated page is
  checked by re-deriving the population, never a row.
- **Names inside mermaid blocks** are under a gate from pass 7's close; the
  23 ambiguous simple names the verifier prints are settled by pass 8 or in
  the tool.
- **Pass 9 adds nothing.** A gap it finds goes to [pass3.md](pass3.md) §7,
  the coverage queue, which seeds the second edition.

## Entries

*(pass-5 sessions append below, newest first)*

## Planning session — between passes 4 and 5 (2026-09-05)

No system page rewritten. Three claims introduced, all in the frame and the
atlas:

- `src/introduction.md` — the *Verified means tested* paragraph now says
  "every link and anchor between pages is checked to land" and "a page that
  fails any of those does not go up": the claim is that `tools/check_links.py`
  runs in `tools/deploy.sh` before the build and exits non-zero on a broken
  link, anchor, include, `SUMMARY.md` entry or redirect (`tools/deploy.sh`,
  the line after `check_deps.py`).
- `src/maps/packages.md` — the *Where each part lives* table is now
  `src/generated/parts.md`, written from `map_source.py`'s `PARTS`. The
  mapping is a set of claims about which packages each part covers, and it
  differs from the hand table it replaced: Part IV adds `world/level/material`,
  `world/attribute`, `world/timeline`, `world/clock`, `world/level/border`;
  Part VI adds `world/damagesource`, `world/effect` and subtracts
  `world/entity/player`; Part II adds `world/flag`; Part IX subtracts
  `network/syncher` (Part VI's); Part X adds `client/input`, `client/server`
  and counts `net/minecraft/client` itself only; Part XI adds
  `client/particle`; Part XIII adds `server/permissions`, `server/bossevents`
  and `client/gui/screens/dialog`. The paragraph above the table says how
  it is counted (no prefix, *itself only*, shared packages counted twice,
  skipped packages left out) — check each against `map_source.in_part`.
  Every landing page's size sentence will quote its row once the part
  sessions switch them to the include; until then a landing page's hand
  count and its row may differ (Part XIII: 473 / 43,900 by hand, 470 /
  43,126 by the atlas).
- `docs/pass5-brief.md` Part 4 — the measured tables (coverage per part, the
  queue by kind, the duplication pairs) are the tools' output on 2026-09-05
  and are claims about the corpus on that day, not about the game; pass 9
  need not check them.
