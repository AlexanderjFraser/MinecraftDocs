#!/usr/bin/env python3
"""Put the break in a lane name where the author wants it, not where mermaid would.

Pass 7, session A. The adopted theme wraps sequence messages at 180px so that lanes stay a
fixed distance apart and the type stays readable (mermaid-init.js has the numbers). The cost
is that mermaid hyphen-breaks any *word* wider than that width, and a lane's word is a class
name: `PersistentEntitySectio-nManager`, `ServerGamePacketLis-tenerImpl`. A hyphen inside a
Mojang name is a name the book gets wrong on screen, so every lane wider than the box carries
its own `<br/>` at a CamelCase (or nested-class dot) boundary instead.

This is the one-time sweep that put them in. It reads render/index.json — the render is the
authority on what actually broke, not a character count — and for each `participant X as Y`
whose Y mermaid hyphenated, splits Y at the boundaries that balance the lines best. It never
changes a name, only where its line ends; `check_lanes.py` and `check_figure_names.py` read a
lane expansion with the break closed up, so the gates see the name they always saw.

    python tools/pass7/break_lane_names.py --dry-run     # what it would change
    python tools/pass7/break_lane_names.py               # change it
    python tools/pass7/break_lane_names.py --probe       # prove it splits where it should

Re-run after a render if a part session adds a long lane; it is idempotent (a lane that
already carries a break is left alone).
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PARTICIPANT = re.compile(r"^(\s*(?:create\s+|destroy\s+)?(?:participant|actor)\s+[A-Za-z0-9_]+\s+as\s+)(.+?)(\s*)$")
# A boundary is the start of a CamelCase word or the character after a nested-class dot.
BOUNDARY = re.compile(r"(?<=[a-z0-9])(?=[A-Z])|(?<=\.)")


def split_name(name: str, target: int = 19, force: bool = False) -> str:
    """Break a class name at CamelCase (or nested-class dot) boundaries, halves first.

    The cut goes at the boundary nearest the middle, a dot preferred over a hump because a
    nested class reads as two names; each half that is still too wide is cut the same way.
    `force` cuts a name the render says broke even where the character count says it fits —
    the box is measured in glyphs, and `AdvancementRewards` is eighteen characters wide and
    still too wide for it."""
    if "<br" in name or (len(name) <= target and not force):
        return name
    cuts = [m.start() for m in BOUNDARY.finditer(name) if 0 < m.start() < len(name)]
    if not cuts:
        return name
    mid = len(name) / 2
    dots = [c for c in cuts if name[c - 1] == "."]
    best = min(dots or cuts, key=lambda c: abs(c - mid))
    left, right = name[:best], name[best:]
    return f"{split_name(left, target)}<br/>{split_name(right, target)}"


def broken_lanes(index: str) -> dict[str, set[str]]:
    """page slug -> the lane texts mermaid hyphenated, from a render."""
    with open(index, encoding="utf-8") as fh:
        data = json.load(fh)
    out: dict[str, set[str]] = {}
    for rec in data["records"]:
        page = rec.get("page")
        if not page:
            continue
        for t in rec.get("texts", []):
            if t["role"] == "participant" and t["text"].rstrip().endswith("-"):
                out.setdefault(page, set()).add(t["text"].rstrip().rstrip("-"))
    return out


def sweep(index: str, dry: bool) -> int:
    pages = broken_lanes(index)
    changed = 0
    for page, stubs in sorted(pages.items()):
        path = os.path.join(ROOT, page.replace("/", os.sep))
        if not os.path.exists(path):
            print(f"  missing: {page}", file=sys.stderr)
            continue
        with open(path, encoding="utf-8") as fh:
            lines = fh.readlines()
        hits = 0
        for i, line in enumerate(lines):
            m = PARTICIPANT.match(line.rstrip("\n"))
            if not m:
                continue
            name = m.group(2)
            if "<br" in name or " " in name:
                continue                     # a word lane, or already broken
            if not any(name.startswith(s) for s in stubs):
                continue                     # this lane rendered on one line
            new = split_name(name, force=True)
            if new == name:
                continue
            lines[i] = f"{m.group(1)}{new}\n"
            hits += 1
            print(f"  {page}:{i + 1}  {name} -> {new}")
        if hits and not dry:
            with open(path, "w", encoding="utf-8", newline="\n") as fh:
                fh.writelines(lines)
        changed += hits
    print(f"{changed} lane{'' if changed == 1 else 's'} broken at a CamelCase boundary"
          f"{' (dry run)' if dry else ''} on {len(pages)} pages")
    return changed


def probe() -> int:
    cases = [
        ("PersistentEntitySectionManager", "PersistentEntity<br/>SectionManager"),
        ("ServerGamePacketListenerImpl", "ServerGamePacket<br/>ListenerImpl"),
        ("ChunkMap.TrackedEntity", "ChunkMap.<br/>TrackedEntity"),
        ("EntityTickList", "EntityTickList"),                        # short enough: untouched
        ("PersistentEntity<br/>SectionManager", "PersistentEntity<br/>SectionManager"),  # idempotent
        ("TrackingDebugSynchronizer.SourceSynchronizer", "TrackingDebug<br/>Synchronizer.<br/>SourceSynchronizer"),
        ("ClientConfigurationPacketListenerImpl", "ClientConfiguration<br/>PacketListenerImpl"),
    ]
    ok = True
    for name, want in cases:
        got = split_name(name)
        good = got == want
        ok &= good
        print(f"{'pass' if good else 'FAIL'}  {name} -> {got}" + ("" if good else f"   (wanted {want})"))
    forced = split_name("AdvancementRewards", force=True)
    good = forced == "Advancement<br/>Rewards"
    ok &= good
    print(f"{'pass' if good else 'FAIL'}  a name the render says broke is cut even where the count says it fits: {forced}")
    joined = re.sub(r"<br\s*/?>", "", split_name("ServerGamePacketListenerImpl"))
    good = joined == "ServerGamePacketListenerImpl"
    ok &= good
    print(f"{'pass' if good else 'FAIL'}  the break closes up to the name the gates check")
    print("probe passed" if ok else "PROBE FAILED")
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--index", default=os.path.join(ROOT, "render", "index.json"))
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--probe", action="store_true")
    args = ap.parse_args()
    if args.probe:
        return probe()
    if not os.path.exists(args.index):
        print(f"no render at {args.index}: run `node tools/render_figures.js` first", file=sys.stderr)
        return 2
    sweep(args.index, args.dry_run)
    return 0


if __name__ == "__main__":
    sys.exit(main())
