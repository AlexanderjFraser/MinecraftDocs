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

A `classDiagram` is read the same way, and until pass 7's session G it was not read at all:
the class name on a `class Foo` line, the display label of `class Foo["Label"]`, every member
line inside the braces, both ends of a relation, and the relation's own `: label`. F10 sends a
vocabulary page to this kind, so the five class diagrams sessions B to F drew had every name
in them unchecked — the fifth thing this pass has found a gate blind to. A **member line is
checked against its own class box**, the way a message is checked against the lane it is sent
to: `int popTime` inside `class ItemStack` names `ItemStack.popTime`, so it is a failure rather
than a note when no such member exists, and it needs no `Class.` prefix in the figure — the box
is the prefix.

Skipped, and counted: ALL-CAPS tokens (enum constants, `MISC`), single-word capitalised tokens
(`Entity` is a class and `Then` is not, and the label cannot say which) — except a word one
letter away from a one-word class in the lane key (`Entty`, `Palyer`), which fails — lane ids,
anything in ALLOW, and any word the page sets in *italics* outside its figures (a profiler zone,
a task name: verify_names.py's convention for a word that is not an identifier).

F12, as pass 7's session O applied it at the close: an unqualified humped member inside a
flowchart, state, note, subgraph or edge label (`runAllTasks` with no class beside it) **fails**
— the lane qualifies a message, nothing qualifies a node — and so does a nested class named
without its outer class. In a classDiagram a member line is qualified by its box and a relation's
label by either of its two boxes. What stays a *note*: a bare lower-case message head that is not
a member (F12(d), `load` is also English), and a qualified head whose class is neither the lane's
nor kin to it (`Gizmos.billboardTextOverMob` on a renderer's lane) — a static façade, an object
with no lane, or the lane's own inner class, each ruled once in pass7-brief.md; or the
caller's-method-at-the-callee fault in its qualified spelling, which is why it is listed.

Report-only by default; `--strict` exits 1 on any failure, and `tools/deploy.sh` runs it that way
from pass 7's close. `--mentions` prints
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
# A `rect` band carries a colour and no label at all, and a `box` may carry one before its
# label: `rect rgba(0, 0, 0, 0.04)` is the tick band F8 tells every part session to draw, and
# read as a label its colour becomes a call named `rgba`. Strip the colour before the label.
SEQ_COLOUR = re.compile(r"^\s*(?:transparent|(?:rgba?|hsla?)\s*\([^)]*\)|#[0-9A-Fa-f]{3,8})\s*")
SUBGRAPH = re.compile(r"^\s*subgraph\s+(?:([A-Za-z0-9_]+)\s*)?(?:\[\s*\"?(.*?)\"?\s*\])?\s*(.*)$")
STATE_TRANS = re.compile(r"^\s*(\[\*\]|[\w.\-\"]+)\s*-->\s*(\[\*\]|[\w.\-\"]+)\s*(?::\s*(.*))?$")
STATE_DEF = re.compile(r"^\s*state\s+\"([^\"]+)\"\s+as\s+(\w+)")
STATE_NOTE = re.compile(r"^\s*note\s+(?:left of|right of)\s+[\w.\-]+\s*:\s*(.*)$")
COLOUR_LINE = re.compile(r"^\s*(classDef|style|linkStyle|class )\b")
# classDiagram — the kind F10 sends a vocabulary page to, and the one this gate could not
# read at all until pass 7's session G: `class Foo["Label"] {`, the member lines inside the
# braces, and a relation with an optional `: label`. A bare `class Foo` line is also how a
# flowchart or a state diagram sets a colour class, which is why COLOUR_LINE swallows it and
# why the classDiagram branch must be taken before that test.
CLASS_DEF = re.compile(r'^\s*class\s+([A-Za-z_][A-Za-z0-9_.]*)\s*(?:\[\s*"(.*?)"\s*\])?\s*\{?\s*$')
# an inheritance head is two characters (`<|--`, `--|>`), so the arrow ends take up to two
CLASS_REL = re.compile(r'^\s*([A-Za-z_]\w*)\s*(?:"[^"]*"\s*)?([<>ox|*]{0,2}(?:--|\.\.)[<>ox|*]{0,2})\s*(?:"[^"]*"\s*)?([A-Za-z_]\w*)\s*(?::\s*(.*))?$')
CLASS_NOTE = re.compile(r'^\s*note(?:\s+for\s+[A-Za-z_]\w*)?\s+"(.*)"\s*$')
CLASS_ANNOT = re.compile(r"^\s*<<.*>>\s*$")
# a classDiagram member line read as a declaration: its last token humped, or parenthesised
# (from session M) or a one-word method, if it is parenthesised: `boolean check(PermissionSet)`
MEMBER_LINE = re.compile(r"(?:^|[\s<>~,*])([a-z_][A-Za-z0-9_]*[A-Z][A-Za-z0-9_]*(?=\s*(?:\(.*)?$)|[a-z_][A-Za-z0-9_]*(?=\s*\(.*$))")

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
    open_class: str | None = None
    out = []
    # `class CM["ChunkMap"]` names the box CM and displays ChunkMap: the id is an alias the way a
    # lane abbreviation is, so the display label carries the name and the id is not a class.
    aliases: dict[str, str] = {}
    if kind == "classDiagram":
        for _ln, raw in body:
            m = CLASS_DEF.match(raw.strip())
            if m and m.group(2):
                aliases[m.group(1)] = m.group(2)
    for ln, raw in body:
        t = raw.strip()
        if not t or t.startswith("%%") or (COLOUR_LINE.match(t) and kind != "classDiagram"):
            continue
        if kind == "sequenceDiagram":
            m = da.PARTICIPANT.match(t)
            if m:
                # A lane whose class name is wider than the box carries its own break at a
                # CamelCase boundary (`as PersistentEntity<br/>SectionManager`), so that mermaid
                # does not hyphenate the name mid-word; the gate reads it closed up (pass 7, A).
                lanes[m.group(1)] = re.sub(r"<br\s*/?>", "", (m.group(2) or m.group(1))).strip()
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
            if m:
                rest = m.group(2).strip()
                if m.group(1) == "rect":
                    continue                      # a colour, never a label
                if m.group(1) == "box":
                    rest = SEQ_COLOUR.sub("", rest, count=1).strip()
                if rest:
                    out.append((ln, "block", rest, None))
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
        elif kind == "classDiagram":
            if t == "}":
                open_class = None
                continue
            if t in ("{",) or t == "classDiagram" or CLASS_ANNOT.match(t) or t.startswith("direction "):
                continue
            m = CLASS_NOTE.match(t)
            if m:
                out.append((ln, "note", m.group(1), None))
                continue
            m = CLASS_DEF.match(t)
            if m:
                if m.group(2):
                    out.append((ln, "node", m.group(2), None))
                else:
                    out.append((ln, "classname", m.group(1), None))
                open_class = m.group(1) if t.endswith("{") else None
                continue
            m = CLASS_REL.match(t)
            if m:
                for end in (m.group(1), m.group(3)):
                    if end not in aliases:
                        out.append((ln, "classname", end, None))
                if m.group(4):
                    # a relation's label is qualified by the two boxes it joins (session O)
                    ends = "|".join(aliases.get(e, e) for e in (m.group(1), m.group(3)))
                    out.append((ln, "edge", m.group(4).strip(), ends))
                continue
            # anything else inside the braces is a member line — and its own class box qualifies
            # it, the way a lane qualifies a message, so it is checked rather than noted
            out.append((ln, "member", t.lstrip("+-#~"), open_class))
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


ITALIC = re.compile(r"(?<![*\w])[*_]([a-z][A-Za-z0-9]*)[*_](?![*\w])")


def italic_words(path: str) -> set[str]:
    """The words a page sets in italics outside its figures -- verify_names.py's convention for a
    word that is not an identifier (a profiler zone, a task name, a data key). A figure that
    carries one of them is spending the page's own word, not naming a member (session O)."""
    words: set[str] = set()
    with open(path, encoding="utf-8") as fh:
        in_fence = False
        for line in fh:
            if FENCE.match(line):
                in_fence = not in_fence
                continue
            if not in_fence:
                words.update(ITALIC.findall(line))
    return words


def close_up_breaks(text: str) -> str:
    """Read a `<br/>` the way pass 7's F17/F18 rule writes it.

    A break is display, never a name. Written tight against *name* characters on
    both sides — `DataComponentType.<br/>codecOrThrow`,
    `PersistentEntity<br/>SectionManager` — it is *inside* a name that mermaid
    would otherwise hyphenate, so the gate closes it up. Written with a space on
    either side it separates clauses, so it becomes one space. **And written
    after punctuation** — `inBlockTickingRange,<br/>DistanceManager.…` — it
    separates two names, because no Mojang name ends in a comma: a flowchart
    node label spends `<br/>` as a line break far more often than as a repair to
    one name, and closing that up welds two names into a third that is in no
    decompile. F17 ruled this for a lane expansion; F18 sends part sessions to
    break names in messages and notes the same way, so the same reading applies
    wherever a name can appear.

    Two more shapes are word breaks and not name breaks, because F17 writes a
    name break **at a CamelCase boundary or at a dot** and nowhere else
    (session I):

    * a break followed by a **lower-case** letter --
      `ensureRunningOnSameThread<br/>queues the pair` -- is the end of a name
      and the start of the next word; closing it up made
      `ensureRunningOnSameThreadqueues`, a member of nothing, and failed a page
      whose figure was right;
    * a break whose word *before* it is all lower-case --
      `a tick, then<br/>MinecraftServer.tickChildren` -- is English meeting a
      name; closing it up buries the name inside `thenMinecraftServer`, an
      unknown class the gate then skips in silence.
    """
    text = re.sub(r"(?<=\.)<br\s*/?>(?=[0-9A-Za-z_$])", "", text)

    def camel(m):
        # the word being cut: all lower-case means English meeting a name, not one name
        return " " if re.search(r"(?:^|[^0-9A-Za-z_$.])[a-z]+$", text[:m.start()]) else ""

    text = re.sub(r"(?<=[0-9A-Za-z_$])<br\s*/?>(?=[A-Z_$])", camel, text)
    return re.sub(r"<br\s*/?>", " ", text)


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
        self.one_word_keys = sorted(c for c in key_classes
                                    if re.fullmatch(r"[A-Z][a-z]+", c) and c in self.classes and len(c) >= 5)

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
                # the whole file, not a window: `ClientPacketListener`'s own declaration sits at
                # byte 21,133, behind three hundred import lines, and a window that misses the
                # declaration reports the class as extending nothing, so every inherited member
                # on that lane fails (session I)
                with open(p, encoding="utf-8", errors="replace") as fh:
                    text = fh.read()
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

    def ancestry(self, cls: str, depth: int = 0, seen: set | None = None) -> set[str]:
        """`cls` and every class it extends or implements, as far as the decompile has them."""
        seen = seen if seen is not None else set()
        if cls in seen or depth > 10:
            return seen
        seen.add(cls)
        for s in self.supers(cls):
            self.ancestry(s, depth + 1, seen)
        return seen

    def near_miss(self, word: str) -> str | None:
        """A one-word class in the lane key that `word` misspells by one letter, or None.

        The identifier token needs two humps, so a one-word class (`Entity`, `Player`) in free
        text is unchecked: it cannot be told from English. What can be told is a word one edit
        away from such a class that is not itself a class -- `Entty`, `Palyer` (session O)."""
        if len(word) < 5 or self.class_ok(word):
            return None
        for k in self.one_word_keys:
            if abs(len(k) - len(word)) > 1 or k == word:
                continue
            if _one_edit(k, word):
                return k
        return None

    def check_page(self, path: str, rel: str):
        failures, notes = [], []
        italics = italic_words(path)
        for start, body in fences_of(path):
            kind, lanes, labels = labels_of(body)
            for ln, role, text, target in labels:
                text = close_up_breaks(text)
                if role == "classname":
                    # A `class Foo` box and both ends of a relation are structurally class names,
                    # not free text, so they are checked whole the way a lane expansion is —
                    # CAMEL needs two humps and would never see `Avatar`, `Player` or `Entity`.
                    self.checked += 1
                    outer, _, inner = text.partition(".")
                    ok = (self.class_ok(text) if not inner
                          else outer in self.classes and outer in self.nested_outer(inner.split(".")[-1]))
                    if not ok:
                        failures.append((rel, ln, text, "no such class for the class box"))
                    elif outer in self.classes:
                        self.mentions.setdefault(outer, set()).add(rel)
                    continue
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
                            failures.append((rel, ln, tok, f"a nested class named without its outer class: {', '.join(o + '.' + tok for o in outers[:3])}"))
                            self.mentions.setdefault(outers[0], set()).add(rel) if len(outers) == 1 else None
                        else:
                            failures.append((rel, ln, tok, "no such class"))
                for m in re.finditer(r"\b([A-Z][a-z]{4,})\b", stripped):
                    k = self.near_miss(m.group(1))
                    if k:
                        failures.append((rel, ln, m.group(1), f"one letter from the class {k}"))
                # a qualified head names a member of some class; that class should be the lane's
                # own or kin to it -- otherwise it is a third class's method on a lane that owns
                # neither (F12, amended by session J): a note, ruled case by case
                if role == "message" and target and target in lanes:
                    hq = re.match(r"^\s*([A-Z][A-Za-z0-9]*)\.([a-z_][A-Za-z0-9_]*)", text)
                    lane_cls = lanes[target].split(".")[0]
                    if hq and lane_cls in self.classes and hq.group(1) in self.classes and hq.group(1) != lane_cls \
                            and hq.group(1) not in self.ancestry(lane_cls) and lane_cls not in self.ancestry(hq.group(1)):
                        notes.append((rel, ln, f"{hq.group(1)}.{hq.group(2)}",
                                      f"a qualified head on a {lane_cls} lane naming a class that is neither it nor its kin"))
                # a message's head names a member of the lane it is sent to
                if role == "message" and target:
                    hm = MSG_HEAD.match(stripped)
                    head = hm.group(1) if hm else None
                    if head and head in italics:
                        pass                    # the page's own italic word: a zone, a task, a key
                    elif head and target in lanes and lanes[target] not in self.key_words and not lanes[target].startswith("*"):
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
                elif role == "member" and target and MEMBER_LINE.search(stripped):
                    # `int popTime` inside `class ItemStack {` names ItemStack.popTime, so the box
                    # qualifies it the way a lane qualifies a message. Only a line whose last token
                    # is humped or parenthesised is read as a declaration: the corpus also writes
                    # member lines as English ("the product of every property's value count"), and
                    # those are node labels, checked below like any other.
                    name = MEMBER_LINE.search(stripped).group(1)
                    box = target.split(".")[0]      # a nested box is read through its outer class, as a dotted name is
                    if box in self.classes:
                        self.checked += 1
                        if not (name in self.members(box) or name in ALLOW or self.inherited_member(box, name)):
                            failures.append((rel, ln, name, f"no member {name} on {target} (the class box it is in)"))
                    else:
                        self.skipped += 1
                elif role in ("node", "edge", "subgraph", "state", "note", "block", "member"):
                    # F12(b): a member outside a message is written `Class.member`, because nothing
                    # else qualifies it -- except in a classDiagram, where a member line's box and a
                    # relation label's two boxes do. A failure from session O; a note before it.
                    boxes = [b.split(".")[0] for b in (target or "").split("|") if b] if kind == "classDiagram" else []
                    toks = [m.group(1) for m in LOWER_CAMEL.finditer(stripped)]
                    toks += [m.group(1) for m in CALL.finditer(stripped) if m.group(1) not in toks]
                    for tok in toks:
                        if tok in ALLOW or tok in ENGLISH_HEADS or tok in italics:
                            continue
                        if any(b in self.classes and (tok in self.members(b) or self.inherited_member(b, tok)) for b in boxes):
                            self.checked += 1
                            continue
                        where = f"a {kind.split('-')[0]} {role} label"
                        if boxes:
                            failures.append((rel, ln, tok, f"no member {tok} on {' or '.join(boxes)} (the boxes that qualify {where})"))
                        else:
                            failures.append((rel, ln, tok, f"unqualified member in {where}: write it Class.{tok}"))
        return failures, notes


def _one_edit(a: str, b: str) -> bool:
    """True when b is a one-letter substitution, insertion, deletion or adjacent swap of a."""
    if len(a) == len(b):
        diff = [i for i in range(len(a)) if a[i] != b[i]]
        return len(diff) == 1 or (len(diff) == 2 and diff[1] == diff[0] + 1
                                  and a[diff[0]] == b[diff[1]] and a[diff[1]] == b[diff[0]])
    if len(a) > len(b):
        a, b = b, a
    return any(b[:i] + b[i + 1:] == a for i in range(len(b)))


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
    participant PESM as PersistentEntity<br/>SectionManager
    participant QQ as PersistentEntity<br/>SectionManagerr
    SL->>MS: tickServer
    SL->>MS: noSuchMethodHere(arg)
    SL->>MS: the factory it was handed runs here
    Main->>SL: load, wrapped in Util.blockUntilDone
    Note over SL,MS: ChunkMap and ChunkMapp and MinecraftServer.tickServer and ServerLevel.noSuchMemberEither
    SL->>MS: a tick, then<br/>MinecraftServer.tickChildren
    SL->>MS: MinecraftServer.<br/>tickServer once more
    SL->>MS: MinecraftServer.<br/>tickServerr once more
    rect rgba(0, 0, 0, 0.04)
        Note over SL,MS: MinecraftServer.tickChildren
        SL->>MS: tickServer
    end
    box transparent ChunkMapp on the server
        participant CM as ChunkMap
    end
```

```mermaid
flowchart TD
    A["NaturalSpawner.createState walks every entity"] --> B{"Mob.finalizeSpawn"}
    E["DistanceManager.inBlockTickingRange,<br/>DistanceManager.inEntityTickingRange"] --> A
    F["ChunkMap.save,<br/>ChunkMapp.save"] --> A
    B -->|"two ClientboundBlockUpdatePackets"| C["runAllTasks then FrobnicatorThing then SpawnState"]
    C --> D["DedicatedServer.runServer"]
```

```mermaid
classDiagram
    class ChunkMap {
        int viewDistance
        int noSuchFieldHere
    }
    class Bad["ChunkMapp, in a display label"] {
        ChunkMapp field
    }
    class Entity
    class Avatarr
    class ChunkMap.TrackedEntity
    class ChunkMap.NoSuchNestedClass
    ChunkMap --> Bad : ChunkMap.save
    ChunkMap ..> Bad : ChunkMapp.save
    Entity <|-- Avatarr
```

```mermaid
sequenceDiagram
    participant Conn as Connection
    participant CPL as ClientPacketListener
    Conn->>CPL: shouldHandleMessage
    Conn->>CPL: shouldHandleMessage<br/>queues the pair and aborts
    Conn->>CPL: a frame, then<br/>ClientPacketListener is asked again
    Conn->>CPL: handleSetEntity<br/>PassengersPackett once more
```

```mermaid
classDiagram
    class PermissionCheck {
        boolean check(PermissionSet)
        boolean frob(PermissionSet)
    }
```

The page sets *zoneName* in italics, which declares it a word and not a member.

```mermaid
flowchart TD
    Z["the zoneName zone, then the otherZone zone"]
    N["Mob.finalizeSpawn and Entty and Palyer, beside Entity and Players"]
```

```mermaid
classDiagram
    class BlockBehaviour.Properties {
        setId first, or the constructor throws
        frobnicateThing first
    }
    class ChunkMap
    class ServerLevel
    ChunkMap --> ServerLevel : getChunkSource, then noSuchRelMember
```

```mermaid
sequenceDiagram
    participant SL as ServerLevel
    participant MS as MinecraftServer
    SL->>MS: ChunkMap.save, a third class on a lane that owns neither
    SL->>MS: MinecraftServer.tickServer, the lane's own
    SL->>SL: ServerLevel.tick, from itself
    SL->>MS: zoneName, the page's italic word
```
"""


def _probe_line(needle: str) -> int:
    return next(i for i, l in enumerate(PROBE.split("\n"), 1) if needle in l)


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
        ("a lane name broken at a CamelCase boundary is read closed up", not any(f[1] == 9 for f in failures)),
        ("a broken lane name that is still not a class fails", (10, "PersistentEntitySectionManagerr") in got),
        ("the humped message head that is not a member of the target lane fails", (12, "noSuchMethodHere") in got),
        ("the good message head (tickServer on MinecraftServer) passes", not any(f[2] == "tickServer" for f in failures)),
        ("an English message is not a failure", not any(f[1] == 13 for f in failures)),
        ("a message to a word lane is skipped", not any(f[1] == 14 for f in failures)),
        ("the bad class in a note fails and the good one passes", (15, "ChunkMapp") in got and not any(f[2] == "ChunkMap" for f in failures)),
        ("the bad dotted member fails and the good one passes", (15, "ServerLevel.noSuchMemberEither") in got and not any(f[2] == "MinecraftServer.tickServer" for f in failures)),
        ("a plural of a class name passes", not any("ClientboundBlockUpdatePackets" in f[2] for f in failures)),
        ("a break with a space before it separates clauses, and the name after it still resolves", not any(f[1] == 16 for f in failures)),
        ("a break tight inside a message's name is read closed up", not any(f[1] == 17 for f in failures)),
        ("a break tight inside a message's name that still does not resolve fails", (18, "MinecraftServer.tickServerr") in got),
        ("a bad class in a flowchart node fails", any(f[2] == "FrobnicatorThing" for f in failures)),
        ("a nested class named bare is a failure, naming its outer class (F12(c), session O)",
         any(f[2] == "SpawnState" and "NaturalSpawner.SpawnState" in f[3] for f in failures)),
        ("an inherited member resolves (DedicatedServer.runServer is MinecraftServer's)", not any(f[2] == "DedicatedServer.runServer" for f in failures)),
        ("an inherited member resolves on a class whose own declaration is past 20kB of imports (ClientPacketListener.shouldHandleMessage)",
         not any(f[2] == "shouldHandleMessage" for f in failures)),
        ("a break before a lower-case word ends the name there, and does not weld the next word onto it",
         not any(f[2].startswith("shouldHandleMessagequeues") for f in failures)),
        ("a break after an all-lower-case word does not bury the class name after it",
         not any("thenClientPacketListener" in f[2] for f in failures)),
        ("a break at a real CamelCase boundary is still closed up, and a bad name through one still fails",
         any(f[2] == "handleSetEntityPassengersPackett" for f in failures)),
        ("an unqualified member in a flowchart label is a failure (F12(b), session O)", any(f[2] == "runAllTasks" for f in failures)),
        ("a rect band's colour is not read as a call named rgba", not any(n[2] == "rgba" for n in notes)),
        ("a box's colour word is stripped and its label still checked", (23, "ChunkMapp") in got),
        ("a break after punctuation in a node label separates two names, and both resolve", not any(f[1] == 31 for f in failures)),
        ("a break after punctuation does not hide a bad name on either side", (32, "ChunkMapp.save") in got),
        ("figure mentions include ChunkMap and NaturalSpawner", "ChunkMap" in c.mentions and "NaturalSpawner" in c.mentions),
        ("a classDiagram is read at all, and its good class resolves", "ChunkMap" in c.mentions and not any(f[2] == "ChunkMap" for f in failures)),
        ("a classDiagram display label is checked like a node label", (43, "ChunkMapp") in got),
        ("a classDiagram member line's type is checked as a class", (44, "ChunkMapp") in got),
        ("a classDiagram relation label's good dotted member passes and its bad one fails", not any(f[2] == "ChunkMap.save" for f in failures) and (51, "ChunkMapp.save") in got),
        ("a classDiagram member line is checked against its own class box, not noted",
         (41, "noSuchFieldHere") in got and not any(n[2] == "viewDistance" for n in notes) and not any(f[2] == "viewDistance" for f in failures)),
        ("a one-word class box with no CamelCase hump is checked: the good one passes",
         "Entity" in c.mentions and not any(f[2] == "Entity" for f in failures)),
        ("a one-word class box with no CamelCase hump is checked: the bad one fails",
         (47, "Avatarr") in got and (52, "Avatarr") in got),
        ("a box id with a display label is an alias, not a class, at its definition and its relations",
         not any(f[2] == "Bad" for f in failures)),
        ("an inheritance relation is parsed at all, so both its ends are checked",
         any(f[1] == 52 and f[2] == "Avatarr" for f in failures)),
        ("a nested class box resolves against its outer class, and a bad one does not",
         not any(f[2] == "ChunkMap.TrackedEntity" for f in failures) and (49, "ChunkMap.NoSuchNestedClass") in got),
        ("a one-word method in a classDiagram member line is checked against its box, not noted: the good one passes",
         not any(n[2] == "check" for n in notes) and not any(f[2] == "check" for f in failures)),
        ("a one-word method in a classDiagram member line is checked against its box: the bad one fails",
         (69, "frob") in got),
        ("a word the page sets in italics is not a member, in a label or a message head",
         not any(f[2] == "zoneName" for f in failures) and not any(n[2] == "zoneName" for n in notes)),
        ("a word the page does not set in italics is still an unqualified member", any(f[2] == "otherZone" for f in failures)),
        ("a one-word class misspelt by one letter fails, and the class and its plural pass",
         {f[2] for f in failures} >= {"Entty", "Palyer"} and not any(f[2] in ("Entity", "Players") for f in failures)),
        ("a nested box qualifies its English member lines through its outer class",
         not any(f[2] == "setId" for f in failures) and any(f[2] == "frobnicateThing" for f in failures)),
        ("a relation label is qualified by either of its two boxes",
         not any(f[2] == "getChunkSource" for f in failures) and any(f[2] == "noSuchRelMember" for f in failures)),
        ("a qualified head naming a third class on a lane that owns neither is a note, and the lane's own is not",
         any(n[1] == _probe_line("a third class on a lane") and n[2] == "ChunkMap.save" for n in notes)
         and not any(n[2] in ("MinecraftServer.tickServer", "ServerLevel.tick") for n in notes)),
        ("exactly the twenty-five failures expected", len(failures) == 25),
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
