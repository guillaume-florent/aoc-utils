# coding: utf-8

r"""Random generation of vectors, colors, materials ..., mostly aimed at
examples and demos.

"""

import logging

import numpy as np

from OCC.gp import gp_Vec
from OCC import Graphic3d
from OCC.Graphic3d import Graphic3d_MaterialAspect

from aocutils.display.color import color

logger = logging.getLogger(__name__)


def random_vec():
    r"""Random vector

    Returns
    -------
    gp_Vec
        A random vector with components between -1 and 1

    """
    x, y, z = [np.random.uniform(-1, 1) for _ in range(3)]
    return gp_Vec(x, y, z)


def random_colored_material_aspect():
    r"""Random colored material aspect

    Returns
    -------
    OCC.Graphic3d.Graphic3d_MaterialAspect

    """
    # noinspection PyUnresolvedReferences
    clrs = [i for i in dir(OCC.Graphic3d) if i.startswith('Graphic3d_NOM_')]
    col = np.random.sample(clrs, 1)[0]
    logger.info('Color : %s' % str(col))
    # noinspection PyUnresolvedReferences
    return Graphic3d_MaterialAspect(getattr(Graphic3d, col))


def random_color():
    r"""Random color generation

    Returns
    -------
    Quantity_Color

    """
    return color(np.random.random(), np.random.random(), np.random.random())
