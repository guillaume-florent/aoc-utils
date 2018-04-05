# coding=utf-8

r"""Triangulation"""

from __future__ import print_function

from OCC.Core.BRepMesh import BRepMesh_FastDiscret
from OCC.Core.Bnd import Bnd_Box
from OCC.Core.BRepBndLib import brepbndlib_Add
from OCC.Core.TopTools import TopTools_IndexedDataMapOfShapeListOfShape,\
    TopTools_ListOfShape

# import aocutils.common
from aocutils.topology import Topo
from aocutils.tolerance import OCCUTILS_DEFAULT_TOLERANCE


def vertices_faces_from_shape(shape, deflection=0.1):
    r"""Vertices and faces of the mesh that represents the BREP

    Parameters
    ----------
    shape: TopoDS_Shape

    """
    list_of_shape = TopTools_ListOfShape()
    list_of_shape.Append(shape)

    indexed_data_map_of_shape_list_of_shape = TopTools_IndexedDataMapOfShapeListOfShape()
    indexed_data_map_of_shape_list_of_shape.Add(shape, list_of_shape)

    bbox = Bnd_Box()
    bbox.SetGap(OCCUTILS_DEFAULT_TOLERANCE)
    brepbndlib_Add(shape, bbox)

    # These arguments are *SO* random...
    fd = BRepMesh_FastDiscret(0.1, 0.1, bbox, False, False, False, False)
    for f in Topo(shape).faces:
        fd.Add(f, indexed_data_map_of_shape_list_of_shape)
    n_vert, n_edge, n_face = fd.NbVertices(), fd.NbEdges(), fd.NbTriangles()
    print('number of mesh vertices, edges, triangles representing the BREP:', n_vert, n_edge, n_face)
    tris = [fd.Triangle(i) for i in range(1, fd.NbTriangles())]
    verts = [fd.Vertex(i) for i in range(1, fd.NbVertices())]

    print(tris)
    print(verts)


if __name__ == '__main__':
    from OCC.BRepPrimAPI import BRepPrimAPI_MakeSphere
    sphere = BRepPrimAPI_MakeSphere(1).Shape()
    vertices_faces_from_shape(sphere)
