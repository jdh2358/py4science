.. _sphinx_helpers:


******************
Sphinx Cheat Sheet
******************

Cheat sheet on how to make this site and install these extensions and
other goodies.  You can see a literal version of this file below in
:ref:`sphinx-literal`.

.. _installing-docdir:
Installing your doc directory
=============================

You may already have sphinx `sphinx <http://sphinx.pocoo.org/>`_
installed -- you can check by doing::

  python -c 'import sphinx'

If that fails grab the latest version of and install it with::

  > sudo easy_install sphinx

Now you are ready to build a template for your docs, using
sphinx-quickstart::

  > sphinx-quickstart

accepting most of the defaults.  I choose "py4sci" as the name of my project

We can test the installation by changing into the project directory,
and typing `make html`::

  cd py4sci
  make html


