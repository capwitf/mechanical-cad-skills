---
name: cad-reference-acceptance
description: Use when a CAD, DWG, DXF, PDF, SVG, PNG, screenshot, scan, or mechanical drawing is claimed to match, replicate, trace, copy, or visually follow a reference, especially after "looks similar", "复刻", "照着画", "不像", "分格", "逐格", or acceptance concerns.
---

# CAD Reference Acceptance

## Core Rule

Never accept a reference-matched CAD/drawing result from whole-page appearance, file validity, entity count, or one broad crop. A match claim needs numbered local-region evidence from the final delivered file.

Observed failure this skill prevents: a hand-redrawn mechanical sheet passed file checks and coarse crop checks, but failed when split into 16 numbered cells.

## Acceptance Gate

Use this gate before saying a reference match is ready:

1. Fix the reference source path and final output path.
2. Render or open the final output, not a working preview.
3. Split both into a numbered grid; default is 4x4, numbered left-to-right, top-to-bottom.
4. Compare each cell for pixel similarity, edge difference, line density, text/leader placement, holes, hatches, dimensions, and view boundaries.
5. List the worst cells and root class: geometry, proportion, line type, hatch, annotation, layout, export, or stale file.
6. If any required cell fails, fix the source of truth and regenerate.
7. Save the grid overlay, side-by-side grid, CSV/JSON metrics, and final file evidence.

Do not bury weak cells inside a good average. Report minimum score and worst cell IDs.

## Default Thresholds

Use thresholds as tripwires, not proof:

| Check | Default |
|---|---:|
| grid | 4x4 |
| minimum cell similarity | >= 0.94 |
| average cell similarity | >= 0.95 |
| maximum edge difference | <= 0.08 |

If the reference is a noisy scan, photo, compressed image, or intentionally redrawn semantic CAD, adjust thresholds but state the reason.

## Visual vs Editable CAD

Choose and state the target:

| Target | Acceptance focus | Risk label |
|---|---|---|
| Visual replica | grid similarity, local outlines, text appearance, hatches | Text/dimensions may be outlines or hatches |
| Editable CAD drawing | LINE/ARC/MTEXT/DIMENSION objects, layers, scale, CAD semantics | Visual similarity may be lower until manually aligned |

Do not deliver a traced outline file while implying it is an editable engineering drawing. Do not deliver editable but rough CAD while implying visual replication.

## Script

Use `scripts/grid_acceptance.py` when reference and output can be rendered as images or PDFs:

```powershell
python .\.codex\skills\cad-reference-acceptance\scripts\grid_acceptance.py `
  --reference .\reference.png `
  --candidate .\output.pdf `
  --output-dir .\deliverables\acceptance `
  --rows 4 --cols 4 `
  --min-similarity 0.94 `
  --max-edge-diff 0.08
```

The script writes:

- `grid_acceptance.json`
- `grid_acceptance.csv`
- `reference_grid.png`
- `candidate_grid.png`
- `side_by_side_grid.png`

## Required Report

Report:

- reference source used,
- final output file checked,
- grid size and thresholds,
- min/average similarity,
- worst cell IDs,
- whether all cells passed,
- root causes for failed cells,
- final file checks and any unverified claims.

## Common Mistakes

- Treating PDF/DXF/DWG existence as match evidence.
- Comparing only the whole sheet or one large view crop.
- Reporting average similarity without the minimum and worst cells.
- Comparing a preview while delivering a stale CAD file.
- Mixing visual-trace output with editable-CAD claims.
