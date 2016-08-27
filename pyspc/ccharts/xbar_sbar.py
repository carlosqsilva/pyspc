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
from .tables import A3, B3, B4
import numpy as np


class xbar_sbar(ccharts):

    _title = "Xbar-S Chart"

    def plot(self, data, size, newdata=None):

        assert size >= 2
        assert size <= 10
        newvalues = None

        X, S = [], []
        for xs in data:
            assert len(xs) == size
            S.append(np.std(xs, ddof=1))
            X.append(np.mean(xs))

        if newdata:
            newvalues = [np.mean(xs) for xs in newdata]

        sbar = np.mean(S)
        xbar = np.mean(X)

        lclx = xbar - A3[size] * sbar
        uclx = xbar + A3[size] * sbar

        return (X, xbar, lclx, uclx, self._title)


class sbar(ccharts):

    _title = "Standard Deviation Chart"

    def plot(self, data, size, newdata=None):

        assert size >= 2
        assert size <= 10
        newvalues = None

        S = []
        for xs in data:
            assert len(xs) == size
            S.append(np.std(xs, ddof=1))

        if newdata:
            newvalues = [np.std(xs, ddof=1) for xs in newdata]

        sbar = np.mean(S)

        lcls = B3[size] * sbar
        ucls = B4[size] * sbar

        return (S, sbar, lcls, ucls, self._title)
