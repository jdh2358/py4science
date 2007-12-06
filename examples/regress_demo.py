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

#pars, err, (Rsquared, F, p) = regress(X, y)
#alphap, betap, cp = pars


print 'alpha=%1.2f, alphap=%1.2f'%(alpha, alphap)
print 'beta=%1.2f, betap=%1.2f'%(beta, betap)
print 'c=%1.2f, cp=%1.2f'%(c, cp)
print 'R=%1.3f'%(100*Rsquared)
print 'p=%g'%p


