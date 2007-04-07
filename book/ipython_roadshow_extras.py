"""Extra stuff for the roadshow configuration which we may want to use"""

def magic_ca(parameter_s=''):
    "Simple magic wrapper to call pylab's close('all')"
    pylab.close('all')
    
__IPYTHON__.magic_ca = magic_ca
del magic_ca

##############################################################
# HACK for Tk backends

HACK_TK = 0   # flag to control its use
# Temporary hack around a matplotlib figure closing bug, remove when the bug
# is fixed.  The bug involves matplotlib destroying Mayavi windows it
# shouldn't, which crashes VTK if close('all') is called.
if HACK_TK and matplotlib.rcParams['backend'].startswith('Tk'):
    try:
        pylab.all_figures
    except AttributeError:
        pylab.all_figures = []

    figure_ori = pylab.figure
    close_ori  = pylab.close

    # hack: sentinel to prevent pylab from destroying tk windows.
    pylab.sentinel = 0
    figure_ori(pylab.sentinel,figsize=(0.1, 0.1))
    pylab.show()
    pylab._pylab_helpers.Gcf.figs[pylab.sentinel].window.iconify()

    def figure(num=None,*args,**kw):
        """Wrapper around pylab.figure which updates a global list of held figures."""
        #print 'our figure:',num
        if num == pylab.sentinel:
            raise ValueError, \
                  '%s is an internal sentinel, do not use for your figures' % num
        newfig = figure_ori(num,*args,**kw)
        pylab.all_figures.append(newfig)
        return newfig

    def close(*args):
        """Close all open figures managed by our figure() wrapper."""

        #print 'our close:',args
        if len(args)==1 and args[0]=='all':
            #print 'Closing figures:',pylab.all_figures
            map(close_ori,pylab.all_figures)
            pylab.all_figures = []
        else:
            close_ori(*args)

    # overwrite the figure/close calls in matplotlib itself
    pylab.figure = figure
    pylab.close  = close

del HACK_TK
# /HACK
##############################################################
