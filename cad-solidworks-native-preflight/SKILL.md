---
name: cad-solidworks-native-preflight
description: Use when CAD work involves native SolidWorks files, SLDPRT, SLDASM, SLDDRW, SolidWorks COM/API automation, pywin32, drawing export, STEP/PDF/DXF export from SolidWorks, rebuild/open checks, feature tree evidence, or claims that SolidWorks files are ready, openable, rebuilt, saved, or production suitable.
---

# CAD SolidWorks Native Preflight

## Overview

Native SolidWorks quality cannot be proven from a STEP, PDF, screenshot, or script alone. Use this gate before claiming `.sldprt`, `.sldasm`, or `.slddrw` files are ready.

## Core Rule

Do not claim native SolidWorks files are correct, openable, rebuilt, editable, or ready unless SolidWorks itself was used to open or create the final native files and the evidence was recorded.

If SolidWorks cannot launch, license is unavailable, COM/API access fails, or native files cannot be reopened and rebuilt, mark native SolidWorks quality as Unverified or fail. Neutral exports may still be delivered, but they do not prove native file quality.

## Native Preflight Checklist

Record these items before native delivery:

| Check | Evidence |
|---|---|
| Installation | SolidWorks installed on this Windows machine |
| License/session | SolidWorks launches without license or activation blocker |
| Version | SolidWorks version or revision captured |
| COM/API | ProgID such as `SldWorks.Application` or selected MCP/API bridge works |
| pywin32/bridge | Python automation dependency available when automation is used |
| Smoke part | Tiny part can be created or opened, rebuilt, saved, closed, and reopened |
| Final open | Final `.sldprt`, `.sldasm`, or `.slddrw` opens from the reported path |
| Rebuild | Rebuild returns no blocking errors; warnings are recorded |
| Feature tree | Feature/body/component/drawing view tree is nonempty and relevant |
| Save/export | Native save succeeds; requested STEP/PDF/DXF exports are fresh |
| Screenshot/log | Screenshot, rebuild log, export log, or evidence ledger entry exists |

## Native Evidence Labels

- **Pass**: final native file opened in SolidWorks, rebuilt, saved or exported, and evidence was recorded.
- **Partial**: SolidWorks opened or exported something, but native reopen/rebuild, drawing, assembly, or export evidence is incomplete.
- **Fail**: SolidWorks could not launch, open, rebuild, save, export, or produced blank/stale/broken output.
- **Unverified**: SolidWorks was not available or the check was not run.

Do not convert Partial or Unverified to Pass because a STEP/PDF exists.

## Automation Boundary

Before running SolidWorks automation:

1. Use `cad-external-skill-intake` for external SolidWorks automation skills, MCP servers, or repos.
2. Use `cad-toolchain-preflight` for the general tool path.
3. Run this native preflight for SolidWorks-specific evidence.
4. Record results with `cad-evidence-ledger`.

Do not run unknown macros, downloaded installers, or external automation scripts without explicit user approval. Prefer small local smoke tests before touching the real deliverable.

## Drawing-Specific Checks

For `.slddrw` or SolidWorks-generated PDF/DXF:

- drawing opens in SolidWorks,
- referenced model resolves,
- views are not empty,
- sheet format/title block is present,
- dimensions and annotations are visible,
- rebuild/update views before export,
- exported PDF/DXF is fresh and nonblank,
- `cad-visual-layout` checks plotted readability.

## Assembly-Specific Checks

For `.sldasm`:

- components resolve from final paths,
- mates are not suppressed or broken without being reported,
- assembly rebuilds,
- approximate interference or clearance checks are run when the task requires fit,
- BOM/exploded/drawing references are updated when delivered.

## Handoff

Use with:

- `cad-sw-delivery` whenever native SolidWorks deliverables are requested.
- `cad-toolchain-preflight` before relying on SolidWorks automation.
- `cad-evidence-ledger` for paths, hashes, timestamps, logs, screenshots, and claim categories.
- `cad-final-verification` before final reporting.

## Common Mistakes

- Claiming `.sldprt` quality because STEP export succeeded.
- Reporting native files ready without reopening them in SolidWorks.
- Ignoring rebuild warnings or suppressed features.
- Delivering a drawing whose referenced model path is broken.
- Treating COM launch as proof that the final file opens.
- Forgetting that PDF/DXF exports do not prove `.slddrw` health.
