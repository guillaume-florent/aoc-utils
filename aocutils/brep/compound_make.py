# coding: utf-8

r"""core/compound_make.py"""

from OCC.TopoDS import TopoDS_Builder, TopoDS_Compound


def compound(topo):
    r"""Accumulate a bunch of TopoDS_* in list `topo`
    to a OCC.TopoDS.TopoDS_Compound

    Parameters
    ----------
    topo : list[TopoDS_*]

    Returns
    -------
    OCC.TopoDS.TopoDS_Compound

    """
    bd = TopoDS_Builder()
    comp = TopoDS_Compound()
    bd.MakeCompound(comp)
    for i in topo:
        bd.Add(comp, i)
    return comp
