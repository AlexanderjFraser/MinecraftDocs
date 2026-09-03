#!/usr/bin/env python3
"""Every diagram on a page as a numbered list of its arrows, so a report can answer each one.

`check_mermaid.js` proves a diagram parses; pass 4's charter (addition 3) says
every sequence-diagram arrow is checked in order against the code that makes
the call, every tick-boundary bar against the phase it names, every flowchart
branch against the condition that decides it, every state transition against
its trigger. A numbered list is what makes "arrow by arrow" auditable: the
agent's report has to carry one verdict per number, and a missing number is a
gap the session can see.

Per diagram: its type and the line it starts on; for a sequence diagram the
lanes (participants, as lane → class) and then, numbered, each message, note,
and block boundary (`rect`, `loop`, `alt`, `opt`, `par`, `critical`, `break`)
in file order; for a flowchart, the node labels and then each edge with its
label; for a state diagram, each transition with its trigger; for a timeline
or pie, each line. Parsing is tolerant — a line the parser cannot read is
printed raw with a `?` so nothing is silently dropped.

Usage:
    python tools/diagram_arrows.py src/systems/server/server-tick.md
    python tools/diagram_arrows.py src/systems/world --out DIR      # one <slug>.arrows.md per page
    python tools/diagram_arrows.py --all --summary                  # diagrams and arrows per page
"""
from __future__ import annotations

import argparse
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "src")

SEQ_MSG = re.compile(r"^\s*([\w.\-]+)\s*(-{1,2}(?:>>|>|x|\))|<<-{1,2}>>)\s*([\w.\-]+)\s*:\s*(.*)$")
SEQ_NOTE = re.compile(r"^\s*[Nn]ote\s+(over|left of|right of)\s+([^:]+):\s*(.*)$")
SEQ_BLOCK = re.compile(r"^\s*(rect|loop|alt|else|opt|par|and|critical|option|break)\b\s*(.*)$")
SEQ_END = re.compile(r"^\s*end\s*$")
PARTICIPANT = re.compile(r"^\s*(?:participant|actor)\s+([\w.\-]+)(?:\s+as\s+(.*))?$")
ACTIVATE = re.compile(r"^\s*(?:activate|deactivate)\s+")

# an id is a word that starts with a letter; its shape follows with no space (mermaid's own rule),
# so `-->` is never read as an id followed by the `>text]` asymmetric shape
NODE_DEF = re.compile(r"(?<![\w>\-])([A-Za-z_]\w*)(\[\[.*?\]\]|\[\(.*?\)\]|\(\(.*?\)\)|\{\{.*?\}\}|\[/.*?/\]|\[\\.*?\\\]|\[.*?\]|\(.*?\)|\{.*?\}|>.*?\])")
FLOW_EDGE = re.compile(
    r"\s*("
    r"<?-{2,}\s*\"[^\"]*\"\s*-{2,}>"        # -- "label" -->
    r"|<?-{2,}\s*\|[^|]*\|\s*-{2,}>"        # --|label|-->  (rare)
    r"|<?-\.+\s*\"[^\"]*\"\s*\.+->"          # -. "label" .->
    r"|<?={2,}\s*\"[^\"]*\"\s*={2,}>"        # == "label" ==>
    r"|<?-{2,}>\s*\|[^|]*\|"                 # -->|label|
    r"|<?-\.+->\s*\|[^|]*\|"                 # -.->|label|
    r"|<?={2,}>\s*\|[^|]*\|"                 # ==>|label|
    r"|<?-{2,}>|<?-\.+->|<?={2,}>|-{3,}|-\.+-|={3,}|-{2,}[ox]|[ox]-{2,}"
    r")\s*")


def label_of(op: str) -> str:
    m = re.search(r"\"([^\"]*)\"|\|([^|]*)\|", op)
    if not m:
        return ""
    return (m.group(1) if m.group(1) is not None else m.group(2)).strip()


def strip_label(text: str) -> str:
    text = text.strip()
    m = re.fullmatch(r"\[\[(.*)\]\]|\[\((.*)\)\]|\(\((.*)\)\)|\{\{(.*)\}\}|\[/(.*)/\]|\[\\(.*)\\\]|\[(.*)\]|\((.*)\)|\{(.*)\}|>(.*)\]", text)
    if m:
        text = next(g for g in m.groups() if g is not None)
    return text.strip().strip("\"").strip()


def diagrams_of(page: str):
    with open(page, encoding="utf-8") as f:
        lines = f.read().split("\n")
    i, n = 0, len(lines)
    while i < n:
        if lines[i].startswith("```mermaid"):
            start = i + 1
            body = []
            i += 1
            while i < n and not lines[i].startswith("```"):
                body.append((i + 1, lines[i]))
                i += 1
            yield start, body
        i += 1


def parse_sequence(body):
    lanes, items = [], []
    for ln, raw in body:
        t = raw.strip()
        if not t or t.startswith("%%") or t == "sequenceDiagram" or t.startswith("autonumber") or t.startswith("title"):
            continue
        m = PARTICIPANT.match(t)
        if m:
            lanes.append((m.group(1), (m.group(2) or m.group(1)).strip()))
            continue
        if ACTIVATE.match(t):
            continue
        m = SEQ_MSG.match(t)
        if m:
            a, op, b, msg = m.groups()
            kind = "async" if op.endswith(")") else "lost" if op.endswith("x") else "reply" if op.startswith("--") else "call"
            items.append((ln, f"{a} → {b}: {msg}" + ("" if kind == "call" else f"  [{kind}]")))
            continue
        m = SEQ_NOTE.match(t)
        if m:
            items.append((ln, f"note {m.group(1)} {m.group(2).strip()}: {m.group(3)}"))
            continue
        m = SEQ_BLOCK.match(t)
        if m:
            items.append((ln, f"[{m.group(1)}] {m.group(2)}".rstrip()))
            continue
        if SEQ_END.match(t):
            items.append((ln, "[end]"))
            continue
        items.append((ln, f"? {t}"))
    return lanes, items


def parse_flow(body):
    nodes: dict[str, str] = {}
    edges = []
    for ln, raw in body:
        t = raw.strip()
        if not t or t.startswith("%%") or re.match(r"^(flowchart|graph)\b", t):
            continue
        if re.match(r"^(classDef|class |style |linkStyle|direction)\b", t):
            continue
        if t.startswith("subgraph"):
            edges.append((ln, f"[subgraph] {strip_label(t[len('subgraph'):])}"))
            continue
        if t == "end":
            edges.append((ln, "[end]"))
            continue
        # collect node definitions first
        for m in NODE_DEF.finditer(t):
            nodes[m.group(1)] = strip_label(m.group(2))
        parts = FLOW_EDGE.split(t)
        # parts alternates: node, op, node, op, node ...
        if len(parts) < 3:
            m = NODE_DEF.fullmatch(t)
            if m or re.fullmatch(r"[\w.\-]+", t):
                continue   # a bare node definition
            edges.append((ln, f"? {t}"))
            continue
        segs = [p for p in parts]
        for k in range(0, len(segs) - 2, 2):
            src, op, dst = segs[k], segs[k + 1], segs[k + 2]
            srcs = [s.strip() for s in src.split("&")]
            dsts = [d.strip() for d in dst.split("&")]
            lab = label_of(op)
            style = "dashed" if "." in op else "thick" if "==" in op else "line" if not op.rstrip("|\" ").endswith(">") and not re.search(r">\s*\|", op) else ""
            for s in srcs:
                sid = NODE_DEF.match(s).group(1) if NODE_DEF.match(s) else s
                for d in dsts:
                    did = NODE_DEF.match(d).group(1) if NODE_DEF.match(d) else d
                    desc = f"{sid} → {did}"
                    if lab:
                        desc += f"  “{lab}”"
                    if style:
                        desc += f"  [{style}]"
                    edges.append((ln, desc))
    return nodes, edges


def parse_state(body):
    items = []
    for ln, raw in body:
        t = raw.strip()
        if not t or t.startswith("%%") or t.startswith("stateDiagram") or t.startswith("direction"):
            continue
        m = re.match(r"^(\[\*\]|[\w.\-]+)\s*-->\s*(\[\*\]|[\w.\-]+)\s*(?::\s*(.*))?$", t)
        if m:
            items.append((ln, f"{m.group(1)} → {m.group(2)}" + (f": {m.group(3)}" if m.group(3) else "")))
            continue
        m = re.match(r"^note\s+(left of|right of)\s+([\w.\-]+)\s*:\s*(.*)$", t)
        if m:
            items.append((ln, f"note {m.group(1)} {m.group(2)}: {m.group(3)}"))
            continue
        m = re.match(r"^state\s+(.*)$", t)
        if m:
            items.append((ln, f"[state] {m.group(1)}"))
            continue
        m = re.match(r"^([\w.\-]+)\s*:\s*(.*)$", t)
        if m:
            items.append((ln, f"[state] {m.group(1)}: {m.group(2)}"))
            continue
        if t in ("}", "end"):
            items.append((ln, "[end]"))
            continue
        items.append((ln, f"? {t}"))
    return items


def parse_lines(body):
    return [(ln, raw.strip()) for ln, raw in body if raw.strip() and not raw.strip().startswith("%%")][1:]


def render_page(page: str) -> tuple[str, int, int]:
    rel = os.path.relpath(page, ROOT).replace("\\", "/")
    out = [f"# Diagrams, arrow by arrow — `{rel}`", ""]
    ndiag = narrow = 0
    for start, body in diagrams_of(page):
        head = next((raw.strip() for _ln, raw in body if raw.strip()), "")
        kind = head.split()[0] if head else "?"
        ndiag += 1
        out.append(f"## Figure {ndiag} — {kind}, line {start}")
        out.append("")
        if kind == "sequenceDiagram":
            lanes, items = parse_sequence(body)
            if lanes:
                out.append("Lanes: " + " · ".join(f"{a} = {b}" for a, b in lanes))
                out.append("")
        elif kind in ("flowchart", "graph"):
            nodes, items = parse_flow(body)
            if nodes:
                out.append("Nodes: " + " · ".join(f"{k} = “{v}”" for k, v in nodes.items()))
                out.append("")
        elif kind.startswith("stateDiagram"):
            items = parse_state(body)
        else:
            items = parse_lines(body)
        for k, (ln, desc) in enumerate(items, 1):
            out.append(f"{k}. (L{ln}) {desc}")
            narrow += 1
        out.append("")
    if ndiag == 0:
        out.append("(no mermaid diagrams on this page)")
    return "\n".join(out), ndiag, narrow


def collect_pages(paths: list[str], all_pages: bool) -> list[str]:
    pages = []
    if all_pages:
        paths = [os.path.join(SRC, "systems"), os.path.join(SRC, "reference"), os.path.join(SRC, "maps"),
                 os.path.join(SRC, "figures"), os.path.join(SRC, "introduction.md"), os.path.join(SRC, "lectures.md")]
    for p in paths:
        p = os.path.abspath(p)
        if os.path.isdir(p):
            for dp, _dn, fn in os.walk(p):
                for f in sorted(fn):
                    if f.endswith(".md"):
                        pages.append(os.path.join(dp, f))
        elif os.path.exists(p):
            pages.append(p)
        else:
            sys.exit(f"no such page: {p}")
    return sorted(set(pages))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paths", nargs="*")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--summary", action="store_true", help="diagrams and arrows per page")
    ap.add_argument("--out", help="write one <slug>.arrows.md per page here")
    args = ap.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    pages = collect_pages(args.paths, args.all)
    if not pages:
        ap.print_help()
        return 2
    if args.out:
        os.makedirs(args.out, exist_ok=True)
    td = ta = tq = 0
    for p in pages:
        text, nd, na = render_page(p)
        nq = text.count("\n") and sum(1 for l in text.split("\n") if re.match(r"^\d+\. \(L\d+\) \? ", l))
        td, ta, tq = td + nd, ta + na, tq + nq
        rel = os.path.relpath(p, SRC).replace("\\", "/")
        if args.summary:
            if nd:
                print(f"{nd:3d} diagrams {na:4d} arrows {nq:3d} unparsed  {rel}")
            continue
        if args.out:
            slug = re.sub(r"^systems/", "", rel)[:-3].replace("/", "--")
            with open(os.path.join(args.out, f"{slug}.arrows.md"), "w", encoding="utf-8") as f:
                f.write(text + "\n")
            print(f"{nd:3d} diagrams {na:4d} arrows {nq:3d} unparsed  {rel}")
        else:
            print(text)
    if args.summary or args.out:
        print(f"\n{td} diagrams, {ta} arrows/notes/bars, {tq} lines the parser could not read (marked ?)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
