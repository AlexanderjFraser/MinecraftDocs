# Pass 4 — the fact-check agent's brief, and the session's runbook

*Written 2026-09-03 by the planning session between pass 3 and pass 4, so
that every pass-4 session (A–O, run on Opus) launches the same check the
same way. Part 1 is handed to the agent verbatim — `tools/pass4_prompts.py`
prepends it to each page's prompt file. Part 2 is the session's own
procedure. The charter this implements is in [plan.md](plan.md); the
protocol it re-runs is in [pass2.md](pass2.md) under *The pass-2 charter
and protocol*.*

---

## Part 1 — The brief (given to one agent per page)

You are fact-checking one page of MinecraftDocs, a book about how the
Java Minecraft 26.2 codebase works, against the decompiled source. Your
job is to **falsify** the page, not to confirm it. Every page checked in
pass 2 had at least one wrong claim, and the errors lived in the confident
sentences. Assume this page has errors, find them, and quote the evidence.

### What you have

- **The page**: the path is at the top of your prompt file. Read all of it.
- **The decompile**: `reference/26.2/` (Mojang names, Java 25; the client
  jar, a superset of the server jar). `reference/26.2/server-classes.txt`
  lists every class the dedicated server ships — the oracle for
  server-side versus client-only. Nothing under `net/minecraft/client/` or
  `com/mojang/blaze3d/` is in it.
- **The data and assets**: `reference/26.2/data/` (the built-in data packs:
  worldgen JSON, tags, loot tables, recipes, advancements) and
  `reference/26.2/assets/` (models, blockstates, items, atlases, fonts,
  particles, post-effect chains, shaders). A claim about JSON is checked
  against the JSON, not against the class that reads it.
- **The libraries**: `reference/libs/` — Brigadier 1.3.10, DataFixerUpper
  10.0.21 and authlib 9.0.75, as source. A claim about how a codec, a
  command parse or a session-server call behaves is checked there.
- **The checklist**: the prompt file carries, after this brief, (1) every
  note the pass-3 sessions left about this page in `docs/pass4.md`, (2) the
  page's confident sentences by category, (3) every diagram on the page as
  a numbered list of arrows. Those three are your opening work; the rest of
  the page is the second half.

### The order of work

1. **The pass4.md checklist first.** Every line is a claim a pass-3
   session introduced or a correction it made. Report on every line, with
   the file and line in the decompile that settles it, before you read the
   rest of the page. A *correction* is checked as a claim in its own right
   — confirm the fix, not the original.
2. **The diagrams, arrow by arrow.** For each numbered arrow: a sequence
   arrow is a call — name the method that makes it and the method it lands
   in, in that order relative to its neighbours; a note or bar naming a
   tick phase is checked against the tick method that runs that phase; a
   flowchart branch is checked against the condition that decides it; a
   state transition against the code that triggers it. One verdict per
   number. A number you cannot settle is *unverifiable*, not silence.
3. **Every count, re-counted.** For each count in the *count* list, name
   the population (the enum, the registry, the class list, the callers)
   and quote how you enumerated it (`grep -c`, the file and lines). Report
   the number you got even when it matches.
4. **Every only, never, always, all, none, every**: name the population
   the claim ranges over, say how you enumerated it, and list the members
   that break the claim if any do.
5. **Every "X, not Y", "X rather than Y", "X is a fallback / the exception"**:
   check both halves separately. The second half is a claim about the
   distribution or the other cases; pass 2 found these confirmed on the
   first half and never tested on the second.
6. **Every ordering** (before, after, then, same tick, next tick): find the
   two call sites and say which runs first, and whether the order is
   fixed by code or by data (a registration order, a list order).
7. **Every side or thread claim**: which side runs the code, and — the
   question pass 2 learned to ask — which side is *authoritative*, and
   what the other side does with the same code instead.
8. **Then the rest of the page**, sentence by sentence, for anything the
   lists above did not catch: a class said to own state it does not own; a
   field or method attributed to the wrong class (`verify_names.py` only
   checks that the token appears somewhere in the named class's file);
   a causal "so" or "because" whose reason is not in the code; a
   1.21-era fact that 26.2 has changed.
9. **The completeness question** (asked only when the prompt says so):
   what is in this page's scope in the decompile that the page never
   mentions? Name the classes and what they do, one line each.

### What to report

A single markdown report in this shape. Nothing else.

```
## Checklist (pass4.md)
- L<line of pass4.md> — <the claim, shortened> — CONFIRMED | WRONG | UNVERIFIABLE | MISLEADING
  evidence: <path relative to reference/>:<line>, <what it says in one sentence>

## Figures
### Figure 1 (<type>, page line N)
- 1 — CONFIRMED | WRONG | UNVERIFIABLE — <evidence: file:line>
- 2 — ...

## Counts
- L<page line> — "<the sentence's number and what it counts>" — page says N, decompile says M — <how counted: file, grep, lines>

## Absolutes
- L<page line> — "<the claim>" — population: <what and how enumerated> — CONFIRMED | WRONG (<the members that break it>)

## Contrasts and orderings
- L<page line> — "<the claim>" — first half: <verdict, evidence>; second half: <verdict, evidence>

## Sides and threads
- L<page line> — "<the claim>" — runs on: <side/thread, evidence>; authoritative: <side, evidence>

## Everything else
- L<page line> — WRONG | MISLEADING | UNVERIFIABLE — <what the page says> — <what the decompile says> — <file:line>

## Names
Every backticked identifier that is declared somewhere other than where the
page attributes it, or does not exist: <name> — page says <class>, declared in <class> (<file:line>)

## Completeness (only if asked)
- <class or mechanism> — <what it does in one line> — <file>

## Could not verify
- <claim> — <what you looked for and where>
```

Rules for the report:

- **Quote evidence for every verdict**, CONFIRMED included: a path under
  `reference/` and a line number. A CONFIRMED without evidence is not a
  verdict. An empty WRONG list from a report with no evidence is a failed
  check.
- **Your names are as suspect as the page's.** Every method or field you
  cite must be one you opened. Do not cite from memory of 1.21; the game
  has changed names (`ResourceLocation` is `Identifier`, `LightTexture` is
  `Lightmap`, `Timer` is `DeltaTracker`) and many mechanisms.
- **Count the call sites.** For any "the only", "exactly one", "N of M":
  list the members. `grep -rn` across `reference/26.2/` is the tool, and
  the report says what was grepped.
- **Mark the severity of a WRONG**: whether the sentence around it — the
  hook, an invariant, a diagram's argument — still stands, or falls with it.
- **Do not rewrite the page.** Report; the session fixes.
- **Do not stop early.** If the page is long, the checklist and the
  figures come first and the rest follows; a report that covers only part
  of the page says which part it did not reach.

---

## Part 2 — The session runbook

One session = one part (Parts IV, XI, XII, XIII may take two), on Opus.
Every step is a command or a rule; the judgement is in steps 5 and 6.

### 1. Read

`docs/plan.md` (the charter and this session's line in the schedule),
`CLAUDE.md`, this file, the part's landing page. `docs/pass2.md`'s lessons
are compressed in Part 1 above; read the originals under *The pass-2
charter and protocol* once.

### 2. Generate the prompts

```
python tools/pass4_prompts.py --part world --out <scratchpad>/pass4-world
```

One file per page, `<part>--<slug>.prompt.md`: this brief, then the
page's pass4.md checklist (`tools/pass4_queue.py`), its confident sentences
(`tools/claims.py`), its diagrams arrow by arrow (`tools/diagram_arrows.py`).
Read the part's `_part-notes.md` yourself — it is the notes from the part's
own sessions that name no page, and routing them to pages is the session's
job, not the agent's. Add `--complete` for a page that gets the
completeness question (the four session-P pages; anything the charter
names). The frame session uses `--part frame` and `--part reference`, and
runs `python tools/check_deps.py` first — its report is session A's
checklist for addition 2, and its two remaining failures are session A's
first two findings.

### 3. Launch

One background agent per page, all at once, on Opus. The prompt is one
line: *Read `<prompt file>` and do what it says; the page is at `<path>`.
Write your report to `<scratchpad>/pass4-<part>/<slug>.report.md`.* Reports
are not committed. Brief per page, never per part — session O of pass 3
hit the spend limit on a part-wide brief.

### 4. Work while they run

Open the part's landing page and `lectures.md` section and check them
against the pages as claims about order (the charter's addition 2), with
`check_deps.py`'s report for the part. Read `_part-notes.md` and decide
which page each note belongs to. For a Reference session, the generated
views' one-sample-per-view check is the session's own work.

### 5. Audit the reports

For every WRONG that changes a trace, a hook, a count in an argument or an
invariant: **open the decompile yourself before touching the page.** Pass
3's drafting agents were wrong in about a third of their own corrections,
and pass 2's agents cited methods that do not exist. Suspect the tool
once (`verify_names.py`, the generators, the extractors here), then the
agent once, then the page. Take the completeness findings on trust; take
nothing else on trust.

### 6. Fix

In place, sentence by sentence. A wrong hook is replaced by a true one
even when the opening paragraph has to be rewritten around it, and the
rewrite is logged in `docs/pass5.md` as wording to re-read. A fix that
changes what the landing page, `lectures.md` or the glossary says about
the page changes those in the same commit. Nothing is restructured, added
or polished; a structural finding goes to `docs/pass5.md`, a system with
no owner page to `docs/pass3.md` §7. **Grep the corpus for every corrected
claim** — a wrong fact stated once was usually leaned on elsewhere.

### 7. Record

In `docs/pass4.md`, under the part's session entry (or a new `## Session X
— Part N (pass 4)` entry at the top of *Entries*): strike (`~~…~~`) each
settled checklist line, and log each correction as *what the page said →
what the decompile says → file:line*. `tools/pass4_queue.py` reads the
strikes, so the next session's checklists shrink as you go.

### 8. Verify and ship

```
python tools/verify_names.py
node tools/check_mermaid.js
python tools/check_lanes.py --strict
python tools/check_deps.py          # if a landing page, lectures.md or the figure changed
mdbook build
git add -A && git commit -F <message file>     # "pass 4, session X — Part N: <summary>"
tools/deploy.sh
```

Run `verify_names.py` after each page, not after all of them, so a
systematic failure is localised. Commit your own files promptly — pass
sessions commit with add-all.

### 9. Log and hand off

The session log in `docs/plan.md` (tick the schedule line); `docs/pass5.md`
for wording debt and structural findings; `docs/pass3.md` §7 for a gap
with no owner. Anything left for later is written when it is found.

### Session N (the count sweep) and session O (the close)

Session N's queue is `python tools/claims.py --all --counts --out DIR`:
one file per page, every number on it. One agent per *part* (not per page),
given the part's count files and only steps 3 and "Counts" of Part 1; a
count already struck in pass4.md by the part's session is skipped, so the
sweep is of what the part sessions did not reach plus a second look at what
they did. Session O re-reads the tools — including these four — for the
bug pass 2 found in each of its own, re-derives one sample per generated
view, and writes pass 5's charter.
