import importlib
import json
import os
import tkinter as tk
import inspect
from copy import copy
from tkinter import filedialog

from ui.frame.layer_window import FrameWindowTK
from component_template import ComponentTemplate
from ui.components import WindowComponents

class MainFrame(tk.Frame):
    """
    Constructor. It creates the UI app.
    """

    def __init__(self, master):
        super().__init__(master)
        self.saved_layer_pane_elements = None
        self.saved_window_elements = None
        self.master = master

        self.main_pane = None
        self.middle_pane = None
        self.category_pane = None
        self.component_pane = None
        self.window = None
        self.layer_pane = None
        self.properties_pane = None
        self.windows_pane = None

        self.config(width=600, height=600)
        self.create_widgets()
        self.pack(fill=tk.BOTH, expand=True)
        self.rows = 1

        self.component_list = []
        self.frames_list = []
        self.windows_buttons = []

        self.current_window_id = -1
        self.create_menu()


    """
    Method that creates the Category Panel for the Application.It includes all the folders from "component" folder.
    :arg left_pane: Panel on which the Category will be added.
    """

    def create_category_panel(self, left_pane):
        self.category_pane = tk.Canvas(left_pane, width=500, height=500)
        scrollbar = tk.Scrollbar(self.category_pane, command=self.category_pane.yview)
        self.category_pane.config(yscrollcommand=scrollbar.set, scrollregion=(0, 0, 0, 2000))
        self.category_pane.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        component_path = "./component"
        folders = [folder for folder in os.listdir(component_path) if
                   os.path.isdir(os.path.join(component_path, folder))]

        for folder in folders:
            button = tk.Button(self.category_pane, text=folder, command=lambda f=folder: self.category_clicked(f))
            button.pack(side=tk.TOP)

        self.create_components_panel(left_pane)

    """
    Method that creates the Component Panel when a Category is clicked. It will add all the .py files, importing them. 
    :arg category: The category on which the Component Tab will be updated.
    """

    def category_clicked(self, category):
        folder_path = f"./component/{category}"
        python_files = [f for f in os.listdir(folder_path) if f.endswith(".py") and not f.startswith("__")]
        if python_files:
            for widget in self.component_pane.winfo_children():
                widget.destroy()
            for python_file in python_files:
                module_name = os.path.splitext(python_file)[0]
                template_file_path = os.path.join(folder_path, python_file)
                try:
                    with open(template_file_path, 'r') as file:
                        module_content = file.read()
                    namespace = {}
                    exec(module_content, namespace)
                    for name, obj in namespace.items():
                        if inspect.isclass(obj) and issubclass(obj, ComponentTemplate) and obj != ComponentTemplate:
                            component_instance = obj(self.frames_list[self.current_window_id].get_component_list())
                            self.category_button(component_instance.name, obj)
                except Exception as e:
                    print(f"Error loading module: {module_name}, {e}")
        else:
            print(f"No Python files found in folder: {folder_path}")

    """
    Method that adds all the buttons with the functionality of getting all the components of the category.
    :arg button_name: The name of the button will be displayed.
    :arg element: The class element
    """

    def category_button(self, button_name, class_element):
        button = tk.Button(self.component_pane, text=button_name,
                           command=lambda name=button_name: self.add_new_component(name, class_element))
        button.pack(side=tk.TOP)

    """
    Method that adds a new component on the window and it creates a new layer, and stores it.
    :arg attribute_name: Name of the attribute, that it will be added to the UI
    :arg element: Name of the class, that its going to be added as a new component. 
    """

    def add_new_component(self, attribute_name, element):
        component = element(self.frames_list[self.current_window_id].get_component_list())
        self.component_list[self.current_window_id].add_component(component)

        layer_frame = tk.Frame(self.layer_pane)
        layer_frame.pack(side=tk.TOP)

        button = tk.Button(layer_frame, text=f"Layer {attribute_name}",
                           command=lambda comp=component: self.properties_component(comp))
        button.pack(side=tk.LEFT)

        component_widget = component.return_component(self.window)

        delete_button = tk.Button(layer_frame, text="Delete",
                                  command=lambda comp=component,
                                                 frame=layer_frame: self.delete_component(component, component_widget,
                                                                                          layer_frame))
        delete_button.pack(side=tk.RIGHT)
        if str(element) == f"<class 'FrameTkinter'>":
            self.frames_list[self.current_window_id].add_component(component_widget)

    """
    Method that activates when the "Delete" button is pressed.
    It removes the layer, and the added component from frame.
    """

    def delete_component(self, component, component_added, layer_button):
        if str(component.__class__) == f"<class 'FrameTkinter'>":
            self.frames_list[self.current_window_id].remove_component(component.return_component())
        self.component_list[self.current_window_id].remove_component(component)
        layer_button.destroy()
        component_added.destroy()

    """
    Method that it activates when the layer is pressed.
    It triggers the options that can be edited.
    :arg attribute_name: The name of the component that it needs to pull the categories.
    """

    def properties_component(self, component_pressed):
        component = None
        for comp in self.component_list[self.current_window_id].components:
            if component_pressed == comp:
                component = comp
                break
        if component:
            self.display_component_properties(component)
        else:
            for frames in self.frames_list[self.current_window_id].components:
                if component_pressed == frames:
                    component = frames
                    break
            if component:
                self.display_component_properties(component)
            else:
                print('No component for properties')

    """
    Method that display all the options that can be edited in the UI.
    :arg component: The component that has all the properties.
    """

    def display_component_properties(self, component):
        for widget in self.properties_pane.winfo_children():
            widget.destroy()

        print(component.attribute_names)
        for attribute_name in component.attribute_names:
            label = tk.Label(self.properties_pane, text=f"{attribute_name}:")
            label.pack(side=tk.TOP)

            attribute_component = component.get_attribute_component(attribute_name, master=self.properties_pane)
            attribute_component.pack(side=tk.TOP)

    """
    Method that adds a frame for the component panel to be added.
    :args left_pane: Frame that will contain all the buttons of Components.
    """

    def create_components_panel(self, left_pane):
        self.component_pane = tk.Frame(left_pane)
        left_pane.add(self.category_pane, minsize=200)
        left_pane.add(self.component_pane, minsize=200)

    """
    Method that adds a frame for the layers panel to be added.
    :args left_pane: Frame that will contain all the buttons of Layer.
    """

    def create_layers_panel(self, right_pane):
        self.layer_pane = tk.Canvas(right_pane, width=500, height=500)
        scrollbar = tk.Scrollbar(self.layer_pane, command=self.layer_pane.yview)
        self.layer_pane.config(yscrollcommand=scrollbar.set, scrollregion=(0, 0, 0, 2000))
        self.layer_pane.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        right_pane.add(self.layer_pane, minsize=200)

    """
    Method that adds a frame for the properties panel to be added.
    :args left_pane: Frame that will contain all the buttons of Properties.
    """

    def create_properties_panel(self, right_pane):
        self.properties_pane = tk.Frame(right_pane)
        right_pane.add(self.properties_pane, minsize=200)

    """
    Method that implements the whole structure of the UI Interface.
    """

    def create_widgets(self):
        self.main_pane = tk.PanedWindow(self, orient=tk.HORIZONTAL, sashrelief=tk.SUNKEN, sashwidth=7)
        self.main_pane.pack(fill=tk.BOTH, expand=True)

        left_pane = tk.PanedWindow(self.main_pane, orient=tk.VERTICAL, sashrelief=tk.RAISED, sashwidth=7)
        self.create_category_panel(left_pane)

        self.middle_pane = tk.Frame(self.main_pane)
        self.middle_pane.pack_propagate(False)

        self.window = self.middle_pane

        self.windows_pane = tk.Frame(self.middle_pane, height=30, highlightbackground="gray60", highlightthickness=1)
        self.windows_pane.pack(fill=tk.X)
        self.windows_pane.id = "New Windows"

        right_pane = tk.PanedWindow(self.main_pane, orient=tk.VERTICAL, sashrelief=tk.RAISED, sashwidth=7)
        right_pane.pack_propagate(False)

        self.create_layers_panel(right_pane)
        self.create_properties_panel(right_pane)

        self.main_pane.add(left_pane, minsize=200)
        self.main_pane.add(self.middle_pane, minsize=600)
        self.main_pane.add(right_pane, minsize=500)

    """
    Method that implements the header.
    """

    def create_menu(self):
        menubar = tk.Menu(self.master)
        self.master.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New", command=self.action_new)
        file_menu.add_command(label="Open", command=self.action_open)
        file_menu.add_command(label="Save", command=self.action_save)
        file_menu.add_separator()
        file_menu.add_command(label="Generate", command=self.dummy_function)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.master.destroy)

        menubar.add_cascade(label="Settings", command=self.dummy_function)

    def window_button_pressed(self, index):
        self.component_list[self.current_window_id].get_component(0).return_component().destroy()
        for widget in self.layer_pane.winfo_children():
            widget.destroy()

        for widget in self.window.winfo_children():
            if hasattr(widget, 'id'):
                if not widget.id == f"Title Bar":
                    widget.destroy()
            else:
                widget.destroy()

        components = self.component_list[index].components

        for component in components:
            layer_frame = tk.Frame(self.layer_pane)
            layer_frame.pack(side=tk.TOP)

            button_name = f"Layer {component.name}"
            button = tk.Button(layer_frame, text=button_name,
                               command=lambda comp=component: self.properties_component(comp))
            button.pack(side=tk.LEFT)

            delete_button = tk.Button(layer_frame, text="Delete",
                                      command=lambda comp=component, frame=layer_frame: self.delete_component(comp,
                                                                                                              comp.return_component(
                                                                                                                  self.window),
                                                                                                              frame))
            delete_button.pack(side=tk.RIGHT)

            component_widget = component.return_component()
            component_widget.pack()

        self.current_window_id = index

    def action_new(self):
        for widget in self.layer_pane.winfo_children():
            if not isinstance(widget, tk.Scrollbar):
                widget.destroy()

        is_mainpane = False
        for widget in self.window.winfo_children():
            if hasattr(widget, 'id'):
                if widget.id == "New Windows":
                    is_mainpane = True
                    break
                elif not widget.id == "Title Bar":
                    widget.destroy()
            else:
                widget.destroy()

        if is_mainpane is False:
            self.component_list[self.current_window_id].get_component(0).return_component().destroy()
            self.window = self.middle_pane

        self.current_window_id = self.current_window_id + 1
        self.component_list.append(WindowComponents())
        self.frames_list.append(WindowComponents())

        self.add_new_component("TK", FrameWindowTK)
        component_widget = self.component_list[self.current_window_id].get_component(0).return_component().content_frame

        self.frames_list[self.current_window_id].add_component(component_widget)
        self.window = component_widget

        self.saved_layer_pane_elements = copy(self.layer_pane)
        self.saved_window_elements = [widget for widget in self.window.winfo_children()]

        new_ui = tk.Button(self.windows_pane, text="Hello", command=lambda index=len(self.windows_buttons):
        self.window_button_pressed(index=index))
        self.windows_buttons.append(new_ui)
        new_ui.pack(side=tk.LEFT, fill=tk.Y)

    def action_save(self):
        self.component_list[self.current_window_id].save_json()

    def action_open(self):
        file_path = filedialog.askopenfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if file_path:
            try:
                with (open(file_path, 'r') as json_file):
                    data = json.load(json_file)

                    if "name" not in data or "category" not in data or "attributes" not in data:
                        print("No class with such information.")
                        return

                    component_name = data["name"]
                    category_name = data["category"]
                    attributes_data = data["attributes"]

                    folder_path = f"./component/{category_name}"

                    if os.path.exists(folder_path) and os.path.isdir(folder_path):
                        python_files = [f for f in os.listdir(folder_path) if
                                        f.endswith(".py") and not f.startswith("__")]

                        for python_file in python_files:
                            module_name = os.path.splitext(python_file)[0]
                            template_file_path = os.path.join(folder_path, python_file)

                            try:
                                with open(template_file_path, 'r') as file:
                                    module_content = file.read()

                                class_name = None
                                namespace = {}
                                exec(module_content, namespace)
                                for name, obj in namespace.items():
                                    if inspect.isclass(obj) and issubclass(
                                            obj, ComponentTemplate) and obj != ComponentTemplate:
                                        class_name = name
                                        break

                                if class_name:
                                    module = importlib.import_module(f"component.{category_name}.{module_name}")
                                    class_instance = getattr(module, class_name)

                                    component_instance = class_instance()

                                    for attribute_data in attributes_data:
                                        attribute_name = attribute_data.get("attribute_name", "")
                                        attribute_value = attribute_data.get("attribute_value", "")
                                        component_instance.modify_value(attribute_name=attribute_name,
                                                                        value=attribute_value)
                                        component_instance.show_properties()

                                    self.component_list[self.current_window_id].add_component(component_instance)

                                    component_widget = component_instance.return_component(self.window)
                                    component_widget.pack()

                                    button_name = f"Layer {category_name} - {component_name}"
                                    self.layer_button(button_name, component_instance, component_widget)

                                    break

                            except Exception as e:
                                print(f"Error on module loading: {module_name}, {e}")

                    else:
                        print(f"Not existent JSON File")

            except Exception as e:
                print(f"JSON File Error: {e}")

    def layer_button(self, button_name, component_instance, component_widget):
        layer_frame = tk.Frame(self.layer_pane)
        layer_frame.pack(side=tk.TOP)

        button = tk.Button(layer_frame, text=button_name,
                           command=lambda comp=component_instance: self.properties_component(comp))
        button.pack(side=tk.LEFT)

        delete_button = tk.Button(layer_frame, text="Delete", command=lambda comp=component_instance,
                                                                             frame=layer_frame: self.delete_component(
            component_instance, component_widget, layer_frame))

        delete_button.pack(side=tk.RIGHT)
        component_widget.pack()

    def dummy_function(self):
        print("Function to be implemented.")
