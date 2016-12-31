#!/usr/bin/python
# coding: utf-8

r"""

PythonOCC
---------
in qtDisplay.py
lines 84 to 87 need to be changed to
        elif HAVE_PYQT4:
            win_id = self.winId()
            win_id = int(win_id)
        return win_id
if using a version earlier than 0.16.5

CSF_GraphicShr
--------------
Should be an env variable pointing to TKOpenGl.dll or libTKOpenGl.dll in the dir where OCC python files are

"""

import os

print("CSF_GraphicShr" in os.environ)
if "CSF_GraphicShr" in os.environ:
    print(os.environ["CSF_GraphicShr"])

from PyQt4 import QtCore, QtGui, QtOpenGL

import OCC.Display.qtDisplay

import aocutils.display.color


# class PicButton(QtGui.QAbstractButton):
#     def __init__(self, pixmap, parent=None):
#         super(PicButton, self).__init__(parent)
#         self.pixmap = pixmap
#         self.setMaximumSize(self.pixmap.size())
#
#     def paintEvent(self, event):
#         painter = QtGui.QPainter(self)
#         painter.drawPixmap(event.rect(), self.pixmap)
#
#     def sizeHint(self):
#         return self.pixmap.size()


class Qt3dViewer(QtGui.QWidget, object):
    def __init__(self, parent, viewer_background_color=(100., 100., 100., 250., 250., 250.), show_topology_menu=True):
        QtGui.QWidget.__init__(self, parent)

        self.viewer = OCC.Display.qtDisplay.qtViewer3d(self)
        self.viewer.InitDriver()

        self.background_color = viewer_background_color
        r1, g1, b1, r2, g2, b2 = viewer_background_color
        self.viewer_display.set_bg_gradient_color(r1, g1, b1, r2, g2, b2)

        vbox = QtGui.QVBoxLayout()

        # tools
        # hbox = QtGui.QHBoxLayout()
        # hbox.setMargin(0)
        # hbox.setSpacing(0)

        max_width = 20
        max_height = 20

        btn_view_left = QtGui.QPushButton(QtGui.QIcon(QtGui.QPixmap("icons/left-16x16.png")), "", self)
        btn_view_left.setMaximumSize(max_width, max_height)
        btn_view_right = QtGui.QPushButton(QtGui.QIcon(QtGui.QPixmap("icons/right-16x16.png")), "", self)
        btn_view_right.setMaximumSize(max_width, max_height)
        btn_view_right.move(max_width, 0)
        btn_view_top = QtGui.QPushButton(QtGui.QIcon(QtGui.QPixmap("icons/top-16x16.png")), "", self)
        btn_view_top.setMaximumSize(max_width, max_height)
        btn_view_top.move(2 * max_width, 0)

        # hbox.addWidget(btn_view_left, 0, QtCore.Qt.AlignLeft)
        # hbox.addWidget(btn_view_right, 0, QtCore.Qt.AlignLeft)
        # hbox.addWidget(btn_view_top, 0, QtCore.Qt.AlignLeft)


        vbox = QtGui.QVBoxLayout()
        vbox.setContentsMargins(0, 0, 0, 0)

        # vbox.addLayout(hbox)
        vbox.addWidget(self.viewer)
        self.setLayout(vbox)
        self.show()

        self._shapes = list()

    @property
    def viewer_display(self):
        r"""Viewer3d getter

        Returns
        -------
        OCC.Display.OCCViewer.Viewer3d

        """
        return self.viewer._display

    def display_shape(self, shapes, material=None, texture=None, color=None, transparency=None, update=False):
        r"""DisplayShape and keep track of displayed shapes

        Parameters
        ----------
        shapes : list of OCC Shapes or single OCC Shape
        material
        texture
        color
        transparency : float between 0 and 1
        update : bool
        """
        self.viewer_display.DisplayShape(shapes, material=material, texture=texture, color=color,
                                         transparency=transparency, update=update)
        if isinstance(shapes, list):
            for shape in shapes:
                self._shapes.append(shape)
        else:
            self._shapes.append(shapes)


def colour_qt_to_occ(qt_colour):
    r"""Convert a qt colour coded on ints from 0 to 255 to an OCC color coded on floats from 0 to 1

    Parameters
    ----------
    qt_colour : tuple of 3 ints

    """
    r, g, b = qt_colour  # 255
    return aocutils.display.color.color(r / 255., g / 255., b / 255.)  # 1


if __name__ == '__main__':
    import aocutils.primitives

    box = aocutils.primitives.box(100, 50, 25)

    app = QtGui.QApplication([])
    window = QtGui.QMainWindow()
    window.resize(400, 300)
    widget = Qt3dViewer(window)
    widget.display_shape(box)
    window.setCentralWidget(widget)
    # window.move(300, 300)
    # w.setWindowTitle('Simple')
    window.show()
    app.exec_()
