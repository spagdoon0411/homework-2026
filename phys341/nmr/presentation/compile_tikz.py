#!/usr/bin/env python3
"""
Compile TikZ diagrams to PNG images.
Reads tikz_files.txt for list of files to compile.
"""
import os
import subprocess
import sys
from pathlib import Path

# Directories
PRESENTATION_DIR = Path(__file__).parent
OUT_DIR = PRESENTATION_DIR / "out"
TIKZ_FILES_LIST = PRESENTATION_DIR / "tikz_files.txt"

# LaTeX template for standalone tikz compilation
LATEX_TEMPLATE = r"""\documentclass[tikz,border=10pt]{standalone}
\usepackage{tikz}
\usepackage{tikz-3dplot}
\usepackage{amsmath}
\usetikzlibrary{calc,patterns,angles,quotes,arrows.meta}

\begin{document}
\input{TIKZ_FILE}
\end{document}
"""

def ensure_out_dir():
    """Create output directory if it doesn't exist."""
    OUT_DIR.mkdir(exist_ok=True)
    print(f"Output directory: {OUT_DIR}")

def read_tikz_files():
    """Read the list of tikz files to compile."""
    if not TIKZ_FILES_LIST.exists():
        print(f"Error: {TIKZ_FILES_LIST} not found")
        sys.exit(1)

    with open(TIKZ_FILES_LIST, 'r') as f:
        files = [line.strip() for line in f if line.strip() and not line.startswith('#')]

    return files

def compile_tikz(tikz_file):
    """Compile a single tikz file to PDF and then to PNG."""
    tikz_path = PRESENTATION_DIR / tikz_file

    if not tikz_path.exists():
        print(f"Warning: {tikz_file} not found, skipping")
        return False

    # Get base name without extension
    base_name = tikz_path.stem

    print(f"\nCompiling {tikz_file}...")

    # Create temporary LaTeX file
    tex_content = LATEX_TEMPLATE.replace("TIKZ_FILE", tikz_file)
    temp_tex = OUT_DIR / f"{base_name}_temp.tex"

    with open(temp_tex, 'w') as f:
        f.write(tex_content)

    # Compile with pdflatex
    try:
        result = subprocess.run(
            ['pdflatex', '-interaction=nonstopmode', '-output-directory', str(OUT_DIR), str(temp_tex)],
            cwd=PRESENTATION_DIR,
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode != 0:
            print(f"Error compiling {tikz_file}:")
            print(result.stdout)
            return False

        print(f"  ✓ PDF created")

        # Move the PDF to final name
        temp_pdf = OUT_DIR / f"{base_name}_temp.pdf"
        final_pdf = OUT_DIR / f"{base_name}.pdf"
        if temp_pdf.exists():
            temp_pdf.rename(final_pdf)

        # Convert PDF to PNG using pdftoppm (part of poppler-utils)
        final_png = OUT_DIR / f"{base_name}.png"

        result = subprocess.run(
            ['pdftoppm', '-png', '-singlefile', '-r', '300', str(final_pdf), str(OUT_DIR / base_name)],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            print(f"  Warning: Could not convert to PNG (pdftoppm not available)")
            print(f"  PDF available at: {final_pdf}")
        else:
            print(f"  ✓ PNG created: {final_png}")

        # Clean up temporary files
        for ext in ['.tex', '.aux', '.log']:
            temp_file = OUT_DIR / f"{base_name}_temp{ext}"
            if temp_file.exists():
                temp_file.unlink()

        return True

    except subprocess.TimeoutExpired:
        print(f"Error: Compilation of {tikz_file} timed out")
        return False
    except FileNotFoundError:
        print("Error: pdflatex not found. Please install LaTeX.")
        sys.exit(1)

def main():
    """Main compilation orchestrator."""
    print("=== TikZ Diagram Compiler ===")

    ensure_out_dir()
    tikz_files = read_tikz_files()

    print(f"\nFound {len(tikz_files)} file(s) to compile:")
    for f in tikz_files:
        print(f"  - {f}")

    success_count = 0
    for tikz_file in tikz_files:
        if compile_tikz(tikz_file):
            success_count += 1

    print(f"\n{'='*50}")
    print(f"Successfully compiled {success_count}/{len(tikz_files)} diagrams")
    print(f"Output location: {OUT_DIR}")

if __name__ == "__main__":
    main()
