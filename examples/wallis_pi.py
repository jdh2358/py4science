#!/usr/bin/env python
"""Simple demonstration of Python's arbitrary-precision integers."""

# We need exact division between integers as the default, without manual
# conversion to float b/c we'll be dividing numbers too big to be represented
# in floating point.
from __future__ import division

from decimal import Decimal

def pi(n):
    """Compute pi using n terms of Wallis' product.

    Wallis' formula approximates pi as

    pi(n) = 2 \prod_{i=1}^{n}\frac{4i^2}{4i^2-1}."""
    
    num = 1
    den = 1
    for i in xrange(1,n+1):
	tmp = 4*i*i
	num *= tmp
	den *= tmp-1
    return 2.0*(num/den)

def part_range(n1,n2,nchunks):
    """Partition a range specification in nchunks"""
    size,rem = divmod(n2-n1,nchunks)
    sizes = [size]*nchunks
    while rem > 0:
        for i in range(nchunks):
            sizes[i] += 1
            rem -= 1
            if rem == 0:
                break

    # The sizes list has the offsets, now we need the actual start,stop pairs
    ranges = []
    start=n1
    for size in sizes:
        ranges.append((start,start+size))
        start += size
    return ranges
    
def wpi_nd(range_spec):
    """Compute pi using n terms of Wallis' product.

    Wallis' formula approximates pi as

    pi(n) = 2 \prod_{i=1}^{n}\frac{4i^2}{4i^2-1}."""

    n1,n2 = range_spec
    
    num = 1
    den = 1
    for i in xrange(n1,n2):
	tmp = 4*i*i
	num *= tmp
	den *= tmp-1

    return num,den

def par_pi(n,num_engines=1):
    """Compute pi using n terms of Wallis' product.

    Wallis' formula approximates pi as

    pi(n) = 2 \prod_{i=1}^{n}\frac{4i^2}{4i^2-1}.

    Parallel version."""

    num,den = reduce(lambda x,y:(x[0]*y[0],x[1]*y[1]),
                     map(wpi_nd,part_range(1,n+1,num_engines)))
    return 2.0*(num/den)
    
    
if __name__ == '__main__':
    # Simple convergence demo.

    import pylab as P
    import numpy as N

    nrng = N.linspace(10,2000,20).astype(N.int_)
    wpi = N.array(map(pi,nrng))
    diff = N.absolute(wpi-N.pi)
    # plot with lines
    P.figure()
    P.semilogy(nrng,diff)
    # and superimpose red circles
    P.semilogy(nrng,diff,'ro')
    P.title(r"$\rm{Convergence of Wallis' product formula for}\ \pi$")
    P.xlabel('Number of terms')
    P.ylabel(r'$|\rm{Error}|$')
    P.grid()
    P.show()
