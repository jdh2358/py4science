import numpy
from regress import regress

N = 1000
weight = 50+10*numpy.random.randn(N) # weight kgs
height = 150+20*numpy.random.randn(N) # height cm

alpha = 1.5
beta = 3.4
c = 60.

y = alpha * weight + beta * height + 5*numpy.random.randn(N) + c
X = numpy.ones((N,3), numpy.float_)
X[:,0] = weight
X[:,1] = height

#estimate the best fit params using B = (Xt X)^-1 Xt y; see numpy.matrix and
#numpy.linalg
XXX
