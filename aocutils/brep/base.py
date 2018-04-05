# coding: utf-8

r"""BaseObject is inherited by Vertex, Edge, Face, Shell, Solid"""

import logging

from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_Copy
from OCC.Core.BRepCheck import BRepCheck_Analyzer
# import OCC.BRepGProp
# import OCC.Display.SimpleGui
# import OCC.GProp
# import OCC.TopoDS

from aocutils.types import topo_types_dict
from aocutils.topology import Topo, shape_to_topology
from aocutils.analyze.distance import MinimumDistance
from aocutils.tolerance import OCCUTILS_DEFAULT_TOLERANCE
from aocutils.mesh import mesh

logger = logging.getLogger(__name__)


class BaseObject(object):
    """Base class for all objects

    Parameters
    ----------
    wrapped_instance : TopoDS_Shape or subclass
    name: str, optional (default is None)
    tolerance: float, optional (default is OCCUTILS_DEFAULT_TOLERANCE)

    """
    def __init__(self,
                 wrapped_instance,
                 name=None,
                 tolerance=OCCUTILS_DEFAULT_TOLERANCE):
        self._wrapped_instance = wrapped_instance
        self.name = name
        self.tolerance = tolerance
        self._is_meshed = False
        self._mesh_factor = None

    @property
    def wrapped_instance(self):
        r"""The instance wrapped by the BaseObject"""
        return self._wrapped_instance

    @property
    def is_meshed(self):
        r"""Flag for meshing status

        Returns
        -------
        bool
            True if the wrapped instance has been meshed, False otherwise

        """
        return self._is_meshed

    @property
    def mesh_factor(self):
        r"""Mesh factor used

        Returns
        -------
        float or None
            last division factor used for meshing if is_meshed is True,
            None if is_meshed is False

        """
        return self._mesh_factor

    def mesh(self, factor=4000.):
        r"""Mesh the wrapped instance

        Parameters
        ----------
        factor : float
            Division factor of the bounding box max dimension

        """
        if self.is_meshed is False or self.mesh_factor != factor:
            logger.info("Meshing with factor %s" % str(factor))
            mesh(self._wrapped_instance, factor=factor)
            self._is_meshed = True
            self._mesh_factor = factor
        else:
            logger.info("Already meshed !")

    @property
    def tshape(self):
        r"""Wrapped instance TShape

        Returns
        -------
        OCC.TopoDS.TopoDS_TShape

        """
        return self._wrapped_instance.TShape()

    @property
    def location(self):
        r"""Wrapped instance Location

        Returns
        -------
        OCC.TopLoc.TopLoc_Location

        """
        return self._wrapped_instance.Location()

    @property
    def orientation(self):
        r"""Wrapped instance

        Returns
        -------
        PCC.TopABs.TopAbs_Orientation

        """
        return self._wrapped_instance.Orientation()

    @property
    def topo(self):
        r"""Topo

        Returns
        -------
        occutils.topology.Topo

        """
        return Topo(self._wrapped_instance)

    @property
    def topo_type(self):
        r"""Topological geom_type"""
        return topo_types_dict[self._wrapped_instance.ShapeType()]

    def check(self):
        """Some subclasses may implement this method ... but some may not"""
        raise NotImplementedError

    @property
    def is_valid(self):
        r"""Checks that the shape is valid

        References
        ----------
        http://www.opencascade.com/doc/occt-6.9.0/refman/html/
        class_b_rep_check___analyzer.html#a8bfc5e0f53f16106fdfaf3e2c28c7cb0

        Returns
        -------
        bool
            True if the object is valid, False otherwise
        """
        analyse = BRepCheck_Analyzer(self._wrapped_instance)
        ok = analyse.IsValid()
        if ok:
            return True
        else:
            return False

    def copy(self):
        r"""Copy

        Returns
        -------
        A copy of self

        """
        brep_builder_copy = BRepBuilderAPI_Copy(self._wrapped_instance)
        brep_builder_copy.Perform(self._wrapped_instance)
        # get the class, construct a new instance
        # cast the cp.Shape() to its specific TopoDS topology
        _copy = self.__class__(shape_to_topology(brep_builder_copy.Shape()))
        return _copy

    def distance(self, other):
        """Minimum distance

        Parameters
        ----------
        other : any TopoDS_*
            The other TopoDS_* object

        Returns
        -------
        tuple
            minimum distance,
            minimum distance points on shp1,
            minimum distance points on shp2

        """
        return MinimumDistance(self._wrapped_instance, other).minimum_distance

    def __eq__(self, other):
        return self._wrapped_instance.IsEqual(other)

    def __ne__(self, other):
        return not self.__eq__(other)
