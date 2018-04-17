#!/usr/bin/env python
# coding: utf-8

r"""Wx viewer example"""

import wx
from aocutils.primitives import box
from aocutils.display.wx_viewer import Wx3dViewerFrame

box = box(100, 50, 25)

app = wx.App()
frame = Wx3dViewerFrame()
frame.wx_3d_viewer.display_shape(box)
app.SetTopWindow(frame)
app.MainLoop()
