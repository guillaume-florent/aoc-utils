# coding: utf-8

r"""Methods to make an edge"""

from __future__ import print_function

import logging
import functools

# import OCC.BRepAdaptor
from OCC.BRepBuilderAPI import BRepBuilderAPI_MakeEdge, \
    BRepBuilderAPI_MakeEdge2d
from OCC.gp import gp_Circ

from aocutils.common import AssertIsDone
from aocutils.math_ import smooth_pnts
from aocutils.operations.interpolate import points_to_bspline

logger = logging.getLogger(__name__)


@functools.wraps(BRepBuilderAPI_MakeEdge2d)
def edge2d(*args):
    r"""Build an edge

    Parameters
    ----------
    args

    Returns
    -------
    TopoDS_Edge

    """
    edge_ = BRepBuilderAPI_MakeEdge2d(*args)
    with AssertIsDone(edge_, 'failed to produce edge'):
        result = edge_.Edge()
        edge_.Delete()
    return result


@functools.wraps(BRepBuilderAPI_MakeEdge)
def edge(*args):
    r"""Make a TopoDS_Edge

    Parameters
    ----------
    args

    Returns
    -------
    TopoDS_Edge

    """
    an_edge = BRepBuilderAPI_MakeEdge(*args)
    with AssertIsDone(an_edge, 'failed to produce edge'):
        result = an_edge.Edge()
        an_edge.Delete()
        return result


def circle(pnt, radius):
    r"""Make a circle

    Parameters
    ----------
    pnt : gp_Pnt
        Circle centre
    radius : float

    Returns
    -------
    TopoDS_Edge

    """
    circ = gp_Circ()
    circ.SetLocation(pnt)
    circ.SetRadius(radius)
    return edge(circ)


def line(pnt1, pnt2):
    r"""Make a line

    Parameters
    ----------
    pnt1 : gp_Pnt
    pnt2 : gp_Pnt

    Returns
    -------
    TopoDS_Edge

    """
    return edge(pnt1, pnt2)


def geodesic_path(pnt_a,
                  pnt_b,
                  aoc_face,
                  n_segments=20,
                  _tolerance=0.1,
                  n_iter=20):
    r"""

    Parameters
    ----------
    pnt_a
        point to start from
    pnt_b
        point to move towards
    aoc_face
        aocutils.brep.face.Face on which `edgA` and `edgB` lie
    n_segments : int
        the number of segments the geodesic is built from
    _tolerance : float
        tolerance when the geodesic is converged
    n_iter : int
        maximum number of iterations

    Returns
    -------
    TopoDS_Edge

    """
    # uv_a, srf_pnt_a = aoc_face.project_vertex(pnt_a)
    # uv_b, srf_pnt_b = aoc_face.project_vertex(pnt_b)
    uv_a, _ = aoc_face.project_vertex(pnt_a)
    uv_b, _ = aoc_face.project_vertex(pnt_b)

    path = []
    for i in range(n_segments):
        t = i / n_segments
        u = uv_a[0] + t*(uv_b[0] - uv_a[0])
        v = uv_a[1] + t*(uv_b[1] - uv_a[1])
        path.append(aoc_face.parameter_to_point(u, v))

    def project_pnts(x):
        r"""Project points

        Parameters
        ----------
        x

        Returns
        -------

        """
        return [aoc_face.project_vertex(j)[1] for j in x]

    def poly_length(x):
        r"""Poly length

        Parameters
        ----------
        x

        Returns
        -------

        """
        return sum([x[j].Distance(x[j + 1]) for j in range(len(x) - 1)]) / len(x)

    length = poly_length(path)

    n = 0
    while True:
        path = smooth_pnts(path)
        path = project_pnts(path)
        newlength = poly_length(path)
        if abs(newlength-length) < _tolerance or n == n_iter:
            crv = points_to_bspline(path)
            return edge(crv)
        n += 1
