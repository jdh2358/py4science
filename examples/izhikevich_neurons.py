import numpy as np
import matplotlib.pyplot as plt
from matplotlib.cbook import iterable

def rk4step(derivs, y0, t, dt):

    dt2 = dt/2.0

    k1 = np.asarray(derivs(y0, t))
    k2 = np.asarray(derivs(y0 + dt2*k1, t+dt2))
    k3 = np.asarray(derivs(y0 + dt2*k2, t+dt2))
    k4 = np.asarray(derivs(y0 + dt*k3, t+dt))
    return y0 + dt/6.0*(k1 + 2*k2 + 2*k3 + k4)

class Izhikevich:
    def __init__(self, a, b, c, d):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.I = 0
        self.indI = 0

    def __call__(self, state, t):
        v, u = state
        if hasattr(self.I, 'shape'):
            if len(self.I.shape)==2:
                I = self.I[:,self.indI]
            else:
                I = self.I[self.indI]
        else:
            I = self.I


        dv = 0.04*v**2 + 5*v + 140 -u + I
        du = self.a*(self.b*v-u)
        return dv, du

    def reset_if_action_potential(self, state):
        v, u = state
        spiked = v>=30.0

        if iterable(spiked):
            ind = np.nonzero(spiked)
            v = np.where(spiked, self.c, v)
            u = np.where(spiked, u + self.d, u)
        else:
            ind = None
            if spiked:
                v = self.c
                u += self.d
        self.indI += 1
        return ind, v, u


def integrate_single(times, abcd, V0, I):

    model = Izhikevich(*abcd)


    state = np.array( [V0,0], float)
    if not iterable(I):
        I = I*np.ones(times.shape, float)


    model.I = I
    volts = np.zeros(times.shape, float)
    volts[0] = state[0]
    for i in range(1, len(times)):

        dt = times[i] - times[i-1]
        state = rk4step(model, state, times[i], dt)
        ind, v, u = model.reset_if_action_potential(state)
        state[0] = v
        state[1] = u
        volts[i] = state[0]

    return volts

regular_spiking = 0.02, 0.2, -65, 8
chattering = 0.02, 0.2, -50, 2
fast_spiking = 0.1, 0.2, -65, 2
intrinsically_bursting = 0.02, 0.2, -55, 4
thalamocortical = 0.02, 0.25, -65, 0.05

lines = []
texts = []
labels = []

times = np.arange(0.0, 500.0, 0.1)
V0 = -65
I = np.where(times>=100, 10, 0)
offset = 150
#ax = plt.subplot(111)
ax = plt.axes([0.125, .11, 0.725, 0.79], axisbg='w')

num = 0
v = integrate_single(times, regular_spiking, V0, I)
l = ax.plot(times/1000.0, v+num*offset, 'k')
ax.text(0.51, v[0]+num*offset+20, 'RS', fontsize=15)
lines.extend(l)
num += 1

v = integrate_single(times, chattering, V0, I)
l = ax.plot(times/1000.0, v+num*offset, 'k')
ax.text(0.51, v[0]+num*offset+20, 'CH', fontsize=15)
lines.extend(l)
num += 1

v = integrate_single(times, fast_spiking, V0, I)
l = ax.plot(times/1000.0, v+num*offset, 'k')
ax.text(0.51, v[0]+num*offset+20, 'FS', fontsize=15)
lines.extend(l)

num += 1

v = integrate_single(times, intrinsically_bursting, V0, I)
l = ax.plot(times/1000.0, v+num*offset, 'k')
ax.text(0.51, v[0]+num*offset+20, 'IB', fontsize=15)
lines.extend(l)
num += 1


ax.axis([0, 0.5, -100, 900])
ax.set_yticklabels([])
ax.set_xlabel('time (s)')
ax.grid(False)


ax = plt.axes([0.25, 0.7, 0.175, 0.175], axisbg='w')
ax.set_xticks([0.02, 0.1])
ax.set_yticks([0.2, 0.25])
ax.plot([0.02, 0.1], [0.2, 0.2], 'o',
     markerfacecolor='k', markeredgecolor='k', markersize=4)
texts.append( ax.text(0.01, 0.18, 'RS, IB, CH') )
texts.append( ax.text(0.1, 0.18, 'FS') )

ax.grid(False)

ax.axis([0, 0.15, 0.15, 0.3])
labels.append(ax.set_xlabel('parameter a'))
labels.append(ax.set_ylabel('parameter b'))

ax = plt.axes([0.6, 0.7, 0.175, 0.175], axisbg='w')
ax.set_xticks([-65, -55, -50])
ax.set_yticks([2, 4, 8])
ax.plot([-65, -50, -55, -65], [2, 2, 4, 8], 'o',
     markerfacecolor='k', markeredgecolor='k', markersize=4)

texts.append( ax.text(-64, 2.5, 'FS') )
texts.append( ax.text(-49, 2.5, 'CH') )
texts.append( ax.text(-54, 4.5, 'IB') )
texts.append( ax.text(-64, 8.5, 'RS') )

for text in texts:
    text.set_fontsize(10)

labels.append(ax.set_xlabel('parameter c'))
labels.append(ax.set_ylabel('parameter d'))

ax.axis([-70, -40, 0.05, 10])
ax.grid(False)
#plt.savefig('figures/four_neurons.eps')

plt.show()
