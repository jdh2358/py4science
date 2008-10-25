"""
In signal processing, the output of a linear system to an arbitrary
input is given by the convolution of the impule response function (the
system response to a Dirac-delta impulse) and the input signal.

Mathematically:

  y(t) = \int_0^\t x(\tau)r(t-\tau)d\tau


where x(t) is the input signal at time t, y(t) is the output, and r(t)
is the impulse response function.

In this exercise, we will compute investigate the convolution of a
white noise process with a double exponential impulse response
function, and compute the results

  * using numpy.convolve

  * in Fourier space using the property that a convolution in the
    temporal domain is a multiplication in the fourier domain
"""

import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

# build the time, input, output and response arrays
dt = 0.01
t = np.arange(0.0, 20.0, dt)        # the time vector from 0..20
Nt = len(t)

def impulse_response(t):
    'double exponential response function'
    return (np.exp(-t) - np.exp(-5*t))*dt


x = np.random.randn(Nt)   # gaussian white noise

# evaluate the impulse response function, and numerically convolve it
# with the input x
r = impulse_response(t)               # evaluate the impulse function
y = np.convolve(x, r, mode='full')   # convultion of x with r
y = y[:Nt]

# compute y by applying F^-1[F(x) * F(r)].  The fft assumes the signal
# is periodic, so to avoid edge artificats, pad the fft with zeros up
# to the length of r + x do avoid circular convolution artifacts
R = np.fft.fft(r, len(r)+len(x)-1)
X = np.fft.fft(x, len(r)+len(x)-1)
Y = R*X

# now inverse fft and extract just the part up to len(x)
yi = np.fft.ifft(Y)[:len(x)].real

# plot t vs x, t vs y and yi, and t vs r in three subplots
fig = plt.figure()
ax1 = fig.add_subplot(311)
ax1.plot(t, x)
ax1.set_ylabel('input x')

ax2 = fig.add_subplot(312)
ax2.plot(t, y, label='convolve')
ax2.set_ylabel('output y')

ax3 = fig.add_subplot(313)
ax3.plot(t, r)
ax3.set_ylabel('input response')
ax3.set_xlabel('time (s)')

ax2.plot(t, yi, label='fft')
ax2.legend(loc='best')

fig.savefig('convolution_demo.png', dpi=150)
fig.savefig('convolution_demo.eps')
plt.show()
