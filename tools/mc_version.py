#!/usr/bin/env python3
"""The one place the book's Minecraft version is written down, for every tool that reads the decompile.

Rule 3 says newest version only, and "verified against <version>" is a test the tools run. Until
pass 8's planning session (2026-09-26) each tool carried its own copy of the version — as the
default decompile path, in a figure title, in `llms.txt`'s preface, on the Open Graph image — so a
version pass was a grep for the number across `tools/`. Now it is one constant here, and the
version pass changes it once (`tools/version_pass.py` does, as its last step, after the new tree is
staged and verified).

    VERSION   the version the pages say they are verified against ("26.2")
    source()  the decompile tree: $MC_SOURCE, else reference/<VERSION>
    libs()    the library source trees: $MC_LIBS, else reference/libs

Usage:
    python tools/mc_version.py            # prints the version and where the decompile is, and whether it is there
    python tools/mc_version.py --probe    # proves the environment overrides win over the defaults
"""
import os
import sys

VERSION = "26.2"
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))


def source(version: str = VERSION) -> str:
    """The decompile for `version`: $MC_SOURCE wins, else reference/<version>."""
    return os.path.abspath(os.environ.get("MC_SOURCE") or os.path.join(ROOT, "reference", version))


def libs() -> str:
    return os.path.abspath(os.environ.get("MC_LIBS") or os.path.join(ROOT, "reference", "libs"))


def present(path: str | None = None) -> bool:
    return os.path.isdir(os.path.join(path or source(), "net", "minecraft"))


def probe() -> int:
    saved = os.environ.get("MC_SOURCE")
    try:
        os.environ["MC_SOURCE"] = os.path.join(ROOT, "reference", "0.0")
        if not source().endswith("0.0"):
            print("probe FAILED: MC_SOURCE did not override the default"); return 1
        os.environ.pop("MC_SOURCE")
        if not source().endswith(VERSION):
            print("probe FAILED: the default is not reference/<VERSION>"); return 1
        if not source("9.9").endswith("9.9"):
            print("probe FAILED: source(version) ignores its argument"); return 1
    finally:
        if saved is not None:
            os.environ["MC_SOURCE"] = saved
    print("probe ok: MC_SOURCE overrides, and the default is reference/<VERSION>")
    return 0


if __name__ == "__main__":
    if "--probe" in sys.argv:
        sys.exit(probe())
    print(f"version {VERSION}")
    print(f"decompile {source()} — {'present' if present() else 'MISSING'}")
    print(f"libraries {libs()} — {'present' if os.path.isdir(libs()) else 'MISSING'}")
    sys.exit(0 if present() else 2)
