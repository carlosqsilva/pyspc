# -*- coding: utf-8 -*-
from .ccharts import ccharts
from .tables import A3, B3, B4
import numpy as np

class sbar(ccharts):
    
    def plot(self, ax, data, size):
        
        assert size >= 2
        assert size <= 10

        s = []
        x = []
        for xs in data:
            assert len(xs) == size
            s.append(np.std(xs, ddof=1))
            x.append(np.mean(xs))

        sbar = np.mean(s)
        xbar = np.mean(x)

#        lclx = xbar + A3[size] * sbar
#        uclx = xbar - A3[size] * sbar

        lcls = B3[size] * sbar
        ucls = B4[size] * sbar
        
        ax.plot([0, len(s)], [sbar, sbar], 'k-')
        ax.plot([0, len(s)], [lcls, lcls], 'r:')
        ax.plot([0, len(s)], [ucls, ucls], 'r:')
        ax.plot(s, 'bo-')
        
        return (s, sbar, lcls, ucls)