# -*- coding: utf-8 -*-
from .ccharts import ccharts
import numpy as np

class u(ccharts):
    def __init__(self, size = 1):
        super(u, self).__init__()
        
        self.size = size - 1
    
    def plot(self, ax, data, size):
        
        sizes, data = data.T        
        if self.size == 1:
            sizes, data = data, sizes
        
        data2 = data / sizes
        ubar = np.sum(data) / np.sum(sizes)
        
        lcl, ucl = [], []
        for i in sizes:
            lcl.append(ubar - 3*np.sqrt(ubar/i))
            ucl.append(ubar + 3*np.sqrt(ubar/i))
        
        ax.plot([0, len(data2)], [ubar, ubar], 'k-')
        ax.step(lcl, 'r', where='mid')
        ax.step(ucl, 'r', where='mid')
        ax.plot(data2, 'bo-')
        
        ax.set_title(self.__class__.__name__.upper())
        return (data2, ubar, lcl, ucl)