# coding: utf-8

r"""Intersections"""

from OCC.gp import gp_Pnt, gp_Lin, gp_Dir
from OCC.IntAna import IntAna_Int3Pln
from OCC.IntCurvesFace import IntCurvesFace_ShapeIntersector

from aocutils.common import AssertIsDone
from aocutils.tolerance import OCCUTILS_DEFAULT_TOLERANCE


def from_three_planes(plane_a, plane_b, plane_c):
    r"""Intersection from 3 planes

    Accepts both Geom_Plane and gp_Pln

    Parameters
    ----------
    plane_a
    plane_b
    plane_c

    Returns
    -------
    OCC.gp.gp_Pnt

    """
    plane_a = plane_a if not hasattr(plane_a, 'Pln') else plane_a.Pln()
    plane_b = plane_b if not hasattr(plane_b, 'Pln') else plane_b.Pln()
    plane_c = plane_c if not hasattr(plane_c, 'Pln') else plane_c.Pln()

    intersection_planes = IntAna_Int3Pln(plane_a, plane_b, plane_c)
    pnt = intersection_planes.Value()
    return pnt


def shape_by_line(topods_shape,
                  line,
                  low_parameter=0.0,
                  hi_parameter=float("+inf")):
    r"""Finds the intersection of a shape and a line

    Parameters
    ----------
    topods_shape : any TopoDS_*
    line : gp_Lin
    low_parameter : float, optional
        (the default value is 0.0)
    hi_parameter : float, optional
        (the default value is infinity)

    Returns
    -------
    a list with a number of tuples that corresponds to the 
    number of intersections found.
    the tuple contains ( OCC.gp.gp_Pnt, TopoDS_Face, u,v,w ), 
    respectively the intersection point, the intersecting face
    and the u,v,w parameters of the intersection point
    """
    shape_inter = IntCurvesFace_ShapeIntersector()
    shape_inter.Load(topods_shape, OCCUTILS_DEFAULT_TOLERANCE)
    shape_inter.PerformNearest(line, low_parameter, hi_parameter)

    with AssertIsDone(shape_inter,
                      "failed to computer shape / line intersection"):
        return (shape_inter.Pnt(1),
                shape_inter.Face(1),
                shape_inter.UParameter(1),
                shape_inter.VParameter(1),
                shape_inter.WParameter(1))


def _intersect_shape_by_line(topods_shape,
                             line,
                             low_parameter=0.0,
                             hi_parameter=float("+inf")):
    r"""Finds the intersection of a shape and a line

    Parameters
    ----------
    topods_shape : any TopoDS_*
    line : gp_Lin
    low_parameter : float, optional
        (the default value is 0.0)
    hi_parameter : float, optional
        (the default value is infinity)

    Returns
    -------
    a list of gp_Pnt

    """
    shape_inter = IntCurvesFace_ShapeIntersector()
    shape_inter.Load(topods_shape, OCCUTILS_DEFAULT_TOLERANCE)
    # shape_inter.PerformNearest(line, low_parameter, hi_parameter)
    shape_inter.Perform(line, low_parameter, hi_parameter)

    with AssertIsDone(shape_inter, "failed to computer shape / line intersection"):
        points = list()

        # Bug correction (some intersection points were missed)
        # for i in range(1, shape_inter.NbPnt()):
        for i in range(1, shape_inter.NbPnt() + 1):
            points.append(shape_inter.Pnt(i))

    return points


def intersect_shape_by_half_line(topods_shape, x, y, z, vx, vy, vz):
    r"""Intersect shape by half line starting at (x, y, z) 
    in the direction (vx, vy, vz)

    This function tries to have a more intuitive interface than 
    intersect_shape_by_line()

    Parameters
    ----------
    topods_shape
    x : float
        Starting point x
    y : float
        Starting point y
    z : float
        Starting point z
    vx : float
        Direction vector x component
    vy : float
        Direction vector y component
    vz : float
        Direction vector z component

    Returns
    -------
    a list of gp_Pnt, ordered in natural order going from the point where the half line starts and following
    the direction

    """
    return _intersect_shape_by_line(topods_shape,
                                    gp_Lin(gp_Pnt(x, y, z),
                                           gp_Dir(vx, vy, vz)),
                                    0,
                                    float("+inf"))

