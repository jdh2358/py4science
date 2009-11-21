from maplib import Logistic, Sine

import numpy as np
import matplotlib
import matplotlib.pyplot as plt

def bifurcation_diagram(map_type, params, 
                        ntransients=100, ncycles=200, dotcolor="0.5",
                        fig=None,
                        nboundaries=2):
    """Plot a bifurcation diagram for an iterated map object.

    Parameters
    ----------

    map_type : functor
      An iterated map constructor.
    """
    nparam = len(params)
    if nboundaries>0:
        boundaries = np.zeros((nparam, nboundaries))
    bound_rng = range(nboundaries)
    xs = []
    ys = []
    for idx,param in enumerate(params):
        m = map_type(param)
        y = m.trajectory(m.iterate_from(0.5, ntransients), ncycles)
        xs.extend(param*np.ones_like(y))
        ys.extend(y)
        if nboundaries:
            # the boundaries are the iterates of the map's maximum, we assume
            # here that it's located at 0.5
            boundaries[idx] = m.trajectory(0.5, nboundaries+1)[1:]

    # Make final figure
    if fig is None:
        fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(xs, ys, '.', mfc=dotcolor, mec=dotcolor, ms=1, mew=0)
    ax.set_xlim(params[0], params[-1])

    if nboundaries>0:
        bound_lines = ax.plot(params, boundaries)

    def toggle(event):
        if event.key!='t': return
        
        for a in bound_lines:
            v = a.get_visible()
            a.set_visible(not v)
        fig.canvas.draw()
        
    fig.canvas.mpl_connect('key_press_event', toggle)
    return fig


def cobweb(mu, walkers=10, steps=7):
    f = plt.figure()
    ax = f.add_subplot(111)
    interval = np.linspace(0.0, 1.0, 100)
    logmap = Logistic(mu)
    logmap.plot(ax, interval, lw=2)
    for x0 in np.random.rand(walkers):
        logmap.plot_cobweb(ax, x0, steps, lw=2)
    ax.set_title('Ex 2A: Random init. cond. for mu=%1.3f'%mu)
    return f


def invariant_density(mu, x0,cycles=1000000,ret_all=False):
    transients = 1000
    bins = 500
    f = plt.figure()
    ax = f.add_subplot(111)
    logmap = Logistic(mu)
    y0 = logmap.iterate_from(x0, transients)
    y = logmap.trajectory(y0, cycles)
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
        return 1./(np.pi * np.sqrt( x*(1.-x)))

    # Don't start from 0.5, which is a fixed point!
    f = invariant_density(1.0,0.567)
    ax = f.gca()
    # avoid the edges: rho(x) is singular at 0 and 1!
    x0 = np.linspace(0.001, 0.999, 1000)
    l, = ax.plot(x0, rho(x0), 'r-', lw=3, alpha=0.7)
    ax.set_title('Ex 2B: invariant density')
    ax.legend((ax.patches[0], l), ('empirical', 'analytic'), loc='upper center')
    ax.set_xlim(0,1)
    ax.set_ylim(0,10)
    

def ex2CD(mu=0.9,x0=0.64):
    
    fig, logmap, n = invariant_density(mu, x0, ret_all=True)
    ax = fig.gca()
    ax.set_xticks(np.linspace(0, 1, 10))
    ax.grid(True)
    # Now, iterate x=1/2 a few times and plot this 'orbit', which corresponds
    # to peaks in the invariant density.
    x0 = 0.5
    pts = logmap.trajectory(x0,10)
    pts_y = 0.5*np.linspace(1, max(n), len(pts))
    ax.plot(pts,pts_y,'ro-')
    ax.set_title('**Ex 2C/D: Analytics of cusps at mu=%0.2g' % mu)
    

def ex2E():
    # Parameter grid to sample each map on
    params = np.linspace(0.5, 1, 500)
    fig = bifurcation_diagram(Logistic, params, nboundaries=8)
    fig.gca().set_title('Ex 2E: Bifurcation diag. with boundaries (press t)')
    fig = bifurcation_diagram(Logistic, params, dotcolor='blue')
    fig = bifurcation_diagram(Sine, params, dotcolor='red', fig = fig)
    fig.gca().set_title('Ex 2E: Bifurcation diag. logistic/sine maps')
    

if __name__=='__main__':
    ex2A()
    ex2B()
    ex2CD()
    ex2E()
    plt.show()
