#!/usr/bin/env python
"""Blitz conversion is terrific, but sometimes you don't have fixed array sizes
in your problem. Fortunately numpy iterators still make writing inline weave
code very, very simple."""

import sys

import numpy as np
from numpy.testing.utils import jiffies

from matplotlib import pyplot as plt

from scipy.weave import inline, converters, blitz

# A little timing utility taken from the old scipy.testing
def measure(code_str,times=1):
    """ Return elapsed time for executing code_str in the
    namespace of the caller for given times.
    """
    frame = sys._getframe(1)
    locs,globs = frame.f_locals,frame.f_globals
    code = compile(code_str,'<Timing code>','exec')
    i = 0
    elapsed = jiffies()
    while i<times:
        i += 1
        exec code in globs,locs
    elapsed = jiffies() - elapsed
    return 0.01*elapsed


def multi_iter_example():
    # This is a very simple example of multi dimensional iterators, and
    # their power to "broadcast" arrays of compatible shapes. It shows that
    # the very same code that is entirely ignorant of dimensionality can
    # achieve completely different computations based on the rules of
    # broadcasting.

    # it is important to know that the weave array conversion of "a"
    # gives you access in C++ to:
    # py_a -- PyObject *
    # a_array -- PyArrayObject *
    # a -- py_array->data cast to the proper data type
    
    a = np.ones((4,4), np.float64)
    # for the sake of driving home the "dynamic code" approach...
    dtype2ctype = {
        np.dtype(np.float64): 'double',
        np.dtype(np.float32): 'float',
        np.dtype(np.int32): 'int',
        np.dtype(np.int16): 'short',
    }
    dt = dtype2ctype.get(a.dtype)
    
    # this code does a = a*b inplace, broadcasting b to fit the shape of a
    code = \
"""
%s *p1, *p2;
PyObject *itr;
itr = PyArray_MultiIterNew(2, a_array, b_array);
while(PyArray_MultiIter_NOTDONE(itr)) {
  p1 = (%s *) PyArray_MultiIter_DATA(itr, 0);
  p2 = (%s *) PyArray_MultiIter_DATA(itr, 1);
  *p1 = (*p1) * (*p2);
  PyArray_MultiIter_NEXT(itr);
}
""" % (dt, dt, dt)

    b = np.arange(4, dtype=a.dtype)
    print '\n         A                  B     '
    print a, b
    # this reshaping is redundant, it would be the default broadcast
    b.shape = (1,4)
    inline(code, ['a', 'b'])
    print "\ninline version of a*b,"
    print a
    a = np.ones((4,4), np.float64)
    b.shape = (4,1)
    inline(code, ['a', 'b'])
    print "\ninline version of a*b[:,None],"
    print a

def data_casting_test():
    # In my MR application, raw data is stored as a file with one or more
    # (block-hdr, block-data) pairs. Block data is one or more
    # rows of Npt complex samples in big-endian integer pairs (real, imag).
    #
    # At the block level, I encounter three different raw data layouts--
    # 1) one plane, or slice: Y rows by 2*Npt samples
    # 2) one volume: Z slices * Y rows by 2*Npt samples
    # 3) one row sliced across the z-axis: Z slices by 2*Npt samples
    #
    # The task is to tease out one volume at a time from any given layout,
    # and cast the integer precision data into a complex64 array.
    # Given that contiguity is not guaranteed, and the number of dimensions
    # can vary, Numpy iterators are useful to provide a single code that can
    # carry out the conversion.
    #
    # Other solutions include:
    # 1) working entirely with the string data from file.read() with string
    #    manipulations (simulated below).
    # 2) letting numpy handle automatic byteorder/dtype conversion
    
    nsl, nline, npt = (20,64,64)
    hdr_dt = np.dtype('>V28')
    # example 1: a block is one slice of complex samples in short integer pairs
    blk_dt1 = np.dtype(('>i2', nline*npt*2))
    dat_dt = np.dtype({'names': ['hdr', 'data'], 'formats': [hdr_dt, blk_dt1]})
    # create an empty volume-- nsl contiguous blocks
    vol = np.empty((nsl,), dat_dt)
    t = time_casting(vol[:]['data'])
    plt.plot(100*t/t.max(), 'b--', label='vol=20 contiguous blocks')
    plt.plot(100*t/t.max(), 'bo')
    # example 2: a block is one entire volume
    blk_dt2 = np.dtype(('>i2', nsl*nline*npt*2))
    dat_dt = np.dtype({'names': ['hdr', 'data'], 'formats': [hdr_dt, blk_dt2]})
    # create an empty volume-- 1 block
    vol = np.empty((1,), dat_dt)
    t = time_casting(vol[0]['data'])
    plt.plot(100*t/t.max(), 'g--', label='vol=1 contiguous block')
    plt.plot(100*t/t.max(), 'go')    
    # example 3: a block slices across the z dimension, long integer precision
    # ALSO--a given volume is sliced discontiguously
    blk_dt3 = np.dtype(('>i4', nsl*npt*2))
    dat_dt = np.dtype({'names': ['hdr', 'data'], 'formats': [hdr_dt, blk_dt3]})
    # a real data set has volumes interleaved, so create two volumes here
    vols = np.empty((2*nline,), dat_dt)
    # and work on casting the first volume
    t = time_casting(vols[0::2]['data'])
    plt.plot(100*t/t.max(), 'r--', label='vol=64 discontiguous blocks')
    plt.plot(100*t/t.max(), 'ro')    
    plt.xticks([0,1,2], ('strings', 'numpy auto', 'inline'))
    plt.gca().set_xlim((-0.25, 2.25))
    plt.gca().set_ylim((0, 110))
    plt.gca().set_ylabel(r"% of slowest time")
    plt.legend(loc=8)
    plt.title('Casting raw file data to an MR volume')
    plt.show()
    

def time_casting(int_data):
    nblk = 1 if len(int_data.shape) < 2 else int_data.shape[0]
    bias = (np.random.rand(nblk) + \
            1j*np.random.rand(nblk)).astype(np.complex64)
    dstr = int_data.tostring()
    dt = np.int16 if int_data.dtype.itemsize == 2 else np.int32
    fshape = list(int_data.shape)
    fshape[-1] = fshape[-1]/2
    float_data = np.empty(fshape, np.complex64)
    # method 1: string conversion
    float_data.shape = (np.product(fshape),)
    tstr = measure("float_data[:] = complex_fromstring(dstr, dt)", times=25)
    float_data.shape = fshape
    print "to-/from- string: ", tstr, "shape=",float_data.shape

    # method 2: numpy dtype magic
    sl = [None, slice(None)] if len(fshape)<2 else [slice(None)]*len(fshape)
    # need to loop since int_data need not be contiguous
    tnpy = measure("""
for fline, iline, b in zip(float_data[sl], int_data[sl], bias):
    cast_to_complex_npy(fline, iline, bias=b)""", times=25)
    print"numpy automagic: ", tnpy

    # method 3: plain inline brute force!
    twv = measure("cast_to_complex(float_data, int_data, bias=bias)",
                  times=25)
    print"inline casting: ", twv
    return np.array([tstr, tnpy, twv], np.float64)
    
def complex_fromstring(data, numtype):
    if sys.byteorder == "little":
        return np.fromstring(
            np.fromstring(data,numtype).byteswap().astype(np.float32).tostring(),
            np.complex64)
    else:
        return np.fromstring(
	    np.fromstring(data,numtype).astype(np.float32).tostring(),
            np.complex64)

def cast_to_complex(cplx_float, cplx_integer, bias=None):
    if cplx_integer.dtype.itemsize == 4:
        replacements = tuple(["l", "long", "SWAPLONG", "l"]*2)
    else:
        replacements = tuple(["s", "short", "SWAPSHORT", "s"]*2)
    if sys.byteorder == "big":
        replacements[-2] = replacements[-6] = "NOP"

    cast_code = """
    #define SWAPSHORT(x) ((short) ((x >> 8) | (x << 8)) )
    #define SWAPLONG(x) ((long) ((x >> 24) | (x << 24) | ((x & 0x00ff0000) >> 8) | ((x & 0x0000ff00) << 8)) )
    #define NOP(x) x
    
    unsigned short *s;
    unsigned long *l;
    float repart, impart;
    PyObject *itr;
    itr = PyArray_IterNew(py_cplx_integer);
    while(PyArray_ITER_NOTDONE(itr)) {

      // get real part
      %s = (unsigned %s *) PyArray_ITER_DATA(itr);
      repart = %s(*%s);
      PyArray_ITER_NEXT(itr);
      // get imag part
      %s = (unsigned %s *) PyArray_ITER_DATA(itr);
      impart = %s(*%s);
      PyArray_ITER_NEXT(itr);
      *(cplx_float++) = std::complex<float>(repart, impart);

    }
    """ % replacements
    
    inline(cast_code, ['cplx_float', 'cplx_integer'])
    if bias is not None:
        if len(cplx_float.shape) > 1:
            bsl = [slice(None)]*(len(cplx_float.shape)-1) + [None]
        else:
            bsl = slice(None)
        np.subtract(cplx_float, bias[bsl], cplx_float)

def cast_to_complex_npy(cplx_float, cplx_integer, bias=None):
    cplx_float.real[:] = cplx_integer[0::2]
    cplx_float.imag[:] = cplx_integer[1::2]
    if bias is not None:
        np.subtract(cplx_float, bias, cplx_float)

if __name__=="__main__":
    data_casting_test()
    multi_iter_example()
