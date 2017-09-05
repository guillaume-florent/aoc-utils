#!/usr/bin/env python
# coding: utf-8

r"""Tests for the operations/intersect.py module"""

from OCC.BRepPrimAPI import BRepPrimAPI_MakeSphere, BRepPrimAPI_MakeBox

from aocutils.operations.intersect import intersect_shape_by_half_line


def test_intersect_sphere():
    r"""Test intersect using a sphere"""
    radius = 10.0
    sphere = BRepPrimAPI_MakeSphere(radius).Shape()

    intersection_points = intersect_shape_by_half_line(sphere,
                                                       x=11., y=0., z=0.,
                                                       vx=-1, vy=0, vz=0)
    assert len(intersection_points) == 2
    assert intersection_points[0].X() == 10.
    assert intersection_points[1].X() == -10.

    intersection_points = intersect_shape_by_half_line(sphere,
                                                       x=-11., y=0., z=0.,
                                                       vx=1, vy=0, vz=0)
    assert len(intersection_points) == 2
    assert intersection_points[0].X() == -10.
    assert intersection_points[1].X() == 10.

    intersection_points = intersect_shape_by_half_line(sphere,
                                                       x=-9., y=0., z=0.,
                                                       vx=1, vy=0, vz=0)
    assert len(intersection_points) == 1
    assert intersection_points[0].X() == 10.

    intersection_points = intersect_shape_by_half_line(sphere,
                                                       x=-9., y=0., z=0.,
                                                       vx=-1, vy=0, vz=0)
    assert len(intersection_points) == 1
    assert intersection_points[0].X() == -10.


def test_intersect_box():
    r"""Test intersect using a sphere"""
    dx = 10.0
    dy = 20.0
    dz = 30.0
    box = BRepPrimAPI_MakeBox(dx, dy, dz).Shape()

    intersection_points = intersect_shape_by_half_line(box,
                                                       x=1., y=1., z=0.,
                                                       vx=0, vy=1, vz=0)
    assert len(intersection_points) == 1
    assert intersection_points[0].Y() == dy

    intersection_points = intersect_shape_by_half_line(box,
                                                       x=1., y=1., z=0.,
                                                       vx=0, vy=-1, vz=0)
    assert len(intersection_points) == 1
    assert intersection_points[0].Y() == 0.

    intersection_points = intersect_shape_by_half_line(box,
                                                       x=1., y=-1., z=1.,
                                                       vx=0, vy=1, vz=0)
    assert len(intersection_points) == 2
    assert intersection_points[0].Y() == 0.
    assert intersection_points[1].Y() == dy

    intersection_points = intersect_shape_by_half_line(box,
                                                       x=1., y=-1., z=0.,
                                                       vx=0, vy=1, vz=0)
    assert len(intersection_points) == 2
    assert intersection_points[0].Y() == 0.
    assert intersection_points[1].Y() == dy

    intersection_points = intersect_shape_by_half_line(box,
                                                       x=1., y=0., z=0.,
                                                       vx=0, vy=1, vz=0)
    assert len(intersection_points) == 2
    assert intersection_points[0].Y() == 0.
    assert intersection_points[1].Y() == dy

    intersection_points = intersect_shape_by_half_line(box,
                                                       x=1., y=0.000001, z=0.,
                                                       vx=0, vy=1, vz=0)
    assert len(intersection_points) == 1
    assert intersection_points[0].Y() == dy

    intersection_points = intersect_shape_by_half_line(box,
                                                       x=1., y=-1., z=-0.0001,
                                                       vx=0, vy=1, vz=0)
    assert len(intersection_points) == 0
