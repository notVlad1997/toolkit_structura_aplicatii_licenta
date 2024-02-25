import os
import tkinter as tk
from datetime import datetime
from tkinter import filedialog

from ui.components.component_tree import ComponentsTree
from ui.frames.category_frame import CategoryFrame
from ui.frames.component_frame import ComponentFrame
from ui.frames.layer_frame import LayerFrame
from ui.window_frame.window_frame import FrameWindowTK


class MainFrame(tk.Frame):
    def __init__(self, master):
        """
        Constructor. It creates the UI app.
        :param master: Main window
        """
        super().__init__(master)
        self.master = master
        self.window = None

        self.category = None
        self.component = None
        self.layer = None
        self.properties = None

        self.main_pane = None
        self.middle_pane = None
        self.windows_pane = None

        self.pack(fill=tk.BOTH, expand=True)

        self.component_list = []
        self.frames_list = []
        self.windows_buttons = []

        self.component_tree = ComponentsTree()

        self.current_window_id = -1
        self.ui_create = False
        self.create_menu()

    def create_widgets(self):
        """
        Method that implements the whole structure of the UI Interface.
        :return:
        """
        self.main_pane = tk.PanedWindow(self, orient=tk.HORIZONTAL, sashrelief=tk.SUNKEN, sashwidth=7)
        self.main_pane.pack(fill=tk.BOTH, expand=True)

        left_pane = tk.PanedWindow(self.main_pane, orient=tk.VERTICAL, sashrelief=tk.RAISED, sashwidth=7)

        self.middle_pane = tk.Frame(self.main_pane)
        self.middle_pane.pack_propagate(False)
        self.window = self.middle_pane

        right_pane = tk.PanedWindow(self.main_pane, orient=tk.VERTICAL, sashrelief=tk.RAISED, sashwidth=7)

        self.category = CategoryFrame(master=left_pane)

        layer_frame = LayerFrame(master=right_pane, component_tree=self.component_tree, window=self.window,
                                 frames_list=self.frames_list)

        self.component = ComponentFrame(master=left_pane, frames_list=self.frames_list,
                                        layer_frame=layer_frame, component_tree=self.component_tree)

        self.windows_pane = tk.Frame(self.middle_pane, height=30, highlightbackground="gray60", highlightthickness=1)
        self.windows_pane.pack(fill=tk.X)
        self.windows_pane.id = "New Windows"

        self.component.add_new_component("TK", FrameWindowTK, window=self.window)

        component_widget = self.component_tree.create_component_list()[0].return_component()

        self.window = component_widget

        self.category.create_category_panel(component_frame=self.component, frame_list=self.frames_list,
                                            window=self.window)

        self.main_pane.add(left_pane, minsize=200)
        self.main_pane.add(self.middle_pane, minsize=600)
        self.main_pane.add(right_pane, minsize=500)

    def create_menu(self):
        """
        Method that implements the header.
        :return:
        """
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

    def action_new(self):
        """
        Method that creates a new tab of window.
        :return:
        """
        # self.current_window_id = self.current_window_id + 1
        # self.component_list.append(WindowComponents())
        # self.frames_list.append([])

        if self.ui_create is False:
            self.create_widgets()
            self.ui_create = True

        new_ui = tk.Button(self.windows_pane, text="Hello")
        # , command=lambda index=len(self.windows_buttons):
        # self.window_button_pressed(index=index))
        self.windows_buttons.append(new_ui)
        new_ui.pack(side=tk.LEFT, fill=tk.Y)

    def action_save(self):
        """
        Method that saves all the components into their JSON file.
        :return:
        """
        # file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        #
        # if file_path:
        #     self.component_tree.save_to_json_recursive(folder_path=file_path)
        folder_path = filedialog.askdirectory(title="Select where to save...")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        save_folder = os.path.join(folder_path, f"save_{timestamp}")
        self.component_tree.save_to_json_recursive(base_folder=save_folder)

    def action_open(self):
        print("NOT FIXED")

    @staticmethod
    def dummy_function():
        print("Function to be implemented.")
