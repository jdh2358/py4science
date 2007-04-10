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
 

class Model(object):
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
        m = self.model(self.t, pars)
        err = numpy.sqrt(numpy.mean((self.s-m)**2.))
        #print pars, err
        return err

    def fit(self, guess, bounds=None):
        """
        Use scipy.optimize to get the best fit of the model to the
        data.  See scipy.optimize.fmin_l_bfgs_b
        """
        bestpars, err, infod = scipy.optimize.fmin_l_bfgs_b(
            self.rms, guess, approx_grad=True, bounds=bounds)
        #print bestpars, err, infod
        return bestpars

    def plot_data(self, ax, pars=None):
        """
        plot the data in axes ax.  If pars is not None, overlay the
        model estimated at those parameters
        """
        ax.vlines(self.t, 0, self.s)
        if pars is not None:
            m = self.model(self.t, pars)
            ax.plot(self.t, m, 'o')
        return

    def plot_isi(self, ax):
        """
        make a plot of the interspike interval histogram (the
        interspike interval is the difference between adjacent spike
        times.  ax is an axes instance to make the plot in
        """
        return ax.hist(numpy.diff(self.t), bins=100)


def one_exponential(t, (a, alpha)):
    """
    a one factor exponential model.  t is a vector of times of the
    delta impulses.  The underlying factor is given by the convolution
    of the response function $a exp(-alpha t)$ with the delta inputs,
    and by the sift theorem we reduce the convolution to

      factor[0] = a
      factor[k] = factor[k-1] * exp(-alpha t) + a 

    and the predicted amplitude

      m[k] = 1 + factor[k]
    """
    m = a*numpy.ones((len(t),), dtype=numpy.float_)

    for k, tk in enumerate(t):
        if k==0:
            m[k] = a
        else:
            m[k] = m[k-1]*numpy.exp(-alpha*(t[k]-t[k-1])) + a
    return m + 1.


# data files are located in 'data' and have filenames
# synapse_times.dat and synapse_data.dat, each of which contain a
# single column of ASCII floating point numbers.  load each into an
# array t and s, where t is the array of times and s an equal length
# array of synapse amplitudes
t = load(os.path.join('data', 'synapse_times.dat'))
s = load(os.path.join('data', 'synapse_data.dat'))

guess = (-0.05, 0.3)


# create the model and do the best fit
model = Model(t, s, one_exponential)
bounds = [(None, 0.), (0., None)]
bestpars = model.fit(guess, bounds=bounds)


# plot the interspike-interval histogram, the actual data, and the best model fit
fig = figure()
ax1 = fig.add_subplot(311)
model.plot_isi(ax1)
ax2 = fig.add_subplot(312)
model.plot_data(ax2, bestpars)





### OPTIONAL BELOW THIS POINT

# for the nexponential model, provide ordered pairs of a, alpha for
# the amplitude and rate constant of an exponential factor.  Eg, if
# pars is length(6), this is a 3 factor model with parameters (a1,
# alpha1, a2, alpha2, a3, alpha3).  If a is negative the factor is
# depression, and if a is positive to factor is excitatory

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

    """
    N,remainder = divmod(len(pars),2)
    assert(remainder==0)
    m = numpy.ones((len(t), ), dtype=numpy.float_)  # the model amplitudes
    factors = numpy.zeros((N,), dtype=numpy.float_) # the N exponential factors
    exp = numpy.exp       # local attribute lookup faster
    as = pars[::2]        # the N amplitudes
    alphas = pars[1::2]   # the N rate constants
    tlast = t[0]
    for k, tk in enumerate(t):
        factors = factors*exp(-alphas*(tk-tlast)) + as
        m[k] += factors.sum()
        tlast = tk
     
    return m
    
def autobounds(pars):
    """
    if pars is an nexponential parameter vector, return bounds
    assuming the sign of the amplitude guess and positive rate
    contants.  return value is a len(pars) list of (pmin, pmax) bounds
    """
    pos = 0., None
    neg = None, 0.
    bounds = []
    for a, alpha in cbook.pieces(pars):
        if a<0: abounds = neg
        else: abounds =   pos    
        bounds.append(abounds)           # amplitude bounds
        bounds.append(pos)               # alpha bounds strictly pos
    return bounds

guess = (-0.05, 0.3, -0.1, 1.0) 
#guess = (-0.05, 0.3, -0.1, 1.0, 0.3, 25.)

# an nexponential model with auto-bounds
model = Model(t, s, nexponential)

bestpars = model.fit(guess, bounds=autobounds(guess))
ax3 = fig.add_subplot(313)
model.plot_data(ax3, bestpars)


show()
