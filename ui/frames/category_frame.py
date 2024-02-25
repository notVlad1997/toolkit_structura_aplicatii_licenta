import inspect
import os
import tkinter as tk

from component_template import ComponentTemplate
from ui.util import ui_util


class CategoryFrame:
    def __init__(self, master):
        self.master = master
        self.category_pane = ui_util.create_scrollbar_pane(self.master)

    def create_category_panel(self, component_frame, frame_list, window):
        """
        Method that creates the Category Panel for the Application.It includes all the folders from "component" folder.
        :return:
        """
        component_path = "./component"
        folders = [folder for folder in os.listdir(component_path) if
                   os.path.isdir(os.path.join(component_path, folder))]

        for folder in folders:
            button = tk.Button(self.category_pane, text=folder,
                               command=lambda f=folder: self.category_clicked(f, component_frame, frame_list, window=window))
            button.pack(side=tk.TOP)

        return self.category_pane

    def category_clicked(self, category, component_frame, frame_list, window=None):
        """
        Method that creates the Component Panel when a Category is clicked. It will add all the .py files, importing them.
        :param frame_list:
        :param component_frame: The "Component Frame" instance of Class
        :param category: The category on which the Component Tab will be updated.
        :return:
        """
        folder_path = f"./component/{category}"
        python_files = [f for f in os.listdir(folder_path) if f.endswith(".py") and not f.startswith("__")]
        if python_files:
            component_frame.destroy()
            for python_file in python_files:
                self.open_file(python_file=python_file, folder_path=folder_path, component_frame=component_frame, frame_list=frame_list, window=window)

        else:
            print(f"No Python files found in folder: {folder_path}")

    def open_file(self, python_file, folder_path, component_frame, frame_list, window):
        """
        Module that opens a file and reads it
        :param frame_list:
        :param component_frame: The "Component Frame" instance of Class
        :param python_file: The file
        :param folder_path: The folder where the file is located
        :return:
        """
        module_name = os.path.splitext(python_file)[0]
        template_file_path = os.path.join(folder_path, python_file)
        try:
            with open(template_file_path, 'r') as file:
                module_content = file.read()
            namespace = {}
            self.check_component_template(module_content=module_content, namespace=namespace,
                                          component_frame=component_frame, frame_list=frame_list, window=window)
        except Exception as e:
            print(f"Error loading module: {module_name}, {e}")

    def check_component_template(self, module_content, namespace, frame_list, component_frame, window):
        """
        Method that checks if the opened class is instance of ComponentTemplate
        :param component_frame:
        :param frame_list: The "Component Frame" instance of Class
        :param module_content: Module which is going to be executed
        :param namespace: A dictionary
        :return:
        """
        exec(module_content, namespace)
        for name, obj in namespace.items():
            if inspect.isclass(obj) and issubclass(obj, ComponentTemplate) and obj != ComponentTemplate:
                component_instance = obj(frame_list)
                if component_instance.visible is True:
                    component_frame.component_button(component_instance.name, obj, window=window)
