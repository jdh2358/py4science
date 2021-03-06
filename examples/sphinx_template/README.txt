sphinx template sampledoc
=========================

This is the top level build directory for the sphinx sampledoc
documentation.  All of the documentation is written using sphinx, a
python documentation system built on top of ReST.  This directory
contains


* model - A document describing a model.  Be sure to see the cheat
  sheet file model/sphinx_helpers.rst

* simulations - A document describing the simulations -- contains a
  code subdir with python scripts and a make.py file to build them
  into PNGs

* make.py - the build script to build the html or PDF docs.  Do
  `python make.py html` or `python make.py latex` for PDF

* sphinxext - some extensions to sphinx to handle math, ipython syntax
  highlighting, autodocs

* index.rst - the top level include document for sampledocs document

* conf.py - the sphinx configuration

* _static - used by the sphinx build system

* _templates - used by the sphinx build system

You can get the latest svn of this document at:

  > svn co https://matplotlib.svn.sourceforge.net/svnroot/matplotlib/trunk/py4science/examples/sphinx_template


