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

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

import matplotlib as mpl
mpl.use('GTK3Cairo')
# import matplotlib.pyplot as plt
# plt.style.use('dark_background')

from matplotlib.backends.backend_gtk3cairo import FigureCanvasGTK3Cairo as FigureCanvas

import os
import pandas as pd
from pyspc import *

control_charts = {"Cusum": [cusum],
                  "Ewma": [ewma],
                  "Sbar": [xbar_sbar, sbar],
                  "Rbar": [xbar_rbar, rbar],
                  "T-Square Hotelling": [hotelling, variation],
                  "Moving Range": [xmr, mr],
                  "C Chart": [c],
                  "NP Chart": [np],
                  "P Chart": [p],
                  "U Chart": [u],
                  "I-MR-R": [I_MR_X, I_MR_MR, I_MR_R],
                  "I-MR-S": [I_MR_X, I_MR_MR, I_MR_STD]}


class Pyspc(Gtk.Window):

    def __init__(self, *args):
        super(Pyspc, self).__init__(*args)

        self.data = []
        self.graph = None
        self.charts = None

        self.win = Gtk.Window()
        self.set_border_width(10)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_title("SPC : Statistical Process Control for humans")
        self.set_default_size(480, 600)
        self.connect("delete-event", Gtk.main_quit)

        self.buildui()

    def buildui(self):
        self.vbox = Gtk.VBox(spacing=6)
        self.add(self.vbox)

        self.open_file = Gtk.Button(label='Open Data File')
        self.open_file.connect("clicked", self.on_file_clicked)

        charts_store = Gtk.ListStore(str)
        charts = ["Cusum", "Ewma", "Sbar", "Rbar", "T-Square Hotelling", "C Chart",
                  "NP Chart", "P Chart", "U Chart", "Moving Range", "I-MR-R",
                  "I-MR-S"]
        for chart in charts:
            charts_store.append([chart])

        charts_combo = Gtk.ComboBox.new_with_model(charts_store)
        charts_combo.connect("changed", self.on_charts_combo_changed)
        renderer_text = Gtk.CellRendererText()
        charts_combo.pack_start(renderer_text, True)
        charts_combo.add_attribute(renderer_text, "text", 0)

        plot_chart = Gtk.Button(label="Plot Chart")
        plot_chart.connect("clicked", self.on_plot_clicked)

        self.save_chart = Gtk.Button(label="Save Chart")
        self.save_chart.connect("clicked", self.on_save_clicked)
        self.save_chart.set_sensitive(False)

        hbox1 = Gtk.HBox(spacing=6)
        hbox1.set_homogeneous(True)
        hbox1.pack_start(self.open_file, True, True, 0)
        hbox1.pack_start(charts_combo, True, True, 0)
        self.vbox.pack_start(hbox1, False, False, 0)

        hbox2 = Gtk.HBox(spacing=6)
        hbox2.set_homogeneous(True)
        hbox2.pack_start(plot_chart, True, True, 0)
        hbox2.pack_start(self.save_chart, True, True, 0)
        self.vbox.pack_start(hbox2, False, False, 0)

        stack = Gtk.Stack()
        stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        stack.set_transition_duration(800)

        self.plotcanvas = Gtk.Label("Plot Goes Here")
        self.canvas_box = Gtk.Box(Gtk.Orientation.VERTICAL)
        self.canvas_box.pack_start(self.plotcanvas, True, True, 0)
        stack.add_titled(self.canvas_box, "canvas", "Charts")

        self.summary = Gtk.ListBox()
        self.summary_box = Gtk.Box(Gtk.Orientation.VERTICAL)
        self.summary_box.pack_start(self.summary, True, True, 0)
        stack.add_titled(self.summary_box, "summary", "Summary")

        stack_switcher = Gtk.StackSwitcher(homogeneous=True)
        stack_switcher.set_stack(stack)
        self.vbox.pack_start(stack_switcher, False, False, 0)
        self.vbox.pack_start(stack, True, True, 0)

    def on_charts_combo_changed(self, combo):
        tree_iter = combo.get_active()
        if tree_iter is not None:
            model = combo.get_model()
            chart = model[tree_iter][0]
            # print("Selected: Chart=%s" % chart)
            self.charts = chart

    def on_plot_clicked(self, widget):
        self.canvas_box.remove(self.plotcanvas)
        graph = spc(self.data) + rules()
        for chart in control_charts[self.charts]:
            graph = graph + chart()
        self.graph = graph
        self.graph.make()

        self.save_chart.set_sensitive(True)
        self.plotcanvas = FigureCanvas(self.graph.fig)
        self.canvas_box.pack_start(self.plotcanvas, True, True, 0)
        self.canvas_box.show_all()
        # self.vbox.show_all()

    def on_file_clicked(self, widget):
        dialog = Gtk.FileChooserDialog("Please choose a file", self,
                                       Gtk.FileChooserAction.OPEN,
                                       (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                        Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            path = dialog.get_filename()
            self.open_file.set_label("File Selected: %s" % os.path.basename(path))
            self.data = pd.read_csv(path)

        elif response == Gtk.ResponseType.CANCEL:
            print("Cancel clicked")

        dialog.destroy()

    def on_save_clicked(self, widget):
        dialog = Gtk.FileChooserDialog("Please choose a file", self,
                                       Gtk.FileChooserAction.SAVE,
                                       (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                        Gtk.STOCK_SAVE, Gtk.ResponseType.OK))

        dialog.set_current_name("Untitled.png")
        dialog.set_do_overwrite_confirmation(True)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            self.graph.save(dialog.get_filename(), dpi=600)

        dialog.destroy()


if __name__ == '__main__':
    app = Pyspc()
    app.show_all()
    Gtk.main()


# win = Gtk.Window()
# win.connect("destroy", Gtk.main_quit)
# win.set_default_size(400, 300)
# win.set_title("Embedding in GTK")

# a = spc(pistonrings) + cusum() + ewma() + rules()
# a.make()

# f = Figure(figsize=(5, 4), dpi=100)
# a = f.add_subplot(111)
# t = arange(0.0, 3.0, 0.01)
# s = sin(2*pi*t)
# a.plot(t, s)

# canvas = FigureCanvas(a.fig)  # a gtk.DrawingArea
# win.add(canvas)

# win.show_all()
# Gtk.main()
