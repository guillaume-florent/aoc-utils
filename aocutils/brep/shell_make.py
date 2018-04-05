# coding: utf-8

r"""Methods to make a shell"""

import functools
import logging

from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeShell
from OCC.Core.TopoDS import TopoDS_Builder, TopoDS_Shell
# import OCC.ShapeAnalysis

from aocutils.common import AssertIsDone
from aocutils.topology import shape_to_topology
from aocutils.exceptions import BRepBuildingException

logger = logging.getLogger(__name__)


@functools.wraps(BRepBuilderAPI_MakeShell)
def shell(*args):
    r"""Make a TopoDS_Shell

    Parameters
    ----------
    args

    Returns
    -------
    TopoDS_Shell

    Notes
    -----
    BRepBuilderAPI_MakeShell (const Handle< Geom_Surface > &S,
                              const Standard_Boolean Segment=Standard_False)
    BRepBuilderAPI_MakeShell (const Handle< Geom_Surface > &S,
                              const Standard_Real UMin, const Standard_Real UMax,
                              const Standard_Real VMin, const Standard_Real VMax,
                              const Standard_Boolean Segment=Standard_False)

    """
    a_shell = BRepBuilderAPI_MakeShell(*args)
    with AssertIsDone(a_shell, 'failed to produce shell'):
        result = a_shell.Shell()
        a_shell.Delete()
        return shape_to_topology(result)


def shell_from_faces(list_of_faces):
    r"""

    Parameters
    ----------
    list_of_faces : list[TopoDS_Face]
                    or
                    list[TopoDS_Shape] where the shapes
                    have a TopAbs_FACE type

    Returns
    -------
    TopoDS_Shell

    """
    if len(list_of_faces) == 0:
        msg = "Cannot build a shell from 0 face"
        logger.error(msg)
        raise BRepBuildingException(msg)

    builder = TopoDS_Builder()
    a_shell = TopoDS_Shell()
    builder.MakeShell(a_shell)
    for face in list_of_faces:
        builder.Add(a_shell, face)
    return a_shell
