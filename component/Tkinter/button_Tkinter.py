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
            if window is not self.master or self.master is None:
                self.master = window
                self.component = tkinter.Button(self.master)
                self.component.place(anchor=tkinter.CENTER)
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
                    self.component = tkinter.Button(self.master)
                    self.component.place(anchor=tkinter.CENTER)

        self.component.config(
            width=self.attribute_values[self.attribute_names.index("Width")],
            height=self.attribute_values[self.attribute_names.index("Height")],
            font=(self.attribute_values[self.attribute_names.index("Font")], 12),
            bg=self.attribute_values[self.attribute_names.index("Background Color")],
        )
        self.component.place(anchor=tkinter.CENTER)
        print(self.master)