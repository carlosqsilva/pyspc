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


class ewma(ccharts):

    _title = "EWMA Chart"

    def __init__(self, target=None, weight=0.2):
        super(ewma, self).__init__()

        self.target = target
        self.weight = weight

    def plot(self, data, size, newdata=None):
        assert ((self.weight > 0) and (self.weight < 1))

        if size > 1:
            data = np.mean(data, axis=1)

        target = self.target
        weight = self.weight

        # calculate the target with not given
        if target is None:
            target = np.mean(data)

        # calculate the standard deviation
        rbar = []
        for i in range(len(data) - 1):
            rbar.append(abs(data[i] - data[i + 1]))
        std = np.mean(rbar) / 1.128

        ewma = []  # values
        i = target
        for x in data:
            ewma.append(weight * x + (1 - weight) * i)
            i = ewma[-1]

        lcl, ucl = [], []
        for i in range(1, len(data) + 1):
            lcl.append(target - 3 * (std) * np.sqrt((weight / (2 - weight)) * (1 - (1 - weight)**(2 * i))))
            ucl.append(target + 3 * (std) * np.sqrt((weight / (2 - weight)) * (1 - (1 - weight)**(2 * i))))

#        ax.plot([0, len(ewma)], [target, target], 'k-')
#        ax.plot(lcl, 'r:')
#        ax.plot(ucl, 'r:')
#        ax.plot(ewma, 'bo--')

        return (ewma, target, lcl, ucl, self._title)
