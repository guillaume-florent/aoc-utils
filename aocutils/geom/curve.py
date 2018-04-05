# coding: utf-8

r"""geom curve"""

import logging

from OCC.Geom import Geom_Curve
from OCC.GeomAdaptor import GeomAdaptor_Curve
# import OCC.Approx
# import OCC.BRepAdaptor
from OCC.GeomAbs import GeomAbs_C1
from OCC.GeomConvert import GeomConvert_ApproxCurve

from aocutils.common import AssertIsDone
from aocutils.tolerance import OCCUTILS_DEFAULT_TOLERANCE
from aocutils.brep.edge_make import edge
from aocutils.exceptions import WrongTopologicalType

logger = logging.getLogger(__name__)


class Curve(object):
    r"""
    _curve is a Geom_Curve (or subclass)
    """
    def __init__(self, curve):
        if not issubclass(curve.__class__, Geom_Curve):
            msg = 'Curve.__init__() needs a Geom_Curve or a subclass, ' \
                  'got a %s' % curve.__class__
            logger.critical(msg)
            raise WrongTopologicalType(msg)
        self._curve = curve

    @classmethod
    def from_handle(cls, handle):
        r"""Initialize from the handle

        Parameters
        ----------
        handle

        """
        # obj = cls()
        # obj._curve = handle.GetObject()
        return cls(handle.GetObject())

    @property
    def handle(self):
        r"""

        Returns
        -------
        Handle< Geom_Curve >

        """
        return self._curve.GetHandle()

    def to_edge(self):
        return edge(self.handle)

    def to_bspline(self,
                   tolerance=OCCUTILS_DEFAULT_TOLERANCE,
                   continuity=GeomAbs_C1,
                   sections=300,
                   degree=12):
        r"""Convert a curve to a bspline

        Parameters
        ----------
        tolerance : float
        continuity : GeomAbs_C*, optional
            (the default is GeomAbs_C1)
        sections : int
        degree : int

        Returns
        -------
        Handle< Geom_BSplineCurve >

        """
        approx_curve = GeomConvert_ApproxCurve(self.handle,
                                               tolerance,
                                               continuity,
                                               sections,
                                               degree)
        with AssertIsDone(approx_curve, 'could not compute bspline from curve'):
            return approx_curve.Curve()

    def to_adaptor_3d(self):
        r"""Abstract curve like geom_type into an adaptor3d

        Returns
        -------
        GeomAdaptor_Curve

        """
        return GeomAdaptor_Curve(self._curve.GetHandle())
