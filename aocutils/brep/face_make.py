# coding: utf-8

r"""Methods to make a face"""

import logging
import functools

from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeFace
from OCC.Core.BRepFill import BRepFill_CurveConstraint, brepfill_Face,\
    BRepFill_Filling
from OCC.Core.Geom import Geom_RectangularTrimmedSurface
from OCC.Core.GeomAbs import GeomAbs_C0
from OCC.Core.GeomPlate import GeomPlate_MakeApprox, GeomPlate_BuildPlateSurface
from OCC.Core.BRepAdaptor import BRepAdaptor_HCurve
from OCC.Core.gp import gp_Pnt, gp_Vec, gp_Dir, gp_Pln

from aocutils.common import AssertIsDone
from aocutils.brep.wire_make import closed_polygon

logger = logging.getLogger(__name__)


@functools.wraps(BRepBuilderAPI_MakeFace)
def face(*args):
    r"""Make a TopoDS_Face

    Parameters
    ----------
    args

    Returns
    -------
    TopoDS_Face

    """
    a_face = BRepBuilderAPI_MakeFace(*args)
    with AssertIsDone(a_face, 'failed to produce face'):
        result = a_face.Face()
        a_face.Delete()
        return result


def from_points(points_list):
    r"""Make a face from n points

    Parameters
    ----------
    points_list : list[gp_Pnt]

    """
    # poly is a TopoDS_Wire
    poly = closed_polygon(points_list)
    return face(poly)


def ruled(edge_a, edge_b):
    r"""Make a ruled surface between 2 edges

    Parameters
    ----------
    edge_a : TopoDS_Edge
    edge_b : TopoDS_Edge

    Returns
    -------
    TopoDS_Face

    """
    return brepfill_Face(edge_a, edge_b)


def plane(center=gp_Pnt(0, 0, 0),
          vec_normal=gp_Vec(0, 0, 1),
          extent_x_min=-100.,
          extent_x_max=100.,
          extent_y_min=-100.,
          extent_y_max=100.,
          depth=0.):
    r"""Make a plane

    Parameters
    ----------
    center : gp_Pnt
    vec_normal : gp_Vec
    extent_x_min : float
    extent_x_max : float
    extent_y_min : float
    extent_y_max : float
    depth : float

    Returns
    -------
    TopoDS_Face

    """
    if depth != 0:
        # noinspection PyUnresolvedReferences
        center = center.add_vec(gp_Vec(0, 0, depth))
    # noinspection PyUnresolvedReferences
    pln = gp_Pln(center, gp_Dir(vec_normal.X(), vec_normal.Y(), vec_normal.Z()))
    a_face = face(pln, extent_x_min, extent_x_max, extent_y_min, extent_y_max)
    return a_face


def n_sided(edges, points, continuity=GeomAbs_C0):
    r"""Builds an n-sided patch, respecting the constraints defined
    by *edges* and *points*

    A simplified call to the BRepFill_Filling class

    It is simplified in the sense that to all constraining edges and points
    the same level of *continuity* will be applied

    Parameters
    ----------
    edges
        the constraining edges
    points
        the constraining points
    continuity : GeomAbs_0, 1, 2
                 GeomAbs_C0 : the surface has to pass by 3D representation
                              of the edge
                 GeomAbs_G1 : the surface has to pass by 3D representation
                              of the edge and to respect tangency with
                              the given face
                 GeomAbs_G2 : the surface has to pass by 3D representation
                              of the edge and to respect tangency and
                              curvature with the given face.

    Returns
    -------
    TopoDS_Face

    Notes
    -----
    It is not required to set constraining points.
    Just leave the tuple or list empty

    """
    an_n_sided = BRepFill_Filling()
    for edg in edges:
        an_n_sided.Add(edg, continuity)
    for pt in points:
        an_n_sided.Add(pt)
    an_n_sided.Build()
    return an_n_sided.Face()


def constrained_surface_from_edges(edges):
    r"""

    DOESNT RESPECT BOUNDARIES

    Parameters
    ----------
    edges : list[TopoDS_Edge]

    Returns
    -------
    TopoDS_Face

    """
    bp_srf = GeomPlate_BuildPlateSurface(3, 15, 2)
    for edg in edges:
        c = BRepAdaptor_HCurve()
        c.ChangeCurve().Initialize(edg)
        constraint = BRepFill_CurveConstraint(c.GetHandle(), 0)
        bp_srf.Add(constraint.GetHandle())
    bp_srf.Perform()
    max_seg, max_deg, crit_order = 9, 8, 0
    tol = 1e-4
    srf = bp_srf.Surface()
    plate = GeomPlate_MakeApprox(srf, tol, max_seg, max_deg, tol, crit_order)
    u_min, u_max, v_min, v_max = srf.GetObject().Bounds()
    return face(plate.Surface(), u_min, u_max, v_min, v_max)


def add_wire_to_face(a_face, wire, reverse=False):
    r"""Apply a wire to a a_face
    use reverse to set the orientation of the wire to opposite

    Parameters
    ----------
    a_face
    wire : TopoDS_Wire
    reverse : bool

    Returns
    -------
    TopoDS_Face

    """
    a_face = BRepBuilderAPI_MakeFace(a_face)
    if reverse:
        wire.Reverse()
    a_face.Add(wire)
    result = a_face.Face()
    a_face.Delete()
    return result


def from_plane(_geom_plane, lower_limit=-1000, upper_limit=1000):
    r"""Face from a plane

    Parameters
    ----------
    _geom_plane
    lower_limit
    upper_limit

    Returns
    -------
    TopoDS_Face

    """
    _trim_plane = face(Geom_RectangularTrimmedSurface(_geom_plane.GetHandle(),
                                                      lower_limit,
                                                      upper_limit,
                                                      lower_limit,
                                                      upper_limit).GetHandle())
    return _trim_plane
