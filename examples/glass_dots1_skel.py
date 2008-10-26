"""
Moire patterns from random dot fields

http://en.wikipedia.org/wiki/Moir%C3%A9_pattern

See L. Glass. 'Moire effect from random dots' Nature 223, 578580 (1969).
"""
import cmath
import numpy as np
import numpy.linalg as linalg
import matplotlib.pyplot as plt

# search for TODO to find the places you need to fix
TODO = None

def myeig(M):
    """
    compute eigen values and eigenvectors analytically

    Solve quadratic:

      lamba^2 - tau*lambda +/- Delta = 0

    where tau = trace(M) and Delta = Determinant(M)

    if M = | a b |
           | c d |

    the trace is a+d and the determinant is a*d-b*c

    Return value is lambda1, lambda2

    Return value is lambda1, lambda2
    """
    # TODO : compute the real values here.  0, 1 is just a place holder
    return 0, 1

# Generate and shape (2000,2) random x,y points in the
# interval [-0.5 ... 0.5]
X1 = TODO

# these are the scaling factor sx, the scaling factor sy, and the
# rotation angle 0
name =  'saddle'
sx, sy, angle = 1.05, 0.95, 0.

# OPTIONAL: try and find other sx, sy, theta for other kinds of nodes:
# stable node, unstable node, center, spiral, saddle

# convert theta to radians: theta = angle * pi/180
theta = TODO

# Create a 2D scaling array
# S = | sx 0  |
#     | 0  sy |
S = TODO

# create a 2D rotation array
# R = | cos(theta)   -sin(theta) |
#     | sin(theta)    cos(theta) |
R = TODO

# do a matrix multiply M = S x R where x is *matrix* multiplication
M = TODO

# compute the eigenvalues using numpy linear algebra
vals, vecs = linalg.eig(M)
print 'numpy eigenvalues', vals

# compare with the analytic values from myeig
avals = myeig(M)
print 'analytic eigenvalues', avals

# transform X1 by the matrix
# X2 = M x X1  where x is *matrix* multiplication
X2 = np.dot(M, X1)

# plot the original x,y as green dots and the transformed x, y as red
# dots
TODO
