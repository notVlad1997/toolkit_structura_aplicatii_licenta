import tkinter as tk
from component_template import ComponentTemplate


class LabelTkinter(ComponentTemplate):
    def __init__(self, frames):
        super().__init__(name="Label", category="Tkinter", frames=frames)
        self.add_property(name="Text", button_type="text", default_value="")
        self.add_property(name="Font", button_type="text", default_value="Arial")
        self.add_property(name="Foreground Color", button_type="color", default_value="black")

    def update_component(self, window=None):
        if window is not None:
            self.component = tk.Label(window)
        else:
            self.component.destroy()
            frame_name = self.attribute_values[self.attribute_names.index("Frame")]
            frame = None
            for fram in self.frames_choice:
                if frame_name == str(fram):
                    frame = fram
                    break
            self.component = tk.Label(frame)
            self.component.place(anchor=tk.CENTER)
        self.component.config(
            text=self.attribute_values[self.attribute_names.index("Text")],
            font=(self.attribute_values[self.attribute_names.index("Font")], 12),
            fg=self.attribute_values[self.attribute_names.index("Foreground Color")],
        )
        self.component.place(anchor=tk.CENTER)
