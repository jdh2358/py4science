
F2PY=f2py

#F2PY=/usr/local/txpython/local/Frameworks/Python.framework/Versions/2.5/bin/f2py

clean:
	rm -f fib.pyf example.so

fib.pyf: fib.f
	rm -f fib.pyf
	$(F2PY) fib.f -h fib.pyf -m example

example: fib.pyf
	$(F2PY) -c fib.pyf fib.f


