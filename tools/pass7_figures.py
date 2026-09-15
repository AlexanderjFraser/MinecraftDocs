#!/usr/bin/env python3
"""Every figure measured for pass 7: its place on the page, its source, and — with render/index.json — how it renders.

Pass 7's charter (`docs/plan.md`, *Pass 7 — the figures*) is about the picture: is it the true
shape, is it legible at the column width, does the section under it need it, and does it show
what the section needs shown. Nothing before this pass ever looked at a figure rendered, and
nothing measured one against its section. This does both, per figure, the same way every time,
so a session starts from numbers rather than from memory. Nothing here is a gate and nothing
here judges a picture — a count in a queue is a description, not a target.

Per figure (a ```mermaid block, or a `<figure class="map">` with an SVG include, on any page
under src/ that is not generated):

  place     the page, the fence line, the H2 and H3 it sits under, whether it is the page's lead
            figure, whether it *opens* its section (nothing but the heading above it), the
            lead-in (the last sentence of the paragraph above it, when that is prose), the
            caption (an italic-only paragraph immediately after it), whether any sentence in its
            section points at it (*figure*, *diagram*, *the bar*, *read it as*, *above*…), and
            whether it sits before the cast table
  source    the diagram type and direction; lanes and their expansions; messages, notes, tick
            bars and blocks; nodes, edges, subgraphs and edge labels; the longest label in
            words; labels that are sentences (over twelve words, or a full stop inside);
            bare-number gates (a label that is only a number, or *flags N*); colour in the page
            (`classDef`, `style`, `linkStyle`, `%%{init}`); `<br/>` line breaks
  names     every identifier-shaped token in its labels — a CamelCase class, a dotted member, a
            call — and, for each, whether the page's prose says it *before* the figure, only
            *after* it, or *never*. The share first met in the figure is the measurable form of
            "a lead figure the page cannot yet be read against" (pass 6, sessions C, D and F);
            a name the prose never says is a figure carrying a fact alone
  render    from `render/index.json` when `tools/render_figures.js` has run: natural and
            displayed size, the scale mermaid shrank it by, the smallest and median type on
            screen, labels under 9px and 11px, overlapping labels, labels over shapes, labels
            outside their box, edges through nodes, crossings, clipping, height on screen

Per page: the figures in order, and the sections over forty lines with no figure whose prose
is an order, a branch, a cycle or a containment — candidates for a figure (`--candidates`).
Per part and corpus: the tables. `--rank` orders every figure by a trouble score that adds one
point per thing a session would have to look at; it is a reading order, not a verdict.

Usage:
    python tools/pass7_figures.py --summary                 # the corpus by part: types, size, flags
    python tools/pass7_figures.py --part world              # every figure of a part, one row each
    python tools/pass7_figures.py world/lighting            # one page's figures in full (markdown)
    python tools/pass7_figures.py --rank [--top 40]         # figures by trouble, worst first
    python tools/pass7_figures.py --candidates              # long sections with no figure
    python tools/pass7_figures.py --json [--out FILE]       # everything, for pass7_prompts.py
    python tools/pass7_figures.py --probe                   # prove the measurements on a synthetic page
Set --render PATH to read another index (default render/index.json; absent is fine).
"""
from __future__ import annotations

import argparse
import collections
import json
import os
import re
import statistics
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import diagram_arrows as da  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "src")
RENDER_INDEX = os.path.join(ROOT, "render", "index.json")

PART_NUM = {"anatomy": "I", "foundations": "II", "server": "III", "world": "IV", "blocks": "V", "entities": "VI",
            "items": "VII", "player": "VIII", "networking": "IX", "client": "X", "rendering": "XI", "worldgen": "XII",
            "commands": "XIII"}
PART_ORDER = list(PART_NUM) + ["reference", "frame"]

FENCE = re.compile(r"^\s*(`{3,}|~{3,})\s*(\w*)\s*$")
HEADING = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
MAP_FIGURE = re.compile(r'<figure class="map">')
SVG_INCLUDE = re.compile(r"\{\{#include\s+([^}]+?\.svg)\s*\}\}")
ITALIC_PARA = re.compile(r"^\*(?!\*)(.+)\*\s*$", re.S)
TABLE_ROW = re.compile(r"^\s*\|")
POINTER = re.compile(r"\b(figure|diagram|picture|the bar|the bars|the note|the arrow|the arrows|the lanes?|the boxes|the box|"
                     r"read it as|read the|the loop|the columns?|above|below|drawn|draws|the dotted|the dashed|the diamond|the subgraph)\b", re.I)
SEQ_MSG = da.SEQ_MSG
SEQ_NOTE = re.compile(r"^\s*[Nn]ote\s+(over|left of|right of)\s+([^:]+):\s*(.*)$")
SEQ_BLOCK = re.compile(r"^\s*(rect|loop|alt|else|opt|par|and|critical|option|break|box)\b\s*(.*)$")
PARTICIPANT = da.PARTICIPANT
TICK_BAR = re.compile(r"\b(tick|frame|later|next|same tick|a tick|the tick|ticks)\b", re.I)
SUBGRAPH = re.compile(r"^\s*subgraph\s+(?:([A-Za-z0-9_]+)\s*)?(?:\[\s*\"?(.*?)\"?\s*\])?\s*(.*)$")
STATE_TRANS = re.compile(r"^\s*(\[\*\]|[\w.\-\"]+)\s*-->\s*(\[\*\]|[\w.\-\"]+)\s*(?::\s*(.*))?$")
STATE_DEF = re.compile(r"^\s*state\s+\"([^\"]+)\"\s+as\s+(\w+)")
DIRECTION = re.compile(r"^\s*(?:flowchart|graph)\s+(TD|TB|LR|RL|BT)\b")
# a `rect` band carries a colour and no label (`rect rgba(0, 0, 0, 0.04)`, F8's tick band), and a
# `box` may carry one before its label; read as a label the colour becomes a call named `rgba`
SEQ_COLOUR = re.compile(r"^\s*(?:transparent|(?:rgba?|hsla?)\s*\([^)]*\)|#[0-9A-Fa-f]{3,8})\s*")
# classDiagram (pass 7, session G): the kind F10 sends a vocabulary page to. Without these it
# fell through to the catch-all, so `classDiagram` itself was counted as a name and every
# `class Foo` line was swallowed by COLOUR_LINE.
CLASS_DEF = re.compile(r'^\s*class\s+([A-Za-z_][A-Za-z0-9_]*)\s*(?:\[\s*"(.*?)"\s*\])?\s*\{?\s*$')
CLASS_REL = re.compile(r'^\s*([A-Za-z_]\w*)\s*(?:"[^"]*"\s*)?([<>ox|*]?(?:--|\.\.)[<>ox|*]?)\s*(?:"[^"]*"\s*)?([A-Za-z_]\w*)\s*(?::\s*(.*))?$')
CLASS_NOTE = re.compile(r'^\s*note(?:\s+for\s+[A-Za-z_]\w*)?\s+"(.*)"\s*$')
CLASS_ANNOT = re.compile(r"^\s*<<.*>>\s*$")
COLOUR_LINE = re.compile(r"^\s*(classDef|style|linkStyle)\b")
INIT = re.compile(r"%%\{\s*init")
NUMBER_GATE = re.compile(r"^\s*(?:flags?\s+)?\d+\s*$|\bflags?\s+\d+\b", re.I)   # a bare number, or a label that spends a flag number

# identifier-shaped tokens inside a label
DOTTED = re.compile(r"(?<![\w/`])([A-Z][A-Za-z0-9]*(?:\.[A-Za-z_][A-Za-z0-9_]*)+)(?![\w/])")
CAMEL = re.compile(r"\b(?=[A-Z][A-Za-z0-9]*[a-z])([A-Z][a-z0-9]*[A-Z][A-Za-z0-9]*)\b")
CALL = re.compile(r"\b([a-z][A-Za-z0-9]*)\(")
LOWER_CAMEL = re.compile(r"\b([a-z]+[A-Z][A-Za-z0-9]*)\b")
ORDER_WORDS = re.compile(r"\b(then|before|after|first|last|next|earlier|later|until|once|precedes|follows)\b", re.I)
BRANCH_WORDS = re.compile(r"\b(if|unless|otherwise|either|whether|else|depending|refuses?|rejects?|falls? through|skips?)\b", re.I)
CYCLE_WORDS = re.compile(r"\b(again|loops?|every tick|each tick|every frame|each frame|repeats?|per tick|per frame|cycle)\b", re.I)
CONTAIN_WORDS = re.compile(r"\b(contains?|inside|owns?|holds?|wraps?|nested|parent|child|children|tree|hierarchy)\b", re.I)


# --- pages ------------------------------------------------------------------------------------

def is_generated(path: str) -> bool:
    try:
        with open(path, encoding="utf-8") as fh:
            return "Do not edit by hand" in fh.read(400)
    except OSError:
        return False


def all_pages(src: str = SRC) -> list[tuple[str, str, str]]:
    """(key, part, rel) for every hand-kept page: key like world/lighting or reference/glossary or introduction."""
    out = []
    for dirpath, _d, files in os.walk(src):
        for f in sorted(files):
            if not f.endswith(".md"):
                continue
            path = os.path.join(dirpath, f)
            rel = os.path.relpath(path, src).replace(os.sep, "/")
            if rel.startswith("generated/") or rel == "SUMMARY.md":
                continue
            if rel.startswith("reference/") and is_generated(path):
                continue
            if rel.startswith("systems/"):
                part = rel.split("/")[1]
                key = rel[len("systems/"):-3]
            elif rel.startswith("reference/"):
                part, key = "reference", rel[:-3]
            else:
                part, key = "frame", rel[:-3]
            out.append((key, part, rel))
    return sorted(out, key=lambda t: (PART_ORDER.index(t[1]) if t[1] in PART_ORDER else 99, t[2]))


# --- the page as lines with structure ---------------------------------------------------------

def sentences(text: str) -> list[str]:
    text = re.sub(r"\s+", " ", text.strip())
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Z\"'(*`])", text)
    return [p for p in parts if p]


def parse_page(path: str):
    """Returns lines, fences [{line, end, body}], map figures [{line, end, svg}], headings [(line, level, text)],
    prose line index (line -> True when outside fences/tables/html), cast line."""
    with open(path, encoding="utf-8") as fh:
        lines = fh.read().split("\n")
    fences, maps, headings = [], [], []
    prose = {}
    in_fence, fence_kind, start, body = False, "", 0, []
    in_html = False
    cast_line = None
    i = 0
    while i < len(lines):
        l = lines[i]
        m = FENCE.match(l)
        if in_fence:
            if m and not m.group(2):
                if fence_kind == "mermaid":
                    fences.append({"line": start, "end": i + 1, "body": body})
                in_fence = False
            else:
                body.append((i + 1, l))
            i += 1
            continue
        if m and m.group(2) == "mermaid":
            in_fence, fence_kind, start, body = True, "mermaid", i + 1, []
            i += 1
            continue
        if m and m.group(2):
            in_fence, fence_kind, start, body = True, m.group(2), i + 1, []
            i += 1
            continue
        if MAP_FIGURE.search(l):
            j = i
            svg = None
            while j < len(lines) and "</figure>" not in lines[j]:
                sm = SVG_INCLUDE.search(lines[j])
                if sm:
                    svg = sm.group(1)
                j += 1
            maps.append({"line": i + 1, "end": j + 1, "svg": svg})
            i = j + 1
            continue
        h = HEADING.match(l)
        if h:
            headings.append((i + 1, len(h.group(1)), h.group(2)))
            i += 1
            continue
        if TABLE_ROW.match(l):
            if cast_line is None and re.search(r"\|\s*class\s*\|", l, re.I):
                cast_line = i + 1
            i += 1
            continue
        if l.strip().startswith("<"):
            in_html = True
        if in_html and l.strip() == "":
            in_html = False
        if not in_html and l.strip():
            prose[i + 1] = True
        i += 1
    return lines, fences, maps, headings, prose, cast_line


def section_of(headings, line):
    h2 = h3 = None
    for ln, level, text in headings:
        if ln > line:
            break
        if level <= 2:
            h2, h3 = (ln, text), None
        elif level == 3:
            h3 = (ln, text)
    return h2, h3


def section_range(headings, line, lines_total):
    """The lines of the innermost section a figure sits in (its H2 or H3 to the next heading of the same or higher level)."""
    cur = None
    for ln, level, text in headings:
        if ln > line:
            break
        if level <= 3:
            cur = (ln, level)
    if cur is None:
        return 1, lines_total
    start, level = cur
    end = lines_total
    for ln, lv, _t in headings:
        if ln > start and lv <= level:
            end = ln - 1
            break
    return start, end


def paragraph_above(lines, line):
    """The non-empty lines directly above `line` (1-based), as (kind, text)."""
    k = line - 2
    while k >= 0 and not lines[k].strip():
        k -= 1
    if k < 0:
        return "top", ""
    l = lines[k]
    if HEADING.match(l):
        return "heading", HEADING.match(l).group(2)
    if TABLE_ROW.match(l):
        return "table", ""
    if l.strip().startswith(("-", "*", "1.", "2.", "3.")) and not ITALIC_PARA.match(l.strip()):
        return "list", l.strip()
    if l.strip().startswith(("```", "</figure>", "<")):
        return "block", ""
    para = []
    while k >= 0 and lines[k].strip() and not HEADING.match(lines[k]):
        para.insert(0, lines[k])
        k -= 1
    return "prose", " ".join(p.strip() for p in para)


def paragraph_below(lines, end):
    """The first non-empty paragraph after line `end` (1-based, the closing fence)."""
    k = end
    while k < len(lines) and not lines[k].strip():
        k += 1
    if k >= len(lines):
        return "end", ""
    if HEADING.match(lines[k]):
        return "heading", HEADING.match(lines[k]).group(2)
    para = []
    while k < len(lines) and lines[k].strip() and not HEADING.match(lines[k]):
        para.append(lines[k].strip())
        k += 1
    text = " ".join(para)
    if ITALIC_PARA.match(text) and not text.startswith("**"):
        return "caption", ITALIC_PARA.match(text).group(1).strip()
    return "prose", text


# --- the source -------------------------------------------------------------------------------

def labels_of(kind: str, body) -> dict:
    """Parses a block into its labels and counts. Every label is (line, role, text)."""
    labels: list[tuple[int, str, str]] = []
    info = {"lanes": [], "messages": 0, "notes": 0, "tick_bars": 0, "blocks": 0, "nodes": 0, "edges": 0,
            "subgraphs": 0, "edge_labels": 0, "transitions": 0, "states": 0, "direction": None,
            "colour_lines": 0, "init": False, "br": 0, "self_messages": 0}
    first = next((raw.strip() for _ln, raw in body if raw.strip() and not raw.strip().startswith("%%")), "")
    d = DIRECTION.match(first)
    if d:
        info["direction"] = d.group(1)
    for ln, raw in body:
        t = raw.strip()
        if INIT.search(t):
            info["init"] = True
        info["br"] += len(re.findall(r"<br\s*/?>", t, re.I))
        if not t or t.startswith("%%"):
            continue
        if COLOUR_LINE.match(t) and kind != "classDiagram":
            info["colour_lines"] += 1
            continue
        if kind == "sequenceDiagram":
            m = PARTICIPANT.match(t)
            if m:
                info["lanes"].append((m.group(1), (m.group(2) or m.group(1)).strip()))
                labels.append((ln, "participant", (m.group(2) or m.group(1)).strip()))
                continue
            m = SEQ_MSG.match(t)
            if m:
                info["messages"] += 1
                if m.group(1) == m.group(3):
                    info["self_messages"] += 1
                labels.append((ln, "message", m.group(4).strip()))
                continue
            m = SEQ_NOTE.match(t)
            if m:
                info["notes"] += 1
                if TICK_BAR.search(m.group(3)):
                    info["tick_bars"] += 1
                labels.append((ln, "note", m.group(3).strip()))
                continue
            m = SEQ_BLOCK.match(t)
            if m:
                info["blocks"] += 1
                rest = SEQ_COLOUR.sub("", (m.group(2) or ""), count=1).strip()
                if rest:
                    labels.append((ln, "block", rest))
                continue
        elif kind in ("flowchart", "graph"):
            m = SUBGRAPH.match(t)
            if m:
                info["subgraphs"] += 1
                title = m.group(2) or m.group(3) or m.group(1) or ""
                labels.append((ln, "subgraph", title.strip().strip('"')))
                continue
            if t == "end":
                continue
            for m in da.NODE_DEF.finditer(t):
                info["nodes"] += 1
                labels.append((ln, "node", da.strip_label(m.group(2))))
            parts = da.FLOW_EDGE.split(t)
            for k in range(1, len(parts) - 1, 2):
                op = parts[k]
                lab = da.label_of(op).strip().strip('"').strip()
                srcs = [s.strip() for s in parts[k - 1].split("&") if s.strip()]
                dsts = [s.strip() for s in parts[k + 1].split("&") if s.strip()]
                info["edges"] += max(1, len(srcs)) * max(1, len(dsts))
                if lab:
                    info["edge_labels"] += 1
                    labels.append((ln, "edge", lab))
        elif kind.startswith("stateDiagram"):
            m = STATE_DEF.match(t)
            if m:
                info["states"] += 1
                labels.append((ln, "state", m.group(1)))
                continue
            m = STATE_TRANS.match(t)
            if m:
                info["transitions"] += 1
                if m.group(3):
                    labels.append((ln, "edge", m.group(3).strip()))
                continue
            m = re.match(r"^note\s+(?:left of|right of)\s+[\w.\-]+\s*:\s*(.*)$", t)
            if m:
                info["notes"] += 1
                labels.append((ln, "note", m.group(1)))
        elif kind == "classDiagram":
            if t in ("{", "}") or t == "classDiagram" or CLASS_ANNOT.match(t) or t.startswith("direction "):
                continue
            m = CLASS_NOTE.match(t)
            if m:
                info["notes"] += 1
                labels.append((ln, "note", m.group(1)))
                continue
            m = CLASS_DEF.match(t)
            if m:
                info["nodes"] += 1
                labels.append((ln, "node", m.group(2) or m.group(1)))
                continue
            m = CLASS_REL.match(t)
            if m:
                info["edges"] += 1
                if m.group(4):
                    info["edge_labels"] += 1
                    labels.append((ln, "edge", m.group(4).strip()))
                continue
            labels.append((ln, "node", t.lstrip("+-#~")))
        else:
            labels.append((ln, "line", t))
    # nodes are defined once but NODE_DEF sees each definition; count ids instead
    if kind in ("flowchart", "graph"):
        ids = set()
        for _ln, raw in body:
            for m in da.NODE_DEF.finditer(raw):
                ids.add(m.group(1))
        info["nodes"] = len(ids)
    info["labels"] = labels
    return info


def tokens_of(text: str, role: str = "") -> set[str]:
    """Identifier-shaped tokens in a label.

    A lane's line break is inside the name, not between two of them (TEMPLATE.md, *Lanes*),
    so a participant expansion closes up: `PersistentEntity<br/>SectionManager` is one token."""
    out = set()
    text = re.sub(r"<br\s*/?>", "" if role == "participant" else " ", text)
    for m in DOTTED.finditer(text):
        out.add(m.group(1))
    stripped = DOTTED.sub(" ", text)
    for m in CAMEL.finditer(stripped):
        out.add(m.group(1))
    for m in CALL.finditer(stripped):
        out.add(m.group(1))
    for m in LOWER_CAMEL.finditer(stripped):
        out.add(m.group(1))
    return out


def word_count(text: str) -> int:
    return len(re.sub(r"<br\s*/?>", " ", text).split())


def is_sentence(text: str) -> bool:
    t = re.sub(r"<br\s*/?>", " ", text).strip()
    return word_count(t) > 12 or bool(re.search(r"[a-z]\.\s+[A-Z]", t))


# --- the render -------------------------------------------------------------------------------

def load_render(path: str) -> dict:
    if not path or not os.path.exists(path):
        return {}
    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)
    by = {}
    for r in data.get("records", []):
        if r.get("kind") == "mermaid" and r.get("fence_line"):
            by[("mermaid", r["page"], r["fence_line"])] = r
        elif r.get("kind") == "map":
            by[("map", r["page"], r["n"])] = r
    by["_meta"] = {k: v for k, v in data.items() if k != "records"}
    return by


def render_summary(rec: dict | None) -> dict | None:
    if not rec:
        return None
    if rec.get("error"):
        return {"error": rec["error"]}
    f = rec["flags"]
    return {
        "natural": rec["natural"], "display": rec["display"], "scale": rec["scale"],
        "font_min": rec["fonts"]["min"], "font_median": rec["fonts"]["median"],
        "under9": rec["fonts"]["under9"], "under11": rec["fonts"]["under11"], "labels": rec["fonts"]["labels"],
        "overlaps": len(f["textOverlaps"]), "over_shape": len(f["textOverShape"]),
        "outside": len(f["textOutsideContainer"]), "through": len(f["edgeThroughNode"]),
        "crossings": f["crossings"], "clipped": len(f["clipped"]), "lifelines": f["lifelinesThroughText"],
        "png": rec.get("png"), "examples": {
            "overlaps": f["textOverlaps"][:3], "over_shape": f["textOverShape"][:3],
            "outside": f["textOutsideContainer"][:3], "through": f["edgeThroughNode"][:3], "clipped": f["clipped"][:3]},
    }


# --- one page ---------------------------------------------------------------------------------

def figures_of(key: str, part: str, rel: str, render: dict) -> dict:
    path = os.path.join(SRC, rel)
    lines, fences, maps, headings, prose, cast_line = parse_page(path)
    # prose text per line, outside fences/tables, for the "said before the figure" question
    prose_lines = {ln: lines[ln - 1] for ln in prose}
    first_mention: dict[str, int] = {}

    def first_line_of(token: str) -> int | None:
        if token in first_mention:
            return first_mention[token]
        # `Level.setBlock` in the prose is a mention of the figure's `setBlock`, so a preceding dot is allowed;
        # and prose saying `checkSpawnRules` unqualified is a mention of the figure's `Mob.checkSpawnRules`
        forms = [token]
        if "." in token:
            forms.append(token.rsplit(".", 1)[1])
        pats = [re.compile(r"(?<![\w])" + re.escape(f) + r"(?![\w])") for f in forms]
        hit = None
        for ln in sorted(prose_lines):
            if any(p.search(prose_lines[ln]) for p in pats):
                hit = ln
                break
        first_mention[token] = hit
        return hit

    figs = []
    order = 0
    entries = [("mermaid", f) for f in fences] + [("map", m) for m in maps]
    entries.sort(key=lambda e: e[1]["line"])
    map_n = 0
    for kind, f in entries:
        order += 1
        h2, h3 = section_of(headings, f["line"])
        s_start, s_end = section_range(headings, f["line"], len(lines))
        above_kind, above = paragraph_above(lines, f["line"])
        below_kind, below = paragraph_below(lines, f["end"])
        sec_text = " ".join(lines[ln - 1] for ln in range(s_start, s_end + 1) if ln in prose and not (f["line"] <= ln <= f["end"]))
        pointers = len(POINTER.findall(sec_text))
        fig = {
            "page": key, "part": part, "rel": rel, "n": order, "kind": kind, "line": f["line"], "end": f["end"],
            "h2": h2[1] if h2 else None, "h3": h3[1] if h3 else None,
            "lead": order == 1, "opens_section": above_kind == "heading",
            "lead_in": sentences(above)[-1] if above_kind == "prose" and above else None,
            "above": above_kind, "caption": below if below_kind == "caption" else None, "below": below_kind,
            "pointers": pointers, "before_cast": bool(cast_line and f["line"] < cast_line),
            "section_lines": s_end - s_start + 1,
        }
        if kind == "mermaid":
            body = f["body"]
            first = next((raw.strip() for _ln, raw in body if raw.strip() and not raw.strip().startswith("%%")), "")
            dtype = first.split()[0] if first else "?"
            info = labels_of(dtype, body)
            labels = info.pop("labels")
            fig["type"] = dtype
            fig["source_lines"] = len(body)
            fig.update({k: v for k, v in info.items() if k != "lanes"})
            fig["lanes"] = info["lanes"]
            fig["lane_count"] = len(info["lanes"])
            words = [word_count(t) for _l, r, t in labels if r != "participant"]
            fig["longest_label_words"] = max(words) if words else 0
            fig["sentence_labels"] = [t for _l, r, t in labels if r != "participant" and is_sentence(t)]
            fig["number_gates"] = [t for _l, r, t in labels if r in ("edge", "node") and NUMBER_GATE.search(t)]
            fig["label_count"] = len(labels)
            toks: set[str] = set()
            for _l, r, t in labels:
                toks |= tokens_of(t, r)
            before, after, never = [], [], []
            for tok in sorted(toks):
                ln = first_line_of(tok)
                (before if ln is not None and ln < f["line"] else after if ln is not None else never).append(tok)
            fig["names"] = {"count": len(toks), "before": before, "after": after, "never": never}
            n = len(toks)
            fig["names_first_here"] = round((len(after) + len(never)) / n, 2) if n else 0.0
            fig["render"] = render_summary(render.get(("mermaid", "src/" + rel, f["line"])))
        else:
            map_n += 1
            fig["type"] = "map"
            fig["svg"] = f.get("svg")
            fig["render"] = render_summary(render.get(("map", "src/" + rel, map_n)))
        figs.append(fig)

    # sections over forty lines with no figure, and what their prose is made of
    candidates = []
    for idx, (ln, level, text) in enumerate(headings):
        if level > 3 or level == 1:     # the H1 is the page; a page-long "section" with no H2 is a Reference table or the glossary
            continue
        end = len(lines)
        for ln2, lv2, _t in headings[idx + 1:]:
            if lv2 <= level:
                end = ln2 - 1
                break
        length = end - ln + 1
        if length <= 40:
            continue
        if any(fg["line"] >= ln and fg["line"] <= end for fg in figs):
            continue
        has_h3 = level == 2 and any(l2 == 3 and ln < ln2 <= end for ln2, l2, _t in headings)
        txt = " ".join(lines[k - 1] for k in range(ln, end + 1) if k in prose)
        counts = {"order": len(ORDER_WORDS.findall(txt)), "branch": len(BRANCH_WORDS.findall(txt)),
                  "cycle": len(CYCLE_WORDS.findall(txt)), "contain": len(CONTAIN_WORDS.findall(txt))}
        candidates.append({"page": key, "part": part, "heading": text, "level": level, "line": ln, "lines": length,
                           "has_h3": has_h3, **counts, "signal": sum(counts.values()),
                           "density": round(sum(counts.values()) * 100 / length, 1)})
    return {"page": key, "part": part, "rel": rel, "lines": len(lines), "figures": figs, "candidates": candidates,
            "cast_line": cast_line}


# --- scoring and reports ----------------------------------------------------------------------

def trouble(fig: dict) -> tuple[int, list[str]]:
    why = []
    r = fig.get("render")
    if r and not r.get("error"):
        if r["scale"] < 0.5:
            why.append(f"shrunk to {r['scale']:.2f}")
        elif r["scale"] < 0.75:
            why.append(f"shrunk to {r['scale']:.2f}")
        if r["font_min"] is not None and r["font_min"] < 9:
            why.append(f"type {r['font_min']}px")
        elif r["font_min"] is not None and r["font_min"] < 11:
            why.append(f"type {r['font_min']}px")
        if r["overlaps"]:
            why.append(f"{r['overlaps']} label overlaps")
        if r["over_shape"]:
            why.append(f"{r['over_shape']} labels over a shape")
        if r["outside"]:
            why.append(f"{r['outside']} labels outside their box")
        if r["through"]:
            why.append(f"{r['through']} edges through a node")
        if r["crossings"] >= 3:
            why.append(f"{r['crossings']} crossings")
        if r["clipped"]:
            why.append("clipped")
        if r["display"]["h"] > 1200:
            why.append(f"{r['display']['h']}px tall")
    elif r and r.get("error"):
        why.append("render error")
    if fig["kind"] == "mermaid":
        if fig["lane_count"] > 7:
            why.append(f"{fig['lane_count']} lanes")
        if fig.get("nodes", 0) > 15:
            why.append(f"{fig['nodes']} nodes")
        if fig.get("edges", 0) > 20:
            why.append(f"{fig['edges']} edges")
        if len(fig["sentence_labels"]) >= 3:
            why.append(f"{len(fig['sentence_labels'])} sentence labels")
        elif fig["sentence_labels"]:
            why.append("a sentence label")
        if fig["number_gates"]:
            why.append("bare-number gates")
        if fig["names"]["count"] >= 4 and fig["names_first_here"] >= 0.5:
            why.append(f"{int(fig['names_first_here'] * 100)}% of its names first met here")
        if fig["colour_lines"] or fig["init"]:
            why.append("colour in the page")
    if fig["opens_section"]:
        why.append("opens its section")
    if not fig["lead_in"] and not fig["pointers"] and not fig["caption"]:
        why.append("nothing points at it")
    score = 0
    for w in why:
        if w.startswith("shrunk") and float(w.split()[-1]) < 0.5:
            score += 3
        elif w.startswith("type") and float(w.split()[1][:-2]) < 9:
            score += 3
        elif "first met here" in w or "lanes" in w or "nodes" in w or "edges" in w or "sentence labels" in w:
            score += 2
        elif "overlap" in w or "over a shape" in w or "outside" in w or "through" in w or "crossings" in w or "clipped" in w or "error" in w:
            score += 2
        else:
            score += 1
    return score, why


def fig_row(fig: dict) -> str:
    r = fig.get("render") or {}
    rs = "—" if not r else ("error" if r.get("error") else f"{r['scale']:.2f} / {r['font_min']}px")
    if fig["kind"] == "map":
        return (f"| {fig['page']} | m{fig['n']} | map | {fig['h2'] or '—'} | — | — | {rs} | "
                f"{'opens' if fig['opens_section'] else ''} {'cap' if fig['caption'] else ''} |")
    score, why = trouble(fig)
    return (f"| {fig['page']} | {fig['n']} | {fig['type']}{(' ' + fig['direction']) if fig.get('direction') else ''} | "
            f"{(fig['h2'] or '—')[:40]} | {fig['lane_count'] or fig.get('nodes', 0)} | {fig['messages'] or fig.get('edges', 0)} | {rs} | "
            f"{score}: {', '.join(why)} |")


def part_table(pages: list[dict], part: str) -> str:
    figs = [f for p in pages if p["part"] == part for f in p["figures"]]
    out = [f"## Part {PART_NUM.get(part, part)} · {part} — {len(figs)} figures on {sum(1 for p in pages if p['part'] == part and p['figures'])} pages", "",
           "| page | # | type | section | lanes/nodes | msgs/edges | scale / min type | trouble |", "|---|---|---|---|---:|---:|---|---|"]
    out += [fig_row(f) for f in figs]
    return "\n".join(out) + "\n"


def page_md(p: dict) -> str:
    out = [f"# Figures — `src/{p['rel']}` ({p['lines']} lines, {len(p['figures'])} figure{'s' if len(p['figures']) != 1 else ''})", ""]
    for fig in p["figures"]:
        score, why = trouble(fig)
        where = f"under *{fig['h2']}*" + (f" › *{fig['h3']}*" if fig["h3"] else "") if fig["h2"] else "before any heading"
        out.append(f"## Figure {fig['n']} — {fig['type']}{(' ' + fig['direction']) if fig.get('direction') else ''}, line {fig['line']}, {where}")
        out.append("")
        out.append(f"- **Place**: {'the lead figure' if fig['lead'] else 'a later figure'}; "
                   f"{'opens its section (a heading directly above it)' if fig['opens_section'] else 'a ' + fig['above'] + ' above it'}; "
                   f"{'before the cast table' if fig['before_cast'] else 'after the cast table' if p['cast_line'] else 'no cast table on the page'}; "
                   f"section of {fig['section_lines']} lines; {fig['pointers']} sentence{'s' if fig['pointers'] != 1 else ''} in the section point at it.")
        out.append(f"- **Lead-in**: {('“' + fig['lead_in'] + '”') if fig['lead_in'] else 'none'}")
        out.append(f"- **Caption**: {('“' + fig['caption'] + '”') if fig['caption'] else 'none — a ' + fig['below'] + ' follows it'}")
        if fig["kind"] == "mermaid":
            if fig["type"] == "sequenceDiagram":
                out.append(f"- **Source**: {fig['lane_count']} lanes ({', '.join(a + '=' + b for a, b in fig['lanes'])}); {fig['messages']} messages "
                           f"({fig['self_messages']} to self), {fig['notes']} notes of which {fig['tick_bars']} read as tick bars, {fig['blocks']} blocks; "
                           f"{fig['source_lines']} source lines.")
            elif fig["type"] in ("flowchart", "graph"):
                out.append(f"- **Source**: {fig['nodes']} nodes, {fig['edges']} edges ({fig['edge_labels']} labelled), {fig['subgraphs']} subgraphs; "
                           f"{fig['source_lines']} source lines.")
            else:
                out.append(f"- **Source**: {fig['states']} named states, {fig['transitions']} transitions, {fig['notes']} notes; {fig['source_lines']} source lines.")
            out.append(f"- **Labels**: {fig['label_count']}; the longest {fig['longest_label_words']} words; "
                       f"{len(fig['sentence_labels'])} read as sentences" + (": " + "; ".join('“' + s[:70] + '”' for s in fig['sentence_labels'][:4]) if fig["sentence_labels"] else "") + "."
                       + (f" Bare-number gates: {', '.join(fig['number_gates'])}." if fig["number_gates"] else "")
                       + (f" {fig['colour_lines']} colour lines in the page." if fig["colour_lines"] else "")
                       + (" An `%%{init}%%` directive." if fig["init"] else "")
                       + (f" {fig['br']} `<br/>`." if fig["br"] else ""))
            nm = fig["names"]
            out.append(f"- **Names**: {nm['count']} identifier-shaped tokens; {len(nm['before'])} said in prose before the figure, "
                       f"{len(nm['after'])} only after it, {len(nm['never'])} never ({int(fig['names_first_here'] * 100)}% first met here)."
                       + (f" After: {', '.join('`' + t + '`' for t in nm['after'][:12])}{'…' if len(nm['after']) > 12 else ''}." if nm["after"] else "")
                       + (f" Never: {', '.join('`' + t + '`' for t in nm['never'][:12])}{'…' if len(nm['never']) > 12 else ''}." if nm["never"] else ""))
        r = fig.get("render")
        if r and r.get("error"):
            out.append(f"- **Render**: FAILED — {r['error']}")
        elif r:
            out.append(f"- **Render**: natural {r['natural']['w']}×{r['natural']['h']}, shown {r['display']['w']}×{r['display']['h']} "
                       f"(scale {r['scale']:.2f}); type {r['font_min']}px smallest, {r['font_median']}px median, {r['under9']} labels under 9px; "
                       f"{r['overlaps']} label overlaps, {r['over_shape']} over a shape, {r['outside']} outside their box, "
                       f"{r['through']} edges through a node, {r['crossings']} crossings, {r['clipped']} clipped. PNG: `{r['png']}`.")
            ex = r["examples"]
            for k in ("overlaps", "over_shape", "outside", "through", "clipped"):
                for e in ex[k]:
                    out.append(f"  - {k}: {json.dumps(e, ensure_ascii=False)[:160]}")
        else:
            out.append("- **Render**: not rendered (run `node tools/render_figures.js`).")
        out.append(f"- **Trouble** {score}: {', '.join(why) if why else 'nothing measured'}")
        out.append("")
    if p["candidates"]:
        out.append("## Sections over forty lines with no figure")
        out.append("")
        out.append("| heading | lines | H3s | order | branch | cycle | contain |")
        out.append("|---|---:|---|---:|---:|---:|---:|")
        for c in p["candidates"]:
            out.append(f"| {'#' * c['level']} {c['heading']} (L{c['line']}) | {c['lines']} | {'yes' if c['has_h3'] else 'no'} | {c['order']} | {c['branch']} | {c['cycle']} | {c['contain']} |")
        out.append("")
    return "\n".join(out)


def summary_md(pages: list[dict], render_meta: dict | None) -> str:
    out = []
    rendered = any(f.get("render") for p in pages for f in p["figures"])
    out.append("| part | pages | figures | seq | flow | state | map | opens section | no lead-in | captioned | pointed at | lanes>7 | nodes>15 | sentence labels | number gates | ≥50% names first here | shrunk <0.75 | type <9px | overlaps/over/outside | crossings ≥3 | >1200px tall |")
    out.append("|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
    tot = collections.Counter()
    for part in PART_ORDER:
        ps = [p for p in pages if p["part"] == part]
        figs = [f for p in ps for f in p["figures"]]
        if not figs:
            continue
        c = collections.Counter()
        c["pages"] = sum(1 for p in ps if p["figures"])
        c["figs"] = len(figs)
        for f in figs:
            c["seq"] += f.get("type") == "sequenceDiagram"
            c["flow"] += f.get("type") in ("flowchart", "graph")
            c["state"] += str(f.get("type", "")).startswith("stateDiagram")
            c["map"] += f["kind"] == "map"
            c["opens"] += f["opens_section"]
            c["nolead"] += not f["lead_in"]
            c["cap"] += bool(f["caption"])
            c["pointed"] += f["pointers"] > 0
            if f["kind"] == "mermaid":
                c["lanes7"] += f["lane_count"] > 7
                c["nodes15"] += f.get("nodes", 0) > 15
                c["sent"] += bool(f["sentence_labels"])
                c["gates"] += bool(f["number_gates"])
                c["first"] += f["names"]["count"] >= 4 and f["names_first_here"] >= 0.5
            r = f.get("render")
            if r and not r.get("error"):
                c["shrunk"] += r["scale"] < 0.75
                c["small"] += (r["font_min"] or 99) < 9
                c["over"] += bool(r["overlaps"] or r["over_shape"] or r["outside"])
                c["cross"] += r["crossings"] >= 3
                c["tall"] += r["display"]["h"] > 1200
        tot.update(c)
        label = f"{PART_NUM[part]} · {part}" if part in PART_NUM else part
        out.append(f"| {label} | {c['pages']} | {c['figs']} | {c['seq']} | {c['flow']} | {c['state']} | {c['map']} | {c['opens']} | {c['nolead']} | {c['cap']} | {c['pointed']} | "
                   f"{c['lanes7']} | {c['nodes15']} | {c['sent']} | {c['gates']} | {c['first']} | "
                   + (f"{c['shrunk']} | {c['small']} | {c['over']} | {c['cross']} | {c['tall']} |" if rendered else "— | — | — | — | — |"))
    c = tot
    out.append(f"| **all** | {c['pages']} | {c['figs']} | {c['seq']} | {c['flow']} | {c['state']} | {c['map']} | {c['opens']} | {c['nolead']} | {c['cap']} | {c['pointed']} | "
               f"{c['lanes7']} | {c['nodes15']} | {c['sent']} | {c['gates']} | {c['first']} | "
               + (f"{c['shrunk']} | {c['small']} | {c['over']} | {c['cross']} | {c['tall']} |" if rendered else "— | — | — | — | — |"))
    out.append("")
    mm = [f for p in pages for f in p["figures"] if f["kind"] == "mermaid"]
    lanes = collections.Counter(f["lane_count"] for f in mm if f["type"] == "sequenceDiagram")
    out.append("Lanes per sequence diagram: " + ", ".join(f"{k}: {v}" for k, v in sorted(lanes.items())) + ".")
    nodes = [f["nodes"] for f in mm if f["type"] in ("flowchart", "graph")]
    if nodes:
        out.append(f"Flowchart nodes: median {statistics.median(nodes):.0f}, max {max(nodes)}; edges max {max(f['edges'] for f in mm if f['type'] in ('flowchart', 'graph'))}.")
    dirs = collections.Counter(f["direction"] for f in mm if f.get("direction"))
    out.append("Flowchart directions: " + ", ".join(f"{k}: {v}" for k, v in dirs.most_common()) + ".")
    tb = sum(f["tick_bars"] for f in mm if f["type"] == "sequenceDiagram")
    out.append(f"Tick bars (a note naming a tick or frame): {tb} on {sum(1 for f in mm if f.get('tick_bars'))} sequence diagrams of {sum(1 for f in mm if f['type'] == 'sequenceDiagram')}.")
    out.append(f"Figures whose caption is an italic paragraph: {sum(1 for p in pages for f in p['figures'] if f['caption'])}; whose next paragraph reads the figure (a pointer word in the section): "
               f"{sum(1 for p in pages for f in p['figures'] if f['pointers'])}.")
    per_page = collections.Counter(len(p["figures"]) for p in pages if p["figures"])
    out.append("Figures per page: " + ", ".join(f"{k}: {v} pages" for k, v in sorted(per_page.items())) + f"; pages with none: {sum(1 for p in pages if not p['figures'])}.")
    if rendered and render_meta:
        sc = sorted(f["render"]["scale"] for f in mm if f.get("render") and not f["render"].get("error"))
        fm = sorted(f["render"]["font_min"] for f in mm if f.get("render") and not f["render"].get("error") and f["render"]["font_min"])
        out.append(f"Rendered at {render_meta.get('width')}px viewport, theme {render_meta.get('theme')}: median scale {statistics.median(sc):.2f}, "
                   f"{sum(1 for s in sc if s < 1)} of {len(sc)} shrunk, {sum(1 for s in sc if s < 0.5)} below half; median smallest type {statistics.median(fm):.1f}px, "
                   f"{sum(1 for m in fm if m < 9)} figures under 9px.")
    cands = [c for p in pages for c in p["candidates"]]
    out.append(f"Sections over forty lines with no figure: {len(cands)} on {len({c['page'] for c in cands})} pages, "
               f"{sum(1 for c in cands if not c['has_h3'])} of them with no H3 either; {sum(1 for c in cands if c['density'] >= 20)} carry twenty or more "
               f"order/branch/cycle/containment words per hundred lines.")
    nv = [len(f["names"]["never"]) for f in mm]
    out.append(f"Names the page's prose never says: {sum(nv)} tokens on {sum(1 for n in nv if n)} figures ({sum(1 for n in nv if n >= 3)} figures carry three or more).")
    return "\n".join(out) + "\n"


def rank_md(pages: list[dict], top: int) -> str:
    figs = [f for p in pages for f in p["figures"]]
    scored = sorted(((trouble(f)[0], f) for f in figs), key=lambda t: -t[0])
    out = ["| trouble | figure | type | section | why |", "|---:|---|---|---|---|"]
    for score, f in scored[:top]:
        _s, why = trouble(f)
        out.append(f"| {score} | `{f['page']}` #{f['n']} L{f['line']} | {f['type']} | {(f['h2'] or '—')[:36]} | {'; '.join(why)} |")
    return "\n".join(out) + "\n"


def candidates_md(pages: list[dict]) -> str:
    """Sections over forty lines with no figure, densest in order/branch/cycle/containment words first — a section
    that is an order or a branch told in prose is where a reader would want a picture; a session judges each."""
    cands = sorted((c for p in pages for c in p["candidates"]), key=lambda c: (-c["density"], -c["lines"]))
    out = [f"{len(cands)} sections over forty lines with no figure, by the density of order/branch/cycle/containment words per hundred lines "
           f"(H3s: whether the section is already broken up).", "",
           "| page | section | lines | H3s | per 100 | order | branch | cycle | contain |", "|---|---|---:|---|---:|---:|---:|---:|---:|"]
    for c in cands:
        out.append(f"| `{c['page']}` | {'#' * c['level']} {c['heading'][:50]} (L{c['line']}) | {c['lines']} | {'yes' if c['has_h3'] else 'no'} | {c['density']} | {c['order']} | {c['branch']} | {c['cycle']} | {c['contain']} |")
    return "\n".join(out) + "\n"


# --- the probe ----------------------------------------------------------------------------------

PROBE_PAGE = """# Probe page

> Verified against **Minecraft 26.2** · Part IV · a probe

An opening that mentions `ChunkMap` before any figure and then stops.

| class | what it decides | thread |
|---|---|---|
| `ChunkMap` | the holders | Server |

## The lead figure opens this section

```mermaid
sequenceDiagram
    participant SL as ServerLevel
    participant CM as ChunkMap
    participant CH as ChunkHolder
    participant DM as DistanceManager
    participant TS as TicketStorage
    participant PCS as PlayerChunkSender
    participant SCC as ServerChunkCache
    participant MS as MinecraftServer
    SL->>CM: getChunk(pos), which walks the holder map and then asks the storage layer whether the chunk is already on disk before it schedules anything at all
    CM->>CH: promote
    rect rgba(0, 0, 0, 0.04)
        Note over SL,MS: a later tick
    end
```

The prose after the figure names `ChunkHolder.promote` and `DistanceManager` for the first time.

## A section with a lead-in and a caption

The write goes through four gates, and the figure below shows only the first:

```mermaid
flowchart TD
    A["LevelChunk.setBlockState"] --> B{"flags 11"}
    B -->|"2"| C["done"]
```

*Figure: the first gate, with the flag word it spends.*

Then the section continues and reads the diagram above.

## A class diagram, which this tool could not read until pass 7

```mermaid
classDiagram
    class LevelChunk {
        int nope
    }
    class Holder["PalettedContainer, the storage"] {
        NaturalSpawner field
    }
    LevelChunk *-- Holder : ChunkMap.promote
```

*Figure: the third, and its kind line is not a name.*

## A long section with no figure

""" + "\n".join(f"Line {i}: first this happens, then that happens, and if the third thing fails it is skipped, again every tick." for i in range(45)) + "\n"


def probe() -> int:
    tmp = tempfile.mkdtemp(prefix="pass7probe-")
    d = os.path.join(tmp, "systems", "world")
    os.makedirs(d)
    with open(os.path.join(d, "probe.md"), "w", encoding="utf-8") as fh:
        fh.write(PROBE_PAGE)
    global SRC
    old = SRC
    SRC = tmp
    try:
        p = figures_of("world/probe", "world", "systems/world/probe.md", {})
    finally:
        SRC = old
    f1, f2 = p["figures"][0], p["figures"][1]
    f3 = p["figures"][2]
    checks = [
        ("three figures found, in order", len(p["figures"]) == 3 and f1["line"] < f2["line"] < f3["line"]),
        ("figure 1 opens its section and is the lead figure after the cast", f1["opens_section"] and f1["lead"] and not f1["before_cast"]),
        ("figure 1 has eight lanes and one tick bar", f1["lane_count"] == 8 and f1["tick_bars"] == 1),
        ("figure 1's long message is a sentence label", len(f1["sentence_labels"]) == 1),
        ("figure 1's names: ChunkMap before, DistanceManager after, TicketStorage never",
         "ChunkMap" in f1["names"]["before"] and "DistanceManager" in f1["names"]["after"] and "TicketStorage" in f1["names"]["never"]),
        ("figure 1: most names first met here", f1["names_first_here"] >= 0.5),
        ("figure 2 has a lead-in ending in a colon and a caption", bool(f2["lead_in"]) and f2["lead_in"].endswith(":") and f2["caption"] == "Figure: the first gate, with the flag word it spends."),
        ("figure 2's bare-number gates are found", set(f2["number_gates"]) == {"flags 11", "2"}),
        ("figure 2 is pointed at by its section", f2["pointers"] >= 1),
        ("the long section with no figure is a candidate with order, branch and cycle words",
         len(p["candidates"]) == 1 and p["candidates"][0]["order"] > 40 and p["candidates"][0]["branch"] > 40 and p["candidates"][0]["cycle"] > 40),
        ("a rect band's colour is not read as a name", "rgba" not in f1["names"]["never"] and "rgba" not in f1["names"]["after"]),
        ("a classDiagram is read, and its own kind line is not a name",
         f3["type"] == "classDiagram" and "classDiagram" not in f3["names"]["never"]),
        ("a classDiagram's class names, display label and relation label are all read",
         {"LevelChunk", "PalettedContainer", "NaturalSpawner", "ChunkMap.promote"} <= set(f3["names"]["never"]) | set(f3["names"]["before"]) | set(f3["names"]["after"])),
        ("trouble ranks figure 1 above figure 2", trouble(f1)[0] > trouble(f2)[0]),
    ]
    ok = True
    for what, passed in checks:
        print(f"{'pass' if passed else 'FAIL'}  {what}")
        ok &= bool(passed)
    print("probe passed" if ok else "PROBE FAILED")
    return 0 if ok else 1


# --- main ---------------------------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pages", nargs="*", help="part/slug, reference/slug, or introduction")
    ap.add_argument("--part", help="a part directory under src/systems, or reference, or frame")
    ap.add_argument("--summary", action="store_true")
    ap.add_argument("--rank", action="store_true")
    ap.add_argument("--top", type=int, default=40)
    ap.add_argument("--candidates", action="store_true")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--out", help="with --json: write here instead of stdout")
    ap.add_argument("--render", default=RENDER_INDEX, help="render/index.json from render_figures.js")
    ap.add_argument("--probe", action="store_true")
    args = ap.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if args.probe:
        return probe()

    render = load_render(args.render)
    meta = render.pop("_meta", None) if render else None
    pages_all = all_pages()
    wanted = pages_all
    if args.pages:
        keys = [re.sub(r"\.md$", "", re.sub(r"^(?:src/)?(?:systems/)?", "", p.replace("\\", "/"))) for p in args.pages]
        wanted = [t for t in pages_all if t[0] in keys]
        missing = set(keys) - {t[0] for t in wanted}
        if missing:
            sys.exit(f"unknown page(s): {', '.join(sorted(missing))}")
    elif args.part:
        wanted = [t for t in pages_all if t[1] == args.part]
        if not wanted:
            sys.exit(f"no pages in part {args.part!r}")
    pages = [figures_of(k, part, rel, render) for k, part, rel in wanted]

    if args.json:
        data = {"render": meta, "pages": pages}
        text = json.dumps(data, ensure_ascii=False, indent=1)
        if args.out:
            with open(args.out, "w", encoding="utf-8") as fh:
                fh.write(text)
            print(f"wrote {args.out}: {sum(len(p['figures']) for p in pages)} figures on {len(pages)} pages")
        else:
            print(text)
        return 0
    if args.summary:
        print(summary_md(pages, meta))
        return 0
    if args.rank:
        print(rank_md(pages, args.top))
        return 0
    if args.candidates:
        print(candidates_md(pages))
        return 0
    if args.pages:
        for p in pages:
            print(page_md(p))
        return 0
    if args.part:
        print(part_table(pages, args.part))
        return 0
    ap.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
