from tkinter import ttk

import json
import os
import tkinter as tk


class ComponentTemplate:
    """
    Constructor
    """
    def __init__(self, name):
        self.name = name
        self.category = os.path.dirname(name)

        self.attribute_names = []
        self.attribute_field = []
        self.attribute_value = []

        self.update_attribute = []

        self.component = ""
        self.color_options = ["white", "black", "red", "green", "blue", "yellow", "purple", "orange"]

    """
    Method which will add a new attribute, that can be modified.
    :arg name: The name of the property that will be shown in the UI app.
    :arg json_attribute: The name of the attribute that will be added in the .json file.
    :arg button_type: The name of the input type that will be used in the UI.
    :arg default_value: The default value for the new item added.
    """
    def add_property(self, name, button_type, default_value):
        self.attribute_names.append(name)
        self.attribute_field.append(button_type)
        self.attribute_value.append(default_value)

    """
    Method which will show all the properties, with their current value.
    """
    def show_properties(self):
        print(f"Component Name: {self.name}")
        print("Attribute Names:")
        for attr_name in self.attribute_names:
            print(f"  - {attr_name}")
        print("Attribute Field:")
        for attr_field in self.attribute_field:
            print(f"  - {attr_field}")
        print("Attribute Values:")
        for attr_value in self.attribute_value:
            print(f"  - {attr_value}")

    """
    Method which will add all the properties into a .json file.
    :arg filename: The name of the file in which will be saved. 
    """

    def save_to_json(self, filename):
        data = {
            "name": self.name,
            "attribute_names": self.attribute_names,
            "attribute_value": self.attribute_value
        }
        with open(filename, 'w') as json_file:
            json.dump(data, json_file, indent=2)

    """
    Method which gets the input type for the required attribute
    :arg attribute_name: The name of the attribute that is required
    :arg master: The name of the panel in which the option will be added.
    """

    def get_attribute_component(self, attribute_name, master, columns=0):
        if attribute_name in self.attribute_names:
            index = self.attribute_names.index(attribute_name)
            attribute_type = self.attribute_field[index]
            attribute_val = self.attribute_value[index]
            if attribute_type == "text":
                self.update_attribute.append(tk.StringVar(value=attribute_val))
                self.update_attribute[index].trace_add("write", lambda *args, i=index: self.update_value(i))
                return tk.Entry(master, textvariable=self.update_attribute[index])
            elif attribute_type == "slider":
                self.update_attribute.append(tk.IntVar(value=attribute_val))
                self.update_attribute[index].trace_add("write", lambda *args, i=index: self.update_value(i))
                return tk.Scale(master, from_=0, to=100, orient=tk.HORIZONTAL, variable=self.update_attribute[index])
            elif attribute_type == "table":
                table_frame = tk.Frame(master)
                table_frame.pack()

                table_label = tk.Label(table_frame, text="Table Data")
                table_label.grid(row=0, column=0)

                table = ttk.Treeview(table_frame, columns=("Table Data"))
                table.grid(row=1, column=0)

                data = attribute_val.split(',')
                for value in data:
                    table.insert("", "end", values=(value,))
                return table_frame
            elif attribute_type == "color":
                self.update_attribute.append(tk.StringVar(value=attribute_val))
                self.update_attribute[index].trace_add("write", lambda *args, i=index: self.update_value(i))

                color_menu = tk.OptionMenu(master, self.update_attribute[index], *self.color_options)

                return color_menu
            else:
                return f"Tip de atribut necunoscut: {attribute_type}"
        else:
            return f"Atributul '{attribute_name}' nu există în lista de atribute."

    """
    Method which triggers when a value field has been updated.
    It updates both the UI Interface, and the storage.
    :arg index: The location where the value is going to be modified in the list of attribute_value
    """
    def update_value(self, index):
        self.attribute_value[index] = self.update_attribute[index].get()
        self.show_properties()
        self.update_component()

    """
    Method which changes the value of an attribute with a new one, from the UI.
    :arg attribute_name: The name of the attribute that is required
    :arg value: The name of the  in which the option will be added.
    """
    def modify_value(self, attribute_name, value):
        if attribute_name in self.attribute_names:
            index = self.attribute_names.index(attribute_name)
            self.attribute_value[index] = value

    """
    Method which creates and returns a UI Component
    """
    def return_component(self, window=None):
        self.update_component(window)
        return self.component

    """
    Method which updates the compononent UI.
    It must be implemented at the class itself
    """
    def update_component(self, window=None):
        print('Nothing')