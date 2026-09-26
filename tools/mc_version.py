#!/usr/bin/env python3
"""The one place the book's Minecraft version is written down, for every tool that reads the decompile.

Rule 3 says newest version only, and "verified against <version>" is a test the tools run. Until
pass 8's planning session (2026-09-26) each tool carried its own copy of the version — as the
default decompile path, in a figure title, in `llms.txt`'s preface, on the Open Graph image — so a
version pass was a grep for the number across `tools/`. Now it is one constant here, and the
version pass changes it once (`tools/version_pass.py --flip`).

A page's own verified line is the test's other half. Since pass 8's session V1 the name gates
check each page against the release *its* line names — `reference/<that version>`, with the
libraries that release pins — so a version pass can move the book a page at a time and every
header stays true between commits: a page still describing the old release says so and is checked
against the old tree, while the tree is staged. `--current` on the gates fails any page that is
behind VERSION, which is the release's test. An explicit MC_SOURCE (or `--mc-source`) still checks
every page against that one tree, which is how `version_pass.py --check` measures a new release.

    VERSION          the version the book is verified against ("26.3")
    source()         the decompile tree: $MC_SOURCE, else reference/<VERSION>
    tree(v)          reference/<v>, whatever MC_SOURCE says (the per-page gates use it)
    libs()           the directory of library source trees: $MC_LIBS, else reference/libs
    lib_roots(v)     the library trees release v pins, from reference/<v>/libraries.json
    page_version(t)  the version a page's verified line names, or None

Usage:
    python tools/mc_version.py            # prints the version and where the decompile is, and whether it is there
    python tools/mc_version.py --probe    # proves the overrides, the page line and the library pins
"""
import json
import os
import re
import sys

VERSION = "26.3"
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
LIBRARIES_FILE = "libraries.json"  # {"authlib": "10.0.77", ...}, written by version_pass.py when it stages a tree
HEADER = re.compile(r"Verified against \*\*Minecraft ([0-9][0-9A-Za-z.\-]*)\*\*")


def source(version: str = VERSION) -> str:
    """The decompile for `version`: $MC_SOURCE wins, else reference/<version>."""
    return os.path.abspath(os.environ.get("MC_SOURCE") or os.path.join(ROOT, "reference", version))


def tree(version: str = VERSION) -> str:
    """reference/<version>, ignoring MC_SOURCE: the tree a page's verified line points at."""
    return os.path.abspath(os.path.join(ROOT, "reference", version))


def libs() -> str:
    return os.path.abspath(os.environ.get("MC_LIBS") or os.path.join(ROOT, "reference", "libs"))


def lib_roots(version: str = VERSION) -> list[str]:
    """The library source trees `version` pins, as <libs>/<name>-<version> directories that exist.

    The pins come from reference/<version>/libraries.json, which version_pass.py writes from the
    release's launcher JSON when it stages the tree. With no such file (a tree staged before
    2026-09-26) every staged library tree is returned — the tools' behaviour until then, which
    checked a library name against every version of the library at once."""
    base = libs()
    pins_path = os.path.join(tree(version), LIBRARIES_FILE)
    if os.path.isfile(pins_path):
        with open(pins_path, encoding="utf-8") as f:
            pins = json.load(f)
        return [os.path.join(base, f"{name}-{ver}") for name, ver in sorted(pins.items())
                if os.path.isdir(os.path.join(base, f"{name}-{ver}"))]
    if not os.path.isdir(base):
        return []
    return [os.path.join(base, d) for d in sorted(os.listdir(base)) if os.path.isdir(os.path.join(base, d))]


def page_version(text: str) -> str | None:
    """The version a page's verified line names (`> Verified against **Minecraft 26.3** · …`), or None."""
    m = HEADER.search(text[:1500])
    return m.group(1) if m else None


def present(path: str | None = None) -> bool:
    return os.path.isdir(os.path.join(path or source(), "net", "minecraft"))


def probe() -> int:
    import tempfile
    saved = {k: os.environ.get(k) for k in ("MC_SOURCE", "MC_LIBS")}
    global ROOT
    saved_root = ROOT
    work = tempfile.mkdtemp(prefix="mcvprobe-")
    try:
        os.environ["MC_SOURCE"] = os.path.join(ROOT, "reference", "0.0")
        if not source().endswith("0.0"):
            print("probe FAILED: MC_SOURCE did not override the default"); return 1
        if not tree("9.9").endswith(os.path.join("reference", "9.9")):
            print("probe FAILED: tree(version) follows MC_SOURCE; it must not"); return 1
        os.environ.pop("MC_SOURCE")
        if not source().endswith(VERSION):
            print("probe FAILED: the default is not reference/<VERSION>"); return 1
        if not source("9.9").endswith("9.9"):
            print("probe FAILED: source(version) ignores its argument"); return 1
        # the page line
        if page_version("# T\n\n> Verified against **Minecraft 26.3** · Part VI · x\n") != "26.3":
            print("probe FAILED: page_version misses the verified line"); return 1
        if page_version("# T\n\nno line here\n") is not None:
            print("probe FAILED: page_version invents a version"); return 1
        # the library pins: a fake ROOT with two releases, one pinned and one not
        ROOT = work
        os.environ["MC_LIBS"] = os.path.join(work, "libs")
        for d in ("authlib-1.0", "authlib-2.0", "brigadier-1.0"):
            os.makedirs(os.path.join(work, "libs", d))
        os.makedirs(os.path.join(work, "reference", "8.8"))
        os.makedirs(os.path.join(work, "reference", "9.9"))
        with open(os.path.join(work, "reference", "9.9", LIBRARIES_FILE), "w", encoding="utf-8") as f:
            json.dump({"authlib": "2.0", "brigadier": "1.0", "datafixerupper": "3.0"}, f)
        pinned = [os.path.basename(p) for p in lib_roots("9.9")]
        if pinned != ["authlib-2.0", "brigadier-1.0"]:
            print(f"probe FAILED: pinned roots {pinned} (want the two pinned trees that exist)"); return 1
        unpinned = [os.path.basename(p) for p in lib_roots("8.8")]
        if unpinned != ["authlib-1.0", "authlib-2.0", "brigadier-1.0"]:
            print(f"probe FAILED: an unpinned release should see every library tree, got {unpinned}"); return 1
    finally:
        ROOT = saved_root
        for k, v in saved.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v
        import shutil
        shutil.rmtree(work, ignore_errors=True)
    print("probe ok: MC_SOURCE overrides source() and not tree(); the verified line is read; "
          "a pinned release sees only its own library trees, an unpinned one all of them")
    return 0


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if "--probe" in sys.argv:
        sys.exit(probe())
    print(f"version {VERSION}")
    print(f"decompile {source()} — {'present' if present() else 'MISSING'}")
    roots = lib_roots()
    print(f"libraries {libs()} — {', '.join(os.path.basename(r) for r in roots) or 'MISSING'}")
    sys.exit(0 if present() else 2)
