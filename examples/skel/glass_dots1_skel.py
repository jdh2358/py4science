"""
Moire patterns from random dot fields

http://en.wikipedia.org/wiki/Moir%C3%A9_pattern

See L. Glass. 'Moire effect from random dots' Nature 223, 578580 (1969).
"""
import cmath  # provides complex math functions
from numpy import cos, sin, pi, matrix
import numpy as npy
import numpy.linalg as linalg
from pylab import figure, show

def myeig(M):
    """
    compute eigen values and eigenvectors analytically
    Solve quadratic:
      lamba^2 - tau*lambda + Delta = 0
    where tau = trace(M) and Delta = Determinant(M)

    Return value is lambda1, lambda2
    """
    XXX
    
# 2000 random x,y points in the interval[-0.5 ... 0.5]
X1 = XXX

name =  'saddle'
#sx, sy, angle = XXX

#name = 'center'
#sx, sy, angle = XXX

name = 'spiral'  #stable focus
sx, sy, angle = XXX

theta = angle * pi/180.  # the rotation in radians


# the scaling matrix
# | sx 0 |
# | 0 sy |
S = XXX

# the rotation matrix
# | cos(theta)  -sin(theta) |
# | sin(theta)  cos(theta)  |
R = XXX

# the transformation is the matrix product of the scaling and rotation
M = XXX

# compute the eigenvalues using numpy linear algebra
print 'numpy eigenvalues', XXX

# compare with the analytic values from myeig
print 'analytic eigenvalues', myeig(M)

# transform X1 by the matrix M
X2 = XXX

# plot the original X1 as green dots and the transformed X2 as red
# dots
XXX
