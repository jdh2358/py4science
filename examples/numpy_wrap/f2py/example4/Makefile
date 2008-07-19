# Python wrappers for a simple Fortran 90 library

# Build the actual library using a standard Python  setup.py script
build: simple.so

simple.so: simple.f90 simple.pyf setup.py
	./setup.py config_fc build_ext --inplace

# Build the library in place via a direct call to f2py, using the manually
# modified simple.pyf file.
libpyf: simple.f90 simple.pyf
	f2py -c --fcompiler=gnu95 simple.pyf simple.f90

# Build the 'raw' library by hand, without any tweaks to the python interface
# of any function.  Note that this will NOT pass the tests, since the tests
# expect the modified interface.
libraw: simple.f90
	f2py -c --fcompiler=gnu95 -m simple simple.f90

# Run a very simple test.
test: build
	python test_simple.py

# If you have nose installed, the test above can be run as a proper unittest.
nose: build
	nosetests test_simple.py

# Build the .pyf file.  Note that the supplied file simple.pyf has been
# manually modified from the auto-generated one.  It's a good idea to
# auto-generate one with a different name if you intend to manually edit yours
# later, to help prevent an accidental clobbering.
pyf: simple.f90
	f2py -h simple_auto.pyf -m simple simple.f90

clean:
	rm -rf *~ *module.c *.pyc *-f2pywrappers*.f90  build

cleanall: clean
	rm -rf *.so
