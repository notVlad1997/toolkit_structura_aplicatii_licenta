import tkinter as tk

from ui.window import FrameWindow


class MainFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.main_pane = None
        self.master = master
        self.config(width=600, height=600)
        self.create_widgets()
        self.pack(fill=tk.BOTH, expand=True)
        self.rows = 1

        self.create_menu()

    def create_widgets(self):
        self.main_pane = tk.PanedWindow(self, orient=tk.HORIZONTAL, sashrelief=tk.SUNKEN, sashwidth=7)
        self.main_pane.pack(fill=tk.BOTH, expand=True)

        left_pane = tk.PanedWindow(self.main_pane, orient=tk.VERTICAL, sashrelief=tk.RAISED, sashwidth=7)
        self.main_pane.add(left_pane, minsize=200)

        top_left_pane = tk.Canvas(left_pane, width=500, height=500)
        scrollbar = tk.Scrollbar(top_left_pane, command=top_left_pane.yview)
        top_left_pane.config(yscrollcommand=scrollbar.set, scrollregion=(0, 0, 0, 2000))
        top_left_pane.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        bottom_left_pane = tk.Frame(left_pane)
        left_pane.add(top_left_pane, minsize=200)
        left_pane.add(bottom_left_pane, minsize=200)

        middle_pane = FrameWindow(self.main_pane)
        self.main_pane.add(middle_pane, minsize=600)

        right_pane = tk.PanedWindow(self.main_pane, orient=tk.VERTICAL, sashrelief=tk.RAISED, sashwidth=7)
        self.main_pane.add(right_pane, minsize=100)
        right_pane.pack_propagate(False)

        top_right_pane = tk.Canvas(right_pane, width=500, height=500)
        scrollbar = tk.Scrollbar(top_right_pane, command=top_right_pane.yview)
        top_right_pane.config(yscrollcommand=scrollbar.set, scrollregion=(0, 0, 0, 2000))
        top_right_pane.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        bottom_right_pane = tk.Frame(right_pane)
        right_pane.add(top_right_pane, minsize=200)
        right_pane.add(bottom_right_pane, minsize=200)

        tk.Label(bottom_right_pane, text="Culoare:").grid(row=0, column=0, padx=5, pady=5)
        culoare_entry = tk.Entry(bottom_right_pane)
        culoare_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(bottom_right_pane, text="Text:").grid(row=1, column=0, padx=5, pady=5)
        text_entry = tk.Entry(bottom_right_pane)
        text_entry.grid(row=1, column=1, padx=5, pady=5)

        buton_modificare = tk.Button(bottom_right_pane, text="Modifică", command=self.modify)
        buton_modificare.grid(row=2, columnspan=2, pady=10)

        self.create_buttons(bottom_left_pane, middle_pane.interior_frame, top_right_pane)

    def create_buttons(self, window, window1, window2):
        button = tk.Button(window, text="Create button!", command=lambda: self.create_button(window1, window2))
        button.pack(pady=10, padx=10)

    def create_button(self, window, layer):
        button1 = tk.Button(window, text=f"Created button{self.rows}!")
        button1.pack(side=tk.TOP)
        button2 = tk.Button(layer, text=f"Layer button{self.rows}!")
        button2.pack(side=tk.TOP)
        #canvas.add(button1)
        # canvas.create_window((20, 10 + (self.rows - 1) * 30), window=button1, anchor="nw")
        #
        # canvas.update_idletasks()
        # canvas.config(scrollregion=canvas.bbox("all"))

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
