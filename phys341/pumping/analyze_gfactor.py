"""
Data analysis for optical pumping g-factor measurements.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
from scipy.optimize import curve_fit
import scipy.constants as const
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.rounding import round_unc_pdg, fmt_pm, fmt_sci, fmt_val

freq_unc_khz = 1  # kHz
volt_unc_v = 0.01  # V

# Helmholtz coil specifications (horizontal sweep coils)
N_coil = 11  # turns per coil
R_coil = 6.46 * 0.0254  # radius in meters (6.46 inches)
R_sense = 1.0  # sense resistor, Ohm

mu_0 = 4 * np.pi * 1e-7  # T*m/A
B_per_amp = (4 / 5) ** (3 / 2) * mu_0 * N_coil / R_coil  # T/A
GAUSS_PER_VOLT = (B_per_amp / R_sense) * 1e4  # G/V
TESLA_PER_VOLT = GAUSS_PER_VOLT * 1e-4  # T/V

print(f"Conversion factor: {GAUSS_PER_VOLT:.4f} G/V\n")

# Earth's field recovery inputs from cancellation settings
V_H_CANCEL_V = 0.45
V_H_CANCEL_UNC_V = 0.05
V_V_CANCEL_V = 0.21
V_V_CANCEL_UNC_V = 0.05
EARTH_B_H_REF_NT = 23_647.7
EARTH_B_V_REF_NT = 39_800.0

N_vertical_coil = 20
R_vertical_coil = 11.7e-2  # meters
R_vertical_sense = 1.0  # Ohm, vertical-coil monitor resistor
B_per_amp_vertical = (
    (4 / 5) ** (3 / 2) * mu_0 * N_vertical_coil / R_vertical_coil
)  # T/A
TESLA_PER_VOLT_VERTICAL = B_per_amp_vertical / R_vertical_sense  # T/V

h = const.h
mu_B = const.value("Bohr magneton")
mu_N = const.value("nuclear magneton")
g_J = 2.00231930436256

mu_I_over_mu_N_87 = 2.751818
mu_I_over_mu_N_85 = 1.353

J = 0.5
I_87 = 1.5
I_85 = 2.5
F_87 = 2.0
F_85 = 3.0


def effective_gI_from_mu_ratio(mu_ratio: float, I: float) -> float:
    """
    Effective nuclear g_I in Bohr-magneton units:
        g_I(effective) = -(mu_I / (I * mu_B))
                        = -(mu_I/mu_N) * (mu_N/mu_B) / I
    """
    return -(mu_ratio / I) * (mu_N / mu_B)


g_I_87 = effective_gI_from_mu_ratio(mu_I_over_mu_N_87, I_87)
g_I_85 = effective_gI_from_mu_ratio(mu_I_over_mu_N_85, I_85)


def calculate_gF_theoretical(F, I, J, g_J, g_I):
    """Calculate theoretical g_F using Breit-Rabi formula."""
    term1 = g_J * (F * (F + 1) - I * (I + 1) + J * (J + 1)) / (2 * F * (F + 1))
    term2 = (
        g_I
        * (mu_N / mu_B)
        * (F * (F + 1) + I * (I + 1) - J * (J + 1))
        / (2 * F * (F + 1))
    )
    return term1 + term2


gF_87_theory = calculate_gF_theoretical(F_87, I_87, J, g_J, g_I_87)
gF_85_theory = calculate_gF_theoretical(F_85, I_85, J, g_J, g_I_85)

data = pd.read_csv(Path(__file__).parent / "g_factor.csv")
freq_khz = data["freq"].values
volt_87 = data["b87_volt"].values
volt_85 = data["b85_volt"].values

freq_hz = freq_khz * 1e3
freq_unc_hz = np.full_like(freq_hz, freq_unc_khz * 1e3)
B_87 = volt_87 * TESLA_PER_VOLT
B_85 = volt_85 * TESLA_PER_VOLT

B_87_unc = np.full_like(volt_87, TESLA_PER_VOLT * volt_unc_v, dtype=float)
B_85_unc = np.full_like(volt_85, TESLA_PER_VOLT * volt_unc_v, dtype=float)


def fit_gfactor(freq, freq_unc, B, B_unc):
    """
    Fit f = (g_F * mu_B / h) * B to extract g_F.
    Returns dict with slope, intercept, g_F, and their uncertainties.
    """
    # Ensure all inputs are 1D arrays
    freq = np.asarray(freq).flatten()
    freq_unc = np.asarray(freq_unc).flatten()
    B = np.asarray(B).flatten()
    B_unc = np.asarray(B_unc).flatten()

    # Initial fit with frequency uncertainties only
    w = 1 / freq_unc**2
    slope_init, intercept_init = np.polyfit(B, freq, 1, w=w)

    # Refine with B uncertainties included
    total_unc = np.sqrt(freq_unc**2 + (slope_init * B_unc) ** 2)
    w_final = 1 / total_unc**2
    slope, intercept = np.polyfit(B, freq, 1, w=w_final)

    # Calculate uncertainties
    y_fit = slope * B + intercept
    residuals = freq - y_fit
    chi2 = np.sum(w_final * residuals**2)
    dof = len(freq) - 2

    S = np.sum(w_final)
    Sx = np.sum(w_final * B)
    Sxx = np.sum(w_final * B**2)
    Delta = S * Sxx - Sx**2

    slope_unc = np.sqrt(S / Delta)
    intercept_unc = np.sqrt(Sxx / Delta)

    g_F = slope * h / mu_B
    g_F_unc = (h / mu_B) * slope_unc

    ss_res = np.sum(residuals**2)
    ss_tot = np.sum((freq - np.mean(freq)) ** 2)
    r_squared = 1 - (ss_res / ss_tot)

    return {
        "slope": slope,
        "slope_unc": slope_unc,
        "intercept": intercept,
        "intercept_unc": intercept_unc,
        "g_F": g_F,
        "g_F_unc": g_F_unc,
        "r_squared": r_squared,
        "chi2": chi2,
        "dof": dof,
    }


fit_87 = fit_gfactor(freq_hz, freq_unc_hz, B_87, B_87_unc)
fit_85 = fit_gfactor(freq_hz, freq_unc_hz, B_85, B_85_unc)

print(f"Rb-87: g_F = {fit_87['g_F']:.6f} ± {fit_87['g_F_unc']:.6f}")
print(f"Rb-85: g_F = {fit_85['g_F']:.6f} ± {fit_85['g_F_unc']:.6f}")


# Generate data table
def generate_data_table():
    freq_unc_header = np.format_float_positional(freq_unc_khz, trim="-")
    volt_unc_header = np.format_float_positional(volt_unc_v, trim="-")
    rows = []
    for i in range(len(freq_khz)):
        B_87_gauss = B_87[i] * 1e4
        B_87_unc_gauss = B_87_unc[i] * 1e4

        B_85_gauss = B_85[i] * 1e4
        B_85_unc_gauss = B_85_unc[i] * 1e4

        freq_s = fmt_val(freq_khz[i], freq_unc_khz)
        volt_87_s = fmt_val(volt_87[i], volt_unc_v)
        volt_85_s = fmt_val(volt_85[i], volt_unc_v)
        b_87_s = fmt_val(B_87_gauss, B_87_unc_gauss)
        b_85_s = fmt_val(B_85_gauss, B_85_unc_gauss)

        rows.append(
            f"    {freq_s} & {volt_87_s} & {b_87_s} & {volt_85_s} & {b_85_s} \\\\"
        )

    table = (
        r"""\begin{tabular}{ccccc}
  \hline
"""
        + f"  Frequency ($\\pm {freq_unc_header}$ kHz) & \\multicolumn{{2}}{{c}}{{Rb-87}} & \\multicolumn{{2}}{{c}}{{Rb-85}} \\\\\n"
        + f"   & Voltage ($\\pm {volt_unc_header}$ V) & $B$ (G) & Voltage ($\\pm {volt_unc_header}$ V) & $B$ (G) \\\\\n"
        + r"""  \hline
"""
        + "\n".join(rows)
        + r"""
  \hline
\end{tabular}"""
    )
    return table


# Generate comparison table
def generate_comparison_table():
    gF_87_r, gF_87_unc_r = round_unc_pdg(fit_87["g_F"], fit_87["g_F_unc"])
    gF_85_r, gF_85_unc_r = round_unc_pdg(fit_85["g_F"], fit_85["g_F_unc"])

    n_sigma_87 = abs(fit_87["g_F"] - gF_87_theory) / fit_87["g_F_unc"]
    n_sigma_85 = abs(fit_85["g_F"] - gF_85_theory) / fit_85["g_F_unc"]

    line1 = f"  $^{{87}}$Rb & ${gF_87_r:.4f} \\pm {gF_87_unc_r:.4f}$ & ${gF_87_theory:.4f}$ & ${n_sigma_87:.2f}\\,\\sigma$ \\\\"
    line2 = f"  $^{{85}}$Rb & ${gF_85_r:.4f} \\pm {gF_85_unc_r:.4f}$ & ${gF_85_theory:.4f}$ & ${n_sigma_85:.2f}\\,\\sigma$ \\\\"

    table = (
        r"""\begin{tabular}{lccc}
  \hline
  Isotope & Experimental $g_F$ & Theoretical $g_F$ & Deviation ($|\Delta|/\sigma$) \\
  \hline
"""
        + line1
        + "\n"
        + line2
        + r"""
  \hline
\end{tabular}"""
    )
    return table


def field_from_voltage(
    voltage_v: float, voltage_unc_v: float, tesla_per_volt: float
) -> tuple[float, float]:
    """Convert cancellation voltage to field magnitude with uncertainty."""
    field_t = abs(voltage_v) * tesla_per_volt
    field_unc_t = tesla_per_volt * voltage_unc_v
    return field_t, field_unc_t


def generate_earth_field_recovery_table() -> str:
    """Generate table of recovered Earth-field components from cancellation voltages."""
    b_h_t, b_h_unc_t = field_from_voltage(
        V_H_CANCEL_V, V_H_CANCEL_UNC_V, TESLA_PER_VOLT
    )
    b_v_t, b_v_unc_t = field_from_voltage(
        V_V_CANCEL_V, V_V_CANCEL_UNC_V, TESLA_PER_VOLT_VERTICAL
    )

    b_h_gauss, b_h_unc_gauss = b_h_t * 1e4, b_h_unc_t * 1e4
    b_v_gauss, b_v_unc_gauss = b_v_t * 1e4, b_v_unc_t * 1e4
    b_h_nt, b_h_unc_nt = b_h_t * 1e9, b_h_unc_t * 1e9
    b_v_nt, b_v_unc_nt = b_v_t * 1e9, b_v_unc_t * 1e9
    n_sigma_h = abs(b_h_nt - EARTH_B_H_REF_NT) / b_h_unc_nt
    n_sigma_v = abs(b_v_nt - EARTH_B_V_REF_NT) / b_v_unc_nt

    b_h_g_r, b_h_g_unc_r = round_unc_pdg(b_h_gauss, b_h_unc_gauss)
    b_v_g_r, b_v_g_unc_r = round_unc_pdg(b_v_gauss, b_v_unc_gauss)
    b_h_nt_r, b_h_nt_unc_r = round_unc_pdg(b_h_nt, b_h_unc_nt)
    b_v_nt_r, b_v_nt_unc_r = round_unc_pdg(b_v_nt, b_v_unc_nt)

    table = (
        r"""\begin{tabular}{lccc}
  \hline
  Component & Recovered field (nT) & Accepted field (nT) & Deviation ($|\Delta|/\sigma$) \\
  \hline
"""
        + f"  $B_H$ & ${b_h_nt_r:.0f} \\pm {b_h_nt_unc_r:.0f}$ & ${EARTH_B_H_REF_NT:.1f}$ & ${n_sigma_h:.2f}\\,\\sigma$ \\\\\n"
        + f"  $B_V$ & ${b_v_nt_r:.0f} \\pm {b_v_nt_unc_r:.0f}$ & ${EARTH_B_V_REF_NT:.1f}$ & ${n_sigma_v:.2f}\\,\\sigma$ \\\\\n"
        + r"""  \hline
\end{tabular}"""
    )
    return table


def generate_earth_field_magnitude_table() -> str:
    """Generate table of recovered vs accepted Earth-field magnitude and dip angle."""
    b_h_t, b_h_unc_t = field_from_voltage(
        V_H_CANCEL_V, V_H_CANCEL_UNC_V, TESLA_PER_VOLT
    )
    b_v_t, b_v_unc_t = field_from_voltage(
        V_V_CANCEL_V, V_V_CANCEL_UNC_V, TESLA_PER_VOLT_VERTICAL
    )

    b_h_nt, b_h_unc_nt = b_h_t * 1e9, b_h_unc_t * 1e9
    b_v_nt, b_v_unc_nt = b_v_t * 1e9, b_v_unc_t * 1e9

    b_mag = np.hypot(b_h_nt, b_v_nt)
    b_mag_unc = np.sqrt((b_h_nt * b_h_unc_nt) ** 2 + (b_v_nt * b_v_unc_nt) ** 2) / b_mag

    theta = np.degrees(np.arctan2(b_v_nt, b_h_nt))
    dtheta_dbh = -b_v_nt / (b_h_nt**2 + b_v_nt**2)
    dtheta_dbv = b_h_nt / (b_h_nt**2 + b_v_nt**2)
    theta_unc = np.degrees(
        np.sqrt((dtheta_dbh * b_h_unc_nt) ** 2 + (dtheta_dbv * b_v_unc_nt) ** 2)
    )

    b_ref_h = EARTH_B_H_REF_NT
    b_ref_v = EARTH_B_V_REF_NT
    b_ref_mag = np.hypot(b_ref_h, b_ref_v)
    theta_ref = np.degrees(np.arctan2(b_ref_v, b_ref_h))

    n_sigma_mag = abs(b_mag - b_ref_mag) / b_mag_unc
    n_sigma_theta = abs(theta - theta_ref) / theta_unc

    b_mag_r, b_mag_unc_r = round_unc_pdg(b_mag, b_mag_unc)
    theta_r, theta_unc_r = round_unc_pdg(theta, theta_unc)

    table = (
        r"""\begin{tabular}{lccc}
  \hline
  Quantity & Recovered & Accepted & Deviation ($|\Delta|/\sigma$) \\
  \hline
"""
        + f"  $|\\mathbf{{B}}|$ (nT) & ${b_mag_r:.0f} \\pm {b_mag_unc_r:.0f}$ & ${b_ref_mag:.1f}$ & ${n_sigma_mag:.2f}\\,\\sigma$ \\\\\n"
        + f"  Dip angle $\\theta$ ($^\\circ$) & ${theta_r:.1f} \\pm {theta_unc_r:.1f}$ & ${theta_ref:.1f}$ & ${n_sigma_theta:.2f}\\,\\sigma$ \\\\\n"
        + r"""  \hline
\end{tabular}"""
    )
    return table


# Write tables
output_dir = Path(__file__).parent / "output"
output_dir.mkdir(exist_ok=True)

with open(output_dir / "gfactor_data_table.tex", "w") as f:
    f.write(generate_data_table())

with open(output_dir / "gfactor_comparison_table.tex", "w") as f:
    f.write(generate_comparison_table())

with open(output_dir / "earth_field_recovery_table.tex", "w") as f:
    f.write(generate_earth_field_recovery_table())

with open(output_dir / "earth_field_magnitude_table.tex", "w") as f:
    f.write(generate_earth_field_magnitude_table())

# Generate plots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

B_87_gauss = B_87 * 1e4
B_87_unc_gauss = B_87_unc * 1e4
freq_khz_vals = freq_hz / 1e3
freq_khz_unc = freq_unc_hz[0] / 1e3

ax1.errorbar(
    B_87_gauss,
    freq_khz_vals,
    xerr=B_87_unc_gauss,
    yerr=freq_khz_unc,
    fmt="o",
    capsize=3,
    label="Resonant field data",
    color="#1f77b4",
)

B_fit_87 = np.linspace(B_87.min(), B_87.max(), 100)
freq_fit_87 = (fit_87["slope"] * B_fit_87 + fit_87["intercept"]) / 1e3

# Slope in kHz/G and intercept in kHz
slope_87_khz_per_g = fit_87["slope"] / 1e3 * 1e-4  # Hz/T to kHz/G
intercept_87_khz = fit_87["intercept"] / 1e3

ax1.plot(
    B_fit_87 * 1e4,
    freq_fit_87,
    "-",
    label=f"$f = ({slope_87_khz_per_g:.3f}\\,\\mathrm{{kHz/G}})\\,B + ({intercept_87_khz:.1f}\\,\\mathrm{{kHz}})$",
    color="#ff7f0e",
)

ax1.set_xlabel("Resonant Magnetic Field $B$ (G)", fontsize=14)
ax1.set_ylabel("RF Frequency $f$ (kHz)", fontsize=14)
ax1.set_title(
    "$^{87}$Rb ($F=2$)\n$g_F = " + fmt_pm(fit_87["g_F"], fit_87["g_F_unc"]) + "$",
    fontsize=15,
    pad=10,
)
ax1.legend(fontsize=12)
ax1.grid(True, alpha=0.3)

B_85_gauss = B_85 * 1e4
B_85_unc_gauss = B_85_unc * 1e4

ax2.errorbar(
    B_85_gauss,
    freq_khz_vals,
    xerr=B_85_unc_gauss,
    yerr=freq_khz_unc,
    fmt="o",
    capsize=3,
    label="Resonant field data",
    color="#2ca02c",
)

B_fit_85 = np.linspace(B_85.min(), B_85.max(), 100)
freq_fit_85 = (fit_85["slope"] * B_fit_85 + fit_85["intercept"]) / 1e3

# Slope in kHz/G and intercept in kHz
slope_85_khz_per_g = fit_85["slope"] / 1e3 * 1e-4  # Hz/T to kHz/G
intercept_85_khz = fit_85["intercept"] / 1e3

ax2.plot(
    B_fit_85 * 1e4,
    freq_fit_85,
    "-",
    label=f"$f = ({slope_85_khz_per_g:.3f}\\,\\mathrm{{kHz/G}})\\,B + ({intercept_85_khz:.1f}\\,\\mathrm{{kHz}})$",
    color="#d62728",
)

ax2.set_xlabel("Resonant Magnetic Field $B$ (G)", fontsize=14)
ax2.set_ylabel("RF Frequency $f$ (kHz)", fontsize=14)
ax2.set_title(
    "$^{85}$Rb ($F=3$)\n$g_F = " + fmt_pm(fit_85["g_F"], fit_85["g_F_unc"]) + "$",
    fontsize=15,
    pad=10,
)
ax2.legend(fontsize=12)
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(output_dir / "gfactor_fits.pdf", dpi=300, bbox_inches="tight")
plt.savefig(output_dir / "gfactor_fits.png", dpi=300, bbox_inches="tight")


def load_scope_csv(path: Path) -> pd.DataFrame:
    """Load scope CSV that contains a metadata preamble before data."""
    lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
    header_idx = None
    for i, line in enumerate(lines):
        if line.strip().startswith("Sample Number,Time (s),1 (VOLT),2 (VOLT)"):
            header_idx = i
            break
    if header_idx is None:
        raise ValueError(f"Could not find data header in {path}")

    df = pd.read_csv(path, skiprows=header_idx)
    df["Time (s)"] = pd.to_numeric(df["Time (s)"], errors="coerce")
    df["2 (VOLT)"] = pd.to_numeric(df["2 (VOLT)"], errors="coerce")
    df = df.dropna(subset=["Time (s)", "2 (VOLT)"]).reset_index(drop=True)
    return df


def exp_recovery(
    t_ms: np.ndarray, c: float, a: float, tau_ms: float, t0_ms: float
) -> np.ndarray:
    """Single-exponential recovery model."""
    return c + a * np.exp(-(t_ms - t0_ms) / tau_ms)


def fit_recovery_tau(scope_csv_path: Path) -> dict:
    """
    Fit CH2 trace in the 0--100 ms window to extract characteristic time.
    Model: V(t) = c + a exp(-(t-t0)/tau)
    """
    df = load_scope_csv(scope_csv_path)
    t_ms_all = 1e3 * df["Time (s)"].to_numpy()
    v2_all = df["2 (VOLT)"].to_numpy()

    mask = (t_ms_all >= 0.0) & (t_ms_all <= 100.0)
    t_ms = t_ms_all[mask]
    v2 = v2_all[mask]
    if len(t_ms) < 10:
        raise ValueError(
            f"Not enough points in 0--100 ms window for {scope_csv_path.name}"
        )

    t0_ms = float(t_ms[0])
    c0 = float(v2[-1])
    a0 = float(v2[0] - v2[-1])
    tau0 = 20.0

    def model(t, c, a, tau):
        return exp_recovery(t, c, a, tau, t0_ms)

    popt, pcov = curve_fit(
        model,
        t_ms,
        v2,
        p0=[c0, a0, tau0],
        bounds=([-np.inf, -np.inf, 1e-6], [np.inf, np.inf, np.inf]),
        maxfev=20000,
    )
    c_fit, a_fit, tau_fit_ms = popt
    perr = np.sqrt(np.diag(pcov))
    tau_unc_ms = float(perr[2]) if np.isfinite(perr[2]) else np.nan

    return {
        "t_ms": t_ms,
        "v2": v2,
        "c": float(c_fit),
        "a": float(a_fit),
        "tau_ms": float(tau_fit_ms),
        "tau_unc_ms": tau_unc_ms,
        "t0_ms": t0_ms,
        "source": scope_csv_path.name,
    }


# Fit exponential recovery traces
trace_dir = Path(__file__).parent / "data" / "optical_pumping_traces"
fit_rec_85 = fit_recovery_tau(trace_dir / "r85_pumping_time.csv")
fit_rec_87 = fit_recovery_tau(trace_dir / "r87_pumping_time.csv")

print(
    f"Rb-87 recovery tau = {fit_rec_87['tau_ms']:.3f} ± {fit_rec_87['tau_unc_ms']:.3f} ms"
)
print(
    f"Rb-85 recovery tau = {fit_rec_85['tau_ms']:.3f} ± {fit_rec_85['tau_unc_ms']:.3f} ms"
)


def generate_recovery_table() -> str:
    tau_87_r, tau_87_unc_r = round_unc_pdg(
        fit_rec_87["tau_ms"], fit_rec_87["tau_unc_ms"]
    )
    tau_85_r, tau_85_unc_r = round_unc_pdg(
        fit_rec_85["tau_ms"], fit_rec_85["tau_unc_ms"]
    )

    table = (
        r"""\begin{tabular}{lc}
  \hline
  Isotope & Pumping time $\tau$ (ms) \\
  \hline
"""
        + f"  $^{{87}}$Rb & ${tau_87_r:.3f} \\pm {tau_87_unc_r:.3f}$ \\\\\n"
        + f"  $^{{85}}$Rb & ${tau_85_r:.3f} \\pm {tau_85_unc_r:.3f}$ \\\\\n"
        + r"""  \hline
\end{tabular}"""
    )
    return table


with open(output_dir / "pumping_time_table.tex", "w") as f:
    f.write(generate_recovery_table())

# Plot recovery fits with style matching g-factor fit plots
fig2, (axr1, axr2) = plt.subplots(1, 2, figsize=(12, 5))

axr1.plot(
    fit_rec_87["t_ms"],
    fit_rec_87["v2"],
    "o",
    markersize=4,
    label="Sweep field strength vs. transmission signal",
    color="#1f77b4",
)
tfit87 = np.linspace(fit_rec_87["t_ms"].min(), fit_rec_87["t_ms"].max(), 400)
vfit87 = exp_recovery(
    tfit87, fit_rec_87["c"], fit_rec_87["a"], fit_rec_87["tau_ms"], fit_rec_87["t0_ms"]
)
axr1.plot(
    tfit87,
    vfit87,
    "-",
    label=r"$V(t)=c + a e^{-(t-t_0)/\tau}$",
    color="#ff7f0e",
)
axr1.set_xlabel("Time $t$ (ms)", fontsize=14)
axr1.set_ylabel("CH2 Voltage (V)", fontsize=14)
axr1.set_title(
    "$^{87}$Rb recovery\n$\\tau = "
    + fmt_pm(fit_rec_87["tau_ms"], fit_rec_87["tau_unc_ms"])
    + r"\,\mathrm{ms}$",
    fontsize=15,
    pad=10,
)
axr1.legend(fontsize=12)
axr1.grid(True, alpha=0.3)

axr2.plot(
    fit_rec_85["t_ms"],
    fit_rec_85["v2"],
    "o",
    markersize=4,
    label="Sweep field strength vs. transmission signal",
    color="#2ca02c",
)
tfit85 = np.linspace(fit_rec_85["t_ms"].min(), fit_rec_85["t_ms"].max(), 400)
vfit85 = exp_recovery(
    tfit85, fit_rec_85["c"], fit_rec_85["a"], fit_rec_85["tau_ms"], fit_rec_85["t0_ms"]
)
axr2.plot(
    tfit85,
    vfit85,
    "-",
    label=r"$V(t)=c + a e^{-(t-t_0)/\tau}$",
    color="#d62728",
)
axr2.set_xlabel("Time $t$ (ms)", fontsize=14)
axr2.set_ylabel("CH2 Voltage (V)", fontsize=14)
axr2.set_title(
    "$^{85}$Rb recovery\n$\\tau = "
    + fmt_pm(fit_rec_85["tau_ms"], fit_rec_85["tau_unc_ms"])
    + r"\,\mathrm{ms}$",
    fontsize=15,
    pad=10,
)
axr2.legend(fontsize=12)
axr2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(output_dir / "recovery_fits.pdf", dpi=300, bbox_inches="tight")
plt.savefig(output_dir / "recovery_fits.png", dpi=300, bbox_inches="tight")
