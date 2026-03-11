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

$$\omega_\beta \equiv \dot \beta = \frac{g \mu_N B_0}{\hbar }$$

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

Short periods of orthogonal precession are created by meeting the resonance condition for short intervals.

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

<div style="display: flex; align-items: center;">
<div style="flex: 0.40;">

# The Experiment

</div>
<div style="flex: 0.50 ;margin-top:25px">

> Observe the responses of various substances' nuclei to resonant radiofrequency signals, reproducing the nuclei's Lande $g$-factors and characterizing the nuclei's free induction decay.

</div>
</div>

---

# The Experiment

<div style="display: flex; align-items: center;">
<div style="flex: 0.50;">

## Measurables

- Applied magnetic field strength: $B_0$
- Frequency of applied RF pulse: $\nu_\text{rf}$
- Free-induction decay trace: $|\vec M_{xy}|$ vs $t$

</div>
<div style="flex: 0.50 ;margin-top:25px">

## Target Values

- $g$-factor: encoded in the slope relating $\nu_\text{rf}$ to $B_0$
- $T_2^*$: characteristic time of exponential decay envelopes from FID scope traces

</div>
</div>

---

## Experimental Equipment

<div style="display: flex; align-items: center;">
<div style="flex: 0.30;">

<!--
Be sure to note that the transverse magnetization
signal is picked up through the RF coil and the
use of blanking.
--->

1. Sample tube
2. Magnet (static field)
3. Electromagnet (dynamic field)
4. RF coil, with controller
5. RF response amplifier
6. Oscilloscope

</div>
<div style="flex: 0.50 ;margin-top:0px;margin-right:-250px">

![width:190%](<Screenshot 2026-03-11 at 12.29.30 PM.png>)

</div>
</div>

---

## Experimental Equipment

<!--
TODO: okay with filling in information that
was in the Google Slides presentation?
-->

<div style="display: flex; align-items: center;">
<div style="flex: 0.50;">

### Controls

- RF signal generator
- Field modulator
- Power supply

</div>
<div style="flex: 0.50 ;margin-top:25px">

### Signals and Wiring

- RF signal jack
- NMR signal jack (same as RF)
- Magnetometer

</div>
</div>

### Viewing Tools

- Oscilloscope displays output signals
- Spectrum analyzer determines uncertainty in $\nu_\text{rf}$ (via Fourier transform)

---

## Experimental Uncertainty

### RF-Signal Frequency

Non-ideal (non-$\delta$) signal with a FWHM $\Delta \nu_\text{rf}$.

### External Field

Measurements of $|\vec B_0|$ are performed with imprecise tools.

### Trace Capture

Oscilloscope captures instantaneous readings; true signals subject to fluctuations.

---

## ~~Applications of NMR~~

## ~~Theoretical Background~~

## ~~Experiment Setup~~

## $\rightarrow$ Procedure

## Results

## Questions

---

## Procedure Steps

<!--
NOTE: mention the need to check across RF ranges to
determine whether one uncertainty applies everywhere
-->

A. Sample FWHM widths from the spectrum analyzer across various RF frequencies

B. Per sample:

1. Set $B_\text{static}$ (via coil current)
2. Measure $B_\text{static}$ using Gaussmeter
3. Insert sample and find $\nu_\text{rf}$ range producing resonance windows
4. Obtain FID trace from oscilloscope
5. Repeat 1-4 for several static field strengths

---

<div style="display: flex; align-items: center;">
<div style="flex: 0.50">

### Sample Data

![alt text](<Screenshot 2026-03-11 at 6.10.07 AM.png>)

</div>
<div style="flex: 0.50 ;margin-top:25px;margin-left:40px;">

### Revised Data for Fits

![alt text](<Screenshot 2026-03-11 at 6.10.54 AM.png>)

</div>
</div>

---

## ~~Applications of NMR~~

## ~~Theoretical Background~~

## ~~Experiment Setup~~

## ~~Procedure~~

## $\rightarrow$ Results

## Questions

---

## Lande $g$-Factor Regression Fits

![alt text](<Screenshot 2026-03-11 at 6.12.36 AM.png>)

---

## Relaxation Time Envelope Fits

![alt text](<Screenshot 2026-03-11 at 6.12.56 AM.png>)

---

## Experimental Values from Fits

| **Material** | **Landé g-factor** | **Relaxation Time** | **Error g-factor** |
| ------------ | ------------------ | ------------------- | ------------------ |
| CuSO₄        | $5.89 \pm 0.49$    | $0.8 \pm 0.3$ ms    | 5.44%              |
| CuSO₄-H₂O    | $5.39 \pm 0.38$    | $3.9 \pm 6.1$ ms    | 3.51%              |
| H₂O          | $5.39 \pm 0.39$    | $5.5 \pm 14.5$ ms   | 3.51%              |
| Glycerin     | $6.13 \pm 0.39$    | $2.2 \pm 1.8$ ms    | 9.74%              |
| Polystyrene  | $4.90 \pm 0.55$    | $0.3 \pm 0.1$ ms    | 12.27%             |
| PTFE         | $5.30 \pm 0.74$    | $0.3 \pm 0.1$ ms    | 0.80%              |

---

<div style="display: flex; align-items: center;">
<div style="flex: 0.60;">

![width:600px](<Screenshot 2026-03-11 at 6.13.52 AM.png>)

</div>
<div style="flex: 0.40 ;margin-top:0px;margin-left:50px">

## Mean and SDOM Analysis

Mean very close to accepted value despite large fluctuations

Final trial (Polystyrene) brought down average significantly

- Proved difficult to measure
- Solid as opposed to liquid

Overall results in good agreement with accepted values of $g_p$

</div>
</div>

---

## Conclusions

### _NMR is a thing!_

Results conclusive that resonance occurs when exciting sample with correct frequency in corresponding magnetic field

- Magnetic field determines resonance

Measurements correctly identify sample makeup

- Landé g-factor consistent with single proton (1H) and fluorine samples

- With sophisticated equipment, precise identification of complex compounds possible

Coherent exponential relaxation from excited states after resonance windows pass

---

## ~~Applications of NMR~~

## ~~Theoretical Background~~

## ~~Experiment Setup~~

## ~~Procedure~~

## ~~Results~~

## $\rightarrow$ Questions

---
