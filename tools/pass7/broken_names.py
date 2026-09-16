#!/usr/bin/env python3
"""Mojang names that mermaid hyphen-broke mid-word on screen, read off a render (pass 7, F18).

The theme wraps a label at 180px (a message) or 220px (a node), and mermaid hyphenates any word
wider than that — so a figure can spell `ServerGamePacketLis-tenerImpl` while the prose three feet
away spells it right. No gate sees it: the source parses, the name resolves, the label is the
right length. The render records every text run it drew (`render/index.json`, `records[].texts`),
so one regex finds them all. Session J's regex needed three letters before the hyphen; session M
found it blind to a break one or two letters after a dot (`SimpleCriterionTrigger.tr-igger`), so
this reads both shapes:

    a run ending `[A-Za-z]{3,}-` that is not `--`, or `[A-Za-z]\\.[A-Za-z]{1,2}-`

and ignores an English hyphen the label really has (`coast-or-interpolate`), which mermaid never
puts at the end of a run.

Usage:
    python tools/pass7/broken_names.py                    # every broken run in render/index.json
    python tools/pass7/broken_names.py --index render/candidate/index.json
    python tools/pass7/broken_names.py --pages systems/world
    python tools/pass7/broken_names.py --probe
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BROKEN = re.compile(r"(?:(?<!-)[A-Za-z]{3,}|[A-Za-z][.(][A-Za-z]{1,2})-$")


def broken_runs(text: str) -> list[str]:
    """The runs of one drawn label that end on mermaid's hyphen."""
    out = []
    for run in re.split(r"\s+", text.strip()):
        if run.endswith("--"):
            continue
        if BROKEN.search(run):
            out.append(run)
    return out


def scan(index: str, only: list[str] | None) -> list[tuple[str, str, str]]:
    with open(index, encoding="utf-8") as fh:
        data = json.load(fh)
    hits = []
    for r in data.get("records", []):
        if only and not any(o in r.get("page", "") for o in only):
            continue
        for t in r.get("texts", []):
            for run in broken_runs(t.get("text", "")):
                hits.append((r.get("id", "?"), run, t.get("text", "")))
    return hits


def probe() -> int:
    cases = [
        ("a long name broken three letters in", "ServerGamePacketLis- tenerImpl", True),
        ("a name broken two letters after a dot", "SimpleCriterionTrigger.tr- igger", True),
        ("a call broken one letter into its argument", "GameTestInstance.run(h- elper)", True),
        ("a name broken one letter after a dot", "Level.s- etBlock", True),
        ("an English hyphen inside a run", "coast-or-interpolate, then applyInput", False),
        ("a dotted arrow drawn as text", "A -- B", False),
        ("a dash as punctuation", "the wall - everything after", False),
        ("a clean name", "ServerGamePacketListenerImpl.handleUseItemOn", False),
    ]
    ok = True
    for what, text, want in cases:
        got = bool(broken_runs(text))
        ok &= got == want
        print(f"{'pass' if got == want else 'FAIL'}  {what} — {'is' if want else 'is not'} a broken name")
    print("probe passed" if ok else "PROBE FAILED")
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--index", default=os.path.join(ROOT, "render", "index.json"))
    ap.add_argument("--pages", nargs="*")
    ap.add_argument("--probe", action="store_true")
    args = ap.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if args.probe:
        return probe()
    hits = scan(args.index, args.pages)
    for fid, run, text in hits:
        print(f"{fid}: `{run}` in “{text[:90]}”")
    print(f"{len(hits)} names broken on screen")
    return 0


if __name__ == "__main__":
    sys.exit(main())
