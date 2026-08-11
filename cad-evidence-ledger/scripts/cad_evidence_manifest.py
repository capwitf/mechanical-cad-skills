#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path


SCHEMA = "cad-evidence-ledger/v1"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def file_mtime_utc(path: Path) -> str:
    return datetime.fromtimestamp(path.stat().st_mtime, timezone.utc).replace(microsecond=0).isoformat()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def resolve_under_root(root: Path, item: str) -> Path:
    path = Path(item)
    if not path.is_absolute():
        path = root / path
    return path.resolve()


def describe_file(root: Path, item: str) -> dict[str, object]:
    path = resolve_under_root(root, item)
    record: dict[str, object] = {
        "input": item,
        "path": str(path),
        "relative_path": None,
        "extension": path.suffix.lower(),
        "exists": path.exists(),
        "is_file": path.is_file(),
        "is_dir": path.is_dir(),
        "size_bytes": None,
        "mtime_utc": None,
        "sha256": None,
    }
    try:
        record["relative_path"] = str(path.relative_to(root))
    except ValueError:
        record["relative_path"] = None

    if path.is_file():
        stat = path.stat()
        record["size_bytes"] = stat.st_size
        record["mtime_utc"] = file_mtime_utc(path)
        record["sha256"] = sha256_file(path)
    return record


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Create a CAD evidence manifest for final deliverable files.")
    parser.add_argument("files", nargs="+", help="Final deliverable files to record.")
    parser.add_argument("--root", default=".", help="Root used to resolve relative file paths.")
    parser.add_argument("--output", help="Optional JSON output path. Defaults to stdout.")
    parser.add_argument("--source", action="append", default=[], help="Source-of-truth file or model path. Repeat as needed.")
    parser.add_argument("--toolchain", action="append", default=[], help="Toolchain or tool version note. Repeat as needed.")
    parser.add_argument("--check", action="append", default=[], help="Check that was actually run or directly inspected. Repeat as needed.")
    parser.add_argument("--evidence", action="append", default=[], help="Evidence artifact path such as screenshot, render, crop, or log. Repeat as needed.")
    parser.add_argument("--verified", action="append", default=[], help="Verified claim. Repeat as needed.")
    parser.add_argument("--inferred", action="append", default=[], help="Inferred claim. Repeat as needed.")
    parser.add_argument("--unverified", action="append", default=[], help="Unverified claim or blocker. Repeat as needed.")
    parser.add_argument("--allow-missing", action="store_true", help="Exit 0 even when files are missing.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    root = Path(args.root).resolve()

    files = [describe_file(root, item) for item in args.files]
    evidence_files = [describe_file(root, item) for item in args.evidence]
    sources = [describe_file(root, item) for item in args.source]

    manifest = {
        "schema": SCHEMA,
        "created_utc": utc_now(),
        "cwd": str(Path.cwd().resolve()),
        "root": str(root),
        "system": {
            "platform": platform.platform(),
            "python": platform.python_version(),
        },
        "source_of_truth": sources,
        "toolchain": args.toolchain,
        "checks_recorded": args.check,
        "files": files,
        "evidence_files": evidence_files,
        "claims": {
            "verified": args.verified,
            "inferred": args.inferred,
            "unverified": args.unverified,
        },
    }

    text = json.dumps(manifest, ensure_ascii=False, indent=2)
    if args.output:
        output = resolve_under_root(root, args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(text + "\n", encoding="utf-8")
    else:
        print(text)

    missing = [record["input"] for record in files if not record["exists"]]
    if missing and not args.allow_missing:
        print("Missing final files: " + ", ".join(str(item) for item in missing), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
