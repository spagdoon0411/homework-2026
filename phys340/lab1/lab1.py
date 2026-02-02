import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import odr
from scipy import stats

df = pd.read_csv("data.csv")

distance_unc = 0.5
df["distance_unc"] = distance_unc * 2 * np.sqrt(2)

df["exit_unc"] = (df["exit_upper"] - df["exit_lower"]) / 2
df["exit"] = (df["exit_upper"] + df["exit_lower"]) / 2
df["return_unc"] = (df["return_upper"] - df["return_lower"]) / 2
df["return"] = (df["return_upper"] + df["return_lower"]) / 2

df["distance"] = df["half_distance"] * 2

df["time"] = df["return"] - df["exit"]
df["time_unc"] = np.sqrt(df["exit_unc"] ** 2 + df["return_unc"] ** 2)


def linear_func(p, x):
    return p[0] * x + p[1]


linear_model = odr.Model(linear_func)
data = odr.RealData(
    df["time"].values,
    df["distance"].values,
    sx=df["time_unc"].values,
    sy=df["distance_unc"].values,
)

initial_guess = [30.0, 0.0]
odr_obj = odr.ODR(data, linear_model, beta0=initial_guess)
output = odr_obj.run()

slope = output.beta[0]
intercept = output.beta[1]
slope_err = output.sd_beta[0]
intercept_err = output.sd_beta[1]

n_obs = len(df)
n_params = 2
dof = n_obs - n_params

# t_68 = stats.norm.ppf(0.84)
# t_95 = stats.norm.ppf(0.975)

t_68 = stats.t.ppf(0.84, dof)
t_95 = stats.t.ppf(0.975, dof)

slope_ci_lower_68 = slope - t_68 * slope_err
slope_ci_upper_68 = slope + t_68 * slope_err
slope_ci_lower_95 = slope - t_95 * slope_err
slope_ci_upper_95 = slope + t_95 * slope_err

intercept_ci_lower_68 = intercept - t_68 * intercept_err
intercept_ci_upper_68 = intercept + t_68 * intercept_err
intercept_ci_lower_95 = intercept - t_95 * intercept_err
intercept_ci_upper_95 = intercept + t_95 * intercept_err

slope_m_s = slope * 1e7
slope_ci_lower_95_m_s = slope_ci_lower_95 * 1e7
slope_ci_upper_95_m_s = slope_ci_upper_95 * 1e7
slope_ci_lower_68_m_s = slope_ci_lower_68 * 1e7
slope_ci_upper_68_m_s = slope_ci_upper_68 * 1e7
intercept_m = intercept / 100
intercept_ci_lower_95_m = intercept_ci_lower_95 / 100
intercept_ci_upper_95_m = intercept_ci_upper_95 / 100
intercept_ci_lower_68_m = intercept_ci_lower_68 / 100
intercept_ci_upper_68_m = intercept_ci_upper_68 / 100

print(
    f"Slope: {slope:.3f} 95% CI: ({slope_ci_lower_95:.3f}, {slope_ci_upper_95:.3f}) 68% CI: ({slope_ci_lower_68:.3f}, {slope_ci_upper_68:.3f}) cm/ns"
)
print(
    f"Intercept: {intercept:.2f} 95% CI: ({intercept_ci_lower_95:.2f}, {intercept_ci_upper_95:.2f}) 68% CI: ({intercept_ci_lower_68:.2f}, {intercept_ci_upper_68:.2f}) cm"
)

plt.figure(figsize=(10, 6))
plt.errorbar(
    df["time"],
    df["distance"],
    xerr=df["time_unc"],
    yerr=df["distance_unc"],
    fmt="o",
    label="Data Points",
    capsize=5,
    ecolor="gray",
    alpha=0.7,
)

x_fit = np.linspace(df["time"].min() - 1, df["time"].max() + 1, 100)
y_fit = linear_func(output.beta, x_fit)

var_slope = output.cov_beta[0, 0]
var_intercept = output.cov_beta[1, 1]
cov_slope_intercept = output.cov_beta[0, 1]

y_fit_var = var_slope * x_fit**2 + var_intercept + 2 * x_fit * cov_slope_intercept
y_fit_std = np.sqrt(y_fit_var)

y_fit_upper_68 = y_fit + t_68 * y_fit_std
y_fit_lower_68 = y_fit - t_68 * y_fit_std
y_fit_upper_95 = y_fit + t_95 * y_fit_std
y_fit_lower_95 = y_fit - t_95 * y_fit_std

plt.plot(x_fit, y_fit, color="red", label="ODR Linear Regression", linewidth=2)
plt.fill_between(
    x_fit,
    y_fit_lower_68,
    y_fit_upper_68,
    color="red",
    alpha=0.3,
    label="68% Confidence Interval",
)
plt.fill_between(
    x_fit,
    y_fit_lower_95,
    y_fit_upper_95,
    color="red",
    alpha=0.15,
    label="95% Confidence Interval",
)

textstr = f"Slope: {slope:.3f} cm/ns\n"
textstr += f"  95% CI: ({slope_ci_lower_95:.3f}, {slope_ci_upper_95:.3f})\n"
textstr += f"  68% CI: ({slope_ci_lower_68:.3f}, {slope_ci_upper_68:.3f})\n"
textstr += f"Slope: {slope_m_s:.2e} m/s\n"
textstr += f"  95% CI: ({slope_ci_lower_95_m_s:.2e}, {slope_ci_upper_95_m_s:.2e})\n"
textstr += f"  68% CI: ({slope_ci_lower_68_m_s:.2e}, {slope_ci_upper_68_m_s:.2e})\n"
textstr += f"Intercept: {intercept:.2f} cm\n"
textstr += f"  95% CI: ({intercept_ci_lower_95:.2f}, {intercept_ci_upper_95:.2f})\n"
textstr += f"  68% CI: ({intercept_ci_lower_68:.2f}, {intercept_ci_upper_68:.2f})\n"
textstr += f"Intercept: {intercept_m:.4f} m\n"
textstr += f"  95% CI: ({intercept_ci_lower_95_m:.4f}, {intercept_ci_upper_95_m:.4f})\n"
textstr += f"  68% CI: ({intercept_ci_lower_68_m:.4f}, {intercept_ci_upper_68_m:.4f})"
plt.text(
    0.05,
    0.95,
    textstr,
    transform=plt.gca().transAxes,
    fontsize=10,
    verticalalignment="top",
    bbox=dict(boxstyle="round", facecolor="white", alpha=0.8),
)

plt.xlabel(r"Time interval $t_i$ (ns)")
plt.ylabel(r"Distance traveled: $2 \cdot d_i$ (cm)")
plt.title("Distance Traveled by Light Pulse vs. Time Interval of Travel")
plt.legend()
plt.grid(True)
plt.savefig("distance_vs_time.png", dpi=300, bbox_inches="tight")
plt.show()
