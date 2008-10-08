"""A special directive for including a matplotlib plot.

Given a path to a .py file, it includes the source code inline, then:

- On HTML, will include a .png with a link to a high-res .png.

- On LaTeX, will include a .pdf

This directive supports all of the options of the `image` directive,
except for `target` (since plot will add its own target).

Additionally, if the :include-source: option is provided, the literal
source will be included inline, as well as a link to the source.
"""

#-----------------------------------------------------------------------------
# Modules

# Stdlib imports
import glob
import os
import shutil
import sys

from os import path

# Third-party imports
from docutils.parsers.rst import directives

try:
    # docutils 0.4
    from docutils.parsers.rst.directives.images import align
except ImportError:
    # docutils 0.5
    from docutils.parsers.rst.directives.images import Image
    align = Image.align

# Congigure matplotlib to only use a non-gui backend for image generations
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import IPython.Shell

#-----------------------------------------------------------------------------
# Global constants

# Make an IPython instance to run scripts
mplshell = IPython.Shell.MatplotlibShell('mpl')

# HTML generation options
options = {'alt': directives.unchanged,
           'height': directives.length_or_unitless,
           'width': directives.length_or_percentage_or_unitless,
           'scale': directives.nonnegative_int,
           'align': align,
           'class': directives.class_option,
           'include-source': directives.flag }

template = """
.. htmlonly::

   [`source code <../%(outdir)s/%(basename)s.py>`__,
   `png <../%(outdir)s/%(basename)s.hires.png>`__,
   `pdf <../%(outdir)s/%(basename)s.pdf>`__]

   .. image:: ../%(outdir)s/%(basename)s.png
%(options)s

.. latexonly::
   .. image:: ../%(outdir)s/%(basename)s.pdf
%(options)s

"""

# XXX - we're abusing things a bit by dumping all output files into the
# top-level static direcotry that sphinx uses.  Ideally we should create our
# own and populate it with a hierarchy similar to that of the inputs, to avoid
# possible name clashes from figures with identical names that originally
# existed in different directories.
static_dir = '_static'

#-----------------------------------------------------------------------------
# Code begins

def makefig(fullpath, outdir):
    """
    run a pyplot script and save the low and high res PNGs and a PDF in outdir
    """

    # Resolutions for each formats (passed as dpi= to savefig call)
    formats = [('png', 100),
               ('hires.png', 200),
               ('pdf', 72),
               ]
             
    fullpath = str(fullpath)  # todo, why is unicode breaking this
    basedir, fname = os.path.split(fullpath)
    basename, ext = os.path.splitext(fname)
    all_exists = True

    if basedir != outdir:
        shutil.copyfile(fullpath, os.path.join(outdir, fname))

    for format, dpi in formats:
        outname = os.path.join(outdir, '%s.%s' % (basename, format))
        if not os.path.exists(outname):
            all_exists = False
            break

    if all_exists:
        print '    already have %s' % fullpath
        return

    print '    building %s' % fullpath
              
    # we need to clear between runs
    plt.close('all')    
    matplotlib.rcdefaults()
    # Set a figure size that doesn't overflow typical browser windows
    matplotlib.rcParams['figure.figsize'] = (6,4)

    # Run the actual script using IPython/mpl shell
    mplshell.magic_run(fullpath)
    
    # Generate output files
    for format, dpi in formats:
        outname = os.path.join(outdir, '%s.%s' % (basename, format))
        if os.path.exists(outname): continue
        plt.savefig(outname, dpi=dpi)


def run(arguments, options, state_machine, lineno):
    """Execution of the docutils plot directive.
    """

    # Code taken from sphinx - locate the full paths to the included script
    # Relative filename, as given in the original directive in the rst source
    rel_fn = arguments[0]
    # Source directory for the input rst file that made the call
    source_dir = path.dirname(path.abspath(state_machine.input_lines.source(
        lineno - state_machine.input_offset - 1)))
    # Full filename for the plot script
    full_fn = path.normpath(path.join(source_dir, rel_fn))

    #
    basedir, fname = os.path.split(full_fn)
    basename, ext = os.path.splitext(fname)

    # XXX - we're abusing the sphinx '_static' direcory here.
    outdir = static_dir

    if not os.path.isdir(outdir):
        os.makedirs(outdir)
        
    makefig(full_fn, outdir)
                
    if options.has_key('include-source'):
        lines = ['.. literalinclude:: %(full_fn)s' % locals()]
        del options['include-source']
    else:
        lines = []

    options = ['      :%s: %s' % (key, val) for key, val in
               options.items()]
    options = "\n".join(options)

    lines.extend((template % locals()).split('\n'))

    state_machine.insert_input(
        lines, state_machine.input_lines.source(0))
    return []


#-----------------------------------------------------------------------------
# Register the plot directive with docutils
try:
    # New docutils API
    from docutils.parsers.rst import Directive
except ImportError:
    # Legacy API
    from docutils.parsers.rst.directives import _directives

    def plot_directive(name, arguments, options, content, lineno,
                       content_offset, block_text, state, state_machine):
        return run(arguments, options, state_machine, lineno)
    
    plot_directive.__doc__ = __doc__
    plot_directive.arguments = (1, 0, 1)
    plot_directive.options = options

    _directives['plot'] = plot_directive
    
else:
    # New API
    class plot_directive(Directive):
        required_arguments = 1
        optional_arguments = 0
        final_argument_whitespace = True
        option_spec = options

        def run(self):
            return run(self.arguments, self.options,
                       self.state_machine, self.lineno)
        
    plot_directive.__doc__ = __doc__

    directives.register_directive('plot', plot_directive)
