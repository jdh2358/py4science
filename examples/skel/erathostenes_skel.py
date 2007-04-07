#!/usr/bin/env python
"""Simple example implementations of the Sieve of Erathostenes."""

import sys
import math

import numpy as N

def sieve(nmax):
    """Return a list of prime numbers up to nmax, using Erathostenes' sieve."""

    raise NotImplementedError

if __name__ == '__main__':
    # A simple test suite.
    import unittest

    # Make the generic test NOT be a subclass of unittest.TestCase, so that it
    # doesn't get picked up automatically.  Each subclass will specify an
    # actual sieve function to test.
    class sieveTestBase:

        def test2(self):
            self.assert_(self.sieve_func(2)==[2])

        def test100(self):
            primes100 = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41,
                         43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
            self.assert_(self.sieve_func(100)==primes100)

    # These subclasses define the actual sieve function to test.  Note that it
    # must be set as a staticmethod, so that the 'self' instance is NOT passed
    # to the called sieve as first argument.
    class sieveTestCase(sieveTestBase,unittest.TestCase):
        sieve_func = staticmethod(sieve)

        
    # This must be called LAST, because no code after it will be seen.
    unittest.main()
