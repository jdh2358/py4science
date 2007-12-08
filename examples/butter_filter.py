import numpy as n
import scipy.signal as signal
from pylab import figure, show

dt = 0.01
t = n.arange(0, 2, dt)
s = n.sin(2*n.pi*t)

# sine corrupted wih gaussian white noise
sn = s + 0.1*n.random.randn(len(s))  # noisy sine

# the nyquist frequency 1/(2dt)
Nyq = 0.5/dt

cornerfreq = 2.  # the corner frequency
stopfreq = 5.    # the stop frequency

# the corner and stop freqs as fractions of the nyquist
ws = cornerfreq/Nyq
wp = stopfreq/Nyq


# the order and butterworth natural frequency for use with butter
N, wn = signal.buttord(wp, ws, 3, 16)

# return the butterworth filter coeffs for the given order and frequency
b, a = signal.butter(N, wn)

# filter the data
sf = signal.lfilter(b, a, sn)

fig = figure()
ax = fig.add_subplot(111)
ax.plot(t, s, label='original signal')
ax.plot(t, sn, label='noisy signal')
ax.plot(t, sf, label='filtered signal')
ax.legend()
ax.set_title('low pass butterworth filter of sine')
ax.set_xlabel('time (s)')
ax.grid()
show()
