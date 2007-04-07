import scipy as S
import pylab as P

# poly1d objects are constructed from coefficients, highest-order first.
coefs = [  1. ,  -3.5,  -0.5,  11. , -17. ,   6. ]

pol = S.poly1d(coefs)
roots = pol.r

print 'Polynomial p(x):\n',pol,'\n'
print 'p(x) built with coefs:',coefs
print 'Roots of p(x):',roots

# Plot p(x)
x = P.frange(-4,4,npts=400)
y = pol(x)
P.figure()
P.axhline(0,color='g')
P.axvline(0,color='g')
P.plot(x,y,'b-')

# Show roots
P.scatter(roots.real,roots.imag,s=80,c='r')

# Set limits and grid to make the plot clear
P.ylim(-40,40)
P.grid()

# Display on screen
P.show()


