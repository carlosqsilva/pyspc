#!/usr/bin/env python3
#
# Copyright (C) 2016  Carlos Henrique Silva <carlosqsilva@outlook.com>
#
# This library is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# from __future__ import (absolute_import, division, print_function,
#                         unicode_literals)
from .results import PlotCharts

import matplotlib.pyplot as plt
import matplotlib as mpl

import numpy as np
import pandas as pd

plt.style.use('grayscale')
mpl.rcParams['lines.markersize'] = 4


class spc(object):
    """
    spc is the main class of the library. It receive the data, plot the chart
    drop values and save the image to a file.

    :param data: Can be a list, nested list, numpy.array or pandas.Dataframe
    :param newdata: the same of above

    :Example:

    >>> import numpy
    >>> from pyspc import *
    >>> fake_data = numpy.random.randn(30, 5) + 100
    >>> chart1 = spc(fake_data) + xbar_rbar() + rbar() + rules()
    >>> print(chart1)

    """

    _title = 'SPC : Statistical Process Control Charts for Humans'

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

    def save(self, filename, **kwargs):
        """
        Save the chart to a image file.

        :param filename: name of the image file, if no extenssion is provide it will be save as '.png'.
        :param **kwargs: see matplotlib.figure.Figure.savefig for more details. 
        """
        if len(self.summary) == 0:
            self.make()

        self.fig.savefig(filename, **kwargs)

    def drop(self, *args):
        self.data = np.delete(self.data, args, axis=0)

    def make(self, **kwargs):
        num_layers = len(self.layers)
        if num_layers == 0:
            plt.show()
            return

        self.fig, *self.subplots = plt.subplots(num_layers, **kwargs)
        self.fig.canvas.set_window_title(self._title)

        for layer, ax in zip(self.layers, self.get_subplots()):
            summary = {}

            values, center, lcl, ucl, title = layer.plot(self.data, self.size, self.newdata)
            PlotCharts(ax, values, center, lcl, ucl, title)

            summary['name'] = title
            summary['values'] = values
            summary['lcl'] = lcl
            summary['ucl'] = ucl
            summary['center'] = center

            if self.points is not None:
                summary['violation-points'] = self.points.plot_violation_points(ax, values, center, lcl, ucl)

            self.summary = summary

        self.fig.tight_layout()
