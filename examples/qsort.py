"""
Simple quicksort implementation.

See http://en.wikipedia.org/wiki/Quicksort for algorithm, pseudocode
and C implementation for comparison
"""

def qsort(lst):
    """Return a sorted copy of the input list."""

    if len(lst) <= 1:
        return lst

    # Select pivot and apply recursively
    pivot, rest   = lst[0],lst[1:]
    less_than     = [ lt for lt in rest if lt < pivot ]
    greater_equal = [ ge for ge in rest if ge >= pivot ]
    
    return qsort(less_than) + [pivot] + qsort(greater_equal)


#-----------------------------------------------------------------------------
# Tests
#-----------------------------------------------------------------------------
import random

import nose, nose.tools as nt

def test_sorted():
    seq = range(10)
    sseq = qsort(seq)
    nt.assert_equal(seq,sseq)

def test_random():
    tseq = range(10)
    rseq = range(10)
    random.shuffle(rseq)
    sseq = qsort(rseq)
    nt.assert_equal(tseq,sseq)

# If called from the command line, run all the tests
if __name__ == '__main__':
    # This call form is ipython-friendly
    nose.runmodule(argv=['-s','--with-doctest'],
                   exit=False)
