#!/usr/bin/env python3
"""Every name inside a mermaid block exists in the decompile — the gate over figures (pass 7).

`verify_names.py` checks backticked names, and a mermaid label carries none: a participant's
expansion (`participant SL as ServerLevel`), a node label, a message (`SL->>CM: getChunk`), a
note, a subgraph title, a state name. Those are the four-hundred-odd tokens no gate had seen
before pass 7, and a figure is where a fact-check found the prose right and the picture wrong
nine times in pass 4. This reads every ```mermaid block under src/ (the shared figures under
src/figures/ included; generated pages skipped, as verify_names.py skips them) and checks, against
the same index verify_names.py builds:

  class     a CamelCase token with an internal capital (`ChunkMap`, `NaturalSpawner`) must be a
            class in the decompile or one of the library trees, or in verify_names.ALLOW; a
            plural of a class name (`two ClientboundBlockUpdatePackets`) resolves to the singular
  member    a dotted token (`Class.member`, `Outer.Inner.member`) must resolve the way
            verify_names.py resolves it; a call (`name(`) with no class is checked as below
  message   in a sequence diagram, a message whose text opens on a method name — `A->>B:
            method`, `method(...)`, `method — …`, `method, …` — names a member of the lane it is
            sent *to*; the lane's class comes from the page's participant line or from the key in
            TEMPLATE.md, and a word lane (Main, Netty, Worker…) is skipped. A bare lower-case
            head that is not a member is a *note*, not a failure, because `load` and `tick` are
            also English; a humped or parenthesised head that is not a member fails
  expansion the class a participant expands to must exist (check_lanes.py checks it against the
            key; this checks the ones the key does not know)

Skipped, and counted: ALL-CAPS tokens (enum constants, `MISC`), single-word capitalised tokens
(`Entity` is a class and `Then` is not, and the label cannot say which), lane ids, and anything
in ALLOW. Unqualified humped members inside flowchart or state labels (`runAllTasks` with no
class beside it) are listed as notes: the lane qualifies a message, nothing qualifies a node.

Report-only by default — pass 7 runs it that way and reads the list; `--strict` exits 1 on any
failure, which is what `tools/deploy.sh` switches to at the pass's close. `--mentions` prints
class → pages as JSON, and `verify_names.py --index` calls `figure_mentions()` here so that a
class named only inside a figure reaches the class index (pass 5, session A: 135 page pairs the
index could not see).

Usage:
    python tools/check_figure_names.py                    # report: failures, then notes, then a summary
    python tools/check_figure_names.py --strict           # exit 1 on any failure
    python tools/check_figure_names.py --pages src/systems/world   # a part or a page
    python tools/check_figure_names.py --notes            # also print the notes (bare heads, unqualified members)
    python tools/check_figure_names.py --mentions         # class -> pages, as JSON
    python tools/check_figure_names.py --probe            # prove it fails on a bad class, a bad member and a bad message
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import diagram_arrows as da                     # noqa: E402
from verify_names import ALLOW, load_index, members_of, GENERATED_MARK   # noqa: E402
from check_lanes import read_key                # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "src")
TEMPLATE = os.path.join(ROOT, "TEMPLATE.md")

FENCE = re.compile(r"^\s*(`{3,}|~{3,})\s*(\w*)\s*$")
SEQ_NOTE = re.compile(r"^\s*[Nn]ote\s+(over|left of|right of)\s+([^:]+):\s*(.*)$")
SEQ_BLOCK = re.compile(r"^\s*(rect|loop|alt|else|opt|par|and|critical|option|break|box)\b\s*(.*)$")
SUBGRAPH = re.compile(r"^\s*subgraph\s+(?:([A-Za-z0-9_]+)\s*)?(?:\[\s*\"?(.*?)\"?\s*\])?\s*(.*)$")
STATE_TRANS = re.compile(r"^\s*(\[\*\]|[\w.\-\"]+)\s*-->\s*(\[\*\]|[\w.\-\"]+)\s*(?::\s*(.*))?$")
STATE_DEF = re.compile(r"^\s*state\s+\"([^\"]+)\"\s+as\s+(\w+)")
STATE_NOTE = re.compile(r"^\s*note\s+(?:left of|right of)\s+[\w.\-]+\s*:\s*(.*)$")
COLOUR_LINE = re.compile(r"^\s*(classDef|style|linkStyle|class )\b")

DOTTED = re.compile(r"(?<![\w/`.])([A-Z][A-Za-z0-9]*(?:\.[A-Za-z_][A-Za-z0-9_]*)+)(?![\w/])")
CAMEL = re.compile(r"\b(?=[A-Z][A-Za-z0-9]*[a-z])([A-Z][a-z0-9]*[A-Z][A-Za-z0-9]*)\b")
CALL = re.compile(r"\b([a-z][A-Za-z0-9]*)\s*\(")
LOWER_CAMEL = re.compile(r"\b([a-z]+[A-Z][A-Za-z0-9]*)\b")
# the head of a message: `getChunk`, `getChunk(pos)`, `tick — …`, `load, wrapped …`, `spin builds …`; a head that
# starts with a capital is a class (a reply carrying an object, a packet) and is checked as one, not as a method
MSG_HEAD = re.compile(r"^\s*([a-z_][A-Za-z0-9_]*)(?:\s*\(|\s*[,—–:;.]|\s*$|\s+)")
# the class a file declares, and what it extends and implements — for the message check, which must accept a
# member a lane's class inherits (a message to `DedicatedServer` may name `MinecraftServer.runServer`)
DECL = re.compile(r"\b(?:class|interface|enum|record)\s+([A-Za-z_][A-Za-z0-9_]*)\s*(?:<[^{]*?>)?\s*(?:\([^)]*\))?\s*((?:extends|implements)[^{]*)\{")
PACKET = re.compile(r"^(?:Clientbound|Serverbound)[A-Z][A-Za-z0-9]*Packet$")
ENGLISH_HEADS = {
    "the", "a", "an", "then", "only", "and", "or", "if", "when", "no", "not", "one", "two", "three", "four", "this", "that",
    "it", "its", "nothing", "every", "each", "all", "for", "from", "in", "on", "at", "to", "of", "as", "by", "with", "but",
    "so", "now", "here", "there", "still", "also", "both", "per", "via", "after", "before", "until", "while", "once", "more",
    "less", "same", "new", "old", "done", "first", "last", "next", "back", "out", "up", "down", "off", "over", "under", "into",
    "onto", "yes", "static", "level", "main", "spin", "nothing", "none", "another", "other", "some", "any", "yet", "again",
    "hands", "hand", "asks", "ask", "sends", "send", "returns", "return", "runs", "run", "reads", "read", "writes", "write",
    "calls", "call", "walks", "walk", "builds", "build", "goes", "go", "comes", "come", "takes", "take", "gets", "get",
    "puts", "put", "tells", "tell", "sets", "set", "is", "are", "was", "were", "has", "have", "had", "does", "do", "did",
    "can", "cannot", "may", "will", "would", "should", "must", "which", "what", "who", "where", "why", "how", "because",
    "since", "without", "within", "between", "through", "across", "against", "around", "about", "above", "below", "inside",
    "outside", "instead", "either", "neither", "otherwise", "except", "unless", "whether", "though", "although", "even",
    "just", "such", "very", "much", "many", "most", "few", "several", "own", "same", "whole", "half", "later", "earlier",
    "already", "always", "never", "sometimes", "often", "soon", "today", "tonight", "tomorrow", "server", "client", "wire",
    "disk", "worker", "packet", "packets", "chunk", "chunks", "block", "blocks", "entity", "entities", "player", "players",
    "tick", "ticks", "frame", "frames", "queue", "queued", "empty", "full", "true", "false", "null", "air", "water", "lava",
}


def fences_of(path: str):
    """Every mermaid block on a page: (first line, [(line, text)…])."""
    with open(path, encoding="utf-8") as fh:
        lines = fh.read().split("\n")
    i, n = 0, len(lines)
    while i < n:
        m = FENCE.match(lines[i])
        if m and m.group(2) == "mermaid":
            start, body = i + 1, []
            i += 1
            while i < n and not (FENCE.match(lines[i]) and not FENCE.match(lines[i]).group(2)):
                body.append((i + 1, lines[i]))
                i += 1
            yield start, body
        elif m and m.group(2):
            i += 1
            while i < n and not (FENCE.match(lines[i]) and not FENCE.match(lines[i]).group(2)):
                i += 1
        i += 1


def labels_of(body):
    """(line, role, text, target_lane) for every label; the lanes declared on the block."""
    first = next((raw.strip() for _ln, raw in body if raw.strip() and not raw.strip().startswith("%%")), "")
    kind = first.split()[0] if first else "?"
    lanes: dict[str, str] = {}
    out = []
    for ln, raw in body:
        t = raw.strip()
        if not t or t.startswith("%%") or COLOUR_LINE.match(t):
            continue
        if kind == "sequenceDiagram":
            m = da.PARTICIPANT.match(t)
            if m:
                lanes[m.group(1)] = (m.group(2) or m.group(1)).strip()
                out.append((ln, "participant", lanes[m.group(1)], m.group(1)))
                continue
            m = da.SEQ_MSG.match(t)
            if m:
                out.append((ln, "message", m.group(4).strip(), m.group(3)))
                continue
            m = SEQ_NOTE.match(t)
            if m:
                out.append((ln, "note", m.group(3).strip(), None))
                continue
            m = SEQ_BLOCK.match(t)
            if m and m.group(2):
                out.append((ln, "block", m.group(2).strip(), None))
                continue
        elif kind in ("flowchart", "graph"):
            m = SUBGRAPH.match(t)
            if m:
                out.append((ln, "subgraph", (m.group(2) or m.group(3) or "").strip().strip('"'), None))
                continue
            if t == "end":
                continue
            for m in da.NODE_DEF.finditer(t):
                out.append((ln, "node", da.strip_label(m.group(2)), None))
            parts = da.FLOW_EDGE.split(t)
            for k in range(1, len(parts) - 1, 2):
                lab = da.label_of(parts[k]).strip().strip('"').strip()
                if lab:
                    out.append((ln, "edge", lab, None))
        elif kind.startswith("stateDiagram"):
            m = STATE_DEF.match(t)
            if m:
                out.append((ln, "state", m.group(1), None))
                continue
            m = STATE_TRANS.match(t)
            if m:
                if m.group(3):
                    out.append((ln, "edge", m.group(3).strip(), None))
                continue
            m = STATE_NOTE.match(t)
            if m:
                out.append((ln, "note", m.group(1), None))
    return kind, lanes, out


class Checker:
    def __init__(self, mc_source: str, libs: str, template: str = TEMPLATE):
        self.classes, self.packages = load_index(mc_source, libs)
        self.member_cache: dict[str, set[str]] = {}
        key_classes, key_words, _problems = read_key(template)
        self.key_classes = key_classes
        self.key_words = set(key_words)
        self.mentions: dict[str, set[str]] = {}
        self.super_cache: dict[str, list[str]] = {}
        self.nested: dict[str, set[str]] | None = None
        self.checked = 0
        self.skipped = 0

    def members(self, cls: str) -> set[str]:
        if cls not in self.member_cache:
            self.member_cache[cls] = members_of(self.classes[cls])
        return self.member_cache[cls]

    def supers(self, cls: str) -> list[str]:
        """The classes and interfaces `cls` extends or implements, by simple name, as far as the decompile has them."""
        if cls in self.super_cache:
            return self.super_cache[cls]
        found: list[str] = []
        for p in self.classes.get(cls, []):
            try:
                with open(p, encoding="utf-8", errors="replace") as fh:
                    text = fh.read(20000)
            except OSError:
                continue
            for m in DECL.finditer(text):
                if m.group(1) != cls:
                    continue
                clause = re.sub(r"<[^<>]*>", "", m.group(2))
                clause = re.sub(r"<[^<>]*>", "", clause)
                for name in re.findall(r"\b([A-Z][A-Za-z0-9_]*)\b", clause):
                    if name in self.classes and name != cls and name not in found:
                        found.append(name)
                break
        self.super_cache[cls] = found
        return found

    def inherited_member(self, cls: str, member: str, depth: int = 0, seen: set | None = None) -> str | None:
        """The class in `cls`'s ancestry that declares `member`, or None."""
        seen = seen if seen is not None else set()
        if cls in seen or depth > 10 or cls not in self.classes:
            return None
        seen.add(cls)
        if member in self.members(cls):
            return cls
        for s in self.supers(cls):
            hit = self.inherited_member(s, member, depth + 1, seen)
            if hit:
                return hit
        return None

    def nested_outer(self, name: str) -> list[str]:
        """The top-level classes that declare a nested class, interface, enum or record called `name`."""
        if self.nested is None:
            self.nested = {}
            decl = re.compile(r"^\s+(?:public |protected |private |static |final |abstract |sealed |non-sealed )*(?:class|interface|enum|record)\s+([A-Za-z_][A-Za-z0-9_]*)")
            for cls, paths in self.classes.items():
                for p in paths:
                    try:
                        with open(p, encoding="utf-8", errors="replace") as fh:
                            for line in fh:
                                m = decl.match(line)
                                if m and m.group(1) != cls:
                                    self.nested.setdefault(m.group(1), set()).add(cls)
                    except OSError:
                        pass
        return sorted(self.nested.get(name, ()))

    def class_ok(self, name: str) -> bool:
        if name in self.classes or name in ALLOW:
            return True
        if name.endswith("s") and name[:-1] in self.classes:     # a plural in a label
            return True
        return False

    def dotted_ok(self, token: str) -> str | None:
        """None when the token resolves; otherwise the reason."""
        cls, _, member = token.partition(".")
        if cls in ALLOW and not member:
            return None
        if cls not in self.classes:
            if token in ALLOW:
                return None
            return f"no class {cls}"
        segs = member.split("(")[0].split(".")
        missing = [s for s in segs if s and s not in self.members(cls) and not self.inherited_member(cls, s)]
        if missing:
            return f"no member {missing[0]} on {cls}"
        return None

    def check_page(self, path: str, rel: str):
        failures, notes = [], []
        for start, body in fences_of(path):
            kind, lanes, labels = labels_of(body)
            for ln, role, text, target in labels:
                text = re.sub(r"<br\s*/?>", " ", text)
                seen_dotted = set()
                for m in DOTTED.finditer(text):
                    tok = m.group(1)
                    seen_dotted.add(tok)
                    self.checked += 1
                    why = self.dotted_ok(tok)
                    if why:
                        failures.append((rel, ln, tok, why))
                    else:
                        cls = tok.split(".")[0]
                        if cls in self.classes:
                            self.mentions.setdefault(cls, set()).add(rel)
                stripped = DOTTED.sub(" ", text)
                if role == "participant":
                    if target in self.key_words or text.startswith("*"):
                        self.skipped += 1       # a word lane: a thread, the wire, the disk
                        continue
                    self.checked += 1
                    outer = text.split(".")[0]
                    if not self.class_ok(outer):
                        failures.append((rel, ln, text, "no such class for the lane"))
                    elif outer in self.classes:
                        self.mentions.setdefault(outer, set()).add(rel)
                    continue
                for m in CAMEL.finditer(stripped):
                    tok = m.group(1)
                    self.checked += 1
                    if self.class_ok(tok):
                        base = tok if tok in self.classes else tok[:-1]
                        if base in self.classes:
                            self.mentions.setdefault(base, set()).add(rel)
                    else:
                        outers = self.nested_outer(tok)
                        if outers:
                            notes.append((rel, ln, tok, f"a nested class named without its outer class: {', '.join(o + '.' + tok for o in outers[:3])}"))
                            self.mentions.setdefault(outers[0], set()).add(rel) if len(outers) == 1 else None
                        else:
                            failures.append((rel, ln, tok, "no such class"))
                # a message's head names a member of the lane it is sent to
                if role == "message" and target:
                    hm = MSG_HEAD.match(stripped)
                    head = hm.group(1) if hm else None
                    if head and target in lanes and lanes[target] not in self.key_words and not lanes[target].startswith("*"):
                        cls = lanes[target].split(".")[0]
                        humped = bool(re.search(r"[a-z][A-Z]", head)) or bool(re.match(r"^\s*" + re.escape(head) + r"\s*\(", stripped))
                        if cls in self.classes:
                            self.checked += 1
                            if head in self.members(cls) or head in ALLOW or self.inherited_member(cls, head):
                                pass
                            elif humped:
                                failures.append((rel, ln, head, f"no member {head} on {cls} (the lane the message is sent to)"))
                            elif head.lower() not in ENGLISH_HEADS and head[0].islower():
                                notes.append((rel, ln, head, f"bare message head that is not a member of {cls}"))
                        elif humped:
                            self.skipped += 1
                    elif head and re.search(r"[a-z][A-Z]", head) and target not in lanes:
                        notes.append((rel, ln, head, f"message to undeclared lane {target}"))
                elif role in ("node", "edge", "subgraph", "state", "note", "block"):
                    for m in LOWER_CAMEL.finditer(stripped):
                        tok = m.group(1)
                        if tok in ALLOW or tok in ENGLISH_HEADS:
                            continue
                        # qualified by a class in the same label? then it was checked as that class's member above
                        notes.append((rel, ln, tok, f"unqualified member in a {kind.split('-')[0]} {role} label"))
                    for m in CALL.finditer(stripped):
                        tok = m.group(1)
                        if not re.search(r"[a-z][A-Z]", tok) and tok in ENGLISH_HEADS:
                            continue
                        notes.append((rel, ln, tok, f"unqualified call in a {kind.split('-')[0]} {role} label"))
        return failures, notes


def walk(src: str, only: list[str] | None):
    for dirpath, _d, files in os.walk(src):
        for f in sorted(files):
            if not f.endswith(".md"):
                continue
            path = os.path.join(dirpath, f)
            rel = os.path.relpath(path, src).replace(os.sep, "/")
            if rel.startswith("generated/"):
                continue
            if only and not any(os.path.abspath(path) == os.path.abspath(o) or os.path.abspath(path).startswith(os.path.abspath(o) + os.sep) for o in only):
                continue
            if rel.startswith("reference/"):
                with open(path, encoding="utf-8") as fh:
                    if GENERATED_MARK in fh.read(400):
                        continue
            yield path, rel


def figure_mentions(src: str = SRC, mc_source: str | None = None, libs: str | None = None) -> dict[str, set[str]]:
    """class -> pages that name it inside a figure, for verify_names.py --index."""
    mc_source = mc_source or os.environ.get("MC_SOURCE", os.path.join(ROOT, "reference", "26.2"))
    libs = libs or os.environ.get("MC_LIBS", os.path.join(ROOT, "reference", "libs"))
    c = Checker(mc_source, libs)
    for path, rel in walk(src, None):
        c.check_page(path, rel)
    return c.mentions


PROBE = """# Probe

```mermaid
sequenceDiagram
    participant SL as ServerLevel
    participant MS as MinecraftServer
    participant Main as Main
    participant ZZ as NoSuchClassAnywhere
    SL->>MS: tickServer
    SL->>MS: noSuchMethodHere(arg)
    SL->>MS: the factory it was handed runs here
    Main->>SL: load, wrapped in Util.blockUntilDone
    Note over SL,MS: ChunkMap and ChunkMapp and MinecraftServer.tickServer and ServerLevel.noSuchMemberEither
```

```mermaid
flowchart TD
    A["NaturalSpawner.createState walks every entity"] --> B{"Mob.finalizeSpawn"}
    B -->|"two ClientboundBlockUpdatePackets"| C["runAllTasks then FrobnicatorThing then SpawnState"]
    C --> D["DedicatedServer.runServer"]
```
"""


def probe(mc_source: str, libs: str) -> int:
    tmp = tempfile.mkdtemp(prefix="figname-")
    d = os.path.join(tmp, "systems", "world")
    os.makedirs(d)
    p = os.path.join(d, "probe.md")
    with open(p, "w", encoding="utf-8") as fh:
        fh.write(PROBE)
    c = Checker(mc_source, libs)
    failures, notes = c.check_page(p, "systems/world/probe.md")
    got = {(f[1], f[2]) for f in failures}
    checks = [
        ("the bad participant expansion fails", (8, "NoSuchClassAnywhere") in got),
        ("the humped message head that is not a member of the target lane fails", (10, "noSuchMethodHere") in got),
        ("the good message head (tickServer on MinecraftServer) passes", not any(f[2] == "tickServer" for f in failures)),
        ("an English message is not a failure", not any(f[1] == 11 for f in failures)),
        ("a message to a word lane is skipped", not any(f[1] == 12 for f in failures)),
        ("the bad class in a note fails and the good one passes", (13, "ChunkMapp") in got and not any(f[2] == "ChunkMap" for f in failures)),
        ("the bad dotted member fails and the good one passes", (13, "ServerLevel.noSuchMemberEither") in got and not any(f[2] == "MinecraftServer.tickServer" for f in failures)),
        ("a plural of a class name passes", not any("ClientboundBlockUpdatePackets" in f[2] for f in failures)),
        ("a bad class in a flowchart node fails", any(f[2] == "FrobnicatorThing" for f in failures)),
        ("a nested class named bare is a note, not a failure", any(n[2] == "SpawnState" and "NaturalSpawner.SpawnState" in n[3] for n in notes) and not any(f[2] == "SpawnState" for f in failures)),
        ("an inherited member resolves (DedicatedServer.runServer is MinecraftServer's)", not any(f[2] == "DedicatedServer.runServer" for f in failures)),
        ("an unqualified member in a flowchart label is a note", any(n[2] == "runAllTasks" for n in notes)),
        ("figure mentions include ChunkMap and NaturalSpawner", "ChunkMap" in c.mentions and "NaturalSpawner" in c.mentions),
        ("exactly the five failures expected", len(failures) == 5),
    ]
    ok = True
    for what, passed in checks:
        print(f"{'pass' if passed else 'FAIL'}  {what}")
        ok &= bool(passed)
    if not ok:
        for f in failures:
            print("   failure:", f)
        for n in notes:
            print("   note:", n)
    print("probe passed" if ok else "PROBE FAILED")
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--src", default=SRC)
    ap.add_argument("--mc-source", default=os.environ.get("MC_SOURCE", os.path.join(ROOT, "reference", "26.2")))
    ap.add_argument("--libs", default=os.environ.get("MC_LIBS", os.path.join(ROOT, "reference", "libs")))
    ap.add_argument("--pages", nargs="*", help="restrict to these files or directories")
    ap.add_argument("--strict", action="store_true", help="exit 1 on any failure")
    ap.add_argument("--notes", action="store_true", help="print the notes too")
    ap.add_argument("--mentions", action="store_true", help="print class -> pages as JSON")
    ap.add_argument("--probe", action="store_true")
    args = ap.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if not os.path.isdir(os.path.join(args.mc_source, "net", "minecraft")):
        print(f"no decompile at {args.mc_source} (set MC_SOURCE)", file=sys.stderr)
        return 2
    if args.probe:
        return probe(args.mc_source, args.libs)
    c = Checker(args.mc_source, args.libs)
    failures, notes = [], []
    blocks = 0
    for path, rel in walk(args.src, args.pages):
        blocks += sum(1 for _ in fences_of(path))
        f, n = c.check_page(path, rel)
        failures += f
        notes += n
    if args.mentions:
        print(json.dumps({k: sorted(v) for k, v in sorted(c.mentions.items())}, indent=1))
        return 0
    for rel, ln, tok, why in failures:
        print(f"src/{rel}:{ln}: `{tok}` ({why})")
    if args.notes:
        print()
        for rel, ln, tok, why in notes:
            print(f"note  src/{rel}:{ln}: `{tok}` ({why})")
    print(f"\n{c.checked} names checked in {blocks} figures: {len(failures)} unresolved, {len(notes)} notes, "
          f"{c.skipped} skipped; {len(c.mentions)} classes named in figures across {len({p for ps in c.mentions.values() for p in ps})} pages")
    return 1 if (args.strict and failures) else 0


if __name__ == "__main__":
    sys.exit(main())
