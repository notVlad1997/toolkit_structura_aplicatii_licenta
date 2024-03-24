import tkinter
import component_template


class ButtonTkinter(component_template.ComponentTemplate):
    def __init__(self, frames, position=None):
        super().__init__(name="Button", category="Tkinter", frames=frames, size=[100, 20], position=position)
        self.add_property(name="Font", button_type="text", default_value="Arial")
        self.add_property(name="Background Color", button_type="color",
                          default_value=None)

    def update_component(self, window=None):
        if window is not None:
            if window is not self.master or self.master is None:
                self.master = window
                self.component = tkinter.Button(self.master)
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

        self.component.config(
            font=(self.attribute_values[self.attribute_names.index("Font")]),
            bg=self.attribute_values[self.attribute_names.index("Background Color")],
        )

        if "Position X" in self.attribute_names:
            self.component.bind("<ButtonPress-1>", self.create_focus_rectangle)
            self.component.place(x=self.attribute_values[self.attribute_names.index("Position X")],
                                 y=self.attribute_values[self.attribute_names.index("Position Y")],
                                 width=self.attribute_values[self.attribute_names.index("Width")],
                                 height=self.attribute_values[self.attribute_names.index("Height")],
                                 )
        else:
            self.component.place(
                width=self.attribute_values[self.attribute_names.index("Width")],
                height=self.attribute_values[self.attribute_names.index("Height")],
            )

        super().update_component(window)