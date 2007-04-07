"""Simple image recognition library - SVD based.

Ben Herbst - U. Stellenbosch.
Fernando Perez - U. Colorado, Boulder."""

# Required packages

# Std lib
import os

# Third-party
import pylab as P
import numpy as N
import scipy as S

# Scipy has a special loading mechanism to import multiple subpackages into
# its own namespace for convenience
S.pkgload('linalg')

# Classes and functions begin
def imshow2(m1,m2,labels=(None,None)):
    """Display two images side by side.

    Returns the created figure instance."""

    fig = P.figure()
    ax1 = [0.025,0.1,0.45,0.775]
    ax2 = [0.525,0.1,0.45,0.775]
    for m,ax_coord,label in [(m1,ax1,labels[0]),(m2,ax2,labels[1])]:
        ax = fig.add_axes(ax_coord)
        ax.imshow(m,cmap=P.cm.gray)
        if label:
            ax.set_xlabel(label)
        P.xticks([],[])
        P.yticks([],[])
    P.draw_if_interactive()
    return fig

class ImageCollection(object):
    """Class to hold a collection of image files stored  in a directory"""

    def __init__(self,images,names=None):
        """Construct a collection from a list of images and names.

        Inputs:

          - images: a sequence of valid image objects.

        Optional inputs:

          - names: a sequence of strings to be used as names for the images.
          If not given, the images are simply named by their index."""

        num_images = len(images)
        if names is None:
            names = map(str,range(num_images))

        assert (len(names) == num_images,
                'List of names must be of same length as image sequence')

        self.images = images
        self.names = names

        # make a dict for keyed access
        self.img_dict = dict(zip(names,images))

        self.num_images = num_images
        
        # Public attributes
        self.interpolation = 'nearest'
        self.images 

    @staticmethod
    def from_directory(dir_name,verbose=False):
        """Read all images in a given directory, return an ImageCollection.

        It reads all files in the directory and tries to compute an image
        (using scipy's imread) for all of them and stores a list of
        (filename,array) pairs.

        Inputs:

          - dir_name: a string containing the directory name to scan.

        Optional inputs:

          - verbose(False): print extra verbose information about skipped
          files while running.  Set to any True value for basic diagnostics of
          error conditions, and to higher integer values for further messages.

        Outputs:
          - an ImageCollection instance.
          """

        img = []
        names = []

        imread = S.misc.pilutil.imread
        for fname in os.listdir(dir_name):
            full_fname = os.path.join(dir_name,fname)
            try:
                if verbose > 1:
                    print 'Reading file:',fname
                img.append(imread(full_fname))
                names.append(fname)
            except IOError:
                if verbose:
                    print 'Skipping non-image file:',fname
        # Safety warning
        if not img:
            print 'WARNING: empty image collection, no valid images found.'
        return ImageCollection(img,names)
            
    def show_image(self,number,fignum=None,interpolation=None):
        """Show a single image, by its index.

        Inputs:
          - number: index (0-offset) of the image to display.
          
        Optional inputs:

          - fignum(None): a matplotlib figure number, to reuse for display.
          If not given, a new figure is automatically created.

          - interpolation: interpolation mode for display.  If not given, the
          instance .interpolation attribute is used.

        Outputs:

          The number of the created figure window, so it can be reused."""

        if interpolation is None:
            interpolation = self.interpolation
        image = self.images[number]
        name = self.names[number]
        if fignum is None:
            # make a new figure from scratch
            fig = P.matshow(image,cmap=P.cm.gray,interpolation=interpolation)
        else:
            # draw into an existing figure directly
            fig = P.figure(fignum)
            ax_im = fig.axes[0].images[0]
            ax_im.set_data(image)
            P.draw()
            
        P.title('Image [%d]: %s - (%d/%d)' %
                (number,name,number+1,self.num_images))
        P.draw_if_interactive()
        return fig.number

    def browse_images(self):
        """Browse a set of image files"""

        # Show the first figure separately, so we can reuse the figure window
        fignum = self.show_image(0)
        count = 0
        while count < self.num_images:
            self.show_image(count,fignum)
            ans = raw_input('Enter for next, <p> for previous, <q> to quit: ')
            if ans=='p':
                if count>0: 
                    count -= 1
            elif ans=='q':
                break
            else:
                count += 1

    def list_images(self):
        """Print a listing of all images in the collection"""

        print 'Total number of images:',self.num_images
        for i,name in enumerate(self.names):
            print '%3d - %s' % (i,name)

    def normalized_flat(self):
        """Return a normalized version of the images in the collection.

        This is a single array where each image has been 'flattened' as a
        column vector."""
        # Make a single matrix where we'll store the flattened version of all
        # the images for further processing.  We pick up the image dimensions
        # from the first one without checking they all have the same
        # dimensions, we can validate this more strictly later.
        im0 = self.images[0]
        imshape = im0.shape
        shape = (imshape[0]*imshape[1],self.num_images)
        # The flat image has to be in a floating-point type so we can do SVD
        # and similar things with it
        img_flat = N.empty(shape,N.float32)
        for col,im in enumerate(self.images):
            img_flat[:,col] = im.flat
        # remove average vectors to make a 'normalized' image
        img_avg = img_flat.mean(axis=1)
        # we need to broadcast the average as a column vector
        return img_avg, img_flat - img_avg[:,N.newaxis]
        
            
# Functions for actual facial recognition
class TrainingImages(object):
    """Class to represent a collection of training images"""

    def __init__(self,dir_name,verbose=False):
        """Load a collection of images from a directory"""

        self.image_coll = ImageCollection.from_directory(dir_name,
                                                         verbose=verbose)
        self.num_images = self.image_coll.num_images
        img_avg,img_flat_norm = self.image_coll.normalized_flat()
        # Compute singular values and U matrix
        #umat,sigma,vtmat = S.linalg.svd(img_flat_norm)
        umat,sigma,vtmat = N.linalg.svd(img_flat_norm,0)

        # Array of 'eigenimages' in normal (not flattened) format
        imshape = self.image_coll.images[0].shape
        eig_img = N.empty((self.num_images,imshape[0],imshape[1]),umat.dtype)
        for i in range(self.num_images):
            eig_img[i] = N.reshape(umat[:,i],imshape)

        # Store in object all these
        self.sigma = sigma
        self.umat = umat
        self.vtmat = vtmat
        self.imshape = self.image_coll.images[0].shape
        self.eig_img = ImageCollection(eig_img)
        self.img_avg = img_avg
        self.img_flat_norm = img_flat_norm

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
        """Verify that a provided test image corresponds to a given key.

        Assumes that the input is unnormalized."""
        
        ref_coeffs = self.proj_c[key]
        norm_test = test_img.flat - self.img_avg
        test_coeffs = N.dot(self.utt,norm_test)
        l2_err = N.linalg.norm(test_coeffs-ref_coeffs,2)
        imshow2(self.image_coll.images[key],test_img,
                labels = ('Reference Image','Test Image'))
        P.title('L2 error: %.2e' % l2_err)

    def identify(self,test_img):
        """Verify that a provided test image corresponds to a given key.

        Assumes that the input is unnormalized."""
        
        norm_test = test_img.flat - self.img_avg
        test_coeffs = N.dot(self.utt,norm_test)
        diff2 = ((self.proj_c - test_coeffs)**2).sum(axis=1)
        minidx = diff2.argmin()
        best_err = diff2[minidx]
        imshow2(test_img,self.image_coll.images[minidx],
                labels = ('Test Image','Best Match: %d' % minidx))
        P.title('L2 error: %.2e' % best_err)
