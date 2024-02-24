import inspect
import os
import tkinter as tk

from component_template import ComponentTemplate
from ui.component_frame import ComponentFrame
from ui.util import ui_util


class CategoryFrame:
    def __init__(self, master, component_tree, frames_list):
        self.master = master
        self.category_pane = ui_util.create_scrollbar_pane(self.master)
        self.component_frame = ComponentFrame(master)
        self.component_tree = component_tree
        self.component_list = self.component_tree.create_component_list()
        self.frames_list = frames_list

    def create_category_panel(self):
        """
        Method that creates the Category Panel for the Application.It includes all the folders from "component" folder.
        :param left_pane: Panel on which the Category will be added.
        :return:
        """
        component_path = "./component"
        folders = [folder for folder in os.listdir(component_path) if
                   os.path.isdir(os.path.join(component_path, folder))]

        for folder in folders:
            button = tk.Button(self.category_pane, text=folder, command=lambda f=folder: self.category_clicked(f))
            button.pack(side=tk.TOP)

    def check_component_template(self, module_content, namespace):
        exec(module_content, namespace)
        for name, obj in namespace.items():
            if inspect.isclass(obj) and issubclass(obj, ComponentTemplate) and obj != ComponentTemplate:
                component_instance = obj(self.frames_list.get_component_list())
                self.category_button(component_instance.name, obj)

    def open_file(self, python_file, folder_path):
        module_name = os.path.splitext(python_file)[0]
        template_file_path = os.path.join(folder_path, python_file)
        try:
            with open(template_file_path, 'r') as file:
                module_content = file.read()
            namespace = {}
            self.check_component_template(module_content=module_content, namespace=namespace)
        except Exception as e:
            print(f"Error loading module: {module_name}, {e}")

    def category_clicked(self, category):
        """
        Method that creates the Component Panel when a Category is clicked. It will add all the .py files, importing them.
        :param category: The category on which the Component Tab will be updated.
        :return:
        """
        folder_path = f"./component/{category}"
        python_files = [f for f in os.listdir(folder_path) if f.endswith(".py") and not f.startswith("__")]
        if python_files:
            self.component_frame.destroy()
            for python_file in python_files:
                self.open_file(python_file=python_file, folder_path=folder_path)

        else:
            print(f"No Python files found in folder: {folder_path}")

    def category_button(self, button_name, class_element):
        """
        Method that adds all the buttons with the functionality of getting all the components of the category.
        :param button_name: The name of the button that will be displayed.
        :param class_element: The class of the component
        :return:
        """
        button = tk.Button(self.component_pane, text=button_name,
                           command=lambda name=button_name: self.add_new_component(name, class_element))
        button.pack(side=tk.TOP)
