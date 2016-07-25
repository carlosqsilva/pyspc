# -*- coding: utf-8 -*-
from .ccharts import ccharts
import numpy as np

class xmr(ccharts):
    
    def plot(self, ax, data, size):
        assert size == 1

        R = []
        for i in range(len(data) - 1):
            R.append(abs(data[i] - data[i + 1]))

        Rbar = np.mean(R)
#        Xbar = np.mean(data)
        
#        lclx = Xbar - 3 * (Rbar / 1.128)
#        uclx = Xbar + 3 * (Rbar / 1.128)
        lclr = 0
        uclr = Rbar + 3 * (Rbar / 1.128)        
        
        ax.plot([0, len(data)], [Rbar, Rbar], 'k-')
        ax.plot([0, len(data)], [lclr, lclr], 'r:')
        ax.plot([0, len(data)], [uclr, uclr], 'r:')
        ax.plot(range(1, len(data)), R, 'bo-')
        
        ax.set_title(self.__class__.__name__.upper())
        
        return (R, Rbar, lclr, uclr)
