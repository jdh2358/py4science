'''
This is kept as a module separate from pyringbuf so that the
latter does not depend on numpy.
'''

cimport c_numpy
import numpy

c_numpy.import_array()

include "c_ringbuf.pxi"


def runstats(data, nrb):
    '''
    Compute running stats on 1D array data for odd length nrb
    '''

    cdef c_numpy.ndarray c_data
    cdef c_numpy.ndarray c_dmean
    cdef c_numpy.ndarray c_dstd
    cdef c_numpy.ndarray c_dmin
    cdef c_numpy.ndarray c_dmax
    cdef c_numpy.ndarray c_dmedian
    cdef c_numpy.ndarray c_ng


    data = numpy.asarray(data, dtype=numpy.float_)
    if data.ndim != 1:
        raise ValueError("data must be 1-D for now")
    nd = data.shape[0]

    dmean = numpy.empty_like(data)
    dstd = numpy.empty_like(data)
    dmin = numpy.empty_like(data)
    dmax = numpy.empty_like(data)
    dmedian = numpy.empty_like(data)
    ng = numpy.empty(data.shape, dtype=numpy.int_)

    c_data = data
    c_dmean = dmean
    c_dstd = dstd
    c_dmin = dmin
    c_dmax = dmax
    c_dmedian = dmedian
    c_ng = ng

    c_runstats(nrb, nd, <double *>c_data.data,
                        <double *>c_dmean.data,
                        <double *>c_dstd.data,
                        <double *>c_dmin.data,
                        <double *>c_dmax.data,
                        <double *>c_dmedian.data,
                        <int *>c_ng.data)
    return dmean, dstd, dmin, dmax, dmedian, ng
