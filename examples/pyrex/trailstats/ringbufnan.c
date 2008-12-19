/*

   Use a ring buffer to calculate running statistics of a data stream.



   compile:
      gcc -Wall -c -fPIC ringbufnan.c


   2003/07/28 EF

*/

#include <stdlib.h>
#include <stdio.h>   /* for debugging printf statements */
#include <math.h>
#include "ringbuf.h"

static double NaN = 0.0;

static void sort_ringbuf(ringbuf_t *rb_ptr);
static void resum_ringbuf(ringbuf_t *rb_ptr);

ringbuf_t *new_ringbuf(int N)
{
   if (!isnan(NaN))
   {
      NaN = strtod("NaN", NULL);  /* May change for Matlab. */
   }
   ringbuf_t *rb_ptr;
   rb_ptr = calloc(1, sizeof(ringbuf_t));
   rb_ptr->i_sorted = calloc(N, sizeof(int));
   rb_ptr->data = calloc(N, sizeof(double));
   rb_ptr->N_size = N;
   zero_ringbuf(rb_ptr);
   return rb_ptr;
}

void zero_ringbuf(ringbuf_t *rb_ptr)
{
   rb_ptr->N_filled = 0;
   rb_ptr->N_good = 0;
   rb_ptr->N_added = 0;
   rb_ptr->i_oldest = 0;
   rb_ptr->i_next = 0;
   rb_ptr->sum = 0.0;
   rb_ptr->sumsq = 0.0;
}

void delete_ringbuf(ringbuf_t *rb_ptr)
{
   free(rb_ptr->data);
   free(rb_ptr->i_sorted);
   free(rb_ptr);
}

int ringbuf_index(ringbuf_t *rb_ptr, int i)
/* i is a Python-style index; return the actual offset, or -1 for error */
{
   /* printf("incoming index: %d", i);*/
   if (i >= rb_ptr->N_filled) return -1;
   if (i < -rb_ptr->N_filled) return -1;
   if (i < 0) i += rb_ptr->i_next;
   else       i += rb_ptr->i_oldest;
   i %= rb_ptr->N_size;
   if (i < 0) i += rb_ptr->N_size;
   /*printf("changed to offset: %d\n", i);*/
   return i;
}

int ringbuf_slice_i(ringbuf_t *rb_ptr, int i)
/* For slices, out of range indices get clipped.*/
/* This function is not needed for the pyrex interface. */
{
   /*printf("incoming index: %d", i);*/
   if (i >= rb_ptr->N_filled) i = rb_ptr->N_filled;
   if (i < -rb_ptr->N_filled) i = 0;
   if (i < 0) i += rb_ptr->i_next;
   else       i += rb_ptr->i_oldest;
   i %= rb_ptr->N_size;
   if (i < 0) i += rb_ptr->N_size;
   /*printf("changed to offset: %d\n", i);*/
   return i;
}

double ringbuf_getitem(ringbuf_t *rb_ptr, int i)
{
   i = ringbuf_index(rb_ptr, i);
   if (i < 0) return 1e38;
   return rb_ptr->data[i];
}


void resum_ringbuf(ringbuf_t *rb_ptr)
{
   int i;
   double d;
   rb_ptr->sum = 0.0;
   rb_ptr->sumsq = 0.0;
   for (i = 0; i < rb_ptr->N_filled; i++)
   {
      d = rb_ptr->data[i];
      if (!isnan(d))
      {
         rb_ptr->sum += d;
         rb_ptr->sumsq += d*d;
      }
   }
}

void ringbuf_add(ringbuf_t *rb_ptr, double d)
{

   double d_old;
   int i, i_new, good_new, N;

   N = rb_ptr->N_size; /* We need this many times. */
   i_new = rb_ptr->i_next;
   /* Save the old value; otherwise, it will be overwritten. */
   d_old = rb_ptr->data[rb_ptr->i_oldest];
   rb_ptr->data[i_new] = d;
   good_new = !isnan(d);
#if 1
   printf("new value: %lf  good_new: %d\n", d, good_new);
   printf("i_next: %d i_oldest: %d N_filled: %d N_good: %d\n",
            rb_ptr->i_next, rb_ptr->i_oldest,
            rb_ptr->N_filled, rb_ptr->N_good);
#endif
   rb_ptr->i_next++;
   rb_ptr->i_next %= N;

   if (rb_ptr->N_filled == rb_ptr->N_size) /* already full */
   {
      if (!isnan(d_old))
      {
         rb_ptr->sum -= d_old;
         rb_ptr->sumsq -= d_old * d_old;
         /* Remove the i_oldest entry from i_sorted,
            and slide the remaining entries down.
         */
         for (i = 0; i < rb_ptr->N_good; i++)
         {
            if (rb_ptr->i_sorted[i] == rb_ptr->i_oldest)
               break;
         }
         for ( ; i < rb_ptr->N_good - 1; i++)
         {
            rb_ptr->i_sorted[i] = rb_ptr->i_sorted[i+1];
         }
         rb_ptr->N_good--;
      }
      /* The new entry is temporarily put at the end of the array.
      */
      if (good_new)
      {
         rb_ptr->i_sorted[rb_ptr->N_good] = i_new;
         rb_ptr->N_good++;
      }
      rb_ptr->i_oldest++;
      rb_ptr->i_oldest %= N;
   }
   else  /* not full before adding this element */
   {
      if (good_new)
      {
         rb_ptr->i_sorted[rb_ptr->N_good] = i_new;
         rb_ptr->N_good++;
      }
      rb_ptr->N_filled++;
   }
   if (good_new)
   {
      rb_ptr->sum += d;
      rb_ptr->sumsq += d*d;
      sort_ringbuf(rb_ptr);
   }
   /* To prevent accumulation of truncation error, we
      recalculate the sums periodically.
   */
   rb_ptr->N_added++;
   if (rb_ptr->N_added % (rb_ptr->N_size + 10000) == 0)
   {
      resum_ringbuf(rb_ptr);
   }
#if 1
   printf("i_next: %d i_oldest: %d N_filled: %d N_good: %d\n",
            rb_ptr->i_next, rb_ptr->i_oldest,
            rb_ptr->N_filled, rb_ptr->N_good);
#endif
}

/* This is not a full sort--it assumes the list is
   already sorted except for the last entry.  It uses a single
   pass of bubble sorting to put that entry in its place.
   The code could be moved bodily into the function above.
*/
void sort_ringbuf(ringbuf_t *rb_ptr)
{
   int i, i_hold;
   int *ip;
   double *dp;

   ip = rb_ptr->i_sorted;
   dp = rb_ptr->data;

   for (i = rb_ptr->N_good - 1; i > 0; i--)
   {
      if (dp[ip[i]] < dp[ip[i-1]])
      {
         i_hold = ip[i];
         ip[i] = ip[i-1];
         ip[i-1] = i_hold;
      }
      else
      {
         break;
      }
   }
}

double ringbuf_min(ringbuf_t *rb_ptr)
{
  if (rb_ptr->N_good==0)
    return NaN;
   return rb_ptr->data[rb_ptr->i_sorted[0]];
}

double ringbuf_max(ringbuf_t *rb_ptr)
{

  int i_end;

  if (rb_ptr->N_good==0)
    return NaN;

   i_end = rb_ptr->N_good - 1;

   return rb_ptr->data[rb_ptr->i_sorted[i_end]];
}

double ringbuf_median(ringbuf_t *rb_ptr)
{
   int i_mid, N;
   N = rb_ptr->N_good;
   if (N == 0) return NaN;
   i_mid = N/2;
   if (N % 2 == 1)
   {
      return rb_ptr->data[rb_ptr->i_sorted[i_mid]];
   }
   else
   {
      return 0.5 * (rb_ptr->data[rb_ptr->i_sorted[i_mid]]
                     + rb_ptr->data[rb_ptr->i_sorted[i_mid - 1]]);
   }
}

double ringbuf_ptile(ringbuf_t *rb_ptr, double ptile)
{
   int i, N;

   N = rb_ptr->N_good;
   if (N == 0) return NaN;
   i = (int)(ptile*N);
   return rb_ptr->data[rb_ptr->i_sorted[i]];
}

int ringbuf_N_good(ringbuf_t *rb_ptr)
{
   return rb_ptr->N_good;
}


int ringbuf_N_filled(ringbuf_t *rb_ptr)
{
   return rb_ptr->N_filled;
}



int ringbuf_N_added(ringbuf_t *rb_ptr)
{
   return rb_ptr->N_added;
}



double ringbuf_mean(ringbuf_t *rb_ptr)
{
   int N;


   N = rb_ptr->N_good;
   if (N > 0)
   {
      return rb_ptr->sum / N;
   }
   else
   {
      return NaN;
   }
}

double ringbuf_sd(ringbuf_t *rb_ptr)
{
   double m, s;

   int N;

   N = rb_ptr->N_good;
   if (N == 0)
      return NaN;
   m = ringbuf_mean(rb_ptr);
   s = rb_ptr->sumsq / N - m*m;
   if (s > 0.0)
   {
      return sqrt(s);
   }
   else
   {
      return 0.0;
   }
}

void c_runstats(int nrb, int nd, double *data, double *dmean, double *dstd,
                double *dmin, double *dmax, double *dmed, double *dptile5, double *dptile95, int *ng)
{
    int i, j;
    ringbuf_t *rb_ptr;

    rb_ptr = new_ringbuf(nrb);

    for (j=0; j<nd; i++, j++)
      {
	ringbuf_add(rb_ptr, data[j]);
        dmean[j] = ringbuf_mean(rb_ptr);
        dstd[j] = ringbuf_sd(rb_ptr);
        dmin[j] = ringbuf_min(rb_ptr);
        dmax[j] = ringbuf_max(rb_ptr);
        dmed[j] = ringbuf_median(rb_ptr);
        dptile5[j] = ringbuf_ptile(rb_ptr, 0.05);
        dptile95[j] = ringbuf_ptile(rb_ptr, 0.95);
        ng[j] = rb_ptr->N_good;
    }
    delete_ringbuf(rb_ptr);
}


void c_runstats2(int nrb, int nd, int step, int ofs,
                 double *data, double *dmean, double *dstd,
                 double *dmin, double *dmax, double *dmed, double
*dptile5, double *dptile95, int *ng)
{
    int i, j;
    int npad = (nrb - 1) / 2;
    ringbuf_t *rb_ptr;

    data += ofs;
    dmean += ofs;
    dstd += ofs;
    dmin += ofs;
    dmax += ofs;
    dmed += ofs;
    dptile5 += ofs;
    dptile95 += ofs;
    ng += ofs;

    rb_ptr = new_ringbuf(nrb);
    for (i = 0; i < npad; i++)
    {
        ringbuf_add(rb_ptr, data[i*step]);
    }
    for (j=0; j<nd; i++, j++)
    {
        if (i < nd) {ringbuf_add(rb_ptr, data[i*step]);}
        else        {ringbuf_add(rb_ptr, NaN);}
        dmean[j*step] = ringbuf_mean(rb_ptr);
        dstd[j*step] = ringbuf_sd(rb_ptr);
        dmin[j*step] = ringbuf_min(rb_ptr);
        dmax[j*step] = ringbuf_max(rb_ptr);
        dmed[j*step] = ringbuf_median(rb_ptr);
        dptile5[j*step] = ringbuf_ptile(rb_ptr, 0.05);
        dptile95[j*step] = ringbuf_ptile(rb_ptr, 0.95);
        ng[j*step] = rb_ptr->N_good;
    }
    delete_ringbuf(rb_ptr);
}


