import tkinter

import component_template


class ButtonTkinter(component_template.ComponentTemplate):
    def __init__(self):
        super().__init__(name="Button", category="Tkinter", source_class="tkinter")
        self.add_property(name="width", json_attribute="Width", button_type="slider", default_value=5)
        self.add_property(name="height", json_attribute="Height", button_type="slider", default_value=1)
        self.add_property(name="font", json_attribute="Font", button_type="text", default_value="Arial")
        self.add_property(name="background_color", json_attribute="Background Color", button_type="color",
                          default_value="gray")

    def return_component(self, window=None):
        self.update_component(window)
        return self.component

    def update_value(self, index):
        super().update_value(index=index)

    def update_component(self, window=None):
        if window is not None:
            self.component = tkinter.Button(window)
        self.component.config(
            width=self.attribute_value[self.attribute_names.index("width")],
            height=self.attribute_value[self.attribute_names.index("height")],
            font=(self.attribute_value[self.attribute_names.index("font")], 12),
            bg=self.attribute_value[self.attribute_names.index("background_color")],
        )
        self.component.pack()
