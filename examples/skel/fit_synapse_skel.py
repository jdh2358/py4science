"""
Modeling synaptic responses to a random train of inputs -- see, eg,
http://www.jneurosci.org/cgi/content/full/21/15/5781
"""

import os
import numpy

import scipy.optimize 
from matplotlib.mlab import load
import matplotlib.cbook as cbook
from pylab import figure, show

XXX = None

class Model:
    """
    Helper class for parametric modeling of spike train data
    """

    def __init__(self, t, s, model):
        """
        Initialize with the times of the impulses as array t, the
        amplitude of the spikes as array s, and a model function which
        has signature

          m = model(t, pars)

        where pars is a parameter vector that the model will be
        evaluated over and m is the model's prediction on times t for
        those parameter.  m is an array that has the same length as t
        and s.
        """
        self.t = t
        self.s = s
        self.model = model
        
    def rms(self, pars):
        """
        call model with signature m = model(t, pars) and return the
        root-mean-square RMS error between actual spikes s and model m
        """
        pass

    def fit(self, guess):
        """
        Use scipy.optimize to get the best fit of the model to the
        data
        """
        pass

    def plot_data(self, ax, pars=None):
        """
        plot the data in axes ax.  If pars is not None, overlay the
        model estimated at those parameters
        """
        pass
        
    def plot_isi(self, ax):
        """
        make a plot of the interspike interval histogram (the
        interspike interval is the difference between adjacent spike
        times.  ax is an axes instance to make the plot in
        """
        pass


def nexponential(t, pars):
    """
    a N-factor linear exponential model
    
    pars is an even length sequence of a, alpha pairs where a is the
    amplitude and alpha is the rate constant of an exponential factor
    if n is the number of factors, the impulse response function is

          r(t) = a1 exp(-alpha1 t) + a2 exp(-alpha2 t) + ... an exp(-alphan t)

    and the spike amplitude is given by

      m(t) = 1 + s(t) * r(t)  where * denotes convolution.

    Since the inputs s(t) = sum_k delta(t-tk) where delta is the Dirac
    delta function, we can write the output

      m_k = 1 + sum_k r(t-tk) where tk is the time of the k-th spike <= t

    pars is an (a1, alpha1, a2, alpha2, ..., an, alphan) tuple

    return value is a length(pars) vector of best fit params
    """
    pass
        


# data files are located in 'data' and have filenames
# synapse_times.dat and synapse_data.dat, each of which contain a
# single column of ASCII floating point numbers.  load each into an
# array t and s, where t is the array of times and s an equal length
# array of synapse amplitudes
t = XXX
s = XXX

# for the nexponential model, provide ordered pairs of a, alpha for
# the amplitude and rate constant of an exponential factor.  Eg, if
# pars is length(6), this is a 3 factor model with parameters (a1,
# alpha1, a2, alpha2, a3, alpha3).  If a is negative the factor is
# depression, and if a is positive to factor is excitatory
guess = (-0.05, 0.3)
#guess = (-0.05, 0.3, -0.1, 1.0)
#guess = (-0.05, 0.3, -0.1, 1.0, 0.3, 25.)

# create the model and do the best fit
model = Model(t, s, nexponential)
bestpars = model.fit(guess)

# plot the interspike-interval histogram, the actual data, and the best model fit
fig = figure()
ax1 = fig.add_subplot(211)
model.plot_isi(ax1)
ax2 = fig.add_subplot(212)
model.plot_data(ax2, bestpars)


show()
