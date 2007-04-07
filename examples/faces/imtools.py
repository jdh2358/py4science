"""Image handling utilities for the SVD-based image matching library."""

import os
import numpy as N
import scipy as S
import pylab as P

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
        # Assume all images have the same shape.
        self.im_shape = images[0].shape

        # make a dict for keyed access
        self.img_dict = dict(zip(names,images))

        self.num_images = num_images
        
        # Public attributes
        self.interpolation = 'nearest'
        self.images

    def __getitem__(self, n):
        """Return image number n."""
        if n > self.num_images-1:
            return 0
        else:
            return self.images[n]
        
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

    def flat(self):
        """Return an array which contains each image 'flattened' as a
        column vector."""
        # Make a single matrix where we'll store the flattened version of all
        # the images for further processing.  We pick up the image dimensions
        # from the first one without checking they all have the same
        # dimensions, we can validate this more strictly later.
        (imheight,imwidth) = self.images[0].shape
        shape = (imheight*imwidth,self.num_images)
        # The flat image has to be in a floating-point type so we can do SVD
        # and similar things with it
        img_flat = N.empty(shape,N.float32)
        for col,im in enumerate(self.images):
            img_flat[:,col] = im.flat

        return img_flat
