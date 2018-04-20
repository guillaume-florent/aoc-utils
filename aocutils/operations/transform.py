# coding: utf-8

r"""Transformations: translate, scale_uniform, mirror_pnt_dir, mirror_axe2,
rotate ....

"""

import math

from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_Transform
from OCC.Core.gp import gp_Trsf, gp_Ax1, gp_Ax2, gp_Pnt, gp_Dir, gp_Vec
from OCC.Core.TopoDS import TopoDS_Shape

from aocutils.common import AssertIsDone
from aocutils.topology import shape_to_topology


def translate(brep_or_iterable, vec, copy=False):
    r"""Translate a TopoDS_* using a vector

    Parameters
    ----------
    brep_or_iterable : TopoDS_Shape or iterable[TopoDS_Shape]
        the Topo_DS to translate
    vec : tuple
        the vector defining the translation
    copy
        copies to brep if True

    Returns
    -------
    list[TopoDS_*]

    """
    # st = occutils.types_lut.ShapeToTopology()
    gp_trsf = gp_Trsf()
    gp_trsf.SetTranslation(gp_Vec(*vec))
    if issubclass(brep_or_iterable.__class__, TopoDS_Shape):
        brep_transform = BRepBuilderAPI_Transform(brep_or_iterable, gp_trsf, copy)
        brep_transform.Build()
        return shape_to_topology(brep_transform.Shape())
    else:
        return [translate(brep_or_iterable, gp_Vec(*vec), copy) for _ in brep_or_iterable]


def rotate(brep, pnt, direction, degree, copy=False):
    r"""Rotate around an axis

    Parameters
    ----------
    brep : TopoDS_*
    pnt : tuple
    direction : tuple
    degree : float
        Rotation angle in degrees
    copy : bool

    Returns
    -------
    TopoDS_*

    """
    axe = gp_Ax1(gp_Pnt(*pnt), gp_Dir(*direction))
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
    pnt : tuple
        x, y, z
    factor : float
        scaling factor
    copy : bool
        copies to brep if True

    Returns
    -------
    TopoDS_Shape

    """
    trns = gp_Trsf()
    trns.SetScale(gp_Pnt(*pnt), factor)
    brep_trns = BRepBuilderAPI_Transform(brep, trns, copy)
    brep_trns.Build()
    return brep_trns.Shape()


def mirror_pnt_dir(brep, pnt, direction, copy=False):
    r"""Mirror ...

    Parameters
    ----------
    brep
    pnt : tuple
    direction : tuple
    copy : bool

    Returns
    -------
    TopoDS_Shape

    """
    trns = gp_Trsf()
    trns.SetMirror(gp_Ax1(gp_Pnt(*pnt), gp_Dir(*direction)))
    brep_trns = BRepBuilderAPI_Transform(brep, trns, copy)
    with AssertIsDone(brep_trns, 'could not produce mirror'):
        brep_trns.Build()
        return brep_trns.Shape()


def mirror_axe2(brep, pnt, direction_1, direction_2, copy=False):
    r"""

    Parameters
    ----------
    brep : TopoDS_*
    pnt : tuple
    direction_1 : tuple
    direction_2 : tuple
    copy : bool

    Returns
    -------
    TopoDS_Shape

    """
    trns = gp_Trsf()
    axe2 = gp_Ax2(gp_Pnt(*pnt), gp_Dir(*direction_1), gp_Dir(*direction_2))
    trns.SetMirror(axe2)
    brep_trns = BRepBuilderAPI_Transform(brep, trns, copy)
    with AssertIsDone(brep_trns, 'could not produce mirror'):
        brep_trns.Build()
        return brep_trns.Shape()
