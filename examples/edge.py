#!/usr/bin/env python
# coding: utf-8

r"""edge.py module example use

Box -> Topology -> 1 edge -> edge tolerance

"""

from __future__ import print_function

from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox, BRepPrimAPI_MakeSphere
from OCC.Display.SimpleGui import init_display

from aocutils.brep.edge import Edge
from aocutils.topology import Topo
from aocutils.display.defaults import backend
# import aocutils.display.display

display, start_display, add_menu, add_function_to_menu = init_display(backend)


if __name__ == '__main__':
    box = BRepPrimAPI_MakeBox(10, 20, 30).Shape()
    box_topology = Topo(box)
    first_edge = next(box_topology.edges)
    occutils_wrapped_edge = Edge(first_edge)

    sphere = BRepPrimAPI_MakeSphere(10).Shape()
    sphere_topology = Topo(sphere, return_iter=False)
    print(sphere_topology.number_of_edges)
    edges = sphere_topology.edges
    edge_sphere_0 = edges[0]
    edge_sphere_1 = edges[1]
    edge_sphere_2 = edges[2]
    wrapped_edge_sphere = Edge(edge_sphere_1)

    print(occutils_wrapped_edge.tolerance)
    display.DisplayShape(edge_sphere_1)
    display.DisplayShape(wrapped_edge_sphere.parameter_to_point(5.))
    display.DisplayShape(wrapped_edge_sphere.parameter_to_point(6.))
    # occutils.display.display.Display("wx").display_shape(first_edge)
    # occutils.display.display.Display("wx").display_shape(first_edge_sphere)
    display.FitAll()
    start_display()
