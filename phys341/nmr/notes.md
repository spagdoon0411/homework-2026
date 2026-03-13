Based on my data (sources listed below),

- phys341/nmr/frequencies.tsv
- some np arrays in nmr.py

Do the following tasks:

- [x] obtain experimental g-factors for each of my samples via a linear fit using the resonance equation
- [x] produce g-factor plots
- [ ] one table of each sample's resonant RF frequency and g-factor
- [ ] one table per sample containing the reported B vs. f values

Insert the tables and plots in the results/ section. Let me define captions; leave captions blank. Define a snake_case latex \label for each table, plot, etc.

Resonance equation:

$$
h \nu_\text{rf} = g \mu _N B_0
$$

Some uncertainties:

- B-field uncertainty: 50G
- RF freuqnecy uncertainty: 1MHz

---

- The following folders contain CSVs containing oscilloscope traces for T2-star
  decaying-envelope NMR signals.

phys341/nmr/trace_processing/t2star_traces/CuSO4_Responses
phys341/nmr/trace_processing/t2star_traces/CuSO4H2O_Responses
phys341/nmr/trace_processing/t2star_traces/Glycerin_Responses_Spandan
phys341/nmr/trace_processing/t2star_traces/H2O_Responses
phys341/nmr/trace_processing/t2star_traces/Polystyrene_Responses_Spandan
phys341/nmr/trace_processing/t2star_traces/PTFE_Responses_Spandan

- Extract the trace data, near the CSV cell "Analog Channels"
- In phys341/nmr/trace_processing.ipynb, plot each of the sinusoids
- Organize the trace data in a Pandas DataFrame with their substance ID
- For all but PTFE, take the absolute value of the signal, sample the local max of each oscillation peak, and display the results
- Fit decaying exponentials to each of the sampled local maxima and to the PTFE decay. Display the exponential in a plot in the Jupyter notebook and report the T2\* value in the plot title.

---

Export the trace from phys341/nmr/trace_processing/t2star_traces/3895G_FFTs/FFT 1 2026-02-23 14-34-27.csv. This is a Fourier transform for a frequency pulse. Fit a Gaussian, report the equation in the legend, and obtain FWHM values (reported in the title). Be

---

- The tables of the measured data have their tiltes in the captions. Put the titltes in the titles.sure to
- For all of the g-factor linear fit plots, title them "g-factor Linear Fit for <sample>"
- Add a supertitle to the T2* plots "T2* analysos for <sample>". The first plot should be titled "Oscilloscope Data" and the second should be titled "Exponential Decay Fit: T2* = <T2* value>". Update those plots so that for the nonPTFE samples the trace after shift and absolute value-ing is displayed along with the envelope points, to provide context as to where the envelope points came from. Plot a continuous line for this, not a scatter. Make it grey and add "Processed oscillation data" to the legend
- Add values and uncertainty bars to the SDOM plot
- for the gaussian plot Add a line denoting the RF frequency peak, placing the frequency value in the legend. Update the title to "Fourier Transform of a Frequency Pulse". Remove the caption in my report; I will write these.

---

# To Dos

- [x] g-factors for each one
- [x] g-factor plots
- [x] data tables
- [x] label data tables
- [x] mass import envelope data
- [x] do inversion of all negative envelope data and display results
- [x] process ptfe separately
- [x] sdom analysis for g-factor results
- [x] report T2\* plots and values in table
- [x] assess rf uncertainty by fitting Gaussian
- [ ] (needs more context): systematic error investigation (red star)
- [ ] does t2\* depend on the resonance frequency? measure and find out
- [ ] answer experimental context quesitons
  - [ ] discuss what you saw inside the hole and how a marginal oscillator works
  - [ ] discuss how chemical structures, polarity, and "the physics that a t2\* signal indicates" results in differences in those signals. "be sure to discuss what physics each constant tells you about the physics of nmr"
  - [ ] why is it important to measure resonant frequency when spikes are equally spaced?
  - [ ] direct analogy with Dynamic #3 lab (cite any sources)
  - [ ] compare all T2\* values
- [x] move around titles
- [ ] discuss g-factor plot results
- [ ] discuss sdom plot results
- [ ] discuss T2\* plot reuslts
- [ ] discuss Gaussian fit
- [ ] use updated rf unc and regenerate plots
- [ ] add captions
- [ ] add citations

\mu(^{19}\mathrm{F}) = 2.628\,321\,353(17)\ \mu_N

# Discussions

## Marginal Oscillator

The sample holder contains a marginal oscillator, which is a standard inductor-capacitor (LC) circuit. LC circuits have a resonant frequency that is a function of their inductance $L$ and their capacitance $C$:

$$
\omega_\text{res} = \frac{1}{\sqrt{LC}}
$$
