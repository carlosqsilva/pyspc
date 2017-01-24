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
from .tables import B3, B4
import numpy as np


class imrstd(ccharts):

    _title = "Standard Deviation Chart"

    def __init__(self, sizecol=1):
        super(imrstd, self).__init__()

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

        sample_std = []
        for key in samples:
            assert sample_size == len(samples[key])
            sample_std.append(np.std(samples[key], ddof=1))

        sbar = np.mean(sample_std)
        ucl_std = B4[sample_size] * sbar
        lcl_std = B3[sample_size] * sbar

        return (sample_std, sbar, lcl_std, ucl_std, self._title)
