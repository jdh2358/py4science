"""Basic functionality for iterated maps"""

import scipy
from matplotlib import pylab

def Iterate(g, x0, N):
    """
    Iterate the function g N times, starting at x0, with extra parameters
    passed in as a tuple args. Return g(g(...(g(x))...)). Used to find a 
    point on the attractor starting from some arbitrary point x0.

    Calling Iterate for the Feigenbaum map at mu=0.9 would look like
        Iterate(logistic_map(0.9), 0.1, 1000)
    """
    
    for i in xrange(N):
        x0 = g(x0)
    return x0

def IterateArray(g, x0, N):
    """Iterate the function g N-1 times, starting at x0

    Returns the entire list 
    (x, g(x), g(g(x)), ... g(g(...(g(x))...))). 

    Can be used to explore the dynamics starting from an arbitrary point 
    x0, or to explore the attractor starting from a point x0 on the 
    attractor (say, initialized using Iterate).

    For example, you can use Iterate to find a point xAttractor on the 
    attractor and IterateArray to create a long series of points attractorXs
    (thousands, or even millions long, if you're in the chaotic region), 
    and then use
        pylab.hist(attractorXs, bins=500, normed=1)
        pylab.show()
    to see the density of points.
    """
    xs = scipy.empty(N,scipy.Float)
    xs[0] = float(x0)
    for i in xrange(1,N):
        xs[i] = g(xs[i-1])
    return xs

def BifurcationDiagram(g, x0, nTransient, nCycle, etaArray,marker='k.'):
    """
    For each parameter value eta in etaArray,
    iterate g nTransient times to find a point on the attractor, and then
    make a list nCycle long to explore the attractor.

    To generate etaArray, it's convenient to use frange: for example,
    BifurcationDiagram(f, 0.1, 500, 128, scipy.linspace(0,1,600)).

    Assemble the points on the attractors into a huge list xList, and the 
    corresponding values of eta onto a list of the same length etaList.
    Use
        pylab.plot(etaList, xList, 'k.')
        pylab.show()
    to visualize the resulting bifurcation diagram, where 'k.' denotes 
    black points.
    """
    etaList = []
    xList = []
    ones = scipy.ones
    for eta in etaArray:
        etaList.extend([eta]*nCycle)
        f = g(eta)
        xList.extend(IterateArray(f, Iterate(f, x0, nTransient),nCycle))
    pylab.plot(etaList, xList, marker)
