#!/usr/bin/env python
"""
file with deliberate syntax errors to check IPython.
"""

g1='a global'

def f():
    1/0

    
class foo:
    """foo class docstring"""
    def __init__(self):
        """init ds"""
        pass
    
class bar:
    """bar class docstring"""
    def __init__(self):
        """bar init ds"""
        pass
    def __call__(self):
        """call ds"""
        print 'bar called!'

from Numeric import *
import time,sys

def Ramp(result, size, start, end):
    step = (end-start)/(size-1)
    for i in xrange(size):
        result[i] = start + step*i

def RampNum(result, size, start, end):
    step = (end-start)/(size-1)
    result[:] = arange(size+1)*step + start

def main():
    #print 'hi'
    size = 6000
    reps = 10
    array_normal = [0]*size
    t0=time.clock()
    for i in xrange(reps):
        Ramp(array_normal, size, 0.0, 1.0)
    Rtime = time.clock()-t0
    #print 'Ramp time:', Rtime

    t0=time.clock()
    array_num = zeros(size,'d')
    for i in xrange(reps):
        RampNum(array_num, size, 0.0, 1.0)
    RNtime = time.clock()-t0
    print 'RampNum time:', RNtime
    print 'speedup:',Rtime/RNtime


if __name__ == '__main__':
    main()
