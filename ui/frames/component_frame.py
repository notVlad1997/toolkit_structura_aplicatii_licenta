from ui.components.component_tree import ComponentsTree
from ui.util import ui_util
import tkinter as tk


class ComponentFrame:
    def __init__(self, master, frames_list, component_tree, layer_frame):
        self.master = master
        self.component_pane = ui_util.create_scrollbar_pane(self.master)
        self.frames_list = frames_list
        self.component_tree = component_tree
        self.layer_frame = layer_frame

    def destroy(self):
        for widget in self.component_pane.winfo_children():
            widget.destroy()

    def add_new_component(self, attribute_name, element, window):
        """
        Method that adds a new component on the window, it creates a new layer, and stores it.
        :param attribute_name: Name of the attribute, that it will be added to the UI.
        :param element: Name of the class, that it's going to be added as a new component.
        :return:
        """
        component = element(self.frames_list)
        component.register_observer(self.component_tree)

        self.layer_frame.create_new_layer(component=component, attribute_name=attribute_name, window=window)
        if str(element) == f"<class 'FrameTkinter'>":
            self.component_tree.add_component(ComponentsTree(value=component))
        elif str(element) == f"<class 'component.Frame.windowFrame_Custom.FrameWindowTK'>":
            self.component_tree.value = component
        else:
            self.component_tree.add_component(component)

    def component_button(self, button_name, class_element, window=None):
        """
        Method that adds all the buttons with the functionality of getting all the components of the category.
        :param button_name: The name of the button that will be displayed.
        :param class_element: The class of the component
        :return:
        """
        button = tk.Button(self.component_pane, text=button_name,
                           command=lambda name=button_name: self.add_new_component(name, class_element, window=window))
        button.pack(side=tk.TOP)
