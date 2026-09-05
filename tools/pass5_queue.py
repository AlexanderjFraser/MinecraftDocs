#!/usr/bin/env python3
"""The passes-5-to-8 queue (docs/pass5.md), routed by kind and by page.

`docs/pass5.md` is one file four passes draw on, and its preface says which pass
takes which kind of entry: a structural finding is pass 5's (the book), a
page-shape finding pass 6's (the lecture), a figure finding pass 7's, wording
debt pass 8's. The file was written by twenty sessions in prose, not tagged, so
this reads it into units the way `pass4_queue.py` reads pass4.md — a heading, or
a list item with its continuation lines, or a paragraph — attributes each unit
to the pages it names, and guesses each unit's kind from two things:

  the section  the nearest enclosing heading or bold lead-in ("**Structural
               findings, not acted on.**", "### Wording the close rewrote") sets
               a prior for everything under it
  the words    a keyword score per kind over the unit's own text

An explicit tag wins over both: put `[kind=book]`, `[kind=lecture]`,
`[kind=figure]` or `[kind=voice]` anywhere in a unit (or `[kind=5]` … `[kind=8]`)
and that is its kind. A unit whose guess is a tie or has no evidence is printed
with `?` so a session can tag it. Struck units (`~~…~~`) are settled and are
listed only with --settled.

Usage:
    python tools/pass5_queue.py --summary                         # units by kind × part; how many are guesses
    python tools/pass5_queue.py --kind book --part world           # pass 5's entries for Part IV, per page
    python tools/pass5_queue.py --kind book --part world --out DIR # one <slug>.queue.md per page, plus _part-notes.md
    python tools/pass5_queue.py --kind book world/lighting         # one page
    python tools/pass5_queue.py --unsure                           # every unit whose kind is a guess, to tag
"""
from __future__ import annotations

import argparse
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pass4_queue as q   # noqa: E402

QUEUE = os.path.join(q.ROOT, "docs", "pass5.md")
NUMERAL = {v: k for k, v in q.ROMAN.items()}
KINDS = ("book", "lecture", "figure", "voice")
PASS_OF = {"book": 5, "lecture": 6, "figure": 7, "voice": 8}
KIND_OF_PASS = {str(v): k for k, v in PASS_OF.items()}
TAG = re.compile(r"\[kind=(book|lecture|figure|voice|[5-8])\]")

# the words that decide a kind, scored per unit; the section prior breaks ties
WORDS = {
    "book": re.compile(
        r"\bstructural\b|\bnot acted on\b|cross-link|\bcoverage\b|\bcompleteness\b|two subjects|duplicat|\boverlap|"
        r"\bbelongs? (?:on|in|to|with|here|beside)\b|\bmoves? (?:to|into)\b|\bmoved\b|\bhome\b|\bowns?\b|\bowner\b|"
        r"\blanding page\b|\bmerge|\bsplit\b|\bseam\b|both explain|stated .{0,20}times|said twice|re-explain|"
        r"\bdependency\b|\bdependants?\b|\bforward reference\b|\bsecond edition\b|no page|nowhere in the corpus|"
        r"\bstates? it\b|\bsection or a page\b|\bown page\b|\brename|\breference (?:page|table|entry|row)\b|"
        r"\bwatch(?:ed)? (?:in|order)\b|\bnamed only\b|\bthree pages\b|\btwo pages\b|\bboth pages\b|\bdisagree", re.I),
    "lecture": re.compile(
        r"\bcloser\b|questions players ask|questions a |\bskeleton|\bsection order\b|\bdevice\b|\bslot\b|\bend on\b|\bends on\b|"
        r"\bcut\b|\bcuts\b|\blength\b|lines against|\blist in prose\b|\bbullet|\bthe trace:|\bsecond person\b|"
        r"\bbrief\b|\bshape\b|\bopens? (?:with|in|on)\b|\bheading\b|\bsubsection\b|\bcast table\b|\bcast\b|"
        r"\bmyth table\b|\bblockquote\b|1\.21-era reader|\bfor a 1\.21\b|\btable or two\b|\bone table\b|\btwo tables\b|"
        r"\bwatched\b|\bwhere to look\b|\bopening paragraph\b|\bthe opening\b|\bdigression\b|\baside\b", re.I),
    "figure": re.compile(
        r"\bfigure|\bdiagram|\bflowchart|\barrow|\bedge|\bnode|\blane|\blabel|\bmermaid\b|\bsequence\b|"
        r"\bstate diagram\b|\bdense|\bsubgraph|\bredraw|\bcaption|\bstateDiagram|\bparticipant|\bswimlane|\bsvg\b|\brender(?:ed|s)?\b", re.I),
    "voice": re.compile(
        r"\bwording\b|\bre-read\b|\bvoice\b|\bhook\b|\bsentence|\btic\b|\btics\b|\bhedge|\bem dash|\bem-dash|"
        r"\brhythm\b|\breads\b|\bcount\b|\bnumber\b|\bterminolog|\bglossary\b|\btypeset|\bword\b|\bwords\b|"
        r"\bphrase|\bclause|\bparagraph .{0,30}long|\blongest\b|\bwordier|\bflabb|\bscans\b|\bcadence\b|\bregister\b|"
        r"\bqualifier|\bcorrection (?:written|in the voice)|\bpunchline\b|\bsuperlative\b|\bambigu|\bcolloquial|\btitle\b|"
        r"\bcosmetic\b|\breflow\b|\bwrap\b|\bruns long\b", re.I),
}
SECTION_PRIOR = [
    (re.compile(r"structural|not acted on|completeness|coverage|cross-link|blind spots|generators", re.I), "book"),
    (re.compile(r"wording|re-read|voice|hook|rewrote|rewritten|counts? that|ambiguit|terminology|glossary|headword|small\.", re.I), "voice"),
    (re.compile(r"closer|device|skeleton|shape|cuts?\b|length|lecture order", re.I), "lecture"),
    (re.compile(r"figure|diagram|arrow", re.I), "figure"),
]


def kind_of(unit: q.Unit, prior: str | None) -> tuple[str, bool]:
    """(kind, sure). An explicit tag is sure; else the word score, the section prior breaking ties."""
    m = TAG.search(unit.text)
    if m:
        k = m.group(1)
        return (KIND_OF_PASS.get(k, k), True)
    text = unit.text
    scores = {k: len(WORDS[k].findall(text)) for k in KINDS}
    # the closer device is pass 6's whatever else the unit says about it
    if re.search(r"questions players ask|questions a |\bcloser device\b", text, re.I):
        scores["lecture"] += 2
    best = max(scores.values())
    if best == 0:
        return (prior or "book", False)
    top = [k for k, v in scores.items() if v == best]
    if len(top) == 1:
        # a clear margin is sure; a one-hit lead with a different prior is not
        second = sorted(scores.values())[-2]
        sure = best - second >= 2 or (prior == top[0]) or (prior is None and best >= 3)
        return (top[0], sure)
    if prior in top:
        return (prior, False)
    return (top[0], False)


def section_prior(text: str) -> str | None:
    for pat, kind in SECTION_PRIOR:
        if pat.search(text):
            return kind
    return None


def classify(units: list[q.Unit]) -> dict[int, tuple[str, bool]]:
    """unit line -> (kind, sure), with the section prior carried from headings and bold lead-ins."""
    out = {}
    prior_stack: list[tuple[int, str | None]] = []   # (level, prior) for headings
    lead_prior: str | None = None                      # from the last bold lead-in paragraph at list level
    for u in units:
        if u.level <= 6:
            prior_stack = [(lvl, p) for lvl, p in prior_stack if lvl < u.level]
            p = section_prior(u.text)
            prior_stack.append((u.level, p))
            lead_prior = None
            out[u.line] = (p or "book", p is not None) if p else ("book", False)
            continue
        first = u.text.strip().lstrip("-* ").strip()
        lead = re.match(r"\*\*(.+?)\*\*", first)
        if lead:
            # a bold lead-in ("**Structural findings, not acted on.**") sets the prior for the unit
            # that carries it and for what follows it, until the next heading
            lp = section_prior(lead.group(1))
            if lp:
                lead_prior = lp
        prior = lead_prior or next((p for _l, p in reversed(prior_stack) if p), None)
        out[u.line] = kind_of(u, prior)
    return out


def probe() -> int:
    """The tool routes by tag, by section and by words, and drops a struck entry."""
    import tempfile
    global QUEUE
    old = QUEUE
    with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False, encoding="utf-8") as f:
        f.write("# probe\n\n## Session Z — Part IV (pass 4)\n\n"
                "**Structural findings, not acted on.**\n\n"
                "- `lighting` and `chunk-anatomy` both explain the same thing.\n"
                "- ~~`lighting`'s hook was rewritten; re-read it.~~\n"
                "- `lighting`'s flowchart has sixteen edges and wants redrawing. [kind=voice]\n\n"
                "### Wording to re-read\n\n"
                "- `chunk-storage`'s hook is now three sentences.\n"
                "- `chunk-storage`'s sequence figure gained a lane and a dashed arrow. [kind=7]\n")
        QUEUE = f.name
    try:
        pages, units, standing, kinds = load()
        def kinds_for(key, kind):
            return [u.line for u in units_for(units, kinds, key, pages[key][1], kind, False)[0]]
        checks = [
            ("section prior routes the first bullet to book", kinds_for("world/lighting", "book") == [7]),
            ("a struck entry is dropped", 8 not in kinds_for("world/lighting", None)),
            ("an explicit tag beats the words (figure words, tagged voice)", kinds_for("world/lighting", "voice") == [9]),
            ("the heading prior routes wording debt to voice", kinds_for("world/chunk-storage", "voice") == [13]),
            ("a numeric tag maps to its pass", kinds_for("world/chunk-storage", "figure") == [14]),
            ("chunk-anatomy is named by the shared bullet", 7 in kinds_for("world/chunk-anatomy", "book")),
        ]
    finally:
        QUEUE = old
        os.unlink(f.name)
    bad = [name for name, ok in checks if not ok]
    for name, ok in checks:
        print(f"  {'ok ' if ok else 'BAD'} {name}")
    if bad:
        print("PROBE FAILED")
        return 1
    print("probe: OK")
    return 0


def load():
    q.QUEUE = QUEUE
    pages = q.corpus_pages()
    units, standing = q.read_units()
    q.attribute(units, pages)
    kinds = classify(units)
    return pages, units, standing, kinds


def units_for(units, kinds, key: str, part_num: int, kind: str | None, settled: bool):
    mine = [u for u in units if (key in u.pages or u.owner == key) and (settled or not u.struck)
            and (kind is None or kinds[u.line][0] == kind) and u.level >= 99]
    partwide = [u for u in units if not u.pages and u.owner is None and u.level >= 99
                and part_num in (u.session_parts or (0,)) and (settled or not u.struck)
                and (kind is None or kinds[u.line][0] == kind)]
    return mine, partwide


def render(u: q.Unit, kinds) -> str:
    kind, sure = kinds[u.line]
    tag = f"[{kind}{'' if sure else '?'}]"
    body = "\n  ".join(l.strip() for l in u.text.split("\n"))
    body = re.sub(r"^[-*]\s+", "", body)
    return f"- **pass5.md:{u.line}** {tag} (session {u.session}) {body}"


def checklist(key: str, pages, units, kinds, kind: str | None, settled: bool) -> str:
    part, num, path = pages[key]
    mine, partwide = units_for(units, kinds, key, num, kind, settled)
    out = [f"# Pass-{PASS_OF.get(kind, '5–8')} queue — `src/{path}`", "",
           f"Part {num or '—'} ({part}). {len(mine)} open {kind or 'queue'} entr{'y' if len(mine) == 1 else 'ies'} name this page. "
           "Every entry is checked against the page before it is acted on — passes 5 to 7 rewrite what this file "
           "describes, and an entry already overtaken is struck with a word saying so. A `?` marks a kind the tool "
           "guessed; tag the entry in pass5.md with `[kind=…]` if it guessed wrong.", "",
           "## Entries that name this page", ""]
    out += [render(u, kinds) for u in mine] or ["- (none)"]
    return "\n".join(out) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pages", nargs="*", help="part/slug")
    ap.add_argument("--part", help="a part directory under src/systems, or reference, or frame")
    ap.add_argument("--kind", choices=KINDS, help="book (pass 5) · lecture (6) · figure (7) · voice (8); default all")
    ap.add_argument("--out", help="write one <slug>.queue.md per page here, plus _part-notes.md")
    ap.add_argument("--settled", action="store_true", help="include struck units")
    ap.add_argument("--summary", action="store_true")
    ap.add_argument("--unsure", action="store_true", help="every unit whose kind is a guess")
    ap.add_argument("--probe", action="store_true", help="prove the routing on a synthetic queue")
    args = ap.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    if args.probe:
        return probe()
    pages, units, standing, kinds = load()
    content = [u for u in units if u.level >= 99 and not u.struck]

    if args.summary:
        print("| part | book (5) | lecture (6) | figure (7) | voice (8) | of which guessed |")
        print("|---|---:|---:|---:|---:|---:|")
        rows = {}
        for u in content:
            num = None
            if u.pages:
                num = pages[next(iter(u.pages))][1]
            elif u.owner:
                num = pages[u.owner][1]
            elif u.session_parts:
                num = u.session_parts[0]
            num = num or 0
            r = rows.setdefault(num, {"book": 0, "lecture": 0, "figure": 0, "voice": 0, "guess": 0})
            k, sure = kinds[u.line]
            r[k] += 1
            r["guess"] += 0 if sure else 1
        tot = {"book": 0, "lecture": 0, "figure": 0, "voice": 0, "guess": 0}
        for num in sorted(rows):
            r = rows[num]
            for k in tot:
                tot[k] += r[k]
            print(f"| {NUMERAL.get(num, 'frame/ref')} | {r['book']} | {r['lecture']} | {r['figure']} | {r['voice']} | {r['guess']} |")
        print(f"| **total** | {tot['book']} | {tot['lecture']} | {tot['figure']} | {tot['voice']} | {tot['guess']} |")
        named = sum(1 for u in content if u.pages or u.owner)
        print(f"\n{len(content)} open units; {named} name a page; {len(content) - named} are part-wide or preamble.")
        return 0

    if args.unsure:
        for u in content:
            k, sure = kinds[u.line]
            if not sure:
                print(render(u, kinds)[:300])
        return 0

    keys = []
    for p in args.pages:
        p = re.sub(r"\.md$", "", re.sub(r"^(?:src/)?(?:systems/)?", "", p.replace("\\", "/")))
        if p not in pages:
            sys.exit(f"unknown page {p!r}")
        keys.append(p)
    if args.part:
        keys += [k for k, (part, _n, _p) in pages.items() if part == args.part]
    if not keys:
        ap.print_help()
        return 2
    if args.out:
        os.makedirs(args.out, exist_ok=True)
    nums = set()
    for key in keys:
        nums.add(pages[key][1])
        text = checklist(key, pages, units, kinds, args.kind, args.settled)
        if args.out:
            with open(os.path.join(args.out, f"{key.replace('/', '--')}.queue.md"), "w", encoding="utf-8") as f:
                f.write(text)
            mine, _pw = units_for(units, kinds, key, pages[key][1], args.kind, args.settled)
            print(f"{len(mine):3d} entries  {key}")
        else:
            print(text)
    if args.out:
        notes = []
        for num in sorted(nums):
            _m, partwide = units_for(units, kinds, "", num, args.kind, args.settled)
            if partwide:
                notes.append(f"## Part {num or 'frame/reference'} — {len(partwide)} entr{'y' if len(partwide) == 1 else 'ies'} naming no page\n")
                notes += [render(u, kinds) for u in partwide]
                notes.append("")
        with open(os.path.join(args.out, "_part-notes.md"), "w", encoding="utf-8") as f:
            f.write("# Queue entries from this part's sessions that name no page — route each to a page, or to the landing page\n\n"
                    + "\n".join(notes))
        print(f"\npart-wide entries -> {os.path.join(args.out, '_part-notes.md')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
