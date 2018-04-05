# coding: utf-8

r"""Extrusion operation"""

from OCC.BRepPrimAPI import BRepPrimAPI_MakePrism

from aocutils.common import AssertIsDone


def extrude(profile, vec):
    r"""Makes a finite prism

    Parameters
    ----------
    profile : TopoDS_Wire
    vec : gp_Vec

    Returns
    -------
    TopoDS_Shape

    """
    pri = BRepPrimAPI_MakePrism(profile, vec, True)
    with AssertIsDone(pri, 'failed building prism'):
        pri.Build()
        return pri.Shape()
