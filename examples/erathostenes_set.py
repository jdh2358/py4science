#!/usr/bin/env python
"""Simple example implementations of the Sieve of Erathostenes."""

__author__ = "Fernando Perez <Fernando.Perez@colorado.edu>"

import sys
import math

import numpy as N

def sieve(nmax):
    """Return a list of prime numbers up to nmax, using Erathostenes' sieve.

    This is a more efficient implementation than the naive one: we combine a
    set with an auxiliary list (kept sorted)."""

    # Sanity checks
    assert nmax>1, "nmax must be > 1"
    if nmax == 2: return [2]
    
    # For nmax>3, do full sieve
    primes_head = [2]
    first = 3

    # The primes tail will be kept both as a set and as a sorted list
    primes_tail_lst = range(first,nmax+1,2)
    primes_tail_set = set(primes_tail_lst)

    # optimize a couple of name lookups from loops
    tail_remove = primes_tail_set.remove
    head_append = primes_head.append
    sqrt = math.sqrt
	
    # Now do the actual sieve
    while first <= round(sqrt(primes_tail_lst[-1])):
	# Move the first leftover prime from the set to the head list
	first = primes_tail_lst[0]
	tail_remove(first)  # remove it from the set
	head_append(first) # and store it in the head list

	# Now, remove from the primes tail all non-primes.  For us to be able
	# to break as soon as a key is not found, it's crucial that the tail
	# list is always sorted.
	for next_candidate in primes_tail_lst:
	    try:
		tail_remove(first*next_candidate)
	    except KeyError:
		break
            
	# Build a new sorted tail list with the leftover keys
	primes_tail_lst = list(primes_tail_set)
	primes_tail_lst.sort()

    return primes_head + primes_tail_lst
