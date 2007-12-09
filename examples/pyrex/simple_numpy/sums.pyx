# -*- Mode: Python -*-  Not really, but close enough

cimport c_python
cimport c_numpy
import numpy

# Numpy must be initialized
c_numpy.import_array()

def sum_elements(c_numpy.ndarray arr):
    cdef int i
    cdef double x, val

    x = 0.
    val = 0.
    for i from 0<=i<arr.dimensions[0]:
        val = (<double*>(arr.data + i*arr.strides[0]))[0]
        x = x + val

    return x



def sum_elements2(c_numpy.ndarray arr):
    cdef int i
    cdef double x, val

    arr = numpy.asarray(arr, numpy.float_)

    if arr.nd!=1:
        raise RuntimeError('only 1D arrays supported; found shape=%s'%str(arr.shape))
    assert(arr.nd==1)
    x = 0.
    val = 0.
    for i from 0<=i<arr.dimensions[0]:
        val = (<double*>(arr.data + i*arr.strides[0]))[0]
        x = x + val

    return x
