#!/usr/bin/env python
# coding: utf-8

r"""Tests for the real_bb_position() function in analyse/bounds.py module"""

from OCC.BRepPrimAPI import BRepPrimAPI_MakeSphere, BRepPrimAPI_MakeBox
from aocutils.analyze.bounds import BoundingBox

from aocutils.analyze.bounds import real_bb_position


def test_with_sphere():
    r"""Test the bounding box workaround with a sphere"""
    radius = 10.0
    sphere = BRepPrimAPI_MakeSphere(radius).Shape()
    bb = BoundingBox(sphere)
    increment = 0.01

    bbw_x_min = real_bb_position("X", "MIN", bb.x_min, sphere, increment=increment)
    bbw_x_max = real_bb_position("X", "MAX", bb.x_max, sphere, increment=increment)

    bbw_y_min = real_bb_position("Y", "MIN", bb.y_min, sphere, increment=increment)
    bbw_y_max = real_bb_position("Y", "MAX", bb.y_max, sphere, increment=increment)

    bbw_z_min = real_bb_position("Z", "MIN", bb.z_min, sphere, increment=increment)
    bbw_z_max = real_bb_position("Z", "MAX", bb.z_max, sphere, increment=increment)

    assert bb.x_min < -radius
    assert bb.x_max > radius

    assert bb.y_min < -radius
    assert bb.y_max > radius

    assert bb.z_min < -radius
    assert bb.z_max > radius

    assert bbw_x_min <= - radius
    assert abs(bbw_x_min - (-radius)) <= 2 * increment

    assert bbw_x_max >= radius
    assert abs(bbw_x_max - radius) <= 2 * increment

    assert bbw_y_min <= - radius
    assert abs(bbw_y_min - (-radius)) <= 2 * increment

    assert bbw_y_max >= radius
    assert abs(bbw_y_max - radius) <= 2 * increment

    assert bbw_z_min <= - radius
    assert abs(bbw_z_min - (-radius)) <= 2 * increment

    assert bbw_z_max >= radius
    assert abs(bbw_z_max - radius) <= 2 * increment


def test_with_box():
    r"""Test the bounding box workaround with a box"""
    dx = 10.0
    dy = 20.0
    dz = 30.0

    # Make a box with a corner at 0,0,0 and the other dx,dy,dz
    box = BRepPrimAPI_MakeBox(dx, dy, dz).Shape()
    bb = BoundingBox(box)
    increment = 0.01

    bbw_x_min = real_bb_position("X", "MIN", bb.x_min, box, increment=increment)
    bbw_x_max = real_bb_position("X", "MAX", bb.x_max, box, increment=increment)

    bbw_y_min = real_bb_position("Y", "MIN", bb.y_min, box, increment=increment)
    bbw_y_max = real_bb_position("Y", "MAX", bb.y_max, box, increment=increment)

    bbw_z_min = real_bb_position("Z", "MIN", bb.z_min, box, increment=increment)
    bbw_z_max = real_bb_position("Z", "MAX", bb.z_max, box, increment=increment)

    assert bb.x_min < 0.
    assert bb.x_max > dx

    assert bb.y_min < 0.
    assert bb.y_max > dy

    assert bb.z_min < 0.
    assert bb.z_max > dz

    assert bbw_x_min <= 0.
    assert abs(bbw_x_min) <= 2 * increment

    assert bbw_x_max >= dx
    assert abs(bbw_x_max - dx) <= 2 * increment

    assert bbw_y_min <= 0.
    assert abs(bbw_y_min) <= 2 * increment

    assert bbw_y_max >= dy
    assert abs(bbw_y_max - dy) <= 2 * increment

    assert bbw_z_min <= 0.
    assert abs(bbw_z_min) <= 2 * increment

    assert bbw_z_max >= dz
    assert abs(bbw_z_max - dz) <= 2 * increment
