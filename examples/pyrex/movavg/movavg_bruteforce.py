"""
Use a brute force, slow method
"""
import numpy

x = numpy.random.rand(10000)

data = []
for i in range(len(x)):
    slice = x[max(0, i-30):i+1]  # slice out the recent history
    data.append([slice.mean(), slice.std(), slice.min(), slice.max(), numpy.median(slice), len(slice)])

r = numpy.rec.fromarrays(data,names='dmean,dstd,dmin,dmax,dmedian,ngood')

