"""
Example code showin how to use the ringbuf extension code from python
"""
import numpy as np
import random
import ringbuf

r = ringbuf.Ringbuf(30)

for i in range(100):
    val = random.random()
    indsorted = r.add(val)
    ng = r.N_good()
    percentile = indsorted/float(ng)
    print 'val=%1.4f, Nadded=%d, Ngood=%d, Nsorted=%d, percentile=%1.4f, min=%1.2f, max=%1.2f, mean=%1.2f, std=%1.2f'%(val, r.N_added(), r.N_good(), indsorted, percentile, r.min(), r.max(), r.mean(), r.sd())

print 'slice', r[:10]
