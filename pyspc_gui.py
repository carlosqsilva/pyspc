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
from gi.repository import Gtk, Gdk

import matplotlib as mpl
mpl.use('GTK3Cairo')
# import matplotlib.pyplot as plt
# plt.style.use('dark_background')

from matplotlib.backends.backend_gtk3cairo import FigureCanvasGTK3Cairo as FigureCanvas

import sys
import pandas as pd
from io import StringIO
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


class FileDialog(Gtk.Dialog):

    def __init__(self, parent):
        Gtk.Dialog.__init__(self, "File Dialog", parent, 0,
                            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                             Gtk.STOCK_OK, Gtk.ResponseType.OK))
        self.set_default_size(500, 550)
        box = self.get_content_area()

        self.verticalbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=3)
        box.add(self.verticalbox)

        self.clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)

        from_file = Gtk.Button("From File")
        from_file.connect("clicked", self.on_file)
        from_clipboard = Gtk.Button("Clipboard")
        from_clipboard.connect("clicked", self.on_clipboard)

        hbox1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, homogeneous=True)
        hbox1.pack_start(from_file, True, True, 0)
        hbox1.pack_start(from_clipboard, True, True, 0)
        self.verticalbox.pack_start(hbox1, False, False, 0)

        # Just holding the Place for real treeview widget
        self.scrollable_treelist = Gtk.Label()
        self.verticalbox.pack_start(self.scrollable_treelist, True, True, 0)

        self.show_all()

    def add_treeview(self):
        num_columns = [float for x in range(len(self.data.columns))]

        liststore = Gtk.ListStore(*num_columns)
        for ref in self.data.values.tolist():
            liststore.append(ref)

        treeview = Gtk.TreeView.new_with_model(liststore)
        for i, column_title in enumerate(self.data.columns):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(column_title, renderer, text=i)
            treeview.append_column(column)

        self.scrollable_treelist = Gtk.ScrolledWindow()
        self.scrollable_treelist.add(treeview)
        self.scrollable_treelist.set_vexpand(True)
        self.scrollable_treelist.set_hexpand(True)
        self.verticalbox.pack_start(self.scrollable_treelist, True, True, 0)
        self.verticalbox.show_all()

    def on_file(self, button):

        dialog = Gtk.FileChooserDialog("Please choose a file", self,
                                       Gtk.FileChooserAction.OPEN,
                                       (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                        Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        filter_csv = Gtk.FileFilter()
        filter_csv.set_name("CSV Files")
        filter_csv.add_pattern("*.csv")
        dialog.add_filter(filter_csv)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            path = dialog.get_filename()
            self.data = pd.read_csv(path)
            self.verticalbox.remove(self.scrollable_treelist)
            self.add_treeview()

        dialog.destroy()

    def on_clipboard(self, button):
        kwargs = dict()
        text = self.clipboard.wait_for_text()
        lines = text[:10000].split('\n')[:-1][:10]

        counts = set([x.lstrip().count('\t') for x in lines])
        if len(lines) > 1 and len(counts) == 1 and counts.pop() != 0:
            kwargs['sep'] = '\t'

        if kwargs.get('sep') is None and kwargs.get('delim_whitespace') is None:
            kwargs['sep'] = '\s+'

        try:
            self.data = pd.read_table(StringIO(text), **kwargs)
        except:
            print("Unexpected Error: ", sys.exc_info())
        else:
            self.verticalbox.remove(self.scrollable_treelist)
            self.add_treeview()


class main(Gtk.Window):

    def __init__(self, *args):
        super(main, self).__init__(*args)

        self.data = []
        self.graph = None
        self.charts = None

        self.win = Gtk.Window()
        self.set_border_width(4)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_title("PySpc : Statistical Process Control Charts for Humans")
        self.set_default_size(480, 600)
        self.connect("delete-event", Gtk.main_quit)

        self.buildui()

    def buildui(self):
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        toolbar = Gtk.Toolbar()
        toolbar.set_icon_size(Gtk.IconSize.SMALL_TOOLBAR)
        vbox.pack_start(toolbar, False, False, 0)
        self.add(vbox)

        open_file = Gtk.ToolButton()
        open_file.set_tooltip_text("Open file contain data")
        open_file.set_icon_name("bookmark-new-symbolic")
        open_file.connect("clicked", self.on_file_clicked)
        toolbar.insert(open_file, 0)

        toolbar.insert(Gtk.SeparatorToolItem(), 1)

        charts_store = Gtk.ListStore(str)
        charts = ["Cusum", "Ewma", "Sbar", "Rbar", "T-Square Single", "T-Square", "MEWMA", "C Chart",
                  "NP Chart", "P Chart", "U Chart", "Moving Range", "I-MR-R", "I-MR-S"]
        for chart in charts:
            charts_store.append([chart])

        charts_combo = Gtk.ComboBox.new_with_model(charts_store)
        charts_combo.connect("changed", self.on_charts_combo_changed)
        renderer_text = Gtk.CellRendererText()
        charts_combo.pack_start(renderer_text, True)
        charts_combo.add_attribute(renderer_text, "text", 0)
        tool_combo_container = Gtk.ToolItem()
        tool_combo_container.add(charts_combo)
        tool_combo_container.set_tooltip_text("Choose the right control chart for the data you opened")
        tool_label_container = Gtk.ToolItem()
        tool_label_container.add(Gtk.Label("Control Chart: "))
        toolbar.insert(tool_label_container, 2)
        toolbar.insert(tool_combo_container, 3)

        toolbar.insert(Gtk.SeparatorToolItem(), 4)

        plot_chart = Gtk.ToolButton()
        plot_chart.set_tooltip_text("Plot the control chart selected")
        plot_chart.connect("clicked", self.on_plot_clicked)
        plot_chart.set_icon_name("image-filter-symbolic")
        toolbar.insert(plot_chart, 5)

        toolbar.insert(Gtk.SeparatorToolItem(), 6)

        save_chart = Gtk.ToolButton()
        save_chart.set_tooltip_text("Save the control chart image")
        save_chart.connect("clicked", self.on_save_clicked)
        save_chart.set_icon_name("insert-image-symbolic")
        toolbar.insert(save_chart, 7)

        stack = Gtk.Stack()
        stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        stack.set_transition_duration(800)

        self.plotcanvas = Gtk.Label("Plot Goes Here")
        self.canvas_box = Gtk.Box(Gtk.Orientation.VERTICAL)
        self.canvas_box.pack_start(self.plotcanvas, True, True, 0)
        stack.add_titled(self.canvas_box, "canvas", "Control Charts")

        self.summary = Gtk.ListBox()
        self.summary_box = Gtk.Box(Gtk.Orientation.VERTICAL)
        self.summary_box.pack_start(self.summary, True, True, 0)
        stack.add_titled(self.summary_box, "summary", "Summary")

        stack_switcher = Gtk.StackSwitcher(homogeneous=True)
        stack_switcher.set_stack(stack)
        vbox.pack_start(stack_switcher, False, False, 0)
        vbox.pack_start(stack, True, True, 0)

    def on_charts_combo_changed(self, combo):
        tree_iter = combo.get_active()
        if tree_iter is not None:
            model = combo.get_model()
            chart = model[tree_iter][0]
            self.charts = chart

    def on_plot_clicked(self, widget):
        self.canvas_box.remove(self.plotcanvas)
        graph = spc(self.data) + rules()
        for chart in control_charts[self.charts]:
            graph = graph + chart()
        self.graph = graph
        self.graph.make()

        self.plotcanvas = FigureCanvas(self.graph.fig)
        self.canvas_box.pack_start(self.plotcanvas, True, True, 0)
        self.canvas_box.show_all()
        # self.vbox.show_all()

    def on_file_clicked(self, widget):
        # dialog = Gtk.FileChooserDialog("Please choose a file", self,
        #                                Gtk.FileChooserAction.OPEN,
        #                                (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
        #                                 Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        # response = dialog.run()
        # if response == Gtk.ResponseType.OK:
        #     path = dialog.get_filename()
        #     # self.open_file.set_label("File Selected: %s" % os.path.basename(path))
        #     self.data = pd.read_csv(path)

        # elif response == Gtk.ResponseType.CANCEL:
        #     print("Cancel clicked")

        # dialog.destroy()
        dialog = FileDialog(self)
        # dialog.show_all()
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            self.data = dialog.data
        dialog.destroy()

    def on_save_clicked(self, widget):
        dialog = Gtk.FileChooserDialog("Please choose a filename to save", self,
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
    app = main()
    app.show_all()
    Gtk.main()
