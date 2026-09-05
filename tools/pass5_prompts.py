#!/usr/bin/env python3
"""One prompt file per page for pass 5's agents — the reader of the book.

Each file is the agent brief (Part 1 of `docs/pass5-brief.md`), then what the
tools know about the page: its pass-5 queue entries (`pass5_queue.py --kind
book`), the pages it shares the most rare names with and its twin sentences
(`pass5_dups.py`), every page that links to it with the sentence the link sits
in and every page it links out to (`check_links.py`), and which of the book's
through-lines it carries (the THROUGH_LINES below, refined by session A). The
part's coverage report (`pass5_coverage.py`) is written once per part as
`_part-coverage.md`, and the queue's part-wide entries as `_part-notes.md`;
both are the session's to route, not the agent's. The agent's own prompt is
then one line: read this file and do what it says.

Usage:
    python tools/pass5_prompts.py --part world --out DIR
    python tools/pass5_prompts.py world/lighting blocks/block-entities --out DIR
`--part frame` covers the introduction, the lecture map and the atlas prose;
`--part reference` the hand-kept Reference pages.
"""
from __future__ import annotations

import argparse
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check_links                  # noqa: E402
import map_source                   # noqa: E402
import pass4_queue as queue         # noqa: E402
import pass5_coverage as coverage   # noqa: E402
import pass5_dups as dups           # noqa: E402
import pass5_queue as p5q           # noqa: E402

ROOT = queue.ROOT
SRC = queue.SRC
BRIEF = os.path.join(ROOT, "docs", "pass5-brief.md")

# The through-lines: the ideas that cross parts and are told at full length once (pass 5, job 3).
# Each is a name and the terms that betray a retelling — a backticked identifier, or a phrase
# matched case-insensitively. Session A refines this list with `pass5_dups.py --terms` in hand
# and records the owner page of each in the brief.
THROUGH_LINES = {
    "the tick and its phases": ["MinecraftServer.tickChildren", "MinecraftServer.tickServer", "tick phase",
                                "first flush", "second flush", "ServerLevel.tick", "chunk-source phase", "connection phase"],
    "the four threads": ["Server thread", "Render thread", "Netty event loop", "Util.backgroundExecutor",
                         "worker pool", "Worker-Main", "BlockableEventLoop"],
    "the wire and the hop": ["Connection.channelRead0", "PacketProcessor", "the hop", "PacketUtils.ensureRunningOnSameThread",
                             "game thread", "off the Netty thread"],
    "authority and prediction": ["Entity.isLocalInstanceAuthoritative", "Entity.canSimulateMovement",
                                 "Player.isClientAuthoritative", "authoritative", "predicts", "prediction"],
    "the registry freeze and the reload": ["MappedRegistry.freeze", "the freeze", "frozen", "/reload",
                                           "ReloadableServerResources", "ReloadableServerRegistries", "PreparableReloadListener"],
    "the data-driven type pattern": ["data-driven type", "the type field", "Registry.byNameCodec", "MapCodec.dispatch",
                                     "Codec.dispatch", "registry data packs cannot extend"],
    "the ledger": ["BlockStatePredictionHandler", "ledger", "ClientboundBlockChangedAckPacket", "endPredictionsUpTo", "sequence number"],
}


def brief_part1() -> str:
    with open(BRIEF, encoding="utf-8") as f:
        text = f.read()
    m = re.search(r"^## Part 1 — The brief.*?(?=^---\s*$\s*^## Part 2)", text, re.M | re.S)
    if not m:
        sys.exit("docs/pass5-brief.md: could not find Part 1 (the brief) — is the heading intact?")
    return m.group(0).strip()


def through_lines_for(path: str) -> list[tuple[str, dict]]:
    with open(path, encoding="utf-8") as f:
        text = f.read()
    out = []
    for name, terms in THROUGH_LINES.items():
        hits = {}
        for t in terms:
            if re.fullmatch(r"[A-Za-z_][A-Za-z0-9_.$/]*", t) and (t[0].isupper() or "." in t):
                n = len(re.findall(r"`" + re.escape(t) + r"(?:[.(*`])", text))
            else:
                n = len(re.findall(re.escape(t), text, re.I))
            if n:
                hits[t] = n
        if hits:
            out.append((name, hits))
    return out


def outbound(rel: str) -> list[tuple[str, str, str]]:
    """(target key, anchor, sentence) for every internal link out of the page."""
    text = check_links.read(os.path.join(SRC, rel))
    rows = []
    for n, line in check_links.paragraph_lines(text):
        for m in check_links.LINK.finditer(line):
            path = check_links.resolve(rel, m.group(2))
            if not path or not os.path.exists(path):
                continue
            key = os.path.relpath(path, SRC).replace("\\", "/")[:-3]
            key = re.sub(r"^systems/", "", key)
            anchor = m.group(2).split("#", 1)[1] if "#" in m.group(2) else ""
            rows.append((key, anchor, check_links.sentence_around(line, m)))
    return rows


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pages", nargs="*", help="part/slug")
    ap.add_argument("--part", help="a part directory under src/systems, or frame, or reference")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    pages, units, standing, kinds = p5q.load()
    corpus = dups.Corpus(max_df=6, min_shingles=2)

    keys: list[str] = []
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

    os.makedirs(args.out, exist_ok=True)
    brief = brief_part1()
    part_dirs, part_nums = set(), set()
    for key in keys:
        part, num, rel = pages[key]
        path = os.path.join(SRC, rel)
        if key not in corpus.pages:
            print(f"  skip (generated)      {key}")
            continue
        part_dirs.add(part)
        part_nums.add(num)
        mine, _pw = p5q.units_for(units, kinds, key, num, "book", False)
        inbound = check_links.inbound(rel)
        out_links = outbound(rel)
        tl = through_lines_for(path)

        out = [f"# Pass-5 read — `src/{rel}`", "",
               f"The page to read is **`src/{rel}`** (repository root: `{ROOT}`). It is in Part {num or '—'} ({part}); "
               f"the part's other pages are under `src/systems/{part}/`, and the pages this one shares the most with are named below.",
               "", brief, "", "---", "",
               p5q.checklist(key, pages, units, kinds, "book", False),
               "---", "",
               corpus.render_page(key),
               "---", "",
               f"# Links into and out of `{key}`", "",
               f"## {len(inbound)} inbound links from {len({r[0] for r in inbound})} pages (the sentence each sits in)", ""]
        out += [f"- `{prel}`:{n}{(' #' + a) if a else ''} — {s}" for prel, n, a, s in inbound] or ["- (no page links here)"]
        out += ["", f"## {len(out_links)} outbound links", ""]
        out += [f"- → `{k}`{(' #' + a) if a else ''} — {s}" for k, a, s in out_links] or ["- (none)"]
        out += ["", "---", "", "# Through-lines this page carries", ""]
        if tl:
            out += [f"- **{name}**: " + ", ".join(f"{t} ×{n}" for t, n in hits.items()) for name, hits in tl]
        else:
            out.append("- (none of the seven, by their terms)")
        fname = os.path.join(args.out, f"{key.replace('/', '--')}.prompt.md")
        with open(fname, "w", encoding="utf-8") as f:
            f.write("\n".join(out) + "\n")
        print(f"{len(mine):3d} queue {len(corpus.pairs_for(key)):2d} pairs {len(inbound):3d} in {len(out_links):3d} out  {fname}")

    # once per part: the coverage report and the part-wide queue entries
    files = None
    for d in sorted(part_dirs):
        if not any(pd == d for pd, _n, _t, _s in map_source.PARTS):
            continue
        if files is None:
            files = map_source.load()
            ticks, figs = coverage.page_names()
        text, _st = coverage.report(files, d, ticks, figs, 80)
        with open(os.path.join(args.out, f"_part-coverage-{d}.md"), "w", encoding="utf-8") as f:
            f.write(text)
        print(f"\ncoverage → {os.path.join(args.out, f'_part-coverage-{d}.md')}")
    notes = []
    for num in sorted(part_nums):
        _m, partwide = p5q.units_for(units, kinds, "", num, "book", False)
        if partwide:
            notes.append(f"## Part {num or 'frame/reference'} — {len(partwide)} entr{'y' if len(partwide) == 1 else 'ies'} naming no page\n")
            notes += [p5q.render(u, kinds) for u in partwide]
            notes.append("")
    with open(os.path.join(args.out, "_part-notes.md"), "w", encoding="utf-8") as f:
        f.write("# Pass-5 queue entries from this part's sessions that name no page — route each to a page, or to the landing page\n\n"
                + "\n".join(notes))
    print(f"part-wide notes → {os.path.join(args.out, '_part-notes.md')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
