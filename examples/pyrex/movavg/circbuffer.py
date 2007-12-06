import numpy as npy

class CircularBuffer:
    def __init__(self, N):
        self.i = 0
        self.data = npy.zeros(N)
        self.N = N

    def add(self, val):
        self.data[self.i%self.N] = val
        self.i += 1

    def get_data(self):
        if self.i<self.N:
            return self.data[:self.i]
        else:
            return self.data



