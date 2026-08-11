#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def scenario_path() -> Path:
    return Path(__file__).resolve().parents[1] / "references" / "scenarios.json"


def load() -> dict:
    return json.loads(scenario_path().read_text(encoding="utf-8"))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="List or emit CAD skill forward-test scenarios.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--list", action="store_true", help="List scenario ids and classes.")
    group.add_argument("--id", help="Emit one scenario by id.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    data = load()
    scenarios = data["scenarios"]
    if args.list:
        for item in scenarios:
            print(f"{item['id']}\t{item['class']}")
        return 0
    for item in scenarios:
        if item["id"] == args.id:
            print(json.dumps(item, ensure_ascii=False, indent=2))
            return 0
    print(f"Scenario not found: {args.id}", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
