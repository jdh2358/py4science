#!/usr/bin/env python
"""Setup script for f2py-wrapped library.
"""

# Third-party modules
from numpy.distutils.core import setup
from numpy.distutils.extension import Extension

# Build the extension module object
extmod = Extension( name = 'simple',
                    # List here the interface (.pyf) file, plus any sources
                    # that need to be explicitly compiled into the wrapped
                    # module (i.e., not already part of one of the fortran
                    # libraries listed below):
                    sources = ['simple.pyf',
                               'simple.f90'
                               ],

                    # Additional libraries required by our extension modules
                    libraries = [],

                    # Add '--debug-capi' for verbose debugging of low-level
                    # calls
                    #f2py_options = ['--debug-capi'],
                    )

# Make the actual distutils setup call
setup(name        = 'simple',  # name of the generated extension (.so)
      description = 'Segmentation library',
      author      = 'Felipe Arrate',
      ext_modules = [extmod],
      )
