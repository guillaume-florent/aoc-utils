#!/usr/bin/env python
# coding: utf-8

r"""pretty_print examples"""


from __future__ import print_function

import math

from OCC.Core.gp import gp_Pnt, gp_Vec, gp_Dir, gp_Ax1, gp_Trsf

from aocutils.primitives import box
from aocutils.pretty_print import gp_pnt_print, gp_vec_print, gp_ax1_print, \
    gp_trsf_print, dump_topology

point = gp_Pnt(1, 2, 3)
print(gp_pnt_print(point))

vec = gp_Vec(1, 2, 3)
print(gp_vec_print(vec))

direction = gp_Dir(1, 2, 3)
ax1 = gp_Ax1(point, direction)
print(gp_ax1_print(ax1))


trsf = gp_Trsf()
trsf.SetTranslation(vec)
print(gp_trsf_print(trsf))

trsf.SetRotation(ax1, math.radians(180))
print(gp_trsf_print(trsf))

box_shape = box(10, 10, 10)
dump_topology(box_shape)
