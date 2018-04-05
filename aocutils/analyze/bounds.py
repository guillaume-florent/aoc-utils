# coding: utf-8

r"""Bounding box analysis"""

import abc
import logging
import re
import struct

from OCC.Core.Bnd import Bnd_Box
from OCC.Core.BRepBndLib import brepbndlib_Add
from OCC.Core.gp import gp_Pnt
from OCC.Core.TopoDS import TopoDS_Shape

from corelib.core.files import is_binary

from aocutils.brep.face_make import from_points
from aocutils.geom.point import Point
from aocutils.tolerance import OCCUTILS_DEFAULT_TOLERANCE
from aocutils.exceptions import WrongTopologicalType
from aocutils.operations.boolean import common
from aocutils.topology import Topo


logger = logging.getLogger(__name__)


class AbstractBoundingBox(object):
    r"""Abstract representation of a bounding box"""
    __metaclass__ = abc.ABCMeta

    # @abc.abstractproperty
    @property
    @abc.abstractmethod
    def x_min(self):
        r"""Minimum x"""
        raise NotImplementedError

    # @abc.abstractproperty
    @property
    @abc.abstractmethod
    def x_max(self):
        r"""Maximum x"""
        raise NotImplementedError

    # @abc.abstractproperty
    @property
    @abc.abstractmethod
    def y_min(self):
        r"""Minimum y"""
        raise NotImplementedError

    # @abc.abstractproperty
    @property
    @abc.abstractmethod
    def y_max(self):
        r"""Maximum y"""
        raise NotImplementedError

    # @abc.abstractproperty
    @property
    @abc.abstractmethod
    def z_min(self):
        r"""Minimum z"""
        raise NotImplementedError

    # @abc.abstractproperty
    @property
    @abc.abstractmethod
    def z_max(self):
        r"""Maximum z"""
        raise NotImplementedError

    # @abc.abstractproperty
    @property
    @abc.abstractmethod
    def x_span(self):
        r"""Dimension along the X axis"""
        raise NotImplementedError

    # @abc.abstractproperty
    @property
    @abc.abstractmethod
    def y_span(self):
        r"""Dimension along the Y axis"""
        raise NotImplementedError

    # @abc.abstractproperty
    @property
    @abc.abstractmethod
    def z_span(self):
        r"""Dimension along the Z axis"""
        raise NotImplementedError

    # @abc.abstractproperty
    @property
    @abc.abstractmethod
    def max_dimension(self):
        r"""Maximum dimension along any of the X Y Z axis"""
        raise NotImplementedError

    # @abc.abstractproperty
    @property
    @abc.abstractmethod
    def min_dimension(self):
        r"""Minimum dimension along any of the X Y Z axis"""
        raise NotImplementedError

    # @abc.abstractproperty
    @property
    @abc.abstractmethod
    def aspect_ratio(self):
        r"""Aspect ratio"""
        raise NotImplementedError

    # @abc.abstractproperty
    @property
    @abc.abstractmethod
    def as_tuple(self):
        r"""bounding box as the original tuple"""
        raise NotImplementedError

    # @abc.abstractproperty
    @property
    @abc.abstractmethod
    def centre(self):
        r"""Centre of the bounding box"""
        raise NotImplementedError


class BoundingBox(AbstractBoundingBox):
    r"""Wrapper class for a bounding box

    Notes
    -----
    Mesh the shape before instantiating a BoundingBox if required,
    infinite recursion would be created by calling mesh.py's mesh() method

    """
    def __init__(self, shape, tol=OCCUTILS_DEFAULT_TOLERANCE):
        if isinstance(shape, TopoDS_Shape) or issubclass(shape.__class__,
                                                         TopoDS_Shape):
            self._shape = shape
        else:
            msg = "Expecting a TopoDS_Shape (or a subclass), " \
                  "got a %s" % str(shape.__class__)
            logger.error(msg)
            raise WrongTopologicalType(msg)
        # self._shape = shape
        self._tol = tol
        self._bbox = Bnd_Box()
        self._bbox.SetGap(tol)
        brepbndlib_Add(self._shape, self._bbox)

        (self._x_min, self._y_min, self._z_min,
         self._x_max, self._y_max, self._z_max) = self._bbox.Get()

    @property
    def x_min(self):
        r"""Minimum x"""
        return self._x_min

    @property
    def x_max(self):
        r"""Maximum x"""
        return self._x_max

    @property
    def y_min(self):
        r"""Minimum y"""
        return self._y_min

    @property
    def y_max(self):
        r"""Maximum y"""
        return self._y_max

    @property
    def z_min(self):
        r"""Minimum z"""
        return self._z_min

    @property
    def z_max(self):
        r"""Maximum z"""
        return self._z_max

    @property
    def bnd_box(self):
        r"""The OCC bounding box object

        Returns
        -------
        OCC.Bnd.Bnd_Box

        """
        return self._bbox

    @property
    def x_span(self):
        r"""x dimension of bounding box"""
        return self.x_max - self.x_min

    @property
    def y_span(self):
        r"""y dimension of bounding box"""
        return self.y_max - self.y_min

    @property
    def z_span(self):
        r"""z dimension of bounding box"""
        return self.z_max - self.z_min

    @property
    def max_dimension(self):
        r"""Maximum dimension"""
        return max([self.x_span, self.y_span, self.z_span])

    @property
    def min_dimension(self):
        r"""Minimum dimension"""
        return min([self.x_span, self.y_span, self.z_span])

    @property
    def aspect_ratio(self):
        r"""Aspect ratio"""
        return self.max_dimension / self.min_dimension

    @property
    def as_tuple(self):
        r"""bounding box as the original tuple"""
        return (self.x_min, self.y_min, self.z_min,
                self.x_max, self.y_max, self.z_max)

    @property
    def centre(self):
        r"""Centre of the bounding box

        Returns
        -------
        gp_Pnt

        """
        return Point.midpoint(gp_Pnt(self.x_min, self.y_min, self.z_min),
                              gp_Pnt(self.x_max, self.y_max, self.z_max))


def build_plane_at_x(x, shape):
    r"""Build a plane for intersection with the shape at x. This is a YZ plane.

    Parameters
    ----------
    x : float
        The x coordinate at which the plane is to be built
    shape : OCC shape

    Returns
    -------
    Face
        The face representing the plane

    """
    bounding_box = BoundingBox(shape)
    extra = 1.
    p1 = gp_Pnt(float(x),
                bounding_box.y_max + extra,
                bounding_box.z_max + extra)
    p2 = gp_Pnt(float(x),
                bounding_box.y_min - extra,
                bounding_box.z_max + extra)
    p3 = gp_Pnt(float(x),
                bounding_box.y_min - extra,
                bounding_box.z_min - extra)
    p4 = gp_Pnt(float(x),
                bounding_box.y_max + extra,
                bounding_box.z_min - extra)
    face = from_points([p1, p2, p3, p4])
    return face


def build_plane_at_y(y, shape):
    r"""Build a plane for intersection with the shape at y. This is a XZ plane.

    Parameters
    ----------
    y : float
        The x coordinate at which the plane is to be built
    shape : OCC shape

    Returns
    -------
    Face
        The face representing the plane

    """
    bounding_box = BoundingBox(shape)
    extra = 1.
    p1 = gp_Pnt(bounding_box.x_max + extra,
                float(y),
                bounding_box.z_max + extra)
    p2 = gp_Pnt(bounding_box.x_min - extra,
                float(y),
                bounding_box.z_max + extra)
    p3 = gp_Pnt(bounding_box.x_min - extra,
                float(y),
                bounding_box.z_min - extra)
    p4 = gp_Pnt(bounding_box.x_max + extra,
                float(y),
                bounding_box.z_min - extra)
    face = from_points([p1, p2, p3, p4])
    return face


def build_plane_at_z(z, shape):
    r"""Build a plane for intersection with the shape at z. This is a XY plane.

    Parameters
    ----------
    z : float
        The x coordinate at which the plane is to be built
    shape : OCC shape

    Returns
    -------
    Face
        The face representing the plane

    """
    bounding_box = BoundingBox(shape)
    extra = 1.
    p1 = gp_Pnt(bounding_box.x_max + extra,
                bounding_box.y_max + extra,
                float(z))
    p2 = gp_Pnt(bounding_box.x_max + extra,
                bounding_box.y_min - extra,
                float(z))
    p3 = gp_Pnt(bounding_box.x_min - extra,
                bounding_box.y_min - extra,
                float(z))
    p4 = gp_Pnt(bounding_box.x_min - extra,
                bounding_box.y_max + extra,
                float(z))
    face = from_points([p1, p2, p3, p4])
    return face


def real_bb_position(axis, side, start_position, shape, increment=0.01):
    r"""Workaround for OCC bounding box imprecision.

    The principle is to move a plane (perpendicular to axis) closer and closer
    until it intersects the shape.
    The goal is to get a 'sure to intersect' coordinates for another program.

    Parameters
    ----------
    axis : str
        in ["X", "Y", "Z"]
    side : str, in ["MIN", "MAX"]
        The side from which we try to intersect the shape
    start_position : float
    shape : OCC Shape
    increment : float, optional
        The distance by which the intersection plane
        is moved to try to intersect the shape
        Default is 0.01

    Returns
    -------
    float
        The value of the position
        for the specified axis and side ("MIN" or "MAX")

    """
    if axis not in ["X", "Y", "Z"]:
        raise ValueError("axis must be 'X', 'Y' or 'Z'")
    if side not in ["MIN", "MAX"]:
        raise ValueError("side must be 'MIN' or 'MAX'")

    plane_builders = {"X": build_plane_at_x,
                      "Y": build_plane_at_y,
                      "Z": build_plane_at_z}
    plane_builder = plane_builders[axis]

    position = start_position

    intersect = False
    while intersect is False:
        plane = plane_builder(position, shape)
        common_shape = common(shape, plane)
        list_vertex = Topo(common_shape, return_iter=False).vertices
        if len(list_vertex) >= 1:
            intersect = True
        else:
            if side == "MIN":
                position += increment
            elif side == "MAX":
                position -= increment

    # Bug correction : make sure the computed bounding box is wider
    # than the shape by a value between 0 and increment
    if side == "MIN":
        return position - 2 * increment
    elif side == "MAX":
        return position + 2 * increment


class BetterBoundingBox(AbstractBoundingBox):
    r"""A bounding box implementation that yields results
    that are closer to the truth.

    This implementation is much slower than BoundingBox but more precise.

    The BoundingBox is used as a starting point
    for a more precise determination of the bounds.

    Notes
    -----
    The OCC bounding box is always wider or equal to the real bounding box.
    Hence the need for a workaround.
    The bounding box workaround is useful for complex shapes,
    not for simple primitives like sphere, box ...

    Potential improvements
    ----------------------
    The algorithm could be faster by using dichotomy rather than linear movement
    of the plane that is tested for intersection with the shape
    The improvement would be useful if this workaround is to be used
    in waterline
    When used to generate hull offsets, BetterBoundingBox is slow when the
    increment is smaller than 10e-2 but we can live with it in the meantime

    Parameters
    ----------
    shape : OCC.TopoDS.TopoDS_Shape
    tol : float, optional
        The tolerance for the evaluation of the bounding box

    """
    def __init__(self, shape, tol=0.01):
        if isinstance(shape, TopoDS_Shape) or issubclass(shape.__class__,
                                                         TopoDS_Shape):
            self._shape = shape
        else:
            msg = "Expecting a TopoDS_Shape (or a subclass), " \
                  "got a %s" % str(shape.__class__)
            logger.error(msg)
            raise WrongTopologicalType(msg)
        # self._shape = shape
        bb = BoundingBox(self._shape)
        self._x_min = real_bb_position("X",
                                       "MIN",
                                       bb.x_min,
                                       self._shape,
                                       increment=tol)
        self._x_max = real_bb_position("X",
                                       "MAX",
                                       bb.x_max,
                                       self._shape,
                                       increment=tol)
        self._y_min = real_bb_position("Y",
                                       "MIN",
                                       bb.y_min,
                                       self._shape,
                                       increment=tol)
        self._y_max = real_bb_position("Y",
                                       "MAX",
                                       bb.y_max,
                                       self._shape,
                                       increment=tol)
        self._z_min = real_bb_position("Z",
                                       "MIN",
                                       bb.z_min,
                                       self._shape,
                                       increment=tol)
        self._z_max = real_bb_position("Z",
                                       "MAX",
                                       bb.z_max,
                                       self._shape,
                                       increment=tol)

    @property
    def x_min(self):
        r"""Minimum x"""
        return self._x_min

    @property
    def x_max(self):
        r"""Maximum x"""
        return self._x_max

    @property
    def y_min(self):
        r"""Minimum y"""
        return self._y_min

    @property
    def y_max(self):
        r"""Maximum y"""
        return self._y_max

    @property
    def z_min(self):
        r"""Minimum z"""
        return self._z_min

    @property
    def z_max(self):
        r"""Maximum z"""
        return self._z_max

    @property
    def x_span(self):
        r"""x dimension of bounding box"""
        return self.x_max - self.x_min

    @property
    def y_span(self):
        r"""y dimension of bounding box"""
        return self.y_max - self.y_min

    @property
    def z_span(self):
        r"""z dimension of bounding box"""
        return self.z_max - self.z_min

    @property
    def max_dimension(self):
        r"""Maximum dimension"""
        return max([self.x_span, self.y_span, self.z_span])

    @property
    def min_dimension(self):
        r"""Minimum dimension"""
        return min([self.x_span, self.y_span, self.z_span])

    @property
    def aspect_ratio(self):
        r"""Aspect ratio"""
        return self.max_dimension / self.min_dimension

    @property
    def as_tuple(self):
        r"""bounding box as the original tuple"""
        return (self.x_min, self.y_min, self.z_min,
                self.x_max, self.y_max, self.z_max)

    @property
    def centre(self):
        r"""Centre of the bounding box

        Returns
        -------
        OCC.gp.gp_Pnt

        """
        return Point.midpoint(gp_Pnt(self.x_min, self.y_min, self.z_min),
                              gp_Pnt(self.x_max, self.y_max, self.z_max))


def stl_bounding_box(path_to_stl):
    """Reads an ascii or binary STL file to determine its bounding box

    Parameters
    ----------
    path_to_stl : str
        Path to the stl file

    References
    ----------
    http://stackoverflow.com/questions/7566825/python-parsing-binary-stl-file
    http://sukhbinder.wordpress.com/2013/11/28/
                              binary-stl-file-reader-in-python-powered-by-numpy/
    """

    xmin, xmax = 1e12, -1e12
    ymin, ymax = 1e12, -1e12
    zmin, zmax = 1e12, -1e12

    binary = is_binary(path_to_stl)

    if binary:

        def unpack(fi, sig, l):
            s = fi.read(l)
            return struct.unpack(sig, s)

        f = open(path_to_stl, 'rb')

        logger.info('Reading binary stl file : %s' % path_to_stl)

        f.seek(f.tell() + 80)  # read header
        # l = struct.unpack("@i", f.read(4))[0]
        _ = struct.unpack("@i", f.read(4))[0]

        try:
            while True:
                # n = unpack(f, "<3f", 12)
                _ = unpack(f, "<3f", 12)
                p1 = unpack(f, "<3f", 12)
                p2 = unpack(f, "<3f", 12)
                p3 = unpack(f, "<3f", 12)
                # b = unpack(f, "<h", 2)
                _ = unpack(f, "<h", 2)
                numbers = [tuple(p1), tuple(p2), tuple(p3)]
                for number in numbers:
                    x, y, z = number[0], number[1], number[2]
                    if x < xmin:
                        xmin = x
                    if x > xmax:
                        xmax = x
                    if y < ymin:
                        ymin = y
                    if y > ymax:
                        ymax = y
                    if z < zmin:
                        zmin = z
                    if z > zmax:
                        zmax = z
        # except struct.error as e:
        except struct.error:
            logger.info('Finished reading binary stl file')

    else:
        lines = open(path_to_stl, 'r').readlines()

        logger.info('Reading ascii stl file : %s' % path_to_stl)

        for line in lines:
            if 'vertex' in line:
                # split the cleaned up line
                s = re.sub(' +', ' ', line.strip()).split(' ')
                x, y, z = float(s[1]), float(s[2]), float(s[3])
                if x < xmin:
                    xmin = x
                if x > xmax:
                    xmax = x
                if y < ymin:
                    ymin = y
                if y > ymax:
                    ymax = y
                if z < zmin:
                    zmin = z
                if z > zmax:
                    zmax = z

        logger.info('Finished reading ascii stl file')

    return (xmin, xmax), (ymin, ymax), (zmin, zmax)
