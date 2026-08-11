from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont


def load_image(path: Path, page: int = 0) -> Image.Image:
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        import fitz

        doc = fitz.open(path)
        try:
            pix = doc[page].get_pixmap(matrix=fitz.Matrix(1, 1), alpha=False)
            return Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        finally:
            doc.close()

    data = np.fromfile(path, dtype=np.uint8)
    img = cv2.imdecode(data, cv2.IMREAD_COLOR)
    if img is None:
        return Image.open(path).convert("RGB")
    return Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))


def overlay_grid(img: Image.Image, rows: int, cols: int, title: str) -> Image.Image:
    out = img.convert("RGB").copy()
    draw = ImageDraw.Draw(out)
    width, height = out.size
    try:
        font = ImageFont.truetype("arial.ttf", max(16, min(width, height) // 45))
    except OSError:
        font = ImageFont.load_default()

    for col in range(1, cols):
        x = round(col * width / cols)
        draw.line([(x, 0), (x, height)], fill=(220, 0, 0), width=2)
    for row in range(1, rows):
        y = round(row * height / rows)
        draw.line([(0, y), (width, y)], fill=(220, 0, 0), width=2)

    for row in range(rows):
        for col in range(cols):
            idx = row * cols + col + 1
            x = round(col * width / cols) + 10
            y = round(row * height / rows) + 10
            label = f"{idx:02d}"
            draw.rectangle([x - 5, y - 5, x + 48, y + 28], fill=(255, 255, 255), outline=(220, 0, 0))
            draw.text((x, y), label, fill=(220, 0, 0), font=font)
    draw.text((width // 2 - 60, 10), title, fill=(220, 0, 0), font=font)
    return out


def compare_cells(ref: Image.Image, cand: Image.Image, rows: int, cols: int) -> list[dict[str, float | int]]:
    cand = cand.resize(ref.size, Image.Resampling.LANCZOS)
    r = np.array(ref.convert("L"))
    c = np.array(cand.convert("L"))
    re = cv2.Canny(r, 80, 160) > 0
    ce = cv2.Canny(c, 80, 160) > 0
    width, height = ref.size
    results: list[dict[str, float | int]] = []
    for row in range(rows):
        for col in range(cols):
            idx = row * cols + col + 1
            x0 = round(col * width / cols)
            x1 = round((col + 1) * width / cols)
            y0 = round(row * height / rows)
            y1 = round((row + 1) * height / rows)
            rr = r[y0:y1, x0:x1].astype(np.float32)
            cc = c[y0:y1, x0:x1].astype(np.float32)
            mae = float(np.mean(np.abs(rr - cc)))
            edge_diff = float(np.mean(re[y0:y1, x0:x1] != ce[y0:y1, x0:x1]))
            results.append(
                {
                    "id": idx,
                    "row": row + 1,
                    "col": col + 1,
                    "similarity": round(1 - mae / 255.0, 5),
                    "mae": round(mae, 4),
                    "edge_diff": round(edge_diff, 5),
                    "ref_edge_density": round(float(np.mean(re[y0:y1, x0:x1])), 5),
                    "cand_edge_density": round(float(np.mean(ce[y0:y1, x0:x1])), 5),
                }
            )
    return results


def main() -> int:
    parser = argparse.ArgumentParser(description="Numbered grid acceptance for reference-matched CAD/drawing outputs.")
    parser.add_argument("--reference", required=True, type=Path)
    parser.add_argument("--candidate", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--rows", type=int, default=4)
    parser.add_argument("--cols", type=int, default=4)
    parser.add_argument("--reference-page", type=int, default=0)
    parser.add_argument("--candidate-page", type=int, default=0)
    parser.add_argument("--min-similarity", type=float, default=0.94)
    parser.add_argument("--max-edge-diff", type=float, default=0.08)
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)
    ref = load_image(args.reference, args.reference_page)
    cand = load_image(args.candidate, args.candidate_page)
    cand_resized = cand.resize(ref.size, Image.Resampling.LANCZOS)

    rows = compare_cells(ref, cand_resized, args.rows, args.cols)
    min_similarity = min(float(r["similarity"]) for r in rows)
    avg_similarity = sum(float(r["similarity"]) for r in rows) / len(rows)
    max_edge_diff = max(float(r["edge_diff"]) for r in rows)
    failed = [
        r for r in rows
        if float(r["similarity"]) < args.min_similarity or float(r["edge_diff"]) > args.max_edge_diff
    ]
    worst = sorted(rows, key=lambda r: (float(r["similarity"]), -float(r["edge_diff"])))[:5]

    ref_grid = overlay_grid(ref, args.rows, args.cols, "reference")
    cand_grid = overlay_grid(cand_resized, args.rows, args.cols, "candidate")
    side = Image.new("RGB", (ref_grid.width + cand_grid.width, max(ref_grid.height, cand_grid.height)), "white")
    side.paste(ref_grid, (0, 0))
    side.paste(cand_grid, (ref_grid.width, 0))

    ref_grid.save(args.output_dir / "reference_grid.png")
    cand_grid.save(args.output_dir / "candidate_grid.png")
    side.save(args.output_dir / "side_by_side_grid.png")

    report = {
        "schema": "cad-reference-acceptance/grid/v1",
        "reference": str(args.reference),
        "candidate": str(args.candidate),
        "rows": args.rows,
        "cols": args.cols,
        "reference_size": list(ref.size),
        "candidate_size": list(cand.size),
        "candidate_resized_to_reference": list(cand_resized.size),
        "thresholds": {
            "min_similarity": args.min_similarity,
            "max_edge_diff": args.max_edge_diff,
        },
        "summary": {
            "pass": len(failed) == 0,
            "min_similarity": round(min_similarity, 5),
            "avg_similarity": round(avg_similarity, 5),
            "max_edge_diff": round(max_edge_diff, 5),
            "failed_cell_ids": [int(r["id"]) for r in failed],
            "worst_cell_ids": [int(r["id"]) for r in worst],
        },
        "cells": rows,
        "outputs": {
            "reference_grid": str(args.output_dir / "reference_grid.png"),
            "candidate_grid": str(args.output_dir / "candidate_grid.png"),
            "side_by_side_grid": str(args.output_dir / "side_by_side_grid.png"),
            "csv": str(args.output_dir / "grid_acceptance.csv"),
            "json": str(args.output_dir / "grid_acceptance.json"),
        },
    }
    (args.output_dir / "grid_acceptance.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    with (args.output_dir / "grid_acceptance.csv").open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(json.dumps(report["summary"], ensure_ascii=False, indent=2))
    return 0 if report["summary"]["pass"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
