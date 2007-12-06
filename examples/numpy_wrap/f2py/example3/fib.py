def fib1(i):
    """Standard recursive Fibonacci."""
    if i < 2:
	return i
    else:
	return fib1(i-1)+fib1(i-2)

def fib2(i, current = 0, next = 1):
    """Fibonacci using tail call."""
    if i == 0:
	return current
    else:
	return fib2(i - 1, next, current + next)

print "First fibo..."
print fib1(30)
print "Second fibo..."
print fib2(30)
