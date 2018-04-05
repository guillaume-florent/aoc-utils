# coding: utf-8

r"""OCC collections utilities and conversions"""

from OCC.TColgp import TColgp_Array1OfPnt, TColgp_Array1OfPnt2d
from OCC.TCollection import TCollection_ExtendedString


def to_string(_string):
    r"""str to OCC string conversion

    Parameters
    ----------
    _string : str

    Returns
    -------
    TCollection_ExtendedString

    """
    return TCollection_ExtendedString(_string)


def to_tcol_(_list, collection_type):
    r"""Convert a Python list to OCC.TColgp* collection_type

    Parameters
    ----------
    _list : list
    collection_type : OCC.TColgp.*
        The OCC collection geom_type to convert to

    Returns
    -------
    Handle to collection_type

    """
    array = collection_type(1, len(_list) + 1)
    for n, i in enumerate(_list):
        array.SetValue(n + 1, i)
    return array.GetHandle()


def tcol_dim_1(li, _type, start_at_one=False):
    r"""function factory for 1-dimensional TCol* types

    Parameters
    ----------
    li : list[object]
        The list that is used to populate the OCC collection
    _type : type
        The OCC collection geom_type
    start_at_one : bool
        Determines if the first index of the OCC collection will be 0 or 1

    Returns
    -------
    _type

    """
    if start_at_one:
        pts = _type(1, len(li))
        for i, element in enumerate(li):
            pts.SetValue(i+1, element)
    else:
        pts = _type(0, len(li)-1)
        for i, element in enumerate(li):
            pts.SetValue(i, element)
    pts.thisown = False
    return pts


def point_list_to_tcolgp_array1_of_pnt(li):
    r"""Populate a TColgp_Array1OfPnt with a list of points

    Parameters
    ----------
    li : list[gp_Pnt]

    Returns
    -------
    TColgp_Array1OfPnt

    """
    pts = TColgp_Array1OfPnt(0, len(li) - 1)
    for n, i in enumerate(li):
        pts.SetValue(n, i)
    return pts


def point2d_list_to_tcolgp_array1_of_pnt2d(li):
    r"""

    Parameters
    ----------
    li : list[gp_Pnt2d]

    Returns
    -------
    TColgp_Array1OfPnt2d

    """
    return tcol_dim_1(li, TColgp_Array1OfPnt2d)
