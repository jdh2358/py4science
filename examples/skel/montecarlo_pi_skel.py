#!/usr/bin/env python
"""Simple generation of pi via MonteCarlo integration.

To do:

- plot convergence

- plot timing comparisons

- implement using numpy

- binned numpy (to avoid creating a very large list,
"""

import random

import numpy as N

from scipy import weave
from scipy.weave import inline,converters


def v1(n = 100000):
    """Approximate pi via monte carlo integration"""

    XXX

    
def v2(n = 100000):
    """Implement v1 above using weave for the C call"""
    
    support = "#include <stdlib.h>"
    
    code = """
    double sm;
    float rnd;
    srand(1); // seed random number generator
    sm = 0.0;
    for(int i=0;i<n;++i) {
        rnd = rand()/(RAND_MAX+1.0);
        sm += sqrt(1.0-rnd*rnd);
    }
    return_val =  4.0*sm/n;"""
    return weave.inline(code,('n'),support_code=support)


def matprint(mat):
    """Simple matrix printer in C++ using weave and blitz.
    """
    nrow,ncol = mat.shape
    code = \
""" 
for(int i=0;i<nrow;i++) {
   for(int j=0;j<ncol;j++) {
     std::cout << mat(i,j) << " ";
   }

   // Line end after each row
   std::cout << std::endl;
}
"""
    # This function doesn't return anything
    inline(code,['mat','nrow','ncol'],
           # The type_converters argument allows us to access an array's
           # elements using arr(i,j) syntax inside the C++ code
           type_converters = converters.blitz)


# Returning a scalar quantity computed from an array
def trace(mat):
    """Return the trace of a matrix.
    """
    nrow,ncol = mat.shape
    code = \
""" 
// Here, compute the trace of 'mat' in C++, store it as variable 'tr'

// This sets the value returned by the function
return_val = tr;
"""
    return inline(code,['mat','nrow','ncol'],
                  type_converters = converters.blitz)


# In-place operations on arrays in general work without any problems
def in_place_mult(num,mat):
    """In-place multiplication of a matrix by a scalar.
    """
    nrow,ncol = mat.shape
    code = \
"""

"""
    inline(code,['num','mat','nrow','ncol'],
           type_converters = converters.blitz)


if __name__ == '__main__':

    # Monte Carlo Pi:
    print 'pi is:', math.pi
    print 'pi - python:',v1()
    print 'pi - weave :',v2()

    # make a simple 10x10 array
    a = N.arange(100)
    a.shape = 10,10

    # Print it using our printer
    print "array a:"
    matprint(a)

    # Print its trace
    print 'A trace:',a.trace()
    # And computed via our C++ code:
    print trace(a)

    # Multiply it in-place and compare:
    b = a.copy()
    
    in_place_mult(10,a)  # with our C++ code
    b *= 10  # Using the standard python operations

    print 'First row of a:',a[0]
    print 'First row of b:',b[0]
    
