#!/usr/bin/env python3
"""One prompt file per page for pass 7's agents — the viewer with the picture and the section — and one
session file per page beside it.

Pass 7's agent looks at each figure the way a reader does — rendered, at the column width, beside
the section it sits in — and answers the brief in `docs/pass7-brief.md` Part 1. Its prompt file is
the brief, the page's path, and for each figure its number, its line, the section it sits under and
the PNG `tools/render_figures.js` wrote for it; nothing else, because the measurements would tell
it what to see. Everything the tools know about the page goes to the *session* instead, in
`<part>--<slug>.session.md`: the page's figure-kind queue entries (`pass5_queue.py --kind figure`),
the page's figure report (`pass7_figures.py`: place, source, names, render, trouble), the name
gate's failures and notes for the page (`check_figure_names.py`), every figure arrow by arrow
(`diagram_arrows.py`, for re-deriving one against the decompile), the sections over forty lines with
no figure, and every inbound link by anchor (a section a session splits moves an anchor). Per part,
`_part-figures-<part>.md` carries the part's figure table and its ranking, and `_part-notes.md`
the part-wide queue entries that name no page. The agent's own prompt is then one line: read this
file and do what it says.

Run `node tools/render_figures.js` first (it writes render/index.json and the PNGs); a page whose
figures are not in the index gets its prompt without pictures and the session file says so.

Usage:
    python tools/pass7_prompts.py --part world --out DIR
    python tools/pass7_prompts.py world/lighting client/the-client-loop --out DIR
`--part frame` covers the introduction, the lecture map and the atlas prose; `--part reference`
the hand-kept Reference pages with a figure (and the four without one, which the queue names).
"""
from __future__ import annotations

import argparse
import io
import os
import re
import sys
from contextlib import redirect_stdout

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check_links                  # noqa: E402
import diagram_arrows as da         # noqa: E402
import pass5_queue as p5q           # noqa: E402
import pass7_figures as p7          # noqa: E402

ROOT = p7.ROOT
SRC = p7.SRC
BRIEF = os.path.join(ROOT, "docs", "pass7-brief.md")


def brief_part1() -> str:
    with open(BRIEF, encoding="utf-8") as f:
        text = f.read()
    m = re.search(r"^## Part 1 — The brief.*?(?=^---\s*$\s*^## Part 2)", text, re.M | re.S)
    if not m:
        sys.exit("docs/pass7-brief.md: could not find Part 1 (the brief) — is the heading intact?")
    return m.group(0).strip()


def inbound_md(rel: str) -> str:
    rows = check_links.inbound(rel)
    if not rows:
        return "## Inbound links\n\n- (no page links here)\n"
    by_anchor: dict[str, list] = {}
    for prel, n, a, _s in rows:
        by_anchor.setdefault(a or "(the page top)", []).append(f"`{prel}`:{n}")
    out = [f"## {len(rows)} inbound links from {len({r[0] for r in rows})} pages, by the anchor they land on", "",
           "A figure moved out of a section, or a section split around one, does not move an anchor; a heading "
           "renamed does, and `check_links.py` fails on the break.", ""]
    for a, refs in sorted(by_anchor.items(), key=lambda kv: (-len(kv[1]), kv[0])):
        out.append(f"- `#{a}` ← " + ", ".join(refs) if a != "(the page top)" else f"- the page top ← " + ", ".join(refs))
    return "\n".join(out) + "\n"


def gate_md(checker, path: str, rel: str) -> str:
    failures, notes = checker.check_page(path, rel)
    out = [f"## The name gate: {len(failures)} unresolved, {len(notes)} notes (`check_figure_names.py`)", ""]
    if failures:
        out.append("Unresolved — a name in a figure that is not in the decompile as written. Each is re-derived; a wrong arrow is a correction for pass9.md:")
        out.append("")
        out += [f"- L{ln}: `{tok}` — {why}" for _rel, ln, tok, why in failures]
        out.append("")
    if notes:
        out.append("Notes — not failures; session A's convention decides what they become:")
        out.append("")
        out += [f"- L{ln}: `{tok}` — {why}" for _rel, ln, tok, why in notes]
        out.append("")
    if not failures and not notes:
        out.append("- every name in every figure on this page resolves")
        out.append("")
    return "\n".join(out)


def arrows_md(path: str) -> str:
    text, _nd, _na = da.render_page(path)
    return "## Every figure, arrow by arrow (`diagram_arrows.py`) — the list to re-derive against the decompile\n\n" + \
        "\n".join(l for l in text.split("\n")[2:]) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pages", nargs="*", help="part/slug")
    ap.add_argument("--part", help="a part directory under src/systems, or frame, or reference")
    ap.add_argument("--out", required=True)
    ap.add_argument("--render", default=p7.RENDER_INDEX)
    args = ap.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    pages, units, standing, kinds = p5q.load()
    all_pages = p7.all_pages()
    by_key = {k: (part, rel) for k, part, rel in all_pages}
    keys: list[str] = []
    for p in args.pages:
        p = re.sub(r"\.md$", "", re.sub(r"^(?:src/)?(?:systems/)?", "", p.replace("\\", "/")))
        if p not in by_key:
            sys.exit(f"unknown page {p!r}")
        keys.append(p)
    if args.part:
        keys += [k for k, part, _rel in all_pages if part == args.part]
    if not keys:
        ap.print_help()
        return 2

    os.makedirs(args.out, exist_ok=True)
    brief = brief_part1()
    render = p7.load_render(args.render)
    meta = render.pop("_meta", None) if render else None
    if not render:
        print("warning: no render/index.json — prompts will carry no pictures; run `node tools/render_figures.js` first", file=sys.stderr)

    import check_figure_names as cfn
    checker = cfn.Checker(os.environ.get("MC_SOURCE", os.path.join(ROOT, "reference", "26.2")),
                          os.environ.get("MC_LIBS", os.path.join(ROOT, "reference", "libs")))

    reports = {}
    part_dirs, part_nums = set(), set()
    for key in keys:
        part, rel = by_key[key]
        path = os.path.join(SRC, rel)
        num = pages[key][1] if key in pages else None
        part_dirs.add(part)
        part_nums.add(num)
        rep = p7.figures_of(key, part, rel, render)
        reports[key] = rep
        figs = rep["figures"]
        # the viewer's file: the brief, the path, the figures and their pictures — nothing else
        lines = [f"# Pass-7 look — `src/{rel}`", "",
                 f"The page is **`src/{rel}`** (repository root: `{ROOT}`). It has {len(figs)} figure{'s' if len(figs) != 1 else ''}; "
                 "each is listed below with the line its source starts on, the section it sits in, and the picture of it as the "
                 "site shows it at the reading column's width. Look at the picture first, then read the page.", ""]
        if not figs:
            lines.append("- (this page has no figure — the brief's last question is the one to answer)")
        for f in figs:
            where = f"*{f['h2']}*" + (f" › *{f['h3']}*" if f["h3"] else "") if f["h2"] else "before the first heading"
            png = (f.get("render") or {}).get("png")
            what = f"{f['type']}" + (f" {f['direction']}" if f.get("direction") else "")
            lines.append(f"- **Figure {f['n']}** — {what}, source at line {f['line']}, under {where}. "
                         + (f"Picture: `{os.path.join(ROOT, png)}`" if png else "Picture: not rendered (judge it from the source, and say so)"))
        lines += ["", brief, ""]
        fname = os.path.join(args.out, f"{key.replace('/', '--')}.prompt.md")
        with open(fname, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        # the session's file: everything the tools know
        mine, _pw = p5q.units_for(units, kinds, key, num, "figure", False)
        sess = [f"# Pass-7 session notes — `src/{rel}`", "",
                "For the session, not the viewer: the queue, the measurements, the gate, the arrows and the links. The viewer's "
                f"report arrives beside this as `{key.replace('/', '--')}.report.md`.", "", "---", "",
                p5q.checklist(key, pages, units, kinds, "figure", False) if key in pages else "## Queue\n\n- (not a page the queue knows)\n",
                "---", "", p7.page_md(rep), "---", "", gate_md(checker, path, rel), "---", "", arrows_md(path), "---", "", inbound_md(rel)]
        sname = os.path.join(args.out, f"{key.replace('/', '--')}.session.md")
        with open(sname, "w", encoding="utf-8") as f:
            f.write("\n".join(sess))
        n_in = len(check_links.inbound(rel))
        print(f"{len(figs):2d} figures {len(mine):3d} queue {n_in:3d} in  {fname}")

    # once per part: the figure table and the ranking, and the part-wide queue entries
    for d in sorted(part_dirs):
        reps = [reports[k] for k in keys if by_key[k][0] == d]
        text = p7.part_table(reps, d) + "\n" + "## The part's figures by trouble, worst first\n\n" + p7.rank_md(reps, 100)
        if any(r["candidates"] for r in reps):
            text += "\n## Sections over forty lines with no figure, by the density of order/branch/cycle/containment words\n\n" + p7.candidates_md(reps)
        with open(os.path.join(args.out, f"_part-figures-{d}.md"), "w", encoding="utf-8") as f:
            f.write(text)
        print(f"\nfigures → {os.path.join(args.out, f'_part-figures-{d}.md')}")
    notes = []
    for num in sorted(n for n in part_nums if n is not None):
        _m, partwide = p5q.units_for(units, kinds, "", num, "figure", False)
        if partwide:
            notes.append(f"## Part {num or 'frame/reference'} — {len(partwide)} entr{'y' if len(partwide) == 1 else 'ies'} naming no page\n")
            notes += [p5q.render(u, kinds) for u in partwide]
            notes.append("")
    with open(os.path.join(args.out, "_part-notes.md"), "w", encoding="utf-8") as f:
        f.write("# Pass-7 queue entries from this part's sessions that name no page — route each to a figure, or strike it\n\n"
                + "\n".join(notes))
    print(f"part-wide notes → {os.path.join(args.out, '_part-notes.md')}")
    if meta:
        print(f"pictures from render/index.json generated {meta.get('generated')} at {meta.get('width')}px, theme {meta.get('theme')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
