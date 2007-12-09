"""
Example code showin how to use the ringbuf extension code from python
"""
import random
import ringbuf

r = ringbuf.Ringbuf(30)

for i in range(100):
    r.add(random.random())
    print 'Nadded=%d, Ngood=%d, min=%1.2f, max=%1.2f, mean=%1.2f, std=%1.2f'%(
        r.N_added(), r.N_good(), r.min(), r.max(), r.mean(), r.sd())

print 'slice', r[:10]
