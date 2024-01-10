import os
import tkinter as tk
import inspect

from component_template import ComponentTemplate
from ui.window import FrameWindow
from ui.components import WindowComponents


class MainFrame(tk.Frame):
    """
    Constructor. It creates the UI app.
    """

    def __init__(self, master):
        super().__init__(master)
        self.master = master

        self.main_pane = None
        self.category_pane = None
        self.component_pane = None
        self.window = None
        self.layer_pane = None
        self.properties_pane = None

        self.config(width=600, height=600)
        self.create_widgets()
        self.pack(fill=tk.BOTH, expand=True)
        self.rows = 1

        self.component_list = WindowComponents()

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
                            component_instance = obj()
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
    Method that a new component on the window and it creates a new layer, and stores it
    """
    def add_new_component(self, attribute_name, element):
        print(f"Name attribute clicked: {attribute_name}")
        button = tk.Button(self.layer_pane, text=f"Layer button for {attribute_name}",
                           command=lambda name=attribute_name: self.properties_component(name, element))
        button.pack(side=tk.TOP)
        component = element()
        self.component_list.add_component(component)

        component_widget = component.return_component(self.window.interior_frame)
        component_widget.pack()

    def properties_component(self, attribute_name, object):
        print(f"Layer button clicked for: {attribute_name}")
        component = None
        for comp in self.component_list.components:
            if comp.name == attribute_name:
                component = comp
                break

        # Dacă componenta corespunzătoare a fost găsită, afișați proprietățile în properties_pane
        if component:
            self.display_component_properties(component)
        else:
            print("Component not found.")

    def display_component_properties(self, component):
        # Ștergeți toate widget-urile din properties_pane
        for widget in self.properties_pane.winfo_children():
            widget.destroy()

        # Iterați prin toate atributele componente și adăugați-le în properties_pane
        for attribute_name in component.attribute_names:
            label = tk.Label(self.properties_pane, text=f"{attribute_name}:")
            label.pack(side=tk.TOP)

            # Utilizați get_attribute_component pentru a obține componenta corespunzătoare atributului
            attribute_component = component.get_attribute_component(attribute_name, master=self.properties_pane)
            attribute_component.pack(side=tk.TOP)

    def create_components_panel(self, left_pane):
        self.component_pane = tk.Frame(left_pane)
        left_pane.add(self.category_pane, minsize=200)
        left_pane.add(self.component_pane, minsize=200)

    def create_widgets(self):
        self.main_pane = tk.PanedWindow(self, orient=tk.HORIZONTAL, sashrelief=tk.SUNKEN, sashwidth=7)
        self.main_pane.pack(fill=tk.BOTH, expand=True)

        left_pane = tk.PanedWindow(self.main_pane, orient=tk.VERTICAL, sashrelief=tk.RAISED, sashwidth=7)
        self.create_category_panel(left_pane)

        self.main_pane.add(left_pane, minsize=200)

        middle_pane = tk.PanedWindow(self.main_pane, orient=tk.VERTICAL, sashrelief=tk.RAISED, sashwidth=7)
        self.main_pane.add(middle_pane, minsize=600)
        middle_pane.pack_propagate(False)

        self.window = FrameWindow(master=middle_pane)
        middle_pane.add(self.window, minsize=200)

        right_pane = tk.PanedWindow(self.main_pane, orient=tk.VERTICAL, sashrelief=tk.RAISED, sashwidth=7)
        self.main_pane.add(right_pane, minsize=100)
        right_pane.pack_propagate(False)

        self.layer_pane = tk.Canvas(right_pane, width=500, height=500)
        scrollbar = tk.Scrollbar(self.layer_pane, command=self.layer_pane.yview)
        self.layer_pane.config(yscrollcommand=scrollbar.set, scrollregion=(0, 0, 0, 2000))
        self.layer_pane.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.properties_pane = tk.Frame(right_pane)
        right_pane.add(self.layer_pane, minsize=200)
        right_pane.add(self.properties_pane, minsize=200)

    def modify(self):
        print("TO DO")

    def create_menu(self):
        menubar = tk.Menu(self.master)
        self.master.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New", command=self.dummy_function)
        file_menu.add_command(label="Open", command=self.dummy_function)
        file_menu.add_command(label="Save", command=self.dummy_function)
        file_menu.add_separator()
        file_menu.add_command(label="Generate", command=self.dummy_function)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.master.destroy)

        menubar.add_cascade(label="Settings", command=self.dummy_function)

    def dummy_function(self):
        print("Function to be implemented.")
