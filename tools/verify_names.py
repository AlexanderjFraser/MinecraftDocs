#!/usr/bin/env python3
"""Every backticked identifier on every page must exist in the decompile.

"Verified against 26.2" is a test, not a claim: this walks `src/**/*.md`,
collects every `` `Name` `` / `` `Name.member` `` / `` `pkg/path` `` and
checks it against the remapped source tree at `MC_SOURCE` (default
`reference/26.2`, gitignored). A name is accepted if it is a class file in
the tree (`net/minecraft` or `com/mojang`), a member (method or field) declared in that class, a package
directory under `net/minecraft`, or in the allow-list of non-Minecraft
identifiers below.

Usage:
    python tools/verify_names.py [--src src] [--mc-source PATH]
    python tools/verify_names.py --index     # also write src/reference/class-index.md
Exit 1 with every unresolved name listed. `--index` writes the reverse
index (class -> every page that names it) so "which page talks about
ChunkMap" has an answer.
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
    # DataFixerUpper / Brigadier / authlib — Mojang libraries outside the game jar.
    "Codec", "MapCodec", "RecordCodecBuilder", "DataResult", "Dynamic", "DynamicOps",
    "DSL", "Schema", "DataFix", "TypeRewriteRule", "Either", "Pair", "Unit",
    "CommandContext", "CommandSyntaxException", "LiteralArgumentBuilder",
    "RequiredArgumentBuilder", "StringReader", "ArgumentType", "GameProfile",
    # JDK / LWJGL / Netty things a page names as concepts.
    "ForkJoinPool", "ThreadLocal", "GLFW", "OpenGL", "Vulkan", "OpenAL", "ChannelPipeline",
    "ChannelInboundHandler", "NioEventLoopGroup", "EpollEventLoopGroup", "LocalAddress",
    "LocalChannel", "LocalServerChannel", "BooleanSupplier", "Supplier", "Consumer", "Function",
    "Optional", "Set", "Map", "List", "Random", "ImmutableSortedMap",
    # DFU ops / lifecycle, JOML.
    "JsonOps", "Lifecycle", "DataFixer", "Vector3f", "Vector3i", "Matrix4f", "Quaternionf",
    # JDK concurrency / IO, and jtracy (Mojang's Tracy binding, outside the game jar).
    "ConcurrentLinkedQueue", "LinkedHashMap", "LockSupport", "FileChannel", "FileChannel.tryLock",
    "System.exit", "System.in", "Runtime.halt", "DiscontinuousFrame", "TracyClient",
    # JDK collections / fastutil a page names as concepts (Part IV).
    "EnumMap", "BitSet", "AtomicReferenceArray", "ShortList", "AtomicLong", "AtomicReference", "CompletableFuture.allOf", "LongSet", "PriorityQueue", "ArrayDeque", "Semaphore", "AtomicBoolean", "AtomicInteger",
}
FILE_EXT = (".py", ".sh", ".json", ".txt", ".properties", ".mcmeta", ".nbt", ".dat", ".mca", ".png", ".ogg", ".fsh", ".vsh", ".glsl", ".lock", ".dat_old")

TICK = re.compile(r"`([A-Za-z_][A-Za-z0-9_./$]*)`")


def load_index(root: str):
    classes: dict[str, list[str]] = {}
    packages: set[str] = set()
    for base in (os.path.join(root, "net", "minecraft"), os.path.join(root, "com", "mojang")):
        for dirpath, _dirs, files in os.walk(base):
            rel = os.path.relpath(dirpath, root).replace(os.sep, "/")
            packages.add(rel)
            for f in files:
                if f.endswith(".java"):
                    classes.setdefault(f[:-5], []).append(os.path.join(dirpath, f))
    return classes, packages


MEMBER = re.compile(r"\b(?:[A-Za-z_][A-Za-z0-9_<>\[\], ?]*\s+)?([A-Za-z_][A-Za-z0-9_]*)\s*(?:\(|=|;)")
ENUM_CONST = re.compile(r"^([A-Z][A-Z0-9_]*)\s*(?:,|;|\(|\{)")  # enum constants: `Kind.REFERENCE`
RECORD = re.compile(r"\brecord\s+[A-Za-z_][A-Za-z0-9_]*\s*\(")  # record components count as members
NESTED = re.compile(r"(?:class|interface|enum|record)\s+([A-Za-z_][A-Za-z0-9_]*)")  # `Outer.Inner` counts as a member


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
                for m in NESTED.finditer(s):
                    names.add(m.group(1))
                if ENUM_CONST.match(s):  # `A, B, C;` on one line: take them all
                    names.update(re.findall(r"\b[A-Z][A-Z0-9_]*\b", s.split("(")[0]))
                if RECORD.search(s):  # `record Foo(Bar a, int b)` on one line: a and b are members
                    names.update(re.findall(r"([A-Za-z_][A-Za-z0-9_]*)\s*[,)]", s.split("(", 1)[1]))
    return names


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", default="src")
    ap.add_argument("--mc-source", default=os.environ.get("MC_SOURCE", os.path.join(os.path.dirname(__file__), "..", "reference", "26.2")))
    ap.add_argument("--index", action="store_true", help="write src/reference/class-index.md")
    args = ap.parse_args()
    if not os.path.isdir(os.path.join(args.mc_source, "net", "minecraft")):
        print(f"no decompile at {args.mc_source} (set MC_SOURCE)", file=sys.stderr)
        return 2
    classes, packages = load_index(args.mc_source)
    member_cache: dict[str, set[str]] = {}
    bad: list[str] = []
    checked = 0
    mentions: dict[str, set[str]] = {}
    for dirpath, _d, files in os.walk(args.src):
        for f in files:
            if not f.endswith(".md"):
                continue
            page = os.path.join(dirpath, f)
            rel = os.path.relpath(page, args.src).replace(os.sep, "/")
            if rel.startswith("maps/") or (rel.startswith("reference/") and rel != "reference/threads.md"):
                continue  # generated pages are not checked; threads.md is hand-written
            with open(page, encoding="utf-8") as fh:
                text = fh.read()
            for m in TICK.finditer(text):
                name = m.group(1)
                checked += 1
                if name in ALLOW or name.endswith(FILE_EXT):
                    continue
                if "/" in name:
                    n = name.strip("/")
                    if any(p == n or p.endswith("/" + n) for p in packages) or name.split("/")[-1] in classes:
                        continue
                    bad.append(f"{page}: `{name}` (no such package or class)")
                    continue
                cls, _, member = name.partition(".")
                cls = cls.split("$")[0]
                if cls not in classes:
                    bad.append(f"{page}: `{name}` (no class {cls})")
                    continue
                mentions.setdefault(cls, set()).add(rel)
                if member:
                    if cls not in member_cache:
                        member_cache[cls] = members_of(classes[cls])
                    # `Outer.Inner.member`: every segment must be declared somewhere in Outer's file
                    # (nested classes live in the same file, so one member set covers them all).
                    missing = [seg for seg in member.split("(")[0].split(".") if seg not in member_cache[cls]]
                    if missing:
                        bad.append(f"{page}: `{name}` (no member {missing[0]} on {cls})")
    if bad:
        print("\n".join(bad))
        print(f"\n{len(bad)} unresolved of {checked} names")
        return 1
    print(f"all {checked} names resolve against {args.mc_source}")
    if args.index:
        write_index(os.path.join(args.src, "reference", "class-index.md"), mentions)
    return 0


def write_index(path: str, mentions: dict[str, set[str]]) -> None:
    """class -> every page that names it, as a table under src/reference/."""
    out = [
        "# Class index",
        "",
        "Every class a system page names, and the pages that name it. Generated by",
        "`python tools/verify_names.py --index`; regenerated on every deploy.",
        "",
        f"{len(mentions)} classes across {len({p for ps in mentions.values() for p in ps})} pages.",
        "",
        "| class | pages |",
        "|---|---|",
    ]
    for cls in sorted(mentions, key=str.lower):
        links = ", ".join(
            f"[{os.path.splitext(os.path.basename(p))[0]}](../{p})" for p in sorted(mentions[cls])
        )
        out.append(f"| `{cls}` | {links} |")
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(out) + "\n")
    print(f"wrote {path}: {len(mentions)} classes")


if __name__ == "__main__":
    sys.exit(main())
