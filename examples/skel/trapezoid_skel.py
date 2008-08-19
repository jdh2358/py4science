#!/usr/bin/env python
"""Simple trapezoid-rule integrator."""

import numpy as N

def trapz(x, y):
    """Simple trapezoid integrator for sequence-based innput.

    Inputs:
      - x,y: arrays of the same length.

    Output:
      - The result of applying the trapezoid rule to the input, assuming that
      y[i] = f(x[i]) for some function f to be integrated.

    Minimally modified from matplotlib.mlab."""

    raise NotImplementedError


def trapzf(f,a,b,npts=100):
    """Simple trapezoid-based integrator.

    Inputs:
      - f: function to be integrated.

      - a,b: limits of integration.

    Optional inputs:
      - npts(100): the number of equally spaced points to sample f at, between
      a and b.

    Output:
      - The value of the trapezoid-rule approximation to the integral."""

    # you will need to apply the function f to easch element of the
    # vector x.  What are several ways to do this?  Can you profile
    # them to see what differences in timings result for long vectors
    # x?
    raise NotImplementedError


#-----------------------------------------------------------------------------
# Tests
#-----------------------------------------------------------------------------
import nose, nose.tools as nt
import numpy.testing as nptest

def square(x): return x**2

def test_err():
    nt.assert_raises(ValueError,trapz,range(2),range(3))

def test_call():
    x = np.linspace(0,1,100)
    y = np.array(map(square,x))
    nptest.assert_almost_equal(trapz(x,y),1./3,4)

def test_square():
    nptest.assert_almost_equal(trapzf(square,0,1),1./3,4)

def test_square2():
    nptest.assert_almost_equal(trapzf(square,0,3,350),9.0,4)


# If called from the command line, run all the tests
if __name__ == '__main__':
    # This call form is ipython-friendly
    nose.runmodule(argv=['-s','--with-doctest'],
                   exit=False)
