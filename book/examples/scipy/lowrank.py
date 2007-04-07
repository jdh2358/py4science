"""Low-rank approximations for images"""

import scipy as S
import pylab as P
from scipy.plt import lena

# Set grayscale colormap
P.gray()

# load lena into array
lena = lena()
U,s,Vh = S.linalg.svd(lena)
P.plot(s)
P.show()
