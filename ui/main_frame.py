import tkinter as tk

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

    def create_components_panel(self):
        left_pane = tk.PanedWindow(self.main_pane, orient=tk.VERTICAL, sashrelief=tk.RAISED, sashwidth=7)
        self.main_pane.add(left_pane, minsize=200)

        self.category_pane = tk.Canvas(left_pane, width=500, height=500)
        scrollbar = tk.Scrollbar(self.category_pane, command=self.category_pane.yview)
        self.category_pane.config(yscrollcommand=scrollbar.set, scrollregion=(0, 0, 0, 2000))
        self.category_pane.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.component_pane = tk.Frame(left_pane)
        left_pane.add(self.category_pane, minsize=200)
        left_pane.add(self.component_pane, minsize=200)

    def create_widgets(self):
        self.main_pane = tk.PanedWindow(self, orient=tk.HORIZONTAL, sashrelief=tk.SUNKEN, sashwidth=7)
        self.main_pane.pack(fill=tk.BOTH, expand=True)
        self.create_components_panel()

        middle_pane = tk.PanedWindow(self.main_pane, orient=tk.VERTICAL, sashrelief=tk.RAISED, sashwidth=7)
        self.main_pane.add(middle_pane, minsize=200)
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
