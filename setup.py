#!/usr/bin/env python
# coding: utf-8

"""setuptools based setup module for aocutils"""

from setuptools import setup
# To use a consistent encoding
import codecs
from os import path

import aocutils

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with codecs.open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name=aocutils.__name__,
    version=aocutils.__version__,
    description=aocutils.__description__,
    long_description=long_description,
    url=aocutils.__url__,
    download_url=aocutils.__download_url__,
    author=aocutils.__author__,
    author_email=aocutils.__author_email__,
    license=aocutils.__license__,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6'],
    keywords='OpenCASCADE pythonocc CAD',
    packages=['aocutils',
              'aocutils.analyze',
              'aocutils.brep',
              'aocutils.display',
              'aocutils.geom',
              'aocutils.operations'],
    install_requires=['OCC', 'numpy', 'scipy', 'corelib', 'wx'],
    extras_require={
        'dev': [],
        'test': ['pytest', 'coverage'],
    },
    package_data={},
    data_files=[],
    entry_points={})
