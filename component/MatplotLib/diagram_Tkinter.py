import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk

import component_template


class MatplotlibDiagram(component_template.ComponentTemplate):
    def __init__(self):
        super().__init__(name="MatplotlibDiagram")
        self.add_property(name="X Data", button_type="table", default_value="1,2")
        self.add_property(name="Y Data", button_type="table", default_value="2,HELLO")
        self.add_property(name="Title", button_type="text", default_value="Matplotlib Diagram")

    def update_component(self, window=None):
        if window is not None:
            self.component = tk.Frame(window)
            self.component.pack()

        x_data = self.attribute_value[self.attribute_names.index("X Data")].split(',')
        y_data = self.attribute_value[self.attribute_names.index("Y Data")].split(',')

        fig, ax = plt.subplots()
        ax.plot(x_data, y_data)
        ax.set_title(self.attribute_value[self.attribute_names.index("Title")])

        canvas = FigureCanvasTkAgg(fig, master=self.component)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)