# coding: utf-8

r"""Offset operations"""

import logging

import OCC.BRepOffset
import OCC.BRepOffsetAPI
import OCC.GeomAbs

from aocutils.exceptions import OffsetShapeException
from aocutils.topology import shape_to_topology
from aocutils.tolerance import OCCUTILS_DEFAULT_TOLERANCE

logger = logging.getLogger(__name__)


def offset_shape(shape_to_offset,
                 offset_distance,
                 tolerance=OCCUTILS_DEFAULT_TOLERANCE,
                 offset_mode=OCC.BRepOffset.BRepOffset_Skin,
                 intersection=False,
                 selfintersection=False,
                 join_type=OCC.GeomAbs.GeomAbs_Arc):
    r"""Builds an offset shell from a shape construct
    an offset version of the shape

    Parameters
    ----------
    shape_to_offset
    offset_distance : float
    tolerance : float
    offset_mode : OCC.BRepOffset.BRepOffset_*, optional
        (the default is OCC.BRepOffset.BRepOffset_Skin)
    intersection : bool
    selfintersection : bool
    join_type : OCC.GeomAbs.GeomAbs_*
        (the default is OCC.GeomAbs.GeomAbs_Arc)

    Returns
    -------
    OCC.TopoDS.TopoDS_Shape

    """
    try:
        an_offset = OCC.BRepOffsetAPI.BRepOffsetAPI_MakeOffsetShape(shape_to_offset,
                                                                    offset_distance,
                                                                    tolerance,
                                                                    offset_mode,
                                                                    intersection,
                                                                    selfintersection,
                                                                    join_type)
        if an_offset.IsDone():
            return an_offset.Shape()
        else:
            msg = "Offset shape not done"
            logger.error(msg)
            raise OffsetShapeException(msg)
    except RuntimeError:
        msg = "Failed to offset shape"
        logger.error(msg)
        raise OffsetShapeException(msg)


def offset(wire_or_face,
           offset_distance,
           altitude=0,
           join_type=OCC.GeomAbs.GeomAbs_Arc):
    r"""Builds a offset wire or face from a wire or face
    construct an offset version of the shape

    Parameters
    ----------
    wire_or_face
        the wire or face to offset
    offset_distance : float
        the distance to offset
    altitude : float
        move the offset shape to altitude from the normal of the wire or face
    join_type
        the geom_type of offset you want can be one of
        OCC.GeomAbs.GeomAbs_Arc, OCC.GeomAbs.GeomAbs_Tangent,
        OCC.GeomAbs.GeomAbs_Intersection

    Returns
    -------
    OCC.TopoDS.TopoDS_Shape

    Notes
    -----
    A shape that has a negative offsetDistance will return a sharp corner

    """
    _joints = [OCC.GeomAbs.GeomAbs_Arc,
               OCC.GeomAbs.GeomAbs_Tangent,
               OCC.GeomAbs.GeomAbs_Intersection]
    # assert join_type in _joints, '%s is not one of %s' % (join_type, _joints)
    if join_type not in _joints:
        msg = '%s is not one of %s' % (join_type, _joints)
        logger.error(msg)
        raise ValueError(msg)
    try:
        an_offset = OCC.BRepOffsetAPI.BRepOffsetAPI_MakeOffset(wire_or_face,
                                                               join_type)
        an_offset.Perform(offset_distance, altitude)
        if an_offset.IsDone():
            return shape_to_topology(an_offset.Shape())
        else:
            msg = "offset not done"
            logger.error(msg)
            raise OffsetShapeException(msg)
    except RuntimeError:
        msg = "failed to offset"
        logger.error(msg)
        raise OffsetShapeException(msg)
