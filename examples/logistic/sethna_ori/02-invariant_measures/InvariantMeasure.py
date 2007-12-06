"""Invariant Measure exercise"""

import scipy
from matplotlib import pylab
from IterateMaps import Iterate,IterateArray,BifurcationDiagram
import Maps

def PlotInvariantDensityWithBoundaries(g, x0, num_boundaries, xMax=0.5):
    """Plots the invariant density, together with the first num_boundaries
    iterates of xMax = 0.5 (which should coincide with folds, and hence
    cusps, in the invariant density). Plots the iterates f^[n](xMax) as red
    circles 'ro' at rho = n."""
    xAttractor = Iterate(g, x0, 1000)
    n, bins, patches = \
       pylab.hist(IterateArray(g, xAttractor, 1000000), 
                  bins = 2000, normed = 1)
    boundaries = IterateArray(g,xMax, num_boundaries)[1:]
    pylab.plot(boundaries, 1.+scipy.arange(len(boundaries)), 'ro-',
                 linewidth=1, antialiased=True)

# Plot bifurcation diagram; explain boundaries as images of x=1/2
def PlotBoundaries(g, nImages, etaArray, xMax=0.5):
    """
    For each parameter value eta in etaArray,
    iterate the point xMax nImages times, and plot the result
    (not including xMax) versus eta. We recommend using
       pylab.plot(etas, halfImages, 'ro')
    where the 'ro' will draw red circles.

    Usually xMax will be the peak in the function g (as hinted at by 
    its name).
    
    This can be used in conjunction with BifurcationDiagram to explain
    the boundary structure in the chaotic region. If you remove 
    pylab.show() from BifurcationDiagram, this plot will be 
    superimposed on the other.
    """
    for n in range(nImages):
        halfImages = [Iterate(g(eta), xMax, n+1) for eta in etaArray]
        pylab.plot(etaArray, halfImages, 'r-', linewidth=1, antialiased=True)
    pylab.axis([etaArray[0],etaArray[-1],0,1])

def demo(mapfn=Maps.logistic,arg=0.9,npts=50):
    """Demonstrates solution for exercise: example of usage"""
    print "Invariant Measure Demo"
    print "Close plots to continue"
    print "  Creating Invariant Density at mu=",arg
    PlotInvariantDensityWithBoundaries(mapfn(arg),0.1,20)
    print "  Creating Bifurcation Diagram With Boundaries"
    pylab.figure() # make a new figure so plots don't overlap
    etaArray = scipy.linspace(0.8,1,npts)
    BifurcationDiagram(mapfn, 0.1, 500, 128, etaArray)
    PlotBoundaries(mapfn, 6, etaArray)
    pylab.show()

if __name__=="__main__":
    demo()

