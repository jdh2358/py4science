import matplotlib.numerix as nx
from matplotlib.mlab import polyfit
from matplotlib.cbook import iterable

class SomeMap:
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
        iterates = self.iterate(x0, numsteps)
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

    def iterate(self, x0, numsteps, lastonly=False):
        """
        iterate self starting at x0 for numsteps

        Return value is an array of the time-series.  If x0 is a scalar, a
        numsteps+1 length 1D vector is returned with x0 as the first
        value. If x0 is a vector, an numsteps+1 x len(x0) 2D array is
        returned with x0 as the first row

        if lastonly is True, only return the last iterate
        """
        if not lastonly:
            if iterable(x0): # return a 2D array
                ret = nx.zeros( (numsteps+1,len(x0)), typecode=nx.Float )
            else:            # return a 1D array
                ret = nx.zeros( (numsteps+1,), typecode=nx.Float )        

        # assign the initial condtion to the 0-th element
        if not lastonly: ret[0] = x0

        # iterate the map for numsteps
        last = x0
        for i in range(1,numsteps+1):
            this = self(last)
            if not lastonly: ret[i] = this
            last = this
            
        if lastonly:
            return last
        else:
            return ret

class Logistic(SomeMap):

    def __init__(self, mu):
        self.R = 4.*mu

    def __call__(self, x):
        'iterate self one step starting at x.  x can be a scalar or array'
        return self.R*x*(1.-x)

class Sine(SomeMap):

    def __init__(self, B):
        self.B = B

    def __call__(self, x):
        'iterate self one step starting at x.  x can be a scalar or array'
        return self.B*nx.sin(nx.pi*x)
    
def test():
    m = Logistic(0.9)
    x0 = nx.mlab.rand(100)
    ret = m.iterate(x0, 3)
    assert( ret.shape == 4,100)

    x0 = 0.2
    ret = m.iterate(x0, 3)
    assert( ret.shape == 4,)
    
    print 'all tests passed'

if __name__=='__main__':
    test()
