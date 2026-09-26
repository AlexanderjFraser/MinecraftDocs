#!/usr/bin/env python3
"""The voice, measured: the tics, the hedges, the ambiguous terms and the register devices, per page and per part.

Pass 8's polish (docs/pass8-brief.md, Part 4) is a list of rulings about sentences, and this is the
count behind each one, taken the same way every time so a session starts from the sentences rather
than from memory, and so session A can rule on a tic knowing how many there are. Nothing here is a
gate and nothing here judges a sentence: a count in a queue is a description, not a target, and most
of what this lists is fine where it stands — the session reads each one and keeps the ones that
earn their place.

Per page, read outside code fences (a figure's labels are `pass7_figures.py`'s business), as
sentences with the line they start on:

  not-but      "not X but Y" (not "not only … but")                 the contrast tic pass 2 logged most
  rather       "rather than", "instead of"                          the same tic in its milder spelling
  hedge        "N of the M", "with two exceptions", "all but one", "almost all", "over half", "the other three"
  dash         a sentence with three or more em dashes              the em-dash chain
  correction   "actually", "in fact", "contrary to", "it turns out", "despite its name", "the obvious …"
                                                                    the correction written in the voice of a correction
  dead         "no reader", "nothing reads", "never read", "dead constant"
                                                                    the dead-constant aside
  poss-link    "is [page](…)'s" — the possessive on a link          three readers read it as a typo
  number       the bold-number device, `**Two** — …` (a number word), lines         two readers read it as a fragment
  you-open     the opening paragraph's first sentence addresses you (A1 allows it; a part that mostly does has one way in)
  long         sentences over 45 words                              a pacing signal, not a fault
  rot          a count of classes, files or lines in a sentence     the numbers that rot at the next release
  terms        the words the queue found used in two senses, counted per page (the session reads them for sense):
               ledger, hop, level, phase, batch, context, lane, extract, record, inert, classes, files,
               client thread, Render thread, game thread, main thread, shared worker pool, game time

Usage:
    python tools/pass8_voice.py --summary                    # every page, one row each, and the totals per part
    python tools/pass8_voice.py --part world                 # the rows for one part
    python tools/pass8_voice.py --list hedge --part world    # the sentences, with page and line
    python tools/pass8_voice.py --list terms --part client   # where each ambiguous term is used, per page
    python tools/pass8_voice.py world/lighting               # one page: every kind, every sentence
    python tools/pass8_voice.py --terms                      # glossary headwords the corpus spells two ways (space against hyphen)
    python tools/pass8_voice.py --probe
"""
from __future__ import annotations

import argparse
import os
import re
import sys
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pass8_queue as q8  # noqa: E402

ROOT = q8.HERE
SRC = q8.SRC
GLOSSARY = os.path.join(SRC, "reference", "glossary.md")
NUM = r"(?:one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|twenty|\d+)"
KINDS = {
    "not-but": re.compile(r"\bnot\b(?! only\b)(?! just\b)[^.;:!?]{0,80}?\bbut\b", re.I),
    "rather": re.compile(r"\brather than\b|\binstead of\b", re.I),
    "hedge": re.compile(rf"\b{NUM} of (?:the|its|those|these|them|which|whose)\b|\bwith (?:{NUM}|a few|some) exceptions?\b|"
                        rf"\ball but (?:{NUM})\b|\balmost (?:all|every|none|nothing|always|never)\b|"
                        rf"\b(?:nearly|over|under|about|roughly) (?:all|half|a third|a quarter|two thirds)\b|\bthe other {NUM}\b", re.I),
    "correction": re.compile(r"\bactually\b|\bin fact\b|\bcontrary to\b|\bas it happens\b|\bit turns out\b|\bdespite (?:its|the) name\b|"
                             r"\bnot what (?:you|the name|it looks)\b|\bthe obvious (?:reading|version|answer)\b|\bcounter-?intuitive", re.I),
    "dead": re.compile(r"\bno reader\b|\bnothing (?:in the (?:game|tree|jar|code) )?reads\b|\bnever read\b|\bdead constant\b|"
                       r"\bread(?:s)? (?:it|either|neither) anywhere\b|\bnot read anywhere\b|\bconstant nobody reads\b|\bnobody reads\b", re.I),
    "poss-link": re.compile(r"\]\([^)\n]*\)'s?(?=[\s.,;:)])|\]\([^)\n]*\)'(?=[.,;:])"),
}
TERMS = ["ledger", "hop", "level", "phase", "batch", "context", "lane", "extract", "record", "inert", "classes", "files",
         "client thread", "Render thread", "game thread", "main thread", "shared worker pool", "game time"]
TERM_RE = {t: re.compile(rf"\b{re.escape(t)}s?\b" if " " not in t else rf"\b{re.escape(t)}s?\b", re.I if t[0].islower() else 0) for t in TERMS}
ROT = re.compile(rf"\b(?:{NUM}|hundred|thousand|[\d,]+)\s+(?:classes|files|lines)\b", re.I)
NUMBER_WORDS = ("One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Eleven", "Twelve", "Thirteen",
                "Fourteen", "Fifteen", "Sixteen", "Seventeen", "Eighteen", "Nineteen", "Twenty", "Thirty", "Forty", "Fifty", "Sixty",
                "Seventy", "Eighty", "Ninety", "Hundred", "Half", "Zero", "None", "Once", "Twice")
BOLD_NUMBER = re.compile(r"^\*\*(?:" + "|".join(NUMBER_WORDS) + r")(?:[ -][a-z]+){0,3}\*\* —")  # the number device, not a glossary headword
YOU = re.compile(r"\byou\b|\byour\b|\byourself\b", re.I)
FENCE = re.compile(r"^(```|~~~)")


def read(path: str) -> str:
    with open(path, encoding="utf-8") as f:
        return f.read()


def prose_lines(text: str):
    """(line number, text) for every line outside a code fence, with figure and HTML blocks dropped."""
    out, fence, html = [], False, False
    for i, line in enumerate(text.splitlines(), 1):
        if FENCE.match(line.strip()):
            fence = not fence
            continue
        if fence:
            continue
        s = line.strip()
        if s.startswith("<figure") or s.startswith("{{#include"):
            html = True
        if html:
            if s.startswith("</figure>") or (s.startswith("{{#include") and not s.startswith("<")):
                html = False
            continue
        out.append((i, line))
    return out


def sentences(text: str):
    """(line, sentence) for the prose: paragraphs joined, tables kept as rows, split on sentence ends."""
    out, para, start = [], [], 0
    def flush():
        if para:
            joined = " ".join(p.strip() for p in para)
            for s in re.split(r"(?<=[.!?])\s+(?=[A-Z`*(\[\"“])", joined):
                s = s.strip()
                if s:
                    out.append((start, s))
    for n, line in prose_lines(text):
        s = line.strip()
        if not s or s.startswith("#") or s.startswith("|") or s.startswith("> Verified") or s.startswith("---"):
            flush(); para = []
            if s.startswith("|") and not re.match(r"^\|[-:| ]+\|$", s):
                for cell in s.strip("|").split("|"):
                    if cell.strip():
                        out.append((n, cell.strip()))
            continue
        if not para:
            start = n
        para.append(re.sub(r"^(?:[-*]|\d+\.)\s+|^>\s?", "", s))
    flush()
    return out


def opening(text: str) -> str:
    """The first prose paragraph after the verified line."""
    lines = prose_lines(text)
    seen_verified, para = False, []
    for _n, line in lines:
        s = line.strip()
        if s.startswith("> Verified"):
            seen_verified = True
            continue
        if not seen_verified or s.startswith("#"):
            continue
        if not s:
            if para:
                break
            continue
        para.append(s)
    return " ".join(para)


def measure(path: str) -> dict:
    text = read(path)
    rows = sentences(text)
    hits = defaultdict(list)
    for n, s in rows:
        for kind, rx in KINDS.items():
            if rx.search(s):
                hits[kind].append((n, s))
        if s.count("—") >= 3:
            hits["dash"].append((n, s))
        if len(s.split()) > 45:
            hits["long"].append((n, s))
        if ROT.search(s):
            hits["rot"].append((n, s))
        for t, rx in TERM_RE.items():
            if rx.search(s):
                hits["terms"].append((n, f"[{t}] {s}"))
    for n, line in prose_lines(text):
        if BOLD_NUMBER.match(line.strip()):
            hits["number"].append((n, line.strip()))
    op = opening(text)
    first = re.split(r"(?<=[.!?])\s+", op, 1)[0] if op else ""
    if first and YOU.search(first):
        hits["you-open"].append((1, first))
    counts = Counter({k: len(v) for k, v in hits.items()})
    counts["sentences"] = len(rows)
    counts["words"] = len(re.findall(r"\w+", " ".join(s for _n, s in rows)))
    return {"counts": counts, "hits": hits}


COLS = ["not-but", "rather", "hedge", "dash", "correction", "dead", "poss-link", "number", "you-open", "long", "rot", "terms"]


def corpus_pages(part: str | None = None):
    """(key, rel, part numeral) for every hand-written page: systems, landing pages, hand-kept Reference, the frame and the maps."""
    import claims
    known = q8.pages()
    seen, out = set(), []
    for key, (md, num) in known.items():
        if md in seen or "/" not in key and key not in ("/",):
            continue
        seen.add(md)
        path = os.path.join(SRC, md)
        if not os.path.exists(path) or claims.is_generated(path):
            continue
        d = md.split("/")[1] if md.startswith("systems/") else md.split("/")[0].replace(".md", "")
        if part and d != part and num != part:
            continue
        out.append((key, md, num))
    return sorted(out, key=lambda r: (q8.ORDER.index(r[2]) if r[2] in q8.ORDER else 99, r[1]))


def row(md: str, c: Counter) -> str:
    return "| `" + md.replace("systems/", "") + "` | " + " | ".join(str(c.get(k, 0)) for k in COLS) + f" | {c['sentences']} |"


def header() -> str:
    return "| page | " + " | ".join(COLS) + " | sentences |\n|---|" + "---:|" * (len(COLS) + 1)


def glossary_variants():
    """Multi-word glossary headwords, and every page that spells one with a hyphen where the glossary has a space or the reverse."""
    heads = []
    for line in read(GLOSSARY).splitlines():
        m = re.match(r"^\*\*`?([^*`]+?)`?\*\*", line)
        if m and " " in m.group(1).strip():
            heads.append(m.group(1).strip())
    out = []
    pages = corpus_pages()
    for head in heads:
        spaced = head.lower()
        hyphen = spaced.replace(" ", "-")
        rx_s = re.compile(rf"\b{re.escape(spaced)}\b", re.I)
        rx_h = re.compile(rf"\b{re.escape(hyphen)}\b", re.I)
        s_pages, h_pages = [], []
        for _k, md, _n in pages:
            t = read(os.path.join(SRC, md))
            if rx_s.search(t):
                s_pages.append(md)
            if rx_h.search(t):
                h_pages.append(md)
        if s_pages and h_pages:
            out.append((head, s_pages, h_pages))
    return out


def probe() -> int:
    page = ("# T\n\n> Verified against **Minecraft 0.0** · Part I · a thing.\n\nYou press a key and nothing happens. "
            "The lock is not a mutex but a flag. Five of the seven callers skip it. It is — as it happens — the one that matters — and it "
            "actually reads the field, which nothing reads. It belongs to [the tick](x.md)'s.\n\n```mermaid\nA-->B\n```\n\n"
            "**Two** — writes per tick.\n\nThe package holds forty-two classes. " + "word " * 50 + "end.\n\n| a | b |\n|---|---|\n| the ledger | a hop |\n")
    import tempfile
    with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False, encoding="utf-8") as f:
        f.write(page)
        p = f.name
    try:
        c = measure(p)["counts"]
    finally:
        os.unlink(p)
    want = {"you-open": 1, "not-but": 1, "hedge": 1, "dash": 1, "correction": 1, "dead": 1, "poss-link": 1, "number": 1, "rot": 1, "long": 1}
    bad = {k: (c.get(k, 0), v) for k, v in want.items() if c.get(k, 0) != v}
    if bad or c.get("terms", 0) < 2:
        print(f"probe FAILED: {bad or 'terms'} — counts {dict(c)}")
        return 1
    print("probe ok: each kind found once on a synthetic page, the figure block skipped, the table cells read as terms")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pages", nargs="*", help="part/slug")
    ap.add_argument("--part", help="a part directory under src/systems, or reference, or maps")
    ap.add_argument("--summary", action="store_true")
    ap.add_argument("--list", help="one kind: " + ", ".join(COLS))
    ap.add_argument("--terms", action="store_true", help="glossary headwords spelled two ways")
    ap.add_argument("--probe", action="store_true")
    args = ap.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if args.probe:
        return probe()
    if args.terms:
        for head, s_pages, h_pages in glossary_variants():
            print(f"- **{head}**: with a space on {len(s_pages)} pages, hyphenated on {len(h_pages)}: " +
                  ", ".join(f"`{m.replace('systems/', '')}`" for m in h_pages))
        return 0
    known = q8.pages()
    if args.pages:
        for p in args.pages:
            p = re.sub(r"\.md$", "", re.sub(r"^(?:src/)?(?:systems/)?", "", p.replace("\\", "/")))
            if p not in known:
                sys.exit(f"unknown page {p!r}")
            md = known[p][0]
            m = measure(os.path.join(SRC, md))
            print(f"# `{md}`\n\n{header()}\n{row(md, m['counts'])}\n")
            for kind in COLS:
                if m["hits"].get(kind):
                    print(f"## {kind} ({len(m['hits'][kind])})\n")
                    for n, s in m["hits"][kind]:
                        print(f"- L{n}: {s}")
                    print()
        return 0
    pages = corpus_pages(args.part)
    if args.list:
        if args.list not in COLS:
            sys.exit(f"unknown kind {args.list!r}; one of {', '.join(COLS)}")
        for _k, md, _n in pages:
            hits = measure(os.path.join(SRC, md))["hits"].get(args.list, [])
            if hits:
                print(f"\n### `{md}` — {len(hits)}")
                for n, s in hits:
                    print(f"- L{n}: {s}")
        return 0
    print(header())
    totals = defaultdict(Counter)
    for _k, md, num in pages:
        c = measure(os.path.join(SRC, md))["counts"]
        print(row(md, c))
        totals[num].update(c)
    if not args.part:
        print("\n| part | " + " | ".join(COLS) + " | sentences |\n|---|" + "---:|" * (len(COLS) + 1))
        for num in q8.ORDER:
            if num in totals:
                print(f"| {num} | " + " | ".join(str(totals[num].get(k, 0)) for k in COLS) + f" | {totals[num]['sentences']} |")
        allc = Counter()
        for c in totals.values():
            allc.update(c)
        print("| **all** | " + " | ".join(str(allc.get(k, 0)) for k in COLS) + f" | {allc['sentences']} |")
    return 0


if __name__ == "__main__":
    sys.exit(main())
