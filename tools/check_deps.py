#!/usr/bin/env python3
"""The landing pages, the lecture map and the parts-dependency figure, checked against each other.

Pass 4's charter (addition 2): the thirteen landing pages, `lectures.md` and
the parts-dependency figure assert that part B needs page A, and a
dependency is a claim. This does the mechanical half of the check, corpus-wide,
in one run; the agent does the other half (finding the sentence in the part
that actually *uses* each dependency). Four sources, read from the pages:

  landing   each part's `## Before you start` — the pages it links in other
            parts — and its `## Watch in this order` — the pages it lists
  figure    `src/generated/parts-dependency.svg` — solid and dashed arcs, which
            `--write-figure` draws from the landing pages (pass 7, session N) and
            `src/figures/parts-dependency.md` includes on two pages
  table     `lectures.md`'s dependency table — page, its part, the parts
            whose landing pages assume it — and each part's section of the map
  sidebar   `SUMMARY.md`'s order within each part
  links     every cross-part link from every system page

Checks (F = fails, exit 1; R = report only, for the session to judge):
  F  the generated figure and its table are what `--write-figure` would write now
  F  every solid arrow in the figure is a landing-page *before you start* link
     to an earlier part, and every such link is a solid arrow
  F  every *before you start* link to a *later* part is a dashed arrow, and
     every dashed arrow is one
  F  the lecture table's "parts whose landing pages assume it" column, re-derived
     from the landing pages
  F  each part's section of lectures.md lists the same pages in the same order
     as the part's *watch in this order*
  F  SUMMARY.md lists each part's pages in the same order as its *watch in this
     order* — pass 5, session A: the landing page's watch order is the book's
     order, and the sidebar and the lecture map follow it
  F  the lecture table's membership, by the rule the page states: a page two or
     more landing pages name under *before you start*, less the three every part
     assumes (they are the boxes the figure draws without edges)
  F  nothing in *watch in this order* is a Reference or maps page or another part's
  F  `reference/README.md`'s *parts* column, re-derived from the landing pages'
     *Reference this part uses* sections — pass 5, session N
  F  no landing page assumes `game-tests`
  R  per part: *before you start* pages that no page in the part links or names
     (candidate unused dependencies), and other parts' pages the part's pages link
     that its landing page does not list (candidate missing entries)

Usage:
    python tools/check_deps.py            # the checks; exit 1 on any F
    python tools/check_deps.py --quiet    # failures only
    python tools/check_deps.py --probe    # prove the checks on synthetic input
    python tools/check_deps.py --write-figure   # the parts-dependency figure and its table, from the landing pages
"""
from __future__ import annotations

import argparse
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "src")
ROMAN = {"I": 1, "II": 2, "III": 3, "IV": 4, "V": 5, "VI": 6, "VII": 7, "VIII": 8, "IX": 9,
         "X": 10, "XI": 11, "XII": 12, "XIII": 13, "XIV": 14}
NUMERAL = {v: k for k, v in ROMAN.items()}
LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
# The three pages every part assumes. `lectures.md`'s paragraph above the figure names them and
# says why they are drawn as boxes and not as edges; the dependency table excludes them for the
# same reason, so listing them here is the tool reading the page's own stated rule.
UNIVERSAL_PAGES = ("systems/anatomy/anatomy", "systems/foundations/codecs-nbt-json",
                   "systems/foundations/identifiers-and-registries")


def read(path: str) -> str:
    with open(path, encoding="utf-8") as f:
        return f.read()


def section(text: str, title: str) -> str:
    m = re.search(rf"^## {re.escape(title)}\s*$(.*?)(?=^## |\Z)", text, re.M | re.S)
    return m.group(1) if m else ""


def norm(base_dir: str, href: str) -> str | None:
    """A link target as a corpus key: systems/<part>/<slug>, reference/<slug>, maps/<slug>, or None."""
    href = href.split("#", 1)[0]
    if not href or href.startswith("http") or not href.endswith(".md"):
        return None
    full = os.path.normpath(os.path.join(base_dir, href))
    rel = os.path.relpath(full, SRC).replace("\\", "/")
    return rel[:-3]


def parts() -> dict:
    """part dir -> {num, title, before: [keys], watch: [keys], pages: [keys]}"""
    out = {}
    sysdir = os.path.join(SRC, "systems")
    for d in sorted(os.listdir(sysdir)):
        readme = os.path.join(sysdir, d, "README.md")
        if not os.path.exists(readme):
            continue
        text = read(readme)
        tm = re.match(r"#\s+([IVX]+)\s*·\s*(.*)", text)
        num = ROMAN[tm.group(1)]
        base = os.path.join(sysdir, d)
        before_text = section(text, "Before you start")
        before, context = [], {}
        for m in LINK.finditer(before_text):
            k = norm(base, m.group(1))
            if not k or k.startswith(f"systems/{d}/") or k in before:
                continue
            before.append(k)
            # the sentence the link sits in, so a forward link can be judged without opening the page
            starts = [x.end() for x in re.finditer(r"\.\s", before_text[:m.start()])]
            s = starts[-1] if starts else 0
            em = re.search(r"\.\s", before_text[m.end():])
            e = m.end() + em.start() + 1 if em else len(before_text)
            context[k] = re.sub(r"\s+", " ", re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", before_text[s:e])).strip()
        # a watch entry is the first link of a numbered item; later links in the item are references
        watch = []
        for item in re.finditer(r"^\s*\d+\.\s+(.*?)(?=^\s*\d+\.\s|\Z)", section(text, "Watch in this order"), re.M | re.S):
            m = LINK.search(item.group(1))
            k = norm(base, m.group(1)) if m else None
            if k:
                watch.append(k)
        # the Reference pages this part's landing page points at, which is the population behind
        # `reference/README.md`'s *parts* column (pass 5, session N)
        refs = []
        for m in LINK.finditer(section(text, "Reference this part uses")):
            k = norm(base, m.group(1))
            if k and k.startswith("reference/") and k not in refs:
                refs.append(k)
        pages = [f"systems/{d}/{f[:-3]}" for f in sorted(os.listdir(base)) if f.endswith(".md") and f != "README.md"]
        out[d] = {"num": num, "title": tm.group(2).strip(), "before": before, "context": context,
                  "watch": watch, "pages": pages, "refs": refs, "readme": readme}
    return out


def part_of(key: str, byslug: dict) -> str | None:
    m = re.match(r"systems/([^/]+)/", key)
    return m.group(1) if m else None


FIG_SVG = os.path.join(SRC, "generated", "parts-dependency.svg")
FIG_MD = os.path.join(SRC, "generated", "parts-dependency.md")
FIG_EDGE = re.compile(r'data-edge="(\d+) (\d+) (solid|dashed)"')


def figure() -> tuple[set, set, list]:
    """The arrows the published figure draws, read back from the generated SVG's `data-edge`
    attributes (pass 7, session N: the figure is generated from the landing pages by
    `--write-figure`, so this reads what the site shows, and `figure_stale` says whether the
    file still matches the landing pages)."""
    if not os.path.exists(FIG_SVG):
        return set(), set(), [f"figure: {os.path.relpath(FIG_SVG, ROOT)} is missing — run `python tools/check_deps.py --write-figure`"]
    solid, dashed = set(), set()
    for m in FIG_EDGE.finditer(read(FIG_SVG)):
        (solid if m.group(3) == "solid" else dashed).add((int(m.group(1)), int(m.group(2))))
    return solid, dashed, []


# The parts-dependency figure (pass 7, session N). Mermaid laid the 27 arrows out with 26 crossings
# and no ordering of the source did better than fourteen, with the parts out of watch order; the
# prose calls the graph "a line with two knots", so the figure draws exactly that: the thirteen
# parts in one column in watch order, every solid arrow an arc on the right running down, the two
# backward dependencies dashed arcs on the left running up. An arc's reach is its span, so a
# nested pair never crosses; ports on a box are ordered so that arcs sharing an end do not either.
ROW, BOX_H, BOX_W = 54, 38, 270
FONT, SMALL = 15, 13


def landing_edges(P: dict) -> tuple[set, set, dict]:
    """(solid, dashed, dashed pages) as the landing pages state them; the arrows out of the two
    universal parts are left off except the spine, which is the rule `lectures.md` states."""
    solid, dashed, pages = set(), set(), {}
    nums = {d: v["num"] for d, v in P.items()}
    for d, v in P.items():
        for k in v["before"]:
            n = nums.get(part_of(k, None))
            if n is None or n == v["num"]:
                continue
            if n < v["num"]:
                if n not in (1, 2) or v["num"] == n + 1:
                    solid.add((n, v["num"]))
            else:
                dashed.add((n, v["num"]))
                pages.setdefault((n, v["num"]), []).append(k)
    return solid, dashed, pages


def page_title(key: str) -> str:
    m = re.match(r"#\s+(.*)", read(os.path.join(SRC, key + ".md")))
    return m.group(1).strip() if m else key.rsplit("/", 1)[1]


def figure_svg(P: dict) -> str:
    solid, dashed, pages = landing_edges(P)
    titles = {v["num"]: v["title"] for v in P.values()}
    n = len(titles)
    labels = {e: [page_title(x) for x in pages[e]] for e in dashed}
    # the left margin is what the widest dashed label needs beside its arc (0.6em a glyph, generously)
    left = max((0.75 * (26 + 20 * (a - b)) + 16 + 0.6 * SMALL * max(len(t) for t in labels[(a, b)])
                for a, b in dashed), default=0)
    xl = int(left) + 8
    xr = xl + BOX_W
    top = lambda p: 10 + (p - 1) * ROW
    mid = lambda p: top(p) + BOX_H / 2

    def ports(edges, side_nodes):
        """node -> {edge: y}: incoming arcs above outgoing; the longer arc of a group nearer the middle."""
        out = {}
        for p in side_nodes:
            inc = sorted((e for e in edges if e[1] == p), key=lambda e: p - e[0])
            outg = sorted((e for e in edges if e[0] == p), key=lambda e: -(e[1] - p))
            seq = [(e, "in") for e in inc] + [(e, "out") for e in outg]
            for i, (e, _) in enumerate(seq):
                out.setdefault(p, {})[e] = top(p) + BOX_H * (i + 1) / (len(seq) + 1)
        return out

    def bulge(e):
        return 26 + 20 * abs(e[1] - e[0])

    rp = ports(solid, titles)
    lp = ports({(b, a) for a, b in dashed}, titles)   # a dashed arc runs up: its head is the earlier part
    reach_r = max((0.75 * bulge(e) for e in solid), default=0) + 12
    W = int(xr + reach_r + 4)
    H = int(top(n) + BOX_H + 10)
    o = [f'<svg class="mapfig" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img">',
         '<title>The thirteen parts in watch order; an arc on the right is a part another part assumes, '
         'an arc on the left is one of the two places a part assumes a later one</title>']
    for p in sorted(titles):
        o.append(f'<g class="part"><title>Part {NUMERAL[p]} · {esc(titles[p])}</title>'
                 f'<rect class="group" x="{xl}" y="{top(p)}" width="{BOX_W}" height="{BOX_H}" rx="3"/>'
                 f'<text x="{xl + 14}" y="{mid(p) + 5:.1f}" font-size="{FONT}">{NUMERAL[p]} · {esc(titles[p])}</text></g>')
    for a, b in sorted(solid, key=lambda e: (e[1] - e[0], e)):
        y1, y2, k = rp[a][(a, b)], rp[b][(a, b)], bulge((a, b))
        o.append(f'<g><title>{NUMERAL[a]} → {NUMERAL[b]}: Part {NUMERAL[b]} assumes Part {NUMERAL[a]}</title>'
                 f'<path class="edge" data-edge="{a} {b} solid" d="M{xr},{y1:.1f} C{xr + k},{y1:.1f} {xr + k},{y2:.1f} {xr + 5},{y2:.1f}"/>'
                 f'<path class="muted" fill="currentColor" d="M{xr},{y2:.1f} l7,-3.5 l0,7 z"/></g>')
    for a, b in sorted(dashed):
        # a → b with a later than b: the arc leaves a's left side and arrives at b's, above it
        y1, y2, k = lp[a][(b, a)], lp[b][(b, a)], bulge((a, b))
        names = labels[(a, b)]
        o.append(f'<g><title>{NUMERAL[a]} ⇢ {NUMERAL[b]}: Part {NUMERAL[b]} assumes {esc(", ".join(names))}, cut on purpose</title>'
                 f'<path class="edge" data-edge="{a} {b} dashed" stroke-dasharray="5 4" '
                 f'd="M{xl},{y1:.1f} C{xl - k},{y1:.1f} {xl - k},{y2:.1f} {xl - 5},{y2:.1f}"/>'
                 f'<path class="muted" fill="currentColor" d="M{xl},{y2:.1f} l-7,-3.5 l0,7 z"/></g>')
        lx, ly = xl - 0.75 * k - 8, (y1 + y2) / 2 - (len(names) - 1) * 9.5
        for i, t in enumerate(names):
            o.append(f'<text x="{lx:.1f}" y="{ly + i * 19 + 4:.1f}" text-anchor="end" font-size="{SMALL}">{esc(t)}</text>')
    o.append("</svg>")
    return "\n".join(o) + "\n"


def figure_table(P: dict) -> str:
    solid, dashed, pages = landing_edges(P)
    titles = {v["num"]: v["title"] for v in P.values()}
    rows = ["| part | assumes (a solid arc) | assumes from a later part (a dashed arc) |", "|---|---|---|"]
    for p in sorted(titles):
        before = ", ".join(NUMERAL[a] for a, b in sorted(solid) if b == p) or "—"
        later = "; ".join(f"{NUMERAL[a]}: " + ", ".join(page_title(k) for k in pages[(a, b)])
                          for a, b in sorted(dashed) if b == p) or "—"
        rows.append(f"| {NUMERAL[p]} · {titles[p]} | {before} | {later} |")
    return "\n".join(rows) + "\n"


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def figure_stale(P: dict) -> list[str]:
    out = []
    for path, want in ((FIG_SVG, figure_svg(P)), (FIG_MD, figure_table(P))):
        if not os.path.exists(path) or read(path) != want:
            out.append(f"figure: {os.path.relpath(path, ROOT)} does not match the landing pages — "
                       f"run `python tools/check_deps.py --write-figure`")
    return out


def lecture_table() -> list[tuple[list[str], int, set[int], int]]:
    """rows of (page keys, part, parts that assume it, line)"""
    text = read(os.path.join(SRC, "lectures.md"))
    rows = []
    for i, line in enumerate(text.split("\n"), 1):
        if not line.startswith("| [") or "systems/" not in line:
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 3:
            continue
        keys = [k for k in (norm(SRC, h) for h in LINK.findall(cells[0])) if k]
        part = ROMAN.get(cells[1], 0)
        assume = {ROMAN[r] for r in re.findall(r"\b([IVX]+)\b", cells[2].split("—")[0]) if r in ROMAN}
        rows.append((keys, part, assume, i))
    return rows


def lecture_sections() -> dict[int, list[str]]:
    text = read(os.path.join(SRC, "lectures.md"))
    out = {}
    for m in re.finditer(r"^## ([IVX]+)\s*·[^\n]*\n(.*?)(?=^## |\Z)", text, re.M | re.S):
        num = ROMAN[m.group(1)]
        keys = []
        for h in LINK.findall(m.group(2)):
            k = norm(SRC, h)
            if k and k.startswith("systems/") and not k.endswith("/README"):
                if k not in keys:
                    keys.append(k)
        out[num] = keys
    return out


def summary_order() -> dict[str, list[str]]:
    """part dir -> the part's pages in SUMMARY.md order (the sidebar)."""
    out: dict[str, list[str]] = {}
    cur = None
    for line in read(os.path.join(SRC, "SUMMARY.md")).split("\n"):
        m = LINK.search(line)
        if not m:
            continue
        k = norm(SRC, m.group(1))
        if not k or not k.startswith("systems/"):
            continue
        d, slug = k.split("/")[1], k.rsplit("/", 1)[1]
        if slug == "README":
            cur = d
            out.setdefault(d, [])
        elif cur == d:
            out.setdefault(d, []).append(k)
    return out


def sidebar_failures(P: dict, sidebar: dict[str, list[str]]) -> list[str]:
    """SUMMARY.md's order within a part against the landing page's watch order."""
    out = []
    for d, v in P.items():
        watch = [k for k in v["watch"] if k.startswith(f"systems/{d}/")]
        side = sidebar.get(d, [])
        if watch != side:
            out.append(f"Part {NUMERAL[v['num']]}: SUMMARY.md and *watch in this order* disagree\n"
                       f"      landing: {' · '.join(k.rsplit('/', 1)[1] for k in watch)}\n"
                       f"      sidebar: {' · '.join(k.rsplit('/', 1)[1] for k in side)}")
    return out


def membership_failures(dependents: dict[str, set[int]], table_pages: set[str]) -> list[str]:
    """The lecture table holds exactly the pages two or more landing pages name under
    *before you start*, less the three every part assumes."""
    out = []
    for k in sorted(set(dependents) | table_pages):
        n = len(dependents.get(k, ()))
        if k in UNIVERSAL_PAGES:
            if k in table_pages:
                out.append(f"lectures.md: {k} is a dependency every part shares — the paragraph above the "
                           f"figure says so and the figure draws it without edges — so it does not take a table row")
            continue
        if n >= 2 and k not in table_pages:
            out.append(f"lectures.md: {k} is named under *before you start* by {n} parts "
                       f"({', '.join(NUMERAL[x] for x in sorted(dependents[k]))}) and has no row in the dependency table")
        if n < 2 and k in table_pages:
            out.append(f"lectures.md: {k} has a row in the dependency table and is named under "
                       f"*before you start* by {n} part{'' if n == 1 else 's'}")
    return out


REF_ROW = re.compile(r"^\|\s*\[[^\]]*\]\((?P<href>[a-z0-9\-]+\.md)\)\s*\|[^|]*\|[^|]*\|(?P<parts>[^|]*)\|\s*$", re.M)


def reference_column(refs_by_part: dict[str, set[int]]) -> list[str]:
    """`reference/README.md`'s *parts* column against the thirteen landing pages.

    The column's own header says *the parts whose landing pages point at it*, and the
    landing page's slot for that is `## Reference this part uses` (TEMPLATE.md, *The
    landing page*). So the column is derivable, and pass 5's session N found it stale in
    six of twenty rows — the only such column in the book with no gate.
    `every part` is the shorthand for all thirteen; an em dash means none.
    """
    out = []
    path = os.path.join(SRC, "reference", "README.md")
    seen = set()
    for m in REF_ROW.finditer(read(path)):
        key = "reference/" + m.group("href")[:-3]
        seen.add(key)
        want = sorted(refs_by_part.get(key, set()))
        cell = m.group("parts").strip()
        if cell == "every part":
            got = sorted(range(1, 14))
        elif cell in ("—", "-", ""):
            got = []
        else:
            got = sorted(ROMAN[x.strip()] for x in cell.split(",") if x.strip() in ROMAN)
        if got != want:
            shown = "every part" if want == list(range(1, 14)) else (", ".join(NUMERAL[n] for n in want) or "—")
            out.append(f"reference/README.md: {m.group('href')}'s *parts* column says “{cell}”; "
                       f"the landing pages that point at it under *Reference this part uses* are {shown}")
    for key in sorted(set(refs_by_part) - seen):
        out.append(f"reference/README.md: no row for {key.split('/')[-1]}.md, which "
                   f"{len(refs_by_part[key])} landing page(s) point at")
    return out


def _ref_truth(drop: bool = False) -> dict[str, set[int]]:
    """The probe's synthetic truth: the shelf's own column, read back as if the landing pages
    said exactly that, so the check passes; with `drop`, one part is removed from one row so it
    must fail. Built from the file rather than hard-coded, so the probe cannot rot."""
    truth: dict[str, set[int]] = {}
    first = None
    for m in REF_ROW.finditer(read(os.path.join(SRC, "reference", "README.md"))):
        key = "reference/" + m.group("href")[:-3]
        cell = m.group("parts").strip()
        if cell == "every part":
            truth[key] = set(range(1, 14))
        elif cell in ("—", "-", ""):
            continue
        else:
            truth[key] = {ROMAN[x.strip()] for x in cell.split(",") if x.strip() in ROMAN}
            if first is None and len(truth[key]) > 1:
                first = key
    if drop and first:
        truth[first] = set(sorted(truth[first])[:-1])
    return truth


def _fig_parts(universal: bool = False) -> dict:
    """Two synthetic parts that assume each other, the probe's input to the figure writer; with
    `universal`, Part IV also names a Part II page and Part III the page before it."""
    before3 = ["systems/b/x"] + (["systems/f/c"] if universal else [])
    before4 = ["systems/a/y"] + (["systems/f/c"] if universal else [])
    P = {"a": {"num": 3, "title": "A", "before": before3},
         "b": {"num": 4, "title": "B", "before": before4}}
    if universal:
        P["f"] = {"num": 2, "title": "F", "before": []}
    return P


def _fig_edges(P: dict) -> tuple[set, set]:
    global page_title
    real, page_title = page_title, (lambda key: key)
    try:
        svg = figure_svg(P)
    finally:
        page_title = real
    solid, dashed = set(), set()
    for m in FIG_EDGE.finditer(svg):
        (solid if m.group(3) == "solid" else dashed).add((int(m.group(1)), int(m.group(2))))
    return solid, dashed


def probe() -> int:
    """Prove the two pass-5 checks fail on the constructs they are for, and pass otherwise."""
    P = {"world": {"num": 4, "watch": ["systems/world/a", "systems/world/b", "systems/world/c"]}}
    checks = [
        ("the sidebar agreeing with the watch order passes",
         sidebar_failures(P, {"world": ["systems/world/a", "systems/world/b", "systems/world/c"]}) == []),
        ("a reordered sidebar fails",
         len(sidebar_failures(P, {"world": ["systems/world/b", "systems/world/a", "systems/world/c"]})) == 1),
        ("a sidebar missing a page fails",
         len(sidebar_failures(P, {"world": ["systems/world/a", "systems/world/b"]})) == 1),
        ("a page two parts assume, with a row, passes",
         membership_failures({"systems/world/x": {5, 6}}, {"systems/world/x"}) == []),
        ("a page two parts assume, with no row, fails",
         len(membership_failures({"systems/world/x": {5, 6}}, set())) == 1),
        ("a row for a page one part assumes fails",
         len(membership_failures({"systems/world/x": {5}}, {"systems/world/x"})) == 1),
        ("a row for a page nobody assumes fails",
         len(membership_failures({}, {"systems/world/x"})) == 1),
        ("a universal with no row passes though six parts assume it",
         membership_failures({UNIVERSAL_PAGES[0]: {3, 4, 5, 6, 7, 8}}, set()) == []),
        ("a universal with a row fails",
         len(membership_failures({UNIVERSAL_PAGES[0]: {3, 4}}, {UNIVERSAL_PAGES[0]})) == 1),
        ("the shelf's *parts* column, as the landing pages have it, passes",
         reference_column(_ref_truth()) == []),
        ("a row missing a part fails",
         len(reference_column(_ref_truth(drop=True))) == 1),
        ("the figure draws a later part's link as a dashed arc and an earlier one as solid",
         _fig_edges(_fig_parts()) == ({(3, 4)}, {(4, 3)})),
        ("the figure leaves off a universal part's arrows except the spine",
         _fig_edges(_fig_parts(universal=True)) == ({(2, 3), (3, 4)}, {(4, 3)})),
    ]
    bad = [name for name, ok in checks if not ok]
    for name, ok in checks:
        print(("  ok  " if ok else "  FAIL ") + name)
    print("probe: OK" if not bad else f"probe: {len(bad)} FAILED")
    return 1 if bad else 0


def page_links(pdir: str, pages: list[str]) -> dict[str, dict[str, list[str]]]:
    """target key -> {from page key: [contexts]} for links out of the part's pages to other parts' pages"""
    out: dict[str, dict[str, list[str]]] = {}
    base = os.path.join(SRC, "systems", pdir)
    for key in list(pages) + [f"systems/{pdir}/README"]:
        if key.endswith("/what-this-book-skips"):
            continue   # its links are pointers to owner pages by design, not dependencies
        text = read(os.path.join(SRC, key + ".md"))
        for h in LINK.findall(text):
            k = norm(base, h)
            if not k or not k.startswith("systems/") or k.startswith(f"systems/{pdir}/"):
                continue
            out.setdefault(k, {}).setdefault(key, [])
    return out


def mentions(pdir: str, pages: list[str], target: str) -> bool:
    """does any page of the part link the target or name its slug in backticks or as link text"""
    slug = target.rsplit("/", 1)[1]
    pat = re.compile(rf"\]\([^)]*{re.escape(slug)}\.md|`{re.escape(slug)}`")
    for key in pages:
        if key.endswith("/what-this-book-skips"):
            continue   # excluded as a link source above; exclude it as evidence too
        if pat.search(read(os.path.join(SRC, key + ".md"))):
            return True
    return False


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--quiet", action="store_true", help="failures only")
    ap.add_argument("--probe", action="store_true",
                    help="prove the sidebar and membership checks on synthetic input")
    ap.add_argument("--write-figure", action="store_true",
                    help="write src/generated/parts-dependency.svg and its table from the landing pages")
    args = ap.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if args.probe:
        return probe()

    P = parts()
    if args.write_figure:
        os.makedirs(os.path.dirname(FIG_SVG), exist_ok=True)
        for path, body in ((FIG_SVG, figure_svg(P)), (FIG_MD, figure_table(P))):
            with open(path, "w", encoding="utf-8", newline="\n") as fh:
                fh.write(body)
            print(f"wrote {os.path.relpath(path, ROOT)}")
        return 0
    bynum = {v["num"]: k for k, v in P.items()}
    solid, dashed, unread = figure()
    fails: list[str] = list(unread) + figure_stale(P)
    reports: list[str] = []

    def numof(key: str) -> int | None:
        d = part_of(key, None)
        return P[d]["num"] if d in P else None

    # 1. landing before-you-start ↔ figure arrows. Parts I and II keep their boxes and the spine
    # I → II → III, but the rest of their arrows are left off on purpose (lectures.md: "the two
    # dependencies every part shares"), so arrows out of them are not expected.
    UNIVERSAL = {1, 2}
    landing_solid, landing_dashed = set(), set()
    landing_by_edge: dict[tuple, list[str]] = {}
    for d, v in P.items():
        for k in v["before"]:
            n = numof(k)
            if n is None or n == v["num"]:
                continue
            edge = (n, v["num"])
            landing_by_edge.setdefault(edge, []).append(k)
            (landing_solid if n < v["num"] else landing_dashed).add(edge)
    for e in sorted(solid - landing_solid):
        fails.append(f"figure: solid arrow {NUMERAL[e[0]]} → {NUMERAL[e[1]]} has no *before you start* link on Part {NUMERAL[e[1]]}'s landing page")
    for e in sorted(landing_solid - solid):
        if e[0] in UNIVERSAL:
            continue
        fails.append(f"figure: Part {NUMERAL[e[1]]}'s landing page links {', '.join(landing_by_edge[e])} (Part {NUMERAL[e[0]]}) under *before you start*, and the figure has no solid arrow {NUMERAL[e[0]]} → {NUMERAL[e[1]]}")
    for e in sorted(dashed - landing_dashed):
        fails.append(f"figure: dashed arrow {NUMERAL[e[0]]} → {NUMERAL[e[1]]} has no *before you start* link to a later part on Part {NUMERAL[e[1]]}'s landing page")
    for e in sorted(landing_dashed - dashed):
        # a landing page may link a later part's page to say what it hands *forward*, which is not a
        # dependency; or to assume it, which is a missing dashed arrow. The sentence decides.
        d = bynum[e[1]]
        for k in landing_by_edge[e]:
            reports.append(f"FORWARD LINK, no dashed arrow {NUMERAL[e[0]]} → {NUMERAL[e[1]]}: Part {NUMERAL[e[1]]}'s *before you start* links {k}\n    “{P[d]['context'].get(k, '')}”\n    → a dependency needs the arrow; a hand-forward belongs outside *before you start*")
    for e in sorted(solid):
        if e[0] >= e[1]:
            fails.append(f"figure: solid arrow {NUMERAL[e[0]]} → {NUMERAL[e[1]]} points at an earlier or the same part")
    for e in sorted(dashed):
        if e[0] <= e[1]:
            fails.append(f"figure: dashed arrow {NUMERAL[e[0]]} → {NUMERAL[e[1]]} points forward; dashed arrows are the backward dependencies")

    # 2. the lecture table's third column
    for keys, part, assume, line in lecture_table():
        derived = set()
        for d, v in P.items():
            if any(k in v["before"] for k in keys):
                derived.add(v["num"])
        if derived != assume:
            fails.append(f"lectures.md:{line}: {', '.join(keys)} — table says assumed by {', '.join(NUMERAL[n] for n in sorted(assume)) or 'nobody'}; landing pages say {', '.join(NUMERAL[n] for n in sorted(derived)) or 'nobody'}")
        for k in keys:
            if numof(k) != part:
                fails.append(f"lectures.md:{line}: {k} is not in Part {NUMERAL[part]}")

    # 3. each part's lectures.md section vs its watch order
    secs = lecture_sections()
    for d, v in P.items():
        watch = [k for k in v["watch"] if k.startswith(f"systems/{d}/")]
        sec = secs.get(v["num"], [])
        sec_own = [k for k in sec if k.startswith(f"systems/{d}/")]
        if watch != sec_own:
            fails.append(f"Part {NUMERAL[v['num']]}: *watch in this order* on the landing page and its section of lectures.md list different pages or a different order\n      landing:  {' · '.join(k.rsplit('/', 1)[1] for k in watch)}\n      lectures: {' · '.join(k.rsplit('/', 1)[1] for k in sec_own)}")
        missing = [p.rsplit("/", 1)[1] for p in v["pages"] if p not in watch]
        if missing:
            reports.append(f"Part {NUMERAL[v['num']]}: pages not in *watch in this order*: {', '.join(missing)}")

    # 4. watch order contains only the part's own pages
    for d, v in P.items():
        for k in v["watch"]:
            if not k.startswith(f"systems/{d}/"):
                fails.append(f"Part {NUMERAL[v['num']]}: *watch in this order* lists {k}, which is not one of its pages")

    # 4b. SUMMARY.md's order within a part is the landing page's watch order (pass 5, session A)
    fails += sidebar_failures(P, summary_order())

    # 4c. the lecture table's membership, by the rule lectures.md states above it
    table_pages = {k for keys, _p, _a, _l in lecture_table() for k in keys}
    dependents: dict[str, set[int]] = {}
    for d, v in P.items():
        for k in v["before"]:
            if k.startswith("systems/") and not k.endswith("/README") and numof(k) != v["num"]:
                dependents.setdefault(k, set()).add(v["num"])
    fails += membership_failures(dependents, table_pages)

    # 4d. the shelf's *parts* column against the landing pages (pass 5, session N)
    refs_by_part: dict[str, set[int]] = {}
    for d, v in P.items():
        for k in v["refs"]:
            refs_by_part.setdefault(k, set()).add(v["num"])
    fails += reference_column(refs_by_part)

    # 5. nobody assumes game-tests
    for d, v in P.items():
        for k in v["before"]:
            if k.endswith("/game-tests"):
                fails.append(f"Part {NUMERAL[v['num']]}: *before you start* assumes game-tests")

    # 6. report: unused before-you-start entries, and cross-part links the landing page does not list
    for d, v in P.items():
        outlinks = page_links(d, v["pages"])
        # a link to another part's landing page is a dependency on the whole part, and no page in
        # this part will ever link it, so it can never satisfy mentions(); the unlisted half below
        # excludes READMEs for the same reason.
        unused = [k for k in v["before"] if k.startswith("systems/") and not k.startswith(f"systems/{d}/")
                  and not k.endswith("/README") and not mentions(d, v["pages"], k)]
        unlisted = {k: srcs for k, srcs in outlinks.items() if k not in v["before"] and not k.endswith("/README")}
        lines = [f"Part {NUMERAL[v['num']]} · {v['title']} — before you start: "
                 + ", ".join(k.split('/', 1)[1] for k in v["before"] if k.startswith("systems/"))]
        if unused:
            lines.append("    entries no page in the part links or names (find the sentence that uses each, or strike): "
                         + ", ".join(k.split('/', 1)[1] for k in unused))
        if unlisted:
            by_part: dict[str, list[str]] = {}
            for k, srcs in sorted(unlisted.items()):
                by_part.setdefault(part_of(k, None), []).append(f"{k.rsplit('/', 1)[1]} ← {', '.join(s.rsplit('/', 1)[1] for s in srcs)}")
            lines.append("    other parts' pages linked but not listed (a link is not a dependency; judge each):")
            for pd, items in by_part.items():
                arrow = "later" if P[pd]["num"] > v["num"] else "earlier"
                lines.append(f"      Part {NUMERAL[P[pd]['num']]} ({arrow}): " + "; ".join(items))
        reports.append("\n".join(lines))

    if not args.quiet:
        print("== Dependency report (for the session to judge)\n")
        for r in reports:
            print(r + "\n")
    print(f"== {len(fails)} failure(s)\n")
    for f in fails:
        print("  " + f)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
