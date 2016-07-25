# -*- coding: utf-8 -*-
from .ccharts import ccharts
from .tables import A2
import numpy as np

class xbar(ccharts):
    
    def plot(self, ax, data, size):
        assert size >= 2
        
        Rsum = 0
        Xbar = [] #values
        for xs in data:
            assert len(xs) == size
            Rsum += max(xs) - min(xs)
            Xbar.append(np.mean(xs))

        Rbar = Rsum / len(data)
        X_bar = np.mean(Xbar) #center

        lcl = X_bar - A2[size] * Rbar
        ucl = X_bar + A2[size] * Rbar
        
        ax.plot([0, len(Xbar)], [X_bar, X_bar], 'k-')
        ax.plot([0, len(Xbar)], [lcl, lcl], 'r:')
        ax.plot([0, len(Xbar)], [ucl, ucl], 'r:')
        ax.plot(Xbar, 'bo-')
        
        return (Xbar, X_bar, lcl, ucl)
        
        
