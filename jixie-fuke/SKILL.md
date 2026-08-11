---
name: jixie-fuke
description: Use when a mechanical engineering drawing, CAD drawing, SolidWorks drawing, DXF, DWG, PDF, screenshot, scan, reference image, or existing CAD output must be copied, imitated, matched, traced, replicated, or kept visually close to a supplied reference, including jixie zhitu, gongcheng zhitu, zhuangpei tu, lingjian tu, cankao tu, zhao zhe hua, yiyang, xiangsi, mofang, fuke, tiejin, or bu xiang.
---

# Jixie Fuke

## Overview

Use this project-local wrapper as the discoverable skill entry for mechanical reference replication. It keeps the deeper root-level `jixie-fuke` rules reachable from the local `.codex/skills` skill cluster.

## Detailed Rule Source

If `../../../jixie-fuke/SKILL.md` exists relative to this skill directory, read it before doing reference replication work. Treat it as the detailed local rule set for:

- reference decomposition,
- local region comparison,
- crop comparison reports via `cad-region-compare` when PDF/image regions are available,
- source-level CAD fixes,
- loop verification,
- mechanical drafting review,
- final reference-match reporting.

If that file is missing, continue with the compact rules below and report that the detailed root rule set was unavailable.

## Compact Rules

- Use this skill only when a reference drawing, screenshot, PDF, scan, DWG/DXF, or existing CAD output exists.
- Do not use reference matching for no-reference original design; use `cad-original-design` instead.
- Split the reference into local regions before editing: sheet layout, views, sections, local features, hatches, line types, dimensions, title block, BOM, and notes.
- Compare the final output against the reference by local crop or zoomed region, not only a whole-page preview.
- Use `cad-region-compare` for high-risk rendered PDF/image crops when possible.
- Use `cad-reference-acceptance` before claiming a reference match is ready; whole-page similarity or a few broad crops are not enough.
- Fix the source of truth: CAD model, drawing, script, SolidWorks document, or FreeCAD file.
- Regenerate final outputs and re-check from the delivered files.

## Handoff

Use with:

- `cad-reference-match` as the cluster-level reference-matching entry.
- `cad-reference-acceptance` for numbered grid acceptance, minimum/worst-cell reporting, and visual-vs-editable CAD claim separation.
- `cad-region-compare` for rendered PDF/image crop metrics and diff images.
- `cad-visual-layout` when the matched drawing also needs formal sheet quality.
- `cad-evidence-ledger` to record reference/output crops, regenerated files, hashes, and comparison claims.
- `cad-final-verification` before reporting ready.

## Common Mistakes

- Claiming "matches" from a full-page screenshot.
- Missing small shaft shoulders, holes, hatches, sections, or dimension chain differences.
- Fixing only the preview while the CAD source remains stale.
- Using this skill when there is no reference to imitate.
