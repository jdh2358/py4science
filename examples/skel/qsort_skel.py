"""Simple quicksort implementation.

From http://en.wikipedia.org/wiki/Quicksort:

function quicksort(array)
     var list less, greater
     if length(array) ≤ 1  
         return array  
     select and remove a pivot value pivot from array
     for each x in array
         if x ≤ pivot then append x to less
         else append x to greater
     return concatenate(quicksort(less), pivot, quicksort(greater))
"""

def qsort(lst):
    """Return a sorted copy of the input list."""

    raise NotImplementedError

#-----------------------------------------------------------------------------
# Tests
#-----------------------------------------------------------------------------
import random

import nose.tools as nt

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

if __name__ == '__main__':
    # From the command line, run the test suite
    import nose
    # This call form is ipython-friendly
    nose.runmodule(argv=['-s','--with-doctest'],
                   exit=False)
