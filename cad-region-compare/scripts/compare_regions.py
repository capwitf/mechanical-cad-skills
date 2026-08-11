#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
from PIL import Image, ImageChops, ImageFilter


IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".bmp", ".tif", ".tiff", ".webp"}


def open_source(path: Path, page_index: int, dpi: int) -> Image.Image:
    ext = path.suffix.lower()
    if ext == ".pdf":
        import fitz  # type: ignore

        doc = fitz.open(str(path))
        try:
            if page_index < 0 or page_index >= doc.page_count:
                raise ValueError(f"page index {page_index} out of range for {path}")
            page = doc.load_page(page_index)
            zoom = dpi / 72.0
            pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom), alpha=False)
            image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        finally:
            doc.close()
        return image
    if ext in IMAGE_EXTS:
        return Image.open(path).convert("RGB")
    raise ValueError(f"unsupported source type: {path.suffix}")


def parse_crop(raw: str, size: tuple[int, int]) -> tuple[int, int, int, int]:
    parts = [float(item.strip()) for item in raw.split(",")]
    if len(parts) != 4:
        raise ValueError("crop must be x,y,w,h")
    width, height = size
    x, y, w, h = parts
    if all(0.0 <= value <= 1.0 for value in parts):
        x, y, w, h = x * width, y * height, w * width, h * height
    left = max(0, int(round(x)))
    top = max(0, int(round(y)))
    right = min(width, int(round(x + w)))
    bottom = min(height, int(round(y + h)))
    if right <= left or bottom <= top:
        raise ValueError(f"invalid crop {raw} for image size {size}")
    return left, top, right, bottom


def crop_image(image: Image.Image, crop: str | None) -> Image.Image:
    if not crop:
        return image.copy()
    return image.crop(parse_crop(crop, image.size))


def grayscale_array(image: Image.Image, size: tuple[int, int]) -> np.ndarray:
    return np.asarray(image.convert("L").resize(size, Image.Resampling.BICUBIC), dtype=np.float32)


def edge_array(image: Image.Image, size: tuple[int, int]) -> np.ndarray:
    gray = image.convert("L").resize(size, Image.Resampling.BICUBIC)
    edges = gray.filter(ImageFilter.FIND_EDGES)
    return np.asarray(edges, dtype=np.float32)


def metrics(reference: Image.Image, candidate: Image.Image) -> dict[str, Any]:
    target = (
        min(reference.width, candidate.width),
        min(reference.height, candidate.height),
    )
    if target[0] <= 0 or target[1] <= 0:
        raise ValueError("empty comparison region")
    ref = grayscale_array(reference, target)
    cand = grayscale_array(candidate, target)
    diff = ref - cand
    mae = float(np.mean(np.abs(diff)))
    rmse = float(math.sqrt(np.mean(diff * diff)))
    similarity = max(0.0, 1.0 - mae / 255.0)
    ref_edges = edge_array(reference, target)
    cand_edges = edge_array(candidate, target)
    edge_diff = float(np.mean(np.abs(ref_edges - cand_edges)))
    return {
        "comparison_size": list(target),
        "mean_absolute_error": round(mae, 4),
        "root_mean_square_error": round(rmse, 4),
        "normalized_similarity": round(similarity, 6),
        "reference_edge_density": round(float(np.mean(ref_edges > 32)), 6),
        "candidate_edge_density": round(float(np.mean(cand_edges > 32)), 6),
        "edge_mean_absolute_error": round(edge_diff, 4),
    }


def save_images(
    output_dir: Path | None,
    label: str,
    reference: Image.Image,
    candidate: Image.Image,
) -> dict[str, str]:
    if output_dir is None:
        return {}
    output_dir.mkdir(parents=True, exist_ok=True)
    ref_path = output_dir / f"{label}-reference.png"
    cand_path = output_dir / f"{label}-candidate.png"
    diff_path = output_dir / f"{label}-diff.png"
    reference.save(ref_path)
    candidate.save(cand_path)
    target = (min(reference.width, candidate.width), min(reference.height, candidate.height))
    ref = reference.convert("RGB").resize(target, Image.Resampling.BICUBIC)
    cand = candidate.convert("RGB").resize(target, Image.Resampling.BICUBIC)
    ImageChops.difference(ref, cand).save(diff_path)
    return {
        "reference_crop": str(ref_path),
        "candidate_crop": str(cand_path),
        "difference_image": str(diff_path),
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Compare local CAD drawing/image regions.")
    parser.add_argument("--reference", required=True, help="Reference PDF or image.")
    parser.add_argument("--candidate", required=True, help="Candidate/output PDF or image.")
    parser.add_argument("--ref-page", type=int, default=0, help="Reference PDF page index, 0-based.")
    parser.add_argument("--candidate-page", type=int, default=0, help="Candidate PDF page index, 0-based.")
    parser.add_argument("--dpi", type=int, default=200, help="PDF render DPI.")
    parser.add_argument("--crop", help="Shared crop x,y,w,h, normalized 0-1 or pixels.")
    parser.add_argument("--ref-crop", help="Reference crop x,y,w,h. Overrides --crop for reference.")
    parser.add_argument("--candidate-crop", help="Candidate crop x,y,w,h. Overrides --crop for candidate.")
    parser.add_argument("--output-dir", help="Optional directory for crop and diff images.")
    parser.add_argument("--json-output", help="Optional JSON report path. Defaults to stdout.")
    parser.add_argument("--label", default="region", help="Label used in report and output filenames.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    ref_path = Path(args.reference).resolve()
    cand_path = Path(args.candidate).resolve()
    reference = crop_image(open_source(ref_path, args.ref_page, args.dpi), args.ref_crop or args.crop)
    candidate = crop_image(open_source(cand_path, args.candidate_page, args.dpi), args.candidate_crop or args.crop)
    comparison = metrics(reference, candidate)
    output_paths = save_images(Path(args.output_dir).resolve() if args.output_dir else None, args.label, reference, candidate)
    report = {
        "schema": "cad-region-compare/v1",
        "created_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "label": args.label,
        "reference": str(ref_path),
        "candidate": str(cand_path),
        "ref_page": args.ref_page,
        "candidate_page": args.candidate_page,
        "crop": {
            "shared": args.crop,
            "reference": args.ref_crop,
            "candidate": args.candidate_crop,
        },
        "reference_crop_size": list(reference.size),
        "candidate_crop_size": list(candidate.size),
        "metrics": comparison,
        "outputs": output_paths,
        "notes": [
            "Metrics compare rendered pixels only.",
            "Use as evidence for local visual review, not proof of dimensions or engineering correctness.",
        ],
    }
    text = json.dumps(report, ensure_ascii=False, indent=2)
    if args.json_output:
        out = Path(args.json_output).resolve()
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text + "\n", encoding="utf-8")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
