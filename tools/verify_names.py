#!/usr/bin/env python3
"""Every backticked identifier on every page must exist in the decompile.

"Verified against <version>" is a test, not a claim: this walks `src/**/*.md`,
collects every `` `Name` `` / `` `Name.member` `` / `` `pkg/path` `` and
checks it against the decompile of the release the page's own verified line
names — `reference/<version>`, gitignored — with the library trees that release
pins (`tools/mc_version.py`: `tree`, `lib_roots`, `page_version`); a page with no
verified line is checked against the book's version. `--mc-source` or
`MC_SOURCE` checks every page against one tree instead. A name is accepted if it is a class file in
the tree (`net/minecraft` or `com/mojang`) or in one of the library source
trees under `MC_LIBS` (default `reference/libs`: Brigadier, DataFixerUpper,
authlib — staged by `tools/fetch_libs.sh`), a member (method or field)
declared in that class, a package directory under `net/minecraft`, or in the
allow-list of non-Minecraft identifiers below.

Usage:
    python tools/verify_names.py [--src src] [--mc-source PATH] [--libs PATH]
    python tools/verify_names.py --index     # also write src/reference/class-index.md
    python tools/verify_names.py --current   # also fail if any page is verified against an earlier release
    python tools/verify_names.py --probe     # prove the per-page routing here and in check_figure_names.py
Exit 1 with every unresolved name listed. `--index` writes the reverse
index (class -> every page that names it) so "which page talks about
ChunkMap" has an answer. A page verified against an earlier release than the
book's is listed in a note, and fails only under `--current` (the release's test).
"""
from __future__ import annotations

import argparse
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mc_version  # noqa: E402  (the one place the version is written)

# A reference page whose header carries this was written by a tool and is not checked: gen_reference.py's
# views (their rows read off the decompile; the paragraph above each table is typed and unchecked) and the
# two --index pages (names already checked). Every other page under
# src/reference/ is hand-kept and is checked like a system page (pass-3 session O).
GENERATED_MARK = "Do not edit by hand"

ALLOW = {
    # Java / Netty / Brigadier / library names a page may reasonably use.
    "Thread", "Runnable", "Executor", "CompletableFuture", "ChannelHandler",
    "ByteBuf", "EventLoop", "Netty", "Brigadier", "Gson", "JSON", "NBT",
    "partialTick", "Mixin", "Yarn", "Mojang",
    # DataFixerUpper, Brigadier and authlib names are NOT allow-listed: their source trees
    # are staged under reference/libs/ (tools/fetch_libs.sh) and checked at member level.
    # JDK / LWJGL / Netty things a page names as concepts.
    "ForkJoinPool", "ThreadLocal", "GLFW", "OpenGL", "Vulkan", "OpenAL", "ChannelPipeline",
    "ChannelInboundHandler", "NioEventLoopGroup", "EpollEventLoopGroup", "LocalAddress",
    "LocalChannel", "LocalServerChannel", "BooleanSupplier", "Supplier", "Consumer", "Function",
    "Optional", "Set", "Map", "List", "Random", "ImmutableSortedMap", "ConcurrentHashMap",
    # JOML.
    "Vector3f", "Vector3i", "Matrix4f", "Quaternionf",
    # JDK concurrency / IO, and jtracy (Mojang's Tracy binding, outside the game jar).
    # JDK names Part XIII names as concepts.
    "Predicate", "StackOverflowError", "Instant", "java.nio",
    "ConcurrentLinkedQueue", "LinkedHashMap", "LockSupport", "FileChannel", "FileChannel.tryLock",
    "System.exit", "System.in", "System.out", "System.err", "Runtime.halt", "DiscontinuousFrame", "TracyClient",
    # JDK collections / fastutil a page names as concepts (Part IV).
    "EnumMap", "BitSet", "AtomicReferenceArray", "ShortList", "AtomicLong", "AtomicReference", "CompletableFuture.allOf", "LongSet", "PriorityQueue", "ArrayDeque", "Semaphore", "AtomicBoolean", "AtomicInteger",
}
FILE_EXT = (".py", ".sh", ".json", ".txt", ".properties", ".mcmeta", ".nbt", ".dat", ".mca", ".png", ".ogg", ".fsh", ".vsh", ".glsl", ".lock", ".dat_old")

# A span containing a character this pattern cannot match is skipped in *silence*, so the
# pattern is the gate's real boundary. It admits an argument list and a trailing `*` because
# the corpus writes both (`Class.method(Arg)`, `Gui.render*`); session A recorded that hole
# as settled without fixing it, and session O found two dead 1.21 names living in it.
TICK = re.compile(r"`([A-Za-z_][A-Za-z0-9_./$]*(?:\*|\([A-Za-z0-9_.,<>\[\] ]*\))?)`")


def load_index(root: str, libs: str | list[str] | None = None):
    classes: dict[str, list[str]] = {}
    packages: set[str] = set()
    bases = [os.path.join(root, "net", "minecraft"), os.path.join(root, "com", "mojang")]
    # Mojang's libraries outside the game jar — Brigadier, DataFixerUpper, authlib — live as
    # separate source trees under reference/libs/<name>-<version>/ (see tools/fetch_libs.sh).
    # Their classes and members are checked exactly like the game's; their packages are not
    # (a `pkg/path` on a page always means the game jar). `libs` is either the list of trees the
    # release pins (`mc_version.lib_roots(version)`, since pass 8's session V1) or a directory,
    # every subdirectory of which is read — the behaviour before, which checked a library name
    # against every staged version of the library at once.
    lib_roots: list[str] = []
    if isinstance(libs, (list, tuple)):
        lib_roots = [d for d in libs if os.path.isdir(d)]
    elif libs and os.path.isdir(libs):
        lib_roots = [os.path.join(libs, d) for d in sorted(os.listdir(libs)) if os.path.isdir(os.path.join(libs, d))]
    for base in bases + lib_roots:
        for dirpath, _dirs, files in os.walk(base):
            if base in bases:
                packages.add(os.path.relpath(dirpath, root).replace(os.sep, "/"))
            for f in files:
                if f.endswith(".java"):
                    classes.setdefault(f[:-5], []).append(os.path.join(dirpath, f))
    return classes, packages


MEMBER = re.compile(r"\b(?:[A-Za-z_][A-Za-z0-9_<>\[\], ?]*\s+)?([A-Za-z_][A-Za-z0-9_]*)\s*(?:\(|=|;)")
ENUM_CONST = re.compile(r"^([A-Z][A-Z0-9_]*)\s*(?:,|;|\(|\{)")  # enum constants: `Kind.REFERENCE`
RECORD = re.compile(r"\brecord\s+[A-Za-z_][A-Za-z0-9_]*\s*(?:<[^(]*>)?\s*\(")  # record components count as members — generic records too (`record Foo<T>(...)`)
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


class Trees:
    """The decompile index each page is checked against. By default a page is checked against the
    release its own verified line names (reference/<version>, with that release's pinned libraries),
    so a version pass can move the book a page at a time with every header true; a page with no
    verified line is checked against the book's version. An explicit tree (`--mc-source`, or
    MC_SOURCE — how `version_pass.py --check` measures a new release) checks every page against it."""

    def __init__(self, single: str | None, libs: str | None):
        self.single, self.libs = single, libs
        self.index: dict[str, tuple[dict[str, list[str]], set[str]]] = {}
        self.members: dict[str, dict[str, set[str]]] = {}

    def version_of(self, text: str) -> str:
        return "*" if self.single else (mc_version.page_version(text) or mc_version.VERSION)

    def root(self, version: str) -> str:
        return self.single if version == "*" else mc_version.tree(version)

    def present(self, version: str) -> bool:
        return os.path.isdir(os.path.join(self.root(version), "net", "minecraft"))

    def load(self, version: str):
        if version not in self.index:
            libs = self.libs or (mc_version.libs() if version == "*" else mc_version.lib_roots(version))
            self.index[version] = load_index(self.root(version), libs)
            self.members[version] = {}
        return self.index[version]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", default="src")
    ap.add_argument("--mc-source", default=None,
                    help="check every page against this one tree (default: each page against the release its "
                         "verified line names, reference/<version>; MC_SOURCE does the same as this flag)")
    ap.add_argument("--libs", default=None,
                    help="directory of library source trees (Brigadier, DataFixerUpper, authlib), one per subdirectory "
                         "(default: the trees the page's release pins)")
    ap.add_argument("--index", action="store_true", help="write src/reference/class-index.md")
    ap.add_argument("--current", action="store_true",
                    help=f"fail if any page is verified against an earlier release than {mc_version.VERSION} (the release's test)")
    args = ap.parse_args()
    trees = Trees(args.mc_source or os.environ.get("MC_SOURCE"), args.libs)
    first = "*" if trees.single else mc_version.VERSION
    if not trees.present(first):
        print(f"no decompile at {trees.root(first)} (set MC_SOURCE)", file=sys.stderr)
        return 2
    bad: list[str] = []
    checked = 0
    mentions: dict[str, set[str]] = {}
    behind: dict[str, list[str]] = {}
    for dirpath, _d, files in os.walk(args.src):
        for f in files:
            if not f.endswith(".md"):
                continue
            page = os.path.join(dirpath, f)
            rel = os.path.relpath(page, args.src).replace(os.sep, "/")
            if rel.startswith("generated/"):
                continue  # the atlas tables and figures, written by map_source.py
            with open(page, encoding="utf-8") as fh:
                text = fh.read()
            if rel.startswith("reference/") and GENERATED_MARK in text[:400]:
                continue  # a generated view or index: its rows are read off the decompile, or its names are already checked
            version = trees.version_of(text)
            if version not in ("*", mc_version.VERSION):
                behind.setdefault(version, []).append(rel)
                if not trees.present(version):
                    bad.append(f"{page}: verified against {version}, but there is no decompile at "
                               f"{trees.root(version)} (stage it, or move the page to {mc_version.VERSION})")
                    continue
            classes, packages = trees.load(version)
            member_cache = trees.members[version]
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
                name = name.rstrip("*")
                cls, _, member = name.partition(".")
                nested = cls.split("$")
                cls = nested[0]
                if cls not in classes:
                    bad.append(f"{page}: `{name}` (no class {cls})")
                    continue
                mentions.setdefault(cls, set()).add(rel)
                if member:
                    if cls not in member_cache:
                        member_cache[cls] = members_of(classes[cls])
                    # `Outer.Inner.member`: every segment must be declared somewhere in Outer's file
                    # (nested classes live in the same file, so one member set covers them all).
                    segs = nested[1:] + member.split("(")[0].split(".")
                    missing = [seg for seg in segs if seg not in member_cache[cls]]
                    if missing:
                        bad.append(f"{page}: `{name}` (no member {missing[0]} on {cls})")
    for version, pages in sorted(behind.items()):
        print(f"note: {len(pages)} pages say they are verified against {version}, not {mc_version.VERSION}, "
              f"and were checked against reference/{version}: {', '.join(sorted(pages))}")
    if args.current and behind:
        bad.append(f"--current: {sum(len(p) for p in behind.values())} pages are verified against an earlier release "
                   f"than {mc_version.VERSION}")
    if bad:
        print("\n".join(bad))
        print(f"\n{len(bad)} unresolved of {checked} names")
        return 1
    if checked == 0:
        print(f"no pages under {args.src}", file=sys.stderr)
        return 2
    classes, _packages = trees.load(first)
    known = set(classes)
    for version in trees.index:
        known |= set(trees.index[version][0])
    ambiguous = sorted(c for c in mentions if len(classes.get(c, ())) > 1)
    if ambiguous:
        print(f"note: {len(ambiguous)} names are ambiguous (two files share the simple name), "
              f"so a member resolves against either: {', '.join(ambiguous[:8])}"
              + (" ..." if len(ambiguous) > 8 else ""))
    against = trees.single or (f"reference/{mc_version.VERSION}" + "".join(f" and reference/{v}" for v in sorted(behind)))
    print(f"all {checked} names resolve against {against}")
    if args.index:
        # A class named only inside a figure reaches the index too (pass 7's planning session; the figure
        # parser is check_figure_names.py, which reads the same decompile index).
        try:
            import check_figure_names
            fig = check_figure_names.figure_mentions(args.src, args.mc_source or os.environ.get("MC_SOURCE"), args.libs)
            added = 0
            for cls, pages in fig.items():
                if cls not in known:
                    continue
                before = len(mentions.get(cls, ()))
                mentions.setdefault(cls, set()).update(pages)
                added += len(mentions[cls]) - before
            print(f"class index: {added} page pairs added from figures ({len(fig)} classes named in figures)")
        except Exception as e:  # noqa: BLE001 — the index is still written from the prose if the figure parser fails
            print(f"warning: figure names not indexed ({e})", file=sys.stderr)
        write_index(os.path.join(args.src, "reference", "class-index.md"), mentions)
    return 0


def probe_releases() -> int:
    """Prove the per-page routing in this gate and in check_figure_names.py, on the staged trees: a
    class only an older release has passes on a page verified against that release and fails on a
    page verified against the book's; a class only the book's release has passes there; `--current`
    fails the older page; MC_SOURCE sends every page to one tree. Needs two staged releases."""
    import shutil
    import subprocess
    import tempfile
    here = os.path.dirname(os.path.abspath(__file__))
    ref = os.path.join(mc_version.ROOT, "reference")
    staged = sorted((d for d in os.listdir(ref) if d != mc_version.VERSION and mc_version.present(os.path.join(ref, d))
                     and re.fullmatch(r"\d+\.\d+(\.\d+)?", d)), key=lambda v: [int(x) for x in v.split(".")])
    if not mc_version.present(mc_version.tree()) or not staged:
        print("probe skipped: it needs the book's release and one earlier release staged under reference/")
        return 0
    old = staged[-1]
    old_classes, _ = load_index(mc_version.tree(old), [])
    new_classes, _ = load_index(mc_version.tree(), [])
    humped = re.compile(r"[A-Z][a-z]+[A-Z][A-Za-z]{4,}$")
    only_old = sorted(c for c in set(old_classes) - set(new_classes) if humped.match(c))[0]
    only_new = sorted(c for c in set(new_classes) - set(old_classes) if humped.match(c))[0]
    tmp = tempfile.mkdtemp(prefix="vnprobe-")
    try:
        pages = {
            "old.md": (old, f"`{only_old}` is named here.", f"flowchart TD\n    A[\"{only_old}\"]"),
            "new.md": (mc_version.VERSION, f"`{only_new}` is named here.", f"flowchart TD\n    A[\"{only_new}\"]"),
            "stale.md": (mc_version.VERSION, f"`{only_old}` is named here.", f"flowchart TD\n    A[\"{only_old}\"]"),
        }
        for name, (v, prose, fig) in pages.items():
            with open(os.path.join(tmp, name), "w", encoding="utf-8") as f:
                f.write(f"# P\n\n> Verified against **Minecraft {v}** · Part I · a probe.\n\n{prose}\n\n```mermaid\n{fig}\n```\n")
        env = {k: v for k, v in os.environ.items() if k not in ("MC_SOURCE", "MC_LIBS")}

        def run(tool, *extra, **envx):
            r = subprocess.run([sys.executable, os.path.join(here, tool), "--src", tmp, *extra],
                               capture_output=True, text=True, encoding="utf-8", errors="replace", env={**env, **envx})
            return r.returncode, r.stdout + r.stderr

        checks = []
        rc, out = run("verify_names.py")
        checks.append(("the older page's old class passes against its own release", f"old.md: `{only_old}`" not in out))
        checks.append(("the same class fails on a page verified against the book's release", f"stale.md: `{only_old}`" in out))
        checks.append(("the book's-release class passes on the book's-release page", f"new.md: `{only_new}`" not in out))
        checks.append(("exactly one failure, and the older page is listed in a note", rc == 1 and "1 unresolved" in out and f"verified against {old}" in out))
        rc, out = run("verify_names.py", "--current")
        checks.append(("--current fails the page that is behind", rc == 1 and "--current:" in out))
        rc, out = run("verify_names.py", MC_SOURCE=mc_version.tree())
        checks.append(("MC_SOURCE sends every page to one tree, so the older page fails too",
                       f"old.md: `{only_old}`" in out and f"stale.md: `{only_old}`" in out))
        rc, out = run("check_figure_names.py", "--strict")
        checks.append(("the figure gate: the older page's figure passes, the stale page's fails",
                       rc == 1 and "stale.md" in out and "src/old.md" not in out and "src/new.md" not in out))
        rc, out = run("check_figure_names.py", "--strict", MC_SOURCE=mc_version.tree())
        checks.append(("the figure gate under MC_SOURCE fails the older page's figure too", "old.md" in out and "stale.md" in out))
        ok = True
        for what, passed in checks:
            print(f"{'pass' if passed else 'FAIL'}  {what}")
            ok &= bool(passed)
        print(f"probe ({only_old} only in {old}, {only_new} only in {mc_version.VERSION}): "
              + ("passed" if ok else "FAILED"))
        return 0 if ok else 1
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def page_label(src: str, rel: str) -> str:
    """The name a page goes by in the index. A README is labelled by its own title
    ("VI · Entities", "Reference", "The atlas"), because eleven distinct pages are
    called README and a reader cannot tell them apart."""
    stem = os.path.splitext(os.path.basename(rel))[0]
    if stem != "README":
        return stem
    try:
        with open(os.path.join(src, rel), encoding="utf-8") as fh:
            for line in fh:
                if line.startswith("# "):
                    return line[2:].strip()
    except OSError:
        pass
    return stem


def write_index(path: str, mentions: dict[str, set[str]]) -> None:
    """class -> every page that names it, as a table under src/reference/."""
    src = os.path.dirname(os.path.dirname(path))
    out = [
        "# Class index",
        "",
        "> Generated by `python tools/verify_names.py --index` on every deploy. Do not edit by hand.",
        "",
        "Every class **backticked** on a page — a system page, a Reference page, the atlas, the",
        "introduction or the lecture map — or named inside one of its figures (a lane, a node, a",
        "message; `tools/check_figure_names.py` reads those), and the pages that name it. Outside it:",
        "the generated pages: the eleven views, whose rows are read off the decompile, and the lane index, read off "
        "the page template's key.",
        "",
        f"{len(mentions)} names across {len({p for ps in mentions.values() for p in ps})} pages. A row is a",
        "simple name, not a class: a few names belong to more than one class (there are five",
        "`Main`s), and a few are library classes from Brigadier, DataFixerUpper or authlib.",
        "",
        "| class | pages |",
        "|---|---|",
    ]
    for cls in sorted(mentions, key=str.lower):
        links = ", ".join(f"[{page_label(src, p)}](../{p})" for p in sorted(mentions[cls]))
        out.append(f"| `{cls}` | {links} |")
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(out) + "\n")
    print(f"wrote {path}: {len(mentions)} classes")


if __name__ == "__main__":
    if "--probe" in sys.argv:
        sys.exit(probe_releases())
    sys.exit(main())
