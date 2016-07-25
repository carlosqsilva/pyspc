# -*- coding: utf-8 -*-
from .ccharts import ccharts
import numpy as np
from .tables import d2

class cusum(ccharts):
    def __init__(self, target = None, std = None, interval = 4):
        super(cusum, self).__init__()        
        
        self.target = target
        self.std = std
        self.interval = interval
    
    def plot(self, ax, data, size):
        
        if size > 1:
            data = np.mean(data, axis =1)
        
        target = self.target
        std = self.std
        interval = self.interval           
        
           
        if target is None:
            target = np.mean(data)

        if std is None:
            rbar = []
            for i in range(len(data) - 1):
                rbar.append(abs(data[i] - data[i + 1]))
            std = np.mean(rbar)/1.128
        
        k = std/2
        
        cplus = [] #values
        cminus = [] #values
        i, j = 0, 0
        for xi in data:
            cplus.append(max([0, xi - (target + k) + i]))
            cminus.append(min([0, xi - (target - k) + j]))
            i, j = cplus[-1], cminus[-1]
        
        lcl = -interval * std
        ucl = interval * std
        center = 0
               
        ax.plot([0, len(cplus)], [center, center], 'k-')
        ax.plot([0, len(cplus)], [lcl, lcl], 'r:')
        ax.plot([0, len(cplus)], [ucl, ucl], 'r:')
        ax.plot(cplus, 'bo-')
        ax.plot(cminus, 'bo-')
        ax.set_title(self.__class__.__name__.upper())
        
        return ([cplus, cminus], center, lcl, ucl)
        
        
    