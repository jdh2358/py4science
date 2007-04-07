#!/usr/bin/env python
"""Basic tests for imatch package."""

# Stdlib modules
import os
import unittest

# Third-party
import numpy as N
import numpy.testing as NT

# Our own code
import imatch
reload(imatch)  # for interactive testing

# Temp - for interactive debugging
from IPython.Shell import IPShellEmbed; ipshell = IPShellEmbed() 

# Testing classes start
class ImageCollectionTestCase(unittest.TestCase):
    def test(self):
        "Simple test to call on a correct image dir"
        dirname = 'data_train'
        images = imatch.ImageCollection.from_directory(dirname)

        # This directory only contains true image files
        self.assert_(images.num_images == len(os.listdir(dirname)))

class TrainingImagesTestCase(unittest.TestCase):
    def test(self):
        "Simple test to call on a correct image dir"
        dirname = 'data_train'
        images = imatch.TrainingImages(dirname)

# Execution as a script

# Select here if you only want to see a few tests.
run_all = True
run_only = []

if __name__ == '__main__':
    print __doc__
    runner = unittest.TextTestRunner()

    if run_all:
        print 'Running all tests.\n'

        # Load ourselves, and load all tests which conform to standard
        # unittest naming conventions
        import test_imatch
        u_tests = unittest.defaultTestLoader.loadTestsFromModule(test_imatch)

        # Define a global suite with all tests to be run
        all_tests = unittest.TestSuite([u_tests])
        runner.run(all_tests)

    else:
        print 'Running only selected tests.\n'
        for test in run_only:
            print 'Running test:',test
            print test.shortDescription()
            runner.run(test)
