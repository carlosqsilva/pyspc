# -*- coding: utf-8 -*-
from .pyspc import spc

class rules(object):
    
    def __init__(self, rules = 1):
        self.layers = self
        self.rules = rules
        
        # default : BASIC
        if rules == 1:
            self.rules = [self.RULE_1_BEYOND_3SIGMA,
                          self.RULE_7_ON_ONE_SIDE]
        # WECO
#        if rules == 2:
#            self.rules = [self.RULES_1_BEYOND_3SIGMA,
#                          self.RULES_2_OF_3_BEYOND_2SIGMA,
#                          self.RULES_4_OF_5_BEYOND_1SIGMA,
#                          self.RULES_8_ON_ONE_SIDE,
#                          self.RULES_6_TRENDING, RULES_14_UP_DOWN]
            
    def __radd__(self, model):
        if isinstance(model, spc):
            model.points = self.layers
            return model

        self.layers.append(model)
        return self
        
        
    def test_violating_runs(self, data, center, lcl, ucl):
        for i in range(1, len(data)):
            if (data[i-1] - center)*(data[i] - center) < 0:
                return False
        return True
        
        
    def RULE_1_BEYOND_3SIGMA(self, ax, values, center, lcl, ucl):
        #points = []
        for i in range(len(values)):
            if values[i] > ucl or values[i] < lcl:
                ax.plot([i], values[i], 'ro')
                #points.append(i)
        #return points
        
    def RULE_7_ON_ONE_SIDE(self, ax, values, center, lcl, ucl):
        #points = []
        num = 7
        for i in range(len(values)):
            if i <= (num - 1):
                continue
            if self.test_violating_runs(values[i - num+1:i + 1], center, lcl, ucl):
                ax.plot([i], values[i], 'yo')
                #points.append(i)
        #return points
        
        
    def plot_violation_points(self, ax, values, center, lcl, ucl):
        violating_points = []
        for func in self.rules:
            violating_points.append(func(ax, values, center, lcl, ucl))
#        return violating_points
        
        
#    def plot(self, ax, values, center, lcl, ucl):
#        
#        violation_points = self.find_violating_points(values, center, lcl, ucl)
#        colors = ['ro', 'yo']
#        
#        for color in colors:
#            for points in violation_points:
#                ax.plot
#                
#        
#        
#        if RULES_7_ON_ONE_SIDE in self.violating_points:
#            for i in self.violating_points[RULES_7_ON_ONE_SIDE]:
#                ax.plot([i], [self._data[i]], "yo")
#        if RULES_1_BEYOND_3SIGMA in self.violating_points:
#            for i in self.violating_points[RULES_1_BEYOND_3SIGMA]:
#                ax.plot([i], [self._data[i]], "ro")
