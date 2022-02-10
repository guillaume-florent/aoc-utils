# coding: utf-8

r"""Sewing operation"""

import logging

try:
    from OCC.BRepBuilderAPI import BRepBuilderAPI_Sewing
except (ImportError, ModuleNotFoundError):
    from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_Sewing

from aocutils.topology import shape_to_topology

logger = logging.getLogger(__name__)


def sew_shapes(shapes, tolerance=1e-3):
    r"""Sew shapes

    Parameters
    ----------
    shapes : list[OCC.TopoDS.TopoDS_Shape]
    tolerance : float

    Returns
    -------
    OCC.TopoDS.TopoDS_*

    """
    sew = BRepBuilderAPI_Sewing(tolerance)
    for shp in shapes:
        if isinstance(shp, list):
            for i in shp:
                sew.Add(i)
        else:
            sew.Add(shp)
    sew.Perform()
    logger.info('%i degenerated shapes' % sew.NbDegeneratedShapes())
    logger.info('%i deleted faces:' % sew.NbDeletedFaces())
    logger.info('%i free edges' % sew.NbFreeEdges())
    logger.info('%i multiple edges:' % sew.NbMultipleEdges())

    return shape_to_topology(sew.SewedShape())
