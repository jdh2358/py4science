import scipy
from math import sin

newton = scipy.optimize.newton
quad = scipy.integrate.quad

# test input function
def f(t):
    return t*(sin(t))**2

# exact \int_0^t f(s) ds - u
def g(t):
    u = 0.25
    return .25*(t**2-t*sin(2*t)+(sin(t))**2)-u

# now let's construct g(t) via numerical integration
def gn(t):
    u = 0.25
    return quad(f,0.0,t)[0] - u

# main
# 
tguess = 10.0

print
print "Solution using the numerical integration technique" 
t1 = newton(gn,tguess,f)
print "t1, g(t1) =",t1,g(t1)

print '"Exact" solution (knowing the analytical form of the integral)'
t0 = newton(g,tguess,f)
print "t0, g(t0) =",t0,g(t0)

print
print "Mathematica gives t==1.06601 for this problem"
