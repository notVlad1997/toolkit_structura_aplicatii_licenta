from ui.frame.window import FrameWindow
import component_template


class FrameWindowTK(component_template.ComponentTemplate):
    def __init__(self, frames):
        super().__init__(name="Frame", category="Frame", frames="")
        self.remove_property(attribute_name="Frame")
        self.add_property(name="Width", button_type="slider", default_value=600)
        self.add_property(name="Height", button_type="slider", default_value=400)
        self.add_property(name="Background Color", button_type="color", default_value="white")

    def update_component(self, window=None):
        if window is not None:
            self.component = FrameWindow(window)
        self.component.config(
            width=self.attribute_values[self.attribute_names.index("Width")],
            height=self.attribute_values[self.attribute_names.index("Height")],
            # bg=self.attribute_values[self.attribute_names.index("Background Color")],
        )
        self.component.pack()
