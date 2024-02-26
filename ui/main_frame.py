import os
import tkinter as tk
from datetime import datetime
from tkinter import filedialog

from ui.components.component_tree import ComponentsTree
from ui.frames.category_frame import CategoryFrame
from ui.frames.component_frame import ComponentFrame
from ui.frames.layer_frame import LayerFrame
from component.Frame.windowFrame_Custom import FrameWindowTK
from ui.util import file_util


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

        self.component.add_new_component("TK", FrameWindowTK, window=self.window)

        component_widget = self.component_tree.create_component_list()[0].return_component()

        self.window = component_widget

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
        folder_path = filedialog.askdirectory(title="Select where to save...")
        if folder_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            save_folder = os.path.join(folder_path, f"save_{timestamp}")
            self.component_tree.save_to_json_recursive(base_folder=save_folder)

    def action_open(self):
        if self.ui_create is False:
            self.create_widgets()
            self.ui_create = True
        folder_path = filedialog.askdirectory(title="Select a folder")

        if folder_path:
            # Dacă utilizatorul a selectat un director, încărcați datele
            self.load_from_folder_recursive(folder_path, window=self.window)
            print(f"Datele au fost încărcate din {folder_path}")

    def load_from_folder_recursive(self, folder_path, window):
        if len(self.frames_list) == 0:
            last_frame = self.middle_pane
        else:
            last_frame = self.frames_list[-1]
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)

            if os.path.isfile(file_path) and filename.endswith(".json"):
                file_util.transform_into_component(component_tree=self.component_tree, component_frame=self.component,
                                                   file_path=file_path, frames_list=self.frames_list, window=window)
                if self.frames_list[-1] is not last_frame:
                    last_frame = self.frames_list[-1]
                    for filename in os.listdir(folder_path):
                        folder_path_child = os.path.join(folder_path, filename)
                        if os.path.isdir(folder_path_child):
                            self.load_from_folder_recursive(folder_path_child, window=self.frames_list[-1])

    @staticmethod
    def dummy_function():
        print("Function to be implemented.")
