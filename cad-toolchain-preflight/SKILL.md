---
name: cad-toolchain-preflight
description: Use when Codex may install, choose, call, or rely on CAD tooling, external agent skills, MCP servers, SolidWorks automation, FreeCAD, text-to-cad, build123d, CadQuery, Python CAD scripts, or format converters before producing CAD deliverables.
---

# CAD Toolchain Preflight

## Core Rule

Do not trust a CAD toolchain because it is popular, installed, or produced a sample image. Trust it only after it passes a task-appropriate local preflight.

`earthtojake/text-to-cad` is appropriate for parameterized mechanical geometry with a STEP-first artifact path. It is not an illustration tracing tool: do not select it for portraits, posters, logos, photographs, or freehand artwork that only need editable 2D line art. Route those requests to `cad-illustration-vectorization`.

## External Skill Intake

Before installing, localizing, or relying on an external GitHub/registry CAD skill, MCP server, or automation package, use `cad-external-skill-intake` first.

Keep the phases separate:

| Phase | Purpose | Must not do |
|---|---|---|
| External intake | Read docs, metadata, examples, and workflows; classify Green/Yellow/Red risk | Install globally, execute external scripts, trust README claims |
| Local preflight | Prove the selected tool path works on this machine with a tiny CAD artifact | Claim final engineering quality from a sample alone |

Only continue from external intake to local preflight when the candidate is Green or Yellow with explicit risk reporting. Red candidates require a different tool path or user approval to continue despite risk.

## Maturity Check

Before installing or relying on an external CAD skill or MCP server, check:

- install count or adoption,
- GitHub stars/forks/issues,
- latest commit or release date,
- supported CAD versions and operating systems,
- whether the project says alpha, experimental, untested, demo, or prototype,
- whether the task needs native SolidWorks files or neutral exports are enough.

Treat maturity as a risk signal, not as proof of engineering correctness.

## Local Preflight

Run the smallest possible local proof before real work:

| Tool path | Minimum proof |
|---|---|
| text-to-cad/build123d/CadQuery | Generate a tiny part, export STEP, confirm file is non-empty and inspectable |
| SolidWorks COM/API | Use `cad-solidworks-native-preflight`: launch SolidWorks, create/open a test part, rebuild, save, reopen native file, and export STEP/PDF/DXF if relevant |
| FreeCAD Python/MCP | Create a test document/body, export STEP or screenshot, confirm nonblank result |
| DXF/DWG converter | Convert a tiny drawing and confirm entities/layers/text survive |
| PDF/image renderer | Render a known page/view and confirm framing is not blank or cropped |

If the preflight fails, switch tools or report the blocker. Do not continue as if the path is verified.

## Tool Risk Levels

- **Green**: local preflight passed and output format matches the task.
- **Yellow**: tool works partly, but native format/export/render needs manual verification.
- **Red**: install fails, tool cannot launch, output is blank/stale, or project is too experimental for the requested deliverable.

Use yellow or red tools only with explicit risk reporting and a fallback.

## External Skill Notes

Useful candidates to verify at task time:

- `earthtojake/text-to-cad` for general parametric CAD and STEP/DXF-oriented work.
- `wzyn20051216/solidworks-automation-skill` for Windows SolidWorks automation, after COM/API preflight.
- FreeCAD scripting or FreeCAD MCP options when FreeCAD is acceptable.

Do not install external skills globally unless the user allows it or the current task clearly needs it.

## Handoff

After preflight:

- Return the selected tool path and risk level.
- Record exact commands or checks run.
- Use `cad-final-verification` for final deliverable checks.
- Use `cad-solidworks-native-preflight` before any native `.sldprt`, `.sldasm`, or `.slddrw` readiness claim.
- Use `cad-reference-match` if visual/reference similarity matters.

## Common Mistakes

- Treating a GitHub star count as a working local install.
- Using a SolidWorks MCP server before confirming SolidWorks can launch and rebuild.
- Trusting a neutral STEP export as evidence that native SolidWorks files are correct.
- Continuing after a blank render because the command exited with code 0.
