"""Basic functionality for iterated maps"""

import scipy
from matplotlib import pylab
from IterateMaps import Iterate,IterateArray

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
    f = g(etaArray[0])
    for eta in etaArray:
        etaList.extend([eta]*nCycle)
        f.param = eta
        xList.extend(IterateArray(f, Iterate(f, x0, nTransient),nCycle))
    pylab.plot(etaList, xList, marker)

# Simple, attribute-based implementations
def logistic_cl(mu):
    """Return a logistic map function with fixed mu.
    
    Logistic map f(x) = 4 mu x (1-x), which folds the unit interval (0,1)
    into itself.
    """
    def f(x):
        return 4*f.param*x*(1.-x)
    f.param = mu
    
    return f

def sine_cl(B):
    """Return a sine map function with fixed B.
    
    Sine map f(x) = 4 B sin(pi*x)
    """
    import math
    def f(x):
        return f.param*math.sin(math.pi*x)
    f.param = B

    return f


def demo(map_type=logistic_cl,npts=300,marker='k.'):
    """Demonstrates solution for exercise: example of usage"""
    print "Map iteration Demo"
    print "Map:",map_type
    print "Close plot to continue"
    print "  Creating Bifurcation Diagram"
    BifurcationDiagram(map_type, 0.1, 500, 128,
                       scipy.linspace(0,1,npts),marker=marker)
    pylab.show()

if __name__=="__main__":
    # quick bifurcation demos using the fast closures
    demo(logistic_cl)
    demo(sine_cl,marker='r.')
