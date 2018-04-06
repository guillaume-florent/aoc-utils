.. -*- coding: utf-8 -*-

*********
aoc-utils
*********

.. image:: https://travis-ci.org/guillaume-florent/aoc-utils.svg?branch=master
    :target: https://travis-ci.org/guillaume-florent/aoc-utils

.. image:: https://api.codacy.com/project/badge/Grade/ad66c28ad30e46ee8816c561eb19d831
    :target: https://www.codacy.com/app/guillaume-florent/aoc-utils?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=guillaume-florent/aoc-utils&amp;utm_campaign=Badge_Grade

.. image:: https://anaconda.org/gflorent/aocutils/badges/version.svg
    :target: https://anaconda.org/gflorent/aocutils

.. image:: https://anaconda.org/gflorent/aocutils/badges/latest_release_date.svg
    :target: https://anaconda.org/gflorent/aocutils

.. image:: https://anaconda.org/gflorent/aocutils/badges/platforms.svg
    :target: https://anaconda.org/gflorent/aocutils

.. image:: https://anaconda.org/gflorent/aocutils/badges/downloads.svg
    :target: https://anaconda.org/gflorent/aocutils

.. image:: http://img.shields.io/badge/Python-2.7_3.*-ff3366.svg
    :target: https://www.python.org/downloads/

The **aoc-utils** project provides a Python package named **aocutils** with
useful modules/classes/methods for `PythonOCC <http://github.com/tpaviot/pythonocc-core>`_. It is a high level API for PythonOCC.

PythonOCC is a set of Python wrappers for the OpenCascade Community Edition (an industrial strength 3D CAD modeling kernel)

install
-------

.. code-block:: shell

  conda install -c gflorent aocutils

Dependencies
~~~~~~~~~~~~

Please see how the Dockerfile satisfies the requirements.


Goal
----

The goal of the **aocutils** package is to simplify some frequently used operations made in PythonOCC.

Versions
--------

aocutils version and target PythonOCC version

+------------------+-------------------+
| aocutils version | PythonOCC version |
+==================+===================+
| 18.*.*           | >=0.18.2          |
+------------------+-------------------+

Examples
--------

The examples are in the *examples* folder at the Github repository (https://github.com/guillaume-florent/aoc-utils).

The wx backend (wxPython) backend is used for the examples that display a UI.
You may easily change this behaviour to use pyqt or PySide by changing the backend in the call to init_display().

.. image:: https://raw.githubusercontent.com/guillaume-florent/aoc-utils/master/img/geomplate.jpg
    :alt: geomplate

.. image:: https://raw.githubusercontent.com/guillaume-florent/aoc-utils/master/img/surfaces.jpg
    :alt: surfaces
