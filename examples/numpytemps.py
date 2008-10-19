#!/usr/bin/env python
"""Demonstration of temporaries in Numpy.
"""

import numpy as np
import numpy.testing as nptest

import nose

# convenience global names
from numpy import (pi, sin, cos, add, subtract, multiply, power)

def test1():
    """Verify an expression using temporaries.
    """
    x = np.linspace(0,2*pi,100)

    # We compute a simple mathematical expression using algebra and functions
    # of x.  This uses a lot of temporaries that are implicitly created. In
    # total, the variable count is:
    # sin(x): 1
    # sin(2*x): 2
    # 4.5*cos(3*x**2): 4
    # The final temporaries for each term are added and the result stored as y,
    # which is also created.  So we have 1 array for the result and 7 temps.
    y = sin(x) + sin(2*x) - 4.5*cos(3*x**2)

    # Now we do it again, but here, we control the temporary creation
    # ourselves.  We use the output argument of all numpy functional forms of
    # the operators.

    # Initialize the array that will hold the output, empty
    z = np.empty_like(x)
    # This version in total uses 1 array for the result and one temporary.
    tmp = np.empty_like(x)

    # Now, we compute each term of the expression above.  Each time, we either
    # store the output back into the temporary or we accumulate it in z.

    # sin(x)
    sin(x,z)

    # + sin(2*x)
    add(z,sin(multiply(2,x,tmp),tmp),z)

    # - 4.5*cos(3*x**2)
    power(x,2,tmp)
    multiply(3,tmp,tmp)
    cos(tmp,tmp)
    multiply(4.5,tmp,tmp)
    subtract(z,tmp,z)
    
    # Verify that the two forms match to 13 digits
    nptest.assert_almost_equal(y,z,13)


def test2():
    """Compute the same expression, using in-place operations
    """
    x = np.linspace(0,2*pi,100)

    y = sin(x) + sin(2*x) - 4.5*cos(3*x**2)

    # This version of the code uses more in-place operators, which make it a
    # bit more readable and still avoid temporaries
    tmp = np.empty_like(x)

    # sin(x)
    z = sin(x)

    # + sin(2*x)
    z += sin(multiply(2,x,tmp),tmp)

    # - 4.5*cos(3*x**2)
    power(x,2,tmp)
    tmp *= 3
    cos(tmp,tmp)
    tmp *= 4.5
    z -= tmp
    
    # Verify that the two forms match to 13 digits
    nptest.assert_almost_equal(y,z,13)

if __name__ == '__main__':
    nose.runmodule(exit=False)
