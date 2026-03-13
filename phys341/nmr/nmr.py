import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress
import scipy.constants as const
from phys341.utils.rounding import fmt_pm, fmt_val, fmt_sci

plt.rcParams["font.size"] = 12

# Uncertainties
sigma_B = 50  # Gauss
sigma_f = 1  # MHz

# Constants
h = const.h
mu_N = const.physical_constants["nuclear magneton"][0]


def nuclear_g_factor(mu_in_muN, I):
    if I == 0:
        raise ValueError("Spin quantum number I must be nonzero.")
    return mu_in_muN / I


# F-19 nuclear properties
I_F19 = 0.5  # Nuclear spin quantum number for F-19
mu_F19_in_muN = 2.628868  # F-19 magnetic moment in nuclear magnetons (NIST)
g_F19_theoretical = nuclear_g_factor(mu_F19_in_muN, I_F19)

# Proton (H-1) nuclear properties
g_H1_theoretical = const.physical_constants["proton g factor"][0]

print(f"Theoretical F-19 g-factor: {g_F19_theoretical:.6f}")
print(f"Theoretical H-1 (proton) g-factor: {g_H1_theoretical:.6f}")

samples = {
    "CuSO4": {
        "B": np.array([3660, 3850, 3960, 4190, 4300]),
        "f": np.array([16.18, 16.69, 17.516, 18.46, 18.90]),
    },
    "CuSO4-H2O": {
        "B": np.array([3600, 3760, 3900, 4180, 4310, 4520]),
        "f": np.array([15.83, 16.43, 17.07, 18.27, 18.83, 19.79]),
    },
    "H2O": {
        "B": np.array([3610, 3792, 3910, 4015, 4220]),
        "f": np.array([15.9, 16.69, 17.39, 17.53, 18.40]),
    },
    "Polystyrene": {
        "B": np.array([3974, 4100, 4210, 4380]),
        "f": np.array([17.53, 18.24, 18.29, 19.25]),
    },
    "PTFE": {
        "B": np.array([3950, 4050, 4150, 4250, 4350]),
        "f": np.array([16.11, 16.56, 17.33, 17.55, 18.27]),
    },
    "Glycerin": {
        "B": np.array([3750, 3850, 3950, 4050, 4150]),
        "f": np.array([16.32, 16.98, 17.68, 17.85, 18.10]),
    },
}


results = {}
for name, data in samples.items():
    B_gauss = data["B"]
    f_mhz = data["f"]

    B_tesla = B_gauss * 1e-4
    f_hz = f_mhz * 1e6

    sigma_B_tesla = sigma_B * 1e-4
    sigma_f_hz = sigma_f * 1e6

    y = h * f_hz
    x = mu_N * B_tesla

    sigma_y = h * sigma_f_hz
    sigma_x = mu_N * sigma_B_tesla

    slope, intercept, r_value, p_value, stderr = linregress(x, y)

    g = slope
    sigma_g = stderr

    results[name] = {
        "B_gauss": B_gauss,
        "f_mhz": f_mhz,
        "x": x,
        "y": y,
        "sigma_x": sigma_x,
        "sigma_y": sigma_y,
        "slope": slope,
        "intercept": intercept,
        "stderr": stderr,
        "g": g,
        "sigma_g": sigma_g,
    }


for name, res in results.items():
    plt.figure(figsize=(8, 6))

    plt.errorbar(
        res["x"],
        res["y"],
        xerr=res["sigma_x"],
        yerr=res["sigma_y"],
        fmt="o",
        capsize=5,
        label="Data",
    )

    x_fit = np.linspace(res["x"].min(), res["x"].max(), 100)
    y_fit = res["slope"] * x_fit + res["intercept"]

    g_str = fmt_pm(res["g"], res["sigma_g"])
    fit_label = f"$g = {g_str}$"
    plt.plot(x_fit, y_fit, "r-", label=fit_label)

    plt.xlabel("$\\mu_N B_0$ (J)")
    plt.ylabel("$h\\nu_{\\mathrm{rf}}$ (J)")
    plt.title(f"{name}")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(f"phys341/nmr/out/{name.lower().replace('-', '_')}_fit.pdf")
    plt.close()


with open("phys341/nmr/report/table_summary.tex", "w") as f:
    f.write("\\begin{tabular}{lcc}\n")
    f.write("\\hline\n")
    f.write("Sample & $g$-factor & Deviation from Theory \\\\\n")
    f.write("\\hline\n")
    for name, res in results.items():
        if name == "PTFE":
            g_theoretical = g_F19_theoretical
        else:
            g_theoretical = g_H1_theoretical
        deviation_sigma = (res["g"] - g_theoretical) / res["sigma_g"]
        f.write(
            f"{name} & ${fmt_pm(res['g'], res['sigma_g'])}$ & ${deviation_sigma:.1f}\\sigma$ \\\\\n"
        )
    f.write("\\hline\n")
    f.write("\\end{tabular}\n")


for name, res in results.items():
    filename = f"phys341/nmr/report/table_{name.lower().replace('-', '_')}_data.tex"
    with open(filename, "w") as f:
        f.write("\\begin{tabular}{cc}\n")
        f.write("\\hline\n")
        f.write(
            f"$B_0$ (G, $\\pm$ {sigma_B}) & $\\nu_{{\\mathrm{{rf}}}}$ (MHz, $\\pm$ {sigma_f}) \\\\\n"
        )
        f.write("\\hline\n")
        for b, freq in zip(res["B_gauss"], res["f_mhz"]):
            f.write(f"{b:.0f} & {freq:.2f} \\\\\n")
        f.write("\\hline\n")
        f.write("\\end{tabular}\n")
