from maplib import Logistic,Sine
from matplotlib.numerix import arange, pi, sqrt, sort, zeros,ones, Float
from matplotlib.numerix.mlab import rand
from pylab import figure, draw, show, ion, ioff,frange,gcf,rcParams,rc

def bifurcation_diagram(map_type,param0=0,param1=1,nparam=300,
                        ntransients=100,ncycles=200, dotcolor="0.5",
                        fig=None,
                        nboundaries=0):

    if nboundaries:
        boundaries = zeros((nparam,nboundaries),Float)
    params = frange(param0,param1,npts=nparam)
    bound_rng = range(nboundaries)
    xs = []
    ys = []
    for idx,param in enumerate(params):
        m = map_type(param)
        y = m.iterate(m.iterate(0.5,ntransients,lastonly=True),
                      ncycles, lastonly=False)
        xs.extend(param*ones(len(y)))
        ys.extend(y)
        if nboundaries:
            # the boundaries are the iterates of the map's maximum, we assume
            # here that it's located at 0.5
            boundaries[idx] = m.iterate(0.5,nboundaries,lastonly=False)[1:]
    if fig is None:
        fig = figure()
    ax = fig.add_subplot(111)
    # save state (John, is there a cleaner way to do this?)
    
    ax.plot(xs, ys, '.', mfc=dotcolor, mec=dotcolor, ms=1, mew=0)

    bound_lines = []
    for i in bound_rng:
        bound_lines.extend(ax.plot(params,boundaries[:,i]))

    def toggle(event):
        if event.key!='t': return
        
        for a in bound_lines:
            v = a.get_visible()
            a.set_visible(not v)
        fig.canvas.draw()
        
    fig.canvas.mpl_connect('key_press_event', toggle)
    return fig

def cobweb(mu, walkers=10, steps=7):
    f = figure()
    ax = f.add_subplot(111)
    interval = frange(0.0, 1.0, npts=100)
    logmap = Logistic(mu)
    logmap.plot(ax, interval, lw=2)
    for x0 in rand(walkers):
        logmap.plot_cobweb(ax, x0, steps, lw=2)
    ax.set_title('Ex 2A: Random init. cond. for mu=%1.3f'%mu)
    return f

def invariant_density(mu, x0,cycles=1000000,ret_all=False):
    transients = 1000
    bins = 500
    f = figure()
    ax = f.add_subplot(111)
    logmap = Logistic(mu)
    y = logmap.iterate(x0, transients, lastonly=True)
    y = logmap.iterate(y, cycles, lastonly=False)
    n, bins, patches = ax.hist(y, bins, normed=1)
    ax.set_xlim(0,1)
    if ret_all:
        return f,logmap,n
    else:
        return f
    

# Exercise solutions
def ex2A():
    cobweb(0.2)
    cobweb(0.4)
    cobweb(0.6)
    

def ex2B():
    def rho(x):
        return 1./(pi * sqrt( x*(1.-x)))

    # Don't start from 0.5, which is a fixed point!
    f = invariant_density(1.0,0.567)
    ax = f.gca()
    # avoid the edges: rho(x) is singular at 0 and 1!
    x0 = frange(0.001, 0.999, npts=1000)
    l, = ax.plot(x0, rho(x0), 'r-', lw=3, alpha=0.5)
    ax.set_title('Ex 2B: invariant density')
    ax.legend((ax.patches[0], l), ('empirical', 'analytic'), loc='upper center')
    ax.set_xlim(0,1)
    ax.set_ylim(0,10)
    

def ex2CD(mu=0.9,x0=0.64):
    
    f,logmap,n = invariant_density(mu,x0,ret_all=True)
    ax = f.gca()
    ax.set_xticks(frange(0,1,npts=10))
    ax.grid(True)
    # Now, iterate x=1/2 a few times and plot this 'orbit', which corresponds
    # to peaks in the invariant density.
    x0 = 0.5
    pts = logmap.iterate(x0,10)
    pts_y = 0.5*frange(1,max(n),npts=len(pts))
    ax.plot(pts,pts_y,'ro-')
    ax.set_title('Ex 2C/D: Analytics of cusps at mu=%0.2g' % mu)
    

def ex2E():
    par0 = 0.8
    par1 = 1.0
    fig = bifurcation_diagram(Logistic,par0,par1,nparam=1000,
                              nboundaries=8)
    fig.gca().set_title('Ex 2E: Bifurcation diag. with boundaries (press t)')
    fig = bifurcation_diagram(Logistic,par0,par1,dotcolor='blue')
    fig = bifurcation_diagram(Sine,par0,par1,dotcolor='red',fig = fig)
    fig.gca().set_title('Ex 2E: Bifurcation diag. logistic/sine maps')
    

if __name__=='__main__':
    ex2A()
    ex2B()
    ex2CD()
    ex2E()
    show()
