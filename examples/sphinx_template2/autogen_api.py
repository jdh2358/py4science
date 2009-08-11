#!/usr/bin/env python
"""Script to auto-generate our API docs.
"""
# stdlib imports
import os
import sys

# local imports
sys.path.append(os.path.abspath('tools/sphinxext'))
from apigen import ApiDocWriter

#*****************************************************************************
if __name__ == '__main__':
    pjoin = os.path.join
    package = 'email'
    outdir = pjoin('api','generated')
    docwriter = ApiDocWriter(package,rst_extension='.rst')
    # Skip packages you don't want to document
    docwriter.package_skip_patterns += [r'\.mime', 'test',
                                        ]
    # For modules, there are also skip patterns
    docwriter.module_skip_patterns += [ r'\.mime',
                                        ]
    docwriter.write_api_docs(outdir)
    docwriter.write_index(outdir, 'gen',
                          relative_to = 'api'
                          )
    print '%d files written' % len(docwriter.written_modules)
