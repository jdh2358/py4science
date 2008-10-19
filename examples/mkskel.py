#!/usr/bin/env python
"""Make skeletons out of Python scripts.

Usage:

   mkskel [--test]  file1.py file2.py ....

If --test is given, the test suite is run instead.

For each input filename f.py, a pair of output files is generated, f_soln.py
and f_skel.py.

Source markup is very simple.  The tests in the file show precisely how it
works, but in summary:

- Pure comment lines with the special marker (#@) are left in the skeleton
  (only the marker is stripped, but they remain as valid comments).  These are
  typically used for hints.

- Code lines terminated with the marker are:

  - In the skeleton, replaced by a NotImplementedError call.  Consecutive lines
  are replaced by a single call.

  - In the solution, kept as is but the marker is removed.
"""

from __future__ import with_statement

#-----------------------------------------------------------------------------
# Stdlib imports
import os
import re
import shutil
import sys

# Third-party imports
import nose

# Constants
MARKER = '#@'
DEL_RE = re.compile(r'''^((\s*)(.*?))\s*%s\s*$''' % MARKER)
HINT_RE = re.compile(r'''^(?P<space>\s*)%s\s+(?P<hint>.*)$''' % MARKER)
                       

#-----------------------------------------------------------------------------
# Main code begins

def src2soln(src):
    """Remove markers from input source, leaving all else intact.

    Inputs:
      src : sequence of lines (file-like objects work out of the box)
    """
    
    out = []
    addline = out.append
    for line in src:
        # Check for lines to delete and with hints
        mdel  = DEL_RE.match(line)
        mhint = HINT_RE.match(line)

        # All hints are unconditionally removed
        if mhint is None:
            if mdel:
                # if marker is matched in code, strip it and leave the code
                line = mdel.group(1)+'\n'
            addline(line)
            
    return ''.join(out)


def src2skel(src):
    """Remove markers from input source, replacing marked lines.

    Marked lines are replaced with "raise NotImplementedError" calls that
    summarize the total number of deleted lines.

    Inputs:
      src : sequence of lines (file-like objects work out of the box)
    """

    def flush_buffers(normal_lines,del_lines=0):
        """Local function to reuse some common code"""

        if state_cur == normal:
            # add the normal lines
            out.extend(normal_lines)
            normal_lines[:] = []
        else:
            # Add the summary of 'raise' lines

            # flush counter of code (disabled, we report static summary)
            #msg = '1 line' if del_lines==1 else ('%s lines' % del_lines)
            #exc = exc_tpl % msg
            exc = exc_tpl
            
            # Use the last value of 'space'
            line = '%s%s' % (spaces[0],exc)
            out.append(line)
            del_lines = 0
            spaces[:] = []
            
        return del_lines
    
    # used to report actual # of lines removed - disabled
    #exc_tpl = "raise NotImplementedError('%s missing')\n"    
    exc_tpl = "raise NotImplementedError('insert missing code here')\n"
    
    # states for state machine and other initialization
    normal,delete = 0,1
    state_cur = normal
    del_lines = 0  # counter, in case we want to report # of deletions
    spaces = []
    normal_lines = []
    out = []
    
    # To remove multiple consecutive lines of input marked for deletion, we
    # need a small state machine.
    for line in src:
        # Check for lines to delete and with hints
        mdel  = DEL_RE.match(line)
        mhint = HINT_RE.match(line)

        if mhint:
            state_new = normal
            hint = mhint.group('space')+'# ' + mhint.group('hint') +'\n'
            normal_lines.append(hint)
        else:
            if mdel is None:
                state_new = normal
                normal_lines.append(line)
            else:
                state_new = delete
                del_lines += 1
                spaces.append(mdel.group(2))
            
        # Flush output only when there's a change of state
        if state_new != state_cur:
            del_lines = flush_buffers(normal_lines,del_lines)

        # Update state machine
        state_cur = state_new

    # Final buffer flush is unconditional
    flush_buffers(normal_lines)
    
    return ''.join(out)


def transform_file(fpath,fname_skel,fname_soln):
    """Run the cleanup routines for a given input, creating skel and soln.
    """

    # get the mode of the input so that we can create the output files with the
    # same mode
    fmode = os.stat(fpath).st_mode
    
    with open(fpath) as infile:
        # Generate the skeleton
        skel = src2skel(infile)
        with open(fname_skel,'w') as fskel:
            fskel.write(skel)
        os.chmod(fname_skel,fmode)
        
        # Reset the input file pointer and generate the solution
        infile.seek(0)
        soln = src2soln(infile)
        with open(fname_soln,'w') as fsoln:
            fsoln.write(soln)
        os.chmod(fname_soln,fmode)

#-----------------------------------------------------------------------------
# Main execution routines

def copyforce(src,dest):
    """Forceful file link/copy that overwrites destination files."""
    try:
        copy = os.link
    except AttributeError:
        copy = shutil.copy
    if os.path.isfile(dest):
        os.remove(dest)
    copy(src,dest)


def mvforce(src,dest):
    """Forceful file copy that overwrites destination files."""
    if os.path.isfile(dest):
        os.remove(dest)
    shutil.move(src,dest)


def main(argv=None):
    """Main entry point as a command line script for normal execution"""
    
    if argv is None:
        argv = sys.argv

    # If there are subdirs called skel and soln, we populate them by moving the
    # generated files there, otherwise they're left in the current dir.
    skel_dir = 'skel'
    soln_dir = 'soln'
    has_skel_dir = os.path.isdir(skel_dir)
    has_soln_dir = os.path.isdir(soln_dir)

    # First, check that all files are present and abort immediately if any of
    # them isn't there.
    for fpath in argv[1:]:
        if not os.path.isfile(fpath):
            raise OSError("file %r not found" % fpath)

    # If all files are there, then go ahead and process them unconditionally
    for fpath in argv[1:]:
        basename, ext = os.path.splitext(fpath)
        fname_skel = basename + '_skel' + ext
        fname_soln = basename + '_soln' + ext
        transform_file(fpath,fname_skel,fname_soln)
        # Move files over to final dirs if present
        if has_skel_dir:
            mvforce(fname_skel,os.path.join(skel_dir,fname_skel))
        if has_soln_dir:
            mvforce(fname_soln,os.path.join(soln_dir,fname_soln))

#-----------------------------------------------------------------------------
# Tests

def str_match(s1,s2):
    """Check that two strings are equal ignoring trailing whitespace."""
    #print '***S1\n',s1,'\n***S2\n',s2  # dbg
    nose.tools.assert_equal(s1.rstrip(),s2.rstrip())
    

def test_simple():
    src = """
    first line
    del line  #@
    second line
    """
    srclines = src.splitlines(True)
    
    clean = """
    first line
    raise NotImplementedError('insert missing code here')
    second line
    """
    
    cleaned = src2skel(srclines)
    yield str_match,cleaned,clean

    clean = """
    first line
    del line
    second line
    """
    cleaned = src2soln(src.splitlines(True))
    yield str_match,cleaned,clean
    

def test_multi():
    src = """
    first line
    #@ Hint: remember that
    #@ idea we discussed before...
    del line  #@
    del line2  #@
    del line3  #@
    second line:
      del line4  #@
      del line5  #@
    third line

    some indented code: #@
      with more... #@
    """
    srclines = src.splitlines(True)

    clean = """
    first line
    # Hint: remember that
    # idea we discussed before...
    raise NotImplementedError('insert missing code here')
    second line:
      raise NotImplementedError('insert missing code here')
    third line

    raise NotImplementedError('insert missing code here')
    """
    cleaned = src2skel(srclines)
    yield str_match,cleaned,clean

    clean = """
    first line
    del line
    del line2
    del line3
    second line:
      del line4
      del line5
    third line

    some indented code:
      with more...
    """
    cleaned = src2soln(srclines)
    yield str_match,cleaned,clean


@nose.tools.nottest
def test():
    """Simple self-contained test runner."""
    nose.runmodule(__name__,exit=False,
                   argv=['--doctests',
                         #'-s',
                         #'--pdb-failures',
                         ])

#-----------------------------------------------------------------------------
# Execution from the command line.

if __name__ == "__main__":
    if '--test' in sys.argv:
        test()
    else:
        main(sys.argv)
