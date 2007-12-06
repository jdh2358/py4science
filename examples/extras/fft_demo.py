#!/usr/bin/env python
"""Simple demo of basic 1-d FFT."""

import numpy as N
import pylab as P

P.rc('lines', linewidth=2)
dx = 0.001
x = N.linspace(0.0, 1.0, 1000)
s = N.sin(2*4*N.pi*x*x)


F = N.fft(s)
nfreq = len(s)/2+1
freqs = N.linspace(0, 1/(2*dx), nfreq)  # the freq vector
F = F[:nfreq]  # extract positive frequencies

magnitude = N.absolute(F)/len(s)
phase = N.arctan2(F.imag,F.real)

# make the BODE plot
P.figure()
P.title('Bode plot')
P.subplot(211)
P.semilogy(freqs, magnitude)
P.xlim(0,20)
P.grid()
P.ylabel('Amplitude')
P.subplot(212)
P.plot(freqs, phase)
P.xlim(0,20)
P.grid()
P.ylabel('Phase')

# now do the reconstuction
def component(i):
    # scale by 2 because we are exluding negative freqs
    if i==0: scale = 1
    else: scale =2
    return scale*magnitude[i]*N.cos(2*N.pi*freqs[i]*x + phase[i])

tot = component(0)
for i in range(1,10): tot += component(i)

P.figure()
P.plot(x, tot, 'r--', x, s, 'b-', lw=2)
P.show()
