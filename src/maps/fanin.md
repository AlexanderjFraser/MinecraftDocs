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

## The vocabulary Part II teaches

The thirty hubs are not thirty ideas; they are seven, and Part II is the
first six of them. The world's nouns are the seventh, and the rest of the
book is about them.

| idea | the hubs | where the book teaches it |
|---|---|---|
| a position | `BlockPos`, `Vec3`, `Direction`, `Mth` | [Math and primitives](../reference/math-and-primitives.md) |
| a name and a registry | `Identifier`, `ResourceKey`, `Registries`, `BuiltInRegistries`, `Holder` | [Identifiers and registries](../systems/foundations/identifiers-and-registries.md) |
| a shape on disk | `Codec`, `MapCodec`, `RecordCodecBuilder` | [Codecs, NBT and JSON](../systems/foundations/codecs-nbt-json.md) |
| a shape on the wire | `StreamCodec`, `ByteBufCodecs`, `RegistryFriendlyByteBuf`, `Packet`, `PacketType` | [Packets and stream codecs](../systems/networking/packets-and-stream-codecs.md) |
| text | `Component` | [Text components](../systems/foundations/text-components.md) |
| chance | `RandomSource` | [Math and primitives](../reference/math-and-primitives.md) |
| the world's nouns | `Level`, `ServerLevel`, `BlockState`, `Block`, `Blocks`, `Entity`, `LivingEntity`, `Player`, `EntityType`, `ItemStack`, `SoundEvents`, `SoundEvent`, `DataComponents` | Parts IV to VIII |

Three rows of the table are worth a second look. `ServerLevel` (726) is
imported by nearly as many files as `Level` (750): most code that touches
the world knows it is on the server, and says so in its types. `Minecraft`
(280) is the only client-only class in the thirty, and it is twenty-ninth —
the client's hub is a hub for a quarter of the code, and the shared three
quarters never name it. And `Schema` (389) and `DSL` (278), the other
library classes on the chart, are the migration tree talking to itself:
all but ten of the files that import `Schema` are in `util/datafix`.
*LogUtils*, at 470, is Mojang's logging library — the one line at the top
of nearly every class that does anything.

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
