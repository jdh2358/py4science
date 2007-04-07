clean:
	rm -f fib.pyf example.so

fib.pyf: fib.f
	rm -f fib.pyf
	f2py fib.f -h fib.pyf -m example

example: fib.pyf
	f2py -c fib.pyf fib.f


