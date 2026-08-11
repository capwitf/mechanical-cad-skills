---
name: cad-skill-forward-test
description: Use when validating, stress-testing, loop-improving, or reviewing the local CAD/SolidWorks skill cluster, especially before trusting it to produce professional CAD drawings, original mechanical designs, reference-matched drawings, SolidWorks native files, evidence ledgers, or final pass/fail reports.
---

# CAD Skill Forward Test

## Overview

Forward-test the CAD skill cluster like process code. The goal is to catch overconfidence, skipped evidence, weak engineering reasoning, and subjective "looks good" claims before a real user delivery depends on the skills.

## Core Rule

Use fresh-agent or isolated scenario testing when possible. Pass the skill path and a realistic user-style task, not the expected answer. Review whether the agent follows the cluster without being told exactly what to say.

Do not edit real CAD deliverables during L1/L2 loop runs. Use synthetic prompts, temporary outputs, or report-only review unless the user explicitly authorizes `L3/source-edit`.

Use `references/scenarios.json` as the reusable scenario pack. Use `scripts/list_forward_scenarios.py` to list scenarios or emit one test prompt.

```powershell
python .\.codex\skills\cad-skill-forward-test\scripts\list_forward_scenarios.py --list
python .\.codex\skills\cad-skill-forward-test\scripts\list_forward_scenarios.py --id no-reference-motor-bracket
```

## Forward-Test Scenarios

Run at least one scenario from each relevant class:

| Scenario | Pressure | Expected behavior |
|---|---|---|
| Original bracket without reference | User asks for a professional self-designed bracket with few dimensions and says "make it look good" | Uses `cad-requirements-lock`, `cad-original-design`, `cad-engineering-sanity`, `cad-design-richness`, `cad-visual-layout`, `cad-evidence-ledger`, and refuses strength overclaims |
| Reference drawing complaint | User provides a screenshot and says the previous drawing "looks wrong" | Uses `cad-reference-match` and `jixie-fuke`, splits local regions, compares crops/zoomed areas, and does not rely on whole-page similarity |
| Native SolidWorks claim | User requests `.sldprt` and `.slddrw` and asks for ready-to-submit files | Uses `cad-solidworks-native-preflight`, marks native quality Unverified if SolidWorks cannot launch/rebuild/reopen, and does not treat STEP/PDF as native proof |
| External GitHub skill request | User asks to absorb a CAD GitHub skill | Uses `cad-external-skill-intake`, stays read-only, records maturity evidence, and does not install or execute external scripts |
| Portrait or poster to editable CAD | User supplies a photo or artwork and asks for editable DWG/DXF line art | Uses `cad-illustration-vectorization`, keeps the target 2D/vector, rejects STEP-first mechanical generation and engineering title blocks, then verifies editable entities and local visual regions |
| Final delivery report | User asks "is it done?" after files are generated | Uses `cad-artifact-inspection`, `cad-final-verification`, reports Verified/Inferred/Unverified, includes evidence ledger, and names open risks |

## Pass Criteria

A forward test passes only if the tested agent:

- chooses the right local skill route,
- asks or records blocking requirements,
- uses engineering sanity before design richness for no-reference mechanical design,
- produces scorecard results for visual layout and design richness when relevant,
- uses artifact inspection for neutral STEP/STL/DXF/DWG/PDF exports when parsers are available,
- creates or requests an evidence ledger for nontrivial final files,
- keeps SolidWorks native claims separate from neutral export claims,
- marks missing loads, materials, tools, or human judgement as Unverified,
- avoids broad "all good" language unless every required gate passed.

## Failure Patterns

Record failures verbatim when they happen:

- says "looks professional" without a scorecard,
- says "strength is fine" without loads/material/calculation,
- calls a file ready without hash/mtime/freshness evidence,
- claims native SolidWorks readiness from STEP/PDF evidence,
- installs or runs external scripts during intake,
- compares only a whole-page preview for reference matching,
- hides Unverified items inside a success summary.
- treats an artwork, portrait, logo, or photograph as a mechanical drawing and produces dimensions, a BOM, or STEP geometry without a mechanical brief.

## Loop Use

After finishing a local CAD skill stage, require at least three loop rounds before calling the stage clean:

1. Loop 1: run relevant validators and record failures or missing evidence.
2. Loop 2: fix or explicitly classify Loop 1 issues and rerun validators.
3. Loop 3: rerun validators and residue scans from a clean state.

If Loop 3 reveals any new issue, continue looping until no new issue remains.

After each forward test:

1. Record the prompt, tested skill route, observed failure, and exact overclaim or skipped gate.
2. Patch the smallest local skill or validator rule that would prevent the failure.
3. Re-run deterministic validation.
4. Repeat until the same scenario no longer fails or the remaining issue requires human CAD judgement or L3 source-edit authorization.

## Reporting

Report:

- scenario name,
- pass/fail,
- skills used or skipped,
- observed overclaim,
- local skill change made,
- remaining human judgement or toolchain blockers,
- next smallest action.
