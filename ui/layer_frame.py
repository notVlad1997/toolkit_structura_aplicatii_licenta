import tkinter as tk
from observers.observer import Observer
from ui.properties_frame import PropertiesFrame
from ui.util import ui_util


class LayerFrame(Observer):
    def __init__(self, master, component_tree, window):
        self.master = master
        self.layer_pane = ui_util.create_scrollbar_pane(self.master)

        self.window = window
        self.component_tree = component_tree
        self.component_list = self.component_tree.create_component_list()
        self.component_tree.register_observer(self)

        self.properties_frame = PropertiesFrame(master=self.master, component_list=self.component_list)
        self.properties_pane = self.properties_frame.properties_pane

    def create_new_layer(self, component, attribute_name):
        layer_frame = tk.Frame(self.layer_pane)
        layer_frame.grid(row=len(self.layer_pane.grid_slaves()) + 1, column=0, sticky="ew")

        button = tk.Button(layer_frame, text=f"Layer {attribute_name}",
                           command=lambda comp=component: self.properties_frame.display_component_properties(comp))
        button.grid(row=0, column=0, sticky="ew")

        component_widget = component.return_component(self.window)

        delete_button = tk.Button(layer_frame, text="Delete",
                                  command=lambda comp=component,
                                                 frame=layer_frame: self.delete_layer(component, component_widget,
                                                                                      layer_frame))
        delete_button.grid(row=0, column=1, sticky="ew")

    def delete_layer(self, component, ui_component, layer_button):
        self.component_tree.remove_component(component)
        layer_button.destroy()
        ui_component.destroy()

    def destroy(self):
        for widget in self.layer_pane.winfo_children():
            if not isinstance(widget, tk.Scrollbar):
                widget.destroy()

    def update(self, value):
        self.component_list = self.component_tree.create_component_list()
        frames = []
        for widget in self.layer_pane.winfo_children():
            frames.append(widget)
            widget.pack_forget()
        # for component in component_list:
        #     for frame in frames:
        #         if component

