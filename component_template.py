from tkinter import ttk

import json
import tkinter as tk

from observers.subject import Subject


class ComponentTemplate(Subject):
    def __init__(self, name, category, frames=None, layer_name=None, visible=True):
        """
        Constructor.
        :param name: Name of the class
        :param category: Category which is included, must be specified as the folder name where it belongs
        egs:
        component/Frame/component.py
        category = "Frame"
        :param frames: All the other frames, of which components can be switched, can be left empty if unwanted, or it can be removed.
        """
        super().__init__()
        self.name = name
        self.master = None
        self.layer_name = layer_name

        self.category = category

        self.attribute_names = []
        self.attribute_field = []
        self.attribute_values = []

        self.update_attribute = []
        self.frames_choice = frames

        self.component = None
        self.color_options = ["white", "black", "red", "green", "blue", "yellow", "purple", "orange"]

        if frames is not None:
            self.add_property(name="Frame", button_type="dropdown", default_value=self.frames_choice)
            self.attribute_values[self.attribute_names.index("Frame")] = self.frames_choice[0]

        self.visible = visible

    def add_property(self, name, button_type, default_value):
        """
        Method which will add a new attribute, that can be modified.
        :param name: The name of the property that will be shown in the UI app.
        :param button_type: The name of the input type that will be used in the UI.
        :param default_value: The default value for the new item added.
        :return:
        """
        self.attribute_names.append(name)
        self.attribute_field.append(button_type)
        self.attribute_values.append(default_value)

    def show_properties(self):
        """
        Method which will show all the properties, with their current value.
        :return:
        """
        print(f"Component Name: {self.name}")
        print("Attribute Names:")
        for attr_name in self.attribute_names:
            print(f"  - {attr_name}")
        print("Attribute Field:")
        for attr_field in self.attribute_field:
            print(f"  - {attr_field}")
        print("Attribute Values:")
        for attr_value in self.attribute_values:
            print(f"  - {attr_value}")

    def save_to_json(self, filename):
        """
        Method which will add all the properties into a .json file.
        :param filename: The name of the file in which will be saved.
        :return:
        """
        data = {
            "name": self.name,
            "category": self.category,
            "attributes": []
        }

        for name, value in zip(self.attribute_names, self.attribute_values):
            attribute_data = {
                "attribute_name": name,
                "attribute_value": str(value)
            }
            data["attributes"].append(attribute_data)

        with open(filename, 'w') as json_file:
            json.dump(data, json_file, indent=2)

    def load_components_from_data(self, data):
        """
        Method that loads the attributes, into self
        :param data: Data which is going to be stored.
        :return:
        """
        for attribute_data in data.get("attributes", []):
            attribute_name = attribute_data.get("attribute_name", "")
            attribute_value = attribute_data.get("attribute_value", "")
            self.modify_value(attribute_name, attribute_value)

    def get_attribute_component(self, attribute_name, master):
        """
        Method which gets the input type for the required attribute
        :param attribute_name: The name of the attribute that is required
        :param master: The name of the panel in which the option will be added.
        :return: The input type.
        """
        if attribute_name in self.attribute_names:
            index = self.attribute_names.index(attribute_name)
            attribute_type = self.attribute_field[index]
            attribute_val = self.attribute_values[index]
            if attribute_type == "text":
                self.update_attribute.append(tk.StringVar(value=attribute_val))
                self.update_attribute[index].trace_add("write", lambda *args, i=index: self.update_value(i))
                return tk.Entry(master, textvariable=self.update_attribute[index])
            elif attribute_type == "slider":
                self.update_attribute.append(tk.IntVar(value=attribute_val))
                self.update_attribute[index].trace_add("write", lambda *args, i=index: self.update_value(i))
                return tk.Scale(master, from_=0, to=1000, orient=tk.HORIZONTAL, variable=self.update_attribute[index])
            elif attribute_type == "table":
                self.update_attribute.append(tk.StringVar())
                table_frame = tk.Frame(master)
                table_frame.pack()

                table_label = tk.Label(table_frame, text="Table Data")
                table_label.grid(row=0, column=0)

                table = ttk.Treeview(table_frame, columns=("Table Data"))
                table.grid(row=1, column=0)

                data = attribute_val.split(',')
                for value in data:
                    table.insert("", "end", values=(value,))

                entry_var = tk.StringVar()
                entry = tk.Entry(table_frame, textvariable=entry_var)
                entry.grid(row=0, column=0)

                def add_row():
                    value = entry_var.get()
                    if value:
                        table.insert("", "end", values=(value,))
                        entry_var.set("")
                        index = self.attribute_names.index(attribute_name)
                        updated_values = [table.item(item, 'values')[0] for item in table.get_children()]
                        self.update_attribute[index].set(','.join(updated_values))
                        self.update_value(index)

                add_button = tk.Button(table_frame, text="Add Row", command=add_row)
                add_button.grid(row=2, column=1)

                def delete_row():
                    selected_items = table.selection()
                    for item in selected_items:
                        table.delete(item)
                        index = self.attribute_names.index(attribute_name)
                        updated_values = [table.item(item, 'values')[0] for item in table.get_children()]
                        self.update_attribute[index].set(','.join(updated_values))
                        self.update_value(index)

                delete_button = tk.Button(table_frame, text="Delete Selected", command=delete_row)
                delete_button.grid(row=2, column=2)

                def update_row():
                    selected_item = table.selection()
                    if selected_item:
                        new_value = entry_var.get()
                        table.item(selected_item, values=(new_value,))
                        entry_var.set("")
                        index = self.attribute_names.index(attribute_name)
                        updated_values = [table.item(item, 'values')[0] for item in table.get_children()]
                        self.update_attribute[index].set(','.join(updated_values))
                        self.update_value(index)

                update_button = tk.Button(table_frame, text="Update Selected", command=update_row)
                update_button.grid(row=2, column=3)

                return table_frame
            elif attribute_type == "color":
                self.update_attribute.append(tk.StringVar(value=attribute_val))
                self.update_attribute[index].trace_add("write", lambda *args, i=index: self.update_value(i))

                color_menu = tk.OptionMenu(master, self.update_attribute[index], *self.color_options)

                return color_menu
            elif attribute_type == "dropdown":
                self.update_attribute.append(tk.StringVar(value=attribute_val[0]))
                self.update_attribute[index].set(attribute_val[0])
                self.update_attribute[index].trace_add("write", lambda *args, i=index: self.update_value(i))

                dropdown = tk.OptionMenu(master, self.update_attribute[index], *attribute_val)

                return dropdown
            else:
                return f"Tip de atribut necunoscut: {attribute_type}"
        else:
            return f"Atributul '{attribute_name}' nu există în lista de atribute."

    def update_value(self, index):
        """
        Method which triggers when a value field has been updated.
        It updates both the UI Interface, and the storage.
        :param index: The location where the value is going to be modified in the list of attribute_value
        :return:
        """
        self.attribute_values[index] = self.update_attribute[index].get()
        #self.show_properties()
        self.update_component()
        self.notify_observers(self)

    def modify_value(self, attribute_name, value):
        """
        Method which changes the value of an attribute with a new one, from the UI.
        :param attribute_name: The name of the attribute that is required
        :param value: The name of the  in which the option will be added.
        :return:
        """
        if attribute_name in self.attribute_names:
            index = self.attribute_names.index(attribute_name)
            self.attribute_values[index] = value
        else:
            print(f"{attribute_name} NO")

    def return_component(self, window=None):
        """
        Method which creates and returns a UI Component
        :param window: The window_frame which is going to be placed, in most cases TK, or WindowFrame.
        :return: The UI Component
        """
        self.update_component(window)
        return self.component

    def update_component(self, window=None):
        """
        Method which updates the compononent UI element.
        It must be implemented at the class itself that extends this base class.
        :param window: The window_frame which is going to be placed, in most cases TK, or WindowFrame.
        :return:
        """
        print('Nothing')

    def remove_property(self, attribute_name):
        """
        Method to remove a property from the component template.
        :param attribute_name: The name of the property to be removed.
        """
        if attribute_name in self.attribute_names:
            index = self.attribute_names.index(attribute_name)
            del self.attribute_names[index]
            del self.attribute_field[index]
            del self.attribute_values[index]
            if index < len(self.update_attribute):
                del self.update_attribute[index]
        else:
            print(f"Property '{attribute_name}' not found in the list of attributes.")
