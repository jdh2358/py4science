from __future__ import division

from math import pi

def WallisPi(n,longform=False):
    """Compute pi using n terms of Wallis' product.
    
    If longform is true, the result is returned as a long integer of the
    form 314..."""
    
    num = 1L
    den = 1L
    for i in xrange(1,n+1):
	tmp = 4*i*i
	num *= tmp
	den *= tmp-1
    if longform:
	order = len(str(num))+1
	return long(10**order)*2*num//den
    else:
	return 2.0*(num/den)
