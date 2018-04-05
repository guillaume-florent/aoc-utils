# coding: utf-8

r"""Pipe operation"""

from OCC.BRepOffsetAPI import BRepOffsetAPI_MakePipe

from aocutils.common import AssertIsDone


def pipe(spine, profile):
    r"""Make a pipe

    Parameters
    ----------
    spine : OCC.TopoDS.TopoDS_Wire
    profile : OCC.TopoDS.TopoDS_Wire

    Returns
    -------
    OCC.TopoDS.TopoDS_Shape

    """
    a_pipe = BRepOffsetAPI_MakePipe(spine, profile)
    with AssertIsDone(a_pipe, 'failed building pipe'):
        a_pipe.Build()
        return a_pipe.Shape()
