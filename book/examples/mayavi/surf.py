from mayavi.tools import imv

from scipy import exp,sin,linspace,pi

def f(x,y):
    return 5*exp(-(x**2+y**2))*(sin(x+y))

def g(x,y):
    r2 = x**2+y**2
    return 0.5+3*exp(-r2)*(sin(r2))

npts = 40
x = y = linspace(-pi,pi,npts)

imv.surf(x,y,f)
imv.surf(x,y,g)

mv = imv.surf(x,y,f)
imv.surf(x,y,g,viewer=mv)
