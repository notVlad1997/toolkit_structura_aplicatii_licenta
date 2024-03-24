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

        space_button = tk.Button(layer_frame, text=" ")
        space_button.grid(row=0, column=0, sticky="ew")

        button = tk.Button(layer_frame, text=layer_name,
                           command=lambda comp=component: self.properties_frame.display_component_properties(comp))
        button.grid(row=0, column=1, sticky="ew")
        layer_frame.id = layer_name

        rename_button = tk.Button(layer_frame, text="Rename",
                                  command=lambda frame=layer_frame, comp=component: self.rename_entry(frame, comp))
        rename_button.grid(row=0, column=2, sticky="ew")

        component_widget = component.return_component(window=window)

        delete_button = tk.Button(layer_frame, text="Delete",
                                  command=lambda comp=component,
                                                 frame=layer_frame: self.delete_layer(component,
                                                                                      layer_frame))
        delete_button.grid(row=0, column=3, sticky="ew")
        if (str(type(component)) == f"<class 'FrameTkinter'>" or
                str(type(component)) == "<class 'component.Frame.frame_Tkinter.FrameTkinter'>" or
                str(type(component)) == f"<class 'component.Frame.windowFrame_Custom.FrameWindowTK'>" or
                str(type(component)) == "<class 'component.Frame.windowFrame_Custom.FrameWindowTK'>"):
            self.frames_list.append(component_widget)
            expand_button = tk.Button(layer_frame, text="Collapse",
                                      command=lambda frame=layer_frame, comp=component: self.toggle_extend(frame, comp))
            expand_button.grid(row=0, column=4, sticky="ew")

    def rename_entry(self, layer_frame, component):
        """
        Method to toggle between displaying the entry field for renaming and hiding it.
        """
        if layer_frame.grid_slaves(row=0, column=2)[0]['text'] == "Rename":
            rename_entry = tk.Entry(layer_frame)
            rename_entry.insert(0, layer_frame.grid_slaves(row=0, column=1)[0]['text'])
            layer_frame.grid_slaves(row=0, column=1)[0].grid_forget()
            rename_entry.grid(row=0, column=1, sticky="ew")
            layer_frame.grid_slaves(row=0, column=2)[0].config(text="Confirm")
        else:
            component.layer_name = layer_frame.grid_slaves(row=0, column=1)[0].get()
            button = tk.Button(layer_frame, text=component.layer_name,
                               command=lambda comp=component: self.properties_frame.display_component_properties(comp))
            component_list = self.component_tree.create_component_list()
            layer_frame.grid_slaves(row=0, column=1)[0].grid_forget()
            button.grid(row=0, column=1, sticky="ew")
            layer_frame.grid_slaves(row=0, column=2)[0].config(text="Rename")


    def toggle_extend(self, layer_frame, comp):
        frame_depth = None
        component_list = self.component_tree.create_component_list_with_depth()
        for component, depth in component_list:
            if component == comp:
                frame_depth = depth
            elif frame_depth is not None:
                if depth > frame_depth:
                    for child in self.layer_pane.winfo_children():
                        if hasattr(child, "id"):
                            if isinstance(child, tk.Frame) and child.id == component.layer_name:
                                if layer_frame.grid_slaves(row=0, column=3)[0]['text'] == "Collapse":
                                    child.grid_forget()
                                else:
                                    child.grid(row=component_list.index([component, depth]) + 1, column=1, sticky="ew")
                                break
                else:
                    break

        if layer_frame.grid_slaves(row=0, column=3)[0]['text'] == "Extend":
            layer_frame.grid_slaves(row=0, column=3)[0].config(text="Collapse")
        else:
            layer_frame.grid_slaves(row=0, column=3)[0].config(text="Extend")

    def delete_layer(self, comp, layer_frame):
        frame_depth = None
        component_list = self.component_tree.create_component_list_with_depth()
        for component, depth in component_list:
            if component == comp:
                frame_depth = depth
                component.destroy()
                layer_frame.destroy()
            elif frame_depth is not None:
                if depth > frame_depth:
                    for child in self.layer_pane.winfo_children():
                        if hasattr(child, "id"):
                            if isinstance(child, tk.Frame) and child.id == component.layer_name:
                                child.destroy()
                                component.destroy()
                else:
                    break


    def destroy(self):
        for widget in self.layer_pane.winfo_children():
            if not isinstance(widget, tk.Scrollbar):
                widget.destroy()

    def update(self, value):
        component_list = self.component_tree.create_component_list_with_depth()
        for child in self.layer_pane.winfo_children():
            if isinstance(child, tk.Frame) and hasattr(child, "id") and child.id == "Layer":
                child.grid_forget()

        for component, depth in component_list:
            for child in self.layer_pane.winfo_children():
                if hasattr(child, "id"):
                    if isinstance(child, tk.Frame) and child.id == component.layer_name:
                        child.grid(row=component_list.index([component, depth]) + 1, column=1, sticky="ew")
                        # Adjust the text of space_button based on depth
                        space_text = " " * (depth * 2)  # Assuming 2 spaces per depth level, adjust as needed
                        space_button = child.grid_slaves(row=0, column=0)[0]  # Get the space_button
                        space_button.config(text=space_text)
                        break
