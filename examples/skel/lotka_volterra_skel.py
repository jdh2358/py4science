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
    raise NotImplementedError('insert missing code here')

def df(r, f):
    """
    return the derivative of *f* (the fox population) evaulated as a
    function of *r* and *f*.  The function should work whether *r* and *f*
    are scalars, 1D arrays or 2D arrays.  The return value should have
    the same dimensionality (shape) as the inputs *r* and *f*.
    """
    raise NotImplementedError('insert missing code here')

def derivs(state, t):
    """
    Return the derivatives of r and f, stored in the *state* vector::

       state = [r, f]

    The return data should be [dr, df] which are the derivatives of r
    and f at position state and time *t*
    """

    raise NotImplementedError('insert missing code here')

alpha, delta = 1, .25
beta, gamma = .2, .05

# the initial population of rabbits and foxes
r0 = 20
f0 = 10

t = np.arange(0.0, 100, 0.1)

y0 = [r0, f0]  # the initial [rabbits, foxes] state vector
y = integrate.odeint(derivs, y0, t)
r = y[:,0]  # extract the rabbits vector
f = y[:,1]  # extract the foxes vector

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


plt.figure()
plt.plot(r, f, color='red')
plt.xlabel('rabbits')
plt.ylabel('foxes')
plt.title('phase plane')


# make a direction field plot with quiver
rmax = 1.1 * r.max()
fmax = 1.1 * f.max()
R, F = np.meshgrid(np.arange(-1, rmax), np.arange(-1, fmax))
dR = dr(R, F)
dF = df(R, F)
plt.quiver(R, F, dR, dF)


R, F = np.meshgrid(np.arange(-1, rmax, .1), np.arange(-1, fmax, .1))
dR = dr(R, F)
dF = df(R, F)

plt.contour(R, F, dR, levels=[0], linewidths=3, colors='blue')
plt.contour(R, F, dF, levels=[0], linewidths=3, colors='green')
plt.ylabel('foxes')
plt.title('trajectory, direction field and null clines')

plt.savefig('lotka_volterra_pplane.png', dpi=150)
plt.savefig('lotka_volterra_pplane.eps')


plt.show()

