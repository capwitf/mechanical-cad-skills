---
name: cad-external-skill-intake
description: Use when Codex is asked to inspect, absorb, compare, install, trust, or localize external GitHub, skills registry, MCP, SolidWorks, FreeCAD, text-to-cad, CadQuery, build123d, STEP, DXF, DWG, or CAD automation skills before using them in the local CAD skill cluster.
---

# CAD External Skill Intake

## Overview

External CAD skills are evidence sources, not trusted execution paths. Extract reusable workflow and checklist ideas only after a read-only maturity and safety review.

## Read-Only Boundary

Default to review-only intake:

- No Install: do not globally install an external skill, plugin, MCP server, package, or binary unless the user explicitly authorizes it for the current task.
- No External Scripts: do not execute external repository scripts, installers, setup files, postinstall hooks, macros, CAD automation, or downloaded binaries during intake.
- Read only documentation first: README, SKILL.md, manifest files, examples, issue summaries, release notes, and source snippets needed to understand workflow.
- Keep all absorbed content local to the project skill cluster unless the user explicitly asks for global installation.
- Treat external licenses as constraints. If license is absent or incompatible, absorb only high-level workflow ideas, not code or substantial text.

If the user asks to install or run an external tool, first finish this intake, then use `cad-toolchain-preflight` for local proof.

## Intake Workflow

1. Identify the external candidate: repo, registry package, MCP server, skill name, tool type, and intended local use.
2. Gather maturity evidence: stars, forks, install count, open issues, latest commit or release, archived status, alpha/experimental warnings, supported OS/CAD versions, license, and required dependencies.
3. Classify risk:

| Rating | Meaning |
|---|---|
| Green | Current, documented, licensed, locally relevant, and can be preflighted without unsafe setup |
| Yellow | Promising but has stale docs, unclear native CAD support, experimental wording, missing evidence, or manual verification needs |
| Red | Archived, unlicensed or incompatible, install-only docs, opaque binaries, unsafe scripts, no examples, broken dependencies, or no path to inspect final CAD output |

4. Extract workflows, not trust:
   - parametric source discipline,
   - named dimensions and design intent,
   - neutral export checks for STEP/DXF/PDF/STL,
   - open/render/screenshot evidence,
   - SolidWorks COM/API launch and rebuild preflight,
   - FreeCAD document, recompute, export, and nonblank screenshot checks,
   - final report categories: Verified, Inferred, Unverified.
5. Reject unsafe material: installers, global registration, shell setup, postinstall hooks, tokens, credentials, opaque binaries, and code whose license or provenance is unclear.
6. Decide absorption target: `cad-sw-delivery`, `cad-toolchain-preflight`, `cad-original-design`, `cad-reference-match`, `cad-visual-layout`, `cad-design-richness`, or `cad-final-verification`.
7. Record an Absorption Ledger before editing any local skill.

## Workflow Extraction Rules

Absorb only reusable process patterns that can be stated as local checks, routing rules, or validation hooks.

## Absorption Ledger

Keep a short ledger for each candidate:

| Field | Required content |
|---|---|
| Candidate | Repo/package/skill URL or name |
| Intended use | CAD generation, SolidWorks automation, FreeCAD control, export verification, drawing layout, or reference matching |
| Maturity Evidence | stars/forks/issues/install count/latest commit/license/archived/alpha notes, with dates when available |
| Risk Rating | Green, Yellow, or Red, with reason |
| Safe Ideas | Workflow/checklist concepts that can be localized |
| Rejected Parts | Installers, scripts, binaries, code, or claims not absorbed |
| Local Target | Which local skill should receive the safe idea |
| Verification Hook | Validator term, preflight proof, or final acceptance check that will catch regressions |

If current metadata cannot be verified because rate limits or network errors block lookup, mark that evidence as Unverified and do not upgrade a candidate to Green.

## CAD-Specific Intake Signals

Prefer candidates that strengthen professional CAD output:

- Regenerable parametric source with named dimensions.
- Explicit support for STEP, DXF, PDF, STL, or native SolidWorks/FreeCAD workflows.
- Examples that include sections, dimensions, datums, tolerances, materials, BOM, line weights, or drawing sheets.
- Local verification steps that open or render final deliverables, not only previews.
- Clear separation between source-of-truth model and exported delivery files.
- Evidence for Windows/SolidWorks COM automation when native SolidWorks files are requested.

Downgrade candidates that only produce decorative images, toy geometry, one-shot prompts, or uninspectable meshes.

## Handoff

After intake:

- Use `cad-toolchain-preflight` before relying on any selected external tool locally.
- Use `cad-sw-delivery` to route safe workflow improvements into the cluster.
- Use `cad-final-verification` to prove final files, not external claims.
- Report which evidence was Verified, Inferred, or Unverified.

## Common Mistakes

- Treating GitHub stars, registry installs, or a polished README as proof that the tool can make professional CAD locally.
- Running install scripts during review.
- Copying external code into local skills when a checklist would be enough.
- Absorbing broad claims without a validator or preflight hook.
- Calling a candidate Green when metadata was blocked by rate limits or not checked.
- Letting external tooling replace engineering judgment about dimensions, loads, manufacturability, layout, or design richness.
