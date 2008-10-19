#!/usr/bin/env python
"""Minimal test script to check for modules needed in python workshop.

Execute this code at the command line by typing:

python workshop_checklist.py

If it does NOT say 'OK' at the end, copy the *entire* output of the run and
send it to the course instructor for help.
"""

# Standard library imports
import glob
import os
import platform
import sys

from StringIO import StringIO

# Third-party imports
import nose
import nose.tools as nt

##############################################################################
# Code begins

#-----------------------------------------------------------------------------
# Generic utility functions
def sys_info():
    """Summarize some info about the system"""

    print '=================='
    print 'System information'
    print '=================='
    print 'os.name      :',os.name
    print 'os.uname     :',os.uname()
    print 'platform     :',sys.platform
    print 'platform+    :',platform.platform()
    print 'prefix       :',sys.prefix
    print 'exec_prefix  :',sys.exec_prefix
    print 'executable   :',sys.executable
    print 'version_info :',sys.version_info
    print 'version      :',sys.version
    print '=================='


#-----------------------------------------------------------------------------
# Tests

def check_import(mname):
    "Check that the given name imports correctly"
    exec "import %s as m" % mname

    if mname == 'matplotlib':
        m.use('Agg')
        m.rcParams['figure.subplot.top']= 0.85
    
    try:
        vinfo = m.__version__
    except AttributeError:
        vinfo = '*no info*'

    print 'MOD: %s, version: %s' % (mname,vinfo)


# Test generators are best written without docstrings, because nose can then
# show the parameters being used.
def test_imports():
    modules = ['setuptools',
               'IPython',
               'numpy','scipy','scipy.weave','scipy.io',
               'matplotlib','pylab',
               'nose',
               #'Cython',  # disabled for now, not included in EPD Beta2
               ]

    for mname in modules:
        yield check_import,mname


def test_weave():
    "Simple code compilation and execution via scipy's weave"
    from scipy import weave

    weave.inline('int x=1;x++;')
    
    n,m=1,2
    code="""
    int m=%s;
    return_val=m+n;
    """ % m
    val = weave.inline(code,['n'])
    nt.assert_equal(val,m+n)


def est_numpy_all():
    "Run the entire numpy test suite"
    import numpy
    numpy.test()


# Test generator, don't put a docstring in it
def test_loadtxt():
    import numpy as np
    import numpy.testing as npt

    # Examples taken from the loadtxt docstring
    array = np.array
    
    c = StringIO("0 1\n2 3")
    a1 = np.loadtxt(c)
    a2 = np.array([[ 0.,  1.],
                   [ 2.,  3.]])
    yield npt.assert_array_equal,a1,a2

    d = StringIO("M 21 72\nF 35 58")
    a1 = np.loadtxt(d, dtype={'names': ('gender', 'age', 'weight'),
                         'formats': ('S1', 'i4', 'f4')})
    
    a2 = np.array([('M', 21, 72.0), ('F', 35, 58.0)],
                  dtype=[('gender', '|S1'), ('age', '<i4'), ('weight', '<f4')])
    yield npt.assert_array_equal,a1,a2

    c = StringIO("1,0,2\n3,0,4")
    x,y = np.loadtxt(c, delimiter=',', usecols=(0,2), unpack=True)
    yield npt.assert_array_equal,x,np.array([ 1.,  3.])
    yield npt.assert_array_equal,y,np.array([ 2.,  4.])


def test_plot():
    "Simple plot generation."
    from matplotlib import pyplot as plt
    plt.figure()
    plt.plot([1,2,3])
    plt.xlabel('some numbers')
    plt.savefig('tmp_test_plot.png')


def test_plot_math():
    "Plots with math"
    from matplotlib import pyplot as plt
    plt.figure()
    plt.plot([1,2,3],label='data')
    t=(r'And X is $\sum_{i=0}^\infty \gamma_i + \frac{\alpha^{i^2}}{\gamma}'
       r'+ \cos(2 \theta^2)$')
    plt.title(t)
    plt.legend()
    plt.grid()
    plt.savefig('tmp_test_plot_math.png')


def cleanup_pngs():
    """Remove temporary pngs made by our plotting tests"""

    for f in glob.glob('tmp_test_*.png'):
        try:
            os.remove(f)
        except OSError:
            print '*** Error: could not remove file',f
            

#-----------------------------------------------------------------------------
# Main routine, executed when this file is run as a script
#
if __name__ == '__main__':
    print "Running tests:"
    # This call form is ipython-friendly
    nose.runmodule(argv=[__file__,'-vvs'],
                   exit=False)
    print """
***************************************************************************
                           TESTS FINISHED
***************************************************************************

If the printout above did not finish in 'OK' but instead says 'FAILED', copy
and send the *entire* output to the instructor for help.
"""
    sys_info()
