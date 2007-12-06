import numpy as n
import pylab as p
import scipy.integrate as integrate

def dr(r, f):
    'return delta r'
    XXX
    
def df(r, f):
    'return delta f'
    XXX
def derivs(state, t):
    """
    Map the state variable [rabbits, foxes] to the derivitives
    [deltar, deltaf] at time t
    """
    XXX
    
alpha, delta = 1, .25
beta, gamma = .2, .05

# the initial population of rabbits and foxes
r0 = 20
f0 = 10

t = XXX       # pick a time vector (think about the time scales!)
y0 = [r0, f0] # the initial [rabbits, foxes] state vector
y = XXX       # integrate derives over t starting at y0
r = XXX       # extract the rabbits vector
f = XXX       # extract the foxes vector


# FIGURE 1: rabbits vs time and foxes vs time on the same plot with
# legend and xlabel, ylabel and title

# FIGURE 2: the phase plane

# plot r vs f and label the x and y axes
XXX

# FIGURE 2 continued....

# use meshgrid to make a grid over R and F
# with a coarse 1 year sampling.  evaluate dR and dF over the 2 s
# grids and make a quiver plot.  See pylab.quiver and matplotlib
# examples/quiver_demo.py
XXX

# FIGURE 2 continued...  use contour to compute the null clines over
# dR (the rabbits null cline) and dF (the foxes null cline).  You will
# need to do a finer meshgrid for accurate null clins and pass
# levels=[0] to contour
XXX

p.show()

