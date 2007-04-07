#!/usr/bin/env python
"""Simple testing script for imatch.py"""

import pylab as P

import imatch, imatch2

from imtools import ImageCollection

classifier = imatch2.FaceClassifier('data_train/')
classifier.truncate_idx = 12

imtest = ImageCollection.from_directory('data_test/')
i0 = imtest.images[0]
i1 = imtest.images[1]

classifier.verify(classifier.image_coll.images[0],0)
classifier.verify(classifier.image_coll.images[0],1)

classifier.identify(imtest.images[0])
classifier.identify(classifier.image_coll.images[1])
classifier.verify(imtest.images[0],13)
classifier.verify(imtest.images[0],37)

classifier.plot_eigenfaces()
classifier.plot_sigma()

classifier.decompose(i0)

P.show()
