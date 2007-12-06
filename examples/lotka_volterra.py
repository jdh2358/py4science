import numpy as n
import pylab as p
import scipy.integrate as integrate

def dr(r, f):
    return alpha*r - beta*r*f    
    
def df(r, f):
    return gamma*r*f - delta*f

def derivs(state, t):
    """
    Map the state variable [rabbits, foxes] to the derivitives
    [deltar, deltaf] at time t
    """
    #print t, state
    r, f = state  # rabbits and foxes
    deltar = dr(r, f)  # change in rabbits
    deltaf = df(r, f) # change in foxes
    return deltar, deltaf

alpha, delta = 1, .25
beta, gamma = .2, .05

# the initial population of rabbits and foxes
r0 = 20
f0 = 10

t = n.arange(0.0, 100, 0.1)

y0 = [r0, f0]  # the initial [rabbits, foxes] state vector
y = integrate.odeint(derivs, y0, t)
r = y[:,0]  # extract the rabbits vector
f = y[:,1]  # extract the foxes vector

p.figure()
p.subplots_adjust(hspace=0.3)
p.subplot(211)
p.plot(t, r, color='blue', label='rabbits', lw=2)
p.plot(t, f, color='green', label='foxes', lw=2)
p.xlabel('time (years)')
p.ylabel('population')
p.title('population trajectories and phase plane')
p.grid()
p.legend()


p.subplot(212, aspect='equal')
p.plot(r, f, 'k', lw=2)
p.xlabel('rabbits')
p.ylabel('foxes')

# make a direction field plot with quiver
rmax = 1.1 * r.max()
fmax = 1.1 * f.max()
R, F = n.meshgrid(n.arange(-1, rmax), n.arange(-1, fmax))
dR = dr(R, F)
dF = df(R, F)
p.quiver(R, F, dR, dF)


R, F = n.meshgrid(n.arange(-1, rmax, .1), n.arange(-1, fmax, .1))
dR = dr(R, F)
dF = df(R, F)

CSR = p.contour(R, F, dR, levels=[0], linewidths=3, colors='blue')
CSF = p.contour(R, F, dF, levels=[0], linewidths=3, colors='green')

p.ylabel('foxes')

p.savefig('lotka_volterra.png', dpi=150)
p.savefig('lotka_volterra.eps')


p.show()

