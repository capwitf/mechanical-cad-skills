---
name: cad-requirements-lock
description: Use when a CAD, SolidWorks, FreeCAD, mechanical drawing, part model, assembly, STEP, DXF, DWG, STL, PDF drawing, or engineering deliverable is requested before geometry, dimensions, standards, constraints, or acceptance criteria are clear.
---

# CAD Requirements Lock

## Core Rule

Do not start modeling or drawing until the minimum acceptance target is explicit. A CAD deliverable can be visually polished and still be wrong if units, constraints, dimensions, or engineering standards were guessed.

## Lock Before Work

Create a short requirements lock with these fields:

| Field | What to capture |
|---|---|
| Deliverables | Native CAD, STEP, DXF, DWG, PDF, STL, 3MF, GLB, screenshots, source scripts |
| Purpose | Manufacturing, homework, reference replica, fit check, assembly, animation, concept |
| Units and scale | mm/inch, drawing scale, sheet size, projection method |
| Geometry facts | Overall size, hole count, diameters, centers, axes, thread specs, fits, chamfers, fillets |
| Engineering sanity | Load path, material, manufacturing process, critical wall thickness, hole edge distance, clearances, standard parts, and which strength claims are allowed |
| Standards | Layers, line weights, title block, BOM, tolerances, materials, surface finish |
| Visual target | Sheet density, view hierarchy, title block level, line hierarchy, readability target |
| Complexity target | Simple, medium, or rich; expected feature families and professional drawing elements |
| Source material | Text spec, reference image, PDF, DWG, model, part photos, user sketch |
| Unknowns | Missing facts and whether they block correctness |
| Acceptance | What final checks must pass before reporting ready |

## Unknowns Policy

Classify unknowns:

- **Blocking**: cannot produce a correct engineering result without the answer.
- **Assumable**: can choose a conservative default, but report it.
- **Decorative**: affects appearance but not engineering correctness.

Ask only for blocking unknowns that cannot be inferred from local files or references. If the user asks to proceed with assumptions, write the assumptions into the lock and mark them as inferred.

If visual quality or design richness is subjective, set a provisional target rather than leaving it blank. Use `cad-visual-layout` and `cad-design-richness` later to check the target.
If engineering strength, fit, clearance, or manufacturability is uncertain, set a provisional engineering sanity target and mark missing loads/materials as blocking or unverified.

## Handoff

After the lock is complete:

- Use `cad-toolchain-preflight` before relying on external CAD tools, SolidWorks automation, FreeCAD, MCP servers, or installed skills.
- Use `cad-engineering-sanity` when the task includes mechanical plausibility, fit, strength, manufacturability, material, load path, wall thickness, hole edge distance, or clearance claims.
- Use `cad-design-richness` when the work must look like a realistic mechanical design.
- Use `cad-visual-layout` when a plotted drawing or PDF must look formal and readable.
- Use `cad-reference-match` when the result must resemble a reference drawing or screenshot.
- Use `cad-final-verification` before claiming the output is ready.

## Common Mistakes

- Starting with a pretty preview before units and dimensions are known.
- Treating "make it like this" as enough when the reference has unmeasured local features.
- Ignoring title block, BOM, projection, tolerances, and material because geometry was the focus.
- Asking too many questions when only one or two blocking facts are actually needed.

## Reporting

Report the lock briefly:

- locked facts,
- assumptions,
- blocking unknowns,
- planned deliverables,
- acceptance checks.
