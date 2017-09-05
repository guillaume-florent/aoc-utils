# coding: utf-8

r"""Inclusion of points in bounding box and in solid"""

import logging

from OCC.BRepClass3d import BRepClass3d_SolidClassifier
from OCC.TopAbs import TopAbs_ON, TopAbs_OUT, TopAbs_IN

from aocutils.analyze.bounds import BoundingBox
from aocutils.types import topo_lut
from aocutils.exceptions import WrongTopologicalType
from aocutils.tolerance import OCCUTILS_DEFAULT_TOLERANCE

logger = logging.getLogger(__name__)


def point_in_boundingbox(shape, pnt, tolerance=OCCUTILS_DEFAULT_TOLERANCE):
    r"""Is pnt inside the bounding box of solid?

    This is a much speedier test than checking the TopoDS_Solid

    Parameters
    ----------
    shape : TopoDS_Shape
    pnt : OCC.gp.gp_Pnt
    tolerance : float

    Returns
    -------
    bool
        True if pnt lies in boundingbox, False otherwise

    """
    return not BoundingBox(shape, tolerance).bnd_box.IsOut(pnt)


def point_in_solid(shape, pnt, tolerance=OCCUTILS_DEFAULT_TOLERANCE):
    r"""Is pnt inside solid?

    Parameters
    ----------
    shape : TopoDS_*
    pnt : OCC.gp.gp_Pnt
    tolerance : float

    Returns
    -------
    bool
        True if pnt lies in solid, False otherwise

    """
    if topo_lut[shape.ShapeType()] not in ["compound",
                                           "compsolid",
                                           "solid",
                                           "shell"]:
        msg = "Cannot evaluate in/out position of a point in a 2D or less shape"
        logger.error(msg)
        raise WrongTopologicalType(msg)

    _in_solid = BRepClass3d_SolidClassifier(shape, pnt, tolerance)
    logger.info('State : %s' % str(_in_solid.State()))
    if _in_solid.State() == TopAbs_ON:
        return None
    if _in_solid.State() == TopAbs_OUT:
        return False
    if _in_solid.State() == TopAbs_IN:
        return True
