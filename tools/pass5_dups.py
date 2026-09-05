#!/usr/bin/env python3
"""Where the book explains one thing twice: page pairs ranked by what they share.

Pass 5's first job is ownership — every mechanism explained in one place — and
its charter asks for a duplication finder so the sessions start from a list
rather than from memory. Two signals, read off every hand-kept page (the system
pages, the hand-kept Reference pages, the atlas prose, the introduction and
the lecture map; generated pages excepted):

  names      the backticked identifiers two pages share, weighted by rarity: a
             name on forty pages is vocabulary (`ServerLevel`), a name on two is
             a mechanism both pages explain. A pair's score is the sum of
             1/(pages carrying it) over the names it shares, over names carried
             by at most --max-df pages (default 6). `Class.member` counts as
             itself and as its class.
  sentences  near-duplicate sentences across pages: two sentences sharing at
             least --shingles word 6-grams (default 2) after markdown is
             stripped. This is what catches the lattice fact stated three times.

Both are hints, not verdicts: a shared rare name may be a link (good) or a
second explanation (the finding); the session reads both pages. `--terms`
answers the through-line question the other way round: given a set of names
or phrases, which pages carry them and in which sentences.

Usage:
    python tools/pass5_dups.py --summary                 # the top pairs corpus-wide
    python tools/pass5_dups.py --page world/lighting      # one page: its pairs, the shared names, the twin sentences
    python tools/pass5_dups.py --part world --out DIR     # one <slug>.dups.md per page of the part
    python tools/pass5_dups.py --terms "tickChildren,tick phase,the first flush"   # a through-line's pages
"""
from __future__ import annotations

import argparse
import os
import re
import sys
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import claims                 # noqa: E402
import pass4_queue as queue   # noqa: E402
from verify_names import TICK, GENERATED_MARK  # noqa: E402

ROOT = queue.ROOT
SRC = queue.SRC

STOP = set("""a an the and or of to in on for by with as at from is are was were be been it its this that these those
which who whom what when where how not no nor but so if then than into out up down over under one two three four
five six seven eight nine ten there here also only every each all any some more most less very just do does did
done has have had having can could will would should may might must own same other another such after before
because while whether about between through during without within against page part lecture book""".split())


def hand_kept_pages() -> dict:
    """key -> (part dir, part number, rel path) for every hand-kept page."""
    pages = queue.corpus_pages()
    out = {}
    for key, (part, num, rel) in pages.items():
        path = os.path.join(SRC, rel)
        with open(path, encoding="utf-8") as f:
            head = f.read(2000)
        if GENERATED_MARK in head:
            continue
        out[key] = (part, num, rel)
    return out


def names_of(path: str) -> Counter:
    with open(path, encoding="utf-8") as f:
        text = f.read()
    c: Counter = Counter()
    for m in TICK.finditer(text):
        name = m.group(1).rstrip("*").split("(")[0]
        if "/" in name or name.endswith((".py", ".js", ".sh", ".md", ".json", ".txt")):
            continue
        c[name] += 1
        if "." in name:
            c[name.split(".")[0]] += 1
    return c


def normalise(sentence: str) -> list[str]:
    s = sentence.lower()
    s = re.sub(r"`([^`]*)`", r"\1", s)
    s = re.sub(r"\*+|_{2,}", "", s)
    s = re.sub(r"[^a-z0-9.\s-]", " ", s)
    return [w for w in s.split() if w and w not in STOP]


def shingles(words: list[str], k: int = 5) -> set[tuple]:
    return {tuple(words[i:i + k]) for i in range(len(words) - k + 1)}


SUMMARISERS = re.compile(r"/README$|^lectures$|^introduction$|^reference/glossary$|^reference/README$|^maps/README$")


def is_summariser(key: str) -> bool:
    """A landing page, the lecture map, the glossary or the introduction restating a page is a
    summariser echoing its page — drift, not duplication — and the report says which."""
    return bool(SUMMARISERS.search(key))


def sentences(path: str) -> list[tuple[int, str]]:
    return [(line, s) for line, kind, s in claims.sentences_of(path) if kind == "prose" and len(s.split()) >= 8]


class Corpus:
    def __init__(self, max_df: int, min_shingles: int, gram: int = 5, pages: dict | None = None):
        self.pages = hand_kept_pages() if pages is None else pages
        self.max_df = max_df
        self.min_shingles = min_shingles
        self.gram = gram
        self.names = {k: names_of(os.path.join(SRC, v[2])) for k, v in self.pages.items()}
        self.df: Counter = Counter()
        for c in self.names.values():
            self.df.update(c.keys())
        self.sents = {k: sentences(os.path.join(SRC, v[2])) for k, v in self.pages.items()}
        self._twins = None

    def rare(self, name: str) -> bool:
        return 1 < self.df[name] <= self.max_df

    def pair_score(self, a: str, b: str) -> tuple[float, list[tuple[str, int]]]:
        shared = [(n, self.df[n]) for n in self.names[a] if n in self.names[b] and self.rare(n)]
        shared.sort(key=lambda x: (x[1], x[0]))
        return sum(1.0 / d for _n, d in shared), shared

    def pairs_for(self, key: str, top: int = 8):
        rows = []
        for other in self.pages:
            if other == key:
                continue
            score, shared = self.pair_score(key, other)
            if shared:
                rows.append((score, other, shared))
        rows.sort(key=lambda r: -r[0])
        return rows[:top]

    def all_pairs(self, top: int = 60):
        keys = list(self.pages)
        rows = []
        for i, a in enumerate(keys):
            for b in keys[i + 1:]:
                score, shared = self.pair_score(a, b)
                if shared:
                    rows.append((score, a, b, shared))
        rows.sort(key=lambda r: -r[0])
        return rows[:top]

    def twins(self):
        """[(page a, line a, sentence a, page b, line b, sentence b, shared shingles)] across pages."""
        if self._twins is not None:
            return self._twins
        index: dict[tuple, list[tuple[str, int]]] = defaultdict(list)
        texts: dict[tuple[str, int], str] = {}
        sh: dict[tuple[str, int], set] = {}
        for key, rows in self.sents.items():
            for line, s in rows:
                w = normalise(s)
                g = shingles(w, self.gram)
                if not g:
                    continue
                texts[(key, line)] = s
                sh[(key, line)] = g
                for x in g:
                    index[x].append((key, line))
        pair_count: Counter = Counter()
        for x, owners in index.items():
            if len(owners) > 12:
                continue   # a boilerplate phrase (the rules footer) is not a duplicate
            for i, a in enumerate(owners):
                for b in owners[i + 1:]:
                    if a[0] != b[0]:
                        pair_count[(a, b)] += 1
        out = []
        for (a, b), n in pair_count.items():
            if n >= self.min_shingles:
                out.append((a[0], a[1], texts[a], b[0], b[1], texts[b], n))
        out.sort(key=lambda r: (-r[6], r[0], r[1]))
        self._twins = out
        return out

    def twins_for(self, key: str):
        rows = []
        for a, la, sa, b, lb, sb, n in self.twins():
            if a == key:
                rows.append((la, sa, b, lb, sb, n))
            elif b == key:
                rows.append((lb, sb, a, la, sa, n))
        rows.sort(key=lambda r: (r[0], -r[5]))
        return rows

    def render_page(self, key: str) -> str:
        part, num, rel = self.pages[key]
        out = [f"# Shared with other pages — `src/{rel}`", "",
               "Two signals: the rare backticked names this page shares with each other page (a name on at most "
               f"{self.max_df} pages), ranked; then sentences here that near-duplicate a sentence elsewhere. "
               "A shared name may be a link, which is fine, or a second explanation, which is the finding; read both pages.",
               "", "## Pages this one shares the most rare names with", ""]
        pairs = self.pairs_for(key)
        if not pairs:
            out.append("- (none: every name on this page is either unique to it or corpus-wide vocabulary)")
        for score, other, shared in pairs:
            names = ", ".join(f"`{n}`" + ("" if d == 2 else f" ({d})") for n, d in shared[:14])
            more = "" if len(shared) <= 14 else f", … {len(shared) - 14} more"
            out.append(f"- **`{other}`** (score {score:.2f}, {len(shared)} shared) — {names}{more}")
        out += ["", "## Sentences that near-duplicate a sentence on another page", ""]
        tw = self.twins_for(key)
        if not tw:
            out.append("- (none above the threshold)")
        for la, sa, b, lb, sb, n in tw[:25]:
            echo = " (a summariser restating this page — check it has not drifted)" if is_summariser(b) else ""
            out.append(f"- L{la}: {sa}")
            out.append(f"  ↔ `{b}`:{lb}{echo}: {sb}")
        return "\n".join(out) + "\n"

    def render_summary(self, top: int) -> str:
        out = [f"# Page pairs sharing the most rare names (a name on at most {self.max_df} pages)", ""]
        for score, a, b, shared in self.all_pairs(top):
            names = ", ".join(f"`{n}`" for n, _d in shared[:10])
            out.append(f"- {score:.2f}  `{a}` ↔ `{b}` ({len(shared)}): {names}")
        tw = self.twins()
        echo = [t for t in tw if is_summariser(t[0]) or is_summariser(t[3])]
        out += ["", f"# Cross-page near-duplicate sentences ({len(tw)} pairs at ≥ {self.min_shingles} shared "
                    f"{self.gram}-grams, {len(echo)} of them a summariser echoing its page; top {top} of the rest)", ""]
        for a, la, sa, b, lb, sb, n in [t for t in tw if t not in echo][:top]:
            out.append(f"- {n} · `{a}`:{la} ↔ `{b}`:{lb}")
            out.append(f"  {sa}")
            out.append(f"  {sb}")
        return "\n".join(out) + "\n"

    def render_terms(self, terms: list[str]) -> str:
        """Pages carrying any of the terms — a backticked name, or a phrase matched case-insensitively in prose."""
        pats = []
        for t in terms:
            t = t.strip()
            if not t:
                continue
            if re.fullmatch(r"[A-Za-z_][A-Za-z0-9_.$]*", t) and (t[0].isupper() or "." in t):
                pats.append((t, re.compile(r"`" + re.escape(t) + r"(?:[.(*`])")))
            else:
                pats.append((t, re.compile(re.escape(t), re.I)))
        out = [f"# Through-line: {', '.join(t for t, _p in pats)}", ""]
        rows = []
        for key, (part, num, rel) in self.pages.items():
            with open(os.path.join(SRC, rel), encoding="utf-8") as f:
                text = f.read()
            hits = {t: len(p.findall(text)) for t, p in pats}
            total = sum(hits.values())
            if total:
                rows.append((total, num, key, hits))
        rows.sort(key=lambda r: (-r[0], r[1], r[2]))
        out.append(f"{len(rows)} pages carry at least one of the terms; by count:")
        out.append("")
        for total, num, key, hits in rows:
            out.append(f"- **`{key}`** ({total}): " + ", ".join(f"{t} ×{n}" for t, n in hits.items() if n))
        out += ["", "## The sentences, on the pages that carry the terms most", ""]
        for total, num, key, hits in rows[:12]:
            out.append(f"### `{key}`")
            for line, kind, s in claims.sentences_of(os.path.join(SRC, self.pages[key][2])):
                if any(p.search(s) or p.search("`" + s + "`") for _t, p in pats):
                    out.append(f"- L{line}: {s}")
            out.append("")
        return "\n".join(out) + "\n"


def probe() -> int:
    """Two synthetic pages that share two rare names and a paraphrased sentence rank first; a third
    that shares only corpus-wide vocabulary does not pair with them; a summariser echo is labelled."""
    import tempfile
    global SRC
    old = SRC
    with tempfile.TemporaryDirectory() as tmp:
        SRC = tmp
        os.makedirs(os.path.join(tmp, "systems", "p"))
        w = lambda rel, text: open(os.path.join(tmp, rel), "w", encoding="utf-8").write(text)
        w("systems/p/a.md", "# A\n\nThe `Widget.spin` call runs on the Server thread and `Gadget` waits for it, "
                            "which is why the block comes back and vanishes again after the tick ends.\n\n`ServerLevel` is everywhere.\n")
        w("systems/p/b.md", "# B\n\nBecause `Widget.spin` runs on the Server thread while `Gadget` waits, "
                            "the block comes back and vanishes again after the tick ends, every time.\n\n`ServerLevel` is everywhere.\n")
        w("systems/p/c.md", "# C\n\nNothing here but `ServerLevel`, which is everywhere, and a sentence of its own.\n")
        w("systems/p/README.md", "# P\n\nThe block comes back and vanishes again after the tick ends, says page A.\n")
        pages = {"p/a": ("p", 1, "systems/p/a.md"), "p/b": ("p", 1, "systems/p/b.md"),
                 "p/c": ("p", 1, "systems/p/c.md"), "p/README": ("p", 1, "systems/p/README.md")}
        c = Corpus(max_df=2, min_shingles=2, pages=pages)
        pairs = c.all_pairs()
        twins = c.twins()
        page_report = c.render_page("p/a")
    SRC = old
    checks = [
        ("a ↔ b is the top pair on the two rare names", bool(pairs) and {pairs[0][1], pairs[0][2]} == {"p/a", "p/b"}
         and {n for n, _d in pairs[0][3]} == {"Widget.spin", "Widget", "Gadget"}),
        ("c pairs with nobody (ServerLevel is on every page)", not any("p/c" in (p[1], p[2]) for p in pairs)),
        ("the paraphrased sentence is caught as a twin", any({t[0], t[3]} == {"p/a", "p/b"} for t in twins)),
        ("the landing page's echo is labelled a summariser", "summariser" in page_report),
    ]
    for name, ok in checks:
        print(f"  {'ok ' if ok else 'BAD'} {name}")
    if not all(ok for _n, ok in checks):
        print("PROBE FAILED")
        return 1
    print("probe: OK")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--probe", action="store_true", help="prove the tool on synthetic pages")
    ap.add_argument("--summary", action="store_true", help="the top pairs and twin sentences corpus-wide")
    ap.add_argument("--page", nargs="*", default=[], help="part/slug — one page's report")
    ap.add_argument("--part", help="every page of a part (a directory under src/systems, or reference, or frame)")
    ap.add_argument("--out", help="write one <slug>.dups.md per page here")
    ap.add_argument("--terms", help="comma-separated names or phrases: which pages carry them (the through-line question)")
    ap.add_argument("--max-df", type=int, default=6, help="a name on more pages than this is vocabulary, not a duplicate")
    ap.add_argument("--shingles", type=int, default=2, help="shared word n-grams for two sentences to count as twins")
    ap.add_argument("--gram", type=int, default=5, help="the n of the n-gram")
    ap.add_argument("--top", type=int, default=60)
    args = ap.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    if args.probe:
        return probe()
    corpus = Corpus(args.max_df, args.shingles, args.gram)
    if args.terms:
        print(corpus.render_terms(args.terms.split(",")))
        return 0
    if args.summary:
        print(corpus.render_summary(args.top))
        return 0
    keys = []
    for p in args.page:
        p = re.sub(r"\.md$", "", re.sub(r"^(?:src/)?(?:systems/)?", "", p.replace("\\", "/")))
        if p not in corpus.pages:
            sys.exit(f"unknown page {p!r}")
        keys.append(p)
    if args.part:
        keys += [k for k, (part, _n, _r) in corpus.pages.items() if part == args.part]
    if not keys:
        ap.print_help()
        return 2
    if args.out:
        os.makedirs(args.out, exist_ok=True)
    for key in keys:
        text = corpus.render_page(key)
        if args.out:
            with open(os.path.join(args.out, f"{key.replace('/', '--')}.dups.md"), "w", encoding="utf-8") as f:
                f.write(text)
            print(f"{len(corpus.pairs_for(key)):2d} pairs {len(corpus.twins_for(key)):3d} twin sentences  {key}")
        else:
            print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
