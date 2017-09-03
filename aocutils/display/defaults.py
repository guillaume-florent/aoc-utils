# coding: utf-8

r"""default display options"""

from __future__ import division

from aocutils.display.backends import available_backends

backend = "wx"

if backend not in available_backends():
    msg = "%s backend is not available" % backend
    # CORRECTED BUG : topology imports defaults (this file) and logger.error
    # is called before logging.basicConfig -> the logging format is not used
    # logger.error(msg)
    raise ValueError(msg)


