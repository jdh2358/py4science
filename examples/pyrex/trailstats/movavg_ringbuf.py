"""
Use a brute force, slow method
"""
import numpy
import ringbuf

r = ringbuf.Ringbuf(31)
x = numpy.random.rand(10000)

data = []
for thisx in x:
    r.add(thisx)
    data.append([thisx, r.N_good(), r.min(), r.max(), r.mean(), r.sd()])

r = numpy.rec.fromarrays(data,names='x,ngood,min30,max30,mean30,sd30')

