#!/usr/bin/env python3
"""Every backticked identifier on every page must exist in the decompile.

"Verified against 1.21.11" is a test, not a claim: this walks `src/**/*.md`,
collects every `` `Name` `` / `` `Name.member` `` / `` `pkg/path` `` and
checks it against the remapped source tree at `MC_SOURCE` (default
`d:/pvpmod/reference/minecraft`). A name is accepted if it is a class file
in the tree, a member (method or field) declared in that class, a package
directory under `net/minecraft`, or in the allow-list of non-Minecraft
identifiers below.

Usage:
    python tools/verify_names.py [--src src] [--mc-source PATH]
Exit 1 with every unresolved name listed.
"""
from __future__ import annotations

import argparse
import os
import re
import sys

ALLOW = {
    # Java / Netty / Brigadier / library names a page may reasonably use.
    "Thread", "Runnable", "Executor", "CompletableFuture", "Channel", "ChannelHandler",
    "ByteBuf", "EventLoop", "Netty", "Brigadier", "CommandDispatcher", "Gson", "JSON", "NBT",
    "partialTick", "Mixin", "Yarn", "Mojang",
}

TICK = re.compile(r"`([A-Za-z_][A-Za-z0-9_./$]*)`")


def load_index(root: str):
    classes: dict[str, list[str]] = {}
    packages: set[str] = set()
    base = os.path.join(root, "net", "minecraft")
    for dirpath, _dirs, files in os.walk(base):
        rel = os.path.relpath(dirpath, base).replace(os.sep, "/")
        if rel != ".":
            packages.add(rel)
        for f in files:
            if f.endswith(".java"):
                classes.setdefault(f[:-5], []).append(os.path.join(dirpath, f))
    return classes, packages


MEMBER = re.compile(r"\b(?:[A-Za-z_][A-Za-z0-9_<>\[\], ?]*\s+)?([A-Za-z_][A-Za-z0-9_]*)\s*(?:\(|=|;)")


def members_of(paths: list[str]) -> set[str]:
    names: set[str] = set()
    for p in paths:
        with open(p, encoding="utf-8", errors="replace") as fh:
            for line in fh:
                s = line.strip()
                if s.startswith(("//", "*", "/*", "import ", "package ")):
                    continue
                for m in MEMBER.finditer(s):
                    names.add(m.group(1))
    return names


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", default="src")
    ap.add_argument("--mc-source", default=os.environ.get("MC_SOURCE", "d:/pvpmod/reference/minecraft"))
    args = ap.parse_args()
    if not os.path.isdir(os.path.join(args.mc_source, "net", "minecraft")):
        print(f"no decompile at {args.mc_source} (set MC_SOURCE)", file=sys.stderr)
        return 2
    classes, packages = load_index(args.mc_source)
    member_cache: dict[str, set[str]] = {}
    bad: list[str] = []
    checked = 0
    for dirpath, _d, files in os.walk(args.src):
        for f in files:
            if not f.endswith(".md"):
                continue
            page = os.path.join(dirpath, f)
            with open(page, encoding="utf-8") as fh:
                text = fh.read()
            for m in TICK.finditer(text):
                name = m.group(1)
                checked += 1
                if name in ALLOW:
                    continue
                if "/" in name:
                    if name.strip("/") in packages or name.split("/")[-1] in classes:
                        continue
                    bad.append(f"{page}: `{name}` (no such package or class)")
                    continue
                cls, _, member = name.partition(".")
                cls = cls.split("$")[0]
                if cls not in classes:
                    bad.append(f"{page}: `{name}` (no class {cls})")
                    continue
                if member:
                    if cls not in member_cache:
                        member_cache[cls] = members_of(classes[cls])
                    if member.split("(")[0] not in member_cache[cls]:
                        bad.append(f"{page}: `{name}` (no member {member} on {cls})")
    if bad:
        print("\n".join(bad))
        print(f"\n{len(bad)} unresolved of {checked} names")
        return 1
    print(f"all {checked} names resolve against {args.mc_source}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
