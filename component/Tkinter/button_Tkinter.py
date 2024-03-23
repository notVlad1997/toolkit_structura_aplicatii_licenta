import tkinter
import component_template


class ButtonTkinter(component_template.ComponentTemplate):
    def __init__(self, frames, position=None):
        super().__init__(name="Button", category="Tkinter", frames=frames, size=[10, 5], position=position)
        self.add_property(name="Font", button_type="text", default_value="Arial")
        self.add_property(name="Background Color", button_type="color",
                          default_value="gray")

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
            width=self.attribute_values[self.attribute_names.index("Width")],
            height=self.attribute_values[self.attribute_names.index("Height")],
            font=(self.attribute_values[self.attribute_names.index("Font")]),
            bg=self.attribute_values[self.attribute_names.index("Background Color")],
        )

        if "Position X" in self.attribute_names:
            self.component.bind("<ButtonPress-1>", self.create_focus_rectangle)
            self.component.place(x=self.attribute_values[self.attribute_names.index("Position X")],
                                 y=self.attribute_values[self.attribute_names.index("Position Y")])
        else:
            self.component.place()

    def create_focus_rectangle(self, event):
        if self.focused_component is not self:
            self.delete_focus_rectangle()
        x = int(self.attribute_values[self.attribute_names.index("Position X")]) - self.offset
        y = int(self.attribute_values[self.attribute_names.index("Position Y")]) - self.offset
        width = self.component.winfo_width() + self.offset * 2
        height = self.component.winfo_height() + self.offset * 2

        self.focus_canvas = tkinter.Canvas(self.master, width=width, height=height, highlightthickness=0)
        self.focus_canvas.place(x=x, y=y)

        focus_rectangle = self.focus_canvas.create_rectangle(0, 0, width, height, fill="blue")
        self.master.update_idletasks()
        self.component.lift()

        component_template.ComponentTemplate.focused_component = self