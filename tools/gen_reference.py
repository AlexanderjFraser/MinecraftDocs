#!/usr/bin/env python3
"""Exhaustive catalogues generated from the decompile. Prints markdown.

Usage:
    python tools/gen_reference.py packets     # every packet: phase group, direction, class
    python tools/gen_reference.py registries  # every registry key: built-in / data-pack / synced
    python tools/gen_reference.py components  # every DataComponentType, persistent / synced
    python tools/gen_reference.py gamerules   # every game rule, type, category, default
    python tools/gen_reference.py all         # write all four into src/reference/

Always regenerate with `all`, which writes each file as UTF-8 with LF. Do NOT
redirect a single view into src/reference/ on Windows: Python's stdout falls
back to the console codepage, the em dashes in the blurbs come out as mojibake,
and mdbook then refuses the chapter with "stream did not contain valid UTF-8".

MC_SOURCE points at the extracted decompile (default reference/26.2). Nothing
here reproduces source: each catalogue is names plus the facts a declaration
line states about them.
"""
from __future__ import annotations

import os
import re
import sys

ROOT = os.path.abspath(os.environ.get("MC_SOURCE", os.path.join(os.path.dirname(__file__), "..", "reference", "26.2")))
MC = os.path.join(ROOT, "net", "minecraft")
OUT = os.path.join(os.path.dirname(__file__), "..", "src", "reference")


def version() -> str:
    import json
    try:
        with open(os.path.join(ROOT, "version.json"), encoding="utf-8") as fh:
            return json.load(fh).get("name") or json.load(fh).get("id")
    except Exception:
        return os.path.basename(ROOT)


def read(*parts: str) -> str:
    with open(os.path.join(MC, *parts), encoding="utf-8", errors="replace") as fh:
        return fh.read()


def header(title: str, blurb: str) -> str:
    return f"# {title}\n\n> Generated from the **{version()}** decompile by `tools/gen_reference.py`. Do not edit by hand.\n\n{blurb}\n\n"


# ---------------------------------------------------------------- packets
# The type parameter can name a nested class (ClientboundMoveEntityPacket.Pos),
# so it is [\w.]+, not \w+ — \w dropped seven packet types silently (session G).
PACKET = re.compile(r"PacketType<([\w.]+)>\s+(\w+)\s*=\s*create(Clientbound|Serverbound)\(\"([\w/]+)\"")


def packets() -> str:
    groups = []
    proto = os.path.join(MC, "network", "protocol")
    for sub in sorted(os.listdir(proto)):
        d = os.path.join(proto, sub)
        if not os.path.isdir(d):
            continue
        for f in os.listdir(d):
            if f.endswith("PacketTypes.java"):
                rows = PACKET.findall(read("network", "protocol", sub, f))
                groups.append((sub, f[:-5], rows))
    shared = {"common", "cookie", "ping"}
    out = header("Packets", "Every packet the game defines, by the `PacketTypes` class that declares it. `common`, `cookie` and `ping` packets are shared by more than one protocol phase; the exact phase→packet bindings are in the `*Protocols` classes next to each `PacketTypes` class (`GameProtocols`, `ConfigurationProtocols`, `LoginProtocols`, `StatusProtocols`, `HandshakeProtocols`). See [Packets and stream codecs](../systems/networking/packets-and-stream-codecs.md).")
    total = 0
    out += "| group | clientbound | serverbound |\n|---|---:|---:|\n"
    for sub, cls, rows in groups:
        c = sum(1 for r in rows if r[2] == "Clientbound")
        s = len(rows) - c
        total += len(rows)
        out += f"| `{sub}` (`{cls}`) | {c} | {s} |\n"
    out += f"| **total** | | **{total}** |\n\n"
    for sub, cls, rows in groups:
        note = " — shared across phases" if sub in shared else ""
        out += f"## `{sub}` — `{cls}`{note}\n\n| id | direction | class |\n|---|---|---|\n"
        for pcls, _const, direction, pid in sorted(rows, key=lambda r: (r[2], r[3])):
            out += f"| `{pid}` | {direction.lower()} | `{pcls}` |\n"
        out += "\n"
    return out


# ------------------------------------------------------------- registries
REGKEY = re.compile(r"ResourceKey<Registry<(.+?)>>\s+(\w+)\s*=\s*createRegistryKey\(\"([\w/]+)\"\)")
BUILTIN = re.compile(r"=\s*register(?:Simple|Defaulted|DefaultedWithIntrusiveHolders)?\(Registries\.(\w+)")
LOADER_LIST = re.compile(r"List<RegistryDataLoader\.RegistryData<\?>>\s+(\w+)\s*=\s*List\.of\((.*?)\);", re.S)


def registries() -> str:
    keys = REGKEY.findall(read("core", "registries", "Registries.java"))
    builtin = set(BUILTIN.findall(read("core", "registries", "BuiltInRegistries.java")))
    lists = {name: set(re.findall(r"Registries\.(\w+)", body)) for name, body in LOADER_LIST.findall(read("resources", "RegistryDataLoader.java"))}
    worldgen = lists.get("WORLDGEN_REGISTRIES", set())
    dimension = lists.get("DIMENSION_REGISTRIES", set())
    synced = lists.get("SYNCHRONIZED_REGISTRIES", set())
    out = header("Registries", "Every registry key declared in `Registries`. **Built-in** registries are populated from static code in `BuiltInRegistries` at class-load time and frozen; **data-pack** registries are loaded per world by `RegistryDataLoader` from JSON (`WORLDGEN_REGISTRIES`, or `DIMENSION_REGISTRIES` for level stems); **synced** ones are sent to the client in the configuration phase (`SYNCHRONIZED_REGISTRIES`). A key that is none of these is a registry *type* the game reasons about without a global instance (e.g. per-world or client-side). See [Identifiers and registries](../systems/foundations/identifiers-and-registries.md).")
    out += f"{len(keys)} keys · {len(builtin)} built-in · {len(worldgen | dimension)} data-pack · {len(synced)} synced\n\n"
    out += "| key | element type | kind | synced |\n|---|---|---|---|\n"
    for elem, const, key in sorted(keys, key=lambda k: k[2]):
        kind = "built-in" if const in builtin else "data-pack" if const in worldgen else "data-pack (dimension)" if const in dimension else "—"
        elem = re.sub(r"<.*", "<…>", elem)
        out += f"| `{key}` (`Registries.{const}`) | `{elem}` | {kind} | {'yes' if const in synced else ''} |\n"
    return out


# ------------------------------------------------------------- components
# the id may contain a slash (villager/variant, wolf/sound_variant …) — \w+ silently
# dropped 29 of the 111 components until pass 2 caught it.
COMP = re.compile(r"DataComponentType<(.+?)>\s+(\w+)\s*=\s*register\(\"([\w/]+)\",\s*\(\w+\)\s*->\s*\{(.*?)\}\);", re.S)


def components() -> str:
    src = read("core", "component", "DataComponents.java")
    rows = COMP.findall(src)
    out = header("Data components", "Every `DataComponentType` registered in `DataComponents`. *Persistent* components have a `Codec` and are written to disk; *synced* ones have a `StreamCodec` and are sent to the client; *cache-encoded* ones use the shared `EncoderCache`. A type that is neither persistent nor synced is transient and lives only in memory. See [Data components](../systems/foundations/data-components.md).")
    out += f"{len(rows)} components\n\n| id | value type | persistent | synced |\n|---|---|---|---|\n"
    for typ, const, cid, body in rows:
        typ = re.sub(r"<.*", "<…>", typ)
        p = "yes" if "persistent(" in body else ""
        s = "yes" if "networkSynchronized(" in body else ""
        if "cacheEncoding(" in body:
            p += " (cached)"
        out += f"| `{cid}` (`DataComponents.{const}`) | `{typ}` | {p} | {s} |\n"
    return out


# -------------------------------------------------------------- game rules
RULE = re.compile(r"GameRule<(\w+)>\s+(\w+)\s*=\s*register(\w+)\(\"(\w+)\",\s*GameRuleCategory\.(\w+),\s*([^,)]+)(?:,\s*([^)]+))?\)")
DEFAULT_NOTE = {"!SharedConstants.DEBUG_WORLD_RECREATE": "true"}


def gamerules() -> str:
    rows = RULE.findall(read("world", "level", "gamerules", "GameRules.java"))
    out = header("Game rules", "Every rule declared in `GameRules`, with its category (`GameRuleCategory`) and default. Integer rules list their minimum after the default where one is declared. Values live per world in a `GameRuleMap` on the level data. See [Level data and rules](../systems/world/level-data-and-rules.md).")
    out += f"{len(rows)} rules\n\n| rule | type | category | default |\n|---|---|---|---|\n"
    for typ, const, _kind, rid, cat, default, extra in sorted(rows, key=lambda r: (r[4], r[3])):
        default = DEFAULT_NOTE.get(default.strip(), default.strip())
        if extra.strip():
            default += f" (min {extra.strip()})"
        out += f"| `{rid}` (`GameRules.{const}`) | {typ} | {cat.lower()} | `{default}` |\n"
    return out


VIEWS = {"packets": packets, "registries": registries, "components": components, "gamerules": gamerules}


def main(argv: list[str]) -> int:
    if len(argv) != 2 or argv[1] not in (*VIEWS, "all"):
        print(__doc__)
        return 2
    if not os.path.isdir(MC):
        print(f"no decompile at {ROOT} (set MC_SOURCE)", file=sys.stderr)
        return 2
    if argv[1] == "all":
        os.makedirs(OUT, exist_ok=True)
        for name, fn in VIEWS.items():
            path = os.path.join(OUT, f"{name}.md")
            with open(path, "w", encoding="utf-8", newline="\n") as fh:
                fh.write(fn())
            print(f"wrote {os.path.relpath(path)}")
        return 0
    sys.stdout.write(VIEWS[argv[1]]())
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
