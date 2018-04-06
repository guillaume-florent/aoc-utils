#!/usr/bin/env python
# coding: utf-8

r"""Wx viewer example"""

import wx

from aocutils.primitives import box
from aocutils.display.wx_viewer import Wx3dViewer


class MyFrame(wx.Frame):
    r"""Frame for testing"""

    def __init__(self):
        wx.Frame.__init__(self, None, -1)
        self.box = box(100, 50, 25)
        self.p = Wx3dViewer(self)
        self.p.display_shape(self.box)
        self.Show()


app = wx.App()
frame = MyFrame()
app.SetTopWindow(frame)
app.MainLoop()