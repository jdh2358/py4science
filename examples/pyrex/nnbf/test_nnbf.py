import time
import numpy as np
import nose, nose.tools as nt
import numpy.testing as nptest


from nnbf_proto import find_neighbors_numpy
# the pure python prototype


#import nnbf_proto as nnbf

# the cython extension
import nnbf



def jdh_add_data():
    nn = nnbf.NNBF(6)

    for i in range(202):
        x = np.random.rand(6)
        nn.add(x)
        data = nn.get_data()
        nptest.assert_equal((x==data[-1]).all(), True)
        nptest.assert_equal(len(data), i+1)

def test_neighbors():
    NUMDIM = 4
    nn = nnbf.NNBF(NUMDIM)

    for i in range(2000):
        x = np.random.rand(NUMDIM)
        nn.add(x)

    radius = 0.2
    x = np.random.rand(NUMDIM)
    ind = nn.find_neighbors(x, radius)
    data = nn.get_data()

    indnumpy = find_neighbors_numpy(data, x, radius)

    nptest.assert_equal((ind==indnumpy), True)



if 1:
#def test_performance():
    NUMDIM = 6
    nn = nnbf.NNBF(NUMDIM)

    print 'loading data... this could take a while'
    # this could take a while
    for i in range(200000):
        x = np.random.rand(NUMDIM)
        nn.add(x)

    x = np.random.rand(NUMDIM)
    radius = 0.2
    data = nn.get_data()

    print 'testing nnbf...'
    times = np.zeros(10)
    for i in range(len(times)): 
        start = time.clock()
        ind = nn.find_neighbors(x, radius)
        end = time.clock()
        times[i] = end-start
    print '    10 trials: mean=%1.4f, min=%1.4f'%(times.mean(), times.min())

    print 'testing numpy...'
    for i in range(len(times)):     
        start = time.clock()
        ind = find_neighbors_numpy(data, x, radius)
        end = time.clock() 
        times[i] = end-start
    print '    10 trials: mean=%1.4f, min=%1.4f'%(times.mean(), times.min())        





if __name__=='__main__':

    #nose.runmodule(argv=['-s','--with-doctest'], exit=False)
    pass

