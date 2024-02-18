import tkinter as tk
import component_template


class FrameTkinter(component_template.ComponentTemplate):
    def __init__(self, frames):
        super().__init__(name="Frame", category="Frame", frames=frames)
        self.add_property(name="Width", button_type="slider", default_value=300)
        self.add_property(name="Height", button_type="slider", default_value=200)
        self.add_property(name="Background Color", button_type="color", default_value="white")

    def update_component(self, window=None):
        if window is not None:
            self.component = tk.Frame(window)
        # else:
        #     self.component.pack_forget()
        #     self.component.master = self.attribute_values[self.attribute_names.index("Frame")]
        self.component.config(
            width=self.attribute_values[self.attribute_names.index("Width")],
            height=self.attribute_values[self.attribute_names.index("Height")],
            bg=self.attribute_values[self.attribute_names.index("Background Color")],
        )
        self.component.pack()
