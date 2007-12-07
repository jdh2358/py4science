all:
	python setup.py build_ext --inplace

test:   all
	python movavg_test.py

.PHONY: clean
clean:
	rm -rf *~ *.so *.o build ringbuf.c
