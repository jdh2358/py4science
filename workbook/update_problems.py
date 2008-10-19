#!/usr/bin/env python
"""Update the problems (skeletons and solutions) relative to their source.

"""
import os

from glob import glob
from os import system as sh

from IPython.genutils import target_outdated

# Constants
SRC_DIR = '../examples'
UPDATE = './mkskel.py'


if __name__ == '__main__':
    
    problems = [f for f in os.listdir('problems') if f.endswith('.py')]

    os.chdir(SRC_DIR)
    to_update = []
    for f in problems:
        skel = os.path.join('skel',f.replace('.py','_skel.py'))
        soln = os.path.join('soln',f.replace('.py','_soln.py'))
        src = [f]
        if target_outdated(skel,src) or target_outdated(soln,src):
            to_update.append(f)

    if to_update:
        targets = ' '.join(to_update)
        print 'Updating the following problems:\n',targets
        sh('%s %s' % (UPDATE,targets))
    else:
        print 'All targets up to date, nothing to do.'
