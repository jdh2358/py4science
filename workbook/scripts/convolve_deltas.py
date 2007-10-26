import numpy as npy
from pylab import figure, show

dt = 0.025
t = npy.arange(0.0, 0.5, dt)        
Nt = len(t)


s = npy.exp(-2*t)*npy.cos(2*3*npy.pi*t)+1.0
fig = figure()
ax = fig.add_subplot(111)
ax.plot(t, s, color='blue', lw=2)
ax.bar(t-dt/8., s, facecolor='blue', width=dt/4.)
ax.axhline(0, color='black', lw=2)
ax.set_xlim(xmin=0)
fig.savefig('convolve_deltas.png', dpi=150)
fig.savefig('convolve_deltas.eps')
show()
