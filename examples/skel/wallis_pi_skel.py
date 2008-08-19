#!/usr/bin/env python
"""Simple demonstration of Python's arbitrary-precision integers."""

# We need exact division between integers as the default, without manual
# conversion to float b/c we'll be dividing numbers too big to be represented
# in floating point.
from __future__ import division

from decimal import Decimal

XXX = None # a sentinel for missing pieces

def pi(n):
    """Compute pi using n terms of Wallis' product.

    Wallis' formula approximates pi as

    pi(n) = 2 \prod_{i=1}^{n}\frac{4i^2}{4i^2-1}."""

    raise NotImplementedError
    
# This part only executes when the code is run as a script, not when it is
# imported as a library
if __name__ == '__main__':
    # Simple convergence demo.

    # A few modules we need
    import pylab as P
    import numpy as N

    # Create a list of points 'nrange' where we'll compute Wallis' formula
    nrange =  XXX
    
    # Make an array of such values
    wpi =  XXX
    # Compute the difference against the value of pi in numpy (standard
    # 16-digit value)
    diff =  XXX

    # Make a new figure and build a semilog plot of the difference so we can
    # see the quality of the convergence
    
    P.figure()
    # Line plot with red circles at the data points
    P.semilogy(nrange,diff,'-o',mfc='red')

    # A bit of labeling and a grid
    P.title(r"Convergence of Wallis' product formula for pi")
    P.xlabel('Number of terms')
    P.ylabel(r'|Error}|')
    P.grid()

    # Display the actual plot
    P.show()
