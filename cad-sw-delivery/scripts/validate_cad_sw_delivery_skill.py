#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from pathlib import Path


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    sys.exit(1)


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def main() -> None:
    skill_dir = Path(__file__).resolve().parents[1]
    project_dir = skill_dir.parents[2]
    skill_md = skill_dir / "SKILL.md"
    reference = skill_dir / "references" / "tooling-options.md"
    openai_yaml = skill_dir / "agents" / "openai.yaml"
    sibling_skill = project_dir / "jixie-fuke" / "SKILL.md"

    require(skill_md.exists(), "SKILL.md is missing")
    text = skill_md.read_text(encoding="utf-8")
    banned_marker = "TO" + "DO"
    require(banned_marker not in text, "SKILL.md still contains banned marker")

    frontmatter = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    require(frontmatter is not None, "YAML frontmatter is missing")
    fm = frontmatter.group(1)
    require(re.search(r"^name:\s*cad-sw-delivery\s*$", fm, re.M) is not None, "name is not cad-sw-delivery")
    desc_match = re.search(r"^description:\s*(.+)$", fm, re.M)
    require(desc_match is not None, "description is missing")
    description = desc_match.group(1)
    require(description.startswith("Use when "), "description must start with 'Use when '")
    require(len(description) <= 1024, "description exceeds 1024 characters")

    required_terms = [
        "Do not claim",
        "cad-requirements-lock",
        "cad-original-design",
        "cad-design-richness",
        "cad-visual-layout",
        "cad-toolchain-preflight",
        "cad-reference-match",
        "cad-final-verification",
        "jixie-fuke",
        "SolidWorks",
        "STEP",
        "DXF",
        "DWG",
        "SLDPRT",
        "acceptance ledger",
        "Verification Loop",
        "preflight",
        "fresh",
        "final deliverable",
        "Verified",
        "Inferred",
        "Unverified",
        "Export success only proves",
        "Default mode is `L1/report-only`",
        "If `LOOP.md` or `STATE.md` is missing",
        "After each loop run, summarize",
    ]
    lowered = text.lower()
    missing = [term for term in required_terms if term.lower() not in lowered]
    require(not missing, "SKILL.md missing required terms: " + ", ".join(missing))

    require(reference.exists(), "tooling-options.md is missing")
    ref_text = reference.read_text(encoding="utf-8")
    for term in ["earthtojake/text-to-cad", "wzyn20051216/solidworks-automation-skill", "FreeCAD", "MCP", "npx --yes skills find"]:
        require(term in ref_text, f"tooling reference missing {term}")

    require(openai_yaml.exists(), "agents/openai.yaml is missing")
    yaml_text = openai_yaml.read_text(encoding="utf-8")
    for term in ["display_name", "short_description", "default_prompt", "$cad-sw-delivery"]:
        require(term in yaml_text, f"openai.yaml missing {term}")

    require(sibling_skill.exists(), "expected sibling local skill jixie-fuke/SKILL.md is missing")
    print("PASS: cad-sw-delivery skill validation passed")


if __name__ == "__main__":
    main()
