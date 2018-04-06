#!/usr/bin/env python
# coding: utf-8

r"""face.py module example use"""

from __future__ import print_function

from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeSphere

from aocutils.brep.face import Face


# BRepPrimAPI_MakeSphere(<params>).Face() in inherited
# from BRepPrimAPI_MakeOneAxis
# Face() returns the lateral face of the rotational primitive.
sphere_face = BRepPrimAPI_MakeSphere(1, 1).Face()
aoutils_wrapped_sphere_face = Face(sphere_face)

print(aoutils_wrapped_sphere_face.topo)
print(aoutils_wrapped_sphere_face.topo_type)
print(aoutils_wrapped_sphere_face.is_trimmed)
print(aoutils_wrapped_sphere_face.is_valid)
print(aoutils_wrapped_sphere_face.is_planar())
