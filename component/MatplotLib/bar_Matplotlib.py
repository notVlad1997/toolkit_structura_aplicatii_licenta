import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk

import component_template


class BarDiagram(component_template.ComponentTemplate):
    def __init__(self, frames, *args, **kwargs):
        super().__init__(name="Bar Color", category="MatplotLib", frames=frames)
        self.add_property(name="X Data", button_type="table", default_value="apple,blueberry,cherry,orange")
        self.add_property(name="Y Data", button_type="table", default_value="40,100,30,55")
        # self.add_property(name="Bar Labels", button_type="table", default_value="red,blue,_red,orange")
        # self.add_property(name="Bar Colors", button_type="table", default_value="tab:red,tab:blue,tab:red,tab:orange")
        # self.add_property(name="Title", button_type="text", default_value="Fruit supply by kind and color")
        self.canvas = None
        self.fig = None
        self.ax = None

    def update_component(self, window=None):
        if window is not None:
            if window is not self.master or self.master is None:
                self.master = window
                self.component = tk.Frame(self.master)
                self.component.pack()
                if self.canvas is not None:
                    self.canvas = FigureCanvasTkAgg(self.fig, master=self.component)
        else:
            if self.frames_choice is not None:
                frame_name = self.attribute_values[self.attribute_names.index("Frame")]
                frame = None
                for fr in self.frames_choice:
                    if str(frame_name) == str(fr):
                        frame = fr
                        break
                if frame is not self.master and frame is not None:
                    self.master = frame
                    self.component.destroy()
                    self.component = tk.Frame(self.master)
                    self.component.pack()
                    if self.canvas is not None:
                        self.canvas = FigureCanvasTkAgg(self.fig, master=self.component)


        x_data = self.attribute_values[self.attribute_names.index("X Data")].split(',')
        y_data = [int(value) for value in self.attribute_values[self.attribute_names.index("Y Data")].split(',')]

        if self.ax is not None:
            for bar in self.ax.patches:
                bar.remove()
            self.ax.set_xticks([])

        if self.canvas is None:
            self.fig, self.ax = plt.subplots()
            self.ax.set_ylabel('fruit supply')
            # ax.set_title(self.attribute_values[self.attribute_names.index("Title")])
            self.ax.legend(title='Fruit color')

        bar_width = 0.4
        bar_positions = range(len(x_data))

        bars = self.ax.bar(bar_positions, y_data, width=bar_width)

        self.ax.set_xticks(bar_positions)
        self.ax.set_xticklabels(x_data)

        self.ax.set_xlim(-0.5, len(x_data) - 0.5)

        if self.canvas is None:
            self.canvas = FigureCanvasTkAgg(self.fig, master=self.component)
            self.canvas.get_tk_widget().config(width=300, height=200)
            self.canvas.get_tk_widget().pack()

        self.canvas.draw()
        self.canvas.get_tk_widget().pack()

        # bar_labels = self.attribute_values[self.attribute_names.index("Bar Labels")].split(',')
        # bar_colors = self.attribute_values[self.attribute_names.index("Bar Colors")].split(',')
