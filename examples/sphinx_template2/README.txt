===========================
 sphinx template sampledoc
===========================

This is the top level build directory for the sphinx "sampledoc" documentation.
You can use this as a starter template for your own projects.  The name
"sampledoc" is the mock name for the project, you'll need to configure this for
your needs by editing the conf.py and index.rst files.

All of the documentation is written using reStructuredText and is meant to be
built Sphinx, a python documentation system built on top of ReST.  As of Python
2.6, Sphinx is the default docuentation system for Python itself, and it is
becoming rapidly adopted by multiple projects.

This directory contains:

* index.rst - the top level include document for your project.

* conf.py - the sphinx configuration file.  You need to edit this file to set
  your project name, authors, etc.

* Makefile - just type 'make' to see a list of available targets.

* model - A directory for a mock document describing a model.  Be sure to see
  the cheat sheet file "model/sphinx_helpers.rst".

* simulations - A directory for another mock part of your project.

* pyplots - a directory with matplotlib scripts to generate figures that can be
  included in your document with the 'plot' directive.  See the
  sphinx_helpers.rst file for details.
  
* tools - a directory that contains:

  * sphinxext - some extensions to sphinx to handle math, ipython syntax
    highlighting, autodocs.

  * static - directory where you can put your static content, meant to be
    copied on output by Sphinx into the top-level _static directory.  This is
    never overwritten, so you can keep static CSS files, etc here, that can
    then override the Sphinx ones.

  * templates - directory for your own templates, also used by sphinx.

  
Note: The makefile and sphinx build system create three directories when
bulding the output, named ``build``, ``dist`` and ``_static``.  Do *not* make
directories with these names as part of your project, to avoid possible
conflicts.


You can get the latest svn of this document with::

    svn co https://matplotlib.svn.sourceforge.net/svnroot/matplotlib/trunk/py4science/examples/sphinx_template2
