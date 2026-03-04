import numpy as np
import matplotlib.pyplot as plt
from scipy.special import genlaguerre, lpmv, factorial

def R_nl(n, l, r):
    rho = 2 * r / n
    norm = np.sqrt((2 / n)**3 * factorial(n - l - 1) / (2 * n * factorial(n + l)))
    L = genlaguerre(n - l - 1, 2 * l + 1)
    return norm * np.exp(-r / n) * rho**l * L(rho)

def Y_squared(l, m, theta):
    abs_m = abs(m)
    norm = (2 * l + 1) / (4 * np.pi) * factorial(l - abs_m) / factorial(l + abs_m)
    P = lpmv(abs_m, l, np.cos(theta))
    return norm * P**2

def prob_density_xz(n, l, m, X, Z):
    r = np.sqrt(X**2 + Z**2)
    r = np.where(r < 1e-12, 1e-12, r)
    theta = np.arccos(np.clip(Z / r, -1, 1))
    return R_nl(n, l, r)**2 * Y_squared(l, m, theta)

states = [
    (2, 1, 0), (3, 1, 0), (3, 2, 0), (3, 2, 2),
]

N = 500
lim = 40
x = np.linspace(-lim, lim, N)
z = np.linspace(-lim, lim, N)
X, Z = np.meshgrid(x, z)

fig, axes = plt.subplots(1, 4, figsize=(13, 2.0),
                         gridspec_kw={'wspace': 0.03})

for ax, (n, l, m) in zip(axes, states):
    prob = prob_density_xz(n, l, m, X, Z)
    prob_vis = prob**0.38

    ax.imshow(prob_vis, extent=[-lim, lim, -lim, lim],
              cmap='Greys', origin='lower', aspect='equal',
              interpolation='bilinear')
    ax.set_title(rf'$(n,\ell,m)=({n},{l},{m})$', color='black',
                 fontsize=10, fontfamily='DejaVu Sans', pad=4)
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)

fig.patch.set_facecolor('white')
plt.savefig(
    '/Users/spandan/Projects/homework/phys341/zeeman/presentation/hydrogen_orbitals.png',
    dpi=180, bbox_inches='tight', pad_inches=0.05,
    facecolor='white', edgecolor='none'
)
print("Saved hydrogen_orbitals.png")
