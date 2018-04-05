# coding: utf-8

r"""vertex module of aocutils"""

import logging

from OCC.BRep import BRep_Tool
# import OCC.BRepBuilderAPI
from OCC.gp import gp_Pnt2d, gp_Pnt, gp_XYZ, gp_Vec, gp_Dir
# import OCC.TopoDS
# import OCC.TopExp
from OCC.ShapeBuild import ShapeBuild_ReShape
# import OCC.BRepCheck

from aocutils.brep.base import BaseObject
from aocutils.brep.vertex_make import vertex

logger = logging.getLogger(__name__)


class Vertex(BaseObject):
    r"""Wraps gp_Pnt

    Parameters
    ----------
        x
        y
        z
    """
    _n = 0

    def __init__(self, x, y, z):
        self._pnt = gp_Pnt(x, y, z)
        BaseObject.__init__(self,
                            vertex(self._pnt),
                            name='Vertex #{0}'.format(self._n))

        Vertex._n += 1

    @staticmethod
    def from_pnt(cls, pnt):
        r"""Create a Vertex object from a gp_Pnt

        Parameters
        ----------
        cls : Vertex class
        pnt : gp_Pnt

        Returns
        -------
        Vertex
            A new Vertex instance
        """
        x, y, z = pnt.X(), pnt.Y(), pnt.Z()
        return cls(x, y, z)

    @property
    def topods_vertex(self):
        return self._wrapped_instance

    def _update(self):
        """

        """
        # TODO: perhaps should take an argument until which topological level
        # topological entities bound to the vertex should be updated too...
        reshape = ShapeBuild_ReShape()
        reshape.Replace(self._wrapped_instance, vertex(self._pnt))

    @property
    def x(self):
        r"""x coordinate"""
        return self._pnt.X()

    @x.setter
    def x(self, val):
        self._pnt.SetX(val)
        self._update()

    @property
    def y(self):
        r"""y coordinate"""
        return self._pnt.Y()

    @y.setter
    def y(self, val):
        self._pnt.SetY(val)
        self._update()

    @property
    def z(self):
        r"""z coordinate"""
        return self._pnt.Z()

    @z.setter
    def z(self, val):
        self._pnt.SetZ(val)
        self._update()

    @property
    def xyz(self):
        r"""Coordinates as a tuple"""
        return self._pnt.Coord()

    @xyz.setter
    def xyz(self, *val):
        self._pnt.SetXYZ(*val)
        self._update()

    def __repr__(self):
        return self.name

    @property
    def as_vec(self):
        r"""returns a gp_Vec version of self"""
        return gp_Vec(self._pnt.X(), self._pnt.Y(), self._pnt.Z())

    @property
    def as_dir(self):
        r"""returns a gp_Dir version of self"""
        return gp_Dir(self._pnt.X(), self._pnt.Y(), self._pnt.Z())

    @property
    def as_xyz(self):
        r"""returns a gp_XYZ version of self"""
        return gp_XYZ(self._pnt.X(), self._pnt.Y(), self._pnt.Z())

    @property
    def as_pnt(self):
        r"""returns a gp_Pnt version of self"""
        return self._pnt

    @staticmethod
    def to_pnt(vertex):
        r"""Returns a gp_Pnt from a TopoDS_Vertex

        Parameters
        ----------
        vertex : TopoDS_Vertex

        Returns
        -------
        gp_Pnt

        """
        return BRep_Tool.Pnt(vertex)

    @property
    def as_2d(self):
        r"""returns a gp_Pnt2d version of self"""
        return gp_Pnt2d(self._pnt.X(), self._pnt.Y())
