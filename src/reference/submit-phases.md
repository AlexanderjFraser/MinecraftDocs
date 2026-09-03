# Submit phases and feature renderers

> Verified against **Minecraft 26.2** · Reference · Hand-kept from
> `SubmitNodeCollection` and the `FeatureRenderDispatcher` constructor.

Everything drawn in a level that is not terrain arrives as a *submit node*.
`SubmitNodeCollection` sorts those nodes into fifteen named phases as they
come in, and thirteen feature renderers turn them into vertices. The lecture
that frames both is [entity rendering](../systems/rendering/entity-rendering.md);
these are the two catalogues it names three or four examples from.

## The fifteen phases

In **declaration order**, which is also the order of
`SubmitNodeCollection.allPhases`. It is *not* the order they are drawn in:
that is the last column, and `FeatureRenderDispatcher.PreparedFrame.executeTranslucent`
alone makes three separate sweeps over every order bucket, so the phases it
drains are numbered by sweep below.

Three phases are a `TranslucentFeatureRenderPhase` and the other twelve a
`SimpleFeatureRenderPhase`. The simple phase groups its nodes by feature type
and then by batch key, and tells the dispatcher its groups may be reordered.
The translucent phase keeps every node, sorts them back to front by squared
distance to the camera, and marks the group strictly ordered — so consecutive
same-type nodes still merge, but nothing merges backwards past a stranger.

| # | phase | what lands in it | drained by |
|---:|---|---|---|
| 1 | `SubmitNodeCollection.solid` | the opaque default: models and block models whose `RenderType` does not blend, items with no translucent quad, custom geometry that neither blends nor outlines, plus every flame and every leash | `.executeSolid` |
| 2 | `SubmitNodeCollection.shadows` | one node per `SubmitNodeCollection.submitShadow`, carrying the radius and the `EntityRenderState.ShadowPiece` list sampled at extract | `.executeTranslucent`, sweep 1 |
| 3 | `SubmitNodeCollection.nameTags` | every name tag gets a node here, see-through or not — a see-through one lands with an emission bump on its light, opaque white, and no background | `.executeTranslucent`, sweep 1 |
| 4 | `SubmitNodeCollection.seeThroughNameTags` | the *second* node a see-through name tag emits, in `Font.DisplayMode.SEE_THROUGH` with the background restored | `.executeTranslucent`, sweep 1 |
| 5 | `SubmitNodeCollection.texts` | world-space text that is not a name tag, from `SubmitNodeCollection.submitText` | `.executeTranslucent`, sweep 1 |
| 6 | `SubmitNodeCollection.shapeOutlines` | `VoxelShape` edge outlines submitted **without** the after-terrain flag | `.executeTranslucent`, sweep 2 |
| 7 | `SubmitNodeCollection.translucentBlocksAndItems` | items with a translucent quad, block models whose render type blends, and moving blocks whose model declares the translucent material flag | `.executeTranslucent`, sweep 3 |
| 8 | `SubmitNodeCollection.translucentModels` | entity models whose `RenderType` blends | `.executeTranslucent`, sweep 1 |
| 9 | `SubmitNodeCollection.translucentCustomGeometry` | custom geometry whose `RenderType` blends — a simple phase in spite of the name, so it is not distance-sorted | `.executeTranslucent`, sweep 1 |
| 10 | `SubmitNodeCollection.gizmos` | debug primitive groups submitted **without** the on-top flag | `.executeTranslucent`, sweep 2 |
| 11 | `SubmitNodeCollection.breakingOverlay` | the crumbling decal: a model submitted with a `ModelFeatureRenderer.CrumblingOverlay` whose render type admits one, and every `SubmitNodeCollection.submitBreakingBlockModel` | `.executeTranslucent`, sweep 3 |
| 12 | `SubmitNodeCollection.waterMask` | models submitted with the water-mask render type | `.executeTranslucent`, sweep 3 |
| 13 | `SubmitNodeCollection.afterTerrain` | outlines flagged after-terrain, plus the translucent half of every quad-particle group | `.executeTranslucentAfterTerrain` |
| 14 | `SubmitNodeCollection.alwaysOnTop` | gizmo groups flagged on top | `.executeAlwaysOnTop` |
| 15 | `SubmitNodeCollection.outline` | a second copy of any model, block model, moving block, item or custom submit whose outline colour was non-zero, re-typed to the outline variant | `.executeOutline` |

Two rows are worth reading twice. A quad-particle group is submitted **once**
and lands in two phases at once, `solid` and `afterTerrain`, with a flag that
picks which of its layers each half draws. And `outline` is filled by the same
calls that filled `solid` — the glow is a second submission of the same
geometry, not a post-process over the first.

## The thirteen feature renderers

In the order `FeatureRenderDispatcher`'s constructor registers them. All but
one extend `RenderTypeFeatureRenderer`, which owns the shared
`StagedVertexBuffer` draw and the merging of consecutive same-render-type
geometry.

| feature renderer | what it writes |
|---|---|
| `ShadowFeatureRenderer` | four vertices per `EntityRenderState.ShadowPiece` onto one shared shadow render type, with the piece's alpha as the colour and UVs derived from its bounds and the shadow radius |
| `FlameFeatureRenderer` | a stack of fire quads scaled to the entity's bounding box, alternating two block-atlas sprites and flipping their U every other pair, at full block light |
| `ModelFeatureRenderer` | the entity models: `Model.setupAnim` and then `Model.renderToBuffer` over the `ModelPart` tree, into a buffer optionally wrapped for a sheeted decal or a single sprite |
| `NameTagFeatureRenderer` | the glyph quads and background of a name tag, prepared through `Font` at the submitted pose and display mode |
| `TextFeatureRenderer` | arbitrary world-space text, with an eight-direction outline pass and a polygon-offset second pass when an outline colour is set |
| `LeashFeatureRenderer` | a twenty-four-step ribbon between the two ends of an `EntityRenderState.LeashState`, its light interpolated between the endpoints and its colour alternating per step |
| `ItemFeatureRenderer` | item quads, in two passes over the same submits — geometry first, then the enchantment foil for every submit that has one |
| `CustomFeatureRenderer` | nothing of its own: it hands the caller's `SubmitNodeCollector.CustomGeometryRenderer` a vertex consumer for the requested render type |
| `BlockModelFeatureRenderer` | the quads of a `BlockStateModelPart` list, in `Direction` order, at one fixed light and overlay coordinate for the whole submit |
| `MovingBlockFeatureRenderer` | a whole block state re-tesselated through `ModelBlockRenderer` — pistons and falling blocks — honouring the ambient-occlusion and cutout-leaves options |
| `QuadParticleFeatureRenderer` | the only one outside `RenderTypeFeatureRenderer`: it appends particle draws to the `StagedVertexBuffer` per `SingleQuadParticle.Layer` and opens its own `RenderPass` to issue them |
| `ShapeOutlineFeatureRenderer` | two line vertices per edge of a `VoxelShape`, each carrying a per-vertex line width |
| `GizmoFeatureRenderer` | the debug vocabulary: quads, triangle fans, lines, texts and points out of a `DrawableGizmoPrimitives.Group`, camera-relative |

That list is the answer to *what can be drawn in a level*. Anything a mod or a
renderer wants that is not one of the other twelve has to go through
`CustomFeatureRenderer`.

---

*Rules: names, never code · how the system works, not how the code reads ·
newest version only · every backticked name passes `tools/verify_names.py`.*
