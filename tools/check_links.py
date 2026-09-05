#!/usr/bin/env python3
"""Every internal link, anchor and include in the corpus resolves.

Pass 5's charter (job 2, the seams) asks for a link checker over every internal
link and anchor, a tool in pass 5 and a gate by pass 10. This walks `src/**/*.md`
(the generated atlas tables excepted — they carry no links) and checks:

  link     `[text](target.md)` and `[text](target.md#anchor)` — the target file
           exists, relative to the page (or to the including page, for a file
           under src/figures/ that reaches the site only through {{#include}}).
           Matched against the whole page outside its fences, not line by line,
           because the corpus hard-wraps and a link's text often crosses a
           newline; a link is reported on the line its `[` sits on
  html     `<a href="…">` inside HTML blocks (figcaptions) — a `.html` target
           maps back to a `.md` that exists
  anchor   `#anchor`, on the same page or another — a heading on the target page
           slugifies to it the way mdBook does (lower-case; letters, digits, `_`
           and `-` kept; whitespace to `-`; everything else dropped; a repeated
           id gets `-1`, `-2`, …), after inline markdown is stripped
  include  `{{#include path}}` — the file exists
  summary  every page under src/ that SUMMARY.md does not list, and every entry
           in SUMMARY.md with no file (an unlisted page is not built)
  redirect every `[output.html.redirect]` target in book.toml resolves to a page

External links (http, https, mailto) are counted and not fetched. Exit 1 on any
failure; `--quiet` prints failures only; `--page` restricts the walk while
drafting. `--inbound PAGE` prints every page that links to PAGE with the sentence
the link sits in, which is the seams report a pass-5 session reads.

Usage:
    python tools/check_links.py
    python tools/check_links.py --quiet
    python tools/check_links.py --inbound src/systems/world/tickets-and-loading.md
"""
from __future__ import annotations

import argparse
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "src")

LINK = re.compile(r"(?<!\!)\[([^\]]*)\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
HTML_HREF = re.compile(r"<a\s+[^>]*href=\"([^\"]+)\"")
INCLUDE = re.compile(r"\{\{#include\s+([^}]+?)\s*\}\}")
HEADING = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
CUSTOM_ID = re.compile(r"\s*\{#([^}]+)\}\s*$")
EXTERNAL = ("http://", "https://", "mailto:")


def read(path: str) -> str:
    with open(path, encoding="utf-8") as f:
        return f.read()


def strip_inline(text: str) -> str:
    """Heading text as mdBook sees it before slugifying: no code spans, emphasis, links or tags."""
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"`([^`]*)`", r"\1", text)
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)
    text = text.replace("*", "")                                        # emphasis marks
    text = re.sub(r"(?<!\w)_{1,2}(\S(?:.*?\S)?)_{1,2}(?!\w)", r"\1", text)  # _emphasis_, but not set_count
    return text


def slug(text: str) -> str:
    out = []
    for ch in text:
        if ch.isalnum() or ch in "_-":
            out.append(ch.lower())
        elif ch.isspace():
            out.append("-")
    return "".join(out)


def outside_fences(text: str):
    """(line number, line) for every line not inside a ``` fence."""
    fence = False
    for i, line in enumerate(text.split("\n"), 1):
        if line.startswith("```"):
            fence = not fence
            continue
        if not fence:
            yield i, line


def prose_of(text: str) -> tuple[str, list[int]]:
    """The page outside its fences as one string, with the source line of every character.

    Links are matched against this rather than line by line: the corpus hard-wraps its
    prose, so `[tickets and<newline>loading](...)` is a link no line-by-line scan can see.
    243 of the corpus's 7,811 links were wrapped that way when this was written, and one
    of them was broken, which is how the blind spot was found.
    """
    buf: list[str] = []
    line_of: list[int] = []
    for i, line in outside_fences(text):
        buf.append(line)
        buf.append("\n")
        line_of.extend([i] * (len(line) + 1))
    line_of.append(line_of[-1] if line_of else 1)
    return "".join(buf), line_of


def anchors_of(path: str, cache: dict) -> set[str]:
    if path in cache:
        return cache[path]
    seen: dict[str, int] = {}
    ids: set[str] = set()
    for _n, line in outside_fences(read(path)):
        m = HEADING.match(line)
        if not m:
            continue
        title = m.group(2)
        cm = CUSTOM_ID.search(title)
        if cm:
            base = cm.group(1)
        else:
            base = slug(strip_inline(title))
        n = seen.get(base, 0)
        ids.add(base if n == 0 else f"{base}-{n}")
        seen[base] = n + 1
    # mdBook also gives every heading's id to the page; an empty anchor means the page top
    cache[path] = ids
    return ids


def corpus_pages() -> list[str]:
    out = []
    for dp, _dn, files in os.walk(SRC):
        for f in files:
            if f.endswith(".md"):
                rel = os.path.relpath(os.path.join(dp, f), SRC).replace(os.sep, "/")
                if not rel.startswith("generated/"):
                    out.append(rel)
    return sorted(out)


def summary_pages() -> list[str]:
    text = read(os.path.join(SRC, "SUMMARY.md"))
    return [m.group(2) for m in LINK.finditer(text)]


def resolve(page_rel: str, target: str) -> str | None:
    """A link target as a path under src (with .html mapped back to .md), or None if external/empty."""
    if not target or target.startswith("#") or target.startswith(EXTERNAL):
        return None
    t = target.split("#", 1)[0]
    if t.endswith(".html"):
        t = t[:-5] + ".md"
    if t.endswith("/"):
        t = t + "README.md"
    base = os.path.dirname(os.path.join(SRC, page_rel))
    return os.path.normpath(os.path.join(base, t))


def sentence_around(line: str, m: re.Match) -> str:
    starts = [x.end() for x in re.finditer(r"[.!?]\s", line[:m.start()])]
    s = starts[-1] if starts else 0
    em = re.search(r"[.!?](?:\s|$)", line[m.end():])
    e = m.end() + em.end() if em else len(line)
    return re.sub(r"\s+", " ", re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", line[s:e])).strip()


def paragraph_lines(text: str):
    """Join wrapped paragraph lines so a sentence that wraps across lines is one string."""
    para: list[tuple[int, str]] = []
    for n, line in outside_fences(text):
        if line.strip() == "" or line.lstrip().startswith(("|", "{{#include")):
            if para:
                yield para[0][0], " ".join(l.strip() for _n, l in para)
                para = []
            if line.lstrip().startswith("|"):
                yield n, line
            continue
        para.append((n, line))
    if para:
        yield para[0][0], " ".join(l.strip() for _n, l in para)


def check(pages: list[str], quiet: bool, toml: str | None = None) -> tuple[list[str], dict]:
    fails: list[str] = []
    stats = {"links": 0, "anchors": 0, "includes": 0, "external": 0, "html": 0}
    anchor_cache: dict = {}
    all_pages = set(corpus_pages())
    toml = os.path.join(ROOT, "book.toml") if toml is None else toml
    includers: dict[str, list[str]] = {}   # figures/x.md -> pages that include it

    # first pass: includes, so a figure file's links can be judged from its includer
    for rel in pages:
        for m in INCLUDE.finditer(read(os.path.join(SRC, rel))):
            target = m.group(1).strip()
            path = os.path.normpath(os.path.join(os.path.dirname(os.path.join(SRC, rel)), target))
            stats["includes"] += 1
            if not os.path.exists(path):
                fails.append(f"{rel}: include {target} does not exist")
            else:
                trel = os.path.relpath(path, SRC).replace(os.sep, "/")
                includers.setdefault(trel, []).append(rel)

    for rel in pages:
        if rel == "SUMMARY.md":
            continue   # checked both ways below
        # a file that only reaches the site through {{#include}} has its links resolved from each includer
        contexts = includers.get(rel, [rel]) if rel.startswith("figures/") else [rel]
        text = read(os.path.join(SRC, rel))
        prose, line_of = prose_of(text)
        hits = [(m.start(), m.group(2), "link") for m in LINK.finditer(prose)]
        hits += [(m.start(), m.group(1), "html") for m in HTML_HREF.finditer(prose)]
        for at, target, kind in sorted(hits):
            n = line_of[at]
            if True:
                if target.startswith(EXTERNAL):
                    stats["external"] += 1
                    continue
                stats["links" if kind == "link" else "html"] += 1
                for ctx in contexts:
                    if target.startswith("#"):
                        path = os.path.join(SRC, ctx)
                    else:
                        path = resolve(ctx, target)
                    if path is None:
                        continue
                    if not os.path.exists(path):
                        where = rel if ctx == rel else f"{rel} (included by {ctx})"
                        fails.append(f"{where}:{n}: {kind} {target} — no such file")
                        continue
                    if "#" in target:
                        anchor = target.split("#", 1)[1]
                        stats["anchors"] += 1
                        if anchor and not path.endswith(".md"):
                            continue
                        if anchor and anchor not in anchors_of(path, anchor_cache):
                            where = rel if ctx == rel else f"{rel} (included by {ctx})"
                            near = sorted(anchors_of(path, anchor_cache), key=lambda a: -len(os.path.commonprefix([a, anchor])))[:3]
                            fails.append(f"{where}:{n}: anchor #{anchor} is not a heading on {os.path.relpath(path, SRC).replace(os.sep, '/')} (nearest: {', '.join(near)})")

    # SUMMARY.md both ways
    listed = summary_pages()
    for p in listed:
        if not os.path.exists(os.path.join(SRC, p)):
            fails.append(f"SUMMARY.md lists {p}, which does not exist")
    unlisted = sorted(all_pages - set(listed) - {"SUMMARY.md"} - {p for p in all_pages if p.startswith("figures/")})
    for p in unlisted:
        fails.append(f"{p} is not in SUMMARY.md (an unlisted page is not built)")

    # book.toml redirects
    if toml and os.path.exists(toml):
        in_redirect = False
        for n, line in enumerate(read(toml).split("\n"), 1):
            if line.strip().startswith("["):
                in_redirect = line.strip() == "[output.html.redirect]"
                continue
            if not in_redirect or not line.strip() or line.strip().startswith("#"):
                continue
            m = re.match(r"\s*\"([^\"]+)\"\s*=\s*\"([^\"]+)\"", line)
            if not m:
                continue
            src_html, dst = m.group(1), m.group(2)
            base = os.path.dirname(os.path.join(SRC, src_html.lstrip("/")))
            dst_md = dst[:-5] + ".md" if dst.endswith(".html") else dst
            if dst_md.endswith("/"):
                dst_md += "README.md"
            path = os.path.normpath(os.path.join(base, dst_md))
            if not os.path.exists(path):
                fails.append(f"book.toml:{n}: redirect {src_html} -> {dst} lands on no page")
    return fails, stats


def inbound(target_rel: str):
    """Every page linking to target_rel, with the sentence each link sits in."""
    target = os.path.normpath(os.path.join(SRC, target_rel))
    rows = []
    for rel in corpus_pages():
        if rel == target_rel or rel == "SUMMARY.md":
            continue
        text = read(os.path.join(SRC, rel))
        if rel.startswith("reference/") and "Do not edit by hand" in text[:400]:
            continue   # a generated index links every page; that is not a seam
        for n, line in paragraph_lines(text):
            for m in LINK.finditer(line):
                path = resolve(rel, m.group(2))
                if path and os.path.normpath(path) == target:
                    anchor = m.group(2).split("#", 1)[1] if "#" in m.group(2) else ""
                    rows.append((rel, n, anchor, sentence_around(line, m)))
    return rows


def probe() -> int:
    """The tool fails on what it should: a missing file, a missing anchor, a missing include, a
    SUMMARY entry with no file, an unlisted page, a redirect to nowhere, and a bad anchor on a
    link whose text is wrapped across a newline — and passes the rest, including an anchor with
    an underscore in it and a link that reaches a page through an include.

    The wrapped case is the one that matters: the tool scanned line by line until 2026-09-05 and
    could not see a wrapped link at all, so 243 of the corpus's links had never been checked and
    one was broken. A probe that only ever writes links on one line proves nothing about a book
    that hard-wraps its prose."""
    import tempfile
    global SRC
    old = SRC
    with tempfile.TemporaryDirectory() as tmp:
        SRC = os.path.join(tmp, "src")
        os.makedirs(os.path.join(SRC, "figures"))
        os.makedirs(os.path.join(SRC, "systems", "p"))
        w = lambda rel, text: open(os.path.join(SRC, rel), "w", encoding="utf-8").write(text)
        w("SUMMARY.md", "- [a](a.md)\n- [b](systems/p/b.md)\n- [ghost](ghost.md)\n")
        w("a.md", "# A\n\n[ok](systems/p/b.md) [ok](systems/p/b.md#one-set_count-under-two) "
                  "[bad](systems/p/b.md#nope) [gone](nope.md) {{#include figures/f.md}} {{#include figures/none.md}}\n"
                  "<a href=\"systems/p/b.html\">html</a> [ext](https://example.org)\n\n"
                  "A wrapped link the old line-by-line scan could not see: [one good\n"
                  "wrapped](systems/p/b.md#dup) and [one bad\n"
                  "wrapped](systems/p/b.md#wrapped-nope).\n")
        w("systems/p/b.md", "# B\n\n## One `set_count` under _two_\n\n## Dup\n\n## Dup\n\n[up](../../a.md#a) [dup](#dup-1)\n")
        w("figures/f.md", "[from a figure](systems/p/b.md)\n")
        w("orphan.md", "# not in SUMMARY\n")
        toml = os.path.join(tmp, "book.toml")
        open(toml, "w").write('[output.html.redirect]\n"/old.html" = "a.html"\n"/older.html" = "zzz.html"\n')
        fails, stats = check(corpus_pages(), True, toml)
    SRC = old
    want = ["anchor #nope", "nope.md — no such file", "include figures/none.md", "SUMMARY.md lists ghost.md",
            "orphan.md is not in SUMMARY.md", "redirect /older.html", "anchor #wrapped-nope"]
    missed = [x for x in want if not any(x in f for f in fails)]
    extra = [f for f in fails if not any(x in f for x in want)]
    for f in fails:
        print("  " + f)
    if missed or extra:
        print(f"PROBE FAILED — not caught: {missed}; false alarms: {extra}")
        return 1
    print(f"probe: {len(fails)} failures caught, none false; {stats['links']} links, {stats['anchors']} anchors checked. OK")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--quiet", action="store_true", help="failures only")
    ap.add_argument("--page", nargs="*", help="restrict to these pages (paths under src or absolute)")
    ap.add_argument("--inbound", help="print every page that links to this page, with the sentence")
    ap.add_argument("--probe", action="store_true", help="prove the tool fails on the constructs it should")
    args = ap.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    if args.probe:
        return probe()
    if args.inbound:
        rel = os.path.relpath(os.path.abspath(args.inbound), SRC).replace(os.sep, "/")
        rows = inbound(rel)
        print(f"# Inbound links — `src/{rel}` ({len(rows)} links from {len({r[0] for r in rows})} pages)\n")
        for prel, n, anchor, sent in rows:
            a = f" #{anchor}" if anchor else ""
            print(f"- `{prel}`:{n}{a} — {sent}")
        return 0

    pages = corpus_pages()
    if args.page:
        want = {os.path.relpath(os.path.abspath(p), SRC).replace(os.sep, "/") for p in args.page}
        pages = [p for p in pages if p in want]
    fails, stats = check(pages, args.quiet)
    if not args.quiet:
        print(f"checked {stats['links']} links, {stats['html']} html hrefs, {stats['anchors']} anchors, "
              f"{stats['includes']} includes on {len(pages)} pages; {stats['external']} external links not fetched")
    print(f"== {len(fails)} failure(s)")
    for f in fails:
        print("  " + f)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
