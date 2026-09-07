# What everything imports

> Verified against **Minecraft 26.2** · Maps · The thirty most-imported Mojang classes: how many files name each one in an import statement.

One file in six imports `BlockPos`. That is the least surprising fact on
this page; the next one is not. The chart counts Mojang imports only —
*net.minecraft* and *com.mojang* — because the JDK's `List` and `Optional`
and the nullability annotation outrank everything on it and say nothing
about the game. Under that rule the second most-imported type is not
Minecraft's: it is `Codec`, from Mojang's DataFixerUpper
library, imported by 987 files, with `MapCodec` third and
`RecordCodecBuilder` sixth. Three of the six classes the game most depends
on are the serialisation vocabulary that turns objects into NBT and JSON
and back, which is why Part II teaches codecs before anything a player can
see.

<figure class="map">
{{#include ../generated/fanin.svg}}
<figcaption>The thirty most-imported Mojang classes of 26.2; JDK and annotation imports are not counted. Blue ships in both jars, orange is client-only, grey is a library outside the decompile. Click to enlarge.</figcaption>
</figure>

## Seven ideas, and where the book teaches them

The hubs are not thirty ideas; they are seven. The table below groups them,
reading down the sixty rows rather than the thirty the figure draws, so that a
family is not broken in half by the cut-off — `ByteBufCodecs` and `PacketType`
are the wire's vocabulary whether or not they clear it. Twenty-four of the
thirty are in a row; the six that are not are the paragraphs after it.

Part II teaches three of the seven, Reference two, Part IX one, and the
seventh — the world's nouns — is the rest of the book. That is the more useful
fact than *Part II teaches the vocabulary*: the classes a reader must know
before Part IV are not one part's worth.

| idea | the hubs | where the book teaches it |
|---|---|---|
| a position | `BlockPos`, `Vec3`, `Direction`, `Mth` | [Math and primitives](../reference/math-and-primitives.md#the-coordinate-spaces) |
| a name and a registry | `Identifier`, `ResourceKey`, `Registries`, `BuiltInRegistries`, `Holder` | [Identifiers and registries](../systems/foundations/identifiers-and-registries.md) |
| a shape on disk | `Codec`, `MapCodec`, `RecordCodecBuilder` | [Codecs, NBT and JSON](../systems/foundations/codecs-nbt-json.md) |
| a shape on the wire | `StreamCodec`, `ByteBufCodecs`, `RegistryFriendlyByteBuf`, `Packet`, `PacketType` | [Packets and stream codecs](../systems/networking/packets-and-stream-codecs.md) |
| text | `Component` | [Text components](../systems/foundations/text-components.md) |
| chance | `RandomSource` | [Math and primitives](../reference/math-and-primitives.md#two-random-families-and-two-that-are-neither) |
| the world's nouns | `Level`, `ServerLevel`, `BlockState`, `Block`, `Blocks`, `Entity`, `LivingEntity`, `Player`, `EntityType`, `ItemStack`, `SoundEvents`, `SoundEvent`, `DataComponents` | Parts IV to VIII |

Three rows of the *chart* are worth a second look. `ServerLevel` (726) is
imported by nearly as many files as `Level` (750): most code that touches
the world knows it is on the server, and says so in its types. `Minecraft`
(280) is the only client-only class in the thirty, and it is twenty-ninth —
the client's hub is a hub for the client-only side alone, which is under a
third of the files, and the shared seven tenths never name it. And `Schema`
(389) and `DSL` (278) are the migration tree talking to itself: all but ten of
the files that import `Schema` are in `util/datafix`, and the ten are its
sibling `util/filefix`.

That leaves three of the thirty with no home in either the table or the
paragraph above, and they are the three that are not vocabulary at all.
*LogUtils* (470) is Mojang's logging library, the one line at the top of nearly
every class that does anything. `Util` (454) is where the executors and the
static odds and ends live ([threads](../reference/threads.md#the-threads-a-lecture-leans-on)) —
a hub because it is where the unclassifiable went, not because it is an idea.
And `BlockBehaviour` (311) is the world's nouns seen one class higher, which is
the next paragraph's subject.

## What the count misses

An import is counted once per file, so the chart says *how many files
name the class*, not how often. It also undercounts every class used
inside its own package, because that needs no import: the 257 files that
import `Block` are the files outside `world/level/block` that use it, and
the same is true of `BlockBehaviour` and `Minecraft`. A class's true
reach is this number plus its package.

## The table

Sixty rows, of which the figure draws thirty. *side* is which jar ships
the class, or *library* for a class outside the decompile.

{{#include ../generated/fanin.md}}

---

*Rules: names, never code · how the system works, not how the code reads ·
newest version only · every backticked name passes `tools/verify_names.py`.*
