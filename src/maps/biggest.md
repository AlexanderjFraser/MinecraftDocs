# Where the mass is

> Verified against **Minecraft 26.2** · Maps · The thirty largest classes by lines of decompiled source, coloured by which jar ships them.

The two largest classes in the game are the top of one hierarchy: `Entity`
and `LivingEntity`, 8,785 lines between them, the thing every mob and
player is before it is anything else. Third is `Minecraft`, the client
itself. And then the list turns odd: two of the top ten never run while
anyone is playing. `BlockModelGenerators` runs only inside the data
generator — its single caller is `ModelProvider` — and writes the block
model JSON that ships in the jar; `BlockStateData` is a table that the
save-migration fixes consult when a world from an older version is opened,
and nothing outside `util/datafix` reads it. Size is where the reading is,
not where the game is.

<figure class="map">
{{#include ../generated/biggest.svg}}
<figcaption>The thirty largest classes of 26.2. Blue ships in both jars, orange is client-only; the small grey text is the package under <code>net/minecraft</code>. Click to enlarge.</figcaption>
</figure>

**The number:** 62,935 — the lines in these thirty classes, 8.7% of the
game in 0.4% of its files.

## Three kinds of big

Read down the bars and the thirty sort themselves into three kinds, and
the kind tells you how to read the class.

**The god objects.** `Entity`, `LivingEntity`, `Player`, `ServerPlayer`,
`LocalPlayer` and `Mob` are one chain of inheritance, and each level adds
a thousand lines or more because each is the base of everything below it.
`Minecraft` and `MinecraftServer` are the two programs' roots; `ServerLevel`
is the world; `ChunkMap` is the world's loader. Only two concrete mobs make
the list — `Fox` and `Bee`, the two with the most bespoke behaviour — and
they are the pages a reader of Part VI should expect to be long.

**The switchboards.** `ClientPacketListener` is a handler method for every
clientbound play packet, and `ServerGamePacketListenerImpl` is the same for
every serverbound one — the packets both phases share are handled one class
up, in `ClientCommonPacketListenerImpl` and `ServerCommonPacketListenerImpl`; between them they are the whole of what the wire
can say, which is why Part IX's pages keep coming back to them.
`FriendlyByteBuf` is the buffer both read from.

**The catalogues written as code.** `SoundEvents`, `Blocks`, `Items` and
`CreativeModeTabs` are registries populated one constant per line;
`DensityFunctions` is the node types the vanilla noise graph is built from —
the graph itself is `NoiseRouterData` and the worldgen JSON; `DataFixers` is the
migration history; `OceanMonumentPieces` and `StrongholdPieces` are
structures built by hand, room by room, in Java rather than in a template;
`Options` is every setting the client has, and `Hud` is the in-world overlay
— the crosshair, the hotbar, the bars — inside the wider `Gui` that also
draws screens, toasts and the loading overlay. These are long because they are lists. None is hard.

## The table

Forty rows, of which the figure draws thirty. *side* is which jar ships
the class.

{{#include ../generated/biggest.md}}

---

*Rules: names, never code · how the system works, not how the code reads ·
newest version only · every backticked name passes `tools/verify_names.py`.*
