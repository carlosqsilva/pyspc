# -*- coding: utf-8 -*-
from .ccharts import ccharts
import numpy as np

class p(ccharts):
    def __init__(self, size = 1):
        super(p, self).__init__()
        
        self.size = size - 1
    
    def plot(self, ax, data, size):
        
        sizes, data = data.T        
        if self.size == 1:
            sizes, data = data, sizes
        
        data2 = data / sizes
        pbar = np.mean(data2)
        
        for n in sizes:
            assert n*pbar >= 5
            assert n*(1 - pbar) >=5
        
        if np.mean(sizes) == sizes[0]:
            size = sizes[0]
            
            lcl = pbar - 3*np.sqrt((pbar*(1 - pbar))/size)
            ucl = pbar + 3*np.sqrt((pbar*(1 - pbar))/size)
            
            if lcl < 0: lcl = 0                
            if ucl > 1: ucl = 1
            
            ax.plot([0, len(data2)], [pbar, pbar], 'k-')
            ax.plot([0, len(data2)], [lcl, lcl], 'r:')
            ax.plot([0, len(data2)], [ucl, ucl], 'r:')
            ax.plot(data2, 'bo-')
            
        else:
            lcl, ucl = [], []
            for size in sizes:
                lcl.append(pbar - 3*np.sqrt((pbar*(1 - pbar))/size))
                ucl.append(pbar + 3*np.sqrt((pbar*(1 - pbar))/size))
                            
            ax.plot([0, len(data2)], [pbar, pbar], 'k-')
            ax.step(lcl, 'r', where='mid')
            ax.step(ucl, 'r', where='mid')
            ax.plot(data2, 'bo-')
        
        ax.set_title(self.__class__.__name__.upper())
        return (data2, pbar, lcl, ucl)
