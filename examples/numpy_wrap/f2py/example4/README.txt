==================================================
 Very simple Fortran 90 wrapping example via f2py
==================================================

This small, self-contained directory shows how to build an extension for Python
based on Fortran 90 code.  You can do it both by directly calling f2py and via
a small setup.py file.

See the accompanying makefile for the actual targets provided, but if you are
impatient and have gfortran installed, simply type::

    make test

which should run the build and a simple test.  If no errors are printed at the
end, you're fine.  If you have nose installed (highly recommended and needed to
test numpy and scipy, see
http://www.somethingaboutorange.com/mrl/projects/nose/) you can try instead::

    make nose

This will run the same test files but as proper tests, indicating number of
tests, errors/failures, etc.  There is currently only one test provided, but
using this in your projects will get you going with proper testing practices
from the start.
