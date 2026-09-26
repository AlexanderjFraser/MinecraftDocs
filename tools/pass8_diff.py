#!/usr/bin/env python3
"""Every sentence pass 8 changed, per page, read off git — the second reading's list.

Pass 8 polishes prose after it fact-checks it, and every sentence a pass touches is a claim (the
plan's standing rule, and pass 4's finding fifteen times over). The ledger carries the changes whose
meaning could have moved; the git history carries all of them. This lists the added or rewritten
lines under src/ since a ref — by default the tag `pass-8-start`, which the version session places
before it touches a page — grouped by page, joined into sentences, with the line each now starts on
in the page, so session P can read every one against the decompile without trusting anyone's list.
A changed line inside a mermaid block is listed as a figure line, not a sentence. Generated pages
are skipped.

Usage:
    python tools/pass8_diff.py                      # every changed sentence, by page
    python tools/pass8_diff.py --summary            # changed sentences and figure lines per page and per part
    python tools/pass8_diff.py --part world         # one part
    python tools/pass8_diff.py --ref pass-8-start~3 # another base
    python tools/pass8_diff.py --probe              # parses a canned diff
"""
from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pass8_queue as q8  # noqa: E402

ROOT = q8.HERE
HUNK = re.compile(r"^@@ -\d+(?:,\d+)? \+(\d+)(?:,(\d+))? @@")
FILE = re.compile(r"^\+\+\+ b/(.*)$")


def parse(diff: str) -> dict[str, list[tuple[int, str]]]:
    """path -> [(new line number, added line)]."""
    out, cur, n = defaultdict(list), None, 0
    for line in diff.splitlines():
        m = FILE.match(line)
        if m:
            cur = m.group(1)
            continue
        m = HUNK.match(line)
        if m:
            n = int(m.group(1))
            continue
        if cur is None:
            continue
        if line.startswith("+") and not line.startswith("+++"):
            out[cur].append((n, line[1:]))
            n += 1
        elif line.startswith("-") and not line.startswith("---"):
            continue
        else:
            n += 1
    return out


def in_fence(path: str, line_no: int) -> bool:
    """Whether a line of the file as it now stands is inside a code fence."""
    try:
        with open(os.path.join(ROOT, path), encoding="utf-8") as f:
            lines = f.read().splitlines()
    except OSError:
        return False
    fence = False
    for i, l in enumerate(lines[:line_no], 1):
        if l.strip().startswith("```") or l.strip().startswith("~~~"):
            fence = not fence
    return fence


def sentences(block: list[tuple[int, str]]):
    """Consecutive added prose lines joined and split into sentences, each with the line it starts on."""
    out, para, start = [], [], 0
    prev = None
    def flush():
        if para:
            joined = " ".join(p.strip() for p in para)
            for s in re.split(r"(?<=[.!?])\s+(?=[A-Z`*(\[\"“])", joined):
                if s.strip():
                    out.append((start, s.strip()))
    for n, text in block:
        if prev is not None and n != prev + 1 or not text.strip() or text.strip().startswith("#"):
            flush(); para = []
            if text.strip().startswith("#"):
                out.append((n, text.strip()))
            prev = n
            continue
        if not para:
            start = n
        para.append(text)
        prev = n
    flush()
    return out


def changes(diff: str, only_part: str | None = None):
    """path -> (sentences, figure lines) for the hand-written pages."""
    result = {}
    for path, added in parse(diff).items():
        if not path.startswith("src/") or not path.endswith(".md") or "/generated/" in path:
            continue
        if only_part and not path.startswith(f"src/systems/{only_part}/") and not path.startswith(f"src/{only_part}/"):
            continue
        fig = [(n, t) for n, t in added if in_fence(path, n)]
        prose = [(n, t) for n, t in added if not in_fence(path, n)]
        result[path] = (sentences(prose), fig)
    return result


def probe() -> int:
    diff = ("diff --git a/src/systems/x/p.md b/src/systems/x/p.md\n--- a/src/systems/x/p.md\n+++ b/src/systems/x/p.md\n"
            "@@ -10,2 +10,3 @@\n-old line\n+A first sentence. A second\n+one that wraps.\n context\n"
            "@@ -30 +31,2 @@\n+## A heading\n+Alone.\n"
            "diff --git a/src/generated/g.md b/src/generated/g.md\n--- a/src/generated/g.md\n+++ b/src/generated/g.md\n@@ -1 +1 @@\n+ignored\n")
    parsed = parse(diff)
    if parsed.get("src/systems/x/p.md") != [(10, "A first sentence. A second"), (11, "one that wraps."), (31, "## A heading"), (32, "Alone.")]:
        print(f"probe FAILED: parse {dict(parsed)}"); return 1
    s = sentences(parsed["src/systems/x/p.md"])
    if s != [(10, "A first sentence."), (10, "A second one that wraps."), (31, "## A heading"), (32, "Alone.")]:
        print(f"probe FAILED: sentences {s}"); return 1
    got = {p for p in parse(diff) if p.startswith("src/") and "/generated/" not in p}
    if got != {"src/systems/x/p.md"}:
        print(f"probe FAILED: generated page not skipped {got}"); return 1
    print("probe ok: added lines numbered from the hunk header, wrapped lines joined into sentences, a heading kept whole, a generated page skipped")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--ref", default="pass-8-start")
    ap.add_argument("--part")
    ap.add_argument("--summary", action="store_true")
    ap.add_argument("--probe", action="store_true")
    args = ap.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if args.probe:
        return probe()
    r = subprocess.run(["git", "diff", "--unified=0", args.ref, "--", "src/"], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0:
        sys.exit(f"git diff failed: {r.stderr.strip()} (is the tag {args.ref} placed?)")
    result = changes(r.stdout, args.part)
    if args.summary:
        per_part = Counter()
        print("| page | sentences | figure lines |\n|---|---:|---:|")
        for path, (s, f) in sorted(result.items()):
            print(f"| `{path}` | {len(s)} | {len(f)} |")
            d = path.split("/")[2] if path.startswith("src/systems/") else path.split("/")[1]
            per_part[d] += len(s)
        print("\n| part | changed sentences |\n|---|---:|")
        for d, n in per_part.most_common():
            print(f"| {d} | {n} |")
        print(f"\n{sum(len(s) for s, _f in result.values())} sentences and {sum(len(f) for _s, f in result.values())} figure lines changed on {len(result)} pages since {args.ref}")
        return 0
    for path, (s, f) in sorted(result.items()):
        print(f"\n### `{path}` — {len(s)} sentences, {len(f)} figure lines")
        for n, t in s:
            print(f"- L{n}: {t}")
        for n, t in f:
            print(f"- L{n} (figure): {t}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
