---
name: cad-illustration-vectorization
description: Use when a portrait, poster, logo, character, artwork, photo, hand-drawn image, or decorative reference must become editable vector line art in SVG, DXF, or DWG, especially after requests such as 人物转CAD, 图片转线稿, 插画转DWG, 照片描线, logo转DXF, or editable outline.
---

# Illustration Vectorization

## Core Rule

Treat a supplied artwork or photograph as an illustration-vectorization task, not an engineering CAD task, unless the user also supplies dimensions, manufacturing intent, or a technical drawing requirement.

Editable vector output is a valid result, but it is not a mechanical model, a manufacturing drawing, or a dimensionally accurate trace.

## Illustration Gate

Route here when the source is primarily a portrait, poster, logo, character, artwork, photograph, or freehand sketch and the requested result is an editable outline, silhouette, graphic line art, or decorative DXF/DWG/SVG.

Before drawing, lock:

- output format: SVG, DXF, DWG, or a stated combination;
- style: silhouette, clean contour, simplified facial features, detailed contour, or technical-looking illustration;
- fidelity target: semantic likeness, major-contour likeness, or local-feature likeness;
- color handling: monochrome, layer-separated colors, or no color;
- intended use: display, plotter, engraving, vinyl, laser marking, or reference only;
- whether the user wants automatic tracing, manual cleanup, or both.

Ask one focused question if the desired line-art density or intended fabrication use changes the result. Otherwise state the assumed simplification level.

## Do Not Use

- Do not use `text-to-cad`, build123d, or STEP-first generation for freehand illustration, portraits, or photographs without required mechanical geometry.
- Do not use `cad-reference-match` or `jixie-fuke` as the primary route; their mechanical regions, dimensions, sections, hatches, title blocks, and engineering acceptance grids are not suitable for artwork.
- Do not add engineering dimensions, datums, hatches, BOMs, title blocks, or manufacturing claims unless the user explicitly requests and supplies the relevant information.
- **No mechanical title block:** do not add an engineering title block, dimensions, BOM, or datums to illustration output by default.
- Do not claim exact likeness or trace accuracy from entity counts, a nonblank DWG, or a single zoomed-out preview.

## Source and Entity Rules

Prefer a regenerable vector source:

| Output | Preferred editable entities |
|---|---|
| SVG | paths, polylines, curves, and text where intended |
| DXF/DWG | polylines, splines, arcs, circles, and text on semantic graphic layers |

Use layer names that express graphic intent, such as `CONTOUR`, `FEATURE`, `ACCENT`, `TEXT`, and `GUIDE`. Do not use an external raster image as the delivered result when the user asked for editable linework. Temporary raster underlays are allowed only for tracing and must be removed or explicitly retained by user request.

## Acceptance

Verify the final delivered vector/DXF/DWG, not only a working preview:

1. Reopen it with the selected vector/CAD tool.
2. Confirm native editable entities exist and list their types/layers.
3. Confirm no unintended raster, OLE, or external reference remains when fully editable output was requested.
4. Review the full composition and at least these local regions when present: face/head, torso/primary shape, hands or small features, and text/logo.
5. Compare semantic silhouette, key contours, feature placement, and intended text—do not apply engineering dimension or grid thresholds to an artistic reference.
6. Record the source script or vector source, final output, and any deliberate simplifications in `cad-evidence-ledger`.

Use `cad-artifact-inspection` for file-level evidence and `cad-evidence-ledger` for source/output provenance. Use `cad-region-compare` only as visual support; it cannot prove artistic fidelity or editable semantics.

## Reporting

Report:

- output path and editable entity types;
- source method and whether an underlay remains;
- accepted likeness target and deliberately simplified regions;
- visual review regions checked;
- Verified, Inferred, and Unverified claims;
- explicit statement: **No engineering claim** unless dimensions and manufacturing intent were provided.

## Common Mistakes

- Treating a portrait as a mechanical reference drawing.
- Adding a title block, dimensions, or engineering text to decorative line art.
- Calling a rough semantic contour an exact photographic trace.
- Delivering a raster image embedded in DWG when editable vectors were requested.
- Using STEP-first CAD to solve a 2D illustration problem.
