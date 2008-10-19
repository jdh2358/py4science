import numpy as np
import scipy.signal as signal
from matplotlib.pyplot import figure, show

dt = 0.01
t = np.arange(0, 2, dt)
s = np.sin(2*np.pi*t)

# sine corrupted wih gaussian white noise
sn = s + 0.1*np.random.randn(len(s))  # noisy sine

# the nyquist frequency 1/(2dt) is the maximum frequency in a sampled
# signal
Nyq = 0.5/dt

#the corner frequency represents a boundary in the system response at
#which energy entering the system begins to be attenuate, and the stop
#frequency is the frequency at which the signal is (practically)
#completely attenuated
cornerfreq = 2.  # the corner frequency
stopfreq = 5.    # the stop frequency

# the scipy.signal routines accept corner an stop frequencies as a
# *fraction* of the nyquist
ws = cornerfreq/Nyq
wp = stopfreq/Nyq


# call scipy.buttord to compute the order and natural frequency of the
# butterorth filter.  See the help for signal.buttord.  You will pass
# in ws and wp, as well as the attenuation in the pass and stop bands
N, wn = signal.buttord(wp, ws, 3, 16)

# scipy.butter will take the output from buttord and return the
# lfilter coeefs for that filter
b, a = signal.butter(N, wn)

# Now lfilter will filter the noisy sine with the filter parameters
# from butter
sf = signal.lfilter(b, a, sn)

# plot the original, noisy and filtered sine, all on the same axes in
# pylab, and make a legend
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
