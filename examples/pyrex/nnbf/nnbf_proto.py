"""
A brute force nearest neighbor routine
"""
import math
import numpy as np

class NNBF:
    def __init__(self, n):
        """
        create a buffer to hold n dimensional points
        """
        self.n = n
        self.numrows = 100
        self.data = np.empty((self.numrows, self.n), np.float)
        self.numpoints = 0

    def add(self, point):
        self.data[self.numpoints] = point
        self.numpoints += 1
        if self.numpoints==self.numrows:
            self.numrows *= 2
            newdata = np.empty((self.numrows, self.n), np.float)
            newdata[:self.numpoints] = self.data
            self.data = newdata

    def get_data(self):
        """
        return a copy of data added so far
        """
        return self.data[:self.numpoints]


    def find_neighbors(self, point, radius):
        """
        return a list of indices into data which are within radius
        from point
        """
        data = self.get_data()
        neighbors = []
        for i in range(self.numpoints):
            row = data[i]
            fail = False
            d2 = 0.
            for j in range(self.n):
                rowval = row[j]
                pntval = point[j]
                d = rowval-pntval
                if d>radius:
                    fail = True
                    break
                d2 += d*d

            if fail: continue

            r = math.sqrt(d2)
            if r<=radius:
                neighbors.append(i)

        return neighbors

    def find_neighbors_numpy(self, point, radius):
        """
        Use plain ol numpy to find neighbors
        """
        data = self.get_data()
        neighbors = []
        for i in range(self.numpoints):
            row = data[i]
            fail = False
            d2 = 0.
            for j in range(self.n):
                rowval = row[j]
                pntval = point[j]
                d = rowval-pntval
                if d>radius:
                    fail = True
                    break
                d2 += d*d

            if fail: continue

            r = math.sqrt(d2)
            if r<=radius:
                neighbors.append(i)

        return neighbors

def find_neighbors_numpy(data, point, radius):
    """
    do a plain ol numpy lookup to compare performance and output

      *data* is a numpoints x numdims array
      *point* is a numdims length vector
      radius is the max distance distance

    return an array of indices into data which are within radius
    """
    numpoints, n = data.shape

    distance = data - point
    r = np.sqrt((distance*distance).sum(axis=1))
    return np.nonzero(r<=radius)[0]
