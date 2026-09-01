# Brigadier and commands

> Verified against **Minecraft 26.2** · Part XII · `/give @p diamond_sword[minecraft:damage=5]`: two parsers for one string, a permission system that is no longer an integer, and a tab-completion that usually never leaves the machine.

## Responsibility

A command is a string typed by a human that has to become a call with typed
arguments, checked against permissions, on the server. Brigadier — Mojang's
parsing library, outside the game's own packages — supplies the shape: a **tree** of
literal and argument nodes, each with a requirement predicate, each
optionally executable. Everything on this page is what Minecraft builds on
top of that: the argument types, the source object, the permission model,
the serialisation of the tree to the client, and the two places the same
string gets parsed.

The single most important structural fact: **the client has a real
dispatcher too.** It is not a lookup table of strings. The server sends the
tree, the client rebuilds it with working parsers instantiated against its
own registries, and uses it for highlighting, usage text and most
completion. That is why tab-completing an item id is instant and
tab-completing a loot table is not.

The one sentence a player would recognise: *the grey ghost text and the red
underline in the chat box.*

## The data it owns

- **`Commands`** — the one server-side `CommandDispatcher` and every
  registration. `Commands.CommandSelection` gates which commands exist at
  all (integrated versus dedicated). `Commands.literal` and
  `Commands.argument` are the builder shorthands every command file uses,
  and `Commands.hasPermission` is the new requirement idiom.
  `Commands.CURRENT_EXECUTION_CONTEXT` is a thread-local that makes nested
  command execution reuse one queue instead of recursing
  ([execution and functions](execution-and-functions.md)).
- **`CommandSourceStack`** — *who is running this, from where*. Immutable;
  every wither returns a copy. It carries a `CommandSource` (the
  output sink), a position, rotation and anchor, a `ServerLevel`, a
  `MinecraftServer`, an entity, a `PermissionSet`, a silence flag, a
  `CommandResultCallback` and a `CommandSigningContext`. It implements both
  `SharedSuggestionProvider` and `ExecutionCommandSource`, which is why one
  object serves parsing, suggesting, executing and reporting.
  `CommandSourceStack.sendSuccess` takes a *supplier*, so the message is
  never built when nobody will see it.
- **`CommandSource`** — the output end alone: `CommandSource.NULL`,
  `CommandSource.acceptsSuccess`, `CommandSource.shouldInformAdmins`. A
  command block, RCON and the console differ only here.
- **`CommandBuildContext`** — a `HolderLookup.Provider` plus
  `CommandBuildContext.enabledFeatures`. Argument types that need registries
  take one, which is how a data-pack biome becomes tab-completable without a
  code change.
- **The argument types** (`net/minecraft/commands/arguments`) — about forty
  files plus the block, item, coordinate and selector
  subpackages. The ones that carry the weight: `EntityArgument` and its
  `EntitySelector` / `EntitySelectorParser`; `ResourceArgument` (yields a
  `Holder.Reference`), `ResourceKeyArgument` (yields a key, resolved
  later), `ResourceOrIdArgument` (an id **or** an inline literal),
  `ResourceOrTagArgument` and `ResourceSelectorArgument` (glob patterns
  over ids); `ItemArgument` with `ItemParser` and `ItemInput`;
  `BlockStateArgument` with `BlockStateParser` and `BlockInput`;
  `ComponentArgument`; `MessageArgument`; and the coordinate family built
  on `WorldCoordinate` and `Coordinates`. `IdentifierArgument` is the class
  a 1.21 reader knows under another name — its registry id is unchanged.
- **`ArgumentTypeInfo`** and **`ArgumentTypeInfos`**
  (`net/minecraft/commands/synchronization`) — the wire description of an
  argument type. `ArgumentTypeInfo.Template` is a *recipe*: it can be
  written to a buffer and `ArgumentTypeInfo.Template.instantiate`d against a
  `CommandBuildContext` on the other side. `SingletonArgumentInfo` is the
  common case and writes nothing at all.
- **`SuggestionProviders`** — the named providers a node can ask for;
  `SuggestionProviders.ASK_SERVER` is the round trip.
- **The permission package** (`net/minecraft/server/permissions`) — see
  below. `PermissionSet`, `Permission`, `Permissions`, `PermissionLevel`,
  `PermissionCheck`, `PermissionProviderCheck`, `LevelBasedPermissionSet`,
  `PermissionSetUnion`, `PermissionSetSupplier`.
- **`ClientSuggestionProvider`** — the client's `SharedSuggestionProvider`:
  the tab list, the looked-at block and entity, and the one method that
  sends a packet.
- **`SignableCommand`**, **`SignedArgument`**, **`ArgumentSignatures`**,
  **`CommandSigningContext`** — the signed-argument plumbing. Chat signing
  itself belongs to [chat and signing](../networking/chat-and-signing.md);
  what lives here is the walk over a parse to find which arguments need a
  signature, and the map that carries them afterwards.

## When it runs

Everything server-side is the server thread, but the two inbound packets
get there differently, and the difference is deliberate:

- `ServerboundCommandSuggestionPacket` goes through
  `PacketUtils.ensureRunningOnSameThread`, so the parse happens on the main
  thread.
- `ServerboundChatCommandPacket` does **not**. Its handler runs the
  character-legality check on the Netty thread — and may disconnect from
  there — before handing the body to `MinecraftServer.execute`. Everything
  after that (the authoritative parse, the permission check, the execution,
  the spam throttle) is on the main thread. The asymmetry is the same one
  [the connection](../networking/the-connection.md) describes: cheap
  validation early, game state never.

Function compilation is the third case: `ServerFunctionLibrary` parses every
`.mcfunction` **off** the main thread during a reload, against a
`CommandSourceStack` with a null level and a null server. That constraint
is invisible until an argument type dereferences one of them.

## The trace: `/give`

```mermaid
sequenceDiagram
    participant CS as CommandSuggestions
    participant CSP as ClientSuggestionProvider
    participant CPL as ClientPacketListener
    participant SGPL as ServerGamePacketListenerImpl
    participant C as Commands
    participant EC as ExecutionContext
    participant GC as GiveCommand

    CS->>CPL: parse against the client's own dispatcher — highlighting only
    CS->>CSP: getCompletionSuggestions — item ids and components, all local
    CSP->>SGPL: ServerboundCommandSuggestionPacket — only if a node asks the server
    SGPL->>CPL: ClientboundCommandSuggestionsPacket — capped at a thousand, id-matched
    CPL->>SGPL: ServerboundChatCommandPacket — the raw string; no signatures for /give
    SGPL->>SGPL: illegal-character check on the Netty thread, then hand to the server thread
    SGPL->>C: parse again, authoritatively, with the player's real source
    C->>C: CommandNode.canUse — the permission check lives inside the parse
    C->>EC: executeCommandInContext — one queue, limits read from the level's game rules
    EC->>GC: the registered lambda — resolve the selector, build the ItemInput
    GC->>GC: Inventory.add, then sendSuccess and broadcast to admins
```

Each arrow is a decision.

**The client parses first, and throws the result away.**
`CommandSuggestions.updateCommandInfo` runs the whole string through the
client's dispatcher every keystroke. That parse produces the red underline,
the grey usage hint and the completion list. It is *never* sent and never
trusted; the string is.

**Most completion never leaves the machine.** `ItemArgument` and
`BlockStateArgument` are registered as context-aware singletons, so the
client instantiated a real `ItemParser` and a real `BlockStateParser`
against its own registries. Item ids, data components and block properties
complete locally. The round trip happens only when a node reaches
`SharedSuggestionProvider.customSuggestion` — in practice when
`ClientSuggestionProvider.suggestRegistryElements` cannot find a
server-only registry (loot tables, advancements, recipes, functions). No
vanilla command attaches `SuggestionProviders.ASK_SERVER` explicitly; the
round trip is a fallback, not a design.

**Suggestion replies are matched by id.**
`ClientSuggestionProvider.customSuggestion` cancels the in-flight future
and increments a counter; the completion resolves only if the
id matches, so a slow reply for an older prefix is dropped rather than
flashing stale entries.

**Enter parses a third time, on the client, for one reason only.**
`ClientPacketListener.sendCommand` runs `SignableCommand.of` to find out
whether any argument is a `SignedArgument`. `/give` has none, so the plain
packet goes. A `/msg` would take a timestamp, a salt and the last-seen
message set, sign each signable argument, and send the signed variant.

**The authoritative parse is the server's, with the player's source.**
`ServerPlayer.createCommandSourceStack` fills in the real `PermissionSet`,
and Brigadier consults the node's requirement *during* the parse — which is
why a permission failure is reported as an unknown command.

**Execution is a queue, not a call.** `Commands.performCommand` flattens
the parse into a flattened context chain and hands it to an `ExecutionContext`; the
limits come from the level's game rules, read once. That machinery is the
subject of [execution and functions](execution-and-functions.md).

**`/give` itself is unremarkable and instructive.**
`EntityArgument.getPlayers` resolves the selector — re-checking the
entity-selector permission at *run* time, not parse time —
`ItemArgument.getItem` hands over the `ItemInput` built during parsing,
`ItemInput.createItemStack` validates it, and the stacks go through
`Inventory.add` ([items and stacks](../items/items-and-stacks.md)). Success
goes to `CommandSourceStack.sendSuccess`, which broadcasts to admins under
two game rules.

## The permission model

This is the part that changed most, and the part every mod and plugin will
notice first: **a permission is no longer an integer.**

- A **`Permission`** is one of two shapes: `Permission.Atom`, a named
  capability with an `Identifier`, or `Permission.HasCommandLevel`, an
  ordered level. `Permissions` holds the vanilla ones —
  `Permissions.COMMANDS_GAMEMASTER` and its siblings,
  `Permissions.COMMANDS_ENTITY_SELECTORS`, and the chat atoms.
- A **`PermissionSet`** answers `PermissionSet.hasPermission` for one
  permission. `PermissionSet.union` composes two; `PermissionSetUnion` is
  the OR, and it refuses to nest.
- **`LevelBasedPermissionSet`** is the ordinary implementation: it carries
  one `PermissionLevel` (all the way to owner, still numbered zero to four) and satisfies a
  `Permission.HasCommandLevel` at or below it — plus, hard-coded, the
  entity-selector atom from gamemaster upward. **It answers false to every
  other atom.**
- A **`PermissionCheck`** is `PermissionCheck.Require` or
  `PermissionCheck.AlwaysPass`, and `PermissionProviderCheck` wraps one as
  the predicate that actually sits on a command node.
  `Commands.LEVEL_GAMEMASTERS` and its siblings are these checks — the
  names survived, the type did not.
- Both `Permission` and `PermissionCheck` are codec-dispatched over
  registries. Those registries are **code-only**: the codecs exist to
  serialise the tree into the generated command report and to give mods a
  hook, not to load permissions from a data pack. There is no permissions
  file in a data pack.

Where a set comes from: `MinecraftServer.getProfilePermissions` resolves the
ops file first, then singleplayer ownership, then the LAN "allow cheats"
flag, then the server's configured operator level. `ops.json` still stores
an integer and the wire still carries one — the op level reaches the client
as one of five values on `ClientboundEntityEventPacket`, which is why the
client can never learn about atoms at all.

## Interfaces

- **Called by:** `ServerGamePacketListenerImpl` for typed commands and
  suggestions; `Commands.performPrefixedCommand` for command blocks, signs,
  RCON and the console; `ServerFunctionManager` for functions.
- **Calls into:** effectively the whole game — every command file in
  `net/minecraft/server/commands` and `net/minecraft/commands`. The
  registries, through the resource argument family; the loot system through
  `ResourceOrIdArgument`; `ServerFunctionManager` through `FunctionArgument`
  and `CacheableFunction`.
- **Crosses the network as:** `ClientboundCommandsPacket` (the tree),
  `ServerboundChatCommandPacket` and `ServerboundChatCommandSignedPacket`
  (execution), `ServerboundCommandSuggestionPacket` and
  `ClientboundCommandSuggestionsPacket` (completion), and
  `ClientboundEntityEventPacket` for the op level. See
  [what the client is told](../networking/what-the-client-is-told.md).
- **Data-driven by:** every dynamic registry (a pack's biomes, structures,
  enchantments, loot tables and dialogs are completable and parseable for
  free, because the argument names the registry key on the wire), plus
  functions and function tags. Text components in JSON get their selectors,
  NBT paths and coordinates parsed **at pack load**, through
  `CompilableString`, and a bad one fails the pack rather than the command.

## The tree on the wire

`Commands.sendCommands` makes a deep copy of the dispatcher's tree filtered
by each node's requirement for that player's source, and serialises it.
Argument nodes carry the registry id of their `ArgumentTypeInfo` plus
whatever the template writes — usually nothing, sometimes a flags byte
(`EntityArgument`: single, players-only) or a registry key. The client then
*builds real parsers* from those templates.

Two separate elisions:

- **Absent** — a node whose requirement the player fails is simply not in the
  packet, and because the filter is recursive, a gated literal takes its
  whole subtree with it.
- **Flagged** — `ClientboundCommandsPacket.FLAG_RESTRICTED` marks a node
  whose requirement fails for a *no-permission* source. It says "this needs
  some permission", independently of this player. The client turns it into
  a synthetic permission so it can keep two dispatcher views: the normal
  one, in which restricted nodes still highlight and suggest, and a
  restricted one used by `ClientPacketListener.verifyCommand` to tell "you
  would need permission for this" apart from "this is a typo" — which is
  how a click-event command gets a confirmation dialog instead of silently
  failing.

The packet is sent on join, on respawn, on a dimension change, on op and
deop, and on the LAN cheats toggle. It is **not** sent after `/reload`.

## The commands that reach into other systems

Most of `net/minecraft/server/commands` is a thin lambda over machinery
another part of this corpus owns. These are the ones worth naming, because
a reader looking for "how does `/locate` work" wants the *mechanism* page,
not this one:

- **`LocateCommand`** — and its two halves are barely related.
  `LocateCommand.locateStructure` can **drive world generation on the server
  thread**, because deciding whether a structure is at a chunk means asking
  the structure check; `LocateCommand.locateBiome` asks the biome source and
  never reads a stored palette at all
  ([structures](../worldgen/structures.md), [biomes](../worldgen/biomes.md)).
- **`FillBiomeCommand`** — writes the biome palette of the affected sections
  and resends them; the only command that edits a chunk's biomes
  ([chunk anatomy](../world/chunk-anatomy.md)).
- **`PlaceCommand`** — three entries into Part XI:
  `PlaceCommand.placeFeature` runs a configured feature with no placement
  layer, `PlaceCommand.placeStructure` lays out a whole structure, and
  `PlaceCommand.placeJigsaw` reaches jigsaw assembly directly
  ([features and placement](../worldgen/features-and-placement.md),
  [structures](../worldgen/structures.md)).
- **`LootCommand`** and **`ItemCommands`** — the second is the more
  interesting: `ItemCommands.applyModifier` runs a loot *function* over an
  existing stack, which is how `/item … with` edits an item in place
  ([loot tables](../items/loot-tables.md)). Both take a table or modifier
  through `ResourceOrIdArgument`, so an inline literal works where an id
  does.
- **`EnchantCommand`** and **`ExperienceCommand`** — thin faces over
  [enchantments](../items/enchantments.md) and
  [hunger, XP and effects](../player/hunger-xp-and-effects.md).
- **`DebugConfigCommand`** — the only vanilla caller of the play-to-
  configuration transition and back
  ([protocol phases](../networking/protocol-phases.md)).
- **`ExecuteCommand`** — not a command so much as the front end of the
  execution engine ([execution and functions](execution-and-functions.md)).
- **`DataPackCommand`** — enables and disables packs, then reloads
  ([the resource system](../foundations/resource-system.md)).

## Invariants and surprises

- **A permission failure is indistinguishable from a typo.** The
  requirement is consulted inside the parse, so an unopped player running
  `/give` is told the command is unknown. The client can tell the
  difference, but only for unattended (click-event) commands, never for
  what you type.
- **`/reload` invalidates the command tree and nobody is told.** A reload
  builds a whole new `Commands` and a whole new dispatcher, but the reload
  broadcast sends tags and recipes only. Clients keep completing against a
  dispatcher for a dead tree until they rejoin, change dimension or are
  op'd. The folklore that `/reload` refreshes tab-completion is false.
- **The node inspector's source has a null level and a null server.** Every
  requirement predicate in the game is evaluated against it once per
  command packet, to compute the restricted flag. A requirement that touches
  the level or the server crashes during *packet construction*, nowhere
  near the command.
- **`LevelBasedPermissionSet` grants exactly one atom.** A level-four
  operator's server-side set denies `Permissions.CHAT_SEND_COMMANDS` — the
  chat atoms live only in the client's own set. The two permission sets are
  not the same universe, and code that assumes an op has everything is
  wrong.
- **`Commands.LEVEL_MODERATORS` is used by no vanilla command.** The level
  exists, is settable, and gates nothing in the shipped game.
- **The suggestion reply is capped at a thousand entries**, silently.
- **An unknown argument type deletes a subtree rather than erroring.** A
  modded argument type reaching a vanilla client decodes to nothing, and
  the node's children are then never attached.
- **The execution limits are read once, from the outermost command's
  level.** An `/execute in` into another dimension does not pick up that
  dimension's game rules for the fork and sequence limits.
- **`MessageArgument` is the only signed argument in the game.** All of
  `ArgumentSignatures`, `SignableCommand` and `CommandSigningContext`
  exists to serve it and the handful of commands that take it.

## Where to look

`Commands` for what exists, `CommandSourceStack` for what a command knows,
`ArgumentTypeInfos` for the catalogue of argument types and their wire
forms, `net/minecraft/server/permissions` for the model that replaced the
integer, and `ClientboundCommandsPacket` for the one place the client and
server agree on a shape.

---

*Rules: names, never code · how the system works, not how the code reads ·
newest version only · every backticked name passes `tools/verify_names.py`.*
