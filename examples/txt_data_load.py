#!/usr/bin/env python
"""Read files from Maribeth's format into arrays."""

# Needed modules from the standard library
import re
import sys

# Third party modules
import numpy as N

# Code begins
def mwread(fname):
    """Read mw file and return dict with arrays.

    The input data is assumed to be in a file whose format is:

        r:
          0.250029,   0.249549,    0.25019,   0.250232

        A:
          0.399973,   0.199979,   0.200005,   0.200014
          0.199992,   0.400235,   0.200033,   0.200102

        B:
          0.428502,   0.142868,   0.142897,   0.142838
          0.142884,    0.57165,   0.143053,   0.285911

    The output is a dict whose keys are the letter labels ('r','A','B', etc)
    and whose values are one-dimensional NumPy arrays with the numbers, in
    double precision.

    :Parameters:
      fname : string
        Name of the input file."""

    fobj = open(fname)

    # Regular expression to match array labels
    label_re = re.compile('^([a-zA-Z])+:')

    # Initialize output dict
    dct = {}
    # Start the state machine in 'scan' mode and switch to data reading mode
    # ('read') whenever we find what looks like a label.
    mode = 'scan'
    for line in fobj:
        if mode == 'scan':
            match = label_re.match(line)
            if match:
                # Switch modes
                mode = 'read'
                # Prepare state for read mode
                name = match.group(1)
                data = []
        elif mode == 'read':
            if line.isspace():
                # Pure whitespace lines force a mode switch back to
                # scanning for variables
                mode = 'scan'
                # Store the data that we'd been accumulating for the
                # current array
                dct[name] = N.array(data,float)
            else:
                # Read data, assume line contains comma-separated strings
                # of numbers
                data.extend([float(n) for n in line.split(',')])

    # Cleanup before exiting
    fobj.close()
        
    return dct
    

# If run as a script
if __name__ == '__main__':
    # This allows calling it from the command line with the name of the file to
    # read as an argument
    try:
        fname = sys.argv[1]
    except IndexError:
        print 'First argument must be filename to read'
        sys.exit(1)
        
    data = mwread(fname)
    print 'Data dict:'
    for k,val in data.iteritems():
        print '%s:' % k
        print val
        print

    # Now, load the names from the data dict as top-level variables (use
    # specially named counters just in case the file declares something common
    # like 'k'):
    for _k,_val in data.iteritems():
        exec '%s = _val' % _k
        
    print "Now, you can use either the top-level dict 'data', or the variables:"
    print data.keys()
