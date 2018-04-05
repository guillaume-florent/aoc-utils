# coding: utf-8

r"""shell module of aocutils"""

import logging

from OCC.TopoDS import TopoDS_Shell
from OCC.ShapeAnalysis import ShapeAnalysis_Shell
from OCC.BRepCheck import BRepCheck_Shell, BRepCheck_NoError

from aocutils.topology import Topo
from aocutils.brep.base import BaseObject
from aocutils.exceptions import WrongTopologicalType

logger = logging.getLogger(__name__)


class Shell(BaseObject):
    r"""Shell class

    Parameters
    ----------
    topods_shell : TopoDS_Shell

    """
    _n = 0

    def __init__(self, topods_shell):
        if not isinstance(topods_shell, TopoDS_Shell):
            msg = 'need a TopoDS_Shell, got a %s' % topods_shell.__class__
            logger.critical(msg)
            raise WrongTopologicalType(msg)

        # assert not topods_shell.IsNull()
        if topods_shell.IsNull():
            msg = "topods_shell is Null"
            logger.error(msg)
            raise ValueError(msg)

        BaseObject.__init__(self, topods_shell, 'shell')

        Shell._n += 1

    @property
    def topods_shell(self):
        return self._wrapped_instance

    def check(self):
        r"""Super class abstract method implementation"""
        shell_check = BRepCheck_Shell(self._wrapped_instance)
        check_orientation = shell_check.Orientation()

        if check_orientation != BRepCheck_NoError:
            return False
        else:
            return True

    @property
    def is_closed(self):
        r"""Is the shell closed?

        Returns
        -------
        bool
            True if closed, False otherwise

        """
        shell_check = BRepCheck_Shell(self._wrapped_instance)
        check_closed = shell_check.Closed()
        if check_closed == BRepCheck_NoError:
            return True
        else:
            return False

    @property
    def is_open(self):
        return not self.is_closed

    def analyse(self):
        r"""Bad edges of the shell"""
        bad_edges = list()
        ss = ShapeAnalysis_Shell()
        ss.LoadShells(self._wrapped_instance)
        if ss.HasFreeEdges():
            bad_edges = [e for e in Topo(ss.BadEdges()).edges]
        return bad_edges

    def faces(self):
        r"""Faces of the shell"""
        return Topo(self._wrapped_instance, return_iter=True).faces

    def wires(self):
        r"""Wires of the shell"""
        return Topo(self._wrapped_instance, return_iter=True).wires

    def edges(self):
        r"""Edges of the shell"""
        return Topo(self._wrapped_instance, return_iter=True).edges
