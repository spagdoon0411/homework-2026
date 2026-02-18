# Error Propagation Equations Used in the Magneton Fit

## Snell's Law

$$\beta = \arcsin\!\left(\frac{\sin\alpha}{n}\right)$$

### Uncertainty in $\beta$

Differentiating with respect to $\alpha$:

$$\frac{\partial \beta}{\partial \alpha} = \frac{\cos\alpha}{n\cos\beta}$$

So:

$$\delta\beta = \left|\frac{\cos\alpha}{n\cos\beta}\right| \delta\alpha$$

## Energy Shift

$$\Delta E = -\frac{hc}{\lambda} \frac{\cos\beta_f - \cos\beta_0}{\cos\beta_0}$$

### Uncertainty in $\Delta E$

Partial derivatives:

$$\frac{\partial(\Delta E)}{\partial \beta_f} = \frac{hc}{\lambda} \frac{\sin\beta_f}{\cos\beta_0}$$

$$\frac{\partial(\Delta E)}{\partial \beta_0} = -\frac{hc}{\lambda} \frac{\sin\beta_0 \cos\beta_f}{\cos^2\beta_0}$$

Propagated uncertainty:

$$\delta(\Delta E) = \sqrt{\left(\frac{\partial(\Delta E)}{\partial \beta_f}\right)^2 (\delta\beta_f)^2 + \left(\frac{\partial(\Delta E)}{\partial \beta_0}\right)^2 (\delta\beta_0)^2}$$

Substituting:

$$\delta(\Delta E) = \sqrt{\left(\frac{hc}{\lambda}\frac{\sin\beta_f}{\cos\beta_0}\right)^2 (\delta\beta_f)^2 + \left(\frac{hc}{\lambda}\frac{\sin\beta_0\cos\beta_f}{\cos^2\beta_0}\right)^2 (\delta\beta_0)^2}$$

## $x$-axis: $g_J B \Delta M_J$

$$x = g_J B \Delta M_J, \qquad \delta x = g_J \,|\Delta M_J|\, \delta B$$

where $\delta B$ is the prediction uncertainty from the $B$ vs. $I$ calibration fit.
