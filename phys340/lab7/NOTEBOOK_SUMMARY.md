# Lab 7 Final Notebook - Complete Summary

## Overview

Updated gamma ray spectroscopy analysis notebook with proper uncertainty handling, ODR regression, professional data visualization, and LaTeX table generation for reports.

## Key Features Implemented

### 1. Imports and Plot Configuration

- Added matplotlib and scipy.odr imports
- Configured default font sizes for all plot elements (14-18pt)
- Set consistent styling across all figures

### 2. Data Organization

- Defined centroids, FWHM values, known energies, and isotope labels
- All arrays properly structured for vectorized operations

### 3. Uncertainty Calculation

- Centroid uncertainties computed from FWHM: `σ = FWHM / (2√(2ln2))`
- This converts FWHM to standard deviation for Gaussian peaks

### 4. ODR Linear Regression

- Replaced least-squares with Orthogonal Distance Regression (ODR)
- ODR accounts for uncertainties in both x (channel) and y (energy)
- Model: E = slope × Ch + intercept
- Results properly rounded using `round_unc()` function

### 5. Calibration Plot

- Scatter plot with error bars showing calibration points
- Red fitted line from ODR regression
- Regression equation displayed in legend with uncertainties
- Professional formatting with grid, large fonts, proper labels

### 6. Cs-137 Spectrum

- X-axis converted from channels to keV using calibration
- Large, readable plot (12×7 inches)
- Proper axis labels with units
- Title and legend included

### 7. Results DataFrame

- Clean dataframe with separate value and uncertainty columns
- **No LaTeX embedded in the dataframe** (per requirements)
- Columns: Isotope, Known Energy, Channel, Channel Unc, FWHM, FWHM Unc, Est Energy, Est Energy Unc
- All values properly rounded with `round_unc()`
- Easy to work with programmatically

### 8. LaTeX Table Generation

- **Separate cell that generates copy-pastable LaTeX**
- Pulls values from dataframe and formats them properly
- Includes calibration results table
- Includes resolution analysis table
- Ready to paste directly into LaTeX reports
- Example output:

```latex
\begin{table}[h]
\centering
\caption{Gamma Ray Energy Calibration Results}
\begin{tabular}{lcccc}
\hline
Isotope & Known Energy & Channel & FWHM & Estimated Energy \\
 & (keV) & & & (keV) \\
\hline
Co-60 & 1173.2 & $680.0 \pm 13.0$ & $30.0 \pm 1.5$ & $1173.0 \pm 23.0$ \\
...
\end{tabular}
\end{table}
```

### 9. Energy Resolution Analysis

- Calculated FWHM in keV units
- Computed percent resolution for each peak
- Text output with formatted uncertainties
- LaTeX table for resolution data
- Dual plot showing:
  - FWHM vs Energy
  - Percent Resolution vs Energy
  - Color-coded by isotope

## Formulas Used

### Uncertainty Propagation for Energy

For E = m×Ch + b:

```
σ_E = √[(m×σ_Ch)² + (Ch×σ_m)² + σ_b²]
```

### Resolution

```
R (%) = (FWHM / E) × 100%
```

## Cell Organization

0. Imports and configuration
1. Data definition
2. round_unc function
3. ODR regression calculation with printed results
4. Calibration plot with equation in legend
5. Load Cs-137 data and convert to keV
6. Cs-137 spectrum plot
7. Results dataframe (clean, no LaTeX)
8. LaTeX table generation for calibration results
9. Resolution analysis (text output)
10. LaTeX table generation for resolution results
11. Resolution plots

## Design Principles

### Separation of Concerns

- **Dataframe**: Clean numeric data with separate value/uncertainty columns

  - Easy to manipulate programmatically
  - No formatting embedded
  - Clear column names

- **LaTeX Generation**: Separate cells that format data for reports
  - Pulls from dataframe
  - Adds proper LaTeX syntax
  - Copy-pastable output
  - Maintains proper significant figures via round_unc

This design makes it easy to:

- Further analyze the data programmatically
- Generate different table formats
- Update values without touching formatting code
- Copy LaTeX directly into reports

## File Requirements

- cs137.csv must be in the same directory
- Contains columns: intensity (counts per channel)

## Running the Notebook

Execute cells in order. All dependencies are in pyproject.toml:

- numpy, pandas, matplotlib, scipy
- Use `uv run jupyter notebook` to launch

## Results Summary

- **Calibration:** E = (1.761 ± 0.008) keV/Ch + (-24.0 ± 3.0) keV
- **Reduced χ²:** 0.035 (excellent fit)
- **Resolutions:** 4.1-8.3% depending on isotope and energy
- All four calibration sources properly analyzed (Co-60, Ba-133, Cs-137)
