"""Simple image recognition library - SVD based.

Ben Herbst - U. Stellenbosch.
Fernando Perez - U. Colorado, Boulder."""

# Required packages

# Std lib
import os

# Third-party
from scipy import linalg

import pylab as P
import numpy as N
import scipy as S

from imtools import ImageCollection, imshow2

# Functions for actual facial recognition
def plot_sigma(sigma):
    """Plot the singular values, normalized by the first"""

    P.figure()
    P.plot(sigma/sigma[0])
    P.title('Normalized singular values')
    P.grid()
    P.draw_if_interactive()

def plot_eigenfaces(eig_img,n=10):
    """Display the first n eigenfaces."""

    P.figure()
    for i in range(n):
        P.subplot(n/5 + n%5,5,i+1)
        P.imshow(eig_img[i], P.cm.gray)
        P.title('Face %d' % (i+1))
        P.xticks([],[])
        P.yticks([],[])

def verify(test_img,key):
    """Verify visually that a provided image corresponds to a specified image
    in the training set.

    Two images, the provided test image and the training image 'key', are
    displayed side-by-side, along with the l2-norm error.  Based on this
    information, the user can visually verify that they are the same."""

    ref_coeffs = proj_c[key]
    norm_test = test_img.flat - data_mean
    test_coeffs = N.dot(utt,norm_test)
    l2_err = N.linalg.norm(test_coeffs-ref_coeffs,2)
    imshow2(imtrain[key],test_img,
            labels = ('Reference Image','Test Image'))        
    P.title('L2 coefficient error: %.2e' % l2_err)

def identify(test_img):
    """Try to find a match for test_img from the training set."""

    # Normalise data, compute projections into eigenspace
    norm_test = test_img.flat - data_mean
    test_coeffs = N.dot(utt,norm_test)

    # Find closest match
    diff2 = ((proj_c - test_coeffs)**2).sum(axis=1)
    minidx = diff2.argmin()
    best_err = diff2[minidx]

    # Display the matching face
    imshow2(test_img,imtrain.images[minidx],
            labels = ('Test Image','Best Match: %d' % minidx))
    P.title('L2 coefficient error: %.2e' % best_err)

def decompose(face, a=[1,5,10,20]):
    """Show how a face is decomposed using eigenfaces.

    The image is reconstructed using n eigenfaces, for each n in a."""

    norm_face = face.flat - data_mean
    test_coeffs = N.dot(utt,norm_face)

    P.figure()

    eig_composition = N.zeros(im_shape,eig_img[0].dtype)
    for (fig_cnt, n) in enumerate([0] + a + [imtrain.num_images-1]):
        P.subplot(1, len(a)+3, fig_cnt+1)
        P.title('%d faces' % n)
        P.xticks([],[])
        P.yticks([],[])

        if fig_cnt != 0:
            for i in range(n):
                # Add the weighted eigenfaces to form the face
                eig_composition += test_coeffs[i]*eig_img[i]

            # Add back the data mean (subtracted before composition)
            eig_composition += data_mean.reshape(im_shape)
            
            P.imshow(eig_composition, P.cm.gray)
        else:
            P.imshow(face, P.cm.gray)
            P.title('Original image')
            
# 'main' script

# Load the training images from directory 'data_train/'
imtrain = ImageCollection.from_directory('data_train/')

# Compute the data mean and normalise
data_mean = imtrain.flat().mean(axis=1)
img_flat_norm = imtrain.flat() - data_mean[:,N.newaxis]

# Compute singular values and U matrix
umat,sigma,vtmat = N.linalg.svd(img_flat_norm,0)

# Create an array of 'eigenfaces' in normal (not flattened) format
im_shape = imtrain.im_shape

eig_img = N.empty((imtrain.num_images,im_shape[0],im_shape[1]),umat.dtype)
for i in range(imtrain.num_images):
    eig_img[i] = N.reshape(umat[:,i],im_shape)

eig_img = ImageCollection(eig_img)
plot_eigenfaces(eig_img)

# Truncation index.
# Indicates the number of eigenfaces used for comparison.
# This is typically read from the singular value plot, it should be an
# integer in the range of the number of images in the collection
# (.num_images).
#
# By default we don't truncate.
truncate_idx = imtrain.num_images-1
umat_trunc = umat[:,:truncate_idx]

# compute projection coefficients for all the original input (but
# normalized) images against the eigenimages.
utt = umat_trunc.transpose().astype(N.float32)
proj_c = N.empty((imtrain.num_images,truncate_idx),N.float32)
for j in range(imtrain.num_images):
    proj_c[j] = N.dot(utt,img_flat_norm[:,j])

# Test the classifier
imtest = ImageCollection.from_directory('data_test/')
verify(imtrain[17], 17)
verify(imtest[20], 17)

identify(imtest[0])
identify(imtest[20])
identify(imtest[21])

decompose(imtrain[0])

P.show()
