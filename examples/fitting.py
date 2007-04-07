#!/usr/bin/env python
"""Simple data fitting and smoothing example"""

from numpy import exp,arange,array,linspace
from numpy.random import normal

from scipy.optimize import leastsq
from scipy.interpolate import splrep,splev

import numpy as N
import scipy as S
import pylab as P

def func(pars):
    a, alpha, k = pars
    return a*exp(alpha*x_vals) + k

def errfunc(pars):
    """Return the error between the function func() evaluated""" 
    return y_noisy - func(pars)  #return the error

# Use globals for the x values and true parameters
pars_true = array([2.0, -.76, 0.1])
x_vals = linspace(0, 4, 1000)

# some pseudo data; add some noise
y_noisy = func(pars_true) + normal(0.0, 0.1, x_vals.shape)

# the intial guess of the params
guess = 1.0, -.4, 0.0

# now solve for the best fit paramters
best, mesg = leastsq(errfunc, guess)

print 'Least-squares fit to the data'
print 'true', pars_true
print 'best', best
print '|err|_l2 =',P.l2norm(pars_true-best)

# scipy's splrep uses FITPACK's curfit (B-spline interpolation)
print
print 'Spline smoothing of the data'
sp = splrep(x_vals,y_noisy)
smooth = splev(x_vals,sp)
print 'Spline information (see splrep and splev for details):',sp

# Polynomial fitting
def plot_polyfit(x,y,n,fignum=None):
    """ """
    if fignum is None:
        fignum = P.figure().number
        P.plot(x,y,label='Data')
        
    fit_coefs = N.polyfit(x,y,n)
    fit_val = N.polyval(fit_coefs,x)
    P.plot(x,fit_val,label='Polynomial fit, $n=%d$' % n)
    P.legend()
    return fignum

# Now use pylab to plot
P.figure()
P.plot(x_vals,y_noisy,label='Noisy data')
P.plot(x_vals,func(best),lw=2,label='Least-squares fit')
P.legend()
P.figure()
P.plot(x_vals,y_noisy,label='Noisy data')
P.plot(x_vals,smooth,lw=2,label='Spline-smoothing')
P.legend()

fignum = plot_polyfit(x_vals,y_noisy,1)
plot_polyfit(x_vals,y_noisy,2,fignum)
plot_polyfit(x_vals,y_noisy,3,fignum)

P.show()
