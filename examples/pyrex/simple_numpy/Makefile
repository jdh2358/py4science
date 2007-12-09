all:
	python setup.py build_ext --inplace

test:   all
	python sums_test.py

.PHONY: clean
clean:
	rm -rf *~ *.so *.c *.o build
