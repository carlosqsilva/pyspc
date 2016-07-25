# -*- coding: utf-8 -*-
from .ccharts import ccharts
import numpy as np

class c(ccharts):
    def __init__(self, size = 1):
        super(c, self).__init__()
        
        self.size = size - 1
    
    def plot(self, ax, data, size):
        
        sizes, data = data.T        
        if self.size == 1:
            sizes, data = data, sizes
            
        # the samples must have the same size for this charts
        assert np.mean(sizes) == sizes[0]
        
        cbar = np.mean(data)
        
        lcl = cbar - 3*np.sqrt(cbar)
        ucl = cbar + 3*np.sqrt(cbar)
        
        ax.plot([0, len(data)], [cbar, cbar], 'k-')
        ax.plot([0, len(data)], [lcl, lcl], 'r:')
        ax.plot([0, len(data)], [ucl, ucl], 'r:')
        ax.plot(data, 'bo-')
        
        ax.set_title(self.__class__.__name__.upper())
        
        return (data, cbar, lcl, ucl)
        
