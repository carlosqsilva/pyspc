#!/usr/bin/python3
#
#Copyright (C) 2016  Carlos Henrique Silva <carlosqsilva@outlook.com>
#
#This library is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#This library is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import matplotlib.pyplot as plt
import matplotlib as mpl

import numpy as np
import pandas as pd

plt.style.use('grayscale')
mpl.rcParams['lines.markersize'] = 5

class spc(object):
    
    _title = 'SPC : Statistical Process Control for humans'
    
    def __init__(self, data=None, newdata=None):
        
        
        if isinstance(data, pd.DataFrame):
            data = data.values
        if isinstance(newdata, pd.DataFrame):
            newdata = newdata.values
        
        try:
            self.size = len(data[0])
        except:
            if not isinstance(data[0], (list, tuple, np.ndarray)):
                self.size = 1
        
        self.data = data
        self.newdata = newdata
        self.layers = []
        self.points = None
        self.summary = []

    def __repr__(self):
        self.make()
        plt.tight_layout()
        plt.show()
        return "<pyspc: (%d)>" % self.__hash__()
        
    def __getitem__(self, i):
        return self.summary[i]
    
    def __iter__(self):
        for x in self.summary:
            yield x
        
    def get_subplots(self):

        if len(self.layers) > 1:
            return self.subplots[0]
        return self.subplots

    def save(self, filename, width=None, height=None):

        self.make()
        w, h = self.fig.get_size_inches()
        if width and height:
            w, h = width, height
        
        self.fig.set_size_inches(w, h)
        self.fig.savefig(filename)

    def drop(self, *args):
        self.data = np.delete(self.data, args, axis=0)

    def make(self):
        
        num_layers = len(self.layers)
        if num_layers == 0:
            plt.show()
            return

        self.fig, *self.subplots = plt.subplots(num_layers)
        self.fig.canvas.set_window_title(self._title)
        
        for layer, ax in zip(self.layers, self.get_subplots()):
            summary = {}
            values, center, lcl, ucl = layer.plot(ax, self.data, self.size, self.newdata)

            if self.points is not None:
                violation_points = self.points.plot_violation_points(ax, values, center, lcl, ucl)
            
            summary['name'] = layer.__class__.__name__
            summary['values'] = values
            summary['lcl'] = lcl
            summary['ucl'] = ucl
            summary['center'] = center
            summary['violation_points'] = violation_points
            self.summary.append(summary)
