#!/usr/bin/env python3
"""Macro views of the decompile: where the code is, what extends what, who
depends on whom. Prints markdown; redirect to src/maps/<view>.md.

Usage:
    python tools/map_source.py packages   # class + line counts per package, client-only vs shared
    python tools/map_source.py biggest    # largest classes by line count
    python tools/map_source.py hierarchy  # the widest inheritance trees (roots with most descendants)
    python tools/map_source.py fanin      # most-imported classes (the hubs)
    python tools/map_source.py all

MC_SOURCE points at the extracted decompile (default reference/26.2). A class
is "shared" if the server jar also contains it (reference/<ver>/server-classes.txt),
else "client-only".
"""
from __future__ import annotations

import os
import re
import sys
from collections import Counter, defaultdict

ROOT = os.environ.get("MC_SOURCE", os.path.join(os.path.dirname(__file__), "..", "reference", "26.2"))
ROOT = os.path.abspath(ROOT)

DECL = re.compile(
    r"^(?:public |protected |private |abstract |final |static |sealed |non-sealed )*"
    r"(class|interface|enum|record)\s+([A-Za-z_][A-Za-z0-9_]*)"
    r"(?:<[^{]*?>)?\s*(?:extends\s+([^{]+?))?\s*(?:implements\s+([^{]+?))?\s*(?:permits[^{]*)?\{",
    re.M,
)
IMPORT = re.compile(r"^import (?:static )?(net\.minecraft\.[\w.]+|com\.mojang\.(?:blaze3d|math)\.[\w.]+)", re.M)


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
    return files


def pkg_of(rel: str, depth: int) -> str:
    parts = rel.split("/")[:-1]
    return "/".join(parts[:depth])


def packages(files, depth=3):
    rows = defaultdict(lambda: [0, 0, 0])  # classes, client-only, lines
    for rel, text, shared in files:
        r = rows[pkg_of(rel, depth)]
        r[0] += 1
        r[1] += 0 if shared else 1
        r[2] += text.count("\n")
    print(f"| package (depth {depth}) | classes | client-only | lines |\n|---|---:|---:|---:|")
    for pkg, (n, c, l) in sorted(rows.items(), key=lambda kv: -kv[1][2]):
        print(f"| `{pkg}` | {n} | {c} | {l:,} |")
    tot = [sum(r[i] for r in rows.values()) for i in range(3)]
    print(f"| **total** | {tot[0]} | {tot[1]} | {tot[2]:,} |")


def biggest(files, n=40):
    rows = sorted(((t.count("\n"), rel, s) for rel, t, s in files), reverse=True)[:n]
    print("| class | lines | side |\n|---|---:|---|")
    for lines, rel, shared in rows:
        print(f"| `{rel[:-5]}` | {lines:,} | {'shared' if shared else 'client'} |")


def parse_decls(files):
    """name -> (kind, parents, rel, shared) for every top-level and nested type."""
    decls = {}
    for rel, text, shared in files:
        for m in DECL.finditer(text):
            kind, name, ext, impl = m.groups()
            parents = []
            for chunk in (ext, impl):
                if chunk:
                    # strip generics before splitting on commas
                    chunk = re.sub(r"<[^<>]*(?:<[^<>]*>[^<>]*)*>", "", chunk)
                    parents += [c.strip().split(".")[-1] for c in chunk.split(",") if c.strip()]
            decls.setdefault(name, (kind, parents, rel, shared))
    return decls


def hierarchy(files, top=40, min_children=15):
    decls = parse_decls(files)
    children = defaultdict(set)
    for name, (_k, parents, _r, _s) in decls.items():
        for p in parents:
            if p in decls:
                children[p].add(name)

    def descendants(root, seen=None):
        seen = seen if seen is not None else set()
        for c in children.get(root, ()):
            if c not in seen:
                seen.add(c)
                descendants(c, seen)
        return seen

    rows = []
    for name in decls:
        if len(children.get(name, ())) >= 1:
            d = descendants(name)
            if len(d) >= min_children:
                rows.append((len(d), len(children[name]), name, decls[name][0], decls[name][2]))
    rows.sort(reverse=True)
    print("| root | descendants | direct | kind | where |\n|---|---:|---:|---|---|")
    for d, c, name, kind, rel in rows[:top]:
        print(f"| `{name}` | {d} | {c} | {kind} | `{os.path.dirname(rel)}` |")


def fanin(files, top=60):
    cnt = Counter()
    for _rel, text, _s in files:
        for m in IMPORT.finditer(text):
            cnt[m.group(1)] += 1
    print("| class | imported by |\n|---|---:|")
    for fq, n in cnt.most_common(top):
        print(f"| `{fq.split('.')[-1]}` ({'.'.join(fq.split('.')[:-1])}) | {n} |")


def main():
    view = sys.argv[1] if len(sys.argv) > 1 else "all"
    files = load()
    ver = os.path.basename(ROOT)
    views = {"packages": lambda: (packages(files, 3), print(), packages(files, 4)), "biggest": lambda: biggest(files),
             "hierarchy": lambda: hierarchy(files), "fanin": lambda: fanin(files)}
    for name, fn in views.items():
        if view in (name, "all"):
            print(f"\n## {name} — {ver}\n")
            fn()


if __name__ == "__main__":
    main()
