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
from .tables import D3, D4
import numpy as np


class imrr(ccharts):

    _title = "R Chart"

    def __init__(self, sizecol=1):
        super(imrr, self).__init__()

        self.size = sizecol - 1

    def plot(self, data, size, newdata=None):

        sizes, data = data.T
        if self.size == 1:
            sizes, data = data, sizes

        samples = dict()
        for n, value in zip(sizes, data):
            if n in samples:
                samples[n].append(value)
            else:
                samples[n] = [value]

        sample_size = len(samples[1])
#        num_samples = len(samples)

        sample_r = []
        for key in samples:
            assert sample_size == len(samples[key])
            sample_r.append(max(samples[key]) - min(samples[key]))

        rbar = np.mean(sample_r)
        ucl_rbar = D4[sample_size] * rbar
        lcl_rbar = D3[sample_size] * rbar

#        ax.plot([0, num_samples], [rbar, rbar], 'k-')
#        ax.plot([0, num_samples], [lcl_rbar, lcl_rbar], 'r:')
#        ax.plot([0, num_samples], [ucl_rbar, ucl_rbar], 'r:')
#        ax.plot(sample_r, 'bo--')

        return (sample_r, rbar, lcl_rbar, ucl_rbar, self._title)
