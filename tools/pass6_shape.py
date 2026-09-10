#!/usr/bin/env python3
"""The shape of every page, measured for pass 6: the devices, the skeletons, the budgets, the landing pages.

Pass 6's charter (`docs/plan.md`, *Pass 6 — the lecture*) is about one page at a
time: the devices that became slots, the twin skeletons, the section order, the
cuts. Pass 5's close counted the devices by hand; this counts them the same way
every time, per page and per part, so a session starts from numbers rather than
from memory and the brief's schedule can be re-derived. Nothing here is a gate
and nothing here measures prose quality — a count in a queue is a description,
not a target.

Per system page (`src/systems/<part>/<slug>.md`), read outside code fences:

  the opening    the first prose paragraph after the verified line: sentences and
                 words; whether its first sentence is in the second person (you,
                 your); whether its last sentence carries bold; whether its last
                 sentence is a dash clause
  the spine      the H2 sections in order, each with its lines, its figures by
                 mermaid type, its H3s, its lists and its tables; the literal
                 `## The trace…` heading
  the cast       the cast table's rows
  the closer     the questions section (an H2 whose title starts *Questions*): its
                 spelling, whether it is the last section before *Where to look*,
                 its question count and its lines
  the blockquote the *For a 1.21-era reader* device: its lines and the section it
                 sits in, and whether that is the foot of the page
  the devices    the myth table, the number on its own line, the tick-boundary bar
  the budgets    lists over seven items, items over two sentences, more than three
                 lists, sections over forty lines with neither a figure nor an H3,
                 *Where to look* names against the cast
  the signature  the spine as tokens (cast · trace · q · look · seq · flow · state ·
                 svg · p), which is what the twin-skeleton finder compares

Per landing page: lines outside *Watch in this order*, the recognition sentence
and whether it ends the argument, the sections that are not one of the six the
template names and where they sit, the size include, a hand-counted coverage
number.

Usage:
    python tools/pass6_shape.py --summary                 # the devices per part, corpus-wide
    python tools/pass6_shape.py --part world              # every page of a part, one row each
    python tools/pass6_shape.py world/lighting            # one page's report in full (markdown)
    python tools/pass6_shape.py --twins                   # skeleton groups: identical spines, and spines one edit apart
    python tools/pass6_shape.py --landing                 # the thirteen landing pages
    python tools/pass6_shape.py --slots                   # pages ranked by how many fixed devices they carry at once
    python tools/pass6_shape.py --probe                   # prove the measurements on a synthetic page
"""
from __future__ import annotations

import argparse
import os
import re
import statistics
import sys
from collections import defaultdict
from dataclasses import dataclass, field

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pass4_queue as queue   # noqa: E402

ROOT = queue.ROOT
SRC = queue.SRC
NUMERAL = {v: k for k, v in queue.ROMAN.items()}

H2 = re.compile(r"^## (.*)$")
H3 = re.compile(r"^### ")
FENCE = re.compile(r"^```")
LIST_ITEM = re.compile(r"^(\s*)(?:[-*]|\d+[.)])\s+(.*)$")
TICK = re.compile(r"`([^`]+)`")
SECOND = re.compile(r"\b(?:you|your|yours|yourself)\b", re.I)
BOLD = re.compile(r"\*\*[^*]+\*\*")
QLEAD = re.compile(r"^\*\*(.+?)\*\*")          # nested emphasis allowed: **why is *this* so?**
QMARK = re.compile(r"^\*\*(.+?)\?\*\*")
BLOCKQUOTE_121 = re.compile(r"^> \*\*For a 1\.21")
NUMBER_DEVICE = re.compile(r"^\*\*[A-Z][A-Za-z-]*(?: [a-z-]+){0,2}\*\* — ")   # **Four** — what it counts
MYTH = re.compile(r"what the forum says", re.I)
RECOGNISE = re.compile(r"recogni[sz]es? (?:this|the) (?:part|split) by", re.I)
PERCENT = re.compile(r"\b\d{1,3}%")
FRACTION_WORDS = re.compile(r"\b(?:a third|a quarter|half|two fifths|a fifth|three quarters|two thirds)\b[^.]{0,80}\bnamed\b"
                            r"|\bnamed\b[^.]{0,80}\b(?:a third|a quarter|half|two fifths|a fifth|three quarters|two thirds)\b", re.I)
CANON_CLOSER = "Questions players ask"
SIX = ("the shape of the part", "before you start", "watch in this order", "reference this part uses")
FIG_TYPE = {"sequenceDiagram": "seq", "flowchart": "flow", "graph": "flow", "stateDiagram-v2": "state",
            "stateDiagram": "state", "classDiagram": "class"}

_AFTER = r"\s+(?=[A-Z`(\[*\"“])"
SENT_END = re.compile(rf"(?<=[.!?]){_AFTER}|(?<=[.!?]\*\*){_AFTER}|(?<=[.!?]\)){_AFTER}|(?<=[.!?]\*){_AFTER}")


def read(path: str) -> str:
    with open(path, encoding="utf-8") as f:
        return f.read()


def sentences(text: str) -> list[str]:
    flat = " ".join(l.strip() for l in text.split("\n")).strip()
    return [p.strip() for p in SENT_END.split(flat) if p.strip()]


@dataclass
class Section:
    title: str
    start: int
    end: int = 0
    figures: list = field(default_factory=list)      # 'seq' | 'flow' | 'state' | 'class' | 'svg'
    h3: int = 0
    lists: list = field(default_factory=list)        # (start line, items, items over two sentences)
    tables: int = 0
    myth: bool = False
    blockquote_121: tuple | None = None              # (line, lines)
    prose_lines: int = 0
    leads: int = 0                                   # bold lead-in paragraphs
    questions: int = 0                               # bold lead-ins ending in ?
    number_devices: int = 0
    tick_bars: int = 0

    @property
    def lines(self) -> int:
        return self.end - self.start + 1

    @property
    def is_look(self) -> bool:
        return self.title.lower().startswith("where to look")

    @property
    def is_cast(self) -> bool:
        return "cast" in self.title.lower()

    @property
    def is_closer(self) -> bool:
        return bool(re.match(r"Questions\b", self.title))

    @property
    def is_trace_heading(self) -> bool:
        return self.title.startswith("The trace")

    @property
    def token(self) -> str:
        if self.is_cast:
            return "cast"
        if self.is_look:
            return "look"
        if self.is_closer:
            return "q"
        if self.is_trace_heading:
            return "trace"
        return self.figures[0] if self.figures else "p"


@dataclass
class Page:
    key: str
    rel: str
    part: str
    num: int
    title: str = ""
    lines: int = 0
    words: int = 0
    opening: str = ""
    opening_line: int = 0
    sections: list = field(default_factory=list)
    preamble: Section | None = None
    cast_rows: int = 0
    look_names: int = 0
    includes_svg: int = 0

    # derived
    @property
    def content(self) -> list:
        return [s for s in self.sections if not s.is_look]

    @property
    def closer(self) -> Section | None:
        cs = [s for s in self.sections if s.is_closer]
        return cs[-1] if cs else None

    @property
    def closer_last(self) -> bool:
        c = self.closer
        return bool(c) and self.content and self.content[-1] is c

    @property
    def trace_heading(self) -> Section | None:
        return next((s for s in self.sections if s.is_trace_heading), None)

    @property
    def blockquote(self) -> tuple | None:
        """(section, line, lines, at the foot?) for the 1.21 device, or None."""
        for s in self.sections + ([self.preamble] if self.preamble else []):
            if s and s.blockquote_121:
                foot = bool(self.content) and (s is self.content[-1] or s.is_look)
                return (s, s.blockquote_121[0], s.blockquote_121[1], foot)
        return None

    @property
    def figures(self) -> list:
        out = []
        for s in ([self.preamble] if self.preamble else []) + self.sections:
            out += s.figures
        return out

    @property
    def signature(self) -> tuple:
        return tuple(s.token for s in self.sections)

    @property
    def opening_sentences(self) -> list:
        return sentences(self.opening) if self.opening else []

    @property
    def opens_second_person(self) -> bool:
        ss = self.opening_sentences
        return bool(ss) and bool(SECOND.search(ss[0]))

    @property
    def opening_second_person(self) -> bool:
        return bool(self.opening) and bool(SECOND.search(self.opening))

    @property
    def opening_ends_bold(self) -> bool:
        ss = self.opening_sentences
        return bool(ss) and bool(BOLD.search(ss[-1]))

    @property
    def opening_ends_dash(self) -> bool:
        ss = self.opening_sentences
        return bool(ss) and (" — " in ss[-1] or ss[-1].rstrip().endswith("—"))

    @property
    def shape_guess(self) -> str:
        first = next((t for t in self.figures if t != "svg"), None)
        return {"seq": "trace", "flow": "pipeline or policy", "state": "state machine", "class": "vocabulary"}.get(first or "", "no mermaid figure" if not self.figures else "generated figure only")

    def all_lists(self) -> list:
        out = []
        for s in ([self.preamble] if self.preamble else []) + self.sections:
            out += s.lists
        return out

    def long_sections(self) -> list:
        return [s for s in self.sections if s.lines > 40 and not s.figures and s.h3 == 0 and not s.is_look]

    def slots(self) -> list:
        """The fixed devices this page carries at once, by name."""
        out = []
        if self.closer:
            out.append("closer")
        if self.trace_heading:
            out.append("trace heading")
        if self.blockquote:
            out.append("1.21 blockquote")
        if self.opening_ends_bold:
            out.append("bold ending")
        if self.opens_second_person:
            out.append("second person")
        if any(s.myth for s in self.sections):
            out.append("myth table")
        if sum(s.number_devices for s in self.sections):
            out.append("the number")
        return out


def parse_text(text: str, key: str = "?", rel: str = "?", part: str = "?", num: int = 0) -> Page:
    page = Page(key, rel, part, num)
    lines = text.split("\n")
    page.lines = len(lines)
    page.preamble = Section("", 1)
    cur = page.preamble
    fence, fence_type, fence_body = False, "", []
    cur_list = None          # [start line, items (list of str), current item index]
    prev_table = False
    bq = None                # [start line, count] for the 1.21 blockquote being counted
    verified_at = 0
    words = 0

    def close_list():
        nonlocal cur_list
        if cur_list:
            start, items = cur_list[0], cur_list[1]
            long = sum(1 for it in items if len(sentences(it)) > 2)
            cur.lists.append((start, len(items), long))
        cur_list = None

    for i, raw in enumerate(lines, 1):
        if FENCE.match(raw):
            if not fence:
                fence, fence_type, fence_body = True, raw[3:].strip(), []
            else:
                fence = False
                if fence_type == "mermaid":
                    first = next((l.strip().split()[0] for l in fence_body if l.strip()), "")
                    t = FIG_TYPE.get(first, first or "?")
                    cur.figures.append(t)
                    if t == "seq":
                        cur.tick_bars += sum(1 for l in fence_body if "Note over" in l)
            close_list()
            continue
        if fence:
            fence_body.append(raw)
            continue
        if bq is not None:
            if raw.startswith(">"):
                bq[1] += 1
                continue
            cur.blockquote_121 = (bq[0], bq[1])
            bq = None
        if raw.startswith("# ") and not page.title:
            page.title = raw[2:].strip()
            continue
        if raw.startswith("> Verified"):
            verified_at = i
            continue
        m = H2.match(raw)
        if m:
            close_list()
            cur.end = i - 1
            cur = Section(m.group(1).strip(), i)
            page.sections.append(cur)
            prev_table = False
            continue
        if H3.match(raw):
            close_list()
            cur.h3 += 1
            continue
        if raw.startswith("#"):
            close_list()
            continue
        if BLOCKQUOTE_121.match(raw):
            close_list()
            bq = [i, 1]
            continue
        if "{{#include" in raw and ".svg" in raw:
            cur.figures.append("svg")
            page.includes_svg += 1
            continue
        if raw.startswith("|"):
            close_list()
            if not prev_table:
                cur.tables += 1
                if MYTH.search(raw):
                    cur.myth = True
            prev_table = True
            if cur.is_cast and not re.match(r"^\|\s*(?:class|-)", raw):
                page.cast_rows += 1
            continue
        prev_table = False
        lm = LIST_ITEM.match(raw)
        if lm:
            indent = len(lm.group(1).expandtabs(4))
            if indent == 0:
                if cur_list is None:
                    cur_list = [i, [], 0]
                cur_list[1].append(lm.group(2))
            elif cur_list:
                cur_list[1][-1] += " " + lm.group(2)
            continue
        if raw.strip() == "":
            close_list()
            continue
        if cur_list and raw[:1] in " \t":
            cur_list[1][-1] += " " + raw.strip()
            continue
        close_list()
        if raw.startswith(">") or raw.startswith("<") or raw.startswith("{{") or raw.startswith("---"):
            continue
        # prose
        cur.prose_lines += 1
        words += len(raw.split())
        if QLEAD.match(raw):
            cur.leads += 1
            if QMARK.match(raw):
                cur.questions += 1
        if NUMBER_DEVICE.match(raw):
            cur.number_devices += 1
        if cur.is_look:
            page.look_names += len(TICK.findall(raw))
        if not page.opening and verified_at and cur is page.preamble:
            # the first prose paragraph after the verified line
            para, j = [raw], i
            while j < len(lines) and lines[j].strip() and not lines[j].startswith("#"):
                para.append(lines[j])
                j += 1
            page.opening = "\n".join(para)
            page.opening_line = i
    if bq is not None:
        cur.blockquote_121 = (bq[0], bq[1])
    close_list()
    cur.end = len(lines)
    page.words = words
    return page


def parse(key: str, pages: dict) -> Page:
    part, num, rel = pages[key]
    return parse_text(read(os.path.join(SRC, rel)), key, rel, part, num)


def system_pages(pages: dict, part: str | None = None) -> list[str]:
    return [k for k, (p, n, rel) in pages.items()
            if rel.startswith("systems/") and not rel.endswith("README.md") and (part is None or p == part)]


def landing_pages(pages: dict) -> list[str]:
    return [k for k, (p, n, rel) in pages.items() if rel.startswith("systems/") and rel.endswith("README.md")]


# --- the twin-skeleton finder -------------------------------------------------------------------

def edit_distance(a: tuple, b: tuple) -> int:
    prev = list(range(len(b) + 1))
    for i, x in enumerate(a, 1):
        cur = [i]
        for j, y in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (x != y)))
        prev = cur
    return prev[-1]


def twins(parsed: dict) -> tuple[list, list]:
    """(identical groups, near pairs). Identical: the same signature, four sections or more.
    Near: signatures one edit apart, five sections or more, not already identical."""
    by_sig = defaultdict(list)
    for key, pg in parsed.items():
        if len(pg.signature) >= 4:
            by_sig[pg.signature].append(key)
    groups = [(sig, sorted(keys)) for sig, keys in by_sig.items() if len(keys) > 1]
    groups.sort(key=lambda g: (-len(g[1]), g[1]))
    near = []
    keys = sorted(parsed)
    for i, a in enumerate(keys):
        sa = parsed[a].signature
        if len(sa) < 5:
            continue
        for b in keys[i + 1:]:
            sb = parsed[b].signature
            if len(sb) < 5 or sa == sb:
                continue
            if abs(len(sa) - len(sb)) <= 1 and edit_distance(sa, sb) == 1:
                near.append((a, b))
    return groups, near


# --- the landing pages ---------------------------------------------------------------------------

@dataclass
class Landing:
    key: str
    lines: int
    watch_lines: int
    h2: list                       # (title, start, lines)
    seventh: list                  # (title, position sentence)
    recognition: tuple | None      # (line, ends the argument?)
    argument_ends_bold: bool
    size_include: bool
    coverage_include: bool
    hand_counted: list             # (line, text)
    figure: bool

    @property
    def outside(self) -> int:
        return self.lines - self.watch_lines


def landing(key: str, pages: dict) -> Landing:
    part, num, rel = pages[key]
    text = read(os.path.join(SRC, rel))
    pg = parse_text(text, key, rel, part, num)
    h2 = [(s.title, s.start, s.lines) for s in pg.sections]
    watch = next((s for s in pg.sections if s.title.lower().startswith("watch in this order")), None)
    seventh = []
    for idx, s in enumerate(pg.sections):
        if any(s.title.lower().startswith(x) for x in SIX):
            continue
        before = pg.sections[idx - 1].title if idx else "the argument"
        after = pg.sections[idx + 1].title if idx + 1 < len(pg.sections) else "the end"
        seventh.append((s.title, f"section {idx + 1} of {len(pg.sections)}, after *{before}*, before *{after}*"))
    rec = None
    lines = text.split("\n")
    # paragraph by paragraph, because the sentence wraps across lines on most of the pages that carry it
    a = 1
    while a <= len(lines):
        if not lines[a - 1].strip() or lines[a - 1].startswith("#"):
            a += 1
            continue
        b = a
        while b < len(lines) and lines[b].strip() and not lines[b].startswith("#"):
            b += 1
        para = "\n".join(lines[a - 1:b])
        if RECOGNISE.search(" ".join(para.split())):
            ss = sentences(para)
            rec = (a, bool(ss) and bool(RECOGNISE.search(ss[-1])) and a == pg.opening_line)
            break
        a = b + 1
    hand = [(i, l.strip()) for i, l in enumerate(lines, 1)
            if "{{#include" not in l and (PERCENT.search(l) or FRACTION_WORDS.search(l))]
    return Landing(key, pg.lines, watch.lines if watch else 0, h2, seventh, rec,
                   pg.opening_ends_bold, "generated/part-" in text, "generated/coverage-" in text, hand,
                   bool(pg.figures))


# --- rendering -----------------------------------------------------------------------------------

def yn(b: bool) -> str:
    return "yes" if b else "no"


def report_md(pg: Page) -> str:
    out = [f"# Shape — `src/{pg.rel}`", "",
           f"Part {NUMERAL.get(pg.num, '—')} · {pg.lines} lines, {pg.words:,} words of prose · first figure says: **{pg.shape_guess}** "
           f"· {len(pg.figures)} figure{'s' if len(pg.figures) != 1 else ''} ({', '.join(pg.figures) or 'none'})", ""]
    ss = pg.opening_sentences
    out.append(f"**The opening** (L{pg.opening_line}; {len(ss)} sentences, {len(pg.opening.split())} words): "
               f"opens in the second person: **{yn(pg.opens_second_person)}** · second person anywhere in it: {yn(pg.opening_second_person)} · "
               f"ends on a bold sentence: **{yn(pg.opening_ends_bold)}** · ends on a dash clause: {yn(pg.opening_ends_dash)}.")
    if ss:
        out.append(f"  First sentence: *{ss[0][:160]}{'…' if len(ss[0]) > 160 else ''}*")
        out.append(f"  Last sentence: *{ss[-1][:200]}{'…' if len(ss[-1]) > 200 else ''}*")
    out += ["", f"**The spine** — {len(pg.sections)} sections; signature `{' '.join(pg.signature)}`", "",
            "| section | lines | figures | H3 | lists | tables | note |", "|---|---:|---|---:|---:|---:|---|"]
    for s in pg.sections:
        notes = []
        if s.is_trace_heading:
            notes.append("literal *The trace* heading")
        if s.is_closer:
            notes.append(f"closer: {s.questions} questions, {s.leads} lead-ins" + ("" if s.title == CANON_CLOSER else f" — spelt *{s.title}*"))
        if s.lines > 40 and not s.figures and s.h3 == 0 and not s.is_look:
            notes.append("over forty lines, no figure or H3")
        for start, n, long in s.lists:
            if n > 7:
                notes.append(f"list of {n} at L{start}")
            if long:
                notes.append(f"{long} item{'s' if long > 1 else ''} over two sentences at L{start}")
        if s.blockquote_121:
            notes.append(f"1.21 blockquote, {s.blockquote_121[1]} lines at L{s.blockquote_121[0]}")
        if s.myth:
            notes.append("myth table")
        if s.number_devices:
            notes.append(f"the number ×{s.number_devices}")
        if s.tick_bars:
            notes.append(f"tick bars ×{s.tick_bars}")
        out.append(f"| {s.title} | {s.lines} | {', '.join(s.figures) or '—'} | {s.h3} | {len(s.lists)} | {s.tables} | {'; '.join(notes)} |")
    c = pg.closer
    out.append("")
    if c:
        out.append(f"**The closer**: `## {c.title}`{'' if c.title == CANON_CLOSER else ' (not the canonical spelling)'} — "
                   f"{'the last content section' if pg.closer_last else 'NOT the last content section'}; {c.questions} questions in {c.lines} lines "
                   f"({100 * c.lines // max(pg.lines, 1)}% of the page).")
    else:
        out.append("**The closer**: none.")
    b = pg.blockquote
    if b:
        s, line, n, foot = b
        out.append(f"**The 1.21 blockquote**: {n} lines at L{line}, inside *{s.title or 'the opening'}* — {'at the foot of the page' if foot else 'in the body'}.")
    else:
        out.append("**The 1.21 blockquote**: none.")
    t = pg.trace_heading
    out.append(f"**The trace heading**: {'`## ' + t.title + '`' if t else 'none'}.")
    out.append(f"**The cast**: {pg.cast_rows} rows · ***Where to look***: {pg.look_names} names.")
    lists = pg.all_lists()
    over = [l for l in lists if l[1] > 7]
    longs = sum(l[2] for l in lists)
    out.append(f"**The budgets**: {len(lists)} list{'s' if len(lists) != 1 else ''}"
               f"{' (over the three the template allows)' if len(lists) > 3 else ''}; "
               f"{len(over)} over seven items; {longs} item{'s' if longs != 1 else ''} over two sentences; "
               f"{len(pg.long_sections())} section{'s' if len(pg.long_sections()) != 1 else ''} over forty lines with neither a figure nor an H3"
               + (": " + ", ".join(f"*{s.title}* ({s.lines})" for s in pg.long_sections()) if pg.long_sections() else "") + ".")
    out.append(f"**The slots this page carries at once**: {', '.join(pg.slots()) or 'none'} ({len(pg.slots())}).")
    return "\n".join(out) + "\n"


def row(pg: Page) -> str:
    c = pg.closer
    b = pg.blockquote
    closer = ("last" if pg.closer_last else "mid") + ("" if not c or c.title == CANON_CLOSER else "*") if c else "—"
    return (f"| `{pg.key.split('/', 1)[1]}` | {pg.lines} | {' '.join(pg.signature)} | {closer} | "
            f"{'yes' if pg.trace_heading else '—'} | {('foot' if b[3] else 'body') if b else '—'} | "
            f"{'yes' if pg.opens_second_person else '—'} | {'yes' if pg.opening_ends_bold else '—'} | "
            f"{len([l for l in pg.all_lists() if l[1] > 7])} | {len(pg.long_sections())} | {len(pg.slots())} |")


PART_HEADER = ("| page | lines | spine | closer | trace heading | 1.21 | 2nd person opening | bold ending | lists >7 | long sections | slots |",
               "|---|---:|---|---|---|---|---|---|---:|---:|---:|")


def part_table_md(part: str, parsed: dict, pages: dict) -> str:
    keys = [k for k in system_pages(pages, part)]
    pgs = [parsed[k] for k in keys]
    num = pages[keys[0]][1] if keys else 0
    n = len(pgs)
    closers = [p for p in pgs if p.closer]
    spellings = sorted({p.closer.title for p in closers})
    out = [f"# Shape — Part {NUMERAL.get(num, '—')} · {part} ({n} pages)", "",
           f"- the closer on **{len(closers)} of {n}** ({', '.join(f'*{s}*' for s in spellings) or '—'}); "
           f"last content section on {sum(1 for p in closers if p.closer_last)}",
           f"- the literal `## The trace` heading on {sum(1 for p in pgs if p.trace_heading)}",
           f"- the 1.21 blockquote on {sum(1 for p in pgs if p.blockquote)} "
           f"(at the foot on {sum(1 for p in pgs if p.blockquote and p.blockquote[3])})",
           f"- the opening in the second person on {sum(1 for p in pgs if p.opens_second_person)}; "
           f"ending on a bold sentence on {sum(1 for p in pgs if p.opening_ends_bold)}; on a dash clause on {sum(1 for p in pgs if p.opening_ends_dash)}",
           f"- lines: {min(p.lines for p in pgs) if pgs else 0}–{max(p.lines for p in pgs) if pgs else 0}, median {int(statistics.median([p.lines for p in pgs])) if pgs else 0}",
           "", "Closer: *last* = the last content section, *mid* = not; `*` = not the canonical spelling. "
           "Slots = the fixed devices the page carries at once (closer, trace heading, 1.21 blockquote, bold ending, second person, myth table, the number).", "",
           *PART_HEADER]
    out += [row(p) for p in pgs]
    groups, near = twins({k: parsed[k] for k in parsed})
    mine_groups = [(sig, ks) for sig, ks in groups if any(k in keys for k in ks)]
    mine_near = [(a, b) for a, b in near if a in keys and b in keys]
    out += ["", "## Skeleton twins touching this part", "",
            "An identical spine anywhere in the book is listed; a spine one edit apart only inside the part, "
            "because on a ten-token alphabet most cross-part near-misses are two prose pages that happen to be the same length.", ""]
    if not mine_groups and not mine_near:
        out.append("- (none: no other page shares a spine with any page here, and no two pages of the part are one edit apart)")
    for sig, ks in mine_groups:
        out.append(f"- identical spine `{' '.join(sig)}`: " + ", ".join(f"`{k}`" for k in ks))
    for a, b in mine_near:
        out.append(f"- one edit apart, within the part: `{a}` (`{' '.join(parsed[a].signature)}`) ↔ `{b}` (`{' '.join(parsed[b].signature)}`)")
    return "\n".join(out) + "\n"


def landing_md(land: Landing) -> str:
    out = [f"# Landing page — `{land.key}`", "",
           f"{land.lines} lines, of which {land.watch_lines} are *Watch in this order*: **{land.outside} outside it** "
           f"(the template's budget is about a hundred). Figure of the part's pages: {yn(land.figure)}. "
           f"Size include: {yn(land.size_include)}. Coverage include: {yn(land.coverage_include)}.", "",
           "Sections: " + " · ".join(f"*{t}* ({n})" for t, _s, n in land.h2), ""]
    if land.seventh:
        for title, pos in land.seventh:
            out.append(f"- **A section outside the template's six**: *{title}* — {pos}.")
    else:
        out.append("- No section outside the template's six (the coverage answer, if any, has no heading of its own).")
    if land.recognition:
        line, last = land.recognition
        out.append(f"- **The recognition sentence** at L{line}" + (", and it is the argument's last sentence." if last else "."))
    else:
        out.append("- No recognition sentence.")
    out.append(f"- The argument ends on a bold sentence: {yn(land.argument_ends_bold)}.")
    for line, text in land.hand_counted:
        out.append(f"- **A hand-counted number** at L{line}: *{text[:140]}*")
    return "\n".join(out) + "\n"


def summary_md(parsed: dict, pages: dict) -> str:
    parts = []
    for k in system_pages(pages):
        p = pages[k][0]
        if p not in parts:
            parts.append(p)
    out = ["| part | pages | closer | spellings | `## The trace` | 1.21 (foot) | 2nd-person opening | bold ending | dash ending | in a twin group | lists >7 | long sections | median lines |",
           "|---|---:|---:|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|"]
    groups, _near = twins(parsed)
    twinned = {k for _sig, ks in groups for k in ks}
    tot = defaultdict(int)
    allpgs = []
    for part in parts:
        keys = system_pages(pages, part)
        pgs = [parsed[k] for k in keys]
        allpgs += pgs
        num = pages[keys[0]][1]
        closers = [p for p in pgs if p.closer]
        vals = {
            "pages": len(pgs), "closer": len(closers), "spellings": len({p.closer.title for p in closers}),
            "trace": sum(1 for p in pgs if p.trace_heading),
            "bq": sum(1 for p in pgs if p.blockquote), "bqfoot": sum(1 for p in pgs if p.blockquote and p.blockquote[3]),
            "second": sum(1 for p in pgs if p.opens_second_person), "bold": sum(1 for p in pgs if p.opening_ends_bold),
            "dash": sum(1 for p in pgs if p.opening_ends_dash), "twin": sum(1 for k in keys if k in twinned),
            "lists": sum(len([l for l in p.all_lists() if l[1] > 7]) for p in pgs),
            "long": sum(len(p.long_sections()) for p in pgs),
        }
        for k2, v in vals.items():
            tot[k2] += v
        out.append(f"| {NUMERAL[num]} · {part} | {vals['pages']} | {vals['closer']} | {vals['spellings']} | {vals['trace']} | "
                   f"{vals['bq']} ({vals['bqfoot']}) | {vals['second']} | {vals['bold']} | {vals['dash']} | {vals['twin']} | "
                   f"{vals['lists']} | {vals['long']} | {int(statistics.median([p.lines for p in pgs]))} |")
    spell = sorted({p.closer.title for p in allpgs if p.closer})
    out.append(f"| **all** | {tot['pages']} | {tot['closer']} | {len(spell)} | {tot['trace']} | {tot['bq']} ({tot['bqfoot']}) | "
               f"{tot['second']} | {tot['bold']} | {tot['dash']} | {tot['twin']} | {tot['lists']} | {tot['long']} | "
               f"{int(statistics.median([p.lines for p in allpgs]))} |")
    out += ["", "Closer spellings: " + "; ".join(f"*{s}* ×{sum(1 for p in allpgs if p.closer and p.closer.title == s)}" for s in spell),
            f"Closer not the last content section on: " + ", ".join(f"`{p.key}`" for p in allpgs if p.closer and not p.closer_last),
            f"Pages over 450 lines: " + ", ".join(f"`{p.key}` ({p.lines})" for p in sorted(allpgs, key=lambda p: -p.lines) if p.lines > 450),
            f"Second person anywhere in the opening: {sum(1 for p in allpgs if p.opening_second_person)} of {len(allpgs)}; "
            f"myth tables: {sum(1 for p in allpgs if any(s.myth for s in p.sections))}; "
            f"the number device: {sum(sum(s.number_devices for s in p.sections) for p in allpgs)} uses on "
            f"{sum(1 for p in allpgs if sum(s.number_devices for s in p.sections))} pages; "
            f"pages with more than three lists: {sum(1 for p in allpgs if len(p.all_lists()) > 3)}."]
    return "\n".join(out) + "\n"


def twins_md(parsed: dict, pages: dict) -> str:
    groups, near = twins(parsed)
    out = ["# Skeleton twins — pages whose H2 spines are the same sequence of tokens", "",
           "Tokens: cast · trace (the literal heading) · q (the closer) · look · seq / flow / state / class / svg (a section whose first figure is that type) · p (prose only). "
           "A page is not done until it reads differently from its neighbours (`TEMPLATE.md`); a pair inside one part is the finding, a pair across parts is worth a look.", "",
           f"## {len(groups)} identical groups", ""]
    for sig, ks in groups:
        parts = {pages[k][0] for k in ks}
        out.append(f"- `{' '.join(sig)}` — " + ", ".join(f"`{k}`" for k in ks) + (" — **within one part**" if len(parts) == 1 else ""))
    within = [(a, b) for a, b in near if pages[a][0] == pages[b][0]]
    out += ["", f"## {len(within)} pairs one edit apart within one part (five sections or more)", "",
            f"Across parts there are {len(near) - len(within)} more, not listed: on a ten-token alphabet a cross-part "
            "near-miss is usually two prose pages of the same length, and the rule is about a page's neighbours.", ""]
    for a, b in within:
        out.append(f"- `{a}` (`{' '.join(parsed[a].signature)}`) ↔ `{b}` (`{' '.join(parsed[b].signature)}`)")
    return "\n".join(out) + "\n"


def slots_md(parsed: dict) -> str:
    ranked = sorted(parsed.values(), key=lambda p: (-len(p.slots()), -p.lines))
    out = ["| page | lines | slots | which |", "|---|---:|---:|---|"]
    for p in ranked[:40]:
        out.append(f"| `{p.key}` | {p.lines} | {len(p.slots())} | {', '.join(p.slots())} |")
    return "\n".join(out) + "\n"


# --- the probe -----------------------------------------------------------------------------------

PROBE_PAGE = """# The probe

> Verified against **Minecraft 26.2** · Part IV · a synthetic page.

You place a block and it vanishes. The server has not answered yet; the
client already drew it. **The block you saw was never there.**

## The cast

| class | what it decides | thread |
|---|---|---|
| `A` | one | Server |
| `B` | two | Render |
| `C` | three | Server |

## The trace: one block

```mermaid
sequenceDiagram
    participant A as A
    participant B as B
    A->>B: hello
    Note over A: a later tick
    Note over B: the next tick
```

Prose under the trace.

## A long section

""" + "\n".join(f"Line {i} of prose that goes on." for i in range(45)) + """

## Lists

- one
- two
- three
- four
- five
- six
- seven
- eight. This item has one sentence. And a second. And a third.

**Four** — things counted here.

## Questions players ask

**Why?** Because.

**Names to look for.** Not a question.

**When?** Then.

**Why is my *entities/* folder empty?** Because.

> **For a 1.21-era reader.** A name moved.
> Second line.

## Where to look

`A.a` · `B.b` · `C.c` · `D`
"""

PROBE_LANDING = """# IV · The probe part

> Verified against **Minecraft 26.2** · Part IV · a synthetic landing page.

The part argues one thing. A player recognises this part by its symptom: a
chunk that loads late, a light that lags. It is the argument's last sentence.

## The shape of the part

A conveyor.

## Before you start

[Anatomy](../anatomy/anatomy.md).

## Watch in this order

1. one
2. two
3. three

## Where the part stops

About 40% of those lines are named on no page.

## Reference this part uses

[Threads](../../reference/threads.md).
"""


def probe() -> int:
    pg = parse_text(PROBE_PAGE, "world/probe", "systems/world/probe.md", "world", 4)
    checks = [
        ("the opening is found after the verified line", pg.opening.startswith("You place a block")),
        ("the opening is in the second person and ends on bold", pg.opens_second_person and pg.opening_ends_bold and not pg.opening_ends_dash),
        ("the spine has six sections in order", [s.title for s in pg.sections][:3] == ["The cast", "The trace: one block", "A long section"]),
        ("the signature tokenises cast, trace, prose, closer and look", pg.signature == ("cast", "trace", "p", "p", "q", "look")),
        ("the cast has three rows", pg.cast_rows == 3),
        ("the trace heading is literal", pg.trace_heading is not None and pg.trace_heading.title == "The trace: one block"),
        ("the sequence figure and its two tick bars are counted", pg.figures == ["seq"] and pg.sections[1].tick_bars == 2),
        ("a section over forty lines with no figure or H3 is flagged", [s.title for s in pg.long_sections()] == ["A long section"]),
        ("a list of eight with one long item is measured", pg.sections[3].lists == [(pg.sections[3].lists[0][0], 8, 1)]),
        ("the number device is counted", pg.sections[3].number_devices == 1),
        ("the closer is last, canonical, three questions of four lead-ins", pg.closer is not None and pg.closer_last
         and pg.closer.title == CANON_CLOSER and pg.closer.questions == 3 and pg.closer.leads == 4),
        ("a lead-in with nested italics still matches the question test",
         bool(QMARK.match("**Why is my *entities/* folder empty?**")) and not QMARK.match("**Names to look for.**")),
        ("the 1.21 blockquote is two lines at the foot", pg.blockquote is not None and pg.blockquote[2] == 2 and pg.blockquote[3]),
        ("Where to look counts four names", pg.look_names == 4),
        ("the slots are counted", set(pg.slots()) == {"closer", "trace heading", "1.21 blockquote", "bold ending", "second person", "the number"}),
    ]
    import tempfile
    d = tempfile.mkdtemp()
    p = os.path.join(d, "README.md")
    with open(p, "w", encoding="utf-8") as f:
        f.write(PROBE_LANDING)
    global SRC
    old = SRC
    SRC = d
    try:
        land = landing("probe/README", {"probe/README": ("probe", 4, "README.md")})
    finally:
        SRC = old
        os.unlink(p)
        os.rmdir(d)
    checks += [
        ("the landing page's seventh section is found with its position", len(land.seventh) == 1 and land.seventh[0][0] == "Where the part stops"
         and "after *Watch in this order*, before *Reference this part uses*" in land.seventh[0][1]),
        ("the recognition sentence is found across a line wrap and is not the argument's last sentence",
         land.recognition is not None and land.recognition[0] == 5 and land.recognition[1] is False),
        ("lines outside the watch order exclude the watch section", land.watch_lines == 6 and land.outside == land.lines - 6),
        ("a hand-counted percentage is flagged", len(land.hand_counted) == 1 and "40%" in land.hand_counted[0][1]),
        ("no includes on the probe", not land.size_include and not land.coverage_include),
    ]
    a = parse_text(PROBE_PAGE, "x/a", "systems/x/a.md", "x", 1)
    b = parse_text(PROBE_PAGE.replace("## A long section", "## Another"), "y/b", "systems/y/b.md", "y", 2)
    c = parse_text(PROBE_PAGE.replace("## Lists\n", "## Lists\n\n```mermaid\nflowchart TD\n  A --> B\n```\n"), "x/c", "systems/x/c.md", "x", 1)
    groups, near = twins({"x/a": a, "y/b": b, "x/c": c})
    checks += [
        ("two pages with the same spine are an identical group", groups == [(a.signature, ["x/a", "y/b"])]),
        ("a page one token different is a near pair with both", sorted(near) == [("x/a", "x/c"), ("x/c", "y/b")]),
    ]
    bad = [n for n, ok in checks if not ok]
    for n, ok in checks:
        print(f"  {'ok ' if ok else 'BAD'} {n}")
    if bad:
        print("PROBE FAILED")
        return 1
    print("probe: OK")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pages", nargs="*", help="part/slug")
    ap.add_argument("--part", help="a part directory under src/systems")
    ap.add_argument("--summary", action="store_true")
    ap.add_argument("--twins", action="store_true")
    ap.add_argument("--landing", action="store_true")
    ap.add_argument("--slots", action="store_true")
    ap.add_argument("--probe", action="store_true")
    args = ap.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if args.probe:
        return probe()
    pages = queue.corpus_pages()
    parsed = {k: parse(k, pages) for k in system_pages(pages)}
    if args.summary:
        print(summary_md(parsed, pages))
    if args.twins:
        print(twins_md(parsed, pages))
    if args.slots:
        print(slots_md(parsed))
    if args.landing:
        for k in landing_pages(pages):
            print(landing_md(landing(k, pages)))
    if args.part:
        print(part_table_md(args.part, parsed, pages))
        lk = f"{args.part}/README"
        if lk in pages:
            print(landing_md(landing(lk, pages)))
    for p in args.pages:
        p = re.sub(r"\.md$", "", re.sub(r"^(?:src/)?(?:systems/)?", "", p.replace("\\", "/")))
        if p not in pages:
            sys.exit(f"unknown page {p!r}")
        if p.endswith("/README"):
            print(landing_md(landing(p, pages)))
        else:
            print(report_md(parsed[p] if p in parsed else parse(p, pages)))
    if not (args.summary or args.twins or args.slots or args.landing or args.part or args.pages):
        ap.print_help()
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
