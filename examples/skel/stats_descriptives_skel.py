import scipy.stats as stats
from matplotlib.mlab import detrend_linear, load

import numpy
import pylab

XXX = None

class Descriptives:
    """
    a helper class for basic descriptive statistics and time series plots
    """
    def __init__(self, samples):
        self.samples = numpy.asarray(samples)
        self.N = XXX        # the number of samples
        self.median = XXX   # sample median 
        self.min = XXX      # sample min
        self.max = XXX      # sample max
        self.mean = XXX     # sample mean
        self.std = XXX      # sample standard deviation
        self.var = XXX      # sample variance
        self.skew = XXX     # the sample skewness
        self.kurtosis = XXX # the sample kurtosis 
        self.range = XXX    # the sample range max-min

    def __repr__(self):
        """
        Create a string representation of self; pretty print all the
        attributes:

         N, median, min, max, mean, std, var, skew, kurtosis, range,
        """
        
        descriptives = (
            'N        = %d'        % self.N,
            XXX # the rest here
            )
        return '\n'.join(descriptives)

    def plots(self, figfunc, maxlags=20, Fs=1, detrend=detrend_linear, fmt='bo'):
        """
        plots the time series, histogram, autocorrelation and spectrogram

        figfunc is a figure generating function, eg pylab.figure
        
        return an object which stores plot axes and their return
        values from the plots.  Attributes of the return object are
        'plot', 'hist', 'acorr', 'psd', 'specgram' and these are the
        return values from the corresponding plots.  Additionally, the
        axes instances are attached as c.ax1...c.ax5 and the figure is
        c.fig

        keyword args:
        
          Fs      : the sampling frequency of the data

          maxlags : max number of lags for the autocorr

          detrend : a function used to detrend the data for the
          correlation and spectral functions

          fmt     : the plot format string
        """
        data = self.samples

	# Here we use a rather strange idiom: we create an empty do
        # nothing class C and simply attach attributes to it for
        # return value (which we carefully describe in the docstring).
        # The alternative is either to return a tuple a,b,c,d or a
        # dictionary {'a':someval, 'b':someotherval} but both of these
        # methods have problems.  If you return a tuple, and later
        # want to return something new, you have to change all the
        # code that calls this function.  Dictionaries work fine, but
        # I find the client code harder to use d['a'] vesus d.a.  The
        # final alternative, which is most suitable for production
        # code, is to define a custom class to store (and pretty
        # print) your return object
        class C: pass
        c = C()
        N = 5
        fig = c.fig = figfunc()
        ax = c.ax1 = fig.add_subplot(N,1,1)
        c.plot = ax.plot(data, fmt)

        # XXX the rest of the plot funtions here

        
        return c


if __name__=='__main__':

    # load the data in filename fname into the list data, which is a
    # list of floating point values, one value per line.  Note you
    # will have to do some extra parsing
    data = []
    #fname = 'data/nm560.dat'  # tree rings in New Mexico 837-1987
    fname = 'data/hsales.dat'  # home sales
    for line in file(fname):
        line = line.strip()
        if not line: continue
        # XXX convert to float and add to data here
        
    desc = Descriptives(data)
    print desc
    c = desc.plots(pylab.figure, Fs=12, fmt='-o')
    c.ax1.set_title(fname)
    pylab.show()
