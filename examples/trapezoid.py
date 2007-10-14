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

    # Sanity checks
    if len(x)!=len(y):
        raise ValueError('x and y must have the same length')
    if len(x)<2:
        raise ValueError('x and y must have > 1 element')

    # Efficient application of trapezoid rule via numpy
    return 0.5*((x[1:]-x[:-1])*(y[1:]+y[:-1])).sum()

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

    # Generate an equally spaced grid to sample the function at
    x = N.linspace(a,b,npts)
    # For an equispaced grid, the x spacing can just be read off from the first
    # two points and factored out of the summation.
    dx = x[1]-x[0]
    # Sample the input function at all values of x
    y = N.array(map(f,x))
    # Compute the trapezoid rule sum for the final result
    return 0.5*dx*(y[1:]+y[:-1]).sum()

if __name__ == '__main__':
    # Simple tests for trapezoid integrator, when this module is called as a
    # script from the command line.  From ipython, run it via:
    #
    # run -e trapezoid
    #
    # so that ipython ignores the SystemExit exception automatically raised by
    # the unittest module at the end.

    import unittest
    import numpy.testing as ntest

    def square(x): return x**2

    class trapzTestCase(unittest.TestCase):
        def test_err(self):
            self.assertRaises(ValueError,trapz,range(2),range(3))

        def test_call(self):
            x = N.linspace(0,1,100)
            y = N.array(map(square,x))
            ntest.assert_almost_equal(trapz(x,y),1./3,4)

    class trapzfTestCase(unittest.TestCase):
        def test_square(self):
            ntest.assert_almost_equal(trapzf(square,0,1),1./3,4)

        def test_square2(self):
            ntest.assert_almost_equal(trapzf(square,0,3,350),9.0,4)

    unittest.main()
