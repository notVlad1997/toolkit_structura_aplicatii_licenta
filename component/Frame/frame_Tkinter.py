import tkinter as tk
import component_template


class FrameTkinter(component_template.ComponentTemplate):
    def __init__(self, frames, position=None, *args, **kwargs):
        super().__init__(name="Frame", category="Frame", frames=frames, size=[300, 200], position=position)
        self.add_property(name="Background Color", button_type="color", default_value="white")

    def update_component(self, window=None):
        if window is not None:
            if window is not self.master or self.master is None:
                self.master = window
                self.component = tk.Frame(self.master)
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
                    self.component = tk.Frame(self.master)
        self.component.config(background=self.attribute_values[self.attribute_names.index("Background Color")])

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
