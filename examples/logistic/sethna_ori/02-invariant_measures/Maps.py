"""Basic functionality for iterated maps"""

import scipy
from matplotlib import pylab
from IterateMaps import BifurcationDiagram

def logistic(mu):
    """Return a logistic map function with fixed mu.
    
    Logistic map f(x) = 4 mu x (1-x), which folds the unit interval (0,1)
    into itself.
    """
    mu4 = 4*mu
    def f(x):
        return mu4*x*(1.-x)
    return f

def sine(B):
    """Return a sine map function with fixed B.
    
    Sine map f(x) = B sin(pi*x)
    """
    sin = math.sin
    pi = math.pi
    
    def f(x):
        return B*sin(pi*x)
    return f

def demo(mapfn=logistic,npts=1000,marker='k.'):
    """Demonstrates solution for exercise: example of usage"""
    print "Map iteration Demo"
    print "Map:",mapfn
    print "Close plot to continue"
    print "  Creating Bifurcation Diagram"
    BifurcationDiagram(mapfn, 0.1, 500, 128,
                       scipy.linspace(0,1,npts),marker=marker)
    pylab.show()

if __name__=="__main__":
    demo(logistic)
    demo(sine,marker='r.')
