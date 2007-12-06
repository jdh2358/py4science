#!/usr/bin/env python
def slopes(x,y):
    """
    SLOPES calculate the slope y'(x) Given data vectors X and Y SLOPES
    calculates Y'(X), i.e the slope of a curve Y(X). The slope is
    estimated using the slope obtained from that of a parabola through
    any three consecutive points.

    This method should be superior to that described in the appendix
    of A CONSISTENTLY WELL BEHAVED METHOD OF INTERPOLATION by Russel
    W. Stineman (Creative Computing July 1980) in at least one aspect:

    Circles for interpolation demand a known aspect ratio between x-
    and y-values.  For many functions, however, the abscissa are given
    in different dimensions, so an aspect ratio is completely
    arbitrary.
    
    The parabola method gives very similar results to the circle
    method for most regular cases but behaves much better in special
    cases

    Norbert Nemec, Institute of Theoretical Physics, University or
    Regensburg, April 2006 Norbert.Nemec at physik.uni-regensburg.de

    (inspired by a original implementation by Halldor Bjornsson,
    Icelandic Meteorological Office, March 2006 halldor at vedur.is)
    """
    # Cast key variables as float.
    x=nx.asarray(x, nx.Float)
    y=nx.asarray(y, nx.Float)

    yp=nx.zeros(y.shape, nx.Float)

    dx=x[1:] - x[:-1]
    dy=y[1:] - y[:-1]
    dydx = dy/dx
    yp[1:-1] = (dydx[:-1] * dx[1:] + dydx[1:] * dx[:-1])/(dx[1:] + dx[:-1])
    yp[0] = 2.0 * dy[0]/dx[0] - yp[1]
    yp[-1] = 2.0 * dy[-1]/dx[-1] - yp[-2]
    return yp


def stineman_interp(xi,x,y,yp=None):
    """
    STINEMAN_INTERP Well behaved data interpolation.  Given data
    vectors X and Y, the slope vector YP and a new abscissa vector XI
    the function stineman_interp(xi,x,y,yp) uses Stineman
    interpolation to calculate a vector YI corresponding to XI.

    Here's an example that generates a coarse sine curve, then
    interpolates over a finer abscissa:

      x = linspace(0,2*pi,20);  y = sin(x); yp = cos(x)
      xi = linspace(0,2*pi,40);
      yi = stineman_interp(xi,x,y,yp);
      plot(x,y,'o',xi,yi)

    The interpolation method is described in the article A
    CONSISTENTLY WELL BEHAVED METHOD OF INTERPOLATION by Russell
    W. Stineman. The article appeared in the July 1980 issue of
    Creative computing with a note from the editor stating that while
    they were

      not an academic journal but once in a while something serious
      and original comes in adding that this was
      "apparently a real solution" to a well known problem.
    
    For yp=None, the routine automatically determines the slopes using
    the "slopes" routine.

    X is assumed to be sorted in increasing order

    For values xi[j] < x[0] or xi[j] > x[-1], the routine tries a
    extrapolation.  The relevance of the data obtained from this, of
    course, questionable...

    original implementation by Halldor Bjornsson, Icelandic
    Meteorolocial Office, March 2006 halldor at vedur.is

    completely reworked and optimized for Python by Norbert Nemec,
    Institute of Theoretical Physics, University or Regensburg, April
    2006 Norbert.Nemec at physik.uni-regensburg.de
    """

    # Cast key variables as float.
    x=nx.asarray(x, nx.Float)
    y=nx.asarray(y, nx.Float)
    assert x.shape == y.shape
    N=len(y)

    if yp is None:
        yp = slopes(x,y)
    else:
        yp=nx.asarray(yp, nx.Float)

    xi=nx.asarray(xi, nx.Float)
    yi=nx.zeros(xi.shape, nx.Float)

    # calculate linear slopes
    dx = x[1:] - x[:-1]
    dy = y[1:] - y[:-1]
    s = dy/dx  #note length of s is N-1 so last element is #N-2

    # find the segment each xi is in
    # this line actually is the key to the efficiency of this implementation
    idx = nx.searchsorted(x[1:-1], xi)

    # now we have generally: x[idx[j]] <= xi[j] <= x[idx[j]+1]
    # except at the boundaries, where it may be that xi[j] < x[0] or xi[j] > x[-1]

    # the y-values that would come out from a linear interpolation:
    sidx = nx.take(s, idx)
    xidx = nx.take(x, idx)
    yidx = nx.take(y, idx)    
    xidxp1 = nx.take(x, idx+1)
    yo = yidx + sidx * (xi - xidx)

    # the difference that comes when using the slopes given in yp
    dy1 = (nx.take(yp, idx)- sidx) * (xi - xidx)       # using the yp slope of the left point
    dy2 = (nx.take(yp, idx+1)-sidx) * (xi - xidxp1) # using the yp slope of the right point

    dy1dy2 = dy1*dy2
    # The following is optimized for Python. The solution actually
    # does more calculations than necessary but exploiting the power
    # of numpy, this is far more efficient than coding a loop by hand
    # in Python
    yi = yo + dy1dy2 * nx.choose(nx.array(nx.sign(dy1dy2), nx.Int32)+1, 
                                 ((2*xi-xidx-xidxp1)/((dy1-dy2)*(xidxp1-xidx)),
                                  0.0,
                                  1/(dy1+dy2),))
        
    return yi

if __name__ == '__main__':
    # Here is some example code

    from pylab import figure, show, nx, linspace

    x = linspace(0,2*nx.pi,20);
    y = nx.sin(x); yp = None 
    xi = linspace(x[0],x[-1],100);
    yi = stineman_interp(xi,x,y,yp);

    fig = figure()
    ax = fig.add_subplot(111)
    ax.plot(x,y,'ro',xi,yi,'-b.')
    show()
