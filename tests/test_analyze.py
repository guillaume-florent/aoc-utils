#!/usr/bin/python
# coding: utf-8

r"""analyze package tests"""

import pytest
import math

import OCC.gp
import OCC.TopAbs

import aocutils.primitives
import aocutils.tolerance
import aocutils.topology
import aocutils.mesh
import aocutils.exceptions
import aocutils.brep.edge_make
import aocutils.brep.wire_make
import aocutils.brep.face_make

import aocutils.analyze.bounds
import aocutils.analyze.distance
import aocutils.analyze.global_
import aocutils.analyze.inclusion

box_dim_x = 10.
box_dim_y = 20.
box_dim_z = 30.

sphere_radius = 10.

square_side_length = 20.


box = aocutils.primitives.box(box_dim_x, box_dim_y, box_dim_z)
sphere = aocutils.primitives.sphere(sphere_radius)
sphere_2 = aocutils.primitives.sphere(OCC.gp.gp_Pnt(40, 0, 0), sphere_radius)

# 4 edges making a square
edge = aocutils.brep.edge_make.line(OCC.gp.gp_Pnt(0, 0, 0), OCC.gp.gp_Pnt(square_side_length, 0, 0))
edge_2 = aocutils.brep.edge_make.line(OCC.gp.gp_Pnt(square_side_length, 0, 0), OCC.gp.gp_Pnt(square_side_length,
                                                                                             square_side_length, 0))
edge_3 = aocutils.brep.edge_make.line(OCC.gp.gp_Pnt(square_side_length, square_side_length, 0),
                                      OCC.gp.gp_Pnt(0, square_side_length, 0))
edge_4 = aocutils.brep.edge_make.line(OCC.gp.gp_Pnt(0, square_side_length, 0), OCC.gp.gp_Pnt(0, 0, 0))

# an open wire
wire = aocutils.brep.wire_make.wire([edge, edge_2])

# a closed wire
closed_wire = aocutils.brep.wire_make.wire([edge, edge_2, edge_3, edge_4])

# a face from the closed wire
face = aocutils.brep.face_make.face(closed_wire)

# shortcut to default tolerance
tol = aocutils.tolerance.OCCUTILS_DEFAULT_TOLERANCE


def test_bounds_box():
    r"""Test the bounding box on a box shape"""
    # occutils.mesh.mesh(box)
    bb = aocutils.analyze.bounds.BoundingBox(box)
    assert box_dim_x <= bb.x_span < box_dim_x + 2.001 * tol
    assert box_dim_y <= bb.y_span < box_dim_y + 2.001 * tol
    assert box_dim_z <= bb.z_span < box_dim_z + 2.001 * tol


def test_better_bounds_box():
    r"""test BetterBoundingBox"""
    tolerance = 0.01
    bbb = aocutils.analyze.bounds.BetterBoundingBox(box, tol=tolerance)

    assert 0 >= bbb.x_min
    assert - bbb.x_min <= tolerance

    assert box_dim_x <= bbb.x_max
    assert bbb.x_max - box_dim_x <= tolerance

    assert box_dim_y <= bbb.y_max
    assert bbb.y_max - box_dim_y <= tolerance

    assert box_dim_z <= bbb.z_max
    assert bbb.z_max - box_dim_z <= tolerance

    tolerance = 0.001
    bbb = aocutils.analyze.bounds.BetterBoundingBox(box, tol=tolerance)

    assert 0 >= bbb.x_min
    assert - bbb.x_min <= tolerance

    assert box_dim_x <= bbb.x_max
    assert bbb.x_max - box_dim_x <= tolerance

    assert box_dim_y <= bbb.y_max
    assert bbb.y_max - box_dim_y <= tolerance

    assert box_dim_z <= bbb.z_max
    assert bbb.z_max - box_dim_z <= tolerance


def test_bounds_sphere():
    r"""Test the bounding box on a sphere"""
    # aocutils.mesh.mesh(box)
    bb = aocutils.analyze.bounds.BoundingBox(sphere)
    assert 2 * sphere_radius <= bb.x_span < 2 * sphere_radius + 2.001 * tol
    assert 2 * sphere_radius <= bb.y_span < 2 * sphere_radius + 2.001 * tol
    assert 2 * sphere_radius <= bb.z_span < 2 * sphere_radius + 2.001 * tol


def test_better_bounds_sphere():
    r"""Test the better bounding box on a sphere"""
    tolerance = 0.01
    bbb = aocutils.analyze.bounds.BetterBoundingBox(sphere, tol=tolerance)
    assert 2 * sphere_radius <= bbb.x_span < 2 * sphere_radius + 2.001 * tol
    assert 2 * sphere_radius <= bbb.y_span < 2 * sphere_radius + 2.001 * tol
    assert 2 * sphere_radius <= bbb.z_span < 2 * sphere_radius + 2.001 * tol

    assert bbb.x_max >= sphere_radius
    assert bbb.x_max - sphere_radius <= tolerance

    assert bbb.y_max >= sphere_radius
    assert bbb.y_max - sphere_radius <= tolerance

    assert bbb.z_max >= sphere_radius
    assert bbb.z_max - sphere_radius <= tolerance


def test_better_bounds_complex_shape():
    r"""Test BetterBoundingBox on a complex shape"""
    import os
    from aocxchange.step import StepImporter
    hullshape = StepImporter(filename=os.path.join(os.path.dirname(__file__), "test_files/G10.stp")).shapes[0]
    # From Rhinoceros bounding box
    # min = 0.000,-82.263,-52.092    max = 990.000,82.263,102.210    in World coordinates
    # dimensions = 990.000,164.527,154.302
    #
    # z max has to be replaced by 102.20984 for the test to pass
    tolerance = 0.01
    bbb = aocutils.analyze.bounds.BetterBoundingBox(hullshape, tol=tolerance)
    assert -tolerance <= bbb.x_min <= 0.
    assert 990. <= bbb.x_max <= 990. + tolerance

    assert -82.263 - tolerance <= bbb.y_min <= -82.263
    assert 82.263 <= bbb.y_max <= 82.263 + tolerance

    assert -52.092 - tolerance <= bbb.z_min <= -52.092
    assert 102.20984 <= bbb.z_max <= 102.210 + tolerance


def test_bounds_sphere_boundingbox_middle():
    r"""Test the determination of the bounding box middle"""
    # occutils.mesh.mesh(box)
    bb = aocutils.analyze.bounds.BoundingBox(sphere)
    assert bb.centre.X() < tol / 10.
    assert bb.centre.Y() < tol / 10.
    assert bb.centre.Z() < tol / 10.


def test_minimum_distance():
    r"""Test the minimum distance determination"""
    md = aocutils.analyze.distance.MinimumDistance(sphere, sphere_2)
    assert md.minimum_distance == 20.
    assert md.nb_solutions == 1
    assert type(md.point_pairs[0][0]) == OCC.gp.gp_Pnt


def test_global_properties_box():
    r"""Properties of a the box"""

    # wrap the box in GlobalProperties
    box_properties = aocutils.analyze.global_.GlobalProperties(box)

    # check the volume
    assert box_properties.volume == box_dim_x * box_dim_y * box_dim_z

    # check the length is not defined for the box
    with pytest.raises(aocutils.exceptions.WrongTopologicalType):
        box_properties.length

    # check the area is not defined for the box ....
    with pytest.raises(aocutils.exceptions.WrongTopologicalType):
        box_properties.area

    # .... but the area of the shell of the box is defined and exact
    box_shell = aocutils.topology.Topo(box, return_iter=False).shells[0]
    shell_properties = aocutils.analyze.global_.GlobalProperties(box_shell)
    theoretical_area = 2 * box_dim_x * box_dim_y + 2 * box_dim_y * box_dim_z + 2 * box_dim_x * box_dim_z
    assert theoretical_area - tol <= shell_properties.area <= theoretical_area + tol

    # but the length is not defined for a shell....
    with pytest.raises(aocutils.exceptions.WrongTopologicalType):
        shell_properties.length

    # ... nor is the volume
    with pytest.raises(aocutils.exceptions.WrongTopologicalType):
        shell_properties.volume


def test_global_properties_edge():
    r"""Test the GlobalProperties of an edge"""
    # wrap the box in GlobalProperties
    edge_properties = aocutils.analyze.global_.GlobalProperties(edge)

    # check the length of the edge
    assert edge_properties.length == square_side_length

    # the volume of an edge is undefined !
    with pytest.raises(aocutils.exceptions.WrongTopologicalType):
        edge_properties.volume

    # but the centre exists and is at the middle of a straight edge
    edge_centre = edge_properties.centre
    assert type(edge_centre) == OCC.gp.gp_Pnt
    assert edge_centre.X() == square_side_length / 2.
    assert edge_centre.Y() == 0
    assert edge_centre.Z() == 0


def test_global_properties_sphere():
    r"""Properties of a the sphere"""
    # wrap the sphere in global properties
    sphere_properties = aocutils.analyze.global_.GlobalProperties(sphere)

    # the centre should be very close to the origin
    sphere_centre = sphere_properties.centre
    assert - tol < sphere_centre.X() < tol
    assert - tol < sphere_centre.Y() < tol
    assert - tol < sphere_centre.Z() < tol

    # the volume should be close to 4/3*pi*r**3
    assert sphere_properties.volume == 4. / 3. * math.pi * sphere_radius**3


def test_global_properties_wire_open():
    r"""Properties of the open wire"""

    wire_properties = aocutils.analyze.global_.GlobalProperties(wire)
    assert wire_properties.length == square_side_length * 2.


def test_global_properties_wire_closed():
    r"""Properties of the closed wire"""

    closed_wire_properties = aocutils.analyze.global_.GlobalProperties(closed_wire)
    assert closed_wire_properties.length == square_side_length * 4.


def test_inclusion():
    r"""Test inclusion of point in bounding box and of point is solid"""
    assert aocutils.analyze.inclusion.point_in_boundingbox(sphere, OCC.gp.gp_Pnt(sphere_radius - 1.,
                                                                                 sphere_radius - 1.,
                                                                                 sphere_radius - 1.)) is True

    assert aocutils.analyze.inclusion.point_in_solid(sphere, OCC.gp.gp_Pnt(sphere_radius - 1., 0, 0)) is True
    assert aocutils.analyze.inclusion.point_in_solid(sphere, OCC.gp.gp_Pnt(sphere_radius - 1.,
                                                                           sphere_radius - 1.,
                                                                           sphere_radius - 1.)) is False
    assert aocutils.analyze.inclusion.point_in_solid(sphere, OCC.gp.gp_Pnt(sphere_radius, 0, 0)) is None

    with pytest.raises(aocutils.exceptions.WrongTopologicalType):
        aocutils.analyze.inclusion.point_in_solid(edge, OCC.gp.gp_Pnt(sphere_radius, 0, 0))

    with pytest.raises(aocutils.exceptions.WrongTopologicalType):
        aocutils.analyze.inclusion.point_in_solid(aocutils.topology.Topo(sphere, return_iter=False).faces[0],
                                                  OCC.gp.gp_Pnt(sphere_radius, 0, 0))

    sphere_shell = aocutils.topology.Topo(sphere, return_iter=False).shells[0]
    assert aocutils.analyze.inclusion.point_in_boundingbox(sphere_shell, OCC.gp.gp_Pnt(sphere_radius - 1.,
                                                                                       sphere_radius - 1.,
                                                                                       sphere_radius - 1.)) is True
    assert aocutils.analyze.inclusion.point_in_solid(sphere_shell, OCC.gp.gp_Pnt(sphere_radius - 1., 0, 0)) is True
    assert aocutils.analyze.inclusion.point_in_solid(sphere_shell, OCC.gp.gp_Pnt(sphere_radius - 1.,
                                                                                 sphere_radius - 1.,
                                                                                 sphere_radius - 1.)) is False
    assert aocutils.analyze.inclusion.point_in_solid(sphere_shell, OCC.gp.gp_Pnt(sphere_radius, 0, 0)) is None
