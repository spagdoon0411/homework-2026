import pandas as pd
import scipy.constants as const


# g \mu_N B_0 = hf
# g = hf / (\mu_N B_0)

B_0 = 3895 * 1e-4  # T
mu_N = const.physical_constants["nuclear magneton"][0]  # J/T
df = pd.read_csv("phys341/nmr/frequencies.tsv")

# MHz to Hz
df["rf"] = df["rf"] * 1e6
df["g_factor"] = (const.h * df["rf"]) / (mu_N * B_0)
print(df)
