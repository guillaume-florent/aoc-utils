# coding: utf-8

r"""geom surface"""

import logging

from OCC.GeomFill import GeomFill_BSplineCurves, GeomFill_StretchStyle

logger = logging.getLogger(__name__)


class Surface(object):
    r"""Wrapper for a Geom_Surface
    """
    def __init__(self, surface):
        self._surface = surface

    @classmethod
    def from_handle(cls, handle):
        r"""Create the Surface object from a surface handle"""
        # TODO : check handle type
        obj = cls(handle.GetObject())
        return obj

    @property
    def handle(self):
        r"""

        Returns
        -------
        Handle< Geom_Curve >

        """
        return self._surface.GetHandle()

    @classmethod
    def coons(cls, edges):
        r"""Make coons -> Surface

        Parameters
        ----------
        edges : list[OCC.TopoDS.TopoDS_Edge]

        Returns
        -------
        Surface

        """
        if len(edges) == 4:
            spl1, spl2, spl3, spl4 = edges
            srf = GeomFill_BSplineCurves(spl1, spl2, spl3, spl4,
                                         GeomFill_StretchStyle)
        elif len(edges) == 3:
            spl1, spl2, spl3 = edges
            srf = GeomFill_BSplineCurves(spl1, spl2, spl3,
                                         GeomFill_StretchStyle)
        elif len(edges) == 2:
            spl1, spl2 = edges
            srf = GeomFill_BSplineCurves(spl1, spl2, GeomFill_StretchStyle)
        else:
            msg = 'give 2,3 or 4 curves'
            logger.critical(msg)
            raise ValueError(msg)
        return cls.from_handle(srf.Surface())
