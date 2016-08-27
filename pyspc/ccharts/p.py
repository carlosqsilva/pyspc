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


class p(ccharts):

    _title = "P Chart"

    def __init__(self, size=1):
        super(p, self).__init__()

        self.size = size - 1

    def plot(self, data, size, newdata=None):

        sizes, data = data.T
        if self.size == 1:
            sizes, data = data, sizes

        data2 = data / sizes
        pbar = np.mean(data2)

        for n in sizes:
            assert n * pbar >= 5
            assert n * (1 - pbar) >= 5

        if np.mean(sizes) == sizes[0]:
            size = sizes[0]
            lcl = pbar - 3 * np.sqrt((pbar * (1 - pbar)) / size)
            ucl = pbar + 3 * np.sqrt((pbar * (1 - pbar)) / size)

            if lcl < 0:
                lcl = 0
            if ucl > 1:
                ucl = 1

            return (data2, pbar, lcl, ucl, self._title)

        else:
            lcl, ucl = [], []
            for size in sizes:
                lcl.append(pbar - 3 * np.sqrt((pbar * (1 - pbar)) / size))
                ucl.append(pbar + 3 * np.sqrt((pbar * (1 - pbar)) / size))

            return (data2, pbar, lcl, ucl, self._title)
