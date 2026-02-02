import pandas as pd
import scipy.constants as const
import matplotlib.pyplot as plt
from scipy import stats
import numpy as np
from scipy.optimize import curve_fit
from sigfig import round


import numpy as np


def round_unc(value, uncertainty, cutoff=2, extract_magnitude=False):
    scalar_input = np.isscalar(value)

    value = np.atleast_1d(value).astype(float)
    uncertainty = np.atleast_1d(uncertainty).astype(float)

    exp = np.floor(np.log10(np.abs(uncertainty)))
    first_digit = (uncertainty / 10**exp).astype(int)
    sigs = np.where(first_digit <= cutoff, 2, 1)

    rounding_decimals = (-exp + (sigs - 1)).astype(int)
    rounded_uncertainty = (
        np.round(uncertainty * 10.0**rounding_decimals) / 10.0**rounding_decimals
    )

    decimals = (-np.floor(np.log10(rounded_uncertainty)) + (sigs - 1)).astype(int)
    rounded_value = np.round(value * 10.0**decimals) / 10.0**decimals

    if extract_magnitude:
        exponent = np.floor(np.log10(np.abs(rounded_value))).astype(int)
        mantissa_value = rounded_value / 10.0**exponent
        mantissa_uncertainty = rounded_uncertainty / 10.0**exponent

        if scalar_input:
            return mantissa_value[0], mantissa_uncertainty[0], exponent[0]
        return mantissa_value, mantissa_uncertainty, exponent

    if scalar_input:
        return rounded_value[0], rounded_uncertainty[0]
    return rounded_value, rounded_uncertainty


voltages_df = pd.read_csv("Stopping Voltages 400.csv")
voltages_df.drop(columns=["filter"], inplace=True)


# def num_round(x: np.ndarray, delta_x: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
#     res = np.vectorize(lambda x, delta_x: round(x, delta_x, cutoff=3))(x, delta_x)
#     ()
#     res = np.array([item.split("±") for item in res])
#     x, delta_x = res[:, 0], res[:, 1]
#     return x.astype(float), delta_x.astype(float)


def gaussian(x, A, mu, sigma):
    return A * np.exp(-((x - mu) ** 2) / (2 * sigma**2))


def find_data_from_spectrometer(filepath):
    df = pd.read_csv(filepath, header=0, names=["wavelength", "intensity"])
    max_intensity = df["intensity"].max()
    max_index = df["intensity"].idxmax()
    max_wavelength = df["wavelength"].iloc[max_index]

    x_data = df["wavelength"]
    y_data = df["intensity"]

    popt, pcov = curve_fit(
        gaussian, x_data, y_data, p0=[max_intensity, x_data[max_index], np.std(x_data)]
    )

    # Generate smooth x values for the fit curve
    # ax1.plot(x_fit, y_fit, "r-", label="Gaussian Fit")

    mu, sigma = popt[1], abs(popt[2])
    lower_bound = mu - sigma
    upper_bound = mu + sigma

    width = upper_bound - lower_bound
    half_width = width / 2

    return {
        "df": df,
        "max_intensity": max_intensity,
        "max_wavelength": max_wavelength,
        "center": mu,
        "width": width,
        "half_width": half_width,
        "lower_bound": lower_bound,
        "upper_bound": upper_bound,
    }


wavelength_labels = [
    # 400,
    455,
    470,
    505,
    525,
    570,
    590,
    604,
    626,
    640,
]
file_paths = [f"spectrometer/{label}.csv" for label in wavelength_labels]

spect_res = []
for i, filepath in enumerate(file_paths):
    result = find_data_from_spectrometer(filepath)
    result.update({"wavelength": wavelength_labels[i]})
    spect_res.append(result)
spect_df = pd.DataFrame(spect_res)
spect_df = spect_df.sort_values("wavelength")


df = pd.merge(spect_df, voltages_df, on="wavelength", how="inner")
df.rename(
    columns={"stopping_voltage_uncertainty": "stopping_voltage_unc"}, inplace=True
)

df["max_wavelength"], df["wavelength_unc"] = round_unc(
    spect_df["max_wavelength"], spect_df["half_width"]
)
df["stopping_voltage"], df["stopping_voltage_unc"] = round_unc(
    df["stopping_voltage"], df["stopping_voltage_unc"]
)

df["-e_delta_v"] = -const.e * (-df["stopping_voltage"])
df["c_over_lambda"] = const.c / (df["max_wavelength"] * 1e-9)

df["-e_delta_v_unc"] = const.e * df["stopping_voltage_unc"]
df["c_over_lambda_unc"] = np.abs(
    const.c / (df["max_wavelength"] * 1e-9) ** 2 * (df["wavelength_unc"] * 1e-9)
)

df["-e_delta_v"], df["-e_delta_v_unc"] = round_unc(
    df["-e_delta_v"], df["-e_delta_v_unc"]
)

df["c_over_lambda"], df["c_over_lambda_unc"] = round_unc(
    df["c_over_lambda"], df["c_over_lambda_unc"]
)

df[["max_wavelength", "lower_bound", "upper_bound", "wavelength_unc"]].to_csv(
    "wavelength_data.csv", index=False
)

df[
    ["max_wavelength", "wavelength_unc", "stopping_voltage", "stopping_voltage_unc"]
].to_csv("wavelength_voltage_data.csv", index=False)

plt.figure(figsize=(15, 9))
slope, intercept, r_value, p_value, std_err = stats.linregress(
    df["c_over_lambda"], df["-e_delta_v"]
)

slope_unc = std_err
n = len(df)
x_mean = df["c_over_lambda"].mean()
x_variance = np.sum((df["c_over_lambda"] - x_mean) ** 2)
intercept_unc = slope_unc * np.sqrt(np.sum(df["c_over_lambda"] ** 2) / n)

slope, slope_unc, slope_exp = round_unc(slope, slope_unc, extract_magnitude=True)
intercept, intercept_unc, intercept_exp = round_unc(
    intercept, intercept_unc, extract_magnitude=True
)

plt.errorbar(
    df["c_over_lambda"],
    df["-e_delta_v"],
    xerr=df["c_over_lambda_unc"],
    yerr=df["-e_delta_v_unc"],
    fmt="o",
    label="Experimental Data",
    capsize=5,
    capthick=2,
    elinewidth=2,
)
plt.plot(
    df["c_over_lambda"],
    intercept * 10.0**intercept_exp + slope * 10.0**slope_exp * df["c_over_lambda"],
    "r",
    label=f"Linear Regression (y = ({slope:.2f}±{slope_unc:.2f}) × 10$^{{{slope_exp}}}$ x + ({intercept:.2f}±{intercept_unc:.2f}) × 10$^{{{intercept_exp}}}$)",
)

plt.xlabel("c/λ (1/s)", fontsize=12)
plt.ylabel("-eΔV (J)", fontsize=12)
plt.title("Photoelectric Effect: -eΔV (J) vs c/λ (1/s)", fontsize=14)
plt.legend()
plt.grid(True)

# plt.text(
#     0.05,
#     0.95,
#     f"Slope (h) = ({slope:.2f} ± {slope_unc:.2f}) × 10$^{{{slope_exp}}}$ J·s\nR² = {r_value**2:.4f}",
#     transform=plt.gca().transAxes,
#     verticalalignment="top",
# )
plt.savefig("photoelectric_effect_plot.png")
plt.tight_layout()
plt.show()
