Below is a clean, structured summary of the **rubidium emission (and corresponding absorption) lines relevant to your optical pumping experiment**. This is formatted for direct copy-paste into a lab report.

---

# Rubidium Emission Lines Relevant to Optical Pumping

## 1. Fine Structure Transitions (D-Lines)

Rubidium optical pumping uses the D-lines, which arise from electric dipole transitions:

[
5S_{1/2} \rightarrow 5P_{J}
]

### D1 Line (used in this experiment)

- **Transition:**
  [
  5S_{1/2} \rightarrow 5P_{1/2}
  ]
- **Wavelength:** 794.8 nm
- **Frequency:** ~377 THz
- **Type:** Electric dipole (E1) allowed
- **Selection rules:**
  - ( \Delta L = \pm 1 )
  - ( \Delta J = 0, \pm 1 ) (but not (0 \to 0))
  - ( \Delta m_J = 0, \pm 1 )

This is the line used in your apparatus (794.8 nm bandpass filter).

---

### D2 Line (not primarily used here)

- **Transition:**
  [
  5S_{1/2} \rightarrow 5P_{3/2}
  ]
- **Wavelength:** 780.2 nm
- **Type:** Electric dipole (E1)

This line is emitted by the Rb lamp but filtered out in the optical pumping experiment.

---

# 2. Hyperfine Structure of Ground and Excited States

Hyperfine structure arises from coupling:

[
\mathbf{F} = \mathbf{I} + \mathbf{J}
]

---

## Rb-85

- Nuclear spin: ( I = 5/2 )

### Ground State: (5S\_{1/2}) (J = 1/2)

[
F = 2, 3
]

- Hyperfine splitting ≈ 3.035 GHz

### Excited State: (5P\_{1/2}) (J = 1/2)

[
F' = 2, 3
]

---

## Rb-87

- Nuclear spin: ( I = 3/2 )

### Ground State: (5S\_{1/2}) (J = 1/2)

[
F = 1, 2
]

- Hyperfine splitting ≈ 6.835 GHz

### Excited State: (5P\_{1/2})

[
F' = 1, 2
]

---

# 3. Allowed Hyperfine Optical Transitions (D1 Line)

Electric dipole selection rules:

[
\Delta F = 0, \pm 1 \quad (\text{but not } 0 \to 0)
]

[
\Delta m_F = 0, \pm 1
]

---

## Rb-85 D1 Transitions

From ground (F=3):

- ( F=3 \rightarrow F'=2 )
- ( F=3 \rightarrow F'=3 )

From ground (F=2):

- ( F=2 \rightarrow F'=2 )
- ( F=2 \rightarrow F'=3 )

---

## Rb-87 D1 Transitions

From ground (F=2):

- ( F=2 \rightarrow F'=1 )
- ( F=2 \rightarrow F'=2 )

From ground (F=1):

- ( F=1 \rightarrow F'=1 )
- ( F=1 \rightarrow F'=2 )

---

# 4. Zeeman Splitting in Magnetic Field

In an applied magnetic field (B), each hyperfine level splits into:

[
m_F = -F, \dots, +F
]

Energy shift (linear Zeeman regime):

[
\Delta E = g_F \mu_B m_F B
]

where:

[
g_F =
g_J
\frac{F(F+1)+J(J+1)-I(I+1)}
{2F(F+1)}
]

Typical values:

- Rb-87 (F=2): ( g_F \approx +1/2 )
- Rb-85 (F=3): ( g_F \approx +1/3 )

---

# 5. RF (Magnetic Dipole) Transitions

RF depumping drives:

[
\Delta m_F = \pm 1
]

Resonance condition:

[
h\nu = g_F \mu_B B
]

Typical frequencies in this experiment:
[
\nu \sim 50\text{–}200 \text{ kHz}
]

These transitions occur **within a fixed hyperfine level**.

---

# 6. Optical Pumping Transition of Interest

For right circularly polarized light:

[
\Delta m_F = +1
]

Atoms are pumped toward the stretched states:

- Rb-85: ( |F=3, m_F=+3\rangle )
- Rb-87: ( |F=2, m_F=+2\rangle )

These states cannot absorb further D1 photons because no excited state with (m_F+1) exists.

This produces transparency.

---

If you would like, I can next provide a compact energy-level diagram in LaTeX format suitable for inclusion in a report.
