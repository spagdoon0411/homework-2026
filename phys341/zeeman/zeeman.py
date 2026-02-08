#!/usr/bin/env python3
"""Zeeman effect analysis."""

import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
from phys341.utils.rounding import round_unc_pdg

# =============================================================================
# Physical constants (adjust as needed)
# =============================================================================
n_etalon = 1.4567              # Fabry-Perot etalon refractive index
lambda_cd = 643.847e-9          # Cd red line wavelength [m]
g_J = 1.0                      # Landé g-factor (normal Zeeman, S=0)
d_alpha = 0.01                  # Uncertainty in alpha [rad]

# =============================================================================
# Global plot settings
# =============================================================================
FONTSIZE = 12
plt.rcParams.update({
    'font.size': FONTSIZE,
    'axes.titlesize': FONTSIZE + 2,
    'axes.labelsize': FONTSIZE + 1,
    'xtick.labelsize': FONTSIZE - 1,
    'ytick.labelsize': FONTSIZE - 1,
    'legend.fontsize': FONTSIZE - 1,
    'figure.titlesize': FONTSIZE + 3,
})

REPORT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'report')

# =============================================================================
# Part 1: B vs. I calibration fit
# =============================================================================
I_cal = np.array([0.020, 0.231, 0.443, 0.656, 0.868, 1.082, 1.294, 1.508,
                  1.721, 1.933, 2.144, 2.356, 2.567, 2.776, 2.987, 3.079])
dI_cal = 0.001  # [A]

B_cal = np.array([56.00, 184.0, 333.0, 420.0, 490.0, 780.0, 830.0, 980.0,
                  1170, 1380, 1470, 1600, 1710, 1760, 1860, 2100])
dB_cal = 150.0  # [Gauss]

df_cal = pd.DataFrame({'I [A]': I_cal, 'B [Gauss]': B_cal})


def linear(x, m, b):
    return m * x + b


popt_BI, pcov_BI = curve_fit(
    linear, I_cal, B_cal,
    sigma=np.full_like(B_cal, dB_cal),
    absolute_sigma=True,
)
m_BI, b_BI = popt_BI
dm_BI, db_BI = np.sqrt(np.diag(pcov_BI))


def predict_B(I_vals):
    """Return (B, dB) in Gauss from calibration fit."""
    I_vals = np.atleast_1d(I_vals)
    B = linear(I_vals, m_BI, b_BI)
    var_B = (I_vals**2 * pcov_BI[0, 0]
             + pcov_BI[1, 1]
             + 2 * I_vals * pcov_BI[0, 1])
    return B, np.sqrt(var_B)


# Rounded fit parameters for display
m_r, dm_r = round_unc_pdg(m_BI, dm_BI)
b_r, db_r = round_unc_pdg(b_BI, db_BI)

# --- B vs I plot ---
fig, ax = plt.subplots(figsize=(7, 5))
I_line = np.linspace(I_cal.min() - 0.1, I_cal.max() + 0.1, 200)

ax.errorbar(I_cal, B_cal, yerr=dB_cal, xerr=dI_cal,
            fmt='o', capsize=3, label='Calibration data', zorder=5)
ax.plot(I_line, linear(I_line, m_BI, b_BI), 'r-',
        label=(f'Fit: $B = ({m_r} \\pm {dm_r})\\,I'
               f' + ({b_r} \\pm {db_r})$'))

ax.set_xlabel('Current $I$ [A]')
ax.set_ylabel('Magnetic field $B$ [Gauss]')
ax.legend()
fig.tight_layout()
fig.savefig(os.path.join(REPORT_DIR, 'b_vs_i.pdf'))
plt.close(fig)

print(f"B vs I fit:  B = ({m_r} ± {dm_r}) I + ({b_r} ± {db_r})  [Gauss]")
print(f"  slope  = {m_BI:.4f} ± {dm_BI:.4f} Gauss/A")
print(f"  offset = {b_BI:.2f} ± {db_BI:.2f} Gauss")
