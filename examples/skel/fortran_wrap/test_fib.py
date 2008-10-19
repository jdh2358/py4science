import numpy as N

import example

n = 10
fn = example.fib(n)

print 'Fibonacci numbers:'
print fn

# Check validity
assert N.alltrue(fn[2:]== fn[1:-1]+fn[:-2]), "Fibonacci mismatch"

