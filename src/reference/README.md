# Reference

> Verified against **Minecraft 26.2** · Reference · The shelf behind the lectures: everything a viewer would pause the video to read, kept where no lecture has to stop for it.

A lecture explains one thing at a time, and it cannot stop to list the 43
entity-data serializers or the ten bits of a flag word without losing the
room. The rule for this tier is one question: *would a viewer pause the
video to read this?* If yes, it lives here and the page links to it — so
nobody arrives at this shelf by walking it, and the table below is sorted
for the one question a reader of a catalogue should ask of it rather than
for browsing.

That question is not *what does it list* but **how is it kept**, because a
catalogue is only as good as the version it was read from. Thirteen of the
twenty-three are rewritten by a tool on every deploy and cannot go stale.
The other ten were read by a person, one class at a time, and go stale
exactly the way this page's own last column did.

A shelf is looked up, not watched, so a Reference page is exempt from the
rule that every page carries a figure: it draws one only where its subject is
a shape — the conversions between [coordinate
spaces](math-and-primitives.md#the-coordinate-spaces), the [ways work crosses a
thread boundary](threads.md#three-ways-work-crosses-a-thread-boundary) — and
everywhere else, this page included, its figure is the table.

## How each page is kept, and who leans on it

*Generated · decompile* is read off the source, *generated · corpus* off the
book's own pages, and both are rewritten on every deploy; *hand-kept* is a
person's reading. The last column's numerals are the parts in sidebar order,
I to XIII, as the [lecture map](../lectures.md) lists them.

| page | what it lists | kept by | the parts whose landing pages point at it |
|---|---|---|---|
| [Packets](packets.md) | every packet, by protocol group and direction | generated · decompile | III, V, VI, VII, VIII, IX, X, XIII |
| [Registries](registries.md) | every registry key: built-in, data-pack, synced | generated · decompile | II, IV, V, VI, VII, IX, XII, XIII |
| [Data components](components.md) | every `DataComponentType`, persistent and synced | generated · decompile | II, V, VII, VIII, IX |
| [Game rules](gamerules.md) | every rule, type, category, default | generated · decompile | III, IV, V, VI, VIII |
| [Attributes](attributes.md) | every attribute: default, range, sentiment, syncable | generated · decompile | VI, VIII |
| [Entity data serializers](entity-data-serializers.md) | all 43, in registration order, which is the wire id | generated · decompile | VI |
| [Enchantment hooks](enchantment-hooks.md) | every public `EnchantmentHelper` entry point and its callers | generated · decompile | VII |
| [Loot context parameter sets](loot-context-params.md) | all twenty-six, with required and optional keys | generated · decompile | VII, XIII |
| [Entity spawn reasons](spawn-reasons.md) | all nineteen, and which classes change behaviour for each | generated · decompile | VI |
| [Structure spawn overrides](structure-spawn-overrides.md) | the six structures that replace a biome's spawn list, and with what | generated · decompile | VI, XII |
| [The weapon helpers](weapon-helpers.md) | the seven `Item.Properties` helpers and every item built by one | generated · decompile | VII |
| [Block update flags](block-update-flags.md) | the ten bits of `Level.setBlock`'s flag word | hand-kept | IV, V |
| [Damage outside `LivingEntity`](non-living-damage.md) | what each of the twenty-one non-living classes does when hit | hand-kept | VI, VIII |
| [What the HUD draws, and when](hud-elements.md) | every HUD element and the condition it is behind | hand-kept | X |
| [Submit phases and feature renderers](submit-phases.md) | the fifteen phases and the thirteen renderers, in declaration order | hand-kept | XI |
| [Density-function nodes](density-function-nodes.md) | the thirty-four node types, what the rewrite installs for each, what range each reports, and which ids the shipped data writes | hand-kept | XII |
| [Threads](threads.md) | every thread, who makes it, what may run on it | hand-kept | I, III, IV, VI, IX, X, XI |
| [Math and primitives](math-and-primitives.md) | the coordinate spaces, packings, shapes and random sources | hand-kept | II, IV, V, VI, XII |
| [Level data and rules](level-data-and-rules.md) | who owns the seed, spawn, rules and border, and which file each is in | hand-kept | III, IV, VIII, IX, XII |
| [Naming drift](naming-drift.md) | every 1.21-era name a reader will reach for, and what 26.2 calls it | hand-kept | I, II, VII, X, XI, XII |
| [Glossary](glossary.md) | one sentence per term, and the page that owns it | hand-kept | II, V, VI, X, XI, XII, XIII |
| [Diagram lanes](lanes.md) | every lane abbreviation and the class it means, and the nine that mean a thread, a process or a boundary instead | generated · corpus | every part |
| [Class index](class-index.md) | every class backticked on a page, and the pages that name it | generated · corpus | — |

The two generated kinds differ in what they are read from.
`python tools/gen_reference.py all` rewrites eleven of them from the
decompile's declaration lines, so a version bump re-derives them rather than
re-reading them; the other two are read off this book instead, by
`python tools/verify_names.py --index` (the class index, from every
backticked name) and `python tools/check_lanes.py --index` (the lanes, from
the key in the book's page template). *Hand-kept* means a part session read the classes and wrote the
rows, `tools/verify_names.py` checks every name on the page, and a
fact-check re-reads the rows — declaration orders drift on a version
bump, and two of these pages (submit phases, density-function nodes) are
nothing but declaration order.

The last column is the one thing on this page a tool can settle, and it is
now settled by one: each of the thirteen parts' landing pages names the shelf
pages it uses, and `tools/check_deps.py` re-derives this column from those
thirteen sections and refuses to publish when the two disagree. It disagreed
in six rows on the day the check was written, which is what a hand-kept
column does.

For agents: the whole site is also served as one file at
[/llms-full.txt](https://minecraftdocs.dev/llms-full.txt).

---

*Rules: names, never code · how the system works, not how the code reads ·
newest version only · every backticked name passes `tools/verify_names.py`.*
