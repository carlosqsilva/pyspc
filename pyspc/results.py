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

import numpy as np
import matplotlib.ticker as mtick


class PlotCharts(object):
    """docstring for PlotCharts"""

    def __init__(self, ax, values, center, lcl, ucl, title):
        super(PlotCharts, self).__init__()

        self.plot_chart(ax, values, center, lcl, ucl, title)

    def plot_chart(self, ax, values, center, lcl, ucl, title, newvalues=None):

        ax.yaxis.tick_right()
        ax.yaxis.set_major_formatter(mtick.FormatStrFormatter('%.3f'))

        num = len(values)
        if isinstance(values[0], list):
            num = len(values[0])

        if newvalues:
            ax.plot([num - 0.5] * 2, [lcl, ucl], 'k--')
            ax.plot(values + newvalues, 'bo--')
            num += len(newvalues)

        newx = list(range(num))
        newx[0] = -0.3
        newx[-1] = num - 0.6

        if isinstance(lcl, list) and isinstance(ucl, list):
            ax.yaxis.set_ticks([center])
            ax.plot([-0.3, num], [center, center], 'k-')
            ax.plot(values, 'bo--')
            ax.fill_between(newx, lcl, ucl, facecolor='green', alpha=0.4, step='mid')
            ax.step(newx, lcl, 'r:', where='mid')
            ax.step(newx, ucl, 'r:', where='mid')

        else:
            ax.fill_between([-0.3, num], [lcl, lcl], [ucl, ucl], facecolor='green', alpha=0.4)
            ax.yaxis.set_ticks([lcl, center, ucl])
            ax.plot([0, num], [center, center], 'k-')
            ax.plot([0, num], [lcl, lcl], 'r:')
            ax.plot([0, num], [ucl, ucl], 'r:')

            if isinstance(values[0], list):
                ax.plot(values[0], 'bo--')
                ax.plot(values[1], 'bo--')
            else:
                ax.plot(values, 'bo--')

        # Set the title
        ax.set_title(title)

        # Change de y limits of the graph
        ylim = ax.get_ylim()
        factor = 0.2
        new_ylim = (ylim[0] + ylim[1]) / 2 + np.array((-0.5, 0.5)) * (ylim[1] - ylim[0]) * (1 + factor)
        if lcl == 0:
            ax.set_ylim([0, new_ylim[1]])
        else:
            ax.set_ylim(new_ylim)

        # Change x ticks
        new_xlim = [0, num]
        ax.set_xlim([0, num] + np.array((-0.3, -0.6)))
        ax.xaxis.set_ticks(np.arange(*new_xlim, 2))
