#!/usr/bin/env python3
"""One prompt file per page for pass 6's agents — the reader with nothing but the page — and one
session file per page beside it.

Pass 6's agent is a reader who has only the page (`docs/pass6-brief.md`, Part 1),
so its prompt file is the brief and the page's path and nothing else: no queue,
no measurements, no other pages. Everything the tools know about the page goes
to the *session* instead, in `<part>--<slug>.session.md`: the page's lecture-kind
queue entries (`pass5_queue.py --kind lecture`), its shape report and skeleton
twins (`pass6_shape.py`), and every page that links to it with the anchor it
uses (`check_links.py --inbound`), because a heading the session renames moves
an anchor. Per part, `_part-shape-<part>.md` carries the part's device table and
the landing page's report, and `_part-notes.md` the part-wide queue entries that
name no page. The agent's own prompt is then one line: read this file and do
what it says.

Usage:
    python tools/pass6_prompts.py --part world --out DIR
    python tools/pass6_prompts.py world/lighting blocks/block-entities --out DIR
`--part frame` covers the introduction, the lecture map and the atlas prose;
`--part reference` the hand-kept Reference pages (generated views are skipped).
Those pages get the brief and their queue entries; the shape report is for
system pages, which are the pages with a shape.
"""
from __future__ import annotations

import argparse
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check_links                  # noqa: E402
import claims                       # noqa: E402
import pass5_queue as p5q           # noqa: E402
import pass6_shape as shape         # noqa: E402

ROOT = shape.ROOT
SRC = shape.SRC
BRIEF = os.path.join(ROOT, "docs", "pass6-brief.md")


def brief_part1() -> str:
    with open(BRIEF, encoding="utf-8") as f:
        text = f.read()
    m = re.search(r"^## Part 1 — The brief.*?(?=^---\s*$\s*^## Part 2)", text, re.M | re.S)
    if not m:
        sys.exit("docs/pass6-brief.md: could not find Part 1 (the brief) — is the heading intact?")
    return m.group(0).strip()


def inbound_md(rel: str) -> str:
    rows = check_links.inbound(rel)
    if not rows:
        return "## Inbound links\n\n- (no page links here)\n"
    by_anchor: dict[str, list] = {}
    for prel, n, a, _s in rows:
        by_anchor.setdefault(a or "(the page top)", []).append(f"`{prel}`:{n}")
    out = [f"## {len(rows)} inbound links from {len({r[0] for r in rows})} pages, by the anchor they land on", "",
           "A heading this session renames moves its anchor; `check_links.py` fails on the break, and every link "
           "below that lands on the renamed section is updated in the same commit.", ""]
    for a, refs in sorted(by_anchor.items(), key=lambda kv: (-len(kv[1]), kv[0])):
        out.append(f"- `#{a}` ← " + ", ".join(refs) if a != "(the page top)" else f"- the page top ← " + ", ".join(refs))
    return "\n".join(out) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pages", nargs="*", help="part/slug")
    ap.add_argument("--part", help="a part directory under src/systems, or frame, or reference")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    pages, units, standing, kinds = p5q.load()
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
    parsed = {k: shape.parse(k, pages) for k in shape.system_pages(pages)}
    part_dirs, part_nums = set(), set()
    for key in keys:
        part, num, rel = pages[key]
        path = os.path.join(SRC, rel)
        if claims.is_generated(path):
            print(f"  skip (generated)      {key}")
            continue
        part_dirs.add(part)
        part_nums.add(num)
        is_landing = rel.endswith("README.md")
        # the reader's file: the brief and the path, nothing else
        prompt = [f"# Pass-6 read — `src/{rel}`", "",
                  f"The page to read is **`src/{rel}`** (repository root: `{ROOT}`). Read it and nothing else.",
                  "", brief, ""]
        fname = os.path.join(args.out, f"{key.replace('/', '--')}.prompt.md")
        with open(fname, "w", encoding="utf-8") as f:
            f.write("\n".join(prompt))
        # the session's file: what the tools know
        mine, _pw = p5q.units_for(units, kinds, key, num, "lecture", False)
        sess = [f"# Pass-6 session notes — `src/{rel}`", "",
                "For the session, not the reader: the queue, the measurements and the links. The reader's report arrives "
                f"beside this as `{key.replace('/', '--')}.report.md`.", "", "---", "",
                p5q.checklist(key, pages, units, kinds, "lecture", False), "---", ""]
        if key in parsed:
            sess += [shape.report_md(parsed[key]), "---", ""]
        elif is_landing and key in pages:
            sess += [shape.landing_md(shape.landing(key, pages)), "---", ""]
        sess.append(inbound_md(rel))
        sname = os.path.join(args.out, f"{key.replace('/', '--')}.session.md")
        with open(sname, "w", encoding="utf-8") as f:
            f.write("\n".join(sess))
        n_in = len(check_links.inbound(rel))
        print(f"{len(mine):3d} queue {n_in:3d} in  {fname}")

    # once per part: the device table with the landing page, and the part-wide queue entries
    for d in sorted(part_dirs):
        if d in ("frame", "reference"):
            continue
        text = shape.part_table_md(d, parsed, pages)
        lk = f"{d}/README"
        if lk in pages:
            text += "\n" + shape.landing_md(shape.landing(lk, pages))
        with open(os.path.join(args.out, f"_part-shape-{d}.md"), "w", encoding="utf-8") as f:
            f.write(text)
        print(f"\nshape → {os.path.join(args.out, f'_part-shape-{d}.md')}")
    notes = []
    for num in sorted(part_nums):
        _m, partwide = p5q.units_for(units, kinds, "", num, "lecture", False)
        if partwide:
            notes.append(f"## Part {num or 'frame/reference'} — {len(partwide)} entr{'y' if len(partwide) == 1 else 'ies'} naming no page\n")
            notes += [p5q.render(u, kinds) for u in partwide]
            notes.append("")
    with open(os.path.join(args.out, "_part-notes.md"), "w", encoding="utf-8") as f:
        f.write("# Pass-6 queue entries from this part's sessions that name no page — route each to a page, or to the landing page\n\n"
                + "\n".join(notes))
    print(f"part-wide notes → {os.path.join(args.out, '_part-notes.md')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
