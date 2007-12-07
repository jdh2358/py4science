"""
ringbuf.pyx Pyrex interface to ringbuf.c It defines ring buffer class,
Ringbuf, on which various statistics are calculated as each entry is
added and a method runstats for computing a host of trailing
statistics over a numpy array
"""

include "c_ringbuf.pxi"

# ringbuf is a C library, but we can give it a pythonic object
# oriented API by managing the ringbuf pointers and function calls in
# a python class

cdef class Ringbuf:
   cdef ringbuf_t *rb_ptr

   def __new__(self, N):
      self.rb_ptr = new_ringbuf(N)

   def __dealloc__(self):
      delete_ringbuf(self.rb_ptr)

   def __getitem__(self, i):
      ret = ringbuf_getitem(self.rb_ptr, i)
      if ret == 1e38:
         raise IndexError("hit bad value marker")
      return ret

   def __len__(self):
      return ringbuf_N_filled(self.rb_ptr)

   def __getslice__(self, i0, i1):
      xx = list()
      i0 = max(0, i0)
      i1 = min(ringbuf_N_filled(self.rb_ptr), i1)
      for i in range(i0, i1):
         x = ringbuf_getitem(self.rb_ptr, i)
         if x == 1e38:
            raise IndexError("hit bad value marker")
         xx.append(x)
      return xx

   def empty(self):
      zero_ringbuf(self.rb_ptr)

   def add(self, d):
      ringbuf_add(self.rb_ptr, d)

   def min(self):
      return ringbuf_min(self.rb_ptr)

   def max(self):
      return ringbuf_max(self.rb_ptr)

   def median(self):
      return ringbuf_median(self.rb_ptr)

   def N_added(self):
      return ringbuf_N_added(self.rb_ptr)

   def N_good(self):
      return ringbuf_N_good(self.rb_ptr)

   def mean(self):
      return ringbuf_mean(self.rb_ptr)

   def sd(self):
      return ringbuf_sd(self.rb_ptr)


cdef class RingbufRecords:
   cdef ringbuf_t *rb_ptr

   cdef object records

   def __new__(self, N):
      self.rb_ptr = new_ringbuf(N)
      self.records = []

   def __dealloc__(self):
      delete_ringbuf(self.rb_ptr)
      del self.records[:]

   def __getitem__(self, i):
      r = self.records[i]
      ret = ringbuf_getitem(self.rb_ptr, i)
      if ret == 1e38:
         raise IndexError("hit bad value marker")
      return ret, r

   def __len__(self):
      return ringbuf_N_filled(self.rb_ptr)

   def __getslice__(self, i0, i1):
      xx = list()
      i0 = max(0, i0)
      i1 = min(ringbuf_N_filled(self.rb_ptr), i1)
      for i in range(i0, i1):
         x = ringbuf_getitem(self.rb_ptr, i)
         if x == 1e38:
            raise IndexError("hit bad value marker")
         xx.append(x)
      return xx, self.records[i0:i1]


   def empty(self):
      zero_ringbuf(self.rb_ptr)
      self.records = []

   def add(self, d, r):
      ringbuf_add(self.rb_ptr, d)
      self.records.append(r)
      if len(self.records) > self.rb_ptr.N_size:
         del self.records[0]

   def min(self):
      return ringbuf_min(self.rb_ptr)

   def max(self):
      return ringbuf_max(self.rb_ptr)

   def median(self):
      return ringbuf_median(self.rb_ptr)

   def N_added(self):
      return ringbuf_N_added(self.rb_ptr)

   def N_good(self):
      return ringbuf_N_good(self.rb_ptr)

   def mean(self):
      return ringbuf_mean(self.rb_ptr)

   def sd(self):
      return ringbuf_sd(self.rb_ptr)




# now we'll provide a numpy interface to the runstats function, which
# fills predimensioned arrays with the trailing mean, std, max, etc,
# for a data array
cimport c_numpy
import numpy
c_numpy.import_array()

def runstats(data, nrb):
    """
    Compute running stats on 1D array data over window length nrb
    """

    # we will be calling the ringbuf C function runstats, which
    # expects a bunch of c data pointers to the data arrays as well as
    # the output arrays for the mean, std, etc...  Create a array for
    # each C float array pointer the C function expects.  The type of
    # the array is c_numpy.ndarray
    cdef c_numpy.ndarray c_data
    cdef c_numpy.ndarray c_dmean
    cdef c_numpy.ndarray c_dstd
    cdef c_numpy.ndarray c_dmin
    cdef c_numpy.ndarray c_dmax
    cdef c_numpy.ndarray c_dmedian
    cdef c_numpy.ndarray c_ng

    # make sure that the input array is a 1D numpy array of floats.
    # asarray is used to copy and cast a python sequence or array to
    # the approriate type, with the advantage that if the data is
    # already the right type, no copy is performed
    data = numpy.asarray(data, dtype=numpy.float_)
    if data.ndim != 1:
        raise ValueError("data must be 1-D for now")
    nd = data.shape[0]

    # use numpy.empty_like to create and empty array of the same type
    # and shape as data for each of the return stats (mean, std, ...)
    # These are genuine numpy arrays we will be passing back to the
    # python level. Remember the ng (the number of good elements) is
    # an int, and everything else is a float
    dmean = numpy.empty_like(data)
    dstd = numpy.empty_like(data)
    dmin = numpy.empty_like(data)
    dmax = numpy.empty_like(data)
    dmedian = numpy.empty_like(data)
    ng = numpy.empty(data.shape, dtype=numpy.int_)

    # now we have to assign the c_data structures and friends to their
    # corresponding numpy arrays
    c_data = data
    c_dmean = dmean
    c_dstd = dstd
    c_dmin = dmin
    c_dmax = dmax
    c_dmedian = dmedian
    c_ng = ng

    # now we call the function and pass in the c data pointers to the
    # arrays.  The syntax <double *>c_data.data tells pyrex to pass
    # the numpy data memory block as a pointer to a float array.
    c_runstats(nrb, nd, <double *>c_data.data,
                        <double *>c_dmean.data,
                        <double *>c_dstd.data,
                        <double *>c_dmin.data,
                        <double *>c_dmax.data,
                        <double *>c_dmedian.data,
                        <int *>c_ng.data)

    # all done, return the arrays
    return dmean, dstd, dmin, dmax, dmedian, ng
