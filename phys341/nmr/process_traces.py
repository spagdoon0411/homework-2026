import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from scipy.signal import find_peaks, butter, filtfilt
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

    df = pd.DataFrame(data, columns=["time", "voltage"])
    return df


def lowpass_filter(time, voltage, cutoff_freq, order=4):
    """Apply Butterworth low-pass filter to the signal."""
    dt = np.mean(np.diff(time)) * 1e-3
    fs = 1.0 / dt
    nyquist = fs / 2.0
    normalized_cutoff = cutoff_freq / nyquist

    if normalized_cutoff >= 1.0:
        return voltage

    b, a = butter(order, normalized_cutoff, btype="low", analog=False)
    filtered_voltage = filtfilt(b, a, voltage)
    return filtered_voltage


def exponential_decay(t, A, T2star, offset):
    """Exponential decay function."""
    return A * np.exp(-t / T2star) + offset


def extract_envelope(time, voltage, min_peak_height=None):
    """Extract envelope by finding local maxima."""
    abs_voltage = np.abs(voltage)

    if len(abs_voltage) == 0:
        raise ValueError("No data points in the specified time range")

    if min_peak_height is None:
        min_peak_height = 0.1 * np.max(abs_voltage)

    peaks, _ = find_peaks(abs_voltage, height=min_peak_height, distance=5)

    if len(peaks) == 0:
        min_peak_height = 0.05 * np.max(abs_voltage)
        peaks, _ = find_peaks(abs_voltage, height=min_peak_height, distance=3)

        if len(peaks) == 0:
            raise ValueError("No peaks found in signal")

    return time[peaks], abs_voltage[peaks]


# Load all traces
trace_dirs = {
    "CuSO4": "trace_processing/t2star_traces/CuSO4_Responses",
    "CuSO4-H2O": "trace_processing/t2star_traces/CuSO4H2O_Responses",
    "Glycerin": "trace_processing/t2star_traces/Glycerin_Responses_Spandan",
    "H2O": "trace_processing/t2star_traces/H2O_Responses",
    "Polystyrene": "trace_processing/t2star_traces/Polystyrene_Responses_Spandan",
    "PTFE": "trace_processing/t2star_traces/PTFE_Responses_Spandan",
}

all_traces = []
for substance, dir_path in trace_dirs.items():
    full_path = Path(dir_path)
    csv_files = list(full_path.glob("*.csv"))
    for csv_file in csv_files:
        try:
            trace_df = load_trace(csv_file)
            trace_df["substance"] = substance
            trace_df["filename"] = csv_file.name
            all_traces.append(trace_df)
        except Exception as e:
            print(f"Error loading {csv_file}: {e}")

traces_df = pd.concat(all_traces, ignore_index=True)

# Configuration (time_range in ms)
trace_config = {
    "CuSO4": {
        "trace_index": 1,
        "time_range": (0, 1.0),
        "vertical_shift": -0.02,
        "lowpass_freq": None,
    },
    "CuSO4-H2O": {
        "trace_index": 0,
        "time_range": (-1.3, -0.25),
        "vertical_shift": -0.012,
        "lowpass_freq": None,
    },
    "H2O": {
        "trace_index": 2,
        "time_range": (-0.85, 0.4),
        "vertical_shift": -0.019,
        "lowpass_freq": None,
    },
    "Polystyrene": {
        "trace_index": 3,
        "time_range": (-3.45, -2.8),
        "vertical_shift": -0.01,
        # "lowpass_freq": 120000,
        "lowpass_freq": 80000,
    },
    "Glycerin": {
        "trace_index": 1,
        "time_range": (-3.8, -1.8),
        "vertical_shift": -0.02,
        "lowpass_freq": None,
    },
    "PTFE": {
        "trace_index": 1,
        "time_range": (-2.75, 0),
        "vertical_shift": -0.013,
        "lowpass_freq": None,
    },
}

# Process traces
t2star_results = []
out_dir = Path("out")
out_dir.mkdir(exist_ok=True)

for substance, config in trace_config.items():
    print(f"\nProcessing {substance}...")

    substance_data = traces_df[traces_df["substance"] == substance]
    files = substance_data["filename"].unique()

    if config["trace_index"] >= len(files):
        continue

    selected_file = files[config["trace_index"]]
    file_data = substance_data[substance_data["filename"] == selected_file]

    time = file_data["time"].values * 1e3
    voltage = file_data["voltage"].values

    time_range_ms = config["time_range"]
    time_mask = (time >= time_range_ms[0]) & (time <= time_range_ms[1])
    time_filtered = time[time_mask]
    voltage_filtered = voltage[time_mask]

    if len(time_filtered) == 0:
        continue

    voltage_shifted = voltage_filtered + config["vertical_shift"]

    if config["lowpass_freq"] is not None:
        voltage_processed = lowpass_filter(
            time_filtered, voltage_shifted, config["lowpass_freq"]
        )
    else:
        voltage_processed = voltage_shifted

    try:
        if substance == "PTFE":
            voltage_processed = -voltage_processed
            time_normalized = time_filtered - time_filtered[0]

            A0 = np.max(voltage_processed) - np.min(voltage_processed)
            T2star0 = 0.5
            offset0 = np.min(voltage_processed)

            popt, pcov = curve_fit(
                exponential_decay,
                time_normalized,
                voltage_processed,
                p0=[A0, T2star0, offset0],
                bounds=([0, 0, -np.inf], [np.inf, np.inf, np.inf]),
                maxfev=10000,
            )

            A, T2star, offset = popt
            sigma_T2star = np.sqrt(pcov[1, 1])

            print(f"  T2* = {T2star:.3f} ± {sigma_T2star:.3f} ms")

            t2star_results.append(
                {
                    "substance": substance,
                    "T2star_ms": T2star,
                    "sigma_T2star_ms": sigma_T2star,
                }
            )

            # Plot
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
            fig.suptitle(
                f"$T_2^*$ Analysis for {substance}", fontsize=14, fontweight="bold"
            )

            ax1.plot(
                time_filtered,
                voltage_processed,
                linewidth=0.8,
                alpha=0.7,
                label="Oscilloscope trace",
                color="blue",
            )
            ax1.set_xlabel("Time (ms)")
            ax1.set_ylabel("Voltage (V)")
            ax1.set_title("Oscilloscope Data")
            ax1.grid(True, alpha=0.3)
            ax1.legend()
            ax1.axhline(y=0, color="k", linewidth=0.5, alpha=0.3)

            voltage_fit = exponential_decay(time_normalized, A, T2star, offset)
            ax2.plot(
                time_filtered,
                voltage_processed,
                "o",
                markersize=2,
                alpha=0.4,
                label="Oscilloscope trace",
            )
            ax2.plot(
                time_filtered,
                voltage_fit,
                "r-",
                linewidth=2,
                label="Exponential fit",
            )
            ax2.set_xlabel("Time (ms)")
            ax2.set_ylabel("Voltage (V)")
            ax2.set_title(
                f"Exponential Decay Fit: $T_2^*$ = ({T2star:.3f} $\\pm$ {sigma_T2star:.3f}) ms"
            )
            ax2.grid(True, alpha=0.3)
            ax2.legend()

            plt.tight_layout()
            plt.savefig(f"out/{substance.lower().replace('-', '_')}_t2star.pdf")
            plt.close()

        else:
            envelope_time, envelope_voltage = extract_envelope(
                time_filtered, voltage_processed
            )
            print(f"  Found {len(envelope_time)} envelope peaks")

            A0 = np.max(envelope_voltage)
            T2star0 = 1.0
            offset0 = np.min(envelope_voltage)

            popt, pcov = curve_fit(
                exponential_decay,
                envelope_time,
                envelope_voltage,
                p0=[A0, T2star0, offset0],
                bounds=([0, 0, -np.inf], [np.inf, np.inf, np.inf]),
                maxfev=10000,
            )

            A, T2star, offset = popt
            sigma_T2star = np.sqrt(pcov[1, 1])

            print(f"  T2* = {T2star:.3f} ± {sigma_T2star:.3f} ms")

            t2star_results.append(
                {
                    "substance": substance,
                    "T2star_ms": T2star,
                    "sigma_T2star_ms": sigma_T2star,
                }
            )

            # Plot
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
            fig.suptitle(
                f"$T_2^*$ Analysis for {substance}", fontsize=14, fontweight="bold"
            )

            ax1.plot(
                time_filtered,
                voltage_processed,
                linewidth=0.8,
                alpha=0.7,
                label="Oscilloscope trace",
                color="blue",
            )
            ax1.set_xlabel("Time (ms)")
            ax1.set_ylabel("Voltage (V)")
            ax1.set_title("Oscilloscope Data")
            ax1.grid(True, alpha=0.3)
            ax1.legend()
            ax1.axhline(y=0, color="k", linewidth=0.5, alpha=0.3)

            # Plot processed oscillation data (absolute value) as context
            ax2.plot(
                time_filtered,
                np.abs(voltage_processed),
                "-",
                linewidth=0.8,
                color="gray",
                alpha=0.5,
                label="Processed oscillation data",
            )
            ax2.plot(
                envelope_time,
                envelope_voltage,
                "o",
                markersize=5,
                alpha=0.6,
                label="Envelope peaks",
            )
            time_fit = np.linspace(envelope_time.min(), envelope_time.max(), 1000)
            voltage_fit = exponential_decay(time_fit, A, T2star, offset)
            ax2.plot(time_fit, voltage_fit, "r-", linewidth=2, label="Exponential fit")
            ax2.set_xlabel("Time (ms)")
            ax2.set_ylabel("|Voltage| (V)")
            ax2.set_title(
                f"Exponential Decay Fit: $T_2^*$ = ({T2star:.3f} $\\pm$ {sigma_T2star:.3f}) ms"
            )
            ax2.grid(True, alpha=0.3)
            ax2.legend()

            plt.tight_layout()
            plt.savefig(f"out/{substance.lower().replace('-', '_')}_t2star.pdf")
            plt.close()

    except Exception as e:
        print(f"  ERROR: {e}")

# Save results
t2star_df = pd.DataFrame(t2star_results)
print("\n" + "=" * 60)
print("T2* Results Summary:")
print("=" * 60)
print(t2star_df.to_string(index=False))
t2star_df.to_csv("out/t2star_results.csv", index=False)
