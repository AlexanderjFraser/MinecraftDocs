#!/usr/bin/env python3
"""The final pass's ledger (docs/pass9.md), routed by page, by part and by session.

pass9.md is where every session of passes 5, 6 and 7 listed the claims it introduced and the
corrections it made, so that the third fact-check — pass 8 — checks them first. This reads the
file into entries (one bullet, top level or nested, under a `## Pass N, session X` heading), resolves
the page each entry names, and prints how much unchecked material each page and each part carries,
which is what sizes pass 8's sessions. An entry names its page in one of the forms the sessions
actually used — `entity-lifecycle`, `entities/entity-lifecycle`, `src/systems/entities/entity-lifecycle.md`,
`reference/threads`, `entities/README`, `/` for the introduction — and an entry that names none is
routed to the part its session heading names (a part session's page-less note is that part's), or
counted as frame-level when the session was the standard, the frame or the close.

  python tools/pass8_queue.py                  per-part totals: named entries, part-wide notes, pages; the names that resolve to nothing
  python tools/pass8_queue.py --pages          per-page counts, largest first
  python tools/pass8_queue.py --part VI        every entry for one part, by page and session, oldest pass first; then the part-wide notes
  python tools/pass8_queue.py --part Frame     the entries the standard, frame and close sessions left that name no page
  python tools/pass8_queue.py --unstruck       per session: entries, struck, unstruck — ruling R3 says the close leaves none unstruck
  python tools/pass8_queue.py --pass 8         only the entries pass 8's own sessions wrote (the second reading's list)
  python tools/pass8_queue.py --probe

Pass 8's own entries are left out of --part and --pages by default (they are what session P reads,
not what a part session checks); --pass 8 lists them. A pass-7 correction that overturns a pass-5
claim is checked once, at the later entry, which is why --part prints oldest pass first with the
session that wrote each line.
"""
import os
import re
import sys
from collections import Counter, defaultdict

HERE = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
SRC = os.path.join(HERE, "src")
QUEUE = os.path.join(HERE, "docs", "pass9.md")

SESSION = re.compile(r"^## (Pass (\d+), (?:session (\w+)|the planning session)[^\n]*)")
BULLET = re.compile(r"^\s*(?:[-*]|\d+\.) ")
STRUCK = re.compile(r"^\s*(?:[-*]|\d+\.)\s*~~")
TICK = re.compile(r"`([^`\n]+)`")
PART_IN_HEADING = re.compile(r"\bParts? ([IVX]+)\b")
PART_LINE = re.compile(r"^- \[([IVX]+) · ([^\]]+)\]\(systems/([a-z-]+)/README\.md\)")
PAGE_LINE = re.compile(r"^\s*- \[[^\]]+\]\(([^)]+\.md)\)")
ORDER = ["Frame", "Maps", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII", "XIII", "Reference"]


def pages():
    """key -> (md path, part numeral). Keys: `slug`, `dir/slug`, `dir/README`, `dir` (the landing page), `/`."""
    by_key, part_of_dir, part = {}, {}, ""
    with open(os.path.join(SRC, "SUMMARY.md"), encoding="utf-8") as fh:
        for line in fh:
            m = PART_LINE.match(line)
            if m:
                part, part_of_dir[m.group(3)] = m.group(1), m.group(1)
                landing = (f"systems/{m.group(3)}/README.md", part)
                by_key.setdefault(m.group(3), landing)
                by_key[f"{m.group(3)}/README"] = landing
                continue
            m = PAGE_LINE.match(line)
            if not m:
                continue
            md = m.group(1)
            slug = os.path.basename(md)[:-3]
            d = md.split("/")[1] if md.startswith("systems/") else md.split("/")[0]
            p = part_of_dir.get(d, {"maps": "Maps", "reference": "Reference"}.get(d, "Frame"))
            if slug == "README":
                by_key[f"{d}/README"] = (md, p)
                continue
            by_key.setdefault(slug, (md, p))
            by_key[f"{d}/{slug}"] = (md, p)
    by_key["/"] = ("introduction.md", "Frame")
    by_key["introduction"] = ("introduction.md", "Frame")
    by_key["lectures"] = ("lectures.md", "Frame")
    return by_key


def resolve(tick: str, known: dict):
    """A backticked token -> the page key it names, or None."""
    t = tick.strip().replace("\\", "/")
    t = re.sub(r":\d+(?:[-–]\d+)?$", "", t)          # `page`:12 inside the ticks
    t = re.sub(r"^\./", "", t)
    t = re.sub(r"^src/", "", t)
    t = re.sub(r"^systems/", "", t)
    t = re.sub(r"\.md$", "", t)
    if t in known:
        return t
    if t.endswith("/README") and t in known:
        return t
    return None


def entries(text: str):
    """(pass, session, session part or None, page keys, struck, line) per bullet under a session heading."""
    out, cur, cur_part = [], None, None
    for line in text.splitlines():
        m = SESSION.match(line)
        if m:
            cur = (int(m.group(2)), m.group(3) or "planning")
            pm = PART_IN_HEADING.search(m.group(1))
            cur_part = pm.group(1) if pm else None
            continue
        if cur and BULLET.match(line):
            out.append((cur[0], cur[1], cur_part, TICK.findall(line), bool(STRUCK.match(line)), line.strip()))
    return out


def route(text: str, known: dict, only_pass=None, skip_pass=8):
    per_page, per_part, partwide, unresolved = Counter(), Counter(), Counter(), Counter()
    detail, notes, frame_notes = defaultdict(list), defaultdict(list), []
    for p, s, spart, ticks, struck, line in entries(text):
        if only_pass is not None and p != only_pass:
            continue
        if only_pass is None and skip_pass is not None and p == skip_pass:
            continue
        keys = [k for k in (resolve(t, known) for t in ticks) if k]
        for t in ticks:
            if resolve(t, known) is None and re.search(r"\.md$|/README$|^(?:src/)?(?:systems|reference|maps)/", t):
                unresolved[t] += 1
        if keys:
            md, part = known[keys[0]]  # the first named page owns the entry
            per_page[md] += 1
            per_part[part] += 1
            detail[(part, md)].append((p, s, struck, line))
        elif spart:
            partwide[spart] += 1
            notes[spart].append((p, s, struck, line))
        else:
            frame_notes.append((p, s, struck, line))
    return per_page, per_part, partwide, unresolved, detail, notes, frame_notes


def strikes(text: str):
    """per (pass, session): entries, struck."""
    rows = Counter()
    for p, s, _sp, _t, struck, _l in entries(text):
        rows[(p, s, "all")] += 1
        rows[(p, s, "struck")] += int(struck)
    return rows


def probe():
    known = {"a-page": ("systems/x/a-page.md", "I"), "x/a-page": ("systems/x/a-page.md", "I"),
             "x": ("systems/x/README.md", "I"), "x/README": ("systems/x/README.md", "I"),
             "reference/r": ("reference/r.md", "Reference"), "/": ("introduction.md", "Frame")}
    text = ("## Pass 7, session A — Part I · x\n- `a-page` fine\n- `src/systems/x/a-page.md`:12 wrong\n"
            "- `x/README` the landing page\n- ~~`reference/r` struck~~\n- no page named here\n- `no-such/page.md` unknown\n"
            "## Pass 6, session N — the frame\n- `/` the introduction\n- a frame note\n"
            "## Pass 8, session B — Part I\n- `a-page` pass 8's own\n")
    per_page, per_part, partwide, unresolved, detail, notes, frame_notes = route(text, known)
    ok = (per_page == Counter({"systems/x/a-page.md": 2, "systems/x/README.md": 1, "reference/r.md": 1, "introduction.md": 1})
          and partwide == Counter({"I": 2}) and unresolved == Counter({"no-such/page.md": 1}) and len(frame_notes) == 1
          and detail[("Reference", "reference/r.md")][0][2] is True)
    if not ok:
        sys.exit(f"probe FAILED: {per_page} {partwide} {unresolved} {len(frame_notes)}")
    if route(text, known, only_pass=8)[0] != Counter({"systems/x/a-page.md": 1}):
        sys.exit("probe FAILED: --pass 8 did not isolate pass 8's entries")
    st = strikes(text)
    if st[(7, "A", "all")] != 6 or st[(7, "A", "struck")] != 1:
        sys.exit(f"probe FAILED: strikes {st}")
    print("probe ok: every page form resolves, a page-less note goes to its session's part, a frame note stays frame-level, "
          "a strike is counted, pass 8's own entries are kept apart")


def print_part(want, detail, notes, frame_notes):
    if want == "Frame":
        print(f"### notes from the standard, frame and close sessions that name no page — {len(frame_notes)} entries")
        for p, s, struck, line in frame_notes:
            print(f"  [pass {p} {s}]{' STRUCK' if struck else ''} {line[:200]}")
    for (part, md), rows in sorted(detail.items()):
        if part != want:
            continue
        print(f"\n### {md} — {len(rows)} entries")
        for p, s, struck, line in sorted(rows, key=lambda r: (r[0], r[1])):
            print(f"  [pass {p} {s}]{' STRUCK' if struck else ''} {line[:200]}")
    if notes.get(want):
        print(f"\n### part-wide notes from Part {want}'s own sessions that name no page — {len(notes[want])} entries; route each to a page, or strike it *(no claim)*")
        for p, s, struck, line in notes[want]:
            print(f"  [pass {p} {s}]{' STRUCK' if struck else ''} {line[:200]}")


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if "--probe" in sys.argv:
        probe()
        sys.exit()
    with open(QUEUE, encoding="utf-8") as fh:
        text = fh.read()
    known = pages()
    only_pass = int(sys.argv[sys.argv.index("--pass") + 1]) if "--pass" in sys.argv else None
    per_page, per_part, partwide, unresolved, detail, notes, frame_notes = route(text, known, only_pass=only_pass)
    if "--unstruck" in sys.argv:
        st = strikes(text)
        print(f"{'session':<20}{'entries':>8}{'struck':>8}{'unstruck':>9}")
        tot_all = tot_struck = 0
        for (p, s) in sorted({(p, s) for p, s, _k in st}):
            a, k = st[(p, s, "all")], st[(p, s, "struck")]
            tot_all += a; tot_struck += k
            print(f"{'pass ' + str(p) + ' ' + s:<20}{a:>8}{k:>8}{a - k:>9}")
        print(f"{'total':<20}{tot_all:>8}{tot_struck:>8}{tot_all - tot_struck:>9}")
        sys.exit(0 if tot_all == tot_struck else 1)
    if "--part" in sys.argv:
        print_part(sys.argv[sys.argv.index("--part") + 1], detail, notes, frame_notes)
        sys.exit()
    if "--pages" in sys.argv:
        for md, n in per_page.most_common():
            print(f"{n:>5}  {md}")
        sys.exit()
    pages_in = Counter(part for part, _ in detail)
    print(f"{'part':<10}{'named':>7}{'part-wide':>11}{'pages':>7}")
    for part in ORDER:
        print(f"{part:<10}{per_part.get(part, 0):>7}{partwide.get(part, 0):>11}{pages_in.get(part, 0):>7}")
    total = sum(per_page.values())
    print(f"{'total':<10}{total:>7}{sum(partwide.values()):>11}{len(per_page):>7}")
    print(f"\nframe-level notes (the standard, frame and close sessions; no page, no part): {len(frame_notes)}")
    print(f"all entries: {total + sum(partwide.values()) + len(frame_notes)}")
    if unresolved:
        print(f"page-shaped names that resolve to no page ({len(unresolved)}):")
        for n, c in unresolved.most_common(30):
            print(f"  {c:>3}  {n}")
