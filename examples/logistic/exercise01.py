import numpy as np
import matplotlib.pyplot as plt

from maplib import Logistic

epsilon = 1e-10
x0 = 0.4
y0 = x0 + epsilon

logmap = Logistic(0.9)
x = logmap.trajectory(x0, 100)
y = logmap.trajectory(y0, 100)
ind = np.arange(len(x), dtype=float)

# x-y \sim epsilon exp(lambda * t)
# log(|x-y|) = log(epsilon) + lambda*t (b=log(epsilon) and m=lambda)
d = np.log(abs(x-y))
coeffs = np.polyfit(ind, d, 1)
lyap_exp, b = coeffs
print 'lyapunov exponent= %1.3f' % lyap_exp
print 'log(epsilon)=%1.3f, b = %1.3f' % (np.log(epsilon), b)

# now plot the result
plt.subplot(211)
plt.plot(ind, x, '-r', ind, x, '--g', )
plt.subplot(212)
plt.plot(ind, d, ind, np.polyval(coeffs, ind))
plt.show()
