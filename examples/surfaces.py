#!/usr/bin/env python
# coding: utf-8

r"""examples/surfaces"""

import itertools

from OCC.Display.SimpleGui import init_display
from OCC.Core.gp import gp_Pnt

# import aocutils.common
from aocutils.operations.interpolate import points_to_bspline
from aocutils.brep.face_make import n_sided
from aocutils.brep.edge_make import edge
from aocutils.brep.vertex_make import vertex
# import aocutils.brep.wire_make
from aocutils.display.defaults import backend
from aocutils.display.color import fp_dark_blue, gray

backend = backend
display, start_display, add_menu, add_function_to_menu = init_display(backend)


def n_sided_patch():
    r"""N sided patch"""

    # left
    pts1 = (gp_Pnt(0, 0, 0.0),
            gp_Pnt(0, 1, 0.3),
            gp_Pnt(0, 2, -0.3),
            gp_Pnt(0, 3, 0.15),
            gp_Pnt(0, 4, 0),
            )
    # front
    pts2 = (gp_Pnt(0, 0, 0.0),
            gp_Pnt(1, 0, -0.3),
            gp_Pnt(2, 0, 0.15),
            gp_Pnt(3, 0, 0),
            gp_Pnt(4, 0, 0),
            )
    # back
    pts3 = (gp_Pnt(0, 4, 0),
            gp_Pnt(1, 4, 0.3),
            gp_Pnt(2, 4, -0.15),
            gp_Pnt(3, 4, 0),
            gp_Pnt(4, 4, 1),
            )
    # right
    pts4 = (gp_Pnt(4, 0, 0),
            gp_Pnt(4, 1, 0),
            gp_Pnt(4, 2, 0.3),
            gp_Pnt(4, 3, -0.15),
            gp_Pnt(4, 4, 1),
            )

    # spl1 is a OCC.Geom.Handle_Geom_BSplineCurve
    spl1 = points_to_bspline(pts1)
    spl2 = points_to_bspline(pts2)
    spl3 = points_to_bspline(pts3)
    spl4 = points_to_bspline(pts4)

    # list of OCC.TopoDS.TopoDS_Edge
    edges = list(map(edge, [spl1, spl2, spl3, spl4]))

    # list of OCC.TopoDS.TopoDS_Vertex
    verts = list(map(vertex, itertools.chain(pts1, pts2, pts3, pts4)))

    f1 = n_sided(edges, [])  # OCC.TopoDS.TopoDS_Face

    display.DisplayShape(edges)
    display.DisplayShape(verts)
    display.DisplayShape(f1, color=fp_dark_blue, update=True)
    print(display.Viewer.__class__)  # OCC.V3d.Handle_V3d_Viewer
    display.View.SetBackgroundColor(gray)


if __name__ == '__main__':
    n_sided_patch()
    start_display()
