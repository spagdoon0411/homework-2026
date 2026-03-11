import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

def draw_3d_arrow(ax, start, direction, color='steelblue', alpha=0.8):
    """Draw a 3D arrow with a conical head"""
    # Arrow parameters
    shaft_radius = 0.02
    head_radius = 0.06
    head_length = 0.15

    shaft_length = np.linalg.norm(direction) - head_length

    # Normalize direction
    dir_norm = direction / np.linalg.norm(direction)

    # Draw shaft as a line
    end_of_shaft = start + dir_norm * shaft_length
    ax.plot([start[0], end_of_shaft[0]],
            [start[1], end_of_shaft[1]],
            [start[2], end_of_shaft[2]],
            color=color, linewidth=2, alpha=alpha)

    # Draw cone head
    cone_base = end_of_shaft
    cone_tip = start + direction

    # Create cone
    n_points = 12
    theta = np.linspace(0, 2*np.pi, n_points)

    # Find perpendicular vectors to direction
    if abs(dir_norm[2]) < 0.9:
        perp1 = np.cross(dir_norm, np.array([0, 0, 1]))
    else:
        perp1 = np.cross(dir_norm, np.array([1, 0, 0]))
    perp1 = perp1 / np.linalg.norm(perp1)
    perp2 = np.cross(dir_norm, perp1)
    perp2 = perp2 / np.linalg.norm(perp2)

    # Generate cone surface points
    for i in range(n_points):
        t1 = theta[i]
        t2 = theta[(i + 1) % n_points]

        base1 = cone_base + head_radius * (np.cos(t1) * perp1 + np.sin(t1) * perp2)
        base2 = cone_base + head_radius * (np.cos(t2) * perp1 + np.sin(t2) * perp2)

        # Triangle for cone surface
        verts = [cone_tip, base1, base2]
        tri = Poly3DCollection([verts], alpha=alpha)
        tri.set_facecolor(color)
        tri.set_edgecolor(color)
        ax.add_collection3d(tri)

# Set up the figure with white background
fig = plt.figure(figsize=(6, 6))
ax = fig.add_subplot(111, projection='3d')
ax.set_facecolor('white')
fig.patch.set_facecolor('white')

# Create a lattice of points in the horizontal plane
x_points = np.arange(-2, 3, 1)
y_points = np.arange(-2, 3, 1)
X, Y = np.meshgrid(x_points, y_points)
X = X.flatten()
Y = Y.flatten()
Z = np.zeros_like(X)

# Generate vector components
# All vectors point generally upward (positive z) but with slight variations
np.random.seed(42)  # For reproducibility
n_vectors = len(X)

# Small random deviations in x and y, but mainly pointing up
U = np.random.normal(0, 0.15, n_vectors)
V = np.random.normal(0, 0.15, n_vectors)
W = np.ones(n_vectors) + np.random.normal(0, 0.1, n_vectors)

# Normalize to make vectors similar length
magnitudes = np.sqrt(U**2 + V**2 + W**2)
U = U / magnitudes
V = V / magnitudes
W = W / magnitudes

# Scale down to make arrows shorter
scale = 0.5
U = U * scale
V = V * scale
W = W * scale

# Draw 3D arrows starting at z=0
for i in range(n_vectors):
    start = np.array([X[i], Y[i], Z[i]])
    direction = np.array([U[i], V[i], W[i]])
    draw_3d_arrow(ax, start, direction, color='grey', alpha=0.6)

# Draw central magnetization vector M
# This should be larger and more prominent
m_length = 2.5
m_start = np.array([0, 0, 0])
m_direction = np.array([0, 0, m_length])
draw_3d_arrow(ax, m_start, m_direction, color='steelblue', alpha=0.9)

# Add label for M vector
ax.text(0.2, 0.2, m_length + 0.3, r'$\vec{M}$', fontsize=20, color='steelblue')

# Add label for individual spin vectors at the corner (2, -2)
ax.text(2.5, -2.5, 0.6, r'$\vec{\mu}_k$', fontsize=18, color='grey')

# Clean up the plot
ax.set_xlim([-3, 3])
ax.set_ylim([-3, 3])
ax.set_zlim([0, 3])
ax.set_box_aspect([1, 1, 0.7])

# Remove axis labels and ticks
ax.set_xlabel('')
ax.set_ylabel('')
ax.set_zlabel('')
ax.set_xticks([])
ax.set_yticks([])
ax.set_zticks([])

# Remove grid
ax.grid(False)

# Remove panes
ax.xaxis.pane.fill = False
ax.yaxis.pane.fill = False
ax.zaxis.pane.fill = False

# Set viewing angle
ax.view_init(elev=20, azim=45)

# Save the figure
plt.tight_layout()
plt.savefig('/Users/spandan/Projects/homework/phys341/nmr/presentation/spin_lattice.png',
            dpi=300,
            bbox_inches='tight',
            facecolor='white',
            edgecolor='none')
plt.close()

print("Spin lattice diagram created successfully!")
