
Broad rules and notes:

Any plots produced that go into my report should be output to a file and embedded from the output site into the report itself.

Any final values placed in the report should be rounded according to their uncertainties. A function for doing this can be found in phys341/utils: round_unc_pdg. All reported values should alwauys have uncertainties on them.

Use global font size settings when creating plots, always.

The script in which you should write all of this code is at phys341/zeeman/zeeman.py. Ignore phys341/zeeman/zeeman.ipynb.

My TeX report is at phys341/zeeman/report/report.tex. This is where produced plots will go.

Any datasets should first be represented in pandas before use.

Uncertainties should be propagated through all computations. If an uncertainty is not provided, do not assume one and let me set it.

Instructions:

Create global settings for plot font sizes.

Using these B vs. I values, obtain a linear fit for B vs. I with uncertainties. Display the plot under my report's results section.

B vs. I values:

I = [0.020 0.231 0.443 0.656 0.868 1.082 1.294 1.508 1.721 1.933 2.144 2.356 2.567 2.776 2.987 3.079];
dI = 0.001;

B = [56.00 184.0 333.0 420.0 490.0 780.0 830.0 980.0  1170  1380  1470  1600  1710  1760  1860  2100];
dB = 20;

The following are data points for multiple current values:

I =           [2.411 2.825 3.110 3.431 3.708 4.100 4.321 4.635 4.909];

ARight =      [0.738 0.738 0.743 0.743 0.743 0.749 0.743 0.743 0.749];
AplusRight =  [0.781 0.786 0.797 0.807 0.807 0.823 0.823 0.829 0.840];
AminusRight = [0.695 0.684 0.679 0.679 0.674 0.663 0.658 0.652 0.647];

ALeft =       [-0.727 -0.733 -0.733 -0.738 -0.738 -0.743 -0.738 -0.738 -0.743];
AplusLeft =   [-0.754 -0.778 -0.781 -0.797 -0.802 -0.813 -0.818 -0.823 -0.829];
AminusLeft =  [-0.679 -0.679 -0.674 -0.668 -0.663 -0.652 -0.647 -0.647 -0.636];


ALower =      [0.770 0.791 0.797 0.807 0.807 0.823 0.823 0.829 0.840];
AHigher =     [1.139 1.139 1.128 1.128 1.128 1.118 1.112 1.107 1.107];

This corresponds to the dataset described in the report (with columns possibly rearranged):
$(B^{(i)}, \alpha^{(i)}_{l, -}, \alpha^{(i)}_{l, +}, \alpha^{(i)}_{l, 0}, \alpha^{(i)}_{r, -}, \alpha^{(i)}_{r, +}, \alpha^{(i)}_{r, 0})$.

Using these values, obtain a datset of the form $(B^{(i)}, \alpha_{-}^{(i)}, \alpha_{0}^{(i)}, \alpha_{+}^{(i)})$, merging left and right alpha values like this:

$\alpha^{(i)}_j = \frac{1}{2} \left ( \alpha_{r, j}^{(i)} - \alpha_{l, j}^{(i)} \right )$ for $j \in \set{-, 0, +}$

USe these two equations, one of which is Snell's law, to obtain a dataset of the form:

$\left (g_J B_0^{(i)} M_J^{(i)}, -\frac{hc}{\lambda} \frac{\cos \beta_f^{(i)} - \cos \beta_0^{(i)}}{\cos \beta_0} \right)$

\begin{equation}
  \Delta E = \mu_B g_J B M_J = -\frac{hc}{\lambda} \frac{\cos \beta_f - \cos \beta_0}{\cos \beta_0}
  \label{eq:zeeman_shift}
\end{equation}

Snell's law relates $\beta$ and $\alpha$:

\begin{equation}
  \sin \beta = \frac{1}{n} \sin \alpha
  \label{eq:snell}
\end{equation}

Through a linear fit, obtain an experimental value of \mu_B. Output the resulting plot with the fit line and uncertainties reported. Also embed the plot in my report.

Create a LaTeX table that is embedded into my report from a file. This table should report each value of $\alpha$ measured, with column headers that I can set easily. Be sure to report the merged $(B^{(i)}, \alpha_{-}^{(i)}, \alpha_{0}^{(i)}, \alpha_{+}^{(i)})$ dataset in this table--not all of the original \alpha values.

For now, use an uncertainty in \alpha of 0.01. Note that values reported in this table must be rounded using round_unc_pdg and the uncertainty in \alpha. The Bi value should be rounded according to its uncertainty from the B vs. I fit.

Create another table for the tidied datset
 
 All uncertainties should be reported in their column headers. Column headers should also report appropriate units.