"""Some simple examples of weave.inline use"""

from weave import inline,converters
import Numeric as nx
from pylab import rand

#-----------------------------------------------------------------------------
# Returning a scalar quantity computed from a Numeric array.
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

def main():
    zz = nx.zeros([10,10])
    print 'tr(zz)=',trace(zz)
    oo = nx.ones([4,4],nx.Float)
    print 'tr(oo)=',trace(oo)
    aa = rand(128,128)
    print 'tr(aa)=',trace(aa)
    print 'oo:',oo
    in_place_mult(3,oo)
    print '3*oo:',oo

if __name__=='__main__':
    main()
