# CAD/SW Tooling Options

Use this reference only when choosing or installing CAD/SolidWorks tooling. Verify current maturity before installation; this file records a starting point, not a permanent trust decision.

Before absorbing, installing, or trusting any external candidate, use `cad-external-skill-intake` for read-only review. Then use `cad-toolchain-preflight` for a local proof on this machine.

## Recommended Order

1. `earthtojake/text-to-cad`
   - Best first choice for general agent-driven CAD.
   - Useful skills include CAD, STEP parts, DXF, viewer, hardware/robotics-oriented workflows.
   - Prefer for parametric parts, STEP generation, and inspectable source scripts.
   - Verify with `npx skills find cad` and GitHub metadata before installing.

2. `wzyn20051216/solidworks-automation-skill`
   - Candidate for native SolidWorks automation on Windows.
   - Depends on local SolidWorks, Python, and COM/API access.
   - Treat as promising but not production-proven. Run preflight before real work.

3. FreeCAD options
   - `github/awesome-copilot@freecad-scripts` for FreeCAD Python scripting guidance.
   - `neka-nat/freecad-mcp` for MCP-style FreeCAD control.
   - Prefer when native SolidWorks is unavailable and FreeCAD outputs are acceptable.

4. SolidWorks MCP servers
   - Examples include TypeScript/Python/C# SolidWorks MCP projects.
   - Treat most as experimental unless they have recent releases, clear docs, and successful local preflight.
   - Do not trust them for final engineering quality without manual/open-file verification.

## Current Verification Commands

```powershell
npx --yes skills find cad
npx --yes skills find solidworks
npx --yes skills find freecad
```

For GitHub metadata:

```powershell
$repo = 'earthtojake/text-to-cad'
Invoke-RestMethod -Headers @{ 'User-Agent' = 'codex' } "https://api.github.com/repos/$repo"
```

## Selection Notes

- Use skill packages for procedure and reusable knowledge.
- Use MCP/API servers as execution bridges only after preflight.
- Use neutral exports such as STEP/DXF/PDF for independent inspection.
- Keep source scripts/models with final outputs so work can be regenerated.
- Do not execute external installers or repository scripts during intake.
