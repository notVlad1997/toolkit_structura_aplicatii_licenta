import tkinter as tk
from component_template import ComponentTemplate


import tkinter as tk
from tkinter import ttk

class LabelTkinter(ComponentTemplate):
    def __init__(self, frames, *args, **kwargs):
        super().__init__(name="Label", category="Tkinter", frames=frames)
        self.add_property(name="Text", button_type="text", default_value="Hello World!")
        self.add_property(name="Font", button_type="text", default_value="Arial")
        self.add_property(name="Foreground Color", button_type="color", default_value="black")
        self.add_property(name="X Position", button_type="slider", default_value=0)
        self.add_property(name="Y Position", button_type="slider", default_value=0)

    def update_component(self, window=None):
        if window is not None:
            if window is not self.master or self.master is None:
                self.master = window
                self.component = tk.Label(self.master)
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
                    self.component = tk.Label(self.master)
        self.component.config(
            text=self.attribute_values[self.attribute_names.index("Text")],
            font=(self.attribute_values[self.attribute_names.index("Font")], 12),
            fg=self.attribute_values[self.attribute_names.index("Foreground Color")],
        )
        self.component.place(x=self.attribute_values[self.attribute_names.index("X Position")],
                             y=self.attribute_values[self.attribute_names.index("Y Position")],
                             anchor=tk.CENTER)