---
name: cad-original-design
description: Use when a CAD, SolidWorks, FreeCAD, STEP, DXF, DWG, STL, part, assembly, mechanism, fixture, bracket, enclosure, tool, or mechanical drawing must be designed from requirements without a reference drawing, screenshot, PDF, scan, or existing CAD file to copy.
---

# CAD Original Design

## Core Rule

When there is no reference drawing, do not use reference-matching criteria. Design from function, constraints, interfaces, loads, manufacturability, and acceptance tests.

## Design Brief

Before modeling, create a concise design brief:

| Field | Capture |
|---|---|
| Function | What the part, assembly, or mechanism must do |
| Interfaces | Mounting points, mating parts, shafts, bearings, fasteners, ports, clearance zones |
| Loads | Force, torque, pressure, vibration, weight, thermal exposure, safety factor if known |
| Envelope | Maximum size, keep-out areas, travel, orientation, installation access |
| Material | Required or assumed material, density, strength, corrosion, finish |
| Manufacturing | 3D print, machining, sheet metal, laser cutting, casting, welding, off-the-shelf parts |
| Adjustability | Slots, shims, tolerances, fit classes, alignment features |
| Complexity target | Simple, medium, or rich; expected information density and feature families |
| Professional elements | Datums, tolerances, roughness, technical notes, sections, local details, title block |
| Deliverables | STEP, DXF, DWG, PDF drawing, STL, native SolidWorks, source script |
| Acceptance | What proves the design satisfies the brief |

Use `cad-requirements-lock` for missing blocking facts. If the user wants assumptions, record them as assumptions.

## Concept Pass

Generate at least one coherent concept before CAD:

- name the design type,
- explain the load path,
- explain how it mounts or mates,
- identify critical dimensions and degrees of freedom,
- identify likely failure modes,
- define function zones and standard mechanical features,
- run `cad-engineering-sanity` for load path, interfaces, wall thickness, hole edge distance, clearances, fits, material, and unverified strength claims,
- define the minimum professional drawing elements,
- choose a manufacturable feature set.

For nontrivial parts, compare two concepts briefly and pick one. Do not over-design beyond the task.

## Modeling Rules

- Build parametric geometry from named dimensions when possible.
- Keep interfaces and datums explicit.
- Prefer standard fasteners, hole sizes, clearances, radii, and stock thicknesses.
- Add fillets/chamfers for function or manufacturing, not decoration.
- Preserve design intent in the source script/model so dimensions can change.
- For drawings, dimension functional features and interfaces first.
- Use `cad-design-richness` to prevent under-designed blocky geometry.
- Use `cad-visual-layout` to prevent sparse or informal plotted drawings.

## Original Design Checks

Before final reporting, check:

- function matches the design brief,
- interfaces are present and dimensioned,
- load path is plausible,
- engineering sanity result is pass, partial, or fail with Verified/Inferred/Unverified claims labeled,
- wall thickness, fillets, hole edge distances, and clearances are reasonable,
- manufacturing method is plausible,
- complexity target is met,
- required professional drawing elements are present,
- visual layout target is met when a drawing/PDF is delivered,
- deliverables are generated from the current source,
- unverified engineering claims are labeled as unverified.

Use `cad-design-richness` before accepting the mechanical concept. Use `cad-visual-layout` before accepting a formal drawing sheet. Use `cad-final-verification` for final file checks. Use `cad-toolchain-preflight` before relying on CAD automation or external tools.
Use `cad-engineering-sanity` before claiming fit, strength, load capacity, manufacturability, or mechanical plausibility.

## When Not To Use

- If a reference drawing/image/PDF/DWG must be copied, use `cad-reference-match`.
- If the task is only checking final files, use `cad-final-verification`.
- If the toolchain itself is unknown, use `cad-toolchain-preflight`.

## Reporting

Report:

- design brief,
- chosen concept and reason,
- key assumptions,
- generated files,
- verified design checks,
- engineering sanity result,
- visual layout result,
- design richness result,
- unverified engineering risks.
