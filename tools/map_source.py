#!/usr/bin/env python3
"""The atlas: macro views of the decompile — where the code is, where the mass
is, what everything imports, what extends what — as markdown tables and SVG
figures that the pages under src/maps/ include.

Usage:
    python tools/map_source.py             # (re)write everything under src/generated/
    python tools/map_source.py packages    # print one view's table to stdout instead
    python tools/map_source.py biggest | fanin | hierarchy

What is written (nothing under src/generated/ is hand-edited):
    packages-depth3.md, packages-depth4.md   class + line counts per package, client-only vs shared
    biggest.md                               the largest classes by line count
    fanin.md                                 the most-imported classes (the hubs), libraries included
    hierarchy-classes.md, hierarchy-interfaces.md   the widest inheritance trees, by root kind
    packages-treemap.svg                     the jar as a treemap: area = lines, colour = jar, hatch = skipped
    biggest.svg, fanin.svg                   the two tables above as bars
    tree-<Root>.svg                          the class hierarchy under each root in TREE_ROOTS, with counts

How things are counted, because the pages say so and pass 4 re-derives them:
a *class* is one .java file (nested types are not counted); a *line* is one
line of the decompiled file; a class is *shared* if the server jar also ships
it (reference/<ver>/server-classes.txt) and *client-only* otherwise; *fan-in*
is the number of files whose import statements name the class; a *descendant*
is any type reachable through `extends`/`implements` declarations, nested
types included. MC_SOURCE points at the decompile (default reference/26.2).

The SVGs carry classes only (svg.mapfig, .shared, .client, .lib, .skip); every
colour, font and theme lives in custom.css, and text is currentColor so the
five mdBook themes and the zoom overlay all read. No blank lines are emitted,
so an SVG survives being included inside an HTML block.
"""
from __future__ import annotations

import os
import re
import sys
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.environ.get("MC_SOURCE", os.path.join(HERE, "..", "reference", "26.2")))
GEN = os.path.join(HERE, "..", "src", "generated")

# The packages the book skips (Part I, *what this book skips*); hatched on the treemap.
SKIPPED = (
    "net/minecraft/util/datafix", "net/minecraft/util/filefix", "net/minecraft/util/profiling",
    "net/minecraft/client/telemetry", "net/minecraft/client/data", "net/minecraft/data",
    "net/minecraft/server/jsonrpc", "net/minecraft/server/rcon",
    "com/mojang/realmsclient", "net/minecraft/realms", "net/minecraft/stats", "net/minecraft/gizmos",
    "net/minecraft/references",
)

# The hierarchies drawn as trees, in the order the parts teach them.
TREE_ROOTS = ("Entity", "Block", "Item", "Screen")
TREE_DEPTH = 3

DECL = re.compile(
    r"^[ \t]*(?:public |protected |private |abstract |final |static |sealed |non-sealed )*"
    r"(class|interface|enum|record)\s+([A-Za-z_][A-Za-z0-9_]*)"
    r"(?:<[^{]*?>)?\s*(?:\([^{]*?\))?\s*(?:extends\s+([^{]+?))?\s*(?:implements\s+([^{]+?))?\s*(?:permits[^{]*)?\{",  # the parenthesis is a record header
    re.M,
)
IMPORT = re.compile(r"^import (?:static )?((?:net\.minecraft|com\.mojang)\.[\w.]+)", re.M)


# ----------------------------------------------------------------------------
# loading

def walk():
    for base in ("net", "com"):
        for dp, _, files in os.walk(os.path.join(ROOT, base)):
            for f in files:
                if f.endswith(".java"):
                    p = os.path.join(dp, f)
                    yield os.path.relpath(p, ROOT).replace(os.sep, "/"), p


def load():
    srv_path = os.path.join(ROOT, "server-classes.txt")
    server = set(open(srv_path).read().split()) if os.path.exists(srv_path) else set()
    files = []
    for rel, p in walk():
        with open(p, encoding="utf-8", errors="replace") as fh:
            text = fh.read()
        files.append((rel, text, rel in server))
    files.sort()
    return files


def pkg_of(rel: str, depth: int) -> str:
    return "/".join(rel.split("/")[:-1][:depth])


def is_skipped(pkg: str) -> bool:
    return any(pkg == s or pkg.startswith(s + "/") for s in SKIPPED)


def fmt(n: int) -> str:
    return f"{n:,}"


# ----------------------------------------------------------------------------
# the four views as rows

def package_rows(files, depth):
    """[(pkg, classes, client_only, lines)] sorted by lines, descending."""
    rows = defaultdict(lambda: [0, 0, 0])
    for rel, text, shared in files:
        r = rows[pkg_of(rel, depth)]
        r[0] += 1
        r[1] += 0 if shared else 1
        r[2] += text.count("\n")
    return sorted(((p, *v) for p, v in rows.items()), key=lambda r: -r[3])


def biggest_rows(files, n=40):
    """[(rel-without-.java, lines, shared)]"""
    rows = sorted(((t.count("\n"), rel, s) for rel, t, s in files), reverse=True)[:n]
    return [(rel[:-5], lines, shared) for lines, rel, shared in rows]


def fanin_rows(files, top=60):
    """[(display, package, importers, kind)] — kind is shared / client / library."""
    by_rel = {rel[:-5]: shared for rel, _t, shared in files}
    cnt = Counter()
    for _rel, text, _s in files:
        for m in IMPORT.finditer(text):
            cnt[m.group(1)] += 1
    out = []
    for fq, n in cnt.most_common(top):
        parts = fq.split(".")
        kind, display, pkg = "library", parts[-1], ".".join(parts[:-1])
        for cut in range(len(parts), 1, -1):  # longest prefix that is a file: the rest is a nested type
            rel = "/".join(parts[:cut])
            if rel in by_rel:
                kind = "shared" if by_rel[rel] else "client"
                display = ".".join(parts[cut - 1:])
                pkg = ".".join(parts[:cut - 1])
                break
        out.append((display, pkg, n, kind))
    return out


def parse_decls(files):
    """name -> (kind, parents, rel, shared) for every top-level and nested type.

    Types are keyed by simple name because that is how `extends` names them. When a
    nested type shares a simple name with a top-level class (blaze3d has a nested
    `Block`, many classes a nested `Builder`), the top-level one wins; among nested
    ones the first file wins."""
    decls = {}
    for rel, text, shared in files:
        top = rel.rsplit("/", 1)[-1][:-5]
        for m in DECL.finditer(text):
            kind, name, ext, impl = m.groups()
            parents = []
            for chunk in (ext, impl):
                if chunk:
                    chunk = re.sub(r"<[^<>]*(?:<[^<>]*>[^<>]*)*>", "", chunk)
                    parents += [c.strip().split(".")[-1] for c in chunk.split(",") if c.strip()]
            if name == top or name not in decls:
                decls[name] = (kind, parents, rel, shared)
    return decls


def hierarchy(files):
    """decls, children map, descendant-count map."""
    decls = parse_decls(files)
    children = defaultdict(set)
    for name, (_k, parents, _r, _s) in decls.items():
        for p in parents:
            if p in decls:
                children[p].add(name)
    memo = {}

    def descendants(root, stack=()):
        if root in memo:
            return memo[root]
        seen = set()
        for c in children.get(root, ()):
            if c not in stack:
                seen.add(c)
                seen |= descendants(c, stack + (root,))
        memo[root] = seen
        return seen

    counts = {name: len(descendants(name)) for name in decls}
    return decls, children, counts


def hierarchy_rows(files, kinds, top=30, min_desc=15):
    decls, children, counts = hierarchy(files)
    rows = []
    for name, (kind, _p, rel, _s) in decls.items():
        if kind in kinds and counts[name] >= min_desc and children.get(name):
            rows.append((counts[name], len(children[name]), name, kind, os.path.dirname(rel)))
    rows.sort(key=lambda r: (-r[0], -r[1], r[2]))
    return rows[:top]


# ----------------------------------------------------------------------------
# markdown

def md_packages(files, depth):
    rows = package_rows(files, depth)
    out = [f"| package (depth {depth}) | classes | client-only | lines |", "|---|---:|---:|---:|"]
    out += [f"| `{p}` | {n} | {c} | {fmt(l)} |" for p, n, c, l in rows]
    tot = [sum(r[i] for r in rows) for i in (1, 2, 3)]
    out.append(f"| **total** | {tot[0]} | {tot[1]} | {fmt(tot[2])} |")
    return "\n".join(out) + "\n"


def md_biggest(files):
    out = ["| class | lines | side |", "|---|---:|---|"]
    out += [f"| `{rel}` | {fmt(lines)} | {'shared' if s else 'client'} |" for rel, lines, s in biggest_rows(files)]
    return "\n".join(out) + "\n"


def md_fanin(files):
    out = ["| class | package | imported by | side |", "|---|---|---:|---|"]
    out += [f"| `{d}` | `{p}` | {n} | {k} |" for d, p, n, k in fanin_rows(files)]
    return "\n".join(out) + "\n"


def md_hierarchy(files, kinds):
    out = ["| root | descendants | direct | kind | where |", "|---|---:|---:|---|---|"]
    out += [f"| `{name}` | {d} | {c} | {kind} | `{where}` |" for d, c, name, kind, where in hierarchy_rows(files, kinds)]
    return "\n".join(out) + "\n"


# ----------------------------------------------------------------------------
# svg helpers

def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def text_w(s: str, size: float) -> float:
    return len(s) * size * 0.58


def svg_open(w, h, title):
    return [f'<svg class="mapfig" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
            f'width="{w}" height="{h}" role="img" aria-label="{esc(title)}">',
            f"<title>{esc(title)}</title>"]


def write(name: str, body: str):
    os.makedirs(GEN, exist_ok=True)
    path = os.path.join(GEN, name)
    body = "\n".join(line for line in body.split("\n") if line.strip())  # no blank lines: it is included inside an HTML block
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(body + "\n")
    print(f"wrote {os.path.relpath(path, os.path.join(HERE, '..'))}")


def squarify(values, x, y, w, h):
    """Bruls/Huizing/van Wijk squarified layout; values sorted descending, all > 0."""
    def worst(row, side):
        s = sum(row)
        if not s or not side:
            return float("inf")
        return max(side * side * max(row) / (s * s), s * s / (side * side * min(row)))

    rects = []
    total = sum(values)
    if total <= 0:
        return [(x, y, 0, 0)] * len(values)
    areas = [v * w * h / total for v in values]
    i = 0
    while i < len(areas):
        vertical_strip = w >= h  # the row is a column on the left, filling the height
        side = h if vertical_strip else w
        row, best, j = [], float("inf"), i
        while j < len(areas):
            cand = row + [areas[j]]
            r = worst(cand, side)
            if r <= best:
                row, best, j = cand, r, j + 1
            else:
                break
        s = sum(row)
        if vertical_strip:
            rw = s / h if h else 0
            yy = y
            for a in row:
                rh = a / rw if rw else 0
                rects.append((x, yy, rw, rh))
                yy += rh
            x, w = x + rw, w - rw
        else:
            rh = s / w if w else 0
            xx = x
            for a in row:
                rw = a / rh if rh else 0
                rects.append((xx, y, rw, rh))
                xx += rw
            y, h = y + rh, h - rh
        i = j
    return rects


# ----------------------------------------------------------------------------
# the treemap

def svg_treemap(files, W=1000, H=600):
    """Groups are depth-3 packages (net/minecraft/world, com/mojang/blaze3d); leaves are depth-4."""
    leaves = defaultdict(lambda: [0, 0, 0])  # leaf pkg -> classes, client-only, lines
    for rel, text, shared in files:
        r = leaves[pkg_of(rel, 4)]
        r[0] += 1
        r[1] += 0 if shared else 1
        r[2] += text.count("\n")
    groups = defaultdict(list)
    for leaf, (n, c, l) in leaves.items():
        groups["/".join(leaf.split("/")[:3])].append((leaf, n, c, l))
    total = sum(v[2] for v in leaves.values())
    gorder = sorted(groups, key=lambda g: -sum(x[3] for x in groups[g]))
    gvals = [sum(x[3] for x in groups[g]) for g in gorder]

    TITLE, PAD, LEGEND = 15, 2, 28
    out = svg_open(W, H + LEGEND, "The 26.2 jar as a treemap of packages: area is lines of decompiled source, colour is which jar ships the package, hatching marks what this book skips")
    out.append('<defs><pattern id="mapfig-hatch" patternUnits="userSpaceOnUse" width="6" height="6" patternTransform="rotate(45)">'
               '<line class="hatch" x1="0" y1="0" x2="0" y2="6"/></pattern></defs>')
    for (gx, gy, gw, gh), g in zip(squarify(gvals, 0, 0, W, H), gorder):
        items = sorted(groups[g], key=lambda x: -x[3])
        gn, gc, gl = (sum(x[i] for x in items) for i in (1, 2, 3))
        side = "client-only" if gc == gn else ("shared" if gc == 0 else f"{gc} client-only")
        out.append(f'<g class="pkg"><title>{esc(g)} — {gn} classes, {fmt(gl)} lines, {side}</title>')
        ix, iy, iw, ih = gx + PAD, gy + TITLE, max(gw - 2 * PAD, 0), max(gh - TITLE - PAD, 0)
        if iw > 0 and ih > 0:
            for (lx, ly, lw, lh), (leaf, n, c, l) in zip(squarify([x[3] for x in items], ix, iy, iw, ih), items):
                cls = "client" if c * 2 > n else "shared"
                short = leaf[len(g) + 1:] if leaf != g else "(itself)"
                lside = "client-only" if c == n else ("shared" if c == 0 else f"{c} of {n} client-only")
                out.append(f'<g class="cell"><title>{esc(leaf)} — {n} classes, {fmt(l)} lines, {lside}'
                           f'{" — skipped by this book" if is_skipped(leaf) else ""}</title>')
                out.append(f'<rect class="{cls}" x="{lx:.1f}" y="{ly:.1f}" width="{lw:.1f}" height="{lh:.1f}"/>')
                if is_skipped(leaf):
                    out.append(f'<rect class="skip" x="{lx:.1f}" y="{ly:.1f}" width="{lw:.1f}" height="{lh:.1f}"/>')
                size = 11
                if lw > text_w(short, size) + 6 and lh > 26:
                    out.append(f'<text x="{lx + lw / 2:.1f}" y="{ly + lh / 2:.1f}" text-anchor="middle" font-size="{size}">{esc(short)}</text>')
                    if lh > 40 and lw > text_w(fmt(l), 9) + 6:
                        out.append(f'<text class="muted" x="{lx + lw / 2:.1f}" y="{ly + lh / 2 + 12:.1f}" text-anchor="middle" font-size="9">{fmt(l)}</text>')
                elif lw > text_w(short, 9) + 4 and lh > 13:
                    out.append(f'<text x="{lx + lw / 2:.1f}" y="{ly + lh / 2 + 3:.1f}" text-anchor="middle" font-size="9">{esc(short)}</text>')
                out.append("</g>")
        out.append(f'<rect class="group" x="{gx:.1f}" y="{gy:.1f}" width="{gw:.1f}" height="{gh:.1f}"/>')
        label = g.replace("net/minecraft/", "").replace("com/mojang/", "mojang/")
        pct = f" {100 * gl / total:.0f}%"
        if gw > text_w(label, 12) + 4:
            if gw > text_w(label + pct, 12) + 8:
                label += pct
            out.append(f'<text class="grouplabel" x="{gx + 4:.1f}" y="{gy + 11.5:.1f}" font-size="12" font-weight="bold">{esc(label)}</text>')
        out.append("</g>")
    # legend
    y = H + 18
    out.append(f'<rect class="shared" x="0" y="{y - 10}" width="14" height="14"/>'
               f'<text x="20" y="{y + 1}" font-size="12">in both jars</text>')
    out.append(f'<rect class="client" x="130" y="{y - 10}" width="14" height="14"/>'
               f'<text x="150" y="{y + 1}" font-size="12">client only</text>')
    out.append(f'<rect class="shared" x="250" y="{y - 10}" width="14" height="14"/><rect class="skip" x="250" y="{y - 10}" width="14" height="14"/>'
               f'<text x="270" y="{y + 1}" font-size="12">hatched: what this book skips</text>')
    out.append(f'<text class="muted" x="{W}" y="{y + 1}" text-anchor="end" font-size="11">{fmt(total)} lines, {sum(v[0] for v in leaves.values())} classes — area is lines of decompiled source</text>')
    out.append("</svg>")
    return "\n".join(out)


# ----------------------------------------------------------------------------
# bars

def svg_bars(rows, title, unit, W=1000, row_h=19, label_w=330):
    """rows: [(label, sublabel, value, cls)]"""
    H = row_h * len(rows) + 8
    out = svg_open(W, H, title)
    mx = max(v for _l, _s, v, _c in rows) or 1
    bar_x, bar_w = label_w + 8, W - label_w - 70
    for i, (label, sub, value, cls) in enumerate(rows):
        y = i * row_h + 4
        w = bar_w * value / mx
        out.append(f'<g><title>{esc(label)} ({esc(sub)}): {fmt(value)} {unit}</title>')
        out.append(f'<text x="{label_w}" y="{y + 13}" text-anchor="end" font-size="12">{esc(label)}'
                   f'<tspan class="muted" font-size="9"> {esc(sub)}</tspan></text>')
        out.append(f'<rect class="{cls}" x="{bar_x}" y="{y + 3}" width="{w:.1f}" height="{row_h - 6}" rx="2"/>')
        out.append(f'<text class="muted" x="{bar_x + w + 5:.1f}" y="{y + 13}" font-size="11">{fmt(value)}</text>')
        out.append("</g>")
    out.append("</svg>")
    return "\n".join(out)


def svg_biggest(files, n=30):
    rows = []
    for rel, lines, shared in biggest_rows(files, n):
        parts = rel.split("/")
        rows.append((parts[-1], "/".join(parts[2:-1]), lines, "shared" if shared else "client"))
    return svg_bars(rows, f"The {n} largest classes of 26.2 by lines of decompiled source", "lines")


def svg_fanin(files, n=30):
    rows = [(d, p.replace("net.minecraft.", ""), c, {"shared": "shared", "client": "client", "library": "lib"}[k])
            for d, p, c, k in fanin_rows(files, n)]
    return svg_bars(rows, f"The {n} most-imported classes of 26.2: how many files import each", "importing files")


# ----------------------------------------------------------------------------
# trees

def svg_tree(root, decls, children, counts, max_depth=TREE_DEPTH, row_h=16, col_w=210):
    """A left-to-right tree under `root`. Subclasses with no subclasses of their own are folded
    into one node per parent; nodes at max_depth show their count and stop."""
    rows = []  # terminal nodes in draw order, each (depth, label, cls)
    nodes = []  # (depth, y, label, cls, parent_index)

    def order(name):
        return (-counts[name], name)

    def layout(name, depth, parent):
        idx = len(nodes)
        kids = sorted(children.get(name, ()), key=order)
        internal = [k for k in kids if counts[k] > 0]
        leaves = [k for k in kids if counts[k] == 0]
        label = f"{name} ({counts[name]})" if counts[name] else name
        if depth >= max_depth or not kids:
            nodes.append([depth, len(rows) * row_h, label, "node", parent])
            rows.append(name)
            return idx
        nodes.append([depth, 0, label, "node", parent])
        first = last = None
        for k in internal:
            c = layout(k, depth + 1, idx)
            first = c if first is None else first
            last = c
        if leaves:
            if len(leaves) == 1:
                lab, cls = leaves[0], "node"
            else:
                names = ", ".join(leaves[:3]) + (", …" if len(leaves) > 3 else "")
                lab, cls = f"{len(leaves)} with no subclasses: {names}", "fold"
            nodes.append([depth + 1, len(rows) * row_h, lab, cls, idx])
            rows.append(lab)
            c = len(nodes) - 1
            first = c if first is None else first
            last = c
        nodes[idx][1] = (nodes[first][1] + nodes[last][1]) / 2
        return idx

    layout(root, 0, None)
    depth_w = defaultdict(float)
    for d, _y, label, _c, _p in nodes:
        depth_w[d] = max(depth_w[d], text_w(label, 12) + 24)
    xs, x = {}, 4
    for d in range(max(depth_w) + 1):
        xs[d] = x
        x += max(depth_w[d], col_w) if d < max(depth_w) else depth_w[d]
    W, H = int(x) + 4, len(rows) * row_h + 8
    out = svg_open(W, H, f"The class hierarchy under {root}: each node shows how many types descend from it")
    for d, y, label, cls, p in nodes:
        px, py = xs[d], y + 12
        if p is not None:
            pd, pyy, plabel = nodes[p][0], nodes[p][1] + 12, nodes[p][2]
            pend = xs[pd] + text_w(plabel, 12) + 6
            mid = xs[d] - 10
            out.append(f'<path class="edge" d="M{pend:.1f} {pyy:.1f} H{mid:.1f} V{py:.1f} H{px - 3:.1f}"/>')
        out.append(f'<text class="{cls}" x="{px:.1f}" y="{py + 4:.1f}" font-size="12">{esc(label)}</text>')
    out.append("</svg>")
    return "\n".join(out)


# ----------------------------------------------------------------------------

def main():
    files = load()
    if len(sys.argv) > 1:
        view = sys.argv[1]
        if view == "packages":
            print(md_packages(files, 3)); print(md_packages(files, 4))
        elif view == "biggest":
            print(md_biggest(files))
        elif view == "fanin":
            print(md_fanin(files))
        elif view == "hierarchy":
            print(md_hierarchy(files, ("class",))); print(md_hierarchy(files, ("interface",)))
        else:
            sys.exit(__doc__)
        return
    write("packages-depth3.md", md_packages(files, 3))
    write("packages-depth4.md", md_packages(files, 4))
    write("biggest.md", md_biggest(files))
    write("fanin.md", md_fanin(files))
    write("hierarchy-classes.md", md_hierarchy(files, ("class",)))
    write("hierarchy-interfaces.md", md_hierarchy(files, ("interface",)))
    write("packages-treemap.svg", svg_treemap(files))
    write("biggest.svg", svg_biggest(files))
    write("fanin.svg", svg_fanin(files))
    decls, children, counts = hierarchy(files)
    for root in TREE_ROOTS:
        if root in decls:
            write(f"tree-{root}.svg", svg_tree(root, decls, children, counts))
        else:
            print(f"no such root: {root}", file=sys.stderr)


if __name__ == "__main__":
    main()
