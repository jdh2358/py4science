"""Simple quicksort implementation."""

def qsort(lst):
    """Return a sorted copy of the input list."""

    raise NotImplementedError

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
