"""Simple image recognition library - SVD based.

Ben Herbst - U. Stellenbosch.
Stefan van der Walt - U. Stellenbosch.
Fernando Perez - U. Colorado, Boulder."""

# Required packages

# Std lib
import os

# Third-party
import pylab as P
import numpy as N
import scipy as S

import scipy.linalg


from imtools import ImageCollection, imshow2

# Functions for actual facial recognition
class FaceClassifier(object):
    """Class to represent a collection of training images"""

    def __init__(self,dir_name,verbose=False):
        """Load a collection of images from a directory"""

        self.image_coll = ImageCollection.from_directory(dir_name,
                                                         verbose=verbose)
        self.num_images = self.image_coll.num_images
        iflat = self.image_coll.flat()
        data_mean = iflat.mean(axis=1)
        img_flat_norm = iflat - data_mean[:,N.newaxis]

        # Compute singular values and U matrix
        umat,sigma,vtmat = N.linalg.svd(img_flat_norm,0)

        # Array of 'eigenimages' in normal (not flattened) format
        im_shape = self.image_coll.images[0].shape
        eig_img = N.empty((self.num_images,im_shape[0],im_shape[1]),umat.dtype)
        for i in range(self.num_images):
            eig_img[i] = N.reshape(umat[:,i],im_shape)

        # Store in object all these
        self.sigma = sigma
        self.umat = umat
        self.vtmat = vtmat
        self.im_shape = im_shape
        self.eig_img = ImageCollection(eig_img)
        self.img_flat_norm = img_flat_norm
        self.data_mean = data_mean

        # Truncation index, by default we don't truncate
        self.truncate_idx = self.num_images-1
            
    def plot_sigma(self):
        """Plot the singular values, normalized by the first"""

        P.figure()
        P.plot(self.sigma/self.sigma[0])
        P.title('Normalized singular values')
        P.grid()
        P.draw_if_interactive()

    def _set_truncate_idx(self,idx):
        """Set the truncation index as an integer.

        This is typically read from the singular value plot, it should be an
        integer in the range of the number of images in the collection
        (.num_images)."""

        if idx<0 or idx>=self.num_images:
            raise ValueError('index must be >0 and <%d' % self.num_images)
        
        self._trunc_idx = idx
        self.umat_trunc = self.umat[:,:self._trunc_idx]

        # compute projection coefficients for all the original input (but
        # normalized) images against the eigenimages.
        utt = self.utt = self.umat_trunc.transpose().astype(N.float32)
        proj_c = N.empty((self.num_images,idx),N.float32)
        for j in range(self.num_images):
            proj_c[j] = N.dot(utt,self.img_flat_norm[:,j])
        self.proj_c = proj_c

    truncate_idx = property(lambda x: self._trunc_idx,
                            _set_truncate_idx,
                            None,
                            _set_truncate_idx.__doc__)

    def verify(self,test_img,key):
        """Verify visually that a provided image corresponds to a specified
        image in the training set.
        
        Two images, the provided test image and the training image 'key', are
        displayed side-by-side, along with the l2-norm error.  Based on this
        information, the user can visually verify that they are the same."""
        
        ref_coeffs = self.proj_c[key]
        norm_test = test_img.flat - self.data_mean
        test_coeffs = N.dot(self.utt,norm_test)
        l2_err = N.linalg.norm(test_coeffs-ref_coeffs,2)
        imshow2(self.image_coll[key],test_img,
                labels = ('Reference Image','Test Image'))        
        P.title('L2 error: %.2e' % l2_err)

    def plot_eigenfaces(self, n=10):
        """Display the first n eigenfaces."""
        
        if self.umat is not None:
            P.figure()
            
            for i in range(n):
                P.subplot(n/5 + n%5,5,i+1)
                P.imshow(self.eig_img[i], P.cm.gray)
                P.title('Face %d' % (i+1))
                P.xticks([],[])
                P.yticks([],[])
                

    def identify(self,test_img):
        """Find the best match from the test set to the provided image."""
        
        norm_test = test_img.flat - self.data_mean
        test_coeffs = N.dot(self.utt,norm_test)
        diff2 = ((self.proj_c - test_coeffs)**2).sum(axis=1)
        minidx = diff2.argmin()
        best_err = diff2[minidx]
        imshow2(test_img,self.image_coll.images[minidx],
                labels = ('Test Image','Best Match: %d' % minidx))
        P.title('L2 error: %.2e' % best_err)

    def decompose(self,face, a=[1,5,10,20]):
        """Show how a face is decomposed using eigenfaces.

        The image is reconstructed using n eigenfaces, for each n in a."""

        eig_img =  self.eig_img
        data_mean = self.data_mean
        im_shape = self.im_shape

        norm_face = face.flat - data_mean
        test_coeffs = N.dot(self.utt,norm_face)

        P.figure()
        eig_composition = N.zeros(self.im_shape,eig_img[0].dtype)
        for (fig_cnt, n) in enumerate([0] + a + [self.num_images-1]):
            P.subplot(1, len(a)+3, fig_cnt+1)
            P.title('%d faces' % n)
            P.xticks([],[])
            P.yticks([],[])

            if fig_cnt != 0:
                for i in range(n):
                    # Add the weighted eigenfaces to form the face
                    try:
                        eig_composition += test_coeffs[i]*eig_img[i]
                    except IndexError:
                        print 'Image %d not available, breaking out.' % i
                        break

                # Add back the data mean (subtracted before composition)
                eig_composition += data_mean.reshape(im_shape)

                P.imshow(eig_composition, P.cm.gray)
            else:
                P.imshow(face, P.cm.gray)
                P.title('Original image')
