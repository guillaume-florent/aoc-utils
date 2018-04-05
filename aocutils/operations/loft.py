# coding: utf-8

r"""Loft operation"""

import logging

from OCC.BRepOffsetAPI import BRepOffsetAPI_ThruSections
from OCC.GeomAbs import GeomAbs_C2
from OCC.TopoDS import TopoDS_Wire, TopoDS_Vertex

from aocutils.common import AssertIsDone
from aocutils.topology import shape_to_topology
from aocutils.tolerance import OCCUTILS_DEFAULT_TOLERANCE

logger = logging.getLogger(__name__)


def loft(elements,
         ruled=False,
         tolerance=OCCUTILS_DEFAULT_TOLERANCE,
         continuity=GeomAbs_C2,
         check_compatibility=True):
    r"""Loft

    Parameters
    ----------
    elements
    ruled : bool
    tolerance : float
    continuity : GeomAbs_C*, optional
        (the default is GeomAbs_C2)
    check_compatibility : bool

    Returns
    -------
    TopoDS_*

    """
    sections = BRepOffsetAPI_ThruSections(False, ruled, tolerance)
    for i in elements:
        if isinstance(i, TopoDS_Wire):
            sections.AddWire(i)
        elif isinstance(i, TopoDS_Vertex):
            sections.AddVertex(i)
        else:
            msg = "elements is a list of TopoDS_Wire or TopoDS_Vertex, " \
                  "found a %s " % i.__class__
            logger.error(msg)
            raise TypeError(msg)

    sections.CheckCompatibility(check_compatibility)
    sections.SetContinuity(continuity)
    sections.Build()
    with AssertIsDone(sections, 'failed lofting'):
        # te = occutils.topology.shape_to_topology()
        return shape_to_topology(sections.Shape())
