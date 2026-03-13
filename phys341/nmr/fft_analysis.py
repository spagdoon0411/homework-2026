import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

plt.rcParams["font.size"] = 12

def load_fft_trace(filepath):
    """Load FFT trace data from CSV file."""
    with open(filepath, "r", encoding="utf-8-sig") as f:
        lines = f.readlines()

    # Find the data header line
    start_idx = None
    for i, line in enumerate(lines):
        if "Frequency (Hz)" in line:
            start_idx = i + 1
            break

    if start_idx is None:
        raise ValueError(f"Could not find data header in {filepath}")

    # Read the data
    data = []
    for line in lines[start_idx:]:
        parts = line.strip().split(",")
        if len(parts) >= 2 and parts[0].strip():
            try:
                freq = float(parts[0])
                voltage = float(parts[1])
                data.append([freq, voltage])
            except ValueError:
                continue

    df = pd.DataFrame(data, columns=["frequency", "voltage"])
    return df

def gaussian(x, A, mu, sigma):
    """Gaussian function."""
    return A * np.exp(-((x - mu) ** 2) / (2 * sigma ** 2))

# Load FFT data
fft_file = "phys341/nmr/trace_processing/t2star_traces/3895G_FFTs/FFT 1 2026-02-23 14-34-27.csv"
df = load_fft_trace(fft_file)

freq = df["frequency"].values
voltage = df["voltage"].values

# Convert frequency to MHz for plotting
freq_mhz = freq / 1e6

# Initial guess for Gaussian fit
A0 = np.max(voltage)
mu0 = freq[np.argmax(voltage)]
sigma0 = 0.5e6  # 0.5 MHz initial guess

# Fit Gaussian
popt, pcov = curve_fit(
    gaussian,
    freq,
    voltage,
    p0=[A0, mu0, sigma0],
    maxfev=10000,
)

A, mu, sigma = popt
sigma_A, sigma_mu, sigma_sigma = np.sqrt(np.diag(pcov))

# Calculate FWHM
# FWHM = 2 * sqrt(2 * ln(2)) * sigma
fwhm = 2 * np.sqrt(2 * np.log(2)) * sigma
fwhm_mhz = fwhm / 1e6
mu_mhz = mu / 1e6

print(f"Gaussian fit parameters:")
print(f"  Amplitude A = {A:.6e} V")
print(f"  Mean μ = {mu_mhz:.6f} MHz")
print(f"  Std dev σ = {sigma/1e6:.6f} MHz")
print(f"  FWHM = {fwhm_mhz:.6f} MHz")

# Plot
fig, ax = plt.subplots(figsize=(10, 6))

ax.plot(freq_mhz, voltage, "b-", linewidth=0.8, alpha=0.7, label="Fourier transform of RF signal")

# Plot Gaussian fit
freq_fit = np.linspace(freq.min(), freq.max(), 1000)
voltage_fit = gaussian(freq_fit, A, mu, sigma)
freq_fit_mhz = freq_fit / 1e6

ax.plot(freq_fit_mhz, voltage_fit, "r-", linewidth=2, label="Gaussian fit")

# Add FWHM annotation
fwhm_left = mu_mhz - fwhm_mhz / 2
fwhm_right = mu_mhz + fwhm_mhz / 2
half_max = A / 2

ax.axvspan(fwhm_left, fwhm_right, alpha=0.2, color='red', label=f'FWHM = {fwhm_mhz:.3f} MHz')

# Add RF frequency peak line
ax.axvline(mu_mhz, color='green', linestyle='--', linewidth=1.5, label=f'RF frequency peak: {mu_mhz:.3f} MHz')

ax.set_xlabel("Frequency (MHz)")
ax.set_ylabel("Voltage (V)")
ax.set_title(f"Fourier Transform of a Frequency Pulse")

# Center on peak and show 2x FWHM on either side
x_min = mu_mhz - 2 * fwhm_mhz
x_max = mu_mhz + 2 * fwhm_mhz
ax.set_xlim(x_min, x_max)

ax.legend(fontsize=9)
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("phys341/nmr/out/fft_gaussian_fit.pdf")
plt.close()

print(f"\nPlot saved to phys341/nmr/out/fft_gaussian_fit.pdf")
