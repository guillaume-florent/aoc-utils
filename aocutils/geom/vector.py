# coding: utf-8

r"""geom vector"""

from __future__ import division

import logging

import numpy as np
from OCC.Core.gp import gp_Pnt, gp_Vec, gp_Dir

from aocutils.tolerance import OCCUTILS_DEFAULT_TOLERANCE
from aocutils.exceptions import ZeroNormVectorException
from aocutils.geom._three_d import ThreeD

logger = logging.getLogger(__name__)


class Vector(ThreeD):
    r"""3D vector

    Can be constructed from 3 parameters or from a tuple of length 3

    Examples
    --------
    """
    @classmethod
    def from_points(cls, start, end):
        r"""Create the vector from 2 points

        Parameters
        ----------
        start : Point
        end : Point
        """
        obj = cls()
        obj._x = end.X() - start.X()
        obj._y = end.Y() - start.Y()
        obj._z = end.Z() - start.Z()
        return obj

    @classmethod
    def from_gp_vec(cls, gp_vec):
        obj = cls()
        obj._x = gp_vec.X()
        obj._y = gp_vec.Y()
        obj._z = gp_vec.Z()
        return obj

    @property
    def gp_vec(self):
        return gp_Vec(self.X(), self.Y(), self.Z())

    @property
    def norm(self):
        return (self.X()**2 + self.Y()**2 + self.Z()**2)**.5

    def to_array(self):
        r"""Convert the vector to an array"""
        return [self.X(), self.Y(), self.Z()]

    def perpendicular(self, other):
        r"""Vector perpendicular to self and other

        Parameters
        ----------
        other : Vector
            The other vector used to compute the perpendicular
        """
        if other.norm == 0 or self.norm == 0:
            raise ZeroNormVectorException

        return Vector.from_tuple(np.cross(self.to_array(), other.to_array()))

    def __add__(self, other):
        r"""Add a vector to self

        Parameters
        ----------
        other : gp_Vec or Vector

        Returns
        -------
        Vector

        """
        return Vector.from_xyz(self.X() + other.X(),
                               self.Y() + other.Y(),
                               self.Z() + other.Z())

    def __sub__(self, other):
        r"""Substract a vector to self

        Parameters
        ----------
        other : gp_Vec or Vector

        Returns
        -------
        Vector

        """
        return Vector.from_xyz(self.X() - other.X(),
                               self.Y() - other.Y(),
                               self.Z() - other.Z())

    def __mul__(self, scalar):
        r"""Multiply a vector by a scalar

        Parameters
        ----------
        scalar : float

        Returns
        -------
        Vector

        """
        return Vector.from_xyz(self.X() * scalar,
                               self.Y() * scalar,
                               self.Z() * scalar)

    def __truediv__(self, scalar):
        r"""Multiply a vector by a scalar

        Parameters
        ----------
        scalar : float

        Returns
        -------
        Vector

        """
        return Vector.from_xyz(self.X() / scalar,
                               self.Y() / scalar,
                               self.Z() / scalar)

    def __div__(self, scalar):
        r"""PY2 compatibility"""
        return self.__truediv__(scalar)

    def __eq__(self, other):
        r"""Is self equal to other?

        Parameters
        ----------
        other : gp_Pnt or Point

        Returns
        -------
        bool

        """
        if isinstance(other, Vector):
            return self.gp_vec.IsEqual(other.gp_vec, OCCUTILS_DEFAULT_TOLERANCE)
        elif isinstance(other, gp_Pnt):
            return self.gp_vec.IsEqual(other, OCCUTILS_DEFAULT_TOLERANCE)
        else:
            msg = "Incompatible vector geom_type for comparison"
            logger.critical(msg)
            raise TypeError(msg)

    def to_dir(self):
        r"""Convert a gp_Vec to a gp_Dir

        Returns
        -------
        gp_Dir

        """
        return gp_Dir(self.gp_vec)
