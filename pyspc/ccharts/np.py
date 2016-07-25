# -*- coding: utf-8 -*-
from .ccharts import ccharts
import numpy

class np(ccharts):
    def __init__(self, size = 1):
        super(np, self).__init__()
        
        self.size = size - 1
    
    def plot(self, ax, data, size):
        
        sizes, data = data.T        
        if self.size == 1:
            sizes, data = data, sizes
            
        # the samples must have the same size for this charts
        assert numpy.mean(sizes) == sizes[0]
        
        p = numpy.mean([float(d) / sizes[0] for d in data])
        pbar = numpy.mean(data)
                                           
        lcl = pbar - 3*numpy.sqrt(pbar*(1 - p))
        ucl = pbar + 3*numpy.sqrt(pbar*(1 - p))
    
        ax.plot([0, len(data)], [pbar, pbar], 'k-')
        ax.plot([0, len(data)], [lcl, lcl], 'r:')
        ax.plot([0, len(data)], [ucl, ucl], 'r:')
        ax.plot(data, 'bo-')
        
        ax.set_title(self.__class__.__name__.upper())
        
        return (data, pbar, lcl, ucl)
        