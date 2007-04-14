from __future__ import division
import sys
import numpy as N
import pylab as P
from scipy import interpolate

#paramaters
dt1 = 0.005     # step size
dt2 = 0.001

tfine = N.arange(0.0, 5, 0.01)
tcoarse = N.arange(0.0, 5, 0.1)
def func(t):
    return N.cos(N.pi*t) * N.sin(2*N.pi*t)

# create sinterp by computing the spline fitting tcoarse to s and then
# evaluating it on tfine.  Plot tcoarse vs s with markers and tfine vs
# sinterp with a solid line
s = func(tcoarse)

tck = interpolate.splrep(tcoarse, s, s=0)
sinterp = interpolate.splev(tfine, tck, der=0)

P.plot(tcoarse, s, 'o', label='coarse')
P.plot(tfine, sinterp, '+', label='fit')
P.plot(tfine, func(tfine), '-', label='actual')
P.legend()
P.show()
