# -*- coding: utf-8 -*-
from .ccharts import ccharts
import numpy as np

class ewma(ccharts):
    def __init__(self, target = None, weight = 0.2):
        super(ewma, self).__init__()        
        
        self.target = target
        self.weight = weight
    
    def plot(self, ax, data, size):
        assert ((self.weight > 0) and (self.weight < 1))
        
        if size > 1:
            data = np.mean(data, axis =1)
        
        target = self.target
        weight = self.weight
        
        #calculate the target with not given
        if target is None:
            target = np.mean(data)

        # calculate the standard deviation
        rbar = []
        std = 0
        for i in range(len(data) - 1):
            rbar.append(abs(data[i] - data[i + 1]))
        std = np.mean(rbar)/1.128
        
                
        ewma = [] #values
        i = target
        for x in data:
            ewma.append(weight*x+(1-weight)*i)
            i = ewma[-1]
        
        lcl, ucl = [], []
        for i in range(1, len(data)+1):
            lcl.append(target - 3*(std)*np.sqrt((weight/(2-weight)) * (1-(1-weight)**(2*i))))
            ucl.append(target + 3*(std)*np.sqrt((weight/(2-weight)) * (1-(1-weight)**(2*i))))

        ax.plot([0, len(ewma)], [target, target], 'k-')
        ax.plot(lcl, 'r:')
        ax.plot(ucl, 'r:')
        ax.plot(ewma, 'bo-')
        ax.set_title(self.__class__.__name__.upper())
                        
        return (ewma, target, lcl, ucl)
