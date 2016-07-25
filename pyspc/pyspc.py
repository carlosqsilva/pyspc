# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import matplotlib.pyplot as plt
import matplotlib as mpl

import numpy as np
import pandas as pd

plt.style.use('grayscale')
mpl.rcParams['toolbar'] = 'None'

TITLE = 'SPC : Statistical Process Control for humans'

class spc(object):
    
    def __init__(self, data = None):
        
        self.data = data
        
        if isinstance(data, pd.DataFrame):
            self.data = data.values
        
        
        self.size = len(self.data[0])
        
        if not isinstance(self.data[0], (list, tuple, np.ndarray)):
            self.size = 1
        
        self.layers = []
        self.facets = None
        
        #check for out of control points
        self.points = None

                 
    def __repr__(self):
        self.make()
        
        plt.show()
        return "<pyspc: (%d)>" % self.__hash__()
        
    def get_facets(self):
        
        if len(self.layers) > 1:
            return self.subplots[0]
        return self.subplots
        
    def save(self, filename, width=None, height=None):
        
        self.make()
        w, h = self.fig.get_size_inches()
        if width:
            w = width
        if height:
            h = height
        self.fig.set_size_inches(w, h)
        self.fig.savefig(filename)
        
    def drop(self, *args):
        self.data = np.delete(self.data, args, axis=0)
    
    def set_limits(self, ax):
        #change de y limits of the graph
        ylim = ax.get_ylim()
        factor = 0.08
        new_ylim = (ylim[0] + ylim[1])/2 + np.array((-0.5, 0.5)) * (ylim[1] - ylim[0]) * (1 + factor) 
        ax.set_ylim(new_ylim)
        
        #Change x ticks
        xlim = ax.get_xlim()
        new_xlim = (0, len(self.data)) + np.array((-0.3, 0.3))
        ax.set_xlim(new_xlim)
        ax.xaxis.set_ticks(np.arange(*xlim, 2))
        
    def make(self):
        plt.close()
        
        if len(self.layers) == 0:
            plt.show()
            return
            
        self.fig, *self.subplots = plt.subplots(len(self.layers))
        self.fig.canvas.set_window_title(TITLE)
        
        for layer, ax in zip(self.layers, self.get_facets()):
            
            values, center, lcl, ucl = layer.plot(ax, self.data, self.size)
            
            if self.points is not None:
                self.points.plot_violation_points(ax, values, center, lcl, ucl)
            
            self.set_limits(ax)
        
                    
                
                