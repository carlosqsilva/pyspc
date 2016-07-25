# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
__version__ = '0.1'

# For testing purposes we might need to set mpl backend before any
# other import of matplotlib.
def _set_mpl_backend():
    import os
    import matplotlib as mpl

    env_backend = os.environ.get('MATPLOTLIB_BACKEND')
    if env_backend:
        # we were instructed
        mpl.use(env_backend)

_set_mpl_backend()


#from .ccharts import xbar, tables, rbar, cusum, sbar, ewma, xmr, xbar_mr, p
from .ccharts import *
from .sampledata import *

from .pyspc import spc
from .rules import rules
