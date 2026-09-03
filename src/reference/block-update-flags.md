# Block update flags

> Verified against **Minecraft 26.2** · Reference · Hand-kept from `Block`'s
> *UPDATE_* constants: the ten bits of `Level.setBlock`'s flag word, what
> reads each, and the named combinations.

The last argument to `Level.setBlock` is a bit set, tagged in signatures by
`Block.UpdateFlags`, an annotation that carries no values of its own.
[Blocks and states](../systems/blocks/blocks-and-states.md) draws the tail
of `Level.setBlock` as a flowchart whose gates name these bits by number;
this is the table behind the numbers, and the other pages that pass a flag
word — [fluids](../systems/world/fluids.md)' bucket, [pistons and block
events](../systems/blocks/pistons-and-block-events.md)' moves — mean the
same bits.

| bit | constant | what reads it |
|---:|---|---|
| 1 | `Block.UPDATE_NEIGHBORS` | the neighbour fan-out in the tail, and the gate on `BlockBehaviour.BlockStateBase.affectNeighborsAfterRemoval` in the chunk write |
| 2 | `Block.UPDATE_CLIENTS` | `Level.sendBlockUpdated` |
| 4 | `Block.UPDATE_INVISIBLE` | suppresses that broadcast, on the client only |
| 8 | `Block.UPDATE_IMMEDIATE` | one place in the game: `LevelExtractor.blockChanged`, which marks the re-mesh as player-caused |
| 16 | `Block.UPDATE_KNOWN_SHAPE` | suppresses all three shape passes |
| 32 | `Block.UPDATE_SUPPRESS_DROPS` | `Block.updateOrDestroy`, whose destroy branch drops resources unless it is set |
| 64 | `Block.UPDATE_MOVE_BY_PISTON` | passed on as *movedByPiston*, and lets `BlockBehaviour.BlockStateBase.affectNeighborsAfterRemoval` run without bit 1 |
| 128 | `Block.UPDATE_SKIP_SHAPE_UPDATE_ON_WIRE` | `NeighborUpdater.executeShapeUpdate`, which then skips redstone wire |
| 256 | `Block.UPDATE_SKIP_BLOCK_ENTITY_SIDEEFFECTS` | suppresses `BlockEntity.preRemoveSideEffects` |
| 512 | `Block.UPDATE_SKIP_ON_PLACE` | suppresses `BlockBehaviour.BlockStateBase.onPlace` |

The named combinations are `Block.UPDATE_ALL` (3),
`Block.UPDATE_ALL_IMMEDIATE` (11, what placement uses),
`Block.UPDATE_NONE` (260) and `Block.UPDATE_SKIP_ALL_SIDEEFFECTS` (816).
`Block.UPDATE_LIMIT` is also 512, and is not a bit at all — it is the default
recursion budget for the shape cascade.

---

*Rules: names, never code · how the system works, not how the code reads ·
newest version only · every backticked name passes `tools/verify_names.py`.*
