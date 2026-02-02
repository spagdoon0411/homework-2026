import numpy as np


def round_unc_pdg(value, uncertainty, extract_magnitude=False):
    """
    Round (value, uncertainty) to PDG-style significant digits.

    PDG rule (common implementation):
      - Keep 2 significant digits in the uncertainty if the first two significant
        digits are between 10 and 35 inclusive; otherwise keep 1.
      - Round the central value to the same decimal place as the rounded uncertainty.

    Parameters
    ----------
    value : float or array-like
        Central value(s).
    uncertainty : float or array-like
        Uncertainty(ies). Must be >= 0 for meaningful results.
    extract_magnitude : bool, default False
        If True, return (mantissa_value, mantissa_uncertainty, exponent) such that
        value = mantissa_value * 10**exponent.

    Returns
    -------
    (rounded_value, rounded_uncertainty) or (mantissa_value, mantissa_uncertainty, exponent)
        Scalars in -> scalars out; arrays in -> arrays out.
    """
    scalar_input = np.isscalar(value) and np.isscalar(uncertainty)

    v = np.atleast_1d(value).astype(float)
    u = np.atleast_1d(uncertainty).astype(float)

    if v.shape != u.shape:
        raise ValueError(
            f"value and uncertainty must have the same shape; got {v.shape} vs {u.shape}"
        )

    if np.any(~np.isfinite(v)) or np.any(~np.isfinite(u)):
        raise ValueError("value and uncertainty must be finite (no NaN/Inf).")

    if np.any(u < 0):
        raise ValueError("uncertainty must be >= 0.")

    # Initialize outputs
    rounded_v = v.copy()
    rounded_u = u.copy()

    # Handle u == 0: leave value unchanged and uncertainty 0; magnitude extraction handled later.
    pos_mask = u > 0
    if np.any(pos_mask):
        u_work = u[pos_mask]

        # Exponent of uncertainty
        exp = np.floor(np.log10(u_work)).astype(int)

        # Scale uncertainty into [1, 10)
        scaled = u_work / (10.0**exp)

        # First two significant digits as integer in [10, 99]
        # small epsilon prevents floating artifacts near boundaries (e.g., 3.5 -> 34.9999999)
        first_two = np.floor(scaled * 10.0 + 1e-12).astype(int)

        # PDG: 2 sig digits if 10..35 inclusive, else 1
        sigs = np.where((first_two >= 10) & (first_two <= 35), 2, 1)

        # Round uncertainty to sigs significant digits via scale-and-round
        rounding_decimals_u = (-exp + (sigs - 1)).astype(int)
        factor_u = 10.0**rounding_decimals_u
        u_rounded = np.round(u_work * factor_u) / factor_u

        # After rounding, uncertainty may jump decade (e.g., 0.99 -> 1.0), so recompute decimals
        exp2 = np.floor(np.log10(u_rounded)).astype(int)
        rounding_decimals_v = (-exp2 + (sigs - 1)).astype(int)
        factor_v = 10.0**rounding_decimals_v

        v_rounded = np.round(v[pos_mask] * factor_v) / factor_v

        rounded_u[pos_mask] = u_rounded
        rounded_v[pos_mask] = v_rounded

    if extract_magnitude:
        # Define exponent = 0 for zero values to avoid log10(0).
        exponent = np.zeros_like(rounded_v, dtype=int)
        nz = rounded_v != 0
        exponent[nz] = np.floor(np.log10(np.abs(rounded_v[nz]))).astype(int)

        mantissa_v = rounded_v / (10.0**exponent)
        mantissa_u = rounded_u / (10.0**exponent)

        if scalar_input:
            return mantissa_v[0], mantissa_u[0], exponent[0]
        return mantissa_v, mantissa_u, exponent

    if scalar_input:
        return rounded_v[0], rounded_u[0]
    return rounded_v, rounded_u
