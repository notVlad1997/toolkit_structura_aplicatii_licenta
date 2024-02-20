import tkinter
import component_template


class ButtonTkinter(component_template.ComponentTemplate):
    def __init__(self, frames):
        super().__init__(name="Button", category="Tkinter", frames=frames)
        self.add_property(name="Width", button_type="slider", default_value=5)
        self.add_property(name="Height", button_type="slider", default_value=1)
        self.add_property(name="Font", button_type="text", default_value="Arial")
        self.add_property(name="Background Color", button_type="color",
                          default_value="gray")

    def update_component(self, window=None):
        if window is not None:
            self.component = tkinter.Button(window)

        else:
            self.component.destroy()
            frame_name = self.attribute_values[self.attribute_names.index("Frame")]
            frame = None
            for fram in self.frames_choice:
                if frame_name == str(fram):
                    frame = fram
                    break
            self.component = tkinter.Button(frame)
            self.component.place(anchor=tkinter.CENTER)
        self.component.config(
            width=self.attribute_values[self.attribute_names.index("Width")],
            height=self.attribute_values[self.attribute_names.index("Height")],
            font=(self.attribute_values[self.attribute_names.index("Font")], 12),
            bg=self.attribute_values[self.attribute_names.index("Background Color")],
        )
        self.component.place(anchor=tkinter.CENTER)
