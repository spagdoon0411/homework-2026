import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy import constants

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
from phys341.utils.rounding import round_unc_pdg, fmt_val, fmt_sci, fmt_mantissa

# Physical constants
n_etalon = 1.4567  # Fabry-Perot etalon refractive index
t_etalon = 4.0e-3  # Fabry-Perot etalon thickness [m]
lambda_cd = 643.847e-9  # Cd red line wavelength [m]
g_J = 1.0  # Landé g-factor (normal Zeeman, S=0)
d_alpha_deg = 0.01  # Uncertainty in alpha [deg]
d_alpha = np.radians(d_alpha_deg)  # same, in radians

# Global plot settings
FONTSIZE = 12
plt.rcParams.update(
    {
        "font.size": FONTSIZE,
        "axes.titlesize": FONTSIZE + 2,
        "axes.labelsize": FONTSIZE + 1,
        "xtick.labelsize": FONTSIZE - 1,
        "ytick.labelsize": FONTSIZE - 1,
        "legend.fontsize": FONTSIZE - 1,
        "figure.titlesize": FONTSIZE + 3,
    }
)

REPORT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "report")

# Part 1: B vs. I calibration fit
I_cal = np.array(
    [
        0.020,
        0.231,
        0.443,
        0.656,
        0.868,
        1.082,
        1.294,
        1.508,
        1.721,
        1.933,
        2.144,
        2.356,
        2.567,
        2.776,
        2.987,
        3.079,
    ]
)
dI_cal = 0.001  # [A]

B_cal = np.array(
    [
        56.00,
        184.0,
        333.0,
        420.0,
        490.0,
        780.0,
        830.0,
        980.0,
        1170,
        1380,
        1470,
        1600,
        1710,
        1760,
        1860,
        2100,
    ]
)
dB_cal = 150.0  # [Gauss]

df_cal = pd.DataFrame({"I [A]": I_cal, "B [Gauss]": B_cal})


def linear(x, m, b):
    return m * x + b


popt_BI, pcov_BI = curve_fit(
    linear,
    I_cal,
    B_cal,
    sigma=np.full_like(B_cal, dB_cal),
    absolute_sigma=True,
)
m_BI, b_BI = popt_BI
dm_BI, db_BI = np.sqrt(np.diag(pcov_BI))


def predict_B(I_vals):
    """Return (B, dB) in Gauss from calibration fit."""
    I_vals = np.atleast_1d(I_vals)
    B = linear(I_vals, m_BI, b_BI)
    var_B = I_vals**2 * pcov_BI[0, 0] + pcov_BI[1, 1] + 2 * I_vals * pcov_BI[0, 1]
    return B, np.sqrt(var_B)


m_r, dm_r = round_unc_pdg(m_BI, dm_BI)
b_r, db_r = round_unc_pdg(b_BI, db_BI)

fig, ax = plt.subplots(figsize=(7, 5))
I_line = np.linspace(I_cal.min() - 0.1, I_cal.max() + 0.1, 200)

ax.errorbar(
    I_cal,
    B_cal,
    yerr=dB_cal,
    xerr=dI_cal,
    fmt="o",
    capsize=3,
    label="$B$ vs. $I$",
    zorder=5,
)
ax.plot(
    I_line,
    linear(I_line, m_BI, b_BI),
    "r-",
    label=(f"Fit: $B = ({m_r} \\pm {dm_r})\\,I" f" + ({b_r} \\pm {db_r})$"),
)

ax.set_xlabel("Current $I$ [A]")
ax.set_ylabel("Magnetic field $B$ [Gauss]")
ax.legend()
fig.tight_layout()
fig.savefig(os.path.join(REPORT_DIR, "b_vs_i.pdf"))
plt.close(fig)

print(f"B vs I fit:  B = ({m_r} ± {dm_r}) I + ({b_r} ± {db_r})  [Gauss]")
print(f"  slope  = {m_BI:.4f} ± {dm_BI:.4f} Gauss/A")
print(f"  offset = {b_BI:.2f} ± {db_BI:.2f} Gauss")

# Part 2: Alpha measurements — merge left and right
I_meas = np.array([2.411, 2.825, 3.110, 3.431, 3.708, 4.100, 4.321, 4.635, 4.909])

ARight = np.array([0.738, 0.738, 0.743, 0.743, 0.743, 0.749, 0.743, 0.743, 0.749])
AplusRight = np.array([0.781, 0.786, 0.797, 0.807, 0.807, 0.823, 0.823, 0.829, 0.840])
AminusRight = np.array([0.695, 0.684, 0.679, 0.679, 0.674, 0.663, 0.658, 0.652, 0.647])

ALeft = np.array(
    [-0.727, -0.733, -0.733, -0.738, -0.738, -0.743, -0.738, -0.738, -0.743]
)
AplusLeft = np.array(
    [-0.754, -0.778, -0.781, -0.797, -0.802, -0.813, -0.818, -0.823, -0.829]
)
AminusLeft = np.array(
    [-0.679, -0.679, -0.674, -0.668, -0.663, -0.652, -0.647, -0.647, -0.636]
)

alpha_0_deg = (ARight - ALeft) / 2
alpha_plus_deg = (AplusRight - AplusLeft) / 2
alpha_minus_deg = (AminusRight - AminusLeft) / 2

alpha_0 = np.radians(alpha_0_deg)
alpha_plus = np.radians(alpha_plus_deg)
alpha_minus = np.radians(alpha_minus_deg)

B_meas, dB_meas = predict_B(I_meas)

df_alpha = pd.DataFrame(
    {
        "B": B_meas,
        "dB": dB_meas,
        "alpha_minus_deg": alpha_minus_deg,
        "alpha_0_deg": alpha_0_deg,
        "alpha_plus_deg": alpha_plus_deg,
    }
)

rows = []
for _, r in df_alpha.iterrows():
    Br = fmt_val(r["B"], r["dB"])
    a_m = fmt_val(r["alpha_minus_deg"], d_alpha_deg)
    a_0 = fmt_val(r["alpha_0_deg"], d_alpha_deg)
    a_p = fmt_val(r["alpha_plus_deg"], d_alpha_deg)
    rows.append(f"    {Br} & {a_m} & {a_0} & {a_p} \\\\")

alpha_table = (
    "\\begin{table}[H]\n"
    "\\centering\n"
    "\\begin{tabular}{cccc}\n"
    "\\hline\n"
    "    $B$ [Gauss] & $\\alpha_{-}$ [$\\pm 0.01^\\circ$] "
    "& $\\alpha_{0}$ [$\\pm 0.01^\\circ$] "
    "& $\\alpha_{+}$ [$\\pm 0.01^\\circ$] \\\\\n"
    "\\hline\n" + "\n".join(rows) + "\n"
    "\\hline\n"
    "\\end{tabular}\n"
    "\\caption{Merged angular positions of Zeeman-split interference fringes.}\n"
    "\\label{tab:alpha}\n"
    "\\end{table}\n"
)

with open(os.path.join(REPORT_DIR, "table_alpha.tex"), "w") as f:
    f.write(alpha_table)

# Part 3: Snell's law + Zeeman shift → (g_J B ΔM_J , ΔE) dataset
hc_over_lambda = constants.h * constants.c / lambda_cd  # [J]


def snell_beta(alpha, n):
    return np.arcsin(np.sin(alpha) / n)


def d_snell_beta(alpha, n, da):
    beta = snell_beta(alpha, n)
    return np.abs(np.cos(alpha) / (n * np.cos(beta))) * da


def delta_E(beta_f, beta_0):
    return -hc_over_lambda * (np.cos(beta_f) - np.cos(beta_0)) / np.cos(beta_0)


def d_delta_E(beta_f, beta_0, dbf, db0):
    dydBf = hc_over_lambda * np.sin(beta_f) / np.cos(beta_0)
    dydB0 = -hc_over_lambda * np.sin(beta_0) * np.cos(beta_f) / np.cos(beta_0) ** 2
    return np.sqrt(dydBf**2 * dbf**2 + dydB0**2 * db0**2)


beta_0 = snell_beta(alpha_0, n_etalon)
beta_plus = snell_beta(alpha_plus, n_etalon)
beta_minus = snell_beta(alpha_minus, n_etalon)

dbeta_0 = d_snell_beta(alpha_0, n_etalon, d_alpha)
dbeta_plus = d_snell_beta(alpha_plus, n_etalon, d_alpha)
dbeta_minus = d_snell_beta(alpha_minus, n_etalon, d_alpha)

B_T = B_meas * 1e-4  # Gauss → Tesla
dB_T = dB_meas * 1e-4

# σ+  (ΔM_J = +1)
x_plus = g_J * B_T * (+1)
dx_plus = g_J * dB_T
y_plus = delta_E(beta_plus, beta_0)
dy_plus = d_delta_E(beta_plus, beta_0, dbeta_plus, dbeta_0)

# σ−  (ΔM_J = −1)
x_minus = g_J * B_T * (-1)
dx_minus = g_J * dB_T
y_minus = delta_E(beta_minus, beta_0)
dy_minus = d_delta_E(beta_minus, beta_0, dbeta_minus, dbeta_0)

x_all = np.concatenate([x_plus, x_minus])
dx_all = np.concatenate([dx_plus, dx_minus])
y_all = np.concatenate([y_plus, y_minus])
dy_all = np.concatenate([dy_plus, dy_minus])

X_EXP = -1  # g_J B ΔM_J values are ~ 10^{-1} T
Y_EXP = -24  # ΔE values are ~ 10^{-24} J

MJ_labels = np.concatenate([np.ones(len(I_meas)), -np.ones(len(I_meas))])
tidied_rows = []
for xi, dxi, yi, dyi, mj in zip(x_all, dx_all, y_all, dy_all, MJ_labels):
    x_str = f"${fmt_mantissa(xi, dxi, X_EXP)}$"
    y_str = f"${fmt_mantissa(yi, dyi, Y_EXP)}$"
    tidied_rows.append(f"    ${int(mj):+d}$ & {x_str} & {y_str} \\\\")

tidied_table = (
    "\\begin{table}[H]\n"
    "\\centering\n"
    "\\begin{tabular}{ccc}\n"
    "\\hline\n"
    f"    $\\Delta M_J$ & $g_J B \\Delta M_J$ [$\\times 10^{{{X_EXP}}}$ T] "
    f"& $\\Delta E$ [$\\times 10^{{{Y_EXP}}}$ J] \\\\\n"
    "\\hline\n" + "\n".join(tidied_rows) + "\n"
    "\\hline\n"
    "\\end{tabular}\n"
    "\\caption{Zeeman energy shifts and corresponding magnetic field products.}\n"
    "\\label{tab:tidied}\n"
    "\\end{table}\n"
)

with open(os.path.join(REPORT_DIR, "table_tidied.tex"), "w") as f:
    f.write(tidied_table)

beta_0_deg = np.degrees(beta_0)
beta_plus_deg = np.degrees(beta_plus)
beta_minus_deg = np.degrees(beta_minus)
dbeta_0_deg = np.degrees(dbeta_0)
dbeta_plus_deg = np.degrees(dbeta_plus)
dbeta_minus_deg = np.degrees(dbeta_minus)

BETA_DE_EXP = -24  # shared exponent for ΔE columns
beta_rows = []
for i in range(len(I_meas)):
    Br = fmt_val(B_meas[i], dB_meas[i])
    bm = fmt_val(beta_minus_deg[i], dbeta_minus_deg[i])
    b0 = fmt_val(beta_0_deg[i], dbeta_0_deg[i])
    bp = fmt_val(beta_plus_deg[i], dbeta_plus_deg[i])
    # Value-only mantissa for ΔE columns (uncertainties moved to header)
    dEm_val = fmt_mantissa(y_minus[i], dy_minus[i], BETA_DE_EXP).split(" \\pm ")[0]
    dEp_val = fmt_mantissa(y_plus[i], dy_plus[i], BETA_DE_EXP).split(" \\pm ")[0]
    beta_rows.append(f"    {Br} & {bm} & {b0} & {bp} & ${dEm_val}$ & ${dEp_val}$ \\\\")

# Representative uncertainties for two-line headers
dbeta_repr = np.degrees(d_snell_beta(np.radians(0.74), n_etalon, d_alpha))
dEm_unc = fmt_mantissa(y_minus[0], dy_minus[0], BETA_DE_EXP).split(" \\pm ")[1]
dEp_unc = fmt_mantissa(y_plus[0], dy_plus[0], BETA_DE_EXP).split(" \\pm ")[1]

beta_table = (
    "\\begin{table}[H]\n"
    "\\centering\n"
    "\\begin{tabular}{cccccc}\n"
    "\\hline\n"
    f"    \\makecell{{$B$ \\\\ {{[Gauss]}}}} "
    f"& \\makecell{{$\\beta_{{-}}$ \\\\ {{[$\\pm {dbeta_repr:.3f}^\\circ$]}}}} "
    f"& \\makecell{{$\\beta_{{0}}$ \\\\ {{[$\\pm {dbeta_repr:.3f}^\\circ$]}}}} "
    f"& \\makecell{{$\\beta_{{+}}$ \\\\ {{[$\\pm {dbeta_repr:.3f}^\\circ$]}}}} "
    f"& \\makecell{{$\\Delta E_{{-}}$ \\\\ {{[$\\pm {dEm_unc} \\times 10^{{{BETA_DE_EXP}}}$ J]}}}} "
    f"& \\makecell{{$\\Delta E_{{+}}$ \\\\ {{[$\\pm {dEp_unc} \\times 10^{{{BETA_DE_EXP}}}$ J]}}}} \\\\\n"
    "\\hline\n" + "\n".join(beta_rows) + "\n"
    "\\hline\n"
    "\\end{tabular}\n"
    "\\caption{Internal angles $\\beta$ (via Snell's law) and Zeeman energy shifts "
    "for each measurement.}\n"
    "\\label{tab:beta_dE}\n"
    "\\end{table}\n"
)

with open(os.path.join(REPORT_DIR, "table_beta_dE.tex"), "w") as f:
    f.write(beta_table)

# Part 4: Linear fit for μ_B
popt_muB, pcov_muB = curve_fit(
    linear,
    x_all,
    y_all,
    sigma=dy_all,
    absolute_sigma=True,
)
mu_B_exp, intercept_exp = popt_muB
dmu_B_exp, dintercept_exp = np.sqrt(np.diag(pcov_muB))

mu_B_known = constants.physical_constants["Bohr magneton"][0]  # J/T

mu_sci = fmt_sci(mu_B_exp, dmu_B_exp)
int_sci = fmt_sci(intercept_exp, dintercept_exp)

pct_unc = abs(dmu_B_exp / mu_B_exp) * 100

pct_diff = abs(mu_B_exp - mu_B_known) / mu_B_known * 100
n_sigma = abs(mu_B_exp - mu_B_known) / dmu_B_exp

print(f"\nμ_B fit:  {mu_B_exp:.4e} ± {dmu_B_exp:.4e} J/T  ({pct_unc:.1f}% unc)")
print(f"  intercept: {intercept_exp:.4e} ± {dintercept_exp:.4e} J")
print(f"  known μ_B: {mu_B_known:.4e} J/T")
print(f"  % diff from accepted: {pct_diff:.2f}%")
print(f"  sigma from accepted:  {n_sigma:.2f}σ")
print(f"  |intercept/μ_B|:      {abs(intercept_exp / mu_B_exp) * 100:.2f}%")

fig2, ax2 = plt.subplots(figsize=(7, 5))

ax2.errorbar(
    np.abs(x_plus),
    np.abs(y_plus),
    xerr=dx_plus,
    yerr=dy_plus,
    fmt="o",
    capsize=3,
    label="$|\\Delta E|$ vs. $g_J B$, $\\Delta M_J = +1$",
    zorder=5,
)
ax2.errorbar(
    np.abs(x_minus),
    np.abs(y_minus),
    xerr=dx_minus,
    yerr=dy_minus,
    fmt="s",
    capsize=3,
    label="$|\\Delta E|$ vs. $g_J B$, $\\Delta M_J = -1$",
    zorder=5,
)

x_line = np.linspace(0, np.abs(x_all).max(), 200)
FIT_EXP = -24
mu_mant = fmt_mantissa(mu_B_exp, dmu_B_exp, FIT_EXP)
int_mant = fmt_mantissa(intercept_exp, dintercept_exp, FIT_EXP)
ax2.plot(
    x_line,
    linear(x_line, mu_B_exp, intercept_exp),
    "r-",
    label=(
        f"$y = [({mu_mant})\\,\\mathrm{{J/T}}"
        f"\\cdot x"
        f" + ({int_mant})\\,\\mathrm{{J}}]"
        f" \\times 10^{{{FIT_EXP}}}$"
    ),
)

ax2.set_xlabel("$g_J B \\, |\\Delta M_J|$ [T]")
ax2.set_ylabel("$|\\Delta E|$ [J]")
ax2.legend()
fig2.tight_layout()
fig2.savefig(os.path.join(REPORT_DIR, "mu_B_fit.pdf"))
plt.close(fig2)

# Part 5: FSR extrapolation — Higher vs Lower ring difference
ALower = np.array([0.770, 0.791, 0.797, 0.807, 0.807, 0.823, 0.823, 0.829, 0.840])
AHigher = np.array([1.139, 1.139, 1.128, 1.128, 1.128, 1.118, 1.112, 1.107, 1.107])

diff = AHigher - ALower  # [deg]
d_diff = d_alpha_deg * np.sqrt(2)  # propagated uncertainty [deg]

B_fsr, dB_fsr = predict_B(I_meas)  # same currents as alpha measurements

# Linear fit: diff = m_fsr * B + b_fsr  → find B where diff = 0
popt_fsr, pcov_fsr = curve_fit(
    linear,
    B_fsr,
    diff,
    sigma=np.full_like(diff, d_diff),
    absolute_sigma=True,
)
m_fsr, b_fsr = popt_fsr
dm_fsr, db_fsr = np.sqrt(np.diag(pcov_fsr))

# B at which diff = 0:  B_0 = -b_fsr / m_fsr
B_cross = -b_fsr / m_fsr
# Propagate: dB_cross = |B_cross| * sqrt((db/b)^2 + (dm/m)^2)
dB_cross = abs(B_cross) * np.sqrt((db_fsr / b_fsr) ** 2 + (dm_fsr / m_fsr) ** 2)

B_cross_r = fmt_val(B_cross, dB_cross)
dB_cross_r = fmt_val(dB_cross, dB_cross)  # uncertainty rounded to itself

print(f"\nFSR extrapolation:")
print(f"  diff slope:  {m_fsr:.6f} ± {dm_fsr:.6f} deg/Gauss")
print(f"  diff offset: {b_fsr:.4f} ± {db_fsr:.4f} deg")
print(f"  B(diff=0) = {B_cross:.0f} ± {dB_cross:.0f} Gauss")

fsr_rows = []
for i in range(len(I_meas)):
    Br = fmt_val(B_fsr[i], dB_fsr[i])
    lo = fmt_val(ALower[i], d_alpha_deg)
    hi = fmt_val(AHigher[i], d_alpha_deg)
    di = fmt_val(diff[i], d_diff)
    fsr_rows.append(f"    {Br} & {lo} & {hi} & {di} \\\\")

fsr_table = (
    "\\begin{table}[H]\n"
    "\\centering\n"
    "\\begin{tabular}{cccc}\n"
    "\\hline\n"
    f"    $B$ [Gauss] "
    f"& $\\alpha_{{\\mathrm{{lower}}}}$ [$\\pm {d_alpha_deg}^\\circ$] "
    f"& $\\alpha_{{\\mathrm{{higher}}}}$ [$\\pm {d_alpha_deg}^\\circ$] "
    f"& $\\Delta\\alpha$ [$\\pm {d_diff:.3f}^\\circ$] \\\\\n"
    "\\hline\n" + "\n".join(fsr_rows) + "\n"
    "\\hline\n"
    "\\end{tabular}\n"
    "\\caption{Adjacent-ring angular positions and their difference "
    "for FSR extrapolation.}\n"
    "\\label{tab:fsr}\n"
    "\\end{table}\n"
)

with open(os.path.join(REPORT_DIR, "table_fsr.tex"), "w") as f:
    f.write(fsr_table)

fig3, ax3 = plt.subplots(figsize=(7, 5))

ax3.errorbar(
    B_fsr, diff, xerr=dB_fsr, yerr=d_diff, fmt="o", capsize=3, label="$\\Delta\\alpha$ vs. $B$", zorder=5
)

B_line = np.linspace(B_fsr.min() - 200, B_cross + 500, 300)
ax3.plot(B_line, linear(B_line, m_fsr, b_fsr), "r-", label="Linear fit")
ax3.axhline(0, color="gray", ls="--", lw=0.8)
ax3.axvline(
    B_cross,
    color="green",
    ls="--",
    lw=0.8,
    label=f"$B_{{\\mathrm{{FSR}}}} = {B_cross_r} \\pm {dB_cross_r}$ Gauss",
)

ax3.set_xlabel("Magnetic field $B$ [Gauss]")
ax3.set_ylabel("$\\alpha_{\\mathrm{higher}} - \\alpha_{\\mathrm{lower}}$ [deg]")
ax3.legend()
fig3.tight_layout()
fig3.savefig(os.path.join(REPORT_DIR, "fsr_extrapolation.pdf"))
plt.close(fig3)

print("FSR extrapolation plot saved.")

delta_M = 1.0
mu_B_known = constants.physical_constants["Bohr magneton"][0]  # J/T
B_FSR_theory = (
    constants.h
    / mu_B_known
    * constants.c
    / (2 * n_etalon * t_etalon)
    * 1
    / (g_J * delta_M)
)
B_FSR_theory_gauss = B_FSR_theory * 1e4  # T → Gauss

B_FSR_exp = 2 * B_cross
dB_FSR_exp = 2 * dB_cross

print(f"\nB_FSR theoretical: {B_FSR_theory_gauss:.0f} Gauss")
print(
    f"B_FSR experimental (2 × B_cross): "
    f"{fmt_val(B_FSR_exp, dB_FSR_exp)} ± {fmt_val(dB_FSR_exp, dB_FSR_exp)} Gauss"
)
