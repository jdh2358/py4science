"""Basic functionality for iterated maps"""

import math
import scipy
from matplotlib import pylab
from IterateMaps import BifurcationDiagram,Iterate,IterateArray

# Simple, closure-based implementations.  This is the fastest approach of all
# I tried.  Surprisingly, it seems as fast for a Bifurcation map as making a
# single instance with a named f.param argument and resetting f.param
# manually.

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

# More complex, but more flexible class-based approach.  The resulting maps
# are richer objects, with builtin plotting and other facilities.
class Map:
    """Class representing generic discrete maps.

    This produces callable instances and allows for multi-parameter maps with
    a natural syntax.

    However, there is an extra overhead in calling the map each time, since
    the call method delegates to the constructor-supplied map function.

    Additionally, the constructor is relatively expensive, so this kind of map
    will prove slow to use for parametric studies which create large numbers
    of instances.  In such cases, a lighter-weight closure-based approach may
    be preferable."""
    
    def __init__(self,mapfn,domain=(0,1),vector=False):
        """Construct and return a map instance.

        The resulting map is a callable, which can be evaluated over the given
        domain (no actual checks are made at call time for efficiency reasons).
        
        Inputs:

          - mapfn: map function, to be called at evaluation time.

          - domain((0,1)): a tuple specifying the domain of the map, used to
          set the default plotting interval.

          - name(None): string naming the map, used in plotting methods.

          - vector(False): if True, it is assumed that the map is
          vectorizable; that is, it can be called with array arguments as well
          as scalars.  This can be used by other algorithms for speed reasons
          (the .plot method makes use of this information).
          """

        self.mapfn = mapfn
        self.domain = domain
        self.vector = vector

    def __call__(self,x):
        "Apply the map to an argument"
        return self.mapfn(x)

    def plot(self,x0=None,x1=None,npts=400,title=None):
        """Produce a plot of the map over the specified domain.

        Inputs:

          - x0, x1 (None): endpoints for the plot.  If not given, the map's
          domain is used.

          - npts(400): number of points to plot with.

          - title(None): if True, the map's name is used as the plot's title.
          A string can be given to set the title explicitly.
          """

        # choose plotting domain
        if x0 is None: x0 = self.domain[0]
        if x1 is None: x1 = self.domain[1]
        x = scipy.linspace(x0,x1,npts)
        # compute map values
        if self.vector:
            y = self.mapfn(x)
        else:
            y = scipy.array(map(self.mapfn,x))
        # actual plot and title
        pylab.plot(x,y)
        if title == True:
            title = self.name
        if title:
            pylab.title(title)

    def BifurcationDiagram(self, x0, nTransient, nCycle, etaArray,marker='k.'):
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
        eta_save = self.mu
        for eta in etaArray:
            etaList.extend([eta]*nCycle)
            self.mu = eta
            f = self.mapfn
            xList.extend(IterateArray(f, Iterate(f, x0, nTransient),nCycle))
        pylab.plot(etaList, xList, marker)

# some class-based factory functions with the same top-level API as the
# closure-based ones.
def logistic_cl(mu):
    """Return a logistic map function with fixed mu.
    
    Logistic map f(x) = 4 mu x (1-x), which folds the unit interval (0,1)
    into itself.
    """
    # this reduces the number of unnecessary multiplications when calling
    mu4 = 4*mu
    
    def f(x):
        return mu4*x*(1.-x)

    return Map(f,vector=True)

def sine_cl(B):
    """Return a sine map function with fixed B.
    
    Sine map f(x) = 4 B sin(pi*x)
    """
    sin,pi = scipy.sin, scipy.pi
    def f(x):
        return B*sin(pi*x)
    
    return Map(f,dict(B=B),vector=True,
               name='Sine map, B=%.2g' % B)

def demo(map_type=logistic,npts=300,marker='k.'):
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
    demo(logistic)
    demo(sine,marker='r.')
    
    # demo of the richer class-based maps
##    smap = sine_cl(0.5)
##    pylab.figure()
##    smap.plot(title=True)

##    pylab.show()
