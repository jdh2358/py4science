"""
Use a brute force, slow method
"""
import numpy
import ringbuf

x = numpy.random.rand(10000)
dmean, dstd, dmin, dmax, dmedian, ng = ringbuf.runstats(x, 30)

r = numpy.rec.fromarrays([dmean, dstd, dmin, dmax, dmedian, ng],
                         names='dmean,dstd,dmin,dmax,dmedian,ngood')



