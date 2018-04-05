#!/usr/bin/env python
# coding: utf-8

r"""
"""

import pytest

from OCC.BRepPrimAPI import BRepPrimAPI_MakeBox
from OCC.TopoDS import TopoDS_Face, TopoDS_Edge, TopoDS_Shape

from aocutils.fixes import fix_shape, fix_face, fix_tolerance, fix_continuity
from aocutils.topology import Topo


@pytest.fixture()
def box_shape():
    r"""Box shape for testing as a pytest fixture"""
    return BRepPrimAPI_MakeBox(10, 20, 30).Shape()


def test_fix_shape(box_shape):
    r"""test shape fixing

    Parameters
    ----------
    box_shape : TopoDS_Shape
        Box shape (pytest fixture)

    """
    # check the result of fixing a shape is a shape
    assert isinstance(fix_shape(box_shape), TopoDS_Shape)


def test_fix_face(box_shape):
    r"""test face fixing

    Parameters
    ----------
    box_shape : TopoDS_Shape
        Box shape (pytest fixture)

    """
    # get a face
    face = Topo(box_shape, return_iter=False).faces[0]

    # check the fixing result is a TopoDS_Face
    assert isinstance(fix_face(face), TopoDS_Face)


def test_fix_tolerance(box_shape):
    r"""test tolerance fixing

    Parameters
    ----------
    box_shape : TopoDS_Shape
        Box shape (pytest fixture)

    """
    fix_tolerance(box_shape)
    assert True


def test_fix_continuity(box_shape):
    r"""test continuity fixing

    Parameters
    ----------
    box_shape : TopoDS_Shape
        Box shape (pytest fixture)

    """
    # get an edge
    edge = Topo(box_shape, return_iter=False).edges[0]

    # test types
    assert isinstance(fix_continuity(edge), TopoDS_Shape)
    assert not isinstance(fix_continuity(edge), TopoDS_Edge)
    assert not fix_continuity(edge).IsNull()

# TODO : test curve resampling
