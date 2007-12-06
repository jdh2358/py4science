''' pyringbuf.pyx Pyrex interface to ringbuf.c
    It defines a single ring buffer class, Ringbuf,
    on which various statistics are calculated
    as each entry is added.
'''

include "c_ringbuf.pxi"

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




