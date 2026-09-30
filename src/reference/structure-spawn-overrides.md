# Structure spawn overrides

> Generated from the **26.3** decompile by `tools/gen_reference.py`. Do not edit by hand.

Which structures replace a biome's spawn list, for which mob category, and with what. A structure JSON's `spawn_overrides` map is read into `Structure.spawnOverrides`; when `NaturalSpawner` builds a spawn list, `ChunkGenerator.getMobsAt` walks the structures that chunk references, in no fixed order, and the first that declares an override for the category and whose box contains the position answers; the biome's list is then not consulted. An override with an **empty** spawn list is therefore a *ban*, not a no-op. The one exception is the creatures a chunk gets while it generates: `NaturalSpawner.spawnMobsForChunkGeneration` draws the *creature* category from the biome's list and reads no override. *box* is `piece` (only inside a piece's own bounding box) or `full` (anywhere in the structure's box, which for a structure that adapts the terrain around it is grown by twelve blocks on every side). The mechanism is on [entity lifecycle](../systems/entities/entity-lifecycle.md#a-spawn-attempt-is-a-filter-not-a-conversation); the nether fortress has a second, hard-coded list in front of this one.

52 structures carry the field · **6** declare an override · 23 overrides in all

| structure | category | box | what spawns instead (weight, min–max) |
|---|---|---|---|
| `ancient_city` | ambient | full | **nothing** — the category is suppressed inside the box |
| `ancient_city` | axolotls | full | **nothing** — the category is suppressed inside the box |
| `ancient_city` | creature | full | **nothing** — the category is suppressed inside the box |
| `ancient_city` | misc | full | **nothing** — the category is suppressed inside the box |
| `ancient_city` | monster | full | **nothing** — the category is suppressed inside the box |
| `ancient_city` | underground_water_creature | full | **nothing** — the category is suppressed inside the box |
| `ancient_city` | water_ambient | full | **nothing** — the category is suppressed inside the box |
| `ancient_city` | water_creature | full | **nothing** — the category is suppressed inside the box |
| `fortress` | monster | piece | `blaze` (10, 2–3), `zombified_piglin` (5, 4–4), `wither_skeleton` (8, 5–5), `skeleton` (2, 5–5), `magma_cube` (3, 4–4) |
| `monument` | axolotls | full | **nothing** — the category is suppressed inside the box |
| `monument` | monster | full | `guardian` (1, 2–4) |
| `monument` | underground_water_creature | full | **nothing** — the category is suppressed inside the box |
| `pillager_outpost` | monster | full | `pillager` (1, 1–1) |
| `swamp_hut` | creature | piece | `cat` (1, 1–1) |
| `swamp_hut` | monster | piece | `witch` (1, 1–1) |
| `trial_chambers` | ambient | piece | **nothing** — the category is suppressed inside the box |
| `trial_chambers` | axolotls | piece | **nothing** — the category is suppressed inside the box |
| `trial_chambers` | creature | piece | **nothing** — the category is suppressed inside the box |
| `trial_chambers` | misc | piece | **nothing** — the category is suppressed inside the box |
| `trial_chambers` | monster | piece | **nothing** — the category is suppressed inside the box |
| `trial_chambers` | underground_water_creature | piece | **nothing** — the category is suppressed inside the box |
| `trial_chambers` | water_ambient | piece | **nothing** — the category is suppressed inside the box |
| `trial_chambers` | water_creature | piece | **nothing** — the category is suppressed inside the box |

The other 46 structures carry the field empty — the field is required — and the biome's list stands.
