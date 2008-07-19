#!/usr/bin/env python

import numpy as np

import simple

def test_linspace():
    """Test both versions of linspace for consistency."""
    n,x,y = 5, 0, 2.0
    a = np.empty(n)

    simple.linspace(x,y,a)
    print a

    b = simple.linspace2(x,y,n)
    print b

    np.testing.assert_almost_equal(a,b,15)

if __name__ == '__main__':
    test_linspace()
