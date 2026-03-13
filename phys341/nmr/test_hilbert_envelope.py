import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from scipy.signal import hilbert
from scipy.optimize import curve_fit

plt.rcParams["font.size"] = 12


def load_trace(filepath):
    """Load oscilloscope trace data from CSV file."""
    with open(filepath, "r", encoding="utf-8-sig") as f:
        lines = f.readlines()

    start_idx = None
    for i, line in enumerate(lines):
        if "Analog Channels" in line:
            start_idx = i + 2
            break

    if start_idx is None:
        raise ValueError(f"Could not find 'Analog Channels' in {filepath}")

    data = []
    for line in lines[start_idx:]:
        parts = line.strip().split(",")
        if len(parts) >= 3 and parts[0].strip().isdigit():
            time = float(parts[1])
            voltage = float(parts[2])
            data.append([time, voltage])

    return np.array(data)


def exponential_decay(t, A, T2star, offset):
    """Exponential decay function."""
    return A * np.exp(-t / T2star) + offset


# Load CuSO4 trace
trace_file = "trace_processing/t2star_traces/CuSO4_Responses/CuSO4_B4190 2026-02-25 13-56-43.csv"
data = load_trace(trace_file)
time = data[:, 0] * 1e3
voltage = data[:, 1]

# Select time range (in ms)
time_range = (0, 1.0)
mask = (time >= time_range[0]) & (time <= time_range[1])
time_filtered = time[mask]
voltage_filtered = voltage[mask]

# Remove vertical shift
voltage_shifted = voltage_filtered - 0.02

# Remove DC baseline
dc_baseline = np.mean(voltage_shifted)
voltage_no_dc = voltage_shifted - dc_baseline

# Apply Hilbert transform to get analytic signal
analytic_signal = hilbert(voltage_no_dc)
envelope = np.abs(analytic_signal)

# Normalize time for fitting
time_normalized = time_filtered - time_filtered[0]

# Fit exponential decay to envelope
A0 = np.max(envelope)
T2star0 = 1.0
offset0 = np.min(envelope)

popt, pcov = curve_fit(
    exponential_decay,
    time_normalized,
    envelope,
    p0=[A0, T2star0, offset0],
    bounds=([0, 0, -np.inf], [np.inf, np.inf, np.inf]),
)

A, T2star, offset = popt
sigma_T2star = np.sqrt(pcov[1, 1])

print(f"\nCuSO4 T2* (Hilbert envelope): {T2star:.3f} ± {sigma_T2star:.3f} ms")

# Plot
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 10))

ax1.plot(time_filtered, voltage_shifted, linewidth=0.8, alpha=0.7)
ax1.set_xlabel("Time (ms)")
ax1.set_ylabel("Voltage (V)")
ax1.set_title("Original Signal (DC shifted)")
ax1.grid(True, alpha=0.3)
ax1.axhline(y=0, color="k", linewidth=0.5, alpha=0.3)

ax2.plot(time_filtered, voltage_no_dc, linewidth=0.8, alpha=0.7, label="Signal (DC removed)")
ax2.plot(time_filtered, envelope, "r-", linewidth=1.5, alpha=0.8, label="Hilbert envelope")
ax2.plot(time_filtered, -envelope, "r-", linewidth=1.5, alpha=0.8)
ax2.set_xlabel("Time (ms)")
ax2.set_ylabel("Voltage (V)")
ax2.set_title("Signal with Hilbert Envelope")
ax2.grid(True, alpha=0.3)
ax2.legend()
ax2.axhline(y=0, color="k", linewidth=0.5, alpha=0.3)

voltage_fit = exponential_decay(time_normalized, A, T2star, offset)
ax3.plot(time_filtered, envelope, "o", markersize=2, alpha=0.4, label="Envelope")
ax3.plot(time_filtered, voltage_fit, "r-", linewidth=2, label="Exponential fit")
ax3.set_xlabel("Time (ms)")
ax3.set_ylabel("Envelope (V)")
ax3.set_title(f"Exponential Fit: T2* = ({T2star:.3f} ± {sigma_T2star:.3f}) ms")
ax3.grid(True, alpha=0.3)
ax3.legend()

plt.tight_layout()
plt.savefig("out/test_hilbert_cuso4.pdf")
plt.close()

print("Plot saved to out/test_hilbert_cuso4.pdf")
