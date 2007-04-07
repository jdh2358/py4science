"""A simple weave exercise.

Problem: write a routine, called asum, which will correctly return the sum
of all the elements of a 1-d array.  Test that it does the right thing by
comparing to nx.sum() for the array
"""

from weave import inline,converters
import Numeric as nx

#-----------------------------------------------------------------------------
# Problem 1
# Let's fill up some arrays with numbers
array_bytes = nx.arange(256).astype(nx.UInt8)
array_short = nx.arange(256**2).astype(nx.UInt16)

# nx.sum has a problem.  What is it?
print 'WRONG'
print nx.sum(array_bytes)
print nx.sum(array_short)

# Now, a brute-force Python sum works OK
def pysum(arr):
    """Return the sum of all the elements in the array"""
    ss = 0
    for i in xrange(len(arr)):
        ss += arr[i]
    return ss

print 'RIGHT'
print pysum(array_bytes)
print pysum(array_short)

# but it's very slow.  Now write your own correct routine using weave.inline:
def asum(arr):
    raise NotImplementedError
