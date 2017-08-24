#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (C) 2016  Carlos Henrique Silva <carlosqsilva@outlook.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import remi.gui as gui
import remi.server as server
from remi import App, start

from matplotlib.backends.backend_agg import FigureCanvasAgg

import os
import pandas as pd
import threading
import time

from io import BytesIO
from pyspc import *

control_charts = {"Cusum": [cusum],
                  "Ewma": [ewma],
                  "Sbar": [xbar_sbar, sbar],
                  "Rbar": [xbar_rbar, rbar],
                  "T-Square Single": [Tsquare_single],
                  "T-Square": [Tsquare],
                  "MEWMA": [mewma],
                  "Moving Range": [xmr, mr],
                  "C Chart": [c],
                  "NP Chart": [np],
                  "P Chart": [p],
                  "U Chart": [u],
                  "I-MR-R": [imrx, imrmr, imrr],
                  "I-MR-S": [imrx, imrmr, imrstd]}


class MatplotImage(gui.Image):
    ax = None

    def __init__(self, **kwargs):
        super(MatplotImage, self).__init__("/%s/get_image_data?update_index=0" % id(self), **kwargs)
        self._buf = None
        self._buflock = threading.Lock()

        self.data = None
        self.layer = []
        # self.redraw()

    def redraw(self):

        self.figure = spc(data=self.data) + rules()
        for chart in self.layer:
            self.figure + chart()
        self.figure.make(figsize=(8, 6))

        canv = FigureCanvasAgg(self.figure.fig)
        buf = BytesIO()
        canv.print_figure(buf, format='png')
        with self._buflock:
            if self._buf is not None:
                self._buf.close()
            self._buf = buf

        i = int(time.time() * 1e6)
        self.attributes['src'] = "/%s/get_image_data?update_index=%d" % (id(self), i)

        super(MatplotImage, self).redraw()

    def get_image_data(self, update_index):
        with self._buflock:
            if self._buf is None:
                return None
            self._buf.seek(0)
            data = self._buf.read()

        return [data, {'Content-type': 'image/png'}]


bgcolor = '#DCDCDC'
overflow = 'hidden'
display = 'block'


class Pyspc(App):

    def __init__(self, *args):
        super(Pyspc, self).__init__(*args)

    def main(self):
        # root widget
        # vertical_container = gui.Widget(width='100%', height='100%')
        # vertical_container.style['background-color'] = bgcolor
        # vertical_container.style['display'] = display
        # vertical_container.style['overflow'] = overflow

        horizontal_container = gui.Widget(width='100%', height='100%', layout_orientation=gui.Widget.LAYOUT_HORIZONTAL)
        horizontal_container.style['background-color'] = bgcolor
        horizontal_container.style['display'] = display
        horizontal_container.style['overflow'] = 'scroll'
        horizontal_container.style['text-align'] = 'center'

        sub_container_left = gui.Widget(width='50%', layout_orientation=gui.Widget.LAYOUT_VERTICAL)
        sub_container_left.style['background-color'] = bgcolor
        sub_container_left.style['display'] = display
        sub_container_left.style['overflow'] = overflow
        sub_container_left.style['text-align'] = 'center'

        sub_container_right = gui.Widget(width='50%', layout_orientation=gui.Widget.LAYOUT_VERTICAL)
        sub_container_right.style['background-color'] = bgcolor
        sub_container_right.style['display'] = display
        sub_container_right.style['overflow'] = overflow
        sub_container_right.style['text-align'] = 'center'

        vbox1 = gui.Widget(width='100%', layout_orientation=gui.Widget.LAYOUT_HORIZONTAL, margin='0px')
        vbox1.style['background-color'] = bgcolor

        open_file = gui.Button('Open File', width='auto', height=30, margin='10px')
        open_file.set_on_click_listener(self, 'open_file_pressed')
        open_file.attributes['title'] = 'Clik here to open a .CSV file with your data'
        # open_file.style['font-size'] = 'large'

        open_clipboard = gui.Button('From Clipboard', widht='auto', height=30, margin='10px')
        open_clipboard.set_on_click_listener(self, 'open_clipboard_pressed')
        open_clipboard.attributes['title'] = 'Clik here to Paste data from the Clipboard eg: excel, html table, etc...'
        # open_clipboard.style['font-size'] = 'large'

        self.data_table = gui.Table(width='100%', height='100%', margin='10px')
        self.data_table.style['overflow'] = overflow
        # self.data_table.style['display'] = display

        vbox1.append(open_file)
        vbox1.append(open_clipboard)

        vbox2 = gui.Widget(width='100%', layout_orientation=gui.Widget.LAYOUT_HORIZONTAL, margin='0px')
        vbox2.style['background-color'] = bgcolor

        charts = ["Cusum", "Ewma", "Sbar", "Rbar", "T-Square Single", "T-Square", "MEWMA", "C Chart",
                  "NP Chart", "P Chart", "U Chart", "Moving Range", "I-MR-R", "I-MR-S"]
        self.dropdown = gui.DropDown.new_from_list(charts, width='auto', height=30, margin='10px')
        self.dropdown.attributes['title'] = 'Choose the right control for the that you have'
        # self.dropdown.style['font-size'] = 'large'

        plot_chart = gui.Button('Plot Chart', width='auto', height=30, margin='10px')
        plot_chart.set_on_click_listener(self, 'plot_chart_pressed')
        # plot_chart.style['font-size'] = 'large'
        save_chart = gui.Button('Save Chart', width='auto', height=30, margin='10px')
        save_chart.set_on_click_listener(self, 'save_chart_pressed')
        # save_chart.style['font-size'] = 'large'

        self.mpl = MatplotImage(width='100%', height='auto')
        self.mpl.style['margin'] = '10px'

        vbox2.append(self.dropdown)
        vbox2.append(plot_chart)
        vbox2.append(save_chart)

        self.status_txt = gui.Label('', width='100%', height=20, margin='10px')

        sub_container_left.append(vbox1)
        sub_container_left.append(self.status_txt)
        sub_container_left.append(self.data_table)

        sub_container_right.append(vbox2)
        sub_container_right.append(self.mpl)

        horizontal_container.append(sub_container_left)
        horizontal_container.append(sub_container_right)

        # vertical_container.append(horizontal_container)

        return horizontal_container

    def open_file_pressed(self):
        self.open_filedialog = gui.FileSelectionDialog(title='File Selection Dialog', message='Select a .CSV file',
                                                       multiple_selection=False, allow_folder_selection=False)
        self.open_filedialog.set_on_confirm_value_listener(self, 'file_selection_confirm')
        self.open_filedialog.show(self)

    def file_selection_confirm(self, filepath):
        try:
            self.data = pd.read_csv(filepath[0])

            self.data_table.empty()
            table = [list(self.data.columns)] + [[str(x) for x in row] for row in self.data.values]
            self.data_table.from_2d_matrix(table)
        except Exception as e:
            self.text_message(repr(e))
        rows, columns = self.data.shape
        filename = os.path.basename(filepath[0])
        self.status_txt.set_text("File Selected: {0} | {1} Rows {2} Columns".format(filename, rows, columns))

    def open_clipboard_pressed(self):
        try:
            self.data = pd.read_clipboard()

            self.data_table.empty()
            table = [list(self.data.columns)] + [[str(x) for x in row] for row in self.data.values]
            self.data_table.from_2d_matrix(table)
        except Exception as e:
            self.text_message(repr(e))
        pass

    def plot_chart_pressed(self):
        try:
            chart = self.dropdown.get_value()
            self.mpl.data = self.data
            self.mpl.layer = control_charts[chart]
            self.mpl.redraw()
        except Exception as e:
            self.text_message(repr(e))

    def save_chart_pressed(self):
        self.save_dialog = gui.InputDialog('Save Dialog', 'Give a name to file:', initial_value='Untitled.png',
                                           width=500, height=160)
        self.save_dialog.set_on_confirm_value_listener(self, 'save_dialog_confirm')
        self.save_dialog.show(self)

    def save_dialog_confirm(self, filename):
        self.mpl.figure.save(filename)
        _root = os.path.abspath(os.path.dirname(__file__))
        self.status_txt.set_text('File Saved in: %s' % os.path.join(_root, filename))

    def text_message(self, message):
        self.custom_dialog = gui.GenericDialog(title='Dialog Box', width='600px')
        text_input = gui.TextInput(single_line=False)
        text_input.set_text(message)

        self.custom_dialog.add_field_with_label('text_input_messade', 'System Message', text_input)
        self.custom_dialog.show(self)


if __name__ == "__main__":
    start(Pyspc, debug=True, address='127.0.0.1', port=8081)
    # s = server.StandaloneServer(Pyspc, start=True, title="Pyspc: Statistical Process Control Library for Humans")
