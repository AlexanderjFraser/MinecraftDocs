# Submit phases and feature renderers

> Verified against **Minecraft 26.3** · Reference · Hand-kept from
> `SubmitNodeCollection` and the `FeatureRenderDispatcher` constructor.

Everything an entity, block entity, particle or debug renderer draws in a
level arrives as a *submit node* — the sky is drawn by its own renderer in its
own frame-graph pass; the clouds, the weather and the world border by their
own renderers inside the main pass; and terrain by its chunk sections.
`SubmitNodeCollection` sorts those nodes into fifteen named phases as they
come in, and twelve feature renderers turn them into vertices. The lecture
that frames both is [entity rendering](../systems/rendering/entity-rendering.md),
which names four of the phases and one of the renderers. Two more renderers
are named elsewhere — `TextFeatureRenderer` on
[text and fonts](../systems/client/text-and-fonts.md), `QuadParticleFeatureRenderer`
on [particles](../systems/rendering/particles.md) — and everything else here is
only here.

## The fifteen phases

One `SubmitNodeCollection` holds fourteen of them, and a `SubmitNodeStorage`
holds one collection per *order* bucket — the global draw order [a submit
chooses with
`SubmitNodeCollector.order`](../systems/rendering/entity-rendering.md#submit-describing-a-draw-without-making-one) —
and the fifteenth, *seeThrough*, which every one of its collections shares.
So "every order bucket" below means every one of those collections in turn.

Those fifteen are the set with improved transparency off, which is how every
storage but `LevelRenderer`'s always runs; the level's follows
`GameRenderer.useImprovedTransparency` each frame, through
`SubmitNodeStorage.setUseImprovedTransparency`. With it on, rows 2 to 10 and
row 12 are ten names for one simple phase, `SubmitNodeCollection.oitTranslucent`,
which `FeatureRenderDispatcher.PreparedFrame.executeOit` drains three times,
once per `OitStage`. Row 11 is drained on its own, by
`FeatureRenderDispatcher.PreparedFrame.executeWaterMask`.

Rows 1 to 14 are in the order of `SubmitNodeCollection.allPhases`, and row 15
comes last because `SubmitNodeStorage.drainPhases` hands it over after every
bucket's. That is *not* the order they are drawn in, and neither is the last
column: `FeatureRenderDispatcher.PreparedFrame.executeTranslucent`
alone makes three separate sweeps over every order bucket, so the phases it
drains are numbered by sweep — but *within* a sweep the order is the one the
sweep's own statements run in, not the order of the rows. Sweep 1 drains
shadows, then translucent models, then name tags, then texts, then
translucent custom geometry — so in each bucket translucent models, row 7, are
drawn **before** the name tags and texts of rows 3 and 4.

Three of the fifteen are a `TranslucentFeatureRenderPhase` — rows 6, 7 and 15,
*translucentBlocksAndItems*, *translucentModels* and *seeThrough* — and the
other twelve a `SimpleFeatureRenderPhase`, which is not what half the names
suggest. What lets those three sort at all is on the node rather than the
phase: `TranslucentSubmit` is a marker interface declaring one method,
`TranslucentSubmit.distanceToCameraSq`, and **five** of the twelve renderers'
nested *Submit* records implement it — `BlockModelFeatureRenderer`,
`ItemFeatureRenderer`, `ModelFeatureRenderer`, `MovingBlockFeatureRenderer` and
`TextFeatureRenderer`. A phase can only order what its nodes can answer. What the two kinds do differently to a node's
chance of sharing a draw is [entity
rendering](../systems/rendering/entity-rendering.md#prepare-sorting-batching-and-the-vertices)'s.

| # | phase | what lands in it | drained by |
|---:|---|---|---|
| 1 | `SubmitNodeCollection.solid` | the opaque default: models whose `RenderType` does not blend or forces the solid phase (`RenderType.forceSolidModelPhase`), block models whose render type does not blend, moving blocks whose model does not declare the translucent material flag, an item's quads whose render type does not blend, custom geometry that neither blends nor outlines, the opaque half of every quad-particle group, every flame and every leash — plus the opaque cases rows 3, 4, 5, 9, 10 and 12 send here | `.executeSolid` |
| 2 | `SubmitNodeCollection.shadows` | one node per `SubmitNodeCollection.submitShadow`, carrying the radius and the `EntityRenderState.ShadowPiece` list sampled at extract | `.executeTranslucent`, sweep 1 |
| 3 | `SubmitNodeCollection.nameTags` | every name tag's node in `Font.DisplayMode.NORMAL`, see-through or not — a see-through one's carries an emission bump on its light, opaque white and no background, and while the level renders goes to *solid* instead | `.executeTranslucent`, sweep 1 |
| 4 | `SubmitNodeCollection.texts` | world-space text that is not a name tag, from `SubmitNodeCollection.submitText`, and a text display's background, from `SubmitNodeCollection.submitTextBackground`, when not see-through — though while the level renders, text in opaque colour with no background goes to *solid* | `.executeTranslucent`, sweep 1 |
| 5 | `SubmitNodeCollection.shapeOutlines` | `VoxelShape` edge outlines submitted **without** the after-terrain flag, unless their colour is fully opaque — those go to *solid*, flag or not | `.executeTranslucent`, sweep 2 |
| 6 | `SubmitNodeCollection.translucentBlocksAndItems` | an item's quads whose render type blends — an item with both kinds is two nodes, here and in *solid* — block models whose render type blends, and moving blocks whose model declares the translucent material flag | `.executeTranslucent`, sweep 3 |
| 7 | `SubmitNodeCollection.translucentModels` | entity models whose `RenderType` blends and does not force the solid phase | `.executeTranslucent`, sweep 1 |
| 8 | `SubmitNodeCollection.translucentCustomGeometry` | custom geometry whose `RenderType` blends — a simple phase in spite of the name, so it is not distance-sorted | `.executeTranslucent`, sweep 1 |
| 9 | `SubmitNodeCollection.translucentGizmos` | the translucent debug primitive group submitted **without** the on-top flag — its opaque twin goes to *solid* | `.executeTranslucent`, sweep 2 |
| 10 | `SubmitNodeCollection.breakingOverlay` | the crumbling decal over geometry that blends: a model's `ModelFeatureRenderer.CrumblingOverlay`, from `SubmitNodeCollection.submitCrumblingOverlay` on a render type that admits one, and a `SubmitNodeCollection.submitBreakingBlockModel` for a block whose model declares the translucent material flag — over anything opaque the decal goes to *solid* | `.executeTranslucent`, sweep 3 |
| 11 | `SubmitNodeCollection.waterMask` | models submitted with the water-mask render type | `.executeTranslucent`, sweep 3 |
| 12 | `SubmitNodeCollection.afterTerrain` | outlines flagged after-terrain, unless fully opaque, plus the translucent half of every quad-particle group | `.executeTranslucentAfterTerrain` |
| 13 | `SubmitNodeCollection.alwaysOnTopGizmos` | gizmo groups flagged on top, opaque or not | `.executeAlwaysOnTop` |
| 14 | `SubmitNodeCollection.outline` | a second copy of a model, block model, moving block or item whose outline colour was non-zero — a model or block model only where its render type has an outline variant, and a moving block or item with its ordinary type, re-typed inside the feature renderer or dropped there — plus custom geometry, which is not a second copy at all: an outline render type routes the *only* copy here | `.executeOutline`, which `FeatureRenderDispatcher.renderAllFeatures` never calls — `LevelRenderer` does, into its own target |
| 15 | `SubmitNodeCollection.seeThrough` | the storage's one phase, `SubmitNodeStorage.seeThrough`, not one per bucket: the *second* node a see-through name tag emits, in `Font.DisplayMode.SEE_THROUGH` with the background restored, and any text or text background submitted in that mode — sorted by distance across every bucket at once | `FeatureRenderDispatcher.PreparedFrame.executeSeeThrough`, once for the whole storage |

Two rows are worth reading twice. A quad-particle group reaches the collector
in one call and becomes **two** nodes, one in *solid* and one in
*afterTerrain*, each wrapping the same render state with a flag that picks
which of its layers it draws. And *outline* is not simply *solid*
submitted twice: the glow is a second submission for a model, a block model, a
moving block or
an item, but flames, leashes and quad particles never reach it at all, a
blending model pairs its outline copy with *translucentModels* rather than
*solid* unless its render type forces the solid phase, and custom geometry goes
to one phase or the other and never both.

## The twelve feature renderers

In the order `FeatureRenderDispatcher`'s constructor registers them. All but
one extend `RenderTypeFeatureRenderer`, which owns the shared
`StagedVertexBuffer` draw and the merging of consecutive same-render-type
geometry.

| feature renderer | what it writes |
|---|---|
| `ShadowFeatureRenderer` | four vertices per `EntityRenderState.ShadowPiece` onto one shared shadow render type, with the piece's alpha as the colour and UVs derived from its bounds and the shadow radius |
| `FlameFeatureRenderer` | a stack of fire quads scaled to the entity's bounding box, alternating two block-atlas sprites and flipping their U every other pair, at full block light |
| `ModelFeatureRenderer` | the entity models: `Model.setupAnim` and then `Model.renderToBuffer` over the `ModelPart` tree, into a buffer optionally wrapped for a sheeted decal or a `UvMapping` — an atlas sprite, or an armour trim's paletted texture |
| `TextFeatureRenderer` | arbitrary world-space text and every name tag: glyph quads and background prepared through `Font` at the submitted pose and display mode, with an eight-direction outline pass and a polygon-offset second pass when an outline colour is set, and a text display's background submitted on its own |
| `LeashFeatureRenderer` | a ribbon between the two ends of an `EntityRenderState.LeashState`, walked twice — twenty-four steps out and twenty-four back for its two faces, a hundred vertices in all — with its light interpolated between the endpoints and its colour alternating per step |
| `ItemFeatureRenderer` | item quads, in one pass over the submits — a stack with a foil draws each quad on its material's glint render type, which samples the enchantment glint beside the item texture, so geometry and foil go out together |
| `CustomFeatureRenderer` | nothing of its own: it hands the caller's `SubmitNodeCollector.CustomGeometryRenderer` a vertex consumer for the requested render type |
| `BlockModelFeatureRenderer` | the quads of a `BlockStateModelPart` list, in `Direction` order, at one fixed light and overlay coordinate for the whole submit |
| `MovingBlockFeatureRenderer` | a whole block state re-tesselated through `ModelBlockRenderer` — pistons and falling blocks — honouring the ambient-occlusion and cutout-leaves options |
| `QuadParticleFeatureRenderer` | the only one outside `RenderTypeFeatureRenderer`: it appends particle draws to the `StagedVertexBuffer` per `SingleQuadParticle.Layer` and issues them into the `RenderPass` it is handed, on each layer's own pipeline |
| `ShapeOutlineFeatureRenderer` | two line vertices per edge of a `VoxelShape`, each carrying a per-vertex line width |
| `GizmoFeatureRenderer` | the debug vocabulary: quads, triangle fans, lines, texts and points out of a `DrawableGizmoPrimitives.Group`, camera-relative |

Those twelve are the answer to *what can be drawn from a submit node* —
which, by the exclusions the opening makes, is everything in a level except
the sky, the clouds, the weather, the world border and terrain. Anything a
renderer wants that none of the other eleven draws goes through
`CustomFeatureRenderer`.

---

*Rules: names, never code · how the system works, not how the code reads ·
newest version only · every backticked name passes `tools/verify_names.py`.*
