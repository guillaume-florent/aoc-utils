# coding: utf-8

r"""Transformations: translate, scale_uniform, mirror_pnt_dir, mirror_axe2,
rotate ....

"""

import math

from OCC.BRepBuilderAPI import BRepBuilderAPI_Transform
from OCC.gp import gp_Trsf, gp_Ax1
from OCC.TopoDS import TopoDS_Shape

from aocutils.common import AssertIsDone
from aocutils.topology import shape_to_topology


def translate(brep_or_iterable, vec, copy=False):
    r"""Translate a TopoDS_* using a vector

    Parameters
    ----------
    brep_or_iterable : TopoDS_Shape or iterable[TopoDS_Shape]
        the Topo_DS to translate
    vec
        the vector defining the translation
    copy
        copies to brep if True

    Returns
    -------
    list[TopoDS_*]

    """
    # st = occutils.types_lut.ShapeToTopology()
    gp_trsf = gp_Trsf()
    gp_trsf.SetTranslation(vec)
    if issubclass(brep_or_iterable.__class__, TopoDS_Shape):
        brep_transform = BRepBuilderAPI_Transform(brep_or_iterable, gp_trsf, copy)
        brep_transform.Build()
        return shape_to_topology(brep_transform.Shape())
    else:
        return [translate(brep_or_iterable, vec, copy) for _ in brep_or_iterable]


def rotate(brep, axe, degree, copy=False):
    r"""Rotate around an axis

    Parameters
    ----------
    brep : TopoDS_*
    axe : gp_Ax1
    degree : float
        Rotation angle in degrees
    copy : bool

    Returns
    -------
    TopoDS_*

    """
    gp_trsf = gp_Trsf()
    gp_trsf.SetRotation(axe, math.radians(degree))
    brep_transform = BRepBuilderAPI_Transform(brep, gp_trsf, copy)
    with AssertIsDone(brep_transform, 'could not produce rotation'):
        brep_transform.Build()
        return shape_to_topology(brep_transform.Shape())


def scale_uniform(brep, pnt, factor, copy=False):
    r"""Scale a brep

    Parameters
    ----------
    brep
        the Topo_DS to scale
    pnt : gp_Pnt
        a gp_Pnt
    factor : float
        scaling factor
    copy : bool
        copies to brep if True

    Returns
    -------
    TopoDS_Shape

    """
    trns = gp_Trsf()
    trns.SetScale(pnt, factor)
    brep_trns = BRepBuilderAPI_Transform(brep, trns, copy)
    brep_trns.Build()
    return brep_trns.Shape()


def mirror_pnt_dir(brep, pnt, direction, copy=False):
    r"""Mirror ...

    Parameters
    ----------
    brep
    pnt : gp_Pnt
    direction : gp_Dir
    copy : bool

    Returns
    -------
    TopoDS_Shape

    """
    trns = gp_Trsf()
    trns.SetMirror(gp_Ax1(pnt, direction))
    brep_trns = BRepBuilderAPI_Transform(brep, trns, copy)
    with AssertIsDone(brep_trns, 'could not produce mirror'):
        brep_trns.Build()
        return brep_trns.Shape()


def mirror_axe2(brep, axe2, copy=False):
    r"""

    Parameters
    ----------
    brep : TopoDS_*
    axe2 : gp_Ax2
    copy : bool

    Returns
    -------
    TopoDS_Shape

    """
    trns = gp_Trsf()
    trns.SetMirror(axe2)
    brep_trns = BRepBuilderAPI_Transform(brep, trns, copy)
    with AssertIsDone(brep_trns, 'could not produce mirror'):
        brep_trns.Build()
        return brep_trns.Shape()
