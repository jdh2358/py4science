import numpy as n
import scipy.signal as signal
from pylab import figure, show

XXX = 0.  # just so he XXX blanks will not crash
dt = 0.01
t = n.arange(0, 2, dt)
s = XXX   # a 1 Hz sine wave over t

# sine corrupted wih gaussian white noise the sine wave s corrupted
# with gaussian white noise with sigma=0.1.  See numpy.random.randn

sn = XXX
# the nyquist frequency 1/(2dt) is the maximum frequency in a sampled
# signal
Nyq = XXX

#the corner frequency represents a boundary in the system response at
#which energy entering the system begins to be attenuate, and the stop
#frequency is the frequency at which the signal is (practically)
#completely attenuated
cornerfreq = 2.  # the corner frequency
stopfreq = 5.    # the stop frequency

# the scipy.signal routines accept corner an stop frequencies as a
# *fraction* of the nyquist
ws = XXX
wp = XXX


# call scipy.buttord to compute the order and natural frequency of the
# butterorth filter.  See the help for signal.buttord.  You will pass
# in ws and wp, as well as the attenuation in the pass and stop bands
N, wn = XXX, XXX  # the output of signal.buttord

# scipy.butter will take the output from buttord and return the
# lfilter coeefs for that filter.  See help signal.butter
b, a = XXX, XXX # the output of signal.butter

# Now lfilter will filter the noisy sine with the filter parameters
# from butter.  See help signal.lfilter
sf = XXX  # the filtered signal returned from lfi,ter

# plot the original, noisy and filtered sine, all on the same axes in
# pylab, and make a legend
XXX
