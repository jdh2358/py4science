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
    raise NotImplementedError('Original solution has 1 line')

def df(r, f):
    """
    return the derivative of *f* (the fox population) evaulated as a
    function of *r* and *f*.  The function should work whether *r* and *f*
    are scalars, 1D arrays or 2D arrays.  The return value should have
    the same dimensionality (shape) as the inputs *r* and *f*.
    """
    raise NotImplementedError('Original solution has 1 line')

def derivs(state, t):
    """
    Return the derivatives of r and f, stored in the *state* vector::

       state = [r, f]

    The return data should be [dr, df] which are the derivatives of r
    and f at position state and time *t*
    """
    raise NotImplementedError('Original solution has 4 lines')

# the parameters for rabbit and fox growth and interactions
alpha, delta = 1, .25
beta, gamma = .2, .05

# the initial population of rabbits and foxes
r0 = 20
f0 = 10

# create a time array from 0..100 sampled at 0.1 second steps
raise NotImplementedError('Original solution has 1 line')


y0 = [r0, f0]  # the initial [rabbits, foxes] state vector

# integrate your ODE using scipy.integrate.  Read the help to see what
# is available
# HINT: see scipy.integrate.odeint
raise NotImplementedError('Original solution has 1 line')

# the return value from the integration is a Nx2 array.  Extract it
# into two 1D arrays caled r and f using numpy slice indexing
raise NotImplementedError('Original solution has 2 lines')

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
raise NotImplementedError('Original solution has 5 lines')


# Create 2D arrays for R and F to represent the entire phase plane --
# the point (R[i,j], F[i,j]) is a single (rabbit, fox) combinations.
# pass these arrays to the functions dr and df above to get 2D arrays
# of dR and dF evaluated at every point in the phase plance.
raise NotImplementedError('Original solution has 6 lines')


# Now find the nul-clines, for dR and dF respectively.  These are the
# points where dR=0 and dF=0 in the (R, F) phase plane.  You can use
# matplotlib's countour routine to find the zero level.  See the
# levels keyword to contour.  You will need a fine mesh of R and F,
# reevaluate dr and df on the finer grid, and use contour to find the
# level curves
raise NotImplementedError('Original solution has 7 lines')

plt.savefig('lotka_volterra_pplane.png', dpi=150)
plt.savefig('lotka_volterra_pplane.eps')
plt.show()

