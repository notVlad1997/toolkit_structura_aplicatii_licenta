import tkinter as tk

from ui.util import ui_util


class PropertiesFrame:
    def __init__(self, master, component_tree):
        self.master = master
        self.properties_pane = ui_util.create_scrollbar_pane(self.master)
        self.component_tree = component_tree

    def find_property_page(self, component_pressed):
        component_list = self.component_tree.create_component_list()
        component = None
        for comp in component_list:
            if component_pressed == comp:
                component = comp
                break
        return component

    def destroy_property_page(self):
        for widget in self.properties_pane.winfo_children():
            widget.destroy()

    def display_component_properties(self, component):
        self.destroy_property_page()
        found_component = self.find_property_page(component)
        print(found_component)
        for attribute_name in found_component.attribute_names:
            label = tk.Label(self.properties_pane, text=f"{attribute_name}:")
            label.pack(side=tk.TOP)

            attribute_component = found_component.get_attribute_component(attribute_name, master=self.properties_pane)
            attribute_component.pack(side=tk.TOP)
