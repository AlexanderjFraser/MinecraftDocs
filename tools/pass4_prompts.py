#!/usr/bin/env python3
"""One prompt file per page for pass 4's fact-check agents.

Each file is the agent brief (Part 1 of `docs/pass4-brief.md`), then the
page's opening checklist from `docs/pass4.md` (`pass4_queue.py`), its
confident sentences by category (`claims.py`) and its diagrams as numbered
arrows (`diagram_arrows.py`). The part's page-less notes go to one
`_part-notes.md` for the session to route by hand. The agent's own prompt
is then one line: read this file and do what it says.

Usage:
    python tools/pass4_prompts.py --part world --out DIR
    python tools/pass4_prompts.py world/tickets-and-loading rendering/the-frame --out DIR
    python tools/pass4_prompts.py --part worldgen --out DIR --complete blending creating-a-world
`--part frame` covers the introduction, the lecture map and the atlas;
`--part reference` the hand-kept Reference pages (generated views are skipped).
"""
from __future__ import annotations

import argparse
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import claims                 # noqa: E402
import diagram_arrows         # noqa: E402
import pass4_queue as queue   # noqa: E402

ROOT = queue.ROOT
SRC = queue.SRC
BRIEF = os.path.join(ROOT, "docs", "pass4-brief.md")


def brief_part1() -> str:
    with open(BRIEF, encoding="utf-8") as f:
        text = f.read()
    m = re.search(r"^## Part 1 — The brief.*?(?=^---\s*$\s*^## Part 2)", text, re.M | re.S)
    if not m:
        sys.exit("docs/pass4-brief.md: could not find Part 1 (the brief) — is the heading intact?")
    return m.group(0).strip()


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pages", nargs="*", help="part/slug")
    ap.add_argument("--part", help="a part directory under src/systems, or frame, or reference")
    ap.add_argument("--out", required=True)
    ap.add_argument("--complete", nargs="*", default=[], help="slugs that also get the completeness question")
    ap.add_argument("--settled", action="store_true", help="include struck-through pass4.md lines")
    args = ap.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    pages = queue.corpus_pages()
    units, standing = queue.read_units()
    queue.attribute(units, pages)

    keys: list[str] = []
    for p in args.pages:
        p = re.sub(r"\.md$", "", re.sub(r"^(?:src/)?(?:systems/)?", "", p.replace("\\", "/")))
        if p not in pages:
            sys.exit(f"unknown page {p!r}")
        keys.append(p)
    if args.part:
        keys += [k for k, (part, _n, _p) in pages.items() if part == args.part]
    if not keys:
        ap.print_help()
        return 2

    os.makedirs(args.out, exist_ok=True)
    brief = brief_part1()
    part_nums = set()
    for key in keys:
        part, num, rel = pages[key]
        path = os.path.join(SRC, rel)
        if claims.is_generated(path):
            print(f"  skip (generated)      {key}")
            continue
        part_nums.add(num)
        slug = key.rsplit("/", 1)[-1]
        complete = slug in args.complete or key in args.complete
        mine, _partwide = queue.units_for_page(units, key, num, args.settled)
        rows = claims.scan(path, None)
        arrows, ndiag, narrow = diagram_arrows.render_page(path)

        out = [f"# Pass-4 fact-check — `src/{rel}`", "",
               f"The page to check is **`src/{rel}`** (repository root: `{ROOT}`).",
               f"Sources: `reference/26.2/` (decompile), `reference/26.2/data/` and `assets/`, `reference/libs/`.",
               ""]
        if complete:
            out += ["**This page also gets the completeness question** (step 9 of the brief): it has been "
                    "checked zero times, so report what is in its scope in the decompile that it never mentions.", ""]
        out += [brief, "", "---", "",
                queue.checklist(key, pages, units, standing, args.settled, with_partwide=False),
                "---", "",
                claims.render(path, rows, None), "",
                "---", "",
                arrows, ""]
        fname = os.path.join(args.out, f"{key.replace('/', '--')}.prompt.md")
        with open(fname, "w", encoding="utf-8") as f:
            f.write("\n".join(out))
        print(f"{len(mine):3d} notes {len(rows):4d} sentences {ndiag:2d} figures/{narrow:3d} arrows  {fname}")

    # the part-wide notes, once, for the session
    notes = []
    for num in sorted(part_nums):
        partwide = [u for u in units if not u.pages and u.owner is None and u.level >= 99
                    and num in (u.session_parts or (0,)) and (args.settled or not u.struck)]
        if partwide:
            notes.append(f"## Part {num or 'frame/reference'} — {len(partwide)} note(s) that name no page\n")
            notes += [queue.render(u) for u in partwide]
            notes.append("")
    with open(os.path.join(args.out, "_part-notes.md"), "w", encoding="utf-8") as f:
        f.write("# Notes from this part's pass-3 sessions that name no page — route each to a page, or to the landing page\n\n"
                + "\n".join(notes))
    print(f"\npart-wide notes → {os.path.join(args.out, '_part-notes.md')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
