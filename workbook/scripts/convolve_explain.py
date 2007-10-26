import numpy as npy
from pylab import figure, show

dt = 0.01
t = npy.arange(0.0, 10.0, dt)        
Nt = len(t)

def impulse_response(t):
    'double exponential response function'
    return (npy.exp(-t) - npy.exp(-5*t))

i1 = npy.zeros(len(t))
i2 = npy.zeros(len(t))
i3 = npy.zeros(len(t))
r = impulse_response(t)

ind1, ind2, ind3  = 100, 300, 900
i1[ind1] = 1
i2[ind2] = 1.7
i3[ind3] = 0.6

y1 = npy.convolve(i1, r, mode='full')[:Nt]
y2 = npy.convolve(i2, r, mode='full')[:Nt]
y3 = npy.convolve(i3, r, mode='full')[:Nt]

fig = figure()
ax1 = ax = fig.add_subplot(311)
ax.plot(t, r, 'k', lw=2)
ax.set_ylabel('impulse response')

ax = fig.add_subplot(312, sharex=ax1)
ax.bar(t[ind1], i1[ind1], facecolor='blue', lw=2, edgecolor='blue', width=3*dt)
ax.bar(t[ind2], i2[ind2], facecolor='green', lw=2, edgecolor='green', width=3*dt)
ax.bar(t[ind3], i3[ind3], facecolor='red', lw=2, edgecolor='red', width=3*dt)
ax.plot(t, y1, color='blue', lw=1, label='input 1')
ax.plot(t, y2, color='green', lw=1, label='input 2')
ax.plot(t, y3, color='red', lw=1, label='input d')
ax.set_ylabel('3 inputs')


ax = fig.add_subplot(313, sharex=ax1)
ax.plot(t, y1+y2+y3, color='black', lw=2, label='sum')
ax.set_ylabel('output')
#ax.legend(loc='best')

fig.savefig('../fig/convolve_explain.png', dpi=150)
fig.savefig('../fig/convolve_explain.eps')
show()
