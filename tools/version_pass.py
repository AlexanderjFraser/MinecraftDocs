#!/usr/bin/env python3
"""The version pass's mechanical half: stage a release's decompile beside the old one, then measure the damage.

Rule 3 is newest version only, and the plan's version pass (docs/plan.md, *The version pass*) runs
once per release: fetch and decompile the release into reference/<version>/ beside the old tree,
with its data/, assets/ and server-classes.txt; re-stage the libraries; run the name gate against the
new tree, whose failures name the pages that need re-reading; regenerate the atlas and the Reference
views and read the diff; bump the header line. Until pass 8's planning session (2026-09-26) the
first of those steps was the owner's, by hand, with the McDeob GUI. Since 26.x the game jar ships
with Mojang's names in it (the version JSON carries no `client_mappings`), so a plain Vineflower
decompile of the jar is the Mojang-mapped source, and this script does the whole staging:

  1. Mojang's version manifest -> the release's own JSON -> the client and server jar URLs, the
     Java version, and the versions of authlib, Brigadier and DataFixerUpper it pins.
  2. Download both jars to reference/_downloads/<version>/ (gitignored with the rest of reference/).
  3. Decompile the client's .class entries under net/ and com/ with the Vineflower bundled in the
     PvP mod's McDeob jar (MCDEOB_JAR, default D:/pvpmod/McDeob-3.4.1.jar) into reference/<version>/.
  4. Copy data/ whole, assets/ without textures (.png, .mcmeta) and version.json from the client jar.
  5. Write server-classes.txt from the server bundler's inner jar: every top-level class the
     dedicated server ships, as `pkg/Name.java`, sorted — the oracle for server-side versus
     client-only.
  6. Stage the libraries with tools/fetch_libs.sh at the versions the JSON pins (authlib's jar is
     downloaded from Mojang's library server, so the launcher need not have run the version).

Then `--check` runs the name gate and the figure gate against the new tree without touching the
tools' default, and prints the failing names by page and by part — the size of the version pass.
`--flip` rewrites tools/mc_version.py to the new version, which is the last step, after the
re-read. `--latest` asks the manifest what the current release is and compares it with the
tools' version, which is what the release day's ruling R6 needs.

Usage:
    python tools/version_pass.py --latest              # the current release, and the last few with their dates
    python tools/version_pass.py 26.3                  # stage reference/26.3 (steps 1-6; each step skips what is already there)
    python tools/version_pass.py 26.3 --check          # the two name gates against reference/26.3, failures by page
    python tools/version_pass.py 26.3 --flip           # tools/mc_version.py -> 26.3 (do this after the pages are re-read)
    python tools/version_pass.py --probe               # proves the jar parsing, the filtering and the flip on synthetic input
Network access needs certifi on this machine (the system trust store carries an expired root).
"""
from __future__ import annotations

import io
import json
import os
import re
import shutil
import ssl
import subprocess
import sys
import tempfile
import urllib.request
import zipfile
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mc_version  # noqa: E402

ROOT = mc_version.ROOT
MANIFEST = "https://piston-meta.mojang.com/mc/game/version_manifest_v2.json"
MCDEOB = os.environ.get("MCDEOB_JAR", "D:/pvpmod/McDeob-3.4.1.jar")
DECOMPILER_MAIN = "org.jetbrains.java.decompiler.main.decompiler.ConsoleDecompiler"
# The options McDeob 3.4.1's own GUI passes (`Util.getDecompilerParams`, read from its bytecode in pass 8's
# session V1), so that a staged tree reads like the 26.2 tree the book was written against: generic
# signatures, default constructors shown, non-ASCII escaped, synthetics removed, and @Override added.
# The first 26.3 staging ran without `aoa`, `hdc` and `asc` and dropped all 16,652 @Override lines, which
# shrank every line count on the site for a reason that was not the game. (`udv=0` is McDeob's only for a
# remapped jar; a 26.x jar carries Mojang's names and debug variables, so the default is kept.)
DECOMPILER_FLAGS = ("-dgs=1", "-hdc=0", "-asc=1", "-rsy=1", "-aoa=1")
LIBS = ("authlib", "brigadier", "datafixerupper")
TEXTURES = (".png", ".mcmeta")


# --- network ------------------------------------------------------------------

def _context() -> ssl.SSLContext:
    try:
        import certifi
        return ssl.create_default_context(cafile=certifi.where())
    except ImportError:
        return ssl.create_default_context()


def fetch_json(url: str) -> dict:
    with urllib.request.urlopen(url, context=_context(), timeout=60) as r:
        return json.load(r)


def download(url: str, dest: str, size: int | None = None) -> str:
    if os.path.exists(dest) and (size is None or os.path.getsize(dest) == size):
        print(f"  present  {dest}")
        return dest
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    print(f"  fetching {url} -> {dest}")
    with urllib.request.urlopen(url, context=_context(), timeout=600) as r, open(dest, "wb") as f:
        shutil.copyfileobj(r, f)
    return dest


# --- the version JSON ----------------------------------------------------------

def manifest_entry(version: str, manifest: dict) -> dict:
    for v in manifest["versions"]:
        if v["id"] == version:
            return v
    sys.exit(f"{version} is not in Mojang's manifest (latest release {manifest['latest']['release']})")


def pins(vjson: dict) -> dict:
    """What a version JSON pins: the jar URLs and sizes, the Java major, the three library versions and their jar URLs."""
    d = vjson["downloads"]
    out = {"client": (d["client"]["url"], d["client"]["size"]),
           "server": (d["server"]["url"], d["server"]["size"]),
           "mapped": "client_mappings" not in d,
           "java": vjson.get("javaVersion", {}).get("majorVersion"),
           "libs": {}}
    for lib in vjson.get("libraries", []):
        name = lib.get("name", "")
        m = re.fullmatch(r"com\.mojang:(\w+):([\w.\-]+)", name)
        if m and m.group(1) in LIBS:
            art = lib.get("downloads", {}).get("artifact", {})
            out["libs"][m.group(1)] = (m.group(2), art.get("url"))
    return out


# --- the jars -----------------------------------------------------------------

def is_game_class(name: str) -> bool:
    return name.endswith(".class") and (name.startswith("net/") or name.startswith("com/"))


def server_classes(server_jar: str, version: str) -> list[str]:
    """Top-level classes in the server bundler's inner jar, as `pkg/Name.java`, sorted."""
    with zipfile.ZipFile(server_jar) as bundle:
        inner = [n for n in bundle.namelist() if re.fullmatch(rf"META-INF/versions/{re.escape(version)}/server-{re.escape(version)}\.jar", n)]
        if inner:
            data = bundle.read(inner[0])
            z = zipfile.ZipFile(io.BytesIO(data))
        else:  # not a bundler: the classes are in the jar itself
            z = bundle
        names = z.namelist()
    out = set()
    for n in names:
        if is_game_class(n) and "$" not in os.path.basename(n):
            out.add(n[:-len(".class")] + ".java")
    return sorted(out)


def stage_resources(client_jar: str, out: str) -> Counter:
    """data/ whole, assets/ without textures, version.json — into `out`, like reference/26.2/."""
    copied = Counter()
    with zipfile.ZipFile(client_jar) as z:
        for info in z.infolist():
            n = info.filename
            if n.endswith("/"):
                continue
            keep = n.startswith("data/") or n == "version.json" or (n.startswith("assets/") and not n.endswith(TEXTURES))
            if not keep:
                continue
            dest = os.path.join(out, *n.split("/"))
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            with z.open(info) as src, open(dest, "wb") as dst:
                shutil.copyfileobj(src, dst)
            copied[n.split("/")[0]] += 1
    return copied


def decompile(client_jar: str, out: str, mcdeob: str = MCDEOB) -> int:
    """Vineflower over the game's classes; the .java tree lands under `out`. Returns the file count."""
    if not os.path.exists(mcdeob):
        sys.exit(f"no decompiler at {mcdeob} (set MCDEOB_JAR to the McDeob fat jar)")
    if os.path.isdir(os.path.join(out, "net", "minecraft")):
        n = sum(1 for _r, _d, fs in os.walk(os.path.join(out, "net")) for f in fs if f.endswith(".java"))
        print(f"  present  {out}/net ({n} java files) — delete it to decompile again")
        return n
    work = tempfile.mkdtemp(prefix="mcdecomp-")
    classes_jar = os.path.join(work, "classes.jar")
    n = 0
    with zipfile.ZipFile(client_jar) as zin, zipfile.ZipFile(classes_jar, "w", zipfile.ZIP_DEFLATED) as zout:
        for info in zin.infolist():
            if is_game_class(info.filename):
                zout.writestr(info, zin.read(info.filename))
                n += 1
    print(f"  {n} classes staged; running Vineflower (this takes minutes)")
    cmd = ["java", "-cp", mcdeob, DECOMPILER_MAIN, *DECOMPILER_FLAGS, "-log=WARN", classes_jar, work]
    subprocess.run(cmd, check=True)
    produced = os.path.join(work, "classes.jar")  # Vineflower writes a jar of the same name beside the input
    count = 0
    with zipfile.ZipFile(produced) as z:
        for info in z.infolist():
            if info.filename.endswith(".java"):
                z.extract(info, out)
                count += 1
    shutil.rmtree(work, ignore_errors=True)
    return count


def write_pins(out: str, libs: dict) -> str:
    """reference/<version>/libraries.json: the library versions the release pins, which the gates read
    (`mc_version.lib_roots`) so that a page verified against this release has its Brigadier, DataFixerUpper
    and authlib names checked against these trees only, not against every version staged beside them."""
    path = os.path.join(out, mc_version.LIBRARIES_FILE)
    os.makedirs(out, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump({lib: ver for lib, (ver, _url) in sorted(libs.items())}, f)
        f.write("\n")
    print(f"  pins     {path}")
    return path


# --- the flip -----------------------------------------------------------------

def flip_text(text: str, version: str) -> str:
    new, n = re.subn(r'^VERSION = "[^"]+"$', f'VERSION = "{version}"', text, flags=re.M)
    if n != 1:
        raise ValueError("mc_version.py has no single VERSION line")
    return new


def flip(version: str) -> None:
    path = os.path.join(ROOT, "tools", "mc_version.py")
    with open(path, encoding="utf-8") as f:
        text = f.read()
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(flip_text(text, version))
    print(f"tools/mc_version.py -> {version}. Every page is still checked against the release its own verified line "
          f"names, so the gates pass; move each page's line to {version} as it is re-read, then the introduction, "
          f"the issue template and fetch_libs.sh's defaults; `verify_names.py --current` passes when none is left behind.")


# --- the check -----------------------------------------------------------------

def check(version: str) -> int:
    tree = os.path.join(ROOT, "reference", version)
    if not mc_version.present(tree):
        sys.exit(f"no decompile at {tree}; stage it first")
    env = dict(os.environ, MC_SOURCE=tree)
    print(f"== verify_names.py against {tree}")
    r = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "verify_names.py")], env=env,
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    fails = [l for l in r.stdout.splitlines() + r.stderr.splitlines() if re.match(r"^\s*src[/\\]", l)]
    by_page, by_part = Counter(), Counter()
    for l in fails:
        page = l.split(":")[0].replace("\\", "/")
        by_page[page] += 1
        by_part[page.split("/")[2] if page.startswith("src/systems/") else page.split("/")[1]] += 1
    print((r.stdout.strip().splitlines() or ["(no output)"])[-1])
    print(f"{len(fails)} unresolved names on {len(by_page)} pages")
    for part, n in by_part.most_common():
        print(f"  {n:4d}  {part}")
    for page, n in by_page.most_common(40):
        print(f"  {n:4d}  {page}")
    print(f"== check_figure_names.py --strict against {tree}")
    r2 = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "check_figure_names.py"), "--strict"], env=env,
                        capture_output=True, text=True, encoding="utf-8", errors="replace")
    print((r2.stdout.strip().splitlines() or ["(no output)"])[-1])
    # the lane key names a class per lane, and a release that renames one breaks the key, not a page
    # (26.3: RedStoneWireBlock, ConfiguredFeature, ItemInHandRenderer) — pass 8, session V1
    print(f"== check_lanes.py --strict against {tree}")
    r3 = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "check_lanes.py"), "--strict"], env=env,
                        capture_output=True, text=True, encoding="utf-8", errors="replace")
    for line in r3.stdout.splitlines():
        if line.startswith("key:"):
            print(f"  {line}")
    print((r3.stdout.strip().splitlines() or ["(no output)"])[-1])
    return 0 if r.returncode == 0 and r2.returncode == 0 and r3.returncode == 0 else 1


# --- the staging ---------------------------------------------------------------

def stage(version: str) -> int:
    out = os.path.join(ROOT, "reference", version)
    dl = os.path.join(ROOT, "reference", "_downloads", version)
    print(f"== {version}: the manifest")
    manifest = fetch_json(MANIFEST)
    entry = manifest_entry(version, manifest)
    vjson = fetch_json(entry["url"])
    p = pins(vjson)
    print(f"  released {entry.get('releaseTime')}, Java {p['java']}, libraries " +
          ", ".join(f"{k} {v[0]}" for k, v in sorted(p["libs"].items())))
    if not p["mapped"]:
        sys.exit("this version JSON carries client_mappings, so the jar is obfuscated and a plain decompile "
                 "would not be Mojang-named; the staging needs a remap step this script does not have")
    print("== the jars")
    client = download(p["client"][0], os.path.join(dl, "client.jar"), p["client"][1])
    server = download(p["server"][0], os.path.join(dl, "server.jar"), p["server"][1])
    print("== the decompile")
    n = decompile(client, out)
    print(f"  {n} java files under {out}")
    print("== data, assets and version.json")
    if os.path.isdir(os.path.join(out, "data")):
        print(f"  present  {out}/data")
    else:
        print("  " + ", ".join(f"{k} {v}" for k, v in sorted(stage_resources(client, out).items())))
    print("== server-classes.txt")
    sc = os.path.join(out, "server-classes.txt")
    if os.path.exists(sc):
        print(f"  present  {sc}")
    else:
        names = server_classes(server, version)
        with open(sc, "w", encoding="utf-8", newline="\n") as f:
            f.write("\n".join(names) + "\n")
        print(f"  {len(names)} classes")
    print("== the libraries (tools/fetch_libs.sh)")
    write_pins(out, p["libs"])
    env = dict(os.environ)
    for lib, (ver, url) in p["libs"].items():
        env[{"authlib": "AUTHLIB", "brigadier": "BRIGADIER", "datafixerupper": "DFU"}[lib]] = ver
        if lib == "authlib" and url:
            env["AUTHLIB_JAR"] = download(url, os.path.join(dl, f"authlib-{ver}.jar"))
    subprocess.run(["bash", os.path.join(ROOT, "tools", "fetch_libs.sh")], env=env, check=False)
    print(f"staged. Next: python tools/version_pass.py {version} --check")
    return 0


def latest() -> int:
    manifest = fetch_json(MANIFEST)
    rel = manifest["latest"]["release"]
    print(f"latest release {rel}; the tools say {mc_version.VERSION}" +
          ("" if rel == mc_version.VERSION else " — THE VERSION PASS IS DUE"))
    rels = [v for v in manifest["versions"] if v["type"] == "release"][:6]
    for v in rels:
        print(f"  {v['id']:<10} {v['releaseTime'][:10]}")
    snaps = [v for v in manifest["versions"] if v["type"] == "snapshot"][:1]
    for v in snaps:
        print(f"  newest snapshot {v['id']} ({v['releaseTime'][:10]})")
    return 0 if rel == mc_version.VERSION else 1


# --- the probe -----------------------------------------------------------------

def probe() -> int:
    work = tempfile.mkdtemp(prefix="vpprobe-")
    try:
        # a client jar with classes, textures, data and version.json
        client = os.path.join(work, "client.jar")
        with zipfile.ZipFile(client, "w") as z:
            z.writestr("net/minecraft/A.class", b"x")
            z.writestr("com/mojang/B.class", b"x")
            z.writestr("org/other/C.class", b"x")
            z.writestr("assets/minecraft/models/a.json", "{}")
            z.writestr("assets/minecraft/textures/a.png", b"x")
            z.writestr("assets/minecraft/textures/a.png.mcmeta", "{}")
            z.writestr("data/minecraft/tags/t.json", "{}")
            z.writestr("version.json", '{"id": "9.9"}')
        out = os.path.join(work, "out")
        copied = stage_resources(client, out)
        want = {"assets": 1, "data": 1, "version.json": 1}
        if dict(copied) != want or os.path.exists(os.path.join(out, "assets", "minecraft", "textures", "a.png")):
            print(f"probe FAILED: resources {dict(copied)}"); return 1
        # a server bundler with an inner jar
        inner = io.BytesIO()
        with zipfile.ZipFile(inner, "w") as z:
            z.writestr("net/minecraft/server/S.class", b"x")
            z.writestr("net/minecraft/server/S$Inner.class", b"x")
            z.writestr("com/mojang/math/Axis.class", b"x")
            z.writestr("org/lib/L.class", b"x")
        server = os.path.join(work, "server.jar")
        with zipfile.ZipFile(server, "w") as z:
            z.writestr("META-INF/versions/9.9/server-9.9.jar", inner.getvalue())
        if server_classes(server, "9.9") != ["com/mojang/math/Axis.java", "net/minecraft/server/S.java"]:
            print(f"probe FAILED: server classes {server_classes(server, '9.9')}"); return 1
        # the pins
        vj = {"downloads": {"client": {"url": "c", "size": 1}, "server": {"url": "s", "size": 2}},
              "javaVersion": {"majorVersion": 25},
              "libraries": [{"name": "com.mojang:authlib:10.0.77", "downloads": {"artifact": {"url": "a"}}},
                            {"name": "com.mojang:brigadier:1.3.11"}, {"name": "org.lwjgl:lwjgl:3.3.3"}]}
        p = pins(vj)
        if not p["mapped"] or p["libs"] != {"authlib": ("10.0.77", "a"), "brigadier": ("1.3.11", None)} or p["java"] != 25:
            print(f"probe FAILED: pins {p}"); return 1
        vj["downloads"]["client_mappings"] = {"url": "m"}
        if pins(vj)["mapped"]:
            print("probe FAILED: client_mappings not noticed"); return 1
        # the pins file the gates read
        pins_path = write_pins(os.path.join(work, "tree"), p["libs"])
        with open(pins_path, encoding="utf-8") as f:
            if json.load(f) != {"authlib": "10.0.77", "brigadier": "1.3.11"}:
                print("probe FAILED: libraries.json"); return 1
        # the flip
        if 'VERSION = "9.9"' not in flip_text('x = 1\nVERSION = "26.2"\ny = 2\n', "9.9"):
            print("probe FAILED: flip"); return 1
        try:
            flip_text("nothing\n", "9.9"); print("probe FAILED: flip accepted a file with no VERSION line"); return 1
        except ValueError:
            pass
        # the class filter
        if not is_game_class("net/minecraft/A.class") or is_game_class("org/x/A.class") or is_game_class("net/minecraft/a.json"):
            print("probe FAILED: class filter"); return 1
    finally:
        shutil.rmtree(work, ignore_errors=True)
    print("probe ok: textures dropped and data kept, inner classes folded out of server-classes.txt, "
          "library pins read and written for the gates, an obfuscated version refused, the flip exact")
    return 0


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    args = sys.argv[1:]
    if "--probe" in args:
        return probe()
    if "--latest" in args:
        return latest()
    versions = [a for a in args if not a.startswith("--")]
    if len(versions) != 1:
        print(__doc__)
        return 2
    version = versions[0]
    if "--check" in args:
        return check(version)
    if "--flip" in args:
        flip(version)
        return 0
    return stage(version)


if __name__ == "__main__":
    sys.exit(main())
