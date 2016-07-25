# -*- coding: utf-8 -*-
from .ccharts import ccharts
import numpy as np

class xbar_mr(ccharts):
    
    def plot(self, ax, data, size):
        assert size == 1

        R = []
        for i in range(len(data) - 1):
            R.append(abs(data[i] - data[i + 1]))

        Rbar = np.mean(R)
        Xbar = np.mean(data)
        
        lclx = Xbar - 3 * (Rbar / 1.128)
        uclx = Xbar + 3 * (Rbar / 1.128)
#        lclr = 0
#        uclr = Rbar + 3 * (Rbar / 1.128)        
        
        ax.plot([0, len(data)], [Xbar, Xbar], 'k-')
        ax.plot([0, len(data)], [lclx, lclx], 'r:')
        ax.plot([0, len(data)], [uclx, uclx], 'r:')
        ax.plot(data, 'bo-')
        
        ax.set_title(self.__class__.__name__.upper())
        
        return (data, Xbar, lclx, uclx)

