# Block update flags

> Verified against **Minecraft 26.2** · Reference · Hand-kept from `Block`'s
> *UPDATE_* constants: the ten bits of `Level.setBlock`'s flag word, what
> reads each, and the named combinations.

The flag word is `Level.setBlock`'s third argument — the last one on the
three-argument overload, and followed by an *update limit* on the four-argument
one. It is a bit set, tagged in signatures by `Block.UpdateFlags`, an
annotation that carries no values of its own.
[Blocks and states](../systems/blocks/blocks-and-states.md#the-two-update-channels)
draws the tail of `Level.setBlock` as a flowchart whose gates name these bits
by number; this is the table behind the numbers. Every page of Parts IV and V
that passes a flag word means the same bits by them.

| bit | constant | what reads it |
|---:|---|---|
| 1 | `Block.UPDATE_NEIGHBORS` | the neighbour fan-out in the tail, and the gate on `BlockBehaviour.BlockStateBase.affectNeighborsAfterRemoval` in the chunk write |
| 2 | `Block.UPDATE_CLIENTS` | `Level.sendBlockUpdated` — the broadcast on the server, a re-mesh on the client, where it is `LevelExtractor.blockChanged` |
| 4 | `Block.UPDATE_INVISIBLE` | the client half of that same gate, and nothing else: `Level.setBlock` tests it only on the client, so a server write carrying it still broadcasts |
| 8 | `Block.UPDATE_IMMEDIATE` | one place in the game: `LevelExtractor.blockChanged`, which marks the re-mesh as player-caused |
| 16 | `Block.UPDATE_KNOWN_SHAPE` | three readers: `Level.setBlock`, where it suppresses all three shape passes; `BlockInput.place`, where it decides whether the state is fixed up against its neighbours before the write; and `WorldGenRegion.setBlock`, where it suppresses the post-processing mark |
| 32 | `Block.UPDATE_SUPPRESS_DROPS` | `Block.updateOrDestroy`, whose destroy branch drops resources unless it is set. A one-level flag: it is masked out of the word as it propagates, both to the neighbours and into the recursive write |
| 64 | `Block.UPDATE_MOVE_BY_PISTON` | passed on as *movedByPiston*, and lets `BlockBehaviour.BlockStateBase.affectNeighborsAfterRemoval` run without bit 1 |
| 128 | `Block.UPDATE_SKIP_SHAPE_UPDATE_ON_WIRE` | `NeighborUpdater.executeShapeUpdate`, which then skips any shape update whose **target** is dust, whatever the source. Only the experimental wire evaluator sets it ([signal and dust](../systems/blocks/signal-and-dust.md#the-second-implementation)) |
| 256 | `Block.UPDATE_SKIP_BLOCK_ENTITY_SIDEEFFECTS` | suppresses `BlockEntity.preRemoveSideEffects` |
| 512 | `Block.UPDATE_SKIP_ON_PLACE` | suppresses `BlockBehaviour.BlockStateBase.onPlace` |

Four named combinations stand beside the bits, and the two large ones are
worth decomposing here rather than in the reader's head.

| constant | value | the bits | where the book meets it |
|---|---:|---|---|
| `Block.UPDATE_ALL` | 3 | 1 + 2 | the common write — every page that says *flags 3* means this |
| `Block.UPDATE_ALL_IMMEDIATE` | 11 | 1 + 2 + 8 | placement |
| `Block.UPDATE_NONE` | 260 | 4 + 256 | nowhere in this book |
| `Block.UPDATE_SKIP_ALL_SIDEEFFECTS` | 816 | 16 + 32 + 256 + 512 | nowhere in this book |

`Block.UPDATE_LIMIT` is also 512, and is not a bit at all — it is the default
recursion budget for the shape cascade, counting **recursion depth** rather
than requests, which is what keeps it distinct from
`CollectingNeighborUpdater.maxChainedNeighborUpdates` ([block
interaction](../systems/blocks/block-interaction.md#the-updater-underneath-a-stack-drained-depth-first)).

---

*Rules: names, never code · how the system works, not how the code reads ·
newest version only · every backticked name passes `tools/verify_names.py`.*
