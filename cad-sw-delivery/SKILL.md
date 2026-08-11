---
name: cad-sw-delivery
description: Use when Codex is asked to create, repair, automate, verify, or deliver CAD/SolidWorks/FreeCAD mechanical models or drawings, including STEP, DXF, DWG, STL, 3MF, GLB, SLDPRT, SLDASM, SLDDRW, engineering drawings, assemblies, or when the user complains a CAD result looked wrong despite being reported as good.
---

# CAD/SW Delivery

## Core Rule

Deliver CAD work as an engineering artifact, not as a pretty preview. Do not claim a CAD/SW result is good, correct, matching, or ready unless the final deliverable passed explicit acceptance checks.

Use this skill as the hub for the local CAD skill cluster:

- `cad-requirements-lock` before geometry or standards are unclear.
- `cad-original-design` when no reference exists and the part, assembly, fixture, enclosure, mechanism, or drawing must be designed from requirements.
- `cad-engineering-sanity` when mechanical plausibility, load path, interfaces, clearances, wall thickness, hole edge distance, fits, standard parts, material, or strength claims need checking.
- `cad-design-richness` when a design must look like a real mechanical object rather than simple geometric blocks.
- `cad-visual-layout` when a drawing sheet, PDF, screenshot, or plotted output must look organized, readable, and formal.
- `cad-external-skill-intake` before absorbing, localizing, installing, or trusting external GitHub/registry CAD skills, MCP servers, or automation workflows.
- `cad-toolchain-preflight` before relying on external CAD tools, MCP servers, SolidWorks automation, FreeCAD, or text-to-cad.
- `cad-illustration-vectorization` when a portrait, poster, logo, artwork, photo, or freehand image must become editable SVG/DXF/DWG line art. This is not a mechanical reference-match route.
- `cad-solidworks-native-preflight` when native `.sldprt`, `.sldasm`, `.slddrw`, SolidWorks rebuild/open/save/export, or COM/API automation quality is claimed.
- `cad-reference-match` when a result must imitate or stay visually close to a reference drawing, screenshot, PDF, or DWG/DXF output.
- `cad-region-compare` when local PDF/image regions from a reference and output need crop/diff comparison evidence.
- `cad-artifact-inspection` when STEP/STL/DXF/DWG/PDF or other neutral exports need read-only format/content inspection.
- `cad-evidence-ledger` when final files, source provenance, hashes, timestamps, checks, screenshots, logs, or Verified/Inferred/Unverified claims need a manifest.
- `cad-final-verification` before claiming a deliverable is ready.

If project-local `jixie-fuke` is available, treat it as the deeper reference-replication rule set behind `cad-reference-match`.

## First Lock

Before creating or editing CAD, use `cad-requirements-lock` to lock the minimum viable acceptance target:

- Intended output: STEP, DXF, DWG, PDF, STL, 3MF, GLB, SLDPRT, SLDASM, SLDDRW, images, or source scripts.
- CAD intent: manufacturable model, engineering drawing, visual replica, classroom assignment, assembly, animation, or inspection artifact.
- Required standards: units, sheet size, projection, scale, layers, title block, BOM, tolerances, materials, line weights, and export format.
- Hard geometry facts: dimensions, constraints, axes, hole counts, thread specs, fits, datum features, mating parts, and forbidden guesses.
- Unknowns: list them plainly and mark whether they block correctness or can be approximated.

## Loop Guard

If the user asks for a loop run, loop engineering, or the Chinese equivalent of "run loop":

1. Read project-local `LOOP.md` and `STATE.md` first.
2. If `LOOP.md` or `STATE.md` is missing, ask whether to initialize loop-engineering for this project.
3. Default mode is `L1/report-only`: inspect, summarize, and update state/logs only.
4. Use `L2/local-skill-edit` or `L3/source-edit` only when the current user message explicitly authorizes that scope.
5. Do not modify CAD drawings, generated deliverables, business source files, or CAD/model source unless the active mode allows it.
6. Prefer project-local state. Never use one global `STATE.md` across unrelated projects.
7. After finishing any local CAD skill stage, run at least three loop rounds before calling the stage clean.
8. Loop 1 records validator failures or missing evidence; Loop 2 fixes or classifies every issue and reruns validators; Loop 3 reruns validators and residue scans from a clean state.
9. If any new issue appears in Loop 3, keep looping until no new issue remains.
10. After each loop run, summarize what changed, what was observed, open risks, and the next smallest action.

## Tool Choice

Prefer the smallest toolchain that produces inspectable engineering files:

| Situation | Preferred path | Acceptance signal |
|---|---|---|
| Parametric mechanical part or simple assembly, no native SW required | text-to-cad/build123d/CadQuery style script in a STEP-first workflow plus preview | Script reruns, STEP opens, dimensions/features match locked requirements, and a snapshot is reviewed |
| No reference, original design required | Use `cad-original-design`, `cad-engineering-sanity`, and `cad-design-richness` before modeling | Design brief, concept rationale, interfaces, load path, clearances, manufacturability, complexity target, and feature checklist are explicit |
| 2D engineering drawing or laser/CNC profile | script or CAD export to DXF/DWG/PDF | `cad-artifact-inspection` reports entities/layers/text or PDF pages, then dimensions and local geometry are checked |
| Formal plotted drawing required | Use `cad-visual-layout` before final reporting | View hierarchy, title block, text, line weights, spacing, dimensions, and thumbnail impression pass |
| Native SolidWorks files required | SolidWorks COM/API automation after `cad-toolchain-preflight` and `cad-solidworks-native-preflight` | SW launches, final native files reopen/rebuild, feature tree or drawing views exist, exports are fresh |
| FreeCAD acceptable | FreeCAD Python/MCP workflow | Model tree exists, export opens, screenshot/render is nonblank |
| Reference matching required | Use `cad-reference-match`, `cad-region-compare`, and project-local `jixie-fuke` when available | Local comparison regions and crop/diff evidence pass, not just whole-sheet preview |
| Portrait, logo, poster, artwork, or photo needs editable 2D linework | Use `cad-illustration-vectorization`; use SVG/DXF/DWG native curve entities | Reopened final output contains editable vectors, no unintended raster underlay, and visual review checks major contours/features rather than engineering dimensions |

Before installing or trusting external skills/MCP servers, use `cad-external-skill-intake` for read-only review, then `cad-toolchain-preflight` for local proof. Useful searches include `npx skills find cad`, `npx skills find solidworks`, and GitHub metadata checks. Treat install counts and stars as triage signals, not proof of correctness.

See `references/tooling-options.md` for current candidate tools and caution levels.

## Acceptance Ledger

Maintain a short ledger during the task:

1. Requirements locked.
2. Source of truth named: script, CAD model, SolidWorks document, FreeCAD document, or existing drawing.
3. Generated outputs listed with paths and timestamps.
4. Artifact inspection run for neutral exports where tooling allows.
5. Automated checks run.
6. Engineering checks run.
7. Engineering sanity result stated when mechanical plausibility or strength/fit/manufacturing claims matter.
8. Evidence ledger manifest path or reason it was not needed.
9. External tool or skill intake stated when external workflow/tooling influenced the result.
10. SolidWorks native preflight stated when native SW files are requested.
11. Visual layout result stated.
12. Design richness result stated.
13. Remaining risks or missing facts stated.

The final answer must distinguish:

- **Verified**: checked directly from the final file or rebuilt source.
- **Inferred**: likely true from script/model structure but not directly inspected.
- **Unverified**: not checked or blocked by missing tools/information.

## Verification Loop

Repeat until the acceptance ledger is clean or a blocker is explicit:

1. Generate or update the source of truth.
2. Rebuild/export all requested formats.
3. Check files exist, are fresh, non-empty, and open/render where tooling allows.
4. Run `cad-artifact-inspection` for STEP/STL/DXF/DWG/PDF neutral exports when local parsers can inspect them.
5. Check model/drawing content: feature counts, dimensions, axes, centers, view layout, layers, sections, hatches, annotations, title block, and BOM as applicable.
6. For original no-reference design, run design-brief and concept checks via `cad-original-design`.
7. Run `cad-engineering-sanity` before accepting no-reference mechanical designs or any strength, fit, clearance, manufacturability, or load-path claim.
8. Run `cad-design-richness` when the task expects professional mechanical complexity or self-designed structure.
9. Run `cad-visual-layout` for any formal drawing sheet, PDF, screenshot, or plotted output.
10. Run `cad-external-skill-intake` before absorbing or trusting any external CAD skill, MCP server, or automation workflow.
11. Run `cad-solidworks-native-preflight` before claiming native SolidWorks files are openable, rebuilt, saved, exported, or ready.
12. Run `cad-evidence-ledger` when reporting final file readiness, external tool provenance, or any nontrivial Verified/Inferred/Unverified claim.
13. For visual/reference work, run local crop/region comparison via `cad-reference-match` and `cad-region-compare` when rendered PDF/image regions are available.
14. Fix the source of truth, not only screenshots or stale delivery copies.
15. Re-run checks from the final deliverable.

Do not stop just because an export succeeded. Export success only proves that a file was produced.

## SolidWorks Preflight

For native SolidWorks work on Windows:

- Confirm SolidWorks is installed, licensed, and can launch.
- Confirm the automation bridge works (`pywin32`, COM access, or the selected MCP/API server).
- Open or create a small test part before touching the real task.
- Rebuild documents before export.
- Export neutral formats such as STEP/PDF/DXF alongside native files when possible.
- If COM/MCP automation is experimental, report it as experimental and keep a manual fallback.

Never claim `.sldprt`, `.sldasm`, or `.slddrw` quality from a neutral export alone.

## Common Mistakes

Avoid these failure modes:

- Saying "looks good" after only checking a full-page screenshot.
- Treating entity count, file size, or successful export as engineering correctness.
- Delivering simple geometric blocks when a real mechanical design was expected.
- Treating a portrait, poster, logo, or freehand image as a mechanical drawing and applying title blocks, dimensions, hatches, STEP-first generation, or engineering acceptance grids.
- Delivering a sparse, flat, tiny, or poorly aligned drawing sheet.
- Installing a random CAD/SW MCP server without checking maturity and local prerequisites.
- Absorbing external CAD skill claims without read-only intake and a local preflight.
- Fixing a PDF/image preview while the STEP/DWG/SolidWorks source remains wrong.
- Mixing stale files from earlier attempts into the final delivery folder.
- Ignoring user complaints because the previous script ran without errors.

## Reporting

When finishing, report:

- Toolchain used and why.
- Source of truth edited or generated.
- Final file paths.
- Evidence ledger manifest if produced.
- Artifact inspection report if produced.
- Automated checks passed.
- Engineering or visual checks passed.
- Engineering sanity: pass/fail/partial.
- Visual layout: pass/fail.
- Design richness: pass/fail.
- Anything not verified and the next smallest action.
