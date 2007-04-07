#!/usr/bin/env python
"""Simple generation of pi via MonteCarlo integration"""

import random
import math
from scipy import weave

def v1(n = 100000):
    rand = random.random
    sqrt = math.sqrt
    sm   = 0.0
    for i in xrange(n):
        sm += sqrt(1.0-rand()**2)
    return 4.0*sm/n

def v2(n = 100000):
    """Implement v1 above using weave for the C call"""
    
    support = "#include <stdlib.h>"
    
    code = """
    double sm;
    float rnd;
    srand(1); // seed random number generator
    sm = 0.0;
    for(int i=0;i<n;++i) {
        rnd = rand()/(RAND_MAX+1.0);
        sm += sqrt(1.0-rnd*rnd);
    }
    return_val =  4.0*sm/n;"""
    return weave.inline(code,('n'),support_code=support)

print 'pi - python:',v1()
print 'pi - weave :',v2()
