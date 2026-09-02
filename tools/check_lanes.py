#!/usr/bin/env python3
"""Every sequence-diagram lane means one class, corpus-wide, and the key says which.

`TEMPLATE.md` carries the lane key (`| lane | class |` rows under "The lane
key"). This reads it and every `participant X as Y` / `actor X as Y` in
`src/**/*.md`, then checks:

  key      every class in the key exists in the decompile (nested classes as
           `Outer.Inner`), every lane is unique and at least two letters, and
           no lane is a bare initial  -> a failure exits 1
  pages    a lane the key knows must expand to the key's class on every page;
           a lane the key does not know must not mean two different classes
           on two pages  -> reported; exit 1 only with --strict

The page checks are report-only by default because the corpus is converted
part by part (pass 3): a part session runs `--strict --pages src/systems/<part>`
on its own pages, and session P turns `--strict` on corpus-wide.

Usage:
    python tools/check_lanes.py [--src src] [--template TEMPLATE.md] [--mc-source PATH] [--libs PATH]
    python tools/check_lanes.py --strict --pages src/systems/world src/systems/networking
    python tools/check_lanes.py --index        # also write src/reference/lanes.md (the key, for readers)
"""
from __future__ import annotations

import argparse
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from verify_names import load_index, members_of  # noqa: E402

KEY_ROW = re.compile(r"^\|\s*`([A-Za-z0-9_]+)`\s*\|\s*(.+?)\s*\|\s*$")
CLASS_CELL = re.compile(r"^`([A-Za-z_][A-Za-z0-9_.]*)`$")
PARTICIPANT = re.compile(r"^\s*(?:participant|actor)\s+([A-Za-z0-9_]+)(?:\s+as\s+(.+?))?\s*$")
WORD_LANE_MARK = "not a class"


def read_key(template: str) -> tuple[dict[str, str], set[str], list[str]]:
    """lane -> class for class lanes; the set of word lanes; problems found in the key itself."""
    classes: dict[str, str] = {}
    words: set[str] = set()
    problems: list[str] = []
    in_key = False
    with open(template, encoding="utf-8") as fh:
        for n, line in enumerate(fh, 1):
            if line.startswith("### The lane key"):
                in_key = True
                continue
            if in_key and line.startswith("#"):
                break
            if not in_key:
                continue
            m = KEY_ROW.match(line)
            if not m:
                continue
            lane, cell = m.group(1), m.group(2)
            if lane == "lane":
                continue
            if lane in classes or lane in words:
                problems.append(f"{template}:{n}: lane `{lane}` appears twice in the key")
            if len(lane) < 2:
                problems.append(f"{template}:{n}: lane `{lane}` is a single letter")
            cm = CLASS_CELL.match(cell)
            if cm:
                classes[lane] = cm.group(1)
            elif WORD_LANE_MARK in cell:
                words.add(lane)
            else:
                problems.append(f"{template}:{n}: lane `{lane}` is neither a backticked class nor marked '{WORD_LANE_MARK}'")
    if not classes:
        problems.append(f"{template}: no lane key found (expected rows under '### The lane key')")
    return classes, words, problems


def check_key_against_source(classes: dict[str, str], root: str, libs: str) -> list[str]:
    index, _packages = load_index(root, libs)
    problems = []
    cache: dict[str, set[str]] = {}
    for lane, name in classes.items():
        outer, _, inner = name.partition(".")
        if outer not in index:
            problems.append(f"key: `{lane}` -> `{name}`: no class {outer} in the decompile")
            continue
        if inner:
            if outer not in cache:
                cache[outer] = members_of(index[outer])
            missing = [seg for seg in inner.split(".") if seg not in cache[outer]]
            if missing:
                problems.append(f"key: `{lane}` -> `{name}`: no nested class {missing[0]} in {outer}")
    return problems


def _under(path: str, root: str) -> bool:
    """True if `path` is `root` or lies inside it. A plain startswith would put
    src/systems/worldgen inside src/systems/world."""
    p, r = os.path.abspath(path), os.path.abspath(root)
    return p == r or p.startswith(r + os.sep)


def walk_pages(src: str, only: list[str] | None):
    for dirpath, _dirs, files in os.walk(src):
        for f in files:
            if not f.endswith(".md"):
                continue
            path = os.path.join(dirpath, f)
            rel = os.path.relpath(path, src).replace(os.sep, "/")
            if only and not any(_under(path, o) for o in only):
                continue
            yield path, rel


def check_pages(src: str, classes: dict[str, str], words: set[str], only: list[str] | None):
    """Returns (mismatches with the key, collisions among unkeyed lanes, count of participants)."""
    mismatches: list[str] = []
    seen: dict[str, dict[str, set[str]]] = {}  # lane -> class -> pages
    count = 0
    for path, rel in walk_pages(src, only):
        with open(path, encoding="utf-8") as fh:
            for n, line in enumerate(fh, 1):
                m = PARTICIPANT.match(line)
                if not m:
                    continue
                lane, expansion = m.group(1), (m.group(2) or m.group(1)).strip()
                count += 1
                if lane in words:
                    continue
                if lane in classes:
                    if expansion != classes[lane]:
                        mismatches.append(f"{rel}:{n}: `{lane}` is `{expansion}` here, `{classes[lane]}` in the key")
                    continue
                seen.setdefault(lane, {}).setdefault(expansion, set()).add(rel)
    collisions = []
    for lane, by_class in sorted(seen.items()):
        if len(by_class) > 1:
            detail = "; ".join(f"`{cls}` in {', '.join(sorted(pages))}" for cls, pages in sorted(by_class.items()))
            collisions.append(f"unkeyed `{lane}` means {len(by_class)} things: {detail}")
    return mismatches, collisions, count


def write_index(path: str, classes: dict[str, str], words: set[str], template: str) -> None:
    out = [
        "# Diagram lanes",
        "",
        "Every lane in a sequence diagram is a class name abbreviated once for the whole",
        f"corpus. This is the key, generated from `{os.path.basename(template)}` by",
        "`python tools/check_lanes.py --index`; the initials of the class's CamelCase words,",
        "a one-word class as itself, and a few words for things that are not classes.",
        "",
        "| lane | class |",
        "|---|---|",
    ]
    for lane in sorted(classes, key=str.lower):
        out.append(f"| `{lane}` | `{classes[lane]}` |")
    for lane in sorted(words, key=str.lower):
        out.append(f"| `{lane}` | *{lane}: not a class* |")
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(out) + "\n")
    print(f"wrote {path}: {len(classes)} class lanes, {len(words)} word lanes")


def main() -> int:
    here = os.path.dirname(os.path.abspath(__file__))
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", default=os.path.join(here, "..", "src"))
    ap.add_argument("--template", default=os.path.join(here, "..", "TEMPLATE.md"))
    ap.add_argument("--mc-source", default=os.environ.get("MC_SOURCE", os.path.join(here, "..", "reference", "26.2")))
    ap.add_argument("--libs", default=os.environ.get("MC_LIBS", os.path.join(here, "..", "reference", "libs")))
    ap.add_argument("--pages", nargs="*", help="restrict the page checks to these files or directories")
    ap.add_argument("--strict", action="store_true", help="page mismatches and collisions fail, not just report")
    ap.add_argument("--index", action="store_true", help="write src/reference/lanes.md")
    args = ap.parse_args()

    classes, words, problems = read_key(args.template)
    problems += check_key_against_source(classes, args.mc_source, args.libs)
    if problems:
        print("\n".join(problems))
        print(f"\n{len(problems)} problems in the lane key")
        return 1
    print(f"lane key: {len(classes)} class lanes and {len(words)} word lanes, all resolve")

    mismatches, collisions, count = check_pages(args.src, classes, words, args.pages)
    for line in mismatches + collisions:
        print(line)
    scope = f" in {' '.join(args.pages)}" if args.pages else ""
    print(f"{count} participants{scope}: {len(mismatches)} disagree with the key, {len(collisions)} unkeyed lanes collide")
    if args.index:
        write_index(os.path.join(args.src, "reference", "lanes.md"), classes, words, args.template)
    if args.strict and (mismatches or collisions):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
