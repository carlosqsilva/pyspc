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
import numpy


class np(ccharts):

    _title = "NP Chart"

    def __init__(self, size=1):
        super(np, self).__init__()

        self.size = size - 1

    def plot(self, data, size, newdata=None):

        sizes, data = data.T
        if self.size == 1:
            sizes, data = data, sizes

        # the samples must have the same size for this charts
        assert numpy.mean(sizes) == sizes[0]

        p = numpy.mean([float(d) / sizes[0] for d in data])
        pbar = numpy.mean(data)

        lcl = pbar - 3 * numpy.sqrt(pbar * (1 - p))
        ucl = pbar + 3 * numpy.sqrt(pbar * (1 - p))

#        ax.plot([0, len(data)], [pbar, pbar], 'k-')
#        ax.plot([0, len(data)], [lcl, lcl], 'r:')
#        ax.plot([0, len(data)], [ucl, ucl], 'r:')
#        ax.plot(data, 'bo--')

        return (data, pbar, lcl, ucl, self._title)
