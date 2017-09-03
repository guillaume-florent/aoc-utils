# coding: utf-8

r"""operations/evolved.py"""

import OCC.BRepOffsetAPI

from aocutils.common import AssertIsDone


def evolved(spine, profile):
    r"""Make an evolved shape

    Parameters
    ----------
    spine : OCC.TopoDS.TopoDS_Wire
    profile : OCC.TopoDS.TopoDS_Wire

    Returns
    -------
    BRepFill_Evolved

    """
    evol = OCC.BRepOffsetAPI.BRepOffsetAPI_MakeEvolved(spine, profile)
    with AssertIsDone(evol, 'failed building evolved'):
        evol.Build()
        return evol.Evolved()
