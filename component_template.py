import json
import tkinter as tk


class ComponentTemplate:
    def __init__(self, name, category, source_class):
        self.name = name
        self.category = category
        self.source_class = source_class
        self.attribute_names = []
        self.attribute_json_names = []
        self.attribute_field = []
        self.attribute_value = []

    def add_property(self, name, json_attribute, button_type, default_value):
        self.attribute_names.append(name)
        self.attribute_json_names.append(json_attribute)
        self.attribute_field.append(button_type)
        self.attribute_value.append(default_value)

    def show_properties(self):
        print(f"Component Name: {self.name}")
        print(f"Source Class: {self.source_class}")
        print("Attribute Names:")
        for attr_name in self.attribute_names:
            print(f"  - {attr_name}")
        print("JSON Attribute Names:")
        for json_name in self.attribute_json_names:
            print(f"  - {json_name}")
        print("Attribute Field:")
        for attr_field in self.attribute_field:
            print(f"  - {attr_field}")
        print("Attribute Values:")
        for attr_value in self.attribute_value:
            print(f"  - {attr_value}")

    def save_to_json(self, filename):
        data = {
            "name": self.name,
            "source_class": self.source_class,
            "attribute_names": self.attribute_names,
            "attribute_json_names": self.attribute_json_names
        }
        with open(filename, 'w') as json_file:
            json.dump(data, json_file, indent=2)

    def get_attribute_component(self, attribute_name, master=None):
        if attribute_name in self.attribute_names:
            index = self.attribute_names.index(attribute_name)
            attribute_type = self.attribute_field[index]

            if attribute_type == "text":
                return tk.Entry(master)
            elif attribute_type == "slider":
                return tk.Scale(master, from_=0, to=100, orient=tk.HORIZONTAL)
            elif attribute_type == "table":
                return "Componenta de tip tabel"
            elif attribute_type == "color":
                color_var = tk.StringVar(master)
                color_var.set("#000000")

                color_options = ["white", "black", "red", "green", "blue", "yellow", "purple", "orange"]

                color_menu = tk.OptionMenu(master, color_var, *color_options)
                return color_menu
            else:
                return f"Tip de atribut necunoscut: {attribute_type}"
        else:
            return f"Atributul '{attribute_name}' nu există în lista de atribute."

    def modify_value(self, attribute_name, value):
        if attribute_name in self.attribute_names:
            index = self.attribute_names.index(attribute_name)
            self.attribute_field[index] = value
