import numpy as np

from matplotlib.cbook import iterable

class IteratedMap(object):
    """
    Define an interface for a map
    """
    def __call__(self, x):
        'iterate self one step starting at x.  x can be a scalar or array'
        raise NotImplementedError('Derived must override')
    
    def plot(self, ax, x, **kwargs):
        """
        Plot the first iterate of map over x including the line of identity

        kwargs are passed onto mpl plot
        """
        y = self(x)
        ax.plot(x, y, **kwargs)
        ax.plot(x, x, **kwargs)


    def plot_timeseries(self, ax, x0, numsteps, **kwargs):
        """
        Plot the timeseries in mpl Axes ax by iterating x0 numsteps

        If x0 is a vector, plot each of the timeseries
        """
        y = self.iterate(x0, numsteps)
        if not iterable(x0):
            ax.plot(y, **kwargs)
        else:
            for walker in y:
                ax.plot(walker, **kwargs)
                
        
    def plot_cobweb(self, ax, x0, numsteps, **kwargs):
        """
        ax is a matplotlib axes instance.

        plot the cobweb map of numsteps iterates of x0 

        kwargs are passed onto mpl plot
        """
        iterates = self.trajectory(x0, numsteps)
        vertices = []
        lasty = 0
        for this, next in zip(iterates[:-1], iterates[1:]):
            vertices.append( (this, lasty) )
            vertices.append( (this, next) )
            vertices.append( (this, next) )
            vertices.append( (next, next) )
            lasty = next
        x, y = zip(*vertices)
        ax.plot(x, y, **kwargs)


    def iterator_from(self, x0):
        while 1:
            x0 =  self(x0)
            yield x0


    def iterate_from(self, x0, numsteps):
        for i in xrange(numsteps):
            x0 =  self(x0)
        return x0


    def trajectory(self, x0, numsteps):
        """iterate self starting at x0 for numsteps, returning whole trajectory

        Return value is an array of the time-series.  If x0 is a scalar, a
        numsteps length 1D vector is returned with x0 as the first value. If x0
        is a vector, a 2D array with shape (numsteps, len(x0)) is returned, with
        x0 as the first row.
        """
        if iterable(x0): # return a 2D array
            ret = np.zeros( (numsteps,len(x0)) )
        else:            # return a 1D array
            ret = np.zeros(numsteps)

        # assign the initial condtion to the 0-th element
        ret[0] = x0
        # iterate the map for numsteps
        for i in range(1,numsteps):
            ret[i] = self(ret[i-1])
        return ret

class Logistic(IteratedMap):

    def __init__(self, mu):
        self.R = 4.0*mu

    def __call__(self, x):
        'iterate self one step starting at x.  x can be a scalar or array'
        return self.R*x*(1.0-x)

class Sine(IteratedMap):

    def __init__(self, B):
        self.B = B

    def __call__(self, x):
        'iterate self one step starting at x.  x can be a scalar or array'
        return self.B*np.sin(np.pi*x)
    
def test():
    m = Logistic(0.9)
    x0 = np.random.rand(100)
    ret = m.iterate(x0, 3)
    assert ret.shape == 4,100

    x0 = 0.2
    ret = m.iterate(x0, 3)
    assert  ret.shape == 4
    
    print 'all tests passed'

if __name__=='__main__':
    test()
