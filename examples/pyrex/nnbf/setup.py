
from distutils.core import setup

import os
from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
import numpy


nnbf = Extension('nnbf',
                 ['nnbf.pyx'],
                 include_dirs = [numpy.get_include()])

packages = [
    'nnbf'
    ]


setup ( name = "nnbf",
        version = "0.0000",
        description = "incremental nearest neighbor brute force",
        author = "John Hunter",
        author_email = "jdh2358@gmail.com",
        packages = packages,
        ext_modules = [nnbf],
        cmdclass    = {'build_ext': build_ext},

        )
