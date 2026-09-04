#!/usr/bin/env python3
"""Every pass4.md note that names a page, collected into that page's opening checklist.

`docs/pass4.md` is the queue pass 4 works from: per pass-3 session, every claim
the rewrite introduced. It is 2,700 lines in two formats (`## Session X` blocks
with `### page` sub-headings; top-level `- **date, session X — Part N**` bullets
with nested bullets), and a note about a page can sit under any session, not
only the part's own. The charter says "grep it"; this is the grep, done once
and the same way for every session.

The file is cut into *units*: a heading, or a list item at any depth together
with its continuation lines. A unit belongs to a page when it names the page
as `` `slug` ``, `part/slug` or `slug.md`; a heading that names a page owns
every unit beneath it until the next heading of the same or higher level; a
unit that names no page belongs to the session's part(s), read off the
session heading ("Part IV", "Parts I · II"). Units whose first line is struck
(`~~ … ~~`) are settled and are listed only with --settled. *Standing items*
are printed for every query because they apply to every page.

Usage:
    python tools/pass4_queue.py world/tickets-and-loading          # one page, to stdout
    python tools/pass4_queue.py --part world                       # every page of Part IV, plus the landing page and part-wide notes
    python tools/pass4_queue.py --part world --out DIR             # one checklist file per page under DIR
    python tools/pass4_queue.py --summary                          # how many open units name each page (the corpus-wide view)
Pages are given as `part/slug`, `src/systems/part/slug.md`, or `reference/slug`.
"""
from __future__ import annotations

import argparse
import os
import re
import sys
from dataclasses import dataclass, field

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QUEUE = os.path.join(ROOT, "docs", "pass4.md")
SRC = os.path.join(ROOT, "src")

ROMAN = {"I": 1, "II": 2, "III": 3, "IV": 4, "V": 5, "VI": 6, "VII": 7, "VIII": 8, "IX": 9,
         "X": 10, "XI": 11, "XII": 12, "XIII": 13, "XIV": 14}

HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")
BULLET_RE = re.compile(r"^(\s*)[-*]\s+(.*)$")
STRUCK_RE = re.compile(r"^\s*(?:[-*]\s+|#{1,6}\s+)?~~")
SESSION_RE = re.compile(r"[Ss]ession\s+([A-P])\b")
INLINE_PAGE_RE = re.compile(r"^\s*(?:\*\*)?`[a-z0-9][a-z0-9/-]*`(?:\*\*)?\s*(?:—|-|:)")
PART_RE = re.compile(r"\bParts?\s+((?:[IVX]+(?:\s*[·,]\s*(?:and\s+)?)?)+)")


@dataclass
class Unit:
    line: int
    level: int            # heading level (1-6) or 100 + indent for list items
    text: str
    struck: bool
    session: str
    session_parts: tuple
    pages: set = field(default_factory=set)   # slugs this unit names directly
    owner: str | None = None                   # slug owned via an enclosing page heading


def parts_in(text: str) -> tuple:
    found = []
    for m in PART_RE.finditer(text):
        for r in re.findall(r"[IVX]+", m.group(1)):
            if r in ROMAN:
                found.append(ROMAN[r])
    return tuple(sorted(set(found)))


def corpus_pages() -> dict:
    """slug -> (part slug, part number, relative path). Reference pages have part 0."""
    pages = {}
    for part in sorted(os.listdir(os.path.join(SRC, "systems"))):
        d = os.path.join(SRC, "systems", part)
        if not os.path.isdir(d):
            continue
        readme = os.path.join(d, "README.md")
        num = 0
        if os.path.exists(readme):
            with open(readme, encoding="utf-8") as f:
                first = f.readline()
            m = re.match(r"#\s+([IVX]+)\s", first)
            if m:
                num = ROMAN.get(m.group(1), 0)
        for name in sorted(os.listdir(d)):
            if name.endswith(".md"):
                slug = name[:-3]
                pages[f"{part}/{slug}"] = (part, num, f"systems/{part}/{name}")
    refdir = os.path.join(SRC, "reference")
    for name in sorted(os.listdir(refdir)):
        if name.endswith(".md"):
            pages[f"reference/{name[:-3]}"] = ("reference", 0, f"reference/{name}")
    for name in ("introduction", "lectures"):
        if os.path.exists(os.path.join(SRC, name + ".md")):
            pages[name] = ("frame", 0, name + ".md")
    mapsdir = os.path.join(SRC, "maps")
    if os.path.isdir(mapsdir):
        for name in sorted(os.listdir(mapsdir)):
            if name.endswith(".md"):
                pages[f"maps/{name[:-3]}"] = ("frame", 0, f"maps/{name}")
    return pages


# Pages pass 3 split or renamed: a note written under the old name belongs to the new page(s).
ALIASES = {
    "world/game-events-and-vibrations": ["game-events-and-poi"],
    "world/points-of-interest": ["game-events-and-poi"],
    "world/scheduled-ticks": ["block-ticks-and-fluids"],
    "world/fluids": ["block-ticks-and-fluids"],
    "player/hunger-and-experience": ["hunger-xp-and-effects"],
    "player/status-effects": ["hunger-xp-and-effects"],
    "rendering/visibility-and-the-frame-graph": ["level-rendering"],
    "rendering/section-meshing": ["level-rendering"],
    "reference/level-data-and-rules": ["level-data-and-rules"],
}


def page_patterns(pages: dict) -> dict:
    """slug key -> compiled pattern that matches the page being named in prose."""
    pats = {}
    for key, (part, _num, _path) in pages.items():
        slug = key.split("/", 1)[1] if "/" in key else key
        alts = [rf"`{re.escape(slug)}`", rf"`{re.escape(key)}`", rf"`{re.escape(key)}\.md`",
                rf"\b{re.escape(key)}\.md\b", rf"`{re.escape(slug)}\.md`"]
        for old in ALIASES.get(key, []):
            alts += [rf"`{re.escape(old)}`", rf"`{re.escape(old)}\.md`"]
        if key in ("introduction", "lectures"):
            alts.append(rf"\b{slug}\.md\b")
        if slug == "README":
            alts.append(rf"`{re.escape(part)}/README(?:\.md)?`")
        pats[key] = re.compile("|".join(alts))
    return pats


def read_units() -> tuple[list[Unit], list[str]]:
    with open(QUEUE, encoding="utf-8") as f:
        lines = f.read().split("\n")
    units: list[Unit] = []
    standing: list[str] = []
    session, session_parts = "?", ()
    in_standing = False
    cur: Unit | None = None
    for i, raw in enumerate(lines, 1):
        h = HEADING_RE.match(raw)
        b = BULLET_RE.match(raw)
        if h:
            title = h.group(2)
            in_standing = title.strip().lower().startswith("standing items")
            if len(h.group(1)) <= 2:
                m = SESSION_RE.search(title)
                if m:
                    session, session_parts = m.group(1), parts_in(title)
            cur = Unit(i, len(h.group(1)), raw, bool(STRUCK_RE.match(raw)), session, session_parts)
            units.append(cur)
            continue
        if in_standing:
            standing.append(raw)
        if b:
            indent = len(b.group(1).expandtabs(4))
            if indent == 0:
                m = SESSION_RE.search(b.group(2)[:120])
                if m and ("Part" in b.group(2)[:160] or "frame" in b.group(2)[:120] or "maps" in b.group(2)[:120]):
                    session, session_parts = m.group(1), parts_in(b.group(2)[:200])
            cur = Unit(i, 100 + indent, raw, bool(STRUCK_RE.match(raw)), session, session_parts)
            units.append(cur)
            continue
        if raw.strip() == "":
            cur = None                # a blank line ends a list item's or paragraph's continuation
            continue
        if cur is None or cur.level <= 6 or INLINE_PAGE_RE.match(raw):
            # a prose paragraph under a heading, or a continuation line that opens on a page
            # marker (`slug` — …, the style sessions H and I used inside one long bullet): its
            # own unit, at the enclosing list item's level or at "paragraph" level.
            # A unit split out of a *struck* parent inherits the strike: striking a bullet
            # settles the whole bullet, and without this a settled note whose continuation
            # line happens to open on a slug comes back on every later checklist for ever.
            level = cur.level if cur is not None and cur.level >= 99 else 99
            struck = bool(STRUCK_RE.match(raw)) or (cur is not None and cur.struck)
            cur = Unit(i, level, raw, struck, session, session_parts)
            units.append(cur)
        else:
            cur.text += "\n" + raw
    return units, standing


def attribute(units: list[Unit], pages: dict) -> None:
    pats = page_patterns(pages)
    owner_stack: list[tuple[int, str]] = []   # (heading level, slug key)
    for u in units:
        names = {key for key, p in pats.items() if p.search(u.text)}
        if u.level <= 6:
            owner_stack = [(lvl, k) for lvl, k in owner_stack if lvl < u.level]
            if len(names) == 1:
                owner_stack.append((u.level, next(iter(names))))
            elif names:
                u.pages |= names
            continue
        u.pages |= names
        if not names and owner_stack:
            u.owner = owner_stack[-1][1]


def units_for_page(units: list[Unit], key: str, part_num: int, settled: bool) -> tuple[list[Unit], list[Unit]]:
    mine = [u for u in units if (key in u.pages or u.owner == key) and (settled or not u.struck)]
    # a session with no part in its heading (A the frame, B the atlas, O Reference, P the close)
    # is part 0, which is also what the frame, maps and reference pages carry
    partwide = [u for u in units if not u.pages and u.owner is None and u.level >= 99
                and part_num in (u.session_parts or (0,)) and (settled or not u.struck)]
    return mine, partwide


def render(u: Unit) -> str:
    text = u.text
    if u.level <= 6:
        text = text.lstrip("#").strip()
        return f"- **pass4.md:{u.line}** (session {u.session}, heading) {text}"
    body = "\n  ".join(l.strip() for l in text.split("\n"))
    body = re.sub(r"^[-*]\s+", "", body)
    return f"- **pass4.md:{u.line}** (session {u.session}) {body}"


def checklist(key: str, pages: dict, units: list[Unit], standing: list[str], settled: bool, with_partwide: bool) -> str:
    part, num, path = pages[key]
    mine, partwide = units_for_page(units, key, num, settled)
    out = [f"# Pass-4 checklist — `src/{path}`", ""]
    out.append(f"Part {num or '—'} ({part}). {len(mine)} open note(s) name this page; "
               f"{len(partwide)} part-wide note(s) from its sessions. Every line below is a claim "
               f"to falsify and report with the file and line that settles it.")
    out += ["", "## Notes that name this page", ""]
    out += [render(u) for u in mine] or ["- (none — this page has no entry; it still gets the full protocol)"]
    if with_partwide and partwide:
        out += ["", "## Part-wide notes from the sessions that wrote this part", ""]
        out += [render(u) for u in partwide]
    out += ["", "## Standing items (apply to every page)", ""]
    out += [l for l in standing if l.strip()]
    return "\n".join(out) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pages", nargs="*", help="part/slug, src/systems/part/slug.md, reference/slug")
    ap.add_argument("--part", help="a part's directory name under src/systems (e.g. world)")
    ap.add_argument("--out", help="write one <slug>.checklist.md per page here")
    ap.add_argument("--settled", action="store_true", help="include struck-through (settled) units")
    ap.add_argument("--summary", action="store_true", help="open units per page, corpus-wide")
    ap.add_argument("--no-partwide", action="store_true", help="omit the part-wide notes section")
    args = ap.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")   # the queue is UTF-8; Windows consoles default to cp1252

    pages = corpus_pages()
    units, standing = read_units()
    attribute(units, pages)

    if args.summary:
        rows = []
        for key, (part, num, _p) in pages.items():
            mine, _ = units_for_page(units, key, num, args.settled)
            rows.append((num, key, len(mine)))
        for num, key, n in sorted(rows):
            print(f"{n:4d}  {key}")
        orphan = [u for u in units if u.level >= 99 and not u.pages and u.owner is None and not u.struck]
        print(f"\n{len(orphan)} open units name no page (part-wide notes and preambles).")
        return 0

    keys: list[str] = []
    for p in args.pages:
        p = p.replace("\\", "/")
        p = re.sub(r"^(?:src/)?(?:systems/)?", "", p)
        p = re.sub(r"\.md$", "", p)
        if p not in pages:
            sys.exit(f"unknown page {p!r}; pages look like world/tickets-and-loading or reference/threads")
        keys.append(p)
    if args.part:
        keys += [k for k, (part, _n, _p) in pages.items() if part == args.part]
        if not keys:
            sys.exit(f"no part directory {args.part!r} under src/systems (also: frame, reference)")
    if not keys:
        ap.print_help()
        return 2

    if args.out:
        os.makedirs(args.out, exist_ok=True)
    for key in keys:
        text = checklist(key, pages, units, standing, args.settled, not args.no_partwide)
        if args.out:
            slug = key.replace("/", "--")
            with open(os.path.join(args.out, f"{slug}.checklist.md"), "w", encoding="utf-8") as f:
                f.write(text)
            mine, partwide = units_for_page(units, key, pages[key][1], args.settled)
            print(f"{len(mine):3d} notes +{len(partwide):3d} part-wide  {key}")
        else:
            print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
