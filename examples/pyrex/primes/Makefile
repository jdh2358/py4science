all:
	python setup.py build_ext --inplace

test:	all
	python run_primes.py 20

clean:
	@echo Cleaning Primes
	@rm -f *.c *.o *.so *~ *.pyc
	@rm -rf build

