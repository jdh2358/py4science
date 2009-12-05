import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as integrate

def dr(r, f):
    """
    return the derivative of *r* (the rabbit population) evaulated as a
    function of *r* and *f*.  The function should work whether *r* and *f*
    are scalars, 1D arrays or 2D arrays.  The return value should have
    the same dimensionality (shape) as the inputs *r* and *f*.
    """
    return alpha*r - beta*r*f    #@

def df(r, f):
    """
    return the derivative of *f* (the fox population) evaulated as a
    function of *r* and *f*.  The function should work whether *r* and *f*
    are scalars, 1D arrays or 2D arrays.  The return value should have
    the same dimensionality (shape) as the inputs *r* and *f*.
    """
    return gamma*r*f - delta*f  #@

def derivs(state, t):
    """
    Return the derivatives of R and F, stored in the *state* vector::

       state = [R, F]

    The return data should be [dR, dF] which are the derivatives of R
    and F at position state and time *t*
    """
    R, F = state          # and foxes    #@
    deltar = dr(r, f)     # in rabbits   #@
    deltaf = df(r, f)     # in foxes     #@
    return deltar, deltaf                #@

# the parameters for rabbit and fox growth and interactions
alpha, delta = 1, .25
beta, gamma = .2, .05

# the initial population of rabbits and foxes
r0 = 20
f0 = 10

# create a time array from 0..100 sampled at 0.1 second steps
t = np.arange(0.0, 100, 0.1)    #@


y0 = [r0, f0]  # the initial [rabbits, foxes] state vector

# integrate your ODE using scipy.integrate.  Read the help to see what
# is available
#@ HINT: see scipy.integrate.odeint
y = integrate.odeint(derivs, y0, t)   #@

# the return value from the integration is a Nx2 array.  Extract it
# into two 1D arrays caled r and f using numpy slice indexing
r = y[:,0]  # extract the rabbits vector   #@
f = y[:,1]  # extract the foxes vector     #@

# time series plot: plot the population of rabbits and foxes as a
# funciton of time
plt.figure()
plt.plot(t, r, label='rabbits')
plt.plot(t, f, label='foxes')
plt.xlabel('time (years)')
plt.ylabel('population')
plt.title('population trajectories')
plt.grid()
plt.legend()
plt.savefig('lotka_volterra.png', dpi=150)
plt.savefig('lotka_volterra.eps')

# phase-plane plot: plot the population of foxes versus rabbits
# make sure you include and xlabel, ylabel and title
plt.figure()                #@
plt.plot(r, f, color='red') #@
plt.xlabel('rabbits')       #@
plt.ylabel('foxes')         #@
plt.title('phase plane')    #@


# Create 2D arrays for R and F to represent the entire phase plane --
# the point (R[i,j], F[i,j]) is a single (rabbit, fox) combinations.
# pass these arrays to the functions dr and df above to get 2D arrays
# of dR and dF evaluated at every point in the phase plance.
rmax = 1.1 * r.max()                                         #@
fmax = 1.1 * f.max()                                         #@
R, F = np.meshgrid(np.arange(-1, rmax), np.arange(-1, fmax)) #@
dR = dr(R, F)                                                #@
dF = df(R, F)                                                #@
plt.quiver(R, F, dR, dF)                                     #@


# Now find the nul-clines, for dR and dF respectively.  These are the
# points where dR=0 and dF=0 in the (R, F) phase plane.  You can use
# matplotlib's countour routine to find the zero level.  See the
# levels keyword to contour.  You will need a fine mesh of R and F,
# reevaluate dr and df on the finer grid, and use contour to find the
# level curves
R, F = np.meshgrid(np.arange(-1, rmax, 0.1), np.arange(-1, fmax, 0.1)) #@
dR = dr(R, F)                                                          #@
dF = df(R, F)                                                          #@
plt.contour(R, F, dR, levels=[0], linewidths=3, colors='blue')         #@
plt.contour(R, F, dF, levels=[0], linewidths=3, colors='green')        #@
plt.ylabel('foxes')                                                    #@
plt.title('trajectory, direction field and null clines')               #@

plt.savefig('lotka_volterra_pplane.png', dpi=150)
plt.savefig('lotka_volterra_pplane.eps')
plt.show()

