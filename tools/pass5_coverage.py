#!/usr/bin/env python3
"""The coverage question, once per part, asked with a tool: what in the part's
packages does no page mention?

Pass 5's charter (job 5) asks it with the atlas as the population. The population
is `map_source.PARTS` — the same package sets that write the landing pages' size
phrases, so the count a part claims and the classes it is judged against are one
mapping. For every class file in a part's packages (skipped packages excluded):

  in part      a page of the part names it in backticks (`Class` or `Class.member`)
  in book      any hand-kept page anywhere names it in backticks — a class owned by
               another part is not a gap, and the report says which page has it
  in a figure  the simple name appears only inside a mermaid block — a lane or a
               node label — which is a mention the reader sees and the verifier
               does not; counted separately, not as coverage
  unmentioned  nowhere in the book: the coverage gap, ranked by lines

The report per part: the counts; the unmentioned classes over --min-lines (default
80), largest first, with the sub-package and whether the server ships it; the
in-book-but-not-in-part classes, which are candidates for a cross-link or a move;
and the sub-packages with the most unmentioned lines, since a whole sub-package no
page names is the shape a missing section has. A class is a file; nested types
are not counted, which is the atlas's rule.

Usage:
    python tools/pass5_coverage.py --part world
    python tools/pass5_coverage.py --all --summary        # one row per part
    python tools/pass5_coverage.py --all --out DIR        # one <part>.coverage.md per part
"""
from __future__ import annotations

import argparse
import os
import re
import sys
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import map_source                  # noqa: E402
import pass4_queue as queue        # noqa: E402
from verify_names import TICK, GENERATED_MARK  # noqa: E402

SRC = queue.SRC
CLASS_TOKEN = re.compile(r"\b([A-Z][A-Za-z0-9]*[a-z][A-Za-z0-9]*)\b")


def page_names() -> tuple[dict, dict]:
    """(backticked simple class names per page key, mermaid-only class-shaped tokens per page key)."""
    ticks: dict[str, set] = {}
    figs: dict[str, set] = {}
    for key, (part, num, rel) in queue.corpus_pages().items():
        path = os.path.join(SRC, rel)
        with open(path, encoding="utf-8") as f:
            text = f.read()
        if GENERATED_MARK in text[:2000]:
            continue
        t = set()
        for m in TICK.finditer(text):
            name = m.group(1).rstrip("*").split("(")[0]
            if "/" in name:
                continue
            t.add(name.split(".")[0].split("$")[0])
        ticks[key] = t
        g = set()
        for block in re.findall(r"```mermaid\n(.*?)```", text, re.S):
            for tok in CLASS_TOKEN.findall(block):
                g.add(tok)
        figs[key] = g - t
    return ticks, figs


def report(files, part_dir: str, ticks: dict, figs: dict, min_lines: int, part_of: dict | None = None) -> tuple[str, dict]:
    spec = next(s for d, _n, _t, s in map_source.PARTS if d == part_dir)
    numeral, title = next((n, t) for d, n, t, _s in map_source.PARTS if d == part_dir)
    mine = map_source.part_files(files, spec)
    if part_of is None:
        part_of = {k: v[0] for k, v in queue.corpus_pages().items()}
    part_pages = [k for k in ticks if part_of.get(k) == part_dir]
    in_part = set().union(*(ticks[k] for k in part_pages)) if part_pages else set()
    in_part_fig = set().union(*(figs[k] for k in part_pages)) if part_pages else set()
    owner: dict[str, list[str]] = defaultdict(list)
    for k, names in ticks.items():
        for n in names:
            owner[n].append(k)
    fig_owner: dict[str, list[str]] = defaultdict(list)
    for k, names in figs.items():
        for n in names:
            fig_owner[n].append(k)

    rows = []
    for rel, text, shared in mine:
        simple = rel.rsplit("/", 1)[-1][:-5]
        if simple == "package-info":
            continue
        lines = text.count("\n")
        sub = rel.rsplit("/", 1)[0].replace("net/minecraft/", "")
        if simple in in_part:
            status = "part"
        elif simple in owner:
            status = "book"
        elif simple in in_part_fig or simple in fig_owner:
            status = "figure"
        else:
            status = "none"
        rows.append((lines, simple, sub, shared, status))
    rows.sort(key=lambda r: -r[0])
    total = sum(r[0] for r in rows)
    by = defaultdict(lambda: [0, 0])
    for lines, _s, _sub, _sh, status in rows:
        by[status][0] += 1
        by[status][1] += lines
    stats = {"part": part_dir, "numeral": numeral, "classes": len(rows), "lines": total,
             **{f"{k}_classes": by[k][0] for k in ("part", "book", "figure", "none")},
             **{f"{k}_lines": by[k][1] for k in ("part", "book", "figure", "none")}}

    out = [f"# Coverage — Part {numeral} · {title}", "",
           f"Population: {len(rows)} classes and {map_source.fmt(total)} lines in {map_source.spec_text(spec)} "
           f"(the atlas's `PARTS` mapping; skipped packages excluded). Pages read: {len(part_pages)}.", "",
           "| named on a page of the part | named on a page elsewhere in the book | named only inside a figure | named nowhere |",
           "|---:|---:|---:|---:|",
           f"| {by['part'][0]} classes, {map_source.fmt(by['part'][1])} lines | {by['book'][0]}, {map_source.fmt(by['book'][1])} | "
           f"{by['figure'][0]}, {map_source.fmt(by['figure'][1])} | **{by['none'][0]}, {map_source.fmt(by['none'][1])}** |", ""]
    pct = 100.0 * (by["part"][1] + by["book"][1]) / total if total else 0
    out.append(f"By lines, {pct:.0f}% of the part's code is named somewhere in the book. A class being named is not a "
               "class being explained; this is the floor, and the list below is what is under it.")
    out += ["", f"## Named nowhere in the book, {min_lines} lines and over, largest first", "",
            "| class | lines | package | ships in |", "|---|---:|---|---|"]
    none_rows = [r for r in rows if r[4] == "none" and r[0] >= min_lines]
    for lines, simple, sub, shared, _st in none_rows:
        out.append(f"| `{simple}` | {lines} | `{sub}` | {'both jars' if shared else 'client only'} |")
    if not none_rows:
        out.append("| (none) | | | |")
    small = [r for r in rows if r[4] == "none" and r[0] < min_lines]
    out.append("")
    out.append(f"{len(small)} more under {min_lines} lines, {map_source.fmt(sum(r[0] for r in small))} lines between them"
               + (": " + ", ".join(f"`{r[1]}`" for r in small[:40]) + (" …" if len(small) > 40 else "") if small else "."))

    out += ["", "## Sub-packages by unmentioned lines", "",
            "| package | classes | unmentioned | unmentioned lines | the largest unmentioned |", "|---|---:|---:|---:|---|"]
    subs = defaultdict(lambda: [0, 0, 0, []])
    for lines, simple, sub, _sh, status in rows:
        s = subs[sub]
        s[0] += 1
        if status == "none":
            s[1] += 1
            s[2] += lines
            s[3].append(simple)
    for sub, (n, un, ul, names) in sorted(subs.items(), key=lambda kv: -kv[1][2])[:25]:
        if un:
            out.append(f"| `{sub}` | {n} | {un} | {map_source.fmt(ul)} | {', '.join(f'`{x}`' for x in names[:5])} |")

    out += ["", "## In the part's packages, named only on pages of other parts", "",
            "A cross-link candidate (the part's page should point at the owner) or a move (the class is this part's "
            "and the other page should point here). The owner page is listed.", "",
            "| class | lines | package | named on |", "|---|---:|---|---|"]
    book_rows = [r for r in rows if r[4] == "book" and r[0] >= min_lines]
    for lines, simple, sub, _sh, _st in book_rows[:60]:
        out.append(f"| `{simple}` | {lines} | `{sub}` | {', '.join(f'`{k}`' for k in sorted(owner[simple])[:4])} |")
    if len(book_rows) > 60:
        out.append(f"| … {len(book_rows) - 60} more | | | |")

    fig_rows = [r for r in rows if r[4] == "figure" and r[0] >= 40]
    if fig_rows:
        out += ["", "## Named only inside a figure (a lane or a node label, never in prose)", "",
                ", ".join(f"`{r[1]}` ({r[0]})" for r in fig_rows[:40])]
    return "\n".join(out) + "\n", stats


def probe() -> int:
    """A class named in backticks on a page of the part is covered; one named on another part's page
    is 'named elsewhere' with its owner; one only in a figure is 'figure'; one named nowhere is the gap."""
    files = [
        ("net/minecraft/world/level/chunk/LevelChunk.java", "x\n" * 300, True),
        ("net/minecraft/world/level/chunk/PaletteResize.java", "x\n" * 120, True),
        ("net/minecraft/world/level/chunk/BulkSectionAccess.java", "x\n" * 90, True),
        ("net/minecraft/world/level/chunk/MissingPaletteEntryException.java", "x\n" * 200, True),
        ("net/minecraft/world/level/chunk/package-info.java", "x\n" * 4, True),
        ("net/minecraft/util/datafix/Old.java", "x\n" * 999, True),   # skipped package, never counted
    ]
    ticks = {"world/chunk-anatomy": {"LevelChunk"}, "blocks/blocks-and-states": {"PaletteResize"}}
    figs = {"world/chunk-anatomy": {"BulkSectionAccess"}, "blocks/blocks-and-states": set()}
    text, st = report(files, "world", ticks, figs, 80, {"world/chunk-anatomy": "world", "blocks/blocks-and-states": "blocks"})
    checks = [
        ("the population excludes the skipped package and package-info", st["classes"] == 4),
        ("LevelChunk is named in the part", st["part_classes"] == 1),
        ("PaletteResize is named elsewhere, owner listed", st["book_classes"] == 1 and "`blocks/blocks-and-states`" in text),
        ("BulkSectionAccess is figure-only", st["figure_classes"] == 1 and "BulkSectionAccess" in text.split("## Named only inside a figure")[-1]),
        ("MissingPaletteEntryException is the gap, listed with its lines", st["none_classes"] == 1
         and "| `MissingPaletteEntryException` | 200 |" in text),
    ]
    for name, ok in checks:
        print(f"  {'ok ' if ok else 'BAD'} {name}")
    if not all(ok for _n, ok in checks):
        print("PROBE FAILED")
        return 1
    print("probe: OK")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--probe", action="store_true", help="prove the tool on a synthetic part")
    ap.add_argument("--part", nargs="*", default=[], help="part directories under src/systems")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--summary", action="store_true", help="one row per part")
    ap.add_argument("--out", help="write one <part>.coverage.md per part here")
    ap.add_argument("--min-lines", type=int, default=80)
    args = ap.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    if args.probe:
        return probe()
    parts = [d for d, _n, _t, _s in map_source.PARTS] if args.all else args.part
    if not parts:
        ap.print_help()
        return 2
    files = map_source.load()
    ticks, figs = page_names()
    if args.out:
        os.makedirs(args.out, exist_ok=True)
    if args.summary:
        print("| part | classes | lines | named in part | named elsewhere | figure only | named nowhere | nowhere, lines | named by lines |")
        print("|---|---:|---:|---:|---:|---:|---:|---:|---:|")
    for d in parts:
        text, st = report(files, d, ticks, figs, args.min_lines)
        if args.summary:
            pct = 100.0 * (st["part_lines"] + st["book_lines"]) / st["lines"] if st["lines"] else 0
            print(f"| {st['numeral']} · {d} | {st['classes']} | {map_source.fmt(st['lines'])} | {st['part_classes']} | "
                  f"{st['book_classes']} | {st['figure_classes']} | **{st['none_classes']}** | {map_source.fmt(st['none_lines'])} | {pct:.0f}% |")
        elif args.out:
            with open(os.path.join(args.out, f"{d}.coverage.md"), "w", encoding="utf-8") as f:
                f.write(text)
            print(f"{st['none_classes']:4d} unmentioned classes, {map_source.fmt(st['none_lines']):>8} lines  {d}")
        else:
            print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
