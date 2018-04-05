# coding: utf-8

r"""Projection operations"""

from OCC.GeomAPI import GeomAPI_ProjectPointOnCurve
from OCC.GeomProjLib import geomprojlib_ProjectOnPlane
from OCC.ProjLib import projlib_Project
from OCC.TopoDS import TopoDS_Shape

# TODO : wrong name
import aocutils.convert.adapt
from aocutils.brep.edge_make import edge


def point_on_curve(crv, pnt):
    r"""Project a point on a curve

    Parameters
    ----------
    crv
    pnt

    Returns
    -------

    """
    if isinstance(crv, TopoDS_Shape):
        # get the curve handle...
        crv = aocutils.convert.adapt.edge_to_curve(crv).Curve().Curve()
    else:
        raise NotImplementedError('expected a TopoDS_Edge...')
    rrr = GeomAPI_ProjectPointOnCurve(pnt, crv)
    return rrr.LowerDistanceParameter(), rrr.NearestPoint()


def point_on_plane(plane, point):
    r"""Project a point on a plane

    Parameters
    ----------
    plane : Geom_Plane
    point : OCC.gp.gp_Pnt

    Returns
    -------
    OCC.gp.gp_Pnt

    """
    pl = plane.Pln()
    aa, bb = projlib_Project(pl, point).Coord()
    point = plane.Value(aa, bb)
    return point


def edge_on_plane(edg, plane):
    r"""Project an edge onto a plane

    Parameters
    ----------
    edg : kbe.edge.Edge ??
    plane : Geom_Plane

    Returns
    -------
    TopoDS_Edge
        TopoDS_Edge projected on the plane

    """
    proj = geomprojlib_ProjectOnPlane(edg.adaptor.Curve().Curve(),
                                      plane.GetHandle(),
                                      plane.Axis().Direction(),
                                      1)
    return edge(proj)
