# coding: utf-8

r"""Methods to make a vertex"""

import functools
import logging

from OCC.BRepBuilderAPI import BRepBuilderAPI_MakeVertex
from OCC.TopoDS import TopoDS_Vertex
from OCC.TopExp import topexp_CommonVertex

from aocutils.common import AssertIsDone
from aocutils.exceptions import NoCommonVertexException

logger = logging.getLogger(__name__)


@functools.wraps(BRepBuilderAPI_MakeVertex)
def vertex(*args):
    r"""Make a TopoDS_Vertex

    Parameters
    ----------
    args

    Returns
    -------
    TopoDS_Vertex

    """
    vert = BRepBuilderAPI_MakeVertex(*args)
    with AssertIsDone(vert, 'failed to produce vertex'):
        result = vert.Vertex()
        vert.Delete()
        return result


def common_vertex(edg1, edg2):
    r"""Common vertex of 2 edges

    Parameters
    ----------
    edg1 : TopoDS_Edge
    edg2 : TopoDS_Edge

    Returns
    -------
    TopoDS_Vertex
        The common vertex of 2 edges

    """
    vert = TopoDS_Vertex()
    if topexp_CommonVertex(edg1, edg2, vert):
        return vert
    else:
        msg = "No common vertex found"
        logger.error(msg)
        raise NoCommonVertexException(msg)
