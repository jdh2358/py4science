"""
Illustrate the connections bettwen the uniform, exponential, gamma and
normal distributions by simulating waiting times from a radioactive
source using the random number generator.  Verify the numerical
results by plotting the analytical density functions from scipy.stats
"""
import numpy as npy
import scipy.stats
from pylab import figure, show, close


# N samples from a uniform distribution on the unit interval.  Create
# a uniform distribution from scipy.stats.uniform and use the "rvs"
# method to generate N uniform random variates
N = 100000
uniform = scipy.stats.uniform()  # the frozed uniform distribution
uninse = uniform.rvs(N)          # the random variates

# in each time interval, the probability of an emission 
rate = 20.  # the emission rate in Hz
dt = 0.001  # the sampling interval in seconds
t = npy.arange(N)*dt  # the time vector

# the probability of an emission is proportionate to the rate and the interval
emit_times = t[uninse < rate*dt]

# the difference in the emission times is the wait time
wait_times = npy.diff(emit_times)  

# plot the distribution of waiting times and the expected exponential
# density function lambda exp( lambda wt) where lambda is the rate
# constant and wt is the wait time; compare the result of the analytic
# function with that provided by scipy.stats.exponential.pdf; note
# that the scipy.stats.expon "scale" parameter is inverse rate
# 1/lambda.  Plot all three on the same graph and make a legend.
# Decorate your graphs with an xlabel, ylabel and title
fig = figure()
ax = fig.add_subplot(111)
p, bins, patches = ax.hist(wait_times, 100, normed=True)
l1, = ax.plot(bins, rate*npy.exp(-rate * bins), lw=2, color='red')
l2, = ax.plot(bins, scipy.stats.expon.pdf(bins, 0, 1./rate),
        lw=2, ls='--', color='green')
ax.set_xlabel('waiting time')
ax.set_ylabel('PDF')
ax.set_title('waiting time density of a %dHz Poisson emitter'%rate)
ax.legend((patches[0], l1, l2), ('simulated', 'analytic', 'scipy.stats.expon'))



# plot the distribution of waiting times for two events; the
# distribution of waiting times for N events should equal a N-th order
# gamma distribution (the exponential distribution is a 1st order
# gamma distribution.  Use scipy.stats.gamma to compare the fits.
# Hint: you can stride your emission times array to get every 2nd
# emission
wait_times2 = npy.diff(emit_times[::2])
fig = figure()
ax = fig.add_subplot(111)
p, bins, patches = ax.hist(wait_times2, 100, normed=True)
l1, = ax.plot(bins, scipy.stats.gamma.pdf(bins, 2, 0, 1./rate),
        lw=2, ls='-', color='red')
ax.set_xlabel('2 event waiting time 2 events')
ax.set_ylabel('PDF')
ax.set_title('waiting time density of a %dHz Poisson emitter'%rate)
ax.legend((patches[0], l1), ('simulated', 'scipy.stats.gamma'))


# plot the distribution of waiting times for 10 events; again the
# distribution will be a 10th order gamma distribution so plot that
# along with the empirical density.  The central limit thm says that
# as we add N indenpendent samples from a distribution, the resultant
# distribution should approach the normal distribution.  The mean of
# the normal should be N times the mean of the underlying and the
# variance of the normal should be 10 times the variance of the
# underlying.  HINT: Use scipy.stats.expon.stats to get the mean and
# variance of the underlying distribution.  Use scipy.stats.norm to
# get the normal distribution.  Note that the scale parameter of the
# normal is the standard deviation which is the square root of the
# variance
expon_mean, expon_var = scipy.stats.expon(0, 1./rate).stats()
mu, var = 10*expon_mean, 10*expon_var
sigma = npy.sqrt(var)
wait_times10 = npy.diff(emit_times[::10])
fig = figure()
ax = fig.add_subplot(111)
p, bins, patches = ax.hist(wait_times10, 100, normed=True)
l1, = ax.plot(bins, scipy.stats.gamma.pdf(bins, 10, 0, 1./rate),
        lw=2, ls='-', color='red')
l2, = ax.plot(bins, scipy.stats.norm.pdf(bins, mu, sigma),
        lw=2, ls='--', color='green')

ax.set_xlabel('waiting time 10 events')
ax.set_ylabel('PDF')
ax.set_title('10 event waiting time density of a %dHz Poisson emitter'%rate)
ax.legend((patches[0], l1, l2), ('simulated', 'scipy.stats.gamma', 'normal approx'))



show()
