"""
A brute force nearest neighbor routine with incremental add.  The
internal array data structure grows as you add points
"""

import numpy as np
cimport numpy as np

cdef extern from "math.h":
     float sqrt(float)

cdef inline int is_neighbor(int n, double*row, double*pp, double d2max):
    """
    return 1 if the sum-of-squares of n length array row[j]-pp[j] <= d2max
    """
    cdef int j
    cdef double d, d2

    d2 = 0.

    for j in range(n):
        d = row[j] - pp[j]
        d2 += d*d
        if d2>d2max:
            return 0
    return 1

cdef class NNBF:
    cdef readonly object data
    cdef double* raw_data
    cdef readonly int n, numrows, numpoints

    def __init__(self, n):
        """
        create a buffer to hold n dimensional points
        """
        cdef np.ndarray[double, ndim=2] inner_data


        self.n = n
        self.numrows = 100
        #  XXX how to create mepty as contiguous w/o copy?
        data = np.empty((self.numrows, self.n), dtype=np.float)
        self.data = np.ascontiguousarray(data, dtype=np.float)
        inner_data = self.data
        self.raw_data = <double*>inner_data.data
        self.numpoints = 0


    def add(NNBF self, object point):
        """
        add a point to the buffer, grow if necessary
        """
        cdef np.ndarray[double, ndim=2] inner_data
        cdef np.ndarray[double, ndim=1] pp
        pp = np.asarray(point).astype(np.float)


        self.data[self.numpoints] = pp
        self.numpoints += 1
        if self.numpoints==self.numrows:
            ## XXX do I need to do memory management here, eg free
            ## raw_data if I were using it?
            self.numrows *= 2
            newdata = np.empty((self.numrows, self.n), np.float)
            newdata[:self.numpoints] = self.data
            self.data = np.ascontiguousarray(newdata, dtype=np.float)
            inner_data = self.data
            self.raw_data = <double*>inner_data.data
            #self.raw_data = <double*>inner_data.data

    def get_data(NNBF self):
        """
        return a copy of data added so far as a numpoints x n array
        """
        return self.data[:self.numpoints]


    def find_neighbors(NNBF self, object point, double radius):
        """
        return a list of indices into data which are within radius
        from point
        """
        cdef int i, neighbor, n
        cdef double d2max
        cdef np.ndarray[double, ndim=1] pp

        # avoid python array indexing in the inner loop
        #cdef np.ndarray[double, ndim=1] row
        cdef double * dataptr
        dataptr = <double*> self.data.data
        if len(point)!=self.n:
            raise ValueError('Expected a length %d vector'%self.n)

        pp = np.asarray(point).astype(np.float)

        d2max = radius*radius
        neighbors = []

        # don't do a python lookup inside the loop
        n = self.n
        
        for i in range(self.numpoints):
            # XXX : is there a more efficient way to access the row
            # data?  Can/should we be using raw_data here?
            #row = self.data[i]
            neighbor = is_neighbor(
                n,
                #(<double*>self.data.data)+i*n,
                self.raw_data + i*n,
                #dataptr + i*n,
                <double*>pp.data,
                d2max)

            # if the number of points in the cluster is small, the
            # python list performance should not kill us
            if neighbor:
                neighbors.append(i)

        return neighbors


