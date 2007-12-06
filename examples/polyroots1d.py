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
nroots_minus1 = 3
coefs = reduce(N.convolve,[[1,1]]*nroots_minus1+[[1,2],[1,-1]])

# Construct the polynomial and get its roots
pol = S.poly1d(coefs)
roots = pol.r

print 'Polynomial p(x):\n',pol,'\n'
print 'p(x) built with coefs:',coefs
print 'Roots of p(x):',roots

# Plot p(x)
x = N.linspace(-4,4,400)
y = pol(x)

# Show roots
plot_poly(x,y,roots)
P.xlim(-3,2)
P.ylim(-250,100)
P.title('All roots')

# Set limits and grid to make the plot clear
#P.ylim(-40,40)
plot_poly(x,y,roots)
eps = 0.05
P.xlim(-1-eps,-1+eps)
P.ylim(-eps,eps)
P.title('Root cluster around $x=-1$')

# Display on screen
P.show()
