"""
WARNING: this code does NOT run yet.  I haven't finished updating it (fperez)

Period Doubling exercise.
"""

import scipy
from IterateMaps import IterateArray

def PlotIterate(g, x0, N):
    """
    Plots g, the diagonal y=x, and the boxes made of the segments
    [[x0,x0], [x0, g(x0)], [g(x0), g(x0)], [g(x0), g(g(x0))], ...
    """
    traj = IterateArray(g, x0, N)
    xs = []
    for x in traj:
        xs.extend([x,x])
    ys = xs[1:]
    xs = xs[0:-1]
    funcplotx = scipy.linspace(0,1,100)
    funcploty = scipy.array(map(g,funcplotx))
    pylab.plot(xs, ys, 'b-', linewidth=1, antialiased=True)
    pylab.plot(funcplotx, funcploty, 'g-', linewidth=3, antialiased=True)
    pylab.plot([0.0, 1.0], [0.0, 1.0], 'r-', linewidth=3, antialiased=True)

def FastBifurcationDiagram(x0, ntransient, ncycleMax, muarray,g):
    mus = []
    trajs = []
    for mu in muarray:
        if mu < 0.75: 
	    ncycle = 2
	elif mu < (1. + scipy.sqrt(6.))/4.0:
	    ncycle = 4
        else:
	    ncycle = ncycleMax
        mus.extend([mu]*ncycle)
        trajs.extend(IterateArray(g, Iterate(g, x0, ntransient),ncycle))
    pylab.plot(mus, trajs, 'k.')
    pylab.show()

def FastBifurcationDiagramWithBoxes(x0, ntransient, ncycleMax, muarray, 
                                    mu, muInfinity, g=f, nBoxes=7, 
				    sY1=0.07, sY2=0.16, xMax=0.5,
				    plotXMin = 0.4, plotXMax = 1.0,
				    plotYMin = 0.3, plotYMax = 0.7):
    pylab.plot()
    pylab.grid('off')
    pylab.axis([plotXMin,plotXMax,plotYMin,plotYMax])
    xMin = g(g(0.5,muInfinity),muInfinity) 
    for n in range(nBoxes):
        nIterated = 2**n
	xMax = Iterate(g(muInfinity), xMin, 2*nIterated)
        boxHoriz = [mu[n], mu[n], muInfinity, muInfinity, mu[n]]
	boxVert = [xMin, xMax, xMax, xMin, xMin]
	pylab.plot(boxHoriz, boxVert, 'r-', linewidth=3, antialiased=True)
	xMin = xMax
    mus = []
    trajs = []
    for mu in muarray:
      if (mu>=plotXMin) and (mu <= plotXMax):
        if mu < 0.75: 
	    ncycle = 2
	elif mu < (1. + scipy.sqrt(6.))/4.0:
	    ncycle = 4
        else:
	    ncycle = ncycleMax
        traj = IterateArray(g, Iterate(g, x0, ntransient), ncycle)
        trajPruned = [y for y in traj if (y>=plotYMin) and (y <= plotYMax)]
	trajs.extend(trajPruned)
        mus.extend([mu]*len(trajPruned))
    pylab.plot(mus, trajs, 'k.')
    pylab.show()

def makeFBDWB(maptype=Maps.logistic):
    mus, deltas, alphas, muInfinity = FindScalingConvergence(maptype,9) 
    FastBifurcationDiagramWithBoxes(0.1,2000,128,scipy.linspace(0.4,1.0,600),
                                    mus, muInfinity)

# Only for solution
def FixedPointIteratedMap(g, x0, nIterated):
    """
    Returns fixed point g^[nIterated](x*) = x*

    Defines a temporary function, fn(x)
    which iterates g nIterated times (Iterate except with only one argument)
    """
    fn = lambda x: Iterate(g, x, nIterated)
    xf = scipy.optimize.fixed_point(fn, x0)
    return xf

def FindSuperstable(g, nIterated, etaMin, etaMax, xMax=0.5):
    """
    Finds superstable orbit g^[nIterated](xMax, eta) = xMax
    in range (etaMin, etaMax). 
    Must be started with g-xMax of different sign at etaMin, etaMax.
   
    Uses scipy.optimize.brentq, defining a temporary function, fn(eta)
    which is zero for the superstable value of eta.

    fn iterates g nIterated times and subtracts xMax
    (basically Iterate - xMax, except with only one argument eta)
    """
    fn = lambda eta: Iterate(g(eta), xMax, nIterated)-xMax
    eta_root = scipy.optimize.brentq(fn, etaMin, etaMax)
    return eta_root


def GetSuperstablePoints(g, nMax, eta0, eta1, xMax=0.5):
    """
    Given the parameters for the first two superstable parameters eta_ss[0] 
    and eta_ss[1], finds the next nMax-1 of them up to eta_ss[nMax].
    Returns dictionary eta_ss 

    Usage:
        Find the value of the parameter eta_ss[0] = eta0 for which the fixed
	point is xMax and g is superstable (g(xMax) = xMax), and the 
	value eta_ss[1] = eta1 for which g(g(xMax)) = xMax, either 
	analytically or using FindSuperstable by hand.
        mus = GetSuperstablePoints(f, 9, eta0, eta1)

    Searches for eta_ss[n] in the range (etaMin, etaMax), 
    with etaMin = eta_ss[n-1] + epsilon and
    etaMax = eta_ss[n-1] + (eta_ss[n-1]-eta_ss[n-2])/A
    where A=3 works fine for the maps I've tried.
    (Asymptotically, A should be smaller than but comparable to delta.)
    """
    eps = 1.0e-06
    A = 3.
    eta_ss = {0:eta0, 1:eta1}
    for n in scipy.arange(2, nMax+1):
        etaMin = eta_ss[n-1] + eps
        etaMax = eta_ss[n-1] + (eta_ss[n-1]-eta_ss[n-2])/A
        nIterated = 2**n
        eta_ss[n] = FindSuperstable(g, nIterated, etaMin, etaMax, xMax)
    return eta_ss


def DeltaAlpha(g, eta_ss, xMax=0.5):
    """
    Given superstable 2^n cycle values eta_ss[n], calculates 
    delta[n] = (eta_{n-1}-eta_{n-2})/(eta_{n}-eta_{n-1}),
    sep[n] = distance from xMax to attractor point halfway around circle,
    and alpha = sep[n-1]/sep[n]

    Also extrapolates eta to etaInfinity using definition of delta and 
    most reliable value for delta:
    delta = lim{n->infinity} (eta_{n-1}-eta_{n-2})/(eta_n - eta_{n-1})

    Returns delta and alpha dictionaries for n>=2, and etaInfinity
    """
    delta = {}
    alpha = {}
    sep = {}
    sep[1] = g(eta_ss[1])(xMax) - xMax
    nMax = max(eta_ss.keys())
    for n in range(2, nMax+1):
        delta[n] = (eta_ss[n-1]-eta_ss[n-2])/(eta_ss[n]-eta_ss[n-1])
        nIterated = 2**n
        sep[n] = Iterate(g(eta_ss[n]), xMax, nIterated/2)-xMax
        alpha[n] = sep[n-1]/sep[n]
    etaInfinity = eta_ss[nMax] + (eta_ss[nMax]-eta_ss[nMax-1])/(delta[nMax]-1.0)
    return delta, alpha, etaInfinity

def FindScalingConvergence(g, nMax, xMax=0.5):
    """
    Finds eta0, eta1:
      Assumes superstable fixed point eta0 is between 0.3 and 1,
      superstable period two cycle eta1 is between eta0+epsilon and 1
    Calls GetSuperstablePoints
    Calls DeltaAlpha
    Returns etas, deltas, alphas, etaInfinity
    """
    eps = 1.0e-6
    eta0 = FindSuperstable(g, 1, 0.3, 1.0, xMax)
    eta1 = FindSuperstable(g, 2, eta0 + eps, 1.0, xMax)
    etas = GetSuperstablePoints(g, nMax, eta0, eta1, xMax)
    deltas, alphas, etaInfinity = DeltaAlpha(g, etas, xMax)
    return etas, deltas, alphas, etaInfinity

def PlotFIterated(g, n, args):
    """
    Plots g^[2^n](x,*args) versus x, along with the curve y=x.
    Also can plot box with corners (1-x*, 1-x*), (x*, x*) 
    """
    nIter = 2**n
    # Curve
    xs = scipy.arange(0.,1.000001,0.00002) 
    ys = [Iterate(g, x, nIter, args) for x in xs]
    # Diagonal
    pylab.plot(xs, ys, 'b-', linewidth=3)
    pylab.plot([0.0,1.0],[0.0,1.0],'k-', linewidth=3)
    # Box
    fnMax = lambda x: g(x,*args) -x
    xStarMax = scipy.optimize.brentq(fnMax, 0.5,1.0)
    fnMin = lambda x: g(x,*args) -xStarMax
    xStarMin = scipy.optimize.brentq(fnMin, 0.0,0.5)
    boxX = [xStarMin, xStarMin, xStarMax, xStarMax, xStarMin]
    boxY = [xStarMin, xStarMax, xStarMax, xStarMin, xStarMin]
    pylab.plot(boxX, boxY,'r-', linewidth=2)
    pylab.show()


def PlotFIteratedAllBoxes(g, nMax, args, alpha, save=False):
    # Curve
    xs = scipy.arange(0.,1.000001,0.0002) 
    ys = [Iterate(g, x, 2.0**nMax, args) for x in xs]
    # Diagonal
    pylab.plot(xs, ys, 'b-', linewidth=3)
    pylab.plot([0.0,1.0],[0.0,1.0],'k-', linewidth=3)
    # Box
    boxX = {}
    boxY = {}
    scale = 1.0
    maxBoxLog2n = nMax
    for n in range(maxBoxLog2n):
        fnMax = lambda x: Iterate(g, x, 2**n, args) -x
        xStarMax = scipy.optimize.brentq(fnMax, 0.5,0.5+0.5/scale)
        fnMin = lambda x: Iterate(g, x, 2**n, args) - xStarMax
        xStarMin = scipy.optimize.brentq(fnMin, 0.5-0.5/scale,0.5)
        boxX[n] = [xStarMin, xStarMin, xStarMax, xStarMax, xStarMin]
        boxY[n] = [xStarMin, xStarMax, xStarMax, xStarMin, xStarMin]
        pylab.plot(boxX[n], boxY[n],'r-', linewidth=2)
	scale *= alpha
    pylab.hold('off')
    pylab.show()
    if save:
        output = file('PlotFIterate.dat','w')
        for x,y in zip(xs, ys):
            output.write("%g %g\n"%(x,y))
        output.write("\n")
        for n in range(maxBoxLog2n):
	    for x,y in zip(boxX[n],boxY[n]):
                output.write("%g %g\n"%(x,y))
            output.write("\n")
        for x,y in [(0.0,0.0),(1.0,1.0)]:
            output.write("%g %g\n"%(x,y))
        output.close()

def XStar(g, args=(), xMax = 0.5):
    """
    Finds fixed point of one-humped map g, which is assumed to be
    between xMax and 1.0.
    """
    gXStar = lambda x: g(x, *args) - x
    return scipy.optimize.brentq(gXStar, xMax, 1.0)

def Alpha(g, args=(), xMax = 0.5):
    """
    Finds the (negative) scale factor alpha which inverts and rescales
    the small inverted region of g(g(x)) running from (1-x*) to x*.
    """
    gWindowMax = XStar(g, args, xMax)
    gWindowMinFunc = lambda x: g(x, *args) - gWindowMax
    gWindowMin = scipy.optimize.brentq(gWindowMinFunc, 0.0, xMax)
    return 1.0/(gWindowMin-gWindowMax)

class T:
    """
    Creates a new function T[g] from g, implementing Feigenbaum's
    renormalization-group transformation of function space into itself.

    We define it as a class so that we can initialize alpha and xStar,
    which otherwise would need to be recalculated each time T[g] was
    evaluated at a point x.

    Usage:
        Tg = T(g, args)
        Tg(x) evaluates the function at x
    """
    def __init__(self, g, args=(), xMax=0.5):
        """
	Stores g and args. 
	Calculates and stores xStar and alpha.
	"""
	self.args = args
        self.xStar = XStar(g, args, xMax)
        self.alpha = Alpha(g, args, xMax)
	self.g = g
    def __call__(self, x):
        """
        Defines xShrunk to be x/alpha + x*
	Evaluates g2 = g(g(xShrunk))
	Returns expanded alpha*(g2-xStar)
	"""
        xShrunk = x/self.alpha + self.xStar
        g2 = self.g(self.g(xShrunk, *(self.args)), *(self.args))
        return self.alpha * (g2 - self.xStar)
    
def PlotTgVsG(g, args, xMax=0.5):
    """Plots Tg(x) and g(x) on the same plot, for x from (0,1)"""
    xs = scipy.arange(0., 1., 0.01)
    gs = []
    Tg = T(g, args)
    Tgs = []
    for x in xs:
       gs.append(g(x, *args))
       Tgs.append(Tg(x))
    pylab.plot(xs, gs, xs, Tgs)
    pylab.show()


def PlotTIterates(g, args, nMax = 2, xMax=0.5):
    """
    Plots g(x), T[g](x), T[T[g]](x) ... 
    on the same plot, for x from (0,1)
    """
    xs = scipy.arange(0., 1., 0.01)
    Tg = {}
    Tg[0] = lambda x: g(x, *args)
    for n in range(1,nMax+1):
        Tg[n] = T(Tg[n-1], xMax=xMax)
    TgValues = {}
    pylab.plot([0.0,1.0],[0.0,1.0])
    for n in range(nMax+1):
        TgValues[n] = [] 
        for x in xs:
            TgValues[n].append(Tg[n](x))
        pylab.plot(xs, TgValues[n])
    pylab.show()


def PlotT2FVsT2Fsin():
    """
    Plots T[T[f]](x), T[T[fsin]](x) ... 
    on the same plot, for x from (0,1)
    """
    xs = scipy.arange(0., 1., 0.01)
    mus, deltas, alphas, muInfinity =  FindScalingConvergence(f, 9)
    mus, deltas, alphas, BInfinity =  FindScalingConvergence(fsin, 9)

    T2F = T(T(f, args=(muInfinity,)))
    T2Fsin = T(T(fsin, args=(BInfinity,)))

    pylab.plot([0.0,1.0],[0.0,1.0])
    
    T2FValues = [] 
    T2FsinValues = [] 
    for x in xs:
        T2FValues.append(T2F(x))
	T2FsinValues.append(T2Fsin(x))
    pylab.plot(xs, T2FValues, "r-", xs, T2FsinValues, "g-")
    pylab.show()

def demo():
    """Demonstrates solution for exercise: example of usage"""
    print "Period Doubling Demo"
    print "Close plots to continue"
    mus, deltas, alphas, muInfinity = FindScalingConvergence(f,9)
    print "  Fixed Point, mu=0.7"
    print "  (Close plot to continue)"
    PlotIterate(f,0.1,20,(0.7,))
    print "  Period Doubling: mu=0.8"
    PlotIterate(f,0.1,100,(0.8,))
    print "  Chaos: mu=0.9"
    x0 = Iterate(f,0.5,100,(0.9,))
    PlotIterate(f,x0,100,(0.9,))
    print "  Onset of Chaos: mu=muInfinity"
    x0 = Iterate(f,0.5,100,(muInfinity,))
    PlotIterate(f,x0,100,(muInfinity,))
    print "  Scaling in Bifurcation Diagram"
    # Optional
    FastBifurcationDiagramWithBoxes(0.1,2000,128,scipy.arange(0.4,1.0,0.002),
    				    mus,muInfinity)
    print "  Convergence of alpha, delta, mu to scaling values"
    pylab.plot(mus.keys(), mus.values(), "ro", label="mu")
    pylab.plot(deltas.keys(), deltas.values(), "go", label = "delta")
    pylab.plot(alphas.keys(), alphas.values(), "bo", label = "alpha")
    pylab.legend()
    pylab.show()
    print "  Renormalization-group Transformation"
    PlotFIterated(f, 1, (muInfinity,))
    print "  Renormalization-group Transformation Twice"
    # Optional
    PlotFIteratedAllBoxes(f, 2, (muInfinity,), alphas[9])
    print "  Repeated renormalization-group transformations"
    PlotTIterates(f, (muInfinity,))
    print "  Universality: T^2 of sine map and logistic map agree"
    print "  (Zoom in to see difference)"
    PlotT2FVsT2Fsin()
    pylab.show()

if __name__=="__main__":
   demo()


