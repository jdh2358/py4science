#!/usr/bin/env python
"""Root finding using SciPy's Newton's method routines.
"""

from math import sin

import scipy, scipy.integrate, scipy.optimize

quad = scipy.integrate.quad
newton = scipy.optimize.newton

# test input function f(t): t * sin^2(t)
def f(t): XXX

# Use u=0.25
def g(t): XXX

# main
tguess = 10.0

print "Solution using the numerical integration technique"
t0 = newton(g,tguess,f)
print "t0, g(t0) =",t0,g(t0)

print
print "To six digits, the answer in this case is t==1.06601."
