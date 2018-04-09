#!/usr/bin/env python
# coding: utf-8

r""""""


from __future__ import print_function

import os
import sys
import time

try:
    import scipy
    import scipy.optimize
    HAVE_SCIPY = True
except ImportError:
    HAVE_SCIPY = False

from OCC.Core.gp import gp_Pnt
from OCC.Core.BRepAdaptor import BRepAdaptor_HCurve
from OCC.Core.BRep import BRep_Builder, BRep_Tool
from OCC.Core.ShapeAnalysis import ShapeAnalysis_Surface
from OCC.Core.GeomLProp import GeomLProp_SLProps
from OCC.Core.BRepFill import BRepFill_CurveConstraint
from OCC.Core.GeomPlate import GeomPlate_MakeApprox, \
    GeomPlate_BuildPlateSurface, GeomPlate_PointConstraint
from OCC.Core.IGESControl import IGESControl_Reader
from OCC.Core.IFSelect import IFSelect_ItemsByEntity, IFSelect_RetDone
from OCC.Display.SimpleGui import init_display
from OCC.Core.TopoDS import TopoDS_Compound
# import OCC.GeomAbs

from corelib.core.files import path_from_file

from aocutils.brep.wire_make import closed_polygon
from aocutils.brep.face_make import n_sided, face
from aocutils.brep.vertex_make import vertex
from aocutils.topology import Topo, WireExplorer

display, start_display, add_menu, add_function_to_menu = init_display()


class IGESImporter(object):
    r"""IGES File Importer"""
    def __init__(self, filename=None):
        self._shapes = []
        self._filename = None
        self.nbs = 0
        if not os.path.isfile(filename):
            raise AssertionError("IGESImporter initialization Error: "
                                 "file %s not found." % filename)
        self.filename = filename

    @property
    def filename(self):
        r"""Filename : str"""
        return self._filename

    @filename.setter
    def filename(self, value):
        if not os.path.isfile(value):
            raise AssertionError("IGESImporter initialization Error: "
                                 "file %s not found." % value)
        else:
            self._filename = value

    def read_file(self):
        """Read the IGES file and stores the result in a list of TopoDS_Shape"""
        a_reader = IGESControl_Reader()
        status = a_reader.ReadFile(self._filename)
        if status == IFSelect_RetDone:
            failsonly = False
            a_reader.PrintCheckLoad(failsonly, IFSelect_ItemsByEntity)
            nbr = a_reader.NbRootsForTransfer()
            a_reader.PrintCheckTransfer(failsonly, IFSelect_ItemsByEntity)
            # ok = a_reader.TransferRoots()
            for _ in range(1, nbr + 1):
                self.nbs = a_reader.NbShapes()
                if self.nbs == 0:
                    # The program stops !!!! Why ?
                    print("At least one shape in IGES cannot be transferred")
                elif nbr == 1 and self.nbs == 1:
                    a_res_shape = a_reader.Shape(1)
                    if a_res_shape.IsNull():
                        print("At least one shape in IGES "
                              "cannot be transferred")
                    self._shapes.append(a_res_shape)
                else:
                    for i in range(1, self.nbs+1):
                        a_shape = a_reader.Shape(i)
                        if a_shape.IsNull():
                            print("At least one shape in STEP "
                                  "cannot be transferred")
                        else:
                            self._shapes.append(a_shape)
            return True
        else:
            print("Error: can't read file %s" % self._filename)
            return False

    def get_compound(self):
        r"""Create and returns a compound from the _shapes list"""
        # Create a compound
        compound = TopoDS_Compound()
        builder = BRep_Builder()
        builder.MakeCompound(compound)
        # Populate the compound
        for shape in self._shapes:
            builder.Add(compound, shape)
        return compound

    @property
    def shapes(self):
        r"""List of shapes"""
        return self._shapes


def geom_plate(event=None):
    r"""Build and display the geom plate

    Called by the 1st menu item

    """
    display.EraseAll()
    p1 = gp_Pnt(0, 0, 0)
    p2 = gp_Pnt(0, 10, 0)
    p3 = gp_Pnt(0, 10, 10)
    p4 = gp_Pnt(0, 0, 10)
    p5 = gp_Pnt(5, 5, 5)

    # poly is a TopoDS_Wire
    poly = closed_polygon([p1, p2, p3, p4])

    # list of TopoDS_Edge
    edges = [edge for edge in Topo(poly).edges]

    # C1 and C2 fail (C0 (default) works) - face is a TopoDS_Face
    face = n_sided(edges, [p5])

    display.DisplayShape(edges)
    # display.DisplayShape(occutils.construct.make_vertex(p5))
    display.DisplayShape(p5)
    display.DisplayShape(face, update=True)

# ============================================================================
# Find a surface where the radius at the vertex is n
# ============================================================================


def build_plate(polygon, points):
    r"""Build a surface from a constraining polygon(s) and point(s)

    Parameters
    ----------
    polygon : list of polygons ( TopoDS_Shape)
    points : list of points ( gp_Pnt )

    Returns
    -------
    TopoDS_Face

    """
    # plate surface
    bp_srf = GeomPlate_BuildPlateSurface(3, 15, 2)

    # add curve constraints
    for poly in polygon:
        for edg in WireExplorer(poly).ordered_edges:
            c = BRepAdaptor_HCurve()
            c.ChangeCurve().Initialize(edg)
            constraint = BRepFill_CurveConstraint(c.GetHandle(), 0)
            bp_srf.Add(constraint.GetHandle())

    # add point constraint
    for pt in points:
        bp_srf.Add(GeomPlate_PointConstraint(pt, 0).GetHandle())
        bp_srf.Perform()

    max_seg, max_deg, crit_order = 9, 8, 0
    tol = 1e-4
    dmax = max([tol, 10 * bp_srf.G0Error()])

    srf = bp_srf.Surface()
    plate = GeomPlate_MakeApprox(srf, tol, max_seg, max_deg, dmax, crit_order)
    u_min, u_max, v_min, v_max = srf.GetObject().Bounds()

    return face(plate.Surface(), u_min, u_max, v_min, v_max, 1e-4)


def radius_at_uv(face, u, v):
    r"""Radius of curvature at u, v

    Parameters
    ----------
    face :
        surface input
    u :
        u coordinate
    v :
        v coordinate

    Returns
    -------
    float
        The radius of curvature at u, v

    """
    h_srf = BRep_Tool.Surface(face)
    # uv_domain = GeomLProp_SurfaceTool().Bounds(h_srf)
    curvature = GeomLProp_SLProps(h_srf, u, v, 1, 1e-6)
    try:
        _crv_min = 1. / curvature.MinCurvature()
    except ZeroDivisionError:
        _crv_min = 0.

    try:
        _crv_max = 1. / curvature.MaxCurvature()
    except ZeroDivisionError:
        _crv_max = 0.
    return abs((_crv_min + _crv_max) / 2.)


def uv_from_projected_point_on_face(face, pt):
    r"""Returns the u, v coordinates of a projected point on a face

    Parameters
    ----------
    face
    pt

    Returns
    -------

    """
    surface = BRep_Tool.Surface(face)
    surface_shape_analysis = ShapeAnalysis_Surface(surface)
    uv = surface_shape_analysis.ValueOfUV(pt, 1e-2)
    print('distance', surface_shape_analysis.Value(uv).Distance(pt))
    return uv.Coord()


class RadiusConstrainedSurface(object):
    r"""returns a surface that has `radius` at `pt`"""
    def __init__(self, display_, poly, pnt, target_radius):
        self.display = display_
        self.targetRadius = target_radius
        self.poly = poly
        self.pnt = pnt
        self.curr_radius = None
        self.plate = None
        self.build_surface()

    def build_surface(self):
        r"""Builds and renders the plate"""
        self.plate = build_plate([self.poly], [self.pnt])
        self.display.EraseAll()
        self.display.DisplayShape(self.plate)
        vert = vertex(self.pnt)
        self.display.DisplayShape(vert, update=True)

    def radius(self, z):
        r"""Sets the height of the point constraining the plate.

        Parameters
        ----------
        z : float
            Height of the point

        Returns
        -------
        float
            Difference between target radius and measured radius

        """
        if isinstance(z, float):
            self.pnt.SetX(z)
        else:
            self.pnt.SetX(float(z[0]))
        self.build_surface()
        uv = uv_from_projected_point_on_face(self.plate, self.pnt)
        print(uv)
        radius = radius_at_uv(self.plate, uv.X(), uv.Y())
        print('z: %f radius: %f ' % (z, radius))
        self.curr_radius = radius
        return self.targetRadius - abs(radius)

    def solve(self):
        r"""Solve"""
        scipy.optimize.fsolve(self.radius, 1, maxfev=1000)
        return self.plate


def solve_radius(event=None):
    r"""Solve radius

    Called by 2nd menu item

    """
    display.EraseAll()
    p1 = gp_Pnt(0, 0, 0)
    p2 = gp_Pnt(0, 10, 0)
    p3 = gp_Pnt(0, 10, 10)
    p4 = gp_Pnt(0, 0, 10)
    p5 = gp_Pnt(5, 5, 5)
    poly = closed_polygon([p1, p2, p3, p4])
    for i in scipy.arange(0.1, 3., 0.2).tolist():
        radius_constrained_surface = RadiusConstrainedSurface(display,
                                                              poly,
                                                              p5,
                                                              i)
        _ = radius_constrained_surface.solve()
        print('Goal: %s radius: %s' % (i,
                                       radius_constrained_surface.curr_radius))
        time.sleep(0.5)


def build_geom_plate(edges):
    r"""

    Parameters
    ----------
    edges

    Returns
    -------
    face
    """
    bp_srf = GeomPlate_BuildPlateSurface(3, 9, 12)

    # add curve constraints
    for edg in edges:
        c = BRepAdaptor_HCurve()
        print('edge:', edg)
        c.ChangeCurve().Initialize(edg)
        constraint = BRepFill_CurveConstraint(c.GetHandle(), 0)
        bp_srf.Add(constraint.GetHandle())

    # add point constraint
    try:
        bp_srf.Perform()
    except RuntimeError:
        print('Failed to build the geom plate surface')

    srf = bp_srf.Surface()
    plate = GeomPlate_MakeApprox(srf, 1e-04, 100, 9, 1e-03, 0)

    u_min, u_max, v_min, v_max = srf.GetObject().Bounds()
    face = face(plate.Surface(), u_min, u_max, v_min, v_max, 1e-6)
    return face


def build_curve_network(event=None):
    r"""Mimic the curve network surfacing command from rhino

    Called by the 3rd menu item

    """
    print('Importing IGES file...', end='')
    iges = IGESImporter(path_from_file(__file__, './curve_geom_plate.igs'))
    iges.read_file()
    iges_cpd = iges.get_compound()
    print('done.')

    print('Building geomplate...', end='')
    topo = Topo(iges_cpd)
    edges_list = list(topo.edges)
    face = build_geom_plate(edges_list)
    print('done.')
    display.EraseAll()
    display.DisplayShape(edges_list)
    display.DisplayShape(face)
    display.FitAll()
    print('Cutting out of edges...')
    # Make a wire from outer edges
    # _edges = [edges_list[2], edges_list[3], edges_list[4], edges_list[5]]
    # outer_wire = make_wire(_edges)


def exit_(event=None):
    r"""Exit the display"""
    sys.exit()

if __name__ == "__main__":
    add_menu('geom plate')
    add_function_to_menu('geom plate', geom_plate)
    if HAVE_SCIPY:
        add_function_to_menu('geom plate', solve_radius)
    add_function_to_menu('geom plate', build_curve_network)
    add_function_to_menu('geom plate', exit_)
    start_display()
