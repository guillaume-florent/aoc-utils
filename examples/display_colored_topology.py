#!/usr/bin/env python
# coding: utf-8

r"""
"""

import logging

from OCC.BRepPrimAPI import BRepPrimAPI_MakeBox, BRepPrimAPI_MakeSphere
from OCC.Display.SimpleGui import init_display
from OCC.gp import gp_Pnt
from OCC.TopoDS import TopoDS_Compound
from OCC.BRep import BRep_Builder

from aocutils.display.defaults import backend
# import aocutils.display.display
from aocutils.display.color import spectral_color_sequence
from aocutils.display.topology import faces, edges, wires, solids
from aocutils.mesh import mesh

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s :: %(levelname)6s :: %(module)20s :: '
                           '%(lineno)3d :: %(message)s')

backend = backend
display, start_display, add_menu, add_function_to_menu = init_display(backend)

box_x_dim = 10.
box_y_dim = 20.
box_z_dim = 30.


def box_shape():
    r"""Box shape for testing as a pytest fixture"""
    return BRepPrimAPI_MakeBox(box_x_dim, box_y_dim, box_z_dim).Shape()


def sphere_shape():
    r"""Box shape for testing as a pytest fixture"""
    shape = BRepPrimAPI_MakeSphere(gp_Pnt(50, 0, 0), 10).Shape()
    mesh(shape)
    return shape


def compound():
    r"""Create and return a compound from box and sphere"""
    # Create a compound
    compound = TopoDS_Compound()
    builder = BRep_Builder()
    builder.MakeCompound(compound)
    # Populate the compound
    builder.Add(compound, box_shape())
    builder.Add(compound, sphere_shape())
    return compound


def box_faces(event=None):
    display.EraseAll()
    # display.GetView().GetObject().SetBackgroundColor(white)
    faces(display, box_shape())
    display.FitAll()


def box_edges(event=None):
    display.EraseAll()
    # display.GetView().GetObject().SetBackgroundColor(white)
    edges(display, box_shape(), width=6)
    display.FitAll()


def box_wires(event=None):
    display.EraseAll()
    # display.GetView().GetObject().SetBackgroundColor(white)
    wires(display, box_shape(), width=6)
    display.FitAll()


def sphere_faces(event=None):
    display.EraseAll()
    # display.GetView().GetObject().SetBackgroundColor(white)
    faces(display, sphere_shape(),
                                    color_sequence=spectral_color_sequence)
    display.FitAll()


def sphere_edges(event=None):
    display.EraseAll()
    # display.GetView().GetObject().SetBackgroundColor(white)
    edges(display, sphere_shape(), width=6,
                                    color_sequence=spectral_color_sequence)
    display.FitAll()


def compound_solids(event=None):
    display.EraseAll()
    solids(display, compound(), color_sequence=spectral_color_sequence)
    display.FitAll()


add_menu('box')
add_function_to_menu('box', box_edges)
add_function_to_menu('box', box_faces)
add_function_to_menu('box', box_wires)
add_menu('sphere')
add_function_to_menu('sphere', sphere_edges)
add_function_to_menu('sphere', sphere_faces)
add_menu('compound')
add_function_to_menu('compound', compound_solids)
start_display()
