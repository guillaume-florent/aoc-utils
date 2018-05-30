# coding: utf-8

r"""types_.py module of aocutils"""

import sys
import itertools

from OCC.Core.BRepCheck import *
from OCC.Core.GeomAbs import *
from OCC.Core.TopoDS import TopoDS_Vertex, TopoDS_Edge, TopoDS_Face, \
    TopoDS_Wire, TopoDS_Shell, TopoDS_Solid, TopoDS_Compound, TopoDS_CompSolid,\
    topods
from OCC.Core.TopAbs import *

# from aocutils.exceptions import WrongTopologicalType

PY3 = not (int(sys.version.split('.')[0]) <= 2)

# dictionary used to "cast" a shape to the subclass corresponding to its type
topo_factory = {TopAbs_VERTEX: topods.Vertex,
                TopAbs_EDGE: topods.Edge,
                TopAbs_FACE: topods.Face,
                TopAbs_WIRE: topods.Wire,
                TopAbs_SHELL: topods.Shell,
                TopAbs_SOLID: topods.Solid,
                TopAbs_COMPOUND: topods.Compound,
                TopAbs_COMPSOLID: topods.CompSolid}

# key: shape type; value: TopoDS_* subclass
topo_type_class = {TopAbs_VERTEX: TopoDS_Vertex,
                   TopAbs_EDGE: TopoDS_Edge,
                   TopAbs_FACE: TopoDS_Face,
                   TopAbs_WIRE: TopoDS_Wire,
                   TopAbs_SHELL: TopoDS_Shell,
                   TopAbs_SOLID: TopoDS_Solid,
                   TopAbs_COMPOUND: TopoDS_Compound,
                   TopAbs_COMPSOLID: TopoDS_CompSolid}


curve_types_dict = {GeomAbs_Line: "line",
                    GeomAbs_Circle: "circle",
                    GeomAbs_Ellipse: "ellipse",
                    GeomAbs_Hyperbola: "hyperbola",
                    GeomAbs_Parabola: "parabola",
                    GeomAbs_BezierCurve: "bezier",
                    GeomAbs_BSplineCurve: "spline",
                    GeomAbs_OtherCurve: "other"}

surface_types_dict = {GeomAbs_Plane: "plane",
                      GeomAbs_Cylinder: "cylinder",
                      GeomAbs_Cone: "cone",
                      GeomAbs_Sphere: "sphere",
                      GeomAbs_Torus: "torus",
                      GeomAbs_BezierSurface: "bezier",
                      GeomAbs_BSplineSurface: "spline",
                      GeomAbs_SurfaceOfRevolution: "revolution",
                      GeomAbs_SurfaceOfExtrusion: "extrusion",
                      GeomAbs_OffsetSurface: "offset",
                      GeomAbs_OtherSurface: "other"}

state_dict = {TopAbs_IN: "in",
              TopAbs_OUT: "out",
              TopAbs_ON: "on",
              TopAbs_UNKNOWN: "unknown"}

orient_dict = {TopAbs_FORWARD: "TopAbs_FORWARD",
               TopAbs_REVERSED: "TopAbs_REVERSED",
               TopAbs_INTERNAL: "TopAbs_INTERNAL",
               TopAbs_EXTERNAL: "TopAbs_EXTERNAL"}

topo_types_dict = {TopAbs_VERTEX: "vertex",
                   TopAbs_EDGE: "edge",
                   TopAbs_WIRE: "wire",
                   TopAbs_FACE: "face",
                   TopAbs_SHELL: "shell",
                   TopAbs_SOLID: "solid",
                   TopAbs_COMPSOLID: "compsolid",
                   TopAbs_COMPOUND: "compound",
                   TopAbs_SHAPE: "shape"}

geom_types_dict = {GeomAbs_Line: "line",
                   GeomAbs_Circle: "circle",
                   GeomAbs_Ellipse: "ellipse",
                   GeomAbs_Hyperbola: "hyperbola",
                   GeomAbs_Parabola: "parabola",
                   GeomAbs_BezierCurve: "beziercurve",
                   GeomAbs_BSplineCurve: "bsplinecurve",
                   GeomAbs_OtherCurve: "othercurve"}


brep_check_dict = {BRepCheck_NoError: "NoError",
                   BRepCheck_InvalidPointOnCurve: "InvalidPointOnCurve",
                   BRepCheck_InvalidPointOnCurveOnSurface: "InvalidPointOnCurveOnSurface",
                   BRepCheck_InvalidPointOnSurface: "InvalidPointOnSurface",
                   BRepCheck_No3DCurve: "No3DCurve",
                   BRepCheck_Multiple3DCurve: "Multiple3DCurve",
                   BRepCheck_Invalid3DCurve: "Invalid3DCurve",
                   BRepCheck_NoCurveOnSurface: "NoCurveOnSurface",
                   BRepCheck_InvalidCurveOnSurface: "InvalidCurveOnSurface",
                   BRepCheck_InvalidCurveOnClosedSurface: "InvalidCurveOnClosedSurface",
                   BRepCheck_InvalidSameRangeFlag: "InvalidSameRangeFlag",
                   BRepCheck_InvalidSameParameterFlag: "InvalidSameParameterFlag",
                   BRepCheck_InvalidDegeneratedFlag: "InvalidDegeneratedFlag",
                   BRepCheck_FreeEdge: "FreeEdge",
                   BRepCheck_InvalidMultiConnexity: "InvalidMultiConnexity",
                   BRepCheck_InvalidRange: "InvalidRange",
                   BRepCheck_EmptyWire: "EmptyWire",
                   BRepCheck_RedundantEdge: "RedundantEdge",
                   BRepCheck_SelfIntersectingWire: "SelfIntersectingWire",
                   BRepCheck_NoSurface: "NoSurface",
                   BRepCheck_InvalidWire: "InvalidWire",
                   BRepCheck_RedundantWire: "RedundantWire",
                   BRepCheck_IntersectingWires: "IntersectingWires",
                   BRepCheck_InvalidImbricationOfWires: "InvalidImbricationOfWires",
                   BRepCheck_EmptyShell: "EmptyShell",
                   BRepCheck_RedundantFace: "RedundantFace",
                   BRepCheck_UnorientableShape: "UnorientableShape",
                   BRepCheck_NotClosed: "NotClosed",
                   BRepCheck_NotConnected: "NotConnected",
                   BRepCheck_SubshapeNotInShape: "SubshapeNotInShape",
                   BRepCheck_BadOrientation: "BadOrientation",
                   BRepCheck_BadOrientationOfSubshape: "BadOrientationOfSubshape",
                   BRepCheck_InvalidToleranceValue: "InvalidToleranceValue",
                   BRepCheck_CheckFail: "CheckFail"}


class BidirDict(dict):
    """Bi-directional dictionary

    Parameters
    ----------
    iterable
    kwargs

    Raises
    ------
    KeyError if a duplicate value exists (as values must
    also be able to behave as keys)

    """
    def __init__(self, iterable=(), **kwargs):
        self.update(iterable, **kwargs)

    def update(self, iterable=(), **kwargs):
        if hasattr(iterable, 'items'):
            iterable = iterable.items()
        for (key, value) in itertools.chain(iterable, kwargs.items()):
            self[key] = value

    def __setitem__(self, key, value):
        if key in self:
            del self[key]
        if value in self:
            del self[value]
        dict.__setitem__(self, key, value)
        dict.__setitem__(self, value, key)

    def __delitem__(self, key):
        value = self[key]
        dict.__delitem__(self, key)
        dict.__delitem__(self, value)

    def __repr__(self):
        return '%s(%s)' % (type(self).__name__, dict.__repr__(self))


brepcheck_lut = BidirDict(brep_check_dict)
curve_lut = BidirDict(curve_types_dict)
surface_lut = BidirDict(surface_types_dict)
state_lut = BidirDict(state_dict)
orient_lut = BidirDict(orient_dict)
topo_lut = BidirDict(topo_types_dict)
geom_lut = BidirDict(geom_types_dict)

# classes = dir()
# geom_classes = list()
# for elem in classes:
#     if elem.startswith('Geom') and 'swig' not in elem:
#         geom_classes.append(elem)


# def what_is_face(face):
#     """Returns all class names for which this class can be downcasted
#
#     Parameters
#     ----------
#     face : OCC.TopoDS_Shape of type TopAbs_FACE
#
#     Returns
#     -------
#     list
#
#     """
#     if not face.ShapeType() == TopAbs_FACE:
#         msg = '%s type is not TopAbs_FACE. Conversion impossible' % str(face)
#         logger.error(msg)
#         raise WrongTopologicalType(msg)
#
#     # BRep_Tool.Surface() signatures
#     # ------------------------------
#     # static const Handle< Geom_Surface > & 	Surface (const TopoDS_Face &F, TopLoc_Location &L)
#     #         static Handle< Geom_Surface > 	Surface (const TopoDS_Face &F)
#     handle_geom_surface = BRep_Tool_Surface(face)
#     geom_surface = handle_geom_surface.GetObject()
#
#     result = list()
#
#     for elem in classes:
#         if elem.startswith('Geom') and 'swig' not in elem:
#             geom_classes.append(elem)
#
#     for geom_class in geom_classes:
#         if geom_surface.IsKind(geom_class) and geom_class not in result:
#             result.append(geom_class)
#     return result


# def shape_is_cylinder(face):
#     r"""
#
#     Parameters
#     ----------
#     face : TopoDS_Face
#
#     Returns
#     -------
#     bool
#         True is the TopoDS_Shape is a cylinder, False otherwise
#
#     """
#     hs = BRep_Tool_Surface(face)
#     downcast_result = Handle_Geom_CylindricalSurface().DownCast(hs)
#     if downcast_result.IsNull():
#         return False
#     else:
#         return True
