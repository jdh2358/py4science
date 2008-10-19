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
p.plot(t, r, label='rabbits')
p.plot(t, f, label='foxes')
p.xlabel('time (years)')
p.ylabel('population')
p.title('population trajectories')
p.grid()
p.legend()
p.savefig('lotka_volterra.png', dpi=150)
p.savefig('lotka_volterra.eps')


p.figure()
p.plot(r, f, color='red')
p.xlabel('rabbits')
p.ylabel('foxes')
p.title('phase plane')


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

p.contour(R, F, dR, levels=[0], linewidths=3, colors='blue')
p.contour(R, F, dF, levels=[0], linewidths=3, colors='green')
p.ylabel('foxes')
p.title('trajectory, direction field and null clines')

p.savefig('lotka_volterra_pplane.png', dpi=150)
p.savefig('lotka_volterra_pplane.eps')


p.show()

