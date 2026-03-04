---
marp: true
theme: default
math: katex
---

<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Serif:wght@400;700&display=swap');
section {
  font-family: "IBM Plex Serif", serif;
  font-size: 22px;
  justify-content: flex-start !important;
  align-items: flex-start !important;
  padding-top: 120px;
}
h1 {
  position: absolute;
  top: 60px;
  left: 75px;
  right: 75px;
  font-size: 1.6em;
  color: #111;
}
section.title h1 { position: static; margin-bottom: 0.1em; }
section.title { justify-content: center !important; padding-top: 0; }
h2, h3 { color: #111; }
h2 { font-size: 1.2em; }
section.roadmap h2 { font-size: 1.8em; }
a { color: #444; }
table { margin: 0 auto; }
.columns {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2em;
  align-items: start;
}
.columns.wide-right {
  grid-template-columns: 1fr 2fr;
}
.columns ul {
  text-align: left;
}
.columns + .columns {
  margin-top: 0.8em;
}
.columns.eq-row {
  align-items: center;
}
.columns > div > *:first-child {
  margin-top: 0;
}
.columns img {
  display: block;
}
.columns .katex-display {
  font-size: 1.1em;
  overflow: visible;
}
</style>

<!-- _class: title -->

# Verification of Zeeman Effect Theory

## via a Fabry-Pérot Interferometer

</br>
</br>

**Spandan Suthar**
PHYS 341, Winter 2026

---

# Mercury's Perihelion Precession

<div class="columns">
<div>

</br>
</br>

**Mercury's orbital precession** comes from other planets' gravitational pulls.

> Two-body Kepler problems are exactly solvable. 3-body and $n$-body problems exhibit chaos.

</br>

**Perturbation theory:**

1. Solve the unperturbed problem first.
2. Add small terms to the Hamiltonian.
3. Observe new, complex behaviors.

</div>
<div>

![w:100%](perihelion.png)

</div>
</div>

---

# From Planets to Magnetic Fields

<div class="columns eq-row">
<div>

$$H = H_{\text{Kepler}} - \boxed{\sum_i \frac{Gmm_i}{|\vec{r} - \vec{r}_i|}}$$

</div>
<div>

$$\hat{H} = \hat{H}_0 - \boxed{\hat{\boldsymbol{\mu}} \cdot \mathbf{B}}$$

</div>
</div>

<div class="columns">
<div>

Classical: Mercury

- System: Kepler orbit around the Sun
- Perturbation: Gravitational pull of other planets
- Effect: Perihelion (closest approach) precession

</div>
<div>

Quantum: Cadmium Potential Well

- System: Energy levels of a cadmium atom
- Perturbation: Weak magnetic field $\vec{B}$
- Effect: Degeneracy splitting (Zeeman effect)

</div>
</div>

---

# Quantum Numbers and Atomic States

</br>

![w:100%](hydrogen_orbitals.png)

| Quantum number           | Symbol | Operator             | Range                             |
| ------------------------ | ------ | -------------------- | --------------------------------- |
| Spin                     | $S$    | $\hat{\mathbf{S}}^2$ | $0,\, \tfrac{1}{2},\, 1,\, \dots$ |
| Orbital angular momentum | $L$    | $\hat{\mathbf{L}}^2$ | $0,\, 1,\, 2,\, \dots$            |
| Total angular momentum   | $J$    | $\hat{\mathbf{J}}^2$ | $\|L - S\|,\, \dots,\, L + S$     |
| Magnetic                 | $M_J$  | $\hat{J}_z$          | $-J,\, \dots,\, J$                |

</br>

---

# Selection Rules

$$(\gamma, L, S, J, M_J) \;\xrightarrow{\pm \text{ photon}}\; (\gamma', L', S, J', M_J')$$

</br>

|     | Operator             | Rule                                                  |
| --- | -------------------- | ----------------------------------------------------- |
| 1   | $\hat{\mathbf{S}}^2$ | $\Delta S = 0$                                        |
| 2   | $\hat{\mathbf{L}}^2$ | $\Delta L = \pm 1$                                    |
| 3   | $\hat{\mathbf{J}}^2$ | $\Delta J = 0, \pm 1$ $\;(J=0 \nleftrightarrow J'=0)$ |
| 4   | $\hat{J}_z$          | $\Delta M_J = 0, \pm 1$                               |
| 5   | $\hat{\Pi}$ (parity) | $\Pi' = -\Pi$                                         |

---

# The Zeeman Effect

<div class="columns wide-right">
<div>

</br>
</br>

$\vec{B} = 0$:

States with different $M_J$ values are degenerate
</br>
$\vec{B} \neq 0$:

Degeneracy is lifted → distinct energy levels

</div>
<div style="display: flex; justify-content: center; align-items: center; height: 100%">

![h:460](energy_levels.png)

</div>
</div>

</br>

---

# Photon Emission and Polarization

<div class="columns">
<div>

</br>
</br>
</br>

![w:100%](photon_emission.png)

</div>
<div>

Photon emission satisfies angular momentum conservation.

$\Delta J_z ^{\text{atom}} + J_z ^{(\gamma)} = 0$

- $\sigma^\pm: J_z^{(\gamma)} = \mp \hbar \space \space \space (\perp \vec B)$
- $\pi: J_z^{(\gamma)} = 0$ $\space \space \space (\parallel \vec B)$
- A polarizer with orientations $\in \set{\perp, \parallel}$ selects split vs. unsplit photons

> Circularly polarized along $\vec B$ $\leftrightarrow$ Linearly polarized transverse to $\vec B$

</div>
</div>

---

<!-- _class: roadmap -->

## ~~Zeeman Effect Theory~~

## → Optics Theory

## Procedure

## Results

---

# The Fabry-Pérot Etalon

<div class="columns eq-row">
<div style="padding-left: 5em">

![h:420](rings.png)

$$\phi_\text{round}(\beta) = 2 \left ( \frac{2\pi n}{\lambda} \right ) t\cos\beta = 2\pi m$$

</div>
<div>

![h:530](etalon.png)

</div>
</div>

---

# Zeeman-Split Interference Pattern

<div class="columns eq-row">
<div>

![h:420](pattern.png)

</div>
<div>

$$\Delta E = \mu_B g_J B M_J = -\frac{hc}{\lambda} \frac{\cos \beta_f - \cos \beta_0}{\cos \beta_0}$$

</br>

<span style="font-size: 0.75em; color: #888">$0$: Unsplit state</span>
<span>$f$: Split state</span>

</br>

> Upward photon energy shifts $\leftrightarrow$ larger radii

</div>
</div>

---

<!-- _class: roadmap -->

## ~~Zeeman Theory~~

## ~~Optics Theory~~

## → Procedure

## Results

---

# Apparatus

![w:100%](apparatus.png)

---

# Procedure

<div class="columns wide-right">
<div>

</br>

> Indirectly measure a precisely known physical constant: $\mu_B$.

- Alignment along optical rail
- Record $(\alpha_-, \alpha_0, \alpha_+)^{(i)}$ values at varying field strengths $B^{(i)}$
- Fit energy-angle eq.
  - $\mu_B g_J B M_J = -\frac{hc}{\lambda} \frac{\cos \beta_f - \cos \beta_0}{\cos \beta_0}$
- Obtain an experimental value for $\mu_B$

</div>
<div>

![w:100%](mu_B_fit.png)

</div>
</div>

---

<!-- _class: roadmap -->

## ~~Zeeman Theory~~

## ~~Optics Theory~~

## ~~Procedure~~

## → Results

---

# Free Spectral Range

<div class="columns eq-row">
<div>

> The field $B_\text{FSR}$ at which $\sigma^\pm$ lines from adjacent rings coincide helps estimate systematic error in $B$.

- $\text{FSR} = \frac{c}{2nt}$
- $B_\text{FSR} = \frac{h}{\mu_B} \frac{c}{2nt} \frac{1}{g_J |\Delta M_J|}$

</br>

|                    | Experimental     | Theoretical |
| ------------------ | ---------------- | ----------- |
| $B_\text{FSR}$ (G) | $15200 \pm 2400$ | $18300$     |

</br>

<span style="font-size: 0.8em; color: #888">$1.3\sigma$ discrepancy — low to moderate systematic error in $B$.</span>

</div>
<div>

![w:100%](fsr_extrapolation.png)

</div>
</div>

---

# Results

|               | Experimental                    | Accepted                |
| ------------- | ------------------------------- | ----------------------- |
| $\mu_B$ (J/T) | $(9.4 \pm 0.4) \times 10^{-24}$ | $9.274 \times 10^{-24}$ |

</br>

## Takeways

- $\mu_B$ is recovered to within $0.23\sigma$ of the accepted value.
- We place greater trust in the perturbative analysis of Zeeman energy splitting.
- Selection rules are verified with clean split-unsplit patterns separation via polarizer.
- Systematic error in $\vec B$ $\rightarrow$ deviations of $\mu_B$ from accepted.
