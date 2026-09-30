# Reference

> Verified against **Minecraft 26.3** · Reference · The shelf behind the lectures: everything a viewer would pause the video to read, kept where no lecture has to stop for it.

A lecture explains one thing at a time, and it cannot stop to list the 44
entity-data serializers or the ten bits of a flag word without losing the
room. The rule for this tier is one question: *would a viewer pause the
video to read this?* If yes, it lives here and the page links to it — so a shelf page is reached from the page that needs it, and the table below is grouped by the one question a reader of a catalogue should ask of it rather than for browsing.

That question is not *what does it list* but **how is it kept**, because a
catalogue is only as good as the version it was read from. Thirteen of the twenty-three are rewritten by a tool on every deploy, so their rows are re-derived each time, though the sentences each tool types around its tables, and the odd cell it types into a row, are not. The other ten were written by a session reading the classes one at a time, and go stale exactly the way this page's own last column did.

A shelf is looked up, not watched, so a Reference page is exempt from the
rule that every page carries a figure: it draws one only where its subject is
a shape — the conversions between [coordinate
spaces](math-and-primitives.md#the-coordinate-spaces), the [ways work crosses a
thread boundary](threads.md#three-ways-work-crosses-a-thread-boundary) — and everywhere else, this page included, the table or the list is the figure.

## How each page is kept, and who leans on it

*Generated · decompile* is read off the source, *generated · corpus* off the book itself — its pages, and the lane key in its page template — and both are rewritten on every deploy; *hand-kept* is a session's reading. The last column's numerals are the parts in sidebar order,
I to XIII, as the [lecture map](../lectures.md) lists them.

| page | what it lists | kept by | the parts whose landing pages point at it |
|---|---|---|---|
| [Packets](packets.md) | every packet, by protocol group and direction | generated · decompile | III, V, VI, VII, VIII, IX, X, XIII |
| [Registries](registries.md) | every registry key but the root's: built-in, data-pack, synced | generated · decompile | II, IV, V, VI, VII, IX, XII, XIII |
| [Data components](components.md) | every `DataComponentType` in `DataComponents`, persistent or not, and how it crosses the wire | generated · decompile | II, V, VII, VIII, IX |
| [Game rules](gamerules.md) | every rule, type, category, default | generated · decompile | III, IV, V, VI, VIII |
| [Attributes](attributes.md) | every attribute: default, range, sentiment, syncable | generated · decompile | VI, VIII |
| [Entity data serializers](entity-data-serializers.md) | all 44, in registration order, which is the wire id | generated · decompile | VI |
| [Enchantment hooks](enchantment-hooks.md) | every public `EnchantmentHelper` entry point and its callers | generated · decompile | VII |
| [Loot context parameter sets](loot-context-params.md) | all thirty-one, with required and optional keys | generated · decompile | VII, XIII |
| [Entity spawn reasons](spawn-reasons.md) | all nineteen, and which classes change behaviour for each | generated · decompile | VI |
| [Structure spawn overrides](structure-spawn-overrides.md) | the six structures that replace a biome's spawn list, and with what | generated · decompile | VI, XII |
| [The weapon helpers](weapon-helpers.md) | the seven `Item.Properties` helpers and every item built by one | generated · decompile | VII |
| [Block update flags](block-update-flags.md) | the ten bits of `Level.setBlock`'s flag word | hand-kept | IV, V |
| [Damage outside `LivingEntity`](non-living-damage.md) | what each of the twenty-two non-living classes does when hit | hand-kept | VI, VIII |
| [What the HUD draws, and when](hud-elements.md) | every HUD element and the condition, if any, it is behind | hand-kept | X |
| [Submit phases and feature renderers](submit-phases.md) | the fifteen phases and the twelve renderers, in the order the code lists them | hand-kept | XI |
| [Density-function nodes](density-function-nodes.md) | the forty-four node types, what the compiler turns each into, what range each reports, and which ids the shipped data writes | hand-kept | XII |
| [Threads](threads.md) | every thread, who makes it, what may run on it | hand-kept | I, III, IV, VI, IX, X, XI |
| [Math and primitives](math-and-primitives.md) | the coordinate spaces, packings, shapes and random sources | hand-kept | II, IV, V, VI, XII |
| [Level data and rules](level-data-and-rules.md) | who owns the seed, spawn, rules and border, and which file each is in | hand-kept | III, IV, VIII, IX, XII |
| [Naming drift](naming-drift.md) | the 1.21-era names a reader will reach for, and what 26.3 calls them | hand-kept | I, II, VII, X, XI, XII |
| [Glossary](glossary.md) | a short entry per term, and the page that owns it | hand-kept | II, V, VI, X, XI, XII, XIII |
| [Diagram lanes](lanes.md) | every lane abbreviation and the class it means, and the ten that mean a thread, the process, the wire, the disk, a service or the game's own code instead | generated · corpus | every part |
| [Class index](class-index.md) | every class a written page backticks or a figure names, and the pages that name it | generated · corpus | — |

The two generated kinds differ in what they are read from.
`python tools/gen_reference.py all` rewrites eleven of them from the decompile — its declarations, its call sites and its data files — so a version bump re-derives their rows rather than re-reading them; the other two are read off this book instead, by
`python tools/verify_names.py --index` (the class index, from every written page's backticked names and every class a figure names) and `python tools/check_lanes.py --index` (the lanes, from
the key in the book's page template). *Hand-kept* means a part session read the classes and wrote the
rows, `tools/verify_names.py` checks the backticked names on the page, and a
fact-check re-reads the rows — the code's own orders drift on a version bump, and three of these pages (the HUD, the submit phases, the density-function nodes) are laid out in one.

The last column is one a tool can settle, and it is now settled by one: each of the thirteen parts' landing pages names the shelf
pages it uses, and `tools/check_deps.py` re-derives this column from those
thirteen sections and refuses to publish when the two disagree. It disagreed
in six rows on the day the check was written, which is what a hand-kept
column does.

For agents: the whole site is also served as one file at
[/llms-full.txt](https://minecraftdocs.dev/llms-full.txt).

---

*Rules: names, never code · how the system works, not how the code reads ·
newest version only · every backticked name passes `tools/verify_names.py`.*
