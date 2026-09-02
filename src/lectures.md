# The lecture map

The video series is an *ordering* over the system pages, which are the
stable content. Each part's landing page lists its lectures in watching
order; this page assembles them and states the dependencies between parts
— where a later part is assumed by an earlier one, and what to watch first
because of it. It is drafted in pass 3, one part per session, and confirmed
by the owner in pass 6 after reading every part with the decompile open.
Until a part's section below is filled, its sidebar order is its watching
order.

The one rule that holds everywhere: **each part assumes only the parts
before it**, and where that is not true the section says so and names the
page to watch early.

## I · Anatomy

1. [Anatomy](systems/anatomy/anatomy.md) — four threads, two loops, one
   wire. Watched first, because every later diagram's lanes assume it.
2. [What this book skips](systems/anatomy/what-this-book-skips.md) — the edge
   of the map, drawn on the treemap of the jar, before investing in thirteen
   parts.

## II · Foundations

Part II is a stack, watched bottom-up; each page is the machinery the one
above it assumes.

1. [Codecs, NBT and JSON](systems/foundations/codecs-nbt-json.md) — one
   `ItemStack` four ways: a chunk file, a packet, a checksum, the text of a
   `/give`. How anything becomes data.
2. [Identifiers and registries](systems/foundations/identifiers-and-registries.md)
   — how anything gets a name and a number, before the game exists and
   again when a world opens; the freeze rule, stated.
3. [The resource system](systems/foundations/resource-system.md) — where
   data comes from and when: F3+T as a pipeline, `/reload` as its coda.
4. [Tags](systems/foundations/tags.md) — data reaching into code; the
   freeze rule paid off.
5. [Data components](systems/foundations/data-components.md) — data on an
   item: prototype, patch, and when the prototype is built.
6. [Text components](systems/foundations/text-components.md) — text as
   data: a death message that is worded on the client.
7. [The data-driven type pattern](systems/foundations/data-driven-types.md)
   — the closer: every *type* field in a data pack is a lookup in a
   registry data packs cannot extend.

[Math and primitives](reference/math-and-primitives.md) is not a lecture;
it is Reference, and the parts link into it.

## III · The server

Part III is a line into a loop and out again: the loop first, because it is
what the rest of the book lives inside, and the beginning and the end last,
because they are only interesting once you know what they start and stop.

1. [The server tick](systems/server/server-tick.md) — one 50 ms lap of the
   Server thread. The most load-bearing lecture in the book after
   *Anatomy*: Parts IV to VIII all assume it, and it is the first place a
   viewer sees a named thread do a full lap.
2. [The level tick](systems/server/server-level-tick.md) — one step of that
   lap, which is the entire world changing. Watched immediately after, and
   never apart from it.
3. [Players and sessions](systems/server/players-and-sessions.md) — a join,
   then death, a dimension and a disconnect compared. The second half
   answers the question people actually ask about a server.
4. [Starting a server](systems/server/starting-a-server.md) — the cold
   open, told fourth: *java -jar server.jar* to the word *Done*.
5. [How a server dies](systems/server/how-a-server-dies.md) — the part's
   closer, and the strongest single lecture in it: three endings, and only
   two of them save your world.

Watch [environment attributes and
timelines](systems/world/environment-attributes-and-timelines.md) (Part IV)
before *the level tick* if you want its first statement to mean anything;
it is the page with the most dependants in the book and Part III is the
earliest of them.

## IV · The world

*Filled by session E.*

## V · Blocks

*Filled by session F.*

## VI · Entities

*Filled by session G.*

## VII · Items and inventories

*Filled by session H.*

## VIII · The player

*Filled by session I.*

## IX · Networking

*Filled by session J.*

## X · The client

*Filled by session K.*

## XI · Rendering

*Filled by session L.*

## XII · World generation

*Filled by session M.*

## XIII · Commands and data packs

*Filled by session N.*

## The dependencies between parts

*Assembled by session P from the landing pages' "before you start" lists,
with the figure of which part assumes which.* Two are already known from
the pass-2 notebook: Part IX assumes the server tick's phase order (Part
III) and the client's frame/tick interleave (Part X); and
[environment attributes and timelines](systems/world/environment-attributes-and-timelines.md)
in Part IV is assumed by a Part III page and by four later parts, so it is
watched early.
