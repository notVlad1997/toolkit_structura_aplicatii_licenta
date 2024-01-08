import os
import tkinter as tk
import inspect

from component_template import ComponentTemplate
from ui.window import FrameWindow


class MainFrame(tk.Frame):
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

        self.create_menu()

    def create_category_panel(self):
        left_pane = tk.PanedWindow(self.main_pane, orient=tk.VERTICAL, sashrelief=tk.RAISED, sashwidth=7)
        self.main_pane.add(left_pane, minsize=200)

        self.category_pane = tk.Canvas(left_pane, width=500, height=500)
        scrollbar = tk.Scrollbar(self.category_pane, command=self.category_pane.yview)
        self.category_pane.config(yscrollcommand=scrollbar.set, scrollregion=(0, 0, 0, 2000))
        self.category_pane.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        component_path = "./component"
        folders = [folder for folder in os.listdir(component_path) if os.path.isdir(os.path.join(component_path, folder))]

        for folder in folders:
            button = tk.Button(self.category_pane, text=folder, command=lambda f=folder: self.folder_button_clicked(f))
            button.pack(side=tk.TOP)

        self.create_components_panel(left_pane)

    def folder_button_clicked(self, folder_name):
        print(f"Folder selected: {folder_name}")
        folder_path = f"./component/{folder_name}"

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

                    # Executarea conținutului într-un spațiu de nume separat
                    namespace = {}
                    exec(module_content, namespace)

                    for name, obj in namespace.items():
                        if inspect.isclass(obj) and issubclass(obj, ComponentTemplate) and obj != ComponentTemplate:
                            # Creați o instanță a clasei și apelați metoda show_properties
                            component_instance = obj()
                            component_instance.show_properties()

                            # Creați butoane pentru atributul 'name'
                            self.create_name_buttons(component_instance.name)

                except Exception as e:
                    print(f"Error loading module: {module_name}, {e}")

        else:
            print(f"No Python files found in folder: {folder_path}")


    def create_name_buttons(self, button_name):
        # Creați butoane pentru atributul 'name'
        button = tk.Button(self.component_pane, text=button_name,
                               command=lambda name=button_name: self.name_button_clicked(name))
        button.pack(side=tk.TOP)

    def name_button_clicked(self, attribute_name):
        # Acțiunea care trebuie efectuată atunci când un buton de nume este apăsat
        print(f"Name attribute clicked: {attribute_name}")

    def create_components_panel(self, left_pane):
        self.component_pane = tk.Frame(left_pane)
        left_pane.add(self.category_pane, minsize=200)
        left_pane.add(self.component_pane, minsize=200)

    def create_widgets(self):
        self.main_pane = tk.PanedWindow(self, orient=tk.HORIZONTAL, sashrelief=tk.SUNKEN, sashwidth=7)
        self.main_pane.pack(fill=tk.BOTH, expand=True)
        self.create_category_panel()

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

        # tk.Label(properties_pane, text="Culoare:").grid(row=0, column=0, padx=5, pady=5)
        # culoare_entry = tk.Entry(properties_pane)
        # culoare_entry.grid(row=0, column=1, padx=5, pady=5)
        #
        # tk.Label(properties_pane, text="Text:").grid(row=1, column=0, padx=5, pady=5)
        # text_entry = tk.Entry(properties_pane)
        # text_entry.grid(row=1, column=1, padx=5, pady=5)

        # buton_modificare = tk.Button(properties_pane, text="Modifică", command=self.modify)
        # buton_modificare.grid(row=2, columnspan=2, pady=10)

        self.create_buttons(self.component_pane, self.window.interior_frame, self.layer_pane)

    def create_buttons(self, window, window1, layers_tab):
        button = tk.Button(window, text="Create button!", command=lambda: self.create_button(window1, layers_tab))
        button.pack(pady=10, padx=10)

    def create_button(self, window, layers_tab):
        button1 = tk.Button(window, text=f"Created button{self.rows}!")
        button1.pack(side=tk.TOP)
        button2 = tk.Button(layers_tab, text=f"Layer button{self.rows}!")
        button2.pack(side=tk.TOP)

        self.rows += 1

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

        menubar.add_cascade(label="Setari", command=self.dummy_function)

    def dummy_function(self):
        print("Function to be implemented.")
