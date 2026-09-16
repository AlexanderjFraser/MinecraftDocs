#!/usr/bin/env python3
"""Every figure caption in the book, as pass 9's checklist (pass 7, session O).

A caption is a claim about what its figure shows (F5), and pass 7's sessions wrote about two
hundred of them. Most session entries in docs/pass9.md say the captions are claims without listing
them, so this lists them from the pages: for every ```mermaid block and every `<figure class="map">`,
its number on the page, the page line, and the caption — the italic paragraph directly after the
figure (or the <figcaption> of a generated one). A figure with no caption is listed too, as
*(none)*, because that is also something pass 9 should see.

Usage:
    python tools/pass7/captions.py                       # the whole book, as markdown
    python tools/pass7/captions.py src/systems/world     # a part or a page
    python tools/pass7/captions.py --missing             # only the figures with no caption
    python tools/pass7/captions.py --probe
"""
from __future__ import annotations

import argparse
import os
import re
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FENCE = re.compile(r"^\s*(`{3,}|~{3,})\s*(\w*)\s*$")
FIGCAPTION = re.compile(r"<figcaption>(.*?)</figcaption>", re.S)


def figures(path: str):
    """(number, line, kind, caption or None) for each figure on a page, in order."""
    lines = open(path, encoding="utf-8").read().split("\n")
    out, i, n = [], 0, len(lines)
    while i < n:
        m = FENCE.match(lines[i])
        if m and m.group(2):
            kind, start = m.group(2), i + 1
            i += 1
            while i < n and not (FENCE.match(lines[i]) and not FENCE.match(lines[i]).group(2)):
                i += 1
            if kind == "mermaid":
                j = i + 1
                while j < n and not lines[j].strip():
                    j += 1
                para = []
                while j < n and lines[j].strip():
                    para.append(lines[j].strip())
                    j += 1
                text = " ".join(para)
                bare = re.sub(r"\*\*[^*]+\*\*", "", re.sub(r"`[^`]*`", "", text))   # a code span or bold inside the run
                cap = text if bare.startswith("*") and bare.endswith("*") and bare.count("*") == 2 else None
                out.append((len(out) + 1, start, "mermaid", cap))
        elif '<figure class="map">' in lines[i]:
            start, block = i + 1, []
            while i < n and "</figure>" not in lines[i]:
                block.append(lines[i])
                i += 1
            block.append(lines[i] if i < n else "")
            cm = FIGCAPTION.search("\n".join(block))
            out.append((len(out) + 1, start, "map", " ".join(cm.group(1).split()) if cm else None))
        i += 1
    return out


def walk(targets: list[str]):
    for t in targets:
        if os.path.isfile(t):
            yield t
            continue
        for dirpath, _d, files in os.walk(t):
            for f in sorted(files):
                p = os.path.join(dirpath, f)
                rel = os.path.relpath(p, os.path.join(ROOT, "src")).replace(os.sep, "/")
                if f.endswith(".md") and not rel.startswith(("generated/", "figures/")):
                    yield p


def probe() -> int:
    page = """# P

```mermaid
flowchart TD
    A --> B
```

*The one italic run, with a `Name` inside it.*

```mermaid
flowchart TD
    C --> D
```

A plain paragraph is not a caption.

<figure class="map">
<svg></svg>
<figcaption>The map's own caption.</figcaption>
</figure>

```mermaid
flowchart TD
    E --> F
```

*Two runs* and `a name` *outside them.*
"""
    d = tempfile.mkdtemp()
    p = os.path.join(d, "p.md")
    open(p, "w", encoding="utf-8").write(page)
    got = figures(p)
    checks = [
        ("four figures, numbered in order", [g[0] for g in got] == [1, 2, 3, 4]),
        ("a one-run caption is read", got[0][3] == "*The one italic run, with a `Name` inside it.*"),
        ("a plain paragraph is no caption", got[1][3] is None),
        ("a generated figure's figcaption is read", got[2][2] == "map" and got[2][3] == "The map's own caption."),
        ("a paragraph that is not one italic run is no caption", got[3][3] is None),
    ]
    ok = all(c for _w, c in checks)
    for w, c in checks:
        print(f"{'pass' if c else 'FAIL'}  {w}")
    print("probe passed" if ok else "PROBE FAILED")
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("targets", nargs="*")
    ap.add_argument("--missing", action="store_true")
    ap.add_argument("--probe", action="store_true")
    args = ap.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if args.probe:
        return probe()
    total = missing = 0
    for p in walk(args.targets or [os.path.join(ROOT, "src")]):
        rel = os.path.relpath(p, ROOT).replace(os.sep, "/")
        for num, line, kind, cap in figures(p):
            total += 1
            missing += cap is None
            if args.missing and cap is not None:
                continue
            print(f"- `{rel}`:{line} f{num} ({kind}) — {cap or '*(none)*'}")
    print(f"\n{total} figures, {total - missing} captioned, {missing} not")
    return 0


if __name__ == "__main__":
    sys.exit(main())
