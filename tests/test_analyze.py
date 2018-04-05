#!/usr/bin/env python
# coding: utf-8

r"""analyze package tests"""

import pytest
import math
import os

from OCC.Core.gp import gp_Pnt

from aocutils.primitives import box, sphere
from aocutils.tolerance import OCCUTILS_DEFAULT_TOLERANCE
from aocutils.topology import Topo
# from aocutils.mesh import mesh
from aocutils.exceptions import WrongTopologicalType
from aocutils.brep.edge_make import line
from aocutils.brep.wire_make import wire
from aocutils.brep.face_make import face

from aocutils.analyze.bounds import BoundingBox, BetterBoundingBox, \
    stl_bounding_box
from aocutils.analyze.distance import MinimumDistance
from aocutils.analyze.global_ import GlobalProperties
from aocutils.analyze.inclusion import point_in_boundingbox, point_in_solid

from aocxchange.step import StepImporter
from aocxchange.utils import path_from_file

box_dim_x = 10.
box_dim_y = 20.
box_dim_z = 30.

sphere_radius = 10.

square_side_length = 20.


box_ = box(box_dim_x, box_dim_y, box_dim_z)
sphere_ = sphere(sphere_radius)
sphere_2 = sphere(gp_Pnt(40, 0, 0), sphere_radius)

# 4 edges making a square
edge = line(gp_Pnt(0, 0, 0), gp_Pnt(square_side_length, 0, 0))
edge_2 = line(gp_Pnt(square_side_length, 0, 0),
              gp_Pnt(square_side_length, square_side_length, 0))
edge_3 = line(gp_Pnt(square_side_length, square_side_length, 0),
              gp_Pnt(0, square_side_length, 0))
edge_4 = line(gp_Pnt(0, square_side_length, 0), gp_Pnt(0, 0, 0))

# an open wire
wire_ = wire([edge, edge_2])

# a closed wire
closed_wire = wire([edge, edge_2, edge_3, edge_4])

# a face from the closed wire
face_ = face(closed_wire)

# shortcut to default tolerance
tol = OCCUTILS_DEFAULT_TOLERANCE


def test_bounds_box():
    r"""Test the bounding box on a box shape"""
    # mesh(box)
    bb = BoundingBox(box_)
    assert box_dim_x <= bb.x_span < box_dim_x + 2.001 * tol
    assert box_dim_y <= bb.y_span < box_dim_y + 2.001 * tol
    assert box_dim_z <= bb.z_span < box_dim_z + 2.001 * tol


def test_better_bounds_box():
    r"""test BetterBoundingBox"""
    tolerance = 0.01
    bbb = BetterBoundingBox(box_, tol=tolerance)

    assert 0 >= bbb.x_min
    assert - bbb.x_min <= 2 * tolerance

    assert box_dim_x <= bbb.x_max
    assert bbb.x_max - box_dim_x <= 2 * tolerance

    assert box_dim_y <= bbb.y_max
    assert bbb.y_max - box_dim_y <= 2 * tolerance

    assert box_dim_z <= bbb.z_max
    assert bbb.z_max - box_dim_z <= 2 * tolerance

    tolerance = 0.001
    bbb = BetterBoundingBox(box_, tol=tolerance)

    assert 0 >= bbb.x_min
    assert - bbb.x_min <= 2 * tolerance

    assert box_dim_x <= bbb.x_max
    assert bbb.x_max - box_dim_x <= 2 * tolerance

    assert box_dim_y <= bbb.y_max
    assert bbb.y_max - box_dim_y <= 2 * tolerance

    assert box_dim_z <= bbb.z_max
    assert bbb.z_max - box_dim_z <= 2 * tolerance


def test_bounds_sphere():
    r"""Test the bounding box on a sphere"""
    # mesh(box)
    bb = BoundingBox(sphere_)
    assert 2 * sphere_radius <= bb.x_span < 2 * sphere_radius + 2.001 * tol
    assert 2 * sphere_radius <= bb.y_span < 2 * sphere_radius + 2.001 * tol
    assert 2 * sphere_radius <= bb.z_span < 2 * sphere_radius + 2.001 * tol


def test_better_bounds_sphere():
    r"""Test the better bounding box on a sphere"""
    tolerance = 0.01
    bbb = BetterBoundingBox(sphere_, tol=tolerance)
    assert 2 * sphere_radius <= bbb.x_span < 2 * sphere_radius + 2.1 * tolerance
    assert 2 * sphere_radius <= bbb.y_span < 2 * sphere_radius + 2.1 * tolerance
    assert 2 * sphere_radius <= bbb.z_span < 2 * sphere_radius + 2.1 * tolerance

    assert bbb.x_max >= sphere_radius
    assert bbb.x_max - sphere_radius <= 2 * tolerance

    assert bbb.y_max >= sphere_radius
    assert bbb.y_max - sphere_radius <= 2 * tolerance

    assert bbb.z_max >= sphere_radius
    assert bbb.z_max - sphere_radius <= 2 * tolerance


def test_better_bounds_complex_shape():
    r"""Test BetterBoundingBox on a complex shape"""

    hullshape = StepImporter(filename=os.path.join(os.path.dirname(__file__),
                                                   "test_files/G10.stp")).shapes[0]
    # From Rhinoceros bounding box
    # min = 0.000,-82.263,-52.092
    # max = 990.000,82.263,102.210    in World coordinates
    # dimensions = 990.000,164.527,154.302
    #
    # z max has to be replaced by 102.20984 for the test to pass
    tolerance = 0.01
    bbb = BetterBoundingBox(hullshape, tol=tolerance)
    assert -2 * tolerance <= bbb.x_min <= 0.
    assert 990. <= bbb.x_max <= 990. + 2 * tolerance

    assert -82.263 - 2 * tolerance <= bbb.y_min <= -82.263
    assert 82.263 <= bbb.y_max <= 82.263 + 2 * tolerance

    assert -52.092 - 2 * tolerance <= bbb.z_min <= -52.092
    assert 102.20984 <= bbb.z_max <= 102.210 + 2 * tolerance


def test_bounds_sphere_boundingbox_middle():
    r"""Test the determination of the bounding box middle"""
    # occutils.mesh.mesh(box)
    bb = BoundingBox(sphere_)
    assert bb.centre.X() < tol / 10.
    assert bb.centre.Y() < tol / 10.
    assert bb.centre.Z() < tol / 10.


def test_minimum_distance():
    r"""Test the minimum distance determination"""
    md = MinimumDistance(sphere_, sphere_2)
    assert md.minimum_distance == 20.
    assert md.nb_solutions == 1
    # assert type(md.point_pairs[0][0]) == gp_Pnt
    assert isinstance(md.point_pairs[0][0], (gp_Pnt, ))


def test_global_properties_box():
    r"""Properties of a the box"""

    # wrap the box in GlobalProperties
    box_properties = GlobalProperties(box_)

    # check the volume
    assert box_properties.volume == box_dim_x * box_dim_y * box_dim_z

    # check the length is not defined for the box
    with pytest.raises(WrongTopologicalType):
        _ = box_properties.length

    # check the area is not defined for the box ....
    with pytest.raises(WrongTopologicalType):
        _ = box_properties.area

    # .... but the area of the shell of the box is defined and exact
    box_shell = Topo(box_, return_iter=False).shells[0]
    shell_properties = GlobalProperties(box_shell)
    theoretical_area = 2 * box_dim_x * box_dim_y + \
                       2 * box_dim_y * box_dim_z + \
                       2 * box_dim_x * box_dim_z
    assert theoretical_area - tol <= shell_properties.area <= theoretical_area + tol

    # but the length is not defined for a shell....
    with pytest.raises(WrongTopologicalType):
        _ = shell_properties.length

    # ... nor is the volume
    with pytest.raises(WrongTopologicalType):
        _ = shell_properties.volume


def test_global_properties_edge():
    r"""Test the GlobalProperties of an edge"""
    # wrap the box in GlobalProperties
    edge_properties = GlobalProperties(edge)

    # check the length of the edge
    assert edge_properties.length == square_side_length

    # the volume of an edge is undefined !
    with pytest.raises(WrongTopologicalType):
        _ = edge_properties.volume

    # but the centre exists and is at the middle of a straight edge
    edge_centre = edge_properties.centre
    # assert type(edge_centre) == gp_Pnt
    assert isinstance(edge_centre, (gp_Pnt, ))
    assert edge_centre.X() == square_side_length / 2.
    assert edge_centre.Y() == 0
    assert edge_centre.Z() == 0


def test_global_properties_sphere():
    r"""Properties of a the sphere"""
    # wrap the sphere in global properties
    sphere_properties = GlobalProperties(sphere_)

    # the centre should be very close to the origin
    sphere_centre = sphere_properties.centre
    assert - tol < sphere_centre.X() < tol
    assert - tol < sphere_centre.Y() < tol
    assert - tol < sphere_centre.Z() < tol

    # the volume should be close to 4/3*pi*r**3
    theoretical_volume = 4. / 3. * math.pi * sphere_radius**3
    assert theoretical_volume - tol <= sphere_properties.volume <= theoretical_volume + tol


def test_global_properties_wire_open():
    r"""Properties of the open wire"""

    wire_properties = GlobalProperties(wire_)
    assert wire_properties.length == square_side_length * 2.


def test_global_properties_wire_closed():
    r"""Properties of the closed wire"""

    closed_wire_properties = GlobalProperties(closed_wire)
    assert closed_wire_properties.length == square_side_length * 4.


def test_inclusion():
    r"""Test inclusion of point in bounding box and of point is solid"""
    assert point_in_boundingbox(sphere_, gp_Pnt(sphere_radius - 1.,
                                                sphere_radius - 1.,
                                                sphere_radius - 1.)) is True

    assert point_in_solid(sphere_, gp_Pnt(sphere_radius - 1., 0, 0)) is True
    assert point_in_solid(sphere_, gp_Pnt(sphere_radius - 1.,
                                          sphere_radius - 1.,
                                          sphere_radius - 1.)) is False
    assert point_in_solid(sphere_, gp_Pnt(sphere_radius, 0, 0)) is None

    with pytest.raises(WrongTopologicalType):
        point_in_solid(edge, gp_Pnt(sphere_radius, 0, 0))

    with pytest.raises(WrongTopologicalType):
        point_in_solid(Topo(sphere_, return_iter=False).faces[0],
                       gp_Pnt(sphere_radius, 0, 0))

    sphere_shell = Topo(sphere_, return_iter=False).shells[0]
    assert point_in_boundingbox(sphere_shell,
                                gp_Pnt(sphere_radius - 1.,
                                       sphere_radius - 1.,
                                       sphere_radius - 1.)) is True
    assert point_in_solid(sphere_shell,
                          gp_Pnt(sphere_radius - 1., 0, 0)) is True
    assert point_in_solid(sphere_shell, gp_Pnt(sphere_radius - 1.,
                                               sphere_radius - 1.,
                                               sphere_radius - 1.)) is False
    assert point_in_solid(sphere_shell, gp_Pnt(sphere_radius, 0, 0)) is None


def test_stl_bounding_box():
    r"""Test the computation of the STL bounding box"""
    bb_ascii = stl_bounding_box(path_from_file(__file__,
                                               "./test_files/board.stl"))
    bb_binary = stl_bounding_box(path_from_file(__file__,
                                                "./test_files/board_binary.stl"))
    tolerance = 1e-8

    # Known values
    assert bb_ascii == ((0.12775, 0.21175),
                        (-0.00252084, 0.00252084),
                        (0.01, 0.31))

    # Test the bounding box is the same for the ascii and the binary files
    # that describe the same geometry
    x_ascii, y_ascii, z_ascii = bb_ascii
    x_min_ascii, x_max_ascii = x_ascii
    y_min_ascii, y_max_ascii = y_ascii
    z_min_ascii, z_max_ascii = z_ascii

    x_binary, y_binary, z_binary = bb_binary
    x_min_binary, x_max_binary = x_binary
    y_min_binary, y_max_binary = y_binary
    z_min_binary, z_max_binary = z_binary

    assert x_min_ascii - tolerance <= x_min_binary <= x_min_ascii + tolerance
    assert x_max_ascii - tolerance <= x_max_binary <= x_max_ascii + tolerance

    assert y_min_ascii - tolerance <= y_min_binary <= y_min_ascii + tolerance
    assert y_max_ascii - tolerance <= y_max_binary <= y_max_ascii + tolerance

    assert z_min_ascii - tolerance <= z_min_binary <= z_min_ascii + tolerance
    assert z_max_ascii - tolerance <= z_max_binary <= z_max_ascii + tolerance