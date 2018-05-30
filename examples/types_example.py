#!/usr/bin/env python
# coding: utf-8

r"""Types example"""

from __future__ import print_function

from aocutils.primitives import box, sphere
from aocutils.types_ import topo_lut
from aocutils.brep.solid import Solid
# import aocutils.brep.solid_make
from aocutils.topology import Topo


box = box(10, 10, 10)
sphere = sphere(10)

print(type(box))
print(topo_lut[box.ShapeType()])

solid = list(Topo(box).solids)[0]
print(type(solid))
wrapped_solid = Solid(solid)
print(type(wrapped_solid))
