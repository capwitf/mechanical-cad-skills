---
name: cad-engineering-sanity
description: Use when CAD, SolidWorks, FreeCAD, STEP, DXF, DWG, STL, mechanical parts, assemblies, fixtures, brackets, mechanisms, enclosures, drawings, or original designs need engineering plausibility checks for loads, interfaces, wall thickness, hole edge distance, clearances, standard parts, materials, interference, or unverified strength claims.
---

# CAD Engineering Sanity

## Overview

Engineering-looking geometry is not automatically engineering-sound geometry. Use this gate to separate directly checked facts from assumptions before claiming a CAD design is structurally or mechanically reasonable.

## Core Rule

Do not claim strength, stiffness, load capacity, fatigue life, sealing, precision fit, production readiness, or safety unless the required evidence was checked. If loads, materials, tolerances, or standards are missing, mark the claim as Unverified or Inferred, not Verified.

## Sanity Table

Before accepting an original or modified mechanical design, fill the applicable rows:

| Check | Evidence to capture |
|---|---|
| Function | What motion, support, enclosure, transmission, clamping, alignment, or protection the part provides |
| Load path | Where force, torque, pressure, vibration, or weight enters and exits the design |
| Interfaces | Mating faces, axes, shafts, bearings, fasteners, pins, slots, cable/pipe ports, keep-out zones |
| Material | Actual or assumed material and why it fits the load, process, environment, and finish |
| Manufacturing | Machined, printed, sheet metal, welded, cast, laser cut, or purchased; note process limits |
| Wall/section thickness | Minimum section thickness and whether it fits the material/process |
| Hole edge distance | Critical hole-to-edge and hole-to-hole distances for fasteners or pins |
| Clearances | Shaft, bearing, fastener, assembly, tool, service, and motion clearances |
| Fits/tolerances | Any press, slip, clearance, threaded, bearing, or datum-controlled fit |
| Standard features | Fastener sizes, threaded holes, counterbores, chamfers, fillets, keyways, bearings, pins, stock sizes |
| Interference | Assembly and motion interference checked or explicitly unverified |
| Failure modes | Likely bending, shear, pull-out, buckling, wear, heat, vibration, cracking, leakage, or loosening risks |

## Minimum Quantitative Boundary

For professional CAD, record at least one numeric boundary for every relevant category:

- envelope size or maximum travel,
- critical thickness,
- critical fastener or shaft diameter,
- hole pattern diameter or spacing,
- clearance or tolerance target,
- estimated load/torque/weight, or state `unknown - blocks strength claim`,
- material or stock thickness,
- minimum fillet/chamfer where stress or manufacturing matters.

If a category cannot be quantified from the request, do not invent precision. Record the assumption and mark related conclusions Inferred or Unverified.

## Claim Discipline

Use these labels:

| Label | Allowed when |
|---|---|
| Verified | Measured, calculated, opened, rendered, or directly inspected from the final source/deliverable |
| Inferred | Plausible from geometry or common practice, but not directly calculated or inspected |
| Unverified | Missing load, material, standard, tolerance, local CAD tool, or inspection evidence |

Forbidden overclaims:

- "strength is sufficient" without loads, material, section check, or FEA/test evidence,
- "manufacturable" without process constraints and minimum feature sizes,
- "fits" without mating dimensions or tolerance/clearance evidence,
- "no interference" without assembly or motion check,
- "professional" when only decorative chamfers or extra holes were added.

## Original Design Gate

For no-reference design, require:

1. Function zones named.
2. Load path stated.
3. Interfaces dimensioned or explicitly assumed.
4. Standard mechanical features chosen for a reason.
5. Clearances and critical hole positions checked.
6. Failure modes listed.
7. Claims classified as Verified, Inferred, or Unverified.

If any item is missing, the engineering sanity result is fail or partial. Do not let visual richness compensate for missing engineering logic.

## Handoff

Use with:

- `cad-original-design` before modeling no-reference parts or assemblies.
- `cad-design-richness` after engineering logic is present, to avoid shallow complexity.
- `cad-visual-layout` when a formal drawing/PDF must communicate the checked design.
- `cad-final-verification` before delivery.
- `cad-toolchain-preflight` if local CAD tooling is needed for measurement, interference, or export checks.

## Common Mistakes

- Adding ribs, holes, or fillets for appearance without a load path.
- Using "standard" fasteners without size, clearance, thread, or counterbore notes.
- Calling a part manufacturable because it exports to STEP.
- Omitting service access, tool access, or assembly sequence.
- Treating a render as proof of fit.
- Hiding missing loads or materials inside a confident final summary.
