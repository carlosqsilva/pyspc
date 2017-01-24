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


class imrmr(ccharts):

    _title = "Moving Range Chart"

    def __init__(self, sizecol=1):
        super(imrmr, self).__init__()

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

        sample_mr = []
        sample_mean = []
        for key in samples:
            assert sample_size == len(samples[key])
            sample_mean.append(np.mean(samples[key]))
            try:
                v1, v2 = sample_mean[-2:]
                sample_mr.append(abs(v1 - v2))
            except:
                sample_mr.append(np.nan)

        mrbar = np.nanmean(sample_mr)  # CENTER
        ucl_mr = D4[2] * mrbar
        lcl_mr = D3[2] * mrbar

#        ax.plot([0, num_samples], [mrbar, mrbar], 'k-')
#        ax.plot([0, num_samples], [lcl_mr, lcl_mr], 'r:')
#        ax.plot([0, num_samples], [ucl_mr, ucl_mr], 'r:')
#        ax.plot(sample_mr, 'bo--')

        return (sample_mr, mrbar, lcl_mr, ucl_mr, self._title)
