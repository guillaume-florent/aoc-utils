#!/usr/bin/env python
# coding: utf-8

try:
    import OCC
    print(" PythonOCC version : %s" % OCC.VERSION)
except ImportError:
    print("PythonOCC not installed")

try:
    import aocxchange
    print("aocxchange version : %s" % aocxchange.__version__)
except ImportError:
    print("aocxchange not installed")

try:
    import aocutils
    print("  aocutils version : %s" % aocutils.__version__)
except ImportError:
    print("aocutils not installed")

