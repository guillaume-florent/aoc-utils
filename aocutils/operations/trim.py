# coding: utf-8

r"""Trim operation"""

import warnings
import logging

from OCC.Geom import Geom_TrimmedCurve

from aocutils.brep.edge_make import edge
from aocutils.brep.wire import Wire
from aocutils.operations.project import point_on_curve


logger = logging.getLogger(__name__)


def trim_wire(wire, shape_limit_1, shape_limit_2, periodic=False):
    r"""Trim wire

    Parameters
    ----------
    wire : OCC.TopoDS.TopoDS_Wire
    shape_limit_1
    shape_limit_2
    periodic

    Returns
    -------
    TopoDS_Edge
        the trimmed wire that lies between `shapeLimit1` and `shapeLimit2`

    """
    adap = Wire(wire).to_adaptor_3d()
    bspl = adap.BSpline()

    if periodic:
        spl = bspl.GetObject()
        if spl.IsClosed():
            spl.SetPeriodic()
        else:
            msg = "the wire to be trimmed is not closed, " \
                  "hence cannot be made periodic"
            logger.warning(msg)
            warnings.warn(msg)

    p1 = point_on_curve(bspl, shape_limit_1)[0]
    p2 = point_on_curve(bspl, shape_limit_2)[0]
    a, b = sorted([p1, p2])
    tr = Geom_TrimmedCurve(bspl, a, b).GetHandle()
    return edge(tr)
