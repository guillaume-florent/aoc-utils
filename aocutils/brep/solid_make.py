# coding: utf-8

r"""Methods to make a solid"""

import functools

from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeSolid
from OCC.Core.BRepOffsetAPI import BRepOffsetAPI_MakePipe
# import OCC.TopoDS

from aocutils.common import AssertIsDone
from aocutils.brep.wire_make import polygon
from aocutils.brep.edge_make import line
from aocutils.brep.face_make import face
from aocutils.operations.transform import translate
from aocutils.operations.sew import sew_shapes


@functools.wraps(BRepBuilderAPI_MakeSolid)
def solid(*args):
    r"""Make a TopoDS_Solid

    Parameters
    ----------
    args

    Returns
    -------
    TopoDS_Solid

    Notes
    -----
    BRepBuilderAPI_MakeSolid ()
    BRepBuilderAPI_MakeSolid (const TopoDS_CompSolid &S)
    BRepBuilderAPI_MakeSolid (const TopoDS_Shell &S)
    BRepBuilderAPI_MakeSolid (const TopoDS_Shell &S1, const TopoDS_Shell &S2)
    BRepBuilderAPI_MakeSolid (const TopoDS_Shell &S1,
                              const TopoDS_Shell &S2,
                              const TopoDS_Shell &S3)
    BRepBuilderAPI_MakeSolid (const TopoDS_Solid &So)
    BRepBuilderAPI_MakeSolid (const TopoDS_Solid &So, const TopoDS_Shell &S)

    """
    sld = BRepBuilderAPI_MakeSolid(*args)
    with AssertIsDone(sld, 'failed to produce solid'):
        result = sld.Solid()
        sld.Delete()
        return result


def oriented_box(v_corner, v_x, v_y, v_z):
    r"""Produces an oriented box
    oriented meaning here that the x,y,z axis do not have
    to be cartesian aligned

    Parameters
    ----------
    v_corner
        the lower corner
    v_x : OCC.gp.gp_Vec
        gp_Vec that describes the X-axis
    v_y : OCC.gp.gp_Vec
        gp_Vec that describes the Y-axis
    v_z : OCC.gp.gp_Vec
        gp_Vec that describes the Z-axis

    Returns
    -------
    TopoDS_Solid

    """
    verts = map(lambda x: x.as_pnt(), [v_corner, v_corner + v_x, v_corner+v_x+v_y, v_corner+v_y])
    p = polygon(verts, closed=True)
    li = line(v_corner.as_pnt(), (v_corner + v_z).as_pnt())
    bmp = BRepOffsetAPI_MakePipe(p, li)
    bmp.Build()
    shp = bmp.Shape()

    bottom = face(p)
    top = translate(bottom, v_z, True)
    oriented_bbox = solid(sew_shapes([bottom, shp, top]))
    return oriented_bbox
