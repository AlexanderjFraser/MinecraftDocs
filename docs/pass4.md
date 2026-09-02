# Pass 4 — the second fact-check (queue; opened 2026-09-02)

*Pass 4 re-runs pass 2's adversarial protocol — archived in
[pass2.md](pass2.md) with its twelve lessons — over the corpus pass 3
rewrote. This file is where pass-3 sessions write down what pass 4 must
check hardest: every page rewritten, every claim a rewrite introduced (a
hook, a redrawn ordering, a new section, a landing page's dependency list),
every diagram redrawn. Pass 4 checks everything anyway; this list decides
what it checks first. The charter is written by pass 3's closing session
(P) into [plan.md](plan.md).*

## How to write an entry

Per session: the pages rewritten; per page, the claims introduced (one line
each, quoting the sentence); the diagrams redrawn (which orderings they
assert); anything an agent drafted that the old page did not say. Newest
entry first.

## Standing items

- The landing pages and `lectures.md` are claims about order and
  dependency: check that every *before you start* link is actually assumed
  by the part, and that nothing earlier depends on something later.
- Every redrawn diagram: arrow by arrow, and every tick-boundary bar.
- The generated Reference views pass 3 adds (serializers, attributes, the
  glossary if generated): re-derive one sample by hand per view — pass 2
  found bugs in both generators, and one had reached the prose.
- The lane key in `TEMPLATE.md`: every lane's expansion is a class that
  exists. (If session A writes a lane linter, strike this.)
- Pass 2's twelve lessons apply unchanged; the shape to watch remains the
  confident sentence — orderings, "only", "never", counts, and "X, not Y".
- **Library facts are checkable now and were not in pass 2.**
  `reference/libs/` holds Brigadier, DataFixerUpper and authlib sources
  (`tools/fetch_libs.sh`) and `reference/26.2/assets/` the atlas, font,
  shader and post-effect JSON. Pass 2 took every claim about them on trust;
  pass 4 re-derives them, hardest on: `codecs-nbt-json` (DFU semantics —
  `DataResult` partials, `MapCodec`, `Lifecycle`), `protocol-phases` and
  `players-and-sessions` (authlib's session-server round trip),
  `chat-and-signing` (profile keys and signature validation),
  `brigadier-and-commands`, `execution-and-functions` and
  `scoreboard-and-data` (parse, suggestions, `ContextChain`, the result
  consumer), `models-and-atlases` and `text-and-fonts` (the atlas and font
  JSON), and whatever pass 3 writes about post-processing.
- **The `execute store` question** on `scoreboard-and-data` — what a failing
  ordinary leaf command writes — is now answerable from Brigadier 1.3.10;
  settle it and remove the page's "cannot be settled from the decompile"
  note.

## Entries

- **2026-09-02, planning session** — the mermaid syntax fixes were
  syntax-only (labels reworded around `;` and `#`, see the commit diff); no
  claim changed. Nothing to check beyond a glance at that diff.
