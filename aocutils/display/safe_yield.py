# coding: utf-8

r"""safe_yield.py"""

from __future__ import print_function

from OCC.Display.SimpleGui import get_backend


def safe_yield():
    r"""Reimplementation of the safe_yield() function
    that once existed in OCC.Display.SimpleGui"""
    if get_backend() == 'wx':
        # This function (SafeYield) is similar to `wx.Yield`,
        # except that it disables the
        # user input to all program windows before calling `wx.Yield` and
        # re-enables it again afterwards. If ``win`` is not None, this window
        # will remain enabled, allowing the implementation of some limited user
        # interaction.
        import wx
        wx.SafeYield()
    elif get_backend() == 'qt-pyqt4':
        # QtCore.processEvents()
        import PyQt4
        PyQt4.QtGui.QApplication.processEvents()
    elif get_backend() == 'qt-pyside':
        import PySide
        PySide.QtGui.QApplication.processEvents()
    else:
        raise RuntimeError("Could not determine the UI backend")
