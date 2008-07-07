#!/usr/bin/env python
"""Image denoising example using 2-dimensional FFT."""

import sys

import numpy as np
from matplotlib import pyplot as plt

def mag_phase(F):
    """Return magnitude and phase components of spectrum F."""

    return (np.absolute(F), np.angle(F))

def plot_spectrum(F, amplify=1000):
    """Normalise, amplify and plot an amplitude spectrum."""
    M, Phase = mag_phase(F)
    M *= amplify/M.max()
    M[M > 1] = 1

    print M.shape, M.dtype
    plt.imshow(M, plt.cm.Blues)

try:
    # Read in original image, convert to floating point for further
    # manipulation; imread returns a MxNx4 RGBA image.  Since the
    # image is grayscale, just extrac the 1st channel
    im = plt.imread('data/moonlanding.png').astype(float)[:,:,0]
except:
    print "Could not open image."
    sys.exit(-1)

# Compute the 2d FFT of the input image
F = np.fft.fft2(im)

# Now, make a copy of the original spectrum and truncate coefficients.
keep_fraction = 0.1

# Call ff a copy of the original transform.  Numpy arrays have a copy method
# for this purpose.
ff = F.copy()

# Set r and c to be the number of rows and columns of the array.  
r,c = ff.shape

# Set to zero all rows with indices between r*keep_fraction and
# r*(1-keep_fraction):
ff[r*keep_fraction:r*(1-keep_fraction)] = 0

# Similarly with the columns:
ff[:, c*keep_fraction:c*(1-keep_fraction)] = 0

# Reconstruct the denoised image from the filtered spectrum, keep only the real
# part for display
im_new = np.fft.ifft2(ff).real

# Show the results
plt.figure()

plt.subplot(221)
plt.title('Original image')
plt.imshow(im, plt.cm.gray)

plt.subplot(222)
plt.title('Fourier transform')
plot_spectrum(F)

plt.subplot(224)
plt.title('Filtered Spectrum')
plot_spectrum(ff)

plt.subplot(223)
plt.title('Reconstructed Image')
plt.imshow(im_new, plt.cm.gray)

plt.savefig('fft_imdenoise.png', dpi=150)
plt.savefig('fft_imdenoise.eps')
plt.show()
