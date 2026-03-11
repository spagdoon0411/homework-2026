"""
Predict coil voltages required to cancel Earth's magnetic field components.

This script is intentionally standalone:
- It does not import from the primary analysis script.
- It does not write any files.
- It only prints prediction values to stdout.
"""

import math


# Target Earth-field components (provided)
B_H_NT = 23_647.7  # horizontal component, nT
B_V_NT = 39_800.0  # vertical component, nT

# Horizontal sweep-coil mapping is intentionally matched to analyze_gfactor.py.
N_HORIZONTAL_SWEEP = 11
R_HORIZONTAL_SWEEP_M = 6.46 * 0.0254  # 6.46 inches
R_HORIZONTAL_SWEEP_SENSE_OHM = 1.00

N_VERTICAL = 20
R_VERTICAL_M = 11.7e-2  # 11.7 cm

# Vertical-coil current measurement calibration
R_VERTICAL_SENSE_OHM = 1.00  # V across resistor equals A through coil

MU_0 = 4.0 * math.pi * 1e-7  # T*m/A


def helmholtz_field_per_amp(n_turns: float, radius_m: float) -> float:
    """Return B/I for a Helmholtz pair at midpoint in T/A."""
    return (4.0 / 5.0) ** (3.0 / 2.0) * MU_0 * n_turns / radius_m


def main() -> None:
    # Convert Earth-field components to Tesla
    b_h_t = B_H_NT * 1e-9
    b_v_t = B_V_NT * 1e-9

    # Horizontal sweep coil (exact mapping used in primary analysis script)
    b_per_amp_h = helmholtz_field_per_amp(N_HORIZONTAL_SWEEP, R_HORIZONTAL_SWEEP_M)
    tesla_per_volt_h = b_per_amp_h / R_HORIZONTAL_SWEEP_SENSE_OHM
    v_h_cancel_v = -b_h_t / tesla_per_volt_h
    i_h_cancel_a = v_h_cancel_v / R_HORIZONTAL_SWEEP_SENSE_OHM

    # Vertical coil
    b_per_amp_v = helmholtz_field_per_amp(N_VERTICAL, R_VERTICAL_M)
    i_v_cancel_a = -b_v_t / b_per_amp_v
    v_v_cancel_v = i_v_cancel_a * R_VERTICAL_SENSE_OHM

    print("Predicted cancellation settings for Earth's field:")
    print(f"  B_H = {B_H_NT:,.1f} nT")
    print(f"  B_V = {B_V_NT:,.1f} nT")
    print()

    print("Horizontal sweep coil (primary-script mapping):")
    print(f"  B/I = {b_per_amp_h:.6e} T/A")
    print(f"  B/V = {tesla_per_volt_h:.6e} T/V")
    print(f"  Required current for cancellation: {i_h_cancel_a:+.6f} A")
    print(f"  Predicted sweep-coil voltage for cancellation: {v_h_cancel_v:+.6f} V")
    print()

    print("Vertical coil (Helmholtz model + 1.00 ohm resistor):")
    print(f"  B/I = {b_per_amp_v:.6e} T/A")
    print(f"  Required current for cancellation: {i_v_cancel_a:+.6f} A")
    print(f"  Predicted coil voltage for cancellation: {v_v_cancel_v:+.6f} V")
    print()

    print("Note: negative sign means the applied coil field opposes Earth's field.")


if __name__ == "__main__":
    main()
