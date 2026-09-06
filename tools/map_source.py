#!/usr/bin/env python3
"""The atlas: macro views of the decompile — where the code is, where the mass
is, what everything imports, what extends what — as markdown tables and SVG
figures that the pages under src/maps/ include.

Usage:
    python tools/map_source.py             # (re)write everything under src/generated/
    python tools/map_source.py packages    # print one view's table to stdout instead
    python tools/map_source.py biggest | fanin | hierarchy | parts

What is written (nothing under src/generated/ is hand-edited):
    packages-depth3.md, packages-depth4.md   class + line counts per package, client-only vs shared
    biggest.md                               the largest classes by line count
    fanin.md                                 the most-imported classes (the hubs), libraries included
    hierarchy-classes.md, hierarchy-interfaces.md   the widest inheritance trees, by root kind
    parts.md                                 the thirteen parts as package sets (PARTS below), with their totals
    part-<dir>.md                            one phrase per part, "**N classes and M lines**", no trailing
                                             newline, for a landing page to {{#include}} mid-sentence
    packages-treemap.svg                     the jar as a treemap: area = lines, colour = jar, hatch = skipped
    biggest.svg, fanin.svg                   the two tables above as bars
    tree-<Root>.svg                          the class hierarchy under each root in TREE_ROOTS, with counts

How things are counted, because the pages say so and pass 4 re-derives them:
a *class* is one .java file (nested types are not counted); a *line* is one
line of the decompiled file; a class is *shared* if the server jar also ships
it (reference/<ver>/server-classes.txt) and *client-only* otherwise; *fan-in*
is the number of files whose `net.minecraft` or `com.mojang` import statements
name the class (the JDK and the annotations are not counted); a *descendant*
is any type reachable through `extends`/`implements` declarations, nested
types included, resolved per file so that two classes of the same simple name
stay two classes. MC_SOURCE points at the decompile (default reference/26.2).

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
    "com/mojang/blaze3d/audio",
    "net/minecraft/references",
)

# The hierarchies drawn as trees, in the order the parts teach them.
TREE_ROOTS = ("Entity", "Block", "Item", "Screen", "EntityRenderState")
TREE_DEPTH = 3

# The thirteen parts as sets of packages — the *where each part lives* table on
# src/maps/packages.md, made the authority (pass-5 planning session). Each entry
# is a directory under src/systems, the part's numeral and title, and what the
# part covers: `pkg` is the package and everything under it, `pkg/.` only the
# files directly in it, `path/Class.java` one file, and `-pkg` subtracts a
# sub-package another part owns. SKIPPED packages are never counted. A package two
# parts share (server/level is Parts III and IV; client/multiplayer is IX and X)
# is counted in both, and parts.md says so. From this one mapping the atlas writes
# parts.md (the table) and part-<dir>.md (one phrase per part, "N classes and M
# lines", for a landing page to {{#include}} inside its size sentence), and
# tools/pass5_coverage.py reads the same mapping for the coverage question, so a
# landing page's count and the coverage population cover the same packages.
# They do not report the same number, and pass-5 session B found out the hard
# way when Part I read 7 classes here and 6 there. The counts here are *files*,
# the convention systems/anatomy/what-this-book-skips.md states for its own
# table; pass5_coverage.py drops package-info.java, because its population is
# what a page could name and a package-info is not nameable. Every part with a
# package-info.java in one of its directories therefore reads one class and a
# few lines larger here. Keep both, and say which you mean.
PARTS = (
    ("anatomy", "I", "Anatomy",
     ("net/minecraft/client/main", "net/minecraft/client/Minecraft.java",
      "net/minecraft/server/Main.java", "net/minecraft/server/MinecraftServer.java")),
    ("foundations", "II", "Foundations",
     ("net/minecraft/core", "net/minecraft/resources", "net/minecraft/tags", "net/minecraft/nbt",
      "net/minecraft/server/packs", "net/minecraft/util", "net/minecraft/world/flag")),
    ("server", "III", "The server",
     ("net/minecraft/server/.", "net/minecraft/server/level", "net/minecraft/server/players",
      "net/minecraft/server/dedicated")),
    ("world", "IV", "The world",
     ("net/minecraft/world/level/chunk", "net/minecraft/world/level/lighting", "net/minecraft/world/ticks",
      "net/minecraft/world/level/gameevent", "net/minecraft/world/level/entity",
      "net/minecraft/world/level/material", "net/minecraft/world/attribute", "net/minecraft/world/timeline",
      "net/minecraft/world/clock", "net/minecraft/world/level/border", "net/minecraft/server/level")),
    ("blocks", "V", "Blocks",
     ("net/minecraft/world/level/block", "net/minecraft/world/level/redstone")),
    ("entities", "VI", "Entities",
     ("net/minecraft/world/entity", "-net/minecraft/world/entity/player", "net/minecraft/network/syncher",
      "net/minecraft/world/level/pathfinder", "net/minecraft/world/damagesource", "net/minecraft/world/effect")),
    ("items", "VII", "Items and inventories",
     ("net/minecraft/world/item", "net/minecraft/world/inventory", "net/minecraft/world/level/storage/loot")),
    ("player", "VIII", "The player",
     ("net/minecraft/world/entity/player", "net/minecraft/world/food",
      "net/minecraft/server/level/ServerPlayer.java", "net/minecraft/client/player")),
    ("networking", "IX", "Networking",
     ("net/minecraft/network", "-net/minecraft/network/syncher", "net/minecraft/server/network",
      "net/minecraft/client/multiplayer")),
    ("client", "X", "The client",
     ("net/minecraft/client/.", "net/minecraft/client/gui", "net/minecraft/client/multiplayer",
      "net/minecraft/client/sounds", "net/minecraft/client/resources", "net/minecraft/client/player",
      "net/minecraft/client/input", "net/minecraft/client/server")),
    ("rendering", "XI", "Rendering",
     ("net/minecraft/client/renderer", "net/minecraft/client/model", "net/minecraft/client/particle",
      "com/mojang/blaze3d")),
    ("worldgen", "XII", "World generation",
     ("net/minecraft/world/level/levelgen", "net/minecraft/world/level/biome")),
    ("commands", "XIII", "Commands and data packs",
     ("net/minecraft/commands", "net/minecraft/server/commands", "net/minecraft/server/dialog",
      "net/minecraft/server/permissions", "net/minecraft/server/bossevents", "net/minecraft/advancements",
      "net/minecraft/gametest", "net/minecraft/world/scores", "net/minecraft/client/gui/screens/dialog")),
)


def in_part(rel: str, spec: tuple) -> bool:
    """Is the file at `rel` (e.g. net/minecraft/world/level/chunk/LevelChunk.java) in the part?"""
    if is_skipped(rel.rsplit("/", 1)[0]):
        return False
    hit = False
    for entry in spec:
        neg = entry.startswith("-")
        e = entry[1:] if neg else entry
        if e.endswith(".java"):
            match = rel == e
        elif e.endswith("/."):
            match = rel.rsplit("/", 1)[0] == e[:-2]
        else:
            match = rel == e or rel.startswith(e + "/")
        if match:
            hit = not neg
    return hit


def part_files(files, spec: tuple):
    """[(rel, text, shared)] of the decompile that the part covers."""
    return [(rel, text, shared) for rel, text, shared in files if in_part(rel, spec)]


def part_rows(files):
    """[(dir, numeral, title, classes, client_only, lines, spec)] in book order."""
    rows = []
    for d, numeral, title, spec in PARTS:
        mine = part_files(files, spec)
        rows.append((d, numeral, title, len(mine), sum(0 if s else 1 for _r, _t, s in mine),
                     sum(t.count("\n") for _r, t, _s in mine), spec))
    return rows

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
    """(rel, name) -> (kind, raw parents, rel, shared) for every top-level and nested type.

    Keyed by file *and* simple name. Keying by simple name alone — which is what this did
    until pass-4 session A — silently merges the two `WarningScreen`s and the two `Pos`
    packets, and sends every `Outer.Inner` parent to whatever top-level class happens to own
    the simple name `Inner`. The parent strings are kept whole here and resolved below."""
    decls = {}
    for rel, text, shared in files:
        for m in DECL.finditer(text):
            kind, name, ext, impl = m.groups()
            parents = []
            for chunk in (ext, impl):
                if chunk:
                    chunk = re.sub(r"<[^<>]*(?:<[^<>]*>[^<>]*)*>", "", chunk)
                    parents += [c.strip() for c in chunk.split(",") if c.strip()]
            key, n = (rel, name), 1
            while key in decls:            # two types of one simple name in one file are two types
                n += 1
                key = (rel, f"{name}#{n}")
            decls[key] = (kind, parents, rel, shared)
    return decls


def hierarchy(files):
    """decls, children map, descendant-count map — all keyed by (rel, name)."""
    decls = parse_decls(files)
    byname = defaultdict(list)
    toplevel = {}
    for key in decls:
        rel, name = key
        byname[name].append(key)
        if rel.rsplit("/", 1)[-1][:-5] == name:
            toplevel[name] = key

    def resolve(rel, ref):
        """A parent reference as written, to the type it names: a nested type of its
        qualifier's file, else one declared in the same file, else the top-level class."""
        segs = ref.split(".")
        last = segs[-1]
        if len(segs) > 1 and segs[0] in ("net", "com", "java", "javax", "org", "it", "io"):
            path = "/".join(segs) + ".java"       # fully qualified: resolve by path, not by name
            return (path, last) if (path, last) in decls else None
        if len(segs) > 1:
            for owner in ([toplevel[segs[-2]]] if segs[-2] in toplevel else []) + byname.get(segs[-2], []):
                if (owner[0], last) in decls:
                    return (owner[0], last)
        if (rel, last) in decls:
            return (rel, last)
        same_pkg = (rel.rsplit("/", 1)[0] + "/" + last + ".java", last)
        if same_pkg in decls:
            return same_pkg
        if last in toplevel and len([k for k in byname.get(last, ()) if k == toplevel[last]]) == 1                 and len([k for k in byname.get(last, ()) if k[0].endswith("/" + last + ".java")]) == 1:
            return toplevel[last]
        candidates = byname.get(last)
        return candidates[0] if candidates and len(candidates) == 1 else None

    children = defaultdict(set)
    for key, (_k, parents, rel, _s) in decls.items():
        for ref in parents:
            p = resolve(rel, ref)
            if p is not None:
                children[p].add(key)
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

    counts = {key: len(descendants(key)) for key in decls}
    return decls, children, counts


def hierarchy_rows(files, kinds, top=30, min_desc=15):
    decls, children, counts = hierarchy(files)
    rows = []
    for key, (kind, _p, rel, _s) in decls.items():
        if kind in kinds and counts[key] >= min_desc and children.get(key):
            rows.append((counts[key], len(children[key]), key[1], kind, os.path.dirname(rel)))
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


def spec_text(spec: tuple) -> str:
    """The part's package set as the table shows it: `pkg`, `pkg` (itself only), `Class`, minus `pkg`.

    The subtractions come last, after every addition, and share one *minus*. Written
    inline a subtraction used to sit where it appears in the spec, so a `-pkg` followed
    by more packages read as though *minus* governed the whole tail — Parts VI and IX
    each looked as if they excluded four packages they include.
    """
    def cell(entry: str) -> str:
        short = entry.replace("net/minecraft/", "")
        if entry.endswith(".java"):
            return f"`{short[:-5].rsplit('/', 1)[-1]}`"
        if entry.endswith("/."):
            return f"`{short[:-2]}` (itself only)"
        return f"`{short}`"

    add = [cell(e) for e in spec if not e.startswith("-")]
    sub = [cell(e[1:]) for e in spec if e.startswith("-")]
    text = ", ".join(add)
    if len(sub) == 1:
        text += ", minus " + sub[0]
    elif sub:
        text += ", minus " + ", ".join(sub[:-1]) + " and " + sub[-1]
    return text


def md_parts(files):
    out = ["| part | packages | classes | client-only | lines |", "|---|---|---:|---:|---:|"]
    total = [0, 0, 0]
    for d, numeral, title, n, c, l, spec in part_rows(files):
        out.append(f"| {numeral} · {title} | {spec_text(spec)} | {fmt(n)} | {fmt(c)} | {fmt(l)} |")
        total[0] += n; total[1] += c; total[2] += l
    out.append(f"| **the thirteen parts, with the shared packages counted twice** | | {fmt(total[0])} | {fmt(total[1])} | {fmt(total[2])} |")
    return "\n".join(out) + "\n"


def part_phrase(n: int, l: int) -> str:
    """The size sentence's payload, for a landing page to include: `**473 classes and 43,896 lines**`."""
    return f"**{fmt(n)} classes and {fmt(l)} lines**"


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
        if is_skipped(g) and not (iw > 0 and ih > 0):
            # a skipped depth-3 package too small for a leaf (gizmos, realms) is hatched as a whole,
            # so the atlas's "hatched boxes" promise holds for every skipped package (session O)
            out.append(f'<rect class="skip" x="{gx:.1f}" y="{gy:.1f}" width="{gw:.1f}" height="{gh:.1f}"/>')
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

    def order(key):
        return (-counts[key], key[1])

    def layout(key, depth, parent):
        name = key[1]
        idx = len(nodes)
        kids = sorted(children.get(key, ()), key=order)
        internal = [k for k in kids if counts[k] > 0]
        leaves = [k for k in kids if counts[k] == 0]
        label = f"{name} ({counts[key]})" if counts[key] else name
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
            leaf_names = [k[1] for k in leaves]
            if len(leaves) == 1:
                lab, cls = leaf_names[0], "node"
            else:
                names = ", ".join(leaf_names[:3]) + (", …" if len(leaves) > 3 else "")
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
    out = svg_open(W, H, f"The class hierarchy under {root[1]}: each node shows how many types descend from it")
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
        elif view == "parts":
            print(md_parts(files))
        elif view == "probe":
            # the PARTS grammar does what its comment says: recursive, itself-only, one file, subtract, skipped
            spec = ("net/minecraft/server/.", "net/minecraft/world/entity", "-net/minecraft/world/entity/player",
                    "net/minecraft/client/Minecraft.java")
            cases = [("net/minecraft/server/MinecraftServer.java", True), ("net/minecraft/server/level/ServerLevel.java", False),
                     ("net/minecraft/world/entity/Entity.java", True), ("net/minecraft/world/entity/monster/Zombie.java", True),
                     ("net/minecraft/world/entity/player/Player.java", False), ("net/minecraft/client/Minecraft.java", True),
                     ("net/minecraft/client/Options.java", False), ("net/minecraft/util/datafix/Old.java", False)]
            bad = [(rel, want) for rel, want in cases if in_part(rel, spec) != want]
            # and spec_text puts every subtraction after every addition, sharing one "minus":
            # inline, a `-pkg` with packages after it read as excluding them too (Parts VI and IX)
            phrases = [(spec, "`server` (itself only), `world/entity`, `Minecraft`, minus `world/entity/player`"),
                       (("net/minecraft/world/item",), "`world/item`"),
                       (("net/minecraft/a", "-net/minecraft/b", "net/minecraft/c", "-net/minecraft/d"),
                        "`a`, `c`, minus `b` and `d`")]
            bad += [(s, want, spec_text(s)) for s, want in phrases if spec_text(s) != want]
            print("probe: OK" if not bad else f"PROBE FAILED: {bad}")
            sys.exit(1 if bad else 0)
        else:
            sys.exit(__doc__)
        return
    write("packages-depth3.md", md_packages(files, 3))
    write("packages-depth4.md", md_packages(files, 4))
    write("biggest.md", md_biggest(files))
    write("fanin.md", md_fanin(files))
    write("hierarchy-classes.md", md_hierarchy(files, ("class",)))
    write("hierarchy-interfaces.md", md_hierarchy(files, ("interface",)))
    write("parts.md", md_parts(files))
    for d, _numeral, _title, n, _c, l, _spec in part_rows(files):
        # no trailing newline: the phrase is included mid-sentence by a landing page
        os.makedirs(GEN, exist_ok=True)
        with open(os.path.join(GEN, f"part-{d}.md"), "w", encoding="utf-8", newline="\n") as fh:
            fh.write(part_phrase(n, l))
        print(f"wrote src/generated/part-{d}.md")
    write("packages-treemap.svg", svg_treemap(files))
    write("biggest.svg", svg_biggest(files))
    write("fanin.svg", svg_fanin(files))
    decls, children, counts = hierarchy(files)
    tops = {name: key for key in decls for name in [key[1]] if key[0].rsplit("/", 1)[-1][:-5] == name}
    for root in TREE_ROOTS:
        if root in tops:
            write(f"tree-{root}.svg", svg_tree(tops[root], decls, children, counts))
        else:
            print(f"no such root: {root}", file=sys.stderr)


if __name__ == "__main__":
    main()
