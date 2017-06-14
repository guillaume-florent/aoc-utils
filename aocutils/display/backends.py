#!/usr/bin/python
# coding: utf-8

r"""backends module

Summary
-------

Graphical backends related stuff

"""


def available_backends():
    r"""List of available backends"""
    backends = list()
    try:
        import wx
        backends.append("wx")
    except ImportError:
        print("No wx backend")
    try:
        import PySide
        backends.append("qt-pyside")
    except ImportError:
        print("No PySide backend")
    try:
        import PyQt4
        backends.append("qt-pyqt4")
    except ImportError:
        print("No PyQt4 backend")
    try:
        import PyQt5
        backends.append("qt-pyqt5")
    except ImportError:
        print("No PyQt5 backend")

    return backends
