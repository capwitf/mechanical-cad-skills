---
name: cad-final-verification
description: Use when Codex is about to claim a CAD, SolidWorks, FreeCAD, STEP, DXF, DWG, PDF drawing, STL, 3MF, GLB, SLDPRT, SLDASM, or SLDDRW deliverable is complete, ready, correct, matching, openable, regenerated, or suitable for delivery.
---

# CAD Final Verification

## Core Rule

Do not claim CAD work is complete until checks were run against the final delivered files, not only the working source, script output, or preview.

## Required Checks

Run the checks that fit the deliverable:

| Check | Evidence |
|---|---|
| Existence | Final files exist at the reported paths |
| Freshness | Modified times match the latest run or export |
| Artifact inspection | `cad-artifact-inspection` reports pass/partial/fail for neutral STEP/STL/DXF/DWG/PDF artifacts when local parsers are available |
| Evidence ledger | `cad-evidence-ledger` manifest records final file paths, SHA256, modified times, source, checks, and claim categories when delivery evidence is needed |
| Nonblank | File size, entity count, render, screenshot, or model tree is not empty |
| Open/render | DWG/DXF/PDF/STEP/STL opens or renders with available local tools |
| Source consistency | Script/model/SolidWorks/FreeCAD source can regenerate the final output |
| Format fit | Requested formats are present, not substituted silently |
| External intake | Any external skill, MCP server, repo, or automation workflow used for the result has read-only intake and local preflight evidence |
| Engineering sanity | `cad-engineering-sanity` passed or reports partial/fail when mechanical plausibility, fit, strength, load path, material, or manufacturability claims matter |
| SolidWorks native | `cad-solidworks-native-preflight` passed or reports partial/fail/unverified for `.sldprt`, `.sldasm`, `.slddrw`, rebuild, reopen, and export claims |
| Engineering content | Dimensions, features, layers, sections, annotations, BOM, and title data checked as applicable |
| Visual layout | `cad-visual-layout` passed for formal drawing sheets, PDFs, screenshots, or plotted views |
| Design richness | `cad-design-richness` passed when realistic mechanical complexity or self-designed structure is expected |
| Reference match | `cad-reference-match` passed when a reference must be matched |
| Reference acceptance | `cad-reference-acceptance` reports min/average score, worst cells, failed cells, and visual-vs-editable CAD target when reference matching is claimed |
| Region comparison | `cad-region-compare` reports are recorded for high-risk reference/output PDF or image regions when available |

Automated checks prove only what they check. If geometry was not inspected, say it is unverified.

## Report Categories

Use these labels in final reporting:

- **Verified**: directly checked from the final file or rebuilt source.
- **Inferred**: likely true from source logic, but not directly inspected.
- **Unverified**: not checked, blocked by missing tools, or outside the available evidence.

Never hide unverified items inside a success summary.

## Four Gates

Final CAD delivery must report these gates:

| Gate | Required result |
|---|---|
| Engineering correctness | pass/fail with checked dimensions, views, sections, features, material, tolerance, or stated limits |
| Engineering sanity | pass/fail/partial with load path, interfaces, clearances, materials, standard features, and unverified strength claims labeled |
| SolidWorks native | pass/fail/partial/unverified when native SolidWorks files are requested |
| Visual layout | pass/fail with sheet composition, readability, line hierarchy, and annotation spacing |
| Design richness | pass/fail with functional zones, standard features, professional details, and complexity target |
| File delivery | pass/fail with fresh, nonblank, openable requested files |

## Failure Handling

If a check fails:

1. Name the failed check.
2. Identify the likely root class: stale file, export failure, blank render, wrong format, geometry, annotation, section, layer, visual layout, design richness, title/BOM, or missing tool.
3. Fix the source of truth when editing is allowed.
4. Regenerate and rerun checks.
5. If editing is not allowed, report the blocker and next smallest action.

## Evidence Package

For nontrivial CAD deliveries, run `cad-evidence-ledger` and include or report the manifest path. The manifest should include:

- final files and requested formats,
- source of truth,
- toolchain notes,
- checks actually run,
- evidence files such as screenshots, renders, crops, or logs,
- Verified, Inferred, and Unverified claims.

Do not treat a manifest as geometry correctness. It proves provenance and file evidence; engineering, visual layout, design richness, and reference match still need their own gates.

Run `cad-artifact-inspection` before or alongside the evidence ledger for neutral exports. Treat pass as artifact-level evidence only. Treat partial as a required risk note. Treat fail as a file delivery failure unless the user explicitly asked for a diagnostic report.

## Final Answer Shape

Report briefly:

- final files,
- artifact inspection report when produced,
- evidence ledger manifest when produced,
- what changed,
- verified checks,
- external skill/tool provenance when relevant,
- SolidWorks native preflight pass/fail/partial/unverified when relevant,
- engineering sanity pass/fail/partial,
- visual layout pass/fail,
- design richness pass/fail,
- inferred or unverified items,
- open risks,
- next smallest action.

Do not use broad phrases like "all good" unless every required acceptance check actually passed.

## Handoff

- Use `cad-requirements-lock` if acceptance criteria are missing.
- Use `cad-external-skill-intake` if any external CAD skill, MCP server, repository, or automation workflow influenced the result.
- Use `cad-artifact-inspection` if STEP, STP, STL, DXF, DWG, PDF, or other neutral exported artifacts need read-only content checks.
- Use `cad-evidence-ledger` if final files, provenance, hashes, timestamps, evidence artifacts, or claim categories need a manifest.
- Use `cad-engineering-sanity` if mechanical plausibility, fit, strength, manufacturability, or material claims are made.
- Use `cad-solidworks-native-preflight` if native SolidWorks files or SolidWorks rebuild/open/save/export claims are made.
- Use `cad-toolchain-preflight` if a tool path was not locally verified.
- Use `cad-visual-layout` if a drawing sheet, PDF, screenshot, or plotted output needs formal visual review.
- Use `cad-design-richness` if the design may be too simple, blocky, sparse, or lacking real mechanical detail.
- Use `cad-reference-match` if any reference similarity claim is needed.
- Use `cad-reference-acceptance` if a reference similarity claim is ready to be accepted or rejected.
- Use `cad-region-compare` if local reference/output PDF or image regions can be compared.
