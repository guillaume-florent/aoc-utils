# coding: utf-8

r"""Boolean operations"""

import logging

import OCC
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Common, BRepAlgoAPI_Cut, \
    BRepAlgoAPI_Fuse

from aocutils.exceptions import BooleanCommonException, BooleanCutException

logger = logging.getLogger(__name__)


def common(shape_1, shape_2):
    r"""Boolean operation : Common

    Parameters
    ----------
    shape_1 : TopoDS_Shape
    shape_2 : TopoDS_Shape

    Returns
    -------
    OCC.TopoDS.TopoDS_Shape

    """
    algo_common = BRepAlgoAPI_Common(shape_1, shape_2)

    # BuilderCanWork() does not exist in v7.*.*
    if OCC.VERSION[0] != '7':
        logger.debug(f"BRepAlgoAPI_Common.BuilderCanWork()? : {algo_common.BuilderCanWork()}")

    if OCC.VERSION[0] != '7':
        _error = {0: '- Ok',
                  1: '- The Object is created but Nothing is Done',
                  2: '- Null source shapes is not allowed',
                  3: '- Check types of the arguments',
                  4: '- Can not allocate memory for the DSFiller',
                  5: '- The Builder can not work with such types of arguments',
                  6: '- Unknown operation is not allowed',
                  7: '- Can not allocate memory for the Builder'}

        if algo_common.ErrorStatus() != 0:
            try:
                msg = _error[algo_common.ErrorStatus()]
            except KeyError:
                msg = f"Unknown error : %s" % str(algo_common.ErrorStatus())
            logger.error(msg)
            raise BooleanCommonException()
        else:
            logger.debug(f"BRepAlgoAPI_Common status: {_error[algo_common.ErrorStatus()]}")

    return algo_common.Shape()


def cut(shape_to_cut_from, cutting_shape):
    r"""Boolean cut

    Parameters
    ----------
    shape_to_cut_from : OCC.TopoDS.TopoDS_Shape
    cutting_shape : OCC.TopoDS.TopoDS_Shape

    Returns
    -------
    OCC.TopoDS.TopoDS_Shape

    """
    try:
        brep_cut = BRepAlgoAPI_Cut(shape_to_cut_from, cutting_shape)
        logger.info('Can work ? : %s' % str(brep_cut.BuilderCanWork()))
        _error = {0: '- Ok',
                  1: '- The Object is created but Nothing is Done',
                  2: '- Null source shapes is not allowed',
                  3: '- Check types of the arguments',
                  4: '- Can not allocate memory for the DSFiller',
                  5: '- The Builder can not work with such types of arguments',
                  6: '- Unknown operation is not allowed',
                  7: '- Can not allocate memory for the Builder'}
        logger.info('Error status : %s' % str(_error[brep_cut.ErrorStatus()]))
        brep_cut.RefineEdges()
        brep_cut.FuseEdges()
        shp = brep_cut.Shape()
        brep_cut.Destroy()
        return shp
    except:
        msg = "Failed to boolean cut"
        logger.error(msg)
        raise BooleanCutException(msg)


def fuse(shape_to_cut_from, joining_shape):
    r"""Boolean fuse

    Parameters
    ----------
    shape_to_cut_from : OCC.TopoDS.TopoDS_Shape
    joining_shape : OCC.TopoDS.TopoDS_Shape

    Returns
    -------
    OCC.TopoDS.TopoDS_Shape

    """
    join = BRepAlgoAPI_Fuse(shape_to_cut_from, joining_shape)
    if OCC.VERSION[0] != '7':
        join.RefineEdges()
        join.FuseEdges()
    shape = join.Shape()
    # join.Destroy()
    return shape
