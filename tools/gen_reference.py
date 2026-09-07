#!/usr/bin/env python3
"""Exhaustive catalogues generated from the decompile. Prints markdown.

Usage:
    python tools/gen_reference.py packets     # every packet: phase group, direction, class
    python tools/gen_reference.py registries  # every registry key: built-in / data-pack / synced
    python tools/gen_reference.py components  # every DataComponentType, persistent / synced
    python tools/gen_reference.py gamerules   # every game rule, type, category, default
    python tools/gen_reference.py entity-data-serializers   # every EntityDataSerializer, in wire-id order
    python tools/gen_reference.py attributes                # every attribute: default, range, syncable
    python tools/gen_reference.py enchantment-hooks         # every EnchantmentHelper entry point and its callers
    python tools/gen_reference.py loot-context-params       # every parameter set, with required and optional keys
    python tools/gen_reference.py spawn-reasons             # every EntitySpawnReason and what it gates
    python tools/gen_reference.py weapon-helpers            # the Item.Properties weapon helpers and every item built by one
    python tools/gen_reference.py structure-spawn-overrides # which structures replace a biome's spawn list
    python tools/gen_reference.py all         # write every view into src/reference/

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
    c_total = s_total = 0
    out += "| group | clientbound | serverbound |\n|---|---:|---:|\n"
    for sub, cls, rows in groups:
        c = sum(1 for r in rows if r[2] == "Clientbound")
        s = len(rows) - c
        c_total += c
        s_total += s
        out += f"| `{sub}` (`{cls}`) | {c} | {s} |\n"
    # the grand total used to be printed in the serverbound column, so the page said 232
    # packets were serverbound where 78 are (session O)
    out += f"| **total** | **{c_total}** | **{s_total}** |\n\n"
    for sub, cls, rows in groups:
        note = " — shared across phases" if sub in shared else ""
        out += f"## `{sub}` — `{cls}`{note}\n\n| id | direction | class |\n|---|---|---|\n"
        for pcls, _const, direction, pid in sorted(rows, key=lambda r: (r[2], r[3])):
            out += f"| `{pid}` | {direction.lower()} | `{pcls}` |\n"
        out += "\n"
    return out


# ------------------------------------------------------------- registries
REGKEY = re.compile(r"ResourceKey<(?:\? extends )?Registry<(.+?)>>\s+(\w+)\s*=\s*createRegistryKey\(\"([\w/]+)\"\)")
# Five registries are keyed from their own class with the public helper rather than
# `Registries`' private one, so reading Registries.java alone published 148 keys for 153
# (session O): function, clock_time_marker, recipe_property_set, equipment_asset,
# waypoint_style_asset.
REGKEY_ELSEWHERE = re.compile(r"ResourceKey<(?:\? extends )?Registry<(.+?)>>\s+(\w+)\s*=\s*ResourceKey\.createRegistryKey\(Identifier\.withDefaultNamespace\(\"([\w/]+)\"\)\)")
BUILTIN = re.compile(r"=\s*register\w*\(Registries\.(\w+)")
LOADER_LIST = re.compile(r"List<RegistryDataLoader\.RegistryData<\?>>\s+(\w+)\s*=\s*List\.of\((.*?)\);", re.S)


def registries() -> str:
    keys = [(e, c, k, "Registries") for e, c, k in REGKEY.findall(read("core", "registries", "Registries.java"))]
    for dirpath, _dirs, files in os.walk(MC):
        if dirpath.endswith(os.path.join("core", "registries")):
            continue
        for f in files:
            if f.endswith(".java"):
                with open(os.path.join(dirpath, f), encoding="utf-8") as fh:
                    keys += [(e, c, k, f[:-5]) for e, c, k in REGKEY_ELSEWHERE.findall(fh.read())]
    builtin = set(BUILTIN.findall(read("core", "registries", "BuiltInRegistries.java")))
    lists = {name: set(re.findall(r"Registries\.(\w+)", body)) for name, body in LOADER_LIST.findall(read("resources", "RegistryDataLoader.java"))}
    worldgen = lists.get("WORLDGEN_REGISTRIES", set())
    dimension = lists.get("DIMENSION_REGISTRIES", set())
    synced = lists.get("SYNCHRONIZED_REGISTRIES", set())
    out = header("Registries", "Every registry key in the game. **148 of them are declared in `Registries`**; five more are declared by the class that owns them (`ServerFunctionLibrary`, `ClockTimeMarkers`, `RecipePropertySet`, `EquipmentAssets`, `WaypointStyleAssets`) with the public `ResourceKey.createRegistryKey` rather than `Registries`' private helper, which is why this total is larger than the 148 [identifiers and registries](../systems/foundations/identifiers-and-registries.md#the-name) counts. **Built-in** registries are populated from static code in `BuiltInRegistries` at class-load time and frozen; **data-pack** registries are loaded per world by `RegistryDataLoader` from JSON (`WORLDGEN_REGISTRIES`, or `DIMENSION_REGISTRIES` for level stems); **synced** ones are sent to the client in the configuration phase (`SYNCHRONIZED_REGISTRIES`). A key that is none of these is a registry *type* the game reasons about without a global instance (e.g. per-world or client-side). See [Identifiers and registries](../systems/foundations/identifiers-and-registries.md).")
    out += f"{len(keys)} keys · {len(builtin)} built-in · {len(worldgen | dimension)} data-pack · {len(synced)} synced\n\n"
    out += "| key | element type | kind | synced |\n|---|---|---|---|\n"
    for elem, const, key, owner in sorted(keys, key=lambda k: k[2]):
        kind = "built-in" if const in builtin else "data-pack" if const in worldgen else "data-pack (dimension)" if const in dimension else "—"
        elem = re.sub(r"<.*", "<…>", elem)
        out += f"| `{key}` (`{owner}.{const}`) | `{elem}` | {kind} | {'yes' if const in synced else ''} |\n"
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
# The trailing arguments are a minimum, a maximum and a FeatureFlagSet, in that order.
# Capturing them as one "min" blob published `8 (min 1, 1000, FeatureFlagSet.of(...)` —
# an unbalanced paren, a maximum called a minimum, and a feature gate as noise (session O).
RULE = re.compile(r"GameRule<(\w+)>\s+(\w+)\s*=\s*register(\w+)\(\"(\w+)\",\s*GameRuleCategory\.(\w+),\s*([^,)]+)(?:,\s*(-?\w+))?(?:,\s*(-?\w+))?(?:,\s*(FeatureFlagSet\.[^)]*\)))?\)")
DEFAULT_NOTE = {"!SharedConstants.DEBUG_WORLD_RECREATE": "true"}


def gamerules() -> str:
    rows = RULE.findall(read("world", "level", "gamerules", "GameRules.java"))
    out = header("Game rules", "Every rule declared in `GameRules`, with its category (`GameRuleCategory`) and default. Integer rules list their bounds and any feature gate after the default. Values live in a `GameRuleMap` — a `SavedData` at *data/minecraft/game_rules.dat*, one set for the whole server rather than one per level. See [Level data and rules](level-data-and-rules.md).")
    out += f"{len(rows)} rules\n\n| rule | type | category | default |\n|---|---|---|---|\n"
    for typ, const, _kind, rid, cat, default, lo, hi, flag in sorted(rows, key=lambda r: (r[4], r[3])):
        default = DEFAULT_NOTE.get(default.strip(), default.strip())
        bounds = []
        if lo.strip():
            bounds.append(f"min {lo.strip()}")
        if hi.strip():
            bounds.append(f"max {hi.strip()}")
        if flag.strip():
            bounds.append("requires " + flag.strip().removeprefix("FeatureFlagSet.of(").removesuffix(")"))
        if bounds:
            default += " (" + ", ".join(bounds) + ")"
        out += f"| `{rid}` (`GameRules.{const}`) | {typ} | {cat.lower()} | `{default}` |\n"
    return out


# --------------------------------------------------- entity data serializers
# Registration order in the static block *is* the wire id: registerSerializer
# pushes into a CrudeIncrementalIntIdentityHashBiMap that hands out the next
# int. The declaration lines carry the value type, the static block carries the
# order, and the two are not in the same order — read both (session G).
# A serializer is declared either through a factory (EntityDataSerializer.forValueType(...)) or,
# for ITEM_STACK alone in 26.2, as an anonymous subclass. The second form used to fall through to
# ("?", "?") and reach the published page (pass-4 session A).
SERIALIZER_DECL = re.compile(r"EntityDataSerializer<(.+?)>\s+(\w+)\s*=\s*(?:EntityDataSerializer\.(\w+)\(|new\s+EntityDataSerializer<)")
SERIALIZER_ORDER = re.compile(r"registerSerializer\(EntityDataSerializers\.(\w+)\)")


def serializers() -> str:
    src = read("network", "syncher", "EntityDataSerializers.java")
    decl = {const: (typ, kind) for typ, const, kind in SERIALIZER_DECL.findall(src)}
    order = SERIALIZER_ORDER.findall(src)
    out = header("Entity data serializers", "Every `EntityDataSerializer` in `EntityDataSerializers`, in **registration order, which is the wire id** — `EntityDataSerializers.registerSerializer` pushes each one into a `CrudeIncrementalIntIdentityHashBiMap` that hands out the next int. A `SynchedEntityData.DataValue` on the wire is an unsigned byte accessor id, this var-int, and the encoded value. *For value type* marks the ones built by `EntityDataSerializer.forValueType`, the immutable case where `EntityDataSerializer.copy` is identity. See [Synched entity data](../systems/entities/synched-entity-data.md).")
    out += f"{len(order)} serializers, wire ids 0 to {len(order) - 1}\n\n"
    out += "| id | constant | value type | built by |\n|---:|---|---|---|\n"
    for i, const in enumerate(order):
        typ, kind = decl.get(const, ("?", "?"))
        if kind == "forValueType":
            kind = "for value type"
        elif kind == "":
            kind = "an anonymous subclass"
        else:
            kind = f"`EntityDataSerializer.{kind}`"
        out += f"| {i} | `EntityDataSerializers.{const}` | `{typ}` | {kind} |\n"
    missing = sorted(set(decl) - set(order))
    if missing:
        out += "\nDeclared but never registered, so unreachable from the wire: " + ", ".join("`" + m + "`" for m in missing) + ".\n"
    return out


# ---------------------------------------------------------------- attributes
ATTRIBUTE = re.compile(
    r"Holder<Attribute>\s+(\w+)\s*=\s*register\(\s*\"([\w/]+)\"\s*,\s*\(?new RangedAttribute\(\s*\"([\w.]+)\"\s*,\s*([-\w.E]+?)D?\s*,\s*([-\w.E]+?)D?\s*,\s*([-\w.E]+?)D?\s*\)\)?((?:\.\w+\([^)]*\))*)"
)


def _num(text: str) -> str:
    try:
        value = float(text)
    except ValueError:
        return text
    if value == int(value) and abs(value) < 1e12:
        return str(int(value))
    return f"{value:g}"


def attributes() -> str:
    rows = ATTRIBUTE.findall(read("world", "entity", "ai", "attributes", "Attributes.java"))
    syncable = sum(1 for r in rows if "setSyncable(true)" in r[6])
    out = header("Attributes", "Every attribute registered in `Attributes`. All of them are `RangedAttribute`s, so every one clamps to its range once, at the end of `AttributeInstance.calculateValue`. **Syncable** attributes are the only ones `ClientboundUpdateAttributesPacket` ever carries: a mutation to one of the others changes the server's number and never reaches the client at all. The sentiment decides tooltip colour and nothing else. Defaults here are the registry's, and most entity types override them in their own `AttributeSupplier`. See [Attributes](../systems/entities/attributes.md).")
    out += f"{len(rows)} attributes, {syncable} syncable and {len(rows) - syncable} not\n\n"
    out += "| id | constant | default | min | max | syncable | sentiment |\n|---|---|---:|---:|---:|---|---|\n"
    for const, aid, _desc, default, lo, hi, tail in sorted(rows, key=lambda r: r[1]):
        sent = re.search(r"setSentiment\(Attribute\.Sentiment\.(\w+)\)", tail)
        out += (
            f"| `{aid}` | `Attributes.{const}` | {_num(default)} | {_num(lo)} | {_num(hi)} | "
            f"{'yes' if 'setSyncable(true)' in tail else ''} | {sent.group(1).lower() if sent else 'positive'} |\n"
        )
    return out


# ------------------------------------------------- loot context parameter sets
# The sets are declared as bare fields and assigned in the static block, each
# from a register("id", builder -> builder.required(X).optional(Y)) call. The
# lambda body is one line per set in the decompile, so the keys can be read off
# it in declaration order — which is the order the builder was called in, not
# the order LootContextParams declares them (session H).
PARAM_SET = re.compile(r"(\w+) = register\(\"([\w/]+)\", \(\w+\) -> \{\s*(.*?)\s*\}\);", re.DOTALL)
PARAM_KEY = re.compile(r"\.(required|optional)\(LootContextParams\.(\w+)\)")


def loot_context_params() -> str:
    src = read("world", "level", "storage", "loot", "parameters", "LootContextParamSets.java")
    sets = PARAM_SET.findall(src)
    out = header(
        "Loot context parameter sets",
        "Every `ContextKeySet` registered in `LootContextParamSets`, with the keys its "
        "`ContextKeySet.Builder` declared. The set belongs to the **caller**, not to the loot table: "
        "`ContextMap.Builder.create` throws both on a required key that is absent and on a key the set "
        "does not declare at all, so this table is the contract each call site has to satisfy. A "
        "required key can be read with `LootContext.getParameter`, an optional one only with "
        "`LootContext.getOptionalParameter`. Twelve of these twenty-six sets never roll a `LootTable` at "
        "all — the engine is older and wider than the loot package. See "
        "[Contexts and predicates](../systems/items/contexts-and-predicates.md).",
    )
    out += f"{len(sets)} parameter sets\n\n"
    out += "| set | id | required | optional |\n|---|---|---|---|\n"
    for const, sid, body in sorted(sets, key=lambda r: r[1]):
        keys = PARAM_KEY.findall(body)
        req = [k for kind, k in keys if kind == "required"]
        opt = [k for kind, k in keys if kind == "optional"]
        fmt = lambda names: ", ".join(f"`LootContextParams.{n}`" for n in names) or "—"
        out += f"| `LootContextParamSets.{const}` | *{sid}* | {fmt(req)} | {fmt(opt)} |\n"
    return out


# ------------------------------------------------------------ enchantment hooks
# EnchantmentHelper is the seam between the enchantment system and everything
# else: it holds no state, and the useful artefact is which class calls which
# entry point. The declarations come off the class, the callers off a scan of
# every other .java in the tree for a qualified call (session H).
EH_DECL = re.compile(r"public static (?:<[^>]+> )?([\w.<>?\[\], ]+?) (\w+)\(")


def _java_files(root: str):
    for base, _dirs, files in os.walk(root):
        for name in files:
            if name.endswith(".java"):
                yield os.path.join(base, name)


def enchantment_hooks() -> str:
    path = os.path.join(MC, "world", "item", "enchantment", "EnchantmentHelper.java")
    with open(path, encoding="utf-8", errors="replace") as fh:
        decl_src = fh.read()
    methods: dict[str, int] = {}
    for _ret, name in EH_DECL.findall(decl_src):
        methods[name] = methods.get(name, 0) + 1
    call = re.compile(r"EnchantmentHelper\.(\w+)\(")
    callers: dict[str, set[str]] = {name: set() for name in methods}
    for f in _java_files(ROOT):
        if os.path.abspath(f) == os.path.abspath(path):
            continue
        with open(f, encoding="utf-8", errors="replace") as fh:
            text = fh.read()
        if "EnchantmentHelper." not in text:
            continue
        owner = os.path.basename(f)[:-5]
        for name in call.findall(text):
            if name in callers:
                callers[name].add(owner)
    used = sum(1 for n in callers if callers[n])
    out = header(
        "Enchantment hooks",
        "Every public entry point of `EnchantmentHelper`, with the classes that call it. "
        "The enchantment package barely calls anything and everything calls it, so this table is the "
        "system's real interface: each row is a moment at which some other system asks whether an "
        "enchantment wants to change what happens. Callers are the declaring files, one per class, "
        "excluding `EnchantmentHelper` itself. See "
        "[Enchantments](../systems/items/enchantments.md) for what an enchantment is and "
        "[Enchanting](../systems/items/enchanting.md) for the selection half.",
    )
    out += f"{len(methods)} entry points, {used} of them called from outside the class\n\n"
    out += "| entry point | overloads | called from |\n|---|---:|---|\n"
    for name in sorted(methods):
        who = sorted(callers[name])
        cells = ", ".join(f"`{c}`" for c in who) if who else "*nothing outside the class*"
        out += f"| `EnchantmentHelper.{name}` | {methods[name]} | {cells} |\n"
    return out


# ------------------------------------------------- entity spawn reasons
# `EntitySpawnReason` is passed into `EntityType.create`, `Mob.finalizeSpawn` and
# `SpawnPlacements`, and a handful of classes branch on it. The catalogue the book
# wanted (pass 3 §7) is *what each one gates*, so the second column is every place
# the constant is compared rather than every place it is passed.
REASON_DECL = re.compile(r"public enum EntitySpawnReason \{\s*\n\s*(.*?);", re.S)
REASON_TEST = re.compile(r"EntitySpawnReason\.([A-Z_]+)\b")
# A method signature in Mojang's decompiled output: four or eight spaces, an access modifier,
# a return type, the name. Requiring the modifier is what keeps `if (…) {` and `for (…) {` out —
# without it the walk-up returns the nearest control block and names the wrong method.
JAVA_METHOD = re.compile(
    r"^ {4,8}(?:public|protected|private)(?: (?:static|final|abstract|synchronized|native))* "
    r"(?:@\w+ )*[\w<>\[\],.?]+(?:<[^>]*>)? (\w+)\s*\([^;]*?\)\s*(?:throws [\w, .]+)?\{", re.M)


def _walk(root: str):
    for dirpath, _dirs, files in os.walk(root):
        for f in files:
            if f.endswith(".java"):
                yield os.path.join(dirpath, f)


def _enclosing_method(text: str, pos: int) -> str:
    """The name of the method whose body contains `pos`, or '' if none does."""
    last = ""
    for m in JAVA_METHOD.finditer(text, 0, pos):
        last = m.group(1)
    return last


def spawn_reasons() -> str:
    order = [c.strip() for c in REASON_DECL.search(read("world", "entity", "EntitySpawnReason.java")).group(1).split(",")]
    tests: dict[str, list[tuple[str, str]]] = {c: [] for c in order}
    passes: dict[str, set[str]] = {c: set() for c in order}
    for path in _walk(os.path.dirname(MC)):
        cls = os.path.basename(path)[:-5]
        with open(path, encoding="utf-8", errors="replace") as fh:
            text = fh.read()
        if "EntitySpawnReason." not in text:
            continue
        for m in REASON_TEST.finditer(text):
            const = m.group(1)
            if const not in tests:
                continue
            line_start = text.rfind("\n", 0, m.start()) + 1
            line = text[line_start:text.find("\n", m.end())]
            if re.search(r"[=!]=\s*EntitySpawnReason\.|EntitySpawnReason\.\w+\s*[=!]=", line) and cls != "EntitySpawnReason":
                where = (cls, _enclosing_method(text, m.start()))
                if where not in tests[const]:
                    tests[const].append(where)
            else:
                passes[const].add(cls)
    out = header("Entity spawn reasons", "Every `EntitySpawnReason` constant, in declaration order, with **what each one gates** — the classes that compare against it and so behave differently for that reason — and how many other classes pass it. A reason with an empty *gates* column changes nothing by itself: it is a label the spawn path carries for other code to read. `EntitySpawnReason.isSpawner` folds `SPAWNER` and `TRIAL_SPAWNER` together and `EntitySpawnReason.ignoresLightRequirements` is true of `TRIAL_SPAWNER` alone. See [entity lifecycle](../systems/entities/entity-lifecycle.md#the-other-ways-in).")
    gated = sum(1 for c in order if tests[c])
    out += f"{len(order)} reasons · {gated} of them tested somewhere · {sum(len(v) for v in tests.values())} test sites\n\n"
    out += "| # | reason | what it gates | classes that pass it |\n|---:|---|---|---:|\n"
    for i, c in enumerate(order):
        cells = "; ".join(f"`{k}.{m}`" if m else f"`{k}`" for k, m in tests[c]) or "*nothing tests it*"
        out += f"| {i} | `EntitySpawnReason.{c}` | {cells} | {len(passes[c])} |\n"
    return out


# ------------------------------------------------- Item.Properties weapon helpers
HELPER_DECL = re.compile(r"public Item\.Properties (tool|pickaxe|axe|hoe|shovel|sword|spear)\((.*?)\) \{(.*?)\n        \}", re.S)
ITEM_REG = re.compile(r"public static final Item (\w+) = registerItem\((.*?)\);\n", re.S)


def weapon_helpers() -> str:
    item_src = read("world", "item", "Item.java")
    material_src = read("world", "item", "ToolMaterial.java")
    items_src = read("world", "item", "Items.java")
    bodies = {m.group(1): (m.group(2), m.group(3)) for m in HELPER_DECL.finditer(item_src)}

    def installs(name: str, seen: tuple = ()) -> list[str]:
        """The DataComponents a helper ends up setting, following the one hop into ToolMaterial."""
        args, body = bodies[name]
        found = list(dict.fromkeys(re.findall(r"DataComponents\.(\w+)", body)))
        for callee in re.findall(r"this\.(tool|pickaxe|axe|hoe|shovel|sword|spear)\(", body):
            if callee not in seen:
                found += [c for c in installs(callee, seen + (name,)) if c not in found]
        for apply in re.findall(r"material\.(apply\w+)\(", body):
            m = re.search(rf"public Item\.Properties {apply}\(.*?\n    \}}", material_src, re.S)
            if m:
                found += [c for c in re.findall(r"DataComponents\.(\w+)", m.group(0)) if c not in found]
                for common in re.findall(r"this\.(applyCommonProperties)\(", m.group(0)):
                    c2 = re.search(rf"public Item\.Properties {common}\(.*?\n    \}}", material_src, re.S)
                    if c2:
                        found += [c for c in re.findall(r"DataComponents\.(\w+)", c2.group(0)) if c not in found]
        return found

    # every Items entry that reaches a helper, directly or through the item class that wraps it
    wrappers = {}
    for path in _walk(os.path.join(MC, "world", "item")):
        with open(path, encoding="utf-8", errors="replace") as fh:
            t = fh.read()
        m = re.search(r"super\(properties\.(tool|pickaxe|axe|hoe|shovel|sword|spear)\(", t)
        if m:
            wrappers[os.path.basename(path)[:-5]] = m.group(1)
    rows = []
    for m in ITEM_REG.finditer(items_src):
        call = " ".join(m.group(2).split())
        h = re.search(r"\.(tool|pickaxe|axe|hoe|shovel|sword|spear)\(ToolMaterial\.(\w+),\s*([-\d.F]+),\s*([-\d.F]+)", call)
        if h:
            rows.append((m.group(1), h.group(1), h.group(2), h.group(3), h.group(4)))
            continue
        w = re.search(r"new (\w+)\(ToolMaterial\.(\w+),\s*([-\d.F]+),\s*([-\d.F]+)", call)
        if w and w.group(1) in wrappers:
            rows.append((m.group(1), wrappers[w.group(1)] + f" (`{w.group(1)}`)", w.group(2), w.group(3), w.group(4)))

    out = header("The weapon helpers on `Item.Properties`", "The seven `Item.Properties` methods that turn a bare item into something you can hit with, what each one installs, and every item built by one. `Item.Properties.tool` is the shared body: `pickaxe`, `axe`, `hoe` and `shovel` are it with a mining tag and a shield-disable time filled in; `sword` and `spear` go their own way. Three of the six tool families need a class of their own because they also do something on right-click, and three are plain `Item`s the helper alone describes. See [items and stacks](../systems/items/items-and-stacks.md) and [data components](../systems/foundations/data-components.md).")
    out += "| helper | delegates to | components it sets | attributes |\n|---|---|---|---|\n"
    for name in ("tool", "pickaxe", "axe", "hoe", "shovel", "sword", "spear"):
        args, body = bodies[name]
        deleg = re.findall(r"this\.(tool|pickaxe|axe|hoe|shovel|sword|spear)\(", body) + re.findall(r"material\.(apply\w+)\(", body)
        comps = ", ".join(f"`DataComponents.{c}`" for c in installs(name)) or "—"
        attrs = ", ".join(f"`Attributes.{a}`" for a in dict.fromkeys(re.findall(r"Attributes\.(\w+)", body))) or \
            ("`Attributes.ATTACK_DAMAGE`, `Attributes.ATTACK_SPEED` (through `ToolMaterial`)" if deleg else "—")
        out += f"| `Item.Properties.{name}` | {', '.join(f'`{d}`' for d in deleg) or '—'} | {comps} | {attrs} |\n"
    out += f"\n## The {len(rows)} items built by one\n\n*damage* and *speed* are the two baselines the call passes; the material adds its own attack-damage bonus on top.\n\n"
    out += "| item | helper | material | damage baseline | speed baseline |\n|---|---|---|---:|---:|\n"
    for name, helper, mat, dmg, spd in rows:
        h = helper if "`" in helper else f"`Item.Properties.{helper}`"
        out += f"| `Items.{name}` | {h} | `ToolMaterial.{mat}` | {dmg.rstrip('F')} | {spd.rstrip('F')} |\n"
    return out


# ------------------------------------------------- structure spawn overrides
def spawn_overrides() -> str:
    import json
    base = os.path.join(ROOT, "data", "minecraft", "worldgen", "structure")
    declared, rows = 0, []
    for f in sorted(os.listdir(base)):
        if not f.endswith(".json"):
            continue
        with open(os.path.join(base, f), encoding="utf-8") as fh:
            d = json.load(fh)
        if "spawn_overrides" not in d:
            continue
        declared += 1
        for cat, v in sorted(d["spawn_overrides"].items()):
            spawns = v.get("spawns", [])
            what = ", ".join(f"`{e['type'].split(':')[-1]}` ({e['weight']}, {e['minCount']}–{e['maxCount']})" for e in spawns) \
                or "**nothing** — the category is suppressed inside the box"
            rows.append((f[:-5], cat, v.get("bounding_box", "?"), what))
    structures = sorted({r[0] for r in rows})
    out = header("Structure spawn overrides", "Which structures replace a biome's spawn list, for which mob category, and with what. A structure JSON's `spawn_overrides` map is read into `Structure.spawnOverrides`; `NaturalSpawner` asks the first structure at the position that declares an override for the category, and if one answers, the biome's list is not consulted at all. An override with an **empty** spawn list is therefore a *ban*, not a no-op. *box* is `piece` (only inside a piece's own bounding box) or `full` (anywhere in the structure's). The mechanism is on [entity lifecycle](../systems/entities/entity-lifecycle.md#a-spawn-attempt-is-a-filter-not-a-conversation); the nether fortress has a second, hard-coded list in front of this one.")
    out += f"{declared} structures carry the field · **{len(structures)}** declare an override · {len(rows)} overrides in all\n\n"
    out += "| structure | category | box | what spawns instead (weight, min–max) |\n|---|---|---|---|\n"
    for name, cat, box, what in rows:
        out += f"| `{name}` | {cat} | {box} | {what} |\n"
    out += (f"\nThe other {declared - len(structures)} structures that carry the field carry it empty, "
            "which is the same as not carrying it: the biome's list stands.\n")
    return out


VIEWS = {
    "packets": packets,
    "registries": registries,
    "components": components,
    "gamerules": gamerules,
    "entity-data-serializers": serializers,
    "attributes": attributes,
    "loot-context-params": loot_context_params,
    "enchantment-hooks": enchantment_hooks,
    "spawn-reasons": spawn_reasons,
    "weapon-helpers": weapon_helpers,
    "structure-spawn-overrides": spawn_overrides,
}


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
