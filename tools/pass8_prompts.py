#!/usr/bin/env python3
"""One prompt file per page for pass 8's fact-check agents, and one session file per page beside it.

Pass 8's agent is pass 4's adversary with the decompile (docs/pass8-brief.md, Part 2), and its
prompt file is the brief, then the page's opening checklist: every ledger entry in docs/pass9.md
that names the page (`pass8_queue.py`, oldest pass first, with the session that wrote it), every
question of fact a reader raised about the page and no session answered (`pass5_queue.py`'s
`[kind=fact]` units, added by pass 8's session A — the queue's other kinds are the session's), every
caption on the page (`tools/pass7/captions.py` — a caption is a claim about what its figure shows,
and most were never listed), the figure gate's notes for the page (`check_figure_names.py`: a bare
head or a third class's method on a lane, which is where the caller's-method fault hides), then the
page's confident sentences by category (`claims.py`) and every diagram arrow by arrow
(`diagram_arrows.py`). Everything that is the session's business and not the agent's goes to the
session file, `<part>--<slug>.session.md`: the page's open queue units of every kind
(`pass5_queue.py` — the voice ones are the polish step's list), the voice measure for the page
(`pass8_voice.py`), and every inbound link by anchor (`check_links.py --inbound`). Per part,
`_part-notes.md` carries the ledger's part-wide notes and the queue's, and `_part-voice.md` the
part's voice table. The agent's own prompt is then one line: read this file and do what it says.

Usage:
    python tools/pass8_prompts.py --part world --out DIR
    python tools/pass8_prompts.py world/lighting client/the-client-loop --out DIR
    python tools/pass8_prompts.py --probe
`--part frame` covers the introduction, the lecture map and the atlas prose; `--part reference`
the hand-kept Reference pages (generated views are skipped).
"""
from __future__ import annotations

import argparse
import os
import re
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "pass7"))
import captions                    # noqa: E402  (tools/pass7/captions.py)
import check_links                 # noqa: E402
import claims                      # noqa: E402
import diagram_arrows as da        # noqa: E402
import mc_version                  # noqa: E402
import pass5_queue as p5q          # noqa: E402
import pass8_queue as q8           # noqa: E402
import pass8_voice as voice        # noqa: E402

ROOT = q8.HERE
SRC = q8.SRC
BRIEF = os.path.join(ROOT, "docs", "pass8-brief.md")


def brief_part2() -> str:
    with open(BRIEF, encoding="utf-8") as f:
        text = f.read()
    m = re.search(r"^## Part 2 — The brief.*?(?=^---\s*$\s*^## Part 3)", text, re.M | re.S)
    if not m:
        sys.exit("docs/pass8-brief.md: could not find Part 2 (the brief) — is the heading intact?")
    return m.group(0).strip()


def ledger_md(md: str, detail: dict) -> str:
    rows = []
    for (_part, page), items in detail.items():
        if page == md:
            rows = sorted(items, key=lambda r: (r[0], r[1]))
    out = [f"## The ledger: {len(rows)} entries in `docs/pass9.md` that name this page, oldest pass first", "",
           "Each is a claim a writing session introduced or a correction it made, with the pass and session that wrote it. "
           "Report on every one, with the file and line in the decompile that settles it, before you read the rest of the page. "
           "A correction is checked as a claim: confirm the fix, not the original, and check that the sentence beside it "
           "still agrees with it. A later entry that overturns an earlier one is checked at the later entry.", ""]
    if not rows:
        out.append("- (no entry names this page; the whole page is the checklist)")
    for p, s, struck, line in rows:
        out.append(f"- [pass {p}, session {s}]{' (struck)' if struck else ''} {re.sub(r'^(?:[-*]|[0-9]+[.])[ ]+', '', line)}")
    return "\n".join(out) + "\n"


def facts_md(key: str, num, units, kinds) -> str:
    """The page's open `[kind=fact]` queue units: questions of fact a reader raised and no session answered."""
    mine, _pw = p5q.units_for(units, kinds, key, num, "fact", False)
    out = [f"## The readers' questions: {len(mine)} in `docs/pass5.md` that name this page", "",
           "Each is a question of fact a reader of an earlier pass asked about this page and no session answered. Answer each "
           "from the decompile, with the file and line, under *The readers' questions* in your report. A question whose "
           "premise the page no longer states is answered *overtaken*, with the line that shows it.", ""]
    out += [p5q.render(u, kinds) for u in mine] or ["- (none)"]
    return "\n".join(out) + "\n"


def captions_md(path: str) -> str:
    figs = captions.figures(path)
    out = [f"## The captions: {sum(1 for f in figs if f[3])} of {len(figs)} figures captioned", "",
           "A caption is a claim about what its figure shows. Read each against the figure above it and the section under it.", ""]
    for n, line, kind, cap in figs:
        out.append(f"- figure {n} ({kind}, page line {line}): {cap or '*(no caption — the figure is unlabelled; say what it shows)*'}")
    return "\n".join(out) + "\n"


def gate_md(checker, path: str, rel: str) -> str:
    failures, notes = checker.check_page(path, rel)
    out = [f"## The figure gate: {len(failures)} unresolved, {len(notes)} notes (`check_figure_names.py`)", ""]
    if failures:
        out += ["Unresolved — a name in a figure that is not in the decompile as written:", ""]
        out += [f"- L{ln}: `{tok}` — {why}" for _rel, ln, tok, why in failures] + [""]
    if notes:
        out += ["Notes — a bare message head, or a message whose head names a third class's method on a lane that owns neither. "
                "The second is the commonest fault pass 7 found (the caller's method drawn arriving at the callee) unless the class "
                "is a static helper, an object with no lane, or the lane's inner class; say which for each:", ""]
        out += [f"- L{ln}: `{tok}` — {why}" for _rel, ln, tok, why in notes] + [""]
    if not failures and not notes:
        out += ["- every name in every figure on this page resolves, and no message head is a note", ""]
    return "\n".join(out)


def inbound_md(rel: str) -> str:
    rows = check_links.inbound(rel)
    if not rows:
        return "## Inbound links\n\n- (no page links here)\n"
    by_anchor: dict[str, list] = {}
    for prel, n, a, _s in rows:
        by_anchor.setdefault(a or "(the page top)", []).append(f"`{prel}`:{n}")
    out = [f"## {len(rows)} inbound links from {len({r[0] for r in rows})} pages, by the anchor they land on", "",
           "A heading is never reworded in this pass: it is an anchor, and every link below moves with it.", ""]
    for a, refs in sorted(by_anchor.items(), key=lambda kv: (-len(kv[1]), kv[0])):
        out.append(f"- `#{a}` ← " + ", ".join(refs) if a != "(the page top)" else "- the page top ← " + ", ".join(refs))
    return "\n".join(out) + "\n"


def voice_md(path: str) -> str:
    m = voice.measure(path)
    out = [f"## The voice, measured (`pass8_voice.py`)", "", voice.header(), voice.row(os.path.relpath(path, SRC).replace(os.sep, "/"), m["counts"]), ""]
    for kind in voice.COLS:
        hits = m["hits"].get(kind)
        if hits:
            out.append(f"### {kind} ({len(hits)})\n")
            out += [f"- L{n}: {s}" for n, s in hits] + [""]
    return "\n".join(out)


def page_keys(pages5: dict, part: str | None, names: list[str]) -> list[str]:
    keys = []
    for p in names:
        p = re.sub(r"\.md$", "", re.sub(r"^(?:src/)?(?:systems/)?", "", p.replace("\\", "/")))
        if p not in pages5:
            sys.exit(f"unknown page {p!r}")
        keys.append(p)
    if part:
        keys += [k for k, (pt, _n, _rel) in pages5.items() if pt == part]
    return keys


def build(keys: list[str], out_dir: str, pages5, units, standing, kinds, detail, notes, brief: str, checker) -> list[str]:
    os.makedirs(out_dir, exist_ok=True)
    known8 = q8.pages()
    written, part_nums, part_dirs = [], set(), set()
    for key in keys:
        part, num, rel = pages5[key]
        path = os.path.join(SRC, rel)
        if claims.is_generated(path):
            print(f"  skip (generated)      {key}")
            continue
        part_nums.add(num); part_dirs.add(part)
        rows = claims.scan(path, None)
        arrows, ndiag, narrow = da.render_page(path)
        prompt = [f"# Pass-8 fact-check — `src/{rel}`", "",
                  f"The page to check is **`src/{rel}`** (repository root: `{ROOT}`).",
                  f"Sources: `{mc_version.source()}` (the {mc_version.VERSION} decompile), its `data/` and `assets/`, and `{mc_version.libs()}`.",
                  "", brief, "", "---", "", ledger_md(rel, detail), "---", "", facts_md(key, num, units, kinds), "---", "",
                  captions_md(path), "---", "",
                  gate_md(checker, path, rel), "---", "", claims.render(path, rows, None), "", "---", "", arrows, ""]
        fname = os.path.join(out_dir, f"{key.replace('/', '--')}.prompt.md")
        with open(fname, "w", encoding="utf-8") as f:
            f.write("\n".join(prompt))
        mine, _pw = p5q.units_for(units, kinds, key, num, None, False)
        sess = [f"# Pass-8 session notes — `src/{rel}`", "",
                "For the session, not the agent: the open queue units of every kind (the voice ones are the polish step's list, the "
                "book and lecture ones are settled if wording-sized and otherwise struck *second edition*), the voice measure, and the "
                f"inbound links. The agent's report arrives beside this as `{key.replace('/', '--')}.report.md`.", "", "---", "",
                p5q.checklist(key, pages5, units, kinds, None, False), "---", "", voice_md(path), "---", "", inbound_md(rel)]
        sname = os.path.join(out_dir, f"{key.replace('/', '--')}.session.md")
        with open(sname, "w", encoding="utf-8") as f:
            f.write("\n".join(sess))
        n_ledger = sum(len(v) for (_p, page), v in detail.items() if page == rel)
        print(f"{n_ledger:3d} ledger {len(mine):3d} queue {len(rows):4d} sentences {ndiag:2d} figures/{narrow:3d} arrows  {fname}")
        written.append(fname)
    # per part: the notes that name no page, from both files; and the voice table
    lines = ["# Notes that name no page — route each to a page, or strike it *(no claim)*", ""]
    for num in sorted(n for n in part_nums if n is not None):
        roman = {v: k for k, v in p5q.q.ROMAN.items()}.get(num)
        if roman and notes.get(roman):
            lines.append(f"## The ledger (`docs/pass9.md`): Part {roman}'s own sessions, {len(notes[roman])} entries\n")
            lines += [f"- [pass {p}, session {s}]{' (struck)' if struck else ''} {re.sub(r'^(?:[-*]|[0-9]+[.])[ ]+', '', line)}"
                      for p, s, struck, line in notes[roman]] + [""]
        _m, partwide = p5q.units_for(units, kinds, "", num, None, False)
        if partwide:
            lines.append(f"## The queue (`docs/pass5.md`): Part {num or 'frame/reference'}, {len(partwide)} units\n")
            lines += [p5q.render(u, kinds) for u in partwide] + [""]
    with open(os.path.join(out_dir, "_part-notes.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    vt = [voice.header()]
    for key in keys:
        part, num, rel = pages5[key]
        path = os.path.join(SRC, rel)
        if not claims.is_generated(path):
            vt.append(voice.row(rel, voice.measure(path)["counts"]))
    with open(os.path.join(out_dir, "_part-voice.md"), "w", encoding="utf-8") as f:
        f.write("# The part's voice, measured\n\n" + "\n".join(vt) + "\n")
    return written


def probe() -> int:
    """One real page, built into a temp dir: the prompt carries the brief and its six sections, the session file its three."""
    brief = brief_part2()
    pages5, units, standing, kinds = p5q.load()
    with open(q8.QUEUE, encoding="utf-8") as fh:
        text = fh.read()
    _pp, _pt, _pw, _un, detail, notes, _fn = q8.route(text, q8.pages())
    import check_figure_names as cfn
    checker = cfn.Checker(mc_version.source(), mc_version.lib_roots())
    tmp = tempfile.mkdtemp(prefix="p8prompts-")
    key = "entities/entity-lifecycle"
    build([key], tmp, pages5, units, standing, kinds, detail, notes, brief, checker)
    prompt = open(os.path.join(tmp, "entities--entity-lifecycle.prompt.md"), encoding="utf-8").read()
    sess = open(os.path.join(tmp, "entities--entity-lifecycle.session.md"), encoding="utf-8").read()
    need_p = ["## Part 2 — The brief", "## The ledger:", "## The readers' questions:", "## The captions:", "## The figure gate:",
              "# Confident sentences", "arrow"]
    need_s = ["## The voice, measured", "inbound links", "queue"]
    missing = [h for h in need_p if h not in prompt] + [h for h in need_s if h.lower() not in sess.lower()]
    if missing:
        print(f"probe FAILED: missing {missing}")
        return 1
    if "[pass " not in prompt:
        print("probe FAILED: the exemplar has ledger entries and none was listed")
        return 1
    print(f"probe ok: the exemplar's prompt carries the brief, its ledger entries, its readers' questions, its captions, the gate, the claims and the arrows; "
          f"the session file the queue, the voice and the links ({tmp})")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pages", nargs="*", help="part/slug")
    ap.add_argument("--part", help="a part directory under src/systems, or frame, or reference")
    ap.add_argument("--out")
    ap.add_argument("--probe", action="store_true")
    args = ap.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if args.probe:
        return probe()
    if not args.out:
        ap.print_help()
        return 2
    pages5, units, standing, kinds = p5q.load()
    keys = page_keys(pages5, args.part, args.pages)
    if not keys:
        ap.print_help()
        return 2
    with open(q8.QUEUE, encoding="utf-8") as fh:
        text = fh.read()
    _pp, _pt, _pw, _un, detail, notes, _fn = q8.route(text, q8.pages())
    import check_figure_names as cfn
    checker = cfn.Checker(mc_version.source(), mc_version.lib_roots())
    build(keys, args.out, pages5, units, standing, kinds, detail, notes, brief_part2(), checker)
    print(f"\npart-wide notes → {os.path.join(args.out, '_part-notes.md')}; the voice table → {os.path.join(args.out, '_part-voice.md')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
