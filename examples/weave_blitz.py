#!/usr/bin/env python
"""Simple comparison of weave.blitz versus pure Numpy """

from __future__ import division

import sys, time

import numpy as np
from scipy import weave
from pylab import figure,subplot, plot, show, legend, xlabel, ylabel, title

rand = np.random.rand

Nadds = 12
Nevals = 10
shape = 2000,2000

x = rand(*shape)

if sys.platform == 'win32':
    now = time.clock
else:
    now = time.time

def repeat_nadds(Nadds, Nevals, useWeave):
    """
    Time the addition of i=2,Nadds arrays.  Evaluate each expression
    Nevals times to produce accurate timing results.  If useWeave is
    True, use weave to inline the addition, else use Numeric

    return value is n,t where n is a list of the the number of arrays
    added and t is the average time it took to add the arrays
    """
    results = []
    for i in range(2,Nadds):
        s = 'result = %s' % '+'.join(['x']*i)
        print 'evaluating: %s with weave=%s' % (s,useWeave)
        # store times here
        times = [None,]*(Nevals+1)
        # compute all we can outside the timing loop
        evalRng = range(Nevals)
        blitz = weave.blitz
        # Repeat the full loop to minimize non-numerical work inside, which
        # can disrupt timings
        if useWeave:
            # only weave needs to predefine result array
            result= np.empty(shape,dtype=float)
            times[0] = now()
            for j in evalRng:
                blitz(s)
                times[j+1] = now()-times[j]
        else:
            times[0] = now()
            for j in evalRng:
                exec(s)
                times[j+1] = now()-times[j]
        # pick the best of the running times
        elapsed = min(times[1:])
        print '\tNadds=%d  Elapsed=%1.2f' % (i, elapsed)
        results.append( (i, elapsed) )
    return zip(*results)
        
# evaluate weave 
nw, tw = repeat_nadds(Nadds, Nevals, useWeave=True)
# evaluate Numeric
nn, tn = repeat_nadds(Nadds, Nevals, useWeave=False)

# plot weave versus Numeric
figure()
ax = subplot(111)
plot(nw, tw, 'go', nn, tn, 'bs')
legend( ('Blitz', 'Numpy') )
xlabel('num adds')
ylabel('time (s)')
title('numpy vs weave; repeated adds, shape: %s' % (shape,))
ax.set_xlim( (0, Nadds+1))
show()       
