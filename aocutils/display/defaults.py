#!/usr/bin/python
# coding: utf-8

r"""default display options"""

from __future__ import division

import aocutils.display.backends
import aocutils.display.color

backend = "wx"

if backend not in aocutils.display.backends.available_backends():
    msg = "%s backend is not available" % backend
    # CORRECTED BUG : topology imports defaults (this file) and logger.error
    # is called before logging.basicConfig -> the logging format is not used
    # logger.error(msg)
    raise ValueError(msg)


