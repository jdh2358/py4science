import example
import numpy

print example.fib(12)

x = numpy.arange(10.)

yf = example.cumsum(x)
yn = numpy.cumsum(x)

numpy.testing.assert_array_almost_equal(yf, yn)
