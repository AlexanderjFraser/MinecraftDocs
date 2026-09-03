#!/usr/bin/env python3
"""The confident sentences on a page, listed by the shape pass 2 found errors in.

Pass 2's evidence: the errors live in the confident sentences — counts,
"only" / "never" / "all", orderings, "X, not Y", and which side or thread
runs something. `verify_names.py` proves the names exist; this lists the
sentences an adversarial agent must re-derive, so the brief can hand it a
population instead of a page, and so session N's corpus-wide count sweep has
its queue (`--counts --all`).

A page is read outside its code fences as prose sentences, table rows and
diagram lines (a figure label is a claim too); each sentence is tagged with
every category it trips. The categories, and what trips them:

  count     a digit number (not the version 26.2), a number word from two to
            a thousand, or "only/exactly/just one", "both", "twice", "a pair",
            "half", "a dozen", "single"
  absolute  only · never · always · every · all · none · nothing · nobody ·
            exactly · sole(ly) · the only · the one · no other · without exception
  order     before · after · then · first · last · earlier · later · precedes ·
            follows · same tick · next tick · by the time · until · once
  contrast  "X, not Y" · "not X but Y" · rather than · instead of · fallback ·
            exception · "does not" / "is not" / "never" a thing
  side      Server / Render / Netty / client / main thread · server-side ·
            client-only · both sides · authoritative · off the tick · worker

Usage:
    python tools/claims.py src/systems/world/tickets-and-loading.md   # one page, every category
    python tools/claims.py src/systems/world --counts                  # a part's counts only
    python tools/claims.py --all --summary                             # a table: page × category, corpus-wide
    python tools/claims.py --all --counts --out DIR                    # session N's queue: one file per page
"""
from __future__ import annotations

import argparse
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "src")

NUMBER_WORDS = (
    r"two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|"
    r"sixteen|seventeen|eighteen|nineteen|twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety|"
    r"hundred|thousand"
)
CATEGORIES = {
    "count": re.compile(
        rf"(?<![\w.])(?!26\.2\b)\d+(?:[.,]\d+)?(?![\w.])"
        rf"|\b(?:{NUMBER_WORDS})(?:-(?:one|two|three|four|five|six|seven|eight|nine))?\b"
        r"|\b(?:only|exactly|just|the) one\b|\bboth\b|\btwice\b|\ba pair\b|\bhalf\b|\ba dozen\b|\bsingle\b",
        re.I),
    "absolute": re.compile(
        r"\b(?:only|never|always|every|all|none|nothing|nobody|exactly|solely?|the one|no other|"
        r"without exception|anywhere|nowhere|whatever|regardless)\b", re.I),
    "order": re.compile(
        r"\b(?:before|after|then|first|last|earlier|later|precedes?|follows?|followed|same tick|"
        r"next tick|by the time|until|once|already|not yet|ahead of|behind)\b", re.I),
    "contrast": re.compile(
        r",\s*not\b|\bnot\b[^.;:]{1,60}\bbut\b|\brather than\b|\binstead of\b|\bfallback\b|"
        r"\bexception\b|\bdoes not\b|\bdo not\b|\bis not\b|\bare not\b|\bnever\b|\bcannot\b|\bno longer\b", re.I),
    "side": re.compile(
        r"\b(?:Server|Render|Netty|client|server|main|worker|IO|Sound) thread\b|\bserver-side\b|\bclient-side\b|"
        r"\bclient-only\b|\bserver-only\b|\bboth sides\b|\bauthoritative\b|\boff the tick\b|\bon a worker\b|"
        r"\bon the (?:server|client)\b|\bthe (?:server|client) (?:does|never|only|owns|decides)\b", re.I),
}
ORDER = ["count", "absolute", "order", "contrast", "side"]


def strip_inline(s: str) -> str:
    s = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", s)     # links → their text
    s = re.sub(r"<!--.*?-->", "", s, flags=re.S)
    return s


def sentences_of(page: str):
    """Yield (line, kind, sentence) for prose sentences, table rows and diagram lines."""
    with open(page, encoding="utf-8") as f:
        lines = f.read().split("\n")
    i, n = 0, len(lines)
    para: list[tuple[int, str]] = []

    def flush():
        if not para:
            return []
        start = para[0][0]
        text = strip_inline(" ".join(re.sub(r"^>\s?", "", t.strip()) for _, t in para))
        text = re.sub(r"^\s*(?:#{1,6}\s+|>\s*|[-*]\s+|\d+\.\s+)", "", text)
        # sentence split: end punctuation followed by space and a capital, quote or asterisk
        parts = re.split(r"(?<=[.!?])\s+(?=[A-Z\"“*(`\[])", text)
        out = []
        for p in parts:
            p = p.strip()
            if len(p) > 3:
                out.append((start, "prose", p))
        para.clear()
        return out

    while i < n:
        raw = lines[i]
        if raw.startswith("```"):
            yield from flush()
            kind = "figure" if "mermaid" in raw else "code"
            i += 1
            while i < n and not lines[i].startswith("```"):
                if kind == "figure":
                    t = lines[i].strip()
                    if t and not re.match(r"^(sequenceDiagram|flowchart|graph|stateDiagram|timeline|pie|participant |actor |direction |title |end$|classDef|style |linkStyle|%%)", t):
                        yield (i + 1, "figure", t)
                i += 1
            i += 1
            continue
        if raw.lstrip().startswith("|"):
            yield from flush()
            cells = [strip_inline(c.strip()) for c in raw.strip().strip("|").split("|")]
            if cells and not all(re.fullmatch(r":?-{2,}:?", c) for c in cells if c):
                yield (i + 1, "table", " | ".join(cells))
            i += 1
            continue
        if raw.strip() == "" or raw.startswith("{{#include"):
            yield from flush()
            i += 1
            continue
        if re.match(r"^\s*(?:#{1,6}\s+|[-*]\s+|\d+\.\s+)", raw) and para:
            yield from flush()
        para.append((i + 1, raw))
        i += 1
    yield from flush()


def tag(sentence: str, only: set[str] | None) -> dict:
    hits = {}
    for cat in ORDER:
        if only and cat not in only:
            continue
        found = [m.group(0) for m in CATEGORIES[cat].finditer(sentence)]
        if found:
            hits[cat] = found
    return hits


def mark(sentence: str, words: list[str]) -> str:
    out = sentence
    for w in sorted(set(words), key=len, reverse=True):
        out = re.sub(rf"(?<!\*)(?<![\w-]){re.escape(w)}(?![\w-])(?!\*)", f"**{w}**", out, count=1)
    return out


def scan(page: str, only: set[str] | None) -> list[tuple[int, str, str, dict]]:
    rows = []
    for line, kind, s in sentences_of(page):
        h = tag(s, only)
        if h:
            rows.append((line, kind, s, h))
    return rows


def render(page: str, rows, only: set[str] | None) -> str:
    rel = os.path.relpath(page, ROOT).replace("\\", "/")
    out = [f"# Confident sentences — `{rel}`", ""]
    cats = [c for c in ORDER if not only or c in only]
    counts = {c: sum(1 for r in rows if c in r[3]) for c in cats}
    out.append("  ".join(f"{c}: {counts[c]}" for c in cats))
    out.append("")
    for cat in cats:
        mine = [r for r in rows if cat in r[3]]
        if not mine:
            continue
        out.append(f"## {cat} ({len(mine)})")
        out.append("")
        for line, kind, s, h in mine:
            k = "" if kind == "prose" else f" [{kind}]"
            out.append(f"- L{line}{k}: {mark(s, h[cat])}")
        out.append("")
    return "\n".join(out)


def collect_pages(paths: list[str], all_pages: bool) -> list[str]:
    pages = []
    if all_pages:
        paths = [os.path.join(SRC, "systems"), os.path.join(SRC, "reference"), os.path.join(SRC, "maps"),
                 os.path.join(SRC, "introduction.md"), os.path.join(SRC, "lectures.md")]
    for p in paths:
        p = os.path.abspath(p)
        if os.path.isdir(p):
            for dp, _dn, fn in os.walk(p):
                for f in sorted(fn):
                    if f.endswith(".md"):
                        pages.append(os.path.join(dp, f))
        elif os.path.exists(p):
            pages.append(p)
        else:
            sys.exit(f"no such page: {p}")
    pages = [p for p in pages if "generated" not in p.replace("\\", "/").split("/")]
    return sorted(set(pages))


def is_generated(page: str) -> bool:
    with open(page, encoding="utf-8") as f:
        head = f.read(2000)
    return "Do not edit by hand" in head


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paths", nargs="*", help="pages or directories under src/")
    ap.add_argument("--all", action="store_true", help="every hand-kept page in the corpus")
    ap.add_argument("--counts", action="store_true", help="the count category only")
    ap.add_argument("--only", help="comma-separated categories: count,absolute,order,contrast,side")
    ap.add_argument("--summary", action="store_true", help="one row per page instead of the sentences")
    ap.add_argument("--out", help="write one <slug>.claims.md per page here")
    args = ap.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    only = None
    if args.counts:
        only = {"count"}
    if args.only:
        only = set(args.only.split(","))
        bad = only - set(ORDER)
        if bad:
            sys.exit(f"unknown categories {sorted(bad)}; choose from {ORDER}")
    pages = collect_pages(args.paths, args.all)
    if not pages:
        ap.print_help()
        return 2
    pages = [p for p in pages if not is_generated(p)]

    if args.summary:
        cats = [c for c in ORDER if not only or c in only]
        print("| page | " + " | ".join(cats) + " | sentences |")
        print("|---|" + "---:|" * (len(cats) + 1))
        total = {c: 0 for c in cats}
        for p in pages:
            rows = scan(p, only)
            rel = os.path.relpath(p, SRC).replace("\\", "/")
            cells = [sum(1 for r in rows if c in r[3]) for c in cats]
            for c, v in zip(cats, cells):
                total[c] += v
            print(f"| {rel} | " + " | ".join(str(v) for v in cells) + f" | {len(rows)} |")
        print("| **total** | " + " | ".join(str(total[c]) for c in cats) + " | |")
        return 0

    if args.out:
        os.makedirs(args.out, exist_ok=True)
    for p in pages:
        rows = scan(p, only)
        text = render(p, rows, only)
        if args.out:
            rel = os.path.relpath(p, SRC).replace("\\", "/")
            slug = re.sub(r"^systems/", "", rel)[:-3].replace("/", "--")
            with open(os.path.join(args.out, f"{slug}.claims.md"), "w", encoding="utf-8") as f:
                f.write(text + "\n")
            print(f"{len(rows):4d}  {rel}")
        else:
            print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
