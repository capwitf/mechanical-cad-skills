#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from pathlib import Path


CLUSTER = {
    "cad-sw-delivery": [
        "cad-requirements-lock",
        "cad-original-design",
        "cad-engineering-sanity",
        "cad-design-richness",
        "cad-visual-layout",
        "cad-external-skill-intake",
        "cad-toolchain-preflight",
        "cad-illustration-vectorization",
        "cad-solidworks-native-preflight",
        "cad-reference-match",
        "cad-region-compare",
        "jixie-fuke",
        "cad-artifact-inspection",
        "cad-evidence-ledger",
        "cad-final-verification",
    ],
    "cad-original-design": [
        "Design Brief",
        "Concept Pass",
        "Modeling Rules",
        "Original Design Checks",
        "complexity target",
        "professional drawing elements",
        "cad-engineering-sanity",
        "cad-design-richness",
        "cad-visual-layout",
        "cad-requirements-lock",
        "cad-toolchain-preflight",
        "cad-final-verification",
        "cad-reference-match",
    ],
    "cad-design-richness": [
        "Richness Gate",
        "Richness Scorecard",
        "Minimum pass",
        "Critical fail",
        "Function zones",
        "Standard features",
        "Complexity Target",
        "cad-engineering-sanity",
        "cad-original-design",
        "cad-visual-layout",
        "design richness pass/fail",
    ],
    "cad-engineering-sanity": [
        "Sanity Table",
        "Minimum Quantitative Boundary",
        "Claim Discipline",
        "Original Design Gate",
        "load path",
        "interfaces",
        "wall thickness",
        "hole edge distance",
        "clearances",
        "standard features",
        "Verified",
        "Inferred",
        "Unverified",
        "cad-original-design",
        "cad-design-richness",
        "cad-final-verification",
    ],
    "cad-visual-layout": [
        "Layout Gate",
        "Layout Scorecard",
        "Minimum pass",
        "Critical fail",
        "View hierarchy",
        "Line hierarchy",
        "Thumbnail impression",
        "visual layout pass/fail",
        "title block",
        "hatch",
    ],
    "cad-requirements-lock": [
        "Unknowns Policy",
        "Visual target",
        "Complexity target",
        "Engineering sanity",
        "cad-engineering-sanity",
        "cad-design-richness",
        "cad-visual-layout",
        "cad-toolchain-preflight",
        "cad-reference-match",
        "cad-final-verification",
    ],
    "cad-toolchain-preflight": [
        "External Skill Intake",
        "cad-external-skill-intake",
        "cad-solidworks-native-preflight",
        "Maturity Check",
        "Local Preflight",
        "SolidWorks COM/API",
        "FreeCAD",
        "text-to-cad",
    ],
    "cad-illustration-vectorization": [
        "Illustration Gate",
        "Do not use",
        "text-to-cad",
        "cad-reference-match",
        "vector",
        "SVG",
        "DXF",
        "DWG",
        "No engineering claim",
        "No mechanical title block",
        "Acceptance",
    ],
    "cad-solidworks-native-preflight": [
        "Native Preflight Checklist",
        "Native Evidence Labels",
        "Automation Boundary",
        "Drawing-Specific Checks",
        "Assembly-Specific Checks",
        "SldWorks.Application",
        "COM/API",
        "pywin32",
        "rebuild",
        "reopened",
        "feature tree",
        "cad-evidence-ledger",
        "cad-final-verification",
    ],
    "cad-external-skill-intake": [
        "Read-Only Boundary",
        "No Install",
        "No External Scripts",
        "Maturity Evidence",
        "Green",
        "Yellow",
        "Red",
        "Workflow Extraction",
        "Absorption Ledger",
        "cad-toolchain-preflight",
        "cad-sw-delivery",
        "cad-final-verification",
        "Verified",
        "Inferred",
        "Unverified",
        "license",
        "latest commit",
        "archived",
        "alpha",
    ],
    "cad-reference-match": [
        "Region Checklist",
        "Comparison Loop",
        "jixie-fuke",
        ".codex/skills/jixie-fuke",
        "cad-region-compare",
        "cad-original-design",
        "cad-final-verification",
    ],
    "jixie-fuke": [
        "Detailed Rule Source",
        "../../../jixie-fuke/SKILL.md",
        "Compact Rules",
        "reference decomposition",
        "local region comparison",
        "cad-region-compare",
        "cad-reference-match",
        "cad-evidence-ledger",
        "cad-final-verification",
    ],
    "cad-region-compare": [
        "Script Usage",
        "Metrics",
        "Region Checklist",
        "compare_regions.py",
        "crop",
        "normalized_similarity",
        "edge",
        "cad-reference-match",
        "jixie-fuke",
        "cad-artifact-inspection",
        "cad-evidence-ledger",
        "cad-final-verification",
    ],
    "cad-evidence-ledger": [
        "Evidence Manifest",
        "cad_evidence_manifest.py",
        "cad-artifact-inspection",
        "SHA256",
        "modified time",
        "Source of truth",
        "Toolchain",
        "Checks run",
        "Evidence files",
        "Verified",
        "Inferred",
        "Unverified",
        "cad-final-verification",
        "cad-toolchain-preflight",
        "cad-engineering-sanity",
    ],
    "cad-artifact-inspection": [
        "Script Usage",
        "Format Coverage",
        "Status Labels",
        "inspect_cad_artifacts.py",
        "STEP/STP",
        "STL",
        "DXF",
        "DWG",
        "PDF",
        "pass",
        "partial",
        "fail",
        "cad-evidence-ledger",
        "cad-final-verification",
        "cad-solidworks-native-preflight",
    ],
    "cad-final-verification": [
        "Required Checks",
        "Four Gates",
        "Artifact inspection",
        "Evidence ledger",
        "Evidence Package",
        "Engineering sanity",
        "SolidWorks native",
        "Visual layout",
        "Design richness",
        "Verified",
        "Inferred",
        "Unverified",
        "cad-visual-layout",
        "cad-design-richness",
        "cad-engineering-sanity",
        "cad-artifact-inspection",
        "cad-evidence-ledger",
        "cad-solidworks-native-preflight",
        "cad-reference-match",
        "cad-region-compare",
    ],
    "cad-skill-forward-test": [
        "Forward-Test Scenarios",
        "scenarios.json",
        "list_forward_scenarios.py",
        "Pass Criteria",
        "Failure Patterns",
        "Loop Use",
        "cad-requirements-lock",
        "cad-original-design",
        "cad-engineering-sanity",
        "cad-design-richness",
        "cad-visual-layout",
        "cad-artifact-inspection",
        "cad-evidence-ledger",
        "cad-solidworks-native-preflight",
        "cad-external-skill-intake",
        "Verified/Inferred/Unverified",
        "L3/source-edit",
    ],
}


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    sys.exit(1)


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def validate_skill(skill_root: Path, name: str, required_terms: list[str]) -> None:
    skill_dir = skill_root / name
    skill_md = skill_dir / "SKILL.md"
    openai_yaml = skill_dir / "agents" / "openai.yaml"

    require(skill_md.exists(), f"{name}: SKILL.md missing")
    text = read(skill_md)
    banned_marker = "TO" + "DO"
    require(banned_marker not in text, f"{name}: banned marker remains")
    bracketed_marker = "[TO" + "DO"
    template_marker = "Complete and " + "informative"
    require(bracketed_marker not in text, f"{name}: bracketed marker remains")
    require(template_marker not in text, f"{name}: template text remains")

    frontmatter = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    require(frontmatter is not None, f"{name}: frontmatter missing")
    fm = frontmatter.group(1)
    require(re.search(rf"^name:\s*{re.escape(name)}\s*$", fm, re.M) is not None, f"{name}: wrong name")
    desc = re.search(r"^description:\s*(.+)$", fm, re.M)
    require(desc is not None, f"{name}: description missing")
    require(desc.group(1).startswith("Use when "), f"{name}: description must start with Use when")
    require(len(desc.group(1)) <= 1024, f"{name}: description too long")

    lowered = text.lower()
    missing = [term for term in required_terms if term.lower() not in lowered]
    require(not missing, f"{name}: missing terms: {', '.join(missing)}")

    require(openai_yaml.exists(), f"{name}: agents/openai.yaml missing")
    yaml_text = read(openai_yaml)
    for term in ["display_name", "short_description", "default_prompt", f"${name}"]:
        require(term in yaml_text, f"{name}: openai.yaml missing {term}")

    if name == "cad-evidence-ledger":
        script = skill_dir / "scripts" / "cad_evidence_manifest.py"
        require(script.exists(), "cad-evidence-ledger: manifest script missing")
    if name == "cad-artifact-inspection":
        script = skill_dir / "scripts" / "inspect_cad_artifacts.py"
        require(script.exists(), "cad-artifact-inspection: inspection script missing")
    if name == "cad-region-compare":
        script = skill_dir / "scripts" / "compare_regions.py"
        require(script.exists(), "cad-region-compare: compare script missing")
    if name == "cad-skill-forward-test":
        scenario_file = skill_dir / "references" / "scenarios.json"
        script = skill_dir / "scripts" / "list_forward_scenarios.py"
        require(scenario_file.exists(), "cad-skill-forward-test: scenarios.json missing")
        require(script.exists(), "cad-skill-forward-test: scenario script missing")


def validate_loop_policy(project_root: Path, skill_root: Path) -> None:
    loop_md = project_root / "LOOP.md"
    state_md = project_root / "STATE.md"
    delivery_md = skill_root / "cad-sw-delivery" / "SKILL.md"

    require(loop_md.exists(), "LOOP.md missing")
    require(state_md.exists(), "STATE.md missing")

    loop_text = read(loop_md)
    delivery_text = read(delivery_md)

    loop_terms = [
        "Default mode is `L1/report-only`",
        "current user message explicitly authorizes",
        "If `LOOP.md` or `STATE.md` is missing",
        "Never use one global `STATE.md`",
        "Stage Completion Loop Rule",
        "at least three loop rounds",
        "Loop 1",
        "Loop 2",
        "Loop 3",
        "Summarize what changed, what was observed, open risks, and the next smallest action",
    ]
    for term in loop_terms:
        require(term in loop_text, f"LOOP.md missing loop policy term: {term}")

    delivery_terms = [
        "Loop Guard",
        "Default mode is `L1/report-only`",
        "If `LOOP.md` or `STATE.md` is missing",
        "current user message explicitly authorizes",
        "Never use one global `STATE.md`",
        "at least three loop rounds",
        "Loop 1",
        "Loop 2",
        "Loop 3",
        "After each loop run, summarize",
    ]
    for term in delivery_terms:
        require(term in delivery_text, f"cad-sw-delivery missing loop policy term: {term}")


def main() -> None:
    skill_root = Path(__file__).resolve().parents[2]
    project_root = skill_root.parents[1]
    validate_loop_policy(project_root, skill_root)
    for name, required_terms in CLUSTER.items():
        validate_skill(skill_root, name, required_terms)

    root_jixie = project_root / "jixie-fuke" / "SKILL.md"
    require(root_jixie.exists(), "root jixie-fuke/SKILL.md missing")

    delivery_text = read(skill_root / "cad-sw-delivery" / "SKILL.md")
    for child in CLUSTER["cad-sw-delivery"]:
        require(child in delivery_text, f"cad-sw-delivery does not reference {child}")

    require(
        "cad-illustration-vectorization" in delivery_text,
        "cad-sw-delivery does not route illustration vectorization",
    )
    require(
        "STEP-first" in delivery_text,
        "cad-sw-delivery does not state text-to-cad STEP-first boundary",
    )

    print("PASS: CAD local skill cluster validation passed")


if __name__ == "__main__":
    main()
