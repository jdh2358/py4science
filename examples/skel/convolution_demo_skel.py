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

import numpy as npy
import matplotlib.mlab as mlab
from pylab import figure, show

# build the time, input, output and response arrays
dt = 0.01
t = XXX        # the time vector from 0..20
Nt = len(t)

def impulse_response(t):
    'double exponential response function'
    return XXX


x = XXX   # gaussian white noise

# evaluate the impulse response function, and numerically convolve it
# with the input x
r = XXX # evaluate the impulse function
y = XXX # convolution of x with r
y = XXX # extract just the length Nt part

# compute y by applying F^-1[F(x) * F(r)].  The fft assumes the signal
# is periodic, so to avoid edge artificats, pad the fft with zeros up
# to the length of r + x do avoid circular convolution artifacts
R = XXX  # the zero padded FFT of r
X = XXX  # the zero padded FFT of x
Y = XXX  # the product of R and X 

# now inverse fft and extract the real part, just the part up to
# len(x)
yi = XXX

# plot x vs t, y and yi vs t, and r vs t in three subplots
XXX
show()
