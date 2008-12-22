
cdef extern from "ringbuf.h":
   ctypedef struct ringbuf_t:
       int N_size
       int N_filled
       int N_good
       int i_oldest
       int i_next
       int *i_sorted
       double *data
       double sum
       double sumsq
   ringbuf_t *new_ringbuf(int N)
   void zero_ringbuf(ringbuf_t *rb_ptr)
   void delete_ringbuf(ringbuf_t *rb_ptr)
   int ringbuf_add(ringbuf_t *rb_ptr, double d)
   double ringbuf_getitem(ringbuf_t *rb_ptr, int i)
   double ringbuf_min(ringbuf_t *rb_ptr)
   double ringbuf_max(ringbuf_t *rb_ptr)
   double ringbuf_median(ringbuf_t *rb_ptr)
   double ringbuf_ptile(ringbuf_t *rb_ptr, double x)
   int    ringbuf_N_good(ringbuf_t *rb_ptr)
   int    ringbuf_N_added(ringbuf_t *rb_ptr)
   int    ringbuf_N_filled(ringbuf_t *rb_ptr)
   double ringbuf_mean(ringbuf_t *rb_ptr)
   double ringbuf_sd(ringbuf_t *rb_ptr)
   void c_runstats (int nrb, int nd, double *data,
                                            double *dmean,
                                            double *dstd,
                                            double *dmin,
                                            double *dmax,
			                    double *dmed,
                                            double *dptile5,
                                            double *dptile95,
                                            int *nsorted,
                                            int *ng)
   void c_runstats2(int nrb, int nd, int step, int ofs,
                 double *data, double *dmean, double *dstd,
		    double *dmin, double *dmax, double *dmed, double *dptile5,
		    double *dptile95, int *nsorted, int *ng)
