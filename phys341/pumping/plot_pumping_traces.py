"""
Plot oscilloscope traces for the optical pumping experiment.

This script is intentionally separate from analyze_gfactor.py.
It reads CSV exports with metadata headers from the scope and
produces a combined figure for all traces found in:
    data/optical_pumping_traces/*.csv
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


ROOT = Path(__file__).parent
TRACE_DIR = ROOT / "data" / "optical_pumping_traces"
OUT_DIR = ROOT / "output"


def load_scope_csv(path: Path) -> pd.DataFrame:
    """Load a Keysight/Agilent scope CSV with metadata preamble."""
    lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
    header_idx = None
    for i, line in enumerate(lines):
        if line.strip().startswith("Sample Number,Time (s),1 (VOLT),2 (VOLT)"):
            header_idx = i
            break
    if header_idx is None:
        raise ValueError(f"Could not find data header in {path.name}")

    df = pd.read_csv(path, skiprows=header_idx)

    # Keep only the scope data columns we care about and coerce numeric.
    cols = ["Sample Number", "Time (s)", "1 (VOLT)", "2 (VOLT)"]
    df = df.loc[:, [c for c in cols if c in df.columns]].copy()
    for c in df.columns:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    df = df.dropna(subset=["Time (s)"]).reset_index(drop=True)
    return df


def main() -> None:
    csv_files = sorted(TRACE_DIR.glob("*.csv"))
    if not csv_files:
        raise FileNotFoundError(f"No CSV traces found in: {TRACE_DIR}")

    OUT_DIR.mkdir(exist_ok=True)

    fig, axes = plt.subplots(
        len(csv_files),
        1,
        figsize=(11, 3.8 * len(csv_files)),
        sharex=False,
    )
    if len(csv_files) == 1:
        axes = [axes]

    for ax, csv_path in zip(axes, csv_files):
        df = load_scope_csv(csv_path)
        t_ms = 1e3 * df["Time (s)"]

        # Plot only CH2, which carries the optical trace.
        ax.plot(t_ms, df["2 (VOLT)"], lw=1.2, label="CH2 (V)")

        ax.set_title(csv_path.stem.replace("_", " "), fontsize=12)
        ax.set_xlabel("Time (ms)")
        ax.set_ylabel("Voltage (V)")
        ax.grid(alpha=0.3)
        ax.legend(loc="best", fontsize=9)

    fig.suptitle("Optical Pumping Oscilloscope Traces", fontsize=14)
    fig.tight_layout(rect=[0, 0, 1, 0.97])

    out_png = OUT_DIR / "pumping_traces.png"
    out_pdf = OUT_DIR / "pumping_traces.pdf"
    fig.savefig(out_png, dpi=300, bbox_inches="tight")
    fig.savefig(out_pdf, dpi=300, bbox_inches="tight")
    print(f"Wrote: {out_png}")
    print(f"Wrote: {out_pdf}")


if __name__ == "__main__":
    main()
