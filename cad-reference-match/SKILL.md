---
name: cad-reference-match
description: Use when a CAD drawing, SolidWorks drawing, FreeCAD output, DXF, DWG, PDF, screenshot, rendered model, or mechanical drawing must match, imitate, trace, copy, or stay visually close to a reference image, PDF, screenshot, scan, or existing CAD file.
---

# CAD Reference Match

## Core Rule

Whole-page similarity is not enough. Verify local engineering regions before claiming a CAD output matches a reference.

If project-local `jixie-fuke` is available in `.codex/skills/jixie-fuke`, use it as the detailed reference-replication rule set. This skill provides the shorter cluster entry point and handoff.

If no reference drawing, screenshot, PDF, scan, or existing CAD output exists, do not use this skill. Use `cad-original-design` and judge the result against the design brief instead.

Use `cad-reference-acceptance` before claiming readiness. Use `cad-region-compare` when reference/output PDF or image regions can be rendered or cropped. Treat metrics as supporting evidence, not automatic proof of matching.

## Region Checklist

Split the reference into regions:

- sheet layout and view placement,
- main outlines and proportions,
- section/detail views,
- holes, shafts, bosses, ribs, flanges, ports, grooves, chamfers, fillets, threads,
- hatches, hidden lines, centerlines, leaders, balloons, dimensions, tolerances,
- title block, BOM, notes, material, scale, drawing number.

Also create a numbered grid, default 4x4, and report minimum similarity, average similarity, worst cell IDs, and failed cell IDs. Do not accept a drawing from whole-page or broad-region similarity alone.

Record what the reference shows before editing. Use feature descriptions, not vague notes like "left side wrong".

## Comparison Loop

1. Render or open the reference and current final output.
2. Crop or zoom the same local region from both.
3. Compare outlines, feature count, centers, relative sizes, line types, hatches, and annotations.
4. Use `cad-region-compare` for high-risk PDF/image regions when possible, and save crop/diff evidence.
5. Classify each mismatch as geometry, proportion, section, line type, annotation, view layout, export, or stale file.
6. Fix the source of truth, then regenerate the final output.
7. Re-check from the final delivered file.

Do not fix only a screenshot or PDF if the source CAD, model, or script remains wrong.

## Acceptance

A reference-matched result is ready only when:

- all high-risk local regions were checked,
- available crop comparison reports were recorded for high-risk PDF/image regions,
- remaining differences are listed and acceptable,
- numbered grid acceptance passed or failed cells are explicitly listed with accepted reasons,
- final files are fresh and match the checked output,
- source files can regenerate the delivered output.

## Handoff

- Use `cad-requirements-lock` if dimensions, standards, or deliverables are unclear.
- Use `cad-original-design` if there is no reference and the CAD must be designed from requirements.
- Use `cad-toolchain-preflight` if a CAD tool, MCP server, converter, or SolidWorks bridge is unverified.
- Use `cad-region-compare` when reference and output regions can be compared as PDF/image crops.
- Use `cad-reference-acceptance` for final numbered-grid acceptance before "matches the reference" claims.
- Use `cad-final-verification` before final reporting.

## Common Mistakes

- Saying "looks close" from a zoomed-out page preview.
- Missing small shaft shoulders, hole centers, section boundaries, or hatch omissions.
- Correcting annotations while the actual geometry remains wrong.
- Comparing a working file but delivering a stale exported file.
