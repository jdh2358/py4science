#!/usr/bin/env python
"""Simple demonstration of polynomials and root finding."""

import numpy as N
import scipy as S
import pylab as P

def plot_poly(x,y,roots):
    """Simple utility to make a charting screen with x/y axes"""
    P.figure()
    P.axhline(0,color='g')
    P.axvline(0,color='g')
    P.grid()
    P.plot(x,y,'b-')
    P.scatter(roots.real,roots.imag,s=80,c='r')
    P.xlabel('Re')
    P.ylabel('Im')

# Create the coefficients for a polynomial with nroots_minus1 at x=-1, one
# root at -2 and one root at 1:
coefs = XXX  # Hint: use reduce() and N.convolve

# Construct the polynomial and get its roots
pol = S.poly1d(coefs)
roots = pol.r

print 'Polynomial p(x):\n',pol,'\n'
print 'p(x) built with coefs:',coefs
print 'Roots of p(x):',roots

# Sample and plot p(x)
x = XXX
y = XXX

# Show roots
plot_poly(x,y,roots)
P.xlim(-3,2)
P.ylim(-250,100)
P.title('All roots')

# Make a new plot around the -1 cluster of roots (use a window of size eps
# around -1)
eps = 0.05
XXX

# Display on screen
P.show()
