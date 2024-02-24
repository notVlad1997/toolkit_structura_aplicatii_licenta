import tkinter as tk
import component_template


class FrameTkinter(component_template.ComponentTemplate):
    def __init__(self, frames):
        super().__init__(name="Frame", category="Frame", frames=frames)
        self.add_property(name="Width", button_type="slider", default_value=300)
        self.add_property(name="Height", button_type="slider", default_value=200)
        self.add_property(name="Background Color", button_type="color", default_value="white")

    def update_component(self, window=None):
        # if window is not None:
        #     if window is not self.master or self.master is None:
        #         self.master = window
        #         self.component = tkinter.Button(self.master)
        # else:
        #     if self.frames_choice is not None:
        #         frame_name = self.attribute_values[self.attribute_names.index("Frame")]
        #         frame = None
        #         for fr in self.frames_choice:
        #             if str(frame_name) == str(fr):
        #                 frame = fr
        #                 break
        #         if frame is not self.master and frame is not None:
        #             self.master = frame
        #             self.component.destroy()
        #             self.component = tkinter.Button(self.master)
        #             self.component.place(anchor=tkinter.CENTER)
        #
        # self.component.config(
        #     width=self.attribute_values[self.attribute_names.index("Width")],
        #     height=self.attribute_values[self.attribute_names.index("Height")],
        #     font=(self.attribute_values[self.attribute_names.index("Font")], 12),
        #     bg=self.attribute_values[self.attribute_names.index("Background Color")],
        # )
        # self.component.place(anchor=tkinter.CENTER)
        # print(self.master)

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
                    self.component.place(anchor=tk.CENTER)

        # else:
        #     self.component.pack_forget()
        #     self.component.master = self.attribute_values[self.attribute_names.index("Frame")]
        self.component.config(
            width=self.attribute_values[self.attribute_names.index("Width")],
            height=self.attribute_values[self.attribute_names.index("Height")],
            bg=self.attribute_values[self.attribute_names.index("Background Color")],
        )
        self.component.pack()
