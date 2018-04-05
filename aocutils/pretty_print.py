# coding: utf-8

r"""Pretty printing of various OCC entities"""

import math

from OCC.Core.gp import gp_Vec, gp_Pnt, gp_Ax1, gp_Trsf, gp_Quaternion
from OCC.Core.BRep import BRep_Tool
from OCC.Core.TopoDS import TopoDS_Iterator, topods_Vertex
from OCC.Core.TopAbs import TopAbs_VERTEX, TopAbs_SOLID, TopAbs_EDGE, \
    TopAbs_FACE, TopAbs_SHELL, TopAbs_WIRE, TopAbs_COMPOUND, TopAbs_COMPSOLID


def add_str_repr():
    r"""Add the shortcuts to the gp types"""
    # print gp_Pnt() should return something informative...
    gp_Vec.__repr__ = gp_vec_print
    gp_Vec.__str__ = gp_vec_print
    gp_Pnt.__repr__ = gp_pnt_print
    gp_Pnt.__str__ = gp_pnt_print
    gp_Ax1.__repr__ = gp_ax1_print
    gp_Ax1.__str__ = gp_ax1_print
    gp_Trsf.__repr__ = gp_trsf_print
    gp_Trsf.__str__ = gp_trsf_print
    gp_Quaternion.__repr__ = gp_quat_print
    gp_Quaternion.__str__ = gp_quat_print


def gp_pnt_print(pnt):
    r"""User friendly version of point coordinates

    Parameters
    ----------
    pnt : gp_Pnt

    Returns
    -------
    str

    """
    x = pnt.X()
    y = pnt.Y()
    z = pnt.Z()
    return '< gp_Pnt: {0}, {1}, {2} >'.format(x, y, z)


def gp_vec_print(vec):
    r"""User friendly version of gp_Vec components

    Parameters
    ----------
    vec : gp_Vec

    Returns
    -------
    str

    """
    x = vec.X()
    y = vec.Y()
    z = vec.Z()
    mag = vec.Magnitude()
    return '< gp_Vec: {0}, {1}, {2}, magnitude: {3} >'.format(x, y, z, mag)


def gp_ax1_print(ax1):
    r"""User friendly version of gp_Ax1 components

    Parameters
    ----------
    ax1 : gp_Ax1

    Returns
    -------
    str

    """
    px = ax1.Location().X()
    py = ax1.Location().Y()
    pz = ax1.Location().Z()
    dx = ax1.Direction().X()
    dy = ax1.Direction().Y()
    dz = ax1.Direction().Z()
    s = "< gp_Ax1: location: {px}, {py}, {pz}, direction: {dx}, {dy}, {dz} >"
    return s.format(px=px, py=py, pz=pz, dx=dx, dy=dy, dz=dz)


def gp_trsf_print(trsf):
    r"""User friendly version of gp_Trsf

    Parameters
    ----------
    trsf : gp_Trsf

    Returns
    -------
    str

    """
    _f = lambda x: [trsf.Value(x, i) for i in range(1, 5)]
    a, b, c, d = _f(1)
    e, f, g, h = _f(2)
    i, j, k, l = _f(3)
    return "< gp_Trsf:\n {a:.3f}, {b:.3f}, {c:.3f}, {d:.3f}\n " \
           "{e:.3f}, {f:.3f}, {g:.3f}, {h:.3f}\n " \
           "{i:.3f}, {j:.3f}, {k:.3f}, {l:.3f} >".format(a=a, b=b, c=c, d=d,
                                                         e=e, f=f, g=g, h=h,
                                                         i=i, j=j, k=k, l=l)


def gp_quat_print(quat):
    r"""User friendly version of gp_Quaternion

    Parameters
    ----------
    quat : gp_Quaternion

    Returns
    -------
    str

    """
    w, x, y, z = quat.W(), quat.X(), quat.Y(), quat.Z()
    vec = gp_Vec()
    angle = math.degrees(quat.GetVectorAndAngle(vec))
    s = "< gp_Quaternion: w:{w}, x:{x}, y:{y}, z:{z} >\n" \
        "vector:{vec} angle:{angle}"
    return s.format(w=w, x=x, y=y, z=z, vec=vec, angle=angle)


def dump_topology(shape, level=0):
    r"""Print the details of an object from the top down.

    The function is recursive

    Parameters
    ----------
    shape : TopoDS_Shape
    level : int

    Returns
    -------
    str
        Multiline description of the shape topology
    """
    brep_tool = BRep_Tool
    s = shape.ShapeType()
    if s == TopAbs_VERTEX:
        pnt = brep_tool.Pnt(topods_Vertex(shape))
        print(".." * level + "<Vertex %i: %s %s %s>" % (hash(shape),
                                                        pnt.X(),
                                                        pnt.Y(),
                                                        pnt.Z()))
    else:
        print(".." * level + shape_type_string(shape))
        # print(shape_type_string(shape))
    shape_iterator = TopoDS_Iterator(shape)
    while shape_iterator.More():
        shp = shape_iterator.Value()
        shape_iterator.Next()
        dump_topology(shp, level + 1)


def shape_type_string(shape):
    r"""Readable geom_type of shape

    Parameters
    ----------
    shape : TopoDS_*

    Returns
    -------
    str
        Readable shape geom_type description and hash value e.g. Solid: 3617953

    """
    st = shape.ShapeType()
    s = "?"
    if st == TopAbs_VERTEX:
        s = "Vertex"
    if st == TopAbs_SOLID:
        s = "Solid"
    if st == TopAbs_EDGE:
        s = "Edge"
    if st == TopAbs_FACE:
        s = "Face"
    if st == TopAbs_SHELL:
        s = "Shell"
    if st == TopAbs_WIRE:
        s = "Wire"
    if st == TopAbs_COMPOUND:
        s = "Compound."
    if st == TopAbs_COMPSOLID:
        s = "Compsolid."
    return "%s: %i" % (s, hash(shape))
