#!/usr/bin/env python
from distutils.core import setup
from distutils.extension import Extension

# Make this usable by people who don't have pyrex installed (I've committed
# the generated C sources to SVN).
try:
    from Pyrex.Distutils import build_ext
    has_pyrex = True
except ImportError:
    has_pyrex = False

import numpy

# Define a pyrex-based extension module, using the generated sources if pyrex
# is not available.


ringbufmod = Extension('ringbuf',
                        ['ringbuf.pyx',
                         'ringbufnan.c'],
                       include_dirs = [numpy.get_include()])

# Call the routine which does the real work
setup(name        = 'ringbuf',
      description = 'trailing stats using a c ring buffer',
      ext_modules = [ringbufmod,],
      cmdclass    = {'build_ext': build_ext},
      )
