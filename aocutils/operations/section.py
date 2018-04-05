# coding: utf-8

r"""Section operation"""


from OCC.BRepFill import BRepFill_NSections
from OCC.TopTools import TopTools_SequenceOfShape


def n_sections(edges):
    r"""

    Parameters
    ----------
    edges : list[OCC.TopoDS.TopoDS_Edge]

    Returns
    -------
    BRepFill_NSections

    """
    seq = TopTools_SequenceOfShape()
    for i in edges:
        seq.Append(i)
    n_sec = BRepFill_NSections(seq, True)
    return n_sec
