# coding: utf-8

r"""geom plane"""

import logging

from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_FindPlane
from OCC.Core.GeomPlate import GeomPlate_BuildAveragePlane
from OCC.Core.gp import gp_Vec
from OCC.Core.TColgp import TColgp_HArray1OfPnt, TColgp_SequenceOfVec

from aocutils.exceptions import FindPlaneException
from aocutils.brep.vertex import Vertex
from aocutils.collections import to_tcol_
from aocutils.topology import Topo
from aocutils.geom.vector import Vector


logger = logging.getLogger(__name__)


class Plane(object):
    r"""Wrapper for Geom_Plane

    """
    def __init__(self, geom_plane):
        self._geom_plane = geom_plane

    @property
    def geom_plane(self):
        return self._geom_plane

    @classmethod
    def from_shape(cls, shape, tolerance=-1):
        r"""Find a plane from a shape

        Parameters
        ----------
        shape : OCC.TopoDS.TopoDS_Shape
        tolerance : float

        Returns
        -------
        OCC.Geom.Geom_Plane

        """
        try:
            fpl = BRepBuilderAPI_FindPlane(shape, tolerance)
            if fpl.Found():
                return cls(fpl.Plane().GetObject())
            else:
                msg = 'Plane not found in %s' % shape
                logger.error(msg)
                raise FindPlaneException(msg)
        except:
            msg = 'Could not find plane in %s' % shape
            logger.error(msg)
            raise FindPlaneException(msg)

    @classmethod
    def through_face_vertices(cls, _face):
        r"""Fit a plane through face vertices

        Parameters
        ----------
        _face : occutils.core.face.Face

        Returns
        -------
        Geom_Plane

        """
        uvs_from_vertices = [_face.project_vertex(Vertex.to_pnt(i))
                             for i in Topo(_face).vertices]
        normals = [gp_Vec(_face.DiffGeom.normal(*uv[0])) for uv in uvs_from_vertices]
        points = [i[1] for i in uvs_from_vertices]

        NORMALS = TColgp_SequenceOfVec()
        # [NORMALS.Append(i) for i in normals]
        for i in normals:
            NORMALS.Append(i)
        POINTS = to_tcol_(points, TColgp_HArray1OfPnt)

        pl = GeomPlate_BuildAveragePlane(NORMALS, POINTS).Plane().GetObject()
        vec = gp_Vec(pl.Location(), _face.GlobalProperties.centre())
        pt = (pl.Location().as_vec() + vec).as_pnt()
        pl.SetLocation(pt)
        return cls(pl)

    def normal_vector(self, vec_length=1.):
        r"""Vector normal to the plane of length vec_length

        Parameters
        ----------
        vec_length

        Returns
        -------
        gp_Vec

        """
        trns = gp_Vec(self._geom_plane.Axis().Direction())
        return Vector(trns.Normalized() * vec_length)
