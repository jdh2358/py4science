#!/usr/bin/env python
"""Simple weave.blitz examples."""

import numpy as N
import scipy as S
from scipy import weave

a = N.arange(10)
x = N.empty_like(a)
weave.blitz('x=a+2*a*a')
print x
print x-(a+2*a*a)
