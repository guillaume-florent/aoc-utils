# coding: utf-8

r"""solid module of aocutils"""

import logging

from OCC.Core.TopoDS import TopoDS_Solid

from aocutils.topology import Topo
from aocutils.brep.base import BaseObject
from aocutils.brep.shell import Shell
from aocutils.exceptions import WrongTopologicalType

logger = logging.getLogger(__name__)


class Solid(BaseObject):
    r"""Solid class

    Parameters
    ----------
        topods_solid : TopoDS_Solid

    """
    def __init__(self, topods_solid):
        if not isinstance(topods_solid, TopoDS_Solid):
            msg = 'need a TopoDS_Solid, got a %s' % topods_solid.__class__
            logger.critical(msg)
            raise WrongTopologicalType(msg)
        # assert not topods_solid.IsNull()
        if topods_solid.IsNull():
            msg = 'topods_solid is Null'
            logger.error(msg)
            raise ValueError(msg)
        BaseObject.__init__(self, topods_solid, 'solid')

        # self.global_properties =
        #                        occutils.analyze.global_.GlobalProperties(self)

    @property
    def topods_solid(self):
        r"""Wrapped solid

        Returns
        -------
        TopoDS_Solid"""
        return self._wrapped_instance

    def shells(self):
        r"""Shells making the solid

        Returns
        -------
        list[Shell]

        """
        return (Shell(sh) for sh in Topo(self._wrapped_instance))
