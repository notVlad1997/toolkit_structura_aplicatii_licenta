import component_template
import tkinter


class ButtonTkinter(component_template.ComponentTemplate):
    def __init__(self):
        super().__init__(name="Test", category="Tkinter", source_class="tkinter")
        self.add_property(name="width", json_attribute="Width", button_type="slider", default_value=100)
        self.add_property(name="height", json_attribute="Height", button_type="slider", default_value=30)
        self.add_property(name="font", json_attribute="Font", button_type="text", default_value="Arial")
        self.add_property(name="background_color", json_attribute="Background Color", button_type="color",
                          default_value="#ffffff")

    def show_properties(self):
        super().show_properties()

    def add_property(self, name, json_attribute, button_type, default_value):
        super().add_property(name=name, json_attribute=json_attribute, button_type=button_type, default_value=default_value)

    def modify_value(self, attribute_name, value):
        super().modify_value(attribute_name=attribute_name, value=value)
