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
    raise NotImplementedError

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
