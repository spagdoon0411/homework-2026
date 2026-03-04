import numpy as np
import matplotlib.pyplot as plt

# Orbital parameters — eccentricity exaggerated for visual clarity
a = 1.0
e = 0.45          # real Mercury: 0.206
b = a * np.sqrt(1 - e**2)
c = a * e         # focus offset from ellipse center

n_orbits = 5
precession_deg = 26   # degrees per step (real: ~0.01 deg/orbit)

fig, ax = plt.subplots(figsize=(5, 5))
ax.set_aspect('equal')
ax.set_axis_off()

theta = np.linspace(0, 2 * np.pi, 600)

for i in range(n_orbits):
    rot = np.radians(i * precession_deg)

    # Ellipse with one focus at origin, perihelion along +x before rotation
    x = a * np.cos(theta) - c
    y = b * np.sin(theta)

    xr = x * np.cos(rot) - y * np.sin(rot)
    yr = x * np.sin(rot) + y * np.cos(rot)

    frac = i / (n_orbits - 1)
    gray = 0.72 * (1 - frac)           # oldest = light gray, newest = black
    ls = '-'
    lw = 0.25 if i < n_orbits - 1 else 0.5

    ax.plot(xr, yr, color=str(gray), linewidth=lw, linestyle=ls, zorder=2)

    # Perihelion point
    px = (a - c) * np.cos(rot)
    py = (a - c) * np.sin(rot)
    ax.plot(px, py, 'o', color=str(gray), markersize=5, zorder=3)

# Sun
ax.plot(0, 0, 'ko', markersize=11, zorder=5)

ax.autoscale(tight=True)
ax.margins(0.02)

plt.savefig(
    '/Users/spandan/Projects/homework/phys341/zeeman/presentation/perihelion.png',
    dpi=180, bbox_inches='tight', pad_inches=0.05, facecolor='white', edgecolor='none'
)
print("Saved perihelion.png")
