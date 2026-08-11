---
name: cad-design-richness
description: Use when a CAD, SolidWorks, FreeCAD, STEP, DXF, DWG, PDF drawing, mechanical part, assembly, mechanism, fixture, bracket, enclosure, or self-designed drawing must be checked for realistic mechanical complexity, professional detail, functional features, manufacturing plausibility, or not looking like simple geometric blocks.
---

# CAD Design Richness

## Core Rule

Do not treat a simple stack of boxes, circles, and holes as a finished mechanical design when the task expects a real engineered object. Require functional structure, standard mechanical features, and drawing information density appropriate to the target.
Design richness cannot compensate for missing engineering sanity. Use `cad-engineering-sanity` when load path, fit, wall thickness, hole edge distance, clearances, material, manufacturability, or strength claims matter.

## Richness Gate

Check whether the design includes relevant real mechanical features:

| Category | Examples |
|---|---|
| Function zones | support, mounting, transmission, sealing, positioning, adjustment, limit, access, service |
| Interfaces | bolt patterns, locating pins, bearing seats, shaft bores, keyways, slots, bosses, flanges, ports |
| Standard features | counterbores, countersinks, threaded holes, tapped bosses, ribs, gussets, chamfers, fillets, grooves |
| Manufacturing details | wall thickness, draft, bend relief, tool access, stock thickness, weld prep, machining allowances |
| Assembly detail | fasteners, washers, clearance, exploded or section logic, mating references, part numbers |
| Drawing detail | datum symbols, tolerances, fits, surface roughness, material, heat treatment, technical notes |
| Explanation | design intent, load path, why features exist, what was simplified |

The exact features depend on the object. Do not add fake complexity that conflicts with function, manufacturing, or the requested scope.

## Complexity Target

Set a target before modeling:

- **Simple**: clean educational part, few features, still dimensioned and readable.
- **Medium**: realistic single part or small assembly with mounting, locating, and manufacturing details.
- **Rich**: professional-looking engineering design with multiple feature families, sections/details, datums, tolerances, notes, and local detail views.

If the user does not specify, choose medium for self-designed mechanical work unless speed or simplicity is explicitly requested.

## Richness Scorecard

Score the design from 0 to 20. Use 0 for absent, 1 for weak, 2 for solid:

| Item | Check |
|---|---|
| Function zones | Distinct support, mounting, positioning, transmission, adjustment, service, or enclosure zones exist |
| Interfaces | Mating faces, shafts, bearings, pins, fasteners, slots, flanges, or ports are explicit |
| Standard feature families | Counterbores, threads, ribs, gussets, fillets, chamfers, grooves, keyways, bosses, or bearing seats serve a purpose |
| Manufacturing detail | Thickness, tool access, stock/process limits, draft/bend/weld/machining details are considered |
| Assembly/service detail | Fastener access, clearance, install order, maintenance, or component references are present |
| Drawing professionalism | Datums, tolerances, fits, roughness, material, notes, sections, details, or BOM appear when needed |
| Engineering rationale | Load path, simplifications, and failure modes are explained or marked unverified |
| Information density | Sheet/model contains enough functional dimensions and detail for the target |
| Non-decorative complexity | Added features have mechanical, manufacturing, assembly, or drawing purpose |
| Scope fit | Complexity matches the requested target without overbuilding or underbuilding |

Minimum pass:

- Simple target: score >= 10/20 and no critical fail.
- Medium target: score >= 14/20, at least 3 real feature families, and no critical fail.
- Rich target: score >= 17/20, at least 5 real feature families, sections/details or equivalent local explanations, and no critical fail.

Critical fail conditions:

- only primitive blocks/plates/holes when realistic design was requested,
- features are decorative or conflict with function/manufacturing,
- no interfaces or mounting logic,
- no load path or engineering rationale for a self-designed mechanical part,
- formal drawing lacks material, notes, dimensions, or professional elements expected by the target.

## Review Method

1. Read the design brief or requirements.
2. List expected functional zones and standard features.
3. Compare expected features to the model/drawing.
4. Mark missing detail as functional, manufacturing, assembly, or annotation.
5. Add only features that serve a purpose.
6. Re-check with `cad-engineering-sanity`, `cad-visual-layout`, and `cad-final-verification`.

## Original Design Hook

For no-reference design, `cad-original-design` must define:

- complexity target,
- function zones,
- structural feature checklist,
- manufacturing method,
- professional drawing elements,
- minimum drawing information density.

For no-reference design, `cad-engineering-sanity` must classify strength, fit, clearance, material, and manufacturability claims as Verified, Inferred, or Unverified before the richness result is accepted.

## Common Mistakes

- Adding dimensions to a weak design and calling it professional.
- Adding decorative ribs, holes, or bosses with no function.
- Forgetting bearing seats, locating features, fastener clearances, or service access.
- Omitting datum, tolerance, surface roughness, material, and notes on a formal drawing.
- Making everything complex when the task only needs a simple educational part.

## Reporting

Report:

- design richness pass/fail,
- richness score, target, and critical fail status,
- complexity target,
- functional zones present,
- missing or intentionally omitted mechanical details,
- unverified strength, fit, or manufacturing risks.
