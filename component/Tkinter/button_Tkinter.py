import tkinter

import component_template


class ButtonTkinter(component_template.ComponentTemplate):
    def __init__(self):
        super().__init__(name="Button", category="Tkinter")
        self.add_property(name="Width", button_type="slider", default_value=5)
        self.add_property(name="Height", button_type="slider", default_value=1)
        self.add_property(name="Font", button_type="text", default_value="Arial")
        self.add_property(name="Background Color", button_type="color",
                          default_value="gray")

    def update_component(self, window=None):
        if window is not None:
            self.component = tkinter.Button(window)
        self.component.config(
            width=self.attribute_values[self.attribute_names.index("Width")],
            height=self.attribute_values[self.attribute_names.index("Height")],
            font=(self.attribute_values[self.attribute_names.index("Font")], 12),
            bg=self.attribute_values[self.attribute_names.index("Background Color")],
        )
        self.component.pack()
