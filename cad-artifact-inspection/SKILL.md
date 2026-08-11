---
name: cad-artifact-inspection
description: Use when CAD, SolidWorks, FreeCAD, STEP, STP, STL, DXF, DWG, PDF drawing, 3MF, GLB, screenshot, render, or exported engineering deliverable files need read-only inspection for existence, freshness, nonblank content, pages, entities, triangles, bounding boxes, layers, text, dimensions, or format-specific verification evidence.
---

# CAD Artifact Inspection

## Overview

Inspect final CAD artifacts as files with measurable content, not just as paths in a report. Use this skill to gather read-only evidence for neutral exports before final delivery claims.

## Core Rule

Artifact inspection proves only artifact-level facts: existence, size, timestamps, parseability, page/entity/triangle counts, and limited format sanity. It does not prove engineering correctness, strength, manufacturability, SolidWorks native health, or visual professionalism by itself.

Use `scripts/inspect_cad_artifacts.py` to produce a JSON inspection report. The script is read-only and does not execute external CAD tools.

## Script Usage

```powershell
python .\.codex\skills\cad-artifact-inspection\scripts\inspect_cad_artifacts.py `
  --root . `
  --output .\deliverables\artifact-inspection.json `
  .\deliverables\part.step .\deliverables\drawing.pdf .\deliverables\plate.dxf
```

The script exits nonzero when final files are missing, empty, or fail basic format inspection. Use `--allow-fail` only when intentionally recording failure evidence.

## Format Coverage

| Format | Evidence gathered |
|---|---|
| PDF | page count, text length, image count, drawing object count when PyMuPDF is available |
| DXF | document version, modelspace entity count, layers, text, dimensions, entity type counts when ezdxf is available |
| STL | ASCII/binary detection, triangle count, vertex count, bounding box |
| STEP/STP | ISO-10303 markers, DATA section, entity count, common shape/product entity counts; geometry remains unverified without a STEP kernel |
| DWG | existence, size, timestamp, and unsupported-parser warning unless a local DWG parser/converter is available |
| Other | existence, size, timestamp, extension, and unsupported warning |

## Status Labels

- **pass**: file exists, is non-empty, and the available parser found nonblank format content.
- **partial**: file exists but parser support is limited, optional dependency is missing, or only container sanity was checked.
- **fail**: file missing, empty, unreadable, malformed, or appears blank.

If a file receives partial, do not call the deliverable fully verified. Report exactly which evidence is missing.

## Handoff

Use with:

- `cad-evidence-ledger` to record paths, hashes, timestamps, and inspection report files.
- `cad-final-verification` before claiming files are ready.
- `cad-visual-layout` for drawing/PDF composition and readability after PDF inspection.
- `cad-reference-match` for local reference crops after artifact parsing.
- `cad-solidworks-native-preflight` for `.sldprt`, `.sldasm`, and `.slddrw`; neutral artifact inspection cannot prove native SolidWorks quality.

## Common Mistakes

- Treating STEP text sanity as proof of valid B-rep geometry.
- Treating PDF page count as proof that drawing layout is professional.
- Treating DXF entity count as proof dimensions and layers are correct.
- Treating STL triangle count as proof the model is manifold or manufacturable.
- Ignoring partial results from unsupported DWG or missing parser dependencies.
