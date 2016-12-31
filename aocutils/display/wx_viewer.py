#!/usr/bin/python
# coding: utf-8

r"""3D viewer as a wx Panel"""

import os

import wx
import wx.lib.buttons
import wx.lib.colourselect

import OCC.Display.wxDisplay
import OCC.Quantity
import OCC.AIS

import aocutils.display.color
import aocutils.display.topology


class Wx3dViewer(wx.Panel):
    r"""wx based 2d viewer Panel"""
    def __init__(self, parent, viewer_background_color=(50., 50., 50.), show_topology_menu=True):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)

        self.viewer = OCC.Display.wxDisplay.wxViewer3d(self)
        self.viewer.InitDriver()

        self.background_color = viewer_background_color
        self.viewer_display.View.SetBackgroundColor(colour_wx_to_occ(viewer_background_color))

        # tools
        self.tools_panel = wx.Panel(self, -1)
        tools_sizer = wx.BoxSizer(wx.HORIZONTAL)

        btn_view_left = self.create_bitmap_button(self.tools_panel, "icons/left-16x16.png", "Left view")
        btn_view_right = self.create_bitmap_button(self.tools_panel, "icons/right-16x16.png", "Right view")
        btn_view_top = self.create_bitmap_button(self.tools_panel, "icons/top-16x16.png", "Top view")
        btn_view_bottom = self.create_bitmap_button(self.tools_panel, "icons/bottom-16x16.png", "Bottom view")
        btn_view_front = self.create_bitmap_button(self.tools_panel, "icons/front-16x16.png", "Front view")
        btn_view_back = self.create_bitmap_button(self.tools_panel, "icons/back-16x16.png", "Rear view")
        btn_view_iso = self.create_bitmap_button(self.tools_panel, "icons/iso-16x16.png", "Iso view")
        btn_view_fitall = self.create_bitmap_button(self.tools_panel, "icons/fitall-16x16.png", "Fit all")
        btn_view_wireframe = self.create_bitmap_button(self.tools_panel, "icons/wireframe-16x16.png", "Wireframe")
        btn_view_hlr = self.create_bitmap_button(self.tools_panel, "icons/hlr-16x16.png", "Hidden Line Removal")
        btn_view_shaded = self.create_bitmap_button(self.tools_panel, "icons/shaded-16x16.png", "Shaded")

        # background colour
        colour_select = wx.lib.colourselect.ColourSelect(self.tools_panel, -1, colour=viewer_background_color,
                                                         size=(32, 16))
        colour_select.SetToolTip(wx.ToolTip("Background colour"))

        # export image
        btn_export_image = self.create_bitmap_button(self.tools_panel, "icons/export_image-16x16.png",
                                                     "Export to image")

        self.Bind(wx.EVT_BUTTON, self.on_view_left, btn_view_left)
        self.Bind(wx.EVT_BUTTON, self.on_view_right, btn_view_right)
        self.Bind(wx.EVT_BUTTON, self.on_view_top, btn_view_top)
        self.Bind(wx.EVT_BUTTON, self.on_view_bottom, btn_view_bottom)
        self.Bind(wx.EVT_BUTTON, self.on_view_front, btn_view_front)
        self.Bind(wx.EVT_BUTTON, self.on_view_back, btn_view_back)
        self.Bind(wx.EVT_BUTTON, self.on_view_iso, btn_view_iso)

        self.Bind(wx.EVT_BUTTON, self.on_fit_all, btn_view_fitall)
        self.Bind(wx.EVT_BUTTON, self.on_set_mode_wireframe, btn_view_wireframe)
        self.Bind(wx.EVT_BUTTON, self.on_set_mode_hlr, btn_view_hlr)
        self.Bind(wx.EVT_BUTTON, self.on_set_mode_shaded, btn_view_shaded)

        self.Bind(wx.lib.colourselect.EVT_COLOURSELECT, self.on_set_background_color, colour_select)

        self.Bind(wx.EVT_BUTTON, self.on_export_image, btn_export_image)

        tools_sizer.Add(btn_view_left, 0, wx.ALL, 0)
        tools_sizer.Add(btn_view_right, 0, wx.ALL, 0)
        tools_sizer.Add(btn_view_top, 0, wx.ALL, 0)
        tools_sizer.Add(btn_view_bottom, 0, wx.ALL, 0)
        tools_sizer.Add(btn_view_front, 0, wx.ALL, 0)
        tools_sizer.Add(btn_view_back, 0, wx.ALL, 0)
        tools_sizer.Add(btn_view_iso, 0, wx.ALL, 0)

        tools_sizer.Add(btn_view_fitall, 0, wx.ALL, 0)
        tools_sizer.Add(btn_view_wireframe, 0, wx.ALL, 0)
        tools_sizer.Add(btn_view_hlr, 0, wx.ALL, 0)
        tools_sizer.Add(btn_view_shaded, 0, wx.ALL, 0)

        tools_sizer.Add(colour_select, 0, wx.ALL, 0)

        tools_sizer.Add(btn_export_image, 0, wx.ALL, 0)

        if show_topology_menu:
            btn_topology_solid = self.create_bitmap_button(self.tools_panel, "icons/topology_solids-16x16.png",
                                                           "Topology - Solids")
            btn_topology_shells = self.create_bitmap_button(self.tools_panel, "icons/topology_shells-16x16.png",
                                                            "Topology - Shells")
            btn_topology_faces = self.create_bitmap_button(self.tools_panel, "icons/topology_faces-16x16.png",
                                                           "Topology - Faces")
            btn_topology_edges = self.create_bitmap_button(self.tools_panel, "icons/topology_edges-16x16.png",
                                                           "Topology - Edges")
            btn_topology_wires = self.create_bitmap_button(self.tools_panel, "icons/topology_wires-16x16.png",
                                                           "Topology - Wires")

            self.Bind(wx.EVT_BUTTON, self.on_topology_solids, btn_topology_solid)
            self.Bind(wx.EVT_BUTTON, self.on_topology_shells, btn_topology_shells)
            self.Bind(wx.EVT_BUTTON, self.on_topology_faces, btn_topology_faces)
            self.Bind(wx.EVT_BUTTON, self.on_topology_edges, btn_topology_edges)
            self.Bind(wx.EVT_BUTTON, self.on_topology_wires, btn_topology_wires)

            tools_sizer.Add(btn_topology_solid, 0, wx.ALL, 0)
            tools_sizer.Add(btn_topology_shells, 0, wx.ALL, 0)
            tools_sizer.Add(btn_topology_faces, 0, wx.ALL, 0)
            tools_sizer.Add(btn_topology_edges, 0, wx.ALL, 0)
            tools_sizer.Add(btn_topology_wires, 0, wx.ALL, 0)

        self.tools_panel.SetSizer(tools_sizer)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.tools_panel, 0, wx.EXPAND, 0)
        self.tools_panel.SetBackgroundColour(viewer_background_color)
        sizer.Add(self.viewer, 1, wx.ALL | wx.EXPAND, 0)
        self.SetSizer(sizer)

        self._shapes = list()

    @staticmethod
    def create_bitmap_button(parent, img_path, tooltip_str):
        r"""Create a bitmap button

        Parameters
        ----------
        parent : a wx Window
        img_path : str
        tooltip_str : str

        """
        img = wx.Bitmap(os.path.join(os.path.dirname(__file__), img_path))
        btn = wx.lib.buttons.GenBitmapButton(parent, wx.ID_ANY, img, size=(img.GetWidth(), img.GetHeight()))
        btn.SetToolTip(wx.ToolTip(tooltip_str))
        return btn

    @property
    def viewer_display(self):
        r"""Viewer3d getter

        Returns
        -------
        OCC.Display.OCCViewer.Viewer3d

        """
        return self.viewer._display

    # Display methods

    def display_shape(self, shapes, material=None, texture=None, color=None, transparency=None, update=False, topology=True):
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
        if topology:
            if isinstance(shapes, list):
                for shape in shapes:
                    self._shapes.append(shape)
            else:
                self._shapes.append(shapes)

    def display_colored_shape(self, shapes, color='YELLOW', update=False, topology=True):
        r"""DisplayColoredShape and keep track of displayed shapes

        Parameters
        ----------
        shapes : list of OCC Shapes or single OCC Shape
        color
        update : bool

        """
        self.viewer_display.DisplayColoredShape(shapes, color, update)
        if topology:
            if isinstance(shapes, list):
                for shape in shapes:
                    self._shapes.append(shape)
            else:
                self._shapes.append(shapes)

    def display_ais_shape(self, shapes, color=OCC.Quantity.Quantity_NOC_MATRABLUE, transparency=0.8, topology=True):
        r"""Display shapes using AIS and keep track of displayed shapes

        Parameters
        ----------
        shapes : list of OCC Shapes or single OCC Shape
        color : OCC.Quantity
        transparency : bool

        """
        def display_ais(shape):
            ais_shp = OCC.AIS.AIS_Shape(shape)
            ais_shp.SetTransparency(transparency)
            ais_shp.SetColor(color)
            ais_context = self.viewer_display.GetContext().GetObject()
            ais_context.Display(ais_shp.GetHandle())
        if isinstance(shapes, list):
            for shape in shapes:
                display_ais(shape)
                if topology:
                    shape._shapes.append(shape)
        else:
            display_ais(shapes)
            if topology:
                self._shapes.append(shapes)

    def display_vector(self, vec, pnt, update=False):
        r"""Display a vector

        Parameters
        ----------
        vec : OCC.gp.gp_Vec
        pnt : OCC.gp.gp_Pnt
        update : bool

        """
        self.viewer_display.DisplayVector(vec, pnt, update)

    def display_message(self, point, text_to_write, height=None, message_color=None, update=False):
        r"""Display a message

        Parameters
        ----------
        point : OCC.gp.gp_Pnt
        text_to_write : str
        height
        message_color
        update : bool

        """
        self.viewer_display.DisplayMessage(point, text_to_write, height, message_color, update)

    def erase_all(self):
        r"""Erase everything and empty the list of shapes"""
        self.viewer_display.EraseAll()
        self._shapes = []

    # Display settings
    # on_*
    # |
    # v

    def on_view_left(self, event):
        r"""Left view"""
        self.viewer_display.View_Left()

    def on_view_right(self, event):
        r"""Right view"""
        self.viewer_display.View_Right()

    def on_view_top(self, event):
        r"""Top view"""
        self.viewer_display.View_Top()

    def on_view_bottom(self, event):
        r"""Bottom view"""
        self.viewer_display.View_Bottom()

    def on_view_front(self, event):
        r"""Front view"""
        self.viewer_display.View_Front()

    def on_view_back(self, event):
        r"""Back view"""
        self.viewer_display.View_Rear()

    def on_view_iso(self, event):
        r"""Iso view"""
        self.viewer_display.View_Iso()

    def on_export_image(self, event):
        r"""Export image of view to a file"""
        dlg = wx.FileDialog(self, message="Choose a file", defaultFile="", defaultDir="", style=wx.FD_SAVE)
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            # print(path)
            self.viewer_display.ExportToImage(str(path))
        dlg.Destroy()

    def on_fit_all(self, event):
        r"""Fit all"""
        self.viewer_display.FitAll()

    def on_set_mode_hlr(self, event):
        r"""Hidden Line Removal mode"""
        self.viewer_display.SetModeHLR()

    def on_set_mode_shaded(self, event):
        r"""Shaded mode"""
        self.viewer_display.SetModeShaded()

    def on_set_mode_wireframe(self, event):
        r"""Wireframe mode"""
        self.viewer_display.SetModeWireFrame()

    def on_set_background_color(self, event):
        r"""Change the background color"""
        wx_colour = event.GetValue()
        self.tools_panel.SetBackgroundColour(wx_colour)
        self.viewer_display.View.SetBackgroundColor(colour_wx_to_occ(wx_colour))
        self.background_color = wx_colour
        self.Refresh()

    def on_topology_solids(self, event):
        r"""Display another viewer with solid topology"""
        dialog = wx.Dialog(self, title="Topology - Solids")
        panel = Wx3dViewer(dialog, viewer_background_color=self.background_color, show_topology_menu=False)
        for shape in self._shapes:
            aocutils.display.topology.solids(panel.viewer_display, shape, transparency=0.5)
        dialog.ShowModal()

    def on_topology_shells(self, event):
        r"""Display another viewer with shells topology"""
        dialog = wx.Dialog(self, title="Topology - Shells")
        panel = Wx3dViewer(dialog, viewer_background_color=self.background_color, show_topology_menu=False)
        for shape in self._shapes:
            aocutils.display.topology.shells(panel.viewer_display, shape, transparency=0.5)
        dialog.ShowModal()

    def on_topology_faces(self, event):
        r"""Display another viewer with faces topology"""
        dialog = wx.Dialog(self, title="Topology - Faces")
        panel = Wx3dViewer(dialog, viewer_background_color=self.background_color, show_topology_menu=False)
        for shape in self._shapes:
            aocutils.display.topology.faces(panel.viewer_display, shape, transparency=0.5)
        dialog.ShowModal()

    def on_topology_edges(self, event):
        r"""Display another viewer with edges topology"""
        dialog = wx.Dialog(self, title="Topology - Edges")
        panel = Wx3dViewer(dialog, viewer_background_color=self.background_color, show_topology_menu=False)

        for shape in self._shapes:
            aocutils.display.topology.edges(panel.viewer_display, shape)
        dialog.ShowModal()

    def on_topology_wires(self, event):
        r"""Display another viewer with wires topology

        This one is trickier because of the way wires are displayed (alternating display)
        Cannot show modal

        """
        dialog = wx.Dialog(self, title="Topology - Wires")
        panel = Wx3dViewer(dialog, viewer_background_color=self.background_color, show_topology_menu=False)
        dialog.Show()  # display of wires iterates over the wires, cannot show model after displaying
        for shape in self._shapes:
            aocutils.display.topology.wires(panel.viewer_display, shape)
            self.Refresh()
        # dialog.ShowModal()


def colour_wx_to_occ(wx_colour):
    r"""Convert a wx colour coded on ints from 0 to 255 to an OCC color coded on floats from 0 to 1

    Parameters
    ----------
    wx_colour : tuple of 3 ints

    """
    r, g, b = wx_colour  # 255
    return aocutils.display.color.color(r / 255., g / 255., b / 255.)  # 1


if __name__ == "__main__":
    import aocutils.primitives

    class MyFrame(wx.Frame):
        r"""Frame for testing"""
        def __init__(self):
            wx.Frame.__init__(self, None, -1)
            self.box = aocutils.primitives.box(100, 50, 25)
            self.p = Wx3dViewer(self)
            self.p.display_shape(self.box)
            self.Show()

    app = wx.App()
    frame = MyFrame()
    app.SetTopWindow(frame)
    app.MainLoop()
