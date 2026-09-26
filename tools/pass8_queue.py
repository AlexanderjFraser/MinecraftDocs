#!/usr/bin/env python3
"""The final pass's queue: what docs/pass9.md holds, routed by page and by part.

pass9.md is where every session of passes 5, 6 and 7 listed the claims it
introduced and the corrections it made, so that the third fact-check checks
them first. Each entry names its page in backticks (`entity-lifecycle`, or
`entities/entity-lifecycle`, or `/` for the introduction). This tool parses
the file, resolves each name to a page in SUMMARY.md, and prints how much
unchecked material each page and each part carries, which is what sizes the
final pass's sessions.

  python tools/pass8_queue.py            per-part totals and the unresolved names
  python tools/pass8_queue.py --pages    per-page counts, largest first
  python tools/pass8_queue.py --part VI  every entry for one part, by page and session
  python tools/pass8_queue.py --probe    proves an entry naming no known page is reported

An entry is one bullet (top level or nested) under a session heading; the
session it belongs to and the pass that wrote it are kept, because a pass-7
correction that overturns a pass-5 claim is checked once, at the later entry.
"""
import os
import re
import sys
from collections import Counter, defaultdict

HERE = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
SRC = os.path.join(HERE, "src")
QUEUE = os.path.join(HERE, "docs", "pass9.md")

SESSION = re.compile(r"^## (Pass (\d+), (?:session (\w+)|the planning session)[^\n]*)")
BULLET = re.compile(r"^\s*(?:[-*]|\d+\.) ")
NAME = re.compile(r"`(/|[a-z0-9-]+(?:/[a-z0-9-]+)?)`")
PART_LINE = re.compile(r"^- \[([IVX]+) · ([^\]]+)\]\(systems/([a-z-]+)/README\.md\)")
PAGE_LINE = re.compile(r"^\s*- \[[^\]]+\]\(([^)]+\.md)\)")


def pages():
    """slug -> (md path, part numeral); the part landing page is its dir name."""
    by_slug, part_of_dir, part = {}, {}, ""
    with open(os.path.join(SRC, "SUMMARY.md"), encoding="utf-8") as fh:
        for line in fh:
            m = PART_LINE.match(line)
            if m:
                part, part_of_dir[m.group(3)] = m.group(1), m.group(1)
                by_slug.setdefault(m.group(3), (f"systems/{m.group(3)}/README.md", part))
                continue
            m = PAGE_LINE.match(line)
            if not m:
                continue
            md = m.group(1)
            slug = os.path.basename(md)[:-3]
            d = md.split("/")[1] if md.startswith("systems/") else md.split("/")[0]
            p = part_of_dir.get(d, {"maps": "Maps", "reference": "Reference"}.get(d, "Frame"))
            if slug == "README":
                continue
            by_slug.setdefault(slug, (md, p))
            by_slug[f"{d}/{slug}"] = (md, p)
    by_slug["/"] = ("introduction.md", "Frame")
    return by_slug


def entries(text: str):
    """(pass, session, page-names, line) per bullet under a session heading."""
    out, cur = [], None
    for line in text.splitlines():
        m = SESSION.match(line)
        if m:
            cur = (int(m.group(2)), m.group(3) or "planning")
            continue
        if cur and BULLET.match(line):
            out.append((cur[0], cur[1], NAME.findall(line), line.strip()))
    return out


def route(text: str, known: dict):
    per_page, per_part, unresolved, unnamed = Counter(), Counter(), Counter(), 0
    detail = defaultdict(list)
    for p, s, names, line in entries(text):
        hit = [known[n] for n in names if n in known]
        for n in names:
            if n not in known and not re.fullmatch(r"[a-z]+", n):  # a bare word is a term, not a page
                unresolved[n] += 1
        if not hit:
            if not names:
                unnamed += 1  # a session-level note; an entry whose names all fail is in `unresolved`
            continue
        md, part = hit[0]  # the first named page owns the entry
        per_page[md] += 1
        per_part[part] += 1
        detail[(part, md)].append((p, s, line))
    return per_page, per_part, unresolved, unnamed, detail


def probe():
    known = {"a-page": ("systems/x/a-page.md", "I")}
    text = "## Pass 7, session A — x\n- `a-page` fine\n- `no-such-page`:12 wrong\n- no page named here\n"
    per_page, per_part, unresolved, unnamed, _ = route(text, known)
    if per_page != Counter({"systems/x/a-page.md": 1}) or unresolved != Counter({"no-such-page": 1}) or unnamed != 1:
        sys.exit(f"probe FAILED: {per_page} {unresolved} {unnamed}")
    print("probe ok: an entry naming an unknown page is reported, one naming none is counted")


if __name__ == "__main__":
    if "--probe" in sys.argv:
        probe()
        sys.exit()
    with open(QUEUE, encoding="utf-8") as fh:
        text = fh.read()
    known = pages()
    per_page, per_part, unresolved, unnamed, detail = route(text, known)
    total = sum(per_page.values())
    if "--part" in sys.argv:
        want = sys.argv[sys.argv.index("--part") + 1]
        for (part, md), rows in sorted(detail.items()):
            if part != want:
                continue
            print(f"\n### {md} — {len(rows)} entries")
            for p, s, line in rows:
                print(f"  [pass {p} {s}] {line[:160]}")
        sys.exit()
    if "--pages" in sys.argv:
        for md, n in per_page.most_common():
            print(f"{n:>5}  {md}")
        sys.exit()
    order = ["Frame", "Maps"] + ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII", "XIII"] + ["Reference"]
    print(f"{'part':<10}{'entries':>8}{'pages':>7}")
    pages_in = Counter(part for part, _ in detail)
    for part in order:
        print(f"{part:<10}{per_part.get(part, 0):>8}{pages_in.get(part, 0):>7}")
    print(f"{'total':<10}{total:>8}{len(per_page):>7}")
    print(f"\nentries naming no page: {unnamed} (session-level notes, standing items)")
    if unresolved:
        print(f"names that resolve to no page ({len(unresolved)}):")
        for n, c in unresolved.most_common(30):
            print(f"  {c:>3}  {n}")
