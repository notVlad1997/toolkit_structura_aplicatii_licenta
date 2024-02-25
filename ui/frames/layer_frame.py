import tkinter as tk
from observers.observer import Observer
from ui.frames.properties_frame import PropertiesFrame
from ui.util import ui_util


class LayerFrame(Observer):
    def __init__(self, master, component_tree, window, frames_list):
        self.master = master
        self.layer_pane = ui_util.create_scrollbar_pane(self.master)

        self.window = window
        self.component_tree = component_tree

        self.component_tree.register_observer(self)
        self.frames_list = frames_list

        self.properties_frame = PropertiesFrame(master=self.master, component_tree=self.component_tree)
        self.properties_pane = self.properties_frame.properties_pane

        self.index = 0

    def create_new_layer(self, component, attribute_name, window=None):
        layer_frame = tk.Frame(self.layer_pane)
        layer_frame.grid(row=len(self.layer_pane.grid_slaves()) + 1, column=0, sticky="ew")

        layer_name = f"Layer {attribute_name} {str(self.index)}"
        self.index = self.index + 1
        component.layer_name = layer_name

        button = tk.Button(layer_frame, text=layer_name,
                           command=lambda comp=component: self.properties_frame.display_component_properties(comp))
        button.id = "Button"
        button.grid(row=0, column=0, sticky="ew")
        layer_frame.id = layer_name

        component_widget = component.return_component(window=window)

        delete_button = tk.Button(layer_frame, text="Delete",
                                  command=lambda comp=component,
                                                 frame=layer_frame: self.delete_layer(component, component_widget,
                                                                                      layer_frame))
        delete_button.grid(row=0, column=1, sticky="ew")

        if str(type(component)) == f"<class 'FrameTkinter'>":
            self.frames_list.append(component_widget)
        elif str(type(component)) == f"<class 'ui.window_frame.window_frame.FrameWindowTK'>":
            self.frames_list.append(component_widget)

    def delete_layer(self, component, ui_component, layer_button):
        self.component_tree.remove_component(component)
        layer_button.destroy()
        ui_component.destroy()

    def destroy(self):
        for widget in self.layer_pane.winfo_children():
            if not isinstance(widget, tk.Scrollbar):
                widget.destroy()

    def update(self, value):
        component_list = self.component_tree.create_component_list()
        for child in self.layer_pane.winfo_children():
            if isinstance(child, tk.Frame) and hasattr(child, "id") and child.id == "Layer":
                child.grid_forget()

        for component in component_list:
            for child in self.layer_pane.winfo_children():
                if isinstance(child, tk.Frame) and child.id == component.layer_name:
                    child.grid(row=component_list.index(component) + 1, column=0, sticky="ew")
