# coding: utf-8

r"""wire module of aocutils"""

import logging

from OCC.Core.TopoDS import TopoDS_Wire, TopoDS_Face
from OCC.Core.Approx import Approx_Curve3d
from OCC.Core.BRepAdaptor import BRepAdaptor_CompCurve, BRepAdaptor_HCompCurve
from OCC.Core.GeomAbs import GeomAbs_C2
from OCC.Core.BRepCheck import BRepCheck_Wire, BRepCheck_NoError

from aocutils.brep.base import BaseObject
from aocutils.common import AssertIsDone
from aocutils.tolerance import OCCUTILS_DEFAULT_TOLERANCE
from aocutils.exceptions import WrongTopologicalType

logger = logging.getLogger(__name__)


class Wire(BaseObject):
    r"""Wire class

    Parameters
    ----------
        topods_wire : TopoDS_Wire

    """

    def __init__(self, topods_wire):
        if not isinstance(topods_wire, TopoDS_Wire):
            msg = 'Wire.__init__() needs a TopoDS_Wire, ' \
                  'got a %s' % topods_wire.__class__
            logger.critical(msg)
            raise WrongTopologicalType(msg)
        # assert not topods_wire.IsNull()
        if topods_wire.IsNull():
            msg = "topods_wire is Null"
            logger.error(msg)
            raise ValueError(msg)

        BaseObject.__init__(self, topods_wire, name='topods_wire')

    @property
    def topods_wire(self):
        return self._wrapped_instance

    def check(self):
        r"""Super class abstract method implementation"""
        wire_check = BRepCheck_Wire(self._wrapped_instance)

        # call with Null face
        check_orientation = wire_check.Orientation(TopoDS_Face())

        # Buggy SelfIntersect ?
        # edge_1 = TopoDS_Edge()
        # edge_2 = TopoDS_Edge()
        # check_self_intersect =
        #     wire_check.SelfIntersect(TopoDS_Face(), edge_1, edge_2)

        if check_orientation != BRepCheck_NoError:
            # check_self_intersect != BRepCheck_NoError):
            return False
        else:
            return True

    def to_curve(self,
                 tolerance=OCCUTILS_DEFAULT_TOLERANCE,
                 order=GeomAbs_C2,
                 max_segment=200,
                 max_order=12):
        r"""A wire can consist of many edges.

        These edges are merged given a tolerance and a curve

        Parameters
        ----------
        tolerance : float, optional
        order : GeomAbs_C*, optional
        max_segment : int, optional
        max_order : int, optional

        Returns
        -------
        OCC.Geom.Geom_BSplineCurve

        """
        adap = BRepAdaptor_CompCurve(self._wrapped_instance)
        hadap = BRepAdaptor_HCompCurve(adap)
        approx = Approx_Curve3d(hadap.GetHandle(),
                                tolerance,
                                order,
                                max_segment,
                                max_order)
        with AssertIsDone(approx,
                          'not able to compute approximation from wire'):
            return approx.Curve().GetObject()

    def to_adaptor_3d(self):
        r"""Abstract curve like geom_type into an adaptor3d"""
        return BRepAdaptor_CompCurve(self._wrapped_instance)
