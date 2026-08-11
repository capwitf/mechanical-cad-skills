---
name: cad-evidence-ledger
description: Use when CAD, SolidWorks, FreeCAD, STEP, DXF, DWG, PDF, STL, 3MF, GLB, SLDPRT, SLDASM, SLDDRW, screenshots, renders, source scripts, or engineering deliverables need a verifiable evidence manifest with file paths, hashes, modified times, source provenance, checks run, and Verified/Inferred/Unverified claims.
---

# CAD Evidence Ledger

## Overview

A CAD result is not ready because the final answer says it is ready. Create an evidence ledger that records the actual files, source of truth, checks, and claim status behind the delivery.

## Core Rule

Before final CAD reporting, produce or update an evidence ledger when files are delivered, external tooling was used, or the task has had quality complaints. The ledger must make stale files, missing formats, unchecked geometry, and overclaims visible.

Use `scripts/cad_evidence_manifest.py` to generate a JSON manifest for final files. The script records file existence, size, modified time, SHA256, source provenance, recorded checks, and claim categories. It does not execute external commands.

## Evidence Manifest

Record these fields:

| Field | Meaning |
|---|---|
| Final files | Requested outputs with path, exists, size, modified time, hash, and extension |
| Source of truth | CAD document, script, SolidWorks/FreeCAD model, or existing drawing used to generate outputs |
| Toolchain | FreeCAD, SolidWorks, text-to-cad, build123d, CadQuery, converter, renderer, or manual source |
| Checks run | Commands or inspections performed; record text only, do not fake execution |
| Evidence files | Screenshots, renders, cropped comparisons, logs, exported previews, or open/rebuild reports |
| Artifact inspection | `cad-artifact-inspection` JSON report path and pass/partial/fail summary when produced |
| Claims | Verified, Inferred, and Unverified statements |
| Blockers | Missing tools, missing dimensions, stale files, failed opens/renders, or manual judgement needed |

## Script Usage

```powershell
python .\.codex\skills\cad-evidence-ledger\scripts\cad_evidence_manifest.py `
  --root . `
  --source .\models\bracket.py `
  --toolchain "FreeCAD export" `
  --check "Rendered PDF page 1 nonblank" `
  --verified "Final STEP exists and hash recorded" `
  --unverified "Strength not calculated; loads missing" `
  --output .\deliverables\cad-evidence.json `
  .\deliverables\bracket.step .\deliverables\bracket.pdf
```

If any final file is missing and `--allow-missing` was not used, the script exits nonzero. Missing files in a manifest are failure evidence, not acceptable delivery.

## Claim Categories

- **Verified**: directly checked from the final file, rebuilt source, open/render log, measurement, hash, screenshot, or script output.
- **Inferred**: plausible from source or tool behavior, but not directly checked in the final file.
- **Unverified**: not checked, blocked, missing data, missing tool, or requires human engineering judgement.

Do not bury Unverified items under a success summary. If strength, fit, layout, or native SolidWorks quality was not directly checked, say so.

## Required Evidence by Deliverable

| Deliverable | Minimum evidence |
|---|---|
| STEP/STL/3MF/GLB | exists, size, mtime, hash, bounding box or open/render evidence when tools allow |
| DXF/DWG | exists, size, mtime, hash, entity/layer/text/dimension checks when tools allow |
| PDF drawing | exists, size, mtime, hash, page render or screenshot, title block and layout checks |
| SolidWorks native | exists, size, mtime, hash, SolidWorks open/rebuild/save/export evidence when available |
| Source script/model | exists, hash, rerun or rebuild status, generated outputs tied to same run |
| Reference match | reference/output crop evidence, region checklist, comparison notes or metrics |

## Handoff

Use with:

- `cad-final-verification` before claiming delivery is ready.
- `cad-artifact-inspection` to generate read-only parser evidence for STEP/STL/DXF/DWG/PDF artifacts.
- `cad-toolchain-preflight` to record local tool proof.
- `cad-engineering-sanity` to label mechanical claims.
- `cad-visual-layout` and `cad-design-richness` to record subjective gates separately from file evidence.

## Common Mistakes

- Reporting paths without checking the files exist.
- Mixing old exports with new source.
- Recording commands that were planned but not run.
- Treating hash/mtime as proof of geometry correctness.
- Marking human judgement items as Verified.
