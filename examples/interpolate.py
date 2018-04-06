#!/usr/bin/env python
# coding: utf-8

r"""Points interpolation examples"""

import logging

from OCC.Display.SimpleGui import init_display
from OCC.Core.gp import gp_Pnt, gp_Vec

from aocutils.operations.interpolate import points_to_bspline, points, \
    points_vectors, points_no_tangency
from aocutils.geom.curve import Curve
# import aocutils.operations.interpolate
# import aocutils.geom.curve
from aocutils.display.defaults import backend

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s :: %(levelname)6s :: %(module)20s :: '
                           '%(lineno)3d :: %(message)s')

display, start_display, add_menu, add_function_to_menu = init_display(backend)

point_1 = gp_Pnt(0, 0, 0)
point_2 = gp_Pnt(10, 0, 0)
point_3 = gp_Pnt(10, 10, 0)
point_list = [point_1, point_2, point_3]

vector_1 = gp_Vec(1, 0, 0)
vector_2 = gp_Vec(0, 1, 0)
vector_3 = gp_Vec(0, 1, 0)
vector_list = [vector_1, vector_2, vector_3]

handle_points_to_bspline = points_to_bspline(point_list)

handle_points = points(point_list, vector_1, vector_3)

handle_points_vectors = points_vectors(point_list, vector_list)

handle_points_no_tangency = points_no_tangency(point_list)

handle_points_no_tangency_closed = points_no_tangency(point_list, closed=True)


display.DisplayShape(Curve.from_handle(handle_points_to_bspline).to_edge())
display.DisplayShape(Curve.from_handle(handle_points).to_edge(),
                     color="BLUE")
display.DisplayShape(Curve.from_handle(handle_points_vectors).to_edge(),
                     color="YELLOW")
display.DisplayShape(Curve.from_handle(handle_points_no_tangency).to_edge(),
                     color="PINK")
display.DisplayShape(Curve.from_handle(handle_points_no_tangency_closed).to_edge(),
                     color="WHITE")
for point in point_list:
    display.DisplayShape(point)
display.FitAll()
start_display()

