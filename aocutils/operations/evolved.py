# coding: utf-8

r"""operations/evolved.py"""

from OCC.BRepOffsetAPI import BRepOffsetAPI_MakeEvolved

from aocutils.common import AssertIsDone


def evolved(spine, profile):
    r"""Make an evolved shape

    Parameters
    ----------
    spine : TopoDS_Wire
    profile : TopoDS_Wire

    Returns
    -------
    BRepFill_Evolved

    """
    evol = BRepOffsetAPI_MakeEvolved(spine, profile)
    with AssertIsDone(evol, 'failed building evolved'):
        evol.Build()
        return evol.Evolved()
