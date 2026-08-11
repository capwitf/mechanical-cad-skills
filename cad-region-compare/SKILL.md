---
name: cad-region-compare
description: Use when a CAD drawing, SolidWorks drawing, FreeCAD output, DXF/DWG/PDF export, screenshot, scan, render, or mechanical reference image needs local crop/region comparison against a generated output before claiming visual similarity, reference matching, layout matching, linework matching, or drawing replication quality.
---

# CAD Region Compare

## Overview

Compare the same local region from a reference and a current output. Use this to gather evidence for "matches the reference" claims beyond a whole-page preview.

## Core Rule

Region metrics are evidence, not judgement. A high similarity score does not prove dimensions, tolerances, layers, or engineering correctness. A low score is a prompt to inspect the source drawing and classify the mismatch.

Use `scripts/compare_regions.py` to compare PDF/image crops. The script is read-only and outputs JSON with crop paths and metrics.

## Script Usage

```powershell
python .\.codex\skills\cad-region-compare\scripts\compare_regions.py `
  --reference .\reference.pdf `
  --candidate .\output.pdf `
  --ref-page 0 `
  --candidate-page 0 `
  --crop 0.10,0.20,0.35,0.30 `
  --output-dir .\deliverables\region-checks `
  --label shaft-end
```

`--crop` accepts `x,y,w,h`. Values from 0 to 1 are treated as normalized fractions of the rendered page/image. Values above 1 are treated as pixels. Use separate `--ref-crop` and `--candidate-crop` when the matching regions are at different locations.

## Metrics

The JSON report includes:

- crop dimensions,
- mean absolute error,
- root mean square error,
- `normalized_similarity`,
- edge density for reference and candidate,
- edge difference,
- optional saved crop images and difference image.

Use metrics to prioritize manual review. Do not set a universal pass threshold across all CAD drawings because hatch density, text, scale, anti-aliasing, and scan quality vary.

## Region Checklist

Compare high-risk regions:

- main outline and proportions,
- holes, shafts, shoulders, ribs, bosses, flanges, slots, ports, grooves, chamfers, fillets, threads,
- section cuts and hatch behavior,
- dimension chains, leaders, text, tolerances, surface symbols,
- title block, BOM, notes, and scale fields,
- any user-complained region.

## Handoff

Use with:

- `cad-reference-match` when the task requires reference similarity.
- `jixie-fuke` for detailed mechanical replication rules.
- `cad-artifact-inspection` before comparing generated PDF/image artifacts.
- `cad-evidence-ledger` to record crop reports and saved crop images.
- `cad-final-verification` before claiming a reference-matched deliverable is ready.

## Common Mistakes

- Comparing only full sheets and missing local geometry errors.
- Comparing different regions or different scales without saying so.
- Treating image similarity as proof of dimensions.
- Ignoring a low-score crop because the whole sheet looks close.
- Fixing only a screenshot instead of the CAD source.
