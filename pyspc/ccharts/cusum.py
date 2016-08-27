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
from .tables import d2


class cusum(ccharts):

    _title = "CUSUM Chart"

    def __init__(self, target=None, std=None, interval=4):
        super(cusum, self).__init__()

        self.target = target
        self.std = std
        self.interval = interval

    def plot(self, data, size, newdata=None):

        if size > 1:
            data = np.mean(data, axis=1)

        target = self.target
        std = self.std
        interval = self.interval

        if target is None:
            target = np.mean(data)

        if std is None:
            rbar = []
            for i in range(len(data) - 1):
                rbar.append(abs(data[i] - data[i + 1]))
            std = np.mean(rbar) / d2[2]

        k = std / 2

        cplus = []  # values
        cminus = []  # values
        i, j = 0, 0
        for xi in data:
            cplus.append(max([0, xi - (target + k) + i]))
            cminus.append(min([0, xi - (target - k) + j]))
            i, j = cplus[-1], cminus[-1]

        lcl = -interval * std
        ucl = interval * std
        center = 0

#        ax.plot([0, len(cplus)], [center, center], 'k-')
#        ax.plot([0, len(cplus)], [lcl, lcl], 'r:')
#        ax.plot([0, len(cplus)], [ucl, ucl], 'r:')
#        ax.plot(cplus, 'bo--')
#        ax.plot(cminus, 'bo--')

        return ([cplus, cminus], center, lcl, ucl, self._title)
