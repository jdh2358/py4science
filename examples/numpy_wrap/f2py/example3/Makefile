
#F2PY=f2py

F2PY=f2py2.4

#F2PY=/usr/local/txpython/local/Frameworks/Python.framework/Versions/2.5/bin/f2py

clean:
	rm -f fib3.pyf example.so

fib3.pyf: fib3.f
	rm -f fib3.pyf
	$(F2PY) fib3.f -h fib3.pyf -m example

example: fib3.pyf
	$(F2PY) -c fib3.pyf fib3.f


