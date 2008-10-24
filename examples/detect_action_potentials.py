"""
In this example we will load binary membrane potential data from a
spiking neuron sampled at 2kHz, plot the voltage response vs time, and
write and algorithm to detect action potentials
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab

# Load the data from the file 'data/membrane.dat'.  The data are
# stored as a single array of 4-byte floats.  To scale the data into
# millivolts, multiple thebinary data by 100.
#@ HINT: You can use numpy.fromstring to load binary data, and the numpy
#@ datatype for 4-byte floats is np.float32
v = 100*np.fromfile('data/membrane.dat', np.float32) #@

# create an evenly sampled time array the same length as v samed at
# 2kHz.  The array should be in seconds
#@ HINT: use np.arange to create an array of len(v) integers and then
#@ multiple by the stepsize 1/sampling frequency
t = np.arange(len(v))/2000. #@

# now plot the data, millivolts versus seconds, make an xlabel,
# ylabel, title and grid
fig = plt.figure()                     #@
ax = fig.add_subplot(111)              #@
ax.plot(t, v)                          #@
ax.set_xlabel('time (s)')              #@
ax.set_ylabel('mV')                    #@
ax.set_title('Spiking aplysia neuron') #@
ax.grid(True)                          #@

# now let's write an alogirthm to detect the times that an action
# potential occurs at.  Plot a vertical line at each action potential
# time from the maximum voltage in the train (approx 5 mV but measure
# this from v) to the mx + 20mV.  Use a simple algorithm which detects
# an action potential any time the voltage crosses -10mV from below.
# You can use a loop when practicing, but this should be done in numpy
# w/o a loop for full credit (and it will be much faster)

#@ HINT: create a boolean array equal to length(v) which is True if
#@ v>-10.  Do the same where v<=-10.  An action potential wjere the
#@ above condition is True and the below condition was True one index
#@ before.  In the indexing below, we add 1 to correct for the [1:]
#@ slicing in the logical test.  np.where turns the logical mask into
#@ an index array For example, the following finds the indicies where
#@ the uniform random numbers are above .95::
#@    x = np.random.rand(100)
#@    ind = np.where(x>0.95)[0]
above = v>-10                                 #@
below = v<=-10                                #@
ind = np.where(above[1:] & below[:-1])[0] + 1 #@
vmax = v.max()                                #@
ax.vlines(t[ind], vmax, vmax+20)              #@

# That was the easy way, but if we want a routine that works in batch,
# where we may not have the leisure to visually inspect the graph to
# find the threshold for action potentials (-10 in the example above)
# we have to bee a bit cleverer.  A standard approach in the
# neurobiology community is to use the 2nd derivative of the voltage
# series, and when this is sufficiently positive, trigger an action
# potential.  Write a function that detects action potentials and test
# it for several scalings of v which add an arbitrary constant and
# multiply it by an arbitrary scaling
def detect(t, vstar, refractory=0.05, percent_voltage=90., percent_d2=95.,
           makefig=None):
    """
    detect action potentials in vstar and return the indices.  Remove
    any event whose distance from the previous event is less than the
    refractory period -- neurons are known to have a minimum time
    between sikes and this will help remove duplicate events for each
    spike.  Return value is a numpy array of indices where the
    conditions are met

    Input parameters
    ----------------

    *t*
        the time array in seconds

    *vstar*
        the voltage array, equal to len(t)

    *refractory*
        the refractory period of the neuron, the minimum time in
        seconds between action potentials

    *percent_voltage*
        an action potential must be in at least the percent voltage
        percentile.  Eg, if *percent_voltage*=95, the the voltage at the
        spike must be at or above the 95th percentile of vstar

    *percent_d2*
        The second derivative of voltage must be in at least the
        *percent_d2*-th percentile of second derivatives.

    *makefig*
        if *makefig* is not None, it is a matplotlib figure instance in
        which to plot diagnostic information like the voltage trace,
        the detected action potentials, the 2nd derivative of voltage,
        and the *percent_voltage* and *percent_d2* tresholds
    """
    # make sure *t* and *vstar* are numpy arrays
    #@ HINT: use np.asarray
    t = np.asarray(t)
    vstar = np.asarray(vstar)

    # Compute the 2nd derivative *d2* of *vstar* and measure the
    # *percent_d2* cutoff percentile of all 2nd derivatives.  Create a
    # boolean mask array of len(v2) called *mask2* which is True
    # everwhere that *d2* is >= cutoff.

    #@ HINT: use np.diff(vstar, 2) to compute the 2nd derivative, and
    #@ remember that the returned array will be two shorter than vstar,
    #@ so you will have to index into your mask array starting in the
    #@ 2nd position.  You can use matplotlib.mlab.prctile to compute the
    #@ percentiles
    d2 = np.diff(vstar, 2)                       #@
    threshold, = mlab.prctile(d2, (percent_d2,)) #@
    mask2 = np.zeros(len(v2), np.bool)           #@
    mask2[2:] = d2>=threshold                    #@


    # Now for the voltage check: the voltage at the action potentials
    # must greater than the *percent_voltage* percentile, sometimes
    # membrane noise has a large *d2*, so the 2nd derivative check
    # alone is not sufficient to be sure we have an action potential.
    # Create a boolean mask of len(v2) called *mask* that is True
    # where *vstar* >= cutoff
    cutoff, = mlab.prctile(vstar, (percent_voltage, )) #@
    mask = vstar>=cutoff                               #@

    # Now check the refractory condition -- the minimum time between
    # spikes must be >= *refractory*.  The default mask is True
    # because the first spike will always be > refractory period First
    # create the indices where both conditions in *mask* and *mask2*
    # are True, find the times corresponding to these indicies, and
    # only kee the times where the interspike-interval (the diff
    # between times) >= refractory period.
    ind = np.nonzero(mask & mask2) [0]    #@
    times = t[ind]                        #@
    mask = np.ones(len(times), np.bool)   #@
    mask[1:] = np.diff(times)>=refractory #@
    ind = ind[mask]                       #@


    if makefig is None: return ind

    fig = makefig
    # plot *t* vs *vstar*, as before, but in an upper subplot plot the
    # vlines as before, but you will have to figure out how big to
    # make the vlines based on the min/max range of vstar
    ax1 = fig.add_subplot(211)                #@
    ax1.plot(t, vstar)                        #@
    ax1.axhline(cutoff)                       #@
    vmax = vstar.max()                        #@
    vrange = vmax-vstar.min()                 #@
    ax1.vlines(t[ind], vmax, vmax+0.1*vrange) #@

    # make a lower subplot to show d2 and the threshold; use the
    # *sharex* keyword arg to link the x axis in the two subplots so as
    # you pan and zoom in one, the other will be updated
    ax2 = fig.add_subplot(212, sharex=ax1) #@
    ax2.plot(t[2:], d2)                    #@
    ax2.set_ylabel('2nd deriv')            #@
    ax2.axhline(threshold)                 #@

    # now just return the indices
    return ind


v1 = 20 + 20*v
v2 = -100 + 0.1*v

fig1 = plt.figure()
fig1.suptitle('Test auto-detect 1')
ind1 = detect(t, v1, makefig=fig1)

fig2 = plt.figure()
fig2.suptitle('Test auto-detect 2')
ind2 = detect(t, v2, makefig=fig2)

plt.show()
