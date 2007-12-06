import numpy
import sums

def sumpy(arr):

    total = 0.
    for val in x:
        total += val
    return total

x = numpy.arange(10)
y = numpy.random.rand(10,10)

print 'sum(x)', sums.sum_elements(x)
print 'sum2(x)', sums.sum_elements2(x)
print 'sum(y)', sums.sum_elements(y)
#print 'sum2(y)', sums.sum_elements2(y)

x = numpy.arange(1e6)
import time
start = time.time()
s1 = sums.sum_elements2(x)
now = time.time()
print 'pyrex time', now - start

start = time.time()
s1 = sumpy(x)
now = time.time()
print 'python time', now - start
