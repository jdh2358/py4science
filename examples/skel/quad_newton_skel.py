#!/usr/bin/env python
"""Root finding using SciPy's Newton's method routines.
"""

from math import sin

from scipy.integrate import quad
from scipy.optimize import newton

# test input function
def f(t):
    # f(t): t * sin^2(t)
    raise NotImplementedError('Original solution has 1 line')

def g(t):
    "Exact form for g by integrating f(t)"
    u = 0.25
    return .25*(t**2-t*sin(2*t)+(sin(t))**2)-u

def gn(t):
    "g(t) obtained by numerical integration"
    u = 0.25
    # Hint: use quad, see its return value carefully.
    raise NotImplementedError('Original solution has 1 line')

# main
tguess = 10.0

print '"Exact" solution (knowing the analytical form of the integral)'
raise NotImplementedError('Original solution has 1 line')
print "t0, g(t0) =",t0,g(t0)

print
print "Solution using the numerical integration technique" 
raise NotImplementedError('Original solution has 1 line')
print "t1, g(t1) =",t1,g(t1)

print
print "To six digits, the answer in this case is t==1.06601."
