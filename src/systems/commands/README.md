# XIII · Commands and data packs

> Verified against **Minecraft 26.2** · Part XIII · a string typed into a chat box becomes a call with typed arguments, on a queue, with a permission attached — and four whole systems are built on top of that and nothing else.

Type a slash. The text turns grey and green and red as you type, a hint
appears behind the cursor, and pressing Enter sends the *string* — the
parse the client just did is thrown away. On the server the same string is
parsed again, against a tree whose nodes carry permission requirements, and
becomes a piece of work on a queue rather than a Java call. Everything else
in this part rides that machinery: an advancement is a subscription
delivered by a trigger and edited by `/advancement`, a scoreboard is a
number written by `/scoreboard` or by `execute store`, a dialog is a
data-pack form opened by `/dialog`, and a game test is a data-pack test run
by `/test`. **None of those four needs any of the others.** What they need
is the parse and the queue, and a reader who has those two can explain any
of the four from them.

The nine packages [the atlas](../../maps/packages.md#where-each-part-lives)
gives this part are the machinery — `net/minecraft/commands` and
`server/commands` — the four systems on top of it —
`net/minecraft/advancements`, `world/scores`, `server/dialog` with its
`client/gui/screens/dialog` screens, and `net/minecraft/gametest` — and two
small ones the machinery needs, `server/permissions` and `server/bossevents`.
Counted the way the atlas counts everything, that is
{{#include ../../generated/part-commands.md}} — of which the command
catalogue alone (`net/minecraft/server/commands`) is 102 files and 12,800
lines, each of them a thin lambda over machinery some other part of this
book owns. So what a command *does* once dispatched is almost always another
part's page, and [Brigadier and commands](brigadier-and-commands.md#commands-that-are-a-door-to-somewhere-else)
carries the list of which; the statistics, which are criteria, are in [what
this book skips](../anatomy/what-this-book-skips.md).

## The shape of the part

Part XIII is **a stack of three floors**, and for a watcher the dependency
runs one way: all four systems on the top floor need both of the floors
below, and none of them needs another. The code is less tidy than the
lecture order — a selector's *advancements=* and *scores=* options reach
straight up into two of the top-floor systems — but nothing on the top floor
reaches sideways.

```mermaid
flowchart TB
    subgraph P["PARSE — a string becomes a call"]
        direction LR
        L1["1 · Brigadier and commands"] --- L2["2 · Permissions"] --- L2b["3 · Entity selectors"]
    end
    P --> X
    subgraph X["EXECUTE — the call becomes work on a queue"]
        direction LR
        L3["4 · The execution engine"] --- L4["5 · Functions and macros"]
    end
    X --> U
    subgraph U["WHAT COMMANDS ARE FOR — four systems whose write surface is a command"]
        direction LR
        L5["6 · Advancements"]
        L6["7 · Scores, teams and stored data"]
        L7["8 · Dialogs"]
        L8["9 · Game tests"]
    end
```

The four pages on the top floor are peers, not a sequence: watch them in any
order, or only the ones you care about. The two floors below them are not
optional for any of the four.

## Before you start

[The server tick](../server/server-tick.md#what-minecraftservertickchildren-runs-and-in-what-order)
from Part III. Two pages in this part turn on where in that order a thing
sits — command functions near the top, an advancement's flush at the end of a
player's own tick — and neither is legible without the order itself.

[Codecs, NBT and JSON](../foundations/codecs-nbt-json.md) and
[the data-driven type pattern](../foundations/data-driven-types.md#the-idea-stated-once)
from Part II. Dialogs and game tests are the pattern's clearest two
instances — a form and a test suite, both reduced to JSON dispatching on a
registry of types — and the pattern page is where that argument is made.

[The connection](../networking/the-connection.md#one-packet-there-and-one-back)
from Part IX, for the Netty-thread / server-thread boundary that the command
packets cross in two different ways on purpose.

[Contexts and predicates](../items/contexts-and-predicates.md) from Part
VII, if you are here for advancements: a trigger's conditions are loot
conditions, evaluated against a loot context, and that page owns the
machine — as it owns `/execute if predicate`, which a selector's own
*predicate* option is the second caller of.

## Watch in this order

1. [Brigadier and commands](brigadier-and-commands.md) — three parsers for
   one string, and a tab-completion whose fast path never leaves the
   machine. Also: which sixty-two of the four hundred and fifty-nine
   argument nodes do leave it, and why they feel like all of them.
2. [Permissions](permissions.md) — the biggest API break in the game since
   the flattening. A permission is no longer an integer, an operator does
   not have everything, and a permission failure is reported as a typo.
3. [Entity selectors](entity-selectors.md) — a selector is a compiled
   query, and eight of its twenty-one options are not filters but the query
   plan. Why *@p* crosses dimensions, why *sort=nearest* is what takes your
   *limit* away, and why one permission is checked twice.
4. [The execution engine](the-execution-engine.md) — a command engine with
   no Java recursion. A fan-out that materialises one player at a time, and
   a `/return` that deletes work out of a queue rather than unwinding a
   stack.
5. [Functions and macros](functions-and-macros.md) — what a `.mcfunction`
   file becomes, in two steps, the second of which usually does nothing.
   The one that fails silently every tick, forever.
6. [Advancements](advancements.md) — the game's general-purpose "tell me
   when the player does X", built as a per-player subscription table that
   shrinks as criteria are met and is rebuilt when one is revoked. The tree
   is laid out on the server and shipped.
7. [Scores, teams and stored data](scoreboard-and-data.md) — one number per
   thing, one query language for any tag, a boss bar, and the `execute store`
   seam that joins all three. Why fake players exist.
8. [Dialogs](dialogs.md) — a data pack puts a form on your screen, possibly
   before you are in a world at all. The values are read at the moment of
   the click and not before.
9. [Game tests](game-tests.md) — the game's own test suite, as a data pack.
   The annotations are gone, a batch *is* an environment, and the shipped
   jar contains exactly one test.

## Where the part stops

Not quite a third of this part by line is the catalogue rather than the
machinery, and it is where the unexplained lines are. The honest answer to what is unexplained is that nearly all of it is one more
instance of something a page above already draws. The **fifty-odd commands**
nobody names are the door table's premise repeated:
`SpreadPlayersCommand`, `FillCommand`, `TeleportCommand`, `WorldBorderCommand`
and their neighbours are each a Brigadier registration and a call into another
part. The **thirty-five unnamed advancement triggers** and the **concrete
predicates** beside them are instances of two shapes
[advancements](advancements.md#what-the-package-holds-that-this-page-does-not-name)
states and then declines to enumerate. The **argument types** are the same
again — [Brigadier and commands](brigadier-and-commands.md#the-tree-on-the-wire)
explains the wire form and names the families rather than the fifty-seven.

What is genuinely not here is a lecture on the three commands that are
*algorithms* rather than doors — `SpreadPlayersCommand`'s scatter,
`CloneCommands`' overlap handling, `FillCommand`'s replace modes. Each is a
self-contained routine that belongs to no other part, and three unrelated
routines do not make one lecture; they are named here so that a reader knows
the omission is deliberate.

## Reference this part uses

[Packets](../../reference/packets.md) for this part's own traffic. The two
systems that only *report* have no serverbound packet at all between them —
the scoreboard's five and the boss bar's one run one way — while everything a
player *does* comes back: the command and its suggestions, a dialog's click,
an advancement tab, and the two a test block's edit screens send.
[Registries](../../reference/registries.md) and
[the data-driven type pattern](../foundations/data-driven-types.md) for the
six type registries dialogs and tests dispatch on.
[Loot context parameter sets](../../reference/loot-context-params.md) for the
sets an advancement trigger and an advancement reward run in.
[Diagram lanes](../../reference/lanes.md) for the abbreviations these figures
use, and [the glossary](../../reference/glossary.md) for *Brigadier*,
*selector head*, *world-limited*, *criterion*, *objective*, *macro*, *boss
bar*, *dialog* and *game test*.

---

*Rules: names, never code · how the system works, not how the code reads ·
newest version only · every backticked name passes `tools/verify_names.py`.*
