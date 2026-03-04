#!/usr/bin/env python3
"""Compile a TikZ standalone .tex file to PNG via pdflatex + pdftoppm."""

import argparse
import subprocess
import sys
from pathlib import Path


def compile_tikz(tex_path: Path, dpi: int) -> None:
    stem = tex_path.stem  # e.g. "rings_standalone"
    out_name = stem.removesuffix("_standalone")  # e.g. "rings"

    # Run pdflatex
    result = subprocess.run(
        ["pdflatex", "-interaction=nonstopmode", tex_path.name],
        cwd=tex_path.parent,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(result.stdout[-3000:])
        print(result.stderr[-1000:])
        sys.exit(f"pdflatex failed for {tex_path.name}")
    print(f"✓ pdflatex → {stem}.pdf")

    pdf_path = tex_path.with_suffix(".pdf")
    tmp_prefix = tex_path.parent / f"{out_name}_tmp"
    png_path = tex_path.parent / f"{out_name}.png"

    # Run pdftoppm
    result = subprocess.run(
        ["pdftoppm", "-r", str(dpi), "-png", str(pdf_path), str(tmp_prefix)],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        sys.exit(f"pdftoppm failed: {result.stderr}")

    # Move numbered output (e.g. rings_tmp-1.png) to final name
    candidates = sorted(tex_path.parent.glob(f"{out_name}_tmp-*.png"))
    if not candidates:
        sys.exit("pdftoppm produced no output files")
    candidates[0].rename(png_path)
    for extra in candidates[1:]:
        extra.unlink()

    print(f"✓ pdftoppm → {png_path.name}  ({dpi} dpi)")


def main():
    parser = argparse.ArgumentParser(
        description="Compile a TikZ standalone .tex to PNG."
    )
    parser.add_argument(
        "files",
        nargs="+",
        metavar="FILE",
        help="Standalone .tex file(s) to compile (e.g. rings_standalone.tex)",
    )
    parser.add_argument(
        "--dpi",
        type=int,
        default=300,
        help="Resolution for PNG output (default: 300)",
    )
    args = parser.parse_args()

    for f in args.files:
        tex_path = Path(f).resolve()
        if not tex_path.exists():
            sys.exit(f"File not found: {tex_path}")
        if tex_path.suffix != ".tex":
            sys.exit(f"Expected a .tex file, got: {tex_path}")
        compile_tikz(tex_path, args.dpi)


if __name__ == "__main__":
    main()
