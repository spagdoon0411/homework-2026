---
marp: true
---

# Nuclear Magnetic Resonance

**Antoni Gonzalez and Spandan Suthar**
Quantum Physics Lab II • 341 Winter 2026

---

## $\rightarrow$ Applications of NMR

## Theoretical Background

## Experiment Setup

## Procedure

## Results

## Questions

---

<div style="display: flex; align-items: center;">
<div style="flex: 1;">

## Applications of NMR

</div>
<div style="flex: 1;">

- Molecular structure investigation
  - Functional groups
  - Protein folding/unfolding studies
  - Polymer structure
- Substance identification
- Non-invasive medical imaging

</div>
</div>

---

## ~~Applications of NMR~~

## $\rightarrow$ Theoretical Background

## Experiment Setup

## Procedure

## Results

## Questions

---

## Magnetization as an Ensemble Average

<!--
Don't forget to say that we have
an ensemble of nuclear magnetic dipoles, first.
-->

<div style="display: flex; align-items: center;">
<div style="flex: 1;">

$$
\hat M = \frac{1}{V} \left \langle {\sum_k  \hat \mu_k} \right \rangle
$$

</br>

$$
\braket{\hat M} = \vec M
$$

</div>
<div style="flex: 1;">

![width:500px](spin_lattice.png)

</div>
</div>

---

<div style="display: flex; align-items: center;">
<div style="flex: 1;">

![width:500px](out/precession.png)

</div>
<div style="flex: 1;">

## Precession of $\vec M$

Magnetic dipoles precess around constant-direction magnetic fields $\vec B_0$.

Precession angle evolves at Larmor frequency:

$$\omega_\beta \equiv \dot \beta = \frac{g \mu_N B_0}{2\pi \hbar }$$

</div>

---

<div style="display: flex; align-items: center;">
<div style="flex: 0.35;">

## RF-Induced Energy Transfer

Apply $\vec B_1$, static in the precession frame.

<!-- Static <-> resonance condition -->

Resonance: $\omega_{\text{rf}} = \omega_\beta$.

Orthogonal precession, at Larmor frequency:

$$
\omega_\alpha \equiv \dot \alpha = \frac{g \mu_B B_1}{ \hbar}
$$

</div>
<div style="flex: 0.65;margin-top:-30px">

![width:120%](out/rf_induced.png)

</div>
</div>

---

<div style="display: flex; justify-content: center; align-items: center;">

![width:900px](out/complete_nutation.png)

</div>

---

## Zeeman Splitting and Resonance

<div style="display: flex; align-items: center;">
<div style="flex: 0.6; margin-right: 40px;">

![width:100%](out/zeeman_splitting.png)

</div>
<div style="flex: 0.4;">

Zeeman energy splitting lifts degeneracy:

$$
E = E_0 - \gamma \hbar B_0 m_I
$$

</br>

$\vec \mu \propto \vec I$, so TFAE:

- More negative $M_z$
- More negative $I_z$
- More negative $m_I$

<!--

What I want to emphasize is that the classical precession picture and the quantum transition picture are consistent.

When the RF pulse causes $\vec M$ to tilt toward the transverse plane, it decreases $M_z$, meaning a decrease in $I_z$, meaning a more negative magnetic quantum number.

RF pulses cause Zeeman transitions across the ensemble.

-->

</div>
</div>

---

<div style="display: flex; align-items: center;">
<div style="flex: 1;">

## The Resonance Condition

The energy shift provided by the RF signal must meet the $\Delta m_I = -1$ energy spacing exactly.

</div>
<div style="flex: 1;">

$$
E_\text{rf} = E_\text{Zeeman}
$$

$$
\downarrow
$$

$$
\boxed{h \nu_\text{rf} = g \mu_N B_0 m_I}
$$

</div>
</div>

</br>

> Goal: plot $h \nu_\text{rf} \space$ vs $\space \mu_N B_0 m_I$. Recover $g$ through slopes of regression lines.

---

## Sweeping $\vec B_0$ vs. Pulsing RF

<!--
We need to meet the resonance condition for short windows of time.

This allows us to clearly see when resonance is met and to produce clear, well-spaced resonance structures that allow us to measure the time taken for the ensemble to relax from the its higher-energy state.

How do we do that?
-->

Short periods of nutation are created by meeting the resonance condition for short intervals.

- Allow slow sinusoidal modulation in $\vec B_0$
  - $B_0(t) = B_\text{static} + \tilde B \cos(\omega_s t)$
- Find $\nu_\text{rf}$ at which $\omega_\text{rf}$ is near $\omega_0$
  - Resonance windows
- Equally-space resonance windows (experimental convenience)

---

## Sweeping $\vec B_0$ vs. Pulsing RF

![width:100%](out/field_sweep.png)

---

## Sweeping $\vec B_0$ vs. Pulsing RF

## ![width:100%](out/field_sweep_resonant.png)

---

## ~~Applications of NMR~~

## ~~Theoretical Background~~

## $\rightarrow$ Experiment Setup

## Procedure

## Results

## Questions

---
