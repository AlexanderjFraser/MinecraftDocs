# Pass 9 — the third fact-check (queue; opened 2026-09-05)

*Pass 9 re-runs pass 4's adversarial protocol — archived in
[pass4.md](pass4.md) with its charter, its agent brief
([pass4-brief.md](pass4-brief.md)) and its lessons — over the corpus passes
5–8 rewrite. This file is where every pass-5, -6, -7 and -8 session writes
down what pass 9 must check first: every page it rewrote, every claim a
rewrite introduced (a hook, a moved paragraph, a redrawn arrow, a re-scoped
count, a new section, a landing page's new argument), and every correction
it made with the decompile open. Pass 9 checks everything anyway; this list
decides what it checks first. It is also what made pass 4 checkable: from
Part VI on, the errors were in what the writing session did not know it had
changed, so a session lists what it changed on purpose and pass 9 reads the
rest harder.*

## How to write an entry

Per session, newest first, under `## Session X — Part N (pass M)`: the pages
rewritten; per page, one line per claim introduced, quoting the sentence;
the figures redrawn, and which orderings they assert; the material moved,
from where to where; and, under *Corrections*, every fact changed with the
decompile open — what the page said, what the decompile says, file and line.
Name the page in backticks on every line so a queue tool can route it.
Strike nothing here; pass 9 strikes.

## Standing items

- **A correction is a claim.** Pass 9 confirms the fix, not the original,
  and its close audits the pass's own strikes — session O of pass 4 found a
  strike that had settled nothing and a correction that was the error.
- **The summarisers are read last.** The thirteen landing pages,
  `lectures.md`, the glossary and the introduction are re-read after the
  pages they summarise are fixed, never before.
- **The figure against the section under it first**, before either is read
  against the source: nine pages in pass 4 had a diagram contradicting its
  own paragraph, and the prose was right every time.
- **Counts are call sites, not `grep -c` lines**; a generated page is
  checked by re-deriving the population, never a row.
- **Names inside mermaid blocks** are under a gate from pass 7's close; the
  23 ambiguous simple names the verifier prints are settled by pass 8 or in
  the tool.
- **Pass 9 adds nothing.** A gap it finds goes to [pass3.md](pass3.md) §7,
  the coverage queue, which seeds the second edition.

## Entries

## Pass 5, session I — Part IX · Networking *(2026-09-06)*

*Five pages plus the landing page, one reader-of-the-book agent each; the part
read end to end in watching order first. All six rewritten, and eleven pages
in seven other parts edited because a Part IX page's owner or duplicate lived
there. Everything below is either a claim this session introduced or a
correction it made with the decompile open; the corrections come first.*

### Corrections — what the page said, what the decompile says

1. **`networking/the-connection`:236 — the flush bracket's scope.** The page
   said "The bracket is opened around the whole server tick".
   `MinecraftServer.suspendFlushing` is called at the top of
   `MinecraftServer.tickChildren` (`MinecraftServer.java`:1209-1211) and
   `resumeFlushing` at its end (:1281), so the packet drain that runs before
   `tickChildren` is **outside** the bracket — which is what
   `server-tick`:215 and `players-and-sessions`:212-213 both turn on. Page
   against two other pages. The section is now cut to a citation and says the
   bracket opens at the top of `tickChildren`.
2. **`networking/the-connection`:122-124 — `PacketListener.onPacketError`.**
   The page said it "by default raises a reported crash", which is the
   interface default (`PacketListener.java`:19-21) and is reached by **no
   listener a drained packet arrives at**: `ServerPacketListener`
   (`ServerPacketListener.java`:13-16) overrides it to log *"suppressing
   error"* and return, `ServerCommonPacketListenerImpl` (:78-81) adds
   `MinecraftServer.reportPacketHandlingException`, and
   `ClientCommonPacketListenerImpl` (:113-120) overrides it the other way,
   storing a disconnection report and calling `Connection.disconnect`. A
   reader of the page alone concluded a bad packet crashes the server. Page
   against `server-tick`:122-126.
3. **`server/server-tick`:221-222 — where `Connection.tick` flushes.** The
   page said "at the end of the connection phase". `Connection.tick`
   (`Connection.java`:387-411) flushes fourth of six steps, after the
   disconnect check and before `tickSecond` — which its own step list at
   :186-188 already had right and `the-connection`:241 states as the point.
   Page against itself and against Part IX. (This was logged for pass 9 by
   session C at [pass9.md](pass9.md); it is fixed rather than carried.)
4. **`server/server-tick`:186 — "flush the deferred send queue".**
   `Connection.tick`'s first step is `Connection.flushQueue`, which drains
   `Connection.pendingActions`, a queue of **closures** (`Connection.java`:388);
   `Connection` holds no outbound packet queue at all, which is
   `the-connection`:406-408's own claim. The step is now named for what it
   drains.
5. **`networking/what-the-client-is-told`:213 — "**Four** feeds ignore gate
   3".** Outside the gate-3 block of `ServerEntity.sendChanges`
   (`ServerEntity.java`:92-271) there are **three** sends — the passenger diff
   (:96-101), the `ItemFrame` tenth-call branch (:105-131) and
   `Entity.hurtMarked` (:266-269) — plus `Entity.updateDataBeforeSync` (:93),
   which is a hook and not a feed. The page's own figure named three and
   `synched-entity-data`:281-283 counts the sends as two with the item frame
   called out separately. Corrected to three, with
   `Entity.updateDataBeforeSync` named in front of them.
6. **`networking/what-the-client-is-told`:346 — the block-entity hop.** The
   page had `ChunkHolder.broadcastBlockEntityIfNeeded` calling
   `BlockEntity.getUpdatePacket`. `ChunkHolder.java`:240-245 has *IfNeeded*
   testing `BlockState.hasBlockEntity` and delegating to
   `ChunkHolder.broadcastBlockEntity` (:247-258), which is the one call site
   of `getUpdatePacket`. `block-entities` named the inner one and was right.
   Page against page.
7. **`networking/what-the-client-is-told`:317 — "Once a tick".**
   `ServerChunkCache.broadcastChangedChunks` is called from
   `ServerChunkCache.tickChunks` (`ServerChunkCache.java`:345-362), inside the
   `!level.isDebug()` guard and only when the caller passed `tickChunks`, so
   it is once per *chunk-ticking* tick and never in a debug world — which
   `lighting`:293-295 and `server-level-tick`:86 both carry and this page did
   not. Page against two pages.
8. **`networking/what-the-client-is-told`:214-215 — "none of them helps a mob
   outside entity-ticking range".** Gate 2 is a disjunction, so a mob out of
   entity-ticking range still passes it on a section change or with
   `Entity.needsSync` set — which the page states twice below (:167-170,
   :430-432). Page against itself; the sentence now names the mob that fails
   *all three* disjuncts.
9. **`networking/chat-and-signing`:266-268 — "vanilla never sends one".** The
   Q&A said no unsigned copy is ever sent, contradicting the page's own
   :44-46 and :219-220. `MessageArgument.resolveChatMessage`
   (`MessageArgument.java`:46-58) calls `PlayerChatMessage.withUnsignedContent`
   with the resolved component on every message-argument command. Page against
   itself; the claim is now that the *decorator* never produces one.
10. **`networking/chat-and-signing`:44-46 — "sets it on every message it
    resolves".** `PlayerChatMessage.withUnsignedContent`
    (`PlayerChatMessage.java`:44-48) keeps the copy only when it differs from
    `Component.literal(signedContent)`, so a command message with no selector
    in it carries none. Corrected to "differs exactly when a selector
    expanded".
11. **`player/player-anatomy`:245 — `ProfileKeyPair` on a `ServerPlayer`.**
    There is no `ProfileKeyPair` anywhere under `net/minecraft/server`; what
    `ServerPlayer` holds is `ServerPlayer.chatSession`, a `RemoteChatSession`
    (`ServerPlayer.java`:281), and the key pair lives on the client inside a
    `LocalChatSession`. Page against `chat-and-signing`:286-290.
    `player/README`:143 said the same thing and is corrected with it.
12. **`networking/packets-and-stream-codecs`:367-375 — an absolute "never".**
    "Client-supplied component *contents* never cross the wire at all" is
    falsified twenty lines above by the creative slot, which the same page
    calls the one packet that carries an arbitrary item. Scoped to the
    container click.
13. **`networking/packets-and-stream-codecs`:302-305 — a broken sentence** on
    a numeric claim ("with `BundlerInfo.BUNDLE_SIZE_LIMIT` caps a bundle at
    4,096"). Rewritten; 4,096 re-derived (`BundlerInfo.java`:13), and
    `BundlePacket`'s relation to `ClientboundBundlePacket` stated (abstract
    class and its one subclass, `ClientboundBundlePacket.java`:7).
14. **`networking/packets-and-stream-codecs`:335-344 — trust and direction.**
    The paragraph said trust is "about the read budget rather than about
    direction" and then "The rule is direction". Both halves are true of
    different things and the page asserted and denied one claim; now the
    *mechanism* is a budget and the *rule for choosing* is direction.
15. **`networking/README`:84-86 — "the only system in the book designed
    against an adversary".** False against page two of its own part, which has
    a section headed *What stops a hostile sender*. Narrowed to a *lying*
    peer against a malformed one, which is the real difference.
16. **`networking/README`:78-80 against :106-108 — an internal
    contradiction.** The watch-order line said the player object is built in
    this part; *where the part stops* said how a `ServerPlayer` comes to exist
    is Part III's. Both now say the same thing.
17. **`networking/protocol-phases`:60 — a table cell naming the wrong kind of
    thing.** The status row's clientbound listener was "reached from
    `ServerStatusPinger`" where every other cell names a listener; it is an
    anonymous `ClientStatusPacketListener` inside that class
    (`ServerStatusPinger.java`:71).

**Four suspicions re-derived and found sound**, recorded because a strike is a
claim: `IdDispatchCodec`'s "not a table the encoder walks" (it is a
`Object2IntMap` lookup and then an indexed list, `IdDispatchCodec.java`:46-67 —
no walk, so the sentence stands); the five-minute server and seven-minute
client chat expiries (`PlayerChatMessage.java`:30-31, exactly 5 and 5+2);
`ServerEntity.FORCED_TELEPORT_PERIOD` as 400 gated calls
(`ServerEntity.java`:59); and the two places the join reads the whole save
file, which `protocol-phases` put in `spawnPlayer` and `players-and-sessions`
in `PrepareSpawnTask.Ready` — both right, since `spawnPlayer` delegates to
`Ready.spawn` (`PrepareSpawnTask.java`:123-131, 225-240); the two pages now
name it the same way.

### Claims introduced

**`networking/README` (rewritten to the role).**
- The part's shape sentence is now "**the wire three times, and two things it
  carries**", replacing "one wire and three passengers", which the page
  contradicted twenty lines below and which `lectures.md` carried in its
  un-softened form. The claim is that lectures 1–3 are all descriptions of the
  wire and 4–5 are applications of the play phase.
- **The figure is redrawn** to two subgraphs — *the wire, described three
  ways* over the chain `TC → PSC → PP`, and *what it carries* over `WCT` and
  `CS` — with one labelled edge between them replacing the two unlabelled
  arrows `PP --> WCT` and `PP --> CS`, which asserted a dependency the page's
  own :88-91 denies. Verified before redrawing that neither target page names
  `protocol-phases`, `ConnectionProtocol` or `ProtocolInfo`.
- The opening's four player-visible failures are replaced: two of the old four
  (the rubber-band, the block that comes back) are paid off only in Parts VIII
  and X, and one (the grey bar) nowhere in the book. The new four —
  *Connection lost*, the mob that freezes and jumps, the chest that says
  nothing until opened, the red chat line that takes the rest of the session
  with it — are each answered on a page of this part.
- The traffic-volume clause is kept and re-purposed as the reason two of five
  lectures take most of the part's length.
- **A new *Where the part stops* section** with the size through
  `{{#include ../../generated/part-networking.md}}`, and the coverage
  argument: **this part owns the wire, not everything in `network/`** —
  `network/chat` is Part II's, much of `client/multiplayer` is Part X's, and
  the largest block is the packet classes, which are catalogued and not
  narrated. Three systems are named and declined with a reason: player
  reporting (already out of scope on `what-this-book-skips`), the server list
  and its screen (Part XI's to draw), and the boss-bar feed, whose sending
  side has no owner anywhere in the book.
- *Reference this part uses* now lists `level-data-and-rules`, which a page of
  the part actually cites, and drops nothing.

**`networking/the-connection`.**
- Keep-alive is stated as the *common* listener's, so it runs in
  configuration, and takes in two facts from `players-and-sessions`: that a
  wrong-id answer disconnects immediately rather than being ignored, and that
  the round trip is smoothed three parts old to one part new, so a tab list
  lags a real latency change by several pings.
- The memory-connection crash answer takes both disconnect strings in from
  `server-tick` and states them as one catch with two branches.
- **New coverage passage**: `client/multiplayer/resolver` —
  `ServerAddress.parseString`, `ServerNameResolver`, `ServerRedirectHandler`'s
  `_minecraft._tcp` SRV lookup, `AddressCheck` and `ResolvedServerAddress` —
  written from `ServerNameResolver.java`:21-38 and
  `ServerRedirectHandler.java`:42. Plus `ServerList`/`ServerData` named in the
  clause that already described them, `LegacyServerPinger` as the client half
  of the legacy-query row, and `Varint21LengthFieldPrepender` named in the
  outbound pipeline list where only the string `"prepender"` stood.

**`networking/packets-and-stream-codecs`.**
- **New passage on the per-phase listener interfaces** —
  `ClientGamePacketListener` and `ServerGamePacketListener` (390 lines
  between them), the common pair, the six phase pairs and the two roots — as
  what `Packet.handle` targets, which the page asserted and never named. The
  claim that a listener of the wrong shape is the cast failure
  `the-connection` describes.
- **New clause on the login-phase payload family** (`CustomQueryPayload`,
  `CustomQueryAnswerPayload` and the discarding forms), because the section
  called `CustomPacketPayload` "the one seam" and the login twin exists.
- The trusted pairs now carry their call-site counts, moved in from
  `codecs-nbt-json`: `TRUSTED_COMPOUND_TAG` has exactly one
  (`ClientboundBlockEntityDataPacket`), `TRUSTED_TAG` none at all, and
  `ComponentSerialization.TRUSTED_STREAM_CODEC` is used by every clientbound
  chat packet — which pays off `text-components`:236's inbound promise and is
  the codec the page's own figure draws (verified against
  `ClientboundSystemChatPacket.java`:13 and
  `ClientboundPlayerChatPacket.java`:22).
- The three-layer serverbound defence, moved in from `codecs-nbt-json`, and
  `ItemStack.CODEC` named as what the validating re-encode runs;
  `ServerGamePacketListenerImpl` named as the server's creative context.
- **"the other *eight* templates — nine in all"** stated once here, where the
  page had "every other template" and `protocol-phases` had a bare correction.

**`networking/protocol-phases`.**
- The registry-and-tag-sync passage is cut to what belongs to a *phase* — the
  order and the count of packets — with the mechanism cited to
  `identifiers-and-registries#when-a-world-opens`. The claim retained here is
  that nothing is applied as it arrives.
- The play-binding paragraph is cut to one sentence whose claim is new in this
  form: the configuration-to-play switch is **the only transition in a
  connection's life that changes what a packet number means as well as which
  packets are legal**.
- `PrepareSpawnTask`'s internals are cut to the two states and the hook, with
  the page keeping "everything between the join task and that handler is a
  server holding a ticket on chunks for a player that does not exist" as its
  own.
- `ClientboundCodeOfConductPacket` and `ServerboundAcceptCodeOfConductPacket`
  named, and `ServerboundCustomQueryAnswerPacket` named where the page had
  only the request side.
- The creative filter and the compression asymmetry are cut to one clause and
  a citation each.

**`networking/what-the-client-is-told`.**
- **`Entity.updateDataBeforeSync` added to the prose and the figure**, ahead
  of the gate-3 branch, with the claim that an effect expiring this tick can
  dirty the container and open its own gate in the same call.
- **New paragraph after the gate-3 table**: the interval gate covers the
  synched-data flush as well as the position block; the `ItemFrame` branch is
  the *only* path to that flush which skips the interval test; and
  `ServerEntity.handleMinecartPosRot` reaches it from inside the gate. All
  three moved from `synched-entity-data` (session F's routed list, discharged).
- Two table rows gain the numbers `movement-and-collision` had and this page
  did not: `FORCED_TELEPORT_PERIOD` as four hundred *gated* calls, "at least
  1,200 ticks on the default interval", and that the ground-flag row is the
  common case.
- `VecDeltaCodec` named in the prose as the object holding the dead-reckoning
  base, where it had appeared only in *Where to look*;
  `ClientboundSetPassengersPacket` and `ClientboundSetEntityLinkPacket` named
  in the feeds and the pairing bundle.
- The chunk enter/leave section and the view's shape are cut to two sentences
  citing `tickets-and-loading`, keeping only `ChunkTrackingView.Positioned`,
  which no other page names; the light audience is cut to one sentence citing
  `lighting`; both block-entity default statements are cut to the consequence
  citing `block-entities`.

**`networking/chat-and-signing`.**
- **New passage on the text filter** — `TextFilter`, `TextFilter.DUMMY`,
  `MinecraftServer.createTextFilterForPlayer`,
  `ServerTextFilter.createFromConfig` and its two implementations,
  `FilteredText` and `Filterable` — with the claim that a vanilla server has
  no filter at all and that filtering here is never destructive, because a
  `FilterMask` travels with the message and is applied per recipient. Written
  from `ServerTextFilter.java`:72-108, `TextFilter.java`:9-19,
  `FilteredText.java`, `Filterable.java`:11 and `MinecraftServer.java`:2290
  against `DedicatedServer.java`:826-828.
- `ChatTypeDecoration` named as the translation key and argument list behind
  the *someone said* wrapper, with the claim that the phrasing around a line
  is data and the line is not.
- `LastSeenTrackedEntry` named as the twenty slots, and `LocalChatSession` as
  what holds the key pair on the client.
- The selector-expansion fact is given one home on the page — the *Commands*
  section — with the mechanism cited to `text-components` and the enumeration
  of which commands to `brigadier-and-commands`; the opening keeps only the
  security consequence.
- The `ChatAbilities` paragraph is cut to a sentence and a link, with the four
  atoms' effects moved to `commands/permissions`.

**Pages in other parts, edited because they held or contradicted Part IX
material.**
- `server/players-and-sessions`: the chunk-batch pacing cut to "a joining
  client is trusted with one batch" plus the claim that the first batch is a
  hard round trip; the keep-alive mechanism cut to a citation, keeping the
  asymmetry the section is about; the reconfigure cut to *a leave that keeps
  the socket* with the phase half cited to `protocol-phases`.
- `server/server-tick`: `Connection.tick`'s step list corrected (above), the
  chunk-pacing citation repointed from `tickets-and-loading` to
  `what-the-client-is-told#the-rate-the-client-asks-for` (the first of the two
  citations `pass5.md`:89-95 left for this session; the second is
  `players-and-sessions`:266, done above), and the memory-connection sentence
  cut to a citation.
- `foundations/identifiers-and-registries`: takes two facts from
  `protocol-phases` — that `PackLocationInfo.knownPackInfo` is an optional, so
  a world's own datapack is absent from the request, and that the client's
  load is dispatched to a background executor and then blocked on.
- `foundations/codecs-nbt-json`: the *Trusted, untrusted and validated*
  section rewritten to what this page owns — that the serverbound path is the
  only one of its four where a codec is run for its errors rather than its
  output, and that the persistent codec is used as a validator for the wire
  one. The trusted-pair enumeration and the three fences moved to Part IX.
- `commands/permissions`: gains what the four chat atoms *do*
  (`ChatAbilities.java`:71-83).
- `commands/brigadier-and-commands`: the fourth telling of the chat Netty hop
  cut to a citation of `server-tick` and `chat-and-signing`, keeping the claim
  that matters for a command — the validation that can disconnect you runs
  before the parse.
- `commands/dialogs`:8-9 repointed: `ClientboundShowDialogPacket`'s two
  protocols are `packets-and-stream-codecs`', not `protocol-phases`'.
- `entities/entity-anatomy`:38's `ServerEntity` row repointed from gate 1 to
  gate 3, which is the section that answers it.
- `anatomy/anatomy`:128 now sends the memory channel to `the-connection` as
  well as the phase walk; `reference/threads` gains a link to
  `protocol-phases#login` for the state machine it was explaining.
- `player/player-anatomy` and `player/README`: correction 11.
- `src/lectures.md` and `src/reference/glossary.md` re-synced: the Part IX
  shape paragraph follows the landing page, the jitter clause follows its
  owner (`the-client-loop` says *most*), *Protocol phase* spells
  *handshaking* as the page does, and *Packet* drops the unsupported "roughly
  half the implementations are records" for "three shapes", which is what the
  owner says. Six glossary owner links gain anchors.

**Anchors.** Part IX carried **7 anchors on 62 cross-part links** before this
session — the sixth part running to arrive with almost none — and carries 67
now, plus 23 within the part. Each asserts that the named section is the
answer; `check_links.py` proves only that the heading exists.

### For pass 9's attention, found and not fixed

- `reference/glossary`:437-440 previously said "roughly half the
  implementations [of `Packet`] are records", which no page supports; it now
  says "three shapes", which the owner page does support but does not count.
  A count either page could state and neither does.
- `chat-and-signing`:139-140 counts "the first fifteen rows" of its check
  table by hand; correct as it stands, and wrong the moment a row is added.
- `chat-and-signing`:100-101 uses "expired" for `hasExpiredServer`, which is
  five minutes; the number appears only in the Q&A at :262-263. True but
  stated in two places in two vocabularies.
- Whether a respawn clears a broken chat chain. `ServerPlayer.restoreFrom`
  copies `chatSession` (`ServerPlayer.java`:1729) but the chain decoder lives
  on `ServerGamePacketListenerImpl` (:274), which survives a respawn — so a
  broken chain almost certainly survives dying. Not written, because it is a
  new claim and the page did not raise it; logged in
  [pass5.md](pass5.md) for pass 6.
- `foundations/text-components` tells the `/say @a` punchline twice on its own
  page (:274-275 body and :425-432 Q&A). Part II's, and a page-shape finding;
  logged for pass 6.

## Pass 5, session H — Part VIII · The player *(2026-09-06)*

All seven pages of Part VIII touched plus the landing page:
`src/systems/player/README.md` (rewritten to the landing-page role, gaining a
*where the part stops*), `player-anatomy.md`, `the-two-phase-tick.md`,
`input-to-movement.md`, `the-sword-swing.md`, `the-spear.md`,
`hunger-and-experience.md`, `status-effects.md`. Nine pages in six other parts
edited because a Part VIII page's owner or duplicate lived there:
`entities/README.md`, `entities/attributes.md`, `entities/damage-and-death.md`,
`blocks/block-interaction.md`, `server/players-and-sessions.md`,
`server/server-tick.md`, `items/using-an-item.md`,
`foundations/data-driven-types.md`, `reference/non-living-damage.md`. Plus
`reference/glossary.md`, the Part VIII block of `src/lectures.md` and
`reference/level-data-and-rules.md`'s *four parts* paragraph. Part VIII has no
hand-kept Reference page of its own; `reference/non-living-damage.md` is Part
VI's and was edited here only to take an explanation off it.

### Corrections — the page was wrong, and the decompile says so

- **`player-anatomy`: `Avatar` does not exist for the renderer.** The page
  said "It exists for the renderer", and `Avatar` is in
  `server-classes.txt` (line 2363) — a server class. `Avatar.java` is 57
  lines holding the player-shaped `POSES`/dimensions, the 1.62 eye height,
  the two cosmetic synched values and the abstract `Avatar.getProfile`, and
  its two subclasses are `Player` (`Player.java`:129) and `Mannequin`
  (`Mannequin.java`:28). `AvatarRenderer` (`AvatarRenderer.java`:52) being
  generic over `Avatar & ClientAvatarEntity` is a consequence of the rung,
  not its cause. Rewritten to say the rung is what `Player` and `Mannequin`
  share, and reconciled with the other two accounts in the book
  (`entity-anatomy`:185 "its point is `Mannequin`", `attributes`:132 "the
  player-shaped hitbox but not the attribute set").
- **`the-sword-swing`: `Player.postPiercingAttack` is `LivingEntity`'s.**
  The method is declared once, at `LivingEntity.java`:1799, and `Player` has
  no override; `Player.java`:989 calls it. `the-spear` and
  `items/enchantments` already spelled it `LivingEntity.postPiercingAttack`,
  so the page disagreed with its own declared pair. Fixed, with a clause
  saying why a *piercing* hook closes an ordinary swing.
- **`the-sword-swing` and `entities/damage-and-death`:
  `LivingEntity.getSecondsToDisableBlocking` is conditional.**
  `LivingEntity.java`:4238-4243 returns `Weapon.disableBlockingForSeconds`
  only when `weaponItem == this.getActiveItem()`; both pages presented it as
  an unconditional read-back. Fixed on both, in the same wording. (Confirmed
  the practical scope: `getActiveItem` is the main-hand stack when nothing is
  being used, so an ordinary axe swing still disables a shield; the condition
  bites while the attacker is using something else.)
- **`player-anatomy`: `Player.HELD_ITEM_SLOT` is the cursor, not the selected
  slot.** Written new this session and corrected before it landed:
  `Player.java`:1710-1726 makes 499 the `containerMenu` carried stack.
- **`status-effects`: `MobEffectInstance.compareTo` orders both surfaces, in
  opposite directions.** The page said it "orders the icons in the HUD".
  `Hud.java`:537 sorts with `Ordering.natural().reverse()`;
  `EffectsInInventory.java`:66 sorts with `Ordering.natural()`. Corrected
  and the consequence stated. (Carried the standing queue entry at
  `pass5.md`:2536.)
- **`status-effects`: the ambient-particle numbers are exact.** "divides by
  about four" was 3.75. `LivingEntity.java`:908-911 has
  `bound = isInvisible() ? 15 : 4` and `ambientFactor = isAmbient ? 5 : 1`,
  rolled as `nextInt(bound * ambientFactor) == 0`. Rewritten as the two
  bounds and their product. (Carried `pass5.md`:858's Part VIII row.)
- **`server/players-and-sessions`: the flying kick's numbers moved, and the
  vehicle half was incomplete on both pages.**
  `ServerGamePacketListenerImpl.java`:346-355 runs a second counter,
  `aboveGroundVehicleTickCount`, against its own `getMaximumFlyingTicks(vehicle)`
  and only for the controlling passenger. `input-to-movement` now says so and
  Part III keeps a clause. (Carried `pass5.md`:209.)
- **`player-anatomy`: `DemoMode` written from the source.** Introduced this
  session, so listed as a claim: `MinecraftServer.java`:2295 constructs it
  (not `PlayerList`), and `DemoMode.java`:26-90 reads the level's *gameTime*,
  not a clock of its own; past `TOTAL_PLAY_TICKS` it overrides
  `handleBlockBreakAction` and `useItem` to answer with a reminder.

### Suspicions re-derived and found sound — no change made

- `the-two-phase-tick`:151, "the one thing that stops phase two is
  `MinecraftServer.isPaused`". `ServerGamePacketListenerImpl.java`:306 is
  `if (this.server.isPaused() || !this.tickPlayer())`. The claim stands.
- `input-to-movement`, "position must have moved by more than 2×10⁻⁴ blocks".
  `LocalPlayer.java`:285 compares `Mth.lengthSquared(...)` against
  `Mth.square(2.0E-4D)`, so the threshold really is 2×10⁻⁴ of distance, not
  of its square.
- `input-to-movement`:131, "Releases are always delivered".
  `KeyboardHandler.java`:602-603 calls `KeyMapping.set(key, false)` outside
  the `handlesGameInput` gate that presses sit behind. The claim stands, and
  it does not contradict `client/input-and-keybinds`, whose "swallowed
  release" is `ToggleKeyMapping`'s and a screen's `KeyMapping.releaseAll`.
- `the-spear`'s figure node "server side only" against
  `using-an-item`:8-9's "runs every tick on both sides".
  `ItemStack.java`:1170-1184 shows both: the method runs on both sides, and
  the divert to `KineticWeapon.damageEntities` is server-gated. No
  contradiction; logged for pass 7 as a compressed label.

### Claims introduced — the ownership cuts

Every trimmed sentence is a new claim, and every anchor asserts that the
named section is the answer. The cuts, each *from* → *to*:

- **The record–simulate–snap-back bracket**, from `input-to-movement`'s
  Q&A to `the-two-phase-tick#the-bracket-and-what-survives-it` — the page
  named after it. The riding qualifier (`Entity.rideTick` repositions a
  passenger every tick, so "never here" is an *on foot* claim) **moved** to
  the owner, and so did the naming of the pipeline
  (`LivingEntity.aiStep` / `LivingEntity.travel` / `Entity.move`).
- **The twin hook.** `the-two-phase-tick` and `input-to-movement` opened on
  the same surprising fact, two consecutive lectures apart.
  `input-to-movement`'s opening now ends on its own three surprises, which
  were already on the page.
- **The authority preamble**, told three times in the book. Both Part VIII
  copies cut to one sentence plus
  `authority#five-predicates-and-the-final-one-the-other-four-hang-off`;
  the fall-damage gate — its third full telling, `pass5.md`:2710 — cut to
  one sentence plus `authority#three-cases-read-on-both-sides` on both
  `the-two-phase-tick` and `input-to-movement`.
- **The Netty-thread survey**, from `the-two-phase-tick` to
  `server-tick#every-packet-since-last-time-in-one-drain`, which owns the
  rule. The count **moved** with it and was re-derived:
  `ServerGamePacketListenerImpl` declares 61 `public void handle*` methods
  and 52 call `PacketUtils.ensureRunningOnSameThread`; the nine that do not
  are `handleEditBook`, `handleChat`, `handleChatCommand`,
  `handleSignedChatCommand`, `handleChatAck`, `handlePingRequest`,
  `handleSignUpdate`, `handleConfigurationAcknowledged` and
  `handleCustomPayload`.
- **`Player.cannotAttack`'s two hooks and `Player.deflectProjectile`**, from
  `reference/non-living-damage` — where a Reference page held the book's
  only explanation, against `TEMPLATE.md` — **onto** `the-sword-swing`'s gate
  paragraph, with `Entity.isAttackable`, `Entity.skipAttackInteraction`,
  `Interaction`, `BlockAttachedEntity`, `EntityTypeTags.REDIRECTABLE_PROJECTILE`
  and the ghast fireball. The Reference page keeps one sentence and a link,
  and its `AbstractHurtingProjectile` row lost the same explanation.
  (`pass5.md`:2700, the oldest open entry on the page.)
- **`Entity.hurtOrSimulate`'s boolean**, the reverse move: the Reference
  page's sharper reading — *was anything damaged*, not *did the hit land* —
  is now on `the-sword-swing`, and both of that page's figures say the same.
- **The `hurtClient` roll-call**, cut from eight names to its count and its
  pattern, with the table cited. **The four-step client-tick order**, cut to
  its consequence with `the-client-loop#what-a-tick-is-in-order` cited.
  **The excluded-player sound rule** (its fourth telling), cut to a citation
  of `what-makes-a-sound`. **The i-frame counter's decrementers**, cut to a
  citation of `damage-and-death`.
- **`UseEffects`**, from `hunger-and-experience` to
  `using-an-item#moving-while-you-use`. Its vibration half **moved** with it
  and was written from the source: `ItemStack.causeUseVibration`
  (`ItemStack.java`:781-788) gates `Entity.gameEvent` on
  `UseEffects.interactVibrations`, called by `LivingEntity` at both ends of a
  use and by `FishingRodItem` and `BoneMealItem` for themselves.
  (`pass5.md`:2980.)
- **`Consumable`'s field roster and the five `ConsumeEffect` implementations**,
  from `hunger-and-experience` to `using-an-item`, which spends the component
  through its whole lecture and never defined it. `hunger-and-experience`
  keeps the *walk* — `ConsumableListener` and `Consumable.onConsume` — because
  the walk is its hook, and keeps `FoodProperties` and `FoodData.eat`. The
  ruling is written out in `pass5.md`. `foundations/data-driven-types`:184's
  `CONSUME_EFFECT_TYPE` row now points at the section that names them.
  (`pass5.md`:2969.)
- **The client replay of a meal**, cut on `hunger-and-experience` to a clause
  plus `using-an-item#the-meal-tick-by-tick`; the page keeps
  `ClientPacketListener.handleSetHealth`, which is the overwrite and its own.
- **Item ticking's two callers** and **the one-orb-per-tick sweep**, cut on
  `the-two-phase-tick` to their placement plus links to `player-anatomy` and
  `hunger-and-experience`. Session G's ruling that `player-anatomy` owns the
  forty-three-slot reason is kept; the page-VIII reader agent's counter-call
  for `items-and-stacks` was declined, in writing, in `pass5.md`.
- **The effect→attribute reload sentence**, the one move *into* Part VIII:
  `attributes`:213 explained that effects are restored from NBT without the
  apply hook running. `status-effects` now has a section for it, written from
  `LivingEntity.java`:762-765 and :818-828, and `attributes` keeps the
  half-sentence it needs.

### Claims introduced — coverage and new material

- `status-effects`: the per-effect `MobEffect` subclass family (`world/effect`
  holds nineteen classes, of which sixteen are one small subclass per effect
  plus `InstantaneousMobEffect`); `MobEffectCategory`'s three constants and
  its two readers (`PotionContents.java`:189 for tooltip colour,
  `Hud.java`:551 for the two-row split, which asks `MobEffect.isBeneficial`
  and so puts *neutral* on the bottom row with a blue tooltip); the reader of
  `LivingEntity.effectsDirty` (`LivingEntity.updateDirtyEffects`, from
  `Entity.updateDataBeforeSync` at the top of `ServerEntity.sendChanges`,
  `ServerEntity.java`:93 and :310); and the six-hundred-tick re-send named at
  last (`LivingEntity.java`:888, a bare literal).
- `player-anatomy`: the skin family — `PlayerSkin` (four textures, a
  `PlayerModelType` of `SLIM` or `WIDE`, a *secure* flag) and
  `PlayerModelPart`'s seven bits, read through
  `Avatar.DATA_PLAYER_MODE_CUSTOMISATION`; `DemoMode`; `Player.getSlot`'s
  command-facing addressing; `LocalPlayerResolver` as the tab-list-first
  profile lookup; `ProfileKeyPair` cross-linked to `chat-and-signing`; and
  `StackedContents` named as `items/recipes`' though it lives in this
  package.
- `the-spear`: the component table now says which subset it is — the nine
  are the *weapon*, and `Item.Properties.spear` also calls
  `durability`, `repairable` and `enchantable` from the material
  (`Item.java`:510). The spear's `UseEffects` row now states all three
  fields, which is its own component. And the charge's targets are named in
  prose for the first time — `KineticWeapon.damageEntities`
  (`KineticWeapon.java`:74-76) walks `ProjectileUtil.getHitEntitiesAlong`
  with `PiercingWeapon.canHitEntity` and the block-collider clip, exactly as
  the stab does; only the figure had said so. (`pass5.md`:2543.)
- `entities/README`: one clause declaring that `world/effect` is in Part VI's
  packages and its lecture is Part VIII's — the ruling is below.
- `player/README`: a *where the part stops* section, which the part had none
  of, with the size include, the upward border at `Avatar`, five outward
  borders, and two declared declines (`Hotbar`/`HotbarManager` as the
  creative screen's; the player half of sleep as a real gap, sent to §7).

### Seams repointed, which are claims about who owns what

- `input-to-movement`'s `BlockStatePredictionHandler.onTeleport` link went to
  `block-interaction`, which never names the handler; now
  `prediction-and-acks#the-six-windows`.
- `player-anatomy`'s `ServerPlayer.chunkTrackingView` link went to
  `tickets-and-loading`; what the client *has been sent* is Part IX's, so it
  now points at `what-the-client-is-told#chunks-arrive-on-a-loop-the-client-paces`.
- `player-anatomy`'s slot-addressing row hand-forwarded to "commands and
  containers" in plain text, and no page named `Player.getSlot`; the page now
  pays it off itself.
- `status-effects`' hand-forward for `PotionContents` and its siblings went
  to `using-an-item`, which names none of them; split between the machinery
  (`using-an-item#the-meal-tick-by-tick`) and the components
  (`hunger-and-experience#eating-is-a-component-walk`).
- `block-interaction`'s reach gate now cites `player-anatomy#what-player-owns`
  — the ruling for `pass5.md`:2861, taken once on the first half of the
  declared pair rather than twice.
- **Anchors on 71 of Part VIII's links, where the part had none at all** —
  the fifth part running to arrive with zero. Plus the anchors on the six
  cross-part edits above.

### Summariser drift corrected

- `player/README`:57-59 said Part VII owns the inventory; `items/README`:38-41
  and `player-anatomy` say Part VIII does. The landing page and
  `src/lectures.md`:211-212 both fixed in Part VIII's favour. (`pass5.md`:2983.)
- `reference/glossary.md`: **Avatar** led on the renderer, which the page no
  longer says; **LocalPlayer** claimed "its own prediction", which
  `player-anatomy`:190 explicitly denies (`MultiPlayerGameMode.startPrediction`
  reaches `ClientLevel.getBlockStatePredictionHandler` per call). Both
  rewritten to the pages, with anchors.
- `reference/level-data-and-rules`:16-19 sent readers to Part VIII "for the
  spawn"; no Part VIII page explains spawn or respawn. Repointed to what
  Part VIII actually reads there — the two movement game rules.
- `player/README`'s figure node called the spear "the same hit, twice"; the
  page says two different attacks sharing a tail. Node reworded.

### For pass 9's attention, found and not fixed

- `Weapon.AXE_DISABLES_BLOCKING_FOR_SECONDS` (5.0) is declared at
  `Weapon.java`:12 and read by nothing — `ToolMaterial.java`:37 passes the
  value through a parameter. Another dead constant, of the shape
  `FoodConstants` and `MinecraftServer.AUTOSAVE_INTERVAL` already have.
- `LivingEntity.TAG_ACTIVE_EFFECTS` (`LivingEntity.java`:145) is likewise
  declared and unread; `:764` and `:820` write the literal *active_effects*.
  The new `status-effects` section names the tag, not the constant, for that
  reason.
- `the-sword-swing` names `Player.attackVisualEffects` and
  `Player.damageStatsAndHearts` in the tail order and no page in the book
  explains either. `ServerPlayer.wardenSpawnTracker` and `ServerPlayer.camera`
  are named on `player-anatomy` and explained nowhere. All four sent to
  `pass3.md` §7 rather than written here.
- `the-sword-swing`:219-221's three attack-ticker resets were re-derived as a
  set and reconcile (`Player.java`:1834 `Player.onAttack` →
  `resetOnlyAttackStrengthTicker`; `MultiPlayerGameMode.java`:462;
  `ServerPlayer.java`:2085), but it is three named resets on two sides in one
  answer and is worth a second reading.

## Pass 5, session G — Part VII · Items and inventories *(2026-09-05)*

All eight pages of Part VII touched plus the landing page:
`src/systems/items/README.md` (rewritten to the landing-page role),
`items-and-stacks.md`, `using-an-item.md`, `containers-and-menus.md`,
`recipes.md`, `enchantments.md`, `enchanting.md`, `contexts-and-predicates.md`,
`loot-tables.md`. Five pages in three other parts edited because a Part VII
page's owner or duplicate lived there: `foundations/data-components.md`,
`foundations/data-driven-types.md`, `foundations/resource-system.md`,
`blocks/block-breaking.md`, `blocks/block-entities.md`. Plus the Part VII block
of `src/lectures.md`. Both of the part's Reference pages
(`reference/enchantment-hooks.md`, `reference/loot-context-params.md`) are
generated and were not edited.

### Corrections — re-derived against the decompile before the fix

- **`enchanting`: which paths roll in `EnchantmentHelper.selectEnchantment`.**
  The page said "only the table and the provider and loot paths roll one to
  decide *what you get*, and they roll it in the same place:
  `EnchantmentHelper.selectEnchantment`", and then contradicted itself twice
  below. The decompile: `selectEnchantment` has four callers —
  `EnchantmentMenu.java`:232, `EnchantmentsByCost.java`:28,
  `EnchantmentsByCostWithDifficulty.java`:31 and `EnchantmentHelper.enchantItem`
  (`EnchantmentHelper.java`:610, which `EnchantWithLevelsFunction.java`:72
  calls). `SingleEnchantment.enchant` samples a level for a named enchantment
  and never selects (`SingleEnchantment.java`:22-24), and
  `EnchantRandomlyFunction.run` picks with `Util.getRandomSafe` off
  `LootContext.getRandom` (`EnchantRandomlyFunction.java`:65-87). Now: four
  callers named, and the two that roll their own said so.
- **`loot-tables`: where `LootTable.createStackSplitter` sits in the call.**
  The sequence diagram put it on the pool's return ("stacks, each through
  createStackSplitter"). The decompile: `LootTable.fill` calls the private
  `getRandomItems(context)` (`LootTable.java`:157 → :137-143), which calls
  `getRandomItems(context, result::add)` (:121-123), which wraps the consumer
  in `createStackSplitter` and hands it to `getRandomItemsRaw` — where the
  *table's* composite function is layered inside it (:93-103). The splitter is
  therefore the outermost wrapper, applied once per fill and after the table's
  own functions, which is what the flowchart and the prose already said. The
  diagram now says so, and the load-bearing consequence (a nested table is
  split once) is unchanged.
- **`containers-and-menus`: the size of a click's traffic.** The page said "the
  traffic is 128 integers rather than 128 full `DataComponentPatch`es". A
  `HashedStack.ActualItem` carries an item holder, a count, one CRC32C integer
  per *added* component and the plain set of removed ones — the page says so
  itself two sentences earlier — so 128 claimed slots is not 128 integers.
  `ServerboundContainerClickPacket.java`:16-17 caps the map at 128 entries.
  Now: "each claimed slot costs an integer per component rather than a
  re-encoded `DataComponentPatch`".
- **`using-an-item`: which method has one override.** The page said
  "**`CrossbowItem.useOnRelease` is its only override in the tree**" of
  `ItemStack.useOnRelease`. `ItemStack.useOnRelease` (`ItemStack.java`:790-791)
  delegates to `Item.useOnRelease` (`Item.java`:367), and it is the latter that
  `CrossbowItem.java`:264 overrides. Now: the delegation is stated and the
  count attaches to the hook.
- **`loot-tables`: the thirteen path prefixes.** The count is right — the
  literal `register` calls in `BuiltInLootTables` fall under thirteen top-level
  prefixes (chests, gameplay, shearing, charged_creeper, archaeology,
  spawners, harvest, equipment, dispensers, pots, entities, carve, brush) — but
  the list beside it named twelve, missing `entities`, which is the sheep
  colour set (`BuiltInLootTables.java`:78-80). The list now names it.
- **`contexts-and-predicates`: the keys `ALL_PARAMS` omits.** L109-112 names
  the four keys the set leaves out and the consequence sentence beneath it
  named three, silently dropping `LootContextParams.ENCHANTMENT_LEVEL`.
  `LootContextParams` declares fifteen keys and `ALL_PARAMS` requires eleven
  (`LootContextParamSets.java`), so all four behave alike. The consequence now
  names four.
- **`enchanting` against `enchantments`: the anvil's two book tests.**
  `enchanting`:158 said the anvil tests `Items.ENCHANTED_BOOK` by identity;
  `enchantments`:300 said it tests `DataComponents.STORED_ENCHANTMENTS`
  instead. Both are true of *different slots*: `AnvilMenu.java`:204 tests
  `input.is(Items.ENCHANTED_BOOK)` on the left-hand target, and
  `AnvilMenu.java`:145 tests `addition.has(DataComponents.STORED_ENCHANTMENTS)`
  on the right-hand addition for the halved price. Neither page said which
  side; both now do.
- **`enchantments`: what cooks the loot.** "That is a loot-table condition on
  `EnchantmentTags.SMELTS_LOOT`" named the guard, not the mechanism. In the
  data the cooking is the `minecraft:furnace_smelt` function
  (`SmeltItemFunction`) behind an `any_of` condition testing *this* entity's
  on-fire flag or the direct attacker's main-hand enchantment tag
  (`data/minecraft/loot_table/entities/cow.json` and its siblings, built by
  `EntityLootSubProvider.java`:60). `EnchantmentTags.SMELTS_LOOT` has one
  member, Fire Aspect (`VanillaEnchantmentTagsProvider.java`:35). Now the
  function is named and the condition is described as the guard.
- **`foundations/resource-system`: a missing step in the reload's completion
  list.** The row said `PlayerList.reloadResources` "re-reads every player's
  advancements and broadcasts `ClientboundUpdateTagsPacket` and
  `ClientboundUpdateRecipesPacket`". It also calls
  `ServerRecipeBook.sendInitialRecipeBook` for every player
  (`PlayerList.java`:956), which is what makes `recipes`:74's claim about
  shifted display ids true. The step is now in the list.
- **`items/README`: two claims the part's own pages contradict.** "the three
  engines … hand each other nothing" — two of enchanting's five paths are loot
  functions (`enchanting`:332-347), `RepairItemRecipe` carries curses
  (`enchanting`:21-23), and the recipe auto-fill refuses enchanted stacks
  (`recipes`:320-327). And "the sword that swings before the server has heard
  about it" is `player/the-sword-swing`'s hook, in Part VIII, and no page of
  this part pays it off. Both replaced.
- **`using-an-item`: `Item.APPROXIMATELY_INFINITE_USE_DURATION` "in all but
  name".** The constant exists (`Item.java`:119) and has no reader in the tree;
  `BowItem.getUseDuration` and the base body both write the literal. Now stated
  that way, in the new roster paragraph.

### Suspicions re-derived and found sound (a strike is a claim)

- `items-and-stacks`' *two spellings*: the reload-time validator installed by
  `Item.Properties.finalizeInitializer` reads `DataComponents.DAMAGE`
  (`Item.java`, the `addValidator` lambda), and `ItemStack.validateComponents`
  reads `DataComponents.MAX_DAMAGE` (`ItemStack.java`:245-247). The two really
  are different components, and the section's hook stands.
- `containers-and-menus`' mount-menu generalisation:
  `AbstractMountInventoryMenu.java`:20 passes `(MenuType) null` to super, and
  `ServerPlayer.openHorseInventory` sends `ClientboundMountScreenOpenPacket`.
  `AbstractChestBoat.openCustomInventoryScreen` calls `player.openMenu(this)`
  and is not a mount menu, which the page now says so a reader crossing to
  `client/gui-and-screens`' wider `HasCustomInventoryScreen` claim is not
  confused.
- `recipes`' "the server re-sends the player's whole book": true, and the gap
  was on `resource-system` (above).
- `using-an-item`'s two `completeUsingItem` spellings:
  `ServerPlayer.completeUsingItem` sends event 9 and calls super
  (`ServerPlayer.java`:1704-1711); `Player.handleEntityEvent` calls
  `completeUsingItem` on id 9 (`Player.java`:404-407). Both sentences correct.
- `enchantments`' `RegistrySynchronization.packRegistry`: a real private
  per-registry method (`RegistrySynchronization.java`:34) beside the public
  `packRegistries` loop (:28). Two methods, two pages, no drift.
- `enchanting`'s "the grindstone and the providers call
  `EnchantmentHelper.updateEnchantments` themselves": the provider path reaches
  it through `EnchantmentHelper.enchantItemFromProvider`
  (`EnchantmentHelper.java`:708-717), which is inside the helper. The
  three-way split of write entry points stands.
- `items/README`'s "enchantments are a world-load dynamic registry that
  `/reload` never re-reads": `Registries.ENCHANTMENT` and
  `Registries.ENCHANTMENT_PROVIDER` are both in
  `RegistryDataLoader.WORLDGEN_REGISTRIES` and neither is in
  `RegistryLayer.RELOADABLE`. Sound — and the claim now has a home on
  `enchantments`, which is the new claim below.

### Claims this session introduced

- **`items-and-stacks`' new hook**: durability is the one thing a client never
  predicts, because `ItemStack.hurtAndBreak`'s working overload demands a
  `ServerLevel` and the `LivingEntity` overloads silently do nothing without
  one. (The page already carried the fact at its old L256-259; it is now the
  opening claim.)
- **`items-and-stacks`**: `ItemStackTemplate` holds a raw, never-sanitised
  patch, so it is the one thing that can carry a value equal to the item's own
  default and send it verbatim (moved from `data-components`, which stated the
  premise without the consequence). The validator section gains the
  one-level/nesting-not-followed rule and the bundle-weight test, both moved
  from `data-components`. New family sentence: the ninety-eight remaining
  `world/item` classes exist for a behaviour hook no component can express,
  and `AxeItem`/`ShovelItem`/`HoeItem` survive for block-side verbs.
- **`data-components`**: the twenty `delayedComponent` call sites and their
  roster, `Item.Properties.repairable` as the eager near miss, and the
  class-init half of the two-phase build (all moved from `items-and-stacks`);
  the claim that the deferral exists for twenty entries and everything else is
  deferred with them because the map is built in one pass.
- **`containers-and-menus`**: `ContainerLevelAccess.NULL` runs nothing and
  returns an empty optional, so a client menu's body is skipped wholesale and
  only the guard in front of it is real (moved in from `recipes` and
  `enchanting`); the menu-open sequence in order (moved in from `loot-tables`);
  a menu-button click is the third place a broadcast happens and does not wait
  for a phase (moved in from `data-components`); the twenty-nine-menu family
  sentence; `AbstractMountInventoryMenu` and the chest-boat exception; a
  `DataSlot` is either a `shared` view or a `standalone` int and each costs its
  own packet (moved in from `enchanting`).
- **`recipes`**: the nine `CustomRecipe`s named (verified against the tree —
  `BannerDuplicateRecipe`, `BookCloningRecipe`, `DecoratedPotRecipe`,
  `FireworkRocketRecipe`, `FireworkStarFadeRecipe`, `FireworkStarRecipe`,
  `MapExtendingRecipe`, `RepairItemRecipe`, `ShieldDecorationRecipe`), with
  `RepairItemRecipe`'s curse behaviour named so `enchanting`'s hand-forward is
  paid; `SingleItemRecipe`, `SmithingTransformRecipe` and `SmithingTrimRecipe`
  named as the stations' recipe shapes; the claim that the ordinary route into
  the recipe book is an advancement reward rather than a craft.
- **`using-an-item`**: the whole `Item.getUseDuration` roster — the base body's
  three-way answer (a `Consumable`'s ticks, else the hour for
  `BLOCKS_ATTACKS`/`KINETIC_WEAPON`, else zero) and the eight overrides with
  their numbers, `EnderEyeItem`'s zero making it the one item instant by
  declaration. (§7's *lost prose* entry, discharged.)
- **`enchantments`**: the new reload paragraph (above); the anvil's
  addition-side test named as such; `SmeltItemFunction` named;
  `LootItemRandomChanceWithEnchantedBonusCondition` moved in from `loot-tables`
  so the Fortune/Looting answer names all four classes.
- **`enchanting`**: the four `selectEnchantment` callers and the two paths that
  roll their own (the correction above, stated positively); the anvil's
  left-slot/right-slot split; `Registries.ENCHANTMENT_PROVIDER` as a
  world-load registry and `EnchantmentProviderTypes` as its dispatch;
  *local difficulty* replacing *regional difficulty*, which is the book's term
  everywhere else.
- **`contexts-and-predicates`**: the six `LootContextUser` sub-interfaces named
  (verified: `SlotSource`, `LootItemFunction`, `LootItemCondition`,
  `NbtProvider`, `NumberProvider`, `ScoreboardNameProvider`); the `SlotSource`
  family — six registered kinds, answering a `SlotCollection`, with `SlotLoot`
  its one consumer; `LootContext.popVisitedElement` and
  `LootContext.Builder.withOptionalRandomSeed` moved in from `loot-tables`;
  `AbstractVillager.addOffersFromTradeSet` moved into the sequence sentence;
  the claim that a registry's tags load before its elements are validated, so a
  predicate naming an item tag has it resolved by validation time.
- **`loot-tables`**: `SequenceFunction` named as the forty-third function, the
  one that is not a `LootItemConditionalFunction` (verified against
  `LootItemFunctions`); `LootPoolEntry` named as the candidate the funnel
  weighs; `SetContainerLootTable` and `SetContainerContents` named as where a
  `SeededContainerLoot` comes from; the claim that no client class references
  the loot package at all (moved from a clause to the section's punchline).
- **`items/README`**: the whole *Where the part stops* section is new — the
  size through the include, the four family sentences, the four declines
  (villager trading, brewing, the creative tabs, armour identity and trims),
  and the *an item is where another system surfaces* claim with its five
  examples. The shape paragraph's engines-touch-at-the-boundaries claim, with
  its three crossings, replaces "hand each other nothing".
- **`data-driven-types`**: *The run half* now stops at the object existing and
  cites `loot-tables#one-roll-drawn`; seven *taught in* cells re-pointed
  (`LOOT_CONDITION_TYPE`, `LOOT_NUMBER_PROVIDER_TYPE`, `LOOT_NBT_PROVIDER_TYPE`,
  `LOOT_SCORE_PROVIDER_TYPE` and `SLOT_SOURCE_TYPE` to
  `contexts-and-predicates`; `ENCHANTMENT_PROVIDER_TYPE` to `enchanting`;
  `CONSUME_EFFECT_TYPE` to `using-an-item`). Each cell is a claim about which
  page names the element; each was checked by grep before it moved.
- **Anchors**: forty-six cross-part links in Part VII carried two anchors before
  this session and now carry them throughout. Every anchor is an implied claim
  that the named section is the answer; `check_links.py` proves the anchor
  exists, not that it answers.

## Pass 5, session F — Part VI · Entities *(2026-09-05)*

Pages rewritten: all nine of Part VI (`entities/README`, `entity-anatomy`,
`authority`, `entity-lifecycle`, `synched-entity-data`, `attributes`,
`movement-and-collision`, `ai-goals-and-brains`, `pathfinding`,
`damage-and-death`) and the part's Reference page
`reference/non-living-damage`. Four pages in three other parts edited because
a Part VI page's owner or duplicate lived there: `server/server-level-tick`,
`world/points-of-interest`, `foundations/text-components`, plus
`src/lectures.md`.

### Corrections — every one re-derived against the decompile

- **`authority`:113-122 put a player's own physics in the wrong phase.** The
  page had the server's copy running `LivingEntity.travel` "during the entity
  phase of its tick". `ServerPlayer.tick` — the half the level's entity loop
  calls — does **not** call the superclass tick (`ServerPlayer.java`:653); the
  half that does is `ServerPlayer.doTick` (`:725`, calling up at `:728`), whose
  only caller is `ServerGamePacketListenerImpl.tickPlayer`
  (`ServerGamePacketListenerImpl.java`:323), which runs in the *connection*
  phase — `MinecraftServer.tickChildren` ticks every level and only then calls
  `tickConnection` (`MinecraftServer.java`:1228-1254). `the-two-phase-tick`
  had it right all along, which makes this a page contradicting its own owner.
- **`authority`:121-122 misattributed the discard.** It had the next
  `ServerboundMovePlayerPacket` overwriting the server's simulated position.
  The discard is inside the bracket: `tickPlayer` records the position, calls
  `doTick`, then snaps straight back to the recorded one with `Entity.absSnapTo`
  (`ServerGamePacketListenerImpl.java`:319-325). Both are cut to a citation of
  `the-two-phase-tick#the-bracket-and-what-survives-it`.
- **`authority`:181-183, "three of those eight read the same member".** True
  but the weaker of two readings, and the page's own bullet list shows the
  stronger. Counted in the source: `Entity.move` reads
  `Entity.isLocalInstanceAuthoritative` three times and
  `Entity.canSimulateMovement` once; `LivingEntity.aiStep` reads
  `canSimulateMovement` twice, `Entity.isEffectiveAi` twice and
  `isLocalInstanceAuthoritative` once — eight call sites, one of which reads a
  pair, so **four** read the root predicate, three `canSimulateMovement`, two
  `isEffectiveAi`. (This is [pass5.md](pass5.md):706, struck.)
- **`authority`:104-106 was too strong about `Entity.move`.** "the only thing
  that would is `Entity.move`, which on this side only `LivingEntity.travel`
  reaches" — `PistonMovingBlockEntity.java`:191 and
  `ShulkerBoxBlockEntity.java`:143 both call the mover directly, and block
  entities tick on the client. Scoped to *nothing in the mob's own tick*, which
  is what `movement-and-collision`:36-37 already said; the two pages disagreed.
- **`attributes`:116-119 said the same clause twice and got the third wrong.**
  "overrides the attack damage the monster builder added, the follow range the
  mob builder added and the follow range the mob builder added — the movement
  speed it also declares has no earlier entry to beat".
  `Zombie.createAttributes` (`Zombie.java`:132-134) names five;
  `LivingEntity.createLivingAttributes` (`LivingEntity.java`:334-336) already
  contains **both** `Attributes.MOVEMENT_SPEED` and `Attributes.ARMOR`, so four
  of the five are overrides and only `Attributes.SPAWN_REINFORCEMENTS_CHANCE`
  is new. The page contradicted itself fifteen lines later, where `Mannequin`
  gets "the plain living set, including the registry's default movement speed".
- **`damage-and-death`:158-161 had the invulnerability window backwards.** It
  said the red flash is "only half the window" and "the other half is the
  silent one". `LivingEntity.hurtServer` takes the partial branch on
  `invulnerableTime` still being above ten (`LivingEntity.java`:1281), and a
  full hit sets that counter to 20 and the flash to 10 together — so the excess
  rule applies in exactly the ten ticks the flash is *showing*, and the second
  ten protect nothing at all. The page's own hook, its figure node N3 and the
  landing page all had it right; this paragraph alone had it inverted.
- **`entity-anatomy`:212 glossed `entity/schedule` as "villager day plans".**
  The package holds `Activity.java` and `package-info.java` and nothing else;
  the day plan is a `Timeline`. The gloss read as the opposite of
  `ai-goals-and-brains`' hook, which is that *Schedule* does not exist in 26.2.
- **`reference/non-living-damage`:8, "twelve of the rows below inherit it
  unchanged".** Thirteen. There are nine declarations of `Entity.hurtClient`,
  one of them the base default; seven of the eight overriders are rows in this
  table (`RemotePlayer` is a `LivingEntity`), `MinecartTNT` inherits
  `VehicleEntity`'s, and 21 − 7 − 1 = 13. ([pass5.md](pass5.md):578 carried the
  same wrong arithmetic and is corrected in place.)
- **`reference/non-living-damage`:46 compressed the creative branch past
  truth.** "a creative player skips to `Entity.discard`" —
  `VehicleEntity.hurtServer` (`VehicleEntity.java`:36-73) applies the hurt
  direction, the hurt timer, `Entity.markHurt` and the ×10 accumulator *before*
  the creative test, which only redirects the destruction.
  `damage-and-death`:384-386 had it right; the catalogue contradicted its own
  lecture.
- **`ai-goals-and-brains`:383 said "everything it will ever do".** A zombie
  gains a thirteenth goal outside `Mob.registerGoals`:
  `Zombie.setCanBreakDoors` inserts a `BreakDoorGoal` at priority 1
  (`Zombie.java`:152-166), rolled at spawn against local difficulty (`:493`).
  The page's own general section eleven lines earlier already allowed for
  "the few mobs that add or remove a goal on a state change".
  ([pass5.md](pass5.md):703, struck.)
- **`ai-goals-and-brains`:341-348 had a dangling *the three*.** Five of the ten
  villager packages carry no `UpdateActivityFromSchedule`: core, panic and hide
  have nothing at priority 99, pre-raid and raid have `ResetRaidStatus` there
  (`VillagerGoalPackages.java`:35-101). The page then gave three escape hatches
  for what read as those five. Core needs none — it is always active alongside
  one other activity — so the pinning applies to the other four.
- **`movement-and-collision`:369 counted ticks where the code counts gated
  calls.** `ServerEntity.teleportDelay` is incremented at
  `ServerEntity.java`:170, inside the interval gate that opens at `:137`, and
  tested against 400 at `:182`. `what-the-client-is-told`:161-164 already said
  so; for an entity on the default interval the real bound is at least 1,200
  ticks.
- **`movement-and-collision`:379-380 named the wrong branch.**
  `LivingEntity.aiStep` opens with an interpolate branch and an *else if* that
  scales the stored delta by 0.98 — the handler is the interpolate branch and
  the 0.98 decay is the coast branch, which `authority`:102-106 had right.
- **`damage-and-death`:322 handed the respawned object to the wrong page.**
  `player-anatomy`:213-216 itself says `players-and-sessions` owns it; the
  section is
  `players-and-sessions#the-object-and-the-reference-that-outlives-it`.
  ([pass5.md](pass5.md):220, struck.)

### Suspicions re-derived and found sound — a strike is a claim

- `synched-entity-data`:284-287 on `Entity.syncPosition` ("realigns the
  tracker's own counter") against `movement-and-collision`:373 ("forces the
  next send outright"). Both describe `ServerEntity.java`:133-135, which
  re-phases the tracker's tick count to the next multiple of the interval
  immediately before the gate — so the send does happen at that evaluation.
  Not a contradiction; `movement-and-collision` now uses the owner's wording.
- `synched-entity-data`:270-271's "seven of those… set *Integer.MAX_VALUE*"
  against `entity-anatomy`:383's `EntityTypes.AREA_EFFECT_CLOUD`. Both true:
  the seven are the area-effect cloud, the end crystal, both item frames, the
  leash knot, the lightning bolt and the painting, and 37 types set an interval
  at all. The gloss "item frames, paintings, leash knots and their kin" was
  loose, not wrong; the list now lives once, on `entity-anatomy`.
- `entity-lifecycle` "spends the chunk model throughout and links it nowhere"
  ([pass5-brief.md](pass5-brief.md) Part 4, session F's row): **overtaken**.
  The page links `chunk-anatomy` at :83 for the heightmap, and now with the
  anchor.
- `pathfinding`:99-102's villager follow range against `entity-lifecycle`:148's
  `Mob.finalizeSpawn` bonus: the sentence was about which of two numbers
  `PathNavigation.updatePathfinderMaxVisitedNodes` takes the larger of, and 48
  wins either way. Reworded to say the constructor sets it rather than that the
  attribute is untouched.
- `SleepInBed` "never times out": `SleepInBed.timedOut` returns false and the
  class overrides `Behavior.canStillUse` (`SleepInBed.java`:58, :95-98). Sound,
  and it is the page's own counter-example to the default.

### Claims introduced

- **`entity-anatomy`.** The non-living half of the tree, which the page had
  left to the atlas: `Projectile` with 26 descendants, `VehicleEntity` with 15,
  thirteen childless direct subclasses (the numbers are `maps/hierarchy`'s).
  `TamableAnimal` named as a rung, with an owner reference and a tame bit. The
  `Avatar` paragraph cut to the tree fact plus a citation of `player-anatomy`.
  The eight base synched accessors cut to a citation. `EntityType.trackDeltas`'
  ten-type list cut to a citation of `what-the-client-is-told` — the page's own
  cast promises it will not carry the packets after the first — and the seven
  *Integer.MAX_VALUE* intervals named in its place. The section heading *Three
  things about the id* renamed *The id, the box, and the numbers on the type*:
  it carried seven questions and only two were about the id (no page linked the
  old anchor).
- **`authority`.** "four other pages depend on it" replaced by four *parts* and
  the measured sixteen. `Player.isClientAuthoritative` named for the first time
  on the page three others cite for it. The `travelRidden` fork cut to the
  ninth predicate reading, the fork itself cited.
- **`entity-lifecycle`.** Two new passages. The species list has a data-driven
  override and a hard-coded one in front of it: `ChunkGenerator.getMobsAt`
  (`ChunkGenerator.java`:481-511) replaces the biome's list with a structure's
  `StructureSpawnOverride` for the first structure at the position that
  declares one for the category, by piece or by whole start; ahead of it
  `NaturalSpawner.isInNetherFortressBounds` (`NaturalSpawner.java`:305-315)
  returns `NetherFortressStructure.FORTRESS_ENEMIES` for `MobCategory.MONSTER`
  on `Blocks.NETHER_BRICKS` anywhere inside a fortress's bounds — a wider box
  than the fortress's own override, which declares the same list. And
  *findable* is now defined: entities live in `EntitySection`s keyed by
  `SectionPos`, held by `EntitySectionStorage`, each section carrying its own
  `Visibility` and a `ClassInstanceMultiMap`. Also: a raid named as a spawn
  source in *the other ways in*, and the overworld-only fact moved in from
  `server-level-tick`.
- **`ai-goals-and-brains`.** The leash given its own paragraph (it is a lever
  that takes `Goal.Flag.MOVE` away, not a control flag), with
  `Leashable.tickLeash` cited to `entity-anatomy`. A family paragraph for the
  two big libraries: 103 behaviour classes, 61 goal classes, 26 sensors,
  eighteen `*Ai` classes, each an instance of a shape the page has already
  described. `AcquirePoi`'s mechanics and `SleepInBed`'s entry conditions cut
  to citations of `points-of-interest`; the job-site half kept, because it is
  the villager's day, and `SleepInBed`'s never-times-out kept, because it is
  this page's counter-example.
- **`pathfinding`.** The budget's trigger, which the owner could not state:
  `Mob.onAttributeUpdated` on `Attributes.FOLLOW_RANGE` **or**
  `Attributes.TEMPT_RANGE`. `PathComputationType`'s three values, and that the
  four controls implement `Control` and re-specialise by movement mode the way
  the evaluators do. "unbounded by distance" moved in from `block-interaction`.
- **`damage-and-death`.** The non-living roster cut from five families naming
  all twenty-one classes to the argument plus four classes, and the heading
  renamed *Twenty-one classes with no pipeline at all* — the lecture and the
  catalogue had been partitioning the same twenty-one two ways (five families
  against six patterns, the lecture filing a forwarder under *destroys*). New
  section *Who gets the credit for a fall*, discharging the homeless
  fall-attribution threshold: `CombatTracker.getMostSignificantFall`
  (`CombatTracker.java`:114-150) credits the entry *before* the biggest fall
  unless the fall is first, keeps a `FallLocation`-carrying alternative, and
  returns nothing unless the fall exceeded five blocks or the alternative's
  damage did. The `Entity.hurtServer` side-enforcement stated in place instead
  of handed forward to `authority`, which never explained it.
- **`reference/non-living-damage`.** An `Entity.hurtClient` column, twenty-one
  rows, from the seven declarations plus the inherited default.
- **`server-level-tick`.** The census kept as the tick's own cost ("walking
  every entity in the dimension is what this step costs, once a tick") with the
  cap arithmetic cut to a citation.
- **`entities/README`, rewritten to the role.** New argument: five surprises,
  one question, asked about everything not in the grid. A *where the part
  stops* section with the size through the include — the largest part of the
  book — and the coverage answer: about 40% of its lines are named nowhere and
  that is right, because the bulk is one class per species. Four mechanisms
  declared too big for a sentence and sent to §7. `Avatar` corrected from
  "below `Player`" to **above** (four other pages say between `LivingEntity`
  and `Player`). The attribute-lag blurb corrected from "a tick late" to what
  `attributes` actually says, and the ids-stop-at-254 blurb from "the packet
  stops at 254". The pair claim for *synched entity data* ↔ *attributes* moved
  in from `lectures.md`, whose "first of the two channels" contradicted both
  the page and the landing figure's *one of six*.

### Anchors and citations

Part VI carried **no anchor on any of its 69 outbound links** before this
session — the same shape as Parts IV and V. Every link out of the nine pages
and the landing page now carries the owner's anchor where one answers the
sentence. The 22 inbound links to `authority` from sixteen pages are still
bare; the ones from Parts VIII, IX and X are sessions H, I and J's.

### The tool bug — the eighteenth of the project

`map_source.spec_text` rendered a part's package set inline, so a subtracted
package followed by additions read as though *minus* governed the whole tail.
Part VI printed as "`world/entity`, minus `world/entity/player`,
`network/syncher`, `world/level/pathfinder`, `world/damagesource`,
`world/effect`" — four packages the part **includes**, shown as exclusions —
and Part IX had the same shape. Published on `maps/packages.md` and copied
into every part's coverage report header, where two agents caught it
independently. Subtractions now come last and share one *minus*, and
`map_source.py --probe` proves the three shapes.

## Pass 5, session E — Part V · Blocks *(2026-09-05)*

Pages rewritten: all seven of Part V (`blocks/README`, `blocks-and-states`,
`block-interaction`, `block-breaking`, `block-entities`, `signal-and-dust`,
`pistons-and-block-events`, `diodes-and-observers`) and the part's Reference
page `reference/block-update-flags`. Four pages in three other parts edited
because a Part V page's owner or duplicate lived there: `world/scheduled-ticks`,
`server/server-level-tick`, `networking/what-the-client-is-told`,
`reference/glossary`, plus `src/lectures.md`.

### Corrections — decompile open

- **`reference/block-update-flags`, bit 4.** The row said
  `Block.UPDATE_INVISIBLE` "suppresses whichever of those the side does",
  i.e. on both sides. `Level.java`:237 is the only reader of bit 4 in the
  game and the test sits inside the client-side arm:
  `(updateFlags & 2) != 0 && (!isClientSide() || (updateFlags & 4) == 0) &&
  (isClientSide() || chunk.getFullStatus()…)`. The server's extra condition is
  the chunk status, never bit 4, so a *server* write carrying bit 4 still
  broadcasts. The row now says so. `blocks-and-states`:291-295 already had it
  right, so this was a Reference page contradicting its own lecture.
- **`world/scheduled-ticks`, `DiodeBlock.shouldPrioritize`.** The deleted
  paragraph said `TickPriority.EXTREMELY_HIGH` is picked "when the block it
  powers is itself a diode **that is not pointing straight back at it**".
  `DiodeBlock.java`:214-219 returns `isDiode(oppositeState) &&
  oppositeState.getValue(FACING) != direction`, where `direction` is the way
  this diode outputs and a diode's *FACING* points at its **input**. A diode
  pointing straight back at this one has *FACING* equal to
  `direction.getOpposite()`, so it satisfies the test — the condition was
  inverted, and the excluded case is the diode aimed the *same* way. The
  surviving copy, `diodes-and-observers`:123-126 ("a diode whose own input is
  not on the far side of it"), is right and stands.
- **`blocks/diodes-and-observers`:177-179 was self-contradicting.** It said
  `RepeaterBlock.LOCKED` "is the only diode property computed from a redstone
  reading *outside* tick time — `DiodeBlock.POWERED` is the only one computed
  from a reading at all", which denies its own first clause.
  `RepeaterBlock.java`:98 declares four properties and exactly two are computed
  from a reading: *POWERED* at tick time (`DiodeBlock.tick`) and *LOCKED* inside
  `RepeaterBlock.updateShape`:61-62. Rewritten to say two, and that the
  difference between them is *when*.
- **`blocks/block-interaction`, the `isDestroying` gate.** The page had
  `Minecraft.rightClickDelay` set "only when `MultiPlayerGameMode.isDestroying`
  is false", which reads as a condition on the assignment.
  `Minecraft.java`:1880-1883 wraps the **whole method body** in
  `if (!this.gameMode.isDestroying())`, so a use press arriving mid-dig is
  discarded entirely rather than merely losing its delay.
  `client/prediction-and-acks`:243-244 already said "gated on", so this was a
  Part V page understating what a Part X page had right.
- **`blocks/signal-and-dust`, "All three stop early".** The sentence followed a
  table whose three rows are three *direction arrays*, two of which
  (`NeighborUpdater.UPDATE_ORDER`, `BlockBehaviour.UPDATE_SHAPE_ORDER`) do not
  stop early at all — they are fan-out orders. The claim is true of the three
  *reading methods* named inside the first row:
  `SignalGetter.getBestNeighborSignal` and `SignalGetter.getDirectSignalTo`
  return at ≥ 15 (`SignalGetter.java`:22-30, 86-88) and
  `SignalGetter.hasNeighborSignal` at > 0 (:73-74). The antecedent is now the
  methods, and the sentence says explicitly that a fan-out never stops early.
  This is [pass5.md](pass5.md):727's second half, confirmed.
- **`reference/glossary`, *Block event*.** Said the queue means a block event
  "lands late, usually within the same tick", which inverts
  `pistons-and-block-events`' argument ("a block event is a tick late" is only
  sometimes true; the queue is a wait for a named phase, not a delay). The
  entry now says a wait for a phase, and carries the owner's anchor. The page
  won, per the summariser rule.

### Suspicions re-derived and found sound — a strike is a claim

- `blocks-and-states`:288-290's re-mesh gate. An agent read it against
  `rendering/section-meshing` as a contradiction. Both are true: a client write
  goes through **two** doors — `Level.setBlocksDirty` →
  `LevelExtractor.setBlockDirty`, gated on `ModelManager.requiresRender`
  (`LevelExtractor.java`:463-466), and the bit-2 `sendBlockUpdated` →
  `LevelExtractor.blockChanged`, ungated (:437-438). The sentence is true of the
  method it names. Not changed.
- `blocks-and-states`'s `Block.UPDATE_LIMIT` against
  `block-interaction`'s `CollectingNeighborUpdater.maxChainedNeighborUpdates`.
  Genuinely two budgets: the first is the shape cascade's recursion depth,
  passed down `Level.setBlock`/`Block.updateOrDestroy` (`Level.java`:248-253),
  the second counts *requests* into the updater (`CollectingNeighborUpdater.java`:57-60).
  Both pages right; both now say which cascade they mean.
- `block-interaction`:151-156's priority-remesh claim. `LevelRenderer.java`:595-598
  is what reads `PrioritizeChunkUpdates` and sets `rebuildSync`; `Options.java`:952
  defaults it to *NONE* and `GraphicsPreset.java` sets *PLAYER_AFFECTED* in both
  fancy presets. The class and the preset claim are both right; a Part XI page
  describes the same switch differently and is the one to change (logged in
  [pass5.md](pass5.md) for session K).
- `block-entities`' three counts. `getUpdatePacket` overriders: **19**
  (20 files under `block/entity/` less the base). `getUpdateTag` overriders:
  **19** as well (18 under `block/entity/` plus `PistonMovingBlockEntity` under
  `block/piston/`; `TrialSpawnerStateData.getUpdateTag(TrialSpawnerState)` is a
  different signature, not an override). The two lists differ by exactly two,
  and they are the two the page names. Of the nineteen tag overriders,
  **thirteen** call `BlockEntity.saveCustomOnly`. `getUpdatePacket` has exactly
  **one** call site in the game (`ChunkHolder.java`:251). All four counts stand.
- `pistons-and-block-events`' *three blocks raise events directly*.
  `PistonBaseBlock`, `NoteBlock`, `PotentSulfurBlock` override
  `triggerEvent`, plus `BaseEntityBlock` (which forwards) and `ComparatorBlock`
  (dead, as the page says). Three is right; [pass3.md](pass3.md) §7's "four
  blocks" is the stale count and was carrying `ComparatorBlock`.
- `pistons-and-block-events`' `PistonMovingBlockEntity.deathTicks` of five.
  `PistonMovingBlockEntity.java`:312-313, `entity.deathTicks < 5`. Sound.
- `signal-and-dust`'s "for every wire but sometimes the first". True, and now
  precise: `ExperimentalRedstoneWireEvaluator.java`:48 sets bit 128 unless
  `shapeUpdateWiresAroundInitialPosition && initialWire`, and of the three call
  sites only `RedStoneWireBlock.onPlace`:302 passes true.

### Claims introduced

- **`blocks/README` — a new argument, and two new sections.** The opening now
  claims that a door's other half and a lamp's delay "are the same event
  underneath" and differ only by channel; that seven lectures is the fewest of
  any part this size *on purpose*; and that "the four kinds of answer a block
  can give" are a neighbour update, a shape update, a block event and a
  scheduled tick — a four the verified line already promised and no page
  enumerated. A *Where the part stops* section claims "about ten thousand
  lines" of the part's own two packages are taught elsewhere (the coverage
  tool's figure is 59 classes / 10,535 lines named only on other parts' pages)
  and names six destinations. The size sentence is now the include.
- **`blocks-and-states`** gains: the *state/properties* sub-package is "the axes
  and their values" and nothing else; `BlockPattern`/`BlockPatternBuilder` match
  an arrangement of `BlockInWorld` and are "how the game recognises a built
  wither or an iron golem"; `BlockStatePredicate` is "a `StateDefinition` turned
  into a test"; `InstantNeighborUpdater` is the other `NeighborUpdater` and is
  "used by nothing the game ships"; and the rail exception to
  `affectNeighborsAfterRemoval` is explained for the first time — a rail carries
  its geometry in a property, and `BaseRailBlock.affectNeighborsAfterRemoval`
  (`BaseRailBlock.java`:136-148) updates above when the old shape was a slope,
  and its own position and below when the rail is straight. It also receives
  the flags-3 and `GameEvent.BLOCK_DESTROY` detail moved off `block-interaction`.
- **`block-interaction`** gains the use-hook family: **25** blocks override
  `BlockBehaviour.useItemOn` and **52** `BlockBehaviour.useWithoutItem`
  (counted as files declaring the signature under `world/level/block/`, less the
  base declaration in `BlockBehaviour.java`), with six named examples and the
  claim that a block overriding neither "is not interactive at all". This
  restores the count [pass5.md](pass5.md):1734 asked for.
- **`block-breaking`** gains a paragraph claiming the two click lectures answer
  the same two gates oppositely, and that the reason is the pipeline: a
  placement's two corrective updates sit in one branch below the build-height
  test and go out for every outcome that reaches it, while a break has no such
  branch and each refusal decides for itself — three of the four sending the
  true state (`ServerPlayerGameMode.java`:165, 178, 189) and spawn protection
  sending only its message (:172-174).
- **`block-entities`** gains the hopper's cadence — one item then a cooldown,
  "two and a half items a second however often it is ticked", the eight written
  as a literal at both sites (`HopperBlockEntity.java`:130, 415) while
  `HopperBlockEntity.MOVE_ITEM_SPEED` is read nowhere — and the claim that every
  other block entity in the sub-package is the shapes on that page with
  different fields in the middle.
- **`signal-and-dust`** gains the sources family: `ButtonBlock` books a
  scheduled tick to turn off, `BasePressurePlateBlock` and its two subclasses
  re-read what stands on them, `DetectorRailBlock` and `TripWireHookBlock` watch
  for entities, `DaylightDetectorBlock` reads the sky
  (`DaylightDetectorBlock.java`:57-58 uses `getEffectiveSkyBrightness` and
  *SUN_ANGLE*), and the two torches invert what they are attached to — "none of
  them needs a section of its own". Its cast row is re-scoped to "the three
  answers *this trace* asks a state for", naming the analog pair as the
  comparator's ([pass5.md](pass5.md):727's first half).
- **`pistons-and-block-events`** names the seven block-entity raisers
  individually, claims "the other forty-odd block entities in the game raise
  none", names `PistonMath` as what computes the swept box
  (`PistonMath.getMovementArea`), and adds that `PistonMovingBlockEntity`'s
  `getUpdateTag` override means a player loading the chunk mid-push receives the
  placeholder and its cargo in the chunk packet — which pays off
  `block-entities`:52-54's citation, previously landing on a page that did not
  carry the fact.
- **`reference/block-update-flags`** gains a second table decomposing all four
  named combinations (3 = 1+2, 11 = 1+2+8, 260 = 4+256, 816 = 16+32+256+512,
  all read off `Block.java`:95-108) with a *where the book meets it* column
  claiming 260 and 816 are spent nowhere in the corpus; bit 128's row now says
  the skip is keyed on the **target** and that only the experimental evaluator
  sets it; and `Block.UPDATE_LIMIT`'s paragraph now names the distinction from
  the chain budget. Its opener stops enumerating three of the seven pages that
  spend a flag word.
- **`networking/what-the-client-is-told`** receives the fact that
  `ChunkHolder.broadcastChanges` "reads the level again when it builds the
  packet", so the set holds positions and not values and a whole cascade is
  broadcast as one state per position — moved from `signal-and-dust`, which
  stated it twice and now cites it once.
- **`world/scheduled-ticks`** now claims "a booking cannot be called off:
  nothing in the game cancels a single scheduled tick, the only removals being
  the bulk area operations" — `LevelTicks.clearArea`/`copyAreaFrom`, which the
  page describes thirty lines above. It also says a block *chooses* its
  priority from seven (`TickPriority.java`:7 declares seven values), where the
  page previously implied five.
- **`server/server-level-tick`**'s block-event section is cut to the phase
  claim plus a citation; it no longer states the queue's four rules.

### Anchors and citations

Thirty-seven links across Part V gained the owner's anchor — the part carried
none on any cross-part link before this session, the same shape session D found
in Part IV. One link was landing on the wrong page:
`blocks-and-states`:308-310 cited `signal-and-dust` for
`Level.updateNeighbourForOutputSignal`, which that page never names; it now
points at `diodes-and-observers#one-int-and-the-fan-out-that-exists-to-deliver-it`.
Six missing backward links added (feature flags from two pages, the level tick
from `block-entities`, `tickets-and-loading`'s number line, `pathfinding`'s
*one place the world pushes back*, `what-makes-a-sound`'s *who hears it*). Each
anchor asserts that the named section is the answer; `check_links.py` proves
only that the heading exists.


## Pass 5, session D — Part IV · The world *(2026-09-05)*

Eleven Part IV pages plus `reference/level-data-and-rules`, read by one agent
each; the part read end to end in watching order first. Four pages outside the
part were edited, each because a Part IV page disagreed with it:
`server/server-level-tick`, `server/server-tick`,
`networking/what-the-client-is-told`, `rendering/lightmap-fog-and-sky`. One
tool bug, and it had been hiding broken links.

### Corrections — every one re-derived against the decompile

- `world/chunk-anatomy`:247 said "Packing therefore buys a smaller palette,
  **not narrower entries**: unreferenced entries are dropped, which can demote
  a container a whole rung, and a `Configuration.Global` container shrinks from
  `Configuration.bitsInMemory` to `Configuration.bitsInStorage`." The head
  clause is false and the two tails contradict it.
  `PalettedContainer.pack` (`PalettedContainer.java:255-281`) re-encodes into a
  fresh `HashMapPalette`, asks `Strategy.getConfigurationForPaletteSize` for
  the *shrunken* palette's configuration, and writes at
  `Configuration.bitsInStorage`. `Configuration.Simple` reports one width for
  both (`Configuration.java:40-47`) and `Configuration.Global` two, so packing
  narrows entries in exactly two cases: a smaller palette landing a rung lower,
  and a global container's storage width. **Now:** what packing recomputes is
  the palette, and narrower entries are the consequence in those two cases,
  each named.
- `world/chunk-storage`:334 said `ImposterProtoChunk` "does not defer to the
  `LevelChunk` it wraps, which **only** `ImposterProtoChunk.markUnsaved` does".
  `ImposterProtoChunk.java:157-158, 248-254`: `markUnsaved`, `isLightCorrect`
  **and** `setLightCorrect` all delegate unconditionally, which
  `chunk-anatomy`:112 already said — the two pages disagreed. The two flat
  falses are `canBeSerialized` and `tryMarkSaved`
  (`ImposterProtoChunk.java:162-169`). **Now:** all three delegating members are
  named, both pages say the same thing, and `chunk-storage` cites
  `chunk-anatomy`'s anchor.
- `world/chunk-storage`:281 said loading "changes hands **four** times" and
  then named four stages. `ChunkMap.java:582-610` and `997-1001`: the stages are
  the IO lane, *upgradeChunk* and *parseChunk* on `Util.backgroundExecutor`, and
  `SerializableChunkData.read` on the main-thread executor — four stages across
  **three** lanes, two of them sharing one. **Now:** "four stages across three
  lanes", with the shared lane said out loud. The same sentence's
  `SimpleRegionStorage.upgradeChunkTag` is now `ChunkMap.upgradeChunkTag`, which
  is the call `ChunkMap.readChunk` actually makes (`ChunkMap.java:999`), so the
  two Part IV pages name one member for one hop.
- `world/scheduled-ticks`:81 said "**Two type parameters**, two parallel
  worlds". `LevelTicks.java:34`, `LevelChunkTicks.java:17`,
  `LevelTickAccess.java:5` and `ScheduledTick.java:8` each declare exactly one
  parameter. **Now:** "Two type *arguments*", with the one-parameter fact stated
  and `Block` and `Fluid` named as what fills it.
- `world/lighting`:184 said `LightEngine.checkNode` "only decides what to
  enqueue", two paragraphs before describing the sky engine writing stored
  levels. Both engines' `checkNode` writes: `BlockLightEngine.java:36`
  (`setStoredLevel(blockNode, 0)` when emission dropped below the stored level)
  and `SkyLightEngine.java:73`, plus `updateSourcesInColumn` →
  `removeSourcesBelow`/`addSourcesAbove` at `SkyLightEngine.java:108, 135`.
  **Now:** "zeroes the stored level where the light that is there must go and
  enqueues the rest as work".
- `world/fluids`:275 attributed lava's slope numbers through
  `WaterFluid.getSlopeFindDistance` while its own table at :338 used
  `FlowingFluid.getSlopeFindDistance`. `FlowingFluid.java:353` declares it
  abstract; `WaterFluid.java:86` and `LavaFluid.java:154` override.
  **Now:** `FlowingFluid.getSlopeFindDistance` in both places.
- `rendering/lightmap-fog-and-sky`:61 said the lightning layer lerps
  `EnvironmentAttributes.SKY_COLOR` "**a fifth** of the way";
  `environment-attributes-and-timelines`:92 says 22%. `ClientLevel.java:274` is
  `ARGB.srgbLerp(0.22F, …)`, so the owner page is right. **Now:** the rendering
  page's whole duplicate paragraph is one clause and a link, so the number is
  stated once.
- `networking/what-the-client-is-told`:368 said the once-a-second time sync
  "carries a game time plus **a map of clock updates**".
  `MinecraftServer.java:1299-1305` broadcasts
  `new ClientboundSetTimePacket(this.overworld().getGameTime(), Map.of())` — an
  **empty** map, which is what `environment-attributes-and-timelines`:221 says.
  **Now:** the networking page says the map is empty and that clock state travels
  only on a change or a join, with the owner's anchor.
- `reference/level-data-and-rules`:47 sent the reader to `server/server-tick`
  for day time; that page does not own it, `environment-attributes-and-timelines`
  does, and the environment page was claiming this Reference page pointed at it.
  **Now:** repointed to `#who-owns-the-clock`, so the hand-forward is paid.

### Suspicions re-derived and found sound — a strike is a claim

- `chunk-generation-pipeline`:190's "the dispatcher's own **four-slot** queue"
  is real: `ChunkTaskDispatcher.DISPATCHER_PRIORITY_COUNT` is 4 and the four
  users are resort 0, release 1, submit 2, poll 3
  (`ChunkTaskDispatcher.java:18, 38, 51, 63, 80`), so a re-sort really does
  outrank a new submission. Unchanged, and it is a *different* four from the
  ticket throttle's.
- `chunk-generation-pipeline`:211's two requirements on the centre chunk are
  both real and not in conflict: `ChunkGenerationTask.java:92-118` wants the
  persisted status at or past the target **and** every chunk of the loading
  pyramid's square at or past what its distance requires. Unchanged.
- `tickets-and-loading`:346's purge gate — "unless the level is frozen and
  chunk ticking is on" — is exactly `ServerChunkCache.java:328`
  (`runsNormally() || !tickChunks`). Unchanged; `server-level-tick`'s shorter
  "running" is a table compressing it.
- `scheduled-ticks`:364's "only `/clone` and the gametest framework do, in bulk"
  distributes correctly: `CloneCommands.java:248` calls `copyAreaFrom`, which
  only reads (`LevelTicks.java:301-326`), and `GameTestInfo.java:81` /
  `StructureUtils.java:107` call `clearArea`, which removes. Unchanged.
- `chunk-anatomy`:126's double-buffered added and removed sets really are
  `ClientChunkCache.Storage`'s fields (`ClientChunkCache.java:220-221`), with
  the accessors and `flipUpdateTrackingSets` on the cache. Unchanged.
- `points-of-interest`:316's "`PoiManager.loadedChunks` never forgets" holds:
  `PoiManager.java:49, 263` is a `LongSet` only ever added to. Unchanged.

### Claims introduced

- `world/README` — the header now says "the five pages off that line — what the
  place and the hour decide, and the four systems that make the world the line
  delivers feel alive", which is a claim that the environment page is neither
  conveyor nor side-system. A new ***Where the part stops*** section claims that
  about 2,900 lines of the part's packages are taught in six other parts, and
  names each family and its owner part; and it **declares the world border
  Reference-only**, with the reason (no scenario, and what a reader needs of it
  is enumerable). *Watch in this order* entry 1 no longer claims the environment
  page is "the one page here that depends on nothing else in the part" — it says
  *off the conveyor, ahead of it*, which is what the figure draws. Five blurbs
  re-synced word for word to their pages (fluids' two halves, chunk storage's
  "almost every write", the sensor's "at least one tick", the tickets page's
  "nothing asks for a chunk *because* it is loaded", chunk anatomy's *distinct*).
  The Reference list gains `reference/registries.md` with the claim that three
  of the part's mechanisms are registry-backed.
- `src/lectures.md` — Part IV's shape paragraph now counts the conveyor the way
  the landing page does (four pages plus a vocabulary page, not five), and
  lighting's blurb no longer says *self-contained*: it says nothing later in the
  part assumes it and Part XI does.
- `world/tickets-and-loading` — a new paragraph claims `ChunkResult` is the
  two-case type all three holder futures carry and that
  `ChunkHolder.UNLOADED_LEVEL_CHUNK` is simply its shared failure, whose message
  is *Unloaded level chunk*. The spectator answer gains a claim that the skip is
  **remembered** in a `PlayerMap` at join rather than re-asked. The renamed
  section *Which chunks a player is owed, and what makes one eligible* claims
  that the BLOCK_TICKING row is the join between the two systems — nothing is
  sent that the server is not also simulating.
- `world/chunk-generation-pipeline` — a new paragraph on the *EMPTY* step
  claims that a null parse and a thrown load both end at
  `ChunkMap.createEmptyChunk`, that the position is marked replaceable in
  `ChunkMap.chunkTypeCache`, and therefore that **an unreadable chunk is
  regenerated, not skipped**. Three passages cut to citations now claim their
  owners: the level→status line to `tickets-and-loading#the-number-line`, the
  synchronous ask to `#when-the-graphs-run`, the pool sizing to
  `anatomy#four-threads-worth-memorising` with the new claim that "the only knob
  is the pool's, and widening the pool widens everything else that shares it".
- `world/chunk-storage` — a new section *The other store under* data/ claims
  `SavedDataStorage` encodes on the caller's thread and writes on the IO pool,
  at most `Util.maxAllowedExecutorThreads` at a time, chained through
  `SavedDataStorage.pendingWriteFuture`, with `SavedDataStorage.saveAndJoin` the
  only wait — moved from `reference/level-data-and-rules`, which now cites it.
  A new section *Doing all of it at once, with no server running* claims
  `WorldUpgrader` runs one daemon thread named *World Upgrader*, hands each of
  the three stores to a `RegionStorageUpgrader`, optionally recreates region
  files (which compacts a fragmented save), and reports through
  `UpgradeProgress` — and that nothing there loads, generates or consults a
  status.
- `world/environment-attributes-and-timelines` — a new paragraph claims
  `ClockState` is the saved form and `PackedClockStates` the saved map,
  `ClockNetworkState` the wire form, that **the difference between the two is
  the paused flag**, and that `ClockManager` is a one-method interface which is
  why `AttributeTrackSampler` is the same class on both sides.
- `world/points-of-interest` — a new callout, ***A village is made of loaded
  sections only***, claims `PoiManager.isVillageCenter` alone in the query
  family reads through the non-loading `SectionStorage.get`, treats its null as
  *not a centre*, and that this is deliberate because the flood settles every
  tick and must not touch the disk.
- `world/scheduled-ticks` — the random-tick section is cut to the contrast and
  now claims two things as its own: that at the edge of simulation distance
  there is **a ring of chunks where appointments come due and nothing is chosen
  at random**, and that a random tick's eligibility is baked in at
  `BlockBehaviour.BlockStateBase.initCache` **before the world exists**, unlike
  an appointment, which is checked against the world when it comes due.
- `world/chunk-anatomy` — the ticker section, renamed *What step 11 leaves
  behind, and what the chunk goes on holding*, claims the handle belongs to the
  chunk and outlives the block entity in it. The step-8/9 paragraph now claims
  step 9 is "the only step whose whole job is to notice that the world moved
  underneath it".
- `world/fluids` — claims `LiquidBlockContainer` is the interface
  `SimpleWaterloggedBlock` narrows to water, and that the client holds the
  predicted bucket write until the acknowledgement arrives (a citation of
  `prediction-and-acks#the-six-windows`, added where the page previously said
  only "with no round trip").
- `world/lighting` — claims a section is not meshed at all until
  `LevelLightEngine.lightOnInColumn` is true for each of its eight surrounding
  columns, so a light flag decides whether a section may have a mesh (the same
  claim as before, now stated once and cited rather than told twice).
- `server/server-level-tick` — now claims `ServerChunkCache.tickChunks` reads
  `GameRules.RANDOM_TICK_SPEED` once per level tick and hands it down (the page
  previously attributed the read to `ServerLevel.tickChunk`); and its
  scheduled-tick section claims only what belongs to the tick — the two calls,
  their order and their budget — citing `scheduled-ticks` for the drain order
  and the cancellation rule.
- `reference/level-data-and-rules` — claims four parts point at it (III, IV,
  VIII, XII) where it previously named only Part IV and the level tick; claims
  *the border has no lecture* and says why. Its game-rule ids no longer carry
  hand-copied defaults, because `gamerules.md` generates them.
- **Eighteen cross-part and nineteen within-part citations gained the owner's
  anchor.** Part IV carried **none** before this session. Each anchor is a claim
  that the named section is the answer; pass 9 should spot-check that the
  section under each anchor says what the citing sentence says it says.

### The tool bug — the seventeenth of the project, and the first that was hiding failures

`tools/check_links.py` scanned each page **line by line**, and its link regex
cannot match across a newline. The corpus hard-wraps its prose, so a link
written as `[tickets and\nloading](…)` was invisible to the gate: **243 of the
corpus's 7,811 links had never been checked**, and one of them was broken by
this session's own heading rename — `server/server-tick`:225 pointed at
`tickets-and-loading#what-the-player-is-sent-and-when` after the heading
changed, and the gate said clean. Fixed by matching against the whole page
outside its fences with a character-to-line map, so a link is still reported on
the line its `[` sits on. On the first run the fixed gate caught **two** real
broken anchors — that one and `world/README`'s `#packing-a-position`, an anchor
this session had invented and which the old gate would have published. The
number of anchors the gate actually checks went from 12 at pass 5's planning
session to 174, which is mostly this pass's own anchor work finally coming under
the gate. `--probe` now writes a wrapped link with a bad anchor and a wrapped
link with a good one, and fails if either is misjudged.

**For pass 9:** every anchor added by pass-5 sessions A, B and C was written
while the gate was blind to wrapped links. They are checked now, but they were
not checked when they were written.

*(pass-5 sessions append below, newest first)*

## Session A — the standard (pass 5) *(2026-09-05)*

Three published pages rewritten — `src/lectures.md`, `src/SUMMARY.md` and
`src/systems/commands/README.md` — plus `TEMPLATE.md` and two tools. No
system page touched, no fact changed, and **no correction made**: nothing
this session read was found wrong against the decompile, and nothing was
re-derived, because every finding was about where a claim lives rather than
whether it is true. The claims introduced:

**`src/lectures.md`**

- The dependency table gained a **membership rule** and three rows and lost
  three. The rule is a claim about the corpus, checkable without the
  decompile: *a page two or more landing pages name under **before you
  start***, less `anatomy/anatomy`, `foundations/codecs-nbt-json` and
  `foundations/identifiers-and-registries`. `tools/check_deps.py` re-derives
  it on every run and fails on a mismatch, so pass 9's job here is to check
  the rule is the right rule, not the rows.
- Three new rows carry a new third-column phrase each, and each is a claim
  about why a part depends on the page, re-derived from the depending
  landing pages' own sentences: **`resource-system`** — "the staged load and
  its barrier: a server's own data at startup, where recipes and loot tables
  come from, and the reload the atlases are built by" (from `server/README`,
  `items/README`, `rendering/README`); **`data-driven-types`** — "the *type*
  field in a data-pack file and the registry it dispatches on; these two
  parts own most of its instances" (from `worldgen/README`,
  `commands/README`; the "most" rests on `worldgen/README`'s existing
  twenty-six-of-fifty-six claim); **`text-components`** — "what a chat
  message and a screen's label are before anything draws them" (from
  `networking/README`, `client/README`).
- "Watched straight through, the sidebar order still needs one departure
  from itself, and it is now as small as it can be" — the claim is that
  moving *environment attributes and timelines* to first in Part IV leaves
  exactly one out-of-order watch (Part IV lecture 1 before Part III lecture
  2) and that no other part's order departs. `check_deps.py` checks the
  three orders agree; the "one departure" is the session's own reading of
  the graph.
- **102 blurbs cut.** Each was a second copy of a line on a landing page.
  The ordering claims inside them were kept and are quoted unchanged; the
  descriptions were dropped, not moved, because the landing page has them.
  Pass 9 should read the kept clauses against the landing pages rather than
  against the source: the risk is a clause that lost its subject in the cut,
  not a fact that changed.
- The new second paragraph ("Because the subject here is the order, nothing
  below describes a lecture…") is a claim about the page itself.
- "one page until this pass" became "two pages that were one" — a
  pass-number rot fix, no claim.

**`src/SUMMARY.md`** — *environment attributes and timelines* is now first
in Part IV. Nothing else moved; no URL changed (mdBook derives the path from
the file, not the summary).

**`src/systems/commands/README.md`** (the exemplar landing page)

- The size sentence is now `{{#include ../../generated/part-commands.md}}`
  and reads **470 classes and 43,126 lines**, against the hand-count it
  replaced (473 / 43,900). The prose's population is now "the nine packages
  the atlas lists for this part", which is `map_source.PARTS` — check the
  nine, and the `#where-each-part-lives` anchor.
- New: "the command catalogue alone (`net/minecraft/server/commands`) is 102
  classes and 12,800 lines" — the old sentence said "a hundred command
  classes and 12,800 lines" without naming the package.
  `src/generated/packages-depth4.md` gives 102 / 12,781.
- New in the argument: "**None of those four needs any of the others.**" —
  moved up from the shape section, which says "none of them needs another".
  The sentence after it ("a reader who has those two can explain any of the
  four from them") is new and is a claim about the part, not about the game.
- **Cut, not moved**: "one of only two parts of a save that go through the
  data fixer as JSON, the other being advancement progress".
  `anatomy/what-this-book-skips`:252 owns it and this page links there.
- Three *before you start* links now carry an anchor
  (`server-tick#what-minecraftservertickchildren-runs-and-in-what-order`,
  `data-driven-types#the-idea-stated-once`,
  `the-connection#the-threads-underneath-it`). The claim in an anchored link
  is that the named section is where the thing is explained; all three were
  checked against the built heading ids.

**`TEMPLATE.md`** — two new sections, *One home per mechanism* and *The
landing page*. The only measured claim in them is the landing-page budget
("about a hundred lines plus the watch order"), derived from the thirteen
pages on 2026-09-05.

**`tools/check_deps.py`, `tools/verify_names.py`** — two new failing checks
and the index label; see `docs/pass5-brief.md` A5. A tool is suspected
first, twice over: `check_deps.py`'s membership check reproduced pass-4
session A's hand-found list exactly (three absent, three present that should
not be) before anything was edited, which is the evidence that it reads the
pages right; and `check_deps.py --probe` now proves both new checks fail on
the constructs they are for — a reordered sidebar, a short sidebar, a
qualifying page with no row, a row for a page one part assumes, a row for a
page nobody assumes, and a universal that takes a row — and pass on the
shapes they must accept.

## Planning session — between passes 4 and 5 (2026-09-05)

No system page rewritten. Three claims introduced, all in the frame and the
atlas:

- `src/introduction.md` — the *Verified means tested* paragraph now says
  "every link and anchor between pages is checked to land" and "a page that
  fails any of those does not go up": the claim is that `tools/check_links.py`
  runs in `tools/deploy.sh` before the build and exits non-zero on a broken
  link, anchor, include, `SUMMARY.md` entry or redirect (`tools/deploy.sh`,
  the line after `check_deps.py`).
- `src/maps/packages.md` — the *Where each part lives* table is now
  `src/generated/parts.md`, written from `map_source.py`'s `PARTS`. The
  mapping is a set of claims about which packages each part covers, and it
  differs from the hand table it replaced: Part IV adds `world/level/material`,
  `world/attribute`, `world/timeline`, `world/clock`, `world/level/border`;
  Part VI adds `world/damagesource`, `world/effect` and subtracts
  `world/entity/player`; Part II adds `world/flag`; Part IX subtracts
  `network/syncher` (Part VI's); Part X adds `client/input`, `client/server`
  and counts `net/minecraft/client` itself only; Part XI adds
  `client/particle`; Part XIII adds `server/permissions`, `server/bossevents`
  and `client/gui/screens/dialog`. The paragraph above the table says how
  it is counted (no prefix, *itself only*, shared packages counted twice,
  skipped packages left out) — check each against `map_source.in_part`.
  Every landing page's size sentence will quote its row once the part
  sessions switch them to the include; until then a landing page's hand
  count and its row may differ (Part XIII: 473 / 43,900 by hand, 470 /
  43,126 by the atlas).
- `docs/pass5-brief.md` Part 4 — the measured tables (coverage per part, the
  queue by kind, the duplication pairs) are the tools' output on 2026-09-05
  and are claims about the corpus on that day, not about the game; pass 9
  need not check them.

## Pass 5, session B — Parts I and II *(2026-09-05)*

Eleven pages read by one agent each, both parts read end to end, nine pages
rewritten (`anatomy/README.md`, `anatomy/anatomy.md`,
`anatomy/what-this-book-skips.md`, `foundations/README.md`,
`foundations/identifiers-and-registries.md`, `foundations/resource-system.md`,
`foundations/tags.md`, `foundations/codecs-nbt-json.md`,
`foundations/data-driven-types.md`) plus one-clause link edits on
`data-components.md` and `text-components.md`.

### Corrections — re-derived against the decompile before the fix

- `foundations/identifiers-and-registries.md` — said `MappedRegistry` "is
  keyed three ways (`byKey`, `byLocation` and the insertion-ordered
  `byId`)". **There are four.** `MappedRegistry.java:40` declares
  `private final Map<T, Holder.Reference<T>> byValue`, an `IdentityHashMap`
  built at :65 and written at :129; `getKey` (:141) and `getResourceKey`
  (:148) both read it, so the object-to-name direction goes through `byValue`
  and not through the three the page named. `toId` (:37) is the parallel
  identity map to the number. Now: four indexes, one per lookup direction.
- `foundations/codecs-nbt-json.md` — said `StreamTagVisitor` and its
  neighbours "let `NbtIo.parse` pull **two** fields out of a region chunk",
  then named three consumers. Two is right for one of them only:
  `IOWorker.java:105` builds a `CollectFields` of two `FieldSelector`s
  (*DataVersion*, *blending_data*); `StructureCheck.java:113` builds one of
  three (*DataVersion*, *Level/Structures/Starts*, *structures/starts*). Now
  stated as the mechanism — a `CollectFields` over whatever selectors the
  caller wants — with both counts attributed.
- **Checked and found correct, so no change:** `data-components.md`:183-191
  and `identifiers-and-registries.md`:306-311 were reported as contradicting
  each other on the singleplayer component binding. They do not.
  `ClientConfigurationPacketListenerImpl.java:177` passes
  `connection.isMemoryConnection()` as
  `tagsAndComponentsForSynchronizedRegistriesOnly`, and
  `RegistryDataCollector.java:166` negates it into `updateComponents`'
  `includeSharedRegistries` (:142-148), so a memory connection binds only the
  `RegistrySynchronization.isNetworkable` registries. Both pages say that.

### Claims introduced

- **A new section, `identifiers-and-registries.md` §*Feature flags: the same
  registry, narrowed*** — the largest new claim of the session, discharging
  a coverage entry. Each sentence, with where it came from:
  `FeatureFlagSet` is a *long* mask plus a `FeatureFlagUniverse`, cap
  `MAX_CONTAINER_SIZE` = 64 (`FeatureFlagSet.java:9-18`); one universe,
  *main*, and four flags — `VANILLA`, `TRADE_REBALANCE`,
  `REDSTONE_EXPERIMENTS`, `MINECART_IMPROVEMENTS` (`FeatureFlags.java:37-48`);
  `isExperimental` is "not a subset of `VANILLA_SET`" (:34-36);
  `FeatureElement` has one method and seven implementors — `Item`,
  `BlockBehaviour`, `EntityType`, `GameRule`, `MenuType`, `Potion`,
  `MobEffect`; `FILTERED_REGISTRIES` names those seven registries
  (`FeatureElement.java:10`);
  `HolderLookup.RegistryLookup.filterFeatures` returns *this* for a registry
  not in the set and a filtering delegate for one that is
  (`HolderLookup.java:82-87`); **"the registry underneath is not touched, and
  neither is its numbering — a disabled item keeps its wire id"** is the
  inference from that delegation and is the sentence most worth re-deriving;
  the consumers are `CommandBuildContext.java:22`, `GameRules.java:109`,
  `MinecraftServer.java:373` and `LevelReader.java:232-235`; the set is
  `WorldDataConfiguration.enabledFeatures`.
- **`resource-system.md`, the two `server/packs` corners** the skips page had
  been promising it: *linkfs* as `LinkFileSystem` / `LinkFSProvider` /
  `LinkFSPath`, and `DownloadQueue` — one directory per pack UUID, one at a
  time on a `ConsecutiveExecutor` over `Util.nonCriticalIoPool`, a
  `JsonEventLog` per attempt, and `DownloadCacheCleaner.vacuumCacheDir` at
  construction trimming to `MAX_KEPT_PACKS` = 20 (`DownloadQueue.java:37-47`,
  `DownloadCacheCleaner.java:30-60`). **"newest kept, one per directory
  before any directory's second"** is a reading of `prioritizeFilesInDirs` and
  the two comparators, and is the claim here to check.
- **`anatomy.md`, the packet-drain contrast.** The hop paragraph now ends
  "so a client at 200 frames a second takes the server's updates ten times
  more often than it ticks" — arithmetic over the page's own 20 Hz tick, and
  a restatement of `what-the-client-is-told.md`:442. Check the framing, not
  the numbers.
- **`anatomy.md`, the 1.21-era callout** was replaced: out went the
  `Gui`/`Hud` box (owned by `client/hud` and `reference/naming-drift`), in
  came `DeltaTracker` was *Timer*, which restates
  `reference/naming-drift.md`:52 and :68.
- **`anatomy.md`, `GameConfig`** — new clause: the client's `Main` parses its
  command line into a `GameConfig` the `Minecraft` constructor is built from.
  Closes the part's one coverage gap; check against `client/main/Main`.
- **`anatomy/README.md` is rewritten to the landing-page role** and its
  figure redrawn from the twelve other parts to the part's own two pages.
  New claims: that the part's argument is the two loops rather than "a server
  that ticks and a client that draws"; that the boundary page is second
  because a boundary is drawn before the investment (moved from
  `lectures.md`:466-468, which keeps it as an ordering claim); and *where the
  part stops*, which asserts that Parts III, IX and X take the three threads
  onward. The lane sentence is now "nearly every lane ... is a class, and the
  handful that are not stand for a thread", which is
  `reference/lanes.md`:5-10 and `check_lanes.py`'s own count (333 and 9).
- **`foundations/README.md`** — "Part II is not a stack but a fan ... the
  figure has two roots and no single column" replaces "Part II is a stack".
  A claim about the figure directly above it, and checkable against it.
- **`what-this-book-skips.md`, three reframings.** `com/mojang/blaze3d/audio`
  is no longer presented as skipped — `client/sound-engine` teaches all of it
  (its cast carries `Library` and `AbstractDeviceTracker`; :129 the thirty
  channels, :240 HRTF), so the section keeps only the address argument. The
  statistics page's criterion-parse paragraph became a citation of
  `scoreboard-and-data`:158-162, which owns it. The recipe book is stated as
  `items/recipes`' rather than as skipped. **The hatching in the generated
  treemap was not changed to match**, so the figure and the prose should be
  read together at pass 9.
- **Ownership moves that changed what a page asserts** (each now one sentence
  and a link where it was an explanation): the two tag tables, from
  `identifiers-and-registries` to `tags`; the GPU-backend retry order, to
  `rendering/the-window`; the crash relay, to `how-a-server-dies`; the
  empty-server pause, to `server-tick`; `MinecraftServer.spin`'s order, to
  `starting-a-server`; the Netty hop's mechanism, to `the-connection`. In
  each case check that the surviving sentence is still true on its own — a
  trimmed sentence is a new claim.
- **Outbound links gained anchors** across the nine pages. An anchor is a
  claim that the named section is the answer; all resolve under
  `check_links.py`, which proves the heading exists and not that it answers.

### Tool bug

- `tools/map_source.py` and `tools/pass5_coverage.py` reported different
  populations for the same packages — Part I as 7 classes / 6,770 lines and
  6 / 6,766 — while `map_source.py`'s own comment claimed they "can never
  disagree". The difference is `package-info.java`, which the atlas counts as
  a file and the coverage tool drops. No published page states either number
  today (Part I's landing page carries no size), so nothing false was
  published. Both tools now say which population they mean, and the false
  comment is gone. Every part with a `package-info.java` reads one class
  larger in the atlas than in its coverage report.

## Pass 5, session C — Part III · The server *(2026-09-05)*

All six pages of Part III touched: `src/systems/server/README.md` (rewritten
to the landing-page role), `server-tick.md`, `server-level-tick.md`,
`players-and-sessions.md`, `starting-a-server.md`, `how-a-server-dies.md`.
Also one line each in `src/lectures.md` and `src/reference/README.md`.

### Corrections — re-derived against the decompile before the fix

- **`how-a-server-dies`: the autosave interval.** The page said the autosave
  runs "every 6000 ticks — five minutes of game clock, floored at 100 ticks".
  The decompile: `MinecraftServer.ticksUntilAutosave` starts at 6000 ticks
  (`MinecraftServer.java`:337) and is thereafter
  `computeNextAutosaveInterval` = `Math.max(100, (int)(ticksPerSecond *
  300.0F))` (`MinecraftServer.java`:1149-1162), i.e. **300 seconds of wall
  clock at the current rate**, not 6000 ticks and not game clock. Now "on the
  countdown the tick keeps … five wall-clock minutes, whatever the tick
  rate", citing `server-tick#the-bookkeeping-at-the-bottom`, which owns the
  arithmetic. This agrees with `server-tick`:403-412 and
  `chunk-storage`:311-316, which were already right.
- **`starting-a-server`: a missing management secret.** The page said
  `JsonRpc.create` "throws, ending the boot, if it is set and the secret is
  not forty alphanumeric characters rather than quietly going without one",
  which reads as *absent secret kills the boot*. The decompile:
  `DedicatedServerProperties`:132 resolves *management-server-secret* with
  `SecurityConfig.generateSecretKey()` as its **default**, and `Settings.get`
  puts the resolved value back into the properties map, which
  `DedicatedServerSettings.forceSave` writes — so an absent secret is
  generated and saved. `JsonRpc.create` throws only when the secret present
  fails `SecurityConfig.isValid` (non-empty, exactly forty alphanumerics —
  `SecurityConfig.java`:9-11). This also settles the disagreement with
  `what-this-book-skips`:180-181 ("generating one if absent"), which was the
  right half.
- **`starting-a-server`: what `DerivedLevelData` causes.** The page said the
  derived data is "why the time of day, the weather, the difficulty and the
  world spawn are one set of numbers every dimension shares". The decompile:
  `DerivedLevelData.java`:18-80 forwards game time, level name, game type,
  hardcore, allow-commands, initialised, difficulty and the difficulty lock,
  and swallows every setter but `setSpawn`. It carries **no** day time and
  **no** weather — day time is `ServerClockManager`'s and weather is one
  server-wide `WeatherData` — and the spawn a level reports comes from
  `MinecraftServer.effectiveRespawnData` through `ServerLevel.getRespawnData`
  (`ServerLevel.java`:1523-1524, `MinecraftServer.java`:1289-1292,
  1884-1885). Three of the four attributions were wrong; the paragraph now
  claims difficulty (and the rest of the forwarded set) and names the real
  owners of the other three, citing
  `level-data-and-rules#the-spawn-every-level-reports-is-the-servers-not-each-levels`.
- **`server-tick`: what ticks the `/schedule` queue.** The page said it
  "ticks from inside `ServerLevel.tickTime`, with the dimension's own game
  time". The decompile: `ServerLevel.tickTime` is wholly inside
  `if (this.tickTime)` (`ServerLevel.java`:458-466), the flag only the
  overworld is constructed with, and it passes the overworld's incremented
  game time to `getScheduledEvents().tick`. Now "which runs in the overworld
  alone and off the overworld's *gameTime*", citing the level tick. This was
  a disagreement with its own declared pair (`server-level-tick`:135-141),
  which was right.
- **`server-level-tick`: what the mob count walks.** The page said
  `NaturalSpawner.createState` walks every entity "skipping mobs that require
  persistence". The decompile (`NaturalSpawner.createState`) also skips every
  entity whose category is `MobCategory.MISC` — items, projectiles, armour
  stands — which is most entities in a busy world. Now states both skips.
  `entity-lifecycle`:41 had both and was right.
- **`server-level-tick`: the second chunk set.** The page said
  `ChunkMap.forEachBlockTickingChunk` walks the entity-ticking set and "each
  of those chunks gets `ServerLevel.tickChunk`". The decompile: it also drops
  any position whose `ChunkHolder` is absent or whose
  `ChunkHolder.getTickingChunk` is null. Now "keeps only those whose
  `ChunkHolder` has a live `ChunkHolder.getTickingChunk`".
  `scheduled-ticks`:295-297 had the filter.

**Re-derived and found sound** (a strike is a claim, so these are recorded
too): `starting-a-server`'s "the tickets the last shutdown parked" —
`TicketStorage.fromPacked` loads every persisted ticket into the
*deactivated* map, so "parked" is exactly the loaded state;
`players-and-sessions`' "`MinecraftServer.saveAllChunks` stamps the current
owner's id into the level data" — `MinecraftServer.java`:642-644 passes
`getSingleplayerProfile().id()` to `saveDataTag`; `server-level-tick`'s
`Player.isAlwaysTicking` — declared on `EntityAccess`, false on `Entity`,
overridden true on `Player` alone, so both this page's and
`entity-lifecycle`'s spellings are right; `server-level-tick`'s ticket-purge
gate — `ServerChunkCache.java`:328 is `runsNormally() || !tickChunks`, and
the page's scope is the level tick, where `tickChunks` is true;
`server-tick`'s *clocks* and *command functions* table rows — both guards are
inside the called method (`ServerClockManager.tick`,
`ServerFunctionManager.tick`), which is what the *skipped when* column
describes; the landing page's "five side threads" — `reference/threads.md`
has exactly five dedicated-only rows.

### Claims introduced

- **`src/systems/server/README.md` rewritten to the landing-page role.** New
  claims: the part's argument, that "almost everything surprising about a
  server's timing is the order of one method", and that a reader who finishes
  can answer *when* for four named things; the size paragraph, which is the
  atlas include plus "over half of those lines are
  `net/minecraft/server/level`'s forty-two classes, at nearly three hundred
  lines apiece" (42 / 11,977 from `map_source.py packages`); the pair claim
  moved in from `lectures.md` ("seven later parts assume one of them or the
  other"), which is `lectures.md`'s own count and is now stated once; a new
  *where the part stops* section, asserting that `ChunkGenerationTask`,
  `ChunkTaskDispatcher`, `ChunkTaskPriorityQueue` and `WorldGenRegion` belong
  to Part IV, `ServerPlayerGameMode` to Parts V and VIII, `ServerScoreboard`,
  `ServerFunctionLibrary` and `ServerAdvancementManager` to Part XIII, and
  `ReloadableServerRegistries` to Part II (each from the coverage report's
  *named on pages of other parts* table); and the *Game rules* line, now "the
  fourteen these five pages name, out of fifty-nine" — counted by grep over
  the five pages and against `gamerules.md`'s own 59.
  **Cut:** "a hopper moves one item per eight of them", which was true
  (`HopperBlockEntity.MOVE_ITEM_SPEED` is 8) and had no home but this
  summariser; logged to [pass5.md](pass5.md) for session E.
  **Moved out:** "a console command … is as late as the piston", now a
  sentence on `server-level-tick`'s broadcast section, where the rule it
  qualifies lives.
- **`server-level-tick`: two new passages.** A paragraph after the cast on
  what the abstract `Level` holds and leaves abstract, and what `ServerLevel`
  adds — the §7 gap, discharged; every member named was read
  (`Level.java`:110-134 for the fields, its nineteen abstract declarations,
  `ServerLevel.java`:202-216 for the four additions), and `getChunkSource` is
  deliberately *not* claimed for `Level`, because it is declared on
  `LevelAccessor`. And a sentence naming the tick's profiler zones in order —
  *world border*, *weather*, *tickPending* (*blockTicks*, *fluidTicks*),
  *raid*, *chunkSource*, *blockEvents*, *entities* (*dragonFight*,
  *checkDespawn*, *tick*), *blockEntities*, *entityManagement*,
  *debugSynchronizers* — read off `ServerLevel.tick`'s own `push`/`popPush`
  calls. Ten pages in five parts already cite these names; this is the first
  page that defines them.
- **`players-and-sessions`: three coverage additions.** The stored-user-list
  family (`StoredUserList` as a JSON file of `StoredUserEntry` records,
  subclassed as `UserBanList`, `IpBanList`, `ServerOpList`, `UserWhiteList`;
  `BanListEntry`'s source, reason and expiry; and **the expiry swept on
  read** — `StoredUserList.get` calls `removeExpired` before answering, so a
  temporary ban lapses when somebody asks rather than on a timer). The
  identity cache named as `CachedUserNameToIdResolver` over *usercache.json*
  with `ProfileResolver` behind it (`Services.java`:17-22). And
  `PlayerDataStorage`'s rescue, which the cast cell had promised and the page
  never gave: a failed *.dat* read copies the file aside under a
  *_corrupted_* name and then tries the *.dat_old* twin
  (`PlayerDataStorage.java`:69-114). The clause that a player with neither is
  "built from nothing, which is a new spawn rather than an error" is the
  session's inference from `load` returning empty, and is the line on this
  page to check hardest.
- **`starting-a-server`: one coverage addition.** `Bootstrap.bootStrap`'s
  last act installs `LoggedPrintStream` (or `DebugLoggedPrintStream` when
  debug logging is on) over `System.out` and `System.err`, keeping the
  original as `Bootstrap.STDOUT` — `Bootstrap.java`:39, 63-64, 146-155. That
  is why `Bootstrap.realStdoutPrintln` exists for the watchdog report.
- **Ownership cuts, each now one sentence and an anchored link.** The crash
  relay, from `server-tick` to `how-a-server-dies#the-crash-that-saves`
  (session B's ruling, applied); what a stopped server does with a submitted
  task, from `server-tick` to
  `how-a-server-dies#the-front-door-closes-the-guests-do-not-leave`, with
  *RejectedExecutionException* **moved** into that page rather than dropped;
  `session.lock`'s nature, from `how-a-server-dies` to
  `starting-a-server#taking-the-lock-and-fixing-leveldat-twice`; the
  `level.dat` write path, from both Part III pages to
  `level-data-and-rules#what-is-left-in-leveldat` (three tellings to one, and
  `how-a-server-dies` keeps `NbtIo.writeCompressed`, which the Reference page
  lacks); the ticket-persistence half, from `how-a-server-dies` to
  `tickets-and-loading#what-a-ticket-asks-for`, keeping only *why the drain
  loop ends*; *Done* against `MinecraftServer.isReady`, from
  `how-a-server-dies` to `starting-a-server#done-comes-before-the-loop`; the
  flush bracket and the 601st-call latency sweep, from `players-and-sessions`
  to `server-tick`; the per-chunk save spacing, from `how-a-server-dies` to
  `chunk-storage#the-four-moments-a-chunk-is-written`; the thread table's
  *what it may touch* framing, from `starting-a-server` to
  `reference/threads#the-threads-a-lecture-leans-on`. **Every trimmed
  sentence is a new claim** — pass 4's finding — and these are where to look
  first.
- **Seams repointed, which are claims about who owns what.**
  `starting-a-server`'s login-encryption hand-forward now goes to
  `protocol-phases#login` instead of `players-and-sessions`, which never
  explained it; `players-and-sessions`' two-place tick hand-forward now goes
  to `the-two-phase-tick#the-trace-one-player-one-tick-twice` instead of
  `player-anatomy`, which does not contain `ServerPlayer.doTick`; its
  permission-model link now goes to `permissions#where-a-set-comes-from`
  instead of `brigadier-and-commands`, which owns the packet and not the set;
  and `how-a-server-dies`' claim about connections with no `ServerPlayer` now
  cites `protocol-phases#configuration` rather than `players-and-sessions`.
- **`players-and-sessions`: `GameRules.KEEP_INVENTORY` re-scoped.** "decides
  only whether `ServerPlayer.transferInventoryXpAndScore` runs" is now
  "decides only whether `ServerPlayer.restoreFrom` runs" it, with a link to
  `damage-and-death` for what the same rule decides on the way out. The rule
  is read in three places (`ServerPlayer.java`:1749, `Player.java`:551 and
  `Player.java`:1609); the *only* was true of `restoreFrom` and read as
  global.
- **Anchors on twenty-eight outbound links across the six pages.** An anchor
  asserts that the named section is the answer; `check_links.py` proves the
  heading exists and not that it answers.
- **`src/lectures.md`** loses the pair claim (moved to the landing page), and
  its III-to-IV paragraph now says the level tick's first step "throws away a
  cache" rather than that its "first statement about the day-night cycle"
  rests on the environment page — the page's dependency is the cache, per
  `server-level-tick`:94-105. **`src/reference/README.md`** adds III to
  *Level data and rules*' parts column, which the landing page now points at.

### For pass 9's attention, found and not fixed

- `server-tick`:403-412 says the autosave countdown "starts at
  `MinecraftServer.AUTOSAVE_INTERVAL` (6000)". The value is right and the
  constant exists, but the constructor writes the literal 6000
  (`MinecraftServer.java`:337) and nothing reads `AUTOSAVE_INTERVAL` — a dead
  constant the page presents as the source of the number.
- `server-tick`:211-212 has `Connection.tick` flushing "at the end of the
  connection phase"; the flush is inside each connection's own tick, so it is
  true of the phase as a whole and not of any one call.
- `server-tick`'s *clocks* row gives *skipped when* as "frozen, or
  `GameRules.ADVANCE_TIME` is off", where only the first is a skip of the
  call and the second is a no-op inside it. Same shape as the *command
  functions* row, so the two are at least consistent.
- `commands/scoreboard-and-data`:277-278 says "a score set and a crash a tick
  later is a score lost", which contradicts `how-a-server-dies`' hook (a
  tick-loop crash writes what `/stop` writes) unless it means a watchdog kill
  or a *kill -9*. Session M's page, flagged in [pass5.md](pass5.md).
