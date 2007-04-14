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
s = N.cos(N.pi*tcoarse) * N.sin(2*N.pi*tcoarse)

# create sinterp by computing the spline fitting tcoarse to s and then
# evaluating it on tfine.  Plot tcoarse vs s with markers and tfine vs
# sinterp with a solid line
XXX
P.show()

interpolate.splrep
interpolate.splev
