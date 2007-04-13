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

if __name__ == '__main__':
    from unittest import main, TestCase
    import random

    class qsortTestCase(TestCase):
        def test_sorted(self):
            seq = range(10)
            sseq = qsort(seq)
            self.assertEqual(seq,sseq)

        def test_random(self):
            tseq = range(10)
            rseq = range(10)
            random.shuffle(rseq)
            sseq = qsort(rseq)
            self.assertEqual(tseq,sseq)
    main()
