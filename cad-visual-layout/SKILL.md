---
name: cad-visual-layout
description: Use when a CAD, SolidWorks, FreeCAD, DXF, DWG, PDF, screenshot, or mechanical engineering drawing needs visual layout, drawing composition, readability, line hierarchy, title block, view placement, annotation spacing, or formal drawing appearance review.
---

# CAD Visual Layout

## Core Rule

A technically valid drawing can still look unprofessional. Do not call a drawing ready if the sheet is empty, scattered, too small to read, visually flat, or poorly composed.

## Layout Gate

Check the final sheet or plotted view for:

| Area | Pass condition |
|---|---|
| Sheet frame | Border, margins, title block, and revision/table areas feel aligned and intentional |
| View hierarchy | Main view is dominant; side/top/section/detail views support it without equal-weight clutter |
| Alignment | Views share centers, projection relationship, baselines, or clear visual grid |
| Spacing | White space is balanced; views do not float randomly or crowd the frame |
| Scale | Primary geometry is large enough to inspect; not lost in the sheet |
| Text | Dimensions, labels, notes, BOM, and title block are readable at final output size |
| Line hierarchy | Visible, hidden, center, section, dimension, leader, border, and construction lines have distinct weight/style |
| Sections | Hatch spacing and angle are readable and do not overpower geometry |
| Dimensions | Dimension chains, leaders, arrows, and balloons do not cross, overlap, drift, or hide features |
| Thumbnail impression | The first zoomed-out view looks like an organized formal engineering drawing |

## Layout Scorecard

Score the final plotted sheet from 0 to 20. Use 0 for fail, 1 for marginal, 2 for pass:

| Item | Check |
|---|---|
| Frame/title block | Border, title block, revision/material/scale areas are present and aligned |
| View hierarchy | Primary view is clearly dominant and supporting views are subordinate |
| Projection alignment | Orthographic, section, detail, and auxiliary views align logically |
| Sheet occupancy | Geometry and tables fill the sheet without looking empty or crowded |
| Text readability | Dimensions, notes, balloons, BOM, and title block are legible at final size |
| Line hierarchy | Visible, hidden, center, hatch, dimension, leader, and border lines separate visually |
| Annotation routing | Dimensions/leaders avoid crossing, overlap, and ambiguous attachment |
| Section/detail quality | Hatches, cut lines, labels, and detail bubbles are readable and not overpowering |
| Information density | Enough dimensions, notes, views, and details exist for the target drawing level |
| Thumbnail impression | Zoomed-out page looks formal, organized, and balanced |

Minimum pass: score >= 16/20 with no critical fail. Score 12-15 is partial. Score < 12 is fail.

Critical fail conditions:

- blank or mostly empty sheet,
- primary geometry too small to inspect,
- missing title block on a formal drawing,
- unreadable dimension text,
- overlapping annotations that hide required features,
- stale export or wrong final file.

## Review Method

1. Open or render the final delivered sheet, not only the source workspace.
2. Inspect full sheet composition first.
3. Zoom into title block, dimensions, dense annotation regions, and sections.
4. Classify issues as alignment, scale, text, line hierarchy, spacing, section, annotation, or stale export.
5. Fix the source drawing/layout and re-export.
6. Re-check from the final file.

## Minimum Professionalism

For homework or simplified tasks, keep the drawing clean and readable. For professional-looking work, require a full frame, clear title area, stable view hierarchy, readable annotation, and enough information density that the sheet does not look empty.

If no reference style is provided, use conservative mechanical drafting conventions and report layout choices as assumptions.

## Common Mistakes

- Treating nonblank export as visual quality.
- Putting every view at the same size and weight.
- Leaving large empty zones while important details are tiny.
- Letting dimension text, arrows, or leaders cross geometry.
- Making hatch or hidden lines visually louder than visible outlines.
- Checking model geometry but not the plotted sheet.

## Reporting

Report:

- visual layout pass/fail,
- layout score and any critical fail,
- checked sheet/view regions,
- remaining visual risks,
- whether a reference style or rubric was available.
