from maplib import Logistic
from matplotlib.numerix import arange, absolute, log, Float
from matplotlib.mlab import polyfit, polyval
from pylab import subplot, plot, show

epsilon = 1e-10
x0 = 0.4
y0 = x0 + epsilon

logmap = Logistic(0.9)
x = logmap.iterate(x0, 100)
y = logmap.iterate(y0, 100)
ind = arange(len(x), typecode=Float)

# x-y \sim epsilon exp(lambda * t)
# log(|x-y|) = log(epsilon) + lambda*t (b=log(epsilon) and m=lambda)
d = log(absolute(x-y))
coeffs = polyfit(ind, d, 1)
lambda_, b = coeffs
print 'lyapunov exponent= %1.3f'%lambda_
print 'log(epsilon)=%1.3f, b = %1.3f' %(log(epsilon), b)

# now plot the result
subplot(211)
plot(ind, x, '-r', ind, x, '--g', )
subplot(212)
plot(ind, d, ind, polyval(coeffs, ind))
show()

