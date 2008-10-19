import numpy as np
from scipy.weave import inline
from numpy.testing import assert_array_almost_equal, assert_almost_equal

def prodsum(a, b, axis=None):
    assert a.shape == b.shape, "cannot take prodsum of different size arrays"
    nd = len(a.shape)
    if axis is not None:
        caxis = axis if axis >=0 else nd + axis
        assert caxis < nd, "cannot perform operation in this axis: %d"%axis  
        dims = list(a.shape)
        dims.pop(axis)
        c = np.zeros(tuple(dims), np.float64)
    else:
        caxis = -1
        c = np.array([0.0])
    
    xtra = \
"""
double prodsum(double *d1, double *d2, int stride, int size)
{
  double sum = 0.0;

  while(size--) {
    sum += (*d1) * (*d2);
    d1 += stride;
    d2 += stride;
  }
  return sum;
}
"""
  
    code = \
"""
double *d1, *d2, *d3;
int sumall = caxis < 0 ? 1 : 0;
PyArrayIterObject *itr1, *itr2, *itr3;

itr1 = (PyArrayIterObject *) PyArray_IterAllButAxis(py_a, &caxis);
itr2 = (PyArrayIterObject *) PyArray_IterAllButAxis(py_b, &caxis);
if (!sumall) itr3 = (PyArrayIterObject *) PyArray_IterNew(py_c);

//...... more definitions here

// make use of auto defined arrays, be careful to use "axis" AFTER
// creating iterators, in case it gets chosen for you
int stride = Sa[caxis]/sizeof(double);
int size = Na[caxis];
while( PyArray_ITER_NOTDONE(itr1) ) {

  //...... iter loop here
  d1 = (double *) itr1->dataptr;
  d2 = (double *) itr2->dataptr;
  if(sumall) {
    d3 = c;
  } else {
    d3 = (double *) itr3->dataptr;
    PyArray_ITER_NEXT(itr3);
  }
  *d3 += prodsum(d1, d2, stride, size);
  PyArray_ITER_NEXT(itr1);
  PyArray_ITER_NEXT(itr2);
}
"""
    inline(code, ['a', 'b', 'c', 'caxis'], compiler='gcc',
           support_code=xtra)
    return c[0] if axis is None else c


def tests():
    a = np.random.rand(4,2,9)
    b = np.ones_like(a)
    
    assert_almost_equal(prodsum(a,b), a.sum())
    assert_array_almost_equal(prodsum(a,b,axis=-1), a.sum(axis=-1))
    assert_array_almost_equal(prodsum(a[:2,:,1::2], b[:2,:,1::2], axis=0),
                              a[:2,:,1::2].sum(axis=0))
    assert_array_almost_equal(prodsum(a[:,:,::-1], b[:,:,::-1], axis=-1),
                              a[:,:,::-1].sum(axis=-1))

if __name__ == '__main__':
    tests()
