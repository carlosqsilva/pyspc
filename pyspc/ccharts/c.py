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

from .ccharts import ccharts
import numpy as np


class c(ccharts):

    _title = "C chart"

    def __init__(self, size=1):
        super(c, self).__init__()

        self.size = size - 1

    def plot(self, data, size, newdata=None):

        sizes, data = data.T
        if self.size == 1:
            sizes, data = data, sizes

        # the samples must have the same size for this charts
        assert np.mean(sizes) == sizes[0]

        cbar = np.mean(data)

        lcl = cbar - 3 * np.sqrt(cbar)
        ucl = cbar + 3 * np.sqrt(cbar)
#
#        ax.plot([0, len(data)], [cbar, cbar], 'k-')
#        ax.plot([0, len(data)], [lcl, lcl], 'r:')
#        ax.plot([0, len(data)], [ucl, ucl], 'r:')
#        ax.plot(data, 'bo-')

        return (data, cbar, lcl, ucl, self._title)
