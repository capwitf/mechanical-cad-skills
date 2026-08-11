#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
import re
import struct
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


STEP_ENTITY_RE = re.compile(r"#\d+\s*=\s*([A-Z0-9_]+)\s*\(", re.I)
STEP_SHAPE_HINTS = {
    "ADVANCED_BREP_SHAPE_REPRESENTATION",
    "MANIFOLD_SOLID_BREP",
    "CLOSED_SHELL",
    "SHELL_BASED_SURFACE_MODEL",
    "FACETED_BREP",
    "GEOMETRIC_CURVE_SET",
    "SHAPE_REPRESENTATION",
    "PRODUCT",
}


def utc_from_ts(ts: float) -> str:
    return datetime.fromtimestamp(ts, timezone.utc).replace(microsecond=0).isoformat()


def resolve(root: Path, item: str) -> Path:
    path = Path(item)
    if not path.is_absolute():
        path = root / path
    return path.resolve()


def base_record(root: Path, item: str) -> dict[str, Any]:
    path = resolve(root, item)
    record: dict[str, Any] = {
        "input": item,
        "path": str(path),
        "relative_path": None,
        "extension": path.suffix.lower(),
        "exists": path.exists(),
        "is_file": path.is_file(),
        "size_bytes": None,
        "mtime_utc": None,
        "status": "fail",
        "errors": [],
        "warnings": [],
        "metrics": {},
    }
    try:
        record["relative_path"] = str(path.relative_to(root))
    except ValueError:
        pass
    if path.is_file():
        stat = path.stat()
        record["size_bytes"] = stat.st_size
        record["mtime_utc"] = utc_from_ts(stat.st_mtime)
        if stat.st_size <= 0:
            record["errors"].append("file is empty")
    elif not path.exists():
        record["errors"].append("file is missing")
    else:
        record["errors"].append("path is not a file")
    return record


def set_status(record: dict[str, Any], status: str) -> None:
    order = {"fail": 0, "partial": 1, "pass": 2}
    if order[status] > order.get(record.get("status", "fail"), 0):
        record["status"] = status


def inspect_pdf(path: Path, record: dict[str, Any]) -> None:
    try:
        import fitz  # type: ignore
    except Exception:
        record["warnings"].append("PyMuPDF not available; PDF content not parsed")
        set_status(record, "partial")
        return

    try:
        doc = fitz.open(str(path))
        page_count = doc.page_count
        text_chars = 0
        image_count = 0
        drawing_count = 0
        page_sizes: list[list[float]] = []
        for page in doc:
            rect = page.rect
            page_sizes.append([round(rect.width, 3), round(rect.height, 3)])
            text_chars += len(page.get_text("text") or "")
            image_count += len(page.get_images(full=True))
            try:
                drawing_count += len(page.get_drawings())
            except Exception:
                record["warnings"].append("drawing object count unavailable for one or more PDF pages")
        doc.close()
        record["metrics"].update(
            {
                "page_count": page_count,
                "text_chars": text_chars,
                "image_count": image_count,
                "drawing_object_count": drawing_count,
                "page_sizes": page_sizes,
            }
        )
        if page_count <= 0:
            record["errors"].append("PDF has no pages")
        elif text_chars == 0 and image_count == 0 and drawing_count == 0:
            record["errors"].append("PDF pages appear blank to parser")
        else:
            set_status(record, "pass")
    except Exception as exc:
        record["errors"].append(f"PDF parse failed: {exc}")


def inspect_dxf(path: Path, record: dict[str, Any]) -> None:
    try:
        import ezdxf  # type: ignore
    except Exception:
        record["warnings"].append("ezdxf not available; DXF content not parsed")
        set_status(record, "partial")
        return

    try:
        doc = ezdxf.readfile(str(path))
        msp = doc.modelspace()
        entities = list(msp)
        counts = Counter(entity.dxftype() for entity in entities)
        record["metrics"].update(
            {
                "dxfversion": doc.dxfversion,
                "modelspace_entity_count": len(entities),
                "entity_type_counts": dict(sorted(counts.items())),
                "layer_count": len(doc.layers),
                "layout_names": [layout.name for layout in doc.layouts],
                "dimension_count": counts.get("DIMENSION", 0),
                "text_count": counts.get("TEXT", 0) + counts.get("MTEXT", 0),
            }
        )
        if len(entities) <= 0:
            record["errors"].append("DXF modelspace has no entities")
        else:
            set_status(record, "pass")
    except Exception as exc:
        record["errors"].append(f"DXF parse failed: {exc}")


def update_bbox(bbox: list[list[float]] | None, vertex: tuple[float, float, float]) -> list[list[float]]:
    if bbox is None:
        return [[vertex[0], vertex[1], vertex[2]], [vertex[0], vertex[1], vertex[2]]]
    for idx in range(3):
        bbox[0][idx] = min(bbox[0][idx], vertex[idx])
        bbox[1][idx] = max(bbox[1][idx], vertex[idx])
    return bbox


def inspect_stl(path: Path, record: dict[str, Any]) -> None:
    data = path.read_bytes()
    bbox: list[list[float]] | None = None
    vertex_count = 0
    triangle_count = 0
    mode = "unknown"

    if len(data) >= 84:
        tri_count = struct.unpack("<I", data[80:84])[0]
        expected_size = 84 + tri_count * 50
        if expected_size == len(data):
            mode = "binary"
            triangle_count = tri_count
            offset = 84
            for _ in range(tri_count):
                offset += 12
                for _vertex_index in range(3):
                    vertex = struct.unpack("<fff", data[offset : offset + 12])
                    if all(math.isfinite(value) for value in vertex):
                        bbox = update_bbox(bbox, vertex)
                        vertex_count += 1
                    offset += 12
                offset += 2

    if triangle_count == 0:
        text = data.decode("utf-8", errors="ignore")
        vertices = re.findall(
            r"vertex\s+([-+0-9.eE]+)\s+([-+0-9.eE]+)\s+([-+0-9.eE]+)",
            text,
        )
        if vertices:
            mode = "ascii"
            vertex_count = len(vertices)
            triangle_count = vertex_count // 3
            for raw in vertices:
                vertex = tuple(float(value) for value in raw)
                bbox = update_bbox(bbox, vertex)

    record["metrics"].update(
        {
            "stl_mode": mode,
            "triangle_count": triangle_count,
            "vertex_count": vertex_count,
            "bounding_box": bbox,
        }
    )
    if triangle_count <= 0 or bbox is None:
        record["errors"].append("STL has no parsed triangles or bounding box")
    else:
        record["warnings"].append("STL manifold and watertightness are not checked")
        set_status(record, "pass")


def inspect_step(path: Path, record: dict[str, Any]) -> None:
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except Exception as exc:
        record["errors"].append(f"STEP read failed: {exc}")
        return

    upper = text.upper()
    entities = [match.upper() for match in STEP_ENTITY_RE.findall(text)]
    counts = Counter(entities)
    shape_counts = {name: counts[name] for name in sorted(STEP_SHAPE_HINTS) if counts[name]}
    record["metrics"].update(
        {
            "has_iso_10303_header": "ISO-10303" in upper[:2048],
            "has_data_section": "DATA;" in upper and "ENDSEC;" in upper,
            "entity_count": len(entities),
            "shape_hint_counts": shape_counts,
            "top_entity_types": dict(counts.most_common(20)),
        }
    )
    record["warnings"].append("STEP geometry topology is not checked without a STEP kernel")
    if not record["metrics"]["has_iso_10303_header"] or not record["metrics"]["has_data_section"] or not entities:
        record["errors"].append("STEP container markers or entities are missing")
    elif not shape_counts:
        record["warnings"].append("No common STEP shape representation entities found")
        set_status(record, "partial")
    else:
        set_status(record, "partial")


def inspect_unknown(record: dict[str, Any]) -> None:
    if record["extension"] == ".dwg":
        record["warnings"].append("DWG parser unavailable; convert to DXF/PDF or open in CAD for content checks")
    else:
        record["warnings"].append("Unsupported CAD artifact type; only file-level checks performed")
    if record["size_bytes"] and record["size_bytes"] > 0:
        set_status(record, "partial")


def inspect_file(root: Path, item: str) -> dict[str, Any]:
    record = base_record(root, item)
    if record["errors"]:
        return record
    path = resolve(root, item)
    ext = record["extension"]
    if ext == ".pdf":
        inspect_pdf(path, record)
    elif ext == ".dxf":
        inspect_dxf(path, record)
    elif ext == ".stl":
        inspect_stl(path, record)
    elif ext in {".step", ".stp"}:
        inspect_step(path, record)
    else:
        inspect_unknown(record)
    return record


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Read-only inspection for CAD artifact deliverables.")
    parser.add_argument("files", nargs="+", help="CAD artifact files to inspect.")
    parser.add_argument("--root", default=".", help="Root used to resolve relative paths.")
    parser.add_argument("--output", help="Optional JSON report path. Defaults to stdout.")
    parser.add_argument("--allow-fail", action="store_true", help="Exit 0 even when one or more files fail inspection.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    root = Path(args.root).resolve()
    records = [inspect_file(root, item) for item in args.files]
    report = {
        "schema": "cad-artifact-inspection/v1",
        "root": str(root),
        "created_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "files": records,
        "summary": {
            "pass": sum(1 for item in records if item["status"] == "pass"),
            "partial": sum(1 for item in records if item["status"] == "partial"),
            "fail": sum(1 for item in records if item["status"] == "fail"),
        },
    }
    text = json.dumps(report, ensure_ascii=False, indent=2)
    if args.output:
        output = resolve(root, args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(text + "\n", encoding="utf-8")
    else:
        print(text)
    if report["summary"]["fail"] and not args.allow_fail:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
