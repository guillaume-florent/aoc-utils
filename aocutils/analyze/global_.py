# coding: utf-8

r"""Global analysis properties"""

import logging

from OCC.Core.GProp import GProp_GProps
from OCC.Core.BRepGProp import brepgprop_LinearProperties, \
    brepgprop_SurfaceProperties, brepgprop_VolumeProperties

from aocutils.types_ import topo_lut
from aocutils.exceptions import WrongTopologicalType

logger = logging.getLogger(__name__)


class GlobalProperties(object):
    r"""Global properties for all topologies

    Parameters
    ----------
    shape : OCC.TopoDS.TopoDS_Shape

    """
    # TODO : how to handle compound ?
    linear_types = ["edge", "wire"]
    surfacic_types = ["face", "shell"]
    volumic_types = ["solid"]

    def __init__(self, shape):
        self.shape = shape
        self._topo_type = topo_lut[self.shape.ShapeType()]
        self._system = None

    @property
    def topo_type(self):
        r"""Topological geom_type"""
        return self._topo_type

    @property
    def system(self):
        r"""Initialise the GProp_GProps depending on the topological type

        Notes
        -----
        geom_type could be abstracted with TopoDS... instead of using _topo_type

        Returns
        -------
        OCC.GProp.GProp_GProps

        """
        self._system = GProp_GProps()

        if self._topo_type in GlobalProperties.surfacic_types:
            brepgprop_SurfaceProperties(self.shape, self._system)
        elif self._topo_type in GlobalProperties.linear_types:
            brepgprop_LinearProperties(self.shape, self._system)
        elif self._topo_type in GlobalProperties.volumic_types:
            brepgprop_VolumeProperties(self.shape, self._system)
        else:
            msg = "ShapeType is not linear, surfacic or volumic"
            logger.error(msg)
            raise WrongTopologicalType(msg)
        return self._system

    @property
    def centre(self):
        r"""Centre of the entity

        Returns
        -------
        """
        return self.system.CentreOfMass()

    @property
    def inertia(self):
        """Inertia matrix"""
        return self.system.MatrixOfInertia(), self.system.MomentOfInertia()

    # @property
    # def area(self):
    #     r"""Area of the surface"""
    #     if self.topo_type not in GlobalProperties.surfacic_types:
    #         msg = "area is only defined for linear surfacic types"
    #         logger.error(msg)
    #         raise aocutils.exceptions.WrongTopologicalType(msg)
    #     return self._mass()
    #
    # @property
    # def volume(self):
    #     r"""Volume"""
    #     if self.topo_type not in GlobalProperties.volumic_types:
    #         msg = "volume is only defined for linear volumic types"
    #         logger.error(msg)
    #         raise aocutils.exceptions.WrongTopologicalType(msg)
    #     return self._mass()

    # New handling of area and volume to properly handle compound

    @property
    def area(self):
        r"""Area of the surface"""
        if self.topo_type not in GlobalProperties.surfacic_types:
            if self.topo_type != "compound":
                msg = "area is only defined for linear surfacic types"
                logger.error(msg)
                raise WrongTopologicalType(msg)
            else:
                import aocutils.topology
                faces = aocutils.topology.Topo(self.shape).faces
                return sum([GlobalProperties(face).area for face in faces])
        return self._mass()

    @property
    def volume(self):
        r"""Volume"""
        if self.topo_type not in GlobalProperties.volumic_types:
            if self.topo_type != "compound":
                msg = "volume is only defined for linear volumic types"
                logger.error(msg)
                raise WrongTopologicalType(msg)
            else:
                import aocutils.topology
                solids = aocutils.topology.Topo(self.shape).solids
                return sum([GlobalProperties(solid).volume for solid in solids])
        return self._mass()

    def _mass(self):
        return self.system.Mass()

    @property
    def length(self):
        r"""length of a wire or edge"""
        if self.topo_type not in GlobalProperties.linear_types:
            msg = "length is only defined for linear topological types"
            logger.error(msg)
            raise WrongTopologicalType(msg)
        return self.system.Mass()
