#!/usr/bin/env python
"""Some simple examples of weave.inline use"""

import numpy as np
from scipy.weave import inline,converters

#-----------------------------------------------------------------------------
# Returning a scalar quantity computed from an array.
def trace(mat):
    """Return the trace of a matrix.
    """
    nrow,ncol = mat.shape
    code = \
""" 
double tr=0.0;

for(int i=0;i<nrow;++i)
    tr += mat(i,i);
return_val = tr;
"""
    return inline(code,['mat','nrow','ncol'],
                  type_converters = converters.blitz)

# In-place operations on arrays in general work without any problems
def in_place_mult(num,mat):
    """In-place multiplication of a matrix by a scalar.
    """
    nrow,ncol = mat.shape
    code = \
"""
for(int i=0;i<nrow;++i)
    for(int j=0;j<ncol;++j)
	mat(i,j) *= num;

"""
    inline(code,['num','mat','nrow','ncol'],
           type_converters = converters.blitz)

def prod(m, v):
    #C++ version
    nrows, ncolumns = m.shape
    assert v.ndim==1 and ncolumns==v.shape[0],"Shape mismatch in prod"
    
    res = np.zeros(nrows, float)
    code = r"""
    for (int i=0; i<nrows; i++)
    {
        for (int j=0; j<ncolumns; j++)
        {
            res(i) += m(i,j)*v(j);
        }
    }
    """
    err = inline(code,['nrows', 'ncolumns', 'res', 'm', 'v'], verbose=2,
                 type_converters=converters.blitz)
    return res


if __name__=='__main__':
    print 'zz is all zeros'
    zz = np.zeros([10,10])
    print 'tr(zz)=',trace(zz)
    print 'oo is all ones'
    oo = np.ones([4,4],float)
    print 'tr(oo)=',trace(oo)
    print 'aa is random'
    aa = np.random.rand(128,128)
    print 'tr(aa)=',trace(aa)
    print 'tr(aa)=',np.trace(aa),' (via numpy)'

    print
    print 'Modify oo in place:'
    print 'oo:',oo
    in_place_mult(3,oo)
    print '3*oo:',oo

    print
    print 'Simple matrix-vector multiply'
    nr,nc = 20,10
    m = np.random.rand(nr,nc)
    v = np.random.rand(nc)
    mv = prod(m,v)
    mvd = np.dot(m,v)
    print 'Mat*vec error:',np.linalg.norm(mv-mvd)
