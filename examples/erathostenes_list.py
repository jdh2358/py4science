#!/usr/bin/env python
"""Simple example implementations of the Sieve of Erathostenes."""

import sys
import math

import numpy as N

def sieve(nmax):
    """Return a list of prime numbers up to nmax.

    Naive, O(N^2) implementation using the Sieve of Erathostenes."""

    # Sanity checks
    assert nmax>1, "nmax must be > 1"
    if nmax == 2: return [2]
    
    # For nmax>3, do full sieve
    primes_head = [2]
    first = 3
    primes_tail = N.arange(first,nmax+1,2)
    while first <= round(math.sqrt(primes_tail[-1])):
	first = primes_tail[0]
	primes_head.append(first)
	non_primes = first * primes_tail
	primes_tail = N.array([ n for n in primes_tail[1:]
                                if n not in non_primes ])

    return primes_head + primes_tail.tolist()
